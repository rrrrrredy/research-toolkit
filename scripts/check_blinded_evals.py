#!/usr/bin/env python3
"""Offline controls for study randomization, masking and failure preservation; no real model calls."""
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
        for i in range(5):
            (self.base / f"brief-{i}.md").write_text(f"Synthetic task {i}: explain the supplied count.", encoding="utf-8")
            (self.base / f"source-{i}.md").write_text(f"Fictional source reports {i} units.", encoding="utf-8")
            self.config["tasks"].append({"task_id": f"task-{i}", "family_id": f"family-{i}", "language": "en", "task_type": "synthetic_control", "brief": f"brief-{i}.md", "sources": [f"source-{i}.md"]})
        self.study = self.base / "study.json"
        self.store()

    def store(self):
        self.study.write_text(json.dumps(self.config), encoding="utf-8")

    def plan(self, name="run", seed=42):
        output = self.base / name
        return output, h.prepare(self.study, output, seed)

    def judgment(self):
        item = {"score": 3, "reason": "Synthetic protocol control", "excerpt": "Paragraph 1: fictional observation", "source_evidence": "S1: fictional count"}
        return {"preference": "tie", "reason": "Synthetic equal reports", "condition_clues": "none observed", "reports": {label: {d: item for d in h.DIMENSIONS} for label in ("A", "B")}}

    def fake(self, settings, messages, folder):
        value = self.judgment() if settings["model"] == "synthetic-judge" else {"report": "Fictional observation; not a real report.", "notes": "Synthetic testing only"}
        h.save(folder / "request.json", {"messages": messages})
        h.save(folder / "response.json", value)
        h.save(folder / "execution.json", {"status": "synthetic_control"})
        return json.dumps(value)

    def test_seed_balance_and_pending_results(self):
        out, a = self.plan()
        _, b = self.plan("same")
        _, c = self.plan("different", 314159)
        self.assertEqual(a["assignments"], b["assignments"])
        self.assertNotEqual(a["assignments"], c["assignments"])
        count = sum(t["run_order"][0] == "with_toolkit" for t in a["assignments"])
        self.assertIn(count, (2, 3))
        self.assertEqual(sum(line.startswith("| pair-") for line in (out / "results.md").read_text().splitlines()), 0)
        self.assertFalse((out / "results.json").exists())

    def test_rejects_invalid_cohort_and_escaping_sources(self):
        self.config["tasks"][1]["family_id"] = "family-0"
        self.store()
        with self.assertRaisesRegex(ValueError, "independent families"):
            self.plan()
        self.config["tasks"][1]["family_id"] = "family-1"
        self.config["tasks"][0]["sources"] = ["../outside.md"]
        self.store()
        with self.assertRaisesRegex(ValueError, "escapes"):
            self.plan()

    def test_template_requires_real_admission(self):
        with self.assertRaises(ValueError):
            h.prepare(h.ROOT / "evals/templates/blinded-study.json", self.base / "template", 1)
        self.assertFalse((self.base / "template").exists())

    def test_masking_lock_and_all_raw_outputs(self):
        out, frozen = self.plan()
        observed = []
        def call(settings, messages, folder):
            observed.append((settings["model"], messages, folder))
            return self.fake(settings, messages, folder)
        rows = h.run(out, call)
        self.assertEqual(len(observed), 15)
        self.assertEqual([r["outcome"] for r in rows], ["tie"] * 5)
        authors = [v for v in observed if v[0] == "synthetic-author"]
        self.assertEqual([v[2].name for v in authors], [c for t in frozen["assignments"] for c in t["run_order"]])
        for _, messages, _ in observed[10:]:
            packet = json.loads(messages[1]["content"])
            self.assertEqual(set(packet), {"brief", "sources", "rubric", "reports"})
            self.assertEqual(set(packet["reports"]), {"A", "B"})
            for term in ("with_toolkit", "without_toolkit", '"seed"', '"run_order"', '"notes"'):
                self.assertNotIn(term, messages[1]["content"])
        self.assertTrue((out / "judgments.lock.json").is_file())
        manifest = h.read(out / "bundle-manifest.json")["sha256"]
        self.assertEqual(len(list(out.rglob("response.json"))), 15)
        for name, digest in manifest.items():
            self.assertEqual(h.sha((out / name).read_bytes()), digest)
        with self.assertRaisesRegex(ValueError, "already started"):
            h.run(out, self.fake)

    def test_failure_is_not_a_win_and_no_retry(self):
        out, _ = self.plan()
        calls = []
        def call(settings, messages, folder):
            calls.append(folder)
            if len(calls) == 1:
                h.save(folder / "execution.json", {"status": "synthetic_failure"})
                return None
            return self.fake(settings, messages, folder)
        rows = h.run(out, call)
        self.assertEqual(len(calls), 14)
        self.assertEqual(rows[0]["status"], "unresolved_author_failure")
        self.assertEqual(rows[0]["outcome"], "unresolved")
        self.assertEqual(len(rows), 5)

    def test_mutated_freeze_and_invalid_judgment(self):
        out, frozen = self.plan()
        frozen["seed"] += 1
        (out / "coordinator/frozen.json").write_text(json.dumps(frozen), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "changed"):
            h.run(out, self.fake)
        for score in (5, True, -1):
            value = copy.deepcopy(self.judgment())
            value["reports"]["A"]["task_fidelity"]["score"] = score
            with self.assertRaises(ValueError):
                h.validate_judgment(value)

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
