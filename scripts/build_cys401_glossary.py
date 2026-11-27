#!/usr/bin/env python3
"""Build the searchable and printable CYS401 glossary and its site wrapper."""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from cys401_glossary_content import CHAPTERS  # noqa: E402

BASE = "/academics/cybersecurity/cys401/extra-resources/"
OUT = ROOT / "docs/academics/cybersecurity/cys401/extra-resources/glossary"


def esc(value):
    return html.escape(value, quote=False)


def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def sort_key(term):
    return re.sub(r"^[^a-z0-9]+", "", term.lower())


def chapter_html(chapter):
    rows = []
    letter = ""
    terms = sorted(chapter["terms"], key=lambda item: sort_key(item[0]))
    for term, definition in terms:
        initial = sort_key(term)[:1].upper()
        if initial != letter:
            letter = initial
            rows.append(f'<div class="letter" aria-hidden="true">{esc(letter)}</div>')
        rows.append(f'<div class="entry" id="{chapter["id"]}-{slug(term)}"><dt>{esc(term)}</dt><dd>{esc(definition)}</dd></div>')
    return f'''<section class="chapter" id="{chapter['id']}">
  <header class="chapter-head"><div class="ch-label">{esc(chapter['label'])}</div><h2>{esc(chapter['title'])}</h2><span class="count">{len(terms)} terms</span></header>
  <dl class="terms">{"".join(rows)}</dl>
</section>'''


