# Changelog

[English](CHANGELOG.md) | [简体中文](CHANGELOG.zh-CN.md)

Released changes are grouped by tag. `Unreleased` describes work not yet included in a published version.

## Unreleased

## v1.4.2 — 2026-10-22

- Ship PR #94's `research_save`, CLI save and collect guidance: distinguish actual `read_scope` from required `reading_requirement`, document its two allowed values and its pairing with `required_source_ids` after partial-update merging.
- Clarify local `read_evidence` paths and the existing `locator` field; preserve supported reference forms and optional `evidence_path`. Synchronize English, Chinese and plugin copies without changing interfaces, validation rules or task formats.
- Publish matching bilingual [release notes](docs/releases/v1.4.2.md), version metadata and plugin ZIP. Archived failing and corrected requests support the examples; reduced rework remains unverified. Reuse PR #94's completed checks without replaying research tasks.

## v1.4.1 — 2026-10-22

- Ship PR #91's revised default entry: understand the user's requirements, follow instructions and develop a useful research answer. Remove guidance that asks users to remind or dispatch the Agent.
- Load existing methods as needed. Move review configuration, record fields and delivery details into existing reference documents; synchronize English, Chinese, Framework pages and plugin copies without adding a workflow or required step.
- Publish matching bilingual [release notes](docs/releases/v1.4.1.md), version metadata and plugin ZIP. The standalone Skill `quick_validate.py` check remains incomplete because PyYAML is unavailable. Improvements in instruction following, user effort and research quality remain unverified; shorter documentation is not evidence of those benefits.

## v1.4.0 — 2026-10-21

- Add optional partial `research_save.brief` updates and explicit `draft.main` / `draft.kind` selection. Preserve custom specification sections and historical receipts; a revised main artifact cannot reuse the wrong delivery.
- Return runtime identity and current-work references at resume, without claiming that the host loaded the displayed Skill or that a file hash proves quality.
- Validate active reading requirements when saving, preserve explicit legacy waivers, and distinguish imported reviews from actual model calls, self submissions, timing and usage.
- Add bilingual continuity guidance, 14 targeted tests and 12 independently constructed semantic diagnostics. An independent code review found three defects, which were corrected and tested.
- Synchronize the plugin and bilingual [release notes](docs/releases/v1.4.0.md). The three-mode short-task probe found no answer-quality advantage; managed execution took more time and tokens. Long-task benefits remain unverified. Nine tools and existing task formats remain compatible; no mandatory new input or migration.

## v1.3.3 — 2026-10-20

- Ship the exact repeated-paragraph advisory from PR #85: `check-draft` returns original prose, headings and every line range in existing `warnings`. It does not change `ok`, delivery eligibility or report contents.
- Ship the Lite analysis guidance from PR #86: choose comparison, explanation or decision methods as needed, with a short example from archived synthetic SaaS materials. English, Chinese and plugin copies stay synchronized; no fixed report structure is required.
- Reduction in false self-check passes and improvements in research quality remain unverified. The archived public-library comparison found no false passes in either v1.3.1 or v1.3.2 and no incremental benefit in that case.
- Publish matching bilingual [release notes](docs/releases/v1.3.3.md), version metadata and plugin ZIP. Reuse completed implementation checks; no new tools, required fields, calls or task migrations.

## v1.3.2 — 2026-10-19

- Ship the corrected Lite self-check instructions and diagnostics from PR #81 and PR #82 in the installed plugin: read the current report, address repeated or off-topic passages, and record concrete findings instead of changing a pass flag to satisfy an error.
- Keep the six checklist items, validation predicates and public interfaces unchanged. The effect of these wording changes on false self-reported passes remains unverified.
- Align bilingual repository, installation, plugin and website descriptions with the existing nine MCP tools; the tool count is unchanged from v1.3.1.
- Preserve original reports and historical results alongside four separate report revisions and current-result corrections. These are report repairs, not a Toolkit core-capability upgrade. Publish matching bilingual [release notes](docs/releases/v1.3.2.md), version metadata and plugin ZIP without new runtime logic or tests.

