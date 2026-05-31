"""Translation module for skill descriptions.

Provides offline translation using built-in dictionaries for common locales,
with support for LLM-based translation as a fallback.
"""

import os
import re
import subprocess
from pathlib import Path

HOME = Path.home()

# Category translations (en -> zh_CN)
CATEGORY_ZH = {
    "testing": "测试",
    "test-driven-development": "测试驱动开发",
    "tdd": "测试驱动开发",
    "tdd-workflow": "测试驱动开发工作流",
    "debugging": "调试",
    "systematic-debugging": "系统化调试",
    "code-review": "代码审查",
    "review": "审查",
    "security": "安全",
    "security-review": "安全审查",
    "security-scan": "安全扫描",
    "frontend": "前端",
    "frontend-patterns": "前端模式",
    "backend": "后端",
    "backend-patterns": "后端模式",
    "planning": "规划",
    "writing-plans": "编写计划",
    "brainstorming": "头脑风暴",
    "verification": "验证",
    "verification-loop": "验证循环",
    "verification-before-completion": "完成前验证",
    "git": "Git 版本控制",
    "using-git-worktrees": "Git 工作树",
    "deployment": "部署",
    "design": "设计",
    "ui-ux": "UI/UX 设计",
    "ui-ux-pro-max": "UI/UX 专业级设计",
    "docker": "Docker 容器",
    "docker-patterns": "Docker 模式",
    "database": "数据库",
    "database-migrations": "数据库迁移",
    "postgres": "PostgreSQL",
    "postgres-patterns": "PostgreSQL 模式",
    "django": "Django 框架",
    "django-patterns": "Django 模式",
    "django-security": "Django 安全",
    "django-tdd": "Django 测试驱动开发",
    "django-verification": "Django 验证",
    "springboot": "Spring Boot",
    "springboot-patterns": "Spring Boot 模式",
    "springboot-security": "Spring Boot 安全",
    "springboot-tdd": "Spring Boot 测试驱动开发",
    "springboot-verification": "Spring Boot 验证",
    "golang": "Go 语言",
    "golang-patterns": "Go 语言模式",
    "golang-testing": "Go 语言测试",
    "python": "Python",
    "python-patterns": "Python 模式",
    "python-testing": "Python 测试",
    "rust": "Rust",
    "rust-patterns": "Rust 模式",
    "rust-testing": "Rust 测试",
    "kotlin": "Kotlin",
    "kotlin-patterns": "Kotlin 模式",
    "kotlin-testing": "Kotlin 测试",
    "kotlin-coroutines-flows": "Kotlin 协程与流",
    "kotlin-exposed-patterns": "Kotlin Exposed 模式",
    "kotlin-ktor-patterns": "Kotlin Ktor 模式",
    "swift": "Swift",
    "swift-concurrency": "Swift 并发",
    "swiftui-patterns": "SwiftUI 模式",
    "laravel": "Laravel",
    "laravel-patterns": "Laravel 模式",
    "laravel-security": "Laravel 安全",
    "laravel-tdd": "Laravel 测试驱动开发",
    "perl": "Perl",
    "perl-patterns": "Perl 模式",
    "perl-security": "Perl 安全",
    "perl-testing": "Perl 测试",
    "java": "Java",
    "java-coding-standards": "Java 编码规范",
    "coding-standards": "编码规范",
    "cpp-coding-standards": "C++ 编码规范",
    "continuous-learning": "持续学习",
    "continuous-learning-v2": "持续学习 v2",
    "continuous-agent-loop": "持续代理循环",
    "strategic-compact": "战略精简",
    "eval-harness": "评估工具",
    "clickhouse": "ClickHouse",
    "clickhouse-io": "ClickHouse",
    "3d": "3D 开发",
    "3d-games": "3D 游戏开发",
    "3d-modeling": "3D 建模",
    "3d-web-experience": "3D Web 体验",
    "3d-camera-interaction": "3D 相机交互",
    "threejs": "Three.js",
    "json-canvas": "JSON Canvas",
    "obsidian": "Obsidian",
    "obsidian-bases": "Obsidian Bases",
    "mcp": "MCP 服务器",
    "mcp-server-patterns": "MCP 服务器模式",
    "iteration": "迭代",
    "iterative-retrieval": "迭代检索",
    "agent": "代理",
    "subagent": "子代理",
    "subagent-driven-development": "子代理驱动开发",
    "dispatching-parallel-agents": "并行代理调度",
    "writing-skills": "编写技能",
    "finishing-a-development-branch": "完成开发分支",
    "requesting-code-review": "请求代码审查",
    "receiving-code-review": "接收代码审查",
    "executing-plans": "执行计划",
    "using-superpowers": "使用超能力",
    "agentic-engineering": "代理工程",
    "ai-first-engineering": "AI 优先工程",
    "ai-regression-testing": "AI 回归测试",
    "api-design": "API 设计",
    "article-writing": "文章写作",
    "autonomous-loops": "自主循环",
    "blueprint": "蓝图",
    "content-engine": "内容引擎",
    "data-scraper-agent": "数据抓取代理",
    "deep-research": "深度研究",
    "deployment-patterns": "部署模式",
    "e2e-testing": "端到端测试",
    "market-research": "市场研究",
    "prompt-optimizer": "提示优化器",
    "search-first": "搜索优先",
    "video-editing": "视频编辑",
    "web-design": "Web 设计",
    "web-design-guidelines": "Web 设计指南",
    "find-skills": "发现技能",
    "skill-creator": "技能创建器",
    "configure-ecc": "配置 ECC",
    "click-path-audit": "点击路径审计",
    "context-budget": "上下文预算审计",
    "investigate": "调查调试",
    "browser-qa": "浏览器 QA",
    "browse": "浏览器浏览",
    "design-consultation": "设计咨询",
    "design-review": "设计审查",
    "plan-design-review": "计划设计审查",
    "plan-eng-review": "计划工程审查",
    "plan-ceo-review": "计划 CEO 审查",
    "office-hours": "办公时间",
    "retro": "回顾",
    "ship": "发布",
    "guard": "守卫",
    "freeze": "冻结",
    "unfreeze": "解冻",
    "qa": "质量保证",
    "qa-only": "仅 QA",
    "openclaw": "OpenClaw",
}

