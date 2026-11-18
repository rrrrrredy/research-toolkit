"""Historical review-execution fixtures used by the repository checks."""
from __future__ import annotations

import json
from pathlib import Path
import re
import time
import uuid

import research_workflow as workflow
from check_delivery import sha256_file
from check_review_completion import matches_review_slot
from research_guidance import BRIEF_FIELDS
from research_workflow import (
    DIMENSIONS, REVIEW_INSTRUCTIONS, append_row, checked_review, completion,
    content_review_summary, finish_recorded, rows_for, task_operation,
)
from review_runner import (
    BACKEND_HELP, ReviewFailure, assignment_config, backend_configured, backend_kind,
    load_review_config, run_reviewer, validate_review_config,
)
from run_observation import now, timed_capture
from task_context import require_current_artifact, task_inputs
from task_storage import digest, load, nonempty, safe_path, save, save_text, task_root


AUDIT_INSTRUCTIONS = """Independently audit this review against the entire supplied report,
task and evidence. You are a fresh context, separate from the author and reviewer.
Assess substantive coverage, correct input/version, locatable evidence and justified reasoning;
JSON shape and a generic PASS do not establish validity. Isolated mistakes are adjudicated,
not grounds for discarding an otherwise valid review. Examine every critical/major finding
and consequential disagreement, and the specified sample of passed content and review decisions.
Do not edit the report. Return one JSON object:
result (valid or invalid), basis (specific reasoning), dispositions keyed by every finding_id
(each has decision confirmed_defect/no_change/unresolved/resolved, reason, evidence),
sample_checks keyed by every assigned sample ID (each has result clear/defect and evidence;
a defect also needs defect_type report/review_validity and follow_up with decision and reason;
follow_up.decision must be confirmed_defect, no_change, unresolved, or resolved),
global_review (result pass/fail, basis, open_issues list).
The top-level result judges REVIEW VALIDITY. global_review judges REPORT READINESS, not
review validity: a valid review can accompany a failing report. Use global_review.result=fail
when required report corrections remain; pass requires an empty open_issues list and no
unresolved required report defects. List the actual remaining report issues without rewriting them.
A report defect still present is confirmed_defect, not resolved. An evaluation may retain it.
An invalid review must explain actual assignment failure, never just a negative verdict.
Do not claim a defect was fixed or a check performed without evidence. No Markdown fences."""
SAMPLING_METHOD = ("Inspect each reviewer slot, the first and last substantive report paragraphs "
                   "and one hash-selected paragraph; independently adjudicate all consequential findings. "
                   "Inspect passed content and no-change decisions. Expand a defective check before "
                   "recording an evidenced follow-up; unresolved review validity remains incomplete.")


def ref(root, name):
    return {"path": name, "sha256": sha256_file(safe_path(root, name))}


def content_review_instructions() -> str:
    reference = (workflow.TOOLKIT / "references/subagents-and-review-loop.md").read_text(encoding="utf-8")
    _, heading, remainder = reference.partition("## Assign Work by Perspective\n")
    methods = remainder.split("\n## ", 1)[0].strip()
    if not heading or not methods:
        raise ValueError("The shared content-review methods are missing from the role reference.")
    return REVIEW_INSTRUCTIONS + "\n\nApply these methods within the assigned review:\n" + methods


