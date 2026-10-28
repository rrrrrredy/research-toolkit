# Research Toolkit

[![MIT License](https://img.shields.io/badge/license-MIT-596259)](./LICENSE) [![Framework checks](https://github.com/rrrrrredy/research-toolkit/actions/workflows/framework-checks.yml/badge.svg)](https://github.com/rrrrrredy/research-toolkit/actions/workflows/framework-checks.yml)

[English](./README.md) · [简体中文](./README.zh-CN.md)

**从研究问题或已有材料出发，交付判断具体、来源可查的报告。**

适用于行业研究、产品比较、公司分析和技术调研。可以从零开展研究，对照来源修订已有报告，也可以在新资料到来后更新判断。Agent 负责检索、分析与写作，Toolkit 提供研究方法和可选执行工具。

[**选用与安装**](#选哪一种) · [开始研究](#快速开始) · [看研究案例](#研究案例) · [文档](#文档)

## 选哪一种？

**Skill 提供研究方法，CLI 和 MCP 调用同一套本地工具，插件把 Skill 与 MCP 打包安装。** 它们不是四套研究方法，也不分别对应简报、长文或不同研究深度。

| 你的情况 | 用什么、装什么 | 怎样开始 |
| --- | --- | --- |
| 希望已有 Agent 按方法完成研究 | **Skill**：可直接读仓库，无需安装；常用时安装 Skill。无需 Python 或 MCP。 | 发送下方研究请求，让 Agent 按需读取方法，用已有能力检索、分析和写作。 |
| 希望方法与任务工具一起接入，宿主支持插件 | **插件**：一次安装包含 Skill 和 MCP；本地工具需要 Python 3.10+ 及 MCP 依赖。 | 按[插件说明](./docs/usage-modes.zh-CN.md#安装插件)安装，重开会话、选用 Toolkit 后提出研究需求。 |
| 需要保存任务状态、恢复工作、关联来源和稿件，宿主支持本地 MCP | **MCP**：配置本地服务；方法仍读同一份 Skill。已有插件时不必重复配置。 | 按[MCP 配置](./docs/usage-modes.zh-CN.md#单独接入-mcp)接入，由 Agent 调用 `research_*` 工具。 |
| 在终端或脚本中工作，或宿主没有 MCP | **CLI**：下载仓库，使用 Python 3.10+；无需 MCP 依赖。 | Agent 读取同一份 Skill，用[命令行](./docs/usage-modes.zh-CN.md#只用-skill或使用-cli)调用相同的任务工具。 |

第一次使用可直接从 Skill 开始。是否启用任务工具，取决于是否需要持久状态、工具化评审和交付检查，不取决于报告字数；无需把四种方式全部安装或依次使用。只用 Skill 也能完成深度长文，不默认维护工具所需的 CSV、JSONL 或交付回执。

**适合什么任务？** 需要多来源分析、比较、解释或有依据建议的行业、公司、技术、政策研究，以及长报告、已有稿修订和持续更新。一页选型建议也可能需要这些方法。单一事实查询、普通翻译或简单润色通常直接使用已有 Agent 即可。Toolkit 不自带搜索服务，也不能代替 Agent 获取和阅读材料。

[从零做一项研究](./docs/quickstart.zh-CN.md#从零研究的步骤) · [修订或更新已有报告](./docs/quickstart.zh-CN.md#修订或更新已有报告) · [按宿主安装](./agents/README.zh-CN.md#选择工具)

<a id="使用"></a>

## 快速开始

把下面的请求交给能读取仓库和来源材料的 Agent。直接使用研究方法无需安装。

```text
使用 Research Toolkit：https://github.com/rrrrrredy/research-toolkit
先阅读 SKILL.md，按本次任务需要使用相关方法。

研究问题或修改要求：[填写读者与用途。]
范围与篇幅：[填写信息截止日、篇幅及计数口径。]
已有材料：[如有，附来源、链接或已有报告。]

围绕研究问题充分展开证据、比较、解释与判断，按需读取完整研究方法。
交付引用可用的完整报告；修订时附简短变化说明。
复用已有材料和笔记，保留接续所需信息，并说明实际完成的检查。
```

[**开始研究：统一使用指南**](./docs/quickstart.zh-CN.md)

同一套方法支持长文、深度研究、修订与更新。研究范围、篇幅和深度由需求决定，Agent 按工作需要读取方法并完成约定检查。

**只想审查一份现成报告？** 使用独立 Skill [Research Review](https://github.com/rrrrrredy/research-review/blob/main/README.zh-CN.md)。Toolkit 已包含相应审查能力，现有用户无需重复安装。

已有稿件或新材料？直接[修订或更新已有研究](./docs/usage-modes.zh-CN.md#接续已有研究)，复用已完成的研究与来源。

## 研究案例

<a href="https://github.com/rrrrrredy/research-toolkit/blob/main/docs/case-study/report.zh-CN.md">
<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 600px)" srcset="./docs/assets/repository-case.zh-CN.mobile.dark.png">
  <source media="(max-width: 600px)" srcset="./docs/assets/repository-case.zh-CN.mobile.png">
  <source media="(prefers-color-scheme: dark)" srcset="./docs/assets/repository-case.zh-CN.dark.png">
  <img src="./docs/assets/repository-case.zh-CN.png" alt="国内办公 Agent 调研，2026 年 9 月报告节选：生成文件、修改既有对象和改变业务状态，是不同的交付。" width="840">
</picture>
</a>

**国内办公 Agent 调研。** 比较 Kimi Work、扣子、飞书／豆包工作、悟空、WPS 和 WorkBuddy，区分生成文件、修改既有对象与改变业务状态的能力。

[**阅读完整报告**](./docs/case-study/report.zh-CN.md) · [初稿](./docs/case-study/office-agents/original.zh-CN.md) · [来源与修订记录](./docs/case-study/office-agents/README.md)

<details open>
<summary><strong>一处影响判断的修改：产品方向不等于版本继承</strong></summary>

**修改前：**
> 这是当前产品说明与此前功能路线的接续证据

**修改后：**
> 两个时间点分别展示对象操作和组织上下文协作的产品方向，不足以证明aily与豆包工作的版本继承

两份不同时期的资料能够说明各自的产品方向，却不足以证明版本继承或功能迁移。修订保留能力描述，并收窄了这项推断。

[查看来源、差异与审阅取舍](https://rrrrrredy.github.io/research-toolkit/?lang=zh&case=versions&detail=review#case)

</details>

这份历史报告基于公开资料，信息截至 2026 年 9 月 9 日，部分动态文档于 9 月 10 日核对，未安装实测。另有原生英文研究 [APIs or browsers](./docs/case-study/api-or-browser/report.md)，以及对应的[来源与修订档案](./docs/case-study/api-or-browser/README.md)。

<a id="作为-mcp-服务使用"></a>
<a id="评审与验收"></a>
<a id="工具箱组成"></a>

## Agent 接入

| 使用方式 | 入口 |
| --- | --- |
| 直接读取方法 | 发送上面的请求；使用附件或纯文本时，见 [Agent 接入说明](./agents/README.zh-CN.md#直接读取使用)。 |
| 安装 Skill 或插件 | [选择你的 Agent](./agents/README.zh-CN.md#选择工具) · [插件安装](./docs/usage-modes.zh-CN.md#安装插件) |
| 保存进度并调用执行工具 | [MCP 安装与客户端配置](./docs/usage-modes.zh-CN.md#单独接入-mcp) · [CLI](./docs/usage-modes.zh-CN.md#只用-skill或使用-cli) |
| 体验本地工具 | [可运行的 MCP 示例与实际返回](./examples/mcp/README.zh-CN.md)；重放已提供的作者自评，不调用外部模型。 |

九个本地工具负责任务记录、阶段方法、已登记版本日志查询、评审与交付检查。MCP 需要 Python 3.10+ 和能启动本地进程的客户端；安装指南覆盖 Windows、macOS 和 Linux。

评审支持作者上下文中的 `self`、配置后端的 `external`，或单独上下文中的 `independent`。Astra 即可承担独立评审，无需外部人员或另一家模型。交付时如实说明实际档位，明确的独立评审要求不能静默降级。[评审配置](./docs/usage-modes.zh-CN.md#评审后端)

<a id="评测集"></a>
<a id="evaluation-results"></a>

## 证据与评测

公开记录保留完整报告、原始失败、评审和修订结果，展示具体正文修正与已验证的流程行为，尚不能证明相对原生 Agent 的普遍质量或效率优势。案例、模型对照和软件检查分别回答不同问题。

[当前证据与边界](./docs/evaluation-status.zh-CN.md) · [完整报告版本比较](./evals/studies/2026-10-13-before-after/README.zh-CN.md) · [数据集与检查](./evals/README.zh-CN.md) · [历史数据归档](https://github.com/rrrrrredy/agent-trajectory-data/blob/main/docs/PUBLIC-EVALUATIONS.zh-CN.md)

## 文档

| 需要什么 | 入口 |
| --- | --- |
| 研究与写作方法 | [研究指南](./docs/research-guide.zh-CN.md) · [Skill 指令](./SKILL.zh-CN.md) |
| 修订报告与更新资料 | [接续已有研究](./docs/usage-modes.zh-CN.md#接续已有研究) |
| 安装与配置 | [Agent 接入](./agents/README.zh-CN.md) · [使用指南](./docs/usage-modes.zh-CN.md) |
| 开发与版本变化 | [贡献指南](./CONTRIBUTING.zh-CN.md) · [更新记录](./CHANGELOG.zh-CN.md) |

[全部文档](./docs/README.zh-CN.md) · [网站](https://rrrrrredy.github.io/research-toolkit/?lang=zh) · [提交失败案例](https://github.com/rrrrrredy/research-toolkit/issues/new?template=failure-case.yml)
