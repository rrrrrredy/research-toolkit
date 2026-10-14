#!/usr/bin/env python3
"""Offline behavioral controls for profiles and reviewer backends; no paid model calls."""
from __future__ import annotations
import copy
import csv
import json
import os
import subprocess
import sys
from pathlib import Path
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from types import SimpleNamespace
from unittest.mock import patch

import research_workflow as w
import review_runner as r
from check_delivery import evaluate_delivery
from check_research_workflow import BRIEF, SyntheticRunner
from profile_policy import CHECKLIST


class ProfileTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=os.environ.get("IRF_TEST_TMPDIR"))
        self.addCleanup(self.tmp.cleanup)
        self.workspace = Path(self.tmp.name)
        self.env = patch.dict(os.environ, {"RESEARCH_TOOLKIT_REVIEW_CONFIG": "", "RESEARCH_TOOLKIT_REVIEW_BACKEND": ""})
        self.env.start()
        self.addCleanup(self.env.stop)

    def task(self, profile="full"):
        started = w.start(self.workspace, "case", BRIEF, profile=profile)
        self.root = self.workspace/"case"
        w.save_text(self.root, "final.md", "The source reports twelve shipments.\n\nRevenue is not reported.\n")
        w.save_text(self.root, "source.md", "Company A reports twelve shipments; revenue is unknown.")
        w.save_text(self.root, "data/source_registry.csv", "source_id,title,url,source_type,read_scope,read_evidence\nS1,Shipments,https://example.org,primary,full_text,source.md\n")
        w.save_text(self.root, "data/claims_registry.csv", "claim_id,claim,claim_type,supporting_sources\nC1,Twelve shipments,verified_fact,S1\n")
        w.status(self.workspace, "case", stage="draft")
        return started

    def self_result(self, prompt, negative=False):
        result = SyntheticRunner(negative=negative)({}, {"role": "reviewer"}, None)
        return {**json.loads(result["content"]), "input_version": prompt["input_version"]}

    def test_lite_length_claim_is_checked_before_writing_receipt(self):
        self.task("lite")
        w.save_text(self.root, "state/requirements.jsonl", json.dumps({
            "requirement_id": "R-length", "summary": "At least 100 words, counting the whole file.",
            "status": "satisfied", "evidence": "final.md",
            "length_constraint": {"unit": "whitespace_words", "scope": "whole_artifact", "min": 100}})+"\n")
        items = {key: {"passed": True, "evidence": "Checked against final.md"} for key in CHECKLIST}
        result = w.finish(self.workspace, "case", "The report is complete.", checklist=items)
        self.assertFalse(result["completed"], result)
        self.assertFalse((self.root/"state/final_checklist.json").exists())

    def test_lite_open_obligations_cannot_be_closed_by_checklist_assertions(self):
        self.task("lite")
        items = {key: {"passed": True, "evidence": "final.md"} for key in CHECKLIST}
        row = {"requirement_id": "R-comparison", "summary": "Compare two options", "status": "open"}
        for status in ("open", "waived", "satisfied"):
            with self.subTest(status=status):
                w.save_text(self.root, "state/requirements.jsonl", json.dumps({**row, "status": status})+"\n")
                result = w.finish(self.workspace, "case", "Complete.", checklist=items)
                self.assertFalse(result["completed"], result)
                self.assertFalse((self.root/"state/final_checklist.json").exists())
                self.assertNotEqual(w.load(self.root, "state/progress.json")["status"], "complete")
        w.save_text(self.root, "state/requirements.jsonl", json.dumps({**row, "status": "satisfied", "evidence": "final.md paragraphs 1–2"})+"\n")
        progress = w.load(self.root, "state/progress.json")
        w.save(self.root, "state/progress.json", {**progress, "open_issues": ["Required comparison remains absent"]})
        self.assertFalse(w.finish(self.workspace, "case", "Complete.", checklist=items)["completed"])
        self.assertFalse((self.root/"state/final_checklist.json").exists())
        w.save(self.root, "state/progress.json", {**progress, "open_issues": []})
        self.assertTrue(w.finish(self.workspace, "case", "Complete.", checklist=items)["completed"])
        receipt = (self.root/"state/final_checklist.json").read_bytes()
        terminal = w.load(self.root, "state/progress.json")
        w.save(self.root, "state/progress.json", {**terminal, "open_issues": ["New required correction"]})
        self.assertFalse(evaluate_delivery(self.root)["ok"])
        self.assertEqual(w.status(self.workspace, "case")["progress"]["status"], "stale")
        self.assertEqual((self.root/"state/final_checklist.json").read_bytes(), receipt)

    def test_lite_specific_user_scope_change_and_absent_optional_ledger(self):
        self.task("lite")
        items = {key: {"passed": True, "evidence": "final.md"} for key in CHECKLIST}
        row = {"requirement_id": "R-comparison", "status": "waived", "summary": "Compare two options",
               "user_decision": {"source_turn": "turn-2", "quote": "Omit the comparison; deliver the explanation."}}
        w.save_text(self.root, "state/requirements.jsonl", json.dumps(row)+"\n")
        self.assertTrue(w.finish(self.workspace, "case", "Delivered the requested explanation.", checklist=items)["completed"])
        (self.root/"state/requirements.jsonl").unlink()
        self.assertTrue(w.finish(self.workspace, "case", "Delivered.", checklist=items)["completed"])

    def length_requirement(self, **changes):
        row = {"requirement_id": "R-length", "summary": "Count the whole report using the declared unit and bounds.",
               "status": "satisfied", "evidence": "final.md",
               "length_constraint": {"unit": "whitespace_words", "scope": "whole_artifact", "min": 1, "max": 200}}
        row.update(changes)
        w.save_text(self.root, "state/requirements.jsonl", json.dumps(row)+"\n")
        return row

    def test_length_measurements_bind_both_profiles_and_survive_checkout_newlines(self):
        for profile in ("full", "lite"):
            with self.subTest(profile=profile), tempfile.TemporaryDirectory() as tmp:
                self.workspace = Path(tmp)
                self.task(profile)
                self.length_requirement()
                args = {}
                if profile == "lite":
                    args["checklist"] = {k: {"passed": True, "evidence": "final.md and source.md"} for k in CHECKLIST}
                else:
                    prompt = w.review(self.workspace, "case", ["source.md"], reviewer="self")
                    w.review(self.workspace, "case", ["source.md"], reviewer="self", self_review=self.self_result(prompt))
                result = w.finish(self.workspace, "case", "The report is complete.", **args)
                self.assertTrue(result["completed"], result)
                self.assertEqual(result["delivery_check"]["length_checks"][0]["actual"], 9)
                name = "state/final_checklist.json" if profile == "lite" else "state/final_delivery.json"
                receipt = w.load(self.root, name)
                report = self.root/"final.md"
                report.write_bytes(report.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
                self.assertTrue(evaluate_delivery(self.root)["ok"])
                receipt["length_checks"][0]["actual"] = 8
                w.save(self.root, name, receipt)
                before = (self.root/name).read_bytes()
                status = w.status(self.workspace, "case")
                self.assertEqual(status["progress"]["status"], "stale")
                self.assertEqual((self.root/name).read_bytes(), before)

    def test_length_boundaries_use_explicit_unicode_and_whitespace_units(self):
        self.task("lite")
        w.save_text(self.root, "final.md", "# 标题\n\n甲乙，a 12。[S1]\n")
        for unit, count in (("nonwhitespace_characters", 14), ("whitespace_words", 4)):
            with self.subTest(unit=unit):
                self.length_requirement(length_constraint={"unit": unit, "scope": "whole_artifact", "min": count, "max": count})
                checks, errors = w.inspect_length_constraints(self.root, "final.md")
                self.assertEqual(errors, [])
                self.assertEqual(checks[0]["actual"], count)
                self.length_requirement(length_constraint={"unit": unit, "scope": "whole_artifact", "max": count-1})
                self.assertTrue(w.inspect_length_constraints(self.root, "final.md")[1])

    def test_malformed_or_ambiguous_length_constraints_fail_closed(self):
        self.task("lite")
        rule = {"unit": "whitespace_words", "scope": "whole_artifact", "min": 1}
        for change in ({"unit": "tokens"}, {"scope": "body_only"}, {"min": True}, {"min": -1},
                       {"min": 3, "max": 2}, {"max": 1.5}, {"min": None}, {"claimed_count": 1}):
            with self.subTest(change=change):
                self.length_requirement(length_constraint={**rule, **change})
                self.assertTrue(w.inspect_length_constraints(self.root, "final.md")[1])
        self.length_requirement(length_constraint={"unit": "whitespace_words", "scope": "whole_artifact"})
        self.assertTrue(w.inspect_length_constraints(self.root, "final.md")[1])
        row = self.length_requirement()
        w.save_text(self.root, "state/requirements.jsonl", (json.dumps(row)+"\n")*2)
        self.assertTrue(w.inspect_length_constraints(self.root, "final.md")[1])

    def test_length_waiver_keeps_measurement_and_requires_existing_user_decision(self):
        self.task("lite")
        for status in ("waived", "accepted_limitation", "out_of_scope"):
            with self.subTest(status=status):
                row = self.length_requirement(status=status, length_constraint={
                    "unit": "whitespace_words", "scope": "whole_artifact", "min": 100})
                self.assertTrue(w.inspect_length_constraints(self.root, "final.md")[1])
                self.length_requirement(**{**row, "user_decision": {
                    "source_turn": "synthetic-user-turn", "quote": "You may deliver fewer than 100 words."}})
                checks, errors = w.inspect_length_constraints(self.root, "final.md")
                self.assertEqual(errors, [])
                self.assertFalse(checks[0]["bounds_met"])
                self.assertEqual(checks[0]["status"], status)
                self.assertEqual(checks[0]["actual"], 9)

    def test_failed_length_recheck_preserves_existing_receipt_and_message(self):
        self.task("lite")
        self.length_requirement()
        items = {k: {"passed": True, "evidence": "final.md and source.md"} for k in CHECKLIST}
        self.assertTrue(w.finish(self.workspace, "case", "Original delivery.", checklist=items)["completed"])
        before = {name: (self.root/name).read_bytes() for name in
                  ("state/final_checklist.json", "state/progress.json", "delivery_message.md")}
        self.length_requirement(length_constraint={"unit": "whitespace_words", "scope": "whole_artifact", "min": 100})
        result = w.finish(self.workspace, "case", "Replacement delivery.", checklist=items)
        self.assertFalse(result["completed"])
        self.assertEqual(before, {name: (self.root/name).read_bytes() for name in before})

    def test_existing_requirements_without_length_are_not_inferred(self):
        self.task("lite")
        w.save_text(self.root, "state/requirements.jsonl", json.dumps({
            "requirement_id": "R-old", "summary": "100 words", "status": "satisfied", "evidence": "final.md"})+"\n")
        self.assertEqual(w.inspect_length_constraints(self.root, "final.md"), ([], []))

    def test_status_checks_current_full_and_lite_delivery_without_rewriting_state(self):
        for profile in ("full", "lite"):
            for mutation in ("report", "claims", "receipt"):
                with self.subTest(profile=profile, mutation=mutation), tempfile.TemporaryDirectory() as tmp:
                    workspace = Path(tmp)
                    saved_workspace = self.workspace
                    self.workspace = workspace
                    try:
                        self.task(profile)
                        args = {}
                        if profile == "lite":
                            args["checklist"] = {k: {"passed": True, "evidence": "final.md and source.md"} for k in CHECKLIST}
                        else:
                            prompt = w.review(workspace, "case", ["source.md"], reviewer="self")
                            w.review(workspace, "case", ["source.md"], reviewer="self", self_review=self.self_result(prompt))
                        self.assertTrue(w.finish(workspace, "case", "Complete without independent review.", **args)["completed"])
                        self.assertEqual(w.status(workspace, "case")["progress"]["status"], "complete")
                        before = (self.root/"state/progress.json").read_bytes()
                        if mutation == "report":
                            w.save_text(self.root, "final.md", "Changed after delivery.")
                        elif mutation == "claims":
                            (self.root/"data/claims_registry.csv").unlink()
                        else:
                            name = "final_checklist.json" if profile == "lite" else "final_delivery.json"
                            w.save_text(self.root, "state/"+name, "not JSON")
                        current = w.status(workspace, "case")
                        self.assertEqual(current["progress"]["status"], "stale")
                        self.assertFalse(current["delivery_check"]["ok"])
                        self.assertTrue(current["progress"]["open_issues"])
                        self.assertEqual((self.root/"state/progress.json").read_bytes(), before)
                    finally:
                        self.workspace = saved_workspace

    def test_negative_review_distinguishes_execution_from_delivery_and_lists_findings(self):
        self.task()
        prompt = w.review(self.workspace, "case", ["source.md"], reviewer="self")
        negative = w.review(self.workspace, "case", ["source.md"], reviewer="self", self_review=self.self_result(prompt, True))
        for result in (negative, w.review(self.workspace, "case", ["source.md"], reviewer="self")):
            self.assertTrue(result["reviews_complete"])
            self.assertEqual(result["review_check"]["completed_slots"], 1)
            self.assertFalse(result["delivery_ready"])
            self.assertIn("shipments, not revenue", " ".join(result["open_issues"]))
        progress = w.status(self.workspace, "case")["progress"]
        self.assertEqual(progress["open_issues"], negative["open_issues"])
        self.assertIn("F1", progress["next_action"])

    def test_cli_template_review_revision_and_delivery(self):
        def call(action, arguments):
            result = subprocess.run([sys.executable, "-X", "utf8", str(w.TOOLKIT/"scripts/research_workflow.py"),
                action, "--workspace", str(self.workspace)], input=json.dumps(arguments),
                text=True, encoding="utf-8", capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
            return json.loads(result.stdout)
        task = "template-cli"
        call("start", {"task": task, "brief": BRIEF, "profile": "full"})
        root = self.workspace/task
        (root/"sources").mkdir()
        (root/"sources/S1.md").write_text("The source reports twelve shipments. No revenue figure is supplied.", encoding="utf-8")
        for name, row in (("source_registry.csv", {"source_id": "S1", "title": "Shipments", "url": "https://example.org/source",
                "source_type": "primary", "read_scope": "full_text", "read_evidence": "https://example.org/source#p1", "evidence_path": "sources/S1.md"}),
                ("claims_registry.csv", {"claim_id": "C1", "claim": "Twelve shipments", "claim_type": "verified_fact", "supporting_sources": "S1"})):
            path = root/"data"/name
            with path.open(encoding="utf-8", newline="") as stream:
                fields = next(csv.reader(stream))
            with path.open("w", encoding="utf-8", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=fields); writer.writeheader(); writer.writerow(row)
        call("status", {"task": task, "stage": "draft"})
        (root/"final.md").write_text("The source reports twelve shipments.\n\nRevenue is twelve.\n", encoding="utf-8")
        args = {"task": task, "evidence_paths": ["sources/S1.md"], "reviewer": "self"}
        prompt = call("review", args)
        negative = call("review", {**args, "self_review": self.self_result(prompt, True)})
        self.assertFalse(negative["delivery_ready"])
        (root/"final.md").write_text("The source reports twelve shipments.\n\nRevenue is not reported.\n", encoding="utf-8")
        prompt = call("review", {**args, "revision": True})
        ready = call("review", {**args, "self_review": self.self_result(prompt)})
        self.assertTrue(ready["delivery_ready"])
        self.assertTrue(call("finish", {"task": task, "message": "Complete with self-review only."})["completed"])
        self.assertEqual(call("status", {"task": task})["progress"]["status"], "complete")
        history = w.rows_for(root)
        self.assertEqual([row["report_verdict"] for row in history if row.get("record_type") == "model_review"], ["needs_revision", "pass"])

    def test_lite_guidance_is_stage_specific_in_both_languages(self):
        for language, suffix in (("en", ".md"), ("zh", ".zh-CN.md")):
            for stage in w.STAGE_FILES:
                with self.subTest(language=language, stage=stage):
                    result = w.guidance(stage, language, "lite")
                    self.assertEqual(result["profile"], "lite")
                    self.assertEqual([item["path"] for item in result["guidance"]],
                                     ["references/lite-workflow" + suffix])
                    content = result["guidance"][0]["content"]
                    headings = [line.split()[1] for line in content.splitlines() if line.startswith("## ")]
                    self.assertEqual(headings, [stage])
                    self.assertNotIn("state/final_delivery.json", content)
                    if stage == "final":
                        for key in CHECKLIST:
                            self.assertIn("`" + key + "`", content)

    def test_full_guidance_keeps_its_existing_methods_and_default(self):
        for language in ("en", "zh"):
            for stage, names in w.STAGE_FILES.items():
                with self.subTest(language=language, stage=stage):
                    expected = [name.replace(".md", ".zh-CN.md") if language == "zh" else name
                                for name in names]
                    result = w.guidance(stage, language)
                    self.assertEqual(result["profile"], "full")
                    self.assertEqual(result, w.guidance(stage, language, "full"))
                    self.assertEqual([item["path"] for item in result["guidance"]], expected)

    def test_lite_status_uses_saved_profile_through_delivery(self):
        started = self.task("lite")
        self.assertEqual(started["guidance"][0]["path"], "references/lite-workflow.md")
        items = {k: {"passed": True, "evidence": "Synthetic control: final.md and source.md."}
                 for k in CHECKLIST}
        with patch.object(w, "run_reviewer", side_effect=AssertionError("must not call a backend")):
            for stage in ("analyze", "draft", "revise"):
                result = w.status(self.workspace, "case", language="zh", stage=stage)
                self.assertEqual(result["profile"], "lite")
                self.assertEqual(result["guidance"][0]["path"], "references/lite-workflow.zh-CN.md")
            self.assertTrue(w.finish(self.workspace, "case", "Complete, without independent review.",
                                     checklist=items)["completed"])
            final = w.status(self.workspace, "case", language="zh")
        self.assertEqual(final["profile"], "lite")
        self.assertEqual(final["stage"], "final")
        self.assertEqual(final["guidance"][0]["path"], "references/lite-workflow.zh-CN.md")

    def test_lite_keeps_claims_and_checklist_without_review(self):
        with patch("review_runner.shutil.which", return_value=None):
            started = self.task("lite")
        self.assertTrue(started["ready_for_collection"])
        with patch.object(w, "run_reviewer", side_effect=AssertionError("must not call a backend")):
            self.assertTrue(w.review(self.workspace, "case", ["source.md"])["skipped"])
            pending = w.finish(self.workspace, "case", "The report is complete, without independent review.")
        self.assertEqual(pending["action_required"], "final_checklist")
        items = {k: {"passed": True, "evidence": "Synthetic control: final.md paragraphs 1-2 and source.md."} for k in CHECKLIST}
        broken = copy.deepcopy(items); broken["claims_and_sources"]["passed"] = False
        self.assertFalse(w.finish(self.workspace, "case", "Complete.", checklist=broken)["completed"])
        complete = w.finish(self.workspace, "case", "Complete, without independent review.", checklist=items)
        self.assertTrue(complete["completed"], complete)
        self.assertFalse(complete["delivery_check"]["full_delivery_gates_checked"])
        self.assertEqual(w.rows_for(self.root), [])
        self.assertFalse((self.root/"state/final_delivery.json").exists())
        self.assertTrue(evaluate_delivery(self.root)["ok"])
        w.save_text(self.root, "final.md", "Changed report")
        self.assertFalse(evaluate_delivery(self.root)["ok"])

    def test_lite_does_not_bypass_brief_claims_or_saved_profile(self):
        self.task("lite")
        with self.assertRaises(ValueError):
            w.start(self.workspace, "case", BRIEF, profile="full")
        w.save_text(self.root, "data/claims_registry.csv", "claim_id,claim,claim_type,supporting_sources\n")
        with self.assertRaises(ValueError):
            w.finish(self.workspace, "case", "Complete.", checklist={})

    def test_lite_actual_delivery_cli_checks_optional_capture_without_writing(self):
        self.task("lite")
        items = {k: {"passed": True, "evidence": "final.md and source.md"} for k in CHECKLIST}
        message = "Report delivered.\nNo independent review."
        self.assertTrue(w.finish(self.workspace, "case", message, checklist=items)["completed"])
        capture = self.workspace / "actual-message.txt"
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        for content, observation, flag in (
                (None, "not_provided", None),
                (b"  Report delivered.\r\nNo independent review.\r\n", "matched", None),
                (b"Different reply.", "mismatch", "actual_delivery_mismatch"),
                (b"\xff", "unreadable", "missing_actual_delivery"),
                (False, "unreadable", "missing_actual_delivery")):
            with self.subTest(observation=observation, content=content):
                args = []
                if content is not None:
                    if content is False:
                        capture.unlink(missing_ok=True)
                    else:
                        capture.write_bytes(content)
                    args = ["--actual-message", str(capture)]
                result = subprocess.run([sys.executable, "-X", "utf8",
                    str(w.TOOLKIT / "scripts/check_delivery.py"), str(self.root), "--json", *args],
                    text=True, encoding="utf-8", capture_output=True)
                checked = json.loads(result.stdout)
                self.assertEqual(result.returncode, 1 if flag else 0, result.stdout + result.stderr)
                self.assertEqual(checked["delivery_observation"], observation)
                self.assertEqual(checked["flags"], [flag] if flag else [])
                self.assertTrue(checked["checklist_valid"])
                self.assertTrue(checked["terminal_state"])
                self.assertEqual(before, {p.relative_to(self.root): p.read_bytes()
                                         for p in self.root.rglob("*") if p.is_file()})

    def test_lite_resume_preserves_checklist_but_requires_current_completion(self):
        self.task("lite")
        items = {k: {"passed": True, "evidence": "final.md and source.md"} for k in CHECKLIST}
        self.assertTrue(w.finish(self.workspace, "case", "Complete.", checklist=items)["completed"])
        receipt = (self.root / "state/final_checklist.json").read_bytes()
        for stage in ("collect", "analyze", "draft", "revise"):
            with self.subTest(stage=stage):
                current = w.status(self.workspace, "case", stage=stage)
                self.assertEqual(current["progress"]["status"], "in_progress")
                progress = (self.root / "state/progress.json").read_bytes()
                result = evaluate_delivery(self.root)
                self.assertFalse(result["ok"], result)
                self.assertTrue(result["checklist_valid"])
                self.assertFalse(result["terminal_state"])
                self.assertEqual(result["status"], "incomplete")
                self.assertIn("incomplete_lite_task", result["flags"])
                self.assertEqual((self.root / "state/final_checklist.json").read_bytes(), receipt)
                self.assertEqual((self.root / "state/progress.json").read_bytes(), progress)
                self.assertTrue(w.finish(self.workspace, "case", "Complete.", checklist=items)["completed"])
                self.assertTrue(evaluate_delivery(self.root)["terminal_state"])
                self.assertTrue(evaluate_delivery(self.root)["ok"])

    def test_lite_research_input_changes_make_delivery_stale_without_rewriting_receipt(self):
        self.task("lite")
        items = {k: {"passed": True, "evidence": "Synthetic control: final.md and source.md."} for k in CHECKLIST}
        self.assertTrue(w.finish(self.workspace, "case", "Complete.", checklist=items)["completed"])
        receipt = (self.root/"state/final_checklist.json").read_bytes()
        progress = (self.root/"state/progress.json").read_bytes()
        for name in ("source.md", "data/source_registry.csv", "data/claims_registry.csv", "state/task_spec.md", "state/requirements.jsonl"):
            path = self.root/name
            original = path.read_bytes()
            with self.subTest(name=name):
                # Keep records structurally valid: freshness must check content, not only shape.
                if name.endswith(".csv"):
                    path.write_bytes(original.replace(b"Synthetic", b"Revised"))
                    if path.read_bytes() == original:
                        path.write_bytes(original + b"\n")
                elif name.endswith(".jsonl"):
                    path.write_text('{"requirement_id":"R-new","summary":"New scope","status":"open"}\n', encoding="utf-8")
                else:
                    path.write_bytes(original + b"\nChanged evidence or requirement.\n")
                self.assertFalse(evaluate_delivery(self.root)["ok"])
                self.assertEqual(w.status(self.workspace, "case")["progress"]["status"], "stale")
                self.assertEqual((self.root/"state/final_checklist.json").read_bytes(), receipt)
                self.assertEqual((self.root/"state/progress.json").read_bytes(), progress)
            path.write_bytes(original)
        self.assertTrue(evaluate_delivery(self.root)["ok"])

    def test_lite_optional_evidence_files_are_located_and_bound(self):
        self.task("lite")
        items = {k: {"passed": True, "evidence": "Synthetic control: final.md and source.md."} for k in CHECKLIST}
        w.save_text(self.root, "checks/length.txt", "Report length checked against the brief.")
        items["requirements"]["evidence_files"] = ["checks/length.txt"]
        self.assertTrue(w.finish(self.workspace, "case", "Complete.", checklist=items)["completed"])
        w.save_text(self.root, "checks/length.txt", "Changed measurement.")
        self.assertFalse(evaluate_delivery(self.root)["ok"])
        self.assertTrue(w.finish(self.workspace, "case", "Complete.", checklist=items)["completed"])
        for targets in (["missing.txt"], ["../outside.txt"], [str(self.root/"source.md")],
                        ["state/progress.json"], "checks/length.txt", []):
            with self.subTest(targets=targets):
                items["requirements"]["evidence_files"] = targets
                before = (self.root/"state/final_checklist.json").read_bytes()
                self.assertFalse(w.finish(self.workspace, "case", "Complete.", checklist=items)["completed"])
                self.assertEqual((self.root/"state/final_checklist.json").read_bytes(), before)

    def test_lite_binding_preserves_locator_only_sources_and_legacy_receipts(self):
        self.task("lite")
        items = {k: {"passed": True, "evidence": "Synthetic control: final.md and source S1, page 2."} for k in CHECKLIST}
        path = self.root/"data/source_registry.csv"
        text = path.read_text(encoding="utf-8").replace("source.md", "p. 2")
        path.write_text(text, encoding="utf-8")
        (self.root/"state/requirements.jsonl").unlink()
        self.assertTrue(w.finish(self.workspace, "case", "Complete.", checklist=items)["completed"])
        record = w.load(self.root, "state/final_checklist.json")
        self.assertNotIn("source.md", record["input_hashes"])
        self.assertIsNone(record["input_hashes"]["state/requirements.jsonl"])
        w.save_text(self.root, "state/requirements.jsonl", "")
        self.assertFalse(evaluate_delivery(self.root)["ok"])
        (self.root/"state/requirements.jsonl").unlink()
        record.pop("schema_version")
        record.pop("input_hashes")
        w.save(self.root, "state/final_checklist.json", record)
        w.save_text(self.root, "state/task_spec.md", "Changed since legacy receipt.")
        result = evaluate_delivery(self.root)
        self.assertTrue(result["ok"])
        self.assertEqual(result["input_binding_scope"], "report_and_message_only")
        self.assertFalse(result["semantic_verification"])

    def test_lite_binds_binary_original_and_explicit_source_text_with_shared_hash_rules(self):
        self.task("lite")
        items = {k: {"passed": True, "evidence": "Synthetic control: final.md and source.md."} for k in CHECKLIST}
        original = self.root/"original.pdf"
        original.write_bytes(b"%PDF synthetic binary control\xff\r\n")
        registry = self.root/"data/source_registry.csv"
        with registry.open(encoding="utf-8", newline="") as file:
            rows = list(csv.DictReader(file))
        rows[0].update(url="original.pdf", evidence_path="source.md")
        with registry.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
        self.assertTrue(w.finish(self.workspace, "case", "Complete.", checklist=items)["completed"])
        record = w.load(self.root, "state/final_checklist.json")
        self.assertEqual(record["input_hashes"]["original.pdf"], w.sha256_file(original))
        source = self.root/"source.md"
        source.write_bytes(source.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
        self.assertTrue(evaluate_delivery(self.root)["ok"])
        original.write_bytes(original.read_bytes().replace(b"\r\n", b"\n"))
        self.assertFalse(evaluate_delivery(self.root)["ok"])

    def test_lite_plural_paragraph_and_section_locators_bind_the_source(self):
        self.task("lite")
        items = {k: {"passed": True, "evidence": "Synthetic control: final.md and source.md."} for k in CHECKLIST}
        path = self.root/"data/source_registry.csv"
        original = path.read_text(encoding="utf-8")
        for locator in ("source.md paragraphs 1-2", "source.md sections 1-2"):
            with self.subTest(locator=locator):
                path.write_text(original.replace("source.md", locator), encoding="utf-8")
                self.assertTrue(w.finish(self.workspace, "case", "Complete.", checklist=items)["completed"])
                self.assertIn("source.md", w.load(self.root, "state/final_checklist.json")["input_hashes"])
        (self.root/"source.md").unlink()
        self.assertFalse(evaluate_delivery(self.root)["ok"])

    def test_full_without_cli_performs_degraded_self_review_and_delivery(self):
        with patch("review_runner.shutil.which", side_effect=AssertionError("no CLI probe for self")):
            started = self.task()
            prompt = w.review(self.workspace, "case", ["source.md"])
        self.assertEqual(started["review_readiness"]["status"], "self_available")
        self.assertEqual(prompt["action_required"], "self_review")
        self.assertEqual(w.rows_for(self.root), [])
        reviewed = w.review(self.workspace, "case", ["source.md"], self_review=self.self_result(prompt))
        self.assertTrue(reviewed["reviews_complete"], reviewed)
        self.assertEqual(reviewed["review_strength"], "degraded")
        record = next(r for r in w.rows_for(self.root) if r.get("record_type") == "model_review")
        self.assertEqual(record["reviewer"], "self")
        self.assertEqual(record["execution_id"], "author:case")
        done = w.finish(self.workspace, "case", "The report is complete; it has a self-review only.")
        self.assertTrue(done["completed"], done)
        receipt = (self.root/"state/final_delivery.json").read_bytes()
        self.assertEqual(json.loads(receipt)["review_strength"], "degraded")
        self.assertTrue(w.review(self.workspace, "case", ["source.md"])["reused"])
        self.assertEqual(receipt, (self.root/"state/final_delivery.json").read_bytes())

    def test_negative_self_review_is_preserved_and_blocks_delivery(self):
        self.task(); prompt = w.review(self.workspace, "case", ["source.md"], reviewer="self")
        result = w.review(self.workspace, "case", ["source.md"], reviewer="self", self_review=self.self_result(prompt, True))
        self.assertTrue(result["reviews_complete"])
        self.assertFalse(result["completion_check"]["ok"])
        self.assertFalse(w.finish(self.workspace, "case", "Complete.")["completed"])
        before = w.rows_for(self.root)
        self.assertTrue(w.review(self.workspace, "case", ["source.md"])["reused"])
        self.assertEqual(before, w.rows_for(self.root))

    def test_stale_self_review_and_explicit_independent_without_backend_fail(self):
        self.task()
        for tier in ("external", "independent"):
            with self.assertRaisesRegex(ValueError, "backend"):
                w.review(self.workspace, "case", ["source.md"], reviewer=tier)
        with self.assertRaises(ValueError):
            w.review(self.workspace, "case", ["source.md"], reviewer="self", purpose="evaluation")
        prompt = w.review(self.workspace, "case", ["source.md"])
        w.save_text(self.root, "source.md", "Now the source reports thirteen shipments.")
        with self.assertRaisesRegex(ValueError, "input_version"):
            w.review(self.workspace, "case", ["source.md"], self_review=self.self_result(prompt))

    def test_self_record_cannot_be_relabelled_independent(self):
        self.task(); prompt = w.review(self.workspace, "case", ["source.md"])
        w.review(self.workspace, "case", ["source.md"], self_review=self.self_result(prompt))
        progress = w.load(self.root, "state/progress.json")
        progress["review_plan"].pop("reviewer")
        w.save(self.root, "state/progress.json", progress)
        self.assertFalse(w.completion(self.root, progress, "final.md")["ok"])

    def test_generic_http_runs_an_external_review_with_complete_evidence(self):
        self.task()
        received = []
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args): pass
            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                received.append((self.path, body))
                assignment = json.loads(body["messages"][1]["content"])
                result = SyntheticRunner()({}, assignment, None)
                raw = json.dumps({"id": "synthetic-http-1", "choices": [{"finish_reason": "stop", "message": {"content": result["content"]}}]}).encode()
                self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(raw)
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
        try:
            config = {"reviewers": [{"id": "http", "backend": "generic", "model": "synthetic", "base_url": f"http://127.0.0.1:{server.server_port}/v1"}]}
            result = w.review(self.workspace, "case", ["source.md"], reviewer="external", config=config)
            self.assertTrue(result["reviews_complete"], result)
            self.assertTrue(w.finish(self.workspace, "case", "The report is complete.")["completed"])
            self.assertEqual(received[0][0], "/v1/chat/completions")
            assignment = json.loads(received[0][1]["messages"][1]["content"])["assignment"]
            self.assertIn("twelve shipments", assignment["report"])
            self.assertIn("source.md", assignment["sources"])
        finally:
            server.shutdown(); server.server_close(); thread.join(timeout=3)


class BackendTests(unittest.TestCase):
    def test_generic_requires_https_except_explicit_loopback(self):
        for url in ("https://review.example/v1", "http://localhost:8000/v1",
                    "http://127.0.0.1:8000/v1", "http://[::1]:8000/v1"):
            with self.subTest(allowed=url):
                self.assertTrue(r.endpoint_url({"base_url": url}).endswith("/chat/completions"))
        for url in ("http://review.example/v1", "http://10.0.0.1/v1",
                    "http://localhost.example/v1", "http://127.0.0.1.example/v1",
                    "http://2130706433/v1", "http://[::]/v1"):
            with self.subTest(rejected=url), patch.object(r.http, "build_opener") as opener:
                with self.assertRaisesRegex(ValueError, "HTTPS"):
                    r.run_generic({"model": "synthetic", "base_url": url}, {"report": "synthetic"})
                opener.assert_not_called()

    def test_dsh_smoke_child_inherits_only_runtime_environment(self):
        from run_dsh_evals import scrub_smoke_environment
        secret_names = ("GITHUB_TOKEN", "AWS_SECRET_ACCESS_KEY", "SERVICE_PASSWORD",
                        "SERVICE_API_KEY", "NPM_TOKEN", "NODE_OPTIONS", "PYTHONPATH")
        host = {key: os.environ[key] for key in ("PATH", "SYSTEMROOT", "WINDIR", "TEMP", "TMP") if key in os.environ}
        host.update({name: "synthetic-secret" for name in secret_names})
        host["LANG"] = "C.UTF-8"
        with patch.dict(os.environ, host, clear=True):
            env = scrub_smoke_environment(Path("synthetic-dsh-home"), "http://127.0.0.1:8000")
        child = subprocess.run([sys.executable, "-I", "-c",
            "import json,os;print(json.dumps(dict(os.environ)))"], env=env,
            check=True, capture_output=True, text=True)
        inherited = json.loads(child.stdout)
        for name in secret_names:
            self.assertFalse(name in inherited, f"Smoke child inherited {name}")
        self.assertEqual(inherited["DEEPSEEK_API_KEY"], "dsh-smoke-local-placeholder")
        self.assertEqual(inherited["DEEPSEEK_BASE_URL"], "http://127.0.0.1:8000")
        self.assertEqual(inherited["LANG"], "C.UTF-8")
        if "PATH" in host:
            self.assertEqual(inherited["PATH"], host["PATH"])

    def test_claude_adapter_uses_fresh_tool_free_session_and_keeps_response(self):
        result = SimpleNamespace(returncode=0, stdout=json.dumps({"subtype": "success", "is_error": False,
            "session_id": "claude-session", "result": '{"report_verdict":"needs_revision"}'}), stderr="")
        with patch.object(r.shutil, "which", return_value="claude"), patch.object(r, "run_bounded", return_value=result) as run:
            response = r.run_reviewer({"backend": "claude", "model": "claude-configured"}, {"report": "evidence"}, Path.cwd())
        self.assertEqual(response["execution_id"], "claude-session")
        argv = run.call_args.args[0]
        self.assertIn("--no-session-persistence", argv)
        self.assertEqual(argv[argv.index("--tools")+1], "")
        self.assertNotIn("--continue", argv)

    def test_generic_rejects_truncated_or_anonymous_responses_and_redacts_http_errors(self):
        config = {"backend": "generic", "model": "synthetic", "base_url": "https://example.org/v1"}
        for envelope in ({"choices":[None]}, {"id":"x", "choices":[{"finish_reason":"length", "message":{"content":"{}"}}]},
                         {"choices":[{"finish_reason":"stop", "message":{"content":"{}"}}]}):
            with patch.object(r.http, "build_opener") as opener:
                stream = opener.return_value.open.return_value.__enter__.return_value
                stream.read.return_value = json.dumps(envelope).encode()
                stream.headers.get.return_value = None
                with self.assertRaises(r.ReviewFailure): r.run_generic(config, {})
        with patch.object(r.http, "build_opener") as opener:
            opener.return_value.open.side_effect = r.error.HTTPError("https://example.org", 401, "secret", {}, None)
            with self.assertRaises(r.ReviewFailure) as failure: r.run_generic(config, {})
            self.assertNotIn("secret", str(failure.exception)+json.dumps(failure.exception.capture))

    def test_invalid_config_does_not_fall_back_to_self(self):
        with patch.dict(os.environ, {"RESEARCH_TOOLKIT_REVIEW_CONFIG": "", "RESEARCH_TOOLKIT_REVIEW_BACKEND": "unknown"}):
            self.assertEqual(r.review_readiness()["status"], "blocked")


if __name__ == "__main__":
    unittest.main()
