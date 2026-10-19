"""Small, explicit profile policy shared by workflow and offline delivery checks."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path, PureWindowsPath

CHECKLIST = {
    "requirements": "Answer the agreed brief and material follow-up requirements.",
    "claims_and_sources": "Check important claims against their sources and citations.",
    "counterevidence": "Address counter-evidence and uncertainty; qualify conclusions.",
    "sections": "Inspect each section of the current report for explanation and coverage, not repeated filler.",
    "reader_edit": "Check the full report and reject duplicated filler, repeated boilerplate, and cross-task or off-topic template text used to pad length; keep it useful to the named reader without internal IDs or production records, and cite the passages checked and any corrections.",
    "limitations": "Disclose evidence limits and the absence of independent review.",
}
LITE_LOG = [
    "SKIP research_review: profile=lite; no independent review is performed.",
    "SKIP full delivery gates: profile=lite; brief, claims and final checklist remain required.",
]


def checklist_errors(value):
    if not isinstance(value, dict):
        return ["Check the current report before submitting the checklist; record each item's actual findings and report/source locations, not a restatement of the criterion."]
    errors = [f"Checklist {key}: complete the check and resolve report defects before marking passed=true; evidence must describe actual findings and report/source locations. Keep passed=false while unchecked or unresolved; changing the flag alone does not fix the report."
            for key in CHECKLIST if not isinstance(value.get(key), dict)
            or value[key].get("passed") is not True
            or not isinstance(value[key].get("evidence"), str) or not value[key]["evidence"].strip()]
    for key in CHECKLIST:
        item = value.get(key)
        if not isinstance(item, dict) or "evidence_files" not in item:
            continue
        paths = item["evidence_files"]
        if (not isinstance(paths, list) or not paths
                or not all(isinstance(p, str) and p.strip() for p in paths)
                or len(set(paths)) != len(paths)):
            errors.append(f"Checklist {key}: evidence_files must be a nonempty list of distinct task-relative paths.")
    return errors


def lite_input_hashes(root: Path, items: dict) -> dict:
    """Bind declared local inputs without adding Full review/source-text gates."""
    # Local import keeps the standalone delivery checker and profile policy acyclic.
    from check_delivery import (inspect_csv_text, inspect_source_reading_evidence,
                                reading_evidence_target, resolve_inside, sha256_file)
    hashes = {}
    volatile = {"state/progress.json", "state/final_checklist.json", "logs/profile.jsonl", "delivery_message.md"}

    def bind(name, *, allow_empty=False, optional=False):
        if Path(name).is_absolute() or PureWindowsPath(name).drive or name.startswith("\\"):
            raise ValueError(f"Lite input must use a task-relative path: {name}")
        path = resolve_inside(root, name)
        if path is None:
            raise ValueError(f"Lite input must stay inside the task: {name}")
        relative = path.relative_to(root.resolve()).as_posix()
        if relative in volatile:
            raise ValueError(f"Use retained research evidence, not a workflow output: {relative}")
        if optional and not path.exists():
            hashes[relative] = None  # Adding a previously absent requirement ledger changes the input.
            return
        if not path.is_file():
            raise ValueError(f"Missing Lite input file: {relative}")
        if not allow_empty:
            with path.open("rb") as file:
                if not any(chunk.strip() for chunk in iter(lambda: file.read(65536), b"")):
                    raise ValueError(f"Empty Lite input file: {relative}")
        hashes[relative] = sha256_file(path)

    for name in ("state/task_spec.md", "data/source_registry.csv", "data/claims_registry.csv"):
        bind(name)
    bind("state/requirements.jsonl", allow_empty=True, optional=True)
    registry = root / "data/source_registry.csv"
    sources, errors = inspect_csv_text(registry.read_text(encoding="utf-8"),
        "data/source_registry.csv", ("source_id", "read_scope", "read_evidence"), "source_id")
    if errors:
        raise ValueError("; ".join(errors))
    for source in sources:
        if source.get("read_scope") not in {"full_text", "relevant_sections"}:
            continue
        errors = inspect_source_reading_evidence(root, source)
        if errors:
            raise ValueError("; ".join(errors))
        for field in ("url", "read_evidence"):
            target = reading_evidence_target(source.get(field))
            if target:
                bind(target)
        if source.get("evidence_path", "").strip():
            bind(source["evidence_path"].strip())
    for key in CHECKLIST:
        for name in items[key].get("evidence_files", []):
            bind(name)
    return hashes


def text_hash(path):
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")).hexdigest()


def lite_completion_errors(root: Path):
    """Honor recorded obligations while keeping Lite free of Full review gates."""
    from check_delivery import collect_open_issues, inspect_requirements
    errors, _ = inspect_requirements(root / "state/requirements.jsonl")
    try:
        progress = json.loads((root / "state/progress.json").read_text(encoding="utf-8"))
        if not isinstance(progress, dict):
            raise ValueError("Progress must be an object")
        if collect_open_issues(progress):
            errors.append("Lite delivery still has recorded open blockers; resolve them before completion.")
    except (OSError, ValueError):
        errors.append("Lite delivery needs readable current task progress.")
    return errors


def inspect_lite_delivery(root: Path, artifact="final.md", delivery_message="delivery_message.md"):
    """Check the lightweight receipt without claiming full delivery-gate acceptance."""
    errors = lite_completion_errors(root)
    length_checks = []
    version = None
    try:
        record = json.loads((root/"state/final_checklist.json").read_text(encoding="utf-8"))
        errors.extend(checklist_errors(record.get("items")))
        version = record.get("schema_version", 1)
        if type(version) is not int or version not in {1, 2}:
            errors.append("Unsupported Lite checklist schema_version.")
        if record.get("profile") != "lite" or record.get("artifact") != artifact:
            errors.append("Lite checklist does not identify this profile and artifact.")
        from check_delivery import inspect_length_constraints, length_receipt_matches
        length_checks, length_errors = inspect_length_constraints(root, artifact)
        errors.extend(length_errors)
        if not length_receipt_matches(record, length_checks):
            errors.append("Lite receipt length measurements differ from the current report and requirements.")
        for name in (artifact, delivery_message):
            path = (root/name).resolve()
            path.relative_to(root.resolve())
            if not path.is_file() or not path.read_text(encoding="utf-8").strip():
                errors.append(f"Missing nonempty lite delivery input: {name}.")
            elif record.get("artifacts", {}).get(name) != text_hash(path):
                errors.append(f"Lite checklist is stale for {name}.")
        if version == 2 and not errors:
            try:
                current = lite_input_hashes(root, record["items"])
                saved = record.get("input_hashes")
                if not isinstance(saved, dict) or set(saved) != set(current):
                    errors.append("Lite checklist research input set changed; recheck and resubmit the checklist.")
                else:
                    errors.extend(f"Lite checklist is stale for {name}." for name, digest in current.items() if saved[name] != digest)
            except (OSError, ValueError, TypeError, KeyError) as exc:
                errors.append(f"Cannot verify Lite research inputs: {exc}")
    except (OSError, ValueError, TypeError, AttributeError):
        errors.append("Lite delivery needs a readable final checklist and task-relative inputs.")
    return {"ok": not errors, "profile": "lite", "status": "checklist_complete" if not errors else "incomplete",
            **({"length_checks": length_checks} if length_checks else {}),
            "warnings": [], "flags": ["incomplete_lite_checklist"] if errors else [], "findings": errors,
            "log": LITE_LOG, "full_delivery_gates_checked": False,
            "independent_review": False, "review_strength": "unreviewed",
            "input_binding_scope": "report_message_and_research_inputs" if version == 2 else "report_and_message_only",
            "semantic_verification": False, "report_quality_certified": False}
