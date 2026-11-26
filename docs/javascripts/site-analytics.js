/**
 * Site analytics for SHOUG.TECH. Added to every page by functions/_middleware.js;
 * the collector is workers/slide-assistant/src/analytics.js and the reports are
 * at /admin/analytics/.
 *
 * What it records: page views, engaged time, scroll depth, quiz answers,
 * searches, outbound links, downloads, button use, frustrated repeat clicks,
 * Core Web Vitals, JavaScript errors, theme/language changes, copy and print.
 *
 * What it never records: cookies, visitor or session IDs, anything typed into
 * a form field other than the site search box, the text people copy.
 *
 * Off switches: Do Not Track, Global Privacy Control, or visiting any page with
 * ?analytics=off (undo with ?analytics=on). ?analytics=debug logs events to the
 * console instead of sending them, on any host.
 */
(function () {
  "use strict";
  if (window.__shougAnalytics) return;
  window.__shougAnalytics = true;

  var ENDPOINT = "https://shoug-tech.shoug-alomran.workers.dev/v1/collect";
  var HOSTS = { "shoug-tech.com": 1, "www.shoug-tech.com": 1 };
  var OPT_OUT = "shoug-analytics-optout";
  var IDLE_MS = 60000;
  var SESSION_GAP_MS = 30 * 60000;

  function store(kind) {
    try {
      return window[kind];
    } catch (e) {
      return null;
    }
  }
  var local = store("localStorage");
  function get(key) {
    try {
      return local ? local.getItem(key) : null;
    } catch (e) {
      return null;
    }
  }
  function set(key, value) {
    try {
      if (local) local.setItem(key, value);
    } catch (e) {}
  }
  function remove(key) {
    try {
      if (local) local.removeItem(key);
    } catch (e) {}
  }

  var params = new URLSearchParams(location.search);
  var mode = params.get("analytics");
  if (mode === "off") set(OPT_OUT, "1");
  if (mode === "on") remove(OPT_OUT);
  var debug = mode === "debug";

  if (!debug) {
    if (!HOSTS[location.hostname]) return;
    if (get(OPT_OUT) === "1") return;
    if (navigator.globalPrivacyControl === true) return;
    if (navigator.doNotTrack === "1" || window.doNotTrack === "1") return;
  }
  if (/^\/admin\//.test(location.pathname)) return;

  // ------------------------------------------------------------- context --
  function today() {
    var d = new Date(Date.now() + 3 * 3600000); // Riyadh calendar day
    return d.toISOString().slice(0, 10);
  }
  function daysBetween(a, b) {
    return Math.round((Date.parse(b) - Date.parse(a)) / 86400000);
  }

  var day = today();
  var firstSeen = get("shoug-a-first");
  var lastDay = get("shoug-a-day");
  var newEver = !firstSeen;
  var newToday = lastDay !== day;
  if (newEver) set("shoug-a-first", day);
  set("shoug-a-day", day);

  // Page number within a visit: shared by tabs, reset after 30 idle minutes.
  var pageIndex = 1;
  try {
    var s = JSON.parse(get("shoug-a-session") || "null");
    if (s && Date.now() - s.t < SESSION_GAP_MS) pageIndex = (s.i || 0) + 1;
  } catch (e) {}
  function touchSession() {
    set("shoug-a-session", JSON.stringify({ i: pageIndex, t: Date.now() }));
  }
  touchSession();

  function themeName() {
    var root = document.documentElement;
    var body = document.body;
    var light =
      root.getAttribute("data-theme") === "light" ||
      (body &&
        (body.classList.contains("shoug-light-mode") ||
          body.classList.contains("light"))) ||
      get("shoug-theme") === "light";
    var palette =
      root.getAttribute("data-site-palette") ||
      get("shoug-palette") ||
      "original";
    return (light ? "light" : "dark") + "/" + palette;
  }

  function siteLanguage() {
    var lang = document.documentElement.getAttribute("lang") || get("shoug-lang") || "en";
    return lang.slice(0, 2).toLowerCase();
  }

  var internalFrom = "";
  var externalReferrer = "";
  try {
    if (document.referrer) {
      var ref = new URL(document.referrer);
      if (HOSTS[ref.hostname] || ref.hostname === location.hostname)
        internalFrom = ref.pathname.replace(/\/index\.html$/, "/");
      else externalReferrer = document.referrer;
    }
  } catch (e) {}

  var isNotFound = /404/.test(document.title) && /not found/i.test(document.title);
  var displayMode =
    window.matchMedia && matchMedia("(display-mode: standalone)").matches
      ? "standalone"
      : /\/offline\.html$/.test(location.pathname)
        ? "offline"
        : "";

  function context() {
    return {
      p: location.pathname,
      t: document.title,
      r: externalReferrer,
      bl: navigator.language || "",
      sl: siteLanguage(),
      th: themeName(),
      si: get("shoug-was-signed-in") === "1" ? 1 : 0,
      us: params.get("utm_source") || params.get("ref") || "",
      um: params.get("utm_medium") || "",
      uc: params.get("utm_campaign") || "",
      vw: window.innerWidth || 0,
      tp: navigator.maxTouchPoints || 0,
      wd: navigator.webdriver ? 1 : 0,
      nv: newEver ? 1 : 0,
      nd: newToday ? 1 : 0,
      ix: pageIndex,
      ds: lastDay ? Math.max(0, daysBetween(lastDay, day)) : -1,
    };
  }

  // --------------------------------------------------------------- queue --
  var queue = [];
  var sentCount = 0;
  var MAX_EVENTS_PER_PAGE = 300;

  function track(name, fields) {
    if (sentCount + queue.length >= MAX_EVENTS_PER_PAGE) return;
    var event = { n: name };
    for (var k in fields) if (fields[k] !== undefined) event[k] = fields[k];
    queue.push(event);
    if (queue.length >= 30) flush();
  }

  function flush() {
    if (!queue.length) return;
    var view = queue[0] && queue[0].n === "pageview" ? queue[0] : null;
    if (view && !view.ms) view.ms = loadMs();
    var batch = queue.splice(0, 40);
    sentCount += batch.length;
    var body = JSON.stringify({ v: 1, c: context(), e: batch });
    if (debug) {
      console.info("[analytics]", JSON.parse(body));
      return;
    }
    var sent = false;
    try {
      // text/plain keeps this a simple CORS request: no preflight.
      sent = navigator.sendBeacon && navigator.sendBeacon(ENDPOINT, new Blob([body], { type: "text/plain" }));
    } catch (e) {}
    if (!sent) {
      try {
        fetch(ENDPOINT, {
          method: "POST",
          body: body,
          keepalive: true,
          mode: "cors",
          credentials: "omit",
          headers: { "content-type": "text/plain" },
        }).catch(function () {});
      } catch (e) {}
    }
  }

  function loadMs() {
    try {
      var nav = performance.getEntriesByType("navigation")[0];
      if (nav && nav.loadEventEnd > 0) return Math.round(nav.loadEventEnd);
    } catch (e) {}
    return 0;
  }

  // ------------------------------------------------------------ pageview --
  track("pageview", {
    l: internalFrom,
    d: isNotFound ? "404" : displayMode,
  });
  if (document.readyState === "complete") setTimeout(flush, 0);
  else
    window.addEventListener("load", function () {
      setTimeout(flush, 0);
    });
  setTimeout(flush, 4000);
  setInterval(flush, 15000);

  // ---------------------------------------------- engaged time & scroll --
  var engagedMs = 0;
  var lastTick = Date.now();
  var lastActive = Date.now();
  var maxScroll = 0;
  var scrollReported = false;
  var quizAnswered = 0;
  var quizCorrect = 0;

  function visible() {
    return document.visibilityState === "visible";
  }
  function tick() {
    var now = Date.now();
    if (visible() && now - lastActive < IDLE_MS) engagedMs += now - lastTick;
    lastTick = now;
  }
  function active() {
    tick();
    lastActive = Date.now();
  }
  ["pointerdown", "keydown", "wheel", "touchstart", "mousemove"].forEach(function (type) {
    window.addEventListener(type, active, { passive: true, capture: true });
  });
  setInterval(tick, 5000);

  function measureScroll() {
    var doc = document.documentElement;
    var height = Math.max(doc.scrollHeight, document.body ? document.body.scrollHeight : 0);
    var seen = (window.scrollY || doc.scrollTop || 0) + window.innerHeight;
    var pct = height <= window.innerHeight ? 100 : Math.round((seen / height) * 100);
    if (pct > maxScroll) maxScroll = Math.min(100, pct);
  }
  var scrollTimer = 0;
  window.addEventListener(
    "scroll",
    function () {
      active();
      if (scrollTimer) return;
      scrollTimer = setTimeout(function () {
        scrollTimer = 0;
        measureScroll();
      }, 250);
    },
    { passive: true },
  );

  function sendEngagement() {
    tick();
    measureScroll();
    var seconds = Math.round(engagedMs / 1000);
    if (!seconds && scrollReported && !quizAnswered) return;
    track("engage", {
      s: seconds,
      sc: scrollReported ? undefined : maxScroll,
      qa: quizAnswered || undefined,
      qc: quizCorrect || undefined,
    });
    scrollReported = true;
    engagedMs = 0;
    quizAnswered = 0;
    quizCorrect = 0;
  }

  // ------------------------------------------------------------- quizzes --
  // quiz-motion.js reports each question's first answer on every exam page.
  var quizTotalAnswered = 0;
  var quizTotalCorrect = 0;
  var quizSubmittedAt = 0;
  document.addEventListener("shoug:quiz-answer", function (event) {
    var ok = !!(event.detail && event.detail.ok);
    quizAnswered++;
    quizTotalAnswered++;
    if (ok) {
      quizCorrect++;
      quizTotalCorrect++;
    }
  });

  // -------------------------------------------------------------- search --
  var searchTimer = 0;
  var lastQuery = "";
  document.addEventListener("shoug:search", function (event) {
    var d = event.detail || {};
    clearTimeout(searchTimer);
    searchTimer = setTimeout(function () {
      var q = String(d.query || "").trim().toLowerCase().slice(0, 80);
      if (q.length < 2 || q === lastQuery) return;
      lastQuery = q;
      track("search", { l: q, v: d.results | 0 });
    }, 1200);
  });

  // ------------------------------------------------------------- clicks --
  var DOWNLOAD = /\.(pdf|docx?|pptx?|xlsx?|zip|rar|ipynb|csv|txt|py|java|sql|png|jpe?g)$/i;
  var CTA = /check|submit|grade|finish|reveal|show (all|answers)|score/i;
  var clickCount = 0;
  var rageTarget = null;
  var rageTimes = [];

  function labelOf(el) {
    var text =
      el.getAttribute("aria-label") ||
      el.getAttribute("title") ||
      el.getAttribute("data-label") ||
      el.textContent ||
      el.value ||
      "";
    text = String(text).replace(/\s+/g, " ").trim();
    if (!text && el.id) text = "#" + el.id;
    return text.slice(0, 80);
  }

  document.addEventListener(
    "click",
    function (event) {
      var el = event.target && event.target.closest && event.target.closest("a, button, [role='button'], summary, input[type='submit']");
      if (!el) return;

      // Several clicks on the same thing within a second: something didn't respond.
      var now = Date.now();
      if (el === rageTarget) {
        rageTimes.push(now);
        rageTimes = rageTimes.filter(function (t) {
          return now - t < 1000;
        });
        if (rageTimes.length === 3) track("rage", { l: labelOf(el) || el.tagName.toLowerCase() });
      } else {
        rageTarget = el;
        rageTimes = [now];
      }

      if (clickCount >= 80) return;
      if (el.tagName === "A") {
        var href = el.getAttribute("href") || "";
        if (/^(mailto|tel):/i.test(href)) {
          clickCount++;
          track("click", { l: href.split("?")[0].slice(0, 120), d: "contact" });
          return;
        }
        var url;
        try {
          url = new URL(href, location.href);
        } catch (e) {
          return;
        }
        if (!/^https?:$/.test(url.protocol)) return;
        if (!HOSTS[url.hostname] && url.hostname !== location.hostname) {
          clickCount++;
          track("click", { l: (url.hostname + url.pathname).slice(0, 160), d: "outbound" });
        } else if (el.hasAttribute("download") || DOWNLOAD.test(url.pathname)) {
          clickCount++;
          track("click", { l: url.pathname.slice(0, 200), d: "download" });
        }
        return;
      }
      var label = labelOf(el);
      if (!label) return;
      clickCount++;
      track("click", { l: label, d: "button" });
      if (CTA.test(label) && quizTotalAnswered > 0) {
        // Let the page grade first, then report the score so far, once per
        // new set of answers (repeat presses of the same button add nothing).
        setTimeout(function () {
          if (quizTotalAnswered === quizSubmittedAt) return;
          quizSubmittedAt = quizTotalAnswered;
          track("quiz", {
            l: label,
            v: Math.round((quizTotalCorrect / quizTotalAnswered) * 100),
            qa: quizTotalAnswered,
            qc: quizTotalCorrect,
          });
        }, 600);
      }
    },
    true,
  );

  // ------------------------------------------------- copy, print, prefs --
  var copies = 0;
  document.addEventListener("copy", function () {
    if (copies++ >= 10) return;
    var sel = String((window.getSelection && window.getSelection()) || "");
    track("copy", { v: sel.length });
  });
  window.addEventListener("beforeprint", function () {
    track("print", {});
  });

  var lastTheme = null;
  var themeTimer = 0;
  function watchTheme() {
    clearTimeout(themeTimer);
    themeTimer = setTimeout(function () {
      var now = themeName();
      if (lastTheme !== null && now !== lastTheme) track("pref", { l: "theme", d: now });
      lastTheme = now;
    }, 400);
  }
  function startThemeWatch() {
    watchTheme();
    var opts = { attributes: true, attributeFilter: ["class", "data-theme", "data-site-palette"] };
    new MutationObserver(watchTheme).observe(document.documentElement, opts);
    if (document.body) new MutationObserver(watchTheme).observe(document.body, opts);
  }
  if (document.body) startThemeWatch();
  else document.addEventListener("DOMContentLoaded", startThemeWatch);

  // arabic-localization.js dispatches this on window.
  window.addEventListener("shoug:language-change", function (event) {
    var lang = (event.detail && (event.detail.lang || event.detail.language)) || siteLanguage();
    track("pref", { l: "language", d: String(lang).slice(0, 10) });
  });

  // ------------------------------------------------------------- errors --
  var errorsSeen = {};
  var errorCount = 0;
  function reportError(message, source) {
    message = String(message || "Unknown error").slice(0, 240);
    if (errorsSeen[message] || errorCount >= 5) return;
    errorsSeen[message] = 1;
    errorCount++;
    track("error", { l: message, d: String(source || "").slice(0, 120) });
  }
  window.addEventListener("error", function (event) {
    if (event.target && event.target !== window && event.target.tagName) {
      var src = event.target.src || event.target.href || "";
      if (src) reportError("Failed to load " + event.target.tagName.toLowerCase(), src.replace(location.origin, ""));
      return;
    }
    var file = String(event.filename || "").replace(location.origin, "").split(/[?#]/)[0];
    reportError(event.message, file ? file + ":" + event.lineno : "");
  }, true);
  window.addEventListener("unhandledrejection", function (event) {
    var r = event.reason;
    reportError("Unhandled promise: " + (r && r.message ? r.message : String(r)), "");
  });

  // ----------------------------------------------------------- web vitals --
  var vitals = {};
  var THRESHOLDS = {
    LCP: [2500, 4000],
    INP: [200, 500],
    CLS: [0.1, 0.25],
    FCP: [1800, 3000],
    TTFB: [800, 1800],
  };
  function observe(type, fn, extra) {
    try {
      var po = new PerformanceObserver(function (list) {
        list.getEntries().forEach(fn);
      });
      var opts = { type: type, buffered: true };
      for (var k in extra) opts[k] = extra[k];
      po.observe(opts);
    } catch (e) {}
  }
  observe("largest-contentful-paint", function (entry) {
    vitals.LCP = entry.startTime;
  });
  observe("paint", function (entry) {
    if (entry.name === "first-contentful-paint") vitals.FCP = entry.startTime;
  });
  // CLS: the largest burst of shifts (gaps under 1s, at most 5s long).
  var clsWindow = 0;
  var clsFirst = 0;
  var clsLast = 0;
  observe("layout-shift", function (entry) {
    if (entry.hadRecentInput) return;
    if (clsWindow && entry.startTime - clsLast < 1000 && entry.startTime - clsFirst < 5000) {
      clsWindow += entry.value;
    } else {
      clsWindow = entry.value;
      clsFirst = entry.startTime;
    }
    clsLast = entry.startTime;
    vitals.CLS = Math.max(vitals.CLS || 0, clsWindow);
  });
  // INP: the slowest interaction (exact for pages with under 50 interactions).
  observe(
    "event",
    function (entry) {
      if (!entry.interactionId) return;
      vitals.INP = Math.max(vitals.INP || 0, entry.duration);
    },
    { durationThreshold: 40 },
  );
  try {
    var nav = performance.getEntriesByType("navigation")[0];
    if (nav && nav.responseStart > 0) vitals.TTFB = nav.responseStart;
  } catch (e) {}

  var vitalsSent = false;
  function sendVitals() {
    if (vitalsSent) return;
    vitalsSent = true;
    Object.keys(vitals).forEach(function (name) {
      var value = vitals[name];
      if (typeof value !== "number" || !isFinite(value)) return;
      var t = THRESHOLDS[name];
      var rating = value <= t[0] ? "good" : value <= t[1] ? "needs-improvement" : "poor";
      track("vital", {
        l: name,
        v: name === "CLS" ? Math.round(value * 1000) / 1000 : Math.round(value),
        d: rating,
      });
    });
  }

  // --------------------------------------------------------------- leave --
  function onHide() {
    touchSession();
    sendEngagement();
    sendVitals();
    flush();
  }
  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "hidden") onHide();
    else {
      lastTick = Date.now();
      lastActive = Date.now();
    }
  });
  window.addEventListener("pagehide", onHide);

  // A small API for page scripts: window.shougTrack("click", { l: "label" }).
  window.shougTrack = function (name, fields) {
    if (typeof name === "string") track(name, fields || {});
  };
})();
