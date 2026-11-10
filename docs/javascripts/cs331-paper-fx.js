/* CS331 past papers: motion on top of the marking engine (cys401-past-paper.js).
   Purely visual: hero stats, answered meter, scroll reveal, self-drawing
   diagrams and confetti. It never touches marks or saved answers. */
(function () {
  "use strict";

  var calm = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var COLORS = [
    "#7c3aed",
    "#ec4899",
    "#f97316",
    "#14b8a6",
    "#3b82f6",
    "#facc15",
  ];

  function $$(sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  }

  function fmt(n) {
    return String(Math.round(n * 100) / 100);
  }

  function heroStats() {
    var intro = document.querySelector(".pp-intro");
    if (!intro) return;
    var marks = $$("[data-unit]").reduce(function (sum, u) {
      return sum + parseFloat(u.dataset.marks || "0");
    }, 0);
    var chapters = {};
    $$(".q[data-ch]").forEach(function (q) {
      chapters[q.dataset.ch] = 1;
    });
    var box = document.createElement("div");
    box.className = "fx-stats";
    [
      [$$(".q").length, "Questions"],
      [fmt(marks), "Marks"],
      [Object.keys(chapters).length, "Chapters"],
    ].forEach(function (s) {
      var el = document.createElement("div");
      el.className = "fx-stat";
      var b = document.createElement("b");
      b.textContent = s[0];
      el.appendChild(b);
      el.appendChild(document.createTextNode(s[1]));
      box.appendChild(el);
    });
    var nav = intro.querySelector(".ch-nav");
    intro.insertBefore(box, nav);
  }

  function isAnswered(u) {
    if (u.dataset.unit === "radio") return !!u.querySelector("input:checked");
    if (u.dataset.unit === "written") {
      var t = u.querySelector("textarea");
      return !!t && !!t.value.trim();
    }
    return !!String(u.value || "").trim();
  }

  function setupMeter() {
    var bar = document.querySelector(".pp-bar");
    var row = document.querySelector(".pp-bar-row");
    var score = document.getElementById("pp-score");
    if (!bar || !row || !score) return;
    var meter = document.createElement("div");
    meter.className = "fx-meter";
    meter.setAttribute("aria-hidden", "true");
    var fill = document.createElement("span");
    meter.appendChild(fill);
    bar.appendChild(meter);
    var chip = document.createElement("span");
    chip.className = "pp-chip fx-answered";
    score.parentNode.insertBefore(chip, score.nextSibling);
    var units = $$("[data-unit]");

    function update() {
      var done = units.filter(isAnswered).length;
      fill.style.width = (units.length ? (done / units.length) * 100 : 0) + "%";
      chip.textContent = done + " / " + units.length + " answered";
    }

    document.addEventListener("input", update);
    document.addEventListener("change", update);
    var reset = document.getElementById("pp-reset");
    if (reset)
      reset.addEventListener("click", function () {
        setTimeout(update, 0);
      });
    update();

    var last = score.textContent;
    new MutationObserver(function () {
      if (score.textContent === last) return;
      last = score.textContent;
      score.classList.remove("fx-pulse");
      void score.offsetWidth;
      score.classList.add("fx-pulse");
    }).observe(score, { childList: true, characterData: true, subtree: true });
  }

  function setupReveal() {
    if (calm || !("IntersectionObserver" in window)) return;
    /* A null root follows the top-level viewport, so this also works inside
       the wrapper page's iframe. */
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          e.target.classList.add("fx-on");
          io.unobserve(e.target);
        });
      },
      { rootMargin: "0px 0px -5% 0px" },
    );
    $$(".q").forEach(function (q) {
      q.classList.add("fx-reveal");
      io.observe(q);
    });
  }

  function setupFigures() {
    if (calm || !("IntersectionObserver" in window)) return;
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          e.target.classList.add("fx-drawn");
          io.unobserve(e.target);
        });
      },
      { threshold: 0.2 },
    );
    $$(".fig").forEach(function (fig) {
      $$("path", fig).forEach(function (p) {
        if (p.getAttribute("stroke-dasharray")) return;
        p.setAttribute("pathLength", "1");
        p.classList.add("fx-draw");
      });
      fig.classList.add("fx-fig");
      io.observe(fig);
    });
  }

  function burst(x, y, count) {
    if (calm) return;
    for (var i = 0; i < count; i++) {
      var bit = document.createElement("span");
      var angle = Math.random() * Math.PI * 2;
      var dist = 50 + Math.random() * 120;
      bit.className = "fx-bit";
      bit.style.left = x + "px";
      bit.style.top = y + "px";
      bit.style.background = COLORS[i % COLORS.length];
      bit.style.setProperty("--dx", Math.cos(angle) * dist + "px");
      bit.style.setProperty("--dy", Math.sin(angle) * dist + "px");
      bit.style.setProperty("--spin", Math.round(Math.random() * 540) + "deg");
      bit.addEventListener("animationend", bit.remove.bind(bit));
      document.body.appendChild(bit);
    }
  }

  function burstFrom(el, count) {
    var r = el.getBoundingClientRect();
    burst(r.left + r.width / 2, r.top + r.height / 2, count);
  }

  function react(q, withBurst) {
    var fb = q.querySelector(":scope > .fb");
    if (!fb || !fb.classList.contains("show")) return;
    var good = fb.classList.contains("ok");
    var cls = good ? "fx-ok" : fb.classList.contains("no") ? "fx-no" : "";
    q.classList.remove("fx-ok", "fx-no");
    if (cls) {
      void q.offsetWidth;
      q.classList.add(cls);
    }
    if (good && withBurst) {
      burstFrom(q.querySelector(":scope > .q-tools .pp-btn") || q, 18);
    }
  }

  /* Runs in the bubbling phase, after the engine's own click handlers. */
  function setupReactions() {
    document.addEventListener("click", function (e) {
      var btn = e.target.closest && e.target.closest("button");
      if (!btn) return;
      if (btn.id === "pp-check") {
        var marked = $$(".q").filter(function (q) {
          return q.querySelector(":scope > .fb.show");
        });
        marked.forEach(function (q, i) {
          react(q, i < 6);
        });
        if (
          marked.length &&
          marked.every(function (q) {
            return q.querySelector(":scope > .fb.ok");
          })
        ) {
          burstFrom(btn, 60);
        }
        return;
      }
      var q = btn.closest(".q");
      if (q && btn.parentNode.parentNode === q) react(q, true);
    });
  }

  function init() {
    heroStats();
    setupMeter();
    setupReveal();
    setupFigures();
    setupReactions();
  }

  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", init);
  else init();
})();
