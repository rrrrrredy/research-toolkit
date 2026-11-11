"""Allowlisted usage events shared by CLI, MCP and usage recording for agent tools.

Research records remain local. This module never uploads a record or exception
verbatim, and never changes the research operation's result.
"""
from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime, timezone
import hashlib
import hmac
import inspect
import json
import os
from pathlib import Path
import platform
import sqlite3
import subprocess
import sys
import time
import uuid
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ENDPOINT = "https://research-toolkit-usage.luosongred.workers.dev"
CONTEXT = ContextVar("research_toolkit_usage", default={})
HOSTS = {"codex", "claude", "opencode", "unknown"}
ENTRIES = {"cli", "mcp", "skill", "plugin", "adapter", "library", "unknown"}
CHANNELS = {"github-clone", "github-release", "plugin-marketplace", "manual", "unknown"}
KINDS = {"installation_seen", "call_started", "call_finished", "record_saved", "work_prepared",
         "review_recorded", "host_execution", "toolkit_activated", "user_turn", "agent_input", "tool_observed",
         "agent_started", "agent_finished", "session_stopped", "session_compacted", "task_linked"}
STATES = {"started", "success", "failed", "blocked", "pending", "saved", "completed", "cancelled",
          "created", "prepared", "error", "waiting", "received", "unknown"}
OPERATIONS = {"start", "status", "guide", "save", "review", "finish", "check-draft", "check-reviewer",
              "check-updates", "host_execution", "prepare_work", "read", "write", "edit", "search",
              "browse", "shell", "skill", "delegate", "other"}
SAFE_ERRORS = {"ValueError", "OSError", "TypeError", "KeyError", "PermissionError", "TimeoutError",
               "RuntimeError", "FileNotFoundError", "ToolError", "other"}
METHODS = {"skill", "research-standard", "research-workflow", "writing-style", "optional-analysis-lenses",
           "subagents-and-review-loop", "quality-gates", "task-continuity", "gotchas", "postmortem-lessons"}


def home():
    return Path(os.environ.get("RESEARCH_TOOLKIT_USAGE_HOME", Path.home()/".research-toolkit"/"usage"))


def disabled_by_environment():
    value = os.environ.get("RESEARCH_TOOLKIT_TELEMETRY", "").lower()
    return value in {"off", "0", "false"} or (bool(os.environ.get("CI")) and value != "on")


@contextmanager
def database():
    folder = home()
    folder.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(folder/"usage.sqlite3", timeout=2)
    connection.row_factory = sqlite3.Row
    try:
        connection.executescript("""
        CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS events (id TEXT PRIMARY KEY, created REAL NOT NULL, payload TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, active INTEGER NOT NULL, task TEXT, parent TEXT);
        CREATE TABLE IF NOT EXISTS aliases (alias TEXT NOT NULL, task TEXT NOT NULL, PRIMARY KEY(alias, task));
        CREATE TABLE IF NOT EXISTS content (id TEXT PRIMARY KEY, created REAL NOT NULL, payload TEXT NOT NULL);
        """)
        for key, value in {"installation_id": uuid.uuid4().hex, "secret": uuid.uuid4().hex+uuid.uuid4().hex,
                           "enabled": "on", "channel": "unknown", "form": "unknown"}.items():
            connection.execute("INSERT OR IGNORE INTO settings VALUES (?,?)", (key, value))
        connection.commit()
        yield connection
        connection.commit()
    finally:
        connection.close()


def settings(db):
    return dict(db.execute("SELECT key,value FROM settings").fetchall())


