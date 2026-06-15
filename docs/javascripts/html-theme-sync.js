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

  function preferredMode() {
    try {
      var saved = localStorage.getItem("shoug-theme") || localStorage.getItem("theme");
      if (saved === DARK || saved === LIGHT) return saved;
    } catch (e) { }

    return window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches
      ? DARK
      : LIGHT;
  }

  function setButtonState(mode) {
    var icon = document.getElementById("themeIcon");
    if (icon) icon.textContent = mode === DARK ? "☀️" : "🌙";

    var labels = document.querySelectorAll("[data-theme-label]");
    labels.forEach(function (label) {
      label.textContent = mode === DARK ? "Light" : "Dark";
    });
  }

  function ensureStyles() {
    if (document.getElementById("html-theme-sync-styles")) return;

    var style = document.createElement("style");
    style.id = "html-theme-sync-styles";
    style.textContent = `
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
        display: flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.35rem;
        border: 1px solid rgba(148, 163, 184, 0.35);
        border-radius: 999px;
        background: rgba(15, 23, 42, 0.88);
        color: #f8fafc;
        max-width: 34rem;
        backdrop-filter: blur(14px);
      }

      body > .sg-page-search {
        position: fixed;
        z-index: 9999;
        bottom: max(0.85rem, env(safe-area-inset-bottom));
        right: max(0.85rem, env(safe-area-inset-right));
        box-shadow: 0 16px 42px rgba(15, 23, 42, 0.24);
        max-width: min(34rem, calc(100vw - 1.7rem));
      }

      header .sg-page-search,
      nav .sg-page-search,
      .header-search .sg-page-search,
      [data-page-search-host] .sg-page-search {
        position: static !important;
        inset: auto !important;
        margin: 0 !important;
        box-shadow: none !important;
        max-width: 100% !important;
        background: var(--bg2, var(--surface2, rgba(15, 23, 42, 0.88))) !important;
        border-color: var(--border, rgba(148, 163, 184, 0.35)) !important;
      }

      .sg-page-search__input {
        width: clamp(8rem, 16vw, 14rem);
        min-width: 0;
        height: 2rem;
        border: 0;
        border-radius: 999px;
        padding: 0 0.8rem;
        background: rgba(255, 255, 255, 0.96);
        color: #0f172a;
        font: 600 0.82rem/1.2 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        outline: none;
      }

      header .sg-page-search__input,
      nav .sg-page-search__input,
      .header-search .sg-page-search__input,
      [data-page-search-host] .sg-page-search__input {
        width: clamp(7rem, 14vw, 12rem);
        background: var(--bg3, var(--surface, rgba(255, 255, 255, 0.96))) !important;
        color: var(--text, #0f172a) !important;
        border: 1px solid var(--border, rgba(148, 163, 184, 0.35)) !important;
      }

      .sg-page-search__input::placeholder {
        color: #64748b;
      }

      .sg-page-search__count {
        min-width: 2.8rem;
        text-align: center;
        font: 700 0.7rem/1 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        color: #e2e8f0;
      }

      header .sg-page-search__count,
      nav .sg-page-search__count,
      .header-search .sg-page-search__count,
      [data-page-search-host] .sg-page-search__count {
        color: var(--text2, var(--text-muted, #e2e8f0)) !important;
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

      header .sg-page-search__button,
      nav .sg-page-search__button,
      .header-search .sg-page-search__button,
      [data-page-search-host] .sg-page-search__button {
        background: var(--bg3, var(--surface, rgba(255, 255, 255, 0.12))) !important;
        color: var(--text, #f8fafc) !important;
        border: 1px solid var(--border, rgba(148, 163, 184, 0.35)) !important;
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
      }

      .sg-theme-toggle:hover {
        transform: scale(1.08);
      }

      @media (max-width: 760px) {
        .sg-table-scroll > table {
          width: max-content;
        }

        header .sg-page-search,
        nav .sg-page-search,
        .header-search .sg-page-search,
        [data-page-search-host] .sg-page-search {
          max-width: 100%;
        }

        header .sg-page-search__input,
        nav .sg-page-search__input,
        .header-search .sg-page-search__input,
        [data-page-search-host] .sg-page-search__input {
          width: 6rem;
        }

        header .sg-page-search__count,
        nav .sg-page-search__count,
        .header-search .sg-page-search__count,
        [data-page-search-host] .sg-page-search__count {
          display: none;
        }
      }

      @media (max-width: 640px) {
        body > .sg-page-search {
          left: 0.75rem;
          right: 0.75rem;
          border-radius: 0.9rem;
        }

        body > .sg-page-search .sg-page-search__input {
          flex: 1 1 auto;
          width: auto;
        }
      }
    `;

    document.head.appendChild(style);
  }

  function applyMode(mode) {
    mode = mode === DARK ? DARK : LIGHT;
    lastMode = mode;

    ensureStyles();

    document.documentElement.setAttribute("data-theme", mode);
    document.documentElement.setAttribute(
      "data-md-color-scheme",
      mode === DARK ? "slate" : "default"
    );
    document.documentElement.classList.toggle("dark", mode === DARK);
    document.documentElement.classList.toggle("light", mode === LIGHT);
    document.documentElement.style.colorScheme = mode;

    if (document.body) {
      document.body.setAttribute("data-theme", mode);
      document.body.setAttribute(
        "data-md-color-scheme",
        mode === DARK ? "slate" : "default"
      );
      document.body.classList.toggle("dark", mode === DARK);
      document.body.classList.toggle("light", mode === LIGHT);
      document.body.classList.toggle("shoug-light-mode", mode === LIGHT);
      document.body.classList.toggle("parent-dark", mode === DARK);
      document.body.classList.toggle("parent-light", mode === LIGHT);
    }

    setButtonState(mode);
  }

  function syncTheme() {
    applyMode(preferredMode());
  }

  function installToggle() {
    window.toggleTheme = function () {
      var next = lastMode === DARK ? LIGHT : DARK;

      try {
        localStorage.setItem("theme", next);
        localStorage.setItem("shoug-theme", next);
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
      } catch (e) { }

      applyMode(next);
    };
  }

  function installThemeButton() {
    if (!document.body) return;
    if (document.querySelector(".sg-theme-toggle")) return;
    if (document.querySelector("#themeToggle, #themeBtn, .theme-toggle, .shoug-theme-btn")) return;
    if (document.querySelector("[onclick*='toggleTheme']")) return;

    var btn = document.createElement("button");
    btn.className = "sg-theme-toggle";
    btn.id = "themeIcon";
    btn.setAttribute("aria-label", "Toggle dark/light mode");
    btn.textContent = lastMode === DARK ? "☀️" : "🌙";

    document.body.appendChild(btn);

    btn.addEventListener("click", function (event) {
      event.stopPropagation();
      if (typeof window.toggleTheme === "function") window.toggleTheme();
    });
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

    if (document.body) document.body.normalize();
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

    return Boolean(
      parent.closest(
        "script, style, noscript, textarea, input, select, option, button, .sg-page-search, .sg-search-mark"
      )
    );
  }

  function focusSearchResult(offset) {
    if (!searchState.marks.length) {
      updateSearchCount();
      return;
    }

    searchState.marks.forEach(function (mark) {
      mark.classList.remove("is-active");
    });

    searchState.active =
      (searchState.active + offset + searchState.marks.length) %
      searchState.marks.length;

    var active = searchState.marks[searchState.active];
    active.classList.add("is-active");
    active.scrollIntoView({
      behavior: "smooth",
      block: "center",
      inline: "nearest"
    });

    updateSearchCount();
  }

  function runSearch(query) {
    clearSearchMarks();

    searchState.query = String(query || "").trim();

    if (!searchState.query || searchState.query.length < 2 || !document.body) {
      updateSearchCount();
      postHeightToParent();
      return;
    }

    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        if (shouldSkipSearchNode(node)) return NodeFilter.FILTER_REJECT;
        if (!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;

        return node.nodeValue
          .toLowerCase()
          .includes(searchState.query.toLowerCase())
          ? NodeFilter.FILTER_ACCEPT
          : NodeFilter.FILTER_REJECT;
      }
    });

    var nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);

    var pattern = new RegExp("(" + safeTextPattern(searchState.query) + ")", "gi");

    nodes.forEach(function (node) {
      var frag = document.createDocumentFragment();
      var text = node.nodeValue;
      var lastIndex = 0;

      text.replace(pattern, function (match, _group, index) {
        if (index > lastIndex) {
          frag.appendChild(document.createTextNode(text.slice(lastIndex, index)));
        }

        var mark = document.createElement("mark");
        mark.className = "sg-search-mark";
        mark.textContent = match;
        frag.appendChild(mark);
        searchState.marks.push(mark);

        lastIndex = index + match.length;
        return match;
      });

      if (lastIndex < text.length) {
        frag.appendChild(document.createTextNode(text.slice(lastIndex)));
      }

      node.replaceWith(frag);
    });

    searchState.active = searchState.marks.length ? 0 : -1;
    focusSearchResult(0);
    updateSearchCount();
    postHeightToParent();
  }

  function getSearchHost() {
    return (
      document.querySelector("[data-page-search-host]") ||
      document.querySelector(".header-search") ||
      document.querySelector("header .header-actions") ||
      document.querySelector("nav .header-actions") ||
      document.querySelector("header") ||
      document.querySelector("nav")
    );
  }

  function moveSearchToHost() {
    var form = document.querySelector(".sg-page-search");
    if (!form) return;

    var host = getSearchHost();

    if (host && !host.contains(form)) {
      host.appendChild(form);
    }
  }

  function installSearch() {
    if (!document.body) return;

    var existing = document.querySelector(".sg-page-search");
    if (existing) {
      moveSearchToHost();
      return;
    }

    var form = document.createElement("form");
    form.className = "sg-page-search";
    form.setAttribute("role", "search");

    form.innerHTML = [
      '<input class="sg-page-search__input" type="search" placeholder="Search page" aria-label="Search this page" autocomplete="off">',
      '<span class="sg-page-search__count" aria-live="polite">0/0</span>',
      '<button class="sg-page-search__button" type="button" data-search-prev aria-label="Previous result">‹</button>',
      '<button class="sg-page-search__button" type="button" data-search-next aria-label="Next result">›</button>'
    ].join("");

    var host = getSearchHost();

    if (host) {
      host.appendChild(form);
    } else {
      document.body.appendChild(form);
    }

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

  function currentHeight() {
    var body = document.body;
    var root = document.documentElement;

    return Math.ceil(
      Math.max(
        body ? body.scrollHeight : 0,
        body ? body.offsetHeight : 0,
        root ? root.scrollHeight : 0,
        root ? root.offsetHeight : 0
      )
    );
  }

  function postHeightToParent() {
    if (window.parent === window) return;

    try {
      window.parent.postMessage(
        {
          type: "sg:iframe-height",
          path: window.location.pathname,
          height: currentHeight()
        },
        window.location.origin
      );
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

  function bindParentObserver() {
    try {
      if (window.parent === window || !window.parent.document || !window.MutationObserver) return;

      var parentBody = window.parent.document.body;
      if (!parentBody) return;

      new MutationObserver(syncTheme).observe(parentBody, {
        attributes: true,
        attributeFilter: ["data-md-color-scheme", "class"]
      });
    } catch (e) { }
  }

  function bindSelfAttrObserver() {
    if (!window.MutationObserver) return;

    var observer = new MutationObserver(function (mutations) {
      mutations.forEach(function (mutation) {
        if (mutation.attributeName !== "data-theme") return;

        var theme = document.documentElement.getAttribute("data-theme");

        if ((theme === DARK || theme === LIGHT) && theme !== lastMode) {
          lastMode = theme;

          try {
            localStorage.setItem("shoug-theme", theme);
          } catch (e) { }

          setButtonState(theme);
        }
      });
    });

    function attach() {
      observer.observe(document.documentElement, {
        attributes: true,
        attributeFilter: ["data-theme"]
      });
    }

    if (document.readyState === "complete") {
      setTimeout(attach, 200);
    } else {
      window.addEventListener(
        "load",
        function () {
          setTimeout(attach, 200);
        },
        { once: true }
      );
    }
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

  function init() {
    ensureStyles();
    installToggle();
    syncTheme();
    installSearch();
    moveSearchToHost();
    installThemeButton();
    wrapResponsiveTables();
    bindDynamicHeight();
    loadPastExamPractice();
    postHeightToParent();
  }

  installToggle();
  syncTheme();

  if (document.readyState === "loading") {
    document.addEventListener(
      "DOMContentLoaded",
      function () {
        init();
      },
      { once: true }
    );
  } else {
    init();
  }

  window.addEventListener("load", function () {
    init();
    moveSearchToHost();
  });

  window.addEventListener("storage", function (event) {
    if (
      !event.key ||
      event.key === "__palette" ||
      event.key === "theme" ||
      event.key === "shoug-theme"
    ) {
      syncTheme();
    }
  });

  if (window.matchMedia) {
    var media = window.matchMedia("(prefers-color-scheme: dark)");

    if (media.addEventListener) {
      media.addEventListener("change", syncTheme);
    } else if (media.addListener) {
      media.addListener(syncTheme);
    }
  }

  bindParentObserver();
  bindSelfAttrObserver();
})();