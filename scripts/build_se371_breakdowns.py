#!/usr/bin/env python3
"""Render the SE371 slide-breakdown pages.

SE371 is a coding course: roughly a third of its slides are screenshots of code,
so a breakdown that paraphrases slide text would drop the part that matters.
Every chapter here carries reconstructed, runnable code taken from the matching
example under extra-resources/, plus a slide map, a trap list, a cheat sheet and
a self-check quiz.

Content lives in scripts/se371_breakdown_content.py; this script only renders it.

Usage:
    python3 scripts/build_se371_breakdowns.py
"""

import html
import json
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'scripts'))

BASE = '/academics/software-engineering/se371/slide-breakdowns/'
OUT = os.path.join(REPO, 'docs', 'academics', 'software-engineering', 'se371', 'slide-breakdowns')
SITE = 'https://shoug-tech.com'

from se371_breakdown_content import CHAPTERS  # noqa: E402


# --------------------------------------------------------------------------- #
# shared presentation
# --------------------------------------------------------------------------- #

STYLE = r"""
/* ── palette ───────────────────────────────────────────────────────────────
   Eight hue tokens drive the per-section colour: each <section> carries
   --sec, and its label, rule, cards and table headers all derive from it. */

:root[data-theme="dark"] {
    --bg: #0a0611;
    --bg2: #150d21;
    --bg3: #1d1330;
    --code-bg: #0d0716;
    --border: rgba(255, 255, 255, 0.10);
    --border2: rgba(255, 255, 255, 0.18);
    --text: #f4f0fa;
    --text2: #aaa2bb;
    --text3: #756e88;
    --accent: #c77dff;
    --accent2: #e6b8ff;

    --c1: #c77dff;   /* violet   */
    --c2: #4cc9f0;   /* cyan     */
    --c3: #4ade80;   /* green    */
    --c4: #fbbf24;   /* amber    */
    --c5: #fb7185;   /* rose     */
    --c6: #818cf8;   /* indigo   */
    --c7: #f472b6;   /* pink     */
    --c8: #2dd4bf;   /* teal     */

    --green: var(--c3);
    --red: var(--c5);
    --amber: var(--c4);
    --blue: var(--c2);

    --shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
    --shadow-lift: 0 6px 24px -12px rgba(0, 0, 0, 0.8);
    --hero-wash: radial-gradient(120% 140% at 8% 0%, rgba(199,125,255,0.20), transparent 60%),
                 radial-gradient(90% 120% at 92% 10%, rgba(76,201,240,0.16), transparent 62%);
}

:root[data-theme="light"] {
    --bg: #fbf9fe;
    --bg2: #f4eefb;
    --bg3: #ffffff;
    --code-bg: #f6f1fc;
    --border: rgba(24, 12, 40, 0.10);
    --border2: rgba(24, 12, 40, 0.18);
    --text: #180d26;
    --text2: #574d68;
    --text3: #8a8299;
    --accent: #7b2cbf;
    --accent2: #9d4edd;

    --c1: #7b2cbf;
    --c2: #0369a1;
    --c3: #047857;
    --c4: #a16207;
    --c5: #be123c;
    --c6: #4338ca;
    --c7: #a21caf;
    --c8: #0f766e;

    --green: var(--c3);
    --red: var(--c5);
    --amber: var(--c4);
    --blue: var(--c2);

    --shadow: 0 1px 4px rgba(24, 12, 40, 0.07);
    --shadow-lift: 0 8px 26px -16px rgba(24, 12, 40, 0.4);
    --hero-wash: radial-gradient(120% 140% at 8% 0%, rgba(123,44,191,0.12), transparent 60%),
                 radial-gradient(90% 120% at 92% 10%, rgba(3,105,161,0.10), transparent 62%);
}

/* ── fluid scale ───────────────────────────────────────────────────────────
   One root font-size ramp scales every rem on the page with the viewport,
   so the layout uses a phone and a 32" monitor equally well. */

html {
    font-size: clamp(15px, calc(13.4px + 0.34vw), 20px);
    scroll-behavior: smooth;
    overflow-x: clip;   /* clip, not hidden: hidden would break the sticky rail */
}

@media (prefers-reduced-motion: reduce) {
    html { scroll-behavior: auto; }
    * { animation: none !important; transition: none !important; }
}

:root {
    --navh: 3.4rem;
    --gutter: clamp(1rem, 3.2vw, 3rem);
    --maxw: 74rem;
    --radius: 0.85rem;
    --sec: var(--c1);
    --sec-soft: color-mix(in srgb, var(--sec) 14%, transparent);
    --sec-line: color-mix(in srgb, var(--sec) 40%, transparent);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* html-theme-sync.js injects `html, body { overflow-x: hidden }` at runtime,
   which turns the root into a scroll container and silently disables the
   sticky TOC rail. overflow-x: clip contains the same overflow without
   creating a scroll container; these selectors outrank the injected rule. */
html:root { overflow-x: clip; }
:root > body { overflow-x: clip; }

body {
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.7;
    width: 100%;
    overflow-x: clip;
    -webkit-font-smoothing: antialiased;
    transition: background 0.3s, color 0.3s;
}

/* ── reading progress ──────────────────────────────────────────────────── */
#progress {
    position: fixed; top: 0; left: 0; height: 3px; width: 0;
    z-index: 200; transform-origin: left;
    background: linear-gradient(90deg, var(--c1), var(--c7), var(--c2), var(--c3));
}

/* ── top bar ───────────────────────────────────────────────────────────
   Scoped to .topbar: the TOC rail is a <nav> too, and bare `nav` rules
   used to leak their sticky positioning and gradient rule into it. */
nav.topbar {
    position: sticky; top: 0; z-index: 100;
    background: color-mix(in srgb, var(--bg) 86%, transparent);
    backdrop-filter: blur(14px);
    border-bottom: 1px solid var(--border);
    padding-inline: var(--gutter);
    display: flex; align-items: center; gap: 1rem;
    min-height: var(--navh);
}
nav.topbar::after {
    content: ''; position: absolute; inset: auto 0 -1px 0; height: 2px;
    background: linear-gradient(90deg, var(--c1), var(--c7), var(--c2), var(--c3), var(--c4));
    opacity: 0.85;
}
.nav-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem; font-weight: 700; white-space: nowrap; flex-shrink: 0;
    background: linear-gradient(90deg, var(--c1), var(--c7));
    -webkit-background-clip: text; background-clip: text; color: transparent;
}
.nav-links {
    display: flex; gap: clamp(0.7rem, 1.4vw, 1.5rem); list-style: none;
    overflow-x: auto; min-width: 0; scrollbar-width: none;
}
.nav-links::-webkit-scrollbar { display: none; }
.nav-links a {
    color: var(--text2); text-decoration: none; font-size: 0.8rem;
    white-space: nowrap; padding: 0.15rem 0; border-bottom: 2px solid transparent;
    transition: color 0.2s, border-color 0.2s;
}
.nav-links a:hover, .nav-links a.active { color: var(--accent); border-bottom-color: var(--accent); }
.nav-actions {
    margin-left: auto; display: flex; align-items: center; gap: 0.55rem;
    flex-shrink: 0; flex-wrap: wrap; justify-content: flex-end;
}
.toggle-btn {
    background: var(--bg2); border: 1px solid var(--border2); color: var(--text2);
    border-radius: 0.6rem; padding: 0.3rem 0.8rem; cursor: pointer;
    font-size: 0.76rem; font-family: inherit; transition: all 0.2s;
}
.toggle-btn:hover { color: var(--accent); border-color: var(--accent); background: var(--sec-soft); }

/* ── hero ──────────────────────────────────────────────────────────────── */
.hero-band {
    background: var(--hero-wash);
    border-bottom: 1px solid var(--border);
}
.hero {
    width: min(100% - 2 * var(--gutter), var(--maxw));
    margin-inline: auto;
    padding-block: clamp(2rem, 5vw, 4rem);
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.18em;
    color: var(--accent); margin-bottom: 0.9rem;
    display: inline-flex; align-items: center; gap: 0.6rem;
}
.hero-eyebrow::before {
    content: ''; width: 2rem; height: 3px; border-radius: 2px;
    background: linear-gradient(90deg, var(--c1), var(--c2));
}
.hero h1 {
    font-size: clamp(2rem, 1.2rem + 3.4vw, 4.4rem);
    line-height: 1.05; font-weight: 800; letter-spacing: -0.025em;
    background: linear-gradient(115deg, var(--text) 20%, var(--c1) 60%, var(--c7) 90%);
    -webkit-background-clip: text; background-clip: text; color: transparent;
    padding-bottom: 0.1em;
}
.hero-sub {
    color: var(--text2); font-size: clamp(0.95rem, 0.88rem + 0.3vw, 1.15rem);
    margin-top: 1rem; max-width: 62ch;
}
.hero-stats { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1.5rem; }
.stat {
    font-family: 'JetBrains Mono', monospace; font-size: 0.7rem;
    border-radius: 999px; padding: 0.3rem 0.85rem;
    text-transform: uppercase; letter-spacing: 0.08em; white-space: nowrap;
    color: var(--sec);
    background: color-mix(in srgb, var(--sec) 13%, transparent);
    border: 1px solid color-mix(in srgb, var(--sec) 38%, transparent);
}
.stat:nth-child(1) { --sec: var(--c1); }
.stat:nth-child(2) { --sec: var(--c2); }
.stat:nth-child(3) { --sec: var(--c3); }
.stat:nth-child(4) { --sec: var(--c4); }
.stat:nth-child(5) { --sec: var(--c7); }

/* ── layout: prose column, plus a sticky TOC rail on wide screens ─────── */
.layout {
    width: min(100% - 2 * var(--gutter), var(--maxw));
    margin-inline: auto;
    padding-block: clamp(1.5rem, 3vw, 3rem) clamp(3rem, 6vw, 6rem);
    display: grid;
    grid-template-columns: minmax(0, 1fr);
    gap: clamp(1.5rem, 3vw, 3rem);
    align-items: start;
}

.chapter-toc {
    display: flex; flex-wrap: wrap; gap: 0.4rem;
    padding: 0.9rem; background: var(--bg2);
    border: 1px solid var(--border); border-radius: var(--radius);
}
.chapter-toc a {
    font-family: 'JetBrains Mono', monospace; font-size: 0.72rem;
    color: var(--text2); text-decoration: none;
    padding: 0.28rem 0.65rem; border-radius: 0.5rem;
    border: 1px solid transparent; transition: all 0.18s;
}
.chapter-toc a:hover { color: var(--accent); border-color: var(--border2); background: var(--bg3); }
.chapter-toc a.active {
    color: var(--accent); background: color-mix(in srgb, var(--accent) 14%, transparent);
    border-color: color-mix(in srgb, var(--accent) 40%, transparent);
}

@media (min-width: 68rem) {
    :root { --maxw: 88rem; }
    .layout { grid-template-columns: 14rem minmax(0, 1fr); }
    .toc-rail {
        position: sticky; top: calc(var(--navh) + 1rem); align-self: start;
        max-height: calc(100vh - var(--navh) - 2rem); overflow-y: auto;
    }
    .chapter-toc {
        flex-direction: column; flex-wrap: nowrap; align-items: stretch;
        gap: 0.1rem; padding: 0.75rem;
    }
    .chapter-toc a { text-align: left; border-left: 2px solid transparent; border-radius: 0 0.4rem 0.4rem 0; }
    .chapter-toc a.active { border-left-color: var(--accent); }
}
@media (min-width: 100rem) { :root { --maxw: 100rem; } .layout { grid-template-columns: 16rem minmax(0, 1fr); } }

/* ── sections ──────────────────────────────────────────────────────────── */
section {
    margin-bottom: clamp(2.5rem, 4.5vw, 4.5rem);
    scroll-margin-top: calc(var(--navh) + 1rem);
}
.section-label {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace; font-size: 0.68rem;
    text-transform: uppercase; letter-spacing: 0.16em;
    color: var(--sec); margin-bottom: 0.7rem;
    background: var(--sec-soft);
    border: 1px solid color-mix(in srgb, var(--sec) 32%, transparent);
    border-radius: 999px; padding: 0.22rem 0.75rem;
}
.section-title {
    font-size: clamp(1.35rem, 1.05rem + 1.1vw, 2.2rem);
    font-weight: 750; line-height: 1.2; letter-spacing: -0.015em;
    margin-bottom: 1.4rem; position: relative; padding-left: 0.85rem;
}
.section-title::before {
    content: ''; position: absolute; left: 0; top: 0.15em; bottom: 0.15em;
    width: 4px; border-radius: 4px;
    background: linear-gradient(180deg, var(--sec), color-mix(in srgb, var(--sec) 25%, transparent));
}

h3 {
    font-size: clamp(1rem, 0.95rem + 0.25vw, 1.2rem);
    font-weight: 680; margin: 1.8rem 0 0.7rem; color: var(--text);
}
h4 { font-size: 0.92rem; font-weight: 650; margin: 1.1rem 0 0.5rem; }
p { margin-bottom: 0.9rem; color: var(--text2); }
p strong, li strong { color: var(--text); font-weight: 600; }
ul, ol { margin: 0 0 1rem 1.3rem; color: var(--text2); }
li { margin-bottom: 0.4rem; }
li::marker { color: var(--sec); }
a { color: var(--accent); }

/* ── cards ─────────────────────────────────────────────────────────────── */
.card {
    background: var(--bg2); border: 1px solid var(--border);
    border-top: 3px solid var(--sec);
    border-radius: var(--radius); padding: 1.1rem 1.25rem;
    margin-bottom: 1rem; box-shadow: var(--shadow);
}
.card h4 { margin-top: 0; color: var(--sec); }
.card p:last-child, .card ul:last-child { margin-bottom: 0; }
.grid-2 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 17rem), 1fr));
    gap: 1rem;
}
.grid-2 > .card:nth-child(2n) { --sec: var(--c2); }
.grid-2 > .card:nth-child(3n) { --sec: var(--c3); }
.grid-2 > .card:nth-child(4n) { --sec: var(--c4); }

/* ── tables ────────────────────────────────────────────────────────────── */
.table-wrap {
    overflow-x: auto; border: 1px solid var(--border);
    border-radius: var(--radius); margin-bottom: 1.4rem; background: var(--bg2);
}
table { border-collapse: collapse; width: 100%; min-width: 32rem; font-size: 0.86rem; }
th {
    text-align: left; padding: 0.75rem 0.9rem;
    background: color-mix(in srgb, var(--sec) 12%, var(--bg3));
    font-family: 'JetBrains Mono', monospace; font-size: 0.68rem;
    text-transform: uppercase; letter-spacing: 0.1em; color: var(--sec);
    border-bottom: 2px solid var(--sec-line); white-space: nowrap;
}
td { padding: 0.7rem 0.9rem; border-bottom: 1px solid var(--border); color: var(--text2); vertical-align: top; }
tbody tr:last-child td { border-bottom: none; }
tbody tr:hover td { background: color-mix(in srgb, var(--sec) 5%, transparent); }
td strong { color: var(--text); }
td code, li code, p code, h4 code, th code, .cheat-col code {
    font-family: 'JetBrains Mono', monospace; font-size: 0.85em;
    background: var(--code-bg); border: 1px solid var(--border);
    border-radius: 0.3rem; padding: 0.05rem 0.35rem; color: var(--accent2);
}
th code { color: inherit; background: transparent; border: none; padding: 0; }
.w-memorize, .w-write, .w-skim {
    font-family: 'JetBrains Mono', monospace; font-size: 0.62rem;
    padding: 0.18rem 0.55rem; border-radius: 999px; white-space: nowrap;
    text-transform: uppercase; letter-spacing: 0.07em; font-weight: 700;
}
.w-memorize { background: color-mix(in srgb, var(--c4) 16%, transparent); color: var(--c4); border: 1px solid color-mix(in srgb, var(--c4) 42%, transparent); }
.w-write    { background: color-mix(in srgb, var(--c3) 16%, transparent); color: var(--c3); border: 1px solid color-mix(in srgb, var(--c3) 42%, transparent); }
.w-skim     { background: color-mix(in srgb, var(--text3) 14%, transparent); color: var(--text3); border: 1px solid var(--border2); }

/* ── code blocks ───────────────────────────────────────────────────────── */
.code-block {
    background: var(--bg2); border: 1px solid var(--border);
    border-radius: var(--radius); margin-bottom: 1.2rem;
    overflow: hidden; box-shadow: var(--shadow);
}
.code-head {
    display: flex; align-items: center; gap: 0.7rem; flex-wrap: wrap;
    padding: 0.6rem 1rem;
    background: linear-gradient(90deg, color-mix(in srgb, var(--sec) 13%, var(--bg3)), var(--bg3));
    border-bottom: 1px solid var(--border);
}
.code-file {
    font-family: 'JetBrains Mono', monospace; font-size: 0.74rem;
    color: var(--text); font-weight: 600;
    display: inline-flex; align-items: center; gap: 0.5rem;
}
.code-file::before {
    content: ''; width: 0.55rem; height: 0.55rem; border-radius: 50%;
    background: var(--sec); flex-shrink: 0;
}
.code-note { font-size: 0.7rem; color: var(--text3); }
.code-run {
    margin-left: auto; font-family: 'JetBrains Mono', monospace; font-size: 0.66rem;
    text-decoration: none; color: var(--sec); white-space: nowrap;
    border: 1px solid color-mix(in srgb, var(--sec) 45%, transparent);
    border-radius: 999px; padding: 0.22rem 0.7rem; transition: all 0.18s;
}
.code-run:hover { background: var(--sec); color: var(--bg); }
.code-block pre {
    margin: 0; padding: clamp(0.8rem, 1.6vw, 1.2rem);
    overflow-x: auto; background: var(--code-bg);
    font-family: 'JetBrains Mono', monospace;
    font-size: clamp(0.7rem, 0.66rem + 0.16vw, 0.84rem);
    line-height: 1.65; color: var(--text); tab-size: 4;
}
.code-block pre .c { color: var(--text3); font-style: italic; }
.code-block pre .k { color: var(--c1); }
.code-block pre .s { color: var(--c3); }
.code-block pre .t { color: var(--c2); }

/* ── traps & hooks ─────────────────────────────────────────────────────── */
.trap {
    background: linear-gradient(90deg, color-mix(in srgb, var(--c5) 9%, var(--bg2)), var(--bg2) 40%);
    border: 1px solid var(--border); border-left: 4px solid var(--c5);
    border-radius: var(--radius); padding: 1rem 1.2rem; margin-bottom: 0.9rem;
}
.trap-title { font-weight: 660; color: var(--text); margin-bottom: 0.4rem; font-size: 0.98rem; }
.trap p { margin-bottom: 0.5rem; font-size: 0.9rem; }
.trap p:last-child { margin-bottom: 0; }
.trap .fix { color: var(--c3); font-weight: 700; }

.hook {
    background: linear-gradient(115deg,
        color-mix(in srgb, var(--c1) 12%, transparent),
        color-mix(in srgb, var(--c2) 10%, transparent));
    border: 1px solid color-mix(in srgb, var(--c1) 28%, transparent);
    border-left: 4px solid var(--c1);
    border-radius: var(--radius); padding: 0.95rem 1.2rem; margin: 1.2rem 0;
    font-size: 0.9rem; color: var(--text2);
}
.hook strong { color: var(--accent2); }

/* ── cheat sheet ───────────────────────────────────────────────────────── */
.cheat {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 15rem), 1fr));
    gap: 1rem;
}
.cheat-col {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-top: 3px solid var(--sec);
    border-radius: var(--radius);
    padding: 1rem 1.1rem;
    box-shadow: var(--shadow);
}
.cheat-col:nth-child(8n+1) { --sec: var(--c1); }
.cheat-col:nth-child(8n+2) { --sec: var(--c2); }
.cheat-col:nth-child(8n+3) { --sec: var(--c3); }
.cheat-col:nth-child(8n+4) { --sec: var(--c4); }
.cheat-col:nth-child(8n+5) { --sec: var(--c5); }
.cheat-col:nth-child(8n+6) { --sec: var(--c6); }
.cheat-col:nth-child(8n+7) { --sec: var(--c7); }
.cheat-col:nth-child(8n+8) { --sec: var(--c8); }
.cheat-col h4 {
    margin-top: 0; font-family: 'JetBrains Mono', monospace; font-size: 0.68rem;
    text-transform: uppercase; letter-spacing: 0.12em; color: var(--sec);
    border-bottom: 1px solid var(--border); padding-bottom: 0.4rem;
}
.cheat-col ul { list-style: none; margin: 0.65rem 0 0; font-size: 0.8rem; }
.cheat-col li { margin-bottom: 0.42rem; line-height: 1.5; }

/* ── drills ────────────────────────────────────────────────────────────── */
.drill { counter-reset: drill; list-style: none; margin-left: 0; }
.drill li {
    counter-increment: drill; position: relative;
    padding-left: 2.6rem; margin-bottom: 0.75rem; font-size: 0.92rem;
}
.drill li::before {
    content: counter(drill, decimal-leading-zero);
    position: absolute; left: 0; top: 0.15rem;
    font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; font-weight: 700;
    color: var(--sec);
    background: color-mix(in srgb, var(--sec) 13%, transparent);
    border: 1px solid color-mix(in srgb, var(--sec) 35%, transparent);
    border-radius: 0.45rem; padding: 0.1rem 0.4rem;
}
.drill li:nth-child(6n+1) { --sec: var(--c1); }
.drill li:nth-child(6n+2) { --sec: var(--c2); }
.drill li:nth-child(6n+3) { --sec: var(--c3); }
.drill li:nth-child(6n+4) { --sec: var(--c4); }
.drill li:nth-child(6n+5) { --sec: var(--c7); }
.drill li:nth-child(6n+6) { --sec: var(--c8); }

/* ── quiz ──────────────────────────────────────────────────────────────── */
.test-card {
    background: var(--bg2); border: 1px solid var(--border);
    border-radius: var(--radius); overflow: hidden; box-shadow: var(--shadow-lift);
}
.test-head {
    display: flex; align-items: center; justify-content: space-between;
    gap: 1rem; padding: 0.9rem 1.2rem;
    background: linear-gradient(90deg,
        color-mix(in srgb, var(--c1) 18%, var(--bg3)),
        color-mix(in srgb, var(--c2) 12%, var(--bg3)));
    border-bottom: 1px solid var(--border);
}
.test-head h3 { margin: 0; font-size: 0.92rem; }
.tag {
    font-family: 'JetBrains Mono', monospace; font-size: 0.65rem;
    background: color-mix(in srgb, var(--accent) 18%, transparent);
    color: var(--accent); border: 1px solid color-mix(in srgb, var(--accent) 40%, transparent);
    border-radius: 999px; padding: 0.2rem 0.65rem;
    text-transform: uppercase; letter-spacing: 0.08em; white-space: nowrap;
}
.test-body { padding: clamp(1rem, 2vw, 1.5rem); }
.test-question { font-size: 1rem; color: var(--text); margin-bottom: 1rem; white-space: pre-wrap; }
.test-options { display: grid; gap: 0.5rem; }
.opt {
    text-align: left; padding: 0.7rem 0.95rem; border-radius: 0.6rem;
    border: 1px solid var(--border2); background: var(--bg3); color: var(--text2);
    cursor: pointer; font-family: inherit; font-size: 0.88rem; transition: all 0.15s;
}
.opt:hover:not(:disabled) { border-color: var(--accent); color: var(--text); transform: translateX(2px); }
.opt.correct { border-color: var(--c3); color: var(--c3); background: color-mix(in srgb, var(--c3) 12%, transparent); }
.opt.wrong   { border-color: var(--c5); color: var(--c5); background: color-mix(in srgb, var(--c5) 12%, transparent); }
.opt:disabled { cursor: default; }
.test-feedback { margin-top: 0.9rem; font-size: 0.88rem; color: var(--text2); display: none; }
.test-feedback.show { display: block; }
.next-btn {
    display: none; margin-top: 1rem; padding: 0.6rem 1.3rem; border-radius: 0.6rem;
    border: 1px solid color-mix(in srgb, var(--accent) 45%, transparent);
    background: color-mix(in srgb, var(--accent) 15%, transparent);
    color: var(--accent); cursor: pointer; font-family: inherit; font-size: 0.85rem;
}
.next-btn:hover { background: var(--accent); color: var(--bg); }
.next-btn.show { display: inline-block; }
#quiz-score {
    display: none; text-align: center; padding: clamp(1.2rem, 3vw, 2rem); margin-top: 1rem;
    background: var(--hero-wash), var(--bg2);
    border: 1px solid var(--border); border-radius: var(--radius);
}
#quiz-score.show { display: block; }
#quiz-score p {
    font-size: clamp(1.6rem, 1.2rem + 1.5vw, 2.6rem); font-weight: 800; margin-bottom: 0.2rem;
    background: linear-gradient(90deg, var(--c1), var(--c7));
    -webkit-background-clip: text; background-clip: text; color: transparent;
}

/* ── footer ────────────────────────────────────────────────────────────── */
footer {
    border-top: 1px solid var(--border);
    background: var(--hero-wash);
    padding: clamp(1.75rem, 4vw, 3rem) var(--gutter);
    text-align: center; color: var(--text2); font-size: 0.85rem;
}

@media (max-width: 40rem) {
    .nav-links { display: none; }
    table { min-width: 26rem; }
}
"""


