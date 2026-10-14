# Complete workflow (Full): research, review and delivery

[English](quickstart-full.md) · [简体中文](quickstart-full.zh-CN.md) · [Research Toolkit](../README.md)

Full shares the research baseline with [Lite](quickstart-lite.md). Choose Full when you need to track changing requirements/evidence and retain version-bound reviews, revision decisions and delivery checks. Lite also handles complex comparisons and conflicting evidence; choose from the workflow needed, with length secondary. [Continue existing research in Full](usage-modes.md#continue-existing-research).

Give the request below to an agent that can read files and research sources. Full covers the brief, source research, analysis, section drafts, review and revision; MCP is an optional tool for managing task state. See the results: [APIs or browsers](case-study/api-or-browser/report.md) · [Office agents in China](case-study/report.zh-CN.md).

## 1. Copy the request and begin

This example is ready to start. For your own question, also change the audience, scope, available material and length.

```text
Use Research Toolkit. Read SKILL.md and choose profile=full:
https://github.com/rrrrrredy/research-toolkit

Write an English decision report for the product and technical leads
of an enterprise knowledge assistant: when should they choose RAG,
long context, or a hybrid?
Cover document updates, permissions, citation location, answer quality,
latency and cost. Read original papers and technical documentation
available as of execution, recording the information cutoff.
Treat unspecified organization size, budget and deployment requirements
as assumptions to verify, and make conditional recommendations.
Deliver final.md with 3000–4000 whitespace-delimited words across the
whole file, including headings, Markdown, citations and references.

Establish the brief and outline, research and read sources, and register
sources and important claims. Develop evidence, comparisons and
counterevidence by section, with concrete recommendations and first steps.
Prefer an available separate review context; Astra can provide this review.
If none is available and independent review is not required, use self-review
and label it. Fix concrete findings and recheck affected content, then deliver
the complete report. Retain source/claim records, review findings and revisions
separately. Cite source titles and URLs in the report.
Use CLI/MCP for progress, counts and delivery when connected; otherwise
apply the research methods directly.
```

3000–4000 words is this example's agreement, not a universal Full minimum. Use existing questions and material directly; clarify only gaps that affect the research. If the agent cannot read GitHub, supply `SKILL.md` and the required references from a [downloaded copy](https://github.com/rrrrrredy/research-toolkit/archive/refs/heads/main.zip).

## 2. Use your existing agent

| Route | Shortest path |
| --- | --- |
| Codex: methods directly | Open or provide the repository files and send the request. Research with the agent's existing retrieval, file and context capabilities; MCP installation is optional. |
| Cursor: local MCP | Follow the [virtual environment setup](usage-modes.md#connect-mcp-separately), merge the [README configuration](../README.md#use-as-an-mcp-server) into `.cursor/mcp.json`, confirm the seven `research_*` tools appear, then send the request. |

Other agents can read the same methods through files, links or text; see [agent setup](../agents/README.md). Client configuration references: [Codex MCP](https://developers.openai.com/codex/mcp) · [Cursor MCP](https://cursor.com/docs/mcp).

Choose review at the start using the capabilities already available:

- **A fresh host context:** supply the task, complete report and necessary sources to Astra or another available reviewer. Return its findings to the author for revision. No outside person or different model vendor is required.
- **Automated CLI/MCP review:** configure the existing `codex`, `claude` or compatible endpoint backend. `research_review` retains inputs, responses and version bindings; see [backend setup](usage-modes.md#reviewer-backends).
- **Self-review:** new Full tasks without a backend default to explicitly labeled self-review. Complete independent review when the task requires it.

A host-session review can serve the methods-only workflow; it does not automatically become a CLI/MCP review record. When using local tools to manage delivery, run the configured backend for those records.

## 3. Deliver the complete work

Return the complete report, source/claim records, review findings and revisions. The report should contain evidence-backed comparisons, specific conclusions and their conditions; citations should remain usable in the exported document. Keep workflow records separate from the reader's report.

With local tools, use `research_check_draft` to measure length before review. After repairing the draft, complete review of the current version and call `research_finish`. This follows the existing Full workflow.

<details>
<summary>Optional: create a local task and length record with the CLI</summary>

From the repository root, use Python 3.10+; the CLI needs only the standard library, without MCP dependencies. Use `python3` on Linux/macOS, or `py -3` or an installed interpreter path on Windows.

```bash
python3 scripts/research_workflow.py start --profile full --workspace ../research-work --request examples/full/start.en.json
```

This creates `../research-work/knowledge-assistant-full-en`. The agent performs retrieval, reading and section writing; the command creates the task. If you change the example question, update the request file's `brief` too. Resume existing tasks with `status`.

Add the single line from [requirements.en.jsonl](../examples/full/requirements.en.jsonl) to the new task's `state/requirements.jsonl`, retaining any other requirements. Start as `pending`; mark it `satisfied` only after checking. Before review, call `check-draft` with this task ID; see [copyable length records and checks](delivery-verification.md#explicit-length-requirements).

Use the [CLI capture and reuse example](usage-modes.md#reuse-task-files-and-retain-a-self-review-packet) for a self-review packet, and the [CLI/MCP instructions](usage-modes.md) for other tiers and delivery. The example does not prefill a report or a review.

</details>

For bounded work where author checks fit the use, choose the [Lite walkthrough](quickstart-lite.md).
