#!/usr/bin/env python3
"""Rebuild the SE423 slide breakdowns that didn't cover their decks (Team, Stakeholders, Old Ch 2 Software
Engineering) on the Estimation breakdown's template, with content written slide by slide in
scripts/se423_breakdowns/.

Each page keeps its own <title>, description, canonical URL and social metadata; the styles, header,
footer and scripts come from the Estimation page. Slide figures are re-embedded afterwards by
    python3 scripts/embed_slide_figures.py se423 --no-extract
(their sections are listed in scripts/slide-figures/se423.json).

    PYTHONUTF8=1 python3 scripts/build_se423_breakdowns.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from se423_breakdowns import team, stakeholders, software_engineering  # noqa: E402

BD = ROOT / "docs/academics/software-engineering/se423/slide-breakdowns"
TEMPLATE = BD / "08-estimation/estimation.html"
PAGES = {
    "05-team/team.html": team,
    "11-stakeholders/stakeholders.html": stakeholders,
    "04-software-engineering/software-engineering.html": software_engineering,
}
META = [
    r"<title>.*?</title>",
    r'<meta\s+name="description"\s+content="[^"]*"\s*/?>',
    r'<link\s+rel="canonical"\s+href="[^"]*"\s*/?>',
    r'<meta\s+property="og:title"\s+content="[^"]*"\s*/?>',
    r'<meta\s+property="og:description"\s+content="[^"]*"\s*/?>',
    r'<meta\s+property="og:url"\s+content="[^"]*"\s*/?>',
    r'<meta\s+name="twitter:title"\s+content="[^"]*"\s*/?>',
    r'<meta\s+name="twitter:description"\s+content="[^"]*"\s*/?>',
    r'<script type="application/ld\+json">.*?</script>',
]


def head_for(old_html, template_html):
    head = template_html[: template_html.index("</head>")]
    old_head = old_html[: old_html.index("</head>")]
    for pat in META:
        new = re.search(pat, old_head, re.S)
        if new and re.search(pat, head, re.S):
            head = re.sub(pat, lambda _m: new.group(0), head, count=1, flags=re.S)
    return head + "</head>"


def header_for(page, template_html):
    start = template_html.index("<body")
    end = template_html.index('<main id="main-content"')
    header = template_html[start:end]
    header = re.sub(r'<div class="brand-text">.*?</div>', f'<div class="brand-text">{page["brand"]}</div>', header, count=1, flags=re.S)
    links = "\n".join(f'          <a href="#{i}">{t}</a>' for i, t in page["nav"])
    header = re.sub(r'(<nav class="pillnav">).*?(</nav>)', lambda m: m.group(1) + "\n" + links + "\n        " + m.group(2), header, count=1, flags=re.S)
    return header


def hero(page):
    badges = "".join(f'<div class="badge">{b}</div>' for b in page["badges"])
    return f'''      <section class="hero">
        <div class="wrap">
          <div>
            <div class="eyebrow">{page["eyebrow"]}</div>
            <h1 class="hero-title">{page["title"]}</h1>
            <p class="hero-sub">{page["lead"]}</p>
            <div class="hero-badges">{badges}</div>
          </div>
        </div>
      </section>
'''


def tail_for(page, template_html):
    tail = template_html[template_html.index("    <footer>"):]
    tail = re.sub(r"(<footer>\s*<div>).*?(</div>)", lambda m: m.group(1) + page["footer"] + m.group(2), tail, count=1, flags=re.S)
    return tail


def main():
    template = TEMPLATE.read_text(encoding="utf-8")
    for rel, mod in PAGES.items():
        path = BD / rel
        old = path.read_text(encoding="utf-8")
        page = mod.PAGE
        out = (head_for(old, template) + "\n\n  " + header_for(page, template)
               + '<main id="main-content" tabindex="-1">\n' + hero(page) + "\n".join(mod.SECTIONS) + "    </main>\n\n"
               + tail_for(page, template))
        path.write_text(out, encoding="utf-8", newline="")
        print(f"{rel:52} {len(mod.SECTIONS):2} sections, {len(out) // 1024} KB")


if __name__ == "__main__":
    main()
