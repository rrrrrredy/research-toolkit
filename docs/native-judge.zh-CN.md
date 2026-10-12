# Codex 评审执行

[English](native-judge.md) · [简体中文](native-judge.zh-CN.md)

Schema 2 的评审可使用 `transport: codex_exec`；作者继续使用兼容 HTTP 接口。[带日期的 Astra 设置](../evals/configs/development-20261012/astra-judge.json)请求 `gpt-6-astra`，本机 Codex CLI 须已登录。把 `RESEARCH_CODEX_EXECUTABLE` 设为可执行文件的绝对路径；这是本地进程设置，不是 API 密钥，也不修改仓库配置。

每份评审输入启动一个全新、临时 CLI 进程，在中性的临时目录中运行。只提供冻结的评审指令和输入包，忽略用户配置，关闭项目指令、记忆、宿主技能发现、插件、应用、命令行／浏览器／电脑／图像工具及委派；子进程只继承系统环境白名单，不接收作者 API 密钥或父对话标识，不恢复或分叉已有对话，保留只读沙箱。独立 provider 配置使用 Codex 正常认证，并将 HTTP 与流重试均设为零；当前 CLI 会拒绝覆盖保留的 `openai` provider。

保留原始 `events.jsonl`、`stderr.txt`、去掉本机路径的命令参数、请求消息和执行元数据。退出失败、轮次失败、观察到工具活动、缺少用量、出现多个无法区分的最终消息或返回后发现 token 超额，均记为未解决。超时保留部分输出。之后另做严格 JSON 解析，CLI 正常结束本身不等于有效评审。`skip_host_skill_discovery` 仍是开发中的 CLI 功能，其警告会保留；新冻结前检查已安装版本，升级后的失败也须留存。

隔离是受控的执行配置，不能证明模型训练中从未见过材料，也不能验证不可见的服务行为。CLI 事件**不认证实际返回的模型名称**，元数据只记录 `model_requested`，`model_returned` 为 `null`。CLI 的输出 token 上限是**返回后的检查**，不是生成或计费硬上限；本地超时也不证明远端已取消。该适配器用于明确限制范围的开发诊断，结果须同时披露这些限制。

## 校准

```powershell
$env:RESEARCH_CODEX_EXECUTABLE = 'C:\path\to\codex.exe'
python scripts/run_judge_calibration.py prepare --settings evals/configs/development-20261012/astra-judge.json --seed 2026101201 --output evals/runs/new-calibration
python scripts/run_judge_calibration.py execute --output evals/runs/new-calibration
```

`prepare` 不调用模型，先核验四题族对照，冻结 12 份输入、指令、设置、随机顺序及执行代码哈希。`execute` 只接纳全新且未变更的运行，最多 12 次首轮尝试，无重试；协调者清单和预期标签不进入评审请求，各种顺序使用独立上下文。全部首轮输出及失败锁定后才解码偏好匹配。结果先记为 `source_adjudication: pending`：标签一致还不够，须另行对照原始来源核查引文、解释、互换结果和有效平局。

## 提供商思考模式

HTTP schema 2 设置可选 `thinking: enabled|disabled`；开启思考时还可设 `reasoning_effort: low|high|max`。它们显式进入 API 请求，两组作者参数相同；省略则保留提供商默认值。冻结前核实具体模型支持，通用 API 参数说明不保证每个模型都允许关闭思考。10 月 12 日 GLM-5.3 首次接入拒绝关闭思考，另行记录的 enabled／low 补测接通；不能用自动回退隐藏这种失败。

2026-10-12 核对的来源：[Codex 非交互执行](https://learn.chatgpt.com/docs/non-interactive-mode)、[Codex 配置](https://learn.chatgpt.com/docs/config-file/config-reference)、[官方 provider 实现](https://github.com/openai/codex/blob/main/codex-rs/model-provider-info/src/lib.rs)、[DeepSeek API](https://api-docs.deepseek.com/api/create-chat-completion/)、[Kimi K2.6](https://platform.kimi.com/docs/guide/kimi-k2-6-quickstart)、[GLM 对话 API](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E5%AF%B9%E8%AF%9D%E8%A1%A5%E5%85%A8)、[LongCat API](https://longcat.chat/platform/docs/api/chat.html)。实际行为是带日期的证据，不是永久的模型保证。
