#!/usr/bin/env python3
"""Build the ACM Programming Jam 2026 (JAM.26) pages under /workshops/ai-programming-jam/.

Content is written once as a single-page BODY and split into the hub plus four
sub-pages; the shared chrome, CSS and page shells come from event_page_kit.
"""

from __future__ import annotations

from pathlib import Path

from event_page_kit import (
    DOCS,
    Event,
    Page,
    breadcrumb,
    build_subpage,
    extract_chrome,
    render,
    split_sections,
    subnav,
    write,
)

ROOT = DOCS / "workshops" / "ai-programming-jam"
BASE = "/workshops/ai-programming-jam/"
EVENT_LABEL = "ACM Programming Jam 2026"

TITLE = "ACM Programming Jam 2026 // SHOUG.TECH"
DESCRIPTION = (
    "ACM Programming Jam 2026 (JAM.26) at Prince Sultan University — an AI-assisted "
    "web engineering event. Three workshop days on planning, full-stack development and "
    "debugging, and deployment, all written and taught by Shoug Alomran, plus the "
    "competition format, rubric, rules and FAQ."
)

THEME_CSS = """
        :root {
            --bg-void: #05070c;
            --bg-surface: #0a0f16;
            --bg-elevated: #0e1620;
            --bg-code: #070b11;
            --text-main: #e6edf3;
            --text-dim: #8b98a8;
            --text-faint: #5d6a79;
            --border-subtle: rgba(255, 255, 255, 0.09);
            --border-medium: rgba(255, 255, 255, 0.18);
            --accent: #3ddc84;
            --accent-soft: rgba(61, 220, 132, 0.14);
            --accent-line: rgba(61, 220, 132, 0.34);
            --blue: #58a6ff;
            --amber: #e3b341;
            --violet: #bc8cff;
            --rose: #ff7b72;
            --font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, monospace;
            --font-display: 'Rajdhani', sans-serif;
            --font-body: 'Inter', system-ui, sans-serif;
        }

        body {
            background-color: var(--bg-void);
            color: var(--text-main);
            font-family: var(--font-body);
            line-height: 1.6;
        }

        ::selection { background: var(--accent); color: #04140b; }

        .grid-bg {
            position: fixed;
            inset: 0;
            z-index: -1;
            pointer-events: none;
            background-image:
                linear-gradient(rgba(61, 220, 132, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(61, 220, 132, 0.05) 1px, transparent 1px);
            background-size: 64px 64px;
            mask-image: radial-gradient(ellipse 90% 60% at 50% 0%, #000 20%, transparent 78%);
            -webkit-mask-image: radial-gradient(ellipse 90% 60% at 50% 0%, #000 20%, transparent 78%);
        }

        .breadcrumb {
            font-family: var(--font-mono);
            font-size: 0.68rem;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: var(--text-faint);
            padding: 26px 0 0;
        }
        .breadcrumb a { color: var(--text-dim); text-decoration: none; }
        .breadcrumb a:hover { color: var(--accent); }
        .breadcrumb .sep { color: var(--accent-line); margin: 0 8px; }

        /* ── hero ───────────────────────────────────────────── */
        .hero {
            display: grid;
            grid-template-columns: minmax(0, 1.15fr) minmax(0, 0.85fr);
            gap: 48px;
            align-items: center;
            padding: 56px 0 64px;
        }

        .kicker {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            font-family: var(--font-mono);
            font-size: 0.68rem;
            letter-spacing: 0.22em;
            text-transform: uppercase;
            color: var(--accent);
            border: 1px solid var(--accent-line);
            background: var(--accent-soft);
            padding: 6px 12px;
            border-radius: 2px;
        }

        .dot {
            width: 6px; height: 6px; border-radius: 50%;
            background: var(--accent);
            box-shadow: 0 0 0 0 rgba(61, 220, 132, 0.6);
            animation: pulse 2.4s infinite;
        }
        @keyframes pulse {
            70% { box-shadow: 0 0 0 8px rgba(61, 220, 132, 0); }
            100% { box-shadow: 0 0 0 0 rgba(61, 220, 132, 0); }
        }

        .hero h1 {
            font-family: var(--font-display);
            font-size: clamp(2.6rem, 6.4vw, 4.6rem);
            line-height: 0.98;
            letter-spacing: -0.01em;
            text-transform: uppercase;
            margin: 22px 0 6px;
        }
        .hero h1 .brace { color: var(--accent); }

        .hero-tagline {
            font-family: var(--font-mono);
            font-size: clamp(0.95rem, 2vw, 1.25rem);
            color: var(--accent);
            letter-spacing: 0.05em;
            margin-bottom: 18px;
        }

        .hero-lede { color: var(--text-dim); max-width: 60ch; font-size: 1.02rem; }

        .hero-facts {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 24px;
            font-family: var(--font-mono);
            font-size: 0.7rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }
        .hero-facts span {
            border: 1px solid var(--border-subtle);
            background: var(--bg-surface);
            color: var(--text-dim);
            padding: 6px 10px;
        }

        .hero-actions { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 28px; }

        .btn {
            font-family: var(--font-mono);
            font-size: 0.72rem;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            text-decoration: none;
            padding: 12px 20px;
            border: 1px solid var(--accent-line);
            transition: background 0.18s ease, color 0.18s ease, transform 0.18s ease;
        }
        .btn-primary { background: var(--accent); color: #04140b; border-color: var(--accent); font-weight: 700; }
        .btn-primary:hover { transform: translateY(-2px); }
        .btn-ghost { color: var(--accent); background: transparent; }
        .btn-ghost:hover { background: var(--accent-soft); transform: translateY(-2px); }

        /* ── window chrome (editor / terminal) ───────────────── */
        .win {
            background: var(--bg-code);
            border: 1px solid var(--border-subtle);
            border-radius: 6px;
            overflow: hidden;
            box-shadow: 0 24px 60px rgba(0, 0, 0, 0.45);
        }
        .win-bar {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 9px 12px;
            background: var(--bg-elevated);
            border-bottom: 1px solid var(--border-subtle);
            font-family: var(--font-mono);
            font-size: 0.65rem;
            letter-spacing: 0.1em;
            color: var(--text-faint);
        }
        .win-dots { display: flex; gap: 6px; margin-right: 6px; }
        .win-dots i { width: 9px; height: 9px; border-radius: 50%; background: var(--border-medium); display: block; }
        .win-dots i:first-child { background: #ff5f57; }
        .win-dots i:nth-child(2) { background: #febc2e; }
        .win-dots i:nth-child(3) { background: #28c840; }
        .win-body { padding: 16px 18px; font-family: var(--font-mono); font-size: 0.78rem; line-height: 1.85; }

        .code { counter-reset: ln; }
        .code .ln { display: block; padding-left: 34px; position: relative; white-space: pre-wrap; min-height: 1.85em; }
        .code .ln::before {
            counter-increment: ln;
            content: counter(ln);
            position: absolute;
            left: 0;
            width: 22px;
            text-align: right;
            color: var(--text-faint);
            opacity: 0.6;
        }
        .k { color: var(--violet); }
        .s { color: var(--amber); }
        .c { color: var(--text-faint); font-style: italic; }
        .fn { color: var(--blue); }
        .num { color: var(--rose); }
        .p { color: var(--text-dim); }

        .term .win-body { white-space: pre-wrap; }
        .term .prompt { color: var(--accent); }
        .term .out { color: var(--text-dim); }
        .term .ok { color: var(--accent); }
        .term .warn { color: var(--amber); }
        .term .err { color: var(--rose); }
        .caret {
            display: inline-block;
            width: 8px;
            height: 1em;
            background: var(--accent);
            vertical-align: -2px;
            animation: blink 1.1s steps(2, start) infinite;
        }
        @keyframes blink { 50% { opacity: 0; } }

        /* ── sections ───────────────────────────────────────── */
        section.block { padding: 64px 0; border-top: 1px solid var(--border-subtle); }

        .sect-label {
            font-family: var(--font-mono);
            font-size: 0.68rem;
            letter-spacing: 0.24em;
            text-transform: uppercase;
            color: var(--accent);
            margin-bottom: 14px;
        }

        .sect-title {
            font-family: var(--font-display);
            font-size: clamp(1.7rem, 3.6vw, 2.6rem);
            line-height: 1.08;
            text-transform: uppercase;
            letter-spacing: -0.005em;
            margin-bottom: 14px;
        }

        .sect-intro { color: var(--text-dim); max-width: 72ch; margin-bottom: 34px; }

        /* ── metadata strip ─────────────────────────────────── */
        .meta-strip {
            border: 1px solid var(--border-subtle);
            border-left: 2px solid var(--accent);
            background: var(--bg-surface);
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
        }
        .meta-item { padding: 18px 22px; border-right: 1px solid var(--border-subtle); border-bottom: 1px solid var(--border-subtle); }
        .meta-label {
            display: block;
            font-family: var(--font-mono);
            font-size: 0.63rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: var(--text-faint);
            margin-bottom: 6px;
        }
        .meta-value { font-size: 0.92rem; color: var(--text-main); }

        /* ── contribution list ──────────────────────────────── */
        .contrib { list-style: none; display: grid; gap: 14px; max-width: 92ch; }
        .contrib li {
            display: grid;
            grid-template-columns: 30px 1fr;
            gap: 12px;
            color: var(--text-dim);
            border-left: 1px solid var(--border-subtle);
            padding: 6px 0 6px 16px;
        }
        .contrib li:hover { border-left-color: var(--accent); }
        .contrib .mark { font-family: var(--font-mono); color: var(--accent); font-size: 0.78rem; }
        .contrib strong { color: var(--text-main); font-weight: 600; }

        /* ── marquee flow strip ─────────────────────────────── */
        .flow {
            margin: 0;
            border-top: 1px solid var(--border-subtle);
            border-bottom: 1px solid var(--border-subtle);
            background: var(--bg-surface);
            overflow: hidden;
            white-space: nowrap;
        }
        .flow-track {
            display: inline-flex;
            gap: 32px;
            padding: 14px 0;
            font-family: var(--font-mono);
            font-size: 0.74rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: var(--text-faint);
            animation: slide 34s linear infinite;
        }
        .flow-track span.hl { color: var(--accent); }
        @keyframes slide { to { transform: translateX(-50%); } }

        /* ── generic card grids ─────────────────────────────── */
        .grid-3 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px; }
        .grid-2 { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; }

        .card {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            padding: 24px;
            position: relative;
            transition: border-color 0.2s ease, transform 0.2s ease;
        }
        .card:hover { border-color: var(--accent-line); transform: translateY(-3px); }
        .card-num {
            font-family: var(--font-mono);
            font-size: 0.68rem;
            letter-spacing: 0.2em;
            color: var(--accent);
            margin-bottom: 10px;
        }
        .card h3 {
            font-family: var(--font-display);
            font-size: 1.25rem;
            text-transform: uppercase;
            letter-spacing: 0.01em;
            margin-bottom: 8px;
        }
        .card p { color: var(--text-dim); font-size: 0.92rem; }
        .card .when {
            font-family: var(--font-mono);
            font-size: 0.66rem;
            letter-spacing: 0.12em;
            color: var(--text-faint);
            text-transform: uppercase;
            margin-bottom: 12px;
            display: block;
        }

        /* ── workshop days ──────────────────────────────────── */
        .day {
            display: grid;
            grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
            gap: 32px;
            align-items: start;
            padding: 34px 0;
            border-top: 1px dashed var(--border-subtle);
        }
        .day:first-of-type { border-top: none; }
        .day-index {
            font-family: var(--font-mono);
            font-size: 0.68rem;
            letter-spacing: 0.2em;
            color: var(--accent);
            margin-bottom: 10px;
        }
        .day h3 {
            font-family: var(--font-display);
            font-size: clamp(1.4rem, 2.6vw, 2rem);
            text-transform: uppercase;
            line-height: 1.1;
            margin-bottom: 10px;
        }
        .day .focus { color: var(--text-dim); margin-bottom: 18px; }
        .objectives { list-style: none; display: grid; gap: 9px; }
        .objectives li {
            font-family: var(--font-mono);
            font-size: 0.8rem;
            color: var(--text-dim);
            display: grid;
            grid-template-columns: 22px 1fr;
            gap: 8px;
            align-items: start;
        }
        .objectives li::before { content: "[+]"; color: var(--accent); white-space: pre; }
        .status-line {
            margin-top: 18px;
            font-family: var(--font-mono);
            font-size: 0.68rem;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: var(--accent);
            border-top: 1px solid var(--border-subtle);
            padding-top: 12px;
        }

        /* ── toolchain ──────────────────────────────────────── */
        .stack { display: flex; flex-wrap: wrap; gap: 10px; }
        .chip {
            font-family: var(--font-mono);
            font-size: 0.72rem;
            letter-spacing: 0.08em;
            border: 1px solid var(--border-subtle);
            background: var(--bg-surface);
            padding: 9px 14px;
            color: var(--text-dim);
            transition: color 0.18s ease, border-color 0.18s ease;
        }
        .chip:hover { color: var(--accent); border-color: var(--accent-line); }
        .chip b { color: var(--text-faint); font-weight: 400; margin-right: 8px; }

        /* ── rubric ─────────────────────────────────────────── */
        .rubric { display: grid; gap: 12px; }
        .rubric-row {
            display: grid;
            grid-template-columns: 62px minmax(0, 1fr);
            gap: 18px;
            align-items: start;
            border: 1px solid var(--border-subtle);
            background: var(--bg-surface);
            padding: 16px 20px;
        }
        .rubric-weight {
            font-family: var(--font-mono);
            font-size: 1.2rem;
            color: var(--accent);
            font-weight: 700;
        }
        .rubric-name {
            font-family: var(--font-display);
            font-size: 1.05rem;
            text-transform: uppercase;
            letter-spacing: 0.02em;
            margin-bottom: 4px;
        }
        .rubric-desc { color: var(--text-dim); font-size: 0.9rem; margin-bottom: 10px; }
        .bar { height: 4px; background: var(--bg-elevated); position: relative; overflow: hidden; }
        .bar i { display: block; height: 100%; background: var(--accent); }

        /* ── timeline ───────────────────────────────────────── */
        .timeline { display: grid; gap: 0; border-left: 1px solid var(--border-subtle); }
        .tl-row {
            display: grid;
            grid-template-columns: minmax(150px, max-content) minmax(0, 1fr);
            gap: 22px;
            padding: 14px 0 14px 20px;
            position: relative;
            font-family: var(--font-mono);
            font-size: 0.8rem;
        }
        .tl-row::before {
            content: "";
            position: absolute;
            left: -4px;
            top: 22px;
            width: 7px;
            height: 7px;
            background: var(--bg-void);
            border: 1px solid var(--accent);
            border-radius: 50%;
        }
        .tl-row.alert::before { background: var(--amber); border-color: var(--amber); }
        .tl-key { color: var(--text-main); letter-spacing: 0.08em; }
        .tl-row.alert .tl-key { color: var(--amber); }
        .tl-val { color: var(--text-faint); letter-spacing: 0.14em; }

        /* ── rules ──────────────────────────────────────────── */
        .rule {
            border: 1px solid var(--border-subtle);
            background: var(--bg-surface);
            padding: 20px 22px;
            transition: border-color 0.2s ease;
        }
        .rule:hover { border-color: var(--rose); }
        .rule-id {
            font-family: var(--font-mono);
            font-size: 0.66rem;
            letter-spacing: 0.2em;
            color: var(--rose);
            margin-bottom: 8px;
        }
        .rule h3 {
            font-family: var(--font-display);
            font-size: 1.1rem;
            text-transform: uppercase;
            margin-bottom: 8px;
        }
        .rule p { color: var(--text-dim); font-size: 0.9rem; }
        .rule .note {
            display: block;
            margin-top: 10px;
            font-family: var(--font-mono);
            font-size: 0.72rem;
            color: var(--text-faint);
        }

        .tiers { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin-top: 22px; }
        .tier { border: 1px solid var(--border-subtle); background: var(--bg-surface); padding: 18px 20px; font-family: var(--font-mono); }
        .tier .lvl { font-size: 0.66rem; letter-spacing: 0.2em; color: var(--text-faint); }
        .tier .verdict { font-size: 1.05rem; margin: 8px 0 4px; }
        .tier .eg { font-size: 0.74rem; color: var(--text-dim); }
        .tier.allow { border-left: 2px solid var(--accent); }
        .tier.allow .verdict { color: var(--accent); }
        .tier.deny { border-left: 2px solid var(--rose); }
        .tier.deny .verdict { color: var(--rose); }

        /* ── checklist ──────────────────────────────────────── */
        .checklist { list-style: none; display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 10px; }
        .checklist li {
            font-family: var(--font-mono);
            font-size: 0.8rem;
            color: var(--text-dim);
            border: 1px solid var(--border-subtle);
            background: var(--bg-surface);
            padding: 12px 14px;
            display: grid;
            grid-template-columns: 24px 1fr;
            gap: 10px;
        }
        .checklist li::before { content: "[ ]"; color: var(--accent); white-space: pre; }

        /* ── faq ────────────────────────────────────────────── */
        .faq-group { margin-bottom: 30px; }
        .faq-group-title {
            font-family: var(--font-mono);
            font-size: 0.68rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: var(--text-faint);
            border-bottom: 1px solid var(--border-subtle);
            padding-bottom: 8px;
            margin-bottom: 12px;
        }
        details.faq {
            border: 1px solid var(--border-subtle);
            background: var(--bg-surface);
            margin-bottom: 8px;
        }
        details.faq summary {
            cursor: pointer;
            list-style: none;
            padding: 14px 18px;
            font-family: var(--font-mono);
            font-size: 0.83rem;
            color: var(--text-main);
            display: flex;
            justify-content: space-between;
            gap: 16px;
        }
        details.faq summary::-webkit-details-marker { display: none; }
        details.faq summary::after { content: "[+]"; color: var(--accent); flex-shrink: 0; }
        details.faq[open] summary::after { content: "[-]"; }
        details.faq summary:hover { color: var(--accent); }
        details.faq .answer { padding: 0 18px 16px; color: var(--text-dim); font-size: 0.92rem; }
        details.faq .answer b { color: var(--accent); }

        /* ── callout + cta ──────────────────────────────────── */
        .callout {
            border: 1px solid var(--accent-line);
            background: var(--accent-soft);
            padding: 20px 24px;
            font-family: var(--font-mono);
            font-size: 0.86rem;
            color: var(--text-main);
        }
        .callout b { color: var(--accent); }

        .cta {
            text-align: center;
            padding: 80px 0 90px;
            border-top: 1px solid var(--border-subtle);
        }
        .cta h2 {
            font-family: var(--font-display);
            font-size: clamp(2rem, 5vw, 3.4rem);
            text-transform: uppercase;
            line-height: 1;
            margin-bottom: 16px;
        }
        .cta p { color: var(--text-dim); max-width: 56ch; margin: 0 auto 26px; }
        .cta .hero-actions { justify-content: center; }

        /* ── sub-navigation (page tabs) ─────────────────────── */
        .subnav {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            border-bottom: 1px solid var(--border-subtle);
            padding: 18px 0 0;
            margin-bottom: 4px;
        }
        .subnav a {
            font-family: var(--font-mono);
            font-size: 0.7rem;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            text-decoration: none;
            color: var(--text-dim);
            padding: 10px 16px;
            border: 1px solid transparent;
            border-bottom: none;
            transition: color 0.18s ease, background 0.18s ease;
        }
        .subnav a:hover { color: var(--accent); background: var(--accent-soft); }
        .subnav a.active {
            color: var(--accent);
            background: var(--bg-surface);
            border-color: var(--border-subtle);
            box-shadow: inset 0 2px 0 var(--accent);
        }

        /* ── sub-page header ────────────────────────────────── */
        .page-head { padding: 44px 0 12px; }
        .page-head .eyebrow {
            font-family: var(--font-mono);
            font-size: 0.68rem;
            letter-spacing: 0.22em;
            text-transform: uppercase;
            color: var(--text-faint);
            margin-bottom: 12px;
        }
        .page-head h1 {
            font-family: var(--font-display);
            font-size: clamp(2.1rem, 5vw, 3.4rem);
            line-height: 1;
            text-transform: uppercase;
            margin-bottom: 14px;
        }
        .page-head h1 .brace { color: var(--accent); }
        .page-head p { color: var(--text-dim); max-width: 74ch; }

        section.block:first-of-type { border-top: none; padding-top: 8px; }

        /* ── hub boxes ──────────────────────────────────────── */
        .hub-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; }
        .hub-card {
            display: block;
            text-decoration: none;
            color: inherit;
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            padding: 28px;
            position: relative;
            overflow: hidden;
            transition: border-color 0.2s ease, transform 0.2s ease;
        }
        .hub-card::after {
            content: "";
            position: absolute;
            inset: 0 auto 0 0;
            width: 2px;
            background: var(--accent);
            transform: scaleY(0);
            transform-origin: top;
            transition: transform 0.24s ease;
        }
        .hub-card:hover { border-color: var(--accent-line); transform: translateY(-3px); }
        .hub-card:hover::after { transform: scaleY(1); }
        .hub-card-top {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            font-family: var(--font-mono);
            font-size: 0.68rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: var(--accent);
            margin-bottom: 14px;
        }
        .hub-card-top .file { color: var(--text-faint); }
        .hub-card h3 {
            font-family: var(--font-display);
            font-size: 1.5rem;
            text-transform: uppercase;
            line-height: 1.05;
            margin-bottom: 10px;
        }
        .hub-card p { color: var(--text-dim); font-size: 0.93rem; margin-bottom: 16px; }
        .hub-card .hub-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-family: var(--font-mono);
            font-size: 0.68rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--text-faint);
            border-top: 1px solid var(--border-subtle);
            padding-top: 12px;
        }
        .hub-card .arrow { color: var(--accent); }

        /* ── pager ──────────────────────────────────────────── */
        .pager {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            border-top: 1px solid var(--border-subtle);
            padding: 26px 0 60px;
            font-family: var(--font-mono);
            font-size: 0.72rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }
        .pager a { color: var(--text-dim); text-decoration: none; }
        .pager a:hover { color: var(--accent); }
        .pager .spacer { flex: 1; }

        /* ── light mode ─────────────────────────────────────── */
        body.shoug-light-mode {
            --bg-void: #f6f4fb;
            --bg-surface: #ffffff;
            --bg-elevated: #eef1f6;
            --bg-code: #f4f6fa;
            --text-main: #16111f;
            --text-dim: #4f5a68;
            --text-faint: #77808d;
            --border-subtle: rgba(22, 17, 31, 0.12);
            --border-medium: rgba(22, 17, 31, 0.2);
            --accent: #128a4d;
            --accent-soft: rgba(18, 138, 77, 0.09);
            --accent-line: rgba(18, 138, 77, 0.3);
            --blue: #1f6feb;
            --amber: #9a6700;
            --violet: #8250df;
            --rose: #cf222e;
        }
        body.shoug-light-mode .grid-bg {
            background-image:
                linear-gradient(rgba(18, 138, 77, 0.07) 1px, transparent 1px),
                linear-gradient(90deg, rgba(18, 138, 77, 0.07) 1px, transparent 1px);
        }
        body.shoug-light-mode .win { box-shadow: 0 18px 42px rgba(22, 17, 31, 0.1); }
        body.shoug-light-mode .btn-primary { color: #ffffff; }
        body.shoug-light-mode ::selection { background: #128a4d; color: #ffffff; }

        /* ── rtl ────────────────────────────────────────────── */
        /* The page body is English technical content (code, terminals, command
           names), so it stays left-to-right while the site chrome flips. */
        html[dir="rtl"] main { direction: ltr; text-align: left; }
        html[dir="rtl"] .breadcrumb { direction: ltr; }

        /* ── responsive ─────────────────────────────────────── */
        @media (max-width: 980px) {
            .hero { grid-template-columns: 1fr; gap: 32px; padding: 36px 0 44px; }
            .day { grid-template-columns: 1fr; gap: 22px; }
            .grid-3, .grid-2, .meta-strip { grid-template-columns: repeat(2, minmax(0, 1fr)); }
            .hub-grid { grid-template-columns: 1fr; }
            .page-head { padding: 28px 0 22px; }
            section.block { padding: 48px 0; }
        }

        @media (max-width: 620px) {
            .tl-row { grid-template-columns: 1fr; gap: 4px; }
            .rubric-row { grid-template-columns: 1fr; gap: 8px; }
            .win-body { font-size: 0.7rem; }
            .meta-item { padding: 14px 16px; }
            .grid-3, .grid-2, .meta-strip { grid-template-columns: 1fr; }
            .subnav a { padding: 9px 11px; font-size: 0.65rem; }
        }
"""


