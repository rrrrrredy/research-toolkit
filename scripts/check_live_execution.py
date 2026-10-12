#!/usr/bin/env python3
"""Offline native-judge isolation and first-attempt retention controls."""
import copy
import json
import os
from pathlib import Path
import subprocess
import shutil
import tempfile
import unittest
from unittest.mock import patch

import codex_judge as c
import run_blinded_evals as h
import run_judge_calibration as calibration
import check_live_diagnostics as diagnostics
from check_blinded_protocol_v2 import ProtocolV2Tests


def settings():
    return {"transport": "codex_exec", "model": "gpt-6-astra", "snapshot_statement": "Requested alias; CLI does not attest returned identity",
            "executable_env": "RESEARCH_CODEX_EXECUTABLE", "reasoning_effort": "low", "max_completion_tokens": 4096,
            "max_total_tokens": 30000, "timeout_seconds": 120, "output_protocol": "json_object_v1", "allow_json_fence": False}


def events(text='{"value":1}', usage=None, extra=()):
    values = [{"type": "thread.started", "thread_id": "synthetic"}, *extra,
              {"type": "item.completed", "item": {"type": "agent_message", "text": text}},
              {"type": "turn.completed", "usage": usage or {"input_tokens": 100, "output_tokens": 20}}]
    return ("\n".join(json.dumps(row) for row in values) + "\n").encode()


class NativeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.executable = self.base / "codex-control.exe"
        self.executable.write_bytes(b"offline test fixture")
        self.settings = settings()
        self.messages = [{"role": "system", "content": "FROZEN_SYSTEM"}, {"role": "user", "content": "PUBLIC_PACKET_ONLY"}]

    def invoke(self, runner, name="run"):
        with patch.dict(os.environ, {"RESEARCH_CODEX_EXECUTABLE": str(self.executable), "AUTHOR_API_KEY": "PRIVATE_SENTINEL", "CODEX_THREAD_ID": "PARENT_CONTEXT"}):
            return c.request(self.settings, self.messages, self.base / name, runner)

    def test_native_context_and_credentials_are_isolated(self):
        observed = []
        def runner(args, **kwargs):
            observed.append(args)
            self.assertEqual(kwargs["input"], b"PUBLIC_PACKET_ONLY")
            self.assertNotIn("AUTHOR_API_KEY", kwargs["env"])
            self.assertNotIn("CODEX_THREAD_ID", kwargs["env"])
            self.assertNotIn("resume", args)
            self.assertIn("--ignore-user-config", args)
            self.assertIn("--ephemeral", args)
            self.assertEqual(args[args.index("--sandbox") + 1], "read-only")
            config = dict(value.split("=", 1) for index, value in enumerate(args) if index and args[index - 1] == "-c")
            self.assertEqual(config["model_providers.research_eval.request_max_retries"], "0")
            self.assertEqual(config["model_providers.research_eval.stream_max_retries"], "0")
            self.assertNotIn("model_providers.openai.request_max_retries", config)
            work = Path(args[args.index("--cd") + 1])
            self.assertEqual([p.name for p in work.iterdir()], ["instructions.txt"])
            self.assertEqual((work / "instructions.txt").read_text(), "FROZEN_SYSTEM")
            for feature in c.DISABLED:
                self.assertIn(["--disable", feature], [args[i:i+2] for i in range(len(args)-1)])
            return subprocess.CompletedProcess(args, 0, events(), b"")
        self.assertEqual(self.invoke(runner), '{"value":1}')
        self.assertEqual(len(observed), 1)
        record = h.read(self.base / "run/execution.json")
        self.assertIsNone(record["model_returned"])
        self.assertFalse(record["hard_token_cap"])
        self.assertNotIn(str(self.executable), (self.base / "run/command.json").read_text())

    def test_tool_activity_failures_ambiguity_and_bad_usage_rejected(self):
        bad = [events(extra=[{"type": "item.started", "item": {"type": "command_execution"}}]),
               events(extra=[{"type": "turn.failed"}]),
               events(extra=[{"type": "item.completed", "item": {"type": "agent_message", "text": "extra"}}]),
               events(usage={"input_tokens": 2, "output_tokens": 5000}),
               events(usage={"input_tokens": True, "output_tokens": 5}), b'not-json']
        for raw in bad:
            with self.assertRaises((ValueError, TypeError)):
                c.extract(raw, self.settings)

    def test_deadline_retains_partial_events_without_retry(self):
        calls = []
        def runner(args, **kwargs):
            calls.append(args)
            raise subprocess.TimeoutExpired(args, 120, output=b'partial-event', stderr=b'partial-error')
        self.assertIsNone(self.invoke(runner))
        self.assertEqual(len(calls), 1)
        self.assertEqual((self.base / "run/events.jsonl").read_bytes(), b'partial-event')
        self.assertEqual(h.read(self.base / "run/execution.json")["failure_kind"], "timeout")
        with self.assertRaises(FileExistsError):
            self.invoke(runner)
        self.assertEqual(len(calls), 1)

    def test_explicit_warning_is_retained_but_other_errors_fail(self):
        warning = {"type": "item.completed", "item": {"type": "error", "message": "Under-development features enabled: skip_host_skill_discovery. Test notice"}}
        self.assertTrue(c.extract(events(extra=[warning]), self.settings)[2])
        warning["item"]["message"] = "Model unavailable"
        with self.assertRaises(ValueError):
            c.extract(events(extra=[warning]), self.settings)

    def test_failed_exit_raw_bytes_retained(self):
        self.assertIsNone(self.invoke(lambda args, **kwargs: subprocess.CompletedProcess(args, 1, b'raw', b'config failure')))
        self.assertEqual((self.base / "run/stderr.txt").read_bytes(), b'config failure')


