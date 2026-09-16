/* Progressive disclosure for long lesson contents lists. Existing toggles stay in charge. */
(function () {
  "use strict";
  function init() {
    var selector = ".toc, .table-of-contents, .chapter-toc, .toc-rail, .toc-bar, .toc-strip, .toc-pills, .toc-grid";
    document.querySelectorAll(selector).forEach(function (toc) {
      if (toc.closest("details, .bd-contents, .bdx-toc") ||
          toc.querySelector("button[aria-expanded], .toc-toggle") ||
          (toc.parentElement && toc.parentElement.closest(selector))) return;
      var links = toc.querySelectorAll('a[href^="#"]');
      if (links.length < 5) return;
      var rect = toc.getBoundingClientRect();
      var style = getComputedStyle(toc);
      // Fixed sidebars already have their own page navigation behavior.
      if (style.position === "fixed") return;
      var details = document.createElement("details");
      details.className = "bd-contents";
      details.style.setProperty("--bd-contents-display", style.display === "none" ? "block" : style.display);
      var summary = document.createElement("summary");
      summary.className = "bd-contents-summary";
      summary.textContent = "Contents · " + links.length + " topics";
      details.open = rect.height > 0 && rect.height <= 160 && window.innerWidth > 768;
      toc.replaceWith(details);
      details.appendChild(summary);
      details.appendChild(toc);
      toc.classList.add("bd-contents-body");
      toc.addEventListener("click", function (event) {
        var link = event.target.closest('a[href^="#"]');
        if (!link) return;
        // Close before native anchor scrolling calculates the new target position.
        details.open = false;
        summary.focus({ preventScroll: true });
      });
      details.addEventListener("keydown", function (event) {
        if (event.key === "Escape" && details.open) {
          details.open = false;
          summary.focus({ preventScroll: true });
        }
      });
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
