# 评审完成记录

[English](review-completion.md) | [简体中文](review-completion.zh-CN.md)

[SKILL.md](../SKILL.md) 规定必需行为。本页说明模型评审、有效性核查、发现处置和抽查的离线记录接口。具体审查方法见[角色与工作规范](../references/subagents-and-review-loop.zh-CN.md)。

## 先区分完成的对象

- **评测**：每个必需评审席位取得有效结果，并完成有证据的处置。有效负评、样本的已证缺陷或未解决来源问题可以作为评测结果保留。
- **报告交付**：上述评审工作全部完成，而且报告的必要修改已解决；还须满足全局交付审查、任务要求和交付凭证。

在仓库目录运行，替换任务路径：

~~~bash
python scripts/check_review_completion.py <task-directory> --artifact final.md
~~~

命令检查 `state/progress.json` 中的评审计划和 `logs/review.jsonl` 中的记录。它不调用模型、不重试请求、不修改报告，也不向供应商付费。退出状态只表示记录是否一致，不表示报告质量高低。

交付检查器默认采用 **contract 3**，在正式报告交付时包含本检查。离线评测器即使关闭了可选交付凭证检查，也会在终态记录上检查评审完成情况。核查评测面板是否到齐时使用上述独立命令；报告格式与流程符合性是另一种结果。

## 评审计划

在现有进度记录中增加 `review_plan`：

| 字段 | 含义 |
|---|---|
| `purpose` | `evaluation` 或 `report_delivery`；交付检查器要求后者 |
| `author_id` | 作者上下文标识 |
| `artifact_sha256` | 实际主要成果的哈希 |
| `slots` | 非空的必需独立评审任务列表 |
| `sampling` | 抽查总体、方法、实际选中项和必查项 |

每个席位包含 `slot_id`、`reviewer_id`、`model`、`scope`、`dimensions` 和 `input`。席位编号唯一，评审者不同于作者，维度逐一明确。相近视角可以由同一席位承担，检查器不固定供应商名单。

`input` 是文件引用，例如 `{"path":"reviews/input.json","sha256":"..."}`。省略号须替换为实际哈希，该片段仅说明格式。保留完整原始任务、报告、证据和量表，并记录实际发送封装造成的转换。单个哈希或来源网址列表不证明模型收到完整来源正文。

引用文件必须位于任务目录内，是非空 UTF-8 文本。哈希沿用交付检查器的换行规范：对识别的文本后缀，将 CRLF 和 CR 规范成 LF 后计算；不改写原文件。输入和执行记录不得包含凭据。

在查看结果前声明范围、评审者、输入、抽样方法和重试规则，再按该方法记录实际总体和选中编号。离线检查无法证明计划何时冻结，也无法证明计划涵盖用户的全部要求。

## 原始尝试

每次尝试追加一条 `model_review`，失败单独保留，不能覆盖。

| 字段 | 必需值或内容 |
|---|---|
| `record_type` | `model_review` |
| `attempt_id`、`slot_id` | 唯一尝试编号及声明的必需席位 |
| `status` | `completed`、`failed` 或 `incomplete` |
| `reviewer_id`、`model`、`scope`、`input` | 有效评审须与计划席位一致 |
| `artifact_sha256` | 对应实际受评成果 |
| `execution_id` | 实际可观察的请求、会话或轮次编号，不得编造 |
| `execution` | 保留执行记录的文件引用 |
| `response` | 完整原始模型回复的文件引用，与执行记录分开 |
| `report_verdict` | `pass`、`needs_revision` 或 `not_assessed`，与尝试完成状态分开 |
| `coverage` | 按每个必评维度建立对象，每项有具体 `location` 和 `basis` |
| `findings` | 可定位发现列表；无问题时使用有依据的空列表 |

每条发现包含 `finding_id`、`severity`、`location` 和 `basis`。严重度使用 `critical`、`major`、`minor` 或 `optional`。短引文、原始分数、来源细节和建议保存在原始回复或附加字段中；结构化记录不替代原回复。

调用完成仍不足以填满席位，回复还须通过有效性核查。失败或截断不计完成；失败可能没有回复，但须保留已有执行或错误证据及具体恢复动作。

同一执行编号或同一回复文件不能填充两个席位。相同文本本身也不证明执行重复，仍须核对执行来源与实质评审。检查器仅比对声明的模型标识，不能从调用者自行创建的文件认证供应商身份。

## 有效性与发现处置

`review_audit` 记录对某一回复的实际核查：

- `attempt_id`、`auditor_id`；
- `result`：`valid` 或 `invalid`；
- `response_sha256`：受核查的原始回复；
- `basis`：为什么已实质完成或没有实质完成分配的任务；
- `evidence`：实际核查记录的文件引用；
- `dispositions`：以有效评审的每条发现编号为键，不得缺项或增加无对应发现的项。

