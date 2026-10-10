**MEMORANDUM**

TO: Director, Customer-Service Products  
FROM: Product Research  
DATE: June 7, 2023  
RE: Chatbot as primary first-contact channel for complaints and transaction disputes — evidence assessment and bounded pilot proposal

*This memo is product research based solely on the CFPB's June 6, 2023 report "Chatbots in consumer finance" [S1]. It is not legal advice and does not describe law or market conditions after June 7, 2023.*

---

**Purpose**

You have asked whether we should deploy a chatbot as the main first-contact channel for consumer complaints and transaction disputes. This memo assesses the evidence in [S1], distinguishes the types of claims it contains, and proposes a bounded pilot.

**What the evidence shows — and what type of evidence it is**

The CFPB report contains three distinct kinds of evidence that should not be conflated:

1. **Cited third-party adoption figures.** The report cites an estimate that over 98 million U.S. users (approximately 37% of the population) engaged with a bank chatbot in 2022, with growth projected; all of the top 10 largest commercial banks have deployed chatbots [S1]. A cited industry estimate claims $8 billion per annum in cost savings, roughly $0.70 per interaction [S1]. These figures describe adoption and projected savings, not outcomes for complaint handling.

2. **Consumer complaint examples.** The CFPB summarizes complaints it received. These include: a customer told a dispute was opened and conditional credit issued, which never appeared, with no case ID provided [S1]; a customer unable to reach a human about a wrongfully frozen credit report [S1]; a customer stuck in chat loops while a payment deadline passed, resulting in a late fee and credit-bureau report [S1]; and customers describing chatbots that parrot FAQ content or fail to recognize disputes [S1]. These are illustrative accounts, not a representative sample, and should not be read as a failure rate.

3. **Agency analysis.** The CFPB's own assessment is that chatbots may be useful for basic inquiries but that effectiveness wanes as problems become more complex; that poorly designed chatbots can hinder access to human support; and that institutions risk violating federal consumer financial laws, eroding trust, and causing consumer harm when deployment fails [S1].

**Suitable uses**

For high-volume, low-complexity tasks — balance inquiries, payment routing, card activation, providing account numbers — chatbots offer 24/7 availability and immediate response, features the report notes as drivers of adoption [S1]. These uses align with the technology's demonstrated strengths.

**Unsuitable uses**

The evidence points to several categories where a chatbot should not be the sole or primary channel:

- **Dispute recognition and resolution.** The CFPB finds that chatbots and scripted systems can introduce inflexibility, where only specific words or syntax trigger dispute handling, and that chatbots limited to regurgitating system information cannot meaningfully resolve disputes [S1]. This is directly relevant to your proposal.
- **Complex or non-standard problems.** The report finds rule-based chatbots function as "one-way streets" and that customers with limited English proficiency face particular difficulty when systems are trained on limited dialects [S1].
- **Customers in distress or facing urgent deadlines.** Complaint examples describe missed payment deadlines and time-sensitive credit-report issues unresolved by chat channels [S1].
- **Situations requiring tailored support or exercise of legal rights.** The agency analysis flags that institutions may fail to recognize when a consumer invokes federal rights [S1].

**Failure mechanisms and incentives**

The report identifies specific failure mechanisms: dispute-recognition failures, "doom loops" of repetitive responses with no offramp, inaccurate or unreliable information from LLM-based systems, system downtime, and security risks including impersonation phishing and exposure of chat logs [S1].

It also describes structural incentives that bear on your decision. Institutions may intentionally substitute chatbots for human agents to grow revenue or minimize write-offs; automated systems may be less likely to waive fees or negotiate [S1]. Investment priorities may favor revenue-generating features over reliability [S1]. In markets with limited consumer choice — such as mortgage servicing — cost savings may not be passed through to customers, and the incentive to reduce service quality increases [S1]. These incentives suggest that cost-driven deployment without safeguards risks the outcomes the report documents.

**Human-handoff requirements**

The evidence supports treating human handoff as a design requirement, not a fallback. Specifically: an offramp that is immediately available, not blocked by unreasonable waits [S1]; guaranteed human access for dispute and complaint matters [S1]; and human support for customers whose issues exceed the chatbot's capability or who cannot use the system effectively [S1].

**Bounded pilot decision**

I recommend a bounded pilot with the following guardrails:

- **Scope.** The chatbot may serve as first contact for identified low-complexity inquiries only. Complaints and transaction disputes are routed to human agents at first contact, or after at most one bot interaction with an explicit, immediate escalation option.
- **Metrics.** Pilot success should be measured by resolution rate, escalation accuracy, dispute-recognition accuracy, and customer-reported resolution — not by per-interaction cost savings, which the report's cited figures do not tie to complaint handling [S1].
- **Sunset.** The pilot should have a predetermined review date with authority to halt expansion if dispute-recognition failures or inadequate escalation rates are observed.

**Counterargument and evidence needed**

A reasonable counterargument is that chatbots can efficiently absorb high volumes of routine inquiries, freeing human agents to handle complex cases better, and that the technology is rapidly improving. This argument has force for simple tasks. However, [S1] does not measure whether chatbot deflection improves or worsens dispute outcomes specifically, nor does it measure whether the cited per-interaction savings survive the cost of mishandled complaints, regulatory exposure, and customer attrition. To resolve this counterargument, we would need pilot data on: (a) dispute-recognition accuracy versus human agents, (b) downstream outcomes for complaints deflected versus handled by humans, and (c) true total cost per resolved complaint, including rework and escalations.

**Bottom line**

The CFPB's June 2023 report supports using chatbots for basic inquiries but provides substantial evidence — through complaint examples and agency analysis — that deploying them as the primary channel for complaints and disputes creates material risks of non-resolution, legal exposure, and customer harm [S1]. A bounded pilot that excludes disputes from the chatbot's primary role, with guaranteed human handoff and outcome-based metrics, is the evidence-consistent path forward.
