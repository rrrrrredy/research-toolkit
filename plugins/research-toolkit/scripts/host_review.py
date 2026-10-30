"""Version-bound review assignments executed by the host's independent agents.

The host owns spawning, waiting and cancellation. This module reuses the task's
source reader, storage and review log; it never starts a second agent runtime.
"""
from __future__ import annotations

import json
import uuid
from difflib import SequenceMatcher
from pathlib import Path

from task_storage import digest, load, nonempty, safe_path, save, save_text
from task_context import current_work, task_inputs, research_outputs, prepare_work
from run_observation import now

DIMENSIONS = ["requirements", "evidence", "adversarial_reasoning", "structure_and_depth",
              "reader_usefulness", "process_language", "natural_expression"]
SAMPLING = ("Read the whole current report and original evidence. Check every effective requirement, "
    "decisive claim, important number/citation, counterexample, required finding and consequential "
    "no-change decision. Independently choose additional passed/no-issue passages and transformations "
    "from branch analysis to report; record selection reasons and locations. If a defect is found, "
    "extend to its shared source, metric, branch or failure pattern and record what was examined. "
    "Do not use a fixed first/last/hash sample or an author's selection as the audit population.")


def run_prefix(version):
    # Keep task paths usable on Windows. The complete digest stays in every
    # assignment and frozen() rejects a conflicting retained directory.
    return "reviews/host/" + version[:20]


def reference(root, path):
    from check_delivery import sha256_file
    return {"path": path, "sha256": sha256_file(safe_path(root, path))}


def history(root):
    from research_workflow import rows_for
    return rows_for(root)


def append(root, row):
    from research_workflow import append_row
    append_row(root, row)


def frozen(root, name, value):
    if safe_path(root, name).exists():
        if load(root, name) != value:
            raise ValueError(f"Retained assignment changed: {name}; preserve the original.")
    else:
        save(root, name, value)
    return reference(root, name)


def producers(root, progress):
    ids = {progress.get("author_id"), progress.get("current_artifact", {}).get("owner")}
    for event in history_activity(root):
        if event.get("host_task"):
            ids.add(event["host_task"])
    return sorted(x for x in ids if nonempty(x))


def history_activity(root):
    path = safe_path(root, "logs/activity.jsonl")
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()] if path.exists() else []


def revision_context(root, previous_plan, packet, bindings):
    """Point the next reader to retained work; never reuse its approval."""
    previous = load(root, previous_plan["input"]["path"])
    selected = selected_results(root, previous_plan)
    audits = selected.get("audit", {}).get("result_data", {}).get("review_checks", {})
    reviews = {}
    for slot in previous_plan["slots"]:
        row = selected.get(slot["slot_id"])
        validity = audits.get(slot["slot_id"], {}).get("result")
        if slot["role"] == "reviewer" and row and validity != "invalid":
            reviews[slot["slot_id"]] = {"attempt_id": row["attempt_id"], "response": row["response"],
                "input": row["input"], "execution": row["execution"], "execution_id": row["execution_id"],
                "report_verdict": row["report_verdict"], "review_validity": validity or "not_separately_audited"}
    before, after = previous["report"].splitlines(), packet["report"].splitlines()
    changes = [{"change": kind,
                "previous_lines": [i + 1, j] if j > i else None,
                "current_lines": [k + 1, n] if n > k else None,
                "previous_text": "\n".join(before[i:j]), "current_text": "\n".join(after[k:n])}
               for kind, i, j, k, n in SequenceMatcher(None, before, after, autojunk=False).get_opcodes()
               if kind != "equal"]
    old_bindings = previous_plan.get("bindings", {})
    names = sorted(set(old_bindings) | set(bindings))
    return {"historical_only": True, "input": previous_plan["input"],
            "input_version": previous_plan["input_version"], "reviews": reviews,
            "changed_inputs": [{"path": name, "previous_sha256": old_bindings.get(name),
                                "current_sha256": bindings.get(name)} for name in names
                               if old_bindings.get(name) != bindings.get(name)],
            "unchanged_inputs": [name for name in names if old_bindings.get(name) == bindings.get(name)],
            "report_changes": changes}


