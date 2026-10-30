# 历史 checklist 任务兼容

本页解释已保存的 `profile=lite` 记录，不是当前研究入口，也不是仅靠作者检查交付的路径。已完成旧成果与回执保留原意；继续研究时使用[统一方法](../SKILL.zh-CN.md)，复用材料并完成当前独立审阅、审计与验收。

## final — 历史作者自检

旧任务以 `state/final_checklist.json` 保存六项作者检查：

| 键 | 历史作者检查的含义 |
| --- | --- |
| `requirements` | 所要求的问题、补充指令、格式与明确篇幅要求 |
| `claims_and_sources` | 重要主张和引用是否对应实际读过的来源 |
| `counterevidence` | 相关结论中的反证和不确定性 |
| `sections` | 必需解释、覆盖与重复填充问题 |
| `reader_edit` | 读者用途、重复／离题内容与生产叙述 |
| `limitations` | 重要证据限制及未经独立审阅 |

保存的 `passed` 和 `evidence` 说明当时作者记录了什么，不能改称独立审阅、审计或最终验收。失败、笼统或错误的通过声明，以及后续更正，作为分别的历史依据保留。

按当时 schema，回执可能只绑定报告与交付说明，也可能同时绑定任务规格、来源／主张表、要求台账、声明的本地阅读文件及可选 `evidence_files`。按实际回执版本理解，不补造更强的历史绑定。文本哈希使用 LF 归一化；来源记录出现远程网址，不代表已经下载或阅读。

已有 `length_constraint` 保留当时的单位与范围：`whitespace_words` 或 `nonwhitespace_characters`、`whole_artifact`、含端点的 `min` 和／或 `max`。它衡量明确约定的范围，不衡量研究深度。字段说明见[计数参考](../docs/delivery-verification.zh-CN.md#显式篇幅要求)。

不能重新提交旧 checklist 替代当前完成要求。保留原成果，读取有效要求和完整研究材料，按[历史任务兼容](../docs/usage-modes.zh-CN.md#历史任务兼容)继续。
