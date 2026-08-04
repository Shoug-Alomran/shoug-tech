#!/usr/bin/env python3
"""Build slide-grounded Ethics-style mindmaps and exams for CYS405/CYS406."""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_se401_study_tools as core

ROOT = Path(__file__).resolve().parents[1]
CYBER = ROOT / "docs/academics/cybersecurity"
WRAPPER_TEMPLATE = CYBER / "cys401/exams/01-chapter-1-quiz/index.html"


def clean(fragment: str) -> str:
    fragment = re.sub(r"<script.*?</script>|<style.*?</style>", " ", fragment, flags=re.S | re.I)
    fragment = re.sub(r"<[^>]+>", " ", fragment)
    return " ".join(html.unescape(fragment).split())


def first(pattern: str, text: str) -> str:
    match = re.search(pattern, text, re.S | re.I)
    return clean(match.group(1)) if match else ""


def slide_model(code: str):
    root = CYBER / code / "slide-breakdowns"
    chapters = []
    for page in sorted(root.glob("*/*.html")):
        if page.name == "index.html":
            continue
        folder = page.parent.name
        match = re.match(r"(\d+)-chapter-\d+-(.+)", folder)
        if not match:
            continue
        number = int(match.group(1))
        source = page.read_text(errors="ignore")
        title = first(r"<h1[^>]*>(.*?)</h1>", source) or match.group(2).replace("-", " ").title()
        branches = []
        for section in re.findall(r"<section\b[^>]*>(.*?)</section>", source, re.S | re.I):
            name = first(r"<h2[^>]*>(.*?)</h2>", section)
            if not name or name.lower() in {"exam tips & tricks", "quick reference — everything at a glance", "quick reference - everything at a glance"}:
                continue
            desc = first(r"<h2[^>]*>.*?</h2>\s*<p[^>]*>(.*?)</p>", section)
            if not desc:
                desc = f"Core concepts, distinctions, and defensive implications of {name}."
            facts = []
            # Preserve named subtopics and pair them with their first explanation.
            for h, tail in re.findall(r"<h[34][^>]*>(.*?)</h[34]>(.*?)(?=<h[34]\b|$)", section, re.S | re.I):
                label = clean(h)
                detail = first(r"<p[^>]*>(.*?)</p>", tail)
                if label and not label.lower().startswith(("mnemonic", "exam tip", "quick reference")):
                    fact = f"{label}: {detail}" if detail and detail.lower() != label.lower() else label
                    if fact not in facts:
                        facts.append(fact)
            for term, detail in re.findall(r'class="def-term[^\"]*"[^>]*>(.*?)</div>\s*<div class="def-desc"[^>]*>(.*?)</div>', section, re.S | re.I):
                fact = f"{clean(term)}: {clean(detail)}"
                if clean(term) and fact not in facts:
                    facts.append(fact)
            for item in re.findall(r"<li[^>]*>(.*?)</li>", section, re.S | re.I):
                fact = clean(item)
                if 20 <= len(fact) <= 220 and fact not in facts:
                    facts.append(fact)
            facts = facts[:8]
            if not facts:
                facts = [clean(p) for p in re.findall(r"<p[^>]*>(.*?)</p>", section, re.S | re.I)
                         if 20 <= len(clean(p)) <= 220][:5]
            branches.append((name, desc, facts))
        if not branches:
            raise RuntimeError(f"No study sections extracted from {page}")
        chapters.append((number, folder, title, branches, page))
    return sorted(chapters)


