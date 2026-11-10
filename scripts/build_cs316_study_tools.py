#!/usr/bin/env python3
"""Build CS316's slide breakdowns, mind maps, practice quizzes and section listings.

All content lives in scripts/cs316_annotated/content*.py; run build_cs316_course.py and
build_cs316_annotated_slides.py first. Safe to re-run.

    python3 scripts/build_cs316_study_tools.py
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import build_cs316_course as course  # noqa: E402
import build_se371_breakdowns as breakdown  # noqa: E402
import build_se401_study_tools as tools  # noqa: E402
from build_academic_sidebar import DATA_FILE, render_nav  # noqa: E402
from cs316_annotated.common import DECKS  # noqa: E402
from cs316_annotated.decks import CONTENT  # noqa: E402
from se371_breakdown_content import cheat, hook, slidemap, trap  # noqa: E402
import build_cs316_resources as resources  # noqa: E402

SITE = "https://shoug-tech.com"
URL = course.COURSE_URL
OUT = course.COURSE_DIR
TEMPLATE = os.path.join(course.TEMPLATE_DIR, "exams/02-chapter-2-quiz/index.html")
# The mind map engine comes from an existing course page, and its data block is replaced for each deck.
MAP_TEMPLATE = os.path.join(course.DOCS, "academics/software-engineering/se322/extra-resources/mindmaps/"
                            "01-introduction-to-software-design-and-architecture/introduction-to-software-design-and-architecture.html")
FOLDER_ICON = (
    '<svg class="dir-folder-icon" style="width:18px;height:18px;vertical-align:-3px;margin-right:10px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="square" stroke-linejoin="square" aria-hidden="true">'
    '<path d="M3 7a1 1 0 0 1 1-1h5l2 2h9a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V7z"/></svg>'
)
KINDS = {
    "breakdown": ("slide-breakdowns/", "Slide Breakdowns", "", "SLIDE BREAKDOWNS"),
    "mindmap": ("extra-resources/mindmaps/", "Mind Maps", " Mind Map", "MIND MAPS"),
    "quiz": ("exams/", "Exams", " Quiz", "EXAMS"),
}
KEYS = list(DECKS)


def esc(text):
    return html.escape(text, quote=False)


def code_ticks(text):
    return esc(text)


def head_title(key):
    return DECKS[key][3].split(": ", 1)


def item_title(kind, key):
    head, title = head_title(key)
    return "%s%s: %s" % (head, KINDS[kind][2], title)


def folder(kind, key):
    return DECKS[key][0] + ("-quiz" if kind == "quiz" else "")


def file_name(kind, key):
    return DECKS[key][1] + ("-quiz.html" if kind == "quiz" else ".html")


def rebrand_tool(text, i, key):
    head = head_title(key)[0]
    text = re.sub(r"SE401 · CHAPTER %d\b" % i, "CS316 · " + head.upper(), text)
    text = re.sub(r"SE401 · Chapter %d\b" % i, "CS316 · " + head, text)
    text = re.sub(r"SE401 Chapter %d\b" % i, "CS316 " + head, text)
    return text.replace("software-engineering/se401", "computer-science/cs316").replace("SE401", "CS316").replace("se401", "cs316")


def self_url(kind, key):
    return "%s%s%s%s/%s" % (SITE, URL, KINDS[kind][0], folder(kind, key), file_name(kind, key))


def set_identity(text, kind, key):
    """Point a generated page's canonical and social tags at its real address."""
    url = self_url(kind, key)
    title = "CS316 %s | %s" % (item_title(kind, key), "Shoug's Digital Garden")
    desc = "CS316 %s, written from the Introduction to AI and Data Science lecture slides." % item_title(kind, key)
    text = re.sub(r"<link rel=\"canonical\"[^>]*>\s*", "", text)
    text = re.sub(r"<link rel=\"alternate\" hreflang=[^>]*>\s*", "", text)
    text = re.sub(r"<meta (?:property=\"og:[^\"]*\"|name=\"twitter:[^\"]*\"|name=\"description\")\s+content=\"[^\"]*\"\s*/?>\s*", "", text)
    text = re.sub(r"<script\s+type=\"application/ld\+json\">.*?</script>\s*", "", text, flags=re.S)
    text = re.sub(r"<title>.*?</title>", lambda _m: "<title>%s</title>" % esc(title), text, count=1, flags=re.S)
    ld = json.dumps({"@context": "https://schema.org", "@type": "WebPage", "url": url, "name": title,
                     "description": desc}, ensure_ascii=False)
    tags = (
        '<link rel="canonical" href="{u}"><meta name="description" content="{d}">'
        '<meta property="og:title" content="{t}"><meta property="og:description" content="{d}">'
        '<meta property="og:url" content="{u}"><meta property="og:type" content="article">'
        '<meta property="og:image" content="{s}/assets/og-banner.png">'
        '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{t}">'
        '<meta name="twitter:description" content="{d}"><meta name="twitter:image" content="{s}/assets/og-banner.png">'
        '<script type="application/ld+json">{l}</script>'
    ).format(u=url, d=html.escape(desc, quote=True), t=html.escape(title, quote=True), s=SITE, l=ld)
    return text.replace("</head>", tags + "</head>", 1)


