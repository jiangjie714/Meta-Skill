#!/usr/bin/env bash
# Meta-Skill Uninstaller
set -e

HOME_DIR="$HOME"

echo "🔍 Uninstalling Meta-Skill..."

# Remove from Claude Code
rm -rf "$HOME_DIR/.claude/skills/meta-skill" 2>/dev/null && echo "✅ Removed from Claude Code" || echo "⏭️  Not found in Claude Code"

# Remove from Codex
rm -rf "$HOME_DIR/.codex/skills/meta-skill" 2>/dev/null && echo "✅ Removed from Codex" || echo "⏭️  Not found in Codex"

# Remove from OpenCode
rm -rf "$HOME_DIR/.config/opencode/skills/meta-skill" 2>/dev/null && echo "✅ Removed from OpenCode" || echo "⏭️  Not found in OpenCode"

# Remove from Gemini
rm -rf "$HOME_DIR/.gemini/antigravity/skills/meta-skill" 2>/dev/null && echo "✅ Removed from Gemini" || echo "⏭️  Not found in Gemini"

echo ""
echo "🎉 Meta-Skill has been uninstalled."
