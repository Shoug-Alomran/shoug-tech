(function () {
  "use strict";

  var DARK = "dark";
  var LIGHT = "light";
  var lastMode = null;

  function normalizeScheme(value) {
    if (!value) return null;
    value = String(value).toLowerCase();
    if (value === "slate" || value === DARK) return DARK;
    if (value === "default" || value === LIGHT) return LIGHT;
    return null;
  }

  function modeFromPalette() {
    try {
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

  function ensureContrastStyle() {
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
        --muted: #cbd5e1 !important;
        --primary-color: #f8fafc !important;
        --secondary-color: #93c5fd !important;
        --accent-color: #c4b5fd !important;
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
      html[data-theme="dark"] nav,
      html[data-theme="dark"] header,
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
      html[data-theme="dark"] [style*="linear-gradient"] {
        background: #111827 !important;
        color: #e5e7eb !important;
        border-color: #374151 !important;
      }

      html[data-theme="dark"] header,
      html[data-theme="dark"] .hero,
      html[data-theme="dark"] .title-section,
      html[data-theme="dark"] .cover {
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
    `;

    (document.head || document.documentElement).appendChild(style);
  }

  function applyMode(mode) {
    mode = mode === DARK ? DARK : LIGHT;
    lastMode = mode;
    ensureContrastStyle();

    document.documentElement.setAttribute("data-theme", mode);
    document.documentElement.setAttribute(
      "data-md-color-scheme",
      mode === DARK ? "slate" : "default"
    );
    document.documentElement.style.colorScheme = mode;

    if (document.body) {
      document.body.setAttribute("data-theme", mode);
      document.body.setAttribute(
        "data-md-color-scheme",
        mode === DARK ? "slate" : "default"
      );
      document.body.classList.toggle("parent-dark", mode === DARK);
      document.body.classList.toggle("parent-light", mode !== DARK);
    }

    setButtonState(mode);
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
        attributeFilter: ["data-md-color-scheme"]
      });
    } catch (e) {}
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
      } catch (e) {}
      applyMode(next);
    };
  }

  installToggle();

  syncTheme();

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      installToggle();
      syncTheme();
    }, { once: true });
  } else {
    installToggle();
    syncTheme();
  }

  bindParentObserver();

  window.addEventListener("load", function () {
    installToggle();
    syncTheme();
  });

  window.addEventListener("storage", function (event) {
    if (!event.key || event.key === "__palette" || event.key === "theme") {
      syncTheme();
    }
  });

  if (window.matchMedia) {
    var media = window.matchMedia("(prefers-color-scheme: dark)");
    if (media.addEventListener) media.addEventListener("change", syncTheme);
    else if (media.addListener) media.addListener(syncTheme);
  }
})();
