#!/usr/bin/env python3
"""Losslessly optimize PDFs in a built static-site directory with qpdf.

No image downsampling, JPEG recompression, or rasterization is performed.
A candidate replaces its original only when qpdf succeeds, passes qpdf --check,
and is smaller.

Deploys stay fast because results are cached by the SHA-256 of the original
file: with --cache, a PDF that was optimized before is copied from the cache
instead of being recompressed, and only new or changed PDFs reach qpdf, which
runs in parallel. --deterministic-id makes the output identical on every run,
so Firebase Hosting does not re-upload unchanged PDFs.

    python3 scripts/compress_pdfs_losslessly.py docs --cache .pdf-cache
"""
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import stat
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

QPDF_ARGS = [
    "--object-streams=generate",
    "--recompress-flate",
    "--compression-level=9",
    "--deterministic-id",
]
# Bump when QPDF_ARGS change so old cached results are not reused.
CACHE_VERSION = "v2"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def optimize_pdf(path: Path) -> tuple[int, int, str]:
    original_stat = path.stat()
    original_size = original_stat.st_size
    with tempfile.NamedTemporaryFile(
        prefix=f".{path.stem}.", suffix=".optimized.pdf", dir=path.parent, delete=False
    ) as handle:
        candidate = Path(handle.name)

    try:
        result = subprocess.run(["qpdf", *QPDF_ARGS, str(path), str(candidate)], capture_output=True, text=True)
        if result.returncode not in (0, 3) or not candidate.exists():
            detail = (result.stderr or result.stdout).strip().splitlines()
            return original_size, original_size, detail[-1] if detail else "qpdf failed"

        check = subprocess.run(["qpdf", "--check", str(candidate)], capture_output=True, text=True)
        if check.returncode not in (0, 3):
            detail = (check.stderr or check.stdout).strip().splitlines()
            return original_size, original_size, detail[-1] if detail else "validation failed"

        optimized_size = candidate.stat().st_size
        if optimized_size < original_size:
            candidate.chmod(stat.S_IMODE(original_stat.st_mode))
            candidate.replace(path)
            return original_size, optimized_size, "optimized"
        return original_size, original_size, "already optimal"
    finally:
        candidate.unlink(missing_ok=True)


def process(pdf: Path, cache: Path | None) -> tuple[int, int, str, bool, set[str]]:
    """Return (before, after, status, cache_hit, cache files used)."""
    if cache is None:
        return (*optimize_pdf(pdf), False, set())
    key = f"{CACHE_VERSION}-{sha256(pdf)}"
    hit_pdf, hit_same = cache / f"{key}.pdf", cache / f"{key}.same"
    before = pdf.stat().st_size
    if hit_pdf.is_file():
        mode = stat.S_IMODE(pdf.stat().st_mode)
        shutil.copyfile(hit_pdf, pdf)
        pdf.chmod(mode)
        return before, pdf.stat().st_size, "optimized", True, {hit_pdf.name}
    if hit_same.is_file():
        return before, before, "already optimal", True, {hit_same.name}
    before, after, status = optimize_pdf(pdf)
    if status == "optimized":
        shutil.copyfile(pdf, hit_pdf)
        return before, after, status, False, {hit_pdf.name}
    if status == "already optimal":
        hit_same.touch()
        return before, after, status, False, {hit_same.name}
    return before, after, status, False, set()  # failures are retried next run


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("directory", type=Path, help="Built site directory to scan")
    parser.add_argument("--cache", type=Path, help="Directory of results from earlier runs")
    parser.add_argument("--jobs", type=int, default=os.cpu_count() or 2, help="Parallel qpdf processes")
    args = parser.parse_args()

    root = args.directory.resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    cache = args.cache.resolve() if args.cache else None
    if cache:
        cache.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(root.rglob("*.pdf")) + sorted(root.rglob("*.PDF"))
    print(f"Found {len(pdfs)} PDF files under {root}" + (f" (cache: {cache})" if cache else ""))

    total_before = total_after = optimized_count = unchanged_count = failed_count = hits = 0
    used: set[str] = set()
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        for pdf, (before, after, status, hit, files) in zip(pdfs, pool.map(lambda p: process(p, cache), pdfs)):
            total_before += before
            total_after += after
            hits += hit
            used |= files
            if status == "optimized":
                optimized_count += 1
                if not hit:
                    print(f"Optimized: {pdf.relative_to(root)} ({before:,} -> {after:,} bytes)")
            elif status == "already optimal":
                unchanged_count += 1
            else:
                failed_count += 1
                print(f"::warning file={pdf}::Could not optimize PDF without altering its content: {status}")

    new = 0
    if cache:
        # Drop results for PDFs that no longer exist so the cache stays the size of the site.
        for entry in cache.iterdir():
            if entry.name not in used:
                entry.unlink()
        new = len(pdfs) - hits - failed_count

    saved = total_before - total_after
    print("\nLossless PDF optimization summary")
    print(f"PDFs scanned: {len(pdfs)}")
    if cache:
        print(f"From cache: {hits}")
        print(f"Newly processed: {new}")
    print(f"Optimized: {optimized_count}")
    print(f"Unchanged: {unchanged_count}")
    print(f"Could not process: {failed_count}")
    print(f"Before: {total_before:,} bytes ({total_before / 1024**3:.2f} GiB)")
    print(f"After:  {total_after:,} bytes ({total_after / 1024**3:.2f} GiB)")
    print(f"Saved:  {saved:,} bytes ({saved / 1024**2:.1f} MiB)")

    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as handle:
            handle.write(f"new={new}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
