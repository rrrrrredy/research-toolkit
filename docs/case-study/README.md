# One report. Three revisions.

This historical AI customer-service report preserves its draft, review, and revision. The changes show defect discovery and repair, not a controlled comparison with and without the toolkit or proof of a general quality gain.

[Interactive case](https://rrrrrredy.github.io/research-toolkit/#case) · [Full English report](report.en.md) · [中文原文](https://github.com/rrrrrredy/research-toolkit/blob/d08dc2d488fb7f00c173d3388cd0841fca1fa09e/evals/diagnostics/2026-09-07/reports/customer-service/repaired.md) · [Review](https://github.com/rrrrrredy/research-toolkit/blob/d08dc2d488fb7f00c173d3388cd0841fca1fa09e/evals/diagnostics/2026-09-07/reports/customer-service/reviews/astra-initial.json)

## 1. Lead with a decision

Give the reader a place to start.

**Original**

> AI customer service has entered production in high-volume, rule-bound operations. The next investment should build the ability to resolve problems sustainably.

**Revised**

> Over the next quarter, prioritize two areas: high-volume requests with explicit rules and verifiable results, and retrieval or reply support where a person makes the final decision. Keep complex disputes and irreversible financial actions out of unattended workflows.

The original already makes a judgment. The revision puts concrete priorities and limits in the opening, so the reader can act on it sooner.

A clear thesis needs a scope: what to do first, where it applies, and when to stop.

*Opening excerpts, translated and shortened. Follow the source links for the full paragraphs.*

[Original source](https://github.com/rrrrrredy/research-toolkit/blob/d08dc2d488fb7f00c173d3388cd0841fca1fa09e/evals/diagnostics/2026-09-07/reports/customer-service/original-framework.md#L1) · [Revised source](https://github.com/rrrrrredy/research-toolkit/blob/d08dc2d488fb7f00c173d3388cd0841fca1fa09e/evals/diagnostics/2026-09-07/reports/customer-service/repaired.md#L7)

## 2. Explain the difference

An average is only the beginning.

**Original**

> A study using adoption data from 5,172 support agents found an average productivity gain of about 15%, with larger gains among less-experienced workers.

**Revised**

> The study included 5,172 workers in total, of whom 1,636 had observations after AI adoption. Gains varied: less-experienced workers benefited more, while the most skilled workers saw little speed improvement and a slight decline in quality. Evaluate outcomes by experience and task difficulty.

The original already mentions variation. The revision separates the total sample from post-adoption observations and adds an adverse result that changes the recommendation.

Analysis connects the result, the exception, and the decision. An average alone cannot tell every team what to do.

*Historical report excerpts, translated and shortened. This is not a new verification of the study.*

[Original source](https://github.com/rrrrrredy/research-toolkit/blob/d08dc2d488fb7f00c173d3388cd0841fca1fa09e/evals/diagnostics/2026-09-07/reports/customer-service/original-framework.md#L49) · [Revised source](https://github.com/rrrrrredy/research-toolkit/blob/d08dc2d488fb7f00c173d3388cd0841fca1fa09e/evals/diagnostics/2026-09-07/reports/customer-service/repaired.md#L75)

## 3. Keep claims within evidence

Show what the source can support.

**Original**

> The vendor case reports a 51.5% automated resolution rate and customer satisfaction rising from 34% to 70%. The original attributes these figures to the customer and notes the lack of a control group.

**Revised**

> The revised report uses the case to describe a deployment sequence: start with a bounded task, authenticate users, connect order data, then expand. Historical figures move to the source notes with the limitation that the original page could not be directly rechecked.

Attribution was already present. Review found a different gap: the source-access limitation needed to sit beside the exact figures. The revision narrows how those numbers are used.

A citation is useful when the claim stays within what can actually be checked.

*Summaries of the two report versions. The archived source-access limitation remains unresolved.*

[Original source](https://github.com/rrrrrredy/research-toolkit/blob/d08dc2d488fb7f00c173d3388cd0841fca1fa09e/evals/diagnostics/2026-09-07/reports/customer-service/original-framework.md#L27) · [Revised source](https://github.com/rrrrrredy/research-toolkit/blob/d08dc2d488fb7f00c173d3388cd0841fca1fa09e/evals/diagnostics/2026-09-07/reports/customer-service/repaired.md#L45)

## Start a research task

Adapted from the case brief. A new run may produce a different report. This request starts the workflow; it does not reproduce the archived result.

```text
Use Research Toolkit for this task:
https://github.com/rrrrrredy/research-toolkit

Research how AI customer service moves from pilots into production.
Compare Intercom, Zendesk, and Salesforce: product mechanisms,
adoption evidence, implementation conditions, and failure modes.
Write for an enterprise AI product lead. End with decisions and
observable signals for the next quarter.

Use information available as of [DATE]. Cite important claims,
distinguish company statements from independent evidence, and
explain what could change your conclusions.

Read SKILL.md first. Clarify any missing requirements and agree
on an outline before collecting sources.
```
