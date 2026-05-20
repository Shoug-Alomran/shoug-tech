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

  function applyMode(mode) {
    mode = mode === DARK ? DARK : LIGHT;
    lastMode = mode;

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
