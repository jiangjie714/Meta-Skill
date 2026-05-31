# Meta-Skill Project Guidelines

## Project Overview

Meta-Skill is an installable skill for AI coding assistants (Claude Code, Codex, Cursor, OpenCode, Gemini) that discovers, analyzes, translates, and explains all installed skills. It's both a CLI tool and an invocable skill.

## Architecture

- `meta_skill/scanner.py` — Filesystem scanner: finds SKILL.md files, parses frontmatter, deduplicates
- `meta_skill/translator.py` — Localization: locale detection, Chinese/English term dictionaries, search keyword expansion
- `meta_skill/report.py` — Report generator: Markdown and JSON output, skill categorization, marketplace metadata enrichment
- `meta_skill/cli.py` — CLI entry point: argparse interface with --locale, --unique, --app, --search, --format, --output

## Plugin Structure

- `.claude-plugin/plugin.json` — Claude Code plugin manifest
- `.codex-plugin/plugin.json` — Codex plugin manifest  
- `.claude/skills/meta-skill/SKILL.md` — Claude Code skill definition (invocable skill)
- `skills/meta-skill/SKILL.md` — Codex/OpenCode skill definition
- `SKILL.md` — Project-level skill definition (root)

## Installation

- `scripts/install.sh` — One-click installer for all AI tools
- `scripts/uninstall.sh` — Uninstaller

## Key Design Decisions

- **Zero external dependencies**: Pure Python stdlib only
- **YAML frontmatter parsing**: Custom parser (no pyyaml)
- **Chinese search expansion**: Searching "调试" expands to ["调试", "debug", "debugg", "investigate"]
- **Deduplication**: Same skill from different sources is kept; use `--unique` to deduplicate

## Running

```bash
# Direct execution
python3 -m meta_skill.cli --locale zh_CN --unique

# Installed
meta-skill --locale zh_CN --unique --app superpowers
```

## Code Style

- Python 3.9+ compatible
- Type hints on function signatures
- Docstrings on all public functions
- f-strings for formatting
- Keep lines under 120 chars
