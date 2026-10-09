# Research Toolkit

[English](./README.md) · [简体中文](./README.zh-CN.md)

**让 AI Agent 写出判断具体、来源可查、经过独立审阅的研究报告。**

研究方法 · 可调用的执行工具 · 独立审阅。适用于行业研究、产品比较、公司分析和技术调研。

[研究案例](#研究案例) · [使用](#使用) · [工具箱组成](#工具箱组成) · [文档](#文档)

## 研究案例

<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 600px)" srcset="./docs/assets/repository-case.zh-CN.mobile.dark.png">
  <source media="(max-width: 600px)" srcset="./docs/assets/repository-case.zh-CN.mobile.png">
  <source media="(prefers-color-scheme: dark)" srcset="./docs/assets/repository-case.zh-CN.dark.png">
  <img src="./docs/assets/repository-case.zh-CN.png" alt="国内办公 Agent 调研，2026 年 9 月报告节选：生成文件、修改既有对象和改变业务状态，是不同的交付。" width="840">
</picture>

[**完整报告**](./docs/case-study/report.zh-CN.md) · [初稿](./docs/case-study/office-agents/original.zh-CN.md) · [定稿](./docs/case-study/office-agents/revised.zh-CN.md) · [来源与审阅记录](./docs/case-study/office-agents/README.md)

这份报告比较 Kimi Work、扣子、飞书／豆包工作、悟空、WPS 和 WorkBuddy。四处真实修改，涵盖表达、结构、产品关系和模型信息：

<details open>
<summary><strong>去 AI 化表述：把价值铺垫改成具体动作</strong></summary>

**初稿**

> 独立办公Agent的价值，不在于把聊天框搬到桌面，而在于把资料、执行与修改放进同一段工作。

**定稿**

> 独立办公Agent把资料、执行与修改组织在同一工作空间。

缩短开头，并把段末泛泛的“实现方式不同”展开为谁提供工具、谁保存上下文、谁维持设备在线。可能减少文件搬运的判断和运行限制仍保留。

