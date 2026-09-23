#!/usr/bin/env python3
"""Synthetic workflow controls; no model calls or report-quality evidence."""
from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
import uuid

import research_workflow as workflow
from review_runner import ReviewFailure, run_reviewer

BRIEF = {"question": "How many shipments are evidenced?", "audience": "Operations manager",
         "scope": "Company A, 2026", "output": "English report", "depth": "Three analytical paragraphs",
         "evidence_standard": "Read the complete supplied source; distinguish shipments from revenue."}
CONFIG = {"reviewers": [{"id": "primary", "model": "synthetic", "format": "json"}],
          "auditor": {"id": "audit", "model": "synthetic", "format": "json"}}


class SyntheticRunner:
    def __init__(self, *, negative=False, bad_review=0, bad_audit=0, reuse=False, inject=False):
        self.negative, self.bad_review, self.bad_audit = negative, bad_review, bad_audit
        self.calls = []
        self.reuse, self.inject = reuse, inject

    def __call__(self, config, request, cwd):
        role = request["role"]
        self.calls.append(role)
        if role == "reviewer":
            if self.bad_review:
                self.bad_review -= 1
                value = {"report_verdict": "pass", "coverage": {}, "findings": []}
            else:
                findings = ([{"finding_id": "F1", "severity": "major", "location": "paragraph 2",
                              "basis": "The source counts shipments, not revenue."}] if self.negative else [])
                value = {"report_verdict": "needs_revision" if findings else "pass", "findings": findings,
                         "coverage": {d: {"location": "paragraph 1", "basis": "Synthetic located comparison with source A."}
                                      for d in workflow.DIMENSIONS}}
                if self.inject:
                    value.update(status="failed", model="injected", input={"path": "../escape"},
                                 execution_id="injected", record_type="injected")
        else:
            if self.bad_audit:
                self.bad_audit -= 1
                raise ReviewFailure("Synthetic interrupted audit", {"synthetic": True, "status": "timeout"})
            value = {"result": "valid", "basis": "Synthetic independent coverage check.",
                     "dispositions": {f["finding_id"]: {"decision": "confirmed_defect",
                        "reason": "The quoted source supports shipments only.", "evidence": "source.md, paragraph 1"}
                        for f in request["finding_records"]},
                     "sample_checks": {s: {"result": "clear", "evidence": "Synthetic passage comparison."}
                                       for s in request["samples"]},
                     "global_review": {"result": "fail" if self.negative else "pass",
                                       "basis": "Synthetic whole-report examination.",
                                       "open_issues": ["Unsupported revenue statement."] if self.negative else []}}
        return {"execution_id": "synthetic-reused" if self.reuse else "synthetic-"+uuid.uuid4().hex,
                "content": json.dumps(value), "capture": {"synthetic": True, "role": role}}


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="research-workflow-test-")
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name)
        workflow.start(self.workspace, "case", BRIEF)
        self.root = self.workspace/"case"
        (self.root/"final.md").write_text("The source reports twelve shipments.\n\nRevenue is not reported.\n\nFurther evidence is needed for a revenue estimate.\n", encoding="utf-8")
        (self.root/"source.md").write_text("Company A reports twelve shipments in 2026. No revenue figure is supplied.\n", encoding="utf-8")
        (self.root/"data/source_registry.csv").write_text("source_id,title,url,source_type,read_scope,read_evidence\nS1,Shipment statement,https://example.org/source,primary,full_text,source.md\n", encoding="utf-8")
        (self.root/"data/claims_registry.csv").write_text("claim_id,claim,claim_type,supporting_sources\nC1,Twelve shipments,verified_fact,S1\n", encoding="utf-8")

    def review(self, runner, purpose="report_delivery", **kwargs):
        return workflow.review(self.workspace, "case", ["source.md"], purpose=purpose,
                               config=CONFIG, runner=runner, **kwargs)

    def test_clarification_precedes_collection_and_merges_answers(self):
        first = workflow.start(self.workspace, "brief-only", {"question": "What changed?"})
        self.assertFalse(first["ready_for_collection"])
        with self.assertRaises(ValueError):
            workflow.status(self.workspace, "brief-only", stage="collect")
        ready = workflow.start(self.workspace, "brief-only", BRIEF, language="zh")
        self.assertTrue(ready["ready_for_collection"])
        self.assertIn("研究工作流", ready["guidance"][0]["content"])

    def test_path_escape_is_rejected(self):
        for task in ("../outside", "/absolute", "x/y"):
            with self.assertRaises(ValueError):
                workflow.start(self.workspace, task, BRIEF)
        with self.assertRaises(ValueError):
            workflow.review(self.workspace, "case", ["../secret.txt"], config=CONFIG)

    def test_draft_requires_source_and_claim_records(self):
        (self.root/"data/claims_registry.csv").write_text("claim_id,claim\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            workflow.status(self.workspace, "case", stage="draft")

    def test_complete_review_and_delivery(self):
        runner = SyntheticRunner()
        result = self.review(runner)
        self.assertEqual(runner.calls, ["reviewer", "auditor"])
        self.assertTrue(result["completion_check"]["ok"], result)
        delivered = workflow.finish(self.workspace, "case", "The final report is complete.")
        self.assertTrue(delivered["completed"], delivered)
        self.assertEqual(workflow.load(self.root, "state/progress.json")["status"], "complete")
        self.assertTrue(workflow.evaluate_delivery(self.root)["ok"])

    def test_valid_negative_evaluation_is_retained_without_rerunning(self):
        runner = SyntheticRunner(negative=True)
        original = (self.root/"final.md").read_bytes()
        result = self.review(runner, purpose="evaluation")
        self.assertTrue(result["evaluation_complete"], result)
        again = self.review(runner, purpose="evaluation")
        self.assertTrue(again["evaluation_complete"], again)
        self.assertEqual(runner.calls, ["reviewer", "auditor"])
        self.assertEqual((self.root/"final.md").read_bytes(), original)

    def test_report_defect_prevents_final_delivery(self):
        result = self.review(SyntheticRunner(negative=True))
        self.assertTrue(result["reviews_complete"])
        self.assertFalse(result["completion_check"]["ok"])
        delivered = workflow.finish(self.workspace, "case", "The final report is complete.")
        self.assertFalse(delivered["completed"])
        self.assertFalse((self.root/"state/final_delivery.json").exists())

    def test_incomplete_response_recovers_and_preserves_failure(self):
        runner = SyntheticRunner(bad_review=1)
        result = self.review(runner)
        self.assertTrue(result["completion_check"]["ok"], result)
        attempts = [r for r in workflow.rows_for(self.root) if r.get("record_type") == "model_review"]
        self.assertEqual([r["status"] for r in attempts], ["incomplete", "completed"])
        self.assertEqual(runner.calls, ["reviewer", "reviewer", "auditor"])

    def test_interrupted_audit_does_not_repeat_completed_reviewer(self):
        runner = SyntheticRunner(bad_audit=1)
        self.assertFalse(self.review(runner)["reviews_complete"])
        result = self.review(runner)
        self.assertTrue(result["completion_check"]["ok"], result)
        self.assertEqual(runner.calls, ["reviewer", "auditor", "auditor"])

    def test_model_cannot_override_execution_bindings(self):
        result = self.review(SyntheticRunner(inject=True))
        self.assertTrue(result["completion_check"]["ok"], result)
        row = next(r for r in workflow.rows_for(self.root) if r.get("record_type") == "model_review")
        self.assertEqual(row["model"], "synthetic")
        self.assertNotEqual(row["execution_id"], "injected")

    def test_frozen_evaluation_cannot_be_replaced_by_changed_evidence(self):
        self.review(SyntheticRunner(), purpose="evaluation")
        (self.root/"source.md").write_text("Different source.", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.review(SyntheticRunner(), purpose="evaluation", revision=True)

    def test_frozen_input_tampering_is_rejected(self):
        self.review(SyntheticRunner())
        progress = workflow.load(self.root, "state/progress.json")
        path = self.root/progress["review_plan"]["slots"][0]["input"]["path"]
        path.write_text('{"tampered":true}', encoding="utf-8")
        with self.assertRaises(ValueError):
            self.review(SyntheticRunner())

    def test_changed_evidence_blocks_delivery(self):
        self.review(SyntheticRunner())
        (self.root/"source.md").write_text("Changed after review.", encoding="utf-8")
        self.assertFalse(workflow.finish(self.workspace, "case", "The final report is complete.")["completed"])

    def test_reused_execution_cannot_validate_its_own_review(self):
        result = self.review(SyntheticRunner(reuse=True))
        self.assertFalse(result["reviews_complete"])

    def test_open_requirement_keeps_persistent_state_nonterminal(self):
        self.review(SyntheticRunner())
        (self.root/"state/requirements.jsonl").write_text(json.dumps({
            "requirement_id": "R1", "source_turn": "1", "summary": "Provide calculations.",
            "status": "open", "evidence": []})+"\n", encoding="utf-8")
        result = workflow.finish(self.workspace, "case", "The final report is complete.")
        self.assertFalse(result["completed"], result)
        self.assertEqual(workflow.load(self.root, "state/progress.json")["status"], "in_progress")

    def test_dependency_failure_stays_open(self):
        def missing(*args):
            raise ReviewFailure("Synthetic missing dependency", {"synthetic": True, "status": "dependency_missing"})
        result = self.review(missing)
        self.assertFalse(result["reviews_complete"])
        self.assertIn("missing_valid_review", result["completion_check"]["flags"])

    def test_real_subprocess_transport_preserves_input_and_response(self):
        worker = self.workspace/"synthetic-worker.py"
        worker.write_text("import json,sys\nrequest=json.load(sys.stdin)\nprint(json.dumps({'execution_id':'synthetic-process-1','content':json.dumps(request,ensure_ascii=False)}))\n", encoding="utf-8")
        request = {"role": "transport-test", "source": "完整中文证据"}
        result = run_reviewer({"id": "test", "model": "synthetic", "format": "json",
                              "command": [sys.executable, "-X", "utf8", str(worker)]}, request, self.workspace)
        self.assertEqual(json.loads(result["content"]), request)
        self.assertEqual(result["capture"]["exit_code"], 0)


if __name__ == "__main__":
    if os.environ.get("IRF_TEST_TMPDIR"):
        tempfile.tempdir = os.environ["IRF_TEST_TMPDIR"]
    unittest.main()
