"""HTML building blocks for CYS403 slide breakdowns.

Class names come from the CYS405 breakdown stylesheet that build_cys403_study_tools.py
clones, plus the bdx-* components in /styles/study-guide.css, so every block renders
with that page's theme in light and dark mode.
"""
import html
import re

ACCENTS = ["a", "b", "c", "d", "e", "f"]

# Line icons (no emoji), drawn with currentColor.
_ICON_PATHS = {
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>',
    "good": '<path d="M20 6 9 17l-5-5"/>',
    "exam": '<path d="M9 11l3 3 8-8"/><path d="M20 12v7a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h9"/>',
    "warn": '<path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/>',
    "brain": '<path d="M9.5 2a2.5 2.5 0 0 1 2.5 2.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24A2.5 2.5 0 0 1 9.5 2Z"/><path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24A2.5 2.5 0 0 0 14.5 2Z"/>',
}


def icon(name: str) -> str:
    return (f'<svg class="bdx-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_ICON_PATHS[name]}</svg>')


# kind -> (tip class, heading colour class, icon)
TIP_STYLES = {
    "info": ("tip-blue", "ta", "info"),
    "good": ("tip-green", "td", "good"),
    "exam": ("tip-yellow", "tf", "exam"),
    "warn": ("tip-warn", "te", "warn"),
}


def p(*paragraphs: str) -> str:
    return "".join(f"<p>{text}</p>" for text in paragraphs)


def ul(*items: str) -> str:
    return "<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"


def h3(text: str, accent: str = "a") -> str:
    return f'<h3 class="t{accent} bdx-sub">{text}</h3>'


def defs(*cards: tuple[str, str]) -> str:
    out = []
    for i, (term, desc) in enumerate(cards):
        accent = ACCENTS[i % len(ACCENTS)]
        out.append(f'<div class="def-card"><div class="def-top" style="background: var(--{accent})"></div>'
                   f'<div class="def-term t{accent}">{term}</div><div class="def-desc">{desc}</div></div>')
    return '<div class="def-grid">' + "".join(out) + "</div>"


def table(headers: list[str], *rows: list[str]) -> str:
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows)
    return f'<div class="tbl-wrap"><table class="tbl"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def steps(*items: tuple[str, str]) -> str:
    out = "".join(f'<div class="step"><div class="step-num">{i}</div><div class="step-body"><h4>{title}</h4>'
                  + (f"<p>{text}</p>" if text else "") + "</div></div>"
                  for i, (title, text) in enumerate(items, 1))
    return f'<div class="steps bdx-timeline">{out}</div>'


def tip(kind: str, title: str, text: str) -> str:
    cls, colour, glyph = TIP_STYLES[kind]
    return (f'<div class="tip {cls}"><div class="tip-icon">{icon(glyph)}</div>'
            f'<div class="tip-body"><h4 class="{colour}">{title}</h4><p>{text}</p></div></div>')


KEY_RE = re.compile(r'<span class="mnem-key">(.*?)</span>')
ACRONYM_RE = re.compile(r"^[A-Z](?:-[A-Z])+$")


def _pairs(text: str):
    """Split 'A = x; B = y' or 'A → x' fragments into (term, meaning) rows."""
    rows = []
    for part in re.split(r";\s+|,\s+(?=[A-Z<])", text.strip().rstrip(".")):
        m = re.match(r"(.+?)\s+(?:=|→)\s+(.+)", part)
        if not m:
            return []
        rows.append((m.group(1).strip(), m.group(2).strip()))
    return rows if len(rows) >= 2 else []


def _clean_note(rest: str) -> str:
    """Drop the connectors left behind once key() spans are lifted out ("and", ", then .")."""
    previous = None
    while previous != rest:
        previous = rest
        rest = re.sub(r"^(?:[\s,:;.=+]|and\b|then\b)+", "", rest).strip()
    leftover = re.sub(r"<[^>]+>|[\s,.;:]|\b(?:and|then)\b", "", rest)
    return rest if leftover else ""


