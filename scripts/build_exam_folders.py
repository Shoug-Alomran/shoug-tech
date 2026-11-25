#!/usr/bin/env python3
"""Sort every course's exams into folders: chapter quizzes, Midterm 1, Midterm 2, Final.

Each course's exams/index.html (a preview grid from build_slide_hub.py) becomes
one folder card per non-empty group, and each group gets its own page at
exams/<group>/index.html with that group's exam previews. Exam pages keep their
URLs, so progress, ratings, bookmarks and search results still work, and the
existing preview strips are reused, so nothing is re-rendered.

Sorting is by the exam's title and folder name (see classify()); put a course's
exceptions in OVERRIDES, keyed by the exam's folder slug.

    python3 scripts/build_exam_folders.py --dry-run     # print where each exam goes
    python3 scripts/build_exam_folders.py               # write every course
    python3 scripts/build_exam_folders.py cys401 se423  # only these courses

It also rewrites the EXAMS entries in scripts/academic-sidebar.json (folders,
then the exams inside each); stamp the pages afterwards with
build_academic_sidebar.py.

Safe to re-run: once a course is sorted, its exams are read back from the group
pages. Works on preview grids and on the older dir-row listings. ETHCS303 (the
paid course, sealed at deploy) is skipped.
"""
from __future__ import annotations

import glob
import html
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, "docs")
SIDEBAR = os.path.join(REPO, "scripts", "academic-sidebar.json")
MARK = "data-exam-folders"

GROUPS = [
    ("chapter-quizzes", "Chapter Quizzes", "اختبارات الفصول",
     "One quiz per chapter or lecture, for practising as you go."),
    ("midterm-1", "Midterm 1", "الاختبار الفصلي الأول",
     "Everything for the first midterm: past papers, practice exams and the quizzes before it."),
    ("midterm-2", "Midterm 2", "الاختبار الفصلي الثاني",
     "Everything for the second midterm: past papers, practice exams and the quizzes before it."),
    ("final", "Final Exams", "الاختبارات النهائية",
     "Past finals, final practice exams and final question banks."),
]
GROUP_IDS = [g[0] for g in GROUPS]

# slug of the exam folder -> group, for exams the name alone can't place.
OVERRIDES: dict[str, str] = {
    # ISC113 calls its two midterms "Exam 1" and "Exam 2".
    "01-exam-1": "midterm-1",
    "02-exam-2": "midterm-2",
    # SE401's photographed past paper doesn't say which exam it was; it was a final.
    "15-past-exam-mcq-and-fill-in": "final",
}

# Attributes in any order: tiles may carry a style="--strip-..." before href.
TILE_RE = re.compile(r'<a\b(?=[^>]*\bclass="deck-preview")([^>]*)>(.*?)</a\s*>', re.S)
# Older listings: one <a class="dir-row"> per exam, attributes in any order.
ROW_RE = re.compile(r'<a\b(?=[^>]*\bclass="dir-row\b)[^>]*>.*?</a\s*>', re.S)
FOLDER_ICON = ('<svg class="dir-folder-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
               'stroke-width="2" aria-hidden="true"><path d="M3 7h6l2 2h10v10H3z"/></svg>')


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def classify(slug: str, title: str) -> str:
    """Place an exam by what its title says, nothing more.

    Midterm folders take titles that name that midterm (Midterm 1/2, Major 1/2,
    Major Exam I/II, first/second midterm); Final takes titles with "final".
    An unnumbered Midterm/Major is settled per course in sort_course(): it joins
    Midterm 1 unless the course also has a second midterm. Everything else,
    including graded quizzes and chapter practice exams, is a chapter quiz.
    """
    if slug in OVERRIDES:
        return OVERRIDES[slug]
    words = re.sub(r"[^a-z0-9]+", " ", (slug + " " + title).lower())
    if re.search(r"\bfinal\b", words):
        return "final"
    exam = r"\b(midterm|major|mid)\s*(exam\s*)?"
    if re.search(exam + r"(2|ii|two)\b|\bsecond (midterm|major)\b", words):
        return "midterm-2"
    if re.search(exam + r"(1|i|one)\b|\bfirst (midterm|major)\b", words):
        return "midterm-1"
    if re.search(r"\b(midterm|major)\b", words) and not re.search(r"\bquiz\b", words):
        return "midterm"  # unnumbered; resolved per course
    return "chapter-quizzes"


def text_of(fragment):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


SECTION_RE = re.compile(r'<section\s+class="slide-gallery"([^>]*)>(.*?)</section\s*>', re.S)


