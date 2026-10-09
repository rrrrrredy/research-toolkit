# Research Toolkit

[English](./README.md) · [简体中文](./README.zh-CN.md)

**Help AI agents write research reports with concrete judgments, traceable sources, and independent review.**

Research methods · Callable workflow tools · Independent review. For industry research, product comparisons, company analysis, and technical research.

[Research case](#research-case) · [Usage](#usage) · [Inside the toolkit](#inside-the-toolkit) · [Documentation](#documentation)

## Research case

<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 600px)" srcset="./docs/assets/repository-case.en.mobile.dark.png">
  <source media="(max-width: 600px)" srcset="./docs/assets/repository-case.en.mobile.png">
  <source media="(prefers-color-scheme: dark)" srcset="./docs/assets/repository-case.en.dark.png">
  <img src="./docs/assets/repository-case.en.png" alt="Office agent research in China. September 2026 report excerpt: creating files, editing existing objects, and changing business state are different deliverables." width="840">
</picture>

[**Full report**](./docs/case-study/report.en.md) · [Initial draft (Chinese)](./docs/case-study/office-agents/original.zh-CN.md) · [Final report (Chinese)](./docs/case-study/office-agents/revised.zh-CN.md) · [Sources and reviews](./docs/case-study/office-agents/README.md)

This report compares Kimi Work, Coze, Feishu / Doubao Work, Wukong, WPS, and WorkBuddy. Four real revisions cover prose, structure, product relationships, and model supply. The excerpts below are translated from the retained Chinese manuscripts.

<details open>
<summary><strong>Direct prose: replace a value claim with an action</strong></summary>

**Initial draft**

> The value of independent office agents lies not in moving a chat box onto the desktop, but in bringing materials, execution, and revisions into one stretch of work.

**Final report**

> Independent office agents organize materials, execution, and revisions in one workspace.

Shorten the opening and replace the vague closing about different implementations with specific criteria: tools, context, and device availability. Keep the conditional benefit of less file handling and the operating limits.

