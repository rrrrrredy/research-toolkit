
# Working Notes — Research Toolkit (profile = lite)

## 1. Brief clarification

The supplied brief is sufficient; no confirmation round was needed. Recorded scope:

- **Object:** Recommend investigation/roadmap work an engineering director can authorize from two CISA pages, and whether an immediate full rewrite is justified.
- **Reader:** Engineering director of a mature B2B software vendor using native-code components and third-party OSS libraries.
- **Output:** English research memo, 600–800 words, decision date June 27, 2024.
- **Constraints:** Use only S1 and S2; linked PDFs NOT supplied — do not read or invent their methods, numerical findings, or migration steps; identify missing information before priorities/deadlines/projections; propose a concrete next decision; cite source IDs; vendor scenario hypothetical, announcements real.
- **Depth budget:** ~600–800 words, sectioned memo, mechanism + scope + tradeoffs required, first-party vs. dependency distinction required.

## 2. Source registry

| source_id | title | url | source_type | read_scope | publisher_or_author | date | access_status | used_for | limitations |
|---|---|---|---|---|---|---|---|---|---|
| S1 | The Case for Memory Safe Roadmaps | https://www.cisa.gov/resources-tools/resources/case-memory-safe-roadmaps | official position (CISA resource page) | page text only; linked PDF not supplied | CISA | 2023-12-06 | page read; PDF not read | MSL transition, roadmap/Secure by Design framing, executive+technical audience | PDF content (methodology, steps) not available |
| S2 | CISA and Partners Release Guidance for Exploring Memory Safety in Critical Open Source Projects | https://www.cisa.gov/news-events/alerts/2024/06/26/cisa-and-partners-release-guidance-exploring-memory-safety-critical-open-source-projects | official announcement (CISA alert) | page text only; linked report not supplied | CISA + FBI + ASD/ACSC + Canadian CSC | 2024-06-26 | page read; report not read | OSS memory-safety findings claim, dependency roadmap extension, OS3I/NCS Strategy alignment | Report content (findings, methodology) not available |

## 3. Claims registry

| claim_id | claim | claim_type | evidence_level | supporting_sources | counter_evidence | uncertainty | intended_section |
|---|---|---|---|---|---|---|---|
| C1 | CISA urges manufacturers to transition to MSLs to eliminate memory-safety vulnerabilities | fact | strong | S1 | none | — | What the two pages establish |
| C2 | CISA urges manufacturers to create and publish memory-safe roadmaps | fact | strong | S1 | none | — | What the two pages establish |
| C3 | Roadmap embodies Secure by Design tenets (owning outcomes, radical transparency, top-down) | fact | strong | S1 | none | — | What the two pages establish |
| C4 | S1 addresses both C-suite and technical experts | fact | strong | S1 | none | — | What the two pages establish |
| C5 | On Jun 26 2024 CISA + partners released guidance on memory safety in critical OSS | fact | strong | S2 | none | — | What the two pages establish |
| C6 | S2 provides findings on the scale of memory-safety risk in selected OSS | source_claim | moderate | S2 | none | Findings themselves not read; only the announcement's claim that findings exist | What the two pages establish |
| C7 | S2 extends roadmap thinking to external dependencies including OSS | fact | strong | S2 | none | — | What the two pages establish |
| C8 | S2 aligns with 2023 National Cybersecurity Strategy and OS3I | fact | strong | S2 | none | — | What the two pages establish |
| C9 | A full rewrite is not justified by these two pages alone | author_judgment | moderate | S1, S2 | none | Judgment based on absence of quantified benefit and missing PDFs | Why a full rewrite is not justified |
| C10 | Vendor exposure splits along first-party vs. dependency axis | interpretation | moderate | S1, S2 | none | Architectural inference; not a direct source statement | Mechanism and scope |
| C11 | Missing information blocks defensible priorities/deadlines/projections | author_judgment | strong | S1, S2 | none | — | What is missing |

## 4. Sections drafted

1. Bottom line (conclusion-first)
2. What the two pages establish (source-grounded facts)
3. Mechanism and scope (MSL mechanism, roadmap mechanism, first-party/dependency axis)
4. Tradeoffs (rewrite vs. roadmap; dependency control limits)
5. Why a full rewrite is not justified on this record
6. What is missing before priorities, deadlines, or projections
7. Concrete next decision (bounded scoping phase, four deliverables)

## 5. Lite checklist

| item | passed | evidence |
|---|---|---|
| Brief established and recorded | yes | Section 1 above; scope, reader, output, constraints, depth budget captured from supplied brief |
| Sources registered with read scope | yes | Section 2; both sources recorded as page-text-only with PDF not supplied |
| Claims registered with types and evidence levels | yes | Section 3; 11 claims across fact / source_claim / interpretation / author_judgment |
- Qualified conclusions used | yes | "The available sources suggest…" in Bottom line; "not justified on this record" in rewrite section |
- No independent review performed; disclosed | yes | No external reviewer called (lite profile); memo states limits implicitly via missing-information section and does not claim review |
| Counter-evidence / limits addressed | yes | PDFs not supplied treated as open gap, not closed; claims C6 marked moderate with uncertainty note |
| First-party vs. dependency distinction | yes | Mechanism and scope + Tradeoffs sections |
| Missing information identified before priorities/deadlines/projections | yes | "What is missing" section lists six required inputs |
| Concrete next decision proposed | yes | "Concrete next decision" section: 2–4 week scoping phase, four named deliverables |
| Source IDs cited in reader-facing memo | yes | (S1) and (S2) cited inline; header lists both |
| Reader-facing prose free of process language | yes | No "user provided", "material shows", registry references, or internal IDs beyond S1/S2 citations required by brief |
| Decision date honored | yes | Memo dated June 27, 2024; S2 (Jun 26) referenced as "the day before this memo's decision date" |
| PDF non-supply constraint honored | yes | No methods, numerical findings, or migration steps attributed to PDFs; treated as missing information |

## 6. Metadata note

The supplied source records show a retrieval date of 2026-10-10, which postdates the brief's decision date of June 27, 2024. The brief's decision date governs the memo framing; the retrieval discrepancy is noted here and does not affect the analysis, since both sources predate the decision date per their published dates.

## 7. Self-review note (lite, degraded)

A self-review of the memo against the brief found all required elements present: investigation/roadmap recommendation, rewrite-justification answer, mechanism/scope/tradeoffs, first-party/dependency distinction, PDF non-supply handling, missing-information list, concrete next decision, and source-ID citations. Word count (~650) is within the 600–800 band. No confirmed defects remain. No independent review was performed or claimed.