#!/usr/bin/env python3
"""Isolated controls for ownership-aware plugin synchronization (no model calls)."""
import json
from pathlib import Path
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
