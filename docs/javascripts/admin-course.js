/**
 * Paid course instructor panel (/admin/course/) for the Ethics course.
 *
 * Reads, as the administrator:
 *   courseTransfers         sales (through the REST API with a field mask, so
 *                           the receipt images are never downloaded)
 *   courseProgress/ethics/students/*   per-student progress (course-tracking.js)
 *   pageComments/{slug}/comments       comments on paid pages
 *   questionReports         reported questions for ethcs303
 *   courseEvents, courseSlots, courseBookings, courseConfig/ethics
 * Firestore rules refuse all of this to anyone but the admin account. Text that
 * students wrote is always inserted with textContent.
 */
(function () {
  "use strict";
  var COURSE = "ethics";
  var COURSE_CODE = "ethcs303";
  var PROJECT = "shoug-tech";
  var SVG = "http://www.w3.org/2000/svg";
  var SECTION_NAMES = {
    "video-explanations": "Video explanations",
    "slide-breakdowns": "Slide breakdowns",
    slides: "Slides",
    exams: "Quizzes & exams",
    "extra-resources": "Extra resources",
    home: "Course home",
  };
  var TYPE_NAMES = { live: "Live session", office: "Office hours", academic: "Academic date" };

  var fb, db, user;
  var S = {
    term: null,
    terms: [],
    sales: null,
    roster: {},
    progress: [],
    tab: "lessons",
  };
  var $ = function (id) { return document.getElementById(id); };

  // ------------------------------------------------------------- helpers --
  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    for (var k in attrs || {}) {
      var v = attrs[k];
      if (v === undefined || v === null) continue;
      if (k === "text") node.textContent = v;
      else if (k === "class") node.className = v;
      else if (k.slice(0, 2) === "on") node.addEventListener(k.slice(2), v);
      else node.setAttribute(k, v);
    }
    (children || []).forEach(function (c) {
      if (c !== null && c !== undefined && c !== false)
        node.appendChild(typeof c === "string" || typeof c === "number" ? document.createTextNode(String(c)) : c);
    });
    return node;
  }
  function svg(tag, attrs) {
    var n = document.createElementNS(SVG, tag);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    return n;
  }
  var nf = new Intl.NumberFormat("en");
  function fmt(n) { return nf.format(Math.round(Number(n) || 0)); }
  function sar(halalas) {
    return new Intl.NumberFormat("en", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format((Number(halalas) || 0) / 100) + " SAR";
  }
  function pct(a, b) { return b ? Math.round((a / b) * 100) + "%" : "–"; }
  function duration(sec) {
    sec = Math.round(sec || 0);
    if (sec < 60) return sec + "s";
    var m = Math.floor(sec / 60);
    return m < 60 ? m + "m" : Math.floor(m / 60) + "h " + (m % 60) + "m";
  }
  function toDate(v) {
    if (!v) return null;
    if (v.toDate) return v.toDate();
    if (v instanceof Date) return v;
    var d = new Date(v);
    return isNaN(d) ? null : d;
  }
  function dateText(v, withTime) {
    var d = toDate(v);
    if (!d) return "–";
    return d.toLocaleString("en-GB", withTime
      ? { day: "numeric", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit", timeZone: "Asia/Riyadh" }
      : { day: "numeric", month: "short", year: "numeric", timeZone: "Asia/Riyadh" });
  }
  function dayKey(d) {
    return new Date(d.getTime() + 3 * 3600000).toISOString().slice(0, 10).replace(/-/g, "");
  }
  function status(text, isError) {
    var s = $("ac-status");
    s.textContent = text || "";
    s.hidden = !text;
    s.classList.toggle("is-error", !!isError);
  }
  function emptyNote(text) { return el("p", { class: "aa-empty", text: text }); }

  // ---------------------------------------------------------------- terms --
  // A term runs from its start date to the next term's start (or today).
  function termRange() {
    if (!S.term) return { from: null, to: null };
    var i = S.terms.findIndex(function (t) { return t.start === S.term; });
    var next = S.terms[i + 1];
    return {
      from: new Date(S.term + "T00:00:00+03:00"),
      to: next ? new Date(next.start + "T00:00:00+03:00") : null,
    };
  }
  function inTerm(d) {
    d = toDate(d);
    if (!d) return false;
    var r = termRange();
    return (!r.from || d >= r.from) && (!r.to || d < r.to);
  }
  function dayInTerm(key) {
    var r = termRange();
    return (!r.from || key >= dayKey(r.from)) && (!r.to || key < dayKey(r.to));
  }
  function renderTermPicker() {
    var sel = $("ac-term");
    sel.textContent = "";
    sel.appendChild(el("option", { value: "", text: "All time" }));
    S.terms.forEach(function (t) {
      sel.appendChild(el("option", { value: t.start, text: t.label + " (from " + dateText(t.start + "T12:00:00+03:00") + ")" }));
    });
    sel.value = S.term || "";
  }

  // ---------------------------------------------------------------- data --
  // courseTransfers through REST: rules allow 10 per query, and the field mask
  // leaves out the receipt image.
  function loadSales() {
    var fields = ["uid", "email", "fullName", "phone", "amount", "currency", "status", "submittedAt", "reviewedAt"];
    var url = "https://firestore.googleapis.com/v1/projects/" + PROJECT + "/databases/(default)/documents:runQuery";
    var out = [];
    function page(token, cursor) {
      var q = {
        structuredQuery: {
          from: [{ collectionId: "courseTransfers" }],
          select: { fields: fields.map(function (f) { return { fieldPath: f }; }) },
          orderBy: [{ field: { fieldPath: "submittedAt" }, direction: "DESCENDING" }, { field: { fieldPath: "__name__" }, direction: "DESCENDING" }],
          limit: 10,
        },
      };
      if (cursor) q.structuredQuery.startAt = { values: cursor, before: false };
      return fetch(url, { method: "POST", headers: { "content-type": "application/json", authorization: "Bearer " + token }, body: JSON.stringify(q) })
        .then(function (r) {
          return r.json().then(function (body) {
            if (!r.ok) throw new Error((body[0] && body[0].error && body[0].error.message) || (body.error && body.error.message) || "HTTP " + r.status);
            return body;
          });
        })
        .then(function (rows) {
          var docs = rows.filter(function (x) { return x.document; }).map(function (x) { return x.document; });
          docs.forEach(function (d) { out.push(parseDoc(d)); });
          if (docs.length < 10 || out.length > 5000) return out;
          var last = docs[docs.length - 1];
          return page(token, [last.fields.submittedAt || { nullValue: null }, { referenceValue: last.name }]);
        });
    }
    return user.getIdToken().then(function (token) { return page(token, null); });
  }
  function value(v) {
    if (!v) return null;
    if ("stringValue" in v) return v.stringValue;
    if ("integerValue" in v) return Number(v.integerValue);
    if ("doubleValue" in v) return v.doubleValue;
    if ("timestampValue" in v) return new Date(v.timestampValue);
    if ("booleanValue" in v) return v.booleanValue;
    return null;
  }
  function parseDoc(d) {
    var o = { id: d.name.split("/").pop() };
    for (var k in d.fields || {}) o[k] = value(d.fields[k]);
    return o;
  }

  function loadProgress() {
    return db.collection("courseProgress").doc(COURSE).collection("students").get().then(function (snap) {
      return snap.docs.map(function (d) { return Object.assign({ uid: d.id }, d.data()); });
    });
  }
  function loadConfig() {
    return db.collection("courseConfig").doc(COURSE).get().then(function (d) {
      var terms = (d.exists && Array.isArray(d.data().terms) ? d.data().terms : []).filter(function (t) {
        return t && /^\d{4}-\d{2}-\d{2}$/.test(t.start);
      });
      terms.sort(function (a, b) { return a.start < b.start ? -1 : 1; });
      return terms;
    });
  }

  // --------------------------------------------------------- aggregation --
  function studentStats(p) {
    var views = 0, viewsWeek = 0, watch = 0, lessonsSeen = 0, lastDay = "";
    var weekAgo = dayKey(new Date(Date.now() - 7 * 86400000));
    Object.keys(p.lessons || {}).forEach(function (k) {
      var l = p.lessons[k];
      var seen = false;
      Object.keys(l.days || {}).forEach(function (day) {
        if (day > lastDay) lastDay = day;
        if (!dayInTerm(day)) return;
        views += Number(l.days[day]) || 0;
        seen = true;
        if (day >= weekAgo) viewsWeek += Number(l.days[day]) || 0;
      });
      if (seen) {
        lessonsSeen++;
        watch += Number(l.watchSeconds) || 0;
      }
    });
    var quizzes = 0, quizzesWeek = 0, scoreSum = 0, scored = 0;
    var weekStart = new Date(Date.now() - 7 * 86400000);
    Object.keys(p.quizzes || {}).forEach(function (k) {
      var q = p.quizzes[k];
      if (!inTerm(q.lastAt)) return;
      quizzes++;
      if (toDate(q.lastAt) >= weekStart) quizzesWeek++;
      if (q.answered) {
        scoreSum += (Number(q.correct) || 0) / Number(q.answered);
        scored++;
      }
    });
    var last = toDate(p.lastSeenAt);
    var idleDays = last ? Math.floor((Date.now() - last.getTime()) / 86400000) : null;
    var avg = scored ? scoreSum / scored : null;
    var follow = [];
    if (idleDays === null || idleDays >= 7) follow.push(idleDays === null ? "never opened the course" : "inactive " + idleDays + " days");
    if (avg !== null && avg < 0.6) follow.push("quiz average " + Math.round(avg * 100) + "%");
    return { views: views, viewsWeek: viewsWeek, watch: watch, lessonsSeen: lessonsSeen, quizzes: quizzes, quizzesWeek: quizzesWeek, avg: avg, last: last, follow: follow };
  }

  function lessonRows() {
    var map = {};
    S.progress.forEach(function (p) {
      Object.keys(p.lessons || {}).forEach(function (k) {
        var l = p.lessons[k];
        var row = map[k] || (map[k] = { key: k, title: l.title || k, section: l.section || "home", path: l.path || "", kind: l.kind, views: 0, students: 0, up: 0, down: 0, watch: 0, pctSum: 0, pctN: 0 });
        if (l.title) row.title = l.title;
        var v = 0;
        Object.keys(l.days || {}).forEach(function (day) {
          if (dayInTerm(day)) v += Number(l.days[day]) || 0;
        });
        if (!v && S.term) return;
        row.views += v;
        row.students++;
        if (Number(l.reaction) === 1) row.up++;
        if (Number(l.reaction) === -1) row.down++;
        row.watch += Number(l.watchSeconds) || 0;
        if (l.maxPct) { row.pctSum += Number(l.maxPct); row.pctN++; }
      });
    });
    return Object.keys(map).map(function (k) { return map[k]; });
  }

  // ------------------------------------------------------------- tiles --
  function tile(label, valueText, note, tone) {
    return el("div", { class: "aa-tile" + (tone ? " ac-" + tone : "") }, [
      el("span", { class: "aa-tile-label", text: label }),
      el("strong", { class: "aa-tile-value", text: valueText }),
      el("span", { class: "aa-delta", text: note || "" }),
    ]);
  }

  // --------------------------------------------------------- tab: lessons --
  function renderLessons(root) {
    var rows = lessonRows().filter(function (r) { return r.kind !== "page" || r.views; });
    var totalViews = 0, up = 0, down = 0;
    rows.forEach(function (r) { totalViews += r.views; up += r.up; down += r.down; });
    root.appendChild(el("div", { class: "aa-tiles" }, [
      tile("Views", fmt(totalViews), S.term ? "this term" : "all time"),
      tile("Like rate", up + down ? pct(up, up + down) : "–", "of students who rated"),
      tile("Likes", fmt(up)),
      tile("Dislikes", fmt(down), null, down ? "warn" : null),
    ]));
    if (!rows.length) return root.appendChild(emptyNote("No lesson views recorded yet. They appear once paid students open lessons."));
    var groups = {};
    rows.forEach(function (r) { (groups[r.section] = groups[r.section] || []).push(r); });
    Object.keys(groups).sort(function (a, b) {
      var order = ["video-explanations", "slide-breakdowns", "slides", "exams", "extra-resources", "home"];
      return (order.indexOf(a) + 100 * (order.indexOf(a) < 0)) - (order.indexOf(b) + 100 * (order.indexOf(b) < 0));
    }).forEach(function (sec) {
      var list = groups[sec].sort(function (a, b) { return a.title.localeCompare(b.title, "en", { numeric: true }); });
      var sv = 0, su = 0, sd = 0;
      list.forEach(function (r) { sv += r.views; su += r.up; sd += r.down; });
      var table = el("table", { class: "aa-plain ac-lessons" }, [
        el("thead", null, [el("tr", null, [
          el("th", { scope: "col", text: "Lesson" }),
          el("th", { scope: "col", class: "num", text: "Views" }),
          el("th", { scope: "col", class: "num", text: "Students" }),
          el("th", { scope: "col", class: "num", text: "Watched" }),
          el("th", { scope: "col", class: "num", text: "Like rate" }),
          el("th", { scope: "col", class: "num", text: "👍" }),
          el("th", { scope: "col", class: "num", text: "👎" }),
        ])]),
        el("tbody", null, list.map(function (r) {
          return el("tr", null, [
            el("td", null, [r.path ? el("a", { href: r.path, target: "_blank", rel: "noopener", text: r.title }) : r.title]),
            el("td", { class: "num strong", text: fmt(r.views) }),
            el("td", { class: "num", text: fmt(r.students) }),
            el("td", { class: "num", text: r.pctN ? Math.round(r.pctSum / r.pctN) + "% avg" : "–" }),
            el("td", { class: "num", text: r.up + r.down ? pct(r.up, r.up + r.down) : "–" }),
            el("td", { class: "num ac-up", text: fmt(r.up) }),
            el("td", { class: "num ac-down", text: fmt(r.down) }),
          ]);
        })),
      ]);
      root.appendChild(el("details", { class: "aa-card ac-group", open: "" }, [
        el("summary", null, [
          el("strong", { text: SECTION_NAMES[sec] || sec }),
          el("span", { class: "ac-sum", text: list.length + " lessons · " + fmt(sv) + " views · " + (su + sd ? pct(su, su + sd) + " liked" : "no ratings") }),
        ]),
        el("div", { class: "aa-table-wrap" }, [table]),
      ]));
    });
  }

  // -------------------------------------------------------- tab: earnings --
  function renderEarnings(root) {
    var sales = (S.sales || []).filter(function (s) { return s.course !== "x"; });
    var approved = sales.filter(function (s) { return s.status === "approved" && inTerm(s.reviewedAt || s.submittedAt); });
    var pending = sales.filter(function (s) { return s.status === "pending"; });
    var total = approved.reduce(function (a, s) { return a + (Number(s.amount) || 0); }, 0);
    root.appendChild(el("div", { class: "ac-hero" }, [
      el("span", { text: "Total earnings " + (S.term ? "this term" : "all time") }),
      el("strong", { text: sar(total) }),
      el("small", { text: approved.length + " approved sales · " + pending.length + " waiting for review" }),
    ]));

    // Weekly bars (weeks start Sunday, Riyadh time).
    var weeks = {};
    approved.forEach(function (s) {
      var d = toDate(s.reviewedAt || s.submittedAt);
      var r = new Date(d.getTime() + 3 * 3600000);
      r.setUTCDate(r.getUTCDate() - r.getUTCDay());
      var k = r.toISOString().slice(0, 10);
      weeks[k] = (weeks[k] || 0) + (Number(s.amount) || 0);
    });
    var keys = Object.keys(weeks).sort();
    var chartCard = el("section", { class: "aa-card" }, [el("header", { class: "aa-card-head" }, [el("h3", { text: "Earnings by week" }), el("p", { text: "Approved sales, each bar one week (Sunday to Saturday)" })])]);
    if (keys.length) {
      // Fill empty weeks between the first and last so gaps read as zero.
      var filled = [];
      for (var d = new Date(keys[0] + "T00:00:00Z"); d <= new Date(keys[keys.length - 1] + "T00:00:00Z"); d.setUTCDate(d.getUTCDate() + 7)) {
        var k = d.toISOString().slice(0, 10);
        filled.push({ week: k, amount: weeks[k] || 0 });
      }
      root.appendChild(chartCard);
      chartCard.appendChild(barChart(filled, chartCard.clientWidth - 36));
    } else {
      chartCard.appendChild(emptyNote("No approved sales in this range."));
      root.appendChild(chartCard);
    }

    // Sales log
    var search = el("input", { type: "search", class: "ac-input", placeholder: "Search by name or email", "aria-label": "Search sales" });
    var filter = el("select", { class: "ac-input", "aria-label": "Status" }, [
      el("option", { value: "", text: "All statuses" }),
      el("option", { value: "approved", text: "Approved" }),
      el("option", { value: "pending", text: "Pending" }),
      el("option", { value: "rejected", text: "Rejected" }),
    ]);
    var body = el("tbody");
    var shown = [];
    function paint() {
      var q = search.value.trim().toLowerCase();
      shown = sales.filter(function (s) {
        if (filter.value && s.status !== filter.value) return false;
        if (S.term && !inTerm(s.reviewedAt || s.submittedAt)) return false;
        return !q || (String(s.fullName || "") + " " + String(s.email || "")).toLowerCase().indexOf(q) >= 0;
      });
      body.textContent = "";
      if (!shown.length) body.appendChild(el("tr", null, [el("td", { colspan: "6", class: "aa-empty", text: "No sales match." })]));
      shown.forEach(function (s) {
        body.appendChild(el("tr", null, [
          el("td", null, [el("strong", { text: s.fullName || "–" }), el("small", { class: "ac-sub", text: s.email || "" })]),
          el("td", { text: "ETHCS303" }),
          el("td", { class: "num strong", text: sar(s.amount) }),
          el("td", null, [el("span", { class: "ac-pill ac-" + s.status, text: s.status === "approved" ? "✓ Approved" : s.status === "pending" ? "● Pending" : "✕ Rejected" })]),
          el("td", { text: dateText(s.submittedAt) }),
          el("td", { text: dateText(s.reviewedAt) }),
        ]));
      });
    }
    search.addEventListener("input", paint);
    filter.addEventListener("change", paint);
    var exportBtn = el("button", { type: "button", class: "ac-btn", text: "Export CSV", onclick: function () { exportCsv(shown); } });
    root.appendChild(el("section", { class: "aa-card" }, [
      el("header", { class: "aa-card-head ac-head-row" }, [el("h3", { text: "Sales log" }), exportBtn]),
      el("div", { class: "ac-filters" }, [search, filter, el("a", { href: "/admin/transfers/", class: "ac-link", text: "Review pending payments →" })]),
      el("div", { class: "aa-table-wrap" }, [el("table", { class: "aa-plain" }, [
        el("thead", null, [el("tr", null, ["Student", "Course", "Paid", "Status", "Submitted", "Approved"].map(function (h, i) {
          return el("th", { scope: "col", class: i === 2 ? "num" : "", text: h });
        }))]),
        body,
      ])]),
    ]));
    paint();
  }

  function barChart(data, width) {
    // Drawn at the card's real width so text stays at its intended size.
    var W = Math.max(320, Math.round(width || 760)), H = 240, L = 54, R = 12, T = 22, B = 28;
    var max = Math.max.apply(null, data.map(function (d) { return d.amount; })) || 1;
    var step = Math.pow(10, Math.floor(Math.log10(max)));
    var top = Math.ceil(max / step) * step;
    var chart = svg("svg", { viewBox: "0 0 " + W + " " + H, class: "aa-line", role: "img", "aria-label": "Earnings by week" });
    for (var g = 0; g <= 4; g++) {
      var v = (top / 4) * g, y = T + (1 - v / top) * (H - T - B);
      chart.appendChild(svg("line", { x1: L, x2: W - R, y1: y, y2: y, class: g ? "aa-gridline" : "aa-axis" }));
      var t = svg("text", { x: L - 8, y: y + 4, class: "aa-tick", "text-anchor": "end" });
      t.textContent = fmt(v / 100);
      chart.appendChild(t);
    }
    var slot = (W - L - R) / data.length;
    var bw = Math.max(4, Math.min(36, slot - 6));
    var tip = el("div", { class: "aa-tip", hidden: "" });
    var every = Math.max(1, Math.ceil(data.length / 8));
    data.forEach(function (d, i) {
      var x = L + slot * i + (slot - bw) / 2;
      var h = (d.amount / top) * (H - T - B);
      var y = H - B - h;
      var r = Math.min(4, bw / 2, h);
      var path = h > 0
        ? "M" + x + "," + (H - B) + "V" + (y + r) + "Q" + x + "," + y + " " + (x + r) + "," + y + "H" + (x + bw - r) + "Q" + (x + bw) + "," + y + " " + (x + bw) + "," + (y + r) + "V" + (H - B) + "Z"
        : "";
      if (path) chart.appendChild(svg("path", { d: path, class: "ac-bar" }));
      var hit = svg("rect", { x: L + slot * i, y: T, width: slot, height: H - T - B, fill: "transparent", tabindex: "0", "aria-label": "Week of " + d.week + ": " + sar(d.amount) });
      function show() {
        tip.textContent = "";
        tip.appendChild(el("div", { class: "aa-tip-title", text: "Week of " + dateText(d.week + "T12:00:00Z") }));
        tip.appendChild(el("strong", { text: sar(d.amount) }));
        tip.hidden = false;
        var box = chart.getBoundingClientRect();
        tip.style.left = Math.min(box.width - 170, Math.max(0, ((x + bw) / W) * box.width + 8)) + "px";
      }
      hit.addEventListener("pointerenter", show);
      hit.addEventListener("focus", show);
      hit.addEventListener("pointerleave", function () { tip.hidden = true; });
      hit.addEventListener("blur", function () { tip.hidden = true; });
      chart.appendChild(hit);
      if (d.amount === max) {
        var lab = svg("text", { x: x + bw / 2, y: y - 6, class: "aa-end", "text-anchor": "middle" });
        lab.textContent = fmt(d.amount / 100);
        chart.appendChild(lab);
      }
      if (i % every === 0 || i === data.length - 1) {
        var tl = svg("text", { x: x + bw / 2, y: H - 8, class: "aa-tick", "text-anchor": "middle" });
        tl.textContent = new Date(d.week + "T12:00:00Z").toLocaleDateString("en-GB", { day: "numeric", month: "short" });
        chart.appendChild(tl);
      }
    });
    var tableRows = data.slice().reverse().map(function (d) { return el("tr", null, [el("td", { text: dateText(d.week + "T12:00:00Z") }), el("td", { class: "num", text: sar(d.amount) })]); });
    return el("div", null, [
      el("div", { class: "aa-chart" }, [chart, tip]),
      el("details", { class: "aa-details" }, [el("summary", { text: "Show as a table" }), el("table", { class: "aa-plain" }, [el("thead", null, [el("tr", null, [el("th", { text: "Week of" }), el("th", { class: "num", text: "Earnings" })])]), el("tbody", null, tableRows)])]),
    ]);
  }

  function exportCsv(rows) {
    var cell = function (v) { return '"' + String(v === null || v === undefined ? "" : v).replace(/"/g, '""') + '"'; };
    var lines = [["Name", "Email", "Phone", "Course", "Amount (SAR)", "Status", "Submitted", "Approved"].map(cell).join(",")];
    rows.forEach(function (s) {
      lines.push([s.fullName, s.email, s.phone, "ETHCS303", ((Number(s.amount) || 0) / 100).toFixed(2), s.status,
        toDate(s.submittedAt) ? toDate(s.submittedAt).toISOString() : "", toDate(s.reviewedAt) ? toDate(s.reviewedAt).toISOString() : ""].map(cell).join(","));
    });
    var blob = new Blob(["﻿" + lines.join("\r\n")], { type: "text/csv;charset=utf-8" });
    var a = el("a", { href: URL.createObjectURL(blob), download: "ethics-sales-" + new Date().toISOString().slice(0, 10) + ".csv" });
    document.body.appendChild(a);
    a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 0);
  }

  // -------------------------------------------------------- tab: students --
  function renderStudents(root) {
    var buyers = Object.keys(S.roster).filter(function (uid) {
      var s = S.roster[uid];
      return s.status === "approved" && (!S.term || inTerm(s.reviewedAt || s.submittedAt) || S.progress.some(function (p) { return p.uid === uid && inTerm(p.lastSeenAt); }));
    });
    var byUid = {};
    S.progress.forEach(function (p) { byUid[p.uid] = p; });
    var stats = buyers.map(function (uid) {
      return Object.assign({ uid: uid, info: S.roster[uid] }, studentStats(byUid[uid] || { lessons: {}, quizzes: {} }));
    });
    var viewsWeek = 0, views = 0, quizWeek = 0, quizTerm = 0, follow = 0;
    stats.forEach(function (s) { viewsWeek += s.viewsWeek; views += s.views; quizWeek += s.quizzesWeek ? 1 : 0; quizTerm += s.quizzes ? 1 : 0; follow += s.follow.length ? 1 : 0; });
    root.appendChild(el("div", { class: "aa-tiles" }, [
      tile("Students", fmt(stats.length), S.term ? "this term" : "all buyers"),
      tile("Views this week", fmt(viewsWeek), fmt(views) + (S.term ? " this term" : " in total")),
      tile("Took a quiz this week", fmt(quizWeek), fmt(quizTerm) + (S.term ? " this term" : " in total")),
      tile("Need follow-up", fmt(follow), "inactive 7+ days or quiz average under 60%", follow ? "warn" : null),
    ]));

    var tabs = [
      ["roster", "Students"],
      ["quizzes", "Quiz performance"],
      ["mistakes", "Common mistakes"],
      ["comments", "Comments"],
      ["reports", "Reported questions"],
    ];
    var bar = el("div", { class: "ac-subtabs", role: "tablist", "aria-label": "Student views" });
    var panel = el("div", { class: "ac-subpanel" });
    function open(id) {
      bar.querySelectorAll("button").forEach(function (b) { b.setAttribute("aria-selected", String(b.dataset.id === id)); });
      panel.textContent = "";
      if (id === "roster") renderRoster(panel, stats, byUid);
      if (id === "quizzes") renderQuizStats(panel);
      if (id === "mistakes") renderMistakes(panel);
      if (id === "comments") renderComments(panel);
      if (id === "reports") renderReports(panel);
    }
    tabs.forEach(function (t) {
      bar.appendChild(el("button", { type: "button", role: "tab", "data-id": t[0], "aria-selected": "false", text: t[1], onclick: function () { open(t[0]); } }));
    });
    root.appendChild(bar);
    root.appendChild(panel);
    open("roster");
  }

  function renderRoster(panel, stats, byUid) {
    if (!stats.length) return panel.appendChild(emptyNote("No approved students in this range."));
    stats.sort(function (a, b) { return b.follow.length - a.follow.length || (b.last || 0) - (a.last || 0); });
    var body = el("tbody");
    stats.forEach(function (s) {
      var detail = el("tr", { class: "ac-detail", hidden: "" }, [el("td", { colspan: "7" })]);
      var row = el("tr", { class: "ac-row", tabindex: "0", "aria-expanded": "false" }, [
        el("td", null, [el("strong", { text: s.info.fullName || "–" }), el("small", { class: "ac-sub", text: s.info.email || "" })]),
        el("td", { text: s.last ? dateText(s.last, true) : "Never" }),
        el("td", { class: "num", text: fmt(s.lessonsSeen) }),
        el("td", { class: "num", text: duration(s.watch) }),
        el("td", { class: "num", text: fmt(s.quizzes) }),
        el("td", { class: "num", text: s.avg === null ? "–" : Math.round(s.avg * 100) + "%" }),
        el("td", null, [s.follow.length ? el("span", { class: "ac-pill ac-pending", text: "! " + s.follow.join(", ") }) : el("span", { class: "ac-pill ac-approved", text: "✓ On track" })]),
      ]);
      function toggle() {
        var openNow = detail.hidden;
        detail.hidden = !openNow;
        row.setAttribute("aria-expanded", String(openNow));
        if (openNow && !detail.firstChild.firstChild) detail.firstChild.appendChild(studentDetail(byUid[s.uid], s.info));
      }
      row.addEventListener("click", toggle);
      row.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggle(); } });
      body.appendChild(row);
      body.appendChild(detail);
    });
    panel.appendChild(el("div", { class: "aa-table-wrap" }, [el("table", { class: "aa-plain ac-roster" }, [
      el("thead", null, [el("tr", null, ["Student", "Last active", "Lessons", "Watched", "Quizzes", "Quiz avg", "Status"].map(function (h, i) {
        return el("th", { scope: "col", class: i >= 2 && i <= 5 ? "num" : "", text: h });
      }))]),
      body,
    ])]));
    panel.appendChild(el("p", { class: "aa-note", text: "Click a student to see each lesson and quiz." }));
  }

  function studentDetail(p, info) {
    var box = el("div", { class: "ac-student" });
    if (info.phone) box.appendChild(el("p", { class: "aa-note", text: "Phone: " + info.phone }));
    if (!p) { box.appendChild(emptyNote("This student hasn't opened the course since tracking started.")); return box; }
    var lessons = Object.keys(p.lessons || {}).map(function (k) { return p.lessons[k]; }).filter(function (l) { return l.kind !== "page"; });
    lessons.sort(function (a, b) { return (toDate(b.lastAt) || 0) - (toDate(a.lastAt) || 0); });
    var quizzes = Object.keys(p.quizzes || {}).map(function (k) { return p.quizzes[k]; });
    box.appendChild(el("h4", { text: "Quizzes" }));
    box.appendChild(quizzes.length ? el("ul", { class: "ac-mini" }, quizzes.map(function (q) {
      var wrong = Object.keys(q.questions || {}).map(function (h) { return q.questions[h]; }).filter(function (x) { return x.wrong > 0 && x.text; });
      return el("li", null, [
        el("strong", { text: q.title || "Quiz" }),
        el("span", { class: "ac-sub", text: " · last " + (q.lastScore !== undefined ? q.lastScore + "%" : "–") + ", best " + (q.best !== undefined ? q.best + "%" : "–") + ", " + fmt(q.attempts) + " attempts · " + dateText(q.lastAt) }),
        wrong.length ? el("ul", null, wrong.slice(0, 5).map(function (w) { return el("li", { class: "ac-wrong", text: "✕ " + w.text }); })) : null,
      ]);
    })) : emptyNote("No quizzes yet."));
    box.appendChild(el("h4", { text: "Lessons" }));
    box.appendChild(lessons.length ? el("ul", { class: "ac-mini" }, lessons.slice(0, 40).map(function (l) {
      return el("li", null, [
        el("strong", { text: l.title || "Lesson" }),
        el("span", { class: "ac-sub", text: " · " + fmt(l.views) + " views" + (l.maxPct ? ", watched to " + l.maxPct + "%" : "") + (Number(l.reaction) === 1 ? " · 👍" : Number(l.reaction) === -1 ? " · 👎" : "") + " · " + dateText(l.lastAt) }),
      ]);
    })) : emptyNote("No lessons yet."));
    return box;
  }

  function quizMap() {
    var map = {};
    S.progress.forEach(function (p) {
      Object.keys(p.quizzes || {}).forEach(function (k) {
        var q = p.quizzes[k];
        if (!inTerm(q.lastAt)) return;
        var r = map[k] || (map[k] = { key: k, title: q.title || k, path: q.path, students: 0, answered: 0, correct: 0, bestSum: 0, bestN: 0, questions: {} });
        r.students++;
        r.answered += Number(q.answered) || 0;
        r.correct += Number(q.correct) || 0;
        if (q.best !== undefined) { r.bestSum += Number(q.best); r.bestN++; }
        Object.keys(q.questions || {}).forEach(function (h) {
          var x = q.questions[h];
          var t = r.questions[h] || (r.questions[h] = { text: "", seen: 0, wrong: 0, students: 0 });
          t.seen += Number(x.seen) || 0;
          t.wrong += Number(x.wrong) || 0;
          if (x.wrong) t.students++;
          if (x.text) t.text = x.text;
        });
      });
    });
    return map;
  }

  function renderQuizStats(panel) {
    var map = quizMap();
    var rows = Object.keys(map).map(function (k) { return map[k]; }).sort(function (a, b) { return b.students - a.students; });
    if (!rows.length) return panel.appendChild(emptyNote("No quiz answers recorded yet."));
    panel.appendChild(el("div", { class: "aa-table-wrap" }, [el("table", { class: "aa-plain" }, [
      el("thead", null, [el("tr", null, ["Quiz", "Students", "Answers", "Correct", "Avg best score"].map(function (h, i) { return el("th", { scope: "col", class: i ? "num" : "", text: h }); }))]),
      el("tbody", null, rows.map(function (r) {
        return el("tr", null, [
          el("td", null, [r.path ? el("a", { href: r.path, target: "_blank", rel: "noopener", text: r.title }) : r.title]),
          el("td", { class: "num", text: fmt(r.students) }),
          el("td", { class: "num", text: fmt(r.answered) }),
          el("td", { class: "num strong", text: pct(r.correct, r.answered) }),
          el("td", { class: "num", text: r.bestN ? Math.round(r.bestSum / r.bestN) + "%" : "–" }),
        ]);
      })),
    ])]));
  }

  function renderMistakes(panel) {
    var map = quizMap();
    var list = [];
    Object.keys(map).forEach(function (k) {
      var q = map[k];
      Object.keys(q.questions).forEach(function (h) {
        var x = q.questions[h];
        if (x.wrong && x.text) list.push({ quiz: q.title, path: q.path, text: x.text, wrong: x.wrong, seen: x.seen, students: x.students });
      });
    });
    list.sort(function (a, b) { return b.wrong / b.seen - a.wrong / a.seen || b.wrong - a.wrong; });
    list = list.filter(function (x) { return x.seen >= 2; });
    if (!list.length) return panel.appendChild(emptyNote("No repeated mistakes yet. A question appears here once it's been answered at least twice."));
    panel.appendChild(el("p", { class: "aa-note", text: "Questions students get wrong most often, worst first. These are good candidates for a re-explanation." }));
    panel.appendChild(el("div", { class: "aa-table-wrap" }, [el("table", { class: "aa-plain" }, [
      el("thead", null, [el("tr", null, ["Question", "Quiz", "Wrong", "Students who missed it"].map(function (h, i) { return el("th", { scope: "col", class: i >= 2 ? "num" : "", text: h }); }))]),
      el("tbody", null, list.slice(0, 60).map(function (x) {
        return el("tr", null, [
          el("td", { text: x.text }),
          el("td", null, [x.path ? el("a", { href: x.path, target: "_blank", rel: "noopener", text: x.quiz }) : x.quiz]),
          el("td", { class: "num strong", text: pct(x.wrong, x.seen) + " of " + fmt(x.seen) }),
          el("td", { class: "num", text: fmt(x.students) }),
        ]);
      })),
    ])]));
  }

  function slugFor(path) {
    return path.replace(/\//g, "|").replace(/^\||\ |$/g, "") || "home";
  }

  function renderComments(panel) {
    var paths = {};
    S.progress.forEach(function (p) {
      Object.keys(p.lessons || {}).forEach(function (k) { if (p.lessons[k].path) paths[p.lessons[k].path] = p.lessons[k].title || k; });
    });
    var list = Object.keys(paths);
    if (!list.length) return panel.appendChild(emptyNote("No paid lessons visited yet, so there are no comments to show."));
    var only = el("label", { class: "ac-check" }, [el("input", { type: "checkbox", checked: "" }), " Only comments waiting for your reply"]);
    var box = el("div", { class: "ah-report-list" });
    panel.appendChild(only);
    panel.appendChild(box);
    box.appendChild(emptyNote("Loading comments…"));
    Promise.all(list.map(function (pth) {
      return db.collection("pageComments").doc(slugFor(pth)).collection("comments").get()
        .then(function (snap) { return snap.docs.map(function (d) { return Object.assign({ id: d.id, page: pth, pageTitle: paths[pth] }, d.data()); }); })
        .catch(function () { return []; });
    })).then(function (groups) {
      var all = [].concat.apply([], groups);
      var answered = {};
      all.forEach(function (c) { if (c.replyTo && c.uid === user.uid) answered[c.replyTo] = true; });
      function paint() {
        var waitingOnly = only.querySelector("input").checked;
        var top = all.filter(function (c) { return !c.replyTo && c.uid !== user.uid && (!waitingOnly || !answered[c.id]); })
          .sort(function (a, b) { return (toDate(b.createdAt) || 0) - (toDate(a.createdAt) || 0); });
        box.textContent = "";
        if (!top.length) return box.appendChild(emptyNote(waitingOnly ? "Nothing waiting for a reply." : "No comments yet."));
        top.forEach(function (c) {
          box.appendChild(el("article", { class: "ah-report" }, [
            el("header", null, [el("strong", { text: c.displayName || c.username || "Student" }), answered[c.id] ? el("span", { class: "ah-chip", text: "✓ Replied" }) : el("span", { class: "ah-chip", text: "Waiting for reply" }), el("time", { text: dateText(c.createdAt, true) })]),
            el("p", { class: "ah-question", text: c.text || "" }),
            el("footer", null, [el("a", { href: c.page + "#shoug-page-comments", target: "_blank", rel: "noopener", text: "Reply on “" + c.pageTitle + "” ↗" })]),
          ]));
        });
      }
      only.querySelector("input").addEventListener("change", paint);
      paint();
    });
  }

  function renderReports(panel) {
    panel.appendChild(emptyNote("Loading…"));
    db.collection("questionReports").where("course", "==", COURSE_CODE).get().then(function (snap) {
      panel.textContent = "";
      if (!snap.size) return panel.appendChild(emptyNote("No reported questions for this course."));
      var docs = snap.docs.slice().sort(function (a, b) { return (toDate(b.data().createdAt) || 0) - (toDate(a.data().createdAt) || 0); });
      panel.appendChild(el("div", { class: "ah-report-list" }, docs.map(function (d) {
        var r = d.data();
        return el("article", { class: "ah-report" }, [
          el("header", null, [el("strong", { text: "Q" + (r.qid || "?") }), el("span", { class: "ah-chip", text: r.reason || "report" }), el("time", { text: dateText(r.createdAt, true) })]),
          r.question ? el("p", { class: "ah-question", text: r.question }) : null,
          r.note ? el("p", { class: "ah-note", text: "Student note: " + r.note }) : null,
          el("footer", null, [r.source && r.source.charAt(0) === "/" ? el("a", { href: r.source, target: "_blank", rel: "noopener", text: "Open the question ↗" }) : null, el("a", { href: "/admin/reports/", text: "Resolve in Question reports →" })]),
        ]);
      })));
    }).catch(function (e) { panel.textContent = ""; panel.appendChild(emptyNote("Couldn't load reports: " + e.message)); });
  }

  // -------------------------------------------------------- tab: calendar --
  function localInput(d) {
    var r = new Date(d.getTime() + 3 * 3600000);
    return r.toISOString().slice(0, 16);
  }
  function fromLocal(v) { return new Date(v + ":00+03:00"); }

  function renderCalendar(root) {
    root.appendChild(el("p", { class: "aa-note", text: "Times are Riyadh time. Paid students see upcoming events and open slots on the course home page, and can book a slot." }));
    var evCard = el("section", { class: "aa-card" }, [el("header", { class: "aa-card-head" }, [el("h3", { text: "Events" }), el("p", { text: "Live sessions, office hours and academic dates" })])]);
    var slotCard = el("section", { class: "aa-card" }, [el("header", { class: "aa-card-head" }, [el("h3", { text: "Bookable slots & bookings" }), el("p", { text: "One student per slot" })])]);
    root.appendChild(el("div", { class: "ac-two" }, [evCard, slotCard]));

    // New event form
    var start = new Date(Date.now() + 86400000); start.setMinutes(0, 0, 0);
    var form = el("form", { class: "ac-form" }, [
      el("label", null, ["Title", el("input", { name: "title", required: "", maxlength: "120", class: "ac-input" })]),
      el("label", null, ["Type", el("select", { name: "type", class: "ac-input" }, Object.keys(TYPE_NAMES).map(function (k) { return el("option", { value: k, text: TYPE_NAMES[k] }); }))]),
      el("label", null, ["Starts", el("input", { name: "start", type: "datetime-local", required: "", value: localInput(start), class: "ac-input" })]),
      el("label", null, ["Ends", el("input", { name: "end", type: "datetime-local", required: "", value: localInput(new Date(start.getTime() + 3600000)), class: "ac-input" })]),
      el("label", { class: "ac-wide" }, ["Join link (optional, https://)", el("input", { name: "link", type: "url", maxlength: "500", class: "ac-input", placeholder: "https://" })]),
      el("button", { type: "submit", class: "ac-btn ac-primary", text: "+ Add event" }),
    ]);
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var f = form.elements;
      var s = fromLocal(f.start.value), en = fromLocal(f.end.value);
      if (en <= s) return alert("The end must be after the start.");
      var link = f.link.value.trim();
      if (link && !/^https:\/\//.test(link)) return alert("The link must start with https://");
      db.collection("courseEvents").add({ course: COURSE, title: f.title.value.trim(), type: f.type.value, start: s, end: en, link: link, createdAt: fb.firestore.FieldValue.serverTimestamp() })
        .then(function () { form.reset(); loadEvents(); });
    });
    evCard.appendChild(form);
    var evList = el("div", { class: "ac-list" });
    evCard.appendChild(evList);
    function loadEvents() {
      evList.textContent = "";
      db.collection("courseEvents").where("course", "==", COURSE).get().then(function (snap) {
        var items = snap.docs.map(function (d) { return Object.assign({ id: d.id }, d.data()); })
          .sort(function (a, b) { return toDate(b.start) - toDate(a.start); });
        if (!items.length) return evList.appendChild(emptyNote("No events yet."));
        var now = new Date();
        items.forEach(function (ev) {
          var past = toDate(ev.end) < now;
          evList.appendChild(el("div", { class: "ac-item" + (past ? " is-past" : "") }, [
            el("div", null, [el("strong", { text: ev.title }), el("small", { class: "ac-sub", text: (TYPE_NAMES[ev.type] || "Event") + " · " + dateText(ev.start, true) + (past ? " · past" : "") })]),
            el("button", { type: "button", class: "ac-btn ac-danger", text: "Delete", onclick: function () {
              if (confirm("Delete “" + ev.title + "”?")) db.collection("courseEvents").doc(ev.id).delete().then(loadEvents);
            } }),
          ]));
        });
      });
    }
    loadEvents();

    // Slots: several at once (date, first start, length, how many).
    var slotForm = el("form", { class: "ac-form" }, [
      el("label", null, ["First slot", el("input", { name: "start", type: "datetime-local", required: "", value: localInput(start), class: "ac-input" })]),
      el("label", null, ["Minutes each", el("input", { name: "minutes", type: "number", min: "10", max: "240", value: "30", class: "ac-input" })]),
      el("label", null, ["How many", el("input", { name: "count", type: "number", min: "1", max: "20", value: "4", class: "ac-input" })]),
      el("button", { type: "submit", class: "ac-btn ac-primary", text: "+ Add slots" }),
    ]);
    slotForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var f = slotForm.elements;
      var s = fromLocal(f.start.value), mins = Math.max(10, Number(f.minutes.value) || 30), n = Math.min(20, Math.max(1, Number(f.count.value) || 1));
      var batch = db.batch();
      for (var i = 0; i < n; i++) {
        var st = new Date(s.getTime() + i * mins * 60000);
        batch.set(db.collection("courseSlots").doc(), { course: COURSE, start: st, end: new Date(st.getTime() + mins * 60000), createdAt: fb.firestore.FieldValue.serverTimestamp() });
      }
      batch.commit().then(loadSlots);
    });
    slotCard.appendChild(slotForm);
    var slotList = el("div", { class: "ac-list" });
    slotCard.appendChild(slotList);
    function loadSlots() {
      slotList.textContent = "";
      Promise.all([db.collection("courseSlots").where("course", "==", COURSE).get(), db.collection("courseBookings").get()]).then(function (r) {
        var bookings = {};
        r[1].forEach(function (d) { bookings[d.id] = d.data(); });
        var items = r[0].docs.map(function (d) { return Object.assign({ id: d.id }, d.data()); })
          .sort(function (a, b) { return toDate(a.start) - toDate(b.start); });
        if (!items.length) return slotList.appendChild(emptyNote("No slots yet."));
        var now = new Date();
        items.forEach(function (sl) {
          var b = bookings[sl.id];
          var past = toDate(sl.end) < now;
          slotList.appendChild(el("div", { class: "ac-item" + (past ? " is-past" : "") }, [
            el("div", null, [
              el("strong", { text: dateText(sl.start, true) }),
              b ? el("small", { class: "ac-sub", text: "Booked by " + (b.name || (S.roster[b.uid] && S.roster[b.uid].fullName) || "a student") + (b.note ? " — “" + b.note + "”" : "") }) : el("small", { class: "ac-sub", text: past ? "Past, not booked" : "Open" }),
            ]),
            b ? el("button", { type: "button", class: "ac-btn", text: "Cancel booking", onclick: function () {
              if (confirm("Cancel this student's booking?")) db.collection("courseBookings").doc(sl.id).delete().then(loadSlots);
            } }) : null,
            el("button", { type: "button", class: "ac-btn ac-danger", text: "Delete", onclick: function () {
              if (!confirm(b ? "This slot is booked. Delete it and the booking?" : "Delete this slot?")) return;
              var batch = db.batch();
              batch.delete(db.collection("courseSlots").doc(sl.id));
              if (b) batch.delete(db.collection("courseBookings").doc(sl.id));
              batch.commit().then(loadSlots);
            } }),
          ]));
        });
      });
    }
    loadSlots();
  }

  // -------------------------------------------------------- tab: settings --
  function renderSettings(root) {
    var card = el("section", { class: "aa-card" }, [el("header", { class: "aa-card-head" }, [el("h3", { text: "Terms" }), el("p", { text: "Each term runs from its start date until the next one starts. Every tab can be filtered by term." })])]);
    var list = el("div", { class: "ac-list" });
    function paint() {
      list.textContent = "";
      if (!S.terms.length) list.appendChild(emptyNote("No terms yet. Everything shows all time until you add one."));
      S.terms.forEach(function (t, i) {
        list.appendChild(el("div", { class: "ac-item" }, [
          el("div", null, [el("strong", { text: t.label }), el("small", { class: "ac-sub", text: "from " + dateText(t.start + "T12:00:00+03:00") })]),
          el("button", { type: "button", class: "ac-btn ac-danger", text: "Remove", onclick: function () {
            var next = S.terms.slice(); next.splice(i, 1); saveTerms(next);
          } }),
        ]));
      });
    }
    var form = el("form", { class: "ac-form" }, [
      el("label", null, ["Name", el("input", { name: "label", required: "", maxlength: "40", placeholder: "e.g. Term 261", class: "ac-input" })]),
      el("label", null, ["Starts on", el("input", { name: "start", type: "date", required: "", class: "ac-input" })]),
      el("button", { type: "submit", class: "ac-btn ac-primary", text: "+ Add term" }),
    ]);
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var next = S.terms.concat([{ label: form.elements.label.value.trim(), start: form.elements.start.value }]);
      saveTerms(next);
      form.reset();
    });
    function saveTerms(next) {
      next.sort(function (a, b) { return a.start < b.start ? -1 : 1; });
      db.collection("courseConfig").doc(COURSE).set({ terms: next }, { merge: true }).then(function () {
        S.terms = next;
        if (S.term && !next.some(function (t) { return t.start === S.term; })) S.term = null;
        renderTermPicker();
        paint();
      }).catch(function (e) { alert("Couldn't save: " + e.message); });
    }
    card.appendChild(list);
    card.appendChild(form);
    root.appendChild(card);
    paint();
    root.appendChild(el("section", { class: "aa-card" }, [
      el("header", { class: "aa-card-head" }, [el("h3", { text: "About this data" })]),
      el("p", { class: "aa-note", text: "Lesson views, watch time, likes and quiz answers are recorded only for students whose payment you approved, from the moment this panel went live. The privacy notice tells students that you can see their progress. Payment details come from the Course payments page." }),
    ]));
  }

  // ---------------------------------------------------------------- shell --
  var RENDER = { lessons: renderLessons, earnings: renderEarnings, students: renderStudents, calendar: renderCalendar, settings: renderSettings };
  function render() {
    document.querySelectorAll("[data-tab]").forEach(function (b) { b.setAttribute("aria-selected", String(b.dataset.tab === S.tab)); });
    var root = $("ac-panel");
    root.textContent = "";
    RENDER[S.tab](root);
  }

  function loadAll() {
    status("Loading course data…");
    return Promise.all([loadConfig(), loadSales(), loadProgress()]).then(function (r) {
      S.terms = r[0];
      if (S.term === null && S.terms.length) {
        var today = new Date().toISOString().slice(0, 10);
        var current = S.terms.filter(function (t) { return t.start <= today; }).pop();
        S.term = current ? current.start : null;
      }
      S.sales = r[1];
      S.roster = {};
      S.sales.forEach(function (s) { S.roster[s.uid || s.id] = s; });
      S.progress = r[2];
      renderTermPicker();
      status("");
      $("ac-content").hidden = false;
      render();
    }).catch(function (e) {
      status("Couldn't load the course data: " + e.message + (e.code === "permission-denied" ? " (publish the updated Firestore rules first)" : ""), true);
    });
  }

  function isAdmin(u) {
    if (!u.emailVerified) return Promise.resolve(false);
    return db.collection("courseCommerce").doc("ethics").get().then(function (s) { return s.exists && s.data().adminUid === u.uid; });
  }

  function boot() {
    fb = window.__shoug_fb;
    db = fb.firestore();
    fb.auth().onAuthStateChanged(function (u) {
      user = u;
      $("ac-content").hidden = true;
      $("ac-login").hidden = !!u;
      if (!u) return status("");
      status("Checking your account…");
      isAdmin(u).then(function (ok) {
        if (!ok) return status("This page is for the site administrator.", true);
        loadAll();
      }).catch(function (e) { status("Couldn't check your account: " + e.message, true); });
    });
  }

  document.querySelectorAll("[data-tab]").forEach(function (b) {
    b.addEventListener("click", function () { S.tab = b.dataset.tab; render(); });
  });
  $("ac-term").addEventListener("change", function (e) { S.term = e.target.value || null; render(); });
  $("ac-refresh").addEventListener("click", loadAll);
  $("ac-signin").addEventListener("click", function () {
    if (window.__shougOpenAuthModal) window.__shougOpenAuthModal();
  });
  if (window.__shoug_fb) boot();
  else window.addEventListener("shoug:fb", boot, { once: true });
})();
