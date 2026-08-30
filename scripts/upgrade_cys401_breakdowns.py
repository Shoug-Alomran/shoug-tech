#!/usr/bin/env python3
"""Unify dark/light theming and inject the shared design layer into the
CYS401 slide-breakdown pages.

Every page ends up driven by html[data-theme], synced with the site theme
(localStorage 'shoug-theme') and with the embedding wrapper via postMessage.

Per page the fix differs:
  * media-query pages  -> each @media (prefers-color-scheme: X) block is
    duplicated as an explicit html[data-theme="X"] rule and the original
    query is guarded so an explicit choice always wins
  * variable pages with only one theme -> a generated counterpart block
  * hard-coded pages (no vars, no theme) -> neutral colours are detected by
    luminance and re-emitted as html[data-theme="dark"] overrides
"""
import colorsys
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "docs/academics/cybersecurity/cys401/slide-breakdowns"

ASSETS = (
    '\n    <link rel="stylesheet" href="/styles/breakdown.css">'
    '\n    <script src="/styles/breakdown-theme.js" defer></script>'
)

# ---------------------------------------------------------------- colour utils
HEX = re.compile(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b")

# the neutral keywords these pages actually use, normalised to hex so the
# same luminance logic applies to `background: white` as to `#ffffff`
KEYWORDS = {
    "white": "#ffffff", "black": "#000000", "whitesmoke": "#f5f5f5",
    "ghostwhite": "#f8f8ff", "snow": "#fffafa", "ivory": "#fffff0",
    "gainsboro": "#dcdcdc", "lightgray": "#d3d3d3", "lightgrey": "#d3d3d3",
    "silver": "#c0c0c0", "gray": "#808080", "grey": "#808080",
    "dimgray": "#696969", "dimgrey": "#696969",
}
KEYWORD_RE = re.compile(r"\b(%s)\b" % "|".join(KEYWORDS))


def hex_to_hsl(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    hu, li, sa = colorsys.rgb_to_hls(r, g, b)
    return hu, sa, li


def is_neutral(h):
    """True for greys, near-whites and near-blacks — the colours that must
    flip between themes. Saturated brand colours are left untouched."""
    _, s, l = hex_to_hsl(h)
    if s < 0.22:                 # true greys
        return True
    if l > 0.93 or l < 0.10:     # near-white / near-black
        return True
    # desaturated slate used for body copy (#2c3e50, #34495e, #4a5568 …)
    return l < 0.42 and s < 0.45


def token_for(h, prop, sel_is_page=False):
    """Map a neutral colour to the shared token that replaces it in dark mode."""
    _, _, l = hex_to_hsl(h)
    if prop.startswith("border") or prop == "outline-color":
        return "var(--bd-border)"
    if "background" in prop:
        if sel_is_page:
            return "var(--bd-bg)"
        if l > 0.95:
            return "var(--bd-surface)"
        if l > 0.86:
            return "var(--bd-surface-2)"
        if l > 0.70:
            return "var(--bd-bg-alt)"
        return "var(--bd-bg)"
    # text colours
    if l < 0.30:
        return "var(--bd-text)"
    if l < 0.62:
        return "var(--bd-text-dim)"
    return "var(--bd-text-dim)"



FILLISH = ("progress", "fill", "-bar", "bar-", "indicator", "dot", "gauge", "meter")


def to_hex(hu, sa, li):
    r, g, b = colorsys.hls_to_rgb(hu, li, sa)
    return "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))


def dark_tint(h):
    """A pale callout wash (#fff3cd) becomes a deep wash of the same hue."""
    hu, sa, _ = hex_to_hsl(h)
    return to_hex(hu, min(max(sa, 0.30), 0.55), 0.145)


def lighten_ink(h):
    """Dark saturated body text inside a callout, raised for a dark wash."""
    hu, sa, _ = hex_to_hsl(h)
    return to_hex(hu, min(max(sa, 0.35), 0.70), 0.74)


# ---------------------------------------------------------------- css helpers
def block_end(css, start):
    """Index just past the '}' closing the block whose '{' is at start-1."""
    depth, i = 1, start
    while i < len(css) and depth:
        if css[i] == "{":
            depth += 1
        elif css[i] == "}":
            depth -= 1
        i += 1
    return i


def split_rules(body):
    """Yield (selector, declarations) for top-level rules inside a media body."""
    i, out = 0, []
    while i < len(body):
        brace = body.find("{", i)
        if brace == -1:
            break
        sel = body[i:brace].strip()
        end = block_end(body, brace + 1)
        out.append((sel, body[brace + 1:end - 1]))
        i = end
    return out


def scope(sel, theme):
    """Prefix a selector so it only applies under an explicit theme choice."""
    attr = 'html[data-theme="%s"]' % theme
    parts = []
    for one in sel.split(","):
        one = one.strip()
        if not one:
            continue
        if one in (":root", "html", "body"):
            parts.append(attr if one != "body" else attr + " body")
        else:
            parts.append(attr + " " + one)
    return ", ".join(parts)


def guard(sel, other):
    """Prefix a selector so the OS-driven copy stops applying once the reader
    has explicitly chosen the opposite theme."""
    g = 'html:not([data-theme="%s"])' % other
    parts = []
    for one in sel.split(","):
        one = one.strip()
        if not one:
            continue
        if one in (":root", "html"):
            parts.append(g)
        elif one == "body":
            parts.append(g + " body")
        else:
            parts.append(g + " " + one)
    return ", ".join(parts)


def dualise_media(css):
    """Duplicate every prefers-color-scheme block as an explicit data-theme
    rule, and guard the original so an explicit choice overrides the OS."""
    out, i, added = [], 0, 0
    pat = re.compile(r"@media\s*\(\s*prefers-color-scheme\s*:\s*(dark|light)\s*\)\s*\{")
    while True:
        m = pat.search(css, i)
        if not m:
            out.append(css[i:])
            break
        theme = m.group(1)
        other = "light" if theme == "dark" else "dark"
        body_start = m.end()
        body_end = block_end(css, body_start)
        body = css[body_start:body_end - 1]
        rules = split_rules(body)

        out.append(css[i:m.start()])
        # OS-driven copy — every rule guarded against an explicit opposite choice
        guarded = "".join("%s{%s}\n" % (guard(sel, other), decls) for sel, decls in rules)
        out.append("@media (prefers-color-scheme: %s) {\n%s}\n" % (theme, guarded))
        # explicit copy — wins whenever the reader has chosen
        out.append("".join("%s{%s}\n" % (scope(sel, theme), decls) for sel, decls in rules))
        added += 1
        i = body_end
    return "".join(out), added


def counterpart_vars(block_body, theme):
    """Build the opposite-theme variable block from a single-theme one."""
    lines = []
    for m in re.finditer(r"(--[\w-]+)\s*:\s*([^;]+);", block_body):
        name, val = m.group(1), m.group(2).strip()
        hexes = HEX.findall(val)
        if not hexes:
            continue
        new = val
        for h in hexes:
            if not is_neutral(h):
                continue
            _, s, l = hex_to_hsl(h)
            # mirror the lightness across the midpoint, keep the hue
            hu, sa = hex_to_hsl(h)[0], s
            nl = 1.0 - l
            if theme == "dark":
                nl = min(nl, 0.16) if l > 0.75 else nl
            else:
                nl = max(nl, 0.90) if l < 0.25 else nl
            r, g, b = colorsys.hls_to_rgb(hu, nl, min(sa, 0.25))
            new = new.replace(h, "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255)))
        if new != val:
            lines.append("    %s: %s;" % (name, new))
    if not lines:
        return ""
    return 'html[data-theme="%s"] {\n%s\n}\n' % (theme, "\n".join(lines))


def hardcoded_dark(css):
    """For pages with no variables at all: emit dark overrides for every rule
    that sets a neutral colour."""
    rules = []
    i = 0
    while i < len(css):
        brace = css.find("{", i)
        if brace == -1:
            break
        sel = css[i:brace].strip()
        end = block_end(css, brace + 1)
        decls = css[brace + 1:end - 1]
        i = end
        if sel.startswith("@") or not sel:
            continue
        keep = []
        for dm in re.finditer(r"([a-z-]+)\s*:\s*([^;]+);?", decls):
            prop, val = dm.group(1), dm.group(2).strip()
            if "gradient" in val or "var(" in val:
                continue
            if prop not in ("color", "background", "background-color", "border", "border-color",
                            "border-top", "border-bottom", "border-left", "border-right"):
                continue
            norm = KEYWORD_RE.sub(lambda m: KEYWORDS[m.group(1)], val)
            hexes = HEX.findall(norm)
            if len(hexes) != 1:
                continue
            h = hexes[0]
            low = sel.lower()
            if is_neutral(h):
                # a white fill sitting on an accent track must stay bright
                if "background" in prop and hex_to_hsl(h)[2] > 0.9 and any(k in low for k in FILLISH):
                    continue
                page = sel.strip() in ("body", "html", "html, body", "body, html")
                keep.append("%s: %s;" % (prop, norm.replace(h, token_for(h, prop, page))))
            elif "background" in prop and hex_to_hsl(h)[2] > 0.85:
                # pale coloured callout wash -> deep wash of the same hue
                keep.append("%s: %s;" % (prop, norm.replace(h, dark_tint(h))))
                ink = re.search(r"(?:^|;)\s*color\s*:\s*(#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b)", decls)
                if ink and hex_to_hsl(ink.group(1))[2] < 0.5:
                    keep.append("color: %s;" % lighten_ink(ink.group(1)))
                elif not ink:
                    keep.append("color: var(--bd-text);")
        if keep:
            rules.append('html[data-theme="dark"] %s { %s }' % (sel, " ".join(keep)))
    return "\n".join(rules)


# ---------------------------------------------------------------- page config
# mode: 'media'  -> dualise prefers-color-scheme blocks
#       'gen'    -> generate the missing counterpart from the :root vars
#       'hard'   -> no vars at all, derive dark overrides from literals
#       'sync'   -> already has both data-theme blocks, only needs the assets
PAGES = [
    ("01-chapter-1-introduction-to-cybersecurity/chapter-1.html", "sync", None),
    ("02-chapter-2-security-foundations-and-principles/chapter-2.html", "sync", None),
    ("03-chapter-3-threat-modeling/chapter-3.html", "media", None),
    ("04-chapter-4-protection-of-information-assets/chapter-4.html", "media", None),
    ("05-chapter-5-cryptography/chapter-5.html", "sync", None),
    ("06-chapter-6-asymmetric-cryptography-and-pki/chapter-6.html", "sync", None),
    ("07-chapter-7-principles-of-security-design-models-and-capabilities/chapter-7.html", "media", None),
    ("08-chapter-8-security-vulnerabilities-threats-and-countermeasures/"
     "security-vulnerabilities-threats-and-countermeasures.html", "sync", None),
    ("09-chapter-9-ics-scada-system-security/ics-scada-system-security.html", "gen", "light"),
    ("10-chapter-10-authentication-and-access-control/authentication-and-access-control.html", "gen", "dark"),
]


# Hand-tuned counterpart palettes. Mechanical lightness mirroring produces
# muddy results for these two designs (a neon-on-navy page and a warm paper
# page), so the opposite theme is authored rather than derived.
PALETTES = {
    "ics-scada-system-security.html": ("light", """
    --bg: #f2f6fb;
    --surface: #ffffff;
    --surface2: #e9f1fa;
    --accent: #0679a3;
    --accent2: #d1500f;
    --accent3: #157f3c;
    --accent4: #9a7400;
    --danger: #c81e45;
    --text: #0b1a2b;
    --muted: #4d6480;
    --border: rgba(6, 121, 163, 0.22);
"""),
    "authentication-and-access-control.html": ("dark", """
    --bg: #14120f;
    --surface: #1c1a16;
    --card: #24211c;
    --border: #35302a;
    --amber: #e8912f;
    --amber-light: #f3b761;
    --amber-dark: #f5c37a;
    --teal: #2fb8b8;
    --teal-light: #0e2e2e;
    --rose: #e46a6c;
    --rose-light: #331718;
    --indigo: #8f87ea;
    --indigo-light: #1a1830;
    --green: #4cba6c;
    --green-light: #12291a;
    --text: #ece8e1;
    --muted: #a3998b;
    --shadow: 0 2px 14px rgba(0, 0, 0, 0.5);
"""),
}

MARK = "/* bd-upgraded */"


def first_root_body(css):
    m = re.search(r":root\s*\{", css)
    if not m:
        return None
    end = block_end(css, m.end())
    return css[m.end():end - 1]


def patch(path, mode, gen_theme):
    p = BASE / path
    s = p.read_text(encoding="utf-8")
    name = p.name
    if MARK in s:
        print("  %-46s already upgraded — refreshing" % name)
        s = re.sub(r"\n<style>%s.*?</style>" % re.escape(MARK), "", s, flags=re.S)
    # strip the shared assets unconditionally: pages that need no generated
    # style block carry no MARK, and would otherwise collect a link per run
    s = s.replace(ASSETS, "")
    s = re.sub(r'\s*<link rel="stylesheet" href="/styles/breakdown\.css">', "", s)
    s = re.sub(r'\s*<script src="/styles/breakdown-theme\.js" defer></script>', "", s)

    notes = []

    # 1. resolve the theme before first paint so nothing flashes
    s = re.sub(r'\s*<script>/\* bd-init \*/.*?</script>', "", s, flags=re.S)
    init = ("\n    <script>/* bd-init */(function(){try{var v=localStorage.getItem('shoug-theme');"
            "if(v!=='light'&&v!=='dark'){v=(window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches)"
            "?'dark':'light';}var d=document.documentElement;d.setAttribute('data-theme',v);"
            "d.style.colorScheme=v;}catch(e){}})();</script>")
    s = re.sub(r'(<head[^>]*>)', lambda m: m.group(1) + init, s, count=1)

    # 2. theme repair
    styles = list(re.finditer(r"<style[^>]*>(.*?)</style>", s, re.S))
    css_all = "".join(m.group(1) for m in styles)
    extra = ""

    if mode == "media":
        new_css, n = dualise_media(styles[0].group(1))
        s = s[:styles[0].start(1)] + new_css + s[styles[0].end(1):]
        notes.append("%d media block(s) mirrored to data-theme" % n)
    elif mode == "gen":
        theme, decls = PALETTES[name]
        extra += 'html[data-theme="%s"] {%s}\n' % (theme, decls)
        notes.append("hand-tuned %s palette applied" % theme)
        if theme == "dark":
            leftovers = hardcoded_dark(css_all)
            if leftovers:
                extra += leftovers + "\n"
                notes.append("%d literal leftovers covered" % leftovers.count("{"))
    elif mode == "hard":
        overrides = hardcoded_dark(css_all)
        if overrides:
            extra += overrides + "\n"
            notes.append("%d dark override rules derived" % overrides.count("{"))
    else:
        notes.append("already dual-theme, synced only")

    # dark pages that declare their palette on :root need it under light too
    if mode == "gen" and gen_theme == "light":
        body = first_root_body(css_all)
        if body:
            extra = 'html[data-theme="dark"] {%s}\n' % body + extra

    if extra:
        s = s.replace("</head>", "<style>%s\n%s</style>\n</head>" % (MARK, extra), 1)

    # 3. shared assets last so tokens and chrome win
    s = s.replace("</head>", ASSETS + "\n</head>", 1)

    p.write_text(s, encoding="utf-8")
    print("  %-46s %s" % (name, "; ".join(notes)))


def patch_wrappers():
    """Make each viewer pass its theme down to the embedded iframe."""
    snippet = """
<script>
(function(){
  function theme(){ return document.body.classList.contains('shoug-light-mode') ? 'light' : 'dark'; }
  function push(){
    var f = document.querySelector('.embed-container iframe');
    if (f && f.contentWindow) f.contentWindow.postMessage({type:'shoug-theme', theme: theme()}, '*');
  }
  var f = document.querySelector('.embed-container iframe');
  if (f) f.addEventListener('load', push);
  var btn = document.querySelector('.shoug-theme-btn');
  if (btn) btn.addEventListener('click', function(){ setTimeout(push, 30); });
  window.addEventListener('message', function(e){
    if (!e.data || e.data.type !== 'shoug-theme') return;
    document.body.classList.toggle('shoug-light-mode', e.data.theme === 'light');
    try { localStorage.setItem('shoug-theme', e.data.theme); } catch(err){}
  });
})();
</script>
"""
    n = 0
    for idx in sorted(BASE.glob("*/index.html")):
        s = idx.read_text(encoding="utf-8")
        if "shoug-theme', theme: theme()" in s or "embed-container" not in s:
            continue
        s = s.replace("</body>", snippet + "</body>", 1)
        idx.write_text(s, encoding="utf-8")
        n += 1
    print("  wrappers wired for theme hand-off: %d" % n)


if __name__ == "__main__":
    print("Upgrading CYS401 slide breakdowns…")
    for path, mode, gen in PAGES:
        patch(path, mode, gen)
    patch_wrappers()
    print("Done.")
