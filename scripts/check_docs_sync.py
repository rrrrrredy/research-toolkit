#!/usr/bin/env python3
"""Check or refresh the copyable SKILL.md block in docs/framework.html."""

from __future__ import annotations

import re
import json
import argparse
import html
from pathlib import Path


START_MARKER = '<pre id="skilltext"><code>'
END_MARKER = "</code></pre>"


def normalize(text: str) -> str:
    """Ignore platform line endings and insignificant trailing blank lines."""

    return text.replace("\r\n", "\n").rstrip("\n") + "\n"


def split_embedded_block(page: str) -> tuple[str, str, str]:
    if page.count(START_MARKER) != 1:
        raise ValueError(f"expected exactly one {START_MARKER!r} marker")

    before, remainder = page.split(START_MARKER, 1)
    if remainder.count(END_MARKER) != 1:
        raise ValueError(f"expected exactly one {END_MARKER!r} marker after the start marker")

    embedded, after = remainder.split(END_MARKER, 1)
    return before, embedded, after


def sync_section(path, marker, body, write):
    source = path.read_text(encoding="utf-8")
    start, end = f"<!-- {marker} -->", f"<!-- /{marker} -->"
    if source.count(start) != 1 or source.count(end) != 1:
        raise ValueError(f"{path}: missing {marker} section")
    before, rest = source.split(start)
    _, after = rest.split(end)
    desired = before + start + "\n" + body + "\n" + end + after
    if source != desired:
        if not write:
            raise ValueError(f"{path}: stale {marker}, use --write")
        path.write_text(desired, encoding="utf-8", newline="\n")


def check_language_navigation(root, write=False):
    from urllib.parse import unquote, urlsplit
    docs = root / "docs"
    en = {p.relative_to(docs/"en") for p in (docs/"en").rglob("*.md")}
    zh = {p.relative_to(docs/"zh") for p in (docs/"zh").rglob("*.md")}
    if not en or en != zh:
        raise ValueError("English and Chinese navigation have unmatched paths: " + str(en ^ zh))
    navigation = json.loads((docs/"navigation.json").read_bytes())
    studies = json.loads((docs/"evaluation-results.json").read_bytes())["studies"]
    for language in ("en", "zh"):
        menu = "\n".join(f"- [{row[language]}]({row['path']})" for row in navigation)
        sync_section(docs/language/"README.md", "navigation", menu, write)
        zh_page = language == "zh"
        table = ["| 可核查的结果 | 能从这份证据知道什么 | 原始材料 |" if zh_page else
                 "| Recorded result | What the evidence establishes | Original material |", "| --- | --- | --- |"]
        for study in studies:
            details = study[language]
            sources = " · ".join(f"[{s['label']}]({s['href']})" for s in details["sources"])
            table.append(f"| {details['label'].format_map(study['counts'])} | {details['scope']} | {sources} |")
        index = docs/("evaluation-status.zh-CN.md" if zh_page else "evaluation-status.md")
        sync_section(index, "evidence-index", "\n".join(table), write)
        for name in en:
            page = docs / language / name
            source = page.read_text(encoding="utf-8")
            for href in re.findall(r'\]\(([^)]+)\)', source):
                target = urlsplit(href)
                if not target.scheme and target.path and not (page.parent / unquote(target.path)).is_file():
                    raise ValueError(f"{page}: missing navigation target {href}")
            if name != Path("README.md") and name.name == "README.md":
                if name.as_posix() not in (docs / language / "README.md").read_text(encoding="utf-8"):
                    raise ValueError(f"{name} missing from {language} navigation")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="refresh the HTML block from SKILL.md")
    parser.add_argument("--skill", default="SKILL.md")
    parser.add_argument("--html", default="docs/framework.html")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    check_language_navigation(repo_root, args.write)
    skill_path = (repo_root / args.skill).resolve()
    html_path = (repo_root / args.html).resolve()

    skill_text = skill_path.read_text(encoding="utf-8")
    page_text = html_path.read_text(encoding="utf-8")

    try:
        before, embedded_html, after = split_embedded_block(page_text)
    except ValueError as error:
        print(f"docs sync check failed: {error}")
        return 1

    embedded_text = html.unescape(embedded_html)
    if normalize(skill_text) == normalize(embedded_text):
        print("docs sync check passed: Full SKILL.md matches SKILL.md")
        return 0

    if not args.write:
        print("docs sync check failed: Full SKILL.md differs from SKILL.md")
        print("Run: python scripts/check_docs_sync.py --write")
        return 1

    rendered = html.escape(normalize(skill_text).rstrip("\n"), quote=False)
    updated_page = before + START_MARKER + rendered + "\n" + END_MARKER + after
    html_path.write_text(updated_page, encoding="utf-8")
    print(f"Updated {html_path.relative_to(repo_root)} from {skill_path.relative_to(repo_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
