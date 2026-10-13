#!/usr/bin/env python3
"""Verify dated development evidence without model calls or evidence writes."""
import argparse
import base64
import json
from pathlib import Path
import shutil
import tempfile
import unittest

import run_blinded_evals as h
import summarize_development_pilot as s

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "evals/studies/2026-10-12-lite-four-models"
FORMAT = ROOT / "evals/diagnostics/2026-10-12-longcat-format"


def verify_format(root):
    public = h.read(root / "public-manifest.json")
    for name, digest in public["sha256"].items():
        h.require(h.sha(s.safe(root, name).read_bytes()) == digest, "Format public artifact changed")
    for name, digest in h.read(root / "manifest.json")["sha256"].items():
        h.require(h.sha(s.safe(root, name).read_bytes()) == digest, "Original format artifact changed")
    plan = h.read(root / "plan.json")
    h.require(h.sha(h.encode(plan)) == h.read(root / "commitment.json")["plan_sha256"], "Format commitment mismatch")
    for name in ("harness", "driver"):
        h.require(h.sha(base64.b64decode((root / (name + ".py.b64")).read_bytes().strip(), validate=True)) == plan[name + "_sha256"], "Format code archive mismatch")
    rows = []
    for item in plan["requests"]:
        folder = root / "attempts" / item["id"]
        settings = plan["settings"]
        expected = {"model": settings["model"], "messages": item["messages"], "stream": False,
                    settings["completion_parameter"]: settings["max_completion_tokens"], "thinking": {"type": settings["thinking"]}}
        h.require(h.read(folder / "request.json") == expected, "Format request differs from plan")
        raw = (folder / "content.txt").read_bytes().decode("utf-8")
        response, execution = h.read(folder / "response.json"), h.read(folder / "execution.json")
        h.require(response["choices"][0]["message"]["content"] == raw and response["usage"] == execution["usage"], "Format reply/usage mismatch")
        try:
            value, _ = h.parse_output(raw, settings, "author")
        except (ValueError, TypeError):
            h.require((folder / "invalid.json").is_file() and not (folder / "parsed.json").exists(), "Missing original format failure")
            status = "unresolved"
        else:
            h.require(value == h.read(folder / "parsed.json"), "Format parse mismatch")
            status = "parsed"
        rows.append({"id": item["id"], "status": status})
    results = h.read(root / "results.json")
    h.require(rows == results["results"] and len(rows) == results["requests_attempted"] == plan["max_requests"] == 4, "Format attempt accounting mismatch")
    h.require(sum(row["status"] == "parsed" for row in rows) == results["format_valid"] == 3, "Format failure disappeared")
    h.require(not results["original_development_results_replaced"], "Follow-up must not replace original outcomes")


def verify_study(root):
    derived = s.summarize(root)
    h.require(derived == h.read(root / "analysis.json"), "Published analysis differs from original evidence")
    adjudication = h.read(root / "source-adjudication.json")
    h.require(not adjudication["outcomes_rewritten"] and len(adjudication["pairs"]) == 20, "Adjudication coverage mismatch")
    for row, pair in zip(adjudication["pairs"], derived["pairs"]):
        h.require(all(row[key] == pair[key] for key in ("provider", "task_id", "pair_id")), "Adjudication identity mismatch")
        for condition, finding in row["findings"].items():
            h.require((finding["status"] == "source_checked") == (condition in pair["lengths"]), "Failed author output was quality-scored")
    return derived


def snapshot(root):
    return {p.relative_to(root).as_posix(): h.sha(p.read_bytes()) for p in root.rglob("*") if p.is_file()}


class EvidenceControls(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "study"
        shutil.copytree(STUDY, self.root)

    def change(self, name, edit):
        path = self.root / name
        value = h.read(path)
        edit(value)
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        # Reseal byte indexes so the test reaches semantic correspondence checks.
        for provider in ("deepseek", "kimi", "glm", "longcat"):
            manifest_path = self.root / provider / "bundle-manifest.json"
            manifest = h.read(manifest_path)
            prefix = provider + "/"
            if name.startswith(prefix) and name[len(prefix):] in manifest["sha256"]:
                manifest["sha256"][name[len(prefix):]] = h.sha(path.read_bytes())
                manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        public = self.root / "public-manifest.json"
        manifest = h.read(public)
        manifest["sha256"] = {p.relative_to(self.root).as_posix(): h.sha(p.read_bytes()) for p in self.root.rglob("*") if p.is_file() and p != public}
        public.write_text(json.dumps(manifest), encoding="utf-8")

    def test_read_only_and_missingness(self):
        before = snapshot(self.root)
        value = verify_study(self.root)
        self.assertEqual(snapshot(self.root), before)
        self.assertEqual(value["requests_attempted"], 72)
        self.assertEqual(value["by_provider"]["longcat"]["unresolved"], 4)
        self.assertEqual(len(value["dimension_drift"]), 21)

    def test_decoded_winner_cannot_be_rewritten(self):
        self.change("deepseek/results.json", lambda v: v["results"][0].update(outcome="with_toolkit"))
        with self.assertRaisesRegex(ValueError, "Decoded outcome"):
            verify_study(self.root)

    def test_missing_pair_cannot_be_assigned_a_winner(self):
        self.change("longcat/results.json", lambda v: v["results"][0].update(outcome="without_toolkit"))
        with self.assertRaisesRegex(ValueError, "Missing author pair"):
            verify_study(self.root)

    def test_judge_packet_must_be_verbatim_report(self):
        self.change("deepseek/judge-inputs/pair-01.json", lambda v: v["reports"].update(A=v["reports"]["A"] + " Edited."))
        with self.assertRaisesRegex(ValueError, "Judge reports"):
            verify_study(self.root)

    def test_resource_budget_cannot_drift(self):
        self.change("deepseek/coordinator/author/pair-01/with_toolkit/request.json", lambda v: v.update(max_tokens=4097))
        with self.assertRaisesRegex(ValueError, "Author request"):
            verify_study(self.root)

    def test_summary_cannot_hide_failure(self):
        self.change("analysis.json", lambda v: v["by_provider"]["longcat"].update(unresolved=0))
        with self.assertRaisesRegex(ValueError, "Published analysis"):
            verify_study(self.root)

    def test_new_json_format_probe_preserves_object_notes_failure(self):
        before = snapshot(FORMAT)
        verify_format(FORMAT)
        self.assertEqual(snapshot(FORMAT), before)
        raw = (FORMAT / "attempts/ceramics-handover-format-zh-with_toolkit/content.txt").read_text(encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "notes"):
            h.parse_output(raw, h.read(FORMAT / "plan.json")["settings"], "author")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    result = verify_study(STUDY)
    verify_format(FORMAT)
    print(json.dumps({"requests": result["requests_attempted"], "families": result["independent_families"], "source_judgments": "not_automatically_certified"}))
    if args.self_test:
        unittest.main(argv=[__file__])
