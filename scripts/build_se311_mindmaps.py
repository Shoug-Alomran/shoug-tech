#!/usr/bin/env python3
"""Build one interactive mindmap per SE311 chapter.

Each map is the ETHCS303 chapter-1 mindmap page (the shared mindmap template, see
build_se401_study_tools.ETHICS_MAP_TEMPLATE; it already carries the landscape PDF
export) with the chapter's DATA, title, SEO URLs and footer swapped in.

Chapter content lives in scripts/se311_mindmaps/chNN.py:
    BRANCHES = [(branch label, intro for the PDF sheet or "", items), ...]
    item     = (label, panel tag, paragraph, ...)   a leaf that opens the details panel
             | (label, [item, ...])                 a nested group

Outputs, under docs/academics/software-engineering/se311/extra-resources/mindmap/:
    NN-<slug>/<slug>.html   the interactive map
    NN-<slug>/index.html    wrapper, cloned from the Final Mindmap wrapper
    index.html              Mindmaps listing, cloned from the Study Material page
It also adds the Mindmaps folder row to Study Material and the sidebar entries to
scripts/academic-sidebar.json, so run build_academic_sidebar.py afterwards.

    python3 scripts/build_se311_mindmaps.py
"""
from __future__ import annotations

import html
import importlib
import json
import re
from pathlib import Path

from sort_academic_folder_rows import sort_folder_rows

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://shoug-tech.com"
COURSE_URL = "/academics/software-engineering/se311"
STUDY = ROOT / "docs/academics/software-engineering/se311/extra-resources"
STUDY_URL = f"{COURSE_URL}/extra-resources/"
MAPS = STUDY / "mindmap"
MAPS_URL = f"{STUDY_URL}mindmap/"
SIDEBAR = ROOT / "scripts/academic-sidebar.json"

TEMPLATE = ROOT / "docs/academics/other-courses/ethcs303/extra-resources/mindmap/01-moral-systems-ethical-concepts-and-theories/moral-systems-ethical-concepts-and-theories.html"
TEMPLATE_TITLE = "Moral Systems, Ethical Concepts, and Theories"
TEMPLATE_URL = f"{SITE}/academics/other-courses/ethcs303/extra-resources/mindmap/01-moral-systems-ethical-concepts-and-theories/moral-systems-ethical-concepts-and-theories.html"
TEMPLATE_DESC = f"Reset Expand All Collapse All Export Node Title 100% Made by Shoug Alomran · {TEMPLATE_TITLE} Mindmap //."
WRAPPER_TEMPLATE = STUDY / "04-final-mindmap/index.html"

AR_MINDMAPS = "الخرائط الذهنية"
ROW_RE = re.compile(r'[ \t]*<a\b[^>]*class="dir-row"[^>]*>.*?</a\s*>', re.S)
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square"><path d="M5 12h14M12 5l7 7-7 7"/></svg>'
FOLDER_ICON = '<svg class="dir-folder-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square" stroke-linejoin="square" aria-hidden="true"><path d="M3 7a1 1 0 0 1 1-1h5l2 2h9a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V7z"/></svg>'
FOLDER_CSS = """
        .dir-title:has(.dir-folder-icon) { display: flex; align-items: center; gap: 10px; }
        .dir-folder-icon { width: 20px; height: 20px; flex-shrink: 0; color: var(--text-tertiary); transition: color 0.15s ease; }
        .dir-row:hover .dir-folder-icon { color: var(--brand-purple); }
    """
# The template's theme button shows emoji; the site's pages use line icons instead.
MOON = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>'
SUN = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'


def swap(text: str, old: str, new: str, count: int | None = 1) -> str:
    """Replace `old`, failing loudly if the template no longer matches."""
    found = text.count(old)
    if (count is None and not found) or (count is not None and found != count):
        raise SystemExit(f"template drift: expected {count or 'some'} of {old[:80]!r}, found {found}")
    return text.replace(old, new)


def folder(ch) -> str:
    return f"{ch.NUMBER:02d}-{ch.SLUG}"


def label(ch) -> str:
    return f"Chapter {ch.NUMBER}: {ch.TITLE}"


def load_chapters() -> list:
    paths = sorted((ROOT / "scripts/se311_mindmaps").glob("ch*.py"))
    return [importlib.import_module(f"se311_mindmaps.{path.stem}") for path in paths]


def build_node(item: tuple, node_id: str) -> dict:
    name, *rest = item
    if len(rest) == 1 and isinstance(rest[0], list):
        return {"id": node_id, "label": name,
                "children": [build_node(child, f"{node_id}-{i}") for i, child in enumerate(rest[0], 1)]}
    tag, *paragraphs = rest
    # Space between paragraphs: the PDF sheet flattens desc with textContent.
    body = " ".join(f"<p>{p}</p>" for p in paragraphs)
    return {"id": node_id, "label": name, "desc": f'<span class="panel-tag">{html.escape(tag)}</span> {body}'}


