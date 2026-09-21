# 评测结果 schema v2 迁移

[English](evaluator-v2-migration.md) | [简体中文](evaluator-v2-migration.zh-CN.md)

schema v2 明确区分机械符合性与研究质量：通过配置检查不等于研究质量通过。

| 旧字段 | schema v2 字段 |
|---|---|
| `status` | `conformance_status` |
| `score` | `conformance_score` |
| `max_score` | `max_conformance_score` |
| `quality_flags` | `conformance_flags` |
| 未明确质量边界 | `research_quality_status: not_evaluated` |
| 无 schema 标识 | `result_schema_version: 2` |

`coverage_flags` 继续保留。结果示例：

~~~json
{
  "result_schema_version": 2,
  "conformance_status": "pass",
  "conformance_score": 100,
  "max_conformance_score": 100,
  "conformance_flags": [],
  "coverage_flags": [],
  "research_quality_status": "not_evaluated"
}
~~~

使用方应明确检查版本，并读取符合性字段：

~~~python
assert result["result_schema_version"] == 2
mechanically_passed = result["conformance_status"] == "pass"
# mechanically_passed 不能转化为事实正确或编辑质量通过。
~~~

默认情况下，`review`、`fail` 或必需输出缺失都会返回非零退出码。`--allow-review` 允许探索性运行在 `review` 状态下成功退出，但不会将结果改成 `pass`。

历史输出保持原样，导入时标识它的 schema。改字段名不会追溯性地证明研究质量。独立交付检查器使用另一套 `ok`/`flags` 契约，不能按评测结果格式解析。
