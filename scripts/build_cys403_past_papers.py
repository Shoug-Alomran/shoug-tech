#!/usr/bin/env python3
"""Build the CYS403 past-paper exam pages from an existing CYS403 quiz page.

The quiz engine used to be cloned from the ETHCS303 business-ethics quiz, but that
page is maintained separately and has since been rewritten, so the swaps in
build_cys403_study_tools.quiz_page no longer match it. The CYS403 pages that
builder already produced carry the same engine and CYS403 branding, so one of them
is the template here: only the titles, counts, canonical URLs and the SECTIONS
data change.

    python3 scripts/build_cys403_past_papers.py

Content lives in cys403_study/exams.py; entries whose slug starts with "past-" are
built by this script. Re-running overwrites the pages, and the exams hub listing
and the sidebar JSON are refreshed to match.
"""
from __future__ import annotations

import importlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_cys403_study_tools as core  # noqa: E402

BASE_PAGE = core.BASE / "exams/07-quiz-1-practice-exam/quiz-1-practice-exam.html"
BASE_URL = f"{core.SITE}{core.URL}/exams/07-quiz-1-practice-exam/quiz-1-practice-exam.html"
BASE_NAME = "Quiz 1 Practice Exam"
BASE_SHORT = "Quiz 1"
BASE_HEADING = "Quiz 1 practice exam (Chapters 1–2)"
BASE_DESC_RE = re.compile(r"Chapters 1–2 — exam-style practice covering[^\"<]*")


def loose(sentence: str) -> re.Pattern:
    """Match a sentence however the formatter has re-wrapped it."""
    return re.compile(r"\s+".join(map(re.escape, sentence.split())))


def page(name: str, short: str, heading: str, scope: str, quiz: dict, url: str, template: str) -> str:
    sections = core.quiz_sections(quiz)
    count = sum(len(s["qs"]) for s in sections)
    types = {q["type"] for s in sections for q in s["qs"]}
    desc = f"{scope} — exam-style practice covering " + ", ".join(s["label"].lower() for s in sections) + ", with instant feedback."

    t = template.replace(BASE_URL, url)
    t = t.replace(f"CYS403 · {BASE_NAME}", core.esc(f"CYS403 · {name}"))
    t = t.replace(f"CYS403 {BASE_SHORT} Study Tool", core.esc(f"CYS403 {short} Study Tool"))
    t = BASE_DESC_RE.sub(core.esc(desc), t)
    t, n = loose(f"<h1>{BASE_HEADING}</h1>").subn(f"<h1>{core.esc(heading)}</h1>", t)
    if not n:
        raise SystemExit("template drift: quiz heading not found")
    t = re.sub(r'(<div class="progress-pill" id="prog-pill">)0 / \d+', rf"\g<1>0 / {count}", t)
    t = re.sub(r'(<span class="dot"></span>\s*)\d+ questions', rf"\g<1>{count} questions", t)
    t = re.sub(r'(<span class="dot amber"></span>\s*)\d+ question types', rf"\g<1>{len(types)} question types", t)

    start = t.index("const SECTIONS = ")
    end = re.search(r"\n[ \t]*let submitted = false;", t)
    if end is None:
        raise SystemExit("template drift: end of SECTIONS block not found")
    t = t[:start] + "const SECTIONS = " + json.dumps(sections, ensure_ascii=False, indent=4) + ";\n" + t[end.start() + 1:]
    core.assert_clean(t, name, BASE_NAME, BASE_HEADING)
    return t


def main() -> int:
    chapters = [importlib.import_module(f"cys403_study.ch{n:02d}") for n in range(1, 7)]
    extras = importlib.import_module("cys403_study.exams").EXAMS
    template = BASE_PAGE.read_text(encoding="utf-8")
    wrapper_ref = core.REF_QUIZ_WRAPPER.read_text(encoding="utf-8")

    quizzes = [(f"{ch.NUMBER:02d}-{ch.SLUG}-quiz", f"{ch.SLUG}-quiz", f"Chapter {ch.NUMBER} Quiz", ch) for ch in chapters]
    quizzes += [(f"{len(chapters) + i:02d}-{ex['slug']}", ex["slug"], ex["label"], ex) for i, ex in enumerate(extras, 1)]
    hrefs = [f"{core.URL}/exams/{folder}/" for folder, *_ in quizzes]

    built = []
    for i, (folder, stem, name, spec) in enumerate(quizzes):
        if not isinstance(spec, dict) or not spec["slug"].startswith("past-"):
            continue
        out = core.BASE / "exams" / folder
        out.mkdir(parents=True, exist_ok=True)
        out.joinpath(f"{stem}.html").write_text(
            page(name, spec["short"], spec["heading"], spec["scope"], spec["quiz"],
                 f"{core.SITE}{hrefs[i]}", template), encoding="utf-8")
        out.joinpath("index.html").write_text(
            core.quiz_wrapper(folder, f"{stem}.html", name, i + 1, wrapper_ref, hrefs, i), encoding="utf-8")
        built.append(folder)

    titles = [f"{name}: {spec.TITLE}" if not isinstance(spec, dict) else f"{name} ({spec['scope']})"
              for _f, _s, name, spec in quizzes]
    hub = core.BASE / "exams/index.html"
    hub.write_text(core.replace_main_listing(hub.read_text(encoding="utf-8"),
                                             core.listing([(h, core.esc(t)) for h, t in zip(hrefs, titles)])),
                   encoding="utf-8")
    core.update_sidebar({f"{core.URL}/exams/": [{"url": h, "attrs": "", "label": t} for h, t in zip(hrefs, titles)]})
    from apply_cyber_red_theme import apply_tree
    apply_tree([core.BASE / "exams"])
    print(f"Built {len(built)} CYS403 past paper(s): {', '.join(built)}")
    print("Run scripts/build_academic_sidebar.py next (scope it to cys403).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
