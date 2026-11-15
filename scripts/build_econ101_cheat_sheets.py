#!/usr/bin/env python3
"""Build the ECON101 cheat sheets (Major 1, Major 2, Final) in the CS331 Major I style.

The look comes straight from the CS331 Major I sheet (its <head>, stylesheet and
tab/answer script are reused as a template): a tab per chapter, an exam plan with
how to answer each question type, a "question clue → answer" table, formula
cards with worked examples, traps, and practice questions with hidden answers.

Content lives in scripts/econ101_cheat_content.py, written once per chapter from
scripts/study_content/econ101/*.md (the slide notes and handwriting), and each
sheet picks its chapters.

    python3 scripts/build_econ101_cheat_sheets.py

Writes docs/academics/other-courses/econ101/extra-resources/cheat-sheets/
{major-1,major-2,final}/<name>-cheat-sheet.html (the wrappers already iframe them).
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import econ101_cheat_content as content  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "docs/academics/computer-science/cs331/extra-resources/major-1-cheat-sheet/major-1-cheat-sheet.html"
OUT = ROOT / "docs/academics/other-courses/econ101/extra-resources/cheat-sheets"
SITE = "https://shoug-tech.com"
esc = html.escape


def head(t, title, desc, url):
    h = t[: t.index("<body")]
    h = re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", h, flags=re.S)
    h = re.sub(r'(<meta\s+name="description"\s+content=")[^"]*"', lambda m: m[1] + esc(desc) + '"', h)
    h = re.sub(r'(<meta\s+property="og:description"\s+content=")[^"]*"', lambda m: m[1] + esc(desc) + '"', h)
    h = re.sub(r'(<meta\s+property="og:title"\s+content=")[^"]*"', lambda m: m[1] + esc(title) + '"', h)
    h = re.sub(r'(<link\s+rel="canonical"\s+href=")[^"]*"', lambda m: m[1] + url + '"', h)
    h = re.sub(r'(<meta\s+property="og:url"\s+content=")[^"]*"', lambda m: m[1] + url + '"', h)
    return h


def script(t, key):
    s = t[t.rindex("<script>", 0, t.rindex("</body>")): t.rindex("</body>")]
    return s.replace('var KEY = "cs331-major1-tab";', f'var KEY = "{key}";')


def tabs(panels):
    out = []
    for i, p in enumerate(panels):
        sel = "true" if i == 0 else "false"
        extra = "" if i == 0 else ' tabindex="-1"'
        out.append(
            f'<button class="tab" role="tab" id="tab-{p["id"]}" aria-controls="{p["id"]}" aria-selected="{sel}"{extra}>'
            f'<span class="n">{esc(p["n"])}</span>{esc(p["tab"])}</button>'
        )
    return "".join(out)


def panel_html(p, first):
    links = "".join(f'<a class="btn" target="_top" href="{h}">{esc(l)}</a>' for l, h in p.get("links", []))
    links = f'<div class="links">{links}</div>' if links else ""
    hidden = "" if first else " hidden"
    return (
        f'<section class="panel" id="{p["id"]}" role="tabpanel" aria-labelledby="tab-{p["id"]}"{hidden}>'
        f'<div class="ch-head"><span class="num">{esc(p["num"])}</span><h2>{p["title"]}</h2>{links}</div>'
        f'<p class="ch-lead">{p["lead"]}</p>{p["body"]}</section>'
    )


LEGEND = (
    '<div class="legend" aria-label="Legend">'
    '<div><span class="swatch" style="background: var(--accent)"></span>Formula or key fact</div>'
    '<div><span class="swatch" style="background: var(--good)"></span>Worked example</div>'
    '<div><span class="swatch" style="background: var(--warn)"></span>Common mistake</div>'
    '<div><span class="swatch" style="background: var(--hook)"></span>How to answer</div></div>'
)


def build(sheet, t):
    panels = [sheet["plan"]] + [content.CHAPTERS[c] for c in sheet["chapters"]] + [sheet["practice"]]
    url = f"{SITE}/academics/other-courses/econ101/extra-resources/cheat-sheets/{sheet['slug']}/"
    body = (
        '<body><header class="topbar"><div class="wrap topbar-row">'
        f'<a class="brand" href="#top">ECON101 <span>{esc(sheet["brand"])}</span></a>'
        '<div class="actions"><div data-page-search-host></div>'
        '<button class="btn" type="button" id="toggle-answers">Show all <span class="long">answers</span></button>'
        '<button class="btn" type="button" onclick="toggleTheme()"><span data-theme-label>Dark</span></button></div></div>'
        f'<div class="wrap tabs" role="tablist" aria-label="Sections">{tabs(panels)}</div></header>'
        '<main class="wrap" id="top"><div class="hero"><div>'
        f'<div class="eyebrow">{esc(sheet["eyebrow"])}</div><h1>{esc(sheet["h1"])}</h1><p>{sheet["intro"]}</p></div>{LEGEND}</div>'
        + "".join(panel_html(p, i == 0) for i, p in enumerate(panels))
        + f'<footer>{sheet["footer"]}</footer></main>'
        + script(t, f"econ101-{sheet['slug']}-tab")
        + "</body>\n</html>\n"
    )
    return head(t, sheet["title"], sheet["desc"], url) + body


def main():
    t = TEMPLATE.read_text(encoding="utf-8")
    for sheet in content.SHEETS:
        path = OUT / sheet["slug"] / f"{sheet['slug']}-cheat-sheet.html"
        path.write_text(build(sheet, t), encoding="utf-8")
        n = sum(1 for _ in re.finditer(r'class="q"', path.read_text(encoding="utf-8")))
        print(f"{path.relative_to(ROOT)}: {len(sheet['chapters'])} chapters, {n} practice questions")


if __name__ == "__main__":
    main()
