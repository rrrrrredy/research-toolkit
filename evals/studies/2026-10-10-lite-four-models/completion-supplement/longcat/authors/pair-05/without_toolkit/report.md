# Memorandum

**TO:** Engineering Director
**FROM:** Security Engineering Analysis
**DATE:** June 27, 2024
**RE:** Memory safety — authorized next steps based on CISA guidance (S1, S2)

**Bottom line.** Two federal publications — CISA's resource *The Case for Memory Safe Roadmaps* (S1, published December 6, 2023) and the June 26, 2024 joint announcement *CISA and Partners Release Guidance for Exploring Memory Safety in Critical Open Source Projects* (S2, issued with the FBI, the Australian Cyber Security Centre, and the Canadian Cyber Security Center) — support authorizing investigation and roadmap work now, but not an immediate full rewrite of native-code components. The publications linked from both pages were not available for this analysis, so their methodology, findings, and detailed steps cannot yet inform priorities, deadlines, or projected vulnerability reduction.

**What the sources establish.** S1 describes how software manufacturers can transition to memory safe programming languages (MSLs) to eliminate memory safety vulnerabilities, and provides steps for creating and publishing memory safe roadmaps that demonstrate ownership of security outcomes, radical transparency, and a top-down approach to secure products — Secure by Design tenets. The underlying premise is that memory-unsafe code permits a distinct class of defects, which MSLs remove at the language level rather than defect by defect. S2 extends this framing to the supply chain: it offers findings on the scale of memory safety risk in selected open source software (OSS) and is explicitly positioned as a starting point for manufacturer roadmaps, including plans to address memory safety in external dependencies, which commonly include OSS. S2 also aligns with the 2023 National Cybersecurity Strategy and the interagency Open Source Software Security Initiative (OS3I). S2 urges organizations to review its methodology and results to reduce vulnerabilities, make secure and informed choices, understand OSS memory-unsafety risk, and evaluate reduction approaches.

**What the sources do not provide.** Neither page text includes the linked documents. We have not seen S1's specific roadmap steps, S2's methodology, or any numerical OSS findings. Quoting rates, affected projects, or migration sequences would therefore be fabrication, and no defensible vulnerability-reduction projection is possible from these pages alone.

**What you can reasonably authorize.**
1. **Inventory and exposure analysis.** Identify first-party native-code components and build a complete dependency inventory of third-party and OSS libraries; S2's dependency guidance presupposes knowing where OSS sits in your stack.
2. **Roadmap drafting on S1's model.** Obtain and review the publication internally, then map a draft roadmap to its stated steps and to the customer-facing transparency S1 describes.
3. **Structured review of S2.** Task architecture and OSS governance staff with extracting dependency-layer options from the report's methodology and results.

**First-party code versus dependencies.** Your first-party native-code components are directly within your control: S1's transition model applies, and migration is your investment decision. Third-party OSS dependencies are different — you do not own that code, and S2 is the directly relevant starting point because it addresses memory safety in external dependencies. Candidate levers (upstream contributions, library substitution, risk acceptance with compensating controls) should be evaluated against S2's findings once reviewed; the announcement encourages exactly this evaluation without prescribing outcomes.

**Is an immediate full rewrite justified?** No. Both sources frame memory safety as a managed transition and planning discipline — roadmaps, informed choices, evaluated approaches — not a single replacement event. A full rewrite now would commit major spend before the missing inputs below exist and would undercut the staged, transparent posture both sources describe.

**Missing information before priorities, deadlines, or projections.** (1) S1's actual roadmap steps; (2) S2's methodology and numerical OSS risk findings; (3) internal data: complete native-code/OSS inventory, customer and regulated-data exposure, memory-safety defect history, and capacity to build and test components in additional memory-safe languages; (4) customer expectations, since S1 ties roadmaps to public transparency.

**Recommended next decision.** By July 12, 2024, charter a six-week, time-boxed scoping study: complete the inventory, obtain and review both linked publications internally, and return (a) a draft memory safe roadmap skeleton and (b) a shortlist of dependency-layer options — with a gate review before any migration schedule or rewrite budget is approved. This keeps the organization aligned with federal guidance, preserves optionality, and ensures later commitments rest on evidence we do not yet hold.
