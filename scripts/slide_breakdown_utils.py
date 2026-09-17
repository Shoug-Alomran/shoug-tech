#!/usr/bin/env python3
"""Filesystem rules shared by slide-breakdown repair and validation."""

from __future__ import annotations

import re
from pathlib import Path


def slide_breakdown_roots(academics: Path) -> list[Path]:
    return sorted(path for path in academics.rglob("slide-breakdowns") if path.is_dir())


def authored_html(folder: Path) -> list[Path]:
    """Return authored English HTML directly inside one breakdown item.

    Deliberately do not recurse: figures, mindmaps, cheat-sheets and other
    nested support directories are not standalone viewer items.
    """
    if not folder.is_dir():
        return []
    return sorted(
        path for path in folder.glob("*.html")
        if path.name.lower() != "index.html" and not path.name.lower().endswith(".ar.html")
    )


def _preferred_source(folder: Path, candidates: list[Path]) -> Path:
    slug_tail = re.sub(r"^\d+[-_]", "", folder.name).lower()
    preferred = [
        path for path in candidates
        if path.stem.lower() in {
            slug_tail,
            slug_tail.replace("-", "_"),
            slug_tail.split("-")[0],
        }
    ]
    return max(preferred or candidates, key=lambda path: path.stat().st_size)


def breakdown_source(folder: Path, root: Path | None = None) -> Path | None:
    """Find the authored HTML represented by a dedicated viewer folder.

    A folder is available when it contains a sibling authored HTML file.  The
    optional root fallback supports older layouts where the authored file sits
    directly in slide-breakdowns while the viewer is in a numbered folder.
    """
    candidates = authored_html(folder)
    if candidates:
        return _preferred_source(folder, candidates)
    if root is not None:
        slug = re.sub(r"^\d+[-_]", "", folder.name).lower()
        root_candidates = [
            path for path in authored_html(root)
            if path.stem.lower() == slug
        ]
        if root_candidates:
            return _preferred_source(folder, root_candidates)
    return None
