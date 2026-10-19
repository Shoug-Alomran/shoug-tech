/* SE423 past-paper engine: renders window.PAPER in the original paper order with the real marks.
   Item types (all take pts and c = concept to review):
   mcq   { q, opts, a, why }
   short { q, groups: [[what the answer must cover, [keywords], weight?]], model }  keyword graded, strict
   rows  { q, head: [label, answer], rows: [{ label, groups, model }] }    one answer box per table row
   num   { q, fields: [{ label, a, tol, unit }], model }                     numeric answers
   raci  { q, roles, tasks, graded: [task indexes], key: { index: [letter per role] }, model }
   cpm   { q, acts, cols, key: { act: [values] } }                           schedule table
   paths { q, paths: [[letters, length]], model }                             network paths + lengths
   self  { q, model }   drawing questions: compare with the model, then mark yourself */
(function () {
  "use strict";
  function norm(s) {
    return (" " + String(s).toLowerCase() + " ")
      .replace(/&/g, " and ")
      .replace(/[’']/g, "")
      .replace(/[^a-z0-9%$]+/g, " ")
      .replace(/\s+/g, " ")
      .trim();
  }
  function lev(a, b) {
    if (Math.abs(a.length - b.length) > 2) return 9;
    var pp = [],
      prev = [],
      cur = [],
      i,
      j;
    for (j = 0; j <= b.length; j++) prev[j] = j;
    for (i = 1; i <= a.length; i++) {
      cur = [i];
      for (j = 1; j <= b.length; j++) {
        cur[j] = Math.min(
          prev[j] + 1,
          cur[j - 1] + 1,
          prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1),
        );
        // adjacent swap ("chnage") counts as one edit
        if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1])
          cur[j] = Math.min(cur[j], pp[j - 2] + 1);
      }
      pp = prev;
      prev = cur;
    }
    return prev[b.length];
  }
  function wordHit(tokens, w) {
    for (var i = 0; i < tokens.length; i++) {
      var t = tokens[i];
      if (t === w) return true;
      if (w.length >= 4 && t.indexOf(w) === 0) return true;
      if (w.length >= 5) {
        var d = lev(t.slice(0, w.length + 1), w);
        if (d <= 1 || (w.length >= 8 && d <= 2)) return true;
        if (lev(t, w) <= 1) return true;
      }
    }
    return false;
  }
  function keyHit(tokens, key) {
    var words = norm(key).split(" ").filter(Boolean);
    if (!words.length) return false;
    return words.every(function (w) {
      return wordHit(tokens, w);
    });
  }
  function anyHit(tokens, keys) {
    return keys.some(function (k) {
      return keyHit(tokens, k);
    });
  }
  function tokensOf(text) {
    var n = norm(text);
    return n ? n.split(" ") : [];
  }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function words(s) {
    return (s || "").trim().split(/\s+/).filter(Boolean).length;
  }
  function q4(x) {
    return Math.round(x * 4) / 4;
  }
  function fmt(x) {
    return String(Math.round(x * 100) / 100);
  }
  function numOf(s) {
    var m = String(s || "")
      .replace(/,/g, "")
      .match(/-?\d+(\.\d+)?/);
    return m ? parseFloat(m[0]) : null;
  }

  var P = window.PAPER;
  var STORE = "se423-paper-" + P.id;
  var state = { v: {}, graded: false, checked: {}, self: {} };
  try {
    state = JSON.parse(localStorage.getItem(STORE)) || state;
  } catch (e) {}
  state.self = state.self || {};
  state.checked = state.checked || {};
  function save() {
    try {
      localStorage.setItem(STORE, JSON.stringify(state));
    } catch (e) {}
  }
  var LETTERS = ["A", "B", "C", "D", "E"];
  var RACI = ["", "R", "A", "C", "I", "A/R"];
  var all = [];
  var root = document.getElementById("paper");

  function val(id) {
    return state.v[id];
  }
  function ta(id, label, ph, small) {
    return (
      '<textarea data-f="' +
      id +
      '" aria-label="' +
      esc(label) +
      '" placeholder="' +
      esc(ph) +
      '"' +
      (small ? ' class="small"' : "") +
      ">" +
      esc(val(id) || "") +
      "</textarea>"
    );
  }
  function inp(id, label, cls) {
    var v = val(id);
    return (
      '<input type="text" inputmode="decimal" class="' +
      (cls || "num-in") +
      '" data-f="' +
      id +
      '" aria-label="' +
      esc(label) +
      '" value="' +
      esc(v == null ? "" : v) +
      '">'
    );
  }

  function body(it, id) {
    var h = "";
    if (it.type === "mcq") {
      h +=
        '<div class="opts">' +
        it.opts
          .map(function (o, k) {
            return (
              '<label class="opt" data-o="' +
              k +
              '"><input type="radio" data-f="' +
              id +
              '" name="' +
              id +
              '" value="' +
              k +
              '"' +
              (val(id) === String(k) ? " checked" : "") +
              '><span class="letter">' +
              LETTERS[k] +
              "</span><span>" +
              esc(o) +
              "</span></label>"
            );
          })
          .join("") +
        "</div>";
    } else if (it.type === "short") {
      h +=
        ta(
          id,
          "Your answer",
          "Explain in full sentences: what, how, and why.",
        ) +
        '<div class="words" data-words="' +
        id +
        '"></div>';
    } else if (it.type === "rows") {
      h +=
        '<div class="rows-tbl"><div class="rows-head"><span>' +
        esc(it.head[0]) +
        "</span><span>" +
        esc(it.head[1]) +
        "</span></div>" +
        it.rows
          .map(function (r, k) {
            return (
              '<div class="rows-row" data-row="' +
              k +
              '"><b>' +
              esc(r.label) +
              "</b>" +
              ta(
                id + "_" + k,
                r.label,
                "Characteristics, then the best communication method and why.",
                true,
              ) +
              "</div>"
            );
          })
          .join("") +
        "</div>";
    } else if (it.type === "num") {
      h +=
        '<div class="num-grid">' +
        it.fields
          .map(function (f, k) {
            return (
              '<label class="num-field" data-k="' +
              k +
              '"><span>' +
              esc(f.label) +
              "</span>" +
              inp(id + "_" + k, f.label) +
              (f.unit ? "<small>" + esc(f.unit) + "</small>" : "") +
              "</label>"
            );
          })
          .join("") +
        "</div>" +
        ta(id + "_work", "Working", "Show your working (optional).", true);
    } else if (it.type === "raci") {
      h +=
        '<div class="tbl-scroll"><table class="grid-tbl"><thead><tr><th></th>' +
        it.roles
          .map(function (r) {
            return "<th>" + esc(r) + "</th>";
          })
          .join("") +
        "</tr></thead><tbody>" +
        it.tasks
          .map(function (t, ti) {
            var asked = it.graded.indexOf(ti) >= 0;
            return (
              '<tr class="' +
              (asked ? "asked" : "not-asked") +
              '"><th>' +
              esc(t) +
              (asked ? "" : " <small>(not asked)</small>") +
              "</th>" +
              it.roles
                .map(function (r, ri) {
                  if (!asked) return "<td></td>";
                  var fid = id + "_" + ti + "_" + ri;
                  return (
                    '<td data-cell="' +
                    ti +
                    "_" +
                    ri +
                    '"><select data-f="' +
                    fid +
                    '" aria-label="' +
                    esc(t + ", " + r) +
                    '">' +
                    RACI.map(function (o) {
                      return (
                        '<option value="' +
                        o +
                        '"' +
                        ((val(fid) || "") === o ? " selected" : "") +
                        ">" +
                        (o || "–") +
                        "</option>"
                      );
                    }).join("") +
                    "</select></td>"
                  );
                })
                .join("") +
              "</tr>"
            );
          })
          .join("") +
        "</tbody></table></div>";
    } else if (it.type === "cpm") {
      h +=
        '<div class="tbl-scroll"><table class="grid-tbl cpm"><thead><tr><th>Activity</th>' +
        it.cols
          .map(function (c) {
            return "<th>" + esc(c) + "</th>";
          })
          .join("") +
        "</tr></thead><tbody>" +
        it.acts
          .map(function (a) {
            return (
              "<tr><th>" +
              esc(a) +
              "</th>" +
              it.cols
                .map(function (c, ci) {
                  return (
                    '<td data-cell="' +
                    a +
                    "_" +
                    ci +
                    '">' +
                    inp(id + "_" + a + "_" + ci, a + " " + c, "num-in cell") +
                    "</td>"
                  );
                })
                .join("") +
              "</tr>"
            );
          })
          .join("") +
        "</tbody></table></div>";
    } else if (it.type === "paths") {
      h += ta(
        id,
        "Your paths",
        "One path per line with its length, e.g. A-B-C = 12",
        true,
      );
    } else if (it.type === "self") {
      h +=
        ta(
          id,
          "Notes",
          "Draw it on paper (or describe it here), then press Check answer to compare with the model.",
          true,
        ) +
        '<div class="self-mark" hidden><span>Mark yourself against the model:</span>' +
        [0, 0.5, 1]
          .map(function (f) {
            return (
              '<button class="btn" type="button" data-self="' +
              f +
              '">' +
              fmt(f * it.pts) +
              " / " +
              fmt(it.pts) +
              "</button>"
            );
          })
          .join("") +
        "</div>";
    }
    return h;
  }

  var n = 0;
  P.parts.forEach(function (part, pi) {
    var sec = document.createElement("section");
    sec.id = "part-" + (pi + 1);
    var sum = part.items.reduce(function (a, it) {
      return a + it.pts;
    }, 0);
    sec.innerHTML =
      '<div class="section-head"><h2>' +
      esc(part.title) +
      "</h2><span>" +
      fmt(sum) +
      " marks</span></div>" +
      (part.intro ? '<div class="card case">' + part.intro + "</div>" : "") +
      '<div class="qlist"></div>';
    root.appendChild(sec);
    var list = sec.querySelector(".qlist");
    part.items.forEach(function (it, k) {
      var id = "p" + pi + "q" + k;
      var label = it.n || String(++n);
      var el = document.createElement("article");
      el.className = "q";
      el.id = id;
      el.innerHTML =
        '<div class="q-top"><span class="pts" data-pts>' +
        fmt(it.pts) +
        (it.pts === 1 ? " mark" : " marks") +
        "</span></div>" +
        '<p class="q-text"><span class="num">' +
        esc(label) +
        ".</span>" +
        (it.html ? it.q : esc(it.q)) +
        "</p>" +
        (it.extra || "") +
        body(it, id) +
        '<div class="q-actions"><button class="btn primary" type="button" data-check>Check answer</button></div><div class="feedback" hidden></div>';
      list.appendChild(el);
      all.push({ it: it, id: id, el: el, part: pi });
    });
  });

  function capture(item) {
    item.el.querySelectorAll("[data-f]").forEach(function (f) {
      if (f.type === "radio") {
        if (f.checked) state.v[f.getAttribute("data-f")] = f.value;
      } else state.v[f.getAttribute("data-f")] = f.value;
    });
    var w = item.el.querySelector("[data-words]");
    if (w) w.textContent = words(state.v[item.id]) + " words";
    save();
    progress();
  }
  all.forEach(function (item) {
    item.el.addEventListener("input", function () {
      capture(item);
    });
    item.el.addEventListener("change", function () {
      capture(item);
    });
    var w = item.el.querySelector("[data-words]");
    if (w) w.textContent = words(state.v[item.id]) + " words";
    item.el
      .querySelector("[data-check]")
      .addEventListener("click", function () {
        capture(item);
        state.checked[item.id] = true;
        grade(item);
        save();
        progress();
      });
    item.el.querySelectorAll("[data-self]").forEach(function (b) {
      b.addEventListener("click", function () {
        state.self[item.id] = parseFloat(b.getAttribute("data-self"));
        state.checked[item.id] = true;
        grade(item);
        save();
        progress();
        if (state.graded) results();
      });
    });
  });

  function answered(item) {
    var it = item.it,
      id = item.id;
    if (it.type === "self") return state.self[id] != null;
    var keys = Object.keys(state.v).filter(function (k) {
      return k === id || k.indexOf(id + "_") === 0;
    });
    return keys.some(function (k) {
      return k !== id + "_work" && String(state.v[k] || "").trim() !== "";
    });
  }
  function progress() {
    if (state.graded) return;
    var done = all.filter(answered).length;
    var ck = all.filter(function (it) {
      return state.checked[it.id] && it.pts != null;
    });
    var got = ck.reduce(function (a, it) {
        return a + it.pts;
      }, 0),
      mx = ck.reduce(function (a, it) {
        return a + it.it.pts;
      }, 0);
    document.getElementById("progress").textContent =
      done +
      " of " +
      all.length +
      " answered" +
      (ck.length
        ? " · " +
          ck.length +
          " checked: " +
          fmt(got) +
          " / " +
          fmt(mx) +
          " marks so far"
        : "") +
      ". Answers are saved in this browser.";
  }

  function pill(frac) {
    var cls = frac >= 0.999 ? "ok" : frac > 0 ? "part" : "no";
    var txt =
      frac >= 0.999 ? "Correct" : frac > 0 ? "Partially correct" : "Incorrect";
    return '<span class="verdict-pill ' + cls + '">' + txt + "</span>";
  }
  function keyGrade(text, groups, pts) {
    var tk = tokensOf(text || ""),
      wc = words(text);
    var gh = groups.map(function (g) {
      return anyHit(tk, g[1]);
    });
    var wsum = 0,
      whit = 0;
    groups.forEach(function (g, k) {
      var w = g[2] || 1;
      wsum += w;
      if (gh[k]) whit += w;
    });
    var got = Math.floor((whit / wsum) * pts * 4 + 1e-9) / 4;
    var brief = wc > 0 && wc < 12;
    if (brief) got = Math.min(got, q4(pts / 3));
    return {
      pts: got,
      wc: wc,
      brief: brief,
      miss: groups
        .filter(function (g, k) {
          return !gh[k];
        })
        .map(function (g) {
          return g[0];
        }),
    };
  }
  function missHtml(r) {
    return (
      (r.wc === 0
        ? "<b>Not answered.</b>"
        : r.brief
          ? "<b>Too brief (" +
            r.wc +
            " words).</b> Name the concept and explain how and why. Capped at a third of the marks."
          : "") +
      (r.miss.length
        ? "<div style='margin-top:6px'><b>Missing:</b></div><ul class='missing'>" +
          r.miss
            .map(function (m) {
              return "<li>" + esc(m) + "</li>";
            })
            .join("") +
          "</ul>"
        : "<div>All expected points are covered.</div>")
    );
  }
  function model(m) {
    return m ? "<div class='model'><b>Model answer:</b> " + m + "</div>" : "";
  }

  function grade(item) {
    var it = item.it,
      id = item.id,
      v = state.v[id],
      pts = 0,
      fb = "";
    if (it.type === "mcq") {
      var c = String(it.a);
      item.el.querySelectorAll(".opt").forEach(function (o) {
        var x = o.getAttribute("data-o");
        o.classList.toggle("right", x === c);
        o.classList.toggle("wrong", x === v && v !== c);
      });
      pts = v === c ? it.pts : 0;
      fb =
        (v == null
          ? "<b>Not answered.</b> "
          : pts
            ? ""
            : "<b>Your answer is wrong.</b> ") +
        "Correct answer: <b>" +
        LETTERS[it.a] +
        ". " +
        esc(it.opts[it.a]) +
        "</b>" +
        (it.why ? "<div class='why'>" + esc(it.why) + "</div>" : "");
    } else if (it.type === "short") {
      var r = keyGrade(v, it.groups, it.pts);
      pts = r.pts;
      fb = missHtml(r) + model(it.model);
    } else if (it.type === "rows") {
      var per = it.pts / it.rows.length;
      fb = it.rows
        .map(function (row, k) {
          var rr = keyGrade(state.v[id + "_" + k], row.groups, per);
          pts += rr.pts;
          return (
            "<div class='row-fb'><b>" +
            esc(row.label) +
            "</b> · " +
            fmt(rr.pts) +
            " / " +
            fmt(per) +
            missHtml(rr) +
            model(row.model) +
            "</div>"
          );
        })
        .join("");
      pts = q4(pts);
    } else if (it.type === "num") {
      var each = it.pts / it.fields.length,
        rows = [];
      it.fields.forEach(function (f, k) {
        var x = numOf(state.v[id + "_" + k]);
        var ok =
          x != null &&
          Math.abs(x - f.a) <=
            (f.tol != null ? f.tol : Math.max(0.05, Math.abs(f.a) * 0.02));
        if (ok) pts += each;
        var lab = item.el.querySelector('.num-field[data-k="' + k + '"]');
        lab.classList.toggle("right", ok);
        lab.classList.toggle("wrong", !ok);
        rows.push(
          "<li class='" +
            (ok ? "hit" : "miss") +
            "'>" +
            (ok ? "✓ " : "✗ ") +
            esc(f.label) +
            ": <b>" +
            esc(f.show || fmt(f.a)) +
            "</b>" +
            (f.unit ? " " + esc(f.unit) : "") +
            (x != null && !ok ? " (you wrote " + fmt(x) + ")" : "") +
            "</li>",
        );
      });
      pts = q4(pts);
      fb = "<ul class='kwlist'>" + rows.join("") + "</ul>" + model(it.model);
    } else if (it.type === "raci") {
      var cells = 0,
        ok = 0;
      it.graded.forEach(function (ti) {
        it.roles.forEach(function (r, ri) {
          var want = it.key[ti][ri],
            got = state.v[id + "_" + ti + "_" + ri] || "";
          var hit =
            got === want ||
            (want === "A" && got === "A/R") ||
            (want === "R" && got === "A/R" && it.key[ti].indexOf("A") < 0);
          cells++;
          if (hit) ok++;
          var td = item.el.querySelector('[data-cell="' + ti + "_" + ri + '"]');
          td.classList.toggle("right", hit);
          td.classList.toggle("wrong", !hit);
          td.setAttribute("data-key", want);
        });
      });
      pts = Math.floor((ok / cells) * it.pts * 4) / 4;
      fb =
        ok +
        " of " +
        cells +
        " cells match the key. Each wrong cell now shows the key's letter." +
        model(it.model);
    } else if (it.type === "cpm") {
      var tot = 0,
        good = 0;
      it.acts.forEach(function (a) {
        it.cols.forEach(function (c, ci) {
          var x = numOf(state.v[id + "_" + a + "_" + ci]),
            want = it.key[a][ci],
            hit = x === want;
          tot++;
          if (hit) good++;
          var td = item.el.querySelector('[data-cell="' + a + "_" + ci + '"]');
          td.classList.toggle("right", hit);
          td.classList.toggle("wrong", !hit);
          td.setAttribute("data-key", want);
        });
      });
      pts = Math.floor((good / tot) * it.pts * 4) / 4;
      fb =
        good +
        " of " +
        tot +
        " cells correct. Each wrong cell now shows the right value." +
        model(it.model);
    } else if (it.type === "paths") {
      var lines = String(v || "")
        .toUpperCase()
        .split(/\n|;/);
      var found = it.paths.map(function (p) {
        var best = 0;
        lines.forEach(function (ln) {
          var letters = (ln.match(/\b[A-Z]\b/g) || []).join("");
          if (letters === p[0])
            best = Math.max(
              best,
              (ln.replace(/\b[A-Z]\b/g, "").match(/\d+/g) || [])
                .map(Number)
                .indexOf(p[1]) >= 0
                ? 1
                : 0.5,
            );
        });
        return best;
      });
      pts =
        Math.floor(
          (found.reduce(function (a, b) {
            return a + b;
          }, 0) /
            it.paths.length) *
            it.pts *
            4,
        ) / 4;
      fb =
        "<ul class='kwlist'>" +
        it.paths
          .map(function (p, k) {
            return (
              "<li class='" +
              (found[k] === 1 ? "hit" : "miss") +
              "'>" +
              (found[k] === 1 ? "✓ " : found[k] ? "½ " : "✗ ") +
              esc(p[0].split("").join(" → ")) +
              " = <b>" +
              p[1] +
              "</b>" +
              (found[k] === 0.5
                ? " (path found, length missing or wrong)"
                : "") +
              "</li>"
            );
          })
          .join("") +
        "</ul>" +
        model(it.model);
    } else if (it.type === "self") {
      item.el.querySelector(".self-mark").hidden = false;
      var s = state.self[id];
      pts = s == null ? 0 : q4(s * it.pts);
      fb =
        (s == null
          ? "<b>Compare your drawing with the model, then mark yourself above.</b>"
          : "You marked this " + fmt(pts) + " / " + fmt(it.pts) + ".") +
        model(it.model);
    }
    item.pts = pts;
    item.el.classList.remove("ok", "part-ok", "no");
    item.el.classList.add(pts >= it.pts ? "ok" : pts > 0 ? "part-ok" : "no");
    var top = item.el.querySelector(".q-top");
    top.querySelectorAll(".verdict-pill").forEach(function (p) {
      p.remove();
    });
    top.insertAdjacentHTML("beforeend", pill(pts / it.pts));
    item.el.querySelector("[data-pts]").textContent =
      fmt(pts) + " / " + fmt(it.pts);
    var f = item.el.querySelector(".feedback");
    f.hidden = false;
    f.innerHTML = fb;
  }

  function results() {
    var tot = 0,
      max = 0,
      review = {};
    var secs = P.parts.map(function (p) {
      return [p.title, 0, 0];
    });
    all.forEach(function (it) {
      secs[it.part][1] += it.pts;
      secs[it.part][2] += it.it.pts;
      tot += it.pts;
      max += it.it.pts;
      if (it.pts < it.it.pts && it.it.c)
        review[it.it.c] = (review[it.it.c] || 0) + (it.it.pts - it.pts);
    });
    var r = Object.keys(review).sort(function (a, b) {
      return review[b] - review[a];
    });
    var pct = Math.round((tot / max) * 100);
    document.getElementById("results").innerHTML =
      '<div class="score"><div><div class="big">' +
      fmt(tot) +
      "<small> / " +
      fmt(max) +
      '</small></div><div class="sub">' +
      pct +
      "% · " +
      (pct >= 90
        ? "exam-ready"
        : pct >= 75
          ? "close, fix the gaps below"
          : "review the topics below, then retake") +
      '</div></div><div class="bars">' +
      secs
        .map(function (s) {
          var p = s[2] ? (s[1] / s[2]) * 100 : 0;
          return (
            '<div class="bar"><div class="lbl"><span>' +
            esc(s[0]) +
            "</span><span>" +
            fmt(s[1]) +
            "/" +
            fmt(s[2]) +
            '</span></div><div class="track"><div class="fill" style="width:' +
            p.toFixed(1) +
            '%"></div></div></div>'
          );
        })
        .join("") +
      "</div></div>" +
      (r.length
        ? '<div class="card" style="margin-bottom:14px"><h4>Concepts to review most</h4><ol class="review-list">' +
          r
            .map(function (c) {
              return (
                "<li>" + esc(c) + " <span>−" + fmt(review[c]) + "</span></li>"
              );
            })
            .join("") +
          "</ol></div>"
        : '<div class="card" style="margin-bottom:14px"><h4>Nothing to review: full marks.</h4></div>');
    document.getElementById("progress").textContent =
      "Graded: " +
      fmt(tot) +
      " / " +
      fmt(max) +
      " (" +
      pct +
      "%). Scroll through for the model answers." +
      (all.some(function (it) {
        return it.it.type === "self" && state.self[it.id] == null;
      })
        ? " Drawing questions count 0 until you mark them yourself."
        : "");
  }
  function gradeAll() {
    all.forEach(capture);
    all.forEach(grade);
    results();
    document.getElementById("exam").classList.add("graded");
    state.graded = true;
    save();
  }
  document.getElementById("submit").addEventListener("click", function () {
    var blank = all.filter(function (it) {
      return !answered(it);
    }).length;
    if (
      blank &&
      !confirm(blank + " question(s) are unanswered. Submit anyway?")
    )
      return;
    gradeAll();
    document.getElementById("results").scrollIntoView({ behavior: "smooth" });
  });
  document.getElementById("reset").addEventListener("click", function () {
    if (!confirm("Clear all your answers and start the exam again?")) return;
    try {
      localStorage.removeItem(STORE);
    } catch (e) {}
    location.reload();
  });
  if (state.graded) gradeAll();
  else {
    all.forEach(function (it) {
      if (state.checked[it.id]) grade(it);
    });
    progress();
  }
})();
