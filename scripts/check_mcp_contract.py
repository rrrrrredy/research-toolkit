#!/usr/bin/env python3
"""Exercise the packaged server over real MCP stdio with synthetic reviewer processes."""
from __future__ import annotations
import asyncio
import json
import os
from pathlib import Path
import sys
import tempfile
from mcp.client import Client
from mcp.client.stdio import StdioServerParameters
from check_research_workflow import BRIEF

ROOT = Path(__file__).resolve().parents[1]


def unpack(result):
    value = result.model_dump(mode="json", by_alias=True)
    assert not value.get("isError"), value
    if value.get("structuredContent") is not None:
        return value["structuredContent"]
    return json.loads("\n".join(item["text"] for item in value["content"] if item["type"] == "text"))


async def verify(base):
    worker = base/"synthetic-worker.py"
    worker.write_text(
        "import json,sys\n"
        f"sys.path.insert(0,{str(ROOT/'scripts')!r})\n"
        "from check_research_workflow import SyntheticRunner\n"
        "request=json.load(sys.stdin)\n"
        "result=SyntheticRunner()({},request,None)\n"
        "print(json.dumps({'execution_id':result['execution_id'],'content':result['content']}))\n",
        encoding="utf-8")
    worker_config = {"format": "json", "model": "synthetic-process",
                     "command": [sys.executable, "-B", "-X", "utf8", str(worker)]}
    config = base/"review-config.json"
    config.write_text(json.dumps({"reviewers": [{"id": "primary", **worker_config}],
                                  "auditor": {"id": "audit", **worker_config}}), encoding="utf-8")
    workspace = base/"tasks"
    env = {"RESEARCH_TOOLKIT_WORKSPACE": str(workspace),
           "RESEARCH_TOOLKIT_REVIEW_CONFIG": str(config), "PYTHONDONTWRITEBYTECODE": "1"}
    server = StdioServerParameters(command=sys.executable, args=[
        "-B", "-X", "utf8", str(ROOT/"plugins/research-toolkit/scripts/research_mcp.py")], env=env)
    async with Client(server, read_timeout_seconds=30) as client:
        tools = await client.list_tools()
        names = {tool.name for tool in tools.tools}
        assert names == {"research_start", "research_status", "research_guide", "research_review", "research_finish"}, names
        guide = unpack(await client.call_tool("research_guide", {"stage": "brief", "language": "zh"}))
        assert "研究工作流" in guide["guidance"][0]["content"]
        denied = await client.call_tool("research_start", {"task": "../outside", "brief": BRIEF})
        assert denied.is_error
        brief = unpack(await client.call_tool("research_start", {"task": "case", "brief": {"question": "What changed?"}}))
        assert not brief["ready_for_collection"]
        ready = unpack(await client.call_tool("research_start", {"task": "case", "brief": BRIEF}))
        assert ready["ready_for_collection"]
        assert ready["review_readiness"]["status"] == "unverified"
        assert not ready["review_readiness"]["model_access_verified"]
        root = Path(ready["task_directory"])
        (root/"final.md").write_text("The source reports twelve shipments.\n\nRevenue is not reported.\n", encoding="utf-8")
        (root/"source.md").write_text("Company A reported twelve shipments in 2026.\n", encoding="utf-8")
        (root/"data/source_registry.csv").write_text("source_id,title,url,source_type,read_scope,read_evidence\nS1,,,,,\n", encoding="utf-8")
        empty = await client.call_tool("research_status", {"task": "case", "stage": "draft"})
        assert empty.is_error
        (root/"data/source_registry.csv").write_text("source_id,title,url,source_type,read_scope,read_evidence\nS1,Shipments,https://example.org/source,primary,full_text,source.md\n", encoding="utf-8")
        (root/"data/claims_registry.csv").write_text("claim_id,claim,claim_type,supporting_sources\nC1,Twelve shipments,verified_fact,S1\n", encoding="utf-8")
        draft = unpack(await client.call_tool("research_status", {"task": "case", "stage": "draft"}))
        assert draft["progress"]["stage"] == "draft"
        reviewed = unpack(await client.call_tool("research_review", {"task": "case", "evidence_paths": ["source.md"]}))
        assert reviewed["reviews_complete"], reviewed
        finished = unpack(await client.call_tool("research_finish", {"task": "case", "message": "The final report is complete."}))
        assert finished["completed"], finished
        current = unpack(await client.call_tool("research_status", {"task": "case"}))
        assert current["progress"]["status"] == "complete"
        resources = await client.list_resources()
        assert any(str(r.uri) == "research-toolkit://instructions" for r in resources.resources)
        prompts = await client.list_prompts()
        assert any(p.name == "research" for p in prompts.prompts)
    print("PASS: packaged MCP discovery, Chinese guidance, path boundary, clarification and full synthetic review/delivery flow.")


def main():
    temp_root = os.environ.get("IRF_TEST_TMPDIR")
    with tempfile.TemporaryDirectory(prefix="research-mcp-test-", dir=temp_root) as tmp:
        asyncio.run(verify(Path(tmp)))


if __name__ == "__main__":
    main()
