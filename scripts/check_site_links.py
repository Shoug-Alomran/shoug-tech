#!/usr/bin/env python3
"""Validate generated internal links and assets in the built MkDocs site."""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
IGNORED_SCHEMES = {"http", "https", "mailto", "tel", "javascript", "data", "blob"}
HTML_SUFFIXES = {"", ".html"}


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.refs: list[tuple[str, str]] = []
        self.anchors: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {name.lower(): value for name, value in attrs if value is not None}

        for attr in ("id", "name"):
            value = attr_map.get(attr)
            if value:
                self.anchors.add(value)

        for attr in ("href", "src"):
            value = attr_map.get(attr)
            if value:
                self.refs.append((attr, value))


def html_files() -> list[Path]:
    return sorted(SITE.rglob("*.html"))


def parse_html(path: Path) -> LinkParser:
    parser = LinkParser()
    parser.feed(path.read_text(encoding="utf-8", errors="ignore"))
    return parser


def route_to_file(url_path: str) -> Path:
    decoded = unquote(url_path).lstrip("/")
    target = SITE / decoded

    if target.is_file():
        return target

    if not Path(decoded).suffix or url_path.endswith("/"):
        return target / "index.html"

    return target


def is_internal(ref: str, base_url: str) -> tuple[bool, str, str]:
    if not ref or ref.startswith("#"):
        resolved = urlsplit(urljoin(base_url, ref))
    else:
        resolved = urlsplit(urljoin(base_url, ref))

    if resolved.scheme in IGNORED_SCHEMES:
        return False, "", ""

    if resolved.netloc not in {"", "site.local"}:
        return False, "", ""

    return True, resolved.path or "/", resolved.fragment


def main() -> int:
    if not SITE.is_dir():
        print("[error] site directory not found. Run `mkdocs build` first.")
        return 1

    parsed = {path: parse_html(path) for path in html_files()}
    anchors_by_file = {path: parser.anchors for path, parser in parsed.items()}
    failures: list[str] = []

    for source, parser in parsed.items():
        rel_source = source.relative_to(SITE).as_posix()
        base_url = f"https://site.local/{rel_source}"

        for attr, ref in parser.refs:
            internal, path, fragment = is_internal(ref, base_url)
            if not internal:
                continue

            target = route_to_file(path)
            if not target.is_file():
                failures.append(f"{rel_source}: {attr}={ref!r} -> missing {path}")
                continue

            if fragment and target.suffix.lower() in HTML_SUFFIXES:
                anchors = anchors_by_file.get(target)
                if anchors is None and target.suffix.lower() == ".html":
                    anchors = parse_html(target).anchors
                    anchors_by_file[target] = anchors

                if anchors is not None and fragment not in anchors:
                    failures.append(
                        f"{rel_source}: {attr}={ref!r} -> missing anchor #{fragment}"
                    )

    if failures:
        print(f"[error] broken internal references: {len(failures)}")
        for item in failures[:100]:
            print(f"  - {item}")
        if len(failures) > 100:
            print(f"  ... {len(failures) - 100} more")
        return 1

    print(f"[ok] generated internal links and assets: {len(parsed)} HTML files checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
