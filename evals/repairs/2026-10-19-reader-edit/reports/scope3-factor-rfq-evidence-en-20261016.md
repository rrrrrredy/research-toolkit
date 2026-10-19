# Scope-3 factors in customer RFQs: match the evidence to the answer

MidForge should permit third-party emissions factors for appropriately labelled estimates, while withholding answers that imply supplier-specific measurement or assurance the available evidence does not support. The immediate decision is not whether GreenFactor Pro is a useful library. It is whether a particular factor, calculation and accompanying statement meet the requirements of a particular buyer question. A broad catalogue and an “RFQ-ready” badge do not settle that question.

This memo uses only the four fictional sources supplied with the task. Products, firms, numbers and incidents are synthetic. The recommendations concern that constructed case, not current regulatory requirements or verified market conditions. No independent review was performed.

## 1. Separate the library's coverage from the buyer's requested claim

GreenFactor Pro advertises more than 12,000 commodity factors, annual updates and “audit-aligned” slides. Its fine print says the factors are spend-based or average-process estimates rather than supplier-specific activity data. Default exports omit uncertainty bands; the premium tier provides ranges for 30% of SKUs. The footer expressly says the product does not substitute for an inventory or third-party assurance. These statements describe different attributes: catalogue breadth, update frequency, estimation method and the limits of the resulting claim. None can stand in for all the others. [Vendor brochure](../../../studies/2026-10-19-external-batches/tasks/scope3-factor-rfq-evidence-en-20261016/sources/S1.md)

A buyer asking for a screening estimate may accept an average factor with a clear description of its basis. A buyer asking for the emissions associated with a particular supplier's product requires an explanation of why an industry average is an acceptable substitute, if it is acceptable at all. A request for verified figures creates a further evidential question: what work was verified, by whom and for which scope? Buying a factor library answers none of those questions automatically.

The commercial owner should therefore retain the actual RFQ wording alongside the proposed answer. The sustainability lead can then identify whether the figure is being used for preliminary comparison, a more specific estimate, or a claim of assurance. This is a proposed decision structure for MidForge, not a universal classification imposed by the source pack. Its purpose is to prevent the same exported number from acquiring stronger meaning as it moves from a calculation sheet into a sales response.

## 2. Use the internal failure record to identify different remedies

MidForge's QA extract covers 22 internally reviewed questionnaires. It lists seven instances of implied assurance language, five involving factors older than three years, six with no uncertainty or only a single point, and four category mismatches. These are four distinct failure modes, not four reasons to ban all external factors. The extract does not explain how cases were selected or establish that the categories are mutually exclusive, even though the counts sum to 22. It should not be presented as a market-wide failure rate. [QA extract](../../../studies/2026-10-19-external-batches/tasks/scope3-factor-rfq-evidence-en-20261016/sources/S3.md)

| Failure in the record | What the error changes | Relevant response |
| --- | --- | --- |
| Assurance implied without a verifier | The buyer may understand an estimate as independently established | Remove unsupported assurance wording and identify the actual basis of the answer |
| An old factor copied forward | The calculation may describe a different period | Identify the factor vintage and decide whether it fits the requested reporting period |
| A single figure without uncertainty | Apparent precision may exceed what the estimate can support | Explain uncertainty and avoid inventing a numerical range |
| A factor from the wrong process family | The calculation may represent a different production activity | Correct the mapping before interpreting the result |

A fresh factor can still be the wrong category. A correctly mapped factor can still be used in an unsupported assurance statement. A disclaimer cannot repair either a wrong input or a miscalculation. Remediation should address the specific defect, rather than attaching a general caveat to every answer and treating the underlying work as complete.

## 3. Apply an evidence bar that follows the intended use

MidForge's internal draft proposes documented methodology, a factor vintage no more than three years old, uncertainty disclosure and a written statement that the figures are estimates rather than an assured inventory. It also proposes preferring supplier-specific activity data for a priority subset of spend categories identified using emissions estimates. These are proposed internal requirements. The pack does not establish them as binding external standards. [Internal sustainability and commercial memo](../../../studies/2026-10-19-external-batches/tasks/scope3-factor-rfq-evidence-en-20261016/sources/S2.md)

For a preliminary screening response, an average or spend-based factor may be usable if the buyer accepts that purpose and the calculation discloses its limitations. The submission should identify the process or spending category, the factor version, its unit and the calculation basis. If those elements cannot be matched to the requested activity, “screening” is not a reason to send an irrelevant number.

For an answer that will influence a product comparison or a consequential procurement representation, MidForge should establish a closer match between the requested object and its inputs. Supplier-specific activity data may improve that match, but their availability is not demonstrated by the pack. Where only an average is available, the team should explain the substitution and ask whether it satisfies the buyer's question. It should not silently rename the average as a measured supplier footprint.

