"""Exercise the optional host adapter with local protocol fixtures, without model calls."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from unittest.mock import patch

import agent_session
import cli_agent_session
import research_host
import research_workflow as workflow
from task_storage import load


def emit(**message):
    print(json.dumps(message), flush=True)


def fake_codex(mode):
    threads = 0
    for line in sys.stdin:
        request = json.loads(line)
        method, params = request["method"], request.get("params", {})
        if method == "initialize":
            emit(id=request["id"], result={})
        elif method == "thread/start":
            threads += 1
            emit(id=request["id"], result={"thread": {"id": f"thread-{threads}"}})
        elif method == "thread/resume":
            emit(id=request["id"], result={"thread": {"id": params["threadId"]}})
        elif method == "turn/start":
            thread = params["threadId"]
            turn = "turn-" + thread
            emit(id=request["id"], result={"turn": {"id": turn}})
            disconnect = thread == "thread-2" and mode == "disconnect"
            content = "Partial observation." if disconnect else "The source supports twelve shipments."
            emit(method="item/completed", params={"threadId": thread, "turnId": turn,
                "item": {"type": "agentMessage", "id": "message", "phase": "final_answer", "text": content}})
            if disconnect:
                return
            emit(method="turn/completed", params={"threadId": thread,
                "turn": {"id": turn, "status": "completed"}})


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


def main():
    with tempfile.TemporaryDirectory(prefix="rtk-host-", dir=os.environ.get("IRF_TEST_TMPDIR")) as folder:
        workspace = Path(folder)
        check_cli_transport(workspace)
        check_continuation(workspace)
    print("Optional host execution passed readiness, terminal status, cleanup, and preserved-state continuation.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--fixture":
        (fake_codex if sys.argv[2] == "codex" else fake_cli)(sys.argv[3])
    elif len(sys.argv) > 1 and sys.argv[1] == "--check":
        main()
    else:
        # Bound the offline scenario itself, not a production research turn.
        subprocess.run([sys.executable, __file__, "--check"], timeout=35, check=True,
                       env={**os.environ, "RESEARCH_TOOLKIT_TELEMETRY": "off"})
