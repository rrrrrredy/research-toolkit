# 评测

[English](README.md) | [简体中文](README.zh-CN.md)

现有及以后的用户题、开发题、参考测试和案例均为真实独立任务；实际执行的测试都是真实测试。任务按研究问题区分，同题重复运行仍按重复运行记录。来源材料保留原有出处与性质，包括用户提供或构造的数据。Astra 在单独上下文中即可承担独立评审，无需外部人员、另一家模型或额外外部材料。分工、评审输入或验收标准变化时，应针对受影响部分复验。

研究工具箱与研究评测集用途不同：工具箱帮助完成研究，评测集用任务、材料和判据发现成果问题。本目录也保留工具箱的软件检查样例；它们的机械通过不能作为研究质量分数。

| 要找的内容 | 入口 |
|---|---|
| 完整原生 Agent 与 Toolkit 对照 | [10 月 14 日真实长任务](studies/2026-10-14-native-agent/README.zh-CN.md)：首稿、终稿盲评均平局；Full 耗时更长，实际发现的 Windows 编码错误已修复 |
| 10 月 12 日基线与 v1.0.0 的完整研究结果 | [十题前后比较及针对性修复](studies/2026-10-13-before-after/README.zh-CN.md)：未观察到稳定总体提升；首轮均分 100 → 99.5，20 篇报告、20 次盲评，两篇修订稿另行通过 |
| 报告缺陷示例与对照片段 | [语义诊断案例](semantic_diagnostics/README.zh-CN.md) |
| 研究质量判据与结果解释 | [五维评测标准](../docs/report-evaluation-standard.zh-CN.md)、[已有结果及公开范围](../docs/evaluation-status.zh-CN.md) |
| Toolkit 软件行为检查 | 下文的案例、正反例夹具和运行命令 |

Toolkit 的默认流程调整不改写既有样本、首评或标签，也不自动启动新的模型评测。

## 案例与评测集清单

[完整集合与方法覆盖](../docs/correction-audit-2026-10-13.zh-CN.md)

Toolkit 专用题集在 [`cases/`](cases/)，与后来四模型测试所用的题集分开。下表覆盖当前题目、对照、示例和带日期的运行结果；复用材料会跨分类出现，不能把所有数量相加当作新增独立任务。

| 材料 | 数量 | 用途与当前状态 |
|---|---|---|
| [Toolkit 研究题集](cases/) | 7 题 | [原七篇报告复验](diagnostics/2026-10-13-dedicated-seven/README.zh-CN.md)：保留15次调用，六份给定来源报告验收；管线题现已另有[具名完整报告及Astra逐项通过R01–R13的评审](repairs/2026-10-13-pipeline-complete/README.zh-CN.md)。 |
| [反例夹具](regression_fixtures/manifest.json)／[正例夹具](conformance_fixtures/manifest.json) | 22／4 | 检查预期失败和有效对照的真实软件测试，不另计 26 个研究问题。 |
| [语义诊断](semantic_diagnostics/README.zh-CN.md) | 23 组成对示例 | 当前目录加载已记录的修正，原始输入与判断继续保留。 |
| [四模型测试题](tasksets/development-v2-synthetic/README.zh-CN.md) | 5 个题族 | [10 月 12 日运行](studies/2026-10-12-lite-four-models/README.zh-CN.md)：72 次请求、16 个有效配对，保留四个缺失配对及六个互换偏好变化。 |
| [评审校准 v3](tasksets/judge-calibration-v3/README.zh-CN.md) | 4 个题族、12 份输入 | [12 次真实 Astra 判断](diagnostics/2026-10-12-astra-calibration/README.zh-CN.md)；已经包含 v2 的算术输入。 |
| [原题／新题修复验收](diagnostics/2026-10-13-targeted-recheck/README.zh-CN.md) | 4 题：2 道原题、2 道新题 | 31 次请求，最终 16 个版本验收通过，其中十份经过维护者修正；保留原件。 |
| [参考写作样例](taste_anchors/README.zh-CN.md) | 4 组 | 可复用来解释具体判据，按实记录先前用途、虚构事实或来源缺少日期的情况。 |
| [来源包](source_packs/) | 3 包 | 题目提供的证据；保留来源事实及出处信息。 |
| [公开研究案例](../docs/case-study/README.zh-CN.md) | 2 个 | 国内办公 Agent 中文研究与 API／浏览器英文原创研究，保留稿件、评审与修订；译文不另计任务。 |
| [模板](templates/)及 [Lite 示例](../examples/lite/) | 工作流辅助材料 | 用于复用配置和入门。 |

七道专用题如下：

