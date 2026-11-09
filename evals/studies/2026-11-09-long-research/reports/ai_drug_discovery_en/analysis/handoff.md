# AI drug discovery author-production handoff

Author: Codex agent `/root/ttc_research`. Substantive author only; no independent-review role. Evidence cutoff: 2026-11-09. This author-production task is complete and is ready for the coordinator's independent reviews. Outline acceptance does not imply manuscript acceptance. No model API was called during this continuation, no clinical/model experiment was run, and no product files, software tests, commits or publications were made.

## Manuscript and preservation

- **Current complete English manuscript:** `draft-current.md`, 9,461 whitespace-separated words, SHA-256 `777bd658ef685df11acc14b3e8f5b41babaf77d8151f94b3183a9968e59057ea`.
- **First complete manuscript, retained:** `draft-first.md`, SHA-256 `44458429a2aaeaf9c37275c6b8e4d354a857bd5f33b4f927bc296fca2690bf32`. The current copy corrects typography and spacing found on inspection. The first complete manuscript already used the substantive U1 correction described below.
- `first-draft-manifest.json` records first assembly. `delivery-manifest.json` records current assembly and author identity. `assemble_report.py` and `package_records.py` preserve the actual assembly and packaging work.
- No coordinator-frozen task manuscript was overwritten. The files in this directory are author artifacts for the coordinator to import or review.

The manuscript follows seven named programs: rentosertib, DSP-1181, EXS21546, REC-994, REC-4881, baricitinib and halicin. It includes dated identity/stage chains, discovery mechanisms, prospective experimental evidence, clinical outcomes and attrition, stage-specific comparisons, collaboration rights and economics, and decisions for R&D/business-development/investment teams. The main comparison is small molecules; the oral and inhaled rentosertib branches are kept distinct. The Sanofi and Roche unnamed research deliverables illustrate collaboration handoffs without being inserted into the seven named clinical histories.

## Units, actual reading and calculations

- `U1-rentosertib-revision-01.md` is the current U1. `U1-rentosertib.md` remains the unmodified first unit.
- `U2-clinical-programs-and-attrition.md`: DSP-1181, EXS21546, REC-994 and REC-4881, with their different analysis populations and stopping decisions.
- `U3-repurposing-and-prospective-discovery.md`: baricitinib clinical evidence and halicin prospective screening/animal evidence.
- `U4-comparison-partnerships-decisions.md`: stage comparisons, historical cohort interpretation, ownership/data rights, economic categories and decision implications.
- `reading-ledger.json` contains 43 source records with paths, publication/version dates, actual reading scope, acquisition method and limits. `source-registry.csv` is its tabular counterpart. These records do not equate download success with full reading.
- `claims-registry.json` and `claims-registry.csv` contain 21 central claims with source mappings and material qualifications.
- `supplemental-sources/` preserves obtained HTML/PDF/registry JSON, retrieval metadata and extracted text; original source-pack files remain under the implementation's `sources/` directory. `web-reading/` preserves available selected tool-response captures. Some primary records were read through web extraction because direct download failed; this is recorded rather than represented as a locally inspected full PDF.
- `calculations.py` and `calculations-results.json` preserve the original actual descriptive calculations. `revise_U1_analysis_population.py` and `calculations-results-revision-01.json` preserve the corrected FVC population mapping and arithmetic. Other arithmetic was carried forward rather than rerun as a new experiment.
- `report-opening.md` and `report-appendix.md` provide the opening comparison/identity register and material source distinctions used in assembly.

## U1 independent-review finding and correction

The coordinator relayed a major clinical-domain finding: the first unit placed the observed-case FVC means next to a description of ANCOVA plus multiple imputation, conflating two analyses. I inspected both panels of the original Figure 2 and the registry's absolute-FVC results before revising the unit.

The corrected manuscript explicitly separates:

