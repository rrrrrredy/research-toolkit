"""Complete previously unjudged development pairs; never replace a valid judgment."""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import random
import sys
import time
import urllib.error
import urllib.request

HERE = Path(__file__).resolve().parent
SEPARATOR = "\n<!-- WORKING_NOTES -->\n"
FORMAT = ("Return the complete reader-facing Markdown report first, then exactly one line "
          "containing <!-- WORKING_NOTES -->, then your separate working notes. "
          "Do not wrap the response in JSON or a Markdown code fence. "
          "Do not include this separator anywhere else.")
PROVIDERS = ("deepseek", "glm", "longcat")
EXTRAS = {"deepseek": {"reasoning_effort": "low"},
          "glm": {"reasoning_effort": "low"},
          "longcat": {"thinking": {"type": "enabled"}}}


def load_source(source):
    # The original adapter and harness are imported unchanged.
    os.environ.setdefault("RESEARCH_TOOLKIT_ROOT", str(HERE.parents[2]))
    sys.path.insert(0, str(source))
    import run_live_study as live
    spec = importlib.util.spec_from_file_location("frozen_completion_harness", source / "harness-snapshot.py")
    h = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(h)
    live.h = h
    return h, live


def parse_markdown(content):
    if not isinstance(content, str) or content.count(SEPARATOR) != 1:
        raise ValueError("Expected exactly one report/notes delimiter on its own line")
    report, notes = content.split(SEPARATOR)
    if not report.strip() or not notes.strip():
        raise ValueError("Both report and working notes must be nonempty")
    # No trimming, escape repair, reflow, factual editing or quality-based rejection.
    return {"report": report, "notes": notes}


def author_messages(h, frozen, task, condition):
    messages = h.author_messages(frozen, task, condition)
    old = "Return a JSON object with report (the complete reader-facing Markdown report) and notes (separate working notes)."
    assert old in messages[0]["content"]
    messages[0]["content"] = messages[0]["content"].replace(old, FORMAT, 1) + "\n\nOutput format for this request: " + FORMAT
    return messages


def original_hashes(h, source):
    paths = []
    for name in ("inputs", "runs", "format-supplement"):
        paths.extend(p for p in (source / name).rglob("*") if p.is_file())
    paths += [source / n for n in ("study-plan.json", "format-supplement-policy.json", "run_live_study.py", "run_format_supplement.py", "harness-snapshot.py")]
    return {p.relative_to(source).as_posix(): h.sha(p.read_bytes()) for p in sorted(paths)}


