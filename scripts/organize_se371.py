#!/usr/bin/env python3
"""Normalize SE371 resource paths and keep local example references working."""

from __future__ import annotations

import os
import filecmp
import html
import re
import shutil
import unicodedata
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "docs/academics/software-engineering/se371"
TEXT_EXTENSIONS = {".css", ".html", ".js", ".json", ".md", ".txt"}


def slug_component(name: str) -> str:
    if name in {"index.html", ".", ".."}:
        return name
    stem, suffix = os.path.splitext(name)
    stem = unicodedata.normalize("NFKD", stem).encode("ascii", "ignore").decode()
    stem = re.sub(r"_[0-9a-f]{24,}$", "", stem, flags=re.I)
    stem = re.sub(r"\bsoution\b", "solution", stem, flags=re.I)
    stem = re.sub(r"\bcheet[ _-]*sheet\b", "cheat-sheet", stem, flags=re.I)
    stem = re.sub(r"\bjavascript\b", "javascript", stem, flags=re.I)
    stem = re.sub(r"[^a-zA-Z0-9]+", "-", stem).strip("-").lower()
    stem = re.sub(r"-+", "-", stem)
    stem = stem.replace("cheet-sheet", "cheat-sheet").replace("11soution", "11-solution")
    return stem + suffix.lower()


def merge_directory(source: Path, target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    for child in source.iterdir():
        destination = target / child.name
        if destination.exists() and child.is_dir() and destination.is_dir():
            merge_directory(child, destination)
        elif destination.exists() and child.is_file() and destination.is_file() and filecmp.cmp(child, destination, shallow=False):
            child.unlink()
        elif not destination.exists():
            shutil.move(str(child), str(destination))
        else:
            raise FileExistsError(f"Cannot merge {child} into {destination}")
    source.rmdir()


def flatten_labs() -> None:
    labs = COURSE / "extra-resources/labs"
    nested = labs / "Labs"
    if not nested.exists():
        return
    nested_solutions = nested / "Solutions"
    if nested_solutions.exists():
        merge_directory(nested_solutions, labs / "solutions")
    merge_directory(nested, labs)


def normalize_paths() -> list[tuple[str, str]]:
    changes: list[tuple[str, str]] = []
    paths = sorted(COURSE.rglob("*"), key=lambda path: len(path.parts), reverse=True)
    for path in paths:
        if path.name == ".DS_Store":
            path.unlink()
            continue
        new_name = slug_component(path.name)
        if new_name == path.name:
            continue
        old_relative = path.relative_to(COURSE).as_posix()
        destination = path.with_name(new_name)
        if destination.exists():
            if destination.samefile(path):
                temporary = path.with_name(f".se371-rename-{path.name}")
                path.rename(temporary)
                path = temporary
            else:
                raise FileExistsError(f"Rename collision: {path} -> {destination}")
        path.rename(destination)
        new_relative = destination.relative_to(COURSE).as_posix()
        changes.append((old_relative, new_relative))
    return changes


def update_references(changes: list[tuple[str, str]]) -> None:
    replacements: dict[str, str] = {}
    for old, new in changes:
        old_name, new_name = old.rsplit("/", 1)[-1], new.rsplit("/", 1)[-1]
        if old_name != new_name:
            replacements[old_name] = new_name
            replacements[quote(old_name)] = quote(new_name)

    for path in COURSE.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        try:
            original = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        updated = original
        for old, new in sorted(replacements.items(), key=lambda pair: len(pair[0]), reverse=True):
            updated = updated.replace(old, new)
        if updated != original:
            path.write_text(updated, encoding="utf-8")


def title_from_slug(value: str) -> str:
    words = value.replace("-", " ").split()
    return " ".join(word.upper() if word in {"css", "dom", "ejs", "html", "js", "json", "pdf"} else word.title() for word in words)


def create_resource_indexes() -> None:
    resources = COURSE / "extra-resources"
    template = (resources / "index.html").read_text(encoding="utf-8")
    folder_icon = '<svg class="dir-folder-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square" stroke-linejoin="square" aria-hidden="true"><path d="M3 7a1 1 0 0 1 1-1h5l2 2h9a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V7z"/></svg>'
    icon_styles = '<style id="se371-folder-icons">.dir-title:has(.dir-folder-icon){display:flex;align-items:center;gap:10px}.dir-folder-icon{width:20px;height:20px;flex:0 0 auto;color:var(--text-tertiary);transition:color .2s ease,transform .2s ease}.dir-row:hover .dir-folder-icon{color:var(--brand-purple);transform:translateY(-1px)}</style>'
    if 'id="se371-folder-icons"' not in template:
        template = template.replace("</head>", f"{icon_styles}</head>")
        (resources / "index.html").write_text(template, encoding="utf-8")
    viewer_root = resources / "resource-viewers"
    directories = sorted((path for path in resources.rglob("*") if path.is_dir() and path != viewer_root and viewer_root not in path.parents), key=lambda path: len(path.parts), reverse=True)
    for directory in directories:
        index = directory / "index.html"
        if index.exists():
            existing = index.read_text(encoding="utf-8", errors="ignore")
            if "SE371 Web Engineering resources and downloadable course files." not in existing and 'id="se371-folder-icons"' not in existing:
                continue
        relative = directory.relative_to(ROOT / "docs").as_posix()
        title = title_from_slug(directory.name)
        items = []
        for number, child in enumerate(sorted((child for child in directory.iterdir() if not child.name.startswith(".") and child.name != "index.html"), key=lambda path: (not path.is_dir(), path.name)), 1):
            href = quote(child.name) + ("/" if child.is_dir() else "")
            label = title_from_slug(child.stem if child.is_file() else child.name)
            # Spell out the file type. Several folders sit next to an archive of
            # the same name (lab-03a-css-solution/ and lab-03a-css-solution.rar),
            # which otherwise renders as two identical rows.
            if child.is_file() and child.suffix.lower() not in {".html", ".htm"}:
                label += f" ({child.suffix.lstrip('.').upper()})"
            icon = folder_icon if child.is_dir() else ""
            items.append(f'<a class="dir-row" href="{href}"><div class="dir-num">{number:02d}</div><div class="dir-title"><span class="dir-title-text">{html.escape(label)}</span>{icon}</div><div class="dir-status"><span class="status-tag available">AVAILABLE</span></div><div class="dir-arrow">-&gt;</div></a>')
        canonical = f"https://shoug-tech.com/{relative}/"
        rows = f'<div class="directory-container"><div class="dir-header"><span>SEQ</span><span>DESCRIPTOR</span><span>SYS_STATE</span><span></span></div>{"".join(items)}</div>'
        page = template
        page = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)} | SE371 Web Engineering</title>", page, count=1, flags=re.S)
        page = re.sub(r'<meta name="description"[^>]*>', f'<meta name="description" content="Browse {html.escape(title)} resources for SE371 Web Engineering, including examples, exercises, and downloadable study files.">', page, count=1)
        page = re.sub(r'<link rel="canonical"[^>]*>', f'<link rel="canonical" href="{canonical}">', page, count=1)
        page = re.sub(r'<meta property="og:url"[^>]*>', f'<meta property="og:url" content="{canonical}">', page, count=1)
        page = page.replace('<span class="current" data-en-text="Study Material" data-ar-text="المواد الدراسية">Study Material</span>', f'<a class="breadcrumb-link" href="/academics/software-engineering/se371/extra-resources/">Study Material</a> / <span class="current">{html.escape(title)}</span>', 1)
        page = page.replace('<div class="type-label" data-en-text="STUDY MATERIAL" data-ar-text="المواد الدراسية">STUDY MATERIAL</div>', f'<div class="type-label">{html.escape(title)}</div>', 1)
        start = page.index('            <div class="directory-container"')
        end = page.index("\n\n\n    <footer", start)
        page = page[:start] + "            " + rows + page[end:]
        index.write_text(page, encoding="utf-8")


