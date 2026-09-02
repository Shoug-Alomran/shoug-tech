#!/usr/bin/env python3
"""Build grounded AI context files for every page in the academics section."""
from __future__ import annotations

import html
import json
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = DOCS / "ai-context"
COURSE_ROUTES = DOCS / "javascripts" / "course-routes.js"
COURSE_DIR = re.compile(r"^/academics/[a-z0-9-]+/([a-z]{2,5}\d{2,4}[a-z]?)/$", re.I)
ELIGIBLE = re.compile(r"^/academics/(?:.+/)?index\.html$")
PDF_REF = re.compile(r'data-pdf-src="([^"]+)"|<iframe[^>]*\bsrc="([^"]+\.pdf(?:[?#][^"]*)?)"', re.I)
IFRAME_REF = re.compile(r'<iframe[^>]*\bsrc="([^"]+\.html(?:[?#][^"]*)?)"', re.I)
TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
MAX_CHUNK_CHARS = 4200


class VisibleText(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.skip = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in {"script", "style", "svg", "nav", "header", "footer", "noscript"}:
            self.skip += 1
        elif not self.skip and tag in {"h1", "h2", "h3", "h4", "p", "li", "tr", "section", "br"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "svg", "nav", "header", "footer", "noscript"} and self.skip:
            self.skip -= 1
        elif not self.skip and tag in {"h1", "h2", "h3", "h4", "p", "li", "tr", "section"}:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.parts.append(data)

    def text(self) -> str:
        value = html.unescape(" ".join(self.parts))
        value = re.sub(r"[ \t]+", " ", value)
        value = re.sub(r"\n\s*\n+", "\n\n", value)
        return value.strip()


def route_for(page: Path) -> str:
    rel = page.relative_to(DOCS).as_posix()
    return "/" + rel[: -len("index.html")]


def resolve(page: Path, src: str) -> Path | None:
    path = unquote(urlsplit(src).path)
    target = DOCS / path.lstrip("/") if path.startswith("/") else page.parent / path
    try:
        target = target.resolve()
        target.relative_to(DOCS.resolve())
        return target
    except (OSError, ValueError):
        return None


def chunk_text(text: str, prefix: str) -> list[dict[str, str]]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n|(?<=\.)\s+(?=[A-Z])", text) if p.strip()]
    chunks: list[dict[str, str]] = []
    current: list[str] = []
    size = 0
    for paragraph in paragraphs:
        if current and size + len(paragraph) > MAX_CHUNK_CHARS:
            chunks.append({"label": f"{prefix} {len(chunks) + 1}", "text": "\n".join(current)})
            current, size = [], 0
        current.append(paragraph[:MAX_CHUNK_CHARS])
        size += len(paragraph)
    if current:
        chunks.append({"label": f"{prefix} {len(chunks) + 1}", "text": "\n".join(current)})
    return chunks


def pdf_chunks(pdf: Path) -> list[dict[str, str]]:
    try:
        result = subprocess.run(
            ["pdftotext", "-q", "-layout", str(pdf), "-"],
            capture_output=True, text=True, timeout=180, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    chunks = []
    for number, page in enumerate(result.stdout.split("\f"), 1):
        text = re.sub(r"[ \t]+", " ", page)
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        if text:
            chunks.append({"label": f"Slide {number}", "text": text[:MAX_CHUNK_CHARS]})
    return chunks


CHROME_LINE = re.compile(
    r"^(skip to content|sys_time.*|item_\d+ // .*|\[.*\]|<\s*-\s*previous.*|next\s*->|"
    r"academics /.*|© \d{4}.*|all rights reserved.*)$",
    re.I,
)


def strip_chrome(text: str) -> str:
    """Drop shared-shell navigation lines so quoted answers cite real content."""
    kept = [line for line in text.split("\n") if not CHROME_LINE.match(line.strip())]
    return re.sub(r"\n\s*\n+", "\n\n", "\n".join(kept)).strip()


def html_text(page: Path, source: str) -> str:
    parser = VisibleText()
    parser.feed(source)
    text = parser.text()
    for src in IFRAME_REF.findall(source):
        child = resolve(page, src)
        if child and child.is_file():
            child_parser = VisibleText()
            child_parser.feed(child.read_text(encoding="utf-8", errors="ignore"))
            text += "\n\n" + child_parser.text()
    return strip_chrome(text)


def main() -> int:
    pages = [p for p in DOCS.rglob("index.html") if ELIGIBLE.search("/" + p.relative_to(DOCS).as_posix())]
    titles: dict[str, str] = {}
    sources: dict[str, str] = {}
    for page in pages:
        source = page.read_text(encoding="utf-8", errors="ignore")
        route = route_for(page)
        sources[route] = source
        match = TITLE.search(source)
        titles[route] = (
            re.sub(r"\s+", " ", html.unescape(match.group(1))).strip() if match else page.parent.name
        )

    # A hub page (course home, "slides" index, …) carries little prose of its
    # own, so list what it links to. That lets the assistant answer general
    # "what does this course cover?" questions instead of finding nothing.
    children: dict[str, list[str]] = {}
    for route in titles:
        parent = route[: route.rstrip("/").rfind("/") + 1]
        if parent and parent != route and parent in titles:
            children.setdefault(parent, []).append(route)

    written = skipped = 0
    for page in pages:
        route = route_for(page)
        source = sources[route]
        title = titles[route]
        chunks: list[dict[str, str]] = []
        for a, b in PDF_REF.findall(source):
            pdf = resolve(page, a or b)
            if pdf and pdf.is_file():
                chunks.extend(pdf_chunks(pdf))
                break
        if not chunks:
            chunks = chunk_text(html_text(page, source), "Section")
        kids = sorted(children.get(route, []))
        if kids:
            listing = "\n".join(f"- {titles[kid]} ({kid})" for kid in kids)
            chunks.insert(0, {
                "label": "Contents",
                "text": f"{title} links to these pages:\n{listing}"[:MAX_CHUNK_CHARS],
            })
        if not chunks:
            skipped += 1
            continue
        destination = OUT / route.lstrip("/") / "context.json"
        destination.parent.mkdir(parents=True, exist_ok=True)
        payload = {"route": route, "title": title, "chunks": chunks}
        destination.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        written += 1
    # Course-code -> course page, so the calendar assistant can find the
    # material behind an exam like "SE322 FINAL".
    courses = {}
    for route in titles:
        match = COURSE_DIR.match(route)
        if match:
            courses[match.group(1).lower()] = route
    COURSE_ROUTES.write_text(
        "// Generated by scripts/build_ai_slide_contexts.py - do not edit.\n"
        "window.SHOUG_COURSE_ROUTES = "
        + json.dumps(dict(sorted(courses.items())), ensure_ascii=False, indent=0).replace("\n", "")
        + ";\n",
        encoding="utf-8",
    )
    print(f"wrote {written} AI contexts; skipped {skipped} empty pages; {len(courses)} course routes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
