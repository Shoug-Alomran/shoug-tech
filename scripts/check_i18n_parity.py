#!/usr/bin/env python3
"""Check EN/AR Markdown parity for mkdocs-static-i18n suffix structure."""

from __future__ import annotations

from pathlib import Path
import argparse
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check English/Arabic markdown parity.")
    parser.add_argument("--docs-dir", default="docs", help="Docs root directory")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on any mismatch")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    docs = Path(args.docs_dir)
    if not docs.exists():
        print(f"[error] docs dir not found: {docs}")
        return 1

    english = []
    arabic = set()
    for path in docs.rglob("*.md"):
        if path.name.endswith(".ar.md"):
            english_pair = path.with_name(path.stem[:-3] + ".md")
            arabic.add(str(english_pair))
        else:
            english.append(path)

    missing_ar = [p for p in english if str(p) not in arabic]
    orphan_ar = []
    for path in docs.rglob("*.ar.md"):
        pair = path.with_name(path.stem[:-3] + ".md")
        if not pair.exists():
            orphan_ar.append(path)

    print("i18n parity report")
    print(f"- English markdown files: {len(english)}")
    print(f"- Missing Arabic pairs: {len(missing_ar)}")
    print(f"- Orphan Arabic files: {len(orphan_ar)}")

    if missing_ar:
        print("\nMissing Arabic:")
        for p in missing_ar:
            print(f"- {p}")
    if orphan_ar:
        print("\nOrphan Arabic:")
        for p in orphan_ar:
            print(f"- {p}")

    if args.strict and (missing_ar or orphan_ar):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
