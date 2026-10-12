# 开发协议 v2：输出、盲法与任务设计

[English](eval-protocol-v2.md) · [简体中文](eval-protocol-v2.zh-CN.md)

这是[固定来源 Lite 试点](eval-protocol.zh-CN.md)的可选扩展，用于后续执行，不改写 10 月 10 日冻结研究。本次没有新增模型运行或质量结果。继续支持 schema 1；schema 2 暂只接受 `prospective_development`，已暴露题目不能改个标签就变成留出集。

## 冻结什么

从[空白 v2 模板](../evals/templates/blinded-study.v2.json)开始，或检查[五任务族虚构开发材料](../evals/tasksets/development-v2-synthetic/README.zh-CN.md)。填写作者／评审端点、请求模型、允许的返回模型名称和快照局限。作者与评审须使用不同身份；声明的名称重叠会被拒绝。这不能独立证明提供商身份或模型族独立性。每个作者模型单独冻结计划，各模型层保留共用的任务族编号。

每个角色声明 `output_protocol`、`allow_json_fence` 和 `response_format`。`response_format: text` 不向 API 发送格式选项；`json_object` 显式发送该选项，须由提供商支持。选择前核对当时的官方文档；不自动探测提供商、不回退格式、不重试。两组作者使用相同的协议、模型设置及上限。

默认作者协议 `markdown_notes_v1` 要求完整 Markdown 正文之后恰好出现一行分隔符：

```text
<<<RESEARCH_NOTES_V1>>>
```

分隔符之前全部是正文，不裁剪、不改写；之后是工作笔记。缺少或重复分隔符计为格式失败。也可使用 `json_object_v1`，要求 `report`、`notes` 字符串。评审使用 `json_object_v1` 和既有五维结构。`allow_json_fence` 为 true 时，允许覆盖整个输出的单个围栏，语言标签仅可省略或精确为 `json`；拒绝前后解说、拼接对象和重复字段。不从任意文本中猜测截取 JSON。这些规则须在生成前声明，不能看过结果后用来挽救偏好的样本。

API 返回字节保存在 `response.json`；成功提取消息后另存 `content.txt`、`parse.json`（协议、成功时的解析方法、内容哈希及状态），以及 `parsed.json` 或 `invalid.json`。执行失败记录在 `execution.json.failure_kind`：HTTP、传输、超时、返回结构／大小、模型身份、缺少用量、token 超额、截断、未正常结束或空内容。这些是执行／格式结果，不是研究质量缺陷。过大返回只保留有界前缀，并明确说明。总 token 和墙钟时间在返回后检查，不能保证费用上限或取消远端请求。

`max_retries` 固定为零。`max_requests` 必须等于每任务族三次请求，或在 `position_swap: true` 时为四次：两个作者、一个主评审及可选的互换评审。缺少作者输出时跳过该对的两次评审；主评审失败不取消预先声明的互换评审。`request_plan` 冻结上限，结果记录实际尝试次数。四个作者模型、五任务族并互换顺序将允许 **80 次**请求，而非 20 次；本材料只供离线检查，实际运行按另行冻结计划执行。先按改进计划完成至多五次接入调用。

`prepare` 冻结来源／题面文本哈希、设计记录、指令、量表、代码哈希、分配和上限。`execute` 核对承诺，schema 2 在调用前拒绝变更过的执行脚本。输入经 Python 通用换行读取后按 UTF-8 文本冻结；这是文本哈希，不是原始来源文件字节哈希。Git 须在 PATH 中。执行器更新后须另建研究目录；已启动运行不能静默续跑或覆盖。

```bash
python scripts/run_blinded_evals.py prepare --study evals/tasksets/development-v2-synthetic/study.json --seed 20261012 --output evals/runs/v2-inspection
```

上述检查命令调用模型零次。随附模型和端点是占位值；真实运行须使用核实后的设置，另行冻结计划。密钥不进入配置、来源、命令参数或公开材料；端点配置只保存环境变量名。

## 任务准入和信息分离

5—10 个不同任务族各需一个设计 JSON 路径，包含 `role: development`、`material_kind`、`rationale`、`provenance`、`exclusions`、`expected_judgments`、`exposure`；最后两项是非空列表。设计记录只在 `coordinator/frozen.json` 中，作者只收到题面／来源和所属条件的指令，评审只收到题面、相同来源、量表及 A/B 正文。预期判断是协调者注释，既不是给作者的答案提示，也不自动成为评审分数。结构检查不能证明任务独立或来源充分，这些声明应在冻结前实质审查。

分为三个不同材料池：

| 材料池 | 用途 | 当前材料 |
| --- | --- | --- |
| 开发 | 诊断缺陷、调整方法 | 五个已暴露的虚构任务族，3 英文、2 中文 |
| 评审校准 | 检查已知错误、有效对照及位置敏感性 | 独立的算术错误对、标签互换和同一有效稿件平局对照 |
| 未来留出研究 | 用未参与调参的材料检验冻结改动 | 本次未提供、未宣称；另需编写／访问记录和新设计 |

这是目的性选题，不是代表性工作负荷抽样。翻译、不同作者模型和标签互换不增加独立任务族。合成任务检验协议；真实研究评测还需权利清晰的真实来源、来源记录、截止时间，以及问题本身必要的实时检索。在结果出现前保留排除候选的编号和理由，在准入后保留全部失败。

## 盲法与校准

正文原样传递，不能看到输出后删除泄露条件或不利的句子。`coordinator/masking-observations.json` 记录少量 Toolkit／条件／模型词项的字面出现和正文哈希。这种提示扫描不排除报告，也不能证明盲法成功；它会漏掉转述、别名及风格线索。评审既有的 `condition_clues` 字段在评分后提供另一项观察。

仅将 `judge-inputs/` 交给评审上下文，不允许它访问分配密钥、开发答案、作者请求／notes、元数据、仓库及本设计对话。Codex 评审适配器需要另行保证这种隔离；v2 通用执行目前使用兼容 HTTP 端点，不启动 Astra 或原生 CLI。模型不能作为自己稿件的独立评审。仅使用新的请求也不证明统计独立。

启用互换后，两种顺序各用新请求。全部首轮评审／失败锁定后才解码。主结果保持不变；`position_swap` 单列互换偏好、解码后的条件及一致性，任一结果未解决时一致性为 `null`。不能选择更有利的顺序、用平均数抹去分歧或重跑。互换是同一任务族内的敏感性观察。

质量研究前，先使用[独立校准包](../evals/tasksets/judge-calibration-v2/README.zh-CN.md)，不传入答案密钥。要求评审定位并说明已知错误、互换后仍识别该错误，并且不在相同有效稿件间编造实质差异。保留失败，依据来源裁定解释。目前仅一个算术例，校准尚不完整：中文与非数值对照仍待设计。通过它不证明五维评审可靠，更不证明 Toolkit 有效。

## 离线验收

```bash
python scripts/check_blinded_evals.py
python scripts/check_blinded_protocol_v2.py
python scripts/check_study_verification.py
```

检查覆盖解析正负对照、原始输出保留、API 选项、别名、失败分类、冻结后代码变更拒绝、任务准入、元数据隔离及互换结果解码。不调用真实模型，只验证软件行为。
