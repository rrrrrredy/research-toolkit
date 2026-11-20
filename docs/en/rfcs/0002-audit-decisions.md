# How duplicate findings receive one decision

[Design decisions](README.md) · [简体中文](../../zh/rfcs/0002-audit-decisions.md)

Four reviewers may find the same omission or make the same mistake about a date. Toolkit retains each finding and its location. An independent auditor checks the sources and decides which findings are equivalent. One decision, reason and source cover the group while preserving every original finding.

The scaffold fills identities, versions and required fields. The Agent supplies the judgments. The final checker reads the revised artifact independently. A material dispute can receive a separate evidence check. A passing final check completes delivery.

- [Audit and final review](../../review-completion.md)
- [Four incorrect objections and the original decision](../../case-study/v3-review/control/originals/audit.json)
