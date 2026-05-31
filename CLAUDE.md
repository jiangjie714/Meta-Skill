# Meta-Skill — AI Coding Assistant Skills Discovery & Analysis

This project is Meta-Skill: a tool that discovers, analyzes, translates, and explains all installed AI coding assistant skills.

## Quick Reference

- **Scan all skills**: `ms --refresh` or `python3 -m meta_skill.cli --locale zh_CN --unique`
- **From cache (fast)**: `ms` or `python3 -m meta_skill.cli`
- **Search skills**: `ms search 调试` or `python3 -m meta_skill.cli --search debug`
- **Filter by app**: `ms gstack` or `python3 -m meta_skill.cli --app gstack`
- **JSON output**: `ms json --scan` or `python3 -m meta_skill.cli --format json --scan`
- **Save report**: `ms -o report.md --scan`

## Architecture

- `meta_skill/scanner.py` — Filesystem scanner, SKILL.md parser, deduplication
- `meta_skill/translator.py` — Locale detection, Chinese dictionary, keyword expansion
- `meta_skill/report.py` — Markdown/JSON report generator, category classification
- `meta_skill/cache.py` — Cache manager (reads/writes `~/.meta-skill/cache.json`)
- `meta_skill/cli.py` — CLI entry point with argparse, cache-first logic

## Cache-First Design

**IMPORTANT**: This skill uses a cache-first approach. The SKILL.md instructs AI assistants to:

1. Read `~/.meta-skill/cache.json` directly (file read, NOT shell command)
2. Parse JSON and present results based on user query
3. Only run `ms --refresh` when cache is missing, stale, or user requests refresh

This makes responses instant (~0.05s) vs filesystem scan (~1.4s).

## Development

Zero external dependencies. Pure Python stdlib. Python 3.9+.