def set_setting(db, key, value):
    db.execute("INSERT INTO settings VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, str(value)))


def installation_key():
    return "install."+hashlib.sha256(str(ROOT).encode()).hexdigest()+"."


def installation_info(config):
    prefix = installation_key()
    channel = os.environ.get("RESEARCH_TOOLKIT_INSTALL_CHANNEL", config.get(prefix+"channel", "unknown"))
    form = os.environ.get("RESEARCH_TOOLKIT_INSTALL_FORM", config.get(prefix+"form", "unknown"))
    if form == "unknown" and (ROOT/"plugin.json").is_file():
        form = "plugin"
    return {"channel": channel if channel in CHANNELS else "unknown", "form": form if form in ENTRIES else "unknown"}


def opaque(config, kind, value):
    if value is None or value == "":
        return None
    return hmac.new(config["secret"].encode(), (kind+":"+str(value)).encode(), hashlib.sha256).hexdigest()[:32]


def host_name():
    value = os.environ.get("RESEARCH_TOOLKIT_HOST", "")
    if value in HOSTS:
        return value
    if os.environ.get("CLAUDE_CODE_ENTRYPOINT"):
        return "claude"
    if os.environ.get("CODEX_THREAD_ID"):
        return "codex"
    if os.environ.get("OPENCODE"):
        return "opencode"
    return "unknown"


def notice(db, config):
    if config.get("notice") == "1":
        return
    print("Research Toolkit: basic usage events are sent automatically; prompts, reports and file paths "
          "are excluded. Disable: RESEARCH_TOOLKIT_TELEMETRY=off or scripts/usage_events.py off. "
          "Details: docs/usage-data.md", file=sys.stderr)
    set_setting(db, "notice", "1")


def enqueue(db, config, kind, *, task=None, host=None, entry=None, operation=None, outcome=None,
            event_id=None, session=None, parent=None, unit=None, call=None, counts=None,
            elapsed_ms=None, error=None, stage=None, revision=None, method=None):
    if kind not in KINDS:
        return
    stamp = time.time()
    version = (ROOT/"VERSION").read_text(encoding="utf-8").strip()
    payload = {"schema": 1, "id": event_id or uuid.uuid4().hex,
               "at": datetime.fromtimestamp(stamp, timezone.utc).isoformat(),
               "installation": config["installation_id"], "version": version,
               "host": host if host in HOSTS else host_name(),
               "entry": entry if entry in ENTRIES else "library", "kind": kind,
               **installation_info(config),
               "os": {"Windows": "windows", "Darwin": "macos", "Linux": "linux"}.get(platform.system(), "other"),
               "test": os.environ.get("RESEARCH_TOOLKIT_USAGE_TEST") == "1"}
    for key, value in {"task": task, "session": session, "parent": parent, "unit": unit, "call": call}.items():
        if value:
            payload[key] = opaque(config, "session" if key == "parent" else key, value)
    if operation in OPERATIONS:
        payload["operation"] = operation
    if outcome in STATES:
        payload["outcome"] = outcome
    if error:
        payload["error"] = error if error in SAFE_ERRORS else "other"
    if stage in {"brief", "collect", "analyze", "draft", "review", "revise", "final"}:
        payload["stage"] = stage
    if method in METHODS:
        payload["method"] = method
    if isinstance(elapsed_ms, (int, float)) and 0 <= elapsed_ms < 31_536_000_000:
        payload["elapsed_ms"] = round(elapsed_ms, 3)
    if isinstance(revision, str) and len(revision) == 64 and all(c in "0123456789abcdef" for c in revision):
        payload["revision"] = opaque(config, "revision", revision)
    if isinstance(counts, dict):
        selected = {key: value for key, value in counts.items()
                    if key in {"sources", "claims", "requirements", "findings", "dependencies"}
                    and type(value) is int and 0 <= value <= 1_000_000}
        if selected:
            payload["counts"] = selected
    db.execute("INSERT OR IGNORE INTO events VALUES (?,?,?)", (payload["id"], stamp, json.dumps(payload, ensure_ascii=False)))
    db.execute("DELETE FROM events WHERE created < ?", (stamp-7*86400,))
    # Bound the local queue if the receiver remains unavailable.
    db.execute("DELETE FROM events WHERE id IN (SELECT id FROM events ORDER BY created DESC LIMIT -1 OFFSET 10000)")


def failure(exc):
    # Observability failures must be visible locally without leaking an exception's contents.
    print("Research Toolkit usage recording unavailable: "+type(exc).__name__+"; research continues.", file=sys.stderr)


def emit(kind, **fields):
    if disabled_by_environment():
        return
    try:
        with database() as db:
            config = settings(db)
            if config["enabled"] != "on":
                return
            notice(db, config)
            if config.get("seen") != "1":
                enqueue(db, config, "installation_seen", entry=fields.get("entry"))
                set_setting(db, "seen", "1")
            enqueue(db, config, kind, **fields)
        schedule_upload()
    except (OSError, sqlite3.Error, ValueError) as exc:
        failure(exc)


def task_identity(root):
    identity = str(Path(root).resolve())
    # Windows uses this spelling to access long paths, not a different task.
    if identity.startswith('\\\\?\\UNC\\'):
        return '\\\\' + identity[8:]
    if identity.startswith('\\\\?\\'):
        return identity[4:]
    return identity


def remember_task(root):
    if disabled_by_environment():
        return
    try:
        with database() as db:
            if settings(db)["enabled"] == "on":
                db.execute("INSERT OR IGNORE INTO aliases VALUES (?,?)", (Path(root).name, task_identity(root)))
    except (OSError, sqlite3.Error) as exc:
        failure(exc)


def observe_record(root, record):
    context = CONTEXT.get()
    operation = record.get("operation", record.get("record_type"))
    kind = {"save": "record_saved", "prepare_work": "work_prepared", "host_execution": "host_execution",
            "model_review": "review_recorded", "review_audit": "review_recorded",
            "final_acceptance": "review_recorded"}.get(operation)
    if not kind:
        return
    remember_task(root)
    ids = record.get("ids", {})
    counts = {key: len(value) for key, value in ids.items() if isinstance(value, list)} if isinstance(ids, dict) else {}
    if isinstance(record.get("findings"), list):
        counts["findings"] = len(record["findings"])
    if isinstance(record.get("depends_on"), list):
        counts["dependencies"] = len(record["depends_on"])
    emit(kind, task=task_identity(root), entry=context.get("entry", "adapter" if operation == "host_execution" else "library"),
         host=record.get("host"), operation=operation, call=context.get("call"),
         outcome=record.get("outcome", record.get("status", "unknown")), counts=counts,
         unit=record.get("unit_id"), session=record.get("host_task", record.get("execution_id")),
         revision=record.get("artifact_sha256", record.get("draft_sha256")))


def observed_call(function, args, kwargs=None, *, entry):
    kwargs = kwargs or {}
    name = function.__name__
    operation = {"save_records": "save", "guidance": "guide", "check_updates": "check-updates",
                 "check_draft": "check-draft", "review_readiness": "check-reviewer"}.get(name, name)
    bound = inspect.signature(function).bind_partial(*args, **kwargs).arguments
    if name == "_dispatch":
        operation = bound.get("action")
        if isinstance(bound.get("request"), dict):
            bound = {**bound, "task": bound["request"].get("task"), "stage": bound["request"].get("stage")}
    root = Path(bound["workspace"])/bound["task"] if "workspace" in bound and isinstance(bound.get("task"), str) else None
    if root is not None:
        remember_task(root)
    identity = uuid.uuid4().hex
    token = CONTEXT.set({"call": identity, "entry": entry})
    fields = {"task": task_identity(root) if root is not None else None, "entry": entry,
              "operation": operation, "call": identity, "stage": bound.get("stage")}
    started = time.monotonic()
    emit("call_started", **fields, outcome="started")
    try:
        result = function(*args, **kwargs)
    except BaseException as exc:
        # Record every Python exit, including cancellation, then preserve it for
        # the caller. Recording an exit must not turn it into a successful call.
        outcome = "failed" if isinstance(exc, Exception) else "cancelled"
        emit("call_finished", **fields, outcome=outcome, error=type(exc).__name__, elapsed_ms=(time.monotonic()-started)*1000)
        raise
    else:
        outcome = "success"
        if isinstance(result, dict):
            if result.get("action_required"):
                outcome = "pending"
            elif result.get("ok") is False or result.get("completed") is False or result.get("reviews_complete") is False:
                outcome = "blocked"
            elif result.get("completed") is True:
                outcome = "completed"
        emit("call_finished", **fields, outcome=outcome, elapsed_ms=(time.monotonic()-started)*1000)
        return result
    finally:
        CONTEXT.reset(token)


def endpoint(config):
    value = os.environ.get("RESEARCH_TOOLKIT_USAGE_ENDPOINT", config.get("endpoint", DEFAULT_ENDPOINT)).rstrip("/")
    if not value:
        return None
    parsed = urlsplit(value)
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("usage endpoint must be an origin/path without credentials, query or fragment")
    if parsed.scheme != "https" and not (parsed.scheme == "http" and parsed.hostname in {"127.0.0.1", "localhost", "::1"}):
        raise ValueError("usage endpoint must use HTTPS (HTTP is allowed only on loopback)")
    return value


def schedule_upload():
    if os.environ.get("RESEARCH_TOOLKIT_USAGE_AUTOSEND") == "off":
        return
    with database() as db:
        db.execute("BEGIN IMMEDIATE")
        config = settings(db)
        if config["enabled"] != "on" or not endpoint(config) or float(config.get("next_upload", "0")) > time.time():
            return
        set_setting(db, "next_upload", time.time()+30)
    options = {"stdin": subprocess.DEVNULL, "stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL,
               "close_fds": True}
    if os.name == "nt":
        options["creationflags"] = subprocess.CREATE_NO_WINDOW
    else:
        options["start_new_session"] = True
    # Reserve one delayed send for this window. Sending immediately and then
    # ignoring new events for 30 seconds stranded the final batch on exit.
    subprocess.Popen([sys.executable, str(Path(__file__).resolve()), "flush", "--scheduled"], **options)


def request_json(url, data, config, method="POST"):
    body = json.dumps(data, ensure_ascii=False).encode() if data is not None else None
    request = Request(url, data=body, method=method,
                      headers={"Content-Type": "application/json", "User-Agent": "Research-Toolkit-Usage/1",
                               "Authorization": "Bearer "+config["installation_id"]+":"+config["secret"]})
    with urlopen(request, timeout=10) as response:
        return json.loads(response.read(1024*1024))


def flush():
    if disabled_by_environment():
        return {"enabled": False, "sent": 0}
    with database() as db:
        db.execute("BEGIN IMMEDIATE")
        config = settings(db)
        target = endpoint(config)
        if config["enabled"] != "on" or not target:
            return {"enabled": config["enabled"] == "on", "sent": 0, "receiver": bool(target)}
        if float(config.get("sending_until", "0")) > time.time():
            return {"sent": 0, "active_sender": True}
        set_setting(db, "sending_until", time.time()+180)
    sent = 0
    try:
        if config.get("registered_at") != target:
            request_json(target+"/v1/install", {"installation": config["installation_id"]}, config)
            with database() as db:
                set_setting(db, "registered_at", target)
        for _ in range(10):
            with database() as db:
                if settings(db)["enabled"] != "on" or disabled_by_environment():
                    break
                db.execute("DELETE FROM events WHERE created < ?", (time.time()-7*86400,))
                rows = db.execute("SELECT id,payload FROM events ORDER BY created LIMIT 100").fetchall()
            if not rows:
                break
            reply = request_json(target+"/v1/events", {"events": [json.loads(row["payload"]) for row in rows]}, config)
            acknowledged = set(reply.get("accepted_ids", []))
            expected = {row["id"] for row in rows}
            if acknowledged != expected:
                raise ValueError("receiver did not acknowledge the complete batch")
            with database() as db:
                db.executemany("DELETE FROM events WHERE id=?", ((identity,) for identity in acknowledged))
            sent += len(rows)
        with database() as db:
            db.execute("DELETE FROM content WHERE created < ?", (time.time()-7*86400,))
            shared = db.execute("SELECT id,payload FROM content ORDER BY created LIMIT 5").fetchall() if settings(db)["enabled"] == "on" else []
        for row in shared:
            if disabled_by_environment():
                break
            with database() as db:
                if settings(db)["enabled"] != "on":
                    break
                if not db.execute("SELECT 1 FROM content WHERE id=?", (row["id"],)).fetchone():
                    continue  # A user withdrew this project grant after the batch was read.
            reply = request_json(target+"/v1/content", json.loads(row["payload"]), config)
            if reply.get("id") != row["id"]:
                raise ValueError("receiver did not acknowledge shared content")
            with database() as db:
                db.execute("DELETE FROM content WHERE id=?", (row["id"],))
        with database() as db:
            set_setting(db, "last_upload", datetime.now(timezone.utc).isoformat())
            set_setting(db, "last_error", "")
        return {"sent": sent, "receiver": True}
    except (HTTPError, URLError, TimeoutError, OSError, ValueError) as exc:
        with database() as db:
            set_setting(db, "last_error", "HTTP "+str(exc.code) if isinstance(exc, HTTPError) else type(exc).__name__)
        return {"sent": sent, "pending": True, "error": "HTTP "+str(exc.code) if isinstance(exc, HTTPError) else type(exc).__name__}
    finally:
        with database() as db:
            set_setting(db, "sending_until", "0")


def sharing_key(project):
    return "content." + hashlib.sha256(task_identity(project).encode()).hexdigest()


def queue_content(db, config, root, paths):
    """Queue only the selected UTF-8 files, through the existing content receiver."""
    root = Path(task_identity(root))
    if config["enabled"] != "on" or disabled_by_environment():
        raise ValueError("usage sharing is disabled; enable it explicitly first")
    files = []
    for index, path in enumerate(paths):
        source = (root / path).resolve()
        relative = source.relative_to(root)
        if any(part in {".git", ".env", "credentials", "auth.json"} for part in relative.parts):
            raise ValueError("credential/configuration files cannot be shared")
        if source.stat().st_size > 1024 * 1024:
            raise ValueError("selected files must each be at most 1 MiB")
        files.append({"name": f"file-{index+1}.txt", "text": source.read_text(encoding="utf-8")})
    if not files:
        raise ValueError("select at least one file")
    packet = {"id": uuid.uuid4().hex, "task": opaque(config, "task", task_identity(root)),
              "consent": True, "files": files, "at": datetime.now(timezone.utc).isoformat()}
    if len(json.dumps(packet).encode()) > 1_900_000:
        raise ValueError("selected content packet exceeds 1,900,000 bytes")
    db.execute("INSERT INTO content VALUES (?,?,?)", (packet["id"], time.time(), json.dumps(packet)))
    return {"queued": packet["id"], "files": len(files)}


def content_offer(root, artifact, project=None, language="en"):
    """Offer once after delivery, or queue reports within an explicit project grant."""
    root = Path(task_identity(root))
    project = Path(task_identity(project)) if project else root.parent
    root.relative_to(project)
    artifact = (root / artifact).resolve().relative_to(root).as_posix()
    with database() as db:
        config = settings(db)
        if config["enabled"] != "on" or disabled_by_environment():
            return {"status": "disabled"}
        key = sharing_key(project)
        choice = config.get(key, "ask")
        if choice == "reports":
            checksum = hashlib.sha256((root / artifact).read_bytes()).hexdigest()
            sent_key = key + ".report." + hashlib.sha256(task_identity(root / artifact).encode()).hexdigest()
            if config.get(sent_key) == checksum:
                return {"status": "already_queued"}
            result = {"status": "queued", **queue_content(db, config, root, [artifact])}
            set_setting(db, sent_key, checksum)
            task_id = opaque(config, "task", task_identity(root))
            set_setting(db, key + ".task." + task_id, task_id)
        elif choice != "ask":
            return {"status": choice}
        else:
            recipient = "rrrrrredy/research-toolkit-usage (private)"
            prompt = (f"报告已交付。愿意将 {artifact} 分享给 Research Toolkit 维护者，"
                      f"用于改进研究方法和产品吗？文件会发送到私密仓库 {recipient}。"
                      "本次不包含聊天记录或原始材料。可选择：仅分享这次报告；"
                      f"允许今后自动分享本项目（{project}）的最终报告；不分享并不再提示。"
                      "未回复不会上传，也不影响报告使用。以后可随时关闭。"
                      if language in {"zh", "zh-CN"} else
                      f"Your report is ready. May we share {artifact} with the Research Toolkit maintainer "
                      f"in {recipient} to improve research methods and the product? Chat and source materials "
                      "are excluded. Choose: share this report once; automatically share future final reports "
                      f"in this project ({project}); or decline and stop asking. No reply means no upload. "
                      "Your report remains available; you can turn sharing off later.")
            result = {"status": "ask", "prompt": prompt, "files": [artifact],
                      "recipient": recipient, "project_root": str(project), "task_root": str(root),
                      "choices": ["once", "reports", "decline"]}
            set_setting(db, key, "offered")
    if result["status"] == "queued":
        schedule_upload()
    return result


def delivery_sharing(root, artifact, language="en"):
    # Sharing is separate from research completion. Keep a local storage failure
    # visible without changing a successful delivery into a research failure.
    try:
        return content_offer(root, artifact, language=language)
    except (OSError, ValueError, sqlite3.Error) as exc:
        return {"status": "error", "error": type(exc).__name__, "next_action": "Report delivered; retry content sharing separately."}


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["status", "on", "off", "flush", "delete", "share", "share-offer"])
    parser.add_argument("--task-root", type=Path)
    parser.add_argument("--project-root", type=Path, help="Project whose final reports the user authorized; defaults to task parent")
    parser.add_argument("--file", type=Path, action="append", default=[])
    parser.add_argument("--decision", choices=["once", "reports", "decline", "ask"], default="once")
    parser.add_argument("--language", choices=["en", "zh", "zh-CN"], default="en")
    parser.add_argument("--confirm-content", action="store_true", help="The user explicitly authorized sharing these selected files")
    parser.add_argument("--scheduled", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.action == "share-offer":
        if not args.task_root or len(args.file) != 1:
            parser.error("share-offer needs --task-root and one delivered report --file")
        print(json.dumps(content_offer(args.task_root, args.file[0], args.project_root, args.language), ensure_ascii=False))
        return
    if args.action == "flush":
        if args.scheduled:
            time.sleep(30)
        result = flush()
        print(json.dumps(result))
        if args.scheduled and result.get("receiver") and not result.get("pending"):
            with database() as db:
                remaining = db.execute("SELECT count(*) FROM events").fetchone()[0] + db.execute("SELECT count(*) FROM content").fetchone()[0]
            if remaining:
                schedule_upload()
        return
    with database() as db:
        config = settings(db)
        if args.action in {"off", "on"}:
            set_setting(db, "enabled", args.action)
            if args.action == "off":
                db.execute("DELETE FROM events")
                db.execute("DELETE FROM content")
                db.execute("DELETE FROM sessions")
            print(json.dumps({"enabled": args.action == "on", "queued_cleared": args.action == "off"}))
        elif args.action == "status":
            print(json.dumps({"enabled": config["enabled"] == "on" and not disabled_by_environment(),
                              "installation": config["installation_id"], "receiver": endpoint(config),
                              **installation_info(config),
                              "pending_events": db.execute("SELECT count(*) FROM events").fetchone()[0],
                              "pending_content": db.execute("SELECT count(*) FROM content").fetchone()[0],
                              "last_upload": config.get("last_upload"), "last_error": config.get("last_error")}))
        elif args.action == "share":
            if not args.task_root:
                parser.error("share requires --task-root")
            root = Path(task_identity(args.task_root))
            project = Path(task_identity(args.project_root)) if args.project_root else root.parent
            root.relative_to(project)
            key = sharing_key(project)
            if args.decision in {"decline", "ask"}:
                # Revoke pending content across this project, including reports
                # queued before the user withdrew authorization.
                for row in db.execute("SELECT key,value FROM settings WHERE key LIKE ?", (key + ".task.%",)).fetchall():
                    matching = [(item["id"],) for item in db.execute("SELECT id,payload FROM content")
                                if json.loads(item["payload"]).get("task") == row["value"]]
                    db.executemany("DELETE FROM content WHERE id=?", matching)
                set_setting(db, key, args.decision)
                print(json.dumps({"decision": args.decision, "project_root": str(project)}))
            else:
                if not args.confirm_content or not args.file:
                    parser.error("share requires selected --file paths and --confirm-content after the user's agreement")
                if args.decision == "reports" and len(args.file) != 1:
                    parser.error("reports authorizes final reports only; use once for separately selected chat or source files")
                result = queue_content(db, config, root, args.file)
                set_setting(db, key, args.decision)
                task_id = opaque(config, "task", task_identity(root))
                set_setting(db, key + ".task." + task_id, task_id)
                if args.decision == "reports":
                    source = (root / args.file[0]).resolve()
                    sent_key = key + ".report." + hashlib.sha256(task_identity(source).encode()).hexdigest()
                    set_setting(db, sent_key, hashlib.sha256(source.read_bytes()).hexdigest())
                print(json.dumps(result))
        elif args.action == "delete":
            target = endpoint(config)
            if not target:
                parser.error("no receiver configured")
            data = {"task": opaque(config, "task", task_identity(args.task_root))} if args.task_root else {}
            print(json.dumps(request_json(target+"/v1/delete", data, config)))
            for table in ("content", "events"):
                if data:
                    matching = [(row["id"],) for row in db.execute(f"SELECT id,payload FROM {table}")
                                if json.loads(row["payload"]).get("task") == data["task"]]
                    db.executemany(f"DELETE FROM {table} WHERE id=?", matching)
                else:
                    db.execute(f"DELETE FROM {table}")
    if args.action == "share":
        schedule_upload()


if __name__ == "__main__":
    main()
