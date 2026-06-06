#!/usr/bin/env python3
"""Patch generated standalone HTML with mobile navigation and overflow fixes."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

MOBILE_FIX_CSS = r"""
    <style id="mobile-launch-fixes">
        html,
        body {
            max-width: 100%;
        }

        body {
            overflow-x: hidden;
        }

        .layout-wrapper,
        .app-layout,
        .content-area,
        .page-content,
        .content-scroll-area,
        .embed-area-wrapper,
        .embed-container,
        main,
        section,
        article {
            max-width: 100%;
            min-width: 0;
        }

        img,
        svg,
        video,
        canvas,
        iframe {
            max-width: 100%;
        }

        .shoug-header-menu-btn,
        .shoug-directory-btn {
            min-width: 34px;
            height: 34px;
            display: none;
            align-items: center;
            justify-content: center;
            border: 1px solid rgba(184, 41, 234, 0.45);
            background: rgba(184, 41, 234, 0.08);
            color: #f8f7fb;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.62rem;
            font-weight: 800;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            cursor: pointer;
        }

        .shoug-header-menu-btn:hover,
        .shoug-directory-btn:hover {
            border-color: rgba(184, 41, 234, 0.7);
            background: rgba(184, 41, 234, 0.16);
        }

        body.shoug-light-mode .shoug-header-menu-btn,
        body.shoug-light-mode .shoug-directory-btn {
            color: #16111f;
            background: rgba(255, 255, 255, 0.72);
        }

        .shoug-header-backdrop {
            display: none;
        }

        @media (max-width: 760px) {
            .shoug-site-header {
                min-height: 68px !important;
                height: auto !important;
            }

            .shoug-header-inner {
                width: calc(100% - 28px) !important;
                min-height: 68px !important;
                flex-wrap: nowrap !important;
                gap: 8px !important;
                padding: 8px 0 !important;
            }

            .shoug-header-logo {
                max-width: 38vw !important;
                overflow: hidden !important;
                text-overflow: ellipsis !important;
                font-size: 0.74rem !important;
                letter-spacing: 0.12em !important;
            }

            .shoug-header-menu-btn {
                display: inline-flex !important;
            }

            body:has(.academic-sidebar) .shoug-directory-btn {
                display: inline-flex !important;
            }

            .shoug-header-actions {
                gap: 6px !important;
                margin-left: auto !important;
            }

            .shoug-icon-btn,
            .shoug-lang-btn,
            .shoug-theme-btn {
                width: 32px !important;
                height: 32px !important;
                flex: 0 0 32px !important;
            }

            .shoug-contact-btn {
                height: 32px !important;
                padding-inline: 10px !important;
                font-size: 0.58rem !important;
                letter-spacing: 0.12em !important;
            }

            .shoug-header-nav {
                position: fixed !important;
                left: 14px !important;
                right: 14px !important;
                top: 74px !important;
                z-index: 10020 !important;
                width: auto !important;
                max-height: calc(100vh - 96px) !important;
                display: grid !important;
                grid-template-columns: 1fr !important;
                gap: 0 !important;
                overflow: auto !important;
                padding: 10px !important;
                border: 1px solid rgba(184, 41, 234, 0.38) !important;
                background: rgba(5, 5, 8, 0.98) !important;
                box-shadow: 0 22px 70px rgba(0, 0, 0, 0.62) !important;
                opacity: 0 !important;
                pointer-events: none !important;
                transform: translateY(-8px) !important;
                transition: opacity 160ms ease, transform 160ms ease !important;
            }

            body.mobile-nav-open .shoug-header-nav {
                opacity: 1 !important;
                pointer-events: auto !important;
                transform: translateY(0) !important;
            }

            body.shoug-light-mode .shoug-header-nav {
                background: rgba(246, 244, 251, 0.98) !important;
            }

            .shoug-header-nav a {
                min-height: 44px !important;
                display: flex !important;
                align-items: center !important;
                padding: 0 14px !important;
                border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
                font-size: 0.76rem !important;
            }

            .shoug-header-nav a:last-child {
                border-bottom: 0 !important;
            }

            .shoug-header-backdrop {
                position: fixed;
                inset: 68px 0 0;
                z-index: 10010;
                background: rgba(0, 0, 0, 0.54);
                backdrop-filter: blur(2px);
                -webkit-backdrop-filter: blur(2px);
            }

            body.mobile-nav-open .shoug-header-backdrop,
            body.sidebar-open .shoug-header-backdrop {
                display: block;
            }

            .layout-wrapper,
            .app-layout {
                width: 100% !important;
                overflow-x: hidden !important;
            }

            .content-area,
            .page-content,
            .content-scroll-area {
                width: 100% !important;
                overflow-x: hidden !important;
            }

            .top-bar,
            .content-topbar,
            .breadcrumb {
                overflow-x: auto !important;
                -webkit-overflow-scrolling: touch;
            }

            .page-header,
            .content-header,
            .content-section,
            .embed-area-wrapper {
                padding-left: 16px !important;
                padding-right: 16px !important;
            }

            .embed-container {
                width: 100% !important;
                overflow: hidden !important;
            }

            .embed-container iframe,
            .embed-frame {
                width: 100% !important;
                min-height: 72vh !important;
                height: 72vh !important;
            }

            .hero {
                min-height: auto !important;
                padding-top: clamp(72px, 18vh, 132px) !important;
                padding-left: 24px !important;
                padding-right: 24px !important;
            }

            .hero-bg-glow {
                left: 0 !important;
                width: 100vw !important;
                max-width: 100vw !important;
                overflow: hidden !important;
            }

            .ticker-wrap {
                max-width: 100vw !important;
                overflow: hidden !important;
                contain: paint;
            }

            .ticker-content {
                width: 100% !important;
                max-width: 100% !important;
                overflow: hidden !important;
            }

            .hero-ctas,
            .action-buttons,
            .filter-bar,
            .sub-nav,
            .content-tabs {
                flex-wrap: wrap !important;
            }

            .work-grid,
            .projects-grid,
            .project-grid,
            .explore-grid,
            .panels-grid,
            .proof,
            [class*="cards-grid"],
            [class*="card-grid"] {
                grid-template-columns: 1fr !important;
            }

            .work-card,
            .project-card,
            .card,
            [class*="-card"] {
                max-width: 100% !important;
                min-width: 0 !important;
                overflow-wrap: anywhere;
            }

            table {
                display: block;
                max-width: 100%;
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
            }
        }

        @media (max-width: 640px) {
            .shoug-header-logo {
                max-width: 32vw !important;
            }

            .shoug-header-actions a[aria-label="GitHub"],
            .shoug-header-actions a[aria-label="LinkedIn"],
            .shoug-header-actions a[aria-label="جيت هب"],
            .shoug-header-actions a[aria-label="لينكدإن"] {
                display: none !important;
            }
        }
    </style>
