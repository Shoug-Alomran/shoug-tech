/* Final exam roadmaps: topic statuses saved per browser, live group and course bars.
   Pages: scripts/build_final_roadmaps.py */
(function () {
  var KEY = document.documentElement.getAttribute("data-roadmap-key") || "final-roadmap";
  var state = {};
  try {
    state = JSON.parse(localStorage.getItem(KEY) || "{}") || {};
  } catch (e) {
    state = {};
  }
  function save() {
    try {
      localStorage.setItem(KEY, JSON.stringify(state));
    } catch (e) {}
  }
  var topics = Array.prototype.slice.call(document.querySelectorAll(".rm-topic"));
  function val(li) {
    return +state[li.getAttribute("data-id")] || 0;
  }
  // a reviewed topic counts a third, can explain two thirds, tested a whole topic
  function score(list) {
    if (!list.length) return 0;
    var s = 0;
    list.forEach(function (li) {
      s += val(li) / 3;
    });
    return s / list.length;
  }
  function pct(n, of) {
    return (of ? (100 * n) / of : 0) + "%";
  }

  function update() {
    var counts = [0, 0, 0, 0];
    topics.forEach(function (li) {
      var v = val(li);
      counts[v]++;
      li.setAttribute("data-state", v);
    });
    var n = topics.length;

    document.querySelectorAll(".rm-group").forEach(function (g) {
      var list = Array.prototype.slice.call(g.querySelectorAll(".rm-topic"));
      var tested = list.filter(function (li) {
        return val(li) === 3;
      }).length;
      g.querySelector(".rm-gbar i").style.width = score(list) * 100 + "%";
      g.querySelector(".rm-gn").textContent = tested + " / " + list.length + " tested";
      g.classList.toggle("done", list.length > 0 && tested === list.length);
    });

    var total = Math.round(score(topics) * 100);
    document.querySelectorAll(".rm-pct, .rm-meter-n").forEach(function (el) {
      el.textContent = total + "%";
    });
    ["s1", "s2", "s3"].forEach(function (cls, i) {
      var w = pct(counts[i + 1], n);
      var a = document.querySelector(".rm-stack ." + cls);
      var b = document.querySelector(".rm-meter-bar .m" + (i + 1));
      if (a) a.style.width = w;
      if (b) b.style.width = w;
    });
    document.querySelectorAll("[data-count]").forEach(function (b) {
      b.textContent = counts[+b.getAttribute("data-count")];
    });

    // next up: the first topic (top of the route) with the lowest status
    var next = null;
    for (var level = 0; level < 3 && !next; level++) {
      next = topics.filter(function (li) {
        return val(li) === level;
      })[0];
    }
    var link = document.querySelector("[data-next]");
    if (!link) return;
    if (next) {
      link.textContent = next.querySelector(".rm-topic-text b").textContent;
      link.onclick = function (e) {
        e.preventDefault();
        var g = next.closest("details");
        if (g) g.open = true;
        next.scrollIntoView({ behavior: "smooth", block: "center" });
      };
    } else {
      link.textContent = "Everything is tested. Do a past paper!";
      link.onclick = null;
      link.setAttribute("href", "#papers");
    }
  }

  topics.forEach(function (li) {
    var input = li.querySelector('input[value="' + val(li) + '"]');
    if (input) input.checked = true;
    li.addEventListener("change", function (e) {
      var id = li.getAttribute("data-id");
      state[id] = +e.target.value;
      if (!state[id]) delete state[id];
      save();
      update();
    });
  });

  var reset = document.querySelector(".rm-reset");
  if (reset)
    reset.addEventListener("click", function () {
      if (!confirm("Clear every status on this roadmap?")) return;
      state = {};
      save();
      topics.forEach(function (li) {
        li.querySelector('input[value="0"]').checked = true;
      });
      update();
    });

  var expand = document.querySelector(".rm-expand");
  if (expand)
    expand.addEventListener("click", function () {
      var groups = document.querySelectorAll(".rm-group");
      var open = Array.prototype.some.call(groups, function (g) {
        return !g.open;
      });
      groups.forEach(function (g) {
        g.open = open;
      });
      expand.textContent = open ? "Collapse all" : "Expand all";
    });

  // highlight the section in view
  var links = Array.prototype.slice.call(document.querySelectorAll(".rm-nav a"));
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          links.forEach(function (a) {
            a.classList.toggle("active", a.getAttribute("href") === "#" + e.target.id);
          });
        });
      },
      { rootMargin: "-30% 0px -60% 0px" }
    );
    document.querySelectorAll(".rm-section").forEach(function (s) {
      io.observe(s);
    });
  }
  update();
})();