def chapter_data(ch) -> dict:
    branches = []
    for b, (name, intro, items) in enumerate(ch.BRANCHES, 1):
        node = {"id": f"b{b}", "label": name}
        if intro:
            node["desc"] = f"<p>{intro}</p>"
        node["children"] = [build_node(item, f"b{b}-{i}") for i, item in enumerate(items, 1)]
        branches.append(node)
    return {"id": "root", "label": ch.TITLE, "children": branches}


def map_page(ch, template: str) -> str:
    title = f"{ch.TITLE} — SE311 Chapter {ch.NUMBER} Mindmap"
    url = f"{SITE}{MAPS_URL}{folder(ch)}/{ch.SLUG}.html"
    data = json.dumps(chapter_data(ch), indent=4, ensure_ascii=False)
    data = "\n".join((" " * 8 + line) if i else line for i, line in enumerate(data.splitlines()))

    t = swap(template, f"&nbsp;·&nbsp; {TEMPLATE_TITLE} Mindmap",
             f"&nbsp;·&nbsp; SE311 Chapter {ch.NUMBER}: {html.escape(ch.TITLE)} Mindmap")
    t = swap(t, TEMPLATE_DESC, html.escape(ch.SUMMARY), count=4)
    t = swap(t, f"{TEMPLATE_TITLE} — Mindmap", html.escape(title), count=4)
    t = swap(t, TEMPLATE_URL, url, count=6)
    t, n = re.subn(r"const DATA = \{.*?\n        \};\n", lambda _m: f"const DATA = {data};\n", t, count=1, flags=re.S)
    if n != 1:
        raise SystemExit("template drift: DATA block not found")
    t = swap(t, '<body data-theme="dark">',
             f'<body data-theme="dark">\n    <h1 class="shoug-visually-hidden">{html.escape(title)}</h1>')
    t = swap(t, '<button class="tb-btn" id="theme-toggle" title="Toggle theme">🌙</button>',
             f'<button class="tb-btn" id="theme-toggle" title="Toggle theme" aria-label="Toggle theme">{MOON}</button>')
    t = swap(t, "const themeBtn = document.getElementById('theme-toggle');",
             f"const THEME_ICONS = {json.dumps({'dark': MOON, 'light': SUN})};\n"
             "        const themeBtn = document.getElementById('theme-toggle');")
    t = swap(t, "themeBtn.textContent = dark ? '🌙' : '☀️';",
             "themeBtn.innerHTML = dark ? THEME_ICONS.dark : THEME_ICONS.light;")
    # Big chapters expand past the 4000px canvas; keep their connectors from clipping.
    return swap(t, "            height: 100%;\n            pointer-events: none;\n        }",
                "            height: 100%;\n            pointer-events: none;\n            overflow: visible;\n        }")


def wrapper_page(ch, prev, nxt, template: str) -> str:
    name = html.escape(label(ch))
    page_url = f"{MAPS_URL}{folder(ch)}/"
    t = swap(template, "SE311 | Final Mindmap", f"SE311 | {name}", count=None)
    t = swap(t, f"{STUDY_URL}04-final-mindmap/", page_url, count=None)
    t = swap(t, f"{STUDY_URL}mindmap/final-mindmap.html", f"{page_url}{ch.SLUG}.html", count=None)
    t = swap(t, f'<a class="breadcrumb-link" href="{STUDY_URL}">Study Material</a> <span class="separator">/</span> <span class="current">Final Mindmap</span>',
             f'<a class="breadcrumb-link" href="{STUDY_URL}">Study Material</a> <span class="separator">/</span> '
             f'<a class="breadcrumb-link" href="{MAPS_URL}">Mindmaps</a> <span class="separator">/</span> <span class="current">{name}</span>')
    t = swap(t, '<div class="ch-label uppercase">ITEM_04 // STUDY MATERIAL</div>',
             f'<div class="ch-label uppercase">ITEM_{ch.NUMBER:02d} // MINDMAPS</div>')
    t = swap(t, '<h1 class="ch-title uppercase">Final Mindmap</h1>', f'<h1 class="ch-title uppercase">{name}</h1>')
    t = swap(t, f'<a class="btn btn-secondary" href="{STUDY_URL}">[ <- BACK TO INDEX ]</a>',
             f'<a class="btn btn-secondary" href="{MAPS_URL}">[ <- BACK TO INDEX ]</a>')
    t = swap(t, 'title="Final Mindmap"', f'title="{name}"', count=2)
    links = ""
    if prev:
        links += f'<a href="{MAPS_URL}{folder(prev)}/" class="nav-link prev"><- PREVIOUS</a>'
    if nxt:
        links += f'<a href="{MAPS_URL}{folder(nxt)}/" class="nav-link next">NEXT -></a>'
    t, n = re.subn(r'<div class="nav-strip uppercase">.*?</div>', lambda _m: f'<div class="nav-strip uppercase">{links}</div>', t, count=1)
    if n != 1:
        raise SystemExit("template drift: nav strip not found")
    return t


