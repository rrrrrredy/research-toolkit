"""Version-bound review assignments executed by the agent tool's independent agents.

The agent tool owns spawning, waiting and cancellation. This module reuses the task's
source reader, storage and review log; it never starts a second agent runtime.
"""
from __future__ import annotations

import json
import re
import uuid
from difflib import SequenceMatcher
from pathlib import Path

from task_storage import digest, load, nonempty, safe_path, save, save_text
from task_context import current_work, task_inputs, research_outputs, prepare_work
from run_observation import now

DIMENSIONS = ["requirements", "evidence", "adversarial_reasoning", "structure_and_depth",
              "reader_usefulness", "process_language", "natural_expression"]
REVIEW_GROUPS = {
    "requirements_and_usefulness": ["requirements", "structure_and_depth", "reader_usefulness"],
    "evidence_and_reasoning": ["evidence", "adversarial_reasoning"],
    "process_and_expression": ["process_language", "natural_expression"],
}
NATIVE_CONTRACTS = {2, 3}
GENERATED_REGISTRIES = {"data/source_registry.csv", "data/claims_registry.csv"}
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


def required_findings(row):
    """Read necessary criticism from its original result, without a second issue ledger."""
    if row.get('record_type') == 'model_review':
        return [finding for finding in row.get('findings', []) if finding.get('severity') != 'optional']
    if row.get('record_type') not in {'review_audit', 'final_blind_review', 'final_acceptance'}:
        return []
    value = row.get('result_data', {})
    findings = []
    fields = (('critical_checks', 'sample_checks', 'open_issues') if row['record_type'] == 'review_audit'
              else ('sample_checks', 'open_issues'))
    for field in fields:
        for index, item in enumerate(value.get(field, [])):
            if field != 'open_issues' and item.get('result') != 'defect':
                continue
            pointer = f'{field}/{index}'
            findings.append({'finding_id': pointer, 'severity': 'required',
                'location': item.get('location', pointer) if isinstance(item, dict) else pointer,
                'basis': item, 'original_location': row['response']['path'] + '#/' + pointer})
    # A negative overall judgment without a structured new defect must not
    # disappear either. Do not duplicate findings already identified by the
    # audit's current or historical dispositions.
    negative = value.get('report_verdict') == 'needs_revision' or value.get('result') == 'fail'
    expanded = row.get('expanded_decisions', value)
    already_identified = (any(d.get('decision') != 'no_change' for d in expanded.get('dispositions', {}).values())
                          or any(d.get('decision') == 'unresolved' for d in expanded.get('prior_findings', {}).values()))
    if negative and not findings and not already_identified:
        findings.append({'finding_id': 'basis', 'severity': 'required', 'location': 'basis',
            'basis': value['basis'], 'original_location': row['response']['path'] + '#/basis'})
    return findings


def report_changes(previous, current):
    before, after = previous.splitlines(), current.splitlines()
    return [{"change": kind,
             "previous_lines": [i + 1, j] if j > i else None,
             "current_lines": [k + 1, n] if n > k else None,
             "previous_text": "\n".join(before[i:j]), "current_text": "\n".join(after[k:n])}
            for kind, i, j, k, n in SequenceMatcher(None, before, after, autojunk=False).get_opcodes()
            if kind != "equal"]


def revision_context(root, previous_plan, packet, bindings):
    """Point the next review agent to retained work; never reuse its approval."""
    previous = load(root, previous_plan["input"]["path"])
    selected = selected_results(root, previous_plan)
    audits = effective_audit(selected).get("result_data", {}).get("review_checks", {})
    reviews = {}
    for slot in previous_plan["slots"]:
        row = selected.get(slot["slot_id"])
        if slot["slot_id"] == "audit":
            row = effective_audit(selected) or None
        validity = audits.get(slot["slot_id"], {}).get("result")
        if slot["role"] == "reviewer" and validity == "invalid":
            continue
        if row:
            reviews[slot["slot_id"]] = {"attempt_id": row["attempt_id"], "response": row["response"],
                "input": row["input"], "execution": row["execution"], "execution_id": row["execution_id"],
                "role": slot["role"],
                "report_verdict": row.get("report_verdict", row.get("result_data", {}).get("report_verdict",
                    row.get("result_data", {}).get("result"))),
                "review_validity": validity or "not_separately_audited"}
        else:
            retained = previous_plan.get("revision_context", {}).get("reviews", {}).get(slot["slot_id"])
            if retained:
                reviews[slot["slot_id"]] = dict(retained)
        if slot["slot_id"] in reviews:
            retained = reviews[slot["slot_id"]]
            original = load(root, retained["input"]["path"])
            # Read the actual earlier responsibility, including across versions
            # prepared without a reply. Do not relabel it after a domain change.
            retained.update(input_version=original["input_version"],
                            dimensions=original["dimensions"], domain=original.get("domain"))
    old_bindings = previous_plan.get("bindings", {})
    names = sorted(set(old_bindings) | set(bindings))
    return {"historical_only": True, "input": previous_plan["input"],
            "input_version": previous_plan["input_version"], "reviews": reviews,
            "changed_inputs": [{"path": name, "previous_sha256": old_bindings.get(name),
                                "current_sha256": bindings.get(name)} for name in names
                               if old_bindings.get(name) != bindings.get(name)],
            "unchanged_inputs": [name for name in names if old_bindings.get(name) == bindings.get(name)],
            "report_changes": report_changes(previous["report"], packet["report"])}


