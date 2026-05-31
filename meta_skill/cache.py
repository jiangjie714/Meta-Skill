"""Cache manager for Meta-Skill scan results.

Stores scan results in a cache file for fast subsequent reads.
Cache locations (in order of preference):
  1. ~/.meta-skill/cache.json  (preferred)
  2. /tmp/meta-skill/cache.json (fallback)
"""

import json
import os
import time
import tempfile
from pathlib import Path
from typing import Optional

from .scanner import SkillInfo, group_skills_by_app, get_marketplace_info
from .translator import detect_locale, get_language_name

# Cache locations in priority order
_CACHE_DIRS = [
    Path.home() / ".meta-skill",
    Path(tempfile.gettempdir()) / "meta-skill",
]

CACHE_FILENAME = "cache.json"
DEFAULT_TTL = 86400  # 24 hours


def _get_cache_dir() -> Path:
    """Find a writable cache directory."""
    for d in _CACHE_DIRS:
        try:
            d.mkdir(parents=True, exist_ok=True)
            test_file = d / ".write_test"
            test_file.write_text("ok")
            test_file.unlink()
            return d
        except (OSError, PermissionError):
            continue
    # Last resort: current directory
    return Path.cwd() / ".meta-skill-cache"


def _get_cache_file() -> Path:
    """Get the cache file path."""
    return _get_cache_dir() / CACHE_FILENAME


def _skill_to_dict(skill: SkillInfo) -> dict:
    """Convert SkillInfo to a serializable dict."""
    return {
        "name": skill.name,
        "description": skill.description,
        "origin": skill.origin,
        "version": skill.version,
        "source_tool": skill.source_tool,
        "source_app": skill.source_app,
        "file_path": skill.file_path,
        "trigger_hints": skill.trigger_hints,
        "has_disable_model_invocation": skill.has_disable_model_invocation,
    }


def _dict_to_skill(d: dict) -> SkillInfo:
    """Convert a dict back to SkillInfo."""
    return SkillInfo(
        name=d["name"],
        description=d.get("description", ""),
        origin=d.get("origin", ""),
        version=d.get("version", ""),
        source_tool=d.get("source_tool", ""),
        source_app=d.get("source_app", ""),
        file_path=d.get("file_path", ""),
        trigger_hints=d.get("trigger_hints", ""),
        has_disable_model_invocation=d.get("has_disable_model_invocation", False),
    )


def save_cache(skills: list[SkillInfo], locale: str = None) -> Path:
    """Save scan results to cache file."""
    if locale is None:
        locale = detect_locale()

    cache_dir = _get_cache_dir()
    cache_dir.mkdir(parents=True, exist_ok=True)

    groups = group_skills_by_app(skills)
    grouped = {}
    for app_name, app_skills in groups.items():
        market_info = get_marketplace_info(app_name)
        grouped[app_name] = {
            "skill_count": len(app_skills),
            "skills": [_skill_to_dict(s) for s in app_skills],
        }
        if market_info:
            grouped[app_name]["market_description"] = market_info.get("description", "")
            if "sub_plugins" in market_info:
                grouped[app_name]["sub_plugins"] = market_info["sub_plugins"]

    name_index = {}
    for skill in skills:
        key = skill.name.lower()
        if key not in name_index:
            name_index[key] = []
        name_index[key].append(_skill_to_dict(skill))

    search_index = {}
    for skill in skills:
        search_index[skill.name] = f"{skill.name} {skill.description}".lower()

    cache_data = {
        "version": 2,
        "timestamp": time.time(),
        "timestamp_human": time.strftime("%Y-%m-%d %H:%M:%S"),
        "locale": locale,
        "language": get_language_name(locale),
        "total_skills": len(skills),
        "total_unique": len(set(s.name for s in skills)),
        "total_sources": len(groups),
        "skills": [_skill_to_dict(s) for s in skills],
        "grouped": grouped,
        "name_index": name_index,
        "search_index": search_index,
    }

    cache_file = _get_cache_file()
    cache_file.write_text(json.dumps(cache_data, ensure_ascii=False, indent=2), encoding="utf-8")
    return cache_file