| Analysis | 60 mg once daily | Placebo | Descriptive subtraction |
|---|---|---|---|
| Observed week-12 cases, Figure 2a | n = 10, +98.4 mL | n = 14, −20.3 mL | 118.7 mL |
| ANCOVA plus multiple imputation, Figure 2b | randomized n = 18, +89.2 mL | randomized n = 17, −8.2 mL | 97.4 mL |

Group confidence intervals are preserved in the unit and manuscript. Neither subtraction is represented as an independently estimated between-group effect with a confidence interval. The 22/71 missing week-12 measurements, high-dose 8/18 versus placebo 3/17, MAR assumption and need for missing-not-at-random sensitivity analysis remain visible. The modeled high-dose group's interval includes zero; that within-group interval is not used as a treatment-contrast test.

`U1-revision-01-notes.json` identifies the preserved originals and new actual reading. `U1-review-handoff.json` supplies source paths for reviewer preparation. The relevant raw files are `supplemental-sources/AIDD-S02/figure-2.png` and `supplemental-sources/AIDD-R01W/download.bin`, in the latter's `resultsSection.outcomeMeasuresModule` absolute-FVC outcome. Original-reviewer confirmation remains with the coordinator; I do not claim independent acceptance of this correction.

## Specific premises useful for independent review

1. **REC-994:** the public stop decision is May 2025; registry result posting on 22 October 2026 is a later evidence layer available at the cutoff. Registry completion does not revive development. Combined safety tables mix controlled-period and extension exposure and are not used as a duration-matched comparison. Sources: `AIDD-S20`, `AIDD-R03W`, original CCM discovery `AIDD-S14`.
2. **REC-4881:** the November 2026 material distinguishes 26 safety participants (5 phase Ib + 21 phase II), 16 efficacy-evaluable, 15 week-13 and 13 week-25 assessments. The conference and earnings presentations are distinct source versions. The natural-history subset is contextual, not a concurrent treatment-effect comparator. Reading-ledger entries `WEB-R4881CGA`, `WEB-R4881EARN`, `WEB-R4881PR`, plus `AIDD-R06` and `WEB-RXRX2025`.
3. **Baricitinib:** COV-BARRIER's primary endpoint failed and mortality inference was nominal under the testing hierarchy; RECOVERY supplied a larger randomized mortality comparison. Raw-proportion differences are distinguished from adjusted hazard/rate ratios. Sources `AIDD-S11`–`AIDD-S13`, corrected original hypothesis `AIDD-S24`, workflow `AIDD-S15`, FDA notice `AIDD-S25`.
4. **Halicin:** the high/low-score prospective library comparison is 51/99 versus 2/63. Halicin was selected from the repurposing library; the 107,349,233-structure ZINC branch is separate, with 8 of 23 compounds active against at least one tested species. Source-pack `AIDD04` is the original paper with methods and supplemental figures.
5. **Contracts:** Sanofi platform IP, program licensing and partner-data use have different scopes; some allocations remain redacted. The $5.2 billion ceiling is contingent, while the October 2026 option milestone is $10 million within $144 million announced aggregate upfront/milestone payments. Roche map/raw-image/program rights concern earlier deliverables than a clinical asset. Source mappings and actual filing-clause reading are in the ledger.

## Material access limits retained

The rentosertib Reporting Summary was obtained and visually inspected; it is not the full protocol or SAP, which were not obtained. The supplementary discovery download that failed is not treated as read. Some issuer PDFs were available only through primary-source web text; no local visual inspection is claimed for those pages. DSP-1181's exact unmet clinical criterion and a reliable trial identifier remain unresolved. The historical AI success-rate paper's public completed-program counts are analyzed, but every supplemental cohort row was not independently re-audited. These limits are localized in the manuscript's evidence appendix and do not replace the substantive findings.

## Coordinator continuation

Use `draft-current.md` as the complete author manuscript. Independent evidence/domain checks and any final task-state import remain coordinator responsibilities. Preserve `draft-first.md`, the original U1 and original calculation result when incorporating changes. This handoff supersedes the older paused `continuation-state.md` for current work status; that earlier snapshot is retained for provenance. The author is ending this turn to release the execution position, with no additional topic selected.
