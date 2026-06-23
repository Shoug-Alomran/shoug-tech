(function () {
  var root = document.documentElement;
  var paletteKeyPattern = /(?:^|\/)__palette$|\.__palette$/;

  function isMkDocsPage() {
    var body = document.body;
    return !!(
      body && body.hasAttribute("data-md-color-scheme") ||
      document.querySelector("[data-md-component='container']")
    );
  }

  if (isMkDocsPage()) return;

  function schemeToTheme(scheme) {
    if (scheme === "slate" || scheme === "dark") return "dark";
    if (scheme === "default" || scheme === "light") return "light";
    return null;
  }

  function paletteToTheme(palette) {
    return schemeToTheme(palette && palette.color && palette.color.scheme);
  }

  function parsePalette(raw) {
    if (!raw) return null;
    try { return JSON.parse(raw); } catch (e) { return null; }
  }

  function readParentScheme() {
    try {
      if (!window.parent || window.parent === window || !window.parent.document) return null;
      var pdoc = window.parent.document;
      var pbody = pdoc.body;
      var proot = pdoc.documentElement;
      if (pbody && pbody.classList.contains("shoug-light-mode")) return "light";
      var scheme = (pbody && pbody.getAttribute("data-md-color-scheme")) ||
        (proot && proot.getAttribute("data-md-color-scheme"));
      var fromScheme = schemeToTheme(scheme);
      if (fromScheme) return fromScheme;

      var parentTheme = (pbody && pbody.getAttribute("data-theme")) ||
        (proot && proot.getAttribute("data-theme"));
      var fromTheme = schemeToTheme(parentTheme);
      if (fromTheme) return fromTheme;

      if (pbody && pbody.classList.contains("dark")) return "dark";
      if (pbody && pbody.classList.contains("light")) return "light";
      if (proot && proot.classList.contains("dark")) return "dark";
      if (proot && proot.classList.contains("light")) return "light";
    } catch (e) { }
    return null;
  }

  function readSystemTheme() {
    return (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) ? "dark" : "light";
  }

  function readStoredScheme() {
    try {
      var shougTheme = window.localStorage && window.localStorage.getItem("shoug-theme");
      if (shougTheme === "light") return "light";
      if (shougTheme === "dark") return "dark";
    } catch (e) { }

    try {
      if (window.parent && typeof window.parent.__md_get === "function") {
        var parentPalette = window.parent.__md_get("__palette");
        var parentTheme = paletteToTheme(parentPalette);
        if (parentTheme) return parentTheme;
      }
    } catch (e) { }

    try {
      if (typeof window.__md_get === "function") {
        var palette = window.__md_get("__palette");
        var theme = paletteToTheme(palette);
        if (theme) return theme;
      }
    } catch (e) { }

    try {
      var direct = paletteToTheme(parsePalette(window.localStorage && window.localStorage.getItem("__palette")));
      if (direct) return direct;

      for (var i = 0; i < window.localStorage.length; i += 1) {
        var key = window.localStorage.key(i);
        if (!paletteKeyPattern.test(key)) continue;
        var scoped = paletteToTheme(parsePalette(window.localStorage.getItem(key)));
        if (scoped) return scoped;
      }
    } catch (e) { }

    return null;
  }

  function resolveTheme() {
    return readParentScheme() || readStoredScheme() || readSystemTheme();
  }

  function ensureFallbackStyle() {
    if (root.hasAttribute("data-sg-styled")) return;

    var id = "standalone-dark-fallback";
    var style = document.getElementById(id);
    if (!style) {
      style = document.createElement("style");
      style.id = id;
      (document.head || document.documentElement).appendChild(style);
    }

    if (style.textContent) return;

    style.textContent = [
      "html[data-theme='dark'], html[data-theme='dark'] :root {",
      "  --white: #111827 !important;",
      "  --card: #111827 !important;",
      "  --surface: #111827 !important;",
      "  --background: #0b1020 !important;",
      "  --bg: #0b1020 !important;",
      "  --light-bg: #1f2937 !important;",
      "  --text-dark: #e5e7eb !important;",
      "  --text-color: #e5e7eb !important;",
      "  --text: #e5e7eb !important;",
      "  --text-light: #cbd5e1 !important;",
      "  --ink: #e5e7eb !important;",
      "  --ink-1: #e5e7eb !important;",
      "  --ink-2: #cbd5e1 !important;",
      "  --primary-color: #93c5fd !important;",
      "  --primary: #93c5fd !important;",
      "  --primary-dark: #bfdbfe !important;",
      "  --secondary: #c4b5fd !important;",
      "  --secondary-color: #c4b5fd !important;",
      "  --accent: #fbbf24 !important;",
      "  --accent-color: #fbbf24 !important;",
      "  --border: #374151 !important;",
      "  --border-color: #4b5563 !important;",
      "}",
      "html[data-theme='dark'] { color-scheme: dark; }",
      "html[data-theme='light'] { color-scheme: light; }",
      "html[data-theme='dark'] body { background: #0b1020 !important; color: #e5e7eb !important; }",
      "html[data-theme='dark'] .container, html[data-theme='dark'] main, html[data-theme='dark'] section, html[data-theme='dark'] article, html[data-theme='dark'] aside, html[data-theme='dark'] nav, html[data-theme='dark'] header, html[data-theme='dark'] footer, html[data-theme='dark'] .content, html[data-theme='dark'] .card, html[data-theme='dark'] .panel, html[data-theme='dark'] .box, html[data-theme='dark'] .wrapper, html[data-theme='dark'] .question, html[data-theme='dark'] .question-card, html[data-theme='dark'] .question-block, html[data-theme='dark'] .quiz-container, html[data-theme='dark'] .chapter, html[data-theme='dark'] .section, html[data-theme='dark'] .topic-card, html[data-theme='dark'] .exam-question, html[data-theme='dark'] .process-structure, html[data-theme='dark'] .solution-card, html[data-theme='dark'] .memory-section, html[data-theme='dark'] .memory-layout, html[data-theme='dark'] .page-table-container, html[data-theme='dark'] .result-box, html[data-theme='dark'] .feedback, html[data-theme='dark'] .mock-answer, html[data-theme='dark'] .answer-box, html[data-theme='dark'] [class*='-card'], html[data-theme='dark'] [class*='-box'], html[data-theme='dark'] [class*='-panel'], html[data-theme='dark'] [class*='-section'], html[data-theme='dark'] [class*='-container'], html[data-theme='dark'] [class*='-wrapper'], html[data-theme='dark'] [class*='-content'], html[data-theme='dark'] [class*='-table'], html[data-theme='dark'] [class*='-grid'], html[data-theme='dark'] [class*='-diagram'] { background: #111827 !important; color: #e5e7eb !important; border-color: #374151 !important; }",
      "html[data-theme='dark'] .learning-outcomes, html[data-theme='dark'] .clo-box, html[data-theme='dark'] .highlight, html[data-theme='dark'] .key-point, html[data-theme='dark'] .warning, html[data-theme='dark'] .principle, html[data-theme='dark'] .timeline-item, html[data-theme='dark'] .stat-card, html[data-theme='dark'] .metric-card, html[data-theme='dark'] .summary-card, html[data-theme='dark'] .concept-box, html[data-theme='dark'] .example-box, html[data-theme='dark'] .exam-section, html[data-theme='dark'] .diagram-container, html[data-theme='dark'] .critical-section-diagram, html[data-theme='dark'] .race-condition-box, html[data-theme='dark'] .key-concept, html[data-theme='dark'] .tip, html[data-theme='dark'] .exam-example, html[data-theme='dark'] .formula, html[data-theme='dark'] .ipc-section, html[data-theme='dark'] .scheduling-box, html[data-theme='dark'] .deadlock-box, html[data-theme='dark'] .memory-box, html[data-theme='dark'] .frame-box, html[data-theme='dark'] .page-box, html[data-theme='dark'] .option, html[data-theme='dark'] .tf-option, html[data-theme='dark'] .mcq-options li { background: #1f2937 !important; color: #e5e7eb !important; border-color: #4b5563 !important; }",
      "html[data-theme='dark'] .diagram-section, html[data-theme='dark'] .symbol-card, html[data-theme='dark'] .symbol-visual, html[data-theme='dark'] .when-to-use, html[data-theme='dark'] .key-points, html[data-theme='dark'] .relationships-section, html[data-theme='dark'] .relationship-item, html[data-theme='dark'] .scenario, html[data-theme='dark'] .quick-nav { background: #1f2937 !important; color: #e5e7eb !important; border-color: #4b5563 !important; }",
      "html[data-theme='dark'] .layer, html[data-theme='dark'] [class*='-badge'], html[data-theme='dark'] [class*='-tag'] { color: #ffffff !important; }",
      "html[data-theme='dark'] .diagram-title, html[data-theme='dark'] .symbol-name, html[data-theme='dark'] .symbol-description, html[data-theme='dark'] .scenario, html[data-theme='dark'] .quick-nav h4, html[data-theme='dark'] .quick-nav a, html[data-theme='dark'] .example-image p { color: #e5e7eb !important; }",
      "html[data-theme='dark'] .diagram-type { background: #312e81 !important; color: #e0e7ff !important; border: 1px solid #6366f1 !important; }",
      "html[data-theme='dark'] .when-to-use h3 { color: #86efac !important; }",
      "html[data-theme='dark'] .key-points h4 { color: #93c5fd !important; }",
      "html[data-theme='dark'] .relationships-section h4, html[data-theme='dark'] .relationship-symbol { color: #c4b5fd !important; }",
      "html[data-theme='dark'] h1, html[data-theme='dark'] h2, html[data-theme='dark'] h3, html[data-theme='dark'] h4, html[data-theme='dark'] h5, html[data-theme='dark'] h6, html[data-theme='dark'] p, html[data-theme='dark'] li, html[data-theme='dark'] dt, html[data-theme='dark'] dd, html[data-theme='dark'] label { color: #e5e7eb !important; }",
      "html[data-theme='dark'] a { color: #c4b5fd !important; }",
      "html[data-theme='dark'] strong, html[data-theme='dark'] b { color: #f8fafc !important; }",
      "html[data-theme='dark'] table { background: #0f172a !important; color: #e5e7eb !important; }",
      "html[data-theme='dark'] th { background: #1f2937 !important; color: #f8fafc !important; }",
      "html[data-theme='dark'] td { background: #111827 !important; color: #e5e7eb !important; border-color: #374151 !important; }",
      "html[data-theme='dark'] .question, html[data-theme='dark'] .question-card, html[data-theme='dark'] .question-block, html[data-theme='dark'] .topic-card, html[data-theme='dark'] .exam-question, html[data-theme='dark'] .solution-card, html[data-theme='dark'] .result-box, html[data-theme='dark'] .feedback, html[data-theme='dark'] .mock-answer, html[data-theme='dark'] .answer-box, html[data-theme='dark'] .learning-outcomes, html[data-theme='dark'] .highlight, html[data-theme='dark'] .key-point, html[data-theme='dark'] .warning, html[data-theme='dark'] .principle, html[data-theme='dark'] .timeline-item, html[data-theme='dark'] .stat-card, html[data-theme='dark'] .metric-card, html[data-theme='dark'] .summary-card, html[data-theme='dark'] .concept-box, html[data-theme='dark'] .example-box, html[data-theme='dark'] .exam-section, html[data-theme='dark'] .key-concept, html[data-theme='dark'] .tip, html[data-theme='dark'] .exam-example, html[data-theme='dark'] .option, html[data-theme='dark'] .tf-option, html[data-theme='dark'] .mcq-option, html[data-theme='dark'] .mcq-options li, html[data-theme='dark'] .practice-list li, html[data-theme='dark'] .requirements-list li, html[data-theme='dark'] .key-points li, html[data-theme='dark'] [class*='-card'], html[data-theme='dark'] [class*='-box'], html[data-theme='dark'] [class*='-panel'], html[data-theme='dark'] [class*='-item'], html[data-theme='dark'] [class*='-option'] { background: #1f2937 !important; color: #e5e7eb !important; border-color: #4b5563 !important; }",
      "html[data-theme='dark'] tr:nth-child(even) td, html[data-theme='dark'] tr:nth-child(even) th { background: #172033 !important; }",
      "html[data-theme='dark'] pre, html[data-theme='dark'] code, html[data-theme='dark'] .formula { background: #111827 !important; color: #e5e7eb !important; border-color: #374151 !important; }",
      "html[data-theme='dark'] .card:hover, html[data-theme='dark'] .question:hover, html[data-theme='dark'] .question-card:hover, html[data-theme='dark'] .question-block:hover, html[data-theme='dark'] .option:hover, html[data-theme='dark'] .tf-option:hover, html[data-theme='dark'] .mcq-option:hover, html[data-theme='dark'] .mcq-options li:hover, html[data-theme='dark'] .practice-list li:hover, html[data-theme='dark'] .requirements-list li:hover, html[data-theme='dark'] .key-points li:hover, html[data-theme='dark'] .toc a:hover, html[data-theme='dark'] nav a:hover, html[data-theme='dark'] tr:hover, html[data-theme='dark'] tr:hover td, html[data-theme='dark'] [class*='-card']:hover, html[data-theme='dark'] [class*='-box']:hover, html[data-theme='dark'] [class*='-panel']:hover, html[data-theme='dark'] [class*='-item']:hover, html[data-theme='dark'] [class*='-option']:hover, html[data-theme='dark'] .active, html[data-theme='dark'] .selected, html[data-theme='dark'] .is-active, html[data-theme='dark'] [aria-selected='true'] { background: #172033 !important; color: #f8fafc !important; border-color: #60a5fa !important; box-shadow: 0 14px 30px rgba(0, 0, 0, 0.28) !important; }",
      "html[data-theme='dark'] .card:hover *, html[data-theme='dark'] .question:hover *, html[data-theme='dark'] .question-card:hover *, html[data-theme='dark'] .question-block:hover *, html[data-theme='dark'] .option:hover *, html[data-theme='dark'] .tf-option:hover *, html[data-theme='dark'] .mcq-option:hover *, html[data-theme='dark'] .mcq-options li:hover *, html[data-theme='dark'] .practice-list li:hover *, html[data-theme='dark'] .requirements-list li:hover *, html[data-theme='dark'] .key-points li:hover *, html[data-theme='dark'] [class*='-card']:hover *, html[data-theme='dark'] [class*='-box']:hover *, html[data-theme='dark'] [class*='-panel']:hover *, html[data-theme='dark'] [class*='-item']:hover *, html[data-theme='dark'] [class*='-option']:hover *, html[data-theme='dark'] .active *, html[data-theme='dark'] .selected *, html[data-theme='dark'] .is-active *, html[data-theme='dark'] [aria-selected='true'] * { color: #f8fafc !important; }",
      "html[data-theme='dark'] [class*='-badge'], html[data-theme='dark'] [class*='-tag'], html[data-theme='dark'] .badge, html[data-theme='dark'] .tag { color: #ffffff !important; border-color: transparent !important; }",
      "html[data-theme='dark'] .hero-content, html[data-theme='dark'] .hero-inner, html[data-theme='dark'] .hero-bg, html[data-theme='dark'] [class*='hero-content'], html[data-theme='dark'] [class*='hero-inner'], html[data-theme='dark'] [class*='hero-bg'] { background: transparent !important; border-color: transparent !important; box-shadow: none !important; }",
      "html[data-theme='dark'] .instructions, html[data-theme='dark'] .instruction, html[data-theme='dark'] .quiz-instructions, html[data-theme='dark'] .exam-info, html[data-theme='dark'] .info-box, html[data-theme='dark'] .score-display, html[data-theme='dark'] .score-breakdown, html[data-theme='dark'] .progress-wrap, html[data-theme='dark'] .section-header, html[data-theme='dark'] .q-card, html[data-theme='dark'] .q-meta, html[data-theme='dark'] .q-scenario, html[data-theme='dark'] .option-btn, html[data-theme='dark'] .tf-btn, html[data-theme='dark'] .options label, html[data-theme='dark'] .answer-option, html[data-theme='dark'] .feedback, html[data-theme='dark'] .explanation, html[data-theme='dark'] .results-card { background: #172033 !important; color: #f8fafc !important; border-color: #475569 !important; }",
      "html[data-theme='dark'] .instructions *, html[data-theme='dark'] .instruction *, html[data-theme='dark'] .quiz-instructions *, html[data-theme='dark'] .exam-info *, html[data-theme='dark'] .info-box *, html[data-theme='dark'] .score-display *, html[data-theme='dark'] .score-breakdown *, html[data-theme='dark'] .progress-wrap *, html[data-theme='dark'] .section-header *, html[data-theme='dark'] .q-card *, html[data-theme='dark'] .q-meta *, html[data-theme='dark'] .q-scenario *, html[data-theme='dark'] .option-btn *, html[data-theme='dark'] .tf-btn *, html[data-theme='dark'] .options label *, html[data-theme='dark'] .answer-option *, html[data-theme='dark'] .feedback *, html[data-theme='dark'] .explanation *, html[data-theme='dark'] .results-card * { color: inherit !important; }",
      "html[data-theme='dark'] .section-header, html[data-theme='dark'] .question-number, html[data-theme='dark'] .q-num, html[data-theme='dark'] .q-type, html[data-theme='dark'] .marks, html[data-theme='dark'] .score-pill, html[data-theme='dark'] .past-exam-badge { color: #ffffff !important; }",
      "html[data-theme='dark'] .question.correct, html[data-theme='dark'] .correct, html[data-theme='dark'] .correct-answer { background: rgba(22, 101, 52, 0.35) !important; color: #dcfce7 !important; border-color: #22c55e !important; }",
      "html[data-theme='dark'] .question.incorrect, html[data-theme='dark'] .wrong, html[data-theme='dark'] .incorrect, html[data-theme='dark'] .incorrect-answer { background: rgba(127, 29, 29, 0.38) !important; color: #fee2e2 !important; border-color: #ef4444 !important; }",
      "html[data-theme='dark'] input, html[data-theme='dark'] textarea, html[data-theme='dark'] select, html[data-theme='dark'] button { background: #1f2937 !important; color: #f8fafc !important; border-color: #4b5563 !important; }",
      "html[data-theme='dark'] hr { border-color: #374151 !important; }",
      "html[data-theme='dark'] svg text { fill: #e5e7eb !important; }"
    ].join("\n");
  }

  function applyTheme(theme) {
    var dark = theme === "dark";
    root.setAttribute("data-theme", dark ? "dark" : "light");
    root.classList.toggle("dark", dark);
    root.classList.toggle("light", !dark);
    root.classList.toggle("force-light", !dark);

    if (document.body) {
      document.body.classList.toggle("dark", dark);
      document.body.classList.toggle("light", !dark);
      document.body.classList.toggle("shoug-light-mode", !dark);
    }
  }

  function sync() {
    ensureFallbackStyle();
    applyTheme(resolveTheme());
  }

  var syncQueued = false;
  function queueSync() {
    if (syncQueued) return;
    syncQueued = true;
    var run = function () {
      syncQueued = false;
      sync();
    };
    if (window.requestAnimationFrame) window.requestAnimationFrame(run);
    else setTimeout(run, 16);
  }

  sync();
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", queueSync);
  }

  var media = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;
  if (media) {
    if (media.addEventListener) media.addEventListener("change", queueSync);
    else if (media.addListener) media.addListener(queueSync);
  }

  window.addEventListener("storage", function (event) {
    if (!event.key || event.key === "__palette" || paletteKeyPattern.test(event.key)) queueSync();
  });

  if (window.MutationObserver) {
    try {
      var pdoc = window.parent && window.parent.document;
      var targets = [pdoc && pdoc.body, pdoc && pdoc.documentElement];

      targets.forEach(function (target) {
        if (!target) return;
        new MutationObserver(queueSync).observe(target, {
          attributes: true,
          attributeFilter: ["data-md-color-scheme", "data-theme", "class"]
        });
      });
    } catch (e) { }
  }
})();