def enhance_resource_metadata() -> None:
    resources = COURSE / "extra-resources"
    for path in resources.rglob("*.html"):
        if path == resources / "index.html":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        relative = path.relative_to(ROOT / "docs").as_posix()
        route = "/" + relative.removesuffix("index.html")
        descriptor = title_from_slug(path.parent.name if path.name == "index.html" else path.stem)
        title = f"{descriptor} | SE371 Web Engineering Resource"
        description = f"Explore the {descriptor} example or study file for SE371 Web Engineering, with practical HTML, CSS, JavaScript, Node.js, and database course resources."
        if "<head" not in text.lower():
            head = f'<head><title>{html.escape(title)}</title><meta name="description" content="{html.escape(description, quote=True)}"><link rel="canonical" href="https://shoug-tech.com{route}"></head>'
            text = re.sub(r"(<html[^>]*>)", rf"\1{head}", text, count=1, flags=re.I)
        if re.search(r"<title>.*?</title>", text, flags=re.I | re.S):
            current = re.search(r"<title>(.*?)</title>", text, flags=re.I | re.S)
            if current and "SE371" not in current.group(1):
                text = text[:current.start()] + f"<title>{html.escape(title)}</title>" + text[current.end():]
        elif "<head" in text.lower():
            text = re.sub(r"(<head[^>]*>)", rf"\1<title>{html.escape(title)}</title>", text, count=1, flags=re.I)
        meta = f'<meta name="description" content="{html.escape(description, quote=True)}">'
        if re.search(r'<meta\s+name=["\']description["\'][^>]*>', text, flags=re.I):
            text = re.sub(r'<meta\s+name=["\']description["\'][^>]*>', meta, text, count=1, flags=re.I)
        else:
            text = re.sub(r"(<title>.*?</title>)", rf"\1\n{meta}", text, count=1, flags=re.I | re.S)
        if 'rel="canonical"' not in text:
            text = re.sub(r"(</title>)", rf'\1\n<link rel="canonical" href="https://shoug-tech.com{route}">', text, count=1, flags=re.I)
        path.write_text(text, encoding="utf-8")


def normalize_course_pages() -> None:
    for path in COURSE.glob("**/index.html"):
        text = path.read_text(encoding="utf-8")
        updated = text.replace("/Academics/software-engineering/se371", "/academics/software-engineering/se371")
        updated = updated.replace("/academics/software-engineering/se371/extra-resorces/", "/academics/software-engineering/se371/extra-resources/")
        if path == COURSE / "slides/index.html":
            updated = updated.replace('<span class="status-tag available">PDF</span>', '<span class="status-tag available">AVAILABLE</span>')
        if updated != text:
            path.write_text(updated, encoding="utf-8")


def main() -> None:
    flatten_labs()
    changes = normalize_paths()
    update_references(changes)
    normalize_course_pages()
    create_resource_indexes()
    enhance_resource_metadata()
    print(f"Normalized {len(changes)} SE371 paths.")


if __name__ == "__main__":
    main()
