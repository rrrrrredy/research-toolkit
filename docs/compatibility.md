# Version and compatibility policy

[English](compatibility.md) | [简体中文](compatibility.zh-CN.md)

## The v2 completion contract

v2 keeps one research entry and the existing Skill, CLI, MCP and plugin forms. The material change is the completion contract: separate independent content perspectives, independent audit and final acceptance are required. Author self-review or a merged-perspective result cannot satisfy it. That changes earlier completion behavior and warrants a major version.

The public operation names and saved source, claim, requirement and artifact formats are reused. Native-host assignments and handoffs extend those operations. Python 3.10+, the `research-toolkit` Skill name and package entry points remain supported.

## Continue saved work

Preserve the task directory, original reports, review replies, input snapshots and receipts before continuing. Read current work through `status`; reuse sources, analysis, stable IDs and still-effective requirements. Keep earlier completed artifacts intact and save the continued report separately.

An unchanged historical completion remains inspectable under the contract it used. It is not retrospectively accepted under v2. When continuing research toward a new delivery, prepare the current review and complete the independent roles and substantive work still missing. Do not create a new research task merely to copy all records, relabel author checks as independent, or fabricate missing executions.

Historical `lite`/`full` profile values and previous response fields remain readable compatibility data. New work has one entry; a legacy parameter cannot select a lighter completion contract. Old request forms that no longer fulfill completion receive an explicit explanation rather than silently passing or deleting old data.

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
