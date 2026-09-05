#!/usr/bin/env python3
"""Build the SE322 Listing Vault: one standalone listing page per chapter.

Mirrors the ETHCS303 listing pages (same stylesheet and search/theme behaviour),
but split so every chapter gets its own page, its own wrapper index.html, and a
hub that lists them all.

    python3 scripts/build_se322_listing_vault.py
"""

from pathlib import Path
import html
import json
import re

from se322_listing_content import CHAPTERS

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/academics/software-engineering/se322"
VAULT = BASE / "extra-resources/listing-vault"

STYLE_SOURCE = ROOT / "docs/academics/other-courses/ethcs303/extra-resources/final-exam-listing/final-exam-listing.html"
WRAPPER_SOURCE = BASE / "extra-resources/mindmaps/08-architecture-evaluation/index.html"
HUB_SOURCE = BASE / "extra-resources/mindmaps/index.html"

ROUTE = "/academics/software-engineering/se322/extra-resources/listing-vault/"
SITE = "https://shoug-tech.com"


# --------------------------------------------------------------------------- #
# shared assets lifted from the ETHCS303 listing page
# --------------------------------------------------------------------------- #

def listing_style() -> str:
    text = STYLE_SOURCE.read_text(encoding="utf-8")
    return re.search(r"<style>.*?</style>", text, re.S).group(0)


THEME_AND_SEARCH_JS = """
        // ---------- theme ----------
        const root = document.documentElement;
        const lightBtn = document.getElementById('lightBtn');
        const darkBtn = document.getElementById('darkBtn');

        function setTheme(t) {
            root.setAttribute('data-theme', t);
            lightBtn.classList.toggle('active', t === 'light');
            darkBtn.classList.toggle('active', t === 'dark');
            try { localStorage.setItem('listingVaultTheme', t); } catch (e) { }
        }
        let saved = 'dark';
        try {
            saved = localStorage.getItem('listingVaultTheme')
                || (localStorage.getItem('shoug-theme') === 'light' ? 'light' : null)
                || (window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
        } catch (e) { }
        setTheme(saved);
        lightBtn.addEventListener('click', () => setTheme('light'));
        darkBtn.addEventListener('click', () => setTheme('dark'));

        // ---------- search ----------
        const input = document.getElementById('searchInput');
        const countEl = document.getElementById('searchCount');
        const cards = Array.from(document.querySelectorAll('.card'));
        const chapters = Array.from(document.querySelectorAll('.chapter'));

        function clearMarks(el) {
            el.querySelectorAll('mark').forEach(m => {
                m.replaceWith(document.createTextNode(m.textContent));
            });
        }

        function highlight(el, term) {
            const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null);
            const nodes = [];
            let n;
            while (n = walker.nextNode()) nodes.push(n);
            nodes.forEach(node => {
                const text = node.textContent;
                const idx = text.toLowerCase().indexOf(term);
                if (idx === -1) return;
                const before = text.slice(0, idx);
                const match = text.slice(idx, idx + term.length);
                const after = text.slice(idx + term.length);
                const frag = document.createDocumentFragment();
                frag.appendChild(document.createTextNode(before));
                const markEl = document.createElement('mark');
                markEl.textContent = match;
                frag.appendChild(markEl);
                frag.appendChild(document.createTextNode(after));
                node.parentNode.replaceChild(frag, node);
            });
        }

        function runSearch() {
            const term = input.value.trim().toLowerCase();
            let visibleCards = 0;

            cards.forEach(card => {
                clearMarks(card);
                if (!term) {
                    card.classList.remove('hidden');
                    return;
                }
                const text = card.textContent.toLowerCase();
                if (text.includes(term)) {
                    card.classList.remove('hidden');
                    highlight(card, term);
                    visibleCards++;
                } else {
                    card.classList.add('hidden');
                }
            });

            chapters.forEach(ch => {
                const anyVisible = Array.from(ch.querySelectorAll('.card')).some(c => !c.classList.contains('hidden'));
                ch.classList.toggle('hidden', term && !anyVisible);
            });

            countEl.textContent = term ? (visibleCards + ' match' + (visibleCards === 1 ? '' : 'es')) : '';
        }
        input.addEventListener('input', runSearch);

        // ---------- stats ----------
        let totalItems = 0;
        document.querySelectorAll('.card ol, .card ul').forEach(list => {
            totalItems += list.querySelectorAll(':scope > li').length;
        });
        document.querySelectorAll('.card .examtable tr').forEach(row => {
            if (!row.querySelector('th')) totalItems += 1;
        });
        document.getElementById('listCountStat').textContent = document.querySelectorAll('.card h3').length;
        document.getElementById('itemCountStat').textContent = totalItems;
"""


