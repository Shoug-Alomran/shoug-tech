#!/usr/bin/env python3
"""Link the shared quiz motion layer into every cybersecurity quiz page.

Adds /styles/cyber-quiz-motion.css and /javascripts/cyber-quiz-motion.js to the
quiz content pages under docs/academics/cybersecurity/*/exams/ (the files the
exam wrappers iframe, not the wrappers themselves), including the CYS401
past-paper replicas, which the stylesheet turns into a card layout.

Course builders don't include the tags, so re-run this after regenerating
quizzes. Idempotent.

    python3 scripts/install_cyber_quiz_motion.py           # install
    python3 scripts/install_cyber_quiz_motion.py --check   # list pages missing it; exit 1 if any
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMS = ROOT / "docs/academics/cybersecurity"
TAGS = (
    '<link rel="stylesheet" href="/styles/cyber-quiz-motion.css" />\n'
    '<script defer src="/javascripts/cyber-quiz-motion.js"></script>\n'
)


def quiz_pages():
    for page in sorted(EXAMS.glob("*/exams/*/*.html")):
        if page.name == "index.html":
            continue
        text = page.read_text(encoding="utf-8")
        if "</head>" not in text:
            continue
        yield page, text


def main() -> int:
    check = "--check" in sys.argv
    missing = []
    for page, text in quiz_pages():
        if "cyber-quiz-motion.js" in text:
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
