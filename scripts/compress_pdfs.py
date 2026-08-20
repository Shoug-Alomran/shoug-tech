#!/usr/bin/env python3
"""Compress course PDFs with Ghostscript.

Slide decks and scanned handouts dominate the deployed site size, so we
re-encode their images at screen resolution. Run with --dry-run first: it
writes the candidates to a scratch directory and reports the savings without
touching anything under docs/.

    python3 scripts/compress_pdfs.py --dry-run
    python3 scripts/compress_pdfs.py --apply
"""
from __future__ import annotations

import argparse
import concurrent.futures
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"

# Below this size the Ghostscript pass rarely wins enough to be worth the
# re-encode, and text-only handouts can even grow.
MIN_BYTES = 400 * 1024

# Keep a rewrite only if it saves at least this fraction of the original.
MIN_SAVING = 0.10

GS_SETTINGS = "/ebook"  # 150 dpi images; slides stay crisp at full-screen.


def human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if abs(n) < 1024 or unit == "GB":
            return f"{n:.1f} {unit}" if unit != "B" else f"{n} B"
        n /= 1024.0
    return f"{n:.1f} GB"


def compress(src: Path, dest: Path) -> bool:
    cmd = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.5",
        f"-dPDFSETTINGS={GS_SETTINGS}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        "-dDetectDuplicateImages=true",
        "-dCompressFonts=true",
        "-dSubsetFonts=true",
        f"-sOutputFile={dest}",
        str(src),
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, timeout=600)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False
    return dest.exists() and dest.stat().st_size > 0


def page_count(pdf: Path) -> int | None:
    """Cheap integrity check: a rewrite that loses pages is a failed rewrite."""
    try:
        out = subprocess.run(
            ["gs", "-q", "-dNODISPLAY", "-dNOSAFER", "-c",
             f"({pdf.as_posix()}) (r) file runpdfbegin pdfpagecount = quit"],
            check=True, capture_output=True, timeout=120, text=True,
        )
        return int(out.stdout.strip())
    except Exception:
        return None


def process(pdf: Path, workdir: Path, apply: bool) -> tuple[Path, int, int, str]:
    before = pdf.stat().st_size
    tmp = workdir / (pdf.stem + "-" + str(abs(hash(str(pdf)))) + ".pdf")
    if not compress(pdf, tmp):
        return pdf, before, before, "gs-failed"

    after = tmp.stat().st_size
    if after >= before * (1 - MIN_SAVING):
        tmp.unlink(missing_ok=True)
        return pdf, before, before, "no-gain"

    src_pages, out_pages = page_count(pdf), page_count(tmp)
    if src_pages is not None and out_pages is not None and src_pages != out_pages:
        tmp.unlink(missing_ok=True)
        return pdf, before, before, f"page-mismatch {src_pages}->{out_pages}"

    if apply:
        shutil.move(str(tmp), str(pdf))
    else:
        tmp.unlink(missing_ok=True)
    return pdf, before, after, "ok"


def main() -> int:
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    ap.add_argument("--limit", type=int, default=0, help="only the N largest PDFs")
    ap.add_argument("--jobs", type=int, default=max(1, (os.cpu_count() or 4) // 2))
    args = ap.parse_args()

    pdfs = [p for p in DOCS.rglob("*.pdf") if p.stat().st_size >= MIN_BYTES]
    pdfs.sort(key=lambda p: p.stat().st_size, reverse=True)
    if args.limit:
        pdfs = pdfs[: args.limit]

    total_before = sum(p.stat().st_size for p in pdfs)
    print(f"{len(pdfs)} PDFs >= {human(MIN_BYTES)}, {human(total_before)} total")
    print(f"mode={'APPLY' if args.apply else 'DRY RUN'} jobs={args.jobs}\n")

    saved = 0
    skipped: list[tuple[Path, str]] = []
    with tempfile.TemporaryDirectory() as td:
        workdir = Path(td)
        with concurrent.futures.ThreadPoolExecutor(args.jobs) as pool:
            futures = [pool.submit(process, p, workdir, args.apply) for p in pdfs]
            for i, fut in enumerate(concurrent.futures.as_completed(futures), 1):
                pdf, before, after, status = fut.result()
                rel = pdf.relative_to(DOCS)
                if status != "ok":
                    skipped.append((rel, status))
                    continue
                saved += before - after
                pct = (before - after) / before * 100
                print(f"[{i}/{len(pdfs)}] {human(before)} -> {human(after)}  "
                      f"-{pct:.0f}%  {rel}")

    print(f"\nwould save {human(saved)}" if args.dry_run else f"\nsaved {human(saved)}")
    print(f"deployed PDF payload: {human(total_before)} -> {human(total_before - saved)}")
    if skipped:
        print(f"\n{len(skipped)} left untouched:")
        for rel, why in skipped[:20]:
            print(f"  {why}: {rel}")
        if len(skipped) > 20:
            print(f"  ...and {len(skipped) - 20} more")
    return 0


if __name__ == "__main__":
    sys.exit(main())
