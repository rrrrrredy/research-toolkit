#!/usr/bin/env python3
"""Packaged MCP stdio control with retained synthetic host executions; no research-quality claim."""
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
        "result=SyntheticRunner(negative='Revenue is twelve.' in request['assignment']['report'],bad_review=int('--malformed' in sys.argv))({},request,None)\n"
        "print(json.dumps(result))\n", encoding="utf-8")
    workspace = base/"tasks"
    env = {"RESEARCH_TOOLKIT_WORKSPACE": str(workspace), "RESEARCH_TOOLKIT_REVIEW_CONFIG": "",
           "RESEARCH_TOOLKIT_REVIEW_BACKEND": "", "PYTHONDONTWRITEBYTECODE": "1"}
    server = StdioServerParameters(command=sys.executable,
        args=["-B", "-X", "utf8", str(ROOT/"plugins/research-toolkit/scripts/research_mcp.py")], env=env)
    async with Client(server, read_timeout_seconds=30) as client:
        async def call(name, arguments, *, error=False):
            result = await client.call_tool(name, arguments)
            with (base/"transport.jsonl").open("a", encoding="utf-8") as log:
                log.write(json.dumps({"tool": name, "arguments": arguments,
                    "return": result.model_dump(mode="json", by_alias=True)}, ensure_ascii=False)+"\n")
            if error:
                assert result.is_error, result
                return result
            return unpack(result)

        tools = await client.list_tools()
        assert {tool.name for tool in tools.tools} == {"research_start", "research_save", "research_status",
            "research_guide", "research_review", "research_finish", "research_check_reviewer", "research_check_draft", "research_check_updates"}
        for language, suffix in (("en", ".md"), ("zh", ".zh-CN.md")):
            for stage in ("brief", "collect", "draft", "revise", "final"):
                guide = await call("research_guide", {"stage": stage, "language": language})
                assert all(item["path"].endswith(suffix) for item in guide["guidance"])
                assert all(item["content"].strip() for item in guide["guidance"])
                if stage in {"brief", "collect"}:
                    assert "artifact_sha256" not in guide["guidance"][0]["content"]
                if stage == "final":
                    assert [item["path"] for item in guide["guidance"]] == ["references/quality-gates"+suffix]
                if stage in {"draft", "revise"}:
                    assert "\n## Worked Choices in Research Prose" not in guide["guidance"][0]["content"]
                    assert "\n## 研究段落的取舍示范" not in guide["guidance"][0]["content"]
            old_alias = await call("research_guide", {"stage": "final", "language": language, "profile": "lite"})
            assert old_alias["guidance"] == guide["guidance"]
        await call("research_start", {"task": "../outside", "brief": BRIEF}, error=True)
        first = await call("research_start", {"task": "case", "brief": {"question": "What changed?"}, "profile": "lite"})
        assert not first["ready_for_collection"] and first["profile"] == "full"
        ready = await call("research_start", {"task": "case", "brief": BRIEF})
        assert ready["ready_for_collection"] and ready["review_readiness"]["status"] == "host_native"
        root = Path(ready["task_directory"])
        assert json.loads((root/"state/progress.json").read_text(encoding="utf-8"))["review_contract"] == 2
        (root/"source.md").write_text("Company A reports twelve shipments in 2026. No revenue figure is supplied.\n", encoding="utf-8")
        (root/"counter.md").write_text("The product catalog lists delivery options, not booked or recognized revenue.\n", encoding="utf-8")
        (root/"final.md").write_text("The source reports twelve shipments.\n\nRevenue is twelve.\n\nA revenue estimate requires prices and revenue recognition evidence.\n", encoding="utf-8")
        (root/"data/source_registry.csv").write_text("source_id,title,url,source_type,read_scope,read_evidence\nS1,,,,,\n", encoding="utf-8")
        await call("research_status", {"task": "case", "stage": "draft"}, error=True)
        await call("research_review", {"task": "case", "evidence_paths": []}, error=True)
        saved = await call("research_save", {"task": "case", "replace": ["sources"],
            "sources": [{"source_id": "S1", "title": "Shipments", "url": "https://example.org/source", "source_type": "primary",
                         "read_scope": "full_text", "read_evidence": "source.md"},
                        {"source_id": "S2", "title": "Catalog", "url": "https://example.org/catalog", "source_type": "primary",
                         "read_scope": "full_text", "read_evidence": "counter.md"}],
            "claims": [{"claim_id": "C1", "claim": "Twelve shipments", "claim_type": "verified_fact",
                        "supporting_sources": ["S1"], "counter_evidence": "S2"}],
            "requirements": [{"requirement_id": "R1", "summary": "Distinguish shipment counts from revenue and explain the missing evidence.",
                              "status": "satisfied", "evidence": "final.md paragraphs 1–3",
                              "length_constraint": {"unit": "whitespace_words", "scope": "whole_artifact", "min": 10, "max": 150}}],
            "draft": {"path": "final.md", "main": True, "host_task": "synthetic-author", "complete": True}})
        assert saved["ok"] and saved["saved_ids"]["sources"] == ["S1", "S2"]
        untouched = await call("research_save", {"task": "case", "sources": [{"source_id": "S1"}]})
        assert untouched["updated_files"] == [] and untouched["changes"]["records"]["sources"]["unchanged"] == ["S1"]
        bad = await call("research_save", {"task": "case", "sources": [{"source_id": "S1", "title": 42}]})
        assert not bad["ok"] and "sources[0].title" in bad["errors"][0]
        pending_req = {"requirement_id": "R1", "status": "pending", "evidence": ""}
        await call("research_save", {"task": "case", "requirements": [pending_req]})
        before = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
        checked = await call("research_check_draft", {"task": "case"})
        assert not checked["ok"] and checked["length_checks"][0]["bounds_met"]
        assert before == {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
        await call("research_save", {"task": "case", "requirements": [{"requirement_id": "R1", "status": "satisfied", "evidence": "final.md paragraphs 1–3"}]})
        checked = await call("research_check_draft", {"task": "case"})
        assert checked["ok"] and checked["semantic_quality"] == checked["delivery_status"] == "not_assessed"
        # A separate unfinished branch must not block selected, already-read work.
        (root/'unread.md').write_text('The separate depot reports two test routes. This supplies no Company A revenue evidence.\n', encoding='utf-8')
        await call('research_save', {'task': 'case',
            'sources': [{'source_id': 'S3', 'title': 'Independent branch', 'url': 'https://example.org/other-depot',
                         'source_type': 'primary', 'read_scope': 'not_read', 'evidence_path': 'unread.md'}],
            'claims': [{'claim_id': 'C2', 'claim': 'The separate depot reports two test routes.',
                        'claim_type': 'verified_fact', 'supporting_sources': ['S3']}]})
        await call('research_status', {'task': 'case', 'stage': 'draft'}, error=True)
        selected = await call('research_status', {'task': 'case', 'stage': 'draft',
            'work': {'question': 'What can the already-read Company A records establish?', 'claim_ids': ['C1']}})
        assert selected['progress']['stage'] == 'draft'
        assert {row['source_id'] for row in selected['work_context']['sources']} == {'S1', 'S2'}
        assert 'unread.md' not in selected['work_context']['files']
        await call('research_save', {'task': 'case',
            'sources': [{'source_id': 'S3', 'read_scope': 'full_text', 'read_evidence': 'unread.md'}]})
        await call('research_status', {'task': 'case', 'stage': 'draft'})
        args = {"task": "case", "evidence_paths": [], "domains": ["shipment and financial metric interpretation"], "include_assignment": True}
        await call("research_review", {**args, "reviewer": "self"}, error=True)
        pending = await call("research_review", args)
        assert len(pending["assignments"]) == 8 and pending["action_required"] == "host_agents"
        assert "counter.md" in pending["assignments"][0]["assignment"]["assignment"]["sources"]
        sequence = 0
        async def submit(item, *, malformed=False, producer=False):
            nonlocal sequence
            sequence += 1
            folder = root/"captures"/str(sequence)
            folder.mkdir(parents=True)
            request = item["assignment"]
            (folder/"request.json").write_text(json.dumps(request, ensure_ascii=False, indent=2), encoding="utf-8")
            command = [sys.executable, "-B", "-X", "utf8", str(worker)] + (["--malformed"] if malformed else [])
            process = await asyncio.create_subprocess_exec(*command, stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await process.communicate(json.dumps(request, ensure_ascii=False).encode("utf-8"))
            (folder/"stdout.json").write_bytes(stdout); (folder/"stderr.txt").write_bytes(stderr)
            (folder/"command.json").write_text(json.dumps(command), encoding="utf-8")
            assert process.returncode == 0, stderr
            result = json.loads(stdout)
            identity = "synthetic-author" if producer else result["execution_id"]
            (folder/"response.json").write_text(result["content"], encoding="utf-8")
            (folder/"execution.json").write_text(json.dumps({"host_task": identity, "status": "completed",
                "assignment_version": request["assignment_version"], "synthetic": True, "returncode": process.returncode}), encoding="utf-8")
            return await call("research_review", {**args, "host_result": {"slot_id": item["slot_id"], "host_task": identity,
                "response_path": (folder/"response.json").relative_to(root).as_posix(),
                "execution_path": (folder/"execution.json").relative_to(root).as_posix()}}, error=malformed or producer)

        # One malformed first response and one producer impersonation are retained/rejected; then complete actual slots.
        await submit(pending["assignments"][0], producer=True)
        await submit(pending["assignments"][0], malformed=True)
        while pending["assignments"]:
            pending = await submit(pending["assignments"][0])
        assert pending["reviews_complete"] and not pending["delivery_ready"] and pending["open_issues"]
        rows = [json.loads(line) for line in (root/"logs/review.jsonl").read_text(encoding="utf-8").splitlines()]
        negatives = [row for row in rows if row.get("record_type") == "model_review" and row.get("status") == "completed"]
        assert len(negatives) == 8 and all(row["report_verdict"] == "needs_revision" for row in negatives)
        assert any(row.get("status") == "incomplete" for row in rows)
        for original in negatives:
            with (root/"logs/review.jsonl").open("a", encoding="utf-8") as log:
                log.write(json.dumps({"record_type": "finding_disposition", "attempt_id": original["attempt_id"],
                    "schema_version": 2, "decision_actor": {"id": "author:case", "role": "author"},
                    "artifact_sha256": original["artifact_sha256"], "response_sha256": original["response"]["sha256"],
                    "finding_id": "F1", "decision": "no_change", "reason": "Synthetic author tries to waive the defect.",
                    "evidence": "final.md paragraph 2"})+"\n")
        assert not (await call("research_finish", {"task": "case", "message": "Complete."}))["completed"]
        first_report = (root/"final.md").read_bytes()
        (root/"first-draft.md").write_bytes(first_report)
        first_log = (root/"logs/review.jsonl").read_bytes()
        (root/"first-review-log.jsonl").write_bytes(first_log)
        # An input-only revision must carry unresolved findings even when prose is identical.
        await call("research_save", {"task": "case", "sources": [{"source_id": "S2", "title": "Catalog and delivery terms"}],
            "requirements": [{"requirement_id": "R1", "summary": "Distinguish shipment counts from revenue, explain missing evidence, and preserve the source's reporting period."}]})
        input_revision = await call("research_review", {**args, "revision": True})
        assert (root/"final.md").read_bytes() == first_report
        carried = input_revision["assignments"][0]["assignment"]["assignment"]["prior_required_findings"]
        assert len(carried) == 8 and all(item["finding"]["finding_id"] == "F1" for item in carried), carried
        corrected = "The source reports twelve shipments.\n\nRevenue is not reported. A shipment count cannot establish recognized revenue without prices and recognition terms.\n\nThe catalog adds product details but no financial evidence, so it does not resolve the gap.\n"
        changed = await call("research_save", {"task": "case", "draft": {"path": "final.md", "content": corrected,
            "host_task": "synthetic-author", "complete": True}})
        assert changed["ok"] and changed["backups"]
        pending = await call("research_review", {**args, "revision": True})
        while pending["assignments"]:
            pending = await submit(pending["assignments"][0])
        assert pending["delivery_ready"] and pending["completion_check"]["completed_slots"] == 10, pending
        done = await call("research_finish", {"task": "case", "message": "The requested report is complete."})
        assert done["completed"], done
        current = await call("research_status", {"task": "case"})
        assert current["progress"]["status"] == "complete" and current["delivery_check"]["ok"]
        assert (root/"first-draft.md").read_bytes() == first_report
        assert (root/"first-review-log.jsonl").read_bytes() == first_log
        receipt = (root/"state/final_delivery.json").read_bytes()
        progress_bytes = (root/"state/progress.json").read_bytes()
        (root/"counter.md").write_text("Changed after delivery.\n", encoding="utf-8")
        stale = await call("research_status", {"task": "case"})
        assert stale["progress"]["status"] == "stale" and not stale["delivery_check"]["ok"]
        assert (root/"state/final_delivery.json").read_bytes() == receipt
        assert (root/"state/progress.json").read_bytes() == progress_bytes
        resources = await client.list_resources()
        assert any(str(item.uri) == "research-toolkit://instructions" for item in resources.resources)
        prompts = await client.list_prompts()
        assert any(item.name == "research" for item in prompts.prompts)
    (base/"RESULT.json").write_text(json.dumps({"result": "pass", "kind": "synthetic_stdio_contract_control",
        "research_quality_assessed": False, "completed_current_slots": 10, "retained_initial_negative_slots": 8,
        "command": "python scripts/check_mcp_contract.py", "artifacts": str(base)}, indent=2), encoding="utf-8")
    print("PASS: v2 packaged MCP stdio, independent perspectives/audit/acceptance, preserved failure and negative results, rejected author clearance, source binding and stale delivery.")
    print("Retained control artifacts: " + str(base))


def main():
    destination = Path(os.environ.get("IRF_TEST_ARTIFACT_DIR", ROOT/"evals/runs"))
    destination.mkdir(parents=True, exist_ok=True)
    base = Path(tempfile.mkdtemp(prefix="mcp-contract-", dir=destination))
    asyncio.run(verify(base))


if __name__ == "__main__":
    main()