def packet_for(root, progress, evidence_paths, artifact, scope, previous_plan=None):
    from research_workflow import required_source_inputs
    from check_delivery import sha256_file
    if not isinstance(evidence_paths, list) or not all(nonempty(x) for x in evidence_paths):
        raise ValueError("evidence_paths must be a list of task-relative source files; registered originals are included.")
    shared = task_inputs(root)
    all_outputs = research_outputs(root, [], progress)
    if scope == "full_report":
        names, binaries = required_source_inputs(root)
        files = sorted(set([*names, *evidence_paths, "data/source_registry.csv", "data/claims_registry.csv"]))
        sources = {name: safe_path(root, name).read_text(encoding="utf-8") for name in files}
        outputs = all_outputs
        bindings = {name: sha256_file(safe_path(root, name)) for name in
                    [artifact, "state/task_spec.md", *files]}
        # Recording actual fulfilment after audit/acceptance must not invalidate
        # those results. Requirement meaning/scope remains version-bound; the
        # frozen packet retains the original rows and finish hashes current rows.
        from record_changes import input_digest
        bindings['record:requirements:effective'] = input_digest(root, 'record:requirements:effective')
    else:
        work_packet = prepare_work(root, progress, {"unit_id": scope, "paths": evidence_paths})
        sources, binaries = work_packet["files"], work_packet["source_files"]
        outputs = [work_packet["unit"], *work_packet["upstream_outputs"]]
        bindings = dict(work_packet["inputs"])
        # Retain the actual selected registry records, without binding unrelated rows.
        sources = {**sources, "selected_source_records": json.dumps(work_packet["sources"], ensure_ascii=False),
                   "selected_claim_records": json.dumps(work_packet["claims"], ensure_ascii=False)}
    # Readiness is a derived view, not part of the evidence being reviewed.
    outputs = [{k: v for k, v in item.items() if k in {"path", "sha256", "kind", "complete", "unit_id",
        "depends_on", "dependency_versions", "host_task", "contributors", "question", "based_on", "handoff",
        "artifact_snapshot", "history", "previous_version"}}
        for item in outputs if item]
    # Freeze just the selected production history. Binding the live activity log
    # would invalidate an assignment when review itself appends an observation.
    artifact_paths = {item['path'] for item in outputs}
    production_history = [{k: v for k, v in row.items() if k in {
        'operation_id', 'started_at', 'finished_at', 'artifact', 'artifact_sha256',
        'artifact_kind', 'unit_id', 'unit_complete', 'complete_draft', 'question',
        'depends_on', 'dependency_versions', 'host_task', 'handoff',
        'artifact_snapshot', 'previous_version'}}
        for row in history_activity(root)
        if row.get('outcome') == 'saved' and row.get('artifact') in artifact_paths]
    for row in production_history:
        for key in ('artifact_snapshot', 'previous_version'):
            ref = row.get(key)
            if ref:
                if reference(root, ref['path']) != ref:
                    raise ValueError('Retained production version changed: ' + ref['path'])
                bindings[ref['path']] = ref['sha256']
    if any(not value.strip() for value in sources.values()):
        raise ValueError("A required evidence file is empty.")
    report = safe_path(root, artifact).read_text(encoding="utf-8")
    if not report.strip():
        raise ValueError("Provide the actual substantive draft before independent review.")
    analyses = {}
    for item in outputs:
        name = item.get("path")
        if name and safe_path(root, name).is_file():
            analyses[name] = safe_path(root, name).read_text(encoding="utf-8")
    work = current_work(root, progress)
    packet = {"task": shared["task"], "requirements": shared["requirements"],
              "effective_requirements": work["effective_requirements"],
              "scope_decisions": work["scope_decisions"], "report_path": artifact,
              "report": report, "sources": sources, "source_files": binaries,
              "research_outputs": outputs, "production_history": production_history,
              "analyses": analyses, "scope": scope}
    if scope != "full_report":
        packet["applicable_requirements"] = work_packet["applicable_requirements"]
        packet["requirement_unit_ids"] = work_packet["requirement_unit_ids"]
    # Keep earlier required criticism visible after revision; do not turn a new
    # version into an opportunity to silently lose an unresolved finding.
    previous_packet = load(root, previous_plan['input']['path']) if previous_plan else None
    if previous_packet and packet == {k: v for k, v in previous_packet.items() if k != 'prior_required_findings'}:
        # Receiving another response to this same assignment must not change its
        # inputs. Earlier criticism remains exactly as supplied at preparation.
        packet['prior_required_findings'] = previous_packet.get('prior_required_findings', [])
    else:
        # Evidence or requirements can change while the prose stays identical.
        # Retain those earlier findings too, for independent current adjudication.
        packet["prior_required_findings"] = [
            {"attempt_id": r["attempt_id"], "slot_id": r["slot_id"],
             "artifact_sha256": r["artifact_sha256"], "response": r["response"], "finding": f}
            for r in history(root) if r.get("record_type") == "model_review" and r.get("contract_version") == 2
            and r.get("scope") == scope and r.get("status") == "completed"
            for f in r.get("findings", []) if f.get("severity") != "optional"]
    bindings.update({name: sha256_file(safe_path(root, name)) for name in [artifact, *analyses]})
    bindings.update(binaries)
    return packet, bindings


def selected_results(root, plan):
    selected = {}
    for row in history(root):
        if (row.get("contract_version") == 2 and row.get("input_version") == plan["input_version"]
                and row.get("scope") == plan["scope"] and row.get("status") == "completed"):
            selected[row["slot_id"]] = row
    # An amended review changes the audit input; an amended audit changes acceptance.
    # Retain old executions but do not let their old verdicts approve new inputs.
    for sid in ("audit", "acceptance"):
        if sid in selected:
            slot = next((s for s in plan["slots"] if s["slot_id"] == sid), None)
            try:
                _, expected = assignment(root, plan, slot, selected, persist=False)
                if selected[sid]["input"] != expected:
                    selected.pop(sid)
            except (KeyError, TypeError):
                selected.pop(sid)
    return selected


