"""Current work references, separate from historical completion receipts."""
from __future__ import annotations

from check_delivery import inspect_jsonl_text, sha256_file


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
    from research_workflow import safe_path
    result = {"task_spec": "state/task_spec.md", "requirements": "state/requirements.jsonl",
              "artifact": None, "open_requirements": [], "warnings": []}
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
                if not isinstance(status, str):
                    result["warnings"].append("Requirement status is not text; retain the row and repair it through existing records.")
                    result["open_requirements"].append(row)
                elif status not in {"satisfied", "waived", "out_of_scope", "accepted_limitation"}:
                    result["open_requirements"].append(row)
    except (OSError, ValueError):
        result["warnings"].append("Requirements unreadable; inspect existing records before recovery.")
    result["scope"] = "Resume references, not proof of reading, applied feedback or semantic quality. No main artifact inferred for legacy tasks."
    return result


def require_current_artifact(progress, artifact):
    current = progress.get("current_artifact")
    if current is not None and current.get("path") != artifact:
        raise ValueError("artifact differs from the registered main draft. Use its path or explicitly register the intended main draft with draft.main=true.")