def replace_sidebar_items(text: str, code: str, chapters, kind: str) -> str:
    items = []
    for number, folder, title, _branches, _source in chapters:
        slug = folder.split(f"{number:02d}-chapter-{number}-", 1)[-1]
        target_folder = f"{number:02d}-{slug}{'-quiz' if kind == 'exam' else ''}"
        label = f"Chapter {number} {'Quiz' if kind == 'exam' else 'Mindmap'}"
        href = f"/academics/cybersecurity/{code}/{'exams' if kind == 'exam' else 'extra-resources/mindmaps'}/{target_folder}/"
        items.append(f'<li class="tree-item tree-viewer"><a class="tree-file" href="{href}">{label}</a></li>')
    return re.sub(r'<ul class="tree-children item-children is-open">.*?</ul>', '<ul class="tree-children item-children is-open">'+''.join(items)+'</ul>', text, count=1, flags=re.S)


def wrapper(code: str, number: int, title: str, slug: str, chapters, kind: str) -> str:
    text = WRAPPER_TEMPLATE.read_text().replace("CYS401", code.upper()).replace("cys401", code)
    text = text.replace("Chapter 1 Quiz", f"Chapter {number} {'Quiz' if kind == 'exam' else 'Mindmap'}")
    text = text.replace("ITEM_01", f"ITEM_{number:02d}")
    content_name = f"{slug}{'-quiz' if kind == 'exam' else ''}.html"
    text = re.sub(r'src="\./chapter-1-quiz\.html"', f'src="./{content_name}"', text)
    text = re.sub(r'href="\./chapter-1-quiz\.html"', f'href="./{content_name}"', text)
    text = re.sub(r'/exams/01-chapter-1-quiz/', f'/extra-resources/mindmaps/{number:02d}-{slug}/' if kind == 'mindmap' else f'/exams/{number:02d}-{slug}-quiz/', text)
    if kind == "mindmap":
        text = text.replace("// EXAMS", "// MINDMAPS").replace(">EXAMS<", ">MINDMAPS<").replace("/exams/", "/extra-resources/mindmaps/")
    text = replace_sidebar_items(text, code, chapters, kind)
    route = "exams" if kind == "exam" else "extra-resources/mindmaps"
    def chapter_href(index: int) -> str:
        n, folder, _title, _branches, _source = chapters[index]
        s = folder.split(f"{n:02d}-chapter-{n}-", 1)[-1]
        return f'/academics/cybersecurity/{code}/{route}/{n:02d}-{s}{"-quiz" if kind == "exam" else ""}/'
    previous = f'/academics/cybersecurity/{code}/{route}/' if number == 1 else chapter_href(number - 2)
    next_link = f'/academics/cybersecurity/{code}/{route}/' if number == len(chapters) else chapter_href(number)
    text = re.sub(r'<div class="nav-strip uppercase">.*?</div>', f'<div class="nav-strip uppercase"><a href="{previous}" class="nav-link prev">&lt;- PREVIOUS</a><a href="{next_link}" class="nav-link next">NEXT -&gt;</a></div>', text, count=1, flags=re.S)
    text = re.sub(r'<title>.*?</title>', f'<title>{code.upper()} | Chapter {number} {"Quiz" if kind == "exam" else "Mindmap"}</title>', text, count=1)
    text = re.sub(r'<h1 class="ch-title">.*?</h1>', f'<h1 class="ch-title">Chapter {number} {"Quiz" if kind == "exam" else "Mindmap"}</h1>', text, count=1, flags=re.S)
    return text


def rows(code: str, chapters, kind: str) -> str:
    out = ['<div class="directory-container"><div class="dir-header"><span>SEQ</span><span>DESCRIPTOR</span><span>SYS_STATE</span><span></span></div>']
    for number, folder, title, _branches, _source in chapters:
        slug = folder.split(f"{number:02d}-chapter-{number}-", 1)[-1]
        target = f"{number:02d}-{slug}{'-quiz' if kind == 'exam' else ''}"
        label = f"Chapter {number}: {title} {'Quiz' if kind == 'exam' else 'Mindmap'}"
        out.append(f'<a class="dir-row" href="/academics/cybersecurity/{code}/{"exams" if kind == "exam" else "extra-resources/mindmaps"}/{target}/"><div class="dir-num">{number}</div><div class="dir-title">{html.escape(label)}</div><div class="dir-status"><span class="status-tag available">AVAILABLE</span></div><div class="dir-arrow">-&gt;</div></a>')
    out.append('</div>')
    return ''.join(out)