# --------------------------------------------------------------------------- #
# standalone listing pages
# --------------------------------------------------------------------------- #

def card_html(card: dict) -> str:
    classes = "card full" if card.get("full") else "card"
    badge = f'<span class="count-badge">{card["badge"]}</span>' if card.get("badge") else ""
    parts = [f'<div class="{classes}">', f'<h3>{card["title"]} {badge}</h3>']
    if card.get("note"):
        parts.append(f'<p class="desc">{card["note"]}</p>')

    if card.get("table"):
        cols = "".join(f"<th>{c}</th>" for c in card["table"]["cols"])
        rows = "".join(
            "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
            for row in card["table"]["rows"]
        )
        parts.append(f'<table class="examtable"><tr>{cols}</tr>{rows}</table>')
    elif card.get("groups"):
        subs = []
        for heading, items in card["groups"]:
            lis = "".join(f"<li>{item}</li>" for item in items)
            subs.append(f'<div class="sub"><h4>{heading}</h4><ul>{lis}</ul></div>')
        parts.append('<div class="subgrid">' + "".join(subs) + "</div>")
    else:
        lis = "".join(f"<li>{item}</li>" for item in card["items"])
        parts.append(f"<ol>{lis}</ol>")

    parts.append("</div>")
    return "".join(parts)


def chapnav_html(current_folder: str) -> str:
    links = [
        f'<a href="{ROUTE}" target="_top"><span class="n">00</span>Vault Index</a>'
    ]
    for folder, label, _slug, title, _blurb, _cards in CHAPTERS:
        short = short_title(title)
        active = ' class="active"' if folder == current_folder else ""
        links.append(
            f'<a href="{ROUTE}{folder}/" target="_top"{active}><span class="n">{label}</span>{html.escape(short)}</a>'
        )
    return "\n            ".join(links)


def short_title(title: str) -> str:
    return {
        "Introduction to Software Design and Architecture": "Introduction",
        "Software Architecture": "Software Architecture",
        "Quality Attributes": "Quality Attributes",
        "Architecture Patterns": "Architecture Patterns",
        "Principles of Detailed Design": "Detailed Design",
        "Creational Design Patterns": "Creational",
        "Structural Design Patterns": "Structural",
        "Behavioral Design Patterns": "Behavioral",
        "Architecture Evaluation": "Evaluation",
        "Architecture Documentation": "Documentation",
    }[title]


