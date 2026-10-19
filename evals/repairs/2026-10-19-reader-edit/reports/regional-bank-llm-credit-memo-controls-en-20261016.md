# LLM credit-memo drafting: what Northlake needs before production use

Northlake should keep CreditScribe's factual and risk-bearing narrative out of unrestricted production drafting until the bank can show how unsupported numbers, softened risk language and stale covenants are detected and prevented from reaching approved credit files. A narrower grammar or structure role may be considered earlier if the restrictions are real. The important distinction is what the tool changes in the credit process, not whether the vendor calls it a copilot or requires a human to click Accept.

This memo uses the four synthetic documents supplied with the task. The bank, vendor and observations are fictional evaluation material, not verified banking practice or legal advice. No independent review was performed.

## 1. Treat the vendor pitch as a set of unverified propositions

CreditScribe drafts sections from CRM notes and uploaded PDFs, claims a 45% reduction in memo time and describes retrieval as a hallucination control. Its one-pager does not explain model-risk inventory, challenger review or adverse-action language controls. Data training and retention are described as configurable, without a stated default. An illustrative demo even includes a debt-service coverage ratio absent from the uploaded document. [Vendor one-pager](../../../studies/2026-10-19-external-batches/tasks/regional-bank-llm-credit-memo-controls-en-20261016/sources/S1.md)

These omissions do not establish that every deployment has the same settings or that the vendor can never provide acceptable controls. They do mean the bank cannot infer the necessary operating conditions from the brochure. Retrieval can provide source text while the generated narrative still changes its meaning. A displayed ratio may look plausible even when neither the ratio nor the inputs needed to calculate it are present.

The 45% time claim also needs a defined boundary. Time to produce a draft is different from time to reach a correct, approved memo. The pack supplies no measured allowance for source comparison, corrections, escalation or later rework. Northlake therefore has no basis to describe that percentage as its own productivity gain. It can retain the claim as something to investigate while separately observing the work actually required of relationship managers and reviewers.

## 2. Read the shadow evidence at the unit actually observed

The shadow QA log covers 120 memo sections during weeks one through eight. It records nine numeric facts absent from source PDFs or CRM, fourteen cases of softened risk language, six stale covenants copied from earlier deals, and ninety-one harmless rephrases. Two high-severity items were nearly accepted before a checker caught them. The vendor calls the problems rare; QA considers them material for credit decisions. [Shadow-mode QA log](../../../studies/2026-10-19-external-batches/tasks/regional-bank-llm-credit-memo-controls-en-20261016/sources/S3.md)

Nine out of 120 is 7.5% at the recorded section level, and six out of 120 is 5%. Neither figure is a loan-level loss rate or a production incident rate. The log does not provide the number of distinct borrowers, the exposure attached to each section, or the sampling design. Its row counts sum to 120, but the description is not sufficient to reconstruct overlaps or the relationship between sections and complete memos. Decisions should use the observed defects without claiming a more representative denominator.

The ninety-one harmless rephrases are evidence that the tool can perform useful language work. They do not offset an unsupported number in a different section. A weighted average score would require an agreed way to value these different outcomes, which the pack does not provide. For the bank's immediate decision, the near-acceptance events matter because they show that having a checker does not make the risk disappear before it reaches a human decision point.

## 3. Match each control to the failure it is supposed to prevent

Northlake's draft policy treats generated text as non-authoritative, prohibits automatic acceptance of ratings, covenants and adverse-action language, and requires prompt and response logging with retention aligned to the credit file. It also requires no vendor training on bank data by default. These are the bank's proposed operating requirements, not controls demonstrated by the vendor's one-pager. [Model-risk and credit policy draft](../../../studies/2026-10-19-external-batches/tasks/regional-bank-llm-credit-memo-controls-en-20261016/sources/S2.md)

| Observed failure | Required decision control | Evidence the bank should retain |
| --- | --- | --- |
| An unsupported number enters a draft | Compare the figure with the underlying file; do not accept absent inputs as facts | The relevant source location and the corrected or rejected passage |
| Risk language becomes softer | Compare meaning with the relationship manager's notes, not merely grammar | The original concern, proposed wording and reason for the retained formulation |
| A covenant is copied from an earlier deal | Confirm borrower, deal and document version before use | The current covenant source and removal of the stale text |
| Sensitive data handling is unclear | Establish the actual training and retention configuration before uploading files | The agreed configuration and the bank's data-flow record |

The first three controls are different. Accurate copying of a number does not show that the risk interpretation is appropriate. A polished paragraph does not establish that a covenant belongs to the borrower under consideration. Source links help a reviewer navigate, but a link alone does not prove that the cited passage supports the generated statement.