def map_node(node_id, label, tag, desc, children=None):
    node = {"id": node_id, "label": label, "desc": '<span class="panel-tag">%s</span><p>%s</p>' % (tag, desc)}
    if children is not None:
        node["children"] = children
    return node


def map_tree(key):
    """The node tree the shared mind map page draws, one branch per topic."""
    head, title = head_title(key)
    branches = []
    for b, (name, summary, facts, examples) in enumerate(CONTENT[key]["map"], 1):
        children = []
        for f, fact in enumerate(facts, 1):
            words = fact.rstrip(".").split()
            label = " ".join(words[:7]) + ("…" if len(words) > 7 else "")
            children.append(map_node("b%d-f%d" % (b, f), label, "Key Detail", esc(fact)))
        if examples:
            children.append(map_node("b%d-ex" % b, "Examples", "Examples", "Worked illustrations of <strong>%s</strong>." % esc(name), [
                map_node("b%d-ex%d" % (b, e), label, "Example", esc(text)) for e, (label, text) in enumerate(examples, 1)
            ]))
        branches.append(map_node("b%d" % b, name, "Core Concept", esc(summary), children))
    root = '<strong>%s</strong>. Expand branches, select a node for detail, search topics, zoom, pan, or export the map.' % esc(title)
    return {"id": "root", "label": title, "desc": '<span class="panel-tag">CS316 · %s</span><p>%s</p>' % (head, root), "children": branches}


def mindmap_page(i, key):
    title = head_title(key)[1]
    text = course.read(MAP_TEMPLATE)
    data_block = re.compile(r"const DATA = \{.*?\n\s*\};(?=\n\n\s*// ─+\n\s*// STATE)", re.S)
    if not data_block.search(text):
        raise SystemExit("mind map template no longer matches")
    text = data_block.sub(lambda _m: "const DATA = " + json.dumps(map_tree(key), ensure_ascii=False, indent=2).replace("</", "<\\/") + ";", text, count=1)
    text = re.sub(r"Moral\s+Systems,\s+Ethical\s+Concepts,\s+and\s+Theories", title, text)
    text = re.sub(r"Introduction\s+to\s+Software\s+Design\s+and\s+Architecture", title, text)
    return set_identity(text.replace("SE322", "CS316"), "mindmap", key)


def quiz_page(i, key):
    title = head_title(key)[1]
    data = CONTENT[key]
    tools.QUIZ_BANK = {i: {
        "mcq": [(m["q"], m["correct"], m["wrong"], m["why"]) for m in data["mcq"]],
        "short": [(s["q"], s["keywords"], s["answer"]) for s in data["short"]],
    }}
    text = rebrand_tool(tools.exam_html(i, title, data["map"]), i, key)
    return set_identity(text, "quiz", key)


