# Documentation

[English](README.md) · [简体中文](README.zh-CN.md) · [Research Toolkit](https://github.com/rrrrrredy/research-toolkit/blob/main/README.md)

[Quick install](quickstart.md) · [Browse English documentation](en/README.md)


- [Current long-research cases](case-study/long-research-2026-11/index.html): microdrama markets and test-time compute, with independently authored English and Chinese reports.
- [Long-research benchmark](https://github.com/rrrrrredy/research-toolkit/blob/main/evals/README.md): 13 questions, 15 report assignments, execution instructions and located judgments.


## Use Research Toolkit

- [Start research](conduct-research.md): one complete entry for long-form research, in-depth analysis, revision and updates.

- [Usage and integration](usage-modes.md): repository, file, and text inputs; optional Skill, plugin, and MCP; review configuration.
- [Use with your agent](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README.md): common input methods, chat-only limits, and tool-specific setup.
- [Updating an installation](installation-versioning.md): choose and replace the intended package copy.

## Find methods for the current work

These are on-demand entry points within one study, not a reading list to finish at startup.

| What you are doing | Where to read |
| --- | --- |
| Understand the request and plan depth | [Research requirements and depth planning](https://github.com/rrrrrredy/research-toolkit/blob/main/references/research-workflow.md); the [research guide](research-guide.md) introduces first use. |
| Read material, compare and explain | [Sources and claims](https://github.com/rrrrrredy/research-toolkit/blob/main/references/research-standard.md#8-source-and-claim-discipline) · [Choose analysis methods by question](https://github.com/rrrrrredy/research-toolkit/blob/main/references/optional-analysis-lenses.md) |
| Delegate research and receive usable results | [Research production and handoff](https://github.com/rrrrrredy/research-toolkit/blob/main/references/subagents-and-review-loop.md#research-production-and-handoff) · [Shared context and actual requests](usage-modes.md#research-delegation-and-handoff) |
| Write, assemble and revise a complete report | [Writing style](https://github.com/rrrrrredy/research-toolkit/blob/main/references/writing-style.md) · [Assembly](https://github.com/rrrrrredy/research-toolkit/blob/main/references/research-workflow.md#9-assembly) |
| Resume work or apply new requirements | [Task continuity](https://github.com/rrrrrredy/research-toolkit/blob/main/references/task-continuity.md) · [Current artifact and scope updates](usage-modes.md#current-artifact-and-scope-updates) |
| Complete independent review, audit and acceptance | [Review methods](https://github.com/rrrrrredy/research-toolkit/blob/main/references/subagents-and-review-loop.md#assign-work-by-perspective) · [Completion conditions](https://github.com/rrrrrredy/research-toolkit/blob/main/references/quality-gates.md); tool record details are under “Reviews and evaluation” below. |

Consult [recurring research problems](https://github.com/rrrrrredy/research-toolkit/blob/main/references/gotchas.md) when a specific problem arises; no separate workflow is needed.

## Reports and cases

- [November English report](case-study/api-or-browser-2026-11/report.md) and [complete archive](case-study/api-or-browser-2026-11/README.md): current API/browser research, original drafts, analyses and independent reviews.
- [November Chinese report](case-study/office-agents-2026-11/report.md) and [complete archive](case-study/office-agents-2026-11/README.md): the six-product office-agent study, refreshed to 5 November.

- [Updating an existing research report](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/): Old report, new source checks, concrete revisions and retained limits.

- [APIs or browsers for AI agents](case-study/api-or-browser/report.md): original English research on action coverage, completion, recovery, and cost.
- [English case archive](case-study/api-or-browser/README.md): initial and final manuscripts, English source and claim records, complete reviews, and the revision decision.
- [Office agent research in China](case-study/office-agents/README.md): the historical Chinese case and its retained [English translation](case-study/report.en.md).

## Reviews and evaluation

- [Review completion](review-completion.md): complete inputs, version binding, valid responses, and failure recovery.
- [Delivery checks](delivery-verification.md): current artifacts, unresolved requirements, and completion conditions.
- [Failed checks and repairs](failure-handling.md): source-based corrections, draft preflight, PR acceptance and stopping rules.
- [Report evaluation standard](report-evaluation-standard.md): separate manuscript quality, delivery readiness, and toolkit-effect studies.
- [Necessary-defect labels](necessary-defects.md): stable categories, evidence-based dispositions and a versioned diagnostic index.
- [Evaluation suite](https://github.com/rrrrrredy/research-toolkit/blob/main/evals/README.md): tasks, controls, fixtures, diagnostics, and offline checks.
- [Evaluation status](evaluation-status.md) and [roadmap](evaluation-roadmap.md): available evidence and open evaluation work.
- [Evaluation data audit](evaluation-data-audit.md): what the public datasets contain and support.
- [Source extraction](source-extraction.md): provenance and retained source text.

## Development

Directories retain their content roles; shared implementations connect the research responsibilities:

| Location | What it maintains |
| --- | --- |
| `SKILL.md` and `references/` | One entry, research standards and on-demand methods. |
| `scripts/` | Shared CLI/MCP logic: `task_context.py` assembles work inputs, `research_records.py` saves records and outputs, and `research_workflow.py` connects research, native-agent review and delivery operations. |
| `docs/` and `agents/` | Usage, website and agent tool integration; agent tools run agents and carry messages. |
| `plugins/research-toolkit/` | Package contents generated from shared sources, without a separate method set. |
| `examples/` and `evals/` | Request examples, research records and relevant checks; historical evidence stays intact. |

- [DSH adapter maintenance](dsh-adapter-validation.md): existing loading checks, separate from normal research.
- [Website discovery and maintenance](site-maintenance.md): static build, static page checks, deployment verification, measurement boundaries and owner setup steps.

[Historical improvement plans](improvement-plan.md): earlier priorities, study designs and their recorded outcomes.

[Contributing](https://github.com/rrrrrredy/research-toolkit/blob/main/CONTRIBUTING.md) · [Changelog](https://github.com/rrrrrredy/research-toolkit/blob/main/CHANGELOG.md) · [Plugin package](https://github.com/rrrrrredy/research-toolkit/tree/main/plugins/research-toolkit) · [Scripts](https://github.com/rrrrrredy/research-toolkit/tree/main/scripts) · [MIT license](https://github.com/rrrrrredy/research-toolkit/blob/main/LICENSE)
