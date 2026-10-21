# Task continuity code review

[English](task-continuity-review.md) | [简体中文](task-continuity-review.zh-CN.md)

2026-10-21. After explicit user authorization, a separate Codex execution context reviewed the generic source diff read-only: task context, records, workflow, change locations, observations, MCP, continuity tests and guidance. Private study directories were excluded. The reviewer performed static analysis; its attempted reproductions could not find Python and were not executed.

| Finding | Correction and verification |
| --- | --- |
| P1: partial brief updates could erase custom specification sections | Replace only known fields; preserve other content; reject conflicting direct edits atomically. Tested section retention and unchanged files after a conflicting batch. |
| P2: malformed historical requirement status could throw after a successful save | Return it as unresolved with a warning. Tested read-only status and an unrelated successful draft save. |
| P2: strict reading validation blocked maintenance of explicitly waived legacy records | Preserve historical reading fields for scope decisions; revalidate on reopening. Tested retirement, summary update and reopening. |

All three were fixed and covered by targeted reruns. The reviewer reported no further concrete issue in main/historical artifact separation, review binding or import counting; this is not a guarantee of correctness. The original review was retained outside the repository.

Maintainer review also checked generated files, bilingual documentation, API compatibility, platform skips and new-file contents. An installation staging-test comparison was corrected separately; see [validation](task-continuity-validation.md). No extra semantic gate, mandatory legacy migration or relaxed independent-review proof was added.

No second model review of unchanged content was requested. Fixes were checked against the original findings, exact changes and targeted tests. Long-term maintenance and research-quality benefits remain unmeasured.

Release CI additionally exposed noncanonical Windows paths: capture paths were resolved while the task root could retain a short-name alias, breaking relative-path calculation. The root is now resolved consistently; an equivalent `..` path reproduced the failure before the fix. The Windows workflow also restores the immediate exit-code check after record tests so a later command cannot mask their failure. These are follow-up CI repairs, not findings attributed to the independent reviewer above.
