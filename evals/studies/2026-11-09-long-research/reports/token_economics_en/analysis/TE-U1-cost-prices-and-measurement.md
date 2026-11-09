## 1. The economic unit is a task that meets its acceptance criteria

A token tariff is one input to an operating model. A buyer needs to know how much work reaches the required standard, how quickly it arrives, and what remains for people or another system to do. A cheap request can be an expensive task if it produces a plausible error, adds another round of investigation, or passes a problem to a person with a longer history to reconstruct. Conversely, a small model that reliably performs a narrow classification or extraction can be the right choice even when a larger model has better general benchmarks.

This report uses public evidence available by **November 9, 2026**. Historical offers retain their historical dates; observations of changing documentation are dated November 9. Prices are US dollars unless stated otherwise. The three worked workloads combine public list prices with explicit assumptions about traffic, quality, review time and workflow. Their arithmetic was executed locally. They are economic scenarios, not new model performance measurements or forecasts of a named provider's success rate.

The useful sequence is to define acceptance, measure complete paths, price those paths, then choose an architecture. “Accepted” means meeting the task's actual rubric, including material errors that an automated checker might miss. “Request” means one model invocation. “Attempt” means a bounded effort that can contain several requests. A trajectory is the complete sequence of model and tool actions. A task can finish accepted, escalated or unresolved; escalation is not itself successful completion. A vendor's billable outcome is a separate contract term.

For a cohort of incoming tasks, use

\[
C_{accepted}=\frac{C_{model}+C_{tools}+C_{data}+C_{human}+C_{allocated\ operations}}{N_{accepted}}.
\]

Include expenditure on unresolved tasks in the numerator. Report the acceptance and unresolved rates beside the ratio: a service that accepts only easy tasks may have a low ratio while failing the business requirement. Where harm has a material expected cost, add that loss separately; a lower operating bill does not compensate automatically for unauthorized actions or expensive mistakes.

## 2. Five ledgers that should remain separate

| Ledger | What belongs in it | What it does not establish |
|---|---|---|
| Model production | Training runs, experiments, data preparation, researchers/engineers, post-training and evaluation | The marginal cost of serving the next request |
| Investment allocation | An explicit share of past development spending allocated across a chosen life and monetization volume | A universal training-recovery tariff or a provider's accounting policy |
| Inference infrastructure | Hardware/rental, power where separately paid, memory/network, serving software, idle capacity and reliability reserves | The provider's selling price |
| Provider price | Token, cache, tool and service-tier charges under a dated contract | Private infrastructure cost or gross margin |
| Application operation and value | Orchestration, retrieval, tools, review, support, integration, customer outcomes and revenue | Realized savings merely because an output was produced |

Purchased equipment is a cash investment that can support many runs. Depreciation allocates its value over time; an economic obsolescence estimate need not match accounting depreciation. A rental rate already includes the lessor's financing, overhead and margin. Adding a full equipment purchase or its depreciation to that same rental expense double-counts infrastructure. Similarly, once training is complete, its historical expenditure does not become avoidable by declining one inference request. It still matters to long-run investment returns and the sustainability of the business.

