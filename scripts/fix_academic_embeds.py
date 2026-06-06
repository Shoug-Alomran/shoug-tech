#!/usr/bin/env python3
"""Fix generated academic embed/link behavior after the section split."""

from __future__ import annotations

import html
import re
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
ACADEMICS = ROOT / "docs" / "Academics"
WORKSHOPS = ROOT / "docs" / "workshops"
ARABIC_LOCALIZATION_SCRIPT = '    <script src="/javascripts/arabic-localization.js"></script>\n'
TRANSLATION_LAUNCH_GUARD = '    <script src="/javascripts/translation-launch-guard.js"></script>\n'
LANGUAGE_QUERY_SUPPORT = """            function initialLang() {
                var requestedLang = new URLSearchParams(window.location.search).get('lang');
                if (requestedLang === 'ar' || requestedLang === 'en') return requestedLang;"""
SAFE_BREADCRUMB_TRANSLATION = """                document.querySelectorAll('.breadcrumb').forEach(function (node) {
                    node.querySelectorAll('a').forEach(function (link) {
                        if (normalizeLabel(link.textContent) === 'academics' || normalizeLabel(link.textContent) === 'الدراسة') {
                            link.textContent = t.breadcrumbAcademics;
                        }
                    });
                });"""


PDF_IFRAME_RE = re.compile(
    r'<iframe\b(?=[^>]*\bsrc=(["\'])(?P<src>/Academics/[^"\']*/slides/[^"\']*\.pdf)\1)[^>]*>\s*</iframe>',
    re.S,
)
SOURCE_IFRAME_RE = re.compile(
    r'<iframe\b(?=[^>]*\bsrc=(["\'])(?P<src>/(?:ar/)?Academics/[^"\']*\.(?:pdf|html))\1)[^>]*>',
    re.S,
)
PRIMARY_ACTION_RE = re.compile(
    r'<a class="btn btn-primary" href="(?P<href>[^"]*)"(?P<attrs>[^>]*)>\[[^\]]*(?:->|-&gt;)\s*\]</a>'
)
PDF_PRIMARY_ACTION_RE = re.compile(
    r'<a class="btn btn-primary" href="(?P<href>/Academics/[^"]*/slides/[^"]*\.pdf)"(?P<attrs>[^>]*)>\[[^\]]*(?:->|-&gt;)\s*\]</a>'
)
PDF_LINK_RE = re.compile(
    r'<a\b(?P<before>(?:(?!\btarget=)[^>])*?)href="(?P<href>/Academics/[^"]*\.pdf)"(?P<after>(?:(?!\btarget=)[^>])*)>'
)
ACADEMIC_HTML_URL_RE = re.compile(r'(?P<quote>["\'])(?P<url>/(?:ar/)?Academics/[^"\']+\.html)(?P=quote)')
INNER_OPEN_LINK_RE = re.compile(
    r'\s*<li>\s*<a href="[^"]+\.(?:html|pdf)"[^>]*>[^<]*(?:new tab|صفحة جديدة|open pdf slides|فتح ملف pdf)[^<]*</a>\s*</li>',
    re.I,
)
EMPTY_LIST_RE = re.compile(r'\s*<ul>\s*</ul>', re.I)
NAV_STRIP_RE = re.compile(r'<div class="nav-strip uppercase">.*?</div>', re.S)
SLIDE_BREAKDOWN_LABEL_RE = re.compile(r'(?P<prefix><a class="breadcrumb-link" href="[^"]*/slide-breakdowns/">)\s*Slides\s*(?P<suffix></a>)')
SLIDE_BREAKDOWN_CURRENT_RE = re.compile(r'(?P<prefix><span class="current">)\s*Slides\s*(?P<suffix></span>)')
SLIDE_LABEL_RE = re.compile(r'(ITEM_\d+\s*//\s*)SLIDES\b')
VIEWER_PRIMARY_RE = re.compile(r'<a class="btn btn-primary" href="[^"]*"[^>]*>\[[^\]]*(?:-&gt;|->)\s*\]</a>')
EMBED_CONTAINER_RE = re.compile(r'<div class="embed-container" id="embedded-content">.*?</div>\s*</div>', re.S)
EMBED_AREA_WRAPPER_RE = re.compile(
    r'<div class="embed-area-wrapper"[^>]*>.*?(?=\s*</main>)',
    re.S,
)
DIR_ROW_RE = re.compile(r'(<a href="(?P<route>[^"]+/slide-breakdowns/[^"]+/)" class="dir-row"[^>]*>.*?<span class="status-tag">)(?P<status>[^<]*)(</span>.*?</a>)', re.S)
RENDERED_IFRAME_WRAP_RE = re.compile(
    r'(<div class="rendered-content"[^>]*>)(?:(?!<div class="rendered-content").)*?'
    r'(<div class="iframe-wrap">\s*<iframe class="embed-frame[^>]*>\s*</iframe>\s*</div>)',
    re.S,
)
RENDERED_BARE_IFRAME_RE = re.compile(
    r'(<div class="rendered-content"[^>]*>)(?:(?!<div class="rendered-content").)*?'
    r'(<iframe class="embed-frame[^>]*>\s*</iframe>)',
    re.S,
)
RENDERED_PREFIX_BEFORE_EMBED_RE = re.compile(
    r'(<div class="rendered-content"[^>]*>).*?(?=(?:<div class="iframe-wrap">\s*)?<iframe class="embed-frame)',
    re.S,
)
PDF_RESOURCE_LINK_RE = re.compile(
    r'\s*<p class="embedded-resource-link"><a href="(?P<src>/Academics/[^"]+\.pdf)"[^>]*>[^<]*</a></p>',
    re.S,
)
GENERIC_ACADEMIC_HTML_IFRAME_RE = re.compile(
    r'<iframe\b(?=[^>]*\bsrc=(["\'])(?P<src>/(?:ar/)?Academics/[^"\']+\.html)\1)[^>]*>\s*</iframe>',
    re.S,
)
GENERIC_ACADEMIC_HTML_IFRAME_OPEN_RE = re.compile(
    r'<iframe\b(?=[^>]*\bsrc=(["\'])(?P<src>/(?:ar/)?Academics/[^"\']+\.html)\1)[^>]*>(?!\s*</iframe>)',
    re.S,
)
ACADEMIC_SIDEBAR_FIX = """
    <style id="academic-sidebar-embed-fix">
    .academic-sidebar {
        display: flex !important;
        flex-direction: column !important;
        align-self: stretch !important;
        overflow: hidden !important;
    }
    .academic-sidebar .file-tree {
        display: block !important;
        flex: 1 1 auto !important;
        min-height: 0 !important;
        padding: 28px 0 34px !important;
        overflow-y: auto !important;
    }
    .academic-sidebar .tree-node {
        display: block !important;
        align-items: initial !important;
        gap: 0 !important;
        cursor: default !important;
        color: inherit !important;
    }
    .academic-sidebar .tree-node:hover {
        color: inherit !important;
    }
    .academic-sidebar .tree-item {
        margin-top: 0 !important;
    }
    </style>"""
