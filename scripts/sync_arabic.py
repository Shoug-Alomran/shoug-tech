#!/usr/bin/env python3
"""
Generate Arabic Markdown files (*.ar.md) from English Markdown files (*.md).

Safety first:
- Dry-run by default
- Doesn't overwrite existing Arabic files unless --update-existing is provided
- Optional backups before overwrite

Requires:
- OPENAI_API_KEY environment variable
Optional:
- OPENAI_MODEL (default: gpt-4.1-mini)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Dict, Iterable, List, Tuple
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


CACHE_FILE = Path(".translation-cache-ar.json")
SYSTEM_PROMPT = (
    "You are a professional Arabic localization editor for a Saudi audience. "
    "Translate English Markdown to Saudi-friendly formal Arabic. "
    "Use clear, natural Arabic suitable for university students in Saudi Arabia. "
    "Keep the same Markdown structure exactly: headings, bullet levels, numbering, "
    "tables, links, references, and spacing patterns. "
    "Do not add commentary. Output only the translated Markdown. "
    "Do not translate code blocks, inline code, URLs, file paths, product names, "
    "course codes, abbreviations (e.g., CS340, SQL, API), and command-line snippets."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync Arabic .ar.md files from English .md files."
    )
    parser.add_argument("--docs-dir", default="docs", help="Docs root directory")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write changes to disk (default is dry-run)",
    )
    parser.add_argument(
        "--update-existing",
        action="store_true",
        help="Also update existing .ar.md files when source changed",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force translation even when source hash did not change",
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Create .bak copy before overwriting existing .ar.md files",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Process only N files (0 means all)",
    )
    parser.add_argument(
        "--sleep-ms",
        type=int,
        default=250,
        help="Sleep between API calls in milliseconds",
    )
    return parser.parse_args()


def is_english_markdown(path: Path) -> bool:
    name = path.name
    if not name.endswith(".md"):
        return False
    if name.endswith(".ar.md"):
        return False
    return True


def find_english_files(docs_dir: Path) -> List[Path]:
    files: List[Path] = []
    for path in docs_dir.rglob("*.md"):
        if is_english_markdown(path):
            files.append(path)
    return sorted(files)


def arabic_path_for(path: Path) -> Path:
    return path.with_name(path.stem + ".ar.md")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_cache() -> Dict[str, str]:
    if not CACHE_FILE.exists():
        return {}
    try:
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_cache(cache: Dict[str, str]) -> None:
    CACHE_FILE.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def split_front_matter(markdown: str) -> Tuple[str, str]:
    # Preserve YAML front matter as-is if present
    if not markdown.startswith("---\n"):
        return "", markdown
    match = re.match(r"^---\n.*?\n---\n", markdown, re.DOTALL)
    if not match:
        return "", markdown
    front = match.group(0)
    body = markdown[len(front) :]
    return front, body


def call_openai_translate(
    api_key: str,
    model: str,
    english_markdown: str,
) -> str:
    body = {
        "model": model,
        "input": [
            {"role": "system", "content": [{"type": "text", "text": SYSTEM_PROMPT}]},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Translate this Markdown to Arabic now:\n\n"
                            f"{english_markdown}"
                        ),
                    }
                ],
            },
        ],
    }
    payload = json.dumps(body).encode("utf-8")
    req = Request(
        "https://api.openai.com/v1/responses",
        data=payload,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    try:
        with urlopen(req, timeout=120) as resp:
            raw = resp.read().decode("utf-8")
    except HTTPError as e:
        err = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"OpenAI HTTP {e.code}: {err}") from e
    except URLError as e:
        raise RuntimeError(f"OpenAI request failed: {e}") from e

    data = json.loads(raw)

    # Primary path for Responses API
    text = data.get("output_text")
    if isinstance(text, str) and text.strip():
        return text

    # Fallback parse for nested output chunks
    output = data.get("output", [])
    chunks: List[str] = []
    for item in output:
        content = item.get("content", [])
        for piece in content:
            if piece.get("type") == "output_text":
                chunks.append(piece.get("text", ""))
    joined = "".join(chunks).strip()
    if joined:
        return joined

    raise RuntimeError("OpenAI response did not include translated text.")


def should_process(
    src: Path,
    dst: Path,
    src_hash: str,
    cache: Dict[str, str],
    update_existing: bool,
    force: bool,
) -> bool:
    key = str(src)
    if force:
        return True
    if not dst.exists():
        return True
    if not update_existing:
        return False
    return cache.get(key) != src_hash


def main() -> int:
    args = parse_args()
    docs_dir = Path(args.docs_dir)
    if not docs_dir.exists():
        print(f"Docs directory not found: {docs_dir}")
        return 1

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip()
    if args.apply and not api_key:
        print("Missing OPENAI_API_KEY in environment.")
        print("Set it and re-run with --apply.")
        return 1

    cache = load_cache()
    english_files = find_english_files(docs_dir)
    if args.limit > 0:
        english_files = english_files[: args.limit]

    planned = 0
    created = 0
    updated = 0
    skipped = 0
    failed = 0

    for src in english_files:
        dst = arabic_path_for(src)
        src_text = src.read_text(encoding="utf-8")
        src_hash = sha256_text(src_text)
        if not should_process(
            src=src,
            dst=dst,
            src_hash=src_hash,
            cache=cache,
            update_existing=args.update_existing,
            force=args.force,
        ):
            skipped += 1
            continue

        planned += 1
        action = "create" if not dst.exists() else "update"
        print(f"[plan] {action}: {dst}")
        if not args.apply:
            continue

        try:
            front_matter, body = split_front_matter(src_text)
            translated_body = call_openai_translate(api_key=api_key, model=model, english_markdown=body)
            output = front_matter + translated_body

            if dst.exists() and args.backup:
                backup = dst.with_suffix(dst.suffix + ".bak")
                backup.write_text(dst.read_text(encoding="utf-8"), encoding="utf-8")

            dst.write_text(output, encoding="utf-8")
            cache[str(src)] = src_hash
            if action == "create":
                created += 1
            else:
                updated += 1
            time.sleep(max(args.sleep_ms, 0) / 1000.0)
        except Exception as exc:
            failed += 1
            print(f"[error] {src}: {exc}")

    if args.apply:
        save_cache(cache)

    print("")
    print("Summary:")
    print(f"- Source English files: {len(english_files)}")
    print(f"- Planned translations: {planned}")
    print(f"- Created: {created}")
    print(f"- Updated: {updated}")
    print(f"- Skipped: {skipped}")
    print(f"- Failed: {failed}")
    print(f"- Mode: {'apply' if args.apply else 'dry-run'}")

    return 1 if failed > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
