/* ==========================================================================
   Study guide enhancements for generated slide breakdowns (CYS403).
   Paired with /styles/study-guide.css. Everything here is progressive:
   without JavaScript the page shows all content, unanimated.
     · reading-progress bar
     · scroll-reveal for sections and cards (skipped with reduced motion)
     · floating "Contents" panel with the current section highlighted
     · flip-to-reveal flashcards
   ========================================================================== */
(function () {
  "use strict";

  var root = document.documentElement;
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function onReady(fn) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  }

  function progressBar() {
    var bar = document.createElement("div");
    bar.className = "bdx-progress";
    bar.setAttribute("aria-hidden", "true");
    bar.innerHTML = "<i></i>";
    // Sits on the bottom edge of the sticky header when there is one.
    (document.querySelector(".bdx-bar") || document.body).appendChild(bar);
    var fill = bar.firstChild;
    var ticking = false;
    function update() {
      ticking = false;
      var max = document.documentElement.scrollHeight - window.innerHeight;
      var pct = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
      fill.style.transform = "scaleX(" + pct + ")";
    }
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    update();
  }

  var REVEAL = [
    "main > section", ".def-card", ".step", ".tip", ".mnemonic", ".flow", ".vs > .ex",
    ".tbl-wrap", ".bdx-card", ".mono", "main ul > li"
  ].join(",");

  function stagger(el) {
    // Siblings of the same kind cascade in so grids and lists ripple.
    var index = 0, sib = el.previousElementSibling;
    while (sib && index < 8) {
      if (sib.className === el.className && sib.tagName === el.tagName) index++;
      sib = sib.previousElementSibling;
    }
    el.style.setProperty("--bdx-i", index);
  }

  function reveal() {
    if (reduceMotion) return;
    var items = Array.prototype.slice.call(document.querySelectorAll(REVEAL));
    var fold = (window.innerHeight || document.documentElement.clientHeight) * 0.9;
    // Only content below the fold waits to animate in; anything visible at load shows at once.
    var pending = items.filter(function (el) { return el.getBoundingClientRect().top > fold; });
    if (!pending.length) return;
    pending.forEach(function (el) { stagger(el); el.classList.add("bdx-wait"); });
    root.classList.add("bdx-anim");

    function show(el) {
      el.classList.remove("bdx-wait");
      el.classList.add("bdx-in");
    }
    // Reveal by position rather than intersection events, so elements scrolled
    // past (contents-panel jumps, #links) or never "intersecting" still appear.
    function sweep() {
      var limit = (window.innerHeight || document.documentElement.clientHeight) * 0.92;
      pending = pending.filter(function (el) {
        if (el.getBoundingClientRect().top < limit) { show(el); return false; }
        return true;
      });
      if (!pending.length) {
        window.removeEventListener("scroll", queue);
        window.removeEventListener("resize", queue);
      }
    }
    var queued = false;
    function queue() {
      if (queued) return;
      queued = true;
      requestAnimationFrame(function () { queued = false; sweep(); });
    }
    window.addEventListener("scroll", queue, { passive: true });
    window.addEventListener("resize", queue);
    window.addEventListener("hashchange", queue);
    window.addEventListener("beforeprint", function () { pending.forEach(show); pending = []; });
    sweep();
  }

  function contents() {
    var sections = document.querySelectorAll("main > section[id]");
    var panel = document.querySelector(".bdx-toc");
    if (!sections.length || !panel) return;
    var toggle = panel.querySelector(".bdx-toc-toggle");
    var counter = panel.querySelector(".bdx-toc-count");
    var links = panel.querySelectorAll("a[href^='#']");

    function setOpen(open) {
      panel.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    }
    toggle.addEventListener("click", function () { setOpen(!panel.classList.contains("is-open")); });
    Array.prototype.forEach.call(links, function (a) {
      a.addEventListener("click", function () { setOpen(false); });
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") setOpen(false); });
    document.addEventListener("click", function (e) { if (!panel.contains(e.target)) setOpen(false); });

    function activate(id) {
      var n = 0;
      Array.prototype.forEach.call(links, function (a, i) {
        var on = a.getAttribute("href") === "#" + id;
        a.classList.toggle("is-active", on);
        if (on) { a.setAttribute("aria-current", "true"); n = i + 1; } else { a.removeAttribute("aria-current"); }
      });
      if (counter && n) counter.textContent = (n < 10 ? "0" : "") + n + " / " + (links.length < 10 ? "0" : "") + links.length;
    }
    if ("IntersectionObserver" in window) {
      var spy = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) { if (entry.isIntersecting) activate(entry.target.id); });
      }, { rootMargin: "-35% 0px -60% 0px" });
      Array.prototype.forEach.call(sections, function (s) { spy.observe(s); });
    }
    activate(sections[0].id);
  }

  function flashcards() {
    Array.prototype.forEach.call(document.querySelectorAll(".bdx-card"), function (card) {
      card.addEventListener("click", function () {
        var flipped = card.classList.toggle("is-flipped");
        card.setAttribute("aria-pressed", flipped ? "true" : "false");
      });
    });
    var shuffle = document.querySelector(".bdx-shuffle");
    var deck = document.querySelector(".bdx-deck");
    if (shuffle && deck) {
      shuffle.addEventListener("click", function () {
        var cards = Array.prototype.slice.call(deck.children);
        cards.forEach(function (c) { c.classList.remove("is-flipped"); c.setAttribute("aria-pressed", "false"); });
        for (var i = cards.length - 1; i > 0; i--) {
          var j = Math.floor(Math.random() * (i + 1));
          var tmp = cards[i]; cards[i] = cards[j]; cards[j] = tmp;
        }
        cards.forEach(function (c) { deck.appendChild(c); });
      });
    }
  }

  function figures() {
    var zooms = document.querySelectorAll(".bdx-figure-zoom");
    if (!zooms.length || typeof HTMLDialogElement !== "function") return;
    var box = document.createElement("dialog");
    box.className = "bdx-lightbox";
    box.innerHTML = '<button type="button" class="bdx-lightbox-close">Close</button><img alt="" />';
    document.body.appendChild(box);
    var img = box.querySelector("img");
    box.querySelector(".bdx-lightbox-close").addEventListener("click", function () { box.close(); });
    // A click on the backdrop lands on the dialog itself.
    box.addEventListener("click", function (e) { if (e.target === box) box.close(); });
    Array.prototype.forEach.call(zooms, function (btn) {
      btn.addEventListener("click", function () {
        var source = btn.querySelector("img");
        img.src = source.currentSrc || source.src;
        img.alt = source.alt;
        box.showModal();
      });
    });
  }

  onReady(function () {
    progressBar();
    contents();
    flashcards();
    figures();
    reveal();
  });
})();
