# 压缩空气节能研究：v1.4.1 与 v1.4.2 保存说明对照

[English](README.md) | [简体中文](README.zh-CN.md)

**两版首次保存均成功，本例未观察到 v1.4.2 减少填写错误或保存返工的增益。新版耗时 606.187 秒，旧版 540.125 秒，多用 66.062 秒。** 新版另有一次 `research_start.language` 参数纠错，单独记录，不算成保存字段错误。

2026 年 10 月 22 日，一道真实研究题、两次 Lite 运行，每版一次。题目为工厂压缩空气系统节能：什么时候先查漏、调压和优化控制，什么时候值得更换空压机？同一模型、配置和固定材料，未人为加入缺陷；运行中没有追加提示、人工修稿或额外评审。入库没有重跑研究。

## 报告与结果

- [v1.4.2 最终简报：先消除浪费，再按真实需求选机](runs/v1.4.2/tasks/compressed-air-priorities-zh-20261022/final.md)
- [v1.4.1 最终简报：先优化系统，何时再换机](runs/v1.4.1/tasks/compressed-air-priorities-zh-20261022/final.md)
- [原交付对照说明](comparison.zh-CN.md) · [结构化结果](results.json) · [共同需求](inputs/brief.md)

两稿均给出措施比较表、适用条件、相互影响、实施顺序及现场数据清单，解释节气与节电的区别、关键末端压力约束和换机的负荷匹配条件，没有虚构工厂测量、回收期或保证节能率。各版首稿与终稿逐字节一致，没有正文返工。

| 观察项 | v1.4.1 | v1.4.2 |
| --- | ---: | ---: |
| 首次 `research_save` | 成功 | 成功 |
| 首次来源 / 必读要求字段错误 | 0 / 0 | 0 / 0 |
| 保存失败 / 保存纠错调用 | 0 / 0 | 0 / 0 |
| 全部保存调用 | 5 | 5 |
| 进程启动至首次保存成功 | 144.796 秒 | 161.281 秒 |
| 方法读取或查找的 shell 命令 | 5 | 3 |
| 全部 Toolkit MCP 调用 | 10 | 12 |
| 其他工具参数纠错 | 0 | 1 次：`research_start.language` |
| 稿件检查 / 首次作者自检 | 各 1 次 | 各 1 次 |
| 完整运行墙钟 | 540.125 秒 | 606.187 秒 |

首次保存同时提交两条来源和七条要求，其中两条为必读要求。两版均正确填写 `full_text` / `relevant_sections` 与对应 `required_source_ids`。旧版将页码说明写入 `read_evidence`，另用 `evidence_path` 指向文件，属于既有兼容写法；新版按补充说明把路径写入 `read_evidence`，页码和阅读说明写入 `locator`。后续记录检查也未暴露这批字段的错误。可确认新写法被实际采用，不能由此宣称减少了本例的保存返工。

新版将启动语言误填为 `zh-CN`，收到工具要求 `en/zh` 的返回后改为 `zh`。从错误返回到纠正成功为 **10.812 秒**，含 Agent 响应与调用；期间未额外读取方法。这次启动纠错计入总耗时，完整失败及纠正请求见[纠错记录](runs/v1.4.2/records/corrections.json)。总耗时差额不能全部归因于它。

两版均先获取最终 checklist 模板，当时各有五项要求 pending；首次作者自检后保存实际完成依据，再提交 checklist 完成。该收尾顺序不计为保存参数错误，也不是两轮作者自检。两版 `check-draft` 各调用一次，没有重放；未声明硬性全文篇幅范围的警告原样保留，任务本来只约定正文约 1500 字的软目标。

## 条件、方法与计时

两次独立会话依次使用 `gpt-6-astra`、`xhigh`、`service_tier=default`，同一执行提示及固定来源。从各发布提交导出的插件通过本版原生 MCP 服务接受真实调用，非材料回放或模拟返回；默认读取 `toolkit/SKILL.zh-CN.md`，其余方法按需加载。实际配置见两版 `command.json`，版本和输入哈希见 [protocol.json](protocol.json)。

| 版本 | 冻结提交 | 北京时间开始 → 结束 |
| --- | --- | --- |
| v1.4.1 | `f39e091c52d6e5fd1896385e32e3a5d39f96bad7` | 14:54:09.785 → 15:03:09.925 |
| v1.4.2 | `dacce3af5f483f93c3a2991491c9b560eb346f90` | 15:03:09.928 → 15:13:16.125 |

共同材料为 DOE 压缩空气手册第三版的 20 页指定章节，以及 DOE 2000 年 12 月《Minimize Compressed Air Leaks》两页短指南；分别要求阅读相关章节和全文。公开 PDF 在运行前从 ORNL、ENERGY STAR 取得，两版研究期间仅使用相同固定材料。保留 [来源目录](inputs/sources.json)、[在线获取记录](raw/fetch-records.json)、[S1 PDF](inputs/sources/S1.pdf) / [章节文本](inputs/sources/S1.md)、[S2 PDF](inputs/sources/S2.pdf) / [全文文本](inputs/sources/S2.md)。来源准备中的失败地址和替换也保留，没有据运行结果更换材料。

