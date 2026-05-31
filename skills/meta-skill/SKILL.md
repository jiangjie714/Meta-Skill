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

## Quick Commands

```bash
ms                  # 扫描所有技能（自动检测语言，自动去重）
ms zh               # 中文输出
ms en               # 英文输出
ms superpowers       # 只看 superpowers 的技能
ms search 调试       # 搜索调试相关技能（支持中文！）
ms search tdd        # 搜索 TDD 相关技能
ms json             # JSON 格式输出
ms -o report.md     # 保存到文件
ms -q               # 静默模式
ms -a               # 显示所有（不去重）
```

## Search Keyword Mapping

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
