# 评测

[English](README.md) | [简体中文](README.zh-CN.md)

[11 月 9 日长研究基线，起于 v2.3.4 工作树](studies/2026-11-09-long-research/README.zh-CN.md)：13 个独立问题、15 份已交付报告，保留首稿、独立意见、修订和实际完成结果。具体发现对应正文；本轮是开发基线，不是固定模型的版本对照。

[10 月 27 日研究取舍示范对照](studies/2026-10-27-research-writing-choices/README.zh-CN.md)：两个新构造任务，固定条件下四份首次输出和两次匿名审阅。新增示范后的正文出现了有用的成本推导和机制解释，也出现遗漏；未观察到整篇全面改善或实质返工减少。保留原始正文、审阅输入输出和实际耗时，不设综合分数。

[10 月 22 日压缩空气保存说明对照](studies/2026-10-22-compressed-air-save/README.zh-CN.md)：一道研究题，两次 Lite 运行；v1.4.1 与 v1.4.2 使用相同模型、配置和材料。两版首次保存均成功，本例未观察到 v1.4.2 减少填写错误或保存返工的增益。新版耗时 606.187 秒，旧版 540.125 秒；语言参数纠错单独记录。首次保存请求与返回、纠错调用、方法读取、首稿、首次自检、最终输出及实际耗时均保留。

[10 月 22 日 Codex 研究入口对照](studies/2026-10-22-codex-entry/README.zh-CN.md)：一道研究题，两次 Lite 运行；v1.4.0 与 v1.4.1 使用相同模型、配置和冻结材料。本例未观察到 v1.4.1 在需求理解、指令遵循和研究质量上的增益，新版耗时 603.484 秒，旧版 473.265 秒。已有接口的纠错能力不计作新版收益。首稿、首次自检、最终输出、方法读取与实际耗时均保留。

[10 月 19 日公共图书馆自检对照](studies/2026-10-19-library-self-check/README.zh-CN.md)：一道研究题，两次 Lite 运行；v1.3.1 与 v1.3.2 使用相同模型、材料和待检查稿。两版都在首次通过清单前修正两处明确人为加入的缺陷，均未假通过；本例未观察到 v1.3.2 的增益。首稿、首次自检、终稿和实际成本均保留。

现有及以后的用户题、开发题、参考测试和案例均为真实独立任务；实际执行的测试都是真实测试。任务按研究问题区分，同题重复运行仍按重复运行记录。来源材料保留原有出处与性质，包括用户提供或构造的数据。Astra 在单独上下文中即可承担独立评审，无需外部人员、另一家模型或额外外部材料。分工、评审输入或验收标准变化时，应针对受影响部分复验。模型实际执行和参与评测同样提供用户视角：根据需求遵循、上下文实际使用、实质修正和研究结果判断收益，不以真人参与为前提；说明实际观察到的作用及其任务范围。

研究工具箱与研究评测集用途不同：工具箱帮助完成研究，评测集用任务、材料和判据发现成果问题。本目录也保留工具箱的软件检查样例；它们的机械通过不能作为研究质量分数。

