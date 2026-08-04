#!/usr/bin/env python3
"""Apply deliberate, per-page visual treatments to the SE311 exam collection."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/academics/software-engineering/se311/exams"


EXAMS = [
    ("01-chapter-1-quiz", "chapter-1-quiz.html", "#d946ef", "#22d3ee", "Requirements Foundations"),
    ("02-chapter-2-quiz", "chapter-2-quiz.html", "#6366f1", "#38bdf8", "Requirements Inception"),
    ("03-chapter-4-quiz", "chapter-4-quiz.html", "#fb7185", "#fbbf24", "Requirements Elicitation"),
    ("04-chapter-5-quiz", "chapter-5-quiz.html", "#06b6d4", "#34d399", "Requirements Analysis"),
    ("05-chapter-6-quiz", "chapter-6-quiz.html", "#22c55e", "#2dd4bf", "Requirements Validation"),
    ("06-chapter-8-quiz", "chapter-8-quiz.html", "#f59e0b", "#f472b6", "Requirements Specification"),
    ("07-chapter-9-quiz", "chapter-9-quiz.html", "#a855f7", "#60a5fa", "Nonfunctional Requirements"),
    ("08-quiz-1", "quiz-1.html", "#f43f5e", "#22d3ee", "Quiz 1 Review"),
]


def replace_marked_style(text: str, marker: str, css: str) -> str:
    pattern = rf"\s*<!-- {re.escape(marker)} -->\s*<style>.*?</style>"
    text = re.sub(pattern, "", text, flags=re.S)
    block = f"\n    <!-- {marker} -->\n    <style>\n{css}\n    </style>\n"
    if "</head>" not in text:
        raise RuntimeError(f"Missing </head> for {marker}")
    return text.replace("</head>", block + "</head>", 1)


def remove_marked_style(text: str, marker: str) -> str:
    pattern = rf"\s*<!-- {re.escape(marker)} -->\s*<style>.*?</style>"
    return re.sub(pattern, "", text, flags=re.S)


def tidy(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.splitlines()) + "\n"


def raw_exam_css(accent: str, accent2: str, order: int) -> str:
    chapter_override = ""
    if order == 1:
        chapter_override = """

        /* Chapter 1 has an older nested layout; normalize it explicitly. */
        html[data-theme="dark"] body,
        html[data-parent-theme="dark"] body {
            background-color: #070b16 !important;
            background-image:
                radial-gradient(circle at 10% 4%, rgba(217, 70, 239, .22), transparent 34rem),
                radial-gradient(circle at 92% 28%, rgba(34, 211, 238, .16), transparent 32rem),
                linear-gradient(145deg, #070b16 0%, #0b1324 52%, #091827 100%) !important;
        }

        .container {
            width: min(100% - clamp(18px, 3vw, 48px), 1480px) !important;
            max-width: 1480px !important;
            background: linear-gradient(145deg, #fbfbff, #f2f8ff) !important;
            border: 1px solid rgba(217, 70, 239, .22);
            box-shadow: 0 24px 70px rgba(0, 0, 0, .38), 0 0 42px rgba(217, 70, 239, .09);
        }

        .container > header {
            width: 100% !important;
            max-width: none !important;
            color: #25304a !important;
            background:
                radial-gradient(circle at 18% 30%, rgba(217, 70, 239, .16), transparent 26rem),
                radial-gradient(circle at 82% 55%, rgba(34, 211, 238, .14), transparent 24rem),
                linear-gradient(110deg, #fcf7ff, #f2f4ff 58%, #eefcff) !important;
        }

        .quiz-info {
            width: auto !important;
            max-width: none !important;
            margin: clamp(16px, 2.5vw, 34px) !important;
            padding: clamp(18px, 2.5vw, 30px) !important;
            color: #25304a !important;
            border: 1px solid rgba(34, 211, 238, .26) !important;
            border-left: 4px solid #d946ef !important;
            background: linear-gradient(110deg, rgba(217, 70, 239, .09), rgba(34, 211, 238, .1)) !important;
        }

        .quiz-info h3 { color: #a21caf !important; }

        .content {
            width: 100% !important;
            max-width: none !important;
            padding: clamp(18px, 3vw, 46px) !important;
            background: transparent !important;
        }

        .section-header {
            width: 100%;
            padding: clamp(16px, 2vw, 24px) !important;
            color: #202943 !important;
            border: 1px solid rgba(217, 70, 239, .25);
            border-left: 4px solid #22d3ee;
            background: linear-gradient(100deg, rgba(217, 70, 239, .16), rgba(34, 211, 238, .1)) !important;
            box-shadow: 0 12px 30px rgba(0, 0, 0, .16);
        }

        .question-block {
            width: 100% !important;
            max-width: none !important;
            padding: clamp(18px, 2.7vw, 34px) !important;
            background-color: #ffffff !important;
            background-image: linear-gradient(135deg, rgba(217, 70, 239, .1), transparent 42%, rgba(34, 211, 238, .07)) !important;
        }

        .question-number {
            background: linear-gradient(105deg, #d946ef, #8b5cf6) !important;
            box-shadow: 0 8px 24px rgba(217, 70, 239, .26);
        }

        .question-marks {
            background: linear-gradient(105deg, #0891b2, #22d3ee) !important;
            color: #06111b !important;
        }

        .question-text { color: #202943 !important; }
        .options { width: 100% !important; margin-left: 0 !important; }

        .option {
            width: 100% !important;
            color: #293550 !important;
            background: #f8faff !important;
            border-color: #ccd6e8 !important;
        }

        .option:hover {
            color: #172033 !important;
            border-color: #22d3ee !important;
            background: linear-gradient(90deg, rgba(217, 70, 239, .18), rgba(34, 211, 238, .12)) !important;
        }

        .answer-section {
            color: #164e63 !important;
            background: linear-gradient(110deg, rgba(34, 211, 238, .13), rgba(52, 211, 153, .1)) !important;
            border-left-color: #22d3ee !important;
        }

        html[data-theme="dark"] .container,
        html[data-parent-theme="dark"] .container {
            background: linear-gradient(145deg, rgba(15, 22, 40, .98), rgba(9, 19, 34, .98)) !important;
        }

        html[data-theme="dark"] .container > header,
        html[data-parent-theme="dark"] .container > header {
            color: #fff !important;
            background:
                radial-gradient(circle at 18% 30%, rgba(217, 70, 239, .28), transparent 26rem),
                linear-gradient(110deg, #16142d, #111e34 58%, #0d2b38) !important;
        }

        html[data-theme="dark"] .quiz-info,
        html[data-parent-theme="dark"] .quiz-info {
            color: #edf3ff !important;
            background: linear-gradient(110deg, rgba(217, 70, 239, .15), rgba(34, 211, 238, .11)) !important;
        }

        html[data-theme="dark"] .quiz-info h3,
        html[data-parent-theme="dark"] .quiz-info h3 { color: #f0a4ff !important; }

        html[data-theme="dark"] .section-header,
        html[data-parent-theme="dark"] .section-header { color: #f8fbff !important; }

        html[data-theme="dark"] .question-block,
        html[data-parent-theme="dark"] .question-block {
            background-color: #111a2c !important;
        }

        html[data-theme="dark"] .question-text,
        html[data-parent-theme="dark"] .question-text { color: #f3f6ff !important; }

        html[data-theme="dark"] .option,
        html[data-parent-theme="dark"] .option {
            color: #e8eefb !important;
            background: rgba(7, 13, 27, .72) !important;
            border-color: #344667 !important;
        }

        html[data-theme="dark"] .option:hover,
        html[data-parent-theme="dark"] .option:hover { color: #fff !important; }

        html[data-theme="dark"] .answer-section,
        html[data-parent-theme="dark"] .answer-section { color: #dffcff !important; }

        @media (max-width: 768px) {
            .container { width: calc(100% - 12px) !important; }
            .quiz-info { margin: 10px !important; }
            .content { padding: 12px !important; }
            .question-header { align-items: flex-start; gap: 10px; }
            .question-number, .question-marks { padding: 6px 10px; }
        }
        """

    return f"""
        :root {{
            --se311-accent: {accent};
            --se311-accent-2: {accent2};
            --se311-glow: color-mix(in srgb, var(--se311-accent) 22%, transparent);
        }}

        html {{ scroll-behavior: smooth; }}

        body {{
            min-height: 100vh;
            background-image:
                radial-gradient(circle at {10 + order * 8}% 6%, color-mix(in srgb, var(--se311-accent) 17%, transparent), transparent 34rem),
                radial-gradient(circle at {92 - order * 6}% 36%, color-mix(in srgb, var(--se311-accent-2) 13%, transparent), transparent 32rem),
                linear-gradient(180deg, rgba(8, 7, 20, .035), transparent 48%);
            background-attachment: fixed;
        }}

        /* Theme-debugged header contract: never derive a background from a text variable. */
        html[data-theme="light"] :where(body > header, .container > header, .quiz-container > header, .topbar) {{
            color: #20283c !important;
            border-color: color-mix(in srgb, var(--se311-accent) 24%, #d9deea) !important;
            background:
                radial-gradient(circle at 14% 30%, color-mix(in srgb, var(--se311-accent) 15%, transparent), transparent 24rem),
                radial-gradient(circle at 86% 55%, color-mix(in srgb, var(--se311-accent-2) 12%, transparent), transparent 22rem),
                linear-gradient(110deg, #fdfbff, #f3f5ff 58%, #effcff) !important;
        }}

        html[data-theme="dark"] :where(body > header, .container > header, .quiz-container > header, .topbar) {{
            color: #f5f7ff !important;
            border-color: color-mix(in srgb, var(--se311-accent) 32%, #27334a) !important;
            background:
                radial-gradient(circle at 14% 30%, color-mix(in srgb, var(--se311-accent) 24%, transparent), transparent 25rem),
                radial-gradient(circle at 86% 55%, color-mix(in srgb, var(--se311-accent-2) 15%, transparent), transparent 23rem),
                linear-gradient(110deg, #121326, #101a2d 58%, #0b2632) !important;
        }}

        html[data-theme="light"] :where(body > header, .container > header, .quiz-container > header, .topbar)
            :where(p, .title, .subtitle, .header-text, .topbar-left, .mode-label) {{
            color: #38445e !important;
        }}

        html[data-theme="dark"] :where(body > header, .container > header, .quiz-container > header, .topbar)
            :where(p, .title, .subtitle, .header-text, .topbar-left, .mode-label) {{
            color: #dbe5f6 !important;
        }}

        html[data-theme="light"] :where(.toggle-btn, .mode-toggle, .theme-toggle) {{
            color: #27324a !important;
            background: rgba(255, 255, 255, .72) !important;
            border-color: color-mix(in srgb, var(--se311-accent) 28%, #cad2e2) !important;
        }}

        html[data-theme="dark"] :where(.toggle-btn, .mode-toggle, .theme-toggle) {{
            color: #f5f7ff !important;
            background: rgba(8, 13, 28, .58) !important;
            border-color: color-mix(in srgb, var(--se311-accent-2) 30%, #3b465c) !important;
        }}

        :where(.quiz-container, .container, .quiz-content, .quiz-wrap, .hero, main) {{
            width: min(100% - clamp(24px, 5vw, 80px), 1320px) !important;
            max-width: 1320px !important;
            margin-inline: auto !important;
        }}

        :where(.quiz-container, .quiz-content, .quiz-wrap, main) > :where(h1, header, .quiz-header):first-child,
        :where(header, .hero, .topbar) {{
            animation: se311-hero-in .66s cubic-bezier(.2, .8, .2, 1) both;
        }}

        :where(h1, .quiz-title, header h1, .hero h2, .topbar h1) {{
            background: linear-gradient(105deg, var(--se311-accent), var(--se311-accent-2));
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent !important;
            text-shadow: 0 0 34px var(--se311-glow);
        }}

        :where(.quiz-info, .info-box, .instructions, .exam-info) {{
            position: relative;
            overflow: hidden;
            border-color: color-mix(in srgb, var(--se311-accent) 48%, transparent) !important;
            background-image: linear-gradient(120deg,
                color-mix(in srgb, var(--se311-accent) 13%, transparent),
                color-mix(in srgb, var(--se311-accent-2) 9%, transparent)) !important;
            box-shadow: 0 14px 38px rgba(5, 4, 18, .16);
        }}

        :where(.question, .question-block, .question-card, .q-card) {{
            position: relative;
            overflow: hidden;
            border-color: color-mix(in srgb, var(--se311-accent) 32%, transparent) !important;
            background-image: linear-gradient(135deg,
                color-mix(in srgb, var(--se311-accent) 8%, transparent),
                transparent 42%,
                color-mix(in srgb, var(--se311-accent-2) 6%, transparent)) !important;
            box-shadow: 0 12px 34px rgba(5, 4, 18, .14);
            animation: se311-card-in .54s cubic-bezier(.2, .8, .2, 1) both;
            transition: transform .23s ease, border-color .23s ease, box-shadow .23s ease;
        }}

        :where(.question, .question-block, .question-card, .q-card)::before {{
            content: '';
            position: absolute;
            inset: 0 auto 0 0;
            width: 3px;
            background: linear-gradient(180deg, var(--se311-accent), var(--se311-accent-2));
        }}

        :where(.question, .question-block, .question-card, .q-card):hover {{
            transform: translateY(-3px);
            border-color: var(--se311-accent) !important;
            box-shadow: 0 18px 46px rgba(5, 4, 18, .21), 0 0 28px var(--se311-glow);
        }}

        :where(.option, .answer-option, label.option, .true-false-option, .opt, .tf-btn) {{
            transition: transform .18s ease, border-color .18s ease, background .18s ease, box-shadow .18s ease !important;
        }}

        :where(.option, .answer-option, label.option, .true-false-option, .opt, .tf-btn):hover {{
            transform: translateX(5px);
            border-color: var(--se311-accent) !important;
            background-image: linear-gradient(90deg,
                color-mix(in srgb, var(--se311-accent) 14%, transparent),
                color-mix(in srgb, var(--se311-accent-2) 8%, transparent)) !important;
            box-shadow: 0 8px 24px var(--se311-glow);
        }}

        :where(input[type="radio"], input[type="checkbox"]) {{ accent-color: var(--se311-accent); }}

        :where(.toggle-answer-btn, .submit-btn, .submit-all-btn, .check-btn, .restart-btn,
            .retry-btn, .nav-btn, button[type="submit"]) {{
            border: 0 !important;
            color: #fff !important;
            background: linear-gradient(105deg, var(--se311-accent), var(--se311-accent-2)) !important;
            box-shadow: 0 10px 28px var(--se311-glow);
            transition: transform .2s ease, box-shadow .2s ease, filter .2s ease !important;
        }}

        :where(.toggle-answer-btn, .submit-btn, .submit-all-btn, .check-btn, .restart-btn,
            .retry-btn, .nav-btn, button[type="submit"]):hover {{
            transform: translateY(-2px) scale(1.015);
            box-shadow: 0 15px 38px var(--se311-glow);
            filter: saturate(1.15) brightness(1.05);
        }}

        :where(.answer, .answer-key, .feedback, .explanation, .mock-answer, .model-answer,
            .result-panel, .results-panel) {{
            border-color: color-mix(in srgb, var(--se311-accent-2) 55%, transparent) !important;
            background-image: linear-gradient(110deg,
                color-mix(in srgb, var(--se311-accent-2) 11%, transparent), transparent) !important;
        }}

        @keyframes se311-hero-in {{
            from {{ opacity: 0; transform: translateY(-12px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        @keyframes se311-card-in {{
            from {{ opacity: 0; transform: translateY(16px) scale(.992); }}
            to {{ opacity: 1; transform: translateY(0) scale(1); }}
        }}

        @media (max-width: 768px) {{
            :where(.quiz-container, .container, .quiz-content, .quiz-wrap, .hero, main) {{
                width: min(100% - 20px, 1320px) !important;
            }}
            :where(.question, .question-block, .question-card, .q-card):hover,
            :where(.option, .answer-option, label.option, .true-false-option, .opt, .tf-btn):hover {{
                transform: none;
            }}
        }}

        @media (prefers-reduced-motion: reduce) {{
            :where(.quiz-container, .quiz-content, .quiz-wrap, main, .question, .question-block, .question-card, .q-card) {{
                animation: none !important;
            }}
            :where(.question, .question-block, .question-card, .q-card, .option, .answer-option,
                .opt, .tf-btn, .toggle-answer-btn, .submit-btn, .submit-all-btn, .check-btn,
                .restart-btn, .retry-btn, .nav-btn):hover {{ transform: none !important; }}
        }}
        {chapter_override}
"""


def wrapper_css(accent: str, accent2: str) -> str:
    return f"""
        :root {{ --se311-accent: {accent}; --se311-accent-2: {accent2}; }}

        .page-header {{
            position: relative;
            overflow: hidden;
            background-image:
                radial-gradient(circle at 12% 20%, color-mix(in srgb, var(--se311-accent) 18%, transparent), transparent 28rem),
                radial-gradient(circle at 88% 65%, color-mix(in srgb, var(--se311-accent-2) 12%, transparent), transparent 26rem);
            animation: se311-wrapper-in .58s cubic-bezier(.2, .8, .2, 1) both;
        }}

        .ch-title {{
            background: linear-gradient(105deg, var(--se311-accent), var(--se311-accent-2));
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent !important;
        }}

        .btn-primary {{
            color: #fff !important;
            background: linear-gradient(105deg, var(--se311-accent), var(--se311-accent-2)) !important;
            box-shadow: 0 10px 28px color-mix(in srgb, var(--se311-accent) 25%, transparent);
            transition: transform .2s ease, box-shadow .2s ease;
        }}

        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 15px 38px color-mix(in srgb, var(--se311-accent) 35%, transparent);
        }}

        .embed-container {{
            border-color: color-mix(in srgb, var(--se311-accent) 52%, var(--border-hard)) !important;
            box-shadow: 0 18px 50px rgba(4, 3, 14, .24), 0 0 32px color-mix(in srgb, var(--se311-accent) 14%, transparent);
            animation: se311-wrapper-in .65s .08s cubic-bezier(.2, .8, .2, 1) both;
        }}

        @keyframes se311-wrapper-in {{
            from {{ opacity: 0; transform: translateY(12px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        @media (prefers-reduced-motion: reduce) {{
            .page-header, .embed-container {{ animation: none !important; }}
            .btn-primary:hover {{ transform: none !important; }}
        }}
"""


def hub_css() -> str:
    return """
        .content-header {
            position: relative;
            overflow: hidden;
            background-image:
                radial-gradient(circle at 12% 24%, rgba(217, 70, 239, .2), transparent 30rem),
                radial-gradient(circle at 88% 65%, rgba(34, 211, 238, .13), transparent 28rem);
            animation: se311-hub-in .6s cubic-bezier(.2, .8, .2, 1) both;
        }

        .course-code {
            background: linear-gradient(105deg, #d946ef, #8b5cf6 55%, #22d3ee);
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent !important;
        }

        .se311-exam-intro {
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 24px;
            align-items: center;
            padding: clamp(22px, 4vw, 44px);
            border-bottom: 1px solid var(--border-hard);
            background:
                linear-gradient(115deg, rgba(217, 70, 239, .12), transparent 48%, rgba(34, 211, 238, .08));
        }

        .se311-exam-intro h2 { margin: 0 0 8px; font-size: clamp(1.35rem, 3vw, 2.25rem); }
        .se311-exam-intro p { margin: 0; color: var(--text-secondary); max-width: 70ch; line-height: 1.7; }
        .se311-exam-count {
            min-width: 106px;
            padding: 14px 18px;
            border: 1px solid rgba(217, 70, 239, .55);
            background: rgba(217, 70, 239, .1);
            color: #ee8cff;
            font-family: var(--font-mono);
            text-align: center;
            box-shadow: 0 0 28px rgba(217, 70, 239, .14);
        }

        .dir-row {
            position: relative;
            isolation: isolate;
            animation: se311-row-in .5s cubic-bezier(.2, .8, .2, 1) both;
            transition: transform .22s ease, border-color .22s ease, box-shadow .22s ease !important;
        }

        .dir-row::before {
            content: '';
            position: absolute;
            inset: 0;
            z-index: -1;
            opacity: 0;
            background: linear-gradient(100deg, rgba(217, 70, 239, .2), rgba(99, 102, 241, .1) 55%, rgba(34, 211, 238, .14));
            transition: opacity .22s ease;
        }

        .dir-row:hover {
            transform: translateX(8px);
            border-color: rgba(217, 70, 239, .58) !important;
            box-shadow: -4px 0 #d946ef, 0 14px 36px rgba(4, 3, 14, .25);
        }
        .dir-row:hover::before { opacity: 1; }
        .dir-row:hover .dir-title { color: #ee8cff !important; text-shadow: 0 0 18px rgba(217, 70, 239, .3); }
        .dir-row:hover .dir-num { color: #22d3ee; }

        .dir-row:nth-of-type(2) { animation-delay: .04s; }
        .dir-row:nth-of-type(3) { animation-delay: .08s; }
        .dir-row:nth-of-type(4) { animation-delay: .12s; }
        .dir-row:nth-of-type(5) { animation-delay: .16s; }
        .dir-row:nth-of-type(6) { animation-delay: .20s; }
        .dir-row:nth-of-type(7) { animation-delay: .24s; }
        .dir-row:nth-of-type(8) { animation-delay: .28s; }
        .dir-row:nth-of-type(9) { animation-delay: .32s; }

        @keyframes se311-hub-in {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes se311-row-in {
            from { opacity: 0; transform: translateY(12px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @media (max-width: 680px) {
            .se311-exam-intro { grid-template-columns: 1fr; }
            .se311-exam-count { justify-self: start; }
            .dir-row:hover { transform: none; }
        }
        @media (prefers-reduced-motion: reduce) {
            .content-header, .dir-row { animation: none !important; }
            .dir-row:hover { transform: none !important; }
        }
"""


def enhance_hub() -> None:
    path = BASE / "index.html"
    text = path.read_text()
    text = re.sub(r'\s*<!-- SE311 EXAM INTRO -->.*?<!-- /SE311 EXAM INTRO -->\s*', "\n", text, flags=re.S)
    intro = """
            <!-- SE311 EXAM INTRO -->
            <section class="se311-exam-intro" aria-label="SE311 exam collection">
                <div>
                    <h2>Requirements Engineering Exam Lab</h2>
                    <p>Eight focused practice sets covering foundations, inception, elicitation, analysis, validation, specification, and nonfunctional requirements.</p>
                </div>
                <div class="se311-exam-count"><strong>8</strong><br>EXAMS</div>
            </section>
            <!-- /SE311 EXAM INTRO -->
"""
    text = text.replace('<div class="directory-container">', intro + '\n            <div class="directory-container">', 1)
    path.write_text(tidy(replace_marked_style(text, "SE311 EXAM HUB ENHANCEMENT", hub_css())))


def main() -> None:
    # The SHOUG.TECH hub and viewer wrappers are intentionally kept unchanged.
    hub = BASE / "index.html"
    hub_text = remove_marked_style(hub.read_text(), "SE311 EXAM HUB ENHANCEMENT")
    hub_text = re.sub(r'\s*<!-- SE311 EXAM INTRO -->.*?<!-- /SE311 EXAM INTRO -->\s*', "\n", hub_text, flags=re.S)
    hub.write_text(tidy(hub_text))

    for order, (folder, raw_name, accent, accent2, _topic) in enumerate(EXAMS, start=1):
        wrapper = BASE / folder / "index.html"
        raw = BASE / raw_name
        wrapper.write_text(tidy(remove_marked_style(wrapper.read_text(), "SE311 EXAM WRAPPER ENHANCEMENT")))
        raw_text = raw.read_text()
        # One theme authority only. html-theme-sync handles parent state, storage,
        # system preference, button labels, and iframe height synchronization.
        raw_text = re.sub(r'\s*<script src="/javascripts/standalone-theme\.js"></script>\s*', "\n", raw_text)
        raw.write_text(tidy(replace_marked_style(raw_text, "SE311 INTERACTIVE EXAM ENHANCEMENT", raw_exam_css(accent, accent2, order))))
    print("Restored SE311 website shell; enhanced only 8 embedded interactive exams")


if __name__ == "__main__":
    main()