## v1.3.1 — 2026-10-16

- Fix public release-log address filtering: normalize hostnames, reject non-public DNS results and connect to the checked address while retaining hostname-based TLS verification. Requests now connect directly; proxy-only environments may return a read failure.
- Include the merged shared paragraph context in `save`, `status` and release-log queries; reuse identical context within each response while preserving claims, sources, match reasons, headings and line numbers.
- Synchronize the nine-tool descriptions and plugin package. Include the already-merged bounded-verification guidance and removal of public corpus pages and entry points.
- Publish matching bilingual [release notes](docs/releases/v1.3.1.md), version metadata and a plugin ZIP. Reuse completed implementation checks; release preparation adds no runtime logic or tests.

## v1.3.0 — 2026-10-16

- Return saved supplemental requirements when explicitly entering analysis or drafting, retaining their text, status and evidence without requiring a second copy in the brief.
- Add the already-merged CLI `check-updates` / MCP `research_check_updates` for registered public release logs: return changes, source dates and related report locations; distinguish unchanged content from read failures.
- Align local source-path validation between draft and delivery checks, with the exact field and a valid relative-path example in errors.
- Include the merged bilingual reading pages, report-update case, external run records, and optional Research Review / AI industry corpus links. Materials and archived runs remain separate from product capability claims.
- Synchronize release metadata and the generated plugin. See the [release notes](docs/releases/v1.3.0.md) for existing validation results and remaining limits; no runtime implementation changes are introduced by the release commit.

## v1.2.0 — 2026-10-15

- Add advisory record differences and source-linked claim/report locations to `save` and `status`, skip byte-identical writes, and exercise the public CLI in a real long-report update with bilingual guidance and plugin synchronization.

- Archive Astra's separate-context review of the long-report continuation and clarify the response-byte serialization method; preserve the original report and measured results.

- Let local self-review callers request the frozen assignment by file reference with `include_assignment: false`, retaining complete inputs, freshness checks and the default inline response.
- Publish an actual long-report continuation with reused records, source-confirmed changes, preserved self-review repair and observed costs; synchronize bilingual usage guidance and plugin payload.

## v1.1.0 — 2026-10-14

- Add `research_save` / CLI `save` for agent-owned record updates, format recovery with original backups, and draft saves. Observe draft timestamps, failed attempts, reviewer timing and returned usage without new acceptance gates.

- Fix Lite actual-reply capture comparison and current completion checks while preserving retained checklists; align bilingual Skill, plugin discovery and website profile guidance.

- Clarify in-range pending length records without changing checks; add a non-overwriting CLI capture example and reuse guidance, and recommend Full for version-bound review and delivery needs.
- Publish one complete native-Agent/Toolkit Full comparison: retain both first/final pairs, tied Astra blind judgments, startup failures and actual resource use; no report-quality advantage observed on this task.
- Keep research CLI JSON input/output in UTF-8 on Windows, including review packets containing private citation characters; fix the failure observed in an actual long-report workflow.
- Validate version manifests and parent paths before any plugin build writes; exercise real CLI file/directory symlink and Windows junction failures without partial version updates.
- Extend advisory citation checks to file citations and file lists, and exempt indented code examples while preserving prose warnings and line numbers.
- Fix deletion/rename synchronization for generated plugin files with ownership tracking, preservation of unmanaged content and cross-platform controls.
- Present Lite/Full alongside each other by task, share the research baseline and document report revision, source updates and Lite-to-Full continuation; correct plugin tool counts and reviewer-tier descriptions.
- Add draft advisories for private chat citations in either profile without new delivery gates or changed historical receipts.

- Add substantial-report examples, Full guides, research requests and length templates to the bilingual README and website.
- Install MCP with a virtual environment and absolute interpreter path; add Windows/Linux troubleshooting and field-specific length errors without changing counting or acceptance rules.

## v1.0.0 — 2026-10-13

