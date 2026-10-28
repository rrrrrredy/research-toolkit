# Optional Analysis Lenses

[English](optional-analysis-lenses.md) | [简体中文](optional-analysis-lenses.zh-CN.md)

Use this file when selecting a method for a specific research question. Do not force every project into every lens.

## Selection Rule

Select lenses that help answer the user's questions, based on the required coverage, useful explanatory dimensions and available evidence. Combine them when they contribute different explanations; omit those that merely repeat a point. There is no fixed number of primary or supporting lenses, and their names need not become report headings.

Ask:

- What does the reader need to understand?
- What kind of evidence is available?
- What kind of claim is the report making?
- Which lens would change the answer, not merely add decoration?

## Applying methods to the question

Choose the approaches that help answer the current question and combine them when useful. They are not sequential steps or required sections. Domain lenses follow below; see [assembly](research-workflow.md#9-assembly) for organizing a complete report.

### Compare: what does the difference change?

Choose dimensions around the options or phenomena the reader needs to distinguish, and explain each object against that same question. Shared capabilities may show that a feature no longer differentiates the options. Differences need consequences: conditions for adoption, sources of cost or divisions of responsibility. Retain concrete designs and facts that affect the judgment instead of converting each table cell into a sentence.

Where evidence is uneven, compare what it supports and identify which differences remain unresolved. Explain the comparable scope of results with different populations, dates, units or measurement conditions. Another sample's accuracy cannot complete a throughput comparison, and separately achieved metrics do not establish that one option meets all requirements together.

### Explain: what conditions produce the outcome?

Connect relevant conditions, actions and outcomes, explaining how the intermediate steps work. Compare possible explanations against specific material: which facts make one explanation more convincing than another? For example, increased adoption may relate to capability, price or distribution changes. Coincidence is a lead; user behavior, timing or other discriminating evidence is needed to distinguish the explanations.

Treat an explanation as revisable and change it when the material does not support it. Develop historical turning points that explain the current question, using [historical and comparative analysis](horizontal-vertical-analysis.md) when useful. When causes cannot be distinguished, explain what relationship is known and what remains unknown, while answering other supported questions.

### Synthesize: what do the sources establish together?

Bring facts addressing the same question together. Determine whether they support each other, expose a trade-off, or appear to conflict because their objects, periods or definitions differ. Identify which cases support a cross-case pattern; unexplained differences may narrow its scope or become an important finding. Multiple articles repeating one original claim do not add independent support.

A synthesis passage should advance the reader's understanding: what the preceding sections jointly support, which conditions explain divergence, and how this answers the original question. Retain the sources and conditions used in that reasoning. Neither source volume nor a forceful conclusion establishes depth.

### Recommend: why choose this path?

When the task calls for a choice, distinguish currently feasible options from conditional ones, then explain trade-offs against the user's objectives. Compare cost, performance and timing within the same delivery scope, and explain whether an advantage changes the choice. Forecast demand, proposed discounts and unconfirmed upgrades can inform scenarios; state which changes in conditions would change the recommendation.

Example from the existing [synthetic SaaS materials](https://github.com/rrrrrredy/research-toolkit/tree/main/evals/studies/2026-10-19-external-batches/tasks/open-weight-saas-lockin-en-20261017-retest/sources): S4 reports 81% versus 76% exact-match success on 500 tasks for a closed model and OW-A, with list inference prices of $4.20 versus $1.10 per 1,000 tasks. S2 says only 2 of 11 advisory-board members have MLOps capacity; others want vendor-managed options. This supports comparing vendor-managed open-weight deployment, rather than recommending customer self-hosting from price alone. Whether switching is worthwhile depends on the success-rate gap and operating/error-handling costs absent from the pack. These are synthetic inputs, not market findings.

## Framing And Category Analysis

Use when the topic involves positioning, legitimacy, category creation, belief formation, media translation, strategic communication, or public meaning.

Core questions:

- Who is trying to define the category?
- What language, metaphor, metric, or storyline do they promote?
- Through what channels does it spread?
- Whose behavior changes because of the positioning or category definition?
- What counter-story challenges it?

Do not use framing/category analysis as a default synonym for all industry research.

## Horizontal-Vertical Analysis

Use when the object needs both:

- a longitudinal view: origin, timeline, phases, turning points
- a cross-sectional view: current peers, substitutes, competitors, adjacent cases

Good fits:

- product or company histories
- market category studies
- technology adoption studies
- concept genealogy plus current competition
- founder or institution trajectories

Risk:

- The method can become too large and dominate the article.
- It can push the agent into a full historical report when the user asked for a narrower judgment.
- It can produce mechanical "timeline + comparison" writing if the thesis is weak.

Mitigation:

- Use it as an optional lens, not as the skill's default process.
- Keep detailed horizontal-vertical instructions in `horizontal-vertical-analysis.md` or an external skill.
- Invoke it only when the user asks for it or when the task genuinely requires time depth plus current comparison.
- State which parts are being used: vertical only, horizontal only, or intersection analysis.

## Adoption And User-Behavior Analysis

Use when the report must explain whether a product, tool, practice, or category is actually being used.

Questions:

- Who adopted it?
- What workflow changed?
- What alternatives did it replace?
- What friction remains?
- What evidence distinguishes usage from awareness?

## Market And Capital Analysis

Use when price, revenue, valuation, funding, margins, procurement, or market structure matters.

Questions:

- What is the economic claim?
- What data supports it?
- Is the data primary, estimated, or promotional?
- What are the cost, pricing, and distribution implications?
- What would disprove the market story?

## Organization And Talent Analysis

Use when company structure, hiring, layoffs, leadership, talent flow, or operating model is central.

Questions:

- What organization design is being tested?
- What talent flows reveal strategic gravity?
- Which capabilities are being built internally versus acquired or partnered?
- How does organizational change affect product or market outcomes?

## Policy And Legitimacy Analysis

Use when regulation, safety, public trust, geopolitical competition, or institutional legitimacy matters.

Questions:

- Which rules or norms shape the market?
- Who benefits from a legitimacy standard?
- What compliance burden or moat is created?
- Where does public risk perception affect adoption?

## Counter-Case Analysis

Use in every high-stakes report, even if briefly.

Questions:

- What is the strongest alternative explanation?
- Which examples contradict the main thesis?
- Which claims are company PR, investor hope, or media amplification?
- What would make the conclusion wrong?
