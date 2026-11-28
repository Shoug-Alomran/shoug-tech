#!/usr/bin/env python3
"""Build the ECON102 cheat sheets: Quiz I, Major I, Quiz II, Major II, Final and the course review.

Same look as the ECON101 and CS331 sheets (the CS331 Major I sheet is the template: a tab per
section, hidden answers, Show all answers). Each sheet has:

  Plan        exam facts from the syllabus, question types and how to answer them, study order
  Chapters    one tab per chapter: big picture, vocabulary, slide map, every lesson (key points,
              tables, formulas, worked assignment problems, traps, memory tricks, pop quizzes),
              a clue -> answer table, the chapter's question bank, and links to every resource
  Compare     comparison tables across the chapters in scope
  Formulas    every formula in scope, by chapter
  Pop exam    fresh exam-style questions plus a sample of each chapter's bank
  Story       (final, course review) how the chapters connect

Lesson content comes from scripts/study_content/econ102/*.md; the rest from
scripts/econ102_cheat_content.py.

    .venv/Scripts/python.exe scripts/build_econ102_cheat_sheets.py
"""
from __future__ import annotations

import glob
import hashlib
import html
import os
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import econ102_cheat_content as content  # noqa: E402
import study_engine as engine  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "docs/academics/computer-science/cs331/extra-resources/major-1-cheat-sheet/major-1-cheat-sheet.html"
COURSE = ROOT / "docs/academics/business/econ102"
OUT = COURSE / "extra-resources/cheat-sheets"
NOTES = ROOT / "scripts/study_content/econ102"
BASE = "/academics/business/econ102/"
SITE = "https://shoug-tech.com"
esc = html.escape

# Diagrams from the teaching files use the breakdown palette; map it onto the template's.
EXTRA_CSS = """<style id="econ102-cheat">
:root, html[data-theme] { --c1: var(--accent); --c2: var(--good); --c3: var(--hook); --c4: var(--warn); --c5: hsl(0 70% 60%);
  --c6: var(--accent); --c7: var(--hook); --c8: var(--good); --text2: var(--dim); --text3: var(--dim); --bg2: var(--surface);
  --bg3: var(--surface-2); --border2: var(--border); }
.diagram { margin: .8rem 0; text-align: center; } .diagram svg { width: 100%; max-width: 34rem; height: auto; }
.diagram figcaption { font-size: .8rem; color: var(--dim); } .diagram text { font-family: var(--mono); }
.pl, .pa { fill: var(--text); font-size: 13px; } .pt { fill: var(--dim); font-size: 12px; } .pn { fill: var(--text); font-size: 13px; font-weight: 700; }
.gn { fill: var(--text); font-size: 13px; font-weight: 600; } .gl { fill: var(--dim); font-size: 12px; }
.f .prose p, .f .prose li { line-height: 1.6; } .f .prose ul { margin-left: 1.1rem; }
.opts { list-style: none; margin: .4rem 0 .2rem; padding: 0; } .opts li { margin: .15rem 0; }
.opts b { display: inline-block; width: 1.6rem; color: var(--accent); font-family: var(--mono); }
.story { display: grid; gap: .8rem; grid-template-columns: repeat(auto-fit, minmax(min(100%, 18rem), 1fr)); }
.pill { font-family: var(--mono); font-size: .68rem; letter-spacing: .06em; text-transform: uppercase; padding: .15rem .5rem;
  border: 1px solid var(--border); border-radius: 99px; color: var(--dim); margin-left: .4rem; white-space: nowrap; }
.pill.must { color: var(--warn); border-color: var(--warn); } .pill.know { color: var(--good); border-color: var(--good); }
</style>"""

LEVEL = {"must": "Must know", "know": "Good to know", "skim": "Just skim"}


# ------------------------------------------------------------------ markup helpers (CS331 template classes)
def md(text):
    return engine.md(text).replace('<div class="table-wrap">', '<div class="tbl">')


