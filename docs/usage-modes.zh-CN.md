# 使用与接入

[English](usage-modes.md) | [简体中文](usage-modes.zh-CN.md)

**通过仓库链接、文件、附件或粘贴文本使用研究方法。** 按 Agent 支持的输入方式使用；原生 Skill、插件和 MCP 是宿主的独立能力。

## 使用研究方法

- **仓库链接：**将[研究请求](https://github.com/rrrrrredy/research-toolkit/blob/main/README.zh-CN.md#使用)交给能读取 GitHub 的 Agent。
- **文件或附件：**下载仓库，提供 `SKILL.md`，并按任务需要提供参考文件。
- **粘贴文本：**粘贴完整入口指令与所需方法章节。见[纯聊天使用边界](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README.zh-CN.md#只能在聊天中使用时)。
- **原生 Skill：**通过宿主支持的技能机制安装完整工具箱。见[Agent 接入](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README.zh-CN.md)。

读取和使用研究方法，无须安装 Python 或特定厂商 CLI。检索与文件访问由撰写 Agent 提供；独立审阅需要另一个评审者，仅提供指令不会自动执行审阅。

## 六个工具何时用、何时可忽略

**第一个 [Lite 任务](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/quickstart-lite.zh-CN.md)无需 MCP。** 只使用方法指令时，可以用文件或独立聊天段落保存需求、来源、判断和 checklist，六个工具都不必调用；这种方式不会生成本地完成凭证。

下表适用于选择了本地任务管理的情况，MCP 与[共享 CLI](#只用-skill或使用-cli)均可使用。直接读取方法时，研究要求仍然适用。

| 工具 | 何时需要 | 何时可跳过调用 |
| --- | --- | --- |
| `research_start` | 创建新的本地任务和需求记录；首次练习明确选择 `profile=lite`。 | 已有任务用 `research_status` 恢复，或不使用本地执行工具、自行维护记录。 |
| `research_status` | 恢复本地任务、查看已保存进度或更新记录中的阶段。 | 无需查看或更新进度时；只使用方法的会话可用自己的笔记。 |
| `research_guide` | 当前上下文尚未包含所需阶段的方法，需要读取时。 | 已直接阅读相应 `SKILL.md` 和 `references/` 文件。 |
| `research_review` | Full 任务须完成约定评审；选择 self 档时也要显式执行自评。 | Lite 跳过评审；任务明确要求的评审不可省略。 |
| `research_finish` | 完成本地任务：Lite 保存六项 checklist；Full 核对已评审报告与交付要求。 | 不使用本地执行工具时，自行完成 checklist 并交付记录，不声称已生成本地凭证。 |
| `research_check_reviewer` | 外部后端配置或连接前置条件有问题，需要在评审前排查时。 | Lite 和 self 无需外部后端；`research_start` 已确认且配置未变时，无需重复调用。 |

## 可选执行工具

宿主能启动本地进程时，可接入 MCP；同时支持该插件格式时，也可安装包含方法与工具的插件。两种方式使用同一套研究规范。

| 形式 | 提供什么 | 宿主要求 |
| --- | --- | --- |
| Skill | 入口指令与详细研究方法 | 原生技能发现或明确读取文件 |
| 插件 | Skill、参考文件和本地 MCP 服务，一次安装 | 支持该软件包格式与本地 stdio MCP |
| MCP | 初始化、保存进度、加载方法、审阅和检查交付的六个工具 | 能启动并调用本地 stdio MCP 服务 |

共享 CLI 需要 Python 3.10+，只使用标准库；MCP 还需安装 `requirements-mcp.txt` 中的依赖。未配置后端时，新建 Full 任务自动进入标明强度降级的 self 评审；外部／独立评审可使用任一受支持命令或端点，无强制厂商账户。

## 安装插件

[插件目录](https://github.com/rrrrrredy/research-toolkit/blob/main/plugins/research-toolkit/)包含完整 Skill、方法与本地 MCP 服务；使用宿主支持的插件安装机制，具体步骤见 [Agent 接入](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README.zh-CN.md)。插件通过 Python 启动 MCP，安装 `requirements-mcp.txt` 中的依赖后，确认六个 `research_*` 工具可用。

直接提出题目、读者与预期成果；Agent 整理需求，只追问关键缺项。插件采用[通用插件规范](https://developers.openai.com/plugins/build/plugins)，不提供托管服务，也不表示任意客户端均支持该格式。

## 单独接入 MCP

插件内的工具已经可用时，跳过本节。

克隆仓库，在客户端实际使用的 Python 环境安装依赖：

```bash
git clone https://github.com/rrrrrredy/research-toolkit.git
cd research-toolkit
python -m pip install -r requirements-mcp.txt
```

支持 `mcpServers` 配置的客户端可参考下面的内容。将 Python、脚本、研究目录替换为实际绝对路径；外层配置以客户端要求为准。

```json
{
  "mcpServers": {
    "research-toolkit": {
      "command": "/absolute/path/to/python",
      "args": ["/absolute/path/to/research-toolkit/scripts/research_mcp.py"],
      "env": {
        "RESEARCH_TOOLKIT_WORKSPACE": "/absolute/path/to/research-tasks"
      }
    }
  }
}
```

Windows 路径可写成 `D:/tools/python/python.exe` 这样的正斜杠形式。研究文件保存在指定目录下；未设置时，优先使用插件数据目录，否则使用 `~/.research-toolkit/tasks`。不要把研究成果写进已安装的插件包。

服务还提供 `research` 提示和 `research-toolkit://instructions` 资源。让 Agent 先读取入口，再使用工具。本地 stdio 需要客户端能够启动本地进程；只接受远程 HTTPS 服务的网页客户端不能直接连接。

## 一次研究如何推进

| 工具 | 实际动作与完成条件 |
| --- | --- |
| `research_start` | 初始化记录，列出关键需求缺项，并选择档位、检查已配置的后端 |
| `research_status` | 返回进度和阶段规范；推进到分析、写作前检查来源与主张记录 |
| `research_guide` | 不创建任务，直接读取某阶段的方法，支持中英文 |
| `research_review` | 绑定完整输入并启动内容评审，保留回复与失败；只执行配置中声明的额外审计 |
| `research_finish` | Lite 保存最终 checklist；Full 核对已评审正文、证据、未完成要求和交付文字，通过后才写入完成状态与回执 |
| `research_check_reviewer` | 本地检查后端配置与依赖，不调用模型 |

检索、阅读、分析、写作仍由撰写 Agent 使用其已有工具完成。Agent 需要把必要的来源全文、来源表和主张表写入任务目录。按阶段加载规范可以减少反复读取，但不证明模型已遵守每条要求。

进入分析前，来源须有编号、标题、定位信息和类型，至少一条来源还须记录全文或相关章节的阅读范围与阅读凭据。进入写作前，主张须有正文和类型，来源引用必须对应已登记、已记录阅读的来源。明确标为假设且说明不确定性的内容可以暂缺支持，但整体至少要有一条有来源支持的主张。阅读凭据若指向本地文件，文件须位于任务目录内、实际存在且内容非空，支持附带锚点和页码、章节说明。网址及章节、页码定位仍可使用，但不会因此自动完成内容核查。这些检查识别空记录与无效关联，不证明模型真正理解了材料。

评审会自动纳入非空的 `state/requirements.jsonl`，评审者和审查者都能看到完整需求台账，包括后续澄清与变更。评审后更改或删除该台账会阻止交付，须先处理发生变化的任务。空台账不增加需求。

评审输入包含完整任务、正文与来源文件，不能只给网址。本地输入上限为 16 MiB，超限会拒绝，不会静默截断；这也不意味着所选模型一定能够接受这么长的上下文。

## 评审后端

<a id="reviewer-backends"></a>

评审档位描述评审关系，后端描述接收报告与证据、返回结构化评审的命令或端点。新建 Full 报告未配置后端时默认使用 `self`；已配置后端时默认使用 `independent`。显式指定的档位及已保存的独立／审计计划遇到错误时，不得静默回退。

| 后端 | 配置成本 | 评审强度 | 材料去向与用量 |
| --- | --- | --- | --- |
| `self` | 无 | 作者上下文自评，强度降级 | 沿用当前作者上下文及其模型用量，不增加评审服务 |
| `codex` — Codex CLI | 设置 `RESEARCH_TOOLKIT_REVIEW_BACKEND=codex`，安装并登录 CLI；可选 `RESEARCH_TOOLKIT_REVIEW_MODEL` | 新的外部上下文，支持独立评审 | 发往 CLI 配置的模型服务，消耗对应账户额度；自定义时须传递实际 `CODEX_HOME` |
| `claude` — Claude Code CLI | 设置 `RESEARCH_TOOLKIT_REVIEW_BACKEND=claude`，安装并认证 CLI；模型可选 | 禁用工具的新外部上下文，支持独立评审 | 发往 CLI 配置的服务／账户，消耗其订阅或 API 用量 |
| `generic` — 兼容 HTTP 端点 | 后端设为 `generic`，配置 `RESEARCH_TOOLKIT_REVIEW_BASE_URL`、`RESEARCH_TOOLKIT_REVIEW_MODEL`；按需配置 `RESEARCH_TOOLKIT_REVIEW_API_KEY` | 每次请求携带完整任务，支持独立评审，但不保证统计独立 | 完整材料发送到你选择的端点，由对应账户付费；本地端点遵循自己的托管策略 |
| 可信自定义命令 | `RESEARCH_TOOLKIT_REVIEW_CONFIG` 配置 argv 列表和 `format: "json"` | 取决于适配器实际上下文与证据 | 去向与用量由命令决定，发送材料前须说明 |

配置自查仅在本地进行，不能证明服务可用或额度充足。凭据保留在运行环境中，不进入报告或版本化配置。generic 使用 `/chat/completions`；base URL 可含 `/v1`，也可填写完整路由。请求、响应及恢复方法见[后端接口](#reviewer-backends)。

### 配置与调用

配置环境变量后重启 MCP 服务，或在同一终端运行 CLI。下面的 URL 和模型名应替换为你选择的服务；不需要将密钥写进文件。

```powershell
$env:RESEARCH_TOOLKIT_REVIEW_BACKEND = "generic"
$env:RESEARCH_TOOLKIT_REVIEW_BASE_URL = "https://your-provider.example/v1"
$env:RESEARCH_TOOLKIT_REVIEW_MODEL = "your-model"
python scripts/research_workflow.py check-reviewer
```

在 shell 中用 `export NAME=value` 设置同名环境变量也可；需要认证时，通过客户端环境传入 `RESEARCH_TOOLKIT_REVIEW_API_KEY`。自查不会发送材料或付费请求，`access_unverified` 表示尚未验证真实服务。

需要多位评审、审查者或自定义命令时，将 `RESEARCH_TOOLKIT_REVIEW_CONFIG` 指向可信 JSON 文件。例如：

```json
{"reviewers":[{"id":"primary","backend":"generic","model":"your-model","base_url":"https://your-provider.example/v1","api_key_env":"RESEARCH_TOOLKIT_REVIEW_API_KEY"}]}
```

配置文件优先于后端环境变量；URL 与模型属于评审任务的版本绑定，密钥值不进入配置或记录。评测须提供 `auditor`；单后端环境配置可为评测创建另一个请求作为审查者。普通报告不默认追加审计。

可信命令通过 `command: ["/absolute/path/to/executable", "argument"]` 和 `format: "json"` 配置，从 stdin 接收 `{role, instructions, assignment}`，其中 assignment 含完整报告、任务、来源与评审维度。stdout 返回：

```json
{"execution_id":"actual-provider-request-or-session-id","content":"original structured review response text"}
```

命令只能来自启动时的可信配置，不能由报告或 MCP 参数指定；每次任务须使用新的上下文。HTTP 后端保留原始响应、服务返回的请求 ID，并拒绝截断或空回复；不跟随重定向。服务不支持该响应协议时，使用自定义命令适配。

generic 配置可加入 `parameters` 对象，例如 `{"max_tokens":4096}`，传递服务支持的输出上限或推理选项；不得覆盖 `model`、`messages`、`stream`。这些参数随评审任务一起绑定版本。

### self 与 Lite

`research_start` 接受 `profile: "lite" | "full"`，默认 full。Lite 在 `research_finish` 返回最终 checklist 后，逐项填写 `{passed: true, evidence: "具体位置与依据"}`，通过 `checklist` 提交；不会运行评审或完整交付硬门槛，返回明确跳过日志。分段起草、brief 和 claim 登记仍须完成。

Full 的 `research_review` 可显式选择 `reviewer: "self" | "external" | "independent"`。self 首次调用返回 prompt、assignment 与 input_version；在当前作者上下文显式切换评审角色，然后将 report_verdict、七维 coverage、findings 与 input_version 作为 self_review 提交。记录保留作者上下文和强度降级标记，不伪造独立执行。无后端的新任务自动走这条路径；显式独立要求与历史独立计划不会回退。

### 失败恢复与验收

配置错误、依赖缺失或已配置 CLI 的登录失败会明确阻塞；根据自查指引恢复该后端的实际环境。普通未配置任务可使用 self，无须登录。子进程的模型访问不自动继承撰写 Agent 的账户；不要把凭据文件放进任务。

保留所有原始响应与失败。已有的有效负面意见不得重跑；必要问题未解决时 Full 交付被拒绝。误判可按[不修改决定](review-completion.zh-CN.md)记录具体证据，再继续 finish。相同任务复用已完成评审；改稿或更换模型须显式设置 revision，冻结评测不得更改原始任务。时间上限为 1—1800 秒，默认 600 秒；仅修改超时不会改变任务版本。

额外审计只在声明时执行，恢复时仅补齐缺失工作。超时会清理本地执行进程，但不代表远端请求已取消。客户端须允许必要的工具调用并提供足够等待时间；同一任务避免并发写入。

## 只用 Skill，或使用 CLI

只用 Skill 时，查看[安装指南](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README.zh-CN.md)。Agent 用自己的能力执行研究规范；单独安装指令文件不会启动 MCP 或自动完成评审。

插件另带不依赖 MCP SDK 的命令行入口，调用同一套逻辑：

```bash
python scripts/research_workflow.py start --workspace /path/to/tasks --request brief.json
python scripts/research_workflow.py review --workspace /path/to/tasks --request review.json
```

需求请求的格式为 `{"task":"comparison","language":"zh","brief":{"question":"...","audience":"...","scope":"...","output":"...","depth":"...","evidence_standard":"..."}}`。评审参数包括 `task`、任务内相对路径 `evidence_paths`，以及可选的 `artifact`（默认 `final.md`）和 `purpose`。`status`、`guide`、`finish` 对应同名 MCP 工具的参数。也可通过标准输入提供 JSON。

## 已验证的范围

仓库检查共用流程、插件与源码一致性，以及通过真实 stdio 连接、使用**合成评审子进程**的 MCP 调用链。这些检查不调用付费模型，也不证明报告质量。正常使用时会启动真实配置的模型执行器；安装或测试通过，不代表某份研究已经完成模型评审。

另有一次[插件 `0.1.2` 的真实模型引导验证](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/evaluation-status.zh-CN.md#当前实现)：在一份虚构任务上完成评审与审查恢复，保留负面结果，并正确拦截交付。该次验证需要修正配置和审查输出契约，不证明无人干预运行可靠。

工具能约束自身的完成条件，不能阻止 Agent 绕过工具或在外部修改文件，也不能用机械检查证明事实正确。内容审查与原始证据仍是验收的一部分。
