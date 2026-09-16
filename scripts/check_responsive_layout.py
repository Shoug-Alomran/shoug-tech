#!/usr/bin/env python3
"""Check that pages use the space available on laptop, iPad and iPhone screens.

Each page is loaded in headless Chrome at several device sizes and checked for:
  overflow      the page scrolls sideways
  narrow        at tablet/laptop widths the content leaves wide empty gutters
  capped-text   long paragraphs held to a fraction of the column they sit in
  gutter        side padding wasted on phone widths
  offscreen     elements running past the right edge on a phone
  tall-header   a sticky/fixed header eating too much of a phone screen

Usage (Playwright lives in the repo's .venv):
    .venv/bin/python scripts/check_responsive_layout.py docs/path/page.html ...
    .venv/bin/python scripts/check_responsive_layout.py --changed [--newer MARKER] [--limit N]

--changed picks standalone HTML pages under docs/ that differ from HEAD (untracked
included), skipping index.html wrappers whose layout comes from the shared site
chrome. --newer keeps only files modified after MARKER (the Stop hook passes a
file touched at session start). Exits 1 when any page has findings.
"""
from __future__ import annotations

import argparse
import functools
import http.server
import socketserver
import subprocess
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

VIEWPORTS = [
    ("laptop", 1440, 900),
    ("ipad-landscape", 1024, 768),
    ("ipad-portrait", 768, 1024),
    ("iphone", 390, 844),
]

PROBE = r"""(() => {
  const vw = document.documentElement.clientWidth, vh = window.innerHeight;
  const found = [];
  const px = n => Math.round(n) + 'px';

  const wide = document.documentElement.scrollWidth - vw;
  if (wide > 1) found.push(['overflow', `page is ${px(wide)} wider than the ${px(vw)} screen`]);

  const visible = e => {
    const r = e.getBoundingClientRect(), cs = getComputedStyle(e);
    return r.width > 40 && r.height > 8 && cs.visibility !== 'hidden' && cs.display !== 'none';
  };
  // A wide table inside a box that scrolls is deliberate, not overflow: the viewer
  // scrolls the box, not the page. Only count it when nothing above it clips.
  const clipped = e => {
    for (let a = e.parentElement; a && a !== document.documentElement; a = a.parentElement) {
      const cs = getComputedStyle(a);
      if (/(auto|scroll|hidden|clip)/.test(cs.overflowX) && a.getBoundingClientRect().right <= vw + 1) return true;
    }
    return false;
  };
  const blocks = [...document.querySelectorAll('p, li, h1, h2, h3, h4, table, pre, figure, img, blockquote')]
    .filter(e => !e.closest('header, nav, footer, dialog, aside, [role=dialog], [hidden]'))
    .filter(visible);

  if (blocks.length >= 5) {
    const edges = blocks.map(e => e.getBoundingClientRect());
    const lefts = edges.map(r => r.left).sort((a, b) => a - b);
    const rights = edges.map(r => r.right).sort((a, b) => a - b);
    const left = lefts[Math.floor(lefts.length * 0.05)];
    const right = rights[Math.floor(rights.length * 0.95)];
    const used = right - left;
    // A persistent side rail (a tall nav/aside beside the text) is part of the design,
    // so the column is judged against the room left over next to it.
    let rail = 0;
    for (const side of document.querySelectorAll('nav, aside, [class*="sidebar"], [class*="side-nav"]')) {
      const r = side.getBoundingClientRect(), cs = getComputedStyle(side);
      if (cs.display === 'none' || cs.visibility === 'hidden' || r.width < 80 || r.height < vh * 0.5) continue;
      if (r.right <= left + 4 || r.left >= right - 4) rail = Math.max(rail, r.width);
    }
    const room = vw - rail;
    if (vw >= 700 && used / room < 0.72)
      found.push(['narrow', `content spans ${px(used)} of the ${px(room)} available${rail ? ` (beside a ${px(rail)} side rail)` : ''} (${Math.round(100 * used / room)}%), leaving ${px(left - rail)} / ${px(vw - right)} empty at the sides`]);
    if (vw <= 430 && (left > 24 || vw - right > 24))
      found.push(['gutter', `content sits ${px(left)} from the left and ${px(vw - right)} from the right edge of a ${px(vw)} phone`]);
    if (vw <= 430) {
      const off = blocks.filter(e => e.getBoundingClientRect().right > vw + 1 && !clipped(e));
      if (off.length) found.push(['offscreen', `${off.length} element(s) run past the right edge, e.g. <${off[0].tagName.toLowerCase()} class="${off[0].className}">`]);
    }
  }

  if (vw >= 700) {
    let capped = 0, example = '';
    for (const p of document.querySelectorAll('p')) {
      if (p.textContent.trim().length < 160 || !visible(p) || p.closest('header, nav, footer, dialog, figure, blockquote')) continue;
      const parent = p.parentElement, cs = getComputedStyle(parent);
      if (cs.display.includes('flex') || cs.display.includes('grid')) continue;
      const inner = parent.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
      const width = p.getBoundingClientRect().width;
      if (inner > 600 && width < inner * 0.8) {
        capped++;
        example = example || `${px(width)} of ${px(inner)}`;
      }
    }
    if (capped >= 3) found.push(['capped-text', `${capped} long paragraphs use under 80% of their column (e.g. ${example})`]);
  }

  if (vw <= 430) {
    for (const e of document.querySelectorAll('body *')) {
      const cs = getComputedStyle(e);
      if (cs.position !== 'fixed' && cs.position !== 'sticky') continue;
      const r = e.getBoundingClientRect();
      if (r.top <= 1 && r.width >= vw * 0.9 && r.height > vh * 0.16) {
        found.push(['tall-header', `a ${cs.position} header takes ${px(r.height)} (${Math.round(100 * r.height / vh)}% of the screen height)`]);
        break;
      }
    }
  }
  return found;
})()"""


