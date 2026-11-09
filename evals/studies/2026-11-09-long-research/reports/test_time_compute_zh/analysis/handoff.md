# 中文独立作者交接

作者阶段已完成，完整内容独立审阅、领域专审、审计和最终验收尚未完成。不要把本交接、作者状态文件或计算退出成功当作研究最终验收。

## 当前主稿与原始成果

- 当前主稿：`draft-current.md`。
- 首份完整稿：`draft-first.md`，与当前稿相同，SHA256 `2e47ab19a31e5c44314dfaeada7bdab6bb7247e083503d86f02ad897c236882b`。
- UTF-8 52,305 bytes；中文字符 12,716（包含标题、表格与文献，不含拉丁字母计为中文字）。
- `outline.md` 保留起始提纲；协调者安排的两个实际独立身份分别完成提纲 requirements 与 structure_and_depth，作者已读取本任务 `native-outline-reviews` 两份原始 response，均 pass 且 findings 为空。这只核查提纲。
- `units/01-mechanisms.md` 至 `05-decisions-and-boundaries.md` 是逐部分形成的完整原稿，正文按这些单元组装。
- `raw-responses/complete-author-response.md` 保留首份完整作者正文；该目录同时保留首份完整组装时的五份单元文本及 `provenance.json`。这是当前原生 Codex 工具写作输出，不是伪造的 Astra API response；原生会话保留实际工具操作历史。

## 输入与实际阅读

本作者仅读取 `frozen-alternate-inputs/test_time_compute_zh/{task.json,sources.json,sources/}`、指定 Toolkit 中文技能和方法，以及本任务中文提纲评审。没有访问英文对应稿、英文作者论断、计算结果或审阅结果，没有阅读其他 research 任务目录，没有联网补事实，没有调用 API。

20 份原件均实际阅读了相关段落。`reading-ledger.json` 每次记录原件绝对路径、文件 SHA256、显示过的行范围；`data/source_registry.csv`汇总实际范围。所有原件哈希与 frozen manifest 一致。不声称全文阅读；初期输出截断处已经剔除或重新读取，TTC012 的第一次读取内排除134–145行，后续单独读取补全这些行。

37 条主张在 `claims.jsonl`，字段为 claim_id、claim、source_ids、report_section、uncertainty；另保留 `data/claims_registry.csv`。算例推导依据与假设数值分开登记；没有把假设数值标成文献实测。

## 实际计算

运行命令：

```powershell
& 'C:/Users/luosong03/Documents/ChatGPT/Others/.research-toolkit-venv/Scripts/python.exe' -B -X utf8 'C:/Users/luosong03/Documents/ChatGPT/Others/work/astra-api-current-chat-20261109/work/implementation/research/test_time_compute_zh/codex-production/budget_example.py'
```

代码 `budget_example.py`，原始 stdout 为 `budget_stdout.txt`，完整数值为 `budget_output.json`。采用 TTC008 的均匀选择通过者公式；所有价格、p、TPR/FPR、时延和并发参数为明确假设。四方案均把全部候选、验证器和工具一次重试期望费用计入。计算不涉及模型实验、真实价格查询或论文复现。

结果：弱验17候选正确提交0.758698，强验11候选0.925341，强生成7候选0.918099，两轮修订10候选0.861017；成本0.09928、0.09284、0.09968、0.09680美元；假设波次耗时81.6、61.4、37.2、104.2秒。正文解释了错误提交、弃答、错交负效用、误判相关性、未计的零项假设与平均服务时间不是尾延迟保证。

## 审阅时值得保留的事实边界

1. TTC001 的2048样本难度估计未计入主比较；4倍生成预算不是4倍全成本。修订/验证能力经过专门训练。
2. TTC002 的REBASE图不计奖励模型计算；新增1000 SFT样本不是全部训练成本；长度拒绝采样的丢弃成本不能忽略。
3. TTC003/v2的参考答案评价器仅是诊断；共享候选池结果与端到端成本不同。v2表1所有响应1,948,821与附录G公开重复采样attempts1,403,520口径不同。
4. TTC006表2的累计翻转定义与计数变化不一致，附录E 7K的p值正文0.038、表格0.014。正文不采用其精确阈值，只作降权辅助反证。
5. TTC005是测试时参数适应，合成题仍靠执行反馈；28题经过基础模型能力筛选；filtered mean@8有通过集合分母和空集合历史承接规则。
6. SUP-TREE表2 VWA基线18.9%、正文18.6%不一致；本文采用表2。Llama实验使用GPT-4o评价器，不能当纯同模型推理扩展。
7. SUP-TAU终态奖励可能漏过程违规；模拟用户实验不足以证明真实长期业务任务的同等收益。

## 后续职责

协调者据实际作者成果安排完整中文内容视角与领域专审、计算核查、独立审计和单独验收，并把必要修订落实到正文。当前 `state/progress.json` 明确 delivery_complete=false。作者保存了 task_spec、来源/主张记录，但未伪造 `final_delivery.json` 或最终评审回执；最终任务规范要求的完整交付状态由协调者在实际通过后管理。

没有写产品代码、改变Toolkit版本或运行Toolkit测试。研究仅进入作者完成、待独立内容审阅状态。

## 补齐原始附件后的有界核对

协调者在首稿后补齐同一20份来源的既有PDF/HTML，未新增事实来源。20个附件哈希均匹配更新的sources.json；这不构成20个附件均全文已读的声明。作者实际额外阅读了4个原始附件：TTC006 PDF完整第4、9、10页视觉核对表2及附录E，SUP-AC PDF完整第6页视觉核对表1，TTC008 HTML单生成器公式原始段落，TTC012 HTML图3原始表格。实际页码或字符区间、原件绝对路径和哈希已追加到reading-ledger.json，attachment-check.json保留结果。

TTC006的累计翻转定义和两处p值差异在PDF页面中仍然存在，SUP-AC主表和TTC008/TTC012公式数字与此前文本一致。首稿、现稿和计算结果均未改变，也没有重跑计算。渲染图保留在tmp/pdfs供本轮独立审阅使用。
