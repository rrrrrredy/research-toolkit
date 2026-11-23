"""Exercise the optional host adapter with local protocol fixtures, without model calls."""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
from unittest.mock import patch

import agent_session
import cli_agent_session
import codex_session
import host_review
import research_host
import research_workflow as workflow
from task_storage import load


def emit(**message):
    print(json.dumps(message), flush=True)


def fake_codex(mode):
    threads, turns = 0, 0
    roles, locked = {}, set()
    for line in sys.stdin:
        request = json.loads(line)
        method, params = request["method"], request.get("params", {})
        if method == "initialize":
            emit(id=request["id"], result={})
        elif method == "thread/start":
            threads += 1
            emit(id=request["id"], result={"thread": {"id": f"thread-{threads}"}})
        elif method == "thread/resume":
            thread = params["threadId"]
            role = roles.get(thread)
            if mode == "complete" and role in {("reviewer", None), ("auditor", "adjudicate")} and role not in locked:
                locked.add(role)
                reason = (f"no rollout found for thread id {thread}" if role == ("reviewer", None)
                          else f"thread {thread} already has an active writer")
                emit(id=request["id"], error={"code": -32600, "message": reason})
            elif mode == "complete" and role == ("acceptance", "reconcile"):
                emit(id=request["id"], error={"code": -32600, "message": f"no rollout found for thread id {thread}"})
            else:
                emit(id=request["id"], result={"thread": {"id": thread}})
        elif method == "turn/start":
            turns += 1
            thread = params["threadId"]
            turn = f"turn-{turns}"
            emit(id=request["id"], result={"turn": {"id": turn}})
            if mode == "malformed-terminal":
                emit(method="item/completed", params={})
                emit(method="turn/completed", params={"threadId": thread, "turn": {"id": turn}})
                continue
            disconnect = thread == "thread-2" and mode == "disconnect"
            content = "Partial observation." if disconnect else "The source supports twelve shipments."
            if mode == "complete":
                content, roles[thread] = complete_response(params["input"][0]["text"], Path(params["cwd"]))
            emit(method="item/completed", params={"threadId": thread, "turnId": turn,
                "item": {"type": "agentMessage", "id": "message", "phase": "final_answer", "text": content}})
            if disconnect:
                return
            emit(method="turn/completed", params={"threadId": thread,
                "turn": {"id": turn, "status": "completed"}})


