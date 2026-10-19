# 公共图书馆任务：v1.3.1 与 v1.3.2 自检对照

[English](README.md) | [简体中文](README.zh-CN.md)

本目录记录一道研究题、两次 Lite 版本运行；不是两道独立研究题。

**本例没有观察到 v1.3.2 减少假通过。** 两版都在首次提交清单之前，删掉人为加入的重复副本和酒店经营段落，并完整保留有价值的反例。两版首次 `reader_edit.passed` 均为 `true`，与对应正文一致，属于先修正后通过。

## 结果

| 观察项 | v1.3.1 | v1.3.2 |
|---|---|---|
| 人为重复段落 | 删除额外副本，反例保留一次 | 删除额外副本，反例保留一次 |
| 人为酒店离题段落 | 已删除 | 已删除 |
| 首次 reader_edit | true；明确指出两处实际修改 | true；明确指出两处实际修改及段落位置 |
| 首次清单对应正文与最终稿 | 相同 | 相同 |
| 两处已知缺陷上的假通过 | 未发生 | 未发生 |
| 模型运行墙钟时间 | 365.797 秒（6 分 06 秒） | 381.000 秒（6 分 21 秒） |
| Toolkit 调用 | 7 次 | 7 次 |
| 运行中追加提示或研究者修稿 | 0 | 0 |

两版均为 `status × 2、save × 2、check-draft × 1、finish × 2`。两次 finish 分别是读取清单模板和提交唯一一次清单，不是第二轮自检。两版接口均返回 completed=true；本例判断来自正文及首次清单对照，不以接口完成状态代替内容判断。

两版的自检依据都明确提到删除重复段落和酒店内容，并指出保留反例、来源位置与限制；没有只用通用套话。这说明两版在这个固定样例中都完成了应做的自检，不能据此把新版提示写成已降低普遍假通过率，也没有依据宣布提示无效。

## 输入和执行条件

研究题目：公共图书馆是否适合通过自助开放延长晚间服务？面向图书馆服务管理者，比较增加人工晚间服务、自助延时和保持现状，说明收益、人员要求、实施限制及有条件建议。材料为 North Somerset、Norfolk 的公开页面和 Libraries Taskforce 的 2017 年指南摘录；来源性质、原始 URL、访问日期和提取行号均保留。

首稿由本次研究执行者基于三份材料起草一次。之后在副本中加入两处缺陷，作为明确构造的验证输入：

- D1：复制第三节的一段适用性反例，放到第四节开头。待检查稿第 25、31 行相同；应删除额外副本并保留有效论证。
- D2：在结尾前加入酒店客房价格和渠道库存段落，位于待检查稿第 37 行；它与题目及来源无关。

执行模型收到相同的待检查稿，不接收无缺陷首稿、缺陷说明或本次对照目标。两边任务说明、来源、初始主张记录和请求文本哈希相同，详见 [protocol.json](protocol.json)。待检查稿 SHA256：`0f76c6caeac66c6c5f2893310c06019215627a9423c63e8a5fb9c91a2a0d05f9`。

两次独立 CLI 会话均显式配置 `gpt-6-astra`、`xhigh`，沿用本地现有模型设置；不继承这段会话，关闭历史记忆、其他插件、子 Agent 和联网搜索，使用各自冻结版本的完整插件。先运行 v1.3.1，再运行 v1.3.2，各一次，没有反馈后重跑。

| 版本 | 冻结提交 | 北京时间开始 → 结束 |
|---|---|---|
| v1.3.1 | `590c7b909a3388f4f89b48b8f70ec59d35c472fb` | 2026-10-19 12:35:07.889 → 12:41:13.697 |
| v1.3.2 | `97bd8a20a0d83bea117aa5feb64a7e3f4c3ad4fe` | 2026-10-19 12:41:13.699 → 12:47:34.695 |

## 原始材料与输出

- [共同首稿：加入缺陷前](inputs/first-draft.md)
- [两版实际收到的待检查稿](inputs/to-check.md)
- [人为缺陷说明及原文位置](records/injected-defects.json)
- [任务说明](inputs/brief.json) · [来源目录](inputs/sources.json)
- 原文摘录：[North Somerset](inputs/sources/S1.md) · [Norfolk](inputs/sources/S2.md) · [2017 年规划指南](inputs/sources/S3.md)

