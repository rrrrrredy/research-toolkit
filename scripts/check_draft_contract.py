#!/usr/bin/env python3
"""Offline draft-check controls: counts and records are not semantic approval."""
import json
import os
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

    def test_archived_repeated_paragraphs_warn_and_repairs_remain_clear(self):
        repo = Path(__file__).resolve().parents[1]
        originals = repo / "evals/studies/2026-10-19-external-batches/tasks"
        repairs = repo / "evals/repairs/2026-10-19-reader-edit/reports"
        progress = w.load(self.root, "state/progress.json")
        w.save(self.root, "state/progress.json", {**progress, "profile": "lite"})
        cases = (
            ("iIoT-predictive-maintenance-arr-zh-20261016", "局限", [39, 51]),
            ("guide-fund-hardtech-return-ratio-zh-20261016", "局限", [41, 53, 65]),
            ("scope3-factor-rfq-evidence-en-20261016", "Limitations", [37, 49, 61, 73, 85, 97]),
            ("regional-bank-llm-credit-memo-controls-en-20261016", "Limitations", [42, 54, 66, 78, 90, 102]),
        )
        for slug, heading, line_numbers in cases:
            with self.subTest(task=slug):
                original = (originals / slug / "final.md").read_text(encoding="utf-8")
                passage = original.splitlines()[line_numbers[0] - 1]
                for text, expect_warning in ((original, True),
                        ((repairs / (slug + ".md")).read_text(encoding="utf-8"), False)):
                    w.save_text(self.root, "final.md", text)
                    before = self.snapshot()
                    result = w.check_draft(self.workspace, "case")
                    warnings = [s for s in result["warnings"] if s.startswith("Repeated paragraph warning:")]
                    self.assertEqual(bool(warnings), expect_warning)
                    if expect_warning:
                        warning, = [s for s in warnings if s.endswith("\nOriginal paragraph:\n" + passage)]
                        self.assertIn(f"{len(line_numbers)} identical occurrences", warning)
                        for line in line_numbers:
                            self.assertIn(f"{heading} (lines {line}-{line})", warning)
                    self.assertTrue(result["ok"], result)
                    self.assertEqual(result["semantic_quality"], "not_assessed")
                    self.assertEqual(result["delivery_status"], "not_assessed")
                    self.assertEqual(before, self.snapshot())

    def test_exact_multiline_prose_keeps_locations_and_ignores_other_blocks(self):
        paragraph = "The source describes the procurement constraint.\nThe decision remains conditional on local demand."
        report = (f"# Findings\n\n{paragraph}\n\n## Discussion\n\n{paragraph}\n\n"
                  f"## Examples\n\n```text\n{paragraph}\n\n{paragraph}\n```\n\n"
                  + ("\n".join("    " + row for row in paragraph.splitlines()) + "\n\n") * 2
                  + ("\n".join("> " + row for row in paragraph.splitlines()) + "\n\n") * 2
                  + ("- " + paragraph.replace("\n", " ") + "\n\n") * 2
                  + ("| " + paragraph.replace("\n", " ") + " |\n\n") * 2
                  + paragraph.lower() + "\n\n" + paragraph + ".\n\nShort note.\n\nShort note.\n")
        w.save_text(self.root, "final.md", report)
        before = self.snapshot()
        result = w.check_draft(self.workspace, "case")
        warning, = [s for s in result["warnings"] if s.startswith("Repeated paragraph warning:")]
        self.assertIn("2 identical occurrences", warning)
        self.assertIn("Findings (lines 3-4); Discussion (lines 8-9)", warning)
        self.assertTrue(warning.endswith("\nOriginal paragraph:\n" + paragraph))
        self.assertTrue(result["ok"], result)
        self.assertEqual(before, self.snapshot())

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
        denied = fixtures.legacy_finish(self.workspace, "case", "Synthetic historical delivery.", checklist={
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
        command = [sys.executable, str(Path(w.__file__)), "check-draft", "--workspace", str(self.workspace)]
        for profile in ("lite", "full"):
            with self.subTest(profile=profile):
                progress = w.load(self.root, "state/progress.json")
                w.save(self.root, "state/progress.json", {**progress, "profile": profile})
                # The observed 3482-character report was in range but still pending.
                w.save_text(self.root, "memo.md", "研" * 3482)
                self.bound(unit="nonwhitespace_characters", min=2500, max=4000)
                row = w.load(self.root, "state/requirements.jsonl")
                row.update(status="pending", evidence="")
                w.save_text(self.root, "state/requirements.jsonl", json.dumps(row) + "\n")

                def check():
                    before = self.snapshot()
                    run = subprocess.run(command, input='{"task":"case","artifact":"memo.md"}',
                                         capture_output=True, text=True, encoding="utf-8")
                    self.assertEqual(self.snapshot(), before)
                    return run.returncode, json.loads(run.stdout)

                code, result = check()
                self.assertEqual(code, 1)
                self.assertFalse(result["ok"])
                self.assertTrue(result["length_checks"][0]["bounds_met"])
                self.assertEqual(result["length_checks"][0]["status"], "pending")
                for clue in ("L1 (3482 nonwhitespace_characters)", "still pending", "state/requirements.jsonl",
                             "counting scope", "evidence citing memo.md", "other listed errors"):
                    self.assertIn(clue, result["next_action"])

                # Only an explicit, evidenced record update clears the pending check.
                row.update(status="satisfied", evidence="memo.md: 3482 nonwhitespace characters, whole artifact.")
                w.save_text(self.root, "state/requirements.jsonl", json.dumps(row) + "\n")
                code, result = check()
                self.assertEqual(code, 0, result)
                self.assertTrue(result["ok"])
                self.assertNotIn("still pending", result["next_action"])

                # The hint must not tell an out-of-range pending draft to mark itself satisfied.
                row.update(status="pending", evidence="")
                w.save_text(self.root, "state/requirements.jsonl", json.dumps(row) + "\n")
                w.save_text(self.root, "memo.md", "Too short.")
                code, result = check()
                self.assertEqual(code, 1)
                self.assertFalse(result["length_checks"][0]["bounds_met"])
                self.assertNotIn("update only those rows", result["next_action"])

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

    def test_cli_review_preserves_unicode_with_legacy_pipe_encoding(self):
        w.save_records(self.workspace, "case", draft={"path": "final.md", "main": True,
                       "host_task": "synthetic-unicode-author", "complete": True})
        marker = "\ue200filecite\ue202turn0file0\ue201"
        w.save_text(self.root, "source.md", "中文来源：twelve shipments. " + marker)
        request = {"task": "case", "evidence_paths": ["source.md"], "include_assignment": True}
        result = subprocess.run([sys.executable, str(Path(w.__file__)), "review", "--workspace", str(self.workspace)],
                                input=json.dumps(request, ensure_ascii=False).encode("utf-8"), capture_output=True,
                                env={**os.environ, "PYTHONIOENCODING": "gbk", "PYTHONUTF8": "0"})
        self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8", errors="replace"))
        response = json.loads(result.stdout.decode("utf-8"))
        self.assertEqual(response["action_required"], "host_agents")
        self.assertEqual(len(response['assignments']), 8)
        self.assertIn("中文来源", result.stdout.decode("utf-8"))
        self.assertIn(marker, result.stdout.decode("utf-8"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
