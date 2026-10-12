#!/usr/bin/env python3
"""Add the "Review mistakes" tracker to every quiz page.

Quiz content pages (docs/academics/**/exams/**/*-quiz.html) come from several
builders, so the tracker is installed here rather than in each builder. Safe
to re-run; run it again after regenerating any quizzes.

    python3 scripts/install_quiz_review.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAG = '<script src="/javascripts/quiz-mistakes.js" defer></script>'


def main() -> int:
    added = 0
    pages = sorted((ROOT / "docs" / "academics").glob("**/exams/**/*-quiz.html"))
    for page in pages:
        text = page.read_text(encoding="utf-8")
        if TAG in text or "</body>" not in text:
            continue
        i = text.rindex("</body>")
        page.write_text(text[:i] + "    " + TAG + "\n  " + text[i:], encoding="utf-8")
        added += 1
    print(f"Tracker added to {added} of {len(pages)} quiz pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
