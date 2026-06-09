#!/usr/bin/env python3
"""
Auto-generates docs/search-index.json by scanning all index.html files in docs/.

Run manually:     python3 scripts/build_search_index.py
Run via hook:     automatically on every `git commit`
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT  = DOCS / "search-index.json"

# Directories inside docs/ that should never appear in the search index
SKIP_DIRS = {"assets", "javascripts", "stylesheets", "fonts", ".git", "__pycache__"}

# Exact URLs to exclude from the index
SKIP_URLS = {"/account/"}

# Map first URL segment → section label used by the search UI
SECTION_MAP = {
    "academics":            "academics",
    "academic-plan-themes": "academic-plan-themes",
    "work":                 "work",
    "workshops":            "workshops",
    "resources":            "resources",
    "about":                "about",
    "policy":               "policy",
    "career-development":   "career-development",
}


def _extract(html: str) -> tuple[str, str]:
    """Return (title, description) from raw HTML text."""
    title_m = re.search(r"<title[^>]*>([^<]+)</title>", html, re.I)
    # description: handle either attribute order
    desc_m = re.search(
        r'<meta\b[^>]*\bname=["\']description["\'][^>]*\bcontent=["\']([^"\']*)["\']',
        html, re.I,
    )
    if not desc_m:
        desc_m = re.search(
            r'<meta\b[^>]*\bcontent=["\']([^"\']*)["\'][^>]*\bname=["\']description["\']',
            html, re.I,
        )
    title = title_m.group(1).strip() if title_m else ""
    desc  = desc_m.group(1).strip()  if desc_m  else ""
    return title, desc


def build() -> list[dict]:
    entries: list[dict] = []

    for dirpath, dirnames, filenames in os.walk(DOCS):
        # Prune skipped directories in-place so os.walk won't descend into them
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)

        if "index.html" not in filenames:
            continue

        rel  = Path(dirpath).relative_to(DOCS)
        url  = "/" if str(rel) == "." else "/" + str(rel).replace(os.sep, "/") + "/"

        if url in SKIP_URLS:
            continue

        parts   = [p for p in url.split("/") if p]
        section = SECTION_MAP.get(parts[0], parts[0]) if parts else "home"

        html_path = Path(dirpath) / "index.html"
        try:
            # Only read the first 8 KB — title/meta are always in <head>
            raw = html_path.read_text(encoding="utf-8", errors="ignore")[:8192]
        except OSError:
            continue

        title, desc = _extract(raw)
        if not title:
            continue

        entries.append({"url": url, "title": title, "description": desc, "section": section})

    entries.sort(key=lambda e: e["url"])
    return entries


def main() -> int:
    entries = build()
    OUT.write_text(
        json.dumps(entries, separators=(",", ":"), ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"[ok] search-index.json → {len(entries)} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
