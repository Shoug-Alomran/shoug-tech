#!/usr/bin/env python3
"""Build the ACM/CyberTech CTF 3.0 pages under /workshops/psu-ctf-3/.

Content is written once as a single-page BODY and split into the hub plus five
sub-pages; the shared chrome, CSS and page shells come from event_page_kit.
"""

from __future__ import annotations

from event_page_kit import (
    DOCS,
    Event,
    Page,
    build_subpage,
    extract_chrome,
    render,
    split_sections,
    subnav,
    write,
)

ROOT = DOCS / "workshops" / "psu-ctf-3"
BASE = "/workshops/psu-ctf-3/"
EVENT_LABEL = "ACM/CyberTech CTF 3.0"

TITLE = "ACM/CyberTech CTF 3.0 // SHOUG.TECH"
DESCRIPTION = (
    "ACM/CyberTech CTF 3.0 at Prince Sultan University — a three-hour capture-the-flag "
    "competition across cryptography, web, forensics and OSINT on 24 October 2026. I built "
    "the official competition website and co-organize the event as ACM Vice President."
)

ABOUT = {
    "@type": "Event",
    "name": "ACM/CyberTech CTF 3.0",
    "description": "A three-hour jeopardy-style capture-the-flag competition across cryptography, web, forensics and OSINT, hosted by the ACM Club and CyberTech Club at Prince Sultan University.",
    "startDate": "2026-10-24T10:00+03:00",
    "endDate": "2026-10-24T13:00+03:00",
    "eventStatus": "https://schema.org/EventScheduled",
    "organizer": {
        "@type": "Organization",
        "name": "ACM Club & CyberTech Club, College of Computer & Information Sciences, Prince Sultan University",
    },
    "location": {
        "@type": "Place",
        "name": "Auditorium B105, Prince Sultan University",
        "address": "Riyadh, Saudi Arabia",
    },
    "url": "https://ctf-psu.shoug-tech.com/",
}

