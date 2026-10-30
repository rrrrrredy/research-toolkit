# Usage and integration

[English](usage-modes.md) | [简体中文](usage-modes.zh-CN.md)

The [compatibility policy](compatibility.md) explains the current completion contract and continuation of older tasks. Preserve original records and reuse the existing materials.

**Use the research methods through a repository link, files, attachments, or pasted text.** Choose the input method your agent supports. Native Skill, plugin, and MCP support are separate capabilities of the host.

## Use the research methods

- **Repository link:** send the [research request](https://github.com/rrrrrredy/research-toolkit/blob/main/README.md#usage) to an agent that can read GitHub.
- **Files or attachments:** download the repository, provide `SKILL.md`, and make the required reference files available.
- **Text-only input:** paste the complete entry instructions and relevant method sections. See [chat-only use](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README.md#chat-only-use).
- **Native Skill:** install the complete toolkit through the host's supported mechanism. See [agent setup](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README.md).

No Python or vendor CLI installation is required merely to read and apply the methods. Retrieval and file access come from the author agent. A separate reviewer is needed for independent review; supplying the instructions does not run one automatically.

## When to use each tool

**Use the [single research entry](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/quickstart.md).** Agents load methods for their work and complete independent review, audit and acceptance. CLI/MCP are optional; omit `profile` in new requests.

The table applies when you choose the managed local workflow, through MCP **or the [shared CLI](#skill-only-and-cli-fallback)**. Skill-only use keeps the same research and independent assessment responsibilities without creating these registries or receipts.

| Tool | When it is needed | When you can skip the call |
| --- | --- | --- |
| `research_start` | Create a new managed task and its brief using the complete methods, without a profile choice. | Resume an existing task with `research_status`, or apply the Skill directly without a managed task. |
| `research_save` | Save/update sources, claims, requirements and drafts; correct located format errors. | No record or draft changes. |
| `research_status` | Resume a managed task, inspect saved progress, or change its recorded stage. | You do not need to read or update progress; a methods-only session can use its own notes. |
| `research_guide` | Retrieve the method for a stage when it is not already available in context. | Read the relevant `SKILL.md` and `references/` files directly. |
| `research_review` | Prepare native-host review, audit and acceptance assignments; retain real responses and bound inputs. | Reuse valid complete results for unchanged inputs; continue unfinished work. |
| `research_check_updates` | Read a registered public release log and locate affected claims/report passages. | No new-source question or no registered release log. |
| `research_check_draft` | Check current draft records and explicit length bounds without model calls or a delivery receipt. | Optional before review/finish; inspect sources and meaning separately. |
| `research_finish` | Complete a managed task by checking the current report and its delivery requirements. | For Skill-only use, complete independent review, audit and acceptance and deliver the requested report and citations; no tool receipt is required. |
| `research_check_reviewer` | Diagnose configuration and dependencies for an explicitly selected external backend. | Host-native subagents need no external service configuration check. |

## Save research records and drafts

Optional `requirements[].unit_ids` records an explicit assignment to research units, for example `["domestic"]`; omit it or use `[]` for global requirements such as audience, overall scope and format. Unit IDs follow the same format as `draft.unit_id`. Preserve the actual instruction; do not turn a global requirement into a local one merely because one agent handles it. `work.requirement_ids` selects records to read, not their applicability.

The agent uses `research_save` (CLI: `save`) to save source, claim and requirement objects. Users describe the research and make scope/use decisions; they do not manage CSV, IDs or review-response JSON. The tool merges partial updates by ID, retains other rows/columns, and writes the existing CSV/JSONL formats. If an ID is omitted, it matches a unique URL/claim/summary or assigns an ID and returns it. Use that ID for later edits. The agent still reads sources and supplies accurate content.

For required reading, `requirements[].reading_requirement` specifies `full_text` or `relevant_sections`; `sources[].read_scope` records what was actually read and cannot replace it. An active mandatory-reading requirement needs both `reading_requirement` and `required_source_ids` after merging with its saved row. `required_source_ids` is a nonempty list of distinct source IDs, such as `["S1"]`, referring to source records. Partial updates may omit already-saved fields; requirements without mandatory reading need neither field.

For a local file, prefer `read_evidence: "sources/S1.md"`, a task-relative path to an existing nonempty file. Put page/section locations, reading scope and notes in the existing `locator` field, for example `"pp. 2-4; relevant sections only"`, rather than appending prose to the path. URL/page locators and already-supported local-reference forms remain valid. Optional `evidence_path` still locates local UTF-8 source text when needed; it does not replace or repair an invalid `read_evidence` value.

Example request for the agent, after saving the source text in the task directory:

```json
{
  "task": "example",
  "sources": [{"source_id":"S1","title":"Source title","url":"https://example.org/source","source_type":"primary","read_scope":"relevant_sections","read_evidence":"sources/source.md","locator":"pp. 2-4; relevant sections only"}],
  "claims": [{"claim":"The source-backed finding","claim_type":"fact","supporting_sources":["S1"]}],
  "requirements": [{"summary":"Read the relevant sections of S1 and explain the comparison","status":"pending","reading_requirement":"relevant_sections","required_source_ids":["S1"]}],
  "draft": {"path":"first-draft.md","complete":true}
}
```

Omit a collection when it does not change. `draft` may include `content` to write the report and create its parent directory; omit content to register an existing UTF-8 file without copying it through the conversation. `complete: true` records that the agent has saved a complete draft, not that its quality passed. A partial update such as `{"requirements":[{"requirement_id":"R1","status":"satisfied","evidence":"final.md, comparison section"}]}` preserves the other fields; it does not invent evidence or automatically close work.

```bash
python3 scripts/research_workflow.py save --workspace ../research-work --request save.json
```

Format errors identify the collection, row and field. The agent fixes those inputs and retries; the whole request is validated before records are replaced. To recover a malformed existing collection, send its complete recovered rows with, for example, `"replace":["sources"]`. The tool preserves the original bytes under `logs/record-backups/`. This is explicit replacement, not silent removal of unparsed rows. Saved input changes continue to invalidate earlier checks normally.

Explicit `research_status(task, stage="analyze")` or `stage="draft"` calls return saved supplemental requirements as JSONL text in `requirements`, retaining their statuses and handling evidence. The agent can use them directly in analysis and drafting without copying them into the brief. The field is omitted when no requirements exist; ordinary status queries do not include the text. Returning a requirement does not establish that the research satisfies it.

`research_status` recovers work and artifact references from saved activity. Event times identify the sequence of saves and handoffs; they are not research deadlines or optimization targets. Original execution evidence is retained when review results are recorded.

`save` and `status` return `changes` for the latest successful record-save batch: added, updated, unchanged, removed or recovered IDs, related claims, and line/heading locations in the latest registered draft. Source associations include `supporting_sources` and the exact registered IDs in `counter_evidence`, using the same whitespace/semicolon/comma/`|` separators as review inputs; free-text counter-evidence is not interpreted as a link. Registered release-log queries reuse these associations. Locations are literal claim-text or source-link matches and may point to a citation paragraph or bibliography; a paraphrase can be found through its citation, while `not_located` means inspect manually, not no impact. Use them to read relevant passages and verify sources before deciding which conclusions to revise; claims are not automatically invalidated.

Each matched location also returns `text` (the matched line). The first occurrence of a context returns `context` with `start_line`, `end_line` and original `text`: the matched paragraph and up to one adjacent paragraph on each side within the same section. Later locations with exactly the same report, line range and original text return `context_ref: {"claim_id": "C1", "line": 7}` instead of repeating `context`; this points directly to that claim's location with an inline context in the same `affected_claims` list. All claims, source associations, match reasons, headings and matched line numbers remain on their respective entries. Equal text at different positions stays separate. Blank lines separate paragraphs; `#` headings bound the context. Line numbers are one-based and inclusive. Registered release-log queries use this same location output. No extra input fields or calls are needed, and the report is not modified.

After changing local source text, save its ID (for example `{"sources":[{"source_id":"S1"}]}`) to compare evidence-file hashes with the previous save observation, without resending other fields. First observations are explicit and say nothing about earlier changes; old tasks need no migration or reconstructed history. Remote pages are not monitored. Byte-identical files are not rewritten and `updated_files` lists actual writes; status is read-only. Registering only a new draft keeps the latest record batch and refreshes its body locations; the next record save replaces that summary. This is not a backlog or a new completion requirement.

### Task record fields

Keep the agreed brief and outline in `state/task_spec.md`. Record substantive follow-up requirements with stable IDs in `state/requirements.jsonl`; closure and explicit scope decisions follow [requirement records](delivery-verification.md#requirement-closure-and-reading-records).

`progress.json.stage` uses `brief`, `collect`, `analyze`, `draft`, `review`, `revise`, and `final`.
`progress.json.status` accepts `in_progress`, `paused`, `blocked`, and `complete`.

Record the actual stage, unresolved issues and next action. On resumption, retrieve the specification, effective requirements, outline, current main draft and related analysis through `status`. Paths in calls are relative to the task directory. Stage names describe the work; real dependencies determine what can proceed.

Keep `state/findings.jsonl`, `state/directions_tried.json`, `state/iteration_log.jsonl` and `logs/work.jsonl` only when useful to the task; they are not universal deliverables. Uncertainty can stay with claims, with `data/uncertainty_registry.csv` optional. Field conventions are in the existing [workflow reference](../references/research-workflow.md#3-state-system).

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

Release-log requests normalize the hostname and require every resolved address to be public. Connections use those checked addresses while preserving hostname-based HTTPS verification. This call connects directly without environment/system proxies, whose target resolution cannot be checked locally; environments requiring a proxy return a reading failure if direct access is unavailable.

The call does not overwrite evidence or change reading status, conclusions or delivery records. Changed results include `current_excerpt` for the agent to read, save separately and register through the existing `research_save` flow. Until adopted, another call still compares against the old evidence. Retry the same request after resolving a network failure.

## Continue existing research

Provide the report, relevant sources and intended use. Reuse existing material and notes without first reconstructing a tool ledger. Starting from a question remains supported. Two adjacent requests are:

```text
Use Research Toolkit to check this report against the related sources,
focusing on important problems that change a conclusion or action.
Preserve the original, locate each issue and its evidence, make the necessary
minimal revision, check the result, and return a short change note.
Do not rewrite for optional style preferences.
```

```text
Update this research with the new material. Explain which facts are outdated,
which judgments change and which still hold. Preserve source dates and versions.
Update affected passages, sources and claims; reuse unaffected research.
Deliver the revised report and change note, refreshing checks invalidated by the changes.
```

When continuing a CLI/MCP-managed task, start with `research_status(task)` and preserve the previous report. Keep existing source, claim and requirement IDs and their reading evidence. Use `research_save` to update only affected records together, registering the saved draft by its existing path; unchanged records need no resubmission. After actually checking a requirement, save its status and concrete evidence with the relevant update. Recheck changed or questioned source sections; reuse still-valid local evidence without fetching it again. Complete the current report’s independent content reviews, audit and acceptance before claiming completion. See the [executed long-report update](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/case-study/coding-benchmark-update/README.md) for preserved materials, source-confirmed changes and revisions.

### When content or sources change

The following calls apply to CLI/MCP-managed tasks.

| Change | Reuse and recheck |
| --- | --- |
| Resume interrupted work with unchanged inputs | Read `research_status` and continue unfinished work; completed valid reviews can be reused. |
| Report, requirements, bound sources or claims change | Update affected analysis. Earlier checks do not approve the current version; use `revision=true` for required reviews and delivery checks of current inputs. Historical receipts remain unchanged; continued work uses the current completion contract. |
| A source webpage changes but the saved text does not | Tools do not monitor remote pages. The agent reads and retains the new version, explains its date and effect, then handles it as changed input. |

The formal checks establish version and record consistency within the declared scope, not source credibility. The private-chat-citation advisory in `research_check_draft` scans only the supplied report and ignores code examples; it changes neither `ok` nor historical receipt meanings. Repair citations from actual sources; reading and review still establish semantic support.

## Optional workflow tools

Use local MCP when the host can start a local process, or the bundled plugin when it supports the plugin format. The tools use the same research methods.

| Form | What it supplies | Host requirement |
| --- | --- | --- |
| Skill | Entry instructions and detailed research methods | Native Skill discovery or explicit file reading |
| Plugin | Skill, references, and the local MCP server in one package | Support for the package format and local stdio MCP |
| MCP | Nine callable tools for task setup, progress, guidance, reviews, and delivery checks | A client that can start and call a local stdio MCP server |

The shared CLI needs Python 3.10+ and only its standard library. Prefer `python3` on Linux; any installed Python 3.10+ interpreter is enough. MCP also needs the dependency in `requirements-mcp.txt`. Research and independent review use host-native agents by default. Separate backend configuration is optional and does not determine whether the host can delegate.

CI exercises the CLI and packaged MCP workflow on Python 3.10/Linux, plus the broader checks on Python 3.12/Linux and Windows. Use the same interpreter for dependency installation and your client's server command. These are server/protocol checks, not tests of every client GUI.

## Install the plugin

The [plugin directory](https://github.com/rrrrrredy/research-toolkit/blob/main/plugins/research-toolkit/) bundles the Skill, methods and local MCP server. Use your host's supported plugin installation mechanism; [agent setup](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README.md) has host-specific instructions. Install `requirements-mcp.txt` in the Python environment that starts MCP, then confirm the nine `research_*` tools are available.

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

Restart the client and confirm the nine `research_*` tools appear. The [executable example](https://github.com/rrrrrredy/research-toolkit/blob/main/examples/mcp/README.md) explains the local request contract using clearly labelled synthetic inputs; historical real runs retain their original scope.

Official configuration references: [Claude Desktop local servers](https://modelcontextprotocol.io/docs/develop/connect-local-servers), [Cursor MCP](https://cursor.com/docs/mcp), [Codex MCP](https://developers.openai.com/codex/mcp). Cursor supports project `.cursor/mcp.json` or global `~/.cursor/mcp.json`; Codex uses `~/.codex/config.toml`. In Claude Desktop, open Settings → Developer → Edit Config.

If no tools appear, run `python -c "import sys, mcp; print(sys.executable)"` with the configured interpreter. An import error means the MCP dependency is missing from that environment. Use absolute script/workspace paths and restart the client. Server startup and protocol calls are exercised by `python3 scripts/check_mcp_contract.py`; that offline check uses synthetic reviewers and does not establish GUI compatibility or research quality.

## What happens during a task

| Tool | Action and completion boundary |
| --- | --- |
| `research_start` | Create the unified task and brief, returning shared context and consequential missing fields |
| `research_status` | Returns saved progress and current methods; changing to analysis/drafting requires prerequisite source/claim records |
| `research_guide` | Loads the applicable methods without starting a task; supports English and Chinese |
| `research_review` | Connect content review, independent audit and final acceptance, retaining native-host originals and version bindings |
| `research_check_draft` | Return current counts, declared range checks and record errors without changing task state; `ok` does not certify content or delivery |
| `research_finish` | Checks the reviewed artifact, evidence, unresolved requirements and delivery text before writing completion state and a receipt |
| `research_check_reviewer` | Diagnose an optional external backend, without gating native-host collaboration |

Research and assembling agents search, read, analyze and write using their host tools and shared task inputs. It must save required source texts and source/claim records in the task directory. Stage guidance reduces repeated context loading; it does not establish that a model has obeyed every instruction.

Before analysis, source records need an ID, title, locator and source type, with at least one full-text or relevant-section reading record and a reading-evidence reference. Before drafting, claims need substantive text and a type; source references must resolve to registered, read sources. Explicit hypotheses may remain unsupported with recorded uncertainty, but at least one grounded claim is required. Local file references in reading evidence must stay inside the task directory and identify an existing, nonempty file; anchors and page/section suffixes are allowed. URLs and section/page locators remain valid references without an automatic content check. These checks detect incomplete records, not whether a source was truly understood.

When `status` also receives `work`, analysis/drafting checks use that selection's sources and claims, including its declared upstream inputs. Unrelated unfinished branches do not block it. A unit can develop its analysis from selected sources before registering new claims; whole-report review and delivery still check the complete task and its claim evidence.

Reviews automatically include nonempty `state/requirements.jsonl` alongside the brief, report and source files. Both reviewer and auditor receive the full ledger, including later clarifications and changes. Editing or deleting that ledger after review prevents delivery until the changed assignment is addressed. An empty ledger adds no requirements.

Reviews retain the full task, report and relevant source files, not just URLs. Native-host assignments return readable file references by default. If the material exceeds one model context, the reviewer reads the retained originals in parts and completes the assigned assessment; a summary must not silently replace required material.

## Reviewer backends

### Native host review

Use the subagent capability already present in Codex, Claude Code or the chosen host. `research_review` prepares assignments and binds the complete task, report and original evidence. The host starts a different independent agent for each base perspective and the relevant domain review; it then runs independent audit and final acceptance. The author and assembling agents do not fill these assignments. No API configuration is needed for this route.

The seven base perspectives are requirements, evidence, adversarial reasoning, structure and depth, reader usefulness, process language and natural expression. They are separate review contexts. Models may be the same; context and production responsibility must be distinct. The [review contract](review-completion.md) specifies the assignments, original results and current-version completion.

The host preserves each actual response and its execution record, then submits their paths through the existing `review` operation. Once the required content results exist, the next assignment is independent audit; final acceptance follows the resolved report and audit. If a task needs an early review of a research unit, identify that unit. Its result supports dependent work and does not replace full-report review.

### Optional configured execution

Use this only when choosing a separate command or endpoint to execute review. It is not the setup for native host subagents.

| Backend | Configuration |
| --- | --- |
| `codex` | `RESEARCH_TOOLKIT_REVIEW_BACKEND=codex`; uses the installed, signed-in CLI. Optional `RESEARCH_TOOLKIT_REVIEW_MODEL`. |
| `claude` | `RESEARCH_TOOLKIT_REVIEW_BACKEND=claude`; uses the installed CLI and its existing configuration. |
| `generic` | Backend `generic`, `RESEARCH_TOOLKIT_REVIEW_BASE_URL` and `RESEARCH_TOOLKIT_REVIEW_MODEL`; an authentication environment variable only if the selected endpoint requires one. |
| Trusted command | `RESEARCH_TOOLKIT_REVIEW_CONFIG` points to a JSON configuration with an argv list and `format: "json"`. |

Native-host and configured execution fulfill the same current review responsibilities. A legacy self-review result remains historical evidence; it cannot replace a required independent review, audit or acceptance.

For a chosen generic backend:

```bash
export RESEARCH_TOOLKIT_REVIEW_BACKEND=generic
export RESEARCH_TOOLKIT_REVIEW_BASE_URL=https://your-provider.example/v1
export RESEARCH_TOOLKIT_REVIEW_MODEL=your-model
python3 scripts/research_workflow.py check-reviewer
```

Use `$env:NAME = "value"` in PowerShell. Credentials stay in the runtime environment, not task files. `check-reviewer` diagnoses local setup; it is not a model invocation. The generic route uses `/chat/completions`, HTTPS for remote endpoints and HTTP only for localhost/literal loopback addresses. Requests contain the research material and follow the chosen endpoint's access policy.

Trusted commands receive `{role, instructions, assignment}` on stdin and return:

```json
{"execution_id":"actual-provider-request-or-session-id","content":"original structured response text"}
```

Keep each task in a separate context and retain original output. Command configuration comes from trusted startup configuration, never source text or a report. HTTP responses retain request IDs; empty or truncated responses remain incomplete. Provider-specific `parameters` may be supplied deliberately, but cannot replace `model`, `messages` or `stream` and are bound to the assignment.

### Recovery and acceptance

CLI, MCP and Python operations share the existing OS task lock. Serialize writes to the same task; branch work can proceed independently. Do not remove the lock file to bypass ownership. The designated main-draft owner integrates branch artifacts instead of multiple writers editing the same report.

Preserve failed calls and original bytes. Invalid UTF-8 in a response is retained as a failure; stderr can be displayed with replacement characters while its bytes remain available. A host cancellation or execution failure leaves that assignment unfinished. Resume the missing work after resolving its actual cause; do not cancel substantive work because it has run for an arbitrary duration.

A valid negative review is retained. Correct the affected report and evidence, then use `revision: true` for the current version. Authors can respond to a disputed finding, but an independent reviewer/auditor adjudicates consequential no-change decisions. Do not rerun unchanged negative results looking for a pass.

Instruction snapshots, original input files and input versions remain available through revision. Unchanged completed results can be reused; changes to the report or its required inputs must be addressed by the relevant review and final whole-report acceptance. When status finds a stale historical receipt, it reports that condition without rewriting the original completion record. See [review completion](review-completion.md) and [compatibility](compatibility.md).

## Skill only and CLI fallback

For Skill-only use, follow the [installation guide](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README.md). The agent carries out the methods with its own capabilities; installing instructions alone does not start MCP or automatically run reviews.

The plugin also includes a dependency-free workflow CLI. It uses the same implementation; only starting MCP requires the SDK:

```bash
python3 scripts/research_workflow.py start --workspace /path/to/tasks --request brief.json
python3 scripts/research_workflow.py review --workspace /path/to/tasks --request review.json
```

CLI requests are JSON objects supplied by `--request` or stdin. Missing/unknown argument errors name the action, fields and input method before creating or changing a task. A source/claim validation error names its CSV, record ID and missing fields; repair that record and repeat the same operation. `start`, `status` and `guide` (and their MCP tools) accept `language: "en"` for English, or `"zh"` / `"zh-CN"` for the same Chinese methods. Unsupported values name the `language` field and accepted values before task records are written or the stage changes. Commands return JSON and a nonzero exit code on failure; no new user confirmation is required to fix an already authorized task.

A brief request is `{"task":"comparison","language":"en","brief":{"question":"...","audience":"...","scope":"...","output":"...","depth":"...","evidence_standard":"..."}}`. Review arguments include `task`, task-relative `evidence_paths`, optional `artifact` (default `final.md`) and `purpose`. The `status`, `guide`, `check-draft` and `finish` actions mirror MCP arguments. `check-draft` takes `task` and optional `artifact`, needs no delivery message and exits 1 on a failed check. JSON may also be supplied through stdin.

<a id="reuse-task-files-and-retain-a-self-review-packet"></a>

### Reuse task files and retain a review packet

Keep reports, analysis and source originals in the task directory. `artifact` and `evidence_paths` address those files directly. Preserve the first draft and subsequent revisions; do not create a new material copy just to invoke another tool.

For an existing managed task:

```json
{"task":"comparison","artifact":"final.md","evidence_paths":["sources/source.md"],"include_assignment":false}
```

```bash
python3 scripts/research_workflow.py review --workspace ../research-work --request review.json
```

With native-host execution, the result identifies pending assignments and their retained input files. Each worker must be able to open the full assignment and referenced originals; across environments, transfer readable content rather than inaccessible local paths. Preserve the real host task ID and the complete original reply and execution record. Submit those records through the same operation using `host_result`; the [review contract](review-completion.md) describes its fields.

The host continues the returned assignment, audit or acceptance work. A summary locates an existing result; it does not replace the result or source text. If the report or required inputs change, retain the earlier packet and use `revision: true` for the new version.

## Verification and limits

Existing software checks exercise record consistency, original-input binding, packaging and MCP transport with labelled synthetic data. Real host executions retain their separate source material, responses and outcomes. The [evaluation status](evaluation-status.md) describes the work actually observed; installation and mechanical checks are not content-review results.

Current delivery requires independent content review, audit and acceptance. The tools enforce their saved contract; the agents perform the substantive reading and judgment. Preserve historical receipts and report their actual contract rather than presenting them as current acceptance. For actual failures, follow the [repair guidance](failure-handling.md) and continue the affected work.

## Current artifact and scope updates

Optional `research_save.brief` updates only supplied question/audience/scope/output/depth/evidence_standard fields and synchronizes the specification with progress.brief. Save affected requirements together where practical; no second scope ledger is needed.

```json
{"task":"comparison","brief":{"output":"A revised comparison report"},"draft":{"path":"drafts/revised.md","main":true,"kind":"report","host_task":"actual-main-writer-host-task"}}
```

`draft.main=true` explicitly selects the current work file; optional kind is report/comparison/review/analysis. Other chapter/reference saves do not change this selection. `complete` still records draft completeness only. `save/status.current_work` returns the current file, effective requirements, unfinished work and resume paths; status separately references the last delivery. A new main or changed brief cannot inherit a terminal state; old receipts remain intact. Review/finish must pass the registered main as artifact. Legacy tasks need no migration and retain previous behavior without an explicit main. The saved file observation is not approval.

`start/status.runtime` identifies the implementation path, version, code hash and available entry hash; host_loaded_entry=not_observed. It does not infer which Skill the host read. Tools identify registered files, not arbitrary new directories.

Reading requirements are validated at save: full_text/relevant_sections paired with a nonempty distinct required_source_ids list. Partial updates to a valid existing pair remain supported. Invalid batches cannot partially overwrite reports or state. See [task continuity](../references/task-continuity.md) for the workflow.

## Historical task compatibility

Saved 1.x tasks, reports, input snapshots and receipts remain readable with their original identities and declared completion results. Historical `profile` and `self_review` fields do not create a second research entry or satisfy current independent responsibilities.

Continue existing material in the same managed task: retrieve its current work, preserve the previous report and receipt, and prepare a current-version review when completing the continuation. Reuse valid sources, analysis and original reviews; complete the roles and content still needed under the current contract. Do not rewrite an old self-review as independent execution or reconstruct missing reviews. See [version compatibility](compatibility.md).

## Research delegation and handoff

The outline and original requirements stay in the existing task specification. Assign meaningful research units and their actual dependencies; keep domestic/overseas coverage or other required dimensions visible even when work is split by technical problem.

Use `status` to prepare the next worker's input. This illustrative request assumes its referenced unit and records already exist:

```json
{"task":"study","methods":["compare","delegate"],"work":{"unit_id":"route-comparison","question":"Which technical differences change the choice?","depends_on":["route-evidence"],"requirement_ids":["R2"],"claim_ids":["C1"],"paths":["reports/current.md"]}}
```

All `work` fields are optional. A new `unit_id` can name the assignment before its first save. Selected claims bring supporting and registered counter-evidence sources, and reading requirements bring their sources. For a saved unit, its full artifact and inherited original inputs are returned; dependencies bring upstream full outputs and originals. `work_context` includes the task, effective requirements, selected records, readable `files`, binary-original references, dependencies and their readiness, `inputs` and `input_version`.

Satisfied requirements stay in `effective_requirements` when still applicable. `scope_decisions` retains explicit waivers, exclusions and accepted limits. Requirements are not automatically inferred from host conversations; save the actual user wording and affected requirement through the existing fields. `applicable_requirements` includes global requirements plus those explicitly assigned to the current unit or its real upstream units (`requirement_unit_ids`); all effective requirements remain visible. Input bindings follow that scope, so unrelated local requirement or source/claim changes do not invalidate the unit. Without a `unit_id`, requirements are bound task-wide. Historical `record:requirements:effective` bindings keep their task-wide meaning; copy new `inputs` unchanged when continuing work.

Send the returned question, requirements and accessible originals through the host's subagent tools. Keep the actual host task/session reference. The host owns startup, messages, waiting and cancellation. Toolkit does not create a second agent runtime.

A worker saves a result through `save`:

```json
{"task":"study","draft":{"path":"analysis/routes.md","kind":"analysis","unit_id":"route-comparison","question":"Which technical differences change the choice?","depends_on":["route-evidence"],"host_task":"actual-producing-host-task-id","complete":false,"handoff":{"summary":"Comparison developed; the deployment assumption still needs resolution.","pending":["Resolve the deployment assumption against the original requirement."],"decisions":["Use the same workload and quality measure for both routes."]}}}
```

Omit `content` to register an existing nonempty file or supply it to save text. Copy `work_context.inputs` into optional `draft.based_on` rather than inventing hashes. `complete` describes the saved unit or draft, not whole-task delivery. A dependent unit cannot be completed while its upstream registered work is incomplete, changed or awaiting required independent review; save the in-progress work with `complete: false` and resolve the dependency.

`current_work.work_units` and `research_outputs` recover registered units, their original snapshots, host references, handoffs and changed inputs. They share the existing activity log, not a second task board. The handoff summary, `pending` and `decisions` are navigation; the next researcher, assembling agent or reviewer can read the full artifact and original sources. The same agent can resume its next phase through these records.

The review packet's `production_history` retains saved production records, handoffs and original draft locations for the selected artifacts. Existing snapshots are bound to the review input; appending review activity does not itself change that version. Missing historical stages are not reconstructed. When the task requires progressive research or writing, structure-and-depth review and audit use these originals to inspect the actual development, rather than treating save counts as completion evidence.

Use `draft.main: true` only for the designated main draft. Its saved `host_task` is the writer; other branches remain separate artifacts. To transfer writing responsibility, the current owner saves `handoff.to` with the receiving host task/session. Merely changing `host_task` cannot seize the main report or an owned unit.

Preserve each saved unit version. New requirements or evidence return to affected analyses and the outline before relying on the revised result. `changed_inputs` identifies changed bindings, not automatic invalidity of the research conclusion. Unit review uses its `unit_id` as `review.scope`; final review, audit and acceptance still cover the complete current report.

Unit readiness also checks its review inputs and original replies, including originals supplied separately through `review.evidence_paths`. If these change, both `status` and downstream `save` treat the unit as awaiting current review; unaffected branches retain their state.

Full-report review retains the original requirement rows and binds their meaning and applicability. After independent review, audit and acceptance actually finish, save the factual completion status and evidence, then call `finish`; that bookkeeping alone does not invalidate the results. Changes to requirement content or scope still require current review, and the final receipt records the current requirements file.