| 要找的内容 | 入口 |
|---|---|
| 完整原生 Agent 与 Toolkit 对照 | [10 月 14 日真实长任务](studies/2026-10-14-native-agent/README.zh-CN.md)：首稿、终稿盲评均平局；Full 耗时更长，实际发现的 Windows 编码错误已修复 |
| 2026-10-14 与 2026-10-15-v1 外部批次 | [12 次 Song 授权运行](studies/2026-10-16-external-batches/README.zh-CN.md)：冻结提交 `45bfc5e38f62f563bb8b800acbdbcb3fd2e27bd3`（v1.0.0，Lite）与 `f31345c5a994a8f1574d946388ee58fe1177ede2`（v1.1.0，Lite×4 与 Full×2）。两道 Full 重复 Day-1 研究问题，故为 12 次运行、10 个问题。合成来源已披露。Full 评审为同会话 degraded 评审。 |
| 2026-10-16-v1 与 2026-10-17-v2 外部批次 | [12 次 Song 授权 Lite 运行](studies/2026-10-19-external-batches/README.zh-CN.md)：冻结提交 `f31345c5a994a8f1574d946388ee58fe1177ede2`（v1.1.0）与 `fedf7cde832139c86cad585883cb5ec2f666427f`（v1.3.0）。该目录 12 段题面彼此不同。两道复测重复 10 月 16 日已入库的研究问题。合成来源已披露。六份外层 Grok 笔记不是 Toolkit 独立评审。 |
| 2026-10-18-v1 与 2026-10-19-v1 外部批次 | [12 次 Song 授权 Lite 运行](studies/2026-10-21-external-batches/README.zh-CN.md)：冻结提交 `fedf7cde832139c86cad585883cb5ec2f666427f`（v1.3.0）与 `e245b90a324933f53fddf0deea039a7715708005`（v1.3.1）。该目录 12 段题面彼此不同。四道复测重复已入库的研究问题。合成来源已披露。十二份外层 Grok 笔记不是 Toolkit 独立评审。  [两篇数值错误及评审漏检另有更正](repairs/2026-10-21-source-polarity/README.zh-CN.md)，原达标记录仅作历史保留。 |
| 10 月 12 日基线与 v1.0.0 的完整研究结果 | [十题前后比较及针对性修复](studies/2026-10-13-before-after/README.zh-CN.md)：未观察到稳定总体提升；首轮均分 100 → 99.5，20 篇报告、20 次盲评，两篇修订稿另行通过 |
| 报告缺陷示例与对照片段 | [语义诊断案例](semantic_diagnostics/README.zh-CN.md) |
| 研究质量判据与结果解释 | [五维评测标准](../docs/report-evaluation-standard.zh-CN.md)、[已有结果及公开范围](../docs/evaluation-status.zh-CN.md) |
| Toolkit 软件行为检查 | 下文的案例、正反例夹具和运行命令 |

Toolkit 的默认流程调整不改写既有样本、首评或标签，也不自动启动新的模型评测。

## 案例与评测集清单

[完整集合与方法覆盖](../docs/correction-audit-2026-10-13.zh-CN.md)

当前长研究题集在 [`cases/`](cases/)，原七题及历史四模型题目另行保留。下表覆盖当前题目、对照、示例和带日期的运行结果；复用材料会跨分类出现，不能把所有数量相加当作新增独立任务。

