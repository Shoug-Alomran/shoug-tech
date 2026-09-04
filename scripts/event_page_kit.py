#!/usr/bin/env python3
"""Shared building blocks for the standalone event pages under /workshops/.

The site chrome (header, footer, theme and language runtime, light-mode rules) is
lifted at build time from an existing hand-written workshop page, so these pages
stay in sync with the rest of the site. Each event builder supplies its own
content, accent palette and page list; everything structural lives here.

Used by build_ai_programming_jam.py, build_psu_ctf_3.py and build_acm_psu_platform.py.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
SOURCE = DOCS / "workshops" / "psu-ctf" / "index.html"
SITE = "https://shoug-tech.com"


def slice_between(text: str, start_marker: str, end_marker: str, *, include: bool = True) -> str:
    start = text.index(start_marker)
    end = text.index(end_marker, start) + len(end_marker)
    return text[start:end] if include else text[start + len(start_marker):end - len(end_marker)]


def extract_chrome() -> dict[str, str]:
    html = SOURCE.read_text(encoding="utf-8")
    css = slice_between(html, "        .shoug-site-header {", "body.shoug-light-mode #glcanvas { opacity: 0.35 !important; }")
    header = slice_between(html, '    <header class="shoug-site-header">', "    </header>")
    footer = slice_between(html, '    <footer class="shoug-site-footer">', "    </footer>")
    # The theme + language runtime shared by every standalone page.
    runtime_start = html.index("    <script>\n        (function () {\n            function normalizeLabel")
    runtime_end = html.index("    </script>", runtime_start) + len("    </script>")
    runtime = html[runtime_start:runtime_end]
    return {"css": css, "header": header, "footer": footer, "runtime": runtime}



BASE_CSS = """
        /* Reset and layout primitives shared by every event theme. The visual
           language — palette, typography, components — lives in each event's own
           stylesheet, so the pages do not all look like the same page. */
        * { box-sizing: border-box; margin: 0; padding: 0; }

        html { scroll-behavior: smooth; scroll-padding-top: 92px; }

        body {
            overflow-x: hidden;
            -webkit-font-smoothing: antialiased;
        }

        main { padding-top: 68px; }

        .wrap { width: min(1280px, calc(100% - 48px)); margin: 0 auto; }

        img, svg { max-width: 100%; }

        a { color: inherit; }

        @media (prefers-reduced-motion: reduce) {
            html { scroll-behavior: auto; }
            *, *::before, *::after {
                animation-duration: 0.001ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.001ms !important;
            }
        }

        @media (max-width: 980px) {
            main { padding-top: 0; }
        }

        @media (max-width: 620px) {
            .wrap { width: calc(100% - 28px); }
        }
"""


HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="icon" type="image/png" sizes="256x256" href="/assets/shoug-favicon-v4.png">
    <link rel="shortcut icon" type="image/png" href="/assets/shoug-favicon-v4.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/shoug-apple-touch-icon-v4.png">
<script>if(localStorage.getItem('shoug-theme')==='light'){document.documentElement.style.background='#f6f4fb';document.documentElement.style.color='#16111f';}</script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>__TITLE__</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="">
    <link href="__FONTS__" rel="stylesheet">

    <style>
__PAGE_CSS__

        /* ── shared site chrome ─────────────────────────────── */
__CHROME_CSS__
    </style>
    <link rel="stylesheet" href="/styles/light-mode.css">

    <meta name="description" content="__DESCRIPTION__">
    <link rel="canonical" href="__CANONICAL__">
    <meta property="og:title" content="__TITLE__">
    <meta property="og:description" content="__DESCRIPTION__">
    <meta property="og:url" content="__CANONICAL__">
    <meta property="og:type" content="website">
    <meta property="og:image" content="https://shoug-tech.com/assets/og-banner.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="__TITLE__">
    <meta name="twitter:description" content="__DESCRIPTION__">
    <meta name="twitter:image" content="https://shoug-tech.com/assets/og-banner.png">
    <script type="application/ld+json">__JSONLD__</script>

      <link rel="alternate" hreflang="en" href="__CANONICAL__">
      <link rel="alternate" hreflang="ar" href="__CANONICAL__?lang=ar">
      <link rel="alternate" hreflang="x-default" href="__CANONICAL__">

    <link rel="stylesheet" href="/styles/mobile-fixes.css">
    <!-- Microsoft Clarity tracking code for https://shoug-tech.com/ -->
    <script type="text/javascript">
        (function(c,l,a,r,i,t,y){
            c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
            t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
            y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
        })(window, document, "clarity", "script", "xub0eqmvs9");
    </script>
    <link rel="stylesheet" href="/styles/a11y.css">

    <link rel="manifest" href="/site.webmanifest">
    <meta name="theme-color" content="#05070c">
</head>
<body>
<a class="shoug-skip-link" href="#main-content">Skip to content</a>
<script>if(localStorage.getItem('shoug-theme')==='light')document.body.classList.add('shoug-light-mode');</script>
"""

TAIL = """
__RUNTIME__
    <script src="/javascripts/arabic-localization.js" defer></script>
    <script src="/javascripts/mobile-navigation.js" defer></script>
<script src="/javascripts/register-sw.js" defer></script>
</body></html>
"""


@dataclass(frozen=True)
class Page:
    """One page of an event: its slug, tab label and the sections it carries."""

    slug: str          # "" for the hub, "rules/" for a sub-page
    filename: str      # directory name under the event root ("" for the hub)
    title: str
    description: str
    label: str = ""    # tab label in the sub-navigation; defaults to the heading
    eyebrow: str = ""
    heading: str = ""
    sections: tuple[str, ...] = ()