def changed_pages(newer: Path | None) -> list[Path]:
    out = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "--untracked-files=all", "--", "docs"],
                         capture_output=True, text=True, check=True).stdout
    pages = []
    for line in out.splitlines():
        path = ROOT / line[3:].strip().strip('"').split(" -> ")[-1]
        if path.suffix != ".html" or path.name == "index.html" or not path.is_file():
            continue
        if newer and newer.exists() and path.stat().st_mtime <= newer.stat().st_mtime:
            continue
        pages.append(path)
    return sorted(pages, key=lambda p: p.stat().st_mtime, reverse=True)


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def start_server() -> tuple[socketserver.ThreadingTCPServer, str]:
    """Serve docs/ on a free local port; returns the server and its origin URL (with trailing slash)."""
    server = socketserver.ThreadingTCPServer(("127.0.0.1", 0), functools.partial(QuietHandler, directory=str(DOCS)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}/"


def launch_browser(pw):
    """Installed Chrome when available, else Playwright's bundled Chromium."""
    try:
        return pw.chromium.launch(channel="chrome")
    except Exception:
        return pw.chromium.launch()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pages", nargs="*", type=Path)
    ap.add_argument("--changed", action="store_true", help="check HTML pages under docs/ that differ from HEAD")
    ap.add_argument("--newer", type=Path, help="with --changed: only files modified after this file")
    ap.add_argument("--limit", type=int, default=0, help="check at most N pages (most recently modified first)")
    args = ap.parse_args()

    pages = [p.resolve() for p in args.pages]
    if args.changed:
        pages += changed_pages(args.newer)
    pages = [p for p in dict.fromkeys(pages) if p.is_relative_to(DOCS)]
    skipped = 0
    if args.limit and len(pages) > args.limit:
        skipped, pages = len(pages) - args.limit, pages[:args.limit]
    if not pages:
        return 0

    from playwright.sync_api import sync_playwright

    server, origin = start_server()

    failures = 0
    with sync_playwright() as pw:
        browser = launch_browser(pw)
        for path in pages:
            rel = path.relative_to(DOCS).as_posix()
            report = []
            for name, width, height in VIEWPORTS:
                page = browser.new_page(viewport={"width": width, "height": height})
                try:
                    # domcontentloaded, not load: figure-heavy pages can keep the load
                    # event pending well past the point where layout has settled.
                    page.goto(origin + rel, wait_until="domcontentloaded", timeout=30000)
                    page.wait_for_timeout(600)
                    page.evaluate("window.scrollTo(0, Math.min(1200, document.documentElement.scrollHeight / 3))")
                    page.wait_for_timeout(300)
                    report += [f"  {name} {width}px  {kind}: {text}" for kind, text in page.evaluate(PROBE)]
                except Exception as exc:
                    report.append(f"  {name} {width}px  error: {exc}")
                finally:
                    page.close()
            if report:
                failures += 1
                print(f"docs/{rel}")
                print("\n".join(report))
        browser.close()
    server.shutdown()
    if skipped:
        print(f"({skipped} more changed page(s) not checked; raise --limit to include them)")
    if failures:
        print(f"{failures} of {len(pages)} page(s) do not use the available space well.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
