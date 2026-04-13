#!/usr/bin/env python3
"""Check-EN/AR-Markdown-parity-for-mkdocs-static-i18n-suffix-structure."""

from __future__ import annotations

import argparse
from pathlib import Path
from urllib.parse import quote


def to_arabic_pair(path: Path) -> Path:
    return path.with_name(f"{path.stem}.ar.md")


def to_english_pair(path: Path) -> Path:
    return path.with_name(path.stem[:-3] + ".md")


def stale_quiz_alias_target(path: Path) -> Path | None:
    """Return the canonical quiz Arabic path for stale aliases like chapter-4.ar.md.

    This catches renamed leftovers inside `quizez/` where the English/Arabic pair
    already exists under `*-quiz.md` / `*-quiz.ar.md`.
    """
    if path.parent.name.lower() != "quizez":
        return None

    english_stem = path.stem[:-3]
    if english_stem.endswith("-quiz"):
        return None

    quiz_en = path.with_name(f"{english_stem}-quiz.md")
    quiz_ar = path.with_name(f"{english_stem}-quiz.ar.md")
    if quiz_en.exists() and quiz_ar.exists():
        return quiz_ar
    return None


def page_href_for_markdown(src: Path, docs_root: Path) -> str:
    rel = src.relative_to(docs_root)
    stemmed = rel.with_suffix("")
    parts = list(stemmed.parts)
    if parts and parts[-1] == "index":
        parts = parts[:-1]
    encoded = "/".join(quote(part) for part in parts)
    return f"/{encoded}/" if encoded else "/"


def make_placeholder_ar(src: Path, docs_root: Path) -> str:
    rel_src = src.relative_to(docs_root).as_posix()
    english_href = page_href_for_markdown(src, docs_root)
    return (
        "> ⚠️ هذه الصفحة قيد الترجمة إلى العربية.\n\n"
        "> This page is pending Arabic localization.\n\n"
        f"[View English version]({english_href})\n\n"
        "---\n\n"
        f"<!-Auto-generated-to-satisfy-EN/AR-parity-for:-{rel_src}->\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check-English/Arabic-markdown-parity.")
    parser.add_argument("--docs-dir", default="docs", help="Docs root directory")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on any mismatch")
    parser.add_argument(
        "--autofix-missing-ar",
        action="store_true",
        help="Auto-create placeholder *.ar.md files for missing Arabic pairs",
    )
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

    created = 0
    if args.autofix_missing_ar and missing_ar:
        for src in missing_ar:
            ar_path = to_arabic_pair(src)
            ar_path.parent.mkdir(parents=True, exist_ok=True)
            ar_path.write_text(make_placeholder_ar(src, docs), encoding="utf-8")
            created += 1
        # Recompute sets after autofix so strict mode reflects final state.
        arabic.update(str(p) for p in missing_ar)
        missing_ar = [p for p in english if str(p) not in arabic]

    orphan_ar = []
    removed_stale_aliases = []
    for path in docs.rglob("*.ar.md"):
        pair = to_english_pair(path)
        if not pair.exists():
            stale_alias = stale_quiz_alias_target(path)
            if args.autofix_missing_ar and stale_alias is not None:
                path.unlink()
                removed_stale_aliases.append((path, stale_alias))
                continue
            orphan_ar.append(path)

    print("i18n parity report")
    print(f"- English markdown files: {len(english)}")
    print(f"- Missing Arabic pairs: {len(missing_ar)}")
    print(f"- Orphan Arabic files: {len(orphan_ar)}")
    if created:
        print(f"- Auto-created Arabic placeholders: {created}")
    if removed_stale_aliases:
        print(f"- Removed stale Arabic aliases: {len(removed_stale_aliases)}")

    if missing_ar:
        print("\nMissing Arabic:")
        for p in missing_ar:
            print(f"- {p}")
    if orphan_ar:
        print("\nOrphan Arabic:")
        for p in orphan_ar:
            stale_alias = stale_quiz_alias_target(p)
            if stale_alias is not None:
                print(f"- {p} (stale alias; canonical file exists at {stale_alias})")
            else:
                print(f"- {p}")
    if removed_stale_aliases:
        print("\nRemoved stale Arabic aliases:")
        for old_path, canonical_path in removed_stale_aliases:
            print(f"- {old_path} -> keep {canonical_path}")

    if args.strict and (missing_ar or orphan_ar):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