def complete_response(prompt, workdir):
    if not prompt.startswith("Perform only the independent assignment at "):
        corrected = "# Depot shipment finding\n\nThe depot shipped twelve units. [Original record](depot.md)\n"
        if "twelve units" in (workdir.parents[2] / "report.md").read_text(encoding="utf-8"):
            return corrected, ("work", None)
        retained = workdir / "depot-correction.md"
        retained.write_text("The depot's correction confirms twelve units and no separate shipment.\n", encoding="utf-8")
        source = retained.relative_to(workdir.parents[2]).as_posix()
        (workdir / "records.json").write_text(json.dumps({
            "sources": [{"source_id": "main-manuscript-S1", "title": "Depot's correction", "url": "https://example.org/correction",
                         "source_type": "primary", "read_scope": "full_text", "read_evidence": source,
                         "evidence_path": source, "locator": "line 1"}],
            "claims": [{"claim_id": "main-manuscript-C1", "claim": "The correction confirms that no separate shipment was made.",
                        "claim_type": "verified_fact", "supporting_sources": ["main-manuscript-S1"]}],
            "draft": {"handoff": {"summary": "Corrected the manuscript against the retained depot record.",
                                  "pending": "Verify the corrected count against line 1.",
                                  "decisions": "Record twelve units and exclude a separate shipment."}},
        }), encoding="utf-8-sig")
        return corrected + "\nThe depot was at full capacity.\n", ("work", None)
    page = Path(prompt.split("assignment at ", 1)[1].split(". Read all supplied", 1)[0])
    version = re.search(r"## assignment_version\s+<code>&quot;([a-f0-9]+)&quot;</code>",
                        page.read_text(encoding="utf-8"))[1]
    root = page.parents[2]
    path, = root.glob(f"reviews/host/*/jobs/*-{version[:16]}.json")
    request = host_review.load_assignment(root, path.relative_to(root).as_posix())
    role, phase = request["role"], request.get("phase")
    finding = "The report's shipment count contradicts depot.md."
    basis = "The exact count in depot.md line 1 is twelve shipments."
    location = "Depot shipment paragraph"
    common = {k: request[k] for k in ("assignment_version", "input_version")}
    report = request["assignment"].get("report", "")
    needs_revision = "twenty-four" in report
    coverage = {dimension: {"location": location, "basis": basis}
                for dimension in request.get("dimensions", []) or workflow.DIMENSIONS}
    sample = {"location": location, "selection_reason": "The result turns on the shipment count.",
              "evidence": basis, "result": "clear"}
    if role == "reviewer":
        result = {"report_verdict": "needs_revision" if needs_revision else "pass", "coverage": coverage,
                  "findings": ([{"finding_id": "count", "severity": "major", "location": location,
                                 "basis": finding}] if needs_revision else [])}
    elif role == "verifier":
        result = {"result": "contradicted", "basis": basis,
                  "evidence": [{"path": "depot.md", "locator": "line 1", "observation": basis}]}
    elif role == "acceptance":
        needs_final_correction = phase == "reconcile" and "at full capacity" in report
        final_issue = "The statement about full capacity has no evidence in the depot record."
        result = {"result": "fail" if needs_final_correction else "pass",
                  "basis": final_issue if needs_final_correction else basis, "coverage": coverage,
                  "sample_checks": [sample], "open_issues": [final_issue] if needs_final_correction else []}
        if phase == "reconcile":
            result["blind_reconciliation"] = {}
    else:
        def decision(kind):
            return {"decision": kind, "reason": "Compared current text with original count.", "evidence": basis}

        findings = [slot_id + "/" + item["finding_id"] for slot_id, response in request["reviews"].items()
                    for item in response["record"]["findings"]]
        critical = [{"location": location, "evidence": basis, "result": "defect" if needs_revision else "clear"}]
        for requirement in request["assignment"]["effective_requirements"]:
            critical.append({**critical[0], "requirement_id": requirement["requirement_id"]})
        result = {"result": "valid", "report_verdict": "needs_revision" if needs_revision else "pass",
                  "basis": basis, "open_issues": [finding] if needs_revision else [],
                  "review_checks": {slot_id: {"result": "valid", "basis": basis} for slot_id in request["reviews"]},
                  "disposition_groups": ([{"finding_ids": findings, **decision("confirmed_defect")}] if findings else []),
                  "prior_findings": {item["attempt_id"] + "/" + item["finding"]["finding_id"]: decision("resolved")
                                     for item in request["assignment"]["prior_required_findings"]},
                  "critical_checks": critical, "sample_checks": [sample]}
        if phase == "initial" and needs_revision:
            result["verification_requests"] = [{"request_id": "shipment-count", "question": "What count does the original record establish?",
                "location": location, "decision_impact": "The total affects the reported stock.", "evidence_paths": ["depot.md"]}]
        if phase == "adjudicate":
            result["verification_decisions"] = {"shipment-count": decision("resolved")}
    return json.dumps({**common, **result}), (role, phase)


def fake_cli(mode):
    sys.stdin.read()
    if mode == "silent":
        time.sleep(8)
        return
    emit(type="step_start", sessionID="fixture-session", part={})
    if mode == "active":
        time.sleep(8)
        return
    emit(type="text", sessionID="fixture-session", part={
        "id": "part", "messageID": "message", "text": "The source supports twelve shipments."})
    if mode == "success":
        emit(type="step_finish", sessionID="fixture-session", part={"reason": "stop"})


def command(host, mode):
    return [sys.executable, str(Path(__file__).resolve()), "--fixture", host, mode]


def require(ok, context):
    if not ok:
        raise AssertionError(context)


