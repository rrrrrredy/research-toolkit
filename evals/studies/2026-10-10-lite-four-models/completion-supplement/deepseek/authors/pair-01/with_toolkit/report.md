# Memory Safety Risk in Native Code and Open-Source Dependencies: What to Authorize on June 27, 2024

## Recommendation

Do not authorize an immediate full rewrite of the vendor's native-code components. The available CISA materials justify starting a memory-safety roadmap and investigating first-party code and external dependencies, but they do not establish that a wholesale rewrite is technically necessary, cost-effective, or sufficient to remove the vendor's memory-safety risk. [S1][S2]

Approve a bounded discovery and roadmap-scoping phase. Its immediate purpose is to produce the inventory, risk classification, and options analysis that a rewrite-or-not decision requires. Defer budget, deadlines, and projected vulnerability-reduction targets until the vendor has both internal data and the full linked CISA guidance.

## What the sources establish

CISA's December 2023 resource describes guidance for software manufacturers to transition to memory safe programming languages (MSLs) to eliminate memory safety vulnerabilities. It also says the guidance provides steps for creating and publishing memory safe roadmaps that show customers how manufacturers are owning security outcomes, embracing radical transparency, and taking a top-down approach to secure products. [S1]

On June 26, 2024, CISA and partners released "Exploring Memory Safety in Critical Open Source Projects." CISA says the guidance provides findings on the scale of memory safety risk in selected open source software (OSS), and builds on "The Case for Memory Safe Roadmaps" by giving manufacturers a starting point for memory safe roadmaps, including plans to address memory safety in external dependencies commonly found in OSS. CISA encourages organizations to review the methodology and results to reduce memory safety vulnerabilities, make secure and informed choices, understand OSS memory-unsafety risk, and evaluate approaches to reducing that risk. [S2]

These are real agency announcements. The linked PDFs are not part of the supplied material. Their methods, numerical findings, criteria, and detailed migration steps are therefore unavailable here. That boundary matters: it prevents turning a credible call to action into a precise cost or risk-reduction estimate. [S1][S2]

## First-party code and dependencies are different problems

For first-party native components, language and code ownership are partly within the vendor's control. A roadmap can consider new memory-safe modules, incremental replacement of vulnerable components, interface boundaries, and where native performance is genuinely required. The source rationale is that transitioning to MSLs can help eliminate memory safety vulnerabilities in code written in those languages, not that every existing native component must be rewritten. [S1]

For third-party open-source libraries, direct rewriting is usually not the first lever. The vendor can update, replace, isolate, wrap, monitor, or contribute upstream. CISA explicitly points roadmaps toward external dependencies commonly made of OSS. [S2] But without the linked report's selected projects, methods, and results, the vendor cannot know which dependencies carry material risk, how much of its exposure is dependency-driven, or whether remediation would be faster than a first-party rewrite.

A serious error would be to treat all native code as one bucket. First-party code and dependencies have different control, maintenance, licensing, support, and upgrade paths. The roadmap should separate them before ranking anything.

## What can be authorized now

A useful discovery phase can inventory first-party native components and third-party OSS dependencies, record languages, versions, maintenance status, build and runtime context, and identify where untrusted input, privilege, network exposure, or customer deployment raises consequence. It can map existing memory-safety defects and incidents, if any, and assess options: upgrade, replace, sandbox, refactor, or write new modules in a memory-safe language. It can also draft an internal roadmap and a customer-transparency plan, consistent with the source emphasis on publishing roadmaps and owning security outcomes. [S1][S2]

This is investigation and roadmap work, not a full migration mandate. It gives the director evidence to decide whether to fund incremental hardening, dependency remediation, selective rewrites, or broader MSL adoption.

## Missing information before priorities or deadlines

The vendor still needs the full CISA roadmap steps and the OSS guidance methodology, selected-project scope, findings, and recommended mitigations. Internally it needs an SBOM or dependency graph, reachability and exploitability analysis, criticality and exposure ratings, customer contractual constraints, performance and platform requirements, engineering capacity, and current memory-safety incident data. Without these, any deadline or projected vulnerability reduction would be unsupported.

## Concrete next decision

At the June 27, 2024 engineering leadership review, approve a time-boxed discovery and roadmap-scoping initiative. Require a first-party versus dependency inventory, a risk-ranked dependency list, an options paper comparing incremental remediation with rewrite scenarios, and a proposal for one bounded pilot. Make full rewrite funding contingent on that output and on reviewing the complete CISA PDFs. That is the defensible decision the available sources support. [S1][S2]

## References

- CISA, "The Case for Memory Safe Roadmaps: Why Both C-Suite Executives and Technical Experts Need to Take Memory Safe Coding Seriously," December 6, 2023. [S1]
- CISA, FBI, Australian Signals Directorate's ACSC, and Canadian Cyber Security Center, "CISA and Partners Release Guidance for Exploring Memory Safety in Critical Open Source Projects," June 26, 2024. [S2]
