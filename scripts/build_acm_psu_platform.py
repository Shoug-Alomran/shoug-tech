#!/usr/bin/env python3
"""Build the ACM PSU digital platform page under /workshops/acm-psu-platform/.

A single page (no sub-pages): the club platform I am building, what it does for
members, and how it connects the chapter's events and archive.
"""

from __future__ import annotations

from event_page_kit import DOCS, Event, Page, extract_chrome, render, subnav, write

ROOT = DOCS / "workshops" / "acm-psu-platform"
BASE = "/workshops/acm-psu-platform/"
EVENT_LABEL = "ACM PSU Digital Platform"

TITLE = "ACM PSU Digital Platform // SHOUG.TECH"
DESCRIPTION = (
    "The ACM PSU digital platform — a central website for the chapter's members, events, "
    "open positions, projects and archive, built by Shoug Alomran so that ACM opportunities "
    "are visible to every member rather than the few who hear about them first."
)

ABOUT = {
    "@type": "WebSite",
    "name": "ACM PSU Digital Platform",
    "description": "Central platform for the ACM student chapter at Prince Sultan University: membership applications, open event positions, project case studies and a chapter archive.",
    "url": "https://acm-psu.shoug-tech.com/",
    "publisher": {
        "@type": "Organization",
        "name": "ACM Student Chapter, College of Computer & Information Sciences, Prince Sultan University",
    },
    "creator": {"@type": "Person", "name": "Shoug Alomran"},
}

FONTS = (
    "https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;"
    "0,6..72,500;1,6..72,300&amp;family=Inter:wght@400;500;600&amp;family=JetBrains+Mono:wght@400;500&amp;display=swap"
)

