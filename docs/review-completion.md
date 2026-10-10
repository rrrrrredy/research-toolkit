# Review Completion Records

[English](review-completion.md) | [简体中文](review-completion.zh-CN.md)

[SKILL.md](../SKILL.md) defines the required behavior. This page describes the offline record interface for required model reviews, validity checks, finding dispositions and sampling. [Role instructions](../references/subagents-and-review-loop.md) describe the actual review work.


Profile rules: Lite skips review and full delivery gates, retaining `state/final_checklist.json` and explicit skip logs. Full self records require `reviewer: self` and `review_strength: degraded`, with the author identity as both reviewer and execution_id; they still require a structured review of the current report and the existing Full delivery checks, and cannot fill an independent slot. External uses the configured backend; independent retains the original separate-context requirements. A historical plan without a reviewer field remains independent. See [profiles and backends](../SKILL.md#choosing-a-profile).

## Choose the Completion Question

- **Evaluation:** all declared review slots must have effective results and evidenced dispositions. A valid negative judgment, confirmed sample defect or unresolved source question can be retained as an evaluation outcome.
- **Report delivery:** declared content reviews are complete, required corrections are resolved, and the current report meets its task and delivery checks. Additional auditing follows the declared plan.

Run the review-completion check from the repository directory, replacing the task path:

~~~bash
python scripts/check_review_completion.py <task-directory> --artifact final.md
~~~

This command checks the declared review plan in `state/progress.json` and the records in `logs/review.jsonl`. It does not call a model, retry a request, edit a report or charge a provider. Its exit status reports record consistency, not whether the report is good.

The delivery checker uses **contract 3** by default and includes this check for terminal report delivery. The eval runner applies it to terminal records even when the case's optional delivery-receipt check is disabled. Use the standalone command for evaluation-panel completion; an offline report-conformance score is a different result.

## Review Plan

The shared workflow includes the role reference's [content-review methods](../references/subagents-and-review-loop.md#assign-work-by-perspective) in the reviewer instructions. The existing reviewer checks question coverage, evidence, comparable measures and reader usefulness with those methods; this adds no review slot. The supplied methods are retained in the original request and included in the assignment signature. A methods update does not rewrite completed results or automatically rerun them.

For ordinary reports the executor writes `audit_required: false`. Complete `model_review` records, original responses, execution captures, dimension coverage and input bindings remain required; `review_audit` and `sampling_audit` are not required. Delivery requires no unresolved necessary correction. A justified `no_change` disposition can clear a mistaken finding without replacing the original negative verdict; `optional` suggestions do not block delivery. The global result summarizes the reviews and their dispositions without another model call.

Evaluations, configured audits and existing plans without this field retain the audited contract. Do not add `audit_required: false` to frozen evaluations to change their completion conditions.

Add `review_plan` to the existing progress record. It contains:

| Field | Meaning |
| --- | --- |
| `purpose` | `evaluation` or `report_delivery`; the delivery checker requires the latter |
| `audit_required` | `false` for ordinary reports; omitted or `true` for audited plans, including evaluations |
| `author_id` | Identity of the author context |
| `artifact_sha256` | Hash of the actual primary artifact |
| `slots` | Nonempty list of assignments for the declared reviewer tier |
| `sampling` | Population, method and selected/mandatory ids for declared audited plans |

Each slot has `slot_id`, `reviewer_id`, `model`, `scope`, `dimensions` and `input`. The shared executor also records `reviewer_signature` for the configured reviewer and instructions, plus `auditor_signature` in the plan and audit rows when an auditor is configured. Timeout changes are excluded from these assignment bindings. When present, signatures must match before selecting the first valid result; a prior model's result cannot fill a changed slot. Legacy records without these fields remain inspectable without inventing evidence of earlier execution. Slot ids are unique; external/independent reviewers are not the author, and each dimension is named explicitly. Compatible perspectives may share a slot. There is no fixed provider list in the checker.

`input` is a file reference: `{"path": "reviews/input.json", "sha256": "..."}`. Replace `...` with the actual hash; the fragment illustrates the shape and is not a completed record. Keep the original full task, report, evidence and criteria in the captured input, with any actual provider-envelope transformation documented. A separate hash or a list of source URLs does not establish that the model received full source text.

All referenced files must be nonempty UTF-8 text inside the task directory. Hashing uses the delivery checker's normalization: CRLF and CR become LF for recognized text suffixes. It does not rewrite the original files. Keep credentials out of input and execution captures.

Declare scope, reviewers, inputs and retry policy before examining outcomes. For declared audited plans, also declare the sampling method and record its actual population and selected ids. Local record checks cannot prove when a plan was frozen or that the declared plan captured every user requirement.

## Plan Changes and Historical Attempts

For an explicitly authorized report-delivery assignment change, append a `review_plan_change` row with `revision_authorized: true` and `previous_plan` / `current_plan` file references. Each reference binds the complete retained plan by task-relative path and hash. Changes form a continuous chain ending at the current plan; every snapshot retains its original author, artifact and full slot input bindings. The shared executor creates these records when `revision: true` accompanies a material assignment change. The flag records the caller's authorization declaration; the checker cannot authenticate user consent.

A retired slot is legitimate history only when its record matches an assignment in a verified earlier plan. It does not count toward the current plan. Unknown slots, altered snapshots and broken chains fail. Keep original failures and negative results. Do not reconstruct missing history by inventing earlier plans; recover a legacy change from preserved original plans and actual authorization before accepting it. Frozen evaluation plans cannot use this route to remove or rename reviewers.

## Original Attempts

Append one `model_review` row for each attempt. Keep failures as separate attempts rather than overwriting them.

| Field | Required value or content |
| --- | --- |
| `record_type` | `model_review` |
| `attempt_id`, `slot_id` | Unique attempt and the declared required slot |
| `status` | `completed`, `failed` or `incomplete` |
| `reviewer_id`, `model`, `scope`, `input` | Match the declared slot for an effective review |
| `artifact_sha256` | Match the reviewed artifact |
| `execution_id` | Actual observable request/session/turn identifier, not a fabricated replacement |
| `execution` | Reference to retained execution capture |
| `response` | Reference to the complete original model response, distinct from the execution capture |
| `report_verdict` | `pass`, `needs_revision` or `not_assessed`; separate from attempt completion |
| `coverage` | Object keyed by every declared dimension; each entry has a concrete `location` and `basis` |
| `findings` | List of located observations; use an empty list when justified |

Each finding contains `finding_id`, `severity`, `location` and `basis`. Severity is `critical`, `major`, `minor` or `optional`. Keep quotes, original ratings, source details and suggested changes in the original response or additional fields. Structured records do not replace it.

A completed invocation alone is insufficient: its response must substantively cover the declared dimensions with locations and reasons. Failed or truncated attempts remain incomplete. Declared audited plans additionally require a valid audit. Preserve execution/error evidence and the recovery action.

The same execution id or response file cannot fill two slots. Identical response text is not by itself proof of a duplicate execution; execution provenance and substantive review remain necessary. The checker compares declared model identifiers with the slot; it cannot authenticate provider identity from caller-created files.

## No-change Decisions for Ordinary Reports

After checking a disputed finding against the unchanged report and reviewed sources, the author can append a `finding_disposition` row to the existing `logs/review.jsonl`. This is a finding disposition, not a new model review or audit. No additional file, reviewer or model call is required. Reports without disputed findings need no such row.

This is a **synthetic format example**; use the actual attempt and finding IDs:

```json
{"record_type":"finding_disposition","attempt_id":"actual-attempt-id","finding_id":"F1","decision":"no_change","reason":"The report explicitly says revenue is not reported; the criticism misreads it.","evidence":"final.md paragraph 2 and source.md paragraph 1: no revenue figure is supplied."}
```

Keep the original response, verdict and severity unchanged. `attempt_id` binds the disposition to that review's report and input version; `finding_id` identifies the exact finding. Both `reason` and `evidence` must be nonempty, specific explanations with locatable support. The latest disposition for that pair applies, while earlier decisions remain in the log.

Only `no_change` clears the corresponding finding. `confirmed_defect`, `unresolved` or merely declaring `resolved` does not clear a necessary correction on the unchanged draft. A `needs_revision` verdict can be cleared only when all its necessary findings have evidenced no-change decisions. `not_assessed`, an unexplained negative verdict, missing/invalid reviews and unrelated blockers still prevent delivery. Changed report or source inputs still require current-version review.

Call the existing `research_finish` after recording dispositions. It reconciles the executor's own review summary and binds the retained log to the receipt; it cannot overwrite a separate later global failure. Independent audits and evaluation plans retain their existing requirements. These are record-consistency checks, not certification that an author's no-change decision is correct.

## Validity and Finding Dispositions

This section and the sampling records below apply to declared audited tasks. Ordinary content reviews do not require these additional records.

A `review_audit` row records an actual examination of a particular response:

- `attempt_id`, `auditor_id`;
- `result`: `valid` or `invalid`;
- `response_sha256`: the exact original response being audited;
- `basis`: why the review did or did not substantively address its assignment;
- `evidence`: a file reference to the actual audit record;
- `dispositions`: an object keyed by every finding id in a valid review, with no extra ids.

The reviewer cannot validate or invalidate their own response. Every invalidation also needs a context separate from the author; changing an earlier validity decision cannot bypass independent adjudication. Each disposition needs `decision`, `reason` and a locatable `evidence` explanation. Decisions are `confirmed_defect`, `no_change`, `unresolved` or `resolved`. Report delivery accepts only resolved or justified no-change dispositions; evaluation can retain defects and unresolved evidence outcomes.

Critical/major findings need an auditor context distinct from both the author and original reviewer. The same independence requirement applies under the protocol to decisive disputes and consequential no-change decisions even if a record understates their severity. Scripts cannot infer whether a severity label was honest.

Keep validity audits and their evidence, including invalidations. The checker uses the latest validity decision for an attempt, then the first valid completed attempt in append order for each slot's current artifact and input version. Historical attempts remain in the log under their original slot ids. An authorized report-delivery plan change may retire or rename a slot when its original assignment is bound by the plan history described below. Within that assignment version, an earlier valid negative result cannot be replaced by a later favorable result. A separately authorized report revision needs current-version coverage; keep its input capture at a new path and preserve the earlier report, input and reviews. Changing the plan or input solely to obtain a favorable result is prohibited. Do not invalidate a response merely because it found a defect or made an isolated, adjudicable mistake. Changed validity decisions require actual evidence and remain visible in the log.

If a response is generic, reads the wrong material or omits required dimensions, mark the content audit invalid and complete that missing assignment. Schema compliance alone cannot distinguish a careful review from well-formatted boilerplate.

## Sampling

`review_plan.sampling` contains:

- `method`: the predeclared selection and escalation method;
- `population`: unique ids of candidate items;
- `selected`: unique ids actually selected;
- `mandatory`: decisive items that must all occur in `selected`, possibly empty when none apply.

Every selected item must belong to the population. The protocol requires risk-based full checks plus task-proportionate coverage of passed items, no-change decisions, sections, source types and review slots. The checker checks the declared sets, not whether the population is exhaustive or the selection statistically sound.

Append a `sampling_audit` row with:

- `auditor_id`, separate from the author;
- `artifact_sha256` and `selected`, matching the plan;
- `evidence`, referencing the actual sampling audit;
- `checks`, an object containing every selected item exactly once.

Each check has `result` (`clear` or `defect`) and a locatable `evidence` explanation. A defect additionally needs:

- `defect_type`: `report` or `review_validity`;
- `follow_up.decision`: `resolved`, `no_change`, `confirmed_defect` or `unresolved`;
- `follow_up.reason`: the actual expanded checks, outcome and justification;
- `follow_up.evidence`: a file reference to the completed follow-up work.

Report delivery accepts only resolved or justified no-change sampling dispositions. Evaluation may retain confirmed or unresolved report defects as findings. Review-validity failures require resolved or justified no-change dispositions for either purpose; recording an unresolved failure does not complete the review. A plain future-action string does not satisfy this gate.

The latest sampling record must cover the current artifact and selection. A review or sampling file does not authenticate the identity, independence or diligence of its author.

## Reading the Result

The result includes `required_slots`, `completed_slots`, `selected_attempts`, flags and explanations. `ok` checks the actual plan: ordinary reports do not need audit or sampling records; evaluations and declared audited plans still do.

These fields remain false even on success:

- `execution_authenticity_verified`;
- `semantic_verification`;
- `report_quality_certified`.

Actual execution captures and original responses must be checked against the available runtime/provider evidence. Content auditing must inspect the report and relevant sources. No local JSON schema can prove that a model executed, understood the input or judged correctly.

## Failure Recovery and Compatibility

Preserve each failure, diagnose the cause and resume the required assignment. Bounded retry batches trigger recovery or a request for a concrete missing dependency, not permission to omit a required reviewer. Do not retry valid negative reviews or silently substitute a specified model.

Contracts 1 and 2 remain available only for labelled historical record inspection. They do not check this model-review contract. Keep frozen research inputs, original responses and historical failures unchanged; new records are not retrospective evidence of earlier execution.

~~~bash
python scripts/check_delivery.py <historical-task-directory> --contract-version 2
python scripts/run_evals.py --delivery-contract-version 2
~~~

The new record types coexist with whole-report delivery review rows in `logs/review.jsonl`. Attempt failures do not become unresolved editorial findings, and a global delivery PASS cannot erase a missing model slot. The delivery receipt binds the log and progress; file references in the plan and audit rows bind the retained inputs, responses and evidence.

For synthetic positive/negative record controls, run:

~~~bash
python scripts/check_review_completion_contract.py
~~~

Those fixtures are labelled synthetic and exercise consistency rules. They are not model calls or evidence of review quality.
