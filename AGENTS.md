# Meta-Skill Project Guidelines

## Project Overview

Meta-Skill is a CLI tool that discovers, analyzes, translates, and explains all installed AI coding assistant skills across multiple tools (Claude Code, Codex, Cursor, OpenCode, Gemini, Trae, CherryStudio).

## Architecture

- `meta_skill/scanner.py` — Filesystem scanner: finds SKILL.md files across tools, parses frontmatter, deduplicates
- `meta_skill/translator.py` — Localization: locale detection, Chinese/English term dictionaries, search keyword expansion
- `meta_skill/report.py` — Report generator: Markdown and JSON output, skill categorization, marketplace metadata enrichment
- `meta_skill/cli.py` — CLI entry point: argparse-based interface with --locale, --unique, --app, --search, --format, --output

## Key Design Decisions

- **Zero external dependencies**: Pure Python stdlib only (no requests, pyyaml, etc.)
- **YAML frontmatter parsing**: Custom parser in scanner.py (no pyyaml dependency)
- **Deduplication**: Same skill from different sources is kept; use `--unique` to deduplicate by name
- **Chinese search expansion**: Searching "调试" automatically expands to ["调试", "debug", "debugg", "investigate"]

## Running

```bash
# Direct execution
python3 -m meta_skill.cli --locale zh_CN --unique

# Installed
meta-skill --locale zh_CN --unique --app superpowers
```

## Testing

No test framework configured yet. Manual testing via CLI execution.

## Code Style

- Python 3.9+ compatible
- Type hints on function signatures
- Docstrings on all public functions
- f-strings for formatting
- Keep lines under 120 chars