| 原始题目文件 | 研究问题 |
|---|---|
| [ai_agent_market_landscape_zh.json](cases/ai_agent_market_landscape_zh.json) | AI Agent 市场格局 |
| [ai_video_generation_investment_memo_zh.json](cases/ai_video_generation_investment_memo_zh.json) | AI 视频生成投资备忘录 |
| [reasoning_model_competition_zh.json](cases/reasoning_model_competition_zh.json) | 推理模型竞争 |
| [model_price_war_competitive_analysis_zh.json](cases/model_price_war_competitive_analysis_zh.json) | 模型价格战竞争分析 |
| [monthly_observation_synthesis_zh.json](cases/monthly_observation_synthesis_zh.json) | AI 月度观察综合 |
| [source_instruction_boundary_zh.json](cases/source_instruction_boundary_zh.json) | 含来源指令干扰的研究任务 |
| [model_company_pipeline_long_horizon_zh.json](cases/model_company_pipeline_long_horizon_zh.json) | 八家公司模型管线，包含 13 轮要求 |

这七道原题为中文；英文索引是导读，不另计七道翻译题。`scripts/run_evals.py` 现会把当前分工写入每份新提示：程序测量篇幅，Astra 在分开的上下文中收到完整题目、报告、来源及必要出处并评审内容，作者直接修正确认的缺陷，另存版本复查。作者和评审可使用同一模型，不要求外部评审者、外部供题或固定面板。一份针对当前报告的完整评审即可；长周期题不再设至少三条评审记录的门槛。评审缺失或未通过，仍不能通过适用的完成检查。

PR #38 当时离线检查了全部七题的提示生成及一份完整评审足够的规则；后续[七篇报告实际复验](diagnostics/2026-10-13-dedicated-seven/README.zh-CN.md)现已保存七份完整生成正文、七次 Astra 首评及一次修改稿复评。六份首稿通过；管线稿从 6,020 压缩到 5,987 字符，作为阶段稿获认可，当时 R04/R05 未闭环；后续[具名完整报告](repairs/2026-10-13-pipeline-complete/README.zh-CN.md)经实际研究、修改及新上下文 Astra 复评，5,244字符终稿逐项通过13项要求，这才是当前任务完成状态。13 轮历史要求作为完整记录一次提供，不宣称执行了实时 13 轮 agent 交互。此前 31 次请求使用的是另外四题。原目录和原结果保留，修复版本另存。

本目录包含 7 个研究案例、22 个反例夹具、4 个正例夹具及报告诊断。案例和检查器不要求特定 agent 运行环境。离线检查覆盖需求、任务文件、来源与主张、评审记录、来源指令边界和成稿表达，不提供模型排名或整体报告质量结论。

结果 schema v2 将 `conformance_status`、`conformance_score`、`conformance_flags` 用于机械结构、追溯与配置的失败信号；`research_quality_status` 为 `not_evaluated`。机械通过不代表有洞察、准确或对决策有用。

必交文件缺失时，无论分数多高都不能通过。损坏的需求或对话 JSONL、无效的来源或主张 CSV 会得到明确失败说明；单个案例损坏不会阻止其余案例生成结果。CSV 按逻辑记录计数，来源 ID 与标题必须在同一条记录内对应。

[2026-09-07 原始开发材料](diagnostics/2026-09-07/)包含四份初稿、两份修订、三模型文字诊断及保留的不完整回复；它们是已实际执行的独立任务与测试。日期化原件按原语言和哈希保存，本页提供中文导读。

前瞻的 5–10 个任务族试验见[盲评配对协议](../docs/eval-protocol.zh-CN.md)。脚本冻结并记录种子／顺序，对评审隐藏 A/B 条件，保留首份产出、判断与失败。[2026-10-10 四模型试验](studies/2026-10-10-lite-four-models/README.zh-CN.md)已覆盖同样五个任务族的全部 20 对模型—任务评审，保留全部首轮尝试及失败，格式诊断与重新生成补跑单列；不证明通用效果。仅复查既有公开两组档案时，运行 `python scripts/reproduce_calibration.py`，生成 `evals/runs/calibration-reproduction/inventory.json` 与 `inventory.md`，不调用模型。

新增[协议 v2](../docs/eval-protocol-v2.zh-CN.md)，附[五个独立测试任务](tasksets/development-v2-synthetic/README.zh-CN.md)和[独立评审校准对照](tasksets/judge-calibration-v3/README.zh-CN.md)。[带日期的 Astra 校准](diagnostics/2026-10-12-astra-calibration/README.zh-CN.md)已新增 12 份首轮判断及来源裁定；[四模型开发试验](studies/2026-10-12-lite-four-models/README.zh-CN.md)现已完成，保留四个缺失配对和六个互换偏好变化。这些材料与既有七个流程案例分开。


