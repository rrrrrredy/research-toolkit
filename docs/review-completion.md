# Independent review, audit and acceptance

[English](review-completion.md) | [简体中文](review-completion.zh-CN.md)

This page describes how the existing `research_review` and completion checker retain independent work. The [role reference](../references/subagents-and-review-loop.md) owns the substantive methods. New research and continued deliveries use the current contract; frozen results retain their original contract and history.

## Conduct the independent work

The agent tool runs the agents. Toolkit prepares their inputs, preserves outputs and reports which work remains. Codex/Claude Code subagents use the agent tool's existing access; no separate API setup is required.

| Assignment | Independent responsibility |
| --- | --- |
| Three content review groups | Independent non-author contexts for requirements, structure and depth, and reader usefulness in one group, evidence and adversarial reasoning in one, and process language and natural expression in one. Each sees the current whole report and necessary originals. |
| Domain review | Add a named specialist context when a consequential conclusion needs domain expertise. |
| Audit | A different agent examines review validity, consequential findings and decisions, decisive report claims and samples of passed content. It can return necessary corrections. |
| Final check | Another independent agent records its initial reading before receiving review verdicts, then reconciles its observations with the audit and actual revisions. The agent delivers the checked version after any necessary corrections. |

Authors, research contributors and the assembling agent are production participants. They may explain or correct their work but cannot fill independent assignments about it. Use actual agent task/session identities; changing a label within the author's context is not another agent. Models may be the same.

Register the main manuscript's actual producing context through the existing `research_save` draft `host_task` (with `main: true` when selecting the main manuscript). Compatible older save inputs still work, but an unregistered main author must be identified before independent assignments are prepared. Earlier producer identities stay in the activity history and remain excluded from independent roles.

Early review of an outline, assumption, calculation or argument unit checks the input on which further work depends. It is saved against that unit's artifact and sources. It does not count as whole-report review or final acceptance. The final perspectives consider the complete assembled argument, including cross-section consistency.

## Native requests and original results

Call `research_review` with the current task, artifact and evidence paths. With no configured external executor, it returns pending native-agent assignments and retained complete inputs. The agent tool launches each required independent agent with the assignment and access to original files.

An illustrative submission shape is:

```json
{
  "task": "study",
  "artifact": "reports/current.md",
  "evidence_paths": ["sources/primary.md"],
  "host_result": {
    "slot_id": "copy-the-returned-slot-id",
    "host_task": "actual-independent-agent-task-id",
    "response_path": "reviews/host/original-response.json",
    "execution_path": "reviews/host/original-execution.json"
  }
}
```

These are placeholders, not a completed review. Preserve the actual original response and execution record as nonempty UTF-8 files inside the task. The returned assignment specifies the response content. Do not construct a favorable reply from the author's interpretation, replace a negative response, or invent an agent tool identifier. Record failed and incomplete attempts too.

Each returned `assignments` entry provides `slot_id`, `role`, `assignment_ref` and `assignment_version`; the operation also returns `input_version`. The original JSON response must quote both versions. The original execution record identifies `host_task`, `status: "completed"`, `assignment_version` and the actual observed agent tool events. These must come from the execution that produced the response.

`scope` defaults to `full_report`. A new v3 plan covers all seven perspectives across three groups and starts with `domains: []`. Supply the specific domains needed for this report. For an early unit review, use its registered `unit_id` as `scope` and select relevant `perspectives`. Omitted selections persist on continuation. Full-report duties stay in place when a unit has already been reviewed.

When a unit needs independent adjudication of a necessary finding or a supported no-change response, use the same `research_review` call with `audit: true`. Existing content reviews of that input stay valid; the next assignment is the unit auditor. The enabled audit remains required on continuation and cannot be removed with `audit: false`. A unit does not acquire final acceptance. Full-report audit is always required. Unit audit covers `applicable_requirements` (global requirements and those assigned to the unit or its upstream dependencies); all effective requirements remain available as context.

The same operation accepts content results, prepares the independent audit, and then prepares final acceptance when the necessary work is resolved. Repeated calls with unchanged valid results resume pending work rather than generating another pass. Each pending assignment returns a `reading_ref` entry alongside the frozen JSON `assignment_ref`; [usage](usage-modes.md) describes the complete reading view. `include_assignment` defaults to `false`; every worker must still be able to read the full input and referenced source originals.

After a submission, `submission_recorded: true` confirms that the result was saved. `delivery_ready` reports whether the whole report has passed its independent checks. Use `summary: true` with MCP `research_review` or `--summary` with CLI `review` to see both states, pending assignment and issue counts, and `action_required`. To retrieve assignment references and issue details, call review again with the same inputs, omitting the submission and summary option.

