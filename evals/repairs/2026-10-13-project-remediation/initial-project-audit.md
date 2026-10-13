# Independent project-scope audit

Date: 2026-10-13. Requested reviewer: Astra (`gpt-6-astra`), in a separate subagent context. This is a fresh project audit, not an endorsement of earlier agents' reviews or completion claims. Model identity here records the requested role; I did not independently attest the serving backend. Both repositories were inspected read-only. No model evaluation, paid call, report rewrite or repository edit was performed. One additional offline negative control reproduced a Lite runtime defect in a temporary directory outside the repositories. This file is the audit output.

Existing and future user tasks, development tasks, reference tests and cases are real independent tasks. Executed tests are real tests. Repeated runs retain the same task identity. Source materials retain their actual provenance. Astra in a context separate from the author is sufficient for independent review, including when the author uses the same model. Changed assignments, reviewer inputs and acceptance criteria require targeted revalidation.

**Conclusion:** the current project has substantive reusable methods and substantial task evidence, but a report's R01–R13 closure cannot establish Toolkit remediation. Remaining work includes a contradictory installed entrypoint, missing source metadata in an evaluation input constructor, inconsistent method guidance across profiles, and current generators/docs that can reintroduce superseded policy. The needed work is bounded; no new external people, vendor, task collection, universal benchmark, or large framework is required.

## Required changes

### 1. Correct the installed plugin's report-repair instruction

`research-toolkit/plugins/research-toolkit/skills/research-toolkit/SKILL.md:17` says “Evaluation reports stay unchanged; use findings to improve the Toolkit.” The root Skill explicitly permits authorized repairs in separately saved versions. The installed entrypoint's unqualified prohibition can stop exactly that authorized work.

State that **original evaluation reports and original judgments remain preserved; authorized repaired versions are saved and reviewed separately**. Explain the existing runtime boundary: a frozen evaluation assignment is retained, and a repaired report uses a new version/repair task linked to the same research question. Do not silently change the original evaluation packet or count that version as a new independent task.

Relevant verification: `scripts/check_installation_contract.py`, `scripts/check_installation.py`, `scripts/build_plugin.py --check`, `scripts/check_research_workflow.py`, and `scripts/check_profiles_reviewers.py`. The wrapper is not one of the shared payload files copied by `build_plugin.py`, so payload equality alone will not detect this contradiction. Check the actual installed wrapper text. No new paid run is needed merely to edit this explanation; any changed assignment delivered to a reviewer needs its own bounded recheck.

### 2. Preserve necessary source identity in new blinded-evaluation packets

`research-toolkit/scripts/run_blinded_evals.py:135` reconstructs every supplied source as only `{id, text}`. It discards the task's source path and any separately recorded citation/provenance metadata. Author and judge receive the same stripped list, so the existing equality test in `scripts/check_blinded_protocol_v2.py:69` does not establish completeness. A brief or report that refers to a supplied source by filename can therefore appear unsupported even when the underlying source was supplied.

Carry the neutral source locator/title/provenance needed to interpret citations into **both** author and judge packets. Keep condition mappings, private author notes and coordinator answer keys excluded. Do not expose a condition-revealing directory as a substitute for a neutral source locator. Freeze the enriched packets for new runs and retain older packets as historical evidence.

The ordinary Full runtime already includes source filenames and source/claim registries in `scripts/research_workflow.py:566–579`; it does not need this same repair. Extend the existing blinded-protocol control with a brief/report citing a source filename and a source whose provenance is outside its body. Verify preserved locator/provenance, identical evidence for author/judge, and absence of private notes and condition labels. Run `check_blinded_protocol_v2.py` and `check_blinded_evals.py`; revalidate only affected reviewer inputs on an existing provenance/citation task.

### 3. Reconcile Full methods with task-dependent structure

Current Full instructions still mandate a six-part card for every analysis unit (`references/research-workflow.md`, §6), an eight-part assembled structure (§9), and a reference appendix (`references/research-standard.md`, §11; `references/quality-gates.md`, Before Final Assembly). Chinese counterparts contain the same requirements. This conflicts with the entrypoint's optional-lens policy and actual task contracts: `evals/cases/model_company_pipeline_long_horizon_zh.json:49–54` explicitly disables reader references and forbids reference-material sections. This observation concerns the reusable case contract, not an assessment of its report.

