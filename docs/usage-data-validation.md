# Usage collection: implementation observations

Recorded on 2026-11-04. Test traffic uses an isolated data directory and `test=true`.

| Path | Actual observation |
| --- | --- |
| CLI → packaged MCP → local Worker/D1 | One synthetic engineering task produced 14 events for five calls: CLI start and a rejected save, packaged MCP save/status and a changed requirement. All 23 assertions in this end-to-end run passed; elapsed wall time was 7.812 seconds. |
| Retry, privacy and controls in that run | A failed upload retained the queue; resending did not add rows. Content/path sentinels were absent, extra receiver fields were rejected, ingest credentials could not read exports, explicit selected-file sharing worked, disabling prevented collection, and deletion removed received data. Private Markdown was generated locally. |
| OpenCode usage recording | The installed `.js` plugin observed Skill/tool use and one child Agent, then a continuation with a changed constraint and another child. The first run exposed incorrect parent identifiers. After the repair, all parent links in the 12 new continuation events resolved. All 27 events, including the earlier failure, remain preserved. Output-stream spans were 34.050 and 29.349 seconds; these are not whole-process wall times. |
| Codex usage recording | The first run exposed a Windows hook launch failure (60.922 seconds). A continuation launched hooks but missed the natural name “Research Toolkit” (75.219 seconds). After those repairs, the continuation produced 14 events with one child start/completion and resolving parent links (50.312 seconds). These are local protocol-run wall times, including the work performed by the agent tool. |
| Same-turn sibling control | Two constructed child-start events in the same parent/turn remained distinct and linked to the parent; four events reached the local receiver. This was an integration control, not another model task. |
| Packaged hook command | The packaged command ran in the Windows shell and emitted installation/user-turn events with `form=plugin`. |
| Task-scoped deletion | Deleting task A through the client/local receiver preserved task B's queued event. |
| Repeated prompt without an agent tool event ID | Two identical constructed Claude-format hook inputs produced two user-turn events. The fallback creates an ID per hook invocation instead of merging equal prompt payloads; upload retries still reuse the queued ID. |
| Deployed receiver and private GitHub report | On GitHub's Ubuntu runner, the v2.3.0 packaged client made two CLI calls and uploaded five events plus one explicitly selected two-file packet containing 1,850,054 ASCII characters. The upload exercise took 2.253 seconds. The private workflow generated the overview, task timeline and downloadable artifact. |
| Online deletion and report cleanup | The same test installation disabled collection and deleted its data in 0.809 seconds. The next private report found zero events and zero content packets, processed the deletion request and removed earlier report runs and artifacts. Downloaded synthetic artifacts remain in the private validation archive. |

The native tasks used synthetic input files and a result file. Child inputs are distinguished from user-role turns. A received tool response and an Agent stopping have separate event categories from successful operations and research completion.

Affected Python compilation, JavaScript syntax checks, plugin generation and bilingual Skill-page generation completed. Repository CI results are attached to the PR.

## Deployment observations

The local Windows network resolved the receiver's `workers.dev` name to an incorrect address and timed out; the online exercise therefore ran on GitHub's Ubuntu runner. Its first health request used Python's default HTTP identity and received 403. Using the existing report client identity allowed the health request and subsequent upload to complete. The receiver accepted the packaged client's normal request headers. The selected-content packet limit is 1,900,000 bytes to fit D1's 2,000,000-byte row limit with its stored envelope.

Original task inputs, raw agent outputs, first failures, receiver requests/responses and elapsed measurements are preserved in the execution archive. The private validation directory includes the packaged client snapshot, online command outputs and downloaded artifacts. The online exercise used synthetic data and made no model calls.

## First-use setup — 2026-11-05

A fresh Codex session received the candidate Skill entry, a complete local repository copy and a short fictional store-hours task. The prompt did not supply the usage setup command. The agent read the entry and usage guide, ran the bundled installer and wrote the requested paragraph in 98.672 seconds. Continuing that already-open session for 27.422 seconds after trusting its exact project hooks produced no usage events: Codex had not loaded the newly written configuration into the session.

The installer now queues the existing `installation_seen` event when recording is enabled and the installation has not already been recorded. Its result explicitly tells Codex users to reload or reopen the session. Resuming the same thread after loading the configuration, rather than starting the task over, produced eight local events: installation, user turn, tool operations and session completion. That continuation took 33.750 seconds including setup and process startup. The original zero-event result and the continuation remain separate records.

A command-level continuation confirmed that repeating setup records no additional installation event and that an existing off setting remains off without an enabled notice. Existing project settings and hooks are preserved. This check used test-marked local events with automatic upload disabled; it reuses the earlier online transport result and makes no new claim about other applications' session-reload behavior.