PAGE_JS = r"""
let currentQ = 0, score = 0, answered = false;

function renderQuestion() {
    const q = questions[currentQ];
    answered = false;
    document.getElementById('quiz-header').textContent = `Question ${currentQ + 1} of ${questions.length}`;
    document.getElementById('quiz-tag').textContent = q.tag;
    document.getElementById('quiz-q').textContent = q.q;
    const opts = document.getElementById('quiz-opts');
    opts.innerHTML = '';
    q.opts.forEach((text, i) => {
        const b = document.createElement('button');
        b.className = 'opt';
        b.type = 'button';
        b.innerHTML = text;
        b.onclick = () => answer(i, b);
        opts.appendChild(b);
    });
    const fb = document.getElementById('quiz-fb');
    fb.className = 'test-feedback';
    fb.textContent = '';
    document.getElementById('quiz-next').className = 'next-btn';
}

function answer(i, btn) {
    if (answered) return;
    answered = true;
    const q = questions[currentQ];
    document.querySelectorAll('#quiz-opts .opt').forEach((b, j) => {
        b.disabled = true;
        if (j === q.a) b.classList.add('correct');
    });
    if (i !== q.a) btn.classList.add('wrong'); else score++;
    const fb = document.getElementById('quiz-fb');
    fb.className = 'test-feedback show';
    fb.textContent = (i === q.a ? 'Correct — ' : 'Not quite — ') + q.why;
    document.getElementById('quiz-next').className = 'next-btn show';
}

function nextQuestion() {
    currentQ++;
    if (currentQ < questions.length) { renderQuestion(); return; }
    document.querySelector('.test-card').style.display = 'none';
    document.getElementById('quiz-score').classList.add('show');
    document.getElementById('score-text').textContent = `${score} / ${questions.length}`;
    document.getElementById('score-sub').textContent =
        score === questions.length ? 'Clean sweep. Move on to the drills.'
        : score >= questions.length * 0.6 ? 'Solid. Re-read the traps you missed.'
        : 'Go back through the slide map before the next chapter.';
}

function restartQuiz() {
    currentQ = 0; score = 0;
    document.getElementById('quiz-score').classList.remove('show');
    document.querySelector('.test-card').style.display = '';
    renderQuestion();
}

function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    // Persist both keys: html-theme-sync.js resolves from localStorage only and
    // runs after this file, so without agreeing with it the page would flip.
    try {
        localStorage.setItem('shoug-theme', theme);
        localStorage.setItem('theme', theme);
    } catch (e) { }
    const btn = document.getElementById('theme-btn');
    if (btn) btn.textContent = theme === 'dark' ? 'Light' : 'Dark';
}

document.addEventListener('DOMContentLoaded', () => {
    // Default to dark — matching the site chrome this page is embedded in —
    // unless the reader has explicitly chosen light.
    let saved = null;
    try { saved = localStorage.getItem('shoug-theme') || localStorage.getItem('theme'); } catch (e) { }
    applyTheme(saved === 'light' ? 'light' : 'dark');

    const btn = document.getElementById('theme-btn');
    if (btn) {
        btn.addEventListener('click', () => {
            applyTheme(document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
        });
    }
    renderQuestion();

    // reading progress
    const bar = document.getElementById('progress');
    const onScroll = () => {
        const h = document.documentElement.scrollHeight - window.innerHeight;
        bar.style.width = (h > 0 ? (window.scrollY / h) * 100 : 0) + '%';
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    // highlight the section currently in view, in both the rail and the nav
    const links = [...document.querySelectorAll('.chapter-toc a, .nav-links a')];
    const byHash = id => links.filter(a => a.getAttribute('href') === '#' + id);
    const io = new IntersectionObserver(entries => {
        entries.forEach(e => {
            if (!e.isIntersecting) return;
            links.forEach(a => a.classList.remove('active'));
            byHash(e.target.id).forEach(a => a.classList.add('active'));
        });
    }, { rootMargin: '-25% 0px -65% 0px' });
    document.querySelectorAll('section[id]').forEach(s => io.observe(s));
});
"""


