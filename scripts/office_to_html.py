#!/usr/bin/env python3
"""Render .docx and .xlsx into HTML fragments, with no third-party libraries.

Office files are ZIP archives of XML, so the parts we need (text, headings,
lists, tables, images, sheet cells) can be read with the standard library.
This is deliberately a readable-content converter, not a layout-faithful one:
the goal is that an activity sheet can be read on the site instead of being
downloaded, while the original file stays one click away.
"""

from __future__ import annotations

import base64
import html
import os
import re
import zipfile
from xml.etree import ElementTree

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
PKG_REL = "{http://schemas.openxmlformats.org/package/2006/relationships}"
S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"

IMAGE_TYPES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
               ".gif": "image/gif", ".bmp": "image/bmp", ".svg": "image/svg+xml"}
# Images are inlined so a generated viewer folder stays a single index.html.
MAX_INLINE_IMAGE = 1_500_000


class ConversionError(RuntimeError):
    pass


# --------------------------------------------------------------------------- #
# shared helpers
# --------------------------------------------------------------------------- #

def _rels(zf: zipfile.ZipFile, part: str) -> dict[str, str]:
    """relationship id -> target, resolved against the part's folder."""
    folder, name = os.path.split(part)
    rel_path = f"{folder}/_rels/{name}.rels"
    if rel_path not in zf.namelist():
        return {}
    out = {}
    for rel in ElementTree.fromstring(zf.read(rel_path)):
        target = rel.get("Target", "")
        if rel.get("TargetMode") == "External":
            out[rel.get("Id")] = target
        else:
            out[rel.get("Id")] = os.path.normpath(os.path.join(folder, target)).replace(os.sep, "/")
    return out


def _data_uri(zf: zipfile.ZipFile, path: str) -> str | None:
    mime = IMAGE_TYPES.get(os.path.splitext(path)[1].lower())
    if not mime or path not in zf.namelist():
        return None
    blob = zf.read(path)
    if len(blob) > MAX_INLINE_IMAGE:
        return None
    return f"data:{mime};base64,{base64.b64encode(blob).decode('ascii')}"


# --------------------------------------------------------------------------- #
# docx
# --------------------------------------------------------------------------- #

def _numbering_formats(zf: zipfile.ZipFile) -> dict[str, str]:
    """numId -> 'decimal' or 'bullet' (level 0 only; nested levels reuse it)."""
    if "word/numbering.xml" not in zf.namelist():
        return {}
    root = ElementTree.fromstring(zf.read("word/numbering.xml"))
    abstract = {}
    for node in root.findall(f"{W}abstractNum"):
        fmt = node.find(f"{W}lvl/{W}numFmt")
        abstract[node.get(f"{W}abstractNumId")] = (fmt.get(f"{W}val") if fmt is not None else "bullet")
    out = {}
    for node in root.findall(f"{W}num"):
        ref = node.find(f"{W}abstractNumId")
        if ref is not None:
            out[node.get(f"{W}numId")] = abstract.get(ref.get(f"{W}val"), "bullet")
    return out


def _runs(node, zf, rels) -> str:
    """Inline content of a paragraph or table cell."""
    out = []
    for child in node:
        tag = child.tag
        if tag == f"{W}hyperlink":
            inner = _runs(child, zf, rels)
            target = rels.get(child.get(f"{R}id", ""))
            if inner and target and target.startswith(("http://", "https://", "mailto:")):
                out.append(f'<a href="{html.escape(target, quote=True)}" rel="noopener noreferrer" '
                           f'target="_blank">{inner}</a>')
            else:
                out.append(inner)
            continue
        if tag != f"{W}r":
            continue
        props = child.find(f"{W}rPr")
        text = []
        for part in child:
            if part.tag == f"{W}t":
                text.append(html.escape(part.text or ""))
            elif part.tag == f"{W}tab":
                text.append(" ")
            elif part.tag == f"{W}br":
                text.append("<br />")
            elif part.tag in (f"{W}drawing", f"{W}pict"):
                for blip in part.iter(f"{A}blip"):
                    uri = _data_uri(zf, rels.get(blip.get(f"{R}embed", ""), ""))
                    if uri:
                        text.append(f'<img src="{uri}" alt="" loading="lazy" />')
        piece = "".join(text)
        if not piece:
            continue
        if props is not None:
            for tag_name, wrap in ((f"{W}b", "strong"), (f"{W}i", "em"), (f"{W}u", "u"),
                                   (f"{W}strike", "s")):
                el = props.find(tag_name)
                if el is not None and el.get(f"{W}val") not in ("0", "false"):
                    piece = f"<{wrap}>{piece}</{wrap}>"
        out.append(piece)
    return "".join(out)


