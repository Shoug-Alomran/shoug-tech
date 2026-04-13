#!/usr/bin/env python3
"""Create legacy site aliases for old docs paths after deploy builds.

This preserves previously indexed URLs that used spaces while keeping the
source tree itself fully hyphenated.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
MAP_PATH = ROOT / "scripts" / "legacy-docs-path-map.json"


def docs_rel_to_site_path(rel: str) -> Path:
    path = Path(rel)
    name = path.name

    if name.endswith(".ar.md"):
        stem = name[: -len(".ar.md")]
        base = SITE / "ar" / path.parent
        return base / "index.html" if stem == "index" else base / stem / "index.html"

    if path.suffix == ".md":
        stem = path.stem
        base = SITE / path.parent
        return base / "index.html" if stem == "index" else base / stem / "index.html"

    return SITE / path


def site_path_to_url(path: Path) -> str:
    rel = path.relative_to(SITE).as_posix()
    if rel.endswith("/index.html"):
        route = rel[: -len("index.html")]
        return f"/{route}"
    return f"/{rel}"


def write_redirect(old_path: Path, new_url: str) -> None:
    old_path.parent.mkdir(parents=True, exist_ok=True)
    old_path.write_text(
        "\n".join(
            [
                "<!doctype html>",
                "<html lang=\"en\">",
                "<head>",
                "  <meta charset=\"utf-8\">",
                f"  <meta http-equiv=\"refresh\" content=\"0; url={new_url}\">",
                f"  <link rel=\"canonical\" href=\"{new_url}\">",
                "  <script>location.replace("
                + json.dumps(new_url)
                + ");</script>",
                "</head>",
                "<body>",
                f"  <p>Redirecting to <a href=\"{new_url}\">{new_url}</a>.</p>",
                "</body>",
                "</html>",
            ]
        ),
        encoding="utf-8",
    )


def main() -> int:
    if not MAP_PATH.exists() or not SITE.exists():
        return 0

    mapping = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    created_redirects = 0
    copied_assets = 0

    for old_rel, new_rel in mapping.items():
        old_site = docs_rel_to_site_path(old_rel)
        new_site = docs_rel_to_site_path(new_rel)

        if old_site == new_site or not new_site.exists():
            continue

        if old_site.suffix == ".html" and old_rel.endswith(".md"):
            write_redirect(old_site, site_path_to_url(new_site))
            created_redirects += 1
            continue

        old_site.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(new_site, old_site)
        copied_assets += 1

    print(f"[legacy-aliases] redirects: {created_redirects}")
    print(f"[legacy-aliases] copied assets: {copied_assets}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