CONTENT_TMPL = """<!DOCTYPE html>
<html lang="en" data-theme="dark" data-sg-styled="true">

<head>
    <link rel="icon" type="image/png" sizes="256x256" href="/assets/shoug-favicon-v4.png">
    <link rel="shortcut icon" type="image/png" href="/assets/shoug-favicon-v4.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/shoug-apple-touch-icon-v4.png">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} &mdash; SE371 Slide Breakdown</title>
    <meta name="description" content="{desc}">
    <link rel="canonical" href="{canonical}">
    <meta property="og:title" content="{title} &mdash; SE371 Slide Breakdown">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:type" content="article">
    <meta property="og:image" content="{site}/assets/og-banner.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title} &mdash; SE371 Slide Breakdown">
    <meta name="twitter:description" content="{desc}">
    <meta name="twitter:image" content="{site}/assets/og-banner.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
    <style>{style}</style>
</head>

<body>
    <div id="progress"></div>

    <nav class="topbar" aria-label="Chapter sections">
        <div class="nav-title">SE371 // CH{num:02d}</div>
        <ul class="nav-links">{navlinks}</ul>
        <div class="nav-actions" data-page-search-host>
            <button class="toggle-btn" id="theme-btn" type="button">Light</button>
        </div>
    </nav>

    <div class="hero-band">
        <header class="hero">
            <div class="hero-eyebrow">Chapter {num:02d} &middot; Slide Breakdown</div>
            <h1>{title}</h1>
            <p class="hero-sub">{sub}</p>
            <div class="hero-stats">{stats}</div>
        </header>
    </div>

    <div class="layout">
        <aside class="toc-rail">
            <nav class="chapter-toc" aria-label="On this page">{toclinks}</nav>
        </aside>

        <main>
{sections}

        <section id="quiz" style="--sec: var(--c7)">
            <div class="section-label">Self-Check</div>
            <h2 class="section-title">Can you answer these without scrolling up?</h2>
            <div class="test-card">
                <div class="test-head">
                    <h3 id="quiz-header">Question 1</h3>
                    <span class="tag" id="quiz-tag">&nbsp;</span>
                </div>
                <div class="test-body">
                    <div class="test-question" id="quiz-q"></div>
                    <div class="test-options" id="quiz-opts"></div>
                    <div class="test-feedback" id="quiz-fb"></div>
                    <button class="next-btn" id="quiz-next" type="button" onclick="nextQuestion()">Next question &rarr;</button>
                </div>
            </div>
            <div id="quiz-score">
                <p id="score-text"></p>
                <span id="score-sub"></span><br><br>
                <button class="toggle-btn" type="button" onclick="restartQuiz()">Restart quiz</button>
            </div>
        </section>
        </main>
    </div>

    <footer>
        <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.12em;color:var(--text3);margin-bottom:0.4rem">Prepared by</div>
        <strong>Shoug Alomran</strong>
        <div style="margin-top:0.5rem;font-size:0.78rem;color:var(--text3)">SE371 Web Engineering &mdash; Chapter {num:02d}: {title}</div>
    </footer>

    <script>const questions = {quiz};{quizjs}</script>
    <script src="/javascripts/standalone-theme.js"></script>
    <script src="/javascripts/html-theme-sync.js"></script>
</body>

</html>
"""

