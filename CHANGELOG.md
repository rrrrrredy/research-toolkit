# Changelog

Released changes are grouped by tag. `Unreleased` describes work not yet included in a published version.

## Unreleased

Research Toolkit naming, clearer usage instructions, and development-only semantic diagnostics. These changes do not establish general efficacy. The v0.1.4 prerelease was withdrawn; v0.1.3 remains the latest available prerelease.

### Changed

- Explain research steps, failure modes, evaluation prerequisites and study configurations consistently across both READMEs and the web guide. Include tool-specific troubleshooting, recovery instructions and setup checks in the adapter guides.

- Clarify the planned single-author review lane: Astra writes with the framework in Codex; fresh-context GPT-5.6 Sol high, DeepSeek, Kimi and subsequently added GLM-5.3 review each required first submission. Preserve earlier three-reviewer freezes and label the fourth review as a later addition. Disclose the supported Coding Plan client and its context/usage boundaries. Missing reviews remain incomplete, critical disputes need evidence, and no human-review prerequisite or human-calibration claim applies. Require accepted improvements to be verified before new author/judge runs; preserve frozen historical protocols and separate LLM judgments from deterministic results. This is a study plan, not new efficacy evidence or a model dependency of the framework.
- Rename the project to Research Toolkit / 研究工具箱 and the repository and Skill identifier to `research-toolkit`. Update current documentation, installation examples, Pages links, and the owner's Profile entry. Preserve historical study inputs and release records.
- Rewrite both READMEs and the bilingual setup guide around concrete actions: give the agent the repository link, upload files if needed, or follow its installation guide. Explain saving and reopening task files in plain language. Keep research steps and their requirements unchanged.
- Remove launch-marketing copy, badges, gallery images, and video assets from the repository and public page.

### Fixed

- Keep evaluation focused on report evidence, preserved findings and matched product comparisons. Simplify the published evaluation materials and offline checks to that scope.

- Keep DSH runtime commands out of general evaluation instructions, qualify profile-specific installation paths, and remove stale approval and editing notes from current documentation. Scope local verification to the changed behavior while retaining the full offline CI suite.

- Align evaluation descriptions with their implementation and published evidence. Keep runtime-specific checks in optional adapter guidance, describe smoke checks as marker-based wiring observations, and distinguish saved delivery messages from captured replies. Update diagnostic review status, historical rubric boundaries, source-map metadata and the existing CI inventory. Retain original samples, reviews, scores and frozen study inputs; evaluation defects inform Toolkit improvements without a mandatory repair loop.

- Separate evaluation completion from reader-ready report delivery in the current bilingual evaluation standard and roadmap, including the complete-chain instruction. Complete still-required missing reviews while preserving their original failures; retain valid reviews and sample defects without a quality-driven repair loop. Use those defects for product iteration and verify the relevant changes. Existing frozen study inputs, reviews and scores remain unchanged.

- Make the existing research-planning checklist connect independently answerable questions to evidence gaps and actual answer passages. Distinguish reading a source from using its relevant evidence, and use unanswered questions to guide source selection. Reuse existing task notes without adding required files, a fixed report format, scoring rules or model calls. This method clarification has not been shown to improve report quality.

- Add an optional stored-HTML extraction helper that preserves JSON-LD publication/version dates, HTML date tags, canonical declarations and link destinations beside the text. Strict decoding, explicit extraction limits and exclusive output creation preserve source provenance. Nine positive/negative controls and checks against retained publisher HTML verify this extraction behavior; no report-quality or causal efficacy improvement is claimed. Existing protocols and frozen study inputs are unchanged.

- Align the core review protocol and guides with evidenced adjudication: preserve original findings, repair confirmed defects, and allow reasoned no-change decisions for unsupported, duplicate, or optional suggestions. Keep required work and current-version review obligations open until satisfied. Correct the Chinese guide's implication that reaching a review-cycle checkpoint can convert required work into a limitation. These instruction changes do not establish a report-quality effect.
- Add three synthetic reader-review pairs for buried opening findings, editorial narration and non-analytical timelines. Keep the earlier twenty inputs and model reviews unchanged; the author-proposed controls are development data, not held-out or measured quality results. Their later internal four-model diagnosis and retained pricing correction are described in the semantic-diagnostics index; private review records are not published here.

