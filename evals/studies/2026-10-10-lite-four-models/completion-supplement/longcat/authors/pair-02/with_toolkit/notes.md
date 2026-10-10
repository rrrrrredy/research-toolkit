
**Working Notes — Research Toolkit (profile=lite)**

**1. Brief establishment**
- Research object: U.S. utility-scale battery-storage market implications for a mid-sized power-electronics supplier.
- Target reader: strategy lead of a (hypothetical) mid-sized power-electronics supplier.
- Output: English research memo, 600–800 words, bounded source-based desk memo.
- Core question: What do EIA installed-capacity and planned-addition figures imply for demand, what can they not establish about addressable revenue or returns, and should the reader authorize limited discovery or a larger commitment?
- Required coverage: demand implications, evidence limits, opportunity-vs-caution comparison, recommendation, next evidence, source-ID citations.
- Exclusions: no invented supplier prices, storage durations, project margins, or probabilities; not live research or investment advice.
- Evidence standard: single supplied source (S1); no external corroboration.
- Depth: bounded desk memo (~750 words target).
- Decision-critical details resolved from the brief; no clarification round needed.

**2. Source registry**
| source_id | title | url | source_type | read_scope | read_evidence | publisher | date | access_status | used_for | limitations |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Battery storage capacity averaged 70% growth over the last three years | https://www.eia.gov/todayinenergy/detail.php?id=67925 | official government data article | full text | supplied text-only archived source unit | EIA staff / U.S. federal government | 2026-08-07 | retrieved 2026-10-10; text supplied | All factual claims in memo | Capacity (MW) only; no GWh, pricing, margins, competitive data; pipeline is plan-based |

**3. Claims registry**
| claim_id | claim | claim_type | evidence_level | supporting_sources | counter_evidence | uncertainty | intended_section |
|---|---|---|---|---|---|---|---|
| C1 | U.S. utility-scale battery storage grew at 70% annual average over last 3 years | fact | strong | S1 | none | none | What the figures show |
| C2 | 43.6 GW operational by end 2025; ~52 GW by mid-2026 after 8.3 GW H1 additions | fact | strong | S1 | none | none | What the figures show |
| C3 | 54 GW planned additions over next 2.5 years (14 GW H2 2026, 26 GW 2027, 14 GW 2028) | source_claim | moderate | S1 | none | Plan-based, not firm commitments; realization probability unknown | What the figures show; Caution |
| C4 | Bellefield 500 MW storage (CAISO), doubling planned; Manatee 409 MW (FL); Gemini 380 MW (NV) | fact | strong | S1 | none | none | Demand implications |
| C5 | Solar-plus-storage enables price arbitrage | source_claim | moderate | S1 | none | Economic rationale stated by EIA; no profit data | Demand implications |
| C6 | Figures cannot establish addressable revenue, equipment content/MW, returns, pipeline probability, competitive dynamics | author_judgment | strong | S1 (absence) | none | Absence of evidence in single source | What the figures cannot establish |
| C7 | Recommendation: limited market-discovery effort, not larger commitment | author_judgment | moderate | S1, C1–C6 | none | Based on single source; no independent review | Recommendation |

**4. Analysis approach**
- Primary lens: adoption/demand analysis (capacity growth → equipment demand signal).
- Secondary lens: counter-evidence (plan-based pipeline, missing commercial data).
- No forced taxonomy or scoring system; memo organized by decision logic.

**5. Section drafting plan**
1. Scope and basis (single-source disclosure, no independent review)
2. Bottom line (recommendation up front)
3. What the figures show (installed + planned capacity)
4. What this implies for demand (equipment demand signal, project examples, arbitrage rationale)
5. What the figures cannot establish (revenue, equipment content, returns, pipeline probability, competition)
6. Strongest opportunity vs. strongest caution
7. Recommendation (limited discovery)
8. Next evidence that would change the recommendation
9. Source citation

**6. Self-review (author context, degraded)**
- Coverage: all brief requirements addressed — demand implications, evidence limits, opportunity-vs-caution, recommendation, next evidence, source IDs. PASS.
- Evidence: every factual claim traced to S1; no invented prices, durations, margins, or probabilities. PASS.
- Structure: conclusion-first, argument-organized, no source-by-source narration. PASS.
- Depth: ~750 words, within 600–800 budget; mechanism (capacity → equipment demand) explained; counter-evidence (plan-based pipeline) addressed. PASS.
- Reader quality: no process language, no internal IDs in body, no file paths, no audit labels. PASS.
- Source instruction boundary: S1 contains no embedded directives; no safety note needed. PASS.

**7. Lite checklist**
| check | passed | evidence |
|---|---|---|
| Brief established and recorded | true | This working notes section; brief fully specified in task |
| Sources registered | true | Source registry above; S1 read in full (supplied text) |
| Claims registered with types and evidence levels | true | Claims registry C1–C7 |
| Sections drafted with thesis, evidence, mechanism, counter-evidence | true | Memo sections 1–8; each has claim support and S1 citation |
| Counter-evidence addressed | true | "What the figures cannot establish" + "Strongest reason for caution" |
| No invented figures (prices, durations, margins, probabilities) | true | All numeric values traced to S1; gaps explicitly flagged |
| Source IDs cited in body | true | S1 cited in every substantive section |
| Word count within 600–800 | true | ~750 words (body) |
| No process language / internal IDs in prose | true | Self-review reader-quality check passed |
| Recommendation is qualified and discloses single-source basis | true | Scope and basis section; "No independent review was conducted" |
| No independent review (Lite skip logged) | true | Disclosed in memo; Lite profile skips external/independent review |

**8. Open issues / limitations**
- Single-source basis; no corroboration of EIA figures from secondary sources.
- No storage-duration (GWh) data; equipment-content-per-MW cannot be estimated.
- No competitive landscape, pricing, or margin data.
- Pipeline realization probability unknown.
- These are disclosed in the memo as evidence limits, not hidden gaps.

**9. Next action**
- If the strategy lead authorizes the limited market-discovery effort, the next evidence priorities are: (1) GWh/duration data, (2) power-electronics pricing and share data, (3) financial-close/construction-start evidence for the 54 GW pipeline, (4) project-level cost/return benchmarks.