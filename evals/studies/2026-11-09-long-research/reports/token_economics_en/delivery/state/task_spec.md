# Research brief

## question

Investigate how model-production costs, inference costs, API prices, and customer value relate to one another, and why a low price per token may not imply a low cost per successful task. Focus on public evidence from 2024 through the cutoff of 2026-11-09, using earlier observations where needed to interpret changes. Record the date, currency, region, service tier, and relevant model version for price comparisons. Use only material publicly available by the cutoff; later price changes must not be substituted for historical terms.

Separate training and development expenditure, possible training-cost amortization, inference infrastructure costs, provider selling prices, and application-level operating costs. Explain how model architecture, hardware, utilization, batching, context length, output generation, and serving reliability affect inference economics. Distinguish marginal operating cost from fully loaded cost and sunk investment. Where providers do not disclose costs or allocation policies, use transparent ranges or scenarios rather than claiming to know private margins or a universal training-cost recovery rate.

Compare input and output pricing, cache writes and reads, cache lifetime and hit rates, reasoning-token billing where disclosed, batch or priority tiers, and relevant tool or multimodal charges. Explain why tokens from different tokenizers or languages are not necessarily equal units of work. Distinguish public list prices from negotiated, promotional, or committed-use terms. A dated price table should support the analysis, not become the whole report.

Construct task-level economic models for three contrasting workloads: a short interactive support exchange, long-document extraction or grounded analysis with reusable context, and a multi-step coding or research agent with tools and retries. State the quality and completion criteria for each workload. Account for failed attempts, context growth, fallbacks to other models, tool execution, storage or retrieval where material, and human review. Show formulas, units, and worked numerical examples based on public inputs or explicitly labeled assumptions. Separate cost per request from cost per accepted task, and do not assume retries are independent or eventually succeed without evidence.

Use sensitivity analysis to examine which variables dominate each workload: output length, reasoning effort, cache reuse, utilization, retry frequency, model choice, latency requirements, and human intervention. Compare API use with a defensible self-hosting scenario where public information permits it, including underutilization and operational overhead. Explain the quality or demand conditions under which a cheaper model, more expensive model, caching strategy, or shorter workflow changes total economics. Avoid treating every saved token as an equal gain if it changes task success or user value.

Connect the calculations to value capture across hardware and infrastructure providers, model developers, application vendors, and customers. Examine how falling prices, model substitution, proprietary workflow integration, distribution, and switching costs may redistribute value without assuming that lower prices automatically destroy or increase provider profits. Distinguish realized savings, willingness to pay, potential productivity value, and revenue actually earned.

Deliver a complete report containing dated pricing comparisons, the three workload models, sensitivity results, and a value-chain map with conditional procurement and product decisions. The principal checks are whether cost, price, and value remain separate; whether arithmetic can be followed from its inputs; and whether task-quality, retry, and utilization effects are represented. Do not invent confidential costs, contractual discounts, or measured productivity gains. Different conclusions about API procurement, self-hosting, and product margins are acceptable when their assumptions and break-even conditions are explicit.

## audience

Enterprise buyers, AI product operators, and investors assessing workload economics and value capture

## scope

Follow the task geography, comparison scope and evidence cutoff of 2026-11-09. Each other-language version uses its frozen sources without seeing the first-language report.

## output

Complete long-form research report final.md with the task-specific comparisons, explanations, tables and locatable citations. Preserve the first draft and actual independent results.

## depth

A full economic research report with auditable workload calculations, explicit cost and price distinctions, sensitivity analysis, and value-chain interpretation.

## evidence_standard

Use original public sources with actual dates, reading evidence and retained originals. Conduct seven separate independent content perspectives, relevant domain review, independent audit and final acceptance. Live primary research
