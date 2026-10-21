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
    var sums = {},
      termCounts = {};
    var add = function (key, n) {
      if (!validScore(n)) return;
      var s = sums[key] || (sums[key] = { total: 0, count: 0 });
      s.total += n;
      s.count += 1;
    };
    docs.forEach(function (d) {
      var code = termCode(d.term);
      if (code) termCounts[code] = (termCounts[code] || 0) + 1;
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

  // University term codes: year + term (1 first, 2 second, 3 summer),
  // 231 through 261. Later terms are typed in through "Other".
  // Ratings saved before the codes existed used "2026-first" style values.
  function termCode(t) {
    var m =
      typeof t === "string" && t.match(/^20(\d\d)-(first|second|summer)$/);
    if (m) return m[1] + { first: 1, second: 2, summer: 3 }[m[2]];
    return typeof t === "string" ? t : "";
  }

  function ratingTerms() {
    var out = [];
    for (var y = 23; y <= 26; y++)
      for (var t = 1; t <= 3 && !(y === 26 && t > 1); t++) out.push(y + "" + t);
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
    ".shoug-light-mode .crt-btn{background:var(--brand-purple,#b829ea)!important;border-color:var(--brand-purple,#b829ea)!important;color:#fff!important}",
    ".shoug-light-mode .crt-btn.crt-ghost{background:transparent!important;color:var(--brand-purple,#b829ea)!important}",
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
    ".crt-field{display:grid;gap:6px;margin:0 0 14px}",
    ".crt-field-label{font:700 10px/1.4 var(--font-mono,monospace);letter-spacing:.12em;text-transform:uppercase;color:var(--crt-dim)}",
    ".crt-field-label span{font-weight:400;letter-spacing:.04em;text-transform:none}",
    ".crt-choices{display:flex;flex-wrap:wrap;gap:6px}",
    ".crt-choice{border:1px solid var(--crt-line);background:transparent;color:var(--text-main,#e2d9f3);font:500 12px/1 var(--font-mono,monospace);padding:8px 11px;cursor:pointer}",
    ".crt-choice:hover{border-color:var(--brand-purple,#b829ea)}",
    ".crt-choice[aria-pressed=true]{border-color:var(--brand-purple,#b829ea);background:var(--brand-purple,#b829ea);color:#fff}",
    ".crt-choice:focus-visible,.crt-input:focus-visible{outline:none;border-color:var(--brand-purple,#b829ea);box-shadow:0 0 0 1px var(--brand-purple,#b829ea)}",
    ".crt-input{width:100%;box-sizing:border-box;padding:10px 12px;border:1px solid var(--crt-line);border-radius:0;background:var(--bg-void,#05020a);color:var(--text-main,#e2d9f3);color-scheme:dark;font:400 14px/1.5 var(--font-sans,sans-serif);letter-spacing:normal;text-transform:none}",
    ".shoug-light-mode .crt-input{color-scheme:light}",
    ".crt-input::placeholder{color:var(--crt-dim);opacity:.8}",
    "textarea.crt-input{min-height:96px;resize:vertical}",
    ".crt-input.crt-short{max-width:120px}",
    ".crt-hint{font:400 11px/1.4 var(--font-sans,sans-serif);color:var(--crt-dim)}",
    ".crt-feed{display:grid;gap:10px;margin:0 0 4px}",
    ".crt-card{border:1px solid var(--crt-line);padding:14px 16px}",
    ".crt-card-head{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:8px}",
    ".crt-tag{font:700 9px/1 var(--font-mono,monospace);letter-spacing:.14em;text-transform:uppercase;color:var(--brand-purple,#b829ea);border:1px solid currentColor;padding:4px 6px}",
    ".crt-date{font:400 11px/1 var(--font-sans,sans-serif);color:var(--crt-dim)}",
    ".crt-card h3{margin:0 0 4px;font:600 14px/1.45 var(--font-sans,sans-serif);color:var(--text-main,#e2d9f3)}",
    ".crt-card p{margin:0;font:400 13px/1.65 var(--font-sans,sans-serif);color:var(--text-main,#e2d9f3);white-space:pre-wrap;overflow-wrap:anywhere}",
    ".crt-card a.crt-link{display:inline-block;margin-top:8px;font:500 12px/1.4 var(--font-sans,sans-serif);color:var(--brand-purple,#b829ea);overflow-wrap:anywhere}",
    ".crt-card-foot{display:flex;align-items:center;gap:14px;margin-top:10px}",
    ".crt-vote{border:1px solid var(--crt-line);background:transparent;color:var(--text-main,#e2d9f3);font:500 11px/1 var(--font-mono,monospace);padding:6px 9px;cursor:pointer}",
    ".crt-vote[aria-pressed=true]{border-color:var(--brand-purple,#b829ea);color:var(--brand-purple,#b829ea)}",
    ".crt-text-btn{border:0;background:none;padding:0;color:var(--crt-dim);font:400 11px/1 var(--font-sans,sans-serif);text-decoration:underline;cursor:pointer}",
    ".crt-tools{display:grid;gap:8px;margin:0 0 18px}",
    ".crt-tools a{color:var(--brand-purple,#b829ea);font:500 13px/1.5 var(--font-sans,sans-serif)}",
    ".crt-tools span{display:block;color:var(--crt-dim);font:400 12px/1.5 var(--font-sans,sans-serif)}",
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
      tipsLabel.textContent =
        (next + 1 < 10 ? "0" : "") + (next + 1) + "_STUDENT_TIPS";
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
        '<span class="meta-key">' +
        esc(L("YOUR RATING", "تقييمك")) +
        '</span><a class="crt-btn crt-launch" href="#section-course-ratings">' +
        esc(L("Rate this course ★", "قيّم هذا المقرر ★")) +
        "</a>";
      meta.insertBefore(rateRow, before || null);
      rateRow.querySelector("a").addEventListener("click", function (e) {
        var target = document.getElementById("section-course-ratings");
        if (!target) return;
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
        window.setTimeout(function () {
          var first =
            panel.querySelector('[data-crt-key="overall"]') ||
            panel.querySelector("[data-crt-signin]");
          if (first) first.focus();
        }, 350);
      });
      var tipsRow = document.createElement("div");
      tipsRow.className = "meta-row crt-tips-link-row";
      tipsRow.innerHTML =
        '<span class="meta-key">' +
        esc(L("STUDENT TIPS", "نصائح الطلاب")) +
        '</span><a class="meta-val crt-meta-val" href="#section-course-tips">' +
        esc(L("View / share tips", "عرض / مشاركة النصائح")) +
        "</a>";
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

    var tipsState = {
      user: undefined,
      items: [],
      posts: [],
      loading: true,
      failed: false,
      saving: false,
      clearDraft: false,
      message: "",
      type: "tip",
    };

    // Software a course needs, with its official download page.
    var toolCatalog = {
      cs331: [
        {
          name: "Wireshark",
          note: "Packet-capture lab",
          url: "https://www.wireshark.org/download.html",
        },
        {
          name: "Cisco Packet Tracer",
          note: "Network projects",
          url: "https://skillsforall.com/resources/lab-downloads",
        },
      ],
    };
    var requiredTools = toolCatalog[course] || [];

    // "tip" posts go to courseRatings/{course}/tips, everything else to
    // courseCommunity/{course}/posts (see firebase/course-ratings.rules).
    var POST_TYPES = [
      {
        id: "tip",
        en: "Study tip",
        ar: "نصيحة دراسية",
        title: [
          "e.g. Practice the past midterms",
          "مثال: حل الاختبارات السابقة",
        ],
        body: [
          "What helped you? Keep it short and practical.",
          "ما الذي ساعدك؟ اجعلها قصيرة وعملية.",
        ],
      },
      {
        id: "exam-report",
        en: "Exam",
        ar: "اختبار",
        title: ["e.g. Midterm", "مثال: الاختبار الفصلي"],
        body: [
          "What did it cover, and what should students focus on?",
          "ماذا شمل، وعلى ماذا يركز الطلاب؟",
        ],
      },
      {
        id: "assignment-report",
        en: "Assignment",
        ar: "واجب",
        title: ["e.g. Assignment 2", "مثال: الواجب 2"],
        body: [
          "How long did it take, and what was tricky?",
          "كم استغرق، وما الصعب فيه؟",
        ],
      },
      {
        id: "resource",
        en: "Resource",
        ar: "مصدر",
        link: true,
        title: [
          "e.g. YouTube playlist for chapter 4",
          "مثال: قائمة يوتيوب للفصل 4",
        ],
        body: ["Why is it useful?", "لماذا هو مفيد؟"],
      },
      {
        id: "tool",
        en: "Software",
        ar: "برنامج",
        link: true,
        title: ["e.g. Wireshark", "مثال: Wireshark"],
        body: ["What is it needed for?", "لماذا نحتاجه؟"],
      },
    ];
    function postType(id) {
      for (var i = 0; i < POST_TYPES.length; i++)
        if (POST_TYPES[i].id === id) return POST_TYPES[i];
      return POST_TYPES[0];
    }

    function openSignIn() {
      if (typeof window.__shougOpenAuthModal === "function")
        window.__shougOpenAuthModal();
      else if (typeof window.__shougLoadFirebaseAuth === "function")
        window.__shougLoadFirebaseAuth(true);
    }

    function feedRef(item) {
      var db = tipsState.fb.firestore();
      return item.kind === "tip"
        ? db
            .collection("courseRatings")
            .doc(course)
            .collection("tips")
            .doc(item.id)
        : db
            .collection("courseCommunity")
            .doc(course)
            .collection("posts")
            .doc(item.id);
    }

    function feed() {
      var millis = function (x) {
        return x.createdAt && typeof x.createdAt.toMillis === "function"
          ? x.createdAt.toMillis()
          : 0;
      };
      return tipsState.items
        .map(function (t) {
          return {
            kind: "tip",
            id: t.id,
            type: "tip",
            title: t.focus,
            body: t.tip,
            url: "",
            uid: t.uid,
            helpfulBy: t.helpfulBy,
            helpfulCount: t.helpfulCount,
            createdAt: t.createdAt,
          };
        })
        .concat(
          tipsState.posts.map(function (p) {
            return {
              kind: "post",
              id: p.id,
              type: p.type,
              title: p.title,
              body: p.body,
              url: p.url,
              uid: p.uid,
              helpfulBy: p.helpfulBy,
              helpfulCount: p.helpfulCount,
              createdAt: p.createdAt,
            };
          }),
        )
        .sort(function (a, b) {
          return millis(b) - millis(a);
        });
    }

    function helpful(item) {
      if (!tipsState.user || !tipsState.fb) return openSignIn();
      var ref = feedRef(item);
      tipsState.fb
        .firestore()
        .runTransaction(function (tx) {
          return tx.get(ref).then(function (snap) {
            if (!snap.exists) return;
            var data = snap.data(),
              votes = data.helpfulBy || {},
              uid = tipsState.user.uid;
            if (votes[uid]) {
              delete votes[uid];
              tx.update(ref, {
                helpfulBy: votes,
                helpfulCount: Math.max(0, (Number(data.helpfulCount) || 0) - 1),
              });
            } else {
              votes[uid] = true;
              tx.update(ref, {
                helpfulBy: votes,
                helpfulCount: (Number(data.helpfulCount) || 0) + 1,
              });
            }
          });
        })
        .catch(function () {
          tipsState.message = L(
            "Couldn't update your vote. Try again.",
            "تعذر تحديث تصويتك. حاول مجددًا.",
          );
          renderTips();
        });
    }

    function feedHtml() {
      var items = feed();
      if (tipsState.loading)
        return (
          '<p class="crt-note">' + esc(L("Loading…", "جارٍ التحميل…")) + "</p>"
        );
      if (tipsState.failed && !items.length)
        return (
          '<p class="crt-note">' +
          esc(
            L(
              "Posts are unavailable right now.",
              "المشاركات غير متاحة حاليًا.",
            ),
          ) +
          "</p>"
        );
      if (!items.length)
        return (
          '<p class="crt-note">' +
          esc(
            L(
              "No posts yet. Be the first to help the next student.",
              "لا توجد مشاركات بعد. كن أول من يساعد الطلاب.",
            ),
          ) +
          "</p>"
        );
      return (
        '<div class="crt-feed">' +
        items
          .map(function (item) {
            var type = postType(item.type);
            var date =
              item.createdAt && typeof item.createdAt.toDate === "function"
                ? item.createdAt.toDate()
                : null;
            var mine = tipsState.user && item.uid === tipsState.user.uid;
            var voted = Boolean(
              tipsState.user &&
              item.helpfulBy &&
              item.helpfulBy[tipsState.user.uid],
            );
            var key = item.kind + ":" + item.id;
            return (
              '<article class="crt-card"><div class="crt-card-head"><span class="crt-tag">' +
              esc(L(type.en, type.ar)) +
              "</span>" +
              (date
                ? '<span class="crt-date">' +
                  esc(
                    date.toLocaleDateString(isArabic() ? "ar" : "en", {
                      year: "numeric",
                      month: "short",
                      day: "numeric",
                    }),
                  ) +
                  "</span>"
                : "") +
              "</div><h3>" +
              esc(item.title) +
              "</h3><p>" +
              esc(item.body) +
              "</p>" +
              (item.url
                ? '<a class="crt-link" href="' +
                  esc(item.url) +
                  '" target="_blank" rel="noopener noreferrer">' +
                  esc(L("Open link", "فتح الرابط")) +
                  " ↗</a>"
                : "") +
              '<div class="crt-card-foot"><button class="crt-vote" type="button" data-feed-vote="' +
              esc(key) +
              '" aria-pressed="' +
              voted +
              '">' +
              esc(L("Helpful", "مفيد")) +
              " · " +
              (Number(item.helpfulCount) || 0) +
              "</button>" +
              (mine
                ? '<button class="crt-text-btn" type="button" data-feed-delete="' +
                  esc(key) +
                  '">' +
                  esc(L("Delete", "حذف")) +
                  "</button>"
                : "") +
              "</div></article>"
            );
          })
          .join("") +
        "</div>"
      );
    }

    function postFormHtml() {
      if (tipsState.user === undefined)
        return (
          '<p class="crt-note">' + esc(L("Loading…", "جارٍ التحميل…")) + "</p>"
        );
      if (!tipsState.user)
        return (
          '<p class="crt-note">' +
          esc(
            L(
              "Took this course? Sign in to share a tip, an exam or assignment report, or a useful resource.",
              "درست هذا المقرر؟ سجّل الدخول لمشاركة نصيحة أو تقرير عن اختبار أو واجب أو مصدر مفيد.",
            ),
          ) +
          '</p><button class="crt-btn" type="button" data-tip-signin>' +
          esc(L("Sign in to post", "سجّل الدخول للمشاركة")) +
          "</button>"
        );
      var type = postType(tipsState.type);
      var isAr = isArabic() ? 1 : 0;
      return (
        '<form class="crt-post-form" novalidate>' +
        '<div class="crt-field"><span class="crt-field-label">' +
        esc(L("What are you sharing?", "ماذا تشارك؟")) +
        '</span><div class="crt-choices">' +
        POST_TYPES.map(function (t) {
          return (
            '<button type="button" class="crt-choice" data-post-type="' +
            t.id +
            '" aria-pressed="' +
            (t.id === type.id) +
            '">' +
            esc(L(t.en, t.ar)) +
            "</button>"
          );
        }).join("") +
        "</div></div>" +
        '<label class="crt-field"><span class="crt-field-label">' +
        esc(L("Title", "العنوان")) +
        '</span><input class="crt-input" name="title" maxlength="120" placeholder="' +
        esc(type.title[isAr]) +
        '"></label>' +
        '<label class="crt-field"><span class="crt-field-label">' +
        esc(L("Details", "التفاصيل")) +
        '</span><textarea class="crt-input" name="body" maxlength="1200" placeholder="' +
        esc(type.body[isAr]) +
        '"></textarea>' +
        '<span class="crt-hint">' +
        esc(L("At least 20 characters.", "20 حرفًا على الأقل.")) +
        "</span></label>" +
        (type.link
          ? '<label class="crt-field"><span class="crt-field-label">' +
            esc(L("Link", "الرابط")) +
            " <span>" +
            esc(L("(optional)", "(اختياري)")) +
            '</span></span><input class="crt-input" name="url" type="url" maxlength="500" placeholder="https://"></label>'
          : "") +
        '<div class="crt-actions" style="margin-top:4px"><button class="crt-btn" type="submit"' +
        (tipsState.saving ? " disabled" : "") +
        ">" +
        esc(L("Post", "نشر")) +
        '</button><span class="crt-status" role="status">' +
        esc(tipsState.message) +
        "</span></div></form>"
      );
    }

    function tipsHtml() {
      var tools = requiredTools.length
        ? '<div class="crt-group" style="margin-top:0">' +
          esc(L("Software you'll need", "برامج ستحتاجها")) +
          '</div><div class="crt-tools">' +
          requiredTools
            .map(function (tool) {
              return (
                '<div><a href="' +
                esc(tool.url) +
                '" target="_blank" rel="noopener noreferrer">' +
                esc(tool.name) +
                " ↗</a><span>" +
                esc(tool.note) +
                "</span></div>"
              );
            })
            .join("") +
          "</div>"
        : "";
      return (
        '<div class="crt-col">' +
        tools +
        '<div class="crt-group"' +
        (tools ? "" : ' style="margin-top:0"') +
        ">" +
        esc(L("From students", "من الطلاب")) +
        "</div>" +
        feedHtml() +
        '</div><div class="crt-col"><div class="crt-group" style="margin-top:0">' +
        esc(L("Share with students", "شارك مع الطلاب")) +
        "</div>" +
        postFormHtml() +
        "</div>"
      );
    }

    function renderTips() {
      if (!tipsHost) return;
      var oldFields = {},
        active = document.activeElement,
        focusName = active && tipsHost.contains(active) && active.name;
      tipsHost
        .querySelectorAll(".crt-post-form [name]")
        .forEach(function (field) {
          oldFields[field.name] = field.value;
        });
      tipsHost.innerHTML = tipsHtml();
      if (!tipsState.clearDraft) {
        tipsHost
          .querySelectorAll(".crt-post-form [name]")
          .forEach(function (field) {
            if (Object.prototype.hasOwnProperty.call(oldFields, field.name))
              field.value = oldFields[field.name];
            if (focusName && field.name === focusName) field.focus();
          });
      }
      tipsState.clearDraft = false;
    }

    function feedItem(key) {
      var parts = key.split(":"),
        items = feed();
      for (var i = 0; i < items.length; i++)
        if (items[i].kind === parts[0] && items[i].id === parts[1])
          return items[i];
      return null;
    }

    tipsHost.addEventListener("click", function (e) {
      var button = e.target.closest("button");
      if (!button) return;
      if (button.hasAttribute("data-tip-signin")) {
        openSignIn();
      } else if (button.hasAttribute("data-post-type")) {
        tipsState.type = button.getAttribute("data-post-type");
        tipsState.message = "";
        renderTips();
        var picked = tipsHost.querySelector(
          '[data-post-type="' + tipsState.type + '"]',
        );
        if (picked) picked.focus();
      } else if (button.hasAttribute("data-feed-vote")) {
        var voteItem = feedItem(button.getAttribute("data-feed-vote"));
        if (voteItem) helpful(voteItem);
      } else if (
        button.hasAttribute("data-feed-delete") &&
        tipsState.user &&
        tipsState.fb
      ) {
        var item = feedItem(button.getAttribute("data-feed-delete"));
        if (item && window.confirm(L("Delete this post?", "حذف هذه المشاركة؟")))
          feedRef(item)
            .delete()
            .catch(function () {
              tipsState.message = L(
                "Couldn't delete that post.",
                "تعذر حذف المشاركة.",
              );
              renderTips();
            });
      }
    });

    tipsHost.addEventListener("submit", function (e) {
      if (!e.target.matches(".crt-post-form")) return;
      e.preventDefault();
      if (!tipsState.user || !tipsState.fb || tipsState.saving) return;
      var data = new FormData(e.target),
        type = postType(tipsState.type),
        title = String(data.get("title") || "").trim(),
        body = String(data.get("body") || "").trim(),
        url = String(data.get("url") || "").trim();
      var problem =
        title.length < 3
          ? L(
              "Add a short title (3+ characters).",
              "أضف عنوانًا قصيرًا (3 أحرف على الأقل).",
            )
          : body.length < 20
            ? L(
                "Add a bit more detail (20+ characters).",
                "أضف تفاصيل أكثر (20 حرفًا على الأقل).",
              )
            : url && !/^https?:\/\/\S+$/i.test(url)
              ? L(
                  "The link should start with https://",
                  "يجب أن يبدأ الرابط بـ https://",
                )
              : "";
      if (problem) {
        tipsState.message = problem;
        renderTips();
        return;
      }
      var db = tipsState.fb.firestore(),
        now = tipsState.fb.firestore.FieldValue.serverTimestamp();
      var write =
        type.id === "tip"
          ? db
              .collection("courseRatings")
              .doc(course)
              .collection("tips")
              .add({
                uid: tipsState.user.uid,
                focus: title.slice(0, 140),
                tip: body,
                helpfulCount: 0,
                helpfulBy: {},
                createdAt: now,
              })
          : db
              .collection("courseCommunity")
              .doc(course)
              .collection("posts")
              .add({
                uid: tipsState.user.uid,
                type: type.id,
                title: title,
                body: body,
                url: type.link ? url : "",
                hours: null,
                difficulty: null,
                helpfulCount: 0,
                helpfulBy: {},
                createdAt: now,
              });
      tipsState.saving = true;
      tipsState.message = "";
      renderTips();
      write
        .then(function () {
          tipsState.saving = false;
          tipsState.clearDraft = true;
          tipsState.message = L(
            "Posted. Thanks for helping other students!",
            "تم النشر. شكرًا لمساعدة الطلاب!",
          );
          renderTips();
        })
        .catch(function () {
          tipsState.saving = false;
          tipsState.message = L(
            "Couldn't post. Check your connection and try again.",
            "تعذر النشر. تحقق من اتصالك وحاول مجددًا.",
          );
          renderTips();
        });
    });
    renderTips();
    new MutationObserver(renderTips).observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["lang"],
    });

    function draftFrom(doc) {
      var d = { term: termCode(doc && doc.term) };
      d.termOther = !!d.term && ratingTerms().indexOf(d.term) < 0;
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
      var terms = Object.keys(sum.termCounts || {})
        .sort()
        .reverse();
      if (terms.length) {
        html +=
          '<div class="crt-group">' +
          esc(L("Ratings by semester", "التقييمات حسب الفصل")) +
          "</div>" +
          terms
            .map(function (term) {
              return (
                '<div class="crt-row"><span class="crt-label">' +
                esc(term) +
                '</span><span class="crt-val">' +
                esc(countLabel(sum.termCounts[term])) +
                "</span></div>"
              );
            })
            .join("");
      }
      return html;
    }

    function termHtml() {
      var term = state.draft.term || "",
        other = !!state.draft.termOther;
      return (
        '<div class="crt-field"><span class="crt-field-label">' +
        esc(L("Semester taken", "الفصل الدراسي")) +
        " <span>" +
        esc(L("(optional)", "(اختياري)")) +
        '</span></span><div class="crt-choices">' +
        ratingTerms()
          .map(function (t) {
            return (
              '<button type="button" class="crt-choice" data-crt-term="' +
              t +
              '" aria-pressed="' +
              (!other && term === t) +
              '">' +
              t +
              "</button>"
            );
          })
          .join("") +
        '<button type="button" class="crt-choice" data-crt-term="other" aria-pressed="' +
        other +
        '">' +
        esc(L("Other", "أخرى")) +
        "</button></div>" +
        (other
          ? '<input class="crt-input crt-short" data-crt-term-input inputmode="numeric" maxlength="3" placeholder="' +
            esc(L("e.g. 262", "مثال: 262")) +
            '" aria-label="' +
            esc(L("Semester code", "رمز الفصل")) +
            '" value="' +
            esc(term) +
            '">'
          : "") +
        "</div>"
      );
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
        "</p>" +
        termHtml();
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
      if (
        state.draft.termOther &&
        state.draft.term &&
        !/^\d{3}$/.test(state.draft.term)
      ) {
        state.status = [
          "Type the semester as 3 digits, e.g. 262.",
          "اكتب الفصل بثلاثة أرقام، مثال: 262.",
        ];
        return render();
      }
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
    panel.addEventListener("click", function (e) {
      var t = e.target.closest("[data-crt-term]");
      if (!t) return;
      var value = t.getAttribute("data-crt-term");
      if (value === "other") {
        state.draft.termOther = !state.draft.termOther;
        state.draft.term = "";
        state.focus = state.draft.termOther
          ? "[data-crt-term-input]"
          : '[data-crt-term="other"]';
      } else {
        state.draft.termOther = false;
        state.draft.term = state.draft.term === value ? "" : value;
        state.focus = '[data-crt-term="' + value + '"]';
      }
      state.status = null;
      render();
    });
    panel.addEventListener("input", function (e) {
      if (!e.target.matches("[data-crt-term-input]")) return;
      e.target.value = e.target.value.replace(/\D/g, "").slice(0, 3);
      state.draft.term = e.target.value;
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
      fb.firestore()
        .collection("courseRatings")
        .doc(course)
        .collection("tips")
        .limit(100)
        .onSnapshot(
          function (snap) {
            tipsState.items = snap.docs
              .map(function (d) {
                return Object.assign({ id: d.id }, d.data());
              })
              .sort(function (a, b) {
                var ta =
                  a.createdAt && typeof a.createdAt.toMillis === "function"
                    ? a.createdAt.toMillis()
                    : 0;
                var tb =
                  b.createdAt && typeof b.createdAt.toMillis === "function"
                    ? b.createdAt.toMillis()
                    : 0;
                return tb - ta;
              });
            tipsState.loading = false;
            tipsState.failed = false;
            renderTips();
          },
          function () {
            tipsState.loading = false;
            tipsState.failed = true;
            renderTips();
          },
        );
      fb.firestore()
        .collection("courseCommunity")
        .doc(course)
        .collection("posts")
        .limit(100)
        .onSnapshot(
          function (snap) {
            tipsState.posts = snap.docs
              .map(function (d) {
                return Object.assign({ id: d.id }, d.data());
              })
              .sort(function (a, b) {
                var ta =
                  a.createdAt && typeof a.createdAt.toMillis === "function"
                    ? a.createdAt.toMillis()
                    : 0;
                var tb =
                  b.createdAt && typeof b.createdAt.toMillis === "function"
                    ? b.createdAt.toMillis()
                    : 0;
                return tb - ta;
              });
            renderTips();
          },
          function () {
            tipsState.message = L(
              "Student contributions are unavailable right now.",
              "مساهمات الطلاب غير متاحة حاليًا.",
            );
            renderTips();
          },
        );
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
    compare.innerHTML =
      "<strong>" +
      esc(L("Compare courses", "قارن المقررات")) +
      '</strong><p class="crt-section-note">' +
      esc(
        L(
          "Choose up to four courses using the Compare buttons.",
          "اختر حتى أربعة مقررات باستخدام أزرار المقارنة.",
        ),
      ) +
      "</p>";
    var list = cards[0].closest(".course-list");
    if (list) list.insertAdjacentElement("afterend", compare);
    function renderCompare() {
      if (selected.length < 2) {
        compare.innerHTML =
          "<strong>" +
          esc(L("Compare courses", "قارن المقررات")) +
          '</strong><p class="crt-section-note">' +
          esc(
            L(
              selected.length
                ? "Choose one more course to compare."
                : "Choose up to four courses using the Compare buttons.",
              selected.length
                ? "اختر مقررًا آخر للمقارنة."
                : "اختر حتى أربعة مقررات باستخدام أزرار المقارنة.",
            ),
          ) +
          "</p>";
        return;
      }
      var rows = metricRows.map(function (row) {
        return (
          "<tr><th>" +
          esc(L(row[1], row[1])) +
          "</th>" +
          selected
            .map(function (code) {
              var score = summaries[code] && summaries[code][row[0]];
              return (
                "<td>" +
                (score ? fixed(score.avg) + "/5 · " + score.count : "—") +
                "</td>"
              );
            })
            .join("") +
          "</tr>"
        );
      });
      rows.push(
        "<tr><th>" +
          esc(L("Exam difficulty (average)", "متوسط صعوبة الاختبارات")) +
          "</th>" +
          selected
            .map(function (code) {
              var s = summaries[code] || {},
                values = Object.keys(s)
                  .filter(function (key) {
                    return key.indexOf("exams.") === 0;
                  })
                  .map(function (key) {
                    return s[key];
                  });
              var total = values.reduce(function (sum, value) {
                  return sum + value.avg * value.count;
                }, 0),
                count = values.reduce(function (sum, value) {
                  return sum + value.count;
                }, 0);
              return (
                "<td>" +
                (count ? fixed(total / count) + "/5 · " + count : "—") +
                "</td>"
              );
            })
            .join("") +
          "</tr>",
      );
      compare.innerHTML =
        "<strong>" +
        esc(L("Course comparison", "مقارنة المقررات")) +
        "</strong><table><thead><tr><th></th>" +
        selected
          .map(function (code) {
            return "<th>" + esc(code.toUpperCase()) + "</th>";
          })
          .join("") +
        "</tr></thead><tbody>" +
        rows.join("") +
        "</tbody></table>";
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
            pick.setAttribute(
              "aria-pressed",
              String(selected.indexOf(course) > -1),
            );
            pick.textContent =
              selected.indexOf(course) > -1
                ? L("Selected", "محدد")
                : L("Compare", "قارن");
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