@dataclass
class Event:
    """Everything a single event's page set needs."""

    root: Path                 # docs/workshops/<event>/
    base: str                  # "/workshops/<event>/"
    css: str                   # this event's complete stylesheet
    pages: tuple[Page, ...]
    nav_label: str = "Event"
    about: dict | None = None  # schema.org Event data, attached to every page
    heading_html: str = '<span class="brace">&lt;</span>{h}<span class="brace">/&gt;</span>'
    fonts: str = (
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600"
        "&amp;family=JetBrains+Mono:wght@400;500;700;800"
        "&amp;family=Rajdhani:wght@500;600;700&amp;display=swap"
    )

    @property
    def canonical(self) -> str:
        return SITE + self.base


def subnav(event: Event, slug: str) -> str:
    links = []
    for page in event.pages:
        active = ' class="active"' if page.slug == slug else ""
        links.append(f'                <a href="{event.base}{page.slug}"{active}>{page.label or page.heading}</a>')
    return (
        f'            <nav class="subnav" aria-label="{event.nav_label} sections">\n'
        + "\n".join(links)
        + "\n            </nav>"
    )


def breadcrumb(event: Event, event_label: str, page_label: str | None) -> str:
    head = '            <div class="breadcrumb">\n                <a href="/workshops/">Workshops</a><span class="sep">/</span>'
    if page_label is None:
        return head + f"<span>{event_label}</span>\n            </div>"
    return (
        head
        + f'<a href="{event.base}">{event_label}</a><span class="sep">/</span><span>{page_label}</span>\n'
        + "            </div>"
    )


def pager(event: Event, slug: str) -> str:
    order = [page.slug for page in event.pages]
    labels = {page.slug: (page.label or page.heading) for page in event.pages}
    index = order.index(slug)
    previous = order[index - 1] if index > 0 else None
    following = order[index + 1] if index < len(order) - 1 else None
    left = (
        f'<a href="{event.base}{previous}">[ &lt;- {labels[previous]} ]</a>'
        if previous is not None
        else '<span class="spacer"></span>'
    )
    right = (
        f'<a href="{event.base}{following}">[ {labels[following]} -&gt; ]</a>'
        if following is not None
        else f'<a href="{event.base}">[ Back to overview ]</a>'
    )
    return f'            <div class="pager">{left}<span class="spacer"></span>{right}</div>'


SUBPAGE_SHELL = """
    <div class="grid-bg" aria-hidden="true"></div>

__HEADER__

    <main id="main-content" tabindex="-1">
        <div class="wrap">
__BREADCRUMB__
__SUBNAV__

            <div class="page-head">
                <div class="eyebrow">__EYEBROW__</div>
                <h1>__HEADING__</h1>
            </div>
__CONTENT__
__PAGER__
        </div>
    </main>

__FOOTER__
"""


def json_ld(url: str, name: str, description: str, about: dict | None) -> str:
    payload = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "url": url,
        "name": name,
        "description": description,
        "isPartOf": {"@type": "WebSite", "name": "Shoug's Digital Garden", "url": "https://shoug-tech.com/"},
    }
    if about:
        payload["about"] = about
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def render(
    event: Event,
    chrome: dict[str, str],
    body: str,
    *,
    url: str,
    title: str,
    description: str,
) -> str:
    head = (
        HEAD.replace("__PAGE_CSS__", BASE_CSS + event.css)
        .replace("__FONTS__", event.fonts)
        .replace("__CHROME_CSS__", chrome["css"])
        .replace("__JSONLD__", json_ld(url, title, description, event.about))
        .replace("__TITLE__", title)
        .replace("__DESCRIPTION__", description)
        .replace("__CANONICAL__", url)
    )
    body = body.replace("__HEADER__", chrome["header"]).replace("__FOOTER__", chrome["footer"])
    return head + body + TAIL.replace("__RUNTIME__", chrome["runtime"])


def split_sections(body: str) -> dict[str, str]:
    """Split a single-page body into its `<section class="block" id="...">` fragments.

    The first chunk (everything before the first section) is returned as "intro";
    the last section keeps only its own markup, with the trailing wrap/CTA dropped.
    """
    chunks = re.split(r'\n(?=            <section class="block" id=")', body)
    parts = {"intro": chunks[0]}
    for chunk in chunks[1:]:
        parts[re.search(r'id="([a-z-]+)"', chunk).group(1)] = chunk
    last = list(parts)[-1]
    marker = '\n        </div>\n\n        <div class="wrap">'
    if marker in parts[last]:
        parts[last] = parts[last][: parts[last].index(marker)]
    return parts


def build_subpage(event: Event, chrome: dict[str, str], parts: dict[str, str], page: Page, event_label: str) -> str:
    fragments = [parts[name] for name in page.sections]
    # The first section's "// label" line would repeat the page heading directly above it.
    fragments[0] = re.sub(r'\n *<div class="(?:sect-label|sec-head)">[^<]*</div>', "", fragments[0], count=1)
    body = (
        SUBPAGE_SHELL.replace("__BREADCRUMB__", breadcrumb(event, event_label, page.heading or page.label))
        .replace("__SUBNAV__", subnav(event, page.slug))
        .replace("__EYEBROW__", page.eyebrow)
        .replace("__HEADING__", event.heading_html.format(h=page.heading or page.label))
        .replace("__CONTENT__", "\n".join(fragments))
        .replace("__PAGER__", pager(event, page.slug))
    )
    return render(event, chrome, body, url=event.canonical + page.slug, title=page.title, description=page.description)


def write(files: list[tuple[Path, str]]) -> int:
    for path, html in files:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html, encoding="utf-8")
        print(f"wrote {path.relative_to(DOCS.parent)} ({path.stat().st_size:,} bytes)")
    return 0
