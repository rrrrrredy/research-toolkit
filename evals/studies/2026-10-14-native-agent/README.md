# One real long-form task: native Agent versus Toolkit Full

[English](README.md) | [简体中文](README.zh-CN.md)

**This task showed no net report-quality gain from Toolkit; Full took more time and operations.** Fresh-context Astra assessments tied both the first-draft and final-report pairs, passing both reports. Extra procedure is not a quality gain. Actual use also exposed a Windows CLI encoding failure, which was repaired and rechecked with the affected input.

## Task and execution

Reuse the existing real independent task [“What procurement judgments can coding-agent leaderboards support?”](../2026-10-13-before-after/protocol.json): compare SWE-bench Verified, SWE-Bench Pro and SWE-Lancer, account for the July 2026 quality critique, and propose procurement and internal trials in a complete 2,500–4,000 nonwhitespace-character Chinese memo. This is a new paired run of one task, not two new research questions.

Both fresh author sessions used Astra, xhigh, Codex CLI 0.162.0-alpha.17.2, the same four starting URLs, live search and local tools. Each searched, opened original sources, calculated, wrote and self-checked. Neither received a prewritten report or fixed source digest. Native Codex retained normal self-checks without Toolkit. The other author read the public `SKILL.md`, ran Full with `reviewer=self`, maintained task records and completed delivery. The common independent assessment took place after the author stage; author checks were not labelled independent.

Toolkit was pinned to `09c8e7cd5c394eea4972c0ff6fd5fcd78c18db5c` (PR #52). The later encoding fix is not backfilled into that run. Authors ran concurrently; latency is observed, not a repeated performance estimate. [Protocol](protocol.json), [execution records](execution/), [driver snapshots](execution-code/).

## Full reports and blind judgments

| Artifact | Native Agent | Toolkit Full |
|---|---|---|
| First complete report | [3,351 characters](reports/native/first-draft.md) | [3,482 characters](reports/toolkit/first-draft.md) |
| Final after author checks | [3,500 characters](reports/native/final.md) | [3,577 characters](reports/toolkit/final.md) |
| Actual revision notes | [Native](reports/native/revision-notes.md) | [Toolkit](reports/toolkit/revision-notes.md) |
| First-draft assessment | 100/100, pass | 100/100, pass |
| Final assessment | 100/100, pass | 100/100, pass |

Each pair went to a separate fresh Astra context with the original task, anonymous A/B full reports and the union of actually read source records. Author notes, methods, workflow state, condition mapping and the other judgment were excluded. Ordering was fixed beforehand: A=Toolkit, B=native. The first packet contained 23 exact-deduplicated records; the final had 24, adding a Scale paper landing page. These are record counts, not independent-source counts. [First judgment](blind/first/response.json), [final judgment](blind/final/response.json), [input bindings](blind/final/bindings.json).

Located differences are more informative than the ceiling score. Toolkit developed Pro V2 execution rules, HARD-51 selection effects and checks on alternative valid/incomplete patches. Native used a concrete OpenLibrary failure and separated historical replay, held-out confirmation and prospective randomized trials. Both found Pro V2 and the Lancer offline-subset change; neither applied old defect rates to a new version or converted historical bounties into business savings. Astra judged these strengths complementary.

Native self-checks clarified Diamond composition, the recommended V2 protocol, pricing and trial denominators. Toolkit clarified all-attempt costs, stratified random assignment and paper locators. These are real revisions, but native also revised successfully: they cannot all be attributed to Toolkit. Neither blind review required a correction; no report was rerun to obtain a win. The five-dimension rubric reached its ceiling here; 100 is not proof that every possible defect was excluded.

## Actual resource use

| Author-stage measure | Native Agent | Toolkit Full |
|---|---:|---:|
| Wall time | 551.516 s (9.2 min) | 856.125 s (14.3 min) |
| Input tokens, including cached | 1,297,739 | 3,320,554 |
| Cached input subset | 1,192,448 | 3,164,160 |
| Uncached input | 105,291 | 156,394 |
| Output tokens | 16,264 | 24,271 |
| Completed web-tool events | 11 | 13 |
| Completed command events | 7 | 24 |
| Completed file-change events | 4 | 24 |

Full used about 5.1 more minutes (55%), and about 49% more uncached input and output tokens. Cached input is not added again. An event can contain multiple queries or file changes; cumulative input includes repeated context, not unique material. Currency charges and human time saved were not measured, so token ratios are not price ratios.

Both first launches rejected an unsupported built-in-provider override before model execution. After correcting that configuration, both sessions were blocked before reading the task because the Windows sandbox selection was absent; those two sessions consumed 136,893 input and 1,373 output tokens. Supplying the machine's configured elevated sandbox with automatic approval enabled the completed author runs; the sandbox was not disabled. All startup attempts are retained separately.

The two shared blind reviews added 429,927 input and 12,863 output tokens, taking 252.359 and 179.016 seconds. All captured sessions total 5,185,113 input tokens (4,624,256 cached) and 54,771 output. Coordinator work in the parent chat is not included. [Complete accounting](summary.json).

## Finding turned into a product repair

Toolkit actually encountered `UnicodeEncodeError: 'gbk' codec can't encode character '\ue200'` while printing source-containing self-review JSON, then recovered with a process UTF-8 setting. It also resolved a pending length record and a not-yet-created output directory. These frictions are retained, not counted as report-quality failures.

The shared CLI now explicitly reads/writes UTF-8 JSON. An isolated replay used the actual retrieved Scale source and identical GBK pipe conditions: the old script exited 1; the repaired script exited 0 with intact citation characters and the full self-review packet. [Replay](encoding-replay.json). The existing draft contract suite adds a real CLI encoding regression. No research gate changed and unaffected report content was not regenerated.

Both reports used public Markdown citations, so this case did not trigger an author repair in response to a private-citation advisory. That branch is not claimed as observed. Previously merged PR #52 covers known marker formats/code examples and runs real file-symlink controls on Linux and Windows cloud runners; all 17 Windows build checks ran without skips.

## Interpretation and verification

This complete native-Agent comparison does not justify extra Full steps solely to improve report quality on this task. Full additionally retained structured sources, claims, review inputs and delivery-version records; later handoff/update time savings were not measured. The result concerns one task, this model and Full/self, not Lite, other models/tasks or continued work. It is not a release prerequisite.

The public bundle contains complete reports, revision notes, original judgments, usage, command/search metadata, exact hashes and input manifests. Original page captures, complete review requests and tool outputs remain in the local capture directory; source bindings, access metadata and original hashes identify them without redistributing entire third-party pages. Public events normalize host paths, replace long commands/tool outputs with hashes, and omit reasoning items; summary records the export rules and original/public hashes. CLI model fields distinguish requested identity from unavailable returned attestation.

Run `python evals/studies/2026-10-14-native-agent/verify.py` to check public bytes, bindings, recorded event usage and summary consistency. It does not call models or establish semantic quality. Drivers are execution snapshots requiring local paths/login to rerun; a rerun remains a repetition of this task.
