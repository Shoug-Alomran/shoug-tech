#!/usr/bin/env python3
"""Build every CYS403 study page from the chapter slides.

Mirrors the CYS405 course layout:
    slides/chapter-N-<slug>/                  PDF viewer (cloned from CYS405)
    slide-breakdowns/NN-chapter-N-<slug>/     study guide + wrapper (CYS405 breakdown chrome)
    extra-resources/mindmaps/NN-<slug>/       Ethics-style mindmap + wrapper
    exams/NN-<slug>-quiz/                     multi-format practice quiz + wrapper
    exams/07-quiz-1-practice-exam/, 08-major-exam-practice/   cumulative exams
plus the hub listings and scripts/academic-sidebar.json entries.

Content lives in scripts/cys403_study/: chNN.py per chapter (SECTIONS, TIPS, QUICK
for the breakdown; BRANCHES for the mindmap; QUIZ for the practice quiz) and exams.py.
Quizzes reuse the ETHCS303 quiz engine (MCQ, true/false, fill-in, matching, short answer).

    python3 scripts/build_cys403_study_tools.py
Then run build_academic_sidebar.py to stamp the sidebars.
"""
from __future__ import annotations

import hashlib
import html
import importlib
import json
import re
import shutil
import zlib
from pathlib import Path

import build_se311_mindmaps as maps_core
from build_cys405_cys406_study_tools import replace_main_listing

swap = maps_core.swap
ROOT = Path(__file__).resolve().parents[1]
SITE = "https://shoug-tech.com"
CYBER = ROOT / "docs/academics/cybersecurity"
BASE = CYBER / "cys403"
URL = "/academics/cybersecurity/cys403"
REF = CYBER / "cys405"
SIDEBAR = ROOT / "scripts/academic-sidebar.json"

REF_VIEWER = REF / "slides/chapter-3-scanning/index.html"
REF_BREAKDOWN = REF / "slide-breakdowns/03-chapter-3-scanning/chapter-3-scanning.html"
REF_BREAKDOWN_WRAPPER = REF / "slide-breakdowns/03-chapter-3-scanning/index.html"
REF_MAP_WRAPPER = REF / "extra-resources/mindmaps/03-scanning/index.html"
REF_QUIZ_WRAPPER = REF / "exams/03-scanning-quiz/index.html"
QUIZ_TEMPLATE = ROOT / "docs/academics/other-courses/ethcs303/exams/16-business-ethics-quiz/business-ethics.html"
QUIZ_TEMPLATE_URL = f"{SITE}/academics/other-courses/ethcs303/exams/16-business-ethics-quiz/"
REF_BREAKDOWN_URL = f"{SITE}/academics/cybersecurity/cys405/slide-breakdowns/03-chapter-3-scanning/chapter-3-scanning.html"

# Superseded hand-made pages from before this builder (their content lives on in git history).
STALE = ["slide-breakdowns/01-security-risk-management-governance-and-control",
         "slide-breakdowns/02-risk-management-fundamentals",
         "slide-breakdowns/03-threat-and-vulnerability-management",
         "slide-breakdowns/04-risk-management-lifecycle",
         "extra-resources/mindmap"]

ACCENTS = ["a", "b", "c", "d", "e", "f"]
AR_MINDMAPS = "الخرائط الذهنية"
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square"><path d="M5 12h14M12 5l7 7-7 7"/></svg>'
FOLDER_ICON = '<svg class="dir-folder-icon" style="width:1.15em;height:1.15em;margin-right:.55em;vertical-align:-.18em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 7a1 1 0 0 1 1-1h5l2 2h9a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V7z"/></svg>'
THEME_ICONS = json.dumps({"dark": maps_core.MOON, "light": maps_core.SUN})
SIDEBAR_NAV = re.compile(r'<nav class="[^"]*academic-sidebar.*?</nav>', re.S)
esc = html.escape


# --------------------------------------------------------------------------- naming

def label(ch) -> str:
    return f"Chapter {ch.NUMBER}: {ch.TITLE}"


def slides_folder(ch) -> str:
    return f"chapter-{ch.NUMBER}-{ch.SLUG}"


def breakdown_folder(ch) -> str:
    return f"{ch.NUMBER:02d}-chapter-{ch.NUMBER}-{ch.SLUG}"


