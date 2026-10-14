"""Read-only checks of this public run record; no models or semantic grading."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def require(condition, message):
    if not condition:
        raise ValueError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    hashes = read(HERE / "artifact-hashes.json")
    files = {p.relative_to(HERE).as_posix() for p in HERE.rglob("*")
             if p.is_file() and p.name != "artifact-hashes.json" and "__pycache__" not in p.parts}
    require(files == set(hashes), "Public file inventory changed")
    for name, expected in hashes.items():
        require(digest(HERE / name) == expected, "Changed public bytes: " + name)
    summary = read(HERE / "summary.json")
    mapping = read(HERE / "blind-map.json")
    totals = {key: 0 for key in summary["total_recorded_usage"]}
    for path in sorted((HERE / "execution").glob("*/*/execution.json")) + sorted((HERE / "blind").glob("*/execution.json")):
        run = read(path)
        events = [json.loads(line) for line in (path.parent / "events.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
        complete = [event["usage"] for event in events if event["type"] == "turn.completed"]
        for key in totals:
            measured = sum(u.get(key, 0) for u in complete)
            require(measured == run.get("usage", {}).get(key, 0), "Event usage mismatch: " + str(path))
            totals[key] += measured
    require(totals == summary["total_recorded_usage"], "Usage total changed")
    for arm, execution in summary["author_sessions"].items():
        require(execution["exit_code"] == 0 and not execution["errors"], "Incomplete author run")
        require(execution["completed_item_counts"]["web_search"] > 0, "Missing actual web-tool activity")
        for name, record in execution["artifacts"].items():
            path = HERE / "reports" / arm / name
            require(digest(path) == record["sha256"], "Report binding mismatch")
            count = len("".join(path.read_text(encoding="utf-8").split()))
            require(count == record["nonwhitespace_characters"], "Report count mismatch")
    for stage, name in (("first", "first-draft.md"), ("final", "final.md")):
        folder = HERE / "blind" / stage
        bindings, manifest, response = (read(folder / f) for f in ("bindings.json", "input-manifest.json", "response.json"))
        require(bindings["reports"] == manifest["reports"], "Blind input binding mismatch")
        require(len(bindings["sources"]) == manifest["source_count"], "Source inventory mismatch")
        for label in ("A", "B"):
            require(digest(HERE / "reports" / mapping[label] / name) == bindings["reports"][label]["sha256"], "Wrong anonymous report")
            result = response["reports"][label]
            recorded = summary["blind_reviews"][stage]["reports"][label]
            require(sum(result["scores"].values()) * 5 == recorded["score"], "Score transcription changed")
            require(result["findings"] == recorded["findings"] and result["verdict"] == recorded["verdict"], "Finding transcription changed")
        require(response["preference"] == summary["blind_reviews"][stage]["preference"], "Preference transcription changed")
    replay = read(HERE / "encoding-replay.json")
    require(replay["before"]["source_sha256"] == replay["after"]["source_sha256"], "Encoding replay used different material")
    require(replay["before"]["unicode_encode_error"] and replay["after"]["valid_utf8_json"], "Encoding replay result changed")
    print(f"PASS: {len(hashes)} public files, four full reports, two bound blind judgments and recorded usage agree; semantic quality is not re-evaluated.")

if __name__ == "__main__":
    main()