def inline(text):
    return engine.inline(text)


def card(fn, title, *parts, cls="f"):
    return f'<article class="{cls}"><header><span class="fn">{fn}</span><h4>{title}</h4></header>{"".join(parts)}</article>'


def grid(*cards, wide=False):
    return f'<div class="grid{" wide" if wide else ""}">' + "".join(cards) + "</div>"


def group(title):
    return f'<h3 class="group">{title}</h3>'


def tbl(head, rows):
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tbl"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def box(kind, label, inner):
    return f'<div class="box {kind}"><b>{label}</b>{inner}</div>'


def ul(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def kv(pairs):
    return '<dl class="kv">' + "".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in pairs) + "</dl>"


def q(tag, ask, ans):
    return (f'<div class="q"><div class="tagline">{tag}</div><div class="ask">{ask}</div>'
            f'<details><summary>Show answer</summary><div class="ans">{ans}</div></details></div>')


def links_html(links):
    return '<div class="links">' + "".join(f'<a class="btn" target="_top" href="{h}">{esc(l)}</a>' for l, h in links) + "</div>"


# ------------------------------------------------------------------ teaching files
def chapter_number(deck):
    return int(deck["slug"].split("-", 1)[0])


def load_decks():
    return {chapter_number(d): d for d in (engine.parse(p) for p in sorted(glob.glob(str(NOTES / "*.md"))))}


def resource_links(deck):
    """Slides, study pages and the instructor's material for one chapter, only where the file exists."""
    n, slug = chapter_number(deck), deck["slug"]
    out = []
    for src in [s.strip() for s in deck["sources"].split(",")]:
        if src.startswith("extra-resources/"):
            name = src.rstrip("/").split("/")[-1]
            out.append(("Student sheet (no slides)", f"{BASE}{src}/{name}.pdf"))
        else:
            out.append(("Short slides" if src.endswith("short-slides") else "Slides", f"{BASE}slides/{src}/"))
    out += [("Breakdown", f"{BASE}slide-breakdowns/{slug}/"), ("Mind map", f"{BASE}extra-resources/mindmaps/{slug}/"),
            ("Chapter quiz", f"{BASE}exams/{slug}-quiz/")]
    for folder, label in (("student-sheets", "Student sheet"), ("group-work", "Group work"), ("chapter-maps", "Chapter map")):
        for item in sorted(glob.glob(str(COURSE / "extra-resources" / folder / f"chapter-{n}-*"))):
            name = os.path.basename(item)
            if label == "Student sheet" and any(name in s for s in deck["sources"].split(",")):
                continue
            pdf = os.path.join(item, name + ".pdf")
            if os.path.exists(pdf):
                extra = " (circular flow)" if "circular-flow" in name else ""
                out.append((label + extra, f"{BASE}extra-resources/{folder}/{name}/{name}.pdf"))
    for item in sorted(glob.glob(str(COURSE / "extra-resources/assignments/*"))):
        name = os.path.basename(item)
        nums = [int(x) for x in re.findall(r"\d+", name.split("chapters-", 1)[-1])]
        if n in nums:
            out.append((name.split("-chapters")[0].replace("-", " ").title(), f"{BASE}extra-resources/assignments/{name}/{name}.pdf"))
    return out


def options(item):
    opts = [item["correct"], *item["wrong"]]
    random.Random(hashlib.sha1(item["q"].encode()).hexdigest()).shuffle(opts)
    return opts, opts.index(item["correct"])


def mcq_html(item, tag):
    opts, a = options(item)
    letters = "ABCD"
    body = inline(item["q"]) + '<ol class="opts">' + "".join(f"<li><b>{letters[i]}</b>{inline(o)}</li>" for i, o in enumerate(opts)) + "</ol>"
    return q(tag, body, f"<p><b>{letters[a]}.</b> {inline(item['correct'])}. {inline(item['why'])}</p>")


