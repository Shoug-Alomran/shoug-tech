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
 *    needs per day left, and raises the daily cap until everything fits.
 *    Sessions are saved as Study events (planSource "study-plan").
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
    { id: "quiz", label: "Quizzes", noun: "Quiz", types: ["quiz", "bonus-quiz"] },
    { id: "midterm", label: "Midterms", noun: "Midterm", types: ["midterm"] },
    { id: "final", label: "Finals", noun: "Final", types: ["final"] },
  ];
  var LEVELS = ["New", "Shaky", "Solid"];
  // Share of an item's study time still needed at each readiness level.
  var FACTOR = [1, 0.55, 0.15];
  var DAY_START = 9 * 60,
    DAY_END = 22 * 60,
    BUFFER = 15,
    MAX_SESSION = 90,
    MIN_SESSION = 30,
    START_CAP = 240,
    MAX_CAP = 600,
    REVIEW_GAP = 3;
  var KIND_ORDER = ["calc", "formula", "number", "list", "process", "compare", "concept"];
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

  var index = null,
    files = {},
    pending = {},
    localPlan = null,
    saveTimer = null,
    ui = { course: "", preview: null, drill: true, revealed: {}, open: {} };

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

  function plan() {
    return localPlan || C.studyPlan || {};
  }
  // Readiness taps save after a short pause so a run of taps is one write.
  function updatePlan(mutate, now) {
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
    render();
  }
  function season() {
    var s = plan().season;
    return SEASONS.some(function (x) {
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
    return Number(r[unit]) || 0;
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
      return a.localeCompare(b);
    });
  }
  function daysUntil(k) {
    return Math.round((C.fromKey(k) - C.fromKey(C.todayKey())) / 86400000);
  }

  // ── Scope and remaining work ──────────────────────────────────────────
  function scopeIds(a, exam) {
    var s = exam && (plan().scope || {})[exam.id];
    var all = a.chapters.map(function (c) {
      return c.id;
    });
    if (!Array.isArray(s) || !s.length) return all;
    return all.filter(function (id) {
      return s.indexOf(id) > -1;
    });
  }
  function chapterItems(a, chId) {
    return (a.items || []).filter(function (i) {
      return i.chapter === chId;
    });
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
      left = 0;
    a.chapters.forEach(function (ch) {
      if (ids.indexOf(ch.id) < 0) return;
      total += ch.minutes;
      left += chapterLeft(course, a, ch);
    });
    return {
      total: total,
      left: left,
      ready: total ? Math.round((1 - left / total) * 100) : 0,
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
      reviews = {};
    a.chapters.forEach(function (ch) {
      if (ids.indexOf(ch.id) < 0) return;
      var left = chapterLeft(course, a, ch);
      if (left < 15) return;
      var n = Math.ceil(left / MAX_SESSION),
        part = Math.max(MIN_SESSION, round15(left / n)),
        name = course + " " + noun + " · " + chapterName(ch),
        focus = chapterItems(a, ch.id)
          .filter(function (i) {
            return level(course, a, i.id) < 2;
          })
          .sort(function (x, y) {
            return y.score - x.score;
          })
          .slice(0, 5)
          .map(function (i) {
            return i.name;
          });
      for (var k = 0; k < n; k++)
        learn.push({
          kind: "learn",
          chapter: ch.id,
          last: k === n - 1,
          minutes: part,
          title: name + (k ? " (continued)" : ""),
          notes: focus.length ? "Focus: " + focus.join("; ") : "",
        });
      reviews[ch.id] = {
        kind: "review",
        chapter: ch.id,
        minutes: 30,
        notBefore: null,
        title: course + " " + noun + " · Review " + chapterName(ch),
        notes: "Active recall: close the slides, write what you remember, then check.",
      };
    });
    return {
      learn: learn,
      reviews: reviews,
      final: learn.length
        ? {
            kind: "final",
            minutes: a.curated ? 120 : 90,
            title: course + " " + noun + " · Final review",
            notes: a.curated
              ? "Formulas, key numbers and lists from the memorize sheet, then one timed problem of each type."
              : "Skim every chapter's slides and redo anything marked Shaky.",
          }
        : null,
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
      // The plan being rebuilt doesn't block itself.
      if (raw && raw.planSource === "study-plan" && raw.planSeason === sid)
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
    return { all: all, busy: busy };
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
  function attempt(jobs, days, sid, cap, startToday, spread) {
    var placed = [];
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
    days.forEach(function (day, di) {
      var startMin = di === 0 ? startToday : DAY_START,
        slots = freeSlots(day, sid, startMin),
        used = 0;
      function take(len) {
        for (var i = 0; i < slots.length; i++) {
          if (slots[i][1] - slots[i][0] >= len) {
            var st = slots[i][0];
            slots[i] = [st + len + BUFFER, slots[i][1]];
            used += len;
            return st;
          }
        }
        return null;
      }
      function biggest() {
        return slots.reduce(function (m, s) {
          return Math.max(m, s[1] - s[0]);
        }, 0);
      }
      function put(j, sess, len) {
        var st = take(len);
        if (st === null) return false;
        placed.push({
          exam: j.exam,
          course: j.course,
          date: day,
          start: C.toTime(st),
          end: C.toTime(st + len),
          minutes: len,
          kind: sess.kind,
          title:
            sess.title + (sess.cont && !/\(continued\)$/.test(sess.title) ? " (continued)" : ""),
          notes: sess.notes,
        });
        return true;
      }
      // The day before an exam opens with its final review.
      jobs.forEach(function (j) {
        if (j.fin && j.lastDay === day && put(j, j.fin, j.fin.minutes))
          j.fin = null;
      });
      // A course with nothing placeable today (only reviews not yet due)
      // sits out the rest of the day instead of ending it for everyone.
      var resting = [];
      jobs.forEach(function (j) {
        j.today = 0;
        var left =
          Math.round((C.fromKey(j.lastDay) - C.fromKey(day)) / 86400000) + 1;
        // The last three days before an exam have no per-course limit.
        j.limit =
          left <= 3
            ? Infinity
            : Math.max(60, Math.ceil(((pendingMin(j) / Math.max(1, left)) * spread) / 15) * 15);
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
          var u = p / left;
          if (u > bestU) {
            bestU = u;
            best = j;
          }
        });
        if (!best) break;
        var room = Math.min(cap - used, biggest(), best.limit - best.today);
        if (room < MIN_SESSION) break;
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
          // Reviews of chapters this plan never studied (all Solid) drop.
          var unstudied = waiting.filter(function (k) {
            return !best.rev[k].notBefore;
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
        var len = Math.min(sess.minutes, Math.floor(room / 15) * 15);
        if (len < MIN_SESSION) len = Math.min(sess.minutes, room);
        if (len < 15 || !put(best, sess, len)) {
          resting.push(best);
          continue;
        }
        best.today += len;
        if (len < sess.minutes) {
          sess.cont = true;
          sess.minutes -= len;
          if (sess.minutes < 15) sess.minutes = 15;
          continue;
        }
        if (reviewId) delete best.rev[reviewId];
        else {
          best.q.shift();
          if (sess.last && best.rev[sess.chapter]) {
            var nb = C.addDays(day, REVIEW_GAP);
            if (nb > best.lastDay) nb = best.lastDay;
            best.rev[sess.chapter].notBefore = nb;
          }
        }
      }
    });
    var short = 0;
    jobs.forEach(function (j) {
      j.left = pendingMin(j) + (j.fin ? j.fin.minutes : 0);
      short += j.left;
    });
    return { placed: placed, short: short };
  }
  function buildSchedule(sid) {
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
      jobs.push({ course: course, exam: exam, a: a, s: sessionsFor(course, a, exam, sid) });
    });
    if (!jobs.length) return { jobs: [], placed: [], skipped: skipped };
    var lastDay = jobs.reduce(function (m, j) {
        var d = C.addDays(j.exam.date, -1);
        return d > m ? d : m;
      }, first),
      days = [];
    for (var d = first; d <= lastDay; d = C.addDays(d, 1)) days.push(d);
    var cap = START_CAP,
      spread = 1.25,
      res = attempt(jobs, days, sid, cap, startToday, spread);
    while (res.short > 0 && cap < MAX_CAP) {
      if (spread < 2) spread += 0.25;
      else cap += 60;
      res = attempt(jobs, days, sid, cap, startToday, spread);
    }
    res.placed.sort(function (x, y) {
      return (x.date + x.start).localeCompare(y.date + y.start);
    });
    return {
      jobs: jobs.map(function (j) {
        var need = 0;
        j.s.learn.forEach(function (x) {
          need += x.minutes;
        });
        Object.keys(j.s.reviews).forEach(function (k) {
          need += j.s.reviews[k].minutes;
        });
        if (j.s.final) need += j.s.final.minutes;
        return { course: j.course, exam: j.exam, need: need, left: j.left };
      }),
      placed: res.placed,
      cap: cap,
      short: res.short,
      first: first,
      skipped: skipped,
    };
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
  function commitPreview() {
    var sid = season(),
      pv = ui.preview;
    if (!pv || !pv.placed.length) return;
    if (!C.signedIn) {
      C.toast("Sign in to save your study plan");
      return;
    }
    removePlanned(sid);
    pv.placed.forEach(function (p) {
      C.items.push({
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
      });
    });
    var n = pv.placed.length;
    ui.preview = null;
    C.persist().then(function () {
      C.renderAll();
      C.toast(n + " study session" + (n === 1 ? "" : "s") + " added to your calendar");
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
  function headHtml(sid) {
    return (
      '<div class="panel-head sp-head"><div><div class="panel-title">Study Plan</div>' +
      '<div class="panel-sub">Your registered courses, your exam dates and what each course\'s slides actually contain</div></div>' +
      '<div class="sp-season" role="tablist" aria-label="Exam season">' +
      SEASONS.map(function (s) {
        return (
          '<button type="button" role="tab" data-sp-season="' +
          s.id +
          '" aria-selected="' +
          (s.id === sid) +
          '">' +
          s.label +
          "</button>"
        );
      }).join("") +
      "</div></div>"
    );
  }
  function examCardsHtml(sid, courses) {
    var noun = seasonInfo(sid).noun;
    if (!courses.length)
      return '<div class="empty">Add your classes on the calendar first. The plan uses your registered courses.</div>';
    return (
      '<div class="sp-exams">' +
      courses
        .map(function (course) {
          var exam = examFor(course, sid),
            a = analysis(course, sid),
            sel = course === ui.course,
            body;
          if (!exam)
            body =
              '<div class="sp-exam-when muted">No ' +
              noun.toLowerCase() +
              ' date yet</div><button class="mini-btn" type="button" data-sp-add-exam="' +
              esc(course) +
              '">Add ' +
              noun.toLowerCase() +
              " date</button>";
          else {
            var d = daysUntil(exam.date),
              prog = a ? courseProgress(course, a, exam) : null;
            body =
              '<div class="sp-exam-when">' +
              esc(examLabel(exam)) +
              '</div><div class="sp-exam-days"><b>' +
              d +
              "</b> day" +
              (d === 1 ? "" : "s") +
              " left</div>" +
              (prog
                ? bar(prog.ready) +
                  '<div class="sp-exam-meta">' +
                  prog.ready +
                  "% ready · " +
                  hours(prog.left) +
                  " to go</div>"
                : '<div class="sp-exam-meta">' +
                  (a === undefined ? "Loading analysis..." : "No slide analysis yet") +
                  "</div>");
          }
          return (
            '<div class="sp-exam' +
            (sel ? " selected" : "") +
            (exam && daysUntil(exam.date) <= 7 ? " soon" : "") +
            '"><button class="sp-exam-pick" type="button" data-sp-course="' +
            esc(course) +
            '" aria-pressed="' +
            sel +
            '">' +
            esc(course) +
            "</button>" +
            body +
            "</div>"
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
      var gap = Math.round((C.fromKey(ex[i].date) - C.fromKey(ex[i - 1].date)) / 86400000);
      if (gap <= 1)
        out.push(
          esc(C.courseLabel(ex[i - 1].course)) +
            " and " +
            esc(C.courseLabel(ex[i].course)) +
            (gap ? " are on back-to-back days" : " are on the same day"),
        );
    }
    return out.length
      ? '<div class="sp-note warn">' + out.join(". ") + ". The day before the first one goes to its final review, so the second one's final review comes after the first exam ends.</div>"
      : "";
  }
  function plannerHtml(sid) {
    var ex = seasonExams(sid),
      noun = seasonInfo(sid).noun.toLowerCase(),
      planned = plannedItems(sid),
      pv = ui.preview,
      out = '<div class="sp-card sp-planner"><div class="sp-card-head"><h3>Schedule</h3>';
    if (!ex.length)
      return (
        out +
        '</div><div class="empty">No upcoming ' +
        noun +
        "s on your calendar. Add the dates and the plan will fill your free time before each one.</div></div>"
      );
    out +=
      '<div class="sp-actions"><button class="btn solid" type="button" data-sp-build>' +
      (planned.length ? "Re-plan" : "Build schedule") +
      "</button>" +
      (planned.length
        ? '<button class="btn muted" type="button" data-sp-clear>Remove planned sessions</button>'
        : "") +
      "</div></div>";
    if (planned.length && !pv) {
      var next = planned.slice().sort(function (x, y) {
        return (x.date + x.start).localeCompare(y.date + y.start);
      })[0];
      out +=
        '<p class="sp-muted">' +
        planned.length +
        " study session" +
        (planned.length === 1 ? " is" : "s are") +
        " on your calendar. Next: <b>" +
        esc(next.title) +
        "</b>, " +
        esc(C.prettyDate(next.date).replace(/, \d{4}$/, "")) +
        " at " +
        esc(C.timeLabel(next.start)) +
        ". Mark items Solid as you go and re-plan whenever you fall behind or finish early.</p>";
    } else if (!pv)
      out +=
        '<p class="sp-muted">Builds learn sessions chapter by chapter, a review three days after each chapter, and a final review the day before each exam, all in your free time between 9 AM and 10 PM around classes, exams and events.</p>';
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
                ? '<span class="sp-warn">' + hours(j.left) + " doesn't fit</span>"
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
          ? "Even at " +
            pv.cap / 60 +
            " h a day there isn't enough free time before these exams. Free up evenings or weekends, or mark items you already know as Solid."
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
            (pv.cap > START_CAP ? " (the plan had to go above 4 h a day to fit everything)" : "") +
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
          ? '<span class="sp-muted">Replaces the ' + planned.length + " planned session" + (planned.length === 1 ? "" : "s") + " from today on.</span>"
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
        '<div class="sp-card"><h3>Finishing the course safely</h3><p class="sp-muted">Final is worth ' +
        esc(w) +
        "% of the grade. Add your quiz, major and assignment marks under Grades &amp; GPA to see exactly what you need on the final.</p></div>"
      );
    var chips = n.needs
      .slice()
      .reverse()
      .map(function (x) {
        var cls =
          x.marks <= 0 ? "secured" : x.percent > 100 ? "gone" : x.percent >= 85 ? "hard" : x.percent >= 65 ? "stretch" : "";
        return (
          '<span class="sp-need ' +
          cls +
          '"><b>' +
          esc(x.letter) +
          "</b>" +
          (x.marks <= 0
            ? "secured"
            : x.percent > 100
              ? "out of reach"
              : Math.ceil(x.marks * 10) / 10 + "/" + n.fw + " (" + Math.ceil(x.percent) + "%)") +
          "</span>"
        );
      })
      .join("");
    var pass = n.needs.find(function (x) {
      return x.letter === "D";
    });
    return (
      '<div class="sp-card"><h3>Finishing the course safely</h3><p class="sp-muted">Coursework so far: <b>' +
      Math.round(n.cw * 10) / 10 +
      "</b> of " +
      n.cwMax +
      " (" +
      Math.round(n.cwUsed) +
      "% of it graded" +
      (n.cwComplete ? "" : ", so these are based on what's entered") +
      "). " +
      (pass && pass.marks > 0
        ? "To pass you need <b>" + Math.ceil(pass.marks * 10) / 10 + " of " + n.fw + "</b> on the final."
        : "You've already passed the course on coursework.") +
      '</p><div class="sp-needs">' +
      chips +
      "</div></div>"
    );
  }
  function statsHtml(a) {
    var t = a.totals,
      k = t.kinds || {},
      tiles = [
        ["Chapters", t.chapters],
        ["Slides", t.slides],
        ["Study time", hours(t.minutes)],
      ];
    if (a.curated)
      tiles = tiles.concat([
        ["Concepts and topics", t.items],
        ["Formulas", k.formula],
        ["Key numbers", k.number],
        ["Lists to memorize", k.list],
        ["Problem types", k.calc],
        ["Comparisons", k.compare],
      ]);
    if (a.syllabus && a.syllabus.final_weight)
      tiles.push(["Final weight", a.syllabus.final_weight + "%"]);
    return (
      '<div class="sp-stats">' +
      tiles
        .map(function (x) {
          return (
            '<div class="sp-stat"><b>' +
            esc(x[1] === undefined ? 0 : x[1]) +
            "</b><span>" +
            esc(x[0]) +
            "</span></div>"
          );
        })
        .join("") +
      "</div>"
    );
  }
  function itemById(a, id) {
    return a.items.find(function (i) {
      return i.id === id;
    });
  }
  function repeatedHtml(a) {
    if (!a.curated || !a.repeated) return "";
    var list = a.repeated.map(function (id) {
        return itemById(a, id);
      }),
      max = list[0] ? list[0].slides : 1;
    return (
      '<div class="sp-card"><h3>Most repeated across the slides</h3><p class="sp-muted">Slides that mention each topic. The more a topic comes back, the safer a bet it is for the exam.</p><div class="sp-rep">' +
      list
        .map(function (i) {
          return (
            '<div class="sp-rep-row"><span>' +
            esc(i.name) +
            "</span>" +
            bar((i.slides / max) * 100, "thin") +
            "<em>" +
            i.slides +
            " slides · " +
            i.decks +
            " deck" +
            (i.decks === 1 ? "" : "s") +
            "</em></div>"
          );
        })
        .join("") +
      "</div></div>"
    );
  }
  function memorizeHtml(course, a) {
    if (!a.curated) return "";
    var groups = ["formula", "number", "list"];
    var count = a.items.filter(function (i) {
      return groups.indexOf(i.kind) > -1;
    }).length;
    return (
      '<div class="sp-card"><div class="sp-card-head"><h3>Memorize sheet · ' +
      count +
      ' items</h3><label class="filter-toggle"><input type="checkbox" data-sp-drill' +
      (ui.drill ? " checked" : "") +
      "> Drill mode</label></div>" +
      '<p class="sp-muted">' +
      (ui.drill
        ? "Answers are hidden. Say each one out loud, then tap to check."
        : "Everything you need word for word.") +
      "</p>" +
      groups
        .map(function (g) {
          var its = a.items.filter(function (i) {
            return i.kind === g;
          });
          if (!its.length) return "";
          return (
            '<h4 class="sp-sub">' +
            esc(a.kind_labels[g]) +
            " (" +
            its.length +
            ")</h4><div class=\"sp-mem\">" +
            its
              .map(function (i) {
                var hidden = ui.drill && !ui.revealed[i.id];
                return (
                  '<button type="button" class="sp-mem-row' +
                  (hidden ? " hidden-answer" : "") +
                  '" data-sp-reveal="' +
                  esc(i.id) +
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
      "</div>"
    );
  }
  function levelButtons(unit, lv) {
    return (
      '<span class="sp-level" role="group" aria-label="Readiness">' +
      LEVELS.map(function (l, n) {
        return (
          '<button type="button" data-sp-level="' +
          n +
          '" data-sp-unit="' +
          esc(unit) +
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
  function chaptersHtml(course, a, exam) {
    var ids = scopeIds(a, exam);
    return (
      '<div class="sp-card"><div class="sp-card-head"><h3>Chapters</h3>' +
      (exam ? '<span class="sp-muted">Untick chapters this exam doesn\'t cover</span>' : "") +
      "</div>" +
      a.chapters
        .map(function (ch) {
          var inScope = ids.indexOf(ch.id) > -1,
            left = chapterLeft(course, a, ch),
            ready = ch.minutes ? Math.round((1 - left / ch.minutes) * 100) : 0,
            its = chapterItems(a, ch.id),
            open = ui.open[ch.id];
          var head =
            '<div class="sp-ch' +
            (inScope ? "" : " out") +
            '"><div class="sp-ch-main">' +
            (exam
              ? '<input type="checkbox" data-sp-scope="' +
                esc(ch.id) +
                '" aria-label="Include ' +
                esc(ch.title) +
                '"' +
                (inScope ? " checked" : "") +
                ">"
              : "") +
            '<div><div class="sp-ch-title">' +
            esc(ch.title) +
            '</div><div class="sp-ch-meta">' +
            ch.slides +
            " slides" +
            (its.length ? " · " + its.length + " items" : "") +
            " · " +
            hours(left) +
            " of " +
            hours(ch.minutes) +
            " left" +
            (ch.syllabus_share ? " · " + Math.round(ch.syllabus_share * 100) + "% of class time" : "") +
            "</div>" +
            bar(ready, "thin") +
            "</div></div><div class=\"sp-ch-side\">" +
            (a.curated
              ? '<button type="button" class="mini-btn" data-sp-open="' +
                esc(ch.id) +
                '" aria-expanded="' +
                Boolean(open) +
                '">' +
                (open ? "Hide items" : "Show items") +
                "</button>"
              : levelButtons("ch:" + ch.id, level(course, a, "ch:" + ch.id))) +
            "</div></div>";
          var links = (ch.links || []).length
            ? '<div class="sp-links">' +
              ch.links
                .map(function (l) {
                  return '<a href="' + esc(l.url) + '">' + esc(l.label) + "</a>";
                })
                .join("") +
              "</div>"
            : "";
          var body =
            a.curated && open
              ? '<div class="sp-items">' +
                its
                  .slice()
                  .sort(function (x, y) {
                    return KIND_ORDER.indexOf(x.kind) - KIND_ORDER.indexOf(y.kind) || y.score - x.score;
                  })
                  .map(function (i) {
                    var lv = level(course, a, i.id);
                    return (
                      '<div class="sp-item l' +
                      lv +
                      '"><div><div class="sp-item-name"><span class="sp-tier ' +
                      i.tier +
                      '">' +
                      esc(TIER_LABEL[i.tier] || i.tier) +
                      '</span><span class="sp-kind">' +
                      esc(KIND_ONE[i.kind] || i.kind) +
                      "</span>" +
                      esc(i.name) +
                      '</div><div class="sp-item-meta">' +
                      i.slides +
                      " slide" +
                      (i.slides === 1 ? "" : "s") +
                      (i.decks > 1 ? " across " + i.decks + " decks" : "") +
                      (i.practice ? " · in " + i.practice + " practice question" + (i.practice === 1 ? "" : "s") : "") +
                      " · " +
                      i.minutes +
                      " min</div>" +
                      (i.memorize
                        ? '<div class="sp-item-mem">' + esc(i.memorize) + "</div>"
                        : "") +
                      "</div>" +
                      levelButtons(i.id, lv) +
                      "</div>"
                    );
                  })
                  .join("") +
                links +
                "</div>"
              : !a.curated
                ? links
                : "";
          return head + body;
        })
        .join("") +
      "</div>"
    );
  }
  function styleHtml(a) {
    var parts = [];
    if (a.style && a.style.question_types)
      parts.push(
        '<div class="sp-card"><h3>How this instructor asks</h3><p class="sp-muted">From ' +
          esc(a.style.source) +
          '.</p><ul class="sp-list">' +
          a.style.question_types
            .map(function (q) {
              return "<li>" + esc(q) + "</li>";
            })
            .join("") +
          "</ul></div>",
      );
    if ((a.resources || []).length || (a.syllabus && a.syllabus.weights))
      parts.push(
        '<div class="sp-card"><h3>Grade weights and resources</h3>' +
          (a.syllabus && a.syllabus.weights
            ? '<ul class="sp-list">' +
              a.syllabus.weights
                .map(function (w) {
                  return "<li>" + esc(w.label) + " · <b>" + esc(w.percent) + "%</b></li>";
                })
                .join("") +
              "</ul>"
            : "") +
          ((a.resources || []).length
            ? '<div class="sp-links">' +
              a.resources
                .map(function (r) {
                  return '<a href="' + esc(r.url) + '">' + esc(r.label) + "</a>";
                })
                .join("") +
              "</div>"
            : "") +
          "</div>",
      );
    return parts.join("");
  }
  function courseHtml(course, sid) {
    var a = analysis(course, sid),
      exam = examFor(course, sid);
    if (a === undefined) return '<div class="empty">Loading the ' + esc(course) + " analysis...</div>";
    if (a === null)
      return (
        '<div class="sp-card"><h3>' +
        esc(course) +
        '</h3><p class="sp-muted">There\'s no slide analysis for this course yet, so it can\'t be planned. It needs its slides on the site first.</p></div>' +
        needsHtml(course, null)
      );
    var seasonNote =
      a.season !== sid
        ? '<div class="sp-note">This uses the final-exam analysis. Untick the chapters this ' +
          seasonInfo(sid).noun.toLowerCase() +
          " doesn't cover.</div>"
        : "";
    var syl = a.syllabus || {};
    return (
      '<div class="sp-course-head"><div><h3>' +
      esc(course) +
      (a.title ? " · " + esc(a.title) : "") +
      '</h3><p class="sp-muted">' +
      (a.curated
        ? "Full analysis of every slide deck: each concept, formula and problem type, counted slide by slide."
        : "Baseline analysis: slide counts and study time. Mark each chapter as you go; the concept breakdown isn't built for this course yet.") +
      (syl.scope_note && a.curated ? " " + esc(syl.scope_note) : "") +
      "</p></div>" +
      (a.course_page ? '<a class="mini-btn" href="' + esc(a.course_page) + '">Course page</a>' : "") +
      "</div>" +
      seasonNote +
      statsHtml(a) +
      '<div class="sp-grid">' +
      needsHtml(course, a) +
      repeatedHtml(a) +
      "</div>" +
      chaptersHtml(course, a, exam) +
      memorizeHtml(course, a) +
      '<div class="sp-grid">' +
      styleHtml(a) +
      "</div>"
    );
  }
  function render() {
    var root = $("study-plan-root");
    if (!root || !C) return;
    loadIndex();
    var sid = season(),
      courses = courseList(sid);
    if (!ui.course || courses.indexOf(ui.course) < 0) ui.course = courses[0] || "";
    var scrollY = window.scrollY;
    root.innerHTML =
      headHtml(sid) +
      '<div class="panel-body sp-body">' +
      examCardsHtml(sid, courses) +
      clashHtml(sid) +
      plannerHtml(sid) +
      (ui.course ? courseHtml(ui.course, sid) : "") +
      "</div>";
    if (Math.abs(window.scrollY - scrollY) > 2) window.scrollTo(0, scrollY);
  }

  // ── Events ────────────────────────────────────────────────────────────
  function onClick(ev) {
    var t = ev.target.closest("button, input");
    if (!t || !$("study-plan-root").contains(t)) return;
    var d = t.dataset;
    if (d.spSeason) {
      ui.preview = null;
      updatePlan(function (p) {
        p.season = d.spSeason;
      }, true);
    } else if (d.spCourse) {
      ui.course = d.spCourse;
      render();
    } else if (d.spAddExam !== undefined) {
      C.openExamEditor("", "", { course: d.spAddExam, type: season() === "quiz" ? "quiz" : season() });
    } else if (t.hasAttribute("data-sp-build")) {
      ui.preview = buildSchedule(season());
      render();
    } else if (t.hasAttribute("data-sp-commit")) commitPreview();
    else if (t.hasAttribute("data-sp-discard")) {
      ui.preview = null;
      render();
    } else if (t.hasAttribute("data-sp-clear")) clearPlanned();
    else if (d.spLevel !== undefined) {
      var a = analysis(ui.course, season());
      if (!a) return;
      var key = readyKey(ui.course, a),
        lv = Number(d.spLevel);
      ui.preview = null;
      updatePlan(function (p) {
        p.ready = p.ready || {};
        p.ready[key] = p.ready[key] || {};
        if (lv) p.ready[key][d.spUnit] = lv;
        else delete p.ready[key][d.spUnit];
      });
    } else if (d.spScope !== undefined) {
      var a2 = analysis(ui.course, season()),
        exam = examFor(ui.course, season());
      if (!a2 || !exam) return;
      var ids = scopeIds(a2, exam),
        on = t.checked;
      ids = on
        ? ids.concat([d.spScope])
        : ids.filter(function (x) {
            return x !== d.spScope;
          });
      if (!ids.length) {
        t.checked = true;
        C.toast("Keep at least one chapter in scope");
        return;
      }
      ui.preview = null;
      updatePlan(function (p) {
        p.scope = p.scope || {};
        p.scope[exam.id] = ids.length === a2.chapters.length ? [] : ids;
      });
    } else if (d.spOpen) {
      ui.open[d.spOpen] = !ui.open[d.spOpen];
      render();
    } else if (d.spReveal) {
      ui.revealed[d.spReveal] = !ui.revealed[d.spReveal];
      render();
    } else if (t.hasAttribute("data-sp-drill")) {
      ui.drill = t.checked;
      ui.revealed = {};
      render();
    }
  }

  function boot() {
    if (!window.__shougCal) return setTimeout(boot, 50);
    if (!$("study-plan-root")) return;
    C = window.__shougCal;
    $("study-plan-root").addEventListener("click", onClick);
    render();
  }
  window.__shougStudyPlan = { render: render };
  boot();
})();
