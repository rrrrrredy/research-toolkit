# Research Memo: Chatbot as Primary First-Contact Channel for Complaints and Disputes

**To:** Product Director, Customer Service (Hypothetical Regional Bank)
**Date:** June 7, 2023
**Basis:** CFPB, *Chatbots in Consumer Finance* (June 6, 2023) [S1]
**Note:** This is product research, not legal advice. It reflects the state of the cited report as of June 2023, not current law or current model capabilities.

## Bottom line

The available evidence argues against making a chatbot the *primary* vehicle for complaints and transaction disputes at launch. A rule-based chatbot is suitable for bounded, high-volume, low-stakes tasks — balance checks, payment scheduling, card activation, FAQs — and as a triage layer that routes dispute-intent customers to humans quickly. The CFPB's analysis is explicit that where a system "fails to understand the person's request or the message from the person contradicts the system's programming, it is not suitable for chatbots to be the primary customer service vehicle" [S1]. A bounded pilot in the low-risk channel is defensible; a chatbot-first dispute channel is not.

## What the source actually establishes

Three evidence classes appear in the report, and they should carry different weight in our decision:

- **Consumer complaint examples** (e.g., a dispute promised conditional credit within 48 hours that was never opened across three chat sessions [S1]; a customer routed into "loop after loop" and facing a late fee [S1]). These illustrate failure *mechanisms*. They are not representative failure rates, and we should not treat them as such.
- **Third-party adoption and survey figures** the CFPB cites: roughly 37% of the U.S. population (over 98 million users) interacted with a bank chatbot in 2022, projected to reach 110.9 million by 2026; all top-10 commercial banks deploy chatbots; a Juniper Research figure of $8 billion annual savings, about $0.70 per interaction; a survey cited in the report that 80% of chatbot users left more frustrated and 78% needed a human afterward [S1]. These come from commercial and media sources; they indicate market direction and incentive structure, not measured outcomes for our bank.
- **Agency analysis**: the CFPB's own assessment of mechanisms and risks — dispute-recognition limits, inaccuracy of LLM outputs, "doom loops," security exposure, and the incentive for institutions to underinvest in resolution features that don't generate revenue [S1].

## Failure mechanisms relevant to our use case

**Dispute recognition is the core gap.** The agency notes that only specific words or syntax may trigger dispute recognition, and that chatbots limited to "parroting" the same system information the customer is disputing back at them do not meaningfully handle disputes [S1]. Since our intended channel is *complaints and disputes specifically*, this is the mechanism most likely to fail.

**Doom loops without an offramp.** When an issue falls outside the bot's capabilities, customers report repetitive loops with no path to a human, sometimes producing direct financial harm (late fees, credit reporting) [S1].

**Inaccuracy risk.** LLM-based systems' statistical methods "are not well-positioned to distinguish between factually correct and incorrect data" [S1]; cited studies found incorrect and fictional outputs from leading models. Legally required disclosures delivered inaccurately create compliance exposure the CFPB warns about [S1].

**Incentive misalignment.** The report's sharptest point for us: resource allocation may favor revenue-generating features (product promotion) over resolution reliability, and automated systems "may be less likely to waive fees, or to be open to negotiation on price" [S1]. We should audit our own roadmap against this bias.

**Security.** Chat logs become sensitive consumer information; the report cites the Ticketmaster/Inbenta breach affecting 9.4 million data subjects and warns there are "too many vulnerabilities for these systems to be entrusted with sensitive customer data without appropriate guardrails" [S1].

## Human handoff requirements

Based on the failure modes described, any pilot must guarantee: (1) an always-visible, one-step escalation to a human, not gated on the bot recognizing the request; (2) human routing triggered by dispute/complaint *intent* detection with human review of unrecognized intents; (3) full conversation-context transfer so customers do not restart; (4) no automated process that concludes a dispute without human confirmation that it was opened, with a case ID issued to the customer — the failure mode in the complaint example [S1]; and (5) language-accessibility testing, since limited-syntax systems burden limited-English-proficiency customers [S1].

## Recommended pilot decision

Launch a bounded pilot: rule-based chatbot for routine servicing (balances, payments, card actions, FAQs) with aggressive human escalation, explicitly *excluding* dispute resolution from bot-handled outcomes; bots may open and acknowledge a dispute, but only a human can investigate and close it. Success metrics: escalation rate, time-to-human, dispute-recognition recall (measured, not assumed), complaint volume, and fee-waiver/late-fee incidence on escalated sessions. Do not commit to cost savings targets in the business case; the $8B/$0.70 figures are third-party projections, not our measurements [S1].

## Counterargument and the evidence needed to resolve it

**Counterargument:** Deficient-chatbot harms are largely artifacts of *poorly designed* bots at large institutions; a well-built, modern system could resolve most disputes without human involvement, capturing the savings.

This is plausible and the report cannot rule it out — it documents failures in deployed systems, not the ceiling of the technology. To resolve it, we would need: (a) dispute-recognition recall/precision measured on our own historical dispute transcripts; (b) resolution accuracy audited against human-gold outcomes; (c) controlled A/B escalation-outcome data (fee incidence, repeat contacts, complaint filings); and (d) security audit of the vendor stack, which the report indicates is essential [S1]. None of that evidence exists today, which is why the pilot is bounded.

## References

- U.S. Consumer Financial Protection Bureau, *Chatbots in Consumer Finance* (June 6, 2023) [S1], and the consumer complaints, Juniper Research, and survey sources it cites.