def prior_final_for_correction(root, old, packet, bindings, producers):
    previous = load(root, old["input"]["path"])
    if (packet["report"] == previous["report"]
            or any(packet[key] != previous[key] for key in ("task", "report_path", "source_files", "scope_decisions"))
            or bindings["record:requirements:effective"] != old["bindings"]["record:requirements:effective"]):
        return None
    if (previous["sources"].keys() != packet["sources"].keys()
            or any(previous["sources"][name] != text for name, text in packet["sources"].items()
                   if name != "data/claims_registry.csv")):
        return None
    selected = selected_results(root, old)
    continuation = old.get("final_continuation", {})
    failed = selected.get("acceptance") or continuation.get("failed")
    blind = selected.get("acceptance_blind") or continuation.get("blind")
    if (not failed or failed["result_data"]["result"] != "fail" or not blind
            or blind["execution_id"] != failed["execution_id"] or failed["execution_id"] in producers):
        return None
    for row in (blind, failed):
        for field in ("input", "response", "execution"):
            ref = row[field]
            if reference(root, ref["path"]) != ref:
                raise ValueError("Retained final review evidence changed: " + ref["path"])
        request = load_assignment(root, row["input"]["path"])
        original = json.loads(response_text(root, row))
        execution = json.loads(safe_path(root, row["execution"]["path"]).read_text(encoding="utf-8-sig"))
        if (request["role"] != "acceptance" or request["phase"] != row["phase"] or original != row["result_data"]
                or request["input_version"] != row["input_version"] or execution.get("host_task") != row["execution_id"]
                or execution.get("status") != "completed" or execution.get("assignment_version") != request["assignment_version"]):
            raise ValueError("Retained final review identity or version does not match its original inputs.")
        validate_result(original, request)
    if blind["phase"] != "blind" or failed["phase"] not in {"reconcile", "correction_review"}:
        return None
    return {"blind": blind, "failed": failed}


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
             "artifact_sha256": r["artifact_sha256"], "response": r["response"],
             "input": r["input"], "execution": r["execution"], "finding": f}
            for r in history(root) if r.get("contract_version") in NATIVE_CONTRACTS
            and r.get("scope") == scope and r.get("status") == "completed"
            for f in required_findings(r)]
    for finding in packet['prior_required_findings']:
        # Old frozen packets keep their original contract. New packets bind all
        # three retained originals on every call, including result ingestion.
        if 'input' not in finding:
            continue
        for key in ('input', 'response', 'execution'):
            ref = finding[key]
            if reference(root, ref['path']) != ref:
                raise ValueError('Retained finding original changed: ' + ref['path'])
            bindings[ref['path']] = ref['sha256']
    bindings.update({name: sha256_file(safe_path(root, name)) for name in [artifact, *analyses]})
    bindings.update(binaries)
    return packet, bindings


def result_key(slot):
    return {"blind": "acceptance_blind", "adjudicate": "audit_adjudication"}.get(slot.get("phase"), slot["slot_id"])


def effective_audit(selected):
    return selected.get("audit_adjudication", selected.get("audit", {}))


def assessment_steps(plan, selected):
    if plan["contract_version"] == 2:
        return plan["slots"]
    reviewers = [slot for slot in plan["slots"] if slot["role"] == "reviewer"]
    auditor = next(slot for slot in plan["slots"] if slot["slot_id"] == "audit")
    acceptance = next(slot for slot in plan["slots"] if slot["slot_id"] == "acceptance")
    steps = [*reviewers, {**auditor, "phase": "initial"}]
    requests = selected.get("audit", {}).get("result_data", {}).get("verification_requests", [])
    if requests:
        steps.extend({"slot_id": "verify-" + item["request_id"], "role": "verifier", "verification": item}
                     for item in requests)
        steps.append({**auditor, "phase": "adjudicate"})
    if plan.get("final_continuation"):
        return [*steps, {**acceptance, "phase": "correction_review"}]
    return [*steps, {**acceptance, "phase": "blind"}, {**acceptance, "phase": "reconcile"}]


def selected_results(root, plan):
    selected = {}
    for row in history(root):
        if (row.get("contract_version") == plan["contract_version"] and row.get("input_version") == plan["input_version"]
                and row.get("scope") == plan["scope"] and row.get("status") == "completed"):
            selected[result_key(row)] = row
    # Reject dependent work whose review, blind, audit or verification inputs changed.
    for slot in assessment_steps(plan, selected):
        key = result_key(slot)
        if slot["role"] == "reviewer" or key not in selected:
            continue
        try:
            _, expected = assignment(root, plan, slot, selected, persist=False)
            if selected[key]["input"] != expected:
                selected.pop(key)
        except (KeyError, TypeError):
            selected.pop(key)
    return {key: selected[key] for slot in assessment_steps(plan, selected)
            if (key := result_key(slot)) in selected}


def response_text(root, row):
    return safe_path(root, row["response"]["path"]).read_text(encoding="utf-8-sig")


def retained_result(root, row):
    return {"record": row, "original": response_text(root, row)}


def current_findings(reviews):
    return {key + "/" + f["finding_id"]: f for key, review in reviews.items()
            for f in review["record"].get("findings", [])}


def blind_input(packet):
    return {"task": packet["task"], "report_path": packet["report_path"], "report": packet["report"],
            "sources": {path: content for path, content in packet["sources"].items() if path not in GENERATED_REGISTRIES},
            "source_files": packet["source_files"],
            "effective_requirements": [{k: v for k, v in row.items() if k not in {"status", "evidence"}}
                                       for row in packet["effective_requirements"]]}


def audit_scaffold(request):
    current = current_findings(request["reviews"])
    possible_duplicates = {}
    for key, finding in current.items():
        signature = (finding["location"].strip().casefold(), " ".join(finding["basis"].split()).casefold())
        possible_duplicates.setdefault(signature, []).append(key)
    return {"current_findings": current,
            "candidate_groups": [keys for keys in possible_duplicates.values() if len(keys) > 1],
            "prior_finding_ids": [item["attempt_id"] + "/" + item["finding"]["finding_id"]
                                  for item in request["assignment"]["prior_required_findings"]],
            "effective_requirement_ids": [row.get("requirement_id") for row in request["assignment"]["effective_requirements"]],
            "source_paths": sorted((set(request["assignment"]["sources"]) | set(request["assignment"]["source_files"]))
                                   - GENERATED_REGISTRIES)}