def listing_page(folder: str, label: str, slug: str, title: str, blurb: str, cards: list) -> str:
    canonical = f"{SITE}{ROUTE}{folder}/{slug}-listing.html"
    page_title = f"SE322 — Chapter {label} Listing: {title}"
    description = (
        f"Every memorizable SE322 list for Chapter {int(label)}: {title}. "
        "Searchable card vault from Shoug's Digital Garden."
    )
    esc_desc = html.escape(description, quote=True)
    esc_title = html.escape(page_title, quote=True)
    structured = json.dumps({
        "@context": "https://schema.org", "@type": "WebPage", "url": canonical,
        "name": page_title, "description": description,
        "isPartOf": {"@type": "WebSite", "name": "Shoug's Digital Garden", "url": f"{SITE}/"},
    })
    cards_html = "\n                ".join(card_html(card) for card in cards)

    return f"""<!DOCTYPE html>
<html lang="en">

<head>
    <link rel="icon" type="image/png" sizes="256x256" href="/assets/shoug-favicon-v4.png">
    <link rel="shortcut icon" type="image/png" href="/assets/shoug-favicon-v4.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/shoug-apple-touch-icon-v4.png">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{esc_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link
        href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap"
        rel="stylesheet">
    {listing_style()}
    <style>
        .grid {{
            align-items: start;
        }}

        .chapnav a.active {{
            border-color: var(--accent);
            color: var(--accent-strong);
            background: color-mix(in srgb, var(--accent) 10%, transparent);
        }}

        .card code {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 12.5px;
            background: var(--bg-alt);
            border-radius: 5px;
            padding: 1px 5px;
        }}

        .card .examtable td b {{
            color: var(--accent-strong);
        }}
    </style>

    <meta name="description" content="{esc_desc}">
    <link rel="canonical" href="{canonical}">
    <meta property="og:title" content="{esc_title}">
    <meta property="og:description" content="{esc_desc}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:type" content="website">
    <meta property="og:image" content="{SITE}/assets/og-banner.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{esc_title}">
    <meta name="twitter:description" content="{esc_desc}">
    <meta name="twitter:image" content="{SITE}/assets/og-banner.png">
    <script type="application/ld+json">{structured}</script>

    <link rel="alternate" hreflang="en" href="{canonical}">
    <link rel="alternate" hreflang="ar" href="{canonical}?lang=ar">
    <link rel="alternate" hreflang="x-default" href="{canonical}">
    <!-- Microsoft Clarity tracking code for https://shoug-tech.com/ -->
    <script type="text/javascript">
        (function(c,l,a,r,i,t,y){{
            c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
            t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
            y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
        }})(window, document, "clarity", "script", "xub0eqmvs9");
    </script>
    <link rel="stylesheet" href="/styles/a11y.css">
</head>

<body>

    <div class="topbar">
        <div class="topbar-inner">
            <div class="brand">
                <span class="mark">Listing Vault</span>
                <span class="sub">SE322 &middot; chapter {label} &middot; {html.escape(title)}</span>
            </div>
            <div class="search-wrap">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="7" />
                    <line x1="21" y1="21" x2="16.65" y2="16.65" />
                </svg>
                <input id="searchInput" type="text" placeholder="Search any list, term, or item…">
            </div>
            <span class="search-count" id="searchCount"></span>
            <div class="theme-toggle" role="group" aria-label="Theme toggle">
                <button id="lightBtn" title="Light mode" aria-label="Light mode">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="4" />
                        <path
                            d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" />
                    </svg>
                </button>
                <button id="darkBtn" title="Dark mode" aria-label="Dark mode">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z" />
                    </svg>
                </button>
            </div>
        </div>
        <nav class="chapnav">
            {chapnav_html(folder)}
        </nav>
    </div>

    <div class="wrap">

        <div class="hero">
            <h1>Chapter {label} — {html.escape(title)}</h1>
            <p>{html.escape(blurb)}</p>
            <div class="stat-row">
                <div class="stat"><b>{label}</b><span>chapter</span></div>
                <div class="stat"><b id="listCountStat">—</b><span>lists</span></div>
                <div class="stat"><b id="itemCountStat">—</b><span>total items</span></div>
            </div>
        </div>

        <div class="banner">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2l9 4.5v6c0 5-3.8 8.5-9 9.5-5.2-1-9-4.5-9-9.5v-6L12 2z" />
                <path d="M9 12l2 2 4-4" />
            </svg>
            <span>Every enumerable list from this chapter, one card each. Search filters the cards live;
                the chips above jump to any other chapter in the vault.</span>
        </div>

        <section class="chapter" id="ch{label}">
            <div class="chapter-head">
                <span class="num">{label}</span>
                <h2>{html.escape(title)}</h2>
                <span class="tag">{len(cards)} lists</span>
            </div>
            <div class="grid">
                {cards_html}
            </div>
        </section>

    </div>

    <footer>
        <span class="name">Shoug Alomran</span>
        <span class="meta">SE322 &middot; Listing Vault &middot; Chapter {label}</span>
    </footer>

    <script>{THEME_AND_SEARCH_JS}    </script>

</body>

</html>
"""


# --------------------------------------------------------------------------- #
# wrappers + hub
# --------------------------------------------------------------------------- #