def map_folder(ch) -> str:
    return f"{ch.NUMBER:02d}-{ch.SLUG}"


# --------------------------------------------------------------------------- shared helpers

def retarget(text: str, pairs: list[tuple[str, str]]) -> str:
    text = text.replace("cys405", "cys403").replace("CYS405", "CYS403")
    for old, new in pairs:
        text = swap(text, old, new, count=None)
    return text


def with_nav(text: str, hrefs: list[str], index: int, hub: str) -> str:
    prev = hrefs[index - 1] if index else hub
    nxt = hrefs[index + 1] if index + 1 < len(hrefs) else hub
    links = (f'<a href="{prev}" class="nav-link prev">&lt;- PREVIOUS</a>'
             f'<a href="{nxt}" class="nav-link next">NEXT -&gt;</a>')
    text, n = re.subn(r'<div class="(nav-strip[^"]*)">.*?</div>', lambda m: f'<div class="{m.group(1)}">{links}</div>', text, count=1, flags=re.S)
    if n != 1:
        raise SystemExit("template drift: nav strip not found")
    return text


def assert_clean(text: str, where: str, *words: str) -> None:
    body = SIDEBAR_NAV.sub("", text)
    for word in words:
        if word in body:
            raise SystemExit(f"{where}: leftover {word!r} from the reference page")


# --------------------------------------------------------------------------- slides

def relocate_slides(chapters: list) -> None:
    slides = BASE / "slides"
    for ch in chapters:
        n = ch.NUMBER
        folder = slides / slides_folder(ch)
        folder.mkdir(exist_ok=True)
        target = folder / f"{slides_folder(ch)}.pdf"
        if not target.exists():
            candidates = [slides / f"chapter-{n}.pdf", folder / f"chapter-{n}.pdf", slides / f"chapter-{n}" / f"chapter-{n}.pdf"]
            source = next((c for c in candidates if c.exists()), None)
            if source is None:
                raise SystemExit(f"no slides PDF found for chapter {n}")
            shutil.move(source, target)
        old_viewer = slides / f"chapter-{n}"
        if old_viewer.is_dir():
            shutil.rmtree(old_viewer)


def viewer_page(ch, ref: str, hrefs: list[str], index: int) -> str:
    t = retarget(ref, [("chapter-3-scanning", slides_folder(ch)), ("Chapter 3 Scanning", esc(label(ch))),
                       ("ITEM_03", f"ITEM_{ch.NUMBER:02d}")])
    t = with_nav(t, hrefs, index, f"{URL}/slides/")
    assert_clean(t, f"slides {ch.NUMBER}", "canning")
    return t


# --------------------------------------------------------------------------- breakdowns

def section_html(number: int, kicker: str, title: str, body: str) -> str:
    grad = ["ga", "gb", "gc", "gd"][(number - 1) % 4]
    return (f'      <section id="s-{number:02d}">\n        <div class="section-header">\n          <span class="sec-num">{number:02d} / {kicker}</span>\n'
            f'          <div class="sec-line"></div>\n        </div>\n        <h2 class="{grad}">{title}</h2>\n        {body}\n      </section>\n')


def header_bar(ch, titles: list[str]) -> str:
    """Sticky page header: contents menu, page search slot and theme toggle.

    html-theme-sync.js mounts its page search into [data-page-search-host];
    study-guide.js highlights the section in view in the contents menu.
    """
    from cys403_study.blocks import plain
    links = "".join(f'<li><a href="#s-{i:02d}"><span class="bdx-toc-num">{i:02d}</span>{esc(plain(t))}</a></li>'
                    for i, t in enumerate(titles, 1))
    return ('    <header class="bdx-bar">\n      <div class="bdx-bar-inner">\n'
            f'        <a class="bdx-bar-title" href="#top">CYS403 <span>Chapter {ch.NUMBER}</span></a>\n'
            '        <nav class="bdx-toc" aria-label="Contents">\n'
            '          <button type="button" class="bdx-toc-toggle" aria-expanded="false" aria-controls="bdx-toc-list">'
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">'
            '<path d="M4 6h16M4 12h10M4 18h13"/></svg><span>Contents</span>'
            f'<span class="bdx-toc-count">01 / {len(titles):02d}</span></button>\n'
            f'          <ol class="bdx-toc-list" id="bdx-toc-list">{links}</ol>\n        </nav>\n'
            '        <div class="bdx-bar-search" data-page-search-host></div>\n'
            '        <button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle theme">'
            '<span class="toggle-icon" id="toggle-icon"></span><span id="toggle-label">Light Mode</span></button>\n'
            '      </div>\n    </header>\n')


