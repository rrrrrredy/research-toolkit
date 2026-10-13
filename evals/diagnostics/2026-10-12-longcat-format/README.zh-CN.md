# LongCat 格式补验 — 2026 年 10 月 12 日

[English](README.md) | [简体中文](README.zh-CN.md)

显式 JSON 协议**尚不能作为稳定替代方案**：四次首轮返回中三次成功解析。中文 Toolkit 返回把 `notes` 写成对象，而解析器要求字符串。整个输出的 JSON 围栏已预先允许，因此不是围栏导致失败。原提示只要求“单独的工作笔记”，没有明确字符串类型，这是需要向前修复的提示／schema 对齐缺陷，不构成强制转换历史对象的理由。

[计划](plan.json)和[承诺哈希](commitment.json)在四次调用前冻结。两个新编的虚构格式探针（英文阅览室、中文陶艺交接）各运行两组，次序交叉平衡。模型 `LongCat-2.0`、关闭思考、4,096 completion／32,768 总 token、180 秒超时，使用 `json_object_v1` 并允许整个输出的 JSON 围栏；未启用提供商 JSON mode。无评审、重试或质量评分。[结果](results.json)及全部原始返回／解析失败保留。

这些探针在原 LongCat 开发队列结束后运行，是单独的诊断，不是留出质量题。它们不替换[原来四个缺失配对](../../studies/2026-10-12-lite-four-models/README.zh-CN.md)。后续提示修复需要独立新冻结；3/4 不足以推荐该配置稳定通过。

[原清单](manifest.json)保存执行材料哈希，[公开清单](public-manifest.json)另含发布新增文件。harness／driver 归档包含精确执行字节。`python scripts/check_development_evidence.py --self-test` 在无调用、无写入条件下检查材料；检查格式和对应关系，不认证研究质量。
