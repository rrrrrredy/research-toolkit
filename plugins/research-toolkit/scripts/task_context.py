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
    from record_changes import input_digest
    changed = []
    for name, expected in inputs.items():
        try:
            if input_digest(root, name) == expected:
                continue
        except (OSError, ValueError):
            pass
        changed.append(name)
    return changed


def research_outputs(root, warnings, progress=None):
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
                if (not isinstance(row, dict) or row.get('outcome') != 'saved'
                        or not row.get('artifact') or (row.get('artifact_kind') != 'analysis'
                            and not row.get('unit_id') and not row.get('host_task'))):
                    continue
                previous = outputs.get(row['artifact'], {})
                item = {'path': row['artifact'], 'sha256': row['artifact_sha256'],
                        'kind': row.get('artifact_kind'), 'complete': row.get('unit_complete', row.get('complete_draft', False)),
                        'contributors': sorted(set(previous.get('contributors', [])) | ({row['host_task']} if row.get('host_task') else set())),
                        'history': {'path': 'logs/activity.jsonl', 'artifact': row['artifact']}}
                for key in ('host_task', 'based_on', 'unit_id', 'depends_on', 'dependency_versions', 'handoff', 'question',
                            'artifact_snapshot', 'previous_version'):
                    if key in row:
                        item[key] = row[key]
                    elif key in previous:
                        item[key] = previous[key]
                item['owner'] = item.get('handoff', {}).get('to') or item.get('host_task')
                item['changed_inputs'] = [name for name in changed_inputs(root, item.get('based_on', {}))
                                          if name.startswith('record:') or safe_path(root, name) != safe_path(root, item['path'])]
                item['changed_since_save'] = bool(changed_inputs(root, {item['path']:item['sha256']}))
                outputs[item['path']] = item
            except (ValueError, KeyError, TypeError, AttributeError):
                warnings.append('Unreadable analysis observation; original activity row retained.')
    units = {item['unit_id']: item for item in outputs.values() if item.get('unit_id')}
    reviews = (progress or {}).get('unit_reviews', {})
    if not isinstance(reviews, dict):
        warnings.append('Unit review references are malformed; retained work requires an intact review record.')
        reviews = {}
    # Cached approval is useful only while the actual review inputs and retained
    # replies still match. Supplemental review evidence need not be in based_on.
    # Reuse the file checks, not inspect(), which itself reads research_outputs.
    current_reviews = set()
    plans = (progress or {}).get('unit_review_plans', {})
    for unit_id, item in units.items():
        review = reviews.get(unit_id, {})
        plan = plans.get(unit_id, {}) if isinstance(plans, dict) else {}
        if (not isinstance(review, dict) or not isinstance(plan, dict)
                or review.get('ok') is not True or review.get('artifact_sha256') != item['sha256']
                or plan.get('input_version') != review.get('input_version')
                or plan.get('artifact') != item['path'] or plan.get('artifact_sha256') != item['sha256']):
            continue
        try:
            from host_review import checked_files
            checked_files(root, plan)
            current_reviews.add(unit_id)
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
            warnings.append(f'Unit {unit_id}: independent review is no longer current: {exc}')
    def inspect_unit(unit_id, visiting):
        if unit_id in visiting:
            return ['cyclic_dependency']
        item = units.get(unit_id)
        if item is None:
            return ['not_registered']
        issues = []
        if not item['complete']:
            issues.append('not_complete')
        if item['changed_inputs']:
            issues.append('inputs_changed')
        if item['changed_since_save']:
            issues.append('artifact_changed')
        if any(units.get(dependency, {}).get('sha256') != checksum
               for dependency, checksum in item.get('dependency_versions', {}).items()):
            issues.append('dependency_version_changed')
        if unit_id not in current_reviews:
            issues.append('independent_review_pending')
        if any(inspect_unit(dependency, visiting | {unit_id}) for dependency in item.get('depends_on', [])):
            issues.append('dependency_pending')
        return issues
    for item in outputs.values():
        item['dependencies'] = [{'unit_id': unit_id, 'path': units.get(unit_id, {}).get('path'),
                                 'issues': inspect_unit(unit_id, set())}
                                for unit_id in item.get('depends_on', [])]
        if item.get('unit_id'):
            item['readiness_issues'] = inspect_unit(item['unit_id'], set())
            item['review'] = reviews.get(item['unit_id'])
    return list(outputs.values())


