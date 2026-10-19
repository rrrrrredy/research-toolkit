"""Advisory record differences and reading locations, reusing the activity log."""
from __future__ import annotations
import json
import re
from check_delivery import inspect_csv_text, inspect_jsonl_text, reading_evidence_target, sha256_file

REGISTRIES = {"sources": ("data/source_registry.csv", "source_id"),
              "claims": ("data/claims_registry.csv", "claim_id"),
              "requirements": ("state/requirements.jsonl", "requirement_id")}
SCOPE = ("Latest successful record-save batch; locations are literal source-link or claim-text matches in the latest registered draft, "
         "not proof of semantic impact or complete coverage. Source files are compared only when their records are saved; no remote monitoring. "
         "No changes to review or delivery checks.")


def rows_from(content, kind):
    name, identity = REGISTRIES[kind]
    text = (content or b"").decode("utf-8-sig")
    if kind == "requirements":
        rows, errors = inspect_jsonl_text(text, name)
    else:
        rows, errors = inspect_csv_text(text, name, (identity,), identity) if text else ([], [])
    if errors:
        raise ValueError("; ".join(errors))
    return {r.get(identity, r.get("id")): {k: v for k, v in r.items() if v != ""} for r in rows}


def history(root):
    from research_workflow import safe_path
    path = safe_path(root, "logs/activity.jsonl")
    events = []
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                row = json.loads(line)
                if isinstance(row, dict) and row.get("outcome") == "saved":
                    events.append(row)
            except ValueError:
                continue
    return events


def source_files(root, row):
    from research_workflow import safe_path
    files = {}
    for field in ("evidence_path", "read_evidence"):
        # evidence_path is an explicit file path, including original formats
        # outside the reading-locator parser's recognized text extensions.
        if field == "evidence_path" and row.get(field):
            try:
                path = safe_path(root, row[field])
                if path.is_file():
                    files[row[field]] = sha256_file(path)
                    continue
            except (ValueError, OSError):
                pass
        try:
            name = reading_evidence_target(row.get(field))
            if name:
                path = safe_path(root, name)
                if path.is_file():
                    files[name] = sha256_file(path)
        except (ValueError, OSError):
            continue  # The existing reading validator handles invalid references.
    return files


def summarize_save(root, plans, ids, events):
    """Compare supplied rows, not every record in the task. Called after commit."""
    prior_files = {}
    for event in events:
        prior_files.update(event.get("record_changes", {}).get("source_observations", {}))
    by_path = {name: (content, original) for name, content, original in plans}
    summary = {"records": {}, "source_files": {}, "source_observations": {}}
    for kind, touched in ids.items():
        content, original = by_path[REGISTRIES[kind][0]]
        new = rows_from(content, kind)
        try:
            old = rows_from(original, kind)
        except ValueError:
            old = None  # Explicit format recovery: do not invent the old row set.
        diff = {"added": [], "updated": [], "unchanged": [], "removed": [], "recovered": []}
        for key in touched:
            category = ("recovered" if old is None else "added" if key not in old else
                        "unchanged" if new[key] == old[key] else "updated")
            diff[category].append(key)
        diff["removed"] = sorted(set(old or {}) - set(new))
        summary["records"][kind] = diff
        if kind == "sources":
            for key in touched:
                files = source_files(root, new[key])
                previous = prior_files.get(key)
                summary["source_observations"][key] = files
                summary["source_files"][key] = {
                    "status": "first_observation" if previous is None else "changed" if files != previous else "unchanged",
                    "paths": sorted(files), "previous_paths": sorted(previous or {})}
    return summary


def repeated_text_positions(texts, *, minimum_chars=24, minimum_count=2):
    """Group exact text, retaining every occurrence; callers own normalization."""
    positions = {}
    for index, text in enumerate(texts):
        if len(re.sub(r"\s+", "", text)) >= minimum_chars:
            positions.setdefault(text, []).append(index)
    return {text: indices for text, indices in positions.items() if len(indices) >= minimum_count}


