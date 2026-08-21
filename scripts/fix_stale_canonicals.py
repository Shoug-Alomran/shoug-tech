#!/usr/bin/env python3
"""Repair canonical URLs that point at pages which do not exist.

Three causes, all leaving search engines following a canonical to a 404:

  * paths from an earlier site structure (flat slide-breakdowns/Chapter-2/
    instead of today's numbered folders)
  * "index.html" stripped by substring rather than path segment, turning
    02-index.html into a truncated 02-
  * casing that only resolves on a case-insensitive filesystem

An embedded document takes its wrapper's canonical, since the wrapper is the
page readers are meant to land on. Everything else gets a canonical derived
from its own location. Pages whose canonical already resolves are untouched.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

DOCS = Path(__file__).resolve().parent.parent / "docs"
SITE = "https://shoug-tech.com"

CANON = re.compile(r'(<link\s+rel="canonical"\s+href=")([^"]*)(")', re.I)
OG_URL = re.compile(r'(<meta\s+property="og:url"\s+content=")([^"]*)(")', re.I)
SRC = re.compile(r'<(?:iframe|embed)[^>]*\bsrc="([^"]+)"', re.I)


def page_url(p: Path) -> str:
    rel = p.relative_to(DOCS).as_posix()
    # Only a whole trailing path segment may be dropped -- stripping the
    # substring is what produced canonicals ending in "02-".
    if rel == "index.html":
        rel = ""
    elif rel.endswith("/index.html"):
        rel = rel[: -len("index.html")]
    return f"{SITE}/{rel}"


def resolves(url: str) -> bool:
    split = urlsplit(url)
    if split.netloc and split.netloc not in {"shoug-tech.com", "www.shoug-tech.com"}:
        return True  # off-site canonical: not ours to judge
    path = unquote(split.path)
    if not path.startswith("/"):
        return False
    target = DOCS / path.lstrip("/")
    if target.is_file():
        return True
    if path.endswith("/") or not Path(path).suffix:
        return (target / "index.html").is_file()
    return False


def embed_map() -> dict[Path, Path]:
    parents: dict[Path, Path] = {}
    for p in DOCS.rglob("*.html"):
        text = p.read_text(encoding="utf-8", errors="ignore")
        if "<iframe" not in text and "<embed" not in text:
            continue
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


def main() -> int:
    apply = "--apply" in sys.argv
    parents = embed_map()
    fixed = 0
    samples: list[str] = []

    for p in sorted(DOCS.rglob("*.html")):
        text = p.read_text(encoding="utf-8", errors="ignore")
        m = CANON.search(text)
        if not m or resolves(m.group(2)):
            continue

        parent = parents.get(p.resolve())
        if parent is not None:
            pm = CANON.search(parent.read_text(encoding="utf-8", errors="ignore"))
            target = pm.group(2) if pm and resolves(pm.group(2)) else page_url(parent)
        else:
            target = page_url(p)

        if target == m.group(2):
            continue

        if len(samples) < 6:
            samples.append(f"{p.relative_to(DOCS).as_posix()}\n     {m.group(2)}\n  -> {target}")

        text = text[: m.start()] + m.group(1) + target + m.group(3) + text[m.end():]
        # og:url must agree with the canonical or check_seo_metadata fails.
        om = OG_URL.search(text)
        if om:
            text = text[: om.start()] + om.group(1) + target + om.group(3) + text[om.end():]

        fixed += 1
        if apply:
            p.write_text(text, encoding="utf-8")

    verb = "fixed" if apply else "would fix"
    print(f"{verb} {fixed} stale canonicals")
    for s in samples:
        print(f"  {s}")
    if not apply:
        print("re-run with --apply to write changes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
