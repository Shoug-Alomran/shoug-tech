/**
 * Murshida (مرشدة, "advisor") — the schedule planner's course advisor, drawn
 * as Shoug in pixel-art game mode.
 *
 * Two jobs:
 *  1. "What to take": reads the student's saved academic plan (the plan grid's
 *     localStorage, or courses they type in), then suggests courses offered
 *     this term whose prerequisites and credit-hour minimums are met, earliest
 *     plan term first, then the ones that unlock the most later courses.
 *  2. "About your picks": warnings and advice on the courses and the schedule
 *     on screen — prerequisites, clashes, credit hours, difficulty from
 *     student ratings, exam weight from the syllabus, related courses,
 *     scarce sections, long days, gaps and crowded finals.
 *
 * Reads window.SchedulePlanner.context(); the planner calls Murshida.update().
 */
(function () {
  "use strict";

  // Key keeps the pre-rename name so visitors keep their saved advisor state.
  var STORE = "shoug_murshid_v1";
  // Plan grid storage keys → plan folder under /academic-plan-themes/ and Edugate department code.
  var PLANS = {
    se: {
      key: "shoug_academic_plan_grid_se_v1",
      dept: "SE",
      label: "Software Engineering",
      labelAr: "هندسة البرمجيات",
    },
    "se-cys": {
      key: "shoug_academic_plan_grid_v4",
      dept: "SE-CYS",
      label: "Software Engineering (Cybersecurity)",
      labelAr: "هندسة البرمجيات (الأمن السيبراني)",
    },
    "se-ai": {
      key: "shoug_academic_plan_grid_se_ai_v1",
      dept: "SE-AI&DS",
      label: "Software Engineering (AI & Data Science)",
      labelAr: "هندسة البرمجيات (الذكاء الاصطناعي وعلم البيانات)",
    },
    "se-dx": {
      key: "shoug_academic_plan_grid_se_dx_v1",
      dept: "SE-DX",
      label: "Software Engineering (Digital Transformation)",
      labelAr: "هندسة البرمجيات (التحول الرقمي)",
    },
    cs: {
      key: "shoug_academic_plan_grid_cs_v1",
      dept: "CS",
      label: "Computer Science",
      labelAr: "علوم الحاسب",
    },
    "cs-cys": {
      key: "shoug_academic_plan_grid_cs_cys_v1",
      dept: "CS-CYS",
      label: "Computer Science (Cybersecurity)",
      labelAr: "علوم الحاسب (الأمن السيبراني)",
    },
    "cs-ai": {
      key: "shoug_academic_plan_grid_cs_ai_v1",
      dept: "CS-AI&DS",
      label: "Computer Science (AI & Data Science)",
      labelAr: "علوم الحاسب (الذكاء الاصطناعي وعلم البيانات)",
    },
    "cs-dx": {
      key: "shoug_academic_plan_grid_cs_dx_v1",
      dept: "CS-DX",
      label: "Computer Science (Digital Transformation)",
      labelAr: "علوم الحاسب (التحول الرقمي)",
    },
    "is-ai": {
      key: "shoug_academic_plan_grid_is_ai_v1",
      dept: "IS-AI&DS",
      label: "Information Systems (AI & Data Science)",
      labelAr: "نظم المعلومات (الذكاء الاصطناعي وعلم البيانات)",
    },
  };
  function isAr() {
    return (
      String(document.documentElement.lang || "")
        .toLowerCase()
        .indexOf("ar") === 0
    );
  }
  function L(en, ar) {
    return isAr() ? ar : en;
  }
  var STOP =
    "introduction intro fundamentals fundamental basics basic overview review part parts chapter concepts concept principles principle using with from into their your what that this and the for are management advanced applications application methods method topics systems system data software computer computing course study case managing working understanding development including other".split(
      " ",
    );

  // Murshida is Shoug in game mode: a 32×32 pixel avatar with long black
  // side-swept hair, plum cat-eye glasses, gold earrings and necklace and a
  // purple V-neck. One character per pixel; "." is transparent. Eyes, mouth
  // and extras are layers, so she can react (see MOODS and react()).
  var PIXEL_ROWS = [
    "................................",
    "...........KKKKKKKKKK...........",
    ".........KKKKKKKKKKKKKK.........",
    ".......KKKHHKKKKKKKKKKKKK.......",
    "......KKKHHKKKKKKKKKHKKKKK......",
    ".....KKKHHKKKKKKKKKKKHHKKKK.....",
    ".....KKHKKKKKKKKKKKKKKKHKKK.....",
    "....KKHKKKKKKKKKKKKKKKKKKKKK....",
    "....KKHKKKKKKKKKKKKKKSSSKKKK....",
    "....KHKKKKKKKKKKKKKSSSSSKKKK....",
    "....KKKKKKKKKKKKKSSSSSSSKKKK....",
    "....KKKKKKKKKSSSSSSSSSSSKKKK....",
    "....KKKKGSSSSSSSSSSSSSSGKKKK....",
    "....KKKKGGGGGGGSSGGGGGGGKKKK....",
    "....KhKKGEEELLGGGGLLEEEGKKhK....",
    "....KKhKGLLLLLGSSGLLLLLGKhKK....",
    "....KhKKGLLLLLGSSGLLLLLGKKhK....",
    "....KKhKSGGGGGGSSGGGGGGSKhKK....",
    "....KhKYSSSSSSSssSSSSSSSYKhK....",
    "....KKhYSSSSSSSSSSSSSSSSYhKK....",
    "....KhKYsSSSSSSSSSSSSSSsYKhK....",
    "....KKhKKsSSSSSSSSSSSSsKKhKK....",
    "....KhKKKKKsSSSSSSSSsKKKKKhK....",
    "....KKhKKKK..sSSSSs..KKKKhKK....",
    "....KhKKKKK..sSSSSs..KKKKKhK....",
    "...KKKhKKPPPPYSSSSYPPPPKKhKKK...",
    "..KKKhKKPPpPPPYSSYPPPpPPKKhKKK..",
    "..KKKKhPPpPPPPPYYPPPPPpPPhKKKK..",
    "..KKKhPPpPPPPPPPPPPPPPPpPPhKKK..",
    "..KKKPhpPPPPPPPPPPPPPPPPphPKKK..",
    "..PPPPpPPPPPQQQQQQQQPPPPPpPPPP..",
    "..PPPPPPPPPQQQQQQQQQQPPPPPPPPP..",
  ];
  var PIXEL_COLORS = {
    K: "#15111b",
    H: "#4d4163",
    h: "#2c2439",
    S: "#f2c6a4",
    s: "#dca684",
    G: "#5a1f52",
    L: "#f1e6ff",
    E: "#1a1220",
    W: "#ffffff",
    B: "#f59bb0",
    M: "#d2466e",
    m: "#f79ab4",
    P: "#8b2fc9",
    p: "#6a1fa0",
    Q: "#a955e0",
    Y: "#f4c542",
    R: "#ff4f86",
    D: "#7cc8ff",
    T: "#8b7d9e",
  };
  // [row, column, colour] cells drawn on top of the face.
  var PIXEL_LAYERS = {
    "e-open": [
      [15, 11, "E"],
      [15, 12, "E"],
      [16, 11, "E"],
      [16, 12, "E"],
      [15, 19, "E"],
      [15, 20, "E"],
      [16, 19, "E"],
      [16, 20, "E"],
      [15, 11, "W"],
      [15, 19, "W"],
    ],
    "e-happy": [
      [16, 10, "E"],
      [15, 11, "E"],
      [16, 12, "E"],
      [16, 19, "E"],
      [15, 20, "E"],
      [16, 21, "E"],
    ],
    "e-wink": [
      [15, 11, "E"],
      [15, 12, "E"],
      [16, 11, "E"],
      [16, 12, "E"],
      [15, 11, "W"],
      [16, 19, "E"],
      [16, 20, "E"],
      [16, 21, "E"],
    ],
    "m-smile": [
      [19, 13, "M"],
      [19, 18, "M"],
      [20, 14, "M"],
      [20, 15, "M"],
      [20, 16, "M"],
      [20, 17, "M"],
      [20, 16, "m"],
    ],
    "m-grin": [
      [19, 13, "M"],
      [19, 14, "W"],
      [19, 15, "W"],
      [19, 16, "W"],
      [19, 17, "W"],
      [19, 18, "M"],
      [20, 14, "M"],
      [20, 15, "M"],
      [20, 16, "M"],
      [20, 17, "M"],
    ],
    "m-frown": [
      [19, 14, "M"],
      [19, 15, "M"],
      [19, 16, "M"],
      [19, 17, "M"],
      [20, 13, "M"],
      [20, 18, "M"],
    ],
    "m-o": [
      [19, 15, "M"],
      [19, 16, "M"],
      [20, 15, "M"],
      [20, 16, "M"],
    ],
    "m-flat": [
      [20, 14, "M"],
      [20, 15, "M"],
      [20, 16, "M"],
      [20, 17, "M"],
    ],
    "x-blush": [
      [18, 9, "B"],
      [18, 10, "B"],
      [18, 21, "B"],
      [18, 22, "B"],
    ],
    "x-sparkle": [
      [9, 2, "Y"],
      [10, 1, "Y"],
      [10, 2, "Y"],
      [10, 3, "Y"],
      [11, 2, "Y"],
      [3, 28, "Y"],
      [4, 27, "Y"],
      [4, 28, "Y"],
      [4, 29, "Y"],
      [5, 28, "Y"],
    ],
    "x-heart": [
      [1, 27, "R"],
      [1, 29, "R"],
      [2, 26, "R"],
      [2, 27, "R"],
      [2, 28, "R"],
      [2, 29, "R"],
      [2, 30, "R"],
      [3, 27, "R"],
      [3, 28, "R"],
      [3, 29, "R"],
      [4, 28, "R"],
    ],
    "x-sweat": [
      [9, 29, "D"],
      [10, 28, "D"],
      [10, 29, "D"],
      [11, 28, "D"],
      [11, 29, "D"],
    ],
    "x-alert": [
      [0, 28, "K"],
      [0, 29, "K"],
      [0, 30, "K"],
      [1, 28, "K"],
      [1, 29, "K"],
      [1, 30, "K"],
      [2, 28, "K"],
      [2, 29, "K"],
      [2, 30, "K"],
      [3, 28, "K"],
      [3, 29, "K"],
      [3, 30, "K"],
      [4, 28, "K"],
      [4, 29, "K"],
      [4, 30, "K"],
      [0, 29, "Y"],
      [1, 29, "Y"],
      [2, 29, "Y"],
      [3, 29, "Y"],
      [6, 28, "K"],
      [6, 29, "K"],
      [6, 30, "K"],
      [7, 28, "K"],
      [7, 29, "K"],
      [7, 30, "K"],
      [8, 28, "K"],
      [8, 29, "K"],
      [8, 30, "K"],
      [7, 29, "Y"],
    ],
    "x-think": [
      [2, 25, "T"],
      [2, 26, "T"],
      [3, 25, "T"],
      [3, 26, "T"],
      [2, 28, "T"],
      [2, 29, "T"],
      [3, 28, "T"],
      [3, 29, "T"],
      [2, 31, "T"],
      [3, 31, "T"],
    ],
  };
  var MOODS = {
    happy: ["e-open", "m-smile", "x-blush"],
    alarm: ["e-open", "m-o", "x-alert"],
    think: ["e-open", "m-flat", "x-think"],
    sad: ["e-open", "m-frown", "x-sweat"],
    love: ["e-wink", "m-grin", "x-heart", "x-blush"],
    celebrate: ["e-happy", "m-grin", "x-sparkle", "x-blush"],
  };

  function rects(cells) {
    var byRow = {},
      out = "";
    cells.forEach(function (c) {
      (byRow[c[0]] = byRow[c[0]] || []).push(c);
    });
    Object.keys(byRow).forEach(function (y) {
      var row = byRow[y].sort(function (p, q) {
        return p[1] - q[1];
      });
      for (var i = 0; i < row.length;) {
        var run = 1;
        while (
          i + run < row.length &&
          row[i + run][1] === row[i][1] + run &&
          row[i + run][2] === row[i][2]
        )
          run++;
        out +=
          '<rect x="' +
          row[i][1] +
          '" y="' +
          y +
          '" width="' +
          run +
          '" height="1" fill="' +
          PIXEL_COLORS[row[i][2]] +
          '"/>';
        i += run;
      }
    });
    return out;
  }

  function pixelAvatar(mood) {
    var base = [];
    PIXEL_ROWS.forEach(function (row, y) {
      for (var x = 0; x < row.length; x++)
        if (row[x] !== ".") base.push([y, x, row[x]]);
    });
    var layers = Object.keys(PIXEL_LAYERS)
      .map(function (name) {
        var extra =
          name === "e-open"
            ? // blink: lens-coloured lids over the pupils, with a lash line
              '<g class="lid">' +
              rects([
                [15, 11, "L"],
                [15, 12, "L"],
                [15, 19, "L"],
                [15, 20, "L"],
                [16, 10, "E"],
                [16, 11, "E"],
                [16, 12, "E"],
                [16, 19, "E"],
                [16, 20, "E"],
                [16, 21, "E"],
              ]) +
              "</g>"
            : "";
        return (
          '<g class="ly ly-' +
          name +
          '">' +
          rects(PIXEL_LAYERS[name]) +
          extra +
          "</g>"
        );
      })
      .join("");
    return (
      '<svg class="ms-me mood-' +
      (mood || "happy") +
      '" viewBox="0 0 32 32" shape-rendering="crispEdges" aria-hidden="true" focusable="false">' +
      rects(base) +
      layers +
      "</svg>"
    );
  }
  var AVATAR = pixelAvatar("happy");

  // Which layers each mood shows, as CSS, generated from MOODS so they never drift apart.
  (function moodStyles() {
    var css = ".ms-me .ly{display:none}";
    Object.keys(MOODS).forEach(function (m) {
      css +=
        MOODS[m]
          .map(function (l) {
            return ".ms-me.mood-" + m + " .ly-" + l;
          })
          .join(",") + "{display:inline}";
    });
    var style = document.createElement("style");
    style.textContent = css;
    document.head.appendChild(style);
  })();

  function setMood(mood) {
    document.querySelectorAll("svg.ms-me").forEach(function (svg) {
      svg.setAttribute("class", "ms-me mood-" + mood);
    });
  }

  var $ = function (sel, root) {
    return (root || document).querySelector(sel);
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

  var prefs = readPrefs();
  var ctx = null;
  var tab = "advice";
  var lastBubble = "";
  var suggestions = null;

  function readPrefs() {
    var p = {};
    try {
      p = JSON.parse(localStorage.getItem(STORE)) || {};
    } catch (e) {}
    return {
      plan: p.plan || "",
      typed: p.typed || "",
      target: p.target || 15,
      seen: !!p.seen,
    };
  }
  function savePrefs() {
    try {
      localStorage.setItem(STORE, JSON.stringify(prefs));
    } catch (e) {}
  }

  // ── What the student has done ──────────────────────────────────────────

  /** The plan grid the student used most recently, with its statuses. */
  function detectPlan() {
    var best = null;
    Object.keys(PLANS).forEach(function (slug) {
      var saved;
      try {
        saved = JSON.parse(localStorage.getItem(PLANS[slug].key));
      } catch (e) {}
      if (!saved || !saved.statusMap) return;
      var marked = Object.keys(saved.statusMap).filter(function (c) {
        return saved.statusMap[c] !== "not-taken";
      });
      if (!marked.length) return;
      if (!best || (saved.updatedAt || 0) > best.updatedAt)
        best = {
          slug: slug,
          updatedAt: saved.updatedAt || 0,
          statusMap: saved.statusMap,
        };
    });
    return best;
  }

  function record() {
    var detected = detectPlan();
    var plan = prefs.plan || (detected && detected.slug) || "";
    var done = {},
      current = {};
    if (detected && detected.slug === plan) {
      Object.keys(detected.statusMap).forEach(function (c) {
        var code = c.replace(/\s+/g, "").toUpperCase();
        if (detected.statusMap[c] === "completed") done[code] = true;
        if (detected.statusMap[c] === "current") current[code] = true;
      });
    }
    (prefs.typed.toUpperCase().match(/[A-Z]{2,5}\s?\d{3}/g) || []).forEach(
      function (c) {
        done[c.replace(/\s+/g, "")] = true;
      },
    );
    // Courses with a grade in the student's academic record are finished (F doesn't count).
    var graded = (ctx && ctx.grades) || {};
    Object.keys(graded).forEach(function (c) {
      if (graded[c].points > 0) done[c] = true;
    });
    // Anything you passed means its prerequisites were passed too, even if they
    // aren't ticked; and past year 1, the prep year is behind you.
    var cat = (ctx && ctx.catalog) || {};
    var stack = Object.keys(done).concat(Object.keys(current));
    while (stack.length) {
      var e = cat[stack.pop()];
      ((e && e.pre) || []).forEach(function (p) {
        if (!done[p]) {
          done[p] = true;
          stack.push(p);
        }
      });
    }
    if (
      plan &&
      Object.keys(done)
        .concat(Object.keys(current))
        .some(function (c) {
          return cat[c] && cat[c].plans && cat[c].plans[plan] >= 2;
        })
    )
      Object.keys(cat).forEach(function (c) {
        if (cat[c].plans && cat[c].plans[plan] === 0) done[c] = true;
      });
    var known = Object.keys(done).length + Object.keys(current).length > 0;
    var hours = function (set) {
      return Object.keys(set).reduce(function (a, c) {
        var e = ctx && ctx.catalog[c];
        return a + ((e && e.h) || 3);
      }, 0);
    };
    return {
      plan: plan,
      fromGrid: !!(detected && detected.slug === plan),
      done: done,
      current: current,
      known: known,
      hoursDone: hours(done),
      hoursWithCurrent: hours(done) + hours(current),
    };
  }

  // ── Suggestions ────────────────────────────────────────────────────────

  function suggest() {
    var rec = record();
    if (!rec.plan || !ctx || !ctx.term)
      return { rec: rec, list: [], blocked: [] };
    var cat = ctx.catalog;
    var have = function (c) {
      return rec.done[c] || rec.current[c];
    };
    var eligible = [],
      blocked = [];
    Object.keys(cat).forEach(function (code) {
      var e = cat[code];
      if (!e.plans || e.plans[rec.plan] == null || have(code)) return;
      if (!ctx.byCourse[code]) return;
      var missing = (e.pre || []).filter(function (p) {
        return !have(p);
      });
      var viaCurrent = (e.pre || []).filter(function (p) {
        return rec.current[p];
      });
      var shortHours = e.minHours && rec.hoursWithCurrent < e.minHours;
      if (missing.length || shortHours) {
        blocked.push({
          code: code,
          missing: missing,
          minHours: shortHours ? e.minHours : 0,
          term: e.plans[rec.plan],
        });
        return;
      }
      eligible.push({
        code: code,
        term: e.plans[rec.plan],
        unlocks: (e.unlocks || []).length,
        viaCurrent: viaCurrent,
        hours: ctx.hoursOf(code),
      });
    });
    eligible.sort(function (a, b) {
      return (
        a.term - b.term || b.unlocks - a.unlocks || a.code.localeCompare(b.code)
      );
    });
    var total = 0;
    eligible.forEach(function (s) {
      s.pick = total + s.hours <= prefs.target;
      if (s.pick) total += s.hours;
    });
    blocked.sort(function (a, b) {
      return a.term - b.term;
    });
    return {
      rec: rec,
      list: eligible,
      blocked: blocked.slice(0, 6),
      total: total,
    };
  }

  // ── Advice ─────────────────────────────────────────────────────────────

  function words(entry) {
    var out = {};
    ((entry && entry.chapters) || []).forEach(function (title) {
      title
        .toLowerCase()
        .split(/[^a-z0-9+#]+/)
        .forEach(function (w) {
          if (w.length < 4 || STOP.indexOf(w) > -1) return;
          var stem = w.slice(0, 6);
          if (!out[stem]) out[stem] = w;
        });
    });
    return out;
  }

  function examShare(entry) {
    if (!entry || !entry.assess || !entry.assess.length) return null;
    var exam = 0,
      total = 0,
      project = false,
      lab = false;
    entry.assess.forEach(function (a) {
      total += a[1] || 0;
      if (a[2]) exam += a[1] || 0;
      if (/project/i.test(a[0])) project = true;
      if (/lab/i.test(a[0])) lab = true;
    });
    return total
      ? { exam: Math.round((exam / total) * 100), project: project, lab: lab }
      : null;
  }

  function advice() {
    var warn = [],
      info = [],
      good = [],
      courses = [];
    if (!ctx) return { warn: warn, info: info, good: good, courses: courses };
    var rec = record();
    var cat = ctx.catalog;
    var picked = ctx.picked;
    var add = function (list, icon, title, body, actions) {
      list.push({
        icon: icon,
        title: title,
        body: body,
        actions: actions || [],
      });
    };
    var and = L(" and ", " و");
    var comma = L(", ", "، ");

    // Lists read naturally in both languages: "A, B and C" / "A، B وC".
    var listOf = function (items) {
      if (items.length < 2) return items.join("");
      return items.slice(0, -1).join(comma) + and + items[items.length - 1];
    };

    // Sections: nothing fits, all closed, one left. One card each, listing the courses.
    if (ctx.leftOut.length)
      add(
        warn,
        "⚠",
        L("No section fits: ", "لا توجد شعبة مناسبة: ") +
          listOf(
            ctx.leftOut.map(function (l) {
              return l.code;
            }),
          ),
        "<ul>" +
          ctx.leftOut
            .map(function (l) {
              return "<li><b>" + l.code + "</b>: " + esc(l.reason) + "</li>";
            })
            .join("") +
          "</ul>",
        ctx.leftOut.map(function (l) {
          return ["sections", l.code, L("Sections: ", "شعب ") + l.code];
        }),
      );
    (ctx.clashingPairs || []).length &&
      add(
        warn,
        "⚠",
        L("Courses that always clash", "مواد تتعارض دائمًا"),
        "<ul>" +
          ctx.clashingPairs
            .map(function (p) {
              return "<li>" + p[0] + and + p[1] + "</li>";
            })
            .join("") +
          "</ul>" +
          L(
            "Every section of one overlaps every section of the other (or their finals are at the same time). Drop one from each pair.",
            "كل شعب إحداهما تتعارض مع كل شعب الأخرى (أو نهائياتهما في نفس الوقت). احذف مادة من كل زوج.",
          ),
      );
    var closedAll = [],
      oneLeft = [];
    picked.forEach(function (code) {
      var o = ctx.options[code];
      if (!o) return;
      var open = o.all.filter(function (x) {
        return x.open;
      }).length;
      if (!open) closedAll.push(code);
      else if (open === 1 && o.all.length > 1) oneLeft.push(code);
    });
    if (closedAll.length)
      add(
        warn,
        "⚠",
        L("Every section is closed: ", "كل الشعب مغلقة: ") + listOf(closedAll),
        L(
          "Watch for seats opening, or ask the department about extra sections.",
          "راقب توفر المقاعد أو اسأل القسم عن شعب إضافية.",
        ),
      );
    if (oneLeft.length)
      add(
        info,
        "•",
        L("Only one open section left: ", "شعبة واحدة متاحة فقط: ") +
          listOf(oneLeft),
        L("Register for these early.", "سجّلها مبكرًا."),
      );

    // Prerequisites, grouped by the prerequisite rather than repeated per course.
    if (picked.length && !rec.known)
      add(
        info,
        "?",
        L(
          "I can't check prerequisites yet",
          "لا أستطيع التحقق من المتطلبات السابقة بعد",
        ),
        L(
          "I don't know which courses you've finished. Mark them in your <a href=\"/academic-plan-themes/academic-plan/\">academic plan</a>, or type them under <b>What to take</b>.",
          'لا أعرف المواد التي أنهيتها. حدّدها في <a href="/academic-plan-themes/academic-plan/">الخطة الدراسية</a> أو اكتبها في تبويب <b>ماذا أسجّل</b>.',
        ),
      );
    var together = {},
      missing = {},
      pending = {},
      shortHours = [],
      offPlan = [];
    picked.forEach(function (code) {
      var e = cat[code];
      if (!e) return;
      (e.pre || []).forEach(function (p) {
        var bucket =
          picked.indexOf(p) > -1
            ? together
            : rec.known && !rec.done[p] && !rec.current[p]
              ? missing
              : rec.current[p]
                ? pending
                : null;
        if (bucket) (bucket[p] = bucket[p] || []).push(code);
      });
      if (e.minHours && rec.known && rec.hoursWithCurrent < e.minHours)
        shortHours.push(code + " (" + e.minHours + L(" h", " س") + ")");
      if (rec.plan && e.plans && e.plans[rec.plan] == null) offPlan.push(code);
    });
    Object.keys(together).forEach(function (p) {
      add(
        warn,
        "⚠",
        L(
          p + " is a prerequisite of " + listOf(together[p]),
          p + " متطلب سابق لـ " + listOf(together[p]),
        ),
        L(
          "You've picked them in the same term. Take " +
            p +
            " first, then " +
            listOf(together[p]) +
            ".",
          "اخترتها في نفس الفصل. خذ " +
            p +
            " أولًا ثم " +
            listOf(together[p]) +
            ".",
        ),
        together[p].map(function (c) {
          return ["drop", c, L("Remove ", "حذف ") + c];
        }),
      );
    });
    Object.keys(missing).forEach(function (p) {
      add(
        warn,
        "⚠",
        L(p + " isn't finished yet", p + " لم تُنهَ بعد"),
        L(
          "It's required for " +
            listOf(missing[p]) +
            ", so registration will refuse " +
            (missing[p].length > 1 ? "them" : "it") +
            " without it.",
          "وهي مطلوبة لـ " + listOf(missing[p]) + "، ولن يقبل التسجيل بدونها.",
        ),
        missing[p].map(function (c) {
          return ["drop", c, L("Remove ", "حذف ") + c];
        }),
      );
    });
    Object.keys(pending).forEach(function (p) {
      add(
        info,
        "•",
        L(
          listOf(pending[p]) +
            " depend" +
            (pending[p].length > 1 ? "" : "s") +
            " on passing " +
            p,
          listOf(pending[p]) + " تعتمد على النجاح في " + p,
        ),
        L(
          "You're taking " + p + " now, so this only works if you pass it.",
          p + " مسجّلة هذا الفصل، فهذا ينجح فقط إذا اجتزتها.",
        ),
      );
    });
    if (shortHours.length)
      add(
        warn,
        "⚠",
        L("Not enough credit hours yet: ", "الساعات المنجزة غير كافية: ") +
          listOf(shortHours),
        L(
          "You'll have about " +
            rec.hoursWithCurrent +
            " hours by the end of this term, going by your record.",
          "حسب سجلك سيكون لديك نحو " +
            rec.hoursWithCurrent +
            " ساعة بنهاية هذا الفصل.",
        ),
      );
    if (offPlan.length)
      add(
        info,
        "•",
        L(
          "Not in your " + planLabel(rec.plan) + " plan: ",
          "ليست ضمن خطة " + planLabel(rec.plan) + ": ",
        ) + listOf(offPlan),
        L(
          "Check with your advisor that " +
            (offPlan.length > 1 ? "they count" : "it counts") +
            " toward your degree.",
          "تأكد مع المرشد الأكاديمي أنها تُحتسب في خطتك.",
        ),
      );

    // Credit hours.
    var hours = picked.reduce(function (a, c) {
      return a + ctx.hoursOf(c);
    }, 0);
    if (hours > 19)
      add(
        warn,
        "⚠",
        L(hours + " credit hours is a lot", hours + " ساعة معتمدة عبء كبير"),
        L(
          "That's above a usual full load. Check your allowed maximum, and make sure your GPA can take it.",
          "هذا أعلى من العبء المعتاد. تحقق من الحد الأقصى المسموح وتأكد أن معدلك يحتمل ذلك.",
        ),
      );
    else if (picked.length && hours < 12)
      add(
        info,
        "•",
        L("Only " + hours + " credit hours", hours + " ساعات معتمدة فقط"),
        L(
          "If you need full-time status (scholarships, rewards, graduation timing), check the minimum with the registrar.",
          "إذا كنت تحتاج للانتظام الكامل (منحة أو مكافأة أو موعد التخرج) فتحقق من الحد الأدنى مع القبول والتسجيل.",
        ),
      );

    // Difficulty from ratings.
    var heavy = picked.filter(function (c) {
      var d = ctx.difficulty(c);
      return d.rated && d.value >= 3.8;
    });
    if (heavy.length >= 2)
      add(
        warn,
        "⚠",
        L("Heavy courses together: ", "مواد ثقيلة معًا: ") + listOf(heavy),
        L(
          "Students rate these as demanding. Pair them with lighter courses, or spread them across terms if your plan allows.",
          "يقيّمها الطلاب على أنها متعبة. اجمعها مع مواد أخف أو وزّعها على فصول إن سمحت خطتك.",
        ),
      );

    // How the picked courses connect: one card per shared foundation, then
    // clusters of courses with overlapping topics (not one card per pair).
    var foundations = {};
    picked.forEach(function (code) {
      ((cat[code] && cat[code].pre) || []).forEach(function (p) {
        if (picked.indexOf(p) < 0)
          (foundations[p] = foundations[p] || []).push(code);
      });
    });
    var linked = {};
    Object.keys(foundations).forEach(function (p) {
      var group = foundations[p];
      if (group.length < 2) return;
      group.forEach(function (a) {
        group.forEach(function (b) {
          linked[a + "|" + b] = true;
        });
      });
      add(
        good,
        "↔",
        L(
          listOf(group) + (group.length > 2 ? " all" : "") + " build on " + p,
          listOf(group) + " مبنية على " + p,
        ),
        L(
          "Same foundation, so revising " +
            p +
            " once helps " +
            (group.length > 2 ? "all of them" : "both") +
            ".",
          "نفس الأساس، فمراجعة " + p + " مرة واحدة تفيد فيها كلها.",
        ),
      );
    });
    var parent = {};
    var root = function (x) {
      while (parent[x] && parent[x] !== x) x = parent[x];
      return x;
    };
    var topics = {};
    for (var i = 0; i < picked.length; i++)
      for (var j = i + 1; j < picked.length; j++) {
        var a = picked[i],
          b = picked[j];
        if (!cat[a] || !cat[b] || linked[a + "|" + b]) continue;
        var wa = words(cat[a]),
          wb = words(cat[b]);
        var shared = Object.keys(wa)
          .filter(function (k) {
            return wb[k];
          })
          .map(function (k) {
            return wa[k];
          });
        if (shared.length < 2) continue;
        parent[a] = parent[a] || a;
        parent[b] = parent[b] || b;
        parent[root(b)] = root(a);
        topics[a + "|" + b] = shared;
      }
    var clusters = {};
    Object.keys(parent).forEach(function (c) {
      (clusters[root(c)] = clusters[root(c)] || []).push(c);
    });
    Object.keys(clusters).forEach(function (r) {
      var group = clusters[r].sort();
      var words_ = [];
      Object.keys(topics).forEach(function (k) {
        var pair = k.split("|");
        if (group.indexOf(pair[0]) > -1)
          topics[k].forEach(function (w) {
            if (words_.indexOf(w) < 0) words_.push(w);
          });
      });
      add(
        good,
        "↔",
        L(listOf(group) + " overlap", listOf(group) + " متداخلة"),
        L("Shared topics: ", "مواضيع مشتركة: ") +
          '<span dir="ltr">' +
          esc(words_.slice(0, 5).join(", ")) +
          "</span>. " +
          L(
            "Studying one will help with the other" +
              (group.length > 2 ? "s" : "") +
              ".",
            "مذاكرة إحداها تساعد في الأخرى.",
          ),
      );
    });

    // Schedule shape.
    var m = ctx.metrics;
    if (m) {
      if (m.clashes)
        add(
          warn,
          "⚠",
          L("Two finals at the same time", "اختباران نهائيان في نفس الوقت"),
          L(
            "You allowed final clashes. You'd need an exam-conflict request; check the deadline.",
            "سمحت بتعارض النهائيات، وستحتاج لتقديم طلب تعارض اختبارات. تحقق من الموعد النهائي.",
          ),
        );
      if (m.sameDay)
        add(
          warn,
          "⚠",
          L(
            m.sameDay +
              " day" +
              (m.sameDay > 1 ? "s" : "") +
              " with two finals",
            "اختباران نهائيان في يوم واحد (" + m.sameDay + ")",
          ),
          L(
            "Look for a schedule with finals spread out (sort by <b>Finals spread out</b>).",
            "ابحث عن جدول باختبارات متباعدة (رتّب حسب <b>النهائيات متباعدة</b>).",
          ),
        );
      else if (m.within24)
        add(
          info,
          "•",
          L(
            "Finals less than 24 hours apart",
            "اختبارات نهائية بينها أقل من 24 ساعة",
          ),
          L(
            "Start revising for the second one early.",
            "ابدأ مراجعة الاختبار الثاني مبكرًا.",
          ),
        );
      if (m.longest > 7 * 60)
        add(
          info,
          "•",
          L(
            "Your longest day is " + (m.longest / 60).toFixed(1) + " hours",
            "أطول يوم في جدولك " + (m.longest / 60).toFixed(1) + " ساعات",
          ),
          L(
            "Bring food, and plan study breaks in the gaps.",
            "احضر وجبة معك، واستغل الفراغات للمذاكرة.",
          ),
        );
      if (m.gaps >= 180)
        add(
          info,
          "•",
          L(
            "About " + Math.round(m.gaps / 60) + " hours of gaps a week",
            "نحو " + Math.round(m.gaps / 60) + " ساعات فراغ أسبوعيًا",
          ),
          L(
            "Good study time if you use it, or try sorting by <b>Fewest gaps</b>.",
            "وقت جيد للمذاكرة إن استغللته، أو رتّب حسب <b>أقل فراغات</b>.",
          ),
        );
      if (m.days <= 3 && ctx.picked.length >= 4)
        add(
          good,
          "✓",
          L(
            "Only " + m.days + " days on campus",
            "حضور " + m.days + " أيام فقط",
          ),
          L("Nice and compact.", "جدول مضغوط ومريح."),
        );
      if (m.closed)
        add(
          warn,
          "⚠",
          L(
            m.closed +
              " closed section" +
              (m.closed > 1 ? "s" : "") +
              " in this schedule",
            "في هذا الجدول شعب مغلقة (" + m.closed + ")",
          ),
          L(
            "Turn off <b>Include closed sections</b> to see only schedules you can register now.",
            "أوقف <b>إظهار الشعب المغلقة</b> لترى الجداول المتاحة للتسجيل الآن فقط.",
          ),
        );
      if (
        ctx.load &&
        (ctx.load.level === "heavy" || ctx.load.level === "very heavy")
      ) {
        var worst = ctx.picked.slice().sort(function (x, y) {
          return (
            ctx.difficulty(y).value * ctx.hoursOf(y) -
            ctx.difficulty(x).value * ctx.hoursOf(x)
          );
        })[0];
        add(
          warn,
          "⚠",
          L(
            "This term looks " + ctx.load.level,
            ctx.load.level === "heavy"
              ? "هذا الفصل يبدو ثقيلًا"
              : "هذا الفصل يبدو ثقيلًا جدًا",
          ),
          L(
            "The biggest share comes from " +
              worst +
              ". If it isn't urgent for your plan, swapping it for a lighter course would help.",
            "أكبر جزء من العبء من " +
              worst +
              ". إن لم تكن مستعجلة في خطتك فاستبدالها بمادة أخف سيساعد.",
          ),
        );
      }
    }

    // Course by course.
    picked.forEach(function (code) {
      var e = cat[code] || {};
      var d = ctx.difficulty(code);
      var r = ctx.ratings[code];
      var lines = [];
      if (d.personal) {
        var list = function (filter) {
          var chosen = d.personal.related.filter(filter);
          return (chosen.length ? chosen : d.personal.related)
            .map(function (x) {
              return x.code + " (" + x.letter + ")";
            })
            .join(comma);
        };
        lines.push(
          d.personal.shift < 0
            ? L(
                "<b>Should go well for you</b>: you did well in ",
                "<b>متوقع أن تكون مناسبة لك</b>: أداؤك كان جيدًا في ",
              ) +
                list(function (x) {
                  return x.points >= 3;
                }) +
                "."
            : d.personal.shift > 0
              ? L(
                  "<b>Give this one extra time</b>: you found ",
                  "<b>خصّص لها وقتًا إضافيًا</b>: ",
                ) +
                list(function (x) {
                  return x.points < 2.5;
                }) +
                L(
                  " harder, and this builds on similar material.",
                  " كانت أصعب عليك، وهذه مبنية على محتوى مشابه.",
                )
              : L("Based on ", "بناءً على ") +
                list(function () {
                  return true;
                }) +
                L(
                  ", expect about average difficulty for you.",
                  "، المتوقع أن تكون متوسطة الصعوبة لك.",
                ),
        );
      }
      if (d.rated)
        lines.push(
          L(
            "Difficulty " +
              d.base.toFixed(1) +
              "/5 from " +
              d.n +
              " student rating" +
              (d.n > 1 ? "s" : ""),
            "الصعوبة " + d.base.toFixed(1) + "/5 من " + d.n + " تقييم",
          ) +
            (r && r.workload
              ? L(", workload ", "، العبء ") + r.workload.toFixed(1) + "/5"
              : ""),
        );
      else if (ctx.ratings[code] === null)
        lines.push(
          L("No student ratings yet", "لا توجد تقييمات من الطلاب بعد") +
            (e.url
              ? L(
                  ' (<a href="' +
                    e.url +
                    "\">rate it</a> once you've taken it)",
                  ' (<a href="' + e.url + '">قيّمها</a> بعد دراستها)',
                )
              : ""),
        );
      var ex = examShare(e);
      if (ex) {
        lines.push(
          L(
            ex.exam + "% of the grade is exams",
            "الاختبارات " + ex.exam + "% من الدرجة",
          ) +
            (ex.exam >= 70
              ? L(
                  ": revise every week, not just before exams",
                  ": راجع أسبوعيًا وليس قبل الاختبارات فقط",
                )
              : ex.exam <= 50
                ? L(
                    ": a lot comes from coursework, so keep up with it",
                    ": جزء كبير من الأعمال الفصلية، فالتزم بها أولًا بأول",
                  )
                : ""),
        );
        if (ex.project)
          lines.push(
            L(
              "Has a project: steady work across the term",
              "فيها مشروع: عمل مستمر طوال الفصل",
            ),
          );
      }
      if (e.chapters && e.chapters.length)
        lines.push(
          L(
            e.chapters.length + " chapters, e.g. ",
            e.chapters.length + " فصول، مثل: ",
          ) +
            '<span dir="ltr">' +
            esc(e.chapters.slice(0, 3).join(", ")) +
            "</span>",
        );
      if (e.unlocks && e.unlocks.length)
        lines.push(
          L("Opens ", "تفتح ") +
            e.unlocks.join(comma) +
            (e.unlocks.length >= 3
              ? L(
                  ". Delaying it delays all of those",
                  ". تأجيلها يؤخر كل هذه المواد",
                )
              : ""),
        );
      var o = ctx.options[code];
      if (o) {
        var openN = o.all.filter(function (x) {
          return x.open;
        }).length;
        lines.push(
          L(
            o.all.length +
              " section" +
              (o.all.length > 1 ? "s" : "") +
              ", " +
              openN +
              " open",
            o.all.length + " شعب، " + openN + " متاحة",
          ),
        );
      }
      if (e.url)
        lines.push(
          '<a href="' +
            e.url +
            '">' +
            L(
              "Study materials on SHOUG.TECH",
              "المواد الدراسية على SHOUG.TECH",
            ) +
            "</a>",
        );
      courses.push({ code: code, name: ctx.nameOf(code), lines: lines });
    });

    return { warn: warn, info: info, good: good, courses: courses };
  }

  // ── UI ─────────────────────────────────────────────────────────────────

  function planLabel(slug) {
    return PLANS[slug] ? L(PLANS[slug].label, PLANS[slug].labelAr) : slug;
  }

  function chrome() {
    var panel = $(".ms-panel");
    if (!panel) return;
    $(".ms-fab").setAttribute(
      "aria-label",
      L("Open Murshida, your course advisor", "افتح مرشدة، المرشدة الدراسية"),
    );
    panel.setAttribute("aria-label", L("Murshida", "مرشدة"));
    $(".ms-head h2", panel).textContent = L("Murshida", "مرشدة");
    $(".ms-head p", panel).textContent = L(
      "Your course advisor",
      "مرشدتك لاختيار المواد",
    );
    $(".ms-x", panel).setAttribute("aria-label", L("Close", "إغلاق"));
    $('[data-tab="suggest"]', panel).textContent = L(
      "What to take",
      "ماذا أسجّل",
    );
    $('[data-tab="advice"]', panel).textContent = L(
      "About your picks",
      "عن اختياراتك",
    );
  }

  function mount() {
    var fab = document.createElement("button");
    fab.type = "button";
    fab.className = "ms-fab";
    fab.innerHTML = AVATAR + '<span class="ms-dot" hidden></span>';
    var bubble = document.createElement("div");
    bubble.className = "ms-bubble";
    bubble.setAttribute("role", "status");
    var panel = document.createElement("aside");
    panel.className = "ms-panel";
    panel.innerHTML =
      '<div class="ms-head"><div class="ms-avatar">' +
      AVATAR +
      '</div><div><h2></h2><p></p></div><button class="ms-x" type="button">✕</button></div>' +
      '<div class="ms-tabs" role="tablist"><button type="button" role="tab" data-tab="suggest"></button><button type="button" role="tab" data-tab="advice"></button></div>' +
      '<div class="ms-body" tabindex="0"></div>';
    document.body.appendChild(bubble);
    document.body.appendChild(fab);
    document.body.appendChild(panel);
    chrome();
    var emptyBird = document.getElementById("empty-mascot");
    if (emptyBird) emptyBird.innerHTML = AVATAR;

    fab.addEventListener("click", function () {
      open();
    });
    bubble.addEventListener("click", function () {
      open("advice");
    });
    $(".ms-x", panel).addEventListener("click", close);
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && panel.classList.contains("open")) close();
    });
    panel.addEventListener("click", onPanelClick);
    panel.addEventListener("change", onPanelChange);

    if (!prefs.seen) {
      setTimeout(function () {
        say(
          L(
            "Hi, I'm Murshida! Tell me your plan and I'll suggest what to take this term.",
            "أهلًا، أنا مرشدة! أخبرني بخطتك وسأقترح عليك مواد هذا الفصل.",
          ),
        );
      }, 1200);
      prefs.seen = true;
      savePrefs();
    }
  }

  function say(msg) {
    var b = $(".ms-bubble");
    if (!b || $(".ms-panel").classList.contains("open")) return;
    b.innerHTML = msg;
    b.classList.add("show");
    clearTimeout(say.t);
    say.t = setTimeout(function () {
      b.classList.remove("show");
    }, 7000);
  }

  function open(which) {
    if (which) tab = which;
    $(".ms-bubble").classList.remove("show");
    $(".ms-panel").classList.add("open");
    renderPanel();
    $(".ms-x").focus();
  }
  function close() {
    $(".ms-panel").classList.remove("open");
    $(".ms-fab").focus();
  }

  function card(kind, c) {
    return (
      '<div class="ms-card ' +
      kind +
      '"><div class="ms-t"><span class="ico" aria-hidden="true">' +
      c.icon +
      "</span><span>" +
      esc(c.title) +
      "</span></div>" +
      c.body +
      (c.actions.length
        ? '<div class="ms-actions">' +
          c.actions
            .map(function (a) {
              return (
                '<button class="ms-mini" type="button" data-act="' +
                a[0] +
                '" data-code="' +
                a[1] +
                '">' +
                esc(a[2]) +
                "</button>"
              );
            })
            .join("") +
          "</div>"
        : "") +
      "</div>"
    );
  }

  function renderPanel() {
    var panel = $(".ms-panel");
    if (!panel || !panel.classList.contains("open")) return;
    panel.querySelectorAll("[data-tab]").forEach(function (b) {
      b.setAttribute("aria-selected", String(b.dataset.tab === tab));
    });
    var body = $(".ms-body", panel);
    body.innerHTML = tab === "suggest" ? suggestHtml() : adviceHtml();
  }

  function adviceHtml() {
    if (!ctx || !ctx.picked.length)
      return (
        '<div class="ms-empty"><div class="ms-bigme">' +
        AVATAR +
        "</div>" +
        L(
          "Pick some courses and I'll tell you what I think: prerequisites, how heavy they are, how they connect, and what to watch for in your schedule.",
          "اختر بعض المواد وسأخبرك برأيي: المتطلبات السابقة، ومدى ثقلها، وكيف ترتبط ببعض، وما يجب الانتباه له في جدولك.",
        ) +
        '<br><br><button class="ms-mini" type="button" data-goto="suggest">' +
        L("Help me choose", "ساعدني في الاختيار") +
        "</button></div>"
      );
    var a = advice();
    var html = "";
    if (a.warn.length)
      html +=
        "<h3>" +
        L("Heads up", "انتبه") +
        "</h3>" +
        a.warn
          .map(function (c) {
            return card("warn", c);
          })
          .join("");
    if (a.good.length)
      html +=
        "<h3>" +
        L("Good to know", "معلومات مفيدة") +
        "</h3>" +
        a.good
          .map(function (c) {
            return card("good", c);
          })
          .join("");
    if (a.info.length)
      html +=
        "<h3>" +
        L("Tips", "نصائح") +
        "</h3>" +
        a.info
          .map(function (c) {
            return card("", c);
          })
          .join("");
    if (!a.warn.length)
      html =
        '<div class="ms-card good"><div class="ms-t"><span class="ico">✓</span><span>' +
        L("Looks good to me", "يبدو جيدًا") +
        "</span></div>" +
        L(
          "No prerequisite problems or clashes I can see.",
          "لا أرى مشاكل في المتطلبات أو تعارضات.",
        ) +
        "</div>" +
        html;
    html +=
      "<h3>" +
      L("Course by course", "مادة مادة") +
      "</h3>" +
      a.courses
        .map(function (c) {
          return (
            '<div class="ms-card"><div class="ms-t"><span>' +
            c.code +
            '</span><span class="ms-muted" dir="auto">' +
            esc(c.name) +
            "</span></div><ul>" +
            c.lines
              .map(function (l) {
                return "<li>" + l + "</li>";
              })
              .join("") +
            "</ul></div>"
          );
        })
        .join("");
    html +=
      '<p class="ms-muted">' +
      L(
        "Advice comes from your plan, the official timetable, syllabi on this site and other students' ratings. Your academic advisor has the final word.",
        "النصائح مبنية على خطتك والجدول الرسمي وتوصيفات المواد في هذا الموقع وتقييمات الطلاب. والقرار الأخير للمرشد الأكاديمي.",
      ) +
      "</p>";
    return html;
  }

  function suggestHtml() {
    var s = (suggestions = suggest());
    var rec = s.rec;
    var plan =
      '<a href="/academic-plan-themes/' +
      rec.plan +
      '/grid.html">' +
      L("academic plan", "الخطة الدراسية") +
      "</a>";
    var html =
      '<div class="ms-field"><label for="ms-plan">' +
      L("Your major", "تخصصك") +
      '</label><select id="ms-plan"><option value="">' +
      L("Choose your major", "اختر تخصصك") +
      "</option>" +
      Object.keys(PLANS)
        .map(function (k) {
          return (
            '<option value="' +
            k +
            '"' +
            (k === rec.plan ? " selected" : "") +
            ">" +
            planLabel(k) +
            "</option>"
          );
        })
        .join("") +
      "</select></div>";
    if (rec.plan) {
      var doneN = Object.keys(rec.done).length,
        nowN = Object.keys(rec.current).length;
      html += rec.fromGrid
        ? '<p class="ms-muted">' +
          L(
            "Using your " +
              plan +
              ": " +
              doneN +
              " courses done (" +
              rec.hoursDone +
              " h)" +
              (nowN ? ", " + nowN + " in progress" : "") +
              ".",
            "حسب " +
              plan +
              ": " +
              doneN +
              " مواد منتهية (" +
              rec.hoursDone +
              " ساعة)" +
              (nowN ? "، و" + nowN + " قيد الدراسة" : "") +
              ".",
          ) +
          "</p>"
        : '<p class="ms-muted">' +
          L(
            "I couldn't find your saved plan in this browser. Mark your courses in the " +
              plan +
              ", or list what you've finished below.",
            "لم أجد خطتك المحفوظة في هذا المتصفح. حدّد موادك في " +
              plan +
              " أو اكتب ما أنهيته بالأسفل.",
          ) +
          "</p>";
    }
    html +=
      '<div class="ms-field"><label for="ms-typed">' +
      L(
        "Other courses you've finished (optional)",
        "مواد أخرى أنهيتها (اختياري)",
      ) +
      '</label><textarea id="ms-typed" rows="2" dir="ltr" placeholder="CS101, MATH111, ENG101">' +
      esc(prefs.typed) +
      "</textarea></div>";
    html +=
      '<div class="ms-field"><label for="ms-target">' +
      L("Credit hours you want", "عدد الساعات المطلوب") +
      '</label><select id="ms-target">' +
      [12, 13, 14, 15, 16, 17, 18, 19]
        .map(function (h) {
          return (
            "<option" +
            (h === prefs.target ? " selected" : "") +
            ">" +
            h +
            "</option>"
          );
        })
        .join("") +
      "</select></div>";
    if (!rec.plan)
      return (
        html +
        '<div class="ms-empty">' +
        L(
          "Choose your major and I'll find the courses you can take this term.",
          "اختر تخصصك وسأجد المواد المتاحة لك هذا الفصل.",
        ) +
        "</div>"
      );
    if (!ctx || !ctx.term)
      return (
        html +
        '<div class="ms-empty">' +
        L("Waiting for the timetable…", "بانتظار الجدول…") +
        "</div>"
      );
    if (!rec.known)
      html +=
        '<div class="ms-card warn"><div class="ms-t"><span class="ico">?</span><span>' +
        L("I don't know what you've finished", "لا أعرف ما أنهيته من مواد") +
        "</span></div>" +
        L(
          "So I'm treating you as a new student. Mark courses in your plan or type them above for real suggestions.",
          "لذلك أتعامل معك كطالب جديد. حدّد المواد في خطتك أو اكتبها بالأعلى لاقتراحات دقيقة.",
        ) +
        "</div>";
    if (!s.list.length)
      return (
        html +
        '<div class="ms-empty">' +
        L(
          "Nothing left in your plan that's offered this term and open to you. You may be done, or the remaining courses aren't offered at your campus this term.",
          "لا يوجد في خطتك مواد مطروحة هذا الفصل ومتاحة لك. ربما أنهيت خطتك، أو المواد المتبقية غير مطروحة في مقرك هذا الفصل.",
        ) +
        "</div>"
      );
    html +=
      "<h3>" +
      L("You can take these this term", "يمكنك تسجيل هذه المواد هذا الفصل") +
      "</h3>";
    html += s.list
      .map(function (x) {
        var why = [L("Plan term ", "المستوى ") + x.term];
        if (x.unlocks)
          why.push(
            L(
              "opens " +
                x.unlocks +
                " later course" +
                (x.unlocks > 1 ? "s" : ""),
              "تفتح " + x.unlocks + " مواد لاحقة",
            ),
          );
        if (x.viaCurrent.length)
          why.push(
            L("if you pass ", "إذا اجتزت ") + x.viaCurrent.join(L(", ", "، ")),
          );
        var d = ctx.difficulty(x.code);
        if (d.rated)
          why.push(L("difficulty ", "الصعوبة ") + d.value.toFixed(1) + "/5");
        var already = ctx.picked.indexOf(x.code) > -1;
        return (
          '<label class="ms-sug"><input type="checkbox" data-sug="' +
          x.code +
          '"' +
          (x.pick && !already ? " checked" : "") +
          (already ? " disabled checked" : "") +
          "><span><b>" +
          x.code +
          "</b> " +
          '<span dir="auto">' +
          esc(ctx.nameOf(x.code)) +
          "</span><small>" +
          why.join(" · ") +
          (already ? L(" · already picked", " · مختارة مسبقًا") : "") +
          '</small></span><span class="h">' +
          x.hours +
          L(" h", " س") +
          "</span></label>"
        );
      })
      .join("");
    html +=
      '<div class="ms-actions" style="margin-top:12px"><button class="btn primary" type="button" data-act="add-suggested">' +
      L("Add ticked courses", "أضف المواد المحددة") +
      "</button></div>";
    html +=
      '<p class="ms-muted">' +
      L(
        "Ticked: the earliest courses in your plan up to " +
          prefs.target +
          " hours, favouring ones that unlock more of your degree. Behind on a course? It comes first.",
        "المحدد: أقدم المواد في خطتك حتى " +
          prefs.target +
          " ساعة، مع تفضيل المواد التي تفتح مواد أكثر. المواد المتأخرة تأتي أولًا.",
      ) +
      "</p>";
    if (s.blocked.length)
      html +=
        "<h3>" +
        L("Not yet", "ليس بعد") +
        "</h3>" +
        s.blocked
          .map(function (b) {
            return (
              '<div class="ms-card"><b>' +
              b.code +
              '</b> <span dir="auto">' +
              esc(ctx.nameOf(b.code)) +
              '</span><br><span class="ms-muted">' +
              (b.missing.length
                ? L("Needs ", "تتطلب ") + b.missing.join(L(", ", "، "))
                : "") +
              (b.minHours
                ? (b.missing.length ? " · " : "") +
                  L(
                    "Needs " + b.minHours + " credit hours",
                    "تتطلب إنهاء " + b.minHours + " ساعة",
                  )
                : "") +
              "</span></div>"
            );
          })
          .join("");
    return html;
  }

  function onPanelClick(e) {
    var t = e.target.closest("[data-tab], [data-act], [data-goto]");
    if (!t) return;
    if (t.dataset.tab || t.dataset.goto) {
      tab = t.dataset.tab || t.dataset.goto;
      return renderPanel();
    }
    var P = window.SchedulePlanner;
    if (!P) return;
    if (t.dataset.act === "drop") P.unpick(t.dataset.code);
    if (t.dataset.act === "sections") P.openSections(t.dataset.code);
    if (t.dataset.act === "add-suggested") {
      var codes = [];
      document
        .querySelectorAll("[data-sug]:checked:not(:disabled)")
        .forEach(function (c) {
          codes.push(c.dataset.sug);
        });
      if (!codes.length) return;
      if (suggestions && suggestions.rec.plan)
        P.setDept(PLANS[suggestions.rec.plan].dept);
      P.pick(codes);
      tab = "advice";
      renderPanel();
    }
  }

  function onPanelChange(e) {
    if (e.target.id === "ms-plan") {
      prefs.plan = e.target.value;
      savePrefs();
      renderPanel();
    }
    if (e.target.id === "ms-target") {
      prefs.target = +e.target.value;
      savePrefs();
      renderPanel();
    }
    if (e.target.id === "ms-typed") {
      prefs.typed = e.target.value;
      savePrefs();
      renderPanel();
    }
  }

  function update(context) {
    ctx = context;
    var fab = $(".ms-fab");
    if (!fab) return;
    var a = advice();
    // Resting mood: worried when something needs attention, sad when nothing fits, happy otherwise.
    baseMood = a.warn.length
      ? "alarm"
      : ctx.picked.length && !ctx.results
        ? "sad"
        : "happy";
    var found = ctx.picked.length && ctx.results && !prevResults;
    var count = ctx.results;
    prevResults = ctx.results;
    if (!reacting) setMood(baseMood);
    if (found && !a.warn.length) {
      react(
        "celebrate",
        2600,
        L(
          "Found " +
            count.toLocaleString() +
            " schedule" +
            (count > 1 ? "s" : "") +
            " that work!",
          "وجدت " + count.toLocaleString() + " جدول مناسب!",
        ),
      );
      lastBubble = "";
      renderPanel();
      return;
    }
    var dot = $(".ms-dot", fab);
    dot.hidden = !a.warn.length;
    dot.textContent = a.warn.length;
    var more = a.warn.length - 1;
    var msg = a.warn.length
      ? "<b>" +
        esc(a.warn[0].title) +
        ".</b>" +
        (more
          ? L(
              " And " +
                more +
                " more thing" +
                (more > 1 ? "s" : "") +
                ". Tap me.",
              " وهناك " + more + " ملاحظات أخرى. اضغط عليّ.",
            )
          : L(" Tap me for details.", " اضغط عليّ للتفاصيل."))
      : a.good.length
        ? esc(a.good[0].title) +
          ". " +
          L("Tap me for more.", "اضغط عليّ للمزيد.")
        : "";
    if (msg && msg !== lastBubble) say(msg);
    lastBubble = msg;
    renderPanel();
  }

  var baseMood = "happy",
    prevResults = 0,
    reacting = null;

  /** A short reaction (e.g. "love" after saving), then back to the resting mood. */
  function react(mood, ms, msg) {
    if (!MOODS[mood]) return;
    clearTimeout(reacting);
    setMood(mood);
    var fab = $(".ms-fab");
    if (fab) {
      fab.classList.remove("ms-pop");
      void fab.offsetWidth;
      fab.classList.add("ms-pop");
    }
    if (msg) say(msg);
    reacting =
      ms === 0
        ? true
        : setTimeout(function () {
            reacting = null;
            setMood(baseMood);
          }, ms || 2200);
  }
  function settle() {
    clearTimeout(reacting);
    reacting = null;
    setMood(baseMood);
  }

  /** Called by the planner when the language changes. */
  function relabel() {
    chrome();
    lastBubble = "";
    if (ctx)
      update(window.SchedulePlanner ? window.SchedulePlanner.context() : ctx);
    renderPanel();
  }

  window.Murshida = {
    update: update,
    open: open,
    relabel: relabel,
    react: react,
    settle: settle,
  };
  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", mount);
  else mount();
})();
