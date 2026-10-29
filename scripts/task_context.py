"""Current work references, separate from historical completion receipts."""
from __future__ import annotations

import json

from check_delivery import (inspect_jsonl_text, inspect_csv_text, sha256_file,
                            reading_evidence_target, resolve_inside)
from task_storage import safe_path, nonempty, digest


def task_inputs(root):
    """One input reader for work preparation and version-bound review packets."""
    spec = safe_path(root, 'state/task_spec.md').read_text(encoding='utf-8')
    path = safe_path(root, 'state/requirements.jsonl')
    text = path.read_text(encoding='utf-8') if path.exists() else ''
    rows, errors = inspect_jsonl_text(text, 'Requirement')
    if errors:
        raise ValueError('; '.join(errors))
    return {'task': spec, 'requirements': text if text.strip() else '', 'rows': rows}


def source_inputs(root, sources):
    """Read selected source originals, using the same locators as content review."""
    texts, originals = {}, {}
    text_suffixes = {'.md', '.txt', '.html', '.htm', '.csv', '.tsv', '.json', '.jsonl', '.rst', '.log', '.yaml', '.yml'}
    for source in sources:
        names = set()
        if nonempty(source.get('evidence_path')):
            names.add(source['evidence_path'].strip())
        for field in ('url', 'read_evidence'):
            target = reading_evidence_target(source.get(field))
            if target:
                path = resolve_inside(root, target)
                if path is None:
                    raise ValueError(f"Source {source['source_id']}: evidence must stay inside the task.")
                names.add(path.relative_to(root.resolve()).as_posix())
        readable = False
        for name in sorted(names):
            path = safe_path(root, name)
            if not path.is_file() or not path.read_bytes().strip():
                raise ValueError(f"Source {source['source_id']}: missing or empty evidence {name}.")
            if path.suffix.lower() in text_suffixes:
                try:
                    texts[name] = path.read_text(encoding='utf-8')
                except UnicodeError as exc:
                    raise ValueError(f"Source {source['source_id']}: provide a UTF-8 evidence_path for {name}.") from exc
                readable = readable or bool(texts[name].strip())
            else:
                originals[name] = sha256_file(path)
        if not readable:
            raise ValueError(f"data/source_registry.csv row {source['source_id']}, evidence_path: set a task-relative UTF-8 source text or extract, such as sources/{source['source_id']}.md. URLs and page locators alone cannot be reviewed.")
    return texts, originals


def changed_inputs(root, inputs):
    changed = []
    for name, expected in inputs.items():
        try:
            if sha256_file(safe_path(root, name)) == expected:
                continue
        except (OSError, ValueError):
            pass
        changed.append(name)
    return changed


def research_outputs(root, warnings):
    """Recover saved branch artifacts from the existing activity log, not another ledger."""
    outputs = {}
    try:
        path = safe_path(root, 'logs/activity.jsonl')
        text = path.read_text(encoding='utf-8') if path.exists() else ''
    except (OSError, ValueError):
        warnings.append('Analysis observations unreadable; original activity log retained.')
        return []
    if text:
        for line in text.splitlines():
            try:
                row = json.loads(line)
                if not isinstance(row, dict) or row.get('outcome') != 'saved' or row.get('artifact_kind') != 'analysis':
                    continue
                item = {'path': row['artifact'], 'sha256': row['artifact_sha256']}
                for key in ('host_task', 'based_on'):
                    if key in row:
                        item[key] = row[key]
                item['changed_inputs'] = changed_inputs(root, row.get('based_on', {}))
                item['changed_since_save'] = bool(changed_inputs(root, {item['path']:item['sha256']}))
                outputs[item['path']] = item
            except (ValueError, KeyError, TypeError, AttributeError):
                warnings.append('Unreadable analysis observation; original activity row retained.')
    return list(outputs.values())


