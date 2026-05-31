#!/usr/bin/env bash
# Meta-Skill Installer
# Installs Meta-Skill as a skill for Claude Code, Codex, and other AI tools
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔍 Meta-Skill — AI 编程助手技能发现与安装工具${NC}"
echo ""

# Detect home directory
HOME_DIR="$HOME"

# Install for Claude Code
install_claude_code() {
    local target="$HOME_DIR/.claude/skills/meta-skill"
    echo -e "${YELLOW}📦 Installing for Claude Code...${NC}"

    mkdir -p "$target"
    cp "$PROJECT_DIR/.claude/skills/meta-skill/SKILL.md" "$target/SKILL.md"

    # Also copy the Python module
    mkdir -p "$target/meta_skill"
    cp "$PROJECT_DIR/meta_skill/__init__.py" "$target/meta_skill/"
    cp "$PROJECT_DIR/meta_skill/scanner.py" "$target/meta_skill/"
    cp "$PROJECT_DIR/meta_skill/translator.py" "$target/meta_skill/"
    cp "$PROJECT_DIR/meta_skill/report.py" "$target/meta_skill/"
    cp "$PROJECT_DIR/meta_skill/cli.py" "$target/meta_skill/"

    echo -e "${GREEN}✅ Claude Code skill installed to: $target${NC}"
}

# Install for Codex
install_codex() {
    local target="$HOME_DIR/.codex/skills/meta-skill"
    echo -e "${YELLOW}📦 Installing for Codex...${NC}"

    if [ -d "$HOME_DIR/.codex" ]; then
        mkdir -p "$target"
        cp "$PROJECT_DIR/skills/meta-skill/SKILL.md" "$target/SKILL.md"

        # Also copy the Python module
        mkdir -p "$target/meta_skill"
        cp "$PROJECT_DIR/meta_skill/__init__.py" "$target/meta_skill/"
        cp "$PROJECT_DIR/meta_skill/scanner.py" "$target/meta_skill/"
        cp "$PROJECT_DIR/meta_skill/translator.py" "$target/meta_skill/"
        cp "$PROJECT_DIR/meta_skill/report.py" "$target/meta_skill/"
        cp "$PROJECT_DIR/meta_skill/cli.py" "$target/meta_skill/"

        echo -e "${GREEN}✅ Codex skill installed to: $target${NC}"
    else
        echo -e "${YELLOW}⏭️  Codex directory not found, skipping${NC}"
    fi
}

# Install for OpenCode
install_opencode() {
    local target="$HOME_DIR/.config/opencode/skills/meta-skill"
    echo -e "${YELLOW}📦 Installing for OpenCode...${NC}"

    if [ -d "$HOME_DIR/.config/opencode" ]; then
        mkdir -p "$target"
        cp "$PROJECT_DIR/.claude/skills/meta-skill/SKILL.md" "$target/SKILL.md"

        mkdir -p "$target/meta_skill"
        cp "$PROJECT_DIR/meta_skill/__init__.py" "$target/meta_skill/"
        cp "$PROJECT_DIR/meta_skill/scanner.py" "$target/meta_skill/"
        cp "$PROJECT_DIR/meta_skill/translator.py" "$target/meta_skill/"
        cp "$PROJECT_DIR/meta_skill/report.py" "$target/meta_skill/"
        cp "$PROJECT_DIR/meta_skill/cli.py" "$target/meta_skill/"

        echo -e "${GREEN}✅ OpenCode skill installed to: $target${NC}"
    else
        echo -e "${YELLOW}⏭️  OpenCode directory not found, skipping${NC}"
    fi
}

# Install for Gemini
install_gemini() {
    local target="$HOME_DIR/.gemini/antigravity/skills/meta-skill"
    echo -e "${YELLOW}📦 Installing for Gemini...${NC}"

    if [ -d "$HOME_DIR/.gemini" ]; then
        mkdir -p "$target"
        cp "$PROJECT_DIR/.claude/skills/meta-skill/SKILL.md" "$target/SKILL.md"

        mkdir -p "$target/meta_skill"
        cp "$PROJECT_DIR/meta_skill/__init__.py" "$target/meta_skill/"
        cp "$PROJECT_DIR/meta_skill/scanner.py" "$target/meta_skill/"
        cp "$PROJECT_DIR/meta_skill/translator.py" "$target/meta_skill/"
        cp "$PROJECT_DIR/meta_skill/report.py" "$target/meta_skill/"
        cp "$PROJECT_DIR/meta_skill/cli.py" "$target/meta_skill/"

        echo -e "${GREEN}✅ Gemini skill installed to: $target${NC}"
    else
        echo -e "${YELLOW}⏭️  Gemini directory not found, skipping${NC}"
    fi
}

# Main
echo -e "${BLUE}This will install Meta-Skill as a skill for your AI coding tools.${NC}"
echo ""

install_claude_code
install_codex
install_opencode
install_gemini

echo ""
echo -e "${GREEN}🎉 Installation complete!${NC}"
echo ""
echo -e "Usage in Claude Code / Codex / OpenCode:"
echo -e "  ${BLUE}python3 -m meta_skill.cli --locale zh_CN --unique${NC}"
echo ""
echo -e "Or invoke the skill:"
echo -e "  ${BLUE}我安装了哪些技能？${NC}"
echo -e "  ${BLUE}superpowers 里面有什么技能？${NC}"
echo -e "  ${BLUE}What does the TDD skill do?${NC}"
echo ""
echo -e "For more options: ${BLUE}python3 -m meta_skill.cli --help${NC}"
