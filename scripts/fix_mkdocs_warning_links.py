#!/usr/bin/env python3
"""Normalize MkDocs warning-prone relative asset links to site-root URLs.

MkDocs validates links against the docs source tree, while many of this repo's
wrapper pages were written relative to the built page route. Those links work
at runtime but show up as warnings during `mkdocs build --strict`.
"""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
MARKDOWN_GLOBS = ("*.md", "*.ar.md")
ASSET_SUFFIXES = (".html", ".pdf", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")
RELATIVE_ASSET_RE = re.compile(r"\.\./[^\s\"')>]+")


def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    for pattern in MARKDOWN_GLOBS:
        files.extend(DOCS.rglob(pattern))
    return sorted(set(files))


def is_arabic_markdown(path: Path) -> bool:
    return path.name.endswith(".ar.md")


def markdown_stem(path: Path) -> str:
    if path.name.endswith(".ar.md"):
        return path.name[: -len(".ar.md")]
    return path.stem


def page_route(rel_path: Path) -> str:
    stem = markdown_stem(rel_path)
    parts: list[str] = []

    if is_arabic_markdown(rel_path):
        parts.append("ar")

    if rel_path.parent != Path("."):
        parts.extend(rel_path.parent.as_posix().split("/"))

    if stem != "index":
        parts.append(stem)

    return "/" + "/".join(parts) + "/"


def docs_asset_path(abs_url: str) -> Path:
    url_path = urlsplit(abs_url).path.lstrip("/")
    if url_path.startswith("ar/"):
        url_path = url_path[3:]
    return DOCS / unquote(url_path)


def should_normalize(url: str) -> bool:
    path = urlsplit(url).path.lower()
    return path.startswith("../") and path.endswith(ASSET_SUFFIXES)


def normalize_file(path: Path) -> tuple[bool, set[str]]:
    rel_path = path.relative_to(DOCS)
    route = page_route(rel_path)
    original = path.read_text(encoding="utf-8")
    unresolved: set[str] = set()

    def replace(match: re.Match[str]) -> str:
        raw_url = match.group(0)
        if not should_normalize(raw_url):
            return raw_url

        abs_url = urljoin(route, raw_url)
        asset_path = docs_asset_path(abs_url)
        if not asset_path.exists():
            unresolved.add(f"{rel_path}: {raw_url} -> {abs_url}")
            return raw_url
        return abs_url

    updated = RELATIVE_ASSET_RE.sub(replace, original)
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return True, unresolved
    return False, unresolved


def main() -> int:
    changed = 0
    unresolved: set[str] = set()

    for path in iter_markdown_files():
        file_changed, file_unresolved = normalize_file(path)
        if file_changed:
            changed += 1
        unresolved.update(file_unresolved)

    print(f"[fix-mkdocs-warning-links] files changed: {changed}")
    if unresolved:
        print("[fix-mkdocs-warning-links] unresolved targets:")
        for item in sorted(unresolved):
            print(f"  - {item}")
        return 1

    print("[fix-mkdocs-warning-links] unresolved targets: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
