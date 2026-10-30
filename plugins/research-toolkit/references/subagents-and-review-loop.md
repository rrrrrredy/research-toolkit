# Subagents and Review

[English](subagents-and-review-loop.md) | [简体中文](subagents-and-review-loop.zh-CN.md)

This reference owns production handoff, independent content review, audit and final acceptance. Read the part needed for the current assignment. The host provides subagent execution; Toolkit supplies the research inputs, methods and versioned artifacts.

<!-- method:delegate -->
## Research production and handoff

Use the host's native subagents when the question has work that can be owned and advanced separately. Start those assignments as soon as their boundaries and initial inputs are clear, while the lead continues research and coordination. No separately configured API is required for native delegation.

The lead owns the original question, effective requirements, overall outline and cross-part decisions. Workers can investigate sources, calculate, compare, challenge explanations, develop local arguments and write sections. Assign whole-report assembly to a named writer, who may be the lead or a separate production agent. Only that writer edits the main report; other workers save distinct contributions. The lead remains responsible for the final research judgment even when assembly is delegated.

Assign work by the actual question and dependencies. Preserve coverage dimensions alongside analytical responsibilities: for a domestic/overseas study, name which researcher covers each geography and required company, and who compares their mechanisms. Dividing by mechanism must not silently drop geographic coverage; dividing by geography must not leave cross-company explanation unowned. Give each assignment the current question, relevant original requirements and corrections, outline context, readable sources and previous analyses, expected output, and the work that depends on it.

Progress through research units rather than waiting to produce the whole report at once. A unit can be a comparison, calculation, case, mechanism or connected argument. Its owner develops evidence and reasoning into usable analysis or prose. Before dependent units rely on a consequential result, give the relevant independent reviewer the premise, evidence and current output. Unrelated units can proceed concurrently. The lead updates the outline and dependencies when a new finding changes the research; the assembler integrates ready contributions without flattening their analysis.

### Handoff that preserves the work

Return the substantive output, its original evidence and relevant locations, conditions and assumptions, unresolved issues, and a short account of what the next owner can use or must resolve. Link full calculations and arguments rather than replacing them with status messages. Keep the previous version when revising a saved artifact.

Handoff applies from researcher to researcher, researcher to assembler, author to reviewer, reviewer to reviser, and one agent's completed phase to its next phase. Continuing in the same context can reuse the existing artifact and current notes; transferring to another context must make them accessible there. Send changed requirements and inputs explicitly. A spawn-time snapshot does not contain later corrections automatically.

When a context is compressed or replaced, preserve the effective requirements, outline, completed conclusions and their conditions, pending decisions, current artifacts and original-material locations. The short handoff is a navigation aid. The receiver reads the full relevant output and sources before relying on them; original texts and raw review replies remain accessible. Do not reconstruct missing history or overwrite originals with their summaries.