def figures_by_section(ch) -> dict[int, list[str]]:
    """Slide diagrams from cys403_study/figures.py as figure blocks, keyed by section number."""
    from PIL import Image
    from cys403_study.blocks import figure
    from cys403_study.figures import FIGURES, image_name
    folder = BASE / "slide-breakdowns" / breakdown_folder(ch) / "figures"
    out: dict[int, list[str]] = {}
    for page, _box, section, caption in FIGURES.get(ch.NUMBER, []):
        if not 1 <= section <= len(ch.SECTIONS):
            raise SystemExit(f"figures.py: chapter {ch.NUMBER} slide {page} points at missing section {section}")
        path = folder / image_name(page)
        if not path.exists():
            raise SystemExit(f"{path.relative_to(ROOT)} missing: run scripts/extract_cys403_figures.py")
        with Image.open(path) as im:
            width, height = im.size
        out.setdefault(section, []).append(figure(f"figures/{image_name(page)}", caption, width, height, page))
    return out


def with_figures(blocks: list[str], figures: list[str]) -> list[str]:
    """Place figures after a section's teaching content, ahead of its closing tips and memory tricks."""
    at = len(blocks)
    while at > 1 and blocks[at - 1].startswith(('<div class="tip ', '<div class="mnemonic')):
        at -= 1
    return blocks[:at] + figures + blocks[at:]


def flashcard_deck(rows: list[list[str]]) -> str:
    """Flip cards built from the quick-reference table: topic on the front, key point on the back."""
    from cys403_study.blocks import plain
    cards = "".join(
        f'<button type="button" class="bdx-card" aria-pressed="false" style="--bdx-i:{i % 8}">'
        f'<span class="bdx-card-inner"><span class="bdx-card-face bdx-front"><span class="bdx-card-kicker">Card {i + 1:02d}</span>'
        f'<span class="bdx-card-topic">{esc(plain(topic))}</span><span class="bdx-card-hint">Tap to reveal</span></span>'
        f'<span class="bdx-card-face bdx-back">{esc(plain(point))}</span></span></button>'
        for i, (topic, point) in enumerate(rows))
    return ('<p>Say the answer out loud, then flip the card to check. Shuffle the deck to test yourself in a new order.</p>'
            '<div class="bdx-deck-bar"><button type="button" class="bdx-shuffle">'
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">'
            '<path d="M16 3h5v5M4 20 21 3M21 16v5h-5M15 15l6 6M4 4l5 5"/></svg>Shuffle deck</button></div>'
            f'<div class="bdx-deck">{cards}</div>')


def versioned(url: str) -> str:
    """Asset URL with a content hash, so browsers drop a cached copy whenever the file changes."""
    digest = hashlib.sha1((ROOT / "docs" / url.lstrip("/")).read_bytes()).hexdigest()[:10]
    return f"{url}?v={digest}"