# Section labels, nav labels and stats are authored HTML (they carry entities
# such as &ndash;), so they are emitted as-is rather than escaped again.
HUES = 8


def render_content(ch):
    nav = ''.join(
        '<li><a href="#%s">%s</a></li>' % (s['id'], s['nav'])
        for s in ch['sections']
    ) + '<li><a href="#quiz">Quiz</a></li>'
    toc = ''.join(
        '<a href="#%s">%02d %s</a>' % (s['id'], i + 1, s['nav'])
        for i, s in enumerate(ch['sections'])
    ) + '<a href="#quiz">%02d Quiz</a>' % (len(ch['sections']) + 1)
    stats = ''.join('<span class="stat">%s</span>' % s for s in ch['stats'])
    body = '\n'.join(
        '        <section id="%s" style="--sec: var(--c%d)">\n'
        '            <div class="section-label">%s</div>\n'
        '            <h2 class="section-title">%s</h2>\n%s\n        </section>'
        % (s['id'], (i % HUES) + 1, s['label'], s['title'], s['html'])
        for i, s in enumerate(ch['sections'])
    )
    return CONTENT_TMPL.format(
        title=html.escape(ch['title']),
        desc=html.escape(ch['desc']),
        canonical='%s%s%s/%s' % (SITE, BASE, ch['slug'], ch['file']),
        site=SITE,
        num=ch['num'],
        style=STYLE,
        navlinks=nav,
        toclinks=toc,
        stats=stats,
        sub=ch['sub'],
        sections=body,
        quiz=json.dumps(ch['quiz'], ensure_ascii=False, indent=None),
        quizjs=PAGE_JS,
    )


