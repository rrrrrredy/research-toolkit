# LongCat format follow-up — 12 October 2026

[English](README.md) | [简体中文](README.zh-CN.md)

The explicit JSON protocol is **not yet a stable replacement**: three of four first replies parsed. The Chinese Toolkit reply returned object-valued `notes`, while the parser requires a string. Its full JSON fence was allowed, so the fence did not cause failure. The original prompt asked for “separate working notes” without spelling out the string type; this is a prompt/schema alignment defect to fix prospectively, not permission to coerce the recorded object.

[Plan](plan.json) and [commitment](commitment.json) were frozen before these four requests. Two new implementation-authored fictional format probes (English reading room, Chinese ceramics handover) each received both conditions, with counterbalanced order. Model `LongCat-2.0`, thinking disabled, 4,096 completion / 32,768 total tokens, 180-second timeout, `json_object_v1`, whole-output JSON fence allowed; no provider JSON-mode option. No judges, retries or quality scoring. [Results](results.json) and every raw response/parse failure are retained.

These probes followed the original LongCat development queue; they are a separate diagnostic, not held-out quality tasks. They do not replace any of the [four original missing pairs](../../studies/2026-10-12-lite-four-models/README.md). Any later prompt fix requires its own new freeze; 3/4 is insufficient to recommend this configuration as reliably passing.

[Manifest](manifest.json) preserves original artifact hashes; [public manifest](public-manifest.json) includes publication additions. Harness/driver archives contain exact execution bytes. `python scripts/check_development_evidence.py --self-test` checks this evidence without calls or writes. The check verifies format and correspondence, not research quality.
