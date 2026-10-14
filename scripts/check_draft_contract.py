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

    def test_private_citations_warn_in_both_profiles_without_mutation_or_new_gate(self):
        for profile in ("lite", "full"):
            progress = w.load(self.root, "state/progress.json")
            w.save(self.root, "state/progress.json", {**progress, "profile": profile})
            w.save_text(self.root, "final.md", "# Report\nA source claim.\ue200cite\ue202turn1search0\ue201\n"
                        "File evidence.\ue200filecite\ue202turn0file0\ue201\n"
                        "Files.\ue200filenavlist\ue2020:0\ue205Source description\ue201\n")
            before = self.snapshot()
            result = w.check_draft(self.workspace, "case")
            self.assertTrue(result["ok"], result)
            self.assertIn("3 private chat", " ".join(result["warnings"]))
            self.assertIn("line(s) 2, 3, 4", " ".join(result["warnings"]))
            self.assertEqual(before, self.snapshot())

    def test_export_citation_examples_and_ordinary_references_do_not_warn(self):
        token = "\ue200cite\ue202turn1search0\ue201"
        report = f"Example `{token}`.\n```markdown\n{token}\n```\n~~~\n{token}\n~~~\n[Actual source](https://example.org/paper). [1]\n"
        self.assertEqual(w.citation_export_warnings(report), [])
        self.assertEqual(w.citation_export_warnings(f"``multi\n{token}\nline``"), [])
        self.assertIn("line(s) 9", " ".join(w.citation_export_warnings(report + token)))

    def test_indented_code_examples_preserve_prose_warnings_and_line_numbers(self):
        for kind in ("cite", "filecite", "filenavlist"):
            token = f"\ue200{kind}\ue202turn0file0\ue201"
            with self.subTest(kind=kind):
                for indent in ("    ", "\t"):
                    report = f"Example:\n\n{indent}{token}\n\n{indent}{token}\n\nActual evidence {token}\n"
                    warning = " ".join(w.citation_export_warnings(report))
                    self.assertIn("1 private chat", warning)
                    self.assertIn("line(s) 7", warning)
                self.assertEqual(w.citation_export_warnings("    " + token + "\n"), [])
                # Indentation alone does not turn a paragraph continuation into code.
                self.assertIn("line(s) 2", " ".join(w.citation_export_warnings("A paragraph\n    " + token)))

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

    def test_length_input_errors_identify_the_field_and_correction_without_mutation(self):
        for rule, clues in (
                ({"minimum": 1, "maximum": 8}, ("minimum", "maximum", "use min/max")),
                ({"min": "1"}, ("min", "JSON integer")),
                ({"min": True}, ("min", "boolean")),
                ({"min": 4, "max": 2}, ("min (4)", "max (2)")),
                ({"unit": "tokens", "max": 8}, ("unit", "nonwhitespace_characters")),
                ({"scope": "body_only", "max": 8}, ("scope", "whole_artifact"))):
            with self.subTest(rule=rule):
                self.bound(**rule)
                before = self.snapshot()
                result = w.check_draft(self.workspace, "case")
                self.assertFalse(result["ok"])
                self.assertEqual(result["length_checks"], [])
                for clue in clues:
                    self.assertIn(clue, " ".join(result["errors"]))
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