"""

MOBILE_FIX_JS = r"""
    <script id="mobile-launch-fixes-script">
        (function () {
            var mobileMenuButton = document.querySelector('.shoug-header-menu-btn');
            var directoryButton = document.querySelector('.shoug-directory-btn');
            var mobileOverlay = document.querySelector('[data-mobile-overlay]');
            var primaryNav = document.querySelector('.shoug-header-nav');
            if (primaryNav && !primaryNav.id) primaryNav.id = 'shoug-mobile-nav';

            function setMobileMenu(open) {
                document.body.classList.toggle('mobile-nav-open', open);
                if (mobileMenuButton) {
                    mobileMenuButton.setAttribute('aria-expanded', open ? 'true' : 'false');
                    mobileMenuButton.setAttribute('aria-label', open ? 'Close site menu' : 'Open site menu');
                }
            }

            function setDirectory(open) {
                document.body.classList.toggle('sidebar-open', open);
                if (directoryButton) {
                    directoryButton.setAttribute('aria-expanded', open ? 'true' : 'false');
                    directoryButton.setAttribute('aria-label', open ? 'Close academic directory' : 'Open academic directory');
                }
            }

            if (mobileMenuButton) {
                mobileMenuButton.addEventListener('click', function () {
                    var next = !document.body.classList.contains('mobile-nav-open');
                    setDirectory(false);
                    setMobileMenu(next);
                });
            }

            if (directoryButton) {
                if (!document.querySelector('.academic-sidebar')) directoryButton.hidden = true;
                directoryButton.addEventListener('click', function () {
                    var next = !document.body.classList.contains('sidebar-open');
                    setMobileMenu(false);
                    setDirectory(next);
                });
            }

            if (mobileOverlay) {
                mobileOverlay.addEventListener('click', function () {
                    setMobileMenu(false);
                    setDirectory(false);
                });
            }

            document.addEventListener('keydown', function (event) {
                if (event.key === 'Escape') {
                    setMobileMenu(false);
                    setDirectory(false);
                }
            });

            document.querySelectorAll('.shoug-header-nav a, .academic-sidebar a').forEach(function (link) {
                link.addEventListener('click', function () {
                    setMobileMenu(false);
                    setDirectory(false);
                });
            });
        })();
    </script>
"""

MOBILE_FIX_STYLESHEET = '    <link rel="stylesheet" href="/styles/mobile-fixes.css">'
MOBILE_FIX_SCRIPT = '    <script src="/javascripts/mobile-navigation.js"></script>'

MENU_BUTTONS = (
    '<button class="shoug-header-menu-btn" type="button" aria-label="Open site menu" '
    'aria-controls="shoug-mobile-nav" aria-expanded="false">Menu</button>\n'
    '                <button class="shoug-directory-btn" type="button" '
    'aria-label="Open academic directory" aria-expanded="false">Dir</button>'
)


def patch_html(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    if "shoug-site-header" not in text:
        return False

    text = re.sub(r"\s*<style id=\"mobile-launch-fixes\">.*?</style>", "", text, count=1, flags=re.S)
    if "/styles/mobile-fixes.css" not in text:
        text = text.replace("</head>", MOBILE_FIX_STYLESHEET + "\n</head>", 1)

    text = re.sub(
        r'<nav class="shoug-header-nav"(?![^>]*\bid=)',
        '<nav class="shoug-header-nav" id="shoug-mobile-nav"',
        text,
        count=1,
    )

    if 'aria-label="Open site menu"' not in text and "aria-label='Open site menu'" not in text:
        text = text.replace('<div class="shoug-header-actions">', '<div class="shoug-header-actions">\n                ' + MENU_BUTTONS, 1)

    if "data-mobile-overlay" not in text:
        text = re.sub(r"(\s*</header>)", '\n        <div class="shoug-header-backdrop" data-mobile-overlay></div>\\1', text, count=1)

    text = re.sub(r"\s*<script id=\"mobile-launch-fixes-script\">.*?</script>", "", text, count=1, flags=re.S)
    if "/javascripts/mobile-navigation.js" not in text:
        text = text.replace("</body>", MOBILE_FIX_SCRIPT + "\n</body>", 1)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    for html_file in sorted(DOCS.rglob("*.html")):
        if patch_html(html_file):
            changed += 1
    print(f"patched {changed} generated HTML files")


if __name__ == "__main__":
    main()
