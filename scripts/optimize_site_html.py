#!/usr/bin/env python3
"""Patch generated HTML for Lighthouse- and crawler-friendly static output."""

from __future__ import annotations

import html as html_lib
import re
import sys
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
if not SITE.is_dir() and (ROOT / "docs").is_dir():
    SITE = ROOT / "docs"
SITE_URL = "https://shoug-tech.com/"
SITE_NAME = "Shoug's Digital Garden"
SITE_DESCRIPTION = (
    "Structured course notes, academic engineering projects, and technical "
    "documentation across software development, cybersecurity, and computer science."
)
SEO_IMAGE = f"{SITE_URL}logo.png"


LOGO_SIZE = 'width="1022" height="385"'
HEADER_LOGO_SIZE = 'width="255" height="96"'
FAVICON_SIZE = 'width="128" height="121"'
TWEMOJI_SIZE = 'width="20" height="20" loading="lazy" decoding="async"'
STANDALONE_SITEMAP = "standalone-sitemap.xml"
SITEMAP = "sitemap.xml"
BAD_DESCRIPTION_FRAGMENTS = (
    "SYSTEM_DIRECTORY",
    "ACADEMICS/",
    "SLIDE BREAKDOWNS",
    "STUDY MATERIAL",
    "Exams",
)


def escape_attr(value: str) -> str:
    return html_lib.escape(value, quote=True)


def add_attr_once(tag: str, attr: str, value: str | None = None) -> str:
    name = attr.split("=", 1)[0]
    if re.search(rf"\s{name}(?:=|\s|>)", tag):
        return tag
    insertion = f" {attr}" if value is None else f' {attr}="{value}"'
    if tag.endswith("/>"):
        return tag[:-2].rstrip() + insertion + ">"
    return tag[:-1] + insertion + ">"


def clean_text(value: str) -> str:
    value = html_lib.unescape(value)
    value = re.sub(r"<script\b.*?</script>", " ", value, flags=re.IGNORECASE | re.DOTALL)
    value = re.sub(r"<style\b.*?</style>", " ", value, flags=re.IGNORECASE | re.DOTALL)
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip(" \t\n\r-")


def trim_description(value: str, limit: int = 155) -> str:
    value = clean_text(value)
    if len(value) <= limit:
        return value
    return value[: limit + 1].rsplit(" ", 1)[0].rstrip(".,;: -") + "."


def is_bad_description(value: str | None) -> bool:
    if not value:
        return True
    return any(fragment in value for fragment in BAD_DESCRIPTION_FRAGMENTS)