- Establish the public 1.x compatibility policy for documented CLI/MCP interfaces, saved tasks and installation requirements; publish matching English and Chinese guides.
- Include the policy in the plugin and synchronize all release metadata. Runtime behavior remains the same as v0.2.7; no task-data migration or new model evaluation is required. [Release notes](docs/releases/v1.0.0.md).

## v0.2.7 — 2026-10-13

- Block Lite completion when recorded required work remains open; preserve lightweight author checks.
- Preserve neutral source identity in new blinded inputs for both roles.
- Align installed repair instructions and task-dependent Full methods; share concrete reasoning checks across profiles.
- Correct current bilingual task descriptions and map all evaluation collections to product changes and targeted verification.

## v0.2.6 — 2026-10-13

Complete named-company research, public data scope and current task/reviewer policy. [Release notes](docs/releases/v0.2.6.md).

- Complete the 5,244-character pipeline report; fresh-context Astra passes R01–R13, with first-review revisions and versions retained.
- Correct bilingual current-case wording, guidance and runtime prompts; perform an Astra blind recheck of four changed inputs and synchronize web/plugin payloads.
- Publish the associated data repository; all 19 releases and 79 assets pass anonymous access checks. Update public scope for historical development and paired-study records.

## v0.2.5 — 2026-10-13

Complete-report rerun, evaluation reviewer correction and synchronized installation payload. [Release notes](docs/releases/v0.2.5.md).

- Publish the seven dedicated complete-report rerun: 15 actual Astra calls, six first-review passes, one retained 6,020-character failure and its accepted 5,987-character stage revision. Preserve open pipeline requirements, exact author/judge sources and every original call. Add read-only evidence verification to Linux/Windows CI; do not relabel the accumulated-requirement run as live 13-turn or MCP execution.

- Remove implicit auditor creation for new evaluations: one configured independent reviewer is sufficient unless an audit is explicitly configured. Preserve saved audited-plan requirements and original negative reviews. Synchronize bilingual guidance, web instructions and the packaged runtime, and correct the earlier overbroad completion statement. The seven complete-report rerun is tracked separately from offline software checks.

- Correct omissions in the dedicated seven-case Toolkit evaluation set: generate current Astra review/repair instructions for every task and remove the long-horizon case's three-review-row minimum. Verify that one complete current review passes while missing or negative reviews fail. Update bilingual dataset/case inventories, v2 calibration status and example-reuse guidance. Preserve original questions, evidence and dated model outputs; these offline checks do not claim a full model rerun of all seven cases.

## v0.2.4 — 2026-10-13

Reliability fixes, draft preflight, simpler review/repair and synchronized bilingual materials. [Release notes](docs/releases/v0.2.4.md).

- Complete the bilingual correction audit across evaluation entry points, research guidance, web instructions and the packaged plugin: replace stale four-reviewer and no-repair directions with Astra review and direct defect repair, link the completed calibration and task recheck, and list all seven MCP tools. Preserve original historical evidence and specify release preparation as the next step.

- Complete a four-task old/new repair recheck: 31 requests, all failures retained, ten maintainer corrections, and 16 final versions with measured length and corresponding Astra acceptance. Correct source-provenance masking in the separately recorded repair review.

- Use Astra in separate author/reviewer contexts without requiring different model IDs, outside reviewers, outside task authors or a fixed panel. Recognize existing independent tasks and real executed tests; simplify repair guidance and optional comparisons. Record two corrected reports accepted by Astra, retaining its first negative review and the subsequent repair.

- Add local draft preflight through CLI/MCP with actual counts, explicit range diagnostics and no state/receipt changes. Preserve count details on failed Lite delivery. Document failure ownership, source-based repairs and stopping rules; retain evaluation originals and quality limitations.

- Preserve the October 12 four-model first-attempt evidence and source checks (72 requests, four missing pairs, six swap preference changes). Correct prospective Lite instruction selection, explicit JSON notes types and bilingual concise constraint/provenance guidance. Eight new October 13 probes parse, but only three meet length and source errors remain; test five real length failures plus two editorial controls against the existing delivery gate. No prompt-only completion guarantee or general quality-benefit claim.

