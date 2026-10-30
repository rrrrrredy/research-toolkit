# 交付检查：契约与观察边界

[English](delivery-verification.md) | [简体中文](delivery-verification.zh-CN.md)

本契约用于 CLI／MCP 管理交付或任务明确要求其回执的情况。纯 Skill 报告完成约定研究与检查即可，不要求创建这些状态文件或回执。

这是可选的离线一致性检查，不是运行时权限钩子，也不能证明 Agent 实际调用过它。研究和写作要求以 [SKILL.md](../SKILL.md) 为准；本页说明接口，不另加写作规则。

默认采用 **delivery contract 3**。交付凭证外层仍为 `schema_version: 1`，契约版本表示执行了哪些检查。结果包含 `delivery_contract_version`、`current_contract_checked` 和 `semantic_verification: false`，均不认证用户授权、实际阅读或编辑质量。

共享 CLI 需要 Python 3.10+，只使用标准库。Linux 上优先使用 `python3`；本机已有的 Python 3.10+ 解释器即可。

~~~bash
python3 <skill-directory>/scripts/check_delivery.py <task-directory>
~~~

凭证绑定当前成果、简报、进度、来源与主张记录、审查日志及拟发送的交付说明；适用的需求和不确定性文件也需绑定。凭证中已记录的每个路径都必须核查文件存在性、任务目录边界和哈希，即使绑定时属于可选文件；从未绑定的可选文件仍可缺省。文本哈希将 CRLF、CR 规范为 LF。相关修改完成后再封存，后续修改会使旧凭证过期；不为重建凭证重做无关研究。

用 `--delivery-message note.md` 指定其他交付说明文件，凭证须绑定选定文件。成果、凭证和拟交付说明的路径均须位于任务目录内。


新研究和继续交付须完成分别独立的内容视角、领域专审、独立审计和最终验收。历史回执按当时完成规则可读，见[兼容性](compatibility.zh-CN.md)。

<a id="完成-full-交付"></a>

## 完成研究交付

对照有效要求和证据核对实际回答，完成当前版本独立内容审阅、审计和最终验收，必要修正落实到正文。有效负评表示该审阅完成，交付仍需等待必要问题解决。

用当前稿件和交付说明调用 `research_finish`，由工具绑定输入及审阅结果，写入 `state/final_delivery.json`；必需工作完成后才进入 `stage: final` 与 `status: complete`。不手写重复回执，也不由作者写一条全局 PASS 替代独立验收。独立检查器用于查看已保留记录，不额外调用内容评审。

## 需求关闭与阅读记录

`state/requirements.jsonl` 中，`satisfied` 需要非空证据字符串或字符串列表。以 `waived`、`out_of_scope` 或 `accepted_limitation` 关闭的要求，需要 `user_decision` 对象，内含非空 `source_turn` 和 `quote`。决定须与该要求相关；用户最初明确排除的事项也可确立边界。状态标签、作者自行决定或披露缺口，不能替代用户的决定。

以下是**合成格式示例**，不是真实授权证据：

~~~json
{"requirement_id":"R-read-1","status":"waived","user_decision":{"source_turn":"user-message-7","quote":"You may skip the inaccessible article."}}
~~~

实际任务要求的阅读可以这样记录：

~~~json
{"requirement_id":"R-read-2","status":"satisfied","evidence":"notes/source-2.md","reading_requirement":"full_text","required_source_ids":["S02"]}
~~~

对应 `data/source_registry.csv` 中的来源行必须恰好出现一次，并有 `read_scope` 及非空 `read_evidence`。实际阅读范围使用 `full_text`、`relevant_sections`、`abstract`、`partial` 或 `not_read`。全文要求只接受全文；相关章节要求接受已完成相关章节或全文阅读。证据引用应定位读过的部分及相应笔记或观察。HTTP 200 和登记网址仅说明可访问，不说明读过；辅助来源不因此被强制全文阅读。

当 `read_evidence` 明确指向本地文件时，文件必须在任务目录内、实际存在且内容非空。缺失文件、目录、空白文件或越界路径都会失败；文件引用可附带锚点、页码或章节说明。网址和章节、页码定位仍可使用，检查器不会抓取或认证其内容。

脚本核对声明字段和上述文件条件，无法发现未记录的需求、从自由文本推导阅读义务、认证引文真实性或从笔记证明理解。作者仍须对照真实请求与来源核查。独立检查器和评测器均检查需求关闭，即使关闭评测器可选的凭证检查也如此。

## 显式篇幅要求

任务可在已有要求台账中，用可选的 `length_constraint` 记录可测范围。起草／送审前记录任务已约定的篇幅及计数口径，不自行设置默认最小篇幅，也不从自然语言猜测阈值。以下是**合成格式示例**，不是通用字数目标：

