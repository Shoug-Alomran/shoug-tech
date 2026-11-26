/**
 * Account sync for Mock exam results and Review mistakes.
 *
 * Both features keep their data in this browser (localStorage) so they work
 * signed out. When the visitor is signed in, this merges that data with their
 * private Firestore copy, so it follows them between devices:
 *
 *   users/{uid}/private/mock      history, ready, seen,  (shoug-mock-exams,
 *                                 cleared                 shoug-mock-cleared,
 *                                                         shoug-mock-readiness,
 *                                                         shoug-mock-seen)
 *   users/{uid}/private/mistakes  items, gone            (shoug-quiz-mistakes,
 *                                                         shoug-quiz-mistakes-gone)
 *
 * Merging never loses an answer: attempts and mistakes are joined by id (the
 * newer copy wins), readiness keeps the latest score per chapter, and a
 * mistake retired on one device stays retired through its tombstone in
 * "gone" unless it is missed again later.
 *
 * Pages call ShougStudySync.changed() after writing; the sync then pulls,
 * merges and pushes. After a merge that changed local data it fires
 * "shoug:study-sync" on window so the page can re-render.
 *
 * Uses the page's Firebase when firebase-auth.js has loaded it; otherwise it
 * loads just the SDK with the same project config (sign-in is shared per site).
 * If the Firestore rules don't allow these documents yet, it stays quiet and
 * local-only.
 */
