# Research guide

[English](research-guide.md) | [简体中文](research-guide.zh-CN.md)

[Project overview](../README.md) · [Start research](quickstart.md) · [Installation and tools](usage-modes.md)

Research Toolkit is used by host agents to produce substantial, source-grounded research for an identified reader. The brief determines what must be explained and how deeply; the working methods and collaboration support that result.

## Example tasks

These are possible requests, not claims that each has been executed:

- **Industry report:** explain the 2026 agent market's important changes, competition and adoption barriers for strategy readers, with a requested scope and depth.
- **Company comparison:** compare named domestic and overseas companies across product, model, organization and strategy, retaining the development timeline.
- **Technical route research:** compare RAG, long context and hybrid routes under stated document, permission and deployment conditions.
- **Investment research:** explain category timing, defensibility, business model and counter-evidence, separating observed facts from investment assumptions.
- **Report update:** apply new sources or requirements to a saved report, preserving still-valid reasoning and explaining changed conclusions.

Simple fact queries, routine translation and a wording change often do not need a full research task. Long work benefits from explicit evidence, progressive arguments, substantive collaboration and independent assessment. A shorter deliverable can still require substantial underlying research.

## One connected research path

The [quick start](quickstart.md#research-from-scratch) shows the complete path. Four responsibilities organize the existing capabilities; they are not four agents or independent workflows.

| Responsibility | What it owns | What the next work receives |
| --- | --- | --- |
| Task and context | Current question, reader, requirements, outline, main artifact and dependencies. | Effective constraints, the specific question, related source and analysis references. |
| Evidence and analysis | Source reading, claim support, comparisons, calculations, mechanisms and competing explanations. | Full reasoning with sources, conditions, counter-evidence and unresolved questions. |
| Writing and revision | Meaningful argument units and a single owned main draft. | Coherent current prose, locatable citations and the original analysis behind it. |
| Review and delivery | Independent content perspectives, domain review, audit and final acceptance. | Located findings and independently checked corrections, then the complete accepted report. |

The lead retains the overall research question and makes cross-part decisions. Research agents perform actual production work; an explicitly assigned agent integrates the main draft. Every handoff preserves full artifacts and accessible originals. A brief summary tells the next worker what to read and continue; it is not a substitute for the original analysis.

Research progresses by dependencies. An unresolved comparison premise or calculation affects the argument that uses it; review that premise before propagating it. Independent research units can proceed together. The outline and draft develop with the findings, rather than imposing a single-shot report or a fixed number of paragraphs per round.

## Where the methods belong

Read the relevant method for the current action. This guide links to the normative originals instead of maintaining another copy of every rule.

| Need | Normative source |
| --- | --- |
| Entry and responsibilities | [SKILL](../SKILL.md) and [research standard](../references/research-standard.md) |
| Understanding the brief, outlining and developing arguments | [Research workflow](../references/research-workflow.md) |
| Choosing comparison, explanation, synthesis or recommendation methods | [Optional analysis lenses](../references/optional-analysis-lenses.md) |
| Writing for the reader and retaining meaning during revision | [Writing style](../references/writing-style.md) |
| Production delegation, independent review, audit and acceptance | [Agent roles and handoff](../references/subagents-and-review-loop.md) |
| Requirements, original materials and task resumption | [Task continuity](../references/task-continuity.md) |
| Completing the current deliverable | [Quality gates](../references/quality-gates.md) |
| Diagnosing a concrete failure | [Gotchas](../references/gotchas.md) and [postmortem lessons](../references/postmortem-lessons.md) |

The same sources serve lead agents, research workers, assembling agents and reviewers. A role reads what its task needs; it does not receive every method and developer instruction on each turn.

## Review and acceptance

Seven distinct independent contexts review requirements, evidence, adversarial reasoning, structure and depth, reader usefulness, process language and natural expression. Relevant domain expertise is assessed separately. A further independent auditor checks substantive reviews, consequential findings and passed-content samples; another independent agent accepts the current complete report after necessary corrections.

The auditor selects samples from the whole actual report and original inputs. Decisive requirements, claims, figures, sources, counter-evidence and consequential decisions are checked fully; other selections have reasons and locations. Problems lead to follow-up on the same source, measure, branch or transformation. This work belongs to audit and acceptance, without another sampling role.

The author may self-edit or explain a disagreement, but cannot replace independent review or close its own required findings. A negative review is retained and used to repair the actual report. Full details belong to the [role methods](../references/subagents-and-review-loop.md); CLI/MCP records are explained in [review completion](review-completion.md).

## Task records and continuation

Skill-only work retains useful original requirements, sources, analysis, drafts and review results in the host's available files or context. It need not reproduce fixed CLI/MCP registries. The substantive review responsibilities still apply.

Tool-managed work uses the existing source/claim records, task specification, requirement log, saved artifacts and review log. `status` supplies shared work inputs; `save` retains results and dependencies; `review` connects the host's independent assignments; `finish` writes the delivery receipt after current acceptance. The [usage guide](usage-modes.md) owns the concrete fields and calls.

Satisfied requirements remain visible when they still apply to later edits. A new instruction changes affected requirements and work, not unrelated original objectives. Old artifacts and receipts retain their original versions; continuation develops a new current result.

## What successful output contains

The answer addresses the reader's actual questions with evidence, explanation, meaningful comparison and appropriately scoped conclusions. It retains necessary conditions, counter-evidence and uncertainty. The final text is a reader-facing report; source-processing notes and handoff logs stay in the working material unless the user asks for them.

A source count, a full outline or a passed record check cannot replace the missing explanation in a draft. Existing mechanical tools locate record and version problems; the independent agents read the actual report and evidence. [Delivery checks](delivery-verification.md) explains the tool contract.

## Reports and retained evidence

- [APIs or browsers](case-study/api-or-browser/report.md), with [first draft, sources and review decisions](case-study/api-or-browser/README.md).
- [Domestic office-agent report](case-study/report.zh-CN.md), with its [source and revision archive](case-study/office-agents/README.md).
- [Research update case](case-study/coding-benchmark-update/README.md), retaining the older report and actual changed evidence.
- [Evaluation status](evaluation-status.md) separates actual studies, software checks and unmeasured effects. Earlier studies retain their own protocols, not the current default research contract.

The original reports, failed attempts and revisions remain available. Method reorganization and software behavior changes alone are not evidence of improved research quality.

## Repository and maintenance

`SKILL.md` is the shared entry; `references/` owns methods; `scripts/` provides shared CLI/MCP logic; `agents/` documents host integration; `docs/` provides usage and the website. `plugins/research-toolkit/` is generated from shared sources. `examples/` demonstrates interfaces, and `evals/` preserves research and relevant checks.

Maintenance and experimental execution instructions are in [Contributing](../CONTRIBUTING.md), [evaluation documentation](../evals/README.md) and [site maintenance](site-maintenance.md). They are not extra steps for every research task. [MIT license](../LICENSE).
