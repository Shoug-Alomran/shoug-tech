#!/usr/bin/env python3
"""Build the ETHCS303 ChatGPT Notes gallery page from the photos on disk.

The notes are screenshots, so the viewer is a grouped image gallery rather than
the usual single-document embed.  Chrome (head, header, sidebar, footer) is
cloned from a sibling Study Material page so the page stays identical to the
rest of the course after any shell change; only <main> is authored here.
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from normalize_page_urls import normalize  # noqa: E402

COURSE = ROOT / "docs/academics/other-courses/ethcs303/extra-resources"
FOLDER = COURSE / "chatgpt-notes"
CHROME = COURSE / "important-people/index.html"
BASE = "/academics/other-courses/ethcs303/extra-resources/"

TITLE = "ChatGPT Notes"
TITLE_AR = "ملاحظات ChatGPT"
ITEM_LABEL = "ITEM_04 // EXTRA RESOURCES"
PREV = BASE + "chapter-10-summary/"
NEXT = BASE + "cheat-sheets/"

# Each group is (first photo number, heading, Arabic heading).  Photos are named
# with a leading number, so a group owns every photo from its start up to the
# next group's start.
GROUPS = [
    (1, "Ethical Theories", "النظريات الأخلاقية"),
    (5, "Ethical Issues in Systems Analysis and Software Engineering",
     "القضايا الأخلاقية في تحليل النظم وهندسة البرمجيات"),
    (10, "Network Security and Privacy", "أمن الشبكات والخصوصية"),
    (23, "Cloud Computing Privacy and Security", "خصوصية وأمن الحوسبة السحابية"),
    (24, "Privacy in Cyberspace", "الخصوصية في الفضاء السيبراني"),
    (35, "Social Media", "وسائل التواصل الاجتماعي"),
    (37, "Business Ethics", "أخلاقيات الأعمال"),
    (40, "Cyber Laws", "قوانين الجرائم السيبرانية"),
]

GALLERY_STYLE = """
<style id="chatgpt-notes-gallery-style">
.notes-intro{max-width:70ch;color:var(--text-secondary,#a09fa6);font-size:.95rem;line-height:1.7;padding:0 clamp(24px,4vw,64px) 8px}
.notes-group{padding:28px clamp(24px,4vw,64px) 0}
.notes-group-head{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;border-bottom:1px solid var(--border-dim,rgba(255,255,255,.08));padding-bottom:10px;margin-bottom:20px}
.notes-group-title{font-family:var(--font-mono,"JetBrains Mono",monospace);font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;color:var(--brand-purple,#b829ea);margin:0}
.notes-group-count{font-family:var(--font-mono,"JetBrains Mono",monospace);font-size:.68rem;color:var(--text-secondary,#a09fa6)}
.notes-grid{display:grid;gap:18px;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));align-items:start}
.notes-card{display:flex;flex-direction:column;border:1px solid var(--border-med,rgba(255,255,255,.12));background:var(--bg-elevated,#0a0611);text-decoration:none;transition:border-color .15s ease,transform .15s ease}
.notes-card:hover,.notes-card:focus-visible{border-color:var(--brand-purple,#b829ea);transform:translateY(-2px)}
.notes-card img{display:block;width:100%;height:auto;background:#000}
.notes-card figcaption{padding:12px 14px;font-size:.86rem;line-height:1.45;color:var(--text-primary,#fff)}
.notes-card .notes-num{font-family:var(--font-mono,"JetBrains Mono",monospace);font-size:.68rem;color:var(--brand-purple,#b829ea);margin-right:8px}
.notes-foot{padding:32px clamp(24px,4vw,64px) 48px}
@media(min-width:1600px){.notes-grid{grid-template-columns:repeat(auto-fill,minmax(360px,1fr))}}
@media(max-width:700px){.notes-group{padding:22px 18px 0}.notes-intro{padding:0 18px 8px}.notes-grid{grid-template-columns:1fr;gap:14px}.notes-foot{padding:24px 18px 36px}}
</style>
"""


def photos() -> list[tuple[int, str, str]]:
    """(number, filename, caption) for every numbered photo in the folder."""
    found = []
    for path in sorted(FOLDER.glob("*.jpg")):
        match = re.match(r"(\d+)-(.+)\.jpg$", path.name)
        if not match:
            continue
        words = match.group(2).replace("-", " ")
        caption = words[:1].upper() + words[1:]
        for term, fixed in (
            (" vs ", " vs. "), ("Dos vs. ddos", "DoS vs. DDoS"), ("Rfid", "RFID"),
            ("Chatgpt", "ChatGPT"), ("E government", "E-government"),
        ):
            caption = caption.replace(term, fixed)
        found.append((int(match.group(1)), path.name, caption))
    return found


def gallery_main() -> str:
    items = photos()
    starts = [g[0] for g in GROUPS]
    parts = [
        '<main class="sys-main" id="main-content" tabindex="-1">',
        '        <div class="content-topbar">',
        '          <div class="breadcrumb">',
        '            <a class="breadcrumb-link" href="/academics/">Academics</a> /',
        '            <a class="breadcrumb-link" href="/academics/other-courses/">Other Courses</a> /',
        '            <a class="breadcrumb-link" href="/academics/other-courses/ethcs303/">ETHCS303</a> /',
        f'            <a class="breadcrumb-link" href="{BASE}">Study Material</a>',
        f'            / <span class="current">{TITLE}</span>',
        '          </div>',
        '          <div class="sys-time" id="live-clock">SYS_TIME [ 00 00 00 ]</div>',
        '        </div>',
        '        <div class="page-header">',
        f'          <div class="ch-label">{ITEM_LABEL}</div>',
        f'          <h1 class="ch-title" data-en-text="{TITLE}" data-ar-text="{TITLE_AR}">{TITLE}</h1>',
        '          <div class="action-buttons">',
        f'            <a class="btn btn-secondary" href="{BASE}">[ &lt;- BACK TO INDEX ]</a>',
        '          </div>',
        '        </div>',
        '        <div class="nav-strip">',
        f'          <a href="{PREV}" class="nav-link prev">&lt;- PREVIOUS</a>',
        f'          <a href="{NEXT}" class="nav-link next">NEXT -&gt;</a>',
        '        </div>',
        f'        <p class="notes-intro">{len(items)} study screenshots generated while revising ETHCS303, '
        'grouped by topic. Select any note to open the full-size image.</p>',
    ]

    for index, (start, heading, heading_ar) in enumerate(GROUPS):
        end = starts[index + 1] if index + 1 < len(starts) else 10 ** 6
        group = [item for item in items if start <= item[0] < end]
        if not group:
            continue
        parts += [
            '        <section class="notes-group">',
            '          <div class="notes-group-head">',
            f'            <h2 class="notes-group-title" data-en-text="{heading}" '
            f'data-ar-text="{heading_ar}">{heading}</h2>',
            f'            <span class="notes-group-count">{len(group)} notes</span>',
            '          </div>',
            '          <div class="notes-grid">',
        ]
        for number, name, caption in group:
            safe_name = html.escape(name, quote=True)
            safe_caption = html.escape(caption)
            parts += [
                f'            <a class="notes-card" href="./{safe_name}" target="_blank" '
                'rel="noopener noreferrer">',
                '              <figure style="margin:0">',
                f'                <img src="./{safe_name}" loading="lazy" decoding="async" '
                f'alt="{safe_caption}" />',
                f'                <figcaption><span class="notes-num">{number:02d}</span>'
                f'{safe_caption}</figcaption>',
                '              </figure>',
                '            </a>',
            ]
        parts += ['          </div>', '        </section>']

    parts += [
        '        <div class="notes-foot">',
        f'          <a class="btn btn-secondary" href="{BASE}">[ &lt;- BACK TO INDEX ]</a>',
        '        </div>',
        '      </main>',
    ]
    return "\n".join(parts)


def main() -> None:
    page = CHROME.read_text(encoding="utf-8")
    page = re.sub(r'<main\b[^>]*\bid="main-content"[^>]*>.*?</main>',
                  lambda _: gallery_main(), page, count=1, flags=re.I | re.S)
    page = re.sub(r"<title>.*?</title>",
                  f"<title>{TITLE} | ETHCS303 | Shoug Alomran</title>", page,
                  count=1, flags=re.I | re.S)
    if 'id="chatgpt-notes-gallery-style"' not in page:
        page = page.replace("</head>", GALLERY_STYLE + "</head>", 1)

    target = FOLDER / "index.html"
    page = normalize(page, target)
    target.write_text(page, encoding="utf-8")
    print(f"built {target.relative_to(ROOT)} with {len(photos())} photos")


if __name__ == "__main__":
    main()
