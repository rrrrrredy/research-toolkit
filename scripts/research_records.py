"""Save agent-provided research records without making users edit CSV/JSONL."""
from __future__ import annotations
import csv
import io
import json
import os
import time
import uuid
import hashlib
import re
from check_delivery import (inspect_csv_text, inspect_jsonl_text, length_constraint_errors, sha256_file,
                            has_evidence, REQUIREMENT_DECISION_STATUSES, READING_REQUIREMENTS)
from run_observation import now, record_event

SCHEMAS = {
    "sources": ("data/source_registry.csv", "source_id", "S", "url",
                ["source_id", "title", "url", "source_type", "read_scope", "read_evidence", "evidence_path"]),
    "claims": ("data/claims_registry.csv", "claim_id", "C", "claim",
               ["claim_id", "claim", "claim_type", "supporting_sources", "counter_evidence", "uncertainty"]),
    "requirements": ("state/requirements.jsonl", "requirement_id", "R", "summary", []),
}


def revised_spec(original, previous, updates):
    """Replace known brief values while retaining manually added sections."""
    text = original.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    for key, value in updates.items():
        if previous.get(key) == value:
            continue
        header = f"## {key}\n\n"
        if key not in previous and not re.search(r"(?m)^## " + re.escape(key) + r"\s*$", text):
            text = text.rstrip() + "\n\n" + header + value + "\n"
            continue
        pattern = re.compile(r"(?m)^" + re.escape(header + previous.get(key, "")) + r"(?=\n|$)")
        if len(list(pattern.finditer(text))) != 1:
            raise ValueError(f"brief.{key}: task_spec no longer matches the saved field. Agent: reconcile that field with the actual specification before retrying; retain other sections.")
        text = pattern.sub(lambda _: header + value, text, count=1)
    return text.encode("utf-8")