THEME_CSS = """
        /* ── ACM PSU platform — reading-room archive ────────────────────
           A catalogue, not a console: serif headings, hairline rules,
           numbered record rows, ledger tables and a warm ink palette. No
           terminals, no scanlines, no code windows. */
        :root {
            --ink: #0f0e13;
            --ink-2: #16151c;
            --paper: #f3efe6;
            --paper-dim: #b9b2a6;
            --paper-faint: #8b8478;
            --rule: rgba(243, 239, 230, 0.16);
            --rule-soft: rgba(243, 239, 230, 0.09);
            --gold: #d8b26a;
            --gold-soft: rgba(216, 178, 106, 0.12);
            --sage: #9fbfa4;
            --serif: 'Newsreader', 'Iowan Old Style', Georgia, serif;
            --sans: 'Inter', system-ui, sans-serif;
            --mono: 'JetBrains Mono', ui-monospace, monospace;
        }

        body {
            background: var(--ink);
            color: var(--paper);
            font-family: var(--sans);
            font-size: 1rem;
            line-height: 1.7;
        }

        ::selection { background: var(--gold); color: var(--ink); }

        /* a faint paper grain, nothing more */
        .grain {
            position: fixed;
            inset: 0;
            z-index: 0;
            pointer-events: none;
            background:
                radial-gradient(ellipse 60% 40% at 20% 0%, rgba(216, 178, 106, 0.07), transparent 65%),
                radial-gradient(ellipse 50% 40% at 100% 30%, rgba(159, 191, 164, 0.05), transparent 60%);
        }
        main, header, footer { position: relative; z-index: 1; }

        .label {
            font-family: var(--mono);
            font-size: 0.66rem;
            letter-spacing: 0.28em;
            text-transform: uppercase;
            color: var(--paper-faint);
        }

        .breadcrumb {
            padding: 26px 0 0;
            font-family: var(--mono);
            font-size: 0.66rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: var(--paper-faint);
        }
        .breadcrumb a { color: var(--paper-dim); text-decoration: none; }
        .breadcrumb a:hover { color: var(--gold); }
        .breadcrumb .sep { margin: 0 10px; color: var(--rule); }

        /* ── masthead ──────────────────────────────────────────────── */
        .masthead {
            padding: 60px 0 44px;
            border-bottom: 1px solid var(--rule);
        }
        .masthead .dir {
            font-family: var(--mono);
            font-size: 0.66rem;
            letter-spacing: 0.24em;
            text-transform: uppercase;
            color: var(--gold);
            margin-bottom: 26px;
        }
        .masthead h1 {
            font-family: var(--serif);
            font-weight: 300;
            font-size: clamp(2.9rem, 7vw, 5.6rem);
            line-height: 0.98;
            letter-spacing: -0.02em;
            margin-bottom: 22px;
        }
        .masthead h1 em { font-style: italic; color: var(--gold); }
        .masthead .standfirst {
            font-family: var(--serif);
            font-weight: 300;
            font-size: clamp(1.1rem, 2.1vw, 1.45rem);
            line-height: 1.55;
            color: var(--paper-dim);
            max-width: 62ch;
        }
        .byline {
            display: flex;
            flex-wrap: wrap;
            gap: 12px 28px;
            margin-top: 30px;
            font-family: var(--mono);
            font-size: 0.68rem;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: var(--paper-faint);
        }
        .byline b { color: var(--paper); font-weight: 400; }

        .actions { display: flex; flex-wrap: wrap; gap: 14px; margin-top: 34px; }
        .action {
            font-family: var(--mono);
            font-size: 0.7rem;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            text-decoration: none;
            padding: 13px 22px;
            border: 1px solid var(--rule);
            color: var(--paper);
            transition: border-color 0.2s ease, color 0.2s ease, background 0.2s ease;
        }
        .action:hover { border-color: var(--gold); color: var(--gold); }
        .action.filled { background: var(--gold); border-color: var(--gold); color: var(--ink); }
        .action.filled:hover { background: transparent; color: var(--gold); }

        /* ── colophon (key/value ledger) ───────────────────────────── */
        .colophon {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0 56px;
            padding: 32px 0 8px;
            border-bottom: 1px solid var(--rule);
        }
        .colophon div {
            display: grid;
            grid-template-columns: 150px 1fr;
            gap: 18px;
            padding: 13px 0;
            border-bottom: 1px solid var(--rule-soft);
            align-items: baseline;
        }
        .colophon dt, .colophon .k {
            font-family: var(--mono);
            font-size: 0.62rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: var(--paper-faint);
        }
        .colophon .v { color: var(--paper-dim); font-size: 0.95rem; }

        /* ── sections ──────────────────────────────────────────────── */
        section.block { padding: 66px 0; border-bottom: 1px solid var(--rule); }

        .sect-mark {
            display: flex;
            align-items: baseline;
            gap: 16px;
            font-family: var(--mono);
            font-size: 0.66rem;
            letter-spacing: 0.26em;
            text-transform: uppercase;
            color: var(--gold);
            margin-bottom: 18px;
        }
        .sect-mark::after { content: ""; flex: 1; height: 1px; background: var(--rule); }

        h2.sect-title {
            font-family: var(--serif);
            font-weight: 300;
            font-size: clamp(1.9rem, 4.2vw, 3.1rem);
            line-height: 1.1;
            letter-spacing: -0.015em;
            margin-bottom: 18px;
        }
        h2.sect-title em { font-style: italic; color: var(--gold); }
        p.intro {
            font-family: var(--serif);
            font-weight: 300;
            font-size: 1.18rem;
            line-height: 1.6;
            color: var(--paper-dim);
            max-width: 68ch;
        }

        /* ── numbered entries (the reading column) ─────────────────── */
        .entries { margin-top: 40px; border-top: 1px solid var(--rule); }
        .entries article {
            display: grid;
            grid-template-columns: 92px minmax(0, 1fr);
            gap: 32px;
            padding: 26px 0;
            border-bottom: 1px solid var(--rule-soft);
        }
        .entries .no {
            font-family: var(--serif);
            font-size: 1.6rem;
            font-weight: 300;
            color: var(--gold);
            line-height: 1;
        }
        .entries h3 {
            font-family: var(--serif);
            font-weight: 400;
            font-size: 1.4rem;
            line-height: 1.25;
            margin-bottom: 8px;
        }
        .entries p { color: var(--paper-dim); font-size: 0.97rem; max-width: 72ch; }
        .entries strong { color: var(--paper); font-weight: 500; }

        /* ── catalogue rows ────────────────────────────────────────── */
        .catalogue { margin-top: 36px; border-top: 1px solid var(--rule); }
        .record {
            display: grid;
            grid-template-columns: 128px minmax(0, 1fr) 150px 40px;
            gap: 26px;
            align-items: baseline;
            padding: 24px 8px 24px 0;
            border-bottom: 1px solid var(--rule-soft);
            text-decoration: none;
            color: inherit;
            transition: background 0.2s ease, padding 0.2s ease;
        }
        .record:hover { background: rgba(243, 239, 230, 0.03); padding-left: 10px; }
        .record .rid {
            font-family: var(--mono);
            font-size: 0.66rem;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: var(--gold);
        }
        .record h3 {
            font-family: var(--serif);
            font-weight: 400;
            font-size: 1.45rem;
            line-height: 1.2;
            margin-bottom: 6px;
        }
        .record p { color: var(--paper-dim); font-size: 0.95rem; max-width: 62ch; }
        .record .when {
            font-family: var(--mono);
            font-size: 0.64rem;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: var(--paper-faint);
        }
        .record .go { font-family: var(--mono); color: var(--gold); text-align: right; }

        /* ── stamps ────────────────────────────────────────────────── */
        .stamps { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 26px; }
        .stamp {
            font-family: var(--mono);
            font-size: 0.64rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: var(--paper-dim);
            border: 1px solid var(--rule);
            padding: 8px 14px;
        }
        .stamp.on { color: var(--sage); border-color: rgba(159, 191, 164, 0.4); }

        /* ── registry list (open roles) ────────────────────────────── */
        .registry {
            border: 1px solid var(--rule);
            padding: 4px 26px 10px;
            background: var(--ink-2);
        }
        .registry .rhead {
            display: flex;
            justify-content: space-between;
            gap: 16px;
            padding: 16px 0 12px;
            border-bottom: 1px solid var(--rule);
            font-family: var(--mono);
            font-size: 0.62rem;
            letter-spacing: 0.22em;
            text-transform: uppercase;
            color: var(--paper-faint);
        }
        .registry ul { list-style: none; }
        .registry li {
            display: grid;
            grid-template-columns: minmax(0, 1fr) auto;
            gap: 18px;
            padding: 12px 0;
            border-bottom: 1px solid var(--rule-soft);
            font-size: 0.94rem;
            color: var(--paper-dim);
        }
        .registry li:last-child { border-bottom: 0; }
        .registry .places { font-family: var(--mono); font-size: 0.7rem; color: var(--gold); white-space: nowrap; }
        .registry .foot {
            padding: 14px 0 6px;
            font-family: var(--mono);
            font-size: 0.66rem;
            letter-spacing: 0.12em;
            color: var(--paper-faint);
        }

        /* ── pull quote ────────────────────────────────────────────── */
        .pull {
            font-family: var(--serif);
            font-weight: 300;
            font-style: italic;
            font-size: clamp(1.4rem, 3.2vw, 2.1rem);
            line-height: 1.4;
            color: var(--paper);
            border-left: 2px solid var(--gold);
            padding: 6px 0 6px 30px;
            max-width: 42ch;
        }

        /* ── figures / counts ──────────────────────────────────────── */
        .figures { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0; margin-top: 40px; border-top: 1px solid var(--rule); }
        .figures div { padding: 26px 28px 26px 0; border-right: 1px solid var(--rule-soft); }
        .figures div:last-child { border-right: 0; }
        .figures .n { font-family: var(--serif); font-weight: 300; font-size: 2.6rem; line-height: 1; color: var(--gold); }
        .figures .k { display: block; font-family: var(--mono); font-size: 0.62rem; letter-spacing: 0.2em; text-transform: uppercase; color: var(--paper-faint); margin-bottom: 12px; }
        .figures p { color: var(--paper-dim); font-size: 0.92rem; margin-top: 10px; }

        .note {
            border-top: 1px solid var(--rule);
            margin-top: 40px;
            padding-top: 20px;
            font-family: var(--mono);
            font-size: 0.74rem;
            letter-spacing: 0.06em;
            color: var(--paper-faint);
        }
        .note b { color: var(--gold); letter-spacing: 0.18em; text-transform: uppercase; }

        /* ── closing ───────────────────────────────────────────────── */
        .closing { padding: 84px 0 96px; text-align: center; }
        .closing h2 {
            font-family: var(--serif);
            font-weight: 300;
            font-size: clamp(2.2rem, 5.4vw, 3.6rem);
            line-height: 1.05;
            letter-spacing: -0.02em;
        }
        .closing h2 em { font-style: italic; color: var(--gold); }
        .closing p { color: var(--paper-dim); max-width: 52ch; margin: 18px auto 30px; font-family: var(--serif); font-size: 1.15rem; }
        .closing .actions { justify-content: center; }

        /* ── light mode: it becomes actual paper ───────────────────── */
        body.shoug-light-mode {
            --ink: #f7f4ec;
            --ink-2: #fffdf8;
            --paper: #1c1a16;
            --paper-dim: #4c473d;
            --paper-faint: #7c7466;
            --rule: rgba(28, 26, 22, 0.18);
            --rule-soft: rgba(28, 26, 22, 0.1);
            --gold: #96662a;
            --gold-soft: rgba(150, 102, 42, 0.1);
            --sage: #3f6b47;
        }
        body.shoug-light-mode .grain {
            background:
                radial-gradient(ellipse 60% 40% at 20% 0%, rgba(150, 102, 42, 0.06), transparent 65%),
                radial-gradient(ellipse 50% 40% at 100% 30%, rgba(63, 107, 71, 0.05), transparent 60%);
        }
        body.shoug-light-mode .action.filled { color: #fffdf8; }
        body.shoug-light-mode ::selection { background: #96662a; color: #fffdf8; }


        /* The global light-mode sheet paints a lavender grid over every page; this
           one is a paper archive, so it reclaims its own ground. */
        body.shoug-light-mode.shoug-light-mode {
            background-color: var(--ink) !important;
            background-image: none !important;
            color: var(--paper) !important;
        }
        body.shoug-light-mode h1,
        body.shoug-light-mode h2,
        body.shoug-light-mode h3 { color: var(--paper); }
        body.shoug-light-mode .masthead h1 em,
        body.shoug-light-mode .sect-title em,
        body.shoug-light-mode .closing h2 em { color: var(--gold); }

        /* ── rtl ───────────────────────────────────────────────────── */
        html[dir="rtl"] main { direction: ltr; text-align: left; }

        /* ── responsive ────────────────────────────────────────────── */
        @media (max-width: 980px) {
            .colophon { grid-template-columns: 1fr; gap: 0; }
            .record { grid-template-columns: 96px minmax(0, 1fr); }
            .record .when, .record .go { grid-column: 2; }
            .figures { grid-template-columns: 1fr; }
            .figures div { border-right: 0; border-bottom: 1px solid var(--rule-soft); padding-right: 0; }
            .masthead { padding: 34px 0 34px; }
        }
        @media (max-width: 620px) {
            .entries article { grid-template-columns: 1fr; gap: 8px; }
            .colophon div { grid-template-columns: 1fr; gap: 2px; }
            .record { grid-template-columns: 1fr; gap: 8px; }
            .record .when, .record .go { grid-column: 1; }
            .pull { padding-left: 18px; }
        }
"""


