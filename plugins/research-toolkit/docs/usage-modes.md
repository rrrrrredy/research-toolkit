# Usage and integration

[English](usage-modes.md) | [简体中文](usage-modes.zh-CN.md)

The [1.x compatibility policy](compatibility.md) covers the public tools, saved tasks and installation requirements. Upgrading from v0.2.7 to v1.0.0 requires no task-data migration.

**Use the research methods through a repository link, files, attachments, or pasted text.** Choose the input method your agent supports. Native Skill, plugin, and MCP support are separate capabilities of the host.

## Use the research methods

- **Repository link:** send the [research request](https://github.com/rrrrrredy/research-toolkit/blob/main/README.md#usage) to an agent that can read GitHub.
- **Files or attachments:** download the repository, provide `SKILL.md`, and make the required reference files available.
- **Text-only input:** paste the complete entry instructions and relevant method sections. See [chat-only use](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README.md#chat-only-use).
- **Native Skill:** install the complete toolkit through the host's supported mechanism. See [agent setup](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README.md).

No Python or vendor CLI installation is required merely to read and apply the methods. Retrieval and file access come from the author agent. A separate reviewer is needed for independent review; supplying the instructions does not run one automatically.

## When to use each tool

**Choose [Lite](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/quickstart-lite.md) or [Full](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/quickstart-full.md) from the task.** Both share the research baseline and agent-managed records. Lite completes author checks; Full adds the selected review, revision checks and delivery consistency. Read the methods directly; connect CLI/MCP when useful.

The table applies when you choose the managed local workflow, through MCP **or the [shared CLI](#skill-only-and-cli-fallback)**. Required methods still apply when you read them directly.

| Tool | When it is needed | When you can skip the call |
| --- | --- | --- |
| `research_start` | Create a new managed task and its brief; explicitly select `lite` or `full` from use, evidence complexity and review needs. | Resume an existing task with `research_status`, or keep records yourself without local workflow tools. |
| `research_save` | Save/update sources, claims, requirements and drafts; correct located format errors. | No record or draft changes. |
| `research_status` | Resume a managed task, inspect saved progress, or change its recorded stage. | You do not need to read or update progress; a methods-only session can use its own notes. |
| `research_guide` | Retrieve the method for a stage when it is not already available in context. | Read the relevant `SKILL.md` and `references/` files directly. |
| `research_review` | Complete the declared reviews in a Full task, including explicit self-review when that is the chosen tier. | Lite skips review; never skip a review explicitly required by the assignment. |
| `research_check_draft` | Check current draft records and explicit length bounds without model calls or a delivery receipt. | Optional before review/finish; inspect sources and meaning separately. |
| `research_finish` | Complete a managed task: Lite records the six-item checklist; Full checks the reviewed report and delivery requirements. | Without local workflow tools, complete the checklist yourself and return the records without claiming a local receipt. |
| `research_check_reviewer` | Diagnose external backend setup or a configuration failure before attempting review. | Lite and self-review need no external backend; a separate call is unnecessary when `research_start` has already confirmed the unchanged configuration. |

## Save research records and drafts

The agent uses `research_save` (CLI: `save`) to save source, claim and requirement objects. Users describe the research and make scope/use decisions; they do not manage CSV, IDs or review-response JSON. The tool merges partial updates by ID, retains other rows/columns, and writes the existing CSV/JSONL formats. If an ID is omitted, it matches a unique URL/claim/summary or assigns an ID and returns it. Use that ID for later edits. The agent still reads sources and supplies accurate content.

Example request for the agent, after saving the source text in the task directory:

```json
{
  "task": "example",
  "sources": [{"title":"Source title","url":"https://example.org/source","source_type":"primary","read_scope":"relevant_sections","read_evidence":"sources/source.md"}],
  "claims": [{"claim":"The source-backed finding","claim_type":"fact","supporting_sources":["S1"]}],
  "requirements": [{"summary":"Explain the comparison","status":"pending"}],
  "draft": {"path":"first-draft.md","complete":true}
}
```

Omit a collection when it does not change. `draft` may include `content` to write the report and create its parent directory; omit content to register an existing UTF-8 file without copying it through the conversation. `complete: true` records that the agent has saved a complete draft, not that its quality passed. A partial update such as `{"requirements":[{"requirement_id":"R1","status":"satisfied","evidence":"final.md, comparison section"}]}` preserves the other fields; it does not invent evidence or automatically close work.

```bash
python3 scripts/research_workflow.py save --workspace ../research-work --request save.json
```

Format errors identify the collection, row and field. The agent fixes those inputs and retries; the whole request is validated before records are replaced. To recover a malformed existing collection, send its complete recovered rows with, for example, `"replace":["sources"]`. The tool preserves the original bytes under `logs/record-backups/`. This is explicit replacement, not silent removal of unparsed rows. Saved input changes continue to invalidate earlier checks normally.

Explicit `research_status(task, stage="analyze")` or `stage="draft"` calls return saved supplemental requirements as JSONL text in `requirements`, retaining their statuses and handling evidence. The agent can use them directly in analysis and drafting without copying them into the brief. The field is omitted when no requirements exist; ordinary status queries do not include the text. Returning a requirement does not establish that the research satisfies it.

`research_status` returns an `activity` summary: task start, first observed complete draft with UTC time/hash and elapsed time since task creation, failed saves, actual review attempts/retries, elapsed invocation time and returned usage. `saved_by_tool` timestamps the save; `existing_file_observed` timestamps registration, not historical creation. Read-only status/draft/delivery checks do not append activity. Review reuse is not a new invocation; author self-review submissions are counted separately. Cached tokens remain a subset of input; unavailable usage is unknown. The tool cannot see the host author's overall tokens, bill, or time before registration. These observations add no delivery requirement and do not establish first usable-result time or research quality.

`save` and `status` return `changes` for the latest successful record-save batch: added, updated, unchanged, removed or recovered IDs, related claims, and line/heading locations in the latest registered draft. Locations are literal claim-text or source-link matches and may point to a citation paragraph or bibliography; `not_located` means inspect manually, not no impact. Use them to read relevant passages and verify sources before deciding which conclusions to revise; claims are not automatically invalidated.

Each matched location also returns `text` (the matched line) and `context` with `start_line`, `end_line` and original `text`: the matched paragraph and up to one adjacent paragraph on each side within the same section. Blank lines separate paragraphs; `#` headings bound the context. Line numbers are one-based and inclusive. Registered release-log queries use this same location output. No extra input fields or calls are needed, and the report is not modified.

After changing local source text, save its ID (for example `{"sources":[{"source_id":"S1"}]}`) to compare evidence-file hashes with the previous save observation, without resending other fields. First observations are explicit and say nothing about earlier changes; old tasks need no migration or reconstructed history. Remote pages are not monitored. Byte-identical files are not rewritten and `updated_files` lists actual writes; status is read-only. Registering only a new draft keeps the latest record batch and refreshes its body locations; the next record save replaces that summary. This is not a backlog or a new completion requirement.

### Check a registered release log on demand

`research_check_updates(task, source_id)` (CLI: `check-updates`) reads one registered public release log. It compares the latest saved date and newer entries, returning added/revised content, source-labelled dates, and existing claim/report locations. No change returns `status: unchanged` and ends the check. Network, reading, format or comparison failures return `status: failed`, `phase` and an explanation; the CLI exits with code 1.

```json
{"task":"alibaba-20261016","source_id":"S3"}
```

```bash
python3 scripts/research_workflow.py check-updates --workspace ../research-work --request check-updates.json
```

Use the existing `official_release` source type, or `release_notes`/`changelog`. The registered `url` must be a public HTTPS log; `evidence_path` (or a parseable `read_evidence`) points to saved UTF-8 log text inside the task. Supported HTML/plain text/Markdown has standalone `YYYY-MM-DD` or `YYYY年MM月DD日` dates, a version on the next nonempty line, and a body. Saved web-tool `Lnumber:` prefixes are ignored. Login pages, JavaScript-only bodies, other date formats, or pages missing the latest saved release fail explicitly rather than reporting no change.

This is a manual call: one registered URL, no redirects, other-page crawling or scheduling. It compares the latest saved date and newer entries, not revisions to older history. Deletions/replacements within compared entries are returned too. Dates are source labels, not exact publication timestamps. Report locations reuse literal matching; inspect manually when no location is found.

The call does not overwrite evidence or change reading status, conclusions or delivery records. Changed results include `current_excerpt` for the agent to read, save separately and register through the existing `research_save` flow. Until adopted, another call still compares against the old evidence. Retry the same request after resolving a network failure.

## Continue existing research

Provide the report, relevant sources and intended use; the agent maintains the records. Starting from a question remains supported. Two adjacent requests are:

```text
Use Research Toolkit to check this report against the related sources,
focusing on important problems that change a conclusion or action.
Preserve the original, locate each issue and its evidence, make the necessary
minimal revision, check the result, and return a short change note.
Recommend Lite or Full for the use. Do not rewrite for optional style preferences.
```

```text
Update this research with the new material. Explain which facts are outdated,
which judgments change and which still hold. Preserve source dates and versions.
Update affected passages, sources and claims; reuse unaffected research.
Deliver the revised report and change note, refreshing checks invalidated by the changes.
```

When continuing the saved profile, start with `research_status(task)` and preserve the previous report. Keep existing source, claim and requirement IDs and their reading evidence. Use `research_save` to update only affected records together, registering the saved draft by its existing path; unchanged records need no resubmission. After actually checking a requirement, save its status and concrete evidence with the relevant update. Recheck changed or questioned source sections; reuse still-valid local evidence without fetching it again. Review the complete current report under its selected tier before claiming completion. See the [executed long-report update](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/case-study/coding-benchmark-update/README.md) for actual reuse, source-confirmed changes, rework and costs.

### Continue Lite work in Full

When formal review or delivery checks are needed, preserve the Lite task and create a linked Full task with a new ID. The agent uses the original brief, noting the old task location, report version and new purpose in `task_spec.md`; reuse the report, source texts and reading scope, claims and known requirements. Unchanged work with still-valid evidence need not be repeated; check new or affected requirements. The user does not refill internal forms.

The new Full task has its own progress, review plan and receipts. Do not copy Lite `progress.json`, passed flags, checklist, review logs or receipts as Full completion evidence, or rewrite the original Lite profile. Earlier author checks remain historical context, not an independent opinion.

Existing tool path: `research_start(new_task, original_brief, profile="full")` → agent arranges reusable material → `research_status(new_task, stage="draft")` → `research_check_draft` → `research_review` → necessary revision/recheck → `research_finish`. Select self, external or independent according to the task; an explicit independent requirement needs actual execution, and Astra in a separate context is sufficient. Methods-only use can retain the same drafts and reviews without claiming a local receipt.

### When content or sources change

| Change | Reuse and recheck |
| --- | --- |
| Resume interrupted work with unchanged inputs | Read `research_status` and continue unfinished work; completed valid reviews can be reused. |
| Report, requirements, bound sources or claims change | Update affected analysis. Earlier checks do not approve the current version; Lite rechecks affected items and submits the current checklist, while Full uses `revision=true` for required reviews and delivery checks of current inputs. |
| A source webpage changes but the saved text does not | Tools do not monitor remote pages. The agent reads and retains the new version, explains its date and effect, then handles it as changed input. |

Full's formal checks establish version and record consistency within the declared scope, not source credibility. The private-chat-citation advisory in `research_check_draft` scans only the supplied report and ignores code examples; it changes neither `ok` nor historical receipt meanings. Repair citations from actual sources; reading and review still establish semantic support.

## Optional workflow tools

Use local MCP when the host can start a local process, or the bundled plugin when it supports the plugin format. The tools use the same research methods.

| Form | What it supplies | Host requirement |
| --- | --- | --- |
| Skill | Entry instructions and detailed research methods | Native Skill discovery or explicit file reading |
| Plugin | Skill, references, and the local MCP server in one package | Support for the package format and local stdio MCP |
| MCP | Eight callable tools for task setup, progress, guidance, reviews, and delivery checks | A client that can start and call a local stdio MCP server |

The shared CLI needs Python 3.10+ and only its standard library. Prefer `python3` on Linux; any installed Python 3.10+ interpreter is enough. MCP also needs the dependency in `requirements-mcp.txt`. Without a backend, new Full tasks use explicitly degraded self-review. External/independent review accepts any supported command or endpoint; no vendor account is mandatory.

CI exercises the CLI and packaged MCP workflow on Python 3.10/Linux, plus the broader checks on Python 3.12/Linux and Windows. Use the same interpreter for dependency installation and your client's server command. These are server/protocol checks, not tests of every client GUI.

## Install the plugin

The [plugin directory](https://github.com/rrrrrredy/research-toolkit/blob/main/plugins/research-toolkit/) bundles the Skill, methods and local MCP server. Use your host's supported plugin installation mechanism; [agent setup](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README.md) has host-specific instructions. Install `requirements-mcp.txt` in the Python environment that starts MCP, then confirm the eight `research_*` tools are available.

Describe the topic, reader and expected result; the agent assembles the brief and asks only about critical missing choices. The package follows the [portable plugin specification](https://developers.openai.com/plugins/build/plugins); it is not a hosted service and does not imply every client supports that format.

## Connect MCP separately

Skip this section if you installed the plugin and its tools are available.

Clone the repository, install its dependency in the Python environment your client will use, and connect the server:

```bash
git clone https://github.com/rrrrrredy/research-toolkit.git
cd research-toolkit
```

Use Python 3.10+ in a dedicated virtual environment. From the cloned repository:

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

If Windows has no `py` launcher, use your installed Python 3.10+ executable in the first command. Use the printed absolute interpreter path as the MCP `command`; no environment activation or PowerShell execution-policy change is needed. If Linux reports that `venv`/`ensurepip` is missing, install your distribution's venv package (commonly `python3-venv` on Debian/Ubuntu), then recreate the environment. An `externally-managed-environment` error usually means the install used system Python: rerun pip through `.venv` as above. See the [Python venv documentation](https://docs.python.org/3/library/venv.html).


A client using an `mcpServers` configuration can use the following example. Replace both executable/script paths and the research workspace with your actual paths; adapt the enclosing configuration to your client.

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

On Windows, forward-slash paths such as `D:/tools/research-toolkit/.venv/Scripts/python.exe` are valid JSON path strings. Research files are saved under the configured workspace. Without this setting, the server uses the plugin's data directory if available, otherwise `~/.research-toolkit/tasks`. Do not save research inside the installed package.

The server also exposes the `research` prompt and `research-toolkit://instructions` resource. Ask the agent to read the instructions before using the tools. Local stdio requires a client that can start a local process; a web-only client expecting a remote HTTPS server cannot connect directly.

### Client configuration and example

Claude Desktop and Cursor use the JSON configuration above. Codex CLI / IDE uses native TOML; add the equivalent to `~/.codex/config.toml`, replacing all three paths with your actual absolute paths:

```toml
[mcp_servers.research-toolkit]
command = "/absolute/path/to/research-toolkit/.venv/bin/python"
args = ["/absolute/path/to/research-toolkit/scripts/research_mcp.py"]

[mcp_servers.research-toolkit.env]
RESEARCH_TOOLKIT_WORKSPACE = "/absolute/path/to/research-tasks"
```

Restart the client and confirm the eight `research_*` tools appear. The [executable example](https://github.com/rrrrrredy/research-toolkit/blob/main/examples/mcp/README.md) captures real local responses with a fictional report and explicitly degraded self-review.

Official configuration references: [Claude Desktop local servers](https://modelcontextprotocol.io/docs/develop/connect-local-servers), [Cursor MCP](https://cursor.com/docs/mcp), [Codex MCP](https://developers.openai.com/codex/mcp). Cursor supports project `.cursor/mcp.json` or global `~/.cursor/mcp.json`; Codex uses `~/.codex/config.toml`. In Claude Desktop, open Settings → Developer → Edit Config.

If no tools appear, run `python -c "import sys, mcp; print(sys.executable)"` with the configured interpreter. An import error means the MCP dependency is missing from that environment. Use absolute script/workspace paths and restart the client. Server startup and protocol calls are exercised by `python3 scripts/check_mcp_contract.py`; that offline check uses synthetic reviewers and does not establish GUI compatibility or research quality.

## What happens during a task

| Tool | Action and completion boundary |
| --- | --- |
| `research_start` | Creates task records; returns missing brief fields and selects the profile and checks configured backend readiness |
| `research_status` | Returns saved progress and current methods; changing to analysis/drafting requires prerequisite source/claim records |
| `research_guide` | Loads the applicable methods without starting a task; supports English and Chinese |
| `research_review` | Binds full inputs, runs content reviews and retains replies/failures; executes additional auditing only when configured |
| `research_check_draft` | Return current counts, declared range checks and record errors without changing task state; `ok` does not certify content or delivery |
| `research_finish` | Records the final checklist for Lite; Full checks the reviewed artifact, evidence, unresolved requirements and delivery text before writing completion state and a receipt |
| `research_check_reviewer` | Checks local backend configuration and dependencies without model calls |

The author agent still searches, reads, analyzes and writes, using its existing tools. It must save required source texts and source/claim records in the task directory. Stage guidance reduces repeated context loading; it does not establish that a model has obeyed every instruction.

Before analysis, source records need an ID, title, locator and source type, with at least one full-text or relevant-section reading record and a reading-evidence reference. Before drafting, claims need substantive text and a type; source references must resolve to registered, read sources. Explicit hypotheses may remain unsupported with recorded uncertainty, but at least one grounded claim is required. Local file references in reading evidence must stay inside the task directory and identify an existing, nonempty file; anchors and page/section suffixes are allowed. URLs and section/page locators remain valid references without an automatic content check. These checks detect incomplete records, not whether a source was truly understood.

Reviews automatically include nonempty `state/requirements.jsonl` alongside the brief, report and source files. Both reviewer and auditor receive the full ledger, including later clarifications and changes. Editing or deleting that ledger after review prevents delivery until the changed assignment is addressed. An empty ledger adds no requirements.

Reviews require the full task, report and source files, not just URLs. The local input limit is 16 MiB; oversized input is rejected rather than silently truncated. This limit is not a promise that the configured model accepts a context of that size.

## Reviewer backends

Reviewer tier describes the review relationship; backend describes the command or endpoint that receives the report and evidence and returns a structured review. With no backend configured, a new Full report defaults to `self`; a configured backend defaults to `independent`. Explicit tiers and saved independent/audited plans never silently fall back after an error.

Astra in a fresh context separate from the author can provide the independent review, including when the author uses the same model. Give it the same task, report and source materials; keep author notes and evaluation condition mappings out of a blind review. No additional outside person, vendor or fixed reviewer panel is required. Existing user and development tasks are independent real tasks, and their executed tests are real tests; record their actual reuse without treating it as missing task material. Model execution and evaluation also provide a user perspective: judge usefulness from actual context use, extra reading, time, rework and research results. Human participation is not a prerequisite; describe the observed benefit and its task scope.

| Backend | Configuration cost | Review strength | Material destination and usage |
| --- | --- | --- | --- |
| `self` | None | Degraded author-context review | Current author context; its existing model usage; no additional reviewer service |
| `codex` — Codex CLI | Set `RESEARCH_TOOLKIT_REVIEW_BACKEND=codex`; install and sign in to the CLI; optional `RESEARCH_TOOLKIT_REVIEW_MODEL` | Fresh review context; supports independent review | Configured CLI model service and account quota; forward the intended `CODEX_HOME` when customized |
| `claude` — Claude Code CLI | Set `RESEARCH_TOOLKIT_REVIEW_BACKEND=claude`; install and authenticate the CLI; optional model | Fresh review context, without tools; supports independent review | Service/account configured by the CLI; consumes that account's subscription or API usage |
| `generic` — compatible HTTP endpoint | Set backend to `generic`, `RESEARCH_TOOLKIT_REVIEW_BASE_URL`, `RESEARCH_TOOLKIT_REVIEW_MODEL`; optional `RESEARCH_TOOLKIT_REVIEW_API_KEY` | Fresh request with the full assignment; supports independent review, not guaranteed statistical independence | Complete materials go to your chosen endpoint; its account is billed; local endpoints follow your own hosting policy |
| Trusted custom command | `RESEARCH_TOOLKIT_REVIEW_CONFIG` with an argv list and `format: "json"` | Depends on the adapter's actual context and evidence | Destination and usage are controlled by that command; document them before sending materials |

The configuration check is local and does not establish service availability or quota. Credentials belong in the runtime environment, never in reports or versioned configuration. The generic adapter uses `/chat/completions`; a base URL may include `/v1` or the complete route. Remote endpoints require HTTPS; HTTP is accepted only for `localhost` or a literal loopback IP address, such as `127.0.0.1` or `::1`. This applies even without an API key because requests contain the report and sources. See the [backend interface](#reviewer-backends) for requests, responses and recovery.

### Configuration and calls

Restart the MCP server after configuring its environment, or run the CLI from the same terminal. Replace the URL and model below with your provider; do not write keys into files.

```bash
export RESEARCH_TOOLKIT_REVIEW_BACKEND=generic
export RESEARCH_TOOLKIT_REVIEW_BASE_URL=https://your-provider.example/v1
export RESEARCH_TOOLKIT_REVIEW_MODEL=your-model
python3 scripts/research_workflow.py check-reviewer
```

On PowerShell, set each variable with `$env:NAME = "value"`. If authentication is required, pass `RESEARCH_TOOLKIT_REVIEW_API_KEY` through the client's environment. The check sends no materials or paid request; `access_unverified` means live service access remains untested.

For multiple reviewers, an auditor or a custom command, set `RESEARCH_TOOLKIT_REVIEW_CONFIG` to a trusted JSON file, for example:

```json
{"reviewers":[{"id":"primary","backend":"generic","model":"your-model","base_url":"https://your-provider.example/v1","api_key_env":"RESEARCH_TOOLKIT_REVIEW_API_KEY"}]}
```

The file takes precedence over backend environment variables. Endpoint and model are assignment-bound; secret values never enter configuration or records. New reports and evaluations use the configured reviewer without adding an auditor. Include `auditor` only when an additional audit is intended. Resuming a saved audited plan retains its auditor requirement; a single-backend environment configuration supplies that separate request only for such a saved plan.

A trusted command uses `command: ["/absolute/path/to/executable", "argument"]` and `format: "json"`. It receives `{role, instructions, assignment}` on stdin; assignment includes the complete report, brief, sources and review dimensions. It returns this envelope on stdout:

```json
{"execution_id":"actual-provider-request-or-session-id","content":"original structured review response text"}
```

Commands come only from trusted startup configuration, never report contents or MCP arguments; use a fresh context per assignment. The HTTP adapter retains the original response and service request ID, rejects empty/truncated replies and does not follow redirects. Use a custom command for services with a different response protocol.

Generic entries may include `parameters`, for example `{"max_tokens":4096}`, for provider-supported output limits or reasoning options. They cannot override `model`, `messages` or `stream`, and remain part of the assignment binding.

### Self-review and Lite

`research_start` accepts `profile: "lite" | "full"`, default full. For Lite, `research_finish` returns the final checklist; complete each item with `{passed: true, evidence: "specific location and basis"}` and submit it as `checklist`. Review and full delivery gates are skipped with explicit logs; the brief, claims and section drafting remain required.

New Lite receipts use `schema_version: 2` and `input_hashes` to bind the task specification, source/claim registries, optional requirement ledger and declared local files of read sources, alongside the report and delivery message. Optional `evidence_files` on a checklist item binds retained check notes using task-relative paths. Missing, empty, escaping or workflow-output evidence files return an error before replacing a receipt. Text hashes normalize newlines; binary originals use exact byte hashes. The checker reports `input_binding_scope`; legacy receipts keep report/message-only checks. Hashes detect changed inputs, not whether an evidence explanation is correct or a remote page has changed.

Choose the profile from the brief and pass it explicitly when starting. For an existing task use `research_status(task)` to inherit its saved profile. Standalone `research_guide(stage, profile="lite")` returns the introduction and requested stage from the [compact Lite guide](../references/lite-workflow.md), without Full review or delivery instructions. File-reading agents use the same guide. The default remains Full for existing integrations.

Full `research_review` accepts `reviewer: "self" | "external" | "independent"`. The first self call returns the prompt, assignment and input_version. Explicitly switch to the reviewer role in the author context, then submit report_verdict, seven-dimension coverage, findings and input_version as self_review. Records retain the author context and degraded strength, never a fabricated independent execution. New tasks without a backend use this path automatically; explicit or saved independent requirements do not fall back.

### Recovery and acceptance

CLI, MCP and Python workflow operations share a local OS task lock. An overlapping operation on the same task fails promptly; wait for the current operation to finish. Different tasks remain independent. The empty `.research-toolkit.lock` file is retained, but OS ownership ends on release or process exit; do not delete it to force access. This coordinates cooperating local processes, not external editors or distributed filesystems.

Reviewer stderr with invalid UTF-8 is displayed with replacement characters and retained as exact bytes in `raw_output_base64`. Invalid UTF-8 in the actual response fails as `invalid_output_encoding`, with the original bytes retained; a completed call is not mislabeled as a launch failure.

Invalid configuration, a missing executable or a configured CLI's failed login blocks that route with guidance. Restore access in its actual environment. Unconfigured ordinary tasks can use self without login. The reviewer process does not automatically inherit the author agent's model access; keep credential files outside tasks.

Preserve original responses and failures. Do not rerun an unchanged valid negative response; unresolved necessary corrections block Full delivery. Record evidenced [no-change decisions](review-completion.md) for mistaken findings, then resume finish. After correcting an ordinary report, call `research_review` with `revision: true` to review the new version. This is the normal revision loop; already authorized corrections do not need another user confirmation. Reconcile changes to research scope in the task records first. A changed reviewer assignment also needs `revision: true`; frozen evaluations reject assignment changes. Timeouts remain 1–1800 seconds, default 600; a timeout-only change does not alter the assignment.

New review plans retain the exact reviewer and auditor instructions in `instruction_snapshot`. Resuming an unchanged assignment uses that snapshot even after the installed references change; completed valid reviews are reused and only unfinished work resumes. An explicit ordinary `revision: true` selects the current instructions and records any assignment change. Frozen evaluations still reject changed assignments. Legacy plans without a snapshot keep their existing version checks; the tool does not invent historical instructions or silently certify an upgrade as equivalent.

`reviews_complete` and `review_check` describe whether the declared reviews were completed; a negative review can count as completed. `delivery_ready` and the existing `completion_check` describe whether an ordinary report is ready for delivery verification. Its slot count excludes reviews with unresolved report defects. `open_issues` lists the findings, also reflected in progress and the next action. A completed review is not a passing report.

When saved progress claims completion, `research_status` checks the current delivery inputs and receipt. Failed checks return `progress.status: stale`, `delivery_check` and the original `recorded_status`; the query does not rewrite hash-bound progress or the historical receipt. Repair the findings and repeat the applicable review/checklist and finish steps before claiming current completion.

Additional audits apply only when declared; recovery completes only missing work. Timeouts clean up local processes without proving remote cancellation. The client must permit the necessary tool calls and wait long enough; avoid concurrent writers for one task.

## Skill only and CLI fallback

For Skill-only use, follow the [installation guide](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README.md). The agent carries out the methods with its own capabilities; installing instructions alone does not start MCP or automatically run reviews.

The plugin also includes a dependency-free workflow CLI. It uses the same implementation; only starting MCP requires the SDK:

```bash
python3 scripts/research_workflow.py start --workspace /path/to/tasks --request brief.json
python3 scripts/research_workflow.py review --workspace /path/to/tasks --request review.json
```

CLI requests are JSON objects supplied by `--request` or stdin. Missing/unknown argument errors name the action, fields and input method before creating or changing a task. A source/claim validation error names its CSV, record ID and missing fields; repair that record and repeat the same operation. Guide languages are `en` and `zh`. Commands return JSON and a nonzero exit code on failure; no new user confirmation is required to fix an already authorized task.

A brief request is `{"task":"comparison","language":"en","brief":{"question":"...","audience":"...","scope":"...","output":"...","depth":"...","evidence_standard":"..."}}`. Review arguments include `task`, task-relative `evidence_paths`, optional `artifact` (default `final.md`) and `purpose`. The `status`, `guide`, `check-draft` and `finish` actions mirror MCP arguments. `check-draft` takes `task` and optional `artifact`, needs no delivery message and exits 1 on a failed check. JSON may also be supplied through stdin.

### Reuse task files and retain a self-review packet

Use the existing task directory as the working location for reports, notes and sources. Pass `artifact` and `evidence_paths` relative to it; tools read those files directly. Retain the first draft before revising, and export the final report when delivering. Additional copies solely for each tool call are unnecessary.

Set the task directory below to the location returned by `start`, and use the same task ID in the request. For an existing Full task named `comparison`, after preparing its report and source/claim records, save this request as `review.json`. Replace `source.md` with the actual evidence paths. Use this self-review example only when that is the selected tier; an independent requirement keeps its configured backend.

```json
{"task":"comparison","reviewer":"self","artifact":"final.md","evidence_paths":["source.md"],"include_assignment":false}
```

This local example returns `prompt`, `input_version`, `task_directory` and `assignment_ref` (relative path and text SHA-256); the complete frozen input remains in the task. Omit `include_assignment` or set it to `true` when the caller needs the full assignment in the response. The default and external/independent input delivery are unchanged. Retain the response by running this Python snippet from the repository/plugin root using the same interpreter as the CLI. `start` already created `logs`; `reviews` may not exist before review. Shell redirection opens its destination before the CLI runs.

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

Opening with `x` refuses to overwrite an existing record before invoking review. For a genuinely new attempt use a new filename; retain a failed attempt's output and error. If the unchanged packet was already saved successfully, use it instead of calling review again.

Read `prompt` and `input_version` from the saved response, then the complete frozen assignment at `Path(task_directory) / assignment_ref["path"]`; its text hash uses canonical LF newlines. If `assignment` is returned inline, use it directly. A local file reference is useful only when the caller can read that task directory. In same-context self-review, verify the current report and requirement/source bindings, reuse unchanged evidence already read, and revisit changed or questioned material. Keep the complete packet; a separate reviewer receives the full required input. Submit the actual judgment as `self_review` using that `input_version`; see the [self-review fields](review-completion.md). After report or review-input changes, use the existing `revision: true` path. Reuse avoids duplicate copying, not current-version checks or required reading.

## Verification and limits

The repository checks the shared workflow, package/source consistency and a real MCP stdio connection with **synthetic** reviewer subprocesses. Those tests do not call paid models or establish report quality. The implementation launches real configured model executors in normal use; a successful installation or test is not evidence that a particular research report has been reviewed.

A separate [guided real-model check of plugin `0.1.2`](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/evaluation-status.md#current-implementation) completed review and audit recovery on one real task using fictional source material while preserving a negative result and correctly blocking delivery. It required configuration and audit-contract corrections; it does not establish unattended reliability.

The tools enforce their own completion conditions. They cannot prevent an agent from ignoring tools or editing files outside them, and they cannot mechanically certify factual truth. Acceptance follows the selected profile and reviewer tier; independent review is required only when declared.

For failed drafts, follow the [repair and stopping rules](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/failure-handling.md). Correct ordinary report versions, preserve frozen evaluation originals, and never repeat an unchanged valid negative judgment until it passes.