def replace_main_listing(text: str, listing: str) -> str:
    """Replace the hub listing without assuming the footer sits outside ``main``."""
    starts = [
        text.find('<div class="coming-soon-container"'),
        text.find('<div class="directory-container"'),
    ]
    starts = [position for position in starts if position >= 0]
    if not starts:
        raise ValueError("Could not find the hub listing container")

    start = min(starts)
    end = text.find('<footer class="shoug-site-footer">', start)
    if end < 0:
        end = text.find('</main>', start)
    if end < 0:
        raise ValueError("Could not find the end of the hub listing")

    return text[:start] + listing + "\n    " + text[end:]


def build_course(code: str):
    base = CYBER / code
    chapters = slide_model(code)
    maps = base / "extra-resources/mindmaps"
    exams = base / "exams"
    maps.mkdir(parents=True, exist_ok=True)
    for number, folder, title, branches, _source in chapters:
        slug = folder.split(f"{number:02d}-chapter-{number}-", 1)[-1]
        map_dir = maps / f"{number:02d}-{slug}"
        exam_dir = exams / f"{number:02d}-{slug}-quiz"
        map_dir.mkdir(parents=True, exist_ok=True); exam_dir.mkdir(parents=True, exist_ok=True)
        map_content = core.mindmap_html(number, title, branches).replace("SE401", code.upper()).replace("se401", code).replace("software-engineering", "cybersecurity")
        exam_content = core.exam_html(number, title, branches).replace("SE401", code.upper()).replace("se401", code).replace("software-engineering", "cybersecurity")
        (map_dir / f"{slug}.html").write_text(map_content)
        (exam_dir / f"{slug}-quiz.html").write_text(exam_content)
        (map_dir / "index.html").write_text(wrapper(code, number, title, slug, chapters, "mindmap"))
        (exam_dir / "index.html").write_text(wrapper(code, number, title, slug, chapters, "exam"))

    exam_hub = replace_main_listing((base / "exams/index.html").read_text(), rows(code, chapters, "exam"))
    (base / "exams/index.html").write_text(exam_hub)
    map_hub = exam_hub.replace(f"{code.upper()} Quizzes", f"{code.upper()} Mindmaps").replace("// EXAMS", "// MINDMAPS").replace(">EXAMS<", ">MINDMAPS<")
    map_hub = replace_main_listing(map_hub, rows(code, chapters, "mindmap"))
    maps.joinpath("index.html").write_text(map_hub)

    extra = base / "extra-resources/index.html"
    icon = '<svg class="dir-folder-icon" style="width:1.15em;height:1.15em;margin-right:.55em;vertical-align:-.18em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 7a1 1 0 0 1 1-1h5l2 2h9a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V7z"/></svg>'
    one = f'<div class="directory-container"><div class="dir-header"><span>SEQ</span><span>DESCRIPTOR</span><span>SYS_STATE</span><span></span></div><a class="dir-row" href="/academics/cybersecurity/{code}/extra-resources/mindmaps/"><div class="dir-num">1</div><div class="dir-title">{icon}<span>Mindmaps</span></div><div class="dir-status"><span class="status-tag available">AVAILABLE</span></div><div class="dir-arrow">-&gt;</div></a></div>'
    extra.write_text(replace_main_listing(extra.read_text(), one))
    from fix_mindmap_sidebar_state import apply_course
    apply_course(code, base)
    from fix_academic_sidebar_links import fix_page
    for page in [maps / "index.html", exams / "index.html", *maps.glob("*/index.html"), *exams.glob("*/index.html")]:
        fix_page(page)
    print(code.upper(), len(chapters), "chapters")


if __name__ == "__main__":
    build_course("cys405")
    build_course("cys406")