Make these structures optional examples selected by the question. Require useful evidence, explanation, counterevidence and coverage where relevant, without requiring a timeline/current-position/implication card for every unit or a references appendix for every report. The same reconciliation should avoid turning the ordinary “remove process language” guidance into an unconditional ban on useful source attribution.

Relevant existing families: long-horizon no-appendix case and its forbidden-appendix regression; short constrained memos; monthly synthesis; original English API/browser case. Check relevant generated prompts and Full stage guidance in both languages, `check_research_workflow.py`, `check_evaluator_contract.py`, `check_regression_fixtures.py`, docs sync and package sync. A targeted Astra check should compare the changed method against these existing task shapes; no rerun of all historical reports is needed.

### 4. Carry reusable analysis corrections into Full, not only Lite

`references/lite-workflow.md` now supplies concrete methods for checking joint hard requirements before preference, separating forecasts from present eligibility, keeping measurement populations/correction states together, and validating time/capacity triggers. `scripts/research_workflow.py:185–188` sends Full analysis only §§7–9 of `references/research-standard.md`, whose source-discipline text does not contain those operational checks. Full users can therefore miss lessons already incorporated for short reports.

Put these concise, generally useful checks in the shared Full source/claim or analysis method and its Chinese counterpart; keep Lite's compact rendition synchronized. Do not add company-specific requirements, new mandatory files, a new scoring system, or a universal procurement template. Use the existing question/claim/source records.

Relevant tasks: backup-budget and archive-scan in `evals/tasksets/development-v2-synthetic/`; forecast, comparison and attribution tasks in the current four-task recheck; semantic denominator, unit/date and causal-overclaim pairs. Verify the returned Full and Lite analyze guidance, then recheck the changed methods with the relevant existing bad/control examples. Existing `check_profiles_reviewers.py` and `check_research_workflow.py` provide the stage-routing controls. New reviewer instructions require targeted actual revalidation; a wording grep alone is insufficient evidence of semantic effectiveness.

### 5. Correct current generator/access prose while preserving historical archives

Current editable source code will continue emitting stale policy/access language:

- `agent-trajectory-data/scripts/runtime_release.py:106`: “Incremental private release”; its line 104 fallback also says earlier material remains in private releases.
- `agent-trajectory-data/scripts/runtime_revision.py:354`: “All material remains private diagnostic development data”.
- `agent-trajectory-data/scripts/research_history.py:499`: “20 组语义案例为合成短文，不是 20 次真实研究”. Distinguish twenty real diagnostic tasks from four full-report author runs directly, rather than denying reality.
- `agent-trajectory-data/docs/DATASET-v0.3.zh-CN.md:74`: “未改名为真实任务” still contradicts the current task policy in a human-authored data card.

Make new generated documentation describe actual distribution state or use access-neutral language; identify task type, source kind, execution count and study use separately. Update the current data card or add a precise current correction adjacent to its historical statement. Keep raw ZIPs, embedded historical scripts, original prompt/output text, scores and execution metadata unchanged. Do not alter training eligibility or source-use permissions merely because repository/release access is public.

Relevant checks: `tests/test_research_history.py`, `tests/test_research_corpus.py`, `tests/test_runtime_dataset.py`, `tests/test_runtime_curriculum.py`, and release/export tests only for generators actually touched. Verify newly generated README text in temporary output and continued exact preservation of embedded prior archives. No paid model call is involved.

### 6. Finish the explicit positive policy wording in active documentation

Despite positive policy paragraphs elsewhere, active prose still uses the rejected framing:

- `research-toolkit/docs/evaluation-roadmap.md:20` and `.zh-CN.md:18`;
- `research-toolkit/docs/evaluation-status.md:15`;
- `research-toolkit/docs/independent-task-design.zh-CN.md:7`;
- `research-toolkit/evals/semantic_diagnostics/README.md:13`;
- `research-toolkit/evals/taste_anchors/README.md:7` and `.zh-CN.md:7`.

Replace “development use does not invalidate…” and corresponding Chinese negations with the positive policy at the top of this audit. Keep useful distinctions about task identity, repeated runs, source provenance, statistical generalization and factual evidence. Do not mechanically replace those terms inside raw transcripts, source documents or frozen packets.

