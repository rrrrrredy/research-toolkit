# Usage trajectories and data

English | [简体中文](usage-data.zh-CN.md)

Toolkit's executable entry points send basic usage events by default to understand installation routes, operation sequences, failures and recovery. The first run displays a notice; collection can be disabled at any time. Prompts, conversations, research titles, reports, source URLs, local paths and credentials are excluded by default.

## How installation connects collection

| Mode | Automatic observation | One-time setup |
| --- | --- | --- |
| CLI | Existing command starts/results, saves, prepared input, reviews and execution records | Use a version containing the collector |
| MCP | The same implementation as CLI, labeled MCP | Use a service version containing the collector |
| Plugin | Bundled MCP events; session events where the host supports and trusts hooks | Install the plugin and complete host hook trust |
| Skill only | A host observer captures actual invocation and tool order; the agent does not manually report each action | Install the observer below in the working project and trust it in the host |
| Reading a link, pasted instructions, or a chat interface unable to execute an observer | No executable component, so no automatic upload | Research methods remain usable |

All executable paths share one event format, local queue and receiver. No separate user account or per-task file upload is needed for basic events. Older releases without the collector do not upload retrospectively. A download that is never used is not an observed active installation.

Run once from the complete downloaded repository or plugin directory, replacing the absolute project path. Select the actual host: `claude`, `opencode` or `codex`.

```sh
python scripts/install_usage.py --host claude --project /absolute/path/to/project --channel github-clone --form skill
```

Use an installed Python 3.10+ interpreter; an absolute interpreter path works on Windows. Set the actual channel to `github-clone`, `github-release`, `plugin-marketplace` or `manual`, or `unknown` when unavailable. Form accepts `skill`, `plugin`, `cli` or `mcp`. This installs observation, not a new research step or method. Do not also install project hooks when the plugin already supplies its own active hooks.

The installer preserves other settings and backs up changed files. Claude Code uses project `.claude/settings.local.json`, Codex `.codex/hooks.json`, and OpenCode `.opencode/plugins/research-toolkit-usage.js`. The host retains responsibility for trust and permissions. Add `--remove` to the same command to remove this observer.

## Recorded fields

Basic events contain version, OS category, host, entry point, install channel/form, time, operation category, success/failure/pending outcome and tool-call duration. Tasks, sessions, child agents, calls and research units use keyed local identifiers; original names and paths are not uploaded. An installation identifier belongs to the local data directory, not a verified person.

CLI/MCP call counts come from the shared executable entry. Host observations separately cover user turns, known method-file reads, tool use, child-agent start/stop and session compaction; they are not added again as Toolkit calls. Method observation recognizes known method names without uploading arbitrary paths. The observer activates only sessions explicitly invoking Toolkit and their children. Later actions in an activated session are session-level observations, not evidence that every action belongs to the same research task. Events without a confirmed task relationship remain unlinked session events.

The observer does not scan unrelated past sessions, browser history or complete transcripts. Basic data can reveal repeated operations, failures and recovery, but cannot explain user intent or establish report quality. An agent stopping is not research delivery; absent later events do not establish abandonment. Only a successful `finish` delivery result counts as a completed tool-managed task.

## Inspect, disable and delete

```sh
python scripts/usage_events.py status
python scripts/usage_events.py off
python scripts/usage_events.py on
python scripts/usage_events.py delete
```

`off` disables recording/upload for this local user and clears pending queues; research continues. Alternatively set `RESEARCH_TOOLKIT_TELEMETRY=off` before starting the host, CLI or MCP to suppress recording/upload in those processes. An environment setting does not change other already-running processes. A request sent before disabling may still be in flight; deletion removes data already received.

`delete` removes this installation's uploaded data; add `--task-root /absolute/path/to/task` for one task. Old private report copies are cleared on the next report refresh. To stop future data as well, run `off` before `delete`.

The local queue defaults to `~/.research-toolkit/usage/`, retaining at most seven days and 10,000 basic events. Uploads run in the background; failures retain pending data for a later use to retry. Research calls do not wait for network transfer. `status` shows last upload and safe error categories. `RESEARCH_TOOLKIT_USAGE_HOME` selects another local directory. CI is disabled by default; explicit acceptance traffic has `test=true` and is separated from actual-use statistics.

## Share selected research content once

Only after the user explicitly authorizes the selected files for this task, the agent or user can run:

```sh
python scripts/usage_events.py share --task-root /absolute/path/to/task --file final.md --file notes/change-note.md --confirm-content
```

Authorization covers only those selected files. Future additions and edits are not automatically shared. Each UTF-8 file must be inside the task directory and at most 1 MiB; a packet is at most 2 MiB. Check the selected files for personal, client or confidential information the user does not want to share. The program does not scan the entire task directory or treat one approval as permanent consent.

## Maintainer access

Events go to a private receiver managed by the project maintainer; detailed records are retained for at most 90 days. The maintainer views aggregates, task sequences and private attachments in a private GitHub repository, not public code or Pages. Client credentials can only write/delete their installation's data, never read other users' records; exports require a separate secret. Hosting infrastructure processes connection metadata, but Toolkit does not store IP addresses in its event table.

Receiver failures do not change research or delivery decisions. Trajectories can locate product problems. Fewer calls, completion flags or shorter paths are not evidence of improved research quality without examining the actual work.