# --------------------------------------------------------------------------- #
# shell page (reuses the site chrome from an existing academic page)
# --------------------------------------------------------------------------- #

SHELL_SRC = os.path.join(
    REPO, 'docs', 'academics', 'other-courses', 'ethcs303',
    'slide-breakdowns', '02-kantianism', 'index.html')


def shell_main(ch, prev_ch, next_ch):
    crumb = (
        '<div class="breadcrumb"><a class="breadcrumb-link" href="/academics/">Academics</a> '
        '<span class="separator">/</span> <a class="breadcrumb-link" href="/academics/software-engineering/">'
        'Software Engineering</a> <span class="separator">/</span> '
        '<a class="breadcrumb-link" href="/academics/software-engineering/se371/">SE371</a> '
        '<span class="separator">/</span> <a class="breadcrumb-link" href="%s">Slide Breakdowns</a> '
        '<span class="separator">/</span> <span class="current">%s</span></div>'
        % (BASE, html.escape(ch['title'])))

    navstrip = ''
    if prev_ch or next_ch:
        parts = []
        if prev_ch:
            parts.append('<a href="%s%s/" class="nav-link prev">&lt;- PREVIOUS</a>'
                         % (BASE, prev_ch['slug']))
        if next_ch:
            parts.append('<a href="%s%s/" class="nav-link next">NEXT -&gt;</a>'
                         % (BASE, next_ch['slug']))
        navstrip = '<div class="nav-strip uppercase">%s</div>' % ''.join(parts)

    title = html.escape(ch['title'])
    return """        <main class="content-area" vid="58">

            <div class="top-bar uppercase" vid="59">
                {crumb}
                <div class="sys-time" id="clock" vid="70">SYS_TIME [ 00 00 00 ]</div>
            </div>

            <div class="page-header" vid="73">
                <div class="ch-label uppercase">CHAPTER_{num:02d} // SLIDE BREAKDOWNS</div>
                <h1 class="ch-title uppercase">{title}</h1>
                <div class="action-buttons"><a class="btn btn-primary" href="./{file}" target="_blank" rel="noopener noreferrer">[ OPEN IN NEW TAB -&gt; ]</a><a class="btn btn-secondary" href="{base}">[ &lt;- BACK TO INDEX ]</a></div>
            </div>

            {navstrip}

            <div class="embed-area-wrapper" vid="82">
                <div class="embed-container" id="embedded-content">
                    <div class="rendered-content" data-lang-panel="en"><iframe class="embed-frame legacy-html-frame" src="./{file}" loading="lazy" title="{title}"></iframe></div>
                    <div class="rendered-content" data-lang-panel="ar" hidden><iframe class="embed-frame legacy-html-frame" src="./{file}" loading="lazy" title="{title}"></iframe></div>
                </div>
            </div>
    </div>
    </div>

    </main>""".format(crumb=crumb, num=ch['num'], title=title, file=ch['file'],
                      base=BASE, navstrip=navstrip)


