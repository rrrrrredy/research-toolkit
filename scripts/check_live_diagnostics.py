#!/usr/bin/env python3
"""Read-only integrity and derived-result checks for the dated live diagnostics."""
import base64
import hashlib
import json
from pathlib import Path

import codex_judge
import run_blinded_evals as h

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local(root, name):
    target = (root / name).resolve()
    h.require(target.is_relative_to(root.resolve()) and target.is_file(), "Invalid diagnostic artifact path")
    return target


def verify_connectivity(root):
    summary = h.read(root / "summary.json")
    for entry in summary["files"]:
        h.require(digest(local(root, entry["file"])) == entry["public_sha256"], "Connectivity public artifact changed")
    successful, network, preflight = [], 0, 0
    for path in root.glob("connectivity-*/**/execution.json"):
        row = h.read(path)
        if row["status"] == "connected":
            successful.append(row)
        if path.parent.name == "astra":
            if row["status"] == "cli_completed":
                network += 1
                events = [json.loads(line) for line in (path.parent / "events.jsonl").read_text().splitlines()]
                messages = [e["item"]["text"] for e in events if e.get("item", {}).get("type") == "agent_message"]
                h.require(len(messages) == 1 and json.loads(messages[0]) == {"connection": "ok", "sum": 5}, "Native connectivity content mismatch")
            else:
                preflight += 1
        else:
            network += 1
    h.require(len(successful) == 4 and sum(row["usage"]["total_tokens"] for row in successful) == summary["api_total_tokens"], "API connectivity accounting mismatch")
    h.require(network == summary["network_generation_requests"] == 6 and preflight == summary["local_preflight_failures"] == 1, "Connectivity attempt accounting mismatch")


def verify_calibration(root):
    manifest = h.read(root / "public-manifest.json")
    for name, expected in manifest["sha256"].items():
        h.require(digest(local(root, name)) == expected, f"Public calibration artifact changed: {name}")
    frozen = h.read(root / "coordinator/frozen.json")
    h.require(h.sha(h.encode(frozen)) == h.read(root / "coordinator/commitment.json")["frozen_sha256"], "Calibration commitment mismatch")
    for name, expected in frozen["code_sha256"].items():
        raw = base64.b64decode(local(root, "code/" + name + ".b64").read_bytes().strip(), validate=True)
        h.require(h.sha(raw) == expected, "Archived execution code differs from frozen bytes")
    transformed = {row["original_path"]: row for row in manifest["transformations"]}
    for name, expected in h.read(root / "judgments.lock.json")["sha256"].items():
        actual = transformed[name]["original_sha256"] if name in transformed else digest(local(root, name))
        h.require(actual == expected, "Original judgment lock mismatch")
    results = h.read(root / "results.json")
    h.require(len(results["results"]) == len(frozen["cases"]) == frozen["max_requests"] == 12, "Calibration request count mismatch")
    by_family, usage, elapsed = {}, {}, 0
    for case, row in zip(frozen["cases"], results["results"]):
        folder = root / "judgments" / case["case_id"]
        content, tokens, _ = codex_judge.extract((folder / "events.jsonl").read_bytes(), frozen["settings"])
        parsed, _ = h.parse_output(content, frozen["settings"], "judge")
        h.require(parsed == h.read(folder / "parsed.json"), "Parsed judgment does not match native events")
        h.require(h.read(root / "judge-inputs" / (case["case_id"] + ".json")) == case["packet"], "Judge packet differs from freeze")
        request = h.read(folder / "request.json")
        h.require(request["messages"] == [{"role": "system", "content": frozen["system"]}, {"role": "user", "content": json.dumps(case["packet"], ensure_ascii=False)}], "Judge request includes changed or extra material")
        h.require(row["case_id"] == case["case_id"] and row["family_id"] == case["family_id"] and row["orientation"] == case["orientation"], "Result identity mismatch")
        h.require(row["preference"] == parsed["preference"] and row["expected_preference"] == case["expected_preference"] and
                  row["preference_matches"] == (parsed["preference"] == case["expected_preference"]), "Preference result mismatch")
        by_family.setdefault(case["family_id"], {})[case["orientation"]] = parsed
        for key, value in tokens.items():
            usage[key] = usage.get(key, 0) + value
        elapsed += h.read(folder / "execution.json")["elapsed_seconds"]
    drift = []
    for family, versions in by_family.items():
        for label, other in (("A", "B"), ("B", "A")):
            for dimension, item in versions["primary"]["reports"][label].items():
                swapped = versions["swapped"]["reports"][other][dimension]["score"]
                if item["score"] != swapped:
                    drift.append({"family_id": family, "primary_label": label, "dimension": dimension,
                                  "primary_score": item["score"], "swapped_score": swapped})
    adjudication = h.read(root / "adjudication.json")
    h.require(drift == adjudication["dimension_drift"] and usage == adjudication["usage"] and
              round(elapsed, 3) == adjudication["elapsed_seconds_sum"], "Derived calibration observations mismatch")
    h.require(sum(row["preference_matches"] for row in results["results"]) == adjudication["preference_matches"] and
              len(by_family) == adjudication["independent_families"] == 4, "Calibration summary mismatch")
    return {"packets": 12, "families": 4, "dimension_score_changes": len(drift), "semantic_verdict": "not_automatically_validated"}


if __name__ == "__main__":
    verify_connectivity(ROOT / "evals/diagnostics/2026-10-12-connectivity")
    print(json.dumps(verify_calibration(ROOT / "evals/diagnostics/2026-10-12-astra-calibration")))
