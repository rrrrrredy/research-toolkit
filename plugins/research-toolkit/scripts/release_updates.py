"""On-demand comparison of one registered, public, dated release log."""
from __future__ import annotations

from datetime import date
import difflib
from http.client import HTTPSConnection
import ipaddress
import re
import socket
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, HTTPSHandler, ProxyHandler, Request, build_opener

from extract_source_text import extract_html
from record_changes import history, impact_view, rows_from
from check_delivery import reading_evidence_target
from run_observation import now

MAX_BYTES = 4 * 1024 * 1024
SOURCE_TYPES = {"official_release", "release_notes", "changelog"}
DATE = re.compile(r"^(\d{4})(?:年|-)(\d{1,2})(?:月|-)(\d{1,2})日?$")
VERSION = re.compile(r"(?<![\w.])v?(\d+\.\d+(?:\.\d+)*(?:[-+][\w.-]+)?)(?![\w.])")


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # Read only the registered URL; do not follow other pages.


def public_connection(address, timeout, source_address=None):
    targets = socket.getaddrinfo(*address, type=socket.SOCK_STREAM)
    if not targets:
        raise ValueError("url: release-log host resolved to no addresses.")
    for _, _, _, _, target in targets:
        ip = ipaddress.ip_address(target[0])
        ip = getattr(ip, "ipv4_mapped", None) or ip
        if not ip.is_global or ip.is_multicast:
            raise ValueError(f"url: release-log host resolved to a non-public address: {target[0]}.")
    error = None
    for family, kind, protocol, _, target in targets:
        connection = None
        try:
            connection = socket.socket(family, kind, protocol)
            connection.settimeout(timeout)
            if source_address:
                connection.bind(source_address)
            # Connect to the checked numeric address, without another DNS lookup.
            connection.connect(target)
            return connection
        except OSError as exc:
            error = exc
            if connection is not None:
                connection.close()
    raise error


