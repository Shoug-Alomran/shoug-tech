#!/usr/bin/env python3
"""Repair ENG101 layout and build the shared English learning hub."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OTHER = DOCS / "Academics" / "other-courses"
HUB = OTHER / "english" / "index.html"
ENG101 = OTHER / "eng101" / "index.html"
OTHER_INDEX = OTHER / "index.html"


ENGL101_STYLE = """
 n    <style id="eng101-layout-fix">
    .page-container {
        width: min(1480px, 100%) !important;
        margin: 0 auto !important;
        padding: 48px clamp(28px, 4vw, 64px) 72px !important;
        display: grid !important;
        grid-template-columns: minmax(0, 1fr) minmax(300px, 360px) !important;
        gap: clamp(36px, 5vw, 72px) !important;
        align-items: start !important;
    }
    .primary-content { min-width: 0 !important; }
    .course-header { padding: 0 0 32px !important; }
    .course-code-wrapper { justify-content: space-between !important; gap: 20px !important; }
    .course-code {
        font-size: clamp(4rem, 7vw, 6.6rem) !important;
        line-height: 0.95 !important;
        overflow-wrap: anywhere !important;
    }
    .course-desc-brief { max-width: 760px !important; }
    .sub-nav {
        display: flex !important;
        gap: 4px !important;
        margin: 0 0 32px !important;
        padding: 0 !important;
        border-bottom: 1px solid var(--border-med) !important;
        flex-wrap: wrap !important;
    }
    .sub-nav-item {
        display: inline-flex !important;
        padding: 14px 10px !important;
        color: var(--text-dim) !important;
        font-family: var(--font-mono) !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        text-decoration: none !important;
        text-transform: uppercase !important;
        border-bottom: 2px solid transparent !important;
    }
    .sub-nav-item:hover,
    .sub-nav-item.active { color: var(--brand-purple) !important; }
    .sub-nav-item.active { border-bottom-color: var(--brand-purple) !important; }
    .content-section { padding: 0 !important; }
    .meta-panel-container { position: sticky !important; top: 96px !important; min-width: 0 !important; }
    .meta-panel { width: 100% !important; }
    @media (max-width: 1180px) {
        .page-container { grid-template-columns: minmax(0, 1fr) !important; }
        .meta-panel-container { position: static !important; }
    }
    @media (max-width: 760px) {
        .page-container { padding: 28px 16px 52px !important; }
        .course-code-wrapper { align-items: flex-start !important; flex-direction: column !important; }
        .course-code { font-size: clamp(3rem, 16vw, 4.5rem) !important; }
        .sub-nav { flex-wrap: nowrap !important; overflow-x: auto !important; }
    }
    </style>