旧版读取入口、Lite 和使用指南，并两次查询字段说明；其中一次包含不存在的文档路径，但也返回源码命中。新版读取入口、Lite，再查找使用指南。这里的 5 / 3 是含读取或查找的完整命令数，不是文件数、token 数或节省时间；一条命令可能包含多个文件。阶段指导另保留于工具响应。少两条查阅命令没有在本例转化为保存错误或返工下降。

墙钟从各进程启动至退出，包含阅读、思考、调用、纠错、写稿、自检和最终回复。首次保存耗时包含此前阅读与准备，不是纯填写时间；事件时刻为接收时间。共同准备 366.785 秒，两次运行合计 1146.312 秒，原交付结果整理 349.729 秒，已计量合计 1862.854 秒。开场及初始查阅未计量；这些数值属于原研究交付，不包含本次入库。详见 [timing.json](timing.json)，未推算费用。

## 留档入口

| 文件 | v1.4.1 | v1.4.2 |
| --- | --- | --- |
| 首次保存请求 / 返回 | [请求](runs/v1.4.1/records/toolkit-calls/02-research_save.request.json) / [返回](runs/v1.4.1/records/toolkit-calls/02-research_save.response.json) | [请求](runs/v1.4.2/records/toolkit-calls/03-research_save.request.json) / [返回](runs/v1.4.2/records/toolkit-calls/03-research_save.response.json) |
| 纠错及正常收尾分类 | [记录](runs/v1.4.1/records/corrections.json) | [记录](runs/v1.4.2/records/corrections.json) |
| 首稿 | [首稿](runs/v1.4.1/tasks/compressed-air-priorities-zh-20261022/first-draft.md) | [首稿](runs/v1.4.2/tasks/compressed-air-priorities-zh-20261022/first-draft.md) |
| 首次作者自检 | [JSON](runs/v1.4.1/tasks/compressed-air-priorities-zh-20261022/first-self-check.json) | [JSON](runs/v1.4.2/tasks/compressed-air-priorities-zh-20261022/first-self-check.json) |
| 自检对应材料 | [所查全文快照](runs/v1.4.1/tasks/compressed-air-priorities-zh-20261022/first-self-check-report.md) | [自检说明与所查稿件哈希](runs/v1.4.2/tasks/compressed-air-priorities-zh-20261022/first-self-check-report.md) |
| 终稿及修订说明 | [终稿](runs/v1.4.1/tasks/compressed-air-priorities-zh-20261022/final.md) / [说明](runs/v1.4.1/tasks/compressed-air-priorities-zh-20261022/revision-notes.md) | [终稿](runs/v1.4.2/tasks/compressed-air-priorities-zh-20261022/final.md) / [说明](runs/v1.4.2/tasks/compressed-air-priorities-zh-20261022/revision-notes.md) |
| 方法读取命令 | [记录](runs/v1.4.1/observed-method-reads.json) | [记录](runs/v1.4.2/observed-method-reads.json) |
| 完整请求 / 返回索引 | [索引](runs/v1.4.1/records/call-index.json) | [索引](runs/v1.4.2/records/call-index.json) |
| 执行事件公开导出 | [事件](runs/v1.4.1/events.jsonl) | [事件](runs/v1.4.2/events.jsonl) |
| 逐事件时间戳 | [时间](runs/v1.4.1/event-times.jsonl) | [时间](runs/v1.4.2/event-times.jsonl) |
| 实际执行耗时及用量 | [execution.json](runs/v1.4.1/execution.json) | [execution.json](runs/v1.4.2/execution.json) |

新版 `first-self-check-report.md` 是自检说明，含所查正文哈希；该正文由未改动的首稿及终稿保留，不将此说明冒称正文副本。

## 入库范围

研究产物、完整 MCP 请求与返回、方法读取命令、事件时间戳、来源与要求台账、共同输入、原对照说明和实际计时均按原字节保留。两份执行事件沿用已有公开导出方式：保留顺序、事件 ID、状态、退出码、消息和用量，规范化宿主路径；shell 命令保留预览和原始哈希，命令输出保留哈希与字符数。完整方法命令及 MCP 请求/返回另存，原始本地事件日志未改动；原对照说明中的事件链接在本目录指向公开导出。

重复原始 PDF、提取中间文件、预览图、本地准备/启动/整理脚本、重复安装包、缓存与锁文件不重复入库。共同输入及各运行输入中的实际 PDF 和文本均保留；省略项、原字节哈希与导出映射见 [archive-manifest.json](archive-manifest.json)。[artifact-hashes.json](artifact-hashes.json)绑定本目录公开文件的准确字节（不包括该哈希清单本身）。历史记录里的本地路径作为执行证据保留，阅读使用相对链接。

本次只入库已有结果并同步入口，不修改产品代码，不新增运行、检查机制或评审，不发版。
