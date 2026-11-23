#!/usr/bin/env python3
"""Exercise usage and sharing CLIs against an isolated loopback receiver."""
from __future__ import annotations

from contextlib import closing
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
from threading import Thread
from usage_events import check_shared_file


SCRIPTS = Path(__file__).resolve().parent


def verify(workspace, endpoint, received):
    usage = workspace / "usage"
    env = {**os.environ, "RESEARCH_TOOLKIT_USAGE_HOME": str(usage),
           "RESEARCH_TOOLKIT_TELEMETRY": "on", "RESEARCH_TOOLKIT_USAGE_AUTOSEND": "off",
           "RESEARCH_TOOLKIT_USAGE_TEST": "1", "RESEARCH_TOOLKIT_USAGE_ENDPOINT": endpoint}

    def run(script, *args, environment=env):
        result = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS / script), *map(str, args)],
                                env=environment, capture_output=True, text=True, encoding="utf-8", timeout=15)
        if result.returncode:
            raise RuntimeError(f"{script} exited {result.returncode}: {result.stderr}")
        return json.loads(result.stdout)

    def usage_command(*args, environment=env):
        return run("usage_events.py", *args, environment=environment)

    def check_inactive_hook():
        result = subprocess.run([sys.executable, str(SCRIPTS / "usage_host.py"), "--host", "codex"],
                                input=b"malformed hook payload", env=env, capture_output=True, timeout=15, check=True)
        assert not result.stdout and not result.stderr

    def deliver(task, report):
        task.mkdir(parents=True, exist_ok=True)
        (task / "final.md").write_text(report + "\n", encoding="utf-8")
        return usage_command("share-offer", "--task-root", task, "--file", "final.md")

    project = workspace / "project"
    alpha = project / "alpha"
    first = alpha / "first"
    second = alpha / "second"
    other = project / "beta" / "other"
    once = workspace / "once"
    disabled = usage_command("share-offer", "--task-root", first, "--file", "final.md",
                             environment={**env, "RESEARCH_TOOLKIT_TELEMETRY": "off"})
    assert disabled == {"status": "disabled"} and not usage.exists() and not received

    install_args = ("--host", "codex", "--project", project, "--channel", "manual")
    fresh = usage_command("status")
    assert fresh["enabled"] is False and fresh["pending_events"] == 0
    inactive = run("install_usage.py", *install_args)
    assert not inactive["configuration_changed"] and "usage_notice" not in inactive
    check_inactive_hook()
    assert not (project / ".codex").exists() and not usage.exists() and not received
    hook = json.loads((SCRIPTS.parent / "hooks/hooks.json").read_text(encoding="utf-8"))["hooks"]["Stop"][0]["hooks"][0]
    hook_env = {k: v for k, v in env.items() if k not in ("PLUGIN_ROOT", "CLAUDE_PLUGIN_ROOT", "CODEX_PLUGIN_ROOT")}
    hook_env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env["PATH"]
    command = hook["commandWindows"] if os.name == "nt" else hook["command"]
    for root_env in ({}, {"PLUGIN_ROOT": str(workspace)}, {"PLUGIN_ROOT": str(SCRIPTS.parent)}):
        quiet = subprocess.run(command, shell=True, cwd=workspace, env={**hook_env, **root_env},
                               input=b"{}", capture_output=True, timeout=10)
        assert (quiet.returncode, quiet.stdout, quiet.stderr) == (0, b"", b""), quiet

    check_shared_file(Path("fields.md"), "字段要求：api_key: required\n工作目录（pwd: /workspace/app）")
    for assignment in ("password: required", "pwd: /workspace/app", "api_key: short"):
        try:
            check_shared_file(Path("settings.md"), assignment)
        except ValueError:
            pass
        else:
            raise AssertionError("A bare credential assignment was accepted")

    usage_command("on")
    installed = run("install_usage.py", *install_args)
    assert installed["configuration_changed"] and installed["usage_notice"]["receiver"] == endpoint
    reused = run("install_usage.py", *install_args)
    assert not reused["configuration_changed"] and "usage_notice" not in reused
    assert usage_command("flush")["sent"] == 1
    event, = [event for route, packet in received if route == "/v1/events" for event in packet["events"]]
    assert event["kind"] == "installation_seen" and event["test"] is True

    def content_received():
        return [item["files"][0]["text"].strip() for route, item in received if route == "/v1/content"]

    offer = deliver(once, "One report authorized for a single share.")
    assert offer["status"] == "ask" and Path(offer["project_root"]) == once
    assert deliver(once, "One report authorized for a single share.")["status"] == "offered"
    usage_command("flush")
    assert not content_received()
    usage_command("share", "--task-root", once, "--file", "final.md", "--confirm-content")
    usage_command("flush")
    assert content_received() == ["One report authorized for a single share."]
    assert deliver(second, "A separate unanswered invitation.")["status"] == "ask"

    assert deliver(first, "A report queued under the project grant.")["status"] == "ask"
    usage_command("share", "--task-root", first, "--project-root", project,
                  "--decision", "reports", "--file", "final.md", "--confirm-content")
    assert deliver(first, "A report queued under the project grant.")["status"] == "already_queued"
    assert deliver(second, "A second report under the project grant.")["status"] == "queued"
    assert deliver(other, "A report in the sibling directory.")["status"] == "queued"
    usage_command("off")
    assert usage_command("status")["enabled"] is False
    check_inactive_hook()
    preserved = run("install_usage.py", *install_args)
    assert not preserved["configuration_changed"] and "usage_notice" not in preserved
    assert usage_command("status")["pending_content"] == 3

    usage_command("share", "--task-root", first, "--project-root", alpha, "--decision", "decline")
    assert usage_command("status")["pending_content"] == 1
    assert deliver(second, "A later report in the declined scope.")["status"] == "decline"
    usage_command("flush")
    assert content_received() == ["One report authorized for a single share.", "A report in the sibling directory."]

    assert deliver(other, "A new sibling report awaiting transfer.")["status"] == "queued"
    usage_command("share", "--task-root", other, "--project-root", project, "--decision", "ask")
    assert usage_command("status")["pending_content"] == 0
    assert deliver(other, "A new sibling report awaiting transfer.")["status"] == "ask"
    usage_command("flush")
    assert len(content_received()) == 2

    # Model a pre-upgrade saved off with a dormant, previously confirmed grant.
    usage_command("share", "--task-root", other, "--project-root", project,
                  "--decision", "reports", "--file", "final.md", "--confirm-content")
    with closing(sqlite3.connect(usage / "usage.sqlite3")) as db, db:
        db.execute("PRAGMA foreign_keys = ON")
        db.execute("DELETE FROM settings WHERE key='legacy_sharing_paused' OR key LIKE '%.sharing_resumed'")
        db.execute("DELETE FROM content")
    assert deliver(other, "A report in a legacy paused scope.") == {"status": "disabled"}
    usage_command("share", "--task-root", other, "--file", "final.md", "--confirm-content")
    usage_command("flush")
    assert content_received()[-1] == "A report in a legacy paused scope."
    assert deliver(other, "An unchanged old authorization cannot auto-share.") == {"status": "disabled"}
    usage_command("share", "--task-root", other, "--project-root", project,
                  "--decision", "reports", "--file", "final.md", "--confirm-content")
    assert deliver(other, "A report with an explicitly renewed grant.")["status"] == "queued"
    usage_command("flush")
    assert content_received()[-1] == "A report with an explicitly renewed grant."
    assert sum(len(packet["events"]) for route, packet in received if route == "/v1/events") == 1

    # Old stores keep the parent ID unqualified, even when two hosts used it.
    usage_command("on")
    with closing(sqlite3.connect(usage / "usage.sqlite3")) as db, db:
        for host in ("codex", "claude"):
            db.execute("INSERT INTO sessions VALUES (?,1,NULL,NULL)", (host + ":shared",))
            db.execute("INSERT INTO sessions VALUES (?,1,NULL,'shared')", (host + ":child",))
    subprocess.run([sys.executable, str(SCRIPTS / "usage_host.py"), "--host", "codex"], env=env,
                   input=b'{"hook_event_name":"SessionEnd","session_id":"shared"}', capture_output=True, check=True)
    with closing(sqlite3.connect(usage / "usage.sqlite3")) as db:
        states = dict(db.execute("SELECT id,active FROM sessions"))
        assert states["claude:child"] and states["claude:shared"]
        assert not states["codex:child"] and not states["codex:shared"]


def main():
    received = []

    class Receiver(BaseHTTPRequestHandler):
        def do_POST(self):
            packet = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            received.append((self.path, packet))
            if self.path == "/v1/events":
                response = {"accepted_ids": [event["id"] for event in packet["events"]]}
            elif self.path == "/v1/content":
                response = {"id": packet["id"]}
            else:
                assert self.path == "/v1/install"
                response = {}
            body = json.dumps(response).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *_args):
            pass

    with tempfile.TemporaryDirectory(prefix="toolkit-usage-") as temporary:
        with ThreadingHTTPServer(("127.0.0.1", 0), Receiver) as server:
            thread = Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                verify(Path(temporary).resolve(), f"http://127.0.0.1:{server.server_port}", received)
            finally:
                server.shutdown()
                thread.join()
    print("PASS: opt-in metadata and hooks, independent content consent, legacy pause, scope precedence and withdrawal over loopback.")


if __name__ == "__main__":
    main()
