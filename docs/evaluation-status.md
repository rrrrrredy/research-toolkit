# Evaluation evidence and version boundaries

[English](evaluation-status.md) | [简体中文](evaluation-status.zh-CN.md)

**Current evidence supports specific corrections and engineering benefits, not a general quality or efficiency advantage over a native agent.** Version comparisons, fixed-source Lite trials and runtime checks answer different questions; they cannot be combined into one efficacy score.

## Current evidence

The [October 19 public-library self-check comparison](../evals/studies/2026-10-19-library-self-check/README.md) contains one research question and two Lite runs, one per version, using the same model, sources and defective draft. v1.3.1 and v1.3.2 both removed the deliberately injected duplicate and off-topic paragraph before their first passing checklist; neither falsely passed these known defects. **This case showed no incremental v1.3.2 benefit and does not verify patch efficacy.** The archive retains the clean first draft, defect ledger, first checklists and corresponding reports, final outputs and measured session times (365.797 s and 381.000 s). No model rerun was made for ingestion.

The [actual long-report update](case-study/coding-benchmark-update/README.md) reuses the coding-benchmark task's sources, claims and requirements, adds source-confirmed explanations/prerequisites, and preserves a self-review correction, draft checks, timing and host usage. The same review input returns 210,018 bytes by default versus 6,444 with an optional local file reference. This measures serialized response size; the continuation has no rewrite counterfactual or new blind score and leaves historical comparison results unchanged. An [October 15 separate-context Astra review](case-study/coding-benchmark-update/review-2026-10-15/README.md) found no necessary fixes and suggested the adopted serialization-method clarification.

The [October 14 complete native-Agent comparison](../evals/studies/2026-10-14-native-agent/README.md) runs one existing real long task with live retrieval, tools, complete drafting and normal author checks in both conditions. Separate-context Astra blind reviews tie both the first and final pairs; both score 100/100. Toolkit Full/self takes 14.3 minutes versus native's 9.2 and uses more tokens and operations. This task shows no net report-quality gain; it does not estimate other tasks or profiles. An actual Windows JSON encoding failure discovered during the run is repaired and rechecked with the affected source material. Full drafts, final reports, original judgments, startup failures and actual resource use are retained.

The [October 13 complete-report comparison](../evals/studies/2026-10-13-before-after/README.md), with repairs completed October 14, directly compares the user-selected October 12 commit against v1.0.0 on seven existing and three new real tasks. Astra's primary mean is 100 → 99.5; three of ten preferences change under order swaps. No stable overall quality gain was observed. All 20 first reports and 20 blind reviews are retained. A subsequent export check found six private citation tokens in one current-version report that both initial reviews missed. Bilingual method clarifications and two revised reports received targeted rechecks; the negative intermediate recheck remains visible. These repair outcomes do not replace first-pass results.

The [current optimization report and executed continuation checks](../evals/diagnostics/2026-10-14-optimization/README.zh-CN.md) separate code repairs, report checks, workflow use and cost; they do not replace historical first-pass scores.

The [October 16 external eval ingest](../evals/studies/2026-10-16-external-batches/README.md) records 12 Song-authorized runs from confirmed batches 2026-10-14 (Toolkit `45bfc5e38f62f563bb8b800acbdbcb3fd2e27bd3`, v1.0.0, Lite) and 2026-10-15-v1 (Toolkit `f31345c5a994a8f1574d946388ee58fe1177ede2`, v1.1.0, Lite×4 and Full×2). Two Full records repeat a Day-1 research question, so the set is 12 runs and 10 questions. Sources are disclosed synthetic packs, and the original-language report stays primary. Lite runs record author self-check only. The two Full runs use same-session degraded review because the independent review backend was unavailable. Mechanical checklist outcomes are retained. This ingest is not a native-agent comparison and does not support a general quality claim. Superseded compare-puzzle and one-pager batches are absent.

The [October 19 external eval ingest](../evals/studies/2026-10-19-external-batches/README.md) records 12 Song-authorized Lite runs from confirmed batches 2026-10-16-v1 (Toolkit `f31345c5a994a8f1574d946388ee58fe1177ede2`, v1.1.0) and 2026-10-17-v2 (Toolkit `fedf7cde832139c86cad585883cb5ec2f666427f`, v1.3.0). The 12 question texts in that folder are distinct. Two retests repeat a question already ingested on October 16. Sources are disclosed synthetic packs, and the original-language report stays primary. Lite runs record author self-check only. The six 2026-10-17-v2 outer Grok notes are separate-context readings, not Toolkit independent reviews. Mechanical checklist outcomes are retained. This ingest is not a native-agent comparison and does not support a general quality claim. Superseded compare-puzzle and one-pager batches, the superseded 2026-10-17-v1 topic gate, and 2026-10-18-v1 are absent.

