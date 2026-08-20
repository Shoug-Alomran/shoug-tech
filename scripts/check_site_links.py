#!/usr/bin/env python3
"""Validate generated internal links and assets in the built MkDocs site."""

from __future__ import annotations

import sys
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
if not SITE.is_dir() and (ROOT / "docs").is_dir():
    SITE = ROOT / "docs"
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


# Verbatim course handouts. The SE371 example-code and lab-solution trees are
# the instructor's original files, shipped as-is so students see exactly what
# they were given. They reference assets that were never in the handout and
# contain textbook typos such as href="www.borland.com". Rewriting them would
# change the study material, so their broken references are accepted rather
# than fixed -- real regressions elsewhere still fail the build.
VERBATIM_PREFIXES = (
    "academics/software-engineering/se371/extra-resources/chapter-2/example-code",
    "academics/software-engineering/se371/extra-resources/chapter-3/example-codes",
    "academics/software-engineering/se371/extra-resources/chapter-4/javascript-codes",
    "academics/software-engineering/se371/extra-resources/chapter-5/js-front-end-all-examples",
    "academics/software-engineering/se371/extra-resources/labs/solutions",
)


def is_verbatim(rel_source: str) -> bool:
    return rel_source.startswith(VERBATIM_PREFIXES)


def html_files() -> list[Path]:
    files = []
    for path in SITE.rglob("*.html"):
        stat = path.stat()
        if stat.st_size > 0 and stat.st_blocks == 0:
            continue
        files.append(path)
    return sorted(files)


# Several study pages render their sections from a JS data array and assign
# the anchor with `label.id = ch.id`, so the id never appears as an HTML
# attribute. Harvest ids written as JS/JSON string values too, otherwise those
# working in-page links are reported as broken.
JS_ID = re.compile(
    r"""(?:\.id\s*=\s*|["']id["']\s*:\s*)["']([A-Za-z0-9_:.-]+)["']"""
)


def parse_html(path: Path) -> LinkParser:
    text = path.read_text(encoding="utf-8", errors="ignore")
    parser = LinkParser()
    parser.feed(text)
    parser.anchors.update(JS_ID.findall(text))
    return parser


def route_to_file(url_path: str) -> Path:
    decoded = unquote(url_path).lstrip("/")
    target = SITE / decoded

    if target.is_file():
        return target

    if not Path(decoded).suffix or url_path.endswith("/"):
        return target / "index.html"

    return target


# Pages are resolved against an https://site.local base, so every internal
# ref comes back carrying the https scheme. Testing the *resolved* scheme
# against IGNORED_SCHEMES therefore discarded every link on the site and the
# check passed vacuously; only non-web schemes on the raw ref should be
# skipped, and externals are excluded by host instead.
NON_WEB_SCHEMES = IGNORED_SCHEMES - {"http", "https"}
LOCAL_HOSTS = {"", "site.local"}


def exact_case(target: Path) -> Path | None:
    """Resolve `target` walking each segment against the real directory
    listing, so casing differences surface on case-insensitive filesystems.
    Returns None when a segment cannot be read."""
    current = SITE
    try:
        for part in target.relative_to(SITE).parts:
            entries = {e.name for e in current.iterdir()}
            if part in entries:
                current = current / part
                continue
            lowered = {e.lower(): e for e in entries}
            match = lowered.get(part.lower())
            if match is None:
                return None
            current = current / match
    except (OSError, ValueError):
        return None
    return current


def is_internal(ref: str, base_url: str) -> tuple[bool, str, str]:
    if not ref:
        return False, "", ""

    raw_scheme = urlsplit(ref).scheme.lower()
    if raw_scheme in NON_WEB_SCHEMES:
        return False, "", ""

    resolved = urlsplit(urljoin(base_url, ref))
    if resolved.scheme.lower() not in {"", "http", "https"}:
        return False, "", ""

    if resolved.netloc not in LOCAL_HOSTS:
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
        if is_verbatim(rel_source):
            continue
        base_url = f"https://site.local/{rel_source}"

        for attr, ref in parser.refs:
            internal, path, fragment = is_internal(ref, base_url)
            if not internal:
                continue

            target = route_to_file(path)
            if not target.is_file():
                failures.append(f"{rel_source}: {attr}={ref!r} -> missing {path}")
                continue

            # macOS resolves paths case-insensitively but GitHub Pages serves
            # from a case-sensitive filesystem, so a link whose casing differs
            # from the file on disk passes here and 404s in production.
            actual = exact_case(target)
            if actual is not None and actual != target:
                failures.append(
                    f"{rel_source}: {attr}={ref!r} -> case mismatch, "
                    f"file is {actual.relative_to(SITE).as_posix()}"
                )
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
