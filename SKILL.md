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

## ⚡ Cache-First Architecture

**IMPORTANT**: This skill uses a cache-first approach. Do NOT run `ms` shell commands for every query. Instead:

1. **Read the cache directly**: Read `~/.meta-skill/cache.json` using file read (NOT shell command)
2. **Parse the JSON** and present results based on the user's query
3. **Only run `ms --refresh`** via shell if:
   - The cache file `~/.meta-skill/cache.json` does not exist, OR
   - The user explicitly asks to refresh/re-scan, OR
   - The cache `timestamp` is older than 24 hours

This makes responses **instant** (~0.05s) instead of requiring a filesystem scan (~1.4s).

## How to Answer Queries Using Cache

### Cache File Path

```
~/.meta-skill/cache.json
```

### Cache Structure

The JSON cache contains these key fields:

- `grouped` — Skills organized by source app (e.g., `grouped["superpowers"]`, `grouped["gstack"]`)
- `name_index` — Lookup by skill name lowercase (e.g., `name_index["tdd-workflow"]`)
- `search_index` — Searchable text for each skill (e.g., `search_index["tdd-workflow"]` = "tdd-workflow ...")
- `skills` — Flat list of all skills with full details
- `total_skills`, `total_unique`, `total_sources` — Summary counts
- `timestamp_human` — When the cache was last generated
- `language` — Detected language (e.g., "简体中文")

Each skill in `grouped[app].skills[]` has:
- `name` — Skill name (e.g., "tdd-workflow")
- `description` — What the skill does
- `trigger_hints` — When to invoke this skill
- `source_app` — Which app this skill belongs to
- `source_tool` — Which tool installed this skill
- `version` — Skill version

### Query Patterns

| User asks | Action |
|-----------|--------|
| "我有哪些技能？" / "What skills do I have?" | Read `grouped` → list all sources with skill counts |
| "superpowers 里面有什么？" | Read `grouped["superpowers"]` → list all skills in that source |
| "What does TDD skill do?" | Read `name_index["tdd-workflow"]` → show description and trigger_hints |
| "有哪些调试技能？" | Search `skills[]` where name/description matches debug keywords → list matches |
| "When should I use gstack?" | Read `grouped["gstack"]` → show each skill's trigger_hints |

### Application Name Mapping

| English | Chinese | Cache Key |
|---------|---------|-----------|
| Superpowers 超能力集 | Superpowers | `superpowers` |
| Everything Claude Code 全能插件 | Everything Claude Code | `everything-claude-code` |
| GStack 开发流程工具集 | GStack | `gstack` |
| Anthropic 官方技能集 | Anthropic Agent Skills | `anthropic-agent-skills` |
| Claude-Mem 记忆插件 | Claude-Mem | `thedotmack` |
| UI/UX 专业级设计技能 | UI/UX Pro Max | `ui-ux-pro-max` |
| OpenAI Codex 插件 | OpenAI Codex | `openai-codex` |
| 极简创业者插件 | Minimalist Entrepreneur | `minimalist-entrepreneur` |

### Search Keyword Mapping (Chinese → English)

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

## Refresh Command

When the cache file does not exist at `~/.meta-skill/cache.json`, or the user asks to refresh, run:

```bash
ms --refresh
```

This scans all skill directories and saves results to `~/.meta-skill/cache.json`. Takes ~1 second.

## CLI Reference (for manual use or refresh only)

```bash
ms                  # 显示缓存摘要（从缓存读取，秒级响应 ⚡）
ms gstack           # 查看 GStack 技能详情（从缓存）
ms search 调试       # 搜索技能（从缓存，支持中文）
ms --refresh        # 重新扫描更新缓存
ms --locale zh_CN   # 切换语言
ms json --scan      # JSON 格式输出
ms -o report.md     # 保存报告到文件
```
