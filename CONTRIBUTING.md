# Contributing

[English](CONTRIBUTING.md) | [简体中文](CONTRIBUTING.zh-CN.md)

Contribute changes that improve research methods, make the workflow easier to follow, catch demonstrated failures, or strengthen the evidence behind the project's claims. Explain the problem and show how the change addresses it. Keep standalone orchestration products outside this repository.

## Authority And Scope

- `SKILL.md` is the sole normative protocol source.
- The public page may embed `SKILL.md`, but `python scripts/check_docs_sync.py` must prove exact synchronization.
- README files, agent adapters, plugins, and examples are distribution or explanation layers. They must not introduce competing protocol rules.
- Mechanical conformance, semantic research quality, loading checks, and general framework efficacy are separate claims and must be reported separately.

## Before Opening A Change

1. State the concrete failure, adoption problem, or evidence gap.
2. Prefer the smallest change that affects an observable result.
3. For changes to deterministic behavior, add a regression for the demonstrated failure when existing fixtures do not cover it.
4. Preserve a valid control so the checker cannot improve by rejecting everything. Documentation-only changes need checks of their claims, examples and links, without new test cases.
5. Use synthetic or rights-cleared data. Sanitized internal summaries are workflow seeds, not public factual authority.
6. Preserve frozen study inputs after runs begin; identify later changes as a separate version.

## Verification

Run the checks relevant to the changed behavior. CI runs the full offline suite below. The DSH validation command checks an optional adapter configuration; it does not install or start that runtime. Repeat or broaden checks only when a change, failure or unresolved concern requires it.

```bash
python scripts/check_docs_sync.py
python scripts/run_dsh_evals.py validate
python scripts/check_eval_source_integrity.py
python scripts/check_source_policy_contract.py
python scripts/check_source_extraction.py
python scripts/check_regression_fixtures.py
python scripts/check_conformance_fixtures.py
python scripts/check_delivery_contract.py
python scripts/check_review_completion_contract.py
python scripts/check_evaluator_contract.py
python scripts/check_semantic_diagnostics.py
python scripts/check_installation_contract.py
python scripts/check_diagnostic_bundle.py --self-test
python scripts/check_semantic_review_bundle.py --self-test
```

If `SKILL.md` changed, refresh the public copy first:

```bash
python scripts/check_docs_sync.py --write
```

Changes to `scripts/run_evals.py` must preserve result schema semantics: `conformance_status`, `conformance_score`, and `conformance_flags` are mechanical; `research_quality_status` cannot become a quality verdict without a separately designed and calibrated evaluation.

## Pull Request Evidence

Include:

- the failure or use case addressed;
- files and contract fields changed;
- exact checks run and their outcomes;
- for changed checker behavior, the relevant failing example and valid control;
- limitations and any intentionally deferred work.

Do not claim improved report quality from a green deterministic test alone. Real efficacy claims require held-out tasks, matched baseline/framework runs, independent LLM review checked against known-error and valid controls, and disclosure of failures, retries, cost, and latency.

## Source Preparation Helper

[Stored HTML extraction](docs/source-extraction.md) documents an optional, offline source-preparation tool. It preserves raw publication/version metadata beside extracted text without adding review requirements or changing frozen inputs.

## Reader Entry Points And Distribution

The English and Chinese READMEs introduce the same framework and link to the web guide near the beginning. Keep these entry points focused on what readers can do and where to start. Copy synchronization and packaging decisions belong in maintenance documentation, not a separate introductory chapter.

This repository supplies the reusable Skill. If a particular environment needs a plugin or another installation package, package the same Skill and link back here instead of maintaining a second protocol. Environment-specific setup belongs in `agents/`; it must not imply that the framework is tailored to one vendor or that setup instructions establish research quality.
