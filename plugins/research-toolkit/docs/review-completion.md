# Independent review, audit and acceptance

[English](review-completion.md) | [简体中文](review-completion.zh-CN.md)

This page describes how the existing `research_review` and completion checker retain independent work. The [role reference](../references/subagents-and-review-loop.md) owns the substantive methods. New research and continued deliveries use the current contract; frozen results retain their original contract and history.

## Conduct the independent work

The host runs the agents. Toolkit prepares their inputs, preserves outputs and reports which work remains. Codex/Claude Code subagents use the host's existing access; no separate API setup is required.

| Assignment | Independent responsibility |
| --- | --- |
| Seven content perspectives | A separate non-author context for each: requirements, evidence, adversarial reasoning, structure and depth, reader usefulness, process language, natural expression. Each sees the whole current report and necessary originals. |
| Domain review | Check task-specific expertise, calculations, terminology or technical assumptions. It supplements the base perspectives. |
| Audit | A different agent examines review validity, consequential findings and decisions, decisive report claims and samples of passed content. It can return necessary corrections. |
| Final acceptance | Another independent agent reads the complete current report, effective requirements, audit and actual corrections before accepting delivery. |

Authors, research contributors and the assembling agent are production participants. They may explain or correct their work but cannot fill independent assignments about it. Use actual host task/session identities; changing a label within the author's context is not another agent. Models may be the same.

Register the main manuscript's actual producing context through the existing `research_save` draft `host_task` (with `main: true` when selecting the main manuscript). Compatible older save inputs still work, but an unregistered main author must be identified before independent assignments are prepared. Earlier producer identities stay in the activity history and remain excluded from independent roles.

Early review of an outline, assumption, calculation or argument unit checks the input on which further work depends. It is saved against that unit's artifact and sources. It does not count as whole-report review or final acceptance. The final perspectives consider the complete assembled argument, including cross-section consistency.

## Native requests and original results

Call `research_review` with the current task, artifact and evidence paths. With no configured external executor, it returns pending native-host assignments and retained complete inputs. The host launches each required independent agent with the assignment and access to original files.

An illustrative submission shape is:

```json
{
  "task": "study",
  "artifact": "reports/current.md",
  "evidence_paths": ["sources/primary.md"],
  "host_result": {
    "slot_id": "copy-the-returned-slot-id",
    "host_task": "actual-independent-host-task-id",
    "response_path": "reviews/host/original-response.json",
    "execution_path": "reviews/host/original-execution.json"
  }
}
```

These are placeholders, not a completed review. Preserve the actual original response and execution record as nonempty UTF-8 files inside the task. The returned assignment specifies the response content. Do not construct a favorable reply from the author's interpretation, replace a negative response, or invent a host identifier. Record failed and incomplete attempts too.

Each returned `assignments` entry provides `slot_id`, `role`, `assignment_ref` and `assignment_version`; the operation also returns `input_version`. The original JSON response must quote both versions. The original execution record identifies `host_task`, `status: "completed"`, `assignment_version` and the actual observed host events. These must come from the execution that produced the response.

`scope` defaults to `full_report`. `domains` names required specialist areas; a new full-report plan defaults to `["domain"]` and includes all seven base perspectives. For an early unit review, use its registered `unit_id` as `scope` and select relevant `perspectives`. A new unit defaults to `domains: []`; previously declared specialists remain selected when the parameter is omitted. Unit review does not remove final whole-report duties.

When a unit needs independent adjudication of a necessary finding or a supported no-change response, use the same `research_review` call with `audit: true`. Existing content reviews of that input stay valid; the next assignment is the unit auditor. The enabled audit remains required on continuation and cannot be removed with `audit: false`. A unit does not acquire final acceptance. Full-report audit is always required. Unit audit covers `applicable_requirements` (global requirements and those assigned to the unit or its upstream dependencies); all effective requirements remain available as context.

The same operation accepts content results, prepares the independent audit, and then prepares final acceptance when the necessary work is resolved. Repeated calls with unchanged valid results resume pending work rather than generating another pass. `include_assignment` defaults to `false`, using retained input references; every worker must still be able to read the full packet and referenced source originals.