MAIN_RE = re.compile(r'        <main class="content-area" vid="58">.*?    </main>', re.S)
HEAD_TITLE_RE = re.compile(r'<title>.*?</title>', re.S)
CANON_RE = re.compile(r'<link rel="canonical"[^>]*>', re.S)


def build_shell(ch, prev_ch, next_ch, template):
    out = MAIN_RE.sub(lambda m: shell_main(ch, prev_ch, next_ch), template, count=1)
    out = HEAD_TITLE_RE.sub(
        '<title>SHOUG.TECH | SE371 %s</title>' % html.escape(ch['title']), out, count=1)
    out = CANON_RE.sub(
        '<link rel="canonical" href="%s%s%s/">' % (SITE, BASE, ch['slug']), out, count=1)
    # strip the stale ETHCS303 SEO block from the borrowed chrome, then restate it
    out = re.sub(r'<meta\s+(?:property="og:[a-z:]+"|name="twitter:[a-z:]+"|name="description")'
                 r'\s+content="[^"]*"\s*>', '', out, flags=re.S)
    out = re.sub(r'<script\s+type="application/ld\+json"\s*>.*?</script>', '', out, flags=re.S)
    out = re.sub(r'<link\s+rel="alternate"\s+hreflang="[^"]*"\s+href="[^"]*"\s*>', '', out, flags=re.S)
    out = out.replace('ethcs303', 'se371').replace('ETHCS303', 'SE371')

    # standalone-theme.js inside the iframe reads the parent for its theme. With
    # no stored preference the shell renders its dark chrome but exposes nothing,
    # so the embedded page fell back to the OS setting and could come up light
    # inside a dark shell. Declaring the shell's own default fixes that; an
    # explicit light choice still wins, because the script checks the
    # shoug-light-mode class on the parent body first.
    out = re.sub(r'<html(?![^>]*\bdata-theme=)([^>]*)>',
                 r'<html\1 data-theme="dark">', out, count=1)

    url = '%s%s%s/' % (SITE, BASE, ch['slug'])
    title = 'SE371 %s &mdash; Slide Breakdown' % html.escape(ch['title'])
    desc = html.escape(ch['desc'])
    seo = (
        '<meta name="description" content="{desc}">'
        '<meta property="og:title" content="{title}">'
        '<meta property="og:description" content="{desc}">'
        '<meta property="og:url" content="{url}">'
        '<meta property="og:type" content="article">'
        '<meta property="og:image" content="{site}/assets/og-banner.png">'
        '<meta name="twitter:card" content="summary_large_image">'
        '<meta name="twitter:title" content="{title}">'
        '<meta name="twitter:description" content="{desc}">'
        '<meta name="twitter:image" content="{site}/assets/og-banner.png">'
        '<script type="application/ld+json">{ld}</script>'
        '<link rel="alternate" hreflang="en" href="{url}">'
        '<link rel="alternate" hreflang="ar" href="{site}/ar{path}">'
        '<link rel="alternate" hreflang="x-default" href="{url}">'
    ).format(desc=desc, title=title, url=url, site=SITE,
             path='%s%s/' % (BASE, ch['slug']),
             ld=json.dumps({
                 '@context': 'https://schema.org', '@type': 'WebPage', 'url': url,
                 'name': 'SE371 %s — Slide Breakdown' % ch['title'], 'description': ch['desc'],
                 'isPartOf': {'@type': 'WebSite', 'name': "Shoug's Digital Garden",
                              'url': SITE + '/'},
             }, ensure_ascii=False))
    out = out.replace('</head>', seo + '</head>', 1)
    return out



