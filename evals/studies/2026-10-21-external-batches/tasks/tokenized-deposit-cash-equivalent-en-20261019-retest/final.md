# Tokenized deposit pilots and cash-equivalent treatment for working-capital reporting

**Audience:** Corporate treasury and external auditor liaison  
**Evidence standard:** Synthetic source pack only (S1–S4). All materials are fictional test evidence. No live web research. No independent review was performed. This memo does not constitute legal, accounting, or audit advice.

## 1. Judgment

Corporate treasuries should **not** treat the Bank-T tokenized deposit pilot as an operational cash equivalent for working-capital (WC) reporting or covenant metrics until four evidence layers are closed together: (1) a written legal opinion that the instrument meets the entity’s cash-equivalent definition under applicable GAAP/IFRS; (2) redeemability evidence under stress—not only happy-path banking-hours redemption; (3) dual-control mint/burn keys plus daily bank-core to general-ledger reconciliation that survives timing gaps between chain credit and fiat movement; and (4) reporting labels and disclosure that refuse “unrestricted cash” presentation while the program remains pilot-only. On the synthetic pack alone, marketing language that calls the token an “on-chain cash equivalent for WC reporting” overstates what the ops design supports. Until those bars are met, classify and disclose the balance as a **restricted digital deposit claim pilot**.

## 2. What the pilot actually is

The Bank-T brief describes a permissioned token that represents a demand-deposit claim at the bank, redeemable one-to-one to fiat during banking hours (S1). The legal claim remains a deposit subject to Bank-T’s insolvency hierarchy. The instrument is explicitly **not** a stablecoin float. Mint and burn go through the bank API; the chain is a messaging layer rather than a freestanding settlement rail that moves fiat by itself.

Two operational facts matter more than the brand language. First, a weekend chain transfer among subsidiaries does **not** move fiat until the next business window, creating an intraday WC illusion risk if dashboards treat chain balances as immediately available cash (S1). Second, the treasury marketing one-pager already used “on-chain cash equivalent for WC reporting,” which collides with the banking-hours fiat leg and with the auditor liaison evidence list (S1, S2). Readers should separate the economic claim (deposit at Bank-T) from the reporting claim (cash equivalent for WC). The first may be true while the second remains unsupported.

## 3. Evidence bar before cash-equivalent treatment

The external auditor liaison notes set a concrete pre-classification bar (S2). Treasuries should treat each item as a hard gate, not a soft preference:

1. **Legal opinion.** A written opinion that the instrument meets the cash-equivalent definition under the GAAP/IFRS framework the entity actually applies—not a slide asserting “cash-like.” A liaison Q&A is not that opinion (S2, S4).
2. **Redeemability under stress.** Same-day or next-day fiat access evidence when the bank core lags, when windows are closed, and when redeem demand spikes—not only the happy-path API path described in the pilot brief (S2).
3. **Controls.** Dual control on mint/burn keys and daily reconciliation of bank balances to the GL, with explicit handling of chain-vs-core timing differences (S2, S3).
4. **Segregation.** Tokens must not be transferable to unrestricted wallets without a bank gate; otherwise the deposit-claim story and the transferable-crypto story blur (S2).
5. **Disclosure.** If the program is pilot-only, do not present token balances as unrestricted cash in WC metrics used for covenants (S2).

The red flag already observed in the liaison notes—a pilot dashboard showing “available cash” including tokens still pending the fiat settlement window—is exactly the failure mode the bar is meant to catch (S2). Closing one gate (for example, dual control) while leaving redeemability and legal classification open is not enough to change the reporting stance.

## 4. Control failures already logged

A ninety-day synthetic incident log shows three failures that map directly onto the evidence bar (S3):

- **Incident 1.** The chain showed a credit while the bank core delayed seven hours. A WC report nearly filed with inflated cash; daily reconciliation caught it. This is empirical proof that chain state is not fiat availability for reporting cutoffs.
- **Incident 2.** Vendor UI labeled the token balance “Cash (on-chain).” Compliance forced a relabel to “Deposit claim token (pilot).” Labeling is a control, not cosmetics: auditors and covenant lenders read what the system prints.
- **Incident 3.** Weekend peer transfers among subsidiaries created reporting asymmetry versus banking-day cash, reproducing the intraday illusion risk flagged in the pilot brief.

Ops conclusion in the same log: treat the program as a **restricted digital deposit claim pilot** until redeemability, reconciliation, and a legal memo are clear; do **not** treat it as an operational cash equivalent for covenant WC (S3). That conclusion is an internal judgment on synthetic incidents, but it is consistent with the auditor liaison bar and with the counter-claim FAQ.

