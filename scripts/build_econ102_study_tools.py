#!/usr/bin/env python3
"""Build ECON102's searchable glossary and chapter listing vault from study notes."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "scripts/study_content/econ102"
BASE = ROOT / "docs/academics/business/econ102/extra-resources"
SE423 = ROOT / "docs/academics/software-engineering/se423/extra-resources/glossary/index.html"


def sections(text):
    return re.split(r"(?m)^\s*@([a-z]+)\s*$", text)


def parse_notes():
    chapters = []
    for path in sorted(NOTES.glob("*.md")):
        parts = sections(path.read_text(encoding="utf-8"))
        meta = {parts[i]: parts[i + 1].strip() for i in range(1, len(parts) - 1, 2)}
        head = meta.get("head", "")
        num_match = re.search(r"\d+", head)
        if not num_match:
            continue
        num = int(num_match.group())
        title = meta.get("title", path.stem)
        vocab = []
        for line in meta.get("vocab", "").splitlines():
            if "|" in line:
                term, definition = line.split("|", 1)
                term, definition = term.strip(), definition.strip()
                if term and definition:
                    vocab.append((term, definition))
        cheat = meta.get("cheat", "")
        lists = []
        current = None
        for line in cheat.splitlines():
            heading = re.match(r"^\s*###\s+(.+?)\s*$", line)
            bullet = re.match(r"^\s*[-*]\s+(.+?)\s*$", line)
            if heading:
                if current and len(current["items"]) > 1:
                    lists.append(current)
                current = {"t": heading.group(1), "items": [], "note": ""}
            elif bullet and current:
                current["items"].append(bullet.group(1).strip())
        if current and len(current["items"]) > 1:
            lists.append(current)
        chapters.append({"num": num, "id": path.stem, "title": title, "vocab": vocab, "lists": lists,
                         "sub": meta.get("tldr", "")})
    return chapters


def glossary_page(chapters):
    entries = []
    seen = set()
    for chapter in chapters:
        terms = []
        for term, definition in chapter["vocab"]:
            key = term.casefold()
            if key not in seen:
                seen.add(key)
                terms.append((term, definition))
        entries.append((chapter, terms))
    total = sum(len(terms) for _, terms in entries)
    toc = "".join(f'<a href="#{c["id"]}">Chapter {c["num"]}: {html.escape(c["title"])} <small>{len(ts)} terms</small></a>' for c, ts in entries)
    body = []
    for chapter, terms in entries:
        rows = "".join(f'<article class="term"><b>{html.escape(t)}</b><span>{html.escape(d)}</span></article>' for t, d in sorted(terms, key=lambda x: x[0].casefold()))
        body.append(f'<section id="{chapter["id"]}"><h2>Chapter {chapter["num"]} · {html.escape(chapter["title"])}</h2><div class="terms">{rows}</div></section>')
    return f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ECON102 Glossary</title>
<style>body{{margin:0;background:#f7f5f0;color:#20212a;font:16px/1.6 Inter,system-ui,sans-serif}}main{{max-width:1050px;margin:auto;padding:24px}}h1,h2{{font-family:Georgia,serif}}.bar{{position:sticky;top:0;background:#f7f5f0;padding:12px;border-bottom:1px solid #ddd;z-index:2}}input{{width:min(600px,80vw);padding:12px;border:1px solid #bbb;border-radius:8px;font:inherit}}nav{{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}}nav a{{background:white;border:1px solid #ddd;border-radius:8px;padding:6px 10px;color:#4f328d;text-decoration:none}}small{{color:#666}}section{{padding-top:18px;margin:30px 0;border-top:2px solid #6b3fd1;scroll-margin-top:80px}}.terms{{columns:2 340px;gap:30px}}.term{{break-inside:avoid;padding:8px 0;border-bottom:1px solid #ddd}}.term b,.term span{{display:block}}.term span{{color:#50515c}}.empty{{display:none}}</style>
<div class="bar"><input id="q" type="search" placeholder="Search {total} course terms…"><button onclick="print()">Print</button></div><main><h1>ECON102 Course Glossary</h1><p>{total} distinct vocabulary terms across {len(chapters)} chapter study guides. Definitions are drawn from the course notes.</p><nav>{toc}</nav>{''.join(body)}<p class="empty" id="empty">No matching terms.</p></main>
<script>let q=document.querySelector('#q'), terms=[...document.querySelectorAll('.term')];q.oninput=()=>{{let n=0;terms.forEach(e=>{{let ok=e.textContent.toLowerCase().includes(q.value.toLowerCase());e.hidden=!ok;n+=ok}});document.querySelectorAll('section').forEach(s=>s.hidden=!s.querySelector('.term:not([hidden])'));document.querySelector('#empty').style.display=n?'none':'block'}};</script></html>'''


def listing_page(chapters):
    payload = [{"n": c["num"], "title": c["title"], "slug": c["id"], "hue": (c["num"] * 29) % 360,
                "sub": c["sub"], "lists": [{"t": l["t"], "slide": 1, "items": l["items"], "note": "", "asked": False, "order": i}
                                                for i, l in enumerate(c["lists"], 1)]} for c in chapters]
    cards = []
    for c in payload:
        items = []
        for l in c["lists"]:
            lis = "".join(f'<li>{html.escape(x)}</li>' for x in l["items"])
            items.append(f'<article class="card"><h3>{html.escape(l["t"])}</h3><ol>{lis}</ol></article>')
        cards.append(f'<section><h2>Chapter {c["n"]} · {html.escape(c["title"])}</h2><p>{html.escape(c["sub"])}</p><div class="grid">{"".join(items)}</div></section>')
    count = sum(len(c["lists"]) for c in payload)
    return f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ECON102 Listing Vault</title><style>body{{margin:0;background:#f7f5f0;color:#20212a;font:16px/1.6 Inter,system-ui,sans-serif}}main{{max-width:1050px;margin:auto;padding:24px}}section{{padding-top:20px;margin:28px 0;border-top:2px solid #6b3fd1}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}}.card{{background:white;border:1px solid #ddd;border-radius:12px;padding:16px}}h1,h2,h3{{font-family:Georgia,serif}}li{{padding:3px 0}}</style><main><h1>ECON102 Listing Vault</h1><p>{count} chapter lists collected from the course study notes, grouped by chapter for quick review.</p>{''.join(cards)}</main></html>'''


def write_wrapper(slug, label, child):
    folder = BASE / slug
    folder.mkdir(parents=True, exist_ok=True)
    template = SE423.read_text(encoding="utf-8")
    template = template.replace("SE423", "ECON102").replace("Software Engineering", "Business")
    template = template.replace("/academics/software-engineering/se423/", "/academics/business/econ102/")
    template = template.replace("Glossary (All Chapters)", label)
    template = re.sub(r'<iframe(.*?)src=".*?"(.*?)></iframe>', rf'<iframe\1src="./{child}"\2></iframe>', template, count=1, flags=re.S)
    canonical = f"https://shoug-tech.com/academics/business/econ102/extra-resources/{slug}/"
    template = re.sub(r'<link\s+rel="canonical"\s+href="[^"]+"\s*/?>', f'<link rel="canonical" href="{canonical}" />', template, count=1, flags=re.S)
    template = re.sub(r'(<div class="breadcrumb">).*?(</div>)', r'\1<a class="breadcrumb-link" href="/academics/">Academics</a> / <a class="breadcrumb-link" href="/academics/business/">Business</a> / <a class="breadcrumb-link" href="/academics/business/econ102/">ECON102</a> / <a class="breadcrumb-link" href="/academics/business/econ102/extra-resources/">Study Material</a> / <span class="current">' + label + r'</span>\2', template, count=1, flags=re.S)
    (folder / "index.html").write_text(template, encoding="utf-8")


def main():
    chapters = parse_notes()
    gloss = BASE / "glossary"
    vault = BASE / "listing-vault"
    gloss.mkdir(parents=True, exist_ok=True)
    vault.mkdir(parents=True, exist_ok=True)
    (gloss / "glossary.html").write_text(glossary_page(chapters), encoding="utf-8")
    (vault / "listing-vault.html").write_text(listing_page(chapters), encoding="utf-8")
    write_wrapper("glossary", "ECON102 Glossary", "glossary.html")
    write_wrapper("listing-vault", "ECON102 Listing Vault", "listing-vault.html")
    print(f"Built glossary from {sum(len(c['vocab']) for c in chapters)} chapter terms and listing vault with {sum(len(c['lists']) for c in chapters)} lists across {len(chapters)} chapters")


if __name__ == "__main__":
    main()
