#!/usr/bin/env python3
"""Synthetic workflow controls; no model calls or report-quality evidence."""
from __future__ import annotations

import copy
import csv
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import uuid

import research_workflow as workflow
from review_runner import ReviewFailure, review_readiness, run_reviewer

BRIEF = {"question": "How many shipments are evidenced?", "audience": "Operations manager",
         "scope": "Company A, 2026", "output": "English report", "depth": "Three analytical paragraphs",
         "evidence_standard": "Read the complete supplied source; distinguish shipments from revenue."}
CONFIG = {"reviewers": [{"id": "primary", "model": "synthetic", "format": "json"}],
          "auditor": {"id": "audit", "model": "synthetic", "format": "json"}}


class SyntheticRunner:
    def __init__(self, *, negative=False, bad_review=0, bad_audit=0, reuse=False, inject=False):
        self.negative, self.bad_review, self.bad_audit = negative, bad_review, bad_audit
        self.calls = []
        self.requests = []
        self.reuse, self.inject = reuse, inject

    def __call__(self, config, request, cwd):
        role = request["role"]
        self.calls.append(role)
        self.requests.append(request)
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
        readiness = patch.object(workflow, "review_readiness", return_value={"status": "local_checks_passed", "model_access_verified": False})
        readiness.start()
        self.addCleanup(readiness.stop)
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
                               config=kwargs.pop("config", CONFIG), runner=runner, **kwargs)

    def test_clarification_precedes_collection_and_merges_answers(self):
        first = workflow.start(self.workspace, "brief-only", {"question": "What changed?"})
        self.assertFalse(first["ready_for_collection"])
        with self.assertRaises(ValueError):
            workflow.status(self.workspace, "brief-only", stage="collect")
        ready = workflow.start(self.workspace, "brief-only", BRIEF, language="zh")
        self.assertTrue(ready["ready_for_collection"])
        self.assertIn("研究工作流", ready["guidance"][0]["content"])

    def test_start_surfaces_blocked_review_access_before_collection(self):
        with patch.object(workflow, "review_readiness", return_value={"status": "blocked", "model_access_verified": False}):
            result = workflow.start(self.workspace, "no-access", BRIEF)
        self.assertFalse(result["ready_for_collection"])
        self.assertEqual(result["missing_fields"], [])
        self.assertEqual(result["review_readiness"]["status"], "blocked")

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

    def test_id_only_sources_cannot_advance_or_change_progress(self):
        before = workflow.load(self.root, "state/progress.json")
        (self.root/"data/source_registry.csv").write_text("source_id,title,url,source_type,read_scope,read_evidence\nS1,,,,,\n", encoding="utf-8")
        for stage in ("analyze", "draft"):
            with self.assertRaises(ValueError):
                workflow.status(self.workspace, "case", stage=stage)
        self.assertEqual(workflow.load(self.root, "state/progress.json"), before)

    def test_claim_content_reading_and_source_links_are_required(self):
        source = self.root/"data/source_registry.csv"
        source_text = source.read_text(encoding="utf-8")
        source.write_text(source_text.replace("full_text,source.md", "full_text,"), encoding="utf-8")
        with self.assertRaises(ValueError):
            workflow.status(self.workspace, "case", stage="analyze")
        source.write_text(source_text, encoding="utf-8")
        claims = self.root/"data/claims_registry.csv"
        for row in ("C1,,,", "C1,,verified_fact,S1", "C1,Twelve shipments,verified_fact,S99", "C1,Twelve shipments,verified_fact,"):
            claims.write_text("claim_id,claim,claim_type,supporting_sources\n"+row+"\n", encoding="utf-8")
            with self.subTest(row=row), self.assertRaises(ValueError):
                workflow.status(self.workspace, "case", stage="draft")

    def test_substantive_records_and_explicit_hypothesis_can_advance(self):
        claims = self.root/"data/claims_registry.csv"
        claims.write_text("claim_id,claim,claim_type,supporting_sources,uncertainty\nC1,Twelve shipments,verified_fact,S1,\nC2,Revenue might grow,hypothesis,,No revenue data supplied\n", encoding="utf-8")
        result = workflow.status(self.workspace, "case", stage="draft")
        self.assertEqual(result["progress"]["stage"], "draft")

    def test_model_change_uses_new_assignment_and_preserves_original(self):
        runner = SyntheticRunner(negative=True)
        self.review(runner)
        originals = [r for r in workflow.rows_for(self.root) if r.get("record_type") == "model_review"]
        original_bytes = (self.root/originals[0]["response"]["path"]).read_bytes()
        changed = copy.deepcopy(CONFIG)
        changed["reviewers"][0]["model"] = "synthetic-B"
        with self.assertRaises(ValueError):
            self.review(runner, config=changed)
        runner.negative = False
        result = self.review(runner, config=changed, revision=True)
        self.assertTrue(result["reviews_complete"], result)
        attempts = [r for r in workflow.rows_for(self.root) if r.get("record_type") == "model_review"]
        self.assertEqual([r["model"] for r in attempts], ["synthetic", "synthetic-B"])
        self.assertEqual(result["completion_check"]["selected_attempts"]["primary"], attempts[1]["attempt_id"])
        self.assertEqual((self.root/originals[0]["response"]["path"]).read_bytes(), original_bytes)
        self.assertTrue(self.review(runner, config=changed)["reviews_complete"])
        self.assertEqual(runner.calls, ["reviewer", "auditor", "reviewer", "auditor"])

    def test_timeout_recovery_retains_review_and_frozen_evaluation(self):
        runner = SyntheticRunner(negative=True, bad_audit=1)
        self.assertFalse(self.review(runner, purpose="evaluation")["reviews_complete"])
        changed = copy.deepcopy(CONFIG)
        for entry in [*changed["reviewers"], changed["auditor"]]:
            entry["timeout_seconds"] = 900
        result = self.review(runner, purpose="evaluation", config=changed)
        self.assertTrue(result["evaluation_complete"], result)
        self.assertEqual(runner.calls, ["reviewer", "auditor", "auditor"])
        self.assertTrue(self.review(runner, purpose="evaluation", config=changed)["evaluation_complete"])
        self.assertEqual(len(runner.calls), 3)
        changed["reviewers"][0]["model"] = "different-model"
        with self.assertRaises(ValueError):
            self.review(runner, purpose="evaluation", config=changed, revision=True)
        self.assertEqual(len(runner.calls), 3)

    def test_changed_auditor_resumes_audit_without_repeating_reviewer(self):
        runner = SyntheticRunner()
        self.review(runner)
        changed = copy.deepcopy(CONFIG)
        changed["auditor"]["model"] = "different-auditor"
        result = self.review(runner, config=changed, revision=True)
        self.assertTrue(result["reviews_complete"], result)
        self.assertEqual(runner.calls, ["reviewer", "auditor", "auditor"])
        self.assertTrue(workflow.finish(self.workspace, "case", "The final report is complete.")["completed"])

    def test_changed_command_does_not_reuse_same_model_label(self):
        runner = SyntheticRunner()
        self.review(runner)
        changed = copy.deepcopy(CONFIG)
        changed["reviewers"][0]["command"] = ["different-configured-executable"]
        self.assertTrue(self.review(runner, config=changed, revision=True)["reviews_complete"])
        self.assertEqual(runner.calls, ["reviewer", "auditor", "reviewer", "auditor"])

    def test_added_reviewer_keeps_completed_slots(self):
        runner = SyntheticRunner()
        self.review(runner)
        changed = copy.deepcopy(CONFIG)
        changed["reviewers"].append({"id": "second", "model": "synthetic-B", "format": "json"})
        result = self.review(runner, config=changed, revision=True)
        self.assertTrue(result["reviews_complete"], result)
        self.assertEqual(runner.calls, ["reviewer", "auditor", "reviewer", "auditor"])

    def test_retired_slot_keeps_history_without_repeating_completed_reviews(self):
        runner = SyntheticRunner()
        two = copy.deepcopy(CONFIG)
        two["reviewers"].append({"id": "second", "model": "synthetic-B", "format": "json"})
        self.assertTrue(self.review(runner, config=two)["reviews_complete"])
        original = workflow.rows_for(self.root)
        with self.assertRaises(ValueError):
            self.review(runner)
        self.assertEqual(workflow.rows_for(self.root), original)
        result = self.review(runner, revision=True)
        self.assertTrue(result["reviews_complete"], result)
        self.assertEqual(result["completion_check"]["completed_slots"], 1)
        self.assertEqual(runner.calls, ["reviewer", "auditor", "reviewer", "auditor"])
        retained = workflow.rows_for(self.root)
        self.assertEqual(retained[:len(original)], original)
        self.assertEqual(len([r for r in retained if r.get("record_type") == "review_plan_change"]), 1)
        self.assertTrue(workflow.finish(self.workspace, "case", "The final report is complete.")["completed"])

    def test_rename_and_return_preserve_first_valid_results_and_plan_chain(self):
        runner = SyntheticRunner()
        first = self.review(runner)
        renamed = copy.deepcopy(CONFIG)
        renamed["reviewers"][0]["id"] = "renamed"
        self.assertTrue(self.review(runner, config=renamed, revision=True)["reviews_complete"])
        returned = self.review(runner, revision=True)
        self.assertTrue(returned["reviews_complete"], returned)
        self.assertEqual(first["completion_check"]["selected_attempts"], returned["completion_check"]["selected_attempts"])
        self.assertEqual(len(runner.calls), 4)
        self.assertTrue(self.review(runner)["reviews_complete"])
        self.assertEqual(len(runner.calls), 4)
        self.assertEqual(len([r for r in workflow.rows_for(self.root) if r.get("record_type") == "review_plan_change"]), 2)

    def test_unknown_history_is_not_silently_ignored(self):
        self.review(SyntheticRunner())
        row = copy.deepcopy(next(r for r in workflow.rows_for(self.root) if r.get("record_type") == "model_review"))
        row.update(attempt_id="unplanned-attempt", slot_id="unknown-slot")
        workflow.append_row(self.root, row)
        outcome = workflow.completion(self.root, workflow.load(self.root, "state/progress.json"), "final.md")
        self.assertIn("invalid_review_record", outcome["flags"])

    def test_plan_change_needs_authorization_bound_snapshots_and_continuity(self):
        runner = SyntheticRunner()
        self.review(runner)
        renamed = copy.deepcopy(CONFIG)
        renamed["reviewers"][0]["id"] = "renamed"
        self.review(runner, config=renamed, revision=True)
        self.review(runner, revision=True)
        rows = workflow.rows_for(self.root)
        changes = [i for i, r in enumerate(rows) if r.get("record_type") == "review_plan_change"]
        variants = []
        unauthorized = copy.deepcopy(rows)
        unauthorized[changes[0]]["revision_authorized"] = False
        variants.append(unauthorized)
        unbound = copy.deepcopy(rows)
        unbound[changes[0]]["previous_plan"]["sha256"] = "0" * 64
        variants.append(unbound)
        broken_chain = copy.deepcopy(rows)
        broken_chain[changes[1]]["previous_plan"] = broken_chain[changes[0]]["previous_plan"]
        variants.append(broken_chain)
        for records in variants:
            workflow.save_text(self.root, "logs/review.jsonl", "".join(json.dumps(r)+"\n" for r in records))
            outcome = workflow.completion(self.root, workflow.load(self.root, "state/progress.json"), "final.md")
            self.assertFalse(outcome["ok"], outcome)
        workflow.save_text(self.root, "logs/review.jsonl", "".join(json.dumps(r)+"\n" for r in rows))
        self.assertTrue(workflow.completion(self.root, workflow.load(self.root, "state/progress.json"), "final.md")["ok"])

    def test_frozen_evaluation_cannot_retire_or_rename_a_negative_reviewer(self):
        runner = SyntheticRunner(negative=True)
        two = copy.deepcopy(CONFIG)
        two["reviewers"].append({"id": "second", "model": "synthetic-B", "format": "json"})
        self.assertTrue(self.review(runner, config=two, purpose="evaluation")["evaluation_complete"])
        original = workflow.rows_for(self.root)
        renamed = copy.deepcopy(two)
        renamed["reviewers"][0]["id"] = "renamed"
        for changed in (CONFIG, renamed):
            with self.assertRaises(ValueError):
                self.review(runner, config=changed, purpose="evaluation", revision=True)
        self.assertEqual(workflow.rows_for(self.root), original)
        self.assertEqual(len(runner.calls), 4)

    def test_local_reading_evidence_must_exist_be_nonempty_and_stay_inside_task(self):
        (self.root/"empty.md").write_text(" \n\t", encoding="utf-8")
        (self.root/"directory.md").mkdir()
        (self.workspace/"outside.md").write_text("Outside the task.", encoding="utf-8")
        path = self.root/"data/source_registry.csv"
        source_rows = list(csv.DictReader(path.read_text(encoding="utf-8").splitlines()))
        for value in ("missing.md", "sources/does-not-exist.md", "empty.md", "directory.md", "../outside.md", str(self.workspace/"outside.md")):
            source_rows[0]["read_evidence"] = value
            with path.open("w", encoding="utf-8", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=source_rows[0].keys())
                writer.writeheader(); writer.writerows(source_rows)
            for stage in ("analyze", "draft"):
                with self.subTest(evidence=value, stage=stage), self.assertRaises(ValueError):
                    workflow.status(self.workspace, "case", stage=stage)

    def test_local_notes_and_other_locator_forms_keep_positive_controls(self):
        (self.root/"reading notes.md").write_text("Read the complete shipment statement.", encoding="utf-8")
        path = self.root/"data/source_registry.csv"
        source_rows = list(csv.DictReader(path.read_text(encoding="utf-8").splitlines()))
        for value in ("source.md", "source.md#paragraph-1", "source.md: paragraph 1", "reading notes.md", "[Reading](source.md#paragraph-1)", "https://example.org/notes#S1", "S1: pp. 2-3"):
            source_rows[0]["read_evidence"] = value
            with path.open("w", encoding="utf-8", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=source_rows[0].keys())
                writer.writeheader(); writer.writerows(source_rows)
            with self.subTest(evidence=value):
                self.assertEqual(workflow.status(self.workspace, "case", stage="draft")["progress"]["stage"], "draft")

    def test_unchanged_legacy_reviews_are_not_repeated(self):
        runner = SyntheticRunner(negative=True)
        self.review(runner, purpose="evaluation")
        rows = workflow.rows_for(self.root)
        for row in rows:
            row.pop("reviewer_signature", None)
            row.pop("auditor_signature", None)
        workflow.save_text(self.root, "logs/review.jsonl", "".join(json.dumps(row)+"\n" for row in rows))
        progress = workflow.load(self.root, "state/progress.json")
        progress["review_plan"]["runner_signature"] = workflow.digest(CONFIG)
        progress["review_plan"].pop("auditor_signature")
        for slot in progress["review_plan"]["slots"]:
            slot.pop("reviewer_signature")
        workflow.save(self.root, "state/progress.json", progress)
        for _ in range(2):
            self.assertTrue(self.review(runner, purpose="evaluation")["evaluation_complete"])
        self.assertEqual(runner.calls, ["reviewer", "auditor"])

    def test_requirements_are_supplied_to_both_contexts_and_bound_at_delivery(self):
        requirement = {"requirement_id": "R1", "source_turn": "2", "summary": "Distinguish shipments from revenue.",
                       "status": "satisfied", "evidence": ["final.md, paragraph 2"]}
        content = json.dumps(requirement)+"\n"
        ledger = self.root/"state/requirements.jsonl"
        ledger.write_text(content, encoding="utf-8")
        runner = SyntheticRunner()
        self.assertTrue(self.review(runner)["reviews_complete"])
        self.assertEqual([r["assignment"]["requirements"] for r in runner.requests], [content, content])
        requirement["summary"] = "Include a comparison table."
        ledger.write_text(json.dumps(requirement)+"\n", encoding="utf-8")
        self.assertFalse(workflow.finish(self.workspace, "case", "The final report is complete.")["completed"])
        ledger.unlink()
        self.assertFalse(workflow.finish(self.workspace, "case", "The final report is complete.")["completed"])
        ledger.write_text(content, encoding="utf-8")
        self.assertTrue(workflow.finish(self.workspace, "case", "The final report is complete.")["completed"])

    def test_malformed_requirements_never_reach_a_reviewer(self):
        (self.root/"state/requirements.jsonl").write_text("{broken json}", encoding="utf-8")
        runner = SyntheticRunner()
        with self.assertRaises(ValueError):
            self.review(runner)
        self.assertEqual(runner.calls, [])

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