BODY = """
    <div class="grain" aria-hidden="true"></div>

__HEADER__

    <main id="main-content" tabindex="-1">
        <div class="wrap">
            <div class="breadcrumb">
                <a href="/workshops/">Workshops</a><span class="sep">/</span><span>ACM PSU Digital Platform</span>
            </div>

            <header class="masthead">
                <div class="dir">Dir: /platforms/acm-psu &nbsp;&middot;&nbsp; designed &amp; built by me</div>
                <h1>The ACM PSU<br><em>digital platform.</em></h1>
                <p class="standfirst">
                    A central home for the ACM student chapter at Prince Sultan University &mdash; the club, its members,
                    its events, its projects and its past work. Students who want in register their interest through the
                    site; current members see every open role on every active event and put themselves forward.
                </p>
                <div class="byline">
                    <span>Role: <b>Designed &amp; built the platform</b></span>
                    <span>Chapter: <b>ACM PSU &middot; CCIS</b></span>
                    <span>Status: <b>In development</b></span>
                </div>
                <div class="actions">
                    <a class="action filled" href="https://acm-psu.shoug-tech.com/" target="_blank" rel="noopener">Visit the platform</a>
                    <a class="action" href="#purpose">Why it exists</a>
                    <a class="action" href="/workshops/">All workshops</a>
                </div>
            </header>

            <div class="colophon">
                <div><span class="k">Platform</span><span class="v">ACM PSU &mdash; club platform and digital archive</span></div>
                <div><span class="k">For</span><span class="v">ACM Student Chapter, College of Computer &amp; Information Sciences</span></div>
                <div><span class="k">Audience</span><span class="v">Prospective members, current members, and anyone looking up the chapter's past work</span></div>
                <div><span class="k">Documents</span><span class="v">ACM Programming Jam 2026 &middot; ACM/CyberTech CTF 3.0 &middot; the CTF 2.0 record</span></div>
                <div><span class="k">Sections</span><span class="v">Join &middot; Positions &middot; Projects &middot; Archive &middot; Team &middot; Member portal</span></div>
                <div><span class="k">Live at</span><span class="v">acm-psu.shoug-tech.com</span></div>
            </div>

            <section class="block" id="purpose">
                <div class="sect-mark">01 &mdash; Why it exists</div>
                <h2 class="sect-title">Opportunities visible to <em>everyone</em></h2>
                <p class="intro">Club opportunities used to travel by word of mouth, which meant the same few people did
                    the same work and everyone else heard about it afterwards. The platform publishes the openings to the
                    whole team, so taking part depends on wanting the work rather than on hearing about it first.</p>

                <div class="entries">
                    <article>
                        <div class="no">01</div>
                        <div>
                            <h3>Anyone interested can register</h3>
                            <p>Students who want to get involved apply through the site from their own account, so they
                                can follow the outcome and have a member dashboard ready the moment they are accepted.
                                <strong>No technical experience is required</strong> &mdash; the club exists to give
                                people that experience, not to test for it.</p>
                        </div>
                    </article>
                    <article>
                        <div class="no">02</div>
                        <div>
                            <h3>Members see every open role</h3>
                            <p>Active and upcoming events publish their available positions, each with the work involved,
                                the event it belongs to, remaining capacity and a closing date &mdash; the
                                <strong>same information to every member</strong>, at the same time.</p>
                        </div>
                    </article>
                    <article>
                        <div class="no">03</div>
                        <div>
                            <h3>Registering for a role is direct</h3>
                            <p>A request is recorded against the member's account and reviewed by an organizer. Members
                                may request more than one role, registration closes automatically at capacity, and every
                                request is <strong>timestamped on a verified record</strong>.</p>
                        </div>
                    </article>
                    <article>
                        <div class="no">04</div>
                        <div>
                            <h3>Hands-on experience is the point</h3>
                            <p>Organize an event, develop a workshop, build a website, contribute technically, help with
                                operations, or try something never done before &mdash; the registry shows
                                <strong>where help is actually needed</strong>.</p>
                        </div>
                    </article>
                    <article>
                        <div class="no">05</div>
                        <div>
                            <h3>The work stays documented</h3>
                            <p>The platform doubles as a long-term archive of the chapter's events, websites, resources,
                                projects and the members who contributed to them, so
                                <strong>work done for ACM remains part of the club's history</strong>.</p>
                        </div>
                    </article>
                </div>

                <div class="registry" style="margin-top: 44px;">
                    <div class="rhead"><span>Live registry &mdash; open assignments</span><span>Places remaining</span></div>
                    <ul>
                        <li><span>Event operations &mdash; <em>ACM Programming Jam 2026</em></span><span class="places">3 of 3</span></li>
                        <li><span>Registration &amp; participant support &mdash; <em>Programming Jam</em></span><span class="places">3 of 3</span></li>
                        <li><span>Workshop presenter &mdash; <em>Programming Jam</em></span><span class="places">2 of 2</span></li>
                        <li><span>Challenge tester &mdash; <em>ACM/CyberTech CTF 3.0</em></span><span class="places">2 of 2</span></li>
                        <li><span>CTF floor support &mdash; <em>CTF 3.0</em></span><span class="places">4 of 4</span></li>
                        <li><span>Media &amp; documentation &mdash; <em>CTF 3.0</em></span><span class="places">2 of 2</span></li>
                    </ul>
                    <div class="foot">Fair access protocol &mdash; members may request more than one role; registration
                        closes automatically at capacity.</div>
                </div>
            </section>

            <section class="block" id="what">
                <div class="sect-mark">02 &mdash; The platform</div>
                <h2 class="sect-title">Section by section</h2>
                <div class="catalogue">
                    <div class="record">
                        <div class="rid">01 / Join</div>
                        <div>
                            <h3>Membership</h3>
                            <p>Create an account, submit the application &mdash; name, student ID, PSU email, major, year,
                                and what you want experience in &mdash; then follow the outcome on your own status page.</p>
                        </div>
                        <div class="when">Public</div>
                        <div class="go"></div>
                    </div>
                    <div class="record">
                        <div class="rid">02 / Positions</div>
                        <div>
                            <h3>Open assignments</h3>
                            <p>A live registry of roles across active events, with the work, the event, remaining places
                                and the closing date stated for everyone.</p>
                        </div>
                        <div class="when">Members</div>
                        <div class="go"></div>
                    </div>
                    <div class="record">
                        <div class="rid">03 / Projects</div>
                        <div>
                            <h3>Technical collection</h3>
                            <p>Case studies for what the chapter builds &mdash; the Programming Jam, CTF 3.0, the CTF 2.0
                                results archive, and the workshop programmes behind them.</p>
                        </div>
                        <div class="when">Public</div>
                        <div class="go"></div>
                    </div>
                    <div class="record">
                        <div class="rid">04 / Archive</div>
                        <div>
                            <h3>Digital archive</h3>
                            <p>Everything the chapter has published, filterable by project and category: workshop
                                material, slide decks, reports, presentations, posters, branding and repositories.</p>
                        </div>
                        <div class="when">Public</div>
                        <div class="go"></div>
                    </div>
                    <div class="record">
                        <div class="rid">05 / Team</div>
                        <div>
                            <h3>Chapter roster</h3>
                            <p>The current generation and the ones before it, so contributions stay attached to the people
                                who made them rather than disappearing at the end of a term.</p>
                        </div>
                        <div class="when">Public</div>
                        <div class="go"></div>
                    </div>
                    <div class="record">
                        <div class="rid">06 / Portal</div>
                        <div>
                            <h3>Member dashboard</h3>
                            <p>The signed-in half of the site: applications, role requests, and a verified record of what
                                a member has taken on.</p>
                        </div>
                        <div class="when">Members</div>
                        <div class="go"></div>
                    </div>
                </div>
                <div class="stamps">
                    <span class="stamp on">Enrollment open</span>
                    <span class="stamp on">Recruiting</span>
                    <span class="stamp">Bilingual: AR / EN</span>
                    <span class="stamp">Archive: 17 records</span>
                </div>
            </section>

            <section class="block" id="events">
                <div class="sect-mark">03 &mdash; What it documents</div>
                <h2 class="sect-title">The chapter's <em>programme</em></h2>
                <p class="intro">The platform indexes the events I have pages for here, and the earlier editions that came
                    before them.</p>
                <div class="catalogue">
                    <a class="record" href="/workshops/ai-programming-jam/">
                        <div class="rid">JAM.26</div>
                        <div>
                            <h3>ACM Programming Jam 2026</h3>
                            <p>An AI-assisted web engineering competition with three preparation workshop days. I wrote
                                and taught all three days and built the event website.</p>
                        </div>
                        <div class="when">19 Sep 2026</div>
                        <div class="go">&rarr;</div>
                    </a>
                    <a class="record" href="/workshops/psu-ctf-3/">
                        <div class="rid">CTF 3.0</div>
                        <div>
                            <h3>ACM/CyberTech CTF 3.0</h3>
                            <p>A three-hour capture-the-flag across cryptography, web, forensics and OSINT, run with the
                                CyberTech Club. I built the competition website and co-organize it.</p>
                        </div>
                        <div class="when">24 Oct 2026</div>
                        <div class="go">&rarr;</div>
                    </a>
                    <a class="record" href="/workshops/psu-ctf/">
                        <div class="rid">CTF 2.0</div>
                        <div>
                            <h3>ACM/Cyber-Tech CTF 2.0</h3>
                            <p>The previous edition, whose verified record the platform archives: 11 teams, 852
                                submissions, 89 captures. I taught three of its five preparation workshops and built its
                                event site.</p>
                        </div>
                        <div class="when">Archived</div>
                        <div class="go">&rarr;</div>
                    </a>
                </div>
            </section>

            <section class="block" id="goal">
                <div class="sect-mark">04 &mdash; The goal</div>
                <h2 class="sect-title">Easier to join. Easier to <em>contribute</em>.</h2>
                <p class="pull">Make it easier to join, easier to contribute, and easier for every member to get real
                    experience through ACM.</p>
                <div class="figures">
                    <div>
                        <span class="k">Access</span>
                        <span class="n">One route in</span>
                        <p>A public application open to anyone who wants to participate, instead of an invitation that
                            depends on who you already know.</p>
                    </div>
                    <div>
                        <span class="k">Fairness</span>
                        <span class="n">Same view</span>
                        <p>Every opening visible to the whole team at once, with capacity and deadlines stated up front.</p>
                    </div>
                    <div>
                        <span class="k">Record</span>
                        <span class="n">Kept</span>
                        <p>Work done for ACM stays part of the chapter's history, credited to the members who did it.</p>
                    </div>
                </div>
                <div class="note">
                    <b>Status</b> &nbsp; The platform is in development. The full link and usage details go out to members
                    from the club once it is ready.
                </div>
            </section>
        </div>

        <div class="wrap">
            <div class="closing">
                <h2>The archive <em>isn't finished.</em></h2>
                <p>Your code, your designs, your leadership could define the next block.</p>
                <div class="actions">
                    <a class="action filled" href="https://acm-psu.shoug-tech.com/" target="_blank" rel="noopener">acm-psu.shoug-tech.com</a>
                    <a class="action" href="/workshops/">All workshops</a>
                </div>
            </div>
        </div>
    </main>

__FOOTER__
"""

PAGES = (Page(slug="", filename="", label="Overview", title=TITLE, description=DESCRIPTION),)
EVENT = Event(root=ROOT, base=BASE, css=THEME_CSS, fonts=FONTS, pages=PAGES, about=ABOUT, nav_label=EVENT_LABEL)


def main() -> int:
    chrome = extract_chrome()
    html = render(EVENT, chrome, BODY, url=EVENT.canonical, title=TITLE, description=DESCRIPTION)
    return write([(ROOT / "index.html", html)])


if __name__ == "__main__":
    raise SystemExit(main())