ABOUT = {
    "@type": "Event",
    "name": "ACM Programming Jam 2026 (JAM.26)",
    "description": "An AI-assisted web engineering event: three preparation workshop days followed by a one-day team competition.",
    "startDate": "2026-09-15",
    "endDate": "2026-09-19",
    "eventStatus": "https://schema.org/EventScheduled",
    "organizer": {
        "@type": "Organization",
        "name": "ACM Student Chapter, College of Computer & Information Sciences, Prince Sultan University",
    },
    "performer": {"@type": "Person", "name": "Shoug Alomran"},
    "location": {"@type": "Place", "name": "Prince Sultan University", "address": "Riyadh, Saudi Arabia"},
    "url": "https://ai-programming-jam.shoug-tech.com/",
}


BODY = """
    <div class="grid-bg" aria-hidden="true"></div>

__HEADER__

    <main id="main-content" tabindex="-1">
        <div class="wrap">
            <div class="breadcrumb">
                <a href="/workshops/">Workshops</a><span class="sep">/</span><span>ACM Programming Jam 2026</span>
            </div>
__SUBNAV__

            <section class="hero">
                <div>
                    <div class="kicker"><span class="dot"></span>Workshop_04 &nbsp;//&nbsp; Authored &amp; Taught</div>
                    <h1><span class="brace">&lt;</span>AI Programming Jam<span class="brace">/&gt;</span></h1>
                    <div class="hero-tagline">// Code. Construct. Create.</div>
                    <p class="hero-lede">
                        ACM Programming Jam 2026 (JAM.26) is an AI-assisted web engineering event at Prince Sultan
                        University. Every team receives the same application brief, then plans it, designs it, builds
                        it, deploys it, and presents it. I wrote the content for all three preparation workshop days,
                        taught them, and built the official event website.
                    </p>
                    <div class="hero-facts">
                        <span>3 Workshop Days</span>
                        <span>15 &middot; 16 &middot; 17 Sep 2026</span>
                        <span>Competition 19 Sep 2026</span>
                        <span>PSU CCIS &middot; ACM</span>
                    </div>
                    <div class="hero-actions">
                        <a class="btn btn-primary" href="https://ai-programming-jam.shoug-tech.com/" target="_blank" rel="noopener">[ Visit the event site -&gt; ]</a>
                        <a class="btn btn-ghost" href="/workshops/ai-programming-jam/workshop-days/">[ Workshop days ]</a>
                        <a class="btn btn-ghost" href="/workshops/">[ &lt;- All workshops ]</a>
                    </div>
                </div>

                <div class="win" aria-hidden="true">
                    <div class="win-bar">
                        <span class="win-dots"><i></i><i></i><i></i></span>
                        <span>jam26 &mdash; build.js</span>
                    </div>
                    <div class="win-body code">
<span class="ln"><span class="c">// one brief, four phases</span></span>
<span class="ln"><span class="k">function</span> <span class="fn">buildIt</span><span class="p">(</span>brief<span class="p">) {</span></span>
<span class="ln">  <span class="k">const</span> plan <span class="p">=</span> <span class="fn">understand</span><span class="p">(</span>brief<span class="p">);</span></span>
<span class="ln">  <span class="k">const</span> ui <span class="p">=</span> <span class="fn">design</span><span class="p">(</span>plan<span class="p">);</span></span>
<span class="ln">  <span class="k">while</span> <span class="p">(!</span>plan<span class="p">.</span>works<span class="p">) {</span></span>
<span class="ln">    <span class="fn">debug</span><span class="p">();</span> <span class="fn">test</span><span class="p">();</span></span>
<span class="ln">  <span class="p">}</span></span>
<span class="ln">  <span class="k">return</span> <span class="fn">ship</span><span class="p">(</span>plan<span class="p">,</span> ui<span class="p">);</span></span>
<span class="ln"><span class="p">}</span><span class="caret"></span></span>
                    </div>
                </div>
            </section>

            <div class="meta-strip">
                <div class="meta-item">
                    <span class="meta-label">Event</span>
                    <span class="meta-value">ACM Programming Jam 2026 &mdash; JAM.26</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">Host</span>
                    <span class="meta-value">ACM Student Chapter &mdash; College of Computer &amp; Information Sciences, Prince Sultan University</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">My role</span>
                    <span class="meta-value">Workshop content author, instructor for all three days, and developer of the official event website</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">Theme</span>
                    <span class="meta-value">AI-assisted web engineering &mdash; plan, build, debug, ship</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">Format</span>
                    <span class="meta-value">3 workshop days + 1 competition day, one shared application brief</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">Schedule</span>
                    <span class="meta-value">Workshops 15, 16 &amp; 17 September 2026 &middot; Competition 19 September 2026 &middot; Time &amp; location announced by the organizers</span>
                </div>
            </div>
        </div>

        <div class="flow" aria-hidden="true">
            <div class="flow-track">
                <span>Plan <span class="hl">-&gt;</span> Build <span class="hl">-&gt;</span> Debug <span class="hl">-&gt;</span> Deploy <span class="hl">-&gt;</span> Adapt <span class="hl">-&gt;</span> Present</span>
                <span class="hl">///</span>
                <span>git commit -m "understand, test, debug, improve"</span>
                <span class="hl">///</span>
                <span>Plan <span class="hl">-&gt;</span> Build <span class="hl">-&gt;</span> Debug <span class="hl">-&gt;</span> Deploy <span class="hl">-&gt;</span> Adapt <span class="hl">-&gt;</span> Present</span>
                <span class="hl">///</span>
                <span>git commit -m "understand, test, debug, improve"</span>
                <span class="hl">///</span>
            </div>
        </div>

        <div class="wrap">
            <section class="block" id="contribution">
                <div class="sect-label">// My contribution</div>
                <h2 class="sect-title">What I built and taught</h2>
                <div class="grid-2">
                    <ul class="contrib">
                        <li><span class="mark">[&gt;]</span> <span>I <strong>wrote the content for all three workshop days</strong> &mdash; planning and development workflow, full-stack development and debugging, and deployment with production readiness &mdash; including the objectives, walkthroughs, and hands-on steps for each session.</span></li>
                        <li><span class="mark">[&gt;]</span> <span>I <strong>taught every one of the three days</strong>. The event site states it plainly: all workshops are developed and taught by Shoug Alomran.</span></li>
                        <li><span class="mark">[&gt;]</span> <span>I <strong>designed and built the official JAM.26 website</strong> at ai-programming-jam.shoug-tech.com &mdash; the workshop pages, competition breakdown, rules, FAQ with search, and the team registration flow.</span></li>
                        <li><span class="mark">[&gt;]</span> <span>I structured the workshops so that the three days rehearse the exact workflow teams use on competition day, rather than teaching tools in isolation.</span></li>
                    </ul>
                    <div class="win term" aria-hidden="true">
                        <div class="win-bar">
                            <span class="win-dots"><i></i><i></i><i></i></span>
                            <span>run_training_sequence.sh</span>
                        </div>
                        <div class="win-body">
<span class="prompt">jam26@sys:~$</span> ./run_training_sequence.sh
<span class="ok">[ok]</span> <span class="out">day_01 &mdash; planning &amp; workflow</span>
<span class="ok">[ok]</span> <span class="out">day_02 &mdash; build &amp; debug</span>
<span class="ok">[ok]</span> <span class="out">day_03 &mdash; deploy &amp; measure</span>
<span class="out">----------------------------------------</span>
<span class="out">build status:</span> <span class="ok">ready</span>
<span class="out">team status: </span> <span class="ok">ready</span>
<span class="out">jam status:  </span> <span class="warn">awaiting challenge</span>
<span class="prompt">jam26@sys:~$</span> <span class="caret"></span>
                        </div>
                    </div>
                </div>
            </section>

            <section class="block" id="journey">
                <div class="sect-label">// The journey</div>
                <h2 class="sect-title">One brief. Four phases. A working application.</h2>
                <p class="sect-intro">Teams receive a single shared application challenge and carry it from requirements
                    all the way to a deployed, measured, demonstrated product.</p>
                <div class="grid-2">
                    <div class="card">
                        <div class="card-num">Phase_01</div>
                        <span class="when">15 September 2026</span>
                        <h3>Understand &amp; Plan</h3>
                        <p>Read the requirements, map how the system works in Excalidraw, and design the interface in Variant.</p>
                    </div>
                    <div class="card">
                        <div class="card-num">Phase_02</div>
                        <span class="when">16 September 2026</span>
                        <h3>Build &amp; Connect</h3>
                        <p>Develop in VS Code with Codex and Claude Code. Add authentication and persistent data with Firebase.</p>
                    </div>
                    <div class="card">
                        <div class="card-num">Phase_03</div>
                        <span class="when">17 September 2026</span>
                        <h3>Deploy &amp; Measure</h3>
                        <p>Version with GitHub, deploy to Vercel, configure the domain in Cloudflare, then measure with PageSpeed Insights.</p>
                    </div>
                    <div class="card">
                        <div class="card-num">Phase_04</div>
                        <span class="when">19 September 2026 &middot; Competition</span>
                        <h3>Adapt &amp; Present</h3>
                        <p>Respond to the unexpected change request, then demonstrate and explain what you built.</p>
                    </div>
                </div>
            </section>

            <section class="block" id="days">
                <div class="sect-label">// Workshop days</div>
                <h2 class="sect-title">Not three workshops. A development workflow.</h2>
                <p class="sect-intro">Three days that take a participant from an idea to a working, deployed web
                    application &mdash; with AI treated as part of the engineering workflow rather than a shortcut around it.</p>

                <div class="day">
                    <div>
                        <div class="day-index">Day_01 // 15 September 2026</div>
                        <h3>Planning &amp; Development Workflow</h3>
                        <p class="focus">Turning a problem into a structured development plan before writing code.</p>
                        <ul class="objectives">
                            <li>Understand requirements and constraints</li>
                            <li>Break a project into features</li>
                            <li>Plan application structure</li>
                            <li>Think about frontend and backend responsibilities</li>
                            <li>Use AI strategically in planning</li>
                        </ul>
                        <div class="status-line">Status: foundation_ready &nbsp;//&nbsp; Output: requirements, architecture, task breakdown</div>
                    </div>
                    <div class="win" aria-hidden="true">
                        <div class="win-bar">
                            <span class="win-dots"><i></i><i></i><i></i></span>
                            <span>jam_project &mdash; requirements.md</span>
                        </div>
                        <div class="win-body code">
<span class="ln"><span class="k"># requirements.md</span></span>
<span class="ln"></span>
<span class="ln"><span class="k">## Core objective</span></span>
<span class="ln"><span class="p">Build a web application that lets users&hellip;</span></span>
<span class="ln"></span>
<span class="ln"><span class="k">## Features</span></span>
<span class="ln"><span class="p">- [</span><span class="fn">x</span><span class="p">] User authentication</span></span>
<span class="ln"><span class="p">- [ ] Real-time dashboard</span></span>
<span class="ln"><span class="p">- [ ] Data visualization widget</span></span>
<span class="ln"></span>
<span class="ln"><span class="c"># frontend/ backend/ architecture/ tasks.md</span></span>
                        </div>
                    </div>
                </div>

                <div class="day">
                    <div>
                        <div class="day-index">Day_02 // 16 September 2026</div>
                        <h3>Full-Stack Development &amp; Debugging</h3>
                        <p class="focus">Turning the plan into a working application and learning how to diagnose problems when things break.</p>
                        <ul class="objectives">
                            <li>Connect frontend and backend logic</li>
                            <li>Work with application state and data</li>
                            <li>Implement and consume APIs</li>
                            <li>Understand errors and debug systematically</li>
                            <li>Use AI to investigate, not just rewrite</li>
                        </ul>
                        <div class="status-line">Status: system_running &nbsp;//&nbsp; Output: a connected frontend, backend, and data layer</div>
                    </div>
                    <div class="win term" aria-hidden="true">
                        <div class="win-bar">
                            <span class="win-dots"><i></i><i></i><i></i></span>
                            <span>~/jam_project/server</span>
                        </div>
                        <div class="win-body">
<span class="prompt">$</span> npm run dev
<span class="out">&gt; starting development server&hellip;</span>
<span class="ok">&#10003;</span> <span class="out">frontend ready on port 3000</span>
<span class="ok">&#10003;</span> <span class="out">api connected</span>
<span class="err">&#10007;</span> <span class="err">error: connection refused (db:5432)</span>
<span class="out">&gt; investigating with the AI assistant&hellip;</span>
<span class="ok">&#10003;</span> <span class="out">resolved: database credentials updated</span>
<span class="prompt">$</span> <span class="caret"></span>
                        </div>
                    </div>
                </div>

                <div class="day">
                    <div>
                        <div class="day-index">Day_03 // 17 September 2026</div>
                        <h3>Deployment, Domains &amp; Production Readiness</h3>
                        <p class="focus">The final preparation stage: take the application from localhost to a real production
                            URL, point a domain at it, make it discoverable, and measure it.</p>
                        <ul class="objectives">
                            <li>Deploy the application with Vercel</li>
                            <li>Configure DNS and the domain in Cloudflare</li>
                            <li>Submit the site to search engines</li>
                            <li>Measure performance with PageSpeed Insights</li>
                            <li>Verify the production build before it is judged</li>
                        </ul>
                        <div class="status-line">Module focus: deploy &rarr; domain &rarr; index &rarr; measure &nbsp;//&nbsp; Status: jam_ready</div>
                    </div>
                    <div class="win term" aria-hidden="true">
                        <div class="win-bar">
                            <span class="win-dots"><i></i><i></i><i></i></span>
                            <span>deployment_readiness</span>
                        </div>
                        <div class="win-body">
<span class="prompt">$</span> vercel --prod
<span class="ok">&#10003;</span> <span class="out">production: https://team.jam26.dev</span>
<span class="prompt">$</span> jam check --readiness
<span class="out">core features&nbsp;&nbsp;&nbsp;&nbsp;</span> <span class="ok">pass</span>
<span class="out">error handling&nbsp;&nbsp;&nbsp;</span> <span class="ok">pass</span>
<span class="out">ui polish&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span> <span class="warn">in_progress</span>
<span class="out">dns + indexing&nbsp;&nbsp;&nbsp;</span> <span class="ok">pass</span>
<span class="out">readiness&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span> <span class="ok">98%</span>
                        </div>
                    </div>
                </div>
            </section>

            <section class="block" id="toolchain">
                <div class="sect-label">// Toolchain</div>
                <h2 class="sect-title">The tools taught across the three days</h2>
                <p class="sect-intro">Each tool is introduced at the point in the workflow where a team actually needs it.</p>
                <div class="stack">
                    <span class="chip"><b>plan</b>Excalidraw</span>
                    <span class="chip"><b>design</b>Variant</span>
                    <span class="chip"><b>build</b>VS Code</span>
                    <span class="chip"><b>build</b>Claude Code</span>
                    <span class="chip"><b>build</b>Codex</span>
                    <span class="chip"><b>data</b>Firebase Auth</span>
                    <span class="chip"><b>data</b>Firebase Persistence</span>
                    <span class="chip"><b>version</b>GitHub</span>
                    <span class="chip"><b>deploy</b>Vercel</span>
                    <span class="chip"><b>domain</b>Cloudflare DNS</span>
                    <span class="chip"><b>index</b>Google Search Console</span>
                    <span class="chip"><b>index</b>Bing Webmaster Tools</span>
                    <span class="chip"><b>measure</b>PageSpeed Insights</span>
                </div>
            </section>

            <section class="block" id="competition">
                <div class="sect-label">// Competition day &middot; 19 September 2026</div>
                <h2 class="sect-title">No tutorial this time. You build it.</h2>
                <p class="sect-intro">Competition day puts everything from the workshops into practice. A team receives the
                    challenge, plans a solution, builds a working web application, adapts to a mid-event change, and presents
                    the result. The brief stays locked until the challenge is released.</p>

                <div class="grid-3">
                    <div class="card"><div class="card-num">01 / Receive</div><p>Teams receive the official application challenge and requirements.</p></div>
                    <div class="card"><div class="card-num">02 / Plan</div><p>Understand the requirements, divide responsibilities, design the solution, and decide how the application will work.</p></div>
                    <div class="card"><div class="card-num">03 / Build</div><p>Turn the plan into a functional web application.</p></div>
                    <div class="card"><div class="card-num">04 / Adapt</div><p>Respond to new information or requirements introduced during the competition.</p></div>
                    <div class="card"><div class="card-num">05 / Submit</div><p>Finalize the application and submit the required project materials before the deadline.</p></div>
                    <div class="card"><div class="card-num">06 / Present</div><p>Demonstrate the finished application and explain the team's engineering decisions.</p></div>
                </div>

                <h3 class="sect-title" style="font-size: 1.5rem; margin: 48px 0 18px;">Scoring &mdash; 100 points across seven categories</h3>
                <div class="rubric">
                    <div class="rubric-row">
                        <div class="rubric-weight">20%</div>
                        <div>
                            <div class="rubric-name">Functional Completeness</div>
                            <p class="rubric-desc">Does the application meet the provided requirements and function correctly?</p>
                            <div class="bar"><i style="width: 20%"></i></div>
                        </div>
                    </div>
                    <div class="rubric-row">
                        <div class="rubric-weight">20%</div>
                        <div>
                            <div class="rubric-name">Technical Implementation</div>
                            <p class="rubric-desc">How effectively were authentication, persistent data, application logic, GitHub, and deployment implemented?</p>
                            <div class="bar"><i style="width: 20%"></i></div>
                        </div>
                    </div>
                    <div class="rubric-row">
                        <div class="rubric-weight">20%</div>
                        <div>
                            <div class="rubric-name">Problem Solving &amp; Adaptability</div>
                            <p class="rubric-desc">How effectively did the team debug problems and respond to the unexpected requirement change?</p>
                            <div class="bar"><i style="width: 20%"></i></div>
                        </div>
                    </div>
                    <div class="rubric-row">
                        <div class="rubric-weight">15%</div>
                        <div>
                            <div class="rubric-name">UI/UX &amp; Design</div>
                            <p class="rubric-desc">Is the application intuitive, coherent, responsive, and easy to use?</p>
                            <div class="bar"><i style="width: 15%"></i></div>
                        </div>
                    </div>
                    <div class="rubric-row">
                        <div class="rubric-weight">10%</div>
                        <div>
                            <div class="rubric-name">System Understanding &amp; Planning</div>
                            <p class="rubric-desc">Can the team explain its Excalidraw diagram and how the major parts of the system interact?</p>
                            <div class="bar"><i style="width: 10%"></i></div>
                        </div>
                    </div>
                    <div class="rubric-row">
                        <div class="rubric-weight">10%</div>
                        <div>
                            <div class="rubric-name">Production Readiness &amp; Performance</div>
                            <p class="rubric-desc">Has the application been deployed correctly, connected to a domain, prepared for search discovery, and evaluated with PageSpeed Insights?</p>
                            <div class="bar"><i style="width: 10%"></i></div>
                        </div>
                    </div>
                    <div class="rubric-row">
                        <div class="rubric-weight">5%</div>
                        <div>
                            <div class="rubric-name">Final Demonstration</div>
                            <p class="rubric-desc">Can the team clearly demonstrate and explain its solution?</p>
                            <div class="bar"><i style="width: 5%"></i></div>
                        </div>
                    </div>
                </div>

                <div class="grid-2" style="margin-top: 48px; align-items: start;">
                    <div>
                        <h3 class="sect-title" style="font-size: 1.5rem; margin-bottom: 16px;">The day</h3>
                        <div class="timeline">
                            <div class="tl-row"><span class="tl-key">check_in</span><span class="tl-val">Time TBD</span></div>
                            <div class="tl-row"><span class="tl-key">challenge_release</span><span class="tl-val">Time TBD</span></div>
                            <div class="tl-row"><span class="tl-key">planning</span><span class="tl-val">Time TBD</span></div>
                            <div class="tl-row"><span class="tl-key">development</span><span class="tl-val">Time TBD</span></div>
                            <div class="tl-row alert"><span class="tl-key">change_event</span><span class="tl-val">Time TBD</span></div>
                            <div class="tl-row"><span class="tl-key">final_build</span><span class="tl-val">Time TBD</span></div>
                            <div class="tl-row"><span class="tl-key">submission</span><span class="tl-val">Time TBD</span></div>
                            <div class="tl-row"><span class="tl-key">presentations</span><span class="tl-val">Time TBD</span></div>
                            <div class="tl-row"><span class="tl-key">results</span><span class="tl-val">Time TBD</span></div>
                        </div>
                        <div class="callout" style="margin-top: 22px;">
                            <b>Expect change.</b> Real software projects rarely stay exactly as planned. A new requirement is
                            introduced mid-event, and teams have to adapt the application they already built.
                        </div>
                    </div>
                    <div>
                        <h3 class="sect-title" style="font-size: 1.5rem; margin-bottom: 16px;">What judges check</h3>
                        <ul class="contrib" style="margin-bottom: 26px;">
                            <li><span class="mark">01</span> <span><strong>Required evidence.</strong> A working production URL, the GitHub repository, the final application, the Excalidraw system plan, and evidence that the team tested and measured the result.</span></li>
                            <li><span class="mark">02</span> <span><strong>Live verification.</strong> Judges may navigate the deployed application, test core requirements, review authentication and persistent data, inspect responsive behavior, and ask the team to explain implementation decisions.</span></li>
                            <li><span class="mark">03</span> <span><strong>Team demonstration.</strong> Present the problem, demonstrate the main user journey, explain the system, show how the change request was handled, and identify one challenge the team investigated.</span></li>
                            <li><span class="mark">04</span> <span><strong>Completion check.</strong> Confirm required tasks are complete, roles are clear, accounts and access work, materials are ready, and the final production build has been verified.</span></li>
                        </ul>
                        <h3 class="sect-title" style="font-size: 1.5rem; margin-bottom: 16px;">Submission checklist</h3>
                        <ul class="checklist">
                            <li>Live production website</li>
                            <li>Custom domain or subdomain</li>
                            <li>GitHub repository</li>
                            <li>Excalidraw functional diagram</li>
                            <li>Working Firebase authentication</li>
                            <li>Working persistent data</li>
                            <li>Required application features</li>
                            <li>Completed change request</li>
                            <li>Google Search Console setup</li>
                            <li>Bing Webmaster Tools setup</li>
                            <li>PageSpeed Insights result</li>
                        </ul>
                    </div>
                </div>
            </section>

            <section class="block" id="rules">
                <div class="sect-label">// Rules</div>
                <h2 class="sect-title">Build freely. Compete fairly.</h2>
                <p class="sect-intro">This is an AI programming jam: AI may generate part or all of an application, and there
                    is no requirement to hand-write a set amount of code. The restrictions exist to keep that freedom fair,
                    not to limit AI-assisted development. If something is not prohibited, it is generally permitted &mdash;
                    and when a team is unsure, they ask an organizer first.</p>

                <div class="tiers">
                    <div class="tier allow">
                        <div class="lvl">Free tier</div>
                        <div class="verdict">Allowed</div>
                        <div class="eg">e.g. ChatGPT Free</div>
                    </div>
                    <div class="tier allow">
                        <div class="lvl">Standard paid tier</div>
                        <div class="verdict">Allowed</div>
                        <div class="eg">e.g. ChatGPT Plus</div>
                    </div>
                    <div class="tier deny">
                        <div class="lvl">Highest / advanced tier</div>
                        <div class="verdict">Not allowed</div>
                        <div class="eg">e.g. ChatGPT Pro</div>
                    </div>
                    <div class="tier allow">
                        <div class="lvl">AI-generated code</div>
                        <div class="verdict">Allowed</div>
                        <div class="eg">Including a full AI build</div>
                    </div>
                </div>
                <p class="sect-intro" style="margin-top: 16px;">The same principle applies to equivalent plans from other AI
                    providers. AI is part of the jam; pay-to-win is not.</p>

                <div class="grid-3" style="margin-top: 28px;">
                    <div class="rule">
                        <div class="rule-id">Rule_01</div>
                        <h3>AI Tier Limit</h3>
                        <p>Do not use the highest-tier AI plans, models, or features prohibited by the organizers. Standard paid consumer plans are allowed.</p>
                        <span class="note">// Organizers may publish an approved AI access list before the competition.</span>
                    </div>
                    <div class="rule">
                        <div class="rule-id">Rule_02</div>
                        <h3>Outside Human Assistance</h3>
                        <p>Do not receive coding, debugging, design, architecture, implementation, or problem-solving assistance from anyone outside your registered team during the competition.</p>
                        <span class="note">// AI assistance is allowed.</span>
                    </div>
                    <div class="rule">
                        <div class="rule-id">Rule_03</div>
                        <h3>Cross-Team Collaboration</h3>
                        <p>Do not share code, prompts, solutions, implementation details, debugging solutions, or challenge-specific strategies with another competing team.</p>
                        <span class="note">// Your own team may collaborate freely.</span>
                    </div>
                    <div class="rule">
                        <div class="rule-id">Rule_04</div>
                        <h3>Building Before the Competition</h3>
                        <p>Do not begin building a solution specifically for the competition challenge before the challenge is officially released.</p>
                        <span class="note">// The competition begins at challenge release.</span>
                    </div>
                    <div class="rule">
                        <div class="rule-id">Rule_05</div>
                        <h3>Pre-Built or Copied Solutions</h3>
                        <p>Do not submit an existing application, another team's work, or a project substantially created before the competition.</p>
                        <span class="note">// Public libraries, frameworks, packages and documentation are fine.</span>
                    </div>
                    <div class="rule">
                        <div class="rule-id">Rule_06</div>
                        <h3>Ignoring the Change Requirement</h3>
                        <p>Do not ignore the additional requirement introduced during the competition. Teams must adapt their existing application to satisfy the updated requirements.</p>
                        <span class="note">// requirements_v1 -&gt; change_detected -&gt; requirements_v2</span>
                    </div>
                    <div class="rule">
                        <div class="rule-id">Rule_07</div>
                        <h3>Interfering with Other Teams</h3>
                        <p>Do not access, modify, sabotage, disrupt, or intentionally interfere with another team's application, repository, accounts, files, or development environment.</p>
                    </div>
                    <div class="rule">
                        <div class="rule-id">Rule_08</div>
                        <h3>Unauthorized Credentials or Secrets</h3>
                        <p>Do not use another team's credentials, API keys, tokens, accounts, or private resources, or intentionally obtain or misuse private credentials.</p>
                    </div>
                    <div class="rule">
                        <div class="rule-id">Rule_09</div>
                        <h3>False Representation</h3>
                        <p>Do not misrepresent what your team built, who contributed, when work was completed, or whether functionality actually works.</p>
                    </div>
                    <div class="rule">
                        <div class="rule-id">Rule_10</div>
                        <h3>Working After the Deadline</h3>
                        <p>Do not modify the judged submission after the official deadline unless organizers explicitly authorize it. The version submitted at the deadline is the version evaluated.</p>
                    </div>
                    <div class="rule">
                        <div class="rule-id">Rule_11</div>
                        <h3>Rule Evasion</h3>
                        <p>Do not intentionally exploit ambiguities, loopholes, or technicalities in the rules to gain an unfair advantage.</p>
                        <span class="note">// When in doubt: ask.</span>
                    </div>
                    <div class="rule" style="border-color: var(--accent-line);">
                        <div class="rule-id" style="color: var(--accent);">Primary directive</div>
                        <h3>When in doubt, ask</h3>
                        <p>If a situation is unclear, ask an organizer before proceeding. Organizers may clarify the rules when necessary to keep the competition fair.</p>
                    </div>
                </div>
            </section>

            <section class="block" id="faq">
                <div class="sect-label">// FAQ</div>
                <h2 class="sect-title">Questions? Let's debug them.</h2>

                <div class="faq-group">
                    <div class="faq-group-title">01 / Getting started</div>
                    <details class="faq"><summary>Do I need web development experience?</summary><div class="answer"><b>No.</b> The Programming Jam is designed to be approachable for participants who are still learning. The preparation workshops introduce the development workflow and the tools used throughout the event.</div></details>
                    <details class="faq"><summary>Do I need to be an experienced programmer?</summary><div class="answer"><b>No.</b> You should be willing to learn, experiment, solve problems, and work with your team. AI is intentionally part of the development process.</div></details>
                    <details class="faq"><summary>Who can participate?</summary><div class="answer">University students who complete registration may participate. Final eligibility details are confirmed by the organizers before the event.</div></details>
                    <details class="faq"><summary>What should I bring?</summary><div class="answer">A laptop, charger, and access to the email and development accounts you plan to use. Install a modern browser, Visual Studio Code, Git, and Node.js in advance.</div></details>
                </div>

                <div class="faq-group">
                    <div class="faq-group-title">02 / Teams</div>
                    <details class="faq"><summary>Do I need a team before registering?</summary><div class="answer"><b>No.</b> Participants without a team can use the team formation process to create or join one.</div></details>
                    <details class="faq"><summary>Can I participate alone?</summary><div class="answer"><b>Yes.</b> You may register alone, and the team-formation process can help you join or create a team.</div></details>
                    <details class="faq"><summary>How many people can be on a team?</summary><div class="answer">A team may include the primary registrant and up to ten additional member email addresses. Only registered team members may collaborate on the competition solution.</div></details>
                    <details class="faq"><summary>Can I change teams?</summary><div class="answer">Request team changes through the organizer contact form before competition day. Changes are valid only after organizers confirm the updated roster.</div></details>
                </div>

                <div class="faq-group">
                    <div class="faq-group-title">03 / AI &amp; tools</div>
                    <details class="faq"><summary>Can AI generate my entire website?</summary><div class="answer"><b>Yes.</b> AI may generate part or all of your application. There is no requirement to manually write a specific percentage of the code.</div></details>
                    <details class="faq"><summary>Can I use ChatGPT Plus?</summary><div class="answer"><b>Yes.</b> Standard paid consumer AI plans such as ChatGPT Plus are allowed. The highest-tier or advanced premium plans, such as ChatGPT Pro, are not.</div></details>
                    <details class="faq"><summary>What about Claude, Gemini, or other AI tools?</summary><div class="answer">Participants are not restricted to one AI provider. The same access principle applies: free and standard paid consumer tiers are permitted, the highest-tier or advanced premium access is not. If unsure about a specific plan, ask an organizer.</div></details>
                    <details class="faq"><summary>Does my team have to understand AI-generated code?</summary><div class="answer">Your team is responsible for the final application. If something breaks, you must be able to investigate the problem, direct your tools toward a solution, test the result, and verify that the application works.</div></details>
                </div>

                <div class="faq-group">
                    <div class="faq-group-title">04 / Workshops</div>
                    <details class="faq"><summary>What will the workshops teach?</summary><div class="answer">Day 01 covers planning and the development workflow. Day 02 covers full-stack development and debugging. Day 03 covers deployment, domains, search discovery, and performance. Together they walk through the same workflow used on competition day.</div></details>
                    <details class="faq"><summary>Do I have to attend the workshops to compete?</summary><div class="answer">Attendance is strongly recommended, because the competition assumes familiarity with the full workflow. Participants remain responsible for the published presentation material and the handout checklists before competition day.</div></details>
                    <details class="faq"><summary>Who teaches them?</summary><div class="answer">All three workshop days are developed and taught by <b>Shoug Alomran</b>.</div></details>
                </div>

                <div class="faq-group">
                    <div class="faq-group-title">05 / Competition</div>
                    <details class="faq"><summary>What are we building?</summary><div class="answer">That is part of the challenge. Teams receive the official application brief when the challenge is released on competition day.</div></details>
                    <details class="faq"><summary>Can we start building before the competition?</summary><div class="answer"><b>No.</b> Teams may prepare and practice, but may not begin building a solution for the competition challenge before it is officially released.</div></details>
                    <details class="faq"><summary>Will the requirements change?</summary><div class="answer">Teams should be prepared to adapt during the competition.</div></details>
                    <details class="faq"><summary>Can teams help each other?</summary><div class="answer"><b>No.</b> Competing teams may not share challenge-specific code, prompts, solutions, debugging fixes, implementation details, or strategies during the competition.</div></details>
                </div>

                <div class="faq-group">
                    <div class="faq-group-title">06 / Submission</div>
                    <details class="faq"><summary>Does the website need to be deployed?</summary><div class="answer"><b>Yes.</b> The final application must be publicly accessible for judging, deployed and connected to a domain or subdomain.</div></details>
                    <details class="faq"><summary>Can we keep working after the deadline?</summary><div class="answer"><b>No.</b> The judged submission may not be modified after the official deadline unless organizers explicitly authorize it.</div></details>
                    <details class="faq"><summary>How will projects be judged?</summary><div class="answer">Out of 100 points across seven categories: functional completeness, technical implementation, problem solving and adaptability, UI/UX, system understanding, production readiness, and the final demonstration.</div></details>
                </div>
            </section>
        </div>

        <div class="wrap">
            <div class="cta">
                <div class="sect-label">// jam.26</div>
                <h2>Think. Build. Adapt. Ship.</h2>
                <p>The workshops give teams the workflow. Competition day tests what they can do with it &mdash; without the
                    tutorial wheels.</p>
                <div class="hero-actions">
                    <a class="btn btn-primary" href="https://ai-programming-jam.shoug-tech.com/" target="_blank" rel="noopener">[ ai-programming-jam.shoug-tech.com ]</a>
                    <a class="btn btn-ghost" href="/workshops/">[ &lt;- All workshops ]</a>
                </div>
            </div>
        </div>
    </main>

__FOOTER__
"""



