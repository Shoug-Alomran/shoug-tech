/**
 * Mock exam builder: /academics/mock-exam/
 *
 * Banks come from scripts/build-mock-exam-banks.js (one JSON per course, built
 * from every quiz and past paper on the site, tagged with the chapter ids the
 * calendar's Study Plan uses). This page picks questions from the chapters you
 * choose, spread evenly across them, runs them as a timed exam and scores each
 * chapter.
 *
 * Everything is kept in this browser (localStorage), like Review mistakes:
 *   shoug-mock-exam-active   the exam in progress, so a reload doesn't lose it
 *   shoug-mock-exams         past attempts (score per chapter)
 *   shoug-mock-seen          per course: question id -> 1 right / 0 wrong
 *   shoug-mock-readiness     per course: latest score in each chapter, read by
 *                            the Study Plan (study-plan.js) next to its ratings
 *   shoug-mock-settings      the last setup, per course
 *   shoug-quiz-mistakes      missed questions go to Review mistakes
 */
(function () {
  "use strict";

  var BANKS = "/academics/mock-exam/banks/";
  var K = {
    active: "shoug-mock-exam-active",
    history: "shoug-mock-exams",
    seen: "shoug-mock-seen",
    ready: "shoug-mock-readiness",
    settings: "shoug-mock-settings",
    mistakes: "shoug-quiz-mistakes",
  };
  var OTHER = "_other";
  var DAY = 86400000;
  var TYPES = [
    ["mcq", "Multiple choice", "Auto-marked"],
    ["tf", "True / false", "Auto-marked"],
    ["multi", "Select all that apply", "Auto-marked, all or nothing"],
    ["fill", "Fill in the blank", "Auto-marked, small typos allowed"],
    ["match", "Matching", "Auto-marked, part marks per pair"],
    ["num", "Calculation", "Auto-marked, small rounding allowed"],
    [
      "written",
      "Written answer",
      "Marked from key words; you can change the mark",
    ],
  ];
  // Suggested minutes per question type, close to PSU exam pacing.
  var PACE = {
    mcq: 1,
    tf: 0.6,
    multi: 1.5,
    fill: 1,
    match: 2,
    num: 2,
    written: 4,
  };
  var LETTERS = "ABCDEFGHIJ";

  /* ------------------------------------------------------------ storage */

  function load(key, fallback) {
    try {
      var v = JSON.parse(localStorage.getItem(key));
      return v == null ? fallback : v;
    } catch (e) {
      return fallback;
    }
  }
  function save(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
      return true;
    } catch (e) {
      return false;
    }
  }
  function drop(key) {
    try {
      localStorage.removeItem(key);
    } catch (e) {}
  }

  /* ------------------------------------------------------------ helpers */

  function $(id) {
    return document.getElementById(id);
  }
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function html(tag, cls, markup) {
    var n = el(tag, cls);
    n.innerHTML = markup; // bank HTML is sanitised at build time
    return n;
  }
  function plain(markup) {
    var d = document.createElement("div");
    d.innerHTML = markup || "";
    return (d.textContent || "").replace(/\s+/g, " ").trim();
  }
  function shuffle(a) {
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1)),
        t = a[i];
      a[i] = a[j];
      a[j] = t;
    }
    return a;
  }
  function hash(s) {
    var h = 2166136261;
    for (var i = 0; i < s.length; i++) {
      h ^= s.charCodeAt(i);
      h = Math.imul(h, 16777619);
    }
    return (h >>> 0).toString(36);
  }
  function clock(sec) {
    sec = Math.max(0, Math.round(sec));
    var h = Math.floor(sec / 3600),
      m = Math.floor((sec % 3600) / 60),
      s = sec % 60;
    return (
      (h ? h + ":" + String(m).padStart(2, "0") : m) +
      ":" +
      String(s).padStart(2, "0")
    );
  }
  function minutesText(min) {
    if (min < 60) return min + " min";
    var h = Math.floor(min / 60),
      m = min % 60;
    return h + " h" + (m ? " " + m + " min" : "");
  }
  function pct(r, t) {
    return t ? Math.round((100 * r) / t) : 0;
  }
  function band(p) {
    return p >= 80 ? "good" : p >= 50 ? "warn" : "bad";
  }
  function bandLabel(p) {
    return p >= 80 ? "Ready" : p >= 50 ? "Shaky" : "Weak";
  }
  function dateText(ts) {
    var d = new Date(ts);
    return (
      d.toLocaleDateString(undefined, { day: "numeric", month: "short" }) +
      " · " +
      d.toLocaleTimeString(undefined, { hour: "numeric", minute: "2-digit" })
    );
  }
  function shortTitle(t) {
    return String(t || "").replace(
      /^(Ch|Chapter|Lecture|Topic)\s*([\d.]+)\s*·\s*/i,
      function (m, a, n) {
        return (/^l/i.test(a) ? "L" : /^t/i.test(a) ? "T" : "Ch ") + n + " · ";
      },
    );
  }
  function bar(p, cls) {
    var b = el("div", "bar " + (cls || band(p)));
    var i = el("i");
    i.style.width = Math.max(2, p) + "%";
    b.appendChild(i);
    return b;
  }

  /* -------------------------------------------------------------- state */

  var index = null; // banks/index.json
  var banks = {}; // course -> bank
  var bank = null; // selected course's bank
  var setup = {
    scope: null,
    chapters: {},
    types: {},
    count: 20,
    timing: "auto",
    minutes: 30,
    fresh: true,
  };
  var exam = null; // the run in progress (also in localStorage)
  var timerId = null;

  function fetchJson(url) {
    return fetch(url, { cache: "no-cache", credentials: "same-origin" }).then(
      function (r) {
        if (!r.ok) {
          var err = new Error(r.status);
          err.status = r.status;
          throw err;
        }
        return r.json();
      },
    );
  }
  function entryFor(course) {
    return (
      (index &&
        index.courses.find(function (c) {
          return c.course === course;
        })) ||
      {}
    );
  }
  function getBank(course) {
    if (banks[course]) return Promise.resolve(banks[course]);
    return fetchJson(entryFor(course).bank || BANKS + course + ".json").then(
      function (b) {
        b.byId = {};
        b.chById = {};
        b.questions.forEach(function (q) {
          b.byId[q.id] = q;
        });
        b.chapters.forEach(function (c) {
          b.chById[c.id] = c;
        });
        banks[course] = b;
        return b;
      },
    );
  }
  function chapterTitle(b, id) {
    if (id === OTHER || !id) return "Mixed and past-paper questions";
    var c = b.chById[id];
    return c ? c.title : id;
  }
  function chKey(q) {
    return q.c || OTHER;
  }
  function show(id) {
    ["loading", "setup", "exam", "results"].forEach(function (s) {
      $(s).hidden = s !== id;
    });
    window.scrollTo(0, 0);
  }

  /* -------------------------------------------------------------- setup */

  function params() {
    var p = new URLSearchParams(location.search);
    return {
      course: (p.get("course") || "").toLowerCase(),
      ch: p.get("ch"),
      scope: p.get("scope"),
      exam: p.get("exam"),
    };
  }
  // ?exam=midterm-1 | midterm-2 | final (from a course's exam folders) -> preset index.
  function scopeForExam(b, exam) {
    if (!exam) return null;
    var want = /^final/.test(exam)
      ? "final"
      : /^midterm/.test(exam)
        ? "midterm"
        : "";
    var hits = [];
    b.scopes.forEach(function (s, i) {
      if (s.type === want || (want === "midterm" && /mid|major/i.test(s.label)))
        hits.push(i);
    });
    if (!hits.length) return null;
    return exam === "midterm-2" ? hits[Math.min(1, hits.length - 1)] : hits[0];
  }

  function initSetup() {
    var sel = $("course");
    sel.innerHTML = "";
    var placeholder = el("option", "", "Choose a course…");
    placeholder.value = "";
    sel.appendChild(placeholder);
    index.courses.forEach(function (c) {
      var o = el(
        "option",
        "",
        c.name +
          " · " +
          c.count +
          " questions" +
          (c.locked ? " · course access" : ""),
      );
      o.value = c.course;
      sel.appendChild(o);
    });
    var want = params().course || load(K.settings, {}).lastCourse || "";
    if (
      !index.courses.some(function (c) {
        return c.course === want;
      })
    )
      want = "";
    sel.value = want;
    sel.addEventListener("change", function () {
      selectCourse(sel.value, false);
      try {
        var u = new URL(location.href);
        if (sel.value) u.searchParams.set("course", sel.value);
        else u.searchParams.delete("course");
        u.searchParams.delete("ch");
        u.searchParams.delete("scope");
        history.replaceState(null, "", u);
      } catch (e) {}
    });

    $("ch-all").addEventListener("click", function () {
      setChapters(
        availableChapters().map(function (c) {
          return c.id;
        }),
        null,
      );
    });
    $("ch-none").addEventListener("click", function () {
      setChapters([], null);
    });
    $("count").addEventListener("input", function () {
      setup.count = Math.max(1, parseInt(this.value, 10) || 1);
      renderSummary();
      renderCountChips();
    });
    $("timing").addEventListener("change", function () {
      setup.timing = this.value;
      if (setup.timing === "custom" && !$("minutes").value)
        $("minutes").value = suggestedMinutes();
      renderSummary();
    });
    $("minutes").addEventListener("input", function () {
      setup.minutes = Math.max(1, parseInt(this.value, 10) || 1);
      renderSummary();
    });
    $("fresh").addEventListener("change", function () {
      setup.fresh = this.checked;
    });
    $("start").addEventListener("click", startExam);
    $("history-clear").addEventListener("click", function () {
      if (
        !bank ||
        !confirm(
          "Delete your past " +
            bank.name +
            " mock exam results from this browser?",
        )
      )
        return;
      save(
        K.history,
        load(K.history, []).filter(function (h) {
          return h.course !== bank.course;
        }),
      );
      var r = load(K.ready, {});
      delete r[bank.course];
      save(K.ready, r);
      var cleared = load("shoug-mock-cleared", {});
      cleared[bank.course] = Date.now();
      save("shoug-mock-cleared", cleared);
      synced();
      renderHistory();
      renderChapters();
    });
    renderResume();
    show("setup");
    if (want) selectCourse(want, true);
    else renderEmptySetup();
  }

  function renderEmptySetup() {
    bank = null;
    $("course-note").textContent =
      index.courses.length +
      " courses, " +
      index.courses
        .reduce(function (n, c) {
          return n + c.count;
        }, 0)
        .toLocaleString() +
      " questions from the site's quizzes and past papers.";
    $("scopes").innerHTML = "";
    $("chapters").innerHTML = "";
    $("chapters").appendChild(el("p", "muted", "Choose a course first."));
    $("types").innerHTML = "";
    $("history-panel").hidden = true;
    renderSummary();
  }

  function selectCourse(course, fromUrl) {
    if (!course) return renderEmptySetup();
    $("start").disabled = true;
    $("course-note").textContent = "Loading…";
    getBank(course).then(
      function (b) {
        if ($("course").value !== course) return;
        bank = b;
        var all = load(K.settings, {});
        all.lastCourse = course;
        save(K.settings, all);
        var saved = all[course] || {};
        var p = fromUrl ? params() : {};
        setup.types = {};
        TYPES.forEach(function (t) {
          var has = typeCount(t[0]) > 0;
          setup.types[t[0]] =
            has && (saved.types ? saved.types.indexOf(t[0]) > -1 : true);
        });
        if (
          !TYPES.some(function (t) {
            return setup.types[t[0]];
          })
        )
          TYPES.forEach(function (t) {
            setup.types[t[0]] = typeCount(t[0]) > 0;
          });
        setup.count = saved.count || 20;
        setup.timing = saved.timing || "auto";
        setup.minutes = saved.minutes || 30;
        $("count").value = setup.count;
        $("timing").value = setup.timing;
        $("minutes").value = setup.minutes;
        var tagged = b.questions.filter(function (q) {
          return q.c;
        }).length;
        $("course-note").innerHTML = "";
        $("course-note").appendChild(
          document.createTextNode(
            b.questions.length +
              " questions from " +
              b.sources.length +
              " quizzes and past papers" +
              (b.chapters.length
                ? ", " +
                  pct(tagged, b.questions.length) +
                  "% matched to a chapter. "
                : ". "),
          ),
        );
        var a = el("a", "", "Course page");
        a.href = b.page;
        $("course-note").appendChild(a);

        // Chapters: from the link (?ch= or ?scope=), else the last setup, else everything.
        var ids = null,
          scope = null;
        if (p.ch) ids = p.ch.split(",");
        else if (p.scope != null && b.scopes[+p.scope]) scope = +p.scope;
        else if (scopeForExam(b, p.exam) != null)
          scope = scopeForExam(b, p.exam);
        else if (saved.chapters) {
          ids = saved.chapters;
          scope = saved.scope != null ? saved.scope : null;
        }
        if (scope != null && b.scopes[scope]) ids = scopeIds(scope);
        if (!ids)
          ids = availableChapters().map(function (c) {
            return c.id;
          });
        renderTypes();
        setChapters(ids, scope);
        renderHistory();
        $("start").disabled = false;
      },
      function (err) {
        if ($("course").value !== course) return;
        if (
          entryFor(course).locked &&
          err &&
          (err.status === 401 || err.status === 403)
        )
          lockedSetup(course, err.status);
        else {
          renderEmptySetup();
          $("course-note").textContent =
            err && err.status === 404
              ? "This course's questions aren't published yet. Try again later."
              : "Couldn't load this course's questions. Check your connection and try again.";
        }
      },
    );
  }

  // ETHCS303's questions come with the paid course. The course-access Worker
  // only returns its bank to approved buyers with a course session.
  function lockedSetup(course, status) {
    var c = entryFor(course);
    renderEmptySetup();
    var note = $("course-note");
    note.innerHTML = "";
    note.appendChild(
      document.createTextNode(
        c.count +
          " " +
          c.name +
          " questions come with the course. " +
          (status === 403
            ? "Your account doesn't have approved access yet. "
            : "Sign in to the course with the account you bought it on, then come back here. "),
      ),
    );
    var signIn = el(
      "a",
      "",
      status === 403 ? "Check your access" : "Sign in to the course",
    );
    signIn.href =
      "/course-access/?next=" +
      encodeURIComponent("/academics/other-courses/" + course + "/exams/");
    note.appendChild(signIn);
    note.appendChild(document.createTextNode(" · "));
    var buy = el("a", "", "Get access");
    buy.href = "/checkout/ethics/";
    note.appendChild(buy);
    $("chapters").innerHTML = "";
    $("chapters").appendChild(
      el("p", "muted", "Chapters appear once the course is unlocked."),
    );
  }

  // Chapters with questions, plus the untagged group when there is one.
  function availableChapters() {
    if (!bank) return [];
    var counts = {};
    bank.questions.forEach(function (q) {
      if (setup.types[q.t]) counts[chKey(q)] = (counts[chKey(q)] || 0) + 1;
    });
    var list = bank.chapters.map(function (c) {
      return { id: c.id, title: c.title, n: counts[c.id] || 0 };
    });
    var other = bank.questions.filter(function (q) {
      return !q.c;
    }).length;
    if (other)
      list.push({
        id: OTHER,
        title: chapterTitle(bank, OTHER),
        n: counts[OTHER] || 0,
      });
    return list;
  }
  function scopeIds(i) {
    var s = bank.scopes[i];
    // Untagged past-paper questions span the course, so only a comprehensive
    // (final) preset takes them; a midterm preset would pull in final papers.
    var comprehensive =
      s.type === "final" || /comprehensive|final/i.test(s.label);
    return s.chapters.concat(
      comprehensive &&
        bank.questions.some(function (q) {
          return !q.c;
        })
        ? [OTHER]
        : [],
    );
  }
  function setChapters(ids, scope) {
    setup.chapters = {};
    ids.forEach(function (id) {
      setup.chapters[id] = true;
    });
    setup.scope = scope;
    renderScopes();
    renderChapters();
    renderSummary();
  }

  function renderScopes() {
    var host = $("scopes");
    host.innerHTML = "";
    var all = availableChapters().map(function (c) {
      return c.id;
    });
    var opts = [["Everything", all, null]];
    bank.scopes.forEach(function (s, i) {
      opts.push([s.label, scopeIds(i), i]);
    });
    if (opts.length === 1) return;
    opts.forEach(function (o) {
      var b = el("button", "chip", o[0]);
      b.type = "button";
      var on =
        o[2] === setup.scope && (o[2] != null || sameSet(o[1], selectedIds()));
      b.setAttribute("aria-pressed", String(on));
      b.addEventListener("click", function () {
        setChapters(o[1], o[2]);
      });
      host.appendChild(b);
    });
  }
  function sameSet(a, b) {
    return (
      a.length === b.length &&
      a.every(function (x) {
        return b.indexOf(x) > -1;
      })
    );
  }
  function selectedIds() {
    return Object.keys(setup.chapters).filter(function (k) {
      return setup.chapters[k];
    });
  }

  function renderChapters() {
    var host = $("chapters");
    host.innerHTML = "";
    var last = load(K.ready, {})[bank.course] || {};
    var list = availableChapters();
    if (!list.length) {
      host.appendChild(
        el(
          "p",
          "muted",
          "This course's questions aren't sorted into chapters yet, so the exam draws from all of them.",
        ),
      );
      return;
    }
    list.forEach(function (c) {
      var lab = el("label", "check");
      var box = el("input");
      box.type = "checkbox";
      box.checked = !!setup.chapters[c.id];
      box.disabled = !c.n;
      box.addEventListener("change", function () {
        setup.chapters[c.id] = box.checked;
        setup.scope = null;
        renderScopes();
        renderSummary();
      });
      var t = el("span", "", shortTitle(c.title));
      t.appendChild(
        el("small", "", c.n + " question" + (c.n === 1 ? "" : "s")),
      );
      lab.appendChild(box);
      lab.appendChild(t);
      var r = last[c.id];
      if (r && r.t) {
        var p = pct(r.r, r.t);
        var tag = el("span", "last " + band(p), p + "%");
        tag.title = "Last mock exam: " + r.r + " of " + r.t + " right";
        lab.appendChild(tag);
      }
      host.appendChild(lab);
    });
  }

  function typeCount(t) {
    return bank
      ? bank.questions.filter(function (q) {
          return q.t === t;
        }).length
      : 0;
  }
  function renderTypes() {
    var host = $("types");
    host.innerHTML = "";
    TYPES.forEach(function (t) {
      var n = typeCount(t[0]);
      if (!n) return;
      var lab = el("label", "check");
      var box = el("input");
      box.type = "checkbox";
      box.checked = !!setup.types[t[0]];
      box.addEventListener("change", function () {
        setup.types[t[0]] = box.checked;
        renderChapters();
        renderSummary();
      });
      var s = el("span", "", t[1]);
      s.appendChild(el("small", "", n + " · " + t[2]));
      lab.appendChild(box);
      lab.appendChild(s);
      host.appendChild(lab);
    });
  }

  function pool() {
    if (!bank) return [];
    var noChapters = !availableChapters().length;
    return bank.questions.filter(function (q) {
      return setup.types[q.t] && (noChapters || setup.chapters[chKey(q)]);
    });
  }
  function suggestedMinutes(qs) {
    var p = pool(),
      n = Math.min(setup.count, p.length);
    if (!qs) {
      // Average pace of the questions you'd get.
      var avg = p.length
        ? p.reduce(function (s, q) {
            return s + PACE[q.t];
          }, 0) / p.length
        : 1;
      return Math.max(5, Math.ceil((avg * n) / 5) * 5);
    }
    return Math.max(
      5,
      Math.ceil(
        qs.reduce(function (s, q) {
          return s + PACE[q.t];
        }, 0) / 5,
      ) * 5,
    );
  }
  function renderCountChips() {
    var host = $("count-chips");
    host.innerHTML = "";
    var max = pool().length;
    [10, 20, 30, 50].forEach(function (n) {
      if (n > max && n !== 10) return;
      var b = el("button", "chip", String(n));
      b.type = "button";
      b.setAttribute("aria-pressed", String(setup.count === n));
      b.addEventListener("click", function () {
        setup.count = n;
        $("count").value = n;
        renderCountChips();
        renderSummary();
      });
      host.appendChild(b);
    });
  }
  function renderSummary() {
    var dl = $("summary");
    dl.innerHTML = "";
    var warn = $("summary-warn");
    warn.hidden = true;
    $("minutes").hidden = setup.timing !== "custom";
    if (!bank) {
      $("start").disabled = true;
      $("minutes-note").textContent = "";
      return;
    }
    var p = pool(),
      n = Math.min(setup.count, p.length),
      chs = {};
    p.forEach(function (q) {
      chs[chKey(q)] = 1;
    });
    var mins =
      setup.timing === "none"
        ? null
        : setup.timing === "custom"
          ? setup.minutes
          : suggestedMinutes();
    $("minutes-note").textContent =
      setup.timing === "auto" ? minutesText(suggestedMinutes()) : "";
    [
      ["Course", bank.name],
      ["Questions", n + (p.length > n ? " of " + p.length : "")],
      [
        "Chapters",
        Object.keys(chs).filter(function (k) {
          return k !== OTHER;
        }).length + (chs[OTHER] ? " + mixed" : ""),
      ],
      ["Time", mins == null ? "No limit" : minutesText(mins)],
    ].forEach(function (r) {
      dl.appendChild(el("dt", "", r[0]));
      dl.appendChild(el("dd", "", r[1]));
    });
    renderCountChips();
    if (!p.length) {
      warn.textContent =
        "No questions match. Tick at least one chapter and one question type.";
      warn.hidden = false;
    } else if (setup.count > p.length) {
      warn.textContent =
        "Only " +
        p.length +
        " questions match, so the exam will have " +
        p.length +
        ".";
      warn.hidden = false;
    }
    $("start").disabled = !p.length;
  }

  function renderHistory() {
    var list = load(K.history, [])
      .filter(function (h) {
        return h.course === bank.course;
      })
      .slice(-6)
      .reverse();
    $("history-panel").hidden = !list.length;
    var host = $("history");
    host.innerHTML = "";
    list.forEach(function (h) {
      var p = pct(h.score, h.max);
      var row = el("div", "history-item");
      row.appendChild(el("span", "muted", dateText(h.at)));
      row.appendChild(bar(p));
      row.appendChild(el("span", "score-pill", p + "%"));
      row.title = h.score + " of " + h.max + " · " + h.n + " questions";
      host.appendChild(row);
    });
  }

  function renderResume() {
    var a = load(K.active, null);
    var box = $("resume");
    if (!a || !a.ids || !a.ids.length) {
      box.hidden = true;
      return;
    }
    var done = a.ids.filter(function (id) {
      return answered(a.answers[id]);
    }).length;
    $("resume-text").textContent =
      "You have an unfinished " +
      a.name +
      " mock exam: " +
      done +
      " of " +
      a.ids.length +
      " answered" +
      (a.limit ? ", " + clock(remaining(a)) + " left." : ".");
    box.hidden = false;
    $("resume-go").onclick = function () {
      getBank(a.course).then(
        function (b) {
          bank = b;
          exam = a;
          if (exam.limit && remaining(exam) <= 0) return finishExam(true);
          runExam();
        },
        function (err) {
          $("resume-text").textContent =
            err && (err.status === 401 || err.status === 403)
              ? "Sign in to the " +
                a.name +
                " course to continue this mock exam."
              : "Couldn't load the questions for this mock exam. Check your connection and try again.";
        },
      );
    };
    $("resume-drop").onclick = function () {
      if (!confirm("Discard the unfinished mock exam?")) return;
      drop(K.active);
      box.hidden = true;
    };
  }

  /* ------------------------------------------------------- choosing */

  // Spread the questions across chapters (round robin, random order), with
  // unseen questions first, then ones you got wrong, then ones you got right.
  function pick(n) {
    var seen = load(K.seen, {})[bank.course] || {};
    var groups = {};
    pool().forEach(function (q) {
      (groups[chKey(q)] = groups[chKey(q)] || []).push(q);
    });
    var rank = function (q) {
      if (!setup.fresh) return 0;
      return !(q.id in seen) ? 0 : seen[q.id] === 0 ? 1 : 2;
    };
    var keys = shuffle(Object.keys(groups));
    keys.forEach(function (k) {
      groups[k] = shuffle(groups[k]).sort(function (a, b) {
        return rank(a) - rank(b);
      });
    });
    // Never two parts of the same scenario, and never two questions that ask nearly the same thing.
    var out = [],
      usedGroups = {},
      usedWords = [];
    function clash(q) {
      if (q.g && usedGroups[q.g]) return true;
      var w = coreWords(q);
      return usedWords.some(function (o) {
        return similar(o, w);
      });
    }
    while (out.length < n && keys.length) {
      keys = keys.filter(function (k) {
        return groups[k].length;
      });
      for (var i = 0; i < keys.length && out.length < n; i++) {
        var list = groups[keys[i]];
        while (list.length) {
          var q = list.shift();
          if (clash(q)) continue;
          out.push(q);
          if (q.g) usedGroups[q.g] = 1;
          usedWords.push(coreWords(q));
          break;
        }
      }
    }
    return shuffle(out);
  }

  var STOP = {};
  (
    "which what when where that this with from into each your their there these those about would could should does have " +
    "following best most describe explain name give list state between other than they them then also only some such being " +
    "used using under over more less after before true false project team order match position step steps stage stages phase phases process right correct"
  )
    .split(" ")
    .forEach(function (w) {
      STOP[w] = 1;
    });
  // The question plus its right answer, so "same concept, different wording" still counts as a repeat.
  // Words in more than 10% of the bank's questions (templates, the course's subject) are ignored.
  function commonWords() {
    if (bank._common) return bank._common;
    var df = {};
    bank.questions.forEach(function (q) {
      rawWords(q).forEach(function (w) {
        df[w] = (df[w] || 0) + 1;
      });
    });
    var limit = Math.max(6, bank.questions.length * 0.1),
      out = {};
    Object.keys(df).forEach(function (w) {
      if (df[w] > limit) out[w] = 1;
    });
    return (bank._common = out);
  }
  function coreWords(q) {
    var common = commonWords();
    return rawWords(q).filter(function (w) {
      return !common[w];
    });
  }
  function rawWords(q) {
    var seen = {};
    var answer =
      q.o && typeof q.a === "number" && q.t !== "tf"
        ? " " + plain(q.o[q.a])
        : "";
    (plain(q.qc || q.q) + answer)
      .toLowerCase()
      .replace(/[^a-z0-9 ]+/g, " ")
      .split(/\s+/)
      .forEach(function (w) {
        if (w.length > 3 && !STOP[w])
          seen[w.replace(/(ies)$/, "y").replace(/(es|s)$/, "")] = 1;
      });
    return Object.keys(seen);
  }
  function similar(a, b) {
    if (a.length < 3 || b.length < 3) return false;
    var set = {},
      both = 0;
    a.forEach(function (w) {
      set[w] = 1;
    });
    b.forEach(function (w) {
      if (set[w]) both++;
    });
    // Stricter than the bank builder (which deletes at 0.5): here it only keeps two
    // look-alike questions out of the same exam.
    return both >= 3 && both / (a.length + b.length - both) >= 0.38;
  }

  // Options keep their order when one refers to another ("all of the above").
  function fixedOrder(q) {
    return q.o.some(function (o) {
      return /\b(all|none|both|neither) of (the )?(above|these|them)\b|\b(both|only) [a-e] and [a-e]\b|\b[a-e] (and|&) [a-e]\b|^\s*(all|none|both)\s*$/i.test(
        plain(o),
      );
    });
  }
  function optionOrder(q) {
    var idx = q.o.map(function (o, i) {
      return i;
    });
    if (q.t === "tf") return idx;
    return fixedOrder(q) ? idx : shuffle(idx);
  }

  function startExam() {
    var qs = pick(Math.min(setup.count, pool().length));
    if (!qs.length) return;
    // The same number the summary showed.
    var mins =
      setup.timing === "none"
        ? 0
        : setup.timing === "custom"
          ? setup.minutes
          : suggestedMinutes();
    var all = load(K.settings, {});
    all[bank.course] = {
      types: TYPES.map(function (t) {
        return t[0];
      }).filter(function (t) {
        return setup.types[t];
      }),
      chapters: selectedIds(),
      scope: setup.scope,
      count: setup.count,
      timing: setup.timing,
      minutes: setup.minutes,
    };
    all.lastCourse = bank.course;
    save(K.settings, all);
    exam = {
      v: 1,
      course: bank.course,
      name: bank.name,
      scope:
        setup.scope != null && bank.scopes[setup.scope]
          ? bank.scopes[setup.scope].label
          : "",
      ids: qs.map(function (q) {
        return q.id;
      }),
      order: {},
      answers: {},
      flags: {},
      marks: {},
      cur: 0,
      started: Date.now(),
      limit: mins * 60,
      settings: all[bank.course],
    };
    // The right answers land evenly on A–D across the exam, so the letter never gives one away.
    var free = qs.filter(function (q) {
      return q.t === "mcq" && q.o && q.o.length > 1 && !fixedOrder(q);
    });
    var off = Math.floor(Math.random() * 4);
    var slots = shuffle(
      free.map(function (q, i) {
        return (i + off) % 4;
      }),
    );
    qs.forEach(function (q) {
      if (q.o) exam.order[q.id] = optionOrder(q);
      if (q.pairs)
        exam.order[q.id] = shuffle(
          q.pairs.map(function (p, i) {
            return i;
          }),
        );
    });
    free.forEach(function (q, i) {
      var rest = shuffle(
        q.o
          .map(function (o, k) {
            return k;
          })
          .filter(function (k) {
            return k !== q.a;
          }),
      );
      rest.splice(slots[i] % q.o.length, 0, q.a);
      exam.order[q.id] = rest;
    });
    persist();
    runExam();
  }

  /* ---------------------------------------------------------- exam */

  function persist() {
    if (exam && !exam.done) save(K.active, exam);
  }
  function remaining(a) {
    return a.limit - (Date.now() - a.started) / 1000;
  }
  function answered(v) {
    if (v == null) return false;
    if (Array.isArray(v))
      return v.some(function (x) {
        return x != null;
      });
    if (typeof v === "string") return v.trim().length > 0;
    return true;
  }

  function runExam() {
    show("exam");
    $("exam-title").textContent =
      exam.name + (exam.scope ? " · " + exam.scope : "") + " · MOCK";
    document.title = exam.name + " mock exam | SHOUG.TECH";
    $("finish").onclick = function () {
      var left = exam.ids.filter(function (id) {
        return !answered(exam.answers[id]);
      }).length;
      var flagged = exam.ids.filter(function (id) {
        return exam.flags[id];
      }).length;
      var msg = left
        ? left +
          " question" +
          (left === 1 ? " is" : "s are") +
          " unanswered and will be marked wrong. Finish anyway?"
        : flagged
          ? "You flagged " +
            flagged +
            " question" +
            (flagged === 1 ? "" : "s") +
            " to come back to. Finish anyway?"
          : "Finish and see your results?";
      if (confirm(msg)) finishExam(false);
    };
    $("quit").onclick = function () {
      if (
        !confirm("Quit this mock exam? Your answers won't be saved or scored.")
      )
        return;
      stopTimer();
      drop(K.active);
      exam = null;
      document.title = "Mock Exam Builder | SHOUG.TECH";
      renderResume();
      show("setup");
      if (bank) selectCourse(bank.course, false);
    };
    startTimer();
    renderQuestion();
  }

  function startTimer() {
    stopTimer();
    var t = $("timer");
    if (!exam.limit) {
      t.textContent = "No limit";
      t.classList.remove("low");
      return;
    }
    var tick = function () {
      var left = remaining(exam);
      t.textContent = clock(left);
      t.classList.toggle("low", left <= 120);
      t.setAttribute("aria-label", "Time left " + clock(left));
      if (left <= 0) {
        stopTimer();
        finishExam(true);
      }
    };
    tick();
    timerId = setInterval(tick, 1000);
  }
  function stopTimer() {
    if (timerId) clearInterval(timerId);
    timerId = null;
  }

  function currentQ() {
    return bank.byId[exam.ids[exam.cur]];
  }

  function renderQuestion() {
    var q = currentQ();
    if (!q) return finishExam(false);
    var card = $("q-card");
    card.innerHTML = "";
    var n = exam.ids.length;
    var meta = el("div", "q-meta");
    meta.appendChild(el("span", "label", typeName(q)));
    if (q.p) meta.appendChild(el("span", "label", "From a past exam"));
    card.appendChild(meta);
    card.appendChild(html("div", "q-text", q.q));

    var ans = exam.answers[q.id];
    if (q.o) {
      var multi = q.t === "multi";
      var box = el("div", "opts" + (multi ? " multi" : ""));
      box.setAttribute("role", multi ? "group" : "radiogroup");
      box.setAttribute("aria-label", "Options");
      exam.order[q.id].forEach(function (oi, pos) {
        var b = el("button", "opt");
        b.type = "button";
        b.setAttribute("role", multi ? "checkbox" : "radio");
        var on = multi
          ? Array.isArray(ans) && ans.indexOf(oi) > -1
          : ans === oi;
        b.setAttribute("aria-checked", String(on));
        b.appendChild(el("span", "key", LETTERS[pos]));
        b.appendChild(html("span", "", q.o[oi]));
        b.addEventListener("click", function () {
          choose(q, oi);
        });
        box.appendChild(b);
      });
      card.appendChild(box);
      if (multi)
        card.appendChild(
          el(
            "p",
            "hint",
            "Select every correct option. You need all of them, and no wrong ones, for the mark.",
          ),
        );
    } else if (q.t === "match") {
      var rows = el("div", "match");
      var cur = Array.isArray(ans)
        ? ans
        : q.pairs.map(function () {
            return null;
          });
      q.pairs.forEach(function (pair, ti) {
        var row = el("label", "match-row");
        row.appendChild(html("span", "match-term", pair[0]));
        var sel = el("select", "match-pick");
        sel.setAttribute("aria-label", "Match for " + plain(pair[0]));
        var none = el("option", "", "Choose…");
        none.value = "";
        sel.appendChild(none);
        exam.order[q.id].forEach(function (di) {
          var o = el("option", "", plain(q.pairs[di][1]));
          o.value = String(di);
          sel.appendChild(o);
        });
        sel.value = cur[ti] == null ? "" : String(cur[ti]);
        sel.addEventListener("change", function () {
          var next = (
            Array.isArray(exam.answers[q.id]) ? exam.answers[q.id] : cur
          ).slice();
          next[ti] = sel.value === "" ? null : +sel.value;
          exam.answers[q.id] = next;
          persist();
          renderNav();
        });
        row.appendChild(sel);
        rows.appendChild(row);
      });
      card.appendChild(rows);
      card.appendChild(
        el("p", "hint", "Each correct pair earns its share of the mark."),
      );
    } else if (q.t === "fill") {
      var inp = el("input", "fill-input");
      inp.type = "text";
      inp.autocomplete = "off";
      inp.spellcheck = false;
      inp.setAttribute("aria-label", "Your answer");
      inp.placeholder = "Type the missing word or phrase";
      inp.value = ans || "";
      inp.addEventListener("input", function () {
        exam.answers[q.id] = inp.value;
        persist();
        renderNav();
      });
      inp.addEventListener("keydown", function (e) {
        if (e.key === "Enter") go(1);
      });
      card.appendChild(inp);
      setTimeout(function () {
        inp.focus();
      }, 0);
    } else if (q.t === "num") {
      var row = el("div", "num-row");
      var ni = el("input", "fill-input num-input");
      ni.type = "text";
      ni.autocomplete = "off";
      ni.setAttribute("inputmode", "decimal");
      ni.setAttribute("aria-label", "Your answer");
      ni.placeholder = "A number, or the calculation (like 100/10)";
      ni.value = ans || "";
      ni.addEventListener("input", function () {
        exam.answers[q.id] = ni.value;
        persist();
        renderNav();
      });
      ni.addEventListener("keydown", function (e) {
        if (e.key === "Enter") go(1);
      });
      row.appendChild(ni);
      if (q.u) row.appendChild(el("span", "num-unit", q.u));
      card.appendChild(row);
      card.appendChild(
        el("p", "hint", "Small rounding differences are accepted."),
      );
    } else {
      var ta = el("textarea", "written");
      ta.setAttribute("aria-label", "Your answer");
      ta.placeholder = "Write your answer as you would in the exam.";
      ta.value = ans || "";
      ta.addEventListener("input", function () {
        exam.answers[q.id] = ta.value;
        persist();
        renderNav();
      });
      card.appendChild(ta);
      card.appendChild(
        el(
          "p",
          "hint",
          "When you finish, this is marked from the key words in the model answer. You can change the mark if the check missed something you said in other words.",
        ),
      );
    }

    var acts = el("div", "q-actions");
    var left = el("div", "group"),
      right = el("div", "group");
    var prev = el("button", "btn", "← Previous");
    prev.type = "button";
    prev.disabled = exam.cur === 0;
    prev.addEventListener("click", function () {
      go(-1);
    });
    var flag = el(
      "button",
      "btn",
      exam.flags[q.id] ? "Flagged" : "Flag for review",
    );
    flag.type = "button";
    flag.setAttribute("aria-pressed", String(!!exam.flags[q.id]));
    flag.addEventListener("click", function () {
      toggleFlag(q);
    });
    var last = exam.cur === n - 1;
    var next = el("button", "btn primary", last ? "Finish" : "Next →");
    next.type = "button";
    next.addEventListener("click", function () {
      if (last) $("finish").click();
      else go(1);
    });
    left.appendChild(prev);
    left.appendChild(flag);
    right.appendChild(next);
    acts.appendChild(left);
    acts.appendChild(right);
    card.appendChild(acts);
    renderNav();
  }

  function typeName(q) {
    return {
      mcq: "Multiple choice",
      tf: "True or false",
      multi: "Select all that apply",
      fill: "Fill in the blank",
      match: "Matching",
      num: "Calculation",
      written: "Written answer",
    }[q.t];
  }

  function choose(q, oi) {
    if (q.t === "multi") {
      var cur = Array.isArray(exam.answers[q.id])
        ? exam.answers[q.id].slice()
        : [];
      var at = cur.indexOf(oi);
      if (at > -1) cur.splice(at, 1);
      else cur.push(oi);
      exam.answers[q.id] = cur;
    } else {
      exam.answers[q.id] = exam.answers[q.id] === oi ? null : oi;
    }
    persist();
    var keep =
      document.activeElement && document.activeElement.classList.contains("opt")
        ? Array.prototype.indexOf.call(
            document.activeElement.parentNode.children,
            document.activeElement,
          )
        : -1;
    renderQuestion();
    if (keep > -1) {
      var opts = $("q-card").querySelectorAll(".opt");
      if (opts[keep]) opts[keep].focus();
    }
  }
  function toggleFlag(q) {
    exam.flags[q.id] = !exam.flags[q.id];
    persist();
    renderQuestion();
  }
  function go(d) {
    var to = exam.cur + d;
    if (to < 0 || to >= exam.ids.length) return;
    exam.cur = to;
    persist();
    renderQuestion();
    if (window.innerWidth < 960) $("q-card").scrollIntoView({ block: "start" });
  }

  function renderNav() {
    var n = exam.ids.length,
      done = exam.ids.filter(function (id) {
        return answered(exam.answers[id]);
      }).length;
    $("exam-count").textContent =
      "Question " + (exam.cur + 1) + " of " + n + " · " + done + " answered";
    $("exam-bar").style.width = pct(done, n) + "%";
    var host = $("nav-grid");
    host.innerHTML = "";
    exam.ids.forEach(function (id, i) {
      var b = el("button", "nav-dot", String(i + 1));
      b.type = "button";
      if (answered(exam.answers[id])) b.classList.add("done");
      if (exam.flags[id]) b.classList.add("flag");
      if (i === exam.cur) {
        b.classList.add("current");
        b.setAttribute("aria-current", "step");
      }
      b.setAttribute(
        "aria-label",
        "Question " +
          (i + 1) +
          (answered(exam.answers[id]) ? ", answered" : ", not answered") +
          (exam.flags[id] ? ", flagged" : ""),
      );
      b.addEventListener("click", function () {
        exam.cur = i;
        persist();
        renderQuestion();
      });
      host.appendChild(b);
    });
  }

  document.addEventListener("keydown", function (e) {
    if ($("exam").hidden || !exam || e.ctrlKey || e.metaKey || e.altKey) return;
    var tag = (e.target.tagName || "").toLowerCase();
    if (tag === "input" || tag === "textarea" || tag === "select") return;
    var q = currentQ();
    if (e.key === "ArrowRight") {
      go(1);
      e.preventDefault();
      return;
    }
    if (e.key === "ArrowLeft") {
      go(-1);
      e.preventDefault();
      return;
    }
    if (e.key === "F" && e.shiftKey) {
      toggleFlag(q);
      e.preventDefault();
      return;
    }
    if (!q.o) return;
    var k = e.key.toUpperCase(),
      pos = /^[1-9]$/.test(k) ? +k - 1 : LETTERS.indexOf(k);
    if (pos > -1 && pos < exam.order[q.id].length && !e.shiftKey) {
      choose(q, exam.order[q.id][pos]);
      e.preventDefault();
    }
  });

  /* ------------------------------------------------------------ marking */

  function norm(s) {
    return String(s || "")
      .toLowerCase()
      .normalize("NFKD")
      .replace(/[̀-ͯ]/g, "")
      .replace(/[^a-z0-9؀-ۿ]+/g, " ")
      .replace(/\b(the|a|an)\b/g, " ")
      .replace(/\s+/g, " ")
      .trim();
  }
  function stem(w) {
    return w.replace(/(ies)$/, "y").replace(/(es|s)$/, "");
  }
  function close(a, b) {
    if (a === b) return true;
    if (Math.abs(a.length - b.length) > 1 || Math.min(a.length, b.length) < 5)
      return false;
    // One edit apart.
    var i = 0,
      j = 0,
      edits = 0;
    while (i < a.length && j < b.length) {
      if (a[i] === b[j]) {
        i++;
        j++;
        continue;
      }
      if (++edits > 1) return false;
      if (a.length > b.length) i++;
      else if (b.length > a.length) j++;
      else {
        i++;
        j++;
      }
    }
    return edits + (a.length - i) + (b.length - j) <= 1;
  }
  function fillRight(q, given) {
    var g = norm(given);
    if (!g) return false;
    var gs = g.split(" ").map(stem).join(" ");
    return q.a.some(function (acc) {
      var a = norm(acc);
      if (!a) return false;
      var as = a.split(" ").map(stem).join(" ");
      if (gs === as || close(gs, as)) return true;
      // A short answer that contains the accepted term ("management buy-in" for "management").
      return (
        g.split(" ").length <= 4 &&
        (" " + gs + " ").indexOf(" " + as + " ") > -1
      );
    });
  }

  function numberOf(text) {
    var t = String(text || "")
      .replace(/,/g, "")
      .replace(/[×xX]/g, "*")
      .replace(/÷/g, "/")
      .replace(/−/g, "-")
      .replace(/\^/g, "**")
      .replace(/%\s*$/, "")
      .replace(/[a-zA-Z\s-]+$/g, "")
      .replace(/^[a-zA-Z\s]+=\s*/, "")
      .trim();
    if (!t || !/^[0-9.+\-*/() ]+$/.test(t)) return NaN;
    try {
      var v = Function('"use strict";return (' + t + ")")();
      return typeof v === "number" && isFinite(v) ? v : NaN;
    } catch (e) {
      return NaN;
    }
  }
  function numRight(q, given) {
    var v = numberOf(given);
    var tol = q.tol != null ? q.tol : Math.abs(q.a) * 0.03;
    return !isNaN(v) && Math.abs(v - q.a) <= tol + 1e-9;
  }

  // Written answers: the points the question asks for (q.k, from the quiz's rubric), or, for
  // older questions, the distinctive words of the model answer. Returns the mark and what was found.
  var KW_STOP = {};
  (
    "about above after again against because been before being below between both could does doing during each every " +
    "from further have having here into itself more most must only other over same should some such than that their theirs " +
    "them then there these they this those through under until very what when where which while whom with would your " +
    "also used uses using make makes made like just many much well need needs often usually example examples called mean means"
  )
    .split(" ")
    .forEach(function (w) {
      KW_STOP[w] = 1;
    });
  function keyPoints(q) {
    if (q.k && q.k.length)
      return {
        list: q.k,
        need: Math.min(q.n || q.k.length, q.k.length),
        from: "rubric",
      };
    var seen = {},
      list = [];
    norm(plain(q.m))
      .split(" ")
      .forEach(function (w) {
        if (w.length < 5 || KW_STOP[w] || /^\d+$/.test(w)) return;
        var st = stem(w);
        if (seen[st] || list.length >= 8) return;
        seen[st] = 1;
        list.push([w, [st]]);
      });
    return {
      list: list,
      need: Math.max(1, Math.min(list.length, Math.ceil(list.length * 0.5))),
      from: "model",
    };
  }
  function keywordMark(q, given) {
    var kp = keyPoints(q);
    var text = " " + norm(given).split(" ").map(stem).join(" ") + " ";
    var raw = " " + norm(given) + " ";
    var found = [],
      missed = [];
    kp.list.forEach(function (pt) {
      var hit = pt[1].some(function (k) {
        var nk = norm(k);
        if (!nk) return false;
        var sk = nk.split(" ").map(stem).join(" ");
        return raw.indexOf(nk) > -1 || text.indexOf(sk) > -1;
      });
      (hit ? found : missed).push(pt[0]);
    });
    var frac = kp.list.length ? Math.min(found.length, kp.need) / kp.need : 0;
    var mark = !answered(given) ? 0 : frac >= 0.75 ? 1 : frac >= 0.34 ? 0.5 : 0;
    return {
      mark: mark,
      found: found,
      missed: missed,
      need: kp.need,
      from: kp.from,
    };
  }
  function autoMarkWritten(ex) {
    ex.auto = ex.auto || {};
    ex.ids.forEach(function (id) {
      var q = bank.byId[id];
      if (!q || q.t !== "written" || ex.marks[id] != null) return;
      var r = keywordMark(q, ex.answers[id]);
      ex.auto[id] = r;
      ex.marks[id] = r.mark;
    });
  }

  // 1 right, 0 wrong, 0.5 half (written only), null not marked yet.
  function markOf(q, ex) {
    var a = ex.answers[q.id];
    if (q.t === "written")
      return ex.marks[q.id] == null ? null : ex.marks[q.id];
    if (!answered(a)) return 0;
    if (q.t === "match") {
      var got = 0;
      q.pairs.forEach(function (p, i) {
        if (a[i] === i) got++;
      });
      return Math.round((got / q.pairs.length) * 100) / 100;
    }
    if (q.t === "multi") {
      var want = q.a
          .slice()
          .sort(function (x, y) {
            return x - y;
          })
          .join(","),
        got = (a || [])
          .slice()
          .sort(function (x, y) {
            return x - y;
          })
          .join(",");
      return want === got ? 1 : 0;
    }
    if (q.t === "fill") return fillRight(q, a) ? 1 : 0;
    if (q.t === "num") return numRight(q, a) ? 1 : 0;
    return a === q.a ? 1 : 0;
  }

  function tally(ex) {
    var t = { score: 0, max: 0, pending: 0, right: 0, wrong: 0, ch: {} };
    ex.ids.forEach(function (id) {
      var q = bank.byId[id];
      if (!q) return;
      var m = markOf(q, ex),
        k = chKey(q);
      t.ch[k] = t.ch[k] || { r: 0, t: 0 };
      if (m == null) {
        t.pending++;
        return;
      }
      t.max++;
      t.score = Math.round((t.score + m) * 100) / 100;
      t.ch[k].t++;
      t.ch[k].r = Math.round((t.ch[k].r + m) * 100) / 100;
      if (m === 1) t.right++;
      else if (m === 0) t.wrong++;
    });
    return t;
  }

  function finishExam(timeUp) {
    stopTimer();
    exam.done = true;
    exam.finished = Date.now();
    exam.timeUp = !!timeUp;
    exam.attempt = exam.attempt || hash(exam.course + exam.started);
    autoMarkWritten(exam);
    drop(K.active);
    record();
    document.title = exam.name + " mock exam results | SHOUG.TECH";
    renderResults();
    if (timeUp)
      setTimeout(function () {
        alert("Time's up. Your exam was submitted.");
      }, 50);
  }

  // Save the attempt, what you've seen, chapter readiness and missed questions.
  // Called again when written answers are marked, so it updates in place.
  function record() {
    var t = tally(exam);
    var chapters = {};
    Object.keys(t.ch).forEach(function (k) {
      if (t.ch[k].t) chapters[k] = [t.ch[k].r, t.ch[k].t];
    });
    var hist = load(K.history, []).filter(function (h) {
      return h.id !== exam.attempt;
    });
    hist.push({
      id: exam.attempt,
      course: exam.course,
      name: exam.name,
      scope: exam.scope,
      at: exam.finished,
      secs: Math.round((exam.finished - exam.started) / 1000),
      limit: exam.limit,
      n: exam.ids.length,
      score: t.score,
      max: t.max,
      pending: t.pending,
      ch: chapters,
      upd: Date.now(),
    });
    save(K.history, hist.slice(-200));

    var seen = load(K.seen, {});
    var mine = seen[exam.course] || {};
    exam.ids.forEach(function (id) {
      var q = bank.byId[id],
        m = q && markOf(q, exam);
      if (m != null) mine[id] = m >= 1 ? 1 : 0;
    });
    var keys = Object.keys(mine);
    if (keys.length > 5000)
      keys.slice(0, keys.length - 5000).forEach(function (k) {
        delete mine[k];
      });
    seen[exam.course] = mine;
    save(K.seen, seen);

    var ready = load(K.ready, {});
    var rc = ready[exam.course] || {};
    Object.keys(chapters).forEach(function (k) {
      if (k === OTHER) return;
      rc[k] = {
        r: chapters[k][0],
        t: chapters[k][1],
        at: exam.finished,
        attempt: exam.attempt,
        title: chapterTitle(bank, k),
      };
    });
    ready[exam.course] = rc;
    save(K.ready, ready);

    saveMistakes();
    synced();
  }
  function synced() {
    if (window.ShougStudySync) window.ShougStudySync.changed();
  }

  function saveMistakes() {
    var list = load(K.mistakes, []);
    if (!Array.isArray(list)) list = [];
    var added = 0,
      forgotten = [];
    exam.ids.forEach(function (id) {
      var q = bank.byId[id];
      if (!q) return;
      var m = markOf(q, exam);
      var src = bank.sources[q.s] || {},
        text = plain(q.q),
        mid = hash((src.url || "") + "|" + text);
      if (m == null || m >= 1) {
        // Re-marked as right: take back only what this attempt added.
        var had = list.some(function (x) {
          return x.id === mid && x.attempt === exam.attempt;
        });
        list = list.filter(function (x) {
          return !(x.id === mid && x.attempt === exam.attempt);
        });
        if (had) forgotten.push(mid);
        return;
      }
      list = list.filter(function (x) {
        return x.id !== mid;
      });
      list.push({
        id: mid,
        q: text.slice(0, 600),
        chosen: yourAnswerText(q, exam).slice(0, 300),
        correct: correctText(q).slice(0, 300),
        explain: plain(q.e).slice(0, 600),
        page: src.url || "/academics/mock-exam/",
        course: bank.name.replace(/\s+/g, ""),
        quiz: (src.title || "Mock exam").slice(0, 120),
        at: Date.now(),
        due: Date.now() + DAY,
        box: 0,
        from: "mock",
        attempt: exam.attempt,
      });
      added++;
    });
    save(K.mistakes, list.slice(-400));
    if (forgotten.length) {
      var gone = load("shoug-quiz-mistakes-gone", {});
      forgotten.forEach(function (id) {
        gone[id] = Date.now();
      });
      save("shoug-quiz-mistakes-gone", gone);
    }
    exam.mistakesAdded = added;
  }

  function yourAnswerText(q, ex) {
    var a = ex.answers[q.id];
    if (!answered(a)) return "";
    if (q.t === "multi")
      return a
        .map(function (i) {
          return plain(q.o[i]);
        })
        .join("; ");
    if (q.t === "match")
      return q.pairs
        .map(function (p, i) {
          return (
            plain(p[0]) + " → " + (a[i] == null ? "?" : plain(q.pairs[a[i]][1]))
          );
        })
        .join("; ");
    if (q.o) return plain(q.o[a]);
    return String(a);
  }
  function correctText(q) {
    if (q.t === "multi")
      return q.a
        .map(function (i) {
          return plain(q.o[i]);
        })
        .join("; ");
    if (q.t === "match")
      return q.pairs
        .map(function (p) {
          return plain(p[0]) + " → " + plain(p[1]);
        })
        .join("; ");
    if (q.o) return plain(q.o[q.a]);
    if (q.t === "fill") return q.a.join(" / ");
    if (q.t === "num") return String(q.a) + (q.u ? " " + q.u : "");
    return plain(q.m);
  }

  /* ------------------------------------------------------------ results */

  var reviewFilter = "all";

  function renderResults() {
    show("results");
    var t = tally(exam);
    var p = pct(t.score, t.max);
    var ring = $("ring");
    ring.style.setProperty("--p", p);
    ring.style.setProperty("--c", "var(--" + band(p) + ")");
    $("score-pct").textContent = t.max ? p + "%" : "—";
    $("score-raw").textContent = fmtScore(t.score) + " / " + t.max;
    $("result-eyebrow").textContent =
      exam.name + (exam.scope ? " · " + exam.scope : "") + " · Mock exam";
    $("result-title").textContent = exam.timeUp
      ? "Time's up"
      : t.max
        ? verdict(p)
        : "Mark your answers";
    $("result-lede").textContent = t.max
      ? "You scored " +
        fmtScore(t.score) +
        " out of " +
        t.max +
        (t.pending ? " so far" : "") +
        ". " +
        (p >= 80
          ? "Keep it there with a quick mock before the exam."
          : p >= 50
            ? "Go back over the chapters marked Shaky and Weak below, then try again."
            : "Start with the weakest chapter below before taking another mock.")
      : "Every question in this exam is written. Compare your answers with the model answers below and mark each one.";
    var secs = Math.round((exam.finished - exam.started) / 1000);
    var stats = $("result-stats");
    stats.innerHTML = "";
    [
      [t.right, "right"],
      [t.wrong, "wrong"],
      [clock(secs), exam.limit ? "of " + clock(exam.limit) : "taken"],
    ]
      .concat(t.pending ? [[t.pending, "to mark"]] : [])
      .forEach(function (s) {
        var d = el("div", "stat");
        d.appendChild(el("b", "", String(s[0])));
        d.appendChild(document.createTextNode(s[1]));
        stats.appendChild(d);
      });

    $("pending-note").hidden = !t.pending;
    $("pending-text").textContent = t.pending
      ? t.pending +
        " written answer" +
        (t.pending === 1 ? " needs" : "s need") +
        " marking before your score is complete."
      : "";
    $("pending-go").onclick = function () {
      reviewFilter = "pending";
      renderReview();
      $("review-title").scrollIntoView({ behavior: "smooth" });
    };

    renderChapterResults(t);
    renderNextSteps(t);
    renderReview();
  }
  function fmtScore(s) {
    return s % 1 ? s.toFixed(1) : String(s);
  }
  function verdict(p) {
    return p >= 90
      ? "Exam ready"
      : p >= 80
        ? "Strong result"
        : p >= 65
          ? "Getting there"
          : p >= 50
            ? "Halfway there"
            : "Needs work";
  }

  function chapterRows(t) {
    return Object.keys(t.ch)
      .filter(function (k) {
        return t.ch[k].t;
      })
      .map(function (k) {
        return {
          id: k,
          r: t.ch[k].r,
          t: t.ch[k].t,
          p: pct(t.ch[k].r, t.ch[k].t),
        };
      })
      .sort(function (a, b) {
        if ((a.id === OTHER) !== (b.id === OTHER))
          return a.id === OTHER ? 1 : -1;
        return a.p - b.p || b.t - a.t;
      });
  }

  function renderChapterResults(t) {
    var host = $("ch-results");
    host.innerHTML = "";
    var rows = chapterRows(t);
    if (!rows.length) {
      host.appendChild(
        el(
          "p",
          "muted",
          "Mark your written answers to see how each chapter went.",
        ),
      );
      return;
    }
    rows.forEach(function (r) {
      var row = el("div", "ch-row");
      var name = el("div", "name", shortTitle(chapterTitle(bank, r.id)));
      var c = bank.chById[r.id];
      if (c && c.link && r.p < 80) {
        var a = el("a", "", "Study →");
        a.href = c.link;
        name.appendChild(a);
      }
      var nums = el("div", "nums");
      nums.appendChild(el("span", "", fmtScore(r.r) + "/" + r.t));
      nums.appendChild(el("span", "pill " + band(r.p), bandLabel(r.p)));
      row.appendChild(name);
      row.appendChild(nums);
      row.appendChild(bar(r.p));
      host.appendChild(row);
    });
    if (
      rows.length &&
      rows[0].id !== OTHER &&
      rows.some(function (r) {
        return r.t < 3 && r.id !== OTHER;
      })
    )
      host.appendChild(
        el(
          "p",
          "muted",
          "Chapters with only one or two questions are a rough signal. A longer exam gives a clearer picture.",
        ),
      );
  }

  function renderNextSteps(t) {
    var host = $("next-steps");
    host.innerHTML = "";
    var weak = chapterRows(t).filter(function (r) {
      return r.id !== OTHER && r.p < 80;
    });
    function action(label, sub, fn, primary) {
      var b = el("button", "btn" + (primary ? " primary" : ""));
      b.type = "button";
      b.appendChild(document.createTextNode(label));
      if (sub) b.appendChild(el("span", "", sub));
      b.addEventListener("click", fn);
      host.appendChild(b);
    }
    if (weak.length) {
      action(
        "Practise your weak chapters",
        weak
          .slice(0, 3)
          .map(function (r) {
            return shortTitle(chapterTitle(bank, r.id)).split(" · ")[0];
          })
          .join(", ") +
          (weak.length > 3 ? " and " + (weak.length - 3) + " more" : "") +
          " · new questions first",
        function () {
          backToSetup(
            weak.map(function (r) {
              return r.id;
            }),
          );
        },
        true,
      );
    }
    action(
      "Take another mock exam",
      "Same settings, questions you haven't seen first",
      function () {
        backToSetup(null, true);
      },
      !weak.length,
    );
    action(
      "Change the setup",
      "Different chapters, length or timer",
      function () {
        backToSetup(null);
      },
    );
    if (exam.mistakesAdded) {
      var a = el("a", "btn", "");
      a.href = "/academics/review/";
      a.appendChild(document.createTextNode("Review mistakes"));
      a.appendChild(
        el(
          "span",
          "",
          exam.mistakesAdded +
            " missed question" +
            (exam.mistakesAdded === 1 ? " was" : "s were") +
            " added. They come back tomorrow, then after 3 and 7 days.",
        ),
      );
      host.appendChild(a);
    }
    var plan = el("a", "btn", "");
    plan.href = "/account/calendar/";
    plan.appendChild(document.createTextNode("Open your Study Plan"));
    plan.appendChild(
      el(
        "span",
        "",
        "Your chapter scores show next to your readiness ratings.",
      ),
    );
    host.appendChild(plan);
  }

  function backToSetup(chapterIds, startNow) {
    var course = exam.course;
    exam = null;
    document.title = "Mock Exam Builder | SHOUG.TECH";
    renderResume();
    show("setup");
    $("course").value = course;
    getBank(course).then(function (b) {
      bank = b;
      var all = load(K.settings, {});
      if (chapterIds) {
        all[course] = all[course] || {};
        all[course].chapters = chapterIds;
        all[course].scope = null;
        save(K.settings, all);
      }
      selectCourse(course, false);
      if (startNow)
        setTimeout(function () {
          if (!$("start").disabled) startExam();
        }, 0);
    });
  }

  function renderReview() {
    var t = tally(exam);
    var filters = [
      ["all", "All " + exam.ids.length],
      ["wrong", "Wrong " + (t.wrong + countPart())],
    ];
    if (t.pending) filters.push(["pending", "To mark " + t.pending]);
    var flagged = exam.ids.filter(function (id) {
      return exam.flags[id];
    }).length;
    if (flagged) filters.push(["flagged", "Flagged " + flagged]);
    if (
      !filters.some(function (f) {
        return f[0] === reviewFilter;
      })
    )
      reviewFilter = "all";
    var fh = $("review-filter");
    fh.innerHTML = "";
    filters.forEach(function (f) {
      var b = el("button", "chip", f[1]);
      b.type = "button";
      b.setAttribute("aria-pressed", String(reviewFilter === f[0]));
      b.addEventListener("click", function () {
        reviewFilter = f[0];
        renderReview();
      });
      fh.appendChild(b);
    });
    var host = $("review-list");
    host.innerHTML = "";
    var shown = 0;
    exam.ids.forEach(function (id, i) {
      var q = bank.byId[id];
      if (!q) return;
      var m = markOf(q, exam);
      if (reviewFilter === "wrong" && !(m != null && m < 1)) return;
      if (reviewFilter === "pending" && m != null) return;
      if (reviewFilter === "flagged" && !exam.flags[id]) return;
      host.appendChild(reviewCard(q, i, m));
      shown++;
    });
    if (!shown)
      host.appendChild(
        el(
          "div",
          "empty",
          reviewFilter === "wrong"
            ? "Nothing wrong. Nice work."
            : "Nothing here.",
        ),
      );
  }
  function countPart() {
    return exam.ids.filter(function (id) {
      var q = bank.byId[id];
      var m = q && markOf(q, exam);
      return m != null && m > 0 && m < 1;
    }).length;
  }

  function reviewCard(q, i, m) {
    var state =
      m == null ? "pending" : m >= 1 ? "right" : m > 0 ? "part" : "wrong";
    var card = el("article", "rv " + state);
    var meta = el("div", "rv-meta");
    meta.appendChild(el("span", "", "Q" + (i + 1)));
    meta.appendChild(
      el(
        "span",
        "verdict " + state,
        {
          right: "Right",
          wrong: answered(exam.answers[q.id]) ? "Wrong" : "Not answered",
          part: q.t === "match" ? "Part marks" : "Half marks",
          pending: "Mark this",
        }[state],
      ),
    );
    meta.appendChild(
      el("span", "", shortTitle(chapterTitle(bank, chKey(q))).split(" · ")[0]),
    );
    if (exam.flags[q.id]) meta.appendChild(el("span", "", "Flagged"));
    card.appendChild(meta);
    card.appendChild(html("div", "rv-q", q.q));
    var a = exam.answers[q.id];

    if (q.t === "match") {
      var mul = el("ul", "rv-opts");
      q.pairs.forEach(function (p, i) {
        var pick = Array.isArray(a) ? a[i] : null;
        var ok = pick === i;
        var li = el("li", ok ? "correct picked" : pick != null ? "picked" : "");
        li.appendChild(
          html(
            "span",
            "",
            "<b>" +
              p[0] +
              "</b> → " +
              (pick == null ? "<i>no answer</i>" : q.pairs[pick][1]),
          ),
        );
        if (!ok) li.appendChild(html("span", "tag", "Correct: " + p[1]));
        else li.appendChild(el("span", "tag", "✓"));
        mul.appendChild(li);
      });
      card.appendChild(mul);
    } else if (q.o) {
      var ul = el("ul", "rv-opts");
      exam.order[q.id].forEach(function (oi, pos) {
        var right = q.t === "multi" ? q.a.indexOf(oi) > -1 : q.a === oi;
        var picked =
          q.t === "multi" ? Array.isArray(a) && a.indexOf(oi) > -1 : a === oi;
        var li = el("li", (right ? "correct " : "") + (picked ? "picked" : ""));
        li.appendChild(el("b", "", LETTERS[pos]));
        li.appendChild(html("span", "", q.o[oi]));
        if (right || picked)
          li.appendChild(
            el(
              "span",
              "tag",
              right && picked
                ? "Your answer ✓"
                : right
                  ? "Correct"
                  : "Your answer",
            ),
          );
        ul.appendChild(li);
      });
      card.appendChild(ul);
    } else if (q.t === "fill") {
      var y = el("p", "rv-answer");
      y.appendChild(el("span", "lab", "You wrote"));
      y.appendChild(document.createTextNode(answered(a) ? a : "(nothing)"));
      card.appendChild(y);
      var c = el("p", "rv-answer");
      c.appendChild(el("span", "lab", "Accepted"));
      c.appendChild(document.createTextNode(q.a.join(" / ")));
      card.appendChild(c);
    } else if (q.t === "num") {
      var yn = el("p", "rv-answer");
      yn.appendChild(el("span", "lab", "You wrote"));
      yn.appendChild(document.createTextNode(answered(a) ? a : "(nothing)"));
      card.appendChild(yn);
      var cn = el("p", "rv-answer");
      cn.appendChild(el("span", "lab", "Answer"));
      cn.appendChild(document.createTextNode(correctText(q)));
      card.appendChild(cn);
    } else {
      card.appendChild(el("div", "label", "Your answer"));
      card.appendChild(
        el("div", "rv-yours", answered(a) ? a : "(nothing written)"),
      );
      card.appendChild(el("div", "label", "Model answer"));
      card.appendChild(html("div", "rv-model", q.m));
      var au =
        (exam.auto && exam.auto[q.id]) ||
        (answered(a) || exam.done ? keywordMark(q, a) : null);
      if (au) {
        var kw = el("div", "kw-box");
        kw.appendChild(
          el(
            "div",
            "label",
            au.from === "rubric"
              ? "Key points the question asks for: found " +
                  Math.min(au.found.length, au.need) +
                  " of " +
                  au.need
              : "Key words from the model answer: found " +
                  au.found.length +
                  " (" +
                  au.need +
                  " needed for full marks)",
          ),
        );
        var chips = el("div", "kw-chips");
        au.found.forEach(function (w) {
          chips.appendChild(el("span", "kw hit", "✓ " + w));
        });
        au.missed.forEach(function (w) {
          chips.appendChild(el("span", "kw miss", w));
        });
        kw.appendChild(chips);
        card.appendChild(kw);
      }
      var sm = el("div", "selfmark");
      var NAMES = { 1: "Full", 0.5: "Half", 0: "None" };
      var changed =
        au && exam.marks[q.id] != null && exam.marks[q.id] !== au.mark;
      sm.appendChild(
        el(
          "span",
          "label",
          !au
            ? "Your mark"
            : changed
              ? "Auto mark: " +
                NAMES[au.mark] +
                " · you changed it to " +
                NAMES[exam.marks[q.id]]
              : "Auto mark: " + NAMES[au.mark] + " · change it if you disagree",
        ),
      );
      [
        [1, "Full"],
        [0.5, "Half"],
        [0, "None"],
      ].forEach(function (o) {
        var b = el("button", "btn small", o[1]);
        b.type = "button";
        b.setAttribute("aria-pressed", String(exam.marks[q.id] === o[0]));
        b.addEventListener("click", function () {
          exam.marks[q.id] = o[0];
          record();
          var y0 = window.scrollY;
          renderResults();
          window.scrollTo(0, y0);
        });
        sm.appendChild(b);
      });
      card.appendChild(sm);
    }
    if (q.e) card.appendChild(html("p", "rv-why", q.e));
    var src = bank.sources[q.s];
    var foot = el("p", "rv-src muted");
    if (src) {
      foot.appendChild(document.createTextNode("From "));
      var link = el("a", "", src.title);
      link.href = src.url;
      foot.appendChild(link);
      foot.appendChild(document.createTextNode(" · "));
    }
    var rep = el(
      "button",
      "linkish",
      reported[q.id] ? "Reported, thank you" : "Report a problem",
    );
    rep.type = "button";
    rep.disabled = !!reported[q.id];
    rep.addEventListener("click", function () {
      rep.hidden = true;
      card.appendChild(
        reportForm(
          q,
          src,
          function () {
            rep.textContent = "Reported, thank you";
            rep.disabled = true;
            rep.hidden = false;
          },
          function () {
            rep.hidden = false;
          },
        ),
      );
    });
    foot.appendChild(rep);
    card.appendChild(foot);
    return card;
  }

  // Questions were pulled from many quiz formats automatically, so a wrong key
  // or a broken question can slip through. Reports go to the site admin
  // (Firestore questionReports, signed in) or, signed out, to an email draft.
  var reported = {};
  var REASONS = [
    ["answer", "The marked answer is wrong"],
    ["unclear", "The question is unclear or broken"],
    ["missing", "It needs a figure, table or code that isn't shown"],
    ["chapter", "It's in the wrong chapter"],
    ["other", "Something else"],
  ];
  function reportForm(q, src, done, undo) {
    var f = el("form", "report");
    f.appendChild(el("div", "label", "What's wrong?"));
    var sel = el("select");
    sel.setAttribute("aria-label", "What's wrong");
    REASONS.forEach(function (r) {
      var o = el("option", "", r[1]);
      o.value = r[0];
      sel.appendChild(o);
    });
    var note = el("textarea");
    note.rows = 2;
    note.maxLength = 1000;
    note.placeholder = "Optional: what should it say?";
    note.setAttribute("aria-label", "Details");
    var row = el("div", "row");
    var send = el("button", "btn primary small", "Send report");
    send.type = "submit";
    var cancel = el("button", "btn small", "Cancel");
    cancel.type = "button";
    var status = el("span", "muted");
    row.appendChild(send);
    row.appendChild(cancel);
    row.appendChild(status);
    f.appendChild(sel);
    f.appendChild(note);
    f.appendChild(row);
    cancel.addEventListener("click", function () {
      f.remove();
      undo();
    });
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var data = {
        course: bank.course,
        qid: q.id,
        source: (src && src.url) || "",
        reason: sel.value,
        note: note.value.trim().slice(0, 1000),
        question: plain(q.q).slice(0, 600),
      };
      send.disabled = true;
      status.textContent = "Sending…";
      var sync = window.ShougStudySync;
      (sync && sync.user() ? sync.report(data) : Promise.resolve(false)).then(
        function (ok) {
          if (ok) {
            reported[q.id] = true;
            f.remove();
            done();
            return;
          }
          // Signed out (or the rules aren't live yet): hand over an email draft.
          var body =
            "Course: " +
            bank.name +
            "\nQuestion id: " +
            q.id +
            "\nPage: " +
            location.origin +
            data.source +
            "\nProblem: " +
            sel.options[sel.selectedIndex].text +
            "\n\n" +
            data.question +
            (data.note ? "\n\nNote: " + data.note : "");
          location.href =
            "mailto:shoug.alomran@shoug-tech.com?subject=" +
            encodeURIComponent(
              "Mock exam question report (" + bank.name + ")",
            ) +
            "&body=" +
            encodeURIComponent(body);
          status.textContent =
            "Opened an email draft. Sign in to send reports from here.";
          send.disabled = false;
        },
      );
    });
    setTimeout(function () {
      sel.focus();
    }, 0);
    return f;
  }

  /* --------------------------------------------------------------- boot */

  window.addEventListener("beforeunload", function (e) {
    if (exam && !exam.done && !$("exam").hidden) {
      persist();
      e.preventDefault();
      e.returnValue = "";
    }
  });

  window.addEventListener("shoug:study-sync", function () {
    if (!$("setup").hidden && bank) {
      renderHistory();
      renderChapters();
    }
  });

  fetchJson(BANKS + "index.json").then(
    function (j) {
      index = j;
      initSetup();
    },
    function () {
      $("loading").textContent =
        "Couldn't load the question banks. Check your connection and reload the page.";
    },
  );
})();