def short_html(item, tag):
    return q(tag, inline(item["q"]), f"<p>{inline(item['answer'])}</p><p><b>Key words:</b> {esc(', '.join(item['keywords']))}</p>")


def spread(items, count):
    if len(items) <= count:
        return list(items)
    return [items[i * len(items) // count] for i in range(count)]


# ------------------------------------------------------------------ one lesson -> one card
def block_html(name, arg, body, head):
    text = "\n".join(body)
    if name == "text":
        return f'<div class="prose">{md(text)}</div>'
    if name == "formula":
        exprs = "".join(f'<span class="expr">{inline(b)}</span>' for b in body if b.strip())
        cap = f"<p><b>{inline(arg)}</b></p>" if arg else ""
        return cap + f'<div class="eq">{exprs}</div>'
    if name == "steps":
        lines = "\n".join(re.sub(r"^\s*\d+\.\s*", "", b) for b in body if b.strip())
        return box("ex", inline(arg), f'<div class="work">{inline(lines.replace(chr(10), "<br>"))}</div>')
    if name == "example":
        return box("ex", inline(arg), md(text))
    if name == "key":
        return box("", "Remember", ul([inline(re.sub(r"^\s*-\s*", "", b)) for b in body if b.strip()]))
    if name == "trap":
        return box("trap", "Trap" + (": " + inline(arg) if arg else ""), md(text))
    if name == "mnemonic":
        return box("hook", "Memory trick" + (": " + inline(arg) if arg else ""), md(text))
    if name == "tip":
        return box("hook", "Exam tip" + (": " + inline(arg) if arg else ""), md(text))
    if name in ("analogy", "class", "why", "says"):
        label = {"analogy": "Think of it like this", "class": "Noted in class", "why": "Why it matters", "says": "What it means"}[name]
        return box("", label + (": " + inline(arg) if arg else ""), md(text))
    if name == "check":
        return q(f"Pop quiz · {head}", inline(arg), md(text))
    if name == "plot":
        return engine.plot(arg, body)
    if name == "graph":
        return engine.graph(arg, body)
    raise SystemExit("unknown block ::" + name)


def lesson_card(i, lesson, head):
    pills = f'<span class="pill {lesson["level"]}">{LEVEL[lesson["level"]]}</span>'
    if lesson["slides"]:
        pills += f'<span class="pill">{esc(lesson["slides"])}</span>'
    return card(str(i), inline(lesson["title"]) + pills, *(block_html(n, a, b, head) for n, a, b in lesson["blocks"]))


# ------------------------------------------------------------------ panels
def chapter_panel(deck):
    n = chapter_number(deck)
    head = deck["head"]
    intro = card("★", "The big picture",
                 f'<p><b>{inline(deck["tldr"])}</b></p>', f'<div class="prose">{md(deck["why"])}</div>',
                 box("hook", "Where this fits", f'<p>{inline(deck.get("connect", ""))}</p>'),
                 box("", "By the end you can", ul([inline(g) for g in deck["goals"]])) if deck["goals"] else "")
    side = []
    if deck["vocab"]:
        side.append(card("A–Z", "Words you need first", kv([(inline(a), inline(b)) for a, b in deck["vocab"]])))
    if deck["map"]:
        side.append(card("⌖", "Slide map: where to spend your time",
                         tbl(["Slides", "Topic", "Weight", "What to do"], [[esc(a), inline(b), w.title(), inline(c)] for a, b, w, c in deck["map"]])))
    lessons = [lesson_card(i, l, head) for i, l in enumerate(deck["lessons"], 1)]
    clues = content.CLUES.get(n, [])
    clue_card = card("?", "If the question says… think…", tbl(["Question clue", "Answer"], [[c, a] for c, a in clues])) if clues else ""
    bank = "".join(mcq_html(m, f"MCQ · {head} · slide {m['slide']}") for m in deck["mcq"])
    bank += "".join(short_html(s, f"Written · {head} · slide {s['slide']}") for s in deck["short"])
    body = (grid(intro, *side, wide=True) + group("Every lesson, in order") + grid(*lessons, wide=True)
            + group("Answer-spotting") + grid(clue_card, wide=True)
            + group(f"Pop exam: {head} question bank ({len(deck['mcq'])} MCQ, {len(deck['short'])} written)") + bank)
    return dict(id=f"ch{n}", n=str(n), tab=deck["title"].split(":")[0][:26], num=f"{head.upper()} · {esc(deck['title'].upper())}",
                title=inline(deck["title"]), links=resource_links(deck), lead=inline(deck["tldr"]), body=body)


def plan_panel(key, decks):
    exam = content.EXAMS[key]
    chapters = ", ".join(f"Ch {c}: {decks[c]['title']}" for c in exam["chapters"] if c in decks)
    facts = card("i", "Exam facts (syllabus)", kv([("Exam", exam["name"]), ("Weight", exam["weight"]), ("When", exam["when"]), ("Covers", esc(chapters))]))
    order = card("1→", "Study in this order", "<ol class=\"steps\">" + "".join(f"<li>{s}</li>" for s in content.STUDY_ORDER[key]) + "</ol>")
    top = card("!", "If you remember nothing else", ul(content.TOP_FACTS[key]))
    types = [card(str(i), t, f"<p>{how}</p>", box("hook", "How to answer", f"<p>{tip}</p>")) for i, (t, how, tip) in enumerate(content.QUESTION_TYPES, 1)]
    method = card("4", "The four-step method for any \"what happens if…\" question",
                  '<ol class="steps"><li>Name the event: spending, costs, capacity, money, or the exchange rate?</li>'
                  "<li>Pick the market or curve: AD, SAS, LAS, loanable funds, money market, foreign exchange.</li>"
                  "<li>Decide the direction of the shift and draw it.</li><li>State what happens to the variables asked about (price, quantity, rate, real GDP).</li></ol>")
    body = grid(facts, top, order, method, wide=True) + group("Question types and how they're marked") + grid(*types)
    return dict(id="plan", n="0", tab="Exam plan", num=f"{exam['name'].upper()} · PLAN", title=f"How to prepare for {exam['name']}",
                links=[], lead=f"{exam['name']} is worth {exam['weight']} of your grade. Start here, then work through each chapter tab and finish with the pop exam.", body=body)


def compare_panel(chapters):
    cards = [card(f"Ch {'/'.join(map(str, chs))}", title, tbl(head, rows))
             for chs, title, head, rows in content.COMPARISONS if any(c in chapters for c in chs)]
    return dict(id="compare", n="≠", tab="Comparisons", num="SIDE BY SIDE", title="Comparisons that prevent lost marks", links=[],
                lead="Most wrong answers come from mixing up two neighbouring ideas. Each table puts them side by side.", body=grid(*cards, wide=True))


def formula_panel(chapters, decks):
    cards = []
    for c in chapters:
        deck = decks.get(c)
        if not deck:
            continue
        parts = []
        for lesson in deck["lessons"]:
            for name, arg, body in lesson["blocks"]:
                if name == "formula":
                    parts.append(block_html(name, arg, body, deck["head"]))
        if parts:
            cards.append(card(f"Ch {c}", inline(deck["title"]), *parts))
    return dict(id="formulas", n="ƒ", tab="Formula bank", num="EVERY FORMULA", title="Formula bank", links=[],
                lead="Every formula in scope. Show formula → substitution → answer with units, and don't round until the end.", body=grid(*cards))


def pop_panel(key, chapters, decks, per_chapter):
    qs = "".join(q(t, a, ans) for t, a, ans in content.QUESTIONS.get(key, []))
    mixed = ""
    for c in chapters:
        deck = decks.get(c)
        if not deck:
            continue
        mixed += "".join(mcq_html(m, f"MCQ · {deck['head']}") for m in spread(deck["mcq"], per_chapter))
        mixed += "".join(short_html(s, f"Written · {deck['head']}") for s in spread(deck["short"], 1))
    body = (group("Part A · Exam-style problems (new numbers)") + qs
            + group("Part B · Mixed MCQ and written questions from every chapter") + mixed)
    return dict(id="pop", n="✎", tab="Pop exam", num="PRACTICE UNDER EXAM CONDITIONS", title="Pop exam", links=[],
                lead="Cover the answers, give yourself one minute per MCQ and three per calculation, then check with Show answer.", body=body)


def story_panel():
    cards = [card(t.split(" · ")[0], t.split(" · ", 1)[1], f"<p>{s}</p>") for t, s in content.STORY]
    return dict(id="story", n="∞", tab="Course story", num="THE COURSE AS ONE STORY", title="How every chapter connects", links=[],
                lead="Read this first if you're revising the whole course: it's the thread that ties the chapters together.",
                body=f'<div class="story">{"".join(cards)}</div>')


# ------------------------------------------------------------------ page assembly
def head(t, title, desc, url):
    h = t[: t.index("<body")]
    h = re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", h, flags=re.S)
    for attr in ('name="description"', 'property="og:description"'):
        h = re.sub(r'(<meta\s+%s\s+content=")[^"]*"' % attr, lambda m: m[1] + esc(desc) + '"', h)
    h = re.sub(r'(<meta\s+property="og:title"\s+content=")[^"]*"', lambda m: m[1] + esc(title) + '"', h)
    h = re.sub(r'(<link\s+rel="canonical"\s+href=")[^"]*"', lambda m: m[1] + url + '"', h)
    h = re.sub(r'(<meta\s+property="og:url"\s+content=")[^"]*"', lambda m: m[1] + url + '"', h)
    return h.replace("</head>", EXTRA_CSS + "</head>", 1)


def script(t, key):
    s = t[t.rindex("<script>", 0, t.rindex("</body>")): t.rindex("</body>")]
    return s.replace('var KEY = "cs331-major1-tab";', f'var KEY = "{key}";')


def tabs(panels):
    return "".join(
        f'<button class="tab" role="tab" id="tab-{p["id"]}" aria-controls="{p["id"]}" aria-selected="{"true" if i == 0 else "false"}"'
        f'{"" if i == 0 else " tabindex=\"-1\""}><span class="n">{esc(p["n"])}</span>{esc(p["tab"])}</button>'
        for i, p in enumerate(panels))


def panel_html(p, first):
    links = links_html(p["links"]) if p["links"] else ""
    return (f'<section class="panel" id="{p["id"]}" role="tabpanel" aria-labelledby="tab-{p["id"]}"{"" if first else " hidden"}>'
            f'<div class="ch-head"><span class="num">{p["num"]}</span><h2>{p["title"]}</h2>{links}</div>'
            f'<p class="ch-lead">{p["lead"]}</p>{p["body"]}</section>')


LEGEND = ('<div class="legend" aria-label="Legend">'
          '<div><span class="swatch" style="background: var(--accent)"></span>Formula or key fact</div>'
          '<div><span class="swatch" style="background: var(--good)"></span>Worked example (assignments, group work)</div>'
          '<div><span class="swatch" style="background: var(--warn)"></span>Exam trap</div>'
          '<div><span class="swatch" style="background: var(--hook)"></span>Memory trick or how to answer</div></div>')


def page(t, sheet, panels):
    url = f"{SITE}{BASE}extra-resources/cheat-sheets/{sheet['slug']}/"
    body = (
        '<body><header class="topbar"><div class="wrap topbar-row">'
        f'<a class="brand" href="#top">ECON102 <span>{esc(sheet["brand"])}</span></a>'
        '<div class="actions"><div data-page-search-host></div>'
        '<button class="btn" type="button" id="toggle-answers">Show all <span class="long">answers</span></button>'
        '<button class="btn" type="button" onclick="toggleTheme()"><span data-theme-label>Dark</span></button></div></div>'
        f'<div class="wrap tabs" role="tablist" aria-label="Sections">{tabs(panels)}</div></header>'
        '<main class="wrap" id="top"><div class="hero"><div>'
        f'<div class="eyebrow">{esc(sheet["eyebrow"])}</div><h1>{esc(sheet["h1"])}</h1><p>{sheet["intro"]}</p></div>{LEGEND}</div>'
        + "".join(panel_html(p, i == 0) for i, p in enumerate(panels))
        + '<footer>Built from the ECON102 slides (Parkin, <i>Macroeconomics</i>, 14th Edition), the instructor\'s short slides, '
          "student sheets, chapter maps, group work and Assignments 1–2. Every number was recomputed. Shoug Alomran.</footer></main>"
        + script(t, f"econ102-{sheet['slug']}-tab") + "</body>\n</html>\n")
    return head(t, sheet["title"], sheet["desc"], url) + body


def sheets(decks):
    out = []
    for key, exam in content.EXAMS.items():
        chs = exam["chapters"]
        scope = ", ".join(str(c) for c in chs)
        per = 3 if len(chs) > 6 else 5
        panels = [plan_panel(key, decks)]
        if key == "final":
            panels.append(story_panel())
        panels += [chapter_panel(decks[c]) for c in chs if c in decks]
        panels += [compare_panel(chs), formula_panel(chs, decks), pop_panel(key, chs, decks, per)]
        out.append((dict(slug=key, file=f"{key}-cheat-sheet.html", brand=exam["name"], h1=f"{exam['name']} cheat sheet",
                         title=f"ECON102 | {exam['name']} Cheat Sheet", eyebrow=f"ECON102 · {exam['name']} · Chapters {scope}",
                         desc=f"ECON102 {exam['name']} cheat sheet for chapters {scope}: full chapter summaries, comparison tables, a formula bank with worked assignment problems, memory tricks, exam traps and a pop exam with answers.",
                         intro=f"Everything for {exam['name']} ({exam['weight']}, chapters {scope}) in one place. Start with the exam plan, go through each chapter tab (every lesson, worked problem and trap from the slides and the instructor's material), then the comparisons and formula bank, and finish with the pop exam."),
                    panels))
    every = [c for c in sorted(decks)]
    review = [story_panel()] + [chapter_panel(decks[c]) for c in every] + [compare_panel(every), formula_panel(every, decks)]
    exams = [q(t, a, ans) for key in content.QUESTIONS for t, a, ans in content.QUESTIONS[key]]
    review.append(dict(id="pop", n="✎", tab="Pop exams", num="EVERY EXAM-STYLE PROBLEM", title="Pop exams for the whole course", links=[],
                       lead="All the exam-style problems from the five exam sheets, in course order. Each chapter tab also ends with its full question bank.",
                       body=group("Every exam-style problem") + "".join(exams)))
    out.append((dict(slug="course-review", file="course-review.html", brand="Course review", h1="ECON102 complete course review",
                     title="ECON102 Complete Course Review", eyebrow="ECON102 · Every chapter · 1, 4–14",
                     desc="The whole of ECON102 in one review: how the chapters connect, every chapter's lessons, worked problems, traps and memory tricks, comparison tables, the formula bank and pop exams with answers.",
                     intro="The whole course, connected. Read the course story, then go chapter by chapter; finish with the comparisons, the formula bank and the pop exams."),
                review))
    return out


def main():
    t = TEMPLATE.read_text(encoding="utf-8")
    decks = load_decks()
    for sheet, panels in sheets(decks):
        path = OUT / sheet["slug"] / sheet["file"]
        path.parent.mkdir(parents=True, exist_ok=True)
        text = page(t, sheet, panels)
        path.write_text(text, encoding="utf-8", newline="")
        print(f"{path.relative_to(ROOT)}: {len(panels)} tabs, {text.count('class=\"q\"')} questions, {len(text) // 1024} KB")


if __name__ == "__main__":
    main()