"""


HUB_STYLE = """
    <style id="english-hub-style">
    .english-hub-main { flex: 1; min-width: 0; padding: clamp(42px, 6vw, 88px); }
    .english-hub-shell { width: min(1240px, 100%); margin: 0 auto; }
    .english-kicker { color: var(--brand-purple); font-family: var(--font-mono); font-size: .72rem; font-weight: 800; text-transform: uppercase; }
    .english-title { margin: 16px 0 18px; color: var(--text-main, #f8f7fb); font-family: var(--font-display); font-size: clamp(3.5rem, 8vw, 7rem); line-height: .92; text-transform: uppercase; }
    .english-lead { max-width: 760px; color: var(--text-dim, #8f8b9a); font-size: 1rem; line-height: 1.8; }
    .english-section { margin-top: 64px; }
    .english-section-title { margin-bottom: 18px; padding-bottom: 12px; border-bottom: 1px solid var(--border-dim); color: var(--text-dim); font-family: var(--font-mono); font-size: .72rem; text-transform: uppercase; }
    .english-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); border-top: 1px solid var(--border-dim); border-left: 1px solid var(--border-dim); }
    .english-card { min-height: 176px; padding: 28px; border-right: 1px solid var(--border-dim); border-bottom: 1px solid var(--border-dim); background: var(--bg-surface); color: inherit; text-decoration: none; transition: background 160ms ease, border-color 160ms ease; }
    .english-card:hover { background: rgba(184,41,234,.08); border-color: rgba(184,41,234,.45); }
    .english-card-code { color: var(--alert-red); font-family: var(--font-mono); font-size: .68rem; font-weight: 800; text-transform: uppercase; }
    .english-card h2, .english-card h3 { margin: 18px 0 8px; color: var(--text-main, #f8f7fb); font-family: var(--font-display); font-size: 1.65rem; line-height: 1.1; }
    .english-card p { color: var(--text-dim); line-height: 1.65; }
    .english-card-action { display: block; margin-top: 20px; color: var(--brand-purple); font-family: var(--font-mono); font-size: .68rem; font-weight: 800; text-transform: uppercase; }
    .english-resources { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .english-resources .english-card { min-height: 190px; }
    @media (max-width: 980px) { .english-resources { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
    @media (max-width: 700px) {
        .english-hub-main { padding: 34px 16px 56px; }
        .english-grid, .english-resources { grid-template-columns: 1fr; }
    }
    </style>
"""


MAIN = """
        <main class="english-hub-main">
            <div class="english-hub-shell">
                <div class="english-kicker">ACADEMICS // OTHER COURSES // ENGLISH</div>
                <h1 class="english-title">English Hub</h1>
                <p class="english-lead">A shared workspace for academic writing, research writing, grammar, referencing, editing, and reusable English-language learning resources.</p>

                <section class="english-section">
                    <div class="english-section-title">01 // Courses</div>
                    <div class="english-grid">
                        <a class="english-card" href="/Academics/other-courses/eng101/">
                            <span class="english-card-code">ENG101</span>
                            <h2>Intensive Writing</h2>
                            <p>Essay structure, classification, argument, process analysis, punctuation, thesis statements, and transitions.</p>
                            <span class="english-card-action">Open course -&gt;</span>
                        </a>
                        <a class="english-card" href="/Academics/other-courses/eng103/">
                            <span class="english-card-code">ENG103</span>
                            <h2>Research Writing Techniques</h2>
                            <p>Annotated bibliographies, research questions, methodology, survey design, ethics, results, and exam preparation.</p>
                            <span class="english-card-action">Open course -&gt;</span>
                        </a>
                    </div>
                </section>

                <section class="english-section">
                    <div class="english-section-title">02 // Shared Learning Resources</div>
                    <div class="english-grid english-resources">
                        <a class="english-card" href="/Academics/other-courses/eng101/extra-resources/writing-resources/"><span class="english-card-code">Writing Library</span><h3>Essay and Writing Guides</h3><p>Browse the complete writing-resource directory.</p><span class="english-card-action">Browse resources -&gt;</span></a>
                        <a class="english-card" href="/Academics/other-courses/eng101/extra-resources/grammar-cheat-sheet.pdf" target="_blank" rel="noopener"><span class="english-card-code">PDF</span><h3>Grammar Cheat Sheet</h3><p>A quick reference for grammar rules and common corrections.</p><span class="english-card-action">Open PDF -&gt;</span></a>
                        <a class="english-card" href="/Academics/other-courses/eng101/extra-resources/apa-referencing-cheat-sheet.pdf" target="_blank" rel="noopener"><span class="english-card-code">PDF</span><h3>APA Referencing</h3><p>A compact guide for academic citation and source use.</p><span class="english-card-action">Open PDF -&gt;</span></a>
                        <a class="english-card" href="/Academics/other-courses/eng101/extra-resources/self-editing-checklist.pdf" target="_blank" rel="noopener"><span class="english-card-code">PDF</span><h3>Self-Editing Checklist</h3><p>Review structure, clarity, evidence, grammar, and formatting before submission.</p><span class="english-card-action">Open PDF -&gt;</span></a>
                        <a class="english-card" href="/Academics/other-courses/eng101/slides/thesis-statement-guide/"><span class="english-card-code">Writing Skill</span><h3>Thesis Statements</h3><p>Build focused, arguable thesis statements for academic essays.</p><span class="english-card-action">Open guide -&gt;</span></a>
                        <a class="english-card" href="/Academics/other-courses/eng103/"><span class="english-card-code">Research Skill</span><h3>Research Writing</h3><p>Move from source collection to methodology, results, and ethical research practice.</p><span class="english-card-action">Open ENG103 -&gt;</span></a>
                    </div>
                </section>
            </div>
        </main>
"""


def add_before_head_end(text: str, addition: str) -> str:
    return text if addition.strip() in text else text.replace("</head>", f"{addition}\n</head>", 1)


def repair_engl101() -> None:
    text = ENG101.read_text(encoding="utf-8")
    text = re.sub(r'\s*<style id="eng101-layout-fix">.*?</style>', "", text, flags=re.S)
    text = add_before_head_end(text, ENGL101_STYLE)
    text = text.replace(">TBD</span>", ">None</span>")
    text = text.replace(
        "<ul class=\"learning-outcomes\">\n                                    <li>TBD</li>\n                                </ul>",
        """<ul class="learning-outcomes">
                                    <li>Develop focused thesis statements and organized academic essays.</li>
                                    <li>Use classification, argument, comparison, and process analysis effectively.</li>
                                    <li>Integrate, cite, and document sources using APA conventions.</li>
                                    <li>Revise and edit writing for clarity, unity, grammar, and punctuation.</li>
                                    <li>Give and apply constructive peer-review feedback.</li>
                                </ul>""",
    )
    ENG101.write_text(text, encoding="utf-8")


def build_hub() -> None:
    text = OTHER_INDEX.read_text(encoding="utf-8")
    text = re.sub(r"<title>.*?</title>", "<title>SHOUG.TECH // ENGLISH HUB</title>", text, count=1, flags=re.S)
    text = add_before_head_end(text, HUB_STYLE)
    text = re.sub(r'<main\b.*?</main>', MAIN, text, count=1, flags=re.S)
    HUB.parent.mkdir(parents=True, exist_ok=True)
    HUB.write_text(text, encoding="utf-8")


def update_other_courses() -> None:
    text = OTHER_INDEX.read_text(encoding="utf-8")
    text = text.replace("4 courses.<br>Writing, ethics,<br>physics, and foundations.", "6 courses.<br>One English hub,<br>and shared resources.")
    text = text.replace("5 courses.<br>One English hub,<br>and shared resources.", "6 courses.<br>One English hub,<br>and shared resources.")
    text = text.replace("<span>4\n                            Courses</span>", "<span>6 Courses</span>")
    text = text.replace("<span>5\n                            Courses</span>", "<span>6 Courses</span>")
    text = text.replace("<span>5 Courses</span>", "<span>6 Courses</span>")
    hub_row = '''<a class="course-row" href="/Academics/other-courses/english/">
                        <div class="course-code">ENGLISH</div>
                        <div class="course-name"><span>English Learning Hub</span></div>
                        <div class="course-status-area"><div class="status-tag status-complete">HUB</div><div class="row-arrow">-&gt;</div></div>
                    </a>'''
    eng103_row = '''<a class="course-row" href="/Academics/other-courses/eng103/">
                        <div class="course-code">ENG103</div>
                        <div class="course-name"><span>Research Writing Techniques</span></div>
                        <div class="course-status-area"><div class="status-tag status-complete">COMPLETE</div><div class="row-arrow">-&gt;</div></div>
                    </a>'''
    if 'href="/Academics/other-courses/english/"' not in text:
        text = text.replace('<div class="course-list">', f'<div class="course-list">{hub_row}', 1)
    if 'class="course-row" href="/Academics/other-courses/eng103/"' not in text:
        text = text.replace('<a class="course-row" href="/Academics/other-courses/eng101/">', f'{eng103_row}<a class="course-row" href="/Academics/other-courses/eng101/">', 1)
    OTHER_INDEX.write_text(text, encoding="utf-8")


def add_hub_to_sidebars() -> None:
    marker = '<ul id="tree-other-courses" class="tree-children'
    row = '<li class="tree-item"><a class="tree-file" href="/Academics/other-courses/english/">ENGLISH HUB</a></li>'
    for path in DOCS.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        if marker not in text or 'href="/Academics/other-courses/english/"' in text:
            continue
        start = text.find(marker)
        insert_at = text.find(">", start) + 1
        text = text[:insert_at] + row + text[insert_at:]
        path.write_text(text, encoding="utf-8")


def main() -> None:
    repair_engl101()
    update_other_courses()
    build_hub()
    add_hub_to_sidebars()
    print("Repaired ENG101 and built English Hub")


if __name__ == "__main__":
    main()
