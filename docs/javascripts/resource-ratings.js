/**
 * Thumbs up/down on every course resource, with the share of thumbs up shown
 * wherever that resource is listed.
 *
 * Resource pages (slides, annotated slides, breakdowns, exams, extra resources)
 * get the voting buttons under the page header. Course overviews and listing
 * pages get a chip with the % and the up/down counts on each row; a row that
 * points at a folder adds up everything inside it, and the overview's meta
 * panel shows the course total.
 *
 * One document per resource at resourceRatings/{path with / as |}, holding the
 * up/down tallies and a uid -> 1|-1 map, so a page view costs one read per rated
 * resource however many students voted. The rules (firebase/resource-ratings.rules)
 * check that a student only changes their own vote and that the tallies follow.
 *
 * Tallies are read over REST so signed-out visitors never load the Firebase SDK;
 * voting needs an account. Loaded by recent-pages.js.
 */
(function () {
  "use strict";

  if (window.__shougResourceRatings || window.top !== window.self) return;
  window.__shougResourceRatings = true;

  var API =
    "https://firestore.googleapis.com/v1/projects/shoug-tech/databases/(default)/documents";
  var COLLECTION = "resourceRatings";
  var CACHE_MS = 5 * 60 * 1000;
  // ETHCS303 pages don't load recent-pages.js, so its resources can't be voted on.
  var EXCLUDED = { ethcs303: true };

  var THUMB =
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M2 21h4V9H2v12zM22 10.5c0-1.1-.9-2-2-2h-6.3l1-4.6v-.3c0-.4-.2-.8-.4-1.1L13.2 1 6.6 7.6c-.4.4-.6.9-.6 1.4v10c0 1.1.9 2 2 2h9c.8 0 1.5-.5 1.8-1.2l3-7.1c.1-.2.2-.5.2-.7v-1.5z"/></svg>';

  var STYLE = [
    ".rrt-chip{display:inline-flex;align-items:center;gap:8px;font-family:var(--font-mono,monospace);font-size:11px;font-weight:700;line-height:1.2;color:var(--text-primary,var(--text-main,#e2d9f3));white-space:nowrap}",
    ".rrt-chip svg{width:12px;height:12px;flex:none;fill:var(--brand-purple,#b829ea)}",
    ".rrt-chip-count{display:inline-flex;align-items:center;gap:3px;font-weight:400;color:var(--text-secondary,var(--text-muted,#8b7ea8))}",
    ".rrt-chip-down svg{transform:rotate(180deg);fill:currentColor}",
    ".rrt-percent{color:var(--text-primary,var(--text-main,#e2d9f3));font-size:14px;font-weight:700}",
    ".rrt-percent:empty{display:none}",
    // Its own grid cell under the title: phones hide the status column, and the
    // Arabic toggle rewrites .dir-title's text, so the chip can live in neither.
    ".dir-row>.rrt-chip{grid-column:2;grid-row:2;display:flex;margin-top:6px}",
    ".topic-item .rrt-chip{flex:none;margin-inline:12px;align-self:center}",
    ".rrt-rating{display:flex;flex-wrap:wrap;align-items:center;gap:8px 10px;margin-top:14px;font-family:var(--font-mono,monospace);font-size:12px;color:var(--text-secondary,var(--text-muted,#8b7ea8))}",
    ".rrt-question{color:var(--text-secondary,var(--text-muted,#8b7ea8));font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase}",
    ".rrt-vote{display:inline-flex;align-items:center;justify-content:center;gap:6px;min-width:52px;min-height:40px;padding:8px 14px;border:1px solid var(--border-med,var(--border-dim,#4a3b69));border-radius:0;background:transparent;color:var(--text-primary,var(--text-main,#e2d9f3));font:inherit;font-weight:600;cursor:pointer}",
    ".rrt-vote svg{width:15px;height:15px;flex:none;fill:var(--brand-purple,#b829ea)}",
    ".rrt-vote[aria-pressed=true] svg{fill:currentColor}",
    ".rrt-vote[data-vote='-1'] svg{transform:rotate(180deg)}",
    ".rrt-vote:hover{border-color:var(--brand-purple,#b829ea);color:var(--brand-purple,#b829ea)}",
    ".rrt-vote:focus-visible{outline:2px solid var(--brand-purple,#b829ea);outline-offset:2px}",
    ".rrt-vote[aria-pressed=true]{border-color:var(--brand-purple,#b829ea);background:var(--brand-purple,#b829ea);color:#fff}",
    ".rrt-vote[disabled]{opacity:.6;cursor:default}",
    ".rrt-status:empty,.rrt-summary:empty{display:none}",
    ".rrt-status{color:var(--brand-purple,#b829ea)}",
    "body.shoug-light-mode .rrt-chip,body.shoug-light-mode .rrt-percent{color:#21152f}",
    "body.shoug-light-mode .rrt-question{color:#6e607d}",
    "body.shoug-light-mode .rrt-chip-count,body.shoug-light-mode .rrt-rating{color:#534a61}",
    "body.shoug-light-mode .rrt-vote{color:#21152f;border-color:#6e607d;background:transparent}",
    "body.shoug-light-mode .rrt-vote:hover{color:var(--brand-purple,#b829ea);border-color:var(--brand-purple,#b829ea);background:rgba(184,41,234,.06)}",
    "body.shoug-light-mode .rrt-vote[aria-pressed=true]{color:#fff;background:var(--brand-purple,#b829ea);border-color:var(--brand-purple,#b829ea)}",
    "@media (max-width:480px){.rrt-chip-count{font-size:10px}.rrt-question{flex-basis:100%}.topic-item .rrt-chip{margin-inline:8px}}",
  ].join("\n");

  // ── Helpers ──────────────────────────────────────────────────────────────

  function isArabic() {
    return (document.documentElement.lang || "").indexOf("ar") === 0;
  }

  function L(en, ar) {
    return isArabic() ? ar : en;
  }

  function courseOf(pathname) {
    var m = pathname.match(/^\/academics\/(?:[a-z-]+\/){1,2}?([a-z]+\d{3})\//);
    return m ? m[1] : "";
  }

  /** The canonical path of a page or link; STAT101's viewer is keyed by its PDF. */
  function resourcePath(url) {
    var path = url.pathname.replace(/index\.html$/, "");
    if (/\/viewer\/$/.test(path) && url.searchParams.get("src"))
      return new URL(url.searchParams.get("src"), location.origin).pathname;
    if (!/\/$/.test(path) && !/\.[a-z0-9]+$/i.test(path)) path += "/";
    return path;
  }

  function docId(path) {
    return path.replace(/\//g, "|");
  }

  function percent(up, down) {
    return Math.round((up / (up + down)) * 100);
  }

  function countLabel(n) {
    if (isArabic()) return n === 1 ? "تقييم واحد" : n + " تقييمات";
    return n === 1 ? "1 rating" : n + " ratings";
  }

  function injectStyle() {
    if (document.getElementById("rrt-style")) return;
    var s = document.createElement("style");
    s.id = "rrt-style";
    s.textContent = STYLE;
    document.head.appendChild(s);
  }

  function onLangChange(fn) {
    new MutationObserver(fn).observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["lang"],
    });
  }

  function intField(fields, key) {
    var n = fields && fields[key] && Number(fields[key].integerValue);
    return n > 0 ? n : 0;
  }

  // ── Listings and course overview ─────────────────────────────────────────

  function cacheKey(course) {
    return "shoug-resource-ratings:" + course;
  }

  function readCache(course) {
    try {
      var c = JSON.parse(sessionStorage.getItem(cacheKey(course)));
      return c && Date.now() - c.at < CACHE_MS ? c.items : null;
    } catch (e) {
      return null;
    }
  }

  function writeCache(course, items) {
    try {
      sessionStorage.setItem(
        cacheKey(course),
        JSON.stringify({ at: Date.now(), items: items }),
      );
    } catch (e) {}
  }

  function clearCache(course) {
    try {
      sessionStorage.removeItem(cacheKey(course));
    } catch (e) {}
  }

  /** Every rated resource in a course, as { path: [up, down] }. */
  function loadCourse(course) {
    var cached = readCache(course);
    if (cached) return Promise.resolve(cached);
    return fetch(API + ":runQuery", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        structuredQuery: {
          from: [{ collectionId: COLLECTION }],
          where: {
            fieldFilter: {
              field: { fieldPath: "course" },
              op: "EQUAL",
              value: { stringValue: course },
            },
          },
          select: {
            fields: [
              { fieldPath: "path" },
              { fieldPath: "up" },
              { fieldPath: "down" },
            ],
          },
          limit: 2000,
        },
      }),
    })
      .then(function (r) {
        if (!r.ok) throw new Error(String(r.status));
        return r.json();
      })
      .then(function (rows) {
        var items = {};
        rows.forEach(function (row) {
          var f = row.document && row.document.fields;
          if (f && f.path)
            items[f.path.stringValue] = [
              intField(f, "up"),
              intField(f, "down"),
            ];
        });
        writeCache(course, items);
        return items;
      });
  }

  /** Tallies for one path; a folder path adds up everything inside it. */
  function tally(items, path) {
    var up = 0,
      down = 0;
    Object.keys(items).forEach(function (p) {
      if (p === path || (/\/$/.test(path) && p.indexOf(path) === 0)) {
        up += items[p][0];
        down += items[p][1];
      }
    });
    return { up: up, down: down, total: up + down };
  }

  function chipHtml(t) {
    return (
      "<span>" +
      percent(t.up, t.down) +
      '%</span><span class="rrt-chip-count">' +
      THUMB +
      t.up +
      '</span><span class="rrt-chip-count rrt-chip-down">' +
      THUMB +
      t.down +
      "</span>"
    );
  }

  function labelChip(chip, t) {
    var label = L(
      percent(t.up, t.down) + "% positive from " + countLabel(t.total),
      percent(t.up, t.down) + "٪ إيجابي من " + countLabel(t.total),
    );
    chip.title = label;
    chip.setAttribute("aria-label", label);
  }

  function placeChip(link, chip) {
    if (link.classList.contains("topic-name-link"))
      link.insertAdjacentElement("afterend", chip);
    else link.appendChild(chip);
  }

  function initListing(course) {
    var links = Array.prototype.filter.call(
      document.querySelectorAll(
        "a.dir-row[href], a.topic-name-link[href], a.deck-preview[href]",
      ),
      function (a) {
        return !a.closest(".academic-sidebar");
      },
    );
    var meta = document.querySelector(".meta-content");
    var overview = !document.querySelector(".directory-container");
    if (!links.length && !(overview && meta)) return;

    loadCourse(course)
      .then(function (items) {
        injectStyle();
        var relabel = [];
        links.forEach(function (a) {
          var url;
          try {
            url = new URL(a.getAttribute("href"), location.href);
          } catch (e) {
            return;
          }
          if (url.origin !== location.origin) return;
          var t = tally(items, resourcePath(url));
          if (!t.total) return;
          var chip = document.createElement("span");
          chip.className = "rrt-chip";
          chip.innerHTML = chipHtml(t);
          labelChip(chip, t);
          placeChip(a, chip);
          relabel.push([chip, t]);
        });

        var whole = tally(items, resourcePath(new URL(location.href)));
        if (overview && meta && whole.total) {
          var row = document.createElement("div");
          row.className = "meta-row rrt-meta-row";
          row.innerHTML =
            '<span class="meta-key"></span><span class="meta-val rrt-chip">' +
            chipHtml(whole) +
            "</span>";
          var key = row.querySelector(".meta-key");
          var setKey = function () {
            key.textContent = L("CONTENT RATING", "تقييم المحتوى");
          };
          setKey();
          meta.insertBefore(row, meta.querySelector(".meta-links-title"));
          labelChip(row.querySelector(".rrt-chip"), whole);
          relabel.push([row.querySelector(".rrt-chip"), whole]);
          onLangChange(setKey);
        }
        if (relabel.length)
          onLangChange(function () {
            relabel.forEach(function (pair) {
              labelChip(pair[0], pair[1]);
            });
          });
      })
      .catch(function () {
        // Rules not merged yet, or offline: listings simply show no chips.
      });
  }

  // ── Resource page ────────────────────────────────────────────────────────

  function initWidget(course, path) {
    var buttons = document.querySelector(".page-header .action-buttons");
    var header = document.querySelector(".content-header");
    var heading = document.querySelector("main h1");
    if (!buttons && !header && !heading) return;
    injectStyle();

    var state = {
      up: 0,
      down: 0,
      votes: {},
      available: false,
      user: null,
      authReady: false,
      pending: 0,
      saving: false,
      status: null,
    };

    var box = document.createElement("div");
    box.className = "rrt-rating";
    box.innerHTML =
      '<span class="rrt-question"></span>' +
      '<span class="rrt-percent"></span>' +
      '<button type="button" class="rrt-vote" data-vote="1">' +
      THUMB +
      '<span data-count="up">0</span></button>' +
      '<button type="button" class="rrt-vote" data-vote="-1">' +
      THUMB +
      '<span data-count="down">0</span></button>' +
      '<span class="rrt-summary"></span>' +
      '<span class="rrt-status" role="status"></span>';
    if (buttons) buttons.insertAdjacentElement("afterend", box);
    else if (header) header.appendChild(box);
    else heading.insertAdjacentElement("afterend", box);

    function mine() {
      return (state.user && state.votes[state.user.uid]) || 0;
    }

    function paint() {
      var total = state.up + state.down;
      box.setAttribute(
        "aria-label",
        L("Rate this resource", "قيّم هذا المصدر"),
      );
      box.setAttribute("role", "group");
      box.querySelector(".rrt-question").textContent = L(
        "Was this helpful?",
        "هل كان هذا مفيدًا؟",
      );
      box.querySelector('[data-count="up"]').textContent = state.up;
      box.querySelector('[data-count="down"]').textContent = state.down;
      box.querySelectorAll(".rrt-vote").forEach(function (btn) {
        var value = Number(btn.getAttribute("data-vote"));
        btn.setAttribute("aria-pressed", String(mine() === value));
        btn.setAttribute(
          "aria-label",
          value === 1
            ? L("Thumbs up, helpful", "إعجاب، مفيد")
            : L("Thumbs down, not helpful", "عدم إعجاب، غير مفيد"),
        );
        btn.disabled = state.saving;
      });
      var share = box.querySelector(".rrt-percent");
      share.textContent = total ? percent(state.up, state.down) + "%" : "";
      share.title = total
        ? L(
            percent(state.up, state.down) +
              "% positive from " +
              countLabel(total),
            percent(state.up, state.down) + "٪ إيجابي من " + countLabel(total),
          )
        : "";
      box.querySelector(".rrt-summary").textContent =
        !total && state.available
          ? L("No ratings yet", "لا توجد تقييمات بعد")
          : "";
      box.querySelector(".rrt-status").textContent = state.status
        ? L(state.status[0], state.status[1])
        : "";
    }

    function ratingRef(fb) {
      return fb.firestore().collection(COLLECTION).doc(docId(path));
    }

    function save(want) {
      var fb = window.__shoug_fb;
      var user = state.user;
      if (!fb || !user || state.saving) return;
      var ref = ratingRef(fb);
      var FieldValue = fb.firestore.FieldValue;
      state.saving = true;
      state.status = null;
      paint();
      fb.firestore()
        .runTransaction(function (tx) {
          return tx.get(ref).then(function (snap) {
            if (!snap.exists) {
              var first = {};
              first[user.uid] = want;
              var fresh = {
                path: path,
                course: course,
                up: want === 1 ? 1 : 0,
                down: want === -1 ? 1 : 0,
                votes: first,
                updatedAt: FieldValue.serverTimestamp(),
              };
              tx.set(ref, fresh);
              return {
                up: fresh.up,
                down: fresh.down,
                vote: want,
                votes: first,
              };
            }
            var d = snap.data();
            var votes = d.votes || {};
            var old = votes[user.uid] || 0;
            var next = old === want ? 0 : want;
            var up = (d.up || 0) + (next === 1 ? 1 : 0) - (old === 1 ? 1 : 0);
            var down =
              (d.down || 0) + (next === -1 ? 1 : 0) - (old === -1 ? 1 : 0);
            var change = {
              up: up,
              down: down,
              updatedAt: FieldValue.serverTimestamp(),
            };
            change["votes." + user.uid] = next || FieldValue.delete();
            tx.update(ref, change);
            return { up: up, down: down, vote: next, votes: votes };
          });
        })
        .then(function (result) {
          state.up = result.up;
          state.down = result.down;
          state.votes = result.votes;
          if (result.vote) state.votes[user.uid] = result.vote;
          else delete state.votes[user.uid];
          state.available = true;
          state.status = result.vote
            ? ["Thanks for the feedback!", "شكرًا على رأيك!"]
            : null;
          clearCache(course);
        })
        .catch(function () {
          state.status = [
            "Couldn't save your rating. Try again.",
            "تعذّر حفظ تقييمك. حاول مرة أخرى.",
          ];
        })
        .then(function () {
          state.saving = false;
          paint();
        });
    }

    function wasSignedIn() {
      try {
        return localStorage.getItem("shoug-was-signed-in") === "1";
      } catch (e) {
        return false;
      }
    }

    function openSignIn() {
      if (typeof window.__shougOpenAuthModal === "function")
        window.__shougOpenAuthModal();
      else if (typeof window.__shougLoadFirebaseAuth === "function")
        window.__shougLoadFirebaseAuth(true);
    }

    box.addEventListener("click", function (e) {
      var btn = e.target.closest(".rrt-vote");
      if (!btn) return;
      var want = Number(btn.getAttribute("data-vote"));
      if (state.user) return save(want);
      // Hold the vote; it is applied as soon as the student is signed in.
      state.pending = want;
      if (!state.authReady && wasSignedIn()) {
        state.status = ["Signing you in…", "جارٍ تسجيل دخولك…"];
      } else {
        state.status = ["Sign in to rate.", "سجّل الدخول للتقييم."];
        openSignIn();
      }
      paint();
    });

    function watchAuth(fb) {
      fb.auth().onAuthStateChanged(function (user) {
        var restoring = !state.authReady;
        state.authReady = true;
        state.user = user || null;
        if (user && state.pending) {
          var want = state.pending;
          state.pending = 0;
          return save(want);
        }
        if (!user && state.pending && restoring) {
          state.status = ["Sign in to rate.", "سجّل الدخول للتقييم."];
          openSignIn();
        } else if (user) {
          state.status = null;
        }
        paint();
      });
    }

    if (window.__shoug_fb) watchAuth(window.__shoug_fb);
    else {
      window.addEventListener(
        "shoug:fb",
        function () {
          watchAuth(window.__shoug_fb);
        },
        { once: true },
      );
      // Needed to show their earlier vote; everyone else loads it on first click.
      if (wasSignedIn() && typeof window.__shougLoadFirebaseAuth === "function")
        window.__shougLoadFirebaseAuth(false);
    }

    onLangChange(paint);
    paint();

    fetch(API + "/" + COLLECTION + "/" + encodeURIComponent(docId(path)))
      .then(function (r) {
        if (r.status === 404) return null;
        if (!r.ok) throw new Error(String(r.status));
        return r.json();
      })
      .then(function (doc) {
        state.available = true;
        if (state.saving) return;
        var f = doc && doc.fields;
        state.up = intField(f, "up");
        state.down = intField(f, "down");
        var votes = {};
        var raw = (f && f.votes && f.votes.mapValue.fields) || {};
        Object.keys(raw).forEach(function (uid) {
          votes[uid] = Number(raw[uid].integerValue);
        });
        state.votes = votes;
        paint();
      })
      .catch(function () {
        paint();
      });
  }

  // ── Start ────────────────────────────────────────────────────────────────

  function start() {
    var url = new URL(location.href);
    var pathname = url.pathname.replace(/index\.html$/, "");
    var course = courseOf(pathname);
    if (!course || EXCLUDED[course]) return;

    var rest = pathname
      .slice(pathname.indexOf("/" + course + "/") + course.length + 2)
      .split("/")
      .filter(Boolean);
    var isViewer = rest[0] === "viewer" && url.searchParams.get("src");

    if (!rest.length || document.querySelector(".directory-container"))
      initListing(course);
    else if (
      (isViewer || rest.length >= 2) &&
      !document.querySelector(".coming-soon-container")
    )
      initWidget(course, resourcePath(url));
  }

  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", start);
  else start();
})();
