/**
 * Study Plan tab for /account/calendar/.
 *
 *  - Pick the exam season (quizzes, midterms, finals). Courses come from the
 *    calendar's registered courses and exam dates from its exams.
 *  - Each course's slides are analysed offline by
 *    scripts/build_exam_analysis.py into /account/calendar/exam-analysis/:
 *    chapters, slide counts, study time, and (for curated courses) every
 *    concept, formula, key number, list and problem type with how many
 *    slides repeat it.
 *  - Mark each item (or chapter, for baseline courses) New / Shaky / Solid.
 *    What's left to learn drives the schedule.
 *  - The scheduler fits learn, review and final-review sessions into free
 *    time before each exam, splitting hours by how much each course still
 *    needs per day left, and only uses more of the daily cap when needed.
 *    Sessions are saved as Study events (planSource "study-plan").
 *  - Remaining: every exam and deadline still ahead, in the order to start
 *    them, and how heavy each week looks against your free time. An
 *    overview only, with no chapters or practice.
 *  - Exam format: what the instructor said about an exam (question types,
 *    length, what's covered). It can narrow the exam's chapters and is noted
 *    on the scheduled sessions. Saved per exam in
 *    plan.formats, with the previous versions kept when it changes.
 *
 * The calendar page owns the data and saving; this reads it through
 * window.__shougCal and re-renders from renderAll().
 */