HUB_CARDS = """
            <section class="block" id="explore">
                <div class="sect-label">// Sections</div>
                <h2 class="sect-title">Open a section</h2>
                <p class="sect-intro">The event is documented across four pages: what the three workshop days teach,
                    how competition day runs and is scored, the rules that govern AI use, and the questions participants
                    ask most.</p>
                <div class="hub-grid">
                    <a class="hub-card" href="/workshops/ai-programming-jam/workshop-days/">
                        <div class="hub-card-top"><span>01 // Workshops</span><span class="file">days.md</span></div>
                        <h3>Workshop Days</h3>
                        <p>Three days that take a participant from an idea to a working, deployed web application:
                            planning and workflow, full-stack development and debugging, then deployment, domains and
                            production readiness.</p>
                        <div class="hub-meta"><span>15 &middot; 16 &middot; 17 Sep 2026</span><span class="arrow">-&gt;</span></div>
                    </a>
                    <a class="hub-card" href="/workshops/ai-programming-jam/competition/">
                        <div class="hub-card-top"><span>02 // Competition</span><span class="file">jam.md</span></div>
                        <h3>Competition Day</h3>
                        <p>The six-step competition loop, the 100-point rubric across seven categories, the timeline of
                            the day, what judges verify, and the full submission checklist.</p>
                        <div class="hub-meta"><span>19 Sep 2026</span><span class="arrow">-&gt;</span></div>
                    </a>
                    <a class="hub-card" href="/workshops/ai-programming-jam/rules/">
                        <div class="hub-card-top"><span>03 // Rules</span><span class="file">rules.md</span></div>
                        <h3>Rules &amp; AI Policy</h3>
                        <p>AI may write the whole application &mdash; within limits. The AI access tiers, and the eleven
                            things a team cannot do.</p>
                        <div class="hub-meta"><span>11 rules</span><span class="arrow">-&gt;</span></div>
                    </a>
                    <a class="hub-card" href="/workshops/ai-programming-jam/faq/">
                        <div class="hub-card-top"><span>04 // FAQ</span><span class="file">faq.md</span></div>
                        <h3>Questions</h3>
                        <p>Experience needed, team size and formation, which AI plans are allowed, what the workshops
                            cover, and what each team has to submit.</p>
                        <div class="hub-meta"><span>6 categories</span><span class="arrow">-&gt;</span></div>
                    </a>
                </div>
            </section>
"""