| 材料 | 数量 | 用途与当前状态 |
|---|---|---|
| [当前长研究题集](cases/) | 13 个独立问题、15 份报告任务 | [v2.4.0 基线 study](studies/2026-11-09-long-research)：15 份完整报告，保留首次意见和实际交付结果。 |
| [已退役原七题](diagnostics/2026-11-09-retired-cases/README.md) | 7 道历史中文题 | 任务文件原样迁移。[原七篇报告复验](diagnostics/2026-10-13-dedicated-seven/README.zh-CN.md)保留15次调用，六份给定来源报告验收；历史管线题另有[具名完整报告及Astra逐项通过R01–R13的评审](repairs/2026-10-13-pipeline-complete/README.zh-CN.md)。这些不是本轮结果。 |
| [外部批次 2026-10-14 与 2026-10-15-v1](studies/2026-10-16-external-batches/README.zh-CN.md) | 12 次运行、10 个问题 | Song 授权的外部任务，冻结于 Toolkit 1.0.0（`45bfc5e38f62f563bb8b800acbdbcb3fd2e27bd3`，Lite）与 1.1.0（`f31345c5a994a8f1574d946388ee58fe1177ede2`，Lite×4 与 Full×2）。合成来源已披露。两道 Full 评审为同会话 degraded 评审。 |
| [外部批次 2026-10-16-v1 与 2026-10-17-v2](studies/2026-10-19-external-batches/README.zh-CN.md) | 12 次 Lite 运行、12 段题面 | Song 授权的外部任务，冻结于 Toolkit 1.1.0（`f31345c5a994a8f1574d946388ee58fe1177ede2`）与 1.3.0（`fedf7cde832139c86cad585883cb5ec2f666427f`）。两道复测重复 10 月 16 日已入库的研究问题。合成来源已披露。六份外层 Grok 笔记不是 Toolkit 独立评审。 |
| [外部批次 2026-10-18-v1 与 2026-10-19-v1](studies/2026-10-21-external-batches/README.zh-CN.md) | 12 次 Lite 运行、12 段题面 | Song 授权的外部任务，冻结于 Toolkit 1.3.0（`fedf7cde832139c86cad585883cb5ec2f666427f`）与 1.3.1（`e245b90a324933f53fddf0deea039a7715708005`）。四道复测重复已入库的研究问题。合成来源已披露。十二份外层 Grok 笔记不是 Toolkit 独立评审。  [两篇数值错误及评审漏检另有更正](repairs/2026-10-21-source-polarity/README.zh-CN.md)，原达标记录仅作历史保留。 |
| [反例夹具](regression_fixtures/manifest.json)／[正例夹具](conformance_fixtures/manifest.json) | 22／4 | 检查预期失败和有效对照的真实软件测试，不另计 26 个研究问题。 |
| [语义诊断](semantic_diagnostics/README.zh-CN.md) | 23 组成对示例 | 当前目录加载已记录的修正，原始输入与判断继续保留。 |
| [四模型冻结题目输入](studies/2026-10-12-lite-four-models/longcat/coordinator/frozen.json) | 5 个历史短题族 | 已从活跃题目目录移除，完整冻结输入仍保留。[10 月 12 日运行](studies/2026-10-12-lite-four-models/README.zh-CN.md)：72 次请求、16 个有效配对，保留四个缺失配对及六个互换偏好变化。 |
| [评审校准 v3](tasksets/judge-calibration-v3/README.zh-CN.md) | 4 个题族、12 份输入 | [12 次真实 Astra 判断](diagnostics/2026-10-12-astra-calibration/README.zh-CN.md)；已经包含 v2 的算术输入。 |
| [原题／新题修复验收](diagnostics/2026-10-13-targeted-recheck/README.zh-CN.md) | 4 题：2 道原题、2 道新题 | 31 次请求，最终 16 个版本验收通过，其中十份经过维护者修正；保留原件。 |
| [参考写作样例](taste_anchors/README.zh-CN.md) | 4 组 | 可复用来解释具体判据，按实记录先前用途、虚构事实或来源缺少日期的情况。 |
| [来源包](source_packs/) | 历史种子包与当前研究材料 | 保留出处及声明用途。公共事实证据须有本地完整原件及匹配哈希；历史工作流种子不是公共事实依据。 |
| [公开研究案例](../docs/case-study/README.zh-CN.md) | 2 个 | 国内办公 Agent 中文研究与 API／浏览器英文原创研究，保留稿件、评审与修订；译文不另计任务。 |
| [模板](templates/) | 工作流辅助材料 | 用于复用配置。[已归档的客服工具比较示例](../examples/lite/)保留旧契约，不作为当前入门方式。 |

13 份主语言报告包括 7 中文、6 英文联网研究。另两份为微短剧英文报告与 TTC 中文报告：各自使用同题已冻结材料独立写作，不读取另一语言答案，不增加独立问题数。修订、审阅和失败重试也不增加独立问题数。

15 份报告每份都须完成七个分别独立于作者的内容视角、适用领域专审、独立审计及完整报告的最终验收。通过可用 Agent 工具或 API 分别启动研究与审阅上下文，可以使用同一模型；保留实际执行身份、首次输出、材料原件及哈希。本次基线先使用 Astra API，收到明确的额度耗尽返回后由 Codex 原生子 Agent 接续，执行记录分别保留。[退役说明](diagnostics/2026-11-09-retired-cases/README.md)提供原七道中文题入口；下文历史结果保持原样。

