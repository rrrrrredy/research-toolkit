"""Execute the bounded helpdesk continuation case; model review is an explicit phase.

Use --workspace outside the repository. No mock reviewer is used. `independent`
and `updated-review` consume the existing signed-in Codex account's model usage.
"""
from pathlib import Path
import argparse, csv, hashlib, io, json, shutil, sys, tempfile, time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import research_workflow as w
import codex_judge
from check_delivery import evaluate_delivery


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def csv_text(fields, rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader(); writer.writerows(rows)
    return stream.getvalue()


def inputs(root):
    w.save_text(root, "sources/plans.md", (REPO / "examples/lite/sources.md").read_text(encoding="utf-8"))
    rows = [{"source_id": sid, "title": title, "url": "sources/plans.md", "source_type": "constructed_plan_note",
             "read_scope": "full_text", "read_evidence": "sources/plans.md", "evidence_path": "sources/plans.md"}
            for sid, title in (("S1", "Cedar plan note"), ("S2", "Maple plan note"))]
    w.save_text(root, "data/source_registry.csv", csv_text(list(rows[0]), rows))
    claims = [
        {"claim_id": "C1", "claim": "Six Cedar seats cost $36/month at $6 each, exceeding $35.", "claim_type": "interpretation", "supporting_sources": "S1"},
        {"claim_id": "C2", "claim": "Maple covers six users at $28/month and manual CSV export.", "claim_type": "source_claim", "supporting_sources": "S2"},
        {"claim_id": "C3", "claim": "Trial Maple under the original constraints; CSV fields and service reliability still require checks.", "claim_type": "author_judgment", "supporting_sources": "S1;S2"}]
    w.save_text(root, "data/claims_registry.csv", csv_text(list(claims[0]), claims))
    report = (HERE / "report-lite.md").read_text(encoding="utf-8")
    w.save_text(root, "final.md", report)
    w.save_text(root, "state/task_spec.md", (root / "state/task_spec.md").read_text(encoding="utf-8") +
                "\nOutline: eligible choice and arithmetic; useful differences and unknowns; trial actions and change conditions.\n")
    row = {"requirement_id": "L1", "summary": "350–500 whitespace words in the whole Markdown artifact, including headings and citations.",
           "status": "pending", "evidence": "final.md", "length_constraint": {"unit": "whitespace_words", "scope": "whole_artifact", "min": 350, "max": 500}}
    w.save_text(root, "state/requirements.jsonl", json.dumps(row) + "\n")


def checklist():
    notes = {
        "requirements": "final.md answers the trial decision, six seats, $35 limit and manual weekly export; measured whole-file count is recorded in check-draft.json.",
        "claims_and_sources": "Compared all report paragraphs with S1/S2 in sources/plans.md: 6×6=36; Maple=28; headroom=7. No measured service performance is claimed.",
        "counterevidence": "What the choice buys retains Cedar scheduling/SSO, excludes them from current hard requirements, and preserves CSV-field and total-cost uncertainty.",
        "sections": "Three sections cover eligibility, trade-offs/unknowns and executable trial/change conditions; no required question is left to a heading alone.",
        "reader_edit": "Read the assembled final.md; recommendation and support-lead/operator actions are explicit; working records are outside the report.",
        "limitations": "The report identifies fictional evidence, missing CSV fields and unmeasured costs/performance; delivery message discloses author checks without independent review."}
    return {key: {"passed": True, "evidence": value} for key, value in notes.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=["prepare", "self-submit", "independent", "change", "updated-review"])
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--codex", type=Path)
    args = parser.parse_args(); workspace = args.workspace.resolve()
    if workspace.is_relative_to(REPO):
        raise ValueError("Keep executed tasks outside the installed repository")
    records = workspace / "execution-records"
    results = {}; started = time.monotonic()
    def record(name, value):
        write_json(records / (name + ".json"), value)
        results[name] = value
        return value
    if args.phase == "prepare":
        if workspace.exists():
            raise ValueError("Use a new workspace; preserved runs are never overwritten")
        brief = json.loads((REPO / "examples/lite/start.en.json").read_text(encoding="utf-8"))["brief"]
        brief["evidence_standard"] = "Read the complete two fictional plan notes; retain their provenance. Separate supported plan terms from proposed checks. Review status belongs in the delivery note."
        record("lite-start", w.start(workspace, "helpdesk-lite", brief, profile="lite"))
        lite = workspace / "helpdesk-lite"; inputs(lite)
        record("lite-draft-stage", w.status(workspace, "helpdesk-lite", stage="draft"))
        message = "Trial Maple under the original constraints. The report uses fictional plan notes and author checks; no independent review was performed."
        record("lite-pending-block", w.finish(workspace, "helpdesk-lite", message, checklist=checklist()))
        row = json.loads((lite / "state/requirements.jsonl").read_text(encoding="utf-8"))
        count = len((lite / "final.md").read_text(encoding="utf-8").split())
        if not 350 <= count <= 500:
            raise ValueError(f"Author report needs length repair: {count}")
        row.update(status="satisfied", evidence=f"final.md: {count} whitespace words, including markup and citations.")
        w.save_text(lite, "state/requirements.jsonl", json.dumps(row) + "\n")
        checked = record("lite-check-draft", w.check_draft(workspace, "helpdesk-lite"))
        w.save(lite, "check-draft.json", checked)
        record("lite-finish", w.finish(workspace, "helpdesk-lite", message, checklist=checklist()))
        record("lite-preserved-hashes", {p.relative_to(lite).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                                        for p in lite.rglob("*") if p.is_file() and p.name != ".research-toolkit.lock"})
        for task in ("helpdesk-full-self", "helpdesk-full"):
            record(task + "-start", w.start(workspace, task, brief, profile="full"))
            root = workspace / task
            for name in ("final.md", "data/source_registry.csv", "data/claims_registry.csv", "state/requirements.jsonl"):
                w.save_text(root, name, (lite / name).read_text(encoding="utf-8"))
            shutil.copytree(lite / "sources", root / "sources", dirs_exist_ok=True)
            w.save_text(root, "state/task_spec.md", (root / "state/task_spec.md").read_text(encoding="utf-8") +
                        "\nContinue the retained report and evidence from sibling task helpdesk-lite. New purpose: formal review and delivery consistency. Original report SHA-256: " + w.sha256_file(lite / "final.md") + ". No source acquisition or requirement re-entry is needed.\n")
            record(task + "-draft-stage", w.status(workspace, task, stage="draft"))
        record("self-prompt", w.review(workspace, "helpdesk-full-self", ["sources/plans.md"], reviewer="self"))
    elif args.phase == "self-submit":
        prompt = json.loads((records / "self-prompt.json").read_text(encoding="utf-8"))
        review = json.loads((HERE / "self-review.json").read_text(encoding="utf-8"))
        review["input_version"] = prompt["input_version"]
        record("self-review", w.review(workspace, "helpdesk-full-self", ["sources/plans.md"], reviewer="self", self_review=review))
        record("self-finish", w.finish(workspace, "helpdesk-full-self", "Maple trial brief delivered after author-context self-review (degraded review strength), without an independent opinion. Fictional sources; CSV fields and service performance remain unmeasured."))
    elif args.phase == "change":
        root = workspace / "helpdesk-full"
        for name in ("final.md", "state/task_spec.md", "state/progress.json", "state/requirements.jsonl", "data/claims_registry.csv", "data/source_registry.csv", "state/final_delivery.json"):
            destination = workspace / "before-update" / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root / name, destination)
        w.save_text(root, "source-update.md", (HERE / "source-update.md").read_text(encoding="utf-8"))
        sources = list(csv.DictReader((root / "data/source_registry.csv").read_text(encoding="utf-8").splitlines()))
        sources.append({"source_id": "S3", "title": "Revised Cedar quote and scheduled-export requirement, constructed scenario v2", "url": "source-update.md", "source_type": "constructed_follow_up", "read_scope": "full_text", "read_evidence": "source-update.md", "evidence_path": "source-update.md"})
        w.save_text(root, "data/source_registry.csv", csv_text(list(sources[0]), sources))
        requirement = {"requirement_id": "R2", "summary": "Scenario v2 now requires scheduled weekly CSV; use the revised Cedar price, same six seats and $35 ceiling.", "status": "pending", "evidence": "source-update.md"}
        w.save_text(root, "state/requirements.jsonl", (root / "state/requirements.jsonl").read_text(encoding="utf-8") + json.dumps(requirement) + "\n")
        w.save_text(root, "state/task_spec.md", (root / "state/task_spec.md").read_text(encoding="utf-8") +
                    "\nScenario-v2 follow-up overrides the original manual-export allowance and extends the source set: read source-update.md; scheduled weekly exports are now required, Cedar is $5 per seat, and all other constraints and length remain. Preserve the original conclusion as history and update the current recommendation.\n")
        progress = w.load(root, "state/progress.json")
        progress["brief"]["scope"] = "Six seats, $35 subscription ceiling, now scheduled weekly CSV mandatory; use original sources/plans.md plus constructed source-update.md v2. SSO optional; staff and migration costs unmeasured."
        w.save(root, "state/progress.json", progress)
        record("changed-input-delivery-check", evaluate_delivery(root))
        record("changed-input-finish-block", w.finish(workspace, "helpdesk-full", "Attempted stale delivery; intentionally expected to fail."))
        record("resume-changed-task", w.status(workspace, "helpdesk-full", stage="revise"))
        w.save_text(root, "final.md", (HERE / "report-updated.md").read_text(encoding="utf-8"))
        rows = list(csv.DictReader((root / "data/claims_registry.csv").read_text(encoding="utf-8").splitlines()))
        rows[0]["claim"] = "Original quote was $36 for six; revised confirmed scenario-v2 quote is $30, within $35."
        rows[0]["supporting_sources"] = "S1;S3"
        rows[2]["claim"] = "Trial Cedar: revised $30 quote and scheduled export meet v2 requirements; Maple manual export no longer qualifies."
        rows[2]["supporting_sources"] = "S1;S2;S3"
        w.save_text(root, "data/claims_registry.csv", csv_text(list(rows[0]), rows))
        count = len((root / "final.md").read_text(encoding="utf-8").split())
        if not 350 <= count <= 500:
            raise ValueError(f"Updated report needs length repair: {count}")
        requirements = [json.loads(line) for line in (root / "state/requirements.jsonl").read_text(encoding="utf-8").splitlines()]
        requirements[0]["evidence"] = f"final.md: {count} whitespace words, including markup and citations."
        requirements[1].update(status="satisfied", evidence="final.md: six × $5 = $30; Cedar scheduling required and supplied; original Maple decision preserved separately.")
        w.save_text(root, "state/requirements.jsonl", "\n".join(json.dumps(row) for row in requirements) + "\n")
        record("updated-check-draft", w.check_draft(workspace, "helpdesk-full"))
    else:
        if not args.codex or not args.codex.is_file():
            raise ValueError("Supply the existing signed-in Codex executable; no account is created")
        updated = args.phase == "updated-review"; label = "updated" if updated else "independent"
        settings = {"model": "gpt-6-astra", "reasoning_effort": "medium"}
        with tempfile.TemporaryDirectory(prefix="toolkit-review-context-") as temp:
            instruction = Path(temp) / "instructions.txt"
            instruction.write_text("You are an independent reviewer. Use only the supplied task, report and source evidence. Return the requested JSON. Do not use tools or speculate about experimental conditions. Do not require outside people or additional vendors.\n", encoding="utf-8")
            command = codex_judge.command(args.codex.resolve(), temp, instruction, settings)
            config = {"reviewers": [{"id": "astra", "backend": "codex", "format": "codex-jsonl", "model": "gpt-6-astra", "command": command, "timeout_seconds": 600}]}
            evidence = ["sources/plans.md", "source-update.md"] if updated else ["sources/plans.md"]
            result = record(label + "-review", w.review(workspace, "helpdesk-full", evidence, reviewer="independent", revision=updated, config=config))
            if not result.get("delivery_ready"):
                raise ValueError("The actual review is not delivery-ready. Read the retained finding or failure and address it; do not rerun unchanged output for a pass.")
            record(label + "-finish", w.finish(workspace, "helpdesk-full", ("Cedar trial brief updated for the revised quote and required scheduling." if updated else "Maple trial brief retained without substantive changes.") + " Reviewed by requested gpt-6-astra in a fresh context; no additional auditor. Fictional source scenario, no market or service-performance measurements."))
            if not updated:
                record("resume-unchanged-task", w.status(workspace, "helpdesk-full"))
                record("resume-review-no-new-call", w.review(workspace, "helpdesk-full", evidence, reviewer="independent", config=config))
    record(args.phase + "-elapsed", {"seconds": round(time.monotonic() - started, 3), "phase": args.phase})
    print(json.dumps({name: {key: value.get(key) for key in ("completed", "ok", "delivery_ready", "reviews_complete", "action_required", "counts", "errors", "error") if key in value}
                      for name, value in results.items()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