CTA = """
        <div class="wrap">
            <div class="cta">
                <div class="sect-label">// jam.26</div>
                <h2>Think. Build. Adapt. Ship.</h2>
                <p>The workshops give teams the workflow. Competition day tests what they can do with it &mdash; without the
                    tutorial wheels.</p>
                <div class="hero-actions">
                    <a class="btn btn-primary" href="https://ai-programming-jam.shoug-tech.com/" target="_blank" rel="noopener">[ ai-programming-jam.shoug-tech.com ]</a>
                    <a class="btn btn-ghost" href="/workshops/">[ &lt;- All workshops ]</a>
                </div>
            </div>
        </div>
"""


PAGES = (
    Page(
        slug="",
        filename="",
        label="Overview",
        title=TITLE,
        description=DESCRIPTION,
    ),
    Page(
        slug="workshop-days/",
        label="Workshop days",
        filename="workshop-days",
        title="JAM.26 Workshop Days // SHOUG.TECH",
        description=(
            "The three ACM Programming Jam 2026 workshop days, written and taught by Shoug Alomran: planning and "
            "development workflow, full-stack development and debugging, and deployment, domains and production "
            "readiness, plus the toolchain taught across them."
        ),
        eyebrow="ACM Programming Jam 2026 // Section 01",
        heading="Workshop Days",
        sections=("days", "toolchain"),
    ),
    Page(
        slug="competition/",
        label="Competition",
        filename="competition",
        title="JAM.26 Competition Day // SHOUG.TECH",
        description=(
            "How ACM Programming Jam 2026 competition day runs: the six-step competition loop, the 100-point rubric "
            "across seven categories, the timeline of the day, what judges verify, and the submission checklist."
        ),
        eyebrow="ACM Programming Jam 2026 // Section 02",
        heading="Competition Day",
        sections=("competition",),
    ),
    Page(
        slug="rules/",
        label="Rules",
        filename="rules",
        title="JAM.26 Rules &amp; AI Policy // SHOUG.TECH",
        description=(
            "The ACM Programming Jam 2026 rules: which AI plans and tiers teams may use, and the eleven prohibited "
            "actions that keep AI-assisted development fair between teams."
        ),
        eyebrow="ACM Programming Jam 2026 // Section 03",
        heading="Rules",
        sections=("rules",),
    ),
    Page(
        slug="faq/",
        label="FAQ",
        filename="faq",
        title="JAM.26 FAQ // SHOUG.TECH",
        description=(
            "Frequently asked questions about ACM Programming Jam 2026: experience required, teams and team size, "
            "permitted AI tools and plans, what the workshops teach, competition day, and what each team submits."
        ),
        eyebrow="ACM Programming Jam 2026 // Section 04",
        heading="FAQ",
        sections=("faq",),
    ),

)

EVENT = Event(root=ROOT, base=BASE, css=THEME_CSS, pages=PAGES, about=ABOUT,
              nav_label=EVENT_LABEL)


def build_hub(chrome: dict[str, str], parts: dict[str, str]) -> str:
    body = (
        parts["intro"].replace("__SUBNAV__", subnav(EVENT, ""))
        + parts["contribution"]
        + parts["journey"]
        + HUB_CARDS
        + "        </div>\n"
        + CTA
        + "    </main>\n\n__FOOTER__\n"
    )
    return render(EVENT, chrome, body, url=EVENT.canonical, title=TITLE, description=DESCRIPTION)


def main() -> int:
    chrome = extract_chrome()
    parts = split_sections(BODY)
    files = [(ROOT / "index.html", build_hub(chrome, parts))]
    for page in PAGES[1:]:
        files.append((ROOT / page.filename / "index.html", build_subpage(EVENT, chrome, parts, page, EVENT_LABEL)))
    return write(files)


if __name__ == "__main__":
    raise SystemExit(main())
