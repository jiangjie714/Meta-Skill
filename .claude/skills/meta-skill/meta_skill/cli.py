"""CLI entry point for Meta-Skill."""

import argparse
import sys
from pathlib import Path

from .scanner import scan_all_skills
from .translator import detect_locale, get_language_name, expand_search_keywords
from .report import generate_markdown_report, generate_json_report


def main():
    parser = argparse.ArgumentParser(
        prog="meta-skill",
        description="🔍 AI 编程助手技能发现与分析工具 / AI Coding Assistant Skills Discovery & Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例 / Examples:
  meta-skill                        # 自动检测语言并扫描所有技能
  meta-skill --locale zh_CN         # 使用简体中文输出
  meta-skill --locale en_US         # 使用英语输出
  meta-skill --format json          # 输出 JSON 格式
  meta-skill --output report.md     # 保存到文件
  meta-skill --app superpowers      # 只显示某个应用的技能
  meta-skill --search tdd           # 搜索包含关键词的技能
  meta-skill --search 调试           # 支持中文搜索（自动映射到英文关键词）
  meta-skill --unique               # 去重：同一技能名称只保留一条
        """,
    )

    parser.add_argument(
        "--locale", "-l",
        default=None,
        help="输出语言 (默认自动检测系统语言) / Output locale (default: auto-detect)"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["markdown", "md", "json"],
        default="markdown",
        help="输出格式 (markdown/json) / Output format (default: markdown)"
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="输出文件路径 / Output file path"
    )
    parser.add_argument(
        "--app", "-a",
        default=None,
        help="只显示指定应用的技能 / Filter by application name"
    )
    parser.add_argument(
        "--search", "-s",
        default=None,
        help="搜索技能（支持中英文关键词）/ Search skills by keyword (supports CJK)"
    )
    parser.add_argument(
        "--unique", "-u",
        action="store_true",
        help="去重：同一技能名称只保留一条 / Deduplicate by skill name"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="静默模式，只输出结果 / Quiet mode, only output results"
    )

    args = parser.parse_args()

    locale = args.locale or detect_locale()
    lang_name = get_language_name(locale)
    is_zh = locale.startswith("zh")

    if not args.quiet:
        if is_zh:
            print(f"🔍 正在扫描系统中的 AI 编程助手技能...")
            print(f"   检测语言: {lang_name} ({locale})")
        else:
            print(f"🔍 Scanning for AI coding assistant skills...")
            print(f"   Detected locale: {lang_name} ({locale})")

    skills = scan_all_skills()

    if not args.quiet:
        if is_zh:
            print(f"   发现 {len(skills)} 个技能（去重前）")
        else:
            print(f"   Found {len(skills)} skills (before dedup)")

    # Deduplicate by name if requested
    if args.unique:
        seen_names = set()
        unique_skills = []
        for skill in skills:
            if skill.name not in seen_names:
                seen_names.add(skill.name)
                unique_skills.append(skill)
        skills = unique_skills
        if not args.quiet:
            if is_zh:
                print(f"   去重后剩余 {len(skills)} 个技能")
            else:
                print(f"   {len(skills)} skills after dedup")

    # Filter by app
    if args.app:
        app_lower = args.app.lower()
        skills = [s for s in skills if app_lower in s.source_app.lower()]
        if not args.quiet:
            if is_zh:
                print(f"   筛选应用 '{args.app}' 后剩余 {len(skills)} 个技能")
            else:
                print(f"   After filtering by '{args.app}': {len(skills)} skills")

    # Search by keyword (with CJK expansion)
    if args.search:
        keywords = expand_search_keywords(args.search, locale)
        skills = [
            s for s in skills
            if any(kw in s.name.lower() or kw in s.description.lower() for kw in keywords)
        ]
        if not args.quiet:
            if is_zh:
                print(f"   搜索关键词 '{args.search}' 后剩余 {len(skills)} 个技能")
            else:
                print(f"   After searching '{args.search}': {len(skills)} skills")

    if not skills:
        if is_zh:
            print("❌ 未找到匹配的技能")
        else:
            print("❌ No matching skills found")
        sys.exit(0)

    # Generate report
    output_path = Path(args.output) if args.output else None

    if args.format in ("json",):
        result = generate_json_report(skills, locale, output_path)
        if not output_path:
            print(result)
    else:
        result = generate_markdown_report(skills, locale, output_path)
        if not output_path:
            print(result)

    if output_path:
        if is_zh:
            print(f"✅ 报告已保存到: {output_path}")
        else:
            print(f"✅ Report saved to: {output_path}")


if __name__ == "__main__":
    main()