THEME_CSS = """
        /* ── CTF 3.0 — cyber range console ──────────────────────────────
           Monospace-first, CRT scanlines, clipped HUD panels and a hard
           cyan/alert-red signal palette. Nothing here is shared with the
           other event pages. */
        :root {
            --void: #04070e;
            --panel: #08111d;
            --panel-2: #0c1826;
            --ink: #e6f6ff;
            --dim: #8ba7c0;
            --faint: #59748d;
            --line: rgba(0, 240, 255, 0.16);
            --line-hard: rgba(0, 240, 255, 0.4);
            --cyan: #00f0ff;
            --alert: #ff2a4b;
            --lime: #44ff9a;
            --amber: #ffc857;
            --mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, monospace;
            --display: 'Rajdhani', sans-serif;
        }

        body {
            background: var(--void);
            color: var(--ink);
            font-family: var(--mono);
            font-size: 0.86rem;
            line-height: 1.7;
        }

        ::selection { background: var(--cyan); color: #02121b; }

        /* CRT scanlines + faint sweep, the signature of this page */
        .scan {
            position: fixed;
            inset: 0;
            z-index: 0;
            pointer-events: none;
            background:
                repeating-linear-gradient(0deg, rgba(0, 0, 0, 0.22) 0 1px, transparent 1px 3px),
                radial-gradient(ellipse 70% 50% at 50% 0%, rgba(0, 240, 255, 0.07), transparent 70%);
            mix-blend-mode: normal;
        }
        main, header, footer { position: relative; z-index: 1; }

        /* ── rails and section headers ─────────────────────────────── */
        .rail {
            border-top: 1px solid var(--line);
            border-bottom: 1px solid var(--line);
            background: linear-gradient(90deg, rgba(0, 240, 255, 0.06), transparent 60%);
            display: flex;
            flex-wrap: wrap;
            gap: 26px;
            padding: 9px 0;
            font-size: 0.66rem;
            letter-spacing: 0.22em;
            text-transform: uppercase;
            color: var(--faint);
        }
        .rail b { color: var(--cyan); font-weight: 500; }
        .rail .live { color: var(--lime); }

        .breadcrumb {
            padding: 22px 0 0;
            font-size: 0.64rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: var(--faint);
        }
        .breadcrumb a { color: var(--dim); text-decoration: none; }
        .breadcrumb a:hover { color: var(--cyan); }
        .breadcrumb .sep { color: var(--line-hard); margin: 0 8px; }

        /* command-bar navigation, not tabs */
        .subnav {
            display: flex;
            flex-wrap: wrap;
            gap: 0;
            margin: 16px 0 0;
            border: 1px solid var(--line);
            background: var(--panel);
        }
        .subnav a {
            font-size: 0.68rem;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            text-decoration: none;
            color: var(--dim);
            padding: 11px 18px;
            border-right: 1px solid var(--line);
            transition: background 0.15s linear, color 0.15s linear;
        }
        .subnav a::before { content: "> "; color: var(--faint); }
        .subnav a:hover { background: rgba(0, 240, 255, 0.08); color: var(--cyan); }
        .subnav a.active { background: var(--cyan); color: #02121b; font-weight: 700; }
        .subnav a.active::before { content: "> "; color: #02121b; }

        .sec-head {
            display: flex;
            align-items: center;
            gap: 14px;
            margin: 0 0 12px;
            font-size: 0.66rem;
            letter-spacing: 0.26em;
            text-transform: uppercase;
            color: var(--cyan);
        }
        .sec-head::after {
            content: "";
            flex: 1;
            height: 1px;
            background: repeating-linear-gradient(90deg, var(--line-hard) 0 6px, transparent 6px 12px);
        }

        h2.sec-title,
        .page-head h1 {
            font-family: var(--display);
            font-weight: 700;
            text-transform: uppercase;
            line-height: 0.95;
            letter-spacing: 0.01em;
        }
        h2.sec-title { font-size: clamp(1.8rem, 4vw, 2.9rem); margin-bottom: 14px; }
        h3.sub-title {
            font-family: var(--display);
            font-size: 1.35rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin: 46px 0 16px;
            color: var(--ink);
        }
        p.lede { color: var(--dim); max-width: 78ch; font-family: 'Inter', system-ui, sans-serif; font-size: 0.95rem; }

        section.block { padding: 54px 0; }
        section.block + section.block { border-top: 1px solid var(--line); }

        /* ── hero console ──────────────────────────────────────────── */
        .console {
            margin: 22px 0 0;
            border: 1px solid var(--line-hard);
            background:
                linear-gradient(180deg, rgba(0, 240, 255, 0.05), transparent 40%),
                var(--panel);
            position: relative;
        }
        .console::before,
        .console::after {
            content: "";
            position: absolute;
            width: 14px;
            height: 14px;
            border: 2px solid var(--cyan);
        }
        .console::before { top: -1px; left: -1px; border-right: 0; border-bottom: 0; }
        .console::after { bottom: -1px; right: -1px; border-left: 0; border-top: 0; }

        .console-top {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            gap: 12px;
            padding: 10px 20px;
            border-bottom: 1px solid var(--line);
            font-size: 0.64rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: var(--faint);
        }
        .console-top .on { color: var(--lime); }
        .console-body { padding: 34px 30px 30px; }

        .tag-line {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            border: 1px solid var(--alert);
            color: var(--alert);
            padding: 5px 12px;
            font-size: 0.64rem;
            letter-spacing: 0.22em;
            text-transform: uppercase;
        }
        .blink { width: 7px; height: 7px; background: var(--alert); animation: bl 1.1s steps(2) infinite; }
        @keyframes bl { 50% { opacity: 0.15; } }

        .console h1 {
            font-family: var(--display);
            font-weight: 700;
            font-size: clamp(2.6rem, 7vw, 5.4rem);
            line-height: 0.9;
            text-transform: uppercase;
            margin: 20px 0 6px;
            text-shadow: 2px 0 0 rgba(255, 42, 75, 0.55), -2px 0 0 rgba(0, 240, 255, 0.55);
        }
        .console h1 em { font-style: normal; color: var(--cyan); }
        .console .sub {
            color: var(--cyan);
            font-size: clamp(0.9rem, 2vw, 1.15rem);
            letter-spacing: 0.06em;
            margin-bottom: 20px;
        }
        .console p.brief {
            font-family: 'Inter', system-ui, sans-serif;
            color: var(--dim);
            max-width: 68ch;
            font-size: 0.97rem;
            line-height: 1.65;
        }

        /* HUD readouts with dotted leaders */
        .hud {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            border-top: 1px solid var(--line);
            margin-top: 30px;
        }
        .hud div {
            padding: 18px 20px 16px;
            border-right: 1px solid var(--line);
        }
        .hud div:last-child { border-right: 0; }
        .hud .k {
            display: block;
            font-size: 0.6rem;
            letter-spacing: 0.24em;
            color: var(--faint);
            text-transform: uppercase;
            margin-bottom: 7px;
        }
        .hud .v {
            font-family: var(--display);
            font-size: 1.5rem;
            line-height: 1;
            text-transform: uppercase;
            color: var(--cyan);
        }
        .hud .v small { display: block; font-family: var(--mono); font-size: 0.66rem; color: var(--dim); letter-spacing: 0.14em; margin-top: 6px; }

        .cmds { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 26px; }
        .cmd {
            font-size: 0.7rem;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            text-decoration: none;
            padding: 12px 18px;
            border: 1px solid var(--line-hard);
            color: var(--cyan);
            background: rgba(0, 240, 255, 0.06);
            transition: background 0.15s linear, color 0.15s linear;
        }
        .cmd:hover { background: var(--cyan); color: #02121b; }
        .cmd.solid { background: var(--cyan); color: #02121b; font-weight: 700; }
        .cmd.solid:hover { background: transparent; color: var(--cyan); }
        .cmd.red { border-color: var(--alert); color: var(--alert); background: rgba(255, 42, 75, 0.07); }
        .cmd.red:hover { background: var(--alert); color: #12010a; }

        /* ── terminal block ────────────────────────────────────────── */
        .term {
            border: 1px solid var(--line);
            background: var(--panel-2);
            padding: 18px 20px;
            font-size: 0.78rem;
            line-height: 1.85;
            white-space: pre-wrap;
            overflow-x: auto;
        }
        .term .p { color: var(--cyan); }
        .term .o { color: var(--dim); }
        .term .ok { color: var(--lime); }
        .term .no { color: var(--alert); }
        .term .wa { color: var(--amber); }
        .caret { display: inline-block; width: 8px; height: 1em; background: var(--cyan); vertical-align: -2px; animation: bl 1.1s steps(2) infinite; }

        /* ── dossier / vector panels (clipped corners) ─────────────── */
        .vectors { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }
        .vector {
            position: relative;
            border: 1px solid var(--line);
            background: var(--panel);
            padding: 24px 26px 26px;
            clip-path: polygon(0 0, calc(100% - 18px) 0, 100% 18px, 100% 100%, 18px 100%, 0 calc(100% - 18px));
            transition: border-color 0.18s linear, background 0.18s linear;
        }
        .vector:hover { border-color: var(--line-hard); background: var(--panel-2); }
        .vector .idx {
            position: absolute;
            right: 18px;
            bottom: 2px;
            font-family: var(--display);
            font-size: 4.6rem;
            line-height: 1;
            color: rgba(0, 240, 255, 0.07);
        }
        .vector .cat { font-size: 0.64rem; letter-spacing: 0.24em; text-transform: uppercase; color: var(--cyan); }
        .vector h3 {
            font-family: var(--display);
            font-size: 1.45rem;
            text-transform: uppercase;
            margin: 8px 0 10px;
        }
        .vector p { color: var(--dim); font-family: 'Inter', system-ui, sans-serif; font-size: 0.92rem; }
        .tags { display: flex; flex-wrap: wrap; gap: 7px; margin-top: 16px; }
        .tags span { font-size: 0.62rem; letter-spacing: 0.14em; text-transform: uppercase; color: var(--faint); }
        .tags span::before { content: "["; color: var(--line-hard); margin-right: 3px; }
        .tags span::after { content: "]"; color: var(--line-hard); margin-left: 3px; }

        /* ── segmented difficulty meter ────────────────────────────── */
        .meter { display: grid; gap: 8px; }
        .meter-row {
            display: grid;
            grid-template-columns: 130px 1fr;
            gap: 18px;
            align-items: center;
            font-size: 0.7rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: var(--dim);
        }
        .blocks { display: flex; gap: 5px; }
        .blocks i { width: 34px; height: 10px; background: rgba(0, 240, 255, 0.12); display: block; }
        .blocks i.on { background: var(--cyan); }
        .meter-row.hot .blocks i.on { background: var(--alert); }
        .meter-row.hot { color: var(--alert); }

        /* ── protocol steps ────────────────────────────────────────── */
        .steps { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 0; border: 1px solid var(--line); }
        .steps div { padding: 20px 18px; border-right: 1px solid var(--line); background: var(--panel); }
        .steps div:last-child { border-right: 0; }
        .steps .n { font-family: var(--display); font-size: 2rem; line-height: 1; color: var(--cyan); }
        .steps h4 { font-size: 0.68rem; letter-spacing: 0.18em; text-transform: uppercase; margin: 10px 0 8px; font-weight: 500; }
        .steps p { font-size: 0.74rem; color: var(--faint); line-height: 1.6; }

        /* ── ledger rules ──────────────────────────────────────────── */
        .ledger { border-top: 1px solid var(--line); }
        .ledger article {
            display: grid;
            grid-template-columns: 108px minmax(0, 1fr);
            gap: 24px;
            padding: 20px 0;
            border-bottom: 1px solid var(--line);
        }
        .ledger article:hover { background: rgba(0, 240, 255, 0.03); }
        .ledger .rid { font-size: 0.66rem; letter-spacing: 0.2em; color: var(--alert); text-transform: uppercase; }
        .ledger h3 { font-family: var(--display); font-size: 1.15rem; text-transform: uppercase; margin-bottom: 6px; }
        .ledger p { color: var(--dim); font-family: 'Inter', system-ui, sans-serif; font-size: 0.92rem; }
        .ledger .note { display: block; margin-top: 8px; font-size: 0.7rem; color: var(--faint); }

        /* ── leaderboard ───────────────────────────────────────────── */
        .board { width: 100%; border-collapse: collapse; font-size: 0.78rem; }
        .board caption {
            text-align: left;
            font-size: 0.64rem;
            letter-spacing: 0.24em;
            text-transform: uppercase;
            color: var(--faint);
            padding-bottom: 10px;
        }
        .board th {
            text-align: left;
            font-size: 0.62rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: var(--faint);
            font-weight: 500;
            padding: 10px 14px;
            border-bottom: 1px solid var(--line-hard);
        }
        .board td { padding: 12px 14px; border-bottom: 1px solid var(--line); vertical-align: top; }
        .board tbody tr:nth-child(odd) { background: rgba(0, 240, 255, 0.025); }
        .board .rank { color: var(--faint); width: 56px; }
        .board .team { color: var(--ink); letter-spacing: 0.06em; }
        .board .roster { display: block; color: var(--faint); font-size: 0.7rem; margin-top: 4px; }
        .board .pts { text-align: right; color: var(--cyan); white-space: nowrap; }
        .board tr.top .team { color: var(--amber); }
        .board tr.top .pts { color: var(--amber); }

        /* ── stat readouts ─────────────────────────────────────────── */
        .stats { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); border: 1px solid var(--line); }
        .stats div { padding: 24px 22px; border-right: 1px solid var(--line); }
        .stats div:last-child { border-right: 0; }
        .stats .n { font-family: var(--display); font-size: 3rem; line-height: 1; color: var(--cyan); }
        .stats .k { display: block; font-size: 0.62rem; letter-spacing: 0.22em; text-transform: uppercase; color: var(--faint); margin-bottom: 10px; }
        .stats p { color: var(--dim); font-size: 0.74rem; margin-top: 10px; line-height: 1.6; }

        /* ── timeline strip ────────────────────────────────────────── */
        .seq { display: grid; gap: 0; border: 1px solid var(--line); }
        .seq div {
            display: grid;
            grid-template-columns: minmax(180px, max-content) 1fr auto;
            gap: 18px;
            padding: 13px 20px;
            border-bottom: 1px solid var(--line);
            font-size: 0.72rem;
            letter-spacing: 0.16em;
            text-transform: uppercase;
        }
        .seq div:last-child { border-bottom: 0; }
        .seq .k { color: var(--dim); }
        .seq .t { color: var(--cyan); text-align: right; }
        .seq .bar { height: 1px; background: repeating-linear-gradient(90deg, var(--line) 0 4px, transparent 4px 8px); align-self: center; }
        .seq div.hot .k { color: var(--alert); }
        .seq div.hot .t { color: var(--alert); }

        /* ── checklist + notice ────────────────────────────────────── */
        .req { display: grid; gap: 8px; list-style: none; }
        .req li { display: grid; grid-template-columns: 26px 1fr; gap: 10px; color: var(--dim); font-size: 0.8rem; }
        .req li::before { content: "[+]"; color: var(--cyan); white-space: pre; }

        .notice {
            border: 1px solid var(--alert);
            background: rgba(255, 42, 75, 0.06);
            padding: 18px 22px;
            font-size: 0.8rem;
            color: var(--ink);
        }
        .notice::before {
            content: "";
            display: block;
            height: 6px;
            margin: -18px -22px 16px;
            background: repeating-linear-gradient(45deg, var(--alert) 0 8px, transparent 8px 16px);
            opacity: 0.6;
        }
        .notice b { color: var(--alert); letter-spacing: 0.1em; text-transform: uppercase; }
        .notice.cy { border-color: var(--line-hard); background: rgba(0, 240, 255, 0.05); }
        .notice.cy::before { background: repeating-linear-gradient(45deg, var(--cyan) 0 8px, transparent 8px 16px); }
        .notice.cy b { color: var(--cyan); }

        /* ── faq as prompt log ─────────────────────────────────────── */
        details.q { border-bottom: 1px solid var(--line); }
        details.q summary {
            cursor: pointer;
            list-style: none;
            padding: 14px 0;
            color: var(--ink);
            font-size: 0.8rem;
            display: flex;
            justify-content: space-between;
            gap: 18px;
        }
        details.q summary::-webkit-details-marker { display: none; }
        details.q summary::before { content: "> "; color: var(--cyan); }
        details.q summary::after { content: "[+]"; color: var(--cyan); }
        details.q[open] summary::after { content: "[-]"; }
        details.q summary:hover { color: var(--cyan); }
        details.q .a {
            padding: 0 0 16px 18px;
            border-left: 1px solid var(--line);
            margin-left: 4px;
            color: var(--dim);
            font-family: 'Inter', system-ui, sans-serif;
            font-size: 0.92rem;
        }
        details.q .a b { color: var(--lime); }

        /* ── contribution list ─────────────────────────────────────── */
        .ops { list-style: none; display: grid; gap: 12px; }
        .ops li {
            display: grid;
            grid-template-columns: 30px 1fr;
            gap: 12px;
            color: var(--dim);
            font-family: 'Inter', system-ui, sans-serif;
            font-size: 0.94rem;
            border-left: 1px solid var(--line);
            padding: 4px 0 4px 16px;
        }
        .ops li::before { content: "//"; color: var(--cyan); font-family: var(--mono); font-size: 0.78rem; }
        .ops strong { color: var(--ink); font-weight: 600; }
        .ops a { color: var(--cyan); }

        /* ── entry cards for sections / people ─────────────────────── */
        .files { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
        .file {
            display: block;
            text-decoration: none;
            border: 1px solid var(--line);
            background: var(--panel);
            padding: 22px 24px;
            transition: border-color 0.18s linear, transform 0.18s linear;
        }
        .file:hover { border-color: var(--cyan); transform: translateY(-2px); }
        .file .fhead {
            display: flex;
            justify-content: space-between;
            font-size: 0.62rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: var(--cyan);
            margin-bottom: 12px;
        }
        .file .fhead em { font-style: normal; color: var(--faint); }
        .file h3 { font-family: var(--display); font-size: 1.4rem; text-transform: uppercase; margin-bottom: 8px; }
        .file p { color: var(--dim); font-family: 'Inter', system-ui, sans-serif; font-size: 0.9rem; }
        .file .fmeta {
            display: flex;
            justify-content: space-between;
            margin-top: 16px;
            padding-top: 12px;
            border-top: 1px solid var(--line);
            font-size: 0.64rem;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: var(--faint);
        }
        .file .fmeta span:last-child { color: var(--cyan); }

        .people { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }
        .person { border: 1px solid var(--line); background: var(--panel); padding: 22px 24px; }
        .person .oid { font-size: 0.62rem; letter-spacing: 0.2em; text-transform: uppercase; color: var(--cyan); }
        .person h3 { font-family: var(--display); font-size: 1.25rem; text-transform: uppercase; margin: 8px 0 4px; }
        .person .post { font-size: 0.66rem; letter-spacing: 0.14em; text-transform: uppercase; color: var(--faint); margin-bottom: 10px; }
        .person p { color: var(--dim); font-family: 'Inter', system-ui, sans-serif; font-size: 0.88rem; }

        /* ── sub-page head + pager ─────────────────────────────────── */
        .page-head { padding: 34px 0 10px; }
        .page-head .eyebrow { font-size: 0.64rem; letter-spacing: 0.24em; text-transform: uppercase; color: var(--faint); margin-bottom: 10px; }
        .page-head h1 { font-size: clamp(2rem, 5vw, 3.4rem); }
        .page-head h1 .brace { color: var(--cyan); animation: bl 1.1s steps(2) infinite; }

        .pager {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            border-top: 1px solid var(--line);
            padding: 22px 0 60px;
            font-size: 0.7rem;
            letter-spacing: 0.14em;
            text-transform: uppercase;
        }
        .pager a { color: var(--dim); text-decoration: none; }
        .pager a:hover { color: var(--cyan); }
        .pager .spacer { flex: 1; }

        .outro { text-align: center; padding: 66px 0 78px; border-top: 1px solid var(--line); }
        .outro h2 { font-family: var(--display); font-size: clamp(2rem, 5vw, 3.4rem); text-transform: uppercase; line-height: 1; }
        .outro p { color: var(--dim); font-family: 'Inter', system-ui, sans-serif; max-width: 54ch; margin: 14px auto 24px; }
        .outro .cmds { justify-content: center; }

        /* ── light mode ────────────────────────────────────────────── */
        body.shoug-light-mode {
            --void: #eef2f6;
            --panel: #ffffff;
            --panel-2: #f5f9fc;
            --ink: #08131c;
            --dim: #3f5666;
            --faint: #6a8092;
            --line: rgba(6, 70, 88, 0.16);
            --line-hard: rgba(6, 70, 88, 0.4);
            --cyan: #056274;
            --alert: #c11734;
            --lime: #0a7a45;
            --amber: #8a5b00;
        }
        body.shoug-light-mode .scan {
            background: repeating-linear-gradient(0deg, rgba(6, 70, 88, 0.035) 0 1px, transparent 1px 3px);
        }
        body.shoug-light-mode .console h1 { text-shadow: none; }
        body.shoug-light-mode .cmd.solid,
        body.shoug-light-mode .subnav a.active { color: #ffffff; }
        body.shoug-light-mode ::selection { background: #056274; color: #ffffff; }


        /* Reclaim the page ground from the global light-mode sheet. */
        body.shoug-light-mode.shoug-light-mode {
            background-color: var(--void) !important;
            background-image:
                linear-gradient(rgba(6, 70, 88, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(6, 70, 88, 0.05) 1px, transparent 1px) !important;
            background-size: 48px 48px !important;
            color: var(--ink) !important;
        }
        body.shoug-light-mode h1,
        body.shoug-light-mode h2,
        body.shoug-light-mode h3 { color: var(--ink); }

        /* ── rtl: the content is English technical copy ────────────── */
        html[dir="rtl"] main { direction: ltr; text-align: left; }

        /* ── responsive ────────────────────────────────────────────── */
        @media (max-width: 1080px) {
            .steps { grid-template-columns: repeat(2, minmax(0, 1fr)); }
            .steps div { border-bottom: 1px solid var(--line); }
            .people { grid-template-columns: 1fr; }
        }
        @media (max-width: 900px) {
            .hud { grid-template-columns: repeat(2, minmax(0, 1fr)); }
            .hud div { border-bottom: 1px solid var(--line); }
            .vectors, .files { grid-template-columns: 1fr; }
            .stats { grid-template-columns: 1fr; }
            .stats div { border-right: 0; border-bottom: 1px solid var(--line); }
            .console-body { padding: 24px 18px; }
        }
        @media (max-width: 620px) {
            .steps { grid-template-columns: 1fr; }
            .meter-row { grid-template-columns: 1fr; gap: 6px; }
            .ledger article { grid-template-columns: 1fr; gap: 6px; }
            .seq div { grid-template-columns: 1fr; gap: 4px; }
            .seq .t { text-align: left; }
            .seq .bar { display: none; }
            .board .roster { font-size: 0.66rem; }
        }
"""