PR #38 当时离线检查了全部七题的提示生成及一份完整评审足够的规则；后续[七篇报告实际复验](diagnostics/2026-10-13-dedicated-seven/README.zh-CN.md)现已保存七份完整生成正文、七次 Astra 首评及一次修改稿复评。六份首稿通过；管线稿从 6,020 压缩到 5,987 字符，作为阶段稿获认可，当时 R04/R05 未闭环；后续[具名完整报告](repairs/2026-10-13-pipeline-complete/README.zh-CN.md)经实际研究、修改及新上下文 Astra 复评，5,244字符终稿逐项通过13项要求，这是已退役管线题保留的历史完成状态，不是当前题集的完成结果。13 轮历史要求作为完整记录一次提供，不宣称执行了实时 13 轮 agent 交互。此前 31 次请求使用的是另外四题。原目录和原结果保留，修复版本另存。

当前题集定义 13 个独立问题、15 份报告任务；本目录另保留 22 个反例夹具、4 个正例夹具、历史案例及报告诊断。案例和检查器不要求特定 agent 运行环境。离线检查覆盖需求、任务文件、来源与主张、评审记录、来源指令边界和成稿表达，不提供模型排名或整体报告质量结论。

结果 schema v2 将 `conformance_status`、`conformance_score`、`conformance_flags` 用于机械结构、追溯与配置的失败信号；`research_quality_status` 为 `not_evaluated`。机械通过不代表有洞察、准确或对决策有用。

检查器不再因不确定性或主张纪律词汇、实体字符串命中、没有通用过程词而奖励分数。既有 `banned_process_phrases` 和强断言词表只在 `review_warnings` 与 `findings` 中提供上下文核读线索，不据此确定缺陷、扣分或阻断完成。全文其他位置出现谨慎词不能证明某项强断言成立。`entity_hits` 仅记录字符串观察：命中与未命中都不能证明实质覆盖或缺失。

`required_sections` 仅用于原始题面明确要求的字面标题。检查实际正文层级的 ATX 或 Setext Markdown 标题，排除代码与注释，不按全文子串命中；标题存在也不证明回答充分。以各道当前题目的明确格式要求为准；`must_cover_entities` 列表及提示中的主题本身不规定字面标题。实质审阅仍须检查覆盖，主题列表不规定措辞或章节顺序。

0–100 分按剩余机械项目归一化：必交文件 20、来源追溯与引用 15、篇幅 15，仅在配置字面标题要求时加入标题 10。删除或不适用的项目不直接赠分；随后施加原有标志惩罚，保留 80/60 阈值。不同检查器版本的分数不可直接比较，不重算冻结结果。明确格式禁令、来源指令检查、未完成要求、独立审阅和版本绑定继续生效。

必交文件缺失时，无论分数多高都不能通过。损坏的需求或对话 JSONL、无效的来源或主张 CSV 会得到明确失败说明；单个案例损坏不会阻止其余案例生成结果。CSV 按逻辑记录计数；规范来源 ID 与标题须在同一条记录内对应，来源包显式登记的 `task_source_id` 别名还须匹配同一来源网址。正文引用可使用来源标题或公开网址。

[2026-09-07 原始开发材料](diagnostics/2026-09-07/)包含四份初稿、两份修订、三模型文字诊断及保留的不完整回复；它们是已实际执行的独立任务与测试。日期化原件按原语言和哈希保存，本页提供中文导读。

历史[盲评配对协议](../docs/eval-protocol.zh-CN.md)说明固定来源 Lite 试点及保留的执行器，不是当前研究入口。脚本冻结并记录种子／顺序，对评审隐藏 A/B 条件，保留首份产出、判断与失败。[2026-10-10 四模型试验](studies/2026-10-10-lite-four-models/README.zh-CN.md)已覆盖同样五个任务族的全部 20 对模型—任务评审，保留全部首轮尝试及失败，格式诊断与重新生成补跑单列；不证明通用效果。仅复查既有公开两组档案时，运行 `python scripts/reproduce_calibration.py`，生成 `evals/runs/calibration-reproduction/inventory.json` 与 `inventory.md`，不调用模型。 20 对中，2 对为主结果、8 对为格式诊断、10 对为重新生成的完成结果，不能合并解读为条件始终相同的一组对照。

