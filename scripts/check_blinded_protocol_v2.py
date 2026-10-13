#!/usr/bin/env python3
"""Offline controls for explicit parsing, development admission and swapped judgments."""
import copy
import json
import urllib.error
from pathlib import Path
from unittest.mock import patch
import unittest

import run_blinded_evals as h
from check_blinded_evals import PilotTests


class ProtocolV2Tests(PilotTests):
    def setUp(self):
        super().setUp()
        self.config.update(schema_version=2, position_swap=False, max_requests=15, max_retries=0)
        for role in ("author", "judge"):
            self.config[role].update(accepted_model_ids=[self.config[role]["model"]], response_format="text",
                                     output_protocol="json_object_v1", allow_json_fence=True)
        for task in self.config["tasks"]:
            task["design"] = task["task_id"] + "-design.json"
            h.save(self.base / task["design"], {"role": "development", "material_kind": "synthetic",
                   "rationale": "Test protocol isolation", "provenance": "Authored test fixture",
                   "exclusions": "Not an efficacy study", "expected_judgments": ["COORDINATOR_ONLY_ANSWER"],
                   "exposure": ["Authors of the software test have seen all inputs"]})
        self.store()

    def test_explicit_fence_acceptance_and_ambiguous_rejection(self):
        settings = self.config["author"]
        raw = '{"report":"Negative findings remain.","notes":"PRIVATE_NOTES"}'
        value, method = h.parse_output('```json\n' + raw + '\n```', settings, "author")
        self.assertEqual(value["report"], "Negative findings remain.")
        self.assertEqual(method, "single_json_fence")
        for content in ('Here is JSON: ' + raw, '```json\n' + raw + '\n```\nExplanation', raw + raw,
                        '{"report":"one","report":"two","notes":""}'):
            with self.assertRaises(ValueError):
                h.parse_output(content, settings, "author")
        with self.assertRaises(ValueError):
            h.parse_output('```json\n' + raw + '\n```', {**settings, "allow_json_fence": False}, "author")

    def test_markdown_report_is_verbatim_and_separator_is_unambiguous(self):
        settings = {**self.config["author"], "output_protocol": "markdown_notes_v1"}
        report = '# Report\r\n\r\nText with source S1.\r\n'
        raw = report + h.NOTES_MARKER + '\r\nPRIVATE_NOTES'
        value, method = h.parse_output(raw, settings, "author")
        self.assertEqual(value["report"], report)
        self.assertEqual(method, "markdown_notes_v1")
        for content in ('No separator', raw + '\n' + h.NOTES_MARKER, 'Inline ' + h.NOTES_MARKER + ' marker'):
            with self.assertRaises(ValueError):
                h.parse_output(content, settings, "author")

    def test_admission_ceiling_and_exposure_controls(self):
        original = copy.deepcopy(self.config)
        for change in ({"max_requests": 16}, {"max_retries": 1}, {"cohort_status": "held_out"}):
            self.config = {**copy.deepcopy(original), **change}
            self.store()
            with self.assertRaises(ValueError):
                self.plan()
        self.config = original
        design_path = self.base / self.config["tasks"][0]["design"]
        design = h.read(design_path)
        design["exposure"] = []
        design_path.write_text(json.dumps(design), encoding="utf-8")
        self.store()
        with self.assertRaisesRegex(ValueError, "exposure"):
            self.plan()

    def test_same_model_can_review_in_separate_requests_without_author_context(self):
        self.config["judge"]["model"] = self.config["author"]["model"]
        self.config["judge"]["accepted_model_ids"] = list(self.config["author"]["accepted_model_ids"])
        self.store()
        out, _ = self.plan()
        judge_requests = []
        author_inputs = {}
        def call(settings, messages, folder):
            if "author" in folder.parts:
                packet = json.loads(messages[1]["content"])
                author_inputs[packet["brief"]] = packet["sources"]
                value = {"report": "A source-backed report.", "notes": "PRIVATE_AUTHOR_CONTEXT"}
            else:
                judge_requests.append(messages)
                value = self.judgment()
            h.save(folder / "response.json", value)
            return json.dumps(value)
        rows = h.run(out, call)
        self.assertEqual(len(rows), 5)
        self.assertEqual(len(judge_requests), 5)
        for messages in judge_requests:
            self.assertEqual([message["role"] for message in messages], ["system", "user"])
            packet = json.loads(messages[1]["content"])
            self.assertEqual(set(packet), {"brief", "sources", "rubric", "reports"})
            self.assertEqual(packet["sources"], author_inputs[packet["brief"]])
            self.assertNotIn("PRIVATE_AUTHOR_CONTEXT", json.dumps(messages))
            self.assertNotIn("COORDINATOR_ONLY_ANSWER", json.dumps(messages))
        self.assertEqual(h.read(out / "results.json")["requests_attempted"], 15)

    def test_changed_harness_stops_before_any_call(self):
        out, frozen = self.plan()
        frozen["harness_sha256"] = "0" * 64
        (out / "coordinator/frozen.json").write_text(json.dumps(frozen), encoding="utf-8")
        (out / "coordinator/freeze-commitment.json").write_text(json.dumps({"frozen_sha256": h.sha(h.encode(frozen))}), encoding="utf-8")
        with patch.object(h, "request") as call, self.assertRaisesRegex(ValueError, "Harness changed"):
            h.run(out, call)
        call.assert_not_called()
        self.assertFalse((out / "run-started.json").exists())

    def test_swaps_are_secondary_observations_and_metadata_stays_hidden(self):
        self.config.update(position_swap=True, max_requests=20)
        self.store()
        out, frozen = self.plan()
        observed = []
        def call(settings, messages, folder):
            observed.append(messages)
            if settings["model"] == "synthetic-author":
                value = {"report": 'Research Toolkit residual clue. ' + folder.name, "notes": "PRIVATE_NOTES"}
            else:
                value = self.judgment()
                value["preference"] = "B" if folder.name.endswith("-swapped") else "A"
            h.save(folder / "response.json", value)
            return '```json\n' + json.dumps(value) + '\n```'
        rows = h.run(out, call)
        self.assertEqual(len(observed), 20)
        self.assertEqual(len(rows), 5)
        self.assertTrue(all(r["position_swap"]["consistent"] for r in rows))
        for messages in observed:
            self.assertNotIn("COORDINATOR_ONLY_ANSWER", json.dumps(messages))
        for messages in observed[10:]:
            packet = json.loads(messages[1]["content"])
            self.assertNotIn("PRIVATE_NOTES", messages[1]["content"])
            self.assertEqual(set(packet), {"brief", "sources", "rubric", "reports"})
        pair = frozen["assignments"][0]["pair_id"]
        primary = h.read(out / f"judge-inputs/{pair}.json")
        swap = h.read(out / f"judge-inputs/{pair}-swapped.json")
        self.assertEqual(primary["reports"]["A"], swap["reports"]["B"])
        self.assertEqual(primary["reports"]["B"], swap["reports"]["A"])
        evidence = h.read(out / "coordinator/masking-observations.json")
        self.assertEqual(len(evidence["reports"]), 10)
        self.assertTrue(all("research toolkit" in r["literal_clues"] for r in evidence["reports"].values()))
        self.assertEqual(h.read(out / "results.json")["requests_attempted"], 20)
        parse = h.read(next((out / "coordinator/author").rglob("parse.json")))
        self.assertEqual(parse["method"], "single_json_fence")

    def test_invalid_output_is_retained_without_judge_or_retry(self):
        out, _ = self.plan()
        calls = []
        def call(settings, messages, folder):
            calls.append(folder)
            h.save(folder / "response.json", {"content": "ambiguous prose {}"})
            return "ambiguous prose {}"
        rows = h.run(out, call)
        self.assertEqual(len(calls), 10)
        self.assertEqual(len(list(out.rglob("content.txt"))), 10)
        self.assertEqual(len(list(out.rglob("invalid.json"))), 10)
        self.assertTrue(all(r["outcome"] == "unresolved" for r in rows))

    def test_swap_disagreement_or_failure_never_replaces_primary(self):
        self.config.update(position_swap=True, max_requests=20)
        self.store()
        out, frozen = self.plan()
        calls = []
        def call(settings, messages, folder):
            calls.append(folder)
            if settings["model"] == "synthetic-author":
                return self.fake(settings, messages, folder)
            if folder.name == "pair-01-swapped":
                h.save(folder / "execution.json", {"status": "synthetic_failure"})
                return None
            value = self.judgment()
            value["preference"] = "A"  # Deliberate position bias in the test judge.
            h.save(folder / "response.json", value)
            return json.dumps(value)
        rows = h.run(out, call)
        self.assertEqual(len(calls), 20)
        self.assertEqual([r["outcome"] for r in rows], [t["labels"]["A"] for t in frozen["assignments"]])
        self.assertIsNone(rows[0]["position_swap"]["consistent"])
        self.assertEqual(rows[0]["position_swap"]["status"], "unresolved_judge_failure")
        self.assertTrue(all(r["position_swap"]["consistent"] is False for r in rows[1:]))

    def test_transport_alias_json_mode_and_failure_categories(self):
        settings = {**self.config["author"], "response_format": "json_object", "accepted_model_ids": ["dated-snapshot"]}
        reply = {"model": "dated-snapshot", "usage": {"total_tokens": 30, "completion_tokens": 10},
                 "choices": [{"finish_reason": "stop", "message": {"content": '{"report":"S1 shows no benefit.","notes":""}'}}]}
        with patch.object(h.urllib.request, "build_opener") as build:
            response = build.return_value.open.return_value.__enter__.return_value
            response.read.return_value = json.dumps(reply).encode()
            self.assertIsNotNone(h.request(settings, [], self.base / "alias-valid"))
            request_body = h.read(self.base / "alias-valid/request.json")
            self.assertEqual(request_body["response_format"], {"type": "json_object"})
            reply["model"] = "undeclared-alias"
            response.read.return_value = json.dumps(reply).encode()
            self.assertIsNone(h.request(settings, [], self.base / "alias-invalid"))
            self.assertEqual(h.read(self.base / "alias-invalid/execution.json")["failure_kind"], "model_identity")
            response.read.return_value = b'not json\xff'
            self.assertIsNone(h.request(settings, [], self.base / "bad-bytes"))
            self.assertEqual((self.base / "bad-bytes/response.json").read_bytes(), b'not json\xff')
            self.assertEqual(h.read(self.base / "bad-bytes/execution.json")["failure_kind"], "response_envelope")
            build.return_value.open.side_effect = urllib.error.URLError(TimeoutError("Deadline reached"))
            self.assertIsNone(h.request(settings, [], self.base / "timeout"))
            self.assertEqual(h.read(self.base / "timeout/execution.json")["failure_kind"], "timeout")

    def test_supplied_development_pack_and_calibration_isolation(self):
        pack = h.ROOT / "evals/tasksets/development-v2-synthetic"
        frozen = h.prepare(pack / "study.json", self.base / "supplied-pack", 7)
        self.assertEqual(len(frozen["task_designs"]), 5)
        self.assertEqual(frozen["request_plan"]["total_max"], 20)
        self.assertEqual({t["language"] for t in frozen["assignments"]}, {"en", "zh-CN"})
        for task in frozen["assignments"]:
            self.assertEqual(frozen["input_text_sha256"][task["task_id"]]["brief"], h.sha(task["brief"].encode()))
            messages = h.author_messages(frozen, task, "without_toolkit")
            self.assertNotIn("expected_judgments", json.dumps(messages))
            self.assertIn(h.NOTES_MARKER, messages[0]["content"])
        cal = h.ROOT / "evals/tasksets/judge-calibration-v2"
        normal = h.read(cal / "judge-inputs/numeric.json")
        swap = h.read(cal / "judge-inputs/numeric-swapped.json")
        tie = h.read(cal / "judge-inputs/valid-tie.json")
        self.assertEqual(normal["reports"]["A"], swap["reports"]["B"])
        self.assertEqual(normal["reports"]["B"], swap["reports"]["A"])
        self.assertEqual(tie["reports"]["A"], tie["reports"]["B"])
        self.assertEqual(len(normal["reports"]["A"].split()), len(normal["reports"]["B"].split()))
        for packet in (normal, swap, tie):
            self.assertEqual(set(packet), {"brief", "sources", "rubric", "reports"})


if __name__ == "__main__":
    # Imported v1 tests are exercised by their own command.
    unittest.main(defaultTest="ProtocolV2Tests", verbosity=2)
