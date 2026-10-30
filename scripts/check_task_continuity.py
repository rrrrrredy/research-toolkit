"""Independent minimal workflow fixtures; no private task data or model-quality claims."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import research_workflow as w
from check_research_workflow import BRIEF, SyntheticRunner, historical_profile, legacy_finish
from profile_policy import CHECKLIST
from run_observation import activity_summary, timed_capture


class ContinuityTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(dir=os.environ.get("IRF_TEST_TMPDIR"))
        self.addCleanup(tmp.cleanup)
        self.workspace = Path(tmp.name)
        w.start(self.workspace, "case", BRIEF, profile="lite")
        self.root = self.workspace / "case"
        w.save_text(self.root, "source.md", "The depot sent twelve shipments. Revenue was not reported.")
        self.assertTrue(w.save_records(self.workspace, "case",
            sources=[{"title": "Depot records", "url": "https://example.org/depot", "source_type": "primary",
                      "read_scope": "full_text", "read_evidence": "source.md"}],
            claims=[{"claim": "Twelve shipments", "claim_type": "verified_fact", "supporting_sources": ["S1"]}],
            requirements=[{"summary": "Explain the revenue limitation", "status": "pending"}],
            draft={"path": "report-a.md", "content": "Twelve shipments. Revenue is unknown.", "main": True})["ok"])

    def snapshot(self):
        return {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}

    def finish_lite(self):
        # Build a retained pre-v2 receipt; current delivery never follows this path.
        w.save_records(self.workspace, "case", requirements=[{"requirement_id": "R1", "status": "satisfied", "evidence": "report-a.md paragraph 1"}])
        historical_profile(self.workspace, 'case', 'lite')
        checklist = {k: {"passed": True, "evidence": "report-a.md paragraph 1 and source.md"} for k in CHECKLIST}
        result = legacy_finish(self.workspace, "case", "Complete.", artifact="report-a.md", checklist=checklist)
        self.assertTrue(result["completed"], result)

    def test_new_main_does_not_inherit_delivery_or_rewrite_receipt(self):
        self.finish_lite()
        receipt = (self.root / "state/final_checklist.json").read_bytes()
        saved = w.save_records(self.workspace, "case", draft={"path": "report-b.md", "content": "A revised interpretation.", "main": True})
        self.assertTrue(saved["ok"], saved)
        before = self.snapshot()
        status = w.status(self.workspace, "case")
        self.assertEqual(status["progress"]["stage"], "revise")
        self.assertEqual(status["progress"]["status"], "in_progress")
        self.assertEqual(status["current_work"]["artifact"]["path"], "report-b.md")
        self.assertEqual(status["current_work"]["last_delivery"]["artifact"], "report-a.md")
        self.assertEqual((self.root / "state/final_checklist.json").read_bytes(), receipt)
        self.assertEqual(self.snapshot(), before)
        with self.assertRaisesRegex(ValueError, "registered main"):
            w.finish(self.workspace, "case", "Old report complete.", artifact="report-a.md")

    def test_partial_and_reference_saves_keep_main_and_locations(self):
        w.save_records(self.workspace, "case", draft={"path": "notes.md", "content": "Twelve shipments", "complete": True})
        result = w.save_records(self.workspace, "case", claims=[{"claim_id": "C1", "uncertainty": "No revenue measure"}])
        self.assertEqual(result["current_work"]["artifact"]["path"], "report-a.md")
        self.assertEqual(result["changes"]["artifact"], "report-a.md")

    def test_main_resume_activates_current_contract_then_retry_is_idempotent(self):
        self.finish_lite()
        receipt = (self.root / 'state/final_checklist.json').read_bytes()
        saved = w.save_records(self.workspace, "case", draft={"path": "report-a.md", "main": True})
        self.assertTrue(saved["ok"])
        current = w.status(self.workspace, 'case')['progress']
        self.assertEqual(current['review_contract'], 2)
        self.assertEqual(current['status'], 'in_progress')
        progress = (self.root / "state/progress.json").read_bytes()
        self.assertTrue(w.save_records(self.workspace, 'case', draft={'path': 'report-a.md', 'main': True})['ok'])
        self.assertEqual((self.root / "state/progress.json").read_bytes(), progress)
        self.assertEqual((self.root / 'state/final_checklist.json').read_bytes(), receipt)
        self.assertFalse(w.finish(self.workspace, 'case', 'Complete.', artifact='report-a.md')['completed'])
        (self.root / "report-a.md").write_text("External edit", encoding="utf-8")
        status = w.status(self.workspace, "case")
        self.assertTrue(status["current_work"]["artifact"]["changed_since_save"])
        self.assertEqual(status["progress"]["status"], "in_progress")
        w.save_records(self.workspace, "case", draft={"path": "report-a.md"})
        self.assertEqual(w.status(self.workspace, "case")["progress"]["stage"], "revise")

    def test_brief_update_preserves_other_fields_and_open_requirements(self):
        result = w.save_records(self.workspace, "case", brief={"output": "A comparison memo"},
            requirements=[{"requirement_id": "R2", "summary": "Compare depot delays", "status": "pending"}],
            draft={"path": "comparison.md", "content": "Comparison still in progress.", "main": True, "kind": "comparison"})
        self.assertTrue(result["ok"], result)
        status = w.status(self.workspace, "case")
        self.assertEqual(status["progress"]["brief"]["scope"], BRIEF["scope"])
        self.assertEqual(status["progress"]["brief"]["output"], "A comparison memo")
        self.assertIn("A comparison memo", (self.root / "state/task_spec.md").read_text(encoding="utf-8"))
        self.assertEqual([r["requirement_id"] for r in status["current_work"]["open_requirements"]], ["R1", "R2"])
        self.assertEqual(status["current_work"]["artifact"]["kind"], "comparison")
        self.assertEqual(status["runtime"]["host_loaded_entry"], "not_observed")
        self.assertEqual(status["runtime"]["version"], (w.TOOLKIT / "VERSION").read_text().strip())

    def test_brief_update_preserves_custom_spec_and_rejects_conflicting_field(self):
        path = self.root / "state/task_spec.md"
        path.write_text(path.read_text(encoding="utf-8") + "\n## Reader constraints\n\nKeep the accessibility analysis.\n", encoding="utf-8")
        result = w.save_records(self.workspace, "case", brief={"output": "A short memo"})
        self.assertTrue(result["ok"], result)
        self.assertIn("Keep the accessibility analysis.", path.read_text(encoding="utf-8"))
        path.write_text(path.read_text(encoding="utf-8").replace("A short memo", "A manually changed format"), encoding="utf-8")
        before = self.snapshot()
        result = w.save_records(self.workspace, "case", brief={"output": "A review"}, draft={"path": "no.md", "content": "No", "main": True})
        self.assertFalse(result["ok"])
        self.assertIn("brief.output", result["errors"][0])
        self.assertEqual(path.read_bytes(), before[Path("state/task_spec.md")])
        self.assertEqual((self.root / "state/progress.json").read_bytes(), before[Path("state/progress.json")])
        self.assertFalse((self.root / "no.md").exists())

    def test_bad_reading_requirement_is_atomic_and_partial_pair_updates_work(self):
        original = self.snapshot()
        result = w.save_records(self.workspace, "case", brief={"scope": "Changed scope"},
            draft={"path": "new.md", "content": "New", "main": True},
            requirements=[{"summary": "Read source", "reading_requirement": "full_substantive_text", "required_source_ids": ["S1"]}])
        self.assertFalse(result["ok"])
        self.assertIn("reading_requirement", result["errors"][0])
        for name, content in original.items():
            if name.as_posix() != "logs/activity.jsonl":
                self.assertEqual((self.root / name).read_bytes(), content)
        self.assertFalse((self.root / "new.md").exists())
        valid = {"summary": "Read source", "reading_requirement": "full_text", "required_source_ids": ["S1"]}
        self.assertTrue(w.save_records(self.workspace, "case", requirements=[valid])["ok"])
        self.assertTrue(w.save_records(self.workspace, "case", requirements=[{"requirement_id": "R2", "reading_requirement": "relevant_sections"}])["ok"])
        for patch_value in ({"reading_requirement": "full_text"}, {"required_source_ids": ["S1"]},
                            {"reading_requirement": "full_text", "required_source_ids": ["S1", "S1"]}):
            self.assertFalse(w.save_records(self.workspace, "case", requirements=[{"summary": "Other", **patch_value}])["ok"])

    def test_failed_write_rolls_back_brief_main_and_draft(self):
        import research_records
        before = self.snapshot()
        original = research_records.os.replace
        count = 0
        def fail(src, dst):
            nonlocal count
            count += 1
            if count == 3:
                raise OSError("controlled failure")
            return original(src, dst)
        with patch.object(research_records.os, "replace", side_effect=fail):
            result = w.save_records(self.workspace, "case", brief={"output": "Review note"},
                draft={"path": "review.md", "content": "Unfinished review", "main": True, "kind": "review"})
        self.assertFalse(result["ok"])
        for name, content in before.items():
            if name.as_posix() != "logs/activity.jsonl":
                self.assertEqual((self.root / name).read_bytes(), content)
        self.assertFalse((self.root / "review.md").exists())

    def test_explicit_scope_decision_can_retire_legacy_reading_row(self):
        legacy = {"requirement_id": "R1", "summary": "Read retired source", "status": "pending",
                  "reading_requirement": "full_substantive_text", "required_source_ids": ["S1"]}
        w.save_text(self.root, "state/requirements.jsonl", json.dumps(legacy) + "\n")
        result = w.save_records(self.workspace, "case", requirements=[{"requirement_id": "R1", "status": "waived",
            "user_decision": {"source_turn": "user-2", "quote": "Remove this source from the task."}}])
        self.assertTrue(result["ok"], result)
        self.assertEqual(json.loads((self.root / "state/requirements.jsonl").read_text())["reading_requirement"], legacy["reading_requirement"])
        self.assertTrue(w.save_records(self.workspace, "case", requirements=[{"requirement_id": "R1", "summary": "Retired reading obligation"}])["ok"])
        self.assertFalse(w.save_records(self.workspace, "case", requirements=[{"requirement_id": "R1", "status": "pending"}])["ok"])

    def test_resume_reports_malformed_requirement_without_crashing_or_writing(self):
        w.save_text(self.root, "state/requirements.jsonl", json.dumps({"requirement_id": "R1", "status": ["pending"]}) + "\n")
        before = self.snapshot()
        status = w.status(self.workspace, "case")
        self.assertTrue(status["current_work"]["warnings"])
        self.assertEqual(len(status["current_work"]["open_requirements"]), 1)
        self.assertEqual(self.snapshot(), before)
        saved = w.save_records(self.workspace, "case", draft={"path": "note.md", "content": "A separate note."})
        self.assertTrue(saved["ok"], saved)
        self.assertTrue(saved["current_work"]["warnings"])
        self.assertEqual((self.root / "note.md").read_text(encoding="utf-8"), "A separate note.")

    def test_legacy_task_does_not_auto_adopt_latest_file(self):
        w.start(self.workspace, "legacy", BRIEF, profile="lite")
        w.save_records(self.workspace, "legacy", draft={"path": "chapter.md", "content": "Chapter", "complete": True})
        self.assertIsNone(w.status(self.workspace, "legacy")["current_work"]["artifact"])

    def test_cli_roundtrip_uses_existing_save_not_a_new_command(self):
        request = {"task": "case", "brief": {"depth": "Explain delays"},
                   "draft": {"path": "review.md", "content": "The report needs a source.", "main": True, "kind": "review"}}
        result = subprocess.run([sys.executable, "-X", "utf8", str(w.TOOLKIT / "scripts/research_workflow.py"),
            "save", "--workspace", str(self.workspace)], input=json.dumps(request), text=True, encoding="utf-8", capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(json.loads(result.stdout)["current_work"]["artifact"]["kind"], "review")

    def test_full_revision_still_requires_current_complete_review(self):
        w.start(self.workspace, "full", BRIEF)
        root = self.workspace / "full"
        w.save_text(root, "source.md", "Twelve shipments; revenue unknown.")
        w.save_records(self.workspace, "full", sources=[{"title": "Records", "url": "https://example.org",
            "source_type": "primary", "read_scope": "full_text", "read_evidence": "source.md"}],
            claims=[{"claim": "Twelve shipments", "claim_type": "verified_fact", "supporting_sources": ["S1"]}],
            draft={"path": "a.md", "content": "Twelve shipments. Revenue unknown.", "main": True})
        config = {"reviewers": [{"id": "one", "model": "synthetic", "format": "json"}]}
        runner = SyntheticRunner()
        self.assertTrue(w.review(self.workspace, "full", ["source.md"], artifact="a.md", config=config, runner=runner)["reviews_complete"])
        self.assertTrue(w.finish(self.workspace, "full", "Complete", artifact="a.md")["completed"])
        receipt = (root / "state/final_delivery.json").read_bytes()
        w.save_records(self.workspace, "full", draft={"path": "b.md", "content": "Twelve shipments. Revenue remains unknown.", "main": True})
        self.assertFalse(w.finish(self.workspace, "full", "Complete", artifact="b.md")["completed"])
        self.assertEqual((root / "state/final_delivery.json").read_bytes(), receipt)
        with self.assertRaisesRegex(ValueError, "registered main"):
            w.review(self.workspace, "full", ["source.md"], artifact="a.md", config=config, runner=runner)
        reviewed = w.review(self.workspace, "full", ["source.md"], artifact="b.md", revision=True, config=config, runner=runner)
        self.assertTrue(reviewed["reviews_complete"], reviewed)
        self.assertTrue(w.finish(self.workspace, "full", "Revised report complete", artifact="b.md")["completed"])
        self.assertEqual(len(runner.calls), 20)  # Two distinct versions, each seven perspectives + domain + audit + acceptance.

    def test_imports_are_not_model_invocations_or_self_submissions(self):
        import time
        new = timed_capture({"import_only": True, "backend": "custom"}, "now", time.monotonic())
        self.assertNotIn("elapsed_seconds", new)
        captures = [new, {"import_only": True, "elapsed_seconds": 0.02, "external_execution": False},
                    {"external_execution": False}, {"backend": "generic", "elapsed_seconds": 2,
                     "response": json.dumps({"usage": {"prompt_tokens": 7, "completion_tokens": 3}})}]
        for i, capture in enumerate(captures):
            w.save(self.root, f"reviews/test/{i}/execution.json", capture)
        for i in range(2):
            w.append_row(self.root, {"record_type": "model_review", "attempt_id": str(i), "slot_id": "same",
                "artifact_sha256": "same", "input": {}, "status": "failed",
                "execution": {"path": f"reviews/test/{i}/execution.json"}})
        for root in (self.root, self.root / ".." / self.root.name):
            with self.subTest(root=str(root)):
                summary = activity_summary(root)
                self.assertEqual(len(summary["imported_reviews"]), 2, summary)
                self.assertEqual(summary["self_review_submissions"], 1)
                self.assertEqual(len(summary["review_invocations"]), 1)
                self.assertEqual(summary["review_retries"], 0)
                self.assertEqual(summary["failed_review_attempts"], 0)
                self.assertEqual(summary["observed_review_usage"], {"input_tokens": 7, "output_tokens": 3})
                self.assertTrue(all(x["review_elapsed_seconds"] is None for x in summary["imported_reviews"]))

    def test_diagnostic_catalog_is_structural_not_a_quality_test(self):
        from check_semantic_diagnostics import validate_catalog
        name = "task-continuity-cases.json"
        catalog = json.loads((w.TOOLKIT / "evals/semantic_diagnostics" / name).read_text(encoding="utf-8"))
        self.assertEqual(len(validate_catalog([(name, catalog)])), 12)


if __name__ == "__main__":
    unittest.main()
