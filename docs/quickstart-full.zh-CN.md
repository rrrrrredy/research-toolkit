# 完整流程（Full）：从研究到评审与交付

[English](quickstart-full.md) · [简体中文](quickstart-full.zh-CN.md) · [Research Toolkit](../README.zh-CN.md)

与 [Lite](quickstart-lite.zh-CN.md) 共用研究底线。需要跟踪要求与证据变化，并保留版本化评审、修订处置和交付核对时，选择 Full。Lite 同样处理复杂比较与冲突证据；根据实际流程需要选择，篇幅只作辅助。已有稿件可[接续 Full](usage-modes.zh-CN.md#接续已有研究)。

准备好一个能读取文件与研究来源的 Agent，把下面的请求发给它即可。Full 覆盖需求、来源研究、分析、分节写作、评审和修订；MCP 是可选的任务管理工具。先看成果：[国内办公 Agent 调研](case-study/report.zh-CN.md) · [APIs or browsers](case-study/api-or-browser/report.md)。

## 1. 复制请求，开始研究

下面是一道可直接开始的选型研究示例。换成自己的题目时，一并修改读者、范围、已有材料和篇幅。

```text
使用 Research Toolkit，先阅读 SKILL.md，选择 profile=full：
https://github.com/rrrrrredy/research-toolkit

为企业知识助手的产品与技术负责人写一份中文选型研究：
RAG、长上下文和混合路线各在什么条件下适用？
研究范围包含文档更新、权限控制、引用定位、回答质量、延迟与成本。
读取截至执行日可取得的原始论文和技术文档，并记录信息截止日。
未给出的企业规模、预算与部署条件作为待验证假设，给出条件化建议。
交付 final.md，整份文件为 6000–8000 个非空白字符，
包括标题、Markdown 标记、引用和参考资料。

先明确需求与提纲，再搜集和阅读来源，登记来源与重要判断。
按章节展开证据、比较和反证，形成具体建议与第一步实施安排。
优先沿用已可用的新上下文完成独立评审；Astra 可以承担这一角色。
若没有单独评审上下文且任务未要求独立评审，使用 self 并注明。
修正具体问题，按受影响内容复查，完成后交付全文。
来源与判断记录、评审意见及修改结果另存；正文引用使用来源标题和网址。
有 CLI/MCP 时用它保存进度、计数和完成交付；否则直接使用研究方法。
```

6000–8000 是这个示例的约定，不是 Full 的通用下限。已有具体题目和材料时直接使用，只澄清会影响研究的关键缺项。Agent 无法读取 GitHub 时，提供[下载后的仓库](https://github.com/rrrrrredy/research-toolkit/archive/refs/heads/main.zip)中的 `SKILL.md` 和所需参考文件。

## 2. 在现有 Agent 中使用

| 使用方式 | 最短路径 |
| --- | --- |
| Codex：直接使用方法 | 打开或提供仓库文件，发送上面的请求。使用 Agent 已有的检索、文件和上下文能力完成研究；无需先安装 MCP。 |
| Cursor：接入本地 MCP | 按[虚拟环境安装步骤](usage-modes.zh-CN.md#单独接入-mcp)安装，将 [README 配置](../README.zh-CN.md#作为-mcp-服务使用)合入 `.cursor/mcp.json`，确认九个 `research_*` 工具可见，再发送请求。 |

其他 Agent 也可通过文件、链接或文本读取同一方法，见[接入说明](../agents/README.zh-CN.md)。客户端配置依据：[Codex MCP](https://developers.openai.com/codex/mcp) · [Cursor MCP](https://cursor.com/docs/mcp)。

评审方式在任务开始时按现有能力选择：

- **宿主内新上下文：**提供研究任务、完整报告和必要来源，让 Astra 或已有评审者单独形成意见；把意见交回作者修订。无需另找外部人员或另一家模型。
- **CLI/MCP 自动评审：**配置已有的 `codex`、`claude` 或兼容端点后端；由 `research_review` 保存输入、回复和版本绑定，见[后端配置](usage-modes.zh-CN.md#reviewer-backends)。
- **self：**没有后端的新 Full 任务默认使用明确标记的自评。若任务已经要求独立评审，就完成该评审。

宿主会话的评审可用于直接使用方法的流程；它不会自动写成 CLI/MCP 的评审记录。选择本地工具管理交付时，通过配置后端完成对应记录。

## 3. 交付完整成果

交付完整报告、来源与判断记录，以及评审意见和修改结果。报告应包含有证据的比较、具体结论和适用条件，引用在导出文档中也能定位。过程记录与读者正文分开。

采用本地工具时，使用 `research_check_draft` 在送审前检查实际篇幅，修好稿件后完成当前版本评审，再调用 `research_finish`。这沿用 Full 的现有流程。

<details>
<summary>可选：用 CLI 建立本地任务和篇幅记录</summary>

从仓库根目录运行，CLI 只需要 Python 3.10+ 标准库，不必安装 MCP 依赖。Linux/macOS 使用 `python3`；Windows 可用 `py -3` 或已有解释器路径。

```bash
python3 scripts/research_workflow.py start --profile full --workspace ../research-work --request examples/full/start.zh.json
```

它建立 `../research-work/knowledge-assistant-full-zh`。Agent 负责实际检索、读写和分节起草；命令负责创建任务。修改了示例研究问题时，也修改请求文件中的 `brief`；已有任务通过 `status` 恢复。

Agent 通过 `research_save`／CLI `save` 的 `requirements` 参数保存实际约定的篇幅，不让用户编辑 JSONL。先记 `pending`，实际核对后提交带依据的 `satisfied` 更新；见[记录保存示例](usage-modes.zh-CN.md#保存研究记录与稿件)。

自评材料的保存与复用见 [CLI 示例](usage-modes.zh-CN.md#复用任务文件并保存自评材料)，其他档位和交付见[现有调用说明](usage-modes.zh-CN.md)。示例不会预填报告或伪造评审。

</details>

研究边界明确、作者自检足以满足用途时，可选 [Lite 体验](quickstart-lite.zh-CN.md)。