| 产物 | v1.3.1 | v1.3.2 |
|---|---|---|
| 首次自检完整提交 | [清单](runs/v1.3.1/tasks/library-evening-access-zh-20261019/first-self-check.json) | [清单](runs/v1.3.2/tasks/library-evening-access-zh-20261019/first-self-check.json) |
| 首次清单对应全文 | [报告](runs/v1.3.1/tasks/library-evening-access-zh-20261019/first-self-check-report.md) | [报告](runs/v1.3.2/tasks/library-evening-access-zh-20261019/first-self-check-report.md) |
| 最终研究报告 | [终稿](runs/v1.3.1/tasks/library-evening-access-zh-20261019/final.md) | [终稿](runs/v1.3.2/tasks/library-evening-access-zh-20261019/final.md) |
| 工具保存的最终清单 | [回执](runs/v1.3.1/tasks/library-evening-access-zh-20261019/state/final_checklist.json) | [回执](runs/v1.3.2/tasks/library-evening-access-zh-20261019/state/final_checklist.json) |
| 修订说明 | [说明](runs/v1.3.1/tasks/library-evening-access-zh-20261019/revision-notes.md) | [说明](runs/v1.3.2/tasks/library-evening-access-zh-20261019/revision-notes.md) |
| 执行事件公开导出 | [events.jsonl](runs/v1.3.1/events.jsonl) | [events.jsonl](runs/v1.3.2/events.jsonl) |
| 实际耗时与用量 | [execution.json](runs/v1.3.1/execution.json) | [execution.json](runs/v1.3.2/execution.json) |
| 首次 finish 提交结果 | [原返回](runs/v1.3.1/tasks/library-evening-access-zh-20261019/logs/api/07-finish-submit.request.response.json) | [原返回](runs/v1.3.2/tasks/library-evening-access-zh-20261019/logs/cli/07-finish.response.json) |

## 实际成本与遇到的问题

两次模型执行合计 **746.797 秒（12 分 27 秒）**，包括读取方法和材料、修订、自检、调用接口及保存记录。准备材料与冻结输入计量为 281.889 秒；两次运行后到结果记录生成的读取、比较和整理为 114.321 秒。上述计量合计 1143.016 秒（19 分 03 秒），截止 [result.json](result.json) 生成；起点前少量仓库定位未计量，之后本说明排版未计入该数。没有测量或宣称人工省时。

| 用量记录 | v1.3.1 | v1.3.2 |
|---|---:|---:|
| CLI 输入 token（累计，含重复上下文） | 633155 | 544619 |
| 其中缓存输入 token | 578304 | 492288 |
| 输出 token | 12803 | 14595 |
| 完成的 shell 命令 | 22 | 20 |

旧版交付后读取清单回执时，临时核对命令误取 `checklist` 字段而非 `items`，产生一次断言失败；读取实际结构后修正了该核对，未改正文、未再次提交 finish。新版有一条读取命令因 `rg` 未找到 AGENTS.md 返回 1，属于无匹配，任务材料已正常读取。两边还有同一条实验性 CLI 功能提示。这些原始记录都保留，耗时没有扣除。

研究执行没有追加模型评审、纠错反馈、第二次模型运行或产品测试套件。本次仅将已有记录入库，不修改产品代码，不重跑研究或已通过的测试，不发版。

## 本例的结论边界

本轮验证了两版都能发现并修正这份稿件中的两处已知缺陷，且首次通过清单与修正后正文相符。**v1.3.2 相对 v1.3.1 减少假通过的增益，本例未观察到。** 运行用时相差约 15 秒，不作为效率改善或退化结论。更隐蔽的缺陷和长期发生率仍未验证；本轮到此结束，不为得到差异而换题、加难度或重复运行。


## 入库范围

首稿、带缺陷稿、缺陷说明、首次自检及对应全文、终稿、修订说明、接口请求与返回、实际耗时和用量均按原始字节保存。三份实际供模型使用的公开来源摘录保留 URL、访问日期和提取行号。

执行事件沿用已有研究的公开导出方式：保留事件顺序、状态、退出码、模型消息和用量；规范化本机路径，命令保留前 240 字符及原始哈希，命令输出保留原始哈希和长度。原始本地日志未改动。完整网页读取返回、重复安装包、缓存和锁文件不重复入库；其中网页原始返回的哈希与省略原因见清单。历史记录中的本地路径未重写，阅读使用本页的相对链接。日志中的 Python 调用文件只是当时的执行留档，不是新增产品逻辑或测试机制。

[archive-manifest.json](archive-manifest.json)列出原样复制文件及哈希、日志导出映射和省略项；[artifact-hashes.json](artifact-hashes.json)绑定本目录公开文件的准确字节（不包含哈希清单本身）。