- Tighten delivery checks: require a specific recorded user decision for waived or excluded requirements, check declared required reading against source records, and bind global/task-required reviews to the actual report hash. Keep ordinary evidence uncertainty and honest partial delivery valid. Default to delivery contract 2; label explicit v1 historical diagnostics without rewriting frozen inputs or results. Record consistency does not authenticate consent, actual reading, or semantic quality.
- Clarify that stopping a search direction or reaching a review-cycle limit leaves unfinished mandatory work open. Make reader review inspect the opening, analytical contribution of tables, and sentence-level voice without imposing phrase bans, a fixed article template, or extra reviewers.

- Include complete task examples, the research completion checklist, recovery guidance, evaluation commands and setup checks in the reader entry points.

- Document the four progress statuses already enforced by the delivery checker and explain how to record an intentional checkpoint. Reject unsupported status names while preserving valid partial states; check that documentation and checker enums agree. The checker is not weakened and research steps are unchanged; this clarification is not efficacy evidence.
- Fail source-integrity checks when the case or source-pack collection is missing or empty, rather than reporting coverage without checking any cases. Reject missing, empty, malformed or duplicate case references, duplicate quarantine IDs and policy entries for missing packs. Report the actual case count; preserve valid workflow controls and the factual-use prohibition. No frozen sources, reports or research-method rules change.

### Added

- Publish eight label-masked semantic-review calls, including a shared missed control defect, severity disagreements and one fresh-context/order-sensitive judgment. Retain and re-review two case corrections without overwriting original inputs; the current catalog applies the corrections while keeping twenty underlying cases. Model agreement is not accuracy or human calibration.
- Add parent-bound case revisions and offline review-bundle checks that recompute observation counts and disagreements from actual model replies, not just document hashes.
- Expand the synthetic semantic diagnostic catalog from six to twenty bad/control pairs. Include justified positive judgments so caution is not mistaken for quality; retain the original six and all historical results. The new labels are author-proposed, uncalibrated development material, not held-out efficacy evidence.
- Validate diagnostic data structure and claim boundaries in CI, with negative cases for missing evidence or controls, duplicate identifiers and invalid types. Passing these checks does not establish that the semantic labels are correct.

## [v0.1.3](https://github.com/rrrrrredy/research-toolkit/releases/tag/v0.1.3) — 2026-09-08

Checker-consistency prerelease. These fixes do not change the core research method or establish research-quality efficacy.

### Fixed

- Share current review and open-issue semantics between delivery checks and evals. A later clean global review can recover from an earlier failure; later local blockers still invalidate delivery, and a local PASS cannot erase another scope. Required scopes and malformed history remain blocking. A routed action alone never closes an issue.
- Preserve English words in repeated-line detection instead of collapsing distinct paragraphs into one placeholder. Keep genuine repetition and citation-variation controls in both languages.
- Reject recognized blanket denials of accepted limitations. Report unmatched or partial disclosure as requiring semantic review, not as verified by a generic keyword; literal coverage is explicitly not semantic certification.
- Add 24 cross-entry regressions to CI, including invalid UTF-8 even when the optional receipt check is disabled. Preserve existing tests, core protocol text, frozen inputs and historical outputs.
- Label the public comparison as illustrative design goals in English and Chinese, and link separately to actual reports and limitations instead of implying measured before/after improvement.
- Explain the framework's purpose in plain language across both READMEs and the public introduction. Replace the ambiguous runtime-agnostic ResearchOps label without changing the core research method or execution rules.

## [v0.1.2](https://github.com/rrrrrredy/research-toolkit/releases/tag/v0.1.2) — 2026-09-07

Delivery-checker prerelease. The core protocol and frozen research inputs are unchanged.

### Fixed

