#!/usr/bin/env python3
"""Make hand-written pages use the free space on laptop, iPad and iPhone screens.

Every page in docs/ has its own inline CSS, so the fixes are measured rather than
guessed: each page is loaded in headless Chrome and a marked style block,
<style data-page-fit>, is written just before </head> with overrides for what
the browser finds:

  laptop (1440px)   containers that cap the main column far below the screen are
                    widened to min(1320px, 100%); long paragraphs and list items held
                    to a narrow max-width inside a wide column are released
  phone (390px)     side padding/margins wider than 16px on the main column are
                    slimmed; sticky headers taller than 16% of the screen scroll away
                    instead; tables, code blocks and long words stop running off
                    the right edge

Passes repeat (up to 3) because widening a container can expose capped text.
Selectors get a :not(#pf) bump so they beat the page's own rules without
!important. Re-running replaces the block. Check results with
scripts/check_responsive_layout.py.

    .venv/bin/python scripts/fit_page_layout.py docs/path/page.html ...
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from check_responsive_layout import DOCS, launch_browser, start_server

BLOCK_RE = re.compile(r"\s*<style data-page-fit>.*?</style>", re.S)
BUMP = ":not(#pf)"

HELPERS = r"""
  const selectorOf = e => {
    if (e.id && /^[A-Za-z][\w-]*$/.test(e.id)) return '#' + e.id;
    let s = e.tagName.toLowerCase();
    for (const c of e.classList) if (/^[A-Za-z_][\w-]*$/.test(c)) s += '.' + c;
    if (s === e.tagName.toLowerCase() && e.parentElement && e.parentElement !== document.body && e.parentElement !== document.documentElement)
      s = selectorOf(e.parentElement) + ' > ' + s;
    return s;
  };
  const chrome = e => e.closest('header, nav, footer, dialog, aside, [role=dialog], .hero, [data-slide-figure]');
  const visible = e => { const r = e.getBoundingClientRect(), cs = getComputedStyle(e); return r.width > 40 && r.height > 8 && cs.display !== 'none' && cs.visibility !== 'hidden'; };
  const contentBlocks = () => [...document.querySelectorAll('p, li, h2, h3, h4, table, pre, figure, blockquote')].filter(e => !chrome(e) && visible(e));
  const mainChain = blocks => {
    const counts = new Map();
    for (const b of blocks) for (let a = b.parentElement; a && a !== document.documentElement; a = a.parentElement) counts.set(a, (counts.get(a) || 0) + 1);
    return [...counts].filter(([a, n]) => n >= blocks.length * 0.3 && a !== document.body).map(([a]) => a);
  };
