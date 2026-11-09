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

The sensitivities show where to work first:

| Change to baseline agent scenario | Cost per accepted task |
|---|---:|
| Half the billed output per call, unchanged quality | $8.0846 |
| Original output | $8.2208 |
| Twice the billed output, unchanged quality | $8.4933 |
| Four times the billed output, unchanged quality | $9.0383 |
| Retry conditional success 10% / 40% / 70% | $10.1581 / $8.2208 / $6.3627 |
| Baseline review one / three / six minutes | $6.1375 / $8.2208 / $11.3458 |

Output compression has value when quality holds; reducing review or failed cycles can have substantially more value. That is why reasoning effort should be treated as a decision variable with a measured success response. Doubling reasoning is beneficial if it reduces sufficiently expensive downstream work; otherwise it is added latency and cost. The table intentionally holds quality fixed to isolate the price effect, not to imply that reasoning is useless.

A research-agent variant makes tool meters visible. Twenty successful DeepSeek searches and forty successful fetches cost **$0.045** at the observed $0.75/1,000 rate. Twenty OpenAI web searches have **$0.20 in search-call fees**, before retrieved-content/model tokens. These are different tool contracts and not a claim of equivalent retrieval quality. A failed fetch may be unbilled by one supplier but still delay the agent, require a new source, and add review. Storage of fetched documents, repeated summarization and citation checking also remain part of the path.

Human productivity should be measured after review and integration. METR's 2025 randomized study involved sixteen experienced developers and 246 real tasks in repositories they knew well. AI availability increased completion time by 19% in that setting, with implementation time including work around PR review. A February 2026 update reported estimates pointing toward speedup but identified participation, task selection and concurrent-agent time-accounting problems, so it did not provide a reliable new universal multiplier. The two findings jointly support measuring current completed work rather than assuming either permanent slowdown or automatic acceleration. [METR original paper](https://arxiv.org/html/2507.09089v1), [methodology update](https://metr.org/blog/2026-02-24-uplift-update/)
