#!/usr/bin/env python3
"""Give every interactive mindmap a real landscape PDF export.

The original Export button called window.print() on the live canvas, which
printed whatever happened to be on screen: portrait, clipped at the viewport,
and missing every collapsed branch. This replaces it with a purpose-built
print sheet — all branches expanded, laid out as balanced columns, scaled to
fit exactly one landscape page.

The mindmaps are generated from the ETHCS303 chapter-1 page (see
build_se401_study_tools.ETHICS_MAP_TEMPLATE), so patching that template makes
the export survive regeneration; the already-generated pages are patched too.

    python3 scripts/add_mindmap_pdf_export.py [path ...]

Idempotent: pages that already carry the sheet are skipped.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DEFAULT_TARGETS = [
    ROOT / "docs/academics/other-courses/ethcs303/extra-resources/mindmap",
    ROOT / "docs/academics",
]

PRINT_CSS = """
        /* ─────────────────────────────────────────────
           PDF EXPORT SHEET (landscape, fully expanded)
           ───────────────────────────────────────────── */
        #print-sheet {
            display: none;
        }

        #print-sheet.measuring {
            display: block;
            position: fixed;
            top: 0;
            left: -20000px;
            z-index: -1;
        }

        #print-inner {
            width: 1520px;
            transform-origin: top left;
            background: #ffffff;
            color: #12151a;
            font-family: 'DM Sans', sans-serif;
        }

        #print-inner .ps-head {
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            gap: 24px;
            border-bottom: 3px solid #0f172a;
            padding-bottom: 10px;
            margin-bottom: 16px;
        }

        #print-inner .ps-kicker {
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: #5b6472;
        }

        #print-inner .ps-title {
            font-size: 34px;
            line-height: 1.1;
            font-weight: 800;
            color: #0f172a;
        }

        #print-inner .ps-meta {
            font-size: 11px;
            line-height: 1.5;
            text-align: right;
            white-space: nowrap;
            color: #5b6472;
        }

        #print-inner .ps-grid {
            column-width: 300px;
            column-gap: 14px;
        }

        #print-inner .ps-card {
            display: inline-block;
            width: 100%;
            margin: 0 0 14px;
            border: 1.5px solid #d8dee7;
            border-top: 5px solid var(--c, #0969da);
            border-radius: 10px;
            padding: 11px 14px 14px;
            background: #ffffff;
            break-inside: avoid;
        }

        #print-inner .ps-card-head {
            display: flex;
            gap: 8px;
            align-items: baseline;
        }

        #print-inner .ps-num {
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.08em;
            color: var(--c, #0969da);
        }

        #print-inner .ps-branch {
            font-size: 15px;
            font-weight: 800;
            line-height: 1.25;
            color: #0f172a;
        }

        #print-inner .ps-branch-desc {
            font-size: 11px;
            line-height: 1.45;
            color: #4a5464;
            margin: 6px 0 9px;
        }

        #print-inner .ps-leaves {
            list-style: none;
            margin: 0;
            padding: 0 0 0 12px;
            border-left: 2px solid var(--c, #0969da);
            display: flex;
            flex-direction: column;
            gap: 7px;
        }

        #print-inner .ps-leaf {
            position: relative;
            font-size: 11.5px;
            line-height: 1.45;
            color: #1f2733;
        }

        #print-inner .ps-leaf::before {
            content: '';
            position: absolute;
            left: -12px;
            top: 7px;
            width: 8px;
            height: 2px;
            background: var(--c, #0969da);
        }

        #print-inner .ps-group > .ps-leaf-label {
            display: block;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 4px;
        }

        #print-inner .ps-sub {
            list-style: none;
            margin: 5px 0 0;
            padding: 0 0 0 11px;
            border-left: 1px dashed #cdd5e0;
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        #print-inner .ps-sub .ps-leaf {
            font-size: 10.5px;
            color: #4a5464;
        }

        #print-inner .ps-sub .ps-leaf::before {
            display: none;
        }

        #print-inner .ps-foot {
            display: flex;
            justify-content: space-between;
            margin-top: 16px;
            padding-top: 8px;
            border-top: 1px solid #d8dee7;
            font-size: 10px;
            letter-spacing: 0.04em;
            color: #69727f;
        }

        @media print {
            @page {
                size: A3 landscape;
                margin: 8mm;
            }

            html,
            body {
                height: auto !important;
                overflow: visible !important;
                background: #ffffff !important;
            }

            body > *:not(#print-sheet) {
                display: none !important;
            }

            #print-sheet {
                display: block !important;
                position: static !important;
                left: auto !important;
            }

            /* A transform does not shrink the layout box, so a scaled sheet
               would still paginate by its full size. Clamp it to one page. */
            #print-sheet.one-page {
                width: 1520px;
                height: 1050px;
                overflow: hidden;
            }

            #print-inner {
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }
        }
