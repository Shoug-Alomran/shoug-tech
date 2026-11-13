/* Final exam cheat sheets: tabs, progress bar, reveal, answers, readiness ticks.
   Generated pages: scripts/build_final_cheat_sheets.py */
(function () {
    document.querySelectorAll(".tbl table").forEach(function (t) {
      var heads = Array.prototype.map.call(
        t.querySelectorAll("thead th"),
        function (th) {
          return th.textContent.trim();
        },
      );
      t.querySelectorAll("tbody tr").forEach(function (tr) {
        Array.prototype.forEach.call(tr.children, function (td, i) {
          if (heads[i] && td.colSpan === 1)
            td.setAttribute("data-label", heads[i]);
        });
      });
    });

    // scroll progress bar
    var bar = document.querySelector(".progress");
    var ticking = false;
    function progress() {
      var max = document.documentElement.scrollHeight - innerHeight;
      bar.style.setProperty(
        "--p",
        max > 0 ? Math.min(1, scrollY / max) : 0,
      );
      ticking = false;
    }
    addEventListener(
      "scroll",
      function () {
        if (!ticking) {
          ticking = true;
          requestAnimationFrame(progress);
        }
      },
      { passive: true },
    );
    progress();

    // staggered fade-up as blocks enter the screen
    var still = matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!still && "IntersectionObserver" in window) {
      var sel =
        ".card, .q, .tbl, .hook, .trap, .tip, .checklist li, .legend > div, .stat";
      var targets = Array.prototype.filter.call(
        document.querySelectorAll(sel),
        function (el) {
          return !el.parentElement.closest(sel);
        },
      );
      targets.forEach(function (el) {
        var i = Array.prototype.indexOf.call(el.parentElement.children, el);
        el.style.setProperty("--d", (i % 4) * 70 + "ms");
        el.classList.add("reveal");
      });
      document.documentElement.classList.add("anim");
      var rio = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (e) {
            if (e.isIntersecting) {
              e.target.classList.add("in");
              rio.unobserve(e.target);
            }
          });
        },
        { rootMargin: "0px 0px -6% 0px" },
      );
      targets.forEach(function (el) {
        rio.observe(el);
      });
      // print everything, including blocks never scrolled into view
      addEventListener("beforeprint", function () {
        targets.forEach(function (el) {
          el.classList.add("in");
        });
      });
    }

    var btn = document.getElementById("toggle-answers");
    var open = false;
    btn.addEventListener("click", function () {
      open = !open;
      document.querySelectorAll(".q details").forEach(function (d) {
        d.open = open;
      });
      btn.firstChild.textContent = open ? "Hide all " : "Show all ";
    });

    var links = Array.prototype.slice.call(
      document.querySelectorAll(".tabs a"),
    );
    var byId = {};
    links.forEach(function (a) {
      byId[a.getAttribute("href").slice(1)] = a;
    });
    if (!("IntersectionObserver" in window)) return;
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          links.forEach(function (a) {
            a.classList.remove("active");
          });
          var a = byId[e.target.id];
          if (a) {
            a.classList.add("active");
            // scroll only the tab strip; scrollIntoView would move the page
            var strip = a.parentNode;
            var left = a.offsetLeft - strip.offsetLeft;
            if (
              left < strip.scrollLeft ||
              left + a.offsetWidth > strip.scrollLeft + strip.clientWidth
            ) {
              strip.scrollTo({
                left: Math.max(0, left - 16),
                behavior: "smooth",
              });
            }
          }
        });
      },
      { rootMargin: "-30% 0px -60% 0px" },
    );
    document.querySelectorAll("section.chapter").forEach(function (s) {
      io.observe(s);
    });
  })();

// readiness checklists: ticks are saved in this browser only
(function () {
  var lists = document.querySelectorAll(".ready[data-key]");
  if (!lists.length) return;
  var store = {};
  var KEY = document.documentElement.getAttribute("data-ready-key") || "final-cheat";
  try {
    store = JSON.parse(localStorage.getItem(KEY) || "{}") || {};
  } catch (e) {
    store = {};
  }
  function save() {
    try {
      localStorage.setItem(KEY, JSON.stringify(store));
    } catch (e) {}
  }
  lists.forEach(function (ul) {
    var key = ul.getAttribute("data-key");
    var boxes = ul.querySelectorAll("input[type=checkbox]");
    var meter = ul.previousElementSibling;
    var fill = meter && meter.querySelector(".bar i");
    var label = meter && meter.querySelector(".n");
    function update() {
      var done = 0;
      boxes.forEach(function (b) {
        if (b.checked) done++;
      });
      if (fill) fill.style.width = (boxes.length ? (100 * done) / boxes.length : 0) + "%";
      if (label) label.textContent = done + " / " + boxes.length;
    }
    boxes.forEach(function (b, i) {
      var id = key + ":" + i;
      b.checked = !!store[id];
      b.addEventListener("change", function () {
        if (b.checked) store[id] = 1;
        else delete store[id];
        save();
        update();
      });
    });
    var reset = meter && meter.querySelector("button");
    if (reset)
      reset.addEventListener("click", function () {
        boxes.forEach(function (b, i) {
          b.checked = false;
          delete store[key + ":" + i];
        });
        save();
        update();
      });
    update();
  });
})();
