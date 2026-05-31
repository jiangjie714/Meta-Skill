"""Scan the filesystem for AI coding assistant skills across multiple tools."""

import os
import re
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional

HOME = Path.home()

# Known skill directories for different AI coding tools
SCAN_PATHS = {
    "Claude Code": [
        HOME / ".claude" / "skills",
    ],
    "Claude Code Plugins (marketplace)": [
        HOME / ".claude" / "plugins" / "marketplaces",
    ],
    "Claude Code Plugins (cache)": [
        HOME / ".claude" / "plugins" / "cache",
    ],
    "Cursor": [
        HOME / ".cursor" / "skills-cursor",
    ],
    "OpenCode": [
        HOME / ".config" / "opencode" / "skills",
        HOME / ".config" / "opencode" / "superpowers" / "skills",
    ],
    "Gemini": [
        HOME / ".gemini" / "antigravity" / "skills",
    ],
    "Trae": [
        HOME / ".trae-cn" / "builtin",
    ],
    "CherryStudio": [
        HOME / "Library" / "Application Support" / "CherryStudio" / "Data" / "Skills",
    ],
}

# Skip directories that are not skill directories
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".claude-plugin", ".codex-plugin",
              ".cursor-plugin", "scripts", "hooks", "tests", "docs", "assets",
              ".github", ".in_use", "references"}


@dataclass
class SkillInfo:
    """Parsed information about a single skill."""
    name: str
    description: str = ""
    origin: str = ""
    version: str = ""
    source_tool: str = ""  # e.g. "Claude Code", "Cursor"
    source_app: str = ""   # e.g. "superpowers", "gstack", "everything-claude-code"
    file_path: str = ""
    trigger_hints: str = ""
    has_disable_model_invocation: bool = False


def parse_frontmatter(content: str) -> dict:
    """Parse YAML-like frontmatter from a SKILL.md file."""
    result = {}
    if not content.startswith("---"):
        return result

    end_match = re.search(r"\n---\n", content[3:])
    if not end_match:
        return result

    fm_text = content[3:end_match.start() + 3]
    current_key = None
    current_value = ""
    in_multiline = False

    for line in fm_text.split("\n"):
        line = line.rstrip()
        if not line:
            if in_multiline and current_key:
                current_value += "\n"
            continue

        if in_multiline and line.startswith("  "):
            current_value += "\n" + line.strip()
            continue

        if current_key and not in_multiline:
            result[current_key] = current_value.strip()
        elif current_key and in_multiline:
            result[current_key] = current_value.strip()
            in_multiline = False

        colon_match = re.match(r"^(\S+):\s*(.*)", line)
        if colon_match:
            current_key = colon_match.group(1)
            current_value = colon_match.group(2).strip()
            if current_value in ("|", ">"):
                in_multiline = True
                current_value = ""
            elif current_value.startswith('"') and current_value.endswith('"'):
                result[current_key] = current_value[1:-1]
                current_key = None
                in_multiline = False
        elif current_key:
            in_multiline = True
            current_value += " " + line.strip()

    if current_key:
        result[current_key] = current_value.strip()

    return result


