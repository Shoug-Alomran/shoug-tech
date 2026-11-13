#!/usr/bin/env python3
"""Put the slide text under each PDF slide viewer so bots and AI assistants can read it.

The slides live inside a PDF viewer, so anything that reads the page without opening
the PDF (search engines, ChatGPT, Claude, Perplexity) sees only the menu. This copies
the text build_ai_slide_contexts.py already extracted into a collapsed "Text version"
section at the end of the page. Run it at deploy after that script:

    python3 scripts/add_slide_text.py
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
CONTEXTS = DOCS / "ai-context"
# The paid course is sealed before publishing; its text must never be copied out.
EXCLUDED = "/ethcs303/"
BLOCK = re.compile(r'\s*<section class="slide-text"[^>]*data-generated="slide-text".*?</section>', re.S)
STYLE = (
    "<style>"
    ".slide-text{margin:2rem 0 1rem;border:1px solid rgba(var(--sg-accent-rgb,0,255,170),.3);border-radius:6px}"
    ".slide-text summary{cursor:pointer;padding:.85rem 1rem;font-family:var(--font-mono,monospace);"
    "font-size:.85rem;letter-spacing:.04em;color:var(--sg-accent,inherit)}"
    ".slide-text-body{padding:0 1rem 1rem;columns:2 26rem;column-gap:2rem}"
    ".slide-text-body article{break-inside:avoid;margin:0 0 1.25rem}"
    ".slide-text-body h2{font-size:.8rem;font-family:var(--font-mono,monospace);margin:0 0 .35rem;"
    "color:var(--sg-accent,inherit);letter-spacing:.06em}"
    ".slide-text-body p{margin:0;white-space:pre-line;font-size:.9rem;line-height:1.5;overflow-wrap:anywhere}"
    "@media (max-width:640px){.slide-text-body{columns:1;padding:0 .75rem .75rem}}"
    "</style>"
)


def clean(text: str) -> str:
    lines = (re.sub(r"[ \t ]+", " ", line).strip() for line in text.splitlines())
    return "\n".join(line for line in lines if line)


def section(chunks: list[dict]) -> str:
    slides = []
    for chunk in chunks:
        if not re.fullmatch(r"Slide \d+", chunk.get("label", "")):
            continue
        body = clean(chunk.get("text", ""))
        if body:
            slides.append(f'<article><h2>{html.escape(chunk["label"]).upper()}</h2><p>{html.escape(body)}</p></article>')
    if not slides:
        return ""
    count = f'{len(slides)} slide{"s" if len(slides) != 1 else ""}'
    return (
        f'\n        <section class="slide-text" aria-label="Text version of these slides" data-generated="slide-text">'
        f"{STYLE}<details><summary>[ TEXT VERSION // {count} ]</summary>"
        f'<div class="slide-text-body">{"".join(slides)}</div></details></section>'
    )


def main() -> int:
    changed = 0
    for context in sorted(CONTEXTS.rglob("context.json")):
        data = json.loads(context.read_text(encoding="utf-8"))
        route = data.get("route", "")
        page = DOCS / route.strip("/") / "index.html"
        if EXCLUDED in route or not route.endswith("/") or not page.is_file():
            continue
        original = page.read_text(encoding="utf-8")
        if "data-pdf-src=" not in original or "</main>" not in original:
            continue
        block = section(data.get("chunks", []))
        updated = BLOCK.sub("", original)
        if block:
            cut = updated.rfind("</main>")
            updated = updated[:cut].rstrip() + block + "\n      " + updated[cut:]
        if updated != original:
            page.write_text(updated, encoding="utf-8")
            changed += 1
    print(f"Slide text: {changed} viewer pages updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
