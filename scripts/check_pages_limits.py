#!/usr/bin/env python3
"""Fail early if the build will not fit Cloudflare Pages' free plan.

Pages accepts at most 20,000 files per deploy and 25 MiB per file. Run on the
final output, after offload_annotated_figures.py:

    python3 scripts/check_pages_limits.py
"""
from __future__ import annotations

import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
MAX_FILES = 20_000
MAX_BYTES = 25 * 1024 * 1024
WARN_FILES = 18_000


def main() -> int:
    files = [p for p in DOCS.rglob("*") if p.is_file()]
    big = sorted((p.stat().st_size, p) for p in files if p.stat().st_size > MAX_BYTES)
    print(f"Pages build: {len(files)} files (limit {MAX_FILES})")
    failed = False
    if len(files) > MAX_FILES:
        print(f"[error] {len(files) - MAX_FILES} files over the Cloudflare Pages limit")
        failed = True
    elif len(files) > WARN_FILES:
        print(f"::warning::Pages build has {len(files)} of {MAX_FILES} allowed files")
    for size, path in big:
        print(f"[error] {path.relative_to(DOCS)} is {size / 1024 / 1024:.1f} MiB (limit 25 MiB)")
        failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
