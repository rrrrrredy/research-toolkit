# Test-Time Compute：表达修订说明

作者修订，待独立审阅。本次沿用冻结题面和材料，不新增研究或改变原稿、原评审。

- [原题](../../../studies/2026-11-09-long-research/reports/test_time_compute_en/task.json) · [原稿](../../../studies/2026-11-09-long-research/reports/test_time_compute_en/final.md) · [来源索引](../../../studies/2026-11-09-long-research/reports/test_time_compute_en/sources/source_registry.csv) · [原分析](../../../studies/2026-11-09-long-research/reports/test_time_compute_en/analysis/) · [原评审](../../../studies/2026-11-09-long-research/reports/test_time_compute_en/reviews/)
- [修订全文](../reports/test_time_compute_en.md) · [完整 diff](test_time_compute_en.diff)
- 本地完整原件：`C:/Users/luosong03/Documents/ChatGPT/Others/work/toolkit-long-research-20261109/evals/runs/2026-11-09-long-research/tasks/test_time_compute_en`

原稿 SHA-256：`0b44a5d0d22dc9aeb62311374be99325839d4c9a62be3a389ddf584f791afe5e`。
修订稿 SHA-256：`b488ea30d8927356263be783f6f44b293f1a269d0c2547c8ad099f8598f941ef`。

1. **Research synthesis，第 2 段**：删除没有新增条件的引导句，让固定 checkpoint、自一致性、过程监督、修复训练和编码代理的既有正面结果直接开头。各结果的资源和信息边界保留。
2. **§7，CodeMonkeys 后的设计解释**：只删去泛泛的“任何多代理架构未必更好”提醒；共享上下文、不同修复路线、生成测试可能出错、选择成本及两篇来源归属均保留。
3. **§9 最后一段**：删除在摘要及 §14 已完整展开的五项选择清单，让跨领域一节止于数学、代码和交互任务的验证差异。§14 的条件、决策树和 §16 的停止情景均原样保留。
4. **§13，算例最后一段**：将反复提醒不要过度解读的表述合并为具体的 0.21 个百分点和抽样不确定性关系，仍明确概率是假设、真实试点不能据此确认准确率优劣，并保留风险和延迟的用途。
5. **§16 收尾段**：删除再解释“停止不代表短输出更好”的两句概括，保留难题值得充分计算的正面判断及完整成本核算原则。

方法和证据矩阵、全部数值与公式、假设算例、决策树、停止条件、两份附录和已修复的 TTC 引用标签均保留；未重新修复标签。

作者核对范围：通读三份原稿与题面，逐项核对完整 diff 及修订后的上下文；网址序列、全部 Markdown 表格、代码围栏及未受影响段落保持不变。该检查用于交接，不构成独立审阅或最终验收。
