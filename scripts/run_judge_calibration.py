#!/usr/bin/env python3
"""Freeze and execute public calibration controls in fresh Codex judge contexts."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import random

import check_judge_calibration as controls
import codex_judge
import run_blinded_evals as h

CODE = ("run_judge_calibration.py", "codex_judge.py", "run_blinded_evals.py", "check_judge_calibration.py")


def hashes():
    return {name: h.sha(Path(__file__).with_name(name).read_bytes()) for name in CODE}


def prepare(settings_path, output, seed, pack=controls.DEFAULT_PACK):
    controls.verify_pack(pack)
    settings = h.read(settings_path)
    codex_judge.validate(settings)
    manifest = controls.read(pack / "coordinator-manifest.json")
    cases = []
    for family in manifest["families"]:
        for orientation, reference in family["packets"].items():
            cases.append({"family_id": family["family_id"], "orientation": orientation,
                          "expected_preference": reference["expected_preference"],
                          "packet": controls.read(controls.packet_path(pack.parent, reference["path"]))})
    random.Random(seed).shuffle(cases)
    for index, case in enumerate(cases, 1):
        case["case_id"] = f"case-{index:02d}"
    frozen = {"phase": "exposed_development_judge_calibration", "created_at": datetime.now(timezone.utc).isoformat(),
              "settings": settings, "seed": seed, "randomization": "Python Random shuffle; orientations remain within families",
              "system": h.JUDGE_SYSTEM, "cases": cases, "manifest": manifest, "code_sha256": hashes(),
              "max_requests": len(cases), "max_retries": 0, "independent_families": len(manifest["families"]),
              "acceptance": "All first outputs/failures retained. Preference matches are mechanical only; source-based adjudication must assess located errors and valid ties before admission to a quality pilot."}
    output.mkdir(parents=True, exist_ok=False)
    h.save(output / "coordinator/frozen.json", frozen)
    h.save(output / "coordinator/commitment.json", {"frozen_sha256": h.sha(h.encode(frozen))})
    return frozen


def execute(output, call=codex_judge.request):
    frozen = h.read(output / "coordinator/frozen.json")
    h.require(h.sha(h.encode(frozen)) == h.read(output / "coordinator/commitment.json")["frozen_sha256"], "Frozen calibration changed")
    h.require(frozen["code_sha256"] == hashes(), "Calibration code changed after freeze")
    # Exclusive creation also rejects concurrent starts and any silent retry of a partial run.
    h.save(output / "run-started.json", {"started_at": datetime.now(timezone.utc).isoformat()})
    judgments = []
    for index, case in enumerate(frozen["cases"], 1):
        h.require(index <= frozen["max_requests"], "Calibration request ceiling reached")
        folder = output / "judgments" / case["case_id"]
        h.save(output / "judge-inputs" / (case["case_id"] + ".json"), case["packet"])
        messages = [{"role": "system", "content": frozen["system"]},
                    {"role": "user", "content": json.dumps(case["packet"], ensure_ascii=False)}]
        raw = call(frozen["settings"], messages, folder)
        value = h.retain_parsed(raw, frozen["settings"], "judge", folder) if raw is not None else None
        judgments.append(value)
        print(f"Calibration {index}/{frozen['max_requests']}: first attempt retained", flush=True)
    h.save(output / "judgments.lock.json", {"status": "all_first_attempts_locked_including_failures",
           "sha256": {p.relative_to(output).as_posix(): h.sha(p.read_bytes()) for p in sorted((output / "judgments").rglob("*")) if p.is_file()}})
    outcomes = [{"case_id": case["case_id"], "family_id": case["family_id"], "orientation": case["orientation"],
                 "status": "parsed" if value is not None else "unresolved",
                 "preference": value["preference"] if value is not None else "unresolved",
                 "expected_preference": case["expected_preference"],
                 "preference_matches": value["preference"] == case["expected_preference"] if value is not None else None}
                for case, value in zip(frozen["cases"], judgments)]
    results = {"phase": frozen["phase"], "requests_attempted": len(outcomes), "independent_families": frozen["independent_families"],
               "results": outcomes, "source_adjudication": "pending", "judge_reliability_established": False,
               "toolkit_efficacy_established": False}
    h.save(output / "results.json", results)
    h.save(output / "bundle-manifest.json", {"sha256": {p.relative_to(output).as_posix(): h.sha(p.read_bytes())
           for p in sorted(output.rglob("*")) if p.is_file()}})
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "execute"))
    parser.add_argument("--settings", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()
    try:
        if args.action == "prepare":
            h.require(args.settings is not None and args.seed is not None, "Prepare needs --settings and --seed")
            prepare(args.settings, args.output, args.seed)
            print("Frozen calibration: no calls made.")
        else:
            result = execute(args.output)
            print("First attempts locked; source adjudication remains separate.")
            return int(any(row["status"] != "parsed" for row in result["results"]))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"FAIL: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