BODY = """
    <div class="scan" aria-hidden="true"></div>

__HEADER__

    <main id="main-content" tabindex="-1">
        <div class="wrap">
            <div class="breadcrumb">
                <a href="/workshops/">Workshops</a><span class="sep">/</span><span>ACM/CyberTech CTF 3.0</span>
            </div>
__SUBNAV__

            <section class="console">
                <div class="console-top">
                    <span>System status: <span class="on">registration open</span></span>
                    <span>Coord: 24.7136&deg; N, 46.6753&deg; E</span>
                    <span>Edition 03 // ACM &times; CyberTech</span>
                </div>
                <div class="console-body">
                    <div class="tag-line"><span class="blink"></span>Event website &amp; organizing</div>
                    <h1>ACM/CyberTech<br><em>CTF 3.0</em></h1>
                    <div class="sub">&gt; hack the challenge. capture the flag._</div>
                    <p class="brief">
                        A three-hour capture-the-flag competition run jointly by the ACM Club and the CyberTech Club at
                        Prince Sultan University. Teams of two to three work four attack vectors &mdash; cryptography,
                        web, forensics and OSINT &mdash; and submit flags for points on a live scoreboard. I designed and
                        built the official competition website, and I co-organize the event as ACM Vice President.
                    </p>
                    <div class="cmds">
                        <a class="cmd solid" href="https://ctf-psu.shoug-tech.com/" target="_blank" rel="noopener">Visit the competition site</a>
                        <a class="cmd" href="/workshops/psu-ctf-3/challenges/">Attack vectors</a>
                        <a class="cmd red" href="/workshops/psu-ctf/">CTF 2.0 archive</a>
                    </div>
                </div>
                <div class="hud">
                    <div><span class="k">// Date</span><span class="v">24 Oct<small>Saturday 2026</small></span></div>
                    <div><span class="k">// Window</span><span class="v">10:00<small>to 13:00 AST</small></span></div>
                    <div><span class="k">// Duration</span><span class="v">03:00:00<small>continuous</small></span></div>
                    <div><span class="k">// Location</span><span class="v">B105<small>auditorium, 2nd floor</small></span></div>
                </div>
            </section>
        </div>

        <div class="wrap">
            <div class="rail">
                <span>Host: <b>ACM Club &times; CyberTech Club</b></span>
                <span>CCIS &middot; Prince Sultan University</span>
                <span>My role: <b>VP, ACM &mdash; organizer &amp; website developer</b></span>
                <span>Teams: <b>2&ndash;3</b></span>
                <span>Flag: <b>ACM{&hellip;}</b></span>
                <span class="live">Scoreboard: locked</span>
            </div>

            <section class="block" id="contribution">
                <div class="sec-head">01 // My contribution</div>
                <h2 class="sec-title">The competition website</h2>
                <div class="vectors" style="margin-top: 26px;">
                    <ul class="ops">
                        <li><span><strong>I designed and built the official CTF 3.0 website</strong> at ctf-psu.shoug-tech.com &mdash; the mission brief, attack-vector pages, competition parameters, training schedule, rules, FAQ, team registry and results archive.</span></li>
                        <li><span><strong>I built the scoreboard and archive views</strong> that publish the previous edition's verified record: 11 teams, 852 submissions, 89 captures and the final standings, with rosters for the top three teams.</span></li>
                        <li><span><strong>As Vice President of the ACM Club</strong>, I co-organize CTF 3.0 &mdash; leading event planning and coordination alongside the website work and supporting technical preparation.</span></li>
                        <li><span>Challenge development, infrastructure and the participant workshop are led by the other organizers. My own workshop teaching for this series was the previous edition, <a href="/workshops/psu-ctf/">ACM/Cyber-Tech CTF 2.0</a>.</span></li>
                    </ul>
                    <div class="term" aria-hidden="true">
<span class="p">operator@cyber-range:~$</span> ./connect --event ctf-3.0
<span class="o">&gt; establishing secure connection&hellip;</span>
<span class="ok">[ok]</span> <span class="o">team: 2&ndash;3 operators</span>
<span class="ok">[ok]</span> <span class="o">vectors: crypto / web / forensics / osint</span>
<span class="ok">[ok]</span> <span class="o">duration: 03:00:00</span>
<span class="wa">[locked]</span> <span class="o">challenge database</span>
<span class="p">operator@cyber-range:~$</span> submit "ACM{example_flag}"
<span class="ok">&#10003; flag accepted &mdash; points awarded</span>
<span class="p">operator@cyber-range:~$</span> <span class="caret"></span>
                    </div>
                </div>
            </section>

            <section class="block" id="brief">
                <div class="sec-head">02 // Mission brief</div>
                <h2 class="sec-title">Enter the cyber range</h2>
                <p class="lede">Participants act as operators, investigating challenges across multiple vectors: identify
                    vulnerabilities, decode encrypted information, follow digital artifacts, and uncover hidden flags to
                    earn points and secure a position on the leaderboard.</p>
                <div class="stats" style="margin-top: 26px;">
                    <div><span class="k">// Objective</span><span class="n">FLAGS</span><p>Each challenge hides a flag in ACM{&hellip;} format. Find it, submit it, score.</p></div>
                    <div><span class="k">// Environment</span><span class="n">CONTROLLED</span><p>Only systems and challenges explicitly provided for the CTF are in scope.</p></div>
                    <div><span class="k">// Mission time</span><span class="n">03:00</span><p>Three continuous hours, 10:00 to 13:00 on competition day.</p></div>
                </div>
            </section>

            <section class="block" id="challenges">
                <div class="sec-head">03 // Attack vectors</div>
                <h2 class="sec-title">Choose your target</h2>
                <p class="lede">Four categories, multiple challenges, one objective. The challenge database itself stays
                    classified until the competition begins.</p>
                <div class="vectors" style="margin-top: 28px;">
                    <div class="vector">
                        <span class="idx">01</span>
                        <div class="cat">01 // Cryptography</div>
                        <h3>Break the cipher</h3>
                        <p>Recognize patterns, decode information, analyze encryption methods, and recover hidden messages
                            across modern and historical schemes.</p>
                        <div class="tags"><span>Ciphers</span><span>Encoding</span><span>Hashing</span><span>Cryptanalysis</span></div>
                    </div>
                    <div class="vector">
                        <span class="idx">02</span>
                        <div class="cat">02 // Web</div>
                        <h3>Find the vulnerability</h3>
                        <p>Investigate web applications, understand how they behave, identify vulnerabilities, and find
                            ways to reach protected information.</p>
                        <div class="tags"><span>HTTP</span><span>Source analysis</span><span>Web security</span><span>Vulnerability discovery</span></div>
                    </div>
                    <div class="vector">
                        <span class="idx">03</span>
                        <div class="cat">03 // Forensics</div>
                        <h3>Follow the evidence</h3>
                        <p>Examine digital evidence and uncover information hidden inside files, metadata, logs, network
                            data and other artifacts.</p>
                        <div class="tags"><span>File analysis</span><span>Metadata</span><span>Logs</span><span>Digital evidence</span></div>
                    </div>
                    <div class="vector">
                        <span class="idx">04</span>
                        <div class="cat">04 // OSINT</div>
                        <h3>Connect the clues</h3>
                        <p>Investigate publicly available information, search effectively, connect clues, and identify
                            relevant intelligence.</p>
                        <div class="tags"><span>Search</span><span>Reconnaissance</span><span>Data correlation</span><span>Public intelligence</span></div>
                    </div>
                </div>

                <h3 class="sub-title">Threat levels</h3>
                <p class="lede" style="margin-bottom: 20px;">Complexity is scaled across five levels. Harder challenges
                    demand deeper investigation and typically award more points; values are assigned dynamically at launch
                    based on solve rates.</p>
                <div class="meter">
                    <div class="meter-row"><span>Very easy</span><span class="blocks"><i class="on"></i><i></i><i></i><i></i><i></i></span></div>
                    <div class="meter-row"><span>Easy</span><span class="blocks"><i class="on"></i><i class="on"></i><i></i><i></i><i></i></span></div>
                    <div class="meter-row"><span>Medium</span><span class="blocks"><i class="on"></i><i class="on"></i><i class="on"></i><i></i><i></i></span></div>
                    <div class="meter-row hot"><span>Hard</span><span class="blocks"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i></i></span></div>
                    <div class="meter-row hot"><span>Insane</span><span class="blocks"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i></span></div>
                </div>

                <h3 class="sub-title">Flag protocol</h3>
                <div class="steps">
                    <div><span class="n">01</span><h4>Select</h4><p>Choose a challenge from the available categories.</p></div>
                    <div><span class="n">02</span><h4>Investigate</h4><p>Analyze the provided target, files, clues or information.</p></div>
                    <div><span class="n">03</span><h4>Find the flag</h4><p>Discover the flag hidden inside the challenge.</p></div>
                    <div><span class="n">04</span><h4>Submit</h4><p>Enter the flag into the competition platform.</p></div>
                    <div><span class="n">05</span><h4>Score</h4><p>A valid flag adds points to the team's total.</p></div>
                </div>
                <div class="notice cy" style="margin-top: 24px;">
                    <b>Format</b> &mdash; ACM{example_flag}. Example only; do not submit test flags during the live
                    competition. Actual challenges, infrastructure and flags stay classified until launch.
                </div>
            </section>

            <section class="block" id="training">
                <div class="sec-head">04 // Training protocol</div>
                <h2 class="sec-title">Prepare for the breach</h2>
                <p class="lede">Preparation workshops run before the competition, built around the four challenge
                    categories so first-time competitors arrive with a working toolkit. Titles, times and instructors are
                    announced by the organizers; the schedule below is the published plan.</p>
                <div class="vectors" style="margin-top: 28px;">
                    <div class="vector">
                        <div class="cat">21 Oct 2026 // Web // Beginner</div>
                        <h3>Web exploitation fundamentals</h3>
                        <p>How web applications work, how vulnerabilities are discovered, and how to investigate insecure
                            behavior in modern web architectures.</p>
                        <div class="tags"><span>Upcoming</span><span>Time TBD</span><span>Instructor TBD</span></div>
                    </div>
                    <div class="vector">
                        <div class="cat">21 Oct 2026 // Cryptography // Intermediate</div>
                        <h3>Applied cryptography</h3>
                        <p>Recognizing, analyzing and breaking the forms of encoded and encrypted information used to
                            secure data.</p>
                        <div class="tags"><span>Upcoming</span><span>Time TBD</span><span>Instructor TBD</span></div>
                    </div>
                    <div class="vector">
                        <div class="cat">22 Oct 2026 // Forensics // Beginner</div>
                        <h3>Digital artifacts</h3>
                        <p>Inspecting files, hidden metadata, network packets and the other evidence left behind on
                            systems.</p>
                        <div class="tags"><span>Upcoming</span><span>Time TBD</span><span>Instructor TBD</span></div>
                    </div>
                    <div class="vector">
                        <div class="cat">22 Oct 2026 // OSINT // Intermediate</div>
                        <h3>Intelligence gathering</h3>
                        <p>Gathering, analyzing and connecting publicly available information to profile targets and
                            uncover secrets.</p>
                        <div class="tags"><span>Upcoming</span><span>Time TBD</span><span>Instructor TBD</span></div>
                    </div>
                </div>

                <h3 class="sub-title">Operator requirements</h3>
                <div class="vectors">
                    <ul class="req">
                        <li>A personal laptop able to run modern browsers and, if required, virtualization software</li>
                        <li>Power adapter or charger &mdash; outlets are provided on site</li>
                        <li>An updated modern browser; Firefox or Chrome recommended</li>
                        <li>Any workshop-specific software or virtual machines, announced beforehand</li>
                        <li>Network access credentials are provided on site</li>
                    </ul>
                    <div class="notice">
                        <b>Training environment is not the competition environment</b> &mdash; workshop materials, examples
                        and practice exercises are educational preparation only. They do not reveal actual competition
                        challenges, infrastructure or flags.
                    </div>
                </div>
            </section>

            <section class="block" id="competition">
                <div class="sec-head">05 // Mission parameters</div>
                <h2 class="sec-title">How the operation works</h2>
                <p class="lede">Teams investigate challenges, find hidden flags, and submit valid flags to earn points over
                    three hours. The previous edition brought together 11 teams across 16+ challenges and recorded 852
                    flag submissions.</p>

                <h3 class="sub-title">Operation timeline</h3>
                <div class="seq">
                    <div><span class="k">Check-in</span><span class="bar"></span><span class="t">TBD</span></div>
                    <div><span class="k">Opening briefing</span><span class="bar"></span><span class="t">TBD</span></div>
                    <div class="hot"><span class="k">Competition begins</span><span class="bar"></span><span class="t">10:00 AM</span></div>
                    <div class="hot"><span class="k">Competition ends</span><span class="bar"></span><span class="t">1:00 PM</span></div>
                    <div><span class="k">Results / awards</span><span class="bar"></span><span class="t">TBD</span></div>
                </div>

                <div class="vectors" style="margin-top: 34px;">
                    <div>
                        <h3 class="sub-title" style="margin-top: 0;">Scoring protocol</h3>
                        <ul class="req">
                            <li>Each challenge contains a hidden flag</li>
                            <li>Valid flag submissions award points</li>
                            <li>Challenge difficulty may affect point value</li>
                            <li>Team scores accumulate throughout the competition</li>
                            <li>The highest final scores rank highest on the scoreboard</li>
                            <li>Ties break by the time the tied score was reached, subject to organizer verification</li>
                        </ul>
                    </div>
                    <div>
                        <h3 class="sub-title" style="margin-top: 0;">Equipment protocol</h3>
                        <ul class="req">
                            <li>Laptop &mdash; required</li>
                            <li>Charger &mdash; required</li>
                            <li>Student ID</li>
                            <li>Network access &mdash; provided on site</li>
                        </ul>
                        <div class="notice cy" style="margin-top: 20px;">
                            <b>Team configuration</b> &mdash; teams of two to three members. Solo registration is not
                            allowed, and each person may join one team only.
                        </div>
                    </div>
                </div>

                <div class="notice" style="margin-top: 30px;">
                    <b>Operation notice</b> &mdash; participants must follow the official rules and interact only with
                    systems, files and targets explicitly provided as part of the competition. Unauthorized scanning or
                    attacks on out-of-scope infrastructure result in immediate disqualification.
                </div>
            </section>

            <section class="block" id="rules">
                <div class="sec-head">06 // Rules of engagement</div>
                <h2 class="sec-title">Play hard, play fair</h2>
                <p class="lede">Every action stays inside the authorized competition environment. Organizers confirm
                    eligibility, dates, prizes and disciplinary policy before registration closes.</p>
                <div class="ledger" style="margin-top: 26px;">
                    <article><div class="rid">Rule_01</div><div><h3>Eligibility</h3><p>Participation is open to eligible PSU students. Each person may join one team only.</p></div></article>
                    <article><div class="rid">Rule_02</div><div><h3>Team size</h3><p>Register in teams of 2&ndash;3 members. Solo participation is not allowed, and roster changes close before the competition begins.</p></div></article>
                    <article><div class="rid">Rule_03</div><div><h3>Authorized scope</h3><p>Only systems and challenges explicitly provided for the CTF are in scope. Do not scan or attack PSU, sponsor or third-party infrastructure.</p></div></article>
                    <article><div class="rid">Rule_04</div><div><h3>Fair play</h3><p>Do not share flags, solutions, credentials or challenge files with another team during the event.</p></div></article>
                    <article><div class="rid">Rule_05</div><div><h3>Platform safety</h3><p>Do not disrupt the scoreboard, infrastructure, other competitors or the event network. Denial-of-service activity is prohibited.</p></div></article>
                    <article><div class="rid">Rule_06</div><div><h3>Flag submission</h3><p>Submit flags only through your team account. Automated guessing or brute-forcing the submission endpoint is prohibited.</p></div></article>
                    <article><div class="rid">Rule_07</div><div><h3>Tools &amp; internet</h3><p>Standard security tools and public reference material are allowed unless a challenge states otherwise. External human assistance is not allowed.</p></div></article>
                    <article><div class="rid">Rule_08</div><div><h3>Conduct</h3><p>Be respectful. Harassment, tampering and attempts to gain unfair access may lead to immediate removal.</p></div></article>
                    <article><div class="rid">Rule_09</div><div><h3>Disputes</h3><p>Contact an organizer privately with evidence. Organizer decisions and final score validation are final.<span class="note">// These rules are the launch-ready draft published on the competition site.</span></p></div></article>
                </div>

                <h3 class="sub-title">Query log</h3>
                <details class="q"><summary>What is a CTF?</summary><div class="a">A capture-the-flag is a cybersecurity competition where participants solve technical challenges to find secret strings called flags.</div></details>
                <details class="q"><summary>Do I need cybersecurity experience?</summary><div class="a"><b>No.</b> The workshops and beginner challenges are designed for first-time participants, while advanced categories keep experienced players challenged.</div></details>
                <details class="q"><summary>Can I compete alone?</summary><div class="a"><b>No.</b> Every participant must join a registered team of two to three members.</div></details>
                <details class="q"><summary>What should I bring?</summary><div class="a">A laptop, charger, student ID and any adapters you need. Install instructions are shared before the event.</div></details>
                <details class="q"><summary>Which operating system should I use?</summary><div class="a">Any modern OS is acceptable. A Linux virtual machine is recommended for many common CTF tools.</div></details>
                <details class="q"><summary>Are online resources allowed?</summary><div class="a">Public documentation and search are generally allowed. Asking outside people for solutions, or exchanging flags with other teams, is not.</div></details>
                <details class="q"><summary>How are ties resolved?</summary><div class="a">The default tie-breaker is the time the tied score was reached, subject to organizer verification.</div></details>
                <details class="q"><summary>How did the previous edition perform?</summary><div class="a">CTF 2.0 hosted 11 teams across 16+ challenges. Competitors made 852 submissions, captured 89 flags, and achieved a 10.4% overall solve rate. HZ placed first with 3,800 points.</div></details>
                <details class="q"><summary>Where will updates be announced?</summary><div class="a">Official dates, registration, room details and changes are posted through ACM PSU channels and the competition website.</div></details>
            </section>

            <section class="block" id="archive">
                <div class="sec-head">07 // Verified archive</div>
                <h2 class="sec-title">CTF 2.0 &mdash; the previous edition</h2>
                <p class="lede">The website publishes the previous edition's verified record, so each CTF leaves a
                    permanent, checkable result rather than a screenshot in a group chat.</p>

                <div class="stats" style="margin-top: 26px;">
                    <div><span class="k">// Submissions</span><span class="n">852</span><p>Total flag submissions recorded across the competition.</p></div>
                    <div><span class="k">// Captures</span><span class="n">89</span><p>Valid flags &mdash; a 10.4% solve rate against 763 failed submissions.</p></div>
                    <div><span class="k">// Teams ranked</span><span class="n">11</span><p>Final standings verified and published, with rosters for the top three.</p></div>
                </div>

                <h3 class="sub-title">Final standings</h3>
                <table class="board">
                    <caption>CTF 2.0 // verified // rosters published for ranks 01&ndash;03</caption>
                    <thead><tr><th class="rank">Rank</th><th>Operative / team</th><th style="text-align:right">Points</th></tr></thead>
                    <tbody>
                        <tr class="top"><td class="rank">01</td><td class="team">HZ<span class="roster">Hasan Belal Farhat &middot; Hazim Khalid Alhatim</span></td><td class="pts">3,800</td></tr>
                        <tr><td class="rank">02</td><td class="team">TheVault<span class="roster">Aljawhara Aljubair &middot; Alshaimaa Babaeer &middot; Judy Waseem Al Hassan</span></td><td class="pts">2,800</td></tr>
                        <tr><td class="rank">03</td><td class="team">ZERO DAY<span class="roster">Omar Fahad Alkhalifah &middot; Abdullah Alanazi</span></td><td class="pts">2,100</td></tr>
                        <tr><td class="rank">04</td><td class="team">Gotcha_flag</td><td class="pts">2,000</td></tr>
                        <tr><td class="rank">05</td><td class="team">ASM</td><td class="pts">1,900</td></tr>
                        <tr><td class="rank">06</td><td class="team">checkmate</td><td class="pts">1,900</td></tr>
                        <tr><td class="rank">07</td><td class="team">Aha</td><td class="pts">1,300</td></tr>
                        <tr><td class="rank">08</td><td class="team">Cybercrackers</td><td class="pts">1,300</td></tr>
                        <tr><td class="rank">09</td><td class="team">404</td><td class="pts">1,000</td></tr>
                        <tr><td class="rank">10</td><td class="team">MAM</td><td class="pts">900</td></tr>
                        <tr><td class="rank">11</td><td class="team">Red Team</td><td class="pts">800</td></tr>
                    </tbody>
                </table>

                <h3 class="sub-title">Organizing unit</h3>
                <div class="people">
                    <div class="person">
                        <div class="oid">Org 01</div>
                        <h3>Shoug Alomran</h3>
                        <div class="post">ACM Club &middot; Vice President</div>
                        <p>CTF organizer and website developer. Leads event planning and coordination while developing the
                            competition website and supporting the technical preparation of the event.</p>
                    </div>
                    <div class="person">
                        <div class="oid">Org 02</div>
                        <h3>Muhammad Yawar Hayat</h3>
                        <div class="post">ACM Student Chapter PSU &middot; President</div>
                        <p>Event planning and sponsor outreach, challenge design and development across categories,
                            infrastructure deployment and maintenance, the participant workshop, and live technical support
                            during the competition.</p>
                    </div>
                    <div class="person">
                        <div class="oid">Org 03</div>
                        <h3>Sultan Alharbi</h3>
                        <div class="post">Cyber-Tech Club &middot; President</div>
                        <p>Role and contribution being confirmed by the organizers.</p>
                    </div>
                </div>

                <div class="notice cy" style="margin-top: 28px;">
                    <b>Earlier editions</b> &mdash; I taught three of the five preparation workshops for the previous
                    edition and built its event website. See <a href="/workshops/psu-ctf/">ACM/Cyber-Tech CTF 2.0</a>.
                </div>
            </section>
        </div>

        <div class="wrap">
            <div class="outro">
                <div class="sec-head" style="justify-content: center;">// end of transmission</div>
                <h2>Capture the flag.</h2>
                <p>Assemble a team of two or three, prepare the system, and enter the cyber range on 24 October.</p>
                <div class="cmds">
                    <a class="cmd solid" href="https://ctf-psu.shoug-tech.com/" target="_blank" rel="noopener">ctf-psu.shoug-tech.com</a>
                    <a class="cmd" href="/workshops/">All workshops</a>
                </div>
            </div>
        </div>
    </main>

__FOOTER__
"""


