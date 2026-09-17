/* Slide diagrams embedded by scripts/embed_slide_figures.py: click a figure to
   see it full size. Without JavaScript the figures still show inline. */
(function () {
  "use strict";

  function init() {
    var zooms = document.querySelectorAll(".sfx-zoom");
    if (!zooms.length || typeof HTMLDialogElement !== "function") return;
    var box = document.createElement("dialog");
    box.className = "sfx-lightbox";
    box.innerHTML =
      '<button type="button" class="sfx-lightbox-close">Close</button><img alt="" />';
    document.body.appendChild(box);
    var img = box.querySelector("img");
    box
      .querySelector(".sfx-lightbox-close")
      .addEventListener("click", function () {
        box.close();
      });
    // A click on the backdrop lands on the dialog itself.
    box.addEventListener("click", function (e) {
      if (e.target === box) box.close();
    });
    Array.prototype.forEach.call(zooms, function (btn) {
      btn.addEventListener("click", function () {
        var source = btn.querySelector("img");
        img.src = source.currentSrc || source.src;
        img.alt = source.alt;
        box.showModal();
      });
    });
  }

  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", init);
  else init();
})();