def methods(role):
    from research_guidance import guidance
    names = {"reviewer": ["review"], "auditor": ["audit"], "acceptance": ["acceptance"]}
    return "\n\n".join(x["content"] for x in guidance("review", methods=names[role])["guidance"])


def assignment(root, plan, slot, selected, *, persist=True):
    packet = load(root, plan["input"]["path"])
    role = slot["role"]
    request = {"contract_version": 2, "role": role, "slot_id": slot["slot_id"], "input_version": plan["input_version"],
               "artifact_sha256": plan["artifact_sha256"], "scope": plan["scope"],
               "dimensions": slot.get("dimensions", []), "assignment": packet,
               "instructions": plan["instructions"][role]}
    if plan.get("revision_context"):
        retained = plan["revision_context"]
        request["revision_context"] = {**retained, "reviews": (
            {slot["slot_id"]: retained["reviews"][slot["slot_id"]]}
            if role == "reviewer" and slot["slot_id"] in retained["reviews"] else
            {} if role == "reviewer" else retained["reviews"])}
        request["instructions"] += ("\nUse the retained previous response and frozen input to recover checks already performed. "
            "The change locations and input hashes help find what changed; they do not decide its substantive impact. "
            "Confirm the current complete artifact in your assigned perspective, inspect affected evidence and cross-part effects, "
            "and reuse unchanged reading where appropriate. Historical results are not current approval.")
    if slot.get("domain"):
        request["domain"] = slot["domain"]
    if role == "reviewer":
        from research_workflow import REVIEW_INSTRUCTIONS
        request["instructions"] += "\n" + REVIEW_INSTRUCTIONS
        request["instructions"] += ("\nYour assigned perspective is " + slot["slot_id"] +
            ". Read the complete supplied draft and relevant originals. Do the assigned substantive assessment "
            "in a context separate from every producer and the other perspectives. Do not edit the draft.")
        if slot['slot_id'] == 'structure_and_depth' and 'production_history' in packet:
            request['instructions'] += ("\nWhen the task requires progressive research or writing, inspect production_history "
                "and its retained drafts against the requested progression; save counts alone do not establish substantive stages.")
    else:
        content = {s["slot_id"]: selected[s["slot_id"]] for s in plan["slots"] if s["role"] == "reviewer"}
        request["reviews"] = {key: {"record": value, "original": safe_path(root, value["response"]["path"]).read_text(encoding="utf-8")}
                              for key, value in content.items()}
        request["sampling"] = SAMPLING
        if role == "auditor":
            if 'production_history' in packet:
                request['instructions'] += ("\nFor required production and handoff behavior, inspect production_history and its "
                    "original draft references. The saved history supplies navigation, not proof that an agent read or followed it.")
            request["instructions"] += """
Return one JSON object with result (valid/invalid, judging review validity), basis,
review_checks keyed by every review slot (each result valid/invalid and basis),
dispositions keyed by every current finding as slot_id/finding_id (decision
confirmed_defect/no_change/unresolved, reason, evidence), critical_checks (list of
location/evidence/result clear|defect, include requirement_id for EVERY effective
requirement), sample_checks (list of location/selection_reason/evidence/result
clear|defect; each defect includes expansion with examined locations and outcome),
prior_findings keyed by every prior attempt_id/finding_id (decision resolved/no_change/
unresolved, reason, evidence in the current draft), report_verdict (pass/needs_revision),
and open_issues (list). A valid negative review remains valid. Do not clear a real
defect as resolved while it remains in the frozen draft. No generic PASS evidence.
"""
            if plan["scope"] != "full_report":
                request["instructions"] = request["instructions"].replace(
                    "include requirement_id for EVERY effective\nrequirement", "include requirement_id for EVERY applicable\nrequirement")
                request["instructions"] += ("\nThis audit is for research unit " + plan["scope"] +
                    ", not whole-report delivery. Read its complete artifact, relevant originals and submitted reviews. "
                    "Check every applicable_requirements entry and decisive premise within this unit; the full effective "
                    "requirements remain available as context. Do not claim unrelated whole-report obligations are completed. "
                    "report_verdict describes whether this unit's reviewed work can support its dependants. "
                    "Independently adjudicate any disputed necessary findings and sample the unit's passed content.")
                request["sampling"] = SAMPLING.replace("whole current report", "complete current research unit").replace(
                    "every effective requirement", "every requirement applicable to this unit")
        else:
            audit = selected["audit"]
            request["audit"] = {"record": audit, "original": safe_path(root, audit["response"]["path"]).read_text(encoding="utf-8")}
            request["instructions"] += """
Independently decide whether this complete current report answers the user's whole
request. Read the full report, actual production handoffs, review/audit originals
and source evidence; do not inherit their verdict. Check coverage, depth, analysis
carried into the prose, preserved conditions/citations and required corrections.
Return one JSON object: result pass/fail, basis, coverage keyed by requirements,
evidence, adversarial_reasoning, structure_and_depth, reader_usefulness,
process_language, natural_expression (each location and basis), sample_checks
(list of location/selection_reason/evidence/result clear|defect, with expansion
for defects), and open_issues (list). Pass requires no necessary corrections.
"""
    request["instructions"] += "\nReturn input_version and assignment_version exactly as supplied, alongside the requested assessment fields."
    request["assignment_version"] = digest(request)
    name = f"{run_prefix(plan['input_version'])}/jobs/{slot['slot_id']}-{request['assignment_version'][:16]}.json"
    if persist:
        ref = frozen(root, name, request)
    else:
        ref = (reference(root, name) if safe_path(root, name).is_file() and load(root, name) == request
               else {"path": name, "sha256": "unrecorded_assignment"})
    return request, ref


