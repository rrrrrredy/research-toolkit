# Usage and integration

[English](usage-modes.md) | [简体中文](usage-modes.zh-CN.md)

**Use the research methods through a repository link, files, attachments, or pasted text.** Choose the input method your agent supports. Native Skill, plugin, and MCP support are separate capabilities of the host.

## Use the research methods

- **Repository link:** send the [research request](https://github.com/rrrrrredy/research-toolkit/blob/main/README.md#usage) to an agent that can read GitHub.
- **Files or attachments:** download the repository, provide `SKILL.md`, and make the required reference files available.
- **Text-only input:** paste the complete entry instructions and relevant method sections. See [chat-only use](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README.md#chat-only-use).
- **Native Skill:** install the complete toolkit through the host's supported mechanism. See [agent setup](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README.md).

No Python or vendor CLI installation is required merely to read and apply the methods. Retrieval and file access come from the author agent. A separate reviewer is needed for independent review; supplying the instructions does not run one automatically.

## When to use each tool

**The first [Lite task](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/quickstart-lite.md) works without MCP.** An instructions-only session can keep the brief, sources, claims and checklist in files or separate chat sections. None of the six tool calls is required in that mode; it produces no local completion receipt.

The table applies when you choose the managed local workflow, through MCP **or the [shared CLI](#skill-only-and-cli-fallback)**. Required methods still apply when you read them directly.

| Tool | When it is needed | When you can skip the call |
| --- | --- | --- |
| `research_start` | Create a new managed task and its brief; explicitly select `profile=lite` for the first exercise. | Resume an existing task with `research_status`, or keep records yourself without local workflow tools. |
| `research_status` | Resume a managed task, inspect saved progress, or change its recorded stage. | You do not need to read or update progress; a methods-only session can use its own notes. |
| `research_guide` | Retrieve the method for a stage when it is not already available in context. | Read the relevant `SKILL.md` and `references/` files directly. |
| `research_review` | Complete the declared reviews in a Full task, including explicit self-review when that is the chosen tier. | Lite skips review; never skip a review explicitly required by the assignment. |
| `research_finish` | Complete a managed task: Lite records the six-item checklist; Full checks the reviewed report and delivery requirements. | Without local workflow tools, complete the checklist yourself and return the records without claiming a local receipt. |
| `research_check_reviewer` | Diagnose external backend setup or a configuration failure before attempting review. | Lite and self-review need no external backend; a separate call is unnecessary when `research_start` has already confirmed the unchanged configuration. |

## Optional workflow tools

Use local MCP when the host can start a local process, or the bundled plugin when it supports the plugin format. The tools use the same research methods.

| Form | What it supplies | Host requirement |
| --- | --- | --- |
| Skill | Entry instructions and detailed research methods | Native Skill discovery or explicit file reading |
| Plugin | Skill, references, and the local MCP server in one package | Support for the package format and local stdio MCP |
| MCP | Six callable tools for task setup, progress, guidance, reviews, and delivery checks | A client that can start and call a local stdio MCP server |

The shared CLI needs Python 3.10+ and only its standard library; MCP also needs the dependency in `requirements-mcp.txt`. Without a backend, new Full tasks use explicitly degraded self-review. External/independent review accepts any supported command or endpoint; no vendor account is mandatory.

## Install the plugin

The [plugin directory](https://github.com/rrrrrredy/research-toolkit/blob/main/plugins/research-toolkit/) bundles the Skill, methods and local MCP server. Use your host's supported plugin installation mechanism; [agent setup](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README.md) has host-specific instructions. Install `requirements-mcp.txt` in the Python environment that starts MCP, then confirm the six `research_*` tools are available.

Describe the topic, reader and expected result; the agent assembles the brief and asks only about critical missing choices. The package follows the [portable plugin specification](https://developers.openai.com/plugins/build/plugins); it is not a hosted service and does not imply every client supports that format.

## Connect MCP separately

Skip this section if you installed the plugin and its tools are available.

Clone the repository, install its dependency in the Python environment your client will use, and connect the server:

```bash
git clone https://github.com/rrrrrredy/research-toolkit.git
cd research-toolkit
python -m pip install -r requirements-mcp.txt
```

A client using an `mcpServers` configuration can use the following example. Replace both executable/script paths and the research workspace with your actual paths; adapt the enclosing configuration to your client.

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

On Windows, forward-slash paths such as `D:/tools/python/python.exe` are valid JSON path strings. Research files are saved under the configured workspace. Without this setting, the server uses the plugin's data directory if available, otherwise `~/.research-toolkit/tasks`. Do not save research inside the installed package.

The server also exposes the `research` prompt and `research-toolkit://instructions` resource. Ask the agent to read the instructions before using the tools. Local stdio requires a client that can start a local process; a web-only client expecting a remote HTTPS server cannot connect directly.

### Client configuration and example

The [README MCP quickstart](https://github.com/rrrrrredy/research-toolkit/blob/main/README.md#use-as-an-mcp-server) includes installation, JSON for Claude Desktop/Cursor and the equivalent native TOML for Codex. The [executable example](https://github.com/rrrrrredy/research-toolkit/blob/main/examples/mcp/README.md) captures real local responses with a fictional report and explicitly degraded self-review.

Official configuration references: [Claude Desktop local servers](https://modelcontextprotocol.io/docs/develop/connect-local-servers), [Cursor MCP](https://cursor.com/docs/mcp), [Codex MCP](https://developers.openai.com/codex/mcp). Cursor supports project `.cursor/mcp.json` or global `~/.cursor/mcp.json`; Codex uses `~/.codex/config.toml`. In Claude Desktop, open Settings → Developer → Edit Config.

If no tools appear, run `python -c "import sys, mcp; print(sys.executable)"` with the configured interpreter. An import error means the MCP dependency is missing from that environment. Use absolute script/workspace paths and restart the client. Server startup and protocol calls are exercised by `python scripts/check_mcp_contract.py`; that offline check uses synthetic reviewers and does not establish GUI compatibility or research quality.

## What happens during a task

| Tool | Action and completion boundary |
| --- | --- |
| `research_start` | Creates task records; returns missing brief fields and selects the profile and checks configured backend readiness |
| `research_status` | Returns saved progress and current methods; changing to analysis/drafting requires prerequisite source/claim records |
| `research_guide` | Loads the applicable methods without starting a task; supports English and Chinese |
| `research_review` | Binds full inputs, runs content reviews and retains replies/failures; executes additional auditing only when configured |
| `research_finish` | Records the final checklist for Lite; Full checks the reviewed artifact, evidence, unresolved requirements and delivery text before writing completion state and a receipt |
| `research_check_reviewer` | Checks local backend configuration and dependencies without model calls |

The author agent still searches, reads, analyzes and writes, using its existing tools. It must save required source texts and source/claim records in the task directory. Stage guidance reduces repeated context loading; it does not establish that a model has obeyed every instruction.

Before analysis, source records need an ID, title, locator and source type, with at least one full-text or relevant-section reading record and a reading-evidence reference. Before drafting, claims need substantive text and a type; source references must resolve to registered, read sources. Explicit hypotheses may remain unsupported with recorded uncertainty, but at least one grounded claim is required. Local file references in reading evidence must stay inside the task directory and identify an existing, nonempty file; anchors and page/section suffixes are allowed. URLs and section/page locators remain valid references without an automatic content check. These checks detect incomplete records, not whether a source was truly understood.

Reviews automatically include nonempty `state/requirements.jsonl` alongside the brief, report and source files. Both reviewer and auditor receive the full ledger, including later clarifications and changes. Editing or deleting that ledger after review prevents delivery until the changed assignment is addressed. An empty ledger adds no requirements.

Reviews require the full task, report and source files, not just URLs. The local input limit is 16 MiB; oversized input is rejected rather than silently truncated. This limit is not a promise that the configured model accepts a context of that size.

## Reviewer backends

Reviewer tier describes the review relationship; backend describes the command or endpoint that receives the report and evidence and returns a structured review. With no backend configured, a new Full report defaults to `self`; a configured backend defaults to `independent`. Explicit tiers and saved independent/audited plans never silently fall back after an error.

| Backend | Configuration cost | Review strength | Material destination and usage |
| --- | --- | --- | --- |
| `self` | None | Degraded author-context review | Current author context; its existing model usage; no additional reviewer service |
| `codex` — Codex CLI | Set `RESEARCH_TOOLKIT_REVIEW_BACKEND=codex`; install and sign in to the CLI; optional `RESEARCH_TOOLKIT_REVIEW_MODEL` | Fresh external context; supports independent review | Configured CLI model service and account quota; forward the intended `CODEX_HOME` when customized |
| `claude` — Claude Code CLI | Set `RESEARCH_TOOLKIT_REVIEW_BACKEND=claude`; install and authenticate the CLI; optional model | Fresh external context, without tools; supports independent review | Service/account configured by the CLI; consumes that account's subscription or API usage |
| `generic` — compatible HTTP endpoint | Set backend to `generic`, `RESEARCH_TOOLKIT_REVIEW_BASE_URL`, `RESEARCH_TOOLKIT_REVIEW_MODEL`; optional `RESEARCH_TOOLKIT_REVIEW_API_KEY` | Fresh request with the full assignment; supports independent review, not guaranteed statistical independence | Complete materials go to your chosen endpoint; its account is billed; local endpoints follow your own hosting policy |
| Trusted custom command | `RESEARCH_TOOLKIT_REVIEW_CONFIG` with an argv list and `format: "json"` | Depends on the adapter's actual context and evidence | Destination and usage are controlled by that command; document them before sending materials |

The configuration check is local and does not establish service availability or quota. Credentials belong in the runtime environment, never in reports or versioned configuration. The generic adapter uses `/chat/completions`; a base URL may include `/v1` or the complete route. See the [backend interface](#reviewer-backends) for requests, responses and recovery.

### Configuration and calls

Restart the MCP server after configuring its environment, or run the CLI from the same terminal. Replace the URL and model below with your provider; do not write keys into files.

```bash
export RESEARCH_TOOLKIT_REVIEW_BACKEND=generic
export RESEARCH_TOOLKIT_REVIEW_BASE_URL=https://your-provider.example/v1
export RESEARCH_TOOLKIT_REVIEW_MODEL=your-model
python scripts/research_workflow.py check-reviewer
```

On PowerShell, set each variable with `$env:NAME = "value"`. If authentication is required, pass `RESEARCH_TOOLKIT_REVIEW_API_KEY` through the client's environment. The check sends no materials or paid request; `access_unverified` means live service access remains untested.

For multiple reviewers, an auditor or a custom command, set `RESEARCH_TOOLKIT_REVIEW_CONFIG` to a trusted JSON file, for example:

```json
{"reviewers":[{"id":"primary","backend":"generic","model":"your-model","base_url":"https://your-provider.example/v1","api_key_env":"RESEARCH_TOOLKIT_REVIEW_API_KEY"}]}
```

The file takes precedence over backend environment variables. Endpoint and model are assignment-bound; secret values never enter configuration or records. Evaluations require `auditor`; a single-backend environment configuration creates another request as auditor for evaluations. Ordinary reports do not add auditing by default.

A trusted command uses `command: ["/absolute/path/to/executable", "argument"]` and `format: "json"`. It receives `{role, instructions, assignment}` on stdin; assignment includes the complete report, brief, sources and review dimensions. It returns this envelope on stdout:

```json
{"execution_id":"actual-provider-request-or-session-id","content":"original structured review response text"}
```

Commands come only from trusted startup configuration, never report contents or MCP arguments; use a fresh context per assignment. The HTTP adapter retains the original response and service request ID, rejects empty/truncated replies and does not follow redirects. Use a custom command for services with a different response protocol.

Generic entries may include `parameters`, for example `{"max_tokens":4096}`, for provider-supported output limits or reasoning options. They cannot override `model`, `messages` or `stream`, and remain part of the assignment binding.

### Self-review and Lite

`research_start` accepts `profile: "lite" | "full"`, default full. For Lite, `research_finish` returns the final checklist; complete each item with `{passed: true, evidence: "specific location and basis"}` and submit it as `checklist`. Review and full delivery gates are skipped with explicit logs; the brief, claims and section drafting remain required.

Full `research_review` accepts `reviewer: "self" | "external" | "independent"`. The first self call returns the prompt, assignment and input_version. Explicitly switch to the reviewer role in the author context, then submit report_verdict, seven-dimension coverage, findings and input_version as self_review. Records retain the author context and degraded strength, never a fabricated independent execution. New tasks without a backend use this path automatically; explicit or saved independent requirements do not fall back.

### Recovery and acceptance

Invalid configuration, a missing executable or a configured CLI's failed login blocks that route with guidance. Restore access in its actual environment. Unconfigured ordinary tasks can use self without login. The reviewer process does not automatically inherit the author agent's model access; keep credential files outside tasks.

Preserve original responses and failures. Never rerun a valid negative response; unresolved necessary corrections block Full delivery. Record evidenced [no-change decisions](review-completion.md) for mistaken findings, then resume finish. Identical assignments reuse completed reviews; changing a model or report requires an explicit revision, while frozen evaluations reject assignment changes. Timeouts remain 1–1800 seconds, default 600; a timeout-only change does not alter the assignment.

Additional audits apply only when declared; recovery completes only missing work. Timeouts clean up local processes without proving remote cancellation. The client must permit the necessary tool calls and wait long enough; avoid concurrent writers for one task.

## Skill only and CLI fallback

For Skill-only use, follow the [installation guide](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README.md). The agent carries out the methods with its own capabilities; installing instructions alone does not start MCP or automatically run reviews.

The plugin also includes a dependency-free workflow CLI. It uses the same implementation; only starting MCP requires the SDK:

```bash
python scripts/research_workflow.py start --workspace /path/to/tasks --request brief.json
python scripts/research_workflow.py review --workspace /path/to/tasks --request review.json
```

A brief request is `{"task":"comparison","language":"en","brief":{"question":"...","audience":"...","scope":"...","output":"...","depth":"...","evidence_standard":"..."}}`. Review arguments include `task`, task-relative `evidence_paths`, optional `artifact` (default `final.md`) and `purpose`. The `status`, `guide` and `finish` actions mirror MCP arguments. JSON may also be supplied through stdin.

## Verification and limits

The repository checks the shared workflow, package/source consistency and a real MCP stdio connection with **synthetic** reviewer subprocesses. Those tests do not call paid models or establish report quality. The implementation launches real configured model executors in normal use; a successful installation or test is not evidence that a particular research report has been reviewed.

A separate [guided real-model check of plugin `0.1.2`](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/evaluation-status.md#current-implementation) completed review and audit recovery on one fictional task while preserving a negative result and correctly blocking delivery. It required configuration and audit-contract corrections; it does not establish unattended reliability.

The tools enforce their own completion conditions. They cannot prevent an agent from ignoring tools or editing files outside them, and they cannot mechanically certify factual truth. Acceptance follows the selected profile and reviewer tier; independent review is required only when declared.
