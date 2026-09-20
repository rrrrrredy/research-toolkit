#!/usr/bin/env python3
"""Offline controls for stored HTML extraction; no semantic quality scoring."""
from contextlib import redirect_stderr, redirect_stdout
import hashlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest

import extract_source_text as extractor


class SourceExtractionTests(unittest.TestCase):
    def test_visible_text_alone_would_lose_publication_date(self):
        data = b'''<html><script type="application/ld+json">
        {"@graph":[{"@type":"NewsArticle","datePublished":"2021-06-23",
                    "dateModified":"2021-06-24"}]}
        </script><p>The pilot plant is operating.</p></html>'''
        result = extractor.extract_html(data)
        self.assertEqual(result["text"], "The pilot plant is operating.")
        fields = result["publisher_metadata"]["date_fields"]
        self.assertEqual(
            [(r["field"], r["raw_value"], r["json_pointer"]) for r in fields],
            [("datePublished", "2021-06-23", "/@graph/0/datePublished"),
             ("dateModified", "2021-06-24", "/@graph/0/dateModified")],
        )
        self.assertEqual(result["source"]["sha256"], hashlib.sha256(data).hexdigest())

    def test_distinct_conflicting_fields_are_retained_not_resolved(self):
        data = b'''<meta property="article:published_time" content="2024-03-05">
        <script type="APPLICATION/LD+JSON; charset=utf-8">
        [{"dateCreated":"2024-03-04","datePublished":"2024-03-06"}]
        </script><link rel="alternate canonical" href="/other-version"><p>Report.</p>'''
        result = extractor.extract_html(data)
        fields = result["publisher_metadata"]["date_fields"]
        self.assertEqual([r["raw_value"] for r in fields],
                         ["2024-03-05", "2024-03-04", "2024-03-06"])
        self.assertEqual(result["publisher_metadata"]["declared_canonical_urls"], ["/other-version"])
        self.assertNotIn("publication_date", result)

    def test_inline_unicode_and_link_are_preserved(self):
        result = extractor.extract_html(
            '<p>培养<b>鲑鱼</b>，有<a href="/source?a=1&amp;b=2">原件</a>。</p>'
            '<p>第二段<img alt="图示"/></p>'.encode()
        )
        self.assertEqual(result["text"], "培养鲑鱼，有原件 [href: /source?a=1&b=2]。\n第二段[image alt: 图示]")

    def test_script_instructions_are_not_executed_or_added_as_article_text(self):
        result = extractor.extract_html(
            b'<script>throw Error("execute me")</script><style>body{display:none}</style>'
            b'<svg><text>hidden figure text</text></svg><noscript>fallback</noscript>'
            b'<template>template</template><p>Actual source</p>'
        )
        self.assertEqual(result["text"], "Actual source")
        self.assertIn("never instructions", result["scope"])

    def test_malformed_and_unclosed_jsonld_remain_visible_as_limits(self):
        for data in [b'<script type="application/ld+json">{broken}</script><p>Body</p>',
                     b'<p>Body</p><script type="application/ld+json">{"datePublished":"2020"}']:
            result = extractor.extract_html(data)
            self.assertEqual(result["text"], "Body")
            self.assertFalse(result["publisher_metadata"]["metadata_extraction_complete"])
            self.assertTrue(result["publisher_metadata"]["jsonld_errors"])

    def test_strict_decoding_and_explicit_override(self):
        text = '<meta charset="windows-1252"><p>caf\u00e9</p>'
        self.assertEqual(extractor.extract_html(text.encode("cp1252"))["text"], "café")
        with self.assertRaises(UnicodeDecodeError):
            extractor.extract_html(b"<p>\xff</p>")
        self.assertEqual(extractor.extract_html(b"<p>\xff</p>", encoding="latin-1")["text"], "ÿ")
        self.assertEqual(extractor.extract_html("<p>研究</p>".encode("utf-16"))["text"], "研究")

    def test_creation_and_access_do_not_become_publication(self):
        result = extractor.extract_html(
            b'<script type="application/ld+json">{"dateCreated":"2020"}</script><p>x</p>',
            source_url="https://example.org/source", accessed_at="2026-09-20T10:00:00Z",
        )
        self.assertEqual(result["source"]["declared_accessed_at"], "2026-09-20T10:00:00Z")
        self.assertEqual([r["field"] for r in result["publisher_metadata"]["date_fields"]], ["dateCreated"])
        self.assertIsNone(extractor.extract_html(b"<p>x</p>")["source"]["declared_accessed_at"])

    def test_existing_output_and_original_source_are_not_overwritten(self):
        with tempfile.TemporaryDirectory(prefix="source-extraction-") as tmp:
            source, output = Path(tmp) / "source.html", Path(tmp) / "evidence.json"
            source.write_bytes(b"<p>Source</p>")
            output.write_bytes(b"existing frozen result")
            with redirect_stderr(io.StringIO()), redirect_stdout(io.StringIO()):
                self.assertEqual(extractor.main([str(source), "--output", str(output)]), 2)
                self.assertEqual(extractor.main([str(source), "--output", str(source)]), 2)
            self.assertEqual(output.read_bytes(), b"existing frozen result")
            self.assertEqual(source.read_bytes(), b"<p>Source</p>")

    def test_cli_json_binds_exact_source_without_local_path_leak(self):
        with tempfile.TemporaryDirectory(prefix="source-extraction-") as tmp:
            source, output = Path(tmp) / "source.html", Path(tmp) / "evidence.json"
            raw = b"<p>Known-good source</p>\r\n"
            source.write_bytes(raw)
            with redirect_stdout(io.StringIO()):
                self.assertEqual(extractor.main([str(source), "--output", str(output)]), 0)
            result = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(result["source"]["sha256"], hashlib.sha256(raw).hexdigest())
            self.assertNotIn(str(source), output.read_text(encoding="utf-8"))
            self.assertEqual(source.read_bytes(), raw)


if __name__ == "__main__":
    if os.environ.get("IRF_TEST_TMPDIR"):
        tempfile.tempdir = os.environ["IRF_TEST_TMPDIR"]
    unittest.main(verbosity=2)
