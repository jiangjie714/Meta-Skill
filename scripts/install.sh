#!/usr/bin/env bash
# Meta-Skill Installer v0.3.0
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

echo -e "${BLUE}🔍 Meta-Skill — AI 编程助手技能发现与安装工具 v0.3.0${NC}"
echo ""

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

    # Copy SKILL.md
    cp "$src_skill/SKILL.md" "$target/SKILL.md"

    # Copy meta_skill Python module (self-contained)
    mkdir -p "$target/meta_skill"
    cp "$PROJECT_DIR/meta_skill/__init__.py" "$target/meta_skill/"
    cp "$PROJECT_DIR/meta_skill/scanner.py" "$target/meta_skill/"
    cp "$PROJECT_DIR/meta_skill/translator.py" "$target/meta_skill/"
    cp "$PROJECT_DIR/meta_skill/report.py" "$target/meta_skill/"
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
echo -e "${BLUE}Usage:${NC}"
echo -e "  ${GREEN}ms${NC}                  扫描所有技能（自动中文）"
echo -e "  ${GREEN}ms zh${NC}               中文输出"
echo -e "  ${GREEN}ms en${NC}               英文输出"
echo -e "  ${GREEN}ms superpowers${NC}       只看 superpowers 的技能"
echo -e "  ${GREEN}ms search 调试${NC}       搜索调试相关技能"
echo -e "  ${GREEN}ms json${NC}             JSON 格式输出"
echo -e "  ${GREEN}ms -o report.md${NC}     保存到文件"
echo ""
echo -e "${BLUE}In Codex, you can also install via:${NC}"
echo -e "  ${GREEN}python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \\${NC}"
echo -e "  ${GREEN}  --repo jiangjie714/Meta-Skill --path skills/meta-skill${NC}"
