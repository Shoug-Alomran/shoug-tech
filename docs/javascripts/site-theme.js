/**
 * Theme follows the device until the visitor picks one, and a theme switch in
 * the phone menu. Added to every page by functions/_middleware.js, which also
 * puts THEME_BOOT (below, inlined there) at the very top of <head>.
 *
 * How "follow the device" works with the site's many theme scripts: they all
 * read localStorage "shoug-theme". The boot script writes the device's mode
 * there and the same value to "shoug-theme-auto". A theme button later writes
 * "shoug-theme" only, so once the two differ the visitor's choice wins and the
 * device is no longer followed.
 */
(function () {
  "use strict";
  if (window.__shougSiteTheme) return;
  window.__shougSiteTheme = true;

  var KEY = "shoug-theme";
  var AUTO = "shoug-theme-auto";
  var mq =
    window.matchMedia && window.matchMedia("(prefers-color-scheme: light)");

  function get(k) {
    try {
      return localStorage.getItem(k);
    } catch (e) {
      return null;
    }
  }
  function set(k, v) {
    try {
      localStorage.setItem(k, v);
    } catch (e) {}
  }
  function following() {
    var auto = get(AUTO);
    return !!auto && get(KEY) === auto;
  }
  function isLight() {
    var root = document.documentElement;
    var t = root.getAttribute("data-theme");
    if (t === "light" || t === "dark") return t === "light";
    return (
      !!document.body && document.body.classList.contains("shoug-light-mode")
    );
  }
  function headerButton() {
    return document.querySelector(".shoug-theme-btn, #shoug-theme-toggle");
  }

  // Switch the page the same way its own theme button would.
  function show(mode) {
    if ((mode === "light") === isLight()) return;
    var btn = headerButton();
    if (btn) return btn.click();
    var root = document.documentElement;
    if (root.hasAttribute("data-theme")) root.setAttribute("data-theme", mode);
    if (document.body)
      document.body.classList.toggle("shoug-light-mode", mode === "light");
    set(KEY, mode);
  }

  // The device switched (e.g. automatic dark mode at sunset).
  if (mq) {
    var onChange = function () {
      if (!following()) return;
      var mode = mq.matches ? "light" : "dark";
      set(KEY, mode);
      set(AUTO, mode);
      show(mode);
    };
    if (mq.addEventListener) mq.addEventListener("change", onChange);
    else if (mq.addListener) mq.addListener(onChange);
  }

  // ---------------------------------------------------- phone menu switch --
  // site-shell.css hides the header theme button under 560px; this puts a
  // switch inside the menu drawer at those widths.
  function label() {
    return isLight() ? "Dark mode" : "Light mode";
  }
  function addMenuSwitch() {
    var navs = document.querySelectorAll(".shoug-header-nav");
    if (!navs.length) return;
    var css = document.createElement("style");
    css.textContent =
      ".shoug-menu-theme{display:none}" +
      "@media (max-width:560px){.shoug-header-nav .shoug-menu-theme{display:inline-flex;align-items:center;gap:8px;" +
      "font:inherit;font-size:inherit;letter-spacing:inherit;text-transform:inherit;color:inherit;background:transparent;" +
      "border:1px solid currentColor;border-radius:999px;padding:8px 14px;cursor:pointer;opacity:.9}}" +
      ".shoug-menu-theme svg{width:15px;height:15px}";
    document.head.appendChild(css);
    navs.forEach(function (nav) {
      if (nav.querySelector(".shoug-menu-theme")) return;
      var b = document.createElement("button");
      b.type = "button";
      b.className = "shoug-menu-theme";
      var paint = function () {
        b.textContent = "";
        var icon = document.createElementNS(
          "http://www.w3.org/2000/svg",
          "svg",
        );
        icon.setAttribute("viewBox", "0 0 24 24");
        icon.setAttribute("fill", "none");
        icon.setAttribute("stroke", "currentColor");
        icon.setAttribute("stroke-width", "2");
        icon.setAttribute("aria-hidden", "true");
        icon.innerHTML = isLight()
          ? '<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>'
          : '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>';
        b.appendChild(icon);
        b.appendChild(document.createTextNode(label()));
        b.setAttribute("aria-label", "Switch to " + label().toLowerCase());
      };
      b.addEventListener("click", function () {
        var next = isLight() ? "dark" : "light";
        var btn = headerButton();
        if (btn) btn.click();
        else show(next);
        // A button press is a choice: stop following the device.
        set(KEY, next);
        try {
          localStorage.removeItem(AUTO);
        } catch (e) {}
        setTimeout(paint, 50);
      });
      paint();
      // Match the menu's own links (font, size, spacing, capitals, colour).
      var link = nav.querySelector("a");
      if (link) {
        var cs = getComputedStyle(link);
        [
          "fontFamily",
          "fontSize",
          "fontWeight",
          "letterSpacing",
          "textTransform",
        ].forEach(function (p) {
          b.style[p] = cs[p];
        });
      }
      new MutationObserver(paint).observe(document.documentElement, {
        attributes: true,
        attributeFilter: ["data-theme"],
      });
      if (document.body)
        new MutationObserver(paint).observe(document.body, {
          attributes: true,
          attributeFilter: ["class"],
        });
      nav.appendChild(b);
    });
  }
  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", addMenuSwitch);
  else addMenuSwitch();
})();
