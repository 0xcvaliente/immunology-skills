#!/usr/bin/env bash
# Install the skills in this repository into ~/.claude/skills.
#
#   ./install.sh           copy each skill (re-run after a git pull)
#   ./install.sh --link    symlink each skill to this clone instead
#   ./install.sh --dry-run say what would change, change nothing
#
# Only directories here that contain a SKILL.md are touched. An installed directory with
# the same name that differs from this repository is moved to a backup folder outside the
# skills directory first (a backup inside it would be loaded as a second copy of the skill).
# Environment: CLAUDE_SKILLS_DIR (default ~/.claude/skills), CLAUDE_SKILLS_BACKUP_DIR
# (default ~/.claude/skills-backups).
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
dest="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
backups="${CLAUDE_SKILLS_BACKUP_DIR:-$HOME/.claude/skills-backups}"
mode=copy
dry=0
for arg in "$@"; do
  case "$arg" in
    --link) mode=link ;;
    --dry-run) dry=1 ;;
    -h|--help) sed -n '2,11p' "$0"; exit 0 ;;
    *) echo "unknown option: $arg" >&2; exit 2 ;;
  esac
done

run() { if [ "$dry" = 1 ]; then echo "  would: $*"; else "$@"; fi; }

copy_skill() {  # source dir, target dir
  if command -v rsync >/dev/null 2>&1; then
    run rsync -a --exclude '__pycache__' --exclude '.DS_Store' "$1/" "$2/"
  else
    run cp -R "$1" "$2"
    [ "$dry" = 1 ] || find "$2" \( -name __pycache__ -o -name .DS_Store \) -prune -exec rm -rf {} +
  fi
}

run mkdir -p "$dest"
stamp="$(date +%Y%m%d-%H%M%S)"
count=0

for skill in "$here"/*/; do
  skill="${skill%/}"
  name="$(basename "$skill")"
  [ -f "$skill/SKILL.md" ] || continue
  target="$dest/$name"
  echo "$name"
  if [ -L "$target" ]; then
    run rm "$target"
  elif [ -e "$target" ]; then
    if diff -rq -x __pycache__ -x .DS_Store "$skill" "$target" >/dev/null 2>&1; then
      echo "  identical copy already installed"
    else
      echo "  installed copy differs from the repository: backing up to $backups/$name-$stamp"
      run mkdir -p "$backups"
      run mv "$target" "$backups/$name-$stamp"
    fi
    [ -e "$target" ] && run rm -rf "$target"
  fi
  if [ "$mode" = link ]; then
    run ln -s "$skill" "$target"
    echo "  linked"
  else
    copy_skill "$skill" "$target"
    echo "  copied"
  fi
  count=$((count + 1))
done

echo "$count skill(s) -> $dest ($mode$([ "$dry" = 1 ] && echo ', dry run'))"
