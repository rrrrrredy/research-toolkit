# Version and compatibility policy

[English](compatibility.md) | [简体中文](compatibility.zh-CN.md)

## Current review contract

New full-report tasks use review contract 3. They group the seven content perspectives across three independent contexts, add domain specialists where needed and keep audit and final checking independent. Delivery binds the current report and the independent results that establish completion. Saved contract 2 plans retain their own assignments and completion rules.

## The v2 completion contract

v2 kept one research entry and the existing Skill, CLI, MCP and plugin forms. Its completion contract required separate independent content perspectives, independent audit and final acceptance. Author self-review or a merged-perspective result cannot satisfy a saved v2 plan. That change to the earlier completion rules warranted a major version.

The public operation names and saved source, claim, requirement and artifact formats are reused. Native-agent assignments and handoffs extend those operations. Python 3.10+, the `research-toolkit` Skill name and package entry points remain supported.

## Continue saved work

Preserve the task directory, original reports, review replies, input snapshots and receipts before continuing. Read current work through `status`; reuse sources, analysis, stable IDs and still-effective requirements. Keep earlier completed artifacts intact and save the continued report separately.

An unchanged historical completion remains inspectable under its recorded contract. When continuing research toward a new delivery, use the applicable review plan and complete the independent roles and substantive work still missing. Do not create a new research task merely to copy all records, relabel author checks as independent, or fabricate missing executions.

Research uses one shared entry across the supported interfaces. Start tasks and request guidance without the old CLI `--profile` or JSON/MCP `profile` argument. Saved source, claim, requirement and artifact records remain readable. Old author checklists remain original files, not an executable completion route or approval of a new delivery. Use the original release to inspect its historical completion behavior; continue current work through independent review, audit and final checking.

## Public compatibility

Documented CLI/MCP operation names, arguments, response fields and exit meanings are the public interface. New optional fields may be added; clients should tolerate unfamiliar optional response fields. Removing a supported entry, changing a field's type/meaning or tightening a promised completion contract is a breaking change.

Internal helpers and diagnostic wording may change. Engineering fixes may reject input already forbidden by the documented contract. Input changes retain their source/version consequences; updating the installed version alone does not rewrite completed research or rerun historical studies.

## Version numbers and updates

Following [Semantic Versioning](https://semver.org/):

| Release type | Use |
| --- | --- |
| Patch, for example `2.0.1` | Compatible fixes, clarifications and packaging corrections. |
| Minor, for example `2.1.0` | Compatible additional functionality. |
| Major, for example `2.0.0` | A changed public compatibility promise, with affected behavior and continuation instructions documented. |

Update the complete installed package and retain task data. Root `VERSION`, plugin manifests, packaged version and bilingual release material agree when a version is published. Tags and historical evaluation records retain their original identities. Dataset repositories keep their own version sequence.

The original 1.x compatibility baseline began at 1.0.0 and preserved v0.2.7 task behavior. Existing 1.x releases remain available under their original tags; this page does not alter what their recorded runs did.
