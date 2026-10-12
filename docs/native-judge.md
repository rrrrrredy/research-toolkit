# Codex judge execution

[English](native-judge.md) · [简体中文](native-judge.zh-CN.md)

Schema 2 can use `transport: codex_exec` for its judge. Authors still use the compatible HTTP transport. [The dated Astra settings](../evals/configs/development-20261012/astra-judge.json) request `gpt-6-astra`; the local Codex CLI must already be signed in. Set `RESEARCH_CODEX_EXECUTABLE` to its absolute executable path. This is a local process setting, not an API credential or a repository configuration change.

The adapter starts one fresh ephemeral CLI process per packet in a neutral temporary directory. It supplies the frozen judge instruction and the packet, ignores user configuration, disables project instructions, memories, host skill discovery, plugins, apps, shell/browser/computer/image tools and delegation, and passes only a system-environment allowlist. Author API keys and parent conversation identifiers do not enter that environment. No resume/fork operation is used. The process retains the read-only sandbox. A separate provider configuration uses Codex's normal authentication with HTTP and stream retries both set to zero; current CLI versions reject attempts to override the reserved `openai` provider.

Raw `events.jsonl`, `stderr.txt`, sanitized command arguments, request messages and execution metadata are retained. A failed exit, failed turn, observed tool activity, missing usage, ambiguous multiple final messages or excessive post-return usage makes the attempt unresolved. Timeout retains partial output. Strict JSON parsing is applied afterward; a complete CLI turn alone does not establish a valid judgment. The CLI's `skip_host_skill_discovery` option is under development; its warning is recorded. Test the installed CLI before a new freeze, and retain failures after a version change.

Isolation is a controlled execution configuration, not proof about unknown model training exposure or hidden service behavior. The CLI events do **not** attest the returned model ID: metadata says `model_requested` and `model_returned: null`. CLI output-token settings are **post-return checks**, not hard generation or billing caps. A local deadline does not prove remote cancellation. This adapter is for explicitly limited development diagnostics; these limits must accompany any results.

## Calibration

```powershell
$env:RESEARCH_CODEX_EXECUTABLE = 'C:\path\to\codex.exe'
python scripts/run_judge_calibration.py prepare --settings evals/configs/development-20261012/astra-judge.json --seed 2026101201 --output evals/runs/new-calibration
python scripts/run_judge_calibration.py execute --output evals/runs/new-calibration
```

`prepare` makes no model calls. It verifies the four-family controls, freezes the 12 packets, instruction, settings, random order and execution-code hashes. `execute` admits only a new, unchanged run and makes at most 12 first attempts with no retries. The coordinator manifest and expected labels never enter a judge request. Every orientation gets a separate context. All first outputs and failures lock before preference matches are decoded. The result starts with `source_adjudication: pending`: matching labels is not enough; separately inspect quoted evidence, explanations, swaps and valid ties against the original sources.

## Provider reasoning modes

HTTP schema-2 settings optionally accept `thinking: enabled|disabled` and, with enabled thinking, `reasoning_effort: low|high|max`. These become explicit API fields and are identical in both author conditions. Omitting them retains provider defaults. Verify model-specific support before freezing; a generic API parameter description does not guarantee every model accepts disabling thought. The October 12 GLM-5.3 connectivity attempt rejected disabled thinking, and a separately recorded low-effort enabled attempt connected. Never hide such failures with automatic fallback.

Sources checked on 2026-10-12: [Codex non-interactive execution](https://learn.chatgpt.com/docs/non-interactive-mode), [Codex configuration](https://learn.chatgpt.com/docs/config-file/config-reference), [official provider implementation](https://github.com/openai/codex/blob/main/codex-rs/model-provider-info/src/lib.rs), [DeepSeek API](https://api-docs.deepseek.com/api/create-chat-completion/), [Kimi K2.6](https://platform.kimi.com/docs/guide/kimi-k2-6-quickstart), [GLM completion API](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E5%AF%B9%E8%AF%9D%E8%A1%A5%E5%85%A8), [LongCat API](https://longcat.chat/platform/docs/api/chat.html). Live behavior remains dated evidence, not a permanent model guarantee.