DeepSeek-V3 provides a particularly useful boundary example. Its version-1 report attributes 2,664,000 H800 GPU-hours to pretraining, 119,000 to context extension and 5,000 to post-training. The total is **2,788,000 hours**; at the report's assumed $2 per GPU-hour, the estimate is **$5.576 million**, including $5.328 million for pretraining. Prior research and ablations are explicitly excluded. Thus this number is broader than pretraining alone and narrower than the organization's development expenditure. The architecture has 671 billion total parameters but 37 billion activated per token; activation count does not imply that only 37 billion parameters need infrastructure capacity. [DeepSeek-V3 report, Table 1 and architecture](https://arxiv.org/html/2412.19437v1)

Meta's Llama 3.1 card supplies a differently bounded comparison: 1.46 million H100-80GB GPU-hours for 8B, 7.0 million for 70B and 30.84 million for 405B, totaling 39.3 million. These are hardware-time disclosures, not reported dollar costs. Multiplying all of them by DeepSeek's H800 rental assumption would conflate chips, systems and commercial arrangements. The 8B model is a July 23, 2024 release with GQA and a custom commercial license, rather than an unrestricted commodity interchangeable with any API. [Meta model card](https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md)

The training-cost literature explains why estimates differ. Cottier and colleagues separate depreciated hardware plus energy, cloud rental equivalents, and broader development including staff and experiments. Their historical cloud-rental estimates are roughly twice the bottom-up estimates on average; individual estimates are highly uncertain. That is evidence about estimation methods and past investments, not a reason to treat either method as a provider invoice. [Training-cost study, methods and results](https://arxiv.org/html/2405.21015v1)

An investment-allocation scenario makes the missing variables visible. Let development investment be \(F\), the share attributed to a model/service be \(\alpha\), and lifetime monetized output be \(Q\) tokens. The allocation per million output tokens is \(10^6\alpha F/Q\).

| Assumed investment | Allocated share | Assumed lifetime output | Allocation per million output tokens |
|---:|---:|---:|---:|
| $10 million | 100% | 1 trillion | $10 |
| $100 million | 100% | 1 trillion | $100 |
| $100 million | 25% | 10 trillion | $2.50 |
| $1 billion | 100% | 10 trillion | $100 |

These examples do not estimate any named company's recovery policy. Retirement, model substitution and unexpectedly low demand reduce the denominator; reuse of training work across products changes the allocation share. Charging this allocation to an internal profitability report is different from deciding whether an additional request generates positive contribution over avoidable serving cost.

## 3. Why serving economics change with the workload

Prefill processes the prompt and constructs intermediate attention state. Decode repeatedly generates additional tokens while consulting that state. Long prompts can make prefill expensive and delay the first token; long answers extend serial generation and keep memory occupied. Reasoning adds generated work even when the visible answer is short. A token saved from a repeatedly reused prompt, a token removed from a long reasoning trace, and a token removed from a brief answer need not save the same infrastructure resources or have the same effect on quality.

At low batch sizes, decode often spends much of its time moving weights and KV state. Batching can amortize weight reads across requests, but consumes more cache memory and can increase queueing. A long prefill can interrupt responsiveness for already decoding requests. DistServe addresses that interference by placing prefill and decode separately and allocating resources for latency-compliant goodput. Its experiments used OPT models in FP16, 32 A100-80GB GPUs and generated Poisson arrivals on selected text workloads. Fault tolerance and some runtime policies remained outside that implementation. This supports the serving mechanism; its speedup is not a 2026 frontier-model unit-cost estimate. [DistServe, architecture and evaluation](https://arxiv.org/html/2401.09670v3)

For a fixed deployment, define goodput as requests meeting the specified latency and correctness requirements, rather than all emitted tokens. GPU occupancy is not the same as economic utilization. A GPU can have a kernel resident much of the time while processing an inefficiently small batch. It can also generate many tokens that arrive too late or fail acceptance. Capacity planning must retain the traffic distribution, prompt/output lengths, concurrent work, cache sharing and response deadlines.

Quantization can reduce resident weight bytes and bandwidth, but its speed depends on kernels and hardware support. Mixture-of-experts models reduce active arithmetic while retaining large weights and routing/interconnect demands. Speculative decoding can improve latency when a draft model's proposals are often accepted; rejected proposals still use resources. Prefix reuse reduces repeated prompt processing, but does not remove new output generation or the need to attend to relevant context. Reliability adds replicas, failover reserves and operational work. A capacity plan at the absolute throughput ceiling usually has little room for bursts or failures.

These mechanisms explain both lower prices and persistent price dispersion. A provider can improve cost through architecture, utilization, hardware procurement and software. It can also change prices for competitive or strategic reasons. Observing the tariff alone cannot distinguish those causes or reveal the margin.

## 4. Dated prices and the contract around them

The table is deliberately selective. It compares offers, not equal-quality outputs. “Observed” identifies a November 9, 2026 documentation snapshot, not proof that a rate applied throughout 2026. All token rates are **USD per million**. Historical announcement pages do not establish a serving region or a negotiated discount; those cells remain unspecified. Global scope is used only where the rate card states it.

| Date/basis | Model or commercial SKU | Channel/scope/tier | Input | Cached read | Output | Important boundary |
|---|---|---|---:|---:|---:|---|
| July 18, 2024 launch | GPT-4o mini | Direct API; region unspecified; ordinary token tariff | 0.15 | Not established by launch passage | 0.60 | Historical offer; current model page marks the 2024-07-18 snapshot deprecated |
| June 2024 announcement, displayed June 21 | Claude 3.5 Sonnet | Anthropic API offer; geographic scope unspecified | 3.00 | Not established here | 15.00 | 200K context; later caching page is not used to backdate a launch cache price |
| April 14, 2025 launch | GPT-4.1 / mini / nano | Direct API; region unspecified; standard | 2 / .40 / .10 | .50 / .10 / .025 | 8 / 1.60 / .40 | Additional 50% Batch discount at launch; no separate long-context surcharge in that offer |
| December 26, 2024 announcement, effective February 8, 2025 | DeepSeek-V3 | Direct API; region unspecified | .27 miss | .07 hit | 1.10 | Published future price change; not the temporary V2-level launch promotion |
| June 2025 stable-model announcement | Gemini 2.5 Flash | Gemini API; paid offer; geography unspecified | .30 text/image/video | Not reconstructed historically | 2.50 | Output includes thinking; historical terms kept separate from current cache rates |
| October 22, 2026 effective list card | Claude Haiku 5.5 | Claude API, global standard, ≤100K | .10 | .01 | .50 | Above 100K, rates are .50/.05/2.50 |
| Same dated card | Claude Sonnet 5.5 | Claude API, global standard, all context bands | 2.00 | .10 | 10.00 | 5-minute/1-hour writes 2.50/4.00 |
| Same dated card | Claude Opus 5.5 | Claude API, global standard, all context bands | 4.00 | .20 | 20.00 | 5-minute/1-hour writes 5.00/8.00 |
| November 9 observation | GPT-6.1 Sol | Direct API, standard, ≤272K input; no regional processing premium | 2.00 | .10 | 10.00 | 30-minute/12-hour writes 2.50/5.00; longer input changes the full-request rates |
| November 9 observation | Gemini 2.5 Flash | Developer API, paid standard; geography unspecified | .30 text | .03 text | 2.50 | Explicit storage $1 per million token-hours; announced December 1 alias replacement is after cutoff |
| November 9 observation | DeepSeek-V4.1-Flash-1017 via `deepseek-flash` | Direct API, peak; geography unspecified | .30 miss | .006 hit | 1.20 | Off-peak is half; legacy aliases no longer identify old weights |

Historical sources: [GPT-4o mini](https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/), [Claude 3.5 Sonnet](https://www.anthropic.com/news/claude-3-5-sonnet), [GPT-4.1](https://openai.com/index/gpt-4-1/), [DeepSeek-V3 price announcement](https://api-docs.deepseek.com/news/news1226), [Gemini 2.5 announcement](https://developers.googleblog.com/en/gemini-2-5-thinking-model-updates/). Cutoff-period sources: [Claude dated rate card](https://assets.claude.com/5633dc848caa431115468f31c7085d695bbfb9cc.pdf), [GPT-6.1 Sol model terms](https://developers.openai.com/api/docs/models/gpt-6.1-sol), [Gemini Developer API pricing](https://ai.google.dev/gemini-api/docs/pricing), [DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing/).

The direction of historical price movement is therefore a question about a chosen task and offer. A newer low-price SKU can have a different tokenizer, answer length, quality, thinking behavior or cache contract. The GPT-4.1 announcement itself reports different coding results for the family, under a specific harness with exclusions; the common branding does not make nano, mini and full models interchangeable. Neither that benchmark nor a model's claimed general ranking supplies the support or document acceptance rates used below.

Several billing distinctions materially change arithmetic:

- **Writes are a token category.** Do not bill a token at ordinary input and the full write tariff simultaneously. Claude distinguishes ordinary input, creation and reads; the newer OpenAI cache contract does likewise. Count each input token in its actual usage category.
- **Lifetime and matching matter.** Claude caches require a matching prefix, and the selected 5.5 SKUs have a 512-token minimum. Read use refreshes lifetime from request start. A changed early instruction can invalidate a long prefix. Parallel requests sent before the first response begins need not receive the intended hits; batch execution order also makes reuse uncertain. [Claude cache lifecycle](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- **A cache is not a universal discount.** OpenAI's newer 30-minute/12-hour write terms differ from older no-additional-write-charge models. Its documentation distinguishes eligibility for discounted reads from guaranteed physical KV reuse or lower latency. A 12-hour upgrade can trigger a new write charge. [OpenAI caching](https://developers.openai.com/api/docs/guides/prompt-caching)
- **Explicit storage creates time exposure.** Gemini's `generateContent` explicit cache is billed for reads and storage duration; implicit caching and explicit caching are different mechanisms. Its Interactions API does not offer the same explicit-cache control. [Gemini cache documentation](https://ai.google.dev/gemini-api/docs/caching?generate-content=true)
- **Reasoning is generated work.** Where output totals already include reasoning, adding reasoning again double-counts it. An output limit can be exhausted before a visible answer appears. Cost models should use actual billed usage, including incomplete attempts. [OpenAI reasoning accounting](https://developers.openai.com/api/docs/guides/reasoning)
- **Tools have separate meters.** The observed OpenAI table lists search-call fees and retrieved-content tokens, file-search calls/storage, and container session terms. Audio has token or time-based charges; images can use resolution-dependent units. The same visible answer can therefore have a different bill depending on its pipeline. [OpenAI pricing and tools](https://developers.openai.com/api/docs/pricing)

At the cutoff, DeepSeek peak periods are 01:00–04:00 and 06:00–10:00 UTC on weekdays, excluding Chinese public holidays. Its Search/Fetch service charges $0.75 per 1,000 successful requests, with specific HTTP/result conditions; failed requests, empty search results and timeouts are unbilled under that tool contract. Failure can still consume application time and downstream resources. [DeepSeek price and tool rules](https://api-docs.deepseek.com/guides/search)

Standard list prices are not negotiated enterprise economics. A public batch discount exchanges speed/scheduling flexibility for price. A priority premium buys a different service tier, not a guaranteed improvement in task correctness. Regional processing premiums reflect a distinct offer. Committed-use plans exchange a spend obligation for discounts and can leave unused capacity. Promotions must retain their end dates; a displayed rate announced for November 16 is outside this report's November 9 cutoff.

## 5. Tokens do not standardize work across models or languages

Tokenizers segment content differently. The relevant comparison is the price of the same useful content and task, not equal counts of unlike tokens. Context limits are also tokenizer-dependent. Shortening a prompt can lower the bill yet remove the evidence needed to answer correctly. Reducing JSON formatting can save little while losing a reliable downstream interface.

To illustrate the measurement issue, the author actually encoded six local strings using **tiktoken 0.12.0**, with the exact text and encoding-file hashes saved in `tokenizer-results.json`. Four are author-composed versions of a brief return/refund instruction; JSON and Python are alternative representations with different syntax. This is a small controlled illustration, not a language-wide evaluation or a billed-usage measurement.

| Sample | Unicode code points | UTF-8 bytes | `cl100k_base` tokens | `o200k_base` tokens |
|---|---:|---:|---:|---:|
| English | 146 | 146 | 31 | 29 |
| Mandarin | 44 | 124 | 39 | 34 |
| Spanish | 161 | 167 | 43 | 36 |
| Arabic | 113 | 201 | 82 | 39 |
| JSON | 124 | 124 | 33 | 33 |
| Python | 160 | 160 | 44 | 44 |

The Arabic/English token ratio changes from 82/31 to 39/29 for these particular strings. That is enough to reject a fixed language multiplier for all tokenizers; it does not rank model quality in Arabic. Raw-text counts omit chat framing, hidden instructions, tools and multimodal encoding. Invoice comparisons require endpoint usage fields and fixed model/configuration versions. [Official tokenizer implementation](https://github.com/openai/tiktoken)

For procurement, create a representative task set with language, input length, output rubric, urgency and difficulty strata. Preserve successful and failed trajectories, evaluator errors, tool calls and review time. Compare candidate workflows on the same acceptance criteria. Re-run a representative subset when a model alias, prompt, retrieval system or evaluator changes; the unit economics can drift even if the posted tariff remains constant.