def paragraph_span(lines, index):
    """Locate one literal block, bounded by blank lines/headings."""
    start = end = index
    if not lines[index].startswith("#"):
        while start > 0 and lines[start - 1].strip() and not lines[start - 1].startswith("#"):
            start -= 1
        while end + 1 < len(lines) and lines[end + 1].strip() and not lines[end + 1].startswith("#"):
            end += 1
    return start, end


def paragraph_context(lines, index):
    """Return literal text blocks around a match, bounded by blank lines/headings."""
    start, end = paragraph_span(lines, index)
    first, last = start, end
    before = start - 1
    while before >= 0 and not lines[before].strip():
        before -= 1
    if before >= 0 and not lines[index].startswith("#") and not lines[before].startswith("#"):
        first, _ = paragraph_span(lines, before)
    after = end + 1
    while after < len(lines) and not lines[after].strip():
        after += 1
    if after < len(lines) and not lines[after].startswith("#"):
        _, last = paragraph_span(lines, after)
    return {"start_line": first + 1, "end_line": last + 1,
            "text": "\n".join(lines[first:last + 1])}


def impact_view(root, summary, artifact):
    from research_workflow import safe_path
    records = summary.get("records", {})
    changed = lambda kind: sorted({key for cat, keys in records.get(kind, {}).items() if cat != "unchanged" for key in keys})
    source_ids = set(changed("sources")) | {k for k, v in summary.get("source_files", {}).items() if v["status"] == "changed"}
    claim_ids = set(changed("claims"))
    sources = rows_from(safe_path(root, REGISTRIES["sources"][0]).read_bytes(), "sources")
    claims = rows_from(safe_path(root, REGISTRIES["claims"][0]).read_bytes(), "claims")
    lines = safe_path(root, artifact).read_text(encoding="utf-8").splitlines() if artifact else []
    locations = []
    heading = ""
    for number, line in enumerate(lines, 1):
        if line.startswith("#"):
            heading = line.lstrip("# ")
        locations.append((number, line, heading))
    affected = []
    contexts = {}
    for key, row in claims.items():
        supporting = set(re.split(r"[;,|\s]+", row.get("supporting_sources", "").strip())) - {""}
        linked = supporting & source_ids
        if not linked and key not in claim_ids:
            continue
        matches = []
        for number, line, heading in locations:
            reasons = []
            if row.get("claim") and row["claim"] in line:
                reasons.append("claim_text")
            for sid in sorted(supporting if key in claim_ids else linked):
                url = sources.get(sid, {}).get("url")
                if (url and re.search(re.escape(url) + r"(?=$|[\s)<>\]\"'])", line)) or re.search(r"\[" + re.escape(sid) + r"\]", line):
                    reasons.append("source_link:" + sid)
            if reasons:
                location = {"line": number, "heading": heading, "matched_by": reasons, "text": line}
                context = paragraph_context(lines, number - 1)
                identity = (artifact, context["start_line"], context["end_line"], context["text"])
                if identity in contexts:
                    location["context_ref"] = contexts[identity]
                else:
                    location["context"] = context
                    # References always target an inline context in this same response.
                    contexts[identity] = {"claim_id": key, "line": number}
                matches.append(location)
        affected.append({"claim_id": key, "claim": row.get("claim"), "changed_source_ids": sorted(linked),
                         "locations": matches, "location_status": "matched" if matches else "not_located"})
    return {"records": records, "source_files": summary.get("source_files", {}), "artifact": artifact,
            "affected_claims": affected, "unlinked_source_ids": sorted(source_ids - {sid for a in affected for sid in a["changed_source_ids"]}),
            "scope": SCOPE}


def latest_changes(root):
    try:
        events = history(root)
        latest = next((e for e in reversed(events) if "record_changes" in e), None)
        if latest is None:
            return {"available": False, "scope": SCOPE}
        artifact = next((e["artifact"] for e in reversed(events) if e.get("artifact")), None)
        return {"available": True, "operation_id": latest["operation_id"], "saved_at": latest.get("finished_at"),
                **impact_view(root, latest["record_changes"], artifact)}
    except (OSError, ValueError, TypeError, KeyError, AttributeError):
        return {"available": False, "warning": "Change summary unavailable; existing research and delivery checks still apply.", "scope": SCOPE}