Frozen role requests may contain `shared_input` with the relative path and SHA-256 of the complete shared input. Earlier requests can contain the input inline under `assignment` and remain readable. Use `reading_ref` for native agents or set `include_assignment=true` to receive the complete request inline through the tool.

Configured command/endpoint execution is optional; see [usage](usage-modes.md#reviewer-backends). It must fulfill the same independence and current-version requirements. Legacy `self` results remain readable historical records; they are author checks, not the current independent review route.

## Inputs and version binding

Retain the actual brief, effective requirements, report, source and claim records, selected original sources and method instructions used by each assignment. Supporting and registered counter-evidence sources enter the review input together. A URL list or the author's summary cannot replace necessary source text.

The plan and each result bind the artifact and required input versions. Inputs, instruction snapshots, original responses and execution captures remain in the task. Text hashes normalize newlines; they do not modify the original research records. File references must resolve inside the task and match their hashes.

New full-report tasks use `progress.review_contract: 3` and `review_plan.contract_version: 3`. Saved v2 tasks retain the seven separate assignments and their historical completion rules. The existing review log and frozen role requests retain original responses and the extra v3 phases. Review-contract numbers are separate from the delivery checker's contract number.

After a substantive edit, save the new report or source version and use `revision: true` for the affected review. Preserve earlier assignments and responses. Current whole-report acceptance must cover the final text. Historical results are evidence of what was checked then, not automatic approval of later prose.

Revision assignments keep each role's last actually completed original response and frozen input in `revision_context`. Work survives intervening revisions with no new response or only some roles responding. `resume_host_task` identifies the original independent agent for the same responsibility, so the agent tool can continue that task directly. If it is unavailable, pass these originals to a new independent context. Audit and acceptance also retain access to the original replies from all review roles.

In these continuation assignments, `report_changes` includes before/after text and line locations relative to the draft that role actually reviewed. `changed_materials` and `changed_context` locate material and task-content changes relative to its reviewed input. Each retained entry in `reviews` records that work's `input_version`, perspectives and domain. Plan-level `changed_inputs`/`unchanged_inputs` still compare adjacent input versions; roles may have read different versions, so continue from their own originals and the above differences. Full texts remain available; differences help locate work.

`prior_required_findings` carries necessary findings from all three roles; audit/acceptance defects retain their original `critical_checks`, `sample_checks` or `open_issues` locations, using `attempt_id/field/index` as the existing audit-disposition key. A negative judgment expressed only in `basis` is retained there. Original inputs, replies and executions stay version-bound; a new draft does not clear their findings. The auditor accounts for each against the current text in the existing `prior_findings`, and acceptance receives that audit together with the originals. Use these to recover earlier checks and examine affected reasoning while confirming the complete current artifact; do not automatically carry an old PASS forward. Already frozen assignments remain unchanged.

## Findings and necessary corrections

An effective review includes located observations, the source or reasoning behind them, and coverage of the assigned perspective. A valid negative result completes that review; it leaves its necessary corrections open. A generic PASS, truncated reply or wrong-input response does not complete the assignment.

Keep the original verdict and severity. The author may propose a correction or a supported no-change response. Independent adjudication checks whether the criticism is mistaken, has been resolved in the actual text, or remains unresolved. Authors cannot clear their own required findings by appending a disposition. Optional preferences need not become changes; important no-change decisions must be inspected against the original report and evidence.

Do not rerun an unchanged valid negative review until it passes. Revisit the changed or genuinely missing work. A response may contain an isolated mistake without invalidating the rest of its substantive review; retain and adjudicate the actual finding.

## Audit and sampling

The auditor reads the complete current report, requirements, review outputs and relevant original material. It selects checks from that input rather than receiving only author-selected highlights.

The v3 request supplies `audit_scaffold` with actual finding IDs, locations and details, possible duplicate groups and coverage items. The auditor confirms which findings can share one decision. Check equivalent findings at the same location once. Submit one `disposition_groups` entry for that evidence and judgment, with `finding_ids`, `decision`, `reason` and `evidence`. `prior_finding_groups` works the same way for previous-version findings. The tool checks that every ID is covered exactly once and retains the original findings and reviewed decision.

**Availability**　This command is available in the [repository source](https://github.com/rrrrrredy/research-toolkit) after v3.0.0. Each pending auditor assignment includes a `response_template_ref` to an editable JSON response skeleton. Run `python scripts/research_workflow.py review --scaffold-audit --workspace WORKSPACE --task TASK` to print the template for the current pending audit. It includes the real review and finding IDs, applicable requirements, input version and assignment version. The independent auditor supplies decisions, reasons, evidence and independently selected samples. To group equivalent findings, move their IDs from individual entries into one `disposition_groups` decision. A blank template fails submission validation.


If a dispute can change delivery and still needs evidence, the auditor can request a focused `verification_requests` assignment. A fresh agent checks just the question before seeing the earlier verdicts. The auditor uses the returned evidence to settle the dispute. Four matching opinions have the same obligation to show evidence as one.

Check all decisive requirements and conclusions, key numbers and citations, consequential counter-evidence, major findings, important no-change decisions and claimed corrections that affect the result. Sample other passed/no-issue content across the actual research, including branch-to-report transformations, retained conditions and cross-section conclusions.

For each selection, retain its location, reason, evidence examined and result. No fixed first/last/hash paragraph rule or sampling percentage substitutes for this choice. A defect expands examination by its cause—for example the same source, measure, branch or transformation—until the affected work is understood and necessary defects are resolved. The auditor performs this within its existing assignment; no additional sampling role or scoring system is needed.

Review validity, report readiness and final acceptance are separate judgments. An audit can find that a negative review was valid and that the report still needs correction. Final acceptance must inspect the resulting complete report, not merely count passed review records.

For `purpose=evaluation`, preserve the sample and complete the independent assessments on the same input. A valid negative assessment can conclude with `evaluation_complete: true` and `evaluation_verdict: "needs_revision"`. A valid positive assessment returns `"pass"`. The evaluation result has separate delivery eligibility. Use `purpose=report_delivery` for report delivery.

## Run the review and revision loop

For an already registered draft, the coordinator can run the workflow through the current host:

```bash
python3 scripts/research_host.py --workspace ./tasks --task study --host codex --complete --max-active 2 --request study-review.json
```

To register `reports/current.md` after saving its evidence and requirements, pass the following JSON to `research_workflow.py save --workspace ./tasks --request save-draft.json`. Replace the example `host_task` with the actual writing session ID.

```json
{"task":"study","draft":{"path":"reports/current.md","main":true,"complete":true,"host_task":"actual-writer-session-id"}}
```

`study-review.json` selects the same task-relative path using `artifact`. UTF-8 request files with an initial BOM are accepted.

```json
{"artifact":"reports/current.md","evidence_paths":["sources/primary.md"],"domains":[]}
```

Use a JSON object with optional `artifact`, `evidence_paths` and `domains`. `writer_handoff_from` is for an authorized transfer when the recorded writer cannot continue. Two active turns are allowed by default. A host with one active turn can run the independent assignments in sequence. Each assignment retains its own context and original result. The host must support independent execution. See [supported hosts](usage-modes.md#agent-host-execution).

The coordinator queues the work, sends verified corrections to one writer and resumes affected independent work on the changed version. On success, `--complete` returns `status: "completed"` and `completed: true`, and the coordinator delivers the checked report. A blocked status identifies the unfinished work.

The first final check uses a fresh blind reading followed by reconciliation. When that checker sends a report back for correction, a new draft with the same scope, requirements and original sources can return to the same checker after the current audit passes. The checker reads the whole revised report and checks the changes and previous issues. The result is bound to the new version. A changed scope or source set, or an unavailable checker, starts a new blind reading.

## Completion and recovery

After the current report passes independent final checking, pass the current `artifact` and `message` (or `delivery_message`) to `research_finish`. The operation verifies the current evidence and independent results, writes the terminal receipt and returns `completed: true`.

For inspection of a managed task:

```bash
python3 scripts/check_review_completion.py <task-directory> --artifact reports/current.md
```

This reads records and bindings; it does not run another reviewer. Actual substantive review is in the original responses and evidence. Preserve the full responses, not just parsed fields.

If the agent tool cancels, a dependency is unavailable, or a response is malformed, retain the original failure and continue that assignment after the cause is addressed. No fixed execution-duration or model-call threshold changes the research obligations. Same-task writes use the existing task lock; no new coordination service is required.

## Historical records

Keep earlier `model_review`, `review_audit`, `sampling_audit`, dispositions and receipts under the conditions they actually used. Existing 1.x self-review, merged-perspective and optional-audit records do not become v2 acceptance. A continued delivery reuses the original materials and completes the current independent work, without erasing earlier failures or claiming it happened previously. See [compatibility](compatibility.md).

Frozen evaluation fixtures and research comparisons retain their recorded protocols. They describe those studies; they are not default instructions for new research. Software control fixtures are labelled synthetic and do not stand in for actual agent tool execution.
