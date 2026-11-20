# Usage trajectories and data

English | [简体中文](usage-data.zh-CN.md)

New installations leave basic usage recording off. If the user opts in, Toolkit sends operation metadata to help the maintainer understand installation routes, failures and recovery. Prompts, conversations, research titles, reports, source URLs, local paths and user credentials are excluded from those events. Existing on/off settings remain in effect. Report sharing is a separate decision.

**Availability**　This command is available in the [repository source](https://github.com/rrrrrredy/research-toolkit) after v3.0.0. To preview the current setting, target path and optional hooks, run `python scripts/research_workflow.py setup --host codex --project .`. A fresh installation reports `planned_action: none`. The preview writes no files. Use `setup --host codex --no-telemetry` to skip setup for this invocation. After opting in, `setup --host codex --apply` applies the previewed hooks.

## How installation connects collection

| Mode | Recorded after opt-in | How it connects |
| --- | --- | --- |
| CLI | Existing command starts/results, saves, prepared input, reviews and execution records | Use a version containing the collector |
| MCP | The same implementation as CLI, labeled MCP | Use a service version containing the collector |
| Plugin | Bundled MCP calls and session operations reported by the application | Bundled hooks call the recording script when operations occur; reuse them when active |
| Codex / Claude Code / OpenCode Skill | Invocation, method reads, tool order and child-agent activity | The optional setup below configures the current project |
| Repository link given to Codex, Claude Code or OpenCode | The same recording scripts as an installed Skill | Read the methods directly or use a complete local copy. Configure recording only after opt-in |
| Chat interface without local command execution | Reading instructions alone does not execute the script | Research methods remain usable; do not count these sessions as collected |

All executable paths share one event format, local queue and receiver. Downloading files alone generates no event. Enabled setup can create an installation event before any research has started.

<a id="automatic-setup-by-the-agent"></a>
<a id="enable-basic-recording"></a>

## Enable basic usage recording

New installations start with basic recording off. Upgrades retain the saved setting. Older versions stored the same `on` value for default and manually enabled recording. Use `status` to see the current value and `off` to turn it off.

When a user explicitly requests recording, run the first command from the complete [Skill installation](https://github.com/rrrrrredy/research-toolkit/blob/main/docs/installation-versioning.md#install-a-version-pinned-skill) or plugin directory. It enables basic events for that local user across projects. CLI and MCP need only this step. If the user also wants session hooks for the current project, run the second command for their Agent tool. Reuse active plugin hooks where available.

```sh
python scripts/usage_events.py on
python scripts/install_usage.py --host claude --project /absolute/path/to/project --channel github-release --form skill
```

Use a Python 3.10+ interpreter. Set `--host` to `codex`, `claude` or `opencode` and `--project` to the research project. Set the actual install channel to `github-clone`, `github-release`, `plugin-marketplace` or `manual`, or `unknown` when unavailable. Form accepts `skill`, `plugin`, `cli` or `mcp`.

The installer adds hooks only with recording enabled. It edits `.claude/settings.local.json` for Claude Code, `.codex/hooks.json` for Codex, or `.opencode/plugins/research-toolkit-usage.js` for OpenCode. It preserves other settings, backs up changed files and reuses an existing matching setup. A bundled hook exits before reading its input when recording is off. Use the same installer with `--remove` to remove Toolkit's project hooks.

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

`off` disables basic recording for this local user and clears pending basic events. To suppress both basic events and content uploads for a process, set `RESEARCH_TOOLKIT_TELEMETRY=off` before starting the agent tool, CLI or MCP. It affects only processes that receive the setting. An already sent request may still complete. With fresh default settings, installation, ordinary operations and status checks do not initialize a local usage store.

`delete` removes this installation's uploaded data. Add `--task-root /absolute/path/to/task` for one task. Old private report copies are cleared on the next report refresh. To stop future transfers, turn off basic usage and withdraw active report-sharing grants separately.

The local queue defaults to `~/.research-toolkit/usage/`, retaining at most seven days and 10,000 basic events. An event schedules a background batch about 30 seconds later, including events added during that window; the final batch does not need another operation after the task ends. Sending rechecks the off setting. Failures retain pending data for a later use to retry. Research calls do not wait for network transfer. `status` shows last upload and safe error categories. `RESEARCH_TOOLKIT_USAGE_HOME` selects another local directory. CI and engineering contract checks disable collection, including their MCP child processes. Explicit collection validation uses an isolated directory and `test=true`.

Ordinary and `\\?\` extended Windows paths for one task share an event identity. Session counts use Agent-tool session events; producer and reviewer execution identifiers are listed separately. `test=true` is a collection flag; research tasks and engineering checks are classified using their actual execution records.

<a id="share-selected-research-content-once"></a>
## Share research content after delivery

One-time report sharing and ongoing project grants require explicit consent and can be used with basic recording off. If the user requests a sharing invitation, or a saved setting calls for one, show the actual filename and recipient after delivering the report links. The recipient is the Toolkit maintainer's private `rrrrrredy/research-toolkit-usage` repository. The user may share once, allow future final reports in the displayed directory and its subdirectories, or decline. Silence leaves the report local. List any chat or source files separately if the user wants to contribute them.

Managed tasks can return an invitation in `finish.content_sharing` after `completed=true`. For Skill-only work with file/command access, use `share-offer` to check an applicable sharing choice after delivery. A fresh install with basic recording off has no automatic invitation. An older recorded off setting keeps old automatic grants paused in the upgraded version. The user can still authorize a new one-time share or explicitly reconfirm a continuing grant for a scope.

```sh
python scripts/usage_events.py share-offer --task-root /project/tasks/study --file final.md --language en
```

Normal delivery, `share-offer` and `share` reuse the nearest saved sharing scope containing the task, including an explicitly selected project above several task directories. A more specific saved choice takes precedence, including refusal or a request to restore the invitation. With no saved scope, the default covers only the task directory and its descendants, not the shared `tasks/` parent. Use `--project-root` only for the containing directory the user explicitly selected. The invitation states that all tasks in that directory and its subdirectories are covered. An old “already offered” marker does not override an explicit ancestor choice. The returned prompt identifies that scope. No reply queues no content. The user can request sharing later. `--confirm-content` records the caller's confirmation that the user actually agreed; it is not a popup or an inferred approval.

Older continuing grants have no record that the user confirmed the displayed directory scope. The next delivery or `share-offer` using such a grant shows the actual directory through the existing invitation and queues no new report until the user agrees. The invitation appears once while unanswered; one-time sharing does not confirm future automatic sharing. Confirming `reports` records the scope confirmation, so later deliveries reuse it. Users can select a narrower directory or decline; existing explicit refusals remain effective.

Only after the user explicitly authorizes the selected files for this task, the agent or user can run:

```sh
python scripts/usage_events.py share --task-root /absolute/path/to/task --file final.md --file notes/change-note.md --confirm-content
```

This command shares only the listed files once and preserves an existing project report grant or refusal. Sharing supplementary material once does not cancel continuing report authorization or reopen sharing after refusal. If the user chose continuing authorization, use `share --decision reports` with the single final report and `--confirm-content`. Later successful deliveries in the same project queue only the final report; they never expand that grant to chat, source materials, or other projects. Unchanged reports are not queued again. Upload uses the existing content queue and private receiver.

When the user selects a containing project after an invitation, that confirmation clears only obsolete invitation markers between the current task and the selected project. Explicit refusal, one-time sharing and renewed-invitation choices are retained. Thus an earlier prompt at `project/tasks/` does not hide the newly confirmed `project/` grant from the next task there.

```sh
python scripts/usage_events.py share --task-root /project/tasks/study --project-root /project --file final.md --decision reports --confirm-content
python scripts/usage_events.py share --task-root /project/tasks/study --project-root /project --decision decline
```

Decline remembers the choice and removes queued content for this project. `share --decision ask` restores the invitation on a later delivery when the user requests it. Both choices leave basic usage recording unchanged. Each UTF-8 file is limited to 1 MiB, and the encoded packet to 1,900,000 bytes. The agent lists selected files before obtaining consent.

When a directory covered by a continuing grant is declined or reset to asking, its pending packets under that grant are removed while sibling directories can still use the grant. Older queued packets under a containing grant can lack enough local path information to confirm that they fall outside the withdrawn scope. Those unlocatable packets are removed as well.

Showing an invitation records only that it was displayed; it does not replace an explicit `ask`, `decline` or report grant. In particular, a child directory set to `ask` continues to block an ancestor report grant after the invitation is shown. No answer queues nothing. An explicit `share --decision ask` resets the invitation so it can be shown again. One-time sharing preserves this choice.

## Maintainer access

Events go to `https://research-toolkit-usage.luosongred.workers.dev`, managed by the project maintainer (`/v1/install`, `/v1/events`, `/v1/content` and `/v1/delete`); detailed records are retained for at most 90 days. The maintainer views aggregates, task sequences and private attachments in a private GitHub repository, not public code or Pages. Client credentials can only write/delete their installation's data, never read other users' records; exports require a separate secret. Hosting infrastructure processes connection metadata, but Toolkit does not store IP addresses in its event table.

Receiver failures do not change research or delivery decisions. Trajectories can locate product problems. Fewer calls, completion flags or shorter paths are not evidence of improved research quality without examining the actual work.

The first successful CLI/MCP result or installation result includes `usage_notice` with the receiver, data scope and disable command. CLI requests pass their `language` to this notice (`zh`/`zh-CN` for Chinese, `en` for English). The agent displays it in the conversation; later results do not repeat it. Existing disabled settings are preserved. Counts contain only numbers of sources, claims, requirements, findings or dependencies.

The generated upload credential is sent for receiver authentication. Task/session identifiers use a separate local `id_secret` that is never sent. Upgrading an older installation creates this local key for new events; existing queued payloads and uploaded history keep their original identifiers. Task deletion covers both identifier generations. Identifiers are pseudonymous; repeated identifiers still connect events within a task.

Selected content is checked before queueing for credential file names, including `.env.*`, `credentials.json`, `client_secret*.json`, `secrets.yaml`, `.npmrc` and `.netrc`; private keys and recognizable OpenAI/Anthropic, GitHub, AWS, Slack and Google token formats; JWTs; and values assigned to authorization/password fields or passwords in database URLs. Ordinary hashes, protocol explanations and explicit placeholders such as `<password>`, `${DB_PASSWORD}` and `YOUR_TOKEN` remain usable in reports. A refusal names the file, not the matched secret, and none of the selected batch enters the queue. Share a redacted copy if needed. This check applies only to selected files, without scanning other project content.
