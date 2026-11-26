/* Study tools for Annotated Slides (installed by scripts/install_annotated_study.py).

   One file, three places:
   - a deck page (body[data-deck]): remembers every pick-an-answer result, shows a score,
     "next unanswered", a quiz-only mode, calculation drills, keyboard shortcuts, a reading
     progress bar and an "on the final" badge;
   - the review page (body[data-study="review"]): mistakes, unanswered and random practice
     across all decks, plus every drill;
   - the course Slides page (script[data-study-hub]): score and final badges on deck tiles.

   Answers live in localStorage ("shoug-study-<course>") and, for someone signed in, in their
   private userProgress/{uid} document under study.<course>.<deck>.<question id> = [result, time],
   where result 1 = right on the first try and 0 = missed. The newest entry wins when merging. */
(function () {
  "use strict";
  if (window.__annStudy) return;
  window.__annStudy = true;

  var body = document.body;
  var hubTag = document.querySelector("script[data-study-hub]");
  var MODE = body.getAttribute("data-deck")
    ? "deck"
    : body.getAttribute("data-study") === "review"
      ? "review"
      : hubTag
        ? "hub"
        : "";
  if (!MODE) return;
  var COURSE =
    body.getAttribute("data-course") ||
    (hubTag && hubTag.getAttribute("data-study-hub")) ||
    "course";
  var LS_KEY = "shoug-study-" + COURSE;
  var LETTERS = "ABCDEFGH";

  /* ------------------------------------------------------------- helpers */
  function el(tag, attrs, kids) {
    var n = document.createElement(tag);
    if (attrs)
      Object.keys(attrs).forEach(function (k) {
        if (k === "text") n.textContent = attrs[k];
        else if (k === "html") n.innerHTML = attrs[k];
        else if (k === "on")
          Object.keys(attrs.on).forEach(function (e) {
            n.addEventListener(e, attrs.on[e]);
          });
        else if (attrs[k] !== null && attrs[k] !== undefined && attrs[k] !== false)
          n.setAttribute(k, attrs[k] === true ? "" : attrs[k]);
      });
    (kids || []).forEach(function (c) {
      if (c == null) return;
      n.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
    });
    return n;
  }
  function lsGet(k) {
    try {
      return localStorage.getItem(k);
    } catch (e) {
      return null;
    }
  }
  function lsSet(k, v) {
    try {
      localStorage.setItem(k, v);
    } catch (e) {}
  }
  function shuffle(a) {
    a = a.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1)),
        t = a[i];
      a[i] = a[j];
      a[j] = t;
    }
    return a;
  }
  function rnd(lo, hi) {
    return lo + Math.floor(Math.random() * (hi - lo + 1));
  }
  function pick(a) {
    return a[Math.floor(Math.random() * a.length)];
  }
  function fmt(x, d) {
    var s = (+x).toFixed(d === undefined ? 2 : d);
    return s.indexOf(".") >= 0 ? s.replace(/0+$/, "").replace(/\.$/, "") : s;
  }
  function typing(t) {
    t = t || {};
    return /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName) || t.isContentEditable;
  }

  /* --------------------------------------------------------------- store */
  var data = {};
  try {
    data = JSON.parse(lsGet(LS_KEY) || "{}") || {};
  } catch (e) {
    data = {};
  }
  var listeners = [];
  function changed() {
    lsSet(LS_KEY, JSON.stringify(data));
    listeners.forEach(function (f) {
      try {
        f();
      } catch (e) {}
    });
  }
  function result(deck, qid) {
    var e = data[deck] && data[deck][qid];
    return e ? e[0] : null;
  }
  function record(deck, qid, r) {
    data[deck] = data[deck] || {};
    var entry = [r ? 1 : 0, Date.now()];
    data[deck][qid] = entry;
    changed();
    Sync.push(deck, qid, entry);
  }
  function resetDeck(deck) {
    delete data[deck];
    changed();
    Sync.clear(deck);
  }
  // Merges another copy in; true when ours had something newer the other side lacks.
  function merge(other) {
    var oursNewer = false;
    Object.keys(other || {}).forEach(function (deck) {
      var od = other[deck] || {};
      data[deck] = data[deck] || {};
      Object.keys(od).forEach(function (q) {
        var a = data[deck][q],
          b = od[q];
        if (!b || !b.length) return;
        if (!a || (b[1] || 0) > (a[1] || 0)) data[deck][q] = [b[0], b[1]];
      });
    });
    Object.keys(data).forEach(function (deck) {
      Object.keys(data[deck]).forEach(function (q) {
        var b = other && other[deck] && other[deck][q];
        if (!b || (data[deck][q][1] || 0) > (b[1] || 0)) oursNewer = true;
      });
    });
    return oursNewer;
  }
  function deckStats(deck, ids) {
    var d = data[deck] || {},
      s = { answered: 0, right: 0, missed: 0, total: ids ? ids.length : 0 };
    (ids || Object.keys(d)).forEach(function (q) {
      if (!d[q]) return;
      s.answered++;
      if (d[q][0]) s.right++;
      else s.missed++;
    });
    if (!ids) s.total = s.answered;
    return s;
  }

  /* ---------------------------------------------------------------- sync */
  var Sync = (function () {
    var rootWindow = window;
    try {
      if (window.top !== window.self && window.top.location.href)
        rootWindow = window.top;
    } catch (e) {}
    var FB_BASE = "https://www.gstatic.com/firebasejs/10.12.0/firebase-";
    var FB_CONFIG = {
      apiKey: "AIzaSyDUklr3u8laDZH2jhHVAO3BPE12GaPpOmI",
      authDomain: "shoug-tech.firebaseapp.com",
      projectId: "shoug-tech",
      storageBucket: "shoug-tech.firebasestorage.app",
      messagingSenderId: "621041999813",
      appId: "1:621041999813:web:8982befd8b0ccc1d9475ac",
    };
    var fb = null,
      user = null,
      ref = null,
      state = "local",
      queue = {},
      clears = [],
      timer = null,
      own = false;

    function ready() {
      var wins = rootWindow === window ? [window] : [rootWindow, window];
      for (var i = 0; i < wins.length; i++) {
        try {
          var c = wins[i].__shoug_fb || wins[i].firebase;
          if (c && c.apps && c.apps.length && c.auth && c.firestore) return c;
        } catch (e) {}
      }
      return null;
    }
    function script(src, done, fail) {
      var s = document.createElement("script");
      s.src = src;
      s.async = true;
      s.onload = done;
      s.onerror = fail;
      document.head.appendChild(s);
    }
    function loadOwn() {
      if (own) return;
      own = true;
      script(
        FB_BASE + "app-compat.js",
        function () {
          var left = 2;
          function done() {
            if (--left) return;
            try {
              if (!window.firebase.apps.length)
                window.firebase.initializeApp(FB_CONFIG);
              window.__shoug_fb = window.firebase;
              window.dispatchEvent(new CustomEvent("shoug:fb"));
            } catch (e) {}
          }
          script(FB_BASE + "auth-compat.js", done, function () {});
          script(FB_BASE + "firestore-compat.js", done, function () {});
        },
        function () {},
      );
    }
    function setState(s) {
      state = s;
      changed();
    }
    function flush() {
      timer = null;
      if (!ref) return;
      var study = {},
        payload = { study: study };
      study[COURSE] = queue;
      clears.forEach(function (deck) {
        queue[deck] = fb.firestore.FieldValue.delete();
      });
      queue = {};
      clears = [];
      ref.set(payload, { merge: true }).catch(function () {
        setState("error");
      });
    }
    function schedule() {
      if (ref && !timer) timer = setTimeout(flush, 1200);
    }
    function attach() {
      if (fb) return true;
      var c = ready();
      if (!c) return false;
      fb = c;
      fb.auth().onAuthStateChanged(function (u) {
        user = u;
        ref = null;
        if (!u) {
          setState("signed-out");
          return;
        }
        setState("syncing");
        var r = fb.firestore().collection("userProgress").doc(u.uid);
        r.get()
          .then(function (snap) {
            var d = (snap.exists && snap.data()) || {};
            var remote = (d.study && d.study[COURSE]) || {};
            var push = merge(remote);
            ref = r;
            if (push) {
              Object.keys(data).forEach(function (deck) {
                queue[deck] = data[deck];
              });
              flush();
            }
            setState("synced");
          })
          .catch(function () {
            setState("error");
          });
      });
      return true;
    }
    function start() {
      if (attach()) return;
      try {
        rootWindow.addEventListener("shoug:fb", attach);
        if (rootWindow !== window) window.addEventListener("shoug:fb", attach);
      } catch (e) {}
      var tries = 0,
        poll = setInterval(function () {
          if (attach() || ++tries > 60) clearInterval(poll);
        }, 500);
      // Only someone who has signed in on this site before gets the account loaded.
      if (lsGet("shoug-account-activated") !== "true") return;
      var loader = null;
      try {
        loader = rootWindow.__shougLoadFirebaseAuth;
      } catch (e) {}
      if (typeof loader === "function") {
        try {
          loader(false);
        } catch (e) {}
      } else if (!ready()) loadOwn();
    }
    return {
      start: start,
      state: function () {
        return state;
      },
      push: function (deck, qid, entry) {
        queue[deck] = queue[deck] || {};
        if (typeof queue[deck] === "object") queue[deck][qid] = entry;
        schedule();
      },
      clear: function (deck) {
        delete queue[deck];
        clears.push(deck);
        schedule();
      },
    };
  })();

  function syncText() {
    var s = Sync.state();
    return s === "synced"
      ? "Saved to your account"
      : s === "syncing"
        ? "Syncing with your account…"
        : s === "error"
          ? "Saved in this browser (account sync failed)"
          : "Saved in this browser. Sign in to keep it on every device.";
  }

  /* --------------------------------------------------------------- style */
  var CSS = [
    ":root{--ss-good:#2e9e62;--ss-bad:#d9534f}",
    ".ss-bar{position:fixed;left:0;top:0;height:3px;width:0;background:var(--accent);z-index:60;transition:width .15s linear;pointer-events:none}",
    ".ss-final{display:inline-block;margin-top:3px;padding:1px 8px;border-radius:999px;font-size:11.5px;font-weight:700;letter-spacing:.02em;border:1px solid}",
    ".ss-final.on{color:var(--past);background:var(--past-bg);border-color:color-mix(in srgb,var(--past) 40%,transparent)}",
    ".ss-final.off{color:var(--trap);background:color-mix(in srgb,var(--trap) 10%,var(--panel));border-color:color-mix(in srgb,var(--trap) 40%,transparent)}",
    ".ss-scorewrap{position:relative;display:inline-flex}",
    ".ss-panel{position:absolute;z-index:70;top:calc(100% + 6px);right:0;width:min(330px,calc(100vw - 24px));background:var(--panel);color:var(--ink);border:1px solid var(--line);border-radius:12px;box-shadow:0 14px 36px rgba(0,0,0,.22);padding:14px;font-size:14px;text-align:left}",
    ".ss-panel[hidden]{display:none}",
    ".ss-panel h4{margin:0 0 8px;font-size:15px}",
    ".ss-meter{height:8px;border-radius:99px;background:var(--line);overflow:hidden;display:flex;margin:6px 0 8px}",
    ".ss-meter i{display:block;height:100%}",
    ".ss-meter .g{background:var(--ss-good)}.ss-meter .b{background:var(--ss-bad)}",
    ".ss-nums{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin:0 0 10px;text-align:center}",
    ".ss-nums b{display:block;font-size:18px}.ss-nums span{font-size:12px;color:var(--muted)}",
    ".ss-acts{display:grid;gap:6px}",
    ".ss-acts button,.ss-acts a{width:100%;text-align:left;border-radius:8px}",
    ".ss-muted{color:var(--muted);font-size:12.5px;margin:10px 0 0}",
    ".ss-chip{margin-left:auto;font-size:12px;font-weight:700;padding:1px 8px;border-radius:999px;border:1px solid var(--line);color:var(--muted);white-space:nowrap}",
    ".q header{display:flex;align-items:center;gap:6px;flex-wrap:wrap}",
    ".ss-chip.good{color:var(--ss-good);border-color:color-mix(in srgb,var(--ss-good) 45%,transparent)}",
    ".ss-chip.bad{color:var(--ss-bad);border-color:color-mix(in srgb,var(--ss-bad) 45%,transparent)}",
    ".q.ss-flash{outline:3px solid var(--accent);outline-offset:4px;border-radius:8px;transition:outline-color .6s}",
    ".q.ss-active .picks{box-shadow:-3px 0 0 var(--accent);}",
    "details.ss-explain{margin-top:16px;border:1px solid var(--line);border-left:3px solid var(--trick);border-radius:8px;padding:0 14px}",
    "details.ss-explain>summary{cursor:pointer;font-weight:700;padding:10px 0;list-style-position:inside}",
    "details.ss-explain[open]>summary{border-bottom:1px solid var(--line);margin-bottom:8px}",
    "details.ss-explain p{margin:0 0 8px;font-size:15px}",
    "details.ss-explain p b{display:block;font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted)}",
    "details.ss-explain p.trap b{color:var(--trap)}",
    ".ss-drill{margin:14px 16px 16px;padding:14px;border:1px dashed var(--accent);border-radius:10px;background:color-mix(in srgb,var(--accent) 5%,var(--panel))}",
    ".ss-drill h4{margin:0 0 4px;font-size:15px}",
    ".ss-drill .ss-given{margin:0 0 10px;font-size:15px}",
    ".ss-drill label{display:flex;flex-wrap:wrap;align-items:center;gap:6px 10px;margin:6px 0;font-size:14.5px}",
    ".ss-drill label span{min-width:150px}",
    ".ss-drill input{font:inherit;font-size:16px;width:150px;padding:5px 8px;border:1px solid var(--line);border-radius:8px;background:var(--panel);color:var(--ink)}",
    ".ss-drill input.good{border-color:var(--ss-good)}.ss-drill input.bad{border-color:var(--ss-bad)}",
    ".ss-drill .ss-mark{font-weight:700;font-size:13.5px}",
    ".ss-drill .ss-mark.good{color:var(--ss-good)}.ss-drill .ss-mark.bad{color:var(--ss-bad)}",
    ".ss-drill .ss-row{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}",
    ".ss-drill ol.ss-steps{margin:10px 0 0;padding-left:20px;font-size:14.5px}",
    ".ss-drill ol.ss-steps[hidden]{display:none}",
    ".ss-drill .ss-tip{font-size:12.5px;color:var(--muted);margin:8px 0 0}",
    ".ss-quiz{position:fixed;inset:0;z-index:90;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(6px);overflow:auto;padding:24px 16px}",
    ".ss-quiz .ss-box{max-width:720px;margin:0 auto;background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:20px;box-shadow:0 18px 50px rgba(0,0,0,.2)}",
    ".ss-quiz .ss-top{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:12px}",
    ".ss-quiz .ss-top strong{flex:1}",
    ".ss-quiz .ss-prog{height:6px;border-radius:99px;background:var(--line);overflow:hidden;margin-bottom:14px}",
    ".ss-quiz .ss-prog i{display:block;height:100%;background:var(--accent)}",
    ".ss-quiz .ss-src{font-size:12.5px;color:var(--muted);margin:0 0 4px}",
    ".ss-quiz .ss-qp{font-size:17px;font-weight:600;margin:0 0 12px}",
    ".ss-quiz ol{list-style:none;margin:0;padding:0;display:grid;gap:8px}",
    ".ss-quiz .ss-opt{display:flex;gap:10px;width:100%;text-align:left;border-radius:8px;font-size:15px;font-weight:500;padding:9px 12px}",
    ".ss-quiz .ss-opt b{color:var(--muted)}",
    ".ss-quiz .ss-opt.right{border-color:var(--ss-good);background:color-mix(in srgb,var(--ss-good) 14%,var(--panel))}",
    ".ss-quiz .ss-opt.wrong{border-color:var(--ss-bad);background:color-mix(in srgb,var(--ss-bad) 12%,var(--panel))}",
    ".ss-quiz .ss-why{font-size:14px;margin:4px 0 2px 12px;padding-left:10px;border-left:2px solid var(--line)}",
    ".ss-quiz .ss-verdict{font-weight:700;margin:12px 0 0;min-height:1.4em}",
    ".ss-quiz .ss-verdict.good{color:var(--ss-good)}.ss-quiz .ss-verdict.bad{color:var(--ss-bad)}",
    ".ss-quiz .ss-foot{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px;align-items:center}",
    ".ss-quiz .ss-foot .ss-grow{flex:1;font-size:12.5px;color:var(--muted)}",
    ".ss-quiz .ss-big{font-size:42px;font-weight:800;margin:4px 0}",
    ".ss-quiz .ss-pickn{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0}",
    ".ss-help{position:fixed;z-index:95;right:16px;bottom:16px;width:min(320px,calc(100vw - 32px));background:var(--panel);color:var(--ink);border:1px solid var(--line);border-radius:12px;box-shadow:0 14px 36px rgba(0,0,0,.25);padding:14px 16px;font-size:14px}",
    ".ss-help table{width:100%;border-collapse:collapse}.ss-help td{padding:3px 0;vertical-align:top}",
    ".ss-help kbd{font:600 12px 'JetBrains Mono',monospace;border:1px solid var(--line);border-bottom-width:2px;border-radius:5px;padding:1px 6px;background:var(--code)}",
    // Render slides only when they come near the screen: big decks open much faster.
    "body:not(.flip) main>.card[data-slide]{content-visibility:auto;contain-intrinsic-size:auto 1100px}",
    "@media print{.ss-bar,.ss-scorewrap,.ss-quiz,.ss-help,.ss-drill,.ss-chip,#ss-quiz-btn{display:none!important}body main>.card[data-slide]{content-visibility:visible}}",
  ].join("");
  function addStyles() {
    document.head.appendChild(el("style", { id: "ss-style", text: CSS }));
  }

  /* -------------------------------------------------------------- drills */
  // Each drill returns {title, given (html), fields:[{label, answer, tol, unit}], steps:[html], tip}
  var COCOMO = {
    organic: [2.4, 1.05, 0.38],
    "semi-detached": [3.0, 1.12, 0.35],
    embedded: [3.6, 1.2, 0.32],
  };
  var DRILLS = {
    cocomo: {
      name: "COCOMO calculator drill",
      make: function () {
        var mode = pick(Object.keys(COCOMO)),
          k = COCOMO[mode];
        var kloc =
          mode === "organic"
            ? rnd(4, 48)
            : mode === "semi-detached"
              ? rnd(10, 120)
              : rnd(10, 90);
        var E = k[0] * Math.pow(kloc, k[1]),
          T = 2.5 * Math.pow(E, k[2]),
          S = E / T,
          P = (kloc * 1000) / E;
        return {
          given:
            "A <b>" + mode + "</b> project of <b>" + kloc + " KLOC</b>. Constants: a = " +
            k[0] + ", b = " + k[1] + ", c = 2.5, d = " + k[2] + ".",
          fields: [
            { label: "Effort E (person-months)", answer: E, rel: 0.03 },
            { label: "Development time TDEV (months)", answer: T, rel: 0.03 },
            { label: "Average staff SS (people)", answer: S, rel: 0.05 },
            { label: "Productivity (LOC per person-month)", answer: P, rel: 0.05 },
          ],
          steps: [
            "E = a·KLOC<sup>b</sup> = " + k[0] + " × " + kloc + "<sup>" + k[1] + "</sup> = <b>" + fmt(E, 1) + " person-months</b>",
            "TDEV = c·E<sup>d</sup> = 2.5 × " + fmt(E, 1) + "<sup>" + k[2] + "</sup> = <b>" + fmt(T, 1) + " months</b>",
            "SS = E ÷ TDEV = " + fmt(E, 1) + " / " + fmt(T, 1) + " = <b>" + fmt(S, 1) + " people</b>",
            "Productivity = LOC ÷ E = " + kloc * 1000 + " / " + fmt(E, 1) + " = <b>" + fmt(P, 0) + " LOC per person-month</b>",
          ],
          tip: "Write each formula with your numbers in it before the result: that is where the method marks are.",
        };
      },
    },
    pert: {
      name: "Three-point (PERT) drill",
      make: function () {
        var o = rnd(2, 12),
          m = o + rnd(1, 7),
          p = m + rnd(2, 14);
        var te = (o + 4 * m + p) / 6,
          sd = (p - o) / 6;
        return {
          given:
            "Optimistic O = <b>" + o + "</b>, most likely M = <b>" + m + "</b>, pessimistic P = <b>" + p + "</b> (days).",
          fields: [
            { label: "Expected time TE (days)", answer: te, abs: 0.02 },
            { label: "Standard deviation σ", answer: sd, abs: 0.02 },
          ],
          steps: [
            "TE = (O + 4M + P) ÷ 6 = (" + o + " + 4×" + m + " + " + p + ") / 6 = " + (o + 4 * m + p) + " / 6 = <b>" + fmt(te) + "</b>",
            "σ = (P − O) ÷ 6 = (" + p + " − " + o + ") / 6 = <b>" + fmt(sd) + "</b>",
          ],
          tip: "Only M is multiplied by 4, and you divide by 6. A bigger σ means a riskier task.",
        };
      },
    },
    risk: {
      name: "Risk exposure drill",
      make: function () {
        var a = { p: pick([10, 15, 20, 25, 30, 40, 50, 60, 70, 75, 80]), i: rnd(2, 20) },
          b = { p: pick([10, 20, 25, 35, 40, 50, 65, 80, 90]), i: rnd(1, 16) };
        var ra = (a.p / 100) * a.i,
          rb = (b.p / 100) * b.i;
        return {
          given:
            "Risk A: probability <b>" + a.p + "%</b>, impact <b>" + a.i + " weeks</b>.<br>Risk B: probability <b>" + b.p + "%</b>, impact <b>" + b.i + " weeks</b>.",
          fields: [
            { label: "Exposure of A (weeks)", answer: ra, abs: 0.01 },
            { label: "Exposure of B (weeks)", answer: rb, abs: 0.01 },
          ],
          steps: [
            "RE = P × I. A: " + a.p / 100 + " × " + a.i + " = <b>" + fmt(ra) + " weeks</b>",
            "B: " + b.p / 100 + " × " + b.i + " = <b>" + fmt(rb) + " weeks</b>",
            ra === rb
              ? "Equal exposure: rank them by urgency."
              : "Handle <b>" + (ra > rb ? "A" : "B") + "</b> first: it has the higher exposure.",
          ],
          tip: "Convert the percentage to a decimal first (25% = 0.25). Exposure is in the same unit as the impact.",
        };
      },
    },
    channels: {
      name: "Communication channels (Brooks’s law) drill",
      make: function () {
        var n = rnd(3, 12),
          k = rnd(1, 6),
          a = (n * (n - 1)) / 2,
          b = ((n + k) * (n + k - 1)) / 2;
        return {
          given: "A team of <b>" + n + "</b> people. The manager adds <b>" + k + "</b> more.",
          fields: [
            { label: "Channels now", answer: a, abs: 0 },
            { label: "Channels after adding", answer: b, abs: 0 },
            { label: "Extra channels created", answer: b - a, abs: 0 },
          ],
          steps: [
            "n(n−1)/2 = " + n + "×" + (n - 1) + "/2 = <b>" + a + "</b>",
            "(" + (n + k) + ")×" + (n + k - 1) + "/2 = <b>" + b + "</b>",
            b + " − " + a + " = <b>" + (b - a) + "</b> new paths: why adding people to a late project slows it down.",
          ],
          tip: "People grow linearly; channels grow roughly with n².",
        };
      },
    },
    ev: {
      name: "Earned value drill",
      make: function () {
        var pv = rnd(8, 40) * 10,
          ev = Math.round(pv * (0.6 + Math.random() * 0.6) / 10) * 10,
          ac = Math.round(ev * (0.7 + Math.random() * 0.6) / 10) * 10;
        var cpi = ev / ac,
          spi = ev / pv;
        return {
          given: "PV = <b>" + pv + "</b>, EV = <b>" + ev + "</b>, AC = <b>" + ac + "</b> (person-hours).",
          fields: [
            { label: "CPI", answer: cpi, abs: 0.011 },
            { label: "SPI", answer: spi, abs: 0.011 },
            { label: "Cost variance CV", answer: ev - ac, abs: 0 },
            { label: "Schedule variance SV", answer: ev - pv, abs: 0 },
          ],
          steps: [
            "CPI = EV ÷ AC = " + ev + " / " + ac + " = <b>" + fmt(cpi) + "</b> → " + (cpi < 1 ? "over budget" : cpi > 1 ? "under budget" : "on budget"),
            "SPI = EV ÷ PV = " + ev + " / " + pv + " = <b>" + fmt(spi) + "</b> → " + (spi < 1 ? "behind schedule" : spi > 1 ? "ahead of schedule" : "on schedule"),
            "CV = EV − AC = <b>" + (ev - ac) + "</b>, SV = EV − PV = <b>" + (ev - pv) + "</b> (negative = bad)",
          ],
          tip: "EV is always on top. Below 1 (or negative variance) is bad.",
        };
      },
    },
    ci: {
      name: "Customization index drill",
      make: function () {
        var s = rnd(2, 60),
          d = rnd(2, 60),
          c = s / (s + d);
        return {
          given: "A web app has <b>" + s + "</b> static pages (Nsp) and <b>" + d + "</b> dynamic pages (Ndp).",
          fields: [{ label: "C = Nsp ÷ (Ndp + Nsp)", answer: c, abs: 0.011 }],
          steps: [
            "C = " + s + " / (" + d + " + " + s + ") = " + s + " / " + (s + d) + " = <b>" + fmt(c) + "</b>",
            c < 0.5
              ? "Closer to 0: mostly dynamic pages, so the app is highly customized."
              : "Closer to 1: mostly static pages, so there is little customization.",
          ],
          tip: "Static pages go on top, and the bottom is all pages.",
        };
      },
    },
    duration: {
      name: "Effort vs duration drill",
      make: function () {
        var people = rnd(2, 6),
          days = rnd(5, 30),
          effort = people * days,
          labor = pick([24, 32, 40, 48, 60]),
          prod = pick([75, 80]);
        return {
          given:
            "A task needs <b>" + effort + " person-days</b> of effort and <b>" + people + "</b> people work on it.<br>Another task needs <b>" + labor + " labor hours</b>, and people are productive <b>" + prod + "%</b> of the day.",
          fields: [
            { label: "Duration (working days)", answer: days, abs: 0.01 },
            { label: "Clock time (business hours)", answer: labor / (prod / 100), abs: 0.5 },
          ],
          steps: [
            "Duration = Effort ÷ People = " + effort + " / " + people + " = <b>" + days + " days</b>",
            "Clock time = Labor ÷ productivity = " + labor + " / " + prod / 100 + " = <b>" + fmt(labor / (prod / 100), 1) + " hours</b>",
          ],
          tip: "Effort is for cost; duration and clock time are for the schedule.",
        };
      },
    },
  };
  function evalAnswer(text) {
    var t = String(text || "")
      .replace(/,/g, "")
      .replace(/[×xX]/g, "*")
      .replace(/÷/g, "/")
      .replace(/−/g, "-")
      .replace(/\^/g, "**")
      .replace(/%$/, "")
      .replace(/[a-zA-Z\s]+$/g, "")
      .trim();
    if (!t || !/^[0-9.+\-*/() ]+$/.test(t)) return NaN;
    try {
      // Whitelisted to digits and arithmetic above, so typing the formula (100/10) works too.
      var v = Function('"use strict";return (' + t + ")")();
      return typeof v === "number" && isFinite(v) ? v : NaN;
    } catch (e) {
      return NaN;
    }
  }
  function makeDrill(type, label) {
    var def = DRILLS[type];
    if (!def) return null;
    var box = el("section", { class: "ss-drill", "aria-label": def.name });
    function draw() {
      var d = def.make();
      box.innerHTML = "";
      box.appendChild(el("h4", { text: "🧮 " + def.name + (label ? " · " + label : "") }));
      box.appendChild(el("p", { class: "ss-given", html: d.given }));
      var inputs = d.fields.map(function (f) {
        var input = el("input", { type: "text", inputmode: "decimal", autocomplete: "off", "aria-label": f.label });
        var mark = el("span", { class: "ss-mark", "aria-live": "polite" });
        box.appendChild(el("label", null, [el("span", { text: f.label }), input, mark]));
        input.addEventListener("keydown", function (e) {
          if (e.key === "Enter") check();
        });
        return { f: f, input: input, mark: mark };
      });
      var steps = el("ol", { class: "ss-steps", hidden: true });
      d.steps.forEach(function (s) {
        steps.appendChild(el("li", { html: s }));
      });
      function check() {
        var all = true;
        inputs.forEach(function (x) {
          var v = evalAnswer(x.input.value),
            a = x.f.answer;
          var tol = x.f.rel ? Math.abs(a) * x.f.rel : x.f.abs || 0;
          var ok = !isNaN(v) && Math.abs(v - a) <= Math.max(tol, 1e-9);
          if (!ok && !isNaN(v) && x.f.rel === undefined && x.f.abs === 0) ok = Math.round(v) === Math.round(a);
          all = all && ok;
          x.input.className = isNaN(v) ? "" : ok ? "good" : "bad";
          x.mark.className = "ss-mark " + (isNaN(v) ? "" : ok ? "good" : "bad");
          x.mark.textContent = isNaN(v) ? (x.input.value ? "Type a number" : "") : ok ? "✓" : "✗ try again";
        });
        if (all) steps.hidden = false;
      }
      box.appendChild(
        el("div", { class: "ss-row" }, [
          el("button", { type: "button", text: "Check", on: { click: check } }),
          el("button", { type: "button", text: "Show the working", on: { click: function () { steps.hidden = false; } } }),
          el("button", { type: "button", text: "New numbers", on: { click: draw } }),
        ]),
      );
      box.appendChild(steps);
      box.appendChild(el("p", { class: "ss-tip", text: d.tip + " You can type the calculation itself, like 100/10." }));
    }
    draw();
    return box;
  }

  /* ---------------------------------------------------------------- quiz */
  // items: [{deck, qid, slide, prompt, options:[{t, c, w}], src, href}]
  var quizOpen = false;
  function runQuiz(all, title, onClose) {
    if (!all.length) {
      alert("No questions here yet.");
      return;
    }
    quizOpen = true;
    var wrap = el("div", { class: "ss-quiz", role: "dialog", "aria-modal": "true", "aria-label": title });
    var box = el("div", { class: "ss-box" });
    wrap.appendChild(box);
    document.body.appendChild(wrap);
    var prevOverflow = document.documentElement.style.overflow;
    document.documentElement.style.overflow = "hidden";
    var items, i, score, missed, answered, keyFn;

    function close() {
      quizOpen = false;
      document.removeEventListener("keydown", keyFn, true);
      document.documentElement.style.overflow = prevOverflow;
      wrap.remove();
      if (onClose) onClose();
    }
    function top(extra) {
      var t = el("div", { class: "ss-top" }, [el("strong", { text: title }), extra || null, el("button", { type: "button", text: "Close", on: { click: close } })]);
      box.appendChild(t);
    }
    function chooser() {
      box.innerHTML = "";
      top();
      box.appendChild(el("p", { text: all.length + " questions. How many do you want? They come in random order, one at a time." }));
      var row = el("div", { class: "ss-pickn" });
      [10, 20, 40].forEach(function (n) {
        if (n < all.length)
          row.appendChild(el("button", { type: "button", text: n + " questions", on: { click: function () { begin(n); } } }));
      });
      row.appendChild(el("button", { type: "button", "aria-pressed": "true", text: "All " + all.length, on: { click: function () { begin(all.length); } } }));
      box.appendChild(row);
      box.appendChild(el("p", { class: "ss-muted", text: "Keys: 1–4 or A–D to answer, Enter for the next question, Esc to close." }));
      row.lastChild.focus();
    }
    function begin(n) {
      items = shuffle(all).slice(0, n);
      i = 0;
      score = 0;
      missed = [];
      show();
    }
    function show() {
      box.innerHTML = "";
      answered = false;
      var it = items[i];
      top(el("span", { class: "ss-muted", style: "margin:0", text: i + 1 + " / " + items.length + " · score " + score }));
      box.appendChild(el("div", { class: "ss-prog" }, [el("i", { style: "width:" + (100 * i) / items.length + "%" })]));
      if (it.src) box.appendChild(el("p", { class: "ss-src", text: it.src }));
      box.appendChild(el("p", { class: "ss-qp", text: it.prompt }));
      var list = el("ol"),
        firstTry = true;
      var verdict = el("p", { class: "ss-verdict", role: "status" });
      var next = el("button", { type: "button", text: i + 1 < items.length ? "Next question" : "See my score", disabled: true, on: { click: advance } });
      var opts = shuffle(it.options);
      var buttons = opts.map(function (o, k) {
        var why = o.w ? el("div", { class: "ss-why", hidden: true, text: o.w }) : null;
        var b = el("button", { type: "button", class: "ss-opt" }, [el("b", { text: LETTERS[k] }), el("span", { text: o.t })]);
        b.addEventListener("click", function () {
          if (answered) return;
          if (o.c) {
            answered = true;
            b.classList.add("right");
            if (firstTry) score++;
            else missed.push(it);
            record(it.deck, it.qid, firstTry);
            verdict.className = "ss-verdict good";
            verdict.textContent = firstTry ? "Correct." : "That’s the one. This question goes on your mistakes list.";
            buttons.forEach(function (x) {
              x.b.disabled = true;
              if (x.why) x.why.hidden = false;
            });
            next.disabled = false;
            next.focus();
          } else {
            if (firstTry) record(it.deck, it.qid, false);
            firstTry = false;
            b.classList.add("wrong");
            b.disabled = true;
            if (why) why.hidden = false;
            verdict.className = "ss-verdict bad";
            verdict.textContent = "Not quite. Read why, then try again.";
          }
        });
        list.appendChild(el("li", null, [b, why]));
        return { b: b, why: why, o: o };
      });
      box.appendChild(list);
      box.appendChild(verdict);
      var foot = el("div", { class: "ss-foot" }, [
        el("span", { class: "ss-grow" }, [
          it.href ? el("a", { href: it.href, target: "_top", text: "Open this slide" }) : null,
        ]),
        el("button", {
          type: "button",
          text: "Show the answer",
          on: {
            click: function () {
              if (answered) return;
              firstTry = false;
              buttons.forEach(function (x) {
                if (x.o.c) x.b.click();
              });
            },
          },
        }),
        next,
      ]);
      box.appendChild(foot);
      box._buttons = buttons;
      box._next = next;
      if (buttons[0]) buttons[0].b.focus();
    }
    function advance() {
      i++;
      if (i < items.length) show();
      else end();
    }
    function end() {
      box.innerHTML = "";
      box._buttons = null;
      top();
      var pct = Math.round((100 * score) / items.length);
      box.appendChild(el("p", { class: "ss-big", text: score + " / " + items.length }));
      box.appendChild(el("p", { text: pct >= 80 ? "Strong. Keep going with another set." : pct >= 50 ? "Getting there. Retry the ones you missed." : "Re-read the slides for the missed ones, then retry." }));
      var row = el("div", { class: "ss-foot" });
      if (missed.length)
        row.appendChild(el("button", { type: "button", "aria-pressed": "true", text: "Retry the " + missed.length + " I missed", on: { click: function () { items = shuffle(missed); i = 0; score = 0; missed = []; show(); } } }));
      row.appendChild(el("button", { type: "button", text: "New set", on: { click: chooser } }));
      row.appendChild(el("button", { type: "button", text: "Close", on: { click: close } }));
      box.appendChild(row);
      box.appendChild(el("p", { class: "ss-muted", text: syncText() }));
    }
    keyFn = function (e) {
      if (e.key === "Escape") {
        e.preventDefault();
        close();
        return;
      }
      if (typing(e.target) || e.ctrlKey || e.metaKey || e.altKey) return;
      var bs = box._buttons;
      if (!bs) return;
      var k = e.key.toLowerCase(),
        n = "1234".indexOf(k) >= 0 ? +k - 1 : "abcd".indexOf(k);
      if (n >= 0 && bs[n] && !bs[n].b.disabled) {
        e.preventDefault();
        bs[n].b.click();
      } else if ((k === "enter" || k === "n") && box._next && !box._next.disabled) {
        e.preventDefault();
        box._next.click();
      }
    };
    document.addEventListener("keydown", keyFn, true);
    if (all.length > 10) chooser();
    else begin(all.length);
  }

  /* ---------------------------------------------------------- deck mode */
  function deckMode() {
    var DECK = body.getAttribute("data-deck");
    var finalOn = body.getAttribute("data-final");
    var chapter = body.getAttribute("data-chapter") || "";
    var reviewUrl = location.pathname.replace(/[^/]+\/[^/]*$/, "review/");
    var cards = [].slice.call(document.querySelectorAll("main>.card"));
    var qs = [].slice.call(document.querySelectorAll("article.q.pick[data-qid]"));
    var ids = qs.map(function (q) {
      return q.getAttribute("data-qid");
    });
    var restoring = false;

    function cardOf(n) {
      return n.closest(".card");
    }
    function slideOf(q) {
      var c = cardOf(q);
      return c ? +c.getAttribute("data-slide") : 0;
    }
    function itemOf(q) {
      var prompt = q.querySelector("header ~ p");
      return {
        deck: DECK,
        qid: q.getAttribute("data-qid"),
        slide: slideOf(q),
        src: "Slide " + slideOf(q),
        prompt: prompt ? prompt.textContent.replace(/\s+/g, " ").trim() : "",
        options: [].slice.call(q.querySelectorAll(".picks>li")).map(function (li) {
          var spans = li.querySelectorAll(".choice span");
          var w = li.querySelector(".opt-why");
          return {
            t: (spans[1] || spans[0]).textContent.replace(/\s+/g, " ").trim(),
            c: li.hasAttribute("data-c"),
            w: w ? w.textContent.replace(/\s+/g, " ").trim() : "",
          };
        }),
      };
    }

    // final badge
    var brand = document.querySelector(".top .brand");
    if (brand && finalOn !== null)
      brand.appendChild(
        el("span", {
          class: "ss-final " + (finalOn === "1" ? "on" : "off"),
          title: finalOn === "1" ? "This chapter is tested on the final exam" : "Your instructor said this chapter is not on the final",
          text: finalOn === "1" ? "✓ On the final" : "✗ Not on the final (" + chapter + ")",
        }),
      );

    // chips + recording
    function chip(q) {
      var r = result(DECK, q.getAttribute("data-qid"));
      var c = q.querySelector(".ss-chip");
      if (!c) {
        c = el("span", { class: "ss-chip" });
        var h = q.querySelector("header");
        if (h) h.appendChild(c);
      }
      c.className = "ss-chip " + (r === 1 ? "good" : r === 0 ? "bad" : "");
      c.textContent = r === 1 ? "✓ Got it" : r === 0 ? "✗ Missed before" : "";
      c.hidden = r === null;
      q.classList.toggle("ss-missed", r === 0);
    }
    qs.forEach(function (q) {
      var qid = q.getAttribute("data-qid");
      q.querySelectorAll(".picks>li .choice").forEach(function (b) {
        b.addEventListener("click", function () {
          if (restoring || q._ssTried) return;
          q._ssTried = true;
          record(DECK, qid, b.parentNode.hasAttribute("data-c"));
          chip(q);
        });
      });
      var rv = q.querySelector(".reveal-ans");
      if (rv)
        rv.addEventListener("click", function () {
          if (restoring || q._ssTried) return;
          q._ssTried = true;
          record(DECK, qid, false);
          chip(q);
        });
    });
    function restore() {
      restoring = true;
      qs.forEach(function (q) {
        if (result(DECK, q.getAttribute("data-qid")) === 1 && !q.classList.contains("done")) {
          var right = q.querySelector(".picks>li[data-c] .choice");
          if (right) right.click();
        }
        chip(q);
      });
      restoring = false;
    }
    restore();

    // controls: score menu + quiz
    var controls = document.querySelector(".top .controls");
    var scoreBtn = el("button", { type: "button", id: "ss-score", "aria-expanded": "false", title: "Your score on this deck (saved)" });
    var panel = el("div", { class: "ss-panel", hidden: true });
    var wrapS = el("div", { class: "ss-scorewrap" }, [scoreBtn, panel]);
    var quizBtn = el("button", {
      type: "button",
      id: "ss-quiz-btn",
      title: "Quiz mode: only this deck’s questions, one at a time (Q)",
      text: "Quiz",
      on: { click: openQuiz },
    });
    if (controls) {
      var anchor = controls.querySelector("a.btn");
      controls.insertBefore(quizBtn, anchor);
      controls.insertBefore(wrapS, anchor);
    }
    function openQuiz() {
      runQuiz(qs.map(itemOf), "Quiz · " + (document.querySelector(".brand strong") || {}).textContent, function () {
        restore();
        paint();
      });
    }
    function togglePanel(open) {
      if (open === undefined) open = panel.hidden;
      panel.hidden = !open;
      scoreBtn.setAttribute("aria-expanded", open ? "true" : "false");
      if (open) paint();
    }
    scoreBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      togglePanel();
    });
    document.addEventListener("click", function (e) {
      if (!panel.hidden && !wrapS.contains(e.target)) togglePanel(false);
    });
    function paint() {
      var s = deckStats(DECK, ids);
      scoreBtn.textContent = s.answered ? "Score " + s.right + "/" + s.total + (s.missed ? " · " + s.missed + " missed" : "") : "Score 0/" + s.total;
      if (panel.hidden) return;
      panel.innerHTML = "";
      panel.appendChild(el("h4", { text: "Your progress on this deck" }));
      var meter = el("div", { class: "ss-meter" }, [
        el("i", { class: "g", style: "width:" + (100 * s.right) / (s.total || 1) + "%" }),
        el("i", { class: "b", style: "width:" + (100 * s.missed) / (s.total || 1) + "%" }),
      ]);
      panel.appendChild(meter);
      panel.appendChild(
        el("div", { class: "ss-nums" }, [
          el("div", null, [el("b", { text: s.right }), el("span", { text: "right first try" })]),
          el("div", null, [el("b", { text: s.missed }), el("span", { text: "missed" })]),
          el("div", null, [el("b", { text: s.total - s.answered }), el("span", { text: "not answered" })]),
        ]),
      );
      var acts = el("div", { class: "ss-acts" }, [
        el("button", { type: "button", text: "↓ Next unanswered question (U)", on: { click: function () { togglePanel(false); jumpTo("unanswered"); } } }),
        s.missed ? el("button", { type: "button", text: "↓ Next missed question (M)", on: { click: function () { togglePanel(false); jumpTo("missed"); } } }) : null,
        s.missed
          ? el("button", {
              type: "button",
              text: "Practice my " + s.missed + (s.missed === 1 ? " mistake" : " mistakes") + " here",
              on: {
                click: function () {
                  togglePanel(false);
                  runQuiz(qs.filter(function (q) { return result(DECK, q.getAttribute("data-qid")) === 0; }).map(itemOf), "My mistakes", function () { restore(); paint(); });
                },
              },
            })
          : null,
        el("a", { class: "btn", href: reviewUrl + "?deck=" + encodeURIComponent(DECK), target: "_top", text: "All chapters: review page →" }),
        el("button", { type: "button", text: "Keyboard shortcuts (?)", on: { click: function () { togglePanel(false); help(); } } }),
        s.answered
          ? el("button", {
              type: "button",
              text: "Reset this deck’s answers",
              on: {
                click: function () {
                  if (confirm("Forget every saved answer on this deck? Reload the page afterwards to clear the answered questions.")) {
                    resetDeck(DECK);
                    paint();
                  }
                },
              },
            })
          : null,
      ]);
      panel.appendChild(acts);
      panel.appendChild(el("p", { class: "ss-muted", text: syncText() }));
    }
    listeners.push(function () {
      paint();
      qs.forEach(chip);
    });
    paint();

    // navigation helpers
    var jump = document.getElementById("f-jump");
    function isFlip() {
      return body.classList.contains("flip");
    }
    function currentIndex() {
      if (isFlip()) {
        for (var i = 0; i < cards.length; i++) if (cards[i].classList.contains("current")) return i;
        return 0;
      }
      for (var k = 0; k < cards.length; k++) if (cards[k].getBoundingClientRect().bottom > 90) return k;
      return cards.length - 1;
    }
    function goCard(i) {
      i = Math.max(0, Math.min(cards.length - 1, i));
      if (isFlip() && jump) {
        jump.value = i;
        jump.dispatchEvent(new Event("change"));
      } else {
        var y = cards[i].getBoundingClientRect().top + window.scrollY - 70;
        window.scrollTo({ top: y, behavior: "smooth" });
      }
    }
    function flash(q) {
      q.classList.add("ss-flash");
      setTimeout(function () {
        q.classList.remove("ss-flash");
      }, 1800);
    }
    function jumpTo(kind) {
      var from = currentIndex();
      var list = qs.filter(function (q) {
        var r = result(DECK, q.getAttribute("data-qid"));
        return kind === "missed" ? r === 0 : r === null && !q.classList.contains("done");
      });
      if (!list.length) {
        alert(kind === "missed" ? "No missed questions left on this deck." : "You have answered every question on this deck.");
        return;
      }
      var target = list.filter(function (q) {
        var i = cards.indexOf(cardOf(q));
        return i > from || (i === from && q.getBoundingClientRect().top > 100);
      })[0] || list[0];
      var ci = cards.indexOf(cardOf(target));
      if (isFlip()) goCard(ci);
      setTimeout(function () {
        target.scrollIntoView({ behavior: "smooth", block: "center" });
        flash(target);
      }, isFlip() ? 50 : 0);
    }
    function activeQuestion() {
      var pool = qs.filter(function (q) {
        return !q.classList.contains("done");
      });
      if (isFlip()) {
        var cur = cards[currentIndex()];
        return pool.filter(function (q) { return cardOf(q) === cur; })[0] || null;
      }
      var vh = window.innerHeight;
      return pool.filter(function (q) {
        var r = q.getBoundingClientRect();
        return r.bottom > 70 && r.top < vh;
      })[0] || null;
    }

    // reading progress bar
    var bar = el("div", { class: "ss-bar", "aria-hidden": "true" });
    body.appendChild(bar);
    function progress() {
      var f;
      if (isFlip()) f = cards.length > 1 ? currentIndex() / (cards.length - 1) : 1;
      else {
        var h = document.documentElement.scrollHeight - window.innerHeight;
        f = h > 0 ? window.scrollY / h : 1;
      }
      bar.style.width = Math.max(0, Math.min(1, f)) * 100 + "%";
    }
    window.addEventListener("scroll", progress, { passive: true });
    new MutationObserver(progress).observe(body, { attributes: true, subtree: true, attributeFilter: ["class"] });
    progress();

    // drills
    document.querySelectorAll(".card[data-drill]").forEach(function (card) {
      card.getAttribute("data-drill").split(/\s+/).forEach(function (t) {
        var d = makeDrill(t);
        if (d) card.appendChild(d);
      });
    });

    // keyboard shortcuts
    var helpBox = null;
    function help() {
      if (helpBox) {
        helpBox.remove();
        helpBox = null;
        return;
      }
      var rows = [
        ["A–D / 1–4", "Answer the question on screen"],
        ["N / J", "Next slide"],
        ["P / K", "Previous slide"],
        ["U", "Next unanswered question"],
        ["M", "Next missed question"],
        ["Q", "Quiz mode"],
        ["H", "Highlights on/off"],
        ["T", "Notes on/off"],
        ["?", "Show or hide this list"],
      ];
      helpBox = el("div", { class: "ss-help", role: "dialog", "aria-label": "Keyboard shortcuts" }, [
        el("strong", { text: "Keyboard shortcuts" }),
        el("table", null, rows.map(function (r) {
          return el("tr", null, [el("td", null, r[0].split(" / ").map(function (k, i) { return el("span", null, [i ? " " : "", el("kbd", { text: k })]); })), el("td", { text: r[1] })]);
        })),
        el("button", { type: "button", text: "Close", style: "margin-top:8px", on: { click: help } }),
      ]);
      body.appendChild(helpBox);
    }
    document.addEventListener("keydown", function (e) {
      if (quizOpen || e.ctrlKey || e.metaKey || e.altKey || typing(e.target)) return;
      var k = e.key.toLowerCase(),
        done = true;
      var n = "1234".indexOf(k) >= 0 && k.length === 1 ? +k - 1 : "abcd".indexOf(k);
      if (n >= 0 && k.length === 1) {
        var q = activeQuestion();
        var bs = q ? q.querySelectorAll(".picks>li .choice") : [];
        if (bs[n] && !bs[n].disabled) bs[n].click();
        else done = false;
      } else if (k === "n" || k === "j") goCard(currentIndex() + 1);
      else if (k === "p" || k === "k") goCard(currentIndex() - 1);
      else if (k === "u") jumpTo("unanswered");
      else if (k === "m") jumpTo("missed");
      else if (k === "q") openQuiz();
      else if (k === "h") (document.getElementById("t-hl") || {}).click && document.getElementById("t-hl").click();
      else if (k === "t") (document.getElementById("t-notes") || {}).click && document.getElementById("t-notes").click();
      else if (e.key === "?") help();
      else if (e.key === "Escape" && helpBox) help();
      else done = false;
      if (done) e.preventDefault();
    });
    // the question the keys will answer gets a thin accent edge
    var lastActive = null;
    function markActive() {
      var q = activeQuestion();
      if (q === lastActive) return;
      if (lastActive) lastActive.classList.remove("ss-active");
      if (q) q.classList.add("ss-active");
      lastActive = q;
    }
    window.addEventListener("scroll", function () {
      clearTimeout(markActive._t);
      markActive._t = setTimeout(markActive, 120);
    }, { passive: true });
    document.addEventListener("click", function () {
      setTimeout(markActive, 0);
    });
    markActive();
  }

  /* -------------------------------------------------------- review mode */
  function reviewMode() {
    var root = document.getElementById("ss-review");
    var src = body.getAttribute("data-questions") || "questions.json";
    var params = new URLSearchParams(location.search);
    var FINAL_KEY = "shoug-study-final-only-" + COURSE;
    var finalOnly = lsGet(FINAL_KEY) !== "0";
    var bank = null;

    fetch(src)
      .then(function (r) {
        return r.json();
      })
      .then(function (j) {
        bank = j;
        render();
        var deck = params.get("deck");
        if (deck && params.get("start")) startDeck(deck, params.get("start"));
      })
      .catch(function () {
        root.textContent = "Couldn’t load the questions. Check your connection and reload.";
      });
    listeners.push(function () {
      if (bank && !quizOpen) render();
    });

    function decks() {
      return bank.decks.filter(function (d) {
        return !finalOnly || d.final;
      });
    }
    function itemsFor(d) {
      return bank.questions
        .filter(function (q) {
          return q.d === d.key;
        })
        .map(function (q) {
          return {
            deck: d.key,
            qid: q.id,
            slide: q.s,
            prompt: q.p,
            src: d.chapter + " · " + d.title + " · slide " + q.s,
            href: d.href + "#slide-" + q.s,
            options: q.o.map(function (o) {
              return { t: o[0], c: !!o[1], w: o[2] || "" };
            }),
          };
        });
    }
    function gather(filter, ds) {
      var out = [];
      (ds || decks()).forEach(function (d) {
        itemsFor(d).forEach(function (it) {
          var r = result(d.key, it.qid);
          if (filter === "missed" ? r === 0 : filter === "new" ? r === null : true) out.push(it);
        });
      });
      return out;
    }
    function startDeck(key, kind) {
      var d = bank.decks.filter(function (x) { return x.key === key; })[0];
      if (!d) return;
      runQuiz(gather(kind || "all", [d]), d.chapter + " · " + d.title + (kind === "missed" ? " · mistakes" : ""), render);
    }
    function render() {
      root.innerHTML = "";
      var ds = decks();
      var missed = gather("missed"),
        fresh = gather("new"),
        everything = gather("all");
      var tot = { right: 0, missed: 0, answered: 0, total: 0 };
      ds.forEach(function (d) {
        var s = deckStats(d.key, d.ids);
        tot.right += s.right;
        tot.missed += s.missed;
        tot.answered += s.answered;
        tot.total += s.total;
      });

      var filter = el("label", { class: "rv-filter" }, [
        el("input", {
          type: "checkbox",
          checked: finalOnly ? true : null,
          on: {
            change: function (e) {
              finalOnly = e.target.checked;
              lsSet(FINAL_KEY, finalOnly ? "1" : "0");
              render();
            },
          },
        }),
        " Final chapters only (hides Ch 6.2 Scheduling and Ch 7 Quality)",
      ]);
      root.appendChild(filter);

      root.appendChild(
        el("section", { class: "rv-card rv-summary" }, [
          el("h2", { text: finalOnly ? "Your progress on the final chapters" : "Your progress on every chapter" }),
          el("div", { class: "ss-meter" }, [
            el("i", { class: "g", style: "width:" + (100 * tot.right) / (tot.total || 1) + "%" }),
            el("i", { class: "b", style: "width:" + (100 * tot.missed) / (tot.total || 1) + "%" }),
          ]),
          el("div", { class: "ss-nums" }, [
            el("div", null, [el("b", { text: tot.right }), el("span", { text: "right first try" })]),
            el("div", null, [el("b", { text: tot.missed }), el("span", { text: "missed" })]),
            el("div", null, [el("b", { text: tot.total - tot.answered }), el("span", { text: "not answered" })]),
          ]),
          el("div", { class: "rv-big" }, [
            el("button", {
              type: "button",
              "aria-pressed": missed.length ? "true" : null,
              disabled: missed.length ? null : true,
              text: missed.length ? "Practice my " + missed.length + (missed.length === 1 ? " mistake" : " mistakes") : "No mistakes saved yet",
              on: { click: function () { runQuiz(missed, "My mistakes", render); } },
            }),
            el("button", {
              type: "button",
              disabled: fresh.length ? null : true,
              text: "Questions I haven’t answered (" + fresh.length + ")",
              on: { click: function () { runQuiz(fresh, "Not answered yet", render); } },
            }),
            el("button", {
              type: "button",
              text: "Random mix from " + (finalOnly ? "the final chapters" : "every chapter"),
              on: { click: function () { runQuiz(everything, "Random mix", render); } },
            }),
          ]),
          el("p", { class: "ss-muted", text: syncText() + " A question leaves the mistakes list when you get it right on the first try." }),
        ]),
      );

      var table = el("div", { class: "rv-decks" });
      ds.forEach(function (d) {
        var s = deckStats(d.key, d.ids);
        table.appendChild(
          el("article", { class: "rv-card rv-deck" }, [
            el("div", { class: "rv-head" }, [
              el("div", null, [
                el("small", { text: d.chapter }),
                el("strong", { text: d.title }),
                el("span", { class: "ss-final " + (d.final ? "on" : "off"), text: d.final ? "On the final" : "Not on the final" }),
              ]),
              el("span", { class: "rv-score", text: s.right + "/" + s.total }),
            ]),
            el("div", { class: "ss-meter" }, [
              el("i", { class: "g", style: "width:" + (100 * s.right) / (s.total || 1) + "%" }),
              el("i", { class: "b", style: "width:" + (100 * s.missed) / (s.total || 1) + "%" }),
            ]),
            el("p", { class: "ss-muted", style: "margin:0 0 8px", text: s.answered + " answered · " + s.missed + " missed · " + (s.total - s.answered) + " to go" }),
            el("div", { class: "rv-acts" }, [
              el("a", { class: "btn", href: d.wrapper, target: "_top", text: "Open slides" }),
              el("button", { type: "button", text: "Quiz this chapter", on: { click: function () { startDeck(d.key, "all"); } } }),
              s.missed ? el("button", { type: "button", text: "Mistakes (" + s.missed + ")", on: { click: function () { startDeck(d.key, "missed"); } } }) : null,
            ]),
          ]),
        );
      });
      root.appendChild(el("h2", { class: "rv-h", text: "By chapter" }));
      root.appendChild(table);

      root.appendChild(el("h2", { class: "rv-h", id: "drills", text: "Calculation drills" }));
      root.appendChild(el("p", { class: "ss-muted", text: "New numbers every time. Type the answer (or the calculation, like 100/10), check it, then compare with the step-by-step working." }));
      var dr = el("div", { class: "rv-drills" });
      (bank.drills || []).forEach(function (x) {
        if (finalOnly && !x.final) return;
        var d = makeDrill(x.type, x.label);
        if (d) dr.appendChild(d);
      });
      root.appendChild(dr);
    }
  }

  /* ----------------------------------------------------------- hub mode */
  function hubMode() {
    var gallery = document.getElementById("annotated");
    if (!gallery) return;
    var links = [].slice.call(gallery.querySelectorAll("a.deck-preview[href*='/annotated-slides/']"));
    if (!links.length) return;
    var base = links[0].getAttribute("href").replace(/[^/]+\/?$/, "");
    var reviewUrl = base + "review/";
    var FINAL_KEY = "shoug-study-final-only-" + COURSE;
    var summary = null;
    var style = el("style", {
      text:
        ".ss-hub-bar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:0 0 14px}" +
        ".ss-hub-bar a{font-weight:700}" +
        ".ss-hub-bar label{display:inline-flex;gap:6px;align-items:center;cursor:pointer;font-size:14px}" +
        ".deck-preview{position:relative}" +
        ".ss-tile{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px;font-size:12px;font-weight:700}" +
        ".ss-tile span{padding:1px 7px;border-radius:999px;border:1px solid currentColor}" +
        ".ss-tile .on{color:#3fb37a}.ss-tile .off{color:#ff6b6b}.ss-tile .sc{color:inherit;opacity:.85}" +
        ".ss-hide-off .deck-preview.ss-off{display:none}",
    });
    document.head.appendChild(style);
    var finalOnly = lsGet(FINAL_KEY) === "1";
    var bar = el("div", { class: "ss-hub-bar" }, [
      el("a", { class: "btn btn-primary", href: reviewUrl, text: "[ REVIEW MY MISTAKES & DRILLS -> ]" }),
      el("label", null, [
        el("input", {
          type: "checkbox",
          checked: finalOnly ? true : null,
          on: {
            change: function (e) {
              finalOnly = e.target.checked;
              lsSet(FINAL_KEY, finalOnly ? "1" : "0");
              gallery.classList.toggle("ss-hide-off", finalOnly);
            },
          },
        }),
        "Final chapters only",
      ]),
    ]);
    var h2 = gallery.querySelector("h2");
    gallery.insertBefore(bar, h2 ? h2.nextSibling : gallery.firstChild);
    gallery.classList.toggle("ss-hide-off", finalOnly);
    function paint() {
      if (!summary) return;
      links.forEach(function (a) {
        var key = a.getAttribute("href").replace(/\/$/, "").split("/").pop();
        var d = summary.decks.filter(function (x) { return x.key === key; })[0];
        if (!d) return;
        a.classList.toggle("ss-off", !d.final);
        var box = a.querySelector(".ss-tile") || a.appendChild(el("div", { class: "ss-tile" }));
        var s = deckStats(d.key, null);
        box.innerHTML = "";
        box.appendChild(el("span", { class: d.final ? "on" : "off", text: d.final ? "On final" : "Not on final" }));
        if (s.answered)
          box.appendChild(el("span", { class: "sc", text: s.right + "/" + d.count + (s.missed ? " · " + s.missed + " missed" : "") }));
      });
    }
    listeners.push(paint);
    fetch(reviewUrl + "summary.json")
      .then(function (r) { return r.json(); })
      .then(function (j) {
        summary = j;
        paint();
      })
      .catch(function () {});
  }

  /* --------------------------------------------------------------- start */
  function start() {
    if (MODE !== "hub") addStyles();
    if (MODE === "deck") deckMode();
    else if (MODE === "review") reviewMode();
    else hubMode();
    Sync.start();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
