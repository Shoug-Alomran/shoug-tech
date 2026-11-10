#!/bin/bash
# SessionStart hook: record which academic pages' sidebars ALREADY drift from
# scripts/academic-sidebar.json, so validate-site.sh only blames drift that
# this session introduced (190 pages drift at the time of writing).
#
# SessionStart also fires on resume and compaction with the same session id;
# the first baseline is kept so drift made before a compaction is still caught.

set -uo pipefail

event=$(cat)
repo="${CLAUDE_PROJECT_DIR:-$(pwd)}"
session=$(printf '%s' "$event" | jq -r '.session_id // empty' 2>/dev/null)
baseline="${TMPDIR:-/tmp}/claude-sidebar-baseline-${session:-nosession}"

[ -f "$baseline" ] && exit 0
cd "$repo" || exit 0

python3 scripts/build_academic_sidebar.py --check 2>/dev/null \
  | sed -n 's/^stale: //p' | sort > "$baseline"
exit 0
