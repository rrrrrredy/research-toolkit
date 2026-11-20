RESEARCH IN PRACTICE

# New material, existing report: what actually needs to change?

A coding-agent procurement research case · Updates on 14–15 October 2026 · The reports are in Chinese.

An existing report asked what coding-agent leaderboards can support in a procurement decision. Research Toolkit was used to continue that work: revisit relevant sources, locate affected claims and revise the complete report while retaining the original evidence. The central recommendation remained: use leaderboards to select candidates, then test them on the buyer’s own work.

[Previous complete report](https://github.com/rrrrrredy/research-toolkit/blob/main/evals/studies/2026-10-14-native-agent/reports/toolkit/final.md) · [14 October update](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/report.zh-CN.md) · [15 October continuation](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/status-save-2026-10-15/report.zh-CN.md)

## From source checks to specific revisions

The table summarizes revisions; it is not a new benchmark result. The [reading notes](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/source-checks.md) retain source IDs and locators; the full report links to the original public sources.

| Previous report | Material checked | Revision in the report |
| --- | --- | --- |
| Discussed defective evaluation tasks without explaining this failure mechanism. | S2: OpenAI’s coding-evaluation audit, OpenLibrary-77c16d5. | Added the one-versus-two leading-space mismatch: an answer can follow the prompt and still fail the test. |
| Did not spell out the prerequisites for a valid SWE-Lancer run. | S6: official running instructions. | Added disabled internet access and Linux iptables; an online Mac trial is not an equivalent score. |
| Did not distinguish the different Pro V2 repair counts. | S9/S10: V2 announcement and repository instructions. | Separated 69 contradictory-instruction tasks from 529 rewritten statements, 214 test patches and 38 reference patches. These counts are not interchangeable. |
| Final control outcomes alone hid first-pass infrastructure failures. | New S11: V2 release-control record. | Separated final 642/642 control passes from three first-pass infrastructure failures per arm followed by successful reruns. |

## A real revision also introduced an omission

The first update dropped an existing explanation: differences between V1 and V2 scores cannot be read directly as model progress. Author-context self-review caught it. The next revision restored that explanation and moved the citation beside the 529/214/38 figures. The [first update](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/first-update.zh-CN.md), [needs_revision response](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/first-self-review.json) and [final pass](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/final-self-review.json) remain accessible.

## The next update: locate, read, then decide

On 15 October, saving two updated source records surfaced five linked claims and report locations. Reading them led to changes in three claims, not all five: the SWE-Lancer Manager monolith-image requirement, scoring of partial patches after the Pro V2 timeout, and a recommendation to separate shared setup from per-task costs. These were details already present in the sources, not newly published upstream changes.

[Previous version](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/status-save-2026-10-15/previous-report.zh-CN.md) · [Source checks](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/status-save-2026-10-15/source-checks.md) · [Actual save response](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/status-save-2026-10-15/calls/03-source-update.response.json) · [Changed records](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/status-save-2026-10-15/updated-records.json) · [Separate-context Astra review and repairs](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/status-save-2026-10-15/review/README.md)

## What this case establishes—and its limits

- The first update preserved the original task’s 50 files; the next preserved its 67 files. Existing source and claim IDs were reused. [First execution record](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/execution-summary.json) · [Continuation record](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/status-save-2026-10-15/execution-summary.json).

- Both continuations used Full/self in the author context. Later separate-context Astra reviews are archived separately; they are not CLI independent-backend receipts.

- No coding benchmark or complete model evaluation was rerun. There was no paired update-versus-rewrite experiment, so this case does not measure overall time saved or establish a general quality or cost advantage.

- Observed timings, response-byte measurements, repeated reads and missing usage data remain in the [original case record](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/README.md) and [follow-up record](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/status-save-2026-10-15/README.md). Response size is not overall token, time or monetary savings. The public archive is an evidence subset, not a portable complete task snapshot.

## Use this approach on your own report

Give your agent the existing report, relevant source material and the decision the report must support. Ask it to identify affected passages, reuse sound evidence, revise the complete report and return a short change note. Choose Lite or Full for the task and state the review actually performed.

[Continue existing research](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/usage-modes.md#continue-existing-research) · [Copy a research request](https://rrrrrredy.github.io/research-toolkit/#start) · [More cases](https://rrrrrredy.github.io/research-toolkit/case-study/)
