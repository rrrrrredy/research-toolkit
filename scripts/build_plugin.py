#!/usr/bin/env python3
"""Build or verify the self-contained plugin from the shared research files."""
from __future__ import annotations
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT/"plugins/research-toolkit"
RUNTIME = ["check_delivery.py", "check_review_completion.py", "research_workflow.py", "review_runner.py"]


def payload() -> dict[str, bytes]:
    paths = [ROOT/"SKILL.md", ROOT/"SKILL.zh-CN.md", ROOT/"LICENSE", *sorted((ROOT/"references").glob("*.md"))]
    paths += [ROOT/"scripts"/name for name in RUNTIME]
    paths += [ROOT/"docs"/name for name in (
        "review-completion.md", "review-completion.zh-CN.md",
        "delivery-verification.md", "delivery-verification.zh-CN.md")]
    mcp = ROOT/"scripts/research_mcp.py"
    if mcp.is_file():
        paths.extend([mcp, ROOT/"requirements-mcp.txt"])
    return {path.relative_to(ROOT).as_posix(): path.read_bytes() for path in paths}


def build(check=False) -> list[str]:
    different = []
    for relative, content in payload().items():
        path = PLUGIN/relative
        if not path.is_file() or path.read_bytes().replace(b"\r\n", b"\n") != content.replace(b"\r\n", b"\n"):
            different.append(relative)
            if not check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
    return different


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    different = build(args.check)
    if args.check and different:
        print("Plugin payload differs: "+", ".join(different))
        return 1
    print(f"Plugin payload {'verified' if args.check else 'built'}: {len(payload())} shared files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