历史[协议 v2](../docs/eval-protocol-v2.zh-CN.md)使用的五个独立短题完整保留在 [frozen.json](studies/2026-10-12-lite-four-models/longcat/coordinator/frozen.json)，另有[独立评审校准对照](tasksets/judge-calibration-v3/README.zh-CN.md)。[带日期的 Astra 校准](diagnostics/2026-10-12-astra-calibration/README.zh-CN.md)已新增 12 份首轮判断及来源裁定；[四模型开发试验](studies/2026-10-12-lite-four-models/README.zh-CN.md)现已完成，保留四个缺失配对和六个互换偏好变化。这些历史材料与已退役七题及当前长研究题集分开。


[10 月 13 日改进复验](diagnostics/2026-10-13-feedback-probes/README.zh-CN.md)保留提示／方法修正后的八次新首轮尝试：全部可解析，仅三篇篇幅达标且仍有语义错误。五篇真实篇幅失败稿与两篇事后编辑对照验证现有交付门槛，不声称质量改善。


[10月13日原题加新题验收](diagnostics/2026-10-13-targeted-recheck/README.zh-CN.md)已完成：四道独立任务、31次新增请求，Astra首轮通过6份，维护者修正10份。最终16个版本篇幅合格并有对应Astra通过评审，其中10份含维护者编辑；原始稿件和失败保留。

## 如何贡献案例

