#!/usr/bin/env python3
"""Wrap SE423 interactive exams in the standard SHOUG.TECH content viewer."""

from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUIZZES = ROOT / "docs/academics/software-engineering/se423/quizzes"
MINDMAP_TEMPLATE = (
    ROOT
    / "docs/academics/software-engineering/se423/extra-resources/mindmaps/01-change-management/index.html"
)
HUB = QUIZZES / "index.html"


EXAMS = [
    ("01-change-management-quiz", "Chapter 1: Change Management Quiz"),
    ("02-development-approach-quiz", "Chapter 2: Development Approach Quiz"),
    ("03-estimation-quiz", "Chapter 3: Estimation Quiz"),
    ("04-introduction-quiz", "Chapter 4: Introduction Quiz"),
    ("05-project-performance-domains-quiz", "Chapter 5: Project Performance Domains Quiz"),
    ("06-quality-quiz", "Chapter 6: Quality Quiz"),
    ("07-risk-management-quiz", "Chapter 7: Risk Management Quiz"),
    ("08-scheduling-and-tracking-quiz", "Chapter 8: Scheduling and Tracking Quiz"),
    ("09-software-engineering-quiz", "Chapter 9: Software Engineering Quiz"),
    ("10-stakeholders-quiz", "Chapter 10: Stakeholders Quiz"),
    ("11-tailoring-models-methods-and-artifacts-quiz", "Chapter 11: Tailoring Models, Methods & Artifacts Quiz"),
    ("12-team-quiz", "Chapter 12: Team Quiz"),
]


def replace_one(text: str, pattern: str, replacement: str) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"Expected one match for {pattern!r}, found {count}")
    return updated


def sidebar_for_exam(hub_html: str, route: str) -> str:
    match = re.search(r'<nav class="sidebar academic-sidebar".*?</nav>', hub_html, flags=re.S)
    if not match:
        raise RuntimeError("Could not find the SE423 exams sidebar")
    sidebar = match.group(0)
    item_pattern = (
        rf'<li class="tree-item tree-viewer"><a class="tree-file" '
        rf'href="{re.escape(route)}">'
    )
    replacement = (
        '<li class="tree-item tree-viewer file-active"><a class="tree-file" '
        f'href="{route}"><span class="status-dot"></span>'
    )
    sidebar, count = re.subn(item_pattern, replacement, sidebar, count=1)
    if count != 1:
        raise RuntimeError(f"Could not activate sidebar item {route}")
    return sidebar


def make_exam_responsive(text: str) -> str:
    """Let the interactive exam use the available viewport without losing readable gutters."""
    text = text.replace(
        "            --maxw: 860px;",
        "            --maxw: 1440px;\n            --page-pad: clamp(14px, 3vw, 48px);",
        1,
    )
    text = text.replace("padding: 12px 20px;", "padding: 12px var(--page-pad);", 1)
    text = text.replace("padding: 0 20px;", "padding: 0 var(--page-pad);", 2)
    text = text.replace("padding: 20px 20px 0;", "padding: 20px var(--page-pad) 0;", 1)
    text = re.sub(r"\bChapter 0([1-9])\b", r"Chapter \1", text)
    text = re.sub(r"\bCHAPTER 0([1-9])\b", r"CHAPTER \1", text)
    if "SE423 exam visual enhancement" not in text:
        enhanced_css = """

        /* SE423 exam visual enhancement */
        :root {
            --violet: #b829ea;
            --violet-soft: rgba(184, 41, 234, .14);
            --cyan: #31d7f5;
            --cyan-soft: rgba(49, 215, 245, .12);
        }

        body {
            background-image:
                radial-gradient(circle at 12% 8%, var(--violet-soft), transparent 32rem),
                radial-gradient(circle at 88% 24%, var(--cyan-soft), transparent 30rem),
                linear-gradient(180deg, rgba(184, 41, 234, .035), transparent 45%);
            background-attachment: fixed;
        }

        .topbar {
            box-shadow: 0 10px 34px rgba(4, 3, 14, .24);
        }

        .topbar::after {
            content: '';
            position: absolute;
            inset: auto 0 -1px;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--violet), var(--cyan), transparent);
            opacity: .7;
        }

        .exam-header {
            animation: exam-rise .65s cubic-bezier(.2, .8, .2, 1) both;
        }

        .exam-header h1 {
            background: linear-gradient(100deg, var(--ink) 18%, var(--violet) 62%, var(--cyan));
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
        }

        .coverage-strip {
            background: linear-gradient(115deg, var(--violet-soft), var(--cyan-soft));
            border-color: color-mix(in srgb, var(--violet) 42%, var(--rule));
        }

        .question-block {
            overflow: hidden;
            border-color: color-mix(in srgb, var(--violet) 28%, var(--rule));
            background-image: linear-gradient(135deg, var(--violet-soft), transparent 34%, var(--cyan-soft));
            animation: exam-rise .58s cubic-bezier(.2, .8, .2, 1) both;
            transition: transform .25s ease, border-color .25s ease, box-shadow .25s ease;
        }

        .question-block:nth-of-type(2) { animation-delay: .09s; }
        .question-block:nth-of-type(3) { animation-delay: .18s; }

        .question-block::before {
            content: '';
            position: absolute;
            inset: 0 auto 0 0;
            width: 3px;
            background: linear-gradient(180deg, var(--violet), var(--cyan), var(--gold));
        }

        .question-block:hover {
            transform: translateY(-3px);
            border-color: color-mix(in srgb, var(--violet) 58%, var(--rule));
            box-shadow: 0 18px 44px rgba(14, 8, 35, .22), 0 0 28px var(--violet-soft);
        }

        .option {
            position: relative;
            background: color-mix(in srgb, var(--paper-raised) 92%, transparent);
            transition: transform .18s ease, background .18s ease, border-color .18s ease, box-shadow .18s ease;
        }

        .option:hover {
            transform: translateX(5px);
            background: linear-gradient(90deg, var(--violet-soft), var(--cyan-soft));
            border-color: var(--violet);
            box-shadow: 0 7px 20px rgba(184, 41, 234, .12);
        }

        textarea:focus {
            border-color: var(--cyan);
            box-shadow: 0 0 0 3px var(--cyan-soft), 0 10px 30px rgba(49, 215, 245, .08);
        }

        .submit-btn {
            background: linear-gradient(105deg, var(--violet), #7b5cff 52%, var(--cyan)) !important;
            color: #fff !important;
            box-shadow: 0 12px 34px rgba(184, 41, 234, .3);
        }

        .submit-btn:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 17px 42px rgba(184, 41, 234, .4), 0 0 24px var(--cyan-soft);
        }

        .score-panel.show {
            background-image: linear-gradient(125deg, var(--violet-soft), transparent 46%, var(--cyan-soft));
            border-color: var(--violet);
        }

        @keyframes exam-rise {
            from { opacity: 0; transform: translateY(18px) scale(.992); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }

        @media (prefers-reduced-motion: reduce) {
            .exam-header, .question-block { animation: none !important; }
            .question-block:hover, .option:hover, .submit-btn:hover { transform: none !important; }
        }
"""
        text = text.replace("</style>", enhanced_css + "    </style>", 1)
    return text


