# Research execution path — 29 October 2026

[English](README.md) | [简体中文](README.zh-CN.md)

This archive preserves the existing local validation of the v1.5.0 working-tree changes based on `be56dcc8a6c9189c35cca2fd03d3f07f3cd24fec`. Archiving did not rerun checks or research. The implementation is in the accompanying commit; the base commit alone does not identify the changed implementation.

## Observed interface behavior

One synthetic cooling-retrofit task exercised **12 CLI operations**, totaling **9.625 seconds** of subprocess wall time. Analyst prose, self-review and the synthetic host reference were supplied by the driver. There were **zero research model calls and zero host subagent executions**; software check methods are not additional research tasks.

- Satisfied but still applicable requirements remain in work inputs.
- Selected claims bring supporting and counter-evidence originals; missing input files are rejected.
- Requested methods are returned, and a saved analysis can be recovered with its input versions and host reference without replacing the main report.
- Updating requirements exposes changed input files; assembly can read the saved analysis.
- The supplied complete report reaches the existing review and delivery path.

See [requests and responses](raw/calls/), [commands and timings](raw/execution.json), [result summary](raw/result.json), and [task artifacts](raw/tasks/handoff/). File changes are notifications, not automatic judgments that an analysis is invalid. These observations do not establish research-quality or rework improvements.

## Existing checks and retained failures

Affected compilation, workflow, draft, records, continuity, release-log, lock and reviewer checks completed, together with plugin, version, DSH configuration and local site checks. The packaged MCP stdio check passed; its retained log is [mcp.log](raw/mcp.log). New work inputs were exercised through CLI; the MCP integration exercised existing calls to shared implementation.

[checks-initial.json](raw/checks-initial.json), [checks.json](raw/checks.json), [resolved-checks.json](raw/resolved-checks.json) and their logs preserve intermediate failures and subsequent results. Windows temporary-directory permissions and path length caused execution failures. A record check also exposed unreadable activity-log handling; that was fixed to preserve the original log and return a warning, and the failed check passed. Read the records together: an intermediate failure is not an unresolved final failure, nor has it been erased. Attempts may repeat inherited checks; do not add their counts as independent cases.

[manifest.json](manifest.json) lists SHA-256 hashes and sizes of 71 byte-identical copied files. Original paths, timestamps and the pre-commit delivery note in `raw/README.md` describe the original execution, not the current publication state. Implementation-edit helpers and abandoned temporary directories are not part of this archive. Original reports and previous evaluation records elsewhere are unchanged.

## Reproduction and unrun host behavior

The original [driver](raw/verify_path.py) expects `<parent>/research-toolkit` and `<parent>/output/<new-run>/verify_path.py`. Copy the driver to a fresh directory in that layout and run it with the project Python environment. It refuses to overwrite an existing task. Historical absolute paths in archived outputs remain unchanged. This instruction is provided for later reproduction; no run was added while preparing the PR.

Actual host startup, messaging, continuation and cancellation were not exercised. The minimal host check is to dispatch the returned work inputs through a native subagent tool, save its analysis with the real host reference and `based_on`, then update a relevant requirement and pass the refreshed input to that task. The lead should read the analysis and integrate it into the main report. Expected behavior: readable originals, visible current requirements, recoverable output, and no substitution of branch completion for whole-task delivery. Use the host's existing lifecycle operations; no new scheduler is introduced.

Research quality, user effort and research elapsed time were not measured. The 9.625 seconds is interface execution time only.