def _cell_html(cell, zf, rels) -> str:
    parts = []
    for child in cell:
        if child.tag == f"{W}p":
            inner = _runs(child, zf, rels)
            if inner:
                parts.append(inner)
        elif child.tag == f"{W}tbl":
            parts.append(_table_html(child, zf, rels))
    return "<br />".join(parts) if parts else "&nbsp;"


def _table_html(table, zf, rels) -> str:
    rows = table.findall(f"{W}tr")
    if not rows:
        return ""
    out = ['<div class="doc-table-wrap"><table class="doc-table">']
    for index, row in enumerate(rows):
        cells = row.findall(f"{W}tc")
        if not cells:
            continue
        tag = "th" if index == 0 else "td"
        out.append("<tr>")
        for cell in cells:
            span = cell.find(f"{W}tcPr/{W}gridSpan")
            attr = f' colspan="{span.get(f"{W}val")}"' if span is not None else ""
            out.append(f"<{tag}{attr}>{_cell_html(cell, zf, rels)}</{tag}>")
        out.append("</tr>")
    out.append("</table></div>")
    return "".join(out)


def docx_to_html(path: str) -> str:
    """Readable HTML for a .docx file."""
    try:
        with zipfile.ZipFile(path) as zf:
            if "word/document.xml" not in zf.namelist():
                raise ConversionError("not a Word document")
            rels = _rels(zf, "word/document.xml")
            numbering = _numbering_formats(zf)
            body = ElementTree.fromstring(zf.read("word/document.xml")).find(f"{W}body")
            if body is None:
                raise ConversionError("document has no body")

            out: list[str] = []
            open_list: str | None = None

            def close_list():
                nonlocal open_list
                if open_list:
                    out.append(f"</{open_list}>")
                    open_list = None

            for node in body:
                if node.tag == f"{W}tbl":
                    close_list()
                    out.append(_table_html(node, zf, rels))
                    continue
                if node.tag != f"{W}p":
                    continue
                props = node.find(f"{W}pPr")
                style = ""
                if props is not None:
                    ref = props.find(f"{W}pStyle")
                    style = (ref.get(f"{W}val") if ref is not None else "") or ""
                inner = _runs(node, zf, rels)
                num = props.find(f"{W}numPr/{W}numId") if props is not None else None
                if num is not None:
                    kind = "ol" if numbering.get(num.get(f"{W}val")) == "decimal" else "ul"
                    if open_list != kind:
                        close_list()
                        out.append(f"<{kind}>")
                        open_list = kind
                    out.append(f"<li>{inner or '&nbsp;'}</li>")
                    continue
                close_list()
                if not inner.strip():
                    continue
                low = style.lower()
                if low in ("title",):
                    out.append(f"<h1>{inner}</h1>")
                elif low.startswith("heading"):
                    level = re.sub(r"\D", "", low) or "2"
                    out.append(f"<h{min(int(level) + 1, 6)}>{inner}</h{min(int(level) + 1, 6)}>")
                else:
                    out.append(f"<p>{inner}</p>")
            close_list()
            return "\n".join(out) or "<p>This document has no readable text content.</p>"
    except zipfile.BadZipFile as exc:
        raise ConversionError(f"unreadable file: {exc}") from exc


# --------------------------------------------------------------------------- #
# xlsx
# --------------------------------------------------------------------------- #