With CLI/MCP, use existing `status.work` to select requirements, claims, sources and files and retrieve `work_context`; use `methods` for the relevant guidance. `save` with `draft.kind="analysis"` registers a contribution; `based_on` binds the provided inputs and `host_task` records its real executor. Unit/dependency and handoff information belongs with that contribution, not in a parallel task-management system. See [the request interface](../docs/usage-modes.md#research-delegation-and-handoff). Skill-only work preserves the same substance in existing host conversations and files.

The host manages launching, waiting, messages, cancellation and recovery. Retain actual task/session references. Continue unaffected work while branches run; await results before dependent work consumes them. A saved contribution marks local progress, not its integration, independent review or whole-task completion. A production context cannot review its own work as an independent reviewer.
<!-- /method:delegate -->

<!-- method:review -->
## Assign Work by Perspective

Every complete research delivery requires the following seven base perspectives, each in a different context separate from every production agent. Add domain review for the specialized claims the task makes. Use native host subagents; author self-checks do not replace these assignments. Independence concerns the context and production role, not a different vendor or outside person.

| Perspective | Method and required output |
| --- | --- |
| Intent and requirements (`requirements`) | Read the original request and effective corrections. Match important questions, required objects and constraints to actual passages or tables; identify missing answers, scope drift and instructions lost in revision. Do not invent requirements or protect the intended thesis from contrary evidence. |
| Evidence and data (`evidence`) | Check consequential claims against original sources, dates, versions, populations, units, denominators and calculations. Distinguish facts, source claims and inference. State actual reading coverage; access metadata and a source summary do not prove that the original was read. |
| Adversarial reasoning (`adversarial_reasoning`) | Challenge central conclusions with relevant counterexamples, alternative explanations, selection effects and missing assumptions. Explain the consequence for the argument; do not manufacture objections or require a finding quota. |
| Structure and depth (`structure_and_depth`) | Check how questions, outline, sections, evidence and synthesis form the answer. Locate missing mechanisms, incomparable measures, compressed reasoning and source repetition. Apply the task's expected depth, not a universal structure or length. |
| Reader usefulness (`reader_usefulness`) | Read the assembled text for its intended use: title and opening, argument continuity, introduced terms, tables, timelines and useful implications. Identify concrete understanding or decision problems. |
| Process-language removal (`process_language`) | Locate production logs, internal paths/IDs, review status and assistant dialogue in reader-facing prose. Retain methods, source attribution, uncertainty and operational details that the reader's question needs. |
| Natural expression (`natural_expression`) | Locate empty abstractions, repetitive caveats, vague actors, obstructive syntax and needless repetition. Explain the reading problem and a suitable remedy. Preserve facts, qualifiers, analytical depth and the user's style preferences; do not impose phrase bans or AI-detection targets. |
| Domain specialist | Apply the actual field's criteria: technical baselines and experimental conditions, financial assumptions, policy applicability, clinical populations or other specialized reasoning. State the domain and claims examined. Use a separate non-author context for the domain assignment. |

Each reviewer receives a fresh assignment context and reads the complete current report, original request and effective changes, and the original evidence relevant to the assignment. Do not seed it with the author's self-rating, other initial reviewers' judgments, expected scores or a preferred review result. Relevant substantive research analyses remain available. A local premise review names its limited scope and cannot substitute for the final whole-report perspective. Review the artifact in its delivery format, including portable citations and table/figure meaning.

## Shared Assignment

Provide the question, reader, effective requirements, actual artifact and input versions, original-material access, assigned perspective and required output. The reviewer reports what was examined, locatable observations and their basis. Each finding identifies its location, applicable requirement, evidence, impact and severity, separating required corrections from optional preferences. When no defect is found, explain the supporting checks instead of returning a generic PASS.

Reviewers remain read-only. Keep original replies and observable execution identities separate from any structured extraction or author response. Skill-only work can retain them in the host conversation or existing files; managed work uses the [review record interface](../docs/review-completion.md). Do not fabricate a missing session identity or source access.

## Complete Every Required Review

A complete review addresses its actual scope and version with substantive observations. Empty, truncated, wrong-version or generic replies leave the assignment open. Preserve failed attempts, correct the missing input or execution problem and resume that assignment. When required material exceeds one context, retain it in accessible originals and arrange complete scoped reading and synthesis, rather than silently replacing it with a summary.

Keep the first valid result for a given input and artifact version. A negative finding is a completed review, not a reason to rerun for a better verdict. An isolated mistaken finding is adjudicated; it does not invalidate the entire review. The auditor determines consequential invalidity and contested no-change decisions from the evidence. A reviewer who never received required material has incomplete work; an examined source that leaves an answer uncertain may support a complete, qualified assessment.

Authors apply necessary fixes and can explain why they disagree with a finding. They cannot approve their own work, dismiss a necessary correction or relabel an incomplete review as complete. Preserve findings and responses for the independent audit. Revisions go back to the affected reviewer with the current complete artifact and relevant changes; unchanged evidence remains available and prior results stay bound to their actual version.
<!-- /method:review -->

<!-- method:audit -->
## Check Reviewers and Sample Passed Work

Every complete research task has an explicitly assigned audit context separate from production and content reviewers. The auditor receives the complete report, effective requirements, original sources, contributions, raw reviews and revision/disposition evidence. Review validity and report readiness are separate judgments: a valid negative review can describe a report that still needs correction.

Check each required review for its actual execution and input version, assigned coverage, locatable observations, supported claims and absence of invented requirements. Inspect all consequential findings and disagreements, including decisions to leave text unchanged. Resolve them against original evidence and actual prose, not majority votes or average scores. Preserve each original finding with one evidenced disposition: confirmed defect, no change, unresolved or resolved. A claimed repair is resolved only after examining the changed text and affected context.

Audit all important requirements, decisive claims, key figures and citations, consequential counterevidence, major findings and necessary fixes. Also examine material marked passed or carrying no finding, including transformations from a worker's analysis into the report. The auditor chooses these samples from the complete artifact, not from an author's selected highlights.

For this additional sampling, retain the relevant population or report scope, selected locations, selection reasons, source checks and results in the existing audit output. Choose passages across relevant sections, evidence types and transformations; do not use a fixed percentage or first/last/hash-selected paragraphs as the default. A targeted sample is described as targeted, not random. When a discrepancy appears, check the same source, measure, branch or reasoning pattern wherever it affects the result; record that expansion and its outcome.

The auditor can request missing work from the existing researcher or reviewer and continue the same audit after repair. Necessary defects and unsupported important no-change decisions remain open. Evidence that genuinely cannot settle a research question is reported at the affected conclusion; it does not erase a missing mandatory reading or review assignment. Sampling is part of this audit and final acceptance, not a separate agent, score or approval process.
<!-- /method:audit -->

<!-- method:acceptance -->
## Stage Scheduling and Acceptance

1. **Outline and first premises:** the lead plans questions, coverage and dependencies; the requirements and structure reviewers examine the outline before extensive dependent writing. Evidence/domain reviewers examine consequential premises and calculations as they become usable. Early local checks are retained as local checks.
2. **Developing research units:** researchers produce evidence-backed arguments progressively. Resolve a premise that could change dependent work before treating it as settled; other independent units continue. The assembler updates the whole-report argument as contributions arrive and the outline changes.
3. **Complete report:** all seven base perspectives and applicable domain review read the complete report. Reader and expression findings are applied without losing facts or depth. The independent audit examines the reviews, important findings, necessary repairs and selected passed content.
4. **Final acceptance:** a further context, separate from production, content review and audit, reads the complete current report against the effective requirements. It examines the audit, dispositions and the actual current text, checks all important requirements and necessary fixes, and selects additional passed content where needed to judge integration. It reports acceptance or the exact remaining work. Its PASS cannot replace a missing required review or audit.

The final acceptance agent verifies the delivered version, source/condition preservation, complete required coverage, developed analysis and reader usability. Cross-part contradictions or lost qualifications return to the responsible production/review assignment, with the affected scope and inputs. Keep the original findings and prior artifacts. Do not let a coordinator's summary stand in for this reading.

Reader-ready delivery requires resolved necessary corrections, complete independent assignments and acceptance of the current whole report. A stage artifact may be delivered with its actual unfinished scope. Historical and evaluation artifacts retain their original defects and labels; keeping them as evidence does not certify them under the current completion contract. Once the agreed result and required work are complete, optional preferences do not restart unchanged reviews.
<!-- /method:acceptance -->
