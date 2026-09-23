#!/usr/bin/env python3
"""Check declared model-review completion without certifying model judgments."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Callable

REVIEW_RECORD_TYPES = {"model_review", "review_audit", "sampling_audit", "review_plan_change"}
PURPOSES = {"evaluation", "report_delivery"}
DECISIONS = {"confirmed_defect", "no_change", "unresolved", "resolved"}
SEVERITIES = {"critical", "major", "minor", "optional"}


def text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def one_of(value: Any, choices: set[str]) -> bool:
    return isinstance(value, str) and value in choices


def distinct_strings(value: Any, *, nonempty: bool = True) -> bool:
    return (isinstance(value, list) and (bool(value) or not nonempty)
            and all(text(item) for item in value) and len(set(value)) == len(value))


def matches_review_slot(row: dict, slot: dict) -> bool:
    """Use the same assignment identity in execution and offline acceptance."""
    return all(row.get(key) == slot.get(key) for key in
               ("slot_id", "reviewer_id", "model", "scope", "input", "reviewer_signature"))


def content_review_rows(rows: list[dict]) -> list[dict]:
    """Keep attempt failures separate from report-delivery findings."""
    return [row for row in rows if not one_of(row.get("record_type"), REVIEW_RECORD_TYPES)]


def inspect_review_completion(
    root: Path, progress: dict, artifact: str, rows: list[dict], *,
    hash_file: Callable, resolve_path: Callable, require_report_ready: bool = True,
) -> dict:
    flags: list[str] = []
    findings: list[str] = []
    selected: dict[str, str] = {}
    error_count = 0

    def add(flag: str, message: str) -> None:
        nonlocal error_count
        error_count += 1
        if flag not in flags:
            flags.append(flag)
            findings.append(message)
        else:
            findings[flags.index(flag)] += "\n" + message

    def reference(value: Any, label: str) -> Path | None:
        if not isinstance(value, dict) or not text(value.get("path")) or not text(value.get("sha256")):
            add("missing_review_evidence", f"{label}: expected a path and sha256.")
            return None
        path = resolve_path(root, value["path"])
        if path is None or not path.is_file():
            add("missing_review_evidence", f"{label}: missing file or path outside the task.")
            return None
        try:
            if not path.read_text(encoding="utf-8").strip():
                raise ValueError("empty evidence")
            if value["sha256"].lower() != hash_file(path):
                add("stale_review_evidence", f"{label}: evidence hash differs.")
                return None
        except (OSError, UnicodeError, ValueError):
            add("invalid_review_evidence", f"{label}: evidence must be nonempty UTF-8.")
            return None
        return path

    def result(planned: int = 0) -> dict:
        return {
            "ok": not flags, "flags": flags, "findings": findings,
            "required_slots": planned, "completed_slots": len(selected),
            "selected_attempts": selected,
            "record_consistency_checked": True,
            "execution_authenticity_verified": False,
            "semantic_verification": False,
            "report_quality_certified": False,
        }

    plan = progress.get("review_plan")
    if not isinstance(plan, dict) or not one_of(plan.get("purpose"), PURPOSES):
        add("missing_review_plan", "Declare review_plan with purpose evaluation or report_delivery.")
        return result()
    author = plan.get("author_id")
    if not text(author):
        add("invalid_review_plan", "review_plan.author_id must identify the author context.")
        author = ""
    artifact_path = resolve_path(root, artifact)
    try:
        artifact_hash = hash_file(artifact_path) if artifact_path and artifact_path.is_file() else None
    except (OSError, UnicodeError):
        artifact_hash = None
    if not artifact_hash or plan.get("artifact_sha256") != artifact_hash:
        add("stale_review_plan", "The review plan must bind the actual artifact.")
    slots = plan.get("slots")
    if not isinstance(slots, list) or not slots or not all(isinstance(s, dict) for s in slots):
        add("invalid_review_plan", "Declare at least one required review slot.")
        return result()
    slot_ids = [s.get("slot_id") for s in slots]
    if not distinct_strings(slot_ids):
        add("invalid_review_plan", "Required slot ids must be distinct nonempty strings.")
        return result(len(slots))

    report_delivery = plan["purpose"] == "report_delivery" and require_report_ready
    historical_plans = []
    previous_current = None
    changes = [r for r in rows if r.get("record_type") == "review_plan_change"]
    for change in changes:
        versions = []
        if change.get("revision_authorized") is not True or plan["purpose"] != "report_delivery":
            add("invalid_review_plan_change", "Only an explicitly authorized report-delivery revision can retire a slot.")
        for key in ("previous_plan", "current_plan"):
            path = reference(change.get(key), f"Review plan change {key}")
            try:
                version = json.loads(path.read_text(encoding="utf-8")) if path else None
            except (OSError, UnicodeError, ValueError):
                version = None
            version_slots = version.get("slots") if isinstance(version, dict) else None
            if (not isinstance(version, dict) or version.get("purpose") != "report_delivery"
                    or version.get("author_id") != author or not text(version.get("artifact_sha256"))
                    or not isinstance(version_slots, list) or not version_slots
                    or not all(isinstance(s, dict) for s in version_slots)
                    or not distinct_strings([s.get("slot_id") for s in version_slots])):
                add("invalid_review_plan_change", "Plan changes must retain both complete, hash-bound report-delivery plans.")
                versions.append(None)
                continue
            for old_slot in version_slots:
                if (not all(text(old_slot.get(k)) for k in ("reviewer_id", "model", "scope"))
                        or not distinct_strings(old_slot.get("dimensions"))):
                    add("invalid_review_plan_change", "A retained plan has an invalid review slot.")
                reference(old_slot.get("input"), "Retained plan frozen input")
            versions.append(version)
        old, new = versions
        if old is None or new is None:
            continue
        if previous_current is not None and old != previous_current:
            add("invalid_review_plan_change", "Retained plan changes do not form a continuous history.")
        historical_plans.append(old)
        previous_current = new
    if changes and previous_current != plan:
        add("invalid_review_plan_change", "The last retained plan change does not bind the current review plan.")

    attempts: dict[str, dict] = {}
    audits: dict[str, dict] = {}
    for row in rows:
        kind = row.get("record_type")
        if not one_of(kind, {"model_review", "review_audit"}):
            continue
        attempt_id = row.get("attempt_id")
        if not text(attempt_id):
            add("invalid_review_record", "Review attempts and audits need attempt_id.")
            continue
        if kind == "model_review":
            if attempt_id in attempts:
                add("duplicate_review_attempt", f"Duplicate attempt id {attempt_id}.")
            attempts[attempt_id] = row
            historical = any(row.get("artifact_sha256") == old["artifact_sha256"]
                             and any(matches_review_slot(row, slot) for slot in old["slots"])
                             for old in historical_plans)
            if ((row.get("slot_id") not in slot_ids and not historical)
                    or not one_of(row.get("status"), {"completed", "failed", "incomplete"})):
                add("invalid_review_record", f"{attempt_id}: unknown slot or attempt status.")
        else:
            if not one_of(row.get("result"), {"valid", "invalid"}):
                add("invalid_review_audit", f"{attempt_id}: audit result must be valid or invalid.")
            if row.get("auditor_signature") == plan.get("auditor_signature"):
                # Keep the first valid audit for this auditor assignment.
                if audits.get(attempt_id, {}).get("result") != "valid":
                    audits[attempt_id] = row
    for row in rows:
        if row.get("record_type") != "review_audit":
            continue
        attempt_id = row.get("attempt_id")
        if not text(attempt_id) or attempt_id not in attempts:
            add("invalid_review_audit", "Audit refers to an unknown attempt.")
            continue
        # Invalidation is a consequential decision too; it cannot be an empty
        # label that hides an earlier negative result before selecting a retry.
        if not text(row.get("basis")) or not text(row.get("auditor_id")):
            add("invalid_review_audit", f"{attempt_id}: every validity decision needs identity and a basis.")
        reference(row.get("evidence"), f"{attempt_id} validity decision evidence")
        original = attempts[attempt_id]
        auditor = row.get("auditor_id")
        if auditor == original.get("reviewer_id"):
            add("self_validated_review", f"{attempt_id}: the reviewer cannot validate or invalidate their own response.")
        if row.get("result") == "invalid" and auditor == author:
            add("missing_independent_adjudication", f"{attempt_id}: invalidating a review requires a context separate from the author.")
        original_response = original.get("response")
        if isinstance(original_response, dict) and row.get("response_sha256") != original_response.get("sha256"):
            add("stale_review_audit", f"{attempt_id}: validity decision binds a different original response.")

    response_paths: set[Path] = set()
    execution_ids: set[str] = set()
    for slot in slots:
        sid = slot["slot_id"]
        before = error_count
        if (not all(text(slot.get(key)) for key in ("reviewer_id", "model", "scope"))
                or not distinct_strings(slot.get("dimensions"))):
            add("invalid_review_plan", f"{sid}: identify reviewer, model, scope and required dimensions.")
            continue
        if slot["reviewer_id"] == author:
            add("author_counted_as_reviewer", f"{sid}: the author cannot fill an independent review slot.")
        reference(slot.get("input"), f"{sid} frozen input")
        candidates = [r for r in attempts.values()
                      if r.get("slot_id") == sid and r.get("status") == "completed"
                      and audits.get(r["attempt_id"], {}).get("result") == "valid"]
        current = [r for r in candidates if r.get("artifact_sha256") == artifact_hash
                   and matches_review_slot(r, slot)]
        if not current:
            if any(r.get("artifact_sha256") == artifact_hash and r.get("input") == slot.get("input") for r in candidates):
                add("review_slot_mismatch", f"{sid}: retained reviews do not match the current reviewer assignment.")
            add("missing_valid_review", f"{sid}: no completed, valid attempt for the current artifact and input.")
            if candidates:
                add("stale_model_review", f"{sid}: retained valid reviews cover a different assignment version.")
            continue
        # Preserve first-valid selection within an assignment version, including negative results.
        review = current[0]
        aid = review["attempt_id"]
        audit = audits[aid]
        for field in ("reviewer_id", "model", "scope", "input"):
            if review.get(field) != slot.get(field):
                add("review_slot_mismatch", f"{aid}: {field} differs from the declared slot.")
        if review.get("artifact_sha256") != artifact_hash:
            add("stale_model_review", f"{aid}: review does not bind the current artifact.")
        response = reference(review.get("response"), f"{aid} original response")
        execution = reference(review.get("execution"), f"{aid} execution capture")
        execution_id = review.get("execution_id")
        if not text(execution_id):
            add("missing_review_execution", f"{aid}: execution_id is missing.")
        elif execution_id in execution_ids:
            add("reused_review_execution", f"{aid}: one execution is counted for multiple slots.")
        else:
            execution_ids.add(execution_id)
        if response:
            if response in response_paths:
                add("reused_review_response", f"{aid}: one response is counted for multiple slots.")
            response_paths.add(response)
            if response == execution:
                add("invalid_review_evidence", f"{aid}: keep response and execution capture distinct.")
        if not one_of(review.get("report_verdict"), {"pass", "needs_revision", "not_assessed"}):
            add("invalid_report_verdict", f"{aid}: declare a separate report_verdict.")
        coverage = review.get("coverage")
        if not isinstance(coverage, dict):
            coverage = {}
        for dimension in slot["dimensions"]:
            assessment = coverage.get(dimension)
            if (not isinstance(assessment, dict)
                    or not all(text(assessment.get(k)) for k in ("location", "basis"))):
                add("incomplete_review_coverage", f"{aid}: missing substantive coverage record for {dimension}.")
        auditor = audit.get("auditor_id")
        if not text(auditor) or auditor == slot["reviewer_id"]:
            add("self_validated_review", f"{aid}: a separate context must check review validity.")
        response_ref = review.get("response")
        if not isinstance(response_ref, dict) or audit.get("response_sha256") != response_ref.get("sha256"):
            add("stale_review_audit", f"{aid}: validity audit binds a different response.")
        audit_evidence = reference(audit.get("evidence"), f"{aid} validity audit")
        if audit_evidence is not None and audit_evidence in {response, execution}:
            add("invalid_review_audit", f"{aid}: a response or invocation is not its own validity audit.")
        if not text(audit.get("basis")):
            add("invalid_review_audit", f"{aid}: explain the validity decision.")
        observations = review.get("findings")
        decisions = audit.get("dispositions")
        if not isinstance(observations, list) or not all(isinstance(f, dict) for f in observations):
            add("invalid_review_findings", f"{aid}: findings must be a list, including an empty list.")
            observations = []
        ids = [f.get("finding_id") for f in observations]
        if not distinct_strings(ids, nonempty=False):
            add("invalid_review_findings", f"{aid}: finding ids must be distinct.")
        if not isinstance(decisions, dict) or set(decisions) != {i for i in ids if text(i)}:
            add("unhandled_review_findings", f"{aid}: each finding needs exactly one disposition.")
            decisions = {}
        for observation in observations:
            fid = observation.get("finding_id")
            if not text(fid):
                continue
            severity = observation.get("severity")
            if (not one_of(severity, SEVERITIES)
                    or not all(text(observation.get(k)) for k in ("location", "basis"))):
                add("invalid_review_findings", f"{aid}/{fid}: severity, location and basis are required.")
            disposition = decisions.get(fid, {})
            if (not isinstance(disposition, dict) or not one_of(disposition.get("decision"), DECISIONS)
                    or not all(text(disposition.get(k)) for k in ("reason", "evidence"))):
                add("unhandled_review_findings", f"{aid}/{fid}: an action label alone is not adjudication.")
                continue
            if one_of(severity, {"critical", "major"}) and auditor in (author, slot["reviewer_id"]):
                add("missing_independent_adjudication", f"{aid}/{fid}: critical or major findings need independent adjudication.")
            if report_delivery and disposition["decision"] not in {"resolved", "no_change"}:
                add("report_not_ready", f"{aid}/{fid}: unresolved required correction prevents report delivery.")
        if error_count == before:
            selected[sid] = aid

    sampling = plan.get("sampling")
    if (not isinstance(sampling, dict) or not text(sampling.get("method"))
            or not distinct_strings(sampling.get("population"))
            or not distinct_strings(sampling.get("selected"))
            or not distinct_strings(sampling.get("mandatory"), nonempty=False)):
        add("missing_sampling_plan", "Declare the sampling population, selection method, selected and mandatory item ids.")
        return result(len(slots))
    population, sample, mandatory = map(set, (sampling["population"], sampling["selected"], sampling["mandatory"]))
    if not mandatory <= sample <= population:
        add("invalid_sampling_plan", "Every mandatory item must be sampled; selected items must belong to the population.")
    samples = [r for r in rows if r.get("record_type") == "sampling_audit"]
    if not samples:
        add("missing_sampling_audit", "No sampling audit covers the declared selection.")
        return result(len(slots))
    sample_audit = samples[-1]
    if sample_audit.get("artifact_sha256") != artifact_hash or sample_audit.get("selected") != sampling["selected"]:
        add("stale_sampling_audit", "Sampling audit does not bind the current artifact and selected items.")
    sample_auditor = sample_audit.get("auditor_id")
    if not text(sample_auditor) or sample_auditor == author:
        add("missing_independent_sampling", "Sampling requires a context separate from the author.")
    reference(sample_audit.get("evidence"), "Sampling audit evidence")
    checks = sample_audit.get("checks")
    if not isinstance(checks, dict) or set(checks) != sample:
        add("incomplete_sampling_audit", "Record the outcome of every selected item, including passed items.")
    else:
        for item, check in checks.items():
            if (not isinstance(check, dict) or not one_of(check.get("result"), {"clear", "defect"})
                    or not text(check.get("evidence"))):
                add("incomplete_sampling_audit", f"{item}: missing result or evidence.")
            elif check["result"] == "defect":
                follow_up = check.get("follow_up")
                if (not one_of(check.get("defect_type"), {"report", "review_validity"})
                        or not isinstance(follow_up, dict)
                        or not one_of(follow_up.get("decision"), DECISIONS)
                        or not text(follow_up.get("reason"))):
                    add("unhandled_sampling_defect", f"{item}: record defect_type and a structured, evidenced follow-up decision.")
                    continue
                reference(follow_up.get("evidence"), f"{item} sampling follow-up")
                if (follow_up["decision"] not in {"resolved", "no_change"}
                        and (report_delivery or check["defect_type"] == "review_validity")):
                    add("unhandled_sampling_defect", f"{item}: delivery corrections and review-validity failures must be resolved or independently justified as no change.")
    return result(len(slots))


def main() -> int:
    # Imported here so delivery checks can use the shared inspector without a module cycle.
    from check_delivery import read_json_or_none, inspect_jsonl, sha256_file, resolve_inside
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task_directory", type=Path)
    parser.add_argument("--artifact", default="final.md")
    args = parser.parse_args()
    root = args.task_directory.resolve()
    progress = read_json_or_none(root / "state/progress.json")
    rows, errors = inspect_jsonl(root / "logs/review.jsonl", "Review")
    result = inspect_review_completion(root, progress if isinstance(progress, dict) else {},
                                       args.artifact, rows, hash_file=sha256_file, resolve_path=resolve_inside)
    if errors:
        result["ok"] = False
        result["flags"].append("invalid_review_log")
        result["findings"].extend(errors)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