ACADEMIC_SIDEBAR_FIX_RE = re.compile(
    r'\s*<style id="academic-sidebar-embed-fix">.*?</style>',
    re.S,
)
SECTION_DIRECTORY_RE = re.compile(
    r'<div class="directory-container"[^>]*>.*?(?=\s*<footer\b)',
    re.S,
)
SECTION_ROW_RE = re.compile(r'<(?:a|div)\b[^>]*class="[^"]*\bdir-row\b', re.S)
EMPTY_SECTION_MARKER_RE = re.compile(
    r'No (?:slide breakdowns|slides) uploaded yet|Quizzes coming soon',
    re.I,
)
GENERATED_EMPTY_SECTION_RE = re.compile(
    r'<style id="empty-section-state-style">.*?(?=\s*<footer\b)',
    re.S,
)
COMING_SOON_COMPONENT_RE = re.compile(
    r'<div class="coming-soon-container"[^>]*>\s*'
    r'<div class="coming-soon-icon"[^>]*>.*?</div>\s*'
    r'<div class="coming-soon-title"[^>]*>.*?</div>\s*'
    r'<div class="coming-soon-text"[^>]*>.*?</div>\s*</div>',
    re.S,
)
COMING_SOON_COMPONENT = '''<div class="coming-soon-container" role="status">
                <div class="coming-soon-icon" aria-hidden="true">[ _ ]</div>
                <div class="coming-soon-title">COMING SOON</div>
                <div class="coming-soon-text">Content for this section is being prepared and will be available soon.</div>
            </div>'''