# --------------------------------------------------------------------------- #
# the slide-breakdowns listing page
# --------------------------------------------------------------------------- #

ARROW = ('<div class="dir-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
         'stroke-width="2" stroke-linecap="square"><path d="M5 12h14M12 5l7 7-7 7"/></svg></div>')

COMING_SOON_RE = re.compile(
    r'\s*<div class="coming-soon-container".*?</div>\s*</div>', re.S)
DIRECTORY_RE = re.compile(
    r'\s*<div class="directory-container">.*</div>\s*(?=<footer)', re.S)

AR_TITLES = {
    1: 'مقدمة في الويب',
    2: 'HTML: المستندات والجداول والنماذج',
    3: 'CSS: المحددات والتتالي والتخطيط',
    4: 'أساسيات جافاسكريبت',
    5: 'جافاسكريبت في الواجهة الأمامية',
    6: 'جانب الخادم: Node.js و Express',
    7: 'العمل مع قواعد البيانات',
}


def listing_rows():
    rows = []
    for ch in CHAPTERS:
        rows.append(
            '                            <a href="%s%s/" class="dir-row" data-ar-title="%s">\n'
            '                                <div class="dir-num">CH %02d</div>\n'
            '                                <div class="dir-title">%s</div>\n'
            '                                <div class="dir-status">'
            '<span class="status-tag available">AVAILABLE</span></div>\n'
            '                                %s\n'
            '                            </a>'
            % (BASE, ch['slug'], html.escape(AR_TITLES[ch['num']], quote=True),
               ch['num'], html.escape(ch['title']), ARROW))
    return (
        '\n                <div class="directory-container">\n'
        '                <div class="dir-header">\n'
        '                    <span>SEQ</span>\n'
        '                    <span>DESCRIPTOR</span>\n'
        '                    <span>SYS_STATE</span>\n'
        '                    <span></span>\n'
        '                </div>\n\n'
        + '\n'.join(rows) +
        '\n                </div>\n\n    ')


