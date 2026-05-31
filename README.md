# Meta-Skill 🤖

> AI 编程助手技能发现与分析工具 / AI Coding Assistant Skills Discovery & Analysis Tool

**Meta-Skill** scans your system for installed AI coding assistant skills (Claude Code, Codex, Cursor, OpenCode, Gemini, Trae, etc.), analyzes what each skill does, groups them by source application, and generates a **localized report** so you can understand and use your skills effectively.

## Why?

If you use AI coding assistants, you probably have dozens of installed skills — but:
- They're all in English, and you don't know what they do
- You don't know which skills belong to which plugin/app (e.g., Superpowers, GStack, ECC)
- You don't know **when** to use which skill
- It's hard to discover new skills across different tools

**Meta-Skill** solves this by:
1. 🔍 **Scanning** all skill directories across multiple AI tools
2. 📋 **Parsing** SKILL.md frontmatter for metadata (name, description, version)
3. 🏷️ **Grouping** skills by their source application/plugin
4. 🌍 **Translating** descriptions to your system locale (中文/日本語/etc.)
5. 📖 **Generating** a readable report with practical usage scenarios

## Quick Start

```bash
# Clone and run directly (no installation needed)
cd Meta-Skill
python3 -m meta_skill.cli

# Auto-detects locale (zh_CN on Chinese systems) and scans all skills
```

## Installation

```bash
cd Meta-Skill
pip install -e .

# Then use anywhere:
meta-skill
```

## Usage

```bash
# Scan all skills (auto-detect locale)
meta-skill

# Output in Simplified Chinese
meta-skill --locale zh_CN

# Output in English
meta-skill --locale en_US

# Deduplicate by skill name (same skill from multiple sources)
meta-skill --unique

# JSON format for programmatic use
meta-skill --format json

# Save to file
meta-skill --output skills-report.md

# Filter by application
meta-skill --app superpowers

# Search by keyword (supports Chinese!)
meta-skill --search 调试
meta-skill --search tdd

# Combine options
meta-skill --locale zh_CN --unique --app superpowers --output superpowers-zh.md
```

### As a Python Library

```python
from meta_skill.scanner import scan_all_skills
from meta_skill.report import generate_markdown_report, generate_json_report

# Scan all skills
skills = scan_all_skills()

# Generate report (auto-detect locale)
report = generate_markdown_report(skills, locale="zh_CN")
print(report)

# JSON for programmatic use
json_data = generate_json_report(skills, locale="zh_CN")
```

## What It Scans

| Tool | Scan Path |
|------|-----------|
| Claude Code | `~/.claude/skills/` |
| Claude Code Plugins | `~/.claude/plugins/marketplaces/*/` |
| Cursor | `~/.cursor/skills-cursor/` |
| OpenCode | `~/.config/opencode/skills/` |
| Gemini | `~/.gemini/antigravity/skills/` |
| Trae | `~/.trae-cn/builtin/` |
| CherryStudio | `~/Library/Application Support/CherryStudio/Data/Skills/` |
| Project-level | `{project}/.claude/skills/`, `{project}/skills/` |

## Example Output

```markdown
# 🤖 AI 编程助手技能全景图

> 自动检测系统语言：**简体中文** | 扫描时间：2026-06-01 01:30
> 共发现 **251** 个技能，来自 **13** 个来源

## 📦 Superpowers 超能力集

| # | 技能名称 | 中文名称 | 说明 | 适用场景 |
|---|---------|---------|------|---------|
| 1 | `test-driven-development` | 测试驱动开发 | Use when implementing any feature or bugfix... | 当你在编写新功能或修复 Bug 时，先写测试用例 |
| 2 | `systematic-debugging` | 系统化调试 | Use when encountering any bug, test failure... | 当你遇到 Bug 或测试失败时 |
| 3 | `brainstorming` | 头脑风暴 | Use this before any creative work... | 当你开始新项目或需要创意发散时 |
```

## Features

- **Multi-tool scanning**: Discovers skills from Claude Code, Codex, Cursor, OpenCode, Gemini, Trae, CherryStudio
- **Auto locale detection**: Detects your system language (macOS `AppleLocale`, `LANG`, `LC_ALL`)
- **Chinese translation**: Built-in dictionary with 100+ terms and usage scenarios
- **Deduplication**: `--unique` flag removes duplicate skills across sources
- **CJK search**: Search `调试` to find `debug`, `debugging`, `investigate` skills
- **Multiple formats**: Markdown reports and JSON for programmatic use
- **Marketplace metadata**: Enriches skill info from plugin manifests
- **Zero dependencies**: Pure Python, no external packages needed

## Supported Locales

- **zh_CN / zh_TW** — Full Chinese translation with 100+ term dictionary
- **en_US** — English (default)
- Other locales fall back to English with partial translation

## Project Structure

```
Meta-Skill/
├── SKILL.md                    # Skill definition (installable as a skill)
├── README.md
├── pyproject.toml
└── meta_skill/
    ├── __init__.py
    ├── scanner.py               # File system scanner and SKILL.md parser
    ├── translator.py            # Translation/localization module
    ├── report.py                # Markdown and JSON report generator
    └── cli.py                   # Command-line interface
```

## License

MIT
