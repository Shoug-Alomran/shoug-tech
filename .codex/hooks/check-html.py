#!/usr/bin/env python3
"""PostToolUse hook: catch structural damage to a single edited HTML file.

Regex surgery on the shared sidebar/tree markup is the main way pages in this
repo break, and a missing </ul> silently reparents whole sections of the tree.
This checks only the file that was just written, so it costs milliseconds.

A file is reported only when the edit made it *worse* than the committed
version, so pre-existing damage elsewhere never blocks unrelated work.

Exit 2 => stderr is fed back to Claude to fix.
"""
import json
import os
import re
import subprocess
import sys

TAGS = ("ul", "li", "div", "section")


def imbalance(text):
    """Return {tag: open_count - close_count} for tags that don't balance."""
    out = {}
    for tag in TAGS:
        opened = len(re.findall(r"<%s\b" % tag, text, re.I))
        closed = len(re.findall(r"</%s\s*>" % tag, text, re.I))
        if opened != closed:
            out[tag] = opened - closed
    return out


def committed_version(path, repo):
    """The file's content at HEAD, or None if untracked/unavailable."""
    rel = os.path.relpath(path, repo)
    try:
        r = subprocess.run(
            ["git", "-C", repo, "show", "HEAD:%s" % rel],
            capture_output=True, timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return r.stdout.decode("utf-8", "replace") if r.returncode == 0 else None


def main():
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    path = (event.get("tool_input") or {}).get("file_path") or ""
    if not path.endswith(".html") or not os.path.isfile(path):
        return 0

    repo = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    if "/docs/" not in path and not path.endswith("/docs"):
        return 0

    # Mark the session as having touched the site, so the Stop hook knows to
    # run the full link/route/SEO validation before finishing.
    session = event.get("session_id") or "nosession"
    marker = os.path.join(
        os.environ.get("TMPDIR", "/tmp"), "claude-site-dirty-%s" % session
    )
    try:
        open(marker, "w").close()
    except OSError:
        pass

    with open(path, encoding="utf-8", errors="replace") as fh:
        now = imbalance(fh.read())
    if not now:
        return 0

    base = committed_version(path, repo)
    was = imbalance(base) if base is not None else {}

    # Only complain about tags this edit made worse.
    worse = {t: d for t, d in now.items() if abs(d) > abs(was.get(t, 0))}
    if not worse:
        return 0

    detail = ", ".join(
        "<%s> %+d (was %+d)" % (t, d, was.get(t, 0)) for t, d in sorted(worse.items())
    )
    sys.stderr.write(
        "Unbalanced HTML introduced in %s: %s\n"
        "(positive = unclosed opening tags, negative = extra closing tags)\n"
        "Re-check the edit before moving on.\n" % (path, detail)
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