(function () {
  "use strict";
  if (window.ShougStudySync) return;

  var FB_VERSION = "10.12.0"; // keep in step with firebase-auth.js
  var FB_BASE =
    "https://www.gstatic.com/firebasejs/" + FB_VERSION + "/firebase-";
  var FB_CONFIG = {
    apiKey: "AIzaSyDUklr3u8laDZH2jhHVAO3BPE12GaPpOmI",
    authDomain: "shoug-tech.firebaseapp.com",
    projectId: "shoug-tech",
    storageBucket: "shoug-tech.firebasestorage.app",
    messagingSenderId: "621041999813",
    appId: "1:621041999813:web:8982befd8b0ccc1d9475ac",
  };
  var K = {
    history: "shoug-mock-exams",
    ready: "shoug-mock-readiness",
    seen: "shoug-mock-seen",
    mistakes: "shoug-quiz-mistakes",
    gone: "shoug-quiz-mistakes-gone",
    cleared: "shoug-mock-cleared", // course -> time its past attempts were cleared
  };
  var CAP = { history: 200, seenPerCourse: 1500, mistakes: 400, gone: 1500 };
  var GONE_DAYS = 120;

  var fb = null,
    user = null,
    disabled = false,
    busy = null,
    again = false,
    timer = null,
    readyResolve;
  var ready = new Promise(function (r) {
    readyResolve = r;
  });

  function load(key, fallback) {
    try {
      var v = JSON.parse(localStorage.getItem(key));
      return v == null ? fallback : v;
    } catch (e) {
      return fallback;
    }
  }
  function save(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (e) {}
  }
  function same(a, b) {
    return JSON.stringify(a) === JSON.stringify(b);
  }
  function stamp(x) {
    return (x && (x.upd || x.at)) || 0;
  }

  /* ------------------------------------------------------------ merging */

  function byId(lists, cap, keep) {
    var all = {};
    lists.forEach(function (list) {
      (Array.isArray(list) ? list : []).forEach(function (x) {
        if (!x || !x.id) return;
        if (!all[x.id] || stamp(x) > stamp(all[x.id])) all[x.id] = x;
      });
    });
    return Object.keys(all)
      .map(function (k) {
        return all[k];
      })
      .filter(
        keep ||
          function () {
            return true;
          },
      )
      .sort(function (a, b) {
        return (a.at || 0) - (b.at || 0);
      })
      .slice(-cap);
  }
  function mergeReady(a, b) {
    var out = JSON.parse(JSON.stringify(a || {}));
    Object.keys(b || {}).forEach(function (course) {
      out[course] = out[course] || {};
      Object.keys(b[course] || {}).forEach(function (ch) {
        var x = b[course][ch];
        if (!out[course][ch] || (x && x.at > (out[course][ch].at || 0)))
          out[course][ch] = x;
      });
    });
    return out;
  }
  function dropCleared(ready, keep) {
    Object.keys(ready).forEach(function (course) {
      Object.keys(ready[course] || {}).forEach(function (ch) {
        if (!keep(course, ready[course][ch] && ready[course][ch].at))
          delete ready[course][ch];
      });
    });
    return ready;
  }
  function mergeSeen(remote, local) {
    var out = {};
    [remote || {}, local || {}].forEach(function (src) {
      Object.keys(src).forEach(function (course) {
        out[course] = Object.assign(out[course] || {}, src[course]);
      });
    });
    Object.keys(out).forEach(function (course) {
      var keys = Object.keys(out[course]);
      if (keys.length > CAP.seenPerCourse)
        keys.slice(0, keys.length - CAP.seenPerCourse).forEach(function (k) {
          delete out[course][k];
        });
    });
    return out;
  }
  function mergeGone(a, b) {
    var out = {},
      cutoff = Date.now() - GONE_DAYS * 86400000;
    [a || {}, b || {}].forEach(function (src) {
      Object.keys(src).forEach(function (id) {
        if (src[id] > cutoff && (!out[id] || src[id] > out[id]))
          out[id] = src[id];
      });
    });
    var ids = Object.keys(out).sort(function (x, y) {
      return out[x] - out[y];
    });
    ids.slice(0, Math.max(0, ids.length - CAP.gone)).forEach(function (id) {
      delete out[id];
    });
    return out;
  }
  // Firestore copy is trimmed so 400 mistakes stay well under 1 MB.
  function slim(m) {
    var c = {};
    Object.keys(m).forEach(function (k) {
      var v = m[k];
      c[k] = typeof v === "string" && v.length > 420 ? v.slice(0, 420) : v;
    });
    return c;
  }

  /* ------------------------------------------------------------ firebase */

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement("script");
      s.src = src;
      s.onload = resolve;
      s.onerror = reject;
      document.head.appendChild(s);
    });
  }
  function firebaseReady() {
    var have = function () {
      return (
        window.firebase &&
        window.firebase.apps &&
        window.firebase.apps.length &&
        window.firebase.firestore
      );
    };
    if (have()) return Promise.resolve(window.firebase);
    // firebase-auth.js may still be booting on this page.
    return new Promise(function (resolve) {
      var done = false;
      var finish = function () {
        if (done) return;
        done = true;
        resolve();
      };
      window.addEventListener("shoug:fb", finish, { once: true });
      setTimeout(
        finish,
        document.querySelector(
          'script[src*="firebase-auth.js"], script[src*="mobile-navigation.js"]',
        )
          ? 4000
          : 0,
      );
    }).then(function () {
      if (have()) return window.firebase;
      var chain =
        window.firebase && window.firebase.initializeApp
          ? Promise.resolve()
          : loadScript(FB_BASE + "app-compat.js");
      return chain
        .then(function () {
          return Promise.all([
            window.firebase.auth
              ? null
              : loadScript(FB_BASE + "auth-compat.js"),
            window.firebase.firestore
              ? null
              : loadScript(FB_BASE + "firestore-compat.js"),
          ]);
        })
        .then(function () {
          if (!window.firebase.apps.length)
            window.firebase.initializeApp(FB_CONFIG);
          return window.firebase;
        });
    });
  }
  function doc(name) {
    return fb
      .firestore()
      .collection("users")
      .doc(user.uid)
      .collection("private")
      .doc(name);
  }

  /* ------------------------------------------------------------ sync */

  function syncOnce() {
    if (!user || disabled) return Promise.resolve(false);
    return Promise.all([doc("mock").get(), doc("mistakes").get()])
      .then(function (snaps) {
        var rm = snaps[0].exists ? snaps[0].data() : {},
          rx = snaps[1].exists ? snaps[1].data() : {};
        var local = {
          history: load(K.history, []),
          ready: load(K.ready, {}),
          seen: load(K.seen, {}),
          mistakes: load(K.mistakes, []),
          gone: load(K.gone, {}),
          cleared: load(K.cleared, {}),
        };
        var gone = mergeGone(rx.gone, local.gone);
        var cleared = Object.assign({}, rm.cleared || {});
        Object.keys(local.cleared).forEach(function (c) {
          if (!cleared[c] || local.cleared[c] > cleared[c])
            cleared[c] = local.cleared[c];
        });
        var notCleared = function (course, at) {
          return !(cleared[course] && (at || 0) <= cleared[course]);
        };
        var merged = {
          history: byId([rm.history, local.history], CAP.history, function (h) {
            return notCleared(h.course, h.at);
          }),
          ready: dropCleared(mergeReady(rm.ready, local.ready), notCleared),
          seen: mergeSeen(rm.seen, local.seen),
          mistakes: byId(
            [rx.items, local.mistakes],
            CAP.mistakes,
            function (m) {
              // Retired after it was last missed: stays retired.
              return !(gone[m.id] && gone[m.id] >= (m.at || 0));
            },
          ),
          gone: gone,
          cleared: cleared,
        };
        var changedLocal = false;
        ["history", "ready", "seen", "mistakes", "gone", "cleared"].forEach(
          function (k) {
            if (!same(local[k], merged[k])) {
              save(K[k], merged[k]);
              changedLocal = true;
            }
          },
        );
        var writes = [];
        var mockDoc = {
          history: merged.history,
          ready: merged.ready,
          seen: merged.seen,
          cleared: cleared,
        };
        if (
          !same(
            {
              history: rm.history || [],
              ready: rm.ready || {},
              seen: rm.seen || {},
              cleared: rm.cleared || {},
            },
            mockDoc,
          )
        )
          writes.push(
            doc("mock").set(Object.assign({ updatedAt: Date.now() }, mockDoc)),
          );
        var items = merged.mistakes.map(slim);
        if (!same(rx.items || [], items) || !same(rx.gone || {}, gone))
          writes.push(
            doc("mistakes").set({
              items: items,
              gone: gone,
              updatedAt: Date.now(),
            }),
          );
        return Promise.all(writes).then(function () {
          if (changedLocal)
            window.dispatchEvent(new CustomEvent("shoug:study-sync"));
          return changedLocal;
        });
      })
      .catch(function (e) {
        // Rules not deployed yet, offline, or signed out mid-sync: stay local.
        if (e && e.code === "permission-denied") disabled = true;
        return false;
      });
  }
  function run() {
    if (busy) {
      again = true;
      return busy;
    }
    busy = syncOnce().then(function (r) {
      busy = null;
      if (again) {
        again = false;
        return run();
      }
      return r;
    });
    return busy;
  }

  firebaseReady()
    .then(function (f) {
      fb = f;
      fb.auth().onAuthStateChanged(function (u) {
        user = u || null;
        disabled = false;
        if (user)
          run().then(function () {
            readyResolve(user);
          });
        else readyResolve(null);
      });
    })
    .catch(function () {
      readyResolve(null);
    });

  window.ShougStudySync = {
    ready: ready,
    user: function () {
      return user;
    },
    // Call after writing any of the synced keys; pushes shortly after.
    changed: function () {
      clearTimeout(timer);
      timer = setTimeout(run, 1200);
    },
    // Record mistakes retired here, so other devices drop them too.
    forget: function (ids) {
      var gone = load(K.gone, {}),
        now = Date.now();
      (ids || []).forEach(function (id) {
        gone[id] = now;
      });
      save(K.gone, gone);
      this.changed();
    },
    // "Report a problem" on a question: resolves true when stored.
    report: function (data) {
      if (!user || !fb) return Promise.resolve(false);
      return fb
        .firestore()
        .collection("questionReports")
        .add(
          Object.assign({}, data, {
            uid: user.uid,
            createdAt: fb.firestore.FieldValue.serverTimestamp(),
          }),
        )
        .then(
          function () {
            return true;
          },
          function () {
            return false;
          },
        );
    },
  };
})();
