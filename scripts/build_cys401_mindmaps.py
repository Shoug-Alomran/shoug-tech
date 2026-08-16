#!/usr/bin/env python3
"""Build Ethics-style interactive mindmaps for CYS401.

The chapter models below are written directly from the CYS401 slide breakdowns in
docs/academics/cybersecurity/cys401/slide-breakdowns/, because that course's
breakdown pages use too many different markup shapes to scrape reliably (the way
build_cys405_cys406_study_tools.py does for CYS405/CYS406).

Output per chapter:
    extra-resources/mindmaps/NN-slug/slug.html   the interactive map (ETHCS303 engine)
    extra-resources/mindmaps/NN-slug/index.html  the site viewer wrapper

Run scripts/build_academic_sidebar.py afterwards to stamp the new sidebar entries.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cys401_mindmap_content import CHAPTERS

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/academics/cybersecurity/cys401"
MAPS = BASE / "extra-resources/mindmaps"
WRAPPER_TEMPLATE = BASE / "exams/01-chapter-1-quiz/index.html"
# The interactive map engine every course's mindmaps are rendered from.
TEMPLATE = (ROOT / "docs/academics/other-courses/ethcs303/extra-resources/mindmap"
            / "01-moral-systems-ethical-concepts-and-theories"
            / "moral-systems-ethical-concepts-and-theories.html")
SITE = "https://shoug-tech.com"
ROUTE = "/academics/cybersecurity/cys401/extra-resources/mindmaps"
# Site metadata uses the legacy capitalised /Academics/ path for canonical URLs.
CANON = "/Academics/cybersecurity/cys401/extra-resources/mindmaps"
ARABIC = "الخرائط الذهنية"


def metadata(text: str, path: str, name: str, description: str) -> str:
    """Point every SEO tag on a page at its own URL instead of the template's."""
    canonical = SITE + path
    text = re.sub(r'(<link rel="canonical" href=")[^"]*(">)', rf'\1{canonical}\2', text, count=1)
    text = re.sub(r'(<meta property="og:url" content=")[^"]*(">)', rf'\1{canonical}\2', text, count=1)
    text = re.sub(r'(<link rel="alternate" hreflang="en" href=")[^"]*(">)', rf'\1{canonical}\2', text, count=1)
    text = re.sub(r'(<link rel="alternate" hreflang="ar" href=")[^"]*(">)',
                  rf'\1{SITE}/ar{path}\2', text, count=1)
    text = re.sub(r'(<link rel="alternate" hreflang="x-default" href=")[^"]*(">)', rf'\1{canonical}\2', text, count=1)
    escaped_name = html.escape(name, quote=True)
    escaped_description = html.escape(description, quote=True)
    for pattern, value in (
        (r'(<meta name="description" content=")[^"]*(">)', escaped_description),
        (r'(<meta property="og:title" content=")[^"]*(">)', escaped_name),
        (r'(<meta property="og:description" content=")[^"]*(">)', escaped_description),
        (r'(<meta name="twitter:title" content=")[^"]*(">)', escaped_name),
        (r'(<meta name="twitter:description" content=")[^"]*(">)', escaped_description),
    ):
        text = re.sub(pattern, lambda m, v=value: m.group(1) + v + m.group(2), text, count=1)
    schema = json.dumps({"@context": "https://schema.org", "@type": "WebPage", "url": canonical,
                         "name": name, "description": description,
                         "isPartOf": {"@type": "WebSite", "name": "Shoug's Digital Garden", "url": SITE + "/"}})
    return re.sub(r'<script type="application/ld\+json">.*?</script>',
                  lambda _m: '<script type="application/ld+json">' + schema + '</script>',
                  text, count=1, flags=re.S)