EMPTY_SECTION_STATE = '''
            <style id="empty-section-state-style">
                .coming-soon-container {
                    flex-grow: 1;
                    min-height: clamp(520px, 65vh, 900px);
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    padding: 80px 40px;
                    gap: 24px;
                    text-align: center;
                }
                .coming-soon-icon {
                    font-family: var(--font-mono);
                    font-size: 3rem;
                    color: var(--text-tertiary);
                    opacity: 0.4;
                }
                .coming-soon-title {
                    font-family: var(--font-display);
                    font-size: 2rem;
                    font-weight: 700;
                    color: var(--text-secondary);
                    text-transform: uppercase;
                }
                .coming-soon-text {
                    max-width: 520px;
                    font-family: var(--font-mono);
                    font-size: 0.95rem;
                    line-height: 1.8;
                    color: var(--text-tertiary);
                }
            </style>
            <div class="coming-soon-container" role="status">
                <div class="coming-soon-icon" aria-hidden="true">[ _ ]</div>
                <div class="coming-soon-title">COMING SOON</div>
                <div class="coming-soon-text">Content for this section is being prepared and will be available soon.</div>
            </div>
'''


def open_button(href: str) -> str:
    return (
        f'<a class="btn btn-primary" href="{href}" '
        'target="_blank" rel="noopener">[ OPEN IN NEW TAB -&gt; ]</a>'
    )


def replace_primary_action(content: str) -> str:
    match = SOURCE_IFRAME_RE.search(content)
    if not match:
        return PDF_PRIMARY_ACTION_RE.sub(lambda m: open_button(m.group("href")), content, count=1)
    source = match.group("src")
    return PRIMARY_ACTION_RE.sub(open_button(source), content, count=1)


def filesystem_path_for_url(url: str) -> Path:
    return ROOT / "docs" / unquote(html.unescape(url).lstrip("/"))


def candidate_academic_html_url(url: str) -> str | None:
    decoded = html.unescape(url)
    if decoded.startswith("/ar/Academics/"):
        english_url = decoded[3:]
        arabic_url = english_url[:-5] + ".ar.html"
        if filesystem_path_for_url(arabic_url).exists():
            return arabic_url
        if filesystem_path_for_url(english_url).exists():
            return english_url
    if decoded != url and filesystem_path_for_url(decoded).exists():
        return decoded
    return candidate_slide_breakdown_url(decoded)


def candidate_slide_breakdown_url(url: str) -> str | None:
    prefix = "/Academics/"
    arabic = False
    body = url
    if body.startswith("/ar/Academics/"):
        arabic = True
        body = body[3:]

    if not body.startswith(prefix) or "/slide-breakdowns/" in body:
        if arabic and body.startswith(prefix):
            ar_url = body[:-5] + ".ar.html"
            if filesystem_path_for_url(ar_url).exists():
                return ar_url
        return None

    parts = body[len(prefix):].split("/")
    if len(parts) < 3:
        return None

    suffix = "/".join(parts[2:])
    if suffix.startswith(("slides/", "study-material/", "study_material/", "quizzes/", "quizez/", "overview/")):
        return None

    inserted = f"{prefix}{parts[0]}/{parts[1]}/slide-breakdowns/{suffix}"
    candidates = []
    if arabic:
        candidates.append(inserted[:-5] + ".ar.html")
    candidates.append(inserted)

    for candidate in candidates:
        if filesystem_path_for_url(candidate).exists():
            return candidate
    return None


def correct_slide_breakdown_urls(content: str) -> str:
    def replacement(match: re.Match[str]) -> str:
        url = match.group("url")
        corrected = candidate_academic_html_url(url)
        if not corrected:
            return match.group(0)
        quote = match.group("quote")
        return f"{quote}{corrected}{quote}"

    return ACADEMIC_HTML_URL_RE.sub(replacement, content)


