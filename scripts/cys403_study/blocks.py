"""HTML building blocks for CYS403 slide breakdowns.

Class names come from the CYS405 breakdown stylesheet that build_cys403_study_tools.py
clones, so every block renders with that page's theme in light and dark mode.
"""

ACCENTS = ["a", "b", "c", "d", "e", "f"]
# kind -> (tip class, heading colour class, icon). Icons are plain glyphs, not emoji.
TIP_STYLES = {
    "info": ("tip-blue", "ta", "i"),
    "good": ("tip-green", "td", "✓"),
    "exam": ("tip-yellow", "tf", "#"),
    "warn": ("tip-warn", "te", "!"),
}


def p(*paragraphs: str) -> str:
    return "".join(f"<p>{text}</p>" for text in paragraphs)


def ul(*items: str) -> str:
    return "<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"


def h3(text: str, accent: str = "a") -> str:
    return f'<h3 class="t{accent}">{text}</h3>'


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
    out = "".join(f'<div class="step"><div class="step-num">{i}</div><div class="step-body"><h4>{title}</h4><p>{text}</p></div></div>'
                  for i, (title, text) in enumerate(items, 1))
    return f'<div class="steps">{out}</div>'


def tip(kind: str, title: str, text: str) -> str:
    cls, colour, icon = TIP_STYLES[kind]
    return (f'<div class="tip {cls}"><div class="tip-icon">{icon}</div>'
            f'<div class="tip-body"><h4 class="{colour}">{title}</h4><p>{text}</p></div></div>')


def mnemonic(title: str, text: str) -> str:
    return (f'<div class="mnemonic"><div class="mnemonic-icon">M</div>'
            f'<div class="mnemonic-body"><h4>{title}</h4><p>{text}</p></div></div>')


def key(text: str) -> str:
    return f'<span class="mnem-key">{text}</span>'


def flow(*boxes: str) -> str:
    styles = ["accent", "accent2", "accent3"]
    parts = []
    for i, box in enumerate(boxes):
        if i:
            parts.append('<div class="flow-arrow">→</div>')
        parts.append(f'<div class="flow-box {styles[i % len(styles)]}">{box}</div>')
    return '<div class="flow">' + "".join(parts) + "</div>"


def vs(*panels: tuple[str, str, str]) -> str:
    """Side-by-side comparison panels: (label, body html, accent letter)."""
    out = "".join(f'<div class="ex ex-{accent}"><div class="ex-label t{accent}">{label}</div><p>{body}</p></div>'
                  for label, body, accent in panels)
    return f'<div class="vs">{out}</div>'


def formula(text: str) -> str:
    return f'<p class="mono">{text}</p>'
