# Independent adversarial reasoning review

Review recorded: 2026-11-05T15:02:41.9046977+08:00. Reviewer execution identity: native agent `/root/case_adversarial_full`. Role: `adversarial_reasoning` only; no production contribution or report editing.

**Verdict: no necessary correction found for the reviewed version.** This is a judgment about the reasoning and its stated conditions, not a comparative performance result or final acceptance of the research package.

## Input version and actual reading coverage

- Complete `report.md`, lines 1–102, SHA-256 `15A3EE49392069F8187759EEC7B889EEBF9365D7424D0C08A59B3B6221A8CF91`. The hash was checked before and after the main reading and was unchanged.
- Complete effective `../requirements.md`, SHA-256 `16B09FC2BBFDEEC3D9835B4CF16D853779349F69AD41CD4D8EE6A4A8B99957A8`; complete `../requirements-clarifications.md`, SHA-256 `98446BF425CBF627AC3BEA86C201358600ABD03EFEDF6D078CD1FE0EC62A58D4`.
- Review responsibilities in `research-toolkit/references/subagents-and-review-loop.md`, especially lines 31–61; complete current `outline.md`, `source-notes.md`, and substantive contribution `analysis/D-scenario-accounting-proposal.md`.
- Original evidence actually read: complete local Markdown originals S02 (Stripe idempotent requests), S03 (API v2 overview), and S04 (advanced error handling); relevant extracted passages from S05 (Playwright user-facing locators, fresh element resolution, structural CSS/XPath fragility), S06 (click actionability and assertions), S07 (isolated contexts and authentication-state authority), S10 (GitHub App permission model), and S13 (indirect injection and agent-specific execution controls). These HTML sources were stripped of script/style and markup for the displayed passages, not treated as full-page readings.
- S09: preserved official-page numbered text, source lines L792–L801, covering latency, coordinate/tool-selection errors and limitations; this reading does not rely on the region-error HTML. S08: relevant original passages on application-owned sessions/permissions, code execution, and line 1774 distinguishing call generation from execution. S12: original lines 2707–2783, including confirmation/consent, action-time confirmation, pre-approval and human takeover.
- No other initial review, author self-check, author handoff or revision disposition was read. No product trial or new performance measurement was performed. Source reading was targeted to the adversarial claims below, not a duplicate complete evidence audit.

## Challenges and their consequences

### 1. A supported API can be a worse local choice

**Location:** report lines 5–20, 58–60, 84 and 88–100. **Applicable requirement:** answer which route fits recurring business work without inventing a universal performance or cost ranking.

The strongest counterexample to an API default is a low-volume workflow with a cheap, stable UI path and expensive integration setup, or a browser account with narrower authority than the available API token. The report explicitly admits both counterexamples. Its opening requires exact coverage, suitable permissions and usable results, while line 84 allows an entirely browser-based implementation when integration effort exceeds its benefit. The local cost comparison includes setup and maintenance rather than presuming API use is free. GitHub's actual permission model and Playwright's authentication-state warning support examining the authority granted rather than naming a transport as inherently safer.

**Disposition:** no defect. These counterexamples change the local route and are already incorporated; they do not overturn the conditional default. No broader comparison experiment is necessary to present that default as a design judgment.

### 2. A visual model need not be inferior to a prepared script

**Location:** lines 19, 32–40, 78 and 98. **Applicable requirement:** distinguish deterministic DOM execution from model-directed control and explain when each earns its operating burden.

A variable interface, visually meaningful state, or infrequent path that is expensive to encode can favor runtime model interpretation. Conversely, visual layout changes need not break a semantic locator. The report preserves both directions: it makes visual interaction a candidate when interpretation or variation handling adds necessary capability, and it does not equate a DOM locator with coordinate replay. Playwright's locator guidance supports the latter distinction; Anthropic's limitations establish possible execution problems but cannot quantify a universal ranking. The report explicitly respects that evidential limit. Its treatment of runtime-generated Playwright code also avoids misclassifying a model's decisions as deterministic merely because the driver uses a familiar library.

