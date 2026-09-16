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
  // Something already scrolling above this element means its width is deliberate.
  const clipped = e => {
    const vw = document.documentElement.clientWidth;
    for (let a = e.parentElement; a && a !== document.documentElement; a = a.parentElement) {
      const cs = getComputedStyle(a);
      if (/(auto|scroll|hidden|clip)/.test(cs.overflowX) && a.getBoundingClientRect().right <= vw + 1) return true;
    }
    return false;
  };
  const visible = e => { const r = e.getBoundingClientRect(), cs = getComputedStyle(e); return r.width > 40 && r.height > 8 && cs.display !== 'none' && cs.visibility !== 'hidden'; };
  const contentBlocks = () => [...document.querySelectorAll('p, li, h2, h3, h4, table, pre, figure, blockquote')].filter(e => !chrome(e) && visible(e));
  // Count by selector, not by element: a page whose sections each wrap their content
  // in .wrap has no single element holding the column, but one selector covers it.
  const mainChain = blocks => {
    const counts = new Map(), sample = new Map();
    for (const b of blocks) {
      const seen = new Set();
      for (let a = b.parentElement; a && a !== document.documentElement; a = a.parentElement) {
        if (a === document.body) continue;
        const s = selectorOf(a);
        if (seen.has(s)) continue;
        seen.add(s);
        counts.set(s, (counts.get(s) || 0) + 1);
        if (!sample.has(s)) sample.set(s, a);
      }
    }
    return [...counts].filter(([s, n]) => n >= blocks.length * 0.3).map(([s]) => sample.get(s));
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
  // A fixed grid track (e.g. "240px 900px" for sidebar + content) caps the column
  // no matter what max-width says; the last track has to become flexible.
  const gridWiden = [];
  const seenGrid = new Set();
  for (const a of mainChain(blocks)) {
    const parent = a.parentElement;
    if (!parent || a.getBoundingClientRect().width >= vw * 0.85) continue;
    const pcs = getComputedStyle(parent);
    if (!pcs.display.includes('grid')) continue;
    const tracks = pcs.gridTemplateColumns.trim().split(/\s+/);
    if (tracks.length < 2 || !/px$/.test(tracks[tracks.length - 1])) continue;
    const sel = selectorOf(parent);
    if (seenGrid.has(sel)) continue;
    seenGrid.add(sel);
    gridWiden.push([sel, tracks.slice(0, -1).join(' ')]);
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
  return { widen: [...widen], release: [...release], gridwiden: gridWiden };
})()"""

PHONE = "(() => {" + HELPERS + r"""
  const vw = document.documentElement.clientWidth, vh = window.innerHeight;
  const blocks = contentBlocks();
  const gutters = new Set(), unstick = new Set(), scroll = new Set(), wrap = new Set(), shrink = new Set();
  // Page-level containers (full-bleed, not cards) stack their side padding: 16 + 20
  // reads as a 36px gutter. Keep the outermost at 16px and flatten the rest.
  // Walk the real ancestor chain of a few content blocks rather than one sample per
  // selector: the sample for a selector can be a narrow element that hides the
  // full-width one actually holding the padding.
  const rails = [];
  const railSeen = new Set();
  const probes = blocks.filter((_, i) => i % Math.max(1, Math.floor(blocks.length / 6)) === 0).slice(0, 6);
  // body counts too: on some pages the whole gutter is body padding.
  for (const block of probes) {
    for (let a = block.parentElement; a && a !== document.documentElement; a = a.parentElement) {
      const cs = getComputedStyle(a), r = a.getBoundingClientRect();
      const side = parseFloat(cs.paddingLeft) + parseFloat(cs.paddingRight);
      const margin = Math.max(parseFloat(cs.marginLeft), parseFloat(cs.marginRight));
      if (r.width < vw * 0.8) continue;
      if (!(side > 8 || (margin > 16 && r.width < vw - 32))) continue;
      const sel = selectorOf(a);
      if (railSeen.has(sel)) continue;
      railSeen.add(sel);
      rails.push([a, sel]);
    }
  }
  rails.sort((x, y) => (x[0].compareDocumentPosition(y[0]) & Node.DOCUMENT_POSITION_CONTAINED_BY) ? -1 : 1);
  const tighten = new Set();
  rails.forEach(([, sel], i) => (i === 0 ? gutters : tighten).add(sel));
  for (const e of document.querySelectorAll('body *')) {
    const cs = getComputedStyle(e);
    if (cs.position === 'sticky') {
      const r = e.getBoundingClientRect();
      if (r.width >= vw * 0.9 && r.height > vh * 0.16) unstick.add(selectorOf(e));
    }
  }
  for (const e of document.querySelectorAll('table, pre')) {
    if (chrome(e) || !visible(e) || clipped(e)) continue;
    if (e.getBoundingClientRect().right > vw + 1) scroll.add(e.tagName.toLowerCase());
  }
  for (const e of document.querySelectorAll('h1, h2, h3, h4, p, li, td, th, code, a, span, small, div')) {
    if (!visible(e) || e.closest('table, pre') || clipped(e)) continue;
    // Either the box itself sticks out, or its text is wider than the box and pushes
    // the document out from the inside (long words, code identifiers, «stereotypes»).
    if (e.getBoundingClientRect().right > vw + 1 || e.scrollWidth > e.clientWidth + 1) wrap.add(selectorOf(e));
  }
  const grids = new Set();
  for (const e of document.querySelectorAll('body *')) {
    if (e.closest('table, pre, header, nav, dialog') || !visible(e)) continue;
    const r = e.getBoundingClientRect(), cs = getComputedStyle(e);
    if (cs.position === 'absolute' || cs.position === 'fixed') continue;
    // A fixed-column grid or a min-width wider than the screen pushes the whole page out.
    if (!clipped(e) && (cs.display === 'grid' || cs.display === 'inline-grid') && e.scrollWidth > e.clientWidth + 1) grids.add(selectorOf(e));
    if (parseFloat(cs.minWidth) > vw) shrink.add(selectorOf(e));
    if (r.right > vw + 1 && !clipped(e)) shrink.add(selectorOf(e));
  }
  return { gutters: [...gutters], tighten: [...tighten], unstick: [...unstick], scroll: [...scroll], wrap: [...wrap], shrink: [...shrink], grids: [...grids] };
})()"""


def bump(selectors) -> str:
    return ",\n".join(f"{s}{BUMP}" for s in sorted(selectors))


# Narrow-screen probes run at these widths; each one's findings go in a media query
# that starts just above it, so a fix measured on an iPad also applies on a phone.
BREAKPOINTS = [(1024, 1100), (768, 820), (390, 600)]
NARROW_ONLY = ("gutters", "tighten", "unstick")

RULES = {
    "gutters": "padding-left: 16px;\n    padding-right: 16px;\n    margin-left: 0;\n    margin-right: 0;",
    "tighten": "padding-left: 0;\n    padding-right: 0;",
    "unstick": "position: relative;\n    top: auto;",
    # min-width: 0 as well, or a table's own min-width keeps the scroll box too wide.
    "scroll": "display: block;\n    max-width: 100%;\n    min-width: 0;\n    overflow-x: auto;",
    # white-space too: overflow-wrap cannot break a line that is set never to wrap.
    "wrap": "overflow-wrap: anywhere;\n    white-space: normal;\n    min-width: 0;",
    "shrink": "max-width: 100%;\n    min-width: 0;\n    overflow-wrap: anywhere;",
    "grids": "grid-template-columns: 1fr;",
}


def css_for(found: dict) -> str:
    parts = ["/* Generated by scripts/fit_page_layout.py from measurements at laptop, iPad and phone widths; re-run to refresh. */"]
    if found["widen"]:
        parts.append(f"{bump(found['widen'])} {{\n  width: auto;\n  max-width: min(1320px, 100%);\n}}")
    for selector, prefix in sorted(found["gridwiden"]):
        tracks = f"{prefix} minmax(0, 1fr)" if prefix else "minmax(0, 1fr)"
        parts.append(f"{selector}{BUMP} {{\n  max-width: min(1320px, 100%);\n  grid-template-columns: {tracks};\n}}")
    if found["release"]:
        parts.append(f"{bump(found['release'])} {{\n  max-width: none;\n}}")
    emitted: dict[str, set[str]] = {key: set() for key in RULES}
    for width, media in BREAKPOINTS:
        block = []
        for key, body in RULES.items():
            if key in NARROW_ONLY and width > 430:
                continue
            fresh = found["narrow"].get(width, {}).get(key, set()) - emitted[key]
            if fresh:
                emitted[key] |= fresh
                block.append(f"{bump(fresh)} {{\n    {body}\n  }}")
        if block:
            parts.append(f"@media (max-width: {media}px) {{\n  " + "\n\n  ".join(block) + "\n}")
    return "\n\n".join(parts)


def write_block(path: Path, css: str) -> None:
    text = BLOCK_RE.sub("", path.read_text(encoding="utf-8"))
    if css:
        idx = text.lower().index("</head>")
        text = text[:idx] + f"<style data-page-fit>\n{css}\n</style>\n" + text[idx:]
    path.write_text(text, encoding="utf-8")


def total(found: dict) -> int:
    return len(found["widen"]) + len(found["release"]) + len(found["gridwiden"]) + sum(
        len(values) for width in found["narrow"].values() for values in width.values())


def fit(browser, origin: str, path: Path) -> dict:
    rel = path.relative_to(DOCS).as_posix()
    found: dict = {"widen": set(), "release": set(), "gridwiden": set(), "narrow": {width: {} for width, _ in BREAKPOINTS}}
    write_block(path, "")
    for _ in range(3):
        before = total(found)
        passes = [(DESKTOP, 1440, 900, None)] + [(PHONE, width, 1180 if width > 430 else 844, width) for width, _ in BREAKPOINTS]
        for script, width, height, bucket in passes:
            page = browser.new_page(viewport={"width": width, "height": height})
            # A page carrying twenty figures can outrun the first navigation; retry once
            # with more time, and skip the pass rather than abandoning the whole run.
            try:
                page.goto(origin + rel, wait_until="domcontentloaded", timeout=30000)
            except Exception:
                try:
                    page.goto(origin + rel, wait_until="commit", timeout=60000)
                except Exception as exc:
                    print(f"  {rel} @{width}px: navigation failed, skipped ({str(exc).splitlines()[0]})")
                    page.close()
                    continue
            page.wait_for_timeout(400)
            for key, values in page.evaluate(script).items():
                if bucket is None:
                    found[key].update(tuple(v) if isinstance(v, list) else v for v in values)
                elif values:
                    found["narrow"][bucket].setdefault(key, set()).update(values)
            page.close()
        write_block(path, css_for(found) if total(found) else "")
        if total(found) == before:
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
            counts = {"widen": len(found["widen"]), "gridwiden": len(found["gridwiden"]), "release": len(found["release"])}
            for width, groups in found["narrow"].items():
                for key, values in groups.items():
                    counts[f"{key}@{width}"] = counts.get(f"{key}@{width}", 0) + len(values)
            summary = ", ".join(f"{k} {n}" for k, n in counts.items() if n) or "nothing to change"
            print(f"{path.relative_to(DOCS.parent)}: {summary}")
        browser.close()
    server.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
