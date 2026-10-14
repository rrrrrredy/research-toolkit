"""Small local observations, separate from research inputs and acceptance."""
from __future__ import annotations
from datetime import datetime, timezone
import json
import time


def now():
    return datetime.now(timezone.utc).isoformat()


def timed_capture(capture, started_at, started):
    return {**capture, "started_at": started_at, "finished_at": now(),
            "elapsed_seconds": round(time.monotonic() - started, 6)}


def capture_usage(capture):
    """Use returned usage only; cached tokens are a subset, never added twice."""
    raw = []
    try:
        if capture.get("backend") == "generic":
            raw = [json.loads(capture["response"]).get("usage", {})]
        elif capture.get("format") == "codex-jsonl":
            raw = [e.get("usage", {}) for line in capture.get("stdout", "").split("\n") if line.strip()
                   for e in [json.loads(line)] if e.get("type") == "turn.completed"]
        elif capture.get("format") in {"json", "claude-json"}:
            raw = [json.loads(capture["stdout"]).get("usage", {})]
    except (ValueError, KeyError, TypeError, AttributeError):
        return None
    totals = {}
    for usage in raw:
        if not isinstance(usage, dict):
            continue
        values = {"input_tokens": usage.get("input_tokens", usage.get("prompt_tokens")),
                  "output_tokens": usage.get("output_tokens", usage.get("completion_tokens"))}
        cached = usage.get("cached_input_tokens")
        details = usage.get("prompt_tokens_details")
        if cached is None and isinstance(details, dict):
            cached = details.get("cached_tokens")
        values["cached_input_tokens"] = cached
        # Claude reports cache reads/writes separately from its input_tokens.
        if capture.get("format") == "claude-json":
            read, write = usage.get("cache_read_input_tokens"), usage.get("cache_creation_input_tokens")
            if all(type(v) is int and v >= 0 for v in (values["input_tokens"], read, write)):
                values["input_tokens"] += read + write
                values["cached_input_tokens"] = read
                values["cache_write_input_tokens"] = write
            else:
                values.pop("input_tokens")  # Do not report a partial total as complete.
        for key, value in values.items():
            if type(value) is int and value >= 0:
                totals[key] = totals.get(key, 0) + value
    return totals or None


def record_event(root, event):
    from research_workflow import safe_path
    path = safe_path(root, "logs/activity.jsonl")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(event, ensure_ascii=False) + "\n")


def _activity_summary(root):
    from research_workflow import safe_path
    events, warnings = [], []
    path = safe_path(root, "logs/activity.jsonl")
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                row = json.loads(line)
                if isinstance(row, dict):
                    events.append(row)
            except ValueError:
                warnings.append("Unreadable activity row; original retained.")
    first = next((e for e in events if e.get("complete_draft") and e.get("outcome") == "saved"), None)
    start = next((e.get("started_at") for e in events if e.get("operation") == "start"), None)
    elapsed = None
    if first and start:
        try:
            elapsed = (datetime.fromisoformat(first["finished_at"]) - datetime.fromisoformat(start)).total_seconds()
        except (ValueError, KeyError, TypeError):
            warnings.append("Draft interval unavailable; original observations retained.")
    attempts, totals, self_submissions = [], {}, 0
    # Only actual invocation captures; reusing a review creates no new capture.
    reviews = safe_path(root, "reviews")
    if reviews.exists():
        for path in sorted(reviews.rglob("execution.json")):
            try:
                path.resolve().relative_to(root.resolve())
                capture = json.loads(path.read_text(encoding="utf-8"))
                if capture.get("external_execution") is False:
                    self_submissions += 1
                    continue
                usage = capture_usage(capture)
                attempts.append({"path": path.relative_to(root).as_posix(),
                                 "elapsed_seconds": capture.get("elapsed_seconds"), "usage": usage})
                for key, value in (usage or {}).items():
                    totals[key] = totals.get(key, 0) + value
            except (ValueError, OSError, AttributeError):
                warnings.append("Unreadable invocation capture: " + str(path.relative_to(root)))
    retry_groups, failed = {}, 0
    history = safe_path(root, "logs/review.jsonl")
    if history.exists():
        for line in history.read_text(encoding="utf-8").splitlines():
            try:
                row = json.loads(line)
                if row.get("record_type") != "model_review" or row.get("reviewer") == "self":
                    continue
                key = (row.get("slot_id"), row.get("artifact_sha256"), json.dumps(row.get("input"), sort_keys=True))
                retry_groups.setdefault(key, set()).add(row.get("attempt_id"))
                failed += row.get("status") != "completed"
            except (ValueError, AttributeError, TypeError):
                warnings.append("Unreadable review activity row; original retained.")
    return {"task_started_at": start, "first_complete_draft": first, "seconds_to_first_complete_draft_observation": elapsed,
            "save_attempts": len([e for e in events if e.get("operation") == "save"]),
            "failed_saves": len([e for e in events if e.get("operation") == "save" and e.get("outcome") == "error"]),
            "review_invocations": attempts, "observed_review_usage": totals or None,
            "failed_review_attempts": failed, "review_retries": sum(max(0, len(ids) - 1) for ids in retry_groups.values()),
            "self_review_submissions": self_submissions,
            "review_invocations_without_usage": sum(a["usage"] is None for a in attempts),
            "author_usage": None, "warnings": warnings,
            "scope": "Tool-observed draft saves and invocation captures; no host author usage, billing or quality inference."}


def activity_summary(root):
    try:
        return _activity_summary(root)
    except (OSError, ValueError, TypeError):
        return {"warnings": ["Activity summary unavailable; research and delivery checks are unchanged."],
                "author_usage": None, "observed_review_usage": None}