def breakdown_sections(data):
    sections = [
        {"id": "orient", "nav": "Start Here", "label": "Orientation", "title": "What this chapter covers",
         "html": "<p>%s</p>" % esc(data["lede"])},
        {"id": "map", "nav": "Slide Map", "label": "Navigation", "title": "Where to spend your time",
         "html": slidemap([(a, b, w, c) for a, b, w, c in data["slide_map"]])},
    ]
    for n, (name, summary, facts, examples) in enumerate(data["map"], 1):
        body = "<p>%s</p><ul>%s</ul>" % (esc(summary), "".join("<li>%s</li>" % esc(f) for f in facts))
        body += "".join(hook("<strong>%s.</strong> %s" % (esc(t), esc(x))) for t, x in examples)
        sections.append({"id": "topic-%d" % n, "nav": esc(name), "label": "Topic %d" % n,
                         "title": esc(name), "html": body})
    sections.append({"id": "traps", "nav": "Traps", "label": "Marks Lost Here", "title": "Common mistakes",
                     "html": "".join(trap(esc(t), esc(w), esc(f)) for t, w, f in data["traps"])})
    sections.append({"id": "cheat", "nav": "Cheat Sheet", "label": "One Screen", "title": "Quick reference",
                     "html": cheat([(esc(t), [esc(x) for x in items]) for t, items in data["cheat"]])})
    return sections


def breakdown_page(i, key):
    head, title = head_title(key)
    data = CONTENT[key]
    quiz = []
    for m in data["mcq"][:6]:
        opts, a = _options(m)
        quiz.append({"tag": head, "q": esc(m["q"]), "opts": [esc(o) for o in opts], "a": a, "why": esc(m["why"])})
    breakdown.BASE = URL + "slide-breakdowns/"
    chapter = {
        "num": i, "slug": DECKS[key][0], "file": file_name("breakdown", key), "title": title,
        "desc": "Slide breakdown of CS316 %s: %s" % (head, data["lede"]), "sub": esc(data["lede"]),
        "stats": ["%d slides" % data["count"], head, "%d topics" % len(data["map"])],
        "sections": breakdown_sections(data), "quiz": quiz,
    }
    text = breakdown.render_content(chapter)
    text = text.replace("SE371 // CH%02d" % i, "CS316 // %s" % head.upper())
    text = text.replace("Chapter %02d &middot; Slide Breakdown" % i, "%s &middot; Slide Breakdown" % head)
    text = re.sub(r"SE371 Web Engineering &mdash; Chapter \{?%d\}?" % i, "CS316 Introduction to AI and Data Science &mdash; %s" % head, text)
    text = text.replace("SE371 Web Engineering", "CS316 Introduction to AI and Data Science")
    return text.replace("software-engineering/se371", "computer-science/cs316").replace("SE371", "CS316").replace("se371", "cs316")


def _options(item):
    from cs316_annotated.decks import options
    return options(item)


def frame_page(url, path, section, upper, i, title, raw, prev_url, next_url, data):
    """A site page wrapping one generated HTML file in an iframe."""
    t = course.rebrand(course.read(TEMPLATE))
    old = "/academics/computer-science/cs316/exams/02-chapter-2-quiz/"
    t = t.replace(old, url).replace("Chapter 2 Quiz", esc(title))
    t = course.replace_block(r'<a\s+class="breadcrumb-link"\s+href="/academics/computer-science/cs316/exams/"\s*>Exams</a\s*>',
                             '<a class="breadcrumb-link" href="%s%s">%s</a>' % (URL, path, section), t)
    t = t.replace("ITEM_02 // EXAMS", "ITEM_%02d // %s" % (i, upper))
    t = course.replace_block(r'class="btn btn-primary"\s+href="[^"]*"', 'class="btn btn-primary" href="./%s"' % raw, t)
    t = course.replace_block(r'class="btn btn-secondary"\s+href="[^"]*"', 'class="btn btn-secondary" href="%s%s"' % (URL, path), t)
    link = lambda u, cls, word: ('<a href="%s" class="nav-link %s">%s</a>' % (u, cls, word) if u
                                 else '<span class="nav-link %s disabled">%s</span>' % (cls, word))
    t = course.replace_block(r'<div class="nav-strip[^"]*">.*?</div>',
                             '<div class="nav-strip uppercase">%s%s</div>' % (link(prev_url, "prev", "&lt;- PREVIOUS"), link(next_url, "next", "NEXT -&gt;")), t)
    t = course.replace_block(r'<iframe.*?</iframe\s*>',
                             '<iframe class="embed-frame legacy-html-frame" src="./%s" loading="lazy" title="%s"></iframe>' % (raw, html.escape(title, quote=True)), t)
    return course.stamp_sidebar(t, data, url)


