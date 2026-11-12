# Portfolio arithmetic correction / 组合收益计算更正

2026-11-12. The original [script](../scenario-model.py), [results](../scenario-results.json), [accepted report](../../final.md) and historical review records remain unchanged. This directory contains the corrected calculation; the [current manuscript](../2026-11-12-arithmetic-revision.md) also retains the November 11 two-location editorial revision.

2026年11月12日更正。原脚本、结果、验收稿与审阅记录保留。本目录交付更正后的计算；当前正文同时保留11月11日两处表达修订。

| Quantity / 指标 | Archived result / 原结果 | Corrected / 更正结果 |
| --- | ---: | ---: |
| Mean distributable revenue / 平均可分配收入 | 1,000,000 yuan | 980,000 yuan |
| Creator contribution / 片方期望贡献 | −250,000 yuan | −257,000 yuan |

The stated pools are 300,000, 1,000,000 and 5,000,000 yuan, with probabilities 0.6, 0.3 and 0.1. Their weighted mean is 980,000 yuan. A 35% creator share minus a 600,000-yuan budget gives −257,000 yuan. The original script hardcoded both output values; the corrected script derives them from the input pools, probabilities, share and budget. The break-even hit rate remains approximately 26.44%.

给定可分配收入30万、100万、500万元及60%、30%、10%的概率，加权均值为98万元；片方取得35%并承担60万元成本，期望贡献为−25.7万元。原脚本直接写入了错误结果常量，更正稿改为从输入计算。保本爆款率仍约26.44%，亏损方向不变。

Run from the repository root / 在仓库根目录复算：

```sh
python evals/studies/2026-11-09-long-research/reports/microdrama_market_zh/analysis/2026-11-12-portfolio-correction/scenario-model.py
```

The corrected run retained all other JSON sections exactly: 23 scenarios, contract/hybrid results and six cash-flow summaries. All seven CSV files match the archived files byte for byte. [Comparison](comparison.json) records the changed quantities. The displayed website uses the corrected manuscript. This is a calculation and publication correction, not another research assignment or a new full-report acceptance.

此次运行中，除组合计算部分外，JSON中的23组情景、合同与混合模式结果、六份现金流摘要均与归档相同；七份CSV逐字节一致。对照文件记录更正值。在线正文采用更正稿；本次属于算术与展示更正，不新增研究题，也不改写原整篇验收。
