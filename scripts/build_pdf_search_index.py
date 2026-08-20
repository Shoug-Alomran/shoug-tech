#!/usr/bin/env python3
"""Build a searchable index of the text inside the course PDFs.

Site search only ever matched page titles and descriptions, so a student
looking for "diffie hellman" found nothing unless it happened to be in a
slide's title. The decks themselves hold the material.

Storing the full text would be ~9 MB. Instead each PDF contributes its set of
distinctive terms (deduplicated, stopwords dropped) plus a short preview, which
compresses to roughly 0.3 MB gzipped for the whole site and is fetched lazily
on the first search.

Results point at the wrapper page that embeds the deck rather than the raw
file, so readers land on the site with its navigation intact.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = DOCS / "search-pdf-index.json"

WORD = re.compile(r"[a-zA-Z][a-zA-Z0-9'-]{3,}")
PDF_REF = re.compile(r'data-pdf-src="([^"]+)"|<iframe[^>]*\bsrc="([^"]+\.pdf)"', re.I)

STOPWORDS = set("""
the a an and or of to in is are was were be been being for on at by with from
as it its this that these those if then else than which who whom what when
where how why not no yes can could should would may might must will shall do
does did done have has had having you they we us our your their them his her
him my mine ours yours theirs there here all any both each few more most other
some such only own same so too very now also into out up down over under again
further once about above below between through during before after
""".split())

# Slide decks repeat their course code and boilerplate on every page; terms
# this common carry no signal and only inflate the index.
MAX_TERMS = 700
PREVIEW_CHARS = 200


def wrapper_pages() -> dict[str, str]:
    """pdf path (site-absolute) -> page URL that embeds it."""
    mapping: dict[str, str] = {}
    for p in DOCS.rglob("*.html"):
        text = p.read_text(encoding="utf-8", errors="ignore")
        if ".pdf" not in text:
            continue
        rel = p.relative_to(DOCS).as_posix()
        url = "/" + (rel[: -len("index.html")] if rel.endswith("index.html") else rel)
        for a, b in PDF_REF.findall(text):
            src = a or b
            path = unquote(urlsplit(src).path)
            target = (DOCS / path.lstrip("/")) if path.startswith("/") \
                else (p.parent / path)
            try:
                key = "/" + target.resolve().relative_to(DOCS.resolve()).as_posix()
            except (OSError, ValueError):
                continue
            mapping.setdefault(key, url)
    return mapping


def extract(pdf: Path) -> tuple[str, str] | None:
    try:
        out = subprocess.run(
            ["pdftotext", "-q", str(pdf), "-"],
            capture_output=True, text=True, timeout=180,
        )
    except (subprocess.SubprocessError, OSError):
        return None
    text = out.stdout
    if not text.strip():
        return None  # scanned deck with no text layer

    words = [w for w in WORD.findall(text.lower()) if w not in STOPWORDS]
    if not words:
        return None

    # Frequency order keeps the most characteristic vocabulary when truncating.
    freq: dict[str, int] = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    terms = sorted(freq, key=lambda w: (-freq[w], w))[:MAX_TERMS]

    preview = re.sub(r"\s+", " ", text).strip()[:PREVIEW_CHARS]
    return " ".join(sorted(terms)), preview


def title_for(pdf: Path) -> str:
    name = pdf.stem.replace("-", " ").replace("_", " ")
    return re.sub(r"\s+", " ", name).strip().title()


def main() -> int:
    pdfs = sorted(DOCS.rglob("*.pdf"))
    wrappers = wrapper_pages()
    print(f"indexing {len(pdfs)} PDFs...")

    entries = []
    skipped = 0

    def work(pdf: Path):
        rel = "/" + pdf.relative_to(DOCS).as_posix()
        result = extract(pdf)
        if result is None:
            return None
        terms, preview = result
        return {
            "u": wrappers.get(rel, rel),
            "f": rel,
            "t": title_for(pdf),
            "k": terms,
            "p": preview,
        }

    with ThreadPoolExecutor(4) as pool:
        for entry in pool.map(work, pdfs):
            if entry is None:
                skipped += 1
            else:
                entries.append(entry)

    OUT.write_text(json.dumps(entries, separators=(",", ":")), encoding="utf-8")
    size = OUT.stat().st_size
    print(f"wrote {OUT.relative_to(ROOT)}: {len(entries)} documents, "
          f"{size/1024:.0f} KB raw")
    if skipped:
        print(f"{skipped} PDFs had no extractable text layer (scanned images)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