# Application/plugin translations
APP_ZH = {
    "superpowers": "Superpowers 超能力集",
    "superpowers-marketplace": "Superpowers 市场",
    "superpowers-chrome": "Superpowers Chrome 浏览器工具",
    "everything-claude-code": "Everything Claude Code 全能插件",
    "gstack": "GStack 开发流程工具集",
    "thedotmack": "Claude-Mem 记忆插件",
    "openai-codex": "OpenAI Codex 插件",
    "ui-ux-pro-max": "UI/UX 专业级设计技能",
    "minimalist-entrepreneur": "极简创业者插件",
    "anthropic-agent-skills": "Anthropic 官方技能集",
    "claude-global-skills": "Claude Code 全局技能",
    "cursor-skills": "Cursor 编辑器技能",
    "opencode-skills": "OpenCode 技能",
    "gemini-skills": "Gemini 技能",
    "trae-skills": "Trae IDE 技能",
    "cherrystudio-skills": "CherryStudio 技能",
    "claude-session-driver": "Claude 会话驱动器",
    "episodic-memory": "情景记忆",
    "double-shot-latte": "双份拿铁（自动续写）",
    "elements-of-style": "英文写作风格指南",
    "superpowers-lab": "Superpowers 实验室",
    "superpowers-developing-for-claude-code": "Claude Code 开发技能",
}

# Chinese keyword -> English keyword mapping for enhanced search
ZH_TO_EN_KEYWORDS = {
    "测试": ["test", "tdd", "verification", "eval", "qa"],
    "调试": ["debug", "investigate"],
    "代码审查": ["review", "code-review"],
    "安全": ["security"],
    "前端": ["frontend", "ui", "ux", "design", "3d", "threejs"],
    "后端": ["backend", "api", "server", "django", "spring", "flask", "laravel"],
    "数据库": ["database", "postgres", "clickhouse", "sql", "migration"],
    "部署": ["deploy", "docker", "kubernetes"],
    "规划": ["plan", "brainstorm"],
    "代理": ["agent", "subagent", "dispatch"],
    "设计": ["design", "ui", "ux"],
    "学习": ["learn", "memory", "compact"],
    "研究": ["research", "search"],
}


