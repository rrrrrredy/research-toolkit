"""Agent tool hook: record metadata only for Toolkit-activated sessions."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sqlite3
import sys
import uuid

import usage_events as usage

EVENTS = {"UserPromptSubmit": "user_turn", "PreToolUse": "tool_observed", "PostToolUse": "tool_observed",
          "PostToolUseFailure": "tool_observed", "SubagentStart": "agent_started", "SubagentStop": "agent_finished",
          "Stop": "session_stopped", "SessionEnd": "session_stopped", "Interrupt": "session_stopped",
          "PreCompact": "session_compacted", "PostCompact": "session_compacted"}
TOOLS = {"read": "read", "write": "write", "edit": "edit", "apply_patch": "edit", "bash": "shell",
         "exec_command": "shell", "glob": "search", "grep": "search", "websearch": "search",
         "webfetch": "browse", "skill": "skill", "agent": "delegate", "task": "delegate",
         "spawn_agent": "delegate", "send_message": "delegate", "wait": "delegate"}
RESEARCH_TOOLS = {"research_start": "start", "research_save": "save", "research_status": "status",
                  "research_guide": "guide", "research_review": "review", "research_finish": "finish",
                  "research_check_draft": "check-draft", "research_check_reviewer": "check-reviewer",
                  "research_check_updates": "check-updates"}


def toolkit_invocation(payload):
    values = payload.get("tool_input", {})
    if not isinstance(values, dict):
        return False
    name = str(payload.get("tool_name", "")).split("__")[-1].lower()
    if name in RESEARCH_TOOLS:
        return True
    skill = str(values.get("skill", values.get("name", ""))).split(":")[-1]
    if name == "skill" and skill == "research-toolkit":
        return True
    path = str(values.get("file_path", values.get("filePath", values.get("path", "")))).replace("\\", "/").lower()
    command = str(values.get("command", values.get("cmd", ""))).replace("\\", "/").lower()
    return path.endswith(("/research-toolkit/skill.md", "/research-toolkit/skill.zh-cn.md")) or bool(
        re.search(r"research-toolkit/(?:skill(?:\.zh-cn)?\.md|scripts/(?:research_workflow|research_mcp)\.py)\b", command))


def method_name(values):
    path = str(values.get("file_path", values.get("filePath", values.get("path", "")))).replace("\\", "/").lower()
    name = path.rsplit("/", 1)[-1].removesuffix(".md").removesuffix(".zh-cn")
    return name if name in usage.METHODS else None


def handle(payload, host):
    if usage.disabled_by_environment() or not isinstance(payload, dict):
        return
    event = payload.get("hook_event_name")
    session = payload.get("session_id")
    if event not in EVENTS or not isinstance(session, str) or not session:
        return
    scoped = host+":"+session
    values = payload.get("tool_input", {})
    values = values if isinstance(values, dict) else {}
    invoke = toolkit_invocation(payload)
    prompt = payload.get("prompt") if event == "UserPromptSubmit" else None
    requested = isinstance(prompt, str) and (bool(re.search(r"research[- ]toolkit", prompt, re.I)) or "研究工具箱" in prompt)
    with usage.database() as db:
        config = usage.settings(db)
        if config["enabled"] != "on":
            return
        current = db.execute("SELECT * FROM sessions WHERE id=?", (scoped,)).fetchone()
        parent = payload.get("parent_session_id") or (current["parent"] if current else None)
        parent_row = db.execute("SELECT * FROM sessions WHERE id=?", (host+":"+parent,)).fetchone() if parent else None
        active = bool(current and current["active"]) or bool(parent_row and parent_row["active"])
        if not (active or invoke or requested):
            return
        task = current["task"] if current else (parent_row["task"] if parent_row else None)
        alias = values.get("task")
        if isinstance(alias, str):
            candidates = db.execute("SELECT task FROM aliases WHERE alias=?", (alias,)).fetchall()
            task = candidates[0]["task"] if len(candidates) == 1 else None
        db.execute("INSERT INTO sessions VALUES (?,?,?,?) ON CONFLICT(id) DO UPDATE SET active=1,task=excluded.task",
                   (scoped, 1, task, parent))
        usage.notice(db, config)
        if config.get("seen") != "1":
            usage.enqueue(db, config, "installation_seen", host=host, entry="skill")
            usage.set_setting(db, "seen", "1")
        identity = payload.get("tool_use_id") or payload.get("turn_id") or payload.get("prompt_id") or payload.get("event_id")
        if not identity:
            # Agent tools without event IDs can legitimately repeat the same prompt.
            # The queued event ID stays stable for upload retries, not new hooks.
            identity = uuid.uuid4().hex
        event_id = usage.opaque(config, "native-event", scoped+":"+event+":"+str(identity)+":"+str(payload.get("agent_id", "")))
        name = str(payload.get("tool_name", "")).split("__")[-1].lower()
        operation = RESEARCH_TOOLS.get(name, TOOLS.get(name, "other"))
        outcome = "started" if event == "PreToolUse" else "unknown"
        response = payload.get("tool_response")
        if event == "PostToolUseFailure" or (isinstance(response, dict) and (response.get("isError") is True
                or (operation == "shell" and type(response.get("exit_code")) is int and response["exit_code"] != 0))):
            outcome = "failed"
        elif event == "PostToolUse":
            outcome = "received"  # Receiving output alone does not prove operation success.
        elif event in {"Stop", "SubagentStop"}:
            outcome = "completed"  # A turn/agent completion, not research delivery.
        elif event == "SubagentStart":
            outcome = "started"
        elif event == "Interrupt":
            outcome = "cancelled"
        if invoke and not active:
            usage.enqueue(db, config, "toolkit_activated", host=host, entry="skill", session=session,
                          event_id=usage.opaque(config, "activation", event_id), outcome="received")
        child = payload.get("agent_id") if event in {"SubagentStart", "SubagentStop"} else None
        kind = "agent_input" if event == "UserPromptSubmit" and parent else "agent_finished" if event == "Stop" and parent else EVENTS[event]
        usage.enqueue(db, config, kind, host=host, entry="skill", operation=operation,
                      task=task if event != "UserPromptSubmit" else None,
                      session=child or session, parent=session if child else parent,
                      call=payload.get("tool_use_id"), event_id=event_id, outcome=outcome, method=method_name(values))
        if child and event == "SubagentStart":
            db.execute("INSERT INTO sessions VALUES (?,?,?,?) ON CONFLICT(id) DO UPDATE SET active=1,task=excluded.task,parent=excluded.parent",
                       (host+":"+child, 1, task, session))
        if event == "SessionEnd":
            db.execute("UPDATE sessions SET active=0 WHERE id=? OR parent=?", (scoped, session))
    usage.schedule_upload()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", choices=["codex", "claude", "opencode", "auto"], required=True)
    args = parser.parse_args()
    try:
        raw = sys.stdin.buffer.read(2*1024*1024+1)
        if len(raw) > 2*1024*1024:
            raise ValueError("hook input too large")
        payload = json.loads(raw)
        host = args.host
        if host == "auto":
            host = "codex" if "turn_id" in payload or os.environ.get("CODEX_THREAD_ID") else "claude"
        handle(payload, host)
    except (OSError, ValueError, sqlite3.Error, TypeError) as exc:
        usage.failure(exc)
    # No hook decision or injected instruction. Research proceeds unchanged.


if __name__ == "__main__":
    main()