[Full passages and reasoning](https://rrrrrredy.github.io/research-toolkit/?lang=en&case=writing&detail=reason#case) · [Review decisions (Chinese)](./docs/case-study/office-agents/reviews.md)

</details>

<details>
<summary><strong>Process narration: remove an outline announcement, retain the scope</strong></summary>

**Initial draft**

> The following sections cover work objects, independent workspaces, office suites, desktop execution, and commercialization. The evidence consists of public product documents and examples, without installed-product testing; a single use record does not represent industry performance.

**Final opening**

> The research uses public documents and examples, without installed-product testing. Some dynamic descriptions were checked on September 10; their capabilities are not attributed retrospectively to earlier versions.

Delete the outline announcement and the sentence announcing three judgments. Keep source, testing, and sample limits in the opening. This is deletion and reorganization; the excerpts occupy different positions in the report.

[Passage locations and reasoning](https://rrrrrredy.github.io/research-toolkit/?lang=en&case=process&detail=reason#case)

</details>

<details>
<summary><strong>aily and Doubao Work: narrow a product-lineage inference</strong></summary>

**Initial excerpt**

> This is evidence of continuity between the current product description and the earlier feature direction

**Final excerpt**

> The two points in time show product directions in object operations and organizational-context collaboration; they do not establish version inheritance between aily and Doubao Work

The dated sources describe each product direction. They do not establish version inheritance or feature migration. Retain the capability descriptions and migration caveat; lack of evidence for inheritance does not establish that inheritance is absent.

[Sources, changes, and review decisions](https://rrrrrredy.github.io/research-toolkit/?lang=en&case=versions&detail=review#case)

</details>

<details>
<summary><strong>Coze's models: distinguish execution frameworks from model supply</strong></summary>

**Initial excerpt**

> Coze brings native agents, third-party agents hosted in the cloud, and local connections into one collaboration interface.

**Added in the final report**

> Third-party cloud mode runs execution frameworks such as Claude Code and Codex CLI on Coze cloud computers, using models supplied by Coze rather than being tied to the original provider’s account and model.

The draft already described execution modes and permission boundaries. The revision adds native-model choices and third-party cloud-model supply. In this deployment, a framework name does not identify the model; supplied by Coze does not mean developed by Coze.

[Full passages, sources, and reasoning](https://rrrrrredy.github.io/research-toolkit/?lang=en&case=analysis&detail=reason#case)

</details>

Historical report: information through September 9, 2026; some dynamic documents checked on September 10. Public-source research without installed-product testing. These versions are not a controlled with/without-toolkit experiment. [Evaluation status](./docs/evaluation-status.md)

<details>
<summary>Case walkthrough</summary>

[![Report changes, reasoning, and review decisions](./docs/assets/case-walkthrough.gif)](./docs/assets/case-walkthrough.mp4)

[Video](./docs/assets/case-walkthrough.mp4) · [Interactive case](https://rrrrrredy.github.io/research-toolkit/?lang=en&case=writing#case)

</details>

## Usage

In a compatible Codex environment, the plugin installs the research methods and MCP tools together. Requires Python 3.10+, Git, and a signed-in Codex CLI. The `python` environment used by MCP must include the dependency below.

```bash
python -m pip install mcp==2.2.0
codex plugin marketplace add rrrrrredy/research-toolkit
codex plugin add research-toolkit@research-toolkit
```

Select Research Toolkit in a new session and describe the research:

```text
Research office agents available in China in 2026 for AI product
and workplace leads. Compare Kimi Work, Coze, Feishu / Doubao Work,
Wukong, WPS, and WorkBuddy. Explain which files and business objects
each changes, where tasks run, and how models, tools, context,
permissions, and human involvement affect delivery and rework.

Use information available as of [DATE]. Cite important claims.
Distinguish company statements, media experiences, and measured
outcomes. Explain what could overturn your conclusions.
Clarify missing requirements and agree on an outline before research.
```

[Installation and configuration](./docs/usage-modes.md#install-the-plugin) · [Other agents and Skill-only use](./agents/README.md) · [Standalone MCP](./docs/usage-modes.md#connect-mcp-separately)

<details>
<summary>Use the methods for one task without installation</summary>

Send this with your research request to an agent that can read the repository and access your sources:

```text
Use Research Toolkit for this task:
https://github.com/rrrrrredy/research-toolkit
Read SKILL.md and load the methods under references/ as needed.
```

Reading the files applies the research methods. It does not start MCP or automatically run model reviews. If repository access is unavailable, use the [file and attachment guide](./agents/README.md#use-without-installation).

</details>

The default reviewer uses a signed-in Codex CLI in a fresh context to examine the task, report, and evidence. Calls send the supplied material to the model service and consume account usage. [Review accounts and recovery](./docs/usage-modes.md#review-accounts-and-recovery)

## Inside the toolkit

| Component | What it provides |
| --- | --- |
| **Research methods** | Scope, source assessment, judgments, analysis, writing, and revision, loaded by your agent by stage. |
| **Workflow tools** | Task creation, saved progress, method loading, review calls, and delivery checks. |
| **Independent review** | A non-author context examines the whole report and evidence; findings and revision decisions are retained. |

Your agent performs retrieval, reading, analysis, and writing with its own capabilities. The plugin bundles the Skill, methods, and local MCP server. The Skill and MCP can also be used separately.

<details>
<summary>The five MCP tools</summary>

| Tool | Function |
| --- | --- |
| `research_start` | Create a task and check the brief and review configuration. |
| `research_status` | Read and save progress; check source and claim records for stage transitions. |
| `research_guide` | Load the methods for the current stage. |
| `research_review` | Bind the report and evidence, run reviews, and retain replies or failures. |
| `research_finish` | Check the current report, unresolved requirements, reviews, and delivery text. |

[Tools and execution boundaries](./docs/usage-modes.md#what-happens-during-a-task)

</details>

## Documentation

| Topic | Entry |
| --- | --- |
| Research methods, writing standards, and full instructions | [Research guide](./docs/research-guide.md) · [Stage methods](./references/) |
| Plugin, Skill, MCP, and agent setup | [Usage and configuration](./docs/usage-modes.md) · [Agent setup](./agents/README.md) |
| Reports, sources, and real revisions | [Case archive](./docs/case-study/office-agents/README.md) |
| Evaluation materials, defects, and evidence limits | [Evaluation suite](./evals/README.md) · [Evaluation status](./docs/evaluation-status.md) |
| Development, contributions, and releases | [Contributing](./CONTRIBUTING.md) · [Changelog](./CHANGELOG.md) |

[All documentation](./docs/README.md) · [Research instructions](./SKILL.md) · [Website](https://rrrrrredy.github.io/research-toolkit/)

Contribute research questions, usage feedback, or failure cases through [Issues](https://github.com/rrrrrredy/research-toolkit/issues/new), and improve methods and tools through [pull requests](https://github.com/rrrrrredy/research-toolkit/compare).

[![MIT License](https://img.shields.io/badge/license-MIT-596259)](./LICENSE) [![Framework checks](https://github.com/rrrrrredy/research-toolkit/actions/workflows/framework-checks.yml/badge.svg)](https://github.com/rrrrrredy/research-toolkit/actions/workflows/framework-checks.yml)