def wrapper_page(index: int, folder: str, label: str, slug: str, title: str) -> str:
    text = WRAPPER_SOURCE.read_text(encoding="utf-8")
    canonical = f"{SITE}{ROUTE}{folder}/"
    page_name = f"SE322 · Chapter {label} Listing Vault — {title}"
    page_desc = f"Every memorizable SE322 Chapter {label} {title} list on one searchable page from Shoug's Digital Garden."
    raw = f"./{slug}-listing.html"

    text = re.sub(r"<title>.*?</title>", f"<title>{html.escape(page_name)}</title>", text, count=1, flags=re.S)
    text = re.sub(r'<meta name="description"\s+content="[^"]*">',
                  f'<meta name="description" content="{html.escape(page_desc, quote=True)}">', text, count=1)
    text = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="{canonical}">', text, count=1)
    text = re.sub(r'(<meta property="og:title" content=")[^"]*(">)',
                  lambda m: m.group(1) + html.escape(page_name, quote=True) + m.group(2), text)
    text = re.sub(r'(<meta property="og:description"\s+content=")[^"]*(">)',
                  lambda m: m.group(1) + html.escape(page_desc, quote=True) + m.group(2), text)
    text = re.sub(r'(<meta property="og:url"\s+content=")[^"]*(">)',
                  lambda m: m.group(1) + canonical + m.group(2), text)
    text = re.sub(r'(<meta name="twitter:title" content=")[^"]*(">)',
                  lambda m: m.group(1) + html.escape(page_name, quote=True) + m.group(2), text)
    text = re.sub(r'(<meta name="twitter:description"\s+content=")[^"]*(">)',
                  lambda m: m.group(1) + html.escape(page_desc, quote=True) + m.group(2), text)
    structured = '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "WebPage", "url": canonical,
        "name": page_name, "description": page_desc,
        "isPartOf": {"@type": "WebSite", "name": "Shoug's Digital Garden", "url": f"{SITE}/"},
    }) + "</script>"
    text = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda _m: structured, text, count=1, flags=re.S)
    text = re.sub(r'(<link rel="alternate" hreflang="(?:en|x-default)"\s*\n?\s*href=")[^"]+',
                  lambda m: m.group(1) + canonical, text)
    text = re.sub(r'(<link rel="alternate" hreflang="ar"\s*\n?\s*href=")[^"]+',
                  lambda m: m.group(1) + canonical.replace(".com/", ".com/ar/"), text)

    # breadcrumb, header, buttons, nav strip, iframe
    text = text.replace(
        '<a class="breadcrumb-link" href="/academics/software-engineering/se322/extra-resources/mindmaps/">Mindmaps</a> / <span class="current">Architecture Evaluation</span>',
        f'<a class="breadcrumb-link" href="{ROUTE}">Listing Vault</a> / <span class="current">{html.escape(title)}</span>',
    )
    text = text.replace('<div class="ch-label">ITEM_08 // MINDMAPS</div>',
                        f'<div class="ch-label">ITEM_{label} // LISTING VAULT</div>')
    text = re.sub(r'<h1 class="ch-title">.*?</h1>', f'<h1 class="ch-title">{html.escape(title)}</h1>', text, count=1, flags=re.S)
    text = re.sub(r'(<a class="btn btn-primary" href=")[^"]+', lambda m: m.group(1) + raw, text, count=1)
    text = re.sub(r'(<a class="btn btn-secondary" href=")[^"]+', lambda m: m.group(1) + ROUTE, text, count=1)

    previous_route = ROUTE if index == 1 else f"{ROUTE}{CHAPTERS[index - 2][0]}/"
    next_route = ROUTE if index == len(CHAPTERS) else f"{ROUTE}{CHAPTERS[index][0]}/"
    text = re.sub(r'<div class="nav-strip">.*?</div>',
                  f'<div class="nav-strip"><a href="{previous_route}" class="nav-link prev">&lt;- PREVIOUS</a>'
                  f'<a href="{next_route}" class="nav-link next">NEXT -&gt;</a></div>',
                  text, count=1, flags=re.S)
    text = re.sub(r'<iframe class="embed-frame".*?</iframe>',
                  f'<iframe class="embed-frame" src="{raw}" title="{html.escape(title)} listing vault" loading="lazy"></iframe>',
                  text, count=1, flags=re.S)

    return re.sub(r"[ \t]+\n", "\n", text)


def hub_rows() -> str:
    rows = ['<div class="dir-header"><span>SEQ</span><span>DESCRIPTOR</span><span>SYS_STATE</span><span></span></div>']
    for folder, label, _slug, title, _blurb, _cards in CHAPTERS:
        rows.append(
            f'<a class="dir-row" href="{ROUTE}{folder}/">'
            f'<div class="dir-num">{int(label)}</div>'
            f'<div class="dir-title">Chapter {int(label)}: {html.escape(title)}</div>'
            f'<div class="dir-status"><span class="status-tag available">AVAILABLE</span></div>'
            f'<div class="dir-arrow">-&gt;</div></a>'
        )
    return '<div class="directory-container">' + "".join(rows) + "</div>"