def with_strip(tile_html, section_attrs):
    """Copy the section's --strip-* preview variables onto the tile, so its thumbnail
    still points at the right strip once tiles from several sections share a grid."""
    if "--strip-light" in tile_html[: tile_html.find(">")]:
        return tile_html
    style = re.search(r'style="([^"]*)"', section_attrs)
    strips = "".join(re.findall(r"--strip-(?:dark|light):\s*url\([^)]*\);?", html.unescape(style.group(1)))) if style else ""
    if not strips:
        return tile_html
    strips = html.escape(re.sub(r"\s+", " ", strips), quote=True)
    return re.sub(r"^<a\b", '<a style="%s"' % strips, tile_html, count=1)


def tiles_from(page_text):
    """(href, markup, title) for every exam on a listing, grid or row style."""
    items = []
    sections = list(SECTION_RE.finditer(page_text))
    for sec in sections or [None]:
        body = sec.group(2) if sec else page_text
        for m in TILE_RE.finditer(body):
            if "data-exam-group" in m.group(1):
                continue  # one of our group folders; real resource folders stay
            href = re.search(r'href="([^"]+)"', m.group(1))
            if not href:
                continue
            markup = with_strip(m.group(0), sec.group(1)) if sec else m.group(0)
            items.append((href.group(1), markup, text_of(m.group(2))))
    if items or sections:
        return items
    for m in ROW_RE.finditer(page_text):
        if "directory-folder" in m.group(0)[: m.group(0).find(">")] or "data-exam-group" in m.group(0):
            continue  # one of our folder rows, not an exam
        href = re.search(r'href="([^"]+)"', m.group(0)[: m.group(0).find(">")])
        title = re.search(r'class="dir-title"[^>]*>(.*?)</div', m.group(0), re.S)
        if href and title:
            items.append((href.group(1), m.group(0), text_of(title.group(1))))
    return items


def layout(page_text):
    if "data-preview-grid" in page_text and grid_bounds(page_text):
        return "grid"
    return "rows" if ROW_RE.search(page_text) else None


def list_bounds(text, kind):
    """Span to replace: the gallery grid, or the run of dir-row anchors."""
    if kind == "grid":
        sections = list(SECTION_RE.finditer(text))
        if sections:
            return sections[0].start(), sections[-1].end()
        return grid_bounds(text)
    rows = list(ROW_RE.finditer(text))
    return rows[0].start(), rows[-1].end()


def row_markup(items):
    """Renumber row-style exams so each folder page counts from 01."""
    out = []
    for n, item in enumerate(items, 1):
        out.append(re.sub(r'(<div class="dir-num">)\s*\d+\s*(</div>)', r"\g<1>%02d\2" % n, item[1], count=1))
    return "\n".join(out)


def grid_bounds(text):
    """Start/end of the <div class="slide-gallery-grid"> holding the tiles."""
    start = text.find('<div class="slide-gallery-grid">')
    if start < 0:
        return None
    depth, i = 0, start
    for m in re.finditer(r"<(/?)div\b", text[start:]):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return start, start + m.end() + text[start + m.end():].find(">") + 1
    return None


def course_exams(index_path, exams_url):
    """Every exam tile of a course, whether or not it has been sorted before."""
    text = read(index_path)
    if MARK not in text:
        return tiles_from(text)
    # Already sorted: exams live on the group pages (and, after an older run, possibly
    # still in sections of the index). Merge them, one entry per exam.
    tiles, seen = [], set()
    pages = [text] + [read(p) for p in (os.path.join(os.path.dirname(index_path), gid, "index.html") for gid in GROUP_IDS)
                      if os.path.isfile(p)]
    for page in pages:
        for tile in tiles_from(page):
            if tile[0] not in seen and not re.search(r"/exams/(%s)/$" % "|".join(GROUP_IDS), tile[0]):
                seen.add(tile[0])
                tiles.append(tile)
    number = lambda t: int(re.match(r"(\d+)", t[0].rstrip("/").split("/")[-1]).group(1)) if re.match(r"\d+", t[0].rstrip("/").split("/")[-1]) else 10**6
    tiles = sorted(tiles, key=number)
    # Courses whose exam folders aren't numbered in chapter order list that order here.
    course = os.path.basename(os.path.dirname(os.path.dirname(index_path)))
    order = EXAM_ORDER.get(course)
    if order:
        rank = {slug: i for i, slug in enumerate(order)}
        tiles = sorted(tiles, key=lambda t: rank.get(t[0].rstrip("/").split("/")[-1], len(order)))
    return tiles