- Add explicit provider thinking settings and a fresh, tool-disabled native Codex judge transport with frozen adapter hashes. Retain dated four-provider/Astra connectivity failures and follow-up, plus 12 Astra calibration attempts across four families: preferences and valid ties match, while three dimension scores vary under swapping. Publish raw evidence, source adjudication and read-only verification; no general efficacy claim. At that stage add task-intake guidance and clarify contributor counting, data rights and platform checks; task selection is now an optional record that permits direct reuse of existing tasks.

- Make CLI missing/unknown argument errors actionable before mutation and identify incomplete source/claim records by file, ID and fields. Add Python 3.10 CLI/MCP CI alongside existing Linux/Windows checks and clarify interpreter and request setup in both languages.

- Measure explicit whole-artifact word/character ranges from requirement records for Lite and Full, retaining actual counts and rejecting false satisfied claims before receipt writes. Record decision actors and original report/response hashes for new ordinary-review dispositions, preserving legacy attempts and original criticism. These checks establish record consistency, not research quality or identity authentication.

- Expand public judge controls to four bilingual families with exact label reversals and valid ties (12 packets). Add read-only hash, input, length and excerpt checks with corruption tests on Linux/Windows; preserve the original arithmetic inputs. This entry records the initial input release; the October 12 Astra calibration subsequently completed 12 real calls on these four independent task families, with inputs and actual results retained separately.

- Bind new Lite completion receipts to research inputs and optional local checklist evidence files. Source, registry, task or requirement changes now make delivery stale without rewriting the old receipt; legacy receipts disclose their narrower binding scope. This adds no reviewer or Full gate and does not certify checklist semantics.

- Pin reviewer/auditor instructions in new workflow review plans so reference upgrades do not invalidate pending recovery or repeat completed reviews. Ordinary explicit revisions adopt current instructions; frozen evaluations and legacy version checks retain their boundaries.

- Add opt-in development protocol v2 with predeclared report/notes parsing, model aliases, format options, failure categories, code-bound freezes, request ceilings and secondary A/B swaps. Supply five exposed real task families using constructed source materials and separate length-matched judge controls; preserve historical inputs and results. No new model calls or quality claims.

- Add a bilingual improvement plan covering reliability, usability, methods, masking, task design and feedback. Share local task locks across CLI/MCP/Python, retain invalid-encoding reviewer bytes without misclassifying execution, add Windows runtime CI, and correct Chinese reference links.

- Keep study integrity checks active under optimized Python, cover completion evidence and frozen outcome labels, and make summary commands read-only by default. Preserve historical data and tables; document the former verifier coverage and unresolved-count field limitations in dated bilingual corrections.

- Require HTTPS for remote generic reviewers and allowlist the local DSH smoke environment. Add source-text paths to new task templates; clarify ordinary revision calls, separate completed reviews from delivery readiness, and report stale completed tasks without rewriting historical receipts. Exercise template-based CLI and packaged MCP revision/delivery flows with synthetic reviewers; no report-quality improvement is inferred.

- Turn observed Lite pilot defects into bilingual guidance for length checks, faithful paraphrases, attributed claims and justified decision criteria, with links to preserved samples. Prioritize substantive corrections in the Chinese showcase and keep existing case links working. These changes have not yet been evaluated for report-quality gains.

- Give Lite a shared bilingual stage guide, returning only the current stage without Full review or delivery instructions. Make profile selection explicit across Skill, MCP and plugin entry points while preserving Full defaults and saved task profiles. Keep source/claim prerequisites and the six-item author checklist; deterministic checks do not establish improved report quality.
- Publish a four-model, five-family fixed-source Lite pilot with judgments for all 20 model–task pairs, readable supplemental reports, raw outputs and offline verification. Preserve all original failures and valid judgments; document the separate format and completion supplements. This does not establish a general quality advantage.
- Keep the evaluation link alongside the other README navigation links, without an arrow.

