#!/usr/bin/env python3
"""Losslessly optimize PDFs in a built static-site directory with qpdf.

No image downsampling, JPEG recompression, or rasterization is performed.
A candidate replaces its original only when qpdf succeeds and the result is smaller.
"""
from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path


def optimize_pdf(path: Path) -> tuple[int, int, str]:
    original_size = path.stat().st_size
    with tempfile.NamedTemporaryFile(
        prefix=f".{path.stem}.", suffix=".optimized.pdf", dir=path.parent, delete=False
    ) as handle:
        candidate = Path(handle.name)

    try:
        result = subprocess.run(
            [
                "qpdf",
                "--object-streams=generate",
                "--recompress-flate",
                "--compression-level=9",
                str(path),
                str(candidate),
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode not in (0, 3) or not candidate.exists():
            detail = (result.stderr or result.stdout).strip().splitlines()
            return original_size, original_size, detail[-1] if detail else "qpdf failed"

        # Validate the generated file before considering replacement.
        check = subprocess.run(
            ["qpdf", "--check", str(candidate)],
            capture_output=True,
            text=True,
        )
        if check.returncode not in (0, 3):
            detail = (check.stderr or check.stdout).strip().splitlines()
            return original_size, original_size, detail[-1] if detail else "validation failed"

        optimized_size = candidate.stat().st_size
        if optimized_size < original_size:
            candidate.replace(path)
            return original_size, optimized_size, "optimized"
        return original_size, original_size, "already optimal"
    finally:
        candidate.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="Built site directory to scan")
    args = parser.parse_args()

    root = args.directory.resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")

    pdfs = sorted(root.rglob("*.pdf")) + sorted(root.rglob("*.PDF"))
    total_before = total_after = optimized_count = unchanged_count = failed_count = 0
    print(f"Found {len(pdfs)} PDF files under {root}")

    for pdf in pdfs:
        before, after, status = optimize_pdf(pdf)
        total_before += before
        total_after += after
        if status == "optimized":
            optimized_count += 1
            print(f"Optimized: {pdf.relative_to(root)} ({before:,} -> {after:,} bytes)")
        elif status == "already optimal":
            unchanged_count += 1
        else:
            failed_count += 1
            print(f"::warning file={pdf}::Could not optimize PDF without altering its content: {status}")

    saved = total_before - total_after
    print("\nLossless PDF optimization summary")
    print(f"PDFs scanned: {len(pdfs)}")
    print(f"Optimized: {optimized_count}")
    print(f"Unchanged: {unchanged_count}")
    print(f"Could not process: {failed_count}")
    print(f"Before: {total_before:,} bytes ({total_before / 1024**3:.2f} GiB)")
    print(f"After:  {total_after:,} bytes ({total_after / 1024**3:.2f} GiB)")
    print(f"Saved:  {saved:,} bytes ({saved / 1024**2:.1f} MiB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