# Exam folders by course, in the order students should see them (first chapter to last).
# Folders not listed keep their numbered order after the listed ones.
EXAM_ORDER = {
    "se423": [
        "04-introduction-quiz", "13-organizational-context-quiz", "12-team-quiz", "02-development-approach-quiz",
        "07-risk-management-quiz", "03-estimation-quiz", "08-scheduling-and-tracking-quiz", "06-quality-quiz",
        "10-stakeholders-quiz", "01-change-management-quiz", "09-software-engineering-quiz",
    ],
}


# Tiles that carry their own strip need --strip resolved on the tile, since the
# page resolves it on .slide-gallery from the section's variables.
TILE_STRIP_STYLE = (
    '<style id="exam-folder-style">'
    ".slide-gallery .deck-preview[style*='--strip-dark']{--strip:var(--strip-dark)}"
    "body.shoug-light-mode .slide-gallery .deck-preview[style*='--strip-light']{--strip:var(--strip-light)}"
    "</style>"
)


def with_tile_strip_style(page):
    if 'id="exam-folder-style"' in page:
        return page
    return re.sub(r"</head\s*>", TILE_STRIP_STYLE + "\n</head>", page, count=1)


def gallery(tiles_html, intro=""):
    head = f'<p class="slide-hub-intro exam-folder-intro">{html.escape(intro)}</p>' if intro else ""
    return f'{head}<section class="slide-gallery"><div class="slide-gallery-grid">{tiles_html}</div></section>'


def folder_row(gid, label, label_ar, count, n, exams_url):
    noun = "exam" if count == 1 else "exams"
    return (
        f'<a class="dir-row directory-folder" href="{exams_url}{gid}/" data-exam-group="{gid}">'
        f'<div class="dir-num">{n:02d}</div><div class="dir-title">{FOLDER_ICON}'
        f'<span class="dir-title-text" data-en-text="{label}" data-ar-text="{label_ar}">{label}</span>'
        f' <span class="exam-folder-count">· {count} {noun}</span></div>'
        f'<div class="dir-status"><span class="status-tag available">AVAILABLE</span></div>'
        f'<div class="dir-arrow">-&gt;</div></a>'
    )


def folder_tile(gid, label, label_ar, count, thumb_style, exams_url, strip=""):
    noun = "exam" if count == 1 else "exams"
    # strip: the first exam's --strip-* variables, so the folder shows its preview (not a blank tile).
    style = f' style="{strip}"' if strip else ""
    return (
        f'<a href="{exams_url}{gid}/"{style} class="deck-preview" data-kind="folder" data-exam-group="{gid}">'
        f'<span class="deck-thumb"{thumb_style}></span>'
        f'<span class="deck-kind" data-en-text="Folder" data-ar-text="مجلد">Folder</span>'
        f'<div class="deck-name"><span class="dir-folder-icon" aria-hidden="true"></span><span data-en-text="{label}" data-ar-text="{label_ar}">{label}</span>'
        f' <span class="exam-folder-count">· {count} {noun}</span></div></a>'
    )


def thumb_style(tile_html):
    m = re.search(r'<span\s+class="deck-thumb"([^>]*)>', tile_html)
    return m.group(1) if m else ""


def strip_vars(tile_html):
    """The --strip-* preview variables on a tile's opening <a>, if any."""
    m = re.match(r'<a\b[^>]*?\bstyle="([^"]*--strip-[^"]*)"', tile_html)
    return m.group(1) if m else ""


def group_page(index_text, kind, exams_url, gid, label, label_ar, about, tiles):
    start, end = list_bounds(index_text, kind)
    if kind == "grid":
        body = gallery("".join(t[1] for t in tiles), about)
    else:
        body = row_markup(tiles)
    page = index_text[:start] + body + index_text[end:]
    page = page.replace(" " + MARK, "").replace(MARK, "")
    page = with_tile_strip_style(page)
    # Intro line and breadcrumb: Exams becomes a link, the group is the current page.
    page = re.sub(
        r'<span class="current" data-en-text="Exams" data-ar-text="الاختبارات"\s*>Exams</span\s*>',
        f'<a class="breadcrumb-link" href="{exams_url}" data-en-text="Exams" data-ar-text="الاختبارات">Exams</a> / '
        f'<span class="current" data-en-text="{label}" data-ar-text="{label_ar}">{label}</span>',
        page, count=1)
    # Canonical, og:url and language alternates name the folder page, not the Exams page.
    page = re.sub(r'(https://shoug-tech\.com)' + re.escape(exams_url) + r'(?=(?:\?lang=\w+)?")',
                  lambda m: m.group(1) + exams_url + gid + "/", page)
    page = re.sub(r"(<title>[^<]*?)(</title>)", lambda m: m.group(1).rstrip() + " · " + label + m.group(2), page, count=1)
    return page


