(function () {
  "use strict";

  var DARK = "dark";
  var LIGHT = "light";
  var lastMode = null;
  var _settingTheme = false;
  var searchState = {
    query: "",
    marks: [],
    active: -1
  };

  function normalizeScheme(value) {
    if (!value) return null;
    value = String(value).toLowerCase();
    if (value === "slate" || value === DARK) return DARK;
    if (value === "default" || value === LIGHT) return LIGHT;
    return null;
  }

  function modeFromPalette() {
    try {
      var shougTheme = localStorage.getItem("shoug-theme");
      if (shougTheme === "light") return LIGHT;
      if (shougTheme === "dark") return DARK;
      var raw = localStorage.getItem("__palette");
      if (!raw) return null;
      var palette = JSON.parse(raw);
      return normalizeScheme(palette && palette.color && palette.color.scheme);
    } catch (e) {
      return null;
    }
  }

  function modeFromParent() {
    try {
      if (window.parent === window || !window.parent.document) return null;
      var parentBody = window.parent.document.body;
      var parentRoot = window.parent.document.documentElement;
      if (parentBody && parentBody.classList.contains("shoug-light-mode")) return LIGHT;
      return normalizeScheme(
        (parentBody && parentBody.getAttribute("data-md-color-scheme")) ||
        (parentRoot && parentRoot.getAttribute("data-md-color-scheme"))
      );
    } catch (e) {
      return null;
    }
  }

  function preferredMode() {
    return (
      modeFromParent() ||
      modeFromPalette() ||
      (window.matchMedia &&
        window.matchMedia("(prefers-color-scheme: dark)").matches
        ? DARK
        : LIGHT)
    );
  }

  function setButtonState(mode) {
    var icon = document.getElementById("themeIcon");
    if (icon) icon.textContent = mode === DARK ? "☀️" : "🌙";

    var labels = document.querySelectorAll("[data-theme-label]");
    labels.forEach(function (label) {
      label.textContent = mode === DARK ? "Light" : "Dark";
    });
  }

  function hasSelfTheme() {
    return document.documentElement.hasAttribute('data-sg-styled');
  }

  function ensureContrastStyle() {
    if (hasSelfTheme()) return;
    if (document.getElementById("html-theme-contrast-style")) return;

    var style = document.createElement("style");
    style.id = "html-theme-contrast-style";
    style.textContent = `
      html[data-theme="dark"] {
        color-scheme: dark;
        --bg: #0b1020 !important;
        --bg2: #111827 !important;
        --bg3: #1f2937 !important;
        --background: #0b1020 !important;
        --card-bg: #111827 !important;
        --card: #111827 !important;
        --surface: #111827 !important;
        --white: #111827 !important;
        --light-bg: #1f2937 !important;
        --text: #e5e7eb !important;
        --text-color: #e5e7eb !important;
        --text-dark: #e5e7eb !important;
        --muted: #cbd5e1 !important;
        --primary-color: #93c5fd !important;
        --primary: #93c5fd !important;
        --primary-dark: #bfdbfe !important;
        --secondary-color: #c4b5fd !important;
        --secondary: #c4b5fd !important;
        --accent-color: #fbbf24 !important;
        --accent: #fbbf24 !important;
        --border: #374151 !important;
        --border-color: #4b5563 !important;
      }

      html[data-theme="light"] {
        color-scheme: light;
        --bg: #f8f9fa !important;
        --bg2: #ffffff !important;
        --bg3: #f0f2f5 !important;
        --background: #f8f9fa !important;
        --bg-void: #f8f9fa !important;
        --bg-surface: #ffffff !important;
        --bg-elevated: #f0f2f5 !important;
        --card-bg: #ffffff !important;
        --card: #ffffff !important;
        --surface: #ffffff !important;
        --white: #ffffff !important;
        --light-bg: #f0f2f5 !important;
        --text: #1e2433 !important;
        --text-color: #1e2433 !important;
        --text-dark: #1e2433 !important;
        --text-main: #1e2433 !important;
        --muted: #6b7280 !important;
        --ink: #1e2433 !important;
        --ink-1: #1e2433 !important;
        --ink-2: #4b5568 !important;
        --border: rgba(0,0,0,0.1) !important;
        --border-color: rgba(0,0,0,0.15) !important;
        --border-dim: rgba(0,0,0,0.1) !important;
        --border-med: rgba(0,0,0,0.2) !important;
      }

      html[data-theme="light"] body {
        background: #f8f9fa !important;
        color: #1e2433 !important;
      }

      html[data-theme="dark"] body {
        background: #0b1020 !important;
        color: #e5e7eb !important;
      }

      html[data-theme="dark"] body > *:not(script):not(style):not(.sg-theme-toggle) {
        color: #e5e7eb;
      }

      html[data-theme="dark"] main,
      html[data-theme="dark"] section,
      html[data-theme="dark"] article,
      html[data-theme="dark"] aside,
      html[data-theme="dark"] footer,
      html[data-theme="dark"] .container,
      html[data-theme="dark"] .content,
      html[data-theme="dark"] .wrapper,
      html[data-theme="dark"] .page,
      html[data-theme="dark"] .chapter,
      html[data-theme="dark"] .section,
      html[data-theme="dark"] .card,
      html[data-theme="dark"] .box,
      html[data-theme="dark"] .panel,
      html[data-theme="dark"] .tile,
      html[data-theme="dark"] .item,
      html[data-theme="dark"] .topic,
      html[data-theme="dark"] .note,
      html[data-theme="dark"] .tip,
      html[data-theme="dark"] .info,
      html[data-theme="dark"] .warning,
      html[data-theme="dark"] .highlight,
      html[data-theme="dark"] .summary,
      html[data-theme="dark"] .definition,
      html[data-theme="dark"] .example,
      html[data-theme="dark"] .objective,
      html[data-theme="dark"] .learning-objectives,
      html[data-theme="dark"] .toc,
      html[data-theme="dark"] .table-container,
      html[data-theme="dark"] .diagram-container,
      html[data-theme="dark"] .quiz-container,
      html[data-theme="dark"] .question,
      html[data-theme="dark"] .answer,
      html[data-theme="dark"] [class*="card"],
      html[data-theme="dark"] [class*="box"],
      html[data-theme="dark"] [class*="panel"],
      html[data-theme="dark"] [class*="section"],
      html[data-theme="dark"] [class*="container"],
      html[data-theme="dark"] [class*="wrapper"],
      html[data-theme="dark"] [class*="content"],
      html[data-theme="dark"] [class*="objective"],
      html[data-theme="dark"] [class*="toc"],
      html[data-theme="dark"] [class*="table"],
      html[data-theme="dark"] [class*="diagram"],
      html[data-theme="dark"] [style*="background: white"],
      html[data-theme="dark"] [style*="background:white"],
      html[data-theme="dark"] [style*="background: #fff"],
      html[data-theme="dark"] [style*="background:#fff"],
      html[data-theme="dark"] [style*="background: #ffffff"],
      html[data-theme="dark"] [style*="background:#ffffff"],
      html[data-theme="dark"] [style*="background-color: white"],
      html[data-theme="dark"] [style*="background-color:white"],
      html[data-theme="dark"] [style*="background-color: #fff"],
      html[data-theme="dark"] [style*="background-color:#fff"],
      html[data-theme="dark"] [style*="background-color: #ffffff"],
      html[data-theme="dark"] [style*="background-color:#ffffff"],
      html[data-theme="dark"] [style*="background: #fee"],
      html[data-theme="dark"] [style*="background:#fee"],
      html[data-theme="dark"] [style*="background: #fef"],
      html[data-theme="dark"] [style*="background:#fef"],
      html[data-theme="dark"] [style*="background: #ffe"],
      html[data-theme="dark"] [style*="background:#ffe"],
      html[data-theme="dark"] [style*="background: #ffd"],
      html[data-theme="dark"] [style*="background:#ffd"],
      html[data-theme="dark"] [style*="background: #ffc"],
      html[data-theme="dark"] [style*="background:#ffc"],
      html[data-theme="dark"] [style*="background: #ffb"],
      html[data-theme="dark"] [style*="background:#ffb"],
      html[data-theme="dark"] [style*="background: #fff0"],
      html[data-theme="dark"] [style*="background:#fff0"],
      html[data-theme="dark"] [style*="background: #fff3"],
      html[data-theme="dark"] [style*="background:#fff3"],
      html[data-theme="dark"] [style*="background: #fff8"],
      html[data-theme="dark"] [style*="background:#fff8"],
      html[data-theme="dark"] [style*="background: #fff9"],
      html[data-theme="dark"] [style*="background:#fff9"],
      html[data-theme="dark"] [style*="background: #fffb"],
      html[data-theme="dark"] [style*="background:#fffb"],
      html[data-theme="dark"] [style*="background: #fffc"],
      html[data-theme="dark"] [style*="background:#fffc"],
      html[data-theme="dark"] [style*="background: #fffe"],
      html[data-theme="dark"] [style*="background:#fffe"],
      html[data-theme="dark"] [style*="background: #f0f"],
      html[data-theme="dark"] [style*="background:#f0f"],
      html[data-theme="dark"] [style*="background: #f5f"],
      html[data-theme="dark"] [style*="background:#f5f"],
      html[data-theme="dark"] [style*="background: #f8f"],
      html[data-theme="dark"] [style*="background:#f8f"],
      html[data-theme="dark"] [style*="background: #faf"],
      html[data-theme="dark"] [style*="background:#faf"],
      html[data-theme="dark"] [style*="linear-gradient"] {
        background: #1f2937 !important;
        color: #e5e7eb !important;
        border-color: #374151 !important;
      }

      html[data-theme="dark"] .important,
      html[data-theme="dark"] .important-note,
      html[data-theme="dark"] .caution,
      html[data-theme="dark"] .caution-box,
      html[data-theme="dark"] .notice,
      html[data-theme="dark"] .notice-box,
      html[data-theme="dark"] .note-box,
      html[data-theme="dark"] .alert-box,
      html[data-theme="dark"] .info-panel,
      html[data-theme="dark"] .hint,
      html[data-theme="dark"] .quote,
      html[data-theme="dark"] .quote-block,
      html[data-theme="dark"] .blockquote,
      html[data-theme="dark"] .step,
      html[data-theme="dark"] .steps,
      html[data-theme="dark"] .step-item,
      html[data-theme="dark"] .numbered-step,
      html[data-theme="dark"] .process-step,
      html[data-theme="dark"] .lifecycle-phase,
      html[data-theme="dark"] .figure,
      html[data-theme="dark"] .visual,
      html[data-theme="dark"] .visual-rep,
      html[data-theme="dark"] .visual-diagram,
      html[data-theme="dark"] .accordion-item,
      html[data-theme="dark"] .accordion-content,
      html[data-theme="dark"] .premises,
      html[data-theme="dark"] .conclusion,
      html[data-theme="dark"] .comparison-side,
      html[data-theme="dark"] .comparison-item,
      html[data-theme="dark"] .matrix,
      html[data-theme="dark"] .data-table,
      html[data-theme="dark"] .qCard,
      html[data-theme="dark"] .score-summary,
      html[data-theme="dark"] .your-answer,
      html[data-theme="dark"] .user-story,
      html[data-theme="dark"] .model-answer,
      html[data-theme="dark"] .rotation-card,
      html[data-theme="dark"] .scenario-section,
      html[data-theme="dark"] .rendered-content,
      html[data-theme="dark"] .svg-diagram,
      html[data-theme="dark"] .flowchart,
      html[data-theme="dark"] .proof-step {
        background: #1f2937 !important;
        color: #e5e7eb !important;
        border-color: #4b5563 !important;
      }

      .sg-theme-toggle {
        position: fixed;
        z-index: 9999;
        bottom: max(0.85rem, env(safe-area-inset-bottom));
        left: max(0.85rem, env(safe-area-inset-left));
        width: 2.6rem;
        height: 2.6rem;
        border-radius: 50%;
        border: 1px solid rgba(148, 163, 184, 0.35);
        background: rgba(15, 23, 42, 0.88);
        color: #f8fafc;
        font-size: 1.15rem;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.28);
        backdrop-filter: blur(10px);
        padding: 0;
        transition: transform 0.12s ease, box-shadow 0.12s ease;
      }

      .sg-theme-toggle:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.35);
      }

      html[data-theme="dark"] .page-hero-cover,
      html[data-theme="dark"] .course-cover {
        background: linear-gradient(135deg, #312e81 0%, #581c87 100%) !important;
        color: #ffffff !important;
      }

      html[data-theme="dark"] h1,
      html[data-theme="dark"] h2,
      html[data-theme="dark"] h3,
      html[data-theme="dark"] h4,
      html[data-theme="dark"] h5,
      html[data-theme="dark"] h6,
      html[data-theme="dark"] p,
      html[data-theme="dark"] li,
      html[data-theme="dark"] span,
      html[data-theme="dark"] label,
      html[data-theme="dark"] dt,
      html[data-theme="dark"] dd,
      html[data-theme="dark"] td,
      html[data-theme="dark"] th,
      html[data-theme="dark"] small,
      html[data-theme="dark"] div {
        color: inherit;
      }

      html[data-theme="dark"] h1,
      html[data-theme="dark"] h2,
      html[data-theme="dark"] h3,
      html[data-theme="dark"] h4,
      html[data-theme="dark"] h5,
      html[data-theme="dark"] h6,
      html[data-theme="dark"] p,
      html[data-theme="dark"] li,
      html[data-theme="dark"] label,
      html[data-theme="dark"] dt,
      html[data-theme="dark"] dd,
      html[data-theme="dark"] td,
      html[data-theme="dark"] th {
        color: #e5e7eb !important;
      }

      html[data-theme="dark"] a {
        color: #c4b5fd !important;
      }

      html[data-theme="dark"] strong,
      html[data-theme="dark"] b {
        color: #f8fafc !important;
      }

      html[data-theme="dark"] table {
        background: #0f172a !important;
        color: #e5e7eb !important;
        border-color: #374151 !important;
      }

      html[data-theme="dark"] th {
        background: #1f2937 !important;
        color: #f8fafc !important;
      }

      html[data-theme="dark"] td {
        background: #111827 !important;
        color: #e5e7eb !important;
        border-color: #374151 !important;
      }

      html[data-theme="dark"] .question,
      html[data-theme="dark"] .question-card,
      html[data-theme="dark"] .question-block,
      html[data-theme="dark"] .topic-card,
      html[data-theme="dark"] .exam-question,
      html[data-theme="dark"] .solution-card,
      html[data-theme="dark"] .result-box,
      html[data-theme="dark"] .feedback,
      html[data-theme="dark"] .mock-answer,
      html[data-theme="dark"] .answer-box,
      html[data-theme="dark"] .learning-outcomes,
      html[data-theme="dark"] .highlight,
      html[data-theme="dark"] .key-point,
      html[data-theme="dark"] .warning,
      html[data-theme="dark"] .principle,
      html[data-theme="dark"] .timeline-item,
      html[data-theme="dark"] .stat-card,
      html[data-theme="dark"] .metric-card,
      html[data-theme="dark"] .summary-card,
      html[data-theme="dark"] .concept-box,
      html[data-theme="dark"] .example-box,
      html[data-theme="dark"] .exam-section,
      html[data-theme="dark"] .key-concept,
      html[data-theme="dark"] .tip,
      html[data-theme="dark"] .exam-example,
      html[data-theme="dark"] .option,
      html[data-theme="dark"] .tf-option,
      html[data-theme="dark"] .mcq-option,
      html[data-theme="dark"] .mcq-options li,
      html[data-theme="dark"] .practice-list li,
      html[data-theme="dark"] .requirements-list li,
      html[data-theme="dark"] .key-points li,
      html[data-theme="dark"] [class*="-card"],
      html[data-theme="dark"] [class*="-box"],
      html[data-theme="dark"] [class*="-panel"],
      html[data-theme="dark"] [class*="-item"],
      html[data-theme="dark"] [class*="-option"] {
        background: #1f2937 !important;
        color: #e5e7eb !important;
        border-color: #4b5563 !important;
      }

      html[data-theme="dark"] tr:nth-child(even) td,
      html[data-theme="dark"] tr:nth-child(even) th {
        background: #172033 !important;
      }

      html[data-theme="dark"] pre,
      html[data-theme="dark"] code,
      html[data-theme="dark"] .code,
      html[data-theme="dark"] .formula {
        background: #0f172a !important;
        color: #e5e7eb !important;
        border-color: #374151 !important;
      }

      html[data-theme="dark"] .card:hover,
      html[data-theme="dark"] .question:hover,
      html[data-theme="dark"] .question-card:hover,
      html[data-theme="dark"] .question-block:hover,
      html[data-theme="dark"] .option:hover,
      html[data-theme="dark"] .tf-option:hover,
      html[data-theme="dark"] .mcq-option:hover,
      html[data-theme="dark"] .mcq-options li:hover,
      html[data-theme="dark"] .practice-list li:hover,
      html[data-theme="dark"] .requirements-list li:hover,
      html[data-theme="dark"] .key-points li:hover,
      html[data-theme="dark"] .toc a:hover,
      html[data-theme="dark"] nav a:hover,
      html[data-theme="dark"] tr:hover,
      html[data-theme="dark"] tr:hover td,
      html[data-theme="dark"] [class*="-card"]:hover,
      html[data-theme="dark"] [class*="-box"]:hover,
      html[data-theme="dark"] [class*="-panel"]:hover,
      html[data-theme="dark"] [class*="-item"]:hover,
      html[data-theme="dark"] [class*="-option"]:hover,
      html[data-theme="dark"] .active,
      html[data-theme="dark"] .selected,
      html[data-theme="dark"] .is-active,
      html[data-theme="dark"] [aria-selected="true"] {
        background: #172033 !important;
        color: #f8fafc !important;
        border-color: #60a5fa !important;
        box-shadow: 0 14px 30px rgba(0, 0, 0, 0.28) !important;
      }

      html[data-theme="dark"] .card:hover *,
      html[data-theme="dark"] .question:hover *,
      html[data-theme="dark"] .question-card:hover *,
      html[data-theme="dark"] .question-block:hover *,
      html[data-theme="dark"] .option:hover *,
      html[data-theme="dark"] .tf-option:hover *,
      html[data-theme="dark"] .mcq-option:hover *,
      html[data-theme="dark"] .mcq-options li:hover *,
      html[data-theme="dark"] .practice-list li:hover *,
      html[data-theme="dark"] .requirements-list li:hover *,
      html[data-theme="dark"] .key-points li:hover *,
      html[data-theme="dark"] [class*="-card"]:hover *,
      html[data-theme="dark"] [class*="-box"]:hover *,
      html[data-theme="dark"] [class*="-panel"]:hover *,
      html[data-theme="dark"] [class*="-item"]:hover *,
      html[data-theme="dark"] [class*="-option"]:hover *,
      html[data-theme="dark"] .active *,
      html[data-theme="dark"] .selected *,
      html[data-theme="dark"] .is-active *,
      html[data-theme="dark"] [aria-selected="true"] * {
        color: #f8fafc !important;
      }

      html[data-theme="dark"] [class*="-badge"],
      html[data-theme="dark"] [class*="-tag"],
      html[data-theme="dark"] .badge,
      html[data-theme="dark"] .tag {
        color: #ffffff !important;
        border-color: transparent !important;
      }

      html[data-theme="dark"] .hero-content,
      html[data-theme="dark"] .hero-inner,
      html[data-theme="dark"] .hero-bg,
      html[data-theme="dark"] [class*="hero-content"],
      html[data-theme="dark"] [class*="hero-inner"],
      html[data-theme="dark"] [class*="hero-bg"] {
        background: transparent !important;
        border-color: transparent !important;
        box-shadow: none !important;
      }

      html[data-theme="dark"] .instructions,
      html[data-theme="dark"] .instruction,
      html[data-theme="dark"] .quiz-instructions,
      html[data-theme="dark"] .exam-info,
      html[data-theme="dark"] .info-box,
      html[data-theme="dark"] .score-display,
      html[data-theme="dark"] .score-breakdown,
      html[data-theme="dark"] .progress-wrap,
      html[data-theme="dark"] .section-header,
      html[data-theme="dark"] .q-card,
      html[data-theme="dark"] .q-meta,
      html[data-theme="dark"] .q-scenario,
      html[data-theme="dark"] .option-btn,
      html[data-theme="dark"] .tf-btn,
      html[data-theme="dark"] .options label,
      html[data-theme="dark"] .answer-option,
      html[data-theme="dark"] .feedback,
      html[data-theme="dark"] .explanation,
      html[data-theme="dark"] .results-card {
        background: #172033 !important;
        color: #f8fafc !important;
        border-color: #475569 !important;
      }

      html[data-theme="dark"] .instructions *,
      html[data-theme="dark"] .instruction *,
      html[data-theme="dark"] .quiz-instructions *,
      html[data-theme="dark"] .exam-info *,
      html[data-theme="dark"] .info-box *,
      html[data-theme="dark"] .score-display *,
      html[data-theme="dark"] .score-breakdown *,
      html[data-theme="dark"] .progress-wrap *,
      html[data-theme="dark"] .section-header *,
      html[data-theme="dark"] .q-card *,
      html[data-theme="dark"] .q-meta *,
      html[data-theme="dark"] .q-scenario *,
      html[data-theme="dark"] .option-btn *,
      html[data-theme="dark"] .tf-btn *,
      html[data-theme="dark"] .options label *,
      html[data-theme="dark"] .answer-option *,
      html[data-theme="dark"] .feedback *,
      html[data-theme="dark"] .explanation *,
      html[data-theme="dark"] .results-card * {
        color: inherit !important;
      }

      html[data-theme="dark"] .section-header,
      html[data-theme="dark"] .question-number,
      html[data-theme="dark"] .q-num,
      html[data-theme="dark"] .q-type,
      html[data-theme="dark"] .marks,
      html[data-theme="dark"] .score-pill,
      html[data-theme="dark"] .past-exam-badge {
        color: #ffffff !important;
      }

      html[data-theme="dark"] .question.correct,
      html[data-theme="dark"] .correct,
      html[data-theme="dark"] .correct-answer {
        background: rgba(22, 101, 52, 0.35) !important;
        color: #dcfce7 !important;
        border-color: #22c55e !important;
      }

      html[data-theme="dark"] .question.incorrect,
      html[data-theme="dark"] .wrong,
      html[data-theme="dark"] .incorrect,
      html[data-theme="dark"] .incorrect-answer {
        background: rgba(127, 29, 29, 0.38) !important;
        color: #fee2e2 !important;
        border-color: #ef4444 !important;
      }

      html[data-theme="dark"] input,
      html[data-theme="dark"] textarea,
      html[data-theme="dark"] select,
      html[data-theme="dark"] button:not(.sg-theme-toggle) {
        background: #1f2937 !important;
        color: #f8fafc !important;
        border-color: #4b5563 !important;
      }

      html[data-theme="dark"] hr {
        border-color: #374151 !important;
      }

      html[data-theme="dark"] img,
      html[data-theme="dark"] svg,
      html[data-theme="dark"] canvas,
      html[data-theme="dark"] video {
        background: transparent;
      }

      html,
      body {
        max-width: 100%;
        overflow-x: hidden;
      }

      img,
      svg,
      canvas,
      video,
      pre {
        max-width: 100%;
      }

      table {
        width: 100%;
        border-collapse: collapse;
        table-layout: auto;
      }

      .sg-table-scroll {
        width: 100%;
        max-width: 100%;
        overflow-x: auto;
        overflow-y: hidden;
        -webkit-overflow-scrolling: touch;
      }

      .sg-table-scroll > table {
        min-width: max-content;
      }

      .sg-page-search {
        position: fixed;
        z-index: 9999;
        bottom: max(0.85rem, env(safe-area-inset-bottom));
        right: max(0.85rem, env(safe-area-inset-right));
        display: flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.4rem;
        border: 1px solid rgba(148, 163, 184, 0.35);
        border-radius: 999px;
        background: rgba(15, 23, 42, 0.88);
        color: #f8fafc;
        box-shadow: 0 16px 42px rgba(15, 23, 42, 0.24);
        backdrop-filter: blur(14px);
        max-width: min(34rem, calc(100vw - 1.7rem));
      }

      .sg-page-search__input {
        width: clamp(10rem, 24vw, 18rem);
        min-width: 0;
        height: 2rem;
        border: 0;
        border-radius: 999px;
        padding: 0 0.8rem;
        background: rgba(255, 255, 255, 0.96);
        color: #0f172a;
        font: 600 0.85rem/1.2 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        outline: none;
      }

      .sg-page-search__input::placeholder {
        color: #64748b;
      }

      .sg-page-search__count {
        min-width: 3.8rem;
        text-align: center;
        font: 700 0.72rem/1 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        color: #e2e8f0;
      }

      .sg-page-search__button {
        width: 2rem;
        height: 2rem;
        display: inline-grid;
        place-items: center;
        border: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.12);
        color: #f8fafc;
        cursor: pointer;
        font: 800 1rem/1 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }

      .sg-page-search__button:hover,
      .sg-page-search__button:focus-visible {
        background: rgba(255, 255, 255, 0.22);
        outline: none;
      }

      .sg-search-mark {
        padding: 0 0.12em;
        border-radius: 0.2em;
        background: #fde68a !important;
        color: #1f2937 !important;
        box-shadow: 0 0 0 1px rgba(146, 64, 14, 0.18);
      }

      .sg-search-mark.is-active {
        background: #fb923c !important;
        color: #111827 !important;
        box-shadow: 0 0 0 2px rgba(251, 146, 60, 0.45);
      }

      @media (max-width: 640px) {
        .sg-page-search {
          left: 0.75rem;
          right: 0.75rem;
          border-radius: 0.9rem;
        }

        .sg-page-search__input {
          flex: 1 1 auto;
          width: auto;
        }
      }

      @media (max-width: 760px) {
        .sg-table-scroll > table {
          width: max-content;
        }
      }
    `;

    (document.head || document.documentElement).appendChild(style);
  }

  function applyMode(mode) {
    mode = mode === DARK ? DARK : LIGHT;
    lastMode = mode;
    _settingTheme = true;
    ensureContrastStyle();

    document.documentElement.setAttribute("data-theme", mode);
    document.documentElement.setAttribute(
      "data-md-color-scheme",
      mode === DARK ? "slate" : "default"
    );
    document.documentElement.classList.toggle("dark", mode === DARK);
    document.documentElement.classList.toggle("light", mode !== DARK);
    document.documentElement.classList.toggle("force-light", mode !== DARK);
    document.documentElement.style.colorScheme = mode;

    if (document.body) {
      document.body.setAttribute("data-theme", mode);
      document.body.setAttribute(
        "data-md-color-scheme",
        mode === DARK ? "slate" : "default"
      );
      document.body.classList.toggle("dark", mode === DARK);
      document.body.classList.toggle("light", mode !== DARK);
      document.body.classList.toggle("shoug-light-mode", mode !== DARK);
      document.body.classList.toggle("parent-dark", mode === DARK);
      document.body.classList.toggle("parent-light", mode !== DARK);
    }

    setButtonState(mode);
    _settingTheme = false;

    if (mode === DARK && document.readyState !== 'loading') {
      fixLightBgsInDark();
    }
  }

  function syncTheme() {
    applyMode(preferredMode());
  }

  function bindParentObserver() {
    try {
      if (window.parent === window || !window.parent.document || !window.MutationObserver) {
        return;
      }

      var parentBody = window.parent.document.body;
      if (!parentBody) return;

      new MutationObserver(syncTheme).observe(parentBody, {
        attributes: true,
        attributeFilter: ["data-md-color-scheme", "class"]
      });
    } catch (e) { }
  }

  function installToggle() {
    window.toggleTheme = function () {
      var next = lastMode === DARK ? LIGHT : DARK;
      try {
        localStorage.setItem(
          "__palette",
          JSON.stringify({
            color: {
              scheme: next === DARK ? "slate" : "default",
              primary: "deep-purple",
              accent: "pink"
            }
          })
        );
        localStorage.setItem("theme", next);
        localStorage.setItem("shoug-theme", next);
      } catch (e) { }
      applyMode(next);
    };
  }

  function installThemeButton() {
    if (!document.body) return;
    if (hasSelfTheme()) return;
    if (document.querySelector('.sg-theme-toggle')) return;
    if (document.querySelector('#themeToggle, #themeBtn, .theme-toggle, .shoug-theme-btn')) return;
    if (document.querySelector('[onclick*="toggleTheme"]')) return;

    var btn = document.createElement('button');
    btn.className = 'sg-theme-toggle';
    btn.id = 'themeIcon';
    btn.setAttribute('aria-label', 'Toggle dark/light mode');
    btn.textContent = lastMode === DARK ? '☀️' : '🌙';
    document.body.appendChild(btn);
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      if (typeof window.toggleTheme === 'function') window.toggleTheme();
    });
  }

  function fixLightBgsInDark() {
    if (!document.body) return;
    if (document.documentElement.getAttribute('data-theme') !== DARK) return;
    if (hasSelfTheme()) return;

    var SKIP = /^(SCRIPT|STYLE|IMG|SVG|CANVAS|VIDEO|AUDIO|IFRAME|INPUT|BUTTON|SELECT|TEXTAREA|OPTION|NOSCRIPT)$/;
    var all = document.body.querySelectorAll('*');
    var batch = Array.prototype.slice.call(all);
    var idx = 0;

    function run() {
      var end = Math.min(idx + 80, batch.length);
      for (; idx < end; idx++) {
        var el = batch[idx];
        if (SKIP.test(el.tagName)) continue;
        if (el.hasAttribute('data-sg-dark')) continue;
        if (el.style.backgroundColor) continue; // inline style already handled by CSS

        var bg = window.getComputedStyle(el).backgroundColor;
        if (!bg || bg === 'transparent' || bg === 'rgba(0, 0, 0, 0)') continue;

        var m = bg.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
        if (!m) continue;

        var lum = (0.299 * +m[1] + 0.587 * +m[2] + 0.114 * +m[3]) / 255;
        if (lum > 0.72) {
          el.style.setProperty('background-color', '#1f2937', 'important');
          el.style.setProperty('color', '#e5e7eb', 'important');
          el.style.setProperty('border-color', '#374151', 'important');
          el.setAttribute('data-sg-dark', '1');
        }
      }
      if (idx < batch.length) {
        window.requestAnimationFrame ? requestAnimationFrame(run) : setTimeout(run, 16);
      }
    }

    window.requestAnimationFrame ? requestAnimationFrame(run) : setTimeout(run, 0);
  }

  function bindSelfAttrObserver() {
    if (!window.MutationObserver) return;
    if (hasSelfTheme()) return;

    var _observer = new window.MutationObserver(function (mutations) {
      mutations.forEach(function (m) {
        if (_settingTheme) return;
        if (m.attributeName === 'data-theme') {
          var theme = document.documentElement.getAttribute('data-theme');
          if ((theme === DARK || theme === LIGHT) && theme !== lastMode) {
            lastMode = theme;
            try { localStorage.setItem('shoug-theme', theme); } catch (e) { }
            setButtonState(theme);
          }
        }
      });
    });

    // Delay attachment so page init scripts (which run before window.load) don't corrupt shoug-theme
    function attach() {
      _observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
    }
    if (document.readyState === 'complete') {
      setTimeout(attach, 200);
    } else {
      window.addEventListener('load', function () { setTimeout(attach, 200); }, { once: true });
    }
  }

  function currentHeight() {
    var body = document.body;
    var root = document.documentElement;
    return Math.ceil(Math.max(
      body ? body.scrollHeight : 0,
      body ? body.offsetHeight : 0,
      root ? root.scrollHeight : 0,
      root ? root.offsetHeight : 0
    ));
  }

  function postHeightToParent() {
    if (window.parent === window) return;
    try {
      window.parent.postMessage({
        type: "sg:iframe-height",
        path: window.location.pathname,
        height: currentHeight()
      }, window.location.origin);
    } catch (e) { }
  }

  function bindDynamicHeight() {
    postHeightToParent();
    window.addEventListener("load", postHeightToParent);
    window.addEventListener("resize", postHeightToParent);

    if (window.ResizeObserver && document.body) {
      new ResizeObserver(postHeightToParent).observe(document.body);
    }

    if (window.MutationObserver && document.body) {
      new MutationObserver(postHeightToParent).observe(document.body, {
        childList: true,
        subtree: true,
        attributes: true,
        characterData: true
      });
    }

    window.setTimeout(postHeightToParent, 250);
    window.setTimeout(postHeightToParent, 1000);
  }

  function wrapResponsiveTables() {
    if (!document.body) return;
    document.querySelectorAll("table").forEach(function (table) {
      if (table.closest(".sg-table-scroll")) return;
      var wrapper = document.createElement("div");
      wrapper.className = "sg-table-scroll";
      table.parentNode.insertBefore(wrapper, table);
      wrapper.appendChild(table);
    });
  }

  function clearSearchMarks() {
    searchState.marks.forEach(function (mark) {
      mark.replaceWith(document.createTextNode(mark.textContent));
    });
    searchState.marks = [];
    searchState.active = -1;
    document.body && document.body.normalize();
  }

  function updateSearchCount() {
    var count = document.querySelector(".sg-page-search__count");
    if (!count) return;
    if (!searchState.query) {
      count.textContent = "0/0";
      return;
    }
    count.textContent = searchState.marks.length
      ? String(searchState.active + 1) + "/" + String(searchState.marks.length)
      : "0/0";
  }

  function safeTextPattern(value) {
    return String(value).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  function shouldSkipSearchNode(node) {
    var parent = node && node.parentElement;
    if (!parent) return true;
    return Boolean(parent.closest(
      "script, style, noscript, textarea, input, select, option, button, .sg-page-search, .sg-search-mark"
    ));
  }

  function runSearch(query) {
    clearSearchMarks();
    searchState.query = String(query || "").trim();

    if (!searchState.query || searchState.query.length < 2 || !document.body) {
      updateSearchCount();
      postHeightToParent();
      return;
    }

    var walker = document.createTreeWalker(
      document.body,
      NodeFilter.SHOW_TEXT,
      {
        acceptNode: function (node) {
          if (shouldSkipSearchNode(node)) return NodeFilter.FILTER_REJECT;
          if (!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
          return node.nodeValue.toLowerCase().includes(searchState.query.toLowerCase())
            ? NodeFilter.FILTER_ACCEPT
            : NodeFilter.FILTER_REJECT;
        }
      }
    );

    var nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);

    var pattern = new RegExp("(" + safeTextPattern(searchState.query) + ")", "gi");
    nodes.forEach(function (node) {
      var frag = document.createDocumentFragment();
      var text = node.nodeValue;
      var lastIndex = 0;
      text.replace(pattern, function (match, _group, index) {
        if (index > lastIndex) frag.appendChild(document.createTextNode(text.slice(lastIndex, index)));
        var mark = document.createElement("mark");
        mark.className = "sg-search-mark";
        mark.textContent = match;
        frag.appendChild(mark);
        searchState.marks.push(mark);
        lastIndex = index + match.length;
        return match;
      });
      if (lastIndex < text.length) frag.appendChild(document.createTextNode(text.slice(lastIndex)));
      node.replaceWith(frag);
    });

    searchState.active = searchState.marks.length ? 0 : -1;
    focusSearchResult(0);
    updateSearchCount();
    postHeightToParent();
  }

  function focusSearchResult(offset) {
    if (!searchState.marks.length) {
      updateSearchCount();
      return;
    }

    searchState.marks.forEach(function (mark) {
      mark.classList.remove("is-active");
    });

    searchState.active = (searchState.active + offset + searchState.marks.length) % searchState.marks.length;
    var active = searchState.marks[searchState.active];
    active.classList.add("is-active");
    active.scrollIntoView({ behavior: "smooth", block: "center", inline: "nearest" });
    updateSearchCount();
  }

  function installSearch() {
    if (document.querySelector(".sg-page-search") || !document.body) return;

    var form = document.createElement("form");
    form.className = "sg-page-search";
    form.setAttribute("role", "search");
    form.innerHTML = [
      '<input class="sg-page-search__input" type="search" placeholder="Search page" aria-label="Search this page" autocomplete="off">',
      '<span class="sg-page-search__count" aria-live="polite">0/0</span>',
      '<button class="sg-page-search__button" type="button" data-search-prev aria-label="Previous result">‹</button>',
      '<button class="sg-page-search__button" type="button" data-search-next aria-label="Next result">›</button>'
    ].join("");
    document.body.appendChild(form);

    var input = form.querySelector("input");
    input.addEventListener("input", function () {
      runSearch(input.value);
    });
    input.addEventListener("keydown", function (event) {
      if (event.key === "Enter") {
        event.preventDefault();
        focusSearchResult(event.shiftKey ? -1 : 1);
      }
      if (event.key === "Escape") {
        input.value = "";
        runSearch("");
        input.blur();
      }
    });
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      focusSearchResult(1);
    });
    form.querySelector("[data-search-prev]").addEventListener("click", function () {
      focusSearchResult(-1);
    });
    form.querySelector("[data-search-next]").addEventListener("click", function () {
      focusSearchResult(1);
    });

    document.addEventListener("keydown", function (event) {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "f") {
        event.preventDefault();
        input.focus();
        input.select();
      }
    });
  }

  function loadPastExamPractice() {
    if (!/\/ethc303\//i.test(location.pathname)) return;
    if (/\/ethc303\/quizez\//i.test(location.pathname)) return;
    if (document.querySelector('script[src="/javascripts/past-exam-practice.js"]')) return;

    var script = document.createElement("script");
    script.src = "/javascripts/past-exam-practice.js";
    script.defer = true;
    (document.body || document.documentElement).appendChild(script);
  }

  installToggle();

  syncTheme();

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      installToggle();
      syncTheme();
      installSearch();
      installThemeButton();
      wrapResponsiveTables();
      bindDynamicHeight();
      loadPastExamPractice();
      fixLightBgsInDark();
    }, { once: true });
  } else {
    installToggle();
    syncTheme();
    installSearch();
    installThemeButton();
    wrapResponsiveTables();
    bindDynamicHeight();
    loadPastExamPractice();
    fixLightBgsInDark();
  }

  bindParentObserver();
  bindSelfAttrObserver();

  window.addEventListener("load", function () {
    installToggle();
    syncTheme();
    installSearch();
    installThemeButton();
    wrapResponsiveTables();
    loadPastExamPractice();
    postHeightToParent();
    fixLightBgsInDark();
  });

  window.addEventListener("storage", function (event) {
    if (!event.key || event.key === "__palette" || event.key === "theme" || event.key === "shoug-theme") {
      syncTheme();
    }
  });

  if (window.matchMedia) {
    var media = window.matchMedia("(prefers-color-scheme: dark)");
    if (media.addEventListener) media.addEventListener("change", syncTheme);
    else if (media.addListener) media.addListener(syncTheme);
  }
})();
