---
name: research-toolkit
description: "Source-backed longform research workflow for AI agents: scope, sources, claims, and independent review."
---

# Research Toolkit

Use for substantial industry, market, company, product, technology, policy and ecosystem research reports. Not for quick facts or short summaries.

Read the bundled [research instructions](../../SKILL.md) first. Keep research in a separate task directory; the execution tools return its location.

Use the bundled research tools when available. The CLI fallback uses the same implementation at `../../scripts/research_workflow.py`; pass a JSON request through stdin or `--request <file>`. Read the [usage guide](../../README.md) for setup.

1. Assemble concrete coverage, questions to answer and expected results from the conversation, then call `research_start` with that brief and a short task ID. Treat returned `missing_fields` and `clarification_questions` as guidance for the agent, not a form to forward. Fill inferable details and record non-critical defaults as proposals; ask only about consequential choices that cannot be inferred, explaining the actual alternatives. Merge resolved details by calling start again while the task is in the brief stage. Inspect `review_readiness` before collecting evidence: resolve blocked dependencies or login, and verify access for a custom reviewer command. A local login check does not establish model availability or quota.
2. Call `research_status` as the task moves through collection, analysis and drafting. Read the stage guidance returned. Save source texts, source/claim records and the report in the returned task directory. The tools do not search or write the report for you.
3. Call `research_review` with the report path, full evidence paths and correct purpose. Ordinary reports use the configured content reviewer without a compulsory second audit context. Retain original responses and resume missing work. Evaluations and explicitly configured audits retain their declared requirements.
4. Resume only missing reviews/audits after a recoverable failure. A valid negative review is complete. Evaluation reports stay unchanged; use findings to improve the Toolkit. A separate report-delivery task may require corrections and explicitly authorized current-version review.
5. For report delivery, record any evidenced no-change decisions in the existing review log using the [record guide](../../docs/review-completion.md#no-change-decisions-for-ordinary-reports), then call `research_finish` with the intended delivery message. It runs the existing delivery checks and creates terminal state only if they pass. If it fails, work on the concrete remaining items and keep the task nonterminal.

Use `research_guide` to read a stage's methods without creating a task. Chinese guidance is available with `language: "zh"`.

If MCP is unavailable, invoke the corresponding CLI action (`start`, `status`, `review`, `finish`, `guide`) from the plugin. Never substitute a mock response, self-authored PASS or failed invocation for an effective model review. These tools enforce their own completion conditions; they do not certify semantic truth or prevent every possible host-agent mistake.
