#!/bin/bash
# PreToolUse (Bash) hook: stop the scripts/ entry points that have quietly
# damaged this site before, and point at the safe path instead.
#
#   * build_search_index.py   -- rewrites docs/search-index.json down to ~1411
#     entries (drops every standalone *.html) while printing "[ok]". DENIED;
#     the Node builder is the real one.
#   * replace_academic_sidebar() -- re-derives Study Material items by directory
#     discovery and emits dead links. DENIED; the JSON + sidebar builder is the
#     source of truth.
#   * add_slide_rights_notice.py, backfill_seo_metadata.py --apply,
#     apply_a11y_baseline.py --apply -- walk ALL of docs/. Allowed, but Claude
#     is told to scope the result back to the course being worked on.

set -uo pipefail

cmd=$(jq -r '.tool_input.command // empty' 2>/dev/null)
[ -n "$cmd" ] || exit 0

deny() {
  jq -n --arg r "$1" \
    '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"deny",permissionDecisionReason:$r}}'
  exit 0
}

context() {
  jq -n --arg c "$1" \
    '{hookSpecificOutput:{hookEventName:"PreToolUse",additionalContext:$c}}'
  exit 0
}

matches() { printf '%s' "$cmd" | grep -Eq "$1"; }

if matches 'python[0-9.]*[[:space:]]+[^|;&]*build_search_index\.py|(^|[;&|[:space:]])(\./)?scripts/build_search_index\.py'; then
  deny "scripts/build_search_index.py silently drops ~700 standalone-page entries from docs/search-index.json. Run 'node scripts/build-search-index.js' instead, then diff the URL set against 'git show HEAD:docs/search-index.json' (expect only additions)."
fi

if matches 'python' && matches 'replace_academic_sidebar[[:space:]]*\(|import[^;]*replace_academic_sidebar'; then
  deny "replace_academic_sidebar() re-derives sidebar items by directory discovery and has produced dead links. Add the entries to scripts/academic-sidebar.json ('children', keyed by parent section URL), then run 'python3 scripts/build_academic_sidebar.py'."
fi

if matches 'add_slide_rights_notice\.py|backfill_seo_metadata\.py[^|;&]*--apply|apply_a11y_baseline\.py[^|;&]*--apply'; then
  context "This script rewrites pages across ALL of docs/, not just the course you are working on. After it runs, revert what landed outside that course, e.g. git checkout -- \$(git diff --name-only -G'<marker it inserts>' | grep -v '<course>'), then re-run python3 scripts/build_academic_sidebar.py (reverting drops the sidebar stamp). Tell Shoug about the out-of-scope drift instead of silently shipping it."
fi

exit 0
