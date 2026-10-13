"""Read-only verification of the seven complete-report calls and retained repairs."""
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def request_packet(folder):
    request = read(folder / "request.json")
    require(request["model"] == "gpt-6-astra", "Unexpected requested model")
    require([m["role"] for m in request["messages"]] == ["system", "user"], "Unexpected context")
    return json.loads(request["messages"][1]["content"])


def verify():
    manifest = read(BASE / "manifest.json")["files"]
    actual_files = {p.relative_to(BASE).as_posix() for p in BASE.rglob("*") if p.is_file()
                    and p.name != "manifest.json" and "__pycache__" not in p.parts}
    require(actual_files == set(manifest), "Manifest inventory changed")
    for name, expected in manifest.items():
        require(digest((BASE / name).read_text(encoding="utf-8")) == expected, f"Changed file: {name}")
    plan = read(BASE / "plan.json")
    require(digest(json.dumps(plan, ensure_ascii=False, sort_keys=True)) == read(BASE / "plan-hash.json")["sha256"], "Changed pre-call plan")
    for name, expected in plan["code_hashes"].items():
        require(digest((BASE / name).read_text(encoding="utf-8")) == expected, f"Changed execution snapshot: {name}")
    summary = read(BASE / "summary.json")
    tasks = {t["case_id"]: t for t in plan["tasks"]}
    require(len(tasks) == len(summary["rows"]) == 7, "Expected seven distinct original tasks")
    require(set(tasks) == {r["case_id"] for r in summary["rows"]}, "Task set mismatch")
    initial_length_passes = first_review_passes = accepted = 0
    for row in summary["rows"]:
        case = row["case_id"]; task = tasks[case]
        author = BASE / "authors" / case / "initial"
        judge = BASE / "judges" / case / "initial"
        authored = request_packet(author); judged = request_packet(judge)
        require(authored["task"] == judged["task"] == task, f"Author/judge task or source mismatch: {case}")
        require(authored["toolkit_methods"] == plan["methods"], f"Changed author methods: {case}")
        require(set(judged) == {"task", "report", "measurement"}, "Author notes or identity entered initial judge input")
        original = (author / "report.md").read_text(encoding="utf-8")
        require(read(author / "parsed.json")["report"] == original == judged["report"], "Original report changed before review")
        n = sum(not c.isspace() for c in original)
        require(n == row["initial_length"] == judged["measurement"]["actual"], "Incorrect initial count")
        initial_length_passes += task["minimum"] <= n <= task["maximum"]
        first = read(judge / "parsed.json")
        require(first["verdict"] == row["first_review"], "First verdict changed")
        first_review_passes += first["verdict"] == "pass"
        report = (BASE / row["report"]).read_text(encoding="utf-8")
        n = sum(not c.isspace() for c in report)
        require(n == row["selected_length"] and task["minimum"] <= n <= task["maximum"], "Selected report length mismatch")
        require(digest(report) == row["report_sha256"], "Selected report hash mismatch")
        review_path = BASE / row["review"]; review = read(review_path)
        require(request_packet(review_path.parent)["report"] == report, "Selected review covers different report")
        require(request_packet(review_path.parent)["task"] == task, "Repair judge source mismatch")
        require(review["verdict"] == row["review_verdict"] == "pass" and not review["findings"], "Selected report not accepted")
        accepted += 1
        if row["selected_version"] != "initial":
            edit = read(BASE / "authors" / case / row["selected_version"] / "edit.json")
            require(original.replace(edit["edit"]["deleted_exact_text"], "", 1) == report, "Unexpected maintainer edit")
            require(row["delivery_scope"] == "stage_only_R04_R05_open", "Stage scope lost")
            require(review["full_task_complete"] is False and review["stage_delivery_appropriate"] is True, "Stage misreported as full completion")
    executions = list(BASE.glob("authors/*/*/execution.json")) + list(BASE.glob("judges/*/*/execution.json"))
    require(len(executions) == summary["total_model_calls"] == 15, "Call count mismatch")
    usage = {k: 0 for k in summary["usage"]}
    for path in executions:
        record = read(path); folder = path.parent
        require(record["status"] == "response_complete" and record["exit_code"] == 0, "Unresolved execution")
        events = [json.loads(line) for line in (folder / "events.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
        completed = [e for e in events if e["type"] == "turn.completed"]
        replies = [e["item"]["text"] for e in events if e["type"] == "item.completed" and e.get("item", {}).get("type") == "agent_message"]
        require(len(completed) == len(replies) == 1, "Missing or ambiguous actual model return")
        require(json.loads(replies[0]) == read(folder / "parsed.json"), "Parsed output differs from original model return")
        require(completed[0]["usage"] == record["usage"], "Usage differs from execution")
        for key in usage:
            usage[key] += record["usage"].get(key, 0)
    require(usage == summary["usage"], "Usage total mismatch")
    require((initial_length_passes, first_review_passes, accepted) == (6, 6, 7), "Result totals mismatch")
    require((summary["initial_length_passes"], summary["first_review_passes"], summary["selected_texts_accepted"]) == (6, 6, 7), "Summary totals mismatch")
    require(summary["accepted_for_supplied_source_task"] == 6 and summary["stage_reports_with_open_requirements"] == 1, "Delivery scope counts changed")
    require(summary["live_13_turn_replay"] is False and summary["full_agent_filesystem_or_mcp_run"] is False, "Execution scope overstated")
    return {"tasks": 7, "model_calls": 15, "first_reviews_passed": 6,
            "selected_texts_accepted": 7, "stage_only": 1, "model_calls_during_verification": 0}


if __name__ == "__main__":
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
