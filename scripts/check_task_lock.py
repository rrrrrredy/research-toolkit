#!/usr/bin/env python3
"""Real-process controls for shared task locking; no model calls."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import research_workflow as workflow
from task_lock import task_lock

SCRIPTS = Path(__file__).resolve().parent


class TaskLockTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="task-lock-")
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name)
        workflow.start(self.workspace, "one", {}, profile="lite")
        workflow.start(self.workspace, "two", {}, profile="lite")

    def cli(self, action, task):
        request = {"start": {"brief": {}, "profile": "lite"}, "status": {"stage": "collect"},
                   "review": {"evidence_paths": []}, "finish": {"message": "Synthetic delivery"}, "check-draft": {}}[action]
        return subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS / "research_workflow.py"),
                               action, "--workspace", str(self.workspace)],
                              input=json.dumps({"task": task, **request}),
                              capture_output=True, text=True, encoding="utf-8")

    def test_cli_and_direct_operations_share_lock_and_preserve_records(self):
        root = self.workspace / "one"
        before = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
        with task_lock(root):
            for action in ("start", "status", "review", "finish", "check-draft"):
                blocked = self.cli(action, "one")
                self.assertNotEqual(blocked.returncode, 0)
                self.assertIn("active operation", blocked.stdout)
            self.assertEqual(self.cli("start", "two").returncode, 0)
        self.assertEqual({p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}, before)
        self.assertEqual(self.cli("start", "one").returncode, 0)

    def test_crashed_process_releases_lock_without_deleting_lock_file(self):
        code = ("import sys;from pathlib import Path;sys.path.insert(0,sys.argv[1]);from task_lock import task_lock;"
                "lock=task_lock(Path(sys.argv[2]));lock.__enter__();print('locked',flush=True);sys.stdin.read()")
        process = subprocess.Popen([sys.executable, "-u", "-c", code, str(SCRIPTS), str(self.workspace / "one")],
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                   creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        try:
            self.assertEqual(process.stdout.readline().strip(), "locked")
            blocked = self.cli("start", "one")
            self.assertIn("active operation", blocked.stdout)
            process.kill()
            process.wait(timeout=10)
            self.assertTrue((self.workspace / "one/.research-toolkit.lock").exists())
            self.assertEqual(self.cli("start", "one").returncode, 0)
        finally:
            if process.poll() is None:
                process.kill()
            process.communicate(timeout=10)

    def test_nested_same_thread_and_exception_release(self):
        root = self.workspace / "one"
        with self.assertRaisesRegex(RuntimeError, "synthetic"):
            with task_lock(root), task_lock(root):
                workflow.status(self.workspace, "one")
                raise RuntimeError("synthetic")
        self.assertEqual(self.cli("start", "one").returncode, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