def methods(role):
    from research_guidance import guidance
    names = {"reviewer": ["review"], "auditor": ["audit"], "acceptance": ["acceptance"]}
    return "\n\n".join(x["content"] for x in guidance("review", methods=names[role])["guidance"])


def load_assignment(root, name):
    """Read a role assignment with its complete, verified frozen input."""
    request = load(root, name)
    if "shared_input" in request:
        shared = request.pop("shared_input")
        if reference(root, shared["path"]) != shared:
            raise ValueError("Frozen role input changed: " + shared["path"])
        request["assignment"] = load(root, shared["path"])
    return request


def assignment(root, plan, slot, selected, *, persist=True):
    phase = slot.get("phase")
    input_ref = plan["blind_input"] if phase == "blind" else plan["input"]
    packet = load(root, input_ref["path"])
    role = slot["role"]
    request = {"contract_version": plan["contract_version"], "role": role, "slot_id": slot["slot_id"], "input_version": plan["input_version"],
               "artifact_sha256": plan["artifact_sha256"], "scope": plan["scope"],
               "dimensions": slot.get("dimensions", []), "assignment": packet,
               "instructions": plan["instructions"].get(role, "")}
    if phase:
        request["phase"] = phase
    if phase == "blind":
        request["instructions"] = (
            "Independently assess the complete current report against the original requirements and evidence. "
            "Use a fresh agent context. Do not read author conclusions outside the report, reviews, audit, prior "
            "verdicts or correction history. Commit your own evidence-based judgment before receiving those results. "
            "Return result pass/fail, basis, coverage keyed by all seven content dimensions (location and basis), "
            "sample_checks (location, selection_reason, evidence, result clear/defect and expansion for defects), and open_issues.")
    elif role == "verifier":
        verification = slot["verification"]
        paths = set(verification["evidence_paths"])
        request["assignment"] = {
            "question": verification["question"], "location": verification["location"],
            "sources": {path: content for path, content in packet["sources"].items() if path in paths},
            "source_files": {path: ref for path, ref in packet["source_files"].items() if path in paths}}
        request["audit_binding"] = selected["audit"]["response"]["sha256"]
        request["instructions"] = (
            "In a fresh context, verify this neutral question from the listed original material, independently "
            "recomputing when applicable. Retain actual source locations and evidence. Do not read the report, prior "
            "judgments, or audit history. Return result (supported, contradicted, or insufficient), basis, and a "
            "nonempty evidence list with path, locator and observation for each check.")
    elif plan.get("revision_context"):
        retained = plan["revision_context"]
        previous = retained["reviews"].get(slot["slot_id"])
        same_work = (previous and previous.get("role") == role
                     and previous.get("dimensions") == slot.get("dimensions", [])
                     and previous.get("domain") == slot.get("domain"))
        request["revision_context"] = {**retained, "reviews": (
            {slot["slot_id"]: previous}
            if role == "reviewer" and previous and (same_work or "dimensions" not in previous) else
            {} if role == "reviewer" else retained["reviews"])}
        request["instructions"] += ("\nUse the retained previous response and frozen input to recover checks already performed. "
            "The change locations and input hashes help find what changed; they do not decide its substantive impact. "
            "Confirm the current complete artifact in your assigned perspective, inspect affected evidence and cross-part effects, "
            "and reuse unchanged reading where appropriate. Historical results are not current approval.")
        if same_work:
            before = load_assignment(root, previous["input"]["path"])["assignment"]
            context = request["revision_context"]
            context["report_changes"] = report_changes(before["report"], packet["report"])
            sections = ("sources", "source_files", "analyses")
            context["changed_materials"] = [
                {"section": section, "path": name} for section in sections
                for name in sorted(set(before.get(section, {})) | set(packet.get(section, {})))
                if before.get(section, {}).get(name) != packet.get(section, {}).get(name)]
            context["changed_context"] = [name for name in sorted(set(before) | set(packet))
                if name not in {*sections, "report"} and before.get(name) != packet.get(name)]
            if previous["execution_id"] not in plan.get("producer_contexts", []):
                request["resume_host_task"] = previous["execution_id"]
            request["instructions"] += (
                "\nContinue the retained assessment in its original independent agent task when available. "
                "report_changes, changed_materials and changed_context compare the current input with the input "
                "you actually reviewed, even after intervening revisions. Reuse the original supported analysis; "
                "check these changes and their effect on your responsibility for the current complete report. "
                "If the agent task is unavailable, give this retained work to a new independent context.")
    if slot.get("domain"):
        request["domain"] = slot["domain"]
    if role == "reviewer":
        from research_workflow import REVIEW_INSTRUCTIONS
        request["instructions"] += "\n" + REVIEW_INSTRUCTIONS
        request["instructions"] += ("\nYour assigned perspective is " + slot["slot_id"] +
            ". Read the complete supplied draft and relevant originals. Do the assigned substantive assessment "
            "in a context separate from every producer and the other perspectives. Do not edit the draft.")
        if 'structure_and_depth' in slot.get('dimensions', []) and 'production_history' in packet:
            request['instructions'] += ("\nWhen the task requires progressive research or writing, inspect production_history "
                "and its retained drafts against the requested progression; save counts alone do not establish substantive stages.")
    elif role != "verifier" and phase != "blind":
        content = {s["slot_id"]: selected[s["slot_id"]] for s in plan["slots"] if s["role"] == "reviewer"}
        request["reviews"] = {key: retained_result(root, value) for key, value in content.items()}
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
            if phase:
                request["audit_scaffold"] = audit_scaffold(request)
                request["instructions"] += (
                    "\nThe scaffold lists original canonical finding IDs. Candidate groups are only suggestions. "
                    "Explicitly choose groups only when your independently checked reason and evidence apply to every "
                    "member. Use disposition_groups and prior_finding_groups (lists of objects with finding_ids, "
                    "decision, reason and evidence), individual decisions in the existing maps, or both without "
                    "overlap. Locate and adjudicate every ID. Resolve conflicts by evidence, not by the number of "
                    "agreeing reviewers.")
                if phase == "initial":
                    request["instructions"] += (
                        "\nOnly when a consequential conclusion remains unresolved after you inspect the originals, request "
                        "fresh blind verification. Each verification_requests item has request_id (lowercase letters, "
                        "digits, hyphen or underscore), neutral question, report location, decision_impact, and evidence_paths "
                        "from the task's frozen originals. Include no prior verdict in the question. Such a request leaves "
                        "report_verdict needs_revision. Otherwise omit verification_requests or return [].")
                else:
                    initial = selected["audit"]
                    request["resume_host_task"] = initial["execution_id"]
                    request["preliminary_audit"] = retained_result(root, initial)
                    request["verifications"] = {item["request_id"]: retained_result(root, selected["verify-" + item["request_id"]])
                                                for item in initial["result_data"]["verification_requests"]}
                    request["instructions"] += (
                        "\nAdjudicate each returned blind verification with the source evidence. Return verification_decisions "
                        "keyed by every request ID (decision resolved/unresolved, reason, evidence). Resolve a conflict "
                        "only with an independently supported finding or a properly supported limitation. Do not request "
                        "another verification on this same frozen input; identify any repair or missing evidence instead.")
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
            audit = effective_audit(selected)
            request["audit"] = retained_result(root, audit)
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
            if phase == "reconcile":
                blind = selected["acceptance_blind"]
                request["blind_assessment"] = retained_result(root, blind)
                request["resume_host_task"] = blind["execution_id"]
                request["blind_issue_ids"] = [item["finding_id"] for item in required_findings(blind)]
                request["instructions"] += (
                    "\nReconcile your retained blind assessment with the actual review and audit evidence. Return "
                    "blind_reconciliation keyed by every blind_issue_ids entry (decision confirmed_defect, no_change "
                    "or unresolved; reason; evidence). A pass must establish why each retained blind concern requires "
                    "no further change to this exact draft. Keep justified disagreement visible.")
            elif phase == "correction_review":
                retained = plan["final_continuation"]
                previous = retained["failed"]
                request["resume_host_task"] = previous["execution_id"]
                request["prior_final"] = {key: retained_result(root, row) for key, row in retained.items()}
                request["prior_final_issue_ids"] = [item["finding_id"] for item in required_findings(previous)]
                request["instructions"] += (
                    "\nYou already performed an independent blind check and reported defects before this revision. "
                    "Verify your earlier issues against the latest full report, original sources and current audit. "
                    "Review changes and their implications across the whole report, including new defects. This is a "
                    "current-version continuation, not a new blind assessment. Return prior_final_reconciliation for "
                    "each prior_final_issue_ids entry (decision resolved, no_change or unresolved; reason; evidence). "
                    "Pass only if substantive checks and all earlier issues are resolved or need no change.")
    request["instructions"] += "\nReturn input_version and assignment_version exactly as supplied, alongside the requested assessment fields."
    request["assignment_version"] = digest(request)
    name = f"{run_prefix(plan['input_version'])}/jobs/{slot['slot_id']}-{request['assignment_version'][:16]}.json"
    if safe_path(root, name).is_file() and load_assignment(root, name) == request:
        # Preserve originally saved inline assignments and their checksums.
        ref = reference(root, name)
    elif persist:
        stored = request if role == "verifier" else {**{k: v for k, v in request.items() if k != "assignment"},
                                                      "shared_input": input_ref}
        ref = frozen(root, name, stored)
    else:
        ref = {"path": name, "sha256": "unrecorded_assignment"}
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


