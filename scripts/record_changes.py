"""Advisory record differences and reading locations, reusing the activity log."""
from __future__ import annotations
import json
import re
from check_delivery import inspect_csv_text, inspect_jsonl_text, reading_evidence_target, sha256_file

REGISTRIES = {"sources": ("data/source_registry.csv", "source_id"),
              "claims": ("data/claims_registry.csv", "claim_id"),
              "requirements": ("state/requirements.jsonl", "requirement_id")}
SCOPE = ("Latest successful record-save batch; report locations are literal source-link or claim-text matches, and research-output links use saved input and unit dependencies in the explicit main draft (latest registered draft for legacy tasks), "
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


def requirements_for_units(rows, unit_ids=None):
    """Keep global requirements and explicit unit assignments, never infer scope."""
    if unit_ids is None:
        return list(rows)
    selected = set(unit_ids)
    result = []
    for row in rows:
        assigned = row.get('unit_ids', [])
        if (not isinstance(assigned, list) or any(not isinstance(value, str) or not
                re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', value) for value in assigned)):
            raise ValueError(f"Requirement {row.get('requirement_id', row.get('id', '?'))}.unit_ids: use research-unit IDs as a list; omit it or use [] for a global requirement.")
        if not assigned or selected.intersection(assigned):
            result.append(row)
    return result


def input_digest(root, name):
    """Bind selected records without invalidating work on unrelated registry edits."""
    from task_storage import digest, safe_path
    if not isinstance(name, str):
        raise ValueError('Input reference must be a task-relative path or record:collection:ID.')
    if not name.startswith('record:'):
        return sha256_file(safe_path(root, name))
    parts = name.split(':', 2)
    if len(parts) != 3 or parts[1] not in REGISTRIES or not parts[2]:
        raise ValueError(f'{name}: use record:sources:S1, record:claims:C1 or record:requirements:effective.')
    kind, identity = parts[1:]
    path = safe_path(root, REGISTRIES[kind][0])
    rows = rows_from(path.read_bytes() if path.exists() else b'', kind)
    if kind == 'requirements':
        # Fulfilment is not applicability. A completed comparison or audience
        # requirement remains binding; retiring/replacing it changes this input.
        def meaning(row):
            result = {k: v for k, v in row.items() if k not in {'status', 'evidence'}}
            result['status'] = row.get('status') if row.get('status') in {
                'waived', 'out_of_scope', 'accepted_limitation'} else 'active'
            return result
        if identity == 'effective':
            return digest({key: meaning(row) for key, row in rows.items()})
        if identity.startswith('effective@'):
            unit_ids = identity.removeprefix('effective@').split(',')
            if any(not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', value) for value in unit_ids):
                raise ValueError(f'{name}: use the requirement binding returned by work_context.inputs.')
            selected = requirements_for_units(rows.values(), unit_ids)
            return digest({row.get('requirement_id', row.get('id')): meaning(row) for row in selected})
        if identity in rows:
            return digest(meaning(rows[identity]))
    elif identity in rows:
        return digest(rows[identity])
    raise ValueError(f'{name}: selected record is missing.')


def history(root):
    from task_storage import safe_path
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
    from task_storage import safe_path
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


def claim_source_ids(row, registered):
    """Reuse review-input ID rules; counter-evidence prose is not an inferred link."""
    supporting = set(re.split(r"[;,|\s]+", row.get("supporting_sources", "").strip())) - {""}
    counter = set(re.split(r"[;,|\s]+", row.get("counter_evidence", "").strip())) & set(registered)
    return supporting | counter


def impact_view(root, summary, artifact):
    from task_storage import safe_path
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
        related = claim_source_ids(row, sources)
        linked = related & source_ids
        if not linked and key not in claim_ids:
            continue
        matches = []
        for number, line, heading in locations:
            reasons = []
            if row.get("claim") and row["claim"] in line:
                reasons.append("claim_text")
            for sid in sorted(related if key in claim_ids else linked):
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
    from task_context import research_outputs
    from task_storage import load
    progress = load(root, 'state/progress.json') if (root / 'state/progress.json').is_file() else {}
    outputs = research_outputs(root, [], progress)
    affected_outputs = [{key: item[key] for key in ('path', 'unit_id', 'question', 'changed_inputs', 'changed_since_save', 'dependencies', 'artifact_snapshot') if key in item}
                        for item in outputs if item['changed_inputs'] or item['changed_since_save']
                        or 'dependency_version_changed' in item.get('readiness_issues', []) or any(
                            any(issue in {'inputs_changed', 'artifact_changed', 'dependency_version_changed', 'dependency_pending'} for issue in dependency['issues'])
                            for dependency in item['dependencies'])]
    return {"records": records, "source_files": summary.get("source_files", {}), "artifact": artifact,
            "affected_claims": affected, "unlinked_source_ids": sorted(source_ids - {sid for a in affected for sid in a["changed_source_ids"]}),
            "affected_outputs": affected_outputs,
            "scope": SCOPE}


def latest_changes(root):
    try:
        from task_storage import load
        events = history(root)
        latest = next((e for e in reversed(events) if "record_changes" in e), None)
        if latest is None:
            return {"available": False, "scope": SCOPE}
        current = load(root, "state/progress.json").get("current_artifact", {})
        artifact = current.get("path") or next((e["artifact"] for e in reversed(events) if e.get("artifact")), None)
        return {"available": True, "operation_id": latest["operation_id"], "saved_at": latest.get("finished_at"),
                **impact_view(root, latest["record_changes"], artifact)}
    except (OSError, ValueError, TypeError, KeyError, AttributeError):
        return {"available": False, "warning": "Change summary unavailable; existing research and delivery checks still apply.", "scope": SCOPE}