原评审者不能认定自身回复有效或无效。任何无效判定还须由作者之外的上下文作出；改动已有有效性结论不能绕过独立裁定。

每项处置需要 `decision`、`reason` 和可定位的 `evidence` 说明。决定为 `confirmed_defect`、`no_change`、`unresolved` 或 `resolved`。报告交付只接受已解决或有依据的不修改；评测可保留缺陷和未决证据结果。

严重或重大发现须由作者与原评审之外的上下文裁定。规范也把决定性争议及关键不采纳决定纳入这一要求，即使记录把严重度写低；脚本不能判断严重度标签是否诚实。

保留所有有效性核查与证据，包括无效判定。检查器采用每次尝试的最新有效性决定，再按追加顺序选择每个席位在**当前正文和输入版本**下的第一份有效完整评审。旧尝试保留原席位编号；推进正式交付的新版本时，计划继续声明这些编号。

同一版本的有效负评不能被后来的好评替代。另获授权的报告修改需要当前版本覆盖，输入保存到新路径，保留旧稿、旧输入和旧评审。不能仅为取得好评而改变计划或输入。发现报告缺陷或存在可逐条裁定的个别误报，均不应成为废弃整份评审的理由。改变有效性决定须有实际证据并留在日志中。

回复套话化、读错材料或遗漏必评维度时，记录无效并完成缺失任务。格式符合要求不代表内容经过认真审查。

## 抽查

`review_plan.sampling` 包含：

- `method`：事先声明的选择与扩大检查方法；
- `population`：候选项的唯一编号列表；
- `selected`：实际选中的唯一编号列表；
- `mandatory`：必须全部出现在选中列表中的决定性项目；确无此类项目时可为空。

选中项必须属于总体。规范要求高风险事项全查，并按任务规模覆盖通过项、不修改决定、章节、来源类型和评审席位。脚本核对声明的集合，不证明总体穷尽或抽样统计合理。

追加 `sampling_audit`：

- `auditor_id`，不同于作者；
- 与计划一致的 `artifact_sha256` 和 `selected`；
- 指向实际抽查记录的 `evidence`；
- `checks`，每个选中项目恰有一项。

每项包含 `result`（`clear` 或 `defect`）及可定位的 `evidence` 说明。缺陷还需：

- `defect_type`：`report` 或 `review_validity`；
- `follow_up.decision`：`resolved`、`no_change`、`confirmed_defect` 或 `unresolved`；
- `follow_up.reason`：实际扩大检查、结果及理由；
- `follow_up.evidence`：已完成后续工作的文件引用。

正式交付只接受已解决或有依据的不修改。评测可保留已证或未决的**报告缺陷**；两类任务的**评审有效性缺陷**都必须解决，或经核查认定无需修改，不能只记录未解决就宣布评审完成。写一句未来行动不能满足条件。

最新抽查记录必须覆盖当前成果和选中列表。评审或抽查文件不能自行认证记录者的身份、独立性或认真程度。

## 理解检查结果

结果包含 `required_slots`、`completed_slots`、`selected_attempts`、标志及解释。席位完成数量不能单独证明任务完成，`ok` 还取决于处置、抽查和其他检查。

即使检查通过，以下字段也保持 `false`：

- `execution_authenticity_verified`；
- `semantic_verification`；
- `report_quality_certified`。

实际执行记录和原始回复须对照可用的运行环境或供应商证据。内容核查必须阅读报告与相关来源。JSON 结构不能证明模型实际运行、理解输入或判断正确。

## 失败恢复与兼容

保留每次失败，定位原因后恢复必需任务。重试批次上限意味着进入恢复或请求具体缺失依赖，不能据此省略必需评审。有效负评不重跑，不静默替换指定模型。

contract 1 和 2 仅用于标明边界的历史记录检查，不检查本页新契约。冻结研究输入、原始回复与历史失败保持原样，后补记录不构成早期执行的证明。

~~~bash
python scripts/check_delivery.py <historical-task-directory> --contract-version 2
python scripts/run_evals.py --delivery-contract-version 2
~~~

新记录类型和全稿交付审查行共同保存在 `logs/review.jsonl`。调用失败不转成未结编辑意见，全局 PASS 不能抹掉缺失席位。交付凭证绑定日志与进度；计划及核查行中的文件引用绑定输入、回复和证据。

合成正反控制命令：

~~~bash
python scripts/check_review_completion_contract.py
~~~

这些明确标注的合成材料检验一致性规则，不是模型调用，也不证明评审质量。
