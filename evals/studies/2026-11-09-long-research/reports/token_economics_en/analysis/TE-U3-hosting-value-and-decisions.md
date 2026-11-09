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
