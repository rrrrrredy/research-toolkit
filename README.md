# Research Toolkit

[![MIT License](https://img.shields.io/badge/license-MIT-596259)](./LICENSE) [![Framework checks](https://github.com/rrrrrredy/research-toolkit/actions/workflows/framework-checks.yml/badge.svg)](https://github.com/rrrrrredy/research-toolkit/actions/workflows/framework-checks.yml)

[English](./README.md) · [简体中文](./README.zh-CN.md)

**Turn a research question or existing material into a report with concrete judgments and traceable sources.**

Use it for industry research, product comparisons, company analysis and technical research. Start a new study, revise an existing report against its sources, or update conclusions when new material arrives. Your agent researches and writes; Toolkit supplies the methods and optional workflow tools.

[**Start here**](#quick-start) · [See a research case](#research-case) · [Agent setup](#agent-setup) · [Documentation](#documentation)

<a id="usage"></a>

## Quick start

Send this request to an agent that can read the repository and your sources. No installation is needed to use the methods directly.

```text
Use Research Toolkit: https://github.com/rrrrrredy/research-toolkit
Read SKILL.md and follow the methods needed for this task.

Question or revision request: [Include the audience and intended use.]
Scope and length: [Include the information cutoff and counting unit.]
Material: [Attach sources, links or an existing report, if available.]

Recommend Lite or Full for the task, briefly explain why, and respect my choice.
Deliver the complete report with usable citations; include a short change note
when revising. Maintain working records yourself and state the checks performed.
```

| Workflow | When to choose it | Completion |
| --- | --- | --- |
| [**Lite — lightweight workflow**](./docs/quickstart-lite.md) | Bounded research where author checks fit the use | Source/claim records and author checks |
| [**Full — complete workflow**](./docs/quickstart-full.md) | Version-bound review, tracked revisions and delivery consistency checks | Selected review, revision checks and delivery consistency |

Both share the same standards for required reading, evidence, analysis and writing. Choose by the task; length is not a profile cap, and Full does not automatically mean independent review.

**Only need to review an existing report?** Use the standalone [Research Review](https://github.com/rrrrrredy/research-review) Skill. Toolkit already includes these review capabilities; existing users do not need a second installation.

Have a draft or new material? [Revise, update or continue Lite work in Full](./docs/usage-modes.md#continue-existing-research), reusing completed research and its sources.

## Research case

<a href="https://github.com/rrrrrredy/research-toolkit/blob/main/docs/case-study/api-or-browser/report.md">
<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 600px)" srcset="./docs/assets/api-browser-case.en.mobile.dark.png">
  <source media="(max-width: 600px)" srcset="./docs/assets/api-browser-case.en.mobile.png">
  <source media="(prefers-color-scheme: dark)" srcset="./docs/assets/api-browser-case.en.dark.png">
  <img src="./docs/assets/api-browser-case.en.png" alt="APIs or browsers for AI agents. Original English research: choose an execution route by action coverage, verified completion, and recovery." width="840">
</picture>
</a>

**APIs or browsers for AI agents.** An English report drawing on 11 primary sources to compare API calls, DOM automation and visual interaction through completion, recovery and cost.

[**Read the report**](./docs/case-study/api-or-browser/report.md) · [Initial draft](./docs/case-study/api-or-browser/initial.md) · [Sources](./docs/case-study/api-or-browser/sources.md) · [Reviews and revisions](./docs/case-study/api-or-browser/reviews.md)

<details open>
<summary><strong>A revision that changes the decision</strong></summary>

**Before:**
> There is no benefit in preserving this split if the API later covers document generation with adequate permissions and result checking.

**After:**
> If the API later covers document generation with adequate permissions and result checking, the original coverage gap disappears. Retiring the browser step then depends on whether the expected maintenance and recovery savings justify migration and revalidation costs.

The review identified a missing counterexample: replacing a working browser step may cost more than the expected savings. The revision makes that trade-off part of the recommendation.

[Explore the revision](https://rrrrrredy.github.io/research-toolkit/?lang=en&case=migration&detail=reason#case) · [Video walkthrough](./docs/assets/api-browser-walkthrough.en.mp4)

</details>

Public-source analysis dated 10 October 2026, not a deployment test. Also read the [Chinese office-agent comparison](./docs/case-study/report.zh-CN.md) and its [source and revision archive](./docs/case-study/office-agents/README.md).

<a id="use-as-an-mcp-server"></a>
<a id="review-and-acceptance"></a>
<a id="inside-the-toolkit"></a>

## Agent setup

| How you want to use it | Entry |
| --- | --- |
| Read the methods directly | Send the request above; for files or text-only chats, see [agent setup](./agents/README.md#use-without-installation). |
| Install a Skill or plugin | [Choose your agent](./agents/README.md#choose-your-tool) · [Plugin installation](./docs/usage-modes.md#install-the-plugin) |
| Save progress and call workflow tools | [MCP installation and client configuration](./docs/usage-modes.md#connect-mcp-separately) · [CLI](./docs/usage-modes.md#skill-only-and-cli-fallback) |
| Try the local tools | [Runnable MCP example and captured responses](./examples/mcp/README.md); replays a supplied self-review without an external model call. |

The eight local tools manage task records, stage guidance, registered release-log queries, reviews and delivery checks. MCP needs Python 3.10+ and a client that can start a local process; the installation guide covers Windows, macOS and Linux.

Full supports author-context `self`, a configured `external` backend, or `independent` review in a separate context. Astra can provide independent review without an outside person or another vendor. State the tier actually used; an explicit independent-review requirement cannot be silently downgraded. [Review configuration](./docs/usage-modes.md#reviewer-backends)

<a id="evaluation-suite"></a>
<a id="evaluation-results"></a>

## Evidence and evaluations

Public records include complete reports, original failures, reviews and repairs. They show concrete report corrections and tested workflow behavior; they do not yet establish a general quality or efficiency advantage over a native agent. Case studies, model comparisons and software checks answer different questions.

[Current evidence and limits](./docs/evaluation-status.md) · [Complete-report version comparison](./evals/studies/2026-10-13-before-after/README.zh-CN.md) (Chinese) · [Datasets and checks](./evals/README.md) · [Historical data archive](https://github.com/rrrrrredy/agent-trajectory-data/blob/main/docs/PUBLIC-EVALUATIONS.md)

## Documentation

| Need | Entry |
| --- | --- |
| Research and writing methods | [Research guide](./docs/research-guide.md) · [Skill instructions](./SKILL.md) |
| Existing reports and source updates | [Continue existing research](./docs/usage-modes.md#continue-existing-research) |
| Installation and configuration | [Agent setup](./agents/README.md) · [Usage guide](./docs/usage-modes.md) |
| Development and changes | [Contributing](./CONTRIBUTING.md) · [Changelog](./CHANGELOG.md) |

[All documentation](./docs/README.md) · [Website](https://rrrrrredy.github.io/research-toolkit/) · [Submit a failure case](https://github.com/rrrrrredy/research-toolkit/issues/new?template=failure-case.yml)