[10 月 13 日改进复验](diagnostics/2026-10-13-feedback-probes/README.zh-CN.md)保留提示／方法修正后的八次新首轮尝试：全部可解析，仅三篇篇幅达标且仍有语义错误。五篇真实篇幅失败稿与两篇事后编辑对照验证现有交付门槛，不声称质量改善。


[10月13日原题加新题验收](diagnostics/2026-10-13-targeted-recheck/README.zh-CN.md)已完成：四道独立任务、31次新增请求，Astra首轮通过6份，维护者修正10份。最终16个版本篇幅合格并有对应Astra通过评审，其中10份含维护者编辑；原始稿件和失败保留。

## 如何贡献案例

1. [提交失败案例](https://github.com/rrrrrredy/research-toolkit/issues/new?template=failure-case.yml)，填写研究问题、期望结果、来源、具体问题以及 profile／评审档位；报告片段可直接粘贴。
2. 维护者对照原始材料复现并评审问题，区分工具缺陷、执行偏差与证据不足；需要补充时在 issue 中说明。
3. 确认后将最小案例加入对应的回归夹具或语义诊断目录，链接原 issue，保留原始失败与适用范围。

入库标准：问题可复现，并有可合法公开的原始材料；无需贡献者编写代码或自行制作夹具。

## 使用哪个标准

新报告评测采用[现行五维标准](../docs/report-evaluation-standard.zh-CN.md)，区分首次交稿评分、读者交付和产品效果研究。补齐原定缺失评审，保留有效评审、原始缺陷和失败；评测完成不要求先修好样稿。[历史量表](rubrics/README.zh-CN.md)只用于理解旧研究，不能与当前 0—4 分混合。

其他入口：

- [结果 schema v2 迁移](../docs/evaluator-v2-migration.zh-CN.md)。
- [交付检查接口](../docs/delivery-verification.zh-CN.md)与[评审完成接口](../docs/review-completion.zh-CN.md)。
- [来源数据核定](../docs/evaluation-data-audit.zh-CN.md)。
- [23 组成对语义诊断](semantic_diagnostics/README.zh-CN.md)。
- [两评审者原始结果](semantic_diagnostics/reviews/2026-09-08/)：保留共同漏检、严重性分歧、顺序与上下文敏感，以及两项案例修订的单独评审。与作者标签一致不等于准确。

9 月 10 日新增的三组读者样本经过内部四模型诊断，保留了收费口径更正。相关历史评审与材料的当前公开入口见[数据管理仓库](https://github.com/rrrrrredy/agent-trajectory-data/blob/main/docs/PUBLIC-EVALUATIONS.zh-CN.md)；早期八次调用没有评过这三组。当前目录应通过加载器读取；旧输入冻结保存。

已完成的历史首评数量与解释见[评测现状及版本边界](../docs/evaluation-status.zh-CN.md)。下列公开文件是保留评测材料的一部分。

## 目录

```text
evals/
  cases/                       # 案例任务 JSON
  conversation_packs/          # 多轮需求序列
  diagnostics/                # 日期化实际输出和非评分诊断
  conformance_fixtures/        # 应通过的正例
  regression_fixtures/         # 必须检出的反例
  rubrics/                    # 历史量表
  semantic_diagnostics/       # 合成语义诊断
  source_policy.json          # 来源用途与明确排除项
  source_packs/
    ai_knowledge_sanitized/    # 历史知识摘要种子
    prompt_injection_synthetic/
    model_company_pipeline_synthetic/
  runs/                       # 本地输出，Git 忽略
```

## 重建来源种子

已有案例可以直接使用。只有需要重新生成时，才提供本地 `aiknowledge-cli` 与 `ai-knowledge-graph`，并写入独立目录，保留旧研究输入：

```bash
python scripts/build_sanitized_eval_set.py --aiknowledge-cli /path/to/aiknowledge-cli --knowledge-graph /path/to/ai-knowledge-graph --out /path/to/new-eval-seed
python scripts/check_eval_source_integrity.py --evals-dir /path/to/new-eval-seed
```

生成器按配置替换内部网址、文档编号、邮箱、手机号与知识系统标签；这不是完整隐私或再发布权利审查。摘要称内容不可用但仍断言事实的记录会隔离。生成材料只用于工作流评测，不能作为公共事实依据。

`source_policy.json` 保存明确排除的原文与理由，检查器阻止这些主张再次出现。现有材料的 `--purpose factual` 必须失败。缺失日期、无法追溯的原件和未核实复用权利持续披露，不能用生成时间替代来源日期。

## 运行案例

新输入版本使用新目录；创建骨架会重写 `prompt.md`：

```bash
python scripts/run_evals.py --create-skeletons --allow-missing-output --runs-dir evals/runs
```

将各案例的 `prompt.md` 交给被测 agent，保存实际输出：

```text
state/task_spec.md
state/progress.json
state/requirements.jsonl
data/source_registry.csv
data/claims_registry.csv
logs/review.jsonl
final.md
conversation/assistant_messages.jsonl
delivery_message.md
state/final_delivery.json
```

要求台账、对话记录与最终回执按案例需求创建。随后执行：

```bash
python scripts/run_evals.py --runs-dir evals/runs --report evals/runs/report.md --json-report evals/runs/report.json
```

`report.json` 为 schema 2。`pass` 仅表示机械符合；`review` 和 `fail` 默认非零退出，探索性收集才用 `--allow-review`。换目录时同时设置两个报告路径。语义评审、分歧和证据限制单独记录。公开历史材料的实际覆盖范围见集合索引。

## 检查交付声明

```bash
python scripts/check_delivery.py <task-directory>
```

默认读取拟交付说明 `delivery_message.md`；`--actual-message <reply-file>` 可额外比较独立捕获的回复，检查器不会读取聊天应用。明确标注的非最终阶段成果可不带终局回执。

默认契约 3 检查实际任务的完成条件。普通报告保留有效内容评审、版本绑定及必需输入；已声明审计计划与历史样例继续检查审计、裁决及抽查。此处机械检查样例用于软件行为验证，不是研究质量评分；详见[交付接口](../docs/delivery-verification.zh-CN.md)。

记录一致性不能认证用户授权、实际阅读、模型执行或内容质量。

## 回归夹具与持续检查

```bash
python scripts/check_regression_fixtures.py
python scripts/check_conformance_fixtures.py
```

反例检查过程泄漏、深度不足、证据漂移、来源指令泄漏、状态与交付不一致、过期或局部回执、丢失补充要求、隐藏限制、禁止附录、非规范状态、流程膨胀、关键词堆砌、无效评审日志或更晚失败覆盖旧 PASS。反例必须被检出，正例必须保留。

历史夹具明确使用契约 1，保留原比较；它们不证明满足当前契约。当前行为由交付、评审完成和 evaluator 契约检查覆盖。

GitHub Actions 的完整离线检查清单见[贡献指南](../CONTRIBUTING.zh-CN.md#验证)。其中不调用模型。更改后完成 GitHub 推送、对应 CI、适用的 Pages 部署及公开内容核对；脚本通过不等于内容质量或整体验收通过。

## 用发现改进工具箱

1. 保留原始输入、输出、评审、失败与已有运行记录。原定缺失评审按原版本补齐；已授权改进中的缺陷稿件直接修正，修订稿另存并复查，不覆盖首评。
2. 对照任务、正文和证据区分方法缺陷、执行失败、来源限制与无依据建议。
3. 做最小有依据的工具箱修改；作者没执行已有规则，不等于需要再加一条规则。
4. 验证与改动相称。机械行为变更需要反例和正例；文档检查事实、命令和链接。无新变化、失败或疑点，不重复已通过检查。
5. 程序检查篇幅等机械要求，Astra核对内容。确认缺陷后直接修复并检查修改版本，不对未改稿件反复抽样刷分。使用／不使用工具箱的比较按需另行安排。
6. 保留有用例子与有理由的不修改决定，不能把写作偏好固化为通用模板。

## 自动检查的范围

检查器检查必要文件、规范阶段和终局状态、指定章节与实体、来源追溯、面向读者的引用、案例禁用标题、补充要求编号及完成时点、交付声明与未决事项、最新全局评审、当前哈希和回执、限制披露、案例状态大小与控制文件预算，以及配置的风险或反证信号。

还检查正文中的过程表达、内部编号、合成指令标记或禁用结果、评测痕迹、重复模板、句内关键词堆砌、高列表比例、逐条来源转述、明显篇幅不足、空壳主张与评审记录，以及缺少不确定性边界的绝对化表达。这些机械信号不能替代编辑判断。

来源边界夹具核对特定诱饵、禁用结果、供应商数字和限制词，不能证明语义拒绝，更不证明通用注入防护或识别所有工具操作、状态修改、秘密泄漏与同义改写。

## LLM 评审

默认离线 runner 不自动调用 LLM。当前语义评测由 LLM 评审承担，没有人工评审或人工校准前提。模型结论与机械结果分开，已知错误与有效对照用于检查评审表现；一致意见不等于事实真相。

[当前报告与评审计划](../docs/evaluation-roadmap.zh-CN.md)由Astra在与作者分开的上下文评审，作者与评审可使用同一模型。程序精确计数，作者修正确认的问题；双方收到相同完整来源及必要出处，隐藏作者身份、私有笔记和分组映射。不要求外部人员或固定评审面板。历史人数按原记录保留，首稿结果与修订稿验收分别记录。