def decision_map(value, field, expected, choices, group_field=None):
    decisions = value.get(field, {})
    if not isinstance(decisions, dict):
        raise ValueError(f"{field} must map finding IDs to evidenced decisions.")
    decisions = dict(decisions)
    if group_field:
        groups = value.get(group_field, [])
        if not isinstance(groups, list):
            raise ValueError(f"{group_field} must list explicitly accepted groups.")
        for group in groups:
            ids = group.get("finding_ids") if isinstance(group, dict) else None
            if not isinstance(ids, list) or not ids or any(not nonempty(key) for key in ids):
                raise ValueError(f"{group_field} needs at least one canonical ID per group.")
            for key in ids:
                if key in decisions:
                    raise ValueError(f"{field} cannot repeat a decision for {key}.")
                decisions[key] = {k: group.get(k) for k in ("decision", "reason", "evidence")}
    if set(decisions) != set(expected):
        raise ValueError(f"{field} must account for every canonical ID exactly once.")
    for item in decisions.values():
        if (not isinstance(item, dict) or item.get("decision") not in choices
                or not all(nonempty(item.get(k)) for k in ("reason", "evidence"))):
            raise ValueError(f"{field} needs an independent decision with reasons and evidence.")
    return decisions


def validate_verification_requests(value, request):
    requests = value.get("verification_requests", [])
    if not isinstance(requests, list):
        raise ValueError("verification_requests must list consequential unresolved questions.")
    if requests and (request.get("phase") != "initial" or value["result"] != "valid"
                     or value["report_verdict"] != "needs_revision"):
        raise ValueError("Only a valid initial audit with unresolved report issues can request blind verification.")
    packet = request["assignment"]
    paths = (set(packet["sources"]) | set(packet["source_files"])) - GENERATED_REGISTRIES
    seen = set()
    for item in requests:
        if (not isinstance(item, dict) or not all(nonempty(item.get(k)) for k in
                ("request_id", "question", "location", "decision_impact"))
                or not re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,31}", item["request_id"])
                or item["request_id"] in seen):
            raise ValueError("Each blind request needs a unique ID, neutral question, location and material decision impact.")
        chosen = item.get("evidence_paths")
        if (not isinstance(chosen, list) or not chosen or any(not nonempty(name) for name in chosen)
                or len(set(chosen)) != len(chosen) or not set(chosen).issubset(paths)):
            raise ValueError("Blind verification needs distinct originals from the current frozen evidence.")
        seen.add(item["request_id"])


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
    if role == "verifier":
        paths = set(request["assignment"]["sources"]) | set(request["assignment"]["source_files"])
        evidence = value.get("evidence")
        if (value.get("result") not in {"supported", "contradicted", "insufficient"} or not nonempty(value.get("basis"))
                or not isinstance(evidence, list) or not evidence or any(
                    not isinstance(item, dict) or not all(nonempty(item.get(k)) for k in ("path", "locator", "observation"))
                    or item["path"] not in paths for item in evidence)):
            raise ValueError("Blind verification needs an independent judgment with actual locations in the supplied originals.")
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
        if request.get("phase") == "reconcile":
            reconciliation = decision_map(value, "blind_reconciliation", request["blind_issue_ids"],
                                          {"no_change", "confirmed_defect", "unresolved"})
            if value["result"] == "pass" and any(item["decision"] != "no_change" for item in reconciliation.values()):
                raise ValueError("Acceptance cannot pass with an unresolved or confirmed blind finding.")
        if request.get("phase") == "correction_review":
            reconciliation = decision_map(value, "prior_final_reconciliation", request["prior_final_issue_ids"],
                                          {"resolved", "no_change", "unresolved"})
            if value["result"] == "pass" and any(item["decision"] == "unresolved" for item in reconciliation.values()):
                raise ValueError("Final correction review cannot pass with an unresolved earlier finding.")
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
    expected = current_findings(reviews)
    grouped = request["contract_version"] == 3
    if not grouped and "dispositions" not in value:
        raise ValueError("Audit dispositions must cover every actual current finding exactly once.")
    dispositions = decision_map(value, "dispositions", expected, {"confirmed_defect", "no_change", "unresolved"},
                                "disposition_groups" if grouped else None)
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
    decisions = decision_map(value, "prior_findings", wanted, {"resolved", "no_change", "unresolved"},
                              "prior_finding_groups" if grouped else None)
    verification_decisions = {}
    if grouped:
        validate_verification_requests(value, request)
        if request.get("phase") == "adjudicate":
            verification_decisions = decision_map(value, "verification_decisions", request["verifications"],
                                                  {"resolved", "unresolved"})
    required_open = any(f.get("severity") != "optional" and dispositions[k]["decision"] != "no_change" for k, f in expected.items())
    from check_review_completion import content_review_issues
    unresolved_review = any(content_review_issues(v['record'], {
        f['finding_id']: dispositions[key + '/' + f['finding_id']]
        for f in v['record'].get('findings', [])}) for key, v in reviews.items())
    if value["report_verdict"] == "pass" and (value["open_issues"] or required_open or unresolved_review
            or any(d["decision"] == "unresolved" for d in decisions.values())
            or any(d["decision"] == "unresolved" for d in verification_decisions.values())
            or any(c["result"] == "defect" for c in [*critical, *value["sample_checks"]])):
        raise ValueError("Report readiness cannot pass with unresolved required findings or actual failed checks.")
    if grouped:
        return {"dispositions": dispositions, "prior_findings": decisions}