1. [提交失败案例](https://github.com/rrrrrredy/research-toolkit/issues/new?template=failure-case.yml)，填写研究问题、期望结果、来源、具体问题和实际审阅配置；复现旧任务时保留其历史参数。报告片段可直接粘贴。
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
  source_policy.json          # 来源用途、原件与哈希要求及明确排除项
  source_packs/
    ai_knowledge_sanitized/    # 历史知识摘要种子
    prompt_injection_synthetic/
    model_company_pipeline_synthetic/
  runs/                       # 本地输出，Git 忽略
```

## 重建来源种子

本生成器重建历史脱敏工作流种子，不生成当前长研究题目或其事实证据。只有需要重新生成时，才提供本地 `aiknowledge-cli` 与 `ai-knowledge-graph`，并写入独立目录，保留旧研究输入：

```bash
python scripts/build_sanitized_eval_set.py --aiknowledge-cli /path/to/aiknowledge-cli --knowledge-graph /path/to/ai-knowledge-graph --out /path/to/new-eval-seed
python scripts/check_eval_source_integrity.py --evals-dir /path/to/new-eval-seed
```

生成器按配置替换内部网址、文档编号、邮箱、手机号与知识系统标签；这不是完整隐私或再发布权利审查。摘要称内容不可用但仍断言事实的记录会隔离。生成材料只用于工作流评测，不能作为公共事实依据。

`source_policy.json` 保存明确排除的原文与理由，检查器阻止这些主张再次出现。`workflow` 检查仅核对元数据，不证明事实支持。历史工作流种子仍不能通过 `--purpose factual`；当前 `public_sources` 只有具备本地完整原件及匹配哈希，才可用于 factual 检查。网址、节选或摘要不能代替完整原件。缺失日期、无法追溯的出处和未核实复用权利持续披露，不能用生成时间替代来源日期。

## 运行案例

用 `--case` 选择实际 `case_id`，可重复该参数选择多题；省略时加载全部案例，不表示每次维护都必须全跑。`material_mode: research` 要求实际检索核验，`frozen` 保持指定材料范围；两者都不会让 evaluator 代替研究。

提示骨架与 managed 任务分目录。骨架生成会重写 `prompt.md`，并创建空占位文件，不能将其冒充工作流执行：

```bash
python scripts/run_evals.py --case microdrama_market_zh --create-skeletons --allow-missing-output --runs-dir evals/runs/2026-11-09-long-research-prompts --report evals/runs/2026-11-09-long-research-prompts/report.md --json-report evals/runs/2026-11-09-long-research-prompts/report.json
```

将生成的 prompt 作为研究输入。当前要求 managed 产物的案例通过现有 [CLI/MCP 工作流](../docs/usage-modes.md#skill-only-and-cli-fallback)执行：workspace 为 `evals/runs/2026-11-09-long-research/tasks`，task 使用 `case_id`；调用 `start`、`save`、`purpose: report_delivery` 的 `review` 及 `finish`。不要在该 workspace 内生成占位骨架。本批案例将 `reports/current.md` 登记为主稿，并通过既有 `delivery_check.artifact` 配置检查该文件；向 evaluator 导出同一正文为 `final.md`，首稿及修订另存。真实记录由工作流保存，回执仅在完成检查通过后产生。

非空 `artifact_requirements` 只配置文件存在性要求，不关闭其他检查。`delivery_check: false` 只跳过交付检查调用，不跳过 progress、来源、主张、评审检查，也不跳过终局意图触发的当前审阅契约检查。即使 `delivery_check.artifact` 指向其他文件，evaluator 的正文检查仍读取 `final.md`。`source_ids` 为空时，来源标题覆盖项不能评价新检索证据；默认篇幅和记录条数也不证明完整研究已交付。

纯 Skill 可以按同样独立职责完成研究，不需要伪造 CLI 状态或回执。若实际采用该路线，保留真实轨迹，并在研究记录中说明 managed 产物符合性检查不适用于该路线，不能记为通过。当前已要求这些产物的案例优先直接走 managed 路径，无需新增产品机制或放宽题目。

managed 任务按案例要求保存真实记录：

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

要求台账、对话记录与最终回执按案例需求及实际执行保存。真实研究、独立审阅和交付完成后，对所选任务执行机械检查：

```bash
python scripts/run_evals.py --case microdrama_market_zh --runs-dir evals/runs/2026-11-09-long-research/tasks --report evals/studies/2026-11-09-long-research/microdrama_market_zh-conformance.md --json-report evals/studies/2026-11-09-long-research/microdrama_market_zh-conformance.json
```

这两个输出是机械检查结果，不是研究报告或其独立内容审阅。检查其他题目或版本时使用不同结果路径。

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

反例保留原始坏样本及其诊断；机械断言检查内部来源编号泄漏、深度不足、薄弱主张记录、来源指令泄漏、状态与交付不一致、过期或局部回执、丢失补充要求、隐藏限制、禁止附录、非规范状态、流程膨胀、关键词堆砌、无效评审日志或更晚失败覆盖旧 PASS。通用过程词与强断言措辞改为上下文核读提示，不再据词面确定语义缺陷。这不清除原始语义问题，也不把反例改称好报告；已有机械反例仍须检出，正例仍须保留。

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

检查器检查必要文件、规范阶段和终局状态、明确要求的字面 Markdown 标题、来源追溯、面向读者的引用、案例禁用标题、补充要求编号及完成时点、交付声明与未决事项、最新全局评审、当前哈希和回执、限制披露，以及案例状态大小与控制文件预算。实体或主题字符串仅作观察，命中和缺席都不能判定实质覆盖。

内部编号、合成指令标记或明确禁用结果、重复模板、句内关键词堆砌、高列表比例、逐条来源转述、明显篇幅不足及空壳主张与评审记录仍按已有规则检查。通用过程表达、评测措辞及强断言词仅提示核读，不确定缺陷、不扣分，也不单独触发 false_completion_signal；谨慎词和主张纪律词既不加分，也不能抵消另一处断言。机械检查不能替代正文与证据审阅。

来源边界夹具核对特定诱饵、禁用结果、供应商数字和限制词，不能证明语义拒绝，更不证明通用注入防护或识别所有工具操作、状态修改、秘密泄漏与同义改写。

## LLM 评审

默认离线 runner 不自动调用 LLM。当前语义评测由 LLM 评审承担，没有人工评审或人工校准前提。模型结论与机械结果分开，已知错误与有效对照用于检查评审表现；一致意见不等于事实真相。

[当前报告与评审计划](../docs/evaluation-roadmap.zh-CN.md)由Astra在与作者分开的上下文评审，作者与评审可使用同一模型。程序精确计数，作者修正确认的问题；双方收到相同完整来源及必要出处，隐藏作者身份、私有笔记和分组映射。不要求外部人员或固定评审面板。历史人数按原记录保留，首稿结果与修订稿验收分别记录。
