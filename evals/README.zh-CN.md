# 评测

[English](README.md) | [简体中文](README.zh-CN.md)

本目录包含 7 个研究案例、22 个反例夹具、4 个正例夹具及报告诊断。案例和检查器不要求特定 agent 运行环境。离线检查覆盖需求、任务文件、来源与主张、评审记录、来源指令边界和成稿表达，不提供模型排名或整体报告质量结论。

结果 schema v2 将 `conformance_status`、`conformance_score`、`conformance_flags` 用于机械结构、追溯与配置的失败信号；`research_quality_status` 为 `not_evaluated`。机械通过不代表有洞察、准确或对决策有用。

必交文件缺失时，无论分数多高都不能通过。损坏的需求或对话 JSONL、无效的来源或主张 CSV 会得到明确失败说明；单个案例损坏不会阻止其余案例生成结果。CSV 按逻辑记录计数，来源 ID 与标题必须在同一条记录内对应。

[2026-09-07 原始开发材料](diagnostics/2026-09-07/)包含四份初稿、两份修订、三模型文字诊断及保留的不完整回复；它们是开发诊断，不是留出效果研究。日期化原件按原语言和哈希保存，本页提供中文导读。

## 使用哪个标准

新报告评测采用[现行五维标准](../docs/report-evaluation-standard.zh-CN.md)，区分首次交稿评分、读者交付和产品效果研究。补齐原定缺失评审，保留有效评审、原始缺陷和失败；评测完成不要求先修好样稿。[历史量表](rubrics/README.zh-CN.md)只用于理解旧研究，不能与当前 0—4 分混合。

其他入口：

- [结果 schema v2 迁移](../docs/evaluator-v2-migration.zh-CN.md)。
- [交付检查接口](../docs/delivery-verification.zh-CN.md)与[评审完成接口](../docs/review-completion.zh-CN.md)。
- [来源数据核定](../docs/evaluation-data-audit.zh-CN.md)。
- [23 组成对语义诊断](semantic_diagnostics/README.zh-CN.md)。
- [两评审者原始结果](semantic_diagnostics/reviews/2026-09-08/)：保留共同漏检、严重性分歧、顺序与上下文敏感，以及两项案例修订的单独评审。与作者标签一致不等于准确。

9 月 10 日新增的三组读者样本经过内部四模型诊断，保留了收费口径更正。私人评审未公开，早期八次公开调用没有评过这三组。当前目录应通过加载器读取；旧输入冻结保存。

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

`report.json` 为 schema 2。`pass` 仅表示机械符合；`review` 和 `fail` 默认非零退出，探索性收集才用 `--allow-review`。换目录时同时设置两个报告路径。语义评审、分歧和证据限制单独记录。公共材料并不包含所有私人研究。

## 检查交付声明

```bash
python scripts/check_delivery.py <task-directory>
```

默认读取拟交付说明 `delivery_message.md`；`--actual-message <reply-file>` 可额外比较独立捕获的回复，检查器不会读取聊天应用。明确标注的非最终阶段成果可不带终局回执。

默认契约 3 要求 `final/complete` 状态一致、无开放阻断、当前版本的全局与指定评审通过、回执绑定必需文件，且模型评审、有效性审计、处置、裁决与抽查记录完整。豁免、排除或已接受限制须有具体用户决定；声明的必读范围与来源记录一致。识别到披露矛盾则失败，模糊匹配需审阅。旧契约只用于明确标注的历史记录，详见[接口](../docs/delivery-verification.zh-CN.md)。

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

1. 保留原始输入、输出、评审、失败与已有运行记录。补齐原定缺失评审，不修样稿、不替换有效结果。
2. 对照任务、正文和证据区分方法缺陷、执行失败、来源限制与无依据建议。
3. 做最小有依据的工具箱修改；作者没执行已有规则，不等于需要再加一条规则。
4. 验证与改动相称。机械行为变更需要反例和正例；文档检查事实、命令和链接。无新变化、失败或疑点，不重复已通过检查。
5. 机械符合与语义质量分开。新产品效果研究须先冻结版本、任务选择、调用预算和停止规则。负面结果不触发修稿或追求高分的额外轮次。
6. 保留有用例子与有理由的不修改决定，不能把写作偏好固化为通用模板。

## 自动检查的范围

检查器检查必要文件、规范阶段和终局状态、指定章节与实体、来源追溯、面向读者的引用、案例禁用标题、补充要求编号及完成时点、交付声明与未决事项、最新全局评审、当前哈希和回执、限制披露、案例状态大小与控制文件预算，以及配置的风险或反证信号。

还检查正文中的过程表达、内部编号、合成指令标记或禁用结果、评测痕迹、重复模板、句内关键词堆砌、高列表比例、逐条来源转述、明显篇幅不足、空壳主张与评审记录，以及缺少不确定性边界的绝对化表达。这些机械信号不能替代编辑判断。

来源边界夹具核对特定诱饵、禁用结果、供应商数字和限制词，不能证明语义拒绝，更不证明通用注入防护或识别所有工具操作、状态修改、秘密泄漏与同义改写。

## LLM 评审

默认离线 runner 不自动调用 LLM。当前语义评测由 LLM 评审承担，没有人工评审或人工校准前提。模型结论与机械结果分开，已知错误与有效对照用于检查评审表现；一致意见不等于事实真相。

[当前报告与评审计划](../docs/evaluation-roadmap.zh-CN.md)采用一名作者、四路模型评审，输入版本相同，各意见独立保存后再比较。这是研究配置，不是工具箱依赖。较早冻结与后来补充评审分别保留。缺陷用于改进产品；另行要求的成稿修复或修复方法研究与首次交稿评测分开。日期化开发材料不构成通用产品效果证明。
