# Limited expression revisions of three long reports

English | [简体中文](README.zh-CN.md)

Based on `a183353` (v2.4.0), this directory contains separate expression revisions of the English test-time compute report, Chinese instant-retail warehouse report, and English on-device model report. Edits merge repeated summaries, tighten generic qualifications, and foreground existing supported judgments. Tasks, calculations, assumptions and sources are retained. Source review also corrected an existing statement: the ASR paper supplies a 328-second aggregate audio duration. Original reports, first editorial revisions and reviews remain available; the corrected TTC reference labels are preserved.

| Report | Complete revision | Changes and comparison |
| --- | --- | --- |
| Test-Time Compute | [Report](reports/test_time_compute_en.md) | [Itemized note](changes/test_time_compute_en.md) · [Full diff](changes/test_time_compute_en.diff) |
| 国内本地生活前置仓 | [Report](reports/instant_retail_warehouses_zh.md) | [Itemized note](changes/instant_retail_warehouses_zh.md) · [Full diff](changes/instant_retail_warehouses_zh.diff) |
| On-Device Models | [Report](reports/on_device_models_en.md) | [Itemized note](changes/on_device_models_en.md) · [Full diff](changes/on_device_models_en.diff) |

The [version manifest](changes/manifest.json) records original tasks, reports, source indexes, analyses, reviews, complete local-material locations, and SHA-256 hashes of original and revised reports. The notes and diffs support continuation of the existing independent review.

Warehouse archive navigation: the [reading ledger](../../studies/2026-11-09-long-research/reports/instant_retail_warehouses_zh/analysis/reading-ledger.json) retains inspected source locations, versions and readers; the [claims record](../../studies/2026-11-09-long-research/reports/instant_retail_warehouses_zh/analysis/claims.jsonl) distinguishes source facts, author inferences and scenario results. Their record-keeping purpose is documented here outside the report; the original records are unchanged.

The seven independent content perspectives and domain review are retained in [reviews](reviews/), followed by [audit](reviews/audit.json) and [final acceptance](reviews/acceptance.json). All three current reports passed final acceptance. The ASR duration correction and removal of the warehouse report's production-ledger sentence were confirmed by their original reviewers. Three optional wording suggestions remain unchanged. Final acceptance also clarifies two inaccurate labels in the audit record without rewriting that original opinion.

This is a limited revision of existing reports, not a new benchmark run or a measurement of overall Toolkit quality or reduced user rework. The initial editorial versions, necessary findings, author responses and follow-ups are preserved.
