# Record-saving verification

[English](record-save-validation.md) | [简体中文](record-save-validation.zh-CN.md)

The new save interface was exercised using the retained [coding-benchmark procurement task](../evals/studies/2026-10-14-native-agent/README.md): 10 sources, 16 claims, six requirements and both complete reports. This reuses real task material to check the changed execution path; it is not a new research generation or model-quality comparison.

In a separate disposable task, the tool imported the records, saved the first complete draft, updated a length record and saved the retained final report. A deliberately mistyped length field rejected the whole batch without changing source records; correcting it recovered normally. A deliberately damaged CSV in the copy was then recovered with an explicit complete replacement, retaining the damaged bytes as a backup. All extra source columns survived. The first draft and its first observation remained unchanged, and the final draft passed the existing record/length checks.

- Five save attempts, two recorded controlled format failures, zero new model calls.
- All 50 files in the original task remained byte-identical.
- First draft hash: `ac517435dae41f0cf7ca81e8f8b94064b4609ff03765266ba1cb4ad44420ba88`.
- Final report hash with normalized line endings: `dffbb316809ec7fa174fd65a1acdd557617b7bcfe2962890c96fc2e0bcc06ad3`.
- First save observed at `2026-10-14T09:45:45.641797+00:00`; this is the replay save, not the historical authoring time.
- The usage parser was also run on the existing native/Toolkit session events. Input/output/cached totals matched the retained summary exactly: native 1,297,739 / 16,264 / 1,192,448; Toolkit 3,320,554 / 24,271 / 3,164,160. These are historical author-session checks, not new calls or usage attributed to the replay.

Focused automated controls additionally cover partial updates, quoted/multiline Unicode CSV, automatic IDs, backups, write-error rollback, task paths, read-only checks, stale Lite receipts, failed reviewer retry and retained provider usage without double counting. Packaged MCP exercises `research_save` in both profiles and recovers from a located field error. These checks run in the existing Linux, Windows and Python 3.10 jobs; no paid evaluation is added.

The source-reading declarations and current report contents were reused, not newly independently reviewed. This verifies record management and observations, not a reduction in real research time. Observation fields do not participate in research input hashes or delivery acceptance. These records do not establish a benefit in subsequent substantive research updates.
