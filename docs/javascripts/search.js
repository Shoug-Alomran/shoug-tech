(function () {
  "use strict";

  var INDEX_URL = "/search-index.json";
  var index = null;
  var modal = null;
  var input = null;
  var results = null;
  var activeIdx = -1;

  var SECTION_LABELS = {
    academics: "Academics",
    work: "Work",
    workshops: "Workshops",
    resources: "Resources",
    about: "About",
    "academic-plan-themes": "Academic Plan",
    policy: "Policy",
    "career-development": "Career",
  };

  function sectionLabel(s) {
    return SECTION_LABELS[s] || s;
  }

  function injectStyles() {
    if (document.getElementById("shoug-search-styles")) return;
    var style = document.createElement("style");
    style.id = "shoug-search-styles";
    style.textContent = [
      "#shoug-search-backdrop{position:fixed;inset:0;z-index:99999;background:rgba(0,0,0,0.7);backdrop-filter:blur(6px);display:flex;align-items:flex-start;justify-content:center;padding-top:80px;opacity:0;transition:opacity 150ms ease}",
      "#shoug-search-backdrop.is-open{opacity:1}",
      "#shoug-search-box{width:min(640px,calc(100vw - 32px));background:#0a0514;border:1px solid rgba(184,41,234,0.4);font-family:'JetBrains Mono',monospace;display:flex;flex-direction:column;max-height:calc(100vh - 120px);box-shadow:0 0 60px rgba(184,41,234,0.15)}",
      "#shoug-search-top{display:flex;align-items:center;gap:10px;padding:14px 16px;border-bottom:1px solid rgba(255,255,255,0.06)}",
      "#shoug-search-top svg{flex-shrink:0;color:#b829ea}",
      "#shoug-search-input{flex:1;background:transparent;border:none;outline:none;color:#f8f7fb;font-family:'JetBrains Mono',monospace;font-size:0.9rem;letter-spacing:0.02em}",
      "#shoug-search-input::placeholder{color:#4a4258}",
      "#shoug-search-kbd{font-size:0.6rem;color:#4a4258;border:1px solid #2a1b40;padding:2px 6px;letter-spacing:0.08em;flex-shrink:0}",
      "#shoug-search-results{overflow-y:auto;max-height:420px}",
      "#shoug-search-results::-webkit-scrollbar{width:4px}",
      "#shoug-search-results::-webkit-scrollbar-track{background:transparent}",
      "#shoug-search-results::-webkit-scrollbar-thumb{background:#2a1b40}",
      ".shoug-sr-section{padding:8px 16px 4px;font-size:0.6rem;color:#b829ea;letter-spacing:0.18em;text-transform:uppercase;border-top:1px solid rgba(255,255,255,0.04)}",
      ".shoug-sr-section:first-child{border-top:none}",
      ".shoug-sr-item{display:flex;flex-direction:column;gap:2px;padding:10px 16px;cursor:pointer;text-decoration:none;color:inherit;transition:background 100ms ease}",
      ".shoug-sr-item:hover,.shoug-sr-item.active{background:rgba(184,41,234,0.1)}",
      ".shoug-sr-item.active{border-left:2px solid #b829ea;padding-left:14px}",
      ".shoug-sr-title{font-size:0.82rem;color:#f8f7fb;font-weight:700;letter-spacing:0.02em}",
      ".shoug-sr-desc{font-size:0.68rem;color:#6d6478;letter-spacing:0.02em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-family:'Inter',sans-serif}",
      ".shoug-sr-url{font-size:0.62rem;color:#4a4258;letter-spacing:0.04em}",
      ".shoug-sr-empty{padding:32px 16px;text-align:center;color:#4a4258;font-size:0.78rem;letter-spacing:0.08em}",
      "#shoug-search-footer{padding:8px 16px;border-top:1px solid rgba(255,255,255,0.04);display:flex;gap:16px;font-size:0.6rem;color:#4a4258;letter-spacing:0.06em}",
      "#shoug-search-footer span{display:flex;align-items:center;gap:6px}",
      ".shoug-search-key{border:1px solid #2a1b40;padding:1px 5px;font-family:'JetBrains Mono',monospace}",
      "mark.shoug-hl{background:transparent;color:#b829ea;font-weight:700}",
    ].join("");
    document.head.appendChild(style);
  }

  function buildModal() {
    if (modal) return;

    injectStyles();

    modal = document.createElement("div");
    modal.id = "shoug-search-backdrop";
    modal.setAttribute("role", "dialog");
    modal.setAttribute("aria-modal", "true");
    modal.setAttribute("aria-label", "Site search");

    modal.innerHTML = [
      '<div id="shoug-search-box">',
      '  <div id="shoug-search-top">',
      '    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg>',
      '    <input id="shoug-search-input" type="text" placeholder="Search pages, courses, projects..." autocomplete="off" spellcheck="false" aria-label="Search query">',
      '    <span id="shoug-search-kbd">ESC</span>',
      '  </div>',
      '  <div id="shoug-search-results" role="listbox" aria-label="Search results"></div>',
      '  <div id="shoug-search-footer">',
      '    <span><kbd class="shoug-search-key">↑↓</kbd> navigate</span>',
      '    <span><kbd class="shoug-search-key">↵</kbd> open</span>',
      '    <span><kbd class="shoug-search-key">ESC</kbd> close</span>',
      '  </div>',
      '</div>',
    ].join("");

    document.body.appendChild(modal);

    input = document.getElementById("shoug-search-input");
    results = document.getElementById("shoug-search-results");

    modal.addEventListener("click", function (e) {
      if (e.target === modal) closeSearch();
    });

    input.addEventListener("input", function () {
      activeIdx = -1;
      renderResults(input.value.trim());
    });

    input.addEventListener("keydown", handleKey);
  }

  function highlight(text, query) {
    if (!query) return escHtml(text);
    var escaped = query.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    return escHtml(text).replace(
      new RegExp("(" + escaped + ")", "gi"),
      '<mark class="shoug-hl">$1</mark>'
    );
  }

  function escHtml(s) {
    return s
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function score(item, q) {
    var lq = q.toLowerCase();
    var lt = item.title.toLowerCase();
    var lu = item.url.toLowerCase();
    var ld = item.description.toLowerCase();
    if (lt === lq) return 100;
    if (lt.startsWith(lq)) return 80;
    if (lu.includes(lq)) return 70;
    if (lt.includes(lq)) return 60;
    if (ld.includes(lq)) return 40;
    // word-level partial match
    var words = lq.split(/\s+/);
    var hits = words.filter(function (w) {
      return lt.includes(w) || lu.includes(w) || ld.includes(w);
    }).length;
    return hits > 0 ? (hits / words.length) * 30 : -1;
  }

  function search(q) {
    if (!q || q.length < 2) return [];
    var scored = index
      .map(function (item) { return { item: item, s: score(item, q) }; })
      .filter(function (x) { return x.s > 0; })
      .sort(function (a, b) { return b.s - a.s; });
    return scored.slice(0, 24).map(function (x) { return x.item; });
  }

  function renderResults(q) {
    if (!q || q.length < 2) {
      results.innerHTML = '<div class="shoug-sr-empty">Type to search 681 pages&hellip;</div>';
      return;
    }
    var matches = search(q);
    if (!matches.length) {
      results.innerHTML = '<div class="shoug-sr-empty">No results for &ldquo;' + escHtml(q) + '&rdquo;</div>';
      return;
    }

    var grouped = {};
    var order = [];
    matches.forEach(function (item) {
      var s = item.section || "other";
      if (!grouped[s]) { grouped[s] = []; order.push(s); }
      grouped[s].push(item);
    });

    var html = "";
    var itemIdx = 0;
    order.forEach(function (section) {
      html += '<div class="shoug-sr-section">' + escHtml(sectionLabel(section)) + '</div>';
      grouped[section].forEach(function (item) {
        html += [
          '<a class="shoug-sr-item" href="' + escHtml(item.url) + '" data-idx="' + itemIdx + '" role="option">',
          '  <span class="shoug-sr-title">' + highlight(item.title, q) + '</span>',
          item.description ? '  <span class="shoug-sr-desc">' + highlight(item.description.slice(0, 120), q) + '</span>' : '',
          '  <span class="shoug-sr-url">' + escHtml(item.url) + '</span>',
          '</a>',
        ].join("");
        itemIdx++;
      });
    });

    results.innerHTML = html;
  }

  function getItems() {
    return results.querySelectorAll(".shoug-sr-item");
  }

  function setActive(idx) {
    var items = getItems();
    if (!items.length) return;
    activeIdx = Math.max(0, Math.min(items.length - 1, idx));
    items.forEach(function (el, i) {
      el.classList.toggle("active", i === activeIdx);
    });
    if (items[activeIdx]) {
      items[activeIdx].scrollIntoView({ block: "nearest" });
    }
  }

  function handleKey(e) {
    var items = getItems();
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setActive(activeIdx + 1);
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setActive(activeIdx - 1);
    } else if (e.key === "Enter") {
      e.preventDefault();
      if (activeIdx >= 0 && items[activeIdx]) {
        window.location.href = items[activeIdx].getAttribute("href");
      } else if (items[0]) {
        window.location.href = items[0].getAttribute("href");
      }
    } else if (e.key === "Escape") {
      closeSearch();
    }
  }

  function openSearch() {
    buildModal();
    modal.style.display = "flex";
    requestAnimationFrame(function () {
      modal.classList.add("is-open");
    });
    results.innerHTML = '<div class="shoug-sr-empty">Type to search 681 pages&hellip;</div>';
    input.value = "";
    activeIdx = -1;
    input.focus();
    document.body.style.overflow = "hidden";

    if (!index) {
      fetch(INDEX_URL)
        .then(function (r) { return r.json(); })
        .then(function (data) {
          index = data;
          if (input.value.trim().length >= 2) renderResults(input.value.trim());
        })
        .catch(function () {
          results.innerHTML = '<div class="shoug-sr-empty">Search index unavailable.</div>';
        });
    }
  }

  function closeSearch() {
    if (!modal) return;
    modal.classList.remove("is-open");
    document.body.style.overflow = "";
    setTimeout(function () {
      modal.style.display = "none";
    }, 150);
  }

  function init() {
    // Intercept all search icon links (href contains ?q= or aria-label="Search")
    document.addEventListener("click", function (e) {
      var link = e.target.closest('a[aria-label="Search"], a[href*="?q="]');
      if (!link) return;
      e.preventDefault();
      openSearch();
    });

    // Keyboard shortcut: / or Ctrl+K / Cmd+K
    document.addEventListener("keydown", function (e) {
      if (modal && modal.classList.contains("is-open")) return;
      var tag = document.activeElement && document.activeElement.tagName;
      if (tag === "INPUT" || tag === "TEXTAREA") return;

      if (
        e.key === "/" ||
        ((e.ctrlKey || e.metaKey) && e.key === "k")
      ) {
        e.preventDefault();
        openSearch();
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