def accept_result(root, progress, plan, slot, request, request_ref, supplied, selected):
    if not isinstance(supplied, dict) or any(not nonempty(supplied.get(k)) for k in ("slot_id", "host_task", "response_path", "execution_path")):
        raise ValueError("host_result needs slot_id, actual host_task, response_path and execution_path.")
    identity = supplied["host_task"]
    if identity in producers(root, progress):
        raise ValueError("A production/assembly context cannot perform independent review, audit or acceptance.")
    phase = slot.get("phase")
    if phase == "correction_review" and identity != request["resume_host_task"]:
        raise ValueError("Final correction review must resume its original independent context.")
    for row in history(root):
        if row.get("contract_version") not in NATIVE_CONTRACTS or row.get("execution_id") != identity:
            continue
        if row.get("slot_id") != slot["slot_id"]:
            raise ValueError("Different review groups, audit, verification and acceptance need different agent contexts.")
        if (phase == "blind" or slot["role"] == "verifier") and row.get("status") == "completed":
            raise ValueError("A blind assessment or verification needs a fresh agent context.")
    previous = selected.get(result_key(slot))
    if previous:
        audit = effective_audit(selected).get("result_data", {})
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
    record_type = {"reviewer": "model_review", "auditor": "review_audit", "acceptance": "final_acceptance",
                   "verifier": "blind_verification"}[slot["role"]]
    if phase == "blind":
        record_type = "final_blind_review"
    row = {"record_type": record_type, "contract_version": plan["contract_version"],
           "attempt_id": attempt, "slot_id": slot["slot_id"], "role": slot["role"],
           **({"phase": phase} if phase else {}),
           "scope": plan["scope"], "input_version": plan["input_version"], "artifact_sha256": plan["artifact_sha256"],
           "input": request_ref, "execution_id": identity, "response": reference(root, prefix + "/response.txt"),
           "execution": reference(root, prefix + "/execution.json"), "recorded_at": now()}
    try:
        execution = json.loads(execution_raw.decode("utf-8-sig"))
        if (execution.get("host_task") != identity or execution.get("status") != "completed"
                or execution.get("assignment_version") != request["assignment_version"]):
            raise ValueError("execution_path must retain the actual completed agent identity and assignment_version.")
        value = json.loads(raw.decode("utf-8-sig"))
        expanded = validate_result(value, request)
        row.update(status="completed", result_data=value)
        if expanded is not None:
            row["expanded_decisions"] = expanded
        if slot["role"] == "reviewer":
            row.update({k: value[k] for k in ("report_verdict", "coverage", "findings")})
    except (ValueError, UnicodeError, AttributeError, TypeError) as exc:
        row.update(status="incomplete", failure=str(exc))
        append(root, row)
        raise ValueError(f"Original agent result retained at {prefix}; {exc}") from exc
    append(root, row)


