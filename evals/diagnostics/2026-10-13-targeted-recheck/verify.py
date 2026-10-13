"""Read-only consistency checks for this dated real-call and repair bundle."""
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]


def require(value, message):
    if not value:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(value):
    return hashlib.sha256(value).hexdigest()


def count(task, report):
    return len(report.split()) if task["language"] == "en" else sum(not c.isspace() for c in report)


def verify():
    manifest = read(BASE / "manifest.json")["sha256"]
    files = {p.relative_to(BASE).as_posix() for p in BASE.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.name != "manifest.json"}
    require(files == set(manifest), "Public inventory differs")
    for name, digest in manifest.items():
        require(sha((BASE / name).read_bytes()) == digest, "Changed public file: " + name)
    plan = read(BASE / "plan.json")
    canonical = json.dumps(plan, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    require(sha(canonical) == read(BASE / "commitment.json")["plan_sha256"], "Plan differs from commitment")
    tasks = {t["task_id"]: t for t in plan["tasks"]}
    authors = read(BASE / "author-results.json")
    repairs = read(BASE / "repair-plan.json")["rows"]
    summary = read(BASE / "summary.json")
    require(len(summary["rows"]) == len(authors["rows"]) == 16, "Report count differs")
    require(len({(r["provider"], r["task_id"]) for r in summary["rows"]}) == 16, "Duplicate report")
    initial_count = revised_count = first_pass = reused = 0
    for row in summary["rows"]:
        provider, tid = row["provider"], row["task_id"]
        task = tasks[tid]
        a = next(a for a in authors["rows"] if (a["provider"], a["task_id"]) == (provider, tid))
        folder = BASE / "authors" / provider / tid
        original = read(folder / "initial/parsed.json")["report"]
        selected = read(folder / "selected.json")["report"]
        for report, measurement in [(original, a["initial_length"]), (selected, a["current_length"])]:
            actual = count(task, report)
            require(actual == measurement["actual"], "Incorrect report count")
            require(measurement["met"] == (task["minimum"] <= actual <= task["maximum"]), "Incorrect length verdict")
        require(read(folder / a["selected"] / "parsed.json")["report"] == selected, "Selected author version differs")
        initial_count += a["initial_length"]["met"]
        revised_count += a["current_length"]["met"]
        label = next(k for k, v in plan["labels_coordinator_only"][tid].items() if v == provider)
        review = next(r for r in read(BASE / "judges" / tid / "review.json")["reviews"] if r["label"] == label)
        require(review["verdict"] == row["first_astra_verdict"], "First review changed")
        first_pass += review["verdict"] == "pass"
        path = BASE / row["report_path"]
        report = read(path)["report"] if path.suffix == ".json" else path.read_text(encoding="utf-8").strip()
        require(sha(report.encode()) == row["report_sha256"], "Final report identity differs")
        require(count(task, report) == row["length"] and task["minimum"] <= row["length"] <= task["maximum"], "Final length differs")
        if row["astra_review"].startswith("evals/"):
            review_path = ROOT / row["astra_review"]
            packet = json.loads(read(review_path.parent / "request.json")["messages"][1]["content"])
            require(packet["brief"] == task["brief"] and packet["sources"] == task["sources"] and packet["report"].strip() == report, "Reused review inputs differ")
            verdict = read(review_path)["verdict"]
            reused += 1
        else:
            review_path = BASE / row["astra_review"]
            packet = read(review_path.parent / "packet.json")
            require(next(r for r in packet["reports"] if r["label"] == label)["report"] == report, "Review covers different report")
            if row["final_type"] == "maintainer_repair":
                require(packet["sources"] == task["sources"], "Corrected review omitted source metadata")
            verdict = next(r for r in read(review_path)["reviews"] if r["label"] == label)["verdict"]
        require(verdict == row["final_verdict"] == "pass", "Final review is not a pass")
    executions = list(BASE.glob("authors/*/*/*/execution.json")) + list(BASE.glob("judges/*/execution.json")) + list(BASE.glob("repair-judges/*/execution.json"))
    require(len(executions) == summary["total_new_requests"] == 31 <= plan["limits"]["total_max"], "Request accounting differs")
    require(all(read(p)["status"] == "response_complete" for p in executions), "Execution not complete")
    invalid = list(BASE.glob("authors/*/*/length-revision/invalid.json"))
    require(len(invalid) == summary["invalid_author_revisions"] == 1, "Lost format failure")
    require((initial_count, revised_count, first_pass, reused, len(repairs)) == (summary["initial_length_passes"], summary["after_author_revision_length_passes"], summary["first_astra_passes"], summary["reused_identical_prior_astra_passes"], summary["maintainer_repairs"]), "Summary differs from evidence")
    return {k: summary[k] for k in ("independent_tasks", "total_new_requests", "first_astra_passes", "maintainer_repairs", "accepted_final_versions")}


if __name__ == "__main__":
    print(json.dumps(verify()))