def hub_page() -> str:
    text = HUB_SOURCE.read_text(encoding="utf-8")
    canonical = f"{SITE}{ROUTE}"
    page_name = "SHOUG.TECH | SE322 Listing Vault"
    page_desc = ("Every memorizable SE322 list, one page per chapter: definitions, tactics, "
                 "principles and pattern families from Shoug's Digital Garden.")

    text = re.sub(r"<title>.*?</title>", f"<title>{html.escape(page_name)}</title>", text, count=1, flags=re.S)
    text = re.sub(r'<meta name="description"\s+content="[^"]*">',
                  f'<meta name="description" content="{html.escape(page_desc, quote=True)}">', text, count=1)
    text = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="{canonical}">', text, count=1)
    text = re.sub(r'(<meta property="og:title" content=")[^"]*(">)',
                  lambda m: m.group(1) + html.escape(page_name, quote=True) + m.group(2), text)
    text = re.sub(r'(<meta property="og:description"\s+content=")[^"]*(">)',
                  lambda m: m.group(1) + html.escape(page_desc, quote=True) + m.group(2), text)
    text = re.sub(r'(<meta property="og:url"\s+content=")[^"]*(">)',
                  lambda m: m.group(1) + canonical + m.group(2), text)
    text = re.sub(r'(<meta name="twitter:title" content=")[^"]*(">)',
                  lambda m: m.group(1) + html.escape(page_name, quote=True) + m.group(2), text)
    text = re.sub(r'(<meta name="twitter:description"\s+content=")[^"]*(">)',
                  lambda m: m.group(1) + html.escape(page_desc, quote=True) + m.group(2), text)
    structured = '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "WebPage", "url": canonical,
        "name": page_name, "description": page_desc,
        "isPartOf": {"@type": "WebSite", "name": "Shoug's Digital Garden", "url": f"{SITE}/"},
    }) + "</script>"
    text = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda _m: structured, text, count=1, flags=re.S)
    text = re.sub(r'(<link rel="alternate" hreflang="(?:en|x-default)"\s*\n?\s*href=")[^"]+',
                  lambda m: m.group(1) + canonical, text)
    text = re.sub(r'(<link rel="alternate" hreflang="ar"\s*\n?\s*href=")[^"]+',
                  lambda m: m.group(1) + canonical.replace(".com/", ".com/ar/"), text)

    text = text.replace(
        '<span class="current" data-en-text="Mindmaps" data-ar-text="الخرائط الذهنية">Mindmaps</span>',
        '<span class="current" data-en-text="Listing Vault" data-ar-text="خزنة القوائم">Listing Vault</span>',
    )
    text = re.sub(r'<div class="type-label"[^>]*>.*?</div>',
                  '<div class="type-label" data-en-text="LISTING VAULT" data-ar-text="خزنة القوائم">LISTING VAULT</div>',
                  text, count=1, flags=re.S)
    text = re.sub(r'<div class="directory-container">.*?</div>\n', hub_rows() + "\n", text, count=1, flags=re.S)

    return re.sub(r"[ \t]+\n", "\n", text)


def add_hub_row_to_study_material() -> None:
    """Link the vault from the SE322 Study Material folder listing."""
    path = BASE / "extra-resources/index.html"
    text = path.read_text(encoding="utf-8")
    if "listing-vault/" in text:
        return
    row = (
        f'<a class="dir-row" href="{ROUTE}">'
        '<div class="dir-num">04</div>'
        '<div class="dir-title"><svg class="dir-folder-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="square" stroke-linejoin="square" aria-hidden="true">'
        '<path d="M3 7a1 1 0 0 1 1-1h5l2 2h9a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V7z"/></svg>'
        '<span class="dir-title-text">Listing Vault</span></div>'
        '<div class="dir-status"><span class="status-tag available">AVAILABLE</span></div>'
        '<div class="dir-arrow">-&gt;</div></a>'
    )
    marker = '<div class="dir-arrow">-&gt;</div></a></div>'
    assert text.count(marker) == 1, "study-material directory container not found (or ambiguous)"
    text = text.replace(marker, '<div class="dir-arrow">-&gt;</div></a>' + row + "</div>", 1)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    VAULT.mkdir(parents=True, exist_ok=True)
    for index, (folder, label, slug, title, blurb, cards) in enumerate(CHAPTERS, 1):
        directory = VAULT / folder
        directory.mkdir(parents=True, exist_ok=True)
        (directory / f"{slug}-listing.html").write_text(
            listing_page(folder, label, slug, title, blurb, cards), encoding="utf-8")
        (directory / "index.html").write_text(
            wrapper_page(index, folder, label, slug, title), encoding="utf-8")
        print(f"  wrote {folder}")
    (VAULT / "index.html").write_text(hub_page(), encoding="utf-8")
    add_hub_row_to_study_material()
    print(f"  wrote hub + study-material row ({len(CHAPTERS)} chapters)")
    print("  now run: python3 scripts/build_academic_sidebar.py  (stamps the SYSTEM_DIRECTORY tree)")


if __name__ == "__main__":
    main()