Relevant verification: scoped bilingual text/link review, `check_docs_sync.py`, `check_installation_contract.py` and `build_plugin.py --check` for mirrored entry/reference changes. Only changed actual reviewer packets need model revalidation.

### 7. Make project coverage and acceptance traceable across collections

The current evaluation inventory lists useful current groups, but `agent-trajectory-data/docs/PUBLIC-EVALUATIONS.md` primarily inventories release/asset counts. HTTP availability and a single report's requirement table are neither a research-method coverage map nor project acceptance. The current `docs/evaluation-status.md` “October 13 final completion” section centers that report; any project completion wording must state the actual Toolkit scope separately.

Extend existing inventory/improvement documents with a compact collection-to-use map: where each material is read, which reusable method/runtime behavior its failures test, what changed, which relevant verification was actually performed, and any reasoned no-change outcome. Include historical full reports and review inputs as well as short semantic controls; explicitly include both public cases and Lite/MCP examples. Use existing sections/tables rather than building a new registry or treating every collection as requiring another run. In acceptance, R01–R13 remain that report's requirements. Project completion follows the actual remaining method/runtime/doc corrections and their affected validations.

For the public archive, add entry paths into v0.4 and its embedded versions, plus an index to later executable-environment/recovery/format studies. The local v0.4 ZIP inspection confirms `prior/tasks.jsonl` has 45 report-review inputs, `prior/reviews.jsonl` 221 retained records, `prior/author_attempts.jsonl` 34 records, `tasks.jsonl` 17 executable task rows, `coverage.jsonl` 98 overlapping coverage rows, and `prior/prior/base/tasks.jsonl` 10 earlier task rows. These counts describe different record types and must not be added into one task total. Preserve older independence/access labels in the archive and explain their historical meaning at the current entrypoint.

Verification is link/path and inventory consistency plus targeted reuse of the relevant existing family, not an obligatory new full evaluation campaign.

### 8. Block Lite terminal completion when its own records show unfinished required work

**Reproduced runtime defect, high priority.** `scripts/research_workflow.py`, `finish_lite`, checks the checklist, source/claim prerequisites and explicit length constraints, then binds the requirement ledger without checking ordinary requirement statuses or `progress.open_issues`. `scripts/profile_policy.py`, `inspect_lite_delivery`, also checks hashes/length but not those contradictions; `check_delivery.py:651` returns directly into that Lite checker.

An offline task with a valid source/claim, an ordinary `R-open` requirement having `status: open`, `progress.open_issues: ["Required comparison remains absent"]`, and all six checklist booleans set true returned:

```json
{"completed": true, "stage": "final", "status": "complete", "open_issues": ["Required comparison remains absent"], "delivery_check_ok": true}
```

The checklist cannot override an explicit unfinished obligation already present in the same task. Add the existing lightweight record-consistency checks for open required work and recorded blockers before writing a terminal Lite receipt/state, and when checking an existing Lite delivery. Validate specific user decisions for closed-as-waived/out-of-scope/accepted-limitation records consistently with the existing requirement contract. Keep semantic adequacy as the author checklist's responsibility; this does not require Full audits or a second reviewer.

Reproduction: `output/astra-lite-open-requirement-repro.py`; observed result: `output/astra-lite-open-requirement-repro-result.json`. It uses a temporary directory beneath output and performs no model calls. Relevant existing controls: `scripts/check_profiles_reviewers.py` (Lite completion, source binding, length closure and stale receipts), `scripts/check_draft_contract.py`, and ordinary requirement-closure checks in `scripts/check_delivery_contract.py`. Add positive controls for satisfied requirements and an explicit authorized waiver, and negative controls for an ordinary open requirement, open progress blocker and unapproved waiver. No paid evaluation is needed to prove this deterministic correction; changes to reviewer inputs are a separate revalidation concern.

## Which existing collections need revalidation after these changes

