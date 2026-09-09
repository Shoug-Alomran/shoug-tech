#!/usr/bin/env python3
"""Format HTML the way VS Code's "Format Document" does — across many files.

VS Code's built-in HTML formatter is js-beautify, so this runs the same engine.
It differs in two ways that matter for this repo:

1. wrap_line_length is 0 (off) rather than VS Code's 120. Wrapping rewrites text
   nodes, which churns the diff of every page for no benefit.

2. Preformatted regions are protected. js-beautify only leaves <pre>, <code> and
   <textarea> alone, but this site marks preformatted content with CSS classes
   instead — .tree-diagram and .code-block are `white-space: pre`/`pre-wrap`, so
   every space in them is load-bearing. Formatting them re-indents ASCII
   diagrams and code samples into rubble. The protected class list is derived
   from the stylesheets themselves (any selector with `white-space: pre*`), so
   it stays correct as styles change.

Usage:
    scripts/format_html.py                    # all of docs/
    scripts/format_html.py docs/.../ethcs303  # one course

Scope it to the course you touched rather than reformatting the whole site.
"""
from __future__ import annotations

import re
import subprocess
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BEAUTIFY = [
    "npx", "--yes", "js-beautify@1.15.1",
    "--type", "html", "--replace",
    "--indent-size", "4",
    "--wrap-line-length", "0",
    "--wrap-attributes", "auto",
    "--preserve-newlines",
    "--extra-liners", "head,body,/html",
    "--content-unformatted", "pre,code,textarea",
]


def protected_classes() -> set[str]:
    """Class names the stylesheets render with significant whitespace."""
    found = set()
    for css in (ROOT / "docs" / "styles").glob("*.css"):
        text = css.read_text(encoding="utf-8", errors="replace")
        for block in re.finditer(r"([^{}]+)\{([^{}]*)\}", text):
            if not re.search(r"white-space:\s*pre", block.group(2)):
                continue
            found.update(re.findall(r"\.([A-Za-z0-9_-]+)", block.group(1)))
    return found


def stash(html: str, classes: set[str]) -> tuple[str, dict[str, str]]:
    """Replace the contents of protected elements with opaque placeholders."""
    saved: dict[str, str] = {}
    if not classes:
        return html, saved
    pattern = re.compile(
        r'<(?P<tag>div|p|span|section)\b[^>]*class="[^"]*\b(?:%s)\b[^"]*"[^>]*>'
        % "|".join(sorted(map(re.escape, classes))),
        re.IGNORECASE,
    )
    out, pos = [], 0
    while (m := pattern.search(html, pos)) is not None:
        tag = m.group("tag")
        # Walk to the matching close tag, counting nested opens of the same tag.
        depth, i = 1, m.end()
        nested = re.compile(r"</?%s\b" % re.escape(tag), re.IGNORECASE)
        while depth and (n := nested.search(html, i)) is not None:
            depth += -1 if n.group(0).startswith("</") else 1
            i = n.end()
        if depth:            # unbalanced markup; leave this one alone
            out.append(html[pos:m.end()])
            pos = m.end()
            continue
        close = html.index(">", i) + 1
        end = html.rindex("</", m.end(), close)
        token = "SHOUGPRE%sX" % uuid.uuid4().hex
        saved[token] = html[m.end():end]
        out.append(html[pos:m.end()])
        out.append(token)
        pos = end
    out.append(html[pos:])
    return "".join(out), saved


def main() -> int:
    target = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "docs")
    if not target.exists():
        print("no such path: %s" % target, file=sys.stderr)
        return 1

    files = sorted(target.rglob("*.html")) if target.is_dir() else [target]
    if not files:
        print("no .html files under %s" % target)
        return 0

    classes = protected_classes()
    print("Formatting %d file(s) under %s" % (len(files), target.relative_to(ROOT)))
    print("Protecting preformatted classes: %s" % (", ".join(sorted(classes)) or "none"))

    stashes = {}
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        held, saved = stash(text, classes)
        if saved:
            path.write_text(held, encoding="utf-8")
            stashes[path] = saved

    for i in range(0, len(files), 200):     # keep the argv comfortably short
        subprocess.run(BEAUTIFY + [str(p) for p in files[i:i + 200]],
                       check=True, stdout=subprocess.DEVNULL)

    for path, saved in stashes.items():
        text = path.read_text(encoding="utf-8", errors="replace")
        for token, original in saved.items():
            text = text.replace(token, original)
        path.write_text(text, encoding="utf-8")

    print("Done. Re-run the deploy gate before pushing:")
    print("  python3 scripts/check_seo_metadata.py && python3 scripts/check_site_links.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
