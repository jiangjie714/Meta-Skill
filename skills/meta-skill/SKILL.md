---
name: meta-skill
description: "发现、分析、翻译和解释所有已安装的 AI 编程助手技能。Use when the user asks what skills they have, what a skill does, or when to use a skill. / Discover, analyze, translate, and explain all installed AI coding assistant skills."
---

# Meta-Skill: Skill Discovery & Analysis

Discover, catalog, translate, and explain all installed skills across your AI coding assistants.

## When to Invoke This Skill

Invoke this skill when the user:

- Asks what skills are installed (e.g., "我有哪些技能？", "What skills do I have?")
- Wants to know what a specific skill does (e.g., "What does TDD skill do?", "superpowers 是什么？")
- Wants to know when to use a skill (e.g., "When should I use systematic-debugging?")
- Wants to search for skills by domain (e.g., "有哪些测试相关的技能？", "Find me debugging skills")
- Wants to understand skills from a specific app (e.g., "superpowers 里面有什么？")
- Asks about skill coverage or gaps (e.g., "Do I have any security skills installed?")
- Wants a translated/localized overview (e.g., "用中文告诉我有哪些技能")

## How to Use

### Step 1: Run the Scanner

Run the scanner to collect all skill data:

```bash
# Full scan (deduplicated, in Chinese)
python3 -m meta_skill.cli --locale zh_CN --unique

# Search for specific skills
python3 -m meta_skill.cli --locale zh_CN --unique --search <keyword>

# Filter by application
python3 -m meta_skill.cli --locale zh_CN --unique --app <app-name>

# JSON output for programmatic use
python3 -m meta_skill.cli --locale zh_CN --unique --format json

# English output
python3 -m meta_skill.cli --locale en_US --unique
```

The scanner searches these paths:

| Tool | Path |
|------|------|
| Claude Code | `~/.claude/skills/` |
| Claude Code Plugins | `~/.claude/plugins/marketplaces/*/` |
| Cursor | `~/.cursor/skills-cursor/` |
| OpenCode | `~/.config/opencode/skills/` |
| Gemini | `~/.gemini/antigravity/skills/` |
| Trae | `~/.trae-cn/builtin/` |
| CherryStudio | `~/Library/Application Support/CherryStudio/Data/Skills/` |

### Step 2: Present Results to the User

Based on the user's question, present the information in a clear, organized way:

**For "what skills do I have?" questions:**
- Show the grouped overview (by application/source)
- Include the total count and source breakdown

**For "what does skill X do?" questions:**
- Show the specific skill's name, Chinese name, description, and usage scenario
- Explain which app it belongs to and when to invoke it

**For "find me skills for X" questions:**
- Use `--search` with relevant keywords (supports Chinese!)
- Present matching skills with their usage scenarios

**For app-specific questions:**
- Use `--app <name>` to filter
- Show all skills from that app with their descriptions

### Step 3: Offer Actionable Guidance

After presenting results, offer to:
- Explain any skill in more detail (read its SKILL.md)
- Help install new skills using `npx skills add`
- Save the report to a file with `--output`
- Search for specific domains with `--search`

## Search Keyword Mapping

The scanner supports Chinese-to-English keyword expansion for better results:

| Chinese | English Keywords |
|---------|-----------------|
| 调试 | debug, investigate |
| 测试 | test, tdd, verification, eval, qa |
| 代码审查 | review, code-review |
| 安全 | security |
| 前端 | frontend, ui, ux, design, 3d |
| 后端 | backend, api, django, spring, flask |
| 数据库 | database, postgres, clickhouse, sql |
| 部署 | deploy, docker, kubernetes |
| 规划 | plan, brainstorm |
| 代理 | agent, subagent, dispatch |

## Application Name Mapping

| English | Chinese |
|---------|---------|
| superpowers | Superpowers 超能力集 |
| everything-claude-code | Everything Claude Code 全能插件 |
| gstack | GStack 开发流程工具集 |
| anthropic-agent-skills | Anthropic 官方技能集 |
| thedotmack | Claude-Mem 记忆插件 |
| ui-ux-pro-max | UI/UX 专业级设计技能 |
| openai-codex | OpenAI Codex 插件 |
| minimalist-entrepreneur | 极简创业者插件 |

## Important Notes

- The scanner automatically detects the system locale (zh_CN for Chinese macOS)
- Use `--unique` to deduplicate skills that appear in multiple locations
- Use `--format json` when you need to process results programmatically
- The scanner is zero-dependency (pure Python stdlib) and runs offline
