#!/usr/bin/env python3
"""Add SE411's uploaded chapter decks to the site.

Moves each upload to slides/<slug>/<slug>.pdf, writes a viewer page per deck
(CS340's viewer shell, via build_new_courses.py) and a plain listing, which
build_slide_hub.py then turns into the Slides page with previews. Safe to re-run.

    .venv/bin/python scripts/build_se411_slides.py
    .venv/bin/python scripts/build_slide_hub.py software-engineering/se411
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_new_courses as base  # noqa: E402
from build_academic_sidebar import load_data  # noqa: E402

base.SECTIONS.setdefault("software-engineering", ("Software Engineering", "هندسة البرمجيات"))

# (original upload, slug, title from the deck's own first page)
DECKS = [
    ("Chapter 01 Introduction to Software Construction_final_updated.pdf",
     "chapter-1-introduction-to-software-construction", "Chapter 1: Introduction to Software Construction"),
    ("Chapter 02 generics and Lambda Expressions [Updated].pdf",
     "chapter-2-generics-and-lambda-expressions", "Chapter 2: Generics and Lambda Expressions"),
    ("Chapter 03_up Dependency Management, Exception handling and logging.pdf",
     "chapter-3-dependency-management-exception-handling-and-logging",
     "Chapter 3: Dependency Management, Exception Handling and Logging"),
    ("Chapter 04 Advanced OO concepts-up.pdf",
     "chapter-4-advanced-oo-concepts", "Chapter 4: Advanced OO Concepts"),
    ("Chapter 05 concurrency_up.pdf",
     "chapter-5-multithreading-and-concurrency", "Chapter 5: Multithreading, Parallel Programming and Concurrency"),
    ("Chapter 06 Java frameworks - Spring_up.pdf",
     "chapter-6-rest-apis-and-spring-boot", "Chapter 6: APIs and Contracts, REST, Spring and Spring Boot"),
    ("Chapter 07 software  security_up.pdf",
     "chapter-7-software-security", "Chapter 7: Software Security"),
]

COURSE = {
    "code": "SE411", "name": "Software Construction", "section": "software-engineering",
    "url": "/academics/software-engineering/se411/",
    "decks": [(src, slug, title, "", "") for src, slug, title in DECKS],
}

ARROW = ('<div class="dir-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="square"><path d="M5 12h14M12 5l7 7-7 7" /></svg></div>')


def write_listing():
    path = os.path.join(base.course_dir(COURSE), "slides", "index.html")
    page = base.read(path)
    if re.search(r'<div\s+class="directory-container', page):
        return  # build_slide_hub.py already owns this page
    rows = "".join(
        '<a href="%sslides/%s/" class="dir-row"><div class="dir-num">%02d</div><div class="dir-title">%s</div>'
        '<div class="dir-status"><span class="status-tag available">AVAILABLE</span></div>%s</a>'
        % (COURSE["url"], slug, i, base.esc(title), ARROW)
        for i, (_src, slug, title, *_r) in enumerate(COURSE["decks"], 1))
    listing = ('<div class="directory-container"><div class="dir-header"><span>SEQ</span><span>DESCRIPTOR</span>'
               '<span>SYS_STATE</span><span></span></div>%s</div>' % rows)
    start = re.search(r'<div\s+class="coming-soon-container"', page).start()
    depth = 0
    for m in re.finditer(r'<div\b|</div>', page[start:]):
        depth += 1 if m.group(0) == '<div' else -1
        if depth == 0:
            stop = start + m.end()
            break
    base.write(path, page[:start] + listing + page[stop:])


def main():
    base.move_decks(COURSE)
    base.build_viewers(load_data(), COURSE)
    write_listing()
    print("SE411: %d decks" % len(DECKS))


if __name__ == "__main__":
    main()
