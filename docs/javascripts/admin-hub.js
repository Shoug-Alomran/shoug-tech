/**
 * The admin home (/admin/) and question reports (/admin/reports/).
 *
 * Both pages show content only to the account in courseCommerce/ethics.adminUid
 * with a verified email. That check here only decides what to display: the
 * Firestore rules (transferAdmin()) are what refuse everyone else's reads.
 * Student-written text is inserted with textContent, never as HTML.
 */
(function () {
  "use strict";
  var page = document.body.getAttribute("data-admin-page");
  var $ = function (id) {
    return document.getElementById(id);
  };
  var REASONS = {
    answer: "Wrong answer",
    unclear: "Unclear question",
    missing: "Missing option or content",
    chapter: "Wrong chapter",
    other: "Other",
  };

  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    for (var k in attrs || {}) {
      if (k === "text") node.textContent = attrs[k];
      else if (k === "class") node.className = attrs[k];
      else if (k.slice(0, 2) === "on") node.addEventListener(k.slice(2), attrs[k]);
      else node.setAttribute(k, attrs[k]);
    }
    (children || []).forEach(function (c) {
      if (c !== null && c !== undefined)
        node.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
    });
    return node;
  }

  function status(text, isError) {
    var s = $("ah-status");
    s.textContent = text;
    s.hidden = !text;
    s.classList.toggle("is-error", !!isError);
  }

  function isAdmin(fb, user) {
    if (!user.emailVerified) return Promise.resolve(false);
    return fb
      .firestore()
      .collection("courseCommerce")
      .doc("ethics")
      .get()
      .then(function (snap) {
        return snap.exists && snap.data().adminUid === user.uid;
      });
  }

  // ---------------------------------------------------------------- home --
  function loadHome(fb) {
    var db = fb.firestore();
    var pending = $("ah-pending");
    db.collection("courseTransfers")
      .where("status", "==", "pending")
      .limit(10)
      .get()
      .then(function (snap) {
        pending.textContent = snap.size >= 10 ? "10+ waiting" : snap.size ? snap.size + " waiting" : "None waiting";
        pending.classList.toggle("has-items", snap.size > 0);
      })
      .catch(function () {
        pending.textContent = "";
      });
    var reports = $("ah-reports");
    db.collection("questionReports")
      .limit(100)
      .get()
      .then(function (snap) {
        reports.textContent = snap.size >= 100 ? "100+ open" : snap.size ? snap.size + " open" : "None open";
        reports.classList.toggle("has-items", snap.size > 0);
      })
      .catch(function () {
        reports.textContent = "";
      });
  }

  // ------------------------------------------------------------- reports --
  var lastDoc = null;
  function when(ts) {
    var d = ts && ts.toDate ? ts.toDate() : null;
    return d
      ? d.toLocaleString("en-GB", { day: "numeric", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" })
      : "";
  }

  function reportCard(fb, doc) {
    var d = doc.data();
    var source = typeof d.source === "string" && d.source.charAt(0) === "/" ? d.source : "";
    var card = el("article", { class: "ah-report" }, [
      el("header", null, [
        el("strong", { text: String(d.course || "").toUpperCase() + " · Q" + (d.qid || "?") }),
        el("span", { class: "ah-chip", text: REASONS[d.reason] || d.reason || "Report" }),
        el("time", { text: when(d.createdAt) }),
      ]),
      d.question ? el("p", { class: "ah-question", text: d.question }) : null,
      d.note ? el("p", { class: "ah-note" }, [el("b", { text: "Student note: " }), d.note]) : null,
      el("footer", null, [
        source ? el("a", { href: source, target: "_blank", rel: "noopener", text: "Open the question page ↗" }) : null,
        el("button", {
          type: "button",
          text: "Resolve (delete)",
          onclick: function (event) {
            var button = event.currentTarget;
            if (!confirm("Delete this report? Do this once the question is fixed or the report is dismissed.")) return;
            button.disabled = true;
            doc.ref
              .delete()
              .then(function () {
                card.remove();
                if (!$("ah-report-list").children.length) status("No open reports.");
              })
              .catch(function (error) {
                button.disabled = false;
                alert("Couldn't delete: " + error.message);
              });
          },
        }),
      ]),
    ]);
    return card;
  }

  function loadReports(fb, more) {
    var list = $("ah-report-list");
    var query = fb.firestore().collection("questionReports").orderBy("createdAt", "desc").limit(25);
    if (more && lastDoc) query = query.startAfter(lastDoc);
    else list.textContent = "";
    status("Loading reports…");
    query
      .get()
      .then(function (snap) {
        status(!snap.size && !more ? "No open reports." : "");
        snap.forEach(function (doc) {
          list.appendChild(reportCard(fb, doc));
        });
        lastDoc = snap.docs[snap.docs.length - 1] || lastDoc;
        $("ah-more").hidden = snap.size < 25;
      })
      .catch(function (error) {
        status("Couldn't load reports: " + error.message, true);
      });
  }

  // ---------------------------------------------------------------- boot --
  function boot() {
    var fb = window.__shoug_fb;
    fb.auth().onAuthStateChanged(function (user) {
      $("ah-content").hidden = true;
      $("ah-login").hidden = !!user;
      if (!user) {
        status("");
        return;
      }
      status("Checking your account…");
      isAdmin(fb, user)
        .then(function (admin) {
          if (!admin) {
            status(
              user.emailVerified
                ? "This page is for the site administrator."
                : "Verify your email address to use the admin pages.",
              true,
            );
            return;
          }
          status("");
          $("ah-content").hidden = false;
          if (page === "home") loadHome(fb);
          if (page === "reports") loadReports(fb, false);
        })
        .catch(function (error) {
          status("Couldn't check your account: " + error.message, true);
        });
    });
  }

  $("ah-signin").addEventListener("click", function () {
    if (window.__shougOpenAuthModal) window.__shougOpenAuthModal();
    else status("Sign-in is still loading. Try again in a moment.");
  });
  if ($("ah-more"))
    $("ah-more").addEventListener("click", function () {
      loadReports(window.__shoug_fb, true);
    });
  if ($("ah-refresh"))
    $("ah-refresh").addEventListener("click", function () {
      loadReports(window.__shoug_fb, false);
    });
  if (window.__shoug_fb) boot();
  else window.addEventListener("shoug:fb", boot, { once: true });
})();