def mnemonic(title: str, text: str) -> str:
    """A memory card: acronym letter tiles, step chains, a term → meaning list, and the note.

    Content is written as before (key() spans plus prose); the layout is derived
    from it so long one-line tricks read as structured cards.
    """
    keys = KEY_RE.findall(text)
    rest = _clean_note(KEY_RE.sub("", text))
    parts = []

    letters = next((k for k in keys if ACRONYM_RE.match(k)), None) or (title if ACRONYM_RE.match(title) else None)
    if letters:
        tiles = "".join(f'<span class="bdx-tile" style="--bdx-i:{i}">{c}</span>' for i, c in enumerate(letters.split("-")))
        parts.append(f'<div class="bdx-tiles" aria-hidden="true">{tiles}</div>')

    rows = []
    for k in keys:
        if k == letters:
            continue
        plain_key = re.sub(r"<[^>]+>", "", k)
        if plain_key.count("→") >= 2 or "·" in plain_key:
            sep = "→" if "→" in plain_key else "·"
            chips = [c for c in re.split(r"\s*(?:→|·)\s*", k) if c]
            joiner = f'<span class="bdx-chain-sep" aria-hidden="true">{sep}</span>'
            parts.append('<div class="bdx-chain">' + joiner.join(
                f'<span class="bdx-chip" style="--bdx-i:{i}">{c}</span>' for i, c in enumerate(chips)) + "</div>")
        elif m := re.match(r"(.+?)\s+(?:=|→)\s+(.+)", k):
            rows.append((m.group(1), m.group(2)))
        else:
            parts.append(f'<p class="bdx-phrase">{k}</p>')
    if not keys or keys == [letters]:
        note_rows = _pairs(re.sub(r"<[^>]+>", "", rest))
        if note_rows:
            rows, rest = note_rows, ""
    if rows:
        items = "".join(f'<li><span class="bdx-term">{t}</span><span class="bdx-arrow" aria-hidden="true">→</span>'
                        f'<span class="bdx-meaning">{m}</span></li>' for t, m in rows)
        parts.append(f'<ul class="bdx-pairs">{items}</ul>')
    if rest:
        parts.append(f'<p class="bdx-note">{rest}</p>')
    return (f'<div class="mnemonic bdx-memory"><div class="mnemonic-icon">{icon("brain")}</div>'
            f'<div class="mnemonic-body"><h4>Memory trick · {title}</h4>{"".join(parts)}</div></div>')


def key(text: str) -> str:
    return f'<span class="mnem-key">{text}</span>'


def flow(*boxes: str) -> str:
    styles = ["accent", "accent2", "accent3"]
    parts = []
    for i, box in enumerate(boxes):
        if i:
            parts.append('<div class="flow-arrow" aria-hidden="true"><span>→</span></div>')
        parts.append(f'<div class="flow-box {styles[i % len(styles)]}" style="--bdx-i:{i}">{box}</div>')
    return '<div class="flow bdx-flow">' + "".join(parts) + "</div>"


def vs(*panels: tuple[str, str, str]) -> str:
    """Side-by-side comparison panels: (label, body html, accent letter)."""
    out = "".join(f'<div class="ex ex-{accent}"><div class="ex-label t{accent}">{label}</div><p>{body}</p></div>'
                  for label, body, accent in panels)
    return f'<div class="vs">{out}</div>'


def formula(text: str) -> str:
    lines = "".join(f'<span class="bdx-line">{line}</span>' for line in text.split("<br>"))
    return f'<p class="mono bdx-formula"><span class="bdx-formula-label">Formula</span>{lines}</p>'


def figure(src: str, caption: str, width: int, height: int, slide: int, source: str = "") -> str:
    """A slide diagram; study-guide.js opens it full size when clicked.

    The caption's tag links back to the page of the slide deck the diagram came from.
    """
    alt = html.escape(plain(caption), quote=True)
    label = f"Slide {slide}"
    tag = (f'<a class="bdx-figure-tag" href="{html.escape(source, quote=True)}">{label}</a>' if source
           else f'<span class="bdx-figure-tag">{label}</span>')
    return (f'<figure class="bdx-figure"><button type="button" class="bdx-figure-zoom" aria-label="Enlarge figure: {alt}">'
            f'<img src="{src}" alt="{alt}" width="{width}" height="{height}" loading="lazy" decoding="async" /></button>'
            f'<figcaption>{tag}{caption}</figcaption></figure>')


def plain(text: str) -> str:
    """Section titles and table cells as plain text (for the contents panel and flashcards)."""
    return html.unescape(re.sub(r"<[^>]+>", "", text)).strip()