```json
{"requirement_id":"R-length","summary":"已约定整个文件为 800—1200 个非空白字符。","status":"pending","evidence":"","length_constraint":{"unit":"nonwhitespace_characters","scope":"whole_artifact","min":800,"max":1200}}
```

用户用自然语言说明篇幅；Agent 将该行作为 `requirements` 元素传给 `research_save`／CLI `save`，工具维护 `state/requirements.jsonl` 并保留其他要求。见[记录保存指南](usage-modes.zh-CN.md#保存研究记录与稿件)。示例先记为 `pending`；实际计数并核对约定后，才改为 `satisfied`，填写 `evidence`（如 `final.md，整个文件`）。

| 要填什么 | 正确写法 |
| --- | --- |
| 上下限 | `min` / `max`，至少填一个；不要写 `minimum`、`max_chars`。 |
| 数值 | `6000` 这样的非负整数，不加引号；最小值不超过最大值。 |
| 计数方式 | 中文常用 `nonwhitespace_characters`；空白分隔词用 `whitespace_words`。 |
| 计数范围 | `scope: "whole_artifact"`，整份文件包含标题、Markdown、引用和参考资料。 |

研究示例提供可修改的 [中文篇幅记录](https://github.com/rrrrrredy/research-toolkit/blob/main/examples/full/requirements.zh.jsonl)及[英文篇幅记录](https://github.com/rrrrrredy/research-toolkit/blob/main/examples/full/requirements.en.jsonl)。不要求使用示例数字，填写任务实际约定。

把 `{"task":"你的任务名"}` 保存为 `check-draft.json`，从仓库根目录执行：

```bash
python3 scripts/research_workflow.py check-draft --workspace ../research-work --request check-draft.json
```

Windows 可将 `python3` 替换为 `py -3` 或已有解释器路径；MCP 可直接调用 `research_check_draft(task="你的任务名")`。查看 `counts` 和 `length_checks` 的实际值与范围；字段填错时，`errors` 会指出字段及正确写法。`bounds_met: true` 表示实际文件符合所记录范围；`status: pending` 表示要求记录仍待核对。此时 `next_action` 会指出要求编号与实测值：核对约定范围和计数口径后，仅将对应记录改为 `satisfied`，以文件、计数和范围作为证据。其他错误分别处理，检查保持只读。


`whitespace_words` 按 Python 空白分词；`nonwhitespace_characters` 统计除空白外的 Unicode 码点。两者均计算整个 UTF-8 文件，包含 Markdown 标记、标题、引用及参考文献；不是模型 token 或编辑器渲染后的字数。目前仅支持 `whole_artifact`。若约定只统计正文或按页限制，应使用相应测量，不能改称全文计数。`min`／`max` 至少提供一个非负整数，范围包含端点；使用独立要求编号，并在 summary 中说明实际约定。

`research_finish` 重算实际篇幅，超出范围的 `satisfied` 自述会在写入凭证或替换交付消息之前被拒绝。凭证保存 `length_checks`，离线检查会重新测量；历史结果按当时契约保留，不倒填审阅。接续时复用原稿和来源，完成当前独立工作；旧 checklist 不升级为当前验收。

评测 runner 在终态交付时也检查显式篇幅要求，即使关闭了可选凭证检查。这些检查只验证实际计数与声明的范围，不能发现漏记要求、证明范围忠实于用户指示，也不能认证研究深度或质量。作者自述或增加篇幅都不能补足缺失的论证。

## 比较实际回复记录

~~~bash
python3 <skill-directory>/scripts/check_delivery.py <task-directory> --actual-message captured-reply.md
~~~

新旧任务均将提供的回复记录与已绑定的拟交付说明比较，只规范换行和首尾空白。运行环境可以单独保存最终输出，在运行后调用检查器；保留原始输出并说明如何提取客户端元数据，不能悄悄删掉实质差异。

`delivery_observation` 为 `not_provided`、`matched`、`mismatch` 或 `unreadable`。指定的记录缺失或不一致会失败。`not_provided` 仅表示检查了拟发送文本，不证明用户收到它。

历史 checklist 任务的 `checklist_valid` 表示保留的 checklist 是否仍匹配输入及已记录要求；`terminal_state` 表示任务当前是否为 `final/complete`。通过 `research_status(stage="revise")` 接续后，checklist 保留，但交付检查返回 `ok: false` 和 `incomplete_lite_task`，直到 `research_finish` 完成当前工作。检查不改写任务记录，也不要求未提供的实际回复记录。

调用方提供的文件不是真实交付的认证。Agent 再写一份预期说明不构成独立捕获证据。本接口本身不拦截或强制约束实际最终回复。

## 必需模型评审的完成

交付检查读取[审阅完成记录](review-completion.zh-CN.md)。当前任务标记 `review_contract: 2`，计划绑定分别独立的内容视角、领域专审、独立审计和最终验收；各项保留真实原始回复、执行证据及输入版本。作者自检不能满足这些角色。

全局 PASS 不能补齐缺失任务，执行失败与正文发现分开保留。审阅完成和报告就绪不同：真实负评可以完成审阅，必要修正仍阻止交付。独立审计核对发现和抽查内容，最终验收覆盖修订后的完整报告。检查历史记录不改写当时契约。

## 任务声明的审查范围

任务可在 `progress.required_review_scopes` 声明额外必需范围。其当前结果应完成且无必要未决问题，同时满足当前内容审阅、审计和验收要求。保留真实范围与稿件绑定；局部单元结果不能替代全稿判断。

最新全局及每个必需范围须含 `artifact_sha256`，对应实际受评主要报告的 LF 规范化 SHA-256。缺失或错误格式触发 `missing_review_artifact_binding`；与当前报告不同触发 `stale_review_artifact`。凭证另行绑定当前审查日志。重建凭证不能让旧评审覆盖新正文；局部复核不能刷新全局绑定，全局 PASS 也不能刷新必需专项评审的绑定。

进度状态允许 `in_progress`、`paused`、`blocked`、`complete`。终态同时要求 `stage: final` 和 `status: complete`，只满足一个不够。

两个入口共享审查和未结问题语义。最新无问题的全局审查覆盖较早的普通单元审查；此后出现的阻断问题仍须由同范围的无问题审查或新的全局审查处理。局部 PASS 不能关闭其他范围或失败的全局审查。显式要求的范围始终独立，全局 PASS 不能取消它们。错误日志不能靠追加 PASS 修复，须明确保留并纠正错误记录。只有 `routed_action` 仍是计划，不是解决。

## 限制披露不是关键词认证

`limitation_disclosure.status` 区分 `not_applicable`、`absent`、`contradiction`、`text_covered` 和 `needs_review`。没有披露信号，或检测到全面否认已有的限制，会使机械检查失败；否认检测是有限启发式规则，不能识别所有措辞。

`text_covered` 表示规范化标点和空白后找到了已记录的限制文本，不代表其真实或诚实。仅部分匹配、改写表达或泛泛说明时，`needs_review` 给出 `unmatched_limitations` 和可见提示。正常同义表达不会只因无法精确匹配就失败，但机械 PASS 不能称为披露已核验。`semantic_verification` 始终为 false，含义、覆盖和重大矛盾仍需内容审阅。不要求固定措辞、额外声明文件或某家模型/API。

## 交付前的稿件检查

`research_check_draft`（CLI `check-draft`）测量当前文件并检查草稿记录前提，不修改进度或生成凭证。无需先写交付说明即可取得显式篇幅检查；缺少范围会警告，不算篇幅合格。`ok` 仅代表这些机械检查，语义质量与交付仍为 `not_assessed`。共用任务锁可能为旧任务创建常规空文件；`finish` 始终重新检查当前版本。

现有 `warnings` 也会提示至少出现两次、完全相同的普通正文段落，长段落沿用现有评测的至少 24 个非空白字符口径。每条提示保留段落原文，以及每处出现的章节和起止行号（含首尾行）。匹配区分大小写，不归一化措辞、引用或段内空白；代码块、标题、表格、列表和引用块不参与。提示不会删文，也不改变 `ok` 或交付资格，是否有意重复由研究者判断。减少自检假通过的收益仍未验证。

## 历史记录

`--contract-version 1` 或 `--contract-version 2` 仅用于检查未改动且早于新字段的历史记录。结果和命令输出明确标注旧版，并设置 `current_contract_checked: false`。评测器对应参数为 `--delivery-contract-version 1` 或 `2`。

版本 2 检查需求决定、阅读范围和报告哈希，不检查模型评审完成与抽查。旧版通过不等于当前契约验收。不要为旧运行补造授权引文或评审哈希；新交付应实际完成并记录缺失工作，冻结研究不倒填。

## 回归覆盖

`python3 scripts/check_delivery_contract.py` 在隔离控制中重新封存无关哈希，避免旧凭证掩盖目标缺陷。覆盖正常控制、自定义消息、回复差异、声明范围、有限审查顺序及终态真值组合，不证明能识别所有自然语言完成声明或研究质量。

`python3 scripts/check_evaluator_contract.py` 覆盖跨入口恢复、后续局部阻断、错误或非 UTF-8 历史、仅分派的问题、否认或部分披露限制，以及中英文不同文本和重复文本。控制在隔离副本内运行，冻结报告和研究输入不改写。

版本 2 控制包括有无授权的需求关闭、全文与部分阅读、当前稿件及过期全局/专项评审。旧正常和回归样例明确用版本 1 保留历史比较；原输入和哈希不变，新正例仅在临时副本中构造。

`scripts/check_review_completion_contract.py` 的版本 3 控制覆盖缺失或失败席位、不完整或过期证据、重复回复、独立裁定、负评评测结果、抽查及兼容。所有记录样例明确为合成数据，不是模型评审证据。