def breakdown_page(ch, ref: str) -> str:
    title = f"CYS403 - Chapter {ch.NUMBER}: {ch.TITLE}"
    url = f"{SITE}{URL}/slide-breakdowns/{breakdown_folder(ch)}/chapter-{ch.NUMBER}-{ch.SLUG}.html"
    desc = f"A comprehensive study guide to CYS403 Chapter {ch.NUMBER}: {ch.TITLE} — {ch.SUMMARY}"

    head = ref[:ref.index("</head>")]
    head = swap(head, "CYS405 - Chapter 3: Scanning", esc(title), count=None)
    head, n = re.subn(r'content="A comprehensive study guide to CYS405 Chapter 3: Scanning[^"]*"', lambda _m: f'content="{esc(desc)}"', head)
    if n != 3:
        raise SystemExit("template drift: breakdown descriptions")
    head, n = re.subn(r'"description": "A comprehensive study guide[^"]*"', lambda _m: '"description": ' + json.dumps(desc, ensure_ascii=False), head)
    if n != 1:
        raise SystemExit("template drift: breakdown structured data")
    head = swap(head, REF_BREAKDOWN_URL, url, count=None)
    assert_clean(head, f"breakdown {ch.NUMBER} head", "cys405", "Scanning")

    tail = ref[ref.index("<script>\n      // Auto-detect"):]
    tail = swap(tail, "<script>\n      // Auto-detect", f"<script>\n      const THEME_ICONS = {THEME_ICONS};\n      // Auto-detect")
    tail = swap(tail, 'icon.textContent = "☀️";', "icon.innerHTML = THEME_ICONS.light;")
    tail = swap(tail, 'icon.textContent = "🌙";', "icon.innerHTML = THEME_ICONS.dark;")

    chips = "".join(f'<span class="chip chip-{ACCENTS[i % 6]}">{c}</span>' for i, c in enumerate(ch.CHIPS))
    body = [
        '  <body id="top">\n',
        f'    <div class="hero">\n      <div class="hero-grid"></div>\n      <div class="hero-badge"><span class="badge-dot"></span>CYS403 · Chapter {ch.NUMBER}</div>\n'
        f'      <h1>{ch.HOOK}<br /><span class="gradient-word">{ch.GRADIENT}</span></h1>\n      <p class="hero-sub">{ch.SUB}</p>\n'
        f'      <div class="hero-chips">{chips}</div>\n      <div class="scroll-hint">scroll ↓</div>\n    </div>\n\n    <main>\n',
    ]
    extra_titles = ["Exam Tips &amp; Tricks", "Flashcards — Test Yourself", "Quick Reference — Everything at a Glance"]
    body.insert(1, header_bar(ch, [heading for _k, heading, _b in ch.SECTIONS] + extra_titles))
    figures = figures_by_section(ch)
    number = 0
    for number, (kicker, heading, blocks) in enumerate(ch.SECTIONS, 1):
        body.append(section_html(number, kicker, heading, "".join(with_figures(list(blocks), figures.get(number, [])))))
    kinds = ["info", "good", "exam", "warn"]
    from cys403_study.blocks import tip, table
    tips = '<div class="grid2">' + "".join(tip(kinds[i % 4], t, d) for i, (t, d) in enumerate(ch.TIPS)) + "</div>"
    body.append(section_html(number + 1, "Exam Prep", extra_titles[0], tips))
    body.append(section_html(number + 2, "Self-Test", extra_titles[1], flashcard_deck(ch.QUICK)))
    body.append(section_html(number + 3, "Cheat Sheet", extra_titles[2], table(["Topic", "Key Point"], *ch.QUICK)))
    head += f'    <link rel="stylesheet" href="{versioned("/styles/study-guide.css")}" />\n  '
    tail = swap(tail, "</body>", f'    <script src="{versioned("/javascripts/study-guide.js")}" defer></script>\n  </body>')
    body.append(f'    </main>\n\n    <footer>\n      <div class="footer-name">Made by Shoug Alomran</div>\n'
                f'      <div class="footer-sub">CYS403 · Chapter {ch.NUMBER}: {esc(ch.TITLE)} · Study Guide</div>\n    </footer>\n\n    ')
    return head + "</head>\n\n" + "".join(body) + tail


def breakdown_wrapper(ch, ref: str, hrefs: list[str], index: int) -> str:
    name = esc(label(ch))
    folder = breakdown_folder(ch)
    t = retarget(ref, [("03-chapter-3-scanning/chapter-3-scanning.html", f"{folder}/chapter-{ch.NUMBER}-{ch.SLUG}.html"),
                       ("03-chapter-3-scanning/", f"{folder}/"), ("Breakdown: Chapter 3 Scanning", f"Breakdown: {name}"),
                       ("Chapter Chapter 3 Scanning", name), ("Chapter 3 Scanning", name), ("ITEM_03", f"ITEM_{ch.NUMBER:02d}")])
    t = with_nav(t, hrefs, index, f"{URL}/slide-breakdowns/")
    assert_clean(t, f"breakdown wrapper {ch.NUMBER}", "canning")
    return t


# --------------------------------------------------------------------------- mindmaps