def next_slots(plan, selected):
    if plan["contract_version"] == 3:
        steps = assessment_steps(plan, selected)
        missing = [step for step in steps if step["role"] == "reviewer"
                   and result_key(step) not in selected]
        if missing:
            return missing
        if "audit" not in selected:
            return [step for step in steps if step.get("phase") == "initial"]
        audit = effective_audit(selected)["result_data"]
        invalid = [step for step in steps if step["role"] == "reviewer"
                   and audit["review_checks"][step["slot_id"]]["result"] == "invalid"]
        if invalid:
            return invalid
        if audit["result"] != "valid":
            return []
        outstanding = [step for step in steps if step["role"] == "verifier" and result_key(step) not in selected]
        if outstanding:
            return outstanding
        if "audit_adjudication" not in selected:
            adjudication = [step for step in steps if step.get("phase") == "adjudicate"]
            if adjudication:
                return adjudication
        if "acceptance" in selected or (plan["purpose"] == "report_delivery" and audit["report_verdict"] != "pass"):
            return []
        phase = ("correction_review" if plan.get("final_continuation") else
                 "reconcile" if "acceptance_blind" in selected else "blind")
        return [step for step in steps if step.get("phase") == phase]
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
    if value["result"] != "valid" or (plan["purpose"] == "report_delivery" and value["report_verdict"] != "pass"):
        return []
    return [s for s in plan["slots"] if s["role"] == "acceptance" and s["slot_id"] not in selected]


