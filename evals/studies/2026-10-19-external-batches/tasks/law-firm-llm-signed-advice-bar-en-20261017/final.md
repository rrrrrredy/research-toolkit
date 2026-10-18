# Evidence Bar for LLM Use on Partner-Signed Advice (Through 2027)

**Audience:** Law-firm general counsel / professional-responsibility lead and practice-innovation partners  
**Materials:** Synthetic source pack S1–S4 only (disclosed). Not legal advice. No live web. No independent review was performed.  
**Question:** Before a mid-market law firm allows associates to use third-party LLM tools on client contract review and draft advice memos, what evidence bar and operational/disclosure controls are required so that tool outputs can support partner-signed advice or client disclosure duties through 2027—and when must the firm treat “AI legal research” claims as insufficient for signed work product?

---

## 1. Judgment in brief

Treat **“AI legal research” vendor marketing as insufficient** for partner-signed advice. On the evidence in this pack, a mid-market firm should operate **two work-product tiers**:

1. **Research assist / clause spotting** — allowed with mandatory verification checklists, matter segregation, and human ownership of every citation and client fact.  
2. **Partner-signed advice / client advice memos** — allowed only when a human attorney owns the analysis, a **source-trace / citation log** exists for sign-off, confidentiality controls meet enterprise (not consumer) standards, and disclosure norms the firm adopts are actually applied.

Silent AI use on signed work, repeated hallucinated citations, or cross-matter leakage are **kill criteria** for production use on client matters (S3). Questionnaire answers from legal-tech vendors do not clear the bar by themselves (S4); firm operational controls remain decisive.

All sources are synthetic. This memo is a professional-responsibility planning document for internal governance discussion, not a bar opinion and not legal advice.

## 2. Starting point: proposed use and weak controls

The firm GC memo (S1) describes the proposed use: associates may use a third-party LLM for (a) clause spotting on NDAs/MSAs and (b) first drafts of advice memos. Partners want clarity on when outputs can support **partner-signed** advice versus research assist only.

Current controls are characterized as weak (S1):

- Optional disclosure footnote “AI-assisted drafting” — inconsistently applied.  
- No mandatory citation/source-trace log for model suggestions.  
- Privilege training mentions cloud LLM risk once in onboarding.

That gap—optional disclosure, no source-trace, one-time privilege mention—is the problem the evidence bar must close. The open question posed in S1 is exactly this memo’s charge: what evidence bar (human accountability, source-trace, confidentiality) is required through 2027 before treating tool output as fit for signed work product?

## 3. What the associate pilot actually showed

A 90-day associate pilot on **40 low/medium-risk matters** (S2, synthetic) recorded failure modes that map directly to signed-work risk:

- **Hallucinated authority:** In 6 matters, the model cited cases/statutes that did not exist or were wrong jurisdiction; in **2** of those, the error nearly reached partner signature before catch.  
- **Cross-matter / confidentiality near miss:** In 9 matters, the model merged client facts from prior chat context (same associate account) into a different client memo draft.  
- **Positive signal:** Clause-spotting recall improved on boilerplate NDAs **when the associate verified every hit**.

The pilot lead’s practice note (S2) recommends **tiering**: research assist OK with a verification checklist; signed opinion / client advice requires human-owned analysis plus a citation log; **silent AI use banned**.

These rates are pilot-local (n=40, low/medium risk only). They do not establish firm-wide base rates. They are enough to reject a policy that treats LLM drafts as casually promotable to partner signature without verification infrastructure.

### 3.1 Implication for the evidence bar

Two near-misses to partner signature on invented or wrong-jurisdiction authority, plus nine confidentiality near misses from shared chat context, show that **human review without structured logs is not a reliable last gate**. Partners need a reproducible record of what the model suggested, what the associate verified, and what authorities/facts the partner is signing against—not a vague assurance that “someone looked at it.”

## 4. Work-product tiers (required design)

Outside ethics counsel themes (S3, synthetic; not a bar opinion) state: **“AI legal research” marketing claims ≠ evidence that outputs are fit for partner-signed advice.** That theme should be firm policy language, not only ethics folklore.

### Tier A — Research assist / clause spotting

**Allowed when:**

- Matter is within approved risk classes (pilot used low/medium only; expand only with explicit PR approval).  
- Associate runs a **verification checklist** on every model hit (S2 positive case depended on verifying every hit).  
- Tooling enforces **matter segregation** (see §5); shared personal accounts that retain cross-matter context are out of policy.  
- Output is labeled internally as assist; it is not pasted into a client-facing advice memo without Tier B controls.

**Not allowed:** Treating vendor “AI legal research” branding as a substitute for verification (S3).

### Tier B — Partner-signed advice / client advice memos

**Allowed only when all of the following hold:**

1. **Human-owned analysis:** A responsible attorney (typically the signing partner or a clear designee) owns the legal analysis and factual framing; the model is a drafting/research aid, not the author of record (S2 practice note; S3 accountability theme).  
2. **Source-trace / citation log:** Mandatory log of authorities and material client facts the model proposed, with associate verification status and partner acknowledgment at sign-off (gap called out in S1; recommended in S2; vendor side shifts verification to the firm in S4).  
3. **Disclosure policy actually applied:** If firm policy requires client disclosure when AI materially shaped advice, the disclosure must be consistent—not optional footnotes applied inconsistently (S1 weakness; S3 disclosure theme).  
4. **Confidentiality / privilege narrative:** Use enterprise contracts, DLP, and matter segregation; consumer or weakly governed SaaS endpoints are treated as incompatible with Tier B (S3).  
5. **No silent AI:** Silent use on signed work is banned (S2; S3 kill criteria).

