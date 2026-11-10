#!/usr/bin/env python3
"""Find old page URLs that still have a real new home, for the indexing Worker.

Google keeps retrying URLs it once knew, so every renamed page lingers as a 404 in
Search Console. This reads renames and deletions from git history and writes
workers/indexing/src/legacy-redirects.json, which build_indexing_manifest.py merges.

A redirect is kept only when it is safe: the old path is gone, the destination
exists, it is the same course and the page name matches apart from case, number
prefix or hash suffix. Pages that really were removed stay 404, which is correct.

Needs full git history, so run it by hand and commit the result; never in CI:

    python3 scripts/build_legacy_redirects.py
"""
from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = ROOT / "workers" / "indexing" / "src" / "legacy-redirects.json"
PAGE = re.compile(r"\.(html|pdf|docx|pptx)$", re.I)
COURSE = re.compile(r"/([a-z]{2,6}\d{3})(?:/|$)")
# The paid course is gated by its own Worker, and old quiz URLs must not lead into it.
EXCLUDED = "/ethcs303"
# Renames still in the working tree, which git history cannot see yet.
MANUAL = {
    f"docs/workshops/psu-ctf/{p}index.html": f"docs/workshops/psu-ctf-2/{p}index.html"
    for p in ("", "agenda-workshops/", "challenges-resources/", "rules-faq/", "team-links/")
}


def current_files() -> set[str]:
    # Built from directory listings because path.exists() ignores case on macOS.
    found = set()
    for folder, _, names in os.walk(DOCS):
        rel = Path(folder).relative_to(ROOT).as_posix()
        found.update(f"{rel}/{name}" for name in names)
    return found


def to_url(path: str) -> str:
    url = "/" + path[len("docs/"):]
    return url[: -len("index.html")] if url.endswith("/index.html") else url


def slug(path: str) -> str:
    parts = path.split("/")
    name = parts[-2] if parts[-1].lower() == "index.html" else PAGE.sub("", parts[-1])
    name = re.sub(r"-[0-9a-f]{8}$", "", re.sub(r"^\d+[-_.\s]*", "", name.lower()))
    return re.sub(r"[^a-z0-9]+", "-", name).strip("-")


def course(path: str) -> str | None:
    match = COURSE.search(path.lower())
    return match.group(1) if match else None


def same_page(old: str, new: str) -> bool:
    return slug(old) == slug(new) and course(old) == course(new)


def git_paths(*args: str) -> list[str]:
    return subprocess.run(
        ["git", "log", "--reverse", "--name-status", "--format=", *args, "--", "docs"],
        cwd=ROOT, capture_output=True, text=True, check=True,
        env={**os.environ, "GIT_CONFIG_PARAMETERS": "'core.quotepath=false'"},
    ).stdout.splitlines()


def main() -> int:
    exists = current_files()
    moves = dict(MANUAL)
    for line in git_paths("--diff-filter=R", "-M", "-l0"):
        parts = line.split("\t")
        if len(parts) == 3 and PAGE.search(parts[1]) and same_page(parts[1], parts[2]):
            moves[parts[1]] = parts[2]

    def final(path: str) -> str:
        seen = set()
        while path in moves and path not in seen:
            seen.add(path)
            path = moves[path]
        return path

    deleted = {
        parts[1] for parts in (line.split("\t") for line in git_paths("--diff-filter=D", "--no-renames"))
        if len(parts) == 2 and PAGE.search(parts[1])
    }
    result = {}
    for old in set(moves) | deleted:
        dest = final(old)
        if dest == old or dest not in exists:
            # Case-only moves often appear as a delete plus an add.
            dest = "docs/" + old[len("docs/"):].lower()
        if old in exists or dest == old or dest not in exists:
            continue
        if EXCLUDED in old.lower() or EXCLUDED in dest.lower():
            continue
        result[to_url(old)] = quote(to_url(dest), safe="/")

    OUT.write_text(json.dumps(dict(sorted(result.items())), indent=0, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} with {len(result)} redirects")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