def enhance_exam_hub(text: str) -> str:
    text = re.sub(r"\bChapter 0([1-9])\b", r"Chapter \1", text)
    text = re.sub(r'<div class="dir-num">0([1-9])</div>', r'<div class="dir-num">\1</div>', text)
    if "SE423 exam directory enhancement" not in text:
        css = """
    <style>
        /* SE423 exam directory enhancement */
        .directory-container {
            position: relative;
            overflow: hidden;
            background:
                radial-gradient(circle at 8% 5%, rgba(184, 41, 234, .13), transparent 34rem),
                radial-gradient(circle at 92% 65%, rgba(49, 215, 245, .09), transparent 32rem);
        }

        .dir-row {
            position: relative;
            isolation: isolate;
            animation: exam-row-rise .48s cubic-bezier(.2, .8, .2, 1) both;
            transition: transform .22s ease, background .22s ease, border-color .22s ease, box-shadow .22s ease;
        }

        .dir-row:nth-of-type(2) { animation-delay: .04s; }
        .dir-row:nth-of-type(3) { animation-delay: .08s; }
        .dir-row:nth-of-type(4) { animation-delay: .12s; }
        .dir-row:nth-of-type(5) { animation-delay: .16s; }
        .dir-row:nth-of-type(6) { animation-delay: .20s; }
        .dir-row:nth-of-type(7) { animation-delay: .24s; }
        .dir-row:nth-of-type(8) { animation-delay: .28s; }
        .dir-row:nth-of-type(9) { animation-delay: .32s; }
        .dir-row:nth-of-type(10) { animation-delay: .36s; }
        .dir-row:nth-of-type(11) { animation-delay: .40s; }
        .dir-row:nth-of-type(12) { animation-delay: .44s; }
        .dir-row:nth-of-type(13) { animation-delay: .48s; }

        .dir-row::before {
            content: '';
            position: absolute;
            inset: 0;
            z-index: -1;
            opacity: 0;
            background: linear-gradient(100deg, rgba(184, 41, 234, .2), rgba(123, 92, 255, .09) 55%, rgba(49, 215, 245, .15));
            transition: opacity .22s ease;
        }

        .dir-row:hover {
            transform: translateX(8px) scale(.995);
            border-color: rgba(184, 41, 234, .55);
            box-shadow: -4px 0 0 #b829ea, 0 12px 34px rgba(14, 5, 32, .28);
        }

        .dir-row:hover::before { opacity: 1; }
        .dir-row:hover .dir-title { color: #e985ff; text-shadow: 0 0 18px rgba(184, 41, 234, .35); }
        .dir-row:hover .dir-num { color: #31d7f5; }

        @keyframes exam-row-rise {
            from { opacity: 0; transform: translateY(12px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @media (prefers-reduced-motion: reduce) {
            .dir-row { animation: none !important; }
            .dir-row:hover { transform: none !important; }
        }
    </style>
"""
        text = text.replace("</head>", css + "</head>", 1)
    return text