(function () {
  "use strict";
  if (window.__shougStudyPlan) return;

  var C = null,
    $ = function (id) {
      return document.getElementById(id);
    };
  var BASE = "/account/calendar/exam-analysis/";
  var SEASONS = [
    {
      id: "quiz",
      label: "Quizzes",
      noun: "Quiz",
      types: ["quiz", "bonus-quiz"],
    },
    { id: "midterm", label: "Midterms", noun: "Midterm", types: ["midterm"] },
    { id: "final", label: "Finals", noun: "Final", types: ["final"] },
    {
      id: "remaining",
      label: "Remaining",
      noun: "Exam",
      types: ["quiz", "bonus-quiz", "midterm", "final"],
    },
  ];
  // A comfortable amount of study for one course in a day, used to say
  // when to start on an exam.
  var EASY_DAY = 90;
  // How much study a day is realistic in total, for judging a week.
  var STUDY_DAY = 180;
  var LEVELS = ["New", "Shaky", "Solid", "Previously studied"];
  // Share of an item's study time still needed at each readiness level.
  // New material gets the most. Previously studied comes back faster than
  // learning it from scratch, so it gets less than Shaky, which you've said
  // you're unsure of. Rate a forgotten topic Shaky or New to give it more.
  var FACTOR = [1, 0.55, 0.15, 0.4];
  var DAY_START = 9 * 60,
    DAY_END = 22 * 60,
    BUFFER = 15,
    MAX_SESSION = 120,
    MIN_SESSION = 45,
    START_CAP = 240,
    FINAL_REACH = 5,
    MAX_CAP = 600;
  // A chapter counts as new when at least this share of its time is still to do.
  var NEW_SHARE = 0.7,
    RETEST = ":retest",
    QUICK = "quick",
    METHOD_NEW =
      "New material: explain each idea in your own words as you go, then spend the last 15 minutes writing what you remember with the slides closed.",
    METHOD_KNOWN =
      "Revision: test yourself from memory first, and only reopen the slides for what you missed.";
  var KIND_ORDER = [
    "calc",
    "formula",
    "number",
    "list",
    "process",
    "compare",
    "concept",
  ];
  var KIND_ONE = {
    calc: "Problem",
    formula: "Formula",
    number: "Number",
    list: "List",
    process: "Process",
    compare: "Compare",
    concept: "Concept",
  };
  var TIER_LABEL = { core: "Must know", high: "Likely", review: "Lower" };
  // Question formats an instructor might announce. `re` picks them out of
  // what the student types.
  var FORMATS = [
    {
      id: "compare",
      label: "Compare / contrast",
      short: "Compare",
      re: /compar|contrast|differen|versus|\bvs\b/i,
    },
    {
      id: "solve",
      label: "Problem solving",
      short: "Solving",
      re: /solv|problem|calculat|compute|numeric|math|work out/i,
    },
    {
      id: "code",
      label: "Code",
      short: "Code",
      re: /\bcode|coding|program|implement|java|python|c\+\+|pseudo|sql/i,
    },
    {
      id: "diagram",
      label: "Diagrams",
      short: "Diagrams",
      re: /diagram|draw|uml|sketch/i,
    },
    {
      id: "mcq",
      label: "Multiple choice",
      short: "MCQ",
      re: /multiple|mcq|choice|choose/i,
    },
    {
      id: "tf",
      label: "True / False",
      short: "T/F",
      re: /true|false|t\/f/i,
    },
    {
      id: "short",
      label: "Short answer",
      short: "Short answer",
      re: /short|defin|\blist\b|name the/i,
    },
    {
      id: "essay",
      label: "Explain / essay",
      short: "Explain",
      re: /essay|discuss|long answer|explain|paragraph/i,
    },
    {
      id: "fill",
      label: "Fill in / match",
      short: "Fill in",
      re: /fill|blank|match/i,
    },
    {
      id: "case",
      label: "Scenarios",
      short: "Scenarios",
      re: /case|scenario|situation/i,
    },
  ];
  var BOOK = {
    "": "Not said",
    closed: "Closed book",
    open: "Open book",
    sheet: "Cheat sheet allowed",
  };

  var index = null,
    files = {},
    pending = {},
    localPlan = null,
    saveTimer = null,
    ui = {
      course: "",
      preview: null,
      drill: true,
      revealed: {},
      open: {},
      readyOpen: {},
      fmtEdit: {},
      fmtCustom: {},
    };

  // ── Data ──────────────────────────────────────────────────────────────
  function fetchJson(url) {
    return fetch(url, { cache: "no-cache" }).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.json();
    });
  }
  function loadIndex() {
    if (index || pending.index) return;
    pending.index = true;
    fetchJson(BASE + "index.json")
      .then(function (j) {
        index = Array.isArray(j) ? j : [];
      })
      .catch(function () {
        index = [];
      })
      .then(render);
  }
  function entryFor(course, season) {
    var list = index || [];
    return (
      list.find(function (e) {
        return e.course === course && e.season === season;
      }) ||
      list.find(function (e) {
        return e.course === course && e.season === "final";
      }) ||
      null
    );
  }
  // null: no analysis for this course; undefined: still loading.
  function analysis(course, season) {
    if (!index) return undefined;
    var e = entryFor(course, season);
    if (!e) return null;
    if (files[e.file]) return files[e.file].failed ? null : files[e.file];
    if (!pending[e.file]) {
      pending[e.file] = true;
      fetchJson(BASE + e.file)
        .then(function (j) {
          files[e.file] = j;
        })
        .catch(function () {
          files[e.file] = { failed: true };
        })
        .then(render);
    }
    return undefined;
  }

  // The season being worked out, which may not be the one on screen: a
  // change to your week rebuilds every season that has a plan.
  var planningSid = null;
  function activeSeason() {
    return planningSid || season();
  }
  function withSeason(sid, fn) {
    var was = planningSid;
    planningSid = sid;
    try {
      return fn();
    } finally {
      planningSid = was;
    }
  }
  function plan() {
    return localPlan || C.studyPlan || {};
  }
  function studyLimits() {
    var x = plan().studyLimits || {};
    return { daily: Number(x.daily) || 10, weekly: Number(x.weekly) || 0 };
  }
  // Readiness taps save after a short pause so a run of taps is one write.
  function updatePlan(mutate, now, quiet) {
    var p = JSON.parse(JSON.stringify(plan()));
    mutate(p);
    localPlan = p;
    clearTimeout(saveTimer);
    var flush = function () {
      var toSave = localPlan;
      C.saveStudyPlan(toSave).then(
        function () {
          if (localPlan === toSave) localPlan = null;
        },
        function () {},
      );
    };
    if (now) flush();
    else saveTimer = setTimeout(flush, 700);
    if (!quiet) render();
  }
  function season() {
    var s = plan().season;
    return s !== "remaining" &&
      SEASONS.some(function (x) {
        return x.id === s;
      })
      ? s
      : "final";
  }
  function seasonInfo(id) {
    return SEASONS.find(function (s) {
      return s.id === id;
    });
  }
  function readyKey(course, a) {
    return course + "|" + a.season;
  }
  function level(course, a, unit) {
    var r = (plan().ready || {})[readyKey(course, a)] || {};
    if (Object.prototype.hasOwnProperty.call(r, unit)) return Number(r[unit]) || 0;
    return previouslyStudied(course, a, unit) ? 3 : 0;
  }
  function previouslyStudied(course, a, unit) {
    var current = examFor(course, activeSeason());
    if (!current || !current.date) return false;
    var chapterId = unit.indexOf("ch:") === 0 ? unit.slice(3) : null;
    if (!chapterId) {
      var item = itemById(a, unit);
      chapterId = item && item.chapter;
    }
    if (!chapterId) return false;
    return C.exams.some(function (earlier) {
      if (!earlier.date || earlier.date >= current.date || C.courseLabel(earlier.course) !== course) return false;
      var earlierType = C.canonicalExamType(earlier.type);
      if (["quiz", "bonus-quiz", "midterm", "final"].indexOf(earlierType) < 0) return false;
      var picked = earlier.chapters && earlier.chapters.length ? earlier.chapters : null;
      var earlierScope = picked
        ? a.chapters.map(function (ch) { return ch.id; }).filter(function (id) { return picked.indexOf(id) > -1; })
        : knownScope(a, earlier);
      return earlierScope.indexOf(chapterId) > -1;
    });
  }
  function migrateLegacyReadiness(sid) {
    if ((plan().readinessMigration || {})[sid] === "previously-studied-v1") return false;
    var exams = seasonExams(sid), changed = false;
    updatePlan(function (p) {
      p.ready = p.ready || {};
      exams.forEach(function (exam) {
        var course = C.courseLabel(exam.course), a = analysis(course, sid);
        if (!a) return;
        var record = p.ready[readyKey(course, a)];
        if (!record) return;
        Object.keys(record).forEach(function (unit) {
          if (Number(record[unit]) === 1 && previouslyStudied(course, a, unit)) {
            record[unit] = 3;
            changed = true;
          }
        });
      });
      p.readinessMigration = p.readinessMigration || {};
      p.readinessMigration[sid] = "previously-studied-v1";
    }, true);
    return changed;
  }
  function isRated(course, a, unit) {
    // Unselected topics use level 0 (New), so every in-scope unit has an
    // effective readiness value even before the student changes a control.
    return true;
  }
  function readinessProgress(sid) {
    var total = 0, marked = 0;
    seasonExams(sid).forEach(function (exam) {
      var course = C.courseLabel(exam.course), a = analysis(course, sid);
      if (!a) return;
      var ids = scopeIds(a, exam);
      a.chapters.forEach(function (ch) {
        if (ids.indexOf(ch.id) < 0) return;
        if (a.curated) chapterItems(a, ch.id).filter(isMainPointReadinessItem).forEach(function (item) {
          total++;
          marked++;
        });
        else {
          total++;
          marked++;
        }
      });
    });
    return { total: total, marked: marked, done: total > 0 && total === marked };
  }
  function recommendedMinutes(sid) {
    var first = firstStudyDay();
    return seasonExams(sid).reduce(function (sum, exam) {
      var course = C.courseLabel(exam.course), a = analysis(course, sid);
      if (!a || exam.date <= first) return sum;
      return sum + workMinutes(course, a, exam, sid);
    }, 0);
  }
  // Everything still to do for an exam: learning, reviews and the final
  // review, less what's already been covered.
  function workMinutes(course, a, exam, sid) {
    return withSeason(sid, function () {
      var sessions = sessionsFor(course, a, exam, sid);
      credit(sessions, course, a, exam, sid, firstStudyDay());
      return sessionMinutes(sessions);
    });
  }

  // ── Exams and courses ─────────────────────────────────────────────────
  function examTime(e) {
    return e.date + " " + (e.start || "00:00");
  }
  function seasonExams(sid) {
    var types = seasonInfo(sid).types,
      today = C.todayKey();
    return C.exams
      .filter(function (e) {
        return (
          e.date &&
          e.date >= today &&
          types.indexOf(C.canonicalExamType(e.type)) > -1
        );
      })
      .sort(function (a, b) {
        return examTime(a).localeCompare(examTime(b));
      });
  }
  function examFor(course, sid) {
    return (
      seasonExams(sid).find(function (e) {
        return C.courseLabel(e.course) === course;
      }) || null
    );
  }
  // The latest exam of this season that's already behind you.
  function pastExamFor(course, sid) {
    var types = seasonInfo(sid).types,
      today = C.todayKey(),
      past = C.exams
        .filter(function (e) {
          return (
            e.date &&
            e.date < today &&
            C.courseLabel(e.course) === course &&
            types.indexOf(C.canonicalExamType(e.type)) > -1
          );
        })
        .sort(function (a, b) {
          return examTime(b).localeCompare(examTime(a));
        });
    return past[0] || null;
  }
  // Exams that happened but were never put on the calendar.
  function markedDone(course, sid) {
    return Boolean(((plan().done || {})[sid] || {})[course]);
  }
  function courseList(sid) {
    var seen = {};
    C.knownCourses().forEach(function (c) {
      seen[c] = true;
    });
    seasonExams(sid).forEach(function (e) {
      var c = C.courseLabel(e.course);
      if (c && /\d{3}/.test(c)) seen[c] = true;
    });
    return Object.keys(seen).sort(function (a, b) {
      var ea = examFor(a, sid),
        eb = examFor(b, sid);
      if (ea && eb) return examTime(ea).localeCompare(examTime(eb));
      if (ea || eb) return ea ? -1 : 1;
      // Without an upcoming exam: missing dates first, finished ones last.
      var pa = pastExamFor(a, sid) || markedDone(a, sid),
        pb = pastExamFor(b, sid) || markedDone(b, sid);
      if (Boolean(pa) !== Boolean(pb)) return pa ? 1 : -1;
      return a.localeCompare(b);
    });
  }
  function daysUntil(k) {
    return Math.round((C.fromKey(k) - C.fromKey(C.todayKey())) / 86400000);
  }

  // ── Scope and remaining work ──────────────────────────────────────────
  // Which chapters an exam covers, from the course overview page's exam
  // cards (exam_scopes in the analysis). The Nth quiz or major of a course
  // on the calendar maps to its Nth card of that type; anything without a
  // card covers every chapter.
  function examScope(a, exam) {
    var base = overviewScope(a, exam),
      f = formatFor(C.courseLabel(a.course), exam, activeSeason()),
      // Chosen on the Exams tab; older plans kept them on the format.
      picked =
        exam && exam.chapters && exam.chapters.length
          ? exam.chapters
          : f && f.chapters && f.chapters.length
            ? f.chapters
            : null;
    if (!picked) return base;
    var ids = a.chapters
      .map(function (c) {
        return c.id;
      })
      .filter(function (id) {
        return picked.indexOf(id) > -1;
      });
    return ids.length ? { ids: ids, label: base.label, custom: true } : base;
  }
  function overviewScope(a, exam) {
    var all = a.chapters.map(function (c) {
      return c.id;
    });
    var type = exam ? C.canonicalExamType(exam.type) : activeSeason();
    if (type === "bonus-quiz") type = "quiz";
    var cards = (a.exam_scopes || []).filter(function (x) {
      return x.type === type;
    });
    if (!cards.length) return { ids: all, label: "", assumed: true };
    var n = 0;
    if (exam) {
      var course = C.courseLabel(exam.course),
        same = C.exams
          .filter(function (e) {
            var t = C.canonicalExamType(e.type);
            return (
              C.courseLabel(e.course) === course &&
              (t === "bonus-quiz" ? "quiz" : t) === type
            );
          })
          .sort(function (x, y) {
            return examTime(x).localeCompare(examTime(y));
          });
      n = Math.max(0, same.indexOf(exam));
    }
    var card = cards[Math.min(n, cards.length - 1)],
      ids = all.filter(function (id) {
        return card.chapters.indexOf(id) > -1;
      });
    return { ids: ids.length ? ids : all, label: card.label };
  }
  // What an earlier exam is known to have covered. With no chapters picked
  // and no card for it, that's unknown, so nothing counts as studied.
  function knownScope(a, exam) {
    var scope = overviewScope(a, exam);
    return scope.assumed ? [] : scope.ids;
  }
  // ── Exam format ──────────────────────────────────────────────────────
  // Saved per calendar exam; before the exam has a date it's saved per
  // course and season, and that one still applies once the date is added.
  function formatKeys(course, exam, sid) {
    return (exam ? ["exam:" + exam.id] : []).concat(course + "|" + sid);
  }
  function formatFor(course, exam, sid) {
    var all = plan().formats || {},
      keys = formatKeys(course, exam, sid);
    for (var n = 0; n < keys.length; n++) if (all[keys[n]]) return all[keys[n]];
    return null;
  }
  function formatInfo(id) {
    return FORMATS.find(function (f) {
      return f.id === id;
    });
  }
  function detectFormats(text) {
    return FORMATS.filter(function (f) {
      return f.re.test(text || "");
    }).map(function (f) {
      return f.id;
    });
  }
  function formatSummary(f, short) {
    if (!f) return "";
    var parts = (f.types || []).map(function (id) {
      var x = formatInfo(id);
      return x ? (short ? x.short : x.label) : id;
    });
    if (short) return parts.join(" · ");
    if (f.questions) parts.push(f.questions + " questions");
    if (f.minutes) parts.push(f.minutes + " min");
    if (f.book) parts.push(BOOK[f.book]);
    return parts.join(" · ");
  }
  function scopeIds(a, exam) {
    return examScope(a, exam).ids;
  }
  function chapterItems(a, chId) {
    return (a.items || []).filter(function (i) {
      return i.chapter === chId;
    });
  }
  // Readiness is a quick check of each slide's main takeaway, not every
  // detail. Conceptual topics are included by default; inventory items such
  // as SOLID can opt in even when their analysis kind is a list or problem.
  // Formula drills, number tables and memorization details stay out unless
  // explicitly marked readiness:true in the source inventory.
  function isMainPointReadinessItem(item) {
    if (item.readiness !== undefined) return item.readiness === true;
    return ["concept", "compare", "process", "list"].indexOf(item.kind) > -1;
  }
  // Mastery is a rating, while scheduled minutes are a separate estimate.
  // Solid means fully ready even though the plan can still reserve review time.
  function levelReadiness(levelIndex) {
    return [0, 50, 100, 50][levelIndex] || 0;
  }
  function chapterReadiness(course, a, ch) {
    if (ch.upcoming) return null;
    if (!a.curated) return levelReadiness(level(course, a, "ch:" + ch.id));
    var its = chapterItems(a, ch.id).filter(isMainPointReadinessItem),
      total = 0,
      ready = 0;
    its.forEach(function (i) {
      var weight = Math.max(1, Number(i.minutes) || 0);
      total += weight;
      ready += weight * levelReadiness(level(course, a, i.id));
    });
    return total ? Math.round(ready / total) : null;
  }
  // Minutes still needed for a chapter: its study time scaled by how much
  // of its items' time is left (curated), or by the chapter's own level.
  function chapterLeft(course, a, ch) {
    if (!a.curated) return ch.minutes * FACTOR[level(course, a, "ch:" + ch.id)];
    var its = chapterItems(a, ch.id),
      total = 0,
      left = 0;
    its.forEach(function (i) {
      total += i.minutes;
      left += i.minutes * FACTOR[level(course, a, i.id)];
    });
    return total ? ch.minutes * (left / total) : ch.minutes;
  }
  function courseProgress(course, a, exam) {
    var ids = scopeIds(a, exam),
      total = 0,
      left = 0,
      readinessTotal = 0,
      readinessWeight = 0;
    a.chapters.forEach(function (ch) {
      if (ids.indexOf(ch.id) < 0) return;
      total += ch.minutes;
      left += chapterLeft(course, a, ch);
      var readiness = chapterReadiness(course, a, ch);
      if (readiness !== null) {
        var weight = a.curated
          ? chapterItems(a, ch.id).filter(isMainPointReadinessItem).reduce(function (sum, item) {
              return sum + Math.max(1, Number(item.minutes) || 0);
            }, 0)
          : ch.minutes;
        if (weight) {
          readinessTotal += readiness * weight;
          readinessWeight += weight;
        }
      }
    });
    return {
      total: total,
      left: left,
      work: exam ? workMinutes(course, a, exam, examSeason(exam)) : left,
      ready: readinessWeight ? Math.round(readinessTotal / readinessWeight) : 0,
    };
  }
  function hours(min) {
    var h = min / 60;
    return (h >= 10 ? Math.round(h) : Math.round(h * 2) / 2) + " h";
  }
  function round15(m) {
    return Math.max(15, Math.round(m / 15) * 15);
  }

  // ── Scheduler ─────────────────────────────────────────────────────────
  // "Ch 3 · Media access control" reads as "Ch 3 Media access control".
  function chapterName(ch) {
    return String(ch.title).replace(" · ", " ");
  }
  function sessionsFor(course, a, exam, sid) {
    var noun = seasonInfo(sid).noun,
      ids = scopeIds(a, exam),
      learn = [],
      reviews = {},
      fmt = formatFor(course, exam, sid),
      fTypes = (fmt && fmt.types) || [],
      fmtLine = fTypes.length
        ? "Exam format: " + formatSummary(fmt) + ". "
        : "",
      heldForReview = null;
    var orderedChapters = a.chapters
        .filter(function (c) {
          return ids.indexOf(c.id) > -1;
        })
        .sort(function (x, y) {
          var xp = x.minutes ? chapterLeft(course, a, x) / x.minutes : 0,
            yp = y.minutes ? chapterLeft(course, a, y) / y.minutes : 0;
          return yp - xp || a.chapters.indexOf(x) - a.chapters.indexOf(y);
        });
    var reviewChapters = orderedChapters.filter(function (c) {
      return chapterLeft(course, a, c) >= 15;
    }).map(function (c) { return c.id; });
    // New chapters go first, in course order, so if the calendar runs out of
    // room it's revision of known material that gets squeezed. Part of a new
    // chapter's time moves from reading to a later retest, because recalling
    // something after a gap makes it stick better than more time on the slides.
    var quick = [],
      quickMinutes = 0,
      retestMinutes = 0;
    orderedChapters.forEach(function (ch) {
      var left = chapterLeft(course, a, ch);
      if (left < 15) {
        if (left > 0) {
          quick.push(ch);
          quickMinutes += left;
        }
        return;
      }
      var isNew = ch.minutes && left / ch.minutes >= NEW_SHARE && left >= 60,
        retest = isNew ? Math.min(45, round15(left * 0.15)) : 0,
        remaining = Math.ceil(left) - retest,
        n = Math.ceil(remaining / MAX_SESSION),
        method = isNew ? METHOD_NEW : METHOD_KNOWN,
        name = course + " " + noun + " · " + chapterName(ch),
        focus = chapterItems(a, ch.id)
          .filter(isMainPointReadinessItem)
          .filter(function (i) {
            return level(course, a, i.id) !== 2;
          })
          .sort(function (x, y) {
            return y.score - x.score;
          })
          .slice(0, 5)
          .map(function (i) {
            return i.name;
          });
      for (var k = 0; k < n; k++) {
        var part = Math.ceil(remaining / (n - k));
        remaining -= part;
        learn.push({
          kind: "learn",
          chapter: ch.id,
          last: k === n - 1,
          minutes: part,
          title: name + (k ? " (continued)" : ""),
          notes: fmtLine + method + (focus.length ? " Focus: " + focus.join("; ") : ""),
        });
      }
      retestMinutes += retest;
      // Chapters are reviewed two at a time, after the second is learned.
      var paired = heldForReview;
      heldForReview = paired ? null : ch;
      if (!paired && reviewChapters.indexOf(ch.id) < reviewChapters.length - 1)
        return;
      // Reviews scale with the work: a chapter you already know needs less.
      var pairLeft = left + (paired ? chapterLeft(course, a, paired) : 0);
      reviews[ch.id] = {
        kind: "review",
        chapter: ch.id,
        minutes: Math.min(paired ? 45 : 30, round15(pairLeft * 0.5)),
        notBefore: null,
        title:
          course +
          " " +
          noun +
          " · Review " +
          (paired ? chapterName(paired) + " and " : "") +
          chapterName(ch),
        notes:
          fmtLine +
          "Active recall: close the slides, write what you remember, then check.",
      };
      if (retestMinutes) {
        reviews[ch.id + RETEST] = {
          kind: "review",
          retest: true,
          after: ch.id,
          chapter: ch.id + RETEST,
          minutes: retestMinutes,
          notBefore: null,
          title:
            course +
            " " +
            noun +
            " · Retest " +
            (paired ? chapterName(paired) + " and " : "") +
            chapterName(ch),
          notes:
            fmtLine +
            "Retest from memory with the slides closed, mixing the chapters. Spend the time on what you still miss.",
        };
        retestMinutes = 0;
      }
      });
    if (quick.length) {
      var quickLeft = Math.ceil(quickMinutes),
        pieces = Math.ceil(quickLeft / MAX_SESSION),
        quickName =
          course +
          " " +
          noun +
          " · Quick check of " +
          quick.length +
          " solid chapter" +
          (quick.length === 1 ? "" : "s");
      for (var q = 0; q < pieces; q++) {
        var quickPart = Math.ceil(quickLeft / (pieces - q));
        quickLeft -= quickPart;
        learn.push({
          kind: "learn",
          chapter: QUICK,
          last: false,
          minutes: quickPart,
          title: quickName + (q ? " (continued)" : ""),
          notes:
            fmtLine +
            "Test yourself on each, from memory: " +
            quick.map(chapterName).join("; "),
        });
      }
    }
    return {
      learn: learn,
      reviews: reviews,
      final: learn.length
        ? {
            kind: "final",
            minutes: a.curated ? 120 : 90,
            title: course + " " + noun + " · Final review",
            notes:
              fmtLine +
              (a.curated
                ? "Timed practice under exam conditions, one problem of each type, then fix what you got wrong. Finish with the memorize sheet."
                : "Timed self-test across every chapter, then go back over what you got wrong and anything marked Shaky."),
          }
        : null,
    };
  }
  function sessionMinutes(s) {
    var total = s.learn.reduce(function (sum, item) {
      return sum + item.minutes;
    }, 0);
    Object.keys(s.reviews).forEach(function (key) {
      total += s.reviews[key].minutes;
    });
    if (s.final) total += s.final.minutes;
    return total;
  }
  function daysBetween(from, to) {
    return Math.round((C.fromKey(to) - C.fromKey(from)) / 86400000);
  }
  // A gap of a fair share of the time left before the exam works best, within
  // sensible limits. It's never later than the day before the last day.
  function reviewDay(day, exam, share, shortest, longest) {
    var last = C.addDays(exam.date, -1),
      gap = Math.min(longest, Math.max(shortest, Math.round(daysBetween(day, exam.date) * share))),
      target = C.addDays(day, gap),
      latest = C.addDays(last, -1);
    if (target > latest) target = latest;
    if (target <= day) target = C.addDays(day, 1) > last ? day : C.addDays(day, 1);
    return target;
  }
  function firstReviewDay(day, exam) {
    return reviewDay(day, exam, 0.15, 2, 5);
  }
  function retestDay(day, exam) {
    return reviewDay(day, exam, 0.3, 3, 10);
  }
  function firstStudyDay() {
    var now = new Date(),
      nowMin = now.getHours() * 60 + now.getMinutes(),
      today = C.todayKey(),
      startToday = Math.max(DAY_START, Math.ceil((nowMin + 30) / 15) * 15);
    return startToday > DAY_END - MIN_SESSION ? C.addDays(today, 1) : today;
  }
  // Minutes of driving each way to campus (plan.commute, 30 if never set).
  function commute() {
    var v = Number(plan().commute);
    return plan().commute === undefined || !isFinite(v) || v < 0 ? 30 : v;
  }
  // When you're on campus: the first in-person class or exam to the end of
  // the last one. Online classes don't count.
  function campusSpan(day) {
    var span = null;
    C.eventsFor(day, true).forEach(function (e) {
      if (!e.start || !((e.kind === "class" && !e.online) || e.kind === "exam"))
        return;
      var s = C.minutes(e.start),
        en = e.end ? C.minutes(e.end) : s + (e.kind === "exam" ? 120 : 60);
      if (s === null) return;
      span = span ? [Math.min(span[0], s), Math.max(span[1], en)] : [s, en];
    });
    return span;
  }
  var UNI_DAYS = [
    "sunday",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
  ];
  // Days being previewed as staying home, before you've agreed to it.
  var homeDays = {};
  // Your usual times for a weekday (plan.uni[weekday] = {leave, back}).
  function uniTimes(day) {
    return (plan().uni || {})[UNI_DAYS[C.fromKey(day).getDay()]] || {};
  }
  // The two drives on a uni day. Times you've set for the weekday win; the
  // rest come from your first and last campus class or exam. Your times
  // also count on online-class days, since you said you go in, but not on
  // days with no class at all (holidays, breaks).
  function uniTrip(day) {
    var span = campusSpan(day),
      t = uniTimes(day),
      drive = commute(),
      leave = t.leave ? C.minutes(t.leave) : null,
      back = t.back ? C.minutes(t.back) : null;
    if (!span) {
      // You said you'd stay home when this day's classes went online.
      if (homeDays[day] || (plan().uniHome || {})[day]) return null;
      var anyClass = C.eventsFor(day, true).some(function (e) {
        return e.kind === "class";
      });
      if (!anyClass || leave === null || back === null) return null;
    }
    if (leave === null || (span && leave + drive > span[0]))
      leave = span[0] - drive;
    if (back === null || (span && back < span[1])) back = span[1];
    return {
      leave: leave,
      arrive: leave + drive,
      back: back,
      home: back + drive,
      drive: drive,
      set: Boolean(t.leave || t.back),
    };
  }
  function busyFor(day, sid) {
    var all = false,
      busy = [];
    C.eventsFor(day, true).forEach(function (e) {
      var raw =
        e.itemId &&
        C.items.find(function (i) {
          return i.id === e.itemId;
        });
      // The plan being rebuilt doesn't block itself, except sessions it
      // keeps: ones you moved or edited yourself, or already ticked off.
      if (
        raw &&
        raw.planSource === "study-plan" &&
        (sid === "remaining" ||
          (raw.planSeason === sid && !raw.planPinned && !raw.planDone))
      )
        return;
      if (!e.start) {
        if (e.kind === "busy" || e.kind === "travel") all = true;
        return;
      }
      // Nothing else gets scheduled before an exam on its day, nor in the
      // hour after it.
      if (e.kind === "exam") {
        var ee = e.end ? C.minutes(e.end) : C.minutes(e.start) + 120;
        busy.push([0, ee + 60]);
        return;
      }
      var s = C.minutes(e.start),
        en = e.end ? C.minutes(e.end) : s + 60;
      if (s === null) return;
      busy.push([s - BUFFER, Math.max(en, s + 15) + BUFFER]);
    });
    // Times you said you can't study.
    blocksOn(day).forEach(function (x) {
      if (!x.start || !x.end) all = true;
      else busy.push([C.minutes(x.start), C.minutes(x.end)]);
    });
    // The drive there and back. Gaps on campus stay free for study.
    var trip = uniTrip(day);
    if (trip) {
      busy.push([trip.leave - BUFFER, trip.arrive]);
      busy.push([trip.back, trip.home + BUFFER]);
    }
    return { all: all, busy: busy };
  }
  // Times you can't study (plan.blocked): weekly on the chosen weekdays,
  // or one date. No times means the whole day.
  function blocks() {
    return Array.isArray(plan().blocked) ? plan().blocked : [];
  }
  function blocksOn(day) {
    var wd = C.fromKey(day).getDay();
    return blocks().filter(function (x) {
      if (x.date) return x.date === day;
      if ((x.skips || []).indexOf(day) > -1) return false;
      return (x.days || []).indexOf(wd) > -1;
    });
  }
  function freeSlots(day, sid, startMin) {
    var b = busyFor(day, sid);
    if (b.all) return [];
    var slots = [[startMin, DAY_END]];
    b.busy.forEach(function (x) {
      var next = [];
      slots.forEach(function (s) {
        if (x[1] <= s[0] || x[0] >= s[1]) next.push(s);
        else {
          if (x[0] > s[0]) next.push([s[0], x[0]]);
          if (x[1] < s[1]) next.push([x[1], s[1]]);
        }
      });
      slots = next;
    });
    return slots.filter(function (s) {
      return s[1] - s[0] >= MIN_SESSION;
    });
  }
  // spread: how far above its even daily share a course may go in one day.
  // Low values pace the work out evenly up to each exam; the caller raises it
  // with the daily cap when the plan doesn't fit.
  function attempt(jobs, days, ctx, cap, spread, weeklyCap, earliestFirst) {
    var placed = [],
      weekUsed = Object.assign({}, ctx.weekBase),
      dayUsed = {},
      daySlots = {},
      lastJob = null;
    days.forEach(function (day) {
      dayUsed[day] = ctx.dayBase[day] || 0;
      daySlots[day] = ctx.slots[day].map(function (x) {
        return x.slice();
      });
    });
    jobs.forEach(function (j) {
      j.q = j.s.learn.map(function (x) {
        return Object.assign({}, x);
      });
      j.rev = {};
      Object.keys(j.s.reviews).forEach(function (k) {
        j.rev[k] = Object.assign({}, j.s.reviews[k]);
      });
      j.fin = j.s.final ? Object.assign({}, j.s.final) : null;
      j.lastDay = C.addDays(j.exam.date, -1);
    });
    function pendingMin(j) {
      var m = 0;
      j.q.forEach(function (x) {
        m += x.minutes;
      });
      Object.keys(j.rev).forEach(function (k) {
        m += j.rev[k].minutes;
      });
      return m;
    }
    function biggest(day) {
      return daySlots[day].reduce(function (m, s) {
        return Math.max(m, s[1] - s[0]);
      }, 0);
    }
    // The most study a day can still take, inside your limits and its gaps.
    function roomOn(day) {
      var week = weekStart(day);
      return Math.min(
        cap - dayUsed[day],
        weeklyCap ? weeklyCap - (weekUsed[week] || 0) : Infinity,
        biggest(day),
      );
    }
    // Largest piece that fits without leaving under 15 minutes behind.
    function pieceFor(minutes, room) {
      var len = Math.min(minutes, Math.floor(room / 15) * 15);
      if (len < MIN_SESSION) len = Math.min(minutes, room);
      if (len < minutes && minutes - len < 15 && len - 15 >= 15) len -= 15;
      return len;
    }
    function put(j, sess, len, day) {
      var slots = daySlots[day];
      for (var i = 0; i < slots.length; i++) {
        if (slots[i][1] - slots[i][0] < len) continue;
        var st = slots[i][0];
        slots[i] = [st + len + BUFFER, slots[i][1]];
        dayUsed[day] += len;
        weekUsed[weekStart(day)] = (weekUsed[weekStart(day)] || 0) + len;
        placed.push({
          exam: j.exam,
          course: j.course,
          date: day,
          start: C.toTime(st),
          end: C.toTime(st + len),
          minutes: len,
          kind: sess.kind,
          retest: Boolean(sess.retest),
          chapter: sess.chapter || "",
          slot: i,
          title:
            sess.title +
            (sess.cont && !/\(continued\)$/.test(sess.title)
              ? " (continued)"
              : ""),
          notes: sess.notes,
        });
        return true;
      }
      return false;
    }
    // Final reviews are placed first, so nothing crowds them out: the day
    // before the exam if it has room, otherwise the few days leading up to it.
    // A long one is split across days rather than breaking your limit.
    jobs.forEach(function (j) {
      if (!j.fin) return;
      var left = j.fin.minutes,
        earliest = C.addDays(j.lastDay, -FINAL_REACH);
      for (var d = j.lastDay; left > 0 && d >= earliest; d = C.addDays(d, -1)) {
        if (!daySlots[d]) continue;
        var room = roomOn(d);
        if (room < Math.min(MIN_SESSION, left)) continue;
        var len = pieceFor(left, room);
        if (len > 0 && put(j, j.fin, len, d)) left -= len;
      }
      j.fin = left > 0 ? Object.assign({}, j.fin, { minutes: left }) : null;
    });
    days.forEach(function (day) {
      // A course with nothing placeable today (only reviews not yet due)
      // sits out the rest of the day instead of ending it for everyone.
      var resting = [];
      jobs.forEach(function (j) {
        j.today = 0;
        var left =
          Math.round((C.fromKey(j.lastDay) - C.fromKey(day)) / 86400000) + 1;
        // The last three days before an exam have no per-course limit.
        j.limit =
          left <= 3 || earliestFirst
            ? Infinity
            : Math.max(
                MAX_SESSION,
                Math.ceil(((pendingMin(j) / Math.max(1, left)) * spread) / 15) *
                  15,
              );
      });
      for (var guard = 0; guard < 60; guard++) {
        var best = null,
          bestU = -1;
        jobs.forEach(function (j) {
          if (day > j.lastDay || resting.indexOf(j) > -1 || j.today >= j.limit)
            return;
          var p = pendingMin(j);
          if (!p) return;
          var left = Math.max(
            1,
            Math.round((C.fromKey(j.lastDay) - C.fromKey(day)) / 86400000) + 1,
          );
          var u = earliestFirst ? 100000 - left : p / left;
          // Switch courses between sessions when another is nearly as urgent.
          if (j === lastJob) {
            if (earliestFirst) u -= 7;
            else u *= 0.75;
          }
          if (u > bestU) {
            bestU = u;
            best = j;
          }
        });
        if (!best) break;
        var room = Math.min(roomOn(day), best.limit - best.today);
        if (room < MIN_SESSION) break;
        // Don't start a sliver of a session; leave it for a day with room.
        var nextLen = (best.q[0] || {}).minutes || 0;
        if (nextLen && room < Math.min(60, nextLen) && !Object.keys(best.rev).some(function (k) {
          return best.rev[k].notBefore && best.rev[k].notBefore <= day;
        })) {
          resting.push(best);
          continue;
        }
        var reviewId = Object.keys(best.rev).find(function (k) {
          var r = best.rev[k];
          return r.notBefore && r.notBefore <= day;
        });
        var sess = reviewId ? best.rev[reviewId] : best.q[0];
        if (!sess) {
          // Only reviews that aren't due yet are left for this course.
          var waiting = Object.keys(best.rev).filter(function (k) {
            return !best.rev[k].notBefore || best.rev[k].notBefore > day;
          });
          if (!waiting.length) {
            resting.push(best);
            continue;
          }
          // Reviews of chapters this plan never studied (all Solid) drop. A
          // retest still waiting on its first review isn't one of those.
          var course = best,
            unstudied = waiting.filter(function (k) {
              var r = course.rev[k];
              return !r.notBefore && !(r.after && course.rev[r.after]);
            });
          if (unstudied.length && !best.q.length) {
            unstudied.forEach(function (k) {
              delete best.rev[k];
            });
            continue;
          }
          // Otherwise wait for the review to come due.
          resting.push(best);
          continue;
        }
        var len = pieceFor(sess.minutes, room);
        if (!len || !put(best, sess, len, day)) {
          resting.push(best);
          continue;
        }
        best.today += len;
        lastJob = best;
        if (len < sess.minutes) {
          sess.cont = true;
          sess.minutes -= len;
          continue;
        }
        if (reviewId) {
          delete best.rev[reviewId];
          var retest = best.rev[reviewId + RETEST];
          if (retest) retest.notBefore = retestDay(day, best.exam);
        } else {
          best.q.shift();
          if (sess.last && best.rev[sess.chapter])
            best.rev[sess.chapter].notBefore = firstReviewDay(day, best.exam);
        }
      }
    });
    var short = 0;
    jobs.forEach(function (j) {
      j.left = pendingMin(j) + (j.fin ? j.fin.minutes : 0);
      short += j.left;
    });
    return {
      placed: placed,
      short: short,
      lefts: jobs.map(function (j) {
        return j.left;
      }),
    };
  }
  // Back-to-back pieces of the same chapter become one session, and a course's
  // first reviews on the same day sit together, up to a normal session length.
  // Only pieces in the same free stretch join, so nothing between them is
  // covered, and the break goes: the session is exactly the study it holds.
  function mergeSessions(list) {
    var out = [];
    list.forEach(function (p) {
      var last = out[out.length - 1];
      if (
        last &&
        last.date === p.date &&
        last.slot === p.slot &&
        last.course === p.course &&
        last.exam === p.exam &&
        last.kind === p.kind &&
        p.kind !== "final" &&
        !last.retest &&
        !p.retest &&
        (p.kind === "review" || last.chapter === p.chapter) &&
        C.minutes(p.start) - C.minutes(last.end) <= BUFFER &&
        last.minutes + p.minutes <= MAX_SESSION
      ) {
        last.end = C.toTime(C.minutes(last.end) + p.minutes);
        last.minutes += p.minutes;
        if (p.kind === "review") {
          last.title = last.title + ", " + p.title.split(" · Review ")[1];
          last.chapters = (last.chapters || [last.chapter]).concat(p.chapter);
          last.chapter = "";
        }
        return;
      }
      out.push(Object.assign({}, p));
    });
    return out;
  }
  // Study already on the calendar that this build won't replace. It uses up
  // your limits like anything newly planned.
  function fixedStudyMinutes(i, sid) {
    if ((i.kind !== "study" && i.planSource !== "study-plan") || !i.date || !i.start || !i.end)
      return 0;
    if (i.planSource === "study-plan" && i.planSeason === sid && !i.planPinned && !i.planDone)
      return 0;
    return Math.max(0, C.minutes(i.end) - C.minutes(i.start));
  }
  function buildSchedule(sid) {
    return withSeason(sid, function () {
      return buildScheduleNow(sid);
    });
  }
  function buildScheduleNow(sid) {
    var now = new Date(),
      nowMin = now.getHours() * 60 + now.getMinutes(),
      today = C.todayKey(),
      startToday = Math.max(DAY_START, Math.ceil((nowMin + 30) / 15) * 15),
      first = startToday > DAY_END - MIN_SESSION ? C.addDays(today, 1) : today;
    if (first !== today) startToday = DAY_START;
    var jobs = [],
      skipped = [];
    seasonExams(sid).forEach(function (exam) {
      var course = C.courseLabel(exam.course),
        a = analysis(course, sid);
      if (!a) {
        skipped.push(course);
        return;
      }
      if (exam.date <= first) return;
      var s = sessionsFor(course, a, exam, sid);
      credit(s, course, a, exam, sid, first);
      jobs.push({ course: course, exam: exam, a: a, s: s });
    });
    if (!jobs.length) return { jobs: [], placed: [], skipped: skipped };
    var lastDay = jobs.reduce(function (m, j) {
        var d = C.addDays(j.exam.date, -1);
        return d > m ? d : m;
      }, first),
      days = [];
    for (var d = first; d <= lastDay; d = C.addDays(d, 1)) days.push(d);
    var ctx = { slots: {}, dayBase: {}, weekBase: {} };
    days.forEach(function (day, di) {
      ctx.slots[day] = freeSlots(day, sid, di === 0 ? startToday : DAY_START);
    });
    C.items.forEach(function (i) {
      var m = fixedStudyMinutes(i, sid);
      if (!m) return;
      ctx.dayBase[i.date] = (ctx.dayBase[i.date] || 0) + m;
      var w = weekStart(i.date);
      ctx.weekBase[w] = (ctx.weekBase[w] || 0) + m;
    });
    // Start close to an even daily pace, and only ask more of a day when the
    // work doesn't fit. Each step first lets a course run ahead of its even
    // share, then tries earliest exam first, and only then raises the daily
    // cap, stopping at the limit you chose. If it never all fits, the lowest
    // cap that gets furthest wins.
    var limits = studyLimits(),
      totalNeed = jobs.reduce(function (sum, j) {
        return sum + sessionMinutes(j.s);
      }, 0),
      averageDaily = totalNeed / Math.max(1, days.length),
      dailyCap = Math.min(Math.round(limits.daily * 60), MAX_CAP),
      weeklyCap = limits.weekly ? Math.round(limits.weekly * 60) : 0,
      PACES = [1.25, 2, 3, 4, 0],
      cap = Math.min(dailyCap, Math.max(START_CAP, Math.ceil(averageDaily / 30) * 30)),
      res = null,
      usedCap = cap;
    for (;;) {
      for (var sp = 0; sp < PACES.length; sp++) {
        var tried = attempt(jobs, days, ctx, cap, PACES[sp], weeklyCap, !PACES[sp]);
        if (!res || tried.short < res.short) {
          res = tried;
          usedCap = cap;
        }
        if (!res.short) break;
      }
      if (!res.short || cap >= dailyCap) break;
      cap = Math.min(dailyCap, cap + 30);
    }
    cap = usedCap;
    res.placed.sort(function (x, y) {
      return (x.date + x.start).localeCompare(y.date + y.start);
    });
    res.placed = mergeSessions(res.placed);
    return {
      jobs: jobs.map(function (j, n) {
        var need = sessionMinutes(j.s);
        return { course: j.course, exam: j.exam, need: need, left: res.lefts[n] };
      }),
      placed: res.placed,
      cap: cap,
      short: res.short,
      first: first,
      skipped: skipped,
    };
  }
  // Sessions a rebuild keeps: days already behind you (a missed session
  // you didn't delete counts as studied), ones you moved or edited, and
  // ones ticked off. Everything else from today on is replaced.
  function kept(i, sid, first) {
    return (
      i.planSource === "study-plan" &&
      i.planSeason === sid &&
      (i.date < first || i.planPinned || i.planDone)
    );
  }
  function sessionChapter(i, course, a, sid) {
    if (i.planChapter) return i.planChapter;
    var noun = seasonInfo(sid).noun,
      title = String(i.title || "").replace(/ \(continued\)$/, ""),
      ch = a.chapters.find(function (c) {
        var name = course + " " + noun + " · ";
        return (
          title === name + chapterName(c) ||
          title === name + "Review " + chapterName(c)
        );
      });
    return ch ? ch.id : "";
  }
  // Which reviews a kept session covers. Reviews merged before sessions
  // recorded their chapters are recognised by the chapter names in the title.
  function reviewKeys(i, course, a, sid, s) {
    if (i.planChapters && i.planChapters.length) return i.planChapters;
    var ch = sessionChapter(i, course, a, sid);
    if (ch) return [ch];
    return Object.keys(s.reviews).filter(function (k) {
      var c = a.chapters.find(function (x) {
        return x.id === k;
      });
      return c && String(i.title || "").indexOf(chapterName(c)) > -1;
    });
  }
  // Take the kept sessions' work out of what's left, so a rebuild only
  // schedules what hasn't been covered yet.
  function credit(s, course, a, exam, sid, first) {
    var learnt = {},
      reviewed = {};
    C.items.forEach(function (i) {
      if (!kept(i, sid, first)) return;
      if (
        i.linkedExamId
          ? i.linkedExamId !== exam.id
          : C.courseLabel(i.course) !== course
      )
        return;
      if (i.planKind === "final") {
        if (s.final) {
          var done =
            i.start && i.end ? C.minutes(i.end) - C.minutes(i.start) : s.final.minutes;
          s.final.minutes -= done;
          if (s.final.minutes <= 0) s.final = null;
        }
        return;
      }
      if (i.planKind === "review") {
        reviewKeys(i, course, a, sid, s).forEach(function (k) {
          delete s.reviews[k];
          if (!reviewed[k] || i.date > reviewed[k]) reviewed[k] = i.date;
        });
        return;
      }
      var ch = sessionChapter(i, course, a, sid);
      if (!ch) return;
      var m =
        i.start && i.end ? C.minutes(i.end) - C.minutes(i.start) : MIN_SESSION;
      s.learn.forEach(function (x) {
        if (x.chapter !== ch || m <= 0) return;
        var used = Math.min(m, x.minutes);
        x.minutes -= used;
        m -= used;
      });
      s.learn = s.learn.filter(function (x) {
        return x.minutes > 0;
      });
      if (!learnt[ch] || i.date > learnt[ch]) learnt[ch] = i.date;
    });
    // A chapter you've finished learning gets its review a few days on.
    Object.keys(learnt).forEach(function (ch) {
      var r = s.reviews[ch];
      if (
        !r ||
        s.learn.some(function (x) {
          return x.chapter === ch;
        })
      )
        return;
      var nb = firstReviewDay(learnt[ch], exam);
      r.notBefore = nb < first ? first : nb;
    });
    // A retest follows its first review, once that's done.
    Object.keys(s.reviews).forEach(function (k) {
      var r = s.reviews[k];
      if (!r.after || r.notBefore || s.reviews[r.after]) return;
      var nb = reviewed[r.after] ? retestDay(reviewed[r.after], exam) : first;
      r.notBefore = nb < first ? first : nb;
    });
  }
  function plannedItems(sid) {
    var today = C.todayKey();
    return C.items.filter(function (i) {
      return (
        i.planSource === "study-plan" && i.planSeason === sid && i.date >= today
      );
    });
  }
  function removePlanned(sid) {
    var drop = plannedItems(sid);
    for (var i = C.items.length - 1; i >= 0; i--)
      if (drop.indexOf(C.items[i]) > -1) C.items.splice(i, 1);
    return drop.length;
  }
  // Swap the season's replaceable sessions for a fresh schedule. Sessions
  // for courses the schedule couldn't build stay put.
  function applySchedule(sid, pv) {
    var built = pv.jobs.map(function (j) {
        return j.exam.id;
      }),
      first = pv.first || C.todayKey(),
      n = 0;
    for (var i = C.items.length - 1; i >= 0; i--) {
      var it = C.items[i];
      if (
        it.planSource === "study-plan" &&
        it.planSeason === sid &&
        it.date >= first &&
        !kept(it, sid, first) &&
        (!it.linkedExamId || built.indexOf(it.linkedExamId) > -1)
      ) {
        C.items.splice(i, 1);
        n++;
      }
    }
    pv.placed.forEach(function (p) {
      var item = {
        id: C.uid(),
        title: p.title,
        date: p.date,
        endDate: p.date,
        kind: "study",
        start: p.start,
        end: p.end,
        location: "",
        course: p.course,
        notes: p.notes || "",
        linkedExamId: p.exam.id,
        planSource: "study-plan",
        planSeason: sid,
        planKind: p.kind,
        planChapter: p.chapter || "",
      };
      if (p.chapters) item.planChapters = p.chapters;
      C.items.push(item);
    });
    return n;
  }
  function commitPreview() {
    var sid = season(),
      pv = ui.preview;
    if (!pv || !pv.placed.length) return;
    if (!C.signedIn) {
      C.toast("Sign in to save your study plan");
      return;
    }
    applySchedule(sid, pv);
    var n = pv.placed.length;
    ui.preview = null;
    ui.view = "plan";
    C.persist().then(function () {
      C.renderAll();
      C.toast(
        n + " study session" + (n === 1 ? "" : "s") + " added to your calendar",
      );
    });
  }
  // Course analyses load on demand; a rebuild waits for the season's.
  function whenLoaded(sid) {
    return new Promise(function (resolve) {
      var tries = 0;
      (function check() {
        loadIndex();
        var done =
          index &&
          seasonExams(sid).every(function (e) {
            return analysis(C.courseLabel(e.course), sid) !== undefined;
          });
        if (done || ++tries > 150) resolve(Boolean(done));
        else setTimeout(check, 100);
      })();
    });
  }
  // Called by the calendar after you delete, move or edit a planned
  // session: the rest of that season's plan is rebuilt around the change,
  // and a deleted session's work goes back into the schedule.
  function replan(sid, what, quiet) {
    if (!sid || !SEASONS.some(function (x) { return x.id === sid; }))
      return Promise.resolve(false);
    return whenLoaded(sid).then(function (ok) {
      if (!ok) return false;
      var pv = buildSchedule(sid);
      applySchedule(sid, pv);
      ui.preview = null;
      return C.persist().then(function () {
        C.renderAll();
        if (quiet) return true;
        C.toast(
          (what ? what + " · " : "") +
            "study plan updated" +
            (pv.short > 0 ? ", but not everything fits before the exam" : ""),
        );
        return true;
      });
    });
  }
  function deleteAll() {
    var n = C.items.filter(function (i) {
      return i.planSource === "study-plan";
    }).length;
    if (!n) return;
    if (
      !window.confirm(
        "Delete all " +
          n +
          " study plan session" +
          (n === 1 ? "" : "s") +
          " from your calendar, past and upcoming, for every exam season? Your readiness marks stay.",
      )
    )
      return;
    for (var i = C.items.length - 1; i >= 0; i--)
      if (C.items[i].planSource === "study-plan") C.items.splice(i, 1);
    ui.preview = null;
    C.persist().then(function () {
      C.renderAll();
      C.toast("Study plan deleted");
    });
  }
  // Delete every study session, past and upcoming, then build a fresh plan
  // for the season from today and save it.
  function startOver(sid) {
    sid = sid || season();
    var n = C.items.filter(function (i) {
      return i.planSource === "study-plan";
    }).length;
    if (
      !window.confirm(
        "Delete all " +
          n +
          " study session" +
          (n === 1 ? "" : "s") +
          " (including ones you moved, edited or ticked off) and build a fresh " +
          seasonInfo(sid).noun.toLowerCase() +
          " plan from today?",
      )
    )
      return Promise.resolve(false);
    for (var i = C.items.length - 1; i >= 0; i--)
      if (C.items[i].planSource === "study-plan") C.items.splice(i, 1);
    ui.preview = null;
    return whenLoaded(sid).then(function () {
      var pv = buildSchedule(sid);
      applySchedule(sid, pv);
      return C.persist().then(function () {
        C.renderAll();
        C.toast(
          pv.placed.length
            ? "Fresh plan: " +
                pv.placed.length +
                " session" +
                (pv.placed.length === 1 ? "" : "s") +
                (pv.short > 0 ? ", but not everything fits" : "")
            : "Study plan deleted. Add exam dates to build a new one.",
        );
        return true;
      });
    });
  }
  function clearPlanned() {
    var sid = season(),
      n = removePlanned(sid);
    if (!n) return;
    C.persist().then(function () {
      C.renderAll();
      C.toast(n + " planned session" + (n === 1 ? "" : "s") + " removed");
    });
  }

  // ── Rendering ─────────────────────────────────────────────────────────
  function esc(v) {
    return C.esc(v);
  }
  function examLabel(e) {
    return (
      C.prettyDate(e.date).replace(/, \d{4}$/, "") +
      (e.start ? " · " + C.timeLabel(e.start) : "")
    );
  }
  function bar(pct, cls) {
    return (
      '<span class="sp-bar' +
      (cls ? " " + cls : "") +
      '"><span style="width:' +
      Math.max(0, Math.min(100, pct)) +
      '%"></span></span>'
    );
  }
  // Each course keeps the colour the calendar gives it.
  function hue(course) {
    var h = C.courseHue ? C.courseHue(course) : 262;
    return ' style="--h:' + (isFinite(h) ? h : 262) + '"';
  }
  function ring(pct, label, cls) {
    var p = Math.max(0, Math.min(100, Math.round(pct)));
    return (
      '<span class="sp-ring' +
      (cls ? " " + cls : "") +
      '" style="--p:' +
      p +
      '" role="img" aria-label="' +
      p +
      '% ready"><span>' +
      (label === undefined ? p + "%" : label) +
      "</span></span>"
    );
  }
  function shortDate(k) {
    return C.prettyDate(k).replace(/, \d{4}$/, "");
  }
  var VIEWS = [
    {
      id: "plan",
      label: "My plan",
      title: "What to do next",
      sub: "Your next study sessions and the exams they lead to.",
    },
    {
      id: "exams",
      label: "Exams",
      title: "Your exams",
      sub: "Open an exam to see its chapters, topics and what to memorize.",
    },
    {
      id: "left",
      label: "What's left",
      title: "Everything still ahead",
      sub: "Every exam and deadline, in the order to start them.",
    },
    {
      id: "setup",
      label: "Setup",
      title: "Set up your plan",
      sub: "Three short steps, then the schedule is built for you.",
    },
  ];
  function headHtml(sid, view) {
    var v = VIEWS.find(function (x) {
        return x.id === view;
      }),
      st = setupState(sid),
      todo = (st.wk ? 0 : 1) + (st.fm || !st.rows.length ? 0 : 1) + (st.built ? 0 : 1);
    return (
      '<div class="sp-head"><div class="sp-head-text"><div class="sp-eyebrow">Study plan</div><h2>' +
      esc(v.title) +
      "</h2><p>" +
      esc(v.sub) +
      "</p></div>" +
      (view === "left"
        ? ""
        : '<div class="sp-for"><span class="sp-wk-label">Planning for</span><div class="sp-season" role="group" aria-label="Exam season">' +
          SEASONS.filter(function (x) {
            return x.id !== "remaining";
          })
            .map(function (x) {
              return (
                '<button type="button" data-sp-season="' +
                x.id +
                '" aria-pressed="' +
                (x.id === sid) +
                '">' +
                x.label +
                "</button>"
              );
            })
            .join("") +
          "</div></div>") +
      '</div><div class="sp-tabs" role="tablist" aria-label="Study plan sections">' +
      VIEWS.map(function (x) {
        return (
          '<button type="button" role="tab" data-sp-view="' +
          x.id +
          '" aria-selected="' +
          (x.id === view) +
          '">' +
          esc(x.label) +
          (x.id === "setup" && todo
            ? '<span class="sp-tab-count" aria-label="' +
              todo +
              ' steps left">' +
              todo +
              "</span>"
            : "") +
          "</button>"
        );
      }).join("") +
      "</div>"
    );
  }
  // The next exam up close, then every exam of the season on one track.
  function heroHtml(sid) {
    var ex = seasonExams(sid),
      noun = seasonInfo(sid).noun;
    if (!ex.length) return "";
    var next = ex[0],
      nc = C.courseLabel(next.course),
      a = analysis(nc, sid),
      prog = a ? courseProgress(nc, a, next) : null,
      d = daysUntil(next.date),
      today = C.todayKey(),
      last = ex[ex.length - 1].date,
      span = Math.max(7, daysUntil(last)),
      planned = plannedItems(sid).filter(function (i) {
        return i.linkedExamId === next.id;
      }).length;
    // Labels go above and below the track, and further out when exams sit
    // too close together to share a row.
    var lastIn = [-100, -100, -100, -100],
      marks = ex
        .map(function (e) {
          var c = C.courseLabel(e.course),
            left = Math.min(100, Math.max(0, (daysUntil(e.date) / span) * 100)),
            lane = 0;
          while (lane < 3 && left - lastIn[lane] < 16) lane++;
          lastIn[lane] = left;
          return (
            '<div class="sp-tl-mark lane' +
            lane +
            (left > 86 ? " end" : "") +
            '" style="left:' +
            left +
            "%;--h:" +
            (C.courseHue ? C.courseHue(c) : 262) +
            '"><span class="sp-tl-dot"></span><span class="sp-tl-label"><b>' +
            esc(c) +
            "</b>" +
            esc(shortDate(e.date)) +
            "</span></div>"
          );
        })
        .join("");
    return (
      '<div class="sp-hero"' +
      hue(nc) +
      '><div class="sp-next"><div class="sp-eyebrow">Next ' +
      esc(noun.toLowerCase()) +
      '</div><div class="sp-next-main"><div><div class="sp-next-course">' +
      esc(nc) +
      '</div><div class="sp-next-when">' +
      esc(examLabel(next)) +
      (next.location ? " · " + esc(next.location) : "") +
      '</div></div><div class="sp-countdown"><b>' +
      d +
      "</b><span>" +
      (d === 0 ? "today" : d === 1 ? "day left" : "days left") +
      "</span></div></div>" +
      '<div class="sp-next-foot">' +
      (prog
        ? ring(prog.ready) +
          "<div><b>" +
          hours(prog.work) +
          "</b> of study left<br><span>" +
          (planned
            ? planned + " sessions on your calendar"
            : "No sessions planned yet") +
          "</span></div>"
        : "<div><span>No slide analysis for this course yet</span></div>") +
      "</div></div>" +
      '<div class="sp-timeline"><div class="sp-eyebrow">' +
      esc(seasonInfo(sid).label) +
      " ahead</div>" +
      '<div class="sp-tl"><div class="sp-tl-track"></div><div class="sp-tl-today"><span>Today</span></div>' +
      marks +
      '</div><div class="sp-tl-ends"><span>' +
      esc(shortDate(today)) +
      "</span><span>" +
      esc(shortDate(last)) +
      "</span></div></div></div>"
    );
  }
  function examCardsHtml(sid, courses) {
    var noun = seasonInfo(sid).noun;
    if (!courses.length)
      return '<div class="sp-empty">Add your classes on the calendar first. The plan uses your registered courses.</div>';
    return (
      '<div class="sp-rail" role="list">' +
      courses
        .map(function (course) {
          var exam = examFor(course, sid),
            past = exam ? null : pastExamFor(course, sid),
            marked = !exam && !past && markedDone(course, sid),
            a = analysis(course, sid),
            sel = course === ui.course,
            prog = exam && a ? courseProgress(course, a, exam) : null,
            body,
            lead;
          if (past || marked) {
            lead = ring(100, "", "done");
            body =
              '<div class="sp-card-when">' +
              (past ? esc(examLabel(past)) : "") +
              '</div><div class="sp-tag done">' +
              esc(noun) +
              " done</div>" +
              (marked
                ? '<button class="sp-link-btn" type="button" data-sp-undone="' +
                  esc(course) +
                  '">Undo</button>'
                : "");
          } else if (!exam) {
            lead = ring(0, "?", "missing");
            body =
              '<div class="sp-card-when muted">No ' +
              noun.toLowerCase() +
              ' date yet</div><div class="sp-card-actions"><button class="sp-chip-btn" type="button" data-sp-add-exam="' +
              esc(course) +
              '">Add date</button><button class="sp-link-btn" type="button" data-sp-done="' +
              esc(course) +
              '">Already done</button></div>';
          } else {
            var d = daysUntil(exam.date);
            lead = prog ? ring(prog.ready) : ring(0, "–", "missing");
            body =
              '<div class="sp-card-when">' +
              esc(examLabel(exam)) +
              '</div><div class="sp-card-meta"><span class="sp-days' +
              (d <= 7 ? " soon" : "") +
              '">' +
              d +
              "d</span>" +
              (prog
                ? hours(prog.work) + " to go"
                : a === undefined
                  ? "Loading..."
                  : "No analysis yet") +
              "</div>" +
              (function () {
                var f = formatFor(course, exam, sid);
                return f && (f.types || []).length
                  ? '<div class="sp-card-format">' +
                      esc(formatSummary(f, true)) +
                      "</div>"
                  : '<div class="sp-card-format unset">Format not set</div>';
              })();
          }
          return (
            '<div class="sp-course-card' +
            (sel ? " selected" : "") +
            (past || marked ? " done" : "") +
            '" role="listitem"' +
            hue(course) +
            '><div class="sp-course-card-hit" role="button" tabindex="0" data-sp-course="' +
            esc(course) +
            '" aria-pressed="' +
            sel +
            '" aria-label="Show ' +
            esc(course) +
            '"></div>' +
            lead +
            '<div class="sp-card-body"><div class="sp-card-code">' +
            esc(course) +
            "</div>" +
            body +
            "</div></div>"
          );
        })
        .join("") +
      "</div>"
    );
  }
  // Two exams within a day of each other get flagged.
  function clashHtml(sid) {
    var ex = seasonExams(sid),
      out = [];
    for (var i = 1; i < ex.length; i++) {
      var gap = Math.round(
        (C.fromKey(ex[i].date) - C.fromKey(ex[i - 1].date)) / 86400000,
      );
      if (gap <= 1)
        out.push(
          esc(C.courseLabel(ex[i - 1].course)) +
            " and " +
            esc(C.courseLabel(ex[i].course)) +
            (gap ? " are on back-to-back days" : " are on the same day"),
        );
    }
    return out.length
      ? '<div class="sp-note warn">' +
          out.join(". ") +
          ". The day before the first one goes to its final review, so the second one's final review comes after the first exam ends.</div>"
      : "";
  }
  // Weekdays you have an in-person class, for ticking the right days at first.
  function classDays() {
    var seen = {};
    C.classes.forEach(function (c) {
      if (c.onlineOnly) return;
      (c.days || []).forEach(function (d) {
        seen[d] = true;
      });
    });
    return UNI_DAYS.filter(function (d) {
      return seen[d];
    });
  }
  // plan.uni stays one entry per weekday; the panel shows the times most
  // days share, and "Repeats every" is the days using them.
  function uniUsual() {
    var all = plan().uni || {},
      groups = {};
    UNI_DAYS.forEach(function (d) {
      var t = all[d];
      if (!t) return;
      var key = (t.leave || "") + "|" + (t.back || "");
      (groups[key] = groups[key] || []).push(d);
    });
    var keys = Object.keys(groups);
    if (!keys.length) {
      if (ui.uniDraft) return ui.uniDraft;
      var known = classDays();
      return {
        leave: "",
        back: "",
        days: known.length ? known : UNI_DAYS.slice(0, 5),
      };
    }
    function full(k) {
      return k.charAt(0) !== "|" && k.charAt(k.length - 1) !== "|" ? 1 : 0;
    }
    keys.sort(function (x, y) {
      return groups[y].length - groups[x].length || full(y) - full(x);
    });
    var parts = keys[0].split("|");
    return { leave: parts[0], back: parts[1], days: groups[keys[0]] };
  }
  function dayShort(d) {
    return d.charAt(0).toUpperCase() + d.slice(1, 3);
  }
  function uniSummary() {
    var u = uniUsual(),
      all = plan().uni || {},
      saved = UNI_DAYS.filter(function (d) {
        return all[d] && (all[d].leave || all[d].back);
      });
    if (!saved.length) return "";
    var extra = saved.length - u.days.length,
      times = [u.leave, u.back].filter(Boolean).map(C.timeLabel).join(" to ");
    return (
      u.days.map(dayShort).join(", ") +
      (times ? " · " + times : "") +
      (extra ? " · " + extra + " different" : "")
    );
  }
  function uniTimesHtml() {
    var all = plan().uni || {},
      u = uniUsual();
    return (
      '<div class="sp-uni"><div class="sp-wk-q"><span class="sp-wk-label">Drive each way</span><label class="sp-commute"><input type="number" min="0" max="240" step="5" data-sp-commute value="' +
      commute() +
      '" aria-label="Minutes of driving each way" /><span>minutes</span></label></div><div class="sp-uni-usual"><label>Leave home<input type="time" data-sp-uni-usual="leave" value="' +
      esc(u.leave) +
      '" /></label><label>Leave uni<input type="time" data-sp-uni-usual="back" value="' +
      esc(u.back) +
      '" /></label></div><div class="sp-wk-q"><span class="sp-wk-label" id="sp-uni-repeat-label">Days you go in</span><div class="sp-block-days" role="group" aria-labelledby="sp-uni-repeat-label">' +
      UNI_DAYS.map(function (d) {
        return (
          '<label><input type="checkbox" data-sp-uni-day="' +
          d +
          '"' +
          (u.days.indexOf(d) > -1 ? " checked" : "") +
          " /><span>" +
          dayShort(d) +
          "</span></label>"
        );
      }).join("") +
      '</div></div><details class="sp-uni-except"' +
      (ui.uniExceptOpen ? " open" : "") +
      '><summary>One day is different</summary><div class="sp-uni-grid"><span></span><span>Leave home</span><span>Leave uni</span><span></span>' +
      UNI_DAYS.map(function (d) {
        var t = all[d] || {};
        return (
          "<b>" +
          dayShort(d) +
          '</b><input type="time" data-sp-uni="' +
          d +
          '" data-f="leave" value="' +
          esc(t.leave || "") +
          '" aria-label="' +
          d +
          ' leave home" /><input type="time" data-sp-uni="' +
          d +
          '" data-f="back" value="' +
          esc(t.back || "") +
          '" aria-label="' +
          d +
          ' leave uni" /><button type="button" class="sp-link-btn" data-sp-uni-clear="' +
          d +
          '"' +
          (t.leave || t.back ? "" : " hidden") +
          ">Clear</button>"
        );
      }).join("") +
      "</div></details></div>"
    );
  }
  // Refreshes the panel in place: re-rendering while a time is being typed
  // would throw away the half-entered value.
  function syncUniPanel() {
    var panel = $("study-plan-root").querySelector(".sp-uni"),
      all = plan().uni || {},
      u = uniUsual(),
      active = document.activeElement;
    if (!panel) return;
    function put(input, value) {
      if (input !== active) input.value = value;
    }
    panel.querySelectorAll("[data-sp-uni-usual]").forEach(function (x) {
      put(x, u[x.dataset.spUniUsual]);
    });
    panel.querySelectorAll("[data-sp-uni-day]").forEach(function (x) {
      x.checked = u.days.indexOf(x.dataset.spUniDay) > -1;
    });
    panel.querySelectorAll("[data-sp-uni]").forEach(function (x) {
      put(x, (all[x.dataset.spUni] || {})[x.dataset.f] || "");
    });
    panel.querySelectorAll("[data-sp-uni-clear]").forEach(function (x) {
      var t = all[x.dataset.spUniClear] || {};
      x.hidden = !(t.leave || t.back);
    });
  }
  function seasonsWithPlan() {
    return SEASONS.map(function (x) {
      return x.id;
    }).filter(function (sid) {
      return plannedItems(sid).length;
    });
  }
  // Your week changed, so every season with a plan is rebuilt around it.
  function rebuildPlans(what, quiet) {
    var list = seasonsWithPlan();
    reflowing = true;
    return list
      .reduce(function (chain, sid, n) {
        return chain.then(function () {
          return replan(sid, what, quiet || n < list.length - 1);
        });
      }, Promise.resolve())
      .then(
        function () {
          reflowing = false;
        },
        function () {
          reflowing = false;
        },
      );
  }
  function refreshAfterUni(what) {
    if (seasonsWithPlan().length) return rebuildPlans(what || "Uni times changed");
    if (ui.preview) ui.preview = buildSchedule(season());
    render();
    return Promise.resolve();
  }
  function planSnapshot() {
    return JSON.parse(
      JSON.stringify(
        C.items.filter(function (i) {
          return i.planSource === "study-plan";
        }),
      ),
    );
  }
  function restorePlan(before) {
    for (var n = C.items.length - 1; n >= 0; n--)
      if (C.items[n].planSource === "study-plan") C.items.splice(n, 1);
    before.forEach(function (i) {
      C.items.push(i);
    });
  }
  // Back to no uni days or times of your own, with an Undo for a slip.
  function resetUni() {
    var p = plan(),
      fields = ["uni", "commute", "uniHome"],
      saved = {},
      before = planSnapshot(),
      any = false;
    fields.forEach(function (f) {
      if (p[f] === undefined) return;
      saved[f] = JSON.parse(JSON.stringify(p[f]));
      if (f !== "uni" || Object.keys(p.uni).length) any = true;
    });
    if (!any && !ui.uniDraft) {
      C.toast("Nothing to reset");
      return;
    }
    ui.uniDraft = null;
    ui.uniDirty = false;
    ui.uniExceptOpen = false;
    updatePlan(
      function (x) {
        fields.forEach(function (f) {
          delete x[f];
        });
      },
      true,
      true,
    );
    rebuildPlans("Uni days reset", true).then(function () {
      if (ui.preview) ui.preview = buildSchedule(season());
      render();
      C.toastUndo("Uni days reset", function () {
        updatePlan(
          function (x) {
            Object.assign(x, saved);
          },
          true,
          true,
        );
        restorePlan(before);
        C.persist().then(C.renderAll);
      });
    });
  }
  var WEEK = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  function blockLabel(x) {
    var when = x.date
        ? shortDate(x.date)
        : x.days.length === 7
          ? "Every day"
          : x.days
              .map(function (d) {
                return WEEK[d];
              })
              .join(", "),
      time =
        x.start && x.end ? C.timeRange(x.start, x.end) : "All day";
    return when + " · " + time + (x.label ? " · " + x.label : "");
  }
  function blockedHtml() {
    var list = blocks();
    return (
      '<div class="sp-blocked">' +
      (list.length
        ? '<ul class="sp-block-list">' +
          list
            .map(function (x) {
              return (
                '<li class="sp-block-row"><span class="sp-block-tag">' +
                (x.date ? "Once" : "Weekly") +
                "</span><span>" +
                esc(blockLabel(x)) +
                '</span><button type="button" class="sp-link-btn" data-sp-block-remove="' +
                esc(x.id) +
                '">Remove</button></li>'
              );
            })
            .join("") +
          "</ul>"
        : "") +
      '<form class="sp-block-form" data-sp-block-form><div class="sp-seg" role="radiogroup" aria-label="How often"><label><input type="radio" name="when" value="week" checked /><span>Every week</span></label><label><input type="radio" name="when" value="date" /><span>One date only</span></label></div><div class="sp-when-week"><span class="sp-wk-label">Which days</span><div class="sp-block-days" role="group" aria-label="Weekdays">' +
      WEEK.map(function (d, i) {
        return (
          '<label><input type="checkbox" name="day" value="' +
          i +
          '" /><span>' +
          d +
          "</span></label>"
        );
      }).join("") +
      '</div></div><label class="sp-when-date"><span class="sp-wk-label">Date</span><input type="date" name="date" /></label><div class="sp-seg" role="radiogroup" aria-label="How long"><label><input type="radio" name="span" value="times" checked /><span>Set times</span></label><label><input type="radio" name="span" value="all" /><span>Whole day</span></label></div><div class="sp-block-fields"><label class="sp-span-time">From<input type="time" name="start" /></label><label class="sp-span-time">To<input type="time" name="end" /></label><label class="sp-block-note">What is it?<input type="text" name="label" maxlength="40" placeholder="Optional, e.g. Grandma" /></label><button class="btn" type="submit">Add</button></div></form></div>'
    );
  }
  // Saving a change to your unavailable times rebuilds the plan around them.
  function saveBlocks(mutate, what) {
    var sid = season();
    updatePlan(mutate, true);
    if (seasonsWithPlan().length) rebuildPlans(what);
    else if (ui.preview) {
      ui.preview = buildSchedule(sid);
      render();
    }
  }
  function addBlock(form) {
    var f = new FormData(form),
      weekly = f.get("when") !== "date",
      wholeDay = f.get("span") === "all",
      days = weekly ? f.getAll("day").map(Number) : [],
      date = weekly ? "" : f.get("date") || "",
      start = wholeDay ? "" : f.get("start") || "",
      end = wholeDay ? "" : f.get("end") || "",
      label = String(f.get("label") || "").trim();
    if (weekly ? !days.length : !date) {
      C.toast(weekly ? "Pick at least one day" : "Pick the date");
      return;
    }
    if (!wholeDay && !start && !end) {
      C.toast("Add the times, or choose Whole day");
      return;
    }
    if (Boolean(start) !== Boolean(end)) {
      C.toast("Add both a start and an end time");
      return;
    }
    if (start && end <= start) {
      C.toast("End time must be after start time");
      return;
    }
    var x = { id: C.uid(), start: start, end: end, label: label };
    if (date) x.date = date;
    else x.days = days.sort();
    form.reset();
    saveBlocks(function (p) {
      p.blocked = (Array.isArray(p.blocked) ? p.blocked : []).concat([x]);
    }, "Unavailable time added");
  }
  // typing: a time field is still being edited, so save without re-rendering.
  function saveUni(days, patch, typing, what) {
    updatePlan(
      function (p) {
        p.uni = p.uni || {};
        [].concat(days).forEach(function (day) {
          var t = Object.assign({}, p.uni[day], patch);
          Object.keys(t).forEach(function (k) {
            if (!t[k]) delete t[k];
          });
          if (Object.keys(t).length) p.uni[day] = t;
          else delete p.uni[day];
        });
      },
      !typing,
      Boolean(typing),
    );
    if (typing) {
      ui.uniDirty = true;
      syncUniPanel();
      return Promise.resolve();
    }
    return refreshAfterUni(what);
  }
  function setUniDay(day, on) {
    var u = uniUsual(),
      hasTimes = Boolean(u.leave || u.back),
      saving = Promise.resolve();
    if (on) {
      saving = saveUni(day, hasTimes ? { leave: u.leave, back: u.back, active: true } : { active: true }, false, "Uni days changed");
    } else {
      saving = saveUni(day, { leave: "", back: "", active: "" }, false, "Uni days changed");
    }
    saving.then(function () {
      var box = $("study-plan-root").querySelector('[data-sp-uni-day="' + day + '"]');
      if (box) box.focus();
    });
  }
  function setUniUsual(field, value) {
    var u = uniUsual(),
      patch = {};
    patch[field] = value;
    if (u.days.length) return saveUni(u.days, patch, true);
    ui.uniDraft = Object.assign({}, u, patch);
    syncUniPanel();
  }
  function planMinutes(pv) {
    return pv.placed.reduce(function (m, p) {
      return m + p.minutes;
    }, 0);
  }
  function plannerHtml(sid, ready) {
    var ex = seasonExams(sid),
      limits = studyLimits(),
      ratings = readinessProgress(sid),
      noun = seasonInfo(sid).noun.toLowerCase(),
      planned = plannedItems(sid),
      pv = ui.preview,
      out =
        '<div class="sp-planner">';
    if (!ex.length)
      return (
        out +
        '<div class="empty">No upcoming ' +
        noun +
        "s on your calendar. Add the dates and the plan will fill your free time before each one.</div></div>"
      );
    if (planned.length && !pv) {
      var next = planned.slice().sort(function (x, y) {
        return (x.date + x.start).localeCompare(y.date + y.start);
      })[0];
      out +=
        '<div class="sp-built"><h4>' +
        planned.length +
        " session" +
        (planned.length === 1 ? "" : "s") +
        ' on your calendar</h4><p class="sp-muted">Next: <b>' +
        esc(next.title) +
        "</b></p><p class=\"sp-muted\">" +
        esc(shortDate(next.date)) +
        (next.start ? " · " + esc(C.timeLabel(next.start)) : "") +
        '</p><div class="sp-actions"><button class="btn solid" type="button" data-sp-build' + (ratings.done ? '' : ' disabled') + '>Re-plan</button><button class="btn muted" type="button" data-sp-clear>Remove upcoming sessions</button><button class="btn muted" type="button" data-sp-start-over>Start over</button><button class="btn muted sp-danger" type="button" data-sp-delete-all>Delete entire study plan</button></div>' + (ratings.done ? '' : '<p class="sp-note">Rate every in-scope topic before rebuilding (' + ratings.marked + ' of ' + ratings.total + ' rated).</p>') + '<div class="sp-hint">Move, edit or delete any session on the calendar and the rest of the plan rebuilds around it.</div></div>';
    } else if (!pv)
      out +=
        '<div class="sp-build-start"><h4>Ready to build your schedule</h4><p class="sp-muted">Study sessions go into your free time before each exam, around your classes, events and the drive.</p><p class="sp-note">Rate every in-scope chapter or topic as New, Shaky, or Solid first (' + ratings.marked + ' of ' + ratings.total + ' rated). The estimate updates as you rate topics.</p><p class="sp-note"><b>Estimated minimum: ' + hours(recommendedMinutes(sid)) + '</b> to cover the analyzed exam scope at your current readiness levels. This is a planning estimate, not a guaranteed 40/40.</p><ul class="sp-build-list">' +
        ex
          .map(function (e) {
            return (
              "<li" +
              hue(C.courseLabel(e.course)) +
              "><b>" +
              esc(C.courseLabel(e.course)) +
              "</b><span>" +
              esc(examLabel(e)) +
              "</span></li>"
            );
          })
          .join("") +
        '</ul><button class="btn solid sp-build-go" type="button" data-sp-build' +
        (ready && ratings.done ? "" : " disabled") +
        ">Build my schedule</button></div>";
    if (pv) {
      out += '<div class="sp-preview">';
      if (pv.skipped.length)
        out +=
          '<div class="sp-note">No slide analysis for ' +
          esc(pv.skipped.join(", ")) +
          ", so those exams aren't scheduled.</div>";
      out +=
        '<div class="sp-job-list">' +
        pv.jobs
          .map(function (j) {
            return (
              '<div class="sp-job"><b>' +
              esc(j.course) +
              "</b><span>" +
              hours(j.need) +
              " planned before " +
              esc(examLabel(j.exam)) +
              "</span>" +
              (j.left > 0
                ? '<span class="sp-warn">' +
                  hours(j.left) +
                  " doesn't fit</span>"
                : '<span class="sp-ok">fits</span>') +
              "</div>"
            );
          })
          .join("") +
        "</div>";
      out +=
        '<div class="sp-note' +
        (pv.short ? " warn" : "") +
        '">' +
        (pv.short
          ? (planMinutes(pv) >= pv.short
              ? "Most of this plan fits. About "
              : "Less than half of this plan fits. About ") +
            hours(pv.jobs.reduce(function (total, job) { return total + (Number(job.left) || 0); }, 0)) +
            " of study is still unscheduled before the exams at your " +
            limits.daily + " h/day" + (limits.weekly ? " and " + limits.weekly + " h/week" : "") +
            " limits. Increase either limit to see whether the remaining work fits, or mark chapters you already know as Solid."
          : "Busiest day needs " +
            hours(
              pv.placed.reduce(function (m, p) {
                var t = 0;
                pv.placed.forEach(function (q) {
                  if (q.date === p.date) t += q.minutes;
                });
                return Math.max(m, t);
              }, 0),
            ) +
            " of study" +
            (pv.cap > START_CAP
              ? " (the plan had to go above 4 h a day to fit everything)"
              : "") +
            ".") +
        "</div>";
      var byDay = {};
      pv.placed.forEach(function (p) {
        (byDay[p.date] || (byDay[p.date] = [])).push(p);
      });
      out +=
        '<div class="sp-days">' +
        Object.keys(byDay)
          .map(function (d) {
            var list = byDay[d],
              total = list.reduce(function (m, p) {
                return m + p.minutes;
              }, 0);
            return (
              '<div class="sp-day"><div class="sp-day-head"><b>' +
              esc(C.prettyDate(d).replace(/, \d{4}$/, "")) +
              "</b><span>" +
              hours(total) +
              "</span></div>" +
              (function () {
                var trip = uniTrip(d);
                return trip
                  ? '<div class="sp-day-campus">Leave home ' +
                      esc(C.timeLabel(C.toTime(trip.leave))) +
                      " · leave uni " +
                      esc(C.timeLabel(C.toTime(trip.back))) +
                      (trip.drive
                        ? " · home " + esc(C.timeLabel(C.toTime(trip.home)))
                        : "") +
                      "</div>"
                  : "";
              })() +
              list
                .map(function (p) {
                  return (
                    '<div class="sp-sess ' +
                    p.kind +
                    '"><span class="sp-sess-time">' +
                    esc(C.timeLabel(p.start)) +
                    "</span><span>" +
                    esc(p.title) +
                    "</span></div>"
                  );
                })
                .join("") +
              "</div>"
            );
          })
          .join("") +
        "</div>";
      out +=
        '<div class="sp-actions sp-commit"><button class="btn solid" type="button" data-sp-commit' +
        (pv.placed.length ? "" : " disabled") +
        ">Add " +
        pv.placed.length +
        " session" +
        (pv.placed.length === 1 ? "" : "s") +
        " to calendar</button>" +
        '<button class="btn muted" type="button" data-sp-discard>Discard</button>' +
        (planned.length
          ? '<span class="sp-muted">Replaces the ' +
            planned.length +
            " planned session" +
            (planned.length === 1 ? "" : "s") +
            " from today on.</span>"
          : "") +
        "</div></div>";
    }
    return out + "</div>";
  }
  function needsHtml(course, a) {
    var n = C.finalNeeds(course),
      w = (a && a.syllabus && a.syllabus.final_weight) || n.fw;
    if (!n.entered)
      return (
        '<div class="sp-box"><h3>Finishing the course safely</h3><p class="sp-muted">Final is worth ' +
        esc(w) +
        "% of the grade. Add your quiz, major and assignment marks under Grades &amp; GPA to see exactly what you need on the final.</p></div>"
      );
    function pct(v) {
      return Math.ceil(v) + "%";
    }
    function mark(v) {
      return String(Math.ceil(v * 10) / 10);
    }
    function cls(v) {
      return v === null
        ? ""
        : v <= 0
          ? "secured"
          : v > 100
            ? "gone"
            : v >= 85
              ? "hard"
              : v >= 70
                ? "stretch"
                : "ok";
    }
    if (n.remaining <= 0.05)
      return (
        '<div class="sp-box"><h3>Finishing the course safely</h3><p class="sp-muted">Everything in this course is graded: <b>' +
        mark(n.weighted) +
        " / 100</b>.</p></div>"
      );
    var cwLeft = Math.max(0, n.cwMax - n.cwUsed),
      reach = n.needs.filter(function (x) {
        return x.avg <= 100;
      }),
      best = reach[0] || null,
      secured = n.needs.filter(function (x) {
        return x.avg <= 0;
      })[0];
    // For each letter: the average needed on everything left, spent evenly
    // across the coursework still to come and the final.
    var rows = n.needs
      .map(function (x) {
        var r = Math.max(0, x.avg / 100),
          cwTarget = n.cwComplete ? n.cw : n.cw + r * cwLeft,
          finalTarget = n.cwComplete ? x.finalMarks : r * n.fw,
          c = cls(x.avg),
          cwCell,
          finalCell;
        if (x.avg > 100) cwCell = finalCell = "Out of reach";
        else if (x.avg <= 0) cwCell = finalCell = "Secured";
        else {
          cwCell = n.cwComplete
            ? mark(n.cw) + " / " + n.cwMax
            : "<b>" +
              mark(cwTarget) +
              " / " +
              n.cwMax +
              "</b><span>" +
              mark(r * cwLeft) +
              " more of the " +
              mark(cwLeft) +
              " left</span>";
          finalCell =
            "<b>" +
            mark(finalTarget) +
            " / " +
            n.fw +
            "</b><span>" +
            pct((finalTarget / n.fw) * 100) +
            "</span>";
        }
        return (
          '<tr class="' +
          c +
          (best && x.letter === best.letter ? " best" : "") +
          '"><th scope="row">' +
          esc(x.letter) +
          '</th><td class="' +
          c +
          '">' +
          cwCell +
          '</td><td class="' +
          c +
          '">' +
          finalCell +
          "</td></tr>"
        );
      })
      .join("");
    var summary =
      (best
        ? "Best grade still possible: <b>" + esc(best.letter) + "</b>."
        : "Even full marks on everything left won't reach a D.") +
      (secured
        ? " <b>" + esc(secured.letter) + "</b> or better is already secured."
        : "");
    return (
      '<div class="sp-box"><h3>Finishing the course safely</h3><p class="sp-muted">' +
      "Coursework is <b>" +
      n.cwMax +
      "</b> and the final <b>" +
      n.fw +
      "</b>. So far you have <b>" +
      mark(n.cw) +
      " / " +
      n.cwMax +
      "</b> from the " +
      mark(n.cwUsed) +
      " coursework points graded" +
      (n.cwComplete
        ? " (coursework complete" +
          (n.cw !== n.projected ? ", rounds to " + n.projected : "") +
          ")"
        : ", with " + mark(cwLeft) + " still to come") +
      ". " +
      summary +
      '</p><table class="sp-need-table"><thead><tr><th scope="col">Grade</th><th scope="col">Coursework total needed (out of ' +
      n.cwMax +
      ')</th><th scope="col">Final exam needed (out of ' +
      n.fw +
      ")</th></tr></thead><tbody>" +
      rows +
      '</tbody></table><p class="sp-muted">Both columns assume the same average on everything still ahead. Do better on one and you need less on the other. PSU rounds the coursework total to a whole mark before adding the final.</p></div>'
    );
  }
  // Question types you typed yourself sit beside the built-in ones. They
  // are stored by name in the same list.
  function customTypes(key, types) {
    return types
      .filter(function (t) {
        return !formatInfo(t);
      })
      .concat(ui.fmtCustom[key] || [])
      .filter(function (t, n, all) {
        return all.indexOf(t) === n;
      });
  }
  function customChipHtml(name, checked) {
    return (
      '<label class="sp-fmt-chip"><input type="checkbox" name="type" value="' +
      esc(name) +
      '"' +
      (checked ? " checked" : "") +
      "><span>" +
      esc(name) +
      "</span></label>"
    );
  }
  function addCustomType(form) {
    var input = form.querySelector("[data-sp-type-input]"),
      name = input.value.trim().replace(/\s+/g, " "),
      key = form.dataset.spFormatForm;
    if (!name) return;
    var known = [].some.call(form.querySelectorAll('input[name="type"]'), function (box) {
      var label = (formatInfo(box.value) || {}).label || box.value;
      if (label.toLowerCase() !== name.toLowerCase()) return false;
      box.checked = true;
      return true;
    });
    if (!known) {
      ui.fmtCustom[key] = (ui.fmtCustom[key] || []).concat(name);
      form
        .querySelector(".sp-fmt-chips")
        .insertAdjacentHTML("beforeend", customChipHtml(name, true));
    }
    input.value = "";
    input.focus();
  }
  function formatEditorHtml(course, a, exam, sid, f, inSetup) {
    var key = formatKeys(course, exam, sid)[0],
      noun = seasonInfo(sid).noun,
      types = (f && f.types) || [],
      base = a ? overviewScope(a, exam) : null,
      chosen = a ? examScope(a, exam).ids : [];
    return (
      '<form class="sp-fmt-form" data-sp-format-course="' +
      esc(course) +
      '" data-sp-format-form="' +
      esc(key) +
      '"><label class="sp-fmt-field wide"><span>What did your instructor say?</span><textarea name="notes" rows="2" placeholder="e.g. All problem solving and code, 5 questions, 30 minutes, closed book">' +
      esc((f && f.notes) || "") +
      '</textarea><small class="sp-fmt-detect" aria-live="polite"></small></label>' +
      '<fieldset class="sp-fmt-field wide"><legend>Question types</legend><div class="sp-fmt-chips">' +
      FORMATS.map(function (x) {
        return (
          '<label class="sp-fmt-chip"><input type="checkbox" name="type" value="' +
          x.id +
          '"' +
          (types.indexOf(x.id) > -1 ? " checked" : "") +
          "><span>" +
          esc(x.label) +
          "</span></label>"
        );
      }).join("") +
      customTypes(key, types)
        .map(function (name) {
          return customChipHtml(name, types.indexOf(name) > -1 || (ui.fmtCustom[key] || []).indexOf(name) > -1);
        })
        .join("") +
      '</div><div class="sp-fmt-addtype"><input type="text" maxlength="40" data-sp-type-input placeholder="Another question type, e.g. Case analysis" aria-label="Another question type" /><button class="sp-chip-btn" type="button" data-sp-type-add>Add type</button></div></fieldset><details class="sp-fmt-more"' +
      (f && (f.questions || f.minutes || f.book || f.topics || (f.chapters && f.chapters.length))
        ? " open"
        : "") +
      '><summary>More details (optional)</summary><div class="sp-fmt-row"><label class="sp-fmt-field"><span>Questions</span><input type="number" name="questions" min="1" max="200" placeholder="Not said" value="' +
      esc((f && f.questions) || "") +
      '"></label><label class="sp-fmt-field"><span>Minutes</span><input type="number" name="minutes" min="5" max="600" step="5" placeholder="Not said" value="' +
      esc((f && f.minutes) || "") +
      '"></label><label class="sp-fmt-field"><span>Book</span><select name="book">' +
      Object.keys(BOOK)
        .map(function (k) {
          return (
            '<option value="' +
            k +
            '"' +
            (((f && f.book) || "") === k ? " selected" : "") +
            ">" +
            BOOK[k] +
            "</option>"
          );
        })
        .join("") +
      "</select></label></div>" +
      (a
        ? '<fieldset class="sp-fmt-field wide"><legend>What it covers</legend><p class="sp-muted">' +
          (base && base.label
            ? "Set from the course overview (" + esc(base.label) + "). "
            : "") +
          "Change it only if your instructor changed what's on the " +
          noun.toLowerCase() +
          '.</p><div class="sp-fmt-chips">' +
          a.chapters
            .map(function (ch) {
              return (
                '<label class="sp-fmt-chip"><input type="checkbox" name="ch" value="' +
                esc(ch.id) +
                '"' +
                (chosen.indexOf(ch.id) > -1 ? " checked" : "") +
                "><span>" +
                esc(chapterName(ch)) +
                "</span></label>"
              );
            })
            .join("") +
          "</div></fieldset>"
        : "") +
      '<label class="sp-fmt-field wide"><span>Topics to focus on or skip (optional)</span><input name="topics" placeholder="e.g. Focus on Liskov and DIP; no Observer" value="' +
      esc((f && f.topics) || "") +
      '"></label></details><div class="sp-fmt-actions"><button class="btn solid" type="submit">' +
      (inSetup ? "Save and next" : "Save format") +
      "</button>" +
      (f && !inSetup
        ? '<button class="btn" type="button" data-sp-fmt-cancel="' +
          esc(key) +
          '">Cancel</button>'
        : "") +
      (f
        ? '<button class="sp-link-btn" type="button" data-sp-fmt-course="' +
          esc(course) +
          '" data-sp-fmt-remove="' +
          esc(key) +
          '">Remove format</button>'
        : "") +
      "</div></form>"
    );
  }
  function formatHtml(course, a, exam, sid) {
    var f = formatFor(course, exam, sid),
      noun = seasonInfo(sid).noun,
      key = formatKeys(course, exam, sid)[0],
      editing = !f || ui.fmtEdit[key],
      sc = a ? examScope(a, exam) : null;
    var head =
      '<div class="sp-box-head"><div><div class="sp-eyebrow">Exam format</div><h3>' +
      (f && !editing
        ? esc(formatSummary(f)) || "Format saved"
        : "How will the " + esc(noun.toLowerCase()) + " ask?") +
      "</h3>" +
      (f && !editing
        ? '<p class="sp-muted">Updated ' +
          esc(shortDate(f.updated || C.todayKey())) +
          (sc && sc.custom ? " · covers your updated chapters" : "") +
          "</p>"
        : '<p class="sp-muted">Note what your instructor said.</p>') +
      "</div>" +
      (f && !editing
        ? '<button class="sp-chip-btn" type="button" data-sp-fmt-edit="' +
          esc(key) +
          '">Update format</button>'
        : "") +
      "</div>";
    if (editing)
      return (
        '<section class="sp-box sp-fmt' +
        (f ? "" : " unset") +
        '">' +
        head +
        formatEditorHtml(course, a, exam, sid, f) +
        "</section>"
      );
    var said =
      (f.notes
        ? '<blockquote class="sp-fmt-quote">' + esc(f.notes) + "</blockquote>"
        : "") +
      (f.topics
        ? '<p class="sp-fmt-topics"><b>Focus:</b> ' + esc(f.topics) + "</p>"
        : "") +
      (sc && sc.custom
        ? '<p class="sp-fmt-topics"><b>Covers:</b> ' +
          esc(
            a.chapters
              .filter(function (ch) {
                return sc.ids.indexOf(ch.id) > -1;
              })
              .map(chapterName)
              .join(", "),
          ) +
          "</p>"
        : "");
    var pace =
      f.minutes && f.questions
        ? '<div class="sp-note">About <b>' +
          Math.max(1, Math.round(f.minutes / f.questions)) +
          " min per question</b>.</div>"
        : "";
    var history = (f.history || []).length
      ? '<details class="sp-fmt-history"><summary>Earlier versions (' +
        f.history.length +
        ")</summary><ul>" +
        f.history
          .map(function (h) {
            return (
              "<li><b>" +
              esc(shortDate(h.at)) +
              "</b> " +
              esc(h.summary) +
              "</li>"
            );
          })
          .join("") +
        "</ul></details>"
      : "";
    return (
      '<section class="sp-box sp-fmt">' +
      head +
      said +
      pace +
      history +
      "</section>"
    );
  }
  function itemById(a, id) {
    return a.items.find(function (i) {
      return i.id === id;
    });
  }
  function levelButtons(unit, lv, course) {
    return (
      '<span class="sp-level" role="group" aria-label="Readiness">' +
      LEVELS.map(function (l, n) {
        return (
          '<button type="button" data-sp-level="' +
          n +
          '" data-sp-unit="' +
          esc(unit) +
          '" data-sp-ready-course="' +
          esc(course || ui.course) +
          '" aria-pressed="' +
          (lv === n) +
          '" class="l' +
          n +
          '">' +
          l +
          "</button>"
        );
      }).join("") +
      "</span>"
    );
  }
  // Counts for the chapters the selected exam covers.
  function statsHtml(a, exam, sid) {
    var sc = examScope(a, exam),
      chs = a.chapters.filter(function (ch) {
        return sc.ids.indexOf(ch.id) > -1;
      }),
      its = (a.items || []).filter(function (i) {
        return sc.ids.indexOf(i.chapter) > -1;
      }),
      k = {},
      t = { slides: 0, minutes: 0 };
    chs.forEach(function (ch) {
      t.slides += ch.slides;
      t.minutes += ch.minutes;
    });
    its.forEach(function (i) {
      k[i.kind] = (k[i.kind] || 0) + 1;
    });
    var noun = seasonInfo(sid).noun,
      wre = { quiz: /quiz/i, midterm: /mid|major/i, final: /final/i }[sid],
      w = ((a.syllabus && a.syllabus.weights) || []).find(function (x) {
        return wre.test(x.label);
      }),
      tiles = [
        ["Slides", t.slides],
        ["Chapters", chs.length],
        ["Study time", hours(t.minutes)],
      ];
    if (a.curated)
      tiles = tiles.concat([
        ["Topics", its.length],
        ["Formulas", k.formula],
        ["Key numbers", k.number],
        ["Lists", k.list],
        ["Problem types", k.calc],
        ["Comparisons", k.compare],
        ["Processes", k.process],
      ]);
    if (w)
      tiles.push([sid === "final" ? "Final weight" : w.label, w.percent + "%"]);
    else if (sid === "final" && a.syllabus && a.syllabus.final_weight)
      tiles.push(["Final weight", a.syllabus.final_weight + "%"]);
    return (
      '<section class="sp-box"><h3>At a glance</h3><p class="sp-muted">' +
      (chs.length < a.chapters.length
        ? "For " +
          esc(sc.label ? sc.label.split(/ [—-] /)[0] : noun) +
          ": " +
          esc(
            chs
              .map(function (ch) {
                return chapterName(ch).split(" ").slice(0, 2).join(" ");
              })
              .filter(function (n, i, all) {
                return all.indexOf(n) === i;
              })
              .join(", "),
          ) +
          " (" +
          chs.length +
          " of " +
          a.chapters.length +
          " chapters)."
        : "For the " + esc(noun.toLowerCase()) + ": every chapter.") +
      '</p><div class="sp-stats">' +
      tiles
        .filter(function (x) {
          return x[1] !== undefined && x[1] !== 0;
        })
        .map(function (x) {
          return (
            '<div class="sp-stat"><b>' +
            esc(x[1]) +
            "</b><span>" +
            esc(x[0]) +
            "</span></div>"
          );
        })
        .join("") +
      "</div></section>"
    );
  }
  function repeatedHtml(a) {
    if (!a.curated || !a.repeated || !a.repeated.length) return "";
    var list = a.repeated
        .map(function (id) {
          return itemById(a, id);
        })
        .filter(Boolean),
      max = list[0] ? list[0].slides : 1;
    return (
      '<section class="sp-box"><h3>Most repeated</h3><p class="sp-muted">Slides that come back to each topic. The more it repeats, the safer a bet it is.</p><ol class="sp-rep">' +
      list
        .map(function (i, n) {
          return (
            '<li><span class="sp-rep-rank">' +
            (n + 1) +
            '</span><span class="sp-rep-name">' +
            esc(i.name) +
            '<span class="sp-rep-bar"><span style="width:' +
            Math.max(6, (i.slides / max) * 100) +
            '%"></span></span></span><span class="sp-rep-count"><b>' +
            i.slides +
            "</b> slides<br>" +
            i.decks +
            " deck" +
            (i.decks === 1 ? "" : "s") +
            "</span></li>"
          );
        })
        .join("") +
      "</ol></section>"
    );
  }
  function memorizeHtml(course, a) {
    if (!a.curated) return "";
    var groups = ["formula", "number", "list"],
      count = a.items.filter(function (i) {
        return groups.indexOf(i.kind) > -1;
      }).length;
    if (!count) return "";
    return (
      '<section class="sp-box"><div class="sp-box-head"><div><h3>Memorize</h3><p class="sp-muted">' +
      count +
      (ui.drill
        ? " cards. Say each one out loud, then tap to check."
        : " items, word for word.") +
      '</p></div><label class="sp-switch"><input type="checkbox" data-sp-drill' +
      (ui.drill ? " checked" : "") +
      "><span></span>Drill</label></div>" +
      groups
        .map(function (g) {
          var its = a.items.filter(function (i) {
            return i.kind === g;
          });
          if (!its.length) return "";
          return (
            '<h4 class="sp-sub">' +
            esc(a.kind_labels[g]) +
            " · " +
            its.length +
            '</h4><div class="sp-mem">' +
            its
              .map(function (i) {
                var hidden = ui.drill && !ui.revealed[i.id];
                return (
                  '<button type="button" class="sp-flash' +
                  (hidden ? "" : " flipped") +
                  '" data-sp-reveal="' +
                  esc(i.id) +
                  '" aria-pressed="' +
                  !hidden +
                  '"><b>' +
                  esc(i.name) +
                  "</b><span>" +
                  (hidden ? "Tap to reveal" : esc(i.memorize)) +
                  "</span></button>"
                );
              })
              .join("") +
            "</div>"
          );
        })
        .join("") +
      "</section>"
    );
  }
  // "Slides · Slides" reads as "Slides"; other labels name the part.
  function linkLabel(l) {
    var parts = String(l.label).split(" · ");
    return parts[1] === "Slides" ? parts[0] : l.label;
  }
  function studyLinksHtml(ch) {
    return (ch.links || []).length
      ? '<div class="sp-links">' +
          ch.links
            .map(function (l) {
              return (
                '<a href="' + esc(l.url) + '">' + esc(linkLabel(l)) + "</a>"
              );
            })
            .join("") +
          "</div>"
      : "";
  }
  function chaptersHtml(course, a, exam, conceptsOnly) {
    var ids = scopeIds(a, exam);
    return (
      '<section class="sp-box"><div class="sp-box-head"><div><h3>What to study</h3><p class="sp-muted">' +
      (a.curated
        ? "Every chapter on this exam, with its slide count and pages. Open one to see its topics."
        : "Every chapter on this exam, with its slide count and pages.") +
      "</p></div></div>" +
      (function () {
        var sc = examScope(a, exam),
          outN = a.chapters.length - sc.ids.length;
        if (sc.custom)
          return (
            '<p class="sp-scope">Covers <b>' +
            sc.ids.length +
            " of " +
            a.chapters.length +
            " chapters</b>, as you updated it in Exam format" +
            (sc.label
              ? " (the course overview says " + esc(sc.label) + ")"
              : "") +
            ".</p>"
          );
        return sc.label
          ? '<p class="sp-scope"><b>' +
              esc(sc.label) +
              "</b> covers " +
              (outN
                ? sc.ids.length + " of " + a.chapters.length + " chapters"
                : "every chapter") +
              ', from the <a href="' +
              esc(a.course_page) +
              '#section-page-count-by-exam">course overview</a>.</p>'
          : "";
      })() +
      '<div class="sp-chapters">' +
      a.chapters
        .filter(function (ch) {
          return ids.indexOf(ch.id) > -1;
        })
        .map(function (ch) {
          var inScope = ids.indexOf(ch.id) > -1,
            left = chapterLeft(course, a, ch),
            ready = chapterReadiness(course, a, ch) || 0,
            its = chapterItems(a, ch.id),
            ratingItems = conceptsOnly ? its.filter(isMainPointReadinessItem) : its,
            open = ui.open[ch.id],
            parts = String(ch.title).split(" · "),
            num = parts.length > 1 ? parts[0] : "",
            name = parts.length > 1 ? parts.slice(1).join(" · ") : parts[0];
          var head =
            '<div class="sp-ch' +
            (inScope ? "" : " out") +
            (open ? " open" : "") +
            '">' +
            ring(ready, undefined, "sm") +
            '<div class="sp-ch-text">' +
            (num ? '<span class="sp-ch-num">' + esc(num) + "</span>" : "") +
            '<span class="sp-ch-title">' +
            esc(name) +
            '</span><span class="sp-ch-meta">' +
            (ch.upcoming ? "Syllabus topic · slides not provided yet" : ch.slides + " slides") +
            (its.length ? " · " + its.length + " topics" : "") +
            " · " +
            hours(left) +
            " left" +
            "</span>" +
            studyLinksHtml(ch) +
            "</div>" +
            (ch.upcoming
              ? '<span class="sp-upcoming-badge">UPCOMING · SYLLABUS</span>'
              : a.curated
              ? '<button type="button" class="sp-chev" data-sp-open="' +
                esc(ch.id) +
                '" aria-expanded="' +
                Boolean(open) +
                '" aria-label="' +
                (open ? "Hide" : "Show") +
                " topics in " +
                esc(ch.title) +
                '"></button>'
              : levelButtons("ch:" + ch.id, level(course, a, "ch:" + ch.id), course)) +
            "</div>";
          if (!a.curated || ch.upcoming) return head;
          if (!open) return head;
          return (
            head +
            '<div class="sp-items">' +
            ratingItems
              .slice()
              .sort(function (x, y) {
                return (
                  KIND_ORDER.indexOf(x.kind) - KIND_ORDER.indexOf(y.kind) ||
                  y.score - x.score
                );
              })
              .map(function (i) {
                var lv = level(course, a, i.id);
                return (
                  '<div class="sp-item l' +
                  lv +
                  '"><div class="sp-item-text"><div class="sp-item-tags"><span class="sp-tier ' +
                  i.tier +
                  '">' +
                  esc(TIER_LABEL[i.tier] || i.tier) +
                  '</span><span class="sp-kind">' +
                  esc(KIND_ONE[i.kind] || i.kind) +
                  '</span><span class="sp-item-count">' +
                  i.slides +
                  " slide" +
                  (i.slides === 1 ? "" : "s") +
                  (i.decks > 1 ? " · " + i.decks + " decks" : "") +
                  (i.practice ? " · " + i.practice + " practice" : "") +
                  '</span></div><div class="sp-item-name">' +
                  esc(i.name) +
                  "</div>" +
                  (i.memorize
                    ? '<div class="sp-item-mem">' + esc(i.memorize) + "</div>"
                    : "") +
                  "</div>" +
                  levelButtons(i.id, lv, course) +
                  "</div>"
                );
              })
              .join("") +
            "</div>"
          );
        })
        .join("") +
      "</div></section>"
    );
  }
  function styleHtml(a) {
    var parts = [];
    if (a.style && a.style.question_types)
      parts.push(
        '<section class="sp-box"><h3>How the exam asks</h3><p class="sp-muted">From ' +
          esc(a.style.source) +
          '.</p><ul class="sp-list">' +
          a.style.question_types
            .map(function (q) {
              return "<li>" + esc(q) + "</li>";
            })
            .join("") +
          "</ul></section>",
      );
    if ((a.syllabus && a.syllabus.weights) || (a.resources || []).length)
      parts.push(
        '<section class="sp-box"><h3>Grade weights and resources</h3>' +
          (a.syllabus && a.syllabus.weights
            ? '<div class="sp-weights">' +
              a.syllabus.weights
                .map(function (w) {
                  return (
                    '<div class="sp-weight"><span>' +
                    esc(w.label) +
                    '</span><span class="sp-weight-bar"><span style="width:' +
                    Math.min(100, w.percent * 2) +
                    '%"></span></span><b>' +
                    esc(w.percent) +
                    "%</b></div>"
                  );
                })
                .join("") +
              "</div>"
            : "") +
          ((a.resources || []).length
            ? '<div class="sp-links">' +
              a.resources
                .map(function (r) {
                  return (
                    '<a href="' + esc(r.url) + '">' + esc(r.label) + "</a>"
                  );
                })
                .join("") +
              "</div>"
            : "") +
          "</section>",
      );
    return parts.join("");
  }
  function courseHtml(course, sid) {
    var a = analysis(course, sid),
      exam = examFor(course, sid);
    if (a === undefined)
      return (
        '<div class="sp-empty">Loading the ' +
        esc(course) +
        " analysis...</div>"
      );
    if (a === null)
      return (
        '<div class="sp-course"' +
        hue(course) +
        '><div class="sp-course-head"><div><div class="sp-eyebrow">' +
        esc(course) +
        '</div><h3>No slide analysis yet</h3><p class="sp-muted">This course needs its slides on the site before it can be planned.</p></div></div>' +
        formatHtml(course, null, exam, sid) +
        '<div class="sp-work"><div class="sp-aside">' +
        needsHtml(course, null) +
        "</div></div></div>"
      );
    var seasonNote =
      a.season !== sid
        ? '<div class="sp-note">This uses the final-exam analysis, limited to the chapters this ' +
          seasonInfo(sid).noun.toLowerCase() +
          " covers on the course overview.</div>"
        : "";
    var syl = a.syllabus || {},
      prog = courseProgress(course, a, exam);
    return (
      '<div class="sp-course"' +
      hue(course) +
      '><div class="sp-course-head">' +
      ring(prog.ready, undefined, "lg") +
      '<div class="sp-course-title"><div class="sp-eyebrow">' +
      esc(course) +
      (exam
        ? " · " + esc(seasonInfo(sid).noun) + " " + esc(examLabel(exam))
        : "") +
      "</div><h3>" +
      esc(a.title || course) +
      '</h3><p class="sp-muted">' +
      (a.curated
        ? "Every slide deck read topic by topic: each concept, formula and problem type, counted slide by slide."
        : "Slide counts and study time only so far.") +
      (syl.scope_note && a.curated ? " " + esc(syl.scope_note) : "") +
      "</p></div>" +
      (a.course_page
        ? '<a class="sp-chip-btn" href="' +
          esc(a.course_page) +
          '">Course page</a>'
        : "") +
      "</div>" +
      seasonNote +
      formatHtml(course, a, exam, sid) +
      '<div class="sp-work"><div class="sp-main">' +
      chaptersHtml(course, a, exam) +
      memorizeHtml(course, a) +
      '</div><div class="sp-aside">' +
      statsHtml(a, exam, sid) +
      needsHtml(course, a) +
      repeatedHtml(a) +
      styleHtml(a) +
      "</div></div></div>"
    );
  }
  // ── Remaining ─────────────────────────────────────────────────────────
  function examSeason(e) {
    var t = C.canonicalExamType(e.type);
    return t === "bonus-quiz" ? "quiz" : t;
  }
  function weightFor(a, sid) {
    var re = { quiz: /quiz/i, midterm: /mid|major/i, final: /final/i }[sid],
      w = ((a && a.syllabus && a.syllabus.weights) || []).find(function (x) {
        return re.test(x.label);
      });
    return w ? w.percent : null;
  }
  // Everything still ahead: exams with the study left for them, and
  // Unsubmitted assignments, projects and presentations with estimated hours.
  // Anything dated today is 0 days away and no longer counts as ahead.
  function remainingEntries() {
    var today = C.todayKey(),
      out = [];
    C.exams.forEach(function (e) {
      if (!e.date || e.date <= today) return;
      var course = C.courseLabel(e.course),
        sid = examSeason(e),
        a = analysis(course, sid),
        prog = a ? courseProgress(course, a, e) : null,
        sc = a ? examScope(a, e) : null,
        name =
          sc && sc.label ? sc.label.split(/ [—–-] /)[0] : seasonInfo(sid).noun;
      if (/^(Final Exam|Final)$/i.test(name)) name = "Final";
      out.push({
        type: "exam",
        sid: sid,
        course: course,
        name: name,
        date: e.date,
        time: e.start || "",
        minutes: prog ? prog.work : null,
        loading: a === undefined,
        weight: a ? weightFor(a, sid) : null,
        format: formatFor(course, e, sid),
      });
    });
    C.items.forEach(function (i) {
      if (
        (i.kind !== "assignment" &&
          i.kind !== "project" &&
          i.kind !== "presentation") ||
        i.submitted ||
        !i.date ||
        i.date <= today
      )
        return;
      out.push({
        type: "due",
        course: C.courseLabel(i.course || "") || "",
        name:
          i.title ||
          (i.kind === "project"
            ? "Project"
            : i.kind === "presentation"
              ? "Presentation"
              : "Assignment"),
        kind: i.kind,
        date: i.date,
        time: i.end || i.start || "",
        minutes: (Number(i.estimatedHours) || 2) * 60,
        priority: i.priority || "",
      });
    });
    out.forEach(function (x) {
      var days = Math.max(1, Math.ceil((x.minutes || 0) / EASY_DAY));
      // An exam also needs its last day for the final review.
      x.startBy = C.addDays(x.date, -(days + (x.type === "exam" ? 1 : 0)));
      x.daysLeft = daysUntil(x.date);
      x.perDay = x.minutes ? x.minutes / Math.max(1, x.daysLeft) : 0;
    });
    return out.sort(function (p, q) {
      return p.startBy.localeCompare(q.startBy) || p.date.localeCompare(q.date);
    });
  }
  function freeMinutes(day) {
    var today = C.todayKey(),
      now = new Date(),
      start = DAY_START;
    if (day === today)
      start = Math.max(DAY_START, now.getHours() * 60 + now.getMinutes());
    return freeSlots(day, "remaining", start).reduce(function (m, sl) {
      return m + (sl[1] - sl[0]);
    }, 0);
  }
  function weekStart(k) {
    return C.addDays(k, -C.fromKey(k).getDay());
  }
  function aboutHours(min) {
    if (min < 50) return Math.max(15, Math.round(min / 15) * 15) + " min";
    return hours(min);
  }
  function entryLabel(x) {
    return x.course ? x.course + " " + x.name : x.name;
  }
  function remainingHtml() {
    var list = remainingEntries(),
      today = C.todayKey();
    if (!list.length)
      return '<div class="sp-empty">Nothing left on your calendar. Add exam dates and assignments and they\'ll show up here.</div>';
    var exams = list.filter(function (x) {
        return x.type === "exam";
      }),
      dues = list.length - exams.length,
      totalMin = list.reduce(function (m, x) {
        return m + (x.minutes || 0);
      }, 0),
      last = list.reduce(function (m, x) {
        return x.date > m ? x.date : m;
      }, today);
    // Courses still waiting on a final date.
    var noFinal = C.knownCourses().filter(function (c) {
      return (
        !markedDone(c, "final") &&
        !pastExamFor(c, "final") &&
        !exams.some(function (x) {
          return x.course === c && x.sid === "final";
        })
      );
    });
    var summary =
      '<div class="sp-rem-summary"><div><b>' +
      exams.length +
      "</b><span>exam" +
      (exams.length === 1 ? "" : "s") +
      " left</span></div><div><b>" +
      dues +
      "</b><span>deadline" +
      (dues === 1 ? "" : "s") +
      "</span></div><div><b>" +
      hours(totalMin) +
      "</b><span>of work left</span></div><div><b>" +
      esc(shortDate(last)) +
      "</b><span>last one</span></div></div>" +
      (noFinal.length
        ? '<div class="sp-note">No final date yet for ' +
          esc(noFinal.join(", ")) +
          ". Add it on the calendar so it's counted here.</div>"
        : "");

    // Focus now: whatever should already be under way.
    var soon = C.addDays(today, 2),
      focus = list.filter(function (x) {
        return x.startBy <= soon && x.minutes;
      });
    var focusHtml =
      '<section class="sp-box sp-rem-focus"><div class="sp-eyebrow">Focus now</div>' +
      (focus.length
        ? "<h3>" +
          (focus.length === 1
            ? "One thing needs your time"
            : focus.length + " things need your time") +
          ' right now</h3><ol class="sp-rem-focus-list">' +
          focus
            .slice(0, 4)
            .map(function (x) {
              return (
                "<li><b>" +
                esc(entryLabel(x)) +
                "</b><span>" +
                (x.type === "exam"
                  ? "in " + x.daysLeft + " day" + (x.daysLeft === 1 ? "" : "s")
                  : "due " + esc(shortDate(x.date))) +
                " · about " +
                esc(aboutHours(x.perDay)) +
                " a day</span></li>"
              );
            })
            .join("") +
          "</ol>" +
          (focus.length > 4
            ? '<p class="sp-muted">And ' +
              (focus.length - 4) +
              " more below.</p>"
            : "")
        : '<h3>Nothing urgent</h3><p class="sp-muted">Nothing needs starting in the next couple of days. Get ahead on the next one, or take the time off.</p>') +
      "</section>";

    // Priorities, in the order to start them.
    var rows = list
      .map(function (x) {
        var state, cls;
        if (x.loading) {
          state = "Working it out...";
          cls = "";
        } else if (!x.minutes) {
          state = x.type === "exam" && x.minutes === null ? "No slide analysis" : "";
          cls = "";
        } else if (x.startBy <= today) {
          state =
            x.perDay > 180
              ? "Behind · " + aboutHours(x.perDay) + " a day"
              : "Start now";
          cls = x.perDay > 180 ? " late" : " now";
        } else {
          state = "Start by " + shortDate(x.startBy);
          cls = x.startBy <= C.addDays(today, 7) ? " soon" : "";
        }
        var meta = [
          x.type === "exam"
            ? shortDate(x.date) + (x.time ? " · " + C.timeLabel(x.time) : "")
            : "Due " + shortDate(x.date),
        ];
        if (x.minutes)
          meta.push(
            hours(x.minutes) + (x.type === "exam" ? " to study" : " of work"),
          );
        if (x.weight) meta.push(x.weight + "% of the grade");
        if (x.format && (x.format.types || []).length)
          meta.push(formatSummary(x.format, true));
        return (
          '<li class="sp-rem-row' +
          cls +
          '"' +
          hue(x.course) +
          '><span class="sp-rem-days"><b>' +
          x.daysLeft +
          "</b>day" +
          (x.daysLeft === 1 ? "" : "s") +
          '</span><span class="sp-rem-main"><span class="sp-rem-name">' +
          esc(entryLabel(x)) +
          (x.type === "due"
            ? '<span class="sp-rem-kind">' + esc(x.kind) + "</span>"
            : "") +
          '</span><span class="sp-rem-meta">' +
          esc(meta.join(" · ")) +
          "</span></span>" +
          (state
            ? '<span class="sp-rem-state">' + esc(state) + "</span>"
            : "<span></span>") +
          (x.type === "exam"
            ? '<button type="button" class="sp-link-btn" data-sp-goto="' +
              esc(x.sid + "|" + x.course) +
              '">Open</button>'
            : "<span></span>") +
          "</li>"
        );
      })
      .join("");
    var prio =
      '<section class="sp-box"><h3>What to start first</h3><p class="sp-muted">In the order to begin them, at about ' +
      EASY_DAY / 60 +
      ' h a day for each, with a day spare before each exam.</p><ol class="sp-rem-list">' +
      rows +
      "</ol></section>";

    // Week by week: the study each week asks for against your free time.
    var load = {};
    list.forEach(function (x) {
      if (!x.minutes) return;
      var from = x.startBy < today ? today : x.startBy,
        to = x.type === "exam" ? C.addDays(x.date, -1) : x.date;
      if (to < from) to = from;
      var n = 0;
      for (var d = from; d <= to; d = C.addDays(d, 1)) n++;
      for (var d2 = from; d2 <= to; d2 = C.addDays(d2, 1)) {
        var w = weekStart(d2);
        load[w] = (load[w] || 0) + x.minutes / n;
      }
    });
    var weeks = [];
    for (var w = weekStart(today); w <= last; w = C.addDays(w, 7))
      weeks.push(w);
    var weekHtml =
      '<section class="sp-box"><h3>Week by week</h3><p class="sp-muted">Study each week asks for if you start on time, next to your free time (9 AM to 10 PM, after classes, work, events and the drive). A week is tight when it needs close to 3 h of study a day.</p><div class="sp-rem-weeks">' +
      weeks
        .map(function (w) {
          var free = 0,
            budget = 0;
          for (var i = 0; i < 7; i++) {
            var d = C.addDays(w, i);
            if (d < today) continue;
            var f = freeMinutes(d);
            free += f;
            budget += Math.min(f, STUDY_DAY);
          }
          // Judged against a realistic study budget (3 h a day at most),
          // not every free minute.
          var need = load[w] || 0,
            ratio = budget ? need / budget : need ? 2 : 0,
            label = !need
              ? "Free"
              : ratio < 0.5
                ? "Comfortable"
                : ratio < 0.85
                  ? "Busy"
                  : "Tight",
            cls = !need
              ? "free"
              : ratio < 0.5
                ? "ok"
                : ratio < 0.85
                  ? "busy"
                  : "tight",
            here = list.filter(function (x) {
              return weekStart(x.date) === w;
            });
          return (
            '<div class="sp-rem-week ' +
            cls +
            '"><div class="sp-rem-week-head"><b>' +
            esc(shortDate(w < today ? today : w)) +
            " – " +
            esc(shortDate(C.addDays(w, 6))) +
            '</b><span class="sp-rem-pill">' +
            label +
            '</span></div><div class="sp-rem-load"><span style="width:' +
            Math.min(100, ratio * 100) +
            '%"></span></div><div class="sp-rem-week-meta">' +
            (need ? "About " + hours(need) + " of study" : "No study needed") +
            " · " +
            hours(free) +
            " free" +
            (cls === "tight"
              ? ". Starting the next exam a few days early would spread this out."
              : "") +
            "</div>" +
            (here.length
              ? '<div class="sp-rem-chips">' +
                here
                  .map(function (x) {
                    return (
                      '<span class="sp-rem-chip ' +
                      x.type +
                      '"' +
                      hue(x.course) +
                      ">" +
                      esc(C.prettyDate(x.date).split(",")[0]) +
                      " · " +
                      esc(entryLabel(x)) +
                      "</span>"
                    );
                  })
                  .join("") +
                "</div>"
              : "") +
            "</div>"
          );
        })
        .join("") +
      "</div></section>";
    return (
      summary +
      focusHtml +
      '<div class="sp-rem-grid">' +
      prio +
      weekHtml +
      "</div>"
    );
  }
  // ── Tabs ──────────────────────────────────────────────────────────────
  // My plan is the day-to-day view, Setup is the one-step-at-a-time wizard
  // (your week, each exam's format, build), and course detail opens from Exams.
  function formatSkipped(key) {
    return Boolean((plan().formatSkip || {})[key]);
  }
  function readinessBodyHtml(sid, st) {
    var rows = st.rows, ratings = readinessProgress(sid);
    return '<p class="sp-wiz-lead"></p>' +
      '<div class="sp-note"><b>Estimated minimum: ' + hours(recommendedMinutes(sid)) + '</b> to cover the analyzed exam scope. Unchanged topics count as New. Previously studied is for material you learned before and need to refresh; it gets less time than New or Shaky, so most of your time goes to what you haven\'t covered. If you\'ve forgotten a topic, rate it Shaky or New. Solid topics count as 100% ready, and the schedule still reserves a short check. Use this as a planning estimate, not a 40/40 guarantee.</div>' +
      rows.map(function (r, n) {
        var a = analysis(r.course, sid);
        if (!a) return '<div class="sp-note">No topic analysis is available for ' + esc(r.course) + '; it cannot be rated here.</div>';
        var key = sid + ':' + n, opened = Boolean(ui.readyOpen[key]), prog = courseProgress(r.course, a, r.exam);
        return '<section class="sp-course sp-readiness-course' + (opened ? ' open' : '') + '"' + hue(r.course) + '><button class="sp-course-head sp-readiness-toggle" type="button" data-sp-readiness="' + key + '" aria-expanded="' + opened + '">' + ring(prog ? prog.ready : 0, undefined, 'sm') + '<span class="sp-course-title"><span class="sp-eyebrow">' + esc(examLabel(r.exam)) + '</span><b>' + esc(r.course) + '</b><small>' + (prog ? Math.round(prog.ready) + '% topic readiness' : 'Readiness not available') + '</small></span><span class="sp-readiness-chevron" aria-hidden="true">' + (opened ? '−' : '+') + '</span></button>' + (opened ? '<div class="sp-readiness-content">' + chaptersHtml(r.course, a, r.exam, true) + '</div>' : '') + '</section>';
      }).join('') +
      '<div class="sp-wiz-foot"><button class="btn muted" type="button" data-sp-step="2">Back</button><span>' + ratings.marked + ' of ' + ratings.total + ' rated</span><button class="btn solid" type="button" data-sp-step="4"' + (ratings.done ? '' : ' disabled') + '>Next: build schedule</button></div>';
  }
  function examRows(sid) {
    return seasonExams(sid).map(function (e) {
      var course = C.courseLabel(e.course),
        key = formatKeys(course, e, sid)[0],
        f = formatFor(course, e, sid);
      return {
        exam: e,
        course: course,
        key: key,
        format: f,
        skipped: !f && formatSkipped(key),
      };
    });
  }
  function hasAnyPlan() {
    return C.items.some(function (i) {
      return i.planSource === "study-plan";
    });
  }
  function weekDone() {
    return Boolean((plan().setup || {}).week) || hasAnyPlan();
  }
  function weekSummary() {
    var parts = ["Drive " + commute() + " min each way"],
      uni = uniSummary(),
      n = blocks().length;
    if (uni) parts.push(uni);
    if (n) parts.push(n + " time" + (n === 1 ? "" : "s") + " you can't study");
    return parts.join(" · ");
  }
  function weekBodyHtml() {
    return (
      '<div class="sp-wk"><div class="sp-wk-part sp-study-limits"><h4>Study time limits</h4><p class="sp-muted">Set your maximum study time. Leave the weekly limit empty for no weekly cap.</p><div class="sp-limit-fields"><label>Hours per day<input type="number" min="1" max="10" step="0.5" data-sp-study-daily value="' + studyLimits().daily + '" /></label><label>Hours per week<input type="number" min="0.5" max="70" step="0.5" data-sp-study-weekly value="' + (studyLimits().weekly || "") + '" placeholder="No limit" /></label></div></div><div class="sp-wk-part"><div class="sp-wk-head"><h4>Getting to uni</h4><button type="button" class="sp-chip-btn" data-sp-uni-reset>Reset</button></div><p class="sp-muted">Set a normal day once. Days you leave off are worked out from your classes.</p>' +
      uniTimesHtml() +
      '</div><div class="sp-wk-part"><h4>Times you can\'t study</h4><p class="sp-muted">Work, gym, family. No study is planned in these.</p>' +
      blockedHtml() +
      '</div></div><div class="sp-wiz-foot"><span></span><button class="btn solid" type="button" data-sp-week-done>Next: exam formats</button></div>'
    );
  }
  function formatStatus(r) {
    return r.format
      ? formatSummary(r.format, true) || "Saved"
      : r.skipped
        ? "Not announced yet"
        : "Not set";
  }
  // One exam at a time: the list on the left, its details on the right.
  function formatsBodyHtml(sid, rows) {
    if (!rows.length)
      return (
        '<p class="sp-muted">No upcoming ' +
        esc(seasonInfo(sid).noun.toLowerCase()) +
        's on your calendar yet. Add the dates from the Exams tab, or switch season above.</p><div class="sp-wiz-foot"><button class="btn muted" type="button" data-sp-step="1">Back</button><button class="btn solid" type="button" data-sp-view="exams">Go to Exams</button></div>'
      );
    var sel =
        rows.find(function (r) {
          return r.key === ui.fmtOpen;
        }) ||
        rows.find(function (r) {
          return !r.format && !r.skipped;
        }) ||
        rows[0],
      left = rows.filter(function (r) {
        return !r.format && !r.skipped;
      }).length,
      a = analysis(sel.course, sid);
    return (
      '<div class="sp-fmt-pane"><div class="sp-fmt-exams" role="group" aria-label="Exams">' +
      rows
        .map(function (r) {
          return (
            '<button type="button" class="' +
            (r.format ? "set" : r.skipped ? "later" : "") +
            '" data-sp-fmt-open="' +
            esc(r.key) +
            '" aria-pressed="' +
            (r === sel) +
            '"' +
            hue(r.course) +
            '><span class="sp-fmt-dot"></span><span class="sp-fmt-exam-text"><b>' +
            esc(r.course) +
            "</b><span>" +
            esc(formatStatus(r)) +
            "</span></span></button>"
          );
        })
        .join("") +
      '</div><div class="sp-fmt-detail"' +
      hue(sel.course) +
      '><div class="sp-fmt-detail-head"><div><h4>' +
      esc(sel.course) +
      '</h4><p class="sp-muted">' +
      esc(examLabel(sel.exam)) +
      "</p></div>" +
      (sel.format || sel.skipped
        ? ""
        : '<button type="button" class="sp-chip-btn" data-sp-fmt-later="' +
          esc(sel.key) +
          '">Instructor hasn\'t said yet</button>') +
      "</div>" +
      formatEditorHtml(sel.course, a || null, sel.exam, sid, sel.format, true) +
      '</div></div><div class="sp-wiz-foot"><button class="btn muted" type="button" data-sp-step="1">Back</button>' +
      (left
        ? '<span class="sp-muted">' +
          left +
          " exam" +
          (left === 1 ? "" : "s") +
          " still to go</span>"
        : "<span></span>") +
      '<button class="btn solid" type="button" data-sp-step="3"' +
      (left ? " disabled" : "") +
      ">Next: rate your readiness</button></div>"
    );
  }
  // Upcoming dates of weekly unavailable times, each of which can be freed.
  function comingUpHtml(sid) {
    if (!plannedItems(sid).length) return "";
    var today = C.todayKey(),
      rows = [];
    blocks().forEach(function (x) {
      if (x.date) return;
      for (var i = 0; i < 14; i++) {
        var d = C.addDays(today, i);
        if ((x.days || []).indexOf(C.fromKey(d).getDay()) > -1)
          rows.push({ x: x, date: d, skipped: (x.skips || []).indexOf(d) > -1 });
      }
    });
    if (!rows.length) return "";
    rows.sort(function (p, q) {
      return p.date.localeCompare(q.date);
    });
    return (
      '<div class="sp-coming"><h4>Plans changed?</h4><p class="sp-muted">Not going to something this time? Study then instead, and the next day\'s study moves up to it.</p><ul>' +
      rows
        .slice(0, 5)
        .map(function (r) {
          return (
            '<li><span><b>' +
            esc(shortDate(r.date)) +
            "</b> " +
            esc(r.x.label || "Unavailable") +
            (r.x.start ? " · " + esc(C.timeRange(r.x.start, r.x.end)) : " · All day") +
            "</span>" +
            (r.skipped
              ? '<span class="sp-coming-free">Studying instead</span><button type="button" class="sp-link-btn" data-sp-unskip="' +
                esc(r.x.id + "|" + r.date) +
                '">Undo</button>'
              : '<button type="button" class="sp-chip-btn" data-sp-skip="' +
                esc(r.x.id + "|" + r.date) +
                '">Study instead</button>') +
            "</li>"
          );
        })
        .join("") +
      "</ul></div>"
    );
  }
  // The chapters an exam can cover, for the picker on the Exams tab: the
  // study plan's list when the course has one (so both stay in step), else
  // the syllabus's list, else nothing and the student writes them in.
  var syllabi = null;
  function loadSyllabi() {
    if (!syllabi)
      syllabi = fetchJson("/academic-plan-themes/course-syllabi.json").catch(
        function () {
          return {};
        },
      );
    return syllabi;
  }
  function examChapters(exam) {
    var course = C.courseLabel(exam.course),
      type = C.canonicalExamType(exam.type),
      sid = type === "bonus-quiz" ? "quiz" : type;
    return new Promise(function (resolve) {
      var tries = 0;
      (function wait() {
        loadIndex();
        var a = analysis(course, sid);
        if (a === undefined && ++tries < 100) return setTimeout(wait, 100);
        resolve(a || null);
      })();
    }).then(function (a) {
      if (a)
        return {
          source: "plan",
          defaults: overviewScope(a, exam).ids,
          chapters: a.chapters.map(function (c) {
            return { id: c.id, label: chapterName(c) };
          }),
        };
      return loadSyllabi().then(function (all) {
        var key = course.replace(/\s+/g, ""),
          entry = all[key] || all[key.replace("ETHCS", "ETHC")],
          list = (entry && entry.chapters) || [];
        return {
          source: list.length ? "syllabus" : "none",
          defaults: [],
          chapters: list.map(function (c) {
            return {
              id: "s" + c.n,
              label: (/^\d/.test(c.n) ? "Ch " + c.n + " " : c.n + " ") + c.title,
            };
          }),
        };
      });
    });
  }
  function setupState(sid) {
    var rows = examRows(sid),
      built = plannedItems(sid).length > 0,
      wk = weekDone(),
      left = rows.filter(function (r) {
        return !r.format && !r.skipped;
      }).length,
      fm = rows.length > 0 && !left;
    var ratings = readinessProgress(sid),
      readinessDone = ratings.done;
    return {
      rows: rows,
      built: built,
      wk: wk,
      left: left,
      fm: fm,
      readinessDone: readinessDone,
      ready: (wk && fm && readinessDone) || built,
      auto: !wk ? 1 : !fm && !built ? 2 : !readinessDone && !built ? 3 : 4,
    };
  }
  function currentView(sid) {
    if (ui.view) return ui.view;
    if (plan().season === "remaining") return "left";
    var st = setupState(sid);
    return st.built || !st.rows.length ? "plan" : "setup";
  }
  function setupHtml(sid) {
    var st = setupState(sid),
      active = ui.step || st.auto,
      steps = [
        { n: 1, label: "Your week", done: st.wk },
        { n: 2, label: "Exam formats", done: st.fm },
        { n: 3, label: "Your readiness", done: st.readinessDone },
        { n: 4, label: "Build your plan", done: st.built },
      ],
      body =
        active === 1
          ? '<p class="sp-wiz-lead">When are you at uni, and when can\'t you study?</p>' +
            weekBodyHtml()
          : active === 2
            ? '<p class="sp-wiz-lead">How will each exam ask?</p>' +
              formatsBodyHtml(sid, st.rows)
            : active === 3
              ? readinessBodyHtml(sid, st)
              : (st.ready
                ? ""
                : '<div class="sp-note">Finish ' +
                  (!st.wk && !st.fm
                    ? "Your week and Exam formats"
                    : !st.wk
                      ? "Your week"
                      : "Exam formats") +
                  " first, so the plan fits your real week.</div>") +
              plannerHtml(sid, st.ready) +
              '<div class="sp-wiz-foot"><button class="btn muted" type="button" data-sp-step="3">Back</button><span></span>' +
              (st.built
                ? '<button class="btn solid" type="button" data-sp-view="plan">Go to my plan</button>'
                : "<span></span>") +
              "</div>";
    return (
      '<ol class="sp-wiz-steps">' +
      steps
        .map(function (x) {
          return (
            '<li><button type="button" class="' +
            (x.n === active ? "current" : x.done ? "done" : "") +
            '" data-sp-step="' +
            x.n +
            '"' +
            (x.n === active ? ' aria-current="step"' : "") +
            '><span class="sp-wiz-num">' +
            (x.done && x.n !== active ? '<span class="sp-step-tick"></span>' : x.n) +
            "</span>" +
            esc(x.label) +
            "</button></li>"
          );
        })
        .join("") +
      '</ol><div class="sp-wiz-body">' +
      body +
      "</div>"
    );
  }
  // ── My plan ───────────────────────────────────────────────────────────
  function dayName(k) {
    var today = C.todayKey();
    return k === today
      ? "Today"
      : k === C.addDays(today, 1)
        ? "Tomorrow"
        : shortDate(k);
  }
  function sessionParts(i) {
    var cut = String(i.title || "Study").split(" · ");
    return {
      head: cut.length > 1 ? cut[0] : i.course || "",
      name: cut.length > 1 ? cut.slice(1).join(" · ") : cut[0],
    };
  }
  function upcomingSessions(sid) {
    var today = C.todayKey(),
      now = nowMinutes();
    return plannedItems(sid)
      .filter(function (i) {
        return (
          !i.planDone &&
          i.start &&
          (i.date > today || (i.end && C.minutes(i.end) > now))
        );
      })
      .sort(function (a, b) {
        return (a.date + a.start).localeCompare(b.date + b.start);
      });
  }
  function examListHtml(sid, st) {
    return (
      '<section class="sp-box"><h3>Exams</h3><div class="sp-plan-exams">' +
      st.rows
        .map(function (r) {
          var a = analysis(r.course, sid),
            prog = a ? courseProgress(r.course, a, r.exam) : null,
            d = daysUntil(r.exam.date);
          return (
            '<button type="button" data-sp-open-course="' +
            esc(r.course) +
            '"' +
            hue(r.course) +
            ">" +
            (prog ? ring(prog.ready, undefined, "sm") : ring(0, "–", "sm")) +
            '<span class="sp-plan-exam-text"><b>' +
            esc(r.course) +
            "</b><span>" +
            esc(examLabel(r.exam)) +
            '</span></span><span class="sp-days' +
            (d <= 7 ? " soon" : "") +
            '">' +
            d +
            "d</span></button>"
          );
        })
        .join("") +
      "</div>" +
      (st.left
        ? '<button type="button" class="sp-link-btn" data-sp-goto-step="2">' +
          st.left +
          " exam" +
          (st.left === 1 ? "" : "s") +
          " without a format. Set them</button>"
        : "") +
      "</section>"
    );
  }
  function planViewHtml(sid) {
    var st = setupState(sid),
      noun = seasonInfo(sid).noun.toLowerCase();
    if (!st.rows.length)
      return (
        '<div class="sp-plan-empty"><h3>No upcoming ' +
        esc(noun) +
        's</h3><p class="sp-muted">Add the dates in the Exams tab, or choose another season above.</p><button class="btn solid" type="button" data-sp-view="exams">Go to Exams</button></div>'
      );
    var list = upcomingSessions(sid),
      main;
    if (!st.built)
      main =
        '<div class="sp-plan-empty"><h3>No plan for your ' +
        esc(noun) +
        's yet</h3><p class="sp-muted">Tell it about your week and how each exam will ask, and it builds the schedule around your calendar.</p><button class="btn solid" type="button" data-sp-view="setup">' +
        (st.wk ? "Continue setup" : "Set up my plan") +
        "</button></div>";
    else if (!list.length)
      main =
        '<div class="sp-plan-empty"><h3>All caught up</h3><p class="sp-muted">Every planned session is done. Re-plan from Setup if you want more practice.</p></div>';
    else {
      var first = list[0],
        fp = sessionParts(first),
        mins = C.minutes(first.end) - C.minutes(first.start),
        rest = list.slice(1),
        shownDays = rest
          .map(function (i) {
            return i.date;
          })
          .filter(function (d, n, all) {
            return all.indexOf(d) === n;
          })
          .slice(0, 3),
        // A short look ahead; the full list lives on the calendar.
        week = rest
          .filter(function (i) {
            return shownDays.indexOf(i.date) > -1;
          })
          .slice(0, 8),
        later = rest.length - week.length,
        byDay = {};
      week.forEach(function (i) {
        (byDay[i.date] = byDay[i.date] || []).push(i);
      });
      main =
        '<section class="sp-next"' +
        hue(first.course) +
        '><div class="sp-eyebrow">Next up</div><h3>' +
        esc(fp.name) +
        '</h3><p class="sp-next-when"><b>' +
        esc(dayName(first.date)) +
        ", " +
        esc(C.timeLabel(first.start)) +
        "</b> · " +
        esc(aboutHours(mins)) +
        (fp.head ? " · " + esc(fp.head) : "") +
        "</p>" +
        (first.notes ? '<p class="sp-muted">' + esc(first.notes) + "</p>" : "") +
        (function () {
          var fa = analysis(first.course, sid),
            fch =
              fa &&
              first.planChapter &&
              fa.chapters.find(function (c) {
                return c.id === first.planChapter;
              });
          return fch
            ? studyLinksHtml(fch)
            : fa && fa.course_page
              ? '<div class="sp-links"><a href="' +
                  esc(fa.course_page) +
                  '">Course page</a></div>'
              : "";
        })() +
        '<button class="btn solid" type="button" data-sp-sess-done="' +
        esc(first.id) +
        '">Finished early · update plan</button><button class="btn muted" type="button" data-sp-sess-more="' +
        esc(first.id) +
        '">I need more time</button></section>' +
        (week.length
          ? '<section class="sp-box"><h3>Coming up</h3>' +
            Object.keys(byDay)
              .sort()
              .map(function (d) {
                return (
                  '<h4 class="sp-week-day">' +
                  esc(dayName(d)) +
                  '</h4><ul class="sp-week-list">' +
                  byDay[d]
                    .map(function (i) {
                      var ip = sessionParts(i);
                      return (
                        "<li" +
                        hue(i.course) +
                        '><input type="checkbox" data-sp-sess-done="' +
                        esc(i.id) +
                        '" aria-label="Mark done: ' +
                        esc(i.title) +
                        '" /><span class="sp-week-time">' +
                        esc(C.timeLabel(i.start)) +
                        '</span><span class="sp-week-text"><b>' +
                        esc(ip.name) +
                        "</b><span>" +
                        esc(ip.head) +
                        "</span></span></li>"
                      );
                    })
                    .join("") +
                  "</ul>"
                );
              })
              .join("") +
            (later
              ? '<p class="sp-muted">And ' +
                later +
                " more on your calendar.</p>"
              : "") +
            "</section>"
          : "");
    }
    var coming = comingUpHtml(sid);
    return (
      '<div class="sp-plan-grid"><div class="sp-plan-main">' +
      main +
      '</div><div class="sp-plan-side">' +
      examListHtml(sid, st) +
      (coming ? '<section class="sp-box">' + coming + "</section>" : "") +
      "</div></div>"
    );
  }
  // A weekly unavailable time is cancelled for one date: that time opens
  // up, and the next study day's sessions move onto it.
  function nowMinutes() {
    var n = new Date();
    return n.getHours() * 60 + n.getMinutes();
  }
  function isOpenSession(i) {
    if (i.planSource !== "study-plan" || i.planDone || !i.start || !i.end) return false;
    var today = C.todayKey();
    return i.date > today || (i.date === today && C.minutes(i.start) > nowMinutes());
  }
  // The freed time itself fills first, then the rest of that day.
  function pullForward(day, block) {
    var today = C.todayKey(),
      open = C.items.filter(isOpenSession),
      next = "";
    open.forEach(function (i) {
      if (i.date > day && i.date <= C.addDays(day, 7) && (!next || i.date < next)) next = i.date;
    });
    if (!next) return { moved: 0, from: "" };
    var start =
        day === today
          ? Math.max(DAY_START, Math.ceil((nowMinutes() + 15) / 15) * 15)
          : DAY_START,
      slots = freeSlots(day, "remaining", start).map(function (x) {
        return x.slice();
      });
    function take(s, e) {
      var out = [];
      slots.forEach(function (x) {
        if (e <= x[0] || s >= x[1]) out.push(x);
        else {
          if (s > x[0]) out.push([x[0], s]);
          if (e < x[1]) out.push([e, x[1]]);
        }
      });
      slots = out;
    }
    C.items.forEach(function (i) {
      if (i.planSource === "study-plan" && i.date === day && i.start && i.end)
        take(C.minutes(i.start) - BUFFER, C.minutes(i.end) + BUFFER);
    });
    var moved = 0;
    open
      .filter(function (i) {
        return i.date === next;
      })
      .sort(function (p, q) {
        return p.start.localeCompare(q.start);
      })
      .forEach(function (i) {
        var len = C.minutes(i.end) - C.minutes(i.start),
          from = block && block.start ? C.minutes(block.start) : null,
          to = block && block.end ? C.minutes(block.end) : null,
          inFreed =
            from === null
              ? null
              : slots.find(function (x) {
                  return Math.min(x[1], to) - Math.max(x[0], from) >= len;
                }),
          slot =
            inFreed ||
            slots.find(function (x) {
              return x[1] - x[0] >= len;
            });
        if (!slot) return;
        var st = inFreed ? Math.max(slot[0], from) : slot[0];
        i.date = day;
        i.endDate = day;
        i.start = C.toTime(st);
        i.end = C.toTime(st + len);
        i.planPinned = true;
        delete i.planOverlapOk;
        take(st, st + len + BUFFER);
        moved++;
      });
    return { moved: moved, from: next };
  }
  function setBlockSkip(id, date, on) {
    updatePlan(
      function (p) {
        (p.blocked || []).forEach(function (x) {
          if (x.id !== id) return;
          var list = (x.skips || []).filter(function (d) {
            return d !== date && d >= C.todayKey();
          });
          if (on) list.push(date);
          x.skips = list;
        });
      },
      true,
      true,
    );
    ui.preview = null;
    var r = on
      ? pullForward(
          date,
          blocks().find(function (x) {
            return x.id === id;
          }),
        )
      : { moved: 0 };
    C.persist().then(function () {
      C.renderAll();
      if (on)
        C.toast(
          r.moved
            ? shortDate(date) +
                " is free. " +
                r.moved +
                " session" +
                (r.moved === 1 ? "" : "s") +
                " moved up from " +
                shortDate(r.from)
            : shortDate(date) + " is free. No later sessions to move up.",
        );
    });
  }
  // Does this session sit on top of something real (an event, class, exam,
  // the drive or an unavailable time)? Other study sessions don't count.
  function overlaps(i) {
    if (!i.start || !i.end) return false;
    var b = busyFor(i.date, "remaining"),
      s = C.minutes(i.start),
      e = C.minutes(i.end);
    return (
      b.all ||
      b.busy.some(function (x) {
        return s < x[1] && e > x[0];
      })
    );
  }
  // Runs after every calendar change. A session now clashing with something
  // new is released, and its season is rebuilt around the change. A session
  // you placed on top of something yourself is left where you put it.
  var reflowing = false,
    reflowTimer = null,
    lastClash = "";
  function scheduleReflow() {
    if (reflowing || reflowTimer || !C.signedIn) return;
    reflowTimer = setTimeout(function () {
      reflowTimer = null;
      reflow();
    }, 0);
  }
  function reflow() {
    var hit = C.items.filter(function (i) {
      return isOpenSession(i) && !i.planOverlapOk && overlaps(i);
    });
    var sig = hit
      .map(function (i) {
        return i.id + i.date + i.start;
      })
      .join();
    if (!hit.length || sig === lastClash) {
      lastClash = sig;
      return;
    }
    lastClash = sig;
    reflowing = true;
    var seasons = {},
      before = JSON.parse(
        JSON.stringify(
          C.items.filter(function (i) {
            return i.planSource === "study-plan";
          }),
        ),
      ),
      hitIds = hit.map(function (i) {
        return i.id;
      });
    hit.forEach(function (i) {
      seasons[i.planSeason] = true;
      delete i.planPinned;
    });
    var n = hit.length,
      what =
        n + " study session" + (n === 1 ? "" : "s") + " moved around your calendar";
    Object.keys(seasons)
      .reduce(function (chain, sid) {
        return chain.then(function () {
          return replan(sid, what, true);
        });
      }, Promise.resolve())
      .then(
        function () {
          reflowing = false;
          C.toastUndo(what, function () {
            for (var n = C.items.length - 1; n >= 0; n--)
              if (C.items[n].planSource === "study-plan") C.items.splice(n, 1);
            before.forEach(function (i) {
              // Left where it was on purpose, so it won't be moved again.
              if (hitIds.indexOf(i.id) > -1) i.planOverlapOk = true;
              C.items.push(i);
            });
            C.persist().then(C.renderAll);
          });
        },
        function () {
          reflowing = false;
        },
      );
  }
  // A class that's cancelled, skipped or moved online frees up time, so offer
  // to move study into it. Only new changes count: whatever was already marked
  // when the page loaded has had its chance.
  var freedKnown = null,
    freedOpen = false,
    freedTimer = null;
  function classWindow(c, x) {
    return { start: x.start || c.start || "", end: x.end || c.end || "" };
  }
  function freedNow() {
    var today = C.todayKey(),
      out = {},
      gone = {};
    function classOf(id) {
      return C.classes.find(function (c) {
        return c.id === id;
      });
    }
    function add(key, c, x, why) {
      var w = classWindow(c, x);
      // Later today, or nothing is actually gained.
      if (x.date === today && w.end && C.minutes(w.end) <= nowMinutes()) return;
      out[key] = {
        date: x.date,
        title: c.title || "Class",
        why: why,
        start: w.start,
        end: w.end,
      };
    }
    C.classAttendance.forEach(function (r) {
      if (r.date < today || (r.reason !== "cancelled" && r.reason !== "skipped")) return;
      var c = classOf(r.classId);
      if (!c) return;
      gone[r.classId + "|" + r.date] = true;
      add("a|" + r.classId + "|" + r.date + "|" + r.reason, c, r, r.reason);
    });
    C.classOverrides.forEach(function (o) {
      if (o.date < today || o.movedTo || !(o.mode === "online" || o.onlineOnly)) return;
      var c = classOf(o.classId);
      if (!c || c.onlineOnly || gone[o.classId + "|" + o.date]) return;
      add("o|" + o.classId + "|" + o.date, c, o, "online");
    });
    return out;
  }
  function scheduleFreedCheck() {
    if (freedTimer || !C.loaded) return;
    freedTimer = setTimeout(function () {
      freedTimer = null;
      checkFreed();
    }, 0);
  }
  function checkFreed() {
    if (freedOpen || reflowing) return;
    var now = freedNow(),
      fresh = freedKnown
        ? Object.keys(now).filter(function (k) {
            return !freedKnown[k];
          })
        : [];
    freedKnown = now;
    if (fresh.length)
      offerFreed(
        fresh.map(function (k) {
          return now[k];
        }),
      );
  }
  function freedLine(x) {
    var when = shortDate(x.date);
    return x.why === "cancelled"
      ? x.title + " on " + when + " is cancelled."
      : x.why === "skipped"
        ? "You're skipping " + x.title + " on " + when + "."
        : x.title + " on " + when + " moved online.";
  }
  function offerFreed(list) {
    var days = {},
      home = {};
    list.forEach(function (x) {
      var d = (days[x.date] = days[x.date] || { date: x.date, start: "", end: "" });
      if (x.start && (!d.start || x.start < d.start)) d.start = x.start;
      if (x.end && x.end > d.end) d.end = x.end;
      if (x.why === "online" && !campusSpan(x.date) && uniTimes(x.date).leave)
        home[x.date] = true;
    });
    var order = Object.keys(days)
      .sort()
      .map(function (k) {
        return days[k];
      });
    function pullAll() {
      order.forEach(function (d) {
        pullForward(d.date, d.start && d.end ? d : null);
      });
    }
    // Try it, note what would move, and put everything back before asking.
    var before = planSnapshot(),
      was = {};
    before.forEach(function (i) {
      was[i.id] = i;
    });
    homeDays = home;
    pullAll();
    homeDays = {};
    var moves = C.items
      .filter(function (i) {
        var b = was[i.id];
        return b && (b.date !== i.date || b.start !== i.start);
      })
      .map(function (i) {
        return { title: i.title || "Study session", from: was[i.id], date: i.date, start: i.start };
      });
    restorePlan(before);
    if (moves.length) showFreed(list, order, home, moves, pullAll);
  }
  function showFreed(list, order, home, moves, pullAll) {
    function when(date, start) {
      return shortDate(date) + " · " + C.timeLabel(start);
    }
    var prior = document.activeElement,
      one = moves.length === 1,
      hasHome = Object.keys(home).length > 0,
      wrap = document.createElement("div");
    wrap.className = "sp-free-overlay";
    wrap.setAttribute("data-ar-own", "");
    wrap.innerHTML =
      '<section class="sp-free-dialog" role="dialog" aria-modal="true" aria-labelledby="sp-free-title"><h3 id="sp-free-title">' +
      esc(
        order.length === 1
          ? "You have free time on " + shortDate(order[0].date)
          : "You have free time on " + order.length + " days",
      ) +
      "</h3>" +
      list
        .map(function (x) {
          return "<p>" + esc(freedLine(x)) + "</p>";
        })
        .join("") +
      (hasHome ? "<p>This assumes you stay home that day.</p>" : "") +
      '<p class="sp-free-ask">' +
      (one
        ? "Want to move this up so a later day is lighter?"
        : "Want to move these up so later days are lighter?") +
      '</p><ul class="sp-free-list">' +
      moves
        .map(function (m) {
          return (
            "<li><b>" +
            esc(m.title) +
            "</b><span>From " +
            esc(when(m.from.date, m.from.start)) +
            " to " +
            esc(when(m.date, m.start)) +
            "</span></li>"
          );
        })
        .join("") +
      '</ul><div class="sp-free-actions"><button type="button" class="btn" data-free-keep>Keep my plan</button><button type="button" class="btn solid" data-free-move>' +
      (one ? "Move it" : "Move them") +
      "</button></div></section>";
    function close() {
      freedOpen = false;
      document.removeEventListener("keydown", onKey, true);
      wrap.remove();
      if (prior && prior.focus) prior.focus();
    }
    function onKey(ev) {
      if (ev.key !== "Escape") return;
      ev.stopPropagation();
      close();
    }
    function accept() {
      close();
      var before = planSnapshot(),
        dates = Object.keys(home);
      if (dates.length)
        updatePlan(
          function (p) {
            var kept = {},
              today = C.todayKey();
            Object.keys(p.uniHome || {}).forEach(function (d) {
              if (d >= today) kept[d] = true;
            });
            dates.forEach(function (d) {
              kept[d] = true;
            });
            p.uniHome = kept;
          },
          true,
          true,
        );
      pullAll();
      C.persist().then(function () {
        C.renderAll();
        C.toastUndo(
          moves.length + " study session" + (one ? "" : "s") + " moved up",
          function () {
            if (dates.length)
              updatePlan(
                function (p) {
                  dates.forEach(function (d) {
                    if (p.uniHome) delete p.uniHome[d];
                  });
                },
                true,
                true,
              );
            restorePlan(before);
            C.persist().then(C.renderAll);
          },
        );
      });
    }
    wrap.addEventListener("click", function (ev) {
      if (ev.target === wrap || ev.target.hasAttribute("data-free-keep")) close();
      else if (ev.target.hasAttribute("data-free-move")) accept();
    });
    document.addEventListener("keydown", onKey, true);
    freedOpen = true;
    document.body.appendChild(wrap);
    wrap.querySelector("[data-free-move]").focus();
  }
  // Anything half-typed in a form survives a re-render of the tab.
  function formKey(form) {
    return form.dataset.spFormatForm || "block";
  }
  function captureForms(root) {
    var saved = {},
      active = document.activeElement;
    root
      .querySelectorAll("[data-sp-format-form], [data-sp-block-form]")
      .forEach(function (form) {
        saved[formKey(form)] = [].map.call(form.elements, function (el) {
          return { value: el.value, checked: el.checked, focused: el === active };
        });
      });
    return saved;
  }
  function restoreForms(root, saved) {
    root
      .querySelectorAll("[data-sp-format-form], [data-sp-block-form]")
      .forEach(function (form) {
        var state = saved[formKey(form)];
        if (!state || state.length !== form.elements.length) return;
        [].forEach.call(form.elements, function (el, n) {
          if (el.type === "checkbox" || el.type === "radio") el.checked = state[n].checked;
          else if (el.tagName !== "BUTTON") el.value = state[n].value;
          if (state[n].focused) el.focus();
        });
      });
  }
  function render() {
    var root = $("study-plan-root");
    if (!root || !C) return;
    loadIndex();
    scheduleReflow();
    scheduleFreedCheck();
    var sid = season(),
      view = currentView(sid),
      courses = courseList(sid);
    if (ui.course && courses.indexOf(ui.course) < 0) ui.course = "";
    var scrollY = window.scrollY,
      drafts = captureForms(root),
      body =
        view === "left"
          ? remainingHtml()
          : view === "setup"
            ? setupHtml(sid)
            : view === "exams"
              ? ui.course
                ? '<div class="sp-back-row"><button type="button" class="sp-chip-btn" data-sp-home>All exams</button></div>' +
                  examCardsHtml(sid, courses) +
                  courseHtml(ui.course, sid)
                : heroHtml(sid) +
                  examCardsHtml(sid, courses) +
                  clashHtml(sid)
              : planViewHtml(sid);
    root.innerHTML =
      headHtml(sid, view) + '<div class="sp-body">' + body + "</div>";
    restoreForms(root, drafts);
    if (Math.abs(window.scrollY - scrollY) > 2) window.scrollTo(0, scrollY);
  }

  // ── Events ────────────────────────────────────────────────────────────
  function onClick(ev) {
    var t = ev.target.closest("button, input, a, [data-sp-course]");
    if (!t || !$("study-plan-root").contains(t)) return;
    var d = t.dataset;
    if (d.spView) {
      ui.view = d.spView;
      if (d.spView !== "exams") ui.course = "";
      render();
      window.scrollTo(
        0,
        $("study-plan-root").getBoundingClientRect().top + window.scrollY - 20,
      );
    } else if (d.spOpenCourse) {
      ui.view = "exams";
      ui.course = d.spOpenCourse;
      render();
    } else if (d.spReadiness) {
      ui.readyOpen[d.spReadiness] = !ui.readyOpen[d.spReadiness];
      render();
    } else if (d.spGotoStep) {
      ui.view = "setup";
      ui.step = Number(d.spGotoStep);
      render();
    } else if (d.spSessDone) {
      var sess = C.items.find(function (i) {
        return i.id === d.spSessDone;
      });
      if (!sess) return;
      sess.planDone = true;
      C.persist().then(function () { return replan(sess.planSeason, "Session finished early"); });
    } else if (d.spSessMore) {
      var sess = C.items.find(function (i) { return i.id === d.spSessMore; });
      if (!sess) return;
      var length = C.minutes(sess.end) - C.minutes(sess.start),
        day = sess.date,
        slot = null;
      for (var n = 0; n < 14 && !slot; n++) {
        day = C.addDays(day, 1);
        var start = day === C.todayKey() ? Math.max(DAY_START, nowMinutes() + 15) : DAY_START;
        slot = freeSlots(day, sess.planSeason, start).find(function (s) { return s[1] - s[0] >= length; }) || null;
      }
      if (!slot) { C.toast("No later free slot found before the exam"); return; }
      sess.date = day; sess.endDate = day; sess.start = C.toTime(slot[0]); sess.end = C.toTime(slot[0] + length); sess.planPinned = true;
      C.persist().then(function () { return replan(sess.planSeason, "Session moved back"); });
    } else if (d.spSeason) {
      ui.preview = null;
      ui.step = undefined;
      ui.fmtOpen = "";
      updatePlan(function (p) {
        p.season = d.spSeason;
      }, true);
    } else if (d.spCourse) {
      ui.course = d.spCourse;
      render();
    } else if (d.spAddExam !== undefined) {
      C.openExamEditor("", "", {
        course: d.spAddExam,
        type: season() === "quiz" ? "quiz" : season(),
      });
    } else if (d.spDone !== undefined || d.spUndone !== undefined) {
      var dc = d.spDone !== undefined ? d.spDone : d.spUndone,
        on = d.spDone !== undefined,
        ds = season();
      updatePlan(function (p) {
        p.done = p.done || {};
        p.done[ds] = p.done[ds] || {};
        if (on) p.done[ds][dc] = true;
        else delete p.done[ds][dc];
      }, true);
    } else if (t.hasAttribute("data-sp-build")) {
      // Setup may be the first screen to need these courses' analyses.
      var buildFor = season();
      t.disabled = true;
      t.textContent = "BUILDING…";
      whenLoaded(buildFor).then(function (ok) {
        if (!ok) {
          C.toast("Could not load the exam chapter plans. Check your connection and try again.");
          return;
        }
        ui.preview = buildSchedule(buildFor);
        if (!ui.preview.placed.length) {
          C.toast("No study sessions could be scheduled. Check the exam dates and available study time.");
          return;
        }
        render();
      }).catch(function (err) {
        console.error("Study plan build failed", err);
        C.toast("The study plan could not be built. Please try again.");
      }).finally(function () {
        if (t.isConnected) { t.disabled = false; t.textContent = "BUILD MY SCHEDULE"; }
      });
    } else if (t.hasAttribute("data-sp-commit")) commitPreview();
    else if (t.hasAttribute("data-sp-discard")) {
      ui.preview = null;
      render();
    } else if (t.hasAttribute("data-sp-clear")) clearPlanned();
    else if (t.hasAttribute("data-sp-delete-all")) deleteAll();
    else if (t.hasAttribute("data-sp-start-over")) startOver();
    else if (d.spBlockRemove) {
      var bid = d.spBlockRemove;
      saveBlocks(function (p) {
        p.blocked = (p.blocked || []).filter(function (x) {
          return x.id !== bid;
        });
      }, "Unavailable time removed");
    }
    else if (d.spLevel !== undefined) {
      var readinessCourse = d.spReadyCourse || ui.course,
        a = analysis(readinessCourse, season());
      if (!a) return;
      var key = readyKey(readinessCourse, a),
        lv = Number(d.spLevel);
      ui.preview = null;
      updatePlan(function (p) {
        p.ready = p.ready || {};
        p.ready[key] = p.ready[key] || {};
        // Store New (0) as an explicit override when prior exams would
        // otherwise infer Previously studied for this chapter/topic.
        p.ready[key][d.spUnit] = lv;
      });
    } else if (d.spOpen) {
      ui.open[d.spOpen] = !ui.open[d.spOpen];
      render();
    } else if (d.spFmtEdit) {
      ui.fmtEdit[d.spFmtEdit] = true;
      render();
    } else if (d.spFmtCancel) {
      delete ui.fmtEdit[d.spFmtCancel];
      ui.fmtOpen = "";
      render();
    } else if (d.spFmtRemove) {
      if (
        !window.confirm(
          "Remove this exam format?",
        )
      )
        return;
      var rk = d.spFmtRemove;
      delete ui.fmtEdit[rk];
      ui.preview = null;
      updatePlan(function (p) {
        p.formats = p.formats || {};
        var fc = d.spFmtCourse || ui.course;
        formatKeys(fc, examFor(fc, season()), season()).forEach(
          function (k) {
            delete p.formats[k];
          },
        );
      }, true);
    } else if (d.spGoto) {
      var g = d.spGoto.split("|");
      ui.view = "exams";
      ui.course = g[1];
      ui.preview = null;
      updatePlan(function (p) {
        p.season = g[0];
      }, true);
      window.scrollTo(
        0,
        $("study-plan-root").getBoundingClientRect().top + window.scrollY - 20,
      );
    } else if (t.hasAttribute("data-sp-home")) {
      ui.course = "";
      render();
    } else if (d.spStep) {
      ui.step = Number(d.spStep);
      if (ui.step === 3) {
        var readinessSeason = season();
        whenLoaded(readinessSeason).then(function (loaded) {
          if (loaded) migrateLegacyReadiness(readinessSeason);
          render();
        });
      } else render();
    } else if (t.hasAttribute("data-sp-week-done")) {
      ui.step = 2;
      updatePlan(function (p) {
        p.setup = Object.assign({}, p.setup, { week: true });
      }, true);
    } else if (t.hasAttribute("data-sp-type-add")) {
      addCustomType(t.closest("form"));
    } else if (d.spFmtOpen) {
      ui.fmtOpen = d.spFmtOpen;
      render();
    } else if (d.spFmtLater) {
      var later = d.spFmtLater;
      ui.fmtOpen = "";
      updatePlan(function (p) {
        p.formatSkip = p.formatSkip || {};
        p.formatSkip[later] = true;
      }, true);
    } else if (d.spSkip || d.spUnskip) {
      var sk = (d.spSkip || d.spUnskip).split("|");
      setBlockSkip(sk[0], sk[1], Boolean(d.spSkip));
    } else if (t.hasAttribute("data-sp-uni-reset")) {
      resetUni();
    } else if (d.spUniClear) {
      saveUni(d.spUniClear, { leave: "", back: "" });
    } else if (d.spReveal) {
      ui.revealed[d.spReveal] = !ui.revealed[d.spReveal];
      render();
    } else if (t.hasAttribute("data-sp-drill")) {
      ui.drill = t.checked;
      ui.revealed = {};
      render();
    }
  }

  function saveFormat(form) {
    var key = form.dataset.spFormatForm,
      fd = new FormData(form),
      num = function (n) {
        var v = Math.round(Number(fd.get(n)));
        return isFinite(v) && v > 0 ? v : "";
      },
      sid = season(),
      course = form.dataset.spFormatCourse || ui.course,
      exam = examFor(course, sid),
      prev = formatFor(course, exam, sid),
      a = analysis(course, sid),
      base = a ? overviewScope(a, exam).ids : [],
      chapters = fd.getAll("ch"),
      next = {
        notes: String(fd.get("notes") || "").trim(),
        types: fd.getAll("type"),
        questions: num("questions"),
        minutes: num("minutes"),
        book: String(fd.get("book") || ""),
        topics: String(fd.get("topics") || "").trim(),
        // Only a change from the overview's chapters is stored, and an exam
        // with a date keeps it on the exam itself.
        chapters:
          !exam &&
          chapters.length &&
          chapters.sort().join() !== base.slice().sort().join()
            ? chapters
            : null,
        updated: C.todayKey(),
      };
    if (exam && a && C.setExamChapters) {
      var changed =
        chapters.length &&
        chapters.slice().sort().join() !== base.slice().sort().join();
      C.setExamChapters(exam.id, {
        chapters: changed ? chapters : [],
        chapterLabels: changed
          ? a.chapters
              .filter(function (c) {
                return chapters.indexOf(c.id) > -1;
              })
              .map(chapterName)
          : [],
      });
    }
    if (!next.types.length) next.types = detectFormats(next.notes);
    if (!next.types.length && !next.notes) {
      C.toast(
        "Pick at least one question type, or type what your instructor said",
      );
      return;
    }
    var history = (prev && prev.history) || [];
    if (prev) {
      var was =
        formatSummary(prev) +
        (prev.notes ? ' ("' + prev.notes + '")' : "") +
        (prev.chapters
          ? " · covered " + prev.chapters.join(", ").replace(/ch/g, "Ch ")
          : "");
      if (
        was !==
          formatSummary(next) + (next.notes ? ' ("' + next.notes + '")' : "") ||
        String(prev.chapters) !== String(next.chapters)
      )
        history = [{ at: prev.updated || C.todayKey(), summary: was }]
          .concat(history)
          .slice(0, 5);
    }
    next.history = history;
    delete ui.fmtEdit[key];
    ui.fmtOpen = "";
    ui.preview = null;
    updatePlan(function (p) {
      p.formats = p.formats || {};
      // A course-level format moves onto the exam once it has a date.
      formatKeys(course, exam, sid).forEach(function (k) {
        delete p.formats[k];
      });
      p.formats[key] = next;
      if (p.formatSkip) delete p.formatSkip[key];
    }, true);
    C.toast(
      (prev ? "Exam format updated" : "Exam format saved") +
        (plannedItems(sid).length
          ? ". Build the plan again to update planned sessions."
          : ""),
    );
  }
  function boot() {
    if (!window.__shougCal) return setTimeout(boot, 50);
    if (!$("study-plan-root")) return;
    C = window.__shougCal;
    $("study-plan-root").addEventListener("click", onClick);
    // Keep the "one day is different" list open across re-renders.
    $("study-plan-root").addEventListener(
      "toggle",
      function (ev) {
        if (!ev.target.classList) return;
        if (ev.target.classList.contains("sp-uni-except"))
          ui.uniExceptOpen = ev.target.open;
      },
      true,
    );
    // Once a time field is left, bring the rest of the tab up to date. The
    // delay lets a click on another control land before anything re-renders.
    $("study-plan-root").addEventListener("focusout", function (ev) {
      if (!ui.uniDirty || ev.target.type !== "time") return;
      setTimeout(function () {
        var a = document.activeElement;
        if (!ui.uniDirty || (a && a.type === "time" && a.closest(".sp-uni"))) return;
        ui.uniDirty = false;
        refreshAfterUni();
      }, 200);
    });
    $("study-plan-root").addEventListener("change", function (ev) {
      if (ev.target.dataset && (ev.target.dataset.spStudyDaily !== undefined || ev.target.dataset.spStudyWeekly !== undefined)) {
        var daily = ev.target.dataset.spStudyDaily !== undefined ? Number(ev.target.value) : studyLimits().daily;
        var weekly = ev.target.dataset.spStudyWeekly !== undefined ? (ev.target.value.trim() ? Number(ev.target.value) : 0) : studyLimits().weekly;
        if (!isFinite(daily) || daily < 1 || daily > 10 || !isFinite(weekly) || weekly < 0 || weekly > 70) { C.toast("Daily limit: 1–10 hours; weekly limit: up to 70 hours"); render(); return; }
        updatePlan(function (p) { p.studyLimits = { daily: daily, weekly: weekly }; }, true);
        if (seasonsWithPlan().length) rebuildPlans("Study time limit changed");
        else render();
        return;
      }
      var ud = ev.target.dataset && ev.target.dataset.spUni;
      if (ud) {
        var patch = {};
        patch[ev.target.dataset.f] = ev.target.value;
        saveUni(ud, patch, true);
        return;
      }
      if (ev.target.dataset && ev.target.dataset.spUniUsual) {
        setUniUsual(ev.target.dataset.spUniUsual, ev.target.value);
        return;
      }
      if (ev.target.dataset && ev.target.dataset.spUniDay) {
        setUniDay(ev.target.dataset.spUniDay, ev.target.checked);
        return;
      }
      if (!ev.target.hasAttribute("data-sp-commute")) return;
      var v = Math.round(Number(ev.target.value));
      if (!isFinite(v) || v < 0 || v > 240) {
        C.toast("Enter the drive in minutes, 0 to 240");
        ev.target.value = commute();
        return;
      }
      updatePlan(function (p) {
        p.commute = v;
      }, true);
      refreshAfterUni("Drive time changed");
    });
    $("study-plan-root").addEventListener("submit", function (ev) {
      if (ev.target.hasAttribute("data-sp-block-form")) {
        ev.preventDefault();
        addBlock(ev.target);
        return;
      }
      var form = ev.target.closest("[data-sp-format-form]");
      if (!form) return;
      ev.preventDefault();
      saveFormat(form);
    });
    // Enter in "another question type" adds it instead of saving the form.
    $("study-plan-root").addEventListener("keydown", function (ev) {
      if (ev.key === "Enter" && ev.target.hasAttribute("data-sp-type-input")) {
        ev.preventDefault();
        addCustomType(ev.target.closest("form"));
      }
    });
    // Ticks the question types it recognises in what was typed.
    $("study-plan-root").addEventListener("input", function (ev) {
      if (ev.target.name !== "notes") return;
      var form = ev.target.closest("[data-sp-format-form]"),
        found = detectFormats(ev.target.value);
      if (!form) return;
      found.forEach(function (id) {
        var box = form.querySelector('input[name="type"][value="' + id + '"]');
        if (box) box.checked = true;
      });
      form.querySelector(".sp-fmt-detect").textContent = found.length
        ? "Picked up: " +
          found
            .map(function (id) {
              return formatInfo(id).label;
            })
            .join(", ")
        : "";
    });
    $("study-plan-root").addEventListener("keydown", function (ev) {
      var card = ev.target.closest && ev.target.closest("[data-sp-course]");
      if (
        card &&
        ev.target === card &&
        (ev.key === "Enter" || ev.key === " ")
      ) {
        ev.preventDefault();
        card.click();
      }
    });
    render();
  }
  window.__shougStudyPlan = {
    render: render,
    replan: replan,
    overlaps: overlaps,
    examChapters: examChapters,
    deleteAll: deleteAll,
    startOver: startOver,
  };
  boot();
})();
