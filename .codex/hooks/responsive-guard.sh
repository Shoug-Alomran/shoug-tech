#!/bin/bash
# Stop hook: HTML pages changed in this session must use the available space on
# laptop, iPad and iPhone widths -- no sideways scrolling, no wide empty gutters,
# no paragraphs capped to a sliver of their column, no wasted phone padding.
#
# Runs scripts/check_responsive_layout.py on standalone pages under docs/ that
# differ from HEAD and were modified after this session started (the
# SessionStart hook touches the marker). Without a marker it checks every
# changed page. index.html wrappers are skipped: their layout is the shared
# site chrome.
#
# Usage:
#   responsive-guard.sh           Stop hook (reads the event on stdin)
#   responsive-guard.sh --start   SessionStart hook: record the session marker
#
# Exit 2 hands the findings back to Claude to fix.

set -uo pipefail

event=$(cat)
repo="${CLAUDE_PROJECT_DIR:-$(pwd)}"
session=$(printf '%s' "$event" | sed -n 's/.*"session_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
marker="${TMPDIR:-/tmp}/claude-responsive-start-${session:-nosession}"

if [ "${1:-}" = "--start" ]; then
  touch "$marker"
  exit 0
fi

# Already inside a Stop-hook-triggered continuation: don't loop.
if printf '%s' "$event" | grep -q '"stop_hook_active"[[:space:]]*:[[:space:]]*true'; then
  exit 0
fi

cd "$repo" || exit 0
py="$repo/.venv/bin/python"
[ -x "$py" ] || exit 0

args=(--changed --limit 8)
[ -f "$marker" ] && args+=(--newer "$marker")

if out=$("$py" scripts/check_responsive_layout.py "${args[@]}" 2>&1); then
  exit 0
fi

{
  echo "Responsive layout check failed for pages changed in this session."
  echo "Pages must use the free space on laptop, iPad and iPhone widths (fix the page or its stylesheet, then re-run"
  echo ".venv/bin/python scripts/check_responsive_layout.py <page>):"
  printf '%s\n' "$out" | tail -60
} >&2
exit 2
