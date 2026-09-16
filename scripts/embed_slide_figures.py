#!/usr/bin/env python3
"""Embed slide diagrams into hand-written slide-breakdown pages.

Each course has a manifest, scripts/slide-figures/<course>.json:

    {
      "pages": [
        {
          "page": "docs/academics/<track>/<course>/slide-breakdowns/<folder>/<topic>.html",
          "decks": {"a": "docs/academics/<track>/<course>/slides/<folder>/<deck>.pdf"},
          "figures": [
            {"deck": "a", "slide": 12, "box": [0, 0.2, 1, 0.9], "section": "framing",
             "caption": "Byte stuffing: an escape byte is added before any flag-like byte."}
          ]
        }
      ]
    }

box is the crop (left, top, right, bottom) as fractions of the slide, keeping the slide
title and footer out; the leftover white margin is trimmed. section is the id of the
<section> the figure belongs to: figures go at the end of that section (inside its
content wrapper when the section holds a single wrapper element). "deck" may be
omitted when the page has one deck.

    python3 scripts/embed_slide_figures.py cs331             # render crops, then embed
    python3 scripts/embed_slide_figures.py cs331 --no-extract
    python3 scripts/embed_slide_figures.py --all

Re-running is safe: figures from an earlier run (data-slide-figure) are replaced, and
the shared /styles/slide-figures.css + /javascripts/slide-figures.js links get a
content hash so browsers pick up changes.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MANIFESTS = ROOT / "scripts" / "slide-figures"
CSS_URL = "/styles/slide-figures.css"
JS_URL = "/javascripts/slide-figures.js"
DPI = 150
PAD = 14

FIGURE_RE = re.compile(r'\s*<figure class="sfx-figure" data-slide-figure>.*?</figure>', re.S)
MASKED_RE = re.compile(r"<(script|style)\b.*?</\1\s*>|<!--.*?-->", re.S | re.I)
TAG_RE = re.compile(r"<(/?)([a-zA-Z][\w-]*)\b[^>]*?(/?)>")
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
WRAPPERS = {"div", "article"}


# --------------------------------------------------------------------------- images

def trim(im: Image.Image) -> Image.Image:
    diff = ImageChops.difference(im, Image.new("RGB", im.size, (255, 255, 255)))
    box = diff.convert("L").point(lambda v: 255 if v > 18 else 0).getbbox()
    if not box:
        return im
    return im.crop((max(0, box[0] - PAD), max(0, box[1] - PAD), min(im.width, box[2] + PAD), min(im.height, box[3] + PAD)))


def render_crop(pdf: Path, slide: int, box: list[float], out: Path, cache: dict) -> None:
    key = (pdf, slide)
    if key not in cache:
        tmp = Path(cache["_dir"]) / f"{len(cache)}"
        subprocess.run(["pdftoppm", "-r", str(DPI), "-png", "-singlefile", "-f", str(slide), "-l", str(slide), str(pdf), str(tmp)], check=True)
        cache[key] = Image.open(f"{tmp}.png").convert("RGB")
    im = cache[key]
    x0, y0, x1, y1 = box
    w, h = im.size
    out.parent.mkdir(parents=True, exist_ok=True)
    trim(im.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)))).save(out, "WEBP", quality=86, method=6)


def image_name(entry: dict, fig: dict) -> str:
    if len(entry["decks"]) == 1:
        return f"slide-{fig['slide']:02d}.webp"
    return f"{deck_of(entry, fig)}-slide-{fig['slide']:02d}.webp"


def deck_of(entry: dict, fig: dict) -> str:
    return fig.get("deck") or next(iter(entry["decks"]))


# --------------------------------------------------------------------------- html

def versioned(url: str) -> str:
    digest = hashlib.sha1((DOCS / url.lstrip("/")).read_bytes()).hexdigest()[:10]
    return f"{url}?v={digest}"


def figure_html(src: str, caption: str, width: int, height: int, slide: int, source: str = "") -> str:
    alt = html.escape(re.sub(r"<[^>]+>", "", html.unescape(caption)), quote=True)
    label = f'PDF page {slide}'
    tag = f'<a class="sfx-tag" href="{html.escape(source, quote=True)}">{label}</a>' if source else f'<span class="sfx-tag">{label}</span>'
    return (f'<figure class="sfx-figure" data-slide-figure><button type="button" class="sfx-zoom" aria-label="Enlarge figure: {alt}">'
            f'<img src="{src}" alt="{alt}" width="{width}" height="{height}" loading="lazy" decoding="async" /></button>'
            f'<figcaption>{tag}{html.escape(caption)}</figcaption></figure>')


def masked(text: str) -> str:
    """Blank out script/style/comment bodies (same length) so their markup-like strings are ignored."""
    return MASKED_RE.sub(lambda m: " " * len(m.group(0)), text)


def children(mtext: str, start: int, end: int) -> tuple[list[tuple[str, int, int]], int]:
    """Top-level elements between start and end as (tag, open_start, close_start), and where the scan stopped."""
    out, stack = [], []
    for m in TAG_RE.finditer(mtext, start, end):
        closing, tag, selfclose = m.group(1), m.group(2).lower(), m.group(3)
        if not closing:
            if tag in VOID or selfclose:
                if not stack:
                    out.append((tag, m.start(), m.start()))
                continue
            stack.append((tag, m.start()))
        else:
            while stack and stack[-1][0] != tag:
                stack.pop()
            if stack:
                open_tag, open_start = stack.pop()
                if not stack:
                    out.append((open_tag, open_start, m.start()))
    return out, end


def section_insert_point(text: str, section_id: str, page: Path) -> int:
    mtext = masked(text)
    # Generated pages (the CYS405/CYS406 study tools) emit <section> without an id,
    # so a manifest may address a section by its 1-based position instead.
    if str(section_id).isdigit():
        sections = list(re.finditer(r"<section\b[^>]*>", mtext))
        index = int(section_id)
        if not 1 <= index <= len(sections):
            raise SystemExit(f"{page.relative_to(ROOT)}: section {index} of {len(sections)} does not exist")
        opening = sections[index - 1]
    else:
        opening = re.search(rf'<section\b[^>]*\bid="{re.escape(section_id)}"[^>]*>', mtext)
    if not opening:
        # Older breakdowns use sibling heading blocks rather than sections.
        # Insert before the next heading block, or at the parent container's end.
        anchor = re.search(rf'<(div|span|article|h2|h3)\b[^>]*\bid="{re.escape(section_id)}"[^>]*>', mtext)
        if anchor:
            stack = []
            for tag in TAG_RE.finditer(mtext, 0, anchor.start()):
                closing, name, selfclose = tag.group(1), tag.group(2).lower(), tag.group(3)
                if closing:
                    if stack and stack[-1][0] == name:
                        stack.pop()
                elif name not in VOID and not selfclose:
                    stack.append((name, tag.end()))
            if stack:
                parent, start = stack[-1]
                # Default to the end of the document: a parent whose closing tag the
                # scan never finds must not leave the bound unset.
                depth, end = 1, len(mtext)
                for tag in TAG_RE.finditer(mtext, start):
                    if tag.group(2).lower() == parent:
                        depth += -1 if tag.group(1) else 1
                        if depth == 0:
                            end = tag.start()
                            break
                kids, _ = children(mtext, start, end)
                for name, begin, close in kids:
                    if begin <= anchor.start():
                        continue
                    opening_text = mtext[begin:mtext.index('>', begin) + 1]
                    if (name in {'h2', 'h3'} or
                            re.search(r'class="[^"]*(?:section-header|section-heading)', opening_text)):
                        return begin
                return end
        ids = re.findall(r'<section\b[^>]*\bid="([^"]+)"', mtext)
        raise SystemExit(f"{page.relative_to(ROOT)}: no <section id=\"{section_id}\">; ids here: {', '.join(ids)}")
    depth, pos = 1, opening.end()
    for m in re.finditer(r"<(/?)section\b[^>]*>", mtext[opening.end():]):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            pos = opening.end() + m.start()
            break
    else:
        raise SystemExit(f"{page.relative_to(ROOT)}: section {section_id} is never closed")
    inner_start, close = opening.end(), pos
    # Descend through lone wrapper elements (e.g. <section><div class="wrap">...</div></section>)
    # so figures keep the section's padding and width.
    for _ in range(3):
        kids, _ = children(mtext, inner_start, close)
        if len(kids) != 1 or kids[0][0] not in WRAPPERS:
            break
        tag, open_start, close_start = kids[0]
        inner_start = mtext.index(">", open_start) + 1
        close = close_start
    return close


def ensure_assets(text: str) -> str:
    css, js = versioned(CSS_URL), versioned(JS_URL)
    if CSS_URL in text:
        text = re.sub(rf'{re.escape(CSS_URL)}(\?v=[0-9a-f]+)?', css, text)
    else:
        text = text.replace("</head>", f'  <link rel="stylesheet" href="{css}" />\n</head>', 1)
    if JS_URL in text:
        text = re.sub(rf'{re.escape(JS_URL)}(\?v=[0-9a-f]+)?', js, text)
    else:
        idx = text.lower().rindex("</body>")
        text = text[:idx] + f'  <script src="{js}" defer></script>\n' + text[idx:]
    return text


def embed(entry: dict, extract: bool, cache: dict) -> int:
    page = ROOT / entry["page"]
    decks = {k: ROOT / v for k, v in entry["decks"].items()}
    folder = page.parent / "figures"
    blocks: dict[str, list[str]] = {}
    for fig in entry["figures"]:
        if deck_of(entry, fig) not in decks:
            raise SystemExit(f"{page}: unknown figure deck")
        if not (len(fig["box"]) == 4 and 0 <= fig["box"][0] < fig["box"][2] <= 1
                and 0 <= fig["box"][1] < fig["box"][3] <= 1):
            raise SystemExit(f"{page}: invalid crop for slide {fig['slide']}")
        out = folder / image_name(entry, fig)
        if extract:
            render_crop(decks[deck_of(entry, fig)], fig["slide"], fig["box"], out, cache)
        if not out.exists():
            raise SystemExit(f"{out.relative_to(ROOT)} missing: run without --no-extract")
        with Image.open(out) as im:
            width, height = im.size
        blocks.setdefault(fig["section"], []).append(
            figure_html(f"figures/{out.name}", fig["caption"], width, height, fig["slide"],
                        os.path.relpath(decks[deck_of(entry, fig)], page.parent) + f"#page={fig['slide']}"))

    text = FIGURE_RE.sub("", page.read_text(encoding="utf-8"))
    # Insert from the end of the file backwards so earlier offsets stay valid.
    points = sorted(((section_insert_point(text, sid, page), sid) for sid in blocks), reverse=True)
    for at, sid in points:
        line_start = text.rfind("\n", 0, at) + 1
        indent = re.match(r"[ \t]*", text[line_start:at]).group(0)
        block = "".join(f"\n{indent}  {b}" for b in blocks[sid]) + f"\n{indent}"
        text = text[:at].rstrip() + block + text[at:].lstrip(" \t")
    page.write_text(ensure_assets(text), encoding="utf-8")
    # A course can contain hundreds of figures; release rendered pages after
    # each breakdown rather than retaining every full-resolution slide.
    for key in list(cache):
        if key != "_dir":
            cache.pop(key).close()
    return len(entry["figures"])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("courses", nargs="*", help="manifest names in scripts/slide-figures/ (e.g. cs331)")
    ap.add_argument("--all", action="store_true", help="every manifest")
    ap.add_argument("--no-extract", action="store_true", help="reuse existing crops")
    args = ap.parse_args()
    names = sorted(p.stem for p in MANIFESTS.glob("*.json")) if args.all else args.courses
    if not names:
        ap.error("name a course manifest or pass --all")
    with tempfile.TemporaryDirectory() as tmp:
        cache = {"_dir": tmp}
        for name in names:
            manifest = json.loads((MANIFESTS / f"{name}.json").read_text(encoding="utf-8"))
            total = sum(embed(entry, not args.no_extract, cache) for entry in manifest["pages"])
            print(f"{name}: {total} figures across {len(manifest['pages'])} page(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
