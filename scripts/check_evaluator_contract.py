#!/usr/bin/env python3
"""Cross-entry regressions for current review state, disclosure and language controls."""
from __future__ import annotations

import copy
import csv
import io
import subprocess
import sys
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest

import check_delivery as delivery
from check_delivery_contract import BASE, FINAL, REPO, seal, write_json, bind_synthetic_reviews
from check_review_completion_contract import synthetic_review_records
import run_evals as evaluator


class EvaluatorContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.case = next(c for c in evaluator.load_cases(REPO / "evals/cases")
                        if c["case_id"] == "model_company_pipeline_long_horizon_zh")
        cls.sources = evaluator.load_sources(REPO / "evals")

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="irf-evaluator-contract-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "task"
        shutil.copytree(BASE, self.root)
        shutil.copyfile(FINAL, self.root / "final.md")
        bind_synthetic_reviews(self.root)

    def progress(self, **changes):
        path = self.root / "state/progress.json"
        value = json.loads(path.read_text(encoding="utf-8"))
        value.update(changes)
        write_json(path, value)

    def review(self, scope, result, **fields):
        fields.setdefault("artifact_sha256", delivery.sha256_file(self.root / "final.md"))
        with (self.root / "logs/review.jsonl").open("a", encoding="utf-8") as out:
            out.write(json.dumps({"scope": scope, "result": result, **fields}) + "\n")

    def check(self, *, delivery_enabled=True):
        seal(self.root)
        case = copy.deepcopy(self.case)
        case["delivery_check"] = delivery_enabled
        d = delivery.evaluate_delivery(self.root, contract_version=2)
        e = evaluator.evaluate_case(case, self.root, self.sources, delivery_contract_version=2)
        self.assertNotIn("stale_delivery_receipt", d["flags"], d)
        self.assertEqual(e["research_quality_status"], "not_evaluated")
        return d, e

    def assert_both_pass(self):
        d, e = self.check()
        self.assertTrue(d["ok"], d)
        self.assertEqual(e["conformance_status"], "pass", e)

    def assert_both_fail(self):
        d, e = self.check()
        self.assertFalse(d["ok"], d)
        self.assertEqual(e["conformance_status"], "fail", e)

    def test_known_good(self):
        self.assert_both_pass()

    def current_case(self):
        plan, rows = synthetic_review_records(self.root, purpose="report_delivery")
        self.progress(review_plan=plan)
        with (self.root / "logs/review.jsonl").open("a", encoding="utf-8") as out:
            for row in rows:
                out.write(json.dumps(row, ensure_ascii=False) + "\n")
        seal(self.root)
        return copy.deepcopy(self.case)

    def test_missing_required_files_fail_with_or_without_delivery_check(self):
        case = self.current_case()
        calculations = self.root / "data/calculations.csv"
        calculations.write_text("metric,value\nshipments,12\n", encoding="utf-8")
        case["artifact_requirements"].append("data/calculations.csv")
        for enabled in (True, False):
            case["delivery_check"] = enabled
            positive = evaluator.evaluate_case(case, self.root, self.sources)
            self.assertEqual(positive["conformance_status"], "pass", positive)
            self.assertEqual(positive["conformance_score"], 100, positive)
            for relative in ("data/calculations.csv", "conversation/assistant_messages.jsonl"):
                with self.subTest(delivery_check=enabled, missing=relative):
                    path = self.root / relative
                    original = path.read_bytes()
                    path.unlink()
                    try:
                        result = evaluator.evaluate_case(case, self.root, self.sources)
                    finally:
                        path.write_bytes(original)
                    self.assertEqual(result["delivery_contract_version"], 3)
                    self.assertEqual(result["conformance_status"], "fail", result)
                    self.assertIn("missing_required_artifacts", result["conformance_flags"])
                    self.assertFalse(result["artifacts"][relative])
                    self.assertIn("Missing artifacts: " + relative, result["findings"])
                    self.assertEqual(result["research_quality_status"], "not_evaluated")

    def test_directory_does_not_satisfy_a_required_file(self):
        case = self.current_case()
        relative = "data/calculations.csv"
        case["artifact_requirements"].append(relative)
        (self.root / relative).mkdir()
        result = evaluator.evaluate_case(case, self.root, self.sources)
        self.assertEqual(result["conformance_status"], "fail", result)
        self.assertIn("missing_required_artifacts", result["conformance_flags"])
        self.assertFalse(result["artifacts"][relative])

    def test_self_waived_requirement_fails_even_without_receipt_check(self):
        with (self.root / "state/requirements.jsonl").open("a", encoding="utf-8") as out:
            out.write(json.dumps({"requirement_id": "R-new", "status": "waived"}) + "\n")
        for enabled in (True, False):
            d, e = self.check(delivery_enabled=enabled)
            self.assertIn("unresolved_required_corrections", d["flags"], d)
            self.assertIn("unresolved_required_corrections", e["coverage_flags"], e)
            self.assertEqual(e["conformance_status"], "fail", e)

    def test_new_prose_with_only_a_new_receipt_fails_both_entries(self):
        with (self.root / "final.md").open("a", encoding="utf-8") as out:
            out.write("\nA substantial new claim appended after the latest complete review.\n")
        d, e = self.check()
        self.assertIn("stale_review_artifact", d["flags"], d)
        self.assertIn("stale_review_artifact", e["conformance_flags"], e)

    def test_current_review_recovery_is_valid_in_both_entries(self):
        with (self.root / "final.md").open("a", encoding="utf-8") as out:
            out.write("\nA new claim separately reviewed as part of the whole report.\n")
        self.review("full_report", "PASS")
        self.assert_both_pass()

    def test_invalid_contract_version_fails_even_without_receipt_check(self):
        case = copy.deepcopy(self.case)
        case["delivery_check"] = False
        seal(self.root)
        for version in (0, 4, True, "1", None, 1.0, 2.0):
            with self.subTest(version=version):
                result = evaluator.evaluate_case(case, self.root, self.sources,
                                                 delivery_contract_version=version)
                self.assertIn("invalid_delivery_contract_version", result["conformance_flags"])
                self.assertEqual(result["conformance_status"], "fail")
                self.assertFalse(any("Historical delivery" in value for value in result["findings"]))

    def test_legacy_result_is_explicit_even_without_receipt_check(self):
        case = copy.deepcopy(self.case)
        case["delivery_check"] = False
        seal(self.root)
        result = evaluator.evaluate_case(case, self.root, self.sources, delivery_contract_version=1)
        self.assertEqual(result["delivery_contract_version"], 1)
        self.assertEqual(result["conformance_status"], "pass")
        self.assertTrue(any("not current-contract acceptance" in value for value in result["findings"]))
        self.assertEqual(result["research_quality_status"], "not_evaluated")

    def test_failure_then_global_recovery(self):
        self.review("full_report", "FAIL", issues=["Fix the claim"])
        self.review("global_final_delivery", "PASS", issues=[])
        self.assert_both_pass()

    def test_pass_then_failure(self):
        self.review("full_report", "PASS")
        self.review("full_report", "FAIL")
        self.assert_both_fail()

    def test_late_local_blocker_invalidates_global_pass(self):
        self.review("unit_a", "FAIL", issues=["New blocking finding"])
        self.assert_both_fail()

    def test_local_pass_cannot_clear_another_scope(self):
        self.review("unit_a", "FAIL")
        self.review("unit_b", "PASS")
        self.assert_both_fail()

    def test_local_recovery_does_not_clear_global_failure(self):
        self.review("full_report", "FAIL")
        self.review("unit_a", "PASS")
        self.assert_both_fail()

    def test_late_local_recovery_has_positive_control(self):
        self.review("unit_a", "FAIL")
        self.review("unit_a", "PASS", issues=[])
        self.assert_both_pass()

    def test_global_review_covers_earlier_ordinary_unit_review(self):
        self.review("unit_a", "FAIL")
        self.review("full_report", "PASS", issues=[])
        self.assert_both_pass()

    def test_declared_scope_cannot_be_erased_by_global_pass(self):
        self.progress(required_review_scopes=["evidence"])
        self.review("evidence", "FAIL")
        self.review("full_report", "PASS")
        self.assert_both_fail()

    def test_malformed_history_is_not_erased_by_pass(self):
        with (self.root / "logs/review.jsonl").open("a", encoding="utf-8") as out:
            out.write("not valid JSON\n")
        self.review("full_report", "PASS")
        self.assert_both_fail()

    def test_routed_action_is_not_resolution_even_without_receipt_check(self):
        self.progress(blockers=[{"id": "R1", "routed_action": "Verify this next"}])
        d, e = self.check(delivery_enabled=False)
        self.assertFalse(d["ok"], d)
        self.assertIn("false_completion_signal", e["conformance_flags"], e)

    def test_invalid_utf8_is_rejected_without_optional_receipt_check(self):
        with (self.root / "logs/review.jsonl").open("ab") as out:
            out.write(b'{"scope":"full_report","result":"PASS","note":"\xff"}\n')
        d, e = self.check(delivery_enabled=False)
        self.assertIn("invalid_review_log", d["flags"], d)
        self.assertIn("invalid_review_log", e["conformance_flags"], e)

    def test_conflicting_failure_status_is_not_hidden_by_result_pass(self):
        self.review("full_report", "PASS", status="FAIL")
        self.assert_both_fail()

    def test_explicitly_resolved_routed_action_is_valid(self):
        self.progress(blockers=[{"id": "R1", "status": "resolved",
                                 "routed_action": "Verify", "resolution": "Corrected claim"}])
        self.assert_both_pass()

    def test_explicit_open_status_wins_over_handling_text(self):
        item = {"status": "open", "handling": "Investigate tomorrow"}
        self.assertTrue(delivery.issue_is_open(item))
        self.assertTrue(evaluator.issue_is_unhandled(item))

    def test_blanket_denial_cannot_disclose_existing_limitations(self):
        for message in ("报告已完成，没有任何限制。", "The report is complete. No limitations."):
            with self.subTest(message=message):
                (self.root / "delivery_message.md").write_text(message, encoding="utf-8")
                d, e = self.check()
                self.assertIn("undisclosed_accepted_limitations", d["flags"], d)
                self.assertEqual(e["conformance_status"], "fail", e)

    def test_specific_coverage_is_observed_not_semantically_certified(self):
        limits = ["无法核验关键财务数据。", "缺少采购合同。"]
        result = delivery.assess_limitation_disclosure("已知限制：无法核验关键财务数据；缺少采购合同。", limits)
        self.assertEqual(result["status"], "text_covered")
        self.assertEqual(result["unmatched_limitations"], [])
        self.assertFalse(result["semantic_verification"])

    def test_partial_disclosure_requires_review(self):
        limits = ["无法核验关键财务数据。", "缺少采购合同。"]
        result = delivery.assess_limitation_disclosure("已知限制：无法核验关键财务数据。", limits)
        self.assertEqual(result["status"], "needs_review")
        self.assertIn("缺少采购合同。", result["unmatched_limitations"])

    def test_valid_paraphrase_is_not_declared_contradictory(self):
        result = delivery.assess_limitation_disclosure(
            "限制是无法从公开资料确认收入。", ["关键财务数据无法核验。"])
        self.assertEqual(result["status"], "needs_review")

    def test_qualified_denials_and_double_negatives_remain_valid(self):
        for message in ("报告并非没有任何限制：收入无法核验。",
                        "The report is not without limitations: revenue is unverified.",
                        "已知限制是收入无法核验，没有其他限制。",
                        "Revenue is unverified; no additional limitations were found."):
            with self.subTest(message=message):
                result = delivery.assess_limitation_disclosure(message, ["收入无法核验。"])
                self.assertNotEqual(result["status"], "contradiction")

    def test_distinct_english_paragraphs_are_not_repetition(self):
        lines = ["Revenue increased as customers renewed their annual contracts.",
                 "The engineering team reduced latency through better scheduling.",
                 "Policy uncertainty may delay procurement decisions next year."]
        self.assertEqual(evaluator.repeated_line_flags("\n".join(lines)), [])
        with (self.root / "final.md").open("a", encoding="utf-8") as out:
            out.write("\n\n" + "\n\n".join(lines))
        self.review("full_report", "PASS")
        self.assert_both_pass()

    def test_real_english_repetition_still_fails(self):
        line = "Revenue increased as customers renewed their annual contracts."
        self.assertTrue(evaluator.repeated_line_flags("\n".join([line] * 3)))

    def test_distinct_chinese_control(self):
        lines = ["收入增长主要来自存量客户续约，但新增客户的获客成本尚未披露。",
                 "工程团队通过重新分配计算任务降低了延迟，具体改善幅度仍需测量。",
                 "政策变化可能影响下一年度采购节奏，企业应区分预算批准和实际签约。"]
        self.assertEqual(evaluator.repeated_line_flags("\n".join(lines)), [])

    def test_citation_variation_does_not_hide_chinese_repetition(self):
        text = "\n".join(f"《资料{i}》显示当前市场规模变化，但其口径不够明确，需要进一步核对。" for i in range(3))
        self.assertTrue(evaluator.repeated_line_flags(text))


    def test_current_receipt_rejects_deleted_optional_binding(self):
        case = self.current_case()
        self.assertEqual(evaluator.evaluate_case(case, self.root, self.sources)["conformance_status"], "pass")
        (self.root / "state/requirements.jsonl").unlink()
        result = evaluator.evaluate_case(case, self.root, self.sources)
        self.assertEqual(result["conformance_status"], "fail")
        self.assertIn("missing_delivery_inputs", result["conformance_flags"])

    def test_malformed_requirement_and_transcript_are_structured_failures(self):
        case = self.current_case()
        case["delivery_check"] = False
        for relative, flag in (
            ("state/requirements.jsonl", "invalid_requirement_log"),
            ("conversation/assistant_messages.jsonl", "invalid_transcript"),
        ):
            path = self.root / relative
            original = path.read_bytes()
            for content in ("{bad json\n", "[]\n", '\n{"id":"valid"}\n{broken\n'):
                with self.subTest(path=relative, content=content):
                    path.write_text(content, encoding="utf-8")
                    result = evaluator.evaluate_case(case, self.root, self.sources)
                    self.assertEqual(result["conformance_status"], "fail", result)
                    self.assertIn(flag, result["conformance_flags"])
                    self.assertTrue(any("row" in finding for finding in result["findings"]))
            path.write_bytes(original)

    def test_batch_preserves_good_result_after_bad_input(self):
        case = self.current_case()
        workspace = Path(self.temp.name)
        evals = workspace / "evals"
        (evals / "cases").mkdir(parents=True)
        (evals / "source_packs/control").mkdir(parents=True)
        (evals / "source_packs/control/sources.jsonl").write_text(
            "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in self.sources.values()),
            encoding="utf-8")
        runs = workspace / "runs"
        for name in ("bad", "good"):
            current = copy.deepcopy(case)
            current["case_id"] = name
            write_json(evals / "cases" / (name + ".json"), current)
            shutil.copytree(self.root, runs / name)
        bad = runs / "bad/state/requirements.jsonl"
        report, json_report = workspace / "report.md", workspace / "report.json"
        for unreadable in (False, True):
            with self.subTest(unreadable=unreadable):
                if unreadable:
                    unreadable_path = runs / "bad/final.md"
                    unreadable_path.unlink()
                    unreadable_path.mkdir()
                else:
                    bad.write_text("{bad json\n", encoding="utf-8")
                result = subprocess.run([
                    sys.executable, str(REPO / "scripts/run_evals.py"),
                    "--evals-dir", str(evals), "--runs-dir", str(runs),
                    "--report", str(report), "--json-report", str(json_report),
                ], capture_output=True, text=True, encoding="utf-8")
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                rows = json.loads(json_report.read_text(encoding="utf-8"))
                self.assertEqual([(row["case_id"], row["conformance_status"]) for row in rows],
                                 [("bad", "fail"), ("good", "pass")])
                self.assertIn("good", report.read_text(encoding="utf-8"))
                if unreadable:
                    self.assertIn("invalid_evaluation_input", rows[0]["conformance_flags"])

    def test_csv_source_matches_require_same_record(self):
        sources = {"S001": {"title": "Alpha Publication"}, "S002": {"title": "Beta Publication"}}
        ids = list(sources)
        control = "source_id,title\nS001,Alpha Publication\nS002,Beta Publication\n"
        swapped = "source_id,title\nS001,Beta Publication\nS002,Alpha Publication\n"
        self.assertEqual(evaluator.count_registry_sources(control, ids, sources), 2)
        self.assertEqual(evaluator.count_registry_sources(swapped, ids, sources), 0)

    def test_csv_multiline_claim_counts_as_one_record(self):
        content = 'claim_id,claim\nC1,"first line\nsecond line\nthird line"\n'
        self.assertEqual(evaluator.data_row_count(content), 1)
        self.assertEqual(evaluator.data_row_count("claim_id,claim\nC1,First\nC2,Second\n"), 2)
        case = self.current_case()
        case["delivery_check"] = False
        (self.root / "data/claims_registry.csv").write_text(content, encoding="utf-8")
        result = evaluator.evaluate_case(case, self.root, self.sources)
        self.assertEqual(result["claim_rows"], 1)
        self.assertIn("weak_claim_registry", result["conformance_flags"])

    def test_csv_corruption_fails_without_receipt_check(self):
        case = self.current_case()
        case["delivery_check"] = False
        for relative, flag in (
            ("data/claims_registry.csv", "invalid_claim_registry"),
            ("data/source_registry.csv", "invalid_source_registry"),
        ):
            path = self.root / relative
            original = path.read_text(encoding="utf-8")
            rows = list(csv.reader(io.StringIO(original)))
            mutations = [
                "wrong,columns\na,b\n",
                original + original.splitlines()[1] + "\n",
                original + 'broken,"unterminated\n',
                original + "too,few\n",
                original + ",".join(["extra"] * (len(rows[0]) + 1)) + "\n",
            ]
            for content in mutations:
                with self.subTest(path=relative, content=content[-60:]):
                    path.write_text(content, encoding="utf-8")
                    result = evaluator.evaluate_case(case, self.root, self.sources)
                    self.assertEqual(result["conformance_status"], "fail", result)
                    self.assertIn(flag, result["conformance_flags"])
            path.write_text(original, encoding="utf-8")

    def test_sentence_repetition_supports_english_and_preserves_tokens(self):
        sentence = "The evidence remains insufficient."
        self.assertTrue(evaluator.repeated_sentence_flags(" ".join([sentence] * 20)))
        self.assertTrue(evaluator.repeated_sentence_flags(" ".join([sentence.replace(".", "。")] * 20)))
        controls = [
            "Dr. Smith measured 3.14 units.",
            "U.S. revenue increased by 2.5 percent.",
            "See https://example.org/a.html?x=3.14 for source data.",
            "Options, e.g. bonds, remain available.",
            "Contact analyst@example.org for the source.",
        ]
        self.assertEqual(evaluator.repeated_sentence_flags(" ".join(controls)), [])
        for sentence in controls:
            self.assertEqual([part.strip() for part in evaluator.sentence_units(sentence) if part.strip()],
                             [sentence[:-1]])


if __name__ == "__main__":
    if os.environ.get("IRF_TEST_TMPDIR"):
        tempfile.tempdir = os.environ["IRF_TEST_TMPDIR"]
    unittest.main(verbosity=2)
