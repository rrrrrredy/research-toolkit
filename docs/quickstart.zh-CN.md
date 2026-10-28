# 开始研究：完整研究方法

[English](quickstart.md) · [简体中文](quickstart.zh-CN.md) · [Research Toolkit](../README.zh-CN.md)

从研究需求出发，使用同一套完整方法完成资料研究、分析、长文写作与修订。方法按当前工作读取，正文按用户要求充分展开。

准备好一个能读取文件与研究来源的 Agent，把下面的请求发给它即可。研究方法覆盖需求、来源研究、分析、分节写作、评审和修订；MCP 是可选的任务管理工具。先看成果：[国内办公 Agent 调研](case-study/report.zh-CN.md) · [APIs or browsers](case-study/api-or-browser/report.md)。

## 1. 复制请求，开始研究

下面是一道可直接开始的选型研究示例。换成自己的题目时，一并修改读者、范围、已有材料和篇幅。

```text
使用 Research Toolkit，先阅读 SKILL.md：
https://github.com/rrrrrredy/research-toolkit

为企业知识助手的产品与技术负责人写一份中文选型研究：
RAG、长上下文和混合路线各在什么条件下适用？
研究范围包含文档更新、权限控制、引用定位、回答质量、延迟与成本。
读取截至执行日可取得的原始论文和技术文档，并记录信息截止日。
未给出的企业规模、预算与部署条件作为待验证假设，给出条件化建议。
交付 final.md，整份文件为 6000–8000 个非空白字符，
包括标题、Markdown 标记、引用和参考资料。

先明确需求与提纲，再搜集和阅读来源，让重要判断对应实际依据。
按章节展开证据、比较和反证，形成具体建议与第一步实施安排。
完成任务约定的作者自检；明确要求独立评审时使用已有独立上下文。
不自动追加评审者或审计轮次。
修正具体问题，按受影响内容复查，完成后交付全文。
正文引用使用来源标题和网址，复用已有材料和笔记，保留接续所需信息。
如已选择 CLI/MCP 管理本任务，通过它保存与交付；否则直接使用研究方法。
```

