**Memorandum**

**To:** Engineering Director  
**From:** Security and Architecture Research  
**Date:** June 27, 2024  
**Subject:** Memory-safety investigation and roadmap options after CISA’s June 26, 2024 guidance

**Recommendation:** Do not authorize an immediate full rewrite. Authorize a bounded discovery and roadmap-scoping effort covering both first-party native code and third-party open-source dependencies. The supplied CISA sources support structured transition planning and dependency-risk review; they do not establish that a wholesale rewrite is required now.

**What the sources support**

Source S1 describes CISA guidance on how software manufacturers can transition to memory safe programming languages (MSLs) to eliminate memory safety vulnerabilities. It says the guidance provides steps for creating and publishing memory safe roadmaps, so customers can see manufacturers owning security outcomes, embracing radical transparency, and taking a top-down approach to secure products—key Secure by Design tenets. That is a planning and governance mechanism, not an immediate rewrite mandate.

Source S2, released June 26, 2024, is the more operationally relevant announcement. It says CISA, with the FBI, Australian Signals Directorate’s Australian Cyber Security Centre, and Canadian Cyber Security Center, released *Exploring Memory Safety in Critical Open Source Projects*. That guidance provides findings on the scale of memory safety risk in selected open source software (OSS). S2 says it builds on S1 by giving manufacturers a starting point for memory safe roadmaps, including plans to address memory safety in external dependencies, which commonly include OSS. It encourages organizations to review the guidance’s methodology and results to reduce memory safety vulnerabilities, make secure and informed choices, understand OSS memory-unsafety risk, evaluate risk-reduction approaches, and continue risk-reducing action.

**Mechanisms, scope, and first-party versus dependency work**

The mechanism in both sources is memory safety: replacing or reducing reliance on languages that permit memory-safety defects, and managing that risk across the software supply chain. For first-party code, the vendor controls language choice, toolchain, interfaces, training, and migration sequencing. For third-party OSS, the vendor does not control upstream source; it can assess memory-unsafety risk, choose safer components, update dependencies, or isolate/replace risky ones. S2 explicitly directs attention to external dependencies, so a first-party-only rewrite would leave a central risk category untouched.

A sensible scoping therefore separates two tracks:

1. **First-party native components:** inventory languages and boundaries; identify where MSL adoption, new-module standards, or targeted component replacement could reduce memory-safety exposure over time.
2. **Third-party OSS dependencies:** build dependency visibility; assess memory-unsafety risk; evaluate secure and informed choices; and plan how to address external dependencies in the roadmap.

**Tradeoffs and the rewrite question**

A full rewrite of mature B2B software would be a large cost, schedule, regression, compatibility, and customer-continuity decision. It might reduce first-party memory-safety exposure in scope, but it would not automatically fix OSS dependency risk. It could also divert engineering capacity from measured, risk-based improvements. Conversely, a roadmap-only approach is slower and requires sustained governance; a dependency-only approach may miss first-party native code. The sources justify investigation and roadmap creation, not a predetermined full rewrite. Full rewrite may become an option for specific components after risk data and cost analysis, but it is not justified as an immediate default.

**Missing information**

The linked CISA PDFs are not supplied in this source set. I have not reviewed their methods, numerical findings, selected OSS projects, or detailed migration steps. Before setting priorities, deadlines, or projected vulnerability reduction, the director needs:

- The CISA roadmap steps from S1 and the methodology/results from S2.
- An internal inventory of first-party native code: languages, components, interfaces, age, and criticality.
- A dependency inventory or SBOM: OSS libraries, versions, upstream health, criticality, and memory-safety exposure.
- Threat and exploitability context for the vendor’s deployment model.
- Feasibility data on MSL migration, dependency replacement, performance, interop, hiring, and customer commitments.

Without these, numerical vulnerability-reduction projections or fixed remediation deadlines would be speculative.

**Concrete next decision**

Approve a time-boxed discovery and roadmap-scoping phase, not a full rewrite. Deliverables should include: obtaining and reviewing the two linked CISA publications; producing first-party and dependency inventories; classifying memory-safety exposure by product and component; evaluating MSL and dependency options; drafting a memory safe roadmap aligned to S1 and S2; and recommending a pilot or go/no-go decision. This is the most defensible action the director can authorize from these sources on June 27, 2024. It preserves product stability while creating the evidence needed for later prioritization, deadlines, and measurable risk reduction.