def prepare(h, source, output, seed):
    output.mkdir(parents=True, exist_ok=False)
    strata = {}
    for provider in PROVIDERS:
        frozen = h.read(source / "runs" / provider / "coordinator/frozen.json")
        primary = h.read(source / "runs" / provider / "results.json")["results"]
        supplement = h.read(source / "format-supplement" / provider / "results.json")["results"]
        judged = {r["pair_id"] for r in primary + supplement if r["status"] == "judged"}
        tasks = [dict(t) for t in frozen["assignments"] if t["pair_id"] not in judged]
        order = random.Random(f"{seed}:{provider}:order-v1")
        labels = random.Random(f"{seed}:{provider}:labels-v1")
        order.shuffle(tasks)
        starts = ["with_toolkit", "without_toolkit"] * (len(tasks) // 2)
        if len(tasks) % 2:
            starts.append(order.choice(["with_toolkit", "without_toolkit"]))
        order.shuffle(starts)
        for task, first in zip(tasks, starts):
            task["run_order"] = [first, "without_toolkit" if first == "with_toolkit" else "with_toolkit"]
            arms = ["with_toolkit", "without_toolkit"]
            labels.shuffle(arms)
            task["labels"] = dict(zip(("A", "B"), arms))
        settings = dict(frozen["config"]["author"])
        settings.update(max_completion_tokens=32768, max_total_tokens=131072, timeout_seconds=1200)
        strata[provider] = {"settings": settings, "extra_parameters": EXTRAS[provider], "assignments": tasks}
    plan = {
        "analysis_type": "post_hoc_completion_supplement",
        "created_at": datetime.now(timezone.utc).isoformat(), "seed": seed,
        "selection": "Every model/task pair without a valid primary or exact-fence judgment; both author arms regenerated. Valid judgments are never rerun.",
        "scope": "Same five development families, briefs, sources, pinned Toolkit text and rubric. Not new independent tasks, held-out data, or replacement primary results.",
        "format": FORMAT, "separator": SEPARATOR,
        "reason_for_changes": {"deepseek": "Three Toolkit responses exhausted the 12288 completion-token budget, including reasoning. Raise both-arm ceiling and use documented low effort.",
                               "glm": "Two pairs have malformed JSON, including unescaped quotations/control characters. Avoid JSON-string transport for Markdown in both arms; retain original failures.",
                               "longcat": "Six of ten calls hit the 240-second client timeout; two completed replies used fences. Raise the request deadline, enlarge both-arm completion ceiling, and separate raw Markdown from notes."},
        "glm_route": "Coding Plan was tried first in the original session and returned an expired-subscription error; ordinary API fallback retained.",
        "provider_docs": ["https://api-docs.deepseek.com/guides/thinking_mode/", "https://longcat.ai/platform/docs/zh/api/chat"],
        "author_calls_planned": sum(2 * len(s["assignments"]) for s in strata.values()),
        "judge_calls_planned": sum(len(s["assignments"]) for s in strata.values()),
        "max_concurrent_provider_strata": 2,
        "automatic_retries": 0,
        "failure_policy": "Record any failure and stop short of calling it complete. A changed recovery policy requires a separate dated addendum; never retry for a negative preference or a factual/style/length defect.",
        "judge": "Unchanged native CLI adapter/settings and rubric; fresh context per pair; labels hidden. Freeze all author outputs before judging; lock judgments before decoding labels.",
        "randomization": "Python Random; independent order-v1 and labels-v1 streams per provider; balanced first arm within each selected stratum.",
        "runner_sha256": h.sha(Path(__file__).read_bytes()),
        "original_sha256": original_hashes(h, source), "strata": strata}
    h.save(output / "plan.json", plan)
    h.save(output / "commitment.json", {"plan_sha256": h.sha(h.encode(plan))})
    return plan


def author_call(h, live, provider, settings, messages, folder):
    body = {"model": settings["model"], "messages": messages, "stream": False,
            "max_tokens": settings["max_completion_tokens"], **EXTRAS[provider]}
    h.save(folder / "request.json", body)
    key = os.environ[settings["api_key_env"]]
    started = time.monotonic()
    record = {"status": "failed", "model_requested": settings["model"], "transport": "chat_completions"}
    try:
        request = urllib.request.Request(h.endpoint(settings["base_url"]), data=h.encode(body),
                                         headers={"Content-Type": "application/json", "Authorization": "Bearer " + key}, method="POST")
        with urllib.request.build_opener(h.NoRedirect).open(request, timeout=settings["timeout_seconds"]) as response:
            raw = response.read(16 * 1024 * 1024 + 1)
        h.require(len(raw) <= 16 * 1024 * 1024, "Response size exceeded")
        (folder / "response.json").write_bytes(live.scrub(raw.decode("utf-8")).encode("utf-8"))
        data = json.loads(raw)
        usage = data.get("usage", {})
        record.update(model_returned=data.get("model"), request_id=data.get("id"), usage=usage,
                      elapsed_seconds=round(time.monotonic() - started, 3))
        h.require(data.get("model") == settings["model"], "Returned model differs")
        for key_name, ceiling in (("completion_tokens", "max_completion_tokens"), ("total_tokens", "max_total_tokens")):
            h.require(h.positive_int(usage.get(key_name)) and usage[key_name] <= settings[ceiling], "Missing usage or token ceiling exceeded")
        h.require(record["elapsed_seconds"] <= settings["timeout_seconds"], "Wall-time ceiling exceeded")
        h.require(data["choices"][0]["finish_reason"] == "stop", "Truncated response")
        content = data["choices"][0]["message"]["content"]
        parsed = parse_markdown(content)
        h.save(folder / "parsed.json", parsed)
        (folder / "report.md").write_bytes(parsed["report"].encode("utf-8"))
        (folder / "notes.md").write_bytes(parsed["notes"].encode("utf-8"))
        record["status"] = "response_complete"
    except urllib.error.HTTPError as exc:
        record["error"] = f"HTTP {exc.code}"
        (folder / "error-response.txt").write_text(live.scrub(exc.read(1024 * 1024).decode("utf-8", "replace")), encoding="utf-8")
    except Exception as exc:
        record["error"] = live.scrub(str(exc))
    record.setdefault("elapsed_seconds", round(time.monotonic() - started, 3))
    h.save(folder / "execution.json", record)
    print(json.dumps({"phase": "completion_author", "provider": provider, "pair": folder.parent.name, "arm": folder.name,
                      "status": record["status"], "seconds": record["elapsed_seconds"], "error": record.get("error")}), flush=True)


def generate_stratum(h, live, source, output, provider, stratum):
    frozen = h.read(source / "runs" / provider / "coordinator/frozen.json")
    for task in stratum["assignments"]:
        for arm in task["run_order"]:
            author_call(h, live, provider, stratum["settings"], author_messages(h, frozen, task, arm),
                        output / provider / "authors" / task["pair_id"] / arm)


def execute(h, live, source, output, plan):
    h.require(h.sha(h.encode(plan)) == h.read(output / "commitment.json")["plan_sha256"], "Plan changed")
    h.require(h.sha(Path(__file__).read_bytes()) == plan["runner_sha256"], "Runner changed after commitment")
    h.require(original_hashes(h, source) == plan["original_sha256"], "Original evidence changed")
    h.save(output / "run-started.json", {"started_at": datetime.now(timezone.utc).isoformat(), "plan_sha256": h.sha(h.encode(plan))})
    # LongCat starts immediately; the other worker processes DeepSeek, then GLM.
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(generate_stratum, h, live, source, output, p, plan["strata"][p]) for p in ("longcat", "deepseek", "glm")]
        for future in futures:
            future.result()
    author_files = {p.relative_to(output).as_posix(): h.sha(p.read_bytes()) for p in sorted(output.rglob("*")) if p.is_file() and "authors" in p.parts}
    h.save(output / "authors.lock.json", {"sha256": author_files})
    # Reuse the identical judge adapter, including its configured isolation and schema.
    live.W = source
    judgments = []
    for provider, stratum in plan["strata"].items():
        frozen = h.read(source / "runs" / provider / "coordinator/frozen.json")
        for task in stratum["assignments"]:
            pair = task["pair_id"]
            row = {"provider": provider, "pair_id": pair, "task_id": task["task_id"], "family_id": task["family_id"], "status": "unresolved_author_failure"}
            folders = {arm: output / provider / "authors" / pair / arm for arm in ("with_toolkit", "without_toolkit")}
            if all(h.read(p / "execution.json")["status"] == "response_complete" for p in folders.values()):
                packet = {"brief": task["brief"], "sources": task["sources"], "rubric": frozen["rubric"],
                          "reports": {label: h.read(folders[arm] / "parsed.json")["report"] for label, arm in task["labels"].items()}}
                h.save(output / provider / "judge-inputs" / f"{pair}.json", packet)
                folder = output / provider / "judgments" / pair
                content = live.judge_call(frozen["config"]["judge"], [{"role": "system", "content": h.JUDGE_SYSTEM},
                                          {"role": "user", "content": json.dumps(packet, ensure_ascii=False)}], folder)
                row["status"] = "unresolved_judge_failure"
                if content is not None:
                    parsed = h.validate_judgment(json.loads(content))
                    h.save(folder / "parsed.json", parsed)
                    row.update(status="judged", preference=parsed["preference"])
            judgments.append(row)
    h.save(output / "judgments.lock.json", {"sha256": {p.relative_to(output).as_posix(): h.sha(p.read_bytes()) for p in sorted(output.rglob("*")) if p.is_file() and "judgments" in p.parts}})
    for row in judgments:
        task = next(t for t in plan["strata"][row["provider"]]["assignments"] if t["pair_id"] == row["pair_id"])
        row["outcome"] = task["labels"].get(row.get("preference"), row.get("preference", "unresolved"))
    h.save(output / "results.json", {"analysis_type": "post_hoc_completion_supplement", "results": judgments, "general_quality_advantage_established": False})
    h.save(output / "bundle-manifest.json", {"sha256": {p.relative_to(output).as_posix(): h.sha(p.read_bytes()) for p in sorted(output.rglob("*")) if p.is_file()}})
    print(json.dumps({"completed_pairs": sum(r["status"] == "judged" for r in judgments), "planned_pairs": len(judgments)}), flush=True)
    return int(any(r["status"] != "judged" for r in judgments))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=HERE)
    parser.add_argument("--output", type=Path, required=True, help="New directory inside the source study; never an existing run")
    parser.add_argument("--seed", type=int, default=2026101002)
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    source, output = args.source.resolve(), args.output.resolve()
    if not output.is_relative_to(source) or output == source:
        parser.error("Output must be a new child of --source so original provenance remains portable")
    h, live = load_source(source)
    plan = prepare(h, source, output, args.seed)
    print(json.dumps({"plan_sha256": h.sha(h.encode(plan)), "author_calls_planned": plan["author_calls_planned"], "judge_calls_planned": plan["judge_calls_planned"], "prepare_only": args.prepare_only}), flush=True)
    if args.prepare_only:
        return 0
    return execute(h, live, source, output, plan)


if __name__ == "__main__":
    raise SystemExit(main())