def tree(number: int, title: str, branches: list) -> dict:
    """Build the map's node tree.

    core.mindmap_html() derives each leaf label by truncating the detail text to
    seven words plus an ellipsis, which produced labels like "Accuracy: the
    information is free from errors…". Here every node carries its own short
    concept label and the panel gets the full explanation, so nothing is elided.
    """
    root = {
        "id": "root",
        "label": title,
        "desc": f'<span class="panel-tag">CYS401 · Chapter {number}</span>'
                f'<p>A comprehensive concept map for <strong>{html.escape(title)}</strong>.</p>'
                "<p>Expand a branch to see its concepts, then select any node for the full "
                "explanation and a worked example. You can search topics, zoom, pan, and export the map.</p>",
        "children": [],
    }
    for branch_index, (name, summary, details) in enumerate(branches, 1):
        branch = {
            "id": f"branch-{branch_index}",
            "label": name,
            "desc": f'<span class="panel-tag">Core Concept</span><p>{summary}</p>',
            "children": [],
        }
        for detail_index, (label, tag, body, example) in enumerate(details, 1):
            desc = f'<span class="panel-tag">{html.escape(tag)}</span><p>{body}</p>'
            if example:
                desc += f"<p><strong>In everyday terms:</strong> {example}</p>"
            branch["children"].append({
                "id": f"branch-{branch_index}-detail-{detail_index}",
                "label": label,
                "desc": desc,
            })
        root["children"].append(branch)
    return root


def mindmap(number: int, slug: str, title: str, branches: list) -> str:
    """Render the ETHCS303 map engine with CYS401 content and metadata."""
    text = TEMPLATE.read_text()
    text = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)} — CYS401 Mindmap</title>",
                  text, count=1, flags=re.S)
    text = text.replace("Moral Systems, Ethical Concepts, and Theories Mindmap", f"{html.escape(title)} Mindmap")
    payload = json.dumps(tree(number, title, branches), ensure_ascii=False, indent=4)
    text, replaced = re.subn(r"const DATA = \{.*?\n\};\n\n        // ─+\n        // STATE",
                             lambda _m: "const DATA = " + payload
                             + ";\n\n        // ─────────────────────────────────────────────\n        // STATE",
                             text, count=1, flags=re.S)
    if replaced != 1:
        raise RuntimeError("Could not replace the DATA block in the mindmap template")
    return metadata(text, f"{CANON}/{number:02d}-{slug}/{slug}.html", f"{title} — CYS401 Mindmap",
                    f"Interactive CYS401 Chapter {number} {title} mindmap with expandable concepts, "
                    "worked examples, search, zoom, pan, and PNG export.")


def sidebar_items(active_folder: str | None, mindmaps_active: bool = True) -> str:
    """The STUDY MATERIAL item list, with Mindmaps (and its chapters) expanded."""
    items = [f'<li class="tree-item tree-viewer"><a class="tree-file" href="/academics/cybersecurity/cys401/extra-resources/summary/" data-en-text="Summary" data-ar-text="الملخص">Summary</a></li>',
             f'<li class="tree-item tree-viewer{" file-active" if mindmaps_active else ""}"><a class="tree-file" href="'
             f'{ROUTE}/">{"<span class=\"status-dot\"></span>" if mindmaps_active else ""}MINDMAPS</a></li>']
    chapters = ['<ul class="tree-children item-children is-open">']
    for number, slug, _title, _branches in CHAPTERS:
        folder = f"{number:02d}-{slug}"
        active = folder == active_folder
        cls = "tree-item tree-viewer file-active" if active else "tree-item tree-viewer"
        dot = '<span class="status-dot"></span>' if active else ""
        chapters.append(f'<li class="{cls}"><a class="tree-file" href="{ROUTE}/{folder}/">{dot}Chapter {number} Mindmap</a></li>')
    chapters.append("</ul>")
    items.append("".join(chapters))
    return "".join(items)


