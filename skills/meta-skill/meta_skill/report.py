"""Report generator for skill analysis results."""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from .scanner import SkillInfo, group_skills_by_app, get_marketplace_info
from .translator import (
    detect_locale, get_language_name, translate_skill_name,
    translate_app_name, translate_description,
    detect_locale, get_language_name, translate_skill_name,
    generate_usage_scenario,
)


def generate_markdown_report(
    skills: list[SkillInfo],
    locale: str = None,
    output_path: Optional[Path] = None,
) -> str:
    """Generate a localized Markdown report of all skills."""
    if locale is None:
        locale = detect_locale()

    lang_name = get_language_name(locale)
    is_zh = locale.startswith("zh")

    groups = group_skills_by_app(skills)
    sorted_groups = sorted(groups.items(), key=lambda x: len(x[1]), reverse=True)

    lines = []

    if is_zh:
        lines.append("# 🤖 AI 编程助手技能全景图")
        lines.append("")
        lines.append(f"> 自动检测系统语言：**{lang_name}** | 扫描时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"> 共发现 **{len(skills)}** 个技能，来自 **{len(groups)}** 个来源")
        lines.append("")
        lines.append("## 📋 目录")
        lines.append("")
        for idx, (app_name, app_skills) in enumerate(sorted_groups, 1):
            display_name = translate_app_name(app_name, locale)
            anchor = app_name.lower().replace(" ", "-").replace("/", "-")
            lines.append(f"{idx}. [{display_name}](#{anchor}) — {len(app_skills)} 个技能")
        lines.append("")
        lines.append("---")
        lines.append("")
    else:
        lines.append("# 🤖 AI Coding Assistant Skills Overview")
        lines.append("")
        lines.append(f"> Detected locale: **{lang_name}** | Scanned at: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"> Found **{len(skills)}** skills from **{len(groups)}** sources")
        lines.append("")
        lines.append("## 📋 Table of Contents")
        lines.append("")
        for idx, (app_name, app_skills) in enumerate(sorted_groups, 1):
            display_name = translate_app_name(app_name, locale)
            anchor = app_name.lower().replace(" ", "-").replace("/", "-")
            lines.append(f"{idx}. [{display_name}](#{anchor}) — {len(app_skills)} skill(s)")
        lines.append("")
        lines.append("---")
        lines.append("")

    for app_name, app_skills in sorted_groups:
        market_info = get_marketplace_info(app_name)
        app_display = translate_app_name(app_name, locale)
        app_desc = market_info.get("description", "")

        lines.append(f"## 📦 {app_display}")
        if app_desc:
            lines.append(f"*{app_desc}*")
        lines.append("")

        if is_zh:
            lines.append("| # | 技能名称 | 中文名称 | 说明 | 适用场景 |")
            lines.append("|---|---------|---------|------|---------|")
        else:
            lines.append("| # | Skill Name | Localized Name | Description | When to Use |")
            lines.append("|---|------------|----------------|-------------|-------------|")

        for idx, skill in enumerate(sorted(app_skills, key=lambda s: s.name), 1):
            local_name = translate_skill_name(skill.name, locale)
            desc = translate_description(skill.description, locale) if is_zh else skill.description
            scenario = generate_usage_scenario(skill.name, skill.description, locale)

            if len(desc) > 100:
                desc = desc[:97] + "..."
            if len(scenario) > 120:
                scenario = scenario[:117] + "..."

            desc = desc.replace("\n", " ").replace("|", "│")
            scenario = scenario.replace("\n", " ").replace("|", "│")

            lines.append(f"| {idx} | `{skill.name}` | {local_name} | {desc} | {scenario} |")

        lines.append("")

        if market_info.get("sub_plugins"):
            if is_zh:
                lines.append("### 包含的子插件")
            else:
                lines.append("### Included Sub-Plugins")
            lines.append("")
            for plugin in market_info["sub_plugins"]:
                plugin_name = plugin["name"]
                plugin_desc = plugin.get("description", "")
                plugin_ver = plugin.get("version", "")
                lines.append(f"- **{plugin_name}** (v{plugin_ver}): {plugin_desc}")
            lines.append("")

        lines.append("---")
        lines.append("")

    # Summary
    if is_zh:
        lines.append("## 📊 总结")
        lines.append("")
        lines.append(f"共扫描到来自 **{len(groups)}** 个来源的 **{len(skills)}** 个技能。")
        lines.append("")
        lines.append("### 按来源分布")
        lines.append("")
        for app_name, app_skills in sorted_groups:
            count = len(app_skills)
            bar = "█" * min(count, 30)
            lines.append(f"- {translate_app_name(app_name, locale)}: {count} {bar}")
        lines.append("")
        lines.append("### 按类别分布")
        lines.append("")
        categories = {}
        for skill in skills:
            cat = categorize_skill(skill)
            if cat not in categories:
                categories[cat] = 0
            categories[cat] += 1
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:15]:
            cat_display = translate_skill_name(cat, locale)
            lines.append(f"- {cat_display}: {count}")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("*由 Meta-Skill 自动生成 · 支持 Claude Code / Codex / Cursor / OpenCode / Gemini 等多种 AI 编程助手*")
    else:
        lines.append("## 📊 Summary")
        lines.append("")
        lines.append(f"Scanned **{len(skills)}** skills from **{len(groups)}** sources.")
        lines.append("")
        lines.append("### Distribution by Source")
        lines.append("")
        for app_name, app_skills in sorted_groups:
            count = len(app_skills)
            bar = "█" * min(count, 30)
            lines.append(f"- {app_name}: {count} {bar}")
        lines.append("")
        lines.append("### Distribution by Category")
        lines.append("")
        categories = {}
        for skill in skills:
            cat = categorize_skill(skill)
            if cat not in categories:
                categories[cat] = 0
            categories[cat] += 1
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:15]:
            lines.append(f"- {cat}: {count}")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("*Generated by Meta-Skill · Supports Claude Code / Codex / Cursor / OpenCode / Gemini and more*")

    report = "\n".join(lines)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding="utf-8")

    return report


