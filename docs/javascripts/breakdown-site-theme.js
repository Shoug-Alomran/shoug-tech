/**
 * Keep a standalone breakdown's own palette in step with the site theme.
 *
 * Breakdowns such as ISC213's carry their own light and dark palettes and an
 * applyTheme(name) function. The generic dark-mode scripts (standalone-theme.js,
 * html-theme-sync.js) repaint pages with forced colours instead, which clashes
 * with those palettes: the page went dark while its callouts stayed light.
 *
 * This script only decides which of the page's own themes to show:
 *   - the site page around the iframe (body.shoug-light-mode means light),
 *   - else the saved site choice (localStorage "shoug-theme"),
 *   - else dark, the site default.
 * It follows later changes in the parent page or another tab, and saves the
 * page's own toggle so the rest of the site matches.
 *
 * Load it at the end of <body>, after the page script that defines applyTheme.
 */
(function () {
  "use strict";

  var root = document.documentElement;

  function valid(theme) {
    return theme === "dark" || theme === "light" ? theme : null;
  }

  function parentDocument() {
    try {
      if (window.parent && window.parent !== window)
        return window.parent.document;
    } catch (e) {}
    return null;
  }

  function parentTheme() {
    var doc = parentDocument();
    if (!doc || !doc.body) return null;
    return doc.body.classList.contains("shoug-light-mode") ? "light" : "dark";
  }

  function savedTheme() {
    try {
      return valid(localStorage.getItem("shoug-theme"));
    } catch (e) {
      return null;
    }
  }

  function siteTheme() {
    return parentTheme() || savedTheme() || "dark";
  }

  function apply(theme) {
    if (!valid(theme)) return;
    if (typeof window.applyTheme === "function") window.applyTheme(theme);
    else root.setAttribute("data-theme", theme);
  }

  apply(siteTheme());

  // The page's own toggle: remember the choice site-wide.
  var toggle = document.getElementById("themeToggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var now = valid(root.getAttribute("data-theme"));
      if (!now) return;
      try {
        localStorage.setItem("shoug-theme", now);
      } catch (e) {}
    });
  }

  // Another tab changed the site theme.
  window.addEventListener("storage", function (event) {
    if (event.key === "shoug-theme" && valid(event.newValue))
      apply(event.newValue);
  });

  // The site page around this iframe changed theme.
  var doc = parentDocument();
  if (doc && doc.body && window.MutationObserver) {
    new MutationObserver(function () {
      var theme = parentTheme();
      if (theme && theme !== root.getAttribute("data-theme")) apply(theme);
    }).observe(doc.body, { attributes: true, attributeFilter: ["class"] });
  }
})();
