**MEMORANDUM**

**To:** Engineering Director
**Date:** June 27, 2024
**Re:** Memory-safety authorization following CISA guidance
**Sources:** S1 (CISA resource page, Dec 6, 2023); S2 (CISA alert, Jun 26, 2024)

## Bottom line

The available sources suggest authorizing a bounded scoping and roadmap-drafting effort now; they do not justify an immediate full rewrite of native-code components. The detailed methodology, numerical findings, and migration steps reside in linked PDFs that were not supplied, and acting on them would require reading them first.

## What the two pages establish

CISA's *The Case for Memory Safe Roadmaps* (published December 6, 2023) urges software manufacturers to transition to memory safe programming languages (MSLs), described as eliminating memory safety vulnerabilities, and to create and publish roadmaps showing they are "owning security outcomes, embracing radical transparency, and taking a top-down approach to developing secure products," framed as Secure by Design tenets (S1). The page is explicitly addressed to both C-suite executives and technical experts.

The day before this memo's decision date, CISA, the FBI, the Australian Cyber Security Centre, and the Canadian Cyber Security Centre released *Exploring Memory Safety in Critical Open Source Projects*, offering "findings on the scale of memory safety risk in selected open source software (OSS)" and building on the roadmaps guide by providing "a starting point for software manufacturers to create memory safe roadmaps, including plans to address memory safety in external dependencies which commonly include OSS" (S2). The joint guidance aligns with the 2023 National Cybersecurity Strategy and the interagency Open Source Software Security Initiative.

## Mechanism and scope

The mechanism these sources advocate is not a rewrite but a published, customer-facing roadmap: a top-down commitment to measured transition. The two pages divide the problem along the first-party/dependency axis, which is the central architectural fact for a vendor built on native-code components and third-party libraries. S1 addresses a manufacturer's own code and its transition path. S2 makes clear that a manufacturer also carries exposure through dependencies it does not control, OSS components it imports. You can, over time, rewrite first-party code; you cannot unilaterally rewrite a dependency. For dependencies you can choose alternatives, isolate usage, contribute fixes upstream, or accept and monitor residual risk.

## Tradeoffs

A full rewrite in an MSL could eliminate a class of bugs but is the most expensive, slowest, and riskiest option, and it would displace feature work. The sources do not quantify the benefit side of that tradeoff. A roadmap approach buys transparency and staged risk reduction at lower delivery risk, but it is also a public commitment: publishing a roadmap signals to customers that you are owning outcomes and invites scrutiny if milestones slip. The dependency half of the problem constrains the rewrite option further, because roadmap progress on third-party code depends on upstream maintainers and community timelines you do not set.

## Why a full rewrite is not justified on this record

The sources recommend roadmaps, informed choices, and risk-reducing action, not immediate rewrites. The PDFs that would quantify the scale of OSS risk, identify which component classes are affected, and lay out migration steps were not supplied. Authorizing a rewrite now would commit the organization to the most expensive path before cheaper scoping options have been exhausted.

## What is missing before priorities, deadlines, or projections

Before defensible priorities, deadlines, or projected vulnerability reduction can be set, you need the PDFs' methodology and numerical findings; a complete inventory of first-party native code versus third-party OSS; the language composition of first-party code; which components parse untrusted input; any history of memory-safety incidents; and available engineering capacity. None of these can be inferred from the two announcement pages.

## Concrete next decision

Authorize a 2–4 week scoping phase with four deliverables: (1) a dependency inventory separating first-party native code from third-party OSS; (2) a language-composition assessment of first-party code; (3) identification of components that handle untrusted input; and (4) a draft memory-safe roadmap skeleton consistent with the Secure by Design tenets in S1. Return that artifact to this office; set priorities, deadlines, and projected vulnerability reduction only on the evidence it produces.