def row_html(href: str, title_html: str, ar_title: str) -> str:
    # dir-num is filled in by sort_folder_rows' renumbering.
    return (f'                            <a href="{href}" class="dir-row" data-ar-title="{html.escape(ar_title)}">\n'
            f'                                <div class="dir-num">00</div>\n'
            f'                                <div class="dir-title">{title_html}</div>\n'
            f'                                <div class="dir-status"><span class="status-tag available">AVAILABLE</span></div>\n'
            f'                                <div class="dir-arrow">\n'
            f'                                    {ARROW}\n'
            f'                                </div>\n'
            f'                            </a>')


def numbered(text: str) -> str:
    rows = list(ROW_RE.finditer(text))
    for index, row in reversed(list(enumerate(rows, 1))):
        fixed = re.sub(r'(<div class="dir-num">)\d+(</div>)', rf"\g<1>{index:02d}\g<2>", row.group(0), count=1)
        text = text[:row.start()] + fixed + text[row.end():]
    return text


def listing_page(chapters: list, template: str) -> str:
    t = swap(template, "SHOUG.TECH | SE311 Study Material", "SHOUG.TECH | SE311 Mindmaps", count=None)
    t, n = re.subn(rf'({re.escape(SITE + STUDY_URL)})(?=["?])', r"\g<1>mindmap/", t)
    if n < 3:
        raise SystemExit("template drift: Study Material canonical URLs not found")
    t = swap(t, '/ <span class="current" data-en-text="Study Material" data-ar-text="المواد الدراسية">Study Material</span>',
             f'/ <a class="breadcrumb-link" href="{STUDY_URL}">Study Material</a> / '
             f'<span class="current" data-en-text="Mindmaps" data-ar-text="{AR_MINDMAPS}">Mindmaps</span>')
    t = swap(t, '<div class="type-label" data-en-text="STUDY MATERIAL" data-ar-text="المواد الدراسية">STUDY MATERIAL</div>',
             f'<div class="type-label" data-en-text="MINDMAPS" data-ar-text="{AR_MINDMAPS}">MINDMAPS</div>')
    rows = list(ROW_RE.finditer(t))
    block = "\n".join(row_html(f"{MAPS_URL}{folder(ch)}/", html.escape(label(ch)), f"الفصل {ch.NUMBER}: {ch.AR_TITLE}")
                      for ch in chapters)
    return numbered(t[:rows[0].start()] + block + t[rows[-1].end():])


def study_material_page(text: str) -> str:
    if f'href="{MAPS_URL}" class="dir-row"' not in text:
        first = next(ROW_RE.finditer(text))
        row = row_html(MAPS_URL, f'<span class="dir-title-text">Mindmaps</span>{FOLDER_ICON}', AR_MINDMAPS)
        text = text[:first.start()] + row + "\n" + text[first.start():]
    if ".dir-folder-icon {" not in text:
        text = text.replace("</style>", FOLDER_CSS + "</style>", 1)
    return sort_folder_rows(text)[0]


def find_parent(node, key: str):
    if isinstance(node, dict):
        if key in node:
            return node
        node = list(node.values())
    if isinstance(node, list):
        for child in node:
            found = find_parent(child, key)
            if found is not None:
                return found
    return None


def update_sidebar(chapters: list) -> None:
    raw = SIDEBAR.read_text()
    data = json.loads(raw)
    parent = find_parent(data, STUDY_URL)
    if parent is None:
        raise SystemExit(f"{STUDY_URL} not found in {SIDEBAR.name}")
    items = [item for item in parent[STUDY_URL] if item["url"] != MAPS_URL]
    items.insert(0, {"url": MAPS_URL, "attrs": f'data-en-text="Mindmaps" data-ar-text="{AR_MINDMAPS}"', "label": "Mindmaps"})
    parent[STUDY_URL] = items
    parent[MAPS_URL] = [{"url": f"{MAPS_URL}{folder(ch)}/", "attrs": "", "label": label(ch)} for ch in chapters]
    indent = re.match(r"[{\[]\n( +)", raw)
    out = json.dumps(data, indent=len(indent.group(1)) if indent else 2, ensure_ascii="\\u0" in raw)
    SIDEBAR.write_text(out + ("\n" if raw.endswith("\n") else ""))


def main() -> None:
    chapters = load_chapters()
    template = TEMPLATE.read_text()
    wrapper = WRAPPER_TEMPLATE.read_text()
    study = (STUDY / "index.html").read_text()
    for i, ch in enumerate(chapters):
        out = MAPS / folder(ch)
        out.mkdir(parents=True, exist_ok=True)
        out.joinpath(f"{ch.SLUG}.html").write_text(map_page(ch, template))
        prev = chapters[i - 1] if i else None
        nxt = chapters[i + 1] if i + 1 < len(chapters) else None
        out.joinpath("index.html").write_text(wrapper_page(ch, prev, nxt, wrapper))
    MAPS.joinpath("index.html").write_text(listing_page(chapters, study))
    (STUDY / "index.html").write_text(study_material_page(study))
    update_sidebar(chapters)
    print(f"Built {len(chapters)} SE311 chapter mindmaps; run scripts/build_academic_sidebar.py next")


if __name__ == "__main__":
    main()
