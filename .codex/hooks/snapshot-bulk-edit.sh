#!/bin/bash
# PreToolUse (Bash) hook: take a restore point before a bulk in-place rewrite.
#
# Sweeping `perl -i` / `sed -i` substitutions across hundreds of files is a
# normal part of working in this repo, and when the pattern is subtly wrong it
# corrupts every file it touches at once. This does NOT block the command --
# it records a snapshot commit object first, so the whole sweep can be undone
# even from an already-dirty tree.
#
# Restore:  git checkout <sha> -- .

set -uo pipefail

event=$(cat)
repo="${CLAUDE_PROJECT_DIR:-$(pwd)}"

cmd=$(printf '%s' "$event" | python3 -c '
import json,sys
try: print((json.load(sys.stdin).get("tool_input") or {}).get("command",""))
except Exception: pass
' 2>/dev/null)

[ -n "$cmd" ] || exit 0

# In-place edit (sed -i / perl -i), fanned out over many files.
printf '%s' "$cmd" | grep -Eq '(^|[|;&[:space:]])(sed|perl)[[:space:]]+(-[a-zA-Z0-9]*i|-i)' || exit 0
printf '%s' "$cmd" | grep -Eq 'xargs|find[[:space:]]|\*|\{\}' || exit 0

cd "$repo" || exit 0
git rev-parse --git-dir >/dev/null 2>&1 || exit 0

# `git stash create` has to read every modified file. Reads in this working
# tree cost ~1.5s each, so on a very dirty tree the snapshot would take longer
# than the edit it protects. Above the threshold, warn instead of stalling.
dirty=$(git status --porcelain -- . 2>/dev/null | wc -l | tr -d ' ')
if [ "${dirty:-0}" -gt 200 ]; then
  echo "Bulk in-place edit with $dirty files already modified -- too many to snapshot quickly."
  echo "Commit or stash first if you want an undo point for this sweep."
  exit 0
fi

sha=$(git stash create 2>/dev/null)
if [ -z "$sha" ]; then
  # Clean tree: HEAD itself is the restore point.
  sha=$(git rev-parse --short HEAD 2>/dev/null)
  echo "Bulk in-place edit; tree is clean, so 'git checkout -- .' undoes it (HEAD $sha)."
  exit 0
fi

ref="refs/claude-snapshots/$(date +%Y%m%d-%H%M%S)"
git update-ref "$ref" "$sha" 2>/dev/null
echo "Bulk in-place edit detected. Snapshot saved before running."
echo "Undo the whole sweep with:  git checkout ${sha:0:12} -- ."
exit 0
