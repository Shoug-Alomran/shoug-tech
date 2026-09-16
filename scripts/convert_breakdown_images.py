#!/usr/bin/env python3
"""Convert local breakdown raster assets to PNG without changing decoded pixels.

Updates references throughout docs and removes an original only after its PNG
has been verified. Shared site artwork outside slide-breakdowns is untouched.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import unquote, urlsplit
import html
import re

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
RASTER = {".webp", ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".tiff", ".avif"}
URL = re.compile(r"[^\s\"'<>`()]+\.(?:webp|jpe?g|gif|bmp|tiff?|avif)(?:[?#][^\s\"'<>`()]*)?", re.I)


def convert(source):
    target = source.with_suffix(".png")
    with Image.open(source) as image:
        if getattr(image, "n_frames", 1) > 1:
            raise ValueError(f"Animated image requires explicit handling: {source}")
        pixels = image.convert("RGBA" if "A" in image.getbands() or "transparency" in image.info else "RGB")
        if not target.exists():
            temporary = target.with_suffix(".png.tmp")
            pixels.save(temporary, format="PNG", optimize=True)
            temporary.replace(target)
        with Image.open(target) as check:
            if check.format != "PNG" or check.size != pixels.size or check.convert(pixels.mode).tobytes() != pixels.tobytes():
                raise ValueError(f"PNG differs from original: {target}")
    return source.resolve(), target.resolve()


def main():
    sources = sorted(p for folder in DOCS.glob("academics/*/*/slide-breakdowns")
                     for p in folder.rglob("*") if p.suffix.lower() in RASTER)
    with ThreadPoolExecutor(max_workers=4) as pool:
        mapping = dict(pool.map(convert, sources))
    changed = 0
    for page in DOCS.rglob("*"):
        if page.suffix.lower() not in {".html", ".css", ".js", ".json", ".md"}:
            continue
        original = page.read_text(encoding="utf-8")
        if not URL.search(original):
            continue

        def replace(match):
            raw = match.group(0)
            url = urlsplit(html.unescape(raw))
            if url.scheme or url.netloc:
                return raw
            path = unquote(url.path)
            resolved = (DOCS / path.lstrip("/") if path.startswith("/") else page.parent / path).resolve()
            if resolved not in mapping:
                return raw
            return re.sub(r"\.(webp|jpe?g|gif|bmp|tiff?|avif)(?=[?#]|$)", ".png", raw, count=1, flags=re.I)

        updated = URL.sub(replace, original)
        if updated != original:
            page.write_text(updated, encoding="utf-8")
            changed += 1
    # Every target has passed a decoded-pixel comparison before any deletion.
    for source in sources:
        source.unlink()
    print(f"Converted and verified {len(mapping)} images; updated {changed} files.")


if __name__ == "__main__":
    main()