def tag_content(document: str, pattern: str) -> str | None:
    match = re.search(pattern, document, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return None
    value = clean_text(match.group(1))
    return value or None


def page_title(document: str, path: Path) -> str:
    title = tag_content(document, r"<title[^>]*>(.*?)</title>")
    if title:
        return title

    heading = tag_content(document, r"<h1[^>]*>(.*?)</h1>")
    if heading:
        return heading

    label = path.stem.replace("-", " ").replace("_", " ")
    return re.sub(r"\s+", " ", label).strip().title()


def page_description(document: str, title: str) -> str:
    existing = tag_content(
        document,
        r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
    )
    if existing:
        existing = trim_description(existing)
        if not is_bad_description(existing):
            return existing

    first_paragraph = tag_content(document, r"<p[^>]*>(.*?)</p>")
    if first_paragraph:
        candidate = trim_description(first_paragraph)
        nav_markers = (
            "SYSTEM_DIRECTORY",
            "ACADEMICS/",
            "SLIDE BREAKDOWNS",
            "STUDY MATERIAL",
            "Exams",
        )
        if len(candidate) >= 45 and not any(marker in candidate for marker in nav_markers):
            return candidate

    return trim_description(f"{title} study material from {SITE_NAME}.")


def canonical_url(path: Path) -> str:
    rel = path.relative_to(SITE).as_posix()
    if rel.endswith("/index.html"):
        rel = rel[: -len("index.html")]
    return SITE_URL + quote(rel, safe="/:.-_%")


def insert_before_head_close(document: str, snippet: str) -> str:
    return re.sub(r"</head\s*>", snippet + "\n</head>", document, count=1, flags=re.IGNORECASE)


def ensure_meta(document: str, path: Path) -> str:
    title = page_title(document, path)
    description = page_description(document, title)
    url = canonical_url(path)

    additions: list[str] = []
    description_pattern = r'(<meta\s+name=["\']description["\']\s+content=["\'])(.*?)(["\'][^>]*>)'
    description_match = re.search(description_pattern, document, flags=re.IGNORECASE | re.DOTALL)
    if description_match and is_bad_description(clean_text(description_match.group(2))):
        document = re.sub(
            description_pattern,
            lambda match: f"{match.group(1)}{escape_attr(description)}{match.group(3)}",
            document,
            count=1,
            flags=re.IGNORECASE | re.DOTALL,
        )
    elif not description_match:
        additions.append(f'    <meta name="description" content="{escape_attr(description)}">')
    if not re.search(r'<link\s+rel=["\']canonical["\']', document, flags=re.IGNORECASE):
        additions.append(f'    <link rel="canonical" href="{escape_attr(url)}">')

    og_tags = {
        "og:title": title,
        "og:description": description,
        "og:url": url,
        "og:type": "article" if "/Academics/" in path.as_posix() else "website",
        "og:image": SEO_IMAGE,
    }
    for name, value in og_tags.items():
        pattern = rf'(<meta\s+property=["\']{re.escape(name)}["\']\s+content=["\'])(.*?)(["\'][^>]*>)'
        match = re.search(pattern, document, flags=re.IGNORECASE | re.DOTALL)
        if name == "og:description" and match and is_bad_description(clean_text(match.group(2))):
            document = re.sub(
                pattern,
                lambda item: f"{item.group(1)}{escape_attr(value)}{item.group(3)}",
                document,
                count=1,
                flags=re.IGNORECASE | re.DOTALL,
            )
        elif not match:
            additions.append(f'    <meta property="{name}" content="{escape_attr(value)}">')

    twitter_tags = {
        "twitter:card": "summary_large_image",
        "twitter:title": title,
        "twitter:description": description,
        "twitter:image": SEO_IMAGE,
    }
    for name, value in twitter_tags.items():
        pattern = rf'(<meta\s+name=["\']{re.escape(name)}["\']\s+content=["\'])(.*?)(["\'][^>]*>)'
        match = re.search(pattern, document, flags=re.IGNORECASE | re.DOTALL)
        if name == "twitter:description" and match and is_bad_description(clean_text(match.group(2))):
            document = re.sub(
                pattern,
                lambda item: f"{item.group(1)}{escape_attr(value)}{item.group(3)}",
                document,
                count=1,
                flags=re.IGNORECASE | re.DOTALL,
            )
        elif not match:
            additions.append(f'    <meta name="{name}" content="{escape_attr(value)}">')

    if 'application/ld+json' not in document:
        additions.append(
            '    <script type="application/ld+json">'
            '{"@context":"https://schema.org","@type":"WebPage",'
            f'"url":"{escape_attr(url)}","name":"{escape_attr(title)}",'
            f'"description":"{escape_attr(description)}",'
            f'"isPartOf":{{"@type":"WebSite","name":"{SITE_NAME}","url":"{SITE_URL}"}}'
            "}</script>"
        )
    else:
        document = re.sub(
            r'("description"\s*:\s*")(.*?)(")',
            lambda match: (
                f'{match.group(1)}{escape_attr(description)}{match.group(3)}'
                if is_bad_description(clean_text(match.group(2)))
                else match.group(0)
            ),
            document,
            count=1,
            flags=re.IGNORECASE | re.DOTALL,
        )

    if not additions:
        return document
    return insert_before_head_close(document, "\n" + "\n".join(additions))


def optimize_images(html: str) -> str:
    def patch_img(match: re.Match[str]) -> str:
        tag = match.group(0)

        if "logo-header.png" in tag:
            tag = add_attr_once(tag, HEADER_LOGO_SIZE)
            tag = add_attr_once(tag, "decoding", "async")
            tag = add_attr_once(tag, "fetchpriority", "high")
            return tag

        if "logo.png" in tag:
            tag = add_attr_once(tag, LOGO_SIZE)
            tag = add_attr_once(tag, "decoding", "async")
            tag = add_attr_once(tag, "fetchpriority", "high")
            return tag

        if "google.png" in tag:
            tag = add_attr_once(tag, FAVICON_SIZE)
            tag = add_attr_once(tag, "decoding", "async")
            return tag

        if "twemoji" in tag:
            for part in TWEMOJI_SIZE.split():
                name, value = part.split("=", 1)
                tag = add_attr_once(tag, name, value.strip('"'))
            return tag

        tag = add_attr_once(tag, "loading", "lazy")
        tag = add_attr_once(tag, "decoding", "async")
        return tag

    return re.sub(r"<img\b[^>]*>", patch_img, html)


def page_variants(path: Path) -> tuple[str, str]:
    rel = path.relative_to(SITE).as_posix()
    is_ar = rel.startswith("ar/")

    if rel.endswith("index.html"):
        route = rel[: -len("index.html")]
    else:
        route = rel

    if is_ar:
        ar_route = route
        en_route = route[3:]
    else:
        en_route = route
        ar_route = f"ar/{route}"

    return en_route, ar_route


def add_alternates(html: str, path: Path) -> str:
    if 'rel="alternate"' in html:
        return html

    en_route, ar_route = page_variants(path)
    en = f"{SITE_URL}{en_route}".replace("index.html", "")
    ar = f"{SITE_URL}{ar_route}".replace("index.html", "")

    links = (
        f'      <link rel="alternate" hreflang="en" href="{en}">\n'
        f'      <link rel="alternate" hreflang="ar" href="{ar}">\n'
        f'      <link rel="alternate" hreflang="x-default" href="{en}">\n'
    )
    if "      <link rel=\"icon\"" in html:
        return html.replace("      <link rel=\"icon\"", links + "      <link rel=\"icon\"", 1)
    return insert_before_head_close(html, "\n" + links.rstrip())


def patch_accessibility(html: str) -> str:
    html = html.replace(
        '<div class="md-search" data-md-component="search" role="dialog">',
        '<div class="md-search" data-md-component="search" role="dialog" aria-label="Search dialog">',
    )
    html = html.replace(
        '<div class="md-dialog" data-md-component="dialog">',
        '<div class="md-dialog" data-md-component="dialog" role="dialog" aria-label="Site message">',
    )
    html = re.sub(
        r'(<a\b(?=[^>]*\btarget=["\']_blank["\'])(?=[^>]*\brel=["\']noopener["\'])(?![^>]*\bnoreferrer\b)[^>]*\brel=["\'])([^"\']*)(["\'])',
        lambda match: f"{match.group(1)}{match.group(2)} noreferrer{match.group(3)}",
        html,
        flags=re.IGNORECASE,
    )
    return html


def is_redirect(html: str) -> bool:
    head = html[:1200].lower()
    return 'http-equiv="refresh"' in head or "location.replace(" in head


def is_indexable_standalone(path: Path, html: str) -> bool:
    if path.name == "index.html":
        return False
    if path.name == "404.html":
        return False
    if is_redirect(html):
        return False
    return True


def is_indexable(path: Path, html: str) -> bool:
    if path.name == "404.html":
        return False
    if is_redirect(html):
        return False
    return True


def write_urlset(filename: str, paths: list[Path]) -> None:
    urls = []
    for path in sorted(paths):
        urls.append(
            "    <url>\n"
            f"        <loc>{escape_attr(canonical_url(path))}</loc>\n"
            "    </url>"
        )

    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    target = SITE / filename
    temporary = target.with_name(target.name + ".tmp")
    temporary.write_text(sitemap, encoding="utf-8")
    temporary.replace(target)


def write_standalone_sitemap(paths: list[Path]) -> None:
    write_urlset(STANDALONE_SITEMAP, paths)


def main() -> int:
    if not SITE.is_dir():
        print("[warn] site directory not found; skipping HTML optimization")
        return 0

    changed = 0
    standalone_pages: list[Path] = []
    all_pages: list[Path] = []
    offline_placeholders = 0
    for path in SITE.rglob("*.html"):
        stat = path.stat()
        if stat.st_size > 0 and stat.st_blocks == 0:
            offline_placeholders += 1
            continue
        original = path.read_text(encoding="utf-8")
        html = patch_accessibility(original)
        html = optimize_images(html)
        html = ensure_meta(html, path)
        html = add_alternates(html, path)

        if html != original:
            path.write_text(html, encoding="utf-8")
            changed += 1

        if is_indexable_standalone(path, html):
            standalone_pages.append(path)
        if is_indexable(path, html):
            all_pages.append(path)

    print(f"[ok] optimized generated HTML: {changed} files")
    if offline_placeholders:
        print(f"[warn] optimizer skipped {offline_placeholders} offline filesystem placeholders")
    write_standalone_sitemap(standalone_pages)
    print(f"[ok] wrote {STANDALONE_SITEMAP}: {len(standalone_pages)} URLs")
    write_urlset(SITEMAP, all_pages)
    print(f"[ok] wrote {SITEMAP}: {len(all_pages)} URLs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
