# On-Device Models: Hardware Constraints, Task Fit, and Edge–Cloud Design

Author: Codex research producer `/root/ttc_research`. Evidence cutoff: 2026-11-09. Revised author outline for independent requirements and structure review. The original Astra planning output and handoff remain unchanged; the case JSON is authoritative.

## Central argument and selected cases

Local deployment is a task envelope: acceptable quality must fit the usable memory, response deadline, operating duration, power and permitted data boundary of a supported device. A download that fits or a high peak token rate does not close that envelope. The report will recommend local, cloud or hybrid execution for three tasks, while preserving unlike measurement conditions.

The representative hardware cases remain a Galaxy S24 Ultra 12 GB phone, a measured M4 Pro 16-GPU-core/24 GB computer configuration, a Surface Laptop 7 Snapdragon X Elite/32 GB integration case, and an actively cooled Jetson Orin Nano 8 GB endpoint. These are explanatory examples, not a newest-hardware catalogue. Chassis, runtime, precision and model identity must be attached to measurements; undocumented conditions stay missing rather than being silently standardized. Apple's system model and Android AICore will illustrate shipping/API constraints separately from custom open-weight runtimes. The historical MELT devices remain evidence about sustained failure mechanisms, not forecasts for the newer selected phone.

## Report structure

1. **Start with the task and its deployment envelope.** Define quality, offline obligation, data movement, latency and duty cycle. Introduce an evidence legend: documented capability, vendor/author measurement, independent measurement, announcement and calculated scenario. Preview the hardware–model–task fit matrix.
2. **What fits, and what responds.** Complete memory decomposition: resident weights and metadata, working buffers/activations, KV state, retrieval assets, application and OS reserve. Distinguish storage, installed memory, app allowance and accelerator residency. Derive architecture-specific KV examples only from original configurations. Explain bandwidth, operation support, CPU/GPU/NPU partitioning, prefill, decode, cold loading, first output and complete task time. Separate burst speed from steady-state energy/thermal behavior.
3. **Optimizations and their quality price.** Compare small models, distillation, PTQ/QAT, weight versus KV quantization, GQA/windowed/shared KV designs, fused kernels, prefix reuse and context reduction. Explain which resource changes, why speed depends on the actual backend, and what evaluation supports retained quality. Use bounded MoE and speech-model contrasts where they help; avoid a model catalogue.
4. **Private document assistance.** Model parsing/OCR → chunks/embeddings → retrieval/reranking → grounded generation → citation validation. Separate short source-backed extraction from broad synthesis and cross-document reasoning. Build explicit phone and PC memory/context envelopes, index-size calculations, and conditional local/cloud/hybrid routes. Read the final Minions study for task-level collaboration evidence without transferring its local-free cost assumption or server results to a phone.
5. **Interactive text generation.** Compare constrained rewrite/short dialogue with knowledge-intensive and difficult reasoning tasks. Preserve source-specific prefill/decode conditions; calculate illustrative 128/512-token completion times only where compatible phase data exist. Address cold/warm behavior, growing histories, foreground contention, context exhaustion, cancellation and device state. Provide a quality- and policy-based router with offline degradation.
6. **Frequent or continuous speech on constrained edge hardware.** Follow capture, resampling, VAD, chunk overlap, recognition, endpointing and transcript stabilization. Reconstruct the WhisperTRT 20-second clip benchmark from code and contrast independent noise/precision evidence without merging their boundaries. Calculate bounded 10%, 50% and continuous-duty energy/throughput scenarios. Explain why clip RTF does not prove live partial-result latency or continuous thermal stability. Include a brief vision-pipeline contrast; numerical vision claims require versioned pipeline evidence.
7. **Architecture, privacy and integration.** Draw local-only, cloud-only and hybrid data flows for documents/chat/speech. Track raw data, excerpts, embeddings, transcripts, logs, crash reports, backups/sync and fallback. Distinguish no training from no retention; system privacy architecture from application policy. Verify shipping APIs, device/region eligibility, foreground/background restrictions, downloads, model/runtime version skew, updates and rollback. Give explicit fallbacks for offline/sensitive cases.
8. **Task economics and conditional choices.** Compare API/network charges with incremental device hardware, energy, engineering/QA/support, distribution, correction and fallback. Separate existing-device marginal expense from a dedicated edge box. Calculate network transfer/latency and task-cost sensitivities with transparent assumptions. Conclude with a complete fit matrix and rules for offline use, sensitive data, bursty hard requests and sustained background work.

Appendices will keep model/configuration provenance, measurement conditions, executable calculations and the specific missing measurements needed to validate a deployment. The main report will make positive suitability judgments within those conditions.

## Author production units

- **ODM-U1: mechanisms and conditioned evidence.** Read the selected original configurations, hardware/runtime sources, performance and quality methods; reconstruct memory and phase-specific evidence. Flag key numeric premises for independent domain/evidence checking.
- **ODM-U2: three workload envelopes and architecture.** Build document, interactive and speech scenarios; inspect benchmark harnesses, API shipping/background rules and privacy boundaries. Use explicit reservations and duty-cycle scenarios where available evidence does not measure the whole device.
- **ODM-U3: economics, fit matrix and synthesis.** Execute memory/KV/index, latency/network and energy/cost calculations; produce conditional recommendations and assemble the preserved first complete manuscript.

These are practical authoring units rather than fixed-length chapters or new approval gates. Reading can proceed while independent outline review runs. This author will not review their own work independently.

## Reviewable exhibits and acceptance checks

- Hardware–model–task fit matrix retaining hardware, runtime, model/precision, conditions, evidence type, sustained limits, quality and integration constraints.
- Complete memory and context worksheets with decimal/binary units and available-memory reservations explicit.
- Phase-resolved latency and speech duty-cycle scenarios; measured values remain separate from derived values.
- Local/cloud/hybrid data-flow and fallback diagrams tied to the actual privacy boundary.
- Task cost/network sensitivities and conditional design decisions.

No new model performance experiment is authorized. Arithmetic and code/harness inspection are actual research work; absence of a sustained benchmark will be reported as a bounded deployment constraint, not filled with a fabricated score. The first full draft, original reading locations and calculation records will be preserved for independent review.