def merge_records(root, kind, incoming, replace):
    from task_storage import safe_path
    name, identity, prefix, natural_key, defaults = SCHEMAS[kind]
    path = safe_path(root, name)
    original = path.read_bytes() if path.exists() else None
    if not isinstance(incoming, list) or any(not isinstance(row, dict) for row in incoming):
        raise ValueError(f"{kind}: provide a list of objects, not CSV text.")
    columns, rows = list(defaults), []
    if original and not replace:
        text = original.decode("utf-8-sig")
        if defaults:
            rows, errors = inspect_csv_text(text, name, (identity,), identity)
            columns = list(csv.DictReader(io.StringIO(text)).fieldnames or defaults)
        else:
            rows, errors = inspect_jsonl_text(text, name)
            ids = [r.get(identity, r.get("id")) for r in rows]
            if any(not isinstance(i, str) or not i.strip() for i in ids) or len(set(ids)) != len(ids):
                errors.append("Missing or duplicate requirement IDs.")
            for row in rows:
                if identity not in row and "id" in row:
                    row[identity] = row["id"]
        if errors:
            raise ValueError(f"{kind}: {'; '.join(errors)} Agent: recover complete rows and resubmit with replace=['{kind}']; the tool retains the original backup.")
    used = {row[identity] for row in rows}
    touched, ids = set(), []
    for index, patch in enumerate(incoming):
        patch = dict(patch)
        if any(not isinstance(key, str) or not key.strip() for key in patch):
            raise ValueError(f"{kind}[{index}]: field names must be nonempty text.")
        key = patch.get(identity)
        if key is None:
            matches = [r for r in rows if patch.get(natural_key) and r.get(natural_key) == patch[natural_key]]
            if len(matches) > 1:
                raise ValueError(f"{kind}[{index}]: multiple {natural_key} matches; supply {identity} from the saved records.")
            if matches:
                key = matches[0][identity]
            else:
                n = 1
                while f"{prefix}{n}" in used:
                    n += 1
                key = f"{prefix}{n}"
        if not isinstance(key, str) or not key.strip() or key in touched:
            raise ValueError(f"{kind}[{index}].{identity}: provide distinct nonempty IDs in this request.")
        patch[identity] = key
        touched.add(key)
        used.add(key)
        ids.append(key)
        old = next((row for row in rows if row[identity] == key), None)
        row = {**(old or {}), **patch}
        if defaults:
            if kind == "sources":
                row.setdefault("read_scope", "not_read")
                if not isinstance(row["read_scope"], str) or row["read_scope"] not in {"", "not_read", "partial", "abstract", "relevant_sections", "full_text"}:
                    raise ValueError(f"sources[{index}].read_scope: use not_read/partial/abstract/relevant_sections/full_text.")
            for field, value in row.items():
                if field == "supporting_sources" and isinstance(value, list) and all(isinstance(v, str) for v in value):
                    row[field] = ";".join(value)
                elif not isinstance(value, str):
                    raise ValueError(f"{kind}[{index}].{field}: use text" + (" or a source-ID list." if field == "supporting_sources" else "."))
                if field not in columns:
                    columns.append(field)
            required = ("title", "url", "source_type") if kind == "sources" else ("claim", "claim_type")
            for field in required:
                if not row.get(field, "").strip():
                    raise ValueError(f"{kind}[{index}].{field}: provide the actual {field}; existing values are retained on updates.")
        else:
            if not isinstance(row.get("summary", row.get("description")), str):
                raise ValueError(f"requirements[{index}].summary: provide the requirement in plain language.")
            row.setdefault("status", "pending")
            if row["status"] not in {"pending", "open", "in_progress", "blocked", "satisfied", "waived", "out_of_scope", "accepted_limitation"}:
                raise ValueError(f"requirements[{index}].status: use pending/open/in_progress/blocked/satisfied/waived/out_of_scope/accepted_limitation.")
            if row["status"] == "satisfied" and not has_evidence(row.get("evidence")):
                raise ValueError(f"requirements[{index}].evidence: satisfied needs a nonempty evidence string or list; keep pending until checked.")
            if row["status"] in REQUIREMENT_DECISION_STATUSES:
                decision = row.get("user_decision")
                if not isinstance(decision, dict) or not all(isinstance(decision.get(k), str) and decision[k].strip() for k in ("source_turn", "quote")):
                    raise ValueError(f"requirements[{index}].user_decision: retain the user's actual source_turn and quote for this scope decision.")
            if "required_source_ids" in row and (not isinstance(row["required_source_ids"], list)
                    or not row["required_source_ids"] or not all(isinstance(s, str) and s.strip() for s in row["required_source_ids"])):
                raise ValueError(f"requirements[{index}].required_source_ids: use a nonempty list of source IDs.")
            # An explicit user scope decision can retire a legacy obligation
            # without inventing a corrected reading promise for that old row.
            if row["status"] not in REQUIREMENT_DECISION_STATUSES and ("reading_requirement" in row or "required_source_ids" in row):
                if not isinstance(row.get("reading_requirement"), str) or row["reading_requirement"] not in READING_REQUIREMENTS:
                    raise ValueError(f"requirements[{index}].reading_requirement: use full_text or relevant_sections.")
                source_ids = row.get("required_source_ids")
                if (not isinstance(source_ids, list) or not source_ids
                        or not all(isinstance(s, str) and s.strip() for s in source_ids)
                        or len(source_ids) != len(set(source_ids))):
                    raise ValueError(f"requirements[{index}].required_source_ids: use a nonempty list of distinct source IDs.")
            if "length_constraint" in row:
                errors = length_constraint_errors(row["length_constraint"])
                if errors:
                    raise ValueError(f"requirements[{index}].length_constraint: {'; '.join(errors)}")
        if old is None:
            rows.append(row)
        else:
            rows[rows.index(old)] = row
    if defaults:
        stream = io.StringIO(newline="")
        writer = csv.DictWriter(stream, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
        content = stream.getvalue()
    else:
        content = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
    return name, content.encode("utf-8"), original, ids


def save_records(root, sources=None, claims=None, requirements=None, draft=None, replace=None, brief=None):
    from task_storage import safe_path, load
    from research_guidance import BRIEF_FIELDS
    started, stamp, operation_id = time.monotonic(), now(), uuid.uuid4().hex
    event = {"operation": "save", "operation_id": operation_id, "started_at": stamp}
    plans, backups, ids, temporary, committed = [], [], {}, [], []
    try:
        progress = load(root, "state/progress.json")
        old_progress = dict(progress)
        if brief is not None:
            if (not isinstance(brief, dict) or not brief or any(k not in BRIEF_FIELDS for k in brief)
                    or any(not isinstance(v, str) or not v.strip() for v in brief.values())):
                raise ValueError("brief: provide nonempty text updates to question/audience/scope/output/depth/evidence_standard.")
            previous_brief = progress.get("brief", {})
            progress["brief"] = {**previous_brief, **brief}
            if progress["brief"] != previous_brief:
                path = safe_path(root, "state/task_spec.md")
                original_spec = path.read_bytes()
                plans.append(("state/task_spec.md", revised_spec(original_spec, previous_brief, brief), original_spec))
        values = {"sources": sources, "claims": claims, "requirements": requirements}
        replace = [] if replace is None else replace
        if not isinstance(replace, list) or any(k not in SCHEMAS or values[k] is None for k in replace):
            raise ValueError("replace: list only supplied record collections (sources, claims, requirements).")
        for kind, incoming in values.items():
            if incoming is not None:
                name, content, original, ids[kind] = merge_records(root, kind, incoming, kind in replace)
                plans.append((name, content, original))
                if kind in replace and original is not None:
                    backups.append((f"logs/record-backups/{operation_id}/{name}", original, None))
        if draft is not None:
            if not isinstance(draft, dict) or set(draft) - {"path", "content", "complete", "main", "kind", "based_on", "host_task"}:
                raise ValueError("draft: use path, optional content/complete/main/kind/based_on/host_task; complete records draft completeness, not delivery approval.")
            name = draft.get("path")
            path = safe_path(root, name)
            target_name = path.relative_to(root.resolve()).as_posix()
            protected = {"state", "data", "logs", "reviews"}
            if (name.split("/")[0] in protected or target_name.split("/")[0] in protected
                    or path.suffix not in {".md", ".txt"}):
                raise ValueError("draft.path: use a report .md/.txt path outside state/data/logs/reviews, including resolved link targets; for example, reports/draft.md.")
            if type(draft.get("complete", False)) is not bool:
                raise ValueError("draft.complete: use true or false.")
            if type(draft.get("main", False)) is not bool:
                raise ValueError("draft.main: use true or false.")
            if draft.get("kind", "report") not in {"report", "comparison", "review", "analysis"}:
                raise ValueError("draft.kind: use report, comparison, review or analysis (a research contribution).")
            if 'host_task' in draft:
                if not isinstance(draft['host_task'], str) or not draft['host_task'].strip():
                    raise ValueError('draft.host_task: retain the actual host task/session reference as text.')
                event['host_task'] = draft['host_task']
            if 'based_on' in draft:
                if not isinstance(draft['based_on'], dict):
                    raise ValueError('draft.based_on: use the work_context.inputs path-to-SHA256 object.')
                for input_name, checksum in draft['based_on'].items():
                    safe_path(root, input_name)
                    if not isinstance(checksum, str) or not re.fullmatch('[a-f0-9]{64}', checksum):
                        raise ValueError(f'draft.based_on[{input_name}]: use the SHA256 returned in work_context.inputs.')
                event['based_on'] = draft['based_on']
            # Preserve earlier contributions through the existing backup mechanism.
            # A child contribution never implicitly replaces the registered main draft.
            original = path.read_bytes() if path.exists() else None
            content = draft.get("content")
            if "content" not in draft:
                content = path.read_text(encoding="utf-8")
            if not isinstance(content, str) or not content.strip():
                raise ValueError("draft.content: provide nonempty report text or an existing nonempty UTF-8 file.")
            if "content" in draft:
                plans.append((name, content.encode("utf-8"), original))
                if draft.get('kind') == 'analysis' and original is not None and original != content.encode('utf-8'):
                    backups.append((f'logs/record-backups/{operation_id}/{name}', original, None))
            event.update(artifact=name, artifact_kind=draft.get('kind', 'report'),
                         complete_draft=draft.get("complete", False) and draft.get('kind') != 'analysis',
                         time_basis="saved_by_tool" if "content" in draft else "existing_file_observed")
            current = progress.get("current_artifact", {})
            if draft.get("main") or current.get("path") == name:
                normalized = content.replace("\r\n", "\n").replace("\r", "\n")
                progress["current_artifact"] = {"path": name,
                    "sha256": hashlib.sha256(normalized.encode("utf-8")).hexdigest(),
                    "kind": draft.get("kind", current.get("kind", "report") if current.get("path") == name else "report")}
        if not plans and draft is None and brief is None:
            raise ValueError("Supply sources, claims, requirements or a draft to save.")
        if progress != old_progress:
            # Keep historical receipts and reviews intact. An explicit new main
            # draft or brief revision cannot retain a terminal current state.
            if progress.get("stage") in {"final", "review"} or progress.get("status") == "complete":
                progress.update(stage="revise", status="in_progress",
                                next_action="Continue the current work; reconcile affected requirements and review this version before delivery.")
            path = safe_path(root, "state/progress.json")
            plans.append(("state/progress.json", (json.dumps(progress, ensure_ascii=False, indent=2) + "\n").encode("utf-8"), path.read_bytes()))
        # Validate and stage every payload before replacing any current record.
        for name, content, original in backups + plans:
            if content == original:
                continue
            path = safe_path(root, name)
            path.parent.mkdir(parents=True, exist_ok=True)
            temp = path.with_name(path.name + "." + operation_id + ".tmp")
            temporary.append(temp)
            with temp.open("xb") as stream:
                stream.write(content)
            committed.append((path, original, False))
        for i, temp in enumerate(temporary):
            path, original, _ = committed[i]
            os.replace(temp, path)
            committed[i] = (path, original, True)
        if draft is not None:
            event["artifact_sha256"] = sha256_file(safe_path(root, draft["path"]))
        event["outcome"] = "saved"
        result = {"ok": True, "saved_ids": ids, "updated_files": [p[0] for p in plans if p[1] != p[2]],
                  "backups": [p[0] for p in backups], "next_action": "Continue the research; existing draft, review and delivery checks still apply."}
        if ids:
            from record_changes import history, summarize_save
            try:
                event["record_changes"] = summarize_save(root, plans, ids, history(root))
            except (OSError, ValueError, TypeError, KeyError, AttributeError):
                result["observation_warning"] = "Records saved; change summary unavailable. Existing checks still apply."
    except (ValueError, TypeError, OSError, KeyError) as exc:
        for path, original, changed in reversed(committed):
            if changed:
                if original is None:
                    path.unlink(missing_ok=True)
                else:
                    path.write_bytes(original)
        event.update(outcome="error", error=str(exc))
        result = {"ok": False, "errors": [str(exc)], "next_action": "Agent: correct the indicated fields and retry. Keep research decisions with the user; do not ask them to edit CSV/JSONL."}
    finally:
        for temp in temporary:
            temp.unlink(missing_ok=True)
    event.update(finished_at=now(), elapsed_seconds=round(time.monotonic() - started, 6))
    try:
        record_event(root, event)
    except (ValueError, OSError) as exc:
        result["observation_warning"] = f"Activity could not be recorded: {exc}"
    if result["ok"]:
        from record_changes import latest_changes
        from task_context import current_work
        result["changes"] = latest_changes(root)
        result["current_work"] = current_work(root, load(root, "state/progress.json"))
    return {**result, "observation": event}