6000–8000 是这个示例的约定，不是通用下限。已有具体题目和材料时直接使用，只澄清会影响研究的关键缺项。Agent 无法读取 GitHub 时，提供[下载后的仓库](https://github.com/rrrrrredy/research-toolkit/archive/refs/heads/main.zip)中的 `SKILL.md` 和所需参考文件。

## 2. 在现有 Agent 中使用

先按 [README 选择入口](../README.zh-CN.md#选哪一种)，只配置需要的一种接入方式：

- **Skill：** 提供仓库或安装 Skill，发送上面的请求。无需执行工具命令，也不要求固定登记表。
- **插件：** 按[插件安装说明](usage-modes.zh-CN.md#安装插件)安装，重开会话并选择 Toolkit。内含 Skill 与 MCP；不再单独装一套 MCP。
- **MCP：** 按[本地 MCP 配置](usage-modes.zh-CN.md#单独接入-mcp)连接，确认九个 `research_*` 工具可见，并让 Agent 读取同一份 Skill。
- **CLI：** 下载仓库，使用 Python 3.10+ 调用 `scripts/research_workflow.py`。下方保留建任务示例，完整命令见[CLI 说明](usage-modes.zh-CN.md#只用-skill或使用-cli)。

检索、浏览来源和写作由 Agent 已有的能力完成。Codex、Cursor 等宿主的具体安装位置与配置见 [Agent 接入说明](../agents/README.zh-CN.md)。

评审方式在任务开始时按现有能力选择：

- **宿主内新上下文：**提供研究任务、完整报告和必要来源，让 Astra 或已有评审者单独形成意见；把意见交回作者修订。无需另找外部人员或另一家模型。
- **CLI/MCP 自动评审：**配置已有的 `codex`、`claude` 或兼容端点后端；由 `research_review` 保存输入、回复和版本绑定，见[后端配置](usage-modes.zh-CN.md#reviewer-backends)。
- **self：**没有后端的新任务默认使用明确标记的自评。若任务已经要求独立评审，就完成该评审。

宿主会话的评审可用于直接使用方法的流程；它不会自动写成 CLI/MCP 的评审记录。选择本地工具管理交付时，通过配置后端完成对应记录。

### 从零研究的步骤

以下用上面的知识助手选型题说明如何推进。用户提供需求、材料和必要决定，Agent 执行后续工作；这不是要求用户逐步调度 Agent 的清单。

| 步骤 | Agent 实际做什么 | 已采用 CLI／MCP 时的对应操作 |
| --- | --- | --- |
| 1. 理解需求 | 明确为谁选型、要比较哪些条件、用什么材料和交付形式；只澄清影响结论的缺项。 | `research_start`／CLI `start` 建立本地任务；已有任务用 `status`。 |
| 2. 阅读与分析 | 阅读原始资料，比较更新、权限、质量和成本等指定问题，解释路线差异与适用条件，保留来源支持及反证。 | 用 `save` 保存实际采用的来源、判断和要求，不把登记网址当成阅读。 |
| 3. 起草 | 按问题组织正文，充分展开比较与理由，给出有条件的建议和可定位引用。 | 用 `save` 保存稿件并登记主稿；方法缺失时才用 `guide`，已有方法无需重取。 |
| 4. 检查与修订 | 阅读当前全文，核对需求、依据和论证；完成约定自检或评审，修正具体问题。 | `review` 完成所选评审；`check-draft` 为可选辅助，不替代正文阅读。 |
| 5. 交付或接续 | 交付当前成果；未完成时保留有效要求、稿件和剩余工作，恢复后从那里继续。 | 完成时 `finish`；恢复时 `status`。工具管理已有记录。 |

表中的 MCP 名称使用 `research_` 前缀（如 `research_save`），CLI 使用对应子命令；不要为同一步同时调用两套接口。纯 Skill 按中间列完成研究，信息保留在可用的对话、材料、引用或已有笔记中，不需照抄右列的记录格式。

### 修订或更新已有报告

1. 提供当前报告、相关来源和修改目标。更新任务还应给出新材料或授权检索，并明确所需截止时间；只有已有稿时，先确定本次能核对的范围。
2. Agent 对照有效要求、现稿及受影响来源，判断哪些事实、条件或推论要变，保留仍成立的分析；不能把来源更新直接当成结论失效。
3. 另存修订稿，核对改动及受影响论证，完成本次任务约定的检查，交付完整当前稿和简短变化说明。

已有工具任务用 `status` 恢复、`save` 更新受影响记录，不重新 `start`。纯 Skill 直接复用旧稿和材料，无需先补建历史台账。可复制的请求及工具详情见[接续已有研究](usage-modes.zh-CN.md#接续已有研究)；[实际更新案例](case-study/coding-benchmark-update/README.zh-CN.md)保留了原稿、来源变化与修改。

## 3. 交付完整成果

默认交付用户要求的报告与可用引用；修订时附简短变化说明。报告应包含有证据的比较、具体结论和适用条件，引用在导出文档中也能定位。台账、评审原件或工具回执只在任务需要时作为附件交付，不是所有报告的必交材料。

采用本地工具管理任务时，按其现有约定完成当前版本评审，再调用 `research_finish`；`research_check_draft` 可辅助检查稿件和明确约定的篇幅，但不是新增必经步骤。

<details>
<summary>可选：用 CLI 建立本地任务和篇幅记录</summary>

从仓库根目录运行，CLI 只需要 Python 3.10+ 标准库，不必安装 MCP 依赖。Linux/macOS 使用 `python3`；Windows 可用 `py -3` 或已有解释器路径。

```bash
python3 scripts/research_workflow.py start --workspace ../research-work --request examples/full/start.zh.json
```

它建立 `../research-work/knowledge-assistant-zh`。示例目录保留旧名称以兼容已有链接，请求使用统一入口。Agent 负责实际检索、读写和分节起草；命令负责创建任务。修改了示例研究问题时，也修改请求文件中的 `brief`；已有任务通过 `status` 恢复。

Agent 通过 `research_save`／CLI `save` 的 `requirements` 参数保存实际约定的篇幅，不让用户编辑 JSONL。先记 `pending`，实际核对后提交带依据的 `satisfied` 更新；见[记录保存示例](usage-modes.zh-CN.md#保存研究记录与稿件)。

自评材料的保存与复用见 [CLI 示例](usage-modes.zh-CN.md#复用任务文件并保存自评材料)，其他档位和交付见[现有调用说明](usage-modes.zh-CN.md)。示例不会预填报告或伪造评审。

</details>

