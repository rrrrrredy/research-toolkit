# 使用与接入

[English](usage-modes.md) | [简体中文](usage-modes.zh-CN.md)

[版本与兼容性](compatibility.zh-CN.md)说明当前完成契约和旧任务接续。保留历史原件，继续研究时复用已有材料。

**通过仓库链接、文件、附件或粘贴文本使用研究方法。** 按 Agent 支持的输入方式使用；原生 Skill、插件和 MCP 是宿主的独立能力。

## 使用研究方法

- **仓库链接：**将[研究请求](https://github.com/rrrrrredy/research-toolkit/blob/main/README.zh-CN.md#使用)交给能读取 GitHub 的 Agent。
- **文件或附件：**下载仓库，提供 `SKILL.md`，并按任务需要提供参考文件。
- **粘贴文本：**粘贴完整入口指令与所需方法章节。见[纯聊天使用边界](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README.zh-CN.md#只能在聊天中使用时)。
- **原生 Skill：**通过宿主支持的技能机制安装完整工具箱。见[Agent 接入](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README.zh-CN.md)。

读取和使用研究方法，无须安装 Python 或特定厂商 CLI。检索与文件访问由撰写 Agent 提供；独立审阅需要另一个评审者，仅提供指令不会自动执行审阅。

## 九个工具何时用、何时可忽略

**使用[统一研究入口](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/quickstart.zh-CN.md)。** 各 Agent 按当前工作读取方法，完成独立审阅、审计和验收。CLI/MCP 按需接入，新请求省略 `profile`。

下表适用于选择了本地任务管理的情况，MCP 与[共享 CLI](#只用-skill或使用-cli)均可使用。纯 Skill 保留相同研究和独立审阅职责，不必创建这些登记表或回执。

| 工具 | 何时需要 | 何时可跳过调用 |
| --- | --- | --- |
| `research_start` | 创建新的本地任务和需求记录；使用完整方法，无需选择档位。 | 已有任务用 `research_status` 恢复，或直接使用 Skill，不创建工具管理的任务。 |
| `research_save` | 保存／更新来源、主张、要求与稿件，由 Agent 处理定位到的格式错误。 | 记录与稿件均无变化。 |
| `research_status` | 恢复本地任务、查看已保存进度或更新记录中的阶段。 | 无需查看或更新进度时；只使用方法的会话可用自己的笔记。 |
| `research_guide` | 当前上下文尚未包含所需阶段的方法，需要读取时。 | 已直接阅读相应 `SKILL.md` 和 `references/` 文件。 |
| `research_review` | 为宿主准备独立审阅、审计及验收任务，保存真实回复和输入版本。 | 未变输入已有完整有效结果时复用，继续未完成工作。 |
| `research_check_updates` | 按需读取已登记公开版本日志，关联受影响主张和正文。 | 当前无更新问题或没有已登记版本日志。 |
| `research_check_draft` | 无模型调用地检查当前稿件记录与显式篇幅，不生成交付凭证。 | 评审／交付前可选；来源与含义仍需单独核对。 |
| `research_finish` | 完成本地任务：核对当前报告与任务约定的交付要求。 | 纯 Skill 完成独立审阅、审计与验收后交付报告和引用，不要求工具回执。 |
| `research_check_reviewer` | 已选择自配后端时，诊断配置与依赖问题。 | 宿主原生子 Agent 无需另查外部服务配置。 |

## 保存研究记录与稿件

Agent 使用 `research_save`（CLI：`save`）提交来源、主张和要求对象。用户描述研究需求、决定范围和用途，不管理 CSV、编号或评审返回 JSON。工具按 ID 合并局部更新，保留其他行和字段，写入既有 CSV／JSONL 格式。省略 ID 时，按唯一网址／主张／要求摘要匹配已有记录，否则分配 ID 并返回；后续修改使用返回的 ID。来源仍由 Agent 实际阅读并准确整理。

必读要求使用 `requirements[].reading_requirement`，取值为 `full_text` 或 `relevant_sections`；`sources[].read_scope` 记录实际阅读范围，不能代替前者。仍需履行的必读要求与已保存行合并后，应同时具有 `reading_requirement` 和 `required_source_ids`。`required_source_ids` 是非空、无重复的来源 ID 列表，例如 `["S1"]`，对应来源记录。局部更新可省略已保存的字段；没有必读要求的行无需填写这两个字段。

使用本地文件时，推荐将 `read_evidence` 写成 `"sources/S1.md"`，即任务内现有非空文件的相对路径。页码、章节、阅读范围和说明放在已有的 `locator` 字段，例如 `"第2–4页，仅读取相关章节"`，不要把说明文字拼在路径后。网址、页码及已支持的本地引用形式继续有效。需要本地 UTF-8 来源文本时仍使用可选的 `evidence_path`；它不能代替或修复无效的 `read_evidence`。

以下是给 Agent 的调用示例，来源正文已保存在任务目录：

```json
{
  "task": "example",
  "sources": [{"source_id":"S1","title":"来源标题","url":"https://example.org/source","source_type":"primary","read_scope":"relevant_sections","read_evidence":"sources/source.md","locator":"第2–4页，仅读取相关章节"}],
  "claims": [{"claim":"有来源支持的判断","claim_type":"fact","supporting_sources":["S1"]}],
  "requirements": [{"summary":"阅读 S1 相关章节并解释比较结果","status":"pending","reading_requirement":"relevant_sections","required_source_ids":["S1"]}],
  "draft": {"path":"first-draft.md","complete":true}
}
```

未变化的集合不传。`draft` 可带 `content`，由工具写稿并创建父目录；省略 content 时登记已有 UTF-8 文件，无需把全文再搬进对话。`complete: true` 表示 Agent 已保存完整稿，不表示质量通过。局部更新如 `{"requirements":[{"requirement_id":"R1","status":"satisfied","evidence":"final.md，比较章节"}]}` 会保留其他字段；工具不编造证据，也不自动关闭要求。

```bash
python3 scripts/research_workflow.py save --workspace ../research-work --request save.json
```

格式错误定位到集合、行和字段，由 Agent 修正调用后重试；整批输入验证通过后才替换记录。已有集合格式损坏时，提交恢复后的完整行，并显式指定如 `"replace":["sources"]`；工具将原始字节备份到 `logs/record-backups/`，不会悄悄丢弃无法解析的行。保存后的输入变化仍按原规则使旧检查失效。

显式调用 `research_status(task, stage="analyze")` 或 `stage="draft"` 时，返回的 `requirements` 包含已保存的补充要求原文（JSONL），保留状态和处理依据，Agent 可直接用于分析与起草，无需再复制进 brief。没有补充要求时省略该字段；普通状态查询不附加正文。返回要求不表示要求已满足，仍需按其内容完成研究。

`research_status` 从已保存活动中恢复工作与成果引用。事件时间用于识别保存和交接顺序，不构成研究限时或优化目标；登记审阅时保留原始执行证据。

`save` 与 `status` 的 `changes` 给出最近一次成功保存记录的批次：新增、更新、未变、删除或格式恢复的 ID，关联主张，以及最近登记稿件中的行号／标题。来源关联同时读取 `supporting_sources` 和 `counter_evidence` 中明确登记的来源编号，沿用评审输入的空白、分号、逗号或 `|` 分隔规则，不从反证说明的文字含义推断关联；已登记版本日志查询复用这些关联。位置来自主张原文或来源链接的字面匹配，可能指向引用段或资料表；改写后的表述可通过引用链接找回，`not_located` 表示需自行定位，不等于没有影响。Agent 根据提示读取相关段落，核对来源后决定改哪些结论；不自动认定主张失效。

每个命中位置还返回 `text`（命中行原文）。一段上下文首次出现时返回 `context`，包含 `start_line`、`end_line` 与原文 `text`：命中段落及同一章节内前后至多各一段。后续位置的报告文件、行范围与原文完全相同时，返回 `context_ref: {"claim_id": "C1", "line": 7}`，不再重复 `context`；它直接指向同一 `affected_claims` 列表中对应主张、行号下的完整上下文。所有主张、来源关联、命中原因、章节与命中行号仍保留在各自条目中；原文相同但位置不同的段落不合并。按空行分段，以 `#` 标题为边界；行号从 1 开始，包含起止行。已登记版本日志查询使用同一份定位输出，无需新增输入字段或调用，也不修改报告。

已有来源正文改动后，保存该来源 ID（如 `{"sources":[{"source_id":"S1"}]}`）即可比较本地证据文件与上次保存时的哈希，不必重交其他字段。首次观察会明确标记，不能据此推断更早是否变化；旧任务无需迁移或补建历史。工具不会监控远端网页。内容字节相同的文件不重写，`updated_files` 只列实际写入；状态查询不写文件。只登记新稿会沿用最近记录批次并更新正文位置，下一批记录保存会替换该摘要；它不是待办清单，也不新增完成条件。

### 任务记录字段

已明确的需求与提纲保存在 `state/task_spec.md`。重要补充要求在 `state/requirements.jsonl` 使用稳定编号；关闭要求和明确的范围变更沿用[需求记录](delivery-verification.zh-CN.md#需求关闭与阅读记录)规则。

`progress.json.stage` 使用 `brief`、`collect`、`analyze`、`draft`、`review`、`revise`、`final`。
`progress.json.status` 使用 `in_progress`、`paused`、`blocked`、`complete`。

记录实际阶段、未决问题和下一步。接续时用 `status` 取得任务规格、有效要求、提纲、当前主稿及相关分析。调用路径相对任务目录；阶段名称描述当前工作，能否推进由实际依赖决定。

`state/findings.jsonl`、`state/directions_tried.json`、`state/iteration_log.jsonl` 和 `logs/work.jsonl` 仅在有助于当前任务时使用，不是普遍必交文件。不确定性可直接记在主张中，`data/uncertainty_registry.csv` 按需使用。字段约定见已有[工作流参考](../references/research-workflow.zh-CN.md#3-状态记录)。

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

版本日志请求会规范化主机名，要求全部解析地址均为公网地址，并直接连接这些已检查地址，保留按主机名进行的 HTTPS 证书校验。此调用不使用环境或系统代理，因为无法在本地核查代理最终解析的目标；必须经过代理的环境若无法直连，将如实返回读取失败。

调用不覆盖旧证据、不改变阅读状态、结论或交付记录。有变化时返回 `current_excerpt`，供 Agent 阅读后另存并通过现有 `research_save` 更新来源；未采纳前再次调用仍会相对旧证据报告变化。网络失败可在恢复访问后重试同一请求。

## 接续已有研究

提供已有报告、相关来源和新的用途即可，复用现有材料和笔记，无须先补建工具台账。支持从零研究，也支持以下两条路径：

```text
用 Research Toolkit 检查这份报告和相关来源，重点看会改变结论或行动的重要问题。
保留原稿，定位问题与依据，做必要的最小修订，核对修改并给我变化说明。
不为文风偏好重写整篇，不把可选建议当成必改。
```

```text
在已有研究上加入这些新资料。说明哪些事实已过期、哪些判断需要改变、哪些仍成立。
保留资料日期与版本，更新受影响的段落、来源和判断，不从头重做未受影响的研究。
交付更新稿及简短变化说明；重新完成本次改动使之失效的检查。
```

接续 CLI／MCP 管理的已有任务时，先用 `research_status(task)` 读取状态并保留旧稿。沿用来源、主张和要求编号及已有阅读依据；用 `research_save` 一并更新受影响记录，按已有路径登记稿件，未变记录无需重交。实际核对要求后，将状态和具体依据随相关更新保存。重读变化或有疑问的来源段落，复用仍有效的本地证据，无需再次获取；完成当前完整报告的独立内容审阅、审计和验收，再声明完成。[长报告实际更新案例](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/case-study/coding-benchmark-update/README.zh-CN.md)保留复用材料、来源确认的问题和实际修订。

### 内容或资料变化后

以下调用适用于 CLI／MCP 管理的任务。

| 变化 | 复用与复验 |
| --- | --- |
| 恢复中断任务，输入未变 | 用 `research_status` 读现有状态，继续未完成工作；有效的已完成评审可复用。 |
| 报告、需求、已绑定来源／主张改变 | 更新受影响分析。旧检查不代表当前版本通过；以 `revision=true` 对当前输入完成所需评审与交付核对。历史 checklist 任务沿用其保存的完成约定。 |
| 来源网页有更新，但本地保存件未变 | 工具不监控远程网页。Agent 读取并保留新版本、说明日期和结论差异后，再按输入变化处理。 |

工具的形式检查验证声明范围内的版本和记录一致性；它们不会判断新来源是否可信。`research_check_draft` 的私有聊天引用提示只扫描传入稿件、忽略代码示例，提示不改变 `ok` 或历史收据含义。引用修复须依据真实来源；具体语义仍由实际阅读和评审核对。

## 可选执行工具

宿主能启动本地进程时，可接入 MCP；同时支持该插件格式时，也可安装包含方法与工具的插件。两种方式使用同一套研究规范。

| 形式 | 提供什么 | 宿主要求 |
| --- | --- | --- |
| Skill | 入口指令与详细研究方法 | 原生技能发现或明确读取文件 |
| 插件 | Skill、参考文件和本地 MCP 服务，一次安装 | 支持该软件包格式与本地 stdio MCP |
| MCP | 初始化、保存进度、加载方法、审阅和检查交付的九个工具 | 能启动并调用本地 stdio MCP 服务 |

共享 CLI 需要 Python 3.10+，只使用标准库。Linux 上优先使用 `python3`；本机已有的 Python 3.10+ 解释器即可。MCP 还需安装 `requirements-mcp.txt` 中的依赖。默认由宿主原生 Agent 完成研究和独立审阅；另配后端是可选方式，不决定宿主能否委派。

CI 在 Python 3.10／Linux 上检查 CLI 和打包 MCP 流程，并在 Python 3.12／Linux、Windows 上执行更完整的检查。安装依赖与客户端启动服务须使用同一解释器。这些验证覆盖服务和协议，不代表所有客户端 GUI 均已实测。

## 安装插件

[插件目录](https://github.com/rrrrrredy/research-toolkit/blob/main/plugins/research-toolkit/)包含完整 Skill、方法与本地 MCP 服务；使用宿主支持的插件安装机制，具体步骤见 [Agent 接入](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README.zh-CN.md)。插件通过 Python 启动 MCP，安装 `requirements-mcp.txt` 中的依赖后，确认九个 `research_*` 工具可用。

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

重启客户端，确认能看到九个 `research_*` 工具。[可执行示例](https://github.com/rrrrrredy/research-toolkit/blob/main/examples/mcp/README.zh-CN.md)使用明确标注的合成输入说明接口，历史真实运行保留其实际审阅范围。

官方配置说明：[Claude Desktop 本地服务](https://modelcontextprotocol.io/docs/develop/connect-local-servers)、[Cursor MCP](https://cursor.com/docs/mcp)、[Codex MCP](https://developers.openai.com/codex/mcp)。Cursor 可使用项目 `.cursor/mcp.json` 或全局 `~/.cursor/mcp.json`，Codex 使用 `~/.codex/config.toml`；Claude Desktop 从 Settings → Developer → Edit Config 打开配置。

看不到工具时，用配置中的解释器执行 `python -c "import sys, mcp; print(sys.executable)"`。导入报错表示该环境缺少 MCP 依赖；使用脚本与工作区的绝对路径，并重启客户端。`python3 scripts/check_mcp_contract.py` 检查服务启动及协议调用，使用合成评审者，不证明各客户端 GUI 兼容性或研究质量。

## 一次研究如何推进

| 工具 | 实际动作与完成条件 |
| --- | --- |
| `research_start` | 建立统一任务与需求，返回共同上下文及待补充的重要缺项 |
| `research_status` | 返回进度和阶段规范；推进到分析、写作前检查来源与主张记录 |
| `research_guide` | 不创建任务，直接读取某阶段的方法，支持中英文 |
| `research_review` | 连接内容审阅、独立审计与最终验收，保存宿主原件和版本绑定 |
| `research_check_draft` | 返回当前计数、声明范围检查与记录错误，不改变任务状态；`ok` 不认证内容或交付 |
| `research_finish` | 核对已评审正文、证据、未完成要求和交付文字，通过后才写入完成状态与回执 |
| `research_check_reviewer` | 诊断可选自配后端，不作为宿主原生协作前置步骤 |

研究和统稿 Agent 使用宿主工具与共同任务输入完成检索、阅读、分析和写作。Agent 需要把必要的来源全文、来源表和主张表写入任务目录。按阶段加载规范可以减少反复读取，但不证明模型已遵守每条要求。

进入分析前，来源须有编号、标题、定位信息和类型，至少一条来源还须记录全文或相关章节的阅读范围与阅读凭据。进入写作前，主张须有正文和类型，来源引用必须对应已登记、已记录阅读的来源。明确标为假设且说明不确定性的内容可以暂缺支持，但整体至少要有一条有来源支持的主张。阅读凭据若指向本地文件，文件须位于任务目录内、实际存在且内容非空，支持附带锚点和页码、章节说明。网址及章节、页码定位仍可使用，但不会因此自动完成内容核查。这些检查识别空记录与无效关联，不证明模型真正理解了材料。

`status` 同时提供 `work` 时，分析／起草检查使用所选来源、主张及声明的上游输入，不让无关支线尚未完成的工作阻塞当前单元。单元可先从已选来源展开分析，再登记新形成的主张；全文审阅和交付仍核对完整任务及主张依据。

评审会自动纳入非空的 `state/requirements.jsonl`，评审者和审查者都能看到完整需求台账，包括后续澄清与变更。评审后更改或删除该台账会阻止交付，须先处理发生变化的任务。空台账不增加需求。

评审保留完整任务、正文与相关来源文件，不能只给网址。宿主原生任务默认返回可读文件引用；必需材料超过一个模型上下文时，评审者分段读取保留的原件并完成所分配的审阅，不能静默用摘要替代必需材料。

## 评审后端

<a id="reviewer-backends"></a>

### 宿主原生审阅

直接使用 Codex、Claude Code 等宿主已有的子 Agent 能力。`research_review` 准备任务，绑定完整需求、报告和原始证据；宿主为每项基础视角和所需领域专审启动不同的独立 Agent，再运行独立审计与最终验收。作者和统稿 Agent 不承担这些独立任务，这条路径无需另配 API。

七项基础视角是需求、证据、对抗推理、结构与深度、读者用途、过程语言、自然表达，各自使用独立上下文。模型可以相同，执行上下文和生产职责必须分开。[审阅契约](review-completion.zh-CN.md)说明任务、原始结果和当前版本的完成条件。

宿主保留每次真实回复与执行记录，通过同一个 `review` 提交路径。内容审阅具备完整结果后，下一项任务是独立审计；报告和审计中的必要问题解决后进入最终验收。前段研究单元需要审阅时，指明对应单元；该结果支撑后续依赖工作，不代替全稿审阅。

### 可选的自配执行方式

只在主动选用独立命令或端点执行评审时配置这一节。宿主原生子 Agent 不需要这些配置。

| 后端 | 配置 |
| --- | --- |
| `codex` | `RESEARCH_TOOLKIT_REVIEW_BACKEND=codex`，使用已安装、已登录的 CLI；可选 `RESEARCH_TOOLKIT_REVIEW_MODEL`。 |
| `claude` | `RESEARCH_TOOLKIT_REVIEW_BACKEND=claude`，使用已安装 CLI 及其现有配置。 |
| `generic` | 后端 `generic`、`RESEARCH_TOOLKIT_REVIEW_BASE_URL`、`RESEARCH_TOOLKIT_REVIEW_MODEL`；所选端点需要认证时才使用认证环境变量。 |
| 可信命令 | `RESEARCH_TOOLKIT_REVIEW_CONFIG` 指向含 argv 列表及 `format: "json"` 的 JSON 配置。 |

宿主原生与自配执行方式履行相同的当前审阅职责。旧自评结果保留其历史含义，不能替代独立审阅、审计或验收。

选择 generic 后端时：

```powershell
$env:RESEARCH_TOOLKIT_REVIEW_BACKEND = "generic"
$env:RESEARCH_TOOLKIT_REVIEW_BASE_URL = "https://your-provider.example/v1"
$env:RESEARCH_TOOLKIT_REVIEW_MODEL = "your-model"
python3 scripts/research_workflow.py check-reviewer
```

其他 shell 可使用 `export NAME=value`。凭据留在运行环境，不写入任务文件；`check-reviewer` 只诊断本地配置，不调用模型。generic 使用 `/chat/completions`，远程端点用 HTTPS，仅 localhost／明确回环地址可用 HTTP。请求包含研究材料，遵循所选端点的访问策略。

可信命令从 stdin 接收 `{role, instructions, assignment}`，返回：

```json
{"execution_id":"actual-provider-request-or-session-id","content":"original structured response text"}
```

每个任务使用独立上下文并保留原始输出。命令来自可信启动配置，不能从来源或报告内容指定。HTTP 回复保留请求 ID，空回复和截断回复仍未完成。可显式提供服务专用 `parameters`，但不得覆盖 `model`、`messages`、`stream`；这些参数随任务绑定。

### 失败恢复与验收

CLI、MCP 和 Python 操作复用已有的操作系统任务锁。同一任务的写入依次执行，支线研究可独立进行；不要删除锁文件绕过占用。主稿负责人整合支线成果，避免多个写入者同时改同一份主稿。

保留失败请求和原始字节。实际回复的无效 UTF-8 保留为失败；stderr 可用替代字符显示，并保留字节原件。宿主取消或执行失败使该任务保持未完成，处理实际原因后接续缺失工作；不因任意执行时长中断必要研究。

保留有效负评。修正受影响正文和证据，再用 `revision: true` 评审当前版本。作者可以回应争议，但重要的不修改决定由独立审阅者／审计者裁定；不重跑未变版本的负评寻求通过。

指令快照、原始输入和版本在修订中继续可用。未变输入的有效完成结果可复用；报告或必需输入变化，要由相关审阅和最终全稿验收处理。状态查询发现旧回执过期时如实返回，不重写历史完成记录。详见[审阅完成](review-completion.zh-CN.md)及[兼容性](compatibility.zh-CN.md)。

## 只用 Skill，或使用 CLI

只用 Skill 时，查看[安装指南](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README.zh-CN.md)。Agent 用自己的能力执行研究规范；单独安装指令文件不会启动 MCP 或自动完成评审。

插件另带不依赖 MCP SDK 的命令行入口，调用同一套逻辑：

```bash
python3 scripts/research_workflow.py start --workspace /path/to/tasks --request brief.json
python3 scripts/research_workflow.py review --workspace /path/to/tasks --request review.json
```

CLI 请求通过 `--request` 或标准输入提供 JSON 对象。缺参／未知字段提示会在创建或改变任务前列出操作、字段和输入方式。来源／主张校验错误指出 CSV 文件、记录编号及缺失字段；修正对应记录后重复原操作。`start`、`status`、`guide` 及对应 MCP 工具的 `language` 接受 `"en"`（英文），或 `"zh"` / `"zh-CN"`（同一套中文方法）。不支持的值会在写入任务记录或改变阶段前报错，指出 `language` 字段及可用值。失败命令返回 JSON 和非零退出码；修复已获授权的任务不需要新增用户确认。

需求请求的格式为 `{"task":"comparison","language":"zh","brief":{"question":"...","audience":"...","scope":"...","output":"...","depth":"...","evidence_standard":"..."}}`。评审参数包括 `task`、任务内相对路径 `evidence_paths`，以及可选的 `artifact`（默认 `final.md`）和 `purpose`。`status`、`guide`、`finish` 对应同名 MCP 工具的参数。也可通过标准输入提供 JSON。

<a id="复用任务文件并保存自评材料"></a>

### 复用任务文件并保存审阅材料

报告、分析和来源原件保存在任务目录，`artifact` 与 `evidence_paths` 直接引用这些文件。保留首稿和后续版本，不为每次工具调用另复制材料。

已有工具任务可准备：

```json
{"task":"comparison","artifact":"final.md","evidence_paths":["sources/source.md"],"include_assignment":false}
```

```bash
python3 scripts/research_workflow.py review --workspace ../research-work --request review.json
```

宿主原生执行时，返回待完成任务及其保存的完整输入。每位执行者都应能够打开完整任务与引用原件；跨环境传递可读内容，不只传无法访问的本地路径。保留真实宿主任务 ID、完整原始回复和执行记录，再通过同一操作的 `host_result` 提交，字段见[审阅契约](review-completion.zh-CN.md)。

宿主继续返回的审阅、审计或验收任务。摘要用于定位结果，不替代完整结果或来源原文。正文或必需输入改变时保留前一材料包，用 `revision: true` 处理新版本。

## 已验证的范围

现有软件检查使用明确标注的合成材料，验证记录一致性、原始输入绑定、打包及 MCP 传输。真实宿主执行另有其来源、回复和结果；[评测现状](evaluation-status.zh-CN.md)列出实际观察。安装成功或机械检查通过，不是内容审阅结果。

当前交付要求独立内容审阅、审计和验收。工具落实保存的完成契约，Agent 实际阅读并作出内容判断。旧回执按原契约保留，不写成当前验收。具体失败按[修复说明](failure-handling.zh-CN.md)接续受影响工作。

## 当前主稿与需求变更

`research_save` 新增可选 `brief` 局部更新：只传变更的 question/audience/scope/output/depth/evidence_standard，未传字段保留，并同步规格和进度中的 brief。与受影响要求一起保存，不需要再维护一份范围台账。

```json
{"task":"comparison","brief":{"output":"一份修订后的比较报告"},"draft":{"path":"drafts/revised.md","main":true,"kind":"report","host_task":"actual-main-writer-host-task"}}
```

`draft.main=true` 显式选定当前工作文件；`kind` 可选 report/comparison/review/analysis。保存其他章节或参考稿不改变该选择。`complete` 仍只记录完整草稿。`save/status.current_work` 返回当前文件、有效要求、未结工作和恢复路径；status 另列上次交付引用。新主稿或需求修订不会继承终态，旧凭证保留。审阅／交付传当前主稿的 artifact。旧任务不必迁移，未选主稿时保持原行为；当前文件观察摘要不是批准。

`start/status.runtime` 返回执行实现的位置、版本、代码摘要和可用入口摘要；host_loaded_entry=not_observed，不推断宿主读了哪个 Skill。工具只识别登记的文件，不监控任意新目录。

阅读要求在保存时检查 full_text/relevant_sections 和非空、不重复的 required_source_ids；配对字段可在既有行上局部更新。无效批次不部分覆盖正文或状态。详细方法见[任务接续](../references/task-continuity.zh-CN.md)。

## 历史任务兼容

1.x 任务、报告、输入快照和回执继续可读，保留原身份及当时的完成结果。历史 `profile`、`self_review` 字段不构成第二套研究入口，也不能满足当前独立职责。

在原工具任务中接续材料：取得当前工作，保留旧稿和回执，为本次接续准备当前版本审阅。复用有效来源、分析与原始评审，补齐当前契约所需的角色与实质工作。不把旧自评改写成独立执行，也不补造缺失审阅。见[版本兼容性](compatibility.zh-CN.md)。

## 研究委派与成果交接

提纲和原始要求保留在现有任务规格中，按有意义的研究单元及实际依赖分工。即使按技术问题拆分，国内／海外或其他明确覆盖维度仍应可见。

用 `status` 准备下一位执行者的输入。以下格式示例假定引用的上游单元及记录已存在：

```json
{"task":"study","methods":["compare","delegate"],"work":{"unit_id":"route-comparison","question":"哪些技术差异会改变选择？","depends_on":["route-evidence"],"requirement_ids":["R2"],"claim_ids":["C1"],"paths":["reports/current.md"]}}
```

`work` 各字段均可选，首次保存前可用新的 `unit_id` 标识本次分工。所选主张带入支持与已登记反证来源，阅读要求带入指定来源。已登记单元会带回完整成果及其原始输入，依赖带入上游全文与原件。`work_context` 返回任务、有效要求、选定记录、可读 `files`、二进制原件引用、依赖及其就绪情况、`inputs` 和 `input_version`。

仍适用的 `satisfied` 要求继续出现在 `effective_requirements`，`scope_decisions` 保留明确的放弃、排除或接受未完成决定。工具不会从宿主对话自动猜出要求；使用已有字段保存真实原话和受影响要求。按具体记录 ID 绑定的工作不再因无关来源／主张行改变而过期，有效要求的变化仍需处理。

通过宿主子 Agent 工具传递返回的问题、要求与可访问原件，保留真实宿主任务／会话标识。宿主负责启动、消息、等待和取消，Toolkit 不另造一套运行时。

执行者用 `save` 保存成果：

```json
{"task":"study","draft":{"path":"analysis/routes.md","kind":"analysis","unit_id":"route-comparison","question":"哪些技术差异会改变选择？","depends_on":["route-evidence"],"host_task":"actual-producing-host-task-id","complete":false,"handoff":{"summary":"比较已展开，部署假设仍待解决。","pending":["对照原始要求解决部署假设。"],"decisions":["两条路线使用相同工作量和质量口径。"]}}}
```

省略 `content` 可登记已有非空文件，也可提供文本保存；把 `work_context.inputs` 原样放入可选 `draft.based_on`，不编造哈希。`complete` 描述已保存单元或稿件的完整性，不代表全任务交付。上游已登记工作未完成、已变化或尚缺必需独立审阅时，不能将依赖它的单元声明完成；先以 `complete: false` 保存进行中的工作并解决依赖。

`current_work.work_units` 与 `research_outputs` 从已有活动日志恢复单元、原始快照、宿主引用、交接和输入变化，不另建任务看板。交接 `summary`、`pending`、`decisions` 用于导航，接收的研究者、统稿者或审阅者可以读取完整成果和原始来源；同一 Agent 接下一阶段也复用这些记录。

`draft.main: true` 只指定当前主稿，保存的 `host_task` 是写入负责人，其他支线保留独立文件。交接写入责任时，由当前负责人保存接收方宿主任务／会话的 `handoff.to`；仅换 `host_task` 不能接管主稿或已有负责人单元。

保留每次已保存单元的版本。新要求或证据先返回受影响分析和提纲，再依赖修订结果；`changed_inputs` 表示绑定变化，不自动认定研究结论失效。单元审阅以 `unit_id` 作为 `review.scope`，最终审阅、审计和验收仍覆盖完整当前报告。
