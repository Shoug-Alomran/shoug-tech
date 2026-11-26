#!/usr/bin/env python3
"""Embed each annotated slide's own text in its deck page, for read-aloud (docs/javascripts/slide-reader.js).

Every annotated slide is a picture of a page of the original lecture PDF (slide N = page N), so the
page itself has no slide text to read. This takes the text of each PDF page, drops what repeats on
most pages (copyright footers, course banners) and page numbers, joins lines that a PDF wrapped
mid-sentence, and stores it in the deck page as
    <script type="application/json" id="slide-speech">{"v":1,"slides":{"1":["line", ...], ...}}</script>

    python scripts/build_slide_speech.py                 every course
    python scripts/build_slide_speech.py cs101 se423     some courses
    python scripts/build_slide_speech.py --print cs101/05-loops 6    show slide 6 of one deck

annotated_search.build_course runs it for a course after its decks are rebuilt. Needs pdfplumber.
A deck whose PDF has a different page count from its slides is skipped: it is the wrong file.
"""
import glob
import json
import logging
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from annotated_page import uncid  # noqa: E402
from annotated_search import source_pdf  # noqa: E402

DOCS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
BLOCK = re.compile(r'\n?<script type="application/json" id="slide-speech">.*?</script>', re.S)
CARD = re.compile(r'<section class="card[^"]*" id="slide-(\d+)" data-slide="\d+"')
# Bullet glyphs (Wingdings and friends) at the start of a line, and private-use symbols anywhere.
BULLET = re.compile(r"^(?:[•▪■●◦○◆❖➢➤►–—Ø§ü∙‣⁃▸▹→\-\*o]\s+)+")
PRIVATE = re.compile(r"[-�]")
NUMBER_ONLY = re.compile(r"^[\d\s./\-–|]+$")
ENDS_SENTENCE = re.compile(r"[.!?:;؟)\]\"”']$")


def norm(line):
    """Key for spotting banners that repeat: a page number merged into a footer must not hide it."""
    return re.sub(r"\s+", " ", re.sub(r"\d", "", line)).strip().casefold()


def mostly_symbols(line):
    letters = sum(ch.isalpha() for ch in line)
    return letters < 2 or letters < len(line.replace(" ", "")) * 0.35


def page_lines(page):
    # The bottom 8% is footer (copyright, page number), as annotated_page.pdf_words treats it.
    body = page.crop((0, 0, float(page.width), float(page.height) * 0.92), relative=True, strict=False)
    text = uncid(body.extract_text() or "")
    out = []
    for raw in text.splitlines():
        line = PRIVATE.sub(" ", raw)
        line = BULLET.sub("", re.sub(r"\s+", " ", line).strip())
        if line:
            out.append(line)
    return out


def tidy(lines, repeated):
    """Drop repeated banners and bare numbers; join a line that continues the one before it."""
    kept = [
        line
        for line in lines
        if norm(line) not in repeated and not NUMBER_ONLY.match(line) and not mostly_symbols(line)
    ]
    joined = []
    for line in kept:
        if (
            joined
            and not ENDS_SENTENCE.search(joined[-1])
            and (line[0].islower() or line[0] in ",;)")
        ):
            joined[-1] += " " + line
        else:
            joined.append(line)
    return joined


def deck_speech(pdf_path, slide_count):
    import pdfplumber

    with pdfplumber.open(pdf_path) as pdf:
        if len(pdf.pages) != slide_count:
            return None
        pages = []
        for page in pdf.pages:
            try:
                pages.append(page_lines(page))
            except Exception:
                pages.append([])
    repeated = set()
    if len(pages) >= 6:
        seen = Counter(norm(line) for lines in pages for line in set(lines))
        repeated = {line for line, n in seen.items() if n >= max(3, len(pages) * 0.3)}
    return {str(i): tidy(lines, repeated) for i, lines in enumerate(pages, 1)}


def deck_pages(courses=()):
    for path in sorted(glob.glob(os.path.join(DOCS, "academics", "*", "*", "annotated-slides", "*", "*.html"))):
        if os.path.basename(path) == "index.html":
            continue
        course = path.split(os.sep)[-4]
        if courses and course not in courses:
            continue
        yield path


def embed(path):
    """Returns 'updated', 'same', or why the deck was skipped."""
    with open(path, encoding="utf-8") as fh:
        page = fh.read()
    cards = CARD.findall(page)
    if not cards:
        return "no slide cards"
    pdf = source_pdf(page, os.path.dirname(path))
    if not pdf:
        return "no source PDF"
    slides = deck_speech(pdf, len(cards))
    if slides is None:
        return "PDF page count differs from slides"
    data = json.dumps({"v": 1, "slides": slides}, ensure_ascii=False, separators=(",", ":"))
    tag = '<script type="application/json" id="slide-speech">%s</script>' % data.replace("</", "<\\/")
    if BLOCK.search(page):
        updated = BLOCK.sub(lambda _: "\n" + tag, page, count=1)
    else:
        updated = page.replace("</main>", "</main>\n" + tag, 1)
    if updated == page:
        return "same"
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(updated)
    return "updated"


def build_course(course_dir):
    """Hook for annotated_search.build_course: every deck of one course."""
    logging.getLogger("pdfminer").setLevel(logging.ERROR)
    for path in sorted(glob.glob(os.path.join(course_dir, "annotated-slides", "*", "*.html"))):
        if os.path.basename(path) != "index.html":
            embed(path)


def main(argv):
    logging.getLogger("pdfminer").setLevel(logging.ERROR)
    if argv[:1] == ["--print"]:
        course, slug = argv[1].strip("/").split("/")
        n = argv[2] if len(argv) > 2 else "1"
        for path in deck_pages({course}):
            if os.path.basename(os.path.dirname(path)) == slug:
                with open(path, encoding="utf-8") as fh:
                    page = fh.read()
                pdf = source_pdf(page, os.path.dirname(path))
                slides = deck_speech(pdf, len(CARD.findall(page))) if pdf else None
                print("\n".join((slides or {}).get(n, ["(nothing)"])))
        return
    results = Counter()
    for path in deck_pages(set(argv)):
        result = embed(path)
        results[result] += 1
        if result not in ("updated", "same"):
            print("skipped %s: %s" % (os.path.relpath(path, DOCS), result))
    print(dict(results))


if __name__ == "__main__":
    main(sys.argv[1:])
