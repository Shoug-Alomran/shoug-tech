#!/usr/bin/env python3
"""Build the SE423 glossary: docs/academics/software-engineering/se423/extra-resources/glossary/glossary.html.

One printable page with every chapter, each in its own section (terms A–Z), from scripts/se423_glossary/.
Search, chapter links and a "final chapters only" filter on screen; on paper each chapter starts a new page.
    PYTHONUTF8=1 python3 scripts/build_se423_glossary.py
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from se423_glossary import part1, part2, part3  # noqa: E402

OUT = ROOT / "docs/academics/software-engineering/se423/extra-resources/glossary/glossary.html"
CHAPTERS = part1.CHAPTERS + part2.CHAPTERS + part3.CHAPTERS


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def sort_key(term):
    return re.sub(r"^[^a-z0-9]+", "", term.lower())


def chapter_html(ch):
    terms = sorted(ch["terms"], key=lambda t: sort_key(t[0]))
    rows, letter = [], ""
    for term, definition in terms:
        first = sort_key(term)[:1].upper()
        if first != letter:
            letter = first
            rows.append(f'<div class="letter" aria-hidden="true">{letter}</div>')
        rows.append(f'<div class="entry" id="{ch["id"]}-{slug(term)}"><dt>{html.escape(term)}</dt><dd>{html.escape(definition)}</dd></div>')
    badge = "" if ch["final"] else '<span class="badge off">Not on the final</span>'
    return f'''  <section class="chapter" id="{ch["id"]}" data-final="{1 if ch["final"] else 0}">
    <header class="ch-head">
      <div class="ch-label">{html.escape(ch["label"])}</div>
      <h2>{html.escape(ch["title"])}</h2>
      <div class="ch-meta"><span class="count">{len(terms)} terms</span>{badge}</div>
    </header>
    <dl class="terms">
      {"".join(rows)}
    </dl>
  </section>
'''


def build():
    total = sum(len(c["terms"]) for c in CHAPTERS)
    toc = "".join(
        f'<li><a href="#{c["id"]}"><span class="toc-label">{html.escape(c["label"])}</span>'
        f'<span class="toc-title">{html.escape(c["title"])}</span><span class="toc-count">{len(c["terms"])}</span></a></li>'
        for c in CHAPTERS)
    chips = "".join(f'<a class="chip" href="#{c["id"]}" data-chip="{c["id"]}">{html.escape(c["label"])}</a>' for c in CHAPTERS)
    body = "".join(chapter_html(c) for c in CHAPTERS)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>SE423 Glossary</title>
<meta name="description" content="SE423 Software Project Management glossary: {total} terms from every chapter, A–Z by chapter, searchable and printable." />
<link rel="icon" type="image/png" sizes="256x256" href="/assets/shoug-favicon-v4.png" />
<script>
  try {{
    var t = localStorage.getItem("shoug-theme");
    document.documentElement.setAttribute("data-theme", t === "dark" || t === "light" ? t : (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"));
  }} catch (e) {{}}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Source+Serif+4:opsz,wght@8..60,600;8..60,700&display=swap" rel="stylesheet" />
<style>
  :root {{
    --bg: #f7f5f0; --panel: #ffffff; --ink: #1c1d22; --muted: #5d5f6a; --line: #dfdcd3;
    --accent: #6b3fd1; --accent-soft: #6b3fd114; --warn: #a3361f; --warn-soft: #a3361f12; --mark: #ffe58a;
    --gutter: clamp(16px, 4vw, 48px);
  }}
  html[data-theme="dark"] {{
    --bg: #121317; --panel: #1b1c22; --ink: #ecebe6; --muted: #a6a7b2; --line: #2e3038;
    --accent: #b49cff; --accent-soft: #b49cff1a; --warn: #ff9a85; --warn-soft: #ff9a8514; --mark: #7a5d00;
  }}
  * {{ box-sizing: border-box; }}
  html, body {{ overflow-x: clip; }}
  body {{ margin: 0; background: var(--bg); color: var(--ink); font: 15.5px/1.6 Inter, system-ui, -apple-system, "Segoe UI", sans-serif; }}
  a {{ color: var(--accent); }}
  .wrap {{ max-width: 1120px; margin: 0 auto; padding: 0 var(--gutter); }}

  /* toolbar */
  .bar {{ position: sticky; top: 0; z-index: 5; background: color-mix(in srgb, var(--bg) 92%, transparent); backdrop-filter: blur(8px); border-bottom: 1px solid var(--line); }}
  .bar .wrap {{ display: flex; flex-wrap: wrap; gap: 10px; align-items: center; padding-top: 10px; padding-bottom: 10px; }}
  .search {{ flex: 1 1 260px; display: flex; align-items: center; gap: 8px; background: var(--panel); border: 1px solid var(--line); border-radius: 10px; padding: 0 12px; }}
  .search input {{ flex: 1; border: 0; background: none; color: var(--ink); font: inherit; font-size: 16px; padding: 9px 0; min-width: 0; outline: none; }}
  .search:focus-within {{ border-color: var(--accent); }}
  .btn {{ font: inherit; font-size: 13.5px; font-weight: 600; border: 1px solid var(--line); background: var(--panel); color: var(--ink); border-radius: 999px; padding: 7px 14px; cursor: pointer; }}
  .btn:hover {{ border-color: var(--accent); }}
  .btn[aria-pressed="true"] {{ background: var(--accent); border-color: var(--accent); color: var(--panel); }}
  .chips {{ display: flex; flex-wrap: wrap; gap: 6px; width: 100%; }}
  .chip {{ font-size: 12.5px; font-weight: 600; text-decoration: none; color: var(--muted); border: 1px solid var(--line); border-radius: 999px; padding: 3px 10px; }}
  .chip:hover {{ color: var(--accent); border-color: var(--accent); }}
  .status {{ font-size: 13px; color: var(--muted); }}

  /* cover */
  .cover {{ padding: 40px 0 10px; }}
  .eyebrow {{ font-size: 12.5px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--accent); }}
  h1 {{ font-family: "Source Serif 4", Georgia, serif; font-size: clamp(32px, 5vw, 50px); line-height: 1.1; margin: 8px 0 10px; }}
  .lead {{ color: var(--muted); max-width: 70ch; margin: 0 0 20px; }}
  .toc {{ list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 330px), 1fr)); gap: 8px; }}
  .toc a {{ display: grid; grid-template-columns: 74px 1fr auto; gap: 10px; align-items: baseline; text-decoration: none; color: var(--ink); background: var(--panel); border: 1px solid var(--line); border-radius: 10px; padding: 10px 14px; }}
  .toc a:hover {{ border-color: var(--accent); }}
  .toc-label {{ font-weight: 800; color: var(--accent); font-size: 13px; }}
  .toc-title {{ font-weight: 600; font-size: 14px; }}
  .toc-count {{ font-size: 12.5px; color: var(--muted); }}

  /* chapters */
  .chapter {{ margin: 34px 0 0; padding-top: 6px; scroll-margin-top: 120px; }}
  .ch-head {{ border-bottom: 2px solid var(--ink); padding-bottom: 10px; margin-bottom: 14px; }}
  .ch-label {{ font-size: 12.5px; font-weight: 800; letter-spacing: .1em; text-transform: uppercase; color: var(--accent); }}
  .ch-head h2 {{ font-family: "Source Serif 4", Georgia, serif; font-size: clamp(22px, 3vw, 30px); line-height: 1.2; margin: 2px 0 6px; }}
  .ch-meta {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; font-size: 13px; color: var(--muted); }}
  .badge {{ font-size: 11.5px; font-weight: 700; padding: 1px 8px; border-radius: 999px; border: 1px solid; }}
  .badge.off {{ color: var(--warn); background: var(--warn-soft); }}
  .terms {{ margin: 0; columns: 2 340px; column-gap: 36px; }}
  .letter {{ font-family: "Source Serif 4", Georgia, serif; font-weight: 700; font-size: 18px; color: var(--accent); border-bottom: 1px solid var(--line); margin: 10px 0 6px; break-after: avoid; }}
  .entry {{ break-inside: avoid; padding: 6px 0 8px; }}
  .entry dt {{ font-weight: 700; }}
  .entry dd {{ margin: 1px 0 0; color: var(--ink); opacity: .88; }}
  .entry.hit dt, .entry.hit dd {{ background: transparent; }}
  mark {{ background: var(--mark); color: inherit; border-radius: 2px; padding: 0 1px; }}
  .empty {{ display: none; padding: 30px 0; color: var(--muted); text-align: center; }}
  footer {{ color: var(--muted); font-size: 13px; text-align: center; padding: 40px var(--gutter); }}
  [hidden] {{ display: none !important; }}

  @media print {{
    @page {{ margin: 16mm 14mm; }}
    :root, html[data-theme="dark"] {{ --bg: #fff; --panel: #fff; --ink: #000; --muted: #444; --line: #bbb; --accent: #3d2a8a; --warn: #8a2a14; }}
    body {{ font-size: 10.5pt; line-height: 1.4; background: #fff; }}
    .bar, .no-print {{ display: none !important; }}
    .cover {{ padding-top: 0; }}
    .toc a {{ border: 0; padding: 3px 0; }}
    .chapter {{ break-before: page; margin-top: 0; }}
    .chapter[hidden], .entry[hidden], .letter[hidden] {{ display: none !important; }}
    .terms {{ columns: 2; column-gap: 9mm; }}
    .entry {{ padding: 3pt 0 4pt; }}
    a {{ color: inherit; text-decoration: none; }}
    mark {{ background: none; }}
  }}
</style>
</head>
<body>
<div class="bar no-print">
  <div class="wrap">
    <label class="search"><span aria-hidden="true">🔎</span><input id="q" type="search" placeholder="Search {total} terms and definitions…" aria-label="Search the glossary" autocomplete="off" /></label>
    <button class="btn" id="final" type="button" aria-pressed="false" title="Hide Ch 6.2 and Ch 7, which are not on the final">Final chapters only</button>
    <button class="btn" id="print" type="button">Print / PDF</button>
    <button class="btn" id="theme" type="button">Dark</button>
    <span class="status" id="status" aria-live="polite"></span>
    <nav class="chips" aria-label="Chapters">{chips}</nav>
  </div>
</div>

<main class="wrap">
  <section class="cover">
    <div class="eyebrow">SE423 · Software Project Management</div>
    <h1>Glossary</h1>
    <p class="lead">{total} terms from every chapter, arranged A–Z within each chapter and written in the lecture slides' wording. Search above,
      or print it: each chapter starts on its own page. Chapters 6.2 and 7 are marked because they are not on the final.</p>
    <ol class="toc">{toc}</ol>
  </section>
{body}
  <p class="empty" id="empty">No terms match your search.</p>
</main>
<footer>SE423 glossary · study aid made by Shoug Alomran · check exact wording against your slides.</footer>

<script>
(function () {{
  var q = document.getElementById("q"), status = document.getElementById("status"), empty = document.getElementById("empty");
  var finalBtn = document.getElementById("final"), themeBtn = document.getElementById("theme");
  var chapters = [].slice.call(document.querySelectorAll(".chapter"));
  var entries = [].slice.call(document.querySelectorAll(".entry"));
  entries.forEach(function (e) {{ e._dt = e.querySelector("dt"); e._dd = e.querySelector("dd"); e._t = e._dt.textContent; e._d = e._dd.textContent; }});
  function esc(s) {{ return s.replace(/[&<>]/g, function (c) {{ return {{ "&": "&amp;", "<": "&lt;", ">": "&gt;" }}[c]; }}); }}
  function mark(text, words) {{
    var out = esc(text);
    words.forEach(function (w) {{ out = out.replace(new RegExp("(" + w.replace(/[.*+?^${{}}()|[\\]\\\\]/g, "\\\\$&") + ")", "ig"), "<mark>$1</mark>"); }});
    return out;
  }}
  var finalOnly = false;
  try {{ finalOnly = localStorage.getItem("se423-glossary-final") === "1"; }} catch (e) {{}}
  function apply() {{
    var words = q.value.trim().toLowerCase().split(/\\s+/).filter(Boolean);
    var shown = 0;
    chapters.forEach(function (ch) {{
      var off = finalOnly && ch.getAttribute("data-final") === "0";
      var n = 0;
      [].forEach.call(ch.querySelectorAll(".entry"), function (e) {{
        var hay = (e._t + " " + e._d).toLowerCase();
        var ok = !off && words.every(function (w) {{ return hay.indexOf(w) > -1; }});
        e.hidden = !ok;
        e._dt.innerHTML = words.length && ok ? mark(e._t, words) : esc(e._t);
        e._dd.innerHTML = words.length && ok ? mark(e._d, words) : esc(e._d);
        if (ok) n++;
      }});
      [].forEach.call(ch.querySelectorAll(".letter"), function (l) {{
        var next = l.nextElementSibling, any = false;
        while (next && !next.classList.contains("letter")) {{ if (!next.hidden) any = true; next = next.nextElementSibling; }}
        l.hidden = !any;
      }});
      ch.hidden = n === 0;
      var chip = document.querySelector('[data-chip="' + ch.id + '"]');
      if (chip) chip.hidden = n === 0;
      shown += n;
    }});
    empty.style.display = shown ? "none" : "block";
    status.textContent = words.length || finalOnly ? shown + " of " + entries.length + " terms" : entries.length + " terms";
    finalBtn.setAttribute("aria-pressed", String(finalOnly));
  }}
  q.addEventListener("input", apply);
  finalBtn.addEventListener("click", function () {{
    finalOnly = !finalOnly;
    try {{ localStorage.setItem("se423-glossary-final", finalOnly ? "1" : "0"); }} catch (e) {{}}
    apply();
  }});
  document.getElementById("print").addEventListener("click", function () {{ window.print(); }});
  var root = document.documentElement;
  function paint() {{ themeBtn.textContent = root.getAttribute("data-theme") === "dark" ? "Light" : "Dark"; }}
  themeBtn.addEventListener("click", function () {{
    var t = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", t);
    try {{ localStorage.setItem("shoug-theme", t); }} catch (e) {{}}
    paint();
  }});
  window.addEventListener("storage", function (e) {{ if (e.key === "shoug-theme" && e.newValue) {{ root.setAttribute("data-theme", e.newValue); paint(); }} }});
  document.addEventListener("keydown", function (e) {{
    if (e.key === "/" && document.activeElement !== q) {{ e.preventDefault(); q.focus(); }}
    if (e.key === "Escape" && document.activeElement === q) {{ q.value = ""; apply(); }}
  }});
  paint();
  apply();
}})();
</script>
</body>
</html>
'''


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    dupes = {}
    for c in CHAPTERS:
        seen = set()
        for t, _ in c["terms"]:
            k = t.lower()
            if k in seen:
                dupes.setdefault(c["label"], []).append(t)
            seen.add(k)
    if dupes:
        print("duplicate terms:", dupes)
    OUT.write_text(build(), encoding="utf-8", newline="")
    print(f"{OUT.relative_to(ROOT)}: {sum(len(c['terms']) for c in CHAPTERS)} terms in {len(CHAPTERS)} chapters")
    for c in CHAPTERS:
        print(f"  {c['label']:9} {len(c['terms']):3}  {c['title']}")


if __name__ == "__main__":
    main()
