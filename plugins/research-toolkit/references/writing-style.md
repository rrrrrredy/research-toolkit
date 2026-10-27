# Writing Style

[English](writing-style.md) | [简体中文](writing-style.zh-CN.md)

Use this file before drafting, rewriting, or finalizing.

For concrete choices about developing, cutting or revising an argument, consult the [worked examples](writing-style.md#worked-choices-in-research-prose) as needed.

## Voice

Write as the author of a finished research article, not as an assistant reporting a work process.

Avoid:

- "the user provided"
- "the material shows"
- "this source supplements"
- "based on the collected materials"
- "the evidence registry"
- "this section passed audit"
- "I searched"
- "I processed"

Prefer:

- direct claims
- precise mechanisms
- clear comparisons
- explicit uncertainty where it affects judgment
- concise source attribution when needed
- reader-facing implications

## Structure

For long reports, prefer:

1. conclusion-first key insights
2. scope note
3. sections organized by argument, case, company, period, or mechanism
4. synthesis section that does more than summarize
5. counter-evidence or boundary section
6. reader-facing reference appendix

Do not make the article follow the order in which sources were collected.

## Length And Decision Usefulness

Allocate space to the required questions before drafting. When the task has a length constraint or delivery requires a length count, count the actual report before delivery using the requested convention (English words or Chinese characters, with headings and references handled as agreed), and record the count and convention in the existing checklist or delivery notes. If a count is needed but no convention is given, state a reasonable one. Cut repeated background and caveats before cutting required analysis; a short-report limit still applies when the analysis is good.

For a decision memo, state the recommendation, rationale, next action and conditions that would change the decision. Distinguish measured results from proposed pilot criteria. Explain any proposed numerical target using the decision's risks, a baseline or an agreed service requirement; without such a basis, describe the trigger and how to calibrate it. Check that a target does not reward hiding failures or blocking necessary escalation. For example, capping human handoffs can conflict with giving customers timely access to a person.

When the brief asks for an executable plan, make its first step usable: identify an initial scope, responsible role, practical time or resource assumptions, and observations that would expand, change or stop the work. Label proposed starting values as proposals. Use the details relevant to this decision; do not turn them into a universal checklist or require new external participants.

For a short brief, combine related answers instead of reproducing a long-report structure. A table, background section, references appendix and repeated summary are not mandatory. Check the recommendation against every current hard constraint; do not silently trade a budget limit for performance or turn a growth forecast into an existing requirement. Preserve a source's time, sample and measurement conditions through the conclusion. A missing measurement means unknown, not a measured difference or a proven absence. Keep production disclosures in the separate delivery note when the agreed format provides one; retain substantive evidence limits in the report.

## Cut Redundancy, Preserve Relationships

Cut repeated background, filler and qualifications that do not affect the judgment. Preserve the relationships readers need to follow the argument: who acts, what changes, why it matters, and which conditions or contrasts connect the evidence to the conclusion. Use concrete subjects and verbs; explain the role of necessary technical terms instead of compressing actions and reasoning into abstract noun stacks. Keep connective words and explanations where they aid understanding; shorter wording is not always clearer.

Before:

> Source changes do not directly invalidate conclusions; perform impact scoping and evidence-sufficiency reassessment.

After:

> First identify which facts changed, then ask whether those facts affect the original conclusion. A page update alone does not overturn it; if the change concerns a fact the conclusion depends on, reassess the reasoning.

The rewrite makes the order of actions and the judgment conditions explicit while preserving the original evidence boundary.

When condensing body text into a summary, table or conclusion, preserve the meaning of key facts. Keep a number connected to its population, metric definition and scope where they affect the judgment. Shortening must not turn a missing-record rate into a completeness rate, or a proportion within a sample into a proportion of all tasks. When a source's label and detailed description can be confused, paraphrase the full description rather than carrying over the label alone.

Example ([archived synthetic pilot material](https://github.com/rrrrrredy/research-toolkit/blob/main/evals/studies/2026-10-21-external-batches/tasks/ai-agent-workforce-fte-roi-bar-en-20261018/sources/S4.md#L7), not a real-company statistic): the label says "completeness," but the description states that 62% of human edits lacked reason codes. The [original report and correction record](https://github.com/rrrrrredy/research-toolkit/blob/main/evals/repairs/2026-10-21-source-polarity/README.md) retain both accurate paraphrases and incorrect shortened versions within the same draft.

Incorrect shortening:

> Reason-code completeness was 62%.

Meaning-preserving alternatives, depending on where the fact appears:

| Location | Example wording |
| --- | --- |
| Body text | In this pilot, 62% of human edits lacked reason codes. |
| Table | Human edits missing reason codes: 62% (this pilot). |
| Conclusion | This pilot has gaps in its records of why humans made edits. This proportion alone does not establish the share of all tasks requiring human edits or a rate of workforce replacement. |

## Worked Choices in Research Prose

Read the relevant example when deciding what to develop, remove or revise. These use synthetic material in public archives, not real-company investigations; original reports and historical records remain unchanged. The first two are teaching adaptations of original and separately revised reports; the third adds a constructed follow-up requirement. They are not unique answers. Different wording and structures can work if they answer the current question and explain the evidence-to-judgment connection. The author's intended conclusion remains subject to the evidence.

### Develop the Analysis: Does Less Downtime Justify Multiyear Prepayment?

**Question and material.** A manufacturer must decide whether predictive maintenance justifies multiyear prepayment. The [90-day review](https://github.com/rrrrrredy/research-toolkit/blob/main/evals/studies/2026-10-19-external-batches/tasks/iIoT-predictive-maintenance-arr-zh-20261016/sources/S3.md) records downtime falling from 1,840 to 1,510 minutes, alongside a 6% reduction in production load and a changed spare-parts strategy. The [procurement minutes](https://github.com/rrrrrredy/research-toolkit/blob/main/evals/studies/2026-10-19-external-batches/tasks/iIoT-predictive-maintenance-arr-zh-20261016/sources/S2.md) also record a non-bottleneck workshop accepting weaker terms.

**The original gap.** [Section 3 of the original](https://github.com/rrrrrredy/research-toolkit/blob/main/evals/studies/2026-10-19-external-batches/tasks/iIoT-predictive-maintenance-arr-zh-20261016/final.md) already warns against attributing all improvement to the model, but quickly concludes that downtime ROI is only marketing, not a basis for contractual consideration. It does not explain how the observed improvement connects to procurement value, and risks dismissing useful observations. [Sections 4–6 of the separate revision](https://github.com/rrrrrredy/research-toolkit/blob/main/evals/repairs/2026-10-19-reader-edit/reports/iIoT-predictive-maintenance-arr-zh-20261016.md) develop that connection.

**Rewritten passage:**

> Downtime fell by 330 minutes, about 17.9% of the comparison-period total, which warrants investigating the product's contribution. But production load and spare-parts policy changed too. Neither assigning all 330 minutes to the model nor subtracting 6% from 17.9% establishes net benefit: load and downtime are different measures. Deciding whether benefits cover the subscription requires linking particular faults, loss per minute and human handling costs. A non-bottleneck workshop's acceptance of weaker terms suggests that a limited trial may still make sense; it does not replace loss estimates, missed-alert liability or prepaid-fee refund terms for a bottleneck line. The evidence supports further assessment of specific uses, but not approval of multiyear prepayment for the critical line.

**Why this choice helps.** Keep the observed improvement and counterexample, then supply the missing connections among observed change, attribution, economic value and contract choice. This needs more explanation. Adding only “limited sample” or making the conclusion more cautious would still leave the procurement question unanswered.

### Remove Distractions: What Determines an RFQ Answer?

**Question and material.** A manufacturer wants to answer a customer RFQ using an emissions-factor library. The [synthetic brochure](https://github.com/rrrrrredy/research-toolkit/blob/main/evals/studies/2026-10-19-external-batches/tasks/scope3-factor-rfq-evidence-en-20261016/sources/S1.md) advertises over 12,000 factors and use in 40 RFQs without buyer challenges. The factors are industry-average or spend-based estimates; premium ranges cover only 30% of SKUs, and the library provides no third-party assurance. The [advisor extract](https://github.com/rrrrrredy/research-toolkit/blob/main/evals/studies/2026-10-19-external-batches/tasks/scope3-factor-rfq-evidence-en-20261016/sources/S4.md) says some buyers accept labelled screening estimates.

**The original gap.** The [original](https://github.com/rrrrrredy/research-toolkit/blob/main/evals/studies/2026-10-19-external-batches/tasks/scope3-factor-rfq-evidence-en-20261016/final.md) has useful tiered advice, but its ending repeatedly explains what makes a qualified long-form report and restates evidence discipline. These reminders do not help determine whether the current factor is suitable. [Sections 1, 3 and 6 of the revision](https://github.com/rrrrrredy/research-toolkit/blob/main/evals/repairs/2026-10-19-reader-edit/reports/scope3-factor-rfq-evidence-en-20261016.md) use the space to match the buyer's question to the evidence.

**Rewritten passage:**

> Whether this answer can be submitted depends on what the buyer asks. Preliminary screening may use an average estimate whose purpose is clear and accepted by the buyer; comparison of a particular supplier's product requires explaining why that average fits the product. Premium ranges for 30% of SKUs do not establish coverage of this product, nor turn an average into a measurement or an assured conclusion. If the customer requires independent assurance, the current material is insufficient. If the purpose is only screening, that limit need not prohibit every use of the library.

**Why this choice helps.** Catalogue size and “no challenges” can describe the product, but do not establish this answer's suitability, so they are not piled into the decision paragraph. Repeated writing advice is removed. Keep the premium coverage limit and the screening counterexample because they change the recommendation. Cutting makes space for necessary analysis; minimum length is not the goal.

### Revise Locally: Which Judgments Change with the Requirements?

**Original question and material.** The [archived Maple task](https://github.com/rrrrrredy/research-toolkit/blob/main/evals/diagnostics/2026-10-13-targeted-recheck/judges/maple-storage-en/packet.json) concerns fictional storage procurement: first-year total cost at most 10 units, recovery within 4 hours, data on premises and current demand of 12 TB. A costs 11 units, recovers in 2 hours and holds 24 TB; B is 8/5/24 and C is 8/3/14. All are on premises. Another 4 TB next year is only a forecast; C's expansion price and recovery time are unknown.

**Original passage and change.** The [archived report](https://github.com/rrrrrredy/research-toolkit/blob/main/evals/repairs/2026-10-13-astra/maple-storage-en.md) recommends C, correctly under those requirements. This example adds a **constructed follow-up**: an approved budget increase to 11, with 16 TB now mandatory; other conditions stay unchanged. Continuing to recommend C retains an obsolete premise. Replacing all analysis with “insufficient information; research again” discards comparisons that still hold.

**Rewritten passage:**

> Under the revised 11-unit budget and current 16 TB capacity requirement, A qualifies with 11 units in total cost, 2-hour recovery and 24 TB capacity. B still exceeds the recovery limit at 5 hours. C's 14 TB is now insufficient; an expansion with unknown price and performance cannot count as meeting the requirement. All three remain on premises, and the evidence still cannot compare reliability or operating labor. The switch to A follows from changed budget and capacity requirements, not new measurements of prices or reliability.

**Why this choice helps.** Change the recommendation and its budget/capacity reasoning while retaining B's recovery limit, the location finding and the unknowns. Revise a judgment when new input changes its premises, not merely because a new file or a large update exists. Follow-up requirements and evidence in an actual task must come from its actual inputs, not be invented to imitate this example.

## Chinese Longform Preferences

For Chinese final articles:

- Use clean section titles.
- Put the strongest insights near the beginning.
- Use numbered insights when the opening is dense.
- Keep English technical terms only when they are real industry terms.
- Replace translationese with natural Chinese.
- Avoid overexplaining the research process.
- Do not show internal source IDs in the body.
- Follow the brief's citation form. Use a reference list only when requested or useful within that brief; omit it when the task excludes one. Retain source attribution and locators needed to understand or verify the answer.

## English Longform Preferences

For English final articles:

- Prefer concrete nouns and active verbs.
- Avoid consulting-style filler.
- Explain why a fact changes the argument.
- Use caveats sparingly but clearly.
- Keep paragraphs purposeful; avoid source-by-source narration.

## Process-Language Cleanup

Remove process narration without removing attribution, uncertainty or the scope of the source. These are editing directions, not fixed replacements:

- "the user-provided material says..." -> name the speaker or publisher and the specific claim
- "the source shows..." -> state the supported finding; retain "reports", "estimates" or "expects" when needed
- "this material supplements..." -> explain how the added evidence changes the analysis, with attribution where relevant
- "the evidence gap means..." -> identify the affected conclusion and the evidence needed to resolve it
- "this report will..." -> use a direct section transition or remove it

## References

For public writing, references should be readable:

- category
- organization or source type
- title

Do not include internal source IDs, file paths, access status, or audit grades unless the user asks for an audit appendix.

Check citations in the destination format. In exported Markdown or documents, replace chat/tool citation tokens with the corresponding source title, URL and useful locator from the source record. A token that worked in the originating chat is not a portable reference. Verify its target rather than guessing a URL; retain literal tokens when the task is explaining the syntax itself.

Example categories:

- official websites, filings, blogs, docs, and reports
- papers, technical reports, datasets, repositories
- interviews, talks, podcasts, and public speeches
- industry reports, market data, pricing, and financial materials
- media coverage and longform commentary
- user, developer, and community discussions
- criticism, failures, disputes, and counter-evidence
