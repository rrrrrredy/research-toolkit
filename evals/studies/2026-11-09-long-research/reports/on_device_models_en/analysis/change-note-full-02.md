# Located process-language revision

Based on the independent process_language findings. Preserve source versions, cited locations, assumptions, calculations and substantive evidence limits; keep access/reading operations in the original execution records.

Previous SHA256: 11093fb5d5a0a18708db9a9175d84ed3bbbb7773b51a393f5161db49f9c8be3e

Revised SHA256: 59f8ac88843287debab4c0176d72575b648dbf581eece7888f22e050e69da8dd

```diff
--- current-before.md
+++ draft-revision-full-02.md
@@ -272,20 +272,20 @@
 
 The report uses public material from 2023 through 9 November 2026, including dated historical measurements where they explain the selected hardware. The cited web pages are access-date snapshots unless a release or commit is specified. Numerical scenarios are author calculations, not observed acceptance, price, power or throughput measurements. Decimal MB/GB are used for transfer sizes; MiB/GiB are binary memory units. Device manufacturers' installed-memory labels are retained as published.
 
-| Evidence item | Preserved version and actual reading | Interpretation retained in the report |
+| Evidence item | Source version and cited locations | Interpretation retained in the report |
 |---|---|---|
 | Qwen2.5-3B-Instruct | Official model card and full configuration JSON, acquired at cutoff | Model-specific 32K context, full-attention cache formula; weight and application reservations remain scenarios |
 | S24 phase measurements | LiteRT-LM README commit `eaa380eee74b677f9f305eb2a92ae0fcc14ffc39`, 21 July 2025 | 1,024-token prefill, 256-token decode, four-bit per-channel artifacts and 4K context, with performance lock on Android devices. Derived times retain this condition; default or sustained phone performance is not established. Current Gemma 4/S26 table is a different experiment |
 | M4 Pro comparison | BaseRT arXiv `2607.00501v1`, §§4.1–4.3 and Tables 1–3 | Paper rates and baseline versions; later repository CSV and KV defaults do not retroactively establish the paper's full setup |
-| Quantization quality | Meta official Llama 3.2 card; Apple `2507.13575v1`, Table 3 visually inspected | Task and optimization-method differences; July Apple quality values kept separate from later updates |
+| Quantization quality | Meta official Llama 3.2 card; Apple `2507.13575v1`, Table 3 | Task and optimization-method differences; July Apple quality values kept separate from later updates |
 | Sustained mobile behavior | MELT `2403.12844v4`, §5.2.3 | Historical iPhone 14 Pro/Jetson AGX mechanisms, not an inferred S24 thermal curve |
-| Collaborative documents | Final ICML 2025 Minions paper, 38 pages; Table 1 visually inspected, Table 2 and methods read | Historical cloud prices, local-free accounting, workstation latency; no formal privacy guarantee |
-| Speech optimization | WhisperTRT commit `268eff10a1e38118a2734745b9db14f7419a08a5`, 15 October 2024; README and profiling/live/model code read | Warm single-clip timing, RSS delta, decoder differences and 30-second-window handling |
-| Speech noise and precision | ASR energy paper `2405.01004`, setup pp.4–7 and Table 4 visually inspected on p.10 | Aggregate experiment, incremental CPU/GPU energy, synthetic-noise procedure; repository unavailable at access time |
+| Collaborative documents | Final ICML 2025 Minions paper, 38 pages; Tables 1–2 and methods | Historical cloud prices, local-free accounting, workstation latency; no formal privacy guarantee |
+| Speech optimization | WhisperTRT commit `268eff10a1e38118a2734745b9db14f7419a08a5`, 15 October 2024; README and profiling/live/model code | Warm single-clip timing, RSS delta, decoder differences and 30-second-window handling |
+| Speech noise and precision | ASR energy paper `2405.01004`, setup pp.4–7 and Table 4 on p.10 | Aggregate experiment, incremental CPU/GPU energy, synthetic-noise procedure; repository unavailable at access time |
 | Current APIs | ML Kit page updated 6 November 2026; current Apple developer Markdown; Microsoft Learn page updated 19 October 2026 | Availability, quotas, entitlement, channel and planned transitions; older raw Microsoft repository page preserved separately |
 
 Several source details affect the arithmetic. The WhisperTRT README labels memory as MB, while its profiler computes MiB and samples an RSS difference rather than a peak. Its `base.en` ratio is 439/666 = 65.9% of the original path's reported memory; the report uses the actual values rather than treating the promotional “about 60%” as precise. The independent speech paper's printed WER formula contains an apparent insertion-term typo; the interpretation here uses the conventional `(substitutions + deletions + insertions) / reference words`. Its unavailable code and unspecified exact aggregate audio duration prevent a precise reconstruction of real-time factor or wall energy.
 
-The accompanying `deployment_calculations.py` and `calculation-results.json` contain the executed memory, phase-time, clip-RTF, power-duty, transfer and economic arithmetic. They run no model inference and make no claim to validate a device. `reading-ledger.json` records the original paths and selected locations actually read.
+The accompanying `deployment_calculations.py` and `calculation-results.json` contain the executed memory, phase-time, clip-RTF, power-duty, transfer and economic arithmetic. They run no model inference and make no claim to validate a device.
 
 For a concrete deployment, the remaining measurements are specific: available and peak working memory on the intended device state; first usable and complete-result latency with the real prompt/output distribution; sustained behavior for the actual operating duration and concurrent apps; task quality on representative documents, languages or acoustic conditions; and endpoint-level power if battery or thermal sizing depends on it. Those missing deployment measurements bound the recommendations here. They are not filled by transferring a rate from another device, runtime or task.
```

## Author acceptance and formal save

Accepted by the registered substantive author `/root/ttc_research` after reading the saved process_language finding and comparing the actual current manuscript with this revision. The textual changes match the recorded diff; numerical results, source versions, page/table references, assumptions and material evidence limits remain intact. This is author acceptance, not independent-review approval.

The coordinator-prepared proposal used CRLF line endings. The accepted file uses LF, with identical text, so its on-disk SHA-256 matches the revised hash above. Original proposal byte SHA-256: `a50efefc9ad53c554835984252c45062c27875f4cf42344378897e461dfad19e`.