def make_viewer_responsive(text: str) -> str:
    responsive_css = """
        /* Responsive exam viewport: phone -> tablet -> laptop/desktop. */
        .embed-area-wrapper {
            width: 100%;
            padding-inline: clamp(10px, 2.2vw, 40px);
        }

        .embed-container,
        .embed-container iframe {
            width: 100%;
            min-width: 0;
            height: clamp(560px, 82dvh, 1400px);
            min-height: 0;
        }

        @media (max-width: 768px) {
            .embed-area-wrapper {
                padding: 8px 8px 16px;
            }

            .embed-container,
            .embed-container iframe {
                height: calc(100dvh - 96px);
                min-height: 560px;
            }
        }

        @media (max-width: 480px) {
            .embed-area-wrapper {
                padding-inline: 0;
            }

            .embed-container {
                border-inline: 0;
            }
        }
"""
    text = text.replace("</style>", responsive_css + "    </style>", 1)
    return "\n".join(line.rstrip() for line in text.splitlines()) + "\n"


def build_wrapper(template: str, hub_html: str, index: int, slug: str, title: str, raw_name: str) -> str:
    safe_title = html.escape(title)
    route = f"/academics/software-engineering/se423/exams/{slug}/"
    previous_route = "/academics/software-engineering/se423/exams/"
    next_route = "/academics/software-engineering/se423/exams/"
    if index > 0:
        previous_route = f"/academics/software-engineering/se423/exams/{EXAMS[index - 1][0]}/"
    if index + 1 < len(EXAMS):
        next_route = f"/academics/software-engineering/se423/exams/{EXAMS[index + 1][0]}/"

    text = template
    text = replace_one(text, r"<title>.*?</title>", f"<title>SE423 | {safe_title}</title>")
    text = replace_one(
        text,
        r'<nav class="sidebar academic-sidebar".*?</nav>',
        sidebar_for_exam(hub_html, route),
    )
    breadcrumb = (
        '<div class="breadcrumb"><a class="breadcrumb-link" href="/academics/">Academics</a> '
        '/ <a class="breadcrumb-link" href="/academics/software-engineering/">Software Engineering</a> '
        '/ <a class="breadcrumb-link" href="/academics/software-engineering/se423/">SE423</a> '
        '/ <a class="breadcrumb-link" href="/academics/software-engineering/se423/exams/" '
        'data-en-text="Exams" data-ar-text="الاختبارات">Exams</a> '
        f'/ <span class="current">{safe_title}</span></div>'
    )
    text = replace_one(text, r'<div class="breadcrumb">.*?</div>', breadcrumb)
    text = replace_one(
        text,
        r'<div class="ch-label(?: uppercase)?">.*?</div>',
        f'<div class="ch-label">ITEM_{index + 1:02d} // EXAMS</div>',
    )
    text = replace_one(text, r'<h1 class="ch-title(?: uppercase)?">.*?</h1>', f'<h1 class="ch-title">{safe_title}</h1>')
    actions = (
        f'<div class="action-buttons"><a class="btn btn-primary" href="./{raw_name}" target="_blank" '
        'rel="noopener noreferrer">[ OPEN IN NEW TAB -&gt; ]</a>'
        '<a class="btn btn-secondary" href="/academics/software-engineering/se423/exams/">'
        '[ &lt;- BACK TO INDEX ]</a></div>'
    )
    text = replace_one(text, r'<div class="action-buttons">.*?</div>', actions)
    nav = (
        f'<div class="nav-strip"><a href="{previous_route}" class="nav-link prev">&lt;- PREVIOUS</a>'
        f'<a href="{next_route}" class="nav-link next">NEXT -&gt;</a></div>'
    )
    text = replace_one(text, r'<div class="nav-strip">.*?</div>', nav)
    embed = (
        '<div class="embed-area-wrapper"><div class="embed-container">'
        f'<iframe class="embed-frame legacy-html-frame" src="./{raw_name}" title="{safe_title}" loading="lazy"></iframe>'
        '</div></div>'
    )
    text = replace_one(text, r'<div class="embed-area-wrapper">.*?</div>\s*</div>', embed)
    return make_viewer_responsive(text)


def main() -> None:
    template = MINDMAP_TEMPLATE.read_text()
    hub_html = enhance_exam_hub(HUB.read_text())
    HUB.write_text(hub_html)

    for index, (slug, title) in enumerate(EXAMS):
        folder = QUIZZES / slug
        wrapper = folder / "index.html"
        raw_name = f"{slug}.html"
        raw = folder / raw_name

        if not raw.exists():
            current = wrapper.read_text()
            if '<iframe class="embed-frame' in current:
                raise RuntimeError(f"{wrapper} is already a wrapper but {raw} is missing")
            wrapper.replace(raw)

        raw.write_text(make_exam_responsive(raw.read_text()))
        wrapper.write_text(build_wrapper(template, hub_html, index, slug, title, raw_name))

    print(f"Wrapped {len(EXAMS)} SE423 exams")


if __name__ == "__main__":
    main()
