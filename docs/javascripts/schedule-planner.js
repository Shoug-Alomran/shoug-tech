/**
 * Schedule planner (/academics/schedule-planner/).
 *
 * Loads PSU's timetable for one term + campus (docs/data/psu-timetable/, kept
 * fresh by scripts/sync-psu-timetable.js) and the course catalog
 * (docs/data/course-catalog.json), then builds every combination of section
 * groups for the picked courses with no time clash, no class in a free hour,
 * and (unless allowed) no two finals at the same time.
 *
 * A "group" is what a student registers: the lecture plus its lab/tutorial,
 * which share a section number on Edugate (e.g. CYS405 44 = CRN 1309 + 1310).
 *
 * Murshid (murshid.js) reads window.SchedulePlanner for advice and can pick
 * courses through it. Everything the student sets is kept in localStorage.
 */
(function () {
  "use strict";

  var STORE = "shoug_schedule_planner_v1";
  var DATA = "/data/psu-timetable/";
  var MAX_RESULTS = 20000;
  // English / Arabic. The choice is the site-wide "shoug-lang" (localStorage)
  // and <html lang dir>; every string below goes through L(english, arabic).
  function isAr() {
    return String(document.documentElement.lang || "").toLowerCase().indexOf("ar") === 0;
  }
  function L(en, ar) {
    return isAr() ? ar : en;
  }
  var DAY_NAMES, DAY_SHORT, DAY_TINY, TYPE, LEVEL;
  function setLanguageData() {
    DAY_NAMES = isAr()
      ? ["الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"]
      : ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    DAY_SHORT = isAr()
      ? ["أحد", "اثنين", "ثلاثاء", "أربعاء", "خميس", "جمعة", "سبت"]
      : ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    DAY_TINY = isAr() ? ["ح", "ن", "ث", "ر", "خ", "ج", "س"] : ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"];
    TYPE = isAr()
      ? { L: "محاضرة", B: "معمل", T: "تمارين", S: "مرسم", C: "تدريب تعاوني" }
      : { L: "Lecture", B: "Lab", T: "Tutorial", S: "Studio", C: "Co-op" };
    LEVEL = isAr()
      ? { light: "خفيف", fine: "مناسب", heavy: "ثقيل", "very heavy": "ثقيل جدًا" }
      : { light: "light", fine: "fine", heavy: "heavy", "very heavy": "very heavy" };
  }
  setLanguageData();
  function dateLocale() {
    return isAr() ? "ar-SA-u-ca-gregory-nu-latn" : "en-GB";
  }
  /** "Sun, Mon" / "Sun–Thu" / "Monday" for a list of days. */
  function daysText(days) {
    if (!days || !days.length || days.length >= 5) return "";
    if (days.length === 1) return DAY_NAMES[days[0]];
    var run = days.every(function (d, i) { return !i || d === days[i - 1] + 1; });
    if (run && days.length > 2) return DAY_SHORT[days[0]] + "–" + DAY_SHORT[days[days.length - 1]];
    return days.map(function (d) { return DAY_SHORT[d]; }).join(L(", ", "، "));
  }
  var COLORS = [
    "#8b5cf6",
    "#0ea5e9",
    "#10b981",
    "#f59e0b",
    "#ef4444",
    "#ec4899",
    "#14b8a6",
    "#6366f1",
    "#84cc16",
    "#f97316",
  ];
  // Mask: 5-minute slots from 07:00 to 22:00, 7 days.
  var SLOT0 = 7 * 60,
    SLOTS = 180,
    WORDS_PER_DAY = Math.ceil(SLOTS / 32);
  var PRESETS = {
    early: function (add) {
      for (var d = 0; d < 5; d++) {
        add(d, 7);
        add(d, 8);
      }
    },
    late: function (add) {
      for (var d = 0; d < 5; d++) for (var h = 14; h < 22; h++) add(d, h);
    },
    thu: function (add) {
      for (var h = 7; h < 22; h++) add(4, h);
    },
    sun: function (add) {
      for (var h = 7; h < 22; h++) add(0, h);
    },
  };

  var $ = function (id) {
    return document.getElementById(id);
  };
  var esc = function (s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;",
      }[c];
    });
  };

  var state = load();
  var index = null; // index.json
  var term = null; // current term file
  var catalog = {}; // course-catalog.json courses
  var byCourse = {}; // code -> { g -> [sections] }
  var options = {}; // code -> [option]
  var results = []; // [[option, …]]
  var current = 0;
  var leftOut = []; // [{code, reason}]
  var ratings = {}; // code -> summary | null (no ratings) ; undefined = not loaded
  var loadedRatings = {};

  function load() {
    var s = {};
    try {
      s = JSON.parse(localStorage.getItem(STORE)) || {};
    } catch (e) {}
    return {
      term: s.term || null,
      campus: s.campus || "f",
      dept: s.dept || "",
      picked: s.picked || [],
      excluded: s.excluded || {},
      closed: s.closed !== false,
      finalClash: !!s.finalClash,
      // 12–1 is the university break, so it is never a free-time choice.
      blocks: (s.blocks || []).filter(function (k) { return !/-12$/.test(k); }),
      presets: (s.presets || []).filter(function (p) { return p !== "noon"; }),
      sort: s.sort || "days",
      freeText: s.freeText || "",
      pinned: s.pinned || {}, // code -> section group the student chose
      showPassed: !!s.showPassed,
      textRules: s.textRules || { rules: [], maxDays: null, preferGaps: false, unknown: [] },
      // One entry per schedule (term + campus + sections), oldest kept.
      saved: (s.saved || []).filter(function (x, i, all) {
        return all.findIndex(function (y) {
          return y.key === x.key && y.term === x.term && y.campus === x.campus;
        }) === i;
      }),
    };
  }
  function persist() {
    try {
      localStorage.setItem(STORE, JSON.stringify(state));
    } catch (e) {}
  }

  function toast(msg) {
    var t = $("toast");
    t.textContent = msg;
    t.classList.add("show");
    clearTimeout(toast.timer);
    toast.timer = setTimeout(function () {
      t.classList.remove("show");
    }, 2200);
  }

  function clockFull(mins) {
    return clock(mins);
  }
  function clock(mins) {
    var h = Math.floor(mins / 60),
      m = mins % 60;
    var ap = h >= 12 ? L("PM", "م") : L("AM", "ص");
    var h12 = h % 12 || 12;
    return h12 + ":" + String(m).padStart(2, "0") + " " + ap;
  }
  function examDate(x) {
    return new Date(
      x.slice(0, 4),
      +x.slice(5, 7) - 1,
      +x.slice(8, 10),
      +x.slice(11, 13),
      +x.slice(14, 16),
    );
  }
  function examLabel(x) {
    var d = examDate(x);
    return (
      d.toLocaleDateString(dateLocale(), {
        weekday: "short",
        day: "numeric",
        month: "short",
      }) +
      " · " +
      clock(d.getHours() * 60 + d.getMinutes())
    );
  }

  // ── Data ────────────────────────────────────────────────────────────────

  function fetchJson(url) {
    return fetch(url, { cache: "no-cache" }).then(function (r) {
      if (!r.ok) throw new Error(url + " " + r.status);
      return r.json();
    });
  }

  function boot() {
    Promise.all([
      fetchJson(DATA + "index.json"),
      fetchJson("/data/course-catalog.json"),
    ])
      .then(function (res) {
        index = res[0];
        catalog = (res[1] && res[1].courses) || {};
        var terms = (index.terms || []).filter(function (t) {
          return (
            index.files[t.value + "-f.json"] || index.files[t.value + "-m.json"]
          );
        });
        if (!terms.length) throw new Error("No timetable files");
        if (
          !state.term ||
          !terms.some(function (t) {
            return t.value === state.term;
          })
        )
          state.term = terms[terms.length - 1].value;
        $("term").innerHTML = terms
          .map(function (t) {
            return (
              '<option value="' +
              t.value +
              '"' +
              (t.value === state.term ? " selected" : "") +
              ">" +
              esc(termName(t)) +
              "</option>"
            );
          })
          .join("");
        buildMajors(index.departments || []);
        renderMajor();
        return loadTerm();
      })
      .catch(function (err) {
        console.error(err);
        $("updated").textContent = L("Timetable unavailable", "الجدول غير متاح");
        $("notice").innerHTML =
          '<div class="notice">' + L("<b>The timetable couldn't load.</b> Check your connection and refresh. If it keeps happening, the data may not have been published yet.", "<b>تعذّر تحميل الجدول.</b> تحقق من الاتصال وحدّث الصفحة. إذا تكرر ذلك فربما لم تُنشر البيانات بعد.") + "</div>";
      });
  }

  function termName(t) {
    // "الفصل الثاني 2026/2027" → "Second term 2026/27"
    var y = t.label.match(/(\d{4})\s*\/\s*(\d{4})/) || [];
    var years = y[1] ? " " + y[1] + "/" + y[2].slice(2) : "";
    if (isAr())
      return ({ 1: "الفصل الأول", 2: "الفصل الثاني", 3: "الفصل الصيفي" }[t.value.slice(-1)] || "الفصل") + years;
    var n =
      { 1: "First", 2: "Second", 3: "Summer" }[t.value.slice(-1)] || "Term";
    return n + " term" + years;
  }

  function renderUpdated() {
    if (!term) return;
    var d = new Date(term.updatedAt);
    $("updated").textContent =
      L("Last update: ", "آخر تحديث: ") +
      d.toLocaleDateString(dateLocale(), { day: "numeric", month: "short" }) +
      (isAr() ? "، " : ", ") +
      d.toLocaleTimeString(dateLocale(), { hour: "2-digit", minute: "2-digit" });
    $("updated").title = L("From PSU Edugate. Refreshed automatically every few hours.", "من بوابة جامعة الأمير سلطان (Edugate)، ويُحدَّث تلقائيًا كل بضع ساعات.");
  }

  function loadTerm() {
    var file = state.term + "-" + state.campus + ".json";
    $("updated").textContent = L("Loading…", "جارٍ التحميل…");
    return fetchJson(DATA + file)
      .then(function (data) {
        term = data;
        byCourse = {};
        data.sections.forEach(function (s) {
          var c = (byCourse[s.c] = byCourse[s.c] || {});
          (c[s.g] = c[s.g] || []).push(s);
        });
        renderUpdated();
        var missing = state.picked.filter(function (c) {
          return !byCourse[c];
        });
        if (missing.length)
          toast(missing.join(", ") + L(" isn't offered this term", " غير مطروحة هذا الفصل"));
        state.picked = state.picked.filter(function (c) {
          return byCourse[c];
        });
        persist();
        syncControls();
        renderList();
        regenerate();
      })
      .catch(function () {
        $("updated").textContent = L("No timetable for this campus yet", "لا يوجد جدول لهذا المقر بعد");
        term = null;
        byCourse = {};
        renderList();
        regenerate();
      });
  }

  // ── Options (one per section group) ────────────────────────────────────

  function emptyMask() {
    return new Uint32Array(WORDS_PER_DAY * 7);
  }
  function markMask(mask, day, start, end) {
    var a = Math.max(0, Math.floor((start - SLOT0) / 5));
    var b = Math.min(SLOTS, Math.ceil((end - SLOT0) / 5));
    for (var k = a; k < b; k++)
      mask[day * WORDS_PER_DAY + (k >> 5)] |= 1 << (k & 31);
  }
  function overlaps(a, b) {
    for (var i = 0; i < a.length; i++) if (a[i] & b[i]) return true;
    return false;
  }

  function blockedSet() {
    var set = {};
    var add = function (d, h) {
      set[d + "-" + h] = true;
    };
    state.blocks.forEach(function (k) {
      set[k] = true;
    });
    state.presets.forEach(function (p) {
      if (PRESETS[p]) PRESETS[p](add);
    });
    if (window.ShougFreeTime)
      window.ShougFreeTime.hours(state.textRules.rules).forEach(function (k) {
        set[k] = true;
      });
    return set;
  }

  function buildOptions(code, blocked) {
    var groups = byCourse[code] || {};
    var all = [],
      reasons = { closed: 0, blocked: 0, excluded: 0 };
    var excluded = state.excluded[code] || [];
    Object.keys(groups).forEach(function (g) {
      var secs = groups[g].slice().sort(function (a, b) {
        return "LBTSC".indexOf(a.t) - "LBTSC".indexOf(b.t);
      });
      var meetings = [];
      secs.forEach(function (s) {
        s.m.forEach(function (m) {
          meetings.push({
            d: m[0],
            s: m[1],
            e: m[2],
            room: m[3],
            t: s.t,
            i: s.i,
            o: s.o,
            crn: s.crn,
          });
        });
      });
      var mask = emptyMask();
      meetings.forEach(function (m) {
        markMask(mask, m.d, m.s, m.e);
      });
      var exam =
        (
          secs.find(function (s) {
            return s.x;
          }) || {}
        ).x || null;
      var opt = {
        code: code,
        g: g,
        secs: secs,
        meetings: meetings,
        mask: mask,
        exam: exam,
        open: secs.every(function (s) {
          return s.o;
        }),
        instructor: (
          secs.find(function (s) {
            return s.t === "L";
          }) || secs[0]
        ).i,
        crns: secs.map(function (s) {
          return s.crn;
        }),
      };
      all.push(opt);
      if (state.pinned[code]) {
        if (state.pinned[code] === g) opt.ok = true;
        return;
      }
      if (excluded.indexOf(g) > -1) return reasons.excluded++;
      if (!state.closed && !opt.open) return reasons.closed++;
      var hit = meetings.some(function (m) {
        for (var h = Math.floor(m.s / 60); h * 60 < m.e; h++)
          if (blocked[m.d + "-" + h]) return true;
        return false;
      });
      if (hit) return reasons.blocked++;
      opt.ok = true;
    });
    all.sort(function (a, b) {
      return (+a.g || 0) - (+b.g || 0);
    });
    return {
      all: all,
      usable: all.filter(function (o) {
        return o.ok;
      }),
      reasons: reasons,
    };
  }

  // ── Generation ─────────────────────────────────────────────────────────

  function regenerate(keepView) {
    var prevKey = keepView && results[current] ? keyOf(results[current]) : null;
    var blocked = blockedSet();
    options = {};
    leftOut = [];
    var lists = [];
    state.picked.forEach(function (code) {
      var o = buildOptions(code, blocked);
      options[code] = o;
      if (!o.usable.length) {
        var r = o.reasons,
          why = [];
        if (r.blocked) why.push(r.blocked + L(" clash with your free time", " تتعارض مع وقت فراغك"));
        if (r.closed) why.push(r.closed + L(" closed", " مغلقة"));
        if (r.excluded) why.push(r.excluded + L(" you turned off", " أُوقفت يدويًا"));
        leftOut.push({ code: code, reason: why.join(L(", ", "، ")) || L("no sections", "لا توجد شعب") });
      } else lists.push(o.usable);
    });
    lists.sort(function (a, b) {
      return a.length - b.length;
    });

    results = [];
    var capped = false;
    var masks = [emptyMask()];
    var picks = [];
    var exams = {};
    (function walk(level) {
      if (results.length >= MAX_RESULTS) {
        capped = true;
        return;
      }
      if (level === lists.length) {
        if (level) results.push(picks.slice());
        return;
      }
      var acc = masks[level];
      for (var i = 0; i < lists[level].length; i++) {
        var o = lists[level][i];
        if (overlaps(acc, o.mask)) continue;
        if (!state.finalClash && o.exam && exams[o.exam]) continue;
        var next = new Uint32Array(acc);
        for (var w = 0; w < next.length; w++) next[w] |= o.mask[w];
        masks[level + 1] = next;
        picks.push(o);
        if (o.exam) exams[o.exam] = (exams[o.exam] || 0) + 1;
        walk(level + 1);
        picks.pop();
        if (o.exam && !--exams[o.exam]) delete exams[o.exam];
        if (capped) return;
      }
    })(0);
    results.capped = capped;
    results.forEach(function (r) {
      r.metrics = metrics(r);
    });
    results.beforeMaxDays = results.length;
    var maxDays = state.textRules.maxDays;
    if (maxDays) {
      var kept = results.filter(function (r) { return r.metrics.days <= maxDays; });
      kept.capped = results.capped;
      kept.beforeMaxDays = results.length;
      results = kept;
    }
    sortResults();
    current = 0;
    if (prevKey) {
      var at = results.findIndex(function (r) {
        return keyOf(r) === prevKey;
      });
      if (at > -1) current = at;
    }
    fetchRatings();
    render();
  }

  function isSaved(key) {
    return state.saved.some(function (s) {
      return s.key === key && s.term === state.term && s.campus === state.campus;
    });
  }

  function keyOf(schedule) {
    return schedule
      .map(function (o) {
        return o.code + ":" + o.g;
      })
      .sort()
      .join(",");
  }

  function metrics(schedule) {
    var perDay = {};
    schedule.forEach(function (o) {
      o.meetings.forEach(function (m) {
        (perDay[m.d] = perDay[m.d] || []).push([m.s, m.e]);
      });
    });
    var days = Object.keys(perDay).map(Number);
    var gaps = 0,
      longDays = 0,
      eights = 0,
      startSum = 0,
      endSum = 0,
      longest = 0;
    days.forEach(function (d) {
      var iv = perDay[d].sort(function (a, b) {
        return a[0] - b[0];
      });
      var end = iv[0][1];
      for (var i = 1; i < iv.length; i++) {
        if (iv[i][0] - end > 15) gaps += iv[i][0] - end;
        end = Math.max(end, iv[i][1]);
      }
      var span = end - iv[0][0];
      longest = Math.max(longest, span);
      if (span > 6 * 60) longDays++;
      if (iv[0][0] < 9 * 60) eights++;
      startSum += iv[0][0];
      endSum += end;
    });
    var ex = schedule
      .filter(function (o) {
        return o.exam;
      })
      .map(function (o) {
        return { code: o.code, x: o.exam, t: examDate(o.exam).getTime() };
      })
      .sort(function (a, b) {
        return a.t - b.t;
      });
    var sameDay = 0,
      within24 = 0,
      clashes = 0,
      minGap = Infinity;
    for (var i = 1; i < ex.length; i++) {
      var dh = (ex[i].t - ex[i - 1].t) / 36e5;
      minGap = Math.min(minGap, dh);
      if (dh === 0) clashes++;
      else if (ex[i].x.slice(0, 10) === ex[i - 1].x.slice(0, 10)) sameDay++;
      else if (dh < 24) within24++;
    }
    return {
      days: days.length,
      dayList: days.sort(),
      gaps: gaps,
      longDays: longDays,
      eights: eights,
      longest: longest,
      avgStart: days.length ? startSum / days.length : 0,
      avgEnd: days.length ? endSum / days.length : 0,
      exams: ex,
      sameDay: sameDay,
      within24: within24,
      clashes: clashes,
      minExamGap: minGap,
      closed: schedule.filter(function (o) {
        return !o.open;
      }).length,
    };
  }

  // ── Load estimate ──────────────────────────────────────────────────────

  function hoursOf(code) {
    var t = term && term.courses[code];
    return (t && t.h) || (catalog[code] && catalog[code].h) || 3;
  }

  /** Difficulty 1–5: student ratings when there are any, else a guess from the course level. */
  function difficulty(code) {
    var r = ratings[code];
    var out;
    if (r && r.difficulty) out = { value: r.difficulty, rated: true, n: r.n };
    else {
      var lvl = +(code.match(/\d/) || ["1"])[0];
      out = { value: [2.2, 2.3, 2.7, 3, 3.3, 3.4][Math.min(lvl, 5)], rated: false, n: 0 };
    }
    out.base = out.value;
    var me = personal(code);
    if (me) {
      out.personal = me;
      out.value = Math.max(1, Math.min(5, out.value + me.shift));
    }
    return out;
  }

  // ── Your grades (users/{uid}/private/data → academicRecord.courses) ─────
  // Grades never leave the browser: they only nudge the difficulty of each
  // picked course up or down, using finished courses that are related to it.

  var grades = {}; // "CS331" -> { letter, points }
  var POINTS = { "A+": 4, A: 3.75, "B+": 3.5, B: 3, "C+": 2.5, C: 2, "D+": 1.5, D: 1, F: 0, DN: 0 };
  var GENERIC = "introduction intro fundamentals fundamental basics basic overview review part chapter concepts concept principles using with from into their your what that this and the for are management advanced applications application methods method topics systems system data software computer computing course study case managing working understanding development including other".split(" ");

  function loadGrades() {
    withFirebase(function (fb) {
      if (!fb || !fb.auth) return;
      fb.auth().onAuthStateChanged(function (user) {
        grades = {};
        if (!user || !window.ShougPrivate) return render();
        window.ShougPrivate.ready(user.uid)
          .then(function (ref) { return ref.get(); })
          .then(function (snap) {
            var record = (snap && snap.exists && snap.data().academicRecord) || {};
            var courses = record.courses || {};
            Object.keys(courses).forEach(function (raw) {
              var c = courses[raw] || {};
              if (c.finished === false || POINTS[c.letter] === undefined) return;
              grades[raw.replace(/\s+/g, "").toUpperCase()] = { letter: c.letter, points: POINTS[c.letter] };
            });
            if (state.sort === "load") sortResults();
            render();
          })
          .catch(function () {});
      });
    });
  }

  function topicWords(entry) {
    var out = {};
    ((entry && entry.chapters) || []).forEach(function (title) {
      title.toLowerCase().split(/[^a-z0-9+#]+/).forEach(function (w) {
        if (w.length >= 4 && GENERIC.indexOf(w) < 0) out[w.slice(0, 6)] = true;
      });
    });
    return out;
  }

  /** Courses passed: "completed" in any plan grid, or a grade of D or better (W, F, DN don't count). */
  function passedCourses() {
    var out = {};
    Object.keys(grades).forEach(function (c) { if (grades[c].points >= 1) out[c] = true; });
    Object.keys(PLAN_GRID_KEYS).forEach(function (k) {
      var saved = null;
      try { saved = JSON.parse(localStorage.getItem(PLAN_GRID_KEYS[k]) || "null"); } catch (e) {}
      var map = (saved && saved.statusMap) || {};
      Object.keys(map).forEach(function (c) { if (map[c] === "completed") out[c.replace(/\s+/g, "").toUpperCase()] = true; });
    });
    return out;
  }

  /** Finished, graded courses most like `code`, and how they shift its difficulty. */
  function personal(code) {
    var graded = Object.keys(grades);
    if (!graded.length) return null;
    var e = catalog[code] || {};
    var prefix = code.replace(/\d.*$/, "");
    var direct = e.pre || [];
    var second = [];
    direct.forEach(function (p) { ((catalog[p] && catalog[p].pre) || []).forEach(function (q) { second.push(q); }); });
    var mine = topicWords(e);
    var scored = graded
      .filter(function (g) { return g !== code; })
      .map(function (g) {
        var weight = 0, why = [];
        if (direct.indexOf(g) > -1) { weight += 3; why.push("prerequisite"); }
        else if (second.indexOf(g) > -1) { weight += 1.5; why.push("builds toward it"); }
        if (g.replace(/\d.*$/, "") === prefix) { weight += 1; if (!why.length) why.push("same subject"); }
        var theirs = topicWords(catalog[g]);
        var shared = Object.keys(mine).filter(function (w) { return theirs[w]; }).length;
        if (shared >= 2) { weight += 2; if (why.indexOf("prerequisite") < 0) why.push("similar topics"); }
        return { code: g, letter: grades[g].letter, points: grades[g].points, weight: weight, why: why[0] || "" };
      })
      .filter(function (x) { return x.weight >= 1.5; })
      .sort(function (a, b) { return b.weight - a.weight; })
      .slice(0, 4);
    if (!scored.length) return null;
    var total = 0, sum = 0;
    scored.forEach(function (x) { total += x.weight; sum += x.weight * x.points; });
    var avg = sum / total;
    // A strong record in related courses makes a course lighter for you, a weak one heavier.
    var shift = avg >= 3.75 ? -0.6 : avg >= 3.25 ? -0.3 : avg >= 2.5 ? 0 : avg >= 2 ? 0.4 : 0.8;
    return { avg: avg, shift: shift, related: scored };
  }

  function loadOf(schedule) {
    var m = schedule.metrics || metrics(schedule);
    var hours = 0,
      weighted = 0,
      rated = 0,
      mine = 0;
    schedule.forEach(function (o) {
      var h = hoursOf(o.code),
        d = difficulty(o.code);
      hours += h;
      weighted += h * (0.6 + 0.2 * d.value);
      if (d.rated) rated++;
      if (d.personal) mine++;
    });
    var parts = [
      [L("Courses and difficulty", "المواد وصعوبتها"), (weighted / 18) * 45],
      [L("Long days (over 6 hours)", "أيام طويلة (أكثر من 6 ساعات)"), m.longDays * 2.5],
      [L("Gaps between classes", "الفراغات بين المحاضرات"), (m.gaps / 60) * 1.5],
      [L("Days starting before 9", "أيام تبدأ قبل 9"), m.eights * 0.8],
      [L("Days on campus", "أيام الحضور"), m.days >= 5 ? 3 : 0],
      [
        L("Finals close together", "اختبارات نهائية متقاربة"),
        m.sameDay * 6 + m.within24 * 3 + m.clashes * 10,
      ],
    ];
    var score = Math.min(
      100,
      parts.reduce(function (a, p) {
        return a + p[1];
      }, 0),
    );
    var level =
      score < 40
        ? "light"
        : score < 60
          ? "fine"
          : score < 75
            ? "heavy"
            : "very heavy";
    return {
      score: score,
      level: level,
      parts: parts,
      hours: hours,
      rated: rated,
      personal: mine,
      total: schedule.length,
    };
  }

  function sortResults() {
    var by =
      {
        days: function (m) {
          return [m.days, m.gaps, -m.avgStart];
        },
        gaps: function (m) {
          return [m.gaps, m.days, -m.avgStart];
        },
        late: function (m) {
          return [-m.avgStart, m.days, m.gaps];
        },
        early: function (m) {
          return [m.avgEnd, m.days, m.gaps];
        },
        finals: function (m) {
          return [
            m.clashes,
            m.sameDay,
            m.within24,
            -Math.min(m.minExamGap, 1e6),
            m.days,
          ];
        },
        load: function (m, r) {
          return [Math.round(loadOf(r).score), m.days, m.gaps];
        },
      }[state.sort] ||
      function (m) {
        return [m.days];
      };
    results.forEach(function (r) {
      r.sortKey = by(r.metrics, r).concat([r.metrics.closed]);
    });
    results.sort(function (a, b) {
      for (var i = 0; i < a.sortKey.length; i++)
        if (a.sortKey[i] !== b.sortKey[i]) return a.sortKey[i] - b.sortKey[i];
      return 0;
    });
  }

  // ── Ratings (courseRatings/{course}/ratings, public read) ──────────────

  function withFirebase(cb) {
    if (window.__shoug_fb) return cb(window.__shoug_fb);
    window.addEventListener(
      "shoug:fb",
      function () {
        cb(window.__shoug_fb);
      },
      { once: true },
    );
  }

  function summarize(docs) {
    var keys = {
      workload: [],
      assignmentDifficulty: [],
      projectDifficulty: [],
      labDifficulty: [],
      overall: [],
      exams: [],
    };
    docs.forEach(function (d) {
      Object.keys(keys).forEach(function (k) {
        if (k === "exams") {
          if (d.exams && typeof d.exams === "object")
            Object.keys(d.exams).forEach(function (e) {
              var v = d.exams[e];
              if (v >= 1 && v <= 5 && v % 1 === 0) keys.exams.push(v);
            });
        } else if (d[k] >= 1 && d[k] <= 5) keys[k].push(d[k]);
      });
    });
    var avg = function (a) {
      return a.length
        ? a.reduce(function (x, y) {
            return x + y;
          }, 0) / a.length
        : null;
    };
    var out = { n: docs.length };
    Object.keys(keys).forEach(function (k) {
      out[k] = avg(keys[k]);
    });
    var diff = [
      out.workload,
      out.assignmentDifficulty,
      out.exams,
      out.projectDifficulty,
      out.labDifficulty,
    ].filter(function (v) {
      return v != null;
    });
    out.difficulty = diff.length ? avg(diff) : null;
    return out;
  }

  function fetchRatings() {
    var need = state.picked.filter(function (c) {
      return !loadedRatings[c];
    });
    if (!need.length) return;
    need.forEach(function (c) {
      loadedRatings[c] = true;
    });
    withFirebase(function (fb) {
      if (!fb || !fb.firestore) return;
      Promise.all(
        need.map(function (code) {
          return fb
            .firestore()
            .collection("courseRatings")
            .doc(code.toLowerCase())
            .collection("ratings")
            .get()
            .then(function (snap) {
              var docs = [];
              snap.forEach(function (d) {
                docs.push(d.data());
              });
              ratings[code] = docs.length ? summarize(docs) : null;
            })
            .catch(function () {
              ratings[code] = null;
            });
        }),
      ).then(function () {
        if (state.sort === "load") {
          sortResults();
        }
        render();
      });
    });
  }

  // ── Rendering ──────────────────────────────────────────────────────────

  function colorOf(code) {
    var i = state.picked.indexOf(code);
    return COLORS[(i < 0 ? 0 : i) % COLORS.length];
  }
  function nameOf(code) {
    var c = catalog[code];
    var ar = (term && term.courses[code] && term.courses[code].ar) || (c && c.ar);
    return (isAr() ? ar || (c && c.en) : (c && c.en) || ar) || code;
  }

  // ── Majors ─────────────────────────────────────────────────────────────
  // Edugate lists 60+ "departments": each major, its preparatory year
  // (PYP-…), its tracks (SE-CYS) or minors (ACC_MKT), and a few leftovers
  // (LAW--). They're folded into ~22 majors by their Arabic name, so the
  // picker is: major, then track/minor chips, then a prep-year tick.
  var majors = {}; // key -> { key, ar, en, college, main, prep, aliases[], tracks[] }
  var MAJOR_EN = {
    SE: "Software Engineering", CS: "Computer Science", IS: "Information Systems",
    FINANCE: "Finance", ACC: "Accounting", MKT: "Marketing", AVM: "Aviation Management", HRM: "Human Resource Management",
    "PROD.MNGT": "Engineering Management (Production)", EE: "Electrical Engineering", CEE: "Civil & Environmental Engineering",
    ISE: "Industrial & Systems Engineering", ME: "Mechanical Engineering", LAW: "Law", LAM: "Language & Media",
    ASDS: "Applied Statistics & Data Science", ETRA: "Translation", ARCH: "Architecture", ID: "Interior Design",
    "PYP-MBBS": "Medicine & Surgery", "PYP-AL": "Applied Linguistics", "PYP-ACTS": "Actuarial Science",
  };
  var TRACK_EN = {
    CYS: "Cybersecurity", "AI&DS": "AI & Data Science", DX: "Digital Transformation",
    ACC: "Accounting", AVM: "Aviation Management", FIN: "Finance", MKT: "Marketing", ID: "Interior Design", ARCH: "Architecture",
  };
  var COLLEGE_EN = {
    "علوم الحاسب والمعلومات": "Computer & Information Sciences", "إدارة الأعمال": "Business Administration",
    "الهندسة": "Engineering", "القانون": "Law", "العلوم والدراسات الإنسانية": "Humanities & Sciences",
    "العمارة والتصميم": "Architecture & Design", "عمادة السنة التحضيرية": "Preparatory Year", "البنات": "Women's Campus",
  };
  var COLLEGE_ORDER = ["علوم الحاسب والمعلومات", "إدارة الأعمال", "الهندسة", "القانون", "العلوم والدراسات الإنسانية", "العمارة والتصميم", "عمادة السنة التحضيرية"];

  function arabicKey(name) {
    // "تحضيري هندسة برمجيات" and "هندسة البرمجيات" → "هندسة برمجيات"
    return String(name)
      .replace(/\(.*\)/, "").replace(/-+/g, " ").replace(/^\s*تحضيري\s+/, "")
      .replace(/ـ/g, "").trim().split(/\s+/)
      .map(function (w) { return w.replace(/^وال/, "و").replace(/^(ال|لل)/, ""); })
      .join(" ");
  }
  function cleanCollege(c) { return String(c || "").replace(/ـ/g, "").trim(); }

  function buildMajors(depts) {
    majors = {};
    depts.forEach(function (d) {
      var key = arabicKey(d.name);
      var m = (majors[key] = majors[key] || { key: key, ar: "", college: "", main: null, prep: null, aliases: [], tracks: [] });
      var paren = String(d.name).match(/\((.*)\)/);
      if (/^PYP/.test(d.code)) {
        m.prep = d.code;
        if (!m.ar) m.ar = String(d.name).replace(/^\s*تحضيري\s+/, "");
      } else if (paren) {
        var suffix = d.code.split(/[-_]/).pop();
        m.tracks.push({ code: d.code, ar: paren[1].replace(/تخصص فرعي\s*/, "").trim(), en: TRACK_EN[suffix] || suffix, minor: /تخصص فرعي/.test(paren[1]) });
      } else if (!m.main && !/--$/.test(d.code) && !/^\d+$/.test(d.code)) {
        m.main = d.code;
        m.ar = String(d.name).replace(/-+$/, "");
        m.college = cleanCollege(d.college);
      } else m.aliases.push(d.code);
    });
    Object.keys(majors).forEach(function (k) {
      var m = majors[k];
      if (!m.main && m.aliases.length) m.main = m.aliases.shift();
      if (!m.college) m.college = cleanCollege((depts.filter(function (d) { return d.code === (m.main || m.prep); })[0] || {}).college);
      m.en = MAJOR_EN[m.main] || MAJOR_EN[m.prep] || null;
    });
  }

  function majorOf(code) {
    if (!code) return null;
    return Object.keys(majors).map(function (k) { return majors[k]; }).filter(function (m) {
      return m.main === code || m.prep === code || m.aliases.indexOf(code) > -1 || m.tracks.some(function (t) { return t.code === code; });
    })[0] || null;
  }

  /** The Edugate department codes the current choice covers (a major includes its leftover duplicates). */
  function deptCodes() {
    var m = majorOf(state.dept);
    if (m && state.dept === m.main) return [m.main].concat(m.aliases);
    return [state.dept];
  }

  function majorName(m) { return isAr() || !m.en ? m.ar : m.en; }

  function renderMajor() {
    var list = Object.keys(majors).map(function (k) { return majors[k]; });
    var current = majorOf(state.dept);
    var groups = {};
    list.forEach(function (m) { (groups[m.college] = groups[m.college] || []).push(m); });
    var order = COLLEGE_ORDER.filter(function (c) { return groups[c]; }).concat(Object.keys(groups).filter(function (c) { return COLLEGE_ORDER.indexOf(c) < 0; }));
    $("major").innerHTML = '<option value="">' + L("All majors", "كل التخصصات") + "</option>" + order.map(function (c) {
      var label = isAr() ? c : COLLEGE_EN[c] || c;
      return '<optgroup label="' + esc(label) + '">' + groups[c]
        .sort(function (a, b) { return majorName(a).localeCompare(majorName(b), isAr() ? "ar" : "en"); })
        .map(function (m) { return '<option value="' + esc(m.key) + '"' + (current === m ? " selected" : "") + ">" + esc(majorName(m)) + "</option>"; })
        .join("") + "</optgroup>";
    }).join("");
    var extra = $("major-extra");
    if (!current) { extra.hidden = true; return; }
    var inPrep = state.dept === current.prep && !!current.main;
    var hasTracks = current.tracks.length > 0;
    extra.hidden = !hasTracks && !(current.prep && current.main);
    var minors = hasTracks && current.tracks.every(function (t) { return t.minor; });
    $("major-tracks-label").textContent = minors ? L("Minor", "التخصص الفرعي") : L("Track", "المسار");
    $("major-tracks-wrap").hidden = !hasTracks || inPrep;
    $("major-tracks").innerHTML = hasTracks
      ? ['<button type="button" class="chip" data-track="" aria-pressed="' + (state.dept === current.main || current.aliases.indexOf(state.dept) > -1) + '">' + (minors ? L("No minor", "بدون") : L("General", "عام")) + "</button>"]
          .concat(current.tracks.map(function (t) {
            return '<button type="button" class="chip" data-track="' + esc(t.code) + '" aria-pressed="' + (state.dept === t.code) + '">' + esc(isAr() ? t.ar : t.en) + "</button>";
          })).join("")
      : "";
    $("major-prep-row").hidden = !(current.prep && current.main);
    $("major-prep").checked = inPrep;
  }

  function syncControls() {
    document.querySelectorAll("[data-campus]").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.dataset.campus === state.campus));
    });
    document.querySelectorAll("[data-preset]").forEach(function (b) {
      b.setAttribute(
        "aria-pressed",
        String(state.presets.indexOf(b.dataset.preset) > -1),
      );
    });
    $("opt-closed").checked = state.closed;
    $("opt-final-clash").checked = state.finalClash;
    $("sort").value = state.sort;
    $("picked-count").textContent = state.picked.length + L(" picked", " مختارة");
  }

  function renderList() {
    var list = $("course-list");
    if (!term) {
      list.innerHTML = "";
      return;
    }
    var q = $("search").value.trim().toLowerCase();
    // Courses already passed (plan grid "completed", or a passing grade) are
    // hidden unless the student asks to see them or has picked them.
    var passed = passedCourses();
    var hiddenPassed = 0;
    var codes = Object.keys(term.courses).filter(function (code) {
      if (passed[code] && !state.showPassed && state.picked.indexOf(code) < 0) {
        if (!state.dept || deptCodes().some(function (x) { return term.courses[code].d.indexOf(x) > -1; })) hiddenPassed++;
        return false;
      }
      if (!state.dept) return true;
      var codes = deptCodes();
      return term.courses[code].d.some(function (x) { return codes.indexOf(x) > -1; });
    });
    // "SE", "cys", "se4", "CS 210": match course codes only. SE ranks above
    // SEC (exact letters first). Anything else, or a code-like query with no
    // code match ("web"), searches names from the start of a word, then
    // instructors.
    var compact = q.replace(/\s+/g, "");
    var codeLike = /^[a-z]{1,6}\d{0,3}$/.test(compact);
    var codeRank = function (code) {
      var c = code.toLowerCase(),
        letters = c.replace(/\d.*$/, "");
      if (!c.startsWith(compact)) return 0;
      if (/\d/.test(compact)) return 3;
      return letters === compact ? 3 : 2;
    };
    var textRank = function (code) {
      var c = term.courses[code],
        cat = catalog[code] || {};
      var names = ((cat.en || "") + " " + c.ar).toLowerCase();
      var wordStart = new RegExp(
        "(^|[\\s(/&-])" + q.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"),
      );
      if (wordStart.test(names)) return 2;
      var groups = byCourse[code] || {};
      var byTeacher = Object.keys(groups).some(function (g) {
        return groups[g].some(function (s) {
          return s.i.toLowerCase().indexOf(q) > -1;
        });
      });
      return byTeacher ? 1 : 0;
    };
    var ranks = {};
    if (q) {
      if (codeLike)
        codes.forEach(function (c) {
          var r = codeRank(c);
          if (r) ranks[c] = r + 10;
        });
      if (!Object.keys(ranks).length)
        codes.forEach(function (c) {
          var r = textRank(c);
          if (r) ranks[c] = r;
        });
    }
    var matches = function (c) {
      return !q || ranks[c];
    };
    var picked = q
      ? state.picked.filter(function (c) {
          return codes.indexOf(c) > -1 && matches(c);
        })
      : state.picked.slice();
    var rest = codes
      .filter(function (c) {
        return picked.indexOf(c) < 0 && matches(c);
      })
      .sort(function (a, b) {
        var pa = catalog[a] && catalog[a].plans ? 0 : 1,
          pb = catalog[b] && catalog[b].plans ? 0 : 1;
        return (
          (ranks[b] || 0) - (ranks[a] || 0) || pa - pb || a.localeCompare(b)
        );
      });
    var LIMIT = 60;
    var html = picked
      .concat(rest.slice(0, LIMIT))
      .map(function (code) {
        var on = picked.indexOf(code) > -1;
        var groups = byCourse[code] || {};
        var keys = Object.keys(groups);
        var open = keys.filter(function (g) {
          return groups[g].every(function (s) {
            return s.o;
          });
        }).length;
        var ar = term.courses[code].ar;
        var en = catalog[code] && catalog[code].en;
        // Arabic first in Arabic mode, English first otherwise.
        if (isAr()) { var swap = en; en = ar; ar = swap || ""; }
        return (
          '<div class="course' +
          (on ? " on" : "") +
          '" role="checkbox" tabindex="0" aria-checked="' +
          on +
          '" data-code="' +
          code +
          '"' +
          (on ? ' style="--c:' + colorOf(code) + '"' : "") +
          ">" +
          '<span class="tick"></span>' +
          '<span><span class="code">' +
          code +
          '</span><br><span class="name">' +
          esc(en || "") +
          (en ? "<br>" : "") +
          '<span class="ar" dir="auto">' +
          esc(ar) +
          "</span></span></span>" +
          '<span class="meta">' +
          hoursOf(code) +
          (passed[code] ? '<span class="pill good">' + L("passed", "مجتازة") + "</span><br>" : "") +
          L(" h", " س") + "<br>" +
          (open
            ? open + "/" + keys.length + L(" open", " متاحة")
            : '<span class="pill bad">' + L("closed", "مغلقة") + "</span>") +
          (on
            ? '<br><button class="btn ghost" type="button" data-sections="' +
              code +
              '" style="padding:4px 8px;font-size:.7rem;margin-top:4px">' + L("Sections", "الشعب") + "</button>"
            : "") +
          "</span></div>"
        );
      })
      .join("");
    if (rest.length > LIMIT)
      html +=
        '<div class="more">' +
        (rest.length - LIMIT) +
        L(" more. Search to narrow down.", " أخرى. ابحث لتضييق النتائج.") + "</div>";
    if (!html) html = '<div class="more">' + L("No courses match.", "لا توجد مواد مطابقة.") + "</div>";
    if (hiddenPassed || state.showPassed)
      html += '<div class="more">' + (state.showPassed
        ? L("Showing courses you've passed. ", "تظهر المواد التي اجتزتها. ") + '<button type="button" class="linkish" data-passed="hide">' + L("Hide them", "إخفاؤها") + "</button>"
        : L(hiddenPassed + " course" + (hiddenPassed > 1 ? "s" : "") + " you've passed " + (hiddenPassed > 1 ? "are" : "is") + " hidden. ", "تم إخفاء " + hiddenPassed + " من المواد التي اجتزتها. ") +
          '<button type="button" class="linkish" data-passed="show">' + L("Show", "إظهار") + "</button>") + "</div>";
    list.innerHTML = html;
  }

  function render() {
    syncControls();
    var has = state.picked.length > 0;
    var sched = results[current] || null;

    // Notice: left-out courses, no results.
    var notes = [];
    if (leftOut.length)
      notes.push(
        L("<b>Left out:</b> ", "<b>مستبعدة:</b> ") +
          leftOut
            .map(function (l) {
              return l.code + " (" + esc(l.reason) + ")";
            })
            .join(L("; ", "؛ ")) +
          ".",
      );
    if (has && !results.length && !leftOut.length && state.picked.length) {
      var pairs = clashingPairs();
      notes.push(
        L("<b>No schedule fits.</b> ", "<b>لا يوجد جدول مناسب.</b> ") +
          (pairs.length
            ? L("These always clash: ", "هذه تتعارض دائمًا: ") +
              pairs
                .map(function (p) {
                  return p.join(" + ");
                })
                .join(", ") +
              L(". Drop one, or allow more sections.", ". احذف إحداها أو اسمح بشعب أكثر.")
            : L("Try allowing closed sections or freeing fewer hours.", "جرّب السماح بالشعب المغلقة أو تقليل ساعات الفراغ.")),
      );
    }
    if (results.capped)
      notes.push(
        L("Showing the first ", "نعرض أول ") +
          MAX_RESULTS.toLocaleString() +
          L(" schedules. Free some hours to narrow them down.", " جدول. حدّد أوقات فراغ لتضييقها."),
      );
    if (state.textRules.maxDays && results.beforeMaxDays && !results.length)
      notes.push(L("<b>No schedule fits in " + state.textRules.maxDays + " day" + (state.textRules.maxDays > 1 ? "s" : "") + ".</b> ", "<b>لا يوجد جدول في " + state.textRules.maxDays + " أيام أو أقل.</b> ") +
        results.beforeMaxDays.toLocaleString() + L(" schedules need more days. Remove the day limit under Free time to see them.", " جدول تحتاج أيامًا أكثر. احذف حد الأيام من وقت الفراغ لعرضها."));
    $("notice").innerHTML = notes.length
      ? '<div class="notice">' + notes.join("<br>") + "</div>"
      : "";

    $("empty").hidden = has;
    $("week").hidden = !term;
    $("navbar").hidden = !results.length;
    $("meter").hidden = !sched;
    if (!sched) $("breakdown").classList.remove("open");
    $("count").textContent = results.length
      ? L("Schedule ", "الجدول ") + (current + 1) + L(" of ", " من ") + results.length.toLocaleString()
      : "–";
    $("prev").disabled = current <= 0;
    $("next").disabled = current >= results.length - 1;
    var savedKey = sched && keyOf(sched);
    var alreadySaved = !!savedKey && isSaved(savedKey);
    $("save").textContent = alreadySaved ? L("★ Saved", "★ محفوظ") : L("☆ Save", "☆ حفظ");
    $("save").setAttribute("aria-pressed", String(alreadySaved));

    renderFreeRules();
    renderWeek(sched);
    renderMeter(sched);
    renderSelected(sched);
    renderFinals(sched);
    renderSaved();
    renderList();
    if (window.Murshid) window.Murshid.update(api.context());
  }

  function clashingPairs() {
    var codes = state.picked.filter(function (c) {
      return options[c] && options[c].usable.length;
    });
    var out = [];
    for (var i = 0; i < codes.length; i++)
      for (var j = i + 1; j < codes.length; j++) {
        var A = options[codes[i]].usable,
          B = options[codes[j]].usable;
        var any = A.some(function (a) {
          return B.some(function (b) {
            return (
              !overlaps(a.mask, b.mask) &&
              (state.finalClash || !a.exam || a.exam !== b.exam)
            );
          });
        });
        if (!any) out.push([codes[i], codes[j]]);
      }
    return out;
  }

  var BREAK_HOUR = 12; // 12:00–1:00 is PSU's university-wide break.

  function renderWeek(sched) {
    var week = $("week");
    if (week.hidden) return;
    var meetings = [];
    (sched || []).forEach(function (o) {
      o.meetings.forEach(function (m) { meetings.push({ o: o, m: m }); });
    });
    var days = [0, 1, 2, 3, 4];
    meetings.forEach(function (x) { if (days.indexOf(x.m.d) < 0) days.push(x.m.d); });
    days.sort();
    // Always show 8 AM–5 PM so every common hour can be tapped free.
    var startH = 8, endH = 17;
    meetings.forEach(function (x) {
      startH = Math.min(startH, Math.floor(x.m.s / 60));
      endH = Math.max(endH, Math.ceil(x.m.e / 60));
    });
    state.blocks.forEach(function (k) {
      var h = +k.split("-")[1];
      startH = Math.min(startH, h);
      endH = Math.max(endH, h + 1);
    });
    var blocked = blockedSet();
    var hourPx = parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--hour")) || 64;
    var closeExams = {};
    if (sched) {
      var ex = sched.metrics.exams;
      for (var i = 1; i < ex.length; i++)
        if ((ex[i].t - ex[i - 1].t) / 36e5 < 24) closeExams[ex[i].code] = closeExams[ex[i - 1].code] = true;
    }

    week.className = "week" + (days.length > 5 ? " has-weekend" : "");
    week.dataset.start = startH;
    var html = '<div class="head"></div>' + days.map(function (d) {
      return '<div class="head">' + (innerWidth < 800 ? DAY_SHORT[d] : DAY_NAMES[d]) + "</div>";
    }).join("");
    html += '<div class="times">';
    for (var h = startH; h < endH; h++) html += '<div class="time">' + clock(h * 60).replace(":00", "") + "</div>";
    html += "</div>";
    days.forEach(function (d) {
      html += '<div class="col" data-day="' + d + '">';
      for (var h = startH; h < endH; h++) {
        if (h === BREAK_HOUR) {
          html += '<div class="slot break" title="' + L("University-wide break: no classes 12–1", "استراحة لكل الجامعة: لا محاضرات من 12 إلى 1") + '"><span>' + L("Break", "استراحة") + "</span></div>";
          continue;
        }
        var on = !!blocked[d + "-" + h];
        html += '<div class="slot' + (on ? " blocked" : "") + '" data-slot="' + d + "-" + h + '" role="button" tabindex="0" aria-pressed="' + on + '" aria-label="' + L("Keep ", "اجعل ") + DAY_NAMES[d] + " " + clock(h * 60) + L(" free", " وقت فراغ") + '"></div>';
      }
      meetings.filter(function (x) { return x.m.d === d; }).forEach(function (x) {
        var top = ((x.m.s - startH * 60) / 60) * hourPx + 2;
        var height = Math.max(24, ((x.m.e - x.m.s) / 60) * hourPx - 4);
        var tip = x.o.code + " " + TYPE[x.m.t] + " · CRN " + x.m.crn + " · " + clock(x.m.s) + "–" + clock(x.m.e) + " · " + (x.m.room || L("room TBA", "القاعة لم تحدد")) + " · " + x.m.i + (x.m.o ? "" : L(" · CLOSED", " · مغلقة")) + L("\nTap to see the other sections", "\nاضغط لعرض الشعب الأخرى");
        html += '<div class="block' + (height < 70 ? " short" : "") + (state.pinned[x.o.code] ? " pinned" : "") + (x.m.o ? "" : " is-closed") + '" style="--c:' + colorOf(x.o.code) + ";top:" + top + "px;height:" + height + 'px" data-code="' + x.o.code + '" role="button" tabindex="0" title="' + esc(tip) + '">' +
          '<div class="bc"><span class="bcode">' + x.o.code + '</span><span class="tag">' + (TYPE[x.m.t] || x.m.t) + "</span></div>" +
          '<div class="who" dir="auto">' + (x.m.o ? "" : '<b class="closed">' + L("Closed · ", "مغلقة · ") + "</b>") + esc(x.m.i) + "</div>" +
          '<div class="room">' + esc(x.m.room || "") + "</div>" +
          (closeExams[x.o.code] ? '<span class="xdot" title="' + L("Final exam close to another", "اختبار نهائي قريب من اختبار آخر") + '"></span>' : "") +
          "</div>";
      });
      html += "</div>";
    });
    week.innerHTML = html;
  }

  function renderMeter(sched) {
    if (!sched) return;
    var l = loadOf(sched);
    var color = {
      light: "var(--good)",
      fine: "var(--good)",
      heavy: "var(--warn)",
      "very heavy": "var(--bad)",
    }[l.level];
    $("meter-arc").setAttribute(
      "stroke-dasharray",
      l.score.toFixed(0) + " 100",
    );
    $("meter-arc").setAttribute("stroke", color);
    var angle = -90 + (l.score / 100) * 180;
    $("meter-needle").setAttribute("transform", "rotate(" + angle + " 27 30)");
    var lvl = $("meter-level");
    lvl.textContent = LEVEL[l.level];
    lvl.style.background = "color-mix(in srgb, " + color + " 16%, transparent)";
    lvl.style.color = color;
    $("meter-sub").textContent =
      l.hours +
      L(" credit hours · ", " ساعة معتمدة · ") +
      sched.metrics.days +
      L(" days on campus · ", " أيام حضور · ") +
      (l.rated === l.total
        ? L("based on student ratings", "بناءً على تقييمات الطلاب")
        : l.rated
          ? L("partly an estimate: " + (l.total - l.rated) + " course" + (l.total - l.rated > 1 ? "s have" : " has") + " no ratings yet",
              "تقدير جزئي: " + (l.total - l.rated) + " من المواد بلا تقييمات بعد")
          : L("an estimate: these courses have no ratings yet", "تقدير: لا توجد تقييمات لهذه المواد بعد")) +
      (l.personal ? L(" · adjusted to your grades", " · معدّل حسب درجاتك") : "");
    $("breakdown").innerHTML =
      "<table>" +
      l.parts
        .map(function (p) {
          return (
            "<tr><td>" + p[0] + "</td><td>+" + p[1].toFixed(1) + "</td></tr>"
          );
        })
        .join("") +
      "<tr><td><b>" + L("Total (out of 100)", "المجموع (من 100)") + "</b></td><td><b>" +
      l.score.toFixed(0) +
      "</b></td></tr></table>" +
      '<p class="hint" style="margin-bottom:4px">' + L("Difficulty per course (out of 5):", "صعوبة كل مادة (من 5):") + "</p><table>" +
      sched
        .map(function (o) {
          var d = difficulty(o.code);
          var source = d.rated ? d.n + L(" rating" + (d.n > 1 ? "s" : ""), " تقييم") : L("guess from course level", "تقدير من مستوى المادة");
          var WHY = { prerequisite: L("prerequisite", "متطلب سابق"), "builds toward it": L("builds toward it", "تمهّد لها"), "same subject": L("same subject", "نفس المجال"), "similar topics": L("similar topics", "مواضيع مشابهة") };
          var mine = d.personal
            ? "<br><span class=\"hint\">" + L("For you: ", "بالنسبة لك: ") + (d.personal.shift < 0 ? L("easier", "أسهل") : d.personal.shift > 0 ? L("harder", "أصعب") : L("about average", "متوسطة تقريبًا")) +
              L(", from ", "، بناءً على ") + d.personal.related.map(function (r) { return r.code + " " + r.letter + (r.why ? " (" + (WHY[r.why] || r.why) + ")" : ""); }).join(L(", ", "، ")) + "</span>"
            : "";
          return "<tr><td>" + o.code + " <span class=\"hint\">" + source + "</span>" + mine + "</td><td>" +
            (d.personal && d.personal.shift ? d.base.toFixed(1) + " → " : "") + d.value.toFixed(1) + "</td></tr>";
        })
        .join("") +
      "</table>" +
      (Object.keys(grades).length
        ? ""
        : '<p class="hint">' + L("Sign in and add your grades (on course pages or in the calendar) to see how heavy this would be for you.", "سجّل الدخول وأضف درجاتك (في صفحات المواد أو التقويم) لترى مدى ثقل الجدول بالنسبة لك.") + "</p>") +
      '<p class="hint">' + L("Rate courses you've finished on their course page to make this better for everyone.", "قيّم المواد التي أنهيتها في صفحاتها ليصبح هذا التقدير أدق للجميع.") + "</p>";
  }

  function renderSelected(sched) {
    var sel = $("sel");
    var hours = 0;
    if (!state.picked.length) {
      sel.innerHTML = '<p class="hint">' + L("Your sections show here.", "ستظهر شعبك هنا.") + "</p>";
    } else {
      var byCode = {};
      (sched || []).forEach(function (o) {
        byCode[o.code] = o;
      });
      sel.innerHTML = state.picked
        .map(function (code) {
          var o = byCode[code];
          hours += o ? hoursOf(code) : 0;
          return (
            '<div class="item" style="--c:' +
            colorOf(code) +
            '"><button type="button" class="item-open" data-open="' + code + '" title="' + L("See " + code + " sections", "عرض شعب " + code) + '"><span class="code">' +
            code +
            "</span> " +
            (state.pinned[code] ? '<span class="pill" title="' + L("You picked this section", "شعبة مثبّتة") + '">📌</span> ' : "") +
            (o
              ? '<span class="crn">' +
                o.crns.join(" · ") +
                "</span>" +
                (o.open ? "" : ' <span class="pill bad">' + L("closed", "مغلقة") + "</span>")
              : '<span class="pill warn">' + L("not placed", "غير موضوعة") + "</span>") +
            '</button><button type="button" data-unpick="' +
            code +
            '" aria-label="' + L("Remove ", "حذف ") +
            code +
            '">✕</button></div>'
          );
        })
        .join("");
    }
    $("hours").textContent = state.picked.length + L(" courses · ", " مواد · ") + hours + L(" h", " س");
    $("copy").disabled = !sched;
  }

  function renderFinals(sched) {
    var box = $("finals");
    if (!sched) {
      box.innerHTML = '<p class="hint">' + L("Finals show here.", "ستظهر الاختبارات النهائية هنا.") + "</p>";
      return;
    }
    var ex = sched.metrics.exams;
    var noExam = sched
      .filter(function (o) {
        return !o.exam;
      })
      .map(function (o) {
        return o.code;
      });
    box.innerHTML =
      ex
        .map(function (e, i) {
          var prev = ex[i - 1],
            next = ex[i + 1];
          var clash = (prev && prev.t === e.t) || (next && next.t === e.t);
          var close =
            !clash &&
            ((prev && (e.t - prev.t) / 36e5 < 24) ||
              (next && (next.t - e.t) / 36e5 < 24));
          return (
            '<div class="f' +
            (clash ? " clash" : close ? " close" : "") +
            '"><b>' +
            e.code +
            "</b><span>" +
            examLabel(e.x) +
            "</span></div>"
          );
        })
        .join("") +
      (noExam.length
        ? '<p class="hint">' + L("No final listed for ", "لا يوجد اختبار نهائي مدرج لـ ") + noExam.join(", ") + ".</p>"
        : "");
  }

  function savedLabel(s) {
    if (s.days != null && s.start != null)
      return s.days + L(" days · ", " أيام · ") + L("", "يبدأ ") + clock(s.start).replace(":00", "") + L(" start", "");
    // Older saves only kept an English label like "4 days · 9:00AM start".
    var m = String(s.label || "").match(/^(\d+) days · (\d{1,2}):(\d{2})\s*(AM|PM)/);
    if (m) {
      var h = (+m[2] % 12) + (m[4] === "PM" ? 12 : 0);
      return savedLabel({ days: +m[1], start: h * 60 + +m[3] });
    }
    return String(s.label || "").split(" · ").slice(0, 2).join(" · ");
  }

  function renderSaved() {
    var box = $("saved");
    var mine = state.saved.filter(function (s) {
      return s.term === state.term && s.campus === state.campus;
    });
    box.innerHTML = mine.length
      ? mine
          .map(function (s) {
            return (
              '<div class="saved-item"><button type="button" class="saved-open" data-load="' +
              esc(s.key) +
              '">' +
              "<span>" + esc(savedLabel(s)) + "</span>" +
              '<span class="saved-secs">' +
              esc(s.sections || s.key.split(",").join(" · ").replace(/:/g, L(" sec ", " شعبة "))) +
              "</span>" +
              '</button><button class="saved-del" type="button" data-unsave="' +
              esc(s.key) +
              '" aria-label="' + L("Delete saved schedule", "حذف الجدول المحفوظ") + '">✕</button></div>'
            );
          })
          .join("")
      : '<p class="hint">' + L("Press ☆ Save on a schedule to keep it here.", "اضغط ☆ حفظ على أي جدول ليُحفظ هنا.") + "</p>";
  }

  // ── Section dialog ─────────────────────────────────────────────────────

  function meetingSummary(o) {
    return o.secs
      .map(function (s) {
        if (!s.m.length) return TYPE[s.t] + ": time not set";
        var byTime = {};
        s.m.forEach(function (m) {
          var k = clock(m[1]) + "–" + clock(m[2]);
          (byTime[k] = byTime[k] || []).push(DAY_SHORT[m[0]]);
        });
        return (
          TYPE[s.t] +
          " " +
          Object.keys(byTime)
            .map(function (k) {
              return byTime[k].join(" ") + " " + k;
            })
            .join(", ")
        );
      })
      .join(" · ");
  }

  var picker = { code: null, sort: "fit", choice: null };

  /** How one section of `code` sits with the rest of the current schedule. */
  function fitOf(code, opt) {
    var others = (results[current] || []).filter(function (o) { return o.code !== code; });
    var blocked = blockedSet();
    var clashes = others.filter(function (o) { return overlaps(o.mask, opt.mask); }).map(function (o) { return o.code; });
    var finals = opt.exam ? others.filter(function (o) { return o.exam === opt.exam; }).map(function (o) { return o.code; }) : [];
    var free = opt.meetings.some(function (m) {
      for (var h = Math.floor(m.s / 60); h * 60 < m.e; h++) if (blocked[m.d + "-" + h]) return true;
      return false;
    });
    return { clashes: clashes, finals: finals, free: free, ok: !clashes.length && (state.finalClash || !finals.length) };
  }

  function pickerCard(code, opt, fit) {
    var first = opt.meetings.filter(function (m) { return m.t === "L"; })[0] || opt.meetings[0];
    var days = {};
    opt.meetings.forEach(function (m) { days[m.d] = true; });
    var rooms = {};
    opt.meetings.forEach(function (m) {
      var k = (m.room || L("Room TBA", "القاعة لم تحدد")) + "|" + TYPE[m.t];
      (rooms[k] = rooms[k] || []).push(DAY_SHORT[m.d]);
    });
    var status = [];
    if (!opt.open) status.push('<span class="pill bad">' + L("Closed", "مغلقة") + "</span>");
    fit.clashes.forEach(function (c) { status.push('<span class="pill bad">⚠ ' + L("Clashes with ", "تتعارض مع ") + c + "</span>"); });
    fit.finals.forEach(function (c) { status.push('<span class="pill bad">' + L("Final at the same time as ", "النهائي في نفس وقت ") + c + "</span>"); });
    if (fit.free) status.push('<span class="pill warn">' + L("In your free time", "في وقت فراغك") + "</span>");
    if (opt.open && fit.ok && !fit.free) status.push('<span class="pill good">' + L("Fits your schedule", "تناسب جدولك") + "</span>");
    var checked = picker.choice === opt.g;
    return '<label class="pcard' + (fit.ok ? "" : " bad") + (checked ? " on" : "") + '" data-g="' + opt.g + '">' +
      '<span class="ptime">' +
      (first ? "<b>" + clock(first.s).replace(/ (AM|PM|ص|م)$/, "<small>$1</small>") + "</b><span>" + L("to ", "إلى ") + clock(first.e) + "</span>" : "<b>" + L("TBA", "لم يحدد") + "</b>") +
      '<span class="pdays">' + [0, 1, 2, 3, 4].map(function (d) { return '<i class="' + (days[d] ? "on" : "") + '">' + DAY_TINY[d] + "</i>"; }).join("") + "</span>" +
      "</span>" +
      '<span class="pinfo"><b class="pwho" dir="auto">' + esc(opt.instructor || L("Instructor TBA", "المحاضر لم يحدد")) + "</b>" +
      '<span class="prooms">' + Object.keys(rooms).map(function (k) {
        var p = k.split("|");
        return "<span>" + esc(p[0]) + " <em>" + p[1] + " · " + rooms[k].join(" ") + "</em></span>";
      }).join("") + "</span>" +
      '<span class="pmeta">' + L("Section ", "الشعبة ") + opt.g + " · CRN " + opt.crns.join(", ") + (opt.exam ? L(" · Final ", " · النهائي ") + examLabel(opt.exam) : "") + "</span>" +
      '<span class="pstatus">' + status.join("") + "</span></span>" +
      '<input type="radio" name="pick-section" value="' + opt.g + '"' + (checked ? " checked" : "") + ' aria-label="' + L("Section ", "الشعبة ") + opt.g + '">' +
      "</label>";
  }

  function renderPicker() {
    var code = picker.code;
    var o = buildOptions(code, blockedSet());
    var list = o.all.map(function (opt) { return { opt: opt, fit: fitOf(code, opt) }; });
    if (picker.sort === "open") list = list.filter(function (x) { return x.opt.open; });
    var startOf = function (x) { var m = x.opt.meetings[0]; return m ? m.s : 9999; };
    list.sort(picker.sort === "early"
      ? function (a, b) { return startOf(a) - startOf(b); }
      : function (a, b) {
          var score = function (x) { return (x.fit.ok ? 0 : 4) + (x.opt.open ? 0 : 2) + (x.fit.free ? 1 : 0); };
          return score(a) - score(b) || startOf(a) - startOf(b);
        });
    var fits = list.filter(function (x) { return x.fit.ok && x.opt.open; }).length;
    $("sections-count").textContent = L(o.all.length + " section" + (o.all.length > 1 ? "s" : "") + " · " + fits + " fit", o.all.length + " شعب · " + fits + " مناسبة");
    document.querySelectorAll("[data-psort]").forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.psort === picker.sort)); });
    $("sections-body").innerHTML =
      '<label class="pcard any' + (picker.choice ? "" : " on") + '" data-g=""><span class="pinfo"><b>' + L("Any section", "أي شعبة") + '</b><span class="pmeta">' + L("Let the planner choose, so you see every schedule that works.", "دع المخطط يختار لترى كل الجداول الممكنة.") + "</span></span>" +
      '<input type="radio" name="pick-section" value=""' + (picker.choice ? "" : " checked") + ' aria-label="' + L("Any section", "أي شعبة") + '"></label>' +
      (list.length ? list.map(function (x) { return pickerCard(code, x.opt, x.fit); }).join("") : '<p class="hint">' + L("No open sections. Switch to Best fit to see closed ones.", "لا توجد شعب متاحة. اختر «الأنسب» لرؤية الشعب المغلقة.") + "</p>");
    var shown = picker.choice && o.all.filter(function (x) { return x.g === picker.choice; })[0];
    var placed = (results[current] || []).filter(function (x) { return x.code === code; })[0];
    renderPreview(code, shown || placed || null);
  }

  /** Mini week: your other courses in grey, this section in colour, clashes in red. */
  function renderPreview(code, opt) {
    var others = (results[current] || []).filter(function (o) { return o.code !== code; });
    var items = [];
    others.forEach(function (o) { o.meetings.forEach(function (m) { items.push({ code: o.code, m: m, kind: "other" }); }); });
    (opt ? opt.meetings : []).forEach(function (m) {
      var clash = others.some(function (o) { return o.meetings.some(function (n) { return n.d === m.d && n.s < m.e && m.s < n.e; }); });
      items.push({ code: code, m: m, kind: clash ? "clash" : "this" });
    });
    var startH = 8, endH = 15;
    items.forEach(function (x) { startH = Math.min(startH, Math.floor(x.m.s / 60)); endH = Math.max(endH, Math.ceil(x.m.e / 60)); });
    var px = 34;
    var html = '<div class="pw" style="--rows:' + (endH - startH) + ";--px:" + px + 'px"><div></div>' +
      [0, 1, 2, 3, 4].map(function (d) { return "<b>" + DAY_SHORT[d] + "</b>"; }).join("");
    html += '<div class="pw-times">';
    for (var h = startH; h < endH; h++) html += "<span>" + clock(h * 60).replace(":00", "") + "</span>";
    html += "</div>";
    [0, 1, 2, 3, 4].forEach(function (d) {
      html += '<div class="pw-col">';
      items.filter(function (x) { return x.m.d === d; }).forEach(function (x) {
        html += '<span class="pw-b ' + x.kind + '" style="top:' + ((x.m.s - startH * 60) / 60) * px + "px;height:" + Math.max(14, ((x.m.e - x.m.s) / 60) * px - 2) + 'px">' + x.code + "</span>";
      });
      html += "</div>";
    });
    $("sections-preview").innerHTML = html + "</div>" +
      (opt ? "" : '<p class="hint">' + L("Hover a section to see where it lands.", "مرّر على أي شعبة لترى موقعها.") + "</p>");
  }

  function openSections(code) {
    picker.code = code;
    picker.sort = "fit";
    picker.choice = state.pinned[code] || null;
    var e = catalog[code] || {};
    $("sections-hours").textContent = hoursOf(code) + L(" credit hours", " ساعات معتمدة");
    $("sections-title").textContent = code;
    var other = isAr() ? e.en : term && term.courses[code] && term.courses[code].ar;
    $("sections-sub").textContent = nameOf(code) + (other && other !== nameOf(code) ? " · " + other : "");
    renderPicker();
    $("sections-dialog").showModal();
  }

  // ── Actions ────────────────────────────────────────────────────────────

  function pick(code, on) {
    var i = state.picked.indexOf(code);
    if (on === undefined) on = i < 0;
    if (on && i < 0 && byCourse[code]) state.picked.push(code);
    if (!on && i > -1) {
      state.picked.splice(i, 1);
      delete state.pinned[code];
    }
    persist();
    regenerate(true);
  }

  function bind() {
    $("term").addEventListener("change", function () {
      state.term = this.value;
      persist();
      loadTerm();
    });
    document.querySelectorAll("[data-campus]").forEach(function (b) {
      b.addEventListener("click", function () {
        if (state.campus === b.dataset.campus) return;
        state.campus = b.dataset.campus;
        persist();
        loadTerm();
      });
    });
    $("major").addEventListener("change", function () {
      var m = majors[this.value];
      state.dept = m ? m.main || m.prep : "";
      persist();
      renderMajor();
      renderList();
    });
    $("major-tracks").addEventListener("click", function (e) {
      var chip = e.target.closest("[data-track]");
      if (!chip) return;
      var m = majorOf(state.dept);
      if (!m) return;
      state.dept = chip.dataset.track || m.main;
      persist();
      renderMajor();
      renderList();
    });
    $("major-prep").addEventListener("change", function () {
      var m = majorOf(state.dept);
      if (!m) return;
      state.dept = this.checked && m.prep ? m.prep : m.main || m.prep;
      persist();
      renderMajor();
      renderList();
    });
    $("search").addEventListener("input", renderList);
    $("opt-closed").addEventListener("change", function () {
      state.closed = this.checked;
      persist();
      regenerate(true);
    });
    $("opt-final-clash").addEventListener("change", function () {
      state.finalClash = this.checked;
      persist();
      regenerate(true);
    });
    $("sort").addEventListener("change", function () {
      state.sort = this.value;
      persist();
      sortResults();
      current = 0;
      render();
    });
    $("prev").addEventListener("click", function () {
      if (current > 0) {
        current--;
        render();
      }
    });
    $("next").addEventListener("click", function () {
      if (current < results.length - 1) {
        current++;
        render();
      }
    });
    document.addEventListener("keydown", function (e) {
      if (e.target.closest("input, select, textarea, dialog")) return;
      if (e.key === "ArrowRight" && current < results.length - 1) {
        current++;
        render();
      }
      if (e.key === "ArrowLeft" && current > 0) {
        current--;
        render();
      }
    });

    $("course-list").addEventListener("click", function (e) {
      var toggle = e.target.closest("[data-passed]");
      if (toggle) {
        state.showPassed = toggle.dataset.passed === "show";
        persist();
        return renderList();
      }
      var sec = e.target.closest("[data-sections]");
      if (sec) {
        e.stopPropagation();
        return openSections(sec.dataset.sections);
      }
      var row = e.target.closest("[data-code]");
      if (row) pick(row.dataset.code);
    });
    $("course-list").addEventListener("keydown", function (e) {
      if ((e.key === " " || e.key === "Enter") && e.target.dataset.code) {
        e.preventDefault();
        pick(e.target.dataset.code);
      }
    });
    $("sel").addEventListener("click", function (e) {
      var b = e.target.closest("[data-unpick]");
      if (b) return pick(b.dataset.unpick, false);
      var o = e.target.closest("[data-open]");
      if (o) openSections(o.dataset.open);
    });

    $("sections-done").addEventListener("click", function () {
      var code = picker.code;
      if (picker.choice) state.pinned[code] = picker.choice;
      else delete state.pinned[code];
      delete state.excluded[code];
      persist();
      $("sections-dialog").close();
      regenerate(true);
      if (picker.choice && !results.length) toast(L("No schedule works with that section. Pick another or choose Any section", "لا يوجد جدول مع هذه الشعبة. اختر غيرها أو «أي شعبة»"));
      else if (picker.choice) {
        toast(L(code + " section " + picker.choice + " pinned", "تم تثبيت " + code + " الشعبة " + picker.choice));
        if (window.Murshid) window.Murshid.react("celebrate", 2000);
      }
    });
    $("sections-close").addEventListener("click", function () { $("sections-dialog").close(); });
    $("sections-remove").addEventListener("click", function () {
      $("sections-dialog").close();
      delete state.pinned[picker.code];
      pick(picker.code, false);
    });
    $("sections-body").addEventListener("change", function (e) {
      if (e.target.name !== "pick-section") return;
      picker.choice = e.target.value || null;
      renderPicker();
    });
    $("sections-body").addEventListener("mouseover", function (e) {
      var card = e.target.closest(".pcard[data-g]");
      if (!card || !card.dataset.g) return;
      var opt = buildOptions(picker.code, blockedSet()).all.filter(function (x) { return x.g === card.dataset.g; })[0];
      if (opt) renderPreview(picker.code, opt);
    });
    $("sections-body").addEventListener("mouseleave", function () { renderPicker(); });
    document.querySelectorAll("[data-psort]").forEach(function (b) {
      b.addEventListener("click", function () { picker.sort = b.dataset.psort; renderPicker(); });
    });

    document.querySelectorAll("[data-preset]").forEach(function (b) {
      b.addEventListener("click", function () {
        var p = b.dataset.preset,
          i = state.presets.indexOf(p);
        if (i > -1) state.presets.splice(i, 1);
        else state.presets.push(p);
        persist();
        regenerate(true);
      });
    });
    // Free time: tap or drag over empty hours; tap a class to free its hour.
    var paintValue = null, painted = false;
    var hourAt = function (col, clientY) {
      var hourPx = parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--hour")) || 64;
      return +$("week").dataset.start + Math.floor((clientY - col.getBoundingClientRect().top) / hourPx);
    };
    var label = function (key) {
      var p = key.split("-");
      return DAY_SHORT[+p[0]] + " " + clock(+p[1] * 60);
    };
    $("week").addEventListener("pointerdown", function (e) {
      var slot = e.target.closest("[data-slot]");
      if (!slot) return;
      e.preventDefault();
      paintValue = !slot.classList.contains("blocked");
      painted = false;
      paintSlot(slot, paintValue);
    });
    $("week").addEventListener("pointerover", function (e) {
      if (paintValue === null) return;
      var slot = e.target.closest("[data-slot]");
      if (slot && slot.classList.contains("blocked") !== paintValue) { paintSlot(slot, paintValue); painted = true; }
    });
    window.addEventListener("pointerup", function () {
      if (paintValue === null) return;
      var v = paintValue;
      paintValue = null;
      persist();
      toast(v ? (painted ? L("Hours kept free", "تم حجز الساعات كوقت فراغ") : L("Kept free. Tap again to undo", "أصبحت وقت فراغ. اضغط مرة أخرى للتراجع")) : L("Free time removed", "أُزيل وقت الفراغ"));
      regenerate(true);
    });
    $("week").addEventListener("click", function (e) {
      var block = e.target.closest(".block[data-code]");
      if (block) openSections(block.dataset.code);
    });
    $("week").addEventListener("keydown", function (e) {
      var block = e.target.closest(".block[data-code]");
      if (block && (e.key === " " || e.key === "Enter")) {
        e.preventDefault();
        return openSections(block.dataset.code);
      }
      var slot = e.target.closest("[data-slot]");
      if (slot && (e.key === " " || e.key === "Enter")) {
        e.preventDefault();
        paintSlot(slot, !slot.classList.contains("blocked"));
        persist();
        regenerate(true);
      }
    });
    $("clear-free").addEventListener("click", function () {
      state.blocks = [];
      state.presets = [];
      state.freeText = "";
      state.textRules = { rules: [], maxDays: null, preferGaps: false, unknown: [] };
      $("free-text").value = "";
      persist();
      regenerate(true);
    });
    $("free-form").addEventListener("submit", function (e) {
      e.preventDefault();
      applyFreeText($("free-text").value);
    });
    $("free-text").addEventListener("keydown", function (e) {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        applyFreeText(this.value);
      }
    });
    $("free-rules").addEventListener("click", function (e) {
      var x = e.target.closest("[data-rule]");
      if (!x) return;
      var which = x.dataset.rule;
      if (which === "maxDays") state.textRules.maxDays = null;
      else if (which === "gaps") state.textRules.preferGaps = false;
      else state.textRules.rules.splice(+which, 1);
      persist();
      regenerate(true);
    });

    $("meter").addEventListener("click", function () {
      var open = $("breakdown").classList.toggle("open");
      this.setAttribute("aria-expanded", String(open));
    });

    $("copy").addEventListener("click", function () {
      var sched = results[current];
      if (!sched) return;
      var text = sched
        .map(function (o) {
          return o.code + ": " + o.crns.join(", ");
        })
        .join("\n");
      (navigator.clipboard
        ? navigator.clipboard.writeText(text)
        : Promise.reject()
      ).then(
        function () {
          toast(L("Section numbers copied", "تم نسخ أرقام الشعب"));
        },
        function () {
          window.prompt(
            L("Copy your section numbers:", "انسخ أرقام شعبك:"),
            text.replace(/\n/g, " | "),
          );
        },
      );
    });

    $("to-calendar").addEventListener("click", addToCalendar);
    $("save").addEventListener("click", function () {
      var sched = results[current];
      if (!sched) return;
      var key = keyOf(sched);
      if (isSaved(key)) {
        toast(L("Already saved. Remove it from Saved schedules with ✕", "محفوظ مسبقًا. احذفه من الجداول المحفوظة بـ ✕"));
        return;
      }
      var m = sched.metrics;
      state.saved.push({
        key: key,
        term: state.term,
        campus: state.campus,
        days: m.days,
        start: Math.round(m.avgStart / 5) * 5,
        label: m.days + " days · " + Math.round(m.avgStart / 60) + " start",
        sections: sched
          .slice()
          .sort(function (x, y) { return x.code.localeCompare(y.code); })
          .map(function (o) { return o.code + " " + o.crns.join("/"); })
          .join(" · "),
      });
      toast(L("Saved", "تم الحفظ"));
      if (window.Murshid) window.Murshid.react("love", 2600, L("Saved! Good choice.", "تم الحفظ! اختيار موفق."));
      persist();
      render();
    });
    $("saved").addEventListener("click", function (e) {
      var del = e.target.closest("[data-unsave]");
      if (del) {
        state.saved = state.saved.filter(function (s) {
          return !(
            s.key === del.dataset.unsave &&
            s.term === state.term &&
            s.campus === state.campus
          );
        });
        persist();
        return render();
      }
      var ld = e.target.closest("[data-load]");
      if (!ld) return;
      var key = ld.dataset.load;
      var codes = key.split(",").map(function (p) {
        return p.split(":")[0];
      });
      state.picked = codes.filter(function (c) {
        return byCourse[c];
      });
      persist();
      regenerate();
      var at = results.findIndex(function (r) {
        return keyOf(r) === key;
      });
      if (at > -1) {
        current = at;
        render();
      } else
        toast(
          L("That schedule no longer fits: a section may have closed or clash with your free time", "هذا الجدول لم يعد مناسبًا: ربما أُغلقت شعبة أو تعارضت مع وقت فراغك"),
        );
    });

    $("ask-murshid").addEventListener("click", function () {
      if (window.Murshid) window.Murshid.open("suggest");
    });
  }

  var FREE_TIME_AI =
    window.SHOUG_FREE_TIME_ENDPOINT ||
    "https://shoug-tech.shoug-alomran.workers.dev/v1/free-time";

  /** Reads the text here first; asks the AI only for what it couldn't read. */
  function applyFreeText(text) {
    text = String(text || "").trim();
    state.freeText = text;
    if (!text) {
      state.textRules = { rules: [], maxDays: null, preferGaps: false, unknown: [] };
      persist();
      return regenerate(true);
    }
    var local = window.ShougFreeTime ? window.ShougFreeTime.parse(text) : { rules: [], unknown: [text] };
    var finish = function (result, how) {
      if (window.Murshid) window.Murshid.settle();
      state.textRules = result;
      if (result.preferGaps && state.sort !== "gaps") state.sort = "gaps";
      persist();
      regenerate(true);
      var n = result.rules.length + (result.maxDays ? 1 : 0) + (result.preferGaps ? 1 : 0);
      toast(n ? L("Applied " + n + " rule" + (n > 1 ? "s" : ""), "تم تطبيق " + n + " قواعد") : L("I couldn't find any times in that", "لم أجد أوقاتًا في هذا النص"));
      if (window.Murshid) window.Murshid.react(n ? "celebrate" : "sad", 2000);
    };
    if (!local.unknown.length && (local.rules.length || local.maxDays || local.preferGaps)) return finish(local);
    var btn = $("free-apply");
    if (window.Murshid) window.Murshid.react("think", 0, L("Let me read that…", "دعني أقرأ ذلك…"));
    btn.disabled = true;
    btn.textContent = L("Reading…", "جارٍ القراءة…");
    var controller = window.AbortController ? new AbortController() : null;
    var timer = setTimeout(function () { if (controller) controller.abort(); }, 9000);
    fetch(FREE_TIME_AI, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ text: text }),
      signal: controller ? controller.signal : undefined,
    })
      .then(function (r) { return r.ok ? r.json() : Promise.reject(r.status); })
      .then(function (ai) {
        var useful = ai && Array.isArray(ai.rules) && (ai.rules.length || ai.maxDays || ai.preferGaps);
        finish(useful ? { rules: ai.rules, maxDays: ai.maxDays || null, preferGaps: !!ai.preferGaps, unknown: ai.unknown || [] } : local);
      })
      .catch(function () { finish(local); })
      .then(function () {
        clearTimeout(timer);
        btn.disabled = false;
        btn.textContent = L("Apply", "تطبيق");
      });
  }

  /** A free-time rule in the current language (rules keep their meaning, not their words). */
  function ruleLabel(r) {
    var clock = function (m) { return clockFull(m).replace(":00", ""); };
    var on = daysText(r.days);
    var except = r.except && r.except.length ? r.except.map(function (d) { return DAY_NAMES[d]; }).join(L(" and ", " و")) : "";
    var base;
    switch (r.kind) {
      case "dayoff":
        return r.days.length >= 5 ? L("Every day off", "كل الأيام إجازة")
          : L(r.days.map(function (d) { return DAY_NAMES[d]; }).join(" and ") + " off", "إجازة يوم " + r.days.map(function (d) { return DAY_NAMES[d]; }).join(" و"));
      case "before": base = L("No classes before ", "لا محاضرات قبل ") + clock(r.to); break;
      case "after": base = L("No classes after ", "لا محاضرات بعد ") + clock(r.from); break;
      case "hour": base = L("No " + clock(r.from) + " classes", "لا محاضرات الساعة " + clock(r.from)); break;
      case "morning": base = L("No morning classes", "لا محاضرات صباحية"); break;
      case "early": base = L("No early classes (before 9 AM)", "لا محاضرات مبكرة (قبل 9 ص)"); break;
      case "afternoon": base = L("No afternoon classes", "لا محاضرات بعد الظهر"); break;
      case "evening": base = L("No evening classes", "لا محاضرات مسائية"); break;
      case "only": base = L("Classes only ", "المحاضرات فقط من ") + clock(r.window[0]) + L("–", " إلى ") + clock(r.window[1]); break;
      case "range": base = L("Free ", "وقت فراغ ") + clock(r.from) + "–" + clock(r.to); break;
      default: base = isAr() ? L("", "وقت فراغ ") + clock(r.from) + "–" + clock(r.to) : r.label || "Free " + clock(r.from) + "–" + clock(r.to);
    }
    if (except) return base + L(" except ", " ما عدا ") + except;
    return base + (on ? L(" on ", " يوم ") + on : "");
  }

  function renderFreeRules() {
    var t = state.textRules;
    var chips = t.rules.map(function (r, i) {
      var label = ruleLabel(r);
      return '<span class="rule">' + esc(label) + '<button type="button" data-rule="' + i + '" aria-label="' + L("Remove: ", "حذف: ") + esc(label) + '">✕</button></span>';
    });
    if (t.maxDays) chips.push('<span class="rule">' + L("At most " + t.maxDays + " day" + (t.maxDays > 1 ? "s" : "") + " on campus", "حضور " + t.maxDays + " أيام كحد أقصى") + '<button type="button" data-rule="maxDays" aria-label="' + L("Remove day limit", "حذف حد الأيام") + '">✕</button></span>');
    if (t.preferGaps) chips.push('<span class="rule">' + L("Fewest gaps first", "أقل فراغات أولًا") + '<button type="button" data-rule="gaps" aria-label="' + L("Remove", "حذف") + '">✕</button></span>');
    $("free-rules").innerHTML =
      (chips.length ? '<div class="label" style="margin:10px 0 6px">' + L("Understood", "فهمت") + '</div><div class="rules">' + chips.join("") + "</div>" : "") +
      (t.unknown && t.unknown.length ? '<p class="hint">' + L("Couldn't use: “", "لم أستطع استخدام: «") + esc(t.unknown.join(L("”, “", "»، «"))) + L("”. Try saying it with days and times.", "». جرّب كتابته بالأيام والأوقات.") + "</p>" : "");
  }

  var TYPE_EN = { L: "", B: "Lab", T: "Tutorial", S: "Studio", C: "Co-op" };
  var WEEKDAY = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"];
  function hhmm(mins) { return String(Math.floor(mins / 60)).padStart(2, "0") + ":" + String(mins % 60).padStart(2, "0"); }
  function newId() { return "sp" + Date.now().toString(36) + Math.random().toString(36).slice(2, 8); }
  function codeOfTitle(t) {
    var m = String(t || "").toUpperCase().replace(/\s+/g, "").match(/[A-Z]{2,6}\d{3}/);
    return m ? m[0] : "";
  }

  /**
   * Writes the schedule on screen into the calendar (users/{uid}/private/data):
   * one class per section meeting time, plus each course's final. Classes and
   * finals the planner added before for the same term are replaced, so
   * pressing it again after changing the schedule doesn't double anything.
   */
  function addToCalendar() {
    var sched = results[current];
    if (!sched) return;
    var fb = window.__shoug_fb;
    var user = fb && fb.auth && fb.auth().currentUser;
    if (!user || !window.ShougPrivate) {
      toast(L("Sign in to add this schedule to your calendar", "سجّل الدخول لإضافة الجدول إلى تقويمك"));
      var signIn = document.querySelector("#shoug-fb-user");
      if (signIn && signIn.tagName === "BUTTON") signIn.click();
      return;
    }
    // Edugate "20262" → the calendar's term "262" (Second Semester 2026).
    var calTerm = state.term.slice(2, 4) + state.term.slice(4);
    var termLabel = termName({ value: state.term, label: (term && term.termLabel) || "" });
    var codes = sched.map(function (o) { return o.code; });
    var btn = $("to-calendar");
    btn.disabled = true;
    window.ShougPrivate.ready(user.uid)
      .then(function (ref) {
        return ref.get().then(function (snap) {
          var data = (snap && snap.exists && snap.data()) || {};
          var classes = Array.isArray(data.calendarClassSchedules) ? data.calendarClassSchedules.filter(Boolean) : [];
          var mine = classes.filter(function (c) {
            return c.termId === calTerm && c.source !== "schedule-planner" && codes.indexOf(codeOfTitle(c.title)) > -1;
          });
          if (mine.length) {
            var list = mine.map(function (c) { return codeOfTitle(c.title); }).filter(function (c, i, a) { return a.indexOf(c) === i; }).join(", ");
            if (!window.confirm(L(
              "Your calendar already has classes for " + list + " in " + termLabel + ". Replace them with this schedule?",
              "تقويمك فيه محاضرات لـ " + list + " في " + termLabel + ". هل تريد استبدالها بهذا الجدول؟"))) return null;
          }
          var kept = classes.filter(function (c) {
            if (c.termId !== calTerm) return true;
            if (c.source === "schedule-planner") return false;
            return codes.indexOf(codeOfTitle(c.title)) < 0;
          });
          var added = 0;
          sched.forEach(function (o) {
            var slots = {};
            o.meetings.forEach(function (m) {
              var k = m.crn + "|" + m.s + "|" + m.e + "|" + m.room;
              var slot = (slots[k] = slots[k] || { m: m, days: [] });
              if (slot.days.indexOf(WEEKDAY[m.d]) < 0) slot.days.push(WEEKDAY[m.d]);
            });
            Object.keys(slots).forEach(function (k) {
              var x = slots[k];
              kept.push({
                id: newId(),
                title: o.code + (TYPE_EN[x.m.t] ? " " + TYPE_EN[x.m.t] : ""),
                days: x.days,
                start: hhmm(x.m.s),
                end: hhmm(x.m.e),
                location: x.m.room || "",
                onlineLink: "",
                onlineOnly: false,
                termId: calTerm,
                source: "schedule-planner",
                crn: x.m.crn,
                section: o.g,
              });
              added++;
            });
          });
          var exams = data.exams && typeof data.exams === "object" ? data.exams : {};
          var examPayload = {};
          var del = fb.firestore.FieldValue.delete();
          Object.keys(exams).forEach(function (id) {
            var e = exams[id] || {};
            if (e.source === "schedule-planner" && e.termId === calTerm) examPayload[id] = del;
          });
          var finals = 0;
          sched.forEach(function (o) {
            if (!o.exam) return;
            var date = o.exam.slice(0, 10), start = o.exam.slice(11, 16);
            var already = Object.keys(exams).some(function (id) {
              var e = exams[id] || {};
              return e.source !== "schedule-planner" && codeOfTitle(e.course) === o.code && /final/i.test(e.type || "") && e.date === date;
            });
            if (already) return;
            examPayload[newId()] = { course: o.code, type: "final", date: date, start: start, end: "", location: "", source: "schedule-planner", termId: calTerm };
            finals++;
          });
          return ref.set({
            calendarClassSchedules: kept,
            exams: examPayload,
            updatedAt: fb.firestore.FieldValue.serverTimestamp(),
          }, { merge: true }).then(function () { return { added: added, finals: finals }; });
        });
      })
      .then(function (done) {
        if (!done) return;
        $("notice").innerHTML = '<div class="notice">' +
          L("<b>Added to your calendar:</b> " + done.added + " class times and " + done.finals + " final" + (done.finals === 1 ? "" : "s") + " in " + termLabel + ". ",
            "<b>أُضيف إلى تقويمك:</b> " + done.added + " مواعيد محاضرات و" + done.finals + " اختبارات نهائية في " + termLabel + ". ") +
          '<a href="/account/calendar/">' + L("Open calendar", "افتح التقويم") + "</a></div>";
        toast(L("Added to your calendar", "أُضيف إلى تقويمك"));
        if (window.Murshid) window.Murshid.react("love", 2600, L("It's in your calendar now!", "صار في تقويمك الآن!"));
      })
      .catch(function (err) {
        console.error(err);
        toast(L("Couldn't reach your calendar. Try again.", "تعذّر الوصول إلى تقويمك. حاول مرة أخرى."));
      })
      .then(function () { btn.disabled = false; });
  }

  function paintSlot(slot, on) {
    var k = slot.dataset.slot,
      i = state.blocks.indexOf(k);
    if (on && i < 0) state.blocks.push(k);
    if (!on && i > -1) state.blocks.splice(i, 1);
    slot.classList.toggle("blocked", on);
    slot.setAttribute("aria-pressed", String(on));
  }

  // ── Public API (for Murshid) ────────────────────────────────────────────

  var api = {
    context: function () {
      var sched = results[current] || null;
      return {
        term: term,
        termLabel: term
          ? termName({ value: term.term, label: term.termLabel })
          : "",
        campus: state.campus,
        catalog: catalog,
        byCourse: byCourse,
        picked: state.picked.slice(),
        options: options,
        schedule: sched,
        metrics: sched && sched.metrics,
        load: sched && loadOf(sched),
        results: results.length,
        leftOut: leftOut,
        ratings: ratings,
        clashingPairs:
          state.picked.length > 1 && !results.length ? clashingPairs() : [],
        hoursOf: hoursOf,
        difficulty: difficulty,
        grades: grades,
        textRules: state.textRules,
        nameOf: nameOf,
      };
    },
    pick: function (codes) {
      codes.forEach(function (c) {
        if (byCourse[c] && state.picked.indexOf(c) < 0) state.picked.push(c);
      });
      persist();
      regenerate(true);
    },
    unpick: function (code) {
      pick(code, false);
    },
    offered: function (code) {
      return !!byCourse[code];
    },
    openSections: openSections,
    setDept: function (code) {
      state.dept = code;
      persist();
      renderMajor();
      renderList();
    },
  };
  window.SchedulePlanner = api;

  var PLAN_GRID_KEYS = {
    "cs-ai": "shoug_academic_plan_grid_cs_ai_v1", "cs-cys": "shoug_academic_plan_grid_cs_cys_v1",
    "cs-dx": "shoug_academic_plan_grid_cs_dx_v1", cs: "shoug_academic_plan_grid_cs_v1",
    "is-ai": "shoug_academic_plan_grid_is_ai_v1", "se-ai": "shoug_academic_plan_grid_se_ai_v1",
    "se-dx": "shoug_academic_plan_grid_se_dx_v1", "se-cys": "shoug_academic_plan_grid_v4",
    se: "shoug_academic_plan_grid_se_v1",
  };
  /** Same choice as the account header: the account's plan, else the grid they've filled in. */
  function setupTabs() {
    var plan = null;
    try {
      plan = localStorage.getItem("shoug-account-plan");
      if (!PLAN_GRID_KEYS[plan]) {
        plan = null;
        var best = 0;
        Object.keys(PLAN_GRID_KEYS).forEach(function (k) {
          var saved = JSON.parse(localStorage.getItem(PLAN_GRID_KEYS[k]) || "null");
          if (saved && (saved.updatedAt || 1) > best) { best = saved.updatedAt || 1; plan = k; }
        });
      }
    } catch (e) {}
    if (plan) $("tab-plan").href = "/academic-plan-themes/" + plan + "/grid.html";
    withFirebase(function (fb) {
      if (!fb || !fb.auth) return;
      fb.auth().onAuthStateChanged(function (user) {
        var tab = $("tab-profile");
        tab.hidden = !user;
        if (user) tab.href = "/community/profile/?u=" + encodeURIComponent(user.uid);
      });
    });
  }

  /** Static text: data-ar (text), data-ar-placeholder, data-ar-aria. English is kept in data-en*. */
  function translateStatic() {
    var ar = isAr();
    document.querySelectorAll("[data-ar]").forEach(function (el) {
      if (el.dataset.en == null) el.dataset.en = el.textContent;
      el.textContent = ar ? el.dataset.ar : el.dataset.en;
    });
    document.querySelectorAll("[data-ar-placeholder]").forEach(function (el) {
      if (el.dataset.enPlaceholder == null) el.dataset.enPlaceholder = el.getAttribute("placeholder") || "";
      el.setAttribute("placeholder", ar ? el.dataset.arPlaceholder : el.dataset.enPlaceholder);
    });
    document.querySelectorAll("[data-ar-aria]").forEach(function (el) {
      if (el.dataset.enAria == null) el.dataset.enAria = el.getAttribute("aria-label") || "";
      el.setAttribute("aria-label", ar ? el.dataset.arAria : el.dataset.enAria);
    });
    document.title = L("Schedule Planner | SHOUG.TECH", "مخطط الجدول | SHOUG.TECH");
    $("lang-toggle").textContent = ar ? "EN" : "عربي";
    var signIn = document.querySelector("#shoug-fb-user.shoug-auth-btn, #shoug-fb-user[data-account-loader]");
    if (signIn && /^(Sign In|تسجيل الدخول)$/.test(signIn.textContent.trim())) signIn.textContent = L("Sign In", "تسجيل الدخول");
    $("lang-toggle").setAttribute("aria-label", ar ? "Switch to English" : "التبديل إلى العربية");
  }

  var MOON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/></svg>';
  var SUN_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>';
  /** Same icons as the site header: a sun in dark mode (switch to light), a moon in light mode. */
  function syncThemeIcon() {
    var dark = document.documentElement.getAttribute("data-theme") === "dark";
    $("theme-ico").innerHTML = dark ? SUN_SVG : MOON_SVG;
  }

  function setLanguage(lang) {
    try { localStorage.setItem("shoug-lang", lang); } catch (e) {}
    document.documentElement.lang = lang === "ar" ? "ar-SA" : "en";
    document.documentElement.dir = lang === "ar" ? "rtl" : "ltr";
    applyLanguage();
    window.dispatchEvent(new CustomEvent("shoug:language-change", { detail: { lang: lang } }));
  }

  function applyLanguage() {
    setLanguageData();
    translateStatic();
    renderUpdated();
    if (term) {
      var current = $("term").value;
      Array.prototype.forEach.call($("term").options, function (o) {
        var t = (index.terms || []).filter(function (x) { return x.value === o.value; })[0];
        if (t) o.textContent = termName(t);
      });
      $("term").value = current;
      renderMajor();
    }
    render();
    if ($("sections-dialog").open) renderPicker();
    if (window.Murshid && window.Murshid.relabel) window.Murshid.relabel();
  }

  function start() {
    var stored = null;
    try {
      var q = new URLSearchParams(location.search).get("lang");
      stored = q === "ar" || q === "en" ? q : localStorage.getItem("shoug-lang");
    } catch (e) {}
    if (stored === "ar" || stored === "en") {
      document.documentElement.lang = stored === "ar" ? "ar-SA" : "en";
      document.documentElement.dir = stored === "ar" ? "rtl" : "ltr";
    }
    setLanguageData();
    translateStatic();
    $("lang-toggle").addEventListener("click", function () { setLanguage(isAr() ? "en" : "ar"); });
    syncThemeIcon();
    if (window.MutationObserver)
      new MutationObserver(syncThemeIcon).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
    // firebase-auth.js rebuilds the sign-in button; relabel it when it does.
    if (window.MutationObserver)
      new MutationObserver(function () {
        var b = document.querySelector("#shoug-fb-user.shoug-auth-btn");
        if (b && isAr() && b.textContent.trim() === "Sign In") b.textContent = "تسجيل الدخول";
      }).observe(document.querySelector(".topbar-end"), { childList: true, subtree: true, characterData: true });
    window.addEventListener("storage", function (e) {
      if (e.key === "shoug-lang" && (e.newValue === "ar" || e.newValue === "en") && (e.newValue === "ar") !== isAr()) setLanguage(e.newValue);
    });
    bind();
    setupTabs();
    $("free-text").value = state.freeText;
    syncControls();
    boot();
    loadGrades();
  }
  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", start);
  else start();
})();
