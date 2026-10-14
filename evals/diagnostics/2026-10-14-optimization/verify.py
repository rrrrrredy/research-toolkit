"""Read-only verification of retained public bytes; no model calls or quality scoring."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    summary = read(HERE / "workflow-results.json")
    for call in summary["calls"]:
        stem = "astra-" + call["phase"]
        for kind in ("request", "response"):
            require(sha(HERE / f"{stem}-{kind}.json") == call[f"{kind}_sha256"], f"Changed {stem} {kind}")
        request = read(HERE / f"{stem}-request.json")
        response = read(HERE / f"{stem}-response.json")
        require(hashlib.sha256(request["assignment"]["report"].encode()).hexdigest() == call["report_sha256"], "Changed submitted report")
        report_name = "report-lite.md" if call["phase"] == "initial" else "report-updated.md"
        require(request["assignment"]["report"] == (HERE / report_name).read_text(encoding="utf-8"), "Report differs from submission")
        events = [json.loads(line) for line in (HERE / f"{stem}-events.jsonl").read_text(encoding="utf-8").splitlines()]
        turns = [e for e in events if e.get("type") == "turn.completed"]
        answers = [json.loads(e["item"]["text"]) for e in events if e.get("item", {}).get("type") == "agent_message"]
        require(len(turns) == 1 and turns[0]["usage"] == call["usage"], "Usage mismatch")
        require(answers == [response], "Response differs from retained events")
    for key, total in summary["usage"].items():
        require(sum(c["usage"].get(key, 0) for c in summary["calls"]) == total, "Usage total mismatch")
    for name, count in summary["report_counts"].items():
        require(len((HERE / name).read_text(encoding="utf-8").split()) == count, "Report count mismatch")
    for key in ("historical_first", "historical_repaired"):
        require(sha(REPO / summary[key]["path"]) == summary[key]["sha256"], "Historical report changed")
    print("Public request/report/response bindings, events, usage and historical bytes verified; no new semantic judgment.")


if __name__ == "__main__":
    main()
