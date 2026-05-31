"""CLI entry point for Meta-Skill with caching support."""

import argparse
import sys
import time
from pathlib import Path

from .scanner import scan_all_skills
from .translator import detect_locale, get_language_name
from .report import generate_markdown_report, generate_json_report
from .cache import (
    save_cache, load_cache, is_cache_fresh, get_cache_age,
    format_cache_summary, format_cache_app, format_cache_search,
    _dict_to_skill,
)

CACHE_TTL = 86400  # 24 hours


def do_scan(locale, unique, quiet, is_zh):
    """Perform a full scan and save to cache."""
    if not quiet:
        if is_zh:
            print("🔍 正在扫描系统中的 AI 编程助手技能...")
            print(f"   检测语言: {get_language_name(locale)} ({locale})")
        else:
            print("🔍 Scanning for AI coding assistant skills...")
            print(f"   Detected locale: {get_language_name(locale)} ({locale})")

    skills = scan_all_skills()

    if not quiet:
        if is_zh:
            print(f"   发现 {len(skills)} 个技能（去重前）")
        else:
            print(f"   Found {len(skills)} skills (before dedup)")

    if unique:
        seen_names = set()
        unique_skills = []
        for skill in skills:
            if skill.name not in seen_names:
                seen_names.add(skill.name)
                unique_skills.append(skill)
        skills = unique_skills

    cache_file = save_cache(skills, locale)
    if not quiet:
        if is_zh:
            print(f"   💾 缓存已保存到 {cache_file}")
        else:
            print(f"   💾 Cache saved to {cache_file}")

    return skills


def main():
    parser = argparse.ArgumentParser(
        prog="meta-skill",
        description="🔍 AI 编程助手技能发现与分析工具（支持缓存）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例 / Examples:
  ms                        显示缓存摘要（秒级响应 ⚡）
  ms gstack                  查看 GStack 技能详情（从缓存）
  ms search 调试             搜索技能（从缓存，支持中文）
  ms --refresh               重新扫描更新缓存
  ms --scan                  强制重新扫描
  ms --locale zh_CN --scan   重新扫描并切换语言
  ms json --scan             JSON 格式输出（需 --scan）
  ms -o report.md --scan     保存报告到文件
        """,
    )

    parser.add_argument("--locale", "-l", default=None, help="输出语言")
    parser.add_argument("--format", "-f", choices=["markdown", "md", "json"], default="markdown", help="输出格式")
    parser.add_argument("--output", "-o", default=None, help="输出文件路径")
    parser.add_argument("--app", "-a", default=None, help="只显示指定应用的技能")
    parser.add_argument("--search", "-s", default=None, help="搜索技能（支持中英文）")
    parser.add_argument("--unique", "-u", action="store_true", help="去重")
    parser.add_argument("--quiet", "-q", action="store_true", help="静默模式")
    parser.add_argument("--refresh", "-r", action="store_true", help="重新扫描更新缓存")
    parser.add_argument("--scan", action="store_true", help="强制重新扫描")

    args = parser.parse_args()
    locale = args.locale or detect_locale()
    is_zh = locale.startswith("zh")
    force_scan = args.refresh or args.scan

    # ─── Force re-scan ────────────────────────────────────────────
    if force_scan:
        skills = do_scan(locale, args.unique, args.quiet, is_zh)

        if args.format in ("json",):
            output_path = Path(args.output) if args.output else None
            result = generate_json_report(skills, locale, output_path)
            if not output_path:
                print(result)
            else:
                print(f"✅ 报告已保存到: {output_path}" if is_zh else f"✅ Report saved to: {output_path}")
        elif args.output:
            result = generate_markdown_report(skills, locale, Path(args.output))
            print(f"✅ 报告已保存到: {args.output}" if is_zh else f"✅ Report saved to: {args.output}")
        return

    # ─── Load cache (fast path) ─────────────────────────────────
    cache_data = load_cache(max_age=0)  # Accept any age
    if cache_data is None:
        if is_zh:
            print("⚠️  没有缓存数据，正在执行首次扫描...")
        else:
            print("⚠️  No cache data. Running initial scan...")
        do_scan(locale, args.unique, args.quiet, is_zh)
        cache_data = load_cache(max_age=0)

    if cache_data is None:
        if is_zh:
            print("❌ 扫描失败，请检查安装")
        else:
            print("❌ Scan failed. Please check installation.")
        sys.exit(1)

    # ─── Search from cache ───────────────────────────────────────
    if args.search:
        print(format_cache_search(cache_data, args.search, locale))
        return

    # ─── App filter from cache ──────────────────────────────────
    if args.app:
        print(format_cache_app(cache_data, args.app.lower(), locale))
        return

    # ─── Default: show cache summary ────────────────────────────
    print(format_cache_summary(cache_data, locale))


if __name__ == "__main__":
    main()