Configured command/endpoint execution is optional; see [usage](usage-modes.md#reviewer-backends). It must fulfill the same independence and current-version requirements. Legacy `self` results remain readable historical records; they are author checks, not the current independent review route.

## Inputs and version binding

Retain the actual brief, effective requirements, report, source and claim records, selected original sources and method instructions used by each assignment. Supporting and registered counter-evidence sources enter the review input together. A URL list or the author's summary cannot replace necessary source text.

The plan and each result bind the artifact and required input versions. Inputs, instruction snapshots, original responses and execution captures remain in the task. Text hashes normalize newlines; they do not modify the original research records. File references must resolve inside the task and match their hashes.

Current tasks use `progress.review_contract: 2` and `review_plan.contract_version: 2`. The existing `logs/review.jsonl` retains `model_review` and `review_audit` records plus the independent `final_acceptance`. These are review-contract identifiers, distinct from the delivery checker's contract number.

After a substantive edit, save the new report or source version and use `revision: true` for the affected review. Preserve earlier assignments and responses. Current whole-report acceptance must cover the final text. Historical results are evidence of what was checked then, not automatic approval of later prose.

New revision assignments include `revision_context`: the prior frozen input, the same perspective's retained original reply and execution reference, input hashes identifying changed and unchanged material, and before/after report lines. Auditors and acceptance agents can consult the retained content-review references. Use these to recover earlier checks and examine affected reasoning while confirming the complete current artifact; do not automatically carry an old PASS forward. Already frozen assignments remain unchanged.

## Findings and necessary corrections

An effective review includes located observations, the source or reasoning behind them, and coverage of the assigned perspective. A valid negative result completes that review; it leaves its necessary corrections open. A generic PASS, truncated reply or wrong-input response does not complete the assignment.

Keep the original verdict and severity. The author may propose a correction or a supported no-change response. Independent adjudication checks whether the criticism is mistaken, has been resolved in the actual text, or remains unresolved. Authors cannot clear their own required findings by appending a disposition. Optional preferences need not become changes; important no-change decisions must be inspected against the original report and evidence.

Do not rerun an unchanged valid negative review until it passes. Revisit the changed or genuinely missing work. A response may contain an isolated mistake without invalidating the rest of its substantive review; retain and adjudicate the actual finding.

## Audit and sampling

The auditor reads the complete current report, requirements, review outputs and relevant original material. It selects checks from that input rather than receiving only author-selected highlights.

Check all decisive requirements and conclusions, key numbers and citations, consequential counter-evidence, major findings, important no-change decisions and claimed corrections that affect the result. Sample other passed/no-issue content across the actual research, including branch-to-report transformations, retained conditions and cross-section conclusions.

For each selection, retain its location, reason, evidence examined and result. No fixed first/last/hash paragraph rule or sampling percentage substitutes for this choice. A defect expands examination by its cause—for example the same source, measure, branch or transformation—until the affected work is understood and necessary defects are resolved. The auditor performs this within its existing assignment; no additional sampling role or scoring system is needed.

Review validity, report readiness and final acceptance are separate judgments. An audit can find that a negative review was valid and that the report still needs correction. Final acceptance must inspect the resulting complete report, not merely count passed review records.

## Completion and recovery

`research_finish` checks the current report, effective requirements and completed independent responsibilities before writing terminal state and the receipt. The author does not hand-write a replacement global PASS or receipt to close missing work.

For inspection of a managed task:

```bash
python3 scripts/check_review_completion.py <task-directory> --artifact reports/current.md
```

This reads records and bindings; it does not run another reviewer. Actual substantive review is in the original responses and evidence. Preserve the full responses, not just parsed fields.

If the host cancels, a dependency is unavailable, or a response is malformed, retain the original failure and continue that assignment after the cause is addressed. No fixed execution-duration or model-call threshold changes the research obligations. Same-task writes use the existing task lock; no new coordination service is required.

## Historical records

Keep earlier `model_review`, `review_audit`, `sampling_audit`, dispositions and receipts under the conditions they actually used. Existing 1.x self-review, merged-perspective and optional-audit records do not become v2 acceptance. A continued delivery reuses the original materials and completes the current independent work, without erasing earlier failures or claiming it happened previously. See [compatibility](compatibility.md).

Frozen evaluation fixtures and research comparisons retain their recorded protocols. They describe those studies; they are not default instructions for new research. Software control fixtures are labelled synthetic and do not stand in for actual host execution.
