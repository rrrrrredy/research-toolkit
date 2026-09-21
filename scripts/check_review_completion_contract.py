#!/usr/bin/env python3
"""Synthetic controls for required review slots, audits and sampling; no model calls."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest

import check_delivery as delivery
from check_review_completion import inspect_review_completion
from check_delivery_contract import BASE, FINAL, bind_synthetic_reviews, seal


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def synthetic_review_records(root, purpose="evaluation"):
    """Build record-consistency controls, never evidence of an actual model review."""
    def ref(name, value):
        p = root / "reviews" / name
        write_json(p, value)
        return {"path": p.relative_to(root).as_posix(), "sha256": delivery.sha256_file(p)}

    artifact_hash = delivery.sha256_file(root / "final.md")
    packet = ref("input.json", {"synthetic": True, "brief": "Check shipment claims.",
                               "report": (root / "final.md").read_text(encoding="utf-8"),
                               "evidence": "The source reports twelve shipments."})
    slots, rows = [], []
    for index in range(2):
        sid, aid = f"slot-{index}", f"attempt-{index}"
        reviewer, model = f"reviewer-{index}", f"model-{index}"
        slot = {"slot_id": sid, "reviewer_id": reviewer, "model": model,
                "scope": "full_report", "dimensions": ["evidence"], "input": packet}
        slots.append(slot)
        response = ref(f"response-{index}.json", {"synthetic": True, "reviewer": reviewer,
                       "assessment": "The source supports shipments, not revenue."})
        rows.extend([
            {"record_type": "model_review", "slot_id": sid, "attempt_id": aid,
             "reviewer_id": reviewer, "model": model, "scope": "full_report",
             "status": "completed", "artifact_sha256": artifact_hash, "input": packet,
             "execution_id": f"synthetic-call-{index}",
             "execution": ref(f"execution-{index}.json", {"synthetic": True, "id": index, "model": model}),
             "response": response, "report_verdict": "pass",
             "coverage": {"evidence": {"location": "paragraph 1", "basis": "Compared the shipment statement with the source."}},
             "findings": []},
            {"record_type": "review_audit", "attempt_id": aid, "auditor_id": "independent-auditor",
             "result": "valid", "response_sha256": response["sha256"],
             "basis": "The response addresses the declared dimension with a located observation.",
             "evidence": ref(f"audit-{index}.json", {"synthetic": True, "review": aid, "checks": ["coverage", "binding"]}),
             "dispositions": {}},
        ])
    sampling = {"method": "Check the decisive claim and a preselected passing passage.",
                "population": ["C1", "C2"], "selected": ["C1", "C2"], "mandatory": ["C1"]}
    rows.append({"record_type": "sampling_audit", "auditor_id": "independent-auditor",
                 "artifact_sha256": artifact_hash, "selected": ["C1", "C2"],
                 "evidence": ref("sampling.json", {"synthetic": True, "checked": ["C1", "C2"]}),
                 "checks": {item: {"result": "clear", "evidence": f"Source comparison for {item}."}
                            for item in sampling["selected"]}})
    plan = {"purpose": purpose, "author_id": "author", "artifact_sha256": artifact_hash,
            "slots": slots, "sampling": sampling}
    return plan, rows


class ReviewCompletionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="research-review-contract-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "final.md").write_text("The source reports twelve shipments.\n", encoding="utf-8")
        self.plan, self.rows = synthetic_review_records(self.root)

    def inspect(self):
        return inspect_review_completion(
            self.root, {"review_plan": self.plan}, "final.md", self.rows,
            hash_file=delivery.sha256_file, resolve_path=delivery.resolve_inside)

    def reject(self, flag):
        result = self.inspect()
        self.assertFalse(result["ok"], result)
        self.assertIn(flag, result["flags"], result)
        return result

    def negative_review(self):
        self.rows[0]["report_verdict"] = "needs_revision"
        self.rows[0]["findings"] = [{"finding_id": "F1", "severity": "major",
                                     "location": "paragraph 1", "basis": "Shipment evidence cannot establish revenue."}]
        self.rows[1]["dispositions"] = {"F1": {"decision": "confirmed_defect",
                                               "reason": "The source supports units only.", "evidence": "Input source, paragraph 1."}}

    def test_complete_zero_finding_controls_do_not_certify_semantics(self):
        result = self.inspect()
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["completed_slots"], 2)
        self.assertFalse(result["execution_authenticity_verified"])
        self.assertFalse(result["semantic_verification"])
        self.assertFalse(result["report_quality_certified"])

    def test_failures_and_truncation_do_not_complete_a_slot(self):
        for status in ("failed", "incomplete"):
            with self.subTest(status=status):
                self.rows[0]["status"] = status
                self.reject("missing_valid_review")

    def test_failed_attempt_is_retained_before_a_successful_completion(self):
        failure = copy.deepcopy(self.rows[0])
        failure.update(attempt_id="failed-original", status="failed")
        self.rows.insert(0, failure)
        result = self.inspect()
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["selected_attempts"]["slot-0"], "attempt-0")

    def test_missing_or_wrong_response_and_invocation_are_rejected(self):
        original = copy.deepcopy(self.rows)
        for field, replacement, flag in [
            ("response", None, "missing_review_evidence"),
            ("execution", {}, "missing_review_evidence"),
            ("model", "unexpected-model", "review_slot_mismatch"),
            ("artifact_sha256", "0" * 64, "stale_model_review"),
            ("execution_id", "", "missing_review_execution"),
        ]:
            with self.subTest(field=field):
                self.rows = copy.deepcopy(original)
                self.rows[0][field] = replacement
                self.reject(flag)

    def test_changed_input_or_artifact_invalidates_bindings(self):
        (self.root / self.plan["slots"][0]["input"]["path"]).write_text("Different input\n", encoding="utf-8")
        self.reject("stale_review_evidence")
        (self.root / "final.md").write_text("A changed report.\n", encoding="utf-8")
        self.reject("stale_review_plan")

    def test_missing_coverage_and_unreviewed_boilerplate_are_not_valid(self):
        self.rows[0]["coverage"] = {}
        self.reject("incomplete_review_coverage")
        self.rows[1]["result"] = "invalid"
        self.reject("missing_valid_review")

    def test_author_self_review_and_self_validation_are_rejected(self):
        self.plan["slots"][0]["reviewer_id"] = "author"
        self.reject("author_counted_as_reviewer")
        self.plan["slots"][0]["reviewer_id"] = "reviewer-0"
        self.rows[1]["auditor_id"] = "reviewer-0"
        self.reject("self_validated_review")

    def test_one_execution_or_response_cannot_fill_two_slots(self):
        self.rows[2]["execution_id"] = self.rows[0]["execution_id"]
        self.rows[2]["response"] = copy.deepcopy(self.rows[0]["response"])
        self.rows[3]["response_sha256"] = self.rows[0]["response"]["sha256"]
        self.reject("reused_review_execution")
        self.reject("reused_review_response")

    def test_negative_evaluation_is_complete_but_report_delivery_is_not(self):
        self.negative_review()
        self.assertTrue(self.inspect()["ok"], self.inspect())
        self.plan["purpose"] = "report_delivery"
        self.reject("report_not_ready")

    def test_critical_disposition_requires_evidence_and_independence(self):
        self.negative_review()
        self.rows[1]["dispositions"]["F1"]["reason"] = ""
        self.reject("unhandled_review_findings")
        self.rows[1]["dispositions"]["F1"]["reason"] = "The author considers it optional."
        self.rows[1]["dispositions"]["F1"]["decision"] = "no_change"
        self.rows[1]["auditor_id"] = "author"
        self.reject("missing_independent_adjudication")

    def test_later_favorable_review_cannot_replace_first_valid_negative(self):
        self.negative_review()
        later, audit = copy.deepcopy(self.rows[0]), copy.deepcopy(self.rows[1])
        later.update(attempt_id="later-favorable", report_verdict="pass", findings=[])
        audit.update(attempt_id="later-favorable", dispositions={})
        self.rows.extend([later, audit])
        self.plan["purpose"] = "report_delivery"
        result = self.reject("report_not_ready")
        self.assertNotEqual(result["selected_attempts"].get("slot-0"), "later-favorable")

    def test_invalidating_an_earlier_result_requires_evidence(self):
        self.rows[1].update(result="invalid", basis="", evidence=None)
        self.reject("invalid_review_audit")
        self.reject("missing_review_evidence")

    def test_author_or_reviewer_cannot_invalidate_negative_and_select_positive(self):
        self.negative_review()
        original_rows = copy.deepcopy(self.rows)
        for auditor, flag in (("author", "missing_independent_adjudication"),
                              ("reviewer-0", "self_validated_review")):
            with self.subTest(auditor=auditor):
                self.rows = copy.deepcopy(original_rows)
                later, audit = copy.deepcopy(self.rows[0]), copy.deepcopy(self.rows[1])
                later.update(attempt_id="later-positive", report_verdict="pass", findings=[])
                audit.update(attempt_id="later-positive", dispositions={})
                invalidation = copy.deepcopy(self.rows[1])
                invalidation.update(result="invalid", auditor_id=auditor,
                                    basis="The author or original reviewer rejects the criticism.")
                self.rows.extend([invalidation, later, audit])
                self.plan["purpose"] = "report_delivery"
                self.reject(flag)

    def test_current_version_can_complete_without_discarding_old_negative(self):
        self.negative_review()
        historical_rows = copy.deepcopy(self.rows)
        shutil.copytree(self.root / "reviews", self.root / "reviews-v1")
        for row in historical_rows:
            for field in ("input", "response", "execution", "evidence"):
                if isinstance(row.get(field), dict) and "path" in row[field]:
                    row[field]["path"] = row[field]["path"].replace("reviews/", "reviews-v1/", 1)
        (self.root / "final.md").write_text("The source reports twelve shipments; revenue is not stated.\n", encoding="utf-8")
        plan, rows = synthetic_review_records(self.root, purpose="report_delivery")
        for row in rows:
            if "attempt_id" in row:
                row["attempt_id"] = "current-" + row["attempt_id"]
            if row.get("record_type") == "model_review":
                row["execution_id"] = "current-" + row["execution_id"]
        self.plan, self.rows = plan, historical_rows + rows
        result = self.inspect()
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["selected_attempts"]["slot-0"], "current-attempt-0")
        self.assertEqual(self.rows[0]["report_verdict"], "needs_revision")

    def test_sampling_includes_mandatory_and_passed_items(self):
        self.plan["sampling"]["selected"] = ["C2"]
        self.reject("invalid_sampling_plan")
        self.plan["sampling"]["selected"] = ["C1", "C2"]
        del self.rows[-1]["checks"]["C2"]
        self.reject("incomplete_sampling_audit")

    def test_sampling_defect_needs_a_recorded_follow_up(self):
        self.rows[-1]["checks"]["C2"]["result"] = "defect"
        self.reject("unhandled_sampling_defect")
        check = self.rows[-1]["checks"]["C2"]
        check.update(defect_type="report", follow_up="The required correction remains unresolved.")
        self.reject("unhandled_sampling_defect")
        check["follow_up"] = {
            "decision": "confirmed_defect",
            "reason": "Expanded same-source checks; retained the supported limitation in evaluation findings.",
            "evidence": copy.deepcopy(self.rows[-1]["evidence"]),
        }
        self.assertTrue(self.inspect()["ok"], self.inspect())
        self.plan["purpose"] = "report_delivery"
        self.reject("unhandled_sampling_defect")
        for decision in ("resolved", "no_change"):
            check["follow_up"]["decision"] = decision
            self.assertTrue(self.inspect()["ok"], self.inspect())
        self.plan["purpose"] = "evaluation"
        check.update(defect_type="review_validity")
        check["follow_up"]["decision"] = "unresolved"
        self.reject("unhandled_sampling_defect")
        check["follow_up"]["decision"] = "resolved"
        check["follow_up"]["evidence"]["sha256"] = "0" * 64
        self.reject("stale_review_evidence")

    def test_outside_evidence_and_stale_validity_audits_fail(self):
        self.rows[1]["evidence"]["path"] = "../outside.json"
        self.reject("missing_review_evidence")
        self.rows[1]["response_sha256"] = "0" * 64
        self.reject("stale_review_audit")

    def test_malformed_fields_fail_closed_instead_of_crashing(self):
        initial_plan, initial_rows = copy.deepcopy(self.plan), copy.deepcopy(self.rows)
        for target, key in (("plan", "purpose"), ("plan", "author_id"),
                            ("review", "response"), ("review", "report_verdict"),
                            ("audit", "auditor_id"), ("audit", "result")):
            with self.subTest(target=target, key=key):
                self.plan, self.rows = copy.deepcopy(initial_plan), copy.deepcopy(initial_rows)
                row = {"plan": self.plan, "review": self.rows[0], "audit": self.rows[1]}[target]
                row[key] = ["malformed"]
                self.assertFalse(self.inspect()["ok"])

    def test_default_delivery_requires_new_contract_but_old_records_remain_inspectable(self):
        root = self.root / "delivery"
        shutil.copytree(BASE, root)
        shutil.copyfile(FINAL, root / "final.md")
        bind_synthetic_reviews(root)
        seal(root)
        old = delivery.evaluate_delivery(root, contract_version=2)
        self.assertTrue(old["ok"], old)
        self.assertFalse(old["current_contract_checked"])
        self.assertIn("missing_review_plan", delivery.evaluate_delivery(root)["flags"])
        plan, rows = synthetic_review_records(root, purpose="report_delivery")
        progress_path = root / "state/progress.json"
        progress = json.loads(progress_path.read_text(encoding="utf-8"))
        progress["review_plan"] = plan
        write_json(progress_path, progress)
        with (root / "logs/review.jsonl").open("a", encoding="utf-8") as stream:
            for row in rows:
                stream.write(json.dumps(row) + "\n")
        seal(root)
        current = delivery.evaluate_delivery(root)
        self.assertTrue(current["ok"], current)
        self.assertTrue(current["current_contract_checked"])
        import run_evals
        case = copy.deepcopy(next(c for c in run_evals.load_cases(Path(__file__).resolve().parents[1] / "evals/cases")
                                  if c["case_id"] == "model_company_pipeline_long_horizon_zh"))
        case["delivery_check"] = False
        sources = run_evals.load_sources(Path(__file__).resolve().parents[1] / "evals")
        self.assertEqual(run_evals.evaluate_case(case, root, sources)["conformance_status"], "pass")
        progress["review_plan"]["slots"].append({**copy.deepcopy(plan["slots"][0]), "slot_id": "missing-third-slot"})
        write_json(progress_path, progress)
        seal(root)
        result = run_evals.evaluate_case(case, root, sources)
        self.assertIn("missing_valid_review", result["conformance_flags"])
        self.assertNotEqual(result["conformance_status"], "pass")
        self.assertEqual(result["research_quality_status"], "not_evaluated")


if __name__ == "__main__":
    if os.environ.get("IRF_TEST_TMPDIR"):
        tempfile.tempdir = os.environ["IRF_TEST_TMPDIR"]
    unittest.main(verbosity=2)
