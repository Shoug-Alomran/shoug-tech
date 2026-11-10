/**
 * PDF / Word switch for viewer pages that carry a document in both formats.
 * Written by scripts/build_se322_diagram_examples.py.
 *
 * The Word pane fetches Microsoft's viewer only when first opened, so reading
 * the PDF never loads it.
 */
(function () {
  "use strict";

  // Microsoft's viewer can only read files that are live. If the file isn't at
  // its current address yet, show the copy published at its previous one.
  function resolveFrame(frame) {
    var primary = frame.getAttribute("data-frame-src");
    var fallback = frame.getAttribute("data-frame-fallback");
    var file = frame.getAttribute("data-file-url");
    if (!fallback || !file) {
      frame.setAttribute("src", primary);
      return;
    }
    fetch(file, { method: "HEAD", cache: "no-store" })
      .then(function (res) {
        frame.setAttribute("src", res.ok ? primary : fallback);
      })
      .catch(function () {
        frame.setAttribute("src", fallback);
      });
  }

  function init() {
    var host = document.querySelector("[data-format-switch]");
    if (!host) return;
    var buttons = host.querySelectorAll("button[data-format]");
    var action = document.querySelector("a[data-format-action]");

    function show(format, chosen) {
      Array.prototype.forEach.call(buttons, function (btn) {
        var on = btn.getAttribute("data-format") === format;
        btn.setAttribute("aria-pressed", on ? "true" : "false");
        btn.className = "btn " + (on ? "btn-primary" : "btn-secondary");
      });
      Array.prototype.forEach.call(
        document.querySelectorAll("[data-format-pane]"),
        function (pane) {
          pane.hidden = pane.getAttribute("data-format-pane") !== format;
        },
      );
      var pane = document.querySelector('[data-format-pane="' + format + '"]');
      var frame = pane.querySelector("iframe[data-frame-src]");
      if (frame && !frame.getAttribute("src") && !frame.dataset.resolving) {
        frame.dataset.resolving = "true";
        resolveFrame(frame);
      }
      // pdf-embed.js shows a click-to-load card; picking PDF is that click.
      var open = chosen && pane.querySelector("button.pdf-embed__btn");
      if (open) open.click();

      if (!action) return;
      if (format === "word") {
        action.href = action.getAttribute("data-word-href");
        action.textContent = "[ DOWNLOAD WORD FILE ]";
        action.setAttribute("download", "");
        action.removeAttribute("target");
      } else {
        action.href = action.getAttribute("data-pdf-href");
        action.textContent = "[ OPEN IN NEW TAB -> ]";
        action.removeAttribute("download");
        action.setAttribute("target", "_blank");
      }
    }

    Array.prototype.forEach.call(buttons, function (btn) {
      btn.addEventListener("click", function () {
        show(btn.getAttribute("data-format"), true);
      });
    });
    show("pdf", false);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
