#!/usr/bin/env python3
"""Give each CYS401 slide-breakdown page a palette and background motif drawn
from the subject it teaches, instead of an arbitrary per-page colour scheme.

Runs after upgrade_cys401_breakdowns.py and layers on top of it: the block is
injected last in <head> so it wins over both the page's own CSS and the shared
breakdown.css tokens. Idempotent — re-running replaces the previous block.
"""
import colorsys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "docs/academics/cybersecurity/cys401/slide-breakdowns"
MARK = "/* bd-topic */"


# ------------------------------------------------------------------ colour ---
def hsl(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    hu, li, sa = colorsys.rgb_to_hls(r, g, b)
    return hu, sa, li


def hexof(hu, sa, li):
    r, g, b = colorsys.hls_to_rgb(hu, li, sa)
    return "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))


def lift(h, li=0.66, sa_min=0.55):
    """Brighter sibling of an accent, for use on a dark ground."""
    hu, sa, _ = hsl(h)
    return hexof(hu, max(sa, sa_min), li)


def rgba(h, a):
    h = h.lstrip("#")
    return "rgba(%d, %d, %d, %s)" % (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


# ------------------------------------------------------------------ motifs ---
def motif(kind, c, a):
    """Background-image texture for a chapter, tinted with its own accent."""
    t = rgba(c, a)
    return {
        # concentric shields — layered defence
        "shield": "repeating-radial-gradient(circle at 50%% -10%%, %s 0 1px, transparent 1px 74px)" % t,
        # hazard tape — threats and malware
        "hazard": "repeating-linear-gradient(45deg, %s 0 2px, transparent 2px 24px)" % t,
        # node lattice — attack trees and STRIDE
        "lattice": "radial-gradient(%s 1px, transparent 1px)" % t,
        # ledger rules — records, retention, classification
        "ledger": "repeating-linear-gradient(0deg, %s 0 1px, transparent 1px 36px)" % t,
        # cipher columns — substitution and transposition
        "cipher": "repeating-linear-gradient(90deg, %s 0 1px, transparent 1px 19px)" % t,
        # mirrored pair — public key / private key
        "keypair": ("radial-gradient(ellipse 40%% 60%% at 0%% 30%%, %s, transparent 70%%), "
                    "radial-gradient(ellipse 40%% 60%% at 100%% 70%%, %s, transparent 70%%)" % (t, t)),
        # blueprint grid — architecture and models
        "blueprint": ("repeating-linear-gradient(0deg, %s 0 1px, transparent 1px 30px), "
                      "repeating-linear-gradient(90deg, %s 0 1px, transparent 1px 30px)" % (t, t)),
        # stacked bands — the layer-by-layer countermeasure chapter
        "strata": "repeating-linear-gradient(0deg, %s 0 2px, transparent 2px 96px)" % t,
        # chevrons — industrial / plant floor
        "chevron": "repeating-linear-gradient(135deg, %s 0 6px, transparent 6px 28px)" % t,
        # ridges — fingerprints and biometrics
        "ridges": "repeating-radial-gradient(circle at 88%% 10%%, %s 0 1px, transparent 1px 15px)" % t,
    }[kind]


# ------------------------------------------------------------------ themes ---
# accents are authored for a light ground; dark variants are derived
THEMES = {
    "01-chapter-1-introduction-to-cybersecurity/chapter-1.html": dict(
        subject="Introduction · CIA triad, defence in depth",
        accents=["#1f6feb", "#0e7490", "#3b82c4"],
        motif="shield",
    ),
    "02-chapter-2-security-foundations-and-principles/chapter-2.html": dict(
        subject="Threats, malware, social engineering",
        accents=["#c0392b", "#d97706", "#8c2f39"],
        motif="hazard",
    ),
    "03-chapter-3-threat-modeling/chapter-3.html": dict(
        subject="Threat modelling · STRIDE, attack trees",
        accents=["#a855f7", "#e11d90", "#22d3ee", "#22c55e", "#f97316"],
        motif="lattice",
        motif_size="26px 26px",
        vars=["--neon-purple", "--neon-pink", "--neon-cyan", "--neon-green", "--neon-orange"],
    ),
    "04-chapter-4-protection-of-information-assets/chapter-4.html": dict(
        subject="Information assets · governance, classification",
        accents=["#0f766e", "#b45309", "#0e7490", "#7c5e10", "#155e75"],
        motif="ledger",
        vars=["--accent1", "--accent2", "--accent3", "--accent4", "--accent5"],
        grads=5,
    ),
    "05-chapter-5-cryptography/chapter-5.html": dict(
        subject="Cryptography · ciphers and hashing",
        accents=["#16a34a", "#0d9488", "#65a30d", "#0891b2", "#4d7c0f", "#059669"],
        motif="cipher",
        vars=["--a", "--b", "--c", "--d", "--e", "--f"],
        mono_headings=True,
    ),
    "06-chapter-6-asymmetric-cryptography-and-pki/chapter-6.html": dict(
        subject="Asymmetric crypto & PKI · the key pair",
        accents=["#4f46e5", "#d97706", "#6366f1", "#f59e0b", "#4338ca", "#b45309"],
        motif="keypair",
        vars=["--v1", "--v2", "--v3", "--v4", "--v5", "--v6"],
    ),
    "07-chapter-7-principles-of-security-design-models-and-capabilities/chapter-7.html": dict(
        subject="Security design, models & capabilities",
        accents=["#2563eb", "#0891b2", "#1d4ed8", "#0e7490"],
        motif="blueprint",
        vars=["--accent1", "--accent2", "--accent3", "--accent4"],
        grads=4,
    ),
    "08-chapter-8-security-vulnerabilities-threats-and-countermeasures/"
    "security-vulnerabilities-threats-and-countermeasures.html": dict(
        subject="Vulnerabilities & countermeasures by layer",
        accents=["#dc2626", "#ea580c", "#475569", "#b91c1c"],
        motif="strata",
        vars=["--accent", "--accent2", "--accent3", "--accent4"],
    ),
    "09-chapter-9-ics-scada-system-security/ics-scada-system-security.html": dict(
        subject="ICS / SCADA · industrial control",
        accents=["#d97706", "#0f766e", "#475569", "#a16207", "#dc2626"],
        motif="chevron",
        vars=["--accent", "--accent2", "--accent3", "--accent4", "--danger"],
    ),
    "10-chapter-10-authentication-and-access-control/authentication-and-access-control.html": dict(
        subject="Authentication & access control · locks, biometrics",
        accents=["#b45309", "#0f766e", "#be123c", "#4338ca", "#15803d"],
        motif="ridges",
        vars=["--amber", "--teal", "--rose", "--indigo", "--green"],
    ),
}


def build_block(cfg):
    acc = cfg["accents"]
    dark_acc = [lift(c) for c in acc]
    a0, d0 = acc[0], dark_acc[0]
    a1 = acc[1] if len(acc) > 1 else acc[0]
    d1 = dark_acc[1] if len(dark_acc) > 1 else dark_acc[0]

    out = ["%s /* %s */" % (MARK, cfg["subject"])]

    # chapter palette on the page's own variables
    if cfg.get("vars"):
        light = "".join("    %s: %s;\n" % (v, acc[i % len(acc)]) for i, v in enumerate(cfg["vars"]))
        dark = "".join("    %s: %s;\n" % (v, dark_acc[i % len(dark_acc)]) for i, v in enumerate(cfg["vars"]))
        out.append(':root, html[data-theme="light"] {\n%s}' % light)
        out.append('html[data-theme="dark"], [data-theme="dark"] {\n%s}' % dark)

    # gradient variables built from the same palette
    if cfg.get("grads"):
        gl, gd = [], []
        for i in range(cfg["grads"]):
            c1, c2 = acc[i % len(acc)], acc[(i + 1) % len(acc)]
            k1, k2 = dark_acc[i % len(dark_acc)], dark_acc[(i + 1) % len(dark_acc)]
            gl.append("    --grad%d: linear-gradient(135deg, %s 0%%, %s 100%%);\n" % (i + 1, c1, c2))
            gd.append("    --grad%d: linear-gradient(135deg, %s 0%%, %s 100%%);\n" % (i + 1, k1, k2))
        out.append(':root, html[data-theme="light"] {\n%s}' % "".join(gl))
        out.append('html[data-theme="dark"], [data-theme="dark"] {\n%s}' % "".join(gd))

    # subject motif, tinted per theme
    size = ("\n    background-size: %s;" % cfg["motif_size"]) if cfg.get("motif_size") else ""
    out.append(
        "body {\n    background-image: %s;\n    background-attachment: fixed;%s\n}"
        % (motif(cfg["motif"], a0, "0.055"), size)
    )
    out.append(
        'html[data-theme="dark"] body {\n    background-image: %s;\n    background-attachment: fixed;%s\n}'
        % (motif(cfg["motif"], d0, "0.075"), size)
    )

    # tie the shared chrome to the chapter
    out.append("::selection { background: %s; }" % rgba(a0, "0.24"))
    out.append('html[data-theme="dark"] ::selection { background: %s; }' % rgba(d0, "0.3"))
    out.append(".bd-progress > i { background: linear-gradient(90deg, %s, %s); }" % (a0, a1))
    out.append('html[data-theme="dark"] .bd-progress > i { background: linear-gradient(90deg, %s, %s); }'
               % (d0, d1))
    out.append(".bd-rail button:hover { border-color: %s; color: %s; }" % (a0, a0))
    out.append('html[data-theme="dark"] .bd-rail button:hover { border-color: %s; color: %s; }' % (d0, d0))

    if cfg.get("mono_headings"):
        out.append("h1, h2, h3 { font-family: ui-monospace, 'JetBrains Mono', "
                   "SFMono-Regular, Menlo, monospace; letter-spacing: -0.02em; }")
    return "\n".join(out)


def apply(path, cfg):
    p = BASE / path
    s = p.read_text(encoding="utf-8")

    # drop any previous topic block so the pass is repeatable
    s = re.sub(r"\n<style>%s.*?</style>" % re.escape(MARK), "", s, flags=re.S)

    notes = []
    # hard-coded pages: retire the stock indigo/purple for the chapter's own hues
    if cfg.get("swap"):
        n = 0
        for old, idx in cfg["swap"].items():
            new = cfg["accents"][idx]
            for variant in (old, old.upper()):
                n += s.count(variant)
                s = s.replace(variant, new)
        notes.append("%d literal accents swapped" % n)
    if cfg.get("vars"):
        notes.append("%d palette vars retinted" % len(cfg["vars"]))
    notes.append("%s motif" % cfg["motif"])

    s = s.replace("</head>", "\n<style>%s</style>\n</head>" % build_block(cfg), 1)
    p.write_text(s, encoding="utf-8")
    print("  %-46s %s" % (p.name[:46], "; ".join(notes)))


if __name__ == "__main__":
    print("Theming CYS401 breakdowns to their subject matter…")
    for path, cfg in THEMES.items():
        apply(path, cfg)
    print("Done.")
