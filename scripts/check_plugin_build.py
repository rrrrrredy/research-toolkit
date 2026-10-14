#!/usr/bin/env python3
"""Isolated controls for ownership-aware plugin synchronization (no model calls)."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import build_plugin as b


class PluginBuildChecks(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="toolkit-plugin-control-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        self.plugin = self.root / "plugins/research-toolkit"
        self.files = {"references/probe.md": b"first\n", "VERSION": b"1.0.0\n"}
        for name, value in (("ROOT", self.root), ("PLUGIN", self.plugin), ("payload", lambda: self.files)):
            mock = patch.object(b, name, value)
            mock.start()
            self.addCleanup(mock.stop)
        b.build()

    def snapshot(self):
        return {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}

    def test_add_modify_delete_rename_readonly_and_idempotence(self):
        for action in ("add", "modify", "delete", "rename"):
            if action == "add":
                self.files["references/added.md"] = b"added\n"
            elif action == "modify":
                self.files["references/probe.md"] = b"edited\n"
            elif action == "delete":
                del self.files["references/added.md"]
            else:
                self.files["references/renamed.md"] = self.files.pop("references/probe.md")
            before = self.snapshot()
            self.assertTrue(b.build(check=True), action)
            self.assertEqual(before, self.snapshot(), action)
            self.assertTrue(b.build(), action)
            self.assertEqual(b.build(check=True), [], action)
            after = self.snapshot()
            self.assertEqual(b.build(), [], action)
            self.assertEqual(after, self.snapshot(), action)
        self.assertFalse((self.plugin / "references/probe.md").exists())
        self.assertFalse((self.plugin / "references/added.md").exists())

    def test_manual_metadata_and_unknown_files_preserved(self):
        for relative in (".codex-plugin/plugin.json", ".mcp.json", "notes.txt", "references/manual.md"):
            path = self.plugin / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"hand written\n")
        before = self.snapshot()
        self.assertEqual(b.build(), [])
        self.assertEqual(before, self.snapshot())

    def test_modified_obsolete_file_is_not_deleted_and_plan_does_not_partially_write(self):
        del self.files["references/probe.md"]
        self.files["references/new.md"] = b"new\n"
        (self.plugin / "references/probe.md").write_bytes(b"local edit\n")
        before = self.snapshot()
        for check in (True, False):
            with self.assertRaisesRegex(ValueError, "modified"):
                b.build(check)
            self.assertEqual(before, self.snapshot())

    def test_bootstrap_only_adopts_matching_files(self):
        (self.plugin / b.MANIFEST).unlink()
        self.assertEqual(b.build(True), [b.MANIFEST])
        b.build()
        (self.plugin / b.MANIFEST).unlink()
        (self.plugin / "references/probe.md").write_bytes(b"unknown content")
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "Unowned file"):
            b.build()
        self.assertEqual(before, self.snapshot())

    def test_newline_equivalence(self):
        (self.plugin / "references/probe.md").write_bytes(b"first\r\n")
        self.assertEqual(b.build(True), [])
        del self.files["references/probe.md"]
        b.build()
        self.assertFalse((self.plugin / "references/probe.md").exists())

    def test_invalid_manifest_cannot_claim_metadata_or_outside_paths(self):
        for relative in ("../outside.md", "/outside.md", "references/../manual.md", "references\\probe.md", ".mcp.json", ".codex-plugin/plugin.json"):
            with self.subTest(relative=relative):
                (self.plugin / b.MANIFEST).write_text(json.dumps({"schema_version": 1, "files": {relative: "0" * 64}}), encoding="utf-8")
                before = self.snapshot()
                with self.assertRaises(ValueError):
                    b.build()
                self.assertEqual(before, self.snapshot())

    def test_linked_obsolete_file_and_parent_are_not_followed(self):
        outside = self.root / "outside.md"
        outside.write_bytes(b"first\n")
        path = self.plugin / "references/probe.md"
        path.unlink()
        try:
            path.symlink_to(outside)
        except OSError as exc:
            self.skipTest(f"Creating symlinks is unavailable: {exc}")
        del self.files["references/probe.md"]
        with self.assertRaises(ValueError):
            b.build()
        self.assertTrue(path.is_symlink())
        self.assertEqual(outside.read_bytes(), b"first\n")
        path.unlink()
        (self.plugin / "references").rmdir()
        target = self.root / "other-references"
        target.mkdir()
        (target / "probe.md").write_bytes(b"first\n")
        (self.plugin / "references").symlink_to(target, target_is_directory=True)
        with self.assertRaises(ValueError):
            b.build()
        self.assertTrue((target / "probe.md").is_file())


class PluginEntrypointChecks(unittest.TestCase):
    """Exercise the real CLI, including version writes before payload generation."""

    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="toolkit-cli-control-")
        self.addCleanup(temp.cleanup)
        self.trial = Path(temp.name).resolve()
        self.root = self.trial / "repo"
        self.plugin = self.root / "plugins/research-toolkit"
        desired = b.payload()
        for relative, content in desired.items():
            for path in (self.root / relative, self.plugin / relative):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
        for relative in ("scripts/build_plugin.py", "scripts/check_version.py", "CHANGELOG.md", "CHANGELOG.zh-CN.md"):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(b.ROOT / relative, path)
        shutil.copytree(b.ROOT / "docs/releases", self.root / "docs/releases")
        for name in ("plugin.json", ".codex-plugin/plugin.json"):
            path = self.plugin / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps({"name": "fixture", "version": "0.0.0"}), encoding="utf-8")
        (self.plugin / b.MANIFEST).write_text(json.dumps({"schema_version": 1, "files": {
            name: b.digest(content) for name, content in desired.items()}}), encoding="utf-8")

    def snapshot(self):
        return {p.relative_to(self.trial): p.read_bytes() for p in self.trial.rglob("*") if p.is_file()}

    def command(self, script, *args):
        return subprocess.run([sys.executable, "-B", "-X", "utf8", str(self.root / "scripts" / script), *args],
                              cwd=self.root, capture_output=True, text=True, encoding="utf-8", timeout=30)

    def link(self, relative, junction=False):
        path = self.root / relative
        outside = self.trial / ("outside-" + path.name)
        directory = path.is_dir()
        path.rename(outside)
        if junction:
            helper = self.trial / "link.ps1"
            helper.write_text("param([string]$LinkPath,[string]$TargetPath)\n$ErrorActionPreference='Stop'\n"
                              "New-Item -ItemType Junction -Path $LinkPath -Target $TargetPath | Out-Null\n", encoding="utf-8")
            result = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
                                     "-File", str(helper), str(path), str(outside)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.addCleanup(os.rmdir, path)  # Remove only the junction, before TemporaryDirectory cleanup.
        else:
            try:
                path.symlink_to(outside, target_is_directory=directory)
            except OSError as exc:
                if os.name == "nt" and exc.winerror == 1314:
                    self.skipTest(f"Local Windows symlink privilege unavailable; Linux CI must run this: {exc}")
                raise
            self.addCleanup(path.unlink)

    def assert_rejected_without_writes(self, include_version=True):
        commands = [("build_plugin.py",), ("build_plugin.py", "--check")]
        if include_version:
            commands += [("check_version.py", "--write"), ("check_version.py",)]
        before = self.snapshot()
        for command in commands:
            with self.subTest(command=command):
                result = self.command(*command)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertEqual(before, self.snapshot(), result.stdout + result.stderr)

    def test_real_cli_updates_versions_and_check_is_readonly(self):
        before = self.snapshot()
        self.assertEqual(self.command("build_plugin.py", "--check").returncode, 1)
        self.assertEqual(before, self.snapshot())
        result = self.command("build_plugin.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        version = (self.root / "VERSION").read_text().strip()
        for name in ("plugin.json", ".codex-plugin/plugin.json"):
            self.assertEqual(json.loads((self.plugin / name).read_text())["version"], version)
        after = self.snapshot()
        self.assertEqual(self.command("build_plugin.py", "--check").returncode, 0)
        self.assertEqual(self.command("build_plugin.py").returncode, 0)
        self.assertEqual(after, self.snapshot())

    def test_first_manifest_file_symlink_is_rejected(self):
        self.link("plugins/research-toolkit/plugin.json")
        self.assert_rejected_without_writes()

    def test_second_manifest_file_symlink_cannot_partially_update_first(self):
        self.link("plugins/research-toolkit/.codex-plugin/plugin.json")
        self.assert_rejected_without_writes()

    def test_manifest_parent_symlink_is_rejected(self):
        self.link("plugins/research-toolkit/.codex-plugin")
        self.assert_rejected_without_writes()

    def test_plugin_directory_symlink_is_rejected(self):
        self.link("plugins/research-toolkit")
        self.assert_rejected_without_writes()

    def test_plugins_parent_symlink_is_rejected(self):
        self.link("plugins")
        self.assert_rejected_without_writes()

    def test_generated_file_symlink_prevents_earlier_version_writes(self):
        self.link("plugins/research-toolkit/SKILL.md")
        self.assert_rejected_without_writes(include_version=False)

    @unittest.skipUnless(os.name == "nt", "Windows junction control")
    def test_manifest_parent_junction_is_rejected(self):
        self.link("plugins/research-toolkit/.codex-plugin", junction=True)
        self.assert_rejected_without_writes()

    @unittest.skipUnless(os.name == "nt", "Windows junction control")
    def test_plugin_directory_junction_is_rejected(self):
        self.link("plugins/research-toolkit", junction=True)
        self.assert_rejected_without_writes()

    def test_invalid_release_metadata_does_not_partially_update_versions(self):
        (self.root / "CHANGELOG.zh-CN.md").write_text("# No version entry\n", encoding="utf-8")
        self.assert_rejected_without_writes()


if __name__ == "__main__":
    unittest.main(verbosity=2)
