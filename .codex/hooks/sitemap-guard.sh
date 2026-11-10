#!/bin/bash
# Stop hook: the sitemaps must never be broken or stale.
#
# Runs scripts/check_sitemap.py --write, which rebuilds docs/sitemap.xml and
# docs/standalone-sitemap.xml in memory with the deploy generator's page
# selection and rewrites them only if they drifted. It never touches HTML --
# those two XML files are the only outputs.
#
# Anything regeneration cannot fix (a canonical pointing at a missing page, a
# folder page whose canonical names another page) is page metadata, so the
# report goes back to Claude with exit 2 to fix before the turn ends.

set -uo pipefail

event=$(cat)
repo="${CLAUDE_PROJECT_DIR:-$(pwd)}"

# Already inside a Stop-hook-triggered continuation: don't loop.
if printf '%s' "$event" | grep -q '"stop_hook_active"[[:space:]]*:[[:space:]]*true'; then
  exit 0
fi

cd "$repo" || exit 0
[ -f scripts/check_sitemap.py ] || exit 0

if out=$(python3 scripts/check_sitemap.py --write 2>&1); then
  exit 0
fi

{
  echo "Sitemap check failed (scripts/check_sitemap.py):"
  printf '%s\n' "$out" | tail -60
  echo "Fix the page metadata above, then rerun python3 scripts/check_sitemap.py --write."
} >&2
exit 2
