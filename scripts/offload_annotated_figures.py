#!/usr/bin/env python3
"""Move annotated-slide figures out of the site build and point pages at R2.

Cloudflare Pages allows 20,000 files per deploy, and the annotated-slide figures
are over half the site. At deploy, this moves every docs/**/annotated-slides/*/figures/*
file into .r2-upload/ (same relative path), rewrites the src="figures/..." references
in each deck's pages to https://assets.shoug-tech.com/<path>, and fails if a page
still points at a moved file. The workflow then syncs .r2-upload/ to the
shoug-tech-assets R2 bucket before the pages go live.

    python3 scripts/offload_annotated_figures.py
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
UPLOAD = ROOT / ".r2-upload"
ASSETS = "https://assets.shoug-tech.com"
# The paid course is sealed in the build and must never be copied to a public bucket.
EXCLUDED = "/ethcs303/"
REF = re.compile(r'(\b(?:src|data-src|href|poster)\s*=\s*["\'])figures/')
LEFT = re.compile(r'\b(?:src|data-src|href|poster|srcset)\s*=\s*["\']figures/|url\(\s*["\']?figures/')


def main() -> int:
    figures = sorted(p for p in DOCS.glob("**/annotated-slides/*/figures/*") if p.is_file())
    figures = [p for p in figures if EXCLUDED not in "/" + p.relative_to(DOCS).as_posix()]
    decks = sorted({p.parent.parent for p in figures})
    problems = []
    for deck in decks:
        base = f"{ASSETS}/{deck.relative_to(DOCS).as_posix()}/figures/"
        for page in deck.glob("*.html"):
            text = page.read_text(encoding="utf-8")
            updated = REF.sub(lambda m: m.group(1) + base, text)
            if LEFT.search(updated):
                problems.append(page.relative_to(ROOT).as_posix())
            if updated != text:
                page.write_text(updated, encoding="utf-8")
    if problems:
        print("[error] pages still reference local figures after the rewrite:")
        print("\n".join(f"  {p}" for p in problems[:20]))
        return 1
    for figure in figures:
        target = UPLOAD / figure.relative_to(DOCS)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(figure), target)
    for deck in decks:
        folder = deck / "figures"
        if folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir()
    print(f"Moved {len(figures)} figures from {len(decks)} annotated decks to {UPLOAD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