class PublicHTTPSConnection(HTTPSConnection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._create_connection = public_connection


class PublicHTTPSHandler(HTTPSHandler):
    def https_open(self, request):
        # Keep the URL hostname for Host, TLS SNI and certificate verification.
        return self.do_open(PublicHTTPSConnection, request, context=self._context)


def fetch_log(url):
    parsed = urlsplit(url)
    host = (parsed.hostname or "").encode("idna").decode("ascii").rstrip(".").lower()
    if parsed.scheme != "https" or parsed.username is not None or parsed.password is not None or "." not in host:
        raise ValueError("url: use a public HTTPS release-log URL without credentials.")
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        if host.lower().endswith((".local", ".localhost", ".internal")):
            raise ValueError("url: local hosts are not public release logs.")
    else:
        if not address.is_global or address.is_multicast:
            raise ValueError("url: local addresses are not public release logs.")
    authority = f"[{host}]" if ":" in host else host
    if parsed.port is not None:
        authority += f":{parsed.port}"
    url = parsed._replace(netloc=authority).geturl()
    request = Request(url, headers={"User-Agent": "Research-Toolkit", "Accept-Encoding": "identity"})
    # A proxy could resolve the target elsewhere, bypassing the checked addresses.
    with build_opener(ProxyHandler({}), NoRedirect(), PublicHTTPSHandler()).open(request, timeout=20) as response:
        kind = response.headers.get_content_type()
        if kind not in {"text/html", "text/plain", "text/markdown"}:
            raise ValueError(f"Unsupported content type: {kind}; expected HTML or text release notes.")
        data = response.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise ValueError("Release log exceeds the 4 MiB read limit.")
        encoding = response.headers.get_content_charset()
        return (extract_html(data, encoding=encoding)["text"] if kind == "text/html"
                else data.decode(encoding or "utf-8-sig"))


def release_entries(text):
    """Support date headings followed by a version, including saved web text."""
    if re.search(r"<!doctype html|<html\b", text, re.I):
        text = extract_html(text.encode("utf-8"), encoding="utf-8")["text"]
    if re.search(r"^L\d+:", text, re.M):
        text = re.sub(r"\bL\d+:\s*", "\n", text)
    text = re.sub(r"\ue200.*?\ue201|\[href: [^\]]*\]", "", text)
    lines = []
    for line in text.splitlines():
        line = re.sub(r"^[\s#>*-]+", "", line.replace("\u200b", "")).strip()
        line = " ".join(line.split())
        if line:
            lines.append(line)
    headings = [(i, DATE.fullmatch(line)) for i, line in enumerate(lines) if DATE.fullmatch(line)]
    entries = {}
    for index, (start, match) in enumerate(headings):
        end = headings[index + 1][0] if index + 1 < len(headings) else len(lines)
        block = lines[start + 1:end]
        version = VERSION.search(block[0]) if block else None
        if not version or len(block) < 2:
            raise ValueError(f"Unrecognized release entry after {lines[start]}; expected version and body.")
        published = date(*(int(part) for part in match.groups())).isoformat()
        key = (published, version[1])
        if key in entries:
            raise ValueError(f"Duplicate release date/version: {key}.")
        entries[key] = {"date": published, "date_raw": lines[start], "version": version[1],
                        "title": block[0], "content": block[1:]}
    if not entries:
        raise ValueError("No dated release entries found; expected YYYY-MM-DD or YYYY年MM月DD日 followed by a version and body. Login/JavaScript-only pages are unsupported.")
    return entries


def compare_entries(previous, current):
    # Compare the latest saved date and newer entries. Older history may be paginated.
    latest = max(key[0] for key in previous)
    baseline = {key: value for key, value in previous.items() if key[0] == latest}
    if not baseline.keys() <= current.keys():
        raise ValueError("Latest saved release is absent from the fetched page; cannot establish an unchanged baseline.")
    changes = []
    for key, entry in current.items():
        if key[0] < latest:
            continue
        before = previous.get(key)
        added, removed = [], []
        if before is None:
            added = entry["content"]
        else:
            for tag, a, b, c, d in difflib.SequenceMatcher(None, before["content"], entry["content"], autojunk=False).get_opcodes():
                if tag in {"insert", "replace"}:
                    added.extend(entry["content"][c:d])
                if tag in {"delete", "replace"}:
                    removed.extend(before["content"][a:b])
        if added or removed:
            changes.append({"date": entry["date"], "date_raw": entry["date_raw"], "version": entry["version"],
                            "kind": "new_entry" if before is None else "updated_entry",
                            "added_content": added, "removed_content": removed})
    return changes, latest


def check_updates(workspace, task, source_id):
    from research_workflow import safe_path, task_root
    root = task_root(workspace, task)
    sources = rows_from(safe_path(root, "data/source_registry.csv").read_bytes(), "sources")
    if source_id not in sources:
        raise ValueError(f"data/source_registry.csv source_id: {source_id!r} is not registered.")
    source = sources[source_id]
    if source.get("source_type") not in SOURCE_TYPES:
        raise ValueError(f"data/source_registry.csv {source_id}.source_type: only registered official_release/release_notes/changelog sources are supported.")
    result = {"source_id": source_id, "url": source.get("url"), "checked_at": now()}
    phase = "baseline"
    try:
        name = source.get("evidence_path") or reading_evidence_target(source.get("read_evidence"))
        if not name:
            raise ValueError(f"data/source_registry.csv {source_id}.evidence_path: provide a saved task-relative release-log text file, e.g. sources/releases.md.")
        previous = release_entries(safe_path(root, name).read_text(encoding="utf-8-sig"))
        phase = "fetch"
        text = fetch_log(source["url"])
        phase = "parse"
        current = release_entries(text)
        phase = "compare"
        changes, latest = compare_entries(previous, current)
        result.update(ok=True, status="changed" if changes else "unchanged", baseline_path=name,
                      baseline_latest_date=latest, changes=changes,
                      scope="Latest saved release date and newer entries only; dates are source labels, not exact publication times. No records, reading status, report or conclusions are changed.")
        if not changes:
            return result
        phase = "locations"
        events = history(root)
        artifact = next((e["artifact"] for e in reversed(events) if e.get("artifact")), None)
        impact = impact_view(root, {"source_files": {source_id: {"status": "changed"}}}, artifact)
        result.update(artifact=artifact, affected_claims=impact["affected_claims"],
                      unlinked_source_ids=impact["unlinked_source_ids"],
                      location_scope="Existing literal claim/source-link matches; inspect these passages before deciding what to revise.")
        # The agent can retain this excerpt using the existing source/save workflow after reading it.
        result["current_excerpt"] = "\n\n".join("\n".join([e["date_raw"], e["title"], *e["content"]])
            for key, e in current.items() if key[0] >= latest)
        return result
    except (OSError, ValueError, LookupError) as exc:
        return {**result, "ok": False, "status": "failed", "phase": phase, "error": str(exc)}
