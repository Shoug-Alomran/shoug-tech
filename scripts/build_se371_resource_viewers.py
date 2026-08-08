#!/usr/bin/env python3
"""Wrap SE371 downloadable resources in branded preview pages when possible."""

from __future__ import annotations

import hashlib
import html
import re
from pathlib import Path
from urllib.parse import quote, unquote


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
COURSE = DOCS / "academics/software-engineering/se371"
RESOURCES = COURSE / "extra-resources"
VIEWERS = RESOURCES / "resource-viewers"
PREVIEWABLE = {".pdf", ".html", ".htm", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".css", ".js", ".json", ".txt", ".md"}
IMAGES = {".png", ".jpg", ".jpeg", ".gif", ".svg"}
VIEWER_STYLES = '''<style id="se371-resource-viewer-styles">
.resource-viewer{margin:0 40px 48px}.viewer-toolbar{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:12px 14px;border:1px solid var(--border-med);background:var(--bg-surface)}.viewer-kind{font-family:var(--font-mono);font-size:.72rem;color:var(--text-tertiary)}.viewer-download{border:1px solid var(--border-purple);color:var(--text-purple-bright);padding:8px 14px;font-family:var(--font-mono);font-size:.72rem}.viewer-download:hover{background:rgba(184,41,234,.12)}.resource-frame{display:block;width:100%;height:76vh;min-height:620px;border:1px solid var(--border-med);border-top:0;background:#fff}.image-preview{display:grid;place-items:center;min-height:60vh;padding:24px;border:1px solid var(--border-med);border-top:0;background:#0a0514}.image-preview img{display:block;max-width:100%;max-height:75vh}.download-only{padding:56px 24px;border:1px solid var(--border-med);border-top:0;text-align:center;color:var(--text-secondary)}.download-only strong{display:block;color:var(--text-primary);font-family:var(--font-display);font-size:1.6rem;margin-bottom:10px}.download-only p{max-width:620px;margin:0 auto}@media(max-width:760px){.resource-viewer{margin:0 16px 32px}.viewer-toolbar{align-items:flex-start;flex-direction:column}.resource-frame{height:68vh;min-height:460px}}
</style>'''


def label_from_name(path: Path) -> str:
    words = path.stem.replace("-", " ").replace("_", " ").split()
    return " ".join(word.upper() if word.lower() in {"css", "dom", "ejs", "html", "js", "json", "pdf"} else word.title() for word in words)


def replace_content(page: str, content: str) -> str:
    start = page.index('            <div class="directory-container"')
    end = page.index("\n\n\n    <footer", start)
    return page[:start] + "            " + content + page[end:]


def viewer_route(asset: Path) -> tuple[Path, str]:
    relative = asset.relative_to(RESOURCES).as_posix()
    digest = hashlib.sha1(relative.encode()).hexdigest()[:8]
    slug = re.sub(r"[^a-z0-9]+", "-", asset.stem.lower()).strip("-") or "resource"
    folder = VIEWERS / f"{slug}-{digest}"
    route = f"/academics/software-engineering/se371/extra-resources/resource-viewers/{folder.name}/"
    return folder, route


