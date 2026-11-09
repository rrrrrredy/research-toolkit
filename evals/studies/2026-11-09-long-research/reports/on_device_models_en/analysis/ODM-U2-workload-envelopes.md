## 4. Private document assistance: keep retrieval close to the source

The most defensible local document assistant starts with retrieval and verifiable extraction. It does not ask a small model to read an entire personal archive in one prompt. A useful pipeline is:

```text
Local files → parsing / OCR → chunks with source locations → local embeddings / index
                                                            ↓
Question → retrieval → optional reranking → bounded evidence → answer + source spans
                                                            ↓
                                            citation and field validation → user
```

Each stage changes the quality envelope. OCR can lose a minus sign or a table heading before generation begins. Chunking can separate a clause from its exception. Retrieval can miss the decisive passage. A fluent response cannot recover evidence it never received. The system should retain page and span identifiers, present the supporting text, and distinguish extraction from synthesis. Exact identifiers and dates can be checked directly against source spans; a plausible summary requires a stronger semantic check.

The 10,000-vector worksheet in Section 2 is a modest local collection, not a claim that all its documents fit in model context. With a 4,096-token session, an example budget is 500 tokens for instructions and the question, 2,500 for selected passages, 300 for source labels and other framing, and up to 700 for the answer. That consumes 4,000 tokens and leaves a small margin. A phone can perform short, cited questions within this envelope if its model meets the domain's extraction quality target. The product should show the retrieved passages when it cannot produce a reliable answer. It should not replace missing evidence with the model's remembered facts.

A PC's larger usable working set makes a higher-precision small model, a reranker, or more context practical. It does not automatically make a 32K prompt the best design. Reading thousands of irrelevant tokens lengthens prefill, expands state and may make a small model less reliable. Use longer context when the task genuinely depends on it: reconciling a short series of related documents, checking several contractual conditions, or summarizing a complete technical note. Use retrieval and selective expansion for a large archive. The decision is governed by evidence coverage and answer quality rather than by filling the advertised context window.

For complex synthesis, a hybrid pipeline can keep parsing, indexing and selection local while sending approved excerpts to a stronger model. This is especially useful when a large file contains only a few passages relevant to the question. Suppose a 20 MB document would otherwise be uploaded over a 10 Mbit/s uplink. Payload transmission alone takes 16 seconds; at 1 Mbit/s it takes 160 seconds. Sending a selected 40 kB excerpt over the 10 Mbit/s link takes 0.032 seconds before transport overhead, round trips and inference. The calculation uses decimal bytes and assumes available throughput, not a promised network rate. If the document is already cached remotely, this first-upload advantage disappears; if offline operation or a strict local boundary is required, the remote route remains unavailable regardless of bandwidth.

The remote model still receives the excerpt's content. A summary can reveal a diagnosis, account balance or identifying event even when it omits the original document. Embeddings and extracted entities also remain data derived from the source. A useful hybrid design has a visible rule about which material may leave, applies that rule before constructing the outbound request, and keeps a local-only route with narrower capabilities. Calling an exchange “compressed” does not establish privacy.

### What collaborative document reasoning actually demonstrates

The final ICML 2025 Minions paper tests collaboration on FinanceBench, LongHealth and QASPER. Its stronger protocol decomposes work into simpler local jobs and coordinates them remotely, exploiting local parallelism rather than relying on one small model to solve the entire problem. This is a positive architectural result: carefully chosen local subtasks can reduce remote communication while preserving much of a stronger model's task performance. [Minions final paper, §§4–6](https://raw.githubusercontent.com/mlresearch/v267/main/assets/narayan25a/narayan25a.pdf).