**Disposition:** no defect. The recommended split is based on the need for interpretation and recurring maintenance, not an unsupported claim that one mechanism always wins.

### 3. Retry protection is not transferable across routes or unlimited in time

**Location:** lines 44–54 and 80–82. **Applicable requirement:** address uncertain results, duplicate effects, retry scope and partial recovery.

The dangerous counterexample is an accepted write whose response is lost: either a fresh key or a browser submission could create a second effect. Stripe v1's retained error response also shows why retry success cannot be equated with business completion; v2 shows why one provider's namespaces cannot be collapsed into one rule. The original S02–S04 text supports the report's distinction between v1 saved responses, v2 retries of failed work, namespace/account/time scope and persistent operation identity. S03's default eventual consistency for v2 lists supports the warning that an empty immediate list is not decisive evidence of absence.

**Disposition:** no defect. The report makes cross-route duplicate protection conditional, requires reconciliation for unresolved attempts, and does not imply that the hypothetical request reference itself enforces idempotency. A visual fallback is not allowed to erase an uncertain write.

### 4. The hybrid example could conceal its hardest dependency

**Location:** lines 70–84. **Applicable requirement:** one coherent hypothetical workflow with explicit assumptions and recoverable partial execution.

The scenario works only if the generator's history can identify the same pending or completed job. A UI that offers only a transient success banner would not support its recovery path. The report identifies the history/reference capability as an assumption to check, says that the history view does not make creation idempotent, and routes ambiguity to investigation rather than automatic resubmission. It retains the already completed preference update and generated document when later stages fail. One owner for the attempt addresses duplicate concurrent submission within the stated example; the report does not pretend to specify a complete distributed workflow implementation.

**Disposition:** no defect. Missing result evidence narrows or defeats the proposed automated step, and the report says so. The scenario illustrates a conditional architecture without presenting invented application capabilities as facts.

### 5. Permission and untrusted instructions can invalidate an otherwise convenient route

**Location:** lines 58–66 and 74–78. **Applicable requirement:** compare actual authority, untrusted content and human handling.

An API response can contain hostile customer text, while a browser can use a carefully restricted account; neither format establishes authority. The report's execution restriction is consistent with OWASP's original permission and parameter-validation guidance. A second counterexample is a workflow authorized in general but still subject to action-time provider confirmation. S12 distinguishes that situation from permitted pre-approval and human takeover. The report scopes the rules to the documented integration and preserves required confirmation in the scenario instead of turning an internal-workflow label into blanket permission.

**Disposition:** no defect. The text avoids both an unsupported API security advantage and an unnecessary universal confirmation rule.

### 6. Cheap completion statistics can hide dropped or assisted work

**Location:** lines 90–96. **Applicable requirement:** discuss operating effort without fabricated benefits or a misleading comparison population.

A route could appear inexpensive by omitting failed attempts, counting heavily assisted completions as autonomous, dropping hard cases or amortizing setup over a different workload. The proposed comparison explicitly holds workload and period common; includes failed execution and human handling; separates assisted completions; and reports unresolved and incorrect cases. Its zero-completion ratio is undefined rather than presented as an attractive cost. The pilot lets the workflow's actual service needs set acceptable completion and turnaround, so the ratio does not silently become the sole acceptance criterion.

**Disposition:** no defect. This is an accounting proposal with relevant selection effects exposed, not evidence that any route is cheaper or reliable enough for a particular enterprise.

## Necessary versus optional work

Necessary corrections: none identified within this perspective and input version. Optional editorial or implementation additions: none requested. Additional vendor benchmarks, universal thresholds, a new recovery platform or an installed-product test would extend the assignment without repairing an observed defect.

The central recommendation survives the examined counterexamples because its exceptions are operationally consequential and preserved through the scenario and local decision method. It remains conditional on the chosen application's real coverage, authority, result evidence and workload costs.
