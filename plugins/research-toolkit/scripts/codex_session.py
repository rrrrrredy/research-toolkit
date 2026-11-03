"""Small stdio client for the installed Codex host; no model or account overrides."""
from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import sys
import threading

from review_process import WindowsJob, WINDOWS_GATE


class CodexSession:
    """Keep native threads and their original events, using the host's login/config."""

    def __init__(self, cwd: Path, directory: Path):
        self.cwd = cwd.resolve()
        directory.mkdir(parents=True, exist_ok=True)
        self.events = queue.Queue()
        self.pending = {}
        self.mutex = threading.Lock()
        self.next_id = 0
        self.closed = False
        self.trace = (directory / "protocol.jsonl").open("a", encoding="utf-8")
        self.stderr = (directory / "stderr.txt").open("a", encoding="utf-8")
        self.job = None
        self.process = None
        executable = shutil.which("codex.exe") or shutil.which("codex")
        if not executable:
            self.close()
            raise OSError("Codex executable not found. Use the installed host's native agents, or add Codex to PATH.")
        command = [executable, "app-server", "--listen", "stdio://"]
        try:
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
        self.trace.write(json.dumps({"at": datetime.now(timezone.utc).isoformat(),
            "direction": direction, "message": message}, ensure_ascii=False) + "\n")
        self.trace.flush()

    def send(self, message):
        with self.mutex:
            self._record("send", message)
            self.process.stdin.write(json.dumps(message, ensure_ascii=False) + "\n")
            self.process.stdin.flush()

    def _read(self):
        try:
            for line in self.process.stdout:
                message = json.loads(line)
                with self.mutex:
                    self._record("receive", message)
                    waiter = self.pending.get(message.get("id")) if "method" not in message else None
                if waiter is not None:
                    waiter.put(message)
                else:
                    self.events.put(message)
        except (OSError, ValueError) as exc:
            self.events.put({"method": "transport/error", "params": {"error": str(exc)}})
        finally:
            with self.mutex:
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
                raise RuntimeError(f"{method}: {reply['error']}")
            return reply["result"]
        except queue.Empty as exc:
            raise RuntimeError(f"{method}: Codex did not acknowledge the request; inspect the retained protocol.") from exc
        finally:
            with self.mutex:
                self.pending.pop(identity, None)

    def thread(self, previous=None):
        params = {"cwd": str(self.cwd), "sandbox": "read-only", "approvalPolicy": "never"}
        if previous:
            params.update(threadId=previous, excludeTurns=True)
            return self.request("thread/resume", params)["thread"]["id"]
        params.update(ephemeral=False, serviceName="research-toolkit")
        return self.request("thread/start", params)["thread"]["id"]

    def turn(self, thread, prompt):
        return self.request("turn/start", {"threadId": thread,
            "input": [{"type": "text", "text": prompt}]})["turn"]["id"]

    def steer(self, thread, turn, prompt):
        return self.request("turn/steer", {"threadId": thread, "expectedTurnId": turn,
            "input": [{"type": "text", "text": prompt}]})

    def close(self):
        if self.closed:
            return
        self.closed = True
        if self.process:
            try:
                self.process.stdin.close()
                self.process.wait(timeout=5)
            except (OSError, subprocess.TimeoutExpired):
                if self.job:
                    self.job.terminate()
                elif self.process.poll() is None:
                    import signal
                    os.killpg(self.process.pid, signal.SIGKILL)
                self.process.wait(timeout=5)
            if hasattr(self, "reader"):
                self.reader.join(timeout=5)
        if self.job:
            self.job.close()
        self.trace.close()
        self.stderr.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