def make_viewer(template: str, asset: Path, route: str) -> str:
    label = label_from_name(asset)
    suffix = asset.suffix.lower()
    asset_route = "/" + quote(asset.relative_to(DOCS).as_posix(), safe="/")
    canonical = f"https://shoug-tech.com{route}"
    page = re.sub(r"<title>.*?</title>", f"<title>{html.escape(label)} | SE371 Resource Viewer</title>", template, count=1, flags=re.S)
    page = re.sub(r'<meta name="description"[^>]*>', f'<meta name="description" content="Preview or download {html.escape(label)}, an SE371 Web Engineering course resource.">', page, count=1)
    page = re.sub(r'<link rel="canonical"[^>]*>', f'<link rel="canonical" href="{canonical}">', page, count=1)
    page = re.sub(r'<meta property="og:url"[^>]*>', f'<meta property="og:url" content="{canonical}">', page, count=1)
    page = page.replace('<span class="current" data-en-text="Study Material" data-ar-text="المواد الدراسية">Study Material</span>', f'<a class="breadcrumb-link" href="/academics/software-engineering/se371/extra-resources/">Study Material</a> / <span class="current">{html.escape(label)}</span>', 1)
    page = page.replace('<div class="type-label" data-en-text="STUDY MATERIAL" data-ar-text="المواد الدراسية">STUDY MATERIAL</div>', f'<div class="type-label">{html.escape(label)}</div>', 1)
    toolbar = f'<div class="viewer-toolbar"><span class="viewer-kind">{html.escape(suffix.lstrip(".").upper() or "FILE")} RESOURCE</span><a class="viewer-download" href="{asset_route}" download>DOWNLOAD FILE ↓</a></div>'
    if suffix == ".docx":
        public_asset = quote(f"https://shoug-tech.com{asset_route}", safe="")
        preview = f'<iframe class="resource-frame" src="https://view.officeapps.live.com/op/embed.aspx?src={public_asset}" title="Preview of {html.escape(label)}" loading="lazy"></iframe>'
    elif suffix in IMAGES:
        preview = f'<div class="image-preview"><img src="{asset_route}" alt="Preview of {html.escape(label)}"></div>'
    elif suffix in PREVIEWABLE:
        sandbox = ' sandbox="allow-scripts allow-forms allow-modals allow-popups allow-same-origin"' if suffix in {".html", ".htm"} else ""
        preview = f'<iframe class="resource-frame" src="{asset_route}" title="Preview of {html.escape(label)}" loading="lazy"{sandbox}></iframe>'
    else:
        preview = f'<div class="download-only"><strong>Preview unavailable for {html.escape(suffix.lstrip(".").upper())}</strong><p>This browser cannot reliably embed this file format. Use the download button above to open it in the appropriate desktop application.</p></div>'
    return replace_content(page, f'<section class="resource-viewer" aria-label="{html.escape(label)} resource viewer">{toolbar}{preview}</section>')


def main() -> None:
    template = (RESOURCES / "index.html").read_text(encoding="utf-8")
    template = re.sub(r'<style id="se371-resource-viewer-styles">.*?</style>', '', template, flags=re.S)
    template = template.replace("</head>", f"{VIEWER_STYLES}</head>")
    VIEWERS.mkdir(exist_ok=True)
    built: dict[Path, str] = {}
    for viewer_index in VIEWERS.glob("*/index.html"):
        existing = viewer_index.read_text(encoding="utf-8", errors="ignore")
        match = re.search(r'class="viewer-download" href="(/academics/software-engineering/se371/extra-resources/[^\"]+)"', existing)
        if not match:
            continue
        asset = DOCS / unquote(match.group(1).lstrip("/"))
        if not asset.is_file():
            continue
        route = f"/academics/software-engineering/se371/extra-resources/resource-viewers/{viewer_index.parent.name}/"
        viewer_index.write_text(make_viewer(template, asset, route), encoding="utf-8")
        built[asset] = route
    listing_indexes = [path for path in RESOURCES.rglob("index.html") if 'id="se371-folder-icons"' in path.read_text(encoding="utf-8", errors="ignore") and VIEWERS not in path.parents]
    for index in listing_indexes:
        text = index.read_text(encoding="utf-8")
        directory = index.parent
        hrefs = re.findall(r'<a class="dir-row" href="([^"?#]+)"', text)
        for href in hrefs:
            if href.endswith("/") or "://" in href:
                continue
            if href.startswith("/academics/software-engineering/se371/extra-resources/"):
                asset = DOCS / unquote(href.lstrip("/"))
            elif href.startswith("/"):
                continue
            else:
                asset = directory / unquote(href)
            if not asset.is_file():
                continue
            folder, route = viewer_route(asset)
            folder.mkdir(parents=True, exist_ok=True)
            (folder / "index.html").write_text(make_viewer(template, asset, route), encoding="utf-8")
            text = text.replace(f'<a class="dir-row" href="{href}"', f'<a class="dir-row" href="{route}"', 1)
            built[asset] = route
        index.write_text(text, encoding="utf-8")
    embedded = sum(path.suffix.lower() in PREVIEWABLE or path.suffix.lower() == ".docx" for path in built)
    print(f"Built {len(built)} SE371 resource viewer pages ({embedded} embedded previews).")


if __name__ == "__main__":
    main()