def map_wrapper(ch, ref: str, hrefs: list[str], index: int) -> str:
    t = retarget(ref, [("mindmaps/03-scanning/", f"mindmaps/{map_folder(ch)}/"), ("./scanning.html", f"./{ch.SLUG}.html"),
                       ("Chapter 3 Mindmap", f"Chapter {ch.NUMBER} Mindmap"), ("ITEM_03", f"ITEM_{ch.NUMBER:02d}")])
    # The CYS405 wrapper labels its Mindmaps breadcrumb "Exams".
    t = swap(t, f'href="{URL}/extra-resources/mindmaps/">Exams</a>', f'href="{URL}/extra-resources/mindmaps/">Mindmaps</a>')
    t = with_nav(t, hrefs, index, f"{URL}/extra-resources/mindmaps/")
    assert_clean(t, f"mindmap wrapper {ch.NUMBER}", "canning")
    return t


# --------------------------------------------------------------------------- quizzes

def spread_answer(text: str, opts: list[str], ans: int) -> tuple[list[str], int]:
    """Move the correct option to a stable, question-specific slot so answers aren't clustered on B.

    Number-only option lists (percentages, counts) keep their natural order.
    """
    if all(re.fullmatch(r"[\d.,%$ ]+", o) for o in opts):
        return opts, ans
    target = zlib.crc32(text.encode()) % len(opts)
    rest = [o for i, o in enumerate(opts) if i != ans]
    return rest[:target] + [opts[ans]] + rest[target:], target


def quiz_sections(quiz: dict) -> list[dict]:
    sections = []

    def add(section_label: str, items: list[dict]) -> None:
        if items:
            sections.append({"id": chr(65 + len(sections)), "label": section_label, "qs": items})

    def fill(rows):
        return [{"type": "fill", "text": t, "ans": a, "kw": [k.lower() for k in kw], "exp": e, "tag": g} for t, a, kw, e, g in rows]

    for text, opts, ans, _exp, _tag in quiz.get("mcq", []):
        if not 0 <= ans < len(opts):
            raise SystemExit(f"MCQ answer index out of range: {text[:60]}")
    for _text, _tag, pairs in quiz.get("match", []):
        if any('"' in d for _t, d in pairs):
            raise SystemExit("matching definitions cannot contain double quotes (used as option values)")
    add("Multiple choice", [dict(zip(("type", "text", "opts", "ans", "exp", "tag"), ("mcq", t, *spread_answer(t, o, a), e, g)))
                            for t, o, a, e, g in quiz.get("mcq", [])])
    add("True or false", [{"type": "tf", "text": t, "ans": a, "exp": e, "tag": g} for t, a, e, g in quiz.get("tf", [])])
    add("Fill in the blank", fill(quiz.get("fill", [])))
    add("Calculations", fill(quiz.get("calc", [])))
    add("Matching", [{"type": "match", "text": t, "tag": g, "pairs": [{"term": a, "def": b} for a, b in pairs]} for t, g, pairs in quiz.get("match", [])])
    add("Short answer and scenarios", [{"type": "short", "text": t, "kw": [k.lower() for k in kw], "modelAns": m, "tag": g}
                                       for t, kw, m, g in quiz.get("short", [])])
    return sections


