# Meta-Skill 🤖

> AI 编程助手技能发现与分析工具 / AI Coding Assistant Skills Discovery & Analysis Tool

**Meta-Skill** 扫描你的系统中所有已安装的 AI 编程助手技能（Claude Code、Codex、Cursor、OpenCode、Gemini 等），分析每个技能的功能，按来源分组，翻译为本地语言，并告诉你每个技能的用途和适用场景。

## 为什么需要 Meta-Skill？

如果你使用 AI 编程助手，你可能安装了几十个技能，但是：
- 🔤 技能说明全是英文，看不懂
- 📦 不知道哪些技能属于哪个应用（如 Superpowers、GStack、ECC）
- ❓ 不知道什么时候该调用哪个技能
- 🔍 难以发现新技能

**Meta-Skill** 帮你解决这些问题！

## 安装

### 方式1：一键安装脚本（推荐）

```bash
git clone https://github.com/jiangjie714/Meta-Skill.git
cd Meta-Skill
./scripts/install.sh
```

自动安装到 Claude Code、Codex、OpenCode、Gemini 的技能目录。

### 方式2：手动安装

**Claude Code:**
```bash
git clone https://github.com/jiangjie714/Meta-Skill.git
cp -r Meta-Skill/.claude/skills/meta-skill ~/.claude/skills/meta-skill
cp -r Meta-Skill/meta_skill ~/.claude/skills/meta-skill/meta_skill
```

**Codex:**
```bash
mkdir -p ~/.codex/skills/meta-skill
cp Meta-Skill/skills/meta-skill/SKILL.md ~/.codex/skills/meta-skill/
cp -r Meta-Skill/meta_skill ~/.codex/skills/meta-skill/meta_skill
```

**OpenCode:**
```bash
mkdir -p ~/.config/opencode/skills/meta-skill
cp Meta-Skill/.claude/skills/meta-skill/SKILL.md ~/.config/opencode/skills/meta-skill/
cp -r Meta-Skill/meta_skill ~/.config/opencode/skills/meta-skill/meta_skill
```

### 方式3：作为 Python 包使用

```bash
cd Meta-Skill
pip install -e .
meta-skill --locale zh_CN --unique
```

### 卸载

```bash
./scripts/uninstall.sh
```

## 使用方法

### 在 AI 编程助手中使用

安装后，直接向 AI 助手提问：

```
我安装了哪些技能？
superpowers 里面有什么技能？
什么是 TDD 技能？什么时候该用它？
帮我找调试相关的技能
用中文告诉我有哪些前端技能？
```

AI 助手会自动调用 Meta-Skill 扫描并展示结果。

### 命令行使用

```bash
# 扫描所有技能（自动检测系统语言，中文系统默认中文输出）
python3 -m meta_skill.cli

# 使用简体中文输出
python3 -m meta_skill.cli --locale zh_CN

# 去重（同一技能名称只保留一条）
python3 -m meta_skill.cli --unique

# 搜索技能（支持中文关键词！）
python3 -m meta_skill.cli --search 调试
python3 -m meta_skill.cli --search tdd

# 按应用过滤
python3 -m meta_skill.cli --app superpowers

# JSON 格式输出
python3 -m meta_skill.cli --format json

# 保存到文件
python3 -m meta_skill.cli --output report.md
```

### Python API

```python
from meta_skill.scanner import scan_all_skills
from meta_skill.report import generate_markdown_report, generate_json_report

skills = scan_all_skills()
report = generate_markdown_report(skills, locale="zh_CN")
json_data = generate_json_report(skills, locale="zh_CN")
```

## 扫描范围

| 工具 | 扫描路径 |
|------|----------|
| Claude Code | `~/.claude/skills/` |
| Claude Code 插件 | `~/.claude/plugins/marketplaces/*/` |
| Cursor | `~/.cursor/skills-cursor/` |
| OpenCode | `~/.config/opencode/skills/` |
| Gemini | `~/.gemini/antigravity/skills/` |
| Trae | `~/.trae-cn/builtin/` |
| CherryStudio | `~/Library/Application Support/CherryStudio/Data/Skills/` |

## 示例输出

```
# 🤖 AI 编程助手技能全景图

> 自动检测系统语言：**简体中文** | 扫描时间：2026-06-01
> 共发现 **251** 个技能，来自 **13** 个来源

## 📦 Superpowers 超能力集

| # | 技能名称 | 中文名称 | 说明 | 适用场景 |
|---|---------|---------|------|---------|
| 1 | `test-driven-development` | 测试驱动开发 | ... | 当你在编写新功能或修复 Bug 时 |
| 2 | `systematic-debugging` | 系统化调试 | ... | 当你遇到 Bug 或测试失败时 |
| 3 | `brainstorming` | 头脑风暴 | ... | 当你开始新项目时 |
```

## 特性

- 🔍 **多工具扫描**：发现 Claude Code、Codex、Cursor、OpenCode、Gemini、Trae、CherryStudio 的技能
- 🌍 **自动语言检测**：检测系统语言（macOS AppleLocale、LANG、LC_ALL）
- 🇨🇳 **中文翻译**：内置 100+ 术语和适用场景的中文字典
- 🔎 **中英搜索**：搜索"调试"可找到 debug、debugging、investigate 等技能
- 📊 **分组报告**：按来源应用分组，附带统计信息
- 🔄 **去重**：`--unique` 标志移除不同来源的重复技能
- 📋 **多格式**：Markdown 报告和 JSON 编程接口
- 🚀 **零依赖**：纯 Python，无需外部包

## 项目结构

```
Meta-Skill/
├── .claude-plugin/plugin.json   # Claude Code 插件配置
├── .codex-plugin/plugin.json    # Codex 插件配置
├── .claude/skills/meta-skill/   # Claude Code 技能定义
├── skills/meta-skill/           # Codex/OpenCode 技能定义
├── meta_skill/                  # Python 核心模块
│   ├── __init__.py
│   ├── scanner.py               # 文件系统扫描器
│   ├── translator.py            # 翻译/本地化模块
│   ├── report.py                # 报告生成器
│   └── cli.py                   # 命令行入口
├── scripts/
│   ├── install.sh               # 一键安装脚本
│   └── uninstall.sh             # 卸载脚本
├── SKILL.md                     # 项目级技能定义
├── CLAUDE.md                    # Claude Code 指令
├── AGENTS.md                    # 开发指南
└── pyproject.toml               # Python 包配置
```

## 支持的语言

- **zh_CN / zh_TW** — 完整中文翻译，100+ 术语字典
- **en_US** — 英语（默认）
- 其他语言回退到英语，部分翻译

## License

MIT
