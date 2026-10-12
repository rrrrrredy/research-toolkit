#!/usr/bin/env python3
"""Read-only study verification controls; mutate temporary copies, never evidence."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

STUDY = Path(__file__).resolve().parents[1] / "evals/studies/2026-10-10-lite-four-models"


class StudyVerificationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="study-verification-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "study"
        shutil.copytree(STUDY, self.root, ignore=shutil.ignore_patterns("__pycache__"))

    def run_script(self, name, *args):
        return subprocess.run([sys.executable, "-B", "-O", "-X", "utf8", str(self.root / name), *args],
                              capture_output=True, text=True, encoding="utf-8",
                              env={**os.environ, "RESEARCH_TOOLKIT_ROOT": str(STUDY.parents[2])})

    def mutate(self, relative, edit):
        path = self.root / relative
        value = json.loads(path.read_text(encoding="utf-8"))
        edit(value)
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")

    def test_optimized_verifier_rejects_changed_plan(self):
        self.mutate("study-plan.json", lambda value: value.update(families=999))
        result = self.run_script("verify_bundle.py")
        self.assertNotEqual(result.returncode, 0, result.stdout)

    def test_default_verifier_covers_completion_supplement(self):
        path = self.root / "completion-supplement/longcat/authors/pair-01/with_toolkit/report.md"
        path.write_text("Changed after the study.", encoding="utf-8")
        result = self.run_script("verify_bundle.py")
        self.assertNotEqual(result.returncode, 0, result.stdout)

    def test_optimized_completion_audit_rejects_changed_plan(self):
        self.mutate("completion-supplement/plan.json", lambda value: value.update(author_calls_planned=999))
        result = self.run_script("summarize_completion.py", "--verify-only")
        self.assertNotEqual(result.returncode, 0, result.stdout)

    def test_valid_default_commands_do_not_write_study_files(self):
        def snapshot():
            return {p.relative_to(self.root).as_posix(): (hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_mtime_ns)
                    for p in self.root.rglob("*") if p.is_file() and "__pycache__" not in p.parts}
        before = snapshot()
        for name in ("verify_bundle.py", "summarize.py", "summarize_completion.py"):
            with self.subTest(command=name):
                result = self.run_script(name)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(snapshot(), before, f"{name} changed study files")

    def test_derived_mismatch_fails_without_repairing_history(self):
        for script, filename in (("summarize.py", "summary.json"), ("summarize_completion.py", "completion-summary.json")):
            with self.subTest(command=script):
                self.mutate(filename, lambda value: value.update(scope="Changed derived summary"))
                before = (self.root / filename).read_bytes()
                result = self.run_script(script)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertEqual((self.root / filename).read_bytes(), before)

    def test_outcomes_are_bound_to_frozen_labels_and_preferences(self):
        for relative, provider in (("runs/deepseek", "deepseek"), ("format-supplement/kimi", "kimi")):
            code = ("import sys;from pathlib import Path;sys.path.insert(0,sys.argv[1]);import verify_bundle as v;"
                    "root=Path(sys.argv[1]);v.check_results(root/sys.argv[2],"
                    "v.read(root/'runs'/sys.argv[3]/'coordinator/frozen.json')['assignments'])")
            command = [sys.executable, "-B", "-O", "-c", code, str(self.root), relative, provider]
            control = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(control.returncode, 0, control.stderr)
            path = self.root / relative / "results.json"
            original = path.read_bytes()
            for field in ("outcome", "preference"):
                with self.subTest(stage=relative, field=field):
                    path.write_bytes(original)
                    def change(value):
                        row = next(row for row in value["results"] if row["status"] == "judged")
                        row[field] = ("without_toolkit" if row[field] == "with_toolkit" else "with_toolkit") if field == "outcome" else ("A" if row[field] != "A" else "B")
                    self.mutate(relative + "/results.json", change)
                    result = subprocess.run(command, capture_output=True, text=True)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(f"{field} differs", result.stderr)

    def test_explicit_write_preserves_newline_style(self):
        for script, files in (("summarize.py", ("summary.json", "scores.csv", "usage.csv")),
                              ("summarize_completion.py", ("completion-summary.json", "coverage-scores.csv", "completion-usage.csv"))):
            with self.subTest(command=script):
                for name in files:
                    path = self.root / name
                    path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
                before = {name: (self.root / name).read_bytes() for name in files}
                result = self.run_script(script, "--write")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual({name: (self.root / name).read_bytes() for name in files}, before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