def build_listing():
    path = os.path.join(OUT, 'index.html')
    with open(path, encoding='utf-8') as fh:
        page = fh.read()
    rows = listing_rows()
    if COMING_SOON_RE.search(page):
        page = COMING_SOON_RE.sub(lambda m: rows, page, count=1)
    elif DIRECTORY_RE.search(page):
        page = DIRECTORY_RE.sub(lambda m: rows, page, count=1)
    else:
        raise SystemExit('listing page: found neither a coming-soon block nor a directory to replace')
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(page)
    print('wrote index.html listing (%d chapters)' % len(CHAPTERS))


def main():
    with open(SHELL_SRC, encoding='utf-8') as fh:
        template = fh.read()

    for i, ch in enumerate(CHAPTERS):
        folder = os.path.join(OUT, ch['slug'])
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, ch['file']), 'w', encoding='utf-8') as fh:
            fh.write(render_content(ch))
        prev_ch = CHAPTERS[i - 1] if i else None
        next_ch = CHAPTERS[i + 1] if i + 1 < len(CHAPTERS) else None
        with open(os.path.join(folder, 'index.html'), 'w', encoding='utf-8') as fh:
            fh.write(build_shell(ch, prev_ch, next_ch, template))
        print('wrote %s/ (%d sections)' % (ch['slug'], len(ch['sections'])))

    build_listing()

    # The chapter shells borrow their chrome from an ETHCS303 page, so the
    # sidebar they arrive with is that course's. Restamp it from the single
    # source of truth rather than leaving the two to drift.
    subprocess.check_call(
        [sys.executable, os.path.join(REPO, 'scripts', 'build_academic_sidebar.py')])


if __name__ == '__main__':
    main()