## 5. Counter-claims to reject for this pilot

The peer FAQ lists three marketing or informal assertions that fail against the pack (S4):

- **“Atomic settlement removes timing risk.”** False here because the fiat leg remains banking-hours. Chain messaging can look atomic while cash for WC purposes is still waiting on the bank window (S1, S4).
- **“Bankruptcy remote.”** Not supported. The claim sits in the bank’s insolvency hierarchy as a deposit claim (S1, S4). Calling the token bankruptcy-remote confuses deposit risk with bankruptcy-remote SPV structures that this brief does not describe.
- **“Auditor already OK’d.”** Only a liaison Q&A occurred. There is no clean opinion on cash-equivalent classification (S2, S4). Treating liaison questions as approval is a process failure.

These rejections are specific to the Bank-T pilot design in the synthetic pack. They are not a blanket statement about every tokenized deposit product in the market—especially products that this pack does not describe.

## 6. Disclosure stance for treasury and auditor liaison

Until the evidence bar is closed, recommended disclosure and internal presentation:

- **Balance sheet / WC pack:** Present token balances as restricted deposit-claim pilot assets (or an equivalent restricted caption the entity’s policy allows), with a footnote that redeemability is banking-hours, that chain credit can lead fiat settlement, and that the program is pilot-scoped.
- **Covenant packs:** Exclude pilot token balances from unrestricted cash and from WC metrics used for lender tests unless lenders have consented in writing to a defined inclusion rule (S2, S4).
- **Dashboards and vendor UI:** Forbid “Cash (on-chain)” and similar labels; require “Deposit claim token (pilot)” or stronger restricted language (S3).
- **Management commentary:** Do not cite marketing “cash equivalent” language as accounting classification. Cite the legal memo when it exists; until then, state that classification remains open.

This stance is deliberately conservative relative to vendor marketing. The cost of over-including pilot tokens in WC is a restatement or covenant dispute; the cost of under-including is temporary optics that can be revised when evidence arrives.

## 7. When the judgment could change

The FAQ’s change triggers are the right checklist for a future reclassification discussion (S4):

1. Independent legal memo affirming cash-equivalent classification under the entity’s framework.
2. Two consecutive quarters of clean daily bank–GL reconciliation under stress drills (not only quiet periods).
3. UI and reporting labels aligned with the restricted-or-reclassified reality—no “available cash” pending fiat.
4. Covenant lender consent if WC metrics change because of inclusion.

All four should be treated as joint conditions. A legal memo without stress redeemability, or clean recon without lender consent when covenants are affected, leaves a residual reporting and relationship risk. Treasuries should also keep a kill switch: if a new incident class appears (for example, transferable tokens escaping the bank gate, or sustained core delays beyond the stress envelope), freeze reclassification and revert to restricted pilot presentation even if a prior memo exists—until the memo and drills are updated.

## 8. Decision framework for the next ninety days

| Decision | Do now | Do not do |
| --- | --- | --- |
| Classification | Restricted digital deposit claim pilot | Cash equivalent for operational WC / covenants |
| Legal | Commission opinion keyed to GAAP/IFRS cash-equivalent tests | Treat liaison Q&A as approval |
| Controls | Dual control; daily recon with chain-vs-core timing rules; stress redeem drills | Rely on happy-path API demos |
| Disclosure | Restricted captions; forbid cash-like UI labels | Unrestricted cash in WC dashboards |
| Vendors | Contract for label control and recon data feeds | Accept “atomic / bankruptcy-remote / auditor OK” marketing |

## 9. Limitations

All four sources are **synthetic** test materials (S1–S4). They do not represent a real bank, auditor firm, or treasury incident series. No live market scan, no survey of GAAP practice across jurisdictions, and **no independent review** were performed under this Lite profile. Incident counts (three events in ninety days) are illustrative, not a measured rate. Change triggers in S4 are proposed conditions, not observed outcomes. Readers must not treat this memo as authorization to adopt or reject any live product.

## Source ledger (synthetic)

| ID | Title | Role |
| --- | --- | --- |
| S1 | Bank pilot brief — tokenized deposit receipt (2026-05) | Instrument design; marketing overclaim; weekend fiat lag |
| S2 | External auditor liaison questions (2026-07) | Evidence bar; dashboard red flag |
| S3 | Treasury control incident log (90 days) | Timing, labeling, asymmetry incidents; ops conclusion |
| S4 | Counter-claims and peer FAQ (2026-06) | Rejected claims; change triggers |

---

*Lite original-condition retest under Research Toolkit 1.3.1. Tool checklist pass is not semantic certification.*
