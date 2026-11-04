# Usage collection: implementation observations

Recorded on 2026-11-04. These checks concern event collection and viewing, not research quality. Test traffic uses an isolated local data directory and `test=true`.

| Path | Actual observation |
| --- | --- |
| CLI → packaged MCP → local Worker/D1 | One synthetic engineering task produced 14 events for five calls: CLI start and a rejected save, packaged MCP save/status and a changed requirement. All 23 assertions in this end-to-end run passed; elapsed wall time was 7.812 seconds. |
| Retry, privacy and controls in that run | A failed upload retained the queue; resending did not add rows. Content/path sentinels were absent, extra receiver fields were rejected, ingest credentials could not read exports, explicit selected-file sharing worked, disabling prevented collection, and deletion removed received data. Private Markdown was generated locally. GitHub report cleanup was queued, not exercised online. |
| OpenCode native observer | The installed `.js` plugin observed Skill/tool use and one child Agent, then a continuation with a changed constraint and another child. The first run exposed incorrect parent identifiers. After the repair, all parent links in the 12 new continuation events resolved. All 27 events, including the earlier failure, remain preserved. Output-stream spans were 34.050 and 29.349 seconds; these are not whole-process wall times. |
| Codex native observer | The first run exposed a Windows hook launch failure (60.922 seconds). A continuation launched hooks but missed the natural name “Research Toolkit” (75.219 seconds). After those repairs, the continuation produced 14 events with one child start/completion and resolving parent links (50.312 seconds). These are local protocol-run wall times, including the work performed by the host. |
| Same-turn sibling control | Two constructed child-start events in the same parent/turn remained distinct and linked to the parent; four events reached the local receiver. This was an integration control, not another model task. |
| Packaged hook command | The packaged command ran in the Windows shell and emitted installation/user-turn events with `form=plugin`. This does not establish marketplace hook discovery or trust in every host. The packaged MCP path above was actually exercised. |
| Task-scoped deletion | Deleting task A through the client/local receiver preserved task B's queued event. |

The native tasks used synthetic input files and a result file; no completed research report or independent research-quality review is claimed. Child inputs are distinguished from user-role turns. Receiving a tool response is not counted as proven operation success, and an Agent stopping is not counted as research completion.

Affected Python compilation, JavaScript syntax checks, plugin generation and bilingual Skill-page generation completed. Repository CI results belong to the PR; passing CI is not a measurement of user journeys.

## Not yet completed

- The production receiver has not been deployed or configured as the default endpoint. This change must remain unreleased until that connection is verified.
- Private GitHub Actions rendering, artifact access and deletion/retention cleanup still need a deployed receiver.
- Claude Code's installed command is available, but the account's login page requires a qualifying plan. No complete Claude session was run and no plan was purchased.
- Native marketplace plugin hook discovery/trust and macOS/Linux host execution were not run. Use a Toolkit task with a child Agent in the relevant host; expect parent/child events, then verify `off` suppresses new events. Do not assume the Windows launcher control establishes those paths.

Original task inputs, raw host outputs, first failures, local receiver requests/responses and elapsed measurements are preserved in the execution archive. No research case was rerun for this feature.
