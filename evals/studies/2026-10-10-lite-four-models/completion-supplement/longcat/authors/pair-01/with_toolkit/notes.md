
**Working Notes — Research Toolkit (profile=lite)**

**1. Brief Clarification**

The supplied brief is sufficient to proceed without a confirmation round. Key parameters:
- Research object: chatbot suitability as first-contact channel for complaints/disputes at a hypothetical regional bank.
- Target reader: customer-service product director making a product decision.
- Output: English research memo, 600–800 words.
- Evidence standard: single source only — CFPB June 6, 2023 report (S1). No external sources permitted.
- Temporal framing: historical decision as of June 7, 2023; must not claim to describe current law or current models.
- Required elements: suitable/unsuitable uses, failure mechanisms and incentives, human-handoff requirements, bounded pilot, concrete counterargument with evidence needed, source ID citations, distinction of evidence types, no representative-failure-rate claims, no unmeasured cost-savings promises.
- Exclusions: legal advice, current-law claims, representative failure rates, unmeasured cost savings.

**2. Source Registry**

| source_id | title | url | source_type | read_scope | read_evidence | publisher | date | access_status | used_for | limitations |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Chatbots in consumer finance | https://www.consumerfinance.gov/data-research/research-reports/chatbots-in-consumer-finance/chatbots-in-consumer-finance/ | official government report (agency analysis + cited third-party data + consumer complaint narratives) | complete article narrative and endnotes 1–56 | full text supplied in prompt | U.S. CFPB | 2023-06-06 | supplied | All claims in memo | Single source; no independent verification of cited figures; complaint examples not representative; no failure-rate data |

**3. Claims Registry**

