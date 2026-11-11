"""Claude Code and OpenCode native CLI sessions behind the Agent event boundary."""
from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import queue
import signal
import subprocess
import sys
import threading
import uuid

from agent_session import native_id
from review_process import WindowsJob, WINDOWS_GATE


class CLIAgentSession:
    supports_steer = False

    def __init__(self, cwd, directory, host, executable):
        self.cwd, self.directory = Path(cwd).resolve(), Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.name, self.executable = host, executable
        self.events, self.runs = queue.Queue(), []
        self.lock = threading.Lock()
        self.trace = (self.directory / "protocol.jsonl").open("a", encoding="utf-8")

    def record(self, turn, direction, message):
        with self.lock:
            self.trace.write(json.dumps({"at": datetime.now(timezone.utc).isoformat(),
                "host": self.name, "turn": turn, "direction": direction, "message": message}, ensure_ascii=False) + "\n")
            self.trace.flush()

    def start(self, prompt, previous=None, read_paths=None, *, workdir=None):
        previous = native_id(self.name, previous)
        turn = uuid.uuid4().hex
        command = list(self.executable)
        paths = [str(Path(p).resolve()) for p in (read_paths or [])]
        if not paths:
            raise ValueError("Prepared research execution needs the retained reading pages for this invocation.")
        cwd = Path(workdir).resolve() if workdir else self.cwd
        if self.name == "claude":
            command += ["-p", "--output-format", "stream-json", "--verbose"]
            command += ["--resume", previous] if previous else ["--session-id", str(uuid.uuid4())]
        else:
            command += ["run", "--format", "json", "--dir", str(cwd)]
            if previous:
                command += ["--session", previous]
        run = {"turn": turn, "previous": previous, "read_paths": paths, "cwd": cwd,
               "ready": queue.Queue(), "process": None, "job": None}
        self.runs.append(run)
        self.record(turn, "send", {"argv": command, "prompt": prompt})
        run["worker"] = threading.Thread(target=self._run, args=(run, command, prompt), daemon=True)
        run["worker"].start()
        # Wait for the native session identity, not for generated content. A
        # launch/error/EOF before identification wakes this queue with the error.
        identity = run["ready"].get()
        if isinstance(identity, Exception):
            raise identity
        return identity, turn

    def _run(self, run, command, prompt):
        session, failure, result = None, None, None
        text_parts, final_reason = {}, None
        stderr = (self.directory / (run["turn"] + ".stderr.txt")).open("w", encoding="utf-8")
        try:
            run["job"] = WindowsJob() if os.name == "nt" else None
            argv = [sys.executable, "-c", WINDOWS_GATE, json.dumps(command)] if run["job"] else command
            env = os.environ.copy()
            # This is a separate native session, not a nested turn of the parent.
            # Keep account/model settings, but do not inherit parent identity.
            for key in ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CODEX_THREAD_ID"):
                env.pop(key, None)
            # Keep the installed tool's tools, permissions and provider settings.
            # Research may require searches, downloads and executable calculations.
            process = run["process"] = subprocess.Popen(argv, cwd=run["cwd"], env=env,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr,
                text=True, encoding="utf-8", bufsize=1,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
                start_new_session=os.name != "nt")
            if run["job"]:
                run["job"].attach(process.pid)
                process.stdin.write("1")
                process.stdin.flush()
            process.stdin.write(prompt)
            process.stdin.close()
            for line in process.stdout:
                try:
                    raw = json.loads(line)
                except ValueError:
                    self.record(run["turn"], "receive", {"unparsed": line})
                    failure = "Native CLI emitted non-JSON output; inspect the original protocol."
                    continue
                self.record(run["turn"], "receive", raw)
                identity = raw.get("session_id") if self.name == "claude" else raw.get("sessionID")
                if identity and not session:
                    if run["previous"] and identity != run["previous"]:
                        raise ValueError("Native CLI resumed a different session than the recorded owner.")
                    session = self.name + ":" + identity
                    run["ready"].put(session)
                if self.name == "claude":
                    if raw.get("type") == "result":
                        result = raw
                else:
                    if raw.get("type") == "error":
                        failure = raw.get("error") or "Native CLI reported an error."
                    part = raw.get("part", {})
                    if raw.get("type") == "text":
                        text_parts[part["id"]] = part
                    if raw.get("type") == "step_finish":
                        final_reason = part.get("reason")
            code = process.wait()
            if self.name == "claude":
                content = result.get("result", "") if result else ""
                completed = result and not result.get("is_error") and result.get("subtype") == "success"
            else:
                parts = list(text_parts.values())
                last_message = parts[-1].get("messageID") if parts else None
                content = "\n\n".join(p["text"] for p in parts if p.get("messageID") == last_message)
                completed = final_reason == "stop"
            if not session:
                raise RuntimeError(f"{self.name}: no native session returned (exit {code}); see {stderr.name}.")
            if content:
                self.events.put({"kind": "message", "session": session, "turn": run["turn"],
                    "id": run["turn"], "phase": "final_answer", "text": content})
            self.events.put({"kind": "completed", "session": session, "turn": run["turn"],
                "status": "completed" if code == 0 and completed and not failure else "failed",
                "raw": {"exit_code": code, "error": failure, "result": result, "finish_reason": final_reason}})
        except Exception as exc:
            self.record(run["turn"], "error", str(exc))
            if session:
                self.events.put({"kind": "completed", "session": session, "turn": run["turn"],
                    "status": "failed", "raw": {"error": str(exc)}})
            else:
                run["ready"].put(exc)
        finally:
            self._stop(run)
            if run.get("process") and run["process"].stdout:
                run["process"].stdout.close()
            stderr.close()

    def _stop(self, run):
        # Also called by close(), so cleanup is serialized with this worker.
        with self.lock:
            process, job = run.get("process"), run.get("job")
            if process and process.poll() is None:
                if job:
                    job.terminate()
                else:
                    try:
                        os.killpg(process.pid, signal.SIGTERM)
                    except ProcessLookupError:
                        pass
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait(timeout=5)
            if job:
                job.close()
                run["job"] = None

    def next_event(self, timeout=1):
        return self.events.get(timeout=timeout)

    def close(self):
        for run in self.runs:
            self._stop(run)
        for run in self.runs:
            run["worker"].join()
        self.trace.close()
