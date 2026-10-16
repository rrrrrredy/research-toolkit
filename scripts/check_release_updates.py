"""Three focused controls for registered release-log comparisons; no model calls."""
import csv
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import URLError

import research_workflow as workflow

# Short verbatim headings from the real QwenWork log read on 2026-10-16.
# The bodies below are synthetic transport controls, not capability evidence.
URL = "https://docs.qwenwork.cn/release-notes/desktop"
OLD = "2026年10月09日\n千问办公 1.2.5\nPrevious release body.\n"
NEW = "2026年10月15日\n千问办公 1.3.1\nNew release body.\n" + OLD


class ReleaseUpdateTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(dir=os.environ.get("IRF_TEST_TMPDIR"))
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name)
        self.root = self.workspace / "case"
        for folder in ("data", "sources", "logs"):
            (self.root / folder).mkdir(parents=True)
        self.baseline = self.root / "sources/log.md"
        self.baseline.write_text(OLD, encoding="utf-8")
        with (self.root / "data/source_registry.csv").open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["source_id", "url", "source_type", "evidence_path"])
            writer.writeheader()
            writer.writerow({"source_id": "S3", "url": URL, "source_type": "official_release", "evidence_path": "sources/log.md"})
        (self.root / "data/claims_registry.csv").write_text("claim_id,claim,supporting_sources\nC5,Previous version,S3\n", encoding="utf-8")
        (self.root / "report.md").write_text(
            f"## Alibaba\nPrevious version. [Release log]({URL})\nReported availability only.\n\n"
            "Actual editing quality remains unverified.\n## Other\nUnrelated section.\n", encoding="utf-8")
        (self.root / "logs/activity.jsonl").write_text(json.dumps({"outcome": "saved", "artifact": "report.md"}) + "\n", encoding="utf-8")

    def check(self):
        return workflow.dispatch("check-updates", {"task": "case", "source_id": "S3"}, self.workspace)

    def test_new_release_returns_content_date_and_existing_location(self):
        report_before = (self.root / "report.md").read_bytes()
        with (self.root / "data/claims_registry.csv").open("a", encoding="utf-8") as file:
            file.write("C6,Related judgment,S3\n")
        with patch("release_updates.fetch_log", return_value=NEW) as fetch:
            result = self.check()
        fetch.assert_called_once_with(URL)
        self.assertEqual(result["status"], "changed")
        self.assertEqual([(e["date"], e["version"], e["added_content"]) for e in result["changes"]],
                         [("2026-10-15", "1.3.1", ["New release body."])])
        self.assertEqual(result["affected_claims"][0]["locations"], [{
            "line": 2, "heading": "Alibaba", "matched_by": ["claim_text", "source_link:S3"],
            "text": f"Previous version. [Release log]({URL})",
            "context": {"start_line": 2, "end_line": 5,
                        "text": f"Previous version. [Release log]({URL})\nReported availability only.\n\n"
                                "Actual editing quality remains unverified."}}])
        self.assertEqual(result["affected_claims"][1], {
            "claim_id": "C6", "claim": "Related judgment", "changed_source_ids": ["S3"],
            "locations": [{"line": 2, "heading": "Alibaba", "matched_by": ["source_link:S3"],
                           "text": f"Previous version. [Release log]({URL})",
                           "context_ref": {"claim_id": "C5", "line": 2}}], "location_status": "matched"})
        self.assertEqual(self.baseline.read_text(encoding="utf-8"), OLD)
        self.assertEqual((self.root / "report.md").read_bytes(), report_before)

    def test_unchanged_ignores_web_export_markup_and_stops(self):
        self.baseline.write_text("L22: 2026年10月09日\nL24: 千问办公 1.2.5\nL26: * Previous release body.\n", encoding="utf-8")
        with patch("release_updates.fetch_log", return_value=OLD), patch("release_updates.impact_view") as locate:
            result = self.check()
        self.assertEqual(result["status"], "unchanged")
        self.assertEqual(result["changes"], [])
        locate.assert_not_called()

    def test_failed_read_is_not_unchanged(self):
        with patch("release_updates.fetch_log", side_effect=URLError("fixture network failure")):
            result = self.check()
        self.assertFalse(result["ok"])
        self.assertEqual((result["status"], result["phase"]), ("failed", "fetch"))
        self.assertIn("fixture network failure", result["error"])
        self.assertEqual(self.baseline.read_text(encoding="utf-8"), OLD)


if __name__ == "__main__":
    unittest.main()
