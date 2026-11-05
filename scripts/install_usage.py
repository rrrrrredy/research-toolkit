"""Configure Toolkit usage recording in Codex, Claude Code or OpenCode."""
from __future__ import annotations
import argparse
import base64
import json
import os
from pathlib import Path
import sys
import time

import usage_events as usage

EVENTS = ["UserPromptSubmit", "PreToolUse", "PostToolUse", "SubagentStart", "SubagentStop", "Stop", "SessionEnd", "PreCompact"]


def write_changed(path, text):
    if path.exists():
        before = path.read_text(encoding="utf-8")
        if before == text:
            return
        backup = path.with_name(path.name+".toolkit-backup-"+str(time.time_ns()))
        backup.write_text(before, encoding="utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def install(host, project, remove=False):
    script = Path(__file__).resolve().with_name("usage_host.py")
    # Quote POSIX paths; Windows uses the explicit PowerShell launcher below.
    # Refuse expansion metacharacters rather than interpolate them.
    paths = [Path(sys.executable).as_posix(), script.as_posix()]
    if any(any(char in item for char in ['"', '$', '`', '%', '\n', '\r']) for item in paths):
        raise ValueError("Install path contains shell metacharacters; use a plain directory path")
    command = f'"{paths[0]}" "{paths[1]}" --host {host}'
    previous_command = command
    if os.name == "nt":
        # Avoid cmd's special treatment of a quoted first token and PowerShell's
        # need for a call operator. Explicit UTF-8 also preserves hook JSON.
        quoted = ["'"+value.replace("'", "''")+"'" for value in paths]
        script_text = ("$OutputEncoding = [System.Text.UTF8Encoding]::new(); "
                       "[Console]::InputEncoding = $OutputEncoding; "
                       f"[Console]::In.ReadToEnd() | & {quoted[0]} {quoted[1]} --host {host}; exit $LASTEXITCODE")
        command = "powershell.exe -NoProfile -NonInteractive -EncodedCommand "+base64.b64encode(script_text.encode("utf-16le")).decode()
    if host == "opencode":
        path = project/".opencode/plugins/research-toolkit-usage.js"
        if path.exists() and "research-toolkit usage observer" not in path.read_text(encoding="utf-8"):
            raise ValueError("Existing OpenCode plugin file is not managed by Toolkit; preserved")
        if remove:
            if path.exists():
                path.unlink()
        else:
            module = script.with_name("usage_opencode.mjs").as_uri()
            write_changed(path, "// research-toolkit usage observer\nimport { createUsagePlugin } from "+json.dumps(module)+";\nexport default createUsagePlugin("+json.dumps(sys.executable)+");\n")
        return path
    path = project/(".codex/hooks.json" if host == "codex" else ".claude/settings.local.json")
    config = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    if not isinstance(config, dict) or not isinstance(config.get("hooks", {}), dict):
        raise ValueError("Existing agent tool hooks configuration is not an object; preserved")
    groups = config.setdefault("hooks", {})
    for event in EVENTS + (["PostToolUseFailure"] if host == "claude" else []):
        existing = groups.get(event, [])
        if not isinstance(existing, list):
            raise ValueError(f"hooks.{event} must be an array; existing file preserved")
        kept = []
        for group in existing:
            if not isinstance(group, dict) or not isinstance(group.get("hooks", []), list):
                raise ValueError(f"hooks.{event} contains an invalid group; existing file preserved")
            handlers = group.get("hooks", [])
            if any(not isinstance(handler, dict) for handler in handlers):
                raise ValueError(f"hooks.{event} contains an invalid handler; existing file preserved")
            remaining = [handler for handler in handlers if handler.get("command") not in {command, previous_command}]
            if remaining or not handlers:
                kept.append({**group, "hooks": remaining})
        if not remove:
            kept.append({"hooks": [{"type": "command", "command": command, "timeout": 3}]})
        if kept:
            groups[event] = kept
        else:
            groups.pop(event, None)
    write_changed(path, json.dumps(config, ensure_ascii=False, indent=2)+"\n")
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", required=True, choices=["codex", "claude", "opencode"])
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--channel", choices=sorted(usage.CHANNELS), default="manual")
    parser.add_argument("--form", choices=["skill", "plugin", "cli", "mcp"], default="skill")
    parser.add_argument("--remove", action="store_true")
    args = parser.parse_args()
    path = install(args.host, args.project.resolve(), args.remove)
    next_step = "Only Toolkit usage recording configuration was removed."
    if not args.remove:
        first_installation = False
        with usage.database() as db:
            usage.set_setting(db, usage.installation_key()+"channel", args.channel)
            usage.set_setting(db, usage.installation_key()+"form", args.form)
            config = usage.settings(db)
            enabled = config["enabled"] == "on" and not usage.disabled_by_environment()
            if enabled:
                usage.notice(db, config)
                if config.get("seen") != "1":
                    usage.enqueue(db, config, "installation_seen", host=args.host, entry=args.form)
                    usage.set_setting(db, "seen", "1")
                    first_installation = True
        if enabled:
            usage.schedule_upload()
        reload_instruction = ("Reload or reopen the Codex session to load this configuration."
                              if args.host == "codex" else
                              "Follow the application's trust or reload instructions to load this configuration.")
        next_step = ("Usage recording is configured. " +
                     ("The installation event is queued. " if first_installation else "") + reload_instruction
                     if enabled else "Usage recording remains off; the existing off setting was preserved.")
    print(json.dumps({"host": args.host, "path": str(path), "removed": args.remove,
                      "next": next_step}))


if __name__ == "__main__":
    main()