HUB_CARDS = """
            <section class="block" id="explore">
                <div class="sec-head">03 // Sections</div>
                <h2 class="sec-title">Open a file</h2>
                <p class="lede">The competition is documented across four pages, with the verified record of the previous
                    edition alongside them.</p>
                <div class="files" style="margin-top: 28px;">
                    <a class="file" href="/workshops/psu-ctf-3/challenges/">
                        <div class="fhead"><span>01 // Vectors</span><em>challenges.md</em></div>
                        <h3>Attack Vectors</h3>
                        <p>Cryptography, web, forensics and OSINT &mdash; what each category asks for, the five threat
                            levels, and the flag protocol from selecting a challenge to scoring points.</p>
                        <div class="fmeta"><span>4 categories</span><span>open -&gt;</span></div>
                    </a>
                    <a class="file" href="/workshops/psu-ctf-3/training/">
                        <div class="fhead"><span>02 // Training</span><em>workshops.md</em></div>
                        <h3>Preparation Workshops</h3>
                        <p>Four sessions across the competition categories on 21 and 22 October, plus the operator
                            requirements every participant needs before event day.</p>
                        <div class="fmeta"><span>21 &middot; 22 Oct 2026</span><span>open -&gt;</span></div>
                    </a>
                    <a class="file" href="/workshops/psu-ctf-3/competition/">
                        <div class="fhead"><span>03 // Operation</span><em>competition.md</em></div>
                        <h3>Competition Day</h3>
                        <p>Mission format, team configuration, the timeline of the three hours, the scoring protocol, and
                            the equipment each operator brings.</p>
                        <div class="fmeta"><span>24 Oct 2026</span><span>open -&gt;</span></div>
                    </a>
                    <a class="file" href="/workshops/psu-ctf-3/rules-faq/">
                        <div class="fhead"><span>04 // Rules</span><em>rules.md</em></div>
                        <h3>Rules &amp; FAQ</h3>
                        <p>The nine rules of engagement that keep the competition inside authorized scope, and the
                            questions first-time players ask most.</p>
                        <div class="fmeta"><span>9 rules</span><span>open -&gt;</span></div>
                    </a>
                    <a class="file" href="/workshops/psu-ctf-3/archive/" style="grid-column: 1 / -1;">
                        <div class="fhead"><span>05 // Archive</span><em>ctf-2.0.results</em></div>
                        <h3>Results Archive &amp; Organizers</h3>
                        <p>The verified record of CTF 2.0 &mdash; 11 teams, 852 submissions, 89 captures and the final
                            standings with top-three rosters &mdash; and the people running this edition.</p>
                        <div class="fmeta"><span>Verified results</span><span>open -&gt;</span></div>
                    </a>
                </div>
            </section>
"""