def quiz_page(name: str, short: str, heading: str, scope: str, quiz: dict, url: str, template: str) -> str:
    sections = quiz_sections(quiz)
    count = sum(len(s["qs"]) for s in sections)
    types = {q["type"] for s in sections for q in s["qs"]}
    desc = f"{scope} — exam-style practice covering " + ", ".join(s["label"].lower() for s in sections) + ", with instant feedback."
    t = swap(template, "ETHC303 · Business Ethics Quiz", esc(f"CYS403 · {name}"), count=4)
    t = swap(t, "Based on the Business Ethics chapter — past exam questions and exam-style practice.", esc(desc), count=5)
    t = swap(t, QUIZ_TEMPLATE_URL, url, count=None)
    t = swap(t, "Business <span>Ethics</span>", f"CYS403 <span>{esc(short)}</span>")
    t = swap(t, '<div class="progress-pill" id="prog-pill">0 / 30</div>', f'<div class="progress-pill" id="prog-pill">0 / {count}</div>')
    t = swap(t, '<button id="theme-btn" onclick="toggleTheme()" aria-label="Toggle dark mode">🌙</button>',
             f'<button id="theme-btn" onclick="toggleTheme()" aria-label="Toggle dark mode">{maps_core.MOON}</button>')
    t = swap(t, "function toggleTheme() {", f"const THEME_ICONS = {THEME_ICONS};\n\n        function toggleTheme() {{")
    t = swap(t, "document.getElementById('theme-btn').textContent = isDark ? '🌙' : '☀️';",
             "document.getElementById('theme-btn').innerHTML = isDark ? THEME_ICONS.dark : THEME_ICONS.light;")
    t = swap(t, "<h1>Exam prep quiz</h1>", f"<h1>{esc(heading)}</h1>")
    t = swap(t, '<span class="dot"></span> 30 questions', f'<span class="dot"></span> {count} questions')
    t = swap(t, '<span class="dot amber"></span> 5 question types', f'<span class="dot amber"></span> {len(types)} question types')
    for emoji in ["🎉 ", "📖 ", "💪 "]:
        t = swap(t, f"'{emoji}", "'")
    t = swap(t, "Business Ethics Study Tool", f"CYS403 {esc(short)} Study Tool")
    start, end = t.index("const SECTIONS = "), t.index("        let submitted = false;")
    t = t[:start] + "const SECTIONS = " + json.dumps(sections, ensure_ascii=False, indent=4) + ";\n\n" + t[end:]
    assert_clean(t, name, "Business Ethics", "ETHC303", "ethcs303")
    return t


def quiz_wrapper(folder: str, file: str, name: str, number: int, ref: str, hrefs: list[str], index: int) -> str:
    t = retarget(ref, [("exams/03-scanning-quiz/", f"exams/{folder}/"), ("./scanning-quiz.html", f"./{file}"),
                       ("Chapter 3 Quiz", esc(name)), ("ITEM_03", f"ITEM_{number:02d}")])
    t = with_nav(t, hrefs, index, f"{URL}/exams/")
    assert_clean(t, f"quiz wrapper {name}", "canning")
    return t


# --------------------------------------------------------------------------- hubs and sidebar

def listing(rows: list[tuple[str, str]]) -> str:
    out = ['<div class="directory-container"><div class="dir-header"><span>SEQ</span><span>DESCRIPTOR</span><span>SYS_STATE</span><span></span></div>']
    for i, (href, title_html) in enumerate(rows, 1):
        out.append(f'<a class="dir-row" href="{href}"><div class="dir-num">{i:02d}</div><div class="dir-title">{title_html}</div>'
                   f'<div class="dir-status"><span class="status-tag available">AVAILABLE</span></div><div class="dir-arrow">{ARROW}</div></a>')
    return "".join(out) + "</div>"


def relabel_hub(text: str, old_title: str, new_title: str, old: tuple[str, str], new: tuple[str, str], crumb_link: str | None = None) -> str:
    """Rename a hub's title, breadcrumb and type label; `old`/`new` are (English, Arabic) section names."""
    text = swap(text, old_title, new_title, count=None)
    current = f'<span class="current" data-en-text="{new[0]}" data-ar-text="{new[1]}">{new[0]}</span>'
    if crumb_link:
        current = f'<a class="breadcrumb-link" href="{crumb_link}">{old[0]}</a> / ' + current
    text, n = re.subn(rf'<span\s+class="current"\s+data-en-text="{old[0]}"\s+data-ar-text="{old[1]}"\s*>{old[0]}</span\s*>', lambda _m: current, text, count=1)
    text, m = re.subn(rf'(class="type-label"\s+data-en-text="){old[0].upper()}("\s+data-ar-text="){old[1]}("\s*>\s*){old[0].upper()}',
                      rf"\g<1>{new[0].upper()}\g<2>{new[1]}\g<3>{new[0].upper()}", text, count=1)
    if n != 1 or m != 1:
        raise SystemExit(f"template drift: {old_title} breadcrumb/type label")
    return text


def retarget_canonical(text: str, old: str, new: str) -> str:
    """Point a cloned hub's canonical, og:url, structured data and hreflang URLs at its own folder."""
    text, n = re.subn(rf'({re.escape(SITE + URL)}/){re.escape(old)}(?=["?])', rf"\g<1>{new}", text)
    if n < 3:
        raise SystemExit(f"template drift: canonical URLs for {old}")
    return text


