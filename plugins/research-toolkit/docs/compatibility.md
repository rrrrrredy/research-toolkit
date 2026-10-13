# Version and compatibility policy

[English](compatibility.md) | [简体中文](compatibility.zh-CN.md)

Research Toolkit 1.0.0 establishes the public compatibility baseline for the Skill, CLI, MCP server and bundled plugin. It retains v0.2.7 runtime behavior; upgrading from v0.2.7 requires no task-data migration or repeat model evaluation.

## Compatibility within 1.x

- **Documented interfaces:** the CLI actions and seven MCP tools in the [usage guide](usage-modes.md), their documented arguments, configuration variables, response fields and exit-code meanings remain compatible. New optional inputs, tools and response fields may be added; clients should ignore unrecognized optional response fields. Removing or renaming a supported interface, changing an existing field's type or meaning, or adding a required input is a breaking change.
- **Saved work:** supported task directories, saved profile/review choices and versioned records remain readable and usable according to their recorded contract. An upgrade preserves reports, reviews and execution history. Existing freshness and revision rules still apply when task inputs change. A future incompatible data change must provide migration instructions with its major release.
- **Installation:** 1.x retains Python 3.10 support for the CLI and local MCP server, the `research-toolkit` Skill name and the documented package entry points. Raising the minimum Python version or removing a supported entry point is a breaking change. Host applications and model services keep their own compatibility requirements.

Internal Python helpers and exact diagnostic prose may change. Research methods, examples and source material can improve while preserving the public interfaces and saved-work commitments above. A bug fix can reject inputs that the documented contract already disallowed. Changes to assignment, reviewer inputs or acceptance receive targeted revalidation when affected; a version bump alone does not require new model runs.

## Version numbers and updates

Following [Semantic Versioning](https://semver.org/):

| Release | Change |
| --- | --- |
| `1.0.1` | Compatible bug fixes, clarifications and packaging corrections |
| `1.1.0` | Compatible new functionality; deprecated interfaces remain supported throughout 1.x |
| `2.0.0` | Incompatible changes to the commitments above, with the affected interfaces and migration steps documented |

Update the complete package and retain local task data. Root `VERSION`, both plugin manifests, the packaged version, bilingual changelogs and release notes must agree. Run the existing release checks and CI before publishing. Published tags and historical evaluation records retain their original version identities. The `agent-trajectory-data` repository follows its own release sequence; Toolkit 1.0.0 does not renumber its datasets.
