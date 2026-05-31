# Meta-Skill — AI Coding Assistant Skills Discovery & Analysis

This project is Meta-Skill: a tool that discovers, analyzes, translates, and explains all installed AI coding assistant skills.

## Quick Reference

- **Scan all skills**: `python3 -m meta_skill.cli --locale zh_CN --unique`
- **Search skills**: `python3 -m meta_skill.cli --locale zh_CN --unique --search <keyword>`
- **Filter by app**: `python3 -m meta_skill.cli --locale zh_CN --unique --app <app-name>`
- **JSON output**: `python3 -m meta_skill.cli --locale zh_CN --unique --format json`
- **Save report**: `python3 -m meta_skill.cli --locale zh_CN --unique --output report.md`

## Architecture

- `meta_skill/scanner.py` — Filesystem scanner, SKILL.md parser, deduplication
- `meta_skill/translator.py` — Locale detection, Chinese dictionary, keyword expansion
- `meta_skill/report.py` — Markdown/JSON report generator, category classification
- `meta_skill/cli.py` — CLI entry point with argparse

## Development

Zero external dependencies. Pure Python stdlib. Python 3.9+.
