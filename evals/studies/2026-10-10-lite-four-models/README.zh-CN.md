# 四模型固定来源 Lite 小型试验 — 2026-10-10

[English](README.md) · [简体中文](README.zh-CN.md)

这项前瞻开发试验让**四个作者模型分别完成同样五个任务族**：三题原生英文、两题原生中文。每对使用同一模型、brief、来源文本和资源上限，随机安排生成顺序及 A/B 展示。它检验一次回复、仅提供指令的 Lite，不包含检索、MCP、持久状态或 Full 评审门槛，不能证明工具箱具有普遍质量优势。

## 原始主结果

保留全部 40 次首轮作者请求。失败或格式不合要求的输出仍是未决，不计质量零分，也不判另一组获胜。下表偏好来自首轮、未经独立裁决的 LLM 评审；四个模型重复的是同样五个任务族，因此仍是 **n=5 个任务族**，不是 20 道独立任务。

| 作者 | 偏好工具箱组 | 偏好基线组 | 持平 | 未决 |
| --- | ---: | ---: | ---: | ---: |
| DeepSeek | 0 | 1 | 1 | 3 |
| Kimi | 0 | 0 | 0 | 5 |
| GLM | 0 | 0 | 0 | 5 |
| LongCat | 0 | 0 | 0 | 5 |

作者执行情况：DeepSeek：3 次输出截断、1 次严格 JSON 解析失败；Kimi：10 次严格 JSON 解析失败；GLM：9 次严格 JSON 解析失败；LongCat：6 次超时／超过时限、2 次严格 JSON 解析失败。详见原始 execution／invalid 记录；请求完整返回仍可能解析失败。

## 单列的格式补充分析

观察到作者解析失败后，[明确记录的事后规则](format-supplement-policy.json)允许去除完整 JSON 外层的一对 Markdown 代码围栏。两次作者请求必须完整返回，至少一组需要这项处理，且该对尚无主评审。规则不修 JSON 语法、不改正文、不重新生成作者回复，也不重试评审；四个模型同等适用。上方主结果保持原样。

| 作者 | 适用配对 | 偏好工具箱组 | 偏好基线组 | 持平 | 适用但未决 |
| --- | ---: | ---: | ---: | ---: | ---: |
| DeepSeek | 0 | 0 | 0 | 0 | 0 |
| Kimi | 5 | 3 | 1 | 1 | 0 |
| GLM | 3 | 1 | 2 | 0 | 0 |
| LongCat | 0 | 0 | 0 | 0 | 0 |

补充分析纳入 8 对此前未评审的报告，没有新增作者调用。这些是同一批任务的补充诊断，不增加任务数，也不替换主结果。[转换记录与原始回复哈希](format-supplement/)将每份合格报告对应到首份回复。规则登记在格式失败出现之后、查看任何评审偏好之前，不属于原始冻结分析。

## 如何理解评审

保留的银行聊天机器人评审更偏好 DeepSeek 基线，理由是试点边界和停止条件更具体，同时认为工具箱报告的安全机制讨论更充分。按空白分词、含标题，两份分别为 913 与 785 词，任务要求 600–800 词。GLM 生产率补充评审偏好的工具箱报告，仍把制造业历史比较起点误写成 1947 年；随附 BLS 正文写的是 1987 年。Kimi 电池市场补充评审更偏好工具箱报告，认为它把机会连接到尚未签约的采购和供应商规格，同时明确指出两篇都有无依据推断。这些已对照原文的例子说明取舍与判断局限，不代表对全部评分的独立裁决；原评审均保留。

## 任务与来源

| 任务 | 语言／要求篇幅 | 纳入的来源单元 |
| --- | --- | --- |
| [电池储能市场调研](inputs/briefs/battery-market-en.md) | 英文，600–800 词 | [EIA 文章正文](inputs/sources/battery.md)；已装与计划功率容量，不是供应商收入 |
| [银行聊天机器人试点](inputs/briefs/banking-chatbots-en.md) | 英文，600–800 词 | [CFPB 正文与尾注](inputs/sources/chatbots.md)；投诉案例，不是发生率 |
| [内存安全路线图](inputs/briefs/memory-roadmap-en.md) | 英文，600–800 词 | [CISA 资源介绍](inputs/sources/memory-roadmap.md)与[公告](inputs/sources/memory-oss.md)；未提供链接的报告全文 |
| [生产率与软件销售目标](inputs/briefs/productivity-outlook-zh.md) | 中文，1,000–1,400 字 | [BLS 公告叙述正文](inputs/sources/productivity.md)，截止表 A1 前；未提供表格和技术说明 |
| [小企业 AI 风险管理](inputs/briefs/ai-risk-adoption-zh.md) | 中文，1,000–1,400 字 | [NIST 常见问题](inputs/sources/ai-faq.md)与 [AI RMF 核心文本](inputs/sources/ai-core.md) |

组织及决策场景是假设的，来源是实际美国联邦机构出版物。[来源清单](inputs/source-manifest.json)保留网址、文本单元范围和哈希。公开文本于 2026 年 10 月 10 日获取，各题另列历史决策时点。这是有目的选取的开发样本，不声称留出、代表总体或未进入模型训练。BLS／CFPB 直接下载不可用时使用浏览器文本，保留可见链接标签、去除提取工具标记；未另行获取引用的第三方作品。随附文本单元不代表已经读取全部链接报告、表格和图片。

## 模型、预算与条件隐藏