| Collection/input | Required targeted verification | What stays preserved/unrerun |
|---|---|---|
| Root/plugin/HTML/agent entry instructions and Full stage methods | Actual resolved entrypoint text, both language paths, package sync; Astra reads changed method with existing no-appendix, constrained-choice and measurement controls | Installation on every possible host is not required |
| New blinded v2 freeze/author/judge packets | Offline locator/provenance and masking controls; one relevant existing citation/provenance task when its actual judge input changes | All October 10/12 frozen packets, first scores, failures and swap outcomes |
| Current semantic catalog | Only pairs actually affected by a changed input or acceptance criterion; preserve mapping and first output | Merely editing the surrounding inventory does not require rejudging all 23 pairs |
| Seven dedicated cases | Generated prompt contract checks for any changed prompt; concrete affected family for method change | The seven distinct task identities, original outputs and report-specific R01–R13 results |
| Five development families and four-task recheck | Backup-budget/archive-scan/measurement/attribution controls as relevant to the shared analysis method | Unchanged unrelated report versions and reviews |
| Historical 23 development topics, 11 retained paired families, 50 archived items/16 parent topics | Inspect reusable defect families and current method coverage; use the relevant existing original inputs for a targeted changed-method review | No compulsory rerun of 92+88 historical first-review slots or relabeling archived scores |
| API/browser and office-agent full-report cases | Check changed Full instructions against the actual task shape and complete-report evidence; revise/review a case only if a concrete case defect is found | No new rewrite solely to certify a method edit |
| Lite/MCP examples and runtime contracts | Offline Lite unresolved-obligation controls and the applicable shared runtime/MCP suite after code edits | Paid provider calls and all-host GUI installation checks |
| Data archive generators and release inventory | New generated-text checks, archive/path map and original-byte preservation tests | Historical ZIPs, original embedded code and source-use declarations |

## Inventory coverage inspected

Machine-readable companion: `output/astra-project-collection-inventory.json`. It records physical collection paths, all seven dedicated IDs, manifest counts, each dated diagnostics/study/repair directory, all 79 asset names from the retained public-access receipt, and direct ZIP row counts. Direct archive cohort parsing confirms **23 development report inputs plus 22 historical paired-study inputs**, along with four historical research runs and eight retained turns. The 50-items/16-parent-topics figure above comes from the repository's historical inventory and was not independently reconstructed by this audit.

| Surface/material | Inspection and useful verification scope |
|---|---|
| Root English/Chinese Skill, README/docs/agent entrypoints, installed plugin wrapper and shared payload builder | Profile/reviewer policy, instructions actually loaded, package-copy boundary |
| Full and Lite workflow, source/claim standard, review roles, writing/quality gates, runtime stage routing and review packet construction | Reusable method coherence; evidence and version scope |
| Seven dedicated task definitions and long-horizon conversation contract | Coverage, source instruction boundary, reader requirements, late corrections and non-final delivery |
| 22 negative and 4 positive mechanical controls | Existing deterministic regression families; original contract versions retained |
| 23 current semantic pairs and revision loader documentation; taste anchors in 4 groups | Reasoning/evidence/reader controls, current versus historical inputs |
| Five development families; calibration v2/v3; dated study/diagnostic inventories | Constrained choice, chronology, attribution, format, length, comparison and judge-input behavior; preserved first attempts |
| Source packs, source policy, optional paired/blinded/intake templates | Provenance, task reuse, condition masking and actual packet construction |
| Two public full-report cases; Lite and MCP example inventories | Full research and ordinary onboarding are distinct from excerpt tests and installation checks |
| Data public release inventory, versioned data cards, current generators | Historical research, repair/environment/recovery tasks, model capture/export, source-use and access distinctions |
| Local `output/agent-runtime-v0.4.zip`, read without extraction/modification | Direct inventory of embedded v0.3/v0.2/v0.1 task and coverage rows; raw reviews were not accepted as proof of current project completion |

This was a source/inventory audit, not a claim to reread every historical report, every source page or every one of the 79 release assets. Public access is reported by the retained receipt; this audit did not independently repeat network access checks. No raw earlier agent review or completion assertion was used as validation of current implementation.

## Optional, not acceptance prerequisites

- A new with/without Toolkit effect study, held-out cohort, multilingual benchmark, fixed judge panel, or formal statistical reliability estimate.
- Re-executing unchanged historical author/reviewer calls or rebuilding released archives.
- A new task-admission system, universal coverage framework, additional mandatory ledgers or expanded source/word quotas.
- Broad profile migration or runtime redesign. The findings above can be addressed using the current version, task, source, review and receipt mechanisms.

The existing code correctly permits same-model independent review in separate requests, keeps author notes/condition maps out of blinded judging, and avoids mandatory extra auditing for ordinary new evaluations. Those properties should be retained and covered by their existing controls rather than replaced with external-person or different-vendor prerequisites.