class ReadinessTests(unittest.TestCase):
    def test_missing_executable_is_reported_before_research(self):
        with patch.dict(os.environ, {"RESEARCH_TOOLKIT_REVIEW_CONFIG": ""}), patch("review_runner.shutil.which", return_value=None), patch("review_runner.subprocess.run") as run:
            result = review_readiness()
        self.assertEqual(result["status"], "blocked")
        self.assertFalse(result["model_access_verified"])
        run.assert_not_called()

    def test_login_probe_is_local_bounded_and_redacted(self):
        for code, expected in ((0, "local_checks_passed"), (1, "blocked")):
            with self.subTest(code=code), patch.dict(os.environ, {"RESEARCH_TOOLKIT_REVIEW_CONFIG": ""}), patch("review_runner.shutil.which", return_value="codex"), patch("review_runner.subprocess.run") as run:
                run.return_value.returncode = code
                run.return_value.stdout = b"private-account-detail"
                result = review_readiness()
                self.assertEqual(result["status"], expected)
                self.assertNotIn("private-account-detail", json.dumps(result))
                self.assertEqual(run.call_args.args[0], ["codex", "login", "status"])
                self.assertEqual(run.call_args.kwargs["timeout"], 10)
                self.assertEqual(run.call_count, 1)

    def test_custom_commands_are_not_executed_by_readiness(self):
        config = copy.deepcopy(CONFIG)
        for entry in [*config["reviewers"], config["auditor"]]:
            entry["command"] = [sys.executable, "custom-adapter.py"]
        with patch("review_runner.load_review_config", return_value=config), patch("review_runner.subprocess.run") as run:
            result = review_readiness()
        self.assertEqual(result["status"], "unverified")
        self.assertFalse(result["model_access_verified"])
        run.assert_not_called()

    def test_invalid_config_is_a_concrete_readiness_failure(self):
        with patch("review_runner.load_review_config", side_effect=ValueError("private configuration detail")):
            result = review_readiness()
        self.assertEqual(result["status"], "blocked")
        self.assertNotIn("private configuration detail", json.dumps(result))


if __name__ == "__main__":
    if os.environ.get("IRF_TEST_TMPDIR"):
        tempfile.tempdir = os.environ["IRF_TEST_TMPDIR"]
    unittest.main()
