"""Small stdio client for the installed Codex agent tool; no model or account overrides."""
from __future__ import annotations

from contextlib import ExitStack
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import sys
import threading

from agent_session import PROCESS_EXIT_TIMEOUT, stop_native_process
from review_process import ProcessCleanupError, WindowsJob, WINDOWS_GATE


class CodexRequestError(RuntimeError):
    def __init__(self, method, error):
        super().__init__(f"{method}: {error}")
        self.method, self.error = method, error


class CodexSession:
    """Keep native threads and their original events, using the agent tool's login/config."""

    def __init__(self, cwd: Path, directory: Path, command=None):
        self.cwd = cwd.resolve()
        directory.mkdir(parents=True, exist_ok=True)
        self.events = queue.Queue()
        self.pending = {}
        self.mutex = threading.Lock()
        self.writer = threading.Lock()
        self.next_id = 0
        self.closed = False
        self.disconnected = False
        self.logs = ExitStack()
        self.job = None
        self.process = None
        try:
            self.trace = self.logs.enter_context((directory / "protocol.jsonl").open("a", encoding="utf-8"))
            self.stderr = self.logs.enter_context((directory / "stderr.txt").open("a", encoding="utf-8"))
            executable = command or [shutil.which("codex.exe") or shutil.which("codex")]
            if not executable[0]:
                raise OSError("Codex executable not found. Use the installed agent tool's native agents, or add Codex to PATH.")
            command = executable + ["app-server", "--listen", "stdio://"]
            self.job = WindowsJob() if os.name == "nt" else None
            argv = ([sys.executable, "-c", WINDOWS_GATE, json.dumps(command)] if self.job else command)
            self.process = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=self.stderr, cwd=self.cwd, text=True, encoding="utf-8", bufsize=1,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
                start_new_session=os.name != "nt")
            if self.job:
                self.job.attach(self.process.pid)
                self.process.stdin.write("1")
                self.process.stdin.flush()
            self.reader = threading.Thread(target=self._read, daemon=True)
            self.reader.start()
            self.request("initialize", {"clientInfo": {"name": "research_toolkit",
                "title": "Research Toolkit", "version": "1"}})
            self.send({"method": "initialized", "params": {}})
        except BaseException:
            self.close()
            raise

    def _record(self, direction, message):
        if self.trace.closed:  # The reader can outlive failed process cleanup.
            return
        self.trace.write(json.dumps({"at": datetime.now(timezone.utc).isoformat(),
            "direction": direction, "message": message}, ensure_ascii=False) + "\n")
        self.trace.flush()

    def send(self, message):
        with self.writer:
            with self.mutex:
                if self.disconnected or self.closed:
                    raise RuntimeError("Codex app-server disconnected; original events retained.")
                self._record("send", message)
            try:
                self.process.stdin.write(json.dumps(message, ensure_ascii=False) + "\n")
                self.process.stdin.flush()
            except OSError as exc:
                raise RuntimeError(f"Codex app-server stopped accepting requests; see {self.trace.name}.") from exc

    def _read(self):
        try:
            for line in self.process.stdout:
                message = json.loads(line)
                with self.mutex:
                    self._record("receive", message)
                    if not isinstance(message, dict):
                        raise ValueError("Codex protocol event must be a JSON object.")
                    waiter = self.pending.get(message.get("id")) if "method" not in message else None
                if waiter is not None:
                    waiter.put(message)
                else:
                    self.events.put(message)
        except (OSError, ValueError) as exc:
            self.events.put({"method": "transport/error", "params": {"error": str(exc)}})
        finally:
            self.process.stdout.close()
            with self.mutex:
                self.disconnected = True
                for waiter in self.pending.values():
                    waiter.put({"error": {"message": "Codex app-server disconnected; original events retained."}})
            self.events.put({"method": "transport/closed", "params": {}})

    def request(self, method, params):
        with self.mutex:
            self.next_id += 1
            identity = self.next_id
            waiter = self.pending[identity] = queue.Queue()
        try:
            self.send({"id": identity, "method": method, "params": params})
            # This is a transport-response deadline, not a limit on a research turn.
            reply = waiter.get(timeout=60)
            if "error" in reply:
                raise CodexRequestError(method, reply["error"])
            return reply["result"]
        except queue.Empty as exc:
            raise RuntimeError(f"{method}: Codex did not acknowledge the request within 60 seconds; see {self.trace.name}.") from exc
        finally:
            with self.mutex:
                self.pending.pop(identity, None)

    def thread(self, previous=None, cwd=None):
        # Use the installed tool's permissions and model. The caller supplies a
        # separate working directory for each contribution/review invocation.
        params = {"cwd": str(cwd or self.cwd)}
        if previous:
            params.update(threadId=previous, excludeTurns=True)
            return self.request("thread/resume", params)["thread"]["id"]
        params.update(ephemeral=False, serviceName="research-toolkit")
        return self.request("thread/start", params)["thread"]["id"]

    def turn(self, thread, prompt, cwd=None):
        params = {"threadId": thread, "input": [{"type": "text", "text": prompt}]}
        if cwd is not None:
            # Research needs downloads and executable calculations. Keep writes
            # inside this invocation; approval/admin policy is still inherited.
            params.update(cwd=str(cwd), sandboxPolicy={"type": "workspaceWrite",
                          "writableRoots": [str(cwd)], "networkAccess": True})
        return self.request("turn/start", params)["turn"]["id"]

    def steer(self, thread, turn, prompt):
        return self.request("turn/steer", {"threadId": thread, "expectedTurnId": turn,
            "input": [{"type": "text", "text": prompt}]})

    def close(self):
        with self.mutex:
            if self.closed:
                return
            self.closed = True
        try:
            if self.process:
                try:
                    self.process.stdin.close()
                    self.process.wait(timeout=PROCESS_EXIT_TIMEOUT)
                except (OSError, subprocess.TimeoutExpired):
                    # Stop the process tree below even when orderly EOF fails.
                    pass
            stop_native_process(self.process, self.job)
            if hasattr(self, "reader"):
                self.reader.join(timeout=PROCESS_EXIT_TIMEOUT)
                if self.reader.is_alive():
                    raise ProcessCleanupError(f"Codex protocol reader did not close; see {self.trace.name}.")
        finally:
            try:
                if self.process and (not hasattr(self, "reader") or not self.reader.is_alive()):
                    self.process.stdout.close()
            finally:
                with self.mutex:
                    self.logs.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