**Result correction, 2026-10-19:** Four 2026-10-16-v1 originals in that ingest (predictive maintenance, guide funds, Scope-3 RFQs and credit memos) contain repeated or off-topic passages. Their author-qualified/pass descriptions conflict with the reports and must not be cited as quality passes. [Separate revisions and per-report change notes](../evals/repairs/2026-10-19-reader-edit/README.md) preserve the originals, self-checks, batch outcomes and run counts. Report repair is not a Toolkit core-capability upgrade.

The [October 21 external eval ingest](../evals/studies/2026-10-21-external-batches/README.md) records 12 Song-authorized Lite runs from confirmed batches 2026-10-18-v1 (Toolkit `fedf7cde832139c86cad585883cb5ec2f666427f`, v1.3.0) and 2026-10-19-v1 (Toolkit `e245b90a324933f53fddf0deea039a7715708005`, v1.3.1). The 12 question texts in that folder are distinct. Four retests repeat a question already ingested. Sources are disclosed synthetic packs, and the original-language report stays primary. Lite runs record author self-check only. All 12 outer Grok notes are separate-context readings, not Toolkit independent reviews. Mechanical checklist outcomes are retained. The guide-fund retest repeats the 20261016 question and source pack and does not replace the prose correction above. This ingest is not a native-agent comparison and does not support a general quality claim. Superseded compare-puzzle and one-pager batches, the superseded 2026-10-17-v1 topic gate, and 2026-10-20-v2 are absent.

## 2026-10-12: connectivity and judge calibration

The [connectivity record](../evals/diagnostics/2026-10-12-connectivity/README.md) retains configuration failures and separately frozen follow-up. The [Astra calibration](../evals/diagnostics/2026-10-12-astra-calibration/README.md) completed 12 first attempts across four families, with source-confirmed defect preferences, swaps and valid ties. Three dimension scores changed under swapping. This admits a bounded development pilot, not a general judge-reliability or Toolkit-effect claim. Existing historical cohorts and outcomes below remain unchanged.

## 2026-10-12: four-model development results

The [fixed-source Lite diagnostic](../evals/studies/2026-10-12-lite-four-models/README.md) completed 40 author and 32 judge requests across five independent task families and 20 model-task pairs. Four pairs remain unresolved due to LongCat format failures; six of 16 judged pairs changed preference after swapping. Only 14 of 36 format-valid reports met length constraints; source checks also identified budget, forecast and attribution errors. Original scores remain unchanged; no general effect claim. Separate [JSON format probes](../evals/diagnostics/2026-10-12-longcat-format/README.md) parsed 3/4 and did not fill missing pairs.

## 2026-10-13: bounded follow-up after corrections

[Eight new probes](../evals/diagnostics/2026-10-13-feedback-probes/README.md) exercise prompt/schema alignment and Lite guidance corrections: 8/8 parse, but only 3/8 meet length, with false comparisons and unknown conditions asserted as changes. This batch records actual format, length and source checks; original failures remain and later repairs are recorded separately. The existing delivery gate rejects five real length failures and accepts two post-result editorial controls. This is software verification, not new model quality scores.

## 2026-10-13: old/new tasks and repair acceptance

The [four-task recheck](../evals/diagnostics/2026-10-13-targeted-recheck/README.md) retains 16 initial drafts, nine measured-feedback revisions and six Astra review batches: 31 requests. First Astra review passed six reports; the maintainer corrected ten. All 16 final versions meet length and have corresponding passing reviews, including two reused reviews with verified identical report and input texts. First-draft quality and maintainer-assisted outcomes remain separate. A false provenance finding caused by omitted judge-source path metadata is recorded and corrected, rather than attributed to author fabrication.

## Historical scope and task identity

**Scheduled first reviews are complete. Their findings inform product improvements; they do not establish general superiority or validate the current plugin/MCP workflow.** This summary uses the retained inventory as of September 21, 2026. Original reports, author failures, original reviews and later interventions remain separate.

