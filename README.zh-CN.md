# Research Toolkit

[![MIT License](https://img.shields.io/badge/license-MIT-596259)](./LICENSE) [![Framework checks](https://github.com/rrrrrredy/research-toolkit/actions/workflows/framework-checks.yml/badge.svg)](https://github.com/rrrrrredy/research-toolkit/actions/workflows/framework-checks.yml)

[English](./README.md) · [简体中文](./README.zh-CN.md)

**从研究问题或已有材料出发，完成中英文长研究与写作，交付判断具体、来源可查的报告。**

面向行业、公司、技术、政策、科学等多领域的长研究与长文写作。可以从零开展研究，对照来源修订已有报告，也可以在新资料到来后更新判断。Codex、Claude Code 等工具中的 Agent 直接操作 Toolkit，负责研究、写作和独立审阅；报告服务于任务指定的实际读者与用途。Toolkit 用统一入口、研究方法与可选任务工具连接材料、协作和成果。

[**选用与安装**](#选哪一种) · [开始研究](#快速开始) · [看研究案例](#研究案例) · [文档](#文档)

## 一项研究怎样完成？

主 Agent 把握研究问题、当前有效要求和整体判断。研究子 Agent 承担调查、比较、计算及实质写作；指定的统稿 Agent 阅读完整成果和来源，理顺论证，逐步形成一份主稿。不同的独立 Agent 负责内容审阅、审计与最终验收。

| 职责 | 工作怎样连接 |
| --- | --- |
| 任务与上下文 | 共同保留需求、提纲、有效要求及实际依赖；已满足但仍约束后续工作的要求继续可见。 |
| 证据与分析 | 每位研究者取得有边界的问题、相关原始材料和已有判断，交接依据、推理、条件及未决问题。 |
| 成稿与修订 | 按有意义的研究单元推进，先审阅后续分析所依赖的关键前提；完整分析进入明确负责人的主稿，变化返回受影响单元与提纲。 |
| 审阅与交付 | 七项基础视角分别独立审阅，补齐所需领域专审，再完成独立审计和最终验收；必要问题落实到当前正文后交付。 |

这四项是相互连接的职责，不是四个固定 Agent 或四套流程。Codex、Claude Code 等工具负责启动 Agent 和传递消息；Toolkit 提供共同输入、方法、成果关联和完成检查。Agent 工具内的原生协作无需另配 API。 如需脚本执行，使用同一套 [Agent 执行适配器](docs/usage-modes.zh-CN.md#agent-host-execution)，连接你正在使用的 Claude Code、OpenCode 或 Codex。[研究步骤](docs/quickstart.zh-CN.md#从零研究的步骤) · [交接与实际调用](docs/usage-modes.zh-CN.md#研究委派与成果交接)

```mermaid
flowchart LR
  L[主 Agent：问题与提纲] --> R[研究 Agent：证据与实质论证]
  R --> W[指定统稿 Agent：逐步形成主稿]
  R --> U[关键依赖处的独立单元审阅]
  U --> R
  W --> V[七项内容视角＋领域专审]
  V --> A[独立审计]
  A --> F[独立最终验收]
  A -->|必要修正| R
  F --> D[完整报告]
```

## 选哪一种？

**Skill 提供研究方法，CLI 和 MCP 调用同一套本地工具，插件把 Skill 与 MCP 打包安装。** 根据 Agent 环境和任务状态保存需要选择入口，各入口使用相同的研究与写作方法。

| 你的情况 | 用什么、装什么 | 怎样开始 |
| --- | --- | --- |
| 希望已有 Agent 按方法完成研究 | **Skill**：直接读取研究方法，或安装后重复使用。方法本身不依赖 Python 或 MCP；默认首用配置见下文。 | 发送下方研究请求，让 Agent 按需读取方法，用已有能力检索、分析和写作。 |
| 希望方法与任务工具一起接入，Agent 工具支持插件 | **插件**：一次安装包含 Skill 和 MCP；本地工具需要 Python 3.10+ 及 MCP 依赖。 | 按[插件说明](./docs/usage-modes.zh-CN.md#安装插件)安装，重开会话、选用 Toolkit 后提出研究需求。 |
| 需要保存任务状态、恢复工作、关联来源和稿件，Agent 工具支持本地 MCP | **MCP**：配置本地服务；方法仍读同一份 Skill。已有插件时不必重复配置。 | 按[MCP 配置](./docs/usage-modes.zh-CN.md#单独接入-mcp)接入，由 Agent 调用 `research_*` 工具。 |
| 在终端或脚本中工作，或 Agent 工具没有 MCP | **CLI**：下载仓库，使用 Python 3.10+；无需 MCP 依赖。 | Agent 读取同一份 Skill，用[命令行](./docs/usage-modes.zh-CN.md#只用-skill或使用-cli)调用相同的任务工具。 |

第一次使用可直接从 Skill 开始。是否启用任务工具，取决于是否需要持久状态、工具化评审和交付检查，不取决于报告字数；无需把四种方式全部安装或依次使用。只用 Skill 也能完成深度长文，不默认维护工具所需的 CSV、JSONL 或交付回执。

**适合什么任务？** 需要多来源分析、比较、解释或有依据建议的中英文多领域长研究，包括长文内的摘要与局部论证、已有稿修订，以及新证据到来后的接续。单一事实查询、普通翻译或简单润色通常直接使用已有 Agent 即可。材料由 Agent 使用已有检索与访问能力获取并阅读。

[从零做一项研究](./docs/quickstart.zh-CN.md#从零研究的步骤) · [修订或更新已有报告](./docs/quickstart.zh-CN.md#修订或更新已有报告) · [按所用工具安装](./agents/README.zh-CN.md#选择工具)

<a id="使用"></a>

**首次使用会做什么？** 研究方法可直接读取，不必先安装 Skill 或 MCP。在 Codex、Claude Code、OpenCode 中，Agent 默认自动复用或下载完整本地副本，按需用 Python 3.10+ 运行包内脚本，为当前项目配置基础使用记录。未变配置直接复用，包括插件已启用的 hooks 和已有关闭设置。仅新增或变更配置需要由 Agent 工具加载；Codex 已打开的会话需重载或重开以加载这些变更。Agent 根据工具可提供的实际状态判断是否生效，不凭配置文件存在作判断。缺少 Python、无法运行命令、配置或加载不可用或失败时，说明实际状态并继续研究。基础操作事件默认发送，不含聊天、报告和本地路径，可随时关闭。Agent 首次说明一次并自行处理配置，不给用户另设安装步骤。[接入、采集范围与关闭](./docs/usage-data.zh-CN.md)。

## 快速开始

用自己的话向能读取仓库和来源材料的 Agent 提出问题或修改要求。下面是可用的起点，不必填写尚未确定的细节；Agent 利用已有背景提出做法，只澄清会改变成果的重要缺项。可以直接发送仓库链接，首次使用的本地配置由 Agent 按上文处理。

```text
使用 Research Toolkit：https://github.com/rrrrrredy/research-toolkit
先阅读 SKILL.md，按本次任务需要使用相关方法。

我想了解或解决：[研究问题，或已有报告需要修改的内容。]
报告目标读者与用途：[谁会阅读报告、用来做什么，如已知。]
已有材料和明确要求：[如有，提供材料、范围、截止日、格式或篇幅。]

交付能回答上述问题的完整报告和可用引用；修订时附简短变化说明。
```

[**开始研究：统一使用指南**](./docs/quickstart.zh-CN.md)

同一套方法支持长文、深度研究、修订与更新。研究范围、篇幅和深度由需求决定，各 Agent 按工作需要读取方法，完成独立审阅、审计和验收。

**只想审查一份现成报告？** 使用独立 Skill [Research Review](https://github.com/rrrrrredy/research-review/blob/main/README.zh-CN.md)。Toolkit 已包含相应审查能力，现有用户无需重复安装。

已有稿件或新材料？直接[修订或更新已有研究](./docs/usage-modes.zh-CN.md#接续已有研究)，复用已完成的研究与来源。

## 研究案例

**中国微短剧市场：增长结构、平台竞争与产业链价值分配。** 从观看人口、应用活跃和广告变现的不同口径出发，解释平台为什么形成不同经营模式，以及流量、版权、合同和现金承担如何影响各方收益。正文包含平台比较、价值流向和可复算的经营情景。资料截至 **2026 年 11 月 9 日**。

[**在线阅读全文**](https://rrrrrredy.github.io/research-toolkit/case-study/long-research-2026-11/microdrama.zh-CN.html) · [同题英文研究](https://rrrrrredy.github.io/research-toolkit/case-study/long-research-2026-11/microdrama.en.html) · [首稿、来源与独立审阅](./evals/studies/2026-11-09-long-research/reports/microdrama_market_zh/README.md)

另一篇新案例是 **Test-Time Compute**：比较采样、搜索、修订、验证及工具反馈，解释增加计算何时改善结果、何时该改变计算用途。包含方法与证据矩阵、预算分配算例和设计决策树。

[**英文全文**](https://rrrrrredy.github.io/research-toolkit/case-study/long-research-2026-11/test-time-compute.en.html) · [同题中文研究](https://rrrrrredy.github.io/research-toolkit/case-study/long-research-2026-11/test-time-compute.zh-CN.html)

两组中英文报告分别基于各题的冻结材料独立撰写，同题另一语言稿不作为作者输入。[本次 benchmark](./evals/studies/2026-11-09-long-research/README.zh-CN.md) 包含 13 个独立问题、15 份报告，保留首次输出、具体缺陷及修订。此前的办公 Agent、API／浏览器及报告更新案例仍在[历史档案](https://rrrrrredy.github.io/research-toolkit/case-study/index.zh-CN.html)。

<a id="作为-mcp-服务使用"></a>
<a id="评审与验收"></a>
<a id="工具箱组成"></a>

## Agent 接入

| 使用方式 | 入口 |
| --- | --- |
| 直接读取方法 | 发送上面的请求；使用附件或纯文本时，见 [Agent 接入说明](./agents/README.zh-CN.md#直接读取使用)。 |
| 安装 Skill 或插件 | [选择你的 Agent](./agents/README.zh-CN.md#选择工具) · [插件安装](./docs/usage-modes.zh-CN.md#安装插件) |
| 保存进度并调用执行工具 | [MCP 安装与客户端配置](./docs/usage-modes.zh-CN.md#单独接入-mcp) · [CLI](./docs/usage-modes.zh-CN.md#只用-skill或使用-cli) |
| 体验本地工具 | [可运行的 MCP 示例与实际返回](./examples/mcp/README.zh-CN.md)；合成示例说明接口，真实运行记录保留实际审阅范围。 |

九个本地工具提供共同任务上下文、按需方法、来源与分析成果保存、已登记版本日志查询、评审与交付检查。CLI 与 MCP 使用相同实现。MCP 需要 Python 3.10+ 和能启动本地进程的客户端；安装指南覆盖 Windows、macOS 和 Linux。

独立审阅使用 Agent 工具的新上下文，每项必需视角有各自的审阅者；作者和统稿者不审自己的成果。审计与最终验收分别承担独立任务。CLI／MCP 通过同一个 `research_review` 保存 Agent 原始回复及其输入版本。[审阅与验收](./docs/review-completion.zh-CN.md)

<a id="评测集"></a>
<a id="evaluation-results"></a>

## 证据与评测

公开记录保留完整报告、原始失败、评审和修订结果。案例展示具体正文修正，模型对照对应记录中的任务与条件，软件检查覆盖实际测试的流程行为。向更广范围比较 Toolkit 与原生 Agent 的质量或效率，需要研究任务、输入、模型和执行条件可比。

[当前证据与边界](./docs/evaluation-status.zh-CN.md) · [完整报告版本比较](./evals/studies/2026-10-13-before-after/README.zh-CN.md) · [数据集与检查](./evals/README.zh-CN.md) · [历史数据归档](https://github.com/rrrrrredy/agent-trajectory-data/blob/main/docs/PUBLIC-EVALUATIONS.zh-CN.md)

## 文档

| 需要什么 | 入口 |
| --- | --- |
| 研究与写作方法 | [研究指南](./docs/research-guide.zh-CN.md) · [Skill 指令](./SKILL.zh-CN.md) |
| 委派研究与整合成果 | [协作说明与调用](./docs/usage-modes.zh-CN.md#研究委派与成果交接) · [实质研究与交接](./references/subagents-and-review-loop.zh-CN.md#实质研究与交接) |
| 修订报告与更新资料 | [接续已有研究](./docs/usage-modes.zh-CN.md#接续已有研究) |
| 安装与配置 | [Agent 接入](./agents/README.zh-CN.md) · [使用指南](./docs/usage-modes.zh-CN.md) |
| 开发与版本变化 | [贡献指南](./CONTRIBUTING.zh-CN.md) · [更新记录](./CHANGELOG.zh-CN.md) |

[全部文档](./docs/README.zh-CN.md) · [网站](https://rrrrrredy.github.io/research-toolkit/?lang=zh) · [提交失败案例](https://github.com/rrrrrredy/research-toolkit/issues/new?template=failure-case.yml)
