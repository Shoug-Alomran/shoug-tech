#!/bin/bash
# Stop hook: run the read-only validators from .github/workflows/deploy-mkdocs.yml
# before the turn ends, so a broken link or route is caught here instead of in
# a red build after push.
#
# Deliberately excludes check_seo_metadata.py: it only passes after
# optimize_site_html.py has injected canonical/OG tags, and that build step
# REWRITES every page under docs/. A hook must not mutate the working tree,
# so SEO metadata stays a CI-only check.
#
# Runs only when this session actually edited a page under docs/ (the
# PostToolUse hook drops a marker file). Exit 2 hands the failures back to
# Claude to fix.

set -uo pipefail

event=$(cat)
repo="${CLAUDE_PROJECT_DIR:-$(pwd)}"

# Already inside a Stop-hook-triggered continuation: don't loop.
if printf '%s' "$event" | grep -q '"stop_hook_active"[[:space:]]*:[[:space:]]*true'; then
  exit 0
fi

session=$(printf '%s' "$event" | sed -n 's/.*"session_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
marker="${TMPDIR:-/tmp}/claude-site-dirty-${session:-nosession}"
[ -f "$marker" ] || exit 0

cd "$repo" || exit 0

if out=$(python3 scripts/verify_site_routes.py 2>&1 &&
         python3 scripts/check_site_links.py 2>&1); then
  rm -f "$marker"
  exit 0
fi

{
  echo "Site validation failed (these are the same checks CI runs on push):"
  printf '%s\n' "$out" | tail -40
  echo
  echo "Fix these before finishing."
} >&2
exit 2