def extract_trigger_hints(content: str) -> str:
    """Extract 'when to use' hints from SKILL.md body."""
    patterns = [
        r"(?:When to [Uu]se|Use when)\s*[:：]?\s*\n((?:[-*]\s+.+\n?)+)",
        r"(?:Trigger|TRIGGER)\s*[:：]?\s*\n((?:[-*]\s+.+\n?)+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        if match:
            text = match.group(1).strip()
            if len(text) > 10:
                return text[:300]

    # Try to get first meaningful paragraph from body
    body_match = re.search(r"\n---\n(.+)", content, re.DOTALL)
    if body_match:
        body = body_match.group(1).strip()
        paragraphs = re.split(r"\n{2,}", body)
        for p in paragraphs:
            p = p.strip()
            if p and not p.startswith("#") and not p.startswith("```") and not p.startswith("<") and len(p) > 20:
                return p[:300]

    return ""


def parse_skill_file(filepath: Path) -> Optional[SkillInfo]:
    """Parse a SKILL.md file and return SkillInfo."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None

    frontmatter = parse_frontmatter(content)
    if not frontmatter and not content.strip():
        return None

    name = frontmatter.get("name", filepath.parent.name)
    description = frontmatter.get("description", "")
    origin = frontmatter.get("origin", "")
    version = frontmatter.get("version", "")
    has_disable = frontmatter.get("disable-model-invocation", "").lower() == "true"

    # Clean description - take first line for multiline
    if description:
        first_line = description.split("\n")[0].strip()
        if first_line and len(first_line) > 10:
            description = first_line
    description = description.strip().strip('"').strip("'")

    trigger = extract_trigger_hints(content)

    return SkillInfo(
        name=name,
        description=description,
        origin=origin,
        version=version,
        file_path=str(filepath),
        trigger_hints=trigger,
        has_disable_model_invocation=has_disable,
    )


def find_skill_files(directory: Path) -> list[Path]:
    """Recursively find all SKILL.md files in a directory."""
    skills = []
    if not directory.exists():
        return skills

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        if "SKILL.md" in files:
            skills.append(Path(root) / "SKILL.md")

    return skills


def determine_source_app(filepath: Path) -> str:
    """Determine which application/plugin a skill belongs to."""
    path_str = str(filepath)

    # Check for marketplace paths
    if "marketplaces" in path_str:
        parts = path_str.split("marketplaces")
        if len(parts) > 1:
            sub = parts[1].lstrip("/").split("/")[0]
            return sub

    # Check for cache paths
    if "/cache/" in path_str:
        parts = path_str.split("/cache/")
        if len(parts) > 1:
            sub = parts[1].lstrip("/").split("/")[0]
            return sub

    # Check for superpowers pattern
    if "/superpowers/skills/" in path_str or "/superpowers/" in path_str:
        return "superpowers"

    # Known app patterns
    known_apps = {
        "gstack": "gstack",
        "thedotmack": "thedotmack",
        "everything-claude-code": "everything-claude-code",
        "anthropic-agent-skills": "anthropic-agent-skills",
        "ui-ux-pro-max": "ui-ux-pro-max",
        "minimalist-entrepreneur": "minimalist-entrepreneur",
        "openai-codex": "openai-codex",
        "claude-plugins-official": "claude-plugins-official",
    }
    for app_key, app_val in known_apps.items():
        if app_key in path_str.lower():
            return app_val

    # For .claude/skills
    if "/.claude/skills/" in path_str:
        return "claude-global-skills"

    # For cursor
    if "/.cursor/" in path_str:
        return "cursor-skills"

    # For opencode
    if "/.config/opencode/" in path_str:
        return "opencode-skills"

    # For gemini
    if "/.gemini/" in path_str:
        return "gemini-skills"

    # For trae
    if "/.trae" in path_str:
        return "trae-skills"

    # For CherryStudio
    if "CherryStudio" in path_str:
        return "cherrystudio-skills"

    # For project-level
    if "/Desktop/dev/" in path_str:
        # Extract project name
        parts = path_str.split("/Desktop/dev/")
        if len(parts) > 1:
            project = parts[1].split("/")[0]
            return f"project-{project}"

    return "unknown"


def determine_source_tool(filepath: Path) -> str:
    """Determine which AI tool a skill belongs to."""
    path_str = str(filepath)

    if "/.claude/" in path_str:
        return "Claude Code"
    elif "/.cursor/" in path_str:
        return "Cursor"
    elif "/.config/opencode/" in path_str:
        return "OpenCode"
    elif "/.gemini/" in path_str:
        return "Gemini"
    elif "/.trae" in path_str:
        return "Trae"
    elif "CherryStudio" in path_str:
        return "CherryStudio"
    else:
        return "Unknown"


def scan_all_skills() -> list[SkillInfo]:
    """Scan all known directories for skills, deduplicating by name+app."""
    all_skills = []
    seen_keys = set()  # (name, source_app) to deduplicate

    for tool_name, directories in SCAN_PATHS.items():
        for directory in directories:
            if not directory.exists():
                continue

            skill_files = find_skill_files(directory)
            for sf in skill_files:
                skill = parse_skill_file(sf)
                if not skill:
                    continue

                skill.source_tool = determine_source_tool(sf)
                skill.source_app = determine_source_app(sf)

                # Deduplicate: same skill name from the same app, keep the most specific one
                # Prefer marketplace paths over cache paths
                key = (skill.name, skill.source_app)
                if key in seen_keys:
                    # Keep the one that's not from cache if possible
                    existing_idx = None
                    for i, existing in enumerate(all_skills):
                        if (existing.name, existing.source_app) == key:
                            existing_idx = i
                            break
                    if existing_idx is not None:
                        # Prefer non-cache entries
                        if "/cache/" not in str(sf) and "/cache/" in all_skills[existing_idx].file_path:
                            all_skills[existing_idx] = skill
                        elif "/cache/" not in str(sf):
                            # Both are non-cache, skip duplicate
                            continue
                        else:
                            continue
                else:
                    seen_keys.add(key)
                    all_skills.append(skill)

    # Also scan project-level skills (limited scope)
    dev_dir = HOME / "Desktop" / "dev"
    if dev_dir.exists():
        for project in dev_dir.iterdir():
            if not project.is_dir():
                continue
            for skills_dir in [project / ".claude" / "skills", project / "skills"]:
                if not skills_dir.exists():
                    continue
                for sf in find_skill_files(skills_dir):
                    skill = parse_skill_file(sf)
                    if not skill:
                        continue
                    skill.source_tool = f"Project ({project.name})"
                    skill.source_app = f"project-{project.name}"
                    key = (skill.name, skill.source_app)
                    if key not in seen_keys:
                        seen_keys.add(key)
                        all_skills.append(skill)

    return all_skills


def group_skills_by_app(skills: list[SkillInfo]) -> dict[str, list[SkillInfo]]:
    """Group skills by their source application."""
    groups = {}
    for skill in skills:
        app_key = skill.source_app or "unknown"
        if app_key not in groups:
            groups[app_key] = []
        groups[app_key].append(skill)
    return groups


def get_marketplace_info(app_name: str) -> dict:
    """Try to load marketplace manifest for richer info."""
    manifest_dirs = {
        "superpowers-marketplace": HOME / ".claude" / "plugins" / "marketplaces" / "superpowers-marketplace",
        "gstack": HOME / ".claude" / "plugins" / "marketplaces" / "gstack",
        "everything-claude-code": HOME / ".claude" / "plugins" / "marketplaces" / "everything-claude-code",
        "thedotmack": HOME / ".claude" / "plugins" / "marketplaces" / "thedotmack",
        "openai-codex": HOME / ".claude" / "plugins" / "marketplaces" / "openai-codex",
        "minimalist-entrepreneur": HOME / ".claude" / "plugins" / "marketplaces" / "minimalist-entrepreneur",
        "ui-ux-pro-max-skill": HOME / ".claude" / "plugins" / "marketplaces" / "ui-ux-pro-max-skill",
        "anthropic-agent-skills": HOME / ".claude" / "plugins" / "marketplaces" / "anthropic-agent-skills",
    }

    if app_name not in manifest_dirs:
        return {}

    base = manifest_dirs[app_name]
    manifest_path = base / ".claude-plugin" / "manifest.json"
    if not manifest_path.exists():
        manifest_path = base / ".claude-plugin" / "marketplace.json"

    if manifest_path.exists():
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
            result = {
                "name": data.get("name", app_name),
                "description": data.get("metadata", {}).get("description", ""),
            }
            if "plugins" in data:
                result["sub_plugins"] = [
                    {"name": p["name"], "description": p.get("description", ""), "version": p.get("version", "")}
                    for p in data["plugins"]
                ]
            return result
        except Exception:
            pass

    return {}