def update_sidebar(data, exams_url, groups):
    """EXAMS lists the folders; each folder lists its exams (labels kept where known)."""
    children = data.setdefault("children", {})
    known = {}
    for key in [exams_url] + [exams_url + gid + "/" for gid in GROUP_IDS]:
        for entry in children.get(key, []):
            known[entry["url"]] = entry
    folders = []
    for gid, label, _ar, _about in GROUPS:
        url = exams_url + gid + "/"
        if not groups[gid]:
            children.pop(url, None)
            continue
        folders.append({"url": url, "attrs": "", "label": label})
        children[url] = [
            known.get(tile[0], {"url": tile[0], "attrs": "", "label": tile[2]}) for tile in groups[gid]
        ]
    children[exams_url] = folders


def sort_course(index_path, dry):
    rel = os.path.relpath(os.path.dirname(index_path), DOCS).replace(os.sep, "/")
    exams_url = "/" + rel + "/"
    text = read(index_path)
    kind = layout(text)
    if not kind:
        return rel, None
    tiles = course_exams(index_path, exams_url)
    if not tiles:
        return rel, None
    groups = {gid: [] for gid in GROUP_IDS}
    unnumbered = []
    for tile in tiles:
        slug = tile[0].rstrip("/").split("/")[-1]
        gid = classify(slug, tile[2])
        (unnumbered if gid == "midterm" else groups[gid]).append(tile)
    # A plain "Midterm"/"Major" is the course's only midterm unless a second one exists.
    groups["midterm-1" if not groups["midterm-2"] else "chapter-quizzes"].extend(unnumbered)
    if dry:
        return rel, groups
    folders = []
    for gid, label, label_ar, about in GROUPS:
        sub_path = os.path.join(os.path.dirname(index_path), gid, "index.html")
        if not groups[gid]:
            if os.path.isfile(sub_path):
                os.remove(sub_path)
                os.rmdir(os.path.dirname(sub_path))
            continue
        write(sub_path, group_page(text, kind, exams_url, gid, label, label_ar, about, groups[gid]))
        if kind == "grid":
            folders.append(folder_tile(gid, label, label_ar, len(groups[gid]), thumb_style(groups[gid][0][1]), exams_url, strip_vars(groups[gid][0][1])))
        else:
            folders.append(folder_row(gid, label, label_ar, len(groups[gid]), len(folders) + 1, exams_url))
    start, end = list_bounds(text, kind)
    if kind == "grid":
        text = with_tile_strip_style(text[:start] + gallery("".join(folders)) + text[end:])
        if MARK not in text:
            text = text.replace("data-preview-grid", "data-preview-grid " + MARK, 1)
    else:
        text = text[:start] + "\n".join(folders) + text[end:]
        if MARK not in text:
            text = re.sub(r"<body\b", "<body " + MARK, text, count=1)
    write(index_path, text)
    return rel, groups


def main():
    dry = "--dry-run" in sys.argv
    only = {a.lower() for a in sys.argv[1:] if not a.startswith("--")}
    skipped = []
    with open(SIDEBAR, encoding="utf-8") as fh:
        sidebar = json.load(fh)
    for index_path in sorted(glob.glob(os.path.join(DOCS, "academics", "**", "exams", "index.html"), recursive=True)):
        course = os.path.basename(os.path.dirname(os.path.dirname(index_path)))
        if course == "ethcs303" or (only and course not in only):
            continue
        rel, groups = sort_course(index_path, dry)
        if groups is None:
            skipped.append(rel)
            continue
        if not dry:
            update_sidebar(sidebar, "/" + rel + "/", groups)
        counts = ", ".join(f"{gid} {len(v)}" for gid, v in groups.items() if v)
        print(f"{rel}: {counts}")
        if dry:
            for gid in GROUP_IDS:
                for tile in groups[gid]:
                    print(f"    {gid:16} {tile[2][:70]}")
    if not dry:
        with open(SIDEBAR, "w", encoding="utf-8") as fh:
            json.dump(sidebar, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        print("sidebar data updated; stamp it with: python3 scripts/build_academic_sidebar.py")
    if skipped:
        print("skipped (no exams found): " + ", ".join(skipped))


if __name__ == "__main__":
    main()
