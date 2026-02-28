(function () {
  var root = document.documentElement;

  function readParentScheme() {
    try {
      if (!window.parent || !window.parent.document) return null;
      var pdoc = window.parent.document;
      var scheme = (pdoc.body && pdoc.body.getAttribute("data-md-color-scheme")) ||
                   (pdoc.documentElement && pdoc.documentElement.getAttribute("data-md-color-scheme"));
      if (scheme === "slate") return "dark";
      if (scheme === "default") return "light";
    } catch (e) {}
    return null;
  }

  function readSystemTheme() {
    return (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) ? "dark" : "light";
  }

  function resolveTheme() {
    return readParentScheme() || readSystemTheme();
  }

  function ensureFallbackStyle() {
    var id = "standalone-dark-fallback";
    if (document.getElementById(id)) return;

    var style = document.createElement("style");
    style.id = id;
    style.textContent = [
      "html[data-theme='dark'], html[data-theme='dark'] :root {",
      "  --white: #111827 !important;",
      "  --card: #111827 !important;",
      "  --surface: #111827 !important;",
      "  --background: #0b1020 !important;",
      "  --bg: #0b1020 !important;",
      "  --light-bg: #1f2937 !important;",
      "  --text-color: #e5e7eb !important;",
      "  --text: #e5e7eb !important;",
      "  --text-light: #cbd5e1 !important;",
      "  --ink: #e5e7eb !important;",
      "  --ink-1: #e5e7eb !important;",
      "  --ink-2: #cbd5e1 !important;",
      "  --primary-color: #e5e7eb !important;",
      "  --primary: #e5e7eb !important;",
      "  --primary-dark: #cbd5e1 !important;",
      "  --secondary: #60a5fa !important;",
      "  --secondary-color: #60a5fa !important;",
      "  --accent: #f59e0b !important;",
      "  --accent-color: #f59e0b !important;",
      "  --border: #374151 !important;",
      "}",
      "html[data-theme='dark'] { color-scheme: dark; }",
      "html[data-theme='dark'] body { background: #0b1020 !important; color: #e5e7eb !important; }",
      "html[data-theme='dark'] .container, html[data-theme='dark'] main, html[data-theme='dark'] section, html[data-theme='dark'] article, html[data-theme='dark'] aside, html[data-theme='dark'] nav, html[data-theme='dark'] header, html[data-theme='dark'] footer, html[data-theme='dark'] .content, html[data-theme='dark'] .card, html[data-theme='dark'] .panel, html[data-theme='dark'] .box, html[data-theme='dark'] .wrapper { background: #111827 !important; color: #e5e7eb !important; }",
      "html[data-theme='dark'] .learning-outcomes, html[data-theme='dark'] .clo-box, html[data-theme='dark'] .highlight, html[data-theme='dark'] .key-point, html[data-theme='dark'] .warning, html[data-theme='dark'] .principle, html[data-theme='dark'] .timeline-item, html[data-theme='dark'] .stat-card, html[data-theme='dark'] .metric-card, html[data-theme='dark'] .summary-card { background: #1f2937 !important; color: #e5e7eb !important; border-color: #374151 !important; }",
      "html[data-theme='dark'] h1, html[data-theme='dark'] h2, html[data-theme='dark'] h3, html[data-theme='dark'] h4, html[data-theme='dark'] h5, html[data-theme='dark'] h6, html[data-theme='dark'] p, html[data-theme='dark'] li, html[data-theme='dark'] dt, html[data-theme='dark'] dd, html[data-theme='dark'] span, html[data-theme='dark'] div, html[data-theme='dark'] label { color: #e5e7eb !important; }",
      "html[data-theme='dark'] a { color: #c4b5fd !important; }",
      "html[data-theme='dark'] table { background: #0f172a !important; color: #e5e7eb !important; }",
      "html[data-theme='dark'] th { background: #1f2937 !important; color: #f8fafc !important; }",
      "html[data-theme='dark'] td { background: #111827 !important; color: #e5e7eb !important; border-color: #374151 !important; }",
      "html[data-theme='dark'] pre, html[data-theme='dark'] code, html[data-theme='dark'] .formula { background: #111827 !important; color: #e5e7eb !important; border-color: #374151 !important; }",
      "html[data-theme='dark'] input, html[data-theme='dark'] textarea, html[data-theme='dark'] select, html[data-theme='dark'] button { background: #1f2937 !important; color: #f8fafc !important; border-color: #4b5563 !important; }"
    ].join("\n");

    (document.head || document.documentElement).appendChild(style);
  }

  function applyTheme(theme) {
    var dark = theme === "dark";
    root.setAttribute("data-theme", dark ? "dark" : "light");
    root.classList.toggle("dark", dark);
    root.classList.toggle("light", !dark);

    if (document.body) {
      document.body.classList.toggle("dark", dark);
      document.body.classList.toggle("light", !dark);
    }
  }

  function sync() {
    ensureFallbackStyle();
    applyTheme(resolveTheme());
  }

  sync();
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", sync);
  }

  var media = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;
  if (media) {
    if (media.addEventListener) media.addEventListener("change", sync);
    else if (media.addListener) media.addListener(sync);
  }

  if (window.MutationObserver) {
    try {
      var pdoc = window.parent && window.parent.document;
      var parentBody = pdoc && pdoc.body;
      if (parentBody) {
        new MutationObserver(sync).observe(parentBody, {
          attributes: true,
          attributeFilter: ["data-md-color-scheme"]
        });
      }
    } catch (e) {}
  }
})();
