# Start research with the complete methods

[English](quickstart.md) · [简体中文](quickstart.zh-CN.md) · [Research Toolkit](../README.md)

Use one research entry for long reports, substantial revisions and continuing updates. The host agents use the methods for their current work; Toolkit connects the requirements, source material, analysis, writing and independent assessment. CLI/MCP task management is optional.

## 1. Copy the request and begin

Describe the question, audience, intended use, available material and explicit constraints. The agents organize the work; users do not need to schedule its steps.

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

Explain route differences and selection reasons, with concrete
recommendations and first steps. Cite source titles and URLs.
```

The word range belongs to this example, not every research task. Use existing context to infer the purpose and ask only about consequential gaps. If GitHub is unavailable, provide `SKILL.md` and its references from a [downloaded copy](https://github.com/rrrrrredy/research-toolkit/archive/refs/heads/main.zip).

## 2. Use your existing agent

Choose the [entry](../README.md#which-should-i-use) your host supports:

- **Skill:** supply the repository or install the Skill; use the host's research and subagent capabilities. No fixed CSV/JSONL records are required.
- **Plugin:** install the [package](usage-modes.md#install-the-plugin), reopen the session and select Toolkit. The Skill and MCP are included.
- **MCP:** connect the [local server](usage-modes.md#connect-mcp-separately) and make the same Skill available.
- **CLI:** use Python 3.10+ and `scripts/research_workflow.py`; MCP dependencies are unnecessary.

Codex, Claude Code and other capable hosts run their own research and review agents. No separate API setup is needed for these host-native tasks. The same model can serve different independent contexts. [Host setup](../agents/README.md) explains installation; [review completion](review-completion.md) explains native assignments and retained responses.

### Research from scratch

| Work | What the agents do | With CLI/MCP task management |
| --- | --- | --- |
| Understand and outline | Retain the user's original questions and constraints; establish an outline and meaningful research units with real dependencies. Assign researchers, a main-draft owner and independent review responsibilities. | `start` creates a task; `status` recovers existing work, effective requirements and the current outline. |
| Investigate and analyze | Research agents read originals, compare, calculate and explain their assigned questions. The lead continues synthesis and resolves cross-unit questions. | `status.work` supplies relevant records and original material; `save` retains sources, claims and substantial analysis. |
| Develop and hand off | Complete an analysis or argument unit, including its support, conditions and unresolved questions. Independent review examines important premises before dependent work relies on them. | Save the result and its actual host reference, input bindings and handoff; read the original result when integrating it. |
| Assemble progressively | The designated assembling agent reads branch arguments and originals, reconciles definitions and connections, and grows one main draft. New findings update affected units and the outline. | Keep branches separate; explicitly register the main artifact. `status` exposes dependencies and changed inputs for continuation. |
| Review the whole report | Seven distinct independent agents cover the base perspectives, with relevant domain review. Each reads the complete current report and necessary originals. | `review` prepares the host assignments and retains each actual response and input version. |
| Audit and revise | A separate auditor checks review validity, decisive claims and consequential decisions, and samples passed content from the full report. Authors repair necessary defects; affected work is re-examined. | Use the same `review` operation for the auditor's original result; preserve earlier negative results and revisions. |
| Accept and deliver | A separate acceptance agent reads the current whole report, effective requirements, audit and corrections. Deliver after necessary work is complete. | `finish` checks the accepted current version and writes the receipt; it does not replace the independent acceptance. |

MCP tools use the `research_` prefix; CLI uses the corresponding subcommand. Use one interface for an operation. Skill-only work follows the middle column using the host's files, conversation and source material; it has the same independent content responsibilities without reproducing the tools' record formats.

For the knowledge-assistant question, research can be split among document updates and permissions, route-quality comparisons, and the calculation of a stated workload. The outline preserves every requested dimension; a separate assembling agent connects these results into a decision. Early review examines the comparison's assumptions and calculation method before later conclusions depend on them. Final whole-report reviewers see the assembled argument, not just branch summaries.

If the user adds “private deployment is required,” retain the original permission, quality and cost questions. Send the effective change to affected work, revise its analysis and then the main report. A satisfied requirement remains active when it still constrains the answer. Previously completed reading is reused, with original text available for changed or disputed points.

### Revise or update a report

1. Supply the current report, relevant sources and change request. For an update, supply new material or authorize research and specify the cutoff.
2. Read the current requirements, report and affected sources. Preserve still-valid explanations and change the claims, conditions or recommendations affected by the new evidence.
3. Retain the original and hand revised analysis to the main-draft owner. Complete current-version content review, independent audit and final acceptance, then deliver the complete report and a short change note.

Managed tasks resume with `status`, without another `start` or reconstructing unaffected records. A 1.x completion receipt remains historical; continued work adopts the current completion contract while reusing its materials. See [continuation calls](usage-modes.md#continue-existing-research), [compatibility](compatibility.md) and the [retained update case](case-study/coding-benchmark-update/README.md).

## 3. Deliver the complete work

Return the requested report with usable citations and, for revisions, a short change note. Keep raw research, review and execution records available for continuation; they need not occupy the reader-facing article. The report should contain the analysis, comparisons and conditions the task requires.

Tool-managed work uses `research_finish` after independent acceptance of the current version. It writes the delivery receipt; agents do not prepare a duplicate receipt by hand. Optional `research_check_draft` helps inspect mechanical draft issues, but is not content review.

<details>
<summary>Optional: create a local task with the CLI</summary>

From the repository root, use Python 3.10+:

```bash
python3 scripts/research_workflow.py start --workspace ../research-work --request examples/full/start.en.json
```

This creates `../research-work/knowledge-assistant-en`. The directory name is retained for existing links; it uses the unified entry. Edit the example's `brief` for a different question. Existing tasks resume through `status`. Record an explicit word range through `save.requirements` only when the task has one; the [saving guide](usage-modes.md#save-research-records-and-drafts) shows the fields. [Native review requests](usage-modes.md#reuse-task-files-and-retain-a-review-packet) retain the actual original responses.

</details>
