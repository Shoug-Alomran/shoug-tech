#!/bin/bash
# SessionEnd hook: shut down local preview servers left running by this repo.
#
# Only kills `python3 -m http.server` processes whose working directory is
# inside the project, so a preview server you started for something else on
# another project is left alone.

set -uo pipefail
repo="${CLAUDE_PROJECT_DIR:-$(pwd)}"
[ -n "$repo" ] || exit 0

for pid in $(pgrep -f "http\.server" 2>/dev/null); do
  cwd=$(lsof -a -p "$pid" -d cwd -Fn 2>/dev/null | sed -n 's/^n//p' | head -1)
  case "$cwd" in
    "$repo"|"$repo"/*) kill "$pid" 2>/dev/null && echo "Stopped preview server (pid $pid)" ;;
  esac
done
exit 0