[完整段落与修改理由](https://rrrrrredy.github.io/research-toolkit/?lang=zh&case=writing&detail=reason#case) · [审阅取舍](./docs/case-study/office-agents/reviews.md#去-ai-化表述中间稿与作者编辑记录)

</details>

<details>
<summary><strong>去过程痕迹：删除章节预告，保留研究边界</strong></summary>

**初稿**

> 以下按工作对象、独立工作台、办公套件、桌面执行与商业化展开。依据是公开产品文档和案例，不含安装实测；单一使用记录不代表行业表现。

**定稿开篇**

> 依据公开文档和案例，不含安装实测；部分动态说明于9月10日核对，不倒推为早期版本的能力。

删除“以下按……展开”和“有三个判断值得先说清楚”。必要的来源、实测和案例代表性说明集中到开篇。这里展示的是删除与重排，两段位于稿件的不同位置。

[段落位置与修改理由](https://rrrrrredy.github.io/research-toolkit/?lang=zh&case=process&detail=reason#case)

</details>

<details>
<summary><strong>aily 与豆包工作：收窄版本继承的推断</strong></summary>

**初稿节选**

> 这是当前产品说明与此前功能路线的接续证据

**定稿节选**

> 两个时间点分别展示对象操作和组织上下文协作的产品方向，不足以证明aily与豆包工作的版本继承

两份不同时期的资料可以各自说明产品方向，无法据此认定版本继承或功能迁移。保留各自的能力描述与迁移限制；未证明继承，也不等于证明没有继承。

[来源、差异与审阅取舍](https://rrrrrredy.github.io/research-toolkit/?lang=zh&case=versions&detail=review#case)

</details>

<details>
<summary><strong>扣子用什么模型：区分执行框架与模型供应</strong></summary>

**初稿节选**

> 扣子把原生Agent、托管在云端的第三方Agent和本地接入放在同一协作入口。

**定稿新增**

> 第三方云端模式则在扣子云电脑运行Claude Code、Codex CLI等执行框架，接入扣子提供的模型，不绑定原厂账号与模型。

初稿已区分运行方式与权限；定稿补充原生模型选项和第三方云端的模型供应方式。在这个部署场景中，框架名称不能直接说明底层模型，“扣子提供”也不等于“扣子自研”。

[完整段落、来源与修改理由](https://rrrrrredy.github.io/research-toolkit/?lang=zh&case=analysis&detail=reason#case)

</details>

这是一份历史报告：信息截至 2026 年 9 月 9 日，部分动态文档于 9 月 10 日核对；基于公开资料，未安装实测。稿件变化不构成有无工具箱的对照实验。[评测现状](./docs/evaluation-status.zh-CN.md)

<details>
<summary>案例浏览演示</summary>

[![报告差异、修改理由与审阅取舍的浏览演示](./docs/assets/case-walkthrough.zh-CN.gif)](./docs/assets/case-walkthrough.zh-CN.mp4)

[视频](./docs/assets/case-walkthrough.zh-CN.mp4) · [交互案例](https://rrrrrredy.github.io/research-toolkit/?lang=zh&case=writing#case)

</details>

## 使用

支持插件的 Codex 环境可以一次安装研究方法与 MCP 工具。需要 Python 3.10+、Git 和已登录的 Codex CLI；MCP 使用的 `python` 环境必须包含下方依赖。

```bash
python -m pip install mcp==2.2.0
codex plugin marketplace add rrrrrredy/research-toolkit
codex plugin add research-toolkit@research-toolkit
```

新会话中选择 Research Toolkit，发送研究需求：

```text
研究 2026 年国内办公 Agent 产品，面向 AI 产品与企业办公负责人写作。
比较 Kimi Work、扣子、飞书／豆包工作、悟空、WPS、WorkBuddy。
说明各产品改变哪些文件和业务对象，任务在哪里运行，
以及模型、工具、上下文、权限和人工参与如何影响交付与返工。

以 [日期] 为信息截止日。重要判断附来源，区分公司说法、
媒体体验与实际效果证据，并说明哪些反证可能改变结论。
澄清缺失的研究需求，确认提纲后搜集资料。
```

[安装与配置](./docs/usage-modes.zh-CN.md#安装插件) · [其他 Agent 与 Skill 用法](./agents/README.zh-CN.md) · [单独连接 MCP](./docs/usage-modes.zh-CN.md#单独接入-mcp)

<details>
<summary>无需安装，用于一次研究</summary>

将以下内容与研究需求一起发给能读取仓库、访问来源的 Agent：

```text
本次研究请使用 Research Toolkit：
https://github.com/rrrrrredy/research-toolkit
阅读 SKILL.md，按当前任务需要读取 references/ 下的研究方法。
```

直接读取文件可以使用研究方法；不会自动启动 MCP 或运行模型审阅。无法读取仓库时，使用[文件与附件说明](./agents/README.zh-CN.md#直接读取使用)。

</details>

审阅默认使用已登录的 Codex CLI，在独立上下文中检查任务、报告和证据。调用会发送所提供的材料并消耗模型账户用量。[审阅账户与恢复](./docs/usage-modes.zh-CN.md)

## 工具箱组成

| 组成 | 提供什么 |
| --- | --- |
| **研究方法** | 明确需求、评估来源、形成判断、展开分析、写作和修订；由 Agent 按阶段读取。 |
| **执行工具** | 创建任务、保存进度、加载方法、调用审阅和检查交付条件。 |
| **独立审阅** | 在非作者上下文中检查完整报告及其证据，保留意见与修改取舍。 |

Agent 使用自身的检索、读写和分析能力完成研究。插件将 Skill、方法和本地 MCP 打包在一起；也可以单独使用 Skill 或连接 MCP。

<details>
<summary>五个 MCP 工具</summary>

| 工具 | 功能 |
| --- | --- |
| `research_start` | 建立研究任务，检查需求与审阅配置。 |
| `research_status` | 读取和保存进度，检查阶段所需的来源与主张记录。 |
| `research_guide` | 按阶段加载研究方法。 |
| `research_review` | 绑定稿件与证据，执行审阅并保留回复或失败。 |
| `research_finish` | 检查当前稿件、未解决要求、审阅与交付文本。 |

[工具与执行边界](./docs/usage-modes.zh-CN.md#一次研究如何推进)

</details>

## 文档

| 内容 | 入口 |
| --- | --- |
| 研究方法、写作标准与完整说明 | [研究指南](./docs/research-guide.zh-CN.md) · [按阶段的方法](./references/) |
| 插件、Skill、MCP 与 Agent 接入 | [使用与配置](./docs/usage-modes.zh-CN.md) · [Agent 接入](./agents/README.zh-CN.md) |
| 报告、来源与真实改稿 | [案例档案](./docs/case-study/office-agents/README.md) |
| 评测材料、已知缺陷与证据范围 | [评测集](./evals/README.zh-CN.md) · [评测现状](./docs/evaluation-status.zh-CN.md) |
| 开发、贡献与版本变化 | [贡献指南](./CONTRIBUTING.zh-CN.md) · [更新记录](./CHANGELOG.zh-CN.md) |

[全部文档](./docs/README.zh-CN.md) · [研究指令](./SKILL.zh-CN.md) · [网站](https://rrrrrredy.github.io/research-toolkit/?lang=zh)

欢迎通过 [Issues](https://github.com/rrrrrredy/research-toolkit/issues/new) 提交研究需求、使用反馈或失败案例，通过 [Pull requests](https://github.com/rrrrrredy/research-toolkit/compare) 改进方法和工具。

[![MIT License](https://img.shields.io/badge/license-MIT-596259)](./LICENSE) [![Framework checks](https://github.com/rrrrrredy/research-toolkit/actions/workflows/framework-checks.yml/badge.svg)](https://github.com/rrrrrredy/research-toolkit/actions/workflows/framework-checks.yml)