## v0.2.3 — 2026-10-10

Current package version, sourced from `VERSION`. Since v0.1.3: Lite tasks, three review tiers, portable reviewer backends, six CLI/MCP workflow tools, stronger evidence/version checks, bilingual onboarding and public case navigation. [Release notes](docs/releases/v0.2.3.md) summarize the changes below. These changes do not establish general efficacy. The v0.1.4 prerelease was withdrawn; historical release records remain unchanged.

Package manifests are synchronized from `VERSION`; the version check also requires matching English and Chinese changelog entries and release notes.

### Getting started

- Add copyable MCP client setup and a locally captured start-to-finish example, plus instructions for recording a demo.
- Shorten the English Skill description for directories and give the Chinese Skill its own translated description.
- Add offline reproduction of the existing calibration archive and a seeded, blinded pairwise pilot harness; the new protocol has no collected results.

- Put a copyable Lite task near the top of both READMEs: supplied sources, a short report, source/claim records and a checklist, with a 5–15 minute walkthrough estimate.
- Add shorter client setup cards and official documentation links, including OpenCode and desktop work agents; distinguish native installation from file/text input and document unavailable integration details.
- Explain when each of the six workflow tools is useful or skippable, including an instructions-only path without MCP.
- Add an index for the existing fictional example and make failure-case submissions and four small first-contribution ideas easier to find.

### Profiles, review backends and contributions

- Add a bilingual Lite quickstart with two explicitly fictional source notes; expose it in README and Pages without requiring a reviewer backend.
- Center the evaluation summary on observed findings and consolidate matching/blinding limits. Add a prospective paired-study template and versioned defect tags for existing diagnostics; no new efficacy results are claimed.

- Surface public comparisons and historical aggregates in README, explicitly marking missing matched-condition and blind-review evidence.
- Add Lite with brief, claims, section drafting and a final checklist; log skipped review and full delivery gates while retaining Full checks.
- Add self, external and independent review tiers with configurable CLI/compatible HTTP backends; new tasks without a backend use degraded self-review, while declared independent requirements never silently fall back.
- Add local backend configuration checks, advisory bilingual PR reminders and a failure-case form without changing original evaluation material or directory structure.

### Changed

- Plugin 0.2.3 replaces abstract briefing questions with agent-proposed coverage, concrete research outcomes and decision-specific clarification across the Skill, plugin and shared CLI/MCP prompts.

- Plugin 0.2.0 defaults to one content reviewer for ordinary reports; independent audits remain available through configuration and stay required for existing audited plans and evaluations. Preserve negative reviews, required corrections and version bindings.
- Make detailed process history optional; separate research-dataset navigation from Toolkit software checks without changing samples or results.

- Preserve Unicode line and paragraph separators inside reviewer JSONL messages; retain incomplete-turn and malformed-record rejection.

- Specify review validity, report readiness and permitted sampling dispositions separately in the model audit assignment.

- Preserve hash-bound plan history for authorized report-delivery reviewer changes; distinguish legitimate retired slots from unknown records without rerunning completed reviews. Frozen evaluations retain their required slots.
- Validate local reading-evidence paths, file existence and nonempty content at stage and required-reading checks; retain URL and section/page locators.

- Reject empty source/claim placeholders and unresolved source references before stage advancement.
- Bind supplemental requirements to both review contexts and delivery; match cached results by reviewer assignment, preserving original replies and timeout-only recovery.
- Check reviewer configuration, executables and default CLI login at task start without model calls; publish bilingual historical evaluation status and version boundaries.

- Add a repository-distributed plugin and local MCP server sharing one workflow for brief clarification, stage guidance, effective review execution and checked delivery. Preserve the standalone Skill.
- Execute reviews in fresh configured processes, retain original replies and failures, audit validity and sample content. Resume missing work without rerunning valid negative evaluations. Publish bilingual installation, account-use and capability guidance.
- Check package/source consistency and exercise the MCP protocol with synthetic reviewer subprocesses; these checks make no model-quality claim.

