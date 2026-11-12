#!/usr/bin/env python3
"""Historical receipt compatibility and current reviewer-adapter controls."""
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
from check_research_workflow import BRIEF, SyntheticRunner, historical_contract, legacy_review, legacy_finish


class HistoricalReceiptTests(unittest.TestCase):
    """Version-1 receipt compatibility controls; new tasks use the independent v2 path."""
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=os.environ.get("IRF_TEST_TMPDIR"))
        self.addCleanup(self.tmp.cleanup)
        self.workspace = Path(self.tmp.name)
        self.env = patch.dict(os.environ, {"RESEARCH_TOOLKIT_REVIEW_CONFIG": "", "RESEARCH_TOOLKIT_REVIEW_BACKEND": ""})
        self.env.start()
        self.addCleanup(self.env.stop)

    def task(self):
        started = w.start(self.workspace, "case", BRIEF)
        self.root = self.workspace/"case"
        w.save_text(self.root, "final.md", "The source reports twelve shipments.\n\nRevenue is not reported.\n")
        w.save_text(self.root, "source.md", "Company A reports twelve shipments; revenue is unknown.")
        w.save_text(self.root, "data/source_registry.csv", "source_id,title,url,source_type,read_scope,read_evidence\nS1,Shipments,https://example.org,primary,full_text,source.md\n")
        w.save_text(self.root, "data/claims_registry.csv", "claim_id,claim,claim_type,supporting_sources\nC1,Twelve shipments,verified_fact,S1\n")
        w.status(self.workspace, "case", stage="draft")
        historical_contract(self.workspace, "case")
        return started

    def self_result(self, prompt, negative=False):
        result = SyntheticRunner(negative=negative)({}, {"role": "reviewer"}, None)
        return {**json.loads(result["content"]), "input_version": prompt["input_version"]}


    def length_requirement(self, **changes):
        row = {"requirement_id": "R-length", "summary": "Count the whole report using the declared unit and bounds.",
               "status": "satisfied", "evidence": "final.md",
               "length_constraint": {"unit": "whitespace_words", "scope": "whole_artifact", "min": 1, "max": 200}}
        row.update(changes)
        w.save_text(self.root, "state/requirements.jsonl", json.dumps(row)+"\n")
        return row

    def test_length_measurements_bind_receipt_and_survive_checkout_newlines(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.workspace = Path(tmp)
            self.task()
            self.length_requirement()
            args = {}
            prompt = legacy_review(self.workspace, "case", ["source.md"], reviewer="self")
            legacy_review(self.workspace, "case", ["source.md"], reviewer="self", self_review=self.self_result(prompt))
            result = legacy_finish(self.workspace, "case", "The report is complete.", **args)
            self.assertTrue(result["completed"], result)
            self.assertEqual(result["delivery_check"]["length_checks"][0]["actual"], 9)
            name = "state/final_delivery.json"
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
        self.task()
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
        self.task()
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
        self.task()
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
        self.task()
        self.length_requirement()
        prompt = legacy_review(self.workspace, "case", ["source.md"], reviewer="self")
        legacy_review(self.workspace, "case", ["source.md"], reviewer="self", self_review=self.self_result(prompt))
        self.assertTrue(legacy_finish(self.workspace, "case", "Original delivery.")["completed"])
        before = {name: (self.root/name).read_bytes() for name in
                  ("state/final_delivery.json", "state/progress.json", "delivery_message.md")}
        self.length_requirement(length_constraint={"unit": "whitespace_words", "scope": "whole_artifact", "min": 100})
        result = legacy_finish(self.workspace, "case", "Replacement delivery.")
        self.assertFalse(result["completed"])
        self.assertEqual(before, {name: (self.root/name).read_bytes() for name in before})

    def test_existing_requirements_without_length_are_not_inferred(self):
        self.task()
        w.save_text(self.root, "state/requirements.jsonl", json.dumps({
            "requirement_id": "R-old", "summary": "100 words", "status": "satisfied", "evidence": "final.md"})+"\n")
        self.assertEqual(w.inspect_length_constraints(self.root, "final.md"), ([], []))

    def test_status_checks_recorded_delivery_without_rewriting_state(self):
        for mutation in ("report", "claims", "receipt"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as tmp:
                workspace = Path(tmp)
                saved_workspace = self.workspace
                self.workspace = workspace
                try:
                    self.task()
                    args = {}
                    prompt = legacy_review(workspace, "case", ["source.md"], reviewer="self")
                    legacy_review(workspace, "case", ["source.md"], reviewer="self", self_review=self.self_result(prompt))
                    self.assertTrue(legacy_finish(workspace, "case", "Complete without independent review.", **args)["completed"])
                    self.assertEqual(w.status(workspace, "case")["progress"]["status"], "complete")
                    before = (self.root/"state/progress.json").read_bytes()
                    if mutation == "report":
                        w.save_text(self.root, "final.md", "Changed after delivery.")
                    elif mutation == "claims":
                        (self.root/"data/claims_registry.csv").unlink()
                    else:
                        name = "final_delivery.json"
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
        prompt = legacy_review(self.workspace, "case", ["source.md"], reviewer="self")
        negative = legacy_review(self.workspace, "case", ["source.md"], reviewer="self", self_review=self.self_result(prompt, True))
        for result in (negative, legacy_review(self.workspace, "case", ["source.md"], reviewer="self")):
            self.assertTrue(result["reviews_complete"])
            self.assertEqual(result["review_check"]["completed_slots"], 1)
            self.assertFalse(result["delivery_ready"])
            self.assertIn("shipments, not revenue", " ".join(result["open_issues"]))
        progress = w.status(self.workspace, "case")["progress"]
        self.assertEqual(progress["open_issues"], negative["open_issues"])
        self.assertIn("F1", progress["next_action"])

    def test_cli_template_native_assignment_and_pending_delivery(self):
        def call(action, arguments, expected_exit=0):
            result = subprocess.run([sys.executable, "-X", "utf8", str(w.TOOLKIT/"scripts/research_workflow.py"),
                action, "--workspace", str(self.workspace)], input=json.dumps(arguments),
                text=True, encoding="utf-8", capture_output=True)
            self.assertEqual(result.returncode, expected_exit, result.stdout+result.stderr)
            return json.loads(result.stdout)
        task = "template-cli"
        call("start", {"task": task, "brief": BRIEF})
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
        call("save", {"task": task, "draft": {"path": "final.md", "main": True,
                     "host_task": "synthetic-template-author", "complete": True}})
        args = {"task": task, "evidence_paths": ["sources/S1.md"], "include_assignment": False}
        pending = call("review", args)
        self.assertEqual(pending["action_required"], "host_agents")
        self.assertEqual(len(pending["assignments"]), 8)
        self.assertFalse(call("finish", {"task": task, "message": "Complete."}, expected_exit=1)["completed"])
        self.assertEqual(call("status", {"task": task})["progress"]["review_contract"], 2)
        original_refs = [item["assignment_ref"] for item in pending["assignments"]]
        repeated = call("review", args)
        self.assertEqual(original_refs, [item["assignment_ref"] for item in repeated["assignments"]])
        self.assertEqual(w.rows_for(root), [])


    def test_shared_guidance_keeps_its_existing_methods_and_default(self):
        for language in ("en", "zh"):
            for stage, names in w.STAGE_FILES.items():
                with self.subTest(language=language, stage=stage):
                    selected = {**w.STAGE_FILES,
                        "analyze": ["references/research-standard.md"],
                        "final": ["references/quality-gates.md"]}[stage]
                    expected = [name.replace(".md", ".zh-CN.md") if language == "zh" else name
                                for name in selected]
                    result = w.guidance(stage, language)
                    self.assertNotIn("profile", result)
                    self.assertEqual([item["path"] for item in result["guidance"]], expected)


    def test_invalid_local_source_has_draft_error_and_invalidates_delivery(self):
        self.task()
        prompt = legacy_review(self.workspace, "case", ["source.md"], reviewer="self")
        legacy_review(self.workspace, "case", ["source.md"], reviewer="self", self_review=self.self_result(prompt))
        self.assertTrue(legacy_finish(self.workspace, "case", "Complete.")["completed"])
        original = w.registry_rows(self.root, "data/source_registry.csv", ("source_id",))[0]
        w.save_records(self.workspace, "case", sources=[{
            "source_id": "S1", "url": "C:/reports/old.md"}])
        draft = w.check_draft(self.workspace, "case")
        self.assertFalse(draft["ok"], draft)
        error = draft["errors"][0]
        self.assertIn("row S1, url:", error)
        self.assertIn("task-relative", error)
        self.assertIn("sources/S1.md", error)
        self.assertFalse(legacy_finish(self.workspace, "case", "Complete.")["completed"])
        delivery = evaluate_delivery(self.root)
        self.assertFalse(delivery["ok"])
        self.assertIn("data/source_registry.csv", " ".join(delivery["findings"]))
        for url in ("source.md", original["url"]):
            with self.subTest(url=url):
                w.save_records(self.workspace, "case", sources=[{"source_id": "S1", "url": url}])
                self.assertTrue(w.check_draft(self.workspace, "case")["ok"])
                prompt = legacy_review(self.workspace, "case", ["source.md"], reviewer="self", revision=True)
                legacy_review(self.workspace, "case", ["source.md"], reviewer="self", self_review=self.self_result(prompt))
                self.assertTrue(legacy_finish(self.workspace, "case", "Complete.")["completed"])

    def test_full_without_cli_uses_native_independent_assignments(self):
        with patch("review_runner.shutil.which", side_effect=AssertionError("native agents need no CLI probe")):
            started = self.task()
            w.save_records(self.workspace, "case", draft={"path": "final.md", "main": True,
                           "host_task": "synthetic-native-author", "complete": True})
            pending = w.review(self.workspace, "case", ["source.md"])
        self.assertEqual(started["review_readiness"]["status"], "host_native")
        self.assertEqual(pending["action_required"], "host_agents")
        self.assertEqual(len(pending["assignments"]), 8)
        self.assertEqual(w.rows_for(self.root), [])
        with self.assertRaisesRegex(ValueError, "self-review"):
            w.review(self.workspace, "case", ["source.md"], reviewer="self")
        self.assertFalse(w.finish(self.workspace, "case", "The report is complete.")["completed"])

    def test_negative_self_review_is_preserved_and_blocks_delivery(self):
        self.task(); prompt = legacy_review(self.workspace, "case", ["source.md"], reviewer="self")
        result = legacy_review(self.workspace, "case", ["source.md"], reviewer="self", self_review=self.self_result(prompt, True))
        self.assertTrue(result["reviews_complete"])
        self.assertFalse(result["completion_check"]["ok"])
        self.assertFalse(legacy_finish(self.workspace, "case", "Complete.")["completed"])
        before = w.rows_for(self.root)
        self.assertTrue(legacy_review(self.workspace, "case", ["source.md"])["reused"])
        self.assertEqual(before, w.rows_for(self.root))

    def test_stale_self_review_and_explicit_independent_without_backend_fail(self):
        self.task()
        for tier in ("external", "independent"):
            with self.assertRaisesRegex(ValueError, "backend"):
                legacy_review(self.workspace, "case", ["source.md"], reviewer=tier)
        with self.assertRaises(ValueError):
            legacy_review(self.workspace, "case", ["source.md"], reviewer="self", purpose="evaluation")
        prompt = legacy_review(self.workspace, "case", ["source.md"])
        w.save_text(self.root, "source.md", "Now the source reports thirteen shipments.")
        with self.assertRaisesRegex(ValueError, "input_version"):
            legacy_review(self.workspace, "case", ["source.md"], self_review=self.self_result(prompt))

    def test_self_record_cannot_be_relabelled_independent(self):
        self.task(); prompt = legacy_review(self.workspace, "case", ["source.md"])
        legacy_review(self.workspace, "case", ["source.md"], self_review=self.self_result(prompt))
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
            result = legacy_review(self.workspace, "case", ["source.md"], reviewer="external", config=config)
            self.assertTrue(result["reviews_complete"], result)
            self.assertTrue(legacy_finish(self.workspace, "case", "The report is complete.")["completed"])
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
    os.environ["RESEARCH_TOOLKIT_TELEMETRY"] = "off"
    unittest.main()
