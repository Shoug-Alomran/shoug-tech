#!/usr/bin/env python3
"""Render the diagrams listed in cys403_study/figures.py out of the slide PDFs.

Each slide is rendered with pdftoppm (poppler), cropped to its box, trimmed of
white margin and saved as WebP next to its breakdown:
    slide-breakdowns/NN-chapter-N-<slug>/figures/slide-PP.webp
Run build_cys403_study_tools.py afterwards to place them in the pages.
"""
from __future__ import annotations

import importlib
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageChops

from build_cys403_study_tools import BASE, breakdown_folder, slides_folder
from cys403_study.figures import FIGURES, image_name

DPI = 150
PAD = 14


def trim(im: Image.Image) -> Image.Image:
    diff = ImageChops.difference(im, Image.new("RGB", im.size, (255, 255, 255)))
    box = diff.convert("L").point(lambda v: 255 if v > 18 else 0).getbbox()
    if not box:
        return im
    return im.crop((max(0, box[0] - PAD), max(0, box[1] - PAD), min(im.width, box[2] + PAD), min(im.height, box[3] + PAD)))


def main() -> None:
    count = 0
    with tempfile.TemporaryDirectory() as tmp:
        for number, figures in FIGURES.items():
            ch = importlib.import_module(f"cys403_study.ch{number:02d}")
            pdf = BASE / "slides" / slides_folder(ch) / f"{slides_folder(ch)}.pdf"
            out = BASE / "slide-breakdowns" / breakdown_folder(ch) / "figures"
            out.mkdir(exist_ok=True)
            for page, (x0, y0, x1, y1), _section, _caption in figures:
                stem = Path(tmp) / f"ch{number}-p{page}"
                subprocess.run(["pdftoppm", "-r", str(DPI), "-png", "-singlefile", "-f", str(page), "-l", str(page), str(pdf), str(stem)], check=True)
                im = Image.open(f"{stem}.png").convert("RGB")
                w, h = im.size
                trim(im.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)))).save(out / image_name(page), "WEBP", quality=86, method=6)
                count += 1
    print(f"Extracted {count} CYS403 slide figures.")


if __name__ == "__main__":
    main()