CTA = """
        <div class="wrap">
            <div class="outro">
                <div class="sec-head" style="justify-content: center;">// end of transmission</div>
                <h2>Capture the flag.</h2>
                <p>Assemble a team of two or three, prepare the system, and enter the cyber range on 24 October.</p>
                <div class="cmds">
                    <a class="cmd solid" href="https://ctf-psu.shoug-tech.com/" target="_blank" rel="noopener">ctf-psu.shoug-tech.com</a>
                    <a class="cmd" href="/workshops/">All workshops</a>
                </div>
            </div>
        </div>
"""

PAGES = (
    Page(slug="", filename="", label="Overview", title=TITLE, description=DESCRIPTION),
    Page(
        slug="challenges/",
        filename="challenges",
        label="Vectors",
        title="CTF 3.0 Attack Vectors // SHOUG.TECH",
        description=(
            "The four ACM/CyberTech CTF 3.0 challenge categories — cryptography, web, forensics and OSINT — with the "
            "skills each one tests, the five threat levels, and the flag submission protocol."
        ),
        eyebrow="ACM/CyberTech CTF 3.0 // Section 01",
        heading="Attack Vectors",
        sections=("challenges",),
    ),
    Page(
        slug="training/",
        filename="training",
        label="Training",
        title="CTF 3.0 Preparation Workshops // SHOUG.TECH",
        description=(
            "Preparation workshops for ACM/CyberTech CTF 3.0 on 21 and 22 October 2026 across web exploitation, applied "
            "cryptography, digital forensics and intelligence gathering, plus operator equipment requirements."
        ),
        eyebrow="ACM/CyberTech CTF 3.0 // Section 02",
        heading="Preparation Workshops",
        sections=("training",),
    ),
    Page(
        slug="competition/",
        filename="competition",
        label="Competition",
        title="CTF 3.0 Competition Day // SHOUG.TECH",
        description=(
            "How ACM/CyberTech CTF 3.0 runs on 24 October 2026: mission format, team configuration, the timeline of the "
            "three-hour window, the scoring protocol and the equipment each operator brings."
        ),
        eyebrow="ACM/CyberTech CTF 3.0 // Section 03",
        heading="Competition Day",
        sections=("competition",),
    ),
    Page(
        slug="rules-faq/",
        filename="rules-faq",
        label="Rules & FAQ",
        title="CTF 3.0 Rules &amp; FAQ // SHOUG.TECH",
        description=(
            "The nine ACM/CyberTech CTF 3.0 rules of engagement — eligibility, team size, authorized scope, fair play, "
            "platform safety, flag submission, tools, conduct and disputes — with answers to common questions."
        ),
        eyebrow="ACM/CyberTech CTF 3.0 // Section 04",
        heading="Rules & FAQ",
        sections=("rules",),
    ),
    Page(
        slug="archive/",
        filename="archive",
        label="Archive",
        title="CTF 2.0 Results Archive // SHOUG.TECH",
        description=(
            "The verified ACM/Cyber-Tech CTF 2.0 record published on the CTF 3.0 site: 11 teams, 852 submissions, 89 "
            "captures, the final standings with top-three rosters, and the CTF 3.0 organizing team."
        ),
        eyebrow="ACM/CyberTech CTF 3.0 // Section 05",
        heading="Results Archive",
        sections=("archive",),
    ),
)

EVENT = Event(
    root=ROOT,
    base=BASE,
    css=THEME_CSS,
    pages=PAGES,
    about=ABOUT,
    nav_label=EVENT_LABEL,
    heading_html='{h}<span class="brace">_</span>',
)


def build_hub(chrome: dict[str, str], parts: dict[str, str]) -> str:
    body = (
        parts["intro"].replace("__SUBNAV__", subnav(EVENT, ""))
        + parts["contribution"]
        + parts["brief"]
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