For a ratio, the manager should identify either the explicitly reported figure or the source inputs and calculation used. If the file lacks those inputs, the draft must leave the ratio unresolved rather than supply a plausible estimate. The synthetic demo is therefore a concrete warning about unsupported factual content, even though the vendor labels it illustrative. That label limits what can be inferred about deployment frequency; it does not make the invented number suitable for a credit memo.

## 4. Make human accountability describe work, not a button press

The policy draft requires the relationship manager to attest that numbers were checked against source documents. An Accept click is weaker evidence: it shows a selection occurred, not what was compared or whether an error was found. The pack also says pilot managers under-report edits. Surveys about perceived speed will therefore miss part of the correction burden.

Northlake should retain the first generated passage and the final text used in the file, together with the source locations consulted for material facts and the reason for material corrections. This is a recommendation for using the existing prompt, response and credit-file records coherently; it does not require treating every stylistic change as a separate approval event. It allows a later reviewer to distinguish an accurate first draft from one made acceptable through substantial human repair.

A practical allocation is for the manager to verify borrower facts, the credit reviewer to assess their risk meaning, and the designated model-risk and compliance owners to examine the tool's permitted uses and control evidence. These are proposed responsibilities for this case, not claims about Northlake's current staffing. Where one person performs more than one role, the record should still explain which judgment was made rather than imply that several independent checks occurred.

## 5. Use the shadow period to decide scope, not to run down a clock

The draft calls for at least sixty days in shadow mode, dual review of sampled memos, and a halt when material factual invention exceeds a predefined threshold. The available record describes weeks one through eight. That description does not document completion of the sixty-day requirement, and elapsed time alone would not resolve the observed defects. The numerical threshold is also absent from the supplied policy excerpt; it should not be invented retrospectively to make the existing result pass.

The same draft identifies any silent insertion of ratios or facts absent from the credit file as a kill condition. Northlake must establish whether the recorded high-severity items meet that condition and how they were handled. It cannot replace that question with the vendor's description of the events as rare. The nearly accepted items make it especially important to distinguish defects caught during shadow review from defects the proposed production process would reliably prevent.

A limited grammar and structure use may be considered before full narrative drafting, consistent with the compliance counterpoint. That permission would need genuine restrictions on changes to numbers, ratings and risk-bearing content. If the configured product cannot enforce or support those limits, labelling the use “grammar assist” does not create a safer operating mode. The bank should retain shadow use or decline that proposed scope until the restriction can be demonstrated.

Broader narrative drafting should depend on evidence that the identified failure modes are controlled within the intended workflow. The bank should agree the unresolved threshold before interpreting subsequent observations and keep the failed outputs visible. It should not obtain a more favorable result by excluding the difficult sections, silently repairing them or counting only drafts that managers chose to accept.

## 6. Keep the declared use consistent with the actual influence on decisions

The compliance briefing distinguishes draft assistance from text that affects adverse action or customer-facing explanations. It recommends inventorying the tool, its data flows, human accountability and sampling results for examiner-facing disclosure. It also warns against calling the process draft-only while allowing practice to drift into decisioning. These are positions in the supplied synthetic briefing, not a comprehensive statement of applicable law. [Compliance briefing](../../../studies/2026-10-19-external-batches/tasks/regional-bank-llm-credit-memo-controls-en-20261016/sources/S4.md)

The distinction should follow the actual workflow. A generated risk-rating narrative can influence approval even if the final rating is selected by a person. Reused language can influence an adverse-action explanation even if the product has no button labelled “decision.” Northlake should therefore describe where generated text enters the file, who changes it, and whether it affects approval or external communications.

The proposed policy's stop on using declined-file adverse-action language without counsel should remain in force for that use. It is not a reason to invent a universal disclosure obligation for every grammar edit. The bank needs advice appropriate to the particular communication, while its internal record should remain truthful about how the text was produced and checked.

## 7. The immediate decision

CreditScribe's unrestricted factual and risk narrative should remain outside production approval files under the present evidence. Northlake can examine a bounded language-assistance use only if the relevant restrictions and data settings are established. The next useful work is to resolve the unsupported-number and stale-covenant cases, inspect how risk meaning changed, and document the human corrections already required. This uses the observed failures rather than generating another favorable headline about speed.

The bank does not yet know its net time saving, a representative production defect rate, or whether the vendor can meet every requested configuration. Those unknowns do not prevent a scoped decision: no unsupported factual insertions, no silent acceptance of credit judgments, and no stronger description of deployment readiness than the actual control evidence warrants. Expansion becomes reasonable when the bank can explain how the intended use handles these concrete failures, not simply when another set of managers clicks Accept.
