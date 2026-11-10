# 三份长研究的限定表达修订

[English](README.md) | 简体中文

基于 `a183353`（v2.4.0），另存 TTC 英文、前置仓中文和端侧模型英文的表达修订。合并重复概括、收紧泛泛限定并前移已有判断，保留原题、计算、假设和来源。来源审阅还纠正了一处既有事实错误：ASR 论文明确给出了 328 秒音频总时长。原稿、首次表达修订和原审阅均保留，TTC 已修好的引用标签继续沿用。

| 报告 | 完整修订稿 | 变化与版本对照 |
| --- | --- | --- |
| Test-Time Compute | [修订稿](reports/test_time_compute_en.md) | [逐项说明](changes/test_time_compute_en.md) · [完整 diff](changes/test_time_compute_en.diff) |
| 国内本地生活前置仓 | [修订稿](reports/instant_retail_warehouses_zh.md) | [逐项说明](changes/instant_retail_warehouses_zh.md) · [完整 diff](changes/instant_retail_warehouses_zh.diff) |
| On-Device Models | [修订稿](reports/on_device_models_en.md) | [逐项说明](changes/on_device_models_en.md) · [完整 diff](changes/on_device_models_en.diff) |

[版本清单](changes/manifest.json)记录原题、原稿、来源索引、分析、原评审、本地完整材料位置和原稿/修订稿 SHA-256。变化说明与 diff 用于接续现有独立审阅。

前置仓档案导航：[阅读记录](../../studies/2026-11-09-long-research/reports/instant_retail_warehouses_zh/analysis/reading-ledger.json)保留实际读到的原文位置、版本及阅读者；[主张记录](../../studies/2026-11-09-long-research/reports/instant_retail_warehouses_zh/analysis/claims.jsonl)区分来源事实、作者推断与情景结果。这些生产记录的用途移到此处说明，原件未改动。

七项独立内容视角和领域专审保存在[评审目录](reviews/)，随后完成[独立审计](reviews/audit.json)与[最终验收](reviews/acceptance.json)。三份当前稿均通过最终验收。ASR 时长更正、前置仓正文移出生产台账说明这两项必要修改，已由各自原评审者确认解决；三条可选措辞建议保留未改。最终验收还澄清了审计记录中的两处标签误写，原始意见没有被覆盖。

这是既有报告的有限修订，没有新增 benchmark 运行，也不作为整体研究质量提升或用户返工减少的测量结果。首次表达修订、必要发现、作者回复和续审均保留。
