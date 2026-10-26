---
name: research-toolkit
description: "Complete research methods for in-depth analysis, long-form reports, revisions and updates."
---

# Research Toolkit

Read the bundled [research instructions](../../SKILL.md). Understand the user's question, purpose, coverage and requested depth. Use the same complete methods for every task; load the sections needed for the current work. Develop evidence, explanations, comparisons and synthesis rather than compressing the answer into a generic brief.

Keep research outside the installation directory. When local tools are available, call `research_start` with the task ID and brief; omit the legacy `profile` parameter. Resume saved tasks with `research_status`. Resolve inferable details yourself and ask only about consequential missing user decisions. Handle records and tool errors without asking the user to manage CSV or JSON.

Use `research_save` for source, claim, requirement and draft records. Reuse unchanged guidance and evidence. Register complete drafts using their existing paths. For tool-managed delivery, use the existing `research_review` and `research_finish` path; without a configured backend, submit an actual author self-review. Follow explicitly agreed independent-review requirements without adding reviewers or audit rounds automatically. For local self-review, `include_assignment: false` returns the frozen input path without repeating its full text.

Fix necessary findings, preserve valid analysis and stop when the requested work is complete. Do not rerun an unchanged report to obtain a different verdict. Saved historical tasks retain their recorded completion requirements; see [compatibility](../../docs/usage-modes.md#historical-task-compatibility).

If MCP is unavailable, the same CLI is at `../../scripts/research_workflow.py`. The methods can also be used directly with the agent's existing tools. See [installation and usage](../../README.md).
