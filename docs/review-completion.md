# Review Completion Records

[English](review-completion.md) | [简体中文](review-completion.zh-CN.md)

[SKILL.md](../SKILL.md) defines the required behavior. This page describes the offline record interface for required model reviews, validity checks, finding dispositions and sampling. [Role instructions](../references/subagents-and-review-loop.md) describe the actual review work.

## Choose the Completion Question

- **Evaluation:** all declared review slots must have effective results and evidenced dispositions. A valid negative judgment, confirmed sample defect or unresolved source question can be retained as an evaluation outcome.
- **Report delivery:** the same review work must be complete, and required report corrections must be resolved. The global delivery review, task requirements and delivery receipt also apply.

Run the review-completion check from the repository directory, replacing the task path:

~~~bash
python scripts/check_review_completion.py <task-directory> --artifact final.md
~~~

This command checks the declared review plan in `state/progress.json` and the records in `logs/review.jsonl`. It does not call a model, retry a request, edit a report or charge a provider. Its exit status reports record consistency, not whether the report is good.

The delivery checker uses **contract 3** by default and includes this check for terminal report delivery. The eval runner applies it to terminal records even when the case's optional delivery-receipt check is disabled. Use the standalone command for evaluation-panel completion; an offline report-conformance score is a different result.

## Review Plan

Add `review_plan` to the existing progress record. It contains:

| Field | Meaning |
| --- | --- |
| `purpose` | `evaluation` or `report_delivery`; the delivery checker requires the latter |
| `author_id` | Identity of the author context |
| `artifact_sha256` | Hash of the actual primary artifact |
| `slots` | Nonempty list of required independent model-review assignments |
| `sampling` | Declared sampling population, method and selected/mandatory item ids |

Each slot has `slot_id`, `reviewer_id`, `model`, `scope`, `dimensions` and `input`. The shared executor also records `reviewer_signature` for the configured reviewer and instructions, plus `auditor_signature` in the plan and audit rows. Timeout changes are excluded from these assignment bindings. When present, signatures must match before selecting the first valid result; a prior model's result cannot fill a changed slot. Legacy records without these fields remain inspectable without inventing evidence of earlier execution. Slot ids are unique, the reviewer is not the author, and each dimension is named explicitly. Compatible perspectives may share a slot. There is no fixed provider list in the checker.

`input` is a file reference: `{"path": "reviews/input.json", "sha256": "..."}`. Replace `...` with the actual hash; the fragment illustrates the shape and is not a completed record. Keep the original full task, report, evidence and criteria in the captured input, with any actual provider-envelope transformation documented. A separate hash or a list of source URLs does not establish that the model received full source text.

All referenced files must be nonempty UTF-8 text inside the task directory. Hashing uses the delivery checker's normalization: CRLF and CR become LF for recognized text suffixes. It does not rewrite the original files. Keep credentials out of input and execution captures.

Declare scope, reviewers, inputs, sampling method and retry policy before examining outcomes. Then record the actual sampling population and selected ids under that method. Local record checks cannot prove when a plan was frozen or that the declared plan captured every user requirement.

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

A completed invocation alone is insufficient: its response must also have a valid audit. A failed or incomplete attempt cannot fill the slot. Failed attempts may lack a response; preserve the available execution/error evidence and the concrete recovery action.

The same execution id or response file cannot fill two slots. Identical response text is not by itself proof of a duplicate execution; execution provenance and substantive review remain necessary. The checker compares declared model identifiers with the slot; it cannot authenticate provider identity from caller-created files.

## Validity and Finding Dispositions

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

The result includes `required_slots`, `completed_slots`, `selected_attempts`, flags and explanations. A `completed_slots` count alone does not establish completion: `ok` also requires valid dispositions, sampling and all other checks.

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
