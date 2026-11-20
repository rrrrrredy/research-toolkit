# Working on Research Toolkit

Read [CONTRIBUTING](CONTRIBUTING.md) for repository conventions. The user-facing research instructions live in [SKILL.md](SKILL.md).

- Change the source files first. Rebuild the bundled plugin with `python scripts/build_plugin.py` and the published pages with `python scripts/build_site.py`.
- Keep public entry points paired in English and Chinese. The [host inventory](integrations/capabilities.toml) and [public review facts](docs/claims.toml) drive their maintained views.
- Preserve original manuscripts, signed review assignments, receipts and historical findings. Place current interpretation beside its dated evidence.
- Run `make check` or `python scripts/check_project.py` using Python 3.11+ and the dependencies in `requirements-mcp.txt`. See [REVIEW](REVIEW.md) for the sources of current contracts.