def wrapper(kind, i, key, data):
    path, section, _suffix, upper = KINDS[kind]
    href = lambda k: "%s%s%s/" % (URL, path, folder(kind, k)) if k else None
    prev_key = KEYS[i - 2] if i > 1 else None
    next_key = KEYS[i] if i < len(KEYS) else None
    url = href(key)
    page = frame_page(url, path, section, upper, i, item_title(kind, key), file_name(kind, key), href(prev_key), href(next_key), data)
    course.write(os.path.join(OUT, path, folder(kind, key), "index.html"), page)


def rows(kind):
    path = KINDS[kind][0]
    return "".join(
        '<a href="%s%s%s/" class="dir-row"><div class="dir-num">%02d</div><div class="dir-title">%s</div>'
        '<div class="dir-status"><span class="status-tag available">AVAILABLE</span></div>'
        '<div class="dir-arrow">%s</div></a>' % (URL, path, folder(kind, k), i, esc(item_title(kind, k)), course.ARROW)
        for i, k in enumerate(KEYS, 1)
    )


def update_sidebar():
    with open(DATA_FILE, encoding="utf-8") as f:
        data = json.load(f)
    for kind in KINDS:
        path = KINDS[kind][0]
        data["children"][URL + path] = [
            {"url": "%s%s%s/" % (URL, path, folder(kind, k)), "attrs": "", "label": item_title(kind, k)} for k in KEYS
        ]
    data["children"][URL + "extra-resources/"] = [
        {"url": URL + "extra-resources/mindmaps/", "attrs": "", "label": "Mind Maps"},
        {"url": URL + "extra-resources/notes/", "attrs": "", "label": "Notes"},
        {"url": URL + "extra-resources/notebooks/", "attrs": "", "label": "Notebooks"},
    ]
    resources.add_sidebar(data)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return data


def restamp(data):
    count = 0
    for dirpath, _dirs, files in os.walk(OUT):
        if "index.html" not in files:
            continue
        path = os.path.join(dirpath, "index.html")
        rel = "/" + os.path.relpath(dirpath, os.path.join(course.DOCS)) + "/"
        text = course.read(path)
        new = course.stamp_sidebar(text, data, rel)
        if new != text:
            course.write(path, new)
            count += 1
    return count


def main():
    data = update_sidebar()
    builders = {"breakdown": breakdown_page, "mindmap": mindmap_page, "quiz": quiz_page}
    for kind, make in builders.items():
        for i, key in enumerate(KEYS, 1):
            folder_path = os.path.join(OUT, KINDS[kind][0], folder(kind, key))
            course.write(os.path.join(folder_path, file_name(kind, key)), make(i, key))
            wrapper(kind, i, key, data)
    course.section_page(data, "slide-breakdowns/", "Slide Breakdowns", "تفكيك الشرائح", rows("breakdown"))
    extras = resources.build(data, frame_page)
    quiz_rows = rows("quiz") + extras["exam_rows"]
    course.section_page(data, "exams/", "Exams", "الاختبارات", quiz_rows)
    course.section_page(data, "extra-resources/mindmaps/", "Mind Maps", "الخرائط الذهنية", rows("mindmap"))
    course.section_page(data, "extra-resources/notes/", "Notes", "ملاحظات", extras["note_rows"])
    course.section_page(data, "extra-resources/notebooks/", "Notebooks", "دفاتر الأكواد", extras["notebook_rows"])
    folder_rows = "".join(
        '<a href="%sextra-resources/%s/" class="dir-row"><div class="dir-num">%02d</div>'
        '<div class="dir-title">%s %s</div><div class="dir-status">'
        '<span class="status-tag available">%d FILES</span></div><div class="dir-arrow">%s</div></a>'
        % (URL, slug, n, FOLDER_ICON, label, count, course.ARROW)
        for n, (slug, label, count) in enumerate(
            [("mindmaps", "Mind Maps", len(KEYS)), ("notes", "Notes", extras["note_count"]), ("notebooks", "Notebooks", extras["notebook_count"])], 1)
    )
    course.section_page(data, "extra-resources/", "Study Material", "المواد الدراسية", folder_rows)
    print("restamped", restamp(data), "CS316 pages")


if __name__ == "__main__":
    main()