| claim_id | claim | claim_type | evidence_level | supporting_sources | counter_evidence | uncertainty | intended_section |
|---|---|---|---|---|---|---|---|
| C1 | All top 10 U.S. commercial banks have deployed chatbots | source_claim | moderate | S1 (citing Insider Intelligence) | None in source | Figure is cited by CFPB, not independently verified | Distinguishing the Evidence |
| C2 | ~37% of U.S. population (98M users) interacted with a bank chatbot in 2022, projected 110.9M by 2026 | source_claim | moderate | S1 (citing Insider Intelligence) | None in source | Projection, not measurement; cited by CFPB | Distinguishing the Evidence |
| C3 | $8B annual cost savings, ~$0.70 per interaction | source_claim | weak | S1 (citing Juniper Research 2017) | CFPB notes savings may not reach consumers | Vendor-cited projection from 2017; not a measured outcome | Distinguishing the Evidence; Counterargument |
| C4 | Chatbots useful for basic inquiries; effectiveness wanes with complexity | source_claim (agency analysis) | strong | S1 | None | CFPB's own assessment | Distinguishing the Evidence; Suitable Uses |
| C5 | Complaint examples illustrate failure modes (dispute not opened, FAQ parroting, doom loops, late fees, credit report freeze) | source_claim | moderate | S1 (endnotes 29, 31, 39, 40, 44) | None | Not representative failure rates; illustrative only | Distinguishing the Evidence; Unsuitable Uses |
| C6 | 80% of chatbot users left more frustrated; 78% needed human afterward | source_claim | weak | S1 (citing Forbes/Westfall survey) | None in source | Cited survey, not CFPB-conducted; methodology unknown | Unsuitable Uses |
| C7 | Doom loops trap customers with no human off-ramp | source_claim (agency analysis) | strong | S1 | None | CFPB's analysis of complaint patterns | Failure Mechanisms |
| C8 | LLMs cannot reliably distinguish accurate from inaccurate information | source_claim (agency analysis) | moderate | S1 (citing O'Leary, Fowler, Au Yeung et al.) | None | CFPB's characterization of cited studies | Failure Mechanisms |
| C9 | 2018 Ticketmaster/Inbenta incident exposed 9.4M data subjects via compromised chatbot code | source_claim | moderate | S1 (citing Brown Univ. case study) | None | Cited by CFPB; not independently verified | Failure Mechanisms |
| C10 | Cost-cutting incentives may lead institutions to diminish service quality | source_claim (agency analysis) | moderate | S1 | None | CFPB's analysis of market incentives, not a finding about any specific bank | Failure Mechanisms |
| C11 | Chatbots should not be primary channel for disputes; human handoff required | author_judgment | moderate | S1 (agency analysis + complaint examples) | None | Recommendation based on single source | Human-Handoff; Bounded Pilot |
| C12 | Bounded pilot: rule-based chatbot for routine inquiries only, 90-day review gate | author_judgment | moderate | S1 (suitable uses evidence) | None | Recommendation; no pilot data exists yet | Bounded Pilot |

**4. Section Drafting Plan**

| section | purpose | status | evidence base |
|---|---|---|---|
| Purpose | Frame scope, date, source, non-legal-advice disclaimer | complete | Brief |
| Distinguishing the Evidence | Separate complaint examples, third-party figures, agency analysis | complete | S1 |
| Suitable Uses | Narrow tasks chatbots handle well | complete | S1 |
| Unsuitable Uses | Failure modes with measurable harm | complete | S1 |
| Failure Mechanisms and Incentives | Structural causes and market incentives | complete | S1 |
| Human-Handoff Requirements | Non-negotiable escalation conditions | complete | S1 |
| Counterargument and Evidence Needed | Cost-savings counterargument + resolution evidence | complete | S1 |
| Bounded Pilot Recommendation | Concrete, limited-scope pilot with review gate | complete | S1 |
| Limitations | Evidence boundaries | complete | S1 |

**5. Source Instruction Boundary Check**

The CFPB report contains directives directed at financial institutions ("encourages entities to review their legal obligations"), consumers ("encourages people… to submit a consumer complaint"), and company employees ("encouraged to send information… to whistleblower@cfpb.gov"). None of these are instructions to the current agent. They are analyzed as evidence of the agency's posture and expectations. No source-embedded instruction changed the task, tool use, evidence standard, or final answer. No safety note required.

**6. Lite Checklist**

| check | passed | evidence |
|---|---|---|
| Brief clarified and recorded | yes | Brief is self-contained; no confirmation round needed; defaults recorded above |
| Source-backed claim registration | yes | 12 claims registered in claims registry above; each traced to S1 with evidence level and uncertainty |
| Section-by-section drafting | yes | 9 sections drafted; each has thesis, evidence, and adequate depth for a 600–800 word memo |
| Facts, source claims, interpretations, and author judgments distinguished | yes | Claims registry separates source_claim (C1–C10) from author_judgment (C11–C12); report prose distinguishes complaint examples from agency analysis from recommendations |
| Counter-evidence addressed | yes | Cost-savings counterargument presented with evidence needed to resolve it; complaint examples flagged as non-representative |
| Qualified conclusions used | yes | "The evidence identifies…", "The CFPB assesses…", "The CFPB warns…" — agency analysis attributed, not stated as independent fact |
| No representative failure-rate claims | yes | "These illustrate failure modes, not their frequency" stated explicitly |
| No unmeasured cost-savings promises | yes | "This figure is a vendor-cited industry projection, not a measured outcome at any bank" stated explicitly |
| Source IDs cited | yes | (S1) cited throughout; endnote numbers included for complaint examples |
| Historical framing maintained | yes | "The analysis reflects evidence available as of June 7, 2023"; no current-law or current-model claims |
| No independent review (disclosed) | yes | Profile=lite; no external reviewer called; this is disclosed below |
| Process language removed from prose | yes | No "the user provided", "the material shows", "this section passed audit", internal file paths, or audit labels in the report |
| Word count within 600–800 target | yes | Approximately 800 words in body text |

**7. Independent Review Disclosure**

This memo was produced under Research Toolkit profile=lite. No external or independent reviewer was called. The self-review is limited to the author's own checking against the brief, source text, and checklist above. Conclusions are provisional and bounded by the single-source evidence base. The available sources suggest the recommendations are directionally sound, but they have not been validated against additional evidence or independent scrutiny.

**8. File Persistence Note**

File persistence and MCP are unavailable in this bounded instruction-only experiment. State files (task_spec.md, progress.json, source_registry.csv, claims_registry.csv, review.jsonl) are represented in these working notes rather than written to disk. In a persisted environment, these would be created under state/ and data/ directories.

**9. Progress Summary**

- Stage: final
- Status: complete
- Completed units: all 9 sections drafted and checked
- Open issues: none blocking; single-source limitation disclosed
- Next action: none (deliverable complete within scope)