实际研究场景

# 有了新材料，已有报告究竟要改哪里？

编程智能体采购研究案例 · 2026 年 10 月 14–15 日接续更新 · 完整报告为中文。

一篇已有报告讨论“编程智能体排行榜能支持什么采购判断”。本次使用 Research Toolkit 接续这项研究：核对相关来源、定位受影响的主张，保留原始证据并修改完整报告。核心建议仍然是：用排行榜筛选候选，再在采购方自己的工作中试用。

[此前完整报告](https://github.com/rrrrrredy/research-toolkit/blob/main/evals/studies/2026-10-14-native-agent/reports/toolkit/final.md) · [10 月 14 日更新稿](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/report.zh-CN.md) · [10 月 15 日接续稿](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/status-save-2026-10-15/report.zh-CN.md)

## 来源核对如何变成具体修订

下表是修订摘要，不是新增的基准测试结果。[阅读记录](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/source-checks.md)保留来源编号和位置；完整报告链接到公开原始来源。

| 旧稿情况 | 核对材料 | 正文中的修订 |
| --- | --- | --- |
| 讨论了评测题缺陷，但没有展开这一错误判定机制。 | S2：OpenAI 编程评测审查中的 OpenLibrary-77c16d5。 | 补入题面要求一个前导空格、测试要求两个的例子：遵循题面仍可能被判错。 |
| 没有写明 SWE-Lancer 有效运行的前提。 | S6：官方运行说明。 | 补入禁网要求和 Linux iptables 条件；联网 Mac 试跑不能作为等价成绩。 |
| 未区分 Pro V2 中不同修复计数的对象。 | S9/S10：V2 公告与仓库说明。 | 区分 69 道矛盾指令题、529 份题面重写、214 份测试补丁和 38 份参考补丁，不能互相替代。 |
| 只看最终控制结果，会遗漏首轮基础设施故障。 | 新增 S11：V2 发布控制记录。 | 区分最终 642/642 通过与两组控制首轮各 3 次基础设施故障、重跑后成功。 |

## 一次真实修订也带来了遗漏

本次首稿改写 V2 段落时，漏掉了旧稿已有的“跨版本分数不能直接解释为模型进步”。作者上下文的 self 自查发现问题，后续修订恢复这层解释，并将引用移到 529/214/38 的数字旁。[本次首稿](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/first-update.zh-CN.md)、[needs_revision 首评](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/first-self-review.json)和[最终通过记录](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/final-self-review.json)均保留。

## 下一轮：先定位、再阅读、再判断

10 月 15 日，保存两条更新后的来源记录，得到五条关联主张和正文位置提示。实际阅读后只修改三条主张：SWE-Lancer Manager 必须使用 monolith 镜像；Pro V2 超时后仍捕获部分补丁评分；采购核算建议分列共享准备与逐题成本。这些细节此前已经存在于来源中，不是上游刚发布了变动。

[上轮稿件](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/status-save-2026-10-15/previous-report.zh-CN.md) · [来源核对](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/status-save-2026-10-15/source-checks.md) · [实际 save 返回](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/status-save-2026-10-15/calls/03-source-update.response.json) · [记录差异](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/status-save-2026-10-15/updated-records.json) · [Astra 单独上下文复核与修复](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/status-save-2026-10-15/review/README.zh-CN.md)

## 案例支持什么，限制是什么

- 第一轮保留原任务 50 个文件，下一轮保留其 67 个文件；来源与主张编号继续复用。见[首次执行记录](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/execution-summary.json)和[接续执行记录](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/status-save-2026-10-15/execution-summary.json)。

- 两轮接续均使用当前作者上下文的 Full/self；后来进行的 Astra 单独上下文复核另行归档，不冒充 CLI 独立后端回执。

- 没有重新执行编程基准或完整模型评测，也没有“更新对完全重写”的配对实验。因此不能量化总时间节省，或据此声称普遍提质、省钱。

- 实际时间、返回字节数、重复读取和未知用量保留在[原始案例记录](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/README.zh-CN.md)与[后续记录](https://rrrrrredy.github.io/research-toolkit/case-study/coding-benchmark-update/status-save-2026-10-15/README.zh-CN.md)中。一次返回体缩小不等于整体 token、时间或费用降幅；公开的是证据子集，并非完整可迁移的任务快照。

## 用于你自己的报告

把已有报告、相关来源和报告要支持的决策交给 Agent。请它定位受影响段落、复用仍可靠的证据、修改完整报告，并给出简短变更说明。按任务选择 Lite 或 Full，说明实际完成了哪一种评审。

[接续已有研究指南](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/usage-modes.zh-CN.md#接续已有研究) · [复制研究请求](https://rrrrrredy.github.io/research-toolkit/index.zh-CN.html#start) · [更多案例](https://rrrrrredy.github.io/research-toolkit/case-study/index.zh-CN.html)