def remove_inner_open_links(content: str) -> str:
    content = INNER_OPEN_LINK_RE.sub("", content)
    return EMPTY_LIST_RE.sub("", content)


def fix_slide_breakdown_labels(content: str) -> str:
    content = SLIDE_BREAKDOWN_LABEL_RE.sub(r"\g<prefix>Slide Breakdowns\g<suffix>", content)
    content = SLIDE_BREAKDOWN_CURRENT_RE.sub(r"\g<prefix>Slide Breakdowns\g<suffix>", content)
    return SLIDE_LABEL_RE.sub(r"\1SLIDE BREAKDOWNS", content)


def has_embedded_html(content: str) -> bool:
    return bool(re.search(r'<iframe\b[^>]*\bsrc=["\']/Academics/[^"\']+\.html["\']', content, re.S))


def coming_soon_panel() -> str:
    return (
        '<div class="embed-container" id="embedded-content">'
        '<div class="rendered-content coming-soon-panel">'
        '<h2>Coming Soon</h2>'
        '<p>This HTML slide breakdown is coming soon.</p>'
        '</div></div></div>'
    )


def mark_viewer_coming_soon(content: str) -> str:
    content = VIEWER_PRIMARY_RE.sub(
        '<span class="btn btn-primary btn-disabled" aria-disabled="true">[ COMING SOON ]</span>',
        content,
        count=1,
    )
    replacement = (
        '<div class="embed-area-wrapper" vid="82">\n'
        f'                {coming_soon_panel()}\n'
        '            </div>\n'
    )
    if EMBED_AREA_WRAPPER_RE.search(content):
        return EMBED_AREA_WRAPPER_RE.sub(replacement, content, count=1)
    return EMBED_CONTAINER_RE.sub(coming_soon_panel(), content, count=1)


def route_has_available_slide_breakdown(route: str) -> bool:
    page_path = ROOT / "docs" / route.lstrip("/") / "index.html"
    if not page_path.exists():
        return False
    return has_embedded_html(page_path.read_text(encoding="utf-8"))


def update_slide_breakdown_index_status(content: str) -> str:
    def replacement(match: re.Match[str]) -> str:
        status = "AVAILABLE" if route_has_available_slide_breakdown(match.group("route")) else "COMING SOON"
        return f'{match.group(1)}{status}{match.group(4)}'

    return DIR_ROW_RE.sub(replacement, content)


def show_embeds_without_intro(content: str, *, allow_pdf_embed: bool) -> str:
    content = GENERIC_ACADEMIC_HTML_IFRAME_RE.sub(
        lambda m: f'<iframe class="embed-frame legacy-html-frame" src="{m.group("src")}" loading="lazy"></iframe>',
        content,
    )
    content = GENERIC_ACADEMIC_HTML_IFRAME_OPEN_RE.sub(
        lambda m: f'<iframe class="embed-frame legacy-html-frame" src="{m.group("src")}" loading="lazy"></iframe>',
        content,
    )
    content = RENDERED_PREFIX_BEFORE_EMBED_RE.sub(r"\1", content)
    content = RENDERED_IFRAME_WRAP_RE.sub(r"\1\2", content)
    content = RENDERED_BARE_IFRAME_RE.sub(r"\1\2", content)
    if not allow_pdf_embed:
        return PDF_RESOURCE_LINK_RE.sub("", content)
    return PDF_RESOURCE_LINK_RE.sub(
        lambda m: f'<iframe class="embed-frame" src="{m.group("src")}" title="PDF"></iframe>',
        content,
    )


def add_sidebar_embed_fix(content: str) -> str:
    if "academic-sidebar" not in content:
        return content
    if "academic-sidebar-embed-fix" in content:
        return ACADEMIC_SIDEBAR_FIX_RE.sub(ACADEMIC_SIDEBAR_FIX, content, count=1)
    return content.replace("</head>", f"{ACADEMIC_SIDEBAR_FIX}\n</head>", 1)


