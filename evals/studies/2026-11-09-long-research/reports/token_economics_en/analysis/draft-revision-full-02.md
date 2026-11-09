# Token Economics: From Model Costs and Pricing to Workload Value

Evidence cutoff: November 9, 2026. English research report for enterprise buyers, AI product operators and investors.

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


## 6. Workload A: a short support exchange

The task is a bounded question about a current return or service policy. Acceptance requires a correct answer to all material issues, no unsupported promise or unauthorized action, and a resolved customer need. A classified escalation is useful routing but becomes an accepted task only after resolution. The illustrative interactive target is first output within two seconds and a useful answer within ten seconds; it is a product assumption, not a measured guarantee from either API.

The rate anchors are the October 22, 2026 global standard Claude API list prices: Haiku 5.5 for the inexpensive route and Sonnet 5.5 for the stronger route. **The assigned quality rates are hypothetical conditions, not estimates of those models' performance.** No caching is enabled for this short case. A 1,500-input/500-output-token initial call costs $0.00040 at the inexpensive tariff and $0.00800 at the stronger tariff. A historical GPT-4o mini call with those counts costs $0.000525 at its July 2024 launch tariff; that is a price calibration, not a quality-matched temporal comparison.

The cohort contains 1,000 incoming tasks. A retry is permitted once, and a stronger fallback once where shown. The success probabilities are conditional on having failed the preceding stage; they are lower than first-attempt success to represent persistent difficult cases. The routing scenario assumes that the workflow detects the failures needing escalation. False acceptance is addressed separately below.

| Stage | Inexpensive-first route | Stronger-first route |
|---|---:|---:|
| First attempts / accepted | 1,000 / 700 | 1,000 / 900 |
| Retry attempts / accepted | 300 / 120 | 100 / 50 |
| Stronger fallback attempts / accepted | 180 / 108 | 0 / 0 |
| Human escalations / resolved | 72 / 66 | 50 / 46 |
| Final accepted / unresolved | 994 / 6 | 996 / 4 |

An inexpensive retry has 2,500 input and 500 output tokens. A stronger retry or fallback has 3,500 input and 500 output tokens, reflecting the prior exchange and diagnostic information. Model expense is therefore

\[
C_{cheap}=1,000(0.0004)+300(0.0005)+180(0.012)=\$2.71,
\]

\[
C_{strong}=1,000(0.008)+100(0.012)=\$9.20.
\]

Assume human escalation takes six minutes, including unresolved cases, and that 5% of machine-resolved cases receive a one-minute quality audit. Loaded human time costs $0.50/minute, or $30/hour. A $1.20 cohort allowance covers retrieval and logging/storage: $0.0002 retrieval per incoming task plus $1 for shared logging/storage. These are scenario operating allowances, not supplier quotations.

| Cohort economics | Inexpensive first | Stronger first |
|---|---:|---:|
| Model calls | $2.71 | $9.20 |
| Human minutes | 478.4 | 347.5 |
| Human cost | $239.20 | $173.75 |
| Retrieval/logging/storage | $1.20 | $1.20 |
| Total | **$243.11** | **$184.15** |
| Cost per incoming task | $0.2431 | $0.1842 |
| Cost per accepted task | **$0.2446** | **$0.1849** |

The first-call tariff is twenty times larger for the stronger route, yet accepted-task cost is about 24% lower under these quality and labor assumptions. The mechanism is 22 fewer human escalations and a different retry path. Counting only first calls would miss nearly the entire economic decision.

This is also a useful way to state the procurement condition. With these route probabilities fixed, the routes have equal accepted-task cost at approximately **$0.0492 per human minute**, or $2.95/hour. Below that value, the inexpensive route can win on direct cost; above it, the stronger route wins. This threshold is a property of the assumptions, including slightly different final acceptance rates. It is not a claim about actual wages or model quality.

Retry quality is more consequential here than modest output compression. If the inexpensive retry resolves 10%, 40% or 70% of its failed-first-attempt tasks, cost per accepted task becomes approximately **$0.3545, $0.2446 or $0.1353**. A useful diagnostic or better retrieved policy can therefore improve economics even without changing the base model. Repeating the original prompt without new information should not inherit the first-attempt success probability. An outage or an unavailable policy database can make all retries fail together; a circuit breaker or human route avoids paying for an unproductive loop.

