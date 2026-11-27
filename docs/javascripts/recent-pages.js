/**
 * "Continue where you left off".
 *
 * Records the last page visited in each course and offers them back on the
 * Academics hub. Deliberately localStorage-only and signed-out friendly: the
 * Firestore progress system in firebase-auth.js tracks completion for people
 * with an account, whereas this is about getting anyone back to the deck they
 * were reading ten minutes ago.
 *
 * Anything under /academics/<track>/<course>/ counts, keyed by course so a
 * term's browsing does not collapse into one long undifferentiated list.
 */
(function () {
  "use strict";

  var KEY = "shoug-recent-pages";
  var MAX = 6;
  var COURSE = /^\/academics\/([^/]+)\/([^/]+)\//;

  function read() {
    try {
      var raw = JSON.parse(localStorage.getItem(KEY));
      return Array.isArray(raw) ? raw : [];
    } catch (e) {
      return [];
    }
  }

  function write(entries) {
    try {
      localStorage.setItem(KEY, JSON.stringify(entries.slice(0, MAX)));
    } catch (e) {
      // Private browsing or a full quota; the feature just goes quiet.
    }
  }

  function pageTitle() {
    var h1 = document.querySelector("h1:not(.shoug-visually-hidden)");
    if (h1 && h1.textContent.trim()) return h1.textContent.trim();
    return (document.title || "").split("—")[0].split("//")[0].trim();
  }

  function record() {
    var path = window.location.pathname;
    var m = path.match(COURSE);
    if (!m) return;

    // The course landing page is where the hub already sends people, so
    // recording it would make every entry point back to the same place.
    if (path === "/academics/" + m[1] + "/" + m[2] + "/") return;

    var entry = {
      url: path,
      title: pageTitle(),
      course: m[2].toUpperCase(),
      track: m[1],
      at: Date.now(),
    };
    if (!entry.title) return;

    var entries = read().filter(function (e) {
      return e.course !== entry.course;
    });
    entries.unshift(entry);
    write(entries);
  }

  var CSS = [
    ".shoug-resume{margin:0 0 34px}",
    ".shoug-resume__head{display:flex;align-items:center;gap:12px;margin-bottom:14px;",
    'font-family:"JetBrains Mono",ui-monospace,monospace;font-size:0.66rem;font-weight:800;',
    "letter-spacing:0.18em;text-transform:uppercase;color:#8f8b9a}",
    ".shoug-resume__head button{appearance:none;background:none;border:none;padding:0;cursor:pointer;",
    "font:inherit;letter-spacing:inherit;color:#8f8b9a;text-decoration:underline;text-underline-offset:3px}",
    ".shoug-resume__head button:hover{color:#ff2a4b}",
    ".shoug-resume__grid{display:grid;gap:10px;grid-template-columns:repeat(auto-fill,minmax(240px,1fr))}",
    ".shoug-resume__card{display:flex;flex-direction:column;gap:6px;padding:14px 16px;text-decoration:none;",
    "border:1px solid rgba(184,41,234,0.24);background:rgba(10,5,20,0.5);",
    "transition:border-color 160ms ease,background 160ms ease}",
    ".shoug-resume__card:hover{border-color:#ff2a4b;background:rgba(184,41,234,0.08)}",
    '.shoug-resume__course{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:0.62rem;',
    "font-weight:800;letter-spacing:0.16em;color:#ff2a4b}",
    '.shoug-resume__title{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:0.78rem;',
    "line-height:1.5;color:#f8f7fb;overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}",
    "body.shoug-light-mode .shoug-resume__card{background:#fff;border-color:rgba(22,17,31,0.15)}",
    "body.shoug-light-mode .shoug-resume__title{color:#16111f}",
    "body.shoug-light-mode .shoug-resume__head,body.shoug-light-mode .shoug-resume__head button{color:#534a61}",
  ].join("");

  function injectStyles() {
    if (document.getElementById("shoug-resume-styles")) return;
    var el = document.createElement("style");
    el.id = "shoug-resume-styles";
    el.textContent = CSS;
    document.head.appendChild(el);
  }

  function buildSection(entries, heading) {
    injectStyles();
    var section = document.createElement("section");
    section.className = "shoug-resume";
    section.setAttribute("aria-label", "Continue where you left off");

    var head = document.createElement("div");
    head.className = "shoug-resume__head";
    var label = document.createElement("span");
    label.textContent = heading;
    var clear = document.createElement("button");
    clear.type = "button";
    clear.textContent = "Clear";
    clear.addEventListener("click", function () {
      var gone = {};
      entries.forEach(function (e) {
        gone[e.course] = true;
      });
      write(
        read().filter(function (e) {
          return !gone[e.course];
        }),
      );
      section.remove();
    });
    head.appendChild(label);
    head.appendChild(clear);

    var grid = document.createElement("div");
    grid.className = "shoug-resume__grid";
    entries.forEach(function (e) {
      var a = document.createElement("a");
      a.className = "shoug-resume__card";
      a.href = e.url;
      var c = document.createElement("span");
      c.className = "shoug-resume__course";
      c.textContent = e.course;
      var t = document.createElement("span");
      t.className = "shoug-resume__title";
      t.textContent = e.title;
      a.appendChild(c);
      a.appendChild(t);
      grid.appendChild(a);
    });

    section.appendChild(head);
    section.appendChild(grid);
    return section;
  }

  function insertAfter(node, ref) {
    ref.parentNode.insertBefore(node, ref.nextSibling);
  }

  // "Review mistakes" link, from quiz-mistakes.js's store.
  function reviewLink() {
    var list = [];
    try {
      list = JSON.parse(localStorage.getItem("shoug-quiz-mistakes")) || [];
    } catch (e) {}
    if (!Array.isArray(list) || !list.length) return null;
    var now = Date.now(),
      due = list.filter(function (m) {
        return m && m.due <= now;
      }).length;
    injectStyles();
    var a = document.createElement("a");
    a.className = "shoug-resume__card shoug-resume__review";
    a.href = "/academics/review/";
    var c = document.createElement("span");
    c.className = "shoug-resume__course";
    c.textContent = "REVIEW MISTAKES";
    var t = document.createElement("span");
    t.className = "shoug-resume__title";
    t.textContent = due
      ? due + " missed question" + (due === 1 ? "" : "s") + " due for review"
      : list.length + " saved, none due yet";
    a.appendChild(c);
    a.appendChild(t);
    return a;
  }

  // Shown on the Academics hub and the account page (every course), and on
  // each course's own hub (that course only).
  function render() {
    var path = window.location.pathname,
      entries = read(),
      review =
        path === "/academics/" || path === "/account/" ? reviewLink() : null;
    if (!entries.length && !review) return;

    if (path === "/academics/") {
      var host =
        document.querySelector("main .container") ||
        document.querySelector("main");
      if (!host) return;
      var section = buildSection(entries, "[ Continue where you left off ]");
      if (review)
        section.querySelector(".shoug-resume__grid").appendChild(review);
      // Sits after the hero so the page still leads with its own heading.
      var hero = host.querySelector(".hero");
      if (hero && hero.nextSibling) insertAfter(section, hero);
      else host.insertBefore(section, host.firstChild);
      return;
    }

    if (path === "/account/") {
      var sub = document.querySelector("main .page-sub");
      if (!sub) return;
      var mine = buildSection(entries, "[ Continue where you left off ]");
      if (review) mine.querySelector(".shoug-resume__grid").appendChild(review);
      insertAfter(mine, sub);
      return;
    }

    var m = path.match(COURSE);
    if (
      !entries.length ||
      !m ||
      path !== "/academics/" + m[1] + "/" + m[2] + "/"
    )
      return;
    var mine = entries.filter(function (e) {
      return e.course === m[2].toUpperCase();
    });
    if (!mine.length) return;
    var anchor =
      document.querySelector("main .course-header") ||
      (document.querySelector("main h1") || {}).parentNode;
    if (anchor && anchor.parentNode)
      insertAfter(
        buildSection(mine, "[ Continue in " + mine[0].course + " ]"),
        anchor,
      );
  }

  function init() {
    record();
    render();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

// Star ratings on course overviews and track pages (see course-ratings.js).
// Loaded here, not from mobile-navigation.js: the course-access Worker serves
// its own bundled copy of that file, which only updates on a Worker deploy.
(function () {
  if (
    !/^\/academics\/[^/]+\/(?:[^/]+\/)?(?:[^/]+\/)?(?:index\.html)?$/.test(
      window.location.pathname,
    )
  )
    return;
  var s = document.createElement("script");
  s.src = "/javascripts/course-ratings.js?v=10";
  s.async = true;
  document.head.appendChild(s);
  // Private "MY GRADE" row for the student's own GPA (academic-record.js).
  var g = document.createElement("script");
  g.src = "/javascripts/academic-record.js?v=5";
  g.async = true;
  document.head.appendChild(g);
})();

// Thumbs up/down on resources, % on listings (see resource-ratings.js).
(function () {
  if (window.location.pathname.indexOf("/academics/") !== 0) return;
  var s = document.createElement("script");
  s.src = "/javascripts/resource-ratings.js?v=4";
  s.async = true;
  document.head.appendChild(s);
})();

// Mock exam entry points (see mock-exam.js): a banner on each course's Exams
// pages when the course has a question bank, and a link on the Academics hub.
(function () {
  var path = window.location.pathname;
  var exams = path.match(
    /^\/academics\/[^/]+\/([^/]+)\/exams\/(?:(chapter-quizzes|midterm-1|midterm-2|final)\/)?(?:index\.html)?$/,
  );
  if (path !== "/academics/" && !exams) return;

  var CSS = [
    ".shoug-mock-cta{display:flex;flex-wrap:wrap;align-items:center;gap:8px 18px;",
    "margin:22px clamp(16px,3vw,40px) 4px;",
    "padding:16px 18px;text-decoration:none;border:1px solid rgba(184,41,234,0.45);",
    "background:linear-gradient(90deg,rgba(184,41,234,0.16),rgba(184,41,234,0.04));",
    "transition:border-color 160ms ease,background 160ms ease}",
    ".shoug-mock-cta:hover{border-color:#ff2a4b}",
    '.shoug-mock-cta__k{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:0.66rem;',
    "font-weight:800;letter-spacing:0.16em;color:#ff2a4b}",
    ".shoug-mock-cta__t{flex:1 1 260px;min-width:0;color:#f8f7fb;font-size:0.92rem;line-height:1.45}",
    '.shoug-mock-cta__go{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:0.74rem;',
    "font-weight:800;letter-spacing:0.08em;color:#c75cf0;white-space:nowrap}",
    "body.shoug-light-mode .shoug-mock-cta{background:linear-gradient(90deg,rgba(155,31,208,0.1),#fff);",
    "border-color:rgba(155,31,208,0.4)}",
    "body.shoug-light-mode .shoug-mock-cta__t{color:#16111f}",
    "body.shoug-light-mode .shoug-mock-cta__go{color:#9b1fd0}",
  ].join("");

  function hubLink() {
    var pack = document.querySelector(
      '.hero-cta a[href="/academics/study-pack/"]',
    );
    if (
      !pack ||
      document.querySelector('.hero-cta a[href^="/academics/mock-exam/"]')
    )
      return;
    var a = document.createElement("a");
    a.href = "/academics/mock-exam/";
    a.textContent = "Take a timed mock exam";
    a.setAttribute("data-ar-text", "خذي اختبارًا تجريبيًا بوقت محدد");
    pack.parentNode.appendChild(a);
  }

  function examBanner(course, group) {
    fetch("/academics/mock-exam/banks/index.json")
      .then(function (r) {
        return r.ok ? r.json() : null;
      })
      .then(function (j) {
        var c =
          j &&
          (j.courses || []).find(function (x) {
            return x.course === course;
          });
        if (!c || document.querySelector(".shoug-mock-cta")) return;
        var host =
          document.querySelector("main [data-exam-folders]") ||
          document.querySelector("main .directory-container") ||
          document.querySelector("main .slide-hub");
        if (!host || !host.parentNode) return;
        var style = document.createElement("style");
        style.textContent = CSS;
        document.head.appendChild(style);
        var a = document.createElement("a");
        a.className = "shoug-mock-cta";
        a.href =
          "/academics/mock-exam/?course=" +
          encodeURIComponent(course) +
          (group && group !== "chapter-quizzes" ? "&exam=" + group : "");
        var k = document.createElement("span");
        k.className = "shoug-mock-cta__k";
        k.textContent = "MOCK EXAM";
        var t = document.createElement("span");
        t.className = "shoug-mock-cta__t";
        t.textContent =
          "Mix " +
          c.count +
          " " +
          c.name +
          " questions from every quiz and past paper into one timed exam, then see your score in each chapter.";
        var go = document.createElement("span");
        go.className = "shoug-mock-cta__go";
        go.textContent = "BUILD ONE ->";
        a.appendChild(k);
        a.appendChild(t);
        a.appendChild(go);
        host.parentNode.insertBefore(a, host);
      })
      .catch(function () {});
  }

  function init() {
    if (exams) examBanner(exams[1], exams[2] || "");
    else hubLink();
  }
  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", init);
  else init();
})();

// Mock exam readiness on each course's overview page: the latest score in
// every chapter, with a sparkline of that chapter across past mock exams
// (mock-exam.js keeps them; study-sync.js brings them from other devices).
(function () {
  var m = window.location.pathname.match(
    /^\/academics\/([^/]+)\/([^/]+)\/(?:index\.html)?$/,
  );
  if (!m || m[1] === "mock-exam" || m[1] === "review" || m[1] === "study-pack")
    return;
  var course = m[2].toLowerCase();

  var CSS = [
    ".shoug-ready{margin:0 0 30px;padding:18px 20px;border:1px solid rgba(184,41,234,0.32);background:rgba(10,5,20,0.5)}",
    ".shoug-ready__head{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:8px 16px;margin-bottom:14px}",
    '.shoug-ready__k{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:0.66rem;font-weight:800;letter-spacing:0.16em;color:#ff2a4b}',
    ".shoug-ready__sub{color:#a99fb5;font-size:0.82rem;margin-top:4px}",
    '.shoug-ready__links{display:flex;flex-wrap:wrap;gap:14px;font-family:"JetBrains Mono",ui-monospace,monospace;font-size:0.72rem;font-weight:800;letter-spacing:0.06em}',
    ".shoug-ready__links a{color:#c75cf0;text-decoration:none}",
    ".shoug-ready__links a:hover{color:#ff2a4b}",
    ".shoug-ready__rows{display:grid;gap:10px;grid-template-columns:repeat(auto-fill,minmax(min(100%,320px),1fr))}",
    ".shoug-ready__row{display:grid;grid-template-columns:minmax(0,1fr) auto auto;gap:4px 12px;align-items:center;padding:10px 12px;border:1px solid rgba(255,255,255,0.08)}",
    ".shoug-ready__name{color:#f8f7fb;font-size:0.86rem;line-height:1.35;overflow-wrap:anywhere}",
    ".shoug-ready__meta{grid-column:1/-1;color:#8f8b9a;font-size:0.72rem}",
    '.shoug-ready__pct{font-family:"JetBrains Mono",ui-monospace,monospace;font-weight:800;font-size:0.82rem;padding:2px 8px;border-radius:999px;color:#07040d}',
    ".shoug-ready__pct.good{background:#41d6c3}.shoug-ready__pct.warn{background:#f2b84b}.shoug-ready__pct.bad{background:#ff536f}",
    ".shoug-ready__spark{display:block}",
    "body.shoug-light-mode .shoug-ready{background:#fff;border-color:rgba(155,31,208,0.3)}",
    "body.shoug-light-mode .shoug-ready__name{color:#16111f}",
    "body.shoug-light-mode .shoug-ready__row{border-color:rgba(22,17,31,0.12)}",
    "body.shoug-light-mode .shoug-ready__links a{color:#9b1fd0}",
    "body.shoug-light-mode .shoug-ready__pct.good{background:#0f8a6c;color:#fff}",
    "body.shoug-light-mode .shoug-ready__pct.warn{background:#b26a00;color:#fff}",
    "body.shoug-light-mode .shoug-ready__pct.bad{background:#d61f45;color:#fff}",
  ].join("");

  function load(key, fallback) {
    try {
      var v = JSON.parse(localStorage.getItem(key));
      return v == null ? fallback : v;
    } catch (e) {
      return fallback;
    }
  }
  function band(p) {
    return p >= 80 ? "good" : p >= 50 ? "warn" : "bad";
  }
  function pretty(id) {
    return String(id)
      .replace(/^ch-?/, "Ch ")
      .replace(/^lecture-/, "Lecture ")
      .replace(/^t(\d+)-/, "Topic $1 · ")
      .replace(/-/g, " ");
  }
  // Up to the last 8 scores as a tiny line, so a trend reads at a glance.
  function spark(points) {
    var NS = "http://www.w3.org/2000/svg",
      w = 64,
      h = 22,
      svg = document.createElementNS(NS, "svg");
    svg.setAttribute("class", "shoug-ready__spark");
    svg.setAttribute("width", w);
    svg.setAttribute("height", h);
    svg.setAttribute("viewBox", "0 0 " + w + " " + h);
    svg.setAttribute("role", "img");
    svg.setAttribute(
      "aria-label",
      "Mock scores over time: " + points.join("%, ") + "%",
    );
    if (points.length < 2) return svg;
    var pts = points.map(function (p, i) {
      return [
        2 + (i * (w - 4)) / (points.length - 1),
        h - 2 - ((h - 4) * p) / 100,
      ];
    });
    var line = document.createElementNS(NS, "polyline");
    line.setAttribute(
      "points",
      pts
        .map(function (p) {
          return p[0].toFixed(1) + "," + p[1].toFixed(1);
        })
        .join(" "),
    );
    line.setAttribute("fill", "none");
    line.setAttribute("stroke", "currentColor");
    line.setAttribute("stroke-width", "1.6");
    line.setAttribute("stroke-linejoin", "round");
    svg.appendChild(line);
    var last = pts[pts.length - 1],
      dot = document.createElementNS(NS, "circle");
    dot.setAttribute("cx", last[0]);
    dot.setAttribute("cy", last[1]);
    dot.setAttribute("r", "2.6");
    dot.setAttribute("fill", "currentColor");
    svg.appendChild(dot);
    svg.style.color =
      points[points.length - 1] >= 80
        ? "#41d6c3"
        : points[points.length - 1] >= 50
          ? "#f2b84b"
          : "#ff536f";
    return svg;
  }

  function render() {
    var old = document.querySelector(".shoug-ready");
    var ready = (load("shoug-mock-readiness", {}) || {})[course] || {};
    var ids = Object.keys(ready).filter(function (k) {
      return ready[k] && ready[k].t;
    });
    if (!ids.length) {
      if (old) old.remove();
      return;
    }
    var history = (load("shoug-mock-exams", []) || [])
      .filter(function (h) {
        return h && h.course === course;
      })
      .sort(function (a, b) {
        return (a.at || 0) - (b.at || 0);
      });
    var anchor =
      document.querySelector("main .course-header") ||
      (document.querySelector("main h1") || {}).parentNode;
    if (!anchor || !anchor.parentNode) return;
    if (!document.getElementById("shoug-ready-styles")) {
      var st = document.createElement("style");
      st.id = "shoug-ready-styles";
      st.textContent = CSS;
      document.head.appendChild(st);
    }
    var box = document.createElement("section");
    box.className = "shoug-ready";
    box.setAttribute("aria-label", "Mock exam readiness");
    var head = document.createElement("div");
    head.className = "shoug-ready__head";
    var left = document.createElement("div");
    var k = document.createElement("div");
    k.className = "shoug-ready__k";
    k.textContent = "MOCK EXAM READINESS";
    var sub = document.createElement("div");
    sub.className = "shoug-ready__sub";
    var lastAt = history.length ? history[history.length - 1].at : 0;
    sub.textContent =
      history.length +
      " mock exam" +
      (history.length === 1 ? "" : "s") +
      (lastAt
        ? " · last on " +
          new Date(lastAt).toLocaleDateString(undefined, {
            day: "numeric",
            month: "short",
          })
        : "");
    left.appendChild(k);
    left.appendChild(sub);
    var links = document.createElement("div");
    links.className = "shoug-ready__links";
    var rows = ids
      .map(function (id) {
        var r = ready[id],
          p = Math.round((100 * r.r) / r.t);
        var trend = history
          .filter(function (h) {
            return h.ch && h.ch[id] && h.ch[id][1];
          })
          .map(function (h) {
            return Math.round((100 * h.ch[id][0]) / h.ch[id][1]);
          })
          .slice(-8);
        return {
          id: id,
          title: r.title || pretty(id),
          p: p,
          r: r,
          trend: trend.length ? trend : [p],
        };
      })
      .sort(function (a, b) {
        return a.title.localeCompare(b.title, "en", { numeric: true });
      });
    var weak = rows.filter(function (x) {
      return x.p < 80;
    });
    if (weak.length) {
      var w = document.createElement("a");
      w.href =
        "/academics/mock-exam/?course=" +
        encodeURIComponent(course) +
        "&ch=" +
        weak
          .map(function (x) {
            return encodeURIComponent(x.id);
          })
          .join(",");
      w.textContent = "PRACTISE " + weak.length + " WEAK ->";
      links.appendChild(w);
    }
    var go = document.createElement("a");
    go.href = "/academics/mock-exam/?course=" + encodeURIComponent(course);
    go.textContent = "NEW MOCK EXAM ->";
    links.appendChild(go);
    head.appendChild(left);
    head.appendChild(links);
    box.appendChild(head);
    var grid = document.createElement("div");
    grid.className = "shoug-ready__rows";
    rows.forEach(function (x) {
      var row = document.createElement("div");
      row.className = "shoug-ready__row";
      var name = document.createElement("span");
      name.className = "shoug-ready__name";
      name.textContent = x.title;
      var pct = document.createElement("span");
      pct.className = "shoug-ready__pct " + band(x.p);
      pct.textContent = x.p + "%";
      var meta = document.createElement("span");
      meta.className = "shoug-ready__meta";
      var d = x.trend.length > 1 ? x.trend[x.trend.length - 1] - x.trend[0] : 0;
      meta.textContent =
        (x.r.r % 1 ? x.r.r.toFixed(1) : x.r.r) +
        " of " +
        x.r.t +
        " right last time" +
        (x.trend.length > 1
          ? " · " +
            (d > 0 ? "up " : d < 0 ? "down " : "steady ") +
            (d
              ? Math.abs(d) + " pts over " + x.trend.length + " tries"
              : "over " + x.trend.length + " tries")
          : "");
      row.appendChild(name);
      row.appendChild(spark(x.trend));
      row.appendChild(pct);
      row.appendChild(meta);
      grid.appendChild(row);
    });
    box.appendChild(grid);
    if (old) old.replaceWith(box);
    else anchor.parentNode.insertBefore(box, anchor.nextSibling);
  }

  function init() {
    render();
    window.addEventListener("shoug:study-sync", render);
    // Brings results from the student's other devices when signed in.
    if (
      !window.ShougStudySync &&
      !document.querySelector('script[src*="study-sync.js"]')
    ) {
      var s = document.createElement("script");
      s.src = "/javascripts/study-sync.js";
      s.async = true;
      document.head.appendChild(s);
    }
  }
  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", init);
  else init();
})();