(function () {
  function initCriticalPath() {
    var courses = window.__ACADEMIC_PLAN_COURSES__;
    if (!Array.isArray(courses) || !courses.length) return;

    var byId = new Map(courses.map(function (course) { return [course.id, course]; }));
    var nextLevelDependents = new Map(courses.map(function (course) { return [course.id, []]; }));

    courses.forEach(function (course) {
      (course.prereqs || []).forEach(function (prereqId) {
        var prereq = byId.get(prereqId);
        if (!prereq || course.level !== prereq.level + 1) return;
        nextLevelDependents.get(prereqId).push(course);
      });
    });

    var critical = new Map();
    courses.forEach(function (course) {
      var unlocks = nextLevelDependents.get(course.id) || [];
      if (course.level === 8 || unlocks.length) {
        critical.set(course.id, {
          course: course,
          unlocks: unlocks
        });
      }
    });
    if (!critical.size) return;

    var style = document.createElement("style");
    style.id = "academic-critical-path-styles";
    style.textContent = [
      ".critical-path-notice{--cp:#f59e0b;--cp-bg:rgba(245,158,11,.10);display:flex;align-items:center;gap:12px;margin:16px 0;padding:12px 14px;border:1px solid rgba(245,158,11,.62);border-left:4px solid var(--cp);border-radius:10px;background:var(--cp-bg);color:inherit;box-shadow:none}",
      ".critical-path-notice__icon{display:grid;place-items:center;flex:0 0 34px;width:34px;height:34px;border-radius:9px;background:var(--cp);color:#211400;font-size:18px;font-weight:900}",
      ".critical-path-notice__copy{min-width:0;flex:1}",
      ".critical-path-notice__title{font:900 12px/1.2 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:1.2px;text-transform:uppercase;color:var(--cp)}",
      ".critical-path-notice__text{margin-top:4px;font-size:12px;line-height:1.5;opacity:.88}",
      ".critical-path-notice__count{flex:0 0 auto;padding:4px 8px;border-radius:999px;background:var(--cp);color:#211400;font:900 10px/1.2 ui-monospace,SFMono-Regular,Menlo,monospace;white-space:nowrap}",
      "[data-id].is-critical-path{position:relative!important;border-color:var(--critical-path-color,#f59e0b)!important;box-shadow:inset 3px 0 0 var(--critical-path-color,#f59e0b)!important}",
      "[data-id].is-critical-path:not(.completed):not(.is-done):not(.st-done){background-image:linear-gradient(90deg,rgba(245,158,11,.08),transparent 34%)!important}",
      "[data-id].is-critical-path.completed,[data-id].is-critical-path.is-done,[data-id].is-critical-path.st-done{--critical-path-color:#22c55e}",
      ".critical-path-badge{display:inline-flex!important;align-items:center;gap:4px;width:max-content!important;max-width:100%;margin:4px 0 0!important;padding:2px 7px!important;border:1px solid rgba(245,158,11,.75)!important;border-radius:4px!important;background:rgba(245,158,11,.14)!important;color:#f59e0b!important;font:800 9px/1.3 ui-monospace,SFMono-Regular,Menlo,monospace!important;letter-spacing:.35px!important;text-transform:uppercase;white-space:nowrap!important;vertical-align:middle}",
      ".critical-path-badge::before{content:'⚠';font-size:9px}",
      ".controls.no-course-search{justify-content:flex-end!important}",
      ".controls.no-course-search .filter-group,.controls.no-course-search .level-filter{margin-left:auto}",
      ".nav-center.no-course-search,.search-box.no-course-search,.search-wrap.no-course-search{display:none!important}",
      "@media(max-width:640px){.critical-path-notice{padding:10px;gap:9px}.critical-path-notice__count{display:none}.critical-path-badge{font-size:8px!important;white-space:normal!important}}"
    ].join("\n");
    document.head.appendChild(style);

    function placeNotice() {
      if (document.querySelector(".critical-path-notice")) return;
      var anchor = document.querySelector(".filter-strip, .controls, .choice-section, .choice-row, .board, #courseList, #roadmap");
      if (!anchor || !anchor.parentNode) return;

      var notice = document.createElement("aside");
      notice.className = "critical-path-notice";
      notice.setAttribute("role", "note");
      notice.innerHTML =
        '<div class="critical-path-notice__icon">⚠</div>' +
        '<div class="critical-path-notice__copy">' +
          '<div class="critical-path-notice__title" data-ar-text="المسار الحرج · لا تؤجل">Critical path · do not delay</div>' +
          '<div class="critical-path-notice__text" data-ar-text="المقررات المحددة مطلوبة في المستوى الموضح للحفاظ على تسلسل الخطة. تأجيلها قد يمنع مقررات المستوى التالي ويؤخر التخرج.">Highlighted courses must be taken in the level shown to stay on sequence. Delaying one can block next-level courses and delay graduation.</div>' +
        '</div>' +
        '<div class="critical-path-notice__count">' + critical.size + ' COURSES</div>';
      anchor.parentNode.insertBefore(notice, anchor);
    }

    function enhanceCards() {
      placeNotice();
      document.querySelectorAll("[data-id]").forEach(function (card) {
        var item = critical.get(card.dataset.id);
        if (!item) return;

        card.classList.add("is-critical-path");
        var unlockedIds = item.unlocks.map(function (course) { return course.id; });
        var message = item.course.level === 8
          ? "Graduation-critical: complete in Level 8."
          : "Take in Level " + item.course.level + ". Delaying blocks " + unlockedIds.join(", ") + " in Level " + (item.course.level + 1) + ".";

        if (card.querySelector(".critical-path-badge")) return;
        card.setAttribute("aria-label", item.course.id + ". " + message);
        var badge = document.createElement("span");
        badge.className = "critical-path-badge";
        badge.textContent = item.course.level === 8
          ? "Critical · Graduate L8"
          : "Critical · Take L" + item.course.level;

        var target = card.querySelector(".cc-name, .c-name, .cr-name-cell, .course-name, .course-info, .course-code");
        if (target) target.appendChild(badge);
        else card.appendChild(badge);
      });
    }

    function removeCourseSearch() {
      document.querySelectorAll("#searchInput").forEach(function (input) {
        var wrapper = input.closest(".nav-center, .search-box, .search-wrap");
        var controls = input.closest(".controls");
        if (controls) controls.classList.add("no-course-search");
        if (wrapper) wrapper.remove();
        else input.remove();
      });
    }

    var queued = false;
    function queueEnhance() {
      if (queued) return;
      queued = true;
      requestAnimationFrame(function () {
        queued = false;
        enhanceCards();
      });
    }

    removeCourseSearch();
    enhanceCards();
    new MutationObserver(queueEnhance).observe(document.body, { childList: true, subtree: true });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initCriticalPath);
  } else {
    initCriticalPath();
  }
})();