def checked_audit(value, review, samples):
    if not isinstance(value, dict) or value.get("result") not in {"valid", "invalid"} or not nonempty(value.get("basis")):
        raise ValueError("Audit needs an evidenced validity decision.")
    if value["result"] == "invalid":
        return value
    decisions = value.get("dispositions")
    ids = {f["finding_id"] for f in review["findings"]}
    if not isinstance(decisions, dict) or set(decisions) != ids:
        raise ValueError("Every finding needs exactly one audit disposition.")
    for item in decisions.values():
        if not isinstance(item, dict) or item.get("decision") not in {"confirmed_defect", "no_change", "unresolved", "resolved"}:
            raise ValueError("Invalid disposition decision.")
        if not all(nonempty(item.get(k)) for k in ("reason", "evidence")):
            raise ValueError("Disposition needs evidence and reasoning.")
    checks = value.get("sample_checks")
    if not isinstance(checks, dict) or set(checks) != set(samples):
        raise ValueError("Audit omitted required samples.")
    for item in checks.values():
        if not isinstance(item, dict) or item.get("result") not in {"clear", "defect"} or not nonempty(item.get("evidence")):
            raise ValueError("Sample needs a concrete check result.")
        if item["result"] == "defect":
            follow = item.get("follow_up")
            if item.get("defect_type") not in {"report", "review_validity"} or not isinstance(follow, dict):
                raise ValueError("Sampling defect needs its type and actual follow-up.")
            if follow.get("decision") not in {"confirmed_defect", "no_change", "unresolved", "resolved"} or not nonempty(follow.get("reason")):
                raise ValueError("Sampling follow-up is incomplete.")
    global_review = value.get("global_review")
    if not isinstance(global_review, dict) or global_review.get("result") not in {"pass", "fail"}:
        raise ValueError("Audit needs a whole-report judgment.")
    if not nonempty(global_review.get("basis")) or not isinstance(global_review.get("open_issues"), list):
        raise ValueError("Whole-report judgment needs a basis and issue list.")
    if global_review["result"] == "pass" and global_review["open_issues"]:
        raise ValueError("A passing whole-report review cannot have open issues.")
    return value


def invoke(root, prefix, config, request, used_ids, runner):
    save(root, prefix+"/request.json", request)
    started_at, started = now(), time.monotonic()
    try:
        result = runner(config, request, safe_path(root, prefix))
        save(root, prefix+"/execution.json", timed_capture(result["capture"], started_at, started))
        save_text(root, prefix+"/response.txt", result["content"])
        identity = result["execution_id"]
        if not nonempty(identity) or (identity in used_ids and config.get("backend") != "self"):
            raise ValueError("Reviewer execution ID is missing or reused.")
        used_ids.add(identity)
        save(root, prefix+"/identity.json", {"execution_id": identity})
        value = json.loads(result["content"])
        return value, identity
    except ReviewFailure as exc:
        save(root, prefix+"/execution.json", timed_capture(exc.capture, started_at, started))
        raise


def review_result_fields(validity, outcome, purpose):
    """Separate completed review work from permission to deliver the report."""
    return {"reviews_complete": validity["ok"], "review_check": validity,
            "delivery_ready": purpose == "report_delivery" and outcome["ok"],
            "evaluation_complete": purpose == "evaluation" and outcome["ok"],
            "completion_check": outcome, "open_issues": outcome["findings"]}


def record_plan_change(root, previous, current):
    references = {}
    for key, plan in (("previous_plan", previous), ("current_plan", current)):
        name = "reviews/plans/" + digest(plan) + ".json"
        if not safe_path(root, name).exists():
            save(root, name, plan)
        if load(root, name) != plan:
            raise ValueError("Retained review plan was modified; preserve and inspect the original records.")
        references[key] = ref(root, name)
    change = {"record_type": "review_plan_change", "revision_authorized": True, **references}
    changes = [r for r in rows_for(root) if r.get("record_type") == "review_plan_change"]
    # Resume a crash between recording the change and publishing the current plan.
    if not changes or changes[-1] != change:
        append_row(root, change)


