#!/usr/bin/env python3
"""Fill in the missing canonical / Open Graph / Twitter metadata.

Two kinds of page need different treatment:

  * Standalone pages get a self-referencing canonical derived from their path
    (index.html -> directory URL, anything else -> the full .html path).

  * Embedded documents -- quiz banks, cheat sheets and slide breakdowns that
    exist only to be loaded into a wrapper page's iframe -- get the *wrapper's*
    canonical instead. A self-canonical there would put the bare document into
    the index competing with the page readers are meant to land on.

Never overwrites metadata a page already has.
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

DOCS = Path(__file__).resolve().parent.parent / "docs"
SITE = "https://shoug-tech.com"
OG_IMAGE = f"{SITE}/assets/og-banner.png"

TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC = re.compile(r'<meta\s+name="description"\s+content="([^"]*)"', re.I)
CANON = re.compile(r'<link\s+rel="canonical"\s+href="([^"]*)"', re.I)
HEAD_CLOSE = re.compile(r"</head>", re.I)
SRC = re.compile(r'<(?:iframe|embed)[^>]*\bsrc="([^"]+)"', re.I)
HTML_TAG = re.compile(r"<html\b([^>]*)>", re.I)


def page_url(p: Path) -> str:
    rel = p.relative_to(DOCS).as_posix()
    if rel.endswith("/index.html"):
        rel = rel[: -len("index.html")]
    elif rel == "index.html":
        rel = ""
    return f"{SITE}/{rel}"


def build_embed_map() -> dict[Path, Path]:
    """embedded document -> the page that embeds it."""
    parents: dict[Path, Path] = {}
    for p in DOCS.rglob("*.html"):
        text = p.read_text(encoding="utf-8", errors="ignore")
        for src in SRC.findall(text):
            path = unquote(urlsplit(src).path)
            if not path.endswith(".html"):
                continue
            target = (DOCS / path.lstrip("/")) if path.startswith("/") \
                else (p.parent / path)
            try:
                target = target.resolve()
            except OSError:
                continue
            if target.is_file() and target != p.resolve():
                parents.setdefault(target, p)
    return parents


def clean_title(raw: str) -> str:
    t = html.unescape(re.sub(r"\s+", " ", raw)).strip()
    # Titles are written as "CYS405 · Chapter 1 Quiz — ..." or with a site
    # suffix; keep the descriptive part, drop a trailing brand segment.
    for sep in (" | SHOUG.TECH", " — SHOUG.TECH", " · SHOUG.TECH"):
        if t.endswith(sep):
            t = t[: -len(sep)]
    return t.strip()


def main() -> int:
    apply = "--apply" in sys.argv
    parents = build_embed_map()
    resolved_parents = {k: v for k, v in parents.items()}

    counts = {"canonical": 0, "og": 0, "twitter": 0, "description": 0, "lang": 0}
    touched = 0

    for p in sorted(DOCS.rglob("*.html")):
        text = p.read_text(encoding="utf-8", errors="ignore")
        original = text
        head_end = HEAD_CLOSE.search(text)
        if not head_end:
            continue
        head = text[: head_end.start()]

        title_m = TITLE.search(head)
        title = clean_title(title_m.group(1)) if title_m else ""
        desc_m = DESC.search(head)
        description = html.unescape(desc_m.group(1)) if desc_m else ""

        # Where should this page's canonical point?
        parent = resolved_parents.get(p.resolve())
        if parent is not None:
            parent_text = parent.read_text(encoding="utf-8", errors="ignore")
            pm = CANON.search(parent_text)
            canonical = pm.group(1) if pm else page_url(parent)
        else:
            canonical = page_url(p)

        additions: list[str] = []

        if not description and title:
            description = f"{title} — study material from Shoug's Digital Garden."
            additions.append(
                f'<meta name="description" content="{html.escape(description, quote=True)}">'
            )
            counts["description"] += 1

        if not CANON.search(head):
            additions.append(f'<link rel="canonical" href="{canonical}">')
            counts["canonical"] += 1

        if "og:title" not in head and title:
            esc_t = html.escape(title, quote=True)
            esc_d = html.escape(description, quote=True)
            additions += [
                f'<meta property="og:title" content="{esc_t}">',
                f'<meta property="og:description" content="{esc_d}">',
                f'<meta property="og:url" content="{canonical}">',
                '<meta property="og:type" content="article">',
                f'<meta property="og:image" content="{OG_IMAGE}">',
            ]
            counts["og"] += 1

        if "twitter:card" not in head and title:
            esc_t = html.escape(title, quote=True)
            esc_d = html.escape(description, quote=True)
            additions += [
                '<meta name="twitter:card" content="summary_large_image">',
                f'<meta name="twitter:title" content="{esc_t}">',
                f'<meta name="twitter:description" content="{esc_d}">',
                f'<meta name="twitter:image" content="{OG_IMAGE}">',
            ]
            counts["twitter"] += 1

        if additions:
            block = "\n" + "\n".join("    " + a for a in additions) + "\n"
            text = text[: head_end.start()] + block + text[head_end.start():]

        # <html> without a lang leaves screen readers guessing pronunciation.
        m = HTML_TAG.search(text)
        if m and "lang=" not in m.group(1):
            text = text[: m.start()] + f"<html{m.group(1)} lang=\"en\">" + text[m.end():]
            counts["lang"] += 1

        if text != original:
            touched += 1
            if apply:
                p.write_text(text, encoding="utf-8")

    verb = "added" if apply else "would add"
    print(f"{verb} across {touched} pages:")
    for k, v in counts.items():
        print(f"  {k:12} {v}")
    if not apply:
        print("re-run with --apply to write changes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
