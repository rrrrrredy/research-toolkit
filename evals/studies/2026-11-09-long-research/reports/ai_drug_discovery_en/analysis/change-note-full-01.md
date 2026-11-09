# Full-report author revision 01

Author: Codex /root/ttc_research; original substantive author, not an independent reviewer.
Recorded: 2026-11-09T14:54:58.082790+00:00.

Input: `C:\Users\luosong03\Documents\ChatGPT\Others\work\toolkit-long-research-20261109\evals\runs\2026-11-09-long-research\tasks\ai_drug_discovery_en\reports\current.md`
Input SHA-256: `4645728a2c1f4b18f13c8c42839d3610b4ec0ebdad5596efa38adc2983417f3c`
Output: `C:\Users\luosong03\Documents\ChatGPT\Others\work\astra-api-current-chat-20261109\work\implementation\research\ai_drug_discovery_en\codex-production\draft-revision-full-01.md`
Output SHA-256: `30c18ece513b127e7c15ad1afe28a5da7a54ddb7932581785acfbd8d07420507`

## Finding disposition

- AIDD-FULL-EV-01 and AIDD-FULL-DOM-B-01: Changed hundreds of design-make-test iterations to hundreds of compounds synthesized and tested through repeated two-week feedback cycles. The 350th compound, less-than-twelve-month interval, nomination endpoint and exclusion of safety evaluation remain unchanged.
- REC-4881 populations, exclusions and excised-polyp handling remain unchanged; no new evidence search was performed.

## Review and original-source reading

- Read `C:\Users\luosong03\Documents\ChatGPT\Others\work\astra-api-current-chat-20261109\work\implementation\research\ai_drug_discovery_en\native-full-reviews\evidence\response.json`; SHA-256 `3eefe1ead6e6b1a48d2ab2bdd4d77413991c23ea373a6e5e0743e8b3e9be269c`. Relevant findings: AIDD-FULL-EV-01, AIDD-FULL-DOM-B-01.
- Read `C:\Users\luosong03\Documents\ChatGPT\Others\work\astra-api-current-chat-20261109\work\implementation\research\ai_drug_discovery_en\native-full-reviews\domain-1\response.json`; SHA-256 `460c9cceb140b284b4068359923d3453ee1a3fcd99fe5ff35ae792a2db8cf55c`. Relevant findings: AIDD-FULL-EV-01, AIDD-FULL-DOM-B-01.
- Actually read `C:\Users\luosong03\Documents\ChatGPT\Others\work\astra-api-current-chat-20261109\work\implementation\sources\AIDD06\original.txt`: PDF p.4, extracted lines 274-305: two-week feedback cycles, 350th compound and 350 compounds synthesized/tested; exploratory endpoint and safety exclusion read in section 2, PDF p.3. SHA-256 `3985f4866d96d0ad5d0f0ee82551934080779d815cef5444ebb9c64f1ff8782d`.

## Scope and preservation

The input current manuscript, first manuscript, prior author checks, upstream originals and calculation artifacts were not edited. No research/model experiment, model API call, calculation rerun, managed-state update or review import was performed. The diff below is the complete textual change. Author completion does not claim independent reviewer acceptance.

## Complete diff

````diff
--- reports/current.md (read-only input)
+++ draft-revision-full-01.md
@@ -102,7 +102,7 @@
 
 This remains one of the clearest descriptions of how computational and experimental work actually interacted. Exscientia generated structures and predicted activity, toxicity-related properties and pharmacokinetics. Sumitomo synthesized the proposed compounds and measured their properties; these observations were fed back into the predictive model. The team ran approximately two-week cycles. Medicinal chemists also made analogues using available synthetic intermediates, producing additional structure–activity information. When stronger binding failed to deliver the desired functional agonism after roughly three months, the team used matched molecular-pair analysis and complementary design strategies. The operational achievement was the ability to change the search direction when one objective stopped improving. [Scientists' technical account, pp. 3–4](https://www.sumitomo-chem.co.jp/english/rd/report/2021E_3.pdf).
 
-DSP-1181 was the 350th compound synthesized in the project. The reported period of less than twelve months ended when a compound with the target profile was identified and **excluded safety evaluation**. The same account describes an already established collaboration spanning several projects. Comparing that clock directly with the entire conventional discovery and development process would attribute earlier platform-building, assay development and later safety work to different sides of the comparison. The useful claim is narrower and substantial: an integrated team carried out hundreds of design–make–test iterations quickly enough to nominate a candidate within the stated exploratory interval.
+DSP-1181 was the 350th compound synthesized in the project. The reported period of less than twelve months ended when a compound with the target profile was identified and **excluded safety evaluation**. The same account describes an already established collaboration spanning several projects. Comparing that clock directly with the entire conventional discovery and development process would attribute earlier platform-building, assay development and later safety work to different sides of the comparison. The useful claim is narrower and substantial: an integrated team synthesized and tested hundreds of compounds through repeated two-week feedback cycles, nominating a candidate within the stated exploratory interval.
 
 The program also used biological and translational techniques outside the design engine, including optogenetic disease-related experiments and biomarker work. These were attempts to connect receptor pharmacology with a clinically meaningful effect. They illustrate why a better predicted molecule is only one component of discovery. Functional agonism, brain exposure, tolerability, target engagement and improvement in the intended disorder must align. The termination preserves a valuable lesson for buyers: process capability can be demonstrated by a program that later fails, but the failure must remain in the platform's development record.
 
````
