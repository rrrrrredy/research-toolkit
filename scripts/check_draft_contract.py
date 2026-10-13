#!/usr/bin/env python3
"""Offline draft-check controls: counts and records are not semantic approval."""
import json
from pathlib import Path
import subprocess
import sys
import unittest

import check_research_workflow as fixtures
import research_workflow as w
from profile_policy import CHECKLIST


class DraftChecks(unittest.TestCase):
    def setUp(self):
        fixtures.WorkflowTests.setUp(self)

    def snapshot(self):
        return {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}

    def bound(self, **rule):
        w.save_text(self.root, "state/requirements.jsonl", json.dumps({
            "requirement_id": "L1", "summary": "Agreed whole-file range for the synthetic control.",
            "status": "satisfied", "evidence": "final.md",
            "length_constraint": {"unit": "whitespace_words", "scope": "whole_artifact", **rule}}) + "\n")

    def test_no_declared_bound_warns_without_inferring_limit_from_brief(self):
        w.save_text(self.root, "final.md", "Source says revenue is twelve.")
        before = self.snapshot()
        result = w.check_draft(self.workspace, "case")
        self.assertTrue(result["ok"])
        self.assertEqual(result["length_checks"], [])
        self.assertEqual(result["counts"]["whitespace_words"], 5)
        self.assertIn("No explicit length", result["warnings"][0])
        self.assertEqual(result["semantic_quality"], "not_assessed")
        self.assertEqual(result["delivery_status"], "not_assessed")
        self.assertEqual(self.snapshot(), before)

    def test_failed_then_revised_lite_report_rechecks_current_bytes_without_receipt(self):
        progress = w.load(self.root, "state/progress.json")
        w.save(self.root, "state/progress.json", {**progress, "profile": "lite"})
        self.bound(min=5, max=7)
        w.save_text(self.root, "final.md", "Too short.")
        before = self.snapshot()
        first = w.check_draft(self.workspace, "case")
        self.assertFalse(first["ok"])
        self.assertEqual(first["length_checks"][0]["actual"], 2)
        self.assertEqual(self.snapshot(), before)
        w.save_text(self.root, "final.md", "The source reports twelve shipments only.")
        revised = self.snapshot()
        second = w.check_draft(self.workspace, "case")
        self.assertTrue(second["ok"], second)
        self.assertNotEqual(first["artifact_sha256"], second["artifact_sha256"])
        self.assertEqual(self.snapshot(), revised)
        # A later edit cannot reuse the earlier check as delivery permission.
        w.save_text(self.root, "final.md", "Short again.")
        denied = w.finish(self.workspace, "case", "Synthetic delivery.", checklist={
            key: {"passed": True, "evidence": "Synthetic false assertion."} for key in CHECKLIST})
        self.assertFalse(denied["completed"])
        self.assertEqual(denied["length_checks"][0]["actual"], 2)
        self.assertFalse((self.root / "state/final_checklist.json").exists())

    def test_whole_artifact_unicode_and_markup_are_counted_on_custom_path(self):
        w.save_text(self.root, "memo.md", "# 标题\n水量 180 L。[S1]\n")
        self.bound(unit="nonwhitespace_characters", min=14, max=14)
        result = w.check_draft(self.workspace, "case", artifact="memo.md")
        self.assertEqual(result["counts"]["nonwhitespace_characters"], 14)
        self.assertTrue(result["length_checks"][0]["bounds_met"])
        self.assertTrue(result["ok"], result)

    def test_bad_records_report_and_requirement_all_remain_visible(self):
        w.save_text(self.root, "data/claims_registry.csv", "claim_id,claim,claim_type,supporting_sources\nC1,Claim,verified_fact,S9\n")
        w.save_text(self.root, "final.md", " \n")
        w.save_text(self.root, "state/requirements.jsonl", "{broken\n")
        before = self.snapshot()
        result = w.check_draft(self.workspace, "case")
        self.assertFalse(result["ok"])
        combined = " ".join(result["errors"])
        for clue in ("S9", "nonempty report", "not valid JSON"):
            self.assertIn(clue, combined)
        self.assertEqual(self.snapshot(), before)

    def test_pending_requirement_does_not_become_satisfied_by_counting(self):
        self.bound(min=1, max=100)
        row = json.loads((self.root / "state/requirements.jsonl").read_text())
        row["status"] = "pending"
        w.save_text(self.root, "state/requirements.jsonl", json.dumps(row) + "\n")
        before = self.snapshot()
        result = w.check_draft(self.workspace, "case")
        self.assertTrue(result["length_checks"][0]["bounds_met"])
        self.assertFalse(result["ok"])
        self.assertEqual(self.snapshot(), before)

    def test_missing_invalid_utf8_and_escaping_reports_fail_without_mutation(self):
        self.bound(max=100)
        (self.root / "bad.md").write_bytes(b"\xff")
        before = self.snapshot()
        for artifact in ("missing.md", "bad.md"):
            with self.subTest(artifact=artifact):
                result = w.check_draft(self.workspace, "case", artifact)
                self.assertFalse(result["ok"])
                self.assertEqual(result["counts"], {})
        with self.assertRaises(ValueError):
            w.check_draft(self.workspace, "case", "../outside.md")
        self.assertEqual(self.snapshot(), before)

    def test_cli_failure_then_success_exit_codes_without_stage_change(self):
        self.bound(max=1)
        command = [sys.executable, "-X", "utf8", str(Path(w.__file__)), "check-draft", "--workspace", str(self.workspace)]
        before = self.snapshot()
        result = subprocess.run(command, input='{"task":"case"}', capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertFalse(json.loads(result.stdout)["ok"])
        self.assertEqual(self.snapshot(), before)
        self.bound(max=100)
        result = subprocess.run(command, input='{"task":"case"}', capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["ok"])
        self.assertEqual(w.load(self.root, "state/progress.json")["stage"], "collect")


if __name__ == "__main__":
    unittest.main(verbosity=2)