A quality audit is not omniscient. If 1% of nominal machine resolutions are actually wrong and the 5% audit catches only the sampled errors, roughly 8.8 incorrect resolutions remain in the inexpensive-first cohort before any later customer return. Those should reduce true accepted count and may create remediation costs. A bot's confident completion flag is not a ground-truth label. In production, measure delayed reopening, unauthorized actions and severe errors separately from immediate conversational closure.

Outcome billing provides a commercial alternative to per-token pricing, but its definition matters. Intercom's September 23, 2026 description prices a resolution at $0.99 and includes confirmed or assumed resolutions; a later return for help reverses the charge. Configured procedure handoffs can also be billable outcomes. These are contractual units, not the same as this report's independent acceptance rubric or a measured autonomous success rate. [Fin outcome terms](https://www.intercom.com/help/en/articles/8205718-fin-ai-agent-outcomes)

The strongest public productivity evidence here concerns assisted work. A study of 5,172 support agents found about 15% more issues resolved per hour after access to an assistant, with substantial heterogeneity. The study measures a human support organization, not a bot replacing all agents. Its value is to show that integration and worker experience affect realized outcomes; it cannot supply the autonomous probabilities in this example. [Generative AI at Work, version 2](https://arxiv.org/pdf/2304.11771v2)

The practical choice is to route by evaluated task type and failure signal. Use the inexpensive path when its acceptance rate is high and errors are easy to detect and correct. Use the stronger model directly when failure would create costly customer history or escalation. A paid faster tier is worthwhile only if the actual response deadline affects abandonment or business value enough to cover its premium.

## 7. Workload B: reusable documents and grounded analysis

The task is a short, cited answer or structured extraction from a stable digital document set. Acceptance requires all critical fields to be correct after normalization, numerical units to be consistent, and material claims to point to valid passages. A valid citation that does not support the claim fails. Broader synthesis and cross-document reasoning should be evaluated as separate difficulty strata; a correct single-field lookup does not demonstrate that capability.

Each document set supplies a **120,000-token stable prefix**, plus 1,000 changing query/instruction tokens and an 800-token answer. There are 12 queries at minutes **0, 2, 4, 10, 12, 14, 30, 32, 34, 90, 92 and 94**. These are request-start times; assume each response begins before the next request, identical prefix/model/settings, no concurrency miss, and no prefix edit in the baseline. Sonnet 5.5 global standard rates supply the common price anchor.

Without caching, each query costs

\[
(121,000\times2+800\times10)/10^6=\$0.25,
\]

or $3 for the set. The 1,000 new tokens and 800 output tokens contribute $0.01 per query under all full-context cache options.

| Request minutes | Five-minute cache | One-hour cache |
|---|---|---|
| 0 | Write | Write |
| 2, 4 | Read, refresh | Read, refresh |
| 10 | Write after expiry | Read, refresh |
| 12, 14 | Read, refresh | Read, refresh |
| 30 | Write after expiry | Read, refresh |
| 32, 34 | Read, refresh | Read, refresh |
| 90 | Write after expiry | Read: previous use was 56 minutes earlier |
| 92, 94 | Read, refresh | Read, refresh |

At five minutes, four prefix writes cost \(4\times120,000\times2.50/10^6=\$1.20\); eight reads cost $0.096. Add $0.12 for changing input and output to obtain **$1.416**. At one hour, one write costs $0.48 and eleven reads cost $0.132, giving **$0.732** including changing input/output. The longer write is individually more expensive but avoids repeated creation. If the prefix changes at minutes 30 and 90, that one-hour strategy writes three times and costs **$1.668**. Query timing and document churn are economic inputs, not implementation trivia.

For a prefix with base price \(P\), write multiplier \(w\) and read multiplier \(r\), one write followed by \(N-1\) full reads costs \(P[w+(N-1)r]\). It beats \(NP\) uncached when \(N>(w-r)/(1-r)\). For this Sonnet tariff, the five-minute threshold is just over 1.26 uses, so two uses suffice if the second really hits. The one-hour threshold is just over 2.05 uses, so three uses are needed to beat uncached processing. Choosing one hour over five minutes requires the actual expiry/write pattern, not merely the total number of requests.

Google's explicit storage mechanism illustrates a different decision. In a separate scenario with twelve uses inside one hour, the observed Gemini 2.5 Flash rates make holding a 120,000-token text cache cost $0.12. Twelve prefix reads cost $0.0432, compared with $0.432 for twelve uncached prefixes. The prefix-only saving is $0.2688 before the changing input/output common to both paths. Storage-only break-even is \(1/(0.30-0.03)\approx3.70\) full uses per hour: four uses cover that storage charge. Keeping the same cache for 24 hours with just twelve uses would cost $2.88 in storage. This is a comparison within that tariff, not evidence that its model matches Sonnet's quality. Explicit lifetime management, deletion and document refresh therefore matter. [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing)

Long-context price boundaries can create discontinuities. Under the observed Gemini 2.5 Pro standard rates, 200,000 input and 800 output tokens cost **$0.258**. Adding one input token crosses the stated 200K band and gives **$0.5120025**, because the higher input and output rates apply to the whole request. That jump is much larger than the price of one token. A context-reduction strategy can avoid it, but only if it preserves the evidence required by the task.

To connect request costs to accepted outputs, consider 100 document sets and 1,200 incoming queries. Full-context variants all assume 90% first-pass correctness; 10% need six minutes of human repair, which succeeds on 90% of those repairs. Every query receives half a minute of validation. Human time is valued at $1/minute. Preparation costs $2 per set, covering the scenario's digital parsing, organization and local processing; scanned-document OCR would be a separate additional charge and quality constraint. These assumptions give 1,188 accepted tasks and 12 unresolved.

The retrieval alternative supplies 10,000 selected context tokens plus the same 1,000 query and 800 output tokens. It costs $0.03 per generation, $3 per document set for preparation/indexing, and $0.002 per retrieval. To expose the quality trade-off, first-pass correctness is assumed to be 86%, with the same validation and repair rules. This produces 1,183.2 expected accepted tasks, not a claimed observed integer cohort.

| Strategy | Model expense / 1,200 queries | Preparation/retrieval | Human expense | Accepted tasks | Cost per accepted task |
|---|---:|---:|---:|---:|---:|
| Full context, uncached | $300.00 | $200.00 | $1,320.00 | 1,188 | **$1.5320** |
| Full context, 5-minute cache | $141.60 | $200.00 | $1,320.00 | 1,188 | **$1.3987** |
| Full context, 1-hour cache | $73.20 | $200.00 | $1,320.00 | 1,188 | **$1.3411** |
| Retrieval, 86% first-pass correctness | $36.00 | $302.40 | $1,608.00 | 1,183.2 | **$1.6450** |

Retrieval has the smallest model bill but the highest accepted-task cost in this particular setting. It loses relevant context often enough to create repair work, while its index has an upfront cost. At 90% correctness it costs $1.3960 per accepted task, close to five-minute caching; at 94% it costs $1.1489 and beats the 90%-quality one-hour strategy. Retrieval can improve quality by excluding distractors as well as damage it by missing evidence. The right comparison measures both effects.

A one-percentage-point change in initial correctness changes repair demand by twelve queries, or **$72** of repair labor in this cohort, before the smaller denominator effect. The difference between five-minute and one-hour API expense is $68.40. This gives a concrete priority: preserve source coverage and validate retrieval quality before optimizing an already small cache bill. Once quality is stable, query scheduling, shared-prefix layout and selective retention can capture real savings without removing useful information.

## 8. Workload C: a coding agent with tools, retries and review

The principal task is a bounded repository change. Acceptance requires the requested behavior, relevant existing checks, no identified regression, and human approval of the actual change. Passing a benchmark's tests is evidence for its particular tests, not complete production acceptance. A research-agent variant additionally requires source support, coverage and accurate citations; more fetched pages do not by themselves satisfy that rubric.

The baseline attempt makes eight sequential Sonnet 5.5 calls. Total input contexts are **4K, 8K, 14K, 22K, 32K, 44K, 58K and 74K** tokens. These are scenario usage counts, including retained messages and tool results. Each call emits 2,000 billed output tokens, of which an illustrative 600 are visible and 1,400 are reasoning/internal generated work. The calculation uses the total 2,000 once. Keep effort and formatting settings stable, append context, and assume each subsequent request starts within the five-minute coverage window. No claim is made that a real eight-step task always fits that timing.

| Step | Total input | Previously cached input | Newly written input | Total billed output | Model cost |
|---:|---:|---:|---:|---:|---:|
| 1 | 4,000 | 0 | 4,000 | 2,000 | $0.0300 |
| 2 | 8,000 | 4,000 | 4,000 | 2,000 | $0.0304 |
| 3 | 14,000 | 8,000 | 6,000 | 2,000 | $0.0358 |
| 4 | 22,000 | 14,000 | 8,000 | 2,000 | $0.0414 |
| 5 | 32,000 | 22,000 | 10,000 | 2,000 | $0.0472 |
| 6 | 44,000 | 32,000 | 12,000 | 2,000 | $0.0532 |
| 7 | 58,000 | 44,000 | 14,000 | 2,000 | $0.0594 |
| 8 | 74,000 | 58,000 | 16,000 | 2,000 | $0.0658 |
| **Total** | **256,000 input processed/billed by category** | **182,000** | **74,000** | **16,000** | **$0.3632** |

Without reuse, ordinary input plus output would cost $0.672 for these counts. This difference does not make growing context free: read charges remain, new state is written, and long histories can reduce task quality. If a wait or configuration change prevents a hit, the relevant prefix must be repriced. Parallel branches incur all their calls and tools even when only one patch is selected.

After a failed baseline attempt, the workflow can compact context and retry once. The compaction call has 74K uncached input and 2K output, costing $0.168. The retry has three calls with 24K, 36K and 50K input and 3K output each; with the same incremental-cache convention it costs $0.221. Total retry model expense is therefore **$0.389**. Compaction is a paid transformation that may omit constraints; any quality effect belongs in the retry's conditional success rate.

After a failed retry, a three-call Opus 5.5 fallback has contexts of 30K, 45K and 60K, with 4K output per call. It costs **$0.555** under the corresponding write/read/output rates. A model switch starts a new cache domain; the fallback does not inherit the previous model's KV discount.

For 100 incoming tasks, assume 60 baseline successes; 40 retries succeed on 16; 24 stronger fallbacks succeed on 12; the remaining 12 receive human repair, resolving eight. The final result is **96 accepted and four unresolved**. Tool/sandbox allowances are $0.20 per baseline attempt, $0.15 per retry and $0.25 per fallback. They include executions that fail; these are scenario estimates for a self-managed tool environment, not a claim about a provider's container tariff. Review takes three minutes per baseline, two per retry and three per fallback. Human repair takes twenty minutes for each of the twelve escalations. Loaded labor is $1/minute.

| Component | Calculation | Cohort expense |
|---|---|---:|
| Model work | 100 × .3632 + 40 × .389 + 24 × .555 | $65.20 |
| Tools/sandbox | 100 × .20 + 40 × .15 + 24 × .25 | $32.00 |
| Review and repair | 100 × 3 + 40 × 2 + 24 × 3 + 12 × 20 minutes | $692.00 |
| **Total / accepted task** | $789.20 / 96 | **$8.2208** |

A stronger-first alternative uses Opus tariffs from the start, assumes 75 first successes, ten successes from 25 retries, and twelve resolutions from fifteen human repairs. With the defined tool/review paths it costs $765.84 for 97 accepted tasks, or **$7.8953 each**. It is a conditional comparison: the larger model needs enough improvement in initial success and remaining human work to justify its higher per-call expense. Merely replacing the name without measuring the new paths would not establish the saving.

The sensitivities show where to work first. The four output rows are **direct output-charge perturbations with every input history, cached-prefix ledger, retry/fallback path, tool charge, human-work allowance and acceptance rate held fixed**. They isolate the generated-output line of the bill; they do not recompute a fully retained conversation after changing its output lengths:

| Change to baseline agent scenario | Cost per accepted task |
|---|---:|
| Half the billed output per call, fixed input/path/quality | $8.0846 |
| Original output, fixed input/path/quality | $8.2208 |
| Twice the billed output, fixed input/path/quality | $8.4933 |
| Four times the billed output, fixed input/path/quality | $9.0383 |
| Retry conditional success 10% / 40% / 70% | $10.1581 / $8.2208 / $6.3627 |
| Baseline review one / three / six minutes | $6.1375 / $8.2208 / $11.3458 |

The output rows quantify only the direct billing effect under those fixed inputs. For example, at four times output, the first baseline call generates 8K tokens from 4K input while the next input remains the original 8K in this calculation. A workflow retaining the entire generated output would already require at least 12K tokens before adding new user or tool content. Its later input, cache writes/reads, compaction, timing and possibly quality would need to be recalculated; the $9.0383 figure is not the cost of that full-history workflow. Output compression can save direct output charges when quality holds, while reducing review or failed cycles can have substantially more value in the separate sensitivities shown. Reasoning effort should therefore be treated as a decision variable with a measured success response and a complete downstream trajectory when making an actual deployment choice.

A research-agent variant makes tool meters visible. Twenty successful DeepSeek searches and forty successful fetches cost **$0.045** at the observed $0.75/1,000 rate. Twenty OpenAI web searches have **$0.20 in search-call fees**, before retrieved-content/model tokens. These are different tool contracts and not a claim of equivalent retrieval quality. A failed fetch may be unbilled by one supplier but still delay the agent, require a new source, and add review. Storage of fetched documents, repeated summarization and citation checking also remain part of the path.

Human productivity should be measured after review and integration. METR's 2025 randomized study involved sixteen experienced developers and 246 real tasks in repositories they knew well. AI availability increased completion time by 19% in that setting, with implementation time including work around PR review. A February 2026 update reported estimates pointing toward speedup but identified participation, task selection and concurrent-agent time-accounting problems, so it did not provide a reliable new universal multiplier. The two findings jointly support measuring current completed work rather than assuming either permanent slowdown or automatic acceleration. [METR original paper](https://arxiv.org/html/2507.09089v1), [methodology update](https://metr.org/blog/2026-02-24-uplift-update/)


## 9. A defensible API versus self-hosting comparison

Self-hosting buys capacity and responsibility. An API buys a metered service with a particular model, endpoint and commercial contract. A useful comparison holds task acceptance and response requirements constant, then measures how each arrangement satisfies them. It should not substitute a small open-weight model for a frontier model solely because both produce text.

The infrastructure anchor here is a **Linux Azure Standard_NC80adis_H100_v5 node in East US**, purchased at the public Consumption rate rather than Spot, Low Priority or a reservation. The official Retail Prices response retrieved on November 9 lists **$13.96 per one hour**, with an effective-start field of March 1, 2024. The original JSON is preserved. The official SKU table specifies **two H100 NVL accelerators with 188 GB combined accelerator memory, 80 vCPUs and 640 GiB host memory**, plus 7,152 GiB of local temporary storage. Temporary storage is not durable application storage. The rate is for the whole node; it cannot be divided by two unless another workload actually pays or uses the other half in the relevant allocation. [Azure hardware specification](https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/gpu-accelerated/ncadsh100v5-series), [official retail-price API](https://prices.azure.com/api/retail/prices?currencyCode=USD&%24filter=serviceName%20eq%20%27Virtual%20Machines%27%20and%20armRegionName%20eq%20%27eastus%27%20and%20armSkuName%20eq%20%27Standard_NC80adis_H100_v5%27%20and%20priceType%20eq%20%27Consumption%27)

A candidate service is Llama 3.1 8B Instruct in FP16 on a vLLM serving stack. Weight storage alone is approximately 16 GB before framework, KV, temporary buffers and batching; the exact allocation and acceptance quality must be profiled. The model's public card establishes the release, GQA, supported languages and license. It does not establish equivalence to the commercial models in this report. The numerical capacity below is therefore an explicit engineering scenario, not a measured benchmark for this node.

A 2026 concurrency preprint usefully emphasizes load-sensitive costs, but its procurement crossover is not adopted here. It prices single-GPU runs at half the two-GPU node cost under a co-tenant assumption and compares against output-only API tariffs. At a 512-input/256-output workload, the comparable API charge per million output tokens is \(2p_{input}+p_{output}\), before caching and other meters. Adding input billing increases that comparator; the paper's statement that input billing would shift it downward is incorrect. The claimed raw-code commit could not be retrieved, and its stated 96 GB per GPU differs from the official SKU's 94 GB. These issues leave its general utilization mechanism useful but prevent treating its numeric crossover as a verified procurement result. [Concurrency study, setup and comparison](https://arxiv.org/html/2606.11690v1)

For the independent scenario, assume 730 provisioned hours per month, $3,000/month in operations and $300/month in durable storage, monitoring and network allowances. These amounts exclude application review common to both options; any differential review must be added. They are not cloud quotations. A single-node total is

\[
F=730(13.96)+3,000+300=\$13,490.80\;\text{per month}.
\]

Assume an independently validated future deployment could sustain **ten complete 512-input/256-output requests per second at the product's SLO**. This is a capacity assumption used to expose feasibility, not a prediction. It gives 26.28 million requests/month. Do not use a no-SLO peak token rate in its place. For comparison, one Sonnet 5.5 request with those token counts costs $0.003584; one Haiku 5.5 request costs $0.0001792 at the applicable ≤100K tariff.

| Monthly requests | Fraction of assumed 10-rps capacity | Node-plus-operations cost/request | Sonnet tariff/request | Haiku tariff/request |
|---:|---:|---:|---:|---:|
| 100,000 | 0.38% | $0.134908 | $0.003584 | $0.0001792 |
| 1,000,000 | 3.81% | $0.013491 | $0.003584 | $0.0001792 |
| 10,000,000 | 38.05% | $0.001349 | $0.003584 | $0.0001792 |

At equal acceptance quality, this node scenario crosses the Sonnet tariff at about **3.764 million requests/month**, or 14.3% of the assumed capacity. It crosses the Haiku tariff at about **75.283 million requests/month**, which exceeds that capacity: there is no feasible one-node crossover under these assumptions. This does not show that Haiku is universally preferable; it shows why choosing a favorable expensive API as the only comparator can make self-hosting look easier than it is.

Let \(q_L\) and \(q_A\) be local and API task acceptance rates, and let \(a\) be API request price. Ignoring differential variable costs for the moment,

\[
\frac{F}{Nq_L}<\frac{a}{q_A}
\quad\Longleftrightarrow\quad
N>\frac{Fq_A}{a q_L}.
\]

If local acceptance is 80% and API acceptance 90%, the Sonnet-price crossover rises to approximately **4.235 million requests/month**. Add correction cost per local failure and it can rise much further. Quality is an economic constraint even if the inference engine is exceptionally fast.

A second node for continuity raises the assumed monthly fixed cost to **$23,681.60**, keeping the same operations/storage allowances for illustration. At equal quality, the Sonnet-price crossover becomes about **6.608 million requests/month**. If the second node is active-active, capacity can grow; if it is reserved for failover, do not also count all of it as normal usable throughput. A single-node outage is different from a managed service with regional resilience. The appropriate reserve depends on the actual contract and cost of downtime.

Traffic also changes feasibility before the monthly bill. Ten million requests concentrated into a few business hours can exceed a deployment that handles the same monthly total evenly. Scaling down can reduce rental hours, but introduces model load/warmup delays, capacity availability and orchestration work. Spot discounts exchange price for interruption risk; they suit recoverable batch work more readily than a strict interactive deadline. Reserved capacity can lower the hourly rate but preserves a commitment during quiet periods. None is interchangeable with the on-demand baseline.

For API procurement, a hypothetical discount \(d\) changes price to \(a(1-d)\) and pushes the equal-quality hosting crossover to \(F/[a(1-d)]\). This is a sensitivity variable, not an invented negotiated offer. Model availability, retention terms, supported regions, rate limits and the cost of changing an integration also belong in the comparison. Procurement should seek a quote and a representative acceptance/latency evaluation together.

## 10. What dominates each workload

The calculations suggest different operating priorities rather than one rule to minimize tokens.

| Workload | Dominant variables in the worked case | First useful intervention | Condition that can reverse the decision |
|---|---|---|---|
| Short support | Human escalation, conditional retry success, severe-error rate | Improve policy grounding and route difficult cases before repeated failure | A cheap model with comparable acceptance and few escalations wins its large tariff advantage |
| Reusable documents | Validation/repair, useful cache reuse, retrieval recall, document churn | Keep a stable prefix and evaluate source coverage; choose TTL from actual arrivals | Sparse use or frequent prefix changes eliminates cache benefit; high-quality retrieval can win |
| Multi-step agent | Review/repair, failed trajectories, context/output growth | Improve stopping/fallback signals and reviewable artifacts; cap unproductive cycles | Higher reasoning or stronger models pay off only if they remove enough downstream work |
| Self-managed serving | Provisioned hours, SLO goodput, quality parity, operations/reserves | Measure the workload under arrival and reliability constraints | Bursty low load favors metered APIs; stable high load and suitable open models can favor hosting |

The right optimization target also depends on which cost is avoidable. Saving two minutes of a salaried employee's time creates capacity, but does not immediately reduce payroll. It may increase throughput, reduce overtime, accelerate a project or simply free time. Realized cash savings require a change in spending. Potential productivity value additionally depends on whether the freed capacity is used for valuable work. A workflow that saves API tokens but increases waiting, debugging or customer churn may destroy value despite a smaller invoice.

Latency requires a separate value model. A batch discount is attractive for overnight document extraction when the deadline permits it; it is not a like-for-like substitute for a live support response. Paying for faster service can be rational when measured abandonment or time-to-decision improves. A long agent may parallelize independent attempts to reduce elapsed time while increasing total compute. Report total work, critical-path duration and human attention separately.

Failure persistence changes the optimum retry count. If \(p_k\) is the conditional success probability of attempt \(k\) after earlier failures, expected additional acceptance is the probability of reaching that attempt times \(p_k\). Its cost includes generation, tools, evaluation and any delay. Retry when the expected incremental value exceeds that incremental cost and the task remains within its allowed risk/time budget. A low-quality evaluator can turn more attempts into more chances to accept an error; “keep trying until something passes” is not a sound economic stopping rule.

## 11. Value capture across the chain

```text
Hardware / networking / energy
        │ equipment, rental and infrastructure services
        ▼
Model developer / inference service
        │ capability, latency, reliability and contract
        ▼
Application and workflow operator
        │ integration, routing, evidence, review and distribution
        ▼
Customer
        │ accepted work, time/cash effects and willingness to pay
        └──────── revenue and demand flow back upstream ────────┘
```

Each layer sells a different unit and can retain value for a different reason. Hardware suppliers sell scarce capacity, performance and a software ecosystem. Infrastructure operators pool demand and provide availability, networking and operations. Model developers sell capability and a continually improving service. Applications turn that capability into an accepted outcome inside a workflow. Customers receive value only when those outcomes improve something they care about.

Public financial results demonstrate that large value pools exist upstream, but they do not identify model-specific margins. NVIDIA reported $96.221 billion revenue and 75.0% GAAP gross margin for the quarter ended July 26, 2026; Data Center revenue was about $89.0 billion. These are company/segment results across products, not a GPU rental margin or the profit on one million inference tokens. [NVIDIA Q2 fiscal 2027 results](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2027)

Microsoft's quarter ended September 30, 2026 reported $63.9 billion of Microsoft Cloud revenue; its investor metrics show a 66% Cloud gross margin. That aggregate includes multiple cloud businesses and a changing mix. It should not be assigned to an individual model endpoint, and investment-related gains or losses are distinct from the operating economics of serving a task. [Microsoft earnings release](https://www.microsoft.com/en-us/investor/earnings/fy-2027-q1/press-release-webcast), [Cloud metric definitions](https://www.microsoft.com/en-us/Investor/earnings/FY-2027-Q1/metrics)

Falling token prices do not determine the sign of profit change. In a simplified service, contribution is \(N(p-c)\), with volume \(N\), selling price \(p\) and avoidable unit cost \(c\), before fixed expense. If price falls from 1.00 to 0.80 and cost falls from 0.60 to 0.36, contribution per unit rises from 0.40 to 0.44. If cost stays 0.60, it falls to 0.20 and volume must double just to restore prior contribution. These are arithmetic examples, not estimates of a provider's costs. Demand growth, mix, capacity investment and model retirement add further effects.

The unit itself can change. Lower input prices may encourage longer documents; better agents may use more reasoning and tools per task. A provider can charge less per token while earning more per completed workflow, or lower total customer cost by improving success with fewer attempts. Revenue growth must be decomposed into customers, tasks, work per task and price by meter. Aggregate token growth alone does not prove productive demand.

For application vendors, model substitution puts pressure on markup attached only to access. Integration can preserve value when it supplies current proprietary context, dependable actions, auditable evidence and distribution that a customer would otherwise have to build. These are economic capabilities, not automatic defensibility: customers can switch when data and workflows are portable, and a model provider can incorporate adjacent functions. Switching costs may come from useful integration or from lock-in; buyers should value the former and price the latter as a future migration obligation.

An application charging $1 per accepted support task against the inexpensive-first scenario's $0.2446 operating cost has about $0.7554 left before its fixed engineering, sales, support, security and other expenses. It does **not** have a 99.7% margin merely because the model-call portion is tiny. An outcome contract also needs a dispute rule, a definition of resolution, treatment of reopened cases and protection against optimizing a billable proxy that customers do not value.

Customers should distinguish four quantities. **Willingness to pay** is what they would exchange for an outcome. **Potential productivity value** is what saved time or greater capability could be worth. **Realized savings** are verified reductions in spending or valuable capacity actually redeployed. **Revenue earned** is what a seller recognizes under its commercial arrangement. None can be inferred just by multiplying generated tokens by an hourly wage.

## 12. Conditional procurement and product decisions

1. **Choose a cheaper model when it clears the task's quality bar with comparable correction work.** Require matched evaluation of difficult cases, languages and long inputs. A general benchmark or low list price is insufficient; the support scenario shows why a small escalation difference can dominate the bill.
2. **Pay more when better capability removes costly work.** Compare the incremental model expense with reduced retries, tools, review, delay and error loss. The stronger-first routes are economically attractive only under their stated quality improvements.
3. **Cache stable, reused context with a measured lifetime distribution.** Keep changing questions after the stable prefix, retain actual usage categories, and include writes, expiry and storage. A cache strategy can be cheaper without reducing the information available to the model; shortening context requires a separate quality check.
4. **Use retrieval when it retains the evidence the task needs.** Include index/preparation and validation cost. Prefer a source excerpt or deterministic extraction when generation adds no needed value. For broad synthesis, evaluate missing evidence and cross-document dependencies explicitly.
5. **Bound agent loops and make review easier.** Preserve a usable change, diagnostic results and source evidence at each handoff. Stop, switch methods or escalate when the next attempt lacks new information. Price parallel branches and discarded candidates as real work.
6. **Self-host when suitable quality and sustained SLO-compliant demand justify capacity ownership.** Require a complete node/instance quote, a measured traffic envelope, operational staffing and a continuity plan. If the crossover exceeds capacity or depends on unmeasured quality parity, the business case is not yet established.
7. **Buy the contract needed by the workload.** Separate direct API and cloud channels, standard and priority, batch and interactive, regional processing, promotions and commitments. Record model identity and effective dates alongside price; evaluate alias migration before it changes the service.
8. **Measure customer value after adoption.** Track accepted throughput, delayed errors, human attention, user abandonment and actual spending. Use those observations to revise the route probabilities and thresholds, rather than treating initial token savings as a completed productivity result.

The central commercial opportunity is to convert improving models and serving systems into dependable work with less total effort. Token-price competition is one mechanism in that conversion. Quality, workflow design and utilization determine how much of the improvement reaches the customer and how much value each supplier can retain.


## Appendix: evidence and calculation boundaries

The report combines three evidence types. Public prices and technical/financial disclosures retain their version or observation date. Published studies retain their experimental setting. Workload acceptance rates, human time, tool allowances, demand and hosting capacity are explicit economic scenarios. Local tokenizer counts and deterministic arithmetic were actually executed; no model inference experiment was performed.

`workload_calculations.py` and `calculation-results.json` contain all route counts, price inputs, cache request rows, agent step rows and sensitivity cases. `tokenizer_count.py` and `tokenizer-results.json` retain the exact paired strings, package version and encoding-file hashes.

Historical OpenAI launch pages supply the dated model and price announcements. The DeepSeek R1 news URL redirected to the current quickstart, so it does not establish a historical R1 price here. Gemini rates use the official documentation version listed in the source record. The current GPT-6.1 model page resolves the short/long price boundary. The dated Claude rate card is used for commercial SKU prices, without inventing an underlying weight revision absent from that source.

The Azure quote retains the full public JSON and exact SKU rows. The report does not use post-cutoff Lambda rates. It also does not use the concurrency preprint's inaccessible raw commit or mismatched GPU capacity claim to assign a measured throughput to its independent hosting scenario. No confidential margin, negotiated discount, realized labor saving or language-wide token ratio is inferred.

For a deployment decision, replace the scenario quality/time/traffic inputs with a representative matched task evaluation and measured latency/availability. Keep failure and delayed reopening in the record. These inputs determine the procurement thresholds; further precision in a posted token price cannot compensate for an unknown accepted-task denominator.
