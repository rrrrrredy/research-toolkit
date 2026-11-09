# Full-report author revision 01

Author: Codex /root/ttc_research; original substantive author, not an independent reviewer.
Recorded: 2026-11-09T14:54:58.082790+00:00.

Input: `C:\Users\luosong03\Documents\ChatGPT\Others\work\toolkit-long-research-20261109\evals\runs\2026-11-09-long-research\tasks\on_device_models_en\reports\current.md`
Input SHA-256: `3afb14812baddbd92f0b79ff3db2fd4a77a3f50deba85c04f6e0077724f9f96b`
Output: `C:\Users\luosong03\Documents\ChatGPT\Others\work\astra-api-current-chat-20261109\work\implementation\research\on_device_models_en\codex-production\draft-revision-full-01.md`
Output SHA-256: `11093fb5d5a0a18708db9a9175d84ed3bbbb7773b51a393f5161db49f9c8be3e`

## Finding disposition

- natural_expression-01: Removed internal author/review status in the opening, the handoff/acquisition correction narrative, and the independent-review pointer. Kept the cutoff, source versions/commits, computation files, actual reading ledger and missing deployment measurements.
- The current manuscript already contains the separately revised Android performance-lock conditions. All three performance-lock passages and their numerical tables are carried forward unchanged.

## Review and original-source reading

- Read `C:\Users\luosong03\Documents\ChatGPT\Others\work\astra-api-current-chat-20261109\work\implementation\research\on_device_models_en\native-full-reviews\natural_expression\response.json`; SHA-256 `976c356d0ac27ed37244bb594c25b6e5b3cb45ec580afdf640676778c24e680e`. Relevant findings: natural_expression-01.
- This is the requested editorial correction using the current manuscript and saved findings; no new external source reading was necessary.

## Scope and preservation

The input current manuscript, first manuscript, prior author checks, upstream originals and calculation artifacts were not edited. No research/model experiment, model API call, calculation rerun, managed-state update or review import was performed. The diff below is the complete textual change. Author completion does not claim independent reviewer acceptance.

## Complete diff

````diff
--- reports/current.md (read-only input)
+++ draft-revision-full-01.md
@@ -1,6 +1,6 @@
 # On-Device Models: Hardware Constraints, Task Fit, and Edge–Cloud Design
 
-Evidence cutoff: 9 November 2026. Author: Codex research producer `/root/ttc_research`. This is substantive author analysis; independent review is separate.
+Evidence cutoff: 9 November 2026.
 
 ## 1. Choose a task envelope before choosing an accelerator
 
@@ -286,8 +286,6 @@
 
 Several source details affect the arithmetic. The WhisperTRT README labels memory as MB, while its profiler computes MiB and samples an RSS difference rather than a peak. Its `base.en` ratio is 439/666 = 65.9% of the original path's reported memory; the report uses the actual values rather than treating the promotional “about 60%” as precise. The independent speech paper's printed WER formula contains an apparent insertion-term typo; the interpretation here uses the conventional `(substitutions + deletions + insertions) / reference words`. Its unavailable code and unspecified exact aggregate audio duration prevent a precise reconstruction of real-time factor or wall energy.
 
-The original handoff's S24 attribution was checked against the current LiteRT page, found to refer to a different table, and resolved by retrieving the historical S24 commit. An unrelated PMLR page acquired during the Minions search is excluded; the final Narayan et al. paper is the source used. Earlier notes and originals are retained rather than rewritten as if these distinctions were known at acquisition.
-
-The accompanying `deployment_calculations.py` and `calculation-results.json` contain the executed memory, phase-time, clip-RTF, power-duty, transfer and economic arithmetic. They run no model inference and make no claim to validate a device. `reading-ledger.json` records the original paths and selected locations actually read; `key-premises-for-review.md` maps the material assumptions for independent review.
+The accompanying `deployment_calculations.py` and `calculation-results.json` contain the executed memory, phase-time, clip-RTF, power-duty, transfer and economic arithmetic. They run no model inference and make no claim to validate a device. `reading-ledger.json` records the original paths and selected locations actually read.
 
 For a concrete deployment, the remaining measurements are specific: available and peak working memory on the intended device state; first usable and complete-result latency with the real prompt/output distribution; sustained behavior for the actual operating duration and concurrent apps; task quality on representative documents, languages or acoustic conditions; and endpoint-level power if battery or thermal sizing depends on it. Those missing deployment measurements bound the recommendations here. They are not filled by transferring a rate from another device, runtime or task.
````
