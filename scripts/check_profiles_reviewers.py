#!/usr/bin/env python3
"""Offline behavioral controls for profiles and reviewer backends; no paid model calls."""
from __future__ import annotations
import copy
import json
import os
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
        for envelope in ({"id":"x", "choices":[{"finish_reason":"length", "message":{"content":"{}"}}]},
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
