"""Agent tool selection and the common event boundary for Agent execution."""
from __future__ import annotations

import os
from pathlib import Path
import queue
import shutil
import signal
import subprocess
import time

from review_process import ProcessCleanupError


HOSTS = ("claude", "opencode", "codex")
PROCESS_EXIT_TIMEOUT = 5


def stop_native_process(process, job):
    """Stop a local host and its descendants, even if the parent already exited."""
    try:
        if job:
            job.close()  # Kill-on-close covers children holding the protocol pipes open.
            if process and process.poll() is None:
                process.kill()  # Also close a launch gate whose job attachment failed.
        elif process:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        if process:
            process.wait(timeout=PROCESS_EXIT_TIMEOUT)
    except (OSError, subprocess.TimeoutExpired) as exc:
        target = f"PID {process.pid}" if process is not None else "the launch job"
        raise ProcessCleanupError(f"Native process cleanup could not be confirmed for {target}.") from exc


def select_host(host=None):
    host = host or os.environ.get("RESEARCH_TOOLKIT_HOST")
    if not host:
        detected = [name for name, present in (
            ("claude", os.environ.get("CLAUDECODE")),
            ("codex", os.environ.get("CODEX_THREAD_ID"))) if present]
        if not detected:
            detected = [name for name in HOSTS if shutil.which(name)]
        if len(detected) == 1:
            host = detected[0]
    if host not in HOSTS:
        raise ValueError("host: specify the current agent tool with --host claude, opencode or codex "
                         "(or RESEARCH_TOOLKIT_HOST). No agent tool is selected as a fallback.")
    return host


def executable_for(host, executable=None):
    value = executable or shutil.which(host + ".exe") or shutil.which(host)
    if not value:
        raise OSError(f"{host}: executable not found; use the installed agent tool or --executable PATH.")
    path = Path(value).expanduser().resolve()
    if not path.is_file():
        raise OSError(f"executable: file not found: {path}")
    if os.name == "nt" and path.suffix.lower() in {".cmd", ".bat"}:
        # Resolve common npm installations without running a shell or putting
        # prompts in command-line quoting. Other wrappers can supply the binary.
        candidates = {
            "claude": [(path.parent / "node_modules/@anthropic-ai/claude-code/cli.js")],
            "opencode": [(path.parent / "node_modules/opencode-ai/bin/opencode.exe")],
        }.get(host, [])
        for candidate in candidates:
            if candidate.is_file():
                if candidate.suffix == ".js" and shutil.which("node"):
                    return [shutil.which("node"), str(candidate)]
                if candidate.suffix == ".exe":
                    return [str(candidate)]
        raise OSError(f"{host}: {path} is a shell wrapper; pass --executable with the native executable path.")
    return [str(path)]


def native_id(host, previous):
    if not previous:
        return None
    prefix, separator, identity = previous.partition(":")
    if separator:
        if prefix != host or not identity:
            raise ValueError(f"host_task {previous!r} belongs to another agent tool; resume its owner with --host {prefix}.")
        return identity
    # v2.2.0 saved unqualified Codex IDs. Keep those tasks resumable.
    if host == "codex":
        return previous
    raise ValueError(f"host_task {previous!r} has no {host} identity; keep its original agent tool or use native handoff.")


class CodexAgentSession:
    name = "codex"
    supports_steer = True

    def __init__(self, cwd, directory, executable=None):
        from codex_session import CodexSession
        self.client = CodexSession(cwd, directory, command=executable_for(self.name, executable))

    def start(self, prompt, previous=None, read_paths=None, *, workdir=None):
        session = self.client.thread(native_id(self.name, previous), cwd=workdir)
        return session, self.client.turn(session, prompt, cwd=workdir)

    def steer(self, session, turn, prompt):
        return self.client.steer(session, turn, prompt)

    def next_event(self, timeout=1):
        deadline = time.monotonic() + timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise queue.Empty
            raw = self.client.events.get(timeout=remaining)
            method, params = raw.get("method"), raw.get("params", {})
            if "id" in raw:
                try:
                    self.client.send({"id": raw["id"], "error": {"code": -32601,
                        "message": "Return the unresolved action to the coordinator; this adapter cannot approve it."}})
                except RuntimeError as exc:
                    # Process the queued terminal notifications, including any completed turns.
                    return {"kind": "request", "method": method, "raw": raw, "error": str(exc)}
                return {"kind": "request", "method": method, "raw": raw}
            if method in {"transport/error", "transport/closed"}:
                return {"kind": "error", "raw": raw}
            event = {"session": params.get("threadId"), "turn": params.get("turnId"), "raw": raw}
            if method == "item/completed" and params["item"]["type"] == "agentMessage":
                return {**event, "kind": "message", **{k: params["item"].get(k) for k in ("id", "text", "phase")}}
            if method == "turn/completed":
                return {**event, "kind": "completed", "turn": params["turn"]["id"],
                        "status": params["turn"]["status"]}

    def close(self):
        self.client.close()


def open_session(cwd, directory, host=None, executable=None):
    host = select_host(host)
    if host == "codex":
        return CodexAgentSession(cwd, directory, executable)
    from cli_agent_session import CLIAgentSession
    return CLIAgentSession(cwd, directory, host, executable_for(host, executable))
