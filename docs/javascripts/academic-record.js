/**
 * Academic record: the final grades a student received and, optionally, the
 * totals from their transcript, kept on their own users/{uid} doc so the
 * calendar can work out semester and cumulative GPA the way PSU does.
 *
 *   academicRecord.transcript         = { gpa, hours, term }  totals through `term`
 *   academicRecord.courses["CS 331"]  = { letter, hours, term }
 *
 * Course grades come from the "MY GRADE" row on each course overview, the
 * Final grade menu in the calendar, or "Add a course" in the calendar for
 * courses this site doesn't have. A course in a term the transcript already
 * covers is not counted twice.
 *
 * Helpers are on window.ShougAcademicRecord (the calendar uses them). Loaded
 * by mobile-navigation.js on course overviews and by the calendar page.
 */
(function () {
  "use strict";

  if (window.ShougAcademicRecord) return;

  // PSU 4.0 scale (Undergraduate Study and Examinations By-Law, Appendix 1).
  var POINTS = { "A+": 4, A: 3.75, "B+": 3.5, B: 3, "C+": 2.5, C: 2, "D+": 1.5, D: 1, F: 0, DN: 0 };
  var NO_GPA = ["W", "NP", "NF"];
  var LETTERS = ["A+", "A", "B+", "B", "C+", "C", "D+", "D", "F", "DN", "W", "NP", "NF"];

  // Term codes are YY + 1 (First, from August), 2 (Second, from December)
  // or 3 (Summer of the next year): 252 Second Semester 2025, 253 Summer
  // 2026, 261 First Semester 2026.
  function termName(code) {
    var m = String(code || "").match(/^(\d{2})([123])$/);
    if (!m) return code ? "Term " + code : "";
    var y = 2000 + Number(m[1]);
    return m[2] === "1"
      ? "First Semester " + y
      : m[2] === "2"
        ? "Second Semester " + y
        : "Summer " + (y + 1);
  }
  function termForDate(d) {
    d = d || new Date();
    var y = d.getFullYear() % 100,
      mo = d.getMonth() + 1,
      day = d.getDate();
    if (mo >= 8 && (mo < 12 || day < 11)) return pad(y) + "1";
    if (mo === 12) return pad(y) + "2";
    if (mo <= 5) return pad(y - 1) + "2";
    return pad(y - 1) + "3";
  }
  function pad(n) {
    return (n < 10 ? "0" : "") + n;
  }
  function prevTerm(code) {
    var y = Number(String(code).slice(0, 2)),
      n = Number(String(code).slice(2));
    return n > 1 ? pad(y) + (n - 1) : pad(y - 1) + "3";
  }
  // The current term and the ones before it, newest first.
  function recentTerms(current, count) {
    var out = [current || termForDate()];
    while (out.length < (count || 24)) out.push(prevTerm(out[out.length - 1]));
    return out;
  }
  // "cs331", "CS-331" and "ethcs303" become "CS 331" and "ETHCS 303".
  function courseCode(value) {
    var m = String(value || "").match(/([A-Za-z]{2,6})\s*-?\s*(\d{3}[A-Za-z]?)/);
    return m ? m[1].toUpperCase() + " " + m[2].toUpperCase() : String(value || "").trim().toUpperCase();
  }
  function validTranscript(t) {
    return (
      t &&
      isFinite(Number(t.gpa)) &&
      Number(t.gpa) >= 0 &&
      Number(t.gpa) <= 4 &&
      Number(t.hours) > 0 &&
      /^\d{3}$/.test(String(t.term || ""))
    );
  }
  function counts(c) {
    return c && POINTS[c.letter] !== undefined && NO_GPA.indexOf(c.letter) < 0 && Number(c.hours) > 0;
  }

  /**
   * Cumulative GPA: transcript totals, plus recorded courses from terms after
   * the transcript (and before `current`), plus this semester's points.
   * `skip` lists course codes the semester figures already include.
   */
  function cumulative(record, current, semQP, semHours, skip) {
    record = record || {};
    var t = validTranscript(record.transcript) ? record.transcript : null,
      qp = t ? Number(t.gpa) * Number(t.hours) : 0,
      hours = t ? Number(t.hours) : 0,
      added = [],
      covered = [];
    Object.keys(record.courses || {}).forEach(function (code) {
      var c = record.courses[code];
      if (!counts(c) || !c.term || c.term >= current || (skip || []).indexOf(code) > -1) return;
      if (t && c.term <= t.term) {
        covered.push(code);
        return;
      }
      qp += POINTS[c.letter] * Number(c.hours);
      hours += Number(c.hours);
      added.push(code);
    });
    qp += semQP || 0;
    hours += semHours || 0;
    return {
      gpa: hours ? qp / hours : null,
      hours: hours,
      qp: qp,
      transcript: t,
      added: added,
      covered: covered,
    };
  }

  function withCurrent(record, current, semQP, semHours) {
    return cumulative(record, current, semQP, semHours, []);
  }

  window.ShougAcademicRecord = {
    POINTS: POINTS,
    NO_GPA: NO_GPA,
    LETTERS: LETTERS,
    termName: termName,
    termForDate: termForDate,
    prevTerm: prevTerm,
    recentTerms: recentTerms,
    courseCode: courseCode,
    validTranscript: validTranscript,
    counts: counts,
    cumulative: cumulative,
    withCurrent: withCurrent,
  };

  // ── Course overview: private "MY GRADE" row in the info panel ────────────

  var TRACKS = "computer-science|software-engineering|cybersecurity|math|other-courses";
  var COURSE_PATH = new RegExp("^/academics/(?:" + TRACKS + ")/(?:english/)?([a-z]+\\d{3})/$");
  var path = location.pathname.replace(/index\.html$/, "");
  var match = path.match(COURSE_PATH);
  if (!match) return;

  function isArabic() {
    return (document.documentElement.lang || "").indexOf("ar") === 0;
  }
  function L(en, ar) {
    return isArabic() && ar ? ar : en;
  }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (ch) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch];
    });
  }

  var STYLE = [
    ".agr-row[hidden],.agr-form[hidden]{display:none!important}",
    ".agr-val{display:inline-flex;align-items:center;gap:8px;flex-wrap:wrap;background:none;border:0;padding:0;font:inherit;color:var(--text-main,#e2d9f3);cursor:pointer;text-align:start}",
    ".agr-val:hover,.agr-val:focus-visible{color:var(--brand-purple,#b829ea);outline:none}",
    ".agr-val .agr-add{color:var(--brand-purple,#b829ea);text-decoration:underline}",
    ".agr-val small{color:var(--text-dim,var(--text-muted,#8b7ea8));font-size:.85em}",
    ".agr-form{display:grid;gap:10px;margin:4px 0 14px;padding:14px;border:1px dashed var(--border-dim,var(--border-main,#2a1f3d));font-family:var(--font-mono,monospace);font-size:12px}",
    ".agr-form label{display:grid;gap:4px;color:var(--text-dim,var(--text-muted,#8b7ea8));font-size:10px;letter-spacing:.12em;text-transform:uppercase}",
    ".agr-form select,.agr-form input{width:100%;box-sizing:border-box;min-height:34px;padding:6px 8px;background:var(--bg-surface,#0a0514);border:1px solid var(--border-dim,var(--border-main,#2a1f3d));color:var(--text-main,#e2d9f3);font:inherit;font-size:13px;letter-spacing:0;text-transform:none}",
    ".agr-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,110px),1fr));gap:10px}",
    ".agr-actions{display:flex;flex-wrap:wrap;gap:8px;align-items:center}",
    ".agr-btn{font-family:var(--font-mono,monospace);font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;padding:8px 14px;border:1px solid var(--brand-purple,#b829ea);background:var(--brand-purple,#b829ea);color:#fff;cursor:pointer}",
    ".agr-btn.agr-ghost{background:transparent;color:var(--brand-purple,#b829ea)}",
    ".agr-btn[disabled]{opacity:.45;cursor:default}",
    ".agr-note{margin:0;color:var(--text-dim,var(--text-muted,#8b7ea8));font-size:11px;line-height:1.6}",
  ].join("\n");

  function pageCreditHours() {
    var rows = document.querySelectorAll(".meta-row");
    for (var i = 0; i < rows.length; i++) {
      var k = rows[i].querySelector(".meta-key"),
        v = rows[i].querySelector(".meta-val");
      if (k && v && /credit/i.test(k.textContent)) {
        var n = parseInt(v.textContent, 10);
        if (n > 0 && n < 13) return n;
      }
    }
    return 3;
  }

  function init() {
    var meta = document.querySelector(".meta-content");
    if (!meta) return;
    var code = courseCode(match[1]),
      defaultHours = pageCreditHours(),
      current = termForDate();

    var s = document.createElement("style");
    s.id = "agr-style";
    s.textContent = STYLE;
    document.head.appendChild(s);

    var row = document.createElement("div");
    row.className = "meta-row agr-row";
    row.hidden = true;
    row.innerHTML =
      '<span class="meta-key">' + L("MY GRADE", "تقديري") + '</span><button type="button" class="meta-val agr-val" aria-expanded="false"></button>';
    var form = document.createElement("div");
    form.className = "agr-form";
    form.hidden = true;
    var before = meta.querySelector(".meta-links-title");
    meta.insertBefore(row, before || null);
    meta.insertBefore(form, before || null);
    var val = row.querySelector(".agr-val");

    var state = { ref: null, record: {}, saving: false };

    function mine() {
      return (state.record.courses || {})[code] || null;
    }
    function renderValue() {
      var c = mine();
      val.innerHTML = c
        ? "<b>" + esc(c.letter) + "</b><small>" + esc(c.hours) + " " + L("hrs", "ساعات") + " · " + esc(termName(c.term)) + "</small>"
        : '<span class="agr-add">' + L("Add the grade you received", "أضف تقديرك") + "</span>";
    }
    function renderForm() {
      var c = mine() || {},
        terms = recentTerms(current, 24),
        term = c.term || current,
        t = validTranscript(state.record.transcript) ? state.record.transcript : null;
      if (terms.indexOf(term) < 0) terms.push(term);
      form.innerHTML =
        '<div class="agr-grid"><label>' + L("Grade", "التقدير") + '<select data-agr="letter">' +
        LETTERS.map(function (l) {
          return '<option value="' + l + '"' + (c.letter === l ? " selected" : "") + ">" + l + "</option>";
        }).join("") +
        "</select></label><label>" + L("Credit hours", "الساعات") + '<input data-agr="hours" type="number" min="1" max="12" step="1" value="' +
        esc(c.hours || defaultHours) +
        '"></label></div><label>' + L("Semester taken", "الفصل") + '<select data-agr="term">' +
        terms.map(function (x) {
          return '<option value="' + x + '"' + (x === term ? " selected" : "") + ">" + esc(termName(x)) + "</option>";
        }).join("") +
        '</select></label><p class="agr-note" data-agr="note"></p><div class="agr-actions"><button type="button" class="agr-btn" data-agr="save">' +
        L("Save", "حفظ") + "</button>" +
        (mine() ? '<button type="button" class="agr-btn agr-ghost" data-agr="remove">' + L("Remove", "حذف") + "</button>" : "") +
        '<button type="button" class="agr-btn agr-ghost" data-agr="cancel">' + L("Cancel", "إلغاء") + "</button></div>";
      var note = form.querySelector('[data-agr="note"]'),
        termSel = form.querySelector('[data-agr="term"]');
      function updateNote() {
        note.textContent =
          t && termSel.value <= t.term
            ? L(
                "Already part of the transcript totals in your calendar (through " + termName(t.term) + "), so it won't be counted twice.",
                "هذا الفصل مشمول في إجمالي السجل الأكاديمي في التقويم، فلن يُحتسب مرتين.",
              )
            : L("Only you can see this. Your calendar uses it for your cumulative GPA.", "لا يراه أحد غيرك، ويُستخدم لحساب معدلك التراكمي في التقويم.");
      }
      termSel.addEventListener("change", updateNote);
      updateNote();
      form.querySelector('[data-agr="save"]').addEventListener("click", save);
      form.querySelector('[data-agr="cancel"]').addEventListener("click", function () {
        toggle(false);
      });
      var rm = form.querySelector('[data-agr="remove"]');
      if (rm) rm.addEventListener("click", remove);
    }
    function toggle(open) {
      form.hidden = !open;
      val.setAttribute("aria-expanded", open ? "true" : "false");
      if (open) renderForm();
    }
    function write(entry) {
      var fb = window.__shoug_fb,
        courses = {};
      courses[code] = entry === null ? fb.firestore.FieldValue.delete() : entry;
      state.saving = true;
      form.querySelectorAll("button").forEach(function (b) {
        b.disabled = true;
      });
      return state.ref
        .set({ academicRecord: { courses: courses } }, { merge: true })
        .then(function () {
          state.saving = false;
          toggle(false);
        })
        .catch(function () {
          state.saving = false;
          form.querySelectorAll("button").forEach(function (b) {
            b.disabled = false;
          });
          form.querySelector('[data-agr="note"]').textContent = L("Could not save. Check your connection and try again.", "تعذّر الحفظ. تحقق من اتصالك وحاول مرة أخرى.");
        });
    }
    function save() {
      var hours = Math.round(Number(form.querySelector('[data-agr="hours"]').value));
      if (!(hours >= 1 && hours <= 12)) {
        form.querySelector('[data-agr="note"]').textContent = L("Credit hours must be between 1 and 12.", "يجب أن تكون الساعات بين 1 و12.");
        return;
      }
      write({
        letter: form.querySelector('[data-agr="letter"]').value,
        hours: hours,
        term: form.querySelector('[data-agr="term"]').value,
      });
    }
    function remove() {
      write(null);
    }
    val.addEventListener("click", function () {
      toggle(form.hidden);
    });

    var unsub = null;
    function withFirebase(cb) {
      if (window.__shoug_fb) return cb(window.__shoug_fb);
      window.addEventListener(
        "shoug:fb",
        function () {
          cb(window.__shoug_fb);
        },
        { once: true },
      );
      if (typeof window.__shougLoadFirebaseAuth === "function") window.__shougLoadFirebaseAuth(false);
    }
    withFirebase(function (fb) {
      fb.auth().onAuthStateChanged(function (user) {
        if (unsub) unsub();
        unsub = null;
        if (!user) {
          row.hidden = true;
          form.hidden = true;
          return;
        }
        state.ref = fb.firestore().collection("users").doc(user.uid);
        unsub = state.ref.onSnapshot(function (snap) {
          var data = (snap && snap.exists && snap.data()) || {};
          state.record = data.academicRecord && typeof data.academicRecord === "object" ? data.academicRecord : {};
          row.hidden = false;
          renderValue();
        });
      });
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
