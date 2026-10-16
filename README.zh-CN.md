# Research Toolkit

[![MIT License](https://img.shields.io/badge/license-MIT-596259)](./LICENSE) [![Framework checks](https://github.com/rrrrrredy/research-toolkit/actions/workflows/framework-checks.yml/badge.svg)](https://github.com/rrrrrredy/research-toolkit/actions/workflows/framework-checks.yml)

[English](./README.md) · [简体中文](./README.zh-CN.md)

**从研究问题或已有材料出发，交付判断具体、来源可查的报告。**

适用于行业研究、产品比较、公司分析和技术调研。可以从零开展研究，对照来源修订已有报告，也可以在新资料到来后更新判断。Agent 负责检索、分析与写作，Toolkit 提供研究方法和可选执行工具。

[**开始使用**](#快速开始) · [看研究案例](#研究案例) · [Agent 接入](#agent-接入) · [文档](#文档)

<a id="使用"></a>

## 快速开始

把下面的请求交给能读取仓库和来源材料的 Agent。直接使用研究方法无需安装。

```text
使用 Research Toolkit：https://github.com/rrrrrredy/research-toolkit
先阅读 SKILL.md，按本次任务需要使用相关方法。

研究问题或修改要求：[填写读者与用途。]
范围与篇幅：[填写信息截止日、篇幅及计数口径。]
已有材料：[如有，附来源、链接或已有报告。]

根据任务推荐 Lite 或 Full，简短解释理由，尊重我的选择。
交付引用可用的完整报告；修订时附简短变化说明。
由你维护工作记录，并说明实际完成的检查。
```

| 流程 | 适用情况 | 完成时检查什么 |
| --- | --- | --- |
| [**Lite — 轻量流程**](./docs/quickstart-lite.zh-CN.md) | 边界明确，作者自检满足用途 | 来源／判断记录与作者自检 |
| [**Full — 完整流程**](./docs/quickstart-full.zh-CN.md) | 需要版本化评审、修订处理与交付一致性核对 | 所选评审、修订核对与交付一致性 |

两种流程共用必读材料、证据、分析和写作标准。按任务选择，篇幅不是档位上限；Full 不自动等于独立评审。

**只想审查一份现成报告？** 使用独立 Skill [Research Review](https://github.com/rrrrrredy/research-review/blob/main/README.zh-CN.md)。Toolkit 已包含相应审查能力，现有用户无需重复安装。

已有稿件或新材料？直接[修订、更新或将 Lite 接续为 Full](./docs/usage-modes.zh-CN.md#接续已有研究)，复用已完成的研究与来源。

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

[查看来源、差异与审阅取舍](https://rrrrrredy.github.io/research-toolkit/?lang=zh&case=versions&detail=review#case) · [视频演示](./docs/assets/case-walkthrough.zh-CN.mp4)

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

八个本地工具负责任务记录、阶段方法、评审与交付检查。MCP 需要 Python 3.10+ 和能启动本地进程的客户端；安装指南覆盖 Windows、macOS 和 Linux。

Full 支持作者上下文中的 `self`、配置后端的 `external`，或单独上下文中的 `independent`。Astra 即可承担独立评审，无需外部人员或另一家模型。交付时如实说明实际档位，明确的独立评审要求不能静默降级。[评审配置](./docs/usage-modes.zh-CN.md#评审后端)

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