def check_cli_transport(workspace):
    page = workspace / "packet.md"
    page.write_text("Synthetic retained page.", encoding="utf-8")
    for mode in ("success", "incomplete", "silent", "active"):
        session = cli_agent_session.CLIAgentSession(workspace, workspace / mode, "opencode", command("opencode", mode))
        try:
            if mode == "silent":
                with patch.object(cli_agent_session, "STARTUP_TIMEOUT", 2):
                    try:
                        session.start("Synthetic request.", read_paths=[page])
                    except RuntimeError as exc:
                        require("session identity" in str(exc), exc)
                    else:
                        raise AssertionError("Silent startup was accepted.")
            else:
                session_id, turn = session.start("Synthetic request.", read_paths=[page])
                require(session_id == "opencode:fixture-session", session_id)
                if mode != "active":
                    message = session.next_event(timeout=5)
                    terminal = session.next_event(timeout=5)
                    require(message["kind"] == "message" and message["turn"] == turn, message)
                    require(terminal["kind"] == "completed" and terminal["turn"] == turn, terminal)
                    require(terminal["status"] == ("completed" if mode == "success" else "failed"), terminal)
        finally:
            session.close()
        run = session.runs[0]
        require(run["process"].poll() is not None and not run["worker"].is_alive(), f"Leaked {mode} host process.")


def check_codex_protocol_failure(workspace):
    with patch.object(agent_session, "executable_for", return_value=command("codex", "malformed-terminal")):
        session = agent_session.CodexAgentSession(workspace, workspace / "malformed-terminal")
    try:
        thread, turn = session.start("Synthetic request.")
        event = session.next_event(timeout=5)
        require(event["kind"] == "error" and "turn/completed" in event["error"], event)
        require(event["raw"]["params"] == {"threadId": thread, "turn": {"id": turn}}, event)
    finally:
        stop = codex_session.stop_native_process
        def cleanup_error(process, job):
            stop(process, job)
            raise codex_session.ProcessCleanupError("fixture cleanup failure")
        with patch.object(codex_session, "stop_native_process", side_effect=cleanup_error):
            try:
                session.close()
            except codex_session.ProcessCleanupError:
                pass
            else:
                raise AssertionError("Cleanup failure must remain visible")
        require(session.client.trace.closed and session.client.stderr.closed, "Unclosed Codex trace or stderr")


def check_continuation(workspace):
    root = workspace / "case"
    workflow.start(workspace, "case", {"question": "What did the depot ship?", "audience": "Manager",
        "scope": "A single depot record", "output": "Two notes", "depth": "One paragraph per finding",
        "evidence_standard": "Read the full supplied depot record."})
    workflow.save_text(root, "depot.md", "The depot shipped twelve units.")
    require(workflow.save_records(workspace, "case", sources=[{"source_id": "S1", "title": "Depot record",
        "url": "https://example.org/depot", "source_type": "primary", "read_scope": "full_text",
        "read_evidence": "depot.md"}])["ok"], "Failed to save source.")
    for mode in ("disconnect", "resume"):
        with patch.object(agent_session, "executable_for", return_value=command("codex", mode)):
            with research_host.ResearchHost(workspace, "case", host="codex") as host:
                for unit in ("first", "second"):
                    host.submit({"unit_id": unit, "question": f"Develop the {unit} finding.", "source_ids": ["S1"]},
                                {"path": f"analysis/{unit}.md", "kind": "analysis", "complete": True})
                events = host.drain()["events"]
        first = root / "analysis" / "first.md"
        if mode == "disconnect":
            require(first.is_file() and not (root / "analysis" / "second.md").exists(), events)
            first_before = first.read_bytes()
            failed = next(event for event in events if event["outcome"] == "failed")
            require(failed["identity"] == "second", failed)
            require((root / failed["response"]).read_text(encoding="utf-8") == "Partial observation.", failed)
            require(load(root, failed["execution"])["status"] == "failed", failed)
        else:
            started = [event for event in events if event["outcome"] == "started"]
            require(len(started) == 1 and started[0]["identity"] == "second"
                    and started[0]["resumed"] and started[0]["execution_id"] == "thread-2", events)
            require(first.read_bytes() == first_before and (root / "analysis" / "second.md").is_file(), events)


