#!/usr/bin/env python3
"""Fresh, tool-disabled Codex judge transport. CLI model identity is requested only."""
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time

KEYS = {"transport", "model", "snapshot_statement", "executable_env", "reasoning_effort",
        "max_completion_tokens", "max_total_tokens", "timeout_seconds", "output_protocol", "allow_json_fence"}
DISABLED = ("apps", "plugins", "remote_plugin", "memories", "multi_agent", "multi_agent_v2",
            "shell_tool", "unified_exec", "view_image", "image_generation", "browser_use",
            "browser_use_external", "computer_use", "hooks", "skill_search", "skill_mcp_dependency_install",
            "workspace_dependencies", "goals", "tool_suggest", "in_app_browser", "unbounded_connection_retries")
ENVIRONMENT = {"PATH", "SYSTEMROOT", "WINDIR", "COMSPEC", "PATHEXT", "TEMP", "TMP", "USERPROFILE",
               "HOMEDRIVE", "HOMEPATH", "HOME", "APPDATA", "LOCALAPPDATA", "PROGRAMDATA",
               "PROGRAMFILES", "PROGRAMFILES(X86)", "OS"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(settings):
    require(isinstance(settings, dict) and set(settings) == KEYS, "Unknown/missing Codex judge setting")
    require(settings["transport"] == "codex_exec", "Expected codex_exec transport")
    for field in ("model", "snapshot_statement"):
        require(isinstance(settings[field], str) and settings[field].strip(), f"Declare {field}")
    require(isinstance(settings["executable_env"], str) and re.fullmatch(r"[A-Z_][A-Z0-9_]*", settings["executable_env"]),
            "Use an environment-variable name for the CLI executable")
    require(settings["reasoning_effort"] in {"low", "medium", "high", "xhigh", "max"}, "Declare reasoning effort")
    for field in ("max_completion_tokens", "max_total_tokens", "timeout_seconds"):
        require(type(settings[field]) is int and settings[field] > 0, f"Set positive {field}")
    require(settings["max_total_tokens"] >= settings["max_completion_tokens"], "Total ceiling must cover output ceiling")
    require(settings["output_protocol"] == "json_object_v1" and type(settings["allow_json_fence"]) is bool,
            "Declare JSON judge parsing")


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as file:
        json.dump(value, file, ensure_ascii=False, indent=2)
        file.write("\n")


def command(executable, workspace, instruction, settings):
    args = [str(executable), "exec", "--ignore-user-config", "--ephemeral", "--skip-git-repo-check",
            "--sandbox", "read-only", "--json", "--color", "never", "--model", settings["model"], "--cd", str(workspace)]
    for feature in DISABLED:
        args += ["--disable", feature]
    config = {"model_reasoning_effort": settings["reasoning_effort"], "model_instructions_file": str(instruction),
              "web_search": "disabled", "project_doc_max_bytes": 0, "memories.use_memories": False,
              "memories.generate_memories": False, "features.skip_host_skill_discovery": True,
              "model_provider": "research_eval", "model_providers.research_eval.name": "Research evaluation",
              "model_providers.research_eval.requires_openai_auth": True,
              "model_providers.research_eval.wire_api": "responses",
              "model_providers.research_eval.supports_websockets": False,
              "model_providers.research_eval.request_max_retries": 0,
              "model_providers.research_eval.stream_max_retries": 0}
    for key, value in config.items():
        args += ["-c", key + "=" + json.dumps(value)]
    return args + ["-"]


def extract(raw, settings):
    events = [json.loads(line) for line in raw.decode("utf-8").splitlines() if line.strip()]
    completed, messages, warnings = [], [], []
    for event in events:
        kind = event.get("type")
        require(kind not in {"turn.failed", "error"}, "CLI reported a failed turn")
        if kind == "turn.completed":
            completed.append(event)
        if kind in {"item.started", "item.updated", "item.completed"}:
            item = event.get("item", {})
            require(item.get("type") in {"agent_message", "reasoning", "error"},
                    "Tool activity or unknown item invalidates isolated judging")
            if item.get("type") == "error":
                warning = item.get("message", "")
                require(warning.startswith("Under-development features enabled: skip_host_skill_discovery."),
                        "CLI reported an item error")
                warnings.append("skip_host_skill_discovery is an under-development CLI feature")
            if kind == "item.completed" and item.get("type") == "agent_message":
                messages.append(item.get("text"))
    require(len(completed) == 1 and len(messages) == 1 and isinstance(messages[0], str) and messages[0].strip(),
            "Expected one completed turn and one unambiguous final message")
    usage = completed[0].get("usage", {})
    incoming, outgoing = usage.get("input_tokens"), usage.get("output_tokens")
    require(type(incoming) is int and incoming >= 0 and type(outgoing) is int and outgoing > 0, "Missing CLI usage")
    require(outgoing <= settings["max_completion_tokens"] and incoming + outgoing <= settings["max_total_tokens"],
            "Post-return CLI token ceiling exceeded")
    return messages[0], usage, warnings


def request(settings, messages, folder, runner=subprocess.run):
    validate(settings)
    require(len(messages) == 2 and [m["role"] for m in messages] == ["system", "user"], "Expected isolated system and packet")
    folder = Path(folder)
    save(folder / "request.json", {"transport": "codex_exec", "model": settings["model"], "messages": messages})
    started = time.monotonic()
    record = {"status": "failed", "model_requested": settings["model"], "model_returned": None,
              "model_identity": "requested_only_cli_does_not_attest", "hard_token_cap": False}
    content = None
    try:
        executable = os.environ.get(settings["executable_env"])
        require(executable and Path(executable).is_absolute() and Path(executable).is_file(), "Set executable_env to an absolute existing Codex CLI path")
        env = {key: value for key, value in os.environ.items() if key.upper() in ENVIRONMENT}
        # A neutral OS temporary directory is outside the repository and contains no coordinator material.
        with tempfile.TemporaryDirectory(prefix="research-judge-") as tmp:
            instruction = Path(tmp) / "instructions.txt"
            instruction.write_text(messages[0]["content"], encoding="utf-8")
            args = command(executable, tmp, instruction, settings)
            save(folder / "command.json", {"argv": command("<CODEX_EXECUTABLE>", "<ISOLATED_WORKDIR>", "<SYSTEM_INSTRUCTION>", settings),
                                          "environment_names": sorted(env), "stdin": "request.json messages[1].content"})
            try:
                result = runner(args, input=messages[1]["content"].encode("utf-8"), stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, timeout=settings["timeout_seconds"], env=env)
            except subprocess.TimeoutExpired as exc:
                (folder / "events.jsonl").write_bytes(exc.stdout or b"")
                (folder / "stderr.txt").write_bytes(exc.stderr or b"")
                record["failure_kind"] = "timeout"
                raise ValueError("CLI deadline exceeded; partial events retained") from exc
        (folder / "events.jsonl").write_bytes(result.stdout)
        (folder / "stderr.txt").write_bytes(result.stderr)
        record["exit_code"] = result.returncode
        require(result.returncode == 0, "CLI exited unsuccessfully; inspect retained stderr")
        content, usage, warnings = extract(result.stdout, settings)
        record.update(usage=usage, warnings=warnings, status="response_complete")
    except (OSError, ValueError, TypeError, KeyError) as exc:
        record.setdefault("failure_kind", "cli_execution_or_envelope")
        record["error"] = str(exc)
        content = None
    record["elapsed_seconds"] = round(time.monotonic() - started, 3)
    save(folder / "execution.json", record)
    return content
