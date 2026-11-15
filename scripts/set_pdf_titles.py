#!/usr/bin/env python3
"""Give PDFs a real document title, so search results don't show "Slide 1".

Bing and Google use a PDF's Title metadata as its result title. Most decks here
have none, or "PowerPoint Presentation", "Slide 1" or the file name, and Bing
flags them as "title too short". At deploy, after compression, this sets Title
from the PDF's viewer page (the canonical in workers/indexing/src/manifest.json,
or the index.html beside it), falling back to the course code and file name.

The change is an incremental update appended to the file, so page content is
untouched and the output is the same on every run. A PDF that already has a
descriptive title of 30+ characters is left alone, as is ETHCS303.

    python3 scripts/set_pdf_titles.py            # dry run
    python3 scripts/set_pdf_titles.py --apply
"""
from __future__ import annotations

import html
import io
import json
import logging
import os
import re
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parent.parent
DOCS = Path(os.environ.get("SEO_DOCS", ROOT / "docs")).resolve()
MANIFEST = ROOT / "workers" / "indexing" / "src" / "manifest.json"
SITE = "https://shoug-tech.com"
MIN_TITLE = 30
SKIP = ("/ethcs303/",)
GENERIC = re.compile(r"(?i)^(slide \d+|powerpoint presentation|microsoft (word|powerpoint)\b.*|untitled.*|"
                     r"document\d*|presentation\d*|title|lecture \d+)$")
TITLE_RE = re.compile(r"<title\b[^>]*>(.*?)</title>", re.S | re.I)
CODE_RE = re.compile(r"/academics/[^/]+/([a-z]{2,5}\d{3})/")

logging.getLogger("pypdf").setLevel(logging.ERROR)


def humanize(stem: str) -> str:
    stem = re.sub(r"[%(]\d+[)]?|\(\d+\)", "", stem)
    words = [w for w in re.split(r"[-_\s]+", stem) if w]
    acronyms = {"cs", "se", "is", "ai", "dx", "cys", "os", "dns", "sql", "ui", "ux", "psu", "it", "ctf", "mcq"}
    return " ".join(w.upper() if re.fullmatch(r"[a-z]{2,5}\d{3}", w) or w.lower() in acronyms else
                    (w if w.isupper() else w.capitalize()) for w in words)


def page_title(page: Path) -> str:
    if not page.is_file():
        return ""
    m = TITLE_RE.search(page.read_text(encoding="utf-8", errors="ignore")[:400000])
    t = html.unescape(re.sub(r"\s+", " ", m.group(1))).strip() if m else ""
    t = re.sub(r"\s*[|—·-]\s*SHOUG\.TECH\s*$", "", t, flags=re.I)
    return re.sub(r"^SHOUG\.TECH\s*(\||//|—|·)\s*", "", t, flags=re.I).strip()


def viewer_for(pdf: Path, canonicals: dict[str, str]) -> Path | None:
    route = "/" + pdf.relative_to(DOCS).as_posix()
    target = canonicals.get(route, "")
    if target.startswith(SITE) and not target.endswith(".pdf"):
        path = target[len(SITE):]
        page = DOCS / path.lstrip("/")
        return page / "index.html" if path.endswith("/") else page
    # The folder's own page only describes this PDF if the PDF is alone in it
    # (a slides/ or course folder lists many).
    sibling = pdf.parent / "index.html"
    if sibling.is_file() and len(list(pdf.parent.glob("*.pdf"))) == 1 \
            and not CODE_RE.fullmatch("/" + pdf.parent.relative_to(DOCS).as_posix() + "/") \
            and pdf.name in html.unescape(sibling.read_text(encoding="utf-8", errors="ignore")):
        return sibling
    return None


def wanted_title(pdf: Path, canonicals: dict[str, str]) -> str:
    viewer = viewer_for(pdf, canonicals)
    t = page_title(viewer) if viewer else ""
    if len(t) >= 20:
        return t if len(t) >= MIN_TITLE else f"{t} | SHOUG.TECH"
    route = "/" + pdf.relative_to(DOCS).as_posix()
    m = CODE_RE.search(route)
    name = humanize(pdf.stem)
    if m and m.group(1).upper() not in name.upper():
        name = f"{name} | {m.group(1).upper()}"
    return f"{name} | SHOUG.TECH" if len(name) < MIN_TITLE else name


def current_title(reader: PdfReader) -> str:
    try:
        meta = reader.metadata
        return str(meta.title or "").strip() if meta else ""
    except Exception:
        return ""


def needs_title(title: str, pdf: Path) -> bool:
    slug = re.sub(r"[^a-z0-9]+", "", title.lower())
    return (len(title) < MIN_TITLE or bool(GENERIC.match(title))
            or slug == re.sub(r"[^a-z0-9]+", "", pdf.stem.lower())
            or title.lower().startswith("microsoft "))


def set_title(pdf: Path, title: str) -> bool:
    original = pdf.read_bytes()
    try:
        writer = PdfWriter(io.BytesIO(original), incremental=True)
        writer.add_metadata({"/Title": title})
        tmp = pdf.with_suffix(".pdf.tmp")
        with open(tmp, "wb") as fh:
            writer.write(fh)
        if current_title(PdfReader(str(tmp))) != title:
            raise ValueError("title did not read back")
        os.replace(tmp, pdf)
        return True
    except Exception as exc:  # broken PDFs: keep the original bytes
        pdf.with_suffix(".pdf.tmp").unlink(missing_ok=True)
        pdf.write_bytes(original)
        print(f"  skipped {pdf.relative_to(DOCS)}: {exc}")
        return False


def main() -> int:
    apply = "--apply" in sys.argv
    canonicals = json.loads(MANIFEST.read_text())["canonicals"] if MANIFEST.is_file() else {}
    changed = skipped = 0
    for pdf in sorted(DOCS.rglob("*.pdf")):
        rel = "/" + pdf.relative_to(DOCS).as_posix()
        if any(s in rel for s in SKIP):
            continue
        try:
            reader = PdfReader(str(pdf))
        except Exception:
            continue
        old = current_title(reader)
        if not needs_title(old, pdf):
            continue
        new = wanted_title(pdf, canonicals)
        if new == old:
            continue
        if not apply:
            if changed < 20:
                print(f"{rel}\n  {old!r} -> {new!r}")
            changed += 1
        elif set_title(pdf, new):
            changed += 1
        else:
            skipped += 1
    print(f"{'set' if apply else 'would set'} {changed} PDF titles" + (f", {skipped} skipped" if skipped else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
