# Continue a real report with change summaries

[简体中文](README.zh-CN.md) · [Complete updated report](report.zh-CN.md) · [Previous continuation](../README.md)

On October 15, 2026, the same real procurement research continued through the public Full guide and `research_workflow.py` `status/save/check-draft/review/finish` entry points. The author read sources, chose revisions and wrote the report; the runner only captured requests, responses and timing. The original task's 67 files remain unchanged. The [previous complete report](previous-report.zh-CN.md), [complete first update](first-update.zh-CN.md) and final report are retained separately.

## Actual improvements

After two source-record updates, `save.changes` identified five linked claims, C8/C13/C14/C15/C16, and report citation locations. Source inspection led to revisions of C8/C14/C15:

| Source evidence | Change reaching the report |
| --- | --- |
| Official SWE-Lancer README, Docker Setup and Manager configuration | Explain that Manager tasks require a monolith image; the IC per-task image configuration cannot simply transfer. |
| Pro V2 locked protocol | Explain partial-patch capture and grading at the 50-minute timeout; recommend retaining timed-out attempts in the trial denominator. |
| Image preparation and pristine-image regrading requirements | Recommend separating shared setup from per-task costs. This is accounting advice, not a measured saving. |

[Source checks](source-checks.md) retain original links, locators and access outcomes. These details already existed in sources but were not developed in the report; its October 14 information cutoff and core conclusion remain.

## Reuse, friction and outcome

All 11 source texts/IDs, 16 claim IDs and seven requirement IDs were reused. Only two source, three claim and three requirement records changed. Nine other sources needed no live refetch. Drafts were registered by path; the user did not manage CSV. See [record differences](updated-records.json) and the [original save response](calls/03-source-update.response.json).

The initial save supplied only S6/S10 IDs and the old draft path to observe this old task's file baseline. It returned `first_observation` and `updated_files=[]`; other old tasks need no reconstructed history. Here source changes are updated reading records/evidence references, not changed upstream files.

Locations still require judgment: the S10 link is on line 21, relevant prose also occurs on neighboring line 23, and procurement advice on line 29. The tool provides reading entry points; it did not decide that all five claims needed revision. The next record save replaces the summary, which is not a cross-batch backlog.

The first and final reports have identical bytes and **3,930 nonwhitespace characters**, within the original 2,500–4,000 range. Author review found no necessary prose correction. Reuse and localized changes were observed; no concurrent update-versus-rewrite control was run, so no saving percentage is estimated.

## Observed timing and usage

The [nine CLI calls](calls.jsonl) span **109.80 seconds** from first capture to observing the complete draft and **280.34 seconds** to local delivery-check completion. CLI subprocesses totaled **8.484 seconds**, with zero nonzero exits. Code/source inspection preceded capture; later Astra review, fixes, CI and merging are excluded. These are not total request-to-delivery or first-usable-result measurements. The [execution summary](execution-summary.json) retains calculations.

Public CLI responses did not provide host author/Astra tokens or billing; these remain unknown. No external backend call for self-review does not mean zero model cost. The S6 commit lookup was empty and file-SHA retrieval failed; the successful web read and retained original text support the check, without a zero-retry claim.

The local copy retains Full/self and its actual author review/delivery checks. The requested clean-context Astra review is archived separately, not presented as a CLI independent-backend receipt. Published files are complete reports and an evidence subset; full frozen assignments and receipts remain in the local task.
