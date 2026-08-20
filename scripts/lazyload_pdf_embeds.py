#!/usr/bin/env python3
"""Convert eager PDF <iframe> embeds into click-to-load facades.

A slide deck in an eager iframe downloads in full before the page settles.
This rewrites each one into a placeholder that javascripts/pdf-embed.js turns
into a card, and adds loading="lazy" to every other iframe on the site.

Idempotent: pages already carrying a .pdf-embed placeholder are left alone.
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
LOADER = "/javascripts/pdf-embed.js"

IFRAME = re.compile(r"<iframe\b[^>]*>\s*</iframe>", re.I)
ATTR = re.compile(r'([a-zA-Z0-9_:.-]+)\s*=\s*"([^"]*)"')
# The facade emits a <noscript> fallback iframe. Re-running must not treat that
# fallback as fresh input, so noscript blocks are masked out before rewriting.
NOSCRIPT = re.compile(r"<noscript\b.*?</noscript>", re.I | re.S)


def attrs_of(tag: str) -> dict[str, str]:
    return {m.group(1).lower(): m.group(2) for m in ATTR.finditer(tag)}


def is_pdf(src: str) -> bool:
    return src.split("?")[0].split("#")[0].lower().endswith(".pdf")


def rewrite(text: str) -> tuple[str, int, int]:
    """Return (new_text, pdf_facades, lazied_iframes)."""
    facades = lazied = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal facades, lazied
        tag = m.group(0)
        a = attrs_of(tag)
        src = a.get("src", "")

        if src and is_pdf(src):
            title = a.get("title", "PDF document")
            facades += 1
            # <noscript> keeps the deck reachable without JS; it is inert
            # otherwise, so it costs nothing in the normal path.
            return (
                f'<div class="pdf-embed" data-pdf-src="{html.escape(src, quote=True)}"'
                f' data-pdf-title="{html.escape(title, quote=True)}"></div>'
                f'<noscript><iframe src="{html.escape(src, quote=True)}"'
                f' width="100%" height="100%"'
                f' title="{html.escape(title, quote=True)}"></iframe></noscript>'
            )

        if "loading" not in a:
            lazied += 1
            return tag[: -len("></iframe>")] + ' loading="lazy"></iframe>' \
                if tag.lower().endswith("></iframe>") else tag
        return tag

    shelf: list[str] = []

    def stash(m: re.Match[str]) -> str:
        shelf.append(m.group(0))
        return f"\x00noscript{len(shelf) - 1}\x00"

    masked = NOSCRIPT.sub(stash, text)
    out = IFRAME.sub(repl, masked)
    for i, block in enumerate(shelf):
        out = out.replace(f"\x00noscript{i}\x00", block)
    return out, facades, lazied


def ensure_loader(text: str) -> str:
    if LOADER in text:
        return text
    tag = f'<script src="{LOADER}" defer></script>\n'
    if "</body>" in text:
        return text.replace("</body>", tag + "</body>", 1)
    return text + tag


def main() -> int:
    apply = "--apply" in sys.argv
    pages = facades = lazied = 0

    for p in sorted(DOCS.rglob("*.html")):
        original = p.read_text(encoding="utf-8", errors="ignore")
        if "<iframe" not in original:
            continue
        text, f, lz = rewrite(original)
        if f:
            text = ensure_loader(text)
        if text == original:
            continue
        pages += 1
        facades += f
        lazied += lz
        if apply:
            p.write_text(text, encoding="utf-8")

    verb = "rewrote" if apply else "would rewrite"
    print(f"{verb} {pages} pages: {facades} PDF embeds -> click-to-load, "
          f"{lazied} other iframes lazied")
    if not apply:
        print("re-run with --apply to write changes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