@task_operation
def legacy_review(workspace: Path, task: str, evidence_paths: list[str], artifact="final.md",
           purpose="report_delivery", revision=False, reviewer=None, self_review=None, include_assignment=True, *, config=None, runner=run_reviewer) -> dict:
    """Generate historical records for compatibility checks."""
    if type(include_assignment) is not bool:
        raise ValueError("include_assignment must be true or false.")
    root = task_root(workspace, task)
    progress = load(root, "state/progress.json")
    require_current_artifact(progress, artifact)
    if any(not nonempty(progress.get("brief", {}).get(k)) for k in BRIEF_FIELDS):
        raise ValueError("Clarify critical research requirements before reviewing.")
    if purpose not in {"evaluation", "report_delivery"}:
        raise ValueError("Unknown review purpose.")
    if not isinstance(evidence_paths, list) or not evidence_paths or not all(nonempty(x) for x in evidence_paths):
        raise ValueError("Provide the task-relative files containing the full required evidence.")
    required_sources, originals = workflow.required_source_inputs(root)
    artifact_path = safe_path(root, artifact)
    report = artifact_path.read_text(encoding="utf-8")
    if not report.strip():
        raise ValueError("The report is empty.")
    old_plan = progress.get("review_plan")
    if reviewer is None:
        reviewer = (old_plan.get("reviewer", "independent") if old_plan else
                    "independent" if config is not None or backend_configured() or purpose == "evaluation" else "self")
    if reviewer not in {"self", "external", "independent"}:
        raise ValueError("Reviewer must be self, external or independent.")
    if self_review is not None and reviewer != "self":
        raise ValueError("An agent tool-supplied response is accepted only for reviewer=self.")
    if reviewer == "self":
        if purpose == "evaluation":
            raise ValueError("Evaluations require a separate reviewer context; self is for report delivery.")
        config = {"reviewers": [{"id": "self", "model": "author-context", "backend": "self", "format": "self"}]}
    config = (load_review_config(require_audit=bool(
        old_plan and old_plan.get("audit_required", True)))
        if config is None else validate_review_config(config))
    if reviewer != "self" and any(backend_kind(r) == "self" for r in config["reviewers"]):
        raise ValueError("The declared external/independent reviewer needs a backend. " + BACKEND_HELP)
    audit_required = "auditor" in config
    if old_plan and old_plan.get("purpose") == "evaluation" and old_plan.get("audit_required", True) and not audit_required:
        raise ValueError("This saved evaluation requires its declared auditor configuration.")
    instruction_snapshot = old_plan.get("instruction_snapshot") if old_plan and not revision else None
    if instruction_snapshot is not None:
        if (not isinstance(instruction_snapshot, dict) or set(instruction_snapshot) != {"reviewer", "auditor"}
                or not nonempty(instruction_snapshot.get("reviewer"))
                or (instruction_snapshot["auditor"] is not None and not nonempty(instruction_snapshot["auditor"]))):
            raise ValueError("Saved review instruction snapshot is malformed; preserve and inspect the task records.")
        review_instructions = instruction_snapshot["reviewer"]
        audit_instructions = instruction_snapshot["auditor"]
    else:
        review_instructions = content_review_instructions()
        if reviewer == "self":
            review_instructions = ("Explicitly switch from author to critical reviewer in this same context. "
                "This is a degraded self-review, not an independent opinion. Examine the frozen input below. "
                "Return the JSON result with the supplied input_version, then submit it as self_review.\n"
                + review_instructions)
        if not audit_required:
            review_instructions += ("\nFor report delivery, pass only when no required corrections remain. "
                                    "Mark nonessential suggestions optional; any critical, major or minor defect "
                                    "requires needs_revision. A negative verdict is a completed review.")
        audit_instructions = AUDIT_INSTRUCTIONS if audit_required else None
        # Do not invent a historical snapshot for legacy executions. An explicit
        # ordinary revision creates a fresh assignment with the current methods.
        if not old_plan or revision:
            instruction_snapshot = {"reviewer": review_instructions, "auditor": audit_instructions}
    source_names = sorted(set([*evidence_paths, *required_sources, "data/source_registry.csv", "data/claims_registry.csv"]))
    sources = {name: safe_path(root, name).read_text(encoding="utf-8") for name in source_names}
    if any(not text.strip() for text in sources.values()):
        raise ValueError("Required source input is empty.")
    shared_inputs = task_inputs(root)
    packet = {"task": shared_inputs["task"],
              "report_path": artifact, "report": report, "sources": sources, "dimensions": DIMENSIONS,
              "purpose": purpose}
    if audit_required:
        packet["sampling_method"] = SAMPLING_METHOD
    if originals:
        packet["source_files"] = originals
    requirements = shared_inputs["requirements"]
    if requirements:
        packet["requirements"] = requirements
    if len(json.dumps(packet, ensure_ascii=False).encode("utf-8")) > 16 * 1024 * 1024:
        raise ValueError("Input exceeds the 16 MiB local limit; explicitly agree a bounded assignment rather than truncating it.")
    version = digest(packet)
    artifact_hash = sha256_file(artifact_path)
    if self_review is not None:
        if not isinstance(self_review, dict) or self_review.get("input_version") != version:
            raise ValueError("Self-review must quote the current frozen input_version; request its prompt first.")
        checked_review(self_review, DIMENSIONS)
    old_plan = progress.get("review_plan")
    runner_signature = digest({"reviewers": [assignment_config(r) for r in config["reviewers"]],
                               "auditor": assignment_config(config["auditor"]) if audit_required else None,
                               "review_instructions": review_instructions,
                               "audit_instructions": audit_instructions if audit_required else None})
    same_runner = bool(old_plan and old_plan.get("runner_signature") in {runner_signature, digest(config)})
    assignment_changed = bool(old_plan and (old_plan.get("input_version") != version or not same_runner))
    if assignment_changed:
        if old_plan.get("purpose") == "evaluation" or purpose == "evaluation":
            raise ValueError("Evaluation input is frozen. Preserve it and use a separate task for another study.")
        if not revision:
            raise ValueError("The reviewed assignment changed. Pass revision=true to review the corrected report or changed reviewer assignment. "
                             "This is the normal report revision loop; an already authorized correction does not need another user confirmation. "
                             "Reconcile any changed research scope in the task records first.")
    prefix = f"reviews/{version}"
    if not safe_path(root, prefix+"/input.json").exists():
        save(root, prefix+"/input.json", packet)
    if load(root, prefix+"/input.json") != packet:
        raise ValueError("Frozen review input was modified; preserve and inspect the original records.")
    input_ref = ref(root, prefix+"/input.json")
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", report) if p.strip()]
    indices = sorted({0, len(paragraphs)-1, int(version[:8], 16) % len(paragraphs)})
    report_samples = {f"paragraph:{i+1}": paragraphs[i] for i in indices}
    slots = [{"slot_id": r["id"], "reviewer_id": progress["author_id"] if reviewer == "self" else f"reviewer:{r['id']}", "model": r["model"],
              "scope": "full_report", "dimensions": DIMENSIONS, "input": input_ref,
              "reviewer_signature": digest({"config": assignment_config(r), "instructions": review_instructions})}
             for r in config["reviewers"]]
    auditor_signature = (digest({"config": assignment_config(config["auditor"]), "instructions": audit_instructions})
                         if audit_required else None)
    # Preserve an unchanged legacy assignment without inventing bindings for old executions.
    if same_runner:
        old_slots = {s["slot_id"]: s for s in old_plan["slots"]}
        for slot in slots:
            previous = old_slots.get(slot["slot_id"], {})
            if "reviewer_signature" not in previous and previous.get("input") == input_ref:
                slot.pop("reviewer_signature", None)
        if "auditor_signature" not in old_plan:
            auditor_signature = None
    population = [*[f"paragraph:{i+1}" for i in range(len(paragraphs))],
                  *[f"review:{s['slot_id']}" for s in slots]]
    selection = [*report_samples, *[f"review:{s['slot_id']}" for s in slots]]
    plan = {"purpose": purpose, "author_id": progress["author_id"], "artifact_sha256": artifact_hash,
            "input_version": version, "runner_signature": runner_signature, "slots": slots,
            "sampling": {"method": SAMPLING_METHOD, "population": population,
                         "selected": selection, "mandatory": [f"review:{s['slot_id']}" for s in slots]}}
    if instruction_snapshot is not None:
        plan["instruction_snapshot"] = instruction_snapshot
    if reviewer != "independent":
        plan.update(reviewer=reviewer, review_strength="degraded" if reviewer == "self" else "external")
    if not audit_required:
        plan.pop("sampling")
        plan["audit_required"] = False
        if not old_plan or (revision and assignment_changed):
            plan["disposition_schema_version"] = 2
        elif "disposition_schema_version" in old_plan:
            plan["disposition_schema_version"] = old_plan["disposition_schema_version"]
    if auditor_signature is not None:
        plan["auditor_signature"] = auditor_signature
    if old_plan == plan:
        validity = completion(root, progress, artifact, require_report_ready=False)
        if validity["ok"]:
            outcome = completion(root, progress, artifact)
            return {**review_result_fields(validity, outcome, purpose),
                    "recovery": [], "reused": True, "task_directory": str(root),
                    "reviewer": reviewer, "review_strength": plan.get("review_strength", "independent")}
    if assignment_changed:
        record_plan_change(root, old_plan, plan)
    progress.update(review_plan=plan, stage="review", status="in_progress",
                    next_action="Complete the declared reviews and any requested audits.")
    save(root, "state/progress.json", progress)
    if reviewer == "self" and self_review is None:
        response = {"reviews_complete": False, "action_required": "self_review", "reviewer": "self",
                "review_strength": "degraded", "independent_review": False, "input_version": version,
                "prompt": review_instructions, "assignment_ref": input_ref, "task_directory": str(root),
                "log": ["SELF REVIEW: same author context; no external backend called; review strength is degraded."]}
        if include_assignment:
            response["assignment"] = packet
        else:
            response["prompt"] += ("\nThe complete frozen assignment is in assignment_ref.path under task_directory. "
                "Read it locally; reuse already-read unchanged evidence and inspect changed passages and sources. "
                "Review the current complete report and required evidence before submitting self_review. "
                "Returning a file reference does not change the assignment or its input_version.")
        return response
    if reviewer == "self":
        def runner(config, request, cwd):
            return {"execution_id": progress["author_id"], "content": json.dumps(self_review, ensure_ascii=False),
                    "capture": {"reviewer": "self", "review_strength": "degraded", "context": "author",
                                "external_execution": False}}
    used_ids = {r.get("execution_id") for r in rows_for(root) if nonempty(r.get("execution_id"))}
    # Include audit executions as well, even after a failed/partial audit.
    for identity_path in safe_path(root, "reviews").rglob("identity.json"):
        identity_path.resolve().relative_to(root)
        used_ids.add(json.loads(identity_path.read_text(encoding="utf-8"))["execution_id"])
    problems = []
    selected = {}
    for slot, reviewer_config in zip(slots, config["reviewers"]):
        sid = slot["slot_id"]
        for _ in range(2):
            history = rows_for(root)
            audits = {}
            for row in history:
                if row.get("record_type") == "review_audit" and row.get("auditor_signature") == auditor_signature:
                    if audits.get(row["attempt_id"], {}).get("result") != "valid":
                        audits[row["attempt_id"]] = row
            candidates = [r for r in history if r.get("record_type") == "model_review"
                          and r.get("slot_id") == sid and r.get("status") == "completed"
                          and matches_review_slot(r, slot) and r.get("artifact_sha256") == artifact_hash]
            valid = next((r for r in candidates if not audit_required
                          or audits.get(r["attempt_id"], {}).get("result") == "valid"), None)
            if valid:
                selected[sid] = (valid, audits.get(valid["attempt_id"]))
                break
            pending = next((r for r in candidates if r["attempt_id"] not in audits), None)
            if pending is None:
                aid = uuid.uuid4().hex
                attempt_prefix = prefix+"/attempts/"+aid
                base = {"record_type": "model_review", "attempt_id": aid,
                        **{k: slot[k] for k in ("slot_id", "reviewer_id", "model", "scope", "input", "reviewer_signature") if k in slot},
                        "artifact_sha256": artifact_hash, "reviewer": reviewer,
                        "review_strength": "degraded" if reviewer == "self" else reviewer}
                if "disposition_schema_version" in plan:
                    base["disposition_schema_version"] = plan["disposition_schema_version"]
                try:
                    value, execution_id = invoke(root, attempt_prefix, reviewer_config,
                        {"role": "reviewer", "instructions": review_instructions, "assignment": packet},
                        used_ids, runner)
                    value = checked_review(value, DIMENSIONS)
                    pending = {**base, "status": "completed", "execution_id": execution_id,
                               "execution": ref(root, attempt_prefix+"/execution.json"),
                               "response": ref(root, attempt_prefix+"/response.txt"),
                               **{k: value[k] for k in ("report_verdict", "coverage", "findings")}}
                    append_row(root, pending)
                except (ReviewFailure, ValueError, TypeError, KeyError) as exc:
                    append_row(root, {**base, "status": "incomplete",
                                      "failure": str(exc), "recovery": "Restore access or complete this same assignment.",
                                      "execution": ref(root, attempt_prefix+"/execution.json")
                                      if safe_path(root, attempt_prefix+"/execution.json").exists() else None})
                    problems.append(f"{sid}: {exc}")
                    if isinstance(exc, ReviewFailure) and exc.capture.get("status") in {"dependency_missing", "launch_failure", "cancellation_unconfirmed"}:
                        break
                    continue
            if not audit_required:
                selected[sid] = (pending, None)
                break
            aid = pending["attempt_id"]
            audit_prefix = prefix+"/audits/"+uuid.uuid4().hex
            samples = {**report_samples, f"review:{sid}": "Check review validity, passed coverage and no-change decisions."}
            try:
                audit_value, audit_id = invoke(root, audit_prefix, config["auditor"],
                    {"role": "auditor", "instructions": audit_instructions, "assignment": packet,
                     "original_review": safe_path(root, pending["response"]["path"]).read_text(encoding="utf-8"),
                     "finding_records": pending["findings"], "samples": samples},
                    used_ids, runner)
                audit_value = checked_audit(audit_value, pending, samples)
                audit = {"record_type": "review_audit", "attempt_id": aid, "auditor_id": audit_id,
                         "execution_id": audit_id, "result": audit_value["result"],
                         "basis": audit_value["basis"], "response_sha256": pending["response"]["sha256"],
                         "evidence": ref(root, audit_prefix+"/response.txt"),
                         "execution": ref(root, audit_prefix+"/execution.json"),
                         "dispositions": audit_value.get("dispositions", {}),
                         "sample_checks": audit_value.get("sample_checks", {}),
                         "global_review": audit_value.get("global_review", {})}
                if auditor_signature is not None:
                    audit["auditor_signature"] = auditor_signature
                append_row(root, audit)
                if audit["result"] == "valid":
                    selected[sid] = (pending, audit)
                    break
            except (ReviewFailure, ValueError, TypeError, KeyError) as exc:
                problems.append(f"{sid} audit: {exc}")
                save(root, audit_prefix+"/failure.json", {"error": str(exc), "attempt_id": aid,
                    "recovery": "Complete the missing audit; preserve the original review."})
                # Do not relaunch a completed reviewer merely because its audit failed.
                break
    if sha256_file(artifact_path) != artifact_hash:
        return {"reviews_complete": False, "error": "Report changed during review; retained results bind the captured version."}
    if len(selected) == len(slots) and audit_required:
        checks = {}
        evidence = {}
        contexts = []
        globals_ = []
        for sid, (_, audit) in selected.items():
            contexts.append(audit["auditor_id"])
            globals_.append(audit["global_review"])
            evidence[sid] = audit["evidence"]
            for item, check in audit["sample_checks"].items():
                if item not in checks or check["result"] == "defect":
                    checks[item] = json.loads(json.dumps(check))
                    if check["result"] == "defect":
                        checks[item]["follow_up"]["evidence"] = audit["evidence"]
        # New assignment summaries must not overwrite evidence referenced by prior audits.
        summary_path = prefix+"/sample-audits-"+digest(evidence)+".json"
        save(root, summary_path, {"method": SAMPLING_METHOD, "audits": evidence, "auditor_contexts": contexts})
        append_row(root, {"record_type": "sampling_audit", "artifact_sha256": artifact_hash,
                          "selected": selection, "auditor_id": "panel:"+",".join(contexts),
                          "auditor_contexts": contexts, "evidence": ref(root, summary_path), "checks": checks})
        global_pass = all(g.get("result") == "pass" and not g.get("open_issues") for g in globals_)
        append_row(root, {"scope": "global_final_delivery", "artifact_sha256": artifact_hash,
                          "result": "pass" if global_pass else "fail",
                          "open_issues": [issue for g in globals_ for issue in g.get("open_issues", [])],
                          "basis": [g.get("basis") for g in globals_], "review_evidence": evidence,
                          "auditor_contexts": contexts})
    if len(selected) == len(slots) and not audit_required:
        append_row(root, content_review_summary({sid: r for sid, (r, _) in selected.items()},
                                               rows_for(root), artifact_hash))
    outcome = completion(root, progress, artifact)
    progress["open_issues"] = outcome["findings"]
    progress["next_action"] = ("Review work is complete; preserve evaluation outcomes." if purpose == "evaluation" and outcome["ok"]
                               else "Run delivery verification." if outcome["ok"]
                               else "Resolve the current review findings: " + "; ".join(outcome["findings"]))
    save(root, "state/progress.json", progress)
    validity = completion(root, progress, artifact, require_report_ready=False)
    return {"reviewer": reviewer, "review_strength": plan.get("review_strength", "independent"),
            **review_result_fields(validity, outcome, purpose), "recovery": problems, "task_directory": str(root)}


@task_operation
def legacy_finish(workspace: Path, task: str, message: str, artifact="final.md") -> dict:
    """Complete a historical fixture."""
    return finish_recorded(workspace, task, message, artifact)