def check_samples(value):
    if not isinstance(value, list) or not value:
        raise ValueError("sample_checks must retain independently selected locations and reasons.")
    for item in value:
        if not isinstance(item, dict) or not all(nonempty(item.get(k)) for k in ("location", "selection_reason", "evidence")):
            raise ValueError("Each sample needs location, selection_reason and evidence.")
        if item.get("result") not in {"clear", "defect"}:
            raise ValueError("Sample result must be clear or defect.")
        if item["result"] == "defect" and not item.get("expansion"):
            raise ValueError("A sample defect needs the actual related-source/metric/branch expansion.")


def validate_result(value, request):
    from research_workflow import checked_review
    if not isinstance(value, dict):
        raise ValueError("The original response must be a JSON object.")
    # Bind the actual returned response, not merely the caller's receipt.
    if any(value.get(k) != request[k] for k in ("input_version", "assignment_version")):
        raise ValueError("The response must quote this assignment's input_version and assignment_version.")
    role = request["role"]
    if role == "reviewer":
        checked_review(value, request["dimensions"])
        return
    if not nonempty(value.get("basis")) or not isinstance(value.get("open_issues"), list):
        raise ValueError("Independent audit/acceptance needs a located basis and open_issues list.")
    check_samples(value.get("sample_checks"))
    if role == "acceptance":
        if value.get("result") not in {"pass", "fail"}:
            raise ValueError("Acceptance result must be pass or fail.")
        checked_review({"report_verdict": "not_assessed", "coverage": value.get("coverage"), "findings": []}, DIMENSIONS)
        if value["result"] == "pass" and (value["open_issues"] or any(x["result"] == "defect" for x in value["sample_checks"])):
            raise ValueError("Acceptance cannot pass while a current defect remains.")
        return
    if value.get("result") not in {"valid", "invalid"} or value.get("report_verdict") not in {"pass", "needs_revision"}:
        raise ValueError("Audit must distinguish review validity and current report readiness.")
    reviews = request["reviews"]
    checks = value.get("review_checks")
    if not isinstance(checks, dict) or set(checks) != set(reviews) or any(
            not isinstance(c, dict) or c.get("result") not in {"valid", "invalid"} or not nonempty(c.get("basis")) for c in checks.values()):
        raise ValueError("Audit must assess every independent review.")
    if value["result"] == "valid" and any(c["result"] != "valid" for c in checks.values()):
        raise ValueError("Audit cannot be valid while a required review is invalid.")
    expected = {key + "/" + f["finding_id"]: f for key, review in reviews.items()
                for f in review["record"].get("findings", [])}
    dispositions = value.get("dispositions")
    if not isinstance(dispositions, dict) or set(dispositions) != set(expected):
        raise ValueError("Audit dispositions must cover every actual current finding exactly once.")
    for d in dispositions.values():
        if not isinstance(d, dict) or d.get("decision") not in {"confirmed_defect", "no_change", "unresolved"} or not all(nonempty(d.get(k)) for k in ("reason", "evidence")):
            raise ValueError("Audit dispositions need independent decisions with reasons and evidence.")
    critical = value.get("critical_checks")
    if not isinstance(critical, list) or not critical or any(not isinstance(c, dict)
            or c.get("result") not in {"clear", "defect"} or not all(nonempty(c.get(k)) for k in ("location", "evidence")) for c in critical):
        raise ValueError("Audit critical_checks needs actual located checks.")
    requirements = request["assignment"].get("applicable_requirements", request["assignment"]["effective_requirements"])
    ids = {r.get("requirement_id") for r in requirements}
    if not ids.issubset({c.get("requirement_id") for c in critical}):
        raise ValueError("Audit omitted a currently effective requirement.")
    prior = request["assignment"]["prior_required_findings"]
    wanted = {f['attempt_id'] + '/' + f['finding']['finding_id'] for f in prior}
    decisions = value.get("prior_findings", {})
    if not isinstance(decisions, dict) or set(decisions) != wanted or any(
            not isinstance(d, dict) or d.get("decision") not in {"resolved", "no_change", "unresolved"}
            or not all(nonempty(d.get(k)) for k in ("reason", "evidence")) for d in decisions.values()):
        raise ValueError("Audit must account for prior required findings against the current draft.")
    required_open = any(f.get("severity") != "optional" and dispositions[k]["decision"] != "no_change" for k, f in expected.items())
    from check_review_completion import content_review_issues
    unresolved_review = any(content_review_issues(v['record'], {
        f['finding_id']: dispositions[key + '/' + f['finding_id']]
        for f in v['record'].get('findings', [])}) for key, v in reviews.items())
    if value["report_verdict"] == "pass" and (value["open_issues"] or required_open or unresolved_review
            or any(d["decision"] == "unresolved" for d in decisions.values())
            or any(c["result"] == "defect" for c in [*critical, *value["sample_checks"]])):
        raise ValueError("Report readiness cannot pass with unresolved required findings or actual failed checks.")