def normalize_empty_section(content: str) -> str:
    content = COMING_SOON_COMPONENT_RE.sub(COMING_SOON_COMPONENT, content)
    state = EMPTY_SECTION_STATE.strip()
    if GENERATED_EMPTY_SECTION_RE.search(content):
        return GENERATED_EMPTY_SECTION_RE.sub(state, content, count=1)
    match = SECTION_DIRECTORY_RE.search(content)
    if not match or '<div class="dir-header">' not in match.group(0):
        return content
    directory = match.group(0)
    if SECTION_ROW_RE.search(directory) and not EMPTY_SECTION_MARKER_RE.search(directory):
        return content
    return content[:match.start()] + state + content[match.end():]


def add_arabic_localization(content: str) -> str:
    if "shoug-lang-btn" not in content or "/javascripts/arabic-localization.js" in content:
        return content
    return content.replace("</body>", f"{ARABIC_LOCALIZATION_SCRIPT}</body>", 1)


def add_translation_launch_guard(content: str) -> str:
    if "data-lang-toggle" not in content or "/javascripts/translation-launch-guard.js" in content:
        return content
    return content.replace("</head>", f"{TRANSLATION_LAUNCH_GUARD}</head>", 1)


def add_language_query_support(content: str) -> str:
    if "function initialLang()" not in content or "var requestedLang = new URLSearchParams" in content:
        return content
    return content.replace("            function initialLang() {", LANGUAGE_QUERY_SUPPORT, 1)


def fix_arabic_shell_script(content: str) -> str:
    content = re.sub(
        r"\s*document\.querySelectorAll\('\.breadcrumb'\)\.forEach\(function \(node\) \{.*?\n\s*\}\);"
        r"(?=\n\s*document\.querySelectorAll\('\.hero-label'\))",
        "\n" + SAFE_BREADCRUMB_TRANSLATION,
        content,
        count=1,
        flags=re.S,
    )
    content = content.replace(
        "document.getElementById('live-clock').textContent = `SYS_TIME: ${timeString}:${ms}`;",
        "document.getElementById('live-clock').textContent = `${document.documentElement.lang.indexOf('ar') === 0 ? 'وقت_النظام' : 'SYS_TIME'}: ${timeString}:${ms}`;",
    )
    return content


def remove_pdf_iframes_from_breakdown(content: str) -> str:
    def replacement(match: re.Match[str]) -> str:
        src = match.group("src")
        return (
            '<p class="embedded-resource-link">'
            f'<a href="{src}" target="_blank" rel="noopener">Open PDF in the Slides section</a>'
            '</p>'
        )

    return PDF_IFRAME_RE.sub(replacement, content)


def add_pdf_link_targets(content: str) -> str:
    def replacement(match: re.Match[str]) -> str:
        return (
            f'<a{match.group("before")}href="{match.group("href")}"'
            f'{match.group("after")} target="_blank" rel="noopener">'
        )

    return PDF_LINK_RE.sub(replacement, content)


def route_for_page(path: Path) -> str:
    rel = path.relative_to(ROOT / "docs").as_posix()
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def remove_index_row(index_content: str, route: str) -> str:
    row_re = re.compile(
        rf'\s*<a href="{re.escape(route)}" class="dir-row"[^>]*>.*?</a>',
        re.S,
    )
    return row_re.sub("", index_content)


def remove_sidebar_item(content: str, route: str) -> str:
    item_re = re.compile(
        rf'<li class="tree-item tree-viewer[^"]*"><a class="tree-file" href="{re.escape(route)}">.*?</a></li>',
        re.S,
    )
    return item_re.sub("", content)


def course_slide_index_for_route(route: str) -> str:
    return route.split("/slide-breakdowns/", 1)[0] + "/slide-breakdowns/"


def update_course_navigation(index_path: Path) -> int:
    index_content = index_path.read_text(encoding="utf-8")
    routes = re.findall(r'<a href="([^"]+/slide-breakdowns/[^"]+/)" class="dir-row"', index_content)
    if not routes:
        return 0

    changed = 0
    index_route = course_slide_index_for_route(routes[0])
    for idx, route in enumerate(routes):
        page_path = ROOT / "docs" / route.lstrip("/") / "index.html"
        if not page_path.exists():
            continue
        content = page_path.read_text(encoding="utf-8")
        previous_route = routes[idx - 1] if idx > 0 else index_route
        next_route = routes[idx + 1] if idx < len(routes) - 1 else index_route
        replacement = (
            '<div class="nav-strip uppercase">'
            f'<a href="{previous_route}" class="nav-link prev">&lt;- PREVIOUS</a>'
            f'<a href="{next_route}" class="nav-link next">NEXT -&gt;</a>'
            '</div>'
        )
        cleaned = NAV_STRIP_RE.sub(replacement, content, count=1)
        if cleaned != content:
            page_path.write_text(cleaned, encoding="utf-8")
            changed += 1
    return changed