- Recognize explicit completion claims that name the selected primary report through a Markdown link or inline filename. Previously, a reply such as `已完成 [report.md](report.md)` could pass the checker while progress remained nonterminal. Keep bare links, unrelated artifacts, negations and explicitly partial work as non-completion controls.
- Add six delivery-contract tests covering report-linked completion claims and bounded wording variants. This closes a known lexical gap; natural-language claim detection is still heuristic, not a semantic guarantee. The core Skill, references and frozen experimental inputs are unchanged.

## [v0.1.1](https://github.com/rrrrrredy/research-toolkit/releases/tag/v0.1.1) — 2026-09-07

Engineering and evidence prerelease. The original SKILL.md and all eight core references are unchanged. Ten offline suites pass; retained development diagnostics are not a held-out efficacy result.

### Changed

- Remove redundant online-reading sections from both READMEs, retain links near the introduction, and make integration guidance platform-neutral; move synchronization and packaging policy to maintenance documentation.
- Reject unknown progress statuses and delivery paths outside the task directory.
- Bind the selected delivery-message filename instead of always requiring the default filename.
- Reject invalid UTF-8 delivery inputs instead of silently replacing bytes or crashing during JSON reads.
- Keep an issue open when it only assigns a routed action; planning a follow-up is not resolution.
- Exclude unresolved numeric-scope claims and a wrong XGBoost attribution from active legacy sources; retain exact originals and audit reasons, and prevent regeneration from restoring them.
- Narrow unsupported assertions in the historical AI Agent editorial example; explicitly distinguish example labels from verified factual or quality results.

### Added

- Optional comparison with a caller-supplied actual reply capture; an absent capture is explicitly `not_provided`.
- Optional verification of task-declared review scopes in addition to the global review.
- Isolated delivery-contract regressions and bounded review-order/state-transition checks.
- Evaluator schema v2 migration guidance and explicit delivery-checker observation limits.
- Workflow-only source-use policy, provenance/rights limitations, and positive/negative regeneration controls.
- Six synthetic semantic bad/control pairs for diagnostic review, not automatic quality scores or held-out evidence.
- Actual calibration report exports, two editorial repairs, retained failed reviews and a frozen three-model text diagnostic with its incomplete response; no efficacy claim.
- Offline public-bundle integrity checks and disclosure of heuristic thresholds, reviewer context exposure and partial stage observability.
- Read-only installed-payload comparison against a selected Git commit and safe-update guidance; local variants are never overwritten.

## [v0.1.0](https://github.com/rrrrrredy/research-toolkit/releases/tag/v0.1.0) — 2026-09-04

First public prerelease. Mechanical checks do not establish research quality or general framework efficacy.

### Changed

- Split English and Simplified Chinese README files while keeping one repository and one authoritative `SKILL.md`.
- Renamed evaluator output to schema v2 fields that distinguish mechanical conformance from semantic research quality.
- Made `review` non-zero by default in the evaluator; exploratory runs must opt in with `--allow-review`.
- Made false completion, malformed review logs, and configured source-instruction violations blocking failures rather than near-passing review results.
- Made terminal state bidirectional: `stage: final` if and only if `status: complete`.
- Made the latest global review authoritative and fail-closed on malformed rows, later failures, or open issues.
- Expanded terminal receipt hashes to bind progress, review log, and intended delivery message as well as the report and backstage evidence.
- Reframed the public page and gallery around an agent-agnostic ResearchOps protocol and explicit conformance limits.
- Marked the original July 2026 launch MP4 and slides as historical assets instead of silently presenting them as current.

### Added

- Six regression fixtures for sentence-level keyword stuffing, late review failure, asymmetric terminal state, completion paraphrases, malformed review logs, and PASS records with open issues.
- Source-pack quarantine output and an integrity checker for active/quarantined records and case references.
- A regenerated agent gallery image that includes DeepSeek Harness.

### Verification

- `python scripts/check_docs_sync.py`
- `python scripts/run_dsh_evals.py validate`
- `python scripts/check_eval_source_integrity.py`
- `python scripts/check_regression_fixtures.py`
- `python scripts/check_conformance_fixtures.py`
