#!/usr/bin/env python3
"""Capture real MCP calls using a fictional report and an explicitly supplied self-review."""
from __future__ import annotations
import argparse
import hashlib
import asyncio
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


def verify_inputs(base=HERE):
    binding = read(base / "self-review-binding.json")["sha256_lf"]
    for name, expected in binding.items():
        actual = hashlib.sha256((base / name).read_text(encoding="utf-8").encode("utf-8")).hexdigest()
        if actual != expected:
            raise ValueError(f"Changed example input: {name}; the supplied self-review applies only to the original example")


async def capture(output, pause, resume):
    verify_inputs()
    if resume:
        calls = read(output / "transcript.json")
    else:
        output.mkdir(parents=True, exist_ok=False)
        calls = []
    workspace = output / "tasks"
    server = StdioServerParameters(command=sys.executable, args=["-B", "-X", "utf8", str(ROOT / "scripts/research_mcp.py")],
        env={"RESEARCH_TOOLKIT_WORKSPACE": str(workspace), "RESEARCH_TOOLKIT_REVIEW_BACKEND": "", "RESEARCH_TOOLKIT_REVIEW_CONFIG": "", "PYTHONDONTWRITEBYTECODE": "1"})
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
            await call("research_guide", {"stage": "draft", "language": "en", "profile": "full"})
            task = Path(started["task_directory"])
            for source, dest in (("source.md", "source.md"), ("final.md", "final.md"), ("source_registry.csv", "data/source_registry.csv"), ("claims_registry.csv", "data/claims_registry.csv")):
                (task / dest).write_text((HERE / source).read_text(encoding="utf-8"), encoding="utf-8")
            await call("research_status", {"task": "shipment-note", "stage": "draft"})
        arguments = {"task": "shipment-note", "evidence_paths": ["source.md"], "reviewer": "self"}
        pending = await call("research_review", arguments)
        save(output / "review-request.json", pending)
        if pause:
            print("Self-review prompt saved in review-request.json; no review submitted.")
            return
        review = read(HERE / "self-review.json")
        reviewed = await call("research_review", {**arguments, "self_review": {**review, "input_version": pending["input_version"]}})
        finished = await call("research_finish", {"task": "shipment-note", "message": "The fictional shipment note is complete, with self-review only and no independent review."})
        if not reviewed.get("reviews_complete") or not finished.get("completed"):
            raise RuntimeError("Example did not complete; inspect transcript.json")
        print("Captured real MCP calls in transcript.json; replayed the supplied author self-review, with degraded strength. No external model was called.")
        print(json.dumps({"reviews_complete": reviewed["reviews_complete"], "review_strength": reviewed["review_strength"], "completed": finished["completed"]}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="New output directory outside the installed toolkit")
    parser.add_argument("--pause-before-review", action="store_true")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    output = args.output.resolve()
    if output == ROOT or ROOT in output.parents:
        parser.error("Use an output directory outside the installed toolkit")
    asyncio.run(capture(output, args.pause_before_review, args.resume))


if __name__ == "__main__":
    main()
