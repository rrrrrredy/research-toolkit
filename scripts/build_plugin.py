#!/usr/bin/env python3
"""Build or verify the self-contained plugin from the shared research files."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
from check_version import check as check_version, safe_repo_file

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT/"plugins/research-toolkit"
RUNTIME = ["profile_policy.py", "check_delivery.py", "check_review_completion.py", "research_workflow.py", "research_records.py", "record_changes.py", "release_updates.py", "extract_source_text.py", "run_observation.py", "review_runner.py", "review_process.py", "task_lock.py", "task_context.py"]
MANIFEST = ".generated-files.json"


def digest(content: bytes) -> str:
    return hashlib.sha256(content.replace(b"\r\n", b"\n")).hexdigest()


def managed_name(relative: str) -> bool:
    parts = PurePosixPath(relative).parts
    return (relative in {"VERSION", "SKILL.md", "SKILL.zh-CN.md", "LICENSE", "requirements-mcp.txt"}
            or len(parts) == 2 and parts[0] in {"references", "docs", "scripts"}
            and parts[1] not in {".", ".."} and relative == "/".join(parts)
            and "\\" not in relative
            and PurePosixPath(relative).suffix == (".py" if parts[0] == "scripts" else ".md"))


def safe_target(relative: str) -> Path:
    """Never read, replace or unlink through a plugin symlink/junction."""
    if relative != MANIFEST and not managed_name(relative):
        raise ValueError(f"Not a managed plugin path: {relative!r}")
    path = PLUGIN / relative
    if not path.resolve().is_relative_to(PLUGIN.resolve()):
        raise ValueError(f"Plugin path escapes its directory: {relative}")
    if not PLUGIN.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError("Plugin directory escapes the repository")
    return safe_repo_file(ROOT, path.relative_to(ROOT).as_posix())


def payload() -> dict[str, bytes]:
    paths = [ROOT/"VERSION", ROOT/"SKILL.md", ROOT/"SKILL.zh-CN.md", ROOT/"LICENSE", *sorted((ROOT/"references").glob("*.md"))]
    paths += [ROOT/"scripts"/name for name in RUNTIME]
    paths += [ROOT/"docs"/name for name in (
        "compatibility.md", "compatibility.zh-CN.md",
        "review-completion.md", "review-completion.zh-CN.md",
        "usage-modes.md", "usage-modes.zh-CN.md",
        "delivery-verification.md", "delivery-verification.zh-CN.md")]
    mcp = ROOT/"scripts/research_mcp.py"
    if mcp.is_file():
        paths.extend([mcp, ROOT/"requirements-mcp.txt"])
    return {path.relative_to(ROOT).as_posix(): path.read_bytes() for path in paths}


def build(check=False) -> list[str]:
    desired = payload()
    manifest_path = safe_target(MANIFEST)
    previous = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if not isinstance(manifest, dict) or manifest.get("schema_version") != 1 or not isinstance(manifest.get("files"), dict):
            raise ValueError("Invalid generated-file manifest")
        previous = manifest["files"]
        for relative, checksum in previous.items():
            safe_target(relative)
            if not isinstance(checksum, str) or len(checksum) != 64 or any(c not in "0123456789abcdef" for c in checksum):
                raise ValueError(f"Invalid generated-file checksum: {relative}")
    different = []
    removals = []
    writes = []
    # Plan and validate everything before changing any payload files.
    for relative in sorted(previous.keys() - desired.keys()):
        path = safe_target(relative)
        different.append(relative + " (obsolete)")
        if path.exists():
            if digest(path.read_bytes()) != previous[relative]:
                raise ValueError(f"Obsolete generated file was modified; preserve and inspect it: {relative}")
            removals.append(path)
    for relative, content in sorted(desired.items()):
        path = safe_target(relative)
        matches = path.is_file() and digest(path.read_bytes()) == digest(content)
        if path.exists() and relative not in previous and not matches:
            raise ValueError(f"Unowned file conflicts with generated content; preserve and inspect it: {relative}")
        if not matches:
            different.append(relative)
            writes.append((path, content))
    manifest_bytes = (json.dumps({"schema_version": 1, "files": {name: digest(content) for name, content in sorted(desired.items())}}, indent=2) + "\n").encode("utf-8")
    if not manifest_path.exists() or digest(manifest_path.read_bytes()) != digest(manifest_bytes):
        different.append(MANIFEST)
    # Untracked content is not proof of ownership, even inside a generated folder.
    for folder in ("references", "docs", "scripts"):
        for path in sorted((PLUGIN / folder).glob("*")):
            relative = path.relative_to(PLUGIN).as_posix()
            if relative not in previous and relative not in desired and managed_name(relative):
                print(f"Preserved unmanaged file (ownership unknown): {relative}")
    if not check:
        for path in removals:
            safe_target(path.relative_to(PLUGIN).as_posix()).unlink()
        for path, content in writes:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        if MANIFEST in different:
            manifest_path.parent.mkdir(parents=True, exist_ok=True)
            manifest_path.write_bytes(manifest_bytes)
    return different


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        # Validate the entire generated-file plan before version synchronization writes.
        # check_version also validates every version destination before writing any of them.
        different = build(check=True)
        errors = check_version(ROOT, write=not args.check)
        if errors:
            print("\n".join(errors))
            return 1
        if not args.check:
            different = build()
    except (OSError, ValueError, TypeError) as exc:
        print(f"Plugin build blocked: {exc}")
        return 1
    if args.check and different:
        print("Plugin payload differs: "+", ".join(different))
        return 1
    print(f"Plugin payload {'verified' if args.check else 'built'}: {len(payload())} shared files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
