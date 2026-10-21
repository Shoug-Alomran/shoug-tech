/**
 * Calendar views for /account/calendar/ (Apple Calendar-style layer).
 *
 *  - Month / Week / Day switcher. Week and Day are time grids with an all-day
 *    strip, side-by-side overlapping events and a live current-time line.
 *  - Phones: month cells show coloured dots and the tapped day is listed
 *    under the grid, like the iPhone Calendar app.
 *  - Quick add: "SE322 quiz Tue 10am", "gym tomorrow 6-7pm".
 *  - Drag: move or resize your own events in Week/Day, drag on an empty slot
 *    to create one, and drag events between days in Month.
 *  - Search across events, keyboard shortcuts, and one colour per course.
 *
 * The calendar page owns the data and saving; it exposes what this needs on
 * window.__shougCal and calls window.__shougCalViews.render() after each
 * render, step()/goTo() for navigation and dayClick() for month cells.
 */
(function () {
  "use strict";
  if (window.__shougCalViews) return;

  var C = null,
    $ = function (id) {
      return document.getElementById(id);
    };
  var VIEW_KEY = "calendar-view",
    CC_KEY = "calendar-colour-by-course";
  var state = {
    view: "month",
    focus: "",
    phoneDay: "",
    colourByCourse: false,
    scrolledFor: "",
  };
  var DAY_NAMES = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  var HUES = [262, 205, 172, 26, 330, 48, 145, 0, 190, 290, 100, 15];
  var phoneQuery = window.matchMedia("(max-width: 600px)");

  function load(k, d) {
    try {
      var v = localStorage.getItem(k);
      return v === null ? d : v;
    } catch (e) {
      return d;
    }
  }
  function save(k, v) {
    try {
      localStorage.setItem(k, v);
    } catch (e) {}
  }
  function isPhone() {
    return phoneQuery.matches;
  }
  function modalOpen() {
    return Boolean(document.querySelector('[aria-hidden="false"].open'));
  }

  // ── Course colours ──────────────────────────────────────────────────────
  function hueFor(course) {
    // Prefer the page's collision-free map so colours match everywhere.
    if (C && C.courseHue) return C.courseHue(course);
    var h = 0,
      s = String(course || "");
    for (var i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) >>> 0;
    return HUES[h % HUES.length];
  }
  function paintCourses(root) {
    (root || document).querySelectorAll("[data-course]").forEach(function (el) {
      el.style.setProperty("--cc", hueFor(el.getAttribute("data-course")));
    });
    document.body.classList.toggle("cal-cc", state.colourByCourse);
  }

  // ── Dates ───────────────────────────────────────────────────────────────
  function weekStart(k) {
    var d = C.fromKey(k);
    return C.addDays(k, -d.getDay());
  }
  function visibleDays() {
    if (state.view === "day") return [state.focus];
    var s = weekStart(state.focus),
      out = [];
    for (var i = 0; i < 7; i++) out.push(C.addDays(s, i));
    return out;
  }
  function fmt(k, opts) {
    return C.fromKey(k).toLocaleDateString("en-US", opts);
  }
  function rangeTitle() {
    if (state.view === "day")
      return fmt(state.focus, {
        weekday: "long",
        month: "short",
        day: "numeric",
        year: "numeric",
      });
    var days = visibleDays(),
      a = C.fromKey(days[0]),
      b = C.fromKey(days[6]);
    var sameMonth = a.getMonth() === b.getMonth();
    return (
      fmt(days[0], { month: "short", day: "numeric" }) +
      " – " +
      (sameMonth
        ? b.getDate()
        : fmt(days[6], { month: "short", day: "numeric" })) +
      ", " +
      b.getFullYear()
    );
  }
  function nowMinutes() {
    var d = new Date();
    return d.getHours() * 60 + d.getMinutes();
  }

  // ── Toolbar ─────────────────────────────────────────────────────────────
  function buildToolbar() {
    var bar = $("cal-toolbar");
    if (!bar || bar.dataset.ready) return;
    bar.dataset.ready = "1";
    bar.innerHTML =
      '<div class="cv-seg" role="tablist" aria-label="Calendar view">' +
      ["month", "week", "day"]
        .map(function (v) {
          return (
            '<button type="button" role="tab" data-view="' +
            v +
            '">' +
            v.charAt(0).toUpperCase() +
            v.slice(1) +
            "</button>"
          );
        })
        .join("") +
      "</div>" +
      '<div class="cv-quick"><input id="cv-quick" type="text" autocomplete="off" placeholder="Quick add: SE322 quiz Tue 10am" aria-describedby="cv-quick-preview" /><div class="cv-quick-preview" id="cv-quick-preview" aria-live="polite"></div></div>' +
      '<div class="cv-search"><input id="cv-search" type="search" autocomplete="off" placeholder="Search events" aria-label="Search events" /><div class="cv-results" id="cv-results" role="listbox" hidden></div></div>' +
      '<button type="button" class="cv-cc" id="cv-cc" aria-pressed="false" title="Colour events by course"><span class="cv-long">Course </span>colours</button>' +
      '<button type="button" class="cv-help" id="cv-help" aria-label="Keyboard shortcuts" title="Keyboard shortcuts">?</button>';
    bar.querySelectorAll("[data-view]").forEach(function (b) {
      b.addEventListener("click", function () {
        setView(b.dataset.view);
      });
    });
    $("cv-cc").addEventListener("click", function () {
      state.colourByCourse = !state.colourByCourse;
      save(CC_KEY, state.colourByCourse ? "1" : "0");
      render();
    });
    $("cv-help").addEventListener("click", showHelp);
    setupQuickAdd();
    setupSearch();
  }
  function syncToolbar() {
    document.querySelectorAll("#cal-toolbar [data-view]").forEach(function (b) {
      var on = b.dataset.view === state.view;
      b.classList.toggle("on", on);
      b.setAttribute("aria-selected", on ? "true" : "false");
    });
    var cc = $("cv-cc");
    if (cc) {
      cc.classList.toggle("on", state.colourByCourse);
      cc.setAttribute("aria-pressed", state.colourByCourse ? "true" : "false");
    }
  }

  function setView(v) {
    if (["month", "week", "day"].indexOf(v) < 0) return;
    state.view = v;
    save(VIEW_KEY, v);
    if (v === "month") C.currentMonth = C.fromKey(state.focus);
    state.scrolledFor = "";
    C.renderAll(true);
  }

  // ── Render entry ────────────────────────────────────────────────────────
  function render() {
    if (!C) return;
    buildToolbar();
    syncToolbar();
    var month = state.view === "month",
      grid = $("month-grid"),
      weekdays = $("month-weekdays"),
      tv = $("time-view"),
      pd = $("phone-day"),
      title = $("calendar-view-title");
    if (title)
      title.textContent = month
        ? "Month"
        : state.view === "week"
          ? "Week"
          : "Day";
    if (grid) grid.hidden = !month;
    if (weekdays) weekdays.hidden = !month;
    if (tv) tv.hidden = month;
    if (month) {
      if (pd) pd.hidden = !isPhone();
      if (isPhone()) renderPhoneMonth();
      setupMonthDrag();
    } else {
      if (pd) pd.hidden = true;
      $("month-name").textContent = rangeTitle();
      renderTimeView();
    }
    paintCourses();
  }

  // ── Week / Day time grid ────────────────────────────────────────────────
  function layoutColumns(events) {
    // Greedy columns inside clusters of overlapping events.
    var sorted = events.slice().sort(function (a, b) {
      return a.s - b.s || b.e - a.e;
    });
    var clusters = [],
      cur = null;
    sorted.forEach(function (ev) {
      if (!cur || ev.s >= cur.end) {
        cur = { items: [], end: ev.e, cols: [] };
        clusters.push(cur);
      }
      cur.end = Math.max(cur.end, ev.e);
      var col = cur.cols.findIndex(function (endAt) {
        return endAt <= ev.s;
      });
      if (col < 0) {
        col = cur.cols.length;
        cur.cols.push(ev.e);
      } else cur.cols[col] = ev.e;
      ev.col = col;
      cur.items.push(ev);
    });
    clusters.forEach(function (c) {
      c.items.forEach(function (ev) {
        ev.cols = c.cols.length;
      });
    });
    return sorted;
  }

  function renderTimeView() {
    var tv = $("time-view"),
      days = visibleDays(),
      today = C.todayKey(),
      byDay = {},
      ranges = {},
      earliest = 24 * 60;
    days.forEach(function (k) {
      var ev = C.eventsFor(k);
      byDay[k] = { allDay: [], timed: [] };
      ev.forEach(function (e) {
        var s = C.minutes(e.start);
        if (C.isRangeEvent(e)) ranges[C.eventIdentity(e)] = e;
        else if (!e.start || s === null) byDay[k].allDay.push(e);
        else {
          var en = C.minutes(e.end);
          if (en === null || en <= s) en = s + 60;
          earliest = Math.min(earliest, s);
          byDay[k].timed.push({ e: e, s: s, e2: en });
        }
      });
    });
    var startHour = Math.max(0, Math.min(7, Math.floor(earliest / 60))),
      endHour = 24,
      px = state.view === "day" ? 64 : 52,
      height = (endHour - startHour) * px,
      cols = days.length;

    // All-day strip: multi-day bars span their columns.
    var first = days[0],
      last = days[days.length - 1],
      strip = [];
    Object.keys(ranges).forEach(function (id) {
      var e = ranges[id],
        a = e.date > first ? e.date : first,
        b = (e.endDate || e.date) < last ? e.endDate || e.date : last;
      strip.push({
        e: e,
        from: days.indexOf(a) + 1,
        to: days.indexOf(b) + 2,
        k: a,
      });
    });
    days.forEach(function (k, i) {
      byDay[k].allDay.forEach(function (e) {
        strip.push({ e: e, from: i + 1, to: i + 2, k: k });
      });
    });
    strip.sort(function (a, b) {
      return a.from - b.from || b.to - b.from - (a.to - a.from);
    });

    var html =
      '<div class="tv tv-' +
      state.view +
      '" style="--cols:' +
      cols +
      '">' +
      '<div class="tv-head"><div class="tv-gutter"></div>' +
      days
        .map(function (k) {
          var d = C.fromKey(k);
          return (
            '<button type="button" class="tv-dayhead' +
            (k === today ? " today" : "") +
            '" data-goto-day="' +
            k +
            '"><span class="tv-dow">' +
            DAY_NAMES[d.getDay()] +
            '</span><span class="tv-num">' +
            d.getDate() +
            "</span></button>"
          );
        })
        .join("") +
      "</div>" +
      '<div class="tv-allday"><div class="tv-gutter">all-day</div><div class="tv-allday-grid">' +
      (strip.length
        ? strip
            .map(function (x) {
              return (
                '<button type="button" class="tv-chip ' +
                C.eventClasses(x.e) +
                '"' +
                C.eventAttrs(x.e) +
                ' data-open-day="' +
                x.k +
                '" style="grid-column:' +
                x.from +
                " / " +
                x.to +
                '" title="' +
                C.esc(x.e.title + (x.e.meta ? " · " + x.e.meta : "")) +
                '">' +
                C.esc(x.e.title) +
                "</button>"
              );
            })
            .join("")
        : "") +
      "</div></div>" +
      '<div class="tv-scroll" id="tv-scroll"><div class="tv-body" style="height:' +
      height +
      'px">' +
      '<div class="tv-gutter tv-hours">' +
      (function () {
        var h = "";
        for (var i = startHour + 1; i < endHour; i++)
          h +=
            '<span style="top:' +
            (i - startHour) * px +
            'px">' +
            (i % 12 || 12) +
            (i < 12 ? " AM" : " PM") +
            "</span>";
        return h;
      })() +
      "</div>" +
      days
        .map(function (k) {
          var placed = layoutColumns(
            byDay[k].timed.map(function (t) {
              return { ev: t.e, s: t.s, e: t.e2 };
            }),
          );
          return (
            '<div class="tv-col' +
            (k === today ? " today" : "") +
            '" data-col-day="' +
            k +
            '" style="background-size:100% ' +
            px +
            'px">' +
            placed
              .map(function (t) {
                var top = ((t.s - startHour * 60) / 60) * px,
                  h = Math.max(18, ((t.e - t.s) / 60) * px - 2),
                  w = 100 / t.cols,
                  mine = (t.ev.itemId && !C.isWork(t.ev)) || Boolean(t.ev.examId);
                return (
                  '<div class="timeline-event tv-ev ' +
                  C.eventClasses(t.ev) +
                  (h < 40 ? " tv-short" : "") +
                  (mine ? " tv-movable" : "") +
                  '"' +
                  C.eventAttrs(t.ev) +
                  ' data-open-day="' +
                  k +
                  '" data-s="' +
                  t.s +
                  '" data-e="' +
                  t.e +
                  '" style="top:' +
                  top +
                  "px;height:" +
                  h +
                  "px;left:calc(" +
                  w * t.col +
                  "% + 2px);width:calc(" +
                  w +
                  '% - 4px)" title="' +
                  C.esc(t.ev.title + (t.ev.meta ? " · " + t.ev.meta : "")) +
                  '"><div class="tv-ev-title">' +
                  C.esc(t.ev.title) +
                  '</div><div class="tv-ev-time">' +
                  C.esc(C.timeRange(t.ev.start, t.ev.end)) +
                  "</div>" +
                  (mine
                    ? '<div class="tv-resize" aria-hidden="true"></div>'
                    : "") +
                  "</div>"
                );
              })
              .join("") +
            (k === today
              ? '<div class="tv-now" style="top:' +
                ((nowMinutes() - startHour * 60) / 60) * px +
                'px"></div>'
              : "") +
            "</div>"
          );
        })
        .join("") +
      "</div></div></div>";
    tv.innerHTML = html;
    tv.dataset.startHour = startHour;
    tv.dataset.px = px;

    tv.querySelectorAll("[data-goto-day]").forEach(function (b) {
      b.addEventListener("click", function () {
        state.focus = b.dataset.gotoDay;
        setView("day");
      });
    });
    tv.querySelectorAll(".tv-chip[data-open-day]").forEach(function (b) {
      b.addEventListener("click", function () {
        C.openDay(b.dataset.openDay);
      });
    });
    setupTimeDrag(tv, startHour, px);

    // Scroll to just before now (or 8 AM) once per view/date change.
    var scroller = $("tv-scroll"),
      sig = state.view + state.focus;
    if (scroller && state.scrolledFor !== sig) {
      state.scrolledFor = sig;
      var target = days.indexOf(today) > -1 ? nowMinutes() - 90 : 8 * 60;
      scroller.scrollTop = Math.max(0, ((target - startHour * 60) / 60) * px);
    }
  }

  // Keep the red line moving.
  setInterval(function () {
    var line = document.querySelector(".tv-now"),
      tv = $("time-view");
    if (!line || !tv) return;
    var sh = Number(tv.dataset.startHour),
      px = Number(tv.dataset.px);
    line.style.top = ((nowMinutes() - sh * 60) / 60) * px + "px";
  }, 60000);

  // ── Drag in Week / Day ──────────────────────────────────────────────────
  var SNAP = 15;
  function snap(m) {
    return Math.round(m / SNAP) * SNAP;
  }
  function colAt(x) {
    var cols = document.querySelectorAll("#time-view .tv-col");
    for (var i = 0; i < cols.length; i++) {
      var r = cols[i].getBoundingClientRect();
      if (x >= r.left && x <= r.right) return cols[i];
    }
    return null;
  }
  function setupTimeDrag(tv, startHour, px) {
    function minsAt(col, y) {
      var r = col.getBoundingClientRect();
      return Math.max(
        0,
        Math.min(24 * 60, startHour * 60 + ((y - r.top) / px) * 60),
      );
    }

    tv.querySelectorAll(".tv-col").forEach(function (col) {
      col.addEventListener("pointerdown", function (ev) {
        if (ev.button !== 0 || ev.target.closest(".tv-ev")) return;
        ev.preventDefault();
        var a = snap(minsAt(col, ev.clientY)),
          ghost = document.createElement("div"),
          b = a + 60,
          moved = false;
        ghost.className = "tv-ghost";
        col.appendChild(ghost);
        function draw() {
          var s = Math.min(a, b),
            e = Math.max(a, b);
          if (e - s < SNAP) e = s + SNAP;
          ghost.style.top = ((s - startHour * 60) / 60) * px + "px";
          ghost.style.height = ((e - s) / 60) * px + "px";
          ghost.textContent = C.timeRange(C.toTime(s), C.toTime(e));
        }
        draw();
        function move(e) {
          var m = snap(minsAt(col, e.clientY));
          if (Math.abs(m - a) >= SNAP) moved = true;
          b = moved ? m : a + 60;
          draw();
        }
        function up() {
          document.removeEventListener("pointermove", move);
          document.removeEventListener("pointerup", up);
          var s = Math.min(a, b),
            e = Math.max(a, b);
          if (e - s < SNAP) e = s + 60;
          ghost.remove();
          createAt(
            col.dataset.colDay,
            C.toTime(s),
            C.toTime(Math.min(e, 24 * 60 - 1)),
          );
        }
        document.addEventListener("pointermove", move);
        document.addEventListener("pointerup", up);
      });
    });

    tv.querySelectorAll(".tv-ev").forEach(function (el) {
      el.addEventListener("pointerdown", function (ev) {
        if (ev.button !== 0) return;
        var movable = el.classList.contains("tv-movable"),
          resizing = Boolean(ev.target.closest(".tv-resize")),
          startX = ev.clientX,
          startY = ev.clientY,
          s0 = Number(el.dataset.s),
          e0 = Number(el.dataset.e),
          col0 = el.parentNode,
          dragging = false,
          targetCol = col0,
          ns = s0,
          ne = e0;
        if (!movable) return; // click handled below
        ev.preventDefault();
        // Listen on the document: moving the element into another day's
        // column mid-drag would drop any pointer capture on it.
        function move(e) {
          var dy = e.clientY - startY,
            dx = e.clientX - startX;
          if (!dragging && Math.abs(dy) < 4 && Math.abs(dx) < 4) return;
          dragging = true;
          el.classList.add("tv-dragging");
          var dm = snap((dy / px) * 60);
          if (resizing) {
            ns = s0;
            ne = Math.max(s0 + SNAP, Math.min(24 * 60 - 1, e0 + dm));
          } else {
            ns = Math.max(0, Math.min(24 * 60 - (e0 - s0), s0 + dm));
            ne = ns + (e0 - s0);
            var c = colAt(e.clientX);
            if (c && c !== targetCol) {
              targetCol = c;
              c.appendChild(el);
            }
          }
          el.style.top = ((ns - startHour * 60) / 60) * px + "px";
          el.style.height = Math.max(18, ((ne - ns) / 60) * px - 2) + "px";
          var t = el.querySelector(".tv-ev-time");
          if (t) t.textContent = C.timeRange(C.toTime(ns), C.toTime(ne));
        }
        function up() {
          document.removeEventListener("pointermove", move);
          document.removeEventListener("pointerup", up);
          el.classList.remove("tv-dragging");
          if (!dragging) {
            C.openDay(el.dataset.openDay);
            return;
          }
          if (el.dataset.examId)
            moveExam(el.dataset.examId, targetCol.dataset.colDay, C.toTime(ns), C.toTime(ne), resizing);
          else
            moveItem(
              el.dataset.itemId,
              targetCol.dataset.colDay,
              C.toTime(ns),
              C.toTime(ne),
            );
        }
        document.addEventListener("pointermove", move);
        document.addEventListener("pointerup", up);
      });
      el.addEventListener("click", function () {
        if (!el.classList.contains("tv-movable")) C.openDay(el.dataset.openDay);
      });
    });
  }

  function findItem(id) {
    return C.items.find(function (x) {
      return x.id === id;
    });
  }
  function moveItem(id, day, start, end) {
    var it = findItem(id);
    if (!it) return C.renderAll();
    var span =
      it.endDate && it.endDate !== it.date
        ? Math.round((C.fromKey(it.endDate) - C.fromKey(it.date)) / 86400000)
        : 0;
    var onlyEnd =
      day === it.date && start && start === it.start && end !== it.end;
    it.date = day;
    it.endDate = C.addDays(day, span);
    if (start) it.start = start;
    if (end) it.end = end;
    C.renderAll();
    C.persist().then(function () {
      C.toast(
        onlyEnd
          ? (it.title || "Event") + " now ends at " + C.timeLabel(it.end)
          : "Moved to " +
              C.prettyDate(day) +
              (start ? ", " + C.timeRange(it.start, it.end) : ""),
      );
    });
  }
  function moveExam(id, day, start, end, resized) {
    var e = C.exams.find(function (x) {
      return x.id === id;
    });
    var label = e ? (e.course || "Exam") + " " + (e.type || "") : "Exam";
    C.moveExam(id, day, start, end).then(function (ok) {
      if (ok && resized) C.toast(label.trim() + " now ends at " + C.timeLabel(end));
      else if (ok)
        C.toast(
          label.trim() +
            " moved to " +
            C.prettyDate(day) +
            (start ? ", " + C.timeRange(start, end) : ""),
        );
      else C.renderAll();
    });
  }
  function createAt(day, start, end) {
    C.openEventEditor(day, "personal");
    var kind = $("event-edit-kind");
    if (kind) {
      kind.value = "personal";
      kind.dispatchEvent(new Event("change"));
    }
    if ($("event-edit-start")) $("event-edit-start").value = start;
    if ($("event-edit-end")) $("event-edit-end").value = end;
    var t = $("event-edit-title");
    if (t) {
      t.placeholder = "New event";
      setTimeout(function () {
        t.focus();
      }, 30);
    }
  }

  // ── Drag between days in Month ──────────────────────────────────────────
  // Pointer-based so it works with a mouse and on touch screens: with a mouse
  // an event lifts after a few pixels of movement; on touch, press and hold
  // (so a normal swipe still scrolls). Your events and exams move; classes
  // stay put.
  var MONTH_DRAG = "[data-item-id], [data-exam-id]";
  function cellAt(x, y) {
    var els = document.elementsFromPoint(x, y);
    for (var i = 0; i < els.length; i++)
      if (els[i].matches && els[i].matches("#month-grid .day[data-date]")) return els[i];
    return null;
  }
  function setupMonthDrag() {
    var grid = $("month-grid");
    if (!grid || grid.dataset.dragReady) return;
    grid.dataset.dragReady = "1";
    var drag = null,
      suppressClick = false;

    // Your own multi-day bars sit in a layer that otherwise ignores the
    // pointer; a plain click on one still opens the day underneath.
    grid.addEventListener("click", function (ev) {
      if (suppressClick) {
        suppressClick = false;
        ev.stopPropagation();
        ev.preventDefault();
        return;
      }
      var bar = ev.target.closest && ev.target.closest(".range-bar[data-item-id]");
      if (!bar) return;
      var cell = cellAt(ev.clientX, ev.clientY);
      if (!cell) return;
      if (!window.__shougCalViews.dayClick(cell.dataset.date, ev)) C.openDay(cell.dataset.date);
    }, true);

    function clearDrop() {
      grid.querySelectorAll(".cv-drop").forEach(function (c) {
        c.classList.remove("cv-drop");
      });
    }
    function lift() {
      drag.active = true;
      var r = drag.el.getBoundingClientRect(),
        g = drag.el.cloneNode(true);
      g.className += " cv-ghost";
      g.removeAttribute("data-item-id");
      g.removeAttribute("data-exam-id");
      g.style.width = Math.min(r.width, 240) + "px";
      g.style.height = r.height + "px";
      document.body.appendChild(g);
      drag.ghost = g;
      drag.dx = Math.min(drag.x - r.left, Math.min(r.width, 240) - 12);
      drag.dy = drag.y - r.top;
      drag.el.classList.add("cv-dragging");
      document.body.classList.add("cv-drag-on");
      if (drag.touch && navigator.vibrate) navigator.vibrate(10);
      place(drag.x, drag.y);
    }
    function place(x, y) {
      drag.ghost.style.left = x - drag.dx + "px";
      drag.ghost.style.top = y - drag.dy + "px";
      var cell = cellAt(x, y);
      clearDrop();
      if (cell) cell.classList.add("cv-drop");
      drag.cell = cell;
    }
    function end(commit) {
      var d = drag;
      drag = null;
      clearTimeout(d.timer);
      document.removeEventListener("pointermove", onMove);
      document.removeEventListener("pointerup", onUp);
      document.removeEventListener("pointercancel", onCancel);
      document.removeEventListener("touchmove", blockScroll, { passive: false });
      document.removeEventListener("keydown", onKey);
      if (!d.active) return;
      suppressClick = true;
      setTimeout(function () {
        suppressClick = false;
      }, 400);
      d.ghost.remove();
      d.el.classList.remove("cv-dragging");
      document.body.classList.remove("cv-drag-on");
      clearDrop();
      if (!commit || !d.cell || !d.from || d.cell.dataset.date === d.from) return;
      var delta = Math.round((C.fromKey(d.cell.dataset.date) - C.fromKey(d.from)) / 86400000);
      if (d.examId) {
        var e = C.exams.find(function (x) {
          return x.id === d.examId;
        });
        if (e) moveExam(d.examId, C.addDays(e.date, delta), "", "");
      } else {
        var it = findItem(d.itemId);
        if (it) moveItem(d.itemId, C.addDays(it.date, delta), "", "");
      }
    }
    function onMove(ev) {
      if (!drag) return;
      var far = Math.abs(ev.clientX - drag.x) + Math.abs(ev.clientY - drag.y);
      if (!drag.active) {
        if (drag.touch) {
          if (far > 10) end(false); // a swipe: let the page scroll
          return;
        }
        if (far < 6) return;
        lift();
      }
      ev.preventDefault();
      place(ev.clientX, ev.clientY);
    }
    function onUp() {
      if (drag) end(true);
    }
    function onCancel() {
      if (drag) end(false);
    }
    function onKey(ev) {
      if (ev.key === "Escape" && drag) end(false);
    }
    function blockScroll(ev) {
      if (drag && drag.active) ev.preventDefault();
    }
    grid.addEventListener("pointerdown", function (ev) {
      if (ev.button !== 0 || drag || isPhone()) return;
      var el = ev.target.closest && ev.target.closest(MONTH_DRAG);
      if (!el || !grid.contains(el)) return;
      var from = cellAt(ev.clientX, ev.clientY);
      drag = {
        el: el,
        itemId: el.dataset.itemId || "",
        examId: el.dataset.examId || "",
        from: from ? from.dataset.date : el.dataset.evDate,
        x: ev.clientX,
        y: ev.clientY,
        touch: ev.pointerType === "touch",
        active: false,
      };
      if (drag.touch) {
        drag.timer = setTimeout(function () {
          if (drag && !drag.active) lift();
        }, 350);
        document.addEventListener("touchmove", blockScroll, { passive: false });
      } else ev.preventDefault(); // no text selection while dragging
      document.addEventListener("pointermove", onMove);
      document.addEventListener("pointerup", onUp);
      document.addEventListener("pointercancel", onCancel);
      document.addEventListener("keydown", onKey);
    });
    // Long-press on touch would otherwise open the context menu / callout.
    grid.addEventListener("contextmenu", function (ev) {
      if (ev.target.closest && ev.target.closest(MONTH_DRAG)) ev.preventDefault();
    });
  }

  // ── Phone month: dots + day list ────────────────────────────────────────
  function renderPhoneMonth() {
    var grid = $("month-grid");
    if (!grid) return;
    var cm = C.currentMonth,
      inMonth = function (k) {
        var d = C.fromKey(k);
        return (
          d.getMonth() === cm.getMonth() && d.getFullYear() === cm.getFullYear()
        );
      };
    if (!state.phoneDay || !inMonth(state.phoneDay))
      state.phoneDay = inMonth(C.todayKey())
        ? C.todayKey()
        : C.key(new Date(cm.getFullYear(), cm.getMonth(), 1));
    grid.querySelectorAll(".day[data-date]").forEach(function (cell) {
      var k = cell.dataset.date,
        ev = C.eventsFor(k).filter(function (e) {
          return !e.hideInMonth;
        }),
        dots = document.createElement("div");
      dots.className = "pd-dots";
      dots.innerHTML = ev
        .slice(0, 4)
        .map(function (e) {
          return (
            '<i class="pd-dot ' +
            C.eventClasses(e) +
            '"' +
            C.eventAttrs(e) +
            "></i>"
          );
        })
        .join("");
      cell.appendChild(dots);
      cell.classList.toggle("pd-selected", k === state.phoneDay);
    });
    renderPhoneDay();
  }
  function renderPhoneDay() {
    var pd = $("phone-day");
    if (!pd) return;
    var k = state.phoneDay,
      ev = C.eventsFor(k);
    pd.innerHTML =
      '<div class="pd-head"><div><div class="pd-date">' +
      C.esc(fmt(k, { weekday: "long", month: "long", day: "numeric" })) +
      '</div><div class="pd-count">' +
      (ev.length
        ? ev.length + " item" + (ev.length === 1 ? "" : "s")
        : "Nothing scheduled") +
      '</div></div><button type="button" class="pd-add" data-pd-add>+ Add</button></div>' +
      '<div class="pd-list">' +
      ev.map(C.dayCardHtml).join("") +
      "</div>";
    C.bindEventActions(pd);
    pd.querySelector("[data-pd-add]").addEventListener("click", function () {
      C.openEventEditor(k, "personal");
    });
    paintCourses(pd);
  }

  // ── Quick add ───────────────────────────────────────────────────────────
  var MONTHS = [
    "jan",
    "feb",
    "mar",
    "apr",
    "may",
    "jun",
    "jul",
    "aug",
    "sep",
    "oct",
    "nov",
    "dec",
  ];
  var DOW = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"];
  function pad(n) {
    return (n < 10 ? "0" : "") + n;
  }
  var quickEvening = "";
  function parseClock(h, m, ap, fallbackAp) {
    h = Number(h);
    m = Number(m || 0);
    ap = (ap || fallbackAp || quickEvening || "").toLowerCase();
    if (h > 24 || m > 59) return null;
    if (ap === "pm" && h < 12) h += 12;
    if (ap === "am" && h === 12) h = 0;
    // "at 3" with no am/pm: classes and plans are daytime, so 1–7 means PM.
    if (!ap && h >= 1 && h <= 7) h += 12;
    return h * 60 + m;
  }

  function parseQuick(text) {
    var raw = String(text || "").trim(),
      t = " " + raw.toLowerCase() + " ",
      today = C.todayKey(),
      out = {
        kind: "personal",
        date: "",
        endDate: "",
        start: "",
        end: "",
        course: "",
        examType: "",
        location: "",
      },
      used = [];
    function take(re, fn) {
      var m = t.match(re);
      if (!m) return false;
      if (fn(m) === false) return false;
      used.push(m[0]);
      t = t.replace(m[0], " ");
      return true;
    }
    // location: "@ hall a" or "in b204"
    take(/\s@\s*([^@]+?)\s*$/, function (m) {
      out.location = raw.slice(
        raw.toLowerCase().lastIndexOf(m[1].trim()),
        raw.toLowerCase().lastIndexOf(m[1].trim()) + m[1].trim().length,
      );
    });
    take(
      /\sin\s+(room\s+\w+|[a-z]?\d{2,4}[a-z]?|hall\s+\w+|building\s+\w+)\s/,
      function (m) {
        out.location = m[1].replace(/\b\w/g, function (c) {
          return c.toUpperCase();
        });
      },
    );
    // course
    take(/\s([a-z]{2,6})\s?-?(\d{3}[a-z]?)\s/, function (m) {
      out.course = C.courseLabel(m[1] + m[2]);
    });
    // kind
    var ex = t.match(/\s(quiz|midterm|final|exam|test)\s/);
    if (ex) {
      out.kind = "exam";
      out.examType = ex[1] === "test" ? "exam" : ex[1];
    } else if (
      /\s(assignment|homework|hw|lab|report|essay|due|submission)\s/.test(t)
    )
      out.kind = "assignment";
    else if (/\s(project|phase|milestone|deliverable)\s/.test(t))
      out.kind = "project";
    else if (/\s(study|review|revise|revision)\s/.test(t)) out.kind = "study";
    else if (/\s(flight|travel|trip|vacation)\s/.test(t)) out.kind = "travel";
    else if (/\s(busy|unavailable|blocked)\s/.test(t)) out.kind = "busy";

    // "tonight at 8" means 8 PM.
    quickEvening = /\s(tonight|evening)\s/.test(t) ? "pm" : "";
    // times: ranges first
    var gotTime =
      take(
        /\s(?:from\s+)?(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\s*(?:-|–|to|until)\s*(\d{1,2})(?::(\d{2}))?\s*(am|pm)?(?!\s*(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec))\s/,
        function (m) {
          var b = parseClock(m[4], m[5], m[6]),
            a = parseClock(m[1], m[2], m[3], m[6]);
          if (a === null || b === null) return false;
          if (b <= a && !m[3]) a -= 12 * 60;
          if (a < 0 || b <= a) return false;
          out.start = pad(Math.floor(a / 60)) + ":" + pad(a % 60);
          out.end = pad(Math.floor(b / 60)) + ":" + pad(b % 60);
        },
      ) ||
      take(/\s(?:at\s+)?(noon|midnight)\s/, function (m) {
        out.start = m[1] === "noon" ? "12:00" : "00:00";
      }) ||
      take(/\s(?:at\s+)?(\d{1,2}):(\d{2})\s*(am|pm)?\s/, function (m) {
        var a = parseClock(m[1], m[2], m[3]);
        if (a === null) return false;
        out.start = pad(Math.floor(a / 60)) + ":" + pad(a % 60);
      }) ||
      take(/\s(?:at\s+)?(\d{1,2})\s*(am|pm)\s/, function (m) {
        var a = parseClock(m[1], 0, m[2]);
        if (a === null) return false;
        out.start = pad(Math.floor(a / 60)) + ":" + pad(a % 60);
      }) ||
      take(/\sat\s+(\d{1,2})\s/, function (m) {
        var a = parseClock(m[1], 0, "");
        if (a === null) return false;
        out.start = pad(Math.floor(a / 60)) + ":" + pad(a % 60);
      });
    take(/\sall[\s-]?day\s/, function () {
      out.start = out.end = "";
    });
    if (out.start && !out.end) {
      var s = C.minutes(out.start) + 60;
      out.end = s >= 24 * 60 ? "23:59" : C.toTime(s);
    }

    // dates
    var monthRe =
      "(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*";
    function mk(y, mo, d) {
      var dt = new Date(y, mo, d);
      return dt.getMonth() === mo ? C.key(dt) : "";
    }
    function yearFor(mo, d) {
      var y = new Date().getFullYear(),
        k = mk(y, mo, d);
      return k && k < C.addDays(today, -60) ? mk(y + 1, mo, d) : k;
    }
    take(/\s(\d{4})-(\d{2})-(\d{2})\s/, function (m) {
      out.date = mk(+m[1], +m[2] - 1, +m[3]);
    }) ||
      take(
        new RegExp(
          "\\s" +
            monthRe +
            "\\s+(\\d{1,2})(?:st|nd|rd|th)?(?:\\s*(?:-|–|to)\\s*(\\d{1,2}))?\\s",
        ),
        function (m) {
          var mo = MONTHS.indexOf(m[1].slice(0, 3));
          out.date = yearFor(mo, +m[2]);
          if (m[3]) out.endDate = yearFor(mo, +m[3]);
        },
      ) ||
      take(
        new RegExp(
          "\\s(\\d{1,2})(?:st|nd|rd|th)?(?:\\s*(?:-|–|to)\\s*(\\d{1,2}))?\\s+" +
            monthRe +
            "\\s",
        ),
        function (m) {
          var mo = MONTHS.indexOf(m[3].slice(0, 3));
          out.date = yearFor(mo, +m[1]);
          if (m[2]) out.endDate = yearFor(mo, +m[2]);
        },
      ) ||
      take(/\s(\d{1,2})\/(\d{1,2})\s/, function (m) {
        var a = +m[1],
          b = +m[2];
        // Day/month (as used in Saudi Arabia) unless that is impossible.
        out.date = a > 12 || b <= 12 ? yearFor(b - 1, a) : yearFor(a - 1, b);
      }) ||
      take(/\s(today|tonight)\s/, function () {
        out.date = today;
      }) ||
      take(/\s(tomorrow|tmrw|tmr)\s/, function () {
        out.date = C.addDays(today, 1);
      }) ||
      take(/\sin\s+(\d{1,2})\s+days?\s/, function (m) {
        out.date = C.addDays(today, +m[1]);
      }) ||
      take(
        /\s(next\s+|this\s+|on\s+)?(sun|mon|tue|tues|wed|thu|thur|thurs|fri|sat)[a-z]*\s/,
        function (m) {
          var want = DOW.indexOf(m[2].slice(0, 3)),
            cur = C.fromKey(today).getDay(),
            add = (want - cur + 7) % 7;
          if (m[1] && /next/.test(m[1]) && add < 7) add += add === 0 ? 7 : 7;
          out.date = C.addDays(today, add);
        },
      ) ||
      take(/\snext\s+week\s/, function () {
        out.date = C.addDays(today, 7);
      });

    // title from what is left
    var title = (" " + t + " ")
      .replace(/\s(at|on|from|to|until|by|for|the|in|due)\s/g, " ")
      .replace(/\s+/g, " ")
      .trim();
    var words = raw.split(/\s+/),
      kept = [];
    title.split(" ").forEach(function (w) {
      var orig = words.find(function (x) {
        return x.toLowerCase() === w;
      });
      if (w) kept.push(orig || w);
    });
    out.title = kept.join(" ");
    if (out.kind === "exam") out.title = "";
    else if (!out.title)
      out.title = out.course ? out.course + " " + out.kind : "";
    else if (
      out.course &&
      out.title.toUpperCase().indexOf(out.course.replace(" ", "")) < 0
    )
      out.title = out.title.charAt(0).toUpperCase() + out.title.slice(1);
    if (out.endDate && out.endDate < out.date) out.endDate = "";
    return out;
  }

  var KIND_LABEL = {
    exam: "Exam",
    assignment: "Assignment",
    project: "Project",
    study: "Study",
    travel: "Travel",
    busy: "Unavailable",
    personal: "Event",
  };
  function describe(q) {
    var when = q.date
      ? fmt(q.date, { weekday: "short", month: "short", day: "numeric" }) +
        (q.endDate && q.endDate !== q.date
          ? " – " + fmt(q.endDate, { month: "short", day: "numeric" })
          : "")
      : "pick a day";
    var what =
      q.kind === "exam"
        ? (q.course || "Course?") +
          " " +
          q.examType.charAt(0).toUpperCase() +
          q.examType.slice(1)
        : q.title || "Untitled";
    return (
      KIND_LABEL[q.kind] +
      " · " +
      what +
      " · " +
      when +
      " · " +
      (q.start ? C.timeRange(q.start, q.end) : "All day") +
      (q.location ? " · " + q.location : "") +
      (q.course && q.kind !== "exam" ? " · " + q.course : "")
    );
  }
  function setupQuickAdd() {
    var input = $("cv-quick"),
      prev = $("cv-quick-preview");
    function update() {
      if (!input.value.trim()) {
        prev.textContent = "";
        prev.classList.remove("show");
        return null;
      }
      var q = parseQuick(input.value);
      prev.textContent = describe(q) + (q.date ? "  ·  Enter to add" : "");
      prev.classList.add("show");
      prev.classList.toggle("bad", !q.date || (q.kind === "exam" && !q.course));
      return q;
    }
    input.addEventListener("input", update);
    input.addEventListener("blur", function () {
      setTimeout(function () {
        prev.classList.remove("show");
      }, 150);
    });
    input.addEventListener("focus", update);
    input.addEventListener("keydown", function (e) {
      if (e.key === "Escape") {
        input.value = "";
        update();
        input.blur();
        return;
      }
      if (e.key !== "Enter") return;
      e.preventDefault();
      var q = update();
      if (!q) return;
      if (!q.date) return C.toast("Add a day, like Tue, tomorrow or Oct 25");
      if (q.kind === "exam" && !q.course)
        return C.toast("Add the course code, like SE322 quiz Tue");
      var done =
        q.kind === "exam"
          ? C.addExam({
              course: q.course,
              examType: q.examType,
              date: q.date,
              start: q.start,
              end: q.end,
              location: q.location,
            })
          : C.saveNewEvent({
              title: q.title,
              date: q.date,
              endDate: q.endDate || q.date,
              kind: q.kind,
              start: q.start,
              end: q.end,
              location: q.location,
              course: q.course,
            });
      Promise.resolve(done).then(function (ok) {
        if (ok === false) return;
        input.value = "";
        update();
        state.focus = q.date;
        C.currentMonth = C.fromKey(q.date);
        C.renderAll(true);
      });
    });
  }

  // ── Search ──────────────────────────────────────────────────────────────
  function searchIndex() {
    var out = [];
    C.items.forEach(function (it) {
      out.push({
        date: it.date,
        end: it.endDate || it.date,
        title: it.title || "Event",
        sub: [KIND_LABEL[it.kind] || "Event", it.course, it.location]
          .filter(Boolean)
          .join(" · "),
        hay: [it.title, it.course, it.location, it.notes, it.kind].join(" "),
      });
    });
    C.exams.forEach(function (e) {
      out.push({
        date: e.date,
        end: e.date,
        title: (e.course || "") + " " + (e.type || "exam"),
        sub: ["Exam", e.location].filter(Boolean).join(" · "),
        hay: [e.course, e.type, e.location, "exam"].join(" "),
      });
    });
    C.classes.forEach(function (c) {
      out.push({
        date: "",
        title: c.title || "Class",
        sub:
          "Weekly class · " +
          (c.days || [])
            .map(function (d) {
              return d.slice(0, 3);
            })
            .join(", ") +
          (c.start ? " · " + C.timeLabel(c.start) : ""),
        hay: [c.title, c.location, "class"].join(" "),
        classId: c.id,
      });
    });
    return out;
  }
  function nextClassDay(classId) {
    var k = C.todayKey();
    for (var i = 0; i < 120; i++) {
      var d = C.addDays(k, i);
      if (
        C.eventsFor(d).some(function (e) {
          return e.classId === classId;
        })
      )
        return d;
    }
    return k;
  }
  function setupSearch() {
    var input = $("cv-search"),
      box = $("cv-results"),
      results = [],
      active = -1;
    function norm(s) {
      return String(s || "")
        .toLowerCase()
        .replace(/\s+/g, "");
    }
    function run() {
      var q = input.value.trim().toLowerCase();
      if (!q) {
        box.hidden = true;
        return;
      }
      var words = q.split(/\s+/),
        today = C.todayKey();
      results = searchIndex()
        .filter(function (r) {
          var hay = r.hay.toLowerCase(),
            flat = norm(r.hay);
          return words.every(function (w) {
            return hay.indexOf(w) > -1 || flat.indexOf(norm(w)) > -1;
          });
        })
        .sort(function (a, b) {
          var au = !a.date || a.end >= today,
            bu = !b.date || b.end >= today;
          if (au !== bu) return au ? -1 : 1;
          if (!a.date || !b.date) return a.date ? -1 : b.date ? 1 : 0;
          return au
            ? a.date.localeCompare(b.date)
            : b.date.localeCompare(a.date);
        })
        .slice(0, 10);
      active = results.length ? 0 : -1;
      draw();
    }
    function draw() {
      box.hidden = false;
      box.innerHTML = results.length
        ? results
            .map(function (r, i) {
              return (
                '<button type="button" role="option" class="cv-result' +
                (i === active ? " on" : "") +
                (r.date && r.end < C.todayKey() ? " past" : "") +
                '" data-i="' +
                i +
                '"><span class="cv-r-title">' +
                C.esc(r.title) +
                '</span><span class="cv-r-sub">' +
                C.esc(
                  (r.date
                    ? fmt(r.date, {
                        weekday: "short",
                        month: "short",
                        day: "numeric",
                        year: "numeric",
                      }) + " · "
                    : "") + r.sub,
                ) +
                "</span></button>"
              );
            })
            .join("")
        : '<div class="cv-empty">No matching events</div>';
      box.querySelectorAll("[data-i]").forEach(function (b) {
        b.addEventListener("mousedown", function (e) {
          e.preventDefault();
          choose(Number(b.dataset.i));
        });
      });
    }
    function choose(i) {
      var r = results[i];
      if (!r) return;
      var k = r.date || nextClassDay(r.classId);
      box.hidden = true;
      input.blur();
      state.focus = k;
      C.currentMonth = C.fromKey(k);
      C.renderAll(true);
      if (state.view === "month") C.openDay(k);
    }
    input.addEventListener("input", run);
    input.addEventListener("focus", run);
    input.addEventListener("blur", function () {
      setTimeout(function () {
        box.hidden = true;
      }, 120);
    });
    input.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        e.preventDefault();
        if (!results.length) return;
        active =
          (active + (e.key === "ArrowDown" ? 1 : -1) + results.length) %
          results.length;
        draw();
      } else if (e.key === "Enter") {
        e.preventDefault();
        choose(active);
      } else if (e.key === "Escape") {
        input.value = "";
        box.hidden = true;
        input.blur();
      }
    });
  }

  // ── Keyboard shortcuts ──────────────────────────────────────────────────
  var HELP = [
    ["T", "Today"],
    ["← / →", "Previous / next"],
    ["M  W  D", "Month, week, day"],
    ["N", "New event"],
    ["Q", "Quick add"],
    ["/", "Search"],
    ["?", "Show shortcuts"],
  ];
  function showHelp() {
    var el = $("cv-help-sheet");
    if (el) {
      el.remove();
      return;
    }
    el = document.createElement("div");
    el.id = "cv-help-sheet";
    el.className = "cv-help-sheet";
    el.setAttribute("role", "dialog");
    el.setAttribute("aria-label", "Keyboard shortcuts");
    el.innerHTML =
      "<b>Keyboard shortcuts</b>" +
      HELP.map(function (h) {
        return "<div><kbd>" + h[0] + "</kbd><span>" + h[1] + "</span></div>";
      }).join("") +
      '<button type="button" class="cv-help-close">Close</button>';
    document.body.appendChild(el);
    el.querySelector(".cv-help-close").addEventListener("click", function () {
      el.remove();
    });
  }
  document.addEventListener("keydown", function (e) {
    if (!C || e.metaKey || e.ctrlKey || e.altKey) return;
    var tgt = e.target;
    if (
      tgt &&
      (tgt.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(tgt.tagName))
    )
      return;
    if (!$("calendar-app") || $("calendar-app").offsetParent === null) return;
    if (modalOpen()) return;
    var k = e.key;
    if (k === "Escape" && $("cv-help-sheet"))
      return $("cv-help-sheet").remove();
    var map = {
      t: function () {
        $("today-btn").click();
      },
      ArrowLeft: function () {
        $("prev-month").click();
      },
      ArrowRight: function () {
        $("next-month").click();
      },
      m: function () {
        setView("month");
      },
      w: function () {
        setView("week");
      },
      d: function () {
        setView("day");
      },
      n: function () {
        C.openEventEditor(
          state.view === "month" ? C.todayKey() : state.focus,
          "personal",
        );
      },
      q: function () {
        $("cv-quick").focus();
      },
      "/": function () {
        $("cv-search").focus();
      },
      "?": showHelp,
    };
    var fn =
      map[k] || map[k.toLowerCase && k.length === 1 ? k.toLowerCase() : k];
    if (!fn) return;
    e.preventDefault();
    // Calendar shortcuts bring the Calendar tab forward first.
    if (window.__shougCalTab && /^(t|m|w|d|q|\/|ArrowLeft|ArrowRight)$/i.test(k)) window.__shougCalTab("calendar");
    fn();
  });

  // ── Hooks the calendar page calls ───────────────────────────────────────
  window.__shougCalViews = {
    render: render,
    step: function (dir) {
      if (!C || state.view === "month") return false;
      state.focus = C.addDays(
        state.focus,
        dir * (state.view === "week" ? 7 : 1),
      );
      C.currentMonth = C.fromKey(state.focus);
      C.renderAll(true);
      return true;
    },
    goTo: function (k) {
      state.focus = k;
      state.phoneDay = k;
      state.scrolledFor = "";
    },
    dayClick: function (k) {
      if (!C) return false;
      state.focus = k;
      if (state.view === "month" && isPhone()) {
        state.phoneDay = k;
        document
          .querySelectorAll("#month-grid .pd-selected")
          .forEach(function (c) {
            c.classList.remove("pd-selected");
          });
        var cell = document.querySelector(
          '#month-grid .day[data-date="' + k + '"]',
        );
        if (cell) cell.classList.add("pd-selected");
        renderPhoneDay();
        return true;
      }
      return false;
    },
    parseQuick: function (s) {
      return parseQuick(s);
    },
  };

  phoneQuery.addEventListener &&
    phoneQuery.addEventListener("change", function () {
      if (C) C.renderAll();
    });

  function boot() {
    if (!window.__shougCal) return setTimeout(boot, 50);
    C = window.__shougCal;
    state.view = load(VIEW_KEY, "month");
    if (["month", "week", "day"].indexOf(state.view) < 0) state.view = "month";
    state.colourByCourse = load(CC_KEY, "0") === "1";
    state.focus = C.todayKey();
    injectStyles();
    if (C.signedIn) C.renderAll();
  }

  // ── Styles ──────────────────────────────────────────────────────────────
  function injectStyles() {
    if ($("cv-styles")) return;
    var css = [
      ".cal-toolbar{display:flex;flex-wrap:wrap;align-items:center;gap:10px;padding:12px 18px;border-bottom:1px solid var(--line);background:var(--surface)}",
      ".cv-seg{display:inline-flex;padding:3px;border:1px solid var(--line);border-radius:999px;background:var(--item-bg)}",
      ".cv-seg button{border:0;background:none;color:var(--dim);font:800 .7rem/1 'JetBrains Mono',monospace;letter-spacing:.06em;padding:8px 14px;border-radius:999px;cursor:pointer}",
      ".cv-seg button.on{background:var(--brand);color:#0a0514}",
      ".cv-quick,.cv-search{position:relative;flex:1 1 220px;min-width:0}",
      ".cv-quick input,.cv-search input{width:100%;height:36px;box-sizing:border-box;border:1px solid var(--line);border-radius:999px;background:var(--input);color:var(--text);padding:0 14px;font:500 .85rem Inter,system-ui,sans-serif;outline:none}",
      ".cv-quick input:focus,.cv-search input:focus{border-color:rgba(184,41,234,.75);box-shadow:0 0 0 3px rgba(184,41,234,.16)}",
      ".cv-quick-preview{position:absolute;left:0;right:0;top:calc(100% + 6px);z-index:50;padding:9px 12px;border:1px solid rgba(184,41,234,.45);border-radius:10px;background:var(--panel);color:var(--text);font:600 .78rem Inter,system-ui,sans-serif;box-shadow:0 10px 30px rgba(0,0,0,.3);display:none}",
      ".cv-quick-preview.show{display:block}.cv-quick-preview.bad{border-color:rgba(245,158,11,.6);color:var(--amber)}",
      ".cv-results{position:absolute;left:0;right:0;top:calc(100% + 6px);z-index:50;max-height:360px;overflow:auto;border:1px solid var(--line);border-radius:12px;background:var(--panel);box-shadow:0 12px 34px rgba(0,0,0,.35)}",
      ".cv-result{display:flex;flex-direction:column;gap:2px;width:100%;text-align:left;border:0;border-bottom:1px solid var(--line);background:none;color:var(--text);padding:9px 12px;cursor:pointer}",
      ".cv-result.on,.cv-result:hover{background:var(--hover)}.cv-result.past{opacity:.6}",
      ".cv-r-title{font:700 .85rem Inter,system-ui,sans-serif}.cv-r-sub{font-size:.72rem;color:var(--muted)}.cv-empty{padding:12px;color:var(--muted);font-size:.8rem}",
      ".cv-cc,.cv-help{height:36px;border:1px solid var(--line);border-radius:999px;background:none;color:var(--dim);font:800 .66rem 'JetBrains Mono',monospace;letter-spacing:.06em;padding:0 14px;cursor:pointer}",
      ".cv-cc.on{border-color:var(--brand);color:var(--brand)}.cv-help{width:36px;padding:0}",
      ".cv-help-sheet{position:fixed;right:24px;bottom:130px;z-index:99998;width:260px;padding:14px 16px;border:1px solid var(--line);border-radius:14px;background:var(--panel);color:var(--text);box-shadow:0 16px 40px rgba(0,0,0,.4);font-size:.82rem}",
      ".cv-help-sheet b{display:block;margin-bottom:8px}.cv-help-sheet div{display:flex;justify-content:space-between;gap:10px;padding:4px 0;color:var(--dim)}",
      ".cv-help-sheet kbd{font:700 .72rem 'JetBrains Mono',monospace;color:var(--text);border:1px solid var(--line);border-radius:6px;padding:2px 6px}.cv-help-close{margin-top:8px;border:1px solid var(--line);background:none;color:var(--dim);border-radius:999px;padding:6px 12px;cursor:pointer}",
      /* time grid */
      ".time-view{background:var(--surface)}",
      ".tv{--gut:58px;display:flex;flex-direction:column}",
      ".tv-head,.tv-allday{display:grid;grid-template-columns:var(--gut) repeat(var(--cols),minmax(0,1fr));border-bottom:1px solid var(--line)}",
      ".tv-gutter{font:700 .62rem 'JetBrains Mono',monospace;color:var(--muted);text-align:right;padding:6px 8px 0 0}",
      ".tv-dayhead{display:flex;align-items:baseline;justify-content:center;gap:6px;border:0;border-left:1px solid var(--line);background:none;color:var(--dim);padding:10px 4px;cursor:pointer;font:700 .72rem 'JetBrains Mono',monospace}",
      ".tv-dayhead .tv-num{font:800 1.05rem Inter,system-ui,sans-serif;color:var(--text);min-width:30px;height:30px;line-height:30px;border-radius:50%;display:inline-block;text-align:center}",
      ".tv-dayhead.today .tv-num{background:var(--red);color:#fff}.tv-dayhead.today{color:var(--red)}",
      ".tv-allday-grid{grid-column:2 / -1;display:grid;grid-template-columns:repeat(var(--cols),minmax(0,1fr));grid-auto-flow:row dense;gap:3px;padding:4px 3px;min-height:30px}",
      "#month-weekdays[hidden],#month-grid[hidden],.time-view[hidden],.phone-day[hidden]{display:none!important}",
      ".tv-chip{border:0;border-left:3px solid currentColor;border-radius:6px;padding:4px 7px;text-align:left;font:700 .7rem Inter,system-ui,sans-serif;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;cursor:pointer;background:rgba(96,165,250,.14);color:var(--blue);min-width:0}",
      ".tv-chip{background:color-mix(in srgb,currentColor 16%,transparent)}",
      ".tv-chip.exam{color:var(--red)}.tv-chip.class{color:var(--blue)}.tv-chip.study{color:#a3e635}.tv-chip.assignment{color:#c084fc}.tv-chip.project{color:#f472b6}.tv-chip.personal{color:var(--green)}.tv-chip.travel{color:var(--teal)}.tv-chip.busy{color:var(--amber)}.tv-chip.academic{color:var(--purple)}",
      ".tv-scroll{max-height:min(72vh,760px);overflow-y:auto;position:relative}",
      ".tv-body{display:grid;grid-template-columns:var(--gut) repeat(var(--cols),minmax(0,1fr));position:relative}",
      ".tv-hours{position:relative;padding:0}.tv-hours span{position:absolute;right:8px;transform:translateY(-50%);font:700 .62rem 'JetBrains Mono',monospace;color:var(--muted)}",
      ".tv-col{position:relative;border-left:1px solid var(--line);background-image:linear-gradient(to bottom,var(--line) 1px,transparent 1px);cursor:crosshair;touch-action:none}",
      ".tv-col.today{background-color:rgba(184,41,234,.04)}",
      ".tv .tv-ev{position:absolute;left:2px;right:auto;min-height:0;padding:4px 6px;border-radius:7px;border-left-width:3px;overflow:hidden;cursor:pointer;box-sizing:border-box;z-index:2}",
      ".tv .tv-ev.tv-movable{cursor:grab}.tv .tv-ev.tv-dragging{opacity:.85;cursor:grabbing;z-index:5;box-shadow:0 8px 20px rgba(0,0,0,.35)}",
      ".tv-ev-title{font:700 .74rem/1.2 Inter,system-ui,sans-serif;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}",
      ".tv-ev-time{font-size:.66rem;opacity:.8;white-space:nowrap}.tv-short .tv-ev-time{display:none}",
      ".tv-resize{position:absolute;left:0;right:0;bottom:0;height:7px;cursor:ns-resize}",
      ".tv-now{position:absolute;left:0;right:0;height:2px;background:var(--red);z-index:4;pointer-events:none}",
      ".tv-now::before{content:'';position:absolute;left:-5px;top:-4px;width:10px;height:10px;border-radius:50%;background:var(--red)}",
      ".tv-ghost{position:absolute;left:2px;right:2px;border-radius:7px;background:rgba(184,41,234,.22);border:1px dashed var(--brand);color:var(--brand);font:700 .68rem 'JetBrains Mono',monospace;padding:4px 6px;z-index:3;pointer-events:none}",
      ".tv-day .tv-ev-title{font-size:.86rem}.tv-day .tv-ev{padding:6px 10px}",
      /* month drag */
      "#month-grid .range-bar[data-item-id]{pointer-events:auto}",
      "#month-grid [data-item-id],#month-grid [data-exam-id]{cursor:grab;-webkit-touch-callout:none;-webkit-user-select:none;user-select:none}",
      "#month-grid .range-bar[data-exam-id]{pointer-events:auto}",
      ".cv-dragging{opacity:.35}.day.cv-drop{outline:2px dashed var(--brand);outline-offset:-3px;background:rgba(184,41,234,.08)}",
      ".cv-ghost{position:fixed!important;z-index:99999;pointer-events:none;margin:0!important;opacity:.95;box-shadow:0 12px 28px rgba(0,0,0,.45);transform:rotate(-1.5deg);overflow:hidden}",
      "body.cv-drag-on,body.cv-drag-on *{cursor:grabbing!important;user-select:none!important}",
      /* course colours */
      "body.cal-cc [data-course]:not(.pd-dot){background:hsl(var(--cc) 75% 60% / .16)!important;color:hsl(var(--cc) 85% 72%)!important;border-color:hsl(var(--cc) 80% 62%)!important}",
      "body.cal-cc .pd-dot[data-course]{background:hsl(var(--cc) 80% 62%)!important}",
      "body.shoug-light-mode.cal-cc [data-course]:not(.pd-dot),html.calendar-light body.cal-cc [data-course]:not(.pd-dot){color:hsl(var(--cc) 65% 32%)!important;background:hsl(var(--cc) 75% 55% / .14)!important}",
      /* phone month */
      ".phone-day{border-top:1px solid var(--line);padding:14px 16px;background:var(--surface)}",
      ".pd-head{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:10px}",
      ".pd-date{font:800 1rem Inter,system-ui,sans-serif;color:var(--text)}.pd-count{font-size:.75rem;color:var(--muted)}",
      ".pd-add{border:1px solid var(--brand);background:none;color:var(--brand);border-radius:999px;padding:7px 14px;font:800 .7rem 'JetBrains Mono',monospace;cursor:pointer}",
      ".pd-list{display:flex;flex-direction:column;gap:8px}",
      ".pd-dots{display:none}",
      "@media (max-width:600px){",
      " .cv-long{display:none}.cv-cc{text-transform:capitalize}",
      " .cal-toolbar{padding:10px 12px;gap:8px}.cv-seg{order:1}.cv-cc{order:2;margin-left:auto}.cv-help{order:3}.cv-quick{order:4}.cv-search{order:5}.cv-quick,.cv-search{flex-basis:100%}",
      " #month-grid .day{min-height:58px;padding:6px 2px}",
      " #month-grid .day-events,#month-grid .range-layer,#month-grid .range-space{display:none!important}",
      " #month-grid .day-num{justify-content:center}#month-grid .day-num span+span{display:none}",
      " #month-grid .pd-dots{display:flex;justify-content:center;flex-wrap:wrap;gap:3px;margin-top:6px}",
      " #month-grid .pd-dot{width:6px;height:6px;border-radius:50%;background:currentColor;display:block}",
      " #month-grid .pd-dot.exam{color:var(--red)}#month-grid .pd-dot.class{color:var(--blue)}#month-grid .pd-dot.study{color:#a3e635}#month-grid .pd-dot.assignment{color:#c084fc}#month-grid .pd-dot.project{color:#f472b6}#month-grid .pd-dot.personal{color:var(--green)}#month-grid .pd-dot.travel{color:var(--teal)}#month-grid .pd-dot.busy{color:var(--amber)}#month-grid .pd-dot.academic{color:var(--purple)}",
      " #month-grid .day.pd-selected .day-num span:first-child{background:var(--brand);color:#0a0514;border-radius:50%;min-width:26px;height:26px;display:inline-flex;align-items:center;justify-content:center}",
      " .month-grid{min-height:0}",
      " .tv{--gut:40px}.tv-dayhead{flex-direction:column;align-items:center;gap:2px;padding:6px 0;font-size:.6rem}.tv-dayhead .tv-num{font-size:.85rem;min-width:24px;height:24px;line-height:24px}",
      " .tv-week .tv-ev-time{display:none}.tv-week .tv-ev{padding:3px 3px}.tv-week .tv-ev-title{font-size:.62rem;white-space:normal}",
      "}",
    ].join("\n");
    var el = document.createElement("style");
    el.id = "cv-styles";
    el.textContent = css;
    document.head.appendChild(el);
  }

  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