class CalibrationExecutionTests(unittest.TestCase):
    def test_all_first_attempts_lock_before_separate_adjudication(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            h.save(base / "settings.json", settings())
            out = base / "run"
            frozen = calibration.prepare(base / "settings.json", out, 20261012)
            calls = []
            def call(config, messages, folder):
                calls.append(messages)
                packet = json.loads(messages[1]["content"])
                self.assertEqual(set(packet), {"brief", "sources", "rubric", "reports"})
                self.assertEqual(messages[0]["content"], h.JUDGE_SYSTEM)
                h.save(folder / "execution.json", {"status": "synthetic_control"})
                if len(calls) == 1:
                    return None
                if len(calls) == 2:
                    return "invalid response"
                item = {"score": 3, "reason": "control", "excerpt": "control", "source_evidence": "control"}
                return json.dumps({"preference": "tie", "reason": "control", "condition_clues": "none", "reports": {label: {d: item for d in h.DIMENSIONS} for label in ("A", "B")}})
            result = calibration.execute(out, call)
            self.assertEqual(len(calls), 12)
            self.assertEqual(result["independent_families"], 4)
            self.assertEqual([r["status"] for r in result["results"][:2]], ["unresolved", "unresolved"])
            self.assertEqual(result["source_adjudication"], "pending")
            self.assertFalse(result["judge_reliability_established"])
            self.assertTrue((out / "judgments.lock.json").exists())
            with self.assertRaises(FileExistsError):
                calibration.execute(out, call)
            with patch.object(calibration, "hashes", return_value={}):
                with self.assertRaisesRegex(ValueError, "code changed"):
                    calibration.execute(out, call)
            frozen["seed"] = 0
            (out / "coordinator/frozen.json").write_text(json.dumps(frozen))
            with self.assertRaisesRegex(ValueError, "Frozen calibration changed"):
                calibration.execute(out, call)


class PublicEvidenceTests(unittest.TestCase):
    def test_read_only_public_verifier_and_derived_tamper(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "calibration"
            shutil.copytree(h.ROOT / "evals/diagnostics/2026-10-12-astra-calibration", root)
            before = {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}
            self.assertEqual(diagnostics.verify_calibration(root)["families"], 4)
            self.assertEqual(before, {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()})
            p = root / "adjudication.json"
            record = h.read(p)
            record["dimension_drift"] = []
            p.write_text(json.dumps(record))
            with self.assertRaisesRegex(ValueError, "artifact changed"):
                diagnostics.verify_calibration(root)
            manifest = h.read(root / "public-manifest.json")
            manifest["sha256"]["adjudication.json"] = diagnostics.digest(p)
            (root / "public-manifest.json").write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, "Derived calibration"):
                diagnostics.verify_calibration(root)

    def test_connectivity_attempts_include_failed_request(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "connectivity"
            shutil.copytree(h.ROOT / "evals/diagnostics/2026-10-12-connectivity", root)
            diagnostics.verify_connectivity(root)
            p = root / "summary.json"
            summary = h.read(p)
            summary["network_generation_requests"] = 5
            p.write_text(json.dumps(summary))
            with self.assertRaisesRegex(ValueError, "accounting mismatch"):
                diagnostics.verify_connectivity(root)


class IntegrationTests(ProtocolV2Tests):
    def test_native_judge_admission_and_adapter_freeze(self):
        self.config["judge"] = settings()
        self.store()
        out, frozen = self.plan()
        self.assertIn("codex_adapter_sha256", frozen)
        frozen["codex_adapter_sha256"] = "0" * 64
        (out / "coordinator/frozen.json").write_text(json.dumps(frozen))
        (out / "coordinator/freeze-commitment.json").write_text(json.dumps({"frozen_sha256": h.sha(h.encode(frozen))}))
        with self.assertRaisesRegex(ValueError, "adapter changed"):
            h.run(out)
        self.assertFalse((out / "run-started.json").exists())
        self.config["author"] = settings()
        self.store()
        with self.assertRaisesRegex(ValueError, "judges only"):
            self.plan("author-rejected")

    def test_explicit_provider_thinking_options_frozen_and_sent(self):
        self.config["author"].update(thinking="enabled", reasoning_effort="low")
        self.store()
        out, frozen = self.plan()
        self.assertEqual(frozen["config"]["author"]["reasoning_effort"], "low")
        with patch.object(h.urllib.request, "build_opener", side_effect=OSError("offline-control")):
            h.request(self.config["author"], [], out / "request-control")
        body = h.read(out / "request-control/request.json")
        self.assertEqual(body["thinking"], {"type": "enabled"})
        self.assertEqual(body["reasoning_effort"], "low")
        self.config["author"]["thinking"] = "disabled"
        self.store()
        with self.assertRaisesRegex(ValueError, "requires enabled"):
            self.plan("invalid-effort")


if __name__ == "__main__":
    unittest.main()