def apply_sidebar(text: str, active_folder: str | None, mindmaps_active: bool = True) -> str:
    """Point the sidebar at Study Material > Mindmaps instead of Exams."""
    # Drop the Exams item list that the quiz template carries.
    text = re.sub(r'(<li class="tree-item tree-section(?: file-active)?"><a class="tree-file" '
                  r'href="/academics/cybersecurity/cys401/exams/"[^>]*>)(?:<span class="status-dot"></span>)?(EXAMS</a></li>)'
                  r'(?:<ul class="tree-children item-children is-open">.*?</ul>)?',
                  r'\1\2', text, count=1, flags=re.S)
    replacement = ('<li class="tree-item tree-section file-active"><a class="tree-file" '
                   'href="/academics/cybersecurity/cys401/extra-resources/" data-en-text="STUDY MATERIAL" '
                   'data-ar-text="المواد الدراسية">'
                   '<span class="status-dot"></span>STUDY MATERIAL</a></li>'
                   '<ul class="tree-children item-children is-open">'
                   + sidebar_items(active_folder, mindmaps_active) + '</ul>')
    text, count = re.subn(r'<li class="tree-item tree-section(?: file-active)?"><a class="tree-file" '
                          r'href="/academics/cybersecurity/cys401/extra-resources/"[^>]*>.*?STUDY MATERIAL</a></li>'
                          r'(?:<ul class="tree-children item-children is-open">.*?</ul>)?',
                          replacement, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError("Could not locate the Study Material sidebar entry")
    return text


def wrapper(number: int, slug: str, title: str) -> str:
    """The site viewer page that frames one mindmap."""
    folder = f"{number:02d}-{slug}"
    label = f"Chapter {number} Mindmap"
    text = WRAPPER_TEMPLATE.read_text()
    text = re.sub(r"<title>.*?</title>", f"<title>CYS401 | {label}</title>", text, count=1, flags=re.S)
    text = text.replace(
        '<a class="breadcrumb-link" href="/academics/cybersecurity/cys401/exams/">Exams</a> '
        '<span class="separator">/</span> <span class="current">Chapter 1 Quiz</span>',
        f'<a class="breadcrumb-link" href="{ROUTE}/">Mindmaps</a> '
        f'<span class="separator">/</span> <span class="current">{html.escape(title)}</span>')
    text = text.replace('<div class="ch-label uppercase">ITEM_01 // EXAMS</div>',
                        f'<div class="ch-label uppercase">ITEM_{number:02d} // MINDMAPS</div>')
    text = re.sub(r'<h1 class="ch-title uppercase">.*?</h1>',
                  f'<h1 class="ch-title uppercase">{html.escape(title)}</h1>', text, count=1, flags=re.S)
    text = text.replace('href="./chapter-1-quiz.html"', f'href="./{slug}.html"')
    text = text.replace('src="./chapter-1-quiz.html"', f'src="./{slug}.html"')
    text = text.replace('title="Chapter 1 Quiz"', f'title="{html.escape(title, quote=True)}"')
    text = text.replace('href="/academics/cybersecurity/cys401/exams/">[ <- BACK TO INDEX ]',
                        f'href="{ROUTE}/">[ <- BACK TO INDEX ]')
    previous = f"{ROUTE}/" if number == 1 else f"{ROUTE}/{CHAPTERS[number - 2][0]:02d}-{CHAPTERS[number - 2][1]}/"
    following = f"{ROUTE}/" if number == len(CHAPTERS) else f"{ROUTE}/{CHAPTERS[number][0]:02d}-{CHAPTERS[number][1]}/"
    text = re.sub(r'<div class="nav-strip uppercase">.*?</div>',
                  f'<div class="nav-strip uppercase"><a href="{previous}" class="nav-link prev">&lt;- PREVIOUS</a>'
                  f'<a href="{following}" class="nav-link next">NEXT -&gt;</a></div>',
                  text, count=1, flags=re.S)
    text = metadata(text, f"{CANON}/{folder}/", f"CYS401 | {label}",
                    f"Interactive CYS401 Chapter {number} mindmap: {title}. "
                    "Expand branches, search concepts, and open every key detail.")
    return apply_sidebar(text, folder)


def hub() -> str:
    """The Mindmaps index page listing every chapter."""
    text = (BASE / "extra-resources/index.html").read_text()
    text = re.sub(r"<title>.*?</title>", "<title>SHOUG.TECH | CYS401 Mindmaps</title>", text, count=1, flags=re.S)
    text = text.replace(
        '<span class="current" data-en-text="Study Material" data-ar-text="المواد الدراسية">Study Material</span>',
        '<a class="breadcrumb-link" href="/academics/cybersecurity/cys401/extra-resources/">Study Material</a> / '
        f'<span class="current" data-en-text="Mindmaps" data-ar-text="{ARABIC}">Mindmaps</span>')
    text = text.replace(
        '<div class="type-label" data-en-text="STUDY MATERIAL" data-ar-text="المواد الدراسية">STUDY MATERIAL</div>',
        f'<div class="type-label" data-en-text="MINDMAPS" data-ar-text="{ARABIC}">MINDMAPS</div>')
    rows = ['<div class="directory-container"><div class="dir-header"><span>SEQ</span><span>DESCRIPTOR</span>'
            '<span>SYS_STATE</span><span></span></div>']
    for number, slug, title, _branches in CHAPTERS:
        rows.append(f'<a class="dir-row" href="{ROUTE}/{number:02d}-{slug}/"><div class="dir-num">{number}</div>'
                    f'<div class="dir-title">Chapter {number}: {html.escape(title)} Mindmap</div>'
                    '<div class="dir-status"><span class="status-tag available">AVAILABLE</span></div>'
                    '<div class="dir-arrow">-&gt;</div></a>')
    rows.append("</div>")
    text = replace_listing(text, "".join(rows))
    text = metadata(text, CANON + "/", "CYS401 Mindmaps",
                    "Interactive CYS401 chapter mindmaps covering every chapter of Fundamentals of Cyber Security.")
    return apply_sidebar(text, None)


def replace_listing(text: str, listing: str) -> str:
    """Swap a hub page's directory/coming-soon block for a new listing."""
    starts = [position for position in (text.find('<div class="coming-soon-container"'),
                                        text.find('<div class="directory-container"')) if position >= 0]
    if not starts:
        raise ValueError("Could not find the hub listing container")
    start = min(starts)
    end = text.find('<footer class="shoug-site-footer">', start)
    if end < 0:
        end = text.find("</main>", start)
    if end < 0:
        raise ValueError("Could not find the end of the hub listing")
    return text[:start] + listing + "\n    " + text[end:]


def extra_resources() -> None:
    """Add a Mindmaps row to the Study Material hub, keeping the existing rows."""
    page = BASE / "extra-resources/index.html"
    text = page.read_text()
    # Drop any row this script wrote previously so re-runs stay idempotent.
    text = re.sub(rf'<a class="dir-row" href="{re.escape(ROUTE)}/".*?</a>', "", text, flags=re.S)
    arrow = ('<div class="dir-arrow" aria-hidden="true">'
             '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square">'
             '<path d="M7 17 17 7"></path><path d="M7 7h10v10"></path></svg></div>')
    position = len(re.findall(r'<a class="dir-row"', text)) + 1
    row = (f'<a class="dir-row" href="{ROUTE}/" data-ar-title="الخرائط الذهنية">'
           f'<div class="dir-num">{position:02d}</div>'
           '<div class="dir-title">CYS401 Mindmaps</div>'
           '<div class="dir-status"><span class="status-tag available">AVAILABLE</span></div>'
           f'{arrow}</a>')
    text, replaced = re.subn(r'(</div>\s*)(?=(?:<footer class="shoug-site-footer">|</main>))', row + r'\1', text, count=1)
    if replaced != 1:
        raise RuntimeError("Could not append the Mindmaps row to the Study Material hub")
    page.write_text(apply_sidebar(text, None, mindmaps_active=False))


def main() -> None:
    MAPS.mkdir(parents=True, exist_ok=True)
    for number, slug, title, branches in CHAPTERS:
        folder = MAPS / f"{number:02d}-{slug}"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / f"{slug}.html").write_text(mindmap(number, slug, title, branches))
        (folder / "index.html").write_text(wrapper(number, slug, title))
    (MAPS / "index.html").write_text(hub())
    extra_resources()
    print("CYS401", len(CHAPTERS), "mindmaps", sum(len(c[3]) for c in CHAPTERS), "branches",
          sum(len(f) for c in CHAPTERS for _n, _d, f in c[3]), "details")


if __name__ == "__main__":
    main()