def move_active_tab(text: str, old: str, new: str) -> str:
    text, a = re.subn(rf'(href="{URL}/{old}"\s+class=")tab active(")', r"\g<1>tab\g<2>", text, count=1)
    text, b = re.subn(rf'(href="{URL}/{new}"\s+class=")tab(")', r"\g<1>tab active\g<2>", text, count=1)
    if a != 1 or b != 1:
        raise SystemExit("template drift: content tabs")
    return text


def update_sidebar(groups: dict[str, list[dict]]) -> None:
    # Nested item lists belong in "children"; build_academic_sidebar.py ignores them under "sections"
    # (which only holds each course's own section list), so the chapters never showed in the sidebar.
    raw = SIDEBAR.read_text()
    data = json.loads(raw)
    if f"{URL}/" not in data["sections"]:
        raise SystemExit(f"{URL}/ not found in {SIDEBAR.name}")
    for key in groups:
        data["sections"].pop(key, None)
    data["children"].update(groups)
    indent = re.match(r"[{\[]\n( +)", raw)
    out = json.dumps(data, indent=len(indent.group(1)) if indent else 2, ensure_ascii="\\u0" in raw)
    SIDEBAR.write_text(out + ("\n" if raw.endswith("\n") else ""))


# --------------------------------------------------------------------------- main