Table 1 reports macro-average accuracy of 0.724 for remote-only GPT-4o and 0.709 for Minions with a Llama 8B local model. The corresponding average cloud charges are $0.233 and $0.042 per query. From the rounded table values, the collaborative system retains 97.9% of baseline accuracy at 18.0% of the cloud charge: an absolute accuracy loss of 1.5 percentage points and a 5.55-fold reduction in that charge. Local-only Llama 8B reaches 0.444. Thus the result supports coordinated assistance by the stronger model; it does not imply that an 8B local model alone provides remote-model quality. The paper uses January 2025 GPT-4o prices and treats local inference as free for this accounting. [Minions final paper, §3 and Table 1](https://raw.githubusercontent.com/mlresearch/v267/main/assets/narayan25a/narayan25a.pdf).

The latency result further clarifies where to apply this pattern. On ten LongHealth examples with an RTX 4090 local GPU, Table 2 reports 31.81 seconds for the 8B Minions system versus 11.00 seconds for remote-only. Those are workstation experiments, not phone measurements. A user willing to wait for a document analysis may accept the extra local work; a short interactive rewrite may not benefit. A phone with little parallel capacity cannot inherit the paper's batching advantage. The report also leaves formal privacy guarantees to future work. Its measured cost-quality frontier is evidence for a collaboration mechanism, while data disclosure, device energy and deployment cost still need their own accounting. [Minions final paper, §6.5, Table 2 and discussion](https://raw.githubusercontent.com/mlresearch/v267/main/assets/narayan25a/narayan25a.pdf).

For the selected hardware, the recommended progression is local retrieval and extraction on the phone, richer local evidence processing on the PC, and optional remote synthesis when quality requires it and the data policy allows it. The task contract should say what happens when extraction confidence is low or sources disagree: expand retrieval, show conflicting spans, request a human decision, or escalate within the permitted boundary. A model's uncalibrated confidence statement alone is insufficient to decide that escalation.

## 5. Interactive generation: optimize the useful response

Interactive text generation contains at least three different products. A rewrite transforms text that the user already supplied. A short dialogue uses a bounded application state. A general assistant must acquire facts, reason through unfamiliar tasks and sometimes invoke tools. Small local models are well aligned with the first two when the prompt is narrow. The third often benefits from a stronger cloud model, even if the network adds delay.

Apple's 2025 framework was explicitly designed around tasks such as extraction, summarization, refinement and short dialogue rather than general world-knowledge chat. Guided generation can make a response conform to a Swift data structure; it cannot establish that the fields contain true facts or that a proposed action is appropriate. This matters for local application design: a typed draft calendar event is useful if the user can inspect its date and location, while silently executing an uncertain action creates a different quality requirement. [Apple technical report, §7](https://arxiv.org/pdf/2507.13575v1).

The S24 results suggest a practical response design. A 128-token Gemma 3n E2B answer has a calculated warm phase sum of about 9.46 seconds with the cited 1,024-token GPU prefill; 512 tokens raises that extrapolated sum to about 34.07 seconds. Asking for a compact rewrite or a few extracted fields therefore improves responsiveness directly. Streaming makes progress visible but does not eliminate the total wait. A user may accept a first partial sentence quickly while still waiting for a final answer that can be validated or acted on. For structured actions, distinguish first visible output from the time when the complete validated object is usable.

The full timing model should be:

`time to usable result = queue + cold setup, if any + input preparation + prefill + generation + validation + presentation`.

Cold setup includes reading weights, allocating buffers, compiling kernels or building an accelerator engine. It may also include a first model download, which is a separate onboarding event rather than an inference latency. A 3 GB package takes at least four minutes over an otherwise available 100 Mbit/s connection, or forty minutes at 10 Mbit/s, before protocol overhead and verification. Keeping a model warm avoids some setup but occupies memory and may compete with the foreground app. A product should load deliberately, show readiness, cancel obsolete work, and release resources when the expected reuse no longer justifies residency.

Conversation history presents a second design choice. Appending every message preserves detail but increases prefill or cache occupancy. Reusing a valid prefix avoids repeating work, whereas changing earlier instructions or replacing history may invalidate it. Summarizing history can reduce state but may omit constraints or facts; the summary should retain structured commitments and link back to source messages when exact wording matters. Sliding attention and retrieval over prior messages are alternatives with different information-loss patterns. They should be evaluated on the kind of long conversation the product actually offers.

A practical router first checks policy and device readiness, then task difficulty and resource state. An offline-required rewrite goes to a ready local model or a simpler deterministic editing UI. A sensitive question can use local retrieval and return supporting passages when the local generator is inadequate. A difficult, nonsensitive analysis can go directly to the cloud when a local attempt would merely add delay. If the product uses a cheap local first attempt, escalation should depend on observable validation failures, missing evidence or a calibrated task classifier. Repeatedly asking the same small model to reconsider is not a reliable substitute for missing capacity.

The M4 Pro is a stronger candidate for a richer local assistant than the phone because it can accommodate larger working sets and the cited 3B runtime produces short outputs quickly. The Surface case is promising for tightly integrated NPU text transformations, but the available sources do not provide a matched throughput result against that Mac. Its 45 TOPS should guide neither a token-rate prediction nor a battery-life claim. A Windows product can choose the system model for supported tasks and an explicitly supported custom runtime for other models, retaining separate quality and performance qualifications for each path.

## 6. Frequent speech: make the entire pipeline continuous

Speech is a strong local candidate when the input is persistent, network availability is uncertain or raw audio should remain nearby. The relevant pipeline is broader than the recognizer:

```text
Microphone → capture / resampling → VAD → bounded chunks with overlap
                                         ↓
                                    speech recognizer
                                         ↓
                           overlap reconciliation / punctuation
                                         ↓
                         partial text → stabilized transcript → application
```

Capture and voice activity detection run even when no words are produced. Endpointing decides how long to wait before treating speech as complete. Overlapping chunks improve continuity but repeat computation. Punctuation, speaker attribution and application-level commands can require additional models. A product may need a small first-stage recognizer for immediate feedback and a later correction stage, or it may prefer an utterance-based result for voice commands. These are different latency targets.

WhisperTRT provides a concrete optimization result for an Orin Nano. At the fixed October 2024 repository commit, its README reports 0.86 seconds to transcribe a 20-second clip with `base.en`, compared with 2.55 seconds for the original Whisper backend. The corresponding reported memory figures are 439 and 666. Inspecting the code clarifies those figures: the profiling script runs a warmup, times one transcription by default, synchronizes the GPU around timing, and records the change in process RSS after execution. Its bit shift converts bytes to MiB, despite the README's MB label. Engine construction and model loading happen outside the timed call. The 439 MiB value is therefore a sampled RSS difference, not peak device memory. [Pinned WhisperTRT README](https://github.com/NVIDIA-AI-IOT/whisper_trt/blob/268eff10a1e38118a2734745b9db14f7419a08a5/README.md), [profiling code](https://github.com/NVIDIA-AI-IOT/whisper_trt/blob/268eff10a1e38118a2734745b9db14f7419a08a5/examples/profile_backend.py).

The rate result is encouraging: 0.86/20 gives a clip real-time factor of 0.043, leaving substantial compute headroom for a single stream under those benchmark conditions. The timed `transcribe` path includes its mel-spectrogram preparation and decoding; it does not include recording twenty seconds of future speech. A linear projection would require 154.8 seconds of recognition computation per hour of audio without overlap, or twice that with twofold repeated processing. This projection describes arithmetic capacity, not a measured continuous service, energy result or latency distribution.

The source code also identifies a concrete integration limit. This WhisperTRT path pads audio and truncates the mel representation to Whisper's 30-second window, then uses greedy argmax decoding. The example live program collects VAD-defined speech and sends a segment only after speech ends. It is consequently a useful utterance-transcription demonstration, but not a complete streaming-caption implementation. For uninterrupted long speech, the product needs bounded segmentation and overlap reconciliation before inference; otherwise material beyond the model window can be lost. Decoding options are not normalized across the compared backends, so the speed ratio is a result for the published paths, not proof of equal WER. [WhisperTRT model implementation](https://github.com/NVIDIA-AI-IOT/whisper_trt/blob/268eff10a1e38118a2734745b9db14f7419a08a5/whisper_trt/model.py), [live example](https://github.com/NVIDIA-AI-IOT/whisper_trt/blob/268eff10a1e38118a2734745b9db14f7419a08a5/examples/live_transcription.py), [Whisper audio constants](https://github.com/openai/whisper/blob/main/whisper/audio.py).

A useful deployment target for voice commands might permit utterance-end processing, while live captions require a bound on partial-text delay. In the latter design, use short rolling chunks, maintain an explicit maximum queue depth, and revise only an identified unstable suffix of the transcript. If recognition falls behind, preserving audio for later processing may suit a recorder; dropping old work to retain freshness may suit a live display. The choice follows the task. An always-on recorder must also specify whether audio is retained at all, for how long, and who can retrieve it.

### Precision, noise and energy change the speech choice

An independent 2024 study on an actively cooled Orin Nano 8 GB used JetPack 5.1, seventy LibriSpeech clips of roughly three to five seconds, and a separately corrupted version with added Gaussian noise. It measured incremental CPU-plus-GPU energy using `tegrastats`, after subtracting an idle baseline. Its noise procedure attenuated generated noise by 10 dB; this is not enough information to call the resulting speech a calibrated 10 dB SNR corpus. [ASR energy study, setup pp.4–7](https://arxiv.org/pdf/2405.01004).

Its Table 4 contains a useful counterexample to automatic gains from lower precision:

| WhisperX base, same study | Aggregate processing time | Reported memory | Incremental CPU+GPU energy | Clean WER | Noisy WER |
|---|---:|---:|---:|---:|---:|
| FP16 | 78.0 s | 4,029 MB | 155 J | 7.40% | 28.84% |
| INT8 | 80.1 s | 3,908 MB | 169 J | 7.83% | 30.69% |

Here INT8 saves about 3.0% of reported memory while taking 2.7% longer and consuming 9.0% more of the measured energy. Noisy WER rises by 1.85 percentage points. FP16 is the stronger choice for this model and experiment unless the memory saving is decisive. Other rows show different trade-offs, including lower energy for the medium INT8 model, so the result is not a universal rejection of INT8. The baseline-subtracted energy is not whole-box wall power, and these aggregate results are not commensurate with the WhisperTRT single-clip benchmark. [ASR energy study, Table 4, p.10](https://arxiv.org/pdf/2405.01004).

The selected edge device also has distinct operating versions. NVIDIA's later Super configuration advertises 102 GB/s bandwidth, 67 sparse TOPS and a 25 W module mode, with a supporting JetPack update. The earlier speech studies do not thereby become measurements of the Super mode. Higher clock and power options can enlarge the available throughput envelope, while cooling, power supply and the installed software remain part of the product configuration. [NVIDIA Super configuration and software requirements](https://developer.nvidia.com/blog/nvidia-jetson-orin-nano-developer-kit-gets-a-super-boost/).

For planning, assume an entire endpoint draws 4 W while idle and 15 W while actively computing. These are scenario inputs, not measured Orin power. Average power is `4 + duty × (15 − 4)` watts. At 10%, 50% and 100% compute duty, that gives 5.1, 9.5 and 15 W, or 0.1224, 0.228 and 0.360 kWh per day. The calculation concerns compute duty, not the fraction of time someone speaks: a recognizer faster than real time can process continuous audio with intermittent compute, while overlap, VAD, postprocessing and other workloads increase its occupancy. Keeping those quantities separate prevents an incorrect battery or cooling estimate.

| Assumed active whole-device power | 10% compute duty | 50% compute duty | Continuous computation |
|---|---:|---:|---:|
| 10 W, with 4 W idle | 4.6 W average | 7.0 W | 10.0 W |
| 15 W, with 4 W idle | 5.1 W | 9.5 W | 15.0 W |
| 25 W, with 4 W idle | 6.1 W | 14.5 W | 25.0 W |

A constrained edge box is thus attractive for frequent local speech when an appropriate recognizer passes the noise and vocabulary target, the pipeline bounds segment length, and sustained operation leaves queue and thermal headroom. Use the cloud for occasional difficult recordings, broad language coverage or stronger diarization when the data boundary permits it. A hybrid speech product can keep the raw stream local and send selected transcripts for reasoning, or upload only user-selected uncertain segments for re-recognition. The first reduces audio transfer but still discloses transcript content; the second requires consent to move the audio itself.

Vision follows the same whole-pipeline principle but cannot inherit speech throughput. Camera capture, exposure, resize, color conversion, frame selection, detection and tracking all consume resources. Raw 1,920×1,080 RGB frames at 30 frames/s represent about 186.6 MB/s before compression. That arithmetic supports local filtering or selecting relevant frames before transfer, not an inference-rate claim. For a continuous visual function, a compact detector or tracker at a reduced frame rate can be a better fit than repeatedly invoking a multimodal language model on every frame. A richer model can handle selected events locally or remotely after the time-critical stage has acted.