def prepare_work(root, progress, work):
    """Assemble the Agent's explicit selection; do not infer scope or choose a plan."""
    from record_changes import claim_source_ids
    allowed = {'question', 'requirement_ids', 'claim_ids', 'source_ids', 'paths'}
    if not isinstance(work, dict) or set(work) - allowed:
        raise ValueError('work: use optional question, requirement_ids, claim_ids, source_ids and paths.')
    if 'question' in work and not nonempty(work['question']):
        raise ValueError('work.question: provide the specific research question as text.')
    for key in allowed - {'question'}:
        if key in work and (not isinstance(work[key], list) or any(not nonempty(v) for v in work[key])):
            raise ValueError(f'work.{key}: use a list of IDs or task-relative paths.')
    supplied = task_inputs(root)
    context = current_work(root, progress)
    def select(rows, field, ids, label):
        missing = set(ids) - {r.get(field, r.get('id')) for r in rows}
        if missing:
            raise ValueError(f"work.{label}: unknown IDs {', '.join(sorted(missing))}.")
        return [r for r in rows if r.get(field, r.get('id')) in ids]
    def registry(name, identity):
        path = safe_path(root, name)
        rows, errors = inspect_csv_text(path.read_text(encoding='utf-8'), name, (identity,), identity)
        if errors:
            raise ValueError('; '.join(errors))
        return rows
    requirements = select(supplied['rows'], 'requirement_id', work.get('requirement_ids', []), 'requirement_ids')
    claims = select(registry('data/claims_registry.csv', 'claim_id'), 'claim_id', work.get('claim_ids', []), 'claim_ids')
    sources = registry('data/source_registry.csv', 'source_id')
    source_ids = set(work.get('source_ids', []))
    registered = {s['source_id'] for s in sources}
    for claim in claims:
        source_ids.update(claim_source_ids(claim, registered))
    for requirement in requirements:
        source_ids.update(requirement.get('required_source_ids', []))
    selected_sources = select(sources, 'source_id', source_ids, 'source_ids')
    files, originals = source_inputs(root, selected_sources)
    for name in work.get('paths', []):
        try:
            files[name] = safe_path(root, name).read_text(encoding='utf-8')
        except (OSError, ValueError) as exc:
            raise ValueError(f'work.paths: cannot read {name}; use an existing task-relative UTF-8 file.') from exc
    input_names = ['state/task_spec.md', *files, *originals]
    if safe_path(root, 'state/requirements.jsonl').exists():
        input_names.append('state/requirements.jsonl')
    if selected_sources:
        input_names.append('data/source_registry.csv')
    if claims:
        input_names.append('data/claims_registry.csv')
    inputs = {name: sha256_file(safe_path(root, name)) for name in dict.fromkeys(input_names)}
    result = {'question': work.get('question'), 'task': supplied['task'],
              'task_directory': str(root), 'effective_requirements': context['effective_requirements'],
              'scope_decisions': context['scope_decisions'], 'selected_requirements': requirements,
              'claims': claims, 'sources': selected_sources, 'files': files, 'source_files': originals,
              'main_artifact': context['artifact'], 'research_outputs': context['research_outputs'], 'inputs': inputs}
    result['input_version'] = digest({'question': result['question'], 'inputs': inputs})
    return result


def runtime_identity(toolkit):
    """Identify this implementation; do not claim the host loaded its Skill."""
    result = {"version": (toolkit / "VERSION").read_text(encoding="utf-8").strip(),
              "implementation_path": str(toolkit / "scripts/research_workflow.py"),
              "implementation_sha256": sha256_file(toolkit / "scripts/research_workflow.py"),
              "entry_path": str(toolkit / "SKILL.md"),
              "entry_sha256": sha256_file(toolkit / "SKILL.md"),
              "host_loaded_entry": "not_observed"}
    return result


def current_work(root, progress):
    result = {"task_spec": "state/task_spec.md", "requirements": "state/requirements.jsonl",
              "artifact": None, "open_requirements": [], "effective_requirements": [],
              "scope_decisions": [], "warnings": [], "brief": progress.get('brief', {})}
    current = progress.get("current_artifact")
    if current is not None:
        try:
            path = safe_path(root, current["path"])
            checksum = sha256_file(path)
            result["artifact"] = {**current, "current_sha256": checksum,
                                  "changed_since_save": checksum != current.get("sha256")}
        except (OSError, ValueError, KeyError, TypeError):
            result["warnings"].append("Current artifact is missing or invalid; inspect the registered path.")
    try:
        path = safe_path(root, result["requirements"])
        if path.exists():
            rows, errors = inspect_jsonl_text(path.read_text(encoding="utf-8"), result["requirements"])
            result["warnings"].extend(errors)
            for row in rows:
                status = row.get("status")
                if isinstance(status, str) and status in {'waived', 'out_of_scope', 'accepted_limitation'}:
                    result['scope_decisions'].append(row)
                else:
                    result['effective_requirements'].append(row)
                if not isinstance(status, str):
                    result["warnings"].append("Requirement status is not text; retain the row and repair it through existing records.")
                    result["open_requirements"].append(row)
                elif status not in {"satisfied", "waived", "out_of_scope", "accepted_limitation"}:
                    result["open_requirements"].append(row)
    except (OSError, ValueError):
        result["warnings"].append("Requirements unreadable; inspect existing records before recovery.")
    result['research_outputs'] = research_outputs(root, result['warnings'])
    result["scope"] = "Resume references, not proof of reading, applied feedback or semantic quality. No main artifact inferred for legacy tasks."
    return result


def require_current_artifact(progress, artifact):
    current = progress.get("current_artifact")
    if current is not None and current.get("path") != artifact:
        raise ValueError("artifact differs from the registered main draft. Use its path or explicitly register the intended main draft with draft.main=true.")