def main() -> None:
    chapters = [importlib.import_module(f"cys403_study.ch{n:02d}") for n in range(1, 7)]
    extra_exams = importlib.import_module("cys403_study.exams").EXAMS
    relocate_slides(chapters)
    for stale in STALE:
        if (BASE / stale).is_dir():
            shutil.rmtree(BASE / stale)

    viewer_ref, bd_ref, bdw_ref = REF_VIEWER.read_text(), REF_BREAKDOWN.read_text(), REF_BREAKDOWN_WRAPPER.read_text()
    map_tpl, mapw_ref = maps_core.TEMPLATE.read_text(), REF_MAP_WRAPPER.read_text()
    quiz_tpl, quizw_ref = QUIZ_TEMPLATE.read_text(), REF_QUIZ_WRAPPER.read_text()
    hubs = {name: (BASE / name / "index.html").read_text() for name in ["slide-breakdowns", "extra-resources", "exams"]}

    slide_hrefs = [f"{URL}/slides/{slides_folder(ch)}/" for ch in chapters]
    bd_hrefs = [f"{URL}/slide-breakdowns/{breakdown_folder(ch)}/" for ch in chapters]
    map_hrefs = [f"{URL}/extra-resources/mindmaps/{map_folder(ch)}/" for ch in chapters]
    quizzes = [(f"{ch.NUMBER:02d}-{ch.SLUG}-quiz", f"{ch.SLUG}-quiz", f"Chapter {ch.NUMBER} Quiz", ch) for ch in chapters]
    quizzes += [(f"{len(chapters) + i:02d}-{ex['slug']}", ex["slug"], ex["label"], ex) for i, ex in enumerate(extra_exams, 1)]
    quiz_hrefs = [f"{URL}/exams/{folder}/" for folder, *_ in quizzes]

    for i, ch in enumerate(chapters):
        (BASE / "slides" / slides_folder(ch) / "index.html").write_text(viewer_page(ch, viewer_ref, slide_hrefs, i))
        bd = BASE / "slide-breakdowns" / breakdown_folder(ch)
        bd.mkdir(parents=True, exist_ok=True)
        bd.joinpath(f"chapter-{ch.NUMBER}-{ch.SLUG}.html").write_text(breakdown_page(ch, bd_ref))
        bd.joinpath("index.html").write_text(breakdown_wrapper(ch, bdw_ref, bd_hrefs, i))
        mp = BASE / "extra-resources/mindmaps" / map_folder(ch)
        mp.mkdir(parents=True, exist_ok=True)
        mp.joinpath(f"{ch.SLUG}.html").write_text(
            maps_core.map_page(ch, map_tpl, f"{SITE}{map_hrefs[i]}{ch.SLUG}.html", f"CYS403 Chapter {ch.NUMBER}"))
        mp.joinpath("index.html").write_text(map_wrapper(ch, mapw_ref, map_hrefs, i))

    for i, (folder, stem, name, spec) in enumerate(quizzes):
        out = BASE / "exams" / folder
        out.mkdir(parents=True, exist_ok=True)
        if isinstance(spec, dict):
            page = quiz_page(name, spec["short"], spec["heading"], spec["scope"], spec["quiz"], f"{SITE}{quiz_hrefs[i]}", quiz_tpl)
        else:
            page = quiz_page(f"{name}: {spec.TITLE}", f"Chapter {spec.NUMBER}", f"Chapter {spec.NUMBER} practice quiz",
                             label(spec), spec.QUIZ, f"{SITE}{quiz_hrefs[i]}", quiz_tpl)
        out.joinpath(f"{stem}.html").write_text(page)
        out.joinpath("index.html").write_text(quiz_wrapper(folder, f"{stem}.html", name, i + 1, quizw_ref, quiz_hrefs, i))

    # Hubs: derive the new Slides and Mindmaps hubs before filling the originals.
    slides_hub = relabel_hub(hubs["slide-breakdowns"], "SHOUG.TECH | CYS403 Slide Breakdowns", "SHOUG.TECH | CYS403 Slides",
                             ("Slide Breakdowns", "تفكيك الشرائح"), ("Slides", "الشرائح"))
    slides_hub = move_active_tab(slides_hub, "slide-breakdowns/", "slides/")
    slides_hub = retarget_canonical(slides_hub, "slide-breakdowns/", "slides/")
    maps_hub = relabel_hub(hubs["extra-resources"], "SHOUG.TECH | CYS403 Study Material", "SHOUG.TECH | CYS403 Mindmaps",
                           ("Study Material", "المواد الدراسية"), ("Mindmaps", AR_MINDMAPS), crumb_link=f"{URL}/extra-resources/")
    maps_hub = retarget_canonical(maps_hub, "extra-resources/", "extra-resources/mindmaps/")
    titled = [(href, esc(label(ch))) for href, ch in zip(slide_hrefs, chapters)]
    (BASE / "slides/index.html").write_text(replace_main_listing(slides_hub, listing(titled)))
    (BASE / "slide-breakdowns/index.html").write_text(replace_main_listing(hubs["slide-breakdowns"], listing(
        [(href, esc(label(ch))) for href, ch in zip(bd_hrefs, chapters)])))
    (BASE / "extra-resources/mindmaps/index.html").write_text(replace_main_listing(maps_hub, listing(
        [(href, esc(label(ch))) for href, ch in zip(map_hrefs, chapters)])))
    quiz_titles = [f"{name}: {spec.TITLE}" if not isinstance(spec, dict) else f"{name} ({spec['scope']})" for _f, _s, name, spec in quizzes]
    (BASE / "exams/index.html").write_text(replace_main_listing(hubs["exams"], listing(
        [(href, esc(t)) for href, t in zip(quiz_hrefs, quiz_titles)])))
    (BASE / "extra-resources/index.html").write_text(replace_main_listing(hubs["extra-resources"], listing(
        [(f"{URL}/extra-resources/mindmaps/", f"{FOLDER_ICON}<span>Mindmaps</span>")])))

    entry = lambda href, text: {"url": href, "attrs": "", "label": text}
    update_sidebar({
        f"{URL}/slides/": [entry(h, label(ch)) for h, ch in zip(slide_hrefs, chapters)],
        f"{URL}/slide-breakdowns/": [entry(h, label(ch)) for h, ch in zip(bd_hrefs, chapters)],
        f"{URL}/extra-resources/": [{"url": f"{URL}/extra-resources/mindmaps/",
                                     "attrs": f'data-en-text="Mindmaps" data-ar-text="{AR_MINDMAPS}"', "label": "Mindmaps"}],
        f"{URL}/extra-resources/mindmaps/": [entry(h, label(ch)) for h, ch in zip(map_hrefs, chapters)],
        f"{URL}/exams/": [entry(h, t) for h, t in zip(quiz_hrefs, quiz_titles)],
    })
    from apply_cyber_red_theme import apply_tree
    apply_tree([BASE])
    print(f"Built CYS403: {len(chapters)} slide viewers, breakdowns, mindmaps; {len(quizzes)} practice exams. "
          "Run scripts/build_academic_sidebar.py next.")


if __name__ == "__main__":
    main()
