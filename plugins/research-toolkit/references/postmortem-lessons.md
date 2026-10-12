# Research Design Lessons

[English](postmortem-lessons.md) | [简体中文](postmortem-lessons.zh-CN.md)

These design lessons describe recurring research failure modes and the practices intended to address them. They are not measured estimates of the toolkit's effect.

## Continuity And Evidence

- Keep current state compact enough to recover the objective, open issues and next action.
- Separate sources, claims and uncertainty so important judgments can be traced and challenged.
- Write bounded sections when the task's depth requires focused analysis.
- Give review findings evidenced dispositions: correct confirmed defects in commissioned reports and explain no-change decisions for unsupported or optional suggestions. In evaluation work, preserve sample defects and use them to improve the toolkit.
- Integrate counter-evidence into the argument where it changes the conclusion.

## Common Failure Modes

- Expanding an article task into system design.
- Exposing backstage source labels, logs or workflow narration in finished prose.
- Treating one topic's analytical structure as a universal method.
- Reviewers repeating the author's assumptions without checking evidence.
- Treating large registries or passing file checks as proof of substantive depth.
- Declaring whole-task completion after a local milestone.
- Losing material follow-up requirements across turns.
- Adding lifecycle machinery that does not improve the deliverable or the accuracy of its status.

## Reader-Facing Quality

A research report needs a clear thesis, relevant evidence, enough detail for the question, explicit uncertainty, useful references and readable analysis. Its expected depth should be settled before drafting. Review the actual text against those requirements rather than relying on file counts or status labels.

## Lessons From The October Lite Pilot

These preserved outputs motivate method changes, not claims that the changes work. They come from different collection stages and must not be pooled into a new win rate.

- [DeepSeek banking memo, original pair 03](https://github.com/rrrrrredy/research-toolkit/blob/ce812f1b52564121212613d5bb6de281d079b8d0/evals/studies/2026-10-10-lite-four-models/runs/deepseek/coordinator/author/pair-03/with_toolkit/parsed.json): its report has 913 whitespace-separated words including headings, against a 600–800-word brief. Check actual length before delivery.
- [Kimi banking memo, format supplement pair 05, report B](https://github.com/rrrrrredy/research-toolkit/blob/ce812f1b52564121212613d5bb6de281d079b8d0/evals/studies/2026-10-10-lite-four-models/format-supplement/kimi/judge-inputs/pair-05.json): the opening claims high failure rates, although the complaint examples do not establish those rates. It also turns anticipated harms into outcomes and proposes a human-escalation ceiling without a rationale. Preserve source scope and modality; justify decision criteria and examine their incentives.
- [DeepSeek memory-safety memo, completion supplement pair 01](https://github.com/rrrrrredy/research-toolkit/blob/ce812f1b52564121212613d5bb6de281d079b8d0/evals/studies/2026-10-10-lite-four-models/completion-supplement/deepseek/authors/pair-01/with_toolkit/report.md): one paraphrase reverses the relationship between external dependencies and open source. It also treats missing external findings as preventing assessment of the vendor's own dependency risk. Check relationship direction and separate missing external evidence from internal evidence the decision-maker can obtain.

The corresponding practices are in [source and claim discipline](research-standard.md#8-source-and-claim-discipline), [writing style](writing-style.md#length-and-decision-usefulness) and the [Lite guide](lite-workflow.md). Assess their effect with a separately frozen comparison; keep the pilot inputs, outputs and judgments unchanged.

## Delivery Boundary

Research records support traceability; the finished report presents the argument and evidence useful to its reader. Neither layer substitutes for the other.

Current requirements, whole-report review, accepted limitations, artifact hashes and the delivery statement must agree. A partial artifact can be delivered with an accurate scope. Evaluation completion depends on the frozen evaluation requirements and preservation of results; it does not require repairing every evaluated report.
