# 两篇报告的数值含义与评审结果更正

[English](README.md) | [简体中文](README.zh-CN.md)

2026-10-21，核对 PR #88 的报告与原有合成来源，确认两篇原稿把“缺少原因码的比例”写成“完整度”，作者自检和外层 Grok 评审均未处理这些错误。两篇原稿的无条件“达标、来源一致”结论不能继续作为当前结果引用；两份批次摘要中的“六题全部达标”也不能作为当前有效结论。历史原件全部保留在[入库目录](../../studies/2026-10-21-external-batches/README.zh-CN.md)。

| 报告 | 来源与原稿位置 | 局部修订 |
| --- | --- | --- |
| [AI 劳动力与 FTE 修订稿](reports/ai-agent-workforce-fte-roi-bar-en-20261018.md) | [S4 第 7 行](../../studies/2026-10-21-external-batches/tasks/ai-agent-workforce-fte-roi-bar-en-20261018/sources/S4.md#L7)明确是 62% 的人工修改缺少原因码。[原稿](../../studies/2026-10-21-external-batches/tasks/ai-agent-workforce-fte-roi-bar-en-20261018/final.md)第 13、42、62、96 行却写成完整度 62%；第 27、50 行的缺失含义正确。 | 只改四处错误表述，统一为 62% 缺少原因码；原有正确表述、其他数字和主要建议不变。 |
| [券商研报外发修订稿](reports/broker-research-llm-publish-bar-zh-20261019.md) | [S4 第 7 行](../../studies/2026-10-21-external-batches/tasks/broker-research-llm-publish-bar-zh-20261019/sources/S4.md#L7)明确是 41% 的人工改写缺少原因码。[原稿](../../studies/2026-10-21-external-batches/tasks/broker-research-llm-publish-bar-zh-20261019/final.md)第 60 行含义正确，第 74 行却写成完整度 41%。 | 只改第 74 行为 41% 的人工改写缺少原因码，其他内容及主要建议不变。 |

[FTE 外层评审](../../studies/2026-10-21-external-batches/tasks/ai-agent-workforce-fte-roi-bar-en-20261018/review/outer_grok_review.md)第 55 行将错误的“62% override completeness”判为 Match，第 57 行称未发现实质数字误读。[券商外层评审](../../studies/2026-10-21-external-batches/tasks/broker-research-llm-publish-bar-zh-20261019/review/outer_grok_review.md)第 28 行称主张与来源一致且无需退回，第 59 行用含义不清的“覆盖 41%”判为一致，未指出正文矛盾。这是两次具体的作者自检和外层评审漏检；修订稿不是新的模型运行或评审通过记录。

原稿、来源、`finish.json`、机械检查输出、外层评审、批次简报与摘要均未改动。原运行仍为 12 次（8 道新题、4 次复测）；表内修订次数仍描述历史运行，本次两份另存稿不增加任务或运行计数。其他十篇维持历史记录，没有在本轮重新判定全部通过。

本轮核对仅确认上述四处英文表述及一处中文表述已与 S4 的缺失比例一致，其余正文保持原样。沿用现有归档核对方式，仅更新入库中英文 README 的哈希；原始证据哈希不变。不重跑研究、不新增评审或检查机制、不改 Toolkit 产品代码。这是报告与结果记录的修订，不是 Toolkit 核心能力升级。
