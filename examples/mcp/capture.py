#!/usr/bin/env python3
"""Capture native-agent assignments over real MCP; preserve the old example as history."""
from __future__ import annotations
import argparse
import asyncio
import csv
import json
from pathlib import Path
import sys
from mcp.client import Client
from mcp.client.stdio import StdioServerParameters

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


async def capture(output, pause, resume, host_result=None, host_task=None):
    if resume:
        calls = read(output / "transcript.json")
    else:
        output.mkdir(parents=True, exist_ok=False)
        calls = []
    workspace = output / "tasks"
    server = StdioServerParameters(command=sys.executable, args=["-B", "-X", "utf8", str(ROOT / "scripts/research_mcp.py")],
        env={"RESEARCH_TOOLKIT_WORKSPACE": str(workspace), "RESEARCH_TOOLKIT_REVIEW_BACKEND": "", "RESEARCH_TOOLKIT_REVIEW_CONFIG": "", "PYTHONDONTWRITEBYTECODE": "1",
             "RESEARCH_TOOLKIT_TELEMETRY": "off"})
    async with Client(server, read_timeout_seconds=60) as client:
        async def call(name, arguments):
            response = await client.call_tool(name, arguments)
            raw = response.model_dump(mode="json", by_alias=True)
            calls.append({"tool": name, "arguments": arguments, "response": raw})
            save(output / "transcript.json", calls)
            if raw.get("isError"):
                raise RuntimeError(raw)
            return raw["structuredContent"]
        if not resume:
            started = await call("research_start", read(HERE / "start.json"))
            await call("research_guide", {"stage": "draft", "language": "en"})
            task = Path(started["task_directory"])
            (task / "source.md").write_text((HERE / "source.md").read_text(encoding="utf-8"), encoding="utf-8")
            await call("research_save", {"task": "shipment-note",
                "sources": list(csv.DictReader((HERE / "source_registry.csv").read_text(encoding="utf-8").splitlines())),
                "claims": list(csv.DictReader((HERE / "claims_registry.csv").read_text(encoding="utf-8").splitlines())),
                "draft": {"path": "final.md", "content": (HERE / "final.md").read_text(encoding="utf-8"),
                          "main": True, "host_task": host_task}})
            await call("research_status", {"task": "shipment-note", "stage": "draft"})
        arguments = {"task": "shipment-note", "evidence_paths": ["source.md"], "include_assignment": False}
        pending = await call("research_review", {**arguments, **({"host_result": read(host_result)} if host_result else {})})
        save(output / "review-request.json", pending)
        if not pending.get("delivery_ready"):
            print("Assignments for independent agents and current findings are in review-request.json. "
                  "Have the agents read the current assignments and source files; submit each actual result with --resume --host-result. "
                  "No supplied self-review is replayed and no independent model work is claimed by this capture script.")
            return
        finished = await call("research_finish", {"task": "shipment-note", "message": "The fictional shipment note has completed its independent review, audit and acceptance."})
        if not finished.get("completed"):
            raise RuntimeError("Example did not complete; inspect transcript.json")
        print("Original MCP calls, agent submissions and the current receipt are retained in the output directory.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="New output directory outside the installed toolkit")
    parser.add_argument("--pause-before-review", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--host-task", help="Actual task/session ID of the agent registering this example manuscript; required on the first run")
    parser.add_argument("--host-result", type=Path, help="JSON with the actual slot_id, host_task, response_path and execution_path")
    args = parser.parse_args()
    output = args.output.resolve()
    if output == ROOT or ROOT in output.parents:
        parser.error("Use an output directory outside the installed toolkit")
    if args.host_result and not args.resume:
        parser.error("Use --resume when submitting a completed agent assignment")
    if not args.resume and not (args.host_task and args.host_task.strip()):
        parser.error("--host-task: provide the actual calling agent task/session ID on the first run")
    asyncio.run(capture(output, args.pause_before_review, args.resume, args.host_result, args.host_task))


if __name__ == "__main__":
    main()
