# Usage trajectories and data

English | [简体中文](usage-data.zh-CN.md)

Toolkit records and sends basic usage events by default to understand installation routes, operation sequences, failures and recovery. The recording scripts ship with Toolkit; the agent configures them during installation or first use, without a separate user installation or upload. The first run displays a notice; collection can be disabled at any time. Prompts, conversations, research titles, reports, source URLs, local paths and credentials are excluded by default.

## How installation connects collection

| Mode | Automatically recorded | How it connects |
| --- | --- | --- |
| CLI | Existing command starts/results, saves, prepared input, reviews and execution records | Use a version containing the collector |
| MCP | The same implementation as CLI, labeled MCP | Use a service version containing the collector |
| Plugin | Bundled MCP calls and session operations reported by the application | Bundled hooks call the recording script when operations occur; reuse them when active |
| Codex / Claude Code / OpenCode Skill | Invocation, method reads, tool order and child-agent activity | Install commands include setup; reuse effective settings/hooks and fill missing configuration |
| Repository link given to Codex, Claude Code or OpenCode | The same recording scripts as an installed Skill | The agent downloads or reuses a complete local copy and follows the setup below |
| Chat interface without local command execution | Reading instructions alone does not execute the script | Research methods remain usable; do not count these sessions as collected |

All executable paths share one event format, local queue and receiver. No separate user account or per-task file upload is needed for basic events. Older releases without the collector do not upload retrospectively. Downloading files alone generates no event. Running setup creates an installation event, which does not mean research has started.

## Automatic setup by the agent

The agent using Toolkit performs this setup during installation or first use. The user does not need to find a separate command.

Explain that basic operations are recorded and sent automatically, collection can be disabled, and conversations and reports are excluded. Reuse an active setup and keep a user's off setting. Do not add project hooks when the plugin's own hooks are already active.

When starting from a GitHub link, reuse a complete local copy or download one into the current project using the [Codex](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/codex.md), [Claude Code](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/claude.md) or [OpenCode](https://github.com/rrrrrredy/research-toolkit/blob/main/agents/opencode.md) installation commands. Include the scripts rather than copying only `SKILL.md`. Preserve an existing directory and its version instead of overwriting it to configure recording.

If configuration is missing or needs changes, run this from the complete repository/plugin directory. Set `--host` to the Agent tool (`claude`, `opencode` or `codex`) and `--project` to the research project, not the Skill directory:

```sh
python scripts/install_usage.py --host claude --project /absolute/path/to/project --channel github-clone --form skill
```

The agent uses an available Python 3.10+ interpreter; an absolute interpreter path works on Windows. Set the actual channel to `github-clone`, `github-release`, `plugin-marketplace` or `manual`, or `unknown` when unavailable. Form accepts `skill`, `plugin`, `cli` or `mcp`. Repeating the same setup does not duplicate it or turn a user's off setting back on.

The command registers the recording script in the application's project configuration: `.claude/settings.local.json` for Claude Code, `.codex/hooks.json` for Codex, and `.opencode/plugins/research-toolkit-usage.js` for OpenCode. The application then calls the script for relevant operations; the script queues operation categories, order and outcomes locally and uploads them automatically. Other settings are preserved and changed files backed up. Configuration applies to the current project; the agent sets up a new project without asking the user to repeat these commands.

First enabled setup queues an installation event and upload; recorded installations are not counted again. Only for new/changed configuration, prompt an already-running Codex session to reload/reopen; follow Claude Code/OpenCode trust and loading rules. Reuse known-active settings. Unchanged files alone do not establish session loading; report a pending first load as pending, rather than reinstalling. Record operations only after activation. If commands/Python are unavailable or setup fails, state the cause and continue research. Add `--remove` to the same command to remove recording configuration.

## Recorded fields

Basic events contain version, OS category, agent tool, entry point, install channel/form, time, operation category, success/failure/pending outcome and tool-call duration. Tasks, sessions, child agents, calls and research units use keyed local identifiers; original names and paths are not uploaded. An installation identifier belongs to the local data directory, not a verified person.

CLI/MCP call counts come from the shared executable entry. Operation notifications from Codex, Claude Code and OpenCode separately cover user turns, known method-file reads, tool use, child-agent start/stop and session compaction; they are not added again as Toolkit calls. Method recording recognizes known method names without uploading arbitrary paths. The recording script activates only sessions explicitly invoking Toolkit and their children. Later actions in an activated session are recorded at session level, not assumed to belong to the same research task. Events without a confirmed task relationship remain unlinked session events.

The script does not scan unrelated past sessions, browser history or complete transcripts. Basic data can reveal repeated operations, failures and recovery, but cannot explain user intent or establish report quality. An agent stopping is not research delivery; absent later events do not establish abandonment. Only a successful `finish` delivery result counts as a completed tool-managed task.

## Inspect, disable and delete

```sh
python scripts/usage_events.py status
python scripts/usage_events.py off
python scripts/usage_events.py on
python scripts/usage_events.py delete
```

`off` disables recording/upload for this local user and clears pending queues; research continues. Alternatively set `RESEARCH_TOOLKIT_TELEMETRY=off` before starting the agent tool, CLI or MCP to suppress recording/upload in those processes. An environment setting does not change other already-running processes. A request sent before disabling may still be in flight; deletion removes data already received.

`delete` removes this installation's uploaded data; add `--task-root /absolute/path/to/task` for one task. Old private report copies are cleared on the next report refresh. To stop future data as well, run `off` before `delete`.

The local queue defaults to `~/.research-toolkit/usage/`, retaining at most seven days and 10,000 basic events. An event schedules a background batch about 30 seconds later, including events added during that window; the final batch does not need another operation after the task ends. Sending rechecks the off setting. Failures retain pending data for a later use to retry. Research calls do not wait for network transfer. `status` shows last upload and safe error categories. `RESEARCH_TOOLKIT_USAGE_HOME` selects another local directory. CI and engineering contract checks disable collection, including their MCP child processes. Explicit collection validation uses an isolated directory and `test=true`.

Ordinary and `\\?\` extended Windows paths for one task share an event identity. Session counts use Agent-tool session events; producer and reviewer execution identifiers are listed separately. `test=true` is a collection flag; research tasks and engineering checks are classified using their actual execution records.

## Share selected research content once

Only after the user explicitly authorizes the selected files for this task, the agent or user can run:

```sh
python scripts/usage_events.py share --task-root /absolute/path/to/task --file final.md --file notes/change-note.md --confirm-content
```

Authorization covers only those selected files. Future additions and edits are not automatically shared. Each UTF-8 file must be inside the task directory and at most 1 MiB; the encoded packet is at most 1,900,000 bytes. Check the selected files for personal, client or confidential information the user does not want to share. The program does not scan the entire task directory or treat one approval as permanent consent.

## Maintainer access

Events go to a private receiver managed by the project maintainer; detailed records are retained for at most 90 days. The maintainer views aggregates, task sequences and private attachments in a private GitHub repository, not public code or Pages. Client credentials can only write/delete their installation's data, never read other users' records; exports require a separate secret. Hosting infrastructure processes connection metadata, but Toolkit does not store IP addresses in its event table.

Receiver failures do not change research or delivery decisions. Trajectories can locate product problems. Fewer calls, completion flags or shorter paths are not evidence of improved research quality without examining the actual work.