def load_cache(max_age: float = DEFAULT_TTL) -> Optional[dict]:
    """Load scan results from cache if fresh enough."""
    cache_file = _get_cache_file()
    if not cache_file.exists():
        return None

    try:
        data = json.loads(cache_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None

    if data.get("version", 0) < 2:
        return None

    timestamp = data.get("timestamp", 0)
    if max_age > 0 and (time.time() - timestamp) > max_age:
        return None

    return data


def get_cache_age() -> Optional[float]:
    """Get cache age in seconds."""
    cache_file = _get_cache_file()
    if not cache_file.exists():
        return None
    try:
        data = json.loads(cache_file.read_text(encoding="utf-8"))
        return time.time() - data.get("timestamp", 0)
    except Exception:
        return None


def is_cache_fresh(max_age: float = DEFAULT_TTL) -> bool:
    """Check if cache exists and is fresh."""
    return load_cache(max_age=max_age) is not None


def search_cache(cache_data: dict, keyword: str, locale: str = None) -> list[dict]:
    """Search cached skills by keyword (supports Chinese expansion)."""
    from .translator import expand_search_keywords

    if locale is None:
        locale = detect_locale()

    keywords = expand_search_keywords(keyword, locale)
    results = []
    seen = set()
    skills = cache_data.get("skills", [])

    for skill_dict in skills:
        name = skill_dict["name"].lower()
        desc = skill_dict.get("description", "").lower()
        text = f"{name} {desc}"

        for kw in keywords:
            if kw in text and name not in seen:
                results.append(skill_dict)
                seen.add(name)
                break

    return results


def format_cache_summary(cache_data: dict, locale: str = None) -> str:
    """Format a fast cache summary."""
    from .translator import translate_app_name

    if locale is None:
        locale = cache_data.get("locale", detect_locale())

    is_zh = locale.startswith("zh")
    timestamp = cache_data.get("timestamp_human", "unknown")
    total = cache_data.get("total_skills", 0)
    unique = cache_data.get("total_unique", total)
    sources = cache_data.get("total_sources", 0)
    grouped = cache_data.get("grouped", {})
    age = get_cache_age()

    if age is not None:
        if age < 60:
            age_str = f"{int(age)}秒前" if is_zh else f"{int(age)}s ago"
        elif age < 3600:
            age_str = f"{int(age/60)}分钟前" if is_zh else f"{int(age/60)}min ago"
        else:
            age_str = f"{int(age/3600)}小时前" if is_zh else f"{int(age/3600)}h ago"
    else:
        age_str = ""

    lines = []
    if is_zh:
        lines.append(f"📦 技能缓存（{age_str}，扫描于 {timestamp}）")
        lines.append(f"   共 {total} 个技能，{unique} 个去重，{sources} 个来源")
        lines.append("")
        lines.append("来源列表（使用 ms <来源名> 查看详情）：")
    else:
        lines.append(f"📦 Skill cache ({age_str}, scanned at {timestamp})")
        lines.append(f"   {total} skills, {unique} unique, {sources} sources")
        lines.append("")
        lines.append("Sources (use ms <source> for details):")

    for app_name, app_data in sorted(grouped.items(), key=lambda x: x[1].get("skill_count", 0), reverse=True):
        display = translate_app_name(app_name, locale)
        count = app_data.get("skill_count", 0)
        lines.append(f"  {display}: {count}")

    lines.append("")
    if is_zh:
        lines.append("💡 使用 ms <来源名> 查看详情  |  ms search <关键词> 搜索  |  ms --refresh 重新扫描")
    else:
        lines.append("💡 Use ms <source> for details | ms search <keyword> | ms --refresh to re-scan")

    return "\n".join(lines)


def format_cache_app(cache_data: dict, app_name: str, locale: str = None) -> str:
    """Format cached skills for a specific app."""
    from .translator import translate_app_name, translate_skill_name, translate_description, generate_usage_scenario
    from .report import get_marketplace_info

    if locale is None:
        locale = cache_data.get("locale", detect_locale())

    is_zh = locale.startswith("zh")
    grouped = cache_data.get("grouped", {})
    app_data = grouped.get(app_name)

    if not app_data:
        if is_zh:
            return f"❌ 未找到来源 '{app_name}'，使用 ms 查看所有来源"
        else:
            return f"❌ Source '{app_name}' not found. Use ms to list all sources."

    skills = app_data.get("skills", [])
    market_info = get_marketplace_info(app_name)
    app_display = translate_app_name(app_name, locale)
    app_desc = app_data.get("market_description", "") or (market_info.get("description", "") if market_info else "")

    lines = []
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

    for idx, skill_dict in enumerate(sorted(skills, key=lambda s: s["name"]), 1):
        name = skill_dict["name"]
        local_name = translate_skill_name(name, locale)
        desc = translate_description(skill_dict.get("description", ""), locale) if is_zh else skill_dict.get("description", "")
        scenario = generate_usage_scenario(name, skill_dict.get("description", ""), locale)

        if len(desc) > 100: desc = desc[:97] + "..."
        if len(scenario) > 120: scenario = scenario[:117] + "..."
        desc = desc.replace("\n", " ").replace("|", "│")
        scenario = scenario.replace("\n", " ").replace("|", "│")

        lines.append(f"| {idx} | `{name}` | {local_name} | {desc} | {scenario} |")

    lines.append("")

    sub_plugins = app_data.get("sub_plugins") or (market_info.get("sub_plugins") if market_info else None)
    if sub_plugins:
        if is_zh:
            lines.append("### 包含的子插件")
        else:
            lines.append("### Included Sub-Plugins")
        lines.append("")
        for plugin in sub_plugins:
            pn = plugin.get("name", "")
            pd = plugin.get("description", "")
            pv = plugin.get("version", "")
            lines.append(f"- **{pn}** (v{pv}): {pd}")
        lines.append("")

    return "\n".join(lines)


def format_cache_search(cache_data: dict, keyword: str, locale: str = None) -> str:
    """Format search results from cache."""
    results = search_cache(cache_data, keyword, locale)

    from .translator import translate_skill_name, translate_app_name, translate_description, generate_usage_scenario

    if locale is None:
        locale = cache_data.get("locale", detect_locale())

    is_zh = locale.startswith("zh")

    if not results:
        if is_zh:
            return f"❌ 未找到与 '{keyword}' 相关的技能（从缓存）"
        else:
            return f"❌ No skills found matching '{keyword}' (from cache)"

    lines = []
    if is_zh:
        lines.append(f"🔍 搜索 '{keyword}' 找到 {len(results)} 个技能（从缓存）")
        lines.append("")
        lines.append("| # | 技能名称 | 中文名称 | 来源 | 说明 | 适用场景 |")
        lines.append("|---|---------|---------|------|------|---------|")
    else:
        lines.append(f"🔍 Found {len(results)} skills matching '{keyword}' (from cache)")
        lines.append("")
        lines.append("| # | Skill Name | Localized Name | Source | Description | When to Use |")
        lines.append("|---|------------|----------------|--------|-------------|-------------|")

    for idx, skill_dict in enumerate(results, 1):
        name = skill_dict["name"]
        local_name = translate_skill_name(name, locale)
        app = translate_app_name(skill_dict.get("source_app", ""), locale)
        desc = translate_description(skill_dict.get("description", ""), locale) if is_zh else skill_dict.get("description", "")
        scenario = generate_usage_scenario(name, skill_dict.get("description", ""), locale)

        if len(desc) > 80: desc = desc[:77] + "..."
        if len(scenario) > 100: scenario = scenario[:97] + "..."
        desc = desc.replace("\n", " ").replace("|", "│")
        scenario = scenario.replace("\n", " ").replace("|", "│")

        lines.append(f"| {idx} | `{name}` | {local_name} | {app} | {desc} | {scenario} |")

    return "\n".join(lines)
