#!/usr/bin/env python3
"""Create legacy site aliases for old docs paths after deploy builds.

This preserves previously indexed URLs that used spaces while keeping the
source tree itself fully hyphenated.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
MAP_PATH = ROOT / "scripts" / "legacy-docs-path-map.json"
ASSET_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".pdf", ".pptx"}


def case_sensitive_exists(path: Path) -> bool:
    """Return true only when each path component exists with exact casing."""
    try:
        path.relative_to(ROOT)
    except ValueError:
        return path.exists()

    current = path.anchor and Path(path.anchor) or Path(".")
    for part in path.parts[1:] if path.is_absolute() else path.parts:
        if not current.exists():
            return False
        try:
            names = {child.name for child in current.iterdir()}
        except OSError:
            return False
        if part not in names:
            return False
        current = current / part

    return True


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


def normalize_rel(rel: str) -> str:
    """Normalize legacy/current paths so safe rename pairs compare equally."""
    parts = rel.replace("\\", "/").split("/")
    normalized_parts: list[str] = []

    for part in parts:
        # Normalize Arabic filename suffix variants like `page.ar.html` vs `page-ar.html`.
        part = re.sub(r"\.ar(?=\.(?:md|html)$)", "-ar", part)

        if "." in part:
            stem, ext = part.rsplit(".", 1)
            stem = re.sub(r"[\s_-]+", "-", stem.strip()).strip("-").lower()
            normalized_parts.append(f"{stem}.{ext.lower()}")
        else:
            part = re.sub(r"[\s_-]+", "-", part.strip()).strip("-").lower()
            normalized_parts.append(part)

    return "/".join(normalized_parts)


def load_manual_mapping() -> dict[str, str]:
    if not MAP_PATH.exists():
        return {}

    raw_mapping = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    return {old: new for old, new in raw_mapping.items() if old != new}


def load_git_rename_mapping() -> dict[str, str]:
    """Derive legacy aliases from git rename history for docs/ files.

    We only accept rename pairs whose normalized old/new paths still match after
    space/hyphen cleanup. This keeps genuine filename migrations while rejecting
    noisy rename-detection false positives from git history.
    """

    try:
        output = subprocess.check_output(
            ["git", "log", "--name-status", "--diff-filter=R", "--format="],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=15,
        )
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return {}

    rename_map: dict[str, str] = {}

    for line in output.splitlines():
        if not line.startswith("R"):
            continue

        parts = line.split("\t")
        if len(parts) != 3:
            continue

        _, old_raw, new_raw = parts
        if not old_raw.startswith("docs/") or not new_raw.startswith("docs/"):
            continue

        old_rel = old_raw[len("docs/") :]
        new_rel = new_raw[len("docs/") :]

        if (ROOT / "docs" / old_rel).exists():
            continue
        if not (ROOT / "docs" / new_rel).exists():
            continue
        if normalize_rel(old_rel) != normalize_rel(new_rel):
            continue

        rename_map.setdefault(old_rel, new_rel)

    return rename_map


def split_component(part: str) -> tuple[str, str]:
    if part.endswith(".ar.md"):
        return part[: -len(".ar.md")], ".ar.md"
    if part.endswith(".ar.html"):
        return part[: -len(".ar.html")], ".ar.html"
    if part.endswith("-ar.html"):
        return part[: -len("-ar.html")], ".ar.html"
    if part.endswith("-ar.md"):
        return part[: -len("-ar.md")], ".ar.md"
    if "." in part:
        stem, ext = part.rsplit(".", 1)
        return stem, f".{ext}"
    return part, ""


def legacy_component_variant(part: str, *, title_case: bool) -> str:
    stem, suffix = split_component(part)
    stem = stem.replace("-", " ")
    if title_case and stem == stem.lower():
        stem = stem.title()
    return f"{stem}{suffix}"


def legacy_spaced_dash_component_variant(part: str) -> str:
    """Return legacy titles like `Chapter 4 - Quiz` for hyphenated stems."""
    stem, suffix = split_component(part)
    stem = stem.replace("-", " ")
    stem = re.sub(r"(?<=\d) (?=[A-Za-z])", " - ", stem)
    return f"{stem}{suffix}"


def load_spacing_heuristic_mapping() -> dict[str, str]:
    """Fallback aliases for common space-to-hyphen filename migrations."""

    heuristic_map: dict[str, str] = {}

    for path in (ROOT / "docs").rglob("*"):
        if not path.is_file():
            continue

        rel = path.relative_to(ROOT / "docs").as_posix()
        parts = rel.split("/")

        candidates: set[str] = set()

        for title_case in (False, True):
            candidate = "/".join(
                legacy_component_variant(part, title_case=title_case) for part in parts
            )
            candidates.add(candidate)

        candidates.add("/".join(legacy_spaced_dash_component_variant(part) for part in parts))

        candidates.add(
            "/".join([*parts[:-1], legacy_component_variant(parts[-1], title_case=True)])
        )

        if len(parts) >= 2:
            candidates.add(
                "/".join(
                    [
                        *parts[:-2],
                        legacy_component_variant(parts[-2], title_case=True),
                        legacy_component_variant(parts[-1], title_case=True),
                    ]
                )
            )

            if parts[-2].lower() == "quizez":
                candidates.add(
                    "/".join(
                        [
                            *parts[:-2],
                            legacy_component_variant(parts[-2], title_case=True),
                            legacy_spaced_dash_component_variant(parts[-1]),
                        ]
                    )
                )

        # Preserve the old `.ar.html` suffix style for standalone Arabic HTML pages.
        if rel.endswith("-ar.html"):
            candidates.add(rel[: -len("-ar.html")] + ".ar.html")

        for candidate in candidates:
            if candidate == rel:
                continue
            if case_sensitive_exists(ROOT / "docs" / candidate):
                continue
            heuristic_map.setdefault(candidate, rel)

    return heuristic_map


def write_redirect_for_markdown_alias(rel: str) -> bool:
    path = Path(rel)
    name = path.name

    if name.endswith(".ar.md"):
        stem = name[: -len(".ar.md")]
        old_site = SITE / "ar" / path.parent / f"{stem}.html"
    elif path.suffix == ".md":
        old_site = SITE / path.parent / f"{path.stem}.html"
    else:
        return False

    new_site = docs_rel_to_site_path(rel)
    if old_site.exists() or not new_site.exists():
        return False

    write_redirect(old_site, site_path_to_url(new_site))
    return True


def write_ar_asset_mirror(rel: str) -> bool:
    path = Path(rel)
    if path.suffix.lower() not in ASSET_SUFFIXES:
        return False
    if rel.startswith("ar/"):
        return False

    new_site = SITE / rel
    old_site = SITE / "ar" / rel

    if old_site.exists() or not new_site.exists():
        return False

    old_site.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(new_site, old_site)
    return True


def write_legacy_route_redirect(old_route: str, new_rel: str) -> bool:
    old_site = SITE / old_route.strip("/") / "index.html"
    new_site = docs_rel_to_site_path(new_rel)

    if old_site.exists() or not new_site.exists():
        return False

    write_redirect(old_site, site_path_to_url(new_site))
    return True


def write_root_policy_redirects() -> int:
    redirects = 0
    policies = ("academic-disclaimer", "copyright", "privacy-notice")

    for slug in policies:
        pairs = (
            (slug, f"policy/{slug}.md"),
            (f"ar/{slug}", f"policy/{slug}.ar.md"),
        )
        for old_route, new_rel in pairs:
            if write_legacy_route_redirect(old_route, new_rel):
                redirects += 1

    return redirects


def main() -> int:
    if not SITE.exists():
        return 0

    mapping = load_git_rename_mapping()
    mapping.update(load_spacing_heuristic_mapping())
    mapping.update(load_manual_mapping())

    if not mapping:
        print("[legacy-aliases] no legacy mappings found")
        return 0

    created_redirects = 0
    copied_assets = 0

    for old_rel, new_rel in mapping.items():
        old_site = docs_rel_to_site_path(old_rel)
        new_site = docs_rel_to_site_path(new_rel)

        if old_site == new_site or not new_site.exists():
            continue
        try:
            if old_site.exists() and old_site.samefile(new_site):
                continue
        except OSError:
            pass

        if new_rel.endswith((".md", ".ar.md", ".html")):
            write_redirect(old_site, site_path_to_url(new_site))
            created_redirects += 1
            continue

        old_site.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(new_site, old_site)
        copied_assets += 1

    for path in (ROOT / "docs").rglob("*"):
        if not path.is_file():
            continue

        rel = path.relative_to(ROOT / "docs").as_posix()

        if write_redirect_for_markdown_alias(rel):
            created_redirects += 1

        if write_ar_asset_mirror(rel):
            copied_assets += 1

    created_redirects += write_root_policy_redirects()

    print(f"[legacy-aliases] mappings: {len(mapping)}")
    print(f"[legacy-aliases] redirects: {created_redirects}")
    print(f"[legacy-aliases] copied assets: {copied_assets}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
