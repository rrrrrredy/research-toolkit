"""Read-only checks for retained completion and targeted review records."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def matches_recorded_bytes(path, expected):
    # Reviewers recorded actual Windows bytes; Git checkouts may convert newlines.
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return expected.lower() in {
        hashlib.sha256(data).hexdigest(),
        hashlib.sha256(data.replace(b"\n", b"\r\n")).hexdigest(),
    }


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    review = read(ROOT / "reviews/02-review.json")
    report = ROOT / "report.zh-CN.md"
    require(digest(report) == review["report_sha256"], "Final review must bind current report")
    require(digest(report) == digest(ROOT / "versions/02-report.zh-CN.md"), "Retain final version")
    count = sum(not c.isspace() for c in report.read_text(encoding="utf-8"))
    require(count == review["nonwhitespace_characters"] and 3500 <= count <= 6000, "Actual length mismatch")
    require(review["verdict"] == "pass" and not review["necessary_findings"], "Final review has unresolved findings")
    expected = {"R%02d" % i for i in range(1, 14)}
    require({v["requirement_id"] for v in review["requirements"]} == expected, "Missing requirement")
    require(all(v["status"] == "pass" for v in review["requirements"]), "Unclosed requirement")
    first = read(ROOT / "reviews/01-review.json")
    require(first["verdict"] == "revise", "Retain original negative verdict")
    require(digest(ROOT / "versions/01-report.zh-CN.md") == first["report_sha256"].lower(), "Retain first report")
    context = read(ROOT / "reviews/02-context.json")
    require(context["fresh_context"] and not context["prior_review_verdicts_or_labels_received"], "Separate review context")
    for filename in ("report.zh-CN.md", "sources.md", "source-receipt.json"):
        bound = [v for v in context["reviewer_inputs"] if v["path"].replace("\\", "/").endswith("/" + filename)]
        require(len(bound) == 1 and matches_recorded_bytes(ROOT / filename, bound[0]["sha256"]), "Changed reviewed input: " + filename)
    progress = [json.loads(line) for line in (ROOT / "progress.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    require(progress[-1]["report_sha256"] == digest(report) and progress[-1]["review"].startswith("completed:"), "Completion receipt missing")
    wording = ROOT.parent / "2026-10-13-wording-recheck"
    context = read(wording / "context.json")
    require(context["fresh_context"], "Wording review must use separate context")
    # The model records the exact received packet, not the coordinator mapping.
    require(matches_recorded_bytes(wording / "judge-input.json", context["input_sha256"]), "Wording input binding mismatch")
    cases = {v["id"]: v for v in read(wording / "review.json")["cases"]}
    mapping = read(wording / "coordinator-map.json")
    require(set(cases) == {v["id"] for v in mapping} and len(cases) == 4, "Wording case coverage mismatch")
    for row in mapping:
        for candidate in ("A", "B"):
            expected_label = "flawed" if row[candidate] == "bad" else "acceptable"
            require(cases[row["id"]][candidate]["judgment"] == expected_label, "Recorded targeted judgment changed")
    print("Pipeline: 13 recorded requirements pass; 5244 characters; original revision finding retained.")
    print("Wording recheck: 4 tasks / 8 candidate judgments retained; record consistency only.")


if __name__ == "__main__":
    main()
