# 参考阅读与改动落点

读取日期：2026-10-27。此说明记录本次实际阅读范围，不是额外研究流程。

## 阅读范围

- [即刻原帖](https://m.okjike.com/originalPosts/6ad87b38756bbb6658221e70)：网页正文解析最初失败，随后直接取得 HTML，并从 `__NEXT_DATA__` 读取帖子正文和图片列表。
- [Puggo 主页](https://m.okjike.com/users/C1A154C3-A334-4BFE-B7A5-F06F84436FB9)：取得同一帖子，核对 ID 和图片列表。
- [YouMind 中文说明](https://youmind.com/zh-HK/evaluating-writing-sense-for-ai-agents)及[英文说明](https://youmind.com/evaluating-writing-sense-for-ai-agents)：通过网页工具阅读方法、完整题目示例、结果与限制。直接下载 HTML 连接失败，不影响网页阅读。
- 七张配图已下载并逐张以原始分辨率打开，读取文字、图表与脚注。原帖和主页各自的该帖子对象都只列出七张图片；未取得第八张。图片标为 1/8—7/8，不据此猜补第八张。

## 图中口径

| 图片 | 实际阅读要点 |
| --- | --- |
| [1/8](https://cdnv2.ruguoapp.com/Fh4ZSun8knBWT-hB13wQrn1hwaOpv3.png) | 文感总分按阅读 25%、写作 75% 加权；不是单独的阅读分数。两个示例模型均为高思考配置，90.3 与 48.1 的差约 42 分。 |
| [2/8](https://cdnv2.ruguoapp.com/FkegDcBr4Axys0sezWrIEomP6RdQv3.png) | 逐项满足情绪描述，不一定实现具体叙事目的；判断依赖上下文。 |
| [3/8](https://cdnv2.ruguoapp.com/FiLlMVjJXQZXxwyW9mfpfu8RnEa4v3.png) | 从文章关键段落构造候选，分别观察选择与写作；脚注限定唯一答案仅适用于该候选集。 |
| [4/8](https://cdnv2.ruguoapp.com/FvXUzpZoVl2E7dCCMqkeu6_TND7Bv3.png) | 高思考配置的总分与单次成本并列。此次不把该排名或价格作为 Toolkit 模型选择依据。 |
| [5/8](https://cdnv2.ruguoapp.com/Fhp1W9WOjqRRLGjIg4A33fvijpJgv3.png) | 长度为字符数之比，各模型取输出中位数；图中总体中位数 1.6 倍，不是 token 开销。 |
| [6/8](https://cdnv2.ruguoapp.com/Fta9lq_cswxXcCN6JvYtFp-01m5jv3.png) | 干扰材料采用量相对于必需材料采用量，不能改写成错误率或全部采用材料中的比例；较短也可能漏掉必需材料。 |
| [7/8](https://cdnv2.ruguoapp.com/FkeKIv6TMK9g6Ep1LDjP3q6KWMuBv3.png) | 58% 仅针对模型每次都读对的文章，其写作仍违反至少一项构造取舍。两个无此类文章的模型被排除，不是所有任务的失败率。 |

官方完整示例同时展示了偏离目的的扩写和删得过多的候选。可借鉴的是用具体上下文解释取舍，并分别观察识别与生成。自由写作允许多种好答案，原作者并非天然正确。此次只观察实际正文的依据、解释和用途，不移植文感分数、作者意图匹配率或字数偏好。

## 最新仓库已有内容及本次增量

基线为 `8e3db9db49aeda63bc9c3b1790da7702f8b66649`。

| 已有文档 | 已覆盖 | 本次处理 |
| --- | --- | --- |
| `references/writing-style.*` | 读者用途、保留理解所需关系、事实含义一致、改写对照 | 在同一文档补三组材料—原稿缺口—正文改写—取舍理由；按需读取。 |
| `references/research-workflow.*` | 需求、分析单元、深度规划、八家公司管线完整论证示范 | 复用，不再增加原则或第二套示范流程。 |
| `references/subagents-and-review-loop.*` | 结合任务和证据审阅具体段落，作者意图不能凌驾事实 | 复用现有审阅方式，本次审阅隐藏方法版本；不增加必经评审。 |
| `references/quality-gates.*` | 补足薄弱论证再编辑、保留有用证据、读者审阅 | 复用，不增加交付门槛。 |

三组示范分别取自公开归档的预测性维护稿及其修订、Scope-3 RFQ 稿及其修订、Maple 存储采购材料。原材料本身为合成材料；前两组是教学改写，第三组新增的要求变化明确标为构造。历史报告、判断和记录均保留。正文中的源文件链接可以定位原材料，示范不是唯一标准答案。
