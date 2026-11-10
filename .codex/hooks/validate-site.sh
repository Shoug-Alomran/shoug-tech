#!/bin/bash
# Stop hook: catch broken site state before the turn ends instead of in a red
# build after push.
#
#   1. Routes + internal links (the read-only validators from
#      .github/workflows/deploy-mkdocs.yml) -- only when this session edited a
#      page under docs/ (check-html.py drops a marker file). Links to pages that
#      merely aren't committed yet are ignored here; CI still checks them.
#   2. Resource embeds: embed_resources.py --check (activities/labs/tutorials
#      dropped in but never embedded). Always runs; ~0.1s.
#   3. Sidebar drift: build_academic_sidebar.py --check, compared against the
#      baseline sidebar-baseline.sh recorded at session start, so only pages
#      this session knocked out of sync count. Skipped without a baseline.
#
# Deliberately excludes check_seo_metadata.py: it only passes after
# optimize_site_html.py has injected canonical/OG tags, and that build step
# REWRITES every page under docs/. A hook must not mutate the working tree.
#
# Exit 2 hands the failures back to Claude to fix.

set -uo pipefail

event=$(cat)
repo="${CLAUDE_PROJECT_DIR:-$(pwd)}"

# Already inside a Stop-hook-triggered continuation: don't loop.
if printf '%s' "$event" | grep -q '"stop_hook_active"[[:space:]]*:[[:space:]]*true'; then
  exit 0
fi

session=$(printf '%s' "$event" | sed -n 's/.*"session_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
tmp="${TMPDIR:-/tmp}"
marker="$tmp/claude-site-dirty-${session:-nosession}"
baseline="$tmp/claude-sidebar-baseline-${session:-nosession}"

cd "$repo" || exit 0
report=""

if [ -f "$marker" ]; then
  if out=$(python3 scripts/verify_site_routes.py 2>&1 &&
           SITE_LINKS_IGNORE_UNTRACKED=1 python3 scripts/check_site_links.py 2>&1); then
    rm -f "$marker"
  else
    report+="Routes/links (the same checks CI runs on push):"$'\n'
    report+="$(printf '%s\n' "$out" | tail -40)"$'\n\n'
  fi
fi

if ! embed=$(python3 scripts/embed_resources.py --check 2>&1); then
  report+="Resource files are not embedded -- run python3 scripts/embed_resources.py:"$'\n'
  report+="$(printf '%s\n' "$embed" | grep '^stale:' | head -20)"$'\n\n'
fi

if [ -f "$baseline" ]; then
  new=$(python3 scripts/build_academic_sidebar.py --check 2>/dev/null \
          | sed -n 's/^stale: //p' | sort | comm -13 "$baseline" -)
  if [ -n "$new" ]; then
    report+="Sidebars drifted from scripts/academic-sidebar.json this session -- run python3 scripts/build_academic_sidebar.py (or fix the JSON):"$'\n'
    report+="$(printf '%s\n' "$new" | head -20)"$'\n\n'
  fi
fi

[ -z "$report" ] && exit 0

{
  printf '%s' "$report"
  echo "Fix these before finishing."
} >&2
exit 2
