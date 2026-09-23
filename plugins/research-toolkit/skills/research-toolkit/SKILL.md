---
name: research-toolkit
description: Execute substantial source-backed research with brief clarification, saved progress, independent model reviews and delivery checks. Use for industry, company, market, product, technology and policy research; not quick facts.
---

# Research Toolkit

Read the bundled [research instructions](../../SKILL.md) first. Keep research in a separate task directory; the execution tools return its location.

Use the bundled research tools when available. The CLI fallback uses the same implementation at `../../scripts/research_workflow.py`; pass a JSON request through stdin or `--request <file>`. Read the [usage guide](../../README.md) for setup.

1. Call `research_start` with a short task ID and the research brief assembled from the conversation. Ask the user only about the missing critical fields returned; merge their answers by calling start again while the task is in the brief stage. Inspect `review_readiness` before collecting evidence: resolve blocked dependencies or login, and verify access for a custom reviewer command. A local login check does not establish model availability or quota.
2. Call `research_status` as the task moves through collection, analysis and drafting. Read the stage guidance returned. Save source texts, source/claim records and the report in the returned task directory. The tools do not search or write the report for you.
3. Call `research_review` with the report path, full evidence file paths and the correct purpose. This starts the configured reviewer and a fresh auditor context, saves original responses, audits validity and samples content. It can use the signed-in Codex CLI or a trusted configured reviewer command.
4. Resume only missing reviews/audits after a recoverable failure. A valid negative review is complete. Evaluation reports stay unchanged; use findings to improve the Toolkit. A separate report-delivery task may require corrections and explicitly authorized current-version review.
5. For report delivery, call `research_finish` with the intended delivery message. It runs the existing delivery checks and creates terminal state only if they pass. If it fails, work on the concrete remaining items and keep the task nonterminal.

Use `research_guide` to read a stage's methods without creating a task. Chinese guidance is available with `language: "zh"`.

If MCP is unavailable, invoke the corresponding CLI action (`start`, `status`, `review`, `finish`, `guide`) from the plugin. Never substitute a mock response, self-authored PASS or failed invocation for an effective model review. These tools enforce their own completion conditions; they do not certify semantic truth or prevent every possible host-agent mistake.
