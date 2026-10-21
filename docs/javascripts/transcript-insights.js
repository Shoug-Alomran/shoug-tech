/**
 * Transcript insights on /account/transcript/: a semester history chart (each
 * term's GPA against the cumulative GPA after it) and graduation progress
 * against the student's academic plan. Reads the private academic record the
 * page has already loaded and the plan page's course list; it never writes.
 *
 * The page calls window.ShougTranscriptInsights.render(record) whenever the
 * record changes.
 */
(function () {
  "use strict";

  var AR = window.ShougAcademicRecord;
  if (!AR) return;
  var SVG = "http://www.w3.org/2000/svg";
  // Courses for non-native Arabic speakers stand in for the plan's versions.
  var EQUIVALENT = {
    "ARAB 113": "ARAB 103",
    "ARAB 213": "ARAB 203",
    "ISC 113": "ISC 103",
    "ISC 213": "ISC 203",
  };
  var NOT_PASSED = ["F", "DN", "W", "NF"];
  var PLAN_KEY = "shoug-transcript-plan";
  var lastRecord = null;
  // { plan: { summer: ["PHY 205"] }, save(plan) } from the page; the plan
  // lives in the private record as degreePlan.
  var lastOpts = {};
  // A typical PSU summer load; more summer courses spill into the next summer.
  var SUMMER_HOURS = 9;

  function $(id) {
    return document.getElementById(id);
  }
  function esc(v) {
    return String(v == null ? "" : v).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function pad(n) {
    return (n < 10 ? "0" : "") + n;
  }
  function el(name, attrs, parent) {
    var node = document.createElementNS(SVG, name);
    Object.keys(attrs || {}).forEach(function (k) {
      node.setAttribute(k, attrs[k]);
    });
    if (parent) parent.appendChild(node);
    return node;
  }
  // "1st ’23", "2nd ’23", "Sum ’24" (summer is named by the year it runs in).
  function termShort(code) {
    var y = Number(code.slice(0, 2)),
      n = code.charAt(2);
    return n === "1" ? "1st ’" + pad(y) : n === "2" ? "2nd ’" + pad(y) : "Sum ’" + pad(y + 1);
  }

  // ── Semester history ─────────────────────────────────────────────────────

  function historyRows(record) {
    var byTerm = {},
      courses = record.courses || {};
    Object.keys(courses).forEach(function (code) {
      var c = courses[code];
      if (!c || c.finished === false || !AR.counts(c, code) || !/^\d{3}$/.test(String(c.term))) return;
      var t = byTerm[c.term] || (byTerm[c.term] = { qp: 0, hours: 0 });
      t.qp += AR.POINTS[c.letter] * Number(c.hours);
      t.hours += Number(c.hours);
    });
    var qp = 0,
      hours = 0;
    return Object.keys(byTerm)
      .sort()
      .map(function (term) {
        var t = byTerm[term];
        qp += t.qp;
        hours += t.hours;
        return { term: term, gpa: t.qp / t.hours, hours: t.hours, cum: qp / hours, cumHours: hours };
      });
  }

  function drawHistory(host, rows) {
    host.innerHTML = "";
    var W = Math.max(280, host.clientWidth || 600),
      narrow = W < 560,
      H = narrow ? 230 : 270,
      m = { t: 14, r: narrow ? 74 : 112, b: 30, l: 34 },
      lo = Math.min.apply(
        null,
        rows.map(function (r) {
          return Math.min(r.gpa, r.cum);
        }),
      ),
      yMin = Math.max(0, Math.floor((lo - 0.2) * 2) / 2),
      plotW = W - m.l - m.r,
      plotH = H - m.t - m.b;
    function x(i) {
      return m.l + (rows.length === 1 ? plotW / 2 : (i * plotW) / (rows.length - 1));
    }
    function y(v) {
      return m.t + ((4 - v) / (4 - yMin)) * plotH;
    }
    var svg = el("svg", { viewBox: "0 0 " + W + " " + H, width: W, height: H, role: "img", "aria-label": "Term GPA and cumulative GPA by semester" }, host);
    for (var v = yMin; v <= 4.001; v += 0.5) {
      el("line", { class: "ti-grid", x1: m.l, x2: W - m.r + 8, y1: y(v), y2: y(v) }, svg);
      el("text", { class: "ti-axis", x: m.l - 8, y: y(v) + 4, "text-anchor": "end" }, svg).textContent = v.toFixed(1);
    }
    var every = Math.max(1, Math.ceil(rows.length / Math.max(2, Math.floor(plotW / 52))));
    rows.forEach(function (r, i) {
      if (i % every && i !== rows.length - 1) return;
      el("text", { class: "ti-axis", x: x(i), y: H - 8, "text-anchor": "middle" }, svg).textContent = termShort(r.term);
    });
    var cross = el("line", { class: "ti-cross", x1: 0, x2: 0, y1: m.t, y2: H - m.b, visibility: "hidden" }, svg);
    var series = [
      { key: "gpa", cls: "ti-s1", label: "Term", short: "Term" },
      { key: "cum", cls: "ti-s2", label: "Cumulative", short: "Cum." },
    ];
    var ends = [];
    series.forEach(function (s) {
      var d = rows
        .map(function (r, i) {
          return (i ? "L" : "M") + x(i).toFixed(1) + " " + y(r[s.key]).toFixed(1);
        })
        .join(" ");
      el("path", { class: "ti-line " + s.cls, d: d }, svg);
      rows.forEach(function (r, i) {
        el("circle", { class: "ti-dot " + s.cls, cx: x(i), cy: y(r[s.key]), r: 4 }, svg);
      });
      ends.push({ s: s, y: y(rows[rows.length - 1][s.key]) });
    });
    // Direct labels at the line ends, nudged apart when the lines finish close.
    if (Math.abs(ends[0].y - ends[1].y) < 16) {
      var mid = (ends[0].y + ends[1].y) / 2,
        up = ends[0].y <= ends[1].y ? 0 : 1;
      ends[up].y = mid - 8;
      ends[1 - up].y = mid + 8;
    }
    ends.forEach(function (e) {
      var t = el("text", { class: "ti-end", x: x(rows.length - 1) + 10, y: e.y + 4 }, svg);
      t.textContent = (narrow ? e.s.short : e.s.label) + " " + rows[rows.length - 1][e.s.key].toFixed(2);
    });
    // Hover and touch: one hit column per semester, wider than the marks.
    var tip = document.createElement("div");
    tip.className = "ti-tip";
    tip.hidden = true;
    host.appendChild(tip);
    rows.forEach(function (r, i) {
      var half = rows.length === 1 ? plotW / 2 : plotW / (rows.length - 1) / 2;
      var hit = el("rect", { class: "ti-hit", x: x(i) - half, y: m.t, width: half * 2, height: plotH, tabindex: 0, "aria-label": AR.termName(r.term) + ": term GPA " + r.gpa.toFixed(2) + ", cumulative " + r.cum.toFixed(2) }, svg);
      function show() {
        cross.setAttribute("x1", x(i));
        cross.setAttribute("x2", x(i));
        cross.setAttribute("visibility", "visible");
        tip.innerHTML =
          "<b>" + esc(AR.termName(r.term)) + "</b>" +
          '<span><i class="ti-key ti-s1"></i>Term GPA ' + r.gpa.toFixed(2) + " · " + r.hours + " hrs</span>" +
          '<span><i class="ti-key ti-s2"></i>Cumulative ' + r.cum.toFixed(2) + " · " + r.cumHours + " hrs</span>";
        tip.hidden = false;
        var left = x(i) + 12;
        if (left + tip.offsetWidth > W) left = x(i) - 12 - tip.offsetWidth;
        tip.style.left = Math.max(0, left) + "px";
        tip.style.top = m.t + "px";
      }
      function hide() {
        cross.setAttribute("visibility", "hidden");
        tip.hidden = true;
      }
      hit.addEventListener("mouseenter", show);
      hit.addEventListener("focus", show);
      hit.addEventListener("touchstart", show, { passive: true });
      hit.addEventListener("mouseleave", hide);
      hit.addEventListener("blur", hide);
    });
  }

  function renderHistory(record) {
    var card = $("history-card");
    if (!card) return;
    var rows = historyRows(record);
    card.hidden = rows.length < 2;
    if (card.hidden) return;
    drawHistory($("history-chart"), rows);
    $("history-table").innerHTML =
      "<table><thead><tr><th>Semester</th><th>Hours</th><th>Term GPA</th><th>Cumulative</th></tr></thead><tbody>" +
      rows
        .map(function (r) {
          return "<tr><td>" + esc(AR.termName(r.term)) + "</td><td>" + r.hours + "</td><td>" + r.gpa.toFixed(2) + "</td><td>" + r.cum.toFixed(2) + "</td></tr>";
        })
        .join("") +
      "</tbody></table>";
  }

  // ── Graduation progress ──────────────────────────────────────────────────

  var plans = {};
  function literal(source, name) {
    var m = source.match(new RegExp("(?:const|let|var)\\s+" + name + "\\s*=\\s*(\\{[\\s\\S]*?\\})\\s*;"));
    if (!m) return {};
    try {
      return JSON.parse(m[1].replace(/([{,]\s*)([A-Za-z_$][\w$]*)(\s*:)/g, '$1"$2"$3').replace(/,\s*([}\]])/g, "$1"));
    } catch (e) {
      return {};
    }
  }
  function loadPlan(value) {
    if (plans[value]) return plans[value];
    plans[value] = fetch("/academic-plan-themes/" + value + ".html")
      .then(function (r) {
        if (!r.ok) throw Error("plan " + r.status);
        return r.text();
      })
      .then(function (html) {
        var source = Array.prototype.map
          .call(new DOMParser().parseFromString(html, "text/html").scripts, function (s) {
            return s.textContent;
          })
          .find(function (t) {
            return /COURSES_RAW\s*=/.test(t);
          });
        var m = source && source.match(/(?:const|let|var)\s+COURSES_RAW\s*=\s*(\[[\s\S]*?\n\s*\]);/);
        if (!m) throw Error("No course list in this plan");
        var text = m[1]
          .replace(/\/\*[\s\S]*?\*\//g, "")
          .replace(/^\s*\/\/.*$/gm, "")
          .replace(/([{,]\s*)([A-Za-z_$][\w$]*)(\s*:)/g, '$1"$2"$3')
          .replace(/,\s*([}\]])/g, "$1");
        var key = source.match(/localStorage\.setItem\(\s*["']([^"']*choices)["']/);
        return { courses: JSON.parse(text), limits: literal(source, "GROUP_LIMITS"), meta: literal(source, "GROUP_META"), choicesKey: key ? key[1] : "" };
      });
    plans[value].catch(function () {
      delete plans[value];
    });
    return plans[value];
  }
  function nextSummer(term) {
    var y = Number(term.slice(0, 2));
    return term.charAt(2) === "3" ? pad(y + 1) + "3" : pad(y) + "3";
  }
  function nextRegular(term) {
    var y = Number(term.slice(0, 2)),
      n = term.charAt(2);
    return n === "1" ? pad(y) + "2" : pad(y + 1) + "1";
  }

  function progress(record, plan, summer) {
    var current = AR.termForDate(),
      courses = record.courses || {},
      status = {},
      counted = {};
    Object.keys(courses).forEach(function (code) {
      var c = courses[code],
        key = EQUIVALENT[code] || code;
      if (!c) return;
      var passed = c.finished !== false && c.letter && NOT_PASSED.indexOf(c.letter) < 0;
      if (passed) {
        status[key] = { state: "done", code: code, hours: Number(c.hours) };
        if (!AR.isPrep(code)) counted[key] = code;
      } else if (!c.letter && String(c.term) === current && !(status[key] && status[key].state === "done")) {
        status[key] = { state: "now", code: code, hours: Number(c.hours) };
      }
    });
    function st(id) {
      return status[AR.courseCode(id)] || null;
    }
    var choices = {};
    try {
      choices = JSON.parse(localStorage.getItem(plan.choicesKey) || "{}") || {};
    } catch (e) {}
    var groups = {},
      planIds = {},
      needed = [],
      open = [];
    plan.courses.forEach(function (c) {
      planIds[AR.courseCode(c.id)] = true;
      if (c.group) (groups[c.group] || (groups[c.group] = [])).push(c);
      else needed.push(c);
    });
    Object.keys(groups).forEach(function (g) {
      var limit = Number(plan.limits[g]) || 1,
        options = groups[g],
        taken = options.filter(function (c) {
          return st(c.id);
        }),
        chosen = [].concat(choices[g] || []).map(function (id) {
          return options.find(function (c) {
            return c.id === id;
          });
        }),
        pick = taken
          .concat(
            chosen.filter(function (c) {
              return c && taken.indexOf(c) < 0;
            }),
          )
          .slice(0, limit);
      needed = needed.concat(pick);
      if (pick.length < limit) open.push({ group: g, label: plan.meta[g] || "Elective group " + g, missing: limit - pick.length, hours: options[0].hours });
    });
    var done = [],
      now = [],
      left = [];
    needed.forEach(function (c) {
      var s = st(c.id);
      (s && s.state === "done" ? done : s && s.state === "now" ? now : left).push(c);
    });
    function sum(list) {
      return list.reduce(function (t, c) {
        return t + Number(c.hours || 0);
      }, 0);
    }
    var openHours = open.reduce(function (t, o) {
        return t + o.missing * o.hours;
      }, 0),
      ready = [],
      waiting = [];
    left.forEach(function (c) {
      var pre = c.prereqs || [];
      if (
        pre.every(function (p) {
          var s = st(p);
          return s && s.state === "done";
        })
      )
        ready.push(c);
      else
        waiting.push({
          course: c,
          after: pre.filter(function (p) {
            var s = st(p);
            return !(s && s.state === "done");
          }),
        });
    });
    // Pace: average hours over the last three regular (non-summer) semesters.
    var perTerm = {};
    Object.keys(courses).forEach(function (code) {
      var c = courses[code],
        t = String((c && c.term) || "");
      if (/^\d{2}[12]$/.test(t) && (c.letter || t === current)) perTerm[t] = (perTerm[t] || 0) + Number(c.hours || 0);
    });
    var recent = Object.keys(perTerm).sort().slice(-3),
      pace = recent.length
        ? Math.round(
            recent.reduce(function (t, k) {
              return t + perTerm[k];
            }, 0) / recent.length,
          )
        : 15,
      remaining = sum(left) + openHours,
      summerSet = {};
    (summer || []).forEach(function (code) {
      summerSet[AR.courseCode(code)] = true;
    });
    // Courses marked for summer come off the regular semesters and go into
    // the summers after this term, up to SUMMER_HOURS each.
    var summerCourses = left.filter(function (c) {
        return summerSet[AR.courseCode(c.id)];
      }),
      summerHours = sum(summerCourses),
      regularLeft = remaining - summerHours,
      terms = regularLeft ? Math.ceil(regularLeft / Math.max(pace, 1)) : 0,
      summers = summerHours ? Math.ceil(summerHours / SUMMER_HOURS) : 0,
      finish = current,
      lastSummer = "",
      nextS = nextSummer(current);
    for (var i = 0; i < terms; i++) finish = nextRegular(finish);
    for (var j = 0; j < summers; j++) {
      lastSummer = nextS;
      nextS = nextSummer(nextS);
    }
    if (lastSummer > finish) finish = lastSummer;
    var outside = Object.keys(counted)
      .filter(function (key) {
        return !planIds[key];
      })
      .map(function (key) {
        return counted[key];
      });
    return {
      total: sum(needed) + openHours,
      doneHours: sum(done),
      nowHours: sum(now),
      left: left,
      leftHours: remaining,
      now: now,
      ready: ready,
      waiting: waiting,
      open: open,
      outside: outside.sort(),
      pace: pace,
      terms: terms,
      finish: finish,
      summerSet: summerSet,
      summerHours: summerHours,
      regularLeft: regularLeft,
      summers: summers,
      groups: groups,
    };
  }

  function chip(c, note, summerOn) {
    var code = AR.courseCode(c.id);
    return (
      '<li class="ti-chip' + (summerOn ? " ti-is-summer" : "") + '"><div><b>' + esc(code) + "</b> " + esc(c.name || "") +
      " <span>" + esc(c.hours) + " hrs" + (note ? " · " + esc(note) : "") + (summerOn ? " · planned for summer" : "") + "</span></div>" +
      '<button type="button" class="ti-summer" data-summer="' + esc(code) + '" aria-pressed="' + (summerOn ? "true" : "false") + '" title="Plan this course for a summer term">Summer</button></li>'
    );
  }
  // "Math Elective - choose 1" -> "Math elective".
  function groupLabel(label) {
    var clean = String(label || "").replace(/\s*[-–]\s*choose\s*\d+\s*$/i, "");
    return clean.replace(/\b(Elective|Education)\b/g, function (w) {
      return w.toLowerCase();
    });
  }
  function gridPlanUrl(value) {
    var match = /^(cs-ai|cs-cys|cs-dx|se-ai|se-cys|se|is-ai)(?:\/classic)?$/.exec(String(value || ""));
    return match ? "/academic-plan-themes/" + match[1] + "/grid.html" : "/academic-plan-themes/se-cys/grid.html";
  }
  function renderProgress(record) {
    var card = $("progress-card"),
      select = $("progress-plan"),
      source = $("plan");
    if (!card || !select) return;
    var hasCourses = Object.keys(record.courses || {}).length > 0;
    card.hidden = !hasCourses;
    if (!hasCourses) return;
    if (!select.options.length && source) select.innerHTML = source.innerHTML;
    var saved = "";
    try {
      saved = localStorage.getItem(PLAN_KEY) || "";
    } catch (e) {}
    if (saved && select.querySelector('option[value="' + saved + '"]')) select.value = saved;
    var gridLink = $("progress-grid-link");
    if (gridLink) gridLink.href = gridPlanUrl(select.value);
    var body = $("progress-body"),
      value = select.value;
    loadPlan(value)
      .then(function (plan) {
        if (select.value !== value) return;
        var p = progress(record, plan, (lastOpts.plan && lastOpts.plan.summer) || []),
          pct = function (h) {
            return p.total ? Math.min(100, (h / p.total) * 100) : 0;
          };
        body.innerHTML =
          '<div class="ti-stats"><div><b>' + p.doneHours + "</b><span>of " + p.total + " plan hours done</span></div>" +
          "<div><b>" + p.nowHours + "</b><span>hours in progress this semester</span></div>" +
          "<div><b>" + (p.leftHours ? esc(AR.termName(p.finish)) : "This semester") + "</b><span>" +
          (p.leftHours
            ? "estimated graduation · " +
              (p.regularLeft
                ? p.regularLeft + " hours over about " + p.terms + " more semester" + (p.terms === 1 ? "" : "s") + " at your usual " + p.pace + " hours"
                : "") +
              (p.summerHours ? (p.regularLeft ? ", plus " : "") + p.summerHours + " hours in " + (p.summers === 1 ? "a summer term" : p.summers + " summer terms") : "")
            : "everything left is in progress now") +
          "</span></div></div>" +
          '<div class="ti-bar" role="img" aria-label="' + p.doneHours + " of " + p.total + " hours done, " + p.nowHours + ' in progress"><span class="ti-done" style="width:' + pct(p.doneHours) + '%"></span><span class="ti-now" style="width:' + pct(p.nowHours) + '%"></span></div>' +
          '<div class="ti-bar-key"><span><i class="ti-done"></i>Done</span><span><i class="ti-now"></i>This semester</span><span><i class="ti-left"></i>Left</span></div>' +
          (p.ready.length
            ? '<h3 class="ti-h">Ready to take next <span>' + p.ready.length + "</span></h3><ul class=\"ti-chips\">" +
              p.ready
                .sort(function (a, b) {
                  return (a.level || 0) - (b.level || 0);
                })
                .map(function (c) {
                  return chip(c, "", p.summerSet[AR.courseCode(c.id)]);
                })
                .join("") +
              "</ul>"
            : "") +
          (p.waiting.length
            ? '<details class="ti-more"><summary>Needs a prerequisite first <span>' + p.waiting.length + '</span></summary><ul class="ti-chips">' +
              p.waiting
                .map(function (w) {
                  return chip(w.course, "after " + w.after.map(AR.courseCode).join(", "), p.summerSet[AR.courseCode(w.course.id)]);
                })
                .join("") +
              "</ul></details>"
            : "") +
          (p.open.length
            ? '<h3 class="ti-h">Electives to choose <span>' + p.open.length + '</span></h3><div class="ti-electives">' +
              p.open
                .map(function (o) {
                  return (
                    '<label class="ti-elective"><span>' + esc(groupLabel(o.label)) + (o.missing > 1 ? " (choose " + o.missing + ")" : "") + "</span>" +
                    '<select data-elective="' + esc(o.group) + '"><option value="">Choose a course</option>' +
                    p.groups[o.group]
                      .map(function (c) {
                        return '<option value="' + esc(c.id) + '">' + esc(AR.courseCode(c.id) + " · " + (c.name || "") + " · " + c.hours + " hrs") + "</option>";
                      })
                      .join("") +
                    "</select><small class=\"ti-elective-note\"><span>Counted as " + o.hours + " hours until you choose.</span><a href=\"" + gridPlanUrl(value) + "\">Choose on the grid plan</a></small></label>"
                  );
                })
                .join("") +
              "</div>"
            : "") +
          (p.outside.length
            ? '<p class="muted ti-open">Counted in your GPA but not in this plan: ' + p.outside.map(esc).join(", ") + ".</p>"
            : "");
      })
      .catch(function () {
        body.innerHTML = '<p class="muted">Could not load this plan. Check your connection and try again.</p>';
      });
  }

  // Summer toggles and elective pickers inside the progress card.
  document.addEventListener("click", function (e) {
    var btn = e.target.closest && e.target.closest("#progress-body [data-summer]");
    if (!btn || !lastRecord) return;
    var code = btn.dataset.summer,
      plan = Object.assign({}, lastOpts.plan),
      list = (plan.summer || []).filter(function (c) {
        return c !== code;
      });
    if (btn.getAttribute("aria-pressed") !== "true") list.push(code);
    plan.summer = list.sort();
    lastOpts.plan = plan;
    renderProgress(lastRecord);
    if (lastOpts.save) lastOpts.save(plan);
  });
  document.addEventListener("change", function (e) {
    var sel = e.target.closest && e.target.closest("#progress-body [data-elective]");
    if (!sel || !sel.value || !lastRecord) return;
    loadPlan($("progress-plan").value).then(function (plan) {
      if (!plan.choicesKey) return;
      var choices = {};
      try {
        choices = JSON.parse(localStorage.getItem(plan.choicesKey) || "{}") || {};
      } catch (err) {}
      var g = sel.dataset.elective,
        limit = Number(plan.limits[g]) || 1;
      // Same shape as the plan page: one course id per group, or a list.
      choices[g] = limit === 1 ? sel.value : [].concat(choices[g] || []).concat(sel.value).slice(-limit);
      try {
        localStorage.setItem(plan.choicesKey, JSON.stringify(choices));
      } catch (err) {}
      renderProgress(lastRecord);
    });
  });

  function render(record, opts) {
    lastRecord = record || {};
    if (opts) lastOpts = opts;
    renderHistory(lastRecord);
    renderProgress(lastRecord);
  }

  document.addEventListener("change", function (e) {
    if (e.target && (e.target.id === "progress-plan" || e.target.id === "plan")) {
      try {
        localStorage.setItem(PLAN_KEY, e.target.value);
      } catch (err) {}
      if (e.target.id === "progress-plan" && lastRecord) renderProgress(lastRecord);
      var gridLink = $("progress-grid-link");
      if (gridLink && e.target.id === "progress-plan") gridLink.href = gridPlanUrl(e.target.value);
    }
  });
  var resizeTimer = null;
  window.addEventListener("resize", function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function () {
      if (lastRecord) renderHistory(lastRecord);
    }, 150);
  });

  window.ShougTranscriptInsights = { render: render, historyRows: historyRows, progress: progress };
})();