For an answer claiming verification or assurance, the available library documentation is insufficient. MidForge's draft explicitly stops answers implying ISO or assurance without an engagement letter. Even if a letter later becomes available, the team would still need to check that its scope covers the figure, period and statement at issue. A general relationship with an assurance provider cannot be assumed to cover every RFQ calculation.

The premium tier does not remove these distinctions. Ranges for 30% of SKUs leave the coverage of a particular RFQ unknown. A range for the wrong process remains unsuitable, while the absence of a range does not authorize MidForge to manufacture one. Where the method supports only a qualitative uncertainty statement, it should say so and determine whether the buyer accepts that limitation.

## 4. Make the submitted calculation reproducible

The internal memo describes one allegedly lost bid in which a buyer asked for a calculation pack and MidForge could not reproduce its overly precise figures. This is a single, incompletely established incident; it cannot quantify how often poor documentation loses bids. It does identify a practical requirement that a headline number alone does not meet: someone other than its author should be able to reconstruct what was sent.

A useful calculation record would retain the requested activity, the selected factor and version, the input quantity or spending basis, the unit conversion, the resulting figure and the exact wording submitted. These are recommended components derived from the documented failure modes, not a claim that MidForge already retains them. They also explain why preserving an export matters. If a library changes after an RFQ is answered, the current export may no longer reproduce the earlier answer.

The record should distinguish correcting an arithmetic mistake from changing a method or category. A new factor may alter a result because its vintage or underlying activity differs; that does not by itself mean the previous calculation was dishonest or that physical emissions changed. The team must explain what changed before using a revised number to tell a performance story.

This approach can reuse a well-documented calculation for similar RFQs, provided the buyer question, period and activity remain compatible. It should not require a fresh inventory project for every preliminary question. Reuse saves work only if the previous record is still applicable; copying a familiar number into a different process category recreates one of the failures already observed.

## 5. Divide responsibility without separating the answer from its evidence

The commercial owner understands the buyer's question and the consequences of a qualification. The sustainability lead is positioned to judge methodological fit. Neither role should independently strengthen the other's statement: sales should not remove an estimate label to simplify a portal answer, while the technical owner should not assume the buyer accepts a limitation that changes the commercial representation.

For the next relevant RFQ, the proposed first step is to select the intended use and identify the calculations that actually matter to that response. The team can then resolve category, vintage and uncertainty questions for those figures. The pack's “top 20%” prioritization proposal needs an operational definition before it can allocate effort: it is unclear whether it means a fifth of categories, a spend-based cutoff or a ranking driven by estimated emissions. Choosing one without explanation would turn an ambiguous draft into an apparently precise policy.

A useful qualification might state that a figure is a screening estimate based on a named factor version and that supplier-specific measurements were unavailable. That is an illustrative wording pattern, not a statement about an actual MidForge submission. The exact answer must reflect the calculation performed. If a portal permits only an unqualified assurance claim, the team should seek clarification or withhold that answer, rather than convert a qualified estimate into a false assertion to complete the form.

## 6. Keep the counter-evidence and the stopping conditions visible

The vendor quotes a customer using its factors in 40 RFQs with “zero challenge from buyers,” without enough information about the buyers or how challenges were counted. Silence does not establish verification. It may reflect screening use, limited buyer scrutiny or other circumstances the pack does not identify. The quotation is not evidence that a stronger assurance statement would be acceptable.

The advisor note provides a more relevant counterpoint: some buyers accept screening factors with explicit labels. That supports a graduated response rather than an automatic ban. The same note expects more buyers to request calculation packs through 2027. This is an outlook in a synthetic advisory document, not an observed universal change or a regulatory deadline. [Advisor note](../../../studies/2026-10-19-external-batches/tasks/scope3-factor-rfq-evidence-en-20261016/sources/S4.md)

MidForge should stop a particular submission when it cannot identify the factor's category or vintage, reproduce the calculation, or support the meaning of the proposed claim. It should also stop unsupported assurance language even if the arithmetic is correct. A missing quantitative uncertainty range requires a decision about whether a clearly labelled estimate remains suitable; it need not prohibit every screening response. The stopping decision belongs to the affected answer, not automatically to every use of the library.

Through 2027, the most useful preparation is a reusable, versioned calculation basis that can answer more detailed buyer questions without upgrading the claim beyond its evidence. The remaining unknowns are concrete: which buyer accepts which estimate, whether the required supplier data can be obtained, what the vendor's methodology actually contains, and whether any assurance engagement covers the requested result. Resolving those questions can justify a stronger answer. Repeating the library's badges cannot.
