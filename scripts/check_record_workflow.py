"""Targeted record persistence and observation checks; no new model evaluation."""
import csv
from contextlib import closing
import json
import os
from pathlib import Path
import sqlite3
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import research_workflow as w
from check_research_workflow import BRIEF, SyntheticRunner, historical_contract, legacy_finish
from review_runner import ReviewFailure
from run_observation import capture_usage


class RecordWorkflowTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(dir=os.environ.get("IRF_TEST_TMPDIR"))
        self.addCleanup(tmp.cleanup)
        self.workspace = Path(tmp.name)
        w.start(self.workspace, "case", BRIEF)
        self.root = self.workspace / "case"

    def seed(self):
        w.save_text(self.root, "source.md", "Twelve shipments; revenue unknown.")
        return w.save_records(self.workspace, "case",
            sources=[{"title": 'Source, "quoted"\n中文', "url": "https://example.org", "source_type": "primary",
                      "read_scope": "full_text", "read_evidence": "source.md"}],
            claims=[{"claim": "Twelve shipments", "claim_type": "verified_fact", "supporting_sources": ["S1"]}],
            requirements=[{"summary": "Explain shipments", "status": "pending"}],
            draft={"path": "drafts/first.md", "content": "Twelve shipments. Revenue is unknown.", "complete": True})

    @unittest.skipUnless(os.name == "posix", "POSIX permission bits require a POSIX filesystem")
    def test_existing_permissions_survive_atomic_and_cli_record_saves(self):
        self.seed()
        modes = {"source.md": 0o644, "data/source_registry.csv": 0o660,
                 "data/claims_registry.csv": 0o600}
        for name, mode in modes.items():
            (self.root / name).chmod(mode)
        w.save_text(self.root, "source.md", "Thirteen shipments; revenue unknown.")
        result = subprocess.run([sys.executable, str(w.TOOLKIT / "scripts/research_workflow.py"),
            "save", "--workspace", str(self.workspace)], input=json.dumps({"task": "case",
            "sources": [{"source_id": "S1", "title": "Updated source"}],
            "claims": [{"claim_id": "C1", "claim": "Thirteen shipments"}]}),
            text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for name, mode in modes.items():
            self.assertEqual(stat.S_IMODE((self.root / name).stat().st_mode), mode, name)
        w.save_text(self.root, "private-new.md", "New file retains private creation permissions.")
        self.assertEqual(stat.S_IMODE((self.root / "private-new.md").stat().st_mode), 0o600)
        self.assertFalse(list(self.root.rglob("*.tmp")))

    def test_cli_selected_sharing_rejects_credentials_before_queueing(self):
        # Offline CLI path: isolated queue, synthetic strings, automatic sending disabled.
        env = {**os.environ, "RESEARCH_TOOLKIT_USAGE_HOME": str(self.workspace / "usage"),
               "RESEARCH_TOOLKIT_TELEMETRY": "on", "RESEARCH_TOOLKIT_USAGE_AUTOSEND": "off"}
        command = [sys.executable, "-X", "utf8", str(w.TOOLKIT / "scripts/usage_events.py"),
                   "share", "--task-root", str(self.root), "--confirm-content"]
        report = self.root / "report.md"
        report.write_text("# Findings\nEvidence remains [available](https://example.org/source).\n"
            "A SHA256: " + "a" * 64 + "\nJWT and Bearer authentication are protocol terms.\n"
            "Examples: password=<password>, password=${DB_PASSWORD}, password=REDACTED,\n"
            "Authorization: Bearer <token> and Authorization: Bearer YOUR_TOKEN.\n"
            "postgresql://user:<password>@db.example/test\n", encoding="utf-8")
        filenames = ["credentials.json", "client_secret.json", "client_secret_demo.json", ".npmrc",
                     ".netrc", "secrets.yaml", "nested/credentials.yml", ".env.local", "auth.json"]
        contents = ["xoxb-" + "1" * 12 + "-" + "2" * 12 + "-" + "a" * 24,
                    "AIza" + "a" * 35,
                    "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmaXh0dXJlIn0." + "a" * 43,
                    "Authorization: Bearer " + "a" * 48, "password=synthetic-not-a-real-password",
                    '{"password": "synthetic-not-a-real-password"}',
                    "postgresql://fixture:synthetic-password@db.invalid/test",
                    "sk-" + "a" * 40, "-----BEGIN PRIVATE KEY-----"]
        for name, content in [(name, "fixture") for name in filenames] + [
                ("selected.md", value) for value in contents]:
            with self.subTest(file=name, case=contents.index(content) if content in contents else "filename"):
                selected = self.root / name
                selected.parent.mkdir(parents=True, exist_ok=True)
                selected.write_text(content, encoding="utf-8")
                result = subprocess.run(command + ["--file", "report.md", "--file", name],
                                        env=env, text=True, encoding="utf-8", capture_output=True)
                self.assertNotEqual(result.returncode, 0, name)
                self.assertIn(name, result.stderr)
                self.assertNotIn(content, result.stderr)
                with closing(sqlite3.connect(self.workspace / "usage/usage.sqlite3")) as db:
                    self.assertEqual(db.execute("SELECT count(*) FROM content").fetchone()[0], 0)
        result = subprocess.run(command + ["--file", "report.md"], env=env,
                                text=True, encoding="utf-8", capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        with closing(sqlite3.connect(self.workspace / "usage/usage.sqlite3")) as db:
            rows = db.execute("SELECT payload FROM content").fetchall()
        self.assertEqual(len(rows), 1)
        self.assertEqual(json.loads(rows[0][0])["files"][0]["text"], report.read_text(encoding="utf-8"))

    def test_roundtrip_partial_updates_and_natural_key_retry(self):
        result = self.seed()
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["saved_ids"], {"sources": ["S1"], "claims": ["C1"], "requirements": ["R1"]})
        again = w.save_records(self.workspace, "case", sources=[{"url": "https://example.org", "title": "Updated title"}])
        self.assertEqual(again["saved_ids"]["sources"], ["S1"])
        with (self.root/"data/source_registry.csv").open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["read_evidence"], "source.md")
        self.assertEqual(w.load(self.root, "state/progress.json")["status"], "in_progress")
        reqs = (self.root/"state/requirements.jsonl").read_text(encoding="utf-8")
        self.assertEqual(json.loads(reqs)["status"], "pending")

    def test_bad_batch_preserves_records_and_reports_error_before_retry(self):
        self.seed()
        before = (self.root/"data/source_registry.csv").read_bytes()
        result = w.save_records(self.workspace, "case", sources=[{"source_id": "S1", "title": "New"}],
            requirements=[{"requirement_id": "R1", "length_constraint": {"min": "100"}}])
        self.assertFalse(result["ok"])
        self.assertIn("requirements[0].length_constraint", result["errors"][0])
        self.assertEqual((self.root/"data/source_registry.csv").read_bytes(), before)
        missing = w.save_records(self.workspace, "case", requirements=[{"requirement_id": "R1", "status": "satisfied"}])
        self.assertFalse(missing["ok"])
        self.assertIn(".evidence", missing["errors"][0])
        self.assertTrue(w.save_records(self.workspace, "case", requirements=[{"requirement_id": "R1", "status": "satisfied", "evidence": "drafts/first.md"}])["ok"])
        self.assertNotIn('activity', w.status(self.workspace, 'case'))
        events = [json.loads(line) for line in (self.root/'logs/activity.jsonl').read_text(encoding='utf-8').splitlines()]
        self.assertEqual(len([row for row in events if row.get('operation') == 'save' and row.get('outcome') == 'error']), 2)

    def test_changes_reuse_ids_locate_body_and_skip_identical_writes(self):
        self.seed()
        w.save_records(self.workspace, "case", claims=[
            {"claim_id": "C2", "claim": "Revenue not reported", "claim_type": "verified_fact", "supporting_sources": ["S1"]},
            {"claim_id": "C3", "claim": "Shipment interpretation", "claim_type": "interpretation", "supporting_sources": ["S1"]}])
        context = ("Before the measurement.\nContinued.\n\n"
                   "Twelve shipments [source](https://example.org).\nRevenue is unknown.\n\n"
                   "Not this URL: https://example.org/other")
        w.save_records(self.workspace, "case", draft={"path": "final.md", "content":
            "# Earlier\nOther section.\n## Findings\n" + context + "\n## Next\n" + context + "\n"})
        report_before = (self.root/"final.md").read_bytes()
        before = (self.root/"data/source_registry.csv").stat().st_mtime_ns
        same = w.save_records(self.workspace, "case", sources=[{"source_id": "S1"}])
        self.assertEqual(same["updated_files"], [])
        self.assertEqual((self.root/"data/source_registry.csv").stat().st_mtime_ns, before)
        self.assertEqual(same["changes"]["records"]["sources"]["unchanged"], ["S1"])
        self.assertEqual(same["changes"]["affected_claims"], [])
        (self.root/"source.md").write_text("Thirteen shipments.", encoding="utf-8")
        changed = w.save_records(self.workspace, "case", sources=[{"source_id": "S1"}])["changes"]
        self.assertEqual(changed["source_files"]["S1"]["status"], "changed")
        self.assertEqual(changed["affected_claims"][0]["claim_id"], "C1")
        self.assertEqual(changed["affected_claims"][0]["locations"], [{
            "line": 7, "heading": "Findings", "matched_by": ["claim_text", "source_link:S1"],
            "text": "Twelve shipments [source](https://example.org).",
            "context": {"start_line": 4, "end_line": 10, "text": context}}, {
            "line": 15, "heading": "Next", "matched_by": ["claim_text", "source_link:S1"],
            "text": "Twelve shipments [source](https://example.org).",
            "context": {"start_line": 12, "end_line": 18, "text": context}}])
        self.assertEqual([claim["claim_id"] for claim in changed["affected_claims"]], ["C1", "C2", "C3"])
        for claim in changed["affected_claims"][1:]:
            self.assertEqual(claim["changed_source_ids"], ["S1"])
            self.assertEqual(claim["locations"], [{
                "line": line, "heading": heading, "matched_by": ["source_link:S1"],
                "text": "Twelve shipments [source](https://example.org).",
                "context_ref": {"claim_id": "C1", "line": line}}
                for line, heading in ((7, "Findings"), (15, "Next"))])
        self.assertEqual((self.root/"final.md").read_bytes(), report_before)
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(w.status(self.workspace, "case")["changes"], changed)
        self.assertEqual(before, {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()})
        # A draft-only save keeps the batch but refreshes its line locations.
        latest = w.save_records(self.workspace, "case", draft={"path": "final.md", "content": "# New\n\nNo citation here."})
        self.assertEqual(latest["changes"]["affected_claims"][0]["location_status"], "not_located")

    def test_changes_first_observation_recovery_and_failed_save(self):
        first = self.seed()["changes"]
        self.assertEqual(first["source_files"]["S1"]["status"], "first_observation")
        self.assertEqual(first["records"]["sources"]["added"], ["S1"])
        failed = w.save_records(self.workspace, "case", sources=[{"source_id": "S1", "title": 1}])
        self.assertFalse(failed["ok"])
        self.assertEqual(w.status(self.workspace, "case")["changes"]["operation_id"], first["operation_id"])
        (self.root/"data/source_registry.csv").write_bytes(b'bad,"unclosed')
        recovered = w.save_records(self.workspace, "case", sources=[{"source_id": "S1", "title": "Restored",
            "url": "https://example.org", "source_type": "primary"}], replace=["sources"])
        self.assertEqual(recovered["changes"]["records"]["sources"]["recovered"], ["S1"])

    def test_source_changes_use_existing_reading_locator_formats(self):
        self.seed()
        for field in ("read_evidence", "evidence_path"):
            for locator in ("source.md#L1", "[reading](source.md#L1)", "source.md:1"):
                with self.subTest(field=field, locator=locator):
                    (self.root/"source.md").write_text("Before", encoding="utf-8")
                    w.save_records(self.workspace, "case", sources=[{"source_id": "S1",
                        "read_evidence": "", "evidence_path": "", field: locator}])
                    (self.root/"source.md").write_text("After", encoding="utf-8")
                    result = w.save_records(self.workspace, "case", sources=[{"source_id": "S1"}])
                    self.assertEqual(result["changes"]["source_files"]["S1"]["status"], "changed")
                    self.assertEqual(result["changes"]["source_files"]["S1"]["paths"], ["source.md"])
                    self.assertEqual(result["changes"]["affected_claims"][0]["claim_id"], "C1")

    def test_changes_legacy_log_and_removed_source_keep_unknown_locations(self):
        self.seed()
        log = self.root/"logs/activity.jsonl"
        legacy = '{"operation":"save","outcome":"saved"}\n'
        log.write_text('not-json\n' + legacy, encoding="utf-8")
        original = log.read_bytes()
        changes = w.status(self.workspace, "case")["changes"]
        self.assertFalse(changes["available"])
        self.assertIn("logs/activity.jsonl row 1", changes["warning"])
        self.assertEqual(log.read_bytes(), original)
        # Valid legacy rows still support removal tracking after log recovery.
        log.write_text(legacy, encoding="utf-8")
        removed = w.save_records(self.workspace, "case", sources=[], replace=["sources"])["changes"]
        self.assertEqual(removed["records"]["sources"]["removed"], ["S1"])
        self.assertEqual(removed["affected_claims"][0]["location_status"], "not_located")
        # A missing source remains an error in the original draft prerequisite.
        with self.assertRaises(ValueError):
            w.check_stage_records(self.root, "draft")

    def test_explicit_evidence_path_keeps_non_locator_extensions(self):
        self.seed()
        original = self.root/"source.xml"
        original.write_text("<shipments>12</shipments>", encoding="utf-8")
        w.save_records(self.workspace, "case", sources=[{"source_id": "S1", "evidence_path": "source.xml"}])
        w.check_stage_records(self.root, "draft")
        original.write_text("<shipments>13</shipments>", encoding="utf-8")
        result = w.save_records(self.workspace, "case", sources=[{"source_id": "S1"}])
        self.assertEqual(result["changes"]["source_files"]["S1"]["status"], "changed")
        self.assertEqual(result["changes"]["source_files"]["S1"]["paths"], ["source.md", "source.xml"])
        self.assertEqual(result["changes"]["affected_claims"][0]["claim_id"], "C1")

    def test_malformed_existing_records_can_be_replaced_with_original_backup(self):
        self.seed()
        path = self.root/"data/source_registry.csv"
        path.write_bytes(b'broken,"unterminated')
        rows = [{"source_id": "S1", "title": "Recovered", "url": "https://example.org", "source_type": "primary"}]
        self.assertFalse(w.save_records(self.workspace, "case", sources=rows)["ok"])
        result = w.save_records(self.workspace, "case", sources=rows, replace=["sources"])
        self.assertTrue(result["ok"], result)
        self.assertEqual((self.root/result["backups"][0]).read_bytes(), b'broken,"unterminated')

    def test_write_failure_rolls_back_and_draft_cannot_overwrite_state(self):
        self.seed()
        before = {name: (self.root/name).read_bytes() for name in ("data/source_registry.csv", "data/claims_registry.csv")}
        import research_records
        original = research_records.os.replace
        count = 0
        def fail_second(src, dst):
            nonlocal count
            count += 1
            if count == 2:
                raise OSError("controlled write failure")
            return original(src, dst)
        with patch.object(research_records.os, "replace", side_effect=fail_second):
            result = w.save_records(self.workspace, "case", sources=[{"source_id": "S1", "title": "New"}], claims=[{"claim_id": "C1", "claim": "Changed"}])
        self.assertFalse(result["ok"])
        self.assertEqual(before, {name: (self.root/name).read_bytes() for name in before})
        for path in ("../outside.md", "state/task_spec.md", "data/source_registry.csv"):
            self.assertFalse(w.save_records(self.workspace, "case", draft={"path": path, "content": "Overwrite"})["ok"])

    def test_first_complete_draft_is_retained_and_status_and_checks_stay_readonly(self):
        self.seed()
        path = self.root/'logs/activity.jsonl'
        original = path.read_bytes()
        first = next(json.loads(line) for line in original.decode('utf-8').splitlines() if json.loads(line).get('complete_draft'))
        self.assertEqual(first['artifact'], 'drafts/first.md')
        self.assertNotIn('elapsed_seconds', first)
        self.assertNotIn('activity', w.status(self.workspace, 'case'))
        self.assertTrue(w.save_records(self.workspace, "case", draft={"path": "final.md", "content": "Updated report.", "complete": True})["ok"])
        self.assertTrue(path.read_bytes().startswith(original))
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        w.status(self.workspace, "case")
        w.check_draft(self.workspace, "case", "final.md")
        self.assertEqual(before, {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()})
        (self.root/"logs/activity.jsonl").write_bytes(b"\xff")
        self.assertTrue(w.status(self.workspace, "case")["current_work"]["warnings"])

    def test_cli_save_resumes_current_contract_and_preserves_historical_checklist(self):
        self.seed()
        w.save_records(self.workspace, "case", requirements=[{"requirement_id": "R1", "status": "satisfied", "evidence": "drafts/first.md"}])
        progress = w.load(self.root, "state/progress.json")
        w.save(self.root, "state/progress.json", {**progress, "review_contract": 1, "stage": "final", "status": "complete"})
        w.save(self.root, "state/final_checklist.json", {"schema_version": 1, "artifact": "drafts/first.md", "items": {"requirements": {"passed": True, "evidence": "Historical saved author check"}}})
        receipt = (self.root/"state/final_checklist.json").read_bytes()
        result = subprocess.run([sys.executable, "-X", "utf8", str(w.TOOLKIT/"scripts/research_workflow.py"),
            "save", "--workspace", str(self.workspace)], input=json.dumps({"task": "case", "claims": [{"claim_id": "C1", "uncertainty": "New qualification"}]}), text=True, encoding="utf-8", capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        progress = w.status(self.workspace, 'case')['progress']
        self.assertEqual(progress['status'], 'in_progress')
        self.assertEqual(progress['review_contract'], 2)
        self.assertFalse(w.finish(self.workspace, 'case', 'Complete.', artifact='drafts/first.md')['completed'])
        self.assertEqual((self.root/"state/final_checklist.json").read_bytes(), receipt)

    def test_failed_backend_capture_is_retained_without_default_activity_totals(self):
        workspace = self.workspace
        w.start(workspace, "full", BRIEF)
        root = workspace/"full"
        w.save_text(root, "source.md", "Twelve shipments.")
        w.save_records(workspace, "full", sources=[{"title": "Source", "url": "https://example.org", "source_type": "primary", "read_scope": "full_text", "read_evidence": "source.md"}],
            claims=[{"claim": "Twelve shipments", "claim_type": "verified_fact", "supporting_sources": ["S1"]}], draft={"path": "final.md", "content": "Twelve shipments.", "complete": True,
                    "main": True, "host_task": "synthetic-backend-author"})
        calls = []
        def runner(config, request, cwd):
            calls.append(1)
            capture = {"backend": "generic", "response": json.dumps({"usage": {"prompt_tokens": 100, "completion_tokens": 10, "prompt_tokens_details": {"cached_tokens": 60}}})}
            if len(calls) == 1:
                raise ReviewFailure("Controlled interrupted response", capture)
            return {**SyntheticRunner()({}, request, cwd), "capture": capture}
        config = {"reviewers": [{"id": "one", "model": "synthetic", "format": "json"}]}
        result = w.review(workspace, "full", ["source.md"], config=config, runner=runner)
        self.assertFalse(result['reviews_complete'])
        failed = root/result['retained_execution']
        failed_bytes = failed.read_bytes()
        self.assertEqual(capture_usage(json.loads(failed_bytes)), {'input_tokens': 100, 'output_tokens': 10, 'cached_input_tokens': 60})
        self.assertNotIn('activity', w.status(workspace, 'full'))
        resumed = w.review(workspace, "full", ["source.md"], config=config, runner=runner)
        self.assertTrue(resumed['delivery_ready'], resumed)
        self.assertEqual(len(calls), 11)  # One interrupted transport; ten completed independent assignments.
        self.assertEqual(failed.read_bytes(), failed_bytes)
        history = (root/'logs/review.jsonl').read_bytes()
        self.assertTrue(w.review(workspace, 'full', ['source.md'], config=config, runner=runner)['delivery_ready'])
        self.assertEqual(len(calls), 11)
        self.assertEqual((root/'logs/review.jsonl').read_bytes(), history)
        self.assertNotIn('activity', w.status(workspace, 'full'))
        self.assertIsNone(capture_usage({"format": "json", "stdout": "{}"}))


if __name__ == "__main__":
    os.environ["RESEARCH_TOOLKIT_TELEMETRY"] = "off"
    unittest.main()
