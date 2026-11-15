#!/usr/bin/env python3
"""Add "Past exam" notes to a course's slide breakdowns.

The questions come from the course's annotated-slide content modules (the exam items with kind 'past',
which are only ever copied from the real papers in exams/), so the breakdowns and the annotated slides
always agree. scripts/past_exam_notes/<course>.json maps each deck's slide numbers to the breakdown
section the point is taught in:

    {"breakdowns": "docs/academics/.../slide-breakdowns", "annotated_package": "se322_annotated",
     "decks": {"ch01": {"page": "01-", "sections": {"4": "foundations", ...}}}}

Each section gets one block at its end, listing every past question for that point: the paper, question
number and marks (linked to the exam page), the question as it was asked, and the model answer in a
collapsed <details>. Re-running replaces the blocks, so it is safe to run after editing the questions.

    python3 scripts/build_past_exam_notes.py se322
"""
from __future__ import annotations

import hashlib
import html
import importlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
CSS_URL = "/styles/past-exam-notes.css"
BLOCK_RE = re.compile(r"\s*<!-- past-exam:start -->.*?<!-- past-exam:end -->", re.S)
LINK_RE = re.compile(r'\s*<link rel="stylesheet" href="/styles/past-exam-notes\.css[^"]*" />')


def md(text: str) -> str:
    """The content modules use **bold** and `code`; everything else is plain text."""
    out = html.escape(str(text), quote=False)
    out = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", out)
    out = re.sub(r"`(.+?)`", r"<code>\1</code>", out)
    return out.replace("\\*", "*")


def answer_html(q: dict) -> str:
    if q.get("opts") is not None and isinstance(q.get("a"), int):
        return f"<b>{'abcdefgh'[q['a']]})</b> {md(q['opts'][q['a']])}"
    if q.get("opts") is not None and isinstance(q.get("a"), (list, tuple)):
        return "; ".join(md(q["opts"][i]) for i in q["a"])
    if q.get("tf") is not None:
        return "<b>True</b>" if q["tf"] else "<b>False</b>"
    return md(q.get("a") or "")


def paper_href(q: dict, papers: dict, exams_url: str) -> str:
    if q.get("href"):
        return q["href"]
    for title, folder in papers.values():
        if q["ref"].startswith(title):
            return f"{exams_url}{folder}/"
    return exams_url


def item_html(q: dict, papers: dict, exams_url: str) -> str:
    ref = q["ref"]
    paper, _, where = ref.partition(" · ")
    if paper.startswith("Quiz") and " · " in where:  # "Quiz 1 · 261 · Q8" -> paper "Quiz 1 · 261"
        extra, _, where = where.partition(" · ")
        paper = f"{paper} · {extra}"
    opts = ""
    if q.get("opts") is not None:
        opts = '<ol class="pex-opts" type="a">' + "".join(f"<li>{md(o)}</li>" for o in q["opts"]) + "</ol>"
    why = f'<p class="pex-why">{md(q["why"])}</p>' if q.get("why") else ""
    return (
        '<li class="pex-item">'
        f'<p class="pex-ref"><a href="{paper_href(q, papers, exams_url)}">{html.escape(paper)}</a>'
        f'<span>{html.escape(where)}</span></p>'
        f'<p class="pex-q">{md(q["q"])}</p>{opts}'
        f'<details class="pex-ans"><summary>What the marker wanted</summary><p>{answer_html(q)}</p>{why}</details>'
        "</li>"
    )


def block_html(items: list[str]) -> str:
    n = len(items)
    return (
        "\n<!-- past-exam:start -->"
        f'<aside class="pex" aria-label="Past exam questions on this section">'
        f'<p class="pex-head"><span class="pex-tag">Past exam</span>'
        f'{"This point came up in a real paper" if n == 1 else f"This point came up {n} times in real papers"}</p>'
        f'<ol class="pex-list">{"".join(items)}</ol></aside>'
        "<!-- past-exam:end -->\n"
    )


def section_end(text: str, section_id: str) -> int:
    m = re.search(r'<section\b[^>]*\bid="%s"' % re.escape(section_id), text)
    if not m:
        raise SystemExit(f"section #{section_id} not found")
    depth, pos = 0, m.start()
    for t in re.finditer(r"<(/?)section\b", text[m.start():]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            return m.start() + t.start()
    raise SystemExit(f"section #{section_id} is not closed")


def css_link() -> str:
    digest = hashlib.sha1((ROOT / "docs" / CSS_URL.lstrip("/")).read_bytes()).hexdigest()[:10]
    return f'\n    <link rel="stylesheet" href="{CSS_URL}?v={digest}" />'


def build(course: str) -> int:
    cfg = json.loads((SCRIPTS / "past_exam_notes" / f"{course}.json").read_text())
    sys.path.insert(0, str(SCRIPTS))
    common = importlib.import_module(f"{cfg['annotated_package']}.common")
    papers = getattr(common, "PAPERS", {})
    folder = ROOT / cfg["breakdowns"]
    total = 0
    for deck, spec in cfg["decks"].items():
        mod = importlib.import_module(f"{cfg['annotated_package']}.{deck}_page")
        by_section: dict[str, list[str]] = {}
        for n, slide in sorted(mod.SLIDES.items()):
            for q in slide.get("exam", ()):
                if q.get("kind") != "past":
                    continue
                sec = spec["sections"].get(str(n))
                if not sec:
                    raise SystemExit(f"{deck} slide {n} has a past question but no section mapping")
                by_section.setdefault(sec, []).append(item_html(q, papers, cfg["exams_url"]))
        page = next(p for p in sorted(folder.glob(spec["page"] + "*/*.html")) if p.name != "index.html")
        text = BLOCK_RE.sub("", page.read_text())
        text = LINK_RE.sub("", text)
        # insert from the bottom up so earlier offsets stay valid
        for sec, items in sorted(by_section.items(), key=lambda kv: -section_end(text, kv[0])):
            at = section_end(text, sec)
            text = text[:at] + block_html(items) + text[at:]
        if by_section:
            text = text.replace("</head>", css_link() + "\n  </head>", 1)
        page.write_text(text)
        count = sum(len(v) for v in by_section.values())
        total += count
        print(f"{page.parent.name}: {count} past question(s) in {len(by_section)} section(s)")
    print(f"{course}: {total} past-exam notes")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    raise SystemExit(build(sys.argv[1]))
