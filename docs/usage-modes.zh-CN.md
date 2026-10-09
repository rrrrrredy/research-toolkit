# 使用与接入

[English](usage-modes.md) | [简体中文](usage-modes.zh-CN.md)

**通过仓库链接、文件、附件或粘贴文本使用研究方法。** 按 Agent 支持的输入方式使用；原生 Skill、插件和 MCP 是宿主的独立能力。

## 使用研究方法

- **仓库链接：**将[研究请求](../README.zh-CN.md#使用)交给能读取 GitHub 的 Agent。
- **文件或附件：**下载仓库，提供 `SKILL.md`，并按任务需要提供参考文件。
- **粘贴文本：**粘贴完整入口指令与所需方法章节。见[纯聊天使用边界](../agents/README.zh-CN.md#只能在聊天中使用时)。
- **原生 Skill：**通过宿主支持的技能机制安装完整工具箱。见[Agent 接入](../agents/README.zh-CN.md)。

读取和使用研究方法，无须安装 Python 或 Codex。检索与文件访问由撰写 Agent 提供；独立审阅需要另一个评审者，仅提供指令不会自动执行审阅。

## 可选执行工具

宿主能启动本地进程时，可接入 MCP；同时支持该插件格式时，也可安装包含方法与工具的插件。两种方式使用同一套研究规范。

| 形式 | 提供什么 | 宿主要求 |
| --- | --- | --- |
| Skill | 入口指令与详细研究方法 | 原生技能发现或明确读取文件 |
| 插件 | Skill、参考文件和本地 MCP 服务，一次安装 | 支持该软件包格式与本地 stdio MCP |
| MCP | 初始化、保存进度、加载方法、审阅和检查交付的五个工具 | 能启动并调用本地 stdio MCP 服务 |

本地工具需要 Python 3.10+ 和 MCP 依赖；自动审阅还需要审阅执行器及模型账户。默认执行器使用 Codex CLI，撰写 Agent 可以是任何支持相应 MCP 的客户端，也可[配置其他审阅命令](#更换评审模型)。

## 安装插件

[插件目录](../plugins/research-toolkit/)同时提供通用插件清单和 Codex 兼容清单。当前通过仓库分发本地插件，不提供托管服务，也不表示已经上架公共插件目录。

以 Codex 为例，先安装 Python 3.10 及以上版本、Git 和新版 Codex CLI，然后运行：

```bash
python -m pip install mcp==2.2.0
codex plugin marketplace add rrrrrredy/research-toolkit
codex plugin add research-toolkit@research-toolkit
```

插件通过 `python` 启动 MCP，该 Python 环境必须装有依赖。重开会话，选择 Research Toolkit，确认能看到 `research_start`、`research_status`、`research_guide`、`research_review`、`research_finish` 五个工具。启动失败时，先检查客户端实际使用的 Python 路径与依赖。

随后直接提出研究需求，例如：

> 用研究工具箱，为企业 IT 采购团队比较三款知识检索产品，覆盖权限、部署、价格和采用风险。输出中文比较报告，给出选择建议与来源。先澄清缺失需求、确认提纲，再搜集资料。

Agent 从对话中整理需求，只追问缺失的关键条件。维护流程记录、执行评审、处理失败和检查交付由 Agent 与工具承担。

通用清单遵循[插件规范](https://developers.openai.com/plugins/build/plugins)。其他客户端须实际支持该格式和本地 stdio MCP，不能据此推断任意插件平台都兼容。单独接入 MCP 可以复用执行逻辑，无需为每个平台重写一套研究流程。

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
| `research_start` | 初始化记录，列出关键需求缺项，并检查评审配置、执行程序与默认 CLI 登录状态 |
| `research_status` | 返回进度和阶段规范；推进到分析、写作前检查来源与主张记录 |
| `research_guide` | 不创建任务，直接读取某阶段的方法，支持中英文 |
| `research_review` | 绑定完整输入并启动内容评审，保留回复与失败；只执行配置中声明的额外审计 |
| `research_finish` | 核对已评审正文、当前证据、未完成要求和交付文字；通过后才写入完成状态与回执 |

检索、阅读、分析、写作仍由撰写 Agent 使用其已有工具完成。Agent 需要把必要的来源全文、来源表和主张表写入任务目录。按阶段加载规范可以减少反复读取，但不证明模型已遵守每条要求。

进入分析前，来源须有编号、标题、定位信息和类型，至少一条来源还须记录全文或相关章节的阅读范围与阅读凭据。进入写作前，主张须有正文和类型，来源引用必须对应已登记、已记录阅读的来源。明确标为假设且说明不确定性的内容可以暂缺支持，但整体至少要有一条有来源支持的主张。阅读凭据若指向本地文件，文件须位于任务目录内、实际存在且内容非空，支持附带锚点和页码、章节说明。网址及章节、页码定位仍可使用，但不会因此自动完成内容核查。这些检查识别空记录与无效关联，不证明模型真正理解了材料。

评审会自动纳入非空的 `state/requirements.jsonl`，评审者和审查者都能看到完整需求台账，包括后续澄清与变更。评审后更改或删除该台账会阻止交付，须先处理发生变化的任务。空台账不增加需求。

评审输入包含完整任务、正文与来源文件，不能只给网址。本地输入上限为 16 MiB，超限会拒绝，不会静默截断；这也不意味着所选模型一定能够接受这么长的上下文。

### 评审使用什么账户，失败怎么办

启动任务时，`review_readiness` 会提前报告配置错误、执行程序缺失和默认 Codex CLI 登录检查失败。存在这些阻塞时，`ready_for_collection` 为 `false`；Agent 处理后重新调用 start，研究需求的关键缺项仍需澄清。检查不发送模型请求，也不证明模型可用、额度充足或后续服务一直可访问。自定义命令只检查执行程序，返回 `access_unverified`，由 Agent 在实际执行环境核对其访问能力；不会为了探测登录而擅自执行任意自定义命令。

默认执行器使用已经安装、登录的 **Codex CLI** 及其配置的模型，在一个非作者新上下文中完成内容评审。普通报告不默认启动另一个审查者，也不要求正式抽查记录。评测和已保存的审计计划继续履行原要求。

**评审会把任务、报告和证据发送到所配置的模型服务，并消耗对应账户额度。** 包内没有凭据，也不附送模型服务。使用获得材料处理授权的账户；撰写 Agent 能使用模型，不代表评审子进程自动取得同一账户的访问能力。如果 Codex 宿主使用自定义 `CODEX_HOME`，在其 stdio MCP 服务配置中加入 `env_vars = ["CODEX_HOME"]`，传递现有环境变量；否则子进程可能使用另一个默认配置及登录。其他客户端通过各自支持的设置传递实际所需环境，不要把凭据文件复制到插件或研究任务中。遇到 401 或令牌刷新失败时，先恢复评审进程实际环境中的访问，再继续原任务。

每路都须取得有具体依据、绑定当前版本、保留执行证据的完整回复。调用过、错误记录或空泛 PASS 均不算完成。每次调用中每个席位最多尝试两次，失败保留后恢复缺失工作；有效负评不重跑。显式配置审查者时，审查也须完成，恢复时只补缺失审查。

有效负面评审已经完成。`reviews_complete` 表示评审有效完成，`completion_check` 另行判断是否符合该任务的交付用途。评测使用 `purpose: "evaluation"`，保留原报告和缺陷，以 `evaluation_complete` 为终点。面向读者交付的报告确需修订时，才单独明确授权 `report_delivery` 修订。工具不会为改善评测结果自动改稿。

明确授权的报告交付变更可以移除或改名必需评审席位。使用 `revision: true` 时，执行器保留带哈希的前后计划，并追加 `review_plan_change` 记录。完成检查按当前计划进行；合法历史尝试留在日志中，不占用新席位。没有匹配历史依据的未知席位仍会失败。冻结评测不能移除或改名必需评审，负面结果也不能成为删除席位的理由。

客户端须为评审设置足够的工具调用时间。如果非交互客户端返回 `MCP tool call requires approval, but approval policy is never`，该次流程工具尚未执行。通过客户端支持的工具策略，仅为已授权任务批准必要的 Toolkit 工具，或在交互会话中批准，再继续同一任务。不要为解决工具批准问题修改全局权限或重跑模型评审。Codex 的配置见[官方 MCP 工具策略](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)。同一任务避免多个客户端或 CLI 同时写入；MCP 进程会拒绝该任务的第二个并发修改操作，但它不是分布式调度器。

### 更换评审模型

默认无需配置文件。如需指定模型或声明多路必需评审，在启动服务时，将 `RESEARCH_TOOLKIT_REVIEW_CONFIG` 指向可信的本地 JSON：

```json
{
  "reviewers": [
    {"id": "primary", "model": "codex-configured", "format": "codex-jsonl"}
  ]
}
```

需要时替换 `codex-configured`。普通报告可省略 `auditor`；需要原有独立审计时，在配置中加入 `"auditor": {"id": "audit", "model": "codex-configured", "format": "codex-jsonl"}`。评测要求审计，自定义评测配置必须提供该字段；默认配置为评测及原有审计计划保留审查者。超时范围仍为 1—1800 秒，默认 600 秒。

超时会终止该执行器的本地派生进程，并保留失败记录；这不证明供应商远端请求已取消。相同输入和配置的重复评审请求复用已有有效结果，保持已完成状态和交付回执。

评审与交付使用相同的来源、阅读和主张检查。主张引用及必读要求对应的本地材料自动加入送评；仅有网址或页码时，在来源表的 `evidence_path` 指明 UTF-8 正文或必要提取文本。二进制原件保留版本绑定，提取文本供模型阅读；原件或文本变化都会阻止使用旧评审交付。

`reviews_complete` 表示指定评审有效完成。普通报告交付要求没有未解决的必要修正。对于误报，在已有评审日志记录[有据不改](review-completion.zh-CN.md#普通报告的有据不改)，再调用 `research_finish`；原始负评保留，不为取得通过而重跑。显式审计计划继续履行额外要求。

只调整超时不改变评审任务，继续恢复缺失工作。更换模型或命令属于任务变更，须明确授权报告交付修订；只重新执行受影响的评审席位，原始回复完整保留。只更换审查者时，复用已完成的评审，仅执行新的审查。冻结评测拒绝实质性的任务变更。旧版任务在已存配置绑定仍一致时保留并复用原记录；代码升级不构成重跑有效负面评审的理由。

其他供应商可通过可信的 `command` 参数列表和 `format: "json"` 接入。命令从标准输入读取一份任务 JSON，真实调用所选模型，保留原始回复，并从标准输出返回：

```json
{"execution_id": "actual-provider-request-or-session-id", "content": "original model response text"}
```

每份任务使用新执行上下文。凭据通过供应商正常的安全配置读取，不写进仓库、研究任务、命令参数或回复。命令只从可信的启动配置读取，不接受模型在 MCP 调用参数中临时提供命令。适配器的自述不能独立证明供应商执行情况，应保留原执行证据。

## 只用 Skill，或使用 CLI

只用 Skill 时，查看[安装指南](../agents/README.zh-CN.md)。Agent 用自己的能力执行研究规范；单独安装指令文件不会启动 MCP 或自动完成评审。

插件另带不依赖 MCP SDK 的命令行入口，调用同一套逻辑：

```bash
python scripts/research_workflow.py start --workspace /path/to/tasks --request brief.json
python scripts/research_workflow.py review --workspace /path/to/tasks --request review.json
```

需求请求的格式为 `{"task":"comparison","language":"zh","brief":{"question":"...","audience":"...","scope":"...","output":"...","depth":"...","evidence_standard":"..."}}`。评审参数包括 `task`、任务内相对路径 `evidence_paths`，以及可选的 `artifact`（默认 `final.md`）和 `purpose`。`status`、`guide`、`finish` 对应同名 MCP 工具的参数。也可通过标准输入提供 JSON。

## 已验证的范围

仓库检查共用流程、插件与源码一致性，以及通过真实 stdio 连接、使用**合成评审子进程**的 MCP 调用链。这些检查不调用付费模型，也不证明报告质量。正常使用时会启动真实配置的模型执行器；安装或测试通过，不代表某份研究已经完成模型评审。

另有一次[插件 `0.1.2` 的真实模型引导验证](evaluation-status.zh-CN.md#当前实现)：在一份虚构任务上完成评审与审查恢复，保留负面结果，并正确拦截交付。该次验证需要修正配置和审查输出契约，不证明无人干预运行可靠。

工具能约束自身的完成条件，不能阻止 Agent 绕过工具或在外部修改文件，也不能用机械检查证明事实正确。内容审查与原始证据仍是验收的一部分。
