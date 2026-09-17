#!/usr/bin/env python3
"""Rebuild SE371 chapter routes as real viewer pages.

SE371's chapter index files were accidentally cloned from the slide-breakdown
listing after the site shell changed from `content-area` to `sys-main`.  The
old builder's regex then stopped matching silently, so every chapter URL showed
the listing page even though the authored chapter HTML existed.

This repair deliberately uses the CURRENT SE371 listing as chrome and replaces
only its <main> region.  That keeps header/sidebar/theme behavior identical to
the rest of the course while making every chapter route a dedicated viewer.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLIDES = ROOT / "docs" / "academics" / "software-engineering" / "se371" / "slide-breakdowns"
BASE = "/academics/software-engineering/se371/slide-breakdowns/"

CHAPTERS = [
    ("01-introduction-to-the-web", "introduction-to-the-web.html", "Introduction to the Web"),
    ("02-html", "html.html", "HTML: Documents, Tables and Forms"),
    ("03-css", "css.html", "CSS: Selectors, Cascade and Layout"),
    ("04-javascript", "javascript.html", "JavaScript Fundamentals"),
    ("05-javascript-in-the-front-end", "javascript-in-the-front-end.html", "JavaScript in the Front End"),
    ("06-server-side-node", "server-side-node.html", "Server-Side: Node.js and Express"),
    ("07-working-with-databases", "working-with-databases.html", "Working with Databases"),
]

MAIN_RE = re.compile(r'<main\b[^>]*\bid="main-content"[^>]*>.*?</main>', re.I | re.S)
TITLE_RE = re.compile(r'<title>.*?</title>', re.I | re.S)

VIEWER_STYLE = """
<style id="se371-viewer-route-style">
.se371-viewer-head{padding:clamp(28px,4vw,56px) clamp(24px,4vw,64px) 24px;border-bottom:1px solid var(--border-dim,rgba(255,255,255,.08))}
.se371-viewer-kicker{font-family:var(--font-mono,"JetBrains Mono",monospace);font-size:.72rem;letter-spacing:.16em;color:var(--brand-purple,#b829ea);margin-bottom:10px}
.se371-viewer-title{font-family:var(--font-display,"Rajdhani",sans-serif);font-size:clamp(2rem,4vw,3.6rem);line-height:1.05;color:var(--text-primary,#fff);margin:0 0 20px}
.se371-viewer-actions{display:flex;flex-wrap:wrap;gap:10px}
.se371-viewer-actions a{font-family:var(--font-mono,"JetBrains Mono",monospace);font-size:.72rem;letter-spacing:.08em;text-decoration:none;padding:10px 14px;border:1px solid rgba(184,41,234,.55);color:#d978ff}
.se371-viewer-actions a:hover{background:rgba(184,41,234,.12)}
.se371-viewer-nav{display:flex;justify-content:space-between;gap:12px;padding:12px clamp(24px,4vw,64px);border-bottom:1px solid var(--border-dim,rgba(255,255,255,.08))}
.se371-viewer-nav a{font-family:var(--font-mono,"JetBrains Mono",monospace);font-size:.7rem;color:var(--text-secondary,#a09fa6);text-decoration:none}
.se371-viewer-nav a:hover{color:#d978ff}
.embed-area-wrapper{padding:16px clamp(16px,3vw,40px) 36px;min-height:70vh}
.embed-container,.rendered-content{width:100%;height:100%}
.embed-frame{display:block;width:100%;height:calc(100vh - 220px);min-height:720px;border:1px solid var(--border-med,rgba(255,255,255,.12));background:#0a0611}
@media(max-width:700px){.embed-frame{height:78vh;min-height:560px}.se371-viewer-head{padding:24px 18px 18px}.embed-area-wrapper{padding:12px}}
</style>
"""


def viewer_main(i: int, slug: str, filename: str, title: str) -> str:
    prev_link = ""
    next_link = ""
    if i:
        pslug, _, ptitle = CHAPTERS[i - 1]
        prev_link = f'<a href="{BASE}{pslug}/">&lt;- {html.escape(ptitle)}</a>'
    if i + 1 < len(CHAPTERS):
        nslug, _, ntitle = CHAPTERS[i + 1]
        next_link = f'<a href="{BASE}{nslug}/">{html.escape(ntitle)} -&gt;</a>'
    safe_title = html.escape(title)
    return f'''<main class="sys-main" id="main-content" tabindex="-1">
{VIEWER_STYLE}
<div class="content-topbar">
  <div class="breadcrumb"><a class="breadcrumb-link" href="/academics/">Academics</a> / <a class="breadcrumb-link" href="/academics/software-engineering/">Software Engineering</a> / <a class="breadcrumb-link" href="/academics/software-engineering/se371/">SE371</a> / <a class="breadcrumb-link" href="{BASE}">Slide Breakdowns</a> / <span class="current">{safe_title}</span></div>
  <div class="sys-time" id="live-clock">SYS_TIME [ 00 00 00 ]</div>
</div>
<section class="se371-viewer-head">
  <div class="se371-viewer-kicker">CHAPTER_{i + 1:02d} // SLIDE BREAKDOWN</div>
  <h1 class="se371-viewer-title">{safe_title}</h1>
  <div class="se371-viewer-actions"><a href="./{filename}" target="_blank" rel="noopener noreferrer">[ OPEN IN NEW TAB -&gt; ]</a><a href="{BASE}">[ &lt;- BACK TO INDEX ]</a></div>
</section>
<div class="se371-viewer-nav"><span>{prev_link}</span><span>{next_link}</span></div>
<div class="embed-area-wrapper">
  <div class="embed-container" id="embedded-content">
    <div class="rendered-content"><iframe class="embed-frame legacy-html-frame" src="./{filename}" loading="lazy" title="{safe_title}"></iframe></div>
  </div>
</div>
</main>'''


def main() -> None:
    template_path = SLIDES / "index.html"
    template = template_path.read_text(encoding="utf-8")
    if not MAIN_RE.search(template):
        raise SystemExit("SE371 listing shell no longer contains #main-content; refusing to generate broken viewers")

    for i, (slug, filename, title) in enumerate(CHAPTERS):
        folder = SLIDES / slug
        source = folder / filename
        if not source.is_file():
            raise SystemExit(f"Missing authored SE371 breakdown: {source.relative_to(ROOT)}")

        page = MAIN_RE.sub(lambda _: viewer_main(i, slug, filename, title), template, count=1)
        page = TITLE_RE.sub(f"<title>SHOUG.TECH | SE371 {html.escape(title)}</title>", page, count=1)
        out = folder / "index.html"
        out.write_text(page, encoding="utf-8")
        print(f"fixed {out.relative_to(ROOT)} -> ./{filename}")

    print(f"SE371 viewer repair complete: {len(CHAPTERS)} dedicated chapter routes rebuilt")


if __name__ == "__main__":
    main()
