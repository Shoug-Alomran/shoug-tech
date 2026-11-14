#!/usr/bin/env python3
"""Copy the site CV into the CV repo that serves cv.shoug-tech.com.

docs/career-development/cv.html is the one CV to edit. cv.shoug-tech.com (the
Shoug-Alomran/CV repo, a Vite site on GitHub Pages) serves the same page at
/cv/, so the version sent to employers never drifts from the site's.

    python3 scripts/sync_cv_subdomain.py ~/path/to/CV-repo [--pdf]

The copy drops what only exists on shoug-tech.com (site shell CSS, palette
and service-worker scripts, Clarity, hreflang), points favicons at the repo's
own /favicon.png and its URLs at https://cv.shoug-tech.com/cv/. With --pdf it
also prints public/cv/Shoug-Alomran-CV.pdf with headless Chrome.
"""
from __future__ import annotations

import argparse
import functools
import http.server
import re
import subprocess
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "docs" / "career-development" / "cv.html"
SITE_URL = "https://shoug-tech.com/career-development/cv.html"
COPY_URL = "https://cv.shoug-tech.com/cv/"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

DROP = [
    r'\s*<script src="/javascripts/translation-launch-guard\.js"></script>',
    r'\s*<!-- Microsoft Clarity tracking code[^>]*-->\s*<script type="text/javascript">[\s\S]*?</script>',
    r'\s*<link rel="stylesheet" href="/styles/a11y\.css" />',
    r'\s*<link rel="manifest" href="/site\.webmanifest" />',
    r'\s*<link rel="stylesheet" href="/styles/site-shell\.css" />',
    r'\s*<script defer src="/javascripts/site-palette\.js"></script>',
    r'\s*<script src="/javascripts/register-sw\.js" defer></script>',
    r'\s*<link\s+rel="alternate"\s+hreflang="[^"]+"\s+href="[^"]+"\s*/>',
]

# The page's screen-reader-only <h1> uses this class from the site shell.
VISUALLY_HIDDEN = """    <style>
      .shoug-visually-hidden {
        position: absolute !important;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border: 0;
      }
    </style>
  </head>"""


def build_copy(html: str) -> str:
    html = html.replace("/assets/shoug-favicon-v4.png", "/favicon.png")
    html = html.replace("/assets/shoug-apple-touch-icon-v4.png", "/favicon.png")
    for pattern in DROP:
        html = re.sub(pattern, "", html)
    html = html.replace(SITE_URL, COPY_URL)
    if html.count("  </head>") != 1:
        sys.exit("expected exactly one </head> in the CV")
    html = html.replace("  </head>", VISUALLY_HIDDEN, 1)
    leftovers = re.findall(r'(?:src|href)="/(?!favicon\.png)[^"]*"', html)
    if leftovers:
        sys.exit(f"site-relative references left in the copy: {leftovers}")
    return html


def print_pdf(public: Path) -> Path:
    """Serve public/ locally and print /cv/ to PDF with reduced motion, so the
    duration count-up is already at its final values."""
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    handler = functools.partial(Quiet, directory=str(public))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    out = public / "cv" / "Shoug-Alomran-CV.pdf"
    try:
        subprocess.run(
            [
                CHROME,
                "--headless=new",
                "--disable-gpu",
                "--no-pdf-header-footer",
                "--force-prefers-reduced-motion",
                "--virtual-time-budget=4000",
                f"--print-to-pdf={out}",
                f"http://127.0.0.1:{server.server_port}/cv/index.html",
            ],
            check=True,
            capture_output=True,
        )
    finally:
        server.shutdown()
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("repo", type=Path, help="checkout of Shoug-Alomran/CV")
    parser.add_argument("--pdf", action="store_true", help="also print the PDF")
    args = parser.parse_args()

    public = args.repo / "public"
    if not (public / "CNAME").exists():
        sys.exit(f"{args.repo} does not look like the CV repo (no public/CNAME)")

    copy = build_copy(SOURCE.read_text(encoding="utf-8"))
    for target in (public / "cv" / "index.html", args.repo / "docs" / "cv" / "index.html"):
        if target.parent.exists():
            target.write_text(copy, encoding="utf-8")
            print(f"wrote {target}")
    if args.pdf:
        print(f"wrote {print_pdf(public)}")


if __name__ == "__main__":
    main()
