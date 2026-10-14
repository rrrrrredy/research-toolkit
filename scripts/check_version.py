#!/usr/bin/env python3
"""Check current release metadata against VERSION; --write refreshes package mirrors."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import stat

ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = ("plugins/research-toolkit/plugin.json", "plugins/research-toolkit/.codex-plugin/plugin.json")


def safe_repo_file(root: Path, relative: str) -> Path:
    """Validate a write target and every parent below the repository root."""
    path = root / relative
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"Path escapes the repository: {relative}")
    current = root
    for component in path.relative_to(root).parts:
        current = current / component
        if current.is_symlink() or (current.exists() and getattr(current.lstat(), "st_file_attributes", 0)
                                    & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)):
            raise ValueError(f"Refusing linked repository path: {relative}")
    if path.exists() and not path.is_file():
        raise ValueError(f"Expected a regular repository file: {relative}")
    return path


def check(root: Path, write: bool = False) -> list[str]:
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)", version):
        return ["VERSION must contain one normal major.minor.patch version"]
    errors = []
    # Validate both destinations before either manifest can be changed.
    paths = [(name, safe_repo_file(root, name)) for name in MANIFESTS]
    updates = []
    for name, path in paths:
        value = json.loads(path.read_text(encoding="utf-8"))
        if value.get("version") != version:
            if write:
                value["version"] = version
                updates.append((name, json.dumps(value, ensure_ascii=False, indent=2) + "\n"))
            else:
                errors.append(f"{name}: version must be {version}; run --write")
    for name in ("CHANGELOG.md", "CHANGELOG.zh-CN.md"):
        headings = re.findall(r"^## (?:\[)?v([0-9]+\.[0-9]+\.[0-9]+)", (root / name).read_text(encoding="utf-8"), re.M)
        if not headings or headings[0] != version:
            errors.append(f"{name}: first version entry must be v{version}; preserve historical entries")
    for suffix in ("", ".zh-CN"):
        path = root / f"docs/releases/v{version}{suffix}.md"
        if not path.is_file() or not path.read_text(encoding="utf-8").startswith(f"# Research Toolkit v{version}\n"):
            errors.append(f"Missing release notes for v{version}: {path.relative_to(root)}")
    if not errors:
        for name, content in updates:
            safe_repo_file(root, name).write_text(content, encoding="utf-8")
    return errors


def self_test() -> None:
    import tempfile
    import shutil
    with tempfile.TemporaryDirectory() as tmp:
        trial = Path(tmp)
        for name in ("VERSION", *MANIFESTS, "CHANGELOG.md", "CHANGELOG.zh-CN.md"):
            dest = trial / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, dest)
        shutil.copytree(ROOT / "docs/releases", trial / "docs/releases")
        assert not check(trial)
        path = trial / MANIFESTS[0]
        value = json.loads(path.read_text(encoding="utf-8"))
        value["version"] = "0.0.0"
        path.write_text(json.dumps(value), encoding="utf-8")
        assert check(trial)
        assert not check(trial, write=True)
        (trial / "CHANGELOG.zh-CN.md").write_text("# Missing current entry\n", encoding="utf-8")
        assert check(trial, write=True), "Writing mirrors must not invent a changelog"
        (trial / "VERSION").write_text("0.2.3-rc1\n", encoding="utf-8")
        assert check(trial)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        errors = check(ROOT, args.write)
        if errors:
            print("\n".join("FAIL: " + e for e in errors))
            return 1
        if args.self_test:
            self_test()
        print("PASS: VERSION, package manifests, bilingual changelogs and release notes agree")
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print(f"FAIL: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
