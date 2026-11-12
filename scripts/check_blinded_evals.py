#!/usr/bin/env python3
"""Offline shared transport and archived-evidence controls; no research execution."""
from __future__ import annotations
import copy
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch
import run_blinded_evals as h
from reproduce_calibration import reproduce


class PilotTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=os.environ.get("IRF_TEST_TMPDIR"))
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.config = copy.deepcopy(h.read(h.ROOT / "evals/templates/blinded-study.json"))
        self.config["publication_rights_confirmed"] = True
        self.config["selection_statement"] = "Synthetic protocol controls, not study tasks"
        self.config["exposure_statement"] = "All authored for software checks"
        self.config["author"]["model"] = "synthetic-author"
        self.config["judge"]["model"] = "synthetic-judge"

    def test_http_transport_budget_and_truncation(self):
        reply = {"id": "synthetic-request", "model": "synthetic-author", "usage": {"total_tokens": 40, "completion_tokens": 15}, "choices": [{"finish_reason": "stop", "message": {"content": '{"report":"Example","notes":"Control"}'}}]}
        captured = []
        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                captured.append(json.loads(self.rfile.read(int(self.headers["Content-Length"]))))
                payload = json.dumps(reply).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)
            def log_message(self, *args):
                pass
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            settings = {**self.config["author"], "base_url": f"http://127.0.0.1:{server.server_port}/v1"}
            with patch.dict(os.environ, {settings["api_key_env"]: "synthetic-test-secret"}):
                self.assertIsNotNone(h.request(settings, [], self.base / "http-ok"))
                reply["usage"]["total_tokens"] = settings["max_total_tokens"] + 1
                self.assertIsNone(h.request(settings, [], self.base / "http-budget"))
                reply["usage"]["total_tokens"] = 40
                reply["choices"][0]["finish_reason"] = "length"
                self.assertIsNone(h.request(settings, [], self.base / "http-truncated"))
            self.assertNotIn("synthetic-test-secret", (self.base / "http-ok/request.json").read_text())
            self.assertEqual(captured[0]["max_tokens"], settings["max_completion_tokens"])
            self.assertTrue((self.base / "http-budget/response.json").exists())
            self.assertEqual(h.read(self.base / "http-budget/execution.json")["failure_kind"], "token_budget")
            truncated = h.read(self.base / "http-truncated/execution.json")
            self.assertEqual(truncated["failure_kind"], "truncated")
            self.assertEqual(truncated["finish_reason"], "length")
        finally:
            server.shutdown()
            server.server_close()
            worker.join()

    def test_public_inventory_and_no_overwrite(self):
        out = self.base / "inventory"
        result = reproduce(out)
        self.assertEqual(result["n"], 2)
        self.assertEqual(result["research_quality_status"], "not_evaluated")
        with self.assertRaises(FileExistsError):
            reproduce(out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
