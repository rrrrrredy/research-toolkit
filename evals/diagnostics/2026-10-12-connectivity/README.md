# Dated connectivity observations

[English](README.md) · [简体中文](README.zh-CN.md)

These short JSON echo requests test access and request configuration, not report quality. [The inventory](summary.json) links all first failures and the separately frozen diagnostic follow-up. No paid request was automatically retried.

| Requested model | First attempt | Separate diagnosed follow-up |
| --- | --- | --- |
| `deepseek-flash` | Expected JSON; same returned ID | None |
| `kimi-k2.6` | Expected JSON; same returned ID | None |
| `glm-5.3` | HTTP 400: this model does not allow disabled thinking | Enabled thinking with low effort: expected JSON; same returned ID |
| `LongCat-2.0` | Expected JSON; same returned ID | None |
| `gpt-6-astra` via Codex | Local configuration error: reserved `openai` provider cannot be overridden; no model request | Separate provider with zero HTTP/stream retries: expected JSON in a completed CLI turn |

There were **six network requests**, including GLM's rejected request, plus **one local preflight failure**; five generations completed. The four successful API replies report 243 total tokens. The successful Codex turn reports 5,185 input and 13 output tokens; its events do not attest the returned model ID. The original five-generation ceiling was not increased; diagnosed failures were retained and a separate two-generation follow-up plan was frozen. None of these calls enters quality scores or calibration counts.

Public copies remove local executable/workdir/instruction paths and home-directory references. `summary.json` gives original and public hashes and the transformation scope. API headers and keys were never stored. Original local evidence remains unchanged. The source materials are original synthetic connectivity prompts; they convey no factual claim about an organization. This evidence is dated 2026-10-12 and does not guarantee future provider availability or model alias stability.

The failures motivated the optional explicit provider thinking fields and the native judge's separate provider configuration. [Offline controls](../../../scripts/check_live_execution.py) cover request settings, isolation, raw failure retention, no retry and frozen-code refusal. [Native judge limits and reproduction](../../../docs/native-judge.md) distinguish software checks, access checks and separately frozen calibration.