"""

EXPORT_JS = """        // ─────────────────────────────────────────────
        // EXPORT — LANDSCAPE PDF (every node expanded)
        // ─────────────────────────────────────────────
        const PRINT_PAGE_W = 1520;   // A3 landscape content box @96dpi
        const PRINT_PAGE_H = 1050;
        const PRINT_ACCENTS = ['#0969da', '#1a7f37', '#8250df', '#bc4c00', '#cf222e', '#0550ae'];

        function psEscape(text) {
            const d = document.createElement('div');
            d.textContent = text == null ? '' : String(text);
            return d.innerHTML;
        }

        function psDesc(html) {
            const d = document.createElement('div');
            d.innerHTML = html || '';
            const tag = d.querySelector('.panel-tag');
            if (tag) tag.remove();
            return d.textContent.replace(/\\s+/g, ' ').trim();
        }

        function psLeaves(nodes) {
            return (nodes || []).map(node => {
                const text = psDesc(node.desc) || node.label;
                if (node.children && node.children.length) {
                    // A grouping node (e.g. "Examples") keeps its own label as a
                    // heading so the nesting still reads on paper.
                    return `<li class="ps-leaf ps-group"><span class="ps-leaf-label">${psEscape(node.label)}</span>` +
                        `<ul class="ps-sub">${psLeaves(node.children)}</ul></li>`;
                }
                return `<li class="ps-leaf">${psEscape(text)}</li>`;
            }).join('');
        }

        function printKicker() {
            const parts = document.title.split('—').map(s => s.trim()).filter(Boolean);
            return parts.find(p => /[A-Z]{2,4}\\s?\\d{3}|chapter/i.test(p)) || parts[parts.length - 1] || '';
        }

        function buildPrintSheet() {
            const old = document.getElementById('print-sheet');
            if (old) old.remove();

            const cards = (DATA.children || []).map((branch, i) => {
                const color = PRINT_ACCENTS[i % PRINT_ACCENTS.length];
                const intro = psDesc(branch.desc);
                return `<section class="ps-card" style="--c:${color}">
                    <div class="ps-card-head">
                        <span class="ps-num">${String(i + 1).padStart(2, '0')}</span>
                        <h2 class="ps-branch">${psEscape(branch.label)}</h2>
                    </div>
                    ${intro ? `<p class="ps-branch-desc">${psEscape(intro)}</p>` : ''}
                    <ul class="ps-leaves">${psLeaves(branch.children)}</ul>
                </section>`;
            }).join('');

            const sheet = document.createElement('div');
            sheet.id = 'print-sheet';
            sheet.innerHTML = `<div id="print-inner">
                <header class="ps-head">
                    <div>
                        <div class="ps-kicker">${psEscape(printKicker())}</div>
                        <h1 class="ps-title">${psEscape(DATA.label)}</h1>
                    </div>
                    <div class="ps-meta">Full mindmap — all branches expanded</div>
                </header>
                <div class="ps-grid">${cards}</div>
                <div class="ps-foot"><span>Made by Shoug Alomran</span><span>shoug-tech.com</span></div>
            </div>`;
            document.body.appendChild(sheet);
            return sheet;
        }

        async function exportPDF() {
            expandAll();
            const sheet = buildPrintSheet();
            const inner = sheet.querySelector('#print-inner');

            // Measure off-screen, then binary-search the largest scale that still
            // fits one landscape page — sparse maps grow, dense ones shrink.
            sheet.classList.add('measuring');
            try { await document.fonts.ready; } catch (_e) { }
            await new Promise(r => requestAnimationFrame(r));

            const fits = s => {
                inner.style.transform = 'none';
                inner.style.width = (PRINT_PAGE_W / s) + 'px';
                return inner.scrollHeight <= PRINT_PAGE_H / s;
            };

            let lo = 0.45, hi = 1.75;
            if (!fits(lo)) hi = lo;                 // even the floor overflows: accept it
            else if (fits(hi)) lo = hi;
            else {
                for (let i = 0; i < 12; i++) {
                    const mid = (lo + hi) / 2;
                    if (fits(mid)) lo = mid; else hi = mid;
                }
            }
            const onePage = fits(lo);   // false only if even the floor overflows
            inner.style.width = (PRINT_PAGE_W / lo) + 'px';
            inner.style.transform = `scale(${lo})`;
            sheet.classList.toggle('one-page', onePage);
            sheet.classList.remove('measuring');

            window.addEventListener('afterprint', () => sheet.remove(), { once: true });
            window.print();
        }
"""

OLD_EXPORT_RE = re.compile(
    r"[ \t]*// ─+\n"
    r"[ \t]*// EXPORT PNG\n"
    r"[ \t]*// ─+\n"
    r"[ \t]*async function exportPNG\(\) \{.*?\n[ \t]*\}\n",
    re.S,
)


def patch_text(src: str) -> str | None:
    """Return the patched page, or None when it is not a patchable mindmap."""
    if 'id="print-sheet"' in src or "exportPDF()" in src:
        return None
    if not OLD_EXPORT_RE.search(src):
        return None

    src = OLD_EXPORT_RE.sub(lambda _m: EXPORT_JS, src, count=1)

    head, sep, tail = src.partition("    </style>")
    if not sep:
        return None
    src = head + PRINT_CSS + sep + tail

    src = src.replace('onclick="exportPNG()" title="Export PNG"',
                      'onclick="exportPDF()" title="Export PDF (landscape, fully expanded)"')
    src = re.sub(r"(\n\s+)Export\n(\s+</button>)", r"\1Export PDF\n\2", src, count=1)
    src = src.replace("details, and PNG export.", "details, and landscape PDF export.")
    src = src.replace("zoom, pan, or export the full map.", "zoom, pan, or export the full map as a PDF.")
    return src


def patch_file(path: Path) -> bool:
    out = patch_text(path.read_text())
    if out is None:
        return False
    path.write_text(out)
    print(f"patched: {path.relative_to(ROOT)}")
    return True


def main(argv: list[str]) -> None:
    targets = [Path(a) for a in argv[1:]] or DEFAULT_TARGETS
    seen: set[Path] = set()
    count = 0
    for target in targets:
        files = [target] if target.is_file() else sorted(target.rglob("*.html"))
        for f in files:
            if f in seen or f.name == "index.html":
                continue
            seen.add(f)
            count += patch_file(f)
    print(f"\n{count} page(s) patched")


if __name__ == "__main__":
    main(sys.argv)
