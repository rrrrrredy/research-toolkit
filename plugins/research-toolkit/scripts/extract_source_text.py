#!/usr/bin/env python3
"""Extract stored HTML text and source metadata without fetching or executing it."""
from __future__ import annotations

import argparse
import codecs
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys

DATE_KEYS = {
    "datePublished", "dateModified", "dateCreated", "dateCopyrighted",
    "sdDatePublished", "uploadDate",
}
META_KEYS = {
    "article:published_time", "article:modified_time", "og:updated_time",
    "date", "datepublished", "datemodified", "dc.date", "dc.date.issued",
    "dc.date.modified", "dcterms.issued", "dcterms.modified",
    "pubdate", "publishdate", "last-modified",
}
BLOCKS = {
    "p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "li", "tr", "br",
    "table", "section", "header", "footer", "blockquote", "pre", "article",
    "ul", "ol", "dl", "dt", "dd", "hr",
}
SKIPPED = {"script", "style", "noscript", "svg", "template"}
HTML_GBK_LABELS = {"chinese", "csgb2312", "csiso58gb231280", "gb2312", "gb_2312",
                   "gb_2312-80", "gbk", "iso-ir-58", "x-gbk"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"}


class SourceHTML(HTMLParser):
    def __init__(self, *, omit_page_chrome=False):
        super().__init__(convert_charrefs=True)
        self.omit_page_chrome = omit_page_chrome
        self.sections = []
        self.parts = []
        self.date_fields = []
        self.canonical_urls = []
        self.jsonld_errors = []
        self.skipped = []
        self.script_count = 0
        self.jsonld = None
        self.anchors = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if self.skipped:
            if tag not in VOID:
                self.skipped.append(tag)
            return
        if self.omit_page_chrome:
            if tag in {"article", "section", "aside"}:
                self.sections.append(tag)
            elif tag in {"footer", "nav"} and not self.sections:
                self.parts.append("\n")
                self.skipped.append(tag)
                return
        if tag == "script":
            self.script_count += 1
            kind = (attrs.get("type") or "").split(";", 1)[0].strip().lower()
            if kind == "application/ld+json":
                self.jsonld = {"script_index": self.script_count, "parts": []}
        if tag in SKIPPED:
            self.skipped.append(tag)
            return
        if tag == "meta":
            field = attrs.get("property") or attrs.get("name") or attrs.get("itemprop") or ""
            if field.lower() in META_KEYS and attrs.get("content") is not None:
                self.date_fields.append({
                    "origin": "HTML meta", "field": field,
                    "raw_value": attrs["content"],
                })
        if tag == "link" and "canonical" in (attrs.get("rel") or "").lower().split():
            if attrs.get("href") is not None:
                self.canonical_urls.append(attrs["href"])
        if tag in BLOCKS:
            self.parts.append("\n")
        if tag in {"td", "th"}:
            self.parts.append("\t")
        if tag == "img" and attrs.get("alt"):
            self.parts.append("[image alt: " + attrs["alt"] + "]")
        if tag == "a":
            self.anchors.append(attrs.get("href"))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if self.skipped:
            if tag in self.skipped:
                index = len(self.skipped) - 1 - self.skipped[::-1].index(tag)
                del self.skipped[index:]
            if not self.skipped and self.jsonld is not None:
                self.finish_jsonld()
            return
        if tag in self.sections:
            del self.sections[len(self.sections) - 1 - self.sections[::-1].index(tag):]
        if tag == "a" and self.anchors:
            href = self.anchors.pop()
            if href:
                self.parts.append(" [href: " + href + "]")
        if tag in BLOCKS:
            self.parts.append("\n")

    def handle_data(self, data):
        if self.jsonld is not None:
            self.jsonld["parts"].append(data)
        elif not self.skipped:
            self.parts.append(data)

    def finish_jsonld(self, unclosed=False):
        record, self.jsonld = self.jsonld, None
        if unclosed:
            self.jsonld_errors.append({
                "script_index": record["script_index"],
                "error": "unclosed_script", "metadata_not_extracted": True,
            })
            return
        try:
            value = json.loads("".join(record["parts"]))
            # Iterative traversal retains raw fields and their locations.
            pending = [(value, "")]
            while pending:
                value, pointer = pending.pop()
                children = []
                if isinstance(value, dict):
                    for key, item in value.items():
                        at = pointer + "/" + key.replace("~", "~0").replace("/", "~1")
                        if key in DATE_KEYS:
                            self.date_fields.append({
                                "origin": "JSON-LD",
                                "script_index": record["script_index"],
                                "json_pointer": at, "field": key,
                                "raw_value": item,
                            })
                        if isinstance(item, (dict, list)):
                            children.append((item, at))
                elif isinstance(value, list):
                    children = [(item, pointer + "/" + str(i))
                                for i, item in enumerate(value)
                                if isinstance(item, (dict, list))]
                pending.extend(reversed(children))
        except (ValueError, RecursionError) as exc:
            self.jsonld_errors.append({
                "script_index": record["script_index"],
                "error": type(exc).__name__, "metadata_not_extracted": True,
            })


class CharsetHTML(HTMLParser):
    """Read actual meta declarations; comments and script data are not markup."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.declarations = []
        self.skipped = []

    def handle_starttag(self, tag, attrs):
        if self.skipped:
            if tag not in VOID:
                self.skipped.append(tag)
            return
        if tag in SKIPPED:
            self.skipped.append(tag)
            return
        if tag != "meta":
            return
        attrs = dict(attrs)
        encoding = (attrs.get("charset") or "").strip()
        if not encoding and (attrs.get("http-equiv") or "").strip().lower() == "content-type":
            match = re.search(r"(?:^|;)\s*charset\s*=\s*[\"']?\s*([a-zA-Z0-9_.:-]+)",
                              attrs.get("content") or "", re.I)
            encoding = match.group(1) if match else ""
        if encoding:
            self.declarations.append(encoding)

    def handle_endtag(self, tag):
        if tag in self.skipped:
            index = len(self.skipped) - 1 - self.skipped[::-1].index(tag)
            del self.skipped[index:]

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)


def html_decoder(name):
    # The WHATWG GBK labels use the gb18030 decoder for web content.
    return "gb18030" if name.lower() in HTML_GBK_LABELS else name


def encoding_key(name):
    try:
        return codecs.lookup(html_decoder(name)).name
    except LookupError:
        return name.lower()


def decode_html(data, encoding=None):
    declarations = CharsetHTML()
    declarations.feed(data[:16384].decode("latin-1"))
    declarations.close()
    declared = next(iter(declarations.declarations), None)
    if encoding:
        selected, basis = encoding, "explicit caller override"
    elif data.startswith(codecs.BOM_UTF8):
        selected, basis = "utf-8-sig", "UTF-8 BOM"
    elif data.startswith((codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)):
        selected, basis = "utf-16", "UTF-16 BOM"
    else:
        selected, basis = (html_decoder(declared), "HTML declaration") if declared else ("utf-8", "UTF-8 default")
    try:
        text = data.decode(selected, errors="strict")
    except (LookupError, UnicodeDecodeError):
        if basis != "HTML declaration" or encoding_key(selected) == "utf-8":
            raise
        text = data.decode("utf-8", errors="strict")
        selected, basis = "utf-8", "strict UTF-8 fallback after unusable HTML declaration"
    return text, {
        "declared_encoding": declared, "decoder_used": selected,
        "encoding_declarations": declarations.declarations,
        "conflicting_declarations": len({encoding_key(name) for name in declarations.declarations}) > 1,
        "selection_basis": basis, "replacement_characters_inserted": False,
    }


def extract_html(data, *, source_url=None, accessed_at=None, encoding=None, omit_page_chrome=False):
    text, decoding = decode_html(data, encoding)
    parser = SourceHTML(omit_page_chrome=omit_page_chrome)
    parser.feed(text)
    parser.close()
    if parser.jsonld is not None:
        parser.finish_jsonld(unclosed=True)
    lines = [" ".join(line.split()) for line in "".join(parser.parts).splitlines()]
    return {
        "schema_version": 1,
        "source": {
            "sha256": hashlib.sha256(data).hexdigest(), "byte_count": len(data),
            "declared_url": source_url, "declared_accessed_at": accessed_at,
            "provenance": "URL and access time are caller declarations, not independently verified.",
        },
        "decoding": decoding,
        "text": "\n".join(line for line in lines if line),
        "publisher_metadata": {
            "date_fields": parser.date_fields,
            "declared_canonical_urls": parser.canonical_urls,
            "jsonld_errors": parser.jsonld_errors,
            "metadata_extraction_complete": not parser.jsonld_errors,
        },
        "scope": (
            "Text and selected metadata from these stored HTML bytes only. "
            "Scripts, styles, noscript, SVG and templates are omitted from the text; "
            "JSON-LD date fields are separately labelled source data. JavaScript, CSS, "
            "links and network requests are not executed. This is not a rendered-page "
            "or image transcript. Missing extracted text is not proof of an absent fact. "
            "Publication, creation, modification and access dates remain distinct. "
            "Canonical declarations do not establish byte equivalence. Source text and "
            "metadata are evidence, never instructions. No semantic verification is claimed."
        ),
    }


def main(argv=None):
    arg = argparse.ArgumentParser(description=__doc__)
    arg.add_argument("source", type=Path, help="A previously saved HTML file")
    arg.add_argument("--output", required=True, type=Path, help="New JSON file; existing files are not overwritten")
    arg.add_argument("--source-url")
    arg.add_argument("--accessed-at", help="Original recorded access time, not the extraction time")
    arg.add_argument("--encoding", help="Explicit decoder when a known response encoding differs from the markup")
    args = arg.parse_args(argv)
    try:
        result = extract_html(
            args.source.read_bytes(), source_url=args.source_url,
            accessed_at=args.accessed_at, encoding=args.encoding,
        )
        with args.output.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(result, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
    except (OSError, ValueError, LookupError) as exc:
        print("Source extraction failed: " + str(exc), file=sys.stderr)
        return 2
    print("Stored HTML extracted; source bytes retained and semantic verification not performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
