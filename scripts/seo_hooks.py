"""MkDocs hooks for page-specific SEO metadata."""

from __future__ import annotations

import html
import re
from pathlib import Path


GENERIC_TITLES = {"overview", "intro", "introduction", "home", "index"}
MAX_DESCRIPTION_LENGTH = 155


def clean_text(value: str) -> str:
    value = html.unescape(value)
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"`([^`]+)`", r"\1", value)
    value = re.sub(r"[*_~#>`]+", " ", value)
    value = re.sub(r":[a-z0-9_+-]+:", " ", value, flags=re.IGNORECASE)
    value = value.replace("&nbsp;", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip(" -\t\n\r")


def strip_front_matter(markdown: str) -> str:
    if not markdown.startswith("---"):
        return markdown

    parts = markdown.split("---", 2)
    if len(parts) == 3:
        return parts[2]
    return markdown


def first_heading(markdown: str) -> str | None:
    for line in strip_front_matter(markdown).splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            title = clean_text(match.group(1))
            if title:
                return title
    return None


def first_paragraph(markdown: str) -> str | None:
    lines = strip_front_matter(markdown).splitlines()
    paragraph: list[str] = []

    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            if paragraph:
                break
            continue

        if line.startswith("#"):
            continue
        if line.startswith(("---", "```", "<div", "</div", "<span", "<a ", "<iframe")):
            continue
        if line.startswith(("-", "*", "|", "!!!", "???")):
            if paragraph:
                break
            continue

        paragraph.append(line)

    text = clean_text(" ".join(paragraph))
    return text or None


def readable_path_title(page) -> str:
    source = Path(page.file.src_path)
    parts = [part for part in source.with_suffix("").parts if part not in {"docs", "index"}]
    label = " ".join(parts[-3:])
    label = label.replace("-", " ").replace("_", " ")
    label = re.sub(r"\b([A-Z]{2,}\d{3})\b", r"\1", label)
    return clean_text(label.title())


def trim_description(description: str) -> str:
    description = clean_text(description)
    if len(description) <= MAX_DESCRIPTION_LENGTH:
        return description

    trimmed = description[: MAX_DESCRIPTION_LENGTH + 1].rsplit(" ", 1)[0]
    return f"{trimmed.rstrip('.,;: -')}."


def on_page_markdown(markdown, page, config, files):
    meta = page.meta
    heading = first_heading(markdown)

    current_title = clean_text(str(meta.get("title") or page.title or ""))
    if not current_title or current_title.lower() in GENERIC_TITLES:
        meta["title"] = heading or readable_path_title(page)

    if not meta.get("description"):
        paragraph = first_paragraph(markdown)
        if paragraph:
            meta["description"] = trim_description(paragraph)
        else:
            title = clean_text(str(meta.get("title") or heading or readable_path_title(page)))
            meta["description"] = trim_description(
                f"{title} from Shoug's Digital Garden, a structured knowledge base for software engineering, cybersecurity, and computer science study resources."
            )

    return markdown
