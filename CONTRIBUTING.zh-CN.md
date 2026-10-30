# 贡献指南

[English](CONTRIBUTING.md) | [简体中文](CONTRIBUTING.zh-CN.md)

欢迎改进研究方法、使用流程、已证实的失败检测，以及项目主张的证据。说明具体问题和改动怎样解决它；独立编排产品不属于本仓库范围。


双语同步工作流会在 README、SKILL、CHANGELOG 或 CONTRIBUTING 配对仅有一方变更时留下不阻断合并的 PR 提醒；在 PR 描述中加入 `[i18n-skip]` 可跳过检查并移除已有提醒。

## 从失败案例开始贡献

无需改代码，也可以[**提交失败案例**](https://github.com/rrrrrredy/research-toolkit/issues/new?template=failure-case.yml)。说明研究问题、期望与实际结果，附报告原文片段、可用来源和评审配置；仅复现旧任务需要时附已保存的 profile 值。公开前去掉隐私和可识别信息。有原始材料、可复现的案例，经评审后可成为回归用例，详见[案例贡献流程](evals/README.zh-CN.md)。

## 适合首次贡献的小任务

以下是 `good first issue` 建议，不表示已经创建了对应 Issue。可选择一个具体问题提交 PR，也可通过失败案例 Issue 讨论范围。

| 方向 | 一次小贡献可以完成什么 |
| --- | --- |
| 改清楚一段说明 | 同步改善 README、`agents/` 或 usage 指南的中英文案，并核对关联示例。 |
| 完善 Agent 接入卡 | 复现一个加载问题，引用宿主官方要求，在双语指南中补一条针对性的排查步骤。 |
| 补充回归夹具 | 把已接纳的失败案例做成小型新夹具，配一个有效对照；保留现有标签与冻结研究输入。 |
| 改进已有 adapter 的接入 | 修正现有 adapter 的安装示例或配置诊断，附可复现命令与双语说明。 |

## 规范与范围

`SKILL.md` 是同一套研究规范的 Agent 入口；关键约束与 `references/research-standard.md`、配套方法中的详细规则保持一致，中英文一同维护。网页嵌入的主文件由 `check_docs_sync.py` 校验精确同步。README、接入说明、插件与示例不能另立冲突规则。机械符合、语义质量、加载检查和整体效果分别陈述。

## 修改前

1. 明确具体失败、使用困难或证据缺口。
2. 优先采用能改变可观察结果的最小修改。
3. 优先通过清晰、正确的实现解决问题。明确受影响行为及相关失败方式，已有验证能够覆盖时直接复用。
4. 保留有效正例，防止靠一律拒绝提高检出率。纯文档修改只检查内容、示例和链接，无须新增测试案例。
5. 使用合成或权利明确的数据；脱敏内部摘要仅是工作流种子，不是公共事实来源。
6. 开始运行后保留冻结输入，后来变化使用独立版本。

## 验证

按[当前兼容性约定](docs/compatibility.zh-CN.md)选择发布版本，保持公开接口及已有任务兼容；发布不兼容主版本时说明迁移步骤。

完成受影响代码的编译或构建及仓库强制检查。根据具体改动或已发现的失败选择必要的补充验证，复用已有覆盖。工作流变化可能需要端到端场景；确定性的解析、路径或状态行为可能更适合针对性检查。保留复现结果所需的输入、命令和输出。文档修改本身不要求新增研究运行或测试套件。

不重复运行已通过且不能提供新信息的检查，不自动叠加评审、版本对照或研究任务复跑。环境限制留下未验证内容时，交付说明原因、最小手动验证步骤、预期结果与注意事项。

[CI 工作流](.github/workflows/framework-checks.yml)是检查项目的权威清单；以下命令是常用入口，不是不同测试用例的计数。可选接入的 `validate` 只检查配置，不安装或启动运行时。仅在新变化、失败或未决疑点需要时扩大或重复检查。

```bash
python scripts/check_docs_sync.py
python scripts/run_dsh_evals.py validate
python scripts/check_eval_source_integrity.py
python scripts/check_source_policy_contract.py
python scripts/check_source_extraction.py
python scripts/check_regression_fixtures.py
python scripts/check_conformance_fixtures.py
python scripts/check_delivery_contract.py
python scripts/check_review_completion_contract.py
python scripts/check_evaluator_contract.py
python scripts/check_semantic_diagnostics.py
python scripts/check_installation_contract.py
python scripts/check_diagnostic_bundle.py --self-test
python scripts/check_semantic_review_bundle.py --self-test
python scripts/check_study_verification.py
python scripts/check_task_lock.py
python scripts/check_draft_contract.py
python scripts/check_plugin_build.py
python scripts/check_blinded_evals.py
python scripts/check_blinded_protocol_v2.py
python scripts/check_judge_calibration.py --self-test
python scripts/check_live_execution.py
python scripts/check_live_diagnostics.py
python scripts/check_development_evidence.py --self-test
python scripts/check_feedback_probes.py --self-test
```

修改主文件后先更新网页副本：

```bash
python scripts/check_docs_sync.py --write
```

更改 `run_evals.py` 必须保持 schema 语义：`conformance_*` 只表示机械符合；没有独立设计和校准的评测，不能把 `research_quality_status` 改成质量判决。

CLI 和 MCP 要求 Python 3.10 及以上。CI 在 Linux 上检查最低版本，并用 Python 3.12 执行 Linux／Windows 主运行检查；安装 `requirements-mcp.txt` 和执行 `check_mcp_contract.py` 须使用同一解释器。用 `python scripts/build_plugin.py --check` 核对生成插件与源文件同步。

分别报告测试方法数、夹具案例数、独立任务族、模型—任务对和 API 尝试次数。继承的测试可能在多个套件中重复执行，不能相加后当成独立对照数量。双语文件或标题数量相同不等于译文含义一致；应核对改动的规则、例子和限制。

## PR 证据

说明解决的问题、涉及文件与接口字段、实际运行的检查及结果；机械行为变更提供相应反例与有效对照，并披露限制和延后事项。

修复 PR 提供失败案例、实际修改和相关检查即可。现有用户与开发任务均可使用，Astra 可在单独上下文中评审。是否比较使用与不使用工具箱按需决定，如实记录实际任务、版本、资源与失败；该比较不是修复 PR 的前提。

## 来源处理与发布入口

[离线 HTML 提取](docs/source-extraction.zh-CN.md)保留原始发布及版本元数据，不增加评审要求或改变冻结输入。

中英文首页介绍同一工具箱，在靠前位置链接网页指南；重点是读者能做什么、从哪里开始。同步与打包政策留在维护文档。

需要平台插件或安装包时，包装同一技能并链接本仓库，不维护第二套规范。平台特有安装放在 `agents/`；接入说明不能暗示工具箱只适用于某供应商，或据此声称研究质量已验证。
