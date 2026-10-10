#!/usr/bin/env python3
"""Reproduce the public calibration inventory offline; never regenerate or score reports."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from check_diagnostic_bundle import DEFAULT, check_bundle, digest


def reproduce(output: Path) -> dict:
    findings = check_bundle(DEFAULT)
    if findings:
        raise ValueError("; ".join(findings))
    provenance = json.loads((DEFAULT / "calibration-provenance.json").read_text(encoding="utf-8"))
    pairs = {}
    for row in provenance["runs"]:
        actual = digest(DEFAULT / row["reader_export"])
        if actual != row["reader_export_sha256_lf"]:
            raise ValueError("Calibration export hash differs: " + row["reader_export"])
        pair = pairs.setdefault(row["task"], {})
        if row["condition"] in pair:
            raise ValueError("Duplicate calibration condition")
        pair[row["condition"]] = {"path": row["reader_export"], "sha256_lf": actual}
    if len(pairs) != 2 or any(set(p) != {"framework", "baseline"} for p in pairs.values()):
        raise ValueError("Expected the two retained with/without pairs")
    result = {"scope": "historical_development_inventory_not_efficacy", "pairs": pairs,
              "n": len(pairs), "condition_order": provenance["condition_order"],
              "human_reviews_completed": provenance["human_reviews_completed"],
              "blinded_efficacy_result": False, "matched_model_and_brief_established": False,
              "model_calls": 0, "research_quality_status": "not_evaluated"}
    output.mkdir(parents=True, exist_ok=False)
    (output / "inventory.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    lines = ["# Public calibration inventory", "", "Two retained development pairs; four original reports. No quality score.", "",
             "| Task | With toolkit | Without toolkit |", "| --- | --- | --- |"]
    for task, pair in pairs.items():
        links = [f"[Original](https://github.com/rrrrrredy/research-toolkit/blob/main/evals/diagnostics/2026-09-07/{pair[c]['path']})" for c in ("framework", "baseline")]
        lines.append(f"| {task} | {links[0]} | {links[1]} |")
    lines += ["", "n=2; unblinded efficacy evidence; toolkit-first in both tasks. Public records do not establish matched model and brief. General quality advantage remains unproven.", "", "This command verifies preserved hashes and reproduces the inventory. It does not recreate historical model outputs or reinterpret later repair reviews as blind comparisons."]
    (output / "inventory.md").write_text("\n".join(lines)+"\n", encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("evals/runs/calibration-reproduction"))
    args = parser.parse_args()
    try:
        result = reproduce(args.output)
        print(f"PASS: {result['n']} pairs / 4 original reports; inventory.json and inventory.md written to {args.output}; 0 model calls; no quality verdict")
        return 0
    except (OSError, ValueError, KeyError) as exc:
        print(f"FAIL: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