| 请求及成功返回的作者模型 | API 路径 | 顺序／展示随机种子 |
| --- | --- | --- |
| `deepseek-flash` | `api.deepseek.com` | 20261010 |
| `kimi-k2.6` | `api.moonshot.cn/v1` | 20261011 |
| `glm-5.3` | `open.bigmodel.cn/api/paas/v4` | 20261012 |
| `LongCat-2.5-Preview` | `api.longcat.chat/openai/v1` | 20261013 |

先通过原生 CLI 尝试 GLM Coding Plan，服务返回订阅过期错误，随后全部 GLM 报告使用普通 API。这些名称是服务方模型别名，不是不可变权重快照。每个作者条件的输出上限为 12,288 token，总量上限 98,304 token，请求时限 240 秒；服务方的输出用量包含思考 token。GLM 两组均使用 `reasoning_effort=low`，其余模型保持服务方默认思考参数。总用量与耗时在返回后核对；超时不证明远端已取消，也不证明没有计费。

工具箱组收到完整固定版本的 Skill、工作流、研究规范和写作参考。两组的 brief、来源及 report／notes JSON 格式相同，评审只看到正文字符串。工具箱输入更长，相同上限不等于实际成本相同。[用量记录](usage.csv)保留逐次 token、耗时和缺失情况，不推算金额。

| 作者 | 调用／完整返回 | 已知输入 token | 已知输出 token | 缺用量调用 |
| --- | ---: | ---: | ---: | ---: |
| DeepSeek | 10 / 7 | 111,599 | 91,073 | 0 |
| Kimi | 10 / 10 | 110,228 | 56,036 | 0 |
| GLM | 10 / 10 | 110,698 | 18,909 | 0 |
| LongCat | 10 / 4 | 47,244 | 24,266 | 6 |

统一评审通过原生 CLI `0.162.0-alpha.17.2` 请求低思考档 `gpt-6-astra`，每对使用新的临时只读上下文，消耗用户已配置的 CLI 额度；服务端实际模型身份未独立确认。评审材料仅含 brief、来源、固定五维 0–4 量表和随机 A/B 正文，不含分组或作者 notes。原始事件记录工具使用；调用工具的评审不通过隔离检查。关闭用户配置和项目文档，但宿主基础上下文或 Skill 元信息仍可能存在。评审的 8,192 输出 token 上限是在返回后检查，并非 CLI 生成时的硬上限。

正文原样送评，也保留可能暴露条件的线索。例如，DeepSeek 与 GLM 的生产率评审都记录了“没有独立复核”之类的流程线索。因此，只能确认隐藏了分配标签，不能保证盲法完全有效。这是小样本、单一评审者试验，没有人工校准或独立裁决。逐维分数及定位理由见 [scores.csv](scores.csv)和对应原始评审，不把它们当成已确认的必要缺陷标签。

[计划](study-plan.json)、来源包、工具箱文本、量表和分组在作者生成前本地冻结，**没有事先公开时间戳注册**。[harness-snapshot.py](harness-snapshot.py)保留原脚本，各模型冻结承诺位于 `runs/*/coordinator/`。既有历史研究、标签和失败记录未改动。

## 查看与复现

在仓库根目录离线核对全部材料哈希和输入匹配，不调用模型：

```bash
python evals/studies/2026-10-10-lite-four-models/verify_bundle.py
python evals/studies/2026-10-10-lite-four-models/summarize.py
```

第二条命令从原始文件生成 [summary.json](summary.json)、[scores.csv](scores.csv) 和 [usage.csv](usage.csv)。离线检查证明材料保留与输入匹配，不证明报告质量。

重新生成时，在进程环境中设置 `DEEPSEEK_API_KEY`、`KIMI_API_KEY`、`GLM_API_KEY`、`LONGCAT_API_KEY`，安装并登录原生评审 CLI，将其加入 PATH 或设置 `CODEX_BIN`；使用固定的工具箱方法和脚本版本，然后运行：

```bash
python evals/studies/2026-10-10-lite-four-models/reproduce.py --output evals/runs/lite-four-models-repeat
```

命令产生 **40 次作者 API 调用及最多 20 次评审调用**，消耗自己的供应商账户与 CLI 额度；复用本研究普通 API 路径，不重新探测 Coding Plan。输出必须是新目录。加 `--prepare-only` 可零调用准备；加 `--include-format-supplement` 则在主结果锁定后执行单列规则。补充分析不增加作者调用，主评审加补充评审总上限仍为 20。主结果有未决时返回非零退出码并保留记录，不表示应重跑失败。模型别名、服务可用性和回复可能改变，不保证逐字复现。

| 材料 | 内容 |
| --- | --- |
| `inputs/` | brief、实际提供的来源文本、出处、四模型配置与评审 schema |
| `runs/<model>/` | 冻结分组与方法、全部首轮作者请求／回复／失败、主评审输入／回复、用量、结果及哈希清单 |
| `format-supplement/<model>/` | 适用性记录、不改正文的格式转换、单列锁定评审与补充结果 |
| `run_live_study.py`、`run_format_supplement.py` | 未在运行后改写的执行适配器；通过 `reproduce.py` 调用 |
| `host.json` | 操作系统、Python／CLI 版本及模型身份边界 |

原始回复内容及失败完整公开。含机器信息的原生 CLI stderr 私下保留，未纳入这些证据清单，也不支持任何质量结论；公开包不含凭据或本机账户路径。Git 属性保留原始字节，避免不同系统检出时改变冻结材料哈希。