The public collection supports workflow diagnostics and product development. It does not yet support a general decision-quality advantage, a representative cross-language benchmark or an efficacy confidence interval. The original English showcase is a research example, not a matched efficacy pair. [Next study design](evaluation-roadmap.md#next-study-freeze-the-design-then-collect-new-evidence) · [Stable defect labels](necessary-defects.md).

The separate [October 10 fixed-source Lite pilot](../evals/studies/2026-10-10-lite-four-models/README.md) publishes judgments for all 20 model–task pairs across five shared families and four models, with original failures retained. Its local freeze, instruction-only scope, post-hoc format analysis and separately regenerated completion pairs are disclosed; it does not change the historical counts below.

Existing and future user tasks, development tasks, reference tests and cases are real independent tasks; tests actually executed are real tests. Model execution and evaluation also provide a user perspective: judge usefulness from actual context use, extra reading, time, rework and research results. Human participation is not a prerequisite; describe the observed benefit and its task scope. Task identity follows the research question, so repeated runs of one task remain repeated runs. Source materials retain their stated provenance, including supplied or constructed data. Astra in a separate context can review independently; no outside person, different model vendor or additional external material is required. Changes to task assignment, reviewer inputs or acceptance criteria require targeted revalidation.

## Retained data

| Collection | Evidence | Use boundary |
| --- | --- | --- |
| Development reports | 23 topics; 92/92 complete first reviews | Development feedback; revisions never replace first-submission results |
| Archived diagnostics | 50 items from 16 parent topics | Development items, not 50 independent held-out tasks |
| Historical paired study | 11 retained families; 22 complete review inputs; 88/88 valid first reviews; 211 adjudicated findings in 61 necessary issue groups | Bounded historical evidence; original failures and supplemental runs reported separately |
| Public semantic diagnostics | [23 bad/control pairs](../evals/semantic_diagnostics/) | Real tasks with constructed failure-mode materials, separate from archived diagnostics |

The paired study originally had 12 families. One was excluded after results were known because required source originals remained unavailable. The current denominator is a post-result exclusion, not the original design or a quality improvement. Those reports are absent from the active collection; the original study and exclusion record remain in the public data archive.

Of 22 original author attempts in the retained families, 12 failed. Twelve supplemental attempts provided complete reports without replacing those failures. The primary comparison has five families with necessary defects in both conditions and six unresolved families affected by author quota failures. The separate supplemental view has one Toolkit win and ten families with necessary defects in both conditions. The 88 reviews assess 22 inputs, not 88 independent tasks.

## Public scope

The repository includes [calibration reports and model replies](../evals/diagnostics/2026-09-07/), [semantic diagnostics and available reviews](../evals/semantic_diagnostics/), and [offline controls](../evals/README.md). The [office-agents development case](case-study/office-agents/README.md) also includes a complete report, retained draft, source and claim records, and a review summary. The associated [data repository is now public](https://github.com/rrrrrredy/agent-trajectory-data/blob/main/docs/PUBLIC-EVALUATIONS.md). Its v0.4 archive includes the preserved v0.3 corpus: 23 development report inputs, 22 paired-study inputs and 221 retained review records, with 92 development and 88 paired first-review slots. Source packages and recorded tool observations retain their original scope and omissions; withdrawn material is not restored. All 19 data releases and 79 assets were accessible without authentication on October 13.

Reviewer agreement is not accuracy. The historical cohort has already informed development; future reuse is regression/development work, not a new unexposed efficacy test. Human calibration is not a prerequisite for completing the required model reviews.

## Current implementation

The plugin and MCP share one workflow. Local controls exercise stage prerequisites, supplemental requirements, assignment matching, recovery and delivery bindings, including an actual MCP stdio connection with synthetic reviewer processes. They establish tested software behavior, not real-model research quality, provider access or reliable behavior by every host agent.

| Historical reviewer backends (retained provenance, not a default dependency) |
| --- |
| Plugin `0.1.2` also has a bounded, guided Codex CLI/MCP check with one brief using fictional source material and real `gpt-6-sol` high reviewer and auditor contexts. The audit completed after recovery without rerunning the completed reviewer; the original negative finding, unchanged report and failed attempts were retained. The delivery gate refused the unresolved report defect. Configuration and audit-contract corrections were needed to complete this check. It does not establish unattended operation or a research-quality advantage. |

The historical report studies do not measure the later shared plugin/MCP implementation. Combining them with passing software checks does not establish a current general quality or efficiency advantage. A future efficacy comparison needs a separately scoped, frozen design. Fixing software defects and preserving existing first-review findings do not require rerunning historical reports.

[Evaluation standard](report-evaluation-standard.md) · [Claim boundaries and study design](evaluation-roadmap.md) · [Usage and execution limits](usage-modes.md)


## October 13 report completion and project correction

The pipeline report’s R01–R13 record covers one report. Project correction also changes Lite completion, Full methods, source packets, installed instructions and data generators. See the [full collection and correction map](correction-audit-2026-10-13.md) and its actual verification records. The earlier v0.2.6 project-wide closure claim is superseded.