def glossary_html():
    total = sum(len(chapter["terms"]) for chapter in CHAPTERS)
    toc = "".join(
        f'<li><a href="#{ch["id"]}"><span>{esc(ch["label"])}</span><strong>{esc(ch["title"])}</strong><small>{len(ch["terms"])}</small></a></li>'
        for ch in CHAPTERS
    )
    chips = "".join(f'<a class="chip" href="#{ch["id"]}">{esc(ch["label"])}</a>' for ch in CHAPTERS)
    chapters = "\n".join(chapter_html(ch) for ch in CHAPTERS)
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>CYS401 Cybersecurity Glossary</title>
  <meta name="description" content="CYS401 Cybersecurity glossary: {total} key terms across all ten chapters, searchable, organized A–Z, and printable." />
  <link rel="canonical" href="https://shoug-tech.com{BASE}glossary/glossary.html" />
  <link rel="icon" type="image/png" sizes="256x256" href="/assets/shoug-favicon-v4.png" />
  <script>
    try {{ var t = localStorage.getItem("shoug-theme"); document.documentElement.dataset.theme = t === "dark" || t === "light" ? t : (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"); }} catch (e) {{}}
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Source+Serif+4:opsz,wght@8..60,600;8..60,700&display=swap" rel="stylesheet" />
  <style>
    :root {{ --bg:#f7f5f0;--panel:#fff;--ink:#1c1d22;--muted:#5d5f6a;--line:#dfdcd3;--accent:#a21e32;--accent-soft:#a21e3214;--mark:#ffe58a;--gutter:clamp(16px,4vw,48px); }}
    html[data-theme="dark"] {{ --bg:#121317;--panel:#1b1c22;--ink:#ecebe6;--muted:#a6a7b2;--line:#2e3038;--accent:#ff7184;--accent-soft:#ff71841a;--mark:#7a5d00; }}
    * {{ box-sizing:border-box }} html,body {{ margin:0;overflow-x:clip }} body {{ background:var(--bg);color:var(--ink);font:15.5px/1.6 Inter,system-ui,sans-serif }} a {{ color:var(--accent) }}
    .wrap {{ max-width:1120px;margin:auto;padding:0 var(--gutter) }} .bar {{ position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--bg) 94%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line) }}
    .bar .wrap {{ display:flex;flex-wrap:wrap;gap:10px;align-items:center;padding-top:10px;padding-bottom:10px }} .search {{ flex:1 1 260px;display:flex;align-items:center;gap:8px;background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:0 12px }}
    .search input {{ flex:1;min-width:0;border:0;background:none;color:var(--ink);font:inherit;font-size:16px;padding:9px 0;outline:none }} .btn {{ font:inherit;font-size:13.5px;font-weight:600;border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:999px;padding:7px 14px;cursor:pointer }} .btn:hover {{ border-color:var(--accent) }}
    .status {{ color:var(--muted);font-size:13px;white-space:nowrap }} .chips {{ flex-basis:100%;display:flex;gap:7px;overflow-x:auto;padding:2px 0 5px }} .chip {{ flex:none;border:1px solid var(--line);border-radius:999px;padding:4px 10px;text-decoration:none;color:var(--muted);font-size:12px }} .chip:hover {{ color:var(--accent);border-color:var(--accent) }}
    .cover {{ padding:46px 0 30px }} .eyebrow,.ch-label {{ color:var(--accent);font-size:12px;font-weight:800;letter-spacing:.14em;text-transform:uppercase }} h1 {{ max-width:850px;margin:8px 0;font:700 clamp(38px,7vw,68px)/1.02 "Source Serif 4",Georgia,serif;letter-spacing:-.035em }} .lead {{ max-width:800px;color:var(--muted);font-size:17px }}
    .toc {{ display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,330px),1fr));gap:8px;margin:26px 0 0;padding:0;list-style:none }} .toc a {{ display:grid;grid-template-columns:55px 1fr auto;gap:8px;align-items:center;padding:10px 12px;border:1px solid var(--line);border-radius:10px;background:var(--panel);text-decoration:none;color:var(--ink) }} .toc a:hover {{ border-color:var(--accent);background:var(--accent-soft) }} .toc span,.toc small {{ color:var(--accent);font:700 11px/1.4 ui-monospace,monospace;text-transform:uppercase }} .toc strong {{ font-size:13px }}
    .chapter {{ padding:27px 0 38px;border-top:1px solid var(--line);scroll-margin-top:110px }} .chapter-head {{ display:grid;grid-template-columns:auto 1fr auto;align-items:end;gap:8px 14px;margin-bottom:16px }} .chapter-head h2 {{ margin:0;font:700 clamp(25px,4vw,36px)/1.1 "Source Serif 4",Georgia,serif }} .count {{ color:var(--muted);font-size:12px;white-space:nowrap }} .terms {{ margin:0 }} .entry {{ display:grid;grid-template-columns:minmax(180px, .32fr) 1fr;gap:8px 22px;padding:10px 12px;border-bottom:1px solid var(--line) }} .entry dt {{ color:var(--ink);font-weight:700 }} .entry dd {{ margin:0;color:var(--muted) }} .letter {{ padding:18px 10px 4px;color:var(--accent);font:800 12px ui-monospace,monospace }} mark {{ background:var(--mark);color:#201800;border-radius:2px }} .empty {{ display:none;padding:30px;text-align:center;color:var(--muted) }} footer {{ padding:24px var(--gutter);border-top:1px solid var(--line);color:var(--muted);text-align:center;font-size:12px }}
    @media(max-width:600px) {{ .entry {{ grid-template-columns:1fr;gap:2px }} .chapter-head {{ grid-template-columns:auto 1fr }} .count {{ grid-column:2 }} }}
    @media print {{ :root {{ --bg:#fff;--panel:#fff;--ink:#111;--muted:#333;--line:#bbb;--accent:#7f1828 }} body {{ font-size:10pt }} .no-print,.toc {{ display:none!important }} .wrap {{ max-width:none;padding:0 }} .cover {{ padding:0 0 12px }} .chapter {{ break-before:page;border:0;padding:0 }} .chapter:first-of-type {{ break-before:auto }} .entry {{ padding:4px 0;break-inside:avoid }} footer {{ display:none }} }}
  </style>
</head>
<body>
  <div class="bar no-print"><div class="wrap">
    <label class="search"><span aria-hidden="true">⌕</span><input id="q" type="search" placeholder="Search {total} terms…" aria-label="Search the glossary" autocomplete="off" /></label>
    <button class="btn" id="print" type="button">Print / PDF</button><button class="btn" id="theme" type="button">Dark</button><span class="status" id="status" aria-live="polite"></span>
    <nav class="chips" aria-label="Chapters">{chips}</nav>
  </div></div>
  <main class="wrap">
    <header class="cover"><div class="eyebrow">CYS401 · Cybersecurity</div><h1>Glossary</h1><p class="lead">{total} key terms from all ten chapters. Each chapter is arranged A–Z. Search by term or definition, jump to a chapter, or print a clean study copy.</p><ol class="toc">{toc}</ol></header>
    {chapters}
    <p class="empty" id="empty">No terms match your search.</p>
  </main>
  <footer>CYS401 glossary · study aid by Shoug Alomran · check exact wording against your course slides.</footer>
  <script>
    (function() {{
      var q=document.getElementById("q"),status=document.getElementById("status"),empty=document.getElementById("empty"),themeBtn=document.getElementById("theme");
      var chapters=[].slice.call(document.querySelectorAll(".chapter")),entries=[].slice.call(document.querySelectorAll(".entry"));
      entries.forEach(function(e){{e._dt=e.querySelector("dt");e._dd=e.querySelector("dd");e._t=e._dt.textContent;e._d=e._dd.textContent;}});
      function esc(s){{return s.replace(/[&<>]/g,function(c){{return {{"&":"&amp;","<":"&lt;",">":"&gt;"}}[c];}});}}
      function mark(text,words){{var out=esc(text);words.forEach(function(w){{out=out.replace(new RegExp("("+w.replace(/[.*+?^${{}}()|[\\]\\\\]/g,"\\\\$&")+")","ig"),"<mark>$1</mark>");}});return out;}}
      function apply(){{var words=q.value.trim().toLowerCase().split(/\\s+/).filter(Boolean),shown=0;entries.forEach(function(e){{var ok=words.every(function(w){{return (e._t+" "+e._d).toLowerCase().indexOf(w)>-1;}});e.hidden=!ok;e._dt.innerHTML=words.length&&ok?mark(e._t,words):esc(e._t);e._dd.innerHTML=words.length&&ok?mark(e._d,words):esc(e._d);if(ok)shown++;}});chapters.forEach(function(ch){{var count=ch.querySelectorAll(".entry:not([hidden])").length;ch.hidden=!count;var chip=document.querySelector('.chip[href="#'+ch.id+'"]');if(chip)chip.hidden=!count;[].forEach.call(ch.querySelectorAll(".letter"),function(l){{var n=l.nextElementSibling,found=false;while(n&&!n.classList.contains("letter")){{if(!n.hidden)found=true;n=n.nextElementSibling;}}l.hidden=!found;}});}});empty.style.display=shown?"none":"block";status.textContent=words.length?shown+" of "+entries.length+" terms":entries.length+" terms";}}
      q.addEventListener("input",apply);document.getElementById("print").addEventListener("click",function(){{window.print();}});
      var root=document.documentElement;function paint(){{themeBtn.textContent=root.dataset.theme==="dark"?"Light":"Dark";}}
      themeBtn.addEventListener("click",function(){{var t=root.dataset.theme==="dark"?"light":"dark";root.dataset.theme=t;try{{localStorage.setItem("shoug-theme",t);}}catch(e){{}}paint();}});
      window.addEventListener("storage",function(e){{if(e.key==="shoug-theme"&&e.newValue){{root.dataset.theme=e.newValue;paint();}}}});
      document.addEventListener("keydown",function(e){{if(e.key==="/"&&document.activeElement!==q){{e.preventDefault();q.focus();}}if(e.key==="Escape"&&document.activeElement===q){{q.value="";apply();}}}});paint();apply();
    }})();
  </script>
</body>
</html>'''


def wrapper_html():
    template = (ROOT / "docs/academics/cybersecurity/cys401/extra-resources/final-exam-cheat-sheet/index.html").read_text(encoding="utf-8")
    for old, new in (
        ("Final Exam Cheat Sheet", "Glossary (All Chapters)"),
        ("final-exam-cheat-sheet", "glossary"),
        ("final-exam-cheat-sheet.html", "glossary.html"),
        ("ITEM_08 // STUDY MATERIAL", "REFERENCE // STUDY MATERIAL"),
    ):
        template = template.replace(old, new)
    template = template.replace('class="nav-link next disabled"', 'href="' + BASE + 'final-exam-cheat-sheet/" class="nav-link next"')
    template = template.replace(
        '<span class="nav-link next disabled">NEXT -&gt;</span>',
        '<a href="' + BASE + 'final-exam-cheat-sheet/" class="nav-link next">NEXT -&gt;</a>',
    )
    return template


def update_sidebar_source():
    path = ROOT / "scripts/academic-sidebar.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    key = BASE
    glossary_url = BASE + "glossary/"
    children = data["children"][key]
    if not any(item["url"] == glossary_url for item in children):
        entry = {
            "url": glossary_url,
            "attrs": 'data-en-text="Glossary (All Chapters)" data-ar-text="Ù…Ø¹Ø¬Ù… Ø¬Ù…ÙŠØ¹ Ø§Ù„ÙØµÙˆÙ„"',
            "label": "Glossary (All Chapters)",
        }
        insert_at = next((i + 1 for i, item in enumerate(children) if item["url"].endswith("final-exam-cheat-sheet/")), len(children))
        children.insert(insert_at, entry)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="")


def update_material_index():
    path = ROOT / "docs/academics/cybersecurity/cys401/extra-resources/index.html"
    text = path.read_text(encoding="utf-8")
    url = BASE + "glossary/"
    if url in text:
        return
    anchor = re.search(r'<a\s+href="' + re.escape(BASE + 'final-exam-cheat-sheet/') + r'"[\s\S]*?</a\s*>', text)
    if not anchor:
        raise ValueError("Could not find the CYS401 material-card insertion point")
    card = '''
              <a href="/academics/cybersecurity/cys401/extra-resources/glossary/" class="deck-preview">
                <span class="deck-thumb" style="background-image: linear-gradient(135deg, rgba(162, 30, 50, 0.92), rgba(54, 10, 21, 0.96)); display: grid; place-items: center; color: white; font: 700 38px 'JetBrains Mono', monospace" aria-hidden="true">A–Z</span>
                <span class="deck-kind">Reference</span><div class="deck-name">Glossary (All Chapters)</div>
              </a>'''
    text = text[:anchor.end()] + card + text[anchor.end():]
    path.write_text(text, encoding="utf-8", newline="")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    total = sum(len(ch["terms"]) for ch in CHAPTERS)
    duplicates = [(ch["label"], term) for ch in CHAPTERS for term, _ in ch["terms"] if sum(t.lower() == term.lower() for t, _ in ch["terms"]) > 1]
    if duplicates:
        raise ValueError(f"Duplicate terms found: {duplicates}")
    (OUT / "glossary.html").write_text(glossary_html(), encoding="utf-8", newline="")
    (OUT / "index.html").write_text(wrapper_html(), encoding="utf-8", newline="")
    update_sidebar_source()
    update_material_index()
    print(f"CYS401 glossary: {total} terms in {len(CHAPTERS)} chapters")


if __name__ == "__main__":
    main()
