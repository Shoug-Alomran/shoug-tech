/* CYS401 past papers: marking engine for the replica exam sheets.
   Every markable piece carries data-unit and data-marks:
     radio   .opts / .fig-opts holding radio inputs; data-answer = option value
     select  <select>; data-answer = "A|B" (any listed value is right)
     text    <input>; data-accept = "A|B" compared on letters/digits only,
             or data-pattern = regular expression tested on the raw text
     num     <input>; data-answer = number (the first number typed is used)
     matrix  <table> of inputs; data-answer = the cells left to right
     axis    McCumber axis: select.title plus three select.item
     stride-threat / stride-prop / stride-cat  cells of a STRIDE table row
     written self-marked: holds a .model the reader reveals, then scores
   A .q groups units, owns the feedback box and the Check button. */
(function () {
  "use strict";

  var KEY = "cys401pp:" + location.pathname;
  var STRIDE = {
    S: {
      name: "Spoofing",
      prop: ["authentication", "authenticity"],
      cat: ["fabrication"],
    },
    T: { name: "Tampering", prop: ["integrity"], cat: ["modification"] },
    R: {
      name: "Repudiation",
      prop: ["nonrepudiation", "accountability"],
      cat: ["fabrication", "modification"],
    },
    I: {
      name: "Information disclosure",
      prop: ["confidentiality"],
      cat: ["interception"],
    },
    D: {
      name: "Denial of service",
      prop: ["availability"],
      cat: ["interruption"],
    },
    E: {
      name: "Elevation of privilege",
      prop: ["authorization", "authorisation"],
      cat: ["modification"],
    },
  };

  function $$(sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  }

  function norm(s) {
    return String(s || "")
      .toUpperCase()
      .replace(/[^A-Z0-9]/g, "");
  }

  function fmt(n) {
    return (Math.round(n * 100) / 100).toString();
  }

  function threatKey(text) {
    var t = String(text || "").toLowerCase();
    if (/spoof/.test(t)) return "S";
    if (/tamper/.test(t)) return "T";
    if (/repud/.test(t)) return "R";
    if (/disclos|information leak|info\b|info\./.test(t)) return "I";
    if (/denial|\bdos\b|\bddos\b/.test(t)) return "D";
    if (/elevat|privil/.test(t)) return "E";
    return "";
  }

  /* ---------- grading ---------- */
  function rowThreat(row) {
    if (row.dataset.given) return row.dataset.given;
    var inp = row.querySelector('[data-unit="stride-threat"]');
    return inp ? threatKey(inp.value) : "";
  }

  function grade(u) {
    var kind = u.dataset.unit;
    var marks = parseFloat(u.dataset.marks || "0");
    var r = { got: 0, max: marks, ok: false, answered: true, show: "" };

    if (kind === "radio") {
      var picked = u.querySelector("input:checked");
      r.answered = !!picked;
      r.ok = !!picked && picked.value === u.dataset.answer;
      $$("label", u).forEach(function (l) {
        var inp = l.querySelector("input");
        l.classList.toggle("is-right", inp.value === u.dataset.answer);
        l.classList.toggle(
          "is-wrong",
          inp.checked && inp.value !== u.dataset.answer,
        );
      });
    } else if (kind === "select") {
      var okVals = u.dataset.answer.split("|").map(norm);
      r.answered = !!u.value;
      r.ok = okVals.indexOf(norm(u.value)) !== -1;
      r.show = u.dataset.answer.split("|")[0];
    } else if (kind === "text") {
      r.answered = !!u.value.trim();
      if (u.dataset.pattern) {
        r.ok = new RegExp(u.dataset.pattern, "i").test(u.value);
      } else {
        r.ok =
          u.dataset.accept.split("|").map(norm).indexOf(norm(u.value)) !== -1;
      }
      r.show = u.dataset.show || (u.dataset.accept || "").split("|")[0];
    } else if (kind === "num") {
      var m = String(u.value)
        .replace(/,/g, "")
        .match(/-?\d+(\.\d+)?/);
      r.answered = !!m;
      r.ok =
        !!m && Math.abs(parseFloat(m[0]) - parseFloat(u.dataset.answer)) < 1e-9;
      r.show = u.dataset.show || u.dataset.answer;
    } else if (kind === "matrix") {
      var want = u.dataset.answer.split("");
      var cells = $$("input", u);
      var right = 0;
      r.answered = cells.some(function (c) {
        return c.value.trim();
      });
      cells.forEach(function (c, i) {
        var v = norm(c.value).replace("J", "I");
        var good = v === want[i];
        if (good) right++;
        c.parentNode.classList.toggle("is-right", good);
        c.parentNode.classList.toggle("is-wrong", !good);
      });
      r.ok = right === cells.length;
      r.show = "";
    } else if (kind === "axis") {
      var title = u.querySelector("select.title");
      var items = $$("select.item", u).map(function (s) {
        return s.value;
      });
      var sets = JSON.parse(u.closest(".mc").dataset.sets);
      var expect = sets[title.value];
      var axes = $$('[data-unit="axis"]', u.closest(".mc"));
      var reused = axes.slice(0, axes.indexOf(u)).some(function (x) {
        return x.querySelector("select.title").value === title.value;
      });
      r.answered = !!title.value;
      r.ok =
        !reused &&
        !!expect &&
        items.slice().sort().join("|") === expect.slice().sort().join("|");
    } else if (kind === "stride-threat") {
      var row = u.closest("tr");
      var k = threatKey(u.value);
      var earlier = $$("tr", row.parentNode).slice(
        0,
        $$("tr", row.parentNode).indexOf(row),
      );
      var dup = earlier.some(function (tr) {
        return rowThreat(tr) === k;
      });
      r.answered = !!u.value.trim();
      r.ok = !!k && !dup;
    } else if (kind === "stride-prop" || kind === "stride-cat") {
      var key = rowThreat(u.closest("tr"));
      var list = key
        ? STRIDE[key][kind === "stride-prop" ? "prop" : "cat"]
        : [];
      var val = u.value.toLowerCase().replace(/[^a-z]/g, "");
      r.answered = !!val;
      r.ok =
        !!key &&
        list.some(function (w) {
          return val.indexOf(w) !== -1;
        });
      r.show = key ? list[0] : "a STRIDE threat in this row first";
    } else if (kind === "written") {
      var pressed = u.querySelector('.selfmark button[aria-pressed="true"]');
      r.self = true;
      r.answered = !!pressed;
      r.got = pressed ? parseFloat(pressed.dataset.v) : 0;
      return r;
    }
    r.got = r.ok ? marks : 0;
    if (kind !== "radio" && kind !== "matrix" && kind !== "axis") {
      u.classList.toggle("is-right", r.ok);
      u.classList.toggle("is-wrong", !r.ok);
    }
    return r;
  }

  function autoUnits(root) {
    return $$("[data-unit]", root).filter(function (u) {
      return u.dataset.unit !== "written";
    });
  }

  function checkQ(q) {
    var units = autoUnits(q);
    if (!units.length) return;
    var got = 0,
      max = 0,
      wrongShows = [];
    units.forEach(function (u) {
      var r = grade(u);
      got += r.got;
      max += r.max;
      if (!r.ok && r.show) wrongShows.push(r.show);
      u.dataset.graded = "1";
    });
    var fb = q.querySelector(":scope > .fb");
    if (!fb) return;
    var cls = got >= max - 1e-9 ? "ok" : got > 0 ? "part" : "no";
    var verdict =
      cls === "ok"
        ? "Correct."
        : cls === "part"
          ? "Partly right."
          : "Not quite.";
    var html =
      '<span class="verdict">' +
      verdict +
      "</span>" +
      fmt(got) +
      " / " +
      fmt(max) +
      " marks.";
    if (wrongShows.length && !q.dataset.hideExpected) {
      html += " Expected: <b>" + wrongShows.join("</b>, <b>") + "</b>.";
    }
    var why = q.querySelector(":scope > .why");
    if (why) html += "<div>" + why.innerHTML + "</div>";
    fb.innerHTML = html;
    fb.className = "fb show " + cls;
  }

  /* ---------- scores ---------- */
  function updateScore() {
    var all = $$("[data-unit]");
    var total = 0,
      got = 0,
      self = 0;
    all.forEach(function (u) {
      var m = parseFloat(u.dataset.marks || "0");
      total += m;
      if (u.dataset.unit === "written") {
        var p = u.querySelector('.selfmark button[aria-pressed="true"]');
        if (p) self += parseFloat(p.dataset.v);
      } else if (u.dataset.graded) {
        got += grade(u).got;
      }
    });
    var el = document.getElementById("pp-score");
    if (el) {
      el.textContent =
        "Score " +
        fmt(got + self) +
        " / " +
        fmt(total) +
        (self ? " (self-marked " + fmt(self) + ")" : "");
    }
    var byQ = {};
    all.forEach(function (u) {
      var holder = u.closest("[data-qno]");
      var id = holder ? holder.dataset.qno : "";
      var v = null;
      if (u.dataset.unit === "written") {
        var p = u.querySelector('.selfmark button[aria-pressed="true"]');
        if (p) v = parseFloat(p.dataset.v);
      } else if (u.dataset.graded) {
        v = grade(u).got;
      }
      if (v === null) return;
      if (id && id !== "all") byQ[id] = (byQ[id] || 0) + v;
      byQ.all = (byQ.all || 0) + v;
    });
    $$(".got[data-q]").forEach(function (slot) {
      var v = byQ[slot.dataset.q];
      slot.textContent = v === undefined ? "" : fmt(v);
    });
  }

  /* ---------- written answers ---------- */
  function steps(m) {
    var out = [0];
    var parts = m >= 1 ? [0.25, 0.5, 0.75] : [0.5];
    parts.forEach(function (p) {
      out.push(m * p);
    });
    out.push(m);
    return out;
  }

  function setupWritten(u) {
    var m = parseFloat(u.dataset.marks || "0");
    var tools = document.createElement("div");
    tools.className = "q-tools";
    var show = document.createElement("button");
    show.type = "button";
    show.className = "pp-btn";
    show.textContent = "Show model answer";
    var sm = document.createElement("span");
    sm.className = "selfmark";
    sm.innerHTML = "Mark yourself:";
    steps(m).forEach(function (v) {
      var b = document.createElement("button");
      b.type = "button";
      b.dataset.v = String(v);
      b.setAttribute("aria-pressed", "false");
      b.textContent = fmt(v);
      b.addEventListener("click", function () {
        $$("button", sm).forEach(function (x) {
          x.setAttribute("aria-pressed", "false");
        });
        b.setAttribute("aria-pressed", "true");
        save();
        updateScore();
      });
      sm.appendChild(b);
    });
    var model = u.querySelector(".model");
    show.addEventListener("click", function () {
      var on = !model.classList.contains("show");
      model.classList.toggle("show", on);
      sm.classList.toggle("show", on);
      show.textContent = on ? "Hide model answer" : "Show model answer";
    });
    tools.appendChild(show);
    tools.appendChild(sm);
    model.parentNode.insertBefore(tools, model);
  }

  function revealAll(on) {
    $$('[data-unit="written"]').forEach(function (u) {
      var model = u.querySelector(".model");
      var sm = u.querySelector(".selfmark");
      var btn = u.querySelector(".q-tools .pp-btn");
      model.classList.toggle("show", on);
      sm.classList.toggle("show", on);
      if (btn) btn.textContent = on ? "Hide model answer" : "Show model answer";
    });
  }

  /* ---------- answer table mirror (Sem 181 paper) ---------- */
  function mirror() {
    $$("[data-mirror]").forEach(function (td) {
      var picked = document.querySelector(
        'input[name="' + td.dataset.mirror + '"]:checked',
      );
      td.textContent = picked
        ? picked
            .closest("label")
            .querySelector(".ol")
            .textContent.replace(/[.)]/g, "")
        : "";
    });
  }

  /* ---------- persistence (this viewer only) ---------- */
  function fields() {
    return $$(".sheet input, .sheet select, .sheet textarea");
  }

  function save() {
    try {
      var data = { f: {}, s: {} };
      fields().forEach(function (el, i) {
        if (el.type === "radio") {
          if (el.checked) data.f[i] = "1";
        } else if (el.value) data.f[i] = el.value;
      });
      $$('[data-unit="written"]').forEach(function (u, i) {
        var p = u.querySelector('.selfmark button[aria-pressed="true"]');
        if (p) data.s[i] = p.dataset.v;
      });
      localStorage.setItem(KEY, JSON.stringify(data));
    } catch (e) {}
  }

  function restore() {
    var data;
    try {
      data = JSON.parse(localStorage.getItem(KEY) || "null");
    } catch (e) {
      data = null;
    }
    if (!data) return;
    var els = fields();
    Object.keys(data.f || {}).forEach(function (i) {
      var el = els[+i];
      if (!el) return;
      if (el.type === "radio") el.checked = true;
      else el.value = data.f[i];
    });
    var ws = $$('[data-unit="written"]');
    Object.keys(data.s || {}).forEach(function (i) {
      var u = ws[+i];
      if (!u) return;
      $$(".selfmark button", u).forEach(function (b) {
        b.setAttribute(
          "aria-pressed",
          b.dataset.v === data.s[i] ? "true" : "false",
        );
      });
      u.querySelector(".model").classList.add("show");
      u.querySelector(".selfmark").classList.add("show");
      var btn = u.querySelector(".q-tools .pp-btn");
      if (btn) btn.textContent = "Hide model answer";
    });
  }

  function reset() {
    if (!window.confirm("Clear every answer on this paper?")) return;
    try {
      localStorage.removeItem(KEY);
    } catch (e) {}
    fields().forEach(function (el) {
      if (el.type === "radio") el.checked = false;
      else el.value = "";
    });
    $$(".is-right, .is-wrong").forEach(function (el) {
      el.classList.remove("is-right", "is-wrong");
    });
    $$(".fb").forEach(function (fb) {
      fb.className = "fb";
      fb.innerHTML = "";
    });
    $$("[data-graded]").forEach(function (u) {
      delete u.dataset.graded;
    });
    $$(".selfmark button").forEach(function (b) {
      b.setAttribute("aria-pressed", "false");
    });
    revealAll(false);
    mirror();
    updateScore();
  }

  /* ---------- wiring ---------- */
  function init() {
    $$('[data-unit="written"]').forEach(setupWritten);

    $$(".q").forEach(function (q) {
      if (
        !autoUnits(q).filter(function (u) {
          return u.closest(".q") === q;
        }).length
      )
        return;
      var tools = document.createElement("div");
      tools.className = "q-tools";
      var b = document.createElement("button");
      b.type = "button";
      b.className = "pp-btn";
      b.textContent = "Check";
      b.addEventListener("click", function () {
        checkQ(q);
        updateScore();
      });
      tools.appendChild(b);
      var fb = document.createElement("div");
      fb.className = "fb";
      fb.setAttribute("aria-live", "polite");
      var anchor = q.querySelector(":scope > .why");
      q.insertBefore(tools, anchor);
      q.insertBefore(fb, anchor);
    });

    $$(".table-stack-labels").forEach(function (t) {
      var heads = $$("thead th", t).map(function (th) {
        return th.textContent.trim();
      });
      $$("tbody tr", t).forEach(function (tr) {
        $$("td", tr).forEach(function (td, i) {
          if (heads[i]) td.setAttribute("data-label", heads[i]);
        });
      });
    });

    restore();
    mirror();

    document.addEventListener("input", function (e) {
      if (e.target.closest(".sheet")) save();
    });
    document.addEventListener("change", function (e) {
      if (e.target.closest(".sheet")) {
        save();
        mirror();
      }
    });

    var all = document.getElementById("pp-check");
    if (all)
      all.addEventListener("click", function () {
        $$(".q").forEach(checkQ);
        updateScore();
      });
    var rev = document.getElementById("pp-reveal");
    if (rev)
      rev.addEventListener("click", function () {
        var on = rev.getAttribute("aria-pressed") !== "true";
        rev.setAttribute("aria-pressed", on ? "true" : "false");
        rev.textContent = on ? "Hide model answers" : "Show model answers";
        rev.dataset.short = on ? "Hide" : "Answers";
        revealAll(on);
      });
    var rst = document.getElementById("pp-reset");
    if (rst) rst.addEventListener("click", reset);

    updateScore();
  }

  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", init);
  else init();
})();
