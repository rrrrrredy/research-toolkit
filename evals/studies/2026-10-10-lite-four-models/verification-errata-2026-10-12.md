# Verification correction — October 12, 2026

[English](verification-errata-2026-10-12.md) | [简体中文](verification-errata-2026-10-12.zh-CN.md)

The original offline verifier and completion audit used Python `assert` checks. Under `python -O`, those checks disappeared and changed study metadata could still be reported as verified. The original `verify_bundle.py` also omitted the completion supplement, so the README's description of that command as checking all retained materials was too broad. Neither issue is evidence of changed original results; both limit what the earlier verification command established.

The maintained verification scripts now use explicit checks under normal and optimized Python, include completion provenance, and bind primary and fence-only outcomes to the frozen labels and retained judge preferences. Completion outcomes already had that binding and retain it. The summary commands compare retained outputs by default and fail without overwriting differences; explicit `--write` is reserved for regenerating derived outputs after inspection. They preserve existing newline style. Regression tests exercise valid evidence, temporary corruptions, outcome mismatches, read-only behavior and explicit regeneration.

Frozen inputs, generation adapters, harness snapshot, raw responses, assignments, labels, results and derived tables have not been rewritten. The changed verification/summary code is maintenance code outside the committed generation hashes. No additional model calls or new quality results are represented by this correction.

The retained `summary.json` keeps its historical field names and values. Its `unresolved` field counts unresolved outcomes only among judged rows, so zero does **not** establish complete coverage. Its `unresolved_attempts` field counts unresolved **pairs**, not failed calls. For original primary coverage use `judged` plus `unresolved_attempts`; for call failures inspect execution records and the separate `authors`/`judges` counts. This verification change preserves that historical schema instead of relabeling the archived table.
