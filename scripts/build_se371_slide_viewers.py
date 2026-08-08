#!/usr/bin/env python3
"""Build branded SE371 PDF viewers with university attribution."""

from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLIDES = ROOT / "docs/academics/software-engineering/se371/slides"
LECTURES = [
    ("01", "Introduction to the Web", "chapter-01-introduction-to-the-web.pdf"),
    ("02", "HTML Fundamentals", "chapter-02-html-2.pdf"),
    ("03", "CSS", "chapter-03-css.pdf"),
    ("04", "JavaScript", "chapter-04-javascript.pdf"),
    ("05", "Front-End JavaScript", "chapter-05-javascript-in-the-front-end.pdf"),
    ("06", "Server-Side Node.js", "chapter-06-server-side-node.pdf"),
    ("07", "Working with Databases", "chapter-07-working-with-databases.pdf"),
]
EXTRA_STYLES = '''<style id="se371-slide-viewer-styles">
.slide-viewer-shell{margin:0 40px 48px}.university-credit{border:1px solid var(--border-purple);background:rgba(184,41,234,.07);padding:16px 18px;margin-bottom:18px;color:var(--text-secondary);line-height:1.65}.university-credit strong{color:var(--text-purple-bright);font-family:var(--font-mono);letter-spacing:.04em}.slide-actions{display:flex;justify-content:flex-end;margin-bottom:12px}.slide-open-link{border:1px solid var(--border-purple);color:var(--text-purple-bright);padding:8px 14px;font-family:var(--font-mono);font-size:.75rem}.slide-open-link:hover{background:rgba(184,41,234,.12)}.pdf-frame{display:block;width:100%;height:78vh;min-height:640px;border:1px solid var(--border-med);background:#fff}@media(max-width:760px){.slide-viewer-shell{margin:0 16px 32px}.pdf-frame{height:70vh;min-height:480px}.university-credit{font-size:.82rem}}
</style>'''
UNIVERSITY_CREDIT = (
    '<div class="university-credit"><strong>PROPERTY OF PRINCE SULTAN UNIVERSITY</strong> &mdash; '
    'These slides are the intellectual property of Prince Sultan University. All academic content, materials, '
    'and resources are owned by the University and are shared here solely for personal study purposes. '
    'Redistribution or reproduction without explicit permission from Prince Sultan University is prohibited.</div>'
)


def replace_page_content(page: str, content: str) -> str:
    start = page.index('            <div class="directory-container"')
    end = page.index("\n\n\n    <footer", start)
    return page[:start] + "            " + content + page[end:]


def build_index(template: str) -> str:
    rows = []
    for number, title, pdf in LECTURES:
        slug = pdf.removesuffix(".pdf")
        rows.append(
            f'<a class="dir-row" href="/academics/software-engineering/se371/slides/{slug}/">'
            f'<div class="dir-num">{number}</div><div class="dir-title"><span class="dir-title-text">{html.escape(title)}</span></div>'
            '<div class="dir-status"><span class="status-tag available">AVAILABLE</span></div><div class="dir-arrow">-&gt;</div></a>'
        )
    directory = '<section class="slide-viewer-shell" aria-label="SE371 slide attribution">' + UNIVERSITY_CREDIT + '</section><div class="directory-container" aria-label="SE371 lecture slides"><div class="dir-header"><span>CH</span><span>LECTURE</span><span>SYS_STATE</span><span></span></div>' + "".join(rows) + "</div>"
    return replace_page_content(template, directory)


def build_viewer(template: str, number: str, title: str, pdf: str) -> str:
    slug = pdf.removesuffix(".pdf")
    route = f"https://shoug-tech.com/academics/software-engineering/se371/slides/{slug}/"
    page = re.sub(r"<title>.*?</title>", f"<title>Chapter {number}: {html.escape(title)} | SE371 Slides</title>", template, count=1, flags=re.S)
    page = re.sub(r'<meta name="description"[^>]*>', f'<meta name="description" content="View the embedded SE371 Chapter {number} lecture slides on {html.escape(title)}, credited to Prince Sultan University.">', page, count=1)
    page = re.sub(r'<link rel="canonical"[^>]*>', f'<link rel="canonical" href="{route}">', page, count=1)
    page = re.sub(r'<meta property="og:url"[^>]*>', f'<meta property="og:url" content="{route}">', page, count=1)
    page = page.replace('<span class="current" data-en-text="Slides" data-ar-text="الشرائح">Slides</span>', f'<a class="breadcrumb-link" href="/academics/software-engineering/se371/slides/">Slides</a> / <span class="current">Chapter {number}</span>', 1)
    page = page.replace('<div class="type-label" data-en-text="SLIDES" data-ar-text="الشرائح">SLIDES</div>', f'<div class="type-label">CHAPTER {number} // {html.escape(title)}</div>', 1)
    viewer = (
        f'<section class="slide-viewer-shell" aria-label="Chapter {number}: {html.escape(title)} slide viewer">{UNIVERSITY_CREDIT}'
        f'<div class="slide-actions"><a class="slide-open-link" href="../{pdf}" target="_blank" rel="noopener">OPEN PDF ↗</a></div>'
        f'<iframe class="pdf-frame" src="../{pdf}#view=FitH" title="Chapter {number}: {html.escape(title)} slides"></iframe></section>'
    )
    return replace_page_content(page, viewer)


def main() -> None:
    index_path = SLIDES / "index.html"
    template = index_path.read_text(encoding="utf-8")
    template = re.sub(r'<section class="slide-viewer-shell" aria-label="SE371 slide attribution">.*?</section>', '', template, count=1, flags=re.S)
    if 'id="se371-slide-viewer-styles"' in template:
        template = re.sub(r'<style id="se371-slide-viewer-styles">.*?</style>', EXTRA_STYLES, template, count=1, flags=re.S)
    else:
        template = template.replace("</head>", f"{EXTRA_STYLES}</head>")
    index_path.write_text(build_index(template), encoding="utf-8")
    for number, title, pdf in LECTURES:
        if not (SLIDES / pdf).is_file():
            raise FileNotFoundError(SLIDES / pdf)
        folder = SLIDES / pdf.removesuffix(".pdf")
        folder.mkdir(exist_ok=True)
        (folder / "index.html").write_text(build_viewer(template, number, title, pdf), encoding="utf-8")
    print(f"Built {len(LECTURES)} embedded SE371 slide viewers.")


if __name__ == "__main__":
    main()
