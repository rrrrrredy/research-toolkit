#!/usr/bin/env python3
"""Offline controls for retained output parsing and transport."""
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



if __name__ == "__main__":
    # Imported v1 tests are exercised by their own command.
    unittest.main(defaultTest="ProtocolV2Tests", verbosity=2)
