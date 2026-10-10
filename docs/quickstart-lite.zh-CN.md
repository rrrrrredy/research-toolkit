# 约 5 分钟完成第一个 Lite 任务

[English](quickstart-lite.md) · [简体中文](quickstart-lite.zh-CN.md) · [Research Toolkit](../README.zh-CN.md)

用两份随附材料完成一篇短比较。只需一个能读取仓库的 Agent，无需评审账号、API key、插件或 MCP 配置。“5 分钟”是 Agent 已就绪时的入门用时估计，不是模型响应时长保证。

## 把这段请求发给 Agent

```text
本次使用 Research Toolkit：
https://github.com/rrrrrredy/research-toolkit
先读 SKILL.md，选择 profile=lite。

完整需求见 examples/lite/start.zh.json，
两份虚构来源见 examples/lite/sources.zh-CN.md。
为六人客服团队选择要试用的客服工具：每月订阅费不超过35美元，
每周需要CSV导出，可接受手动操作。产出600–900字中文简报。

现有需求足以提出试用建议。先明确简短提纲，阅读两份说明，
登记重要判断，再分节起草。仅使用随附来源，不编造CSV字段、
实测可靠性和迁移费用。引用使用可读来源名，任务记录不混入报告。

跳过 research_review 和 Full 交付硬门槛。
最后逐项完成Lite的六项checklist，每项给出具体依据。
披露材料虚构且未进行独立评审。
如有本地执行工具，使用research_start和research_finish
或同一套CLI；否则在聊天中分别提供简报、来源与判断记录、
checklist，并说明没有生成本地交付凭证。
```

成果是一份包含成本计算和条件的试用建议，不是采购背书。Agent 无法读取 GitHub 时，提供下载后的 `SKILL.md`、相关参考文件、[需求](../examples/lite/start.zh.json)和[来源包](../examples/lite/sources.zh-CN.md)。

## 会得到什么

| 成果 | 应包含什么 |
| --- | --- |
| 简报 | 明确建议、六席位费用比较、相反条件及具体试用检查。 |
| 来源与判断记录 | 重要事实对应随附材料；建议和未知项分别标明。 |
| 最终 checklist | 需求、判断与来源、反证、分节、读者编辑、限制说明，每项给出具体位置或解释。 |

Lite 不发起评审，checklist 是作者检查，不是独立批准。未通过项保持打开，修正后才能标记通过；字段完整不等于研究质量获得认证。

<details>
<summary>在 clone 或 fork 中运行本地流程</summary>

从仓库根目录使用 Python 3.10+；共享 CLI 只需标准库。任务放在仓库之外。阅读与写作由 Agent 完成，这些命令不会自动生成报告。

```bash
python scripts/research_workflow.py start --profile lite --workspace ../research-work --request examples/lite/start.zh.json
```

命令会建立 `../research-work/helpdesk-lite`。Agent 把来源说明复制到任务目录，填写 `data/source_registry.csv` 和 `data/claims_registry.csv`，保存提纲与分节稿，写出 `final.md`。更新阶段用已有的 `status` 动作，参见 [CLI 参数](usage-modes.zh-CN.md)。

先以任务名和交付消息调用 `finish` 获取 checklist，再保存包含 `task`、`message`、`checklist` 的 `finish.json`。六个键分别为 `requirements`、`claims_and_sources`、`counterevidence`、`sections`、`reader_edit`、`limitations`；每项需有 `passed: true` 及说明真实检查与位置的 `evidence` 字符串。

```bash
python scripts/research_workflow.py finish --workspace ../research-work --request ../research-work/helpdesk-lite/finish.json
python scripts/check_delivery.py ../research-work/helpdesk-lite
```

完成后可看到 `final.md`、`state/final_checklist.json`、`status: checklist_complete`、`independent_review: false` 以及明确的 `SKIP` 日志，没有独立评审记录。正文改变后需要重新检查并提交 checklist。

</details>

用于自己的任务时，替换需求与来源。决策重要性、证据规模或审阅要求超出这个小任务时，选择 [Full 及合适的评审档位](../SKILL.zh-CN.md#选择档位)。本虚构练习用于入门，不增加研究评测样本数。
