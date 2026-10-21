#!/usr/bin/env python3
"""Exercise the packaged server over real MCP stdio with synthetic reviewer processes."""
from __future__ import annotations
import asyncio
import csv
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
        "corrected='The source reports twelve shipments. No revenue figure is supplied.\\n'\n"
        "result=SyntheticRunner(negative=request['assignment']['report']!=corrected)({},request,None)\n"
        "print(json.dumps({'execution_id':result['execution_id'],'content':result['content']}))\n",
        encoding="utf-8")
    worker_config = {"format": "json", "model": "synthetic-process",
                     "command": [sys.executable, "-B", "-X", "utf8", str(worker)]}
    config = base/"review-config.json"
    config.write_text(json.dumps({"reviewers": [{"id": "primary", **worker_config}]}), encoding="utf-8")
    workspace = base/"tasks"
    env = {"RESEARCH_TOOLKIT_WORKSPACE": str(workspace),
           "RESEARCH_TOOLKIT_REVIEW_CONFIG": str(config), "PYTHONDONTWRITEBYTECODE": "1"}
    server = StdioServerParameters(command=sys.executable, args=[
        "-B", "-X", "utf8", str(ROOT/"plugins/research-toolkit/scripts/research_mcp.py")], env=env)
    async with Client(server, read_timeout_seconds=30) as client:
        tools = await client.list_tools()
        names = {tool.name for tool in tools.tools}
        assert names == {"research_start", "research_save", "research_status", "research_guide", "research_review", "research_finish", "research_check_reviewer", "research_check_draft", "research_check_updates"}, names
        guide = unpack(await client.call_tool("research_guide", {"stage": "brief", "language": "zh"}))
        assert "研究工作流" in guide["guidance"][0]["content"]
        for language, suffix in (("en", ".md"), ("zh", ".zh-CN.md")):
            lite_guide = unpack(await client.call_tool("research_guide", {
                "stage": "final", "language": language, "profile": "lite"}))
            assert [item["path"] for item in lite_guide["guidance"]] == ["references/lite-workflow" + suffix]
            assert "`claims_and_sources`" in lite_guide["guidance"][0]["content"]
            assert "state/final_delivery.json" not in lite_guide["guidance"][0]["content"]
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
        denied_review = await client.call_tool("research_review", {"task": "case", "evidence_paths": ["source.md"]})
        assert denied_review.is_error
        (root/"data/source_registry.csv").write_text("source_id,title,url,source_type,read_scope,read_evidence\nS1,Shipments,https://example.org/source,primary,full_text,source.md\n", encoding="utf-8")
        (root/"data/claims_registry.csv").write_text("claim_id,claim,claim_type,supporting_sources\nC1,Twelve shipments,verified_fact,S1\n", encoding="utf-8")
        draft = unpack(await client.call_tool("research_status", {"task": "case", "stage": "draft"}))
        assert draft["progress"]["stage"] == "draft"
        reviewed = unpack(await client.call_tool("research_review", {"task": "case", "evidence_paths": ["source.md"]}))
        assert reviewed["reviews_complete"], reviewed

        rows = [json.loads(line) for line in (root/"logs/review.jsonl").read_text(encoding="utf-8").splitlines()]
        assert len([row for row in rows if row.get("record_type") == "model_review"]) == 1
        assert not any(row.get("record_type") in {"review_audit", "sampling_audit"} for row in rows)
        blocked = unpack(await client.call_tool("research_finish", {"task": "case", "message": "The final report is complete."}))
        assert not blocked["completed"], blocked
        original = next(row for row in rows if row.get("record_type") == "model_review")
        decision = {"record_type": "finding_disposition", "attempt_id": original["attempt_id"],
                    "schema_version": 2, "decision_actor": {"id": "author:case", "role": "author"},
                    "artifact_sha256": original["artifact_sha256"], "response_sha256": original["response"]["sha256"],
                    "finding_id": "F1", "decision": "no_change",
                    "reason": "The report states that revenue is not reported; the review misreads it.",
                    "evidence": "final.md paragraph 2 and source.md paragraph 1 report shipments, not revenue."}
        with (root/"logs/review.jsonl").open("a", encoding="utf-8") as log:
            log.write(json.dumps(decision)+"\n")
        finished = unpack(await client.call_tool("research_finish", {"task": "case", "message": "The final report is complete."}))
        assert finished["completed"], finished
        current = unpack(await client.call_tool("research_status", {"task": "case"}))
        assert current["progress"]["status"] == "complete"
        receipt = (root/"state/final_delivery.json").read_bytes()
        history = (root/"logs/review.jsonl").read_bytes()
        replay = unpack(await client.call_tool("research_review", {"task": "case", "evidence_paths": ["source.md"]}))
        assert replay["reviews_complete"] and replay["reused"], replay
        current = unpack(await client.call_tool("research_status", {"task": "case"}))
        assert current["progress"]["status"] == "complete"
        assert (root/"state/final_delivery.json").read_bytes() == receipt
        assert (root/"logs/review.jsonl").read_bytes() == history
        readiness = unpack(await client.call_tool("research_check_reviewer", {}))
        assert readiness["status"] == "unverified"
        from profile_policy import CHECKLIST
        for profile, task in (("lite", "lite-case"), ("full", "self-case")):
            created = unpack(await client.call_tool("research_start", {"task": task, "brief": BRIEF, "profile": profile}))
            local = Path(created["task_directory"])
            (local/"source.md").write_bytes((root/"source.md").read_bytes())
            record_args = {"task": task,
                "sources": [{"source_id": "S1", "title": "Shipments", "url": "https://example.org/source", "source_type": "primary", "read_scope": "full_text", "read_evidence": "source.md"}],
                "claims": [{"claim_id": "C1", "claim": "Twelve shipments", "claim_type": "verified_fact", "supporting_sources": ["S1"]}],
                "draft": {"path": "final.md", "content": (root/"final.md").read_text(encoding="utf-8"), "complete": True},
                "requirements": [{
                "requirement_id": "R-length", "summary": "Synthetic whole-file limit of 1–100 words.",
                "status": "satisfied", "evidence": "final.md",
                "length_constraint": {"unit": "whitespace_words", "scope": "whole_artifact", "min": 1, "max": 100}}]}
            saved = unpack(await client.call_tool("research_save", record_args))
            assert saved["ok"] and saved["saved_ids"]["sources"] == ["S1"], saved
            assert saved["changes"]["records"]["sources"]["added"] == ["S1"], saved
            unchanged = unpack(await client.call_tool("research_save", {"task": task, "sources": [{"source_id": "S1"}]}))
            assert unchanged["updated_files"] == [] and unchanged["changes"]["records"]["sources"]["unchanged"] == ["S1"], unchanged
            current_changes = unpack(await client.call_tool("research_status", {"task": task}))["changes"]
            assert current_changes == unchanged["changes"], current_changes
            bad = unpack(await client.call_tool("research_save", {"task": task, "sources": [{"source_id": "S1", "title": 42}]}))
            assert not bad["ok"] and "sources[0].title" in bad["errors"][0], bad
            arguments = {"task": task, "evidence_paths": ["source.md"], "reviewer": "self"}
            length_file = local/"state/requirements.jsonl"
            length_row = json.loads(length_file.read_text(encoding="utf-8"))
            length_row.update(status="pending", evidence="")
            assert unpack(await client.call_tool("research_save", {"task": task, "requirements": [length_row]}))["ok"]
            before = {p.relative_to(local): p.read_bytes() for p in local.rglob("*") if p.is_file()}
            unresolved = unpack(await client.call_tool("research_check_draft", {"task": task}))
            assert not unresolved["ok"] and unresolved["length_checks"][0]["bounds_met"], unresolved
            assert "R-length" in unresolved["next_action"] and "still pending" in unresolved["next_action"]
            assert before == {p.relative_to(local): p.read_bytes() for p in local.rglob("*") if p.is_file()}
            length_row.update(status="satisfied", evidence="final.md")
            assert unpack(await client.call_tool("research_save", {"task": task, "requirements": [length_row]}))["ok"]
            before = {p.relative_to(local): p.read_bytes() for p in local.rglob("*") if p.is_file()}
            checked = unpack(await client.call_tool("research_check_draft", {"task": task}))
            assert checked["ok"] and checked["length_checks"][0]["bounds_met"], checked
            assert checked["semantic_quality"] == checked["delivery_status"] == "not_assessed"
            assert before == {p.relative_to(local): p.read_bytes() for p in local.rglob("*") if p.is_file()}
            pending = unpack(await client.call_tool("research_review", arguments))
            finish_args = {"task": task, "message": "The report is complete; no independent review was performed."}
            if profile == "lite":
                assert pending["skipped"]
                needed = unpack(await client.call_tool("research_finish", finish_args))
                assert needed["action_required"] == "final_checklist"
                finish_args["checklist"] = {k: {"passed": True, "evidence": "Synthetic MCP control: final.md and source.md."} for k in CHECKLIST}
            else:
                assert pending["action_required"] == "self_review"
                arguments["include_assignment"] = False
                compact = unpack(await client.call_tool("research_review", arguments))
                assert "assignment" in pending and "assignment" not in compact
                assert compact["input_version"] == pending["input_version"]
                assert compact["assignment_ref"] == pending["assignment_ref"]
                frozen = local/compact["assignment_ref"]["path"]
                assert json.loads(frozen.read_text(encoding="utf-8")) == pending["assignment"]
                from check_research_workflow import SyntheticRunner
                value = json.loads(SyntheticRunner()({}, {"role": "reviewer"}, None)["content"])
                arguments["self_review"] = {**value, "input_version": pending["input_version"]}
                reviewed = unpack(await client.call_tool("research_review", arguments))
                assert reviewed["reviews_complete"] and reviewed["review_strength"] == "degraded"
            done = unpack(await client.call_tool("research_finish", finish_args))
            assert done["completed"], done
            assert done["delivery_check"]["length_checks"][0]["bounds_met"] is True
            resumed = unpack(await client.call_tool("research_status", {"task": task, "language": "zh"}))
            assert resumed["profile"] == profile
            if profile == "lite":
                assert resumed["guidance"][0]["path"] == "references/lite-workflow.zh-CN.md"
                assert resumed["delivery_check"]["terminal_state"] and resumed["delivery_check"]["checklist_valid"]
                receipt = (local/"state/final_checklist.json").read_bytes()
                resumed = unpack(await client.call_tool("research_status", {"task": task, "stage": "revise"}))
                assert resumed["progress"]["status"] == "in_progress"
                process = await asyncio.create_subprocess_exec(sys.executable, "-X", "utf8",
                    str(ROOT/"plugins/research-toolkit/scripts/check_delivery.py"), str(local), "--json",
                    stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
                stdout, stderr = await process.communicate()
                checked = json.loads(stdout)
                assert process.returncode == 1 and "incomplete_lite_task" in checked["flags"], (checked, stderr)
                assert checked["checklist_valid"] and not checked["terminal_state"]
                assert (local/"state/final_checklist.json").read_bytes() == receipt
                done = unpack(await client.call_tool("research_finish", finish_args))
                assert done["completed"], done
                resumed = unpack(await client.call_tool("research_status", {"task": task}))
                assert resumed["progress"]["status"] == "complete" and resumed["delivery_check"]["ok"]
        # Fill only the columns emitted by start, then correct a real negative
        # synthetic verdict and re-review through the packaged stdio interface.
        created = unpack(await client.call_tool("research_start", {"task": "template-mcp", "brief": BRIEF, "profile": "full"}))
        local = Path(created["task_directory"])
        (local/"sources").mkdir()
        corrected = "The source reports twelve shipments. No revenue figure is supplied.\n"
        (local/"sources/S1.md").write_text(corrected, encoding="utf-8")
        for name, row in (("source_registry.csv", {"source_id": "S1", "title": "Shipments", "url": "https://example.org/source",
                "source_type": "primary", "read_scope": "full_text", "read_evidence": "https://example.org/source#p1", "evidence_path": "sources/S1.md"}),
                ("claims_registry.csv", {"claim_id": "C1", "claim": "Twelve shipments", "claim_type": "verified_fact", "supporting_sources": "S1"})):
            path = local/"data"/name
            with path.open(encoding="utf-8", newline="") as stream:
                fields = next(csv.reader(stream))
            with path.open("w", encoding="utf-8", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=fields); writer.writeheader(); writer.writerow(row)
        (local/"memo.md").write_text("The source reports twelve shipments.\n\nRevenue is twelve.\n", encoding="utf-8")
        unpack(await client.call_tool("research_status", {"task": "template-mcp", "stage": "draft"}))
        args = {"task": "template-mcp", "artifact": "memo.md", "evidence_paths": ["sources/S1.md"]}
        reviewed = unpack(await client.call_tool("research_review", args))
        assert reviewed["reviews_complete"] and reviewed["review_check"]["completed_slots"] == 1
        assert not reviewed["delivery_ready"] and reviewed["open_issues"]
        (local/"memo.md").write_text(corrected, encoding="utf-8")
        revised = unpack(await client.call_tool("research_review", {**args, "revision": True}))
        assert revised["delivery_ready"] and not revised["open_issues"]
        delivered = unpack(await client.call_tool("research_finish", {"task": "template-mcp", "artifact": "memo.md", "message": "The memo is complete."}))
        assert delivered["completed"], delivered
        resumed = unpack(await client.call_tool("research_status", {"task": "template-mcp"}))
        assert resumed["progress"]["status"] == "complete" and resumed["delivery_check"]["ok"]
        recorded = (local/"state/progress.json").read_bytes()
        (local/"memo.md").write_text("Changed after delivery.", encoding="utf-8")
        stale = unpack(await client.call_tool("research_status", {"task": "template-mcp"}))
        assert stale["progress"]["status"] == "stale" and not stale["delivery_check"]["ok"]
        assert (local/"state/progress.json").read_bytes() == recorded
        history = [json.loads(line) for line in (local/"logs/review.jsonl").read_text(encoding="utf-8").splitlines()]
        assert [r["report_verdict"] for r in history if r.get("record_type") == "model_review"] == ["needs_revision", "pass"]
        # Optional continuity fields travel through the packaged MCP schema.
        before_receipt = (local/"state/final_delivery.json").read_bytes()
        current = unpack(await client.call_tool("research_save", {"task": "template-mcp",
            "brief": {"output": "A comparison note"},
            "draft": {"path": "comparison.md", "content": "Comparison underway.", "main": True, "kind": "comparison"}}))
        assert current["ok"] and current["current_work"]["artifact"]["kind"] == "comparison"
        resumed = unpack(await client.call_tool("research_status", {"task": "template-mcp"}))
        assert resumed["progress"]["status"] == "in_progress"
        assert resumed["current_work"]["last_delivery"]["artifact"] == "memo.md"
        assert resumed["runtime"]["host_loaded_entry"] == "not_observed"
        wrong = await client.call_tool("research_finish", {"task": "template-mcp", "artifact": "memo.md", "message": "Done"})
        assert wrong.is_error
        assert (local/"state/final_delivery.json").read_bytes() == before_receipt
        resources = await client.list_resources()
        assert any(str(r.uri) == "research-toolkit://instructions" for r in resources.resources)
        prompts = await client.list_prompts()
        assert any(p.name == "research" for p in prompts.prompts)
    print("PASS: packaged MCP discovery, bilingual guidance, template-based review/revision/delivery, stale status and preserved negative reviews.")


def main():
    temp_root = os.environ.get("IRF_TEST_TMPDIR")
    with tempfile.TemporaryDirectory(prefix="research-mcp-test-", dir=temp_root) as tmp:
        asyncio.run(verify(Path(tmp)))


if __name__ == "__main__":
    main()