def prepare_work(root, progress, work):
    """Assemble the Agent's explicit selection; do not infer scope or choose a plan."""
    from record_changes import claim_source_ids, input_digest, requirements_for_units
    allowed = {'question', 'unit_id', 'depends_on', 'requirement_ids', 'claim_ids', 'source_ids', 'paths'}
    if not isinstance(work, dict) or set(work) - allowed:
        raise ValueError('work: use optional question, unit_id, depends_on, requirement_ids, claim_ids, source_ids and paths.')
    if 'question' in work and not nonempty(work['question']):
        raise ValueError('work.question: provide the specific research question as text.')
    if 'unit_id' in work:
        import re
        if not isinstance(work['unit_id'], str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', work['unit_id']):
            raise ValueError('work.unit_id: use a saved or new research-unit ID with letters, numbers, dots, underscores or hyphens.')
    for key in allowed - {'question', 'unit_id'}:
        if key in work and (not isinstance(work[key], list) or any(not nonempty(v) for v in work[key])):
            raise ValueError(f'work.{key}: use a list of IDs or task-relative paths.')
    supplied = task_inputs(root)
    context = current_work(root, progress)
    unit = next((item for item in context['research_outputs'] if item.get('unit_id') == work.get('unit_id')),
                None) if work.get('unit_id') else None
    paths = list(work.get('paths', []))
    record_ids = {key: list(work.get(key, [])) for key in ('requirement_ids', 'claim_ids', 'source_ids')}
    upstream = []
    def take_inputs(item):
        paths.append(item['path'])
        for name in item.get('based_on', {}):
            if name.startswith('record:'):
                _, kind, identity = name.split(':', 2)
                field = {'sources': 'source_ids', 'claims': 'claim_ids', 'requirements': 'requirement_ids'}[kind]
                aggregate = kind == 'requirements' and (identity == 'effective' or identity.startswith('effective@'))
                if not aggregate and identity not in record_ids[field]:
                    record_ids[field].append(identity)
            elif name not in {'state/task_spec.md', 'state/requirements.jsonl', 'data/source_registry.csv', 'data/claims_registry.csv'}:
                paths.append(name)
    if unit:
        take_inputs(unit)
    dependencies = list(work.get('depends_on', (unit or {}).get('depends_on', [])))
    seen = set()
    def take_upstream(dependency):
        if dependency in seen:
            return
        seen.add(dependency)
        selected = next((item for item in context['research_outputs'] if item.get('unit_id') == dependency), None)
        if selected:
            upstream.append(selected)
            take_inputs(selected)
            for ancestor in selected.get('depends_on', []):
                take_upstream(ancestor)
    for dependency in dependencies:
        take_upstream(dependency)
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
    requirements = select(supplied['rows'], 'requirement_id', record_ids['requirement_ids'], 'requirement_ids')
    claims = select(registry('data/claims_registry.csv', 'claim_id'), 'claim_id', record_ids['claim_ids'], 'claim_ids')
    sources = registry('data/source_registry.csv', 'source_id')
    source_ids = set(record_ids['source_ids'])
    registered = {s['source_id'] for s in sources}
    for claim in claims:
        source_ids.update(claim_source_ids(claim, registered))
    for requirement in requirements:
        source_ids.update(requirement.get('required_source_ids', []))
    selected_sources = select(sources, 'source_id', source_ids, 'source_ids')
    files, originals = source_inputs(root, selected_sources)
    for name in dict.fromkeys(paths):
        try:
            files[name] = safe_path(root, name).read_text(encoding='utf-8')
        except (OSError, ValueError) as exc:
            raise ValueError(f'work.paths: cannot read {name}; use an existing task-relative UTF-8 file.') from exc
    input_names = ['state/task_spec.md', *files, *originals]
    requirement_unit_ids = sorted({work['unit_id'], *seen}) if work.get('unit_id') else None
    requirement_binding = ('record:requirements:effective@' + ','.join(requirement_unit_ids)
                           if requirement_unit_ids else 'record:requirements:effective')
    input_names.append(requirement_binding)
    input_names.extend('record:sources:' + source['source_id'] for source in selected_sources)
    input_names.extend('record:claims:' + claim['claim_id'] for claim in claims)
    inputs = {name: input_digest(root, name) for name in dict.fromkeys(input_names)}
    result = {'question': work.get('question', (unit or {}).get('question')), 'unit_id': work.get('unit_id'),
              'unit': unit, 'upstream_outputs': upstream, 'task': supplied['task'],
              'dependencies': [{'unit_id': dependency,
                                'issues': next((item.get('readiness_issues', []) for item in upstream
                                                if item.get('unit_id') == dependency), ['not_registered'])}
                               for dependency in dependencies],
              'task_directory': str(root), 'effective_requirements': context['effective_requirements'],
              'applicable_requirements': requirements_for_units(context['effective_requirements'], requirement_unit_ids),
              'requirement_unit_ids': requirement_unit_ids,
              'scope_decisions': context['scope_decisions'], 'selected_requirements': requirements,
              'claims': claims, 'sources': selected_sources, 'files': files, 'source_files': originals,
              'main_artifact': context['artifact'], 'research_outputs': context['research_outputs'], 'inputs': inputs,
              'production_contexts': context['production_contexts']}
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
    result['research_outputs'] = research_outputs(root, result['warnings'], progress)
    result['work_units'] = [item for item in result['research_outputs'] if item.get('unit_id')]
    result['production_contexts'] = sorted({host for item in result['research_outputs']
                                          for host in item.get('contributors', [])}
                                         | ({progress['author_id']} if nonempty(progress.get('author_id')) else set()))
    result["scope"] = "Resume references, not proof of reading, applied feedback or semantic quality. No main artifact inferred for legacy tasks."
    return result


def require_current_artifact(progress, artifact):
    current = progress.get("current_artifact")
    if current is not None and current.get("path") != artifact:
        raise ValueError("artifact differs from the registered main draft. Use its path or explicitly register the intended main draft with draft.main=true.")
