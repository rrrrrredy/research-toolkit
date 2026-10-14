# Updating an existing long research report

[English](README.md) | [简体中文](README.zh-CN.md)

On October 14, 2026, we continued the existing Chinese report on what coding-agent leaderboards support in procurement. The update adds distinguishing evidence and operational prerequisites, delivering a complete report of 3,839 nonwhitespace characters. It uses Full/self in the current author context. No complete model evaluation or coding-benchmark execution was rerun.

[Updated final](report.zh-CN.md) · [First update](first-update.zh-CN.md) · [Previous final](../../../evals/studies/2026-10-14-native-agent/reports/toolkit/final.md) · [Original first draft](../../../evals/studies/2026-10-14-native-agent/reports/toolkit/first-draft.md)

## Source checks that changed the report

| Actual check | Omission addressed |
| --- | --- |
| S2, OpenAI coding-evaluation audit, OpenLibrary-77c16d5 | Add the concrete one-versus-two leading-space mismatch between prompt and tests, explaining how following the prompt can fail. |
| S6, official SWE-Lancer instructions | Add the offline requirement for valid scores and current Linux iptables implementation; an online Mac trial is not equivalent. |
| S9/S10, Scale V2 announcement and repository | Distinguish 69 contradictory-instruction tasks from 529 rewritten statements, 214 test patches and 38 reference patches; explain different V1/V2 tooling and conditions. |
| S10, locked protocol and regrading | Distinguish model-endpoint-only agent access from normal setup/verifier networking, and explain clean-image regrading before a larger trial. |
| New S11, V2 release controls | Distinguish final 642/642 control passes from three first-pass infrastructure failures in each arm followed by successful reruns. |

These changes add missing explanation and prerequisites. They retain the conclusion: use leaderboards to select candidates, then run an internal procurement trial. [Reading notes](source-checks.md) retain source IDs and locators; public links appear in the report and [updated records](updated-records.json).

## Reuse, rework and simplification

The original task's 50 files remain unchanged; work continued in a copy. All 10 source texts/IDs, 16 claim IDs and six requirement IDs were retained. Four source records and five claims changed; S11 and the update requirement were added. Six unaffected sources needed no live refetch; relevant stored text was checked as needed. The user did not edit CSV or answer the brief again.

The first self-review found that editing the V2 paragraph had removed the existing explanation that cross-version scores cannot be read as model progress. The localized revision restored it using S9/S10 and moved the S10 citation next to its 529/214/38 figures, followed by checking the complete current report. The actual [needs_revision response](first-self-review.json) and [final pass](final-self-review.json) retain their versions. Unchanged output was not repeatedly judged for a better verdict. Historical independent blind reviews remain historical; no new independent score was produced.

Two actual frictions remain in the record: the 3,803-character first update was in range but its length requirement was still pending, so the agreed bounds were verified and that record updated before rechecking; S10 was reopened after the initial tool output was truncated. S11 was also fetched as raw text for retention. This was not a zero-duplication run.

Avoidable self-review transport became a product change: local callers can set `include_assignment: false` to receive the frozen input's path and hash. On the same actual review input, the response fell from **210,018 to 6,444 UTF-8 bytes, a 96.9% reduction**. Complete inputs, version binding and checks are unchanged; the default still returns the complete assignment. This measures response bytes, not overall tokens, time or monetary savings.

## Actual time and usage

From this request to the first complete updated draft: **5m 23s**. To completed report delivery checks: **11m 28s**. These are observed wall-clock intervals, including interleaved source checks, writing, self-review and the small implementation/regression work. They are not isolated authoring measurements and cannot be subtracted from historical from-scratch timings to estimate savings.

Host counters through report completion increased by **3,084,005 input tokens**, including **3,004,160 cached input**, and **21,488 output tokens**, including **8,830 reasoning output**. Cached input and reasoning output are subsets, not additional tokens. The interval includes the current long context, interleaved work and immediate completion verification; later documentation, CI and merging are excluded. No monetary bill or separate author-only usage was available. [Numeric snapshots and timestamps](resource-use.json) retain the measurement boundary.

Observed benefits are preserving existing research, adding specific explanations/prerequisites, avoiding reconstruction of unchanged records and shrinking one tool response. There is no paired update-versus-rewrite run, so this case does not quantify total time/rework saved or establish a general Full quality/cost advantage.

The [execution summary](execution-summary.json) retains original-file hashes, input versions, report hashes, reuse counts and completion results. [First-draft checks](first-draft-check.json) preserve the pending state; [final checks](final-draft-check.json) pass. Complete frozen assignments and receipts remain in the local task; the public evidence subset is not a portable full-task snapshot.
