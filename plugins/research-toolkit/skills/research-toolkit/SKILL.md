---
name: research-toolkit
description: "Source-backed longform research workflow for AI agents: scope, sources, claims, and independent review."
---

# Research Toolkit

Use for substantial industry, market, company, product, technology, policy and ecosystem research reports. Not for quick facts or short summaries.

Read the bundled [research instructions](../../SKILL.md) first. Keep research in a separate task directory; the execution tools return its location.

Use the bundled research tools when available. The CLI fallback uses the same implementation at `../../scripts/research_workflow.py`; pass a JSON request through stdin or `--request <file>`. Read the [usage guide](../../README.md) for setup.

1. Assemble concrete coverage, questions to answer and expected results from the conversation. Choose the profile using the bundled instructions, then call `research_start` with that explicit `profile`, brief and a short task ID. Resume an existing task through `research_status`, which preserves its saved profile. Treat returned `missing_fields` and `clarification_questions` as guidance for the agent, not a form to forward. Fill inferable details and record non-critical defaults as proposals; ask only about consequential choices that cannot be inferred, explaining the actual alternatives. Merge resolved details by calling start again with the saved profile while the task is in the brief stage. For Full, inspect `review_readiness` before collecting evidence: resolve blocked dependencies or login, and verify access for a custom reviewer command. A local login check does not establish model availability or quota. Lite skips reviewer setup.
2. Call `research_status` as the task moves through collection, analysis and drafting. Read the stage guidance returned. Save source texts, source/claim records and the report in the returned task directory. The tools do not search or write the report for you.
3. Lite follows the returned compact stage methods and skips `research_review`. For Full, call `research_review` with the report path, full evidence paths and correct purpose. Ordinary reports use the configured content reviewer without a compulsory second audit context. Retain original responses and resume missing work. Evaluations and explicitly configured audits retain their declared requirements.
4. For Full, resume only missing reviews/audits after a recoverable failure. A valid negative review is complete. Preserve original evaluation reports and judgments; use findings to improve the Toolkit. Carry out authorized report repairs in separately saved versions and review those versions. A frozen evaluation uses a separate repair task linked to the same research question; an ordinary report uses `research_review` with `revision: true`. Already authorized corrections do not need another confirmation. Reconcile changed research scope in the task records first.
5. Call `research_finish` with the intended delivery message. Lite returns its six-item author checklist; perform the checks and submit actual results with concrete evidence. For Full, first record any evidenced no-change decisions in the existing review log using the [record guide](../../docs/review-completion.md#no-change-decisions-for-ordinary-reports). The tool creates terminal state only if the selected profile's checks pass. If it fails, work on the concrete remaining items and keep the task nonterminal.

Use `research_guide` with an explicit `profile` to read a stage's methods without creating a task. Chinese guidance is available with `language: "zh"`.

If MCP is unavailable, invoke the corresponding CLI action (`start`, `status`, `review`, `finish`, `guide`) from the plugin, retaining the selected profile. Never present Lite author checks or a degraded Full self-review as independent review. These tools enforce their own completion conditions; they do not certify semantic truth or prevent every possible host-agent mistake.