def main() -> None:
    updated = 0
    pdf_only_breakdown_routes: list[str] = []
    for path in sorted(ACADEMICS.rglob("*.html")):
        content = path.read_text(encoding="utf-8")
        original = content

        content = correct_slide_breakdown_urls(content)

        if "/slide-breakdowns/" in path.as_posix():
            content = fix_slide_breakdown_labels(content)
            content = remove_inner_open_links(content)
            if PDF_PRIMARY_ACTION_RE.search(content):
                pdf_only_breakdown_routes.append(route_for_page(path))
            content = remove_pdf_iframes_from_breakdown(content)

        content = replace_primary_action(content)
        content = add_pdf_link_targets(content)
        content = show_embeds_without_intro(content, allow_pdf_embed="/slide-breakdowns/" not in path.as_posix())
        content = normalize_empty_section(content)
        if "/slide-breakdowns/" in path.as_posix() and path.name == "index.html":
            if path.parent.name == "slide-breakdowns":
                content = update_slide_breakdown_index_status(content)
            elif not has_embedded_html(content):
                content = mark_viewer_coming_soon(content)
        content = add_sidebar_embed_fix(content)
        content = add_translation_launch_guard(content)
        content = add_arabic_localization(content)
        content = add_language_query_support(content)
        content = fix_arabic_shell_script(content)

        if content != original:
            path.write_text(content, encoding="utf-8")
            updated += 1

    for route in pdf_only_breakdown_routes:
        index_path = ROOT / "docs" / route.lstrip("/").split("/slide-breakdowns/", 1)[0] / "slide-breakdowns" / "index.html"
        if not index_path.exists():
            continue
        content = index_path.read_text(encoding="utf-8")
        cleaned = remove_index_row(content, route)
        if cleaned != content:
            index_path.write_text(cleaned, encoding="utf-8")
            updated += 1

    if pdf_only_breakdown_routes:
        touched_indexes: set[Path] = set()
        for path in sorted(ACADEMICS.rglob("*.html")):
            content = path.read_text(encoding="utf-8")
            cleaned = content
            for route in pdf_only_breakdown_routes:
                cleaned = remove_sidebar_item(cleaned, route)
                if f'href="{route}"' in cleaned:
                    cleaned = cleaned.replace(f'href="{route}"', f'href="{course_slide_index_for_route(route)}"')
            if cleaned != content:
                path.write_text(cleaned, encoding="utf-8")
                updated += 1

        for route in pdf_only_breakdown_routes:
            index_path = ROOT / "docs" / route.lstrip("/").split("/slide-breakdowns/", 1)[0] / "slide-breakdowns" / "index.html"
            if index_path.exists():
                touched_indexes.add(index_path)

        for index_path in sorted(touched_indexes):
            updated += update_course_navigation(index_path)

    for path in sorted(WORKSHOPS.rglob("*.html")):
        content = path.read_text(encoding="utf-8")
        cleaned = add_sidebar_embed_fix(content)
        cleaned = add_translation_launch_guard(cleaned)
        cleaned = add_arabic_localization(cleaned)
        cleaned = add_language_query_support(cleaned)
        cleaned = fix_arabic_shell_script(cleaned)
        if cleaned != content:
            path.write_text(cleaned, encoding="utf-8")
            updated += 1

    for path in sorted((ROOT / "docs").rglob("*.html")):
        content = path.read_text(encoding="utf-8")
        cleaned = add_translation_launch_guard(content)
        cleaned = add_arabic_localization(cleaned)
        cleaned = add_language_query_support(cleaned)
        cleaned = fix_arabic_shell_script(cleaned)
        if cleaned != content:
            path.write_text(cleaned, encoding="utf-8")
            updated += 1

    print(f"Updated {updated} academic HTML files")


if __name__ == "__main__":
    main()
