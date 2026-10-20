#!/bin/sh
# ContentSCALE OS: install from the downloaded GitHub ZIP (no plugin needed).
# Usage: sh install.sh            (run from the unzipped folder)
# Copies skills to ~/.claude/skills, the quality agent to ~/.claude/agents,
# the /contentscale and /cs-status commands to ~/.claude/commands, then sets up tools.
# Existing folders with the same names are moved to ~/.claude/skills/.backup-<date>/ first.
set -e
SRC="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/.claude"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP="$DEST/skills/.backup-$STAMP"

[ -d "$SRC/skills/cs-pipeline" ] || { echo "Run this from the unzipped ContentSCALE folder (skills/cs-pipeline not found)."; exit 1; }
mkdir -p "$DEST/skills" "$DEST/agents" "$DEST/commands"

n=0
for d in "$SRC"/skills/*/; do
  name="$(basename "$d")"
  if [ -e "$DEST/skills/$name" ]; then
    mkdir -p "$BACKUP"
    mv "$DEST/skills/$name" "$BACKUP/$name"
  fi
  cp -R "$d" "$DEST/skills/$name"
  n=$((n+1))
done
cp "$SRC"/agents/*.md "$DEST/agents/"
cp "$SRC"/commands/*.md "$DEST/commands/"
echo "Installed $n skills to $DEST/skills, agent cs-quality-reviewer, commands /contentscale and /cs-status."
[ -d "$BACKUP" ] && echo "Previous versions of same-named skills saved in $BACKUP"

if command -v claude >/dev/null 2>&1 && claude plugin list 2>/dev/null | grep -q "contentscale@"; then
  echo "NOTE: the contentscale plugin is also installed. Remove one copy to avoid duplicates:"
  echo "      claude plugin uninstall contentscale@contentscale"
fi

if ! command -v ffmpeg >/dev/null 2>&1 || ! command -v yt-dlp >/dev/null 2>&1; then
  echo "NOTE: install video tools once: brew install yt-dlp ffmpeg"
fi
[ -n "$CS_SKIP_SETUP" ] || sh "$DEST/skills/cs-pipeline/scripts/setup.sh" || echo "NOTE: tool setup did not finish; run again: sh $DEST/skills/cs-pipeline/scripts/setup.sh"
echo ""
echo "One more step for Instagram research (once per computer):"
echo "  1. Install the Sort Feed extension in Chrome (sortfeed.com) and sign in with the team Pro account."
echo "  2. Be signed in to Instagram in that Chrome."
echo "  3. In Claude: + > Connectors > make sure SortFeed is on, then open a NEW session."
echo "Without it the skill still works (slower Instagram via Chrome scrolling)."
echo "Done. Restart Claude Code, then type: /contentscale <client name>"
