"""Audit completion provenance and derive coverage without changing frozen evidence."""
from collections import Counter
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import run_completion_supplement as runner
import verify_bundle
from audit_helpers import check_or_write, csv_text, require

ROOT = Path(__file__).resolve().parent
PROVIDERS = ("deepseek", "kimi", "glm", "longcat")
OUTCOMES = ("with_toolkit", "without_toolkit", "tie", "unresolved")


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_manifest(base, name):
    manifest = read(base / name)["sha256"]
    paths = [p for p in base.rglob("*") if p.is_file()]
    if name == "authors.lock.json":
        paths = [p for p in paths if "authors" in p.relative_to(base).parts]
    elif name == "judgments.lock.json":
        paths = [p for p in paths if "judgments" in p.relative_to(base).parts]
    else:
        paths = [p for p in paths if p != base / name]
    require(set(manifest) == {p.relative_to(base).as_posix() for p in paths}, name)
    for relative, digest in manifest.items():
        path = (base / relative).resolve()
        require(path.is_relative_to(base.resolve()), relative)
        require(sha(path) == digest, relative)


def audit(root, check_primary=True):
    if check_primary:
        verify_bundle.check_primary(root)
    base = root / "completion-supplement"
    plan = read(base / "plan.json")
    # Auditing needs the frozen pure helpers, not the live network/CLI adapter.
    spec = importlib.util.spec_from_file_location("audited_frozen_harness", root / "harness-snapshot.py")
    h = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(h)
    require(h.sha(h.encode(plan)) == read(base / "commitment.json")["plan_sha256"], "Failed check: h.sha(h.encode(plan)) == read(base / 'commitment.json')['plan_sha256']")
    require(sha(root / "run_completion_supplement.py") == plan["runner_sha256"], "Failed check: sha(root / 'run_completion_supplement.py') == plan['runner_sha256']")
    require(runner.original_hashes(h, root) == plan["original_sha256"], "Failed check: runner.original_hashes(h, root) == plan['original_sha256']")
    require(plan["author_calls_planned"] == 20 and plan["judge_calls_planned"] == 10, "Failed check: plan['author_calls_planned'] == 20 and plan['judge_calls_planned'] == 10")
    for name in ("authors.lock.json", "judgments.lock.json", "bundle-manifest.json"):
        check_manifest(base, name)
    results = read(base / "results.json")["results"]
    require(len(results) == 10, 'Failed check: len(results) == 10')
    require(len({(r["provider"], r["pair_id"]) for r in results}) == 10, "Failed check: len({(r['provider'], r['pair_id']) for r in results}) == 10")
    author_count = judge_count = 0
    for provider, stratum in plan["strata"].items():
        frozen = read(root / "runs" / provider / "coordinator/frozen.json")
        originals = {t["pair_id"]: t for t in frozen["assignments"]}
        primary = read(root / "runs" / provider / "results.json")["results"]
        fences = read(root / "format-supplement" / provider / "results.json")["results"]
        already = {r["pair_id"] for r in primary + fences if r["status"] == "judged"}
        require({t["pair_id"] for t in stratum["assignments"]} == set(originals) - already, "Failed check: {t['pair_id'] for t in stratum['assignments']} == set(originals) - already")
        starts = Counter(t["run_order"][0] for t in stratum["assignments"])
        require(abs(starts["with_toolkit"] - starts["without_toolkit"]) <= 1, "Failed check: abs(starts['with_toolkit'] - starts['without_toolkit']) <= 1")
        settings = stratum["settings"]
        for task in stratum["assignments"]:
            for key in ("task_id", "family_id", "brief", "sources", "language", "task_type"):
                require(task[key] == originals[task["pair_id"]][key], "Failed check: task[key] == originals[task['pair_id']][key]")
            require(set(task["run_order"]) == {"with_toolkit", "without_toolkit"}, "Failed check: set(task['run_order']) == {'with_toolkit', 'without_toolkit'}")
            require(set(task["labels"]) == {"A", "B"}, "Failed check: set(task['labels']) == {'A', 'B'}")
            require(set(task["labels"].values()) == {"with_toolkit", "without_toolkit"}, "Failed check: set(task['labels'].values()) == {'with_toolkit', 'without_toolkit'}")
            pair = base / provider / "authors" / task["pair_id"]
            reports = {}
            for arm in task["run_order"]:
                folder = pair / arm
                request = read(folder / "request.json")
                require(request == {"model": settings["model"], "messages": runner.author_messages(h, frozen, task, arm),
                                   "stream": False, "max_tokens": settings["max_completion_tokens"], **stratum["extra_parameters"]}, "Failed check: request == {'model': settings['model'], 'messages': runner.author_messages(h, frozen, task, arm), 'stream': False, 'max_tokens': settings['max_completion_tokens'], **stratum['extra_parameters']}")
                record = read(folder / "execution.json")
                require(record["status"] == "response_complete", (provider, task["pair_id"], arm, record))
                raw = read(folder / "response.json")
                require(raw["model"] == settings["model"] == record["model_returned"], "Failed check: raw['model'] == settings['model'] == record['model_returned']")
                require(raw["choices"][0]["finish_reason"] == "stop", "Failed check: raw['choices'][0]['finish_reason'] == 'stop'")
                require(raw["usage"] == record["usage"], "Failed check: raw['usage'] == record['usage']")
                require(0 < record["usage"]["completion_tokens"] <= settings["max_completion_tokens"], "Failed check: 0 < record['usage']['completion_tokens'] <= settings['max_completion_tokens']")
                require(0 < record["usage"]["total_tokens"] <= settings["max_total_tokens"], "Failed check: 0 < record['usage']['total_tokens'] <= settings['max_total_tokens']")
                require(record["elapsed_seconds"] <= settings["timeout_seconds"], "Failed check: record['elapsed_seconds'] <= settings['timeout_seconds']")
                parsed = runner.parse_markdown(raw["choices"][0]["message"]["content"])
                require(parsed == read(folder / "parsed.json"), "Failed check: parsed == read(folder / 'parsed.json')")
                for name in ("report", "notes"):
                    require((folder / f"{name}.md").read_bytes() == parsed[name].encode("utf-8"), "Failed check: (folder / f'{name}.md').read_bytes() == parsed[name].encode('utf-8')")
                reports[arm] = parsed["report"]
                author_count += 1
            packet = read(base / provider / "judge-inputs" / f"{task['pair_id']}.json")
            expected = {"brief": task["brief"], "sources": task["sources"], "rubric": frozen["rubric"],
                        "reports": {label: reports[arm] for label, arm in task["labels"].items()}}
            require(packet == expected, 'Failed check: packet == expected')
            judge = base / provider / "judgments" / task["pair_id"]
            request = read(judge / "request.json")
            require(request["messages"] == [{"role": "system", "content": h.JUDGE_SYSTEM}, {"role": "user", "content": json.dumps(packet, ensure_ascii=False)}], "Failed check: request['messages'] == [{'role': 'system', 'content': h.JUDGE_SYSTEM}, {'role': 'user', 'content': json.dumps(packet, ensure_ascii=False)}]")
            require(request["model_requested"] == frozen["config"]["judge"]["model"], "Failed check: request['model_requested'] == frozen['config']['judge']['model']")
            record = read(judge / "execution.json")
            require(record["status"] == "response_complete" and record["tools_observed"] == 0, "Failed check: record['status'] == 'response_complete' and record['tools_observed'] == 0")
            events = [json.loads(line) for line in (judge / "response.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
            actual = [e["item"]["text"] for e in events if e.get("type") == "item.completed" and e.get("item", {}).get("type") == "agent_message"]
            usage_events = [e for e in events if e.get("type") == "turn.completed"]
            require(record["returncode"] == 0 and usage_events, "Failed check: record['returncode'] == 0 and usage_events")
            require(record["usage"] == usage_events[-1]["usage"], "Failed check: record['usage'] == usage_events[-1]['usage']")
            judge_settings = frozen["config"]["judge"]
            require(request["reasoning_effort"] == "low", "Failed check: request['reasoning_effort'] == 'low'")
            require(0 < record["usage"]["output_tokens"] <= judge_settings["max_completion_tokens"], "Failed check: 0 < record['usage']['output_tokens'] <= judge_settings['max_completion_tokens']")
            require(record["usage"]["input_tokens"] + record["usage"]["output_tokens"] <= judge_settings["max_total_tokens"], "Failed check: record['usage']['input_tokens'] + record['usage']['output_tokens'] <= judge_settings['max_total_tokens']")
            require(record["elapsed_seconds"] <= judge_settings["timeout_seconds"], "Failed check: record['elapsed_seconds'] <= judge_settings['timeout_seconds']")
            parsed = h.validate_judgment(read(judge / "parsed.json"))
            require(json.loads(actual[-1]) == parsed, 'Failed check: json.loads(actual[-1]) == parsed')
            require(not [e for e in events if e.get("type") in ("item.started", "item.completed") and e.get("item", {}).get("type") not in ("agent_message", "reasoning")], "Failed check: not [e for e in events if e.get('type') in ('item.started', 'item.completed') and e.get('item', {}).get('type') not in ('agent_message', 'reasoning')]")
            row = next(r for r in results if r["provider"] == provider and r["pair_id"] == task["pair_id"])
            require(row["status"] == "judged" and row["preference"] == parsed["preference"], "Failed check: row['status'] == 'judged' and row['preference'] == parsed['preference']")
            require(row["outcome"] == task["labels"].get(parsed["preference"], parsed["preference"]), "Failed check: row['outcome'] == task['labels'].get(parsed['preference'], parsed['preference'])")
            judge_count += 1
    require(author_count == 20 and judge_count == 10, 'Failed check: author_count == 20 and judge_count == 10')
    print(json.dumps({"completion_audit": "pass", "new_author_requests": author_count, "new_judgments": judge_count, "original_files_unchanged": len(plan["original_sha256"])}))
    return plan


def derive(root, plan, write=False):
    rows, scores, usage = [], [], []
    summary = {"scope": "Coverage of five reused development families under four author models; mixed primary and post-hoc settings, not a pooled primary effect estimate.",
               "families": 5, "models": 4, "general_quality_advantage_established": False, "coverage": {}, "completion_only": {}, "rows": rows}
    completion_results = read(root / "completion-supplement/results.json")["results"]
    for provider in PROVIDERS:
        frozen = read(root / "runs" / provider / "coordinator/frozen.json")
        by_task = {}
        for stage, base in (("primary", root / "runs" / provider), ("format_supplement", root / "format-supplement" / provider),
                            ("completion_supplement", root / "completion-supplement" / provider)):
            candidates = [r for r in completion_results if r["provider"] == provider] if stage == "completion_supplement" else read(base / "results.json")["results"]
            for r in candidates:
                if r["status"] != "judged":
                    continue
                require(r["task_id"] not in by_task, "A valid judgment was replaced")
                task = next(t for t in (plan["strata"][provider]["assignments"] if stage == "completion_supplement" else frozen["assignments"]) if t["pair_id"] == r["pair_id"])
                jp = base / "judgments" / r["pair_id"] / "parsed.json"
                judgment = read(jp)
                row = {"provider": provider, "task_id": r["task_id"], "pair_id": r["pair_id"], "stage": stage, "outcome": r["outcome"],
                       "judgment_path": jp.relative_to(root).as_posix()}
                by_task[r["task_id"]] = row
                for label, arm in task["labels"].items():
                    scores.append({**row, "language": task["language"], "condition": arm, "presentation": label,
                                   **{d: judgment["reports"][label][d]["score"] for d in frozen["rubric"]["dimensions"]}})
        require(len(by_task) == 5, 'Failed check: len(by_task) == 5')
        rows.extend(sorted(by_task.values(), key=lambda r: r["task_id"]))
        summary["coverage"][provider] = {"judged": 5, **dict(Counter(r["stage"] for r in by_task.values())),
                                         **{k: sum(r["outcome"] == k for r in by_task.values()) for k in OUTCOMES}}
        extra = [r for r in completion_results if r["provider"] == provider]
        summary["completion_only"][provider] = {"judged": len(extra), **{k: sum(r["outcome"] == k for r in extra) for k in OUTCOMES}}
        for p in sorted((root / "completion-supplement" / provider).rglob("execution.json")):
            record = read(p); u = record.get("usage", {})
            usage.append({"provider": provider, "role": "author" if "authors" in p.parts else "judge", "path": p.relative_to(root).as_posix(),
                          "status": record["status"], "input_tokens": u.get("prompt_tokens", u.get("input_tokens", "")),
                          "completion_tokens": u.get("completion_tokens", u.get("output_tokens", "")), "elapsed_seconds": record.get("elapsed_seconds", "")})
    require(len(rows) == 20 and len(scores) == 40 and len(usage) == 30, 'Failed check: len(rows) == 20 and len(scores) == 40 and (len(usage) == 30)')
    check_or_write(root, {"completion-summary.json": json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
                         "coverage-scores.csv": csv_text(scores), "completion-usage.csv": csv_text(usage)}, write)
    print(json.dumps({"coverage": summary["coverage"], "completion_only": summary["completion_only"]}))
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--verify-only", action="store_true", help="Compatibility alias for the read-only default")
    mode.add_argument("--write", action="store_true", help="Explicitly regenerate derived tables; preserve evidence and newline style")
    args = parser.parse_args()
    plan = audit(ROOT)
    derive(ROOT, plan, args.write)