def generate_json_report(
    skills: list[SkillInfo],
    locale: str = None,
    output_path: Optional[Path] = None,
) -> str:
    """Generate a JSON report of all skills."""
    if locale is None:
        locale = detect_locale()

    groups = group_skills_by_app(skills)

    result = {
        "meta": {
            "generated_at": datetime.now().isoformat(),
            "locale": locale,
            "language": get_language_name(locale),
            "total_skills": len(skills),
            "total_sources": len(groups),
        },
        "sources": {},
    }

    for app_name, app_skills in sorted(groups.items()):
        market_info = get_marketplace_info(app_name)
        source_data = {
            "display_name": translate_app_name(app_name, locale),
            "original_name": app_name,
            "description": market_info.get("description", ""),
            "skill_count": len(app_skills),
            "skills": [],
        }

        if market_info.get("sub_plugins"):
            source_data["sub_plugins"] = market_info["sub_plugins"]

        for skill in sorted(app_skills, key=lambda s: s.name):
            skill_data = {
                "name": skill.name,
                "localized_name": translate_skill_name(skill.name, locale),
                "description": skill.description,
                "localized_description": translate_description(skill.description, locale),
                "origin": skill.origin,
                "version": skill.version,
                "source_tool": skill.source_tool,
                "source_app": skill.source_app,
                "when_to_use": generate_usage_scenario(skill.name, skill.description, locale),
                "file_path": skill.file_path,
            }
            source_data["skills"].append(skill_data)

        result["sources"][app_name] = source_data

    json_str = json.dumps(result, ensure_ascii=False, indent=2)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json_str, encoding="utf-8")

    return json_str


def categorize_skill(skill: SkillInfo) -> str:
    """Assign a category to a skill based on its name and description."""
    name_lower = skill.name.lower()
    desc_lower = skill.description.lower() if skill.description else ""

    category_rules = [
        (["test", "tdd", "verification", "eval"], "testing"),
        (["debug", "debugg"], "debugging"),
        (["review", "code-review"], "code-review"),
        (["security"], "security"),
        (["frontend", "ui", "ux", "design", "3d", "threejs", "web-design", "liquid-glass"], "frontend"),
        (["backend", "api", "server", "spring", "django", "flask", "laravel"], "backend"),
        (["database", "postgres", "clickhouse", "sql", "jpa"], "database"),
        (["docker", "deploy", "kubernetes", "k8s"], "devops"),
        (["git", "branch", "worktree"], "git"),
        (["plan", "brainstorm", "execut"], "planning"),
        (["agent", "subagent", "dispatch", "parallel"], "agent"),
        (["golang", "go-"], "golang"),
        (["python"], "python"),
        (["rust-"], "rust"),
        (["kotlin"], "kotlin"),
        (["swift"], "swift"),
        (["java-"], "java"),
        (["perl"], "perl"),
        (["react", "nextjs", "remotion"], "react"),
        (["document", "obsidian", "json-canvas"], "documentation"),
        (["learn", "memory", "compact"], "learning"),
        (["research", "search", "exa", "tavily"], "research"),
        (["video", "media", "fal-ai"], "media"),
        (["modeling"], "3d-modeling"),
        (["game"], "game-dev"),
    ]

    for keywords, category in category_rules:
        for kw in keywords:
            if kw in name_lower or kw in desc_lower:
                return category

    return "general"
