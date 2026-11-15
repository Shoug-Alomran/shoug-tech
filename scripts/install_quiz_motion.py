#!/usr/bin/env python3
"""Link the shared colour-and-motion layer into every course's exam pages.

Adds /styles/quiz-motion.css and /javascripts/quiz-motion.js to the exam
content pages under docs/academics/*/*/exams/ (the files the exam wrappers
iframe, not the wrappers or listings). Skipped: ETHCS303 (the paid course,
sealed at deploy) and CS331, whose pages already have their own colourful theme
(cs331-past-paper.css + cs331-paper-fx.js).

Course builders don't include the tags, so re-run this after regenerating
exams. Idempotent.

    python3 scripts/install_quiz_motion.py           # install
    python3 scripts/install_quiz_motion.py --check   # list pages missing it; exit 1 if any
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACADEMICS = ROOT / "docs/academics"
SKIP = {"ethcs303", "cs331"}
TAGS = (
    '<link rel="stylesheet" href="/styles/quiz-motion.css" />\n'
    '<script defer src="/javascripts/quiz-motion.js"></script>\n'
)


def quiz_pages():
    for page in sorted(ACADEMICS.glob("*/*/exams/**/*.html")):
        course = page.relative_to(ACADEMICS).parts[1]
        if page.name == "index.html" or course in SKIP:
            continue
        text = page.read_text(encoding="utf-8")
        if "</head>" not in text:
            continue
        yield page, text


def main() -> int:
    check = "--check" in sys.argv
    missing = []
    for page, text in quiz_pages():
        if "quiz-motion.js" in text:
            continue
        missing.append(page)
        if not check:
            # Last in <head>, so its rules come after the page's own CSS.
            page.write_text(re.sub(r"</head\s*>", TAGS + "</head>", text, count=1), encoding="utf-8")
    for page in missing:
        print(("missing: " if check else "linked: ") + str(page.relative_to(ROOT)))
    print(f"{len(missing)} page(s) {'missing the motion layer' if check else 'updated'}")
    return 1 if check and missing else 0


if __name__ == "__main__":
    sys.exit(main())
