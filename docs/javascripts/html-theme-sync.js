(function () {
  "use strict";

  var DARK = "dark";
  var LIGHT = "light";
  var lastMode = null;
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

      html,
      body {
        max-width: 100%;
        overflow-x: hidden;
      }

      img,
      svg,
      canvas,
      video,
      table,
      pre {
        max-width: 100%;
      }

      table {
        display: block;
        overflow-x: auto;
      }

      .sg-page-search {
        position: fixed;
        z-index: 9999;
        top: max(0.85rem, env(safe-area-inset-top));
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
    } catch (e) {}
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

  installToggle();

  syncTheme();

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      installToggle();
      syncTheme();
      installSearch();
      bindDynamicHeight();
    }, { once: true });
  } else {
    installToggle();
    syncTheme();
    installSearch();
    bindDynamicHeight();
  }

  bindParentObserver();

  window.addEventListener("load", function () {
    installToggle();
    syncTheme();
    installSearch();
    postHeightToParent();
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