def accept_result(root, progress, plan, slot, request, request_ref, supplied, selected):
    if not isinstance(supplied, dict) or any(not nonempty(supplied.get(k)) for k in ("slot_id", "host_task", "response_path", "execution_path")):
        raise ValueError("host_result needs slot_id, actual host_task, response_path and execution_path.")
    identity = supplied["host_task"]
    if identity in producers(root, progress):
        raise ValueError("A production/assembly context cannot perform independent review, audit or acceptance.")
    if any(r.get("execution_id") == identity and r.get("slot_id") != slot["slot_id"] for r in history(root)
           if r.get("contract_version") == 2):
        raise ValueError("Different review perspectives, audit and acceptance need different host contexts.")
    previous = selected.get(slot["slot_id"])
    if previous:
        audit = selected.get("audit", {}).get("result_data", {})
        invalid = audit.get("review_checks", {}).get(slot["slot_id"], {}).get("result") == "invalid"
        if not invalid:
            raise ValueError("This assignment already has a completed result. Retain valid negative results; revise the draft instead of rerunning it.")
    attempt = uuid.uuid4().hex
    prefix = f"{run_prefix(plan['input_version'])}/results/{attempt[:16]}"
    raw = safe_path(root, supplied["response_path"]).read_bytes()
    execution_raw = safe_path(root, supplied["execution_path"]).read_bytes()
    for name, content in (("response.txt", raw), ("execution.json", execution_raw)):
        target = safe_path(root, prefix + "/" + name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    row = {"record_type": {"reviewer": "model_review", "auditor": "review_audit", "acceptance": "final_acceptance"}[slot["role"]],
           "contract_version": 2, "attempt_id": attempt, "slot_id": slot["slot_id"], "role": slot["role"],
           "scope": plan["scope"], "input_version": plan["input_version"], "artifact_sha256": plan["artifact_sha256"],
           "input": request_ref, "execution_id": identity, "response": reference(root, prefix + "/response.txt"),
           "execution": reference(root, prefix + "/execution.json"), "recorded_at": now()}
    try:
        execution = json.loads(execution_raw.decode("utf-8"))
        if (execution.get("host_task") != identity or execution.get("status") != "completed"
                or execution.get("assignment_version") != request["assignment_version"]):
            raise ValueError("execution_path must retain the actual completed host identity and assignment_version.")
        value = json.loads(raw.decode("utf-8"))
        validate_result(value, request)
        row.update(status="completed", result_data=value)
        if slot["role"] == "reviewer":
            row.update({k: value[k] for k in ("report_verdict", "coverage", "findings")})
    except (ValueError, UnicodeError, AttributeError, TypeError) as exc:
        row.update(status="incomplete", failure=str(exc))
        append(root, row)
        raise ValueError(f"Original host result retained at {prefix}; {exc}") from exc
    append(root, row)


def next_slots(plan, selected):
    content = [s for s in plan["slots"] if s["role"] == "reviewer"]
    missing = [s for s in content if s["slot_id"] not in selected]
    if missing:
        return missing
    if not plan.get("audit_required"):
        return []
    audit = selected.get("audit")
    if audit is None:
        return [s for s in plan["slots"] if s["role"] == "auditor"]
    value = audit["result_data"]
    invalid = [s for s in content if value["review_checks"][s["slot_id"]]["result"] == "invalid"]
    if invalid:
        return invalid
    if value["result"] != "valid" or value["report_verdict"] != "pass":
        return []
    return [s for s in plan["slots"] if s["role"] == "acceptance" and s["slot_id"] not in selected]


def review(workflow, root, progress, evidence_paths, artifact, purpose, revision, include_assignment,
           host_result=None, scope="full_report", perspectives=None, domains=None, audit=None):
    from check_delivery import sha256_file
    if scope == "full_report":
        workflow.require_current_artifact(progress, artifact)
        current = progress.get("current_artifact", {})
        if current.get("path") != artifact or not nonempty(current.get("owner")):
            raise ValueError("Register the main draft's actual producer before independent review: "
                "save draft.path, draft.main=true and draft.host_task with the real producing host task/session. "
                "Historical files and results remain readable.")
    else:
        units = [x for x in research_outputs(root, [], progress) if x.get("unit_id") == scope and x.get("path") == artifact]
        if not units:
            raise ValueError("scope must identify the registered unit_id and its actual artifact.")
    if any(not nonempty(progress.get("brief", {}).get(k)) for k in workflow.BRIEF_FIELDS):
        raise ValueError("Complete the actual research brief before review.")
    if purpose not in {"report_delivery", "evaluation"}:
        raise ValueError("purpose must be report_delivery or evaluation.")
    old = progress.get("review_plan") if scope == "full_report" else progress.get("unit_review_plans", {}).get(scope)
    if audit is not None and type(audit) is not bool:
        raise ValueError("audit must be true or false when supplied.")
    audit_required = scope == "full_report" or bool(old and old.get("audit_required")) or audit is True
    if audit is False and audit_required:
        raise ValueError("audit cannot disable whole-report audit or an already declared unit audit.")
    dimensions = DIMENSIONS if scope == "full_report" else (perspectives or ["evidence", "adversarial_reasoning", "structure_and_depth"])
    if not isinstance(dimensions, list) or not dimensions or len(set(dimensions)) != len(dimensions) or any(d not in DIMENSIONS for d in dimensions):
        raise ValueError("perspectives must select distinct existing review perspectives.")
    if scope == "full_report" and perspectives not in (None, DIMENSIONS):
        raise ValueError("Whole-report review requires all seven distinct perspectives.")
    default_domains = ["domain"] if scope == "full_report" else []
    domains = (old.get("domains", default_domains) if old else default_domains) if domains is None else domains
    if not isinstance(domains, list) or any(not nonempty(d) for d in domains) or len(set(domains)) != len(domains):
        raise ValueError("domains must list the needed domain perspectives.")
    same_selection = (old and old.get('contract_version') == 2 and old.get('domains') == domains
        and old.get('purpose') == purpose
        and [s['slot_id'] for s in old['slots'] if s['role'] == 'reviewer' and s.get('dimensions') != ['domain']] == dimensions)
    packet, bindings = packet_for(root, progress, evidence_paths, artifact, scope, old if same_selection else None)
    version = digest({"packet": packet, "perspectives": dimensions, "domains": domains, "purpose": purpose})
    if old and old.get("input_version") != version and not revision:
        raise ValueError("The assignment changed; use revision=true for the current draft. Earlier originals remain retained.")
    input_ref = frozen(root, f"{run_prefix(version)}/input.json", packet)
    slots = [{"slot_id": d, "role": "reviewer", "dimensions": [d]} for d in dimensions]
    slots += [{"slot_id": "domain-" + str(i + 1), "role": "reviewer", "dimensions": ["domain"], "domain": d} for i, d in enumerate(domains)]
    if audit_required:
        slots.append({"slot_id": "audit", "role": "auditor"})
    if scope == "full_report":
        slots.append({"slot_id": "acceptance", "role": "acceptance"})
    plan = {"contract_version": 2, "purpose": purpose, "reviewer": "independent", "audit_required": audit_required,
            "author_id": progress["author_id"], "producer_contexts": producers(root, progress),
            "scope": scope, "artifact": artifact, "artifact_sha256": sha256_file(safe_path(root, artifact)),
            "input_version": version, "input": input_ref, "bindings": bindings, "domains": domains, "slots": slots,
            "instructions": (old["instructions"] if old and old.get("input_version") == version
                             and "instructions" in old else {role: methods(role) for role in ("reviewer", "auditor", "acceptance")})}
    if old and old.get("contract_version") == 2:
        if old.get("input_version") == version:
            if old.get("revision_context"):
                plan["revision_context"] = old["revision_context"]
        else:
            plan["revision_context"] = revision_context(root, old, packet, bindings)
    if old != plan:
        if old:
            frozen(root, "reviews/plans/" + digest(old) + ".json", old)
        frozen(root, "reviews/plans/" + digest(plan) + ".json", plan)
        if scope == "full_report":
            progress.update(review_plan=plan, stage="review", status="in_progress")
        else:
            progress.setdefault("unit_review_plans", {})[scope] = plan
        progress["review_contract"] = 2
        save(root, "state/progress.json", progress)
    selected = selected_results(root, plan)
    if host_result is not None:
        available = {s["slot_id"]: s for s in next_slots(plan, selected)}
        sid = host_result.get("slot_id") if isinstance(host_result, dict) else None
        if sid not in available:
            raise ValueError("host_result.slot_id is not a currently outstanding assignment.")
        request, request_ref = assignment(root, plan, available[sid], selected)
        accept_result(root, progress, plan, available[sid], request, request_ref, host_result, selected)
        selected = selected_results(root, plan)
    pending = next_slots(plan, selected)
    requests = []
    for slot in pending:
        request, request_ref = assignment(root, plan, slot, selected)
        requests.append({"slot_id": slot["slot_id"], "role": slot["role"],
                         "assignment_ref": request_ref, "assignment_version": request["assignment_version"],
                         **({"assignment": request} if include_assignment else {})})
    result = inspect(root, progress, artifact, plan=plan)
    if scope != "full_report":
        progress.setdefault("unit_reviews", {})[scope] = {
            "artifact_sha256": plan["artifact_sha256"], "input_version": version, "ok": result["ok"],
            "reviewers": [r["execution_id"] for r in selected.values()], "record_path": plan["input"]["path"]}
        save(root, "state/progress.json", progress)
    if scope == "full_report" and result["ok"]:
        summary = {"stage": "final", "scope": "global_final_delivery", "result": "pass",
                   "basis": selected["acceptance"]["result_data"]["basis"], "open_issues": [],
                   "artifact_sha256": plan["artifact_sha256"], "contract_version": 2,
                   "review_evidence": {k: r["response"] for k, r in selected.items()}}
        if not history(root) or history(root)[-1] != summary:
            append(root, summary)
    return {"task_directory": str(root), "input_version": version, "scope": scope,
            "assignments": requests, "reviews_complete": all(s["slot_id"] in selected for s in slots if s["role"] == "reviewer"),
            "delivery_ready": scope == "full_report" and purpose == "report_delivery" and result["ok"],
            "unit_ready": scope != "full_report" and result["ok"], "completion_check": result,
            "action_required": "host_agents" if pending else "revise" if not result["ok"] else None,
            "open_issues": result["findings"]}


def checked_files(root, plan):
    from record_changes import input_digest
    files = {name for name in plan["bindings"] if not name.startswith("record:")}
    for name, expected in plan["bindings"].items():
        if input_digest(root, name) != expected:
            raise ValueError(f"Reviewed input changed: {name}.")
    files.add(plan["input"]["path"])
    if reference(root, plan["input"]["path"]) != plan["input"]:
        raise ValueError("Frozen review input changed.")
    retained = plan.get("revision_context", {})
    previous_refs = [retained["input"]] if retained else []
    previous_refs.extend(row[key] for row in retained.get("reviews", {}).values()
                         for key in ("input", "response", "execution"))
    for ref in previous_refs:
        if reference(root, ref["path"]) != ref:
            raise ValueError("Retained revision context changed: " + ref["path"])
        files.add(ref["path"])
    for row in selected_results(root, plan).values():
        for key in ("input", "response", "execution"):
            if reference(root, row[key]["path"]) != row[key]:
                raise ValueError(f"Retained {key} changed for {row['slot_id']}.")
            files.add(row[key]["path"])
    return files


def inspect(root, progress, artifact, *, plan=None, require_report_ready=True):
    # Shared upstreams need one complete inspection per call, never a cached
    # approval across calls that could conceal changed files or review records.
    return _inspect(root, progress, artifact, plan=plan, require_report_ready=require_report_ready,
                    walk={"outputs": None, "completed": {}})


def _inspect(root, progress, artifact, *, plan, require_report_ready, walk):
    plan = plan or progress.get("review_plan", {})
    key = (artifact, digest(plan), require_report_ready)
    if key in walk["completed"]:
        return walk["completed"][key]
    findings = []
    selected = selected_results(root, plan) if plan.get("contract_version") == 2 else {}
    if plan.get("contract_version") != 2 or plan.get("artifact") != artifact:
        findings.append("The current artifact needs the independent host review contract.")
    else:
        try:
            checked_files(root, plan)
            content = [s for s in plan["slots"] if s["role"] == "reviewer"]
            if plan.get("audit_required") and not any(s["slot_id"] == "audit" and s["role"] == "auditor" for s in plan["slots"]):
                raise ValueError("The declared independent audit assignment is missing.")
            if plan["scope"] == "full_report" and not set(DIMENSIONS).issubset({s["slot_id"] for s in content}):
                raise ValueError("All seven independent perspectives are required.")
            if plan["scope"] == "full_report":
                if any(not any(s['slot_id'] == sid and s['role'] == role for s in plan['slots'])
                       for sid, role in [('audit', 'auditor'), ('acceptance', 'acceptance')]):
                    raise ValueError("Every full report requires separate independent audit and final acceptance assignments.")
                if any(not any(s['slot_id'] == d and s.get('dimensions') == [d] for s in content) for d in DIMENSIONS):
                    raise ValueError("Each required content perspective must retain its own assignment.")
                if len([s for s in content if s.get('dimensions') == ['domain']]) != len(plan.get('domains', [])):
                    raise ValueError("Declared domain reviews are incomplete.")
            if walk["outputs"] is None:
                walk["outputs"] = research_outputs(root, [], progress)
            contribution = next((x for x in walk["outputs"] if x['path'] == artifact), None)
            if contribution and contribution.get('unit_id'):
                if not contribution['complete']:
                    raise ValueError('The registered research unit is still incomplete: ' + contribution['unit_id'])
                issues = [issue for issue in contribution.get('readiness_issues', []) if issue != 'independent_review_pending']
                if issues:
                    raise ValueError('Research dependencies are not ready: ' + ', '.join(issues))
                for dependency in contribution.get('depends_on', []):
                    unit_plan = progress.get('unit_review_plans', {}).get(dependency)
                    if not unit_plan:
                        raise ValueError('Missing independent review of upstream research: ' + dependency)
                    upstream = _inspect(root, progress, unit_plan['artifact'], plan=unit_plan,
                                        require_report_ready=True, walk=walk)
                    if not upstream['ok']:
                        findings.extend('Upstream ' + dependency + ': ' + f for f in upstream['findings'])
            identities = []
            for slot in plan["slots"]:
                row = selected.get(slot["slot_id"])
                if row is None:
                    findings.append("Incomplete independent assignment: " + slot["slot_id"])
                    continue
                request, request_ref = assignment(root, plan, slot, selected, persist=False)
                if row["input"] != request_ref:
                    raise ValueError("Dependent review/audit/acceptance inputs changed: " + slot["slot_id"])
                original = json.loads(safe_path(root, row["response"]["path"]).read_text(encoding="utf-8"))
                if original != row["result_data"]:
                    raise ValueError("Stored judgment differs from the original response.")
                capture = load(root, row['execution']['path'])
                if (capture.get('host_task') != row['execution_id'] or capture.get('status') != 'completed'
                        or capture.get('assignment_version') != request['assignment_version']):
                    raise ValueError("Execution identity/version differs from the retained host capture.")
                validate_result(original, request)
                identities.append(row["execution_id"])
                if row["execution_id"] in producers(root, progress):
                    raise ValueError("An author/producer performed independent review.")
                if require_report_ready:
                    if slot["role"] == "reviewer" and plan["scope"] != "full_report" and not plan.get("audit_required"):
                        from check_review_completion import content_review_issues
                        findings.extend(content_review_issues(original, {}))
                    elif slot["role"] == "auditor" and (original["result"] != "valid" or original["report_verdict"] != "pass"):
                        findings.extend(original["open_issues"] or ["Independent audit has unresolved findings."])
                    elif slot["role"] == "acceptance" and original["result"] != "pass":
                        findings.extend(original["open_issues"] or ["Independent final acceptance did not pass."])
            if len(set(identities)) != len(identities):
                raise ValueError("Review perspectives, audit and acceptance must use distinct host contexts.")
        except (ValueError, OSError, KeyError, TypeError) as exc:
            findings.append(str(exc))
    result = {"ok": not findings, "flags": ["incomplete_independent_review"] if findings else [],
            "findings": findings, "required_slots": len(plan.get("slots", [])), "completed_slots": len(selected),
            "selected_attempts": {k: r["attempt_id"] for k, r in selected.items()},
            "independent_review": True, "record_consistency_checked": True,
            "reviewer": "independent", "review_strength": "independent"}
    walk["completed"][key] = result
    return result


def run_configured(workflow, root, progress, evidence_paths, artifact, purpose, revision,
                   include_assignment, host_result, scope, perspectives, domains, config, runner, audit=None):
    """Optional existing backend bridge; the same assignments and completion contract apply."""
    from review_runner import backend_kind, ReviewFailure
    if any(backend_kind(c) == "self" for c in config["reviewers"]):
        raise ValueError("Author self-review cannot satisfy independent assignments. Use native host agents.")
    result = review(workflow, root, progress, evidence_paths, artifact, purpose, revision,
                    False, host_result, scope, perspectives, domains, audit)
    while result["assignments"]:
        for job in result["assignments"]:
            request = load(root, job["assignment_ref"]["path"])
            role = job["role"]
            default = config["reviewers"][0]
            selected = (config.get("auditor", default) if role == "auditor" else
                        config.get("acceptance", default) if role == "acceptance" else
                        next((c for c in config["reviewers"] if c["id"] == job["slot_id"]), default))
            prefix = f"{run_prefix(result['input_version'])}/backend/{uuid.uuid4().hex[:16]}"
            cwd = safe_path(root, prefix)
            cwd.mkdir(parents=True, exist_ok=True)
            try:
                returned = runner(selected, request, cwd)
            except ReviewFailure as exc:
                save(root, prefix + "/execution.json", exc.capture)
                result.update(failure=str(exc), retained_execution=prefix + "/execution.json")
                return result
            save_text(root, prefix + "/response.txt", returned["content"])
            save(root, prefix + "/execution.json", {**returned["capture"], "host_task": returned["execution_id"],
                "status": "completed", "assignment_version": request["assignment_version"]})
            result = review(workflow, root, load(root, "state/progress.json"), evidence_paths, artifact,
                purpose, False, False, {"slot_id": job["slot_id"], "host_task": returned["execution_id"],
                    "response_path": prefix + "/response.txt", "execution_path": prefix + "/execution.json"},
                scope, perspectives, domains, audit)
            if role == 'auditor' and any(item['role'] == 'reviewer' for item in result['assignments']):
                result['action_required'] = 'repair_review'
                result['recovery'] = 'The audit identified incomplete or invalid review work. Repair that assignment before continuing; its original result is retained.'
                return result
        # A completed negative assessment ends here. No automatic reroll for a pass.
        if result.get("action_required") != "host_agents":
            break
    return result