- Shorten the bilingual Skill entry points and route detailed methods by research stage. Preserve the complete research standard in references and synchronize the web entry point.
- Make the agent responsible for eliciting missing research requirements and executing the workflow. Resolve critical choices before dependent work; use recorded defaults only for non-critical details, without a fixed question count.

- Add standalone Simplified Chinese versions and consistent language navigation for current research references, review and delivery interfaces, evaluation guides, setup instructions and maintenance documentation.

- Require effective model-review completion with original response and execution bindings, independent adjudication and sampling. Separate valid negative evaluation results from report-delivery readiness. Delivery contract 3 checks declared review slots; explicitly labelled versions 1 and 2 preserve historical record inspection.
- Define review perspectives and working standards, failure recovery, reviewer audits and sampling of passed material in the Skill, role reference and bilingual introductions.

- Explain research steps, failure modes, evaluation prerequisites and study configurations consistently across both READMEs and the web guide. Include tool-specific troubleshooting, recovery instructions and setup checks in the adapter guides.

- Clarify the planned single-author review lane: Astra writes with the framework in Codex; fresh-context GPT-5.6 Sol high, DeepSeek, Kimi and subsequently added GLM-5.3 review each required first submission. Preserve earlier three-reviewer freezes and label the fourth review as a later addition. Disclose the supported Coding Plan client and its context/usage boundaries. Missing reviews remain incomplete, critical disputes need evidence, and no human-review prerequisite or human-calibration claim applies. Require accepted improvements to be verified before new author/judge runs; preserve frozen historical protocols and separate LLM judgments from deterministic results. This is a study plan, not new efficacy evidence or a model dependency of the framework.
- Rename the project to Research Toolkit / 研究工具箱 and the repository and Skill identifier to `research-toolkit`. Update current documentation, installation examples, Pages links, and the owner's Profile entry. Preserve historical study inputs and release records.
- Rewrite both READMEs and the bilingual setup guide around concrete actions: give the agent the repository link, upload files if needed, or follow its installation guide. Explain saving and reopening task files in plain language. Keep research steps and their requirements unchanged.
- Remove launch-marketing copy, badges, gallery images, and video assets from the repository and public page.

### Fixed

- Plugin 0.2.2 sends the existing content-review methods to the reviewer instead of only naming review dimensions. Reuse the shared role reference and assignment bindings without extra review calls or changes to historical evaluations.

- Plugin 0.2.1 accepts evidenced no-change decisions for ordinary report findings while retaining original criticism, version bindings and unresolved blockers. Reuse the existing review log and finish tool without additional model calls.
- Align stage outputs with optional research notes and uncertainty records.

- Apply source, reading and claim prerequisites at review and delivery; include declared necessary evidence automatically and bind originals, extracts and delivery receipts to their versions.
- Preserve completed state and receipts when replaying unchanged reviews; include independent global audit failures in report-readiness checks while preserving valid negative evaluations.
- Terminate local reviewer descendants on timeout using process groups or Windows jobs, retain cancellation boundaries, and align source field names in both workflow guides.

- Validate every receipt-bound file even after deletion, including optional and additional inputs; retain task-directory path boundaries.
- Reuse validated JSONL records and report malformed or unreadable case inputs as failures without interrupting other cases. Parse source and claim CSVs as records, validate their structure, and match each source ID to its title in the same row.
- Preserve draft qualifiers in completion checks and detect repeated English sentences while retaining common abbreviations, decimal numbers, and URLs.
- Read HTML encoding only from actual meta declarations, retain caller/BOM precedence, and expose conflicting declarations.
- Remove runtime-specific adapter claims from the general evaluation roadmap.

- Reject missing required evaluation files regardless of the numeric score or whether delivery checking is enabled. Directories cannot satisfy required file entries; complete inputs retain their passing behavior.

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
