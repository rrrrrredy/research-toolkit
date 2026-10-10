"""Small, explicit profile policy shared by workflow and offline delivery checks."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

CHECKLIST = {
    "requirements": "Answer the agreed brief and material follow-up requirements.",
    "claims_and_sources": "Check important claims against their sources and citations.",
    "counterevidence": "Address counter-evidence and uncertainty; qualify conclusions.",
    "sections": "Draft and inspect each section for adequate explanation and coverage.",
    "reader_edit": "Remove internal IDs and production narration; edit for the reader.",
    "limitations": "Disclose evidence limits and the absence of independent review.",
}
LITE_LOG = [
    "SKIP research_review: profile=lite; no independent review is performed.",
    "SKIP full delivery gates: profile=lite; brief, claims and final checklist remain required.",
]


def checklist_errors(value):
    if not isinstance(value, dict):
        return ["Provide the final checklist with every item and its evidence."]
    return [f"Checklist {key}: require passed=true and a substantive evidence/location."
            for key in CHECKLIST if not isinstance(value.get(key), dict)
            or value[key].get("passed") is not True
            or not isinstance(value[key].get("evidence"), str) or not value[key]["evidence"].strip()]


def text_hash(path):
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")).hexdigest()


def inspect_lite_delivery(root: Path, artifact="final.md", delivery_message="delivery_message.md"):
    """Check the lightweight receipt without claiming full delivery-gate acceptance."""
    errors = []
    try:
        record = json.loads((root/"state/final_checklist.json").read_text(encoding="utf-8"))
        errors.extend(checklist_errors(record.get("items")))
        if record.get("profile") != "lite" or record.get("artifact") != artifact:
            errors.append("Lite checklist does not identify this profile and artifact.")
        for name in (artifact, delivery_message):
            path = (root/name).resolve()
            path.relative_to(root.resolve())
            if not path.is_file() or not path.read_text(encoding="utf-8").strip():
                errors.append(f"Missing nonempty lite delivery input: {name}.")
            elif record.get("artifacts", {}).get(name) != text_hash(path):
                errors.append(f"Lite checklist is stale for {name}.")
    except (OSError, ValueError, TypeError, AttributeError):
        errors.append("Lite delivery needs a readable final checklist and task-relative inputs.")
    return {"ok": not errors, "profile": "lite", "status": "checklist_complete" if not errors else "incomplete",
            "warnings": [], "flags": ["incomplete_lite_checklist"] if errors else [], "findings": errors,
            "log": LITE_LOG, "full_delivery_gates_checked": False,
            "independent_review": False, "review_strength": "unreviewed",
            "semantic_verification": False, "report_quality_certified": False}
