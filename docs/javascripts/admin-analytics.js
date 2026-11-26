/**
 * Site analytics dashboard (/admin/analytics/). Reads the reports from
 * workers/slide-assistant/src/analytics.js, which allows only the account in
 * courseCommerce/ethics.adminUid. All labels arrive from visitors' browsers,
 * so everything is inserted with textContent, never innerHTML.
 */
(function () {
  "use strict";
  var ENDPOINT =
    "https://shoug-tech.shoug-alomran.workers.dev/v1/analytics-query";
  var SVG = "http://www.w3.org/2000/svg";
  var DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  var KIND_NAMES = {
    home: "Home page",
    "section-home": "Section home",
    "course-home": "Course home",
    "course-page": "Other course page",
    page: "Other page",
    "annotated-slides": "Annotated slides",
    "slide-breakdowns": "Slide breakdowns",
    "chapter-summaries": "Chapter summaries",
    "past-papers": "Past papers",
    "mock-exam": "Mock exam",
    exams: "Exams & quizzes",
    mindmaps: "Mind maps",
    "cheat-sheets": "Cheat sheets",
    notebooks: "Notebooks",
    "study-pack": "Study pack",
    "study-guide": "Study guide",
    flashcards: "Flashcards",
    labs: "Labs",
    assignments: "Assignments",
    "extra-resources": "Extra resources",
  };
  var VITALS = {
    LCP: {
      name: "Largest contentful paint",
      unit: "ms",
      good: 2500,
      poor: 4000,
    },
    INP: {
      name: "Interaction to next paint",
      unit: "ms",
      good: 200,
      poor: 500,
    },
    CLS: { name: "Cumulative layout shift", unit: "", good: 0.1, poor: 0.25 },
    FCP: { name: "First contentful paint", unit: "ms", good: 1800, poor: 3000 },
    TTFB: { name: "Time to first byte", unit: "ms", good: 800, poor: 1800 },
  };

  var state = {
    range: "7",
    filters: {},
    data: null,
    user: null,
    loading: false,
  };
  var $ = function (id) {
    return document.getElementById(id);
  };

  // ------------------------------------------------------------ helpers --
  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    if (attrs)
      for (var k in attrs) {
        if (k === "text") node.textContent = attrs[k];
        else if (k === "class") node.className = attrs[k];
        else if (k.slice(0, 2) === "on")
          node.addEventListener(k.slice(2), attrs[k]);
        else if (attrs[k] !== undefined && attrs[k] !== null)
          node.setAttribute(k, attrs[k]);
      }
    (children || []).forEach(function (c) {
      if (c === null || c === undefined) return;
      node.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
    });
    return node;
  }
  function svg(tag, attrs) {
    var node = document.createElementNS(SVG, tag);
    for (var k in attrs) node.setAttribute(k, attrs[k]);
    return node;
  }
  function n(v) {
    return Number(v) || 0;
  }
  var nf = new Intl.NumberFormat("en");
  function fmt(v) {
    v = n(v);
    if (Math.abs(v) >= 10000)
      return new Intl.NumberFormat("en", {
        notation: "compact",
        maximumFractionDigits: 1,
      }).format(v);
    return nf.format(Math.round(v));
  }
  function pct(v, digits) {
    return (
      (isFinite(v)
        ? (v * 100).toFixed(digits === undefined ? 0 : digits)
        : "0") + "%"
    );
  }
  function duration(seconds) {
    seconds = Math.round(n(seconds));
    if (seconds < 60) return seconds + "s";
    var m = Math.floor(seconds / 60);
    if (m < 60) return m + "m " + (seconds % 60) + "s";
    return Math.floor(m / 60) + "h " + (m % 60) + "m";
  }
  function ms(v) {
    v = n(v);
    return v >= 1000 ? (v / 1000).toFixed(2) + " s" : Math.round(v) + " ms";
  }
  function rows(name) {
    return (state.data && state.data.data && state.data.data[name]) || [];
  }
  function failed(name) {
    return state.data && state.data.errors && state.data.errors[name];
  }
  function dayLabel(yyyymmdd) {
    var s = String(Math.round(n(yyyymmdd)));
    var d = new Date(
      Date.UTC(+s.slice(0, 4), +s.slice(4, 6) - 1, +s.slice(6, 8)),
    );
    return d.toLocaleDateString("en-GB", {
      day: "numeric",
      month: "short",
      timeZone: "UTC",
    });
  }
  function pathLabel(path) {
    return path === "/" ? "/ (home)" : path;
  }
  function countryName(code) {
    try {
      return new Intl.DisplayNames(["en"], { type: "region" }).of(code) || code;
    } catch (e) {
      return code;
    }
  }
  function languageName(code) {
    try {
      return (
        new Intl.DisplayNames(["en"], { type: "language" }).of(code) +
        " (" +
        code +
        ")"
      );
    } catch (e) {
      return code;
    }
  }

  // ------------------------------------------------------------- cards --
  function card(id, title, subtitle, opts) {
    opts = opts || {};
    var body = el("div", { class: "aa-card-body" });
    var node = el(
      "section",
      {
        class:
          "aa-card" +
          (opts.wide ? " aa-wide" : "") +
          (opts.full ? " aa-full" : ""),
        id: "card-" + id,
        "aria-labelledby": "h-" + id,
      },
      [
        el("header", { class: "aa-card-head" }, [
          el("h3", { id: "h-" + id, text: title }),
          subtitle ? el("p", { text: subtitle }) : null,
        ]),
        body,
      ],
    );
    return { node: node, body: body };
  }
  function empty(body, name) {
    var err = name && failed(name);
    body.appendChild(
      el("p", {
        class: err ? "aa-empty aa-error" : "aa-empty",
        text: err
          ? "Couldn't load this report: " + err
          : "No data in this range yet.",
      }),
    );
  }

  /**
   * A ranked list rendered as a real table: label, optional extra columns,
   * the count, and a thin bar for the share. filterKey makes rows clickable
   * to scope the whole dashboard.
   */
  function barList(body, items, opts) {
    opts = opts || {};
    if (!items.length) return empty(body, opts.source);
    var max =
      Math.max.apply(
        null,
        items.map(function (i) {
          return n(i.value);
        }),
      ) || 1;
    var total =
      opts.total ||
      items.reduce(function (s, i) {
        return s + n(i.value);
      }, 0) ||
      1;
    var table = el("table", { class: "aa-bars" });
    var headRow = el("tr", null, [
      el("th", { scope: "col", text: opts.labelHead || "Name" }),
    ]);
    (opts.columns || []).forEach(function (c) {
      headRow.appendChild(
        el("th", { scope: "col", class: "num", text: c.head }),
      );
    });
    headRow.appendChild(
      el("th", { scope: "col", class: "num", text: opts.valueHead || "Views" }),
    );
    if (opts.share !== false)
      headRow.appendChild(
        el("th", { scope: "col", class: "num", text: "Share" }),
      );
    table.appendChild(el("thead", null, [headRow]));
    var tbody = el("tbody");
    items.slice(0, opts.limit || 12).forEach(function (item) {
      var label = el("span", {
        class: "aa-bar-label",
        title: item.title || item.label,
        text: item.label,
      });
      var cell;
      if (opts.filterKey && item.filter !== undefined && item.filter !== "") {
        cell = el(
          "button",
          {
            type: "button",
            class: "aa-link",
            title: "Show only " + item.label,
            onclick: function () {
              setFilter(opts.filterKey, item.filter);
            },
          },
          [label],
        );
      } else cell = label;
      var bar = el("span", {
        class: "aa-bar",
        style:
          "width:" +
          Math.max(1.5, (n(item.value) / max) * 100).toFixed(1) +
          "%",
      });
      var tr = el("tr", null, [
        el("td", { class: "aa-bar-cell" }, [
          bar,
          cell,
          item.sub ? el("small", { text: item.sub }) : null,
        ]),
      ]);
      (opts.columns || []).forEach(function (c) {
        tr.appendChild(el("td", { class: "num", text: c.format(item) }));
      });
      tr.appendChild(
        el("td", {
          class: "num strong",
          text: (opts.format || fmt)(item.value),
        }),
      );
      if (opts.share !== false)
        tr.appendChild(
          el("td", { class: "num dim", text: pct(n(item.value) / total) }),
        );
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    body.appendChild(el("div", { class: "aa-table-wrap" }, [table]));
    if (items.length > (opts.limit || 12)) {
      var more = el("button", {
        type: "button",
        class: "aa-more",
        text: "Show all " + items.length,
      });
      more.addEventListener("click", function () {
        body.textContent = "";
        barList(body, items, Object.assign({}, opts, { limit: items.length }));
      });
      body.appendChild(more);
    }
  }

  function simple(name, mapLabel, opts) {
    return rows(name).map(function (r) {
      var key = r.k === undefined ? "" : String(r.k);
      return Object.assign(
        {
          label: mapLabel ? mapLabel(key, r) : key || "(none)",
          value: n(r.n),
          filter: key,
        },
        opts && opts.extra ? opts.extra(r) : {},
      );
    });
  }

  // ------------------------------------------------------------- tiles --
  function tile(label, value, previous, opts) {
    opts = opts || {};
    var delta = null;
    if (previous !== undefined && previous !== null && isFinite(previous)) {
      var cur = opts.raw !== undefined ? opts.raw : value;
      if (previous === 0) delta = cur > 0 ? { text: "new", dir: 0 } : null;
      else {
        var change = (cur - previous) / Math.abs(previous);
        if (opts.points) change = cur - previous;
        var dir = Math.abs(change) < 0.005 ? 0 : change > 0 ? 1 : -1;
        var good = opts.lowerIsBetter ? dir < 0 : dir > 0;
        delta = {
          text:
            (dir > 0 ? "▲ " : dir < 0 ? "▼ " : "") +
            (opts.points
              ? (Math.abs(change) * 100).toFixed(1) + " pts"
              : pct(Math.abs(change))),
          dir: dir,
          good: dir === 0 ? null : good,
        };
      }
    }
    return el("div", { class: "aa-tile" }, [
      el("span", { class: "aa-tile-label", text: label }),
      el("strong", {
        class: "aa-tile-value",
        text: opts.display || fmt(value),
      }),
      delta
        ? el("span", {
            class:
              "aa-delta" +
              (delta.good === true
                ? " up"
                : delta.good === false
                  ? " down"
                  : ""),
            title:
              "Compared with the previous " +
              state.data.days +
              " day" +
              (state.data.days > 1 ? "s" : ""),
            text: delta.text + " vs previous",
          })
        : el("span", { class: "aa-delta", text: opts.note || "" }),
    ]);
  }

  function derive(t) {
    t = t || {};
    var pv = n(t.pageviews);
    var sessions = n(t.sessions);
    return {
      pageviews: pv,
      visitors: n(t.visitors),
      sessions: sessions,
      perSession: sessions ? pv / sessions : 0,
      bounce: sessions ? 1 - n(t.sessions_2plus) / sessions : 0,
      engaged: pv ? n(t.engaged_seconds) / pv : 0,
      scroll: n(t.scroll_n) ? n(t.scroll_sum) / n(t.scroll_n) / 100 : 0,
      newShare: n(t.visitors) ? n(t.new_visitors) / n(t.visitors) : 0,
      searches: n(t.searches),
      accuracy: n(t.quiz_answered) ? n(t.quiz_correct) / n(t.quiz_answered) : 0,
      answered: n(t.quiz_answered),
      errors: n(t.errors),
      notFound: n(t.not_found),
    };
  }

  function renderTiles() {
    var box = $("aa-tiles");
    box.textContent = "";
    var cur = derive(rows("totals")[0]);
    var prevRow = rows("previous")[0];
    var prev = prevRow ? derive(prevRow) : {};
    var has = !!prevRow;
    function p(key) {
      return has ? prev[key] : null;
    }
    [
      tile("Visitors", cur.visitors, p("visitors"), { note: "unique per day" }),
      tile("Page views", cur.pageviews, p("pageviews")),
      tile("Visits", cur.sessions, p("sessions"), {
        note: "30-minute sessions",
      }),
      tile("Pages per visit", cur.perSession, p("perSession"), {
        display: cur.perSession.toFixed(2),
      }),
      tile("Bounce rate", cur.bounce, p("bounce"), {
        display: pct(cur.bounce, 1),
        lowerIsBetter: true,
        points: true,
      }),
      tile("Engaged time per page", cur.engaged, p("engaged"), {
        display: duration(cur.engaged),
      }),
      tile("Average scroll depth", cur.scroll, p("scroll"), {
        display: pct(cur.scroll),
        points: true,
      }),
      tile("First-time visitors", cur.newShare, p("newShare"), {
        display: pct(cur.newShare),
        points: true,
      }),
      tile("Searches", cur.searches, p("searches")),
      tile("Quiz accuracy", cur.accuracy, p("accuracy"), {
        display: cur.answered ? pct(cur.accuracy, 1) : "–",
        points: true,
        note: fmt(cur.answered) + " answers",
      }),
      tile("JavaScript errors", cur.errors, p("errors"), {
        lowerIsBetter: true,
      }),
      tile("Page-not-found hits", cur.notFound, p("notFound"), {
        lowerIsBetter: true,
      }),
    ].forEach(function (t) {
      box.appendChild(t);
    });
  }

  // --------------------------------------------------------- line chart --
  var SERIES = [
    { key: "pageviews", name: "Page views", cls: "s1" },
    { key: "visitors", name: "Visitors", cls: "s2" },
    { key: "sessions", name: "Visits", cls: "s3" },
  ];

  function renderTrend(body) {
    var data = rows("series").map(function (r) {
      return {
        day: n(r.day),
        pageviews: n(r.pageviews),
        visitors: n(r.visitors),
        sessions: n(r.sessions),
      };
    });
    // Fill missing days with zeros so gaps read as quiet days, not as lines across them.
    if (data.length) {
      var filled = [];
      var byDay = {};
      data.forEach(function (d) {
        byDay[d.day] = d;
      });
      var start = new Date(
        Date.now() + 3 * 3600000 - (state.data.days - 1) * 86400000,
      );
      for (var i = 0; i < state.data.days; i++) {
        var d = new Date(start.getTime() + i * 86400000);
        var key =
          d.getUTCFullYear() * 10000 +
          (d.getUTCMonth() + 1) * 100 +
          d.getUTCDate();
        filled.push(
          byDay[key] || { day: key, pageviews: 0, visitors: 0, sessions: 0 },
        );
      }
      data = filled;
    }
    if (
      !data.length ||
      !data.some(function (d) {
        return d.pageviews;
      })
    )
      return empty(body, "series");

    var legend = el("div", { class: "aa-legend", role: "list" });
    SERIES.forEach(function (s) {
      legend.appendChild(
        el("span", { class: "aa-legend-item", role: "listitem" }, [
          el("i", { class: "aa-key-line " + s.cls }),
          s.name,
        ]),
      );
    });
    body.appendChild(legend);

    // Draw at the card's real width so text stays at its intended size.
    var W = Math.max(300, Math.round(body.clientWidth || 760)),
      H = 280,
      L = 44,
      R = W < 560 ? 96 : 120,
      T = 12,
      B = 28;
    var max =
      Math.max.apply(
        null,
        data.map(function (d) {
          return d.pageviews;
        }),
      ) || 1;
    var step = Math.pow(10, Math.floor(Math.log10(max)));
    var top = Math.ceil(max / step) * step;
    if (top / step <= 2) step /= 2;
    var x = function (i) {
      return (
        L +
        (data.length === 1
          ? (W - L - R) / 2
          : (i / (data.length - 1)) * (W - L - R))
      );
    };
    var y = function (v) {
      return T + (1 - v / top) * (H - T - B);
    };

    var chart = svg("svg", {
      viewBox: "0 0 " + W + " " + H,
      class: "aa-line",
      role: "img",
      "aria-label": "Daily page views, visitors and visits",
    });
    for (var g = 0; g <= top + 1e-9; g += step) {
      chart.appendChild(
        svg("line", {
          x1: L,
          x2: W - R,
          y1: y(g),
          y2: y(g),
          class: g === 0 ? "aa-axis" : "aa-gridline",
        }),
      );
      var tl = svg("text", {
        x: L - 8,
        y: y(g) + 4,
        class: "aa-tick",
        "text-anchor": "end",
      });
      tl.textContent = fmt(g);
      chart.appendChild(tl);
    }
    var every = Math.max(
      1,
      Math.ceil(data.length / Math.max(3, Math.floor((W - L - R) / 90))),
    );
    var lastIndex = data.length - 1;
    data.forEach(function (d, i) {
      // Every nth day plus the last one, dropping a regular tick that would crowd it.
      if (i !== lastIndex && (i % every || lastIndex - i < every * 0.75))
        return;
      var t = svg("text", {
        x: x(i),
        y: H - 8,
        class: "aa-tick",
        "text-anchor": "middle",
      });
      t.textContent = dayLabel(d.day);
      chart.appendChild(t);
    });

    // End labels, nudged apart when values sit close together.
    var ends = SERIES.map(function (s) {
      return { s: s, y: y(data[data.length - 1][s.key]) };
    }).sort(function (a, b) {
      return a.y - b.y;
    });
    for (var e = 1; e < ends.length; e++)
      if (ends[e].y - ends[e - 1].y < 14) ends[e].y = ends[e - 1].y + 14;

    SERIES.forEach(function (s) {
      var dpath = data
        .map(function (d, i) {
          return (
            (i ? "L" : "M") + x(i).toFixed(1) + " " + y(d[s.key]).toFixed(1)
          );
        })
        .join(" ");
      chart.appendChild(svg("path", { d: dpath, class: "aa-series " + s.cls }));
      var last = data[data.length - 1];
      chart.appendChild(
        svg("circle", {
          cx: x(data.length - 1),
          cy: y(last[s.key]),
          r: 4,
          class: "aa-dot " + s.cls,
        }),
      );
    });
    ends.forEach(function (end) {
      var label = svg("text", { x: W - R + 10, y: end.y + 4, class: "aa-end" });
      label.textContent =
        end.s.name + " " + fmt(data[data.length - 1][end.s.key]);
      chart.appendChild(label);
    });

    var hair = svg("line", {
      y1: T,
      y2: H - B,
      class: "aa-hair",
      visibility: "hidden",
    });
    chart.appendChild(hair);
    var tip = el("div", { class: "aa-tip", hidden: "" });
    var wrap = el("div", { class: "aa-chart" }, [chart, tip]);
    function show(i) {
      var d = data[i];
      hair.setAttribute("x1", x(i));
      hair.setAttribute("x2", x(i));
      hair.setAttribute("visibility", "visible");
      tip.textContent = "";
      tip.appendChild(
        el("div", { class: "aa-tip-title", text: dayLabel(d.day) }),
      );
      SERIES.forEach(function (s) {
        tip.appendChild(
          el("div", { class: "aa-tip-row" }, [
            el("i", { class: "aa-key-line " + s.cls }),
            el("strong", { text: fmt(d[s.key]) }),
            el("span", { text: s.name }),
          ]),
        );
      });
      tip.hidden = false;
      var box = chart.getBoundingClientRect();
      var px = (x(i) / W) * box.width;
      tip.style.left = Math.min(box.width - 170, Math.max(0, px + 12)) + "px";
    }
    function hide() {
      hair.setAttribute("visibility", "hidden");
      tip.hidden = true;
    }
    chart.addEventListener("pointermove", function (ev) {
      var box = chart.getBoundingClientRect();
      var vx = ((ev.clientX - box.left) / box.width) * W;
      var i = Math.round(((vx - L) / (W - L - R)) * (data.length - 1));
      show(Math.max(0, Math.min(data.length - 1, i)));
    });
    chart.addEventListener("pointerleave", hide);
    chart.setAttribute("tabindex", "0");
    var focusIndex = data.length - 1;
    chart.addEventListener("focus", function () {
      show(focusIndex);
    });
    chart.addEventListener("blur", hide);
    chart.addEventListener("keydown", function (ev) {
      if (ev.key === "ArrowLeft") focusIndex = Math.max(0, focusIndex - 1);
      else if (ev.key === "ArrowRight")
        focusIndex = Math.min(data.length - 1, focusIndex + 1);
      else return;
      ev.preventDefault();
      show(focusIndex);
    });
    body.appendChild(wrap);

    body.appendChild(
      dataTable(
        ["Day"].concat(
          SERIES.map(function (s) {
            return s.name;
          }),
        ),
        data
          .slice()
          .reverse()
          .map(function (d) {
            return [
              dayLabel(d.day),
              fmt(d.pageviews),
              fmt(d.visitors),
              fmt(d.sessions),
            ];
          }),
      ),
    );
  }

  function dataTable(head, bodyRows) {
    var t = el("table", { class: "aa-plain" });
    t.appendChild(
      el("thead", null, [
        el(
          "tr",
          null,
          head.map(function (h, i) {
            return el("th", { scope: "col", class: i ? "num" : "", text: h });
          }),
        ),
      ]),
    );
    t.appendChild(
      el(
        "tbody",
        null,
        bodyRows.map(function (r) {
          return el(
            "tr",
            null,
            r.map(function (c, i) {
              return el("td", { class: i ? "num" : "", text: c });
            }),
          );
        }),
      ),
    );
    return el("details", { class: "aa-details" }, [
      el("summary", { text: "Show as a table" }),
      el("div", { class: "aa-table-wrap" }, [t]),
    ]);
  }

  // ------------------------------------------------------------ heatmap --
  function renderHeat(body) {
    var grid = {};
    var max = 0;
    rows("heat").forEach(function (r) {
      var key = n(r.weekday) + "-" + n(r.hour);
      grid[key] = n(r.n);
      if (grid[key] > max) max = grid[key];
    });
    if (!max) return empty(body, "heat");
    var STEPS = 7;
    var table = el("table", {
      class: "aa-heat",
      "aria-label": "Page views by weekday and hour, Riyadh time",
    });
    var head = el("tr", null, [
      el("th", { scope: "col", class: "aa-heat-corner" }),
    ]);
    for (var h = 0; h < 24; h++)
      head.appendChild(
        el("th", {
          scope: "col",
          text: h % 3 === 0 ? String(h).padStart(2, "0") : "",
          "aria-label": h + ":00",
        }),
      );
    table.appendChild(el("thead", null, [head]));
    var tbody = el("tbody");
    var tip = el("div", { class: "aa-tip", hidden: "" });
    for (var d = 0; d < 7; d++) {
      var tr = el("tr", null, [el("th", { scope: "row", text: DAYS[d] })]);
      for (var hr = 0; hr < 24; hr++) {
        var v = grid[d + "-" + hr] || 0;
        var level = v
          ? Math.min(STEPS, 1 + Math.floor((v / max) * (STEPS - 1) + 0.5))
          : 0;
        var text =
          DAYS[d] +
          " " +
          String(hr).padStart(2, "0") +
          ":00 – " +
          fmt(v) +
          " page views";
        var td = el("td", {
          class: "aa-h" + level,
          tabindex: "0",
          "aria-label": text,
        });
        (function (t, cell) {
          function on() {
            tip.textContent = t;
            tip.hidden = false;
            var box = table.getBoundingClientRect();
            var c = cell.getBoundingClientRect();
            tip.style.left =
              Math.min(box.width - 220, Math.max(0, c.left - box.left - 60)) +
              "px";
            tip.style.top = c.top - box.top - 40 + "px";
          }
          cell.addEventListener("pointerenter", on);
          cell.addEventListener("focus", on);
          cell.addEventListener("pointerleave", function () {
            tip.hidden = true;
          });
          cell.addEventListener("blur", function () {
            tip.hidden = true;
          });
        })(text, td);
        tr.appendChild(td);
      }
      tbody.appendChild(tr);
    }
    table.appendChild(tbody);
    var scale = el("div", { class: "aa-heat-scale" }, [
      el("span", { text: "Fewer" }),
    ]);
    for (var s = 1; s <= STEPS; s++)
      scale.appendChild(el("i", { class: "aa-h" + s }));
    scale.appendChild(el("span", { text: "More (peak " + fmt(max) + ")" }));
    body.appendChild(
      el("div", { class: "aa-chart aa-heat-wrap" }, [table, tip]),
    );
    body.appendChild(scale);
  }

  // ------------------------------------------------------------- vitals --
  function rating(name, v) {
    var t = VITALS[name];
    return v <= t.good ? "good" : v <= t.poor ? "needs-improvement" : "poor";
  }
  var RATING_TEXT = {
    good: "✓ Good",
    "needs-improvement": "! Needs work",
    poor: "✕ Poor",
  };

  function renderVitals(body) {
    var list = rows("vitals");
    if (!list.length) return empty(body, "vitals");
    var by = {};
    list.forEach(function (r) {
      by[r.k] = r;
    });
    var grid = el("div", { class: "aa-vitals" });
    Object.keys(VITALS).forEach(function (key) {
      var r = by[key];
      if (!r) return;
      var p75 = n(r.p75);
      var rate = rating(key, p75);
      var total = n(r.good) + n(r.ni) + n(r.poor) || 1;
      var bar = el(
        "div",
        {
          class: "aa-seg",
          role: "img",
          "aria-label":
            pct(n(r.good) / total) +
            " good, " +
            pct(n(r.ni) / total) +
            " needs improvement, " +
            pct(n(r.poor) / total) +
            " poor",
        },
        [
          el("i", { class: "good", style: "flex-grow:" + n(r.good) }),
          el("i", { class: "ni", style: "flex-grow:" + n(r.ni) }),
          el("i", { class: "poor", style: "flex-grow:" + n(r.poor) }),
        ],
      );
      grid.appendChild(
        el("div", { class: "aa-vital" }, [
          el("span", {
            class: "aa-tile-label",
            text: key + " · " + VITALS[key].name,
          }),
          el("strong", {
            class: "aa-tile-value",
            text: key === "CLS" ? p75.toFixed(3) : ms(p75),
          }),
          el("span", {
            class: "aa-rating " + rate,
            text: RATING_TEXT[rate] + " at the 75th percentile",
          }),
          bar,
          el("span", {
            class: "aa-seg-legend",
            text:
              pct(n(r.good) / total) +
              " good · " +
              pct(n(r.ni) / total) +
              " needs work · " +
              pct(n(r.poor) / total) +
              " poor",
          }),
        ]),
      );
    });
    body.appendChild(grid);

    var lt = rows("loadTime")[0];
    if (lt && n(lt.p50))
      body.appendChild(
        el("p", {
          class: "aa-note",
          text:
            "Full page load: median " +
            ms(lt.p50) +
            " · 75th percentile " +
            ms(lt.p75) +
            " · 95th percentile " +
            ms(lt.p95) +
            ".",
        }),
      );

    var dev = rows("vitalsByDevice");
    if (dev.length) {
      var devices = ["desktop", "mobile", "tablet"].filter(function (d) {
        return dev.some(function (r) {
          return r.device === d;
        });
      });
      var table = dataTable(
        ["Metric (75th percentile)"].concat(devices),
        Object.keys(VITALS).map(function (key) {
          return [key].concat(
            devices.map(function (d) {
              var r = dev.filter(function (x) {
                return x.k === key && x.device === d;
              })[0];
              if (!r) return "–";
              return (
                (key === "CLS" ? n(r.p75).toFixed(3) : ms(r.p75)) +
                " (" +
                fmt(r.n) +
                ")"
              );
            }),
          );
        }),
      );
      table.querySelector("summary").textContent = "By device";
      body.appendChild(table);
    }
  }

  // ------------------------------------------------------------ filters --
  var FILTER_NAMES = {
    course: "Course",
    section: "Section",
    kind: "Content",
    country: "Country",
    device: "Device",
    path: "Page",
  };
  function setFilter(key, value) {
    state.filters[key] = value;
    load();
  }
  function renderChips() {
    var box = $("aa-chips");
    box.textContent = "";
    Object.keys(state.filters).forEach(function (key) {
      var value = state.filters[key];
      var label =
        key === "country"
          ? countryName(value)
          : key === "kind"
            ? KIND_NAMES[value] || value
            : value;
      box.appendChild(
        el(
          "button",
          {
            type: "button",
            class: "aa-chip",
            title: "Remove this filter",
            onclick: function () {
              delete state.filters[key];
              load();
            },
          },
          [FILTER_NAMES[key] + ": " + label + "  ✕"],
        ),
      );
    });
  }

  // ---------------------------------------------------------- dashboard --
  function render() {
    renderChips();
    renderTiles();
    var live = rows("live");
    var liveTotal = live.reduce(function (s, r) {
      return s + n(r.n);
    }, 0);
    $("aa-live").textContent =
      fmt(liveTotal) +
      " page view" +
      (liveTotal === 1 ? "" : "s") +
      " in the last 30 minutes";
    $("aa-updated").textContent =
      "Updated " +
      new Date(state.data.generatedAt).toLocaleTimeString("en-GB", {
        hour: "2-digit",
        minute: "2-digit",
      });

    var titles = {};
    rows("titles").forEach(function (r) {
      if (!titles[r.k]) titles[r.k] = r.title;
    });
    var engage = {};
    rows("pageEngage").forEach(function (r) {
      engage[r.k] = r;
    });

    var root = $("aa-sections");
    root.textContent = "";
    function section(id, title, intro) {
      var grid = el("div", { class: "aa-grid" });
      root.appendChild(
        el(
          "section",
          { class: "aa-section", id: "s-" + id, "aria-labelledby": "sh-" + id },
          [
            el("h2", { id: "sh-" + id, text: title }),
            intro ? el("p", { class: "aa-intro", text: intro }) : null,
            grid,
          ],
        ),
      );
      return function (c) {
        grid.appendChild(c.node);
        return c;
      };
    }

    // Traffic
    var add = section(
      "traffic",
      "Traffic",
      "Riyadh time. Visitors are counted once per browser per day.",
    );
    renderTrend(add(card("trend", "Daily traffic", null, { full: true })).body);
    renderHeat(
      add(
        card("heat", "When people visit", "Page views by weekday and hour", {
          wide: true,
        }),
      ).body,
    );
    var liveCard = add(
      card("live", "Right now", "Pages viewed in the last 30 minutes"),
    );
    barList(
      liveCard.body,
      live.map(function (r) {
        return {
          label: pathLabel(r.k),
          value: n(r.n),
          filter: r.k,
          title: titles[r.k],
        };
      }),
      { filterKey: "path", labelHead: "Page", source: "live" },
    );

    // Content
    add = section(
      "content",
      "Content",
      "Click any name to filter the whole dashboard to it.",
    );
    var pagesCard = add(
      card(
        "pages",
        "Top pages",
        "Views, daily visitors, engaged time and scroll depth",
        { full: true },
      ),
    );
    barList(
      pagesCard.body,
      rows("pages").map(function (r) {
        var e = engage[r.k] || {};
        return {
          label: titles[r.k] ? titles[r.k] : pathLabel(r.k),
          sub: titles[r.k] ? r.k : "",
          value: n(r.n),
          visitors: n(r.visitors),
          seconds: n(r.n) ? n(e.seconds) / n(r.n) : 0,
          scroll: n(e.scroll_n) ? n(e.scroll_sum) / n(e.scroll_n) : null,
          filter: r.k,
          title: r.k,
        };
      }),
      {
        filterKey: "path",
        labelHead: "Page",
        limit: 15,
        source: "pages",
        columns: [
          {
            head: "Visitors",
            format: function (i) {
              return fmt(i.visitors);
            },
          },
          {
            head: "Time / view",
            format: function (i) {
              return duration(i.seconds);
            },
          },
          {
            head: "Scroll",
            format: function (i) {
              return i.scroll === null ? "–" : Math.round(i.scroll) + "%";
            },
          },
        ],
      },
    );
    barList(
      add(card("entries", "Landing pages", "First page of each visit")).body,
      simple("entries", pathLabel),
      {
        filterKey: "path",
        labelHead: "Page",
        valueHead: "Visits",
        source: "entries",
      },
    );
    barList(
      add(card("courses", "Courses")).body,
      rows("courses").map(function (r) {
        return {
          label: String(r.k).toUpperCase(),
          value: n(r.n),
          sub: fmt(r.visitors) + " visitors",
          filter: r.k,
        };
      }),
      {
        filterKey: "course",
        labelHead: "Course",
        source: "courses",
        limit: 15,
      },
    );
    barList(
      add(card("kinds", "Study material types")).body,
      simple("kinds", function (k) {
        return KIND_NAMES[k] || k;
      }),
      { filterKey: "kind", labelHead: "Type", source: "kinds" },
    );
    barList(add(card("sections", "Site sections")).body, simple("sections"), {
      filterKey: "section",
      labelHead: "Section",
      source: "sections",
    });
    barList(
      add(
        card(
          "flows",
          "Page to page",
          "Most common next clicks inside the site",
          { wide: true },
        ),
      ).body,
      rows("flows").map(function (r) {
        return {
          label: pathLabel(r.source) + "  →  " + pathLabel(r.target),
          value: n(r.n),
        };
      }),
      {
        labelHead: "From → to",
        valueHead: "Times",
        source: "flows",
        share: false,
      },
    );

    // Acquisition
    add = section("acquisition", "Where visitors come from");
    barList(
      add(
        card(
          "referrers",
          "Referring sites",
          "Visits that arrived from another site",
        ),
      ).body,
      simple("referrers"),
      { labelHead: "Site", source: "referrers" },
    );
    barList(
      add(card("utm", "Campaign links", "utm_source (or ?ref=) on the link"))
        .body,
      rows("utm").map(function (r) {
        return { label: r.k, sub: r.rest, value: n(r.n) };
      }),
      { labelHead: "Source", source: "utm" },
    );
    barList(
      add(
        card(
          "returning",
          "Return cadence",
          "Time since the visitor's previous day on the site",
        ),
      ).body,
      simple("returning"),
      { labelHead: "Last visit", valueHead: "Visitors", source: "returning" },
    );

    // Audience
    add = section("audience", "Audience");
    barList(
      add(card("countries", "Countries")).body,
      simple("countries", countryName),
      { filterKey: "country", labelHead: "Country", source: "countries" },
    );
    barList(
      add(card("cities", "Cities")).body,
      rows("cities").map(function (r) {
        return { label: r.k, sub: countryName(r.country), value: n(r.n) };
      }),
      { labelHead: "City", source: "cities" },
    );
    barList(
      add(card("devices", "Devices")).body,
      simple("devices", function (k) {
        return k.charAt(0).toUpperCase() + k.slice(1);
      }),
      { filterKey: "device", labelHead: "Device", source: "devices" },
    );
    barList(add(card("browsers", "Browsers")).body, simple("browsers"), {
      labelHead: "Browser",
      source: "browsers",
    });
    barList(add(card("os", "Operating systems")).body, simple("os"), {
      labelHead: "System",
      source: "os",
    });
    barList(add(card("viewports", "Screen widths")).body, simple("viewports"), {
      labelHead: "Width",
      source: "viewports",
    });
    barList(
      add(card("languages", "Browser languages")).body,
      simple("languages", languageName),
      { labelHead: "Language", source: "languages" },
    );
    barList(
      add(card("siteLanguage", "Site language chosen")).body,
      simple("siteLanguage", function (k) {
        return k === "ar"
          ? "Arabic"
          : k === "en"
            ? "English"
            : k || "(unknown)";
      }),
      { labelHead: "Language", source: "siteLanguage" },
    );
    barList(add(card("themes", "Theme & palette")).body, simple("themes"), {
      labelHead: "Theme / palette",
      source: "themes",
    });
    barList(
      add(card("signedIn", "Signed in")).body,
      simple("signedIn", function (k) {
        return k === "1" ? "Signed in" : "Not signed in";
      }),
      { labelHead: "State", source: "signedIn" },
    );
    barList(
      add(card("pwa", "Installed app & offline")).body,
      simple("pwa", function (k) {
        return k === "standalone"
          ? "Opened as installed app"
          : "Offline page shown";
      }),
      { labelHead: "Mode", source: "pwa", share: false },
    );

    // Study tools
    add = section("study", "Study tools");
    var quizzes = rows("quizzes").map(function (r) {
      var answered = n(r.answered);
      return {
        label: titles[r.k] || pathLabel(r.k),
        sub: titles[r.k] ? r.k : "",
        value: answered,
        correct: n(r.correct),
        filter: r.k,
      };
    });
    barList(
      add(
        card(
          "quizzes",
          "Quizzes",
          "Questions answered and the share answered correctly on the first try",
          { full: true },
        ),
      ).body,
      quizzes,
      {
        filterKey: "path",
        labelHead: "Quiz",
        valueHead: "Answers",
        source: "quizzes",
        columns: [
          {
            head: "Correct",
            format: function (i) {
              return i.value ? pct(i.correct / i.value) : "–";
            },
          },
        ],
      },
    );
    barList(
      add(
        card(
          "quizSubmits",
          "Quiz submissions",
          "Check / submit / grade clicks, with the running score",
        ),
      ).body,
      rows("quizSubmits").map(function (r) {
        return {
          label: titles[r.k] || pathLabel(r.k),
          value: n(r.n),
          score: n(r.avg_score),
          filter: r.k,
        };
      }),
      {
        filterKey: "path",
        labelHead: "Quiz",
        valueHead: "Submits",
        source: "quizSubmits",
        share: false,
        columns: [
          {
            head: "Avg score",
            format: function (i) {
              return Math.round(i.score) + "%";
            },
          },
        ],
      },
    );
    barList(
      add(card("searches", "Searches")).body,
      rows("searches").map(function (r) {
        return { label: r.k, value: n(r.n), results: n(r.results) };
      }),
      {
        labelHead: "Query",
        valueHead: "Times",
        source: "searches",
        columns: [
          {
            head: "Results",
            format: function (i) {
              return Math.round(i.results);
            },
          },
        ],
      },
    );
    barList(
      add(
        card(
          "zeroSearches",
          "Searches with no results",
          "Content people looked for and didn't find",
        ),
      ).body,
      simple("zeroSearches"),
      { labelHead: "Query", valueHead: "Times", source: "zeroSearches" },
    );
    barList(
      add(card("buttons", "Buttons & tools used", null, { wide: true })).body,
      rows("buttons").map(function (r) {
        return { label: r.k, sub: KIND_NAMES[r.kind] || r.kind, value: n(r.n) };
      }),
      {
        labelHead: "Button",
        valueHead: "Clicks",
        source: "buttons",
        limit: 15,
      },
    );
    barList(add(card("downloads", "Downloads")).body, simple("downloads"), {
      labelHead: "File",
      valueHead: "Clicks",
      source: "downloads",
    });
    barList(add(card("outbound", "Links out")).body, simple("outbound"), {
      labelHead: "Destination",
      valueHead: "Clicks",
      source: "outbound",
    });
    barList(
      add(card("contact", "Email & phone links")).body,
      simple("contact"),
      { labelHead: "Link", valueHead: "Clicks", source: "contact" },
    );
    barList(
      add(card("copies", "Most copied from")).body,
      simple("copies", pathLabel),
      {
        filterKey: "path",
        labelHead: "Page",
        valueHead: "Copies",
        source: "copies",
      },
    );
    barList(
      add(card("prints", "Most printed")).body,
      simple("prints", pathLabel),
      {
        filterKey: "path",
        labelHead: "Page",
        valueHead: "Prints",
        source: "prints",
      },
    );
    barList(
      add(card("prefs", "Settings changed")).body,
      rows("prefs").map(function (r) {
        return { label: r.k + " → " + r.value, value: n(r.n) };
      }),
      { labelHead: "Change", valueHead: "Times", source: "prefs" },
    );

    // Quality
    add = section("quality", "Speed & problems");
    renderVitals(
      add(
        card(
          "vitals",
          "Core Web Vitals",
          "Real visitors, 75th percentile (Google's pass mark)",
          { full: true },
        ),
      ).body,
    );
    barList(
      add(
        card(
          "slowPages",
          "Slowest pages",
          "Largest contentful paint, 75th percentile (3+ views)",
        ),
      ).body,
      rows("slowPages").map(function (r) {
        return {
          label: pathLabel(r.k),
          value: n(r.p75),
          views: n(r.n),
          filter: r.k,
        };
      }),
      {
        filterKey: "path",
        labelHead: "Page",
        valueHead: "LCP",
        format: ms,
        share: false,
        source: "slowPages",
        columns: [
          {
            head: "Samples",
            format: function (i) {
              return fmt(i.views);
            },
          },
        ],
      },
    );
    barList(
      add(
        card(
          "notFound",
          "Broken links (404)",
          "Missing pages, with the page that linked to them",
        ),
      ).body,
      rows("notFound").map(function (r) {
        return {
          label: r.k,
          sub: r.source ? "linked from " + r.source : "direct or external",
          value: n(r.n),
        };
      }),
      { labelHead: "Missing page", valueHead: "Hits", source: "notFound" },
    );
    barList(
      add(card("errors", "JavaScript errors", null, { wide: true })).body,
      rows("errors").map(function (r) {
        return { label: r.k, sub: r.source, value: n(r.n) };
      }),
      { labelHead: "Error", valueHead: "Times", source: "errors" },
    );
    barList(
      add(card("errorPages", "Pages with errors")).body,
      simple("errorPages", pathLabel),
      {
        filterKey: "path",
        labelHead: "Page",
        valueHead: "Errors",
        source: "errorPages",
      },
    );
    barList(
      add(
        card(
          "rage",
          "Frustrated clicks",
          "Three clicks on the same thing within a second",
        ),
      ).body,
      rows("rage").map(function (r) {
        return { label: r.k, sub: r.path, value: n(r.n) };
      }),
      { labelHead: "Element", valueHead: "Times", source: "rage" },
    );
  }

  // --------------------------------------------------------------- load --
  function status(text, isError) {
    var s = $("aa-status");
    s.textContent = text;
    s.classList.toggle("is-error", !!isError);
    s.hidden = !text;
  }

  function load() {
    if (!state.user || state.loading) return;
    state.loading = true;
    $("aa-dashboard").classList.add("is-loading");
    status(state.data ? "" : "Loading reports…");
    state.user
      .getIdToken()
      .then(function (token) {
        return fetch(ENDPOINT, {
          method: "POST",
          headers: {
            "content-type": "application/json",
            authorization: "Bearer " + token,
          },
          body: JSON.stringify({ range: state.range, filters: state.filters }),
        });
      })
      .then(function (res) {
        return res.json().then(function (body) {
          if (res.status === 404)
            throw new Error(
              "The analytics service isn't live yet. Deploy the updated worker: cd workers/slide-assistant && npx wrangler deploy",
            );
          if (!res.ok)
            throw new Error(
              body.error || "Request failed (" + res.status + ")",
            );
          return body;
        });
      })
      .then(function (body) {
        state.data = body;
        state.filters = body.filters || {};
        $("aa-dashboard").hidden = false;
        status("");
        render();
        var failures = Object.keys(body.errors || {});
        if (
          failures.length ===
            Object.keys(body.data || {}).length + failures.length &&
          failures.length
        )
          status(
            "Every report failed. First error: " + body.errors[failures[0]],
            true,
          );
      })
      .catch(function (err) {
        status(err.message || String(err), true);
      })
      .then(function () {
        state.loading = false;
        $("aa-dashboard").classList.remove("is-loading");
      });
  }

  function download() {
    if (!state.data) return;
    var blob = new Blob([JSON.stringify(state.data, null, 2)], {
      type: "application/json",
    });
    var a = el("a", {
      href: URL.createObjectURL(blob),
      download:
        "shoug-tech-analytics-" +
        state.range +
        "d-" +
        new Date().toISOString().slice(0, 10) +
        ".json",
    });
    document.body.appendChild(a);
    a.click();
    setTimeout(function () {
      URL.revokeObjectURL(a.href);
      a.remove();
    }, 0);
  }

  function setup() {
    document.querySelectorAll("[data-range]").forEach(function (button) {
      button.addEventListener("click", function () {
        state.range = button.getAttribute("data-range");
        document.querySelectorAll("[data-range]").forEach(function (b) {
          b.setAttribute("aria-pressed", String(b === button));
        });
        load();
      });
    });
    $("aa-refresh").addEventListener("click", load);
    $("aa-download").addEventListener("click", download);
    $("aa-signin").addEventListener("click", function () {
      if (window.__shougOpenAuthModal) window.__shougOpenAuthModal();
      else status("Sign-in is still loading. Try again in a moment.");
    });
    // Live figures stay current while the tab is open.
    setInterval(function () {
      if (document.visibilityState === "visible" && state.data) load();
    }, 5 * 60000);
  }

  function boot() {
    var fb = window.__shoug_fb;
    fb.auth().onAuthStateChanged(function (user) {
      state.user = user;
      $("aa-login").hidden = !!user;
      if (!user) {
        $("aa-dashboard").hidden = true;
        status("");
        return;
      }
      load();
    });
  }

  setup();
  if (window.__shoug_fb) boot();
  else window.addEventListener("shoug:fb", boot, { once: true });
})();
