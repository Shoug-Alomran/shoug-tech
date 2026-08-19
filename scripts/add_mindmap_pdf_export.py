#!/usr/bin/env python3
"""Give SE322 (and other) mindmap pages a real landscape PDF export.

The old Export button just called window.print(), which printed the live
canvas: portrait, clipped, and only whatever branches happened to be open.
This replaces it with a purpose-built print sheet — every node expanded,
laid out horizontally as branch cards, scaled to fit one landscape page.
"""
import re
import sys
from pathlib import Path

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
            color: #5b6472;
            text-align: right;
            line-height: 1.5;
            white-space: nowrap;
        }

        #print-inner .ps-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 14px;
            align-items: start;
        }

        #print-inner .ps-card {
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

        #print-inner .ps-sub {
            list-style: none;
            margin: 5px 0 0;
            padding: 0 0 0 11px;
            border-left: 1px dashed #cdd5e0;
            display: flex;
            flex-direction: column;
            gap: 4px;
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

            #print-inner {
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }
        }
"""

EXPORT_JS = """        // ─────────────────────────────────────────────
        // EXPORT — LANDSCAPE PDF (every node expanded)
        // ─────────────────────────────────────────────
        const PRINT_PAGE_H = 1050;   // A3 landscape content height @96dpi
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
                const sub = node.children && node.children.length
                    ? `<ul class="ps-sub">${psLeaves(node.children)}</ul>`
                    : '';
                return `<li class="ps-leaf">${psEscape(text)}${sub}</li>`;
            }).join('');
        }

        function buildPrintSheet() {
            const old = document.getElementById('print-sheet');
            if (old) old.remove();

            const kicker = (document.title.split('—')[0] || '').trim();
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
                        <div class="ps-kicker">${psEscape(kicker)}</div>
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

            // Measure off-screen at full size, then scale down to one page.
            sheet.classList.add('measuring');
            inner.style.transform = 'none';
            try { await document.fonts.ready; } catch (_e) { }
            await new Promise(r => requestAnimationFrame(r));
            const scale = Math.min(1, PRINT_PAGE_H / inner.scrollHeight);
            inner.style.transform = scale < 1 ? `scale(${scale})` : 'none';
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


def patch(path: Path) -> bool:
    src = path.read_text()

    if "id=\"print-sheet\"" in src or "exportPDF()" in src:
        print(f"skip (already patched): {path}")
        return False

    if not OLD_EXPORT_RE.search(src):
        print(f"!! no exportPNG block: {path}")
        return False

    src = OLD_EXPORT_RE.sub(lambda _m: EXPORT_JS, src, count=1)

    # CSS goes just before the page's own </style>
    head, sep, tail = src.partition("    </style>")
    if not sep:
        print(f"!! no </style>: {path}")
        return False
    src = head + PRINT_CSS + sep + tail

    src = src.replace('onclick="exportPNG()" title="Export PNG"',
                      'onclick="exportPDF()" title="Export PDF (landscape, fully expanded)"')
    src = re.sub(r"(\n\s+)Export\n(\s+</button>)", r"\1Export PDF\n\2", src, count=1)

    # Keep the meta descriptions honest.
    src = src.replace("details, and PNG export.", "details, and landscape PDF export.")

    path.write_text(src)
    print(f"patched: {path}")
    return True


def main(argv):
    roots = [Path(a) for a in argv[1:]] or [
        Path("docs/academics/software-engineering/se322/extra-resources/mindmaps")
    ]
    count = 0
    for root in roots:
        for f in sorted(root.rglob("*.html")):
            if f.name == "index.html":
                continue
            count += patch(f)
    print(f"\n{count} file(s) patched")


if __name__ == "__main__":
    main(sys.argv)
