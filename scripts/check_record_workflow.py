"""Targeted record persistence and observation checks; no new model evaluation."""
import csv
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import research_workflow as w
from check_research_workflow import BRIEF, SyntheticRunner
from profile_policy import CHECKLIST
from review_runner import ReviewFailure
from run_observation import capture_usage


class RecordWorkflowTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(dir=os.environ.get("IRF_TEST_TMPDIR"))
        self.addCleanup(tmp.cleanup)
        self.workspace = Path(tmp.name)
        w.start(self.workspace, "case", BRIEF, profile="lite")
        self.root = self.workspace / "case"

    def seed(self):
        w.save_text(self.root, "source.md", "Twelve shipments; revenue unknown.")
        return w.save_records(self.workspace, "case",
            sources=[{"title": 'Source, "quoted"\n中文', "url": "https://example.org", "source_type": "primary",
                      "read_scope": "full_text", "read_evidence": "source.md"}],
            claims=[{"claim": "Twelve shipments", "claim_type": "verified_fact", "supporting_sources": ["S1"]}],
            requirements=[{"summary": "Explain shipments", "status": "pending"}],
            draft={"path": "drafts/first.md", "content": "Twelve shipments. Revenue is unknown.", "complete": True})

    def test_roundtrip_partial_updates_and_natural_key_retry(self):
        result = self.seed()
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["saved_ids"], {"sources": ["S1"], "claims": ["C1"], "requirements": ["R1"]})
        again = w.save_records(self.workspace, "case", sources=[{"url": "https://example.org", "title": "Updated title"}])
        self.assertEqual(again["saved_ids"]["sources"], ["S1"])
        with (self.root/"data/source_registry.csv").open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["read_evidence"], "source.md")
        self.assertEqual(w.load(self.root, "state/progress.json")["status"], "in_progress")
        reqs = (self.root/"state/requirements.jsonl").read_text(encoding="utf-8")
        self.assertEqual(json.loads(reqs)["status"], "pending")

    def test_bad_batch_preserves_records_and_reports_error_before_retry(self):
        self.seed()
        before = (self.root/"data/source_registry.csv").read_bytes()
        result = w.save_records(self.workspace, "case", sources=[{"source_id": "S1", "title": "New"}],
            requirements=[{"requirement_id": "R1", "length_constraint": {"min": "100"}}])
        self.assertFalse(result["ok"])
        self.assertIn("requirements[0].length_constraint", result["errors"][0])
        self.assertEqual((self.root/"data/source_registry.csv").read_bytes(), before)
        missing = w.save_records(self.workspace, "case", requirements=[{"requirement_id": "R1", "status": "satisfied"}])
        self.assertFalse(missing["ok"])
        self.assertIn(".evidence", missing["errors"][0])
        self.assertTrue(w.save_records(self.workspace, "case", requirements=[{"requirement_id": "R1", "status": "satisfied", "evidence": "drafts/first.md"}])["ok"])
        self.assertEqual(w.status(self.workspace, "case")["activity"]["failed_saves"], 2)

    def test_malformed_existing_records_can_be_replaced_with_original_backup(self):
        self.seed()
        path = self.root/"data/source_registry.csv"
        path.write_bytes(b'broken,"unterminated')
        rows = [{"source_id": "S1", "title": "Recovered", "url": "https://example.org", "source_type": "primary"}]
        self.assertFalse(w.save_records(self.workspace, "case", sources=rows)["ok"])
        result = w.save_records(self.workspace, "case", sources=rows, replace=["sources"])
        self.assertTrue(result["ok"], result)
        self.assertEqual((self.root/result["backups"][0]).read_bytes(), b'broken,"unterminated')

    def test_write_failure_rolls_back_and_draft_cannot_overwrite_state(self):
        self.seed()
        before = {name: (self.root/name).read_bytes() for name in ("data/source_registry.csv", "data/claims_registry.csv")}
        import research_records
        original = research_records.os.replace
        count = 0
        def fail_second(src, dst):
            nonlocal count
            count += 1
            if count == 2:
                raise OSError("controlled write failure")
            return original(src, dst)
        with patch.object(research_records.os, "replace", side_effect=fail_second):
            result = w.save_records(self.workspace, "case", sources=[{"source_id": "S1", "title": "New"}], claims=[{"claim_id": "C1", "claim": "Changed"}])
        self.assertFalse(result["ok"])
        self.assertEqual(before, {name: (self.root/name).read_bytes() for name in before})
        for path in ("../outside.md", "state/task_spec.md", "data/source_registry.csv"):
            self.assertFalse(w.save_records(self.workspace, "case", draft={"path": path, "content": "Overwrite"})["ok"])

    def test_first_complete_draft_is_retained_and_status_and_checks_stay_readonly(self):
        self.seed()
        first = w.status(self.workspace, "case")["activity"]["first_complete_draft"]
        self.assertGreaterEqual(w.status(self.workspace, "case")["activity"]["seconds_to_first_complete_draft_observation"], 0)
        self.assertEqual(first["time_basis"], "saved_by_tool")
        self.assertTrue(w.save_records(self.workspace, "case", draft={"path": "final.md", "content": "Updated report.", "complete": True})["ok"])
        self.assertEqual(w.status(self.workspace, "case")["activity"]["first_complete_draft"], first)
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        w.status(self.workspace, "case")
        w.check_draft(self.workspace, "case", "final.md")
        self.assertEqual(before, {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()})
        (self.root/"logs/activity.jsonl").write_bytes(b"\xff")
        self.assertTrue(w.status(self.workspace, "case")["activity"]["warnings"])

    def test_cli_save_and_changed_inputs_stale_the_existing_lite_checklist(self):
        self.seed()
        w.save_records(self.workspace, "case", requirements=[{"requirement_id": "R1", "status": "satisfied", "evidence": "drafts/first.md"}])
        items = {k: {"passed": True, "evidence": "drafts/first.md and source.md"} for k in CHECKLIST}
        self.assertTrue(w.finish(self.workspace, "case", "Complete.", artifact="drafts/first.md", checklist=items)["completed"])
        receipt = (self.root/"state/final_checklist.json").read_bytes()
        result = subprocess.run([sys.executable, "-X", "utf8", str(w.TOOLKIT/"scripts/research_workflow.py"),
            "save", "--workspace", str(self.workspace)], input=json.dumps({"task": "case", "claims": [{"claim_id": "C1", "uncertainty": "New qualification"}]}), text=True, encoding="utf-8", capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(w.status(self.workspace, "case")["progress"]["status"], "stale")
        self.assertEqual((self.root/"state/final_checklist.json").read_bytes(), receipt)

    def test_returned_usage_and_failed_review_retry_are_observed_not_invented(self):
        workspace = self.workspace
        w.start(workspace, "full", BRIEF)
        root = workspace/"full"
        w.save_text(root, "source.md", "Twelve shipments.")
        w.save_records(workspace, "full", sources=[{"title": "Source", "url": "https://example.org", "source_type": "primary", "read_scope": "full_text", "read_evidence": "source.md"}],
            claims=[{"claim": "Twelve shipments", "claim_type": "verified_fact", "supporting_sources": ["S1"]}], draft={"path": "final.md", "content": "Twelve shipments.", "complete": True})
        calls = []
        def runner(config, request, cwd):
            calls.append(1)
            capture = {"backend": "generic", "response": json.dumps({"usage": {"prompt_tokens": 100, "completion_tokens": 10, "prompt_tokens_details": {"cached_tokens": 60}}})}
            if len(calls) == 1:
                raise ReviewFailure("Controlled interrupted response", capture)
            return {**SyntheticRunner()({}, request, cwd), "capture": capture}
        config = {"reviewers": [{"id": "one", "model": "synthetic", "format": "json"}]}
        result = w.review(workspace, "full", ["source.md"], config=config, runner=runner)
        self.assertTrue(result["reviews_complete"], result)
        info = w.status(workspace, "full")["activity"]
        self.assertEqual(info["review_retries"], 1)
        self.assertEqual(info["failed_review_attempts"], 1)
        self.assertEqual(info["observed_review_usage"], {"input_tokens": 200, "output_tokens": 20, "cached_input_tokens": 120})
        self.assertIsNone(info["author_usage"])
        self.assertTrue(all(i["elapsed_seconds"] >= 0 for i in info["review_invocations"]))
        w.review(workspace, "full", ["source.md"], config=config, runner=runner)
        self.assertEqual(len(calls), 2)
        self.assertEqual(w.status(workspace, "full")["activity"], info)
        self.assertIsNone(capture_usage({"format": "json", "stdout": "{}"}))


if __name__ == "__main__":
    unittest.main()
