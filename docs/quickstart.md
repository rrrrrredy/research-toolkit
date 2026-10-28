# Start research with the complete methods

[English](quickstart.md) · [简体中文](quickstart.zh-CN.md) · [Research Toolkit](../README.md)


Give the request below to an agent that can read files and research sources. The methods cover the brief, source research, analysis, section drafts, review and revision; MCP is an optional tool for managing task state. See the results: [APIs or browsers](case-study/api-or-browser/report.md) · [Office agents in China](case-study/report.zh-CN.md).

## 1. Copy the request and begin

Describe what you want researched, who it is for, why it is needed, and any available material or explicit constraints. You need not write execution steps for the agent. The selection example below has established requirements; keep the conditions your own task needs rather than filling in as many fields.

```text
Use Research Toolkit. Read SKILL.md:
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

Explain the differences and reasons for choosing a route, with concrete
recommendations and first steps. Cite source titles and URLs in the report.
```

3000–4000 words is this example's agreement, not a universal research minimum. Use existing questions and material directly; clarify only gaps that affect the research. If the agent cannot read GitHub, supply `SKILL.md` and the required references from a [downloaded copy](https://github.com/rrrrrredy/research-toolkit/archive/refs/heads/main.zip).

The Skill guides the agent to infer purpose from context, retain requirements and ask when needed; the host agent performs that interpretation. CLI/MCP saves the requirements it assembles and reports missing fields. It does not choose the research purpose for the user or establish understanding merely because fields are filled. Users supply consequential decisions that depend on their needs.

## 2. Use your existing agent

Use the [README selection table](../README.md#which-should-i-use) and configure only the entry you need:

- **Skill:** provide the repository or install the Skill, then send the request. No tool commands or fixed registries are required.
- **Plugin:** follow the [plugin instructions](usage-modes.md#install-the-plugin), reopen the session and select Toolkit. It includes the Skill and MCP; do not install a second MCP service.
- **MCP:** follow the [local MCP setup](usage-modes.md#connect-mcp-separately), confirm the nine `research_*` tools appear, and give the agent access to the same Skill.
- **CLI:** download the repository and use Python 3.10+ to invoke `scripts/research_workflow.py`. A task-creation example is below; see the [CLI instructions](usage-modes.md#skill-only-and-cli-fallback) for the commands.

Retrieval, browsing sources and writing use the agent's existing capabilities. Host-specific locations and setup for Codex, Cursor and other agents are in [agent setup](../agents/README.md).

Choose review at the start using the capabilities already available:

- **A fresh host context:** supply the task, complete report and necessary sources to Astra or another available reviewer. Return its findings to the author for revision. No outside person or different model vendor is required.
- **Automated CLI/MCP review:** configure the existing `codex`, `claude` or compatible endpoint backend. `research_review` retains inputs, responses and version bindings; see [backend setup](usage-modes.md#reviewer-backends).
- **Self-review:** new tasks without a backend default to explicitly labeled self-review. Complete independent review when the task requires it.

A host-session review can serve the methods-only workflow; it does not automatically become a CLI/MCP review record. When using local tools to manage delivery, run the configured backend for those records.

### Research from scratch

The knowledge-assistant question above illustrates the steps. The user supplies needs, material and necessary decisions; the agent performs the work. These are not instructions for the user to supervise each step.

| Step | What the agent actually does | If CLI/MCP task management is selected |
| --- | --- | --- |
| 1. Understand the brief | Establish the reader, comparison conditions, material and deliverable; clarify only consequential gaps. | Create a local task with `research_start` / CLI `start`; use `status` for an existing task. |
| 2. Read and analyze | Read original sources, compare the specified update, permission, quality and cost questions, and explain differences and conditions with support and counterevidence. | Use `save` for sources, judgments and requirements actually used; a registered URL is not reading. |
| 3. Draft | Organize around the questions, develop comparisons and reasoning, and give conditional recommendations with locatable citations. | Use `save` for drafts and register the main artifact. Use `guide` only when the method is not already available. |
| 4. Check and revise | Read the current full report, check requirements, support and argument, complete agreed self-checks or reviews, and repair concrete defects. | Run the selected `review`; optional `check-draft` does not replace reading the report. |
| 5. Deliver or continue | Deliver the current result; if unfinished, retain effective requirements, the draft and remaining work, then resume from there. | Use `finish` for completion and `status` for resumption. Tools maintain their existing records. |

MCP names use the `research_` prefix (for example `research_save`); CLI uses the corresponding subcommand. Do not call both interfaces for the same step. Skill-only work follows the middle column using available conversation, material, citations or existing notes, without adopting the right column's record formats.

### Revise or update a report

1. Supply the current report, related sources and requested change. For an update, supply new material or authorize research and specify the required cutoff. If only the report is available, establish what can be checked.
2. The agent compares effective requirements, the draft and affected sources, identifies which facts, conditions or inferences change, and preserves analysis that still holds. A changed source does not automatically invalidate a conclusion.
3. Save the revision separately, check changes and affected reasoning, complete agreed checks, and deliver the complete current report with a short change note.

For a saved managed task, resume with `status` and update affected records with `save`, without another `start`. Skill-only work reuses the report and material directly; no historical ledger must first be reconstructed. See [continuation requests and tool details](usage-modes.md#continue-existing-research) and the [executed update case](case-study/coding-benchmark-update/README.md), which retains the original report, source changes and revisions.

## 3. Deliver the complete work

Return the requested report with usable citations and, for a revision, a short change note. Include supported comparisons, specific conclusions and their conditions; citations should remain usable when exported. Registries, raw reviews and tool receipts are attachments only when the task needs them, not mandatory deliverables for every report.

For tool-managed tasks, complete current-version review under the existing contract, then call `research_finish`. Optional `research_check_draft` can help inspect the draft and explicit length requirements; it is not an additional mandatory step.

<details>
<summary>Optional: create a local task and length record with the CLI</summary>

From the repository root, use Python 3.10+; the CLI needs only the standard library, without MCP dependencies. Use `python3` on Linux/macOS, or `py -3` or an installed interpreter path on Windows.

```bash
python3 scripts/research_workflow.py start --workspace ../research-work --request examples/full/start.en.json
```

This creates `../research-work/knowledge-assistant-en`. The example directory retains its old name for existing links; the request uses the unified entry. The agent performs retrieval, reading and section writing; the command creates the task. If you change the example question, update the request file's `brief` too. Resume existing tasks with `status`.

The agent saves the agreed length through `research_save` / CLI `save` using `requirements`; users do not edit JSONL. Start pending, then submit an evidenced satisfied update after checking. See the [record-saving example](usage-modes.md#save-research-records-and-drafts).

Use the [CLI capture and reuse example](usage-modes.md#reuse-task-files-and-retain-a-self-review-packet) for a self-review packet, and the [CLI/MCP instructions](usage-modes.md) for other tiers and delivery. The example does not prefill a report or a review.

</details>

