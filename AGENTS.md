# Meta-Skill Project Guidelines

## Project Overview

Meta-Skill is an installable skill for AI coding assistants (Claude Code, Codex, Cursor, OpenCode, Gemini) that discovers, analyzes, translates, and explains all installed skills. It uses a **cache-first architecture** — the AI reads `~/.meta-skill/cache.json` directly instead of running shell commands for each query.

## Architecture

- `meta_skill/scanner.py` — Filesystem scanner: finds SKILL.md files, parses frontmatter, deduplicates
- `meta_skill/translator.py` — Localization: locale detection, Chinese/English term dictionaries, search keyword expansion
- `meta_skill/report.py` — Report generator: Markdown and JSON output, skill categorization, marketplace metadata enrichment
- `meta_skill/cache.py` — Cache manager: reads/writes `~/.meta-skill/cache.json`, cache-first query functions
- `meta_skill/cli.py` — CLI entry point: argparse interface with --locale, --unique, --app, --search, --format, --output, positional args

## Cache-First Design

The SKILL.md instructs AI assistants to:
1. Read `~/.meta-skill/cache.json` directly (file read, NOT shell command)
2. Parse JSON and present results
3. Only run `ms --refresh` when cache is missing/stale

This makes responses instant (~0.05s) vs filesystem scan (~1.4s).

## Plugin Structure

- `.claude-plugin/plugin.json` — Claude Code plugin manifest
- `.codex-plugin/plugin.json` — Codex plugin manifest
- `skills/meta-skill/SKILL.md` — Skill definition (Codex/OpenCode)
- `SKILL.md` — Project-level skill definition

## Installation

- `scripts/install.sh` — One-click installer for all AI tools
- `scripts/uninstall.sh` — Uninstaller
- `scripts/ms` — CLI shortcut command

## Key Design Decisions

- **Cache-first**: AI reads `~/.meta-skill/cache.json` directly, no shell commands for queries
- **Zero external dependencies**: Pure Python stdlib only
- **YAML frontmatter parsing**: Custom parser (no pyyaml)
- **Chinese search expansion**: Searching "调试" expands to ["调试", "debug", "debugg", "investigate"]
- **Deduplication**: Same skill from different sources is kept; use `--unique` to deduplicate

## Running

```bash
# Quick query (from cache, ~0.05s)
ms                    # Show summary
ms gstack             # Show GStack skills
ms search 调试        # Search skills

# Force re-scan
ms --refresh

# Direct Python execution
python3 -m meta_skill.cli --locale zh_CN --unique
```

## Code Style

- Python 3.9+ compatible
- Type hints on function signatures
- Docstrings on all public functions
- f-strings for formatting
- Keep lines under 120 chars
