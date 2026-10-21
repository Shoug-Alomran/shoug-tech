/**
 * Course ratings and student tips.
 *
 * Signed-in students rate a course out of five stars: overall, workload,
 * assignment difficulty and length, project/lab difficulty when the course
 * has them, and the difficulty of each exam listed under the overview's
 * "Weight of Assessments" (Midterm + Final when a course has no such list).
 *
 * One document per student per course at courseRatings/{course}/ratings/{uid};
 * the rules live in firebase/course-ratings.rules. Course overviews get a
 * summary + rating form + student tips, track pages (CS, SE, CYS, Math, Other, English hub)
 * get an average chip on every course row. Loaded by mobile-navigation.js.
 */
(function () {
  "use strict";

  if (window.__shougCourseRatings) return;
  window.__shougCourseRatings = true;

  var TRACKS =
    "computer-science|software-engineering|cybersecurity|math|other-courses";
  var COURSE_PATH = new RegExp(
    "^/academics/(?:" + TRACKS + ")/(?:english/)?([a-z]+\\d{3})/$",
  );
  var TRACK_PATH = new RegExp(
    "^/academics/(?:(?:" + TRACKS + ")|other-courses/english)/$",
  );
  var MAX_EXAMS = 10;
  var path = location.pathname.replace(/index\.html$/, "");

  var SCALES = {
    quality: {
      en: ["Poor", "Fair", "Good", "Very good", "Excellent"],
      ar: ["ضعيف", "مقبول", "جيد", "جيد جدًا", "ممتاز"],
    },
    difficulty: {
      en: ["Very easy", "Easy", "Moderate", "Hard", "Very hard"],
      ar: ["سهل جدًا", "سهل", "متوسط", "صعب", "صعب جدًا"],
    },
    length: {
      en: ["Very short", "Short", "Moderate", "Long", "Very long"],
      ar: ["قصير جدًا", "قصير", "متوسط", "طويل", "طويل جدًا"],
    },
    load: {
      en: ["Very light", "Light", "Moderate", "Heavy", "Very heavy"],
      ar: ["خفيف جدًا", "خفيف", "متوسط", "ثقيل", "ثقيل جدًا"],
    },
  };

  var STAR =
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 2.6l2.9 6.2 6.7.8-5 4.6 1.3 6.7L12 17.6l-5.9 3.3 1.3-6.7-5-4.6 6.7-.8z"/></svg>';

  // ── Helpers ──────────────────────────────────────────────────────────────

  function isArabic() {
    return (document.documentElement.lang || "").indexOf("ar") === 0;
  }

  function L(en, ar) {
    return isArabic() && ar ? ar : en;
  }

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;",
      }[c];
    });
  }

  function validScore(n) {
    return typeof n === "number" && n % 1 === 0 && n >= 1 && n <= 5;
  }

  function fixed(n) {
    return (Math.round(n * 10) / 10).toFixed(1);
  }

  function scaleWord(scale, n) {
    var words = SCALES[scale][isArabic() ? "ar" : "en"];
    return words[Math.min(4, Math.max(0, Math.round(n) - 1))];
  }

  function countLabel(n) {
    if (isArabic()) return n === 1 ? "تقييم واحد" : n + " تقييمات";
    return n === 1 ? "1 rating" : n + " ratings";
  }

  function stars(avg, cls) {
    var pct = avg ? Math.max(0, Math.min(100, (avg / 5) * 100)) : 0;
    var row = new Array(6).join(STAR);
    return (
      '<span class="crt-stars ' +
      (cls || "") +
      '" aria-hidden="true"><span class="crt-stars-base">' +
      row +
      '</span><span class="crt-stars-fill" style="width:' +
      pct +
      '%">' +
      row +
      "</span></span>"
    );
  }

  /** Waits for firebase-auth.js to boot Firebase, asking it to load now. */
  function withFirebase(cb) {
    if (window.__shoug_fb) return cb(window.__shoug_fb);
    window.addEventListener(
      "shoug:fb",
      function () {
        cb(window.__shoug_fb);
      },
      { once: true },
    );
    if (typeof window.__shougLoadFirebaseAuth === "function")
      window.__shougLoadFirebaseAuth(false);
  }

  function ratingsRef(fb, course) {
    return fb
      .firestore()
      .collection("courseRatings")
      .doc(course)
      .collection("ratings");
  }

  /** Averages every category (and every exam key) across rating docs. */
  function summarize(docs) {
    var sums = {}, termCounts = {};
    var add = function (key, n) {
      if (!validScore(n)) return;
      var s = sums[key] || (sums[key] = { total: 0, count: 0 });
      s.total += n;
      s.count += 1;
    };
    docs.forEach(function (d) {
      if (typeof d.term === "string" && d.term) termCounts[d.term] = (termCounts[d.term] || 0) + 1;
      Object.keys(d).forEach(function (k) {
        if (k === "exams" && d.exams && typeof d.exams === "object") {
          Object.keys(d.exams).forEach(function (e) {
            add("exams." + e, d.exams[e]);
          });
        } else if (k !== "uid" && k !== "updatedAt") {
          add(k, d[k]);
        }
      });
    });
    var out = { count: 0 };
    Object.keys(sums).forEach(function (k) {
      out[k] = { avg: sums[k].total / sums[k].count, count: sums[k].count };
    });
    if (out.overall) out.count = out.overall.count;
    out.termCounts = termCounts;
    return out;
  }

  function ratingTerms() {
    var year = new Date().getFullYear(), out = [];
    for (var y = year; y >= year - 3; y--) {
      out.push({ value: y + "-first", label: L("First semester " + y, "الفصل الأول " + y) });
      out.push({ value: y + "-second", label: L("Second semester " + y, "الفصل الثاني " + y) });
      out.push({ value: y + "-summer", label: L("Summer " + y, "الفصل الصيفي " + y) });
    }
    return out;
  }

  var STYLE = [
    ".crt-stars{position:relative;display:inline-flex;line-height:0;vertical-align:middle;flex:none}",
    ".crt-stars svg{width:14px;height:14px;fill:currentColor;flex:none}",
    ".crt-stars-base{display:inline-flex;gap:2px;color:var(--border-med,var(--border-main,#4a3b69))}",
    ".crt-stars-fill{position:absolute;inset:0 auto 0 0;display:inline-flex;gap:2px;overflow:hidden;color:var(--brand-purple,#b829ea);white-space:nowrap}",
    "[dir=rtl] .crt-stars-fill{inset:0 0 0 auto}",
    ".crt-stars.crt-lg svg{width:22px;height:22px}",
    ".crt-panel{--crt-surface:var(--bg-surface,#0a0514);--crt-line:var(--border-dim,var(--border-main,#2a1f3d));--crt-dim:var(--text-dim,var(--text-muted,#8b7ea8));display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));gap:1px;background:var(--crt-line);border:1px solid var(--crt-line);margin-bottom:48px;font-family:var(--font-mono,monospace)}",
    ".crt-col{background:var(--crt-surface);padding:20px;min-width:0}",
    ".crt-head{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-bottom:18px}",
    ".crt-big{font-family:var(--font-display,inherit);font-size:44px;font-weight:700;line-height:1;color:var(--text-main,#e2d9f3)}",
    ".crt-sub{font-size:11px;letter-spacing:.08em;color:var(--crt-dim);text-transform:uppercase}",
    ".crt-group{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--crt-dim);margin:18px 0 6px}",
    ".crt-row{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:center;gap:4px 12px;padding:8px 0;border-bottom:1px dashed var(--crt-line);font-size:12px}",
    ".crt-row:last-child{border-bottom:0}",
    ".crt-label{color:var(--text-main,#e2d9f3);overflow-wrap:anywhere}",
    ".crt-val{display:inline-flex;align-items:center;gap:8px;white-space:nowrap;color:var(--crt-dim);font-size:11px}",
    ".crt-val b{color:var(--text-main,#e2d9f3);font-weight:700}",
    ".crt-none{color:var(--crt-dim)}",
    ".crt-form .crt-row{grid-template-columns:minmax(0,1fr) auto}",
    ".crt-pick{display:inline-flex;align-items:center;gap:2px}",
    ".crt-pick button{background:none;border:0;padding:3px;cursor:pointer;color:var(--border-med,var(--border-main,#4a3b69));line-height:0;border-radius:2px}",
    ".crt-pick button svg{width:20px;height:20px;fill:currentColor}",
    ".crt-pick button.is-on{color:var(--brand-purple,#b829ea)}",
    ".crt-pick button:hover,.crt-pick button:focus-visible{color:var(--brand-purple,#b829ea);outline:none}",
    ".crt-pick button:focus-visible{box-shadow:0 0 0 1px var(--brand-purple,#b829ea)}",
    ".crt-word{grid-column:1/-1;font-size:10px;letter-spacing:.06em;color:var(--crt-dim)}",
    ".crt-word:empty{display:none}",
    ".crt-word button{background:none;border:0;padding:0;margin-inline-start:10px;font:inherit;color:var(--crt-dim);text-decoration:underline;cursor:pointer}",
    ".crt-req{color:var(--brand-purple,#b829ea)}",
    ".crt-actions{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-top:18px}",
    ".crt-btn{font-family:var(--font-mono,monospace);font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;padding:9px 16px;border:1px solid var(--brand-purple,#b829ea);background:var(--brand-purple,#b829ea);color:#fff;cursor:pointer}",
    ".crt-btn[disabled]{opacity:.45;cursor:default}",
    ".crt-btn.crt-ghost{background:transparent;color:var(--brand-purple,#b829ea)}",
    ".crt-status{font-size:11px;color:var(--crt-dim)}",
    ".crt-note{font-size:12px;line-height:1.6;color:var(--crt-dim);margin:0 0 14px}",
    ".crt-meta-val{display:inline-flex;align-items:center;gap:6px;color:var(--text-main,#e2d9f3);text-decoration:none}",
    ".crt-meta-val:hover{color:var(--brand-purple,#b829ea)}",
    ".crt-launch{display:inline-flex;align-items:center;justify-content:center;min-height:34px;padding:7px 12px;text-decoration:none;font-size:10px}",
    ".crt-chip{display:inline-flex;align-items:center;gap:5px;font-family:var(--font-mono,monospace);font-size:11px;font-weight:700;color:var(--text-main,#e0e0e0);white-space:nowrap}",
    ".crt-chip svg{width:13px;height:13px;fill:var(--brand-purple,#b829ea)}",
    ".crt-chip-count{font-weight:400;color:var(--text-muted,var(--text-dim,#888899))}",
    ".crt-chip.crt-empty{font-weight:400;color:var(--text-muted,var(--text-dim,#888899))}",
    ".crt-chip.crt-empty svg{fill:currentColor;opacity:.5}",
    ".english-card .crt-chip{margin-top:14px}",
    ".crt-standalone{margin-top:64px;padding-top:40px;border-top:1px solid #32283f}",
    ".crt-standalone .crt-panel{--bg-surface:#140f1c;--border-dim:#32283f;--border-med:#4a3b69;--text-main:#f2edf8;--text-dim:#a296b4;--brand-purple:#c27df0;margin-bottom:0}",
    ".crt-standalone h2{font-size:30px;font-weight:500;letter-spacing:-.03em;margin:8px 0 24px}",
    ".crt-tips-section{margin-top:36px}",
    ".crt-tips-list{display:grid;gap:10px;margin:14px 0}",
    ".crt-tip{border:1px solid var(--crt-line);background:var(--crt-surface);padding:14px 16px}",
    ".crt-tip-head{display:flex;justify-content:space-between;gap:12px;align-items:center;color:var(--crt-dim);font-size:10px;letter-spacing:.08em;text-transform:uppercase}",
    ".crt-tip h3{font:700 12px/1.5 var(--font-mono,monospace);color:var(--text-main,#e2d9f3);margin:10px 0 4px}",
    ".crt-tip p{font:400 13px/1.7 var(--font-sans, sans-serif);color:var(--text-main,#e2d9f3);white-space:pre-wrap;margin:0}",
    ".crt-tip-form{display:grid;gap:12px;margin-top:18px}",
    ".crt-tip-form label{display:grid;gap:6px;font:700 10px/1.4 var(--font-mono,monospace);letter-spacing:.08em;text-transform:uppercase;color:var(--crt-dim)}",
    ".crt-tip-form input,.crt-tip-form textarea{width:100%;box-sizing:border-box;padding:10px 12px;border:1px solid var(--crt-line);background:var(--bg-void,#05020a);color:var(--text-main,#e2d9f3);font:400 13px/1.6 var(--font-sans,sans-serif);letter-spacing:normal;text-transform:none}",
    ".crt-tip-form textarea{min-height:100px;resize:vertical}",
    ".crt-tip-delete{border:0;background:none;color:var(--crt-dim);font:inherit;text-decoration:underline;cursor:pointer}",
    ".crt-section-note{margin:0 0 14px;color:var(--crt-dim);font:400 12px/1.6 var(--font-sans,sans-serif)}",
    ".crt-tool-list,.crt-checklist,.crt-community-list{display:grid;gap:10px;margin:12px 0}",
    ".crt-tool,.crt-community-post{border:1px solid var(--crt-line);padding:12px 14px;background:var(--crt-surface)}",
    ".crt-tool strong,.crt-community-post strong{display:block;color:var(--text-main,#e2d9f3);font:700 12px/1.5 var(--font-mono,monospace)}",
    ".crt-tool p,.crt-community-post p{margin:5px 0;color:var(--crt-dim);font:400 12px/1.6 var(--font-sans,sans-serif);white-space:pre-wrap}",
    ".crt-tool a{display:inline-block;margin-top:8px;color:var(--brand-purple,#b829ea);font-size:11px}",
    ".crt-check{display:flex;align-items:flex-start;gap:9px;color:var(--text-main,#e2d9f3);font:400 12px/1.5 var(--font-sans,sans-serif)}",
    ".crt-check input{margin-top:3px;accent-color:var(--brand-purple,#b829ea)}",
    ".crt-post-actions{display:flex;align-items:center;gap:12px;margin-top:10px;color:var(--crt-dim);font-size:10px}",
    ".crt-vote{border:1px solid var(--crt-line);background:transparent;color:var(--text-main,#e2d9f3);padding:5px 9px;cursor:pointer;font:inherit}",
    ".crt-community-form{display:grid;gap:10px;margin-top:16px}",
    ".crt-community-form label{display:grid;gap:5px;color:var(--crt-dim);font:700 10px/1.4 var(--font-mono,monospace);text-transform:uppercase}",
    ".crt-community-form input,.crt-community-form select,.crt-community-form textarea{width:100%;box-sizing:border-box;padding:9px 11px;border:1px solid var(--crt-line);background:var(--bg-void,#05020a);color:var(--text-main,#e2d9f3);font:400 12px/1.5 var(--font-sans,sans-serif);text-transform:none;letter-spacing:normal}",
    ".crt-community-form textarea{min-height:80px;resize:vertical}",
    ".crt-compare-pick{border:1px solid var(--crt-line,#2a1f3d);background:transparent;color:var(--crt-dim,#8b7ea8);font:700 9px/1.2 var(--font-mono,monospace);padding:5px 7px;cursor:pointer}",
    ".crt-compare-pick[aria-pressed=true]{border-color:var(--brand-purple,#b829ea);color:var(--brand-purple,#b829ea)}",
    ".crt-compare-box{margin-top:18px;padding:14px;border:1px solid var(--crt-line,#2a1f3d);background:var(--crt-surface,#0a0514);font-family:var(--font-mono,monospace)}",
    ".crt-compare-box table{width:100%;border-collapse:collapse;font-size:11px}",
    ".crt-compare-box th,.crt-compare-box td{padding:8px;text-align:start;border-bottom:1px solid var(--crt-line,#2a1f3d)}",
    "@media (max-width:480px){.crt-col{padding:16px 14px}.crt-chip-count{display:none}.crt-pick button svg{width:24px;height:24px}}",
  ].join("\n");

  function injectStyle() {
    if (document.getElementById("crt-style")) return;
    var s = document.createElement("style");
    s.id = "crt-style";
    s.textContent = STYLE;
    document.head.appendChild(s);
  }

  // ── Course overview ──────────────────────────────────────────────────────

  /** English + Arabic text of each "Weight of Assessments" item. */
  function assessments() {
    var label = document.getElementById("section-weight-of-assessments");
    var list = label && label.nextElementSibling;
    if (!list) return [];
    return Array.prototype.map.call(
      list.querySelectorAll(".topic-name"),
      function (node) {
        var html = node.dataset.arOriginalHtml;
        var en = node.textContent;
        if (html) {
          var tmp = document.createElement("div");
          tmp.innerHTML = html;
          en = tmp.textContent;
        }
        return {
          en: en.replace(/\s+/g, " ").trim(),
          ar: (node.getAttribute("data-ar-text") || "").trim(),
        };
      },
    );
  }

  // "Midterm — Week 8" -> "Midterm", "Quizzes - lowest score dropped" ->
  // "Quizzes", but "Lab Final Exam - Practical" keeps its suffix.
  function cleanLabel(s) {
    return s
      .split(/\s+[—–]\s+|\s*\(|,\s|،\s?/)[0]
      .replace(/\s+-\s+[a-z].*$/, "")
      .trim();
  }

  function isExam(en) {
    return (
      /\b(final|mid-?terms?|mid|major|exams?|examination|quiz(?:zes)?|quiz\s*\d)\b/i.test(
        en,
      ) && !/component|total/i.test(en)
    );
  }

  function slug(s) {
    return s
      .toLowerCase()
      .replace(/&/g, "and")
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-|-$/g, "")
      .slice(0, 40);
  }

  function categories() {
    var items = assessments();
    var cats = [
      {
        key: "overall",
        group: "course",
        scale: "quality",
        required: true,
        en: "Overall",
        ar: "التقييم العام",
      },
      {
        key: "workload",
        group: "course",
        scale: "load",
        en: "Workload",
        ar: "عبء العمل",
      },
      {
        key: "assignmentDifficulty",
        group: "work",
        scale: "difficulty",
        en: "Assignment difficulty",
        ar: "صعوبة الواجبات",
      },
      {
        key: "assignmentLength",
        group: "work",
        scale: "length",
        en: "Assignment length",
        ar: "طول الواجبات",
      },
    ];
    var rest = items.filter(function (i) {
      return !isExam(i.en);
    });
    if (
      rest.some(function (i) {
        return /project/i.test(i.en);
      })
    )
      cats.push({
        key: "projectDifficulty",
        group: "work",
        scale: "difficulty",
        en: "Project difficulty",
        ar: "صعوبة المشروع",
      });
    if (
      rest.some(function (i) {
        return /\blabs?\b/i.test(i.en);
      })
    )
      cats.push({
        key: "labDifficulty",
        group: "work",
        scale: "difficulty",
        en: "Lab difficulty",
        ar: "صعوبة المعامل",
      });

    var exams = items.filter(function (i) {
      return isExam(i.en);
    });
    if (!exams.length)
      exams = [
        { en: "Midterm", ar: "الاختبار الفصلي" },
        { en: "Final Exam", ar: "الاختبار النهائي" },
      ];
    var seen = {};
    exams.slice(0, MAX_EXAMS).forEach(function (e) {
      var en = cleanLabel(e.en) || e.en;
      var id = slug(en);
      if (!id || seen[id]) return;
      seen[id] = true;
      cats.push({
        key: "exams." + id,
        exam: id,
        group: "exams",
        scale: "difficulty",
        en: en,
        ar: e.ar ? cleanLabel(e.ar) : "",
      });
    });
    return cats;
  }

  var GROUPS = [
    { id: "course", en: "Course", ar: "المقرر" },
    { id: "work", en: "Coursework", ar: "الأعمال الفصلية" },
    { id: "exams", en: "Exam difficulty", ar: "صعوبة الاختبارات" },
  ];

  function readScore(doc, cat) {
    if (!doc) return null;
    var v = cat.exam ? doc.exams && doc.exams[cat.exam] : doc[cat.key];
    return validScore(v) ? v : null;
  }

  function initOverview(course) {
    var cats = categories();
    var host;
    var tipsHost;
    var faq = document.querySelector(".course-faq");
    var article = document.querySelector(".content-section");
    var panel = document.createElement("div");
    panel.className = "crt-panel";
    panel.setAttribute("aria-live", "polite");

    if (article) {
      var nums = Array.prototype.map.call(
        article.querySelectorAll(".section-label"),
        function (l) {
          return parseInt(l.textContent, 10) || 0;
        },
      );
      var next = Math.max.apply(null, nums.concat(0)) + 1;
      var label = document.createElement("div");
      label.className = "section-label";
      label.id = "section-course-ratings";
      label.textContent = (next < 10 ? "0" : "") + next + "_COURSE_RATINGS";
      article.appendChild(label);
      article.appendChild(panel);
      var tipsLabel = document.createElement("div");
      tipsLabel.className = "section-label";
      tipsLabel.id = "section-course-tips";
      tipsLabel.textContent = (next + 1 < 10 ? "0" : "") + (next + 1) + "_STUDENT_TIPS";
      article.appendChild(tipsLabel);
      tipsHost = document.createElement("div");
      tipsHost.className = "crt-panel crt-tips-panel";
      article.appendChild(tipsHost);
    } else if (faq) {
      host = document.createElement("section");
      host.className = "crt-standalone";
      host.id = "section-course-ratings";
      host.setAttribute("aria-labelledby", "crt-title");
      host.innerHTML =
        '<p class="eyebrow">Student ratings</p><h2 id="crt-title">How students rate this course.</h2>';
      host.appendChild(panel);
      faq.parentNode.insertBefore(host, faq);
      tipsHost = document.createElement("div");
      tipsHost.className = "crt-panel crt-tips-panel";
      faq.parentNode.insertBefore(tipsHost, faq);
    } else {
      return;
    }

    var meta = document.querySelector(".meta-content");
    var metaVal = null;
    if (meta) {
      var row = document.createElement("div");
      row.className = "meta-row crt-meta-row";
      row.innerHTML =
        '<span class="meta-key">RATING</span><a class="meta-val crt-meta-val" href="#section-course-ratings"></a>';
      var before = meta.querySelector(".meta-links-title");
      meta.insertBefore(row, before || null);
      metaVal = row.querySelector("a");
      metaVal.addEventListener("click", function (e) {
        var target = document.getElementById("section-course-ratings");
        if (!target) return;
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      });
      var rateRow = document.createElement("div");
      rateRow.className = "meta-row crt-rate-row";
      rateRow.innerHTML =
        '<span class="meta-key">' + esc(L("YOUR RATING", "تقييمك")) + '</span><a class="crt-btn crt-launch" href="#section-course-ratings">' +
        esc(L("Rate this course ★", "قيّم هذا المقرر ★")) + "</a>";
      meta.insertBefore(rateRow, before || null);
      rateRow.querySelector("a").addEventListener("click", function (e) {
        var target = document.getElementById("section-course-ratings");
        if (!target) return;
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
        window.setTimeout(function () {
          var first = panel.querySelector('[data-crt-key="overall"]') || panel.querySelector("[data-crt-signin]");
          if (first) first.focus();
        }, 350);
      });
      var tipsRow = document.createElement("div");
      tipsRow.className = "meta-row crt-tips-link-row";
      tipsRow.innerHTML = '<span class="meta-key">' + esc(L("STUDENT TIPS", "نصائح الطلاب")) +
        '</span><a class="meta-val crt-meta-val" href="#section-course-tips">' + esc(L("View / share tips", "عرض / مشاركة النصائح")) + "</a>";
      meta.insertBefore(tipsRow, before || null);
      var tipsRow = document.createElement("div");
      tipsRow.className = "meta-row crt-tips-link-row";
      tipsRow.innerHTML = '<span class="meta-key">' + esc(L("STUDENT TIPS", "نصائح الطلاب")) +
        '</span><a class="meta-val crt-meta-val" href="#section-course-tips">' + esc(L("View / share tips", "عرض / مشاركة النصائح")) + "</a>";
      meta.insertBefore(tipsRow, before || null);
    }

    var state = {
      fb: null,
      user: undefined,
      docs: [],
      mine: null,
      draft: {},
      loaded: false,
      failed: false,
      saving: false,
      status: null,
      focus: null,
    };

    var tipsState = { user: undefined, items: [], posts: [], loading: true, failed: false, saving: false, clearDraft: false, message: "" };

    var toolCatalog = {
      cs331: [
        { name: "Wireshark", note: "Needed for the Wireshark packet-capture lab.", url: "https://www.wireshark.org/download.html" },
        { name: "Cisco Packet Tracer", note: "Needed for the two Packet Tracer network projects.", url: "https://skillsforall.com/resources/lab-downloads" },
      ],
    };
    var requiredTools = toolCatalog[course] || [];
    var prepDefaults = [
      "Read the syllabus and note grading weights and major deadlines.",
      "Review the listed prerequisites and refresh unfamiliar topics.",
      "Open the course resources and identify the first topics to study.",
    ].concat(requiredTools.map(function (tool) { return "Install and open " + tool.name + " before its first lab or project."; }));

    function helpful(ref) {
      if (!tipsState.user || !tipsState.fb) {
        if (typeof window.__shougOpenAuthModal === "function") window.__shougOpenAuthModal();
        else if (typeof window.__shougLoadFirebaseAuth === "function") window.__shougLoadFirebaseAuth(true);
        return;
      }
      tipsState.fb.firestore().runTransaction(function (tx) {
        return tx.get(ref).then(function (snap) {
          if (!snap.exists) return;
          var data = snap.data(), votes = data.helpfulBy || {}, uid = tipsState.user.uid;
          if (votes[uid]) {
            delete votes[uid];
            tx.update(ref, { helpfulBy: votes, helpfulCount: Math.max(0, (Number(data.helpfulCount) || 0) - 1) });
          } else {
            votes[uid] = true;
            tx.update(ref, { helpfulBy: votes, helpfulCount: (Number(data.helpfulCount) || 0) + 1 });
          }
        });
      }).catch(function () {
        tipsState.message = L("Couldn't update your vote. Try again.", "تعذر تحديث تصويتك. حاول مجددًا.");
        renderTips();
      });
    }

    function tipsHtml() {
      var html = '<div class="crt-col"><div class="crt-group" style="margin-top:0">' +
        esc(L("Student tips & focus", "نصائح الطلاب والتركيز")) +
        '</div><p class="crt-note">' + esc(L("Share what helped you and what future students should focus on.", "شارك ما ساعدك وما ينبغي للطلاب التركيز عليه.")) + "</p>";
      if (tipsState.loading) html += '<p class="crt-note">' + esc(L("Loading tips…", "جارٍ تحميل النصائح…")) + "</p>";
      else if (tipsState.failed) html += '<p class="crt-note">' + esc(L("Tips are unavailable right now.", "النصائح غير متاحة حاليًا.")) + "</p>";
      else if (!tipsState.items.length) html += '<p class="crt-note">' + esc(L("No tips yet. Be the first to help the next student.", "لا توجد نصائح بعد. كن أول من يساعد الطلاب.")) + "</p>";
      else {
        html += '<div class="crt-tips-list">' + tipsState.items.map(function (tip) {
          var date = tip.createdAt && typeof tip.createdAt.toDate === "function" ? tip.createdAt.toDate() : null;
          return '<article class="crt-tip"><div class="crt-tip-head"><span>' + esc(L("Student tip", "نصيحة طالب")) +
            (date ? " · " + esc(date.toLocaleDateString(isArabic() ? "ar" : "en", { year: "numeric", month: "short", day: "numeric" })) : "") +
            "</span>" + (tipsState.user && tip.uid === tipsState.user.uid ? '<button class="crt-tip-delete" type="button" data-tip-delete="' + esc(tip.id) + '">' + esc(L("Delete", "حذف")) + "</button>" : "") +
            "</div><h3>" + esc(tip.focus) + "</h3><p>" + esc(tip.tip) + '</p><div class="crt-post-actions"><button class="crt-vote" type="button" data-tip-vote="' + esc(tip.id) + '" aria-pressed="' + Boolean(tipsState.user && tip.helpfulBy && tip.helpfulBy[tipsState.user.uid]) + '">' + esc(L("Helpful", "مفيد")) + " · " + (Number(tip.helpfulCount) || 0) + "</button></div></article>";
        }).join("") + "</div>";
      }
      if (tipsState.user === undefined) html += '<p class="crt-note">' + esc(L("Checking sign-in…", "جارٍ التحقق من تسجيل الدخول…")) + "</p>";
      else if (!tipsState.user) html += '<button class="crt-btn" type="button" data-tip-signin>' + esc(L("Sign in to share a tip", "سجّل الدخول لمشاركة نصيحة")) + "</button>";
      else html += '<form class="crt-tip-form"><label>' + esc(L("What should students focus on?", "ما الذي ينبغي للطلاب التركيز عليه؟")) +
        '<input name="focus" maxlength="140" required placeholder="' + esc(L("e.g. Practice the design patterns", "مثال: تدرب على أنماط التصميم")) + '"></label><label>' +
        esc(L("Tips and tricks", "نصائح وحيل")) + '<textarea name="tip" maxlength="1200" minlength="20" required placeholder="' +
        esc(L("Share a practical study tip, useful resource, or common pitfall…", "شارك نصيحة دراسية أو مصدرًا مفيدًا أو خطأً شائعًا…")) +
        '"></textarea></label><button class="crt-btn" type="submit"' + (tipsState.saving ? " disabled" : "") + ">" + esc(L("Share tip", "شارك النصيحة")) + '</button><span class="crt-status" role="status">' + esc(tipsState.message) + "</span></form>";

      html += '<div class="crt-group">' + esc(L("Get ready for this course", "استعد لهذا المقرر")) + "</div>";
      html += '<div class="crt-tool-list">' + (requiredTools.length ? requiredTools.map(function (tool) {
        return '<div class="crt-tool"><strong>' + esc(tool.name) + "</strong><p>" + esc(tool.note) + '</p><a href="' + esc(tool.url) + '" target="_blank" rel="noopener noreferrer">' + esc(L("Official download / access", "التنزيل أو الوصول الرسمي")) + " ↗</a></div>";
      }).join("") : '<p class="crt-section-note">' + esc(L("No required downloads have been confirmed in the course materials yet. Students can suggest a tool below.", "لم يتم تأكيد برامج مطلوبة في مواد المقرر بعد. يمكن للطلاب اقتراح أداة أدناه.")) + "</p>") + "</div>";
      var prep = {};
      try { prep = JSON.parse(localStorage.getItem("course-prep-" + course) || "{}"); } catch (e) {}
      html += '<div class="crt-checklist">' + prepDefaults.map(function (item, index) {
        return '<label class="crt-check"><input type="checkbox" data-prep-index="' + index + '" ' + (prep[index] ? "checked" : "") + ">" + esc(item) + "</label>";
      }).join("") + "</div>";

      html += '<div class="crt-group">' + esc(L("Student resources & course reports", "مصادر الطلاب وتقارير المقرر")) + "</div>";
      if (!tipsState.posts.length) html += '<p class="crt-section-note">' + esc(L("Recommend a useful resource or share what an assignment or exam covered.", "رشح مصدرًا مفيدًا أو شارك ما تناوله واجب أو اختبار.")) + "</p>";
      else html += '<div class="crt-community-list">' + tipsState.posts.map(function (post) {
        var typeName = post.type === "resource" ? L("Resource", "مصدر") : post.type === "assignment-report" ? L("Assignment report", "تقرير واجب") : post.type === "exam-report" ? L("Exam report", "تقرير اختبار") : L("Tool suggestion", "اقتراح أداة");
        return '<article class="crt-community-post"><div class="crt-tip-head"><span>' + esc(typeName) + "</span>" +
          (tipsState.user && post.uid === tipsState.user.uid ? '<button class="crt-tip-delete" type="button" data-post-delete="' + esc(post.id) + '">' + esc(L("Delete", "حذف")) + "</button>" : "") +
          "</div><strong>" + esc(post.title) + "</strong><p>" + esc(post.body) + "</p>" + (post.url ? '<p><a href="' + esc(post.url) + '" target="_blank" rel="noopener noreferrer">' + esc(post.url) + " ↗</a></p>" : "") +
          (post.hours ? '<p>' + esc(L("Estimated time", "الوقت المتوقع")) + ": " + esc(post.hours) + "h</p>" : "") +
          (post.difficulty ? '<p>' + esc(L("Difficulty", "الصعوبة")) + ": " + esc(post.difficulty) + "/5</p>" : "") +
          '<div class="crt-post-actions"><button class="crt-vote" type="button" data-post-vote="' + esc(post.id) + '" aria-pressed="' + Boolean(tipsState.user && post.helpfulBy && post.helpfulBy[tipsState.user.uid]) + '">' + esc(L("Helpful", "مفيد")) + " · " + (Number(post.helpfulCount) || 0) + "</button></div></article>";
      }).join("") + "</div>";
      if (tipsState.user) html += '<form class="crt-community-form"><label>' + esc(L("Contribution type", "نوع المشاركة")) + '<select name="type"><option value="resource">' + esc(L("Recommend a resource", "رشح مصدرًا")) + '</option><option value="assignment-report">' + esc(L("Assignment report", "تقرير واجب")) + '</option><option value="exam-report">' + esc(L("Exam report", "تقرير اختبار")) + '</option><option value="tool">' + esc(L("Suggest a required tool", "اقترح أداة مطلوبة")) + '</option></select></label><label>' + esc(L("Title / assignment or exam", "العنوان / الواجب أو الاختبار")) + '<input name="title" maxlength="120" required></label><label>' + esc(L("What should students know?", "ماذا ينبغي أن يعرف الطلاب؟")) + '<textarea name="body" maxlength="1200" minlength="20" required></textarea></label><label>' + esc(L("Resource or official download URL (optional)", "رابط المصدر أو التنزيل الرسمي (اختياري)")) + '<input name="url" type="url" maxlength="500"></label><label>' + esc(L("Estimated hours (optional)", "الساعات المتوقعة (اختياري)")) + '<input name="hours" type="number" min="0.5" max="200" step="0.5"></label><label>' + esc(L("Difficulty (optional)", "الصعوبة (اختياري)")) + '<select name="difficulty"><option value="">—</option><option value="1">1 / 5</option><option value="2">2 / 5</option><option value="3">3 / 5</option><option value="4">4 / 5</option><option value="5">5 / 5</option></select></label><button class="crt-btn" type="submit">' + esc(L("Share contribution", "شارك المساهمة")) + "</button></form>";
      else html += '<button class="crt-btn" type="button" data-tip-signin>' + esc(L("Sign in to recommend resources or report on work", "سجّل الدخول لترشيح مصادر أو مشاركة تقارير")) + "</button>";
      return html + "</div>";
    }

    function renderTips() {
      if (!tipsHost) return;
      var oldFields = {},
        active = document.activeElement,
        focusName = active && active.name;
      tipsHost.querySelectorAll(".crt-tip-form [name],.crt-community-form [name]").forEach(function (field) {
        oldFields[field.name] = field.value;
      });
      tipsHost.innerHTML = tipsHtml();
      if (!tipsState.clearDraft) {
        tipsHost.querySelectorAll(".crt-tip-form [name],.crt-community-form [name]").forEach(function (field) {
          if (Object.prototype.hasOwnProperty.call(oldFields, field.name)) field.value = oldFields[field.name];
          if (focusName && field.name === focusName) field.focus();
        });
      }
      tipsState.clearDraft = false;
      tipsHost.querySelectorAll("[data-prep-index]").forEach(function (input) {
        input.addEventListener("change", function () {
          var prep = {};
          try { prep = JSON.parse(localStorage.getItem("course-prep-" + course) || "{}"); } catch (e) {}
          prep[input.dataset.prepIndex] = input.checked;
          try { localStorage.setItem("course-prep-" + course, JSON.stringify(prep)); } catch (e) {}
        });
      });
    }

    tipsHost.addEventListener("click", function (e) {
      var button = e.target.closest("button");
      if (!button) return;
      if (button.hasAttribute("data-tip-signin")) {
        if (typeof window.__shougOpenAuthModal === "function") window.__shougOpenAuthModal();
        else if (typeof window.__shougLoadFirebaseAuth === "function") window.__shougLoadFirebaseAuth(true);
      } else if (button.hasAttribute("data-tip-delete") && tipsState.user && tipsState.fb) {
        var id = button.getAttribute("data-tip-delete");
        tipsState.fb.firestore().collection("courseRatings").doc(course).collection("tips").doc(id).delete().catch(function () {
          tipsState.failed = true;
          renderTips();
        });
      } else if (button.hasAttribute("data-tip-vote")) {
        helpful(tipsState.fb.firestore().collection("courseRatings").doc(course).collection("tips").doc(button.dataset.tipVote));
      } else if (button.hasAttribute("data-post-vote")) {
        helpful(tipsState.fb.firestore().collection("courseCommunity").doc(course).collection("posts").doc(button.dataset.postVote));
      } else if (button.hasAttribute("data-post-delete") && tipsState.user && tipsState.fb) {
        tipsState.fb.firestore().collection("courseCommunity").doc(course).collection("posts").doc(button.dataset.postDelete).delete().catch(function () {
          tipsState.message = L("Couldn't delete that contribution.", "تعذر حذف هذه المساهمة.");
          renderTips();
        });
      }
    });
    tipsHost.addEventListener("submit", function (e) {
      if (!e.target.matches(".crt-tip-form")) return;
      e.preventDefault();
      if (!tipsState.user || !tipsState.fb || tipsState.saving) return;
      var data = new FormData(e.target), focus = String(data.get("focus") || "").trim(), tip = String(data.get("tip") || "").trim();
      if (focus.length < 3 || tip.length < 20 || tip.length > 1200) return;
      tipsState.saving = true;
      tipsState.message = "";
      renderTips();
      tipsState.fb.firestore().collection("courseRatings").doc(course).collection("tips").add({
        uid: tipsState.user.uid, focus: focus, tip: tip, helpfulCount: 0, helpfulBy: {},
        createdAt: tipsState.fb.firestore.FieldValue.serverTimestamp(),
      }).then(function () {
        tipsState.saving = false;
        tipsState.clearDraft = true;
        tipsState.message = L("Tip shared. Thanks for helping other students!", "تمت مشاركة النصيحة. شكرًا لمساعدة الطلاب!");
        renderTips();
      }).catch(function () {
        tipsState.saving = false;
        tipsState.message = L("Couldn't share your tip. Check your connection and try again.", "تعذرت مشاركة النصيحة. تحقق من اتصالك وحاول مجددًا.");
        renderTips();
      });
    });
    tipsHost.addEventListener("submit", function (e) {
      if (!e.target.matches(".crt-community-form")) return;
      e.preventDefault();
      if (!tipsState.user || !tipsState.fb || tipsState.saving) return;
      var data = new FormData(e.target),
        type = String(data.get("type") || ""),
        title = String(data.get("title") || "").trim(),
        body = String(data.get("body") || "").trim(),
        url = String(data.get("url") || "").trim(),
        hours = Number(data.get("hours")),
        difficulty = Number(data.get("difficulty"));
      if (["resource", "assignment-report", "exam-report", "tool"].indexOf(type) < 0 || title.length < 3 || title.length > 120 || body.length < 20 || body.length > 1200 || (url && !/^https?:\/\//i.test(url))) return;
      tipsState.saving = true;
      renderTips();
      tipsState.fb.firestore().collection("courseCommunity").doc(course).collection("posts").add({
        uid: tipsState.user.uid, type: type, title: title, body: body, url: url,
        hours: isFinite(hours) && hours > 0 && hours <= 200 ? hours : null,
        difficulty: isFinite(difficulty) && difficulty >= 1 && difficulty <= 5 ? difficulty : null,
        helpfulCount: 0, helpfulBy: {},
        createdAt: tipsState.fb.firestore.FieldValue.serverTimestamp(),
      }).then(function () {
        tipsState.saving = false;
        tipsState.clearDraft = true;
        tipsState.message = L("Contribution shared. Thank you!", "تمت مشاركة المساهمة. شكرًا لك!");
        renderTips();
      }).catch(function () {
        tipsState.saving = false;
        tipsState.message = L("Couldn't share that contribution. Check your connection and try again.", "تعذرت مشاركة المساهمة. تحقق من اتصالك وحاول مجددًا.");
        renderTips();
      });
    });
    renderTips();
    new MutationObserver(renderTips).observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["lang"],
    });

    function draftFrom(doc) {
      var d = { term: doc && typeof doc.term === "string" ? doc.term : "" };
      cats.forEach(function (c) {
        var v = readScore(doc, c);
        if (v) d[c.key] = v;
      });
      return d;
    }

    function summaryHtml(sum) {
      var overall = sum.overall;
      var html =
        '<div class="crt-head">' +
        (overall
          ? '<span class="crt-big">' +
            fixed(overall.avg) +
            "</span>" +
            stars(overall.avg, "crt-lg") +
            '<span class="crt-sub">' +
            esc(countLabel(sum.count)) +
            "</span>"
          : '<span class="crt-sub">' +
            esc(
              state.failed
                ? L(
                    "Ratings are unavailable right now",
                    "التقييمات غير متاحة حاليًا",
                  )
                : state.loaded
                  ? L(
                      "No ratings yet — be the first",
                      "لا توجد تقييمات بعد — كن الأول",
                    )
                  : L("Loading ratings…", "جارٍ تحميل التقييمات…"),
            ) +
            "</span>") +
        "</div>";
      GROUPS.forEach(function (g) {
        var rows = cats.filter(function (c) {
          return c.group === g.id;
        });
        if (!rows.length) return;
        html += '<div class="crt-group">' + esc(L(g.en, g.ar)) + "</div>";
        rows.forEach(function (c) {
          var s = sum[c.key];
          html +=
            '<div class="crt-row"><span class="crt-label">' +
            esc(L(c.en, c.ar)) +
            "</span>" +
            (s
              ? '<span class="crt-val">' +
                stars(s.avg) +
                "<b>" +
                fixed(s.avg) +
                "</b>" +
                esc(scaleWord(c.scale, s.avg)) +
                " · " +
                s.count +
                "</span>"
              : '<span class="crt-val crt-none">—</span>') +
            "</div>";
        });
      });
      var terms = Object.keys(sum.termCounts || {}).sort().reverse();
      if (terms.length) {
        html += '<div class="crt-group">' + esc(L("Ratings by semester", "التقييمات حسب الفصل")) + "</div>" +
          terms.map(function (term) {
            return '<div class="crt-row"><span class="crt-label">' + esc(term.replace("-", " ")) + '</span><span class="crt-val">' + sum.termCounts[term] + " " + esc(L("ratings", "تقييمات")) + "</span></div>";
          }).join("");
      }
      return html;
    }

    function formHtml() {
      if (state.user === undefined)
        return (
          '<p class="crt-note">' + esc(L("Loading…", "جارٍ التحميل…")) + "</p>"
        );
      if (!state.user)
        return (
          '<div class="crt-group" style="margin-top:0">' +
          esc(L("Your rating", "تقييمك")) +
          '</div><p class="crt-note">' +
          esc(
            L(
              "Took this course? Sign in to rate it out of five stars — overall, workload, assignments and each exam.",
              "درست هذا المقرر؟ سجّل الدخول لتقييمه من خمس نجوم — التقييم العام وعبء العمل والواجبات وكل اختبار.",
            ),
          ) +
          '</p><button type="button" class="crt-btn" data-crt-signin>' +
          esc(L("Sign in to rate", "سجّل الدخول للتقييم")) +
          "</button>"
        );

      var html =
        '<div class="crt-form"><div class="crt-group" style="margin-top:0">' +
        esc(
          L(
            state.mine ? "Your rating" : "Rate this course",
            state.mine ? "تقييمك" : "قيّم هذا المقرر",
          ),
        ) +
        '</div><p class="crt-note">' +
        esc(
          L(
            "Only Overall is required — skip anything that didn't apply to you. Difficulty and length: more stars means harder or longer.",
            "التقييم العام فقط مطلوب — تجاوز ما لا ينطبق عليك. في الصعوبة والطول: نجوم أكثر تعني أصعب أو أطول.",
          ),
        ) +
        "</p><label class=\"crt-term-label\">" + esc(L("Semester taken (optional)", "الفصل الدراسي (اختياري)")) +
        '<select data-crt-term><option value="">' + esc(L("Prefer not to say", "أفضل عدم الإجابة")) + "</option>" +
        ratingTerms().map(function (term) {
          return '<option value="' + esc(term.value) + '"' + (state.draft.term === term.value ? " selected" : "") + ">" + esc(term.label) + "</option>";
        }).join("") + "</select></label>";
      GROUPS.forEach(function (g) {
        var rows = cats.filter(function (c) {
          return c.group === g.id;
        });
        if (!rows.length) return;
        html += '<div class="crt-group">' + esc(L(g.en, g.ar)) + "</div>";
        rows.forEach(function (c) {
          var v = state.draft[c.key] || 0;
          var name = L(c.en, c.ar);
          html +=
            '<div class="crt-row"><span class="crt-label">' +
            esc(name) +
            (c.required ? ' <span class="crt-req">*</span>' : "") +
            '</span><span class="crt-pick" role="group" aria-label="' +
            esc(name) +
            '">';
          for (var n = 1; n <= 5; n++) {
            html +=
              '<button type="button" data-crt-key="' +
              c.key +
              '" data-crt-n="' +
              n +
              '" class="' +
              (n <= v ? "is-on" : "") +
              '" aria-pressed="' +
              (n === v) +
              '" aria-label="' +
              esc(name + ": " + n + "/5 — " + scaleWord(c.scale, n)) +
              '">' +
              STAR +
              "</button>";
          }
          html +=
            '</span><span class="crt-word">' +
            (v
              ? esc(scaleWord(c.scale, v)) +
                (c.required
                  ? ""
                  : '<button type="button" data-crt-clear="' +
                    c.key +
                    '">' +
                    esc(L("Clear", "مسح")) +
                    "</button>")
              : "") +
            "</span></div>";
        });
      });
      html +=
        '<div class="crt-actions"><button type="button" class="crt-btn" data-crt-save' +
        (state.draft.overall && !state.saving ? "" : " disabled") +
        ">" +
        esc(
          state.mine
            ? L("Update rating", "تحديث التقييم")
            : L("Submit rating", "إرسال التقييم"),
        ) +
        "</button>" +
        (state.mine
          ? '<button type="button" class="crt-btn crt-ghost" data-crt-delete' +
            (state.saving ? " disabled" : "") +
            ">" +
            esc(L("Remove", "حذف")) +
            "</button>"
          : "") +
        '<span class="crt-status" role="status">' +
        esc(state.status ? L(state.status[0], state.status[1]) : "") +
        "</span></div></div>";
      return html;
    }

    function render() {
      var sum = summarize(state.docs);
      panel.innerHTML =
        '<div class="crt-col">' +
        summaryHtml(sum) +
        '</div><div class="crt-col">' +
        formHtml() +
        "</div>";
      if (metaVal) {
        metaVal.innerHTML = sum.overall
          ? stars(sum.overall.avg) +
            " " +
            fixed(sum.overall.avg) +
            " (" +
            sum.count +
            ")"
          : esc(L("Not rated yet", "لم يُقيَّم بعد"));
      }
      if (state.focus) {
        var f = panel.querySelector(state.focus);
        if (f) f.focus();
        state.focus = null;
      }
    }

    function save() {
      if (!state.user || !state.draft.overall || state.saving) return;
      var data = { uid: state.user.uid };
      var exams = {};
      cats.forEach(function (c) {
        var v = state.draft[c.key];
        if (!validScore(v)) return;
        if (c.exam) exams[c.exam] = v;
        else data[c.key] = v;
      });
      if (Object.keys(exams).length) data.exams = exams;
      if (state.draft.term) data.term = state.draft.term;
      data.updatedAt = state.fb.firestore.FieldValue.serverTimestamp();
      state.saving = true;
      state.status = ["Saving…", "جارٍ الحفظ…"];
      render();
      ratingsRef(state.fb, course)
        .doc(state.user.uid)
        .set(data)
        .then(function () {
          state.status = [
            "Saved. Thanks for rating!",
            "تم الحفظ. شكرًا لتقييمك!",
          ];
        })
        .catch(function () {
          state.status = [
            "Couldn't save — try again.",
            "تعذّر الحفظ — حاول مرة أخرى.",
          ];
        })
        .then(function () {
          state.saving = false;
          render();
        });
    }

    function remove() {
      if (!state.user || !state.mine || state.saving) return;
      state.saving = true;
      render();
      ratingsRef(state.fb, course)
        .doc(state.user.uid)
        .delete()
        .then(function () {
          state.draft = {};
          state.status = ["Your rating was removed.", "تم حذف تقييمك."];
        })
        .catch(function () {
          state.status = [
            "Couldn't remove — try again.",
            "تعذّر الحذف — حاول مرة أخرى.",
          ];
        })
        .then(function () {
          state.saving = false;
          render();
        });
    }

    panel.addEventListener("click", function (e) {
      var t = e.target.closest("button");
      if (!t || !panel.contains(t)) return;
      if (t.hasAttribute("data-crt-signin")) {
        if (typeof window.__shougOpenAuthModal === "function")
          window.__shougOpenAuthModal();
        else if (typeof window.__shougLoadFirebaseAuth === "function")
          window.__shougLoadFirebaseAuth(true);
      } else if (t.hasAttribute("data-crt-key")) {
        var key = t.getAttribute("data-crt-key");
        var n = +t.getAttribute("data-crt-n");
        state.draft[key] = n;
        state.status = null;
        state.focus = '[data-crt-key="' + key + '"][data-crt-n="' + n + '"]';
        render();
      } else if (t.hasAttribute("data-crt-clear")) {
        var ck = t.getAttribute("data-crt-clear");
        delete state.draft[ck];
        state.focus = '[data-crt-key="' + ck + '"][data-crt-n="1"]';
        render();
      } else if (t.hasAttribute("data-crt-save")) {
        save();
      } else if (t.hasAttribute("data-crt-delete")) {
        remove();
      }
    });
    panel.addEventListener("change", function (e) {
      if (e.target.matches("[data-crt-term]")) state.draft.term = e.target.value;
    });

    new MutationObserver(render).observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["lang"],
    });
    render();

    withFirebase(function (fb) {
      state.fb = fb;
      ratingsRef(fb, course)
        .limit(1000)
        .onSnapshot(
          function (snap) {
            state.docs = snap.docs.map(function (d) {
              return d.data();
            });
            state.loaded = true;
            state.failed = false;
            syncMine();
            render();
          },
          function () {
            state.failed = true;
            render();
          },
        );
      fb.auth().onAuthStateChanged(function (user) {
        state.user = user || null;
        tipsState.user = user || null;
        state.status = null;
        syncMine(true);
        render();
        renderTips();
      });
      tipsState.fb = fb;
      fb.firestore().collection("courseRatings").doc(course).collection("tips")
        .limit(100)
        .onSnapshot(function (snap) {
          tipsState.items = snap.docs.map(function (d) {
            return Object.assign({ id: d.id }, d.data());
          }).sort(function (a, b) {
            var ta = a.createdAt && typeof a.createdAt.toMillis === "function" ? a.createdAt.toMillis() : 0;
            var tb = b.createdAt && typeof b.createdAt.toMillis === "function" ? b.createdAt.toMillis() : 0;
            return tb - ta;
          });
          tipsState.loading = false;
          tipsState.failed = false;
          renderTips();
        }, function () {
          tipsState.loading = false;
          tipsState.failed = true;
          renderTips();
        });
      fb.firestore().collection("courseCommunity").doc(course).collection("posts")
        .limit(100)
        .onSnapshot(function (snap) {
          tipsState.posts = snap.docs.map(function (d) {
            return Object.assign({ id: d.id }, d.data());
          }).sort(function (a, b) {
            var ta = a.createdAt && typeof a.createdAt.toMillis === "function" ? a.createdAt.toMillis() : 0;
            var tb = b.createdAt && typeof b.createdAt.toMillis === "function" ? b.createdAt.toMillis() : 0;
            return tb - ta;
          });
          renderTips();
        }, function () {
          tipsState.message = L("Student contributions are unavailable right now.", "مساهمات الطلاب غير متاحة حاليًا.");
          renderTips();
        });
    });

    function syncMine(reset) {
      var uid = state.user && state.user.uid;
      var prev = state.mine;
      state.mine = null;
      if (uid)
        state.docs.forEach(function (d) {
          if (d.uid === uid) state.mine = d;
        });
      // Seed the form from the saved rating unless the student is mid-edit.
      if (reset || !prev || !state.mine) state.draft = draftFrom(state.mine);
    }
  }

  // ── Track pages ──────────────────────────────────────────────────────────

  function initTrack() {
    var cards = Array.prototype.filter.call(
      document.querySelectorAll("a.course-row[href], a.english-card[href]"),
      function (a) {
        if (a.closest(".english-resources")) return false;
        return /\/([a-z]+\d{3})\/$/.test(a.getAttribute("href"));
      },
    );
    if (!cards.length) return;
    var selected = [],
      summaries = {},
      metricRows = [
        ["overall", "Overall"],
        ["workload", "Workload"],
        ["assignmentDifficulty", "Assignment difficulty"],
        ["assignmentLength", "Assignment length"],
        ["projectDifficulty", "Project difficulty"],
        ["labDifficulty", "Lab difficulty"],
      ],
      compare = document.createElement("section");
    compare.className = "crt-compare-box";
    compare.innerHTML = '<strong>' + esc(L("Compare courses", "قارن المقررات")) + '</strong><p class="crt-section-note">' +
      esc(L("Choose up to four courses using the Compare buttons.", "اختر حتى أربعة مقررات باستخدام أزرار المقارنة.")) + "</p>";
    var list = cards[0].closest(".course-list");
    if (list) list.insertAdjacentElement("afterend", compare);
    function renderCompare() {
      if (selected.length < 2) {
        compare.innerHTML = '<strong>' + esc(L("Compare courses", "قارن المقررات")) + '</strong><p class="crt-section-note">' +
          esc(L(selected.length ? "Choose one more course to compare." : "Choose up to four courses using the Compare buttons.", selected.length ? "اختر مقررًا آخر للمقارنة." : "اختر حتى أربعة مقررات باستخدام أزرار المقارنة.")) + "</p>";
        return;
      }
      var rows = metricRows.map(function (row) {
        return "<tr><th>" + esc(L(row[1], row[1])) + "</th>" + selected.map(function (code) {
          var score = summaries[code] && summaries[code][row[0]];
          return "<td>" + (score ? fixed(score.avg) + "/5 · " + score.count : "—") + "</td>";
        }).join("") + "</tr>";
      });
      rows.push("<tr><th>" + esc(L("Exam difficulty (average)", "متوسط صعوبة الاختبارات")) + "</th>" + selected.map(function (code) {
        var s = summaries[code] || {}, values = Object.keys(s).filter(function (key) { return key.indexOf("exams.") === 0; }).map(function (key) { return s[key]; });
        var total = values.reduce(function (sum, value) { return sum + value.avg * value.count; }, 0),
          count = values.reduce(function (sum, value) { return sum + value.count; }, 0);
        return "<td>" + (count ? fixed(total / count) + "/5 · " + count : "—") + "</td>";
      }).join("") + "</tr>");
      compare.innerHTML = '<strong>' + esc(L("Course comparison", "مقارنة المقررات")) + '</strong><table><thead><tr><th></th>' +
        selected.map(function (code) { return "<th>" + esc(code.toUpperCase()) + "</th>"; }).join("") +
        "</tr></thead><tbody>" + rows.join("") + "</tbody></table>";
    }
    withFirebase(function (fb) {
      cards.forEach(function (a) {
        var course = a.getAttribute("href").match(/\/([a-z]+\d{3})\/$/)[1];
        var area = a.querySelector(".course-status-area");
        if (area) {
          var pick = document.createElement("button");
          pick.className = "crt-compare-pick";
          pick.type = "button";
          pick.textContent = L("Compare", "قارن");
          pick.setAttribute("aria-pressed", "false");
          pick.addEventListener("click", function (e) {
            e.preventDefault();
            e.stopPropagation();
            var index = selected.indexOf(course);
            if (index > -1) selected.splice(index, 1);
            else if (selected.length < 4) selected.push(course);
            else return;
            pick.setAttribute("aria-pressed", String(selected.indexOf(course) > -1));
            pick.textContent = selected.indexOf(course) > -1 ? L("Selected", "محدد") : L("Compare", "قارن");
            renderCompare();
          });
          area.appendChild(pick);
        }
        ratingsRef(fb, course)
          .limit(1000)
          .get()
          .then(function (snap) {
            var sum = summarize(
              snap.docs.map(function (d) {
                return d.data();
              }),
            );
            summaries[course] = sum;
            renderCompare();
            var chip = document.createElement("span");
            chip.className = "crt-chip" + (sum.overall ? "" : " crt-empty");
            var render = function () {
              chip.innerHTML = sum.overall
                ? STAR +
                  fixed(sum.overall.avg) +
                  '<span class="crt-chip-count">(' +
                  sum.count +
                  ")</span>"
                : STAR + esc(L("No ratings", "بلا تقييم"));
              chip.setAttribute(
                "aria-label",
                sum.overall
                  ? L(
                      "Rated " +
                        fixed(sum.overall.avg) +
                        " out of 5, " +
                        countLabel(sum.count),
                      "التقييم " +
                        fixed(sum.overall.avg) +
                        " من 5، " +
                        countLabel(sum.count),
                    )
                  : L("No ratings yet", "لا توجد تقييمات بعد"),
              );
            };
            render();
            new MutationObserver(render).observe(document.documentElement, {
              attributes: true,
              attributeFilter: ["lang"],
            });
            var area = a.querySelector(".course-status-area");
            if (area) area.insertBefore(chip, area.firstChild);
            else a.appendChild(chip);
          })
          .catch(function () {});
      });
    });
  }

  function start() {
    var m = path.match(COURSE_PATH);
    if (m) {
      injectStyle();
      initOverview(m[1]);
    } else if (TRACK_PATH.test(path)) {
      injectStyle();
      initTrack();
    }
  }

  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", start);
  else start();
})();
