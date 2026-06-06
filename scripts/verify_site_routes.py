#!/usr/bin/env python3
"""Verify high-value generated routes exist after an MkDocs build."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
if not SITE.is_dir() and (ROOT / "docs").is_dir():
    SITE = ROOT / "docs"

REQUIRED_ROUTES = (
    "Academics/software-engineering/se201/",
    "Academics/software-engineering/se311/",
    "Academics/computer-science/cs340/",
    "Academics/cybersecurity/cys401/",
)


def route_to_index(route: str) -> Path:
    return SITE / route.strip("/") / "index.html"


def main() -> int:
    missing = [route for route in REQUIRED_ROUTES if not route_to_index(route).is_file()]

    if missing:
        for route in missing:
            print(f"[error] missing generated route: /{route}")
        return 1

    for route in REQUIRED_ROUTES:
        print(f"[ok] generated route: /{route}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
