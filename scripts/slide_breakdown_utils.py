#!/usr/bin/env python3
"""Filesystem rules shared by slide-breakdown repair and validation."""

from __future__ import annotations

import re
from pathlib import Path


def slide_breakdown_roots(academics: Path) -> list[Path]:
    return sorted(path for path in academics.rglob("slide-breakdowns") if path.is_dir())


def authored_html(folder: Path) -> list[Path]:
    """Return authored English HTML below a breakdown item, excluding wrappers."""
    return sorted(
        path for path in folder.rglob("*.html")
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
    """Find the authored HTML represented by an immediate child viewer folder."""
    candidates = authored_html(folder)
    if candidates:
        return _preferred_source(folder, candidates)
    if root is not None:
        root_candidates = [
            path for path in authored_html(root)
            if path.stem.lower() == re.sub(r"^\d+[-_]", "", folder.name).lower()
        ]
        if root_candidates:
            return _preferred_source(folder, root_candidates)
    return None