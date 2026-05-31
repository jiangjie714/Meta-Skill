#!/usr/bin/env bash
# Meta-Skill Installer v0.4.0
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

HOME_DIR="$HOME"
BIN_DIR="$HOME_DIR/.local/bin"
CACHE_DIR="$HOME_DIR/.meta-skill"

echo -e "${BLUE}🔍 Meta-Skill — AI 编程助手技能发现与安装工具 v0.4.0${NC}"
echo ""

# ─── Ensure cache directory exists ───────────────────────
mkdir -p "$CACHE_DIR"
echo -e "${GREEN}✅ Cache directory: $CACHE_DIR${NC}"

# ─── Install ms command ───────────────────────────────
mkdir -p "$BIN_DIR"
echo -e "${YELLOW}📦 Installing ms command...${NC}"
cp "$PROJECT_DIR/scripts/ms" "$BIN_DIR/ms"
chmod +x "$BIN_DIR/ms"

if echo ":$PATH:" | grep -q ":$BIN_DIR:"; then
    echo -e "${GREEN}✅ ms command installed to: $BIN_DIR/ms${NC}"
else
    echo -e "${YELLOW}⚠️  $BIN_DIR is not in PATH. Adding it...${NC}"
    SHELL_RC="$HOME_DIR/.zshrc"
    [ ! -f "$SHELL_RC" ] && SHELL_RC="$HOME_DIR/.bashrc"
    if ! grep -q "$BIN_DIR" "$SHELL_RC" 2>/dev/null; then
        echo "" >> "$SHELL_RC"
        echo "# Meta-Skill" >> "$SHELL_RC"
        echo "export PATH=\"$BIN_DIR:\$PATH\"" >> "$SHELL_RC"
        echo -e "${GREEN}✅ Added $BIN_DIR to PATH in $SHELL_RC${NC}"
        echo -e "${YELLOW}   Run: source $SHELL_RC  (or restart terminal)${NC}"
    fi
    export PATH="$BIN_DIR:$PATH"
fi

# ─── Helper: Install skill for a tool ────────────────
install_for_tool() {
    local tool_name="$1"
    local target="$2"
    local src_skill="$PROJECT_DIR/skills/meta-skill"

    echo -e "${YELLOW}📦 Installing for $tool_name...${NC}"
    rm -rf "$target" 2>/dev/null
    mkdir -p "$target"

    # Copy SKILL.md (cache-first version)
    cp "$PROJECT_DIR/SKILL.md" "$target/SKILL.md"

    # Copy meta_skill Python module (self-contained)
    mkdir -p "$target/meta_skill"
    cp "$PROJECT_DIR/meta_skill/__init__.py" "$target/meta_skill/"
    cp "$PROJECT_DIR/meta_skill/scanner.py" "$target/meta_skill/"
    cp "$PROJECT_DIR/meta_skill/translator.py" "$target/meta_skill/"
    cp "$PROJECT_DIR/meta_skill/report.py" "$target/meta_skill/"
    cp "$PROJECT_DIR/meta_skill/cache.py" "$target/meta_skill/"
    cp "$PROJECT_DIR/meta_skill/cli.py" "$target/meta_skill/"

    # Copy ms script
    mkdir -p "$target/scripts"
    cp "$PROJECT_DIR/scripts/ms" "$target/scripts/ms"
    chmod +x "$target/scripts/ms"

    echo -e "${GREEN}✅ $tool_name skill installed to: $target${NC}"
}

# ─── Install for each tool ────────────────────────────
install_for_tool "Claude Code" "$HOME_DIR/.claude/skills/meta-skill"

if [ -d "$HOME_DIR/.codex" ]; then
    install_for_tool "Codex" "$HOME_DIR/.codex/skills/meta-skill"
else
    echo -e "${YELLOW}⏭️  Codex directory not found, skipping${NC}"
fi

if [ -d "$HOME_DIR/.config/opencode" ]; then
    install_for_tool "OpenCode" "$HOME_DIR/.config/opencode/skills/meta-skill"
else
    echo -e "${YELLOW}⏭️  OpenCode directory not found, skipping${NC}"
fi

if [ -d "$HOME_DIR/.gemini" ]; then
    install_for_tool "Gemini" "$HOME_DIR/.gemini/antigravity/skills/meta-skill"
else
    echo -e "${YELLOW}⏭️  Gemini directory not found, skipping${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Installation complete!${NC}"
echo ""
echo -e "${BLUE}Quick Start:${NC}"
echo -e "  ${GREEN}ms${NC}              显示缓存摘要（从缓存读取 ⚡）"
echo -e "  ${GREEN}ms gstack${NC}       查看 GStack 技能详情"
echo -e "  ${GREEN}ms superpowers${NC}   查看 Superpowers 技能详情"
echo -e "  ${GREEN}ms search 调试${NC}   搜索调试相关技能"
echo -e "  ${GREEN}ms --refresh${NC}    重新扫描更新缓存"
echo ""
echo -e "${BLUE}Cache-First Design:${NC}"
echo -e "  缓存文件: ${GREEN}~/.meta-skill/cache.json${NC}"
echo -e "  首次使用运行 ${GREEN}ms --refresh${NC} 创建缓存"
echo -e "  之后所有查询从缓存读取，秒级响应 ⚡"
echo ""
echo -e "${BLUE}In AI assistants (Codex/Claude Code):${NC}"
echo -e "  技能会自动读取缓存文件，无需运行命令"