If any of (1)–(5) cannot be evidenced for a matter, the firm must treat the tool output as **insufficient for signed work product** and keep the matter at Tier A or unaided work.

## 5. Operational and disclosure controls (through 2027)

### 5.1 Human accountability

Accountability means a named attorney owns the advice, not that a model “helped.” S3 frames work-product tiers around that distinction. Operationalize it as: partner signature certifies human analysis; AI assistance, if any, is logged.

### 5.2 Source-trace evidence

S1 notes there is currently no mandatory citation/source-trace log. S2 makes that log part of the signed-opinion tier. S4 shows vendors may answer that the model “may invent; user must verify,” and may offer only short-lived admin export of prompts/outputs—not an immutable audit for partner sign-off. Therefore the **firm must keep its own durable citation/verification log** tied to the matter file; do not rely on vendor export windows as the record of professional judgment.

### 5.3 Privilege / confidentiality failure modes

S2’s nine near misses (prior chat context bleeding into another client’s memo) are the concrete failure mode. S3 lists consumer or weakly governed SaaS LLM endpoints as jeopardizing privilege narratives; enterprise contracts, DLP, and matter segregation are minimum discussion points. Controls should include:

- Per-matter workspaces or equivalent isolation (logical tenancy alone is weak—see S4).  
- Ban on consumer LLM endpoints for client confidential information.  
- DLP and retention settings aligned with matter file policy.  
- Training that goes beyond a single onboarding mention (S1 gap).

### 5.4 Client disclosure duties

S3 notes clients may need to know when AI materially shaped advice; firm policies vary; silent use is a risk theme through 2027. This pack does not prescribe a single jurisdiction’s disclosure rule. It does require the firm to **pick a disclosure standard, write it down, and apply it consistently**—replacing S1’s optional, inconsistent footnote practice. Where policy requires disclosure for Tier B matters, absence of disclosure is a policy failure, not a wording preference.

## 6. Why vendor questionnaires do not clear the bar

Synthetic vendor security questionnaire answers (S4) illustrate the gap:

| Topic | Vendor answer | Firm risk note |
| --- | --- | --- |
| Training on client data | “Not by default” | Default ≠ contractually barred |
| Matter isolation | “Logical tenancy” | No cryptographic matter keys |
| Citation provenance | “Model may invent; user must verify” | Shifts all accountability to firm |
| Export of prompts/outputs | “Admin export within 30 days” | No immutable audit for partner sign-off |

**Implication (S4):** Questionnaire alone does not clear the bar for signed advice; operational controls inside the firm remain decisive.

Procurement can still use questionnaires to **exclude** clearly unfit vendors (e.g., no contractual training ban, consumer-grade tenancy). Clearing a questionnaire is not affirmative proof that Tier B use is safe.

## 7. Kill criteria (suspend production use on client matters)

From ethics counsel themes (S3) and reinforced by pilot events (S2):

1. **Undisclosed AI on signed work** — suspend Tier B (and investigate Tier A labeling failures).  
2. **Repeated hallucinated citations** — especially any that approach partner signature (S2: 6 matters; 2 near signature).  
3. **Cross-matter leakage** — including chat-context bleed (S2: 9 matters).  

On kill, stop production use on client matters until root cause, control redesign, and PR sign-off to resume. Do not “train harder” as the sole fix when tooling allows cross-matter context or provides no citation log.

## 8. Counter-evidence and uncertainties

- Pilot is **n=40, low/medium risk only** (S2); high-stakes litigation or regulated advice may need a higher bar or a ban.  
- Ethics extract is **not a bar opinion** (S3).  
- Vendor answers are synthetic and vendor-favorable on wording (“not by default”) (S4).  
- Disclosure duties vary by jurisdiction and client contract; this pack does not resolve conflicts of law.  
- Clause-spotting **can** help when every hit is verified (S2)—do not ban Tier A solely because Tier B is strict.  
- No independent review; all materials synthetic; not legal advice.

## 9. Recommended policy package (decision-ready)

1. Adopt **Tier A / Tier B** definitions above in writing.  
2. Ban silent AI on any client work product that can become signed advice.  
3. Require matter-segregated enterprise LLM (or equivalent) before any client confidential use; reject consumer endpoints for Tier A or B.  
4. Mandate citation/source-trace logs for Tier B; retain them with the matter file beyond vendor export windows.  
5. Replace optional AI footnotes with a firm disclosure standard and audit for consistency.  
6. Treat vendor “AI legal research” claims as marketing, not evidence of fitness for signed work (S3).  
7. Encode kill criteria; empower PR/GC to suspend production use.  
8. Re-run a bounded pilot before expanding beyond low/medium-risk matter classes.

## 10. Limitations

Synthetic sources S1–S4 only. Not legal advice; not a bar opinion; no independent review. Pilot statistics are not firm-wide rates. Questionnaire rows are illustrative. Through-2027 horizon assumes continued third-party LLM use pressure; if the firm bans cloud LLMs entirely, Tier design still helps for any remaining assistive tools.

---

### Source ledger (synthetic)

| ID | Title (short) | Type |
| --- | --- | --- |
| S1 | Mid-market firm GC memo — LLM on contract review & advice memos (2026-05) | synthetic GC memo |
| S2 | Associate pilot log — contract review LLM (90 days, n=40) | synthetic pilot log |
| S3 | Outside ethics counsel Q&A extract (2026-06) | synthetic ethics extract |
| S4 | Vendor security questionnaire answers (legal-tech LLM) | synthetic vendor Q&A |
