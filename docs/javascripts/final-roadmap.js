/* Final exam roadmaps: topic statuses, live group and course bars, and sync.
   Pages: scripts/build_final_roadmaps.py

   Statuses are saved in this browser straight away. When the student is signed
   in they are also kept in users/{uid}/private/data → finalRoadmaps.<course>,
   which only the owner can read (see ShougPrivate in firebase-auth.js). The
   roadmap runs inside the course wrapper's iframe and borrows the wrapper's
   Firebase session; opened on its own it stays browser-only.

   Each topic is stored as {v: status 0–3, t: ms timestamp}; devices merge topic
   by topic and the newest mark wins, so a reset is stored as v: 0, not deleted. */
(function () {
  var html = document.documentElement;
  var KEY = html.getAttribute("data-roadmap-key") || "final-roadmap";
  var COURSE = KEY.replace(/^final-roadmap-/, "");

  function now() {
    return Date.now();
  }
  function normalize(obj) {
    var out = {};
    Object.keys(obj || {}).forEach(function (id) {
      var e = obj[id];
      if (typeof e === "number") out[id] = { v: e, t: 0 };
      else if (e && typeof e.v === "number") out[id] = { v: e.v, t: +e.t || 0 };
    });
    return out;
  }
  var state = {};
  try {
    state = normalize(JSON.parse(localStorage.getItem(KEY) || "{}"));
  } catch (e) {
    state = {};
  }
  function saveLocal() {
    try {
      localStorage.setItem(KEY, JSON.stringify(state));
    } catch (e) {}
  }

  var topics = Array.prototype.slice.call(
    document.querySelectorAll(".rm-topic"),
  );
  function val(li) {
    var e = state[li.getAttribute("data-id")];
    return e ? e.v : 0;
  }
  // a reviewed topic counts a third, can explain two thirds, tested a whole topic
  function score(list) {
    if (!list.length) return 0;
    var s = 0;
    list.forEach(function (li) {
      s += val(li) / 3;
    });
    return s / list.length;
  }
  function pct(n, of) {
    return (of ? (100 * n) / of : 0) + "%";
  }

  function update() {
    var counts = [0, 0, 0, 0];
    topics.forEach(function (li) {
      var v = val(li);
      counts[v]++;
      li.setAttribute("data-state", v);
      var input = li.querySelector('input[value="' + v + '"]');
      if (input && !input.checked) input.checked = true;
    });
    var n = topics.length;
    document.querySelectorAll(".rm-group").forEach(function (g) {
      var list = Array.prototype.slice.call(g.querySelectorAll(".rm-topic"));
      var tested = list.filter(function (li) {
        return val(li) === 3;
      }).length;
      g.querySelector(".rm-gbar i").style.width = score(list) * 100 + "%";
      g.querySelector(".rm-gn").textContent =
        tested + " / " + list.length + " tested";
      g.classList.toggle("done", list.length > 0 && tested === list.length);
    });
    var total = Math.round(score(topics) * 100);
    document.querySelectorAll(".rm-pct, .rm-meter-n").forEach(function (el) {
      el.textContent = total + "%";
    });
    ["s1", "s2", "s3"].forEach(function (cls, i) {
      var w = pct(counts[i + 1], n);
      var a = document.querySelector(".rm-stack ." + cls);
      var b = document.querySelector(".rm-meter-bar .m" + (i + 1));
      if (a) a.style.width = w;
      if (b) b.style.width = w;
    });
    document.querySelectorAll("[data-count]").forEach(function (b) {
      b.textContent = counts[+b.getAttribute("data-count")];
    });
    var next = null;
    for (var level = 0; level < 3 && !next; level++) {
      next = topics.filter(function (li) {
        return val(li) === level;
      })[0];
    }
    var link = document.querySelector("[data-next]");
    if (!link) return;
    if (next) {
      link.textContent = next.querySelector(".rm-topic-text b").textContent;
      link.setAttribute("href", "#route");
      link.onclick = function (e) {
        e.preventDefault();
        var g = next.closest("details");
        if (g) g.open = true;
        next.scrollIntoView({ behavior: "smooth", block: "center" });
      };
    } else {
      link.textContent = "Everything is tested. Do a past paper!";
      link.onclick = null;
      link.setAttribute("href", "#papers");
    }
  }

  // ---------- account sync ----------
  var sync = { ref: null, user: null, timer: null, unsubscribe: null };
  var syncEl = document.querySelector(".rm-sync");
  function setSync(text, action) {
    if (!syncEl) return;
    syncEl.textContent = text;
    if (action) {
      var a = document.createElement("button");
      a.type = "button";
      a.className = "rm-signin";
      a.textContent = action.label;
      a.addEventListener("click", action.run);
      syncEl.appendChild(document.createTextNode(" "));
      syncEl.appendChild(a);
    }
  }
  // The course wrapper loads firebase-auth.js; the roadmap is its same-origin iframe.
  var host = null;
  try {
    if (window.parent !== window && window.parent.__shougLoadFirebaseAuth)
      host = window.parent;
  } catch (e) {
    host = null;
  }
  if (!host && window.__shougLoadFirebaseAuth) host = window;

  function pushSoon() {
    if (!sync.ref) return;
    clearTimeout(sync.timer);
    sync.timer = setTimeout(push, 700);
  }
  function push() {
    if (!sync.ref) return;
    var fb = host.firebase;
    var payload = { finalRoadmaps: {} };
    payload.finalRoadmaps[COURSE] = {
      topics: state,
      updatedAt: fb.firestore.FieldValue.serverTimestamp(),
    };
    setSync("Saving to your account…");
    sync.ref
      .set(payload, { merge: true })
      .then(function () {
        setSync("Synced to your account.");
      })
      .catch(function (err) {
        console.error("Roadmap sync failed", err);
        setSync(
          "Saved in this browser; account sync failed, will retry on your next change.",
        );
      });
  }
  // Merge remote topics into local ones; returns true if local has newer marks.
  function merge(remote) {
    remote = normalize(remote);
    var localNewer = false;
    Object.keys(remote).forEach(function (id) {
      var r = remote[id],
        l = state[id];
      if (!l || r.t > l.t) state[id] = r;
    });
    Object.keys(state).forEach(function (id) {
      var r = remote[id];
      if (!r || state[id].t > r.t) localNewer = true;
    });
    return localNewer;
  }
  function startSync(user) {
    sync.user = user;
    setSync("Connecting to your account…");
    host.ShougPrivate.ready(user.uid)
      .then(function (ref) {
        if (sync.user !== user) return;
        if (!ref.parent || ref.parent.id !== "private") {
          // Rules not deployed yet: ShougPrivate fell back to the public profile. Stay local.
          setSync("Saved in this browser.");
          return;
        }
        sync.ref = ref;
        sync.unsubscribe = ref.onSnapshot(
          function (snap) {
            var data = snap.exists ? snap.data() : {};
            var mine = (data.finalRoadmaps || {})[COURSE] || {};
            var localNewer = merge(mine.topics);
            saveLocal();
            update();
            if (localNewer) pushSoon();
            else setSync("Synced to your account.");
          },
          function (err) {
            console.error("Roadmap sync listener failed", err);
            setSync("Saved in this browser; could not reach your account.");
          },
        );
      })
      .catch(function (err) {
        console.error("Roadmap sync failed", err);
        setSync("Saved in this browser; could not reach your account.");
      });
  }
  function stopSync() {
    if (sync.unsubscribe) sync.unsubscribe();
    sync.unsubscribe = null;
    sync.ref = null;
    sync.user = null;
  }
  function signInPrompt() {
    setSync("Saved in this browser.", {
      label: "Sign in to sync",
      run: function () {
        if (typeof host.__shougOpenAuthModal === "function")
          host.__shougOpenAuthModal();
        else host.__shougLoadFirebaseAuth(true);
      },
    });
  }
  function watch(fb) {
    fb.auth().onAuthStateChanged(function (user) {
      stopSync();
      if (user && host.ShougPrivate) startSync(user);
      else signInPrompt();
    });
  }
  if (!host) {
    setSync(
      "Saved in this browser. Open the roadmap from the course page to sync it to your account.",
    );
  } else if (host.__shoug_fb) {
    watch(host.__shoug_fb);
  } else {
    signInPrompt();
    host.addEventListener(
      "shoug:fb",
      function () {
        watch(host.__shoug_fb);
      },
      { once: true },
    );
    var signedBefore = false;
    try {
      signedBefore = host.localStorage.getItem("shoug-was-signed-in") === "1";
    } catch (e) {}
    if (signedBefore) host.__shougLoadFirebaseAuth(false);
  }

  // ---------- controls ----------
  topics.forEach(function (li) {
    li.addEventListener("change", function (e) {
      var id = li.getAttribute("data-id");
      state[id] = { v: +e.target.value, t: now() };
      saveLocal();
      update();
      pushSoon();
    });
  });

  var reset = document.querySelector(".rm-reset");
  if (reset)
    reset.addEventListener("click", function () {
      if (
        !confirm(
          "Clear every status on this roadmap" +
            (sync.ref ? " (on all your devices)?" : "?"),
        )
      )
        return;
      var t = now();
      topics.forEach(function (li) {
        state[li.getAttribute("data-id")] = { v: 0, t: t };
      });
      saveLocal();
      update();
      pushSoon();
    });

  var expand = document.querySelector(".rm-expand");
  if (expand)
    expand.addEventListener("click", function () {
      var groups = document.querySelectorAll(".rm-group");
      var open = Array.prototype.some.call(groups, function (g) {
        return !g.open;
      });
      groups.forEach(function (g) {
        g.open = open;
      });
      expand.textContent = open ? "Collapse all" : "Expand all";
    });

  var links = Array.prototype.slice.call(
    document.querySelectorAll(".rm-nav a"),
  );
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          links.forEach(function (a) {
            a.classList.toggle(
              "active",
              a.getAttribute("href") === "#" + e.target.id,
            );
          });
        });
      },
      { rootMargin: "-30% 0px -60% 0px" },
    );
    document.querySelectorAll(".rm-section").forEach(function (s) {
      io.observe(s);
    });
  }
  update();
})();
