# Evaluation evidence and version boundaries

[English](evaluation-status.md) | [简体中文](evaluation-status.zh-CN.md)

**Scheduled first reviews are complete. Their findings inform product improvements; they do not establish general superiority or validate the current plugin/MCP workflow.** This summary uses the retained inventory as of September 21, 2026. Original reports, author failures, original reviews and later interventions remain separate.

## Retained data

| Collection | Evidence | Use boundary |
| --- | --- | --- |
| Development reports | 23 topics; 92/92 complete first reviews | Development feedback; revisions never replace first-submission results |
| Private diagnostics | 50 items from 16 parent topics | Development items, not 50 independent held-out tasks |
| Historical paired study | 11 retained families; 22 complete review inputs; 88/88 valid first reviews; 211 adjudicated findings in 61 necessary issue groups | Bounded historical evidence; original failures and supplemental runs reported separately |
| Public semantic diagnostics | [23 bad/control pairs](../evals/semantic_diagnostics/) | Synthetic failure-mode cases, separate from the private diagnostics |

The paired study originally had 12 families. One was excluded after results were known because required source originals remained unavailable. The current denominator is a post-result exclusion, not the original design or a quality improvement. Those reports are absent from the active collection; the original study and exclusion record remain archived privately.

Of 22 original author attempts in the retained families, 12 failed. Twelve supplemental attempts provided complete reports without replacing those failures. The primary comparison has five families with necessary defects in both conditions and six unresolved families affected by author quota failures. The separate supplemental view has one Toolkit win and ten families with necessary defects in both conditions. The 88 reviews assess 22 inputs, not 88 independent tasks.

## Public scope

The repository includes [calibration reports and model replies](../evals/diagnostics/2026-09-07/), [semantic diagnostics and available reviews](../evals/semantic_diagnostics/), and [offline controls](../evals/README.md). Private full reports, the original review corpus and source packages behind the aggregate counts above are not published here. Public downloads are a subset, not all 92 development reviews or all 88 paired-study reviews.

Reviewer agreement is not accuracy. The historical cohort has already informed development; future reuse is regression/development work, not a new unexposed efficacy test. Human calibration is not a prerequisite for completing the required model reviews.

## Current implementation

The plugin and MCP share one workflow. Local controls exercise stage prerequisites, supplemental requirements, assignment matching, recovery and delivery bindings, including an actual MCP stdio connection with synthetic reviewer processes. They establish tested software behavior, not real-model research quality, provider access or reliable behavior by every host agent.

Plugin `0.1.2` also has a bounded, guided Codex CLI/MCP check with one fictional brief and real `gpt-6-sol` high reviewer and auditor contexts. The audit completed after recovery without rerunning the completed reviewer; the original negative finding, unchanged report and failed attempts were retained. The delivery gate refused the unresolved report defect. Configuration and audit-contract corrections were needed to complete this check. It does not establish unattended operation or a research-quality advantage.

The historical report studies do not measure the later shared plugin/MCP implementation. Combining them with passing software checks does not establish a current general quality or efficiency advantage. A future efficacy comparison needs a separately scoped, frozen design. Fixing software defects and preserving existing first-review findings do not require rerunning historical reports.

[Evaluation standard](report-evaluation-standard.md) · [Claim boundaries and study design](evaluation-roadmap.md) · [Usage and execution limits](usage-modes.md)
