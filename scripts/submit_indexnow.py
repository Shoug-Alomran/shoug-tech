#!/usr/bin/env python3
"""Submit changed site URLs to IndexNow after a successful deployment."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
HOST = "shoug-tech.com"
SITE_URL = f"https://{HOST}"
KEY = "411b4d7bc13843ca8290bfa526fbf823"
KEY_FILE = DOCS / f"{KEY}.txt"
KEY_URL = f"{SITE_URL}/{KEY}.txt"
ENDPOINT = "https://api.indexnow.org/indexnow"
MAX_BATCH = 10_000
NON_FATAL_HTTP_STATUSES = {403, 429}


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, check=True, text=True, capture_output=True
    )
    return result.stdout


def page_url(relative_path: str) -> str | None:
    if not relative_path.startswith("docs/") or not relative_path.endswith(".html"):
        return None
    path = relative_path.removeprefix("docs/")
    if path == "index.html":
        return f"{SITE_URL}/"
    if path.endswith("/index.html"):
        return f"{SITE_URL}/{path.removesuffix('index.html')}"
    return f"{SITE_URL}/{path}"


def changed_urls(before: str, after: str) -> list[str]:
    if not before or set(before) == {"0"}:
        return []

    output = run_git("diff", "--name-status", before, after, "--", "docs")
    urls: set[str] = set()
    for line in output.splitlines():
        fields = line.split("\t")
        if len(fields) < 2:
            continue
        # Renames include old and new paths; both matter because IndexNow also
        # notifies search engines about deleted/moved URLs.
        for path in fields[1:]:
            url = page_url(path)
            if url:
                urls.add(url)
    return sorted(urls)


def sitemap_urls() -> list[str]:
    sitemap = DOCS / "sitemap.xml"
    root = ET.parse(sitemap).getroot()
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = {
        node.text.strip()
        for node in root.findall("sm:url/sm:loc", namespace)
        if node.text and node.text.strip().startswith(f"{SITE_URL}/")
    }
    return sorted(urls)


def key_was_added(before: str) -> bool:
    if not before or set(before) == {"0"}:
        return True
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{before}:docs/{KEY}.txt"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode != 0


def verify_live_key(attempts: int = 6) -> None:
    expected = KEY_FILE.read_text(encoding="utf-8").strip()
    if expected != KEY:
        raise RuntimeError("Local IndexNow key file content does not match its filename")

    for attempt in range(1, attempts + 1):
        result = subprocess.run(
            [
                "curl",
                "--fail",
                "--silent",
                "--show-error",
                "--location",
                "--max-time",
                "20",
                KEY_URL,
            ],
            capture_output=True,
        )
        actual = result.stdout.decode("utf-8", errors="replace").strip()
        if result.returncode == 0 and actual == KEY:
            print(f"[ok] verified live IndexNow key: {KEY_URL}")
            return
        if attempt < attempts:
            print(f"[wait] IndexNow key is not live yet ({attempt}/{attempts})")
            time.sleep(10)
    raise RuntimeError(f"IndexNow key was not verifiable at {KEY_URL}")


def submit(urls: list[str], dry_run: bool) -> None:
    if not urls:
        print("[ok] no changed HTML URLs to submit")
        return

    print(f"[info] prepared {len(urls)} IndexNow URL(s)")
    if dry_run:
        for url in urls[:20]:
            print(f"  {url}")
        if len(urls) > 20:
            print(f"  ... {len(urls) - 20} more")
        return

    verify_live_key()
    for offset in range(0, len(urls), MAX_BATCH):
        batch = urls[offset : offset + MAX_BATCH]
        payload = json.dumps(
            {
                "host": HOST,
                "key": KEY,
                "keyLocation": KEY_URL,
                "urlList": batch,
            }
        ).encode("utf-8")
        result = subprocess.run(
            [
                "curl",
                "--silent",
                "--show-error",
                "--output",
                "/dev/null",
                "--write-out",
                "%{http_code}",
                "--request",
                "POST",
                "--header",
                "Content-Type: application/json; charset=utf-8",
                "--data-binary",
                "@-",
                ENDPOINT,
            ],
            input=payload,
            capture_output=True,
        )
        if result.returncode != 0:
            error = result.stderr.decode("utf-8", errors="replace").strip()
            raise RuntimeError(f"IndexNow request failed: {error}")
        status_text = result.stdout.decode("ascii", errors="replace").strip()
        status = int(status_text) if status_text.isdigit() else 0
        if status in NON_FATAL_HTTP_STATUSES:
            print(
                f"[warn] IndexNow returned HTTP {status}; "
                "skipping notification without failing deploy"
            )
            continue
        if status not in {200, 202}:
            raise RuntimeError(f"IndexNow returned unexpected HTTP {status}")
        print(f"[ok] IndexNow accepted {len(batch)} URL(s): HTTP {status}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--before", default="")
    parser.add_argument("--after", default="HEAD")
    parser.add_argument("--all", action="store_true", help="submit sitemap URLs")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    use_sitemap = args.all or key_was_added(args.before)
    urls = sitemap_urls() if use_sitemap else changed_urls(args.before, args.after)
    submit(urls, args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
