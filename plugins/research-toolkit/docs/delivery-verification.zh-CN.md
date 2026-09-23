# 交付检查：契约与观察边界

[English](delivery-verification.md) | [简体中文](delivery-verification.zh-CN.md)

这是可选的离线一致性检查，不是运行时权限钩子，也不能证明 Agent 实际调用过它。研究和写作要求以 [SKILL.md](../SKILL.md) 为准；本页说明接口，不另加写作规则。

默认采用 **delivery contract 3**。交付凭证外层仍为 `schema_version: 1`，契约版本表示执行了哪些检查。结果包含 `delivery_contract_version`、`current_contract_checked` 和 `semantic_verification: false`，均不认证用户授权、实际阅读或编辑质量。

~~~bash
python <skill-directory>/scripts/check_delivery.py <task-directory>
~~~

凭证绑定当前成果、简报、进度、来源与主张记录、审查日志及拟发送的交付说明；适用的需求和不确定性文件也需绑定。凭证中已记录的每个路径都必须核查文件存在性、任务目录边界和哈希，即使绑定时属于可选文件；从未绑定的可选文件仍可缺省。文本哈希将 CRLF、CR 规范为 LF。相关修改完成后再封存，后续修改会使旧凭证过期；不为重建凭证重做无关研究。

用 `--delivery-message note.md` 指定其他交付说明文件，凭证须绑定选定文件。成果、凭证和拟交付说明的路径均须位于任务目录内。

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

## 比较实际回复记录

~~~bash
python <skill-directory>/scripts/check_delivery.py <task-directory> --actual-message captured-reply.md
~~~

将提供的回复记录与已绑定的拟交付说明比较，只规范换行和首尾空白。运行环境可以单独保存最终输出，在运行后调用检查器；保留原始输出并说明如何提取客户端元数据，不能悄悄删掉实质差异。

`delivery_observation` 为 `not_provided`、`matched`、`mismatch` 或 `unreadable`。指定的记录缺失或不一致会失败。`not_provided` 仅表示检查了拟发送文本，不证明用户收到它。

调用方提供的文件不是真实交付的认证。Agent 再写一份预期说明不构成独立捕获证据。本接口本身不拦截或强制约束实际最终回复。

## 必需模型评审的完成

contract 3 在原有交付检查之外要求[评审完成记录](review-completion.zh-CN.md)。在 `progress.json.review_plan` 中声明席位，`purpose` 使用 `report_delivery`。保留原始回复、执行记录、版本绑定、实质有效性核查、发现处置和抽查证据。

全局 PASS 不能填补缺失席位。调用失败和编辑意见分别保留。评审有效性与报告判断分开；即使有负面报告判断，也可使用 `check_review_completion.py` 和 `evaluation` 检查面板是否完成。交付检查器仍要求报告本身达到交付条件。

这些只是声明记录的检查，不能认证供应商、证明核查者独立、确认实际阅读，或保证严重度和裁定正确。

## 任务声明的审查范围

任务可在 `progress.json.required_review_scopes` 中声明多个互不重复的非空范围。最终交付前，每个范围的最新审查均须通过且无未结问题，全局审查仍然必需。此可选接口不会为普通工作自动增加评审者或轮次。模型 PASS 是判断，不是事实或编辑质量证明。

最新全局及每个必需范围须含 `artifact_sha256`，对应实际受评主要报告的 LF 规范化 SHA-256。缺失或错误格式触发 `missing_review_artifact_binding`；与当前报告不同触发 `stale_review_artifact`。凭证另行绑定当前审查日志。重建凭证不能让旧评审覆盖新正文；局部复核不能刷新全局绑定，全局 PASS 也不能刷新必需专项评审的绑定。

进度状态允许 `in_progress`、`paused`、`blocked`、`complete`。终态同时要求 `stage: final` 和 `status: complete`，只满足一个不够。

两个入口共享审查和未结问题语义。最新无问题的全局审查覆盖较早的普通单元审查；此后出现的阻断问题仍须由同范围的无问题审查或新的全局审查处理。局部 PASS 不能关闭其他范围或失败的全局审查。显式要求的范围始终独立，全局 PASS 不能取消它们。错误日志不能靠追加 PASS 修复，须明确保留并纠正错误记录。只有 `routed_action` 仍是计划，不是解决。

## 限制披露不是关键词认证

`limitation_disclosure.status` 区分 `not_applicable`、`absent`、`contradiction`、`text_covered` 和 `needs_review`。没有披露信号，或检测到全面否认已有的限制，会使机械检查失败；否认检测是有限启发式规则，不能识别所有措辞。

`text_covered` 表示规范化标点和空白后找到了已记录的限制文本，不代表其真实或诚实。仅部分匹配、改写表达或泛泛说明时，`needs_review` 给出 `unmatched_limitations` 和可见提示。正常同义表达不会只因无法精确匹配就失败，但机械 PASS 不能称为披露已核验。`semantic_verification` 始终为 false，含义、覆盖和重大矛盾仍需内容审阅。不要求固定措辞、额外声明文件或某家模型/API。

## 历史记录

`--contract-version 1` 或 `--contract-version 2` 仅用于检查未改动且早于新字段的历史记录。结果和命令输出明确标注旧版，并设置 `current_contract_checked: false`。评测器对应参数为 `--delivery-contract-version 1` 或 `2`。

版本 2 检查需求决定、阅读范围和报告哈希，不检查模型评审完成与抽查。旧版通过不等于当前契约验收。不要为旧运行补造授权引文或评审哈希；新交付应实际完成并记录缺失工作，冻结研究不倒填。

## 回归覆盖

`python scripts/check_delivery_contract.py` 在隔离控制中重新封存无关哈希，避免旧凭证掩盖目标缺陷。覆盖正常控制、自定义消息、回复差异、声明范围、有限审查顺序及终态真值组合，不证明能识别所有自然语言完成声明或研究质量。

`python scripts/check_evaluator_contract.py` 覆盖跨入口恢复、后续局部阻断、错误或非 UTF-8 历史、仅分派的问题、否认或部分披露限制，以及中英文不同文本和重复文本。控制在隔离副本内运行，冻结报告和研究输入不改写。

版本 2 控制包括有无授权的需求关闭、全文与部分阅读、当前稿件及过期全局/专项评审。旧正常和回归样例明确用版本 1 保留历史比较；原输入和哈希不变，新正例仅在临时副本中构造。

`scripts/check_review_completion_contract.py` 的版本 3 控制覆盖缺失或失败席位、不完整或过期证据、重复回复、独立裁定、负评评测结果、抽查及兼容。所有记录样例明确为合成数据，不是模型评审证据。
