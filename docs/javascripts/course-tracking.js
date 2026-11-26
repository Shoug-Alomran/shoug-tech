/**
 * Paid course tracking and student tools (Ethics, ETHCS303).
 *
 * Loaded on paid course pages by site-palette.js, which every course page
 * includes and the Pages site serves (the pages themselves come from the
 * course-access Worker). For a signed-in buyer whose payment was approved it:
 *
 *  - records lesson views (per day), video watch time and furthest point,
 *  - records quiz answers per question (from quiz-motion.js),
 *  - adds "Was this lesson helpful?" buttons to lesson pages,
 *  - shows upcoming sessions and bookable office-hour slots on the course home.
 *
 * Everything goes to courseProgress/ethics/students/{uid}, which only the
 * student and the course administrator can read (see firebase/firestore.rules
 * and the privacy notice). Nothing is recorded for anyone else.
 */
(function () {
  "use strict";
  if (window.__shougCourseTracking) return;
  window.__shougCourseTracking = true;

  var COURSE = "ethics";
  var BASE = "/academics/other-courses/ethcs303";
  var path = location.pathname;
  if (path.indexOf(BASE) !== 0) return;

  var FB_BASE = "https://www.gstatic.com/firebasejs/10.12.0/firebase-";
  var FB_CONFIG = {
    apiKey: "AIzaSyDUklr3u8laDZH2jhHVAO3BPE12GaPpOmI",
    authDomain: "shoug-tech.firebaseapp.com",
    projectId: "shoug-tech",
    storageBucket: "shoug-tech.firebasestorage.app",
    messagingSenderId: "621041999813",
    appId: "1:621041999813:web:8982befd8b0ccc1d9475ac",
  };

  // ------------------------------------------------------------- lesson key --
  var rest = path.slice(BASE.length).replace(/index\.html$/, "").replace(/\.html$/, "");
  var parts = rest.split("/").filter(Boolean);
  var KEY = parts.length ? parts.join("~").toLowerCase().replace(/[^a-z0-9~_-]/g, "-").slice(0, 140) : "home";
  var SECTION = parts[0] || "home";
  // The page address as firebase-auth.js keys page comments (pageComments/{slug}).
  var PATH = path.replace(/index\.html$/, "").slice(0, 300);
  var TITLE = document.title.replace(/^SHOUG\.TECH\s*(\||\/\/|-)\s*/i, "").replace(/\s*[|·—-]\s*SHOUG\.TECH.*$/i, "").slice(0, 140);
  var IS_QUIZ = SECTION === "exams" && parts.length > 1;
  // Pages people learn from (not listings): one level below a section.
  var IS_LESSON = !IS_QUIZ && parts.length >= 2;
  var IS_HOME = parts.length === 0;

  function riyadhDay(d) {
    var t = new Date((d ? d.getTime() : Date.now()) + 3 * 3600000);
    return t.toISOString().slice(0, 10).replace(/-/g, "");
  }

  // ------------------------------------------------------------- firebase --
  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement("script");
      s.src = src;
      s.onload = resolve;
      s.onerror = reject;
      document.head.appendChild(s);
    });
  }

  // Reuse the site's Firebase when the page has it; never load the SDK twice.
  function firebaseReady() {
    return new Promise(function (resolve) {
      if (window.__shoug_fb) return resolve(window.__shoug_fb);
      var hasLoader =
        document.querySelector('script[src*="firebase-auth.js"]') ||
        typeof window.__shougLoadFirebaseAuth === "function";
      if (hasLoader) {
        window.addEventListener("shoug:fb", function () { resolve(window.__shoug_fb); }, { once: true });
        if (typeof window.__shougLoadFirebaseAuth === "function") window.__shougLoadFirebaseAuth(false);
        return;
      }
      if (window.firebase && window.firebase.apps) {
        if (!window.firebase.apps.length) window.firebase.initializeApp(FB_CONFIG);
        return resolve(window.firebase);
      }
      loadScript(FB_BASE + "app-compat.js")
        .then(function () {
          return Promise.all([loadScript(FB_BASE + "auth-compat.js"), loadScript(FB_BASE + "firestore-compat.js")]);
        })
        .then(function () {
          if (!window.firebase.apps.length) window.firebase.initializeApp(FB_CONFIG);
          resolve(window.firebase);
        })
        .catch(function () {});
    });
  }

  var fb, db, user, ref, record = null, ready = false;
  var inc = function (n) { return fb.firestore.FieldValue.increment(n); };
  var now = function () { return fb.firestore.FieldValue.serverTimestamp(); };

  function save(patch) {
    if (!ready) return Promise.resolve();
    patch.lastSeenAt = now();
    return ref.set(patch, { merge: true }).catch(function (error) {
      if (window.console) console.warn("Course progress not saved", error && error.code);
    });
  }

  function lessonPatch(fields) {
    var lessons = {};
    lessons[KEY] = Object.assign({ title: TITLE, section: SECTION, path: PATH }, fields);
    return { lessons: lessons };
  }

  function quizPatch(fields) {
    var quizzes = {};
    quizzes[KEY] = Object.assign({ title: TITLE, path: PATH }, fields);
    return { quizzes: quizzes };
  }

  function start(firebase) {
    fb = firebase;
    db = fb.firestore();
    fb.auth().onAuthStateChanged(function (u) {
      if (!u || ready) return;
      user = u;
      db.collection("courseTransfers").doc(u.uid).get()
        .then(function (snap) {
          if (!snap.exists || snap.data().status !== "approved") return null;
          ref = db.collection("courseProgress").doc(COURSE).collection("students").doc(u.uid);
          return ref.get().then(function (doc) {
            if (doc.exists) {
              record = doc.data();
              return;
            }
            record = { lessons: {}, quizzes: {} };
            return ref.set({ uid: u.uid, lessons: {}, quizzes: {}, firstSeenAt: now(), lastSeenAt: now() });
          });
        })
        .then(function () {
          if (!ref) return;
          ready = true;
          onReady();
        })
        .catch(function () {});
    });
  }

  // ---------------------------------------------------------------- views --
  function onReady() {
    var days = {};
    days[riyadhDay()] = inc(1);
    save(lessonPatch({ views: inc(1), days: days, lastAt: now(), kind: IS_QUIZ ? "quiz" : IS_LESSON ? "lesson" : "page" }));
    watchVideos();
    if (IS_LESSON) addReactions();
    if (IS_HOME) addSessions();
  }

  // ---------------------------------------------------------------- video --
  var watched = 0;
  var pendingWatch = 0;
  var furthest = 0;
  var duration = 0;
  function watchVideos() {
    var videos = document.querySelectorAll("video");
    if (!videos.length) return;
    var prev = (record.lessons && record.lessons[KEY]) || {};
    furthest = Number(prev.maxPct) || 0;
    var last = new WeakMap();
    videos.forEach(function (v) {
      v.addEventListener("timeupdate", function () {
        var t = v.currentTime;
        var before = last.get(v);
        last.set(v, t);
        if (v.paused || before === undefined) return;
        var step = t - before;
        if (step > 0 && step < 2) {
          watched += step;
          pendingWatch += step;
        }
        if (v.duration && isFinite(v.duration)) {
          duration = v.duration;
          furthest = Math.max(furthest, Math.min(100, Math.round((t / v.duration) * 100)));
        }
      });
      v.addEventListener("seeking", function () { last.delete(v); });
      v.addEventListener("ended", flushWatch);
    });
    setInterval(flushWatch, 30000);
  }
  function flushWatch() {
    if (pendingWatch < 1) return;
    var secs = Math.round(pendingWatch);
    pendingWatch = 0;
    save(lessonPatch({ watchSeconds: inc(secs), maxPct: furthest, duration: Math.round(duration) }));
  }

  // ---------------------------------------------------------------- quiz --
  var quizAnswered = 0, quizCorrect = 0, attemptCounted = false;
  var wrongQueue = {};
  function hash(text) {
    var h = 0;
    for (var i = 0; i < text.length; i++) h = (h * 31 + text.charCodeAt(i)) | 0;
    return "q" + (h >>> 0).toString(36);
  }
  document.addEventListener("shoug:quiz-answer", function (event) {
    if (!IS_QUIZ) return;
    var d = event.detail || {};
    quizAnswered++;
    if (d.ok) quizCorrect++;
    var patch = { answered: inc(1), correct: inc(d.ok ? 1 : 0), lastAt: now() };
    if (!attemptCounted) {
      attemptCounted = true;
      patch.attempts = inc(1);
    }
    // Every question keeps two counters; its text is stored only once someone
    // gets it wrong, which keeps large question banks well under 1 MB.
    var text = String(d.text || "").replace(/\s+/g, " ").trim().slice(0, 160);
    if (text) {
      var entry = { seen: inc(1), wrong: inc(d.ok ? 0 : 1) };
      if (!d.ok) entry.text = text;
      var questions = {};
      questions[hash(text)] = entry;
      patch.questions = questions;
    }
    save(quizPatch(patch));
  });
  function flushQuiz() {
    if (!quizAnswered) return;
    var prev = (record.quizzes && record.quizzes[KEY]) || {};
    var score = Math.round((quizCorrect / quizAnswered) * 100);
    save(quizPatch({ lastScore: score, best: Math.max(score, Number(prev.best) || 0), lastAnswered: quizAnswered }));
  }

  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "hidden") {
      flushWatch();
      flushQuiz();
    }
  });
  window.addEventListener("pagehide", function () {
    flushWatch();
    flushQuiz();
  });

  // ------------------------------------------------------------ reactions --
  function addReactions() {
    if (document.getElementById("ct-react")) return;
    var current = Number((record.lessons[KEY] || {}).reaction) || 0;
    var box = document.createElement("aside");
    box.id = "ct-react";
    box.className = "ct-react";
    box.setAttribute("aria-label", "Lesson feedback");
    var label = document.createElement("span");
    label.textContent = "Was this lesson helpful?";
    label.setAttribute("data-ar-text", "هل كان هذا الدرس مفيدًا؟");
    box.appendChild(label);
    function button(value, text, title) {
      var b = document.createElement("button");
      b.type = "button";
      b.textContent = text;
      b.title = title;
      b.setAttribute("aria-label", title);
      b.setAttribute("aria-pressed", String(current === value));
      b.addEventListener("click", function () {
        current = current === value ? 0 : value;
        box.querySelectorAll("button").forEach(function (x) {
          x.setAttribute("aria-pressed", String(Number(x.dataset.v) === current));
        });
        record.lessons[KEY] = Object.assign({}, record.lessons[KEY], { reaction: current });
        save(lessonPatch({ reaction: current }));
      });
      b.dataset.v = value;
      return b;
    }
    box.appendChild(button(1, "👍", "Helpful"));
    box.appendChild(button(-1, "👎", "Not helpful"));
    document.body.appendChild(box);
    injectStyles();
  }

  // ------------------------------------------------------------- sessions --
  function fmt(ts) {
    var d = ts && ts.toDate ? ts.toDate() : new Date(ts);
    return d.toLocaleString("en-GB", { weekday: "short", day: "numeric", month: "short", hour: "2-digit", minute: "2-digit", timeZone: "Asia/Riyadh" });
  }
  var TYPE = { live: "Live session", office: "Office hours", academic: "Academic date" };

  function addSessions() {
    var now = new Date();
    Promise.all([
      // One range filter each, so no composite index is needed; course is checked below.
      db.collection("courseEvents").where("end", ">=", now).get(),
      db.collection("courseSlots").where("start", ">=", now).get(),
      db.collection("courseBookings").where("uid", "==", user.uid).get(),
    ])
      .then(function (r) {
        var mineCourse = function (x) { return x.course === COURSE; };
        var events = r[0].docs.map(function (d) { return Object.assign({ id: d.id }, d.data()); }).filter(mineCourse)
          .sort(function (a, b) { return a.start.toMillis() - b.start.toMillis(); });
        var slots = r[1].docs.map(function (d) { return Object.assign({ id: d.id }, d.data()); }).filter(mineCourse)
          .sort(function (a, b) { return a.start.toMillis() - b.start.toMillis(); });
        var mine = {};
        r[2].forEach(function (d) { mine[d.id] = true; });
        if (!events.length && !slots.length) return;
        renderSessions(events, slots, mine);
      })
      .catch(function () {});
  }

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text !== undefined) n.textContent = text;
    return n;
  }

  function renderSessions(events, slots, mine) {
    injectStyles();
    var card = el("section", "ct-sessions");
    card.setAttribute("aria-label", "Sessions and office hours");
    card.appendChild(el("h2", "", "Sessions & office hours"));
    if (events.length) {
      var list = el("ul", "ct-list");
      events.slice(0, 6).forEach(function (e) {
        var li = el("li");
        li.appendChild(el("strong", "", e.title));
        li.appendChild(el("span", "ct-meta", (TYPE[e.type] || "Event") + " · " + fmt(e.start)));
        if (e.link && /^https:\/\//.test(e.link)) {
          var a = el("a", "", "Join link");
          a.href = e.link;
          a.target = "_blank";
          a.rel = "noopener";
          li.appendChild(a);
        }
        list.appendChild(li);
      });
      card.appendChild(list);
    }
    if (slots.length) {
      card.appendChild(el("h3", "", "Book a one-to-one slot"));
      var grid = el("div", "ct-slots");
      slots.slice(0, 12).forEach(function (s) {
        var b = el("button", "ct-slot");
        b.type = "button";
        var state = mine[s.id] ? "mine" : "unknown";
        function paint() {
          b.textContent = fmt(s.start) + (state === "mine" ? " · Booked (cancel)" : state === "taken" ? " · Taken" : "");
          b.disabled = state === "taken";
          b.classList.toggle("is-mine", state === "mine");
        }
        if (state !== "mine")
          db.collection("courseBookings").doc(s.id).get()
            .then(function (d) { state = d.exists ? "taken" : "free"; paint(); })
            .catch(function () { state = "taken"; paint(); });
        b.addEventListener("click", function () {
          var doc = db.collection("courseBookings").doc(s.id);
          if (state === "mine") {
            if (!confirm("Cancel this booking?")) return;
            doc.delete().then(function () { state = "free"; paint(); });
            return;
          }
          var note = prompt("Booking " + fmt(s.start) + ". Anything you'd like to cover? (optional)") ;
          if (note === null) return;
          doc.set({ slotId: s.id, uid: user.uid, name: (user.displayName || user.email || "").slice(0, 120), note: String(note).slice(0, 500), createdAt: fb.firestore.FieldValue.serverTimestamp() })
            .then(function () { state = "mine"; paint(); })
            .catch(function () { state = "taken"; paint(); alert("Someone just booked that slot. Pick another one."); });
        });
        paint();
        grid.appendChild(b);
      });
      card.appendChild(grid);
    }
    var host = document.querySelector("main") || document.body;
    host.insertBefore(card, host.firstElementChild ? host.firstElementChild.nextSibling : null);
  }

  // --------------------------------------------------------------- styles --
  var styled = false;
  function injectStyles() {
    if (styled) return;
    styled = true;
    var css = document.createElement("style");
    css.textContent =
      ".ct-react{position:fixed;left:16px;bottom:16px;z-index:900;display:flex;align-items:center;gap:8px;padding:8px 12px;border-radius:999px;background:rgba(19,19,27,.92);border:1px solid rgba(255,255,255,.12);color:#eee;font:14px/1.2 system-ui,sans-serif;box-shadow:0 6px 20px rgba(0,0,0,.3)}" +
      ".ct-react button{font-size:18px;line-height:1;padding:6px 8px;border-radius:999px;border:1px solid transparent;background:transparent;cursor:pointer}" +
      ".ct-react button[aria-pressed=true]{border-color:#ff2e2e;background:rgba(255,46,46,.15)}" +
      ".ct-sessions{margin:24px auto;max-width:960px;padding:18px 20px;border:1px solid rgba(255,255,255,.12);border-radius:14px;background:rgba(19,19,27,.85);color:#eee;font-family:system-ui,sans-serif}" +
      ".ct-sessions h2{margin:0 0 10px;font-size:18px}.ct-sessions h3{margin:16px 0 8px;font-size:15px}" +
      ".ct-list{list-style:none;margin:0;padding:0;display:grid;gap:8px}.ct-list li{display:flex;flex-wrap:wrap;gap:4px 12px;align-items:baseline}" +
      ".ct-meta{color:#a3a3b2;font-size:13px}.ct-list a{color:#6aabf1}" +
      ".ct-slots{display:flex;flex-wrap:wrap;gap:8px}.ct-slot{font:inherit;font-size:13px;padding:8px 12px;border-radius:9px;border:1px solid rgba(255,255,255,.18);background:#1b1b26;color:#eee;cursor:pointer}" +
      ".ct-slot.is-mine{border-color:#0aac23}.ct-slot:disabled{opacity:.45;cursor:default}" +
      "html[data-theme=light] .ct-react,html[data-theme=light] .ct-sessions,body.shoug-light-mode .ct-react,body.shoug-light-mode .ct-sessions{background:#fff;color:#191919;border-color:rgba(0,0,0,.12)}" +
      "html[data-theme=light] .ct-slot,body.shoug-light-mode .ct-slot{background:#f1f0f6;color:#191919}";
    document.head.appendChild(css);
  }

  function boot() {
    firebaseReady().then(start);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