def review(workflow, root, progress, evidence_paths, artifact, purpose, revision, include_assignment,
           host_result=None, scope="full_report", perspectives=None, domains=None, audit=None, *,
           fresh_final=False, allow_final_continuation=True):
    from check_delivery import sha256_file
    if scope == "full_report":
        workflow.require_current_artifact(progress, artifact)
        current = progress.get("current_artifact", {})
        if current.get("path") != artifact or not nonempty(current.get("owner")):
            raise ValueError("Register the main draft's actual producer before independent review: "
                "save draft.path, draft.main=true and draft.host_task with the real producing agent task/session. "
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
    version_number = 2
    if scope == "full_report":
        version_number = ((old or {}).get("contract_version") if (old or {}).get("contract_version") in NATIVE_CONTRACTS
                          else 3 if progress.get("review_contract") == 3 else 2)
    if audit is not None and type(audit) is not bool:
        raise ValueError("audit must be true or false when supplied.")
    audit_required = scope == "full_report" or bool(old and old.get("audit_required")) or audit is True
    if audit is False and audit_required:
        raise ValueError("audit cannot disable whole-report audit or an already declared unit audit.")
    default_dimensions = ([s["slot_id"] for s in (old or {}).get("slots", [])
                           if s["role"] == "reviewer" and s.get("dimensions") != ["domain"]]
                          or ["evidence", "adversarial_reasoning", "structure_and_depth"])
    dimensions = DIMENSIONS if scope == "full_report" else (default_dimensions if perspectives is None else perspectives)
    if not isinstance(dimensions, list) or not dimensions or len(set(dimensions)) != len(dimensions) or any(d not in DIMENSIONS for d in dimensions):
        raise ValueError("perspectives must select distinct existing review perspectives.")
    if scope == "full_report" and perspectives not in (None, DIMENSIONS):
        raise ValueError("Whole-report review requires all seven distinct perspectives.")
    default_domains = ["domain"] if scope == "full_report" and version_number == 2 else []
    domains = (old.get("domains", default_domains) if old else default_domains) if domains is None else domains
    if not isinstance(domains, list) or any(not nonempty(d) for d in domains) or len(set(domains)) != len(domains):
        raise ValueError("domains must list the needed domain perspectives.")
    groups = REVIEW_GROUPS if version_number == 3 else {dimension: [dimension] for dimension in dimensions}
    same_selection = (old and old.get('contract_version') == version_number and old.get('domains') == domains
        and old.get('purpose') == purpose
        and [s['slot_id'] for s in old['slots'] if s['role'] == 'reviewer' and s.get('dimensions') != ['domain']] == list(groups))
    packet, bindings = packet_for(root, progress, evidence_paths, artifact, scope, old if same_selection else None)
    version = digest({"packet": packet, "perspectives": dimensions, "domains": domains, "purpose": purpose,
                      **({"review_groups": groups} if version_number == 3 else {})})
    if fresh_final and (not old or old["input_version"] != version or not old.get("final_continuation")
                        or host_result is not None or "acceptance" in selected_results(root, old)):
        raise ValueError("Only an unfinished final correction review can switch to a fresh blind assessment.")
    if old and old.get("input_version") != version and not revision:
        raise ValueError("The assignment changed; use revision=true for the current draft. Earlier originals remain retained.")
    input_ref = frozen(root, f"{run_prefix(version)}/input.json", packet)
    slots = [{"slot_id": name, "role": "reviewer", "dimensions": lenses} for name, lenses in groups.items()]
    slots += [{"slot_id": "domain-" + str(i + 1), "role": "reviewer", "dimensions": ["domain"], "domain": d} for i, d in enumerate(domains)]
    if audit_required:
        slots.append({"slot_id": "audit", "role": "auditor"})
    if scope == "full_report":
        slots.append({"slot_id": "acceptance", "role": "acceptance"})
    plan = {"contract_version": version_number, "purpose": purpose, "reviewer": "independent", "audit_required": audit_required,
            "author_id": progress["author_id"], "producer_contexts": producers(root, progress),
            "scope": scope, "artifact": artifact, "artifact_sha256": sha256_file(safe_path(root, artifact)),
            "input_version": version, "input": input_ref, "bindings": bindings, "domains": domains, "slots": slots,
            "instructions": (old["instructions"] if old and old.get("input_version") == version
                             and "instructions" in old else {role: methods(role) for role in ("reviewer", "auditor", "acceptance")})}
    if version_number == 3:
        plan["blind_input"] = frozen(root, f"{run_prefix(version)}/blind-input.json", blind_input(packet))
    if old and old.get("contract_version") == version_number:
        if old.get("input_version") == version:
            if old.get("revision_context"):
                plan["revision_context"] = old["revision_context"]
            if old.get("final_continuation") and not fresh_final:
                plan["final_continuation"] = old["final_continuation"]
        else:
            plan["revision_context"] = revision_context(root, old, packet, bindings)
            if version_number == 3 and purpose == "report_delivery" and same_selection and allow_final_continuation:
                retained = prior_final_for_correction(root, old, packet, bindings, plan["producer_contexts"])
                if retained:
                    plan["final_continuation"] = retained
    if old != plan:
        if old:
            frozen(root, "reviews/plans/" + digest(old) + ".json", old)
        frozen(root, "reviews/plans/" + digest(plan) + ".json", plan)
        if scope == "full_report":
            progress.update(review_plan=plan, stage="review", status="in_progress")
        else:
            progress.setdefault("unit_review_plans", {})[scope] = plan
        if progress.get("review_contract") != 3:
            progress["review_contract"] = version_number
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
        from task_reading import reading_view
        requests.append({"slot_id": slot["slot_id"], "role": slot["role"],
                         "reading_ref": reading_view(root, request),
                         "assignment_ref": request_ref, "assignment_version": request["assignment_version"],
                         **({"phase": request["phase"]} if "phase" in request else {}),
                         **({"resume_host_task": request["resume_host_task"]} if "resume_host_task" in request else {}),
                         **({"assignment": request} if include_assignment else {})})
    evaluation = purpose == "evaluation"
    result = inspect(root, progress, artifact, plan=plan, require_report_ready=not evaluation)
    unit_ready = scope != "full_report" and not evaluation and result["ok"]
    if scope != "full_report":
        progress.setdefault("unit_reviews", {})[scope] = {
            "artifact_sha256": plan["artifact_sha256"], "input_version": version, "ok": unit_ready,
            "reviewers": [r["execution_id"] for r in selected.values()], "record_path": plan["input"]["path"]}
        save(root, "state/progress.json", progress)
    if scope == "full_report" and not evaluation and result["ok"]:
        summary = {"stage": "review" if version_number == 3 else "final", "scope": "global_final_delivery", "result": "pass",
                   "basis": selected["acceptance"]["result_data"]["basis"], "open_issues": [],
                   "artifact_sha256": plan["artifact_sha256"], "contract_version": version_number,
                   "review_evidence": {k: r["response"] for k, r in selected.items()}}
        rows = history(root)
        previous_summary = rows[-1] if rows else {}
        if version_number == 3:
            # Previously stored summaries can carry extra metadata. An unchanged
            # approval keeps its original review log and any receipt bound to it.
            previous_summary = {key: previous_summary.get(key) for key in summary}
        if previous_summary != summary:
            append(root, summary)
    evaluation_result = {}
    if evaluation:
        evaluation_result["evaluation_complete"] = result["ok"]
        if result["ok"]:
            from check_review_completion import content_review_issues
            audit_result = effective_audit(selected).get("result_data")
            acceptance_result = selected.get("acceptance", {}).get("result_data")
            if audit_result is not None:
                needs_revision = audit_result["report_verdict"] == "needs_revision"
            else:
                needs_revision = any(content_review_issues(row, {}) for row in selected.values())
            if acceptance_result is not None:
                needs_revision = needs_revision or acceptance_result["result"] == "fail"
            evaluation_result["evaluation_verdict"] = "needs_revision" if needs_revision else "pass"
    action = "host_agents" if pending else None
    if not action and not result["ok"]:
        action = "repair_review" if evaluation else "revise"
    delivery_ready = scope == "full_report" and not evaluation and result["ok"]
    return {"task_directory": str(root), "input_version": version, "scope": scope,
            "assignments": requests, "reviews_complete": all(s["slot_id"] in selected for s in slots if s["role"] == "reviewer"),
            "delivery_ready": delivery_ready,
            **({"submission_recorded": True} if host_result is not None else {}),
            "unit_ready": unit_ready, "completion_check": result,
            "action_required": action, "open_issues": result["findings"], **evaluation_result}


def checked_files(root, plan):
    from record_changes import input_digest
    files = {name for name in plan["bindings"] if not name.startswith("record:")}
    for name, expected in plan["bindings"].items():
        if input_digest(root, name) != expected:
            raise ValueError(f"Reviewed input changed: {name}.")
    files.add(plan["input"]["path"])
    if reference(root, plan["input"]["path"]) != plan["input"]:
        raise ValueError("Frozen review input changed.")
    if plan["contract_version"] == 3:
        blinded = plan["blind_input"]
        if reference(root, blinded["path"]) != blinded:
            raise ValueError("Frozen blind assessment input changed.")
        files.add(blinded["path"])
    retained = plan.get("revision_context", {})
    previous_refs = [retained["input"]] if retained else []
    previous_refs.extend(row[key] for row in retained.get("reviews", {}).values()
                         for key in ("input", "response", "execution"))
    for row in plan.get("final_continuation", {}).values():
        previous_refs.extend(row[key] for key in ("input", "response", "execution"))
        envelope = load(root, row["input"]["path"])
        if "shared_input" in envelope:
            previous_refs.append(envelope["shared_input"])
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
    selected = {}
    steps = []
    version = plan.get("contract_version")
    if version not in NATIVE_CONTRACTS or plan.get("artifact") != artifact:
        findings.append("The current artifact needs the independent agent review contract.")
    else:
        try:
            content = [s for s in plan["slots"] if s["role"] == "reviewer"]
            if plan.get("audit_required") and not any(s["slot_id"] == "audit" and s["role"] == "auditor" for s in plan["slots"]):
                raise ValueError("The declared independent audit assignment is missing.")
            if plan["scope"] == "full_report":
                if any(not any(s['slot_id'] == sid and s['role'] == role for s in plan['slots'])
                       for sid, role in [('audit', 'auditor'), ('acceptance', 'acceptance')]):
                    raise ValueError("Every full report requires separate independent audit and final acceptance assignments.")
                expected = REVIEW_GROUPS if version == 3 else {dimension: [dimension] for dimension in DIMENSIONS}
                if any(not any(s['slot_id'] == name and s.get('dimensions') == lenses for s in content)
                       for name, lenses in expected.items()):
                    raise ValueError("All seven perspectives must retain their assigned independent roles.")
                if len([s for s in content if s.get('dimensions') == ['domain']]) != len(plan.get('domains', [])):
                    raise ValueError("Declared domain reviews are incomplete.")
            checked_files(root, plan)
            selected = selected_results(root, plan)
            steps = assessment_steps(plan, selected)
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
            identities = {}
            producer_contexts = producers(root, progress)
            effective_audit_id = effective_audit(selected).get("attempt_id")
            for slot in steps:
                step = result_key(slot)
                row = selected.get(step)
                if row is None:
                    findings.append("Incomplete independent assignment: " + step)
                    continue
                request, request_ref = assignment(root, plan, slot, selected, persist=False)
                if row["input"] != request_ref:
                    raise ValueError("Dependent review/audit/acceptance inputs changed: " + slot["slot_id"])
                original = json.loads(response_text(root, row))
                if original != row["result_data"]:
                    raise ValueError("Stored judgment differs from the original response.")
                capture = json.loads(safe_path(root, row['execution']['path']).read_text(encoding="utf-8-sig"))
                if (capture.get('host_task') != row['execution_id'] or capture.get('status') != 'completed'
                        or capture.get('assignment_version') != request['assignment_version']):
                    raise ValueError("Execution identity/version differs from the retained execution capture.")
                expanded = validate_result(original, request)
                if expanded != row.get("expanded_decisions"):
                    raise ValueError("Expanded audit decisions differ from the original response.")
                identity = row["execution_id"]
                if slot.get("phase") == "correction_review" and identity != request["resume_host_task"]:
                    raise ValueError("The final correction review did not resume its original independent context.")
                if identity in producer_contexts:
                    raise ValueError("An author/producer performed independent review.")
                if identities.setdefault(identity, slot["slot_id"]) != slot["slot_id"]:
                    raise ValueError("Review groups, audit, blind verification and acceptance need distinct agent contexts.")
                if slot["role"] == "auditor" and original["result"] != "valid":
                    findings.append("Independent audit did not establish valid review work.")
                elif require_report_ready:
                    if slot["role"] == "reviewer" and plan["scope"] != "full_report" and not plan.get("audit_required"):
                        from check_review_completion import content_review_issues
                        findings.extend(content_review_issues(original, {}))
                    elif (slot["role"] == "auditor" and row["attempt_id"] == effective_audit_id
                          and original["report_verdict"] != "pass"):
                        findings.extend(original["open_issues"] or ["Independent audit has unresolved findings."])
                    elif slot["role"] == "acceptance" and slot.get("phase") != "blind" and original["result"] != "pass":
                        findings.extend(original["open_issues"] or ["Independent final acceptance did not pass."])
        except (ValueError, OSError, KeyError, TypeError, StopIteration) as exc:
            findings.append(str(exc))
    role_steps = {}
    for slot in steps or plan.get("slots", []):
        role_steps.setdefault(slot["slot_id"], []).append(result_key(slot))
    result = {"ok": not findings, "flags": ["incomplete_independent_review"] if findings else [],
            "findings": findings, "required_slots": len(role_steps),
            "completed_slots": sum(all(step in selected for step in slots) for slots in role_steps.values()),
            **({"required_steps": len(steps), "completed_steps": len(selected)} if version == 3 else {}),
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
        raise ValueError("Author self-review cannot satisfy independent assignments. Use native agents.")
    result = review(workflow, root, progress, evidence_paths, artifact, purpose, revision,
                    False, host_result, scope, perspectives, domains, audit, allow_final_continuation=False)
    while result["assignments"]:
        if any(job.get("phase") == "correction_review" for job in result["assignments"]):
            result = review(workflow, root, load(root, "state/progress.json"), evidence_paths, artifact, purpose,
                            False, False, None, scope, perspectives, domains, audit, fresh_final=True)
        for job in result["assignments"]:
            request = load_assignment(root, job["assignment_ref"]["path"])
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