"""

DESKTOP = "(() => {" + HELPERS + r"""
  const vw = document.documentElement.clientWidth;
  const blocks = contentBlocks();
  const widen = new Set(), release = new Set();
  for (const a of mainChain(blocks)) {
    const cs = getComputedStyle(a), r = a.getBoundingClientRect();
    const capped = cs.maxWidth !== 'none' && parseFloat(cs.maxWidth) >= 400 && parseFloat(cs.maxWidth) < 1200;
    const parent = a.parentElement.getBoundingClientRect();
    const fixedWidth = cs.maxWidth === 'none' && r.width < parent.width * 0.8 && Math.abs((r.left - parent.left) - (parent.right - r.right)) < 4;
    if ((capped || fixedWidth) && r.width < vw * 0.85) widen.add(selectorOf(a));
  }
  for (const p of document.querySelectorAll('main p, main li, section p, section li, article p, .container p, .wrap p, .content p')) {
    if (chrome(p) || !visible(p) || p.textContent.trim().length < 80) continue;
    const cs = getComputedStyle(p);
    if (cs.maxWidth === 'none') continue;
    const parent = p.parentElement, pcs = getComputedStyle(parent);
    if (pcs.display.includes('flex') || pcs.display.includes('grid')) continue;
    const inner = parent.clientWidth - parseFloat(pcs.paddingLeft) - parseFloat(pcs.paddingRight);
    if (inner > 560 && p.getBoundingClientRect().width < inner * 0.85) release.add(selectorOf(p));
  }
  return { widen: [...widen], release: [...release] };
})()"""

PHONE = "(() => {" + HELPERS + r"""
  const vw = document.documentElement.clientWidth, vh = window.innerHeight;
  const blocks = contentBlocks();
  const gutters = new Set(), unstick = new Set(), scroll = new Set(), wrap = new Set(), shrink = new Set();
  for (const a of mainChain(blocks)) {
    const cs = getComputedStyle(a);
    const side = Math.max(parseFloat(cs.paddingLeft), parseFloat(cs.paddingRight));
    const margin = Math.max(parseFloat(cs.marginLeft), parseFloat(cs.marginRight));
    const r = a.getBoundingClientRect();
    if (side > 16 || (margin > 16 && r.width < vw - 32)) gutters.add(selectorOf(a));
  }
  for (const e of document.querySelectorAll('body *')) {
    const cs = getComputedStyle(e);
    if (cs.position === 'sticky') {
      const r = e.getBoundingClientRect();
      if (r.width >= vw * 0.9 && r.height > vh * 0.16) unstick.add(selectorOf(e));
    }
  }
  for (const e of document.querySelectorAll('table, pre')) {
    if (chrome(e) || !visible(e)) continue;
    const box = e.parentElement.getBoundingClientRect();
    if (e.scrollWidth > box.width + 1 || e.getBoundingClientRect().right > vw + 1) scroll.add(e.tagName.toLowerCase());
  }
  for (const e of document.querySelectorAll('h1, h2, h3, h4, p, li, td, th, code, a, span')) {
    if (!visible(e) || e.closest('table, pre')) continue;
    if (e.getBoundingClientRect().right > vw + 1) wrap.add(selectorOf(e));
  }
  for (const e of document.querySelectorAll('body *')) {
    if (e.closest('table, pre, header, nav, dialog') || !visible(e)) continue;
    const r = e.getBoundingClientRect(), cs = getComputedStyle(e);
    if (r.right > vw + 1 && r.width > vw * 0.6 && cs.position !== 'absolute' && cs.position !== 'fixed') shrink.add(selectorOf(e));
  }
  return { gutters: [...gutters], unstick: [...unstick], scroll: [...scroll], wrap: [...wrap], shrink: [...shrink] };
})()"""


def bump(selectors) -> str:
    return ",\n".join(f"{s}{BUMP}" for s in sorted(selectors))


def css_for(found: dict[str, set[str]]) -> str:
    parts = ["/* Generated by scripts/fit_page_layout.py from measurements at laptop and phone widths; re-run to refresh. */"]
    if found["widen"]:
        parts.append(f"{bump(found['widen'])} {{\n  width: auto;\n  max-width: min(1320px, 100%);\n}}")
    if found["release"]:
        parts.append(f"{bump(found['release'])} {{\n  max-width: none;\n}}")
    phone = []
    if found["gutters"]:
        phone.append(f"{bump(found['gutters'])} {{\n    padding-left: 16px;\n    padding-right: 16px;\n    margin-left: 0;\n    margin-right: 0;\n  }}")
    if found["unstick"]:
        phone.append(f"{bump(found['unstick'])} {{\n    position: relative;\n    top: auto;\n  }}")
    if found["scroll"]:
        phone.append(f"{bump(found['scroll'])} {{\n    display: block;\n    max-width: 100%;\n    overflow-x: auto;\n  }}")
    if found["wrap"]:
        phone.append(f"{bump(found['wrap'])} {{\n    overflow-wrap: anywhere;\n    min-width: 0;\n  }}")
    if found["shrink"]:
        phone.append(f"{bump(found['shrink'])} {{\n    max-width: 100%;\n    min-width: 0;\n  }}")
    if phone:
        parts.append("@media (max-width: 600px) {\n  " + "\n\n  ".join(phone) + "\n}")
    return "\n\n".join(parts)


def write_block(path: Path, css: str) -> None:
    text = BLOCK_RE.sub("", path.read_text(encoding="utf-8"))
    if css:
        idx = text.lower().index("</head>")
        text = text[:idx] + f"<style data-page-fit>\n{css}\n</style>\n" + text[idx:]
    path.write_text(text, encoding="utf-8")


def fit(browser, origin: str, path: Path) -> dict[str, set[str]]:
    rel = path.relative_to(DOCS).as_posix()
    found: dict[str, set[str]] = {k: set() for k in ("widen", "release", "gutters", "unstick", "scroll", "wrap", "shrink")}
    write_block(path, "")
    for _ in range(3):
        before = sum(len(v) for v in found.values())
        for script, width, height in ((DESKTOP, 1440, 900), (PHONE, 390, 844)):
            page = browser.new_page(viewport={"width": width, "height": height})
            page.goto(origin + rel, wait_until="load", timeout=20000)
            page.wait_for_timeout(300)
            for key, values in page.evaluate(script).items():
                found[key].update(values)
            page.close()
        write_block(path, css_for(found) if any(found.values()) else "")
        if sum(len(v) for v in found.values()) == before:
            break
    return found


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pages", nargs="+", type=Path)
    args = ap.parse_args()
    from playwright.sync_api import sync_playwright

    server, origin = start_server()
    with sync_playwright() as pw:
        browser = launch_browser(pw)
        for path in (p.resolve() for p in args.pages):
            found = fit(browser, origin, path)
            summary = ", ".join(f"{k} {len(v)}" for k, v in found.items() if v) or "nothing to change"
            print(f"{path.relative_to(DOCS.parent)}: {summary}")
        browser.close()
    server.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
