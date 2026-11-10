# On-Device Models：表达修订说明

作者修订，待独立审阅。本次沿用冻结题面和材料，不新增研究或改变原稿、原评审。

- [原题](../../../studies/2026-11-09-long-research/reports/on_device_models_en/task.json) · [原稿](../../../studies/2026-11-09-long-research/reports/on_device_models_en/final.md) · [来源索引](../../../studies/2026-11-09-long-research/reports/on_device_models_en/sources/source_registry.csv) · [原分析](../../../studies/2026-11-09-long-research/reports/on_device_models_en/analysis/) · [原评审](../../../studies/2026-11-09-long-research/reports/on_device_models_en/reviews/)
- [修订全文](../reports/on_device_models_en.md) · [完整 diff](on_device_models_en.diff)
- 本地完整原件：`C:/Users/luosong03/Documents/ChatGPT/Others/work/toolkit-long-research-20261109/evals/runs/2026-11-09-long-research/tasks/on_device_models_en`

原稿 SHA-256：`59f8ac88843287debab4c0176d72575b648dbf581eece7888f22e050e69da8dd`。
首次表达修订稿 SHA-256：`e82e4fbad93e8f1754b0ac613f333a1d3d68cd732d2556b26a3a464deea495bc`（[保留全文](on_device_models_en.editorial-first.md) · [当时完整 diff](on_device_models_en.editorial-first.diff)）。
当前修订稿 SHA-256：`c8d8f2b96f91e6032bbc542241417516d232e5fe28a707430eb297c87af2ea46`。

1. **§5，S24 响应设计段**：不再第二次抄写 §3 的 128/512 token、9.46/34.07 秒和 1,024 token prefill；指回该节完整计算并保留 performance lock、排除启动/呈现和不能推定日常或持续表现的边界，把本段留给短回复、流式显示与完整可用结果的区别。原数值及 512 token 超出实测 256 token 的说明在 §3 原样保留。
2. **§6，WhisperX 精度比较表后**：将“并非全面否定 INT8”的泛泛限定改为已有 medium INT8 行节能的正面反例。base 模型的内存、时长、能耗、WER 数值和 FP16 优先建议不变，仍明确精度选择取决于模型。
3. **附录末段**：删去再次泛泛提醒不能跨设备、运行时或任务套用速率的末句；完整的待测项目、建议边界、各实验条件及适配矩阵均保留。

4. **附录原 L287，EVIDENCE-ODM-01**：核对本地 ODM17 原文 p.7 Table 3，确认其明确给出 328 秒 clean audio。删除“未给出精确总音频时长”的错误限制，说明已知总时长支持聚合 RTF 算术，同时保留代码在读取时不可得、片段总量不等于持续流式延迟及整机墙插能耗的边界。第 6 节的 70 个短片段、基线扣除和 FP16/INT8 表不变；未新增 RTF 数值或重跑计算。[本次精确 diff](on_device_models_en.evidence-odm-01.diff) · [作者回复](author-response.json)。

硬件—模型—任务矩阵、内存/KV 公式、相位计时、持续性能边界、量化质量、语音流水线、隐私和 OS 条件、全部成本和能耗算例、版本与来源链接均保留。

作者核对范围：通读三份原稿与题面，逐项核对完整 diff 及修订后的上下文；网址序列、全部 Markdown 表格、代码围栏及未受影响段落保持不变。该检查用于交接，不构成独立审阅或最终验收。
