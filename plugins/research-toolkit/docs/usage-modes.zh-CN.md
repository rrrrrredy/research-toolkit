# 使用与接入

[English](usage-modes.md) | [简体中文](usage-modes.zh-CN.md)

[1.x 兼容性约定](compatibility.zh-CN.md)覆盖公开工具、已有任务和安装要求。从 v0.2.7 升级到 v1.0.0 无需迁移任务数据。

**通过仓库链接、文件、附件或粘贴文本使用研究方法。** 按 Agent 支持的输入方式使用；原生 Skill、插件和 MCP 是宿主的独立能力。

## 使用研究方法

- **仓库链接：**将[研究请求](https://github.com/rrrrrredy/research-toolkit/blob/main/README.zh-CN.md#使用)交给能读取 GitHub 的 Agent。
- **文件或附件：**下载仓库，提供 `SKILL.md`，并按任务需要提供参考文件。
- **粘贴文本：**粘贴完整入口指令与所需方法章节。见[纯聊天使用边界](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README.zh-CN.md#只能在聊天中使用时)。
- **原生 Skill：**通过宿主支持的技能机制安装完整工具箱。见[Agent 接入](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README.zh-CN.md)。

读取和使用研究方法，无须安装 Python 或特定厂商 CLI。检索与文件访问由撰写 Agent 提供；独立审阅需要另一个评审者，仅提供指令不会自动执行审阅。

## 八个工具何时用、何时可忽略

**按任务选择 [Lite](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/quickstart-lite.zh-CN.md) 或 [Full](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/quickstart-full.zh-CN.md)。** 两者共用研究底线，Agent 维护记录。Lite 完成作者自检；Full 增加所选评审、修订核对和交付一致性检查。可直接读方法，CLI/MCP 按需接入。

下表适用于选择了本地任务管理的情况，MCP 与[共享 CLI](#只用-skill或使用-cli)均可使用。直接读取方法时，研究要求仍然适用。

| 工具 | 何时需要 | 何时可跳过调用 |
| --- | --- | --- |
| `research_start` | 创建新的本地任务和需求记录；按用途、版本化评审和修订需要显式选择 `lite` 或 `full`。 | 已有任务用 `research_status` 恢复，或不使用本地执行工具、自行维护记录。 |
| `research_save` | 保存／更新来源、主张、要求与稿件，由 Agent 处理定位到的格式错误。 | 记录与稿件均无变化。 |
| `research_status` | 恢复本地任务、查看已保存进度或更新记录中的阶段。 | 无需查看或更新进度时；只使用方法的会话可用自己的笔记。 |
| `research_guide` | 当前上下文尚未包含所需阶段的方法，需要读取时。 | 已直接阅读相应 `SKILL.md` 和 `references/` 文件。 |
| `research_review` | Full 任务须完成约定评审；选择 self 档时也要显式执行自评。 | Lite 跳过评审；任务明确要求的评审不可省略。 |
| `research_check_draft` | 无模型调用地检查当前稿件记录与显式篇幅，不生成交付凭证。 | 评审／交付前可选；来源与含义仍需单独核对。 |
| `research_finish` | 完成本地任务：Lite 保存六项 checklist；Full 核对已评审报告与交付要求。 | 不使用本地执行工具时，自行完成 checklist 并交付记录，不声称已生成本地凭证。 |
| `research_check_reviewer` | 外部后端配置或连接前置条件有问题，需要在评审前排查时。 | Lite 和 self 无需外部后端；`research_start` 已确认且配置未变时，无需重复调用。 |

## 保存研究记录与稿件

Agent 使用 `research_save`（CLI：`save`）提交来源、主张和要求对象。用户描述研究需求、决定范围和用途，不管理 CSV、编号或评审返回 JSON。工具按 ID 合并局部更新，保留其他行和字段，写入既有 CSV／JSONL 格式。省略 ID 时，按唯一网址／主张／要求摘要匹配已有记录，否则分配 ID 并返回；后续修改使用返回的 ID。来源仍由 Agent 实际阅读并准确整理。

以下是给 Agent 的调用示例，来源正文已保存在任务目录：

```json
{
  "task": "example",
  "sources": [{"title":"来源标题","url":"https://example.org/source","source_type":"primary","read_scope":"relevant_sections","read_evidence":"sources/source.md"}],
  "claims": [{"claim":"有来源支持的判断","claim_type":"fact","supporting_sources":["S1"]}],
  "requirements": [{"summary":"解释比较结果","status":"pending"}],
  "draft": {"path":"first-draft.md","complete":true}
}
```

未变化的集合不传。`draft` 可带 `content`，由工具写稿并创建父目录；省略 content 时登记已有 UTF-8 文件，无需把全文再搬进对话。`complete: true` 表示 Agent 已保存完整稿，不表示质量通过。局部更新如 `{"requirements":[{"requirement_id":"R1","status":"satisfied","evidence":"final.md，比较章节"}]}` 会保留其他字段；工具不编造证据，也不自动关闭要求。

```bash
python3 scripts/research_workflow.py save --workspace ../research-work --request save.json
```

格式错误定位到集合、行和字段，由 Agent 修正调用后重试；整批输入验证通过后才替换记录。已有集合格式损坏时，提交恢复后的完整行，并显式指定如 `"replace":["sources"]`；工具将原始字节备份到 `logs/record-backups/`，不会悄悄丢弃无法解析的行。保存后的输入变化仍按原规则使旧检查失效。

显式调用 `research_status(task, stage="analyze")` 或 `stage="draft"` 时，返回的 `requirements` 包含已保存的补充要求原文（JSONL），保留状态和处理依据，Agent 可直接用于分析与起草，无需再复制进 brief。没有补充要求时省略该字段；普通状态查询不附加正文。返回要求不表示要求已满足，仍需按其内容完成研究。

`research_status` 的 `activity` 汇总任务开始时间、首次观察到的完整稿 UTC 时间／哈希及距创建任务的耗时、保存失败、实际评审尝试／重试、调用耗时及返回用量。`saved_by_tool` 表示工具保存时间；`existing_file_observed` 表示登记时间，不冒充旧文件创建时间。只读状态／草稿／交付检查不追加日志；复用评审不算新调用，作者上下文自评提交单独计数。缓存 token 不重复计入输入总量，缺失用量为未知。工具看不到宿主作者的全程 token、账单或登记前耗时。这些观察不增加交付要求，也不等于首次可用结果时间或研究质量判定。

`save` 与 `status` 的 `changes` 给出最近一次成功保存记录的批次：新增、更新、未变、删除或格式恢复的 ID，关联主张，以及最近登记稿件中的行号／标题。位置来自主张原文或来源链接的字面匹配，可能指向引用段或资料表；`not_located` 表示需自行定位，不等于没有影响。Agent 根据提示读取相关段落，核对来源后决定改哪些结论；不自动认定主张失效。

每个命中位置还返回 `text`（命中行原文）和 `context`，后者包含 `start_line`、`end_line` 与原文 `text`：命中段落及同一章节内前后至多各一段。按空行分段，以 `#` 标题为边界；行号从 1 开始，包含起止行。已登记版本日志查询使用同一份定位输出，无需新增输入字段或调用，也不修改报告。

已有来源正文改动后，保存该来源 ID（如 `{"sources":[{"source_id":"S1"}]}`）即可比较本地证据文件与上次保存时的哈希，不必重交其他字段。首次观察会明确标记，不能据此推断更早是否变化；旧任务无需迁移或补建历史。工具不会监控远端网页。内容字节相同的文件不重写，`updated_files` 只列实际写入；状态查询不写文件。只登记新稿会沿用最近记录批次并更新正文位置，下一批记录保存会替换该摘要；它不是待办清单，也不新增完成条件。

### 按需检查已登记的版本日志

`research_check_updates(task, source_id)`（CLI：`check-updates`）读取一个已登记的公开版本日志，对比已保存的最新日期条目及其后的版本，返回新增／修订内容、来源标注日期，以及现有主张和稿件的关联位置。无变化返回 `status: unchanged` 后结束；网络、读取、格式或对照失败返回 `status: failed`、`phase` 和原因，CLI 退出码为1。

```json
{"task":"alibaba-20261016","source_id":"S3"}
```

```bash
python3 scripts/research_workflow.py check-updates --workspace ../research-work --request check-updates.json
```

来源的 `source_type` 使用已有的 `official_release`，或 `release_notes`／`changelog`；`url` 是公开 HTTPS 日志地址，`evidence_path`（或可解析的 `read_evidence`）指向任务内已保存的 UTF-8 日志正文。只支持 HTML／纯文本／Markdown 中独占一行的 `YYYY-MM-DD` 或 `YYYY年MM月DD日`，下一非空行须含版本号，随后为条目正文；已有网页工具导出的 `L数字:` 行号会被忽略。登录页、依赖 JavaScript 才能显示的正文、其他日期格式和无可对应旧版本的页面明确报错，不当作无变化。

这是一项手动调用：每次只请求登记网址，不跟随跳转、不抓其他页面、不定时运行。仅比较最新保存日期和更新条目，不追查更早版本的修订。相同条目中的删改也会返回，日期是来源标签，不冒充精确发布时间。关联段落复用现有字面匹配；未定位时需自行检查。

调用不覆盖旧证据、不改变阅读状态、结论或交付记录。有变化时返回 `current_excerpt`，供 Agent 阅读后另存并通过现有 `research_save` 更新来源；未采纳前再次调用仍会相对旧证据报告变化。网络失败可在恢复访问后重试同一请求。

## 接续已有研究

提供已有报告、相关来源和新的用途即可，记录整理由 Agent 负责。支持从零研究，也支持以下两条路径：

```text
用 Research Toolkit 检查这份报告和相关来源，重点看会改变结论或行动的重要问题。
保留原稿，定位问题与依据，做必要的最小修订，核对修改并给我变化说明。
根据用途建议 Lite 或 Full；不为文风偏好重写整篇，不把可选建议当成必改。
```

```text
在已有研究上加入这些新资料。说明哪些事实已过期、哪些判断需要改变、哪些仍成立。
保留资料日期与版本，更新受影响的段落、来源和判断，不从头重做未受影响的研究。
交付更新稿及简短变化说明；重新完成本次改动使之失效的检查。
```

按已保存的档位接续时，先用 `research_status(task)` 读取状态并保留旧稿。沿用来源、主张和要求编号及已有阅读依据；用 `research_save` 一并更新受影响记录，按已有路径登记稿件，未变记录无需重交。实际核对要求后，将状态和具体依据随相关更新保存。重读变化或有疑问的来源段落，复用仍有效的本地证据，无需再次获取；按所选档位核对完整当前稿，再声明完成。[长报告实际更新案例](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/case-study/coding-benchmark-update/README.zh-CN.md)保留复用、来源确认的问题、返工及消耗。

### Lite 接续 Full

用户需要补正式评审或交付核对时，保留原 Lite 任务，以新 ID 创建关联的 Full 任务。Agent 从原 brief 建立新任务，在 `task_spec.md` 说明原任务位置、稿件版本及新增用途；复用报告、来源原文与阅读范围、主张和已知要求。内容不变、依据仍有效的工作无需重做；新增或受影响的要求重新核对。无需用户重填表格。

新 Full 任务使用自己的进度、评审计划和回执。不要复制 Lite 的 `progress.json`、通过标记、checklist、评审日志或收据来充当 Full 完成凭证，也不改写原 Lite 档位。旧作者检查可作为历史说明，不能冒充独立意见。

已有工具路径：`research_start(new_task, original_brief, profile="full")` → Agent 整理可复用材料 → `research_status(new_task, stage="draft")` → `research_check_draft` → `research_review` → 修订及必要复验 → `research_finish`。Full 的 self、external、independent 按任务选择；明确独立要求须实际执行，Astra 单独上下文即可。纯方法使用也按这一路径保留稿件和评审，不能声称产生本地回执。

### 内容或资料变化后

| 变化 | 复用与复验 |
| --- | --- |
| 恢复中断任务，输入未变 | 用 `research_status` 读现有状态，继续未完成工作；有效的已完成评审可复用。 |
| 报告、需求、已绑定来源／主张改变 | 更新受影响分析。旧检查不代表当前版本通过；Lite 重做相应检查并提交当前 checklist，Full 以 `revision=true` 对当前输入完成所需评审与交付核对。 |
| 来源网页有更新，但本地保存件未变 | 工具不监控远程网页。Agent 读取并保留新版本、说明日期和结论差异后，再按输入变化处理。 |

Full 的形式检查验证声明范围内的版本和记录一致性；它们不会判断新来源是否可信。`research_check_draft` 的私有聊天引用提示只扫描传入稿件、忽略代码示例，提示不改变 `ok` 或历史收据含义。引用修复须依据真实来源；具体语义仍由实际阅读和评审核对。

## 可选执行工具

宿主能启动本地进程时，可接入 MCP；同时支持该插件格式时，也可安装包含方法与工具的插件。两种方式使用同一套研究规范。

| 形式 | 提供什么 | 宿主要求 |
| --- | --- | --- |
| Skill | 入口指令与详细研究方法 | 原生技能发现或明确读取文件 |
| 插件 | Skill、参考文件和本地 MCP 服务，一次安装 | 支持该软件包格式与本地 stdio MCP |
| MCP | 初始化、保存进度、加载方法、审阅和检查交付的八个工具 | 能启动并调用本地 stdio MCP 服务 |

共享 CLI 需要 Python 3.10+，只使用标准库。Linux 上优先使用 `python3`；本机已有的 Python 3.10+ 解释器即可。MCP 还需安装 `requirements-mcp.txt` 中的依赖。未配置后端时，新建 Full 任务自动进入标明强度降级的 self 评审；外部／独立评审可使用任一受支持命令或端点，无强制厂商账户。

CI 在 Python 3.10／Linux 上检查 CLI 和打包 MCP 流程，并在 Python 3.12／Linux、Windows 上执行更完整的检查。安装依赖与客户端启动服务须使用同一解释器。这些验证覆盖服务和协议，不代表所有客户端 GUI 均已实测。

## 安装插件

[插件目录](https://github.com/rrrrrredy/research-toolkit/blob/main/plugins/research-toolkit/)包含完整 Skill、方法与本地 MCP 服务；使用宿主支持的插件安装机制，具体步骤见 [Agent 接入](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README.zh-CN.md)。插件通过 Python 启动 MCP，安装 `requirements-mcp.txt` 中的依赖后，确认八个 `research_*` 工具可用。

直接提出题目、读者与预期成果；Agent 整理需求，只追问关键缺项。插件采用[通用插件规范](https://developers.openai.com/plugins/build/plugins)，不提供托管服务，也不表示任意客户端均支持该格式。

## 单独接入 MCP

插件内的工具已经可用时，跳过本节。

克隆仓库，在客户端实际使用的 Python 环境安装依赖：

```bash
git clone https://github.com/rrrrrredy/research-toolkit.git
cd research-toolkit
```

使用 Python 3.10+，在独立虚拟环境中安装依赖。从已克隆的仓库目录执行：

**macOS / Linux**

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-mcp.txt
.venv/bin/python -c "import sys, mcp; print(sys.executable)"
```

**Windows PowerShell**

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-mcp.txt
.\.venv\Scripts\python.exe -c "import sys, mcp; print(sys.executable)"
```

Windows 没有 `py` 启动器时，第一条命令改用已安装的 Python 3.10+ 解释器。把打印出的解释器绝对路径填入 MCP 的 `command`；无需激活环境或修改 PowerShell 执行策略。Linux 若提示缺少 `venv`／`ensurepip`，先安装发行版的 venv 包（Debian/Ubuntu 通常为 `python3-venv`），再创建环境。若出现 `externally-managed-environment`，通常是安装时用了系统 Python，改用上面的 `.venv` 解释器运行 pip。见 [Python venv 文档](https://docs.python.org/3/library/venv.html)。


支持 `mcpServers` 配置的客户端可参考下面的内容。将 Python、脚本、研究目录替换为实际绝对路径；外层配置以客户端要求为准。

```json
{
  "mcpServers": {
    "research-toolkit": {
      "command": "/absolute/path/to/research-toolkit/.venv/bin/python",
      "args": ["/absolute/path/to/research-toolkit/scripts/research_mcp.py"],
      "env": {
        "RESEARCH_TOOLKIT_WORKSPACE": "/absolute/path/to/research-tasks"
      }
    }
  }
}
```

Windows 路径可写成 `D:/tools/research-toolkit/.venv/Scripts/python.exe` 这样的正斜杠形式。研究文件保存在指定目录下；未设置时，优先使用插件数据目录，否则使用 `~/.research-toolkit/tasks`。不要把研究成果写进已安装的插件包。

服务还提供 `research` 提示和 `research-toolkit://instructions` 资源。让 Agent 先读取入口，再使用工具。本地 stdio 需要客户端能够启动本地进程；只接受远程 HTTPS 服务的网页客户端不能直接连接。

### 客户端配置与示例

Claude Desktop 与 Cursor 使用上面的 JSON 配置。Codex CLI / IDE 使用原生 TOML；将等效配置加入 `~/.codex/config.toml`，三处路径均替换为实际绝对路径：

```toml
[mcp_servers.research-toolkit]
command = "/absolute/path/to/research-toolkit/.venv/bin/python"
args = ["/absolute/path/to/research-toolkit/scripts/research_mcp.py"]

[mcp_servers.research-toolkit.env]
RESEARCH_TOOLKIT_WORKSPACE = "/absolute/path/to/research-tasks"
```

重启客户端，确认能看到八个 `research_*` 工具。[可执行示例](https://github.com/rrrrrredy/research-toolkit/blob/main/examples/mcp/README.zh-CN.md)使用虚构报告与明确降级的自评，采集本地服务真实返回。

官方配置说明：[Claude Desktop 本地服务](https://modelcontextprotocol.io/docs/develop/connect-local-servers)、[Cursor MCP](https://cursor.com/docs/mcp)、[Codex MCP](https://developers.openai.com/codex/mcp)。Cursor 可使用项目 `.cursor/mcp.json` 或全局 `~/.cursor/mcp.json`，Codex 使用 `~/.codex/config.toml`；Claude Desktop 从 Settings → Developer → Edit Config 打开配置。

看不到工具时，用配置中的解释器执行 `python -c "import sys, mcp; print(sys.executable)"`。导入报错表示该环境缺少 MCP 依赖；使用脚本与工作区的绝对路径，并重启客户端。`python3 scripts/check_mcp_contract.py` 检查服务启动及协议调用，使用合成评审者，不证明各客户端 GUI 兼容性或研究质量。

## 一次研究如何推进

| 工具 | 实际动作与完成条件 |
| --- | --- |
| `research_start` | 初始化记录，列出关键需求缺项，并选择档位、检查已配置的后端 |
| `research_status` | 返回进度和阶段规范；推进到分析、写作前检查来源与主张记录 |
| `research_guide` | 不创建任务，直接读取某阶段的方法，支持中英文 |
| `research_review` | 绑定完整输入并启动内容评审，保留回复与失败；只执行配置中声明的额外审计 |
| `research_check_draft` | 返回当前计数、声明范围检查与记录错误，不改变任务状态；`ok` 不认证内容或交付 |
| `research_finish` | Lite 保存最终 checklist；Full 核对已评审正文、证据、未完成要求和交付文字，通过后才写入完成状态与回执 |
| `research_check_reviewer` | 本地检查后端配置与依赖，不调用模型 |

检索、阅读、分析、写作仍由撰写 Agent 使用其已有工具完成。Agent 需要把必要的来源全文、来源表和主张表写入任务目录。按阶段加载规范可以减少反复读取，但不证明模型已遵守每条要求。

进入分析前，来源须有编号、标题、定位信息和类型，至少一条来源还须记录全文或相关章节的阅读范围与阅读凭据。进入写作前，主张须有正文和类型，来源引用必须对应已登记、已记录阅读的来源。明确标为假设且说明不确定性的内容可以暂缺支持，但整体至少要有一条有来源支持的主张。阅读凭据若指向本地文件，文件须位于任务目录内、实际存在且内容非空，支持附带锚点和页码、章节说明。网址及章节、页码定位仍可使用，但不会因此自动完成内容核查。这些检查识别空记录与无效关联，不证明模型真正理解了材料。

评审会自动纳入非空的 `state/requirements.jsonl`，评审者和审查者都能看到完整需求台账，包括后续澄清与变更。评审后更改或删除该台账会阻止交付，须先处理发生变化的任务。空台账不增加需求。

评审输入包含完整任务、正文与来源文件，不能只给网址。本地输入上限为 16 MiB，超限会拒绝，不会静默截断；这也不意味着所选模型一定能够接受这么长的上下文。

## 评审后端

<a id="reviewer-backends"></a>

评审档位描述评审关系，后端描述接收报告与证据、返回结构化评审的命令或端点。新建 Full 报告未配置后端时默认使用 `self`；已配置后端时默认使用 `independent`。显式指定的档位及已保存的独立／审计计划遇到错误时，不得静默回退。

Astra 在与作者分开的新上下文中即可承担独立评审，作者使用相同模型也可以。评审收到同一题目、报告和来源材料；盲评时不接收作者 notes 和评测分组映射。不要求额外的外部人员、供应商或固定评审面板。既有用户任务和开发任务都是独立的真实任务，已执行测试都是真实测试；如实记录复用，不将其视为缺少任务材料。模型实际执行和参与评测同样提供用户视角：根据上下文使用、额外阅读、耗时、返工和研究结果判断收益，不以真人参与为前提；说明实际观察到的作用及其任务范围。

| 后端 | 配置成本 | 评审强度 | 材料去向与用量 |
| --- | --- | --- | --- |
| `self` | 无 | 作者上下文自评，强度降级 | 沿用当前作者上下文及其模型用量，不增加评审服务 |
| `codex` — Codex CLI | 设置 `RESEARCH_TOOLKIT_REVIEW_BACKEND=codex`，安装并登录 CLI；可选 `RESEARCH_TOOLKIT_REVIEW_MODEL` | 新的评审上下文，支持独立评审 | 发往 CLI 配置的模型服务，消耗对应账户额度；自定义时须传递实际 `CODEX_HOME` |
| `claude` — Claude Code CLI | 设置 `RESEARCH_TOOLKIT_REVIEW_BACKEND=claude`，安装并认证 CLI；模型可选 | 禁用工具的新评审上下文，支持独立评审 | 发往 CLI 配置的服务／账户，消耗其订阅或 API 用量 |
| `generic` — 兼容 HTTP 端点 | 后端设为 `generic`，配置 `RESEARCH_TOOLKIT_REVIEW_BASE_URL`、`RESEARCH_TOOLKIT_REVIEW_MODEL`；按需配置 `RESEARCH_TOOLKIT_REVIEW_API_KEY` | 每次请求携带完整任务，支持独立评审，但不保证统计独立 | 完整材料发送到你选择的端点，由对应账户付费；本地端点遵循自己的托管策略 |
| 可信自定义命令 | `RESEARCH_TOOLKIT_REVIEW_CONFIG` 配置 argv 列表和 `format: "json"` | 取决于适配器实际上下文与证据 | 去向与用量由命令决定，发送材料前须说明 |

配置自查仅在本地进行，不能证明服务可用或额度充足。凭据保留在运行环境中，不进入报告或版本化配置。generic 使用 `/chat/completions`；base URL 可含 `/v1`，也可填写完整路由。远程端点须使用 HTTPS；只有 `localhost` 或明确的回环 IP 地址（如 `127.0.0.1`、`::1`）可用 HTTP。即使没有 API key 也适用，因为请求携带报告和来源。请求、响应及恢复方法见[后端接口](#reviewer-backends)。

### 配置与调用

配置环境变量后重启 MCP 服务，或在同一终端运行 CLI。下面的 URL 和模型名应替换为你选择的服务；不需要将密钥写进文件。

```powershell
$env:RESEARCH_TOOLKIT_REVIEW_BACKEND = "generic"
$env:RESEARCH_TOOLKIT_REVIEW_BASE_URL = "https://your-provider.example/v1"
$env:RESEARCH_TOOLKIT_REVIEW_MODEL = "your-model"
python3 scripts/research_workflow.py check-reviewer
```

在 shell 中用 `export NAME=value` 设置同名环境变量也可；需要认证时，通过客户端环境传入 `RESEARCH_TOOLKIT_REVIEW_API_KEY`。自查不会发送材料或付费请求，`access_unverified` 表示尚未验证真实服务。

需要多位评审、审查者或自定义命令时，将 `RESEARCH_TOOLKIT_REVIEW_CONFIG` 指向可信 JSON 文件。例如：

```json
{"reviewers":[{"id":"primary","backend":"generic","model":"your-model","base_url":"https://your-provider.example/v1","api_key_env":"RESEARCH_TOOLKIT_REVIEW_API_KEY"}]}
```

配置文件优先于后端环境变量；URL 与模型属于评审任务的版本绑定，密钥值不进入配置或记录。新报告和新评测均使用已配置的评审者，不默认追加审计者；需要额外审计时才配置 `auditor`。恢复已保存的审计计划时保留其审计要求，单后端环境配置只在此时补出对应的独立审计请求。

可信命令通过 `command: ["/absolute/path/to/executable", "argument"]` 和 `format: "json"` 配置，从 stdin 接收 `{role, instructions, assignment}`，其中 assignment 含完整报告、任务、来源与评审维度。stdout 返回：

```json
{"execution_id":"actual-provider-request-or-session-id","content":"original structured review response text"}
```

命令只能来自启动时的可信配置，不能由报告或 MCP 参数指定；每次任务须使用新的上下文。HTTP 后端保留原始响应、服务返回的请求 ID，并拒绝截断或空回复；不跟随重定向。服务不支持该响应协议时，使用自定义命令适配。

generic 配置可加入 `parameters` 对象，例如 `{"max_tokens":4096}`，传递服务支持的输出上限或推理选项；不得覆盖 `model`、`messages`、`stream`。这些参数随评审任务一起绑定版本。

### self 与 Lite

`research_start` 接受 `profile: "lite" | "full"`，默认 full。Lite 在 `research_finish` 返回最终 checklist 后，逐项填写 `{passed: true, evidence: "具体位置与依据"}`，通过 `checklist` 提交；不会运行评审或完整交付硬门槛，返回明确跳过日志。分段起草、brief 和 claim 登记仍须完成。

新 Lite 凭证使用 `schema_version: 2` 和 `input_hashes`，在稿件及交付说明之外，绑定任务说明、来源／主张表、可选的要求记录和已读来源声明的本地文件。checklist 每项可选填 `evidence_files`，用任务相对路径绑定保留的检查说明。文件缺失、为空、越界或指向工作流输出时，在替换凭证前返回错误。文本哈希归一化换行，二进制原件按精确字节计算。检查器返回 `input_binding_scope`；历史凭证继续只检查稿件／交付说明。哈希检验输入是否变化，不证明证据解释正确，也不监测远程网页变化。

新建任务时根据需求选择并显式传入档位；已有任务用 `research_status(task)` 沿用保存的档位。单独调用 `research_guide(stage, profile="lite")` 仅返回[精简 Lite 指南](../references/lite-workflow.zh-CN.md)的共同说明和指定阶段，不加载 Full 评审或交付规范。直接读取文件的 Agent 使用同一指南。默认值仍为 Full，以兼容已有集成。

Full 的 `research_review` 可显式选择 `reviewer: "self" | "external" | "independent"`。self 首次调用返回 prompt、assignment 与 input_version；在当前作者上下文显式切换评审角色，然后将 report_verdict、七维 coverage、findings 与 input_version 作为 self_review 提交。记录保留作者上下文和强度降级标记，不伪造独立执行。无后端的新任务自动走这条路径；显式独立要求与历史独立计划不会回退。

### 失败恢复与验收

CLI、MCP 与 Python 工作流操作共用本地操作系统任务锁。同一任务的重叠操作会立即失败；等待当前操作结束后再执行。不同任务互不阻塞。空的 `.research-toolkit.lock` 文件会保留，但操作系统锁会随释放或进程退出而结束；不要删除锁文件来强行访问。这仅协调遵循协议的本地进程，不锁定外部编辑器或分布式文件系统。

评审 stderr 含无效 UTF-8 时，以替代字符显示，并在 `raw_output_base64` 保留完整原始字节。实际回复含无效 UTF-8 则以 `invalid_output_encoding` 失败并保留原件；已经执行的调用不再误记为启动失败。

配置错误、依赖缺失或已配置 CLI 的登录失败会明确阻塞；根据自查指引恢复该后端的实际环境。普通未配置任务可使用 self，无须登录。子进程的模型访问不自动继承撰写 Agent 的账户；不要把凭据文件放进任务。

保留所有原始响应与失败，不重跑同一未变版本已有的有效负面评审；必要问题未解决时 Full 交付被拒绝。误判可按[不修改决定](review-completion.zh-CN.md)记录具体证据，再继续 finish。普通报告修正后，用 `revision: true` 调用 `research_review` 评审新版本。这是正常修稿循环，已获授权的修正不需要再次向用户确认；研究范围变更应先在任务记录中处理。更换评审配置也须传入 `revision: true`，冻结评测不得更改原始任务。时间上限为 1—1800 秒，默认 600 秒；仅修改超时不会改变任务版本。

新评审计划在 `instruction_snapshot` 中保存完整的评审者与审计者指令。恢复未变更的任务时沿用该快照，不受已安装参考文档更新影响；复用已完成的有效评审，只继续未完成部分。普通报告显式传入 `revision: true` 时使用当前指令，并记录发生的任务变更；冻结评测仍拒绝改变原任务。没有快照的历史计划继续执行原有版本检查，不补造历史指令，也不静默认定升级前后等价。

`reviews_complete` 和 `review_check` 表示约定评审是否执行完成，负面评审也可算完成。`delivery_ready` 和已有的 `completion_check` 表示普通报告是否可进入交付验证，其中的计数不包含仍有报告缺陷的评审。`open_issues` 列出具体发现，并同步到进度和下一步。评审完成不等于报告通过。

保存的进度声称完成时，`research_status` 会检查当前交付输入与凭证。检查失败返回 `progress.status: stale`、`delivery_check` 和原来的 `recorded_status`；查询不重写哈希绑定的进度或历史凭证。先处理发现，再完成适用的复审／checklist 与 finish，才能宣称当前版本完成。

额外审计只在声明时执行，恢复时仅补齐缺失工作。超时会清理本地执行进程，但不代表远端请求已取消。客户端须允许必要的工具调用并提供足够等待时间；同一任务避免并发写入。

## 只用 Skill，或使用 CLI

只用 Skill 时，查看[安装指南](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README.zh-CN.md)。Agent 用自己的能力执行研究规范；单独安装指令文件不会启动 MCP 或自动完成评审。

插件另带不依赖 MCP SDK 的命令行入口，调用同一套逻辑：

```bash
python3 scripts/research_workflow.py start --workspace /path/to/tasks --request brief.json
python3 scripts/research_workflow.py review --workspace /path/to/tasks --request review.json
```

CLI 请求通过 `--request` 或标准输入提供 JSON 对象。缺参／未知字段提示会在创建或改变任务前列出操作、字段和输入方式。来源／主张校验错误指出 CSV 文件、记录编号及缺失字段；修正对应记录后重复原操作。指南语言参数为 `en` 或 `zh`。失败命令返回 JSON 和非零退出码；修复已获授权的任务不需要新增用户确认。

需求请求的格式为 `{"task":"comparison","language":"zh","brief":{"question":"...","audience":"...","scope":"...","output":"...","depth":"...","evidence_standard":"..."}}`。评审参数包括 `task`、任务内相对路径 `evidence_paths`，以及可选的 `artifact`（默认 `final.md`）和 `purpose`。`status`、`guide`、`finish` 对应同名 MCP 工具的参数。也可通过标准输入提供 JSON。

### 复用任务文件并保存自评材料

直接在已有任务目录中保存稿件、笔记和来源，向工具传入相对该目录的 `artifact` 和 `evidence_paths`，工具会读取原文件。修订前保留首稿，交付时再导出终稿，无需为每次调用另复制一套材料。

将下方任务目录改为 `start` 返回的实际位置，并在请求中使用同一任务名。以下用于已有的 Full 任务 `comparison`。准备好稿件及来源／主张记录后，将请求保存为 `review.json`，把 `source.md` 换成实际证据路径。仅在已选择 self 档位时使用此例；独立评审要求继续使用所配置的后端。

```json
{"task":"comparison","reviewer":"self","artifact":"final.md","evidence_paths":["source.md"],"include_assignment":false}
```

此本地示例返回 `prompt`、`input_version`、`task_directory` 和 `assignment_ref`（相对路径及文本 SHA-256）；完整冻结输入仍保存在任务内。调用方需要直接取得全文时，省略 `include_assignment` 或设为 `true`，默认行为及 external／independent 的输入传递不变。从仓库／插件根目录用 CLI 的同一解释器运行以下 Python 片段，保存返回内容。`start` 已创建 `logs`；首次评审前可能还没有 `reviews`，而 Shell 重定向会先于 CLI 执行打开目标文件。

```python
import subprocess
import sys
from pathlib import Path

task = Path("../research-work/comparison").resolve()
with (task / "logs/self-review-01.json").open("x", encoding="utf-8") as output:
    subprocess.run(
        [sys.executable, "scripts/research_workflow.py", "review",
         "--workspace", str(task.parent), "--request", "review.json"],
        stdout=output, check=True,
    )
```

`x` 模式会在调用评审前拒绝覆盖旧记录。确需新一次执行时使用新文件名；失败时保留已有输出和错误。相同输入的材料已经成功保存时，直接使用，不为重新读取再调用评审。

从保存的返回内容读取 `prompt`、`input_version`，再读取 `Path(task_directory) / assignment_ref["path"]` 对应的完整冻结输入；文本哈希统一使用 LF 换行。如果返回中已有 `assignment`，直接使用。文件引用适用于能读取该任务目录的调用方。在同一上下文自评时，核对当前稿件及要求／来源绑定，复用已经读过且未变的证据，重读发生变化或有疑问的部分。保留完整材料；单独上下文评审者仍收到所需的完整输入。以该 `input_version` 将实际判断作为 `self_review` 提交，字段见[自评记录说明](review-completion.zh-CN.md)。稿件或评审输入变化后沿用 `revision: true` 路径。复用减少重复复制，当前版本核对和必需阅读照常完成。

## 已验证的范围

仓库检查共用流程、插件与源码一致性，以及通过真实 stdio 连接、使用**合成评审子进程**的 MCP 调用链。这些检查不调用付费模型，也不证明报告质量。正常使用时会启动真实配置的模型执行器；安装或测试通过，不代表某份研究已经完成模型评审。

另有一次[插件 `0.1.2` 的真实模型引导验证](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/evaluation-status.zh-CN.md#当前实现)：在一份采用虚构来源材料的真实任务上完成评审与审查恢复，保留负面结果，并正确拦截交付。该次验证需要修正配置和审查输出契约，不证明无人干预运行可靠。

工具能约束自身的完成条件，不能阻止 Agent 绕过工具或在外部修改文件，也不能用机械检查证明事实正确。内容审查与原始证据仍是验收的一部分。

CLI 的 `check-draft` 使用 `task` 和可选 `artifact`，无需交付说明；检查失败退出码为 1。未达标稿件遵循[修正与停止规则](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/failure-handling.zh-CN.md)：修正普通报告的新版本，保留冻结评测原件，不反复重跑未修改的有效负面判断直到通过。