def detect_locale() -> str:
    """Detect the user's preferred locale."""
    for var in ("LANG", "LC_ALL", "LC_MESSAGES"):
        val = os.environ.get(var, "")
        if val:
            locale = val.split(".")[0].replace("UTF-8", "").replace("utf8", "").rstrip(".")
            if locale:
                return locale

    try:
        result = subprocess.run(
            ["defaults", "read", "-g", "AppleLocale"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass

    return "en_US"


def get_language_name(locale: str) -> str:
    """Get a human-readable language name for a locale."""
    locale_langs = {
        "zh_CN": "简体中文", "zh_TW": "繁體中文", "zh_HK": "繁體中文（香港）",
        "ja_JP": "日本語", "ko_KR": "한국어", "fr_FR": "Français",
        "de_DE": "Deutsch", "es_ES": "Español", "pt_BR": "Português",
        "ru_RU": "Русский", "it_IT": "Italiano", "en_US": "English",
    }
    if locale in locale_langs:
        return locale_langs[locale]
    lang_map = {
        "zh": "简体中文", "ja": "日本語", "ko": "한국어",
        "fr": "Français", "de": "Deutsch", "es": "Español",
        "pt": "Português", "ru": "Русский", "it": "Italiano",
        "en": "English", "ar": "العربية", "hi": "हिन्दी",
        "th": "ไทย", "vi": "Tiếng Việt",
    }
    return lang_map.get(locale.split("_")[0], locale)


def translate_skill_name(name: str, locale: str) -> str:
    """Translate a skill name to the target locale."""
    if not locale.startswith("zh"):
        return name

    key = name.lower().replace(" ", "-").replace("_", "-")
    if key in CATEGORY_ZH:
        return CATEGORY_ZH[key]

    # Try partial matches
    name_lower = name.lower()
    for eng, zh in sorted(CATEGORY_ZH.items(), key=lambda x: len(x[0]), reverse=True):
        if eng in name_lower:
            return name.replace(eng.replace("-", " "), zh).replace(eng, zh)

    return name


def translate_app_name(app_name: str, locale: str) -> str:
    """Translate an application/plugin name."""
    if locale.startswith("zh"):
        key = app_name.lower()
        if key in APP_ZH:
            return APP_ZH[key]
    return app_name


def translate_description(description: str, locale: str) -> str:
    """Translate a skill description to the target locale.

    For Chinese locales, uses built-in dictionary for partial translation.
    """
    if not locale.startswith("zh") or not description:
        return description

    result = description
    sorted_phrases = sorted(
        {
            "Use when": "适用场景：", "use when": "适用场景：",
            "Use for": "用于：", "use for": "用于：",
            "before writing": "在编写...之前",
            "implementing any feature": "实现任何功能",
            "bugfix": "Bug 修复", "bug fix": "Bug 修复",
            "test-driven development": "测试驱动开发",
            "systematic debugging": "系统化调试",
            "code review": "代码审查",
            "starting any conversation": "开始任何对话时",
            "encountering any bug": "遇到任何 Bug 时",
            "test failure": "测试失败",
            "unexpected behavior": "异常行为",
            "before proposing fixes": "在提出修复方案之前",
            "writing implementation code": "编写实现代码",
            "Patterns and best practices": "模式和最佳实践",
            "Best practices": "最佳实践",
            "architecture patterns": "架构模式",
            "production-grade": "生产级",
            "scalable, maintainable": "可扩展、可维护",
        }.items(),
        key=lambda x: len(x[0]), reverse=True,
    )
    for eng, zh in sorted_phrases:
        result = result.replace(eng, zh)

    return result


def generate_usage_scenario(name: str, description: str, locale: str = "en_US") -> str:
    """Generate a usage scenario description for a skill."""
    name_lower = name.lower()
    desc_lower = (description or "").lower()

    scenarios_zh = {
        "tdd": "当你在编写新功能或修复 Bug 时，先写测试用例，再写实现代码",
        "test-driven-development": "当你在编写新功能或修复 Bug 时，先写测试用例，再写实现代码",
        "debugging": "当你遇到 Bug、测试失败或异常行为时，在提出修复方案之前先系统化地排查根因",
        "systematic-debugging": "当你遇到 Bug、测试失败或异常行为时，在提出修复方案之前先系统化地排查根因",
        "investigate": "当你需要系统性地调查和调试问题时",
        "brainstorming": "当你开始新项目或需要创意发散时，帮你头脑风暴和探索方案",
        "writing-plans": "当任务较复杂需要规划时，帮你制定结构化的执行计划",
        "executing-plans": "当你有了计划需要逐步执行时，帮你按步骤推进",
        "code-review": "当你完成代码需要审查时，帮你检查代码质量",
        "requesting-code-review": "当你完成代码需要请求他人审查时",
        "receiving-code-review": "当你收到代码审查反馈需要处理时",
        "git-worktrees": "当你需要同时处理多个分支时，使用 Git worktree 并行开发",
        "verification": "当你在标记任务完成之前，需要验证所有工作是否正确",
        "verification-before-completion": "当你在标记任务完成之前，需要验证所有工作是否正确",
        "frontend": "当你开发前端应用时，提供前端开发模式和最佳实践",
        "backend": "当你开发后端服务时，提供后端架构模式和最佳实践",
        "security": "当你需要安全审查时，帮你检查代码中的安全漏洞",
        "security-review": "当你需要安全审查时，帮你检查代码中的安全漏洞",
        "continuous-learning": "当你在工作中需要持续学习和改进时",
        "agent": "当你需要创建子代理或代理系统时",
        "subagent": "当你需要创建和管理子代理任务时",
        "dispatching-parallel-agents": "当你有2+个独立任务需要并行处理时",
        "subagent-driven-development": "当你需要用子代理驱动开发时",
        "parallel": "当你有多个独立任务需要并行处理时",
        "ui-ux": "当你设计用户界面和用户体验时",
        "django": "当你使用 Django 框架开发时",
        "springboot": "当你使用 Spring Boot 框架开发时",
        "golang": "当你使用 Go 语言开发时",
        "python": "当你使用 Python 开发时",
        "rust": "当你使用 Rust 开发时",
        "kotlin": "当你使用 Kotlin 开发时",
        "swift": "当你使用 Swift 开发时",
        "postgres": "当你使用 PostgreSQL 数据库时",
        "docker": "当你使用 Docker 容器化时",
        "3d": "当你开发 3D 应用、游戏或可视化时",
        "threejs": "当你使用 Three.js 开发 3D Web 应用时",
        "api-design": "当你设计 API 时",
        "deployment": "当你部署应用时",
        "docker-patterns": "当你使用 Docker 构建和部署容器时",
        "writing-skills": "当你需要创建或编辑技能时",
        "finishing-a-development-branch": "当实现完成、测试通过，需要决定如何集成工作时",
        "using-superpowers": "当开始任何对话时，建立如何查找和使用技能",
        "browse": "当你需要浏览网页时",
        "qa": "当你需要质量保证测试时",
        "ship": "当你准备发布代码时",
        "design-review": "当你需要设计审查时",
        "design-consultation": "当你需要设计咨询时",
        "retro": "当你需要项目回顾时",
        "office-hours": "当你需要办公时间咨询时",
        "guard": "当你需要代码守护时",
        "find-skills": "当你想查找和安装技能时",
        "skill-creator": "当你需要创建新技能时",
    }

    scenarios_en = {
        "tdd": "Use when implementing any feature or bugfix, before writing implementation code",
        "test-driven-development": "Use when implementing any feature or bugfix, before writing implementation code",
        "debugging": "Use when encountering any bug, test failure, or unexpected behavior",
        "systematic-debugging": "Use when encountering any bug, test failure, or unexpected behavior",
        "brainstorming": "Use when starting a new project or needing creative exploration",
        "writing-plans": "Use when a task is complex enough to need structured planning",
        "executing-plans": "Use when you have a plan and need to execute it step by step",
        "code-review": "Use when code is complete and needs review",
        "verification": "Use before marking work complete to verify everything is correct",
        "frontend": "Use when developing frontend applications",
        "backend": "Use when developing backend services",
        "security": "Use when performing security reviews of code",
        "git-worktrees": "Use when you need to work on multiple branches simultaneously",
    }

    scenarios = scenarios_zh if locale.startswith("zh") else scenarios_en

    for key, scenario in scenarios.items():
        if key in name_lower:
            return scenario

    for key, scenario in scenarios.items():
        if key in desc_lower:
            return scenario

    if locale.startswith("zh"):
        if description:
            # Generate from description, truncate for table
            short_desc = description.split(".")[0].split("。")[0]
            if len(short_desc) > 80:
                short_desc = short_desc[:77] + "..."
            return f"当需要 {short_desc} 时使用"
        return "根据技能名称和描述判断适用场景"
    else:
        if description:
            short_desc = description.split(".")[0]
            if len(short_desc) > 80:
                short_desc = short_desc[:77] + "..."
            return f"Use when you need: {short_desc}"
        return "Refer to the skill name and description for usage scenarios"


def expand_search_keywords(keyword: str, locale: str) -> list[str]:
    """Expand a search keyword with translations for better matching.

    For example, searching '调试' (Chinese for 'debug') will also match
    skills containing 'debug', 'debugging', etc.
    """
    keywords = [keyword.lower()]

    if locale.startswith("zh"):
        # Add English equivalents for Chinese keywords
        for zh_term, en_terms in ZH_TO_EN_KEYWORDS.items():
            if zh_term in keyword:
                keywords.extend(en_terms)

    # Also add Chinese equivalents for English keywords
    for zh_term, en_terms in ZH_TO_EN_KEYWORDS.items():
        for en in en_terms:
            if en in keyword.lower():
                keywords.append(zh_term)

    return list(set(keywords))