def check_completion(workspace):
    task = "prepared"
    root = workspace / task
    original = "# Depot shipment finding\n\nThe depot shipped twenty-four units. [Original record](depot.md)\n"
    origin = "external:imported-draft"
    workflow.start(workspace, task, {"question": "What did the depot ship?", "audience": "Inventory manager",
        "scope": "A single depot record", "output": "A sourced finding", "depth": "A complete sourced paragraph",
        "evidence_standard": "Read the full supplied depot record."})
    workflow.save_text(root, "depot.md", "The depot shipped twelve units.")
    require(workflow.save_records(workspace, task,
        sources=[{"source_id": "S1", "title": "Depot record", "url": "https://example.org/depot", "source_type": "primary",
                  "read_scope": "full_text", "read_evidence": "depot.md"}],
        claims=[{"claim_id": "C1", "claim": "The depot recorded twelve units shipped.",
                 "claim_type": "verified_fact", "supporting_sources": ["S1"]}],
        requirements=[{"requirement_id": "R1", "summary": "Use the original depot record for the shipment count.",
                       "status": "pending", "reading_requirement": "full_text", "required_source_ids": ["S1"]},
                      {"requirement_id": "R2", "summary": "Keep the complete Markdown artifact between 40 and 200 nonwhitespace characters.",
                       "status": "pending", "length_constraint": {"unit": "nonwhitespace_characters", "scope": "whole_artifact",
                                                                    "min": 40, "max": 200}}],
        draft={"path": "report.md", "content": original, "main": True, "complete": True, "host_task": origin})["ok"],
        "Failed to prepare an independently checkable draft.")
    receipt = root / "state" / "final_delivery.json"
    premature = workflow.finish(workspace, task, artifact="report.md", delivery_message="The research report is complete.")
    require(not premature["completed"] and not receipt.exists(), premature)
    with patch.object(agent_session, "executable_for", return_value=command("codex", "complete")):
        with research_host.ResearchHost(workspace, task, host="codex", max_active=2) as host:
            peak = 0
            observe = host.observe

            def watch(event):
                nonlocal peak
                if event["outcome"] == "started":
                    peak = max(peak, len(host.active))
                    require(not receipt.exists(), "Delivery occurred before independent review finished.")
                return observe(event)

            with patch.object(host, "observe", side_effect=watch):
                result = host.complete(domains=["inventory"], writer_handoff_from=origin)
                require(result["status"] == "completed" and result["completed"] and result["delivery_check"]["ok"], result)
                require(result["recorded_requirements"] == ["R1", "R2"] and result["check_draft"]["ok"], result)
                require(peak == 2 and sum(e["outcome"] == "started" for e in host.results) > 2,
                        "Active turn limit was not exercised.")
            require(Path(result["artifact"]).samefile(root / "report.md") and Path(result["receipt"]).samefile(receipt), result)
            progress = load(root, "state/progress.json")
            require(progress["stage"] == "final" and progress["status"] == "complete"
                    and result["input_version"] == progress["review_plan"]["input_version"], progress)
            delivered = load(root, "state/final_delivery.json")
            require(delivered["status"] == "pass" and delivered["artifacts"]["report.md"] == result["artifact_sha256"],
                    delivered)
            require("twelve" in (root / "report.md").read_text(encoding="utf-8"), result)
            require(any(path.read_text(encoding="utf-8") == original
                        for path in root.glob("logs/record-backups/*/report.md")), "Original was not retained.")
            writer = progress["current_artifact"]["owner"]
            starts = [row for row in host.results if row["outcome"] == "started"]
            writer_turns = [row for row in starts if row["kind"] == "work"]
            require(writer != origin and [row["execution_id"] for row in writer_turns] == [writer, writer]
                    and any(row["identity"] == "full_report:acceptance"
                            for row in starts[starts.index(writer_turns[0]):starts.index(writer_turns[1])]),
                    "Each independent rejection must trigger exactly one writer turn before reassessment.")
            require("main-manuscript-S1" in (root / "data" / "source_registry.csv").read_text(encoding="utf-8")
                    and "main-manuscript-C1" in (root / "data" / "claims_registry.csv").read_text(encoding="utf-8"),
                    "The writer's additional evidence and claim must be saved before reassessment.")
            handoffs = [row["handoff"] for row in host_review.history_activity(root)
                        if row.get("operation") == "save" and row.get("outcome") == "saved"
                        and row.get("artifact") == "report.md" and row.get("host_task") == writer and "handoff" in row]
            require(handoffs == [{"summary": "Corrected the manuscript against the retained depot record.",
                                  "pending": ["Verify the corrected count against line 1."],
                                  "decisions": ["Record twelve units and exclude a separate shipment."]}], handoffs)
            unavailable = [row for row in host.results if row["outcome"] == "review_context_unavailable"]
            reassignments = [row for row in unavailable if row["identity"] != "full_report:acceptance"]
            require(len(reassignments) == 2 and any(row["identity"] == "full_report:audit" for row in reassignments), unavailable)
            for row in reassignments:
                require(any(start.get("reassigned_from") == row["prior_execution_id"]
                            and start["assignment_ref"] == row["assignment_ref"]
                            and start["execution_id"] != row["prior_execution_id"] and not start["resumed"]
                            for start in host.results if start["outcome"] == "started"), row)
            final_unavailable, = [row for row in unavailable if row["identity"] == "full_report:acceptance"]
            missed = host_review.load_assignment(root, final_unavailable["assignment_ref"]["path"])
            require(missed["phase"] == "correction_review" and missed["input_version"] == result["input_version"]
                    and "no rollout found" in (root / final_unavailable["protocol_path"]).read_text(encoding="utf-8"),
                    final_unavailable)
            final_turns = [(row, host_review.load_assignment(root, row["assignment_ref"]["path"])) for row in starts
                           if row["identity"] == "full_report:acceptance"]
            require([request["phase"] for _, request in final_turns] == ["blind", "reconcile", "blind", "reconcile"],
                    "An unavailable final reviewer must not start the exposed correction assignment.")
            (blind_start, blind), (reconcile_start, reconcile) = final_turns[-2:]
            require(blind["input_version"] == reconcile["input_version"] == missed["input_version"]
                    and blind_start["execution_id"] == reconcile_start["execution_id"] != missed["resume_host_task"]
                    and not blind_start["resumed"] and reconcile_start["resumed"], final_turns[-2:])
            require(sum(host_review.load_assignment(root, row["assignment_ref"]["path"])["input_version"]
                        == missed["input_version"] for row in starts if row["identity"] == "full_report:audit") == 1,
                    "The fallback must reuse the passing audit for this input.")
        recorded_receipt = receipt.read_bytes(), receipt.stat().st_mtime_ns
        with research_host.ResearchHost(workspace, task, host="codex", max_active=2) as resumed:
            existing = resumed.complete(domains=["inventory"], writer_handoff_from=origin)
            require(existing["completed"] and existing["input_version"] == result["input_version"]
                    and existing["check_draft"]["ok"] and existing["delivery_check"]["ok"], existing)
            require(not resumed.results, "Reopening verified delivery started new turns.")
        require((receipt.read_bytes(), receipt.stat().st_mtime_ns) == recorded_receipt,
                "Reopening verified delivery rewrote the receipt.")


def main():
    with tempfile.TemporaryDirectory(prefix="rtk-host-", dir=os.environ.get("IRF_TEST_TMPDIR")) as folder:
        workspace = Path(folder)
        check_cli_transport(workspace)
        check_codex_protocol_failure(workspace)
        check_continuation(workspace)
        check_completion(workspace)
    print("Optional host execution passed readiness, cleanup, two-slot scheduling, revision, and automatic verified delivery.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--fixture":
        (fake_codex if sys.argv[2] == "codex" else fake_cli)(sys.argv[3])
    elif len(sys.argv) > 1 and sys.argv[1] == "--check":
        main()
    else:
        # Bound the offline scenario itself, not a production research turn.
        subprocess.run([sys.executable, __file__, "--check"], timeout=60, check=True,
                       env={**os.environ, "RESEARCH_TOOLKIT_TELEMETRY": "off"})