def _column_index(ref: str) -> int:
    letters = re.match(r"[A-Z]+", ref or "")
    if not letters:
        return 0
    index = 0
    for char in letters.group():
        index = index * 26 + (ord(char) - 64)
    return index - 1


def _shared_strings(zf: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in zf.namelist():
        return []
    root = ElementTree.fromstring(zf.read("xl/sharedStrings.xml"))
    return ["".join(node.text or "" for node in item.iter(f"{S}t")) for item in root.findall(f"{S}si")]


def xlsx_to_html(path: str) -> str:
    """Readable HTML tables for a .xlsx workbook, one per sheet."""
    try:
        with zipfile.ZipFile(path) as zf:
            if "xl/workbook.xml" not in zf.namelist():
                raise ConversionError("not an Excel workbook")
            strings = _shared_strings(zf)
            rels = _rels(zf, "xl/workbook.xml")
            book = ElementTree.fromstring(zf.read("xl/workbook.xml"))

            out = []
            sheets = book.findall(f"{S}sheets/{S}sheet")
            for sheet in sheets:
                target = rels.get(sheet.get(f"{R}id", ""))
                if not target or target not in zf.namelist():
                    continue
                grid: list[list[str]] = []
                for row in ElementTree.fromstring(zf.read(target)).iter(f"{S}row"):
                    cells: list[str] = []
                    for cell in row.findall(f"{S}c"):
                        at = _column_index(cell.get("r", ""))
                        while len(cells) < at:
                            cells.append("")
                        kind = cell.get("t")
                        if kind == "s":
                            value = cell.find(f"{S}v")
                            text = strings[int(value.text)] if value is not None and value.text else ""
                        elif kind == "inlineStr":
                            text = "".join(n.text or "" for n in cell.iter(f"{S}t"))
                        else:
                            value = cell.find(f"{S}v")
                            text = (value.text or "") if value is not None else ""
                        cells.append(text)
                    grid.append(cells)

                while grid and not any(c.strip() for c in grid[-1]):
                    grid.pop()
                if not grid:
                    continue
                width = max(len(r) for r in grid)
                # Sheets are padded out with blank columns/rows that would
                # otherwise squeeze the real text into a sliver of the table.
                keep = [i for i in range(width)
                        if any(i < len(r) and r[i].strip() for r in grid)]
                if not keep:
                    continue
                grid = [[(r[i] if i < len(r) else "") for i in keep] for r in grid]
                grid = [r for r in grid if any(c.strip() for c in r)]
                width = len(keep)
                name = html.escape(sheet.get("name") or "Sheet")
                if len(sheets) > 1:
                    out.append(f"<h2>{name}</h2>")
                out.append('<div class="doc-table-wrap"><table class="doc-table">')
                for index, row in enumerate(grid):
                    padded = row + [""] * (width - len(row))
                    tag = "th" if index == 0 else "td"
                    filled = [i for i, cell in enumerate(padded) if cell.strip()]
                    if len(filled) == 1 and filled[0] == 0 and width > 1:
                        # A merged banner row (a title across the sheet): span it
                        # rather than trailing blank cells after the text.
                        out.append(f'<tr><{tag} colspan="{width}">'
                                   f'{html.escape(padded[0])}</{tag}></tr>')
                        continue
                    out.append("<tr>" + "".join(
                        f"<{tag}>{html.escape(cell) or '&nbsp;'}</{tag}>" for cell in padded) + "</tr>")
                out.append("</table></div>")
            return "\n".join(out) or "<p>This workbook has no readable cells.</p>"
    except zipfile.BadZipFile as exc:
        raise ConversionError(f"unreadable file: {exc}") from exc


def convert(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".docx":
        return docx_to_html(path)
    if ext == ".xlsx":
        return xlsx_to_html(path)
    raise ConversionError(f"unsupported extension: {ext}")


if __name__ == "__main__":
    import sys
    for arg in sys.argv[1:]:
        print(f"--- {arg}")
        print(convert(arg)[:2000])
