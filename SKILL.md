---
name: meta-skill
description: "发现、分析、翻译和解释系统中所有已安装的 AI 编程助手技能。当用户想了解有哪些技能、技能的用途、何时使用某个技能时调用。/ Discover, analyze, translate, and explain all installed AI coding assistant skills. Use when users want to understand available skills, what they do, and when to use them."
---

# Meta-Skill: AI 编程助手技能发现与分析工具

扫描系统中所有 AI 编程助手（Claude Code、Codex、Cursor、OpenCode、Gemini 等）的技能，按来源分组，翻译为本地语言，并生成可读报告。

## 何时使用

当用户想：
- 了解系统中有哪些技能
- 某个应用/插件包含哪些技能（如 Superpowers 有哪些技能）
- 某个技能是做什么的
- 什么时候应该调用哪个技能
- 用中文了解技能说明
- 搜索特定领域的技能（如"调试""测试""前端"）

## 使用方法

```bash
# 扫描所有技能（自动检测系统语言）
python3 /Users/jiejiang/Desktop/dev/Claude/Meta-Skill/meta_skill/cli.py

# 使用简体中文输出
python3 /Users/jiejiang/Desktop/dev/Claude/Meta-Skill/meta_skill/cli.py --locale zh_CN

# 去重（同一技能只保留一条）
python3 /Users/jiejiang/Desktop/dev/Claude/Meta-Skill/meta_skill/cli.py --unique

# 搜索技能（支持中文关键词！）
python3 /Users/jiejiang/Desktop/dev/Claude/Meta-Skill/meta_skill/cli.py --search 调试
python3 /Users/jiejiang/Desktop/dev/Claude/Meta-Skill/meta_skill/cli.py --search tdd

# 按应用过滤
python3 /Users/jiejiang/Desktop/dev/Claude/Meta-Skill/meta_skill/cli.py --app superpowers

# 输出 JSON
python3 /Users/jiejiang/Desktop/dev/Claude/Meta-Skill/meta_skill/cli.py --format json

# 保存到文件
python3 /Users/jiejiang/Desktop/dev/Claude/Meta-Skill/meta_skill/cli.py --output report.md
```

### Python API

```python
from meta_skill.scanner import scan_all_skills
from meta_skill.report import generate_markdown_report, generate_json_report

skills = scan_all_skills()
report = generate_markdown_report(skills, locale="zh_CN")
json_data = generate_json_report(skills, locale="zh_CN")
```

## 支持的 AI 工具

| 工具 | 扫描路径 |
|------|----------|
| Claude Code | `~/.claude/skills/` |
| Claude Code 插件 | `~/.claude/plugins/marketplaces/*/` |
| Cursor | `~/.cursor/skills-cursor/` |
| OpenCode | `~/.config/opencode/skills/` |
| Gemini | `~/.gemini/antigravity/skills/` |
| Trae | `~/.trae-cn/builtin/` |
| CherryStudio | `~/Library/Application Support/CherryStudio/Data/Skills/` |

## 特性

- 🔍 多工具扫描：发现来自 Claude Code、Codex、Cursor、OpenCode、Gemini、Trae、CherryStudio 的技能
- 🌍 自动语言检测：检测系统语言（macOS AppleLocale、LANG、LC_ALL）
- 🇨🇳 中文翻译：内置 100+ 术语和适用场景的中文字典
- 🔎 中英搜索：搜索"调试"可找到 debug、debugging、investigate 等技能
- 📊 分组报告：按来源应用分组，附带统计信息
- 🔄 去重：`--unique` 标志移除不同来源的重复技能
- 📋 多格式：Markdown 报告和 JSON 编程接口
- 🚀 零依赖：纯 Python，无需外部包
