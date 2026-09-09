/**
 * Video lesson pages: like/dislike reactions and the discussion box.
 *
 * Reactions live in Firestore under pageReactions/{key}/votes/{uid}, one
 * document per person, so a vote is a toggle and the tallies are exact. Counts
 * are read over the Firestore REST API so a signed-out visitor never pays for
 * the SDK; voting itself needs the SDK and an account.
 *
 * The discussion reuses the site-wide comment section from firebase-auth.js:
 * once that script injects #shoug-page-comments (signed-in only, appended to
 * the end of <main>) this moves it into the slot on the page. Signed-out
 * visitors get a read-only rendering of the same thread over REST, plus a
 * sign-in prompt.
 *
 * Requires: pageReactions read/write rules in Firestore (see
 * scripts/build_ethics_video_pages.py for the snippet).
 */
(function () {
  "use strict";

  var root = document.querySelector("[data-video-lesson]");
  if (!root) return;

  var PROJECT = "shoug-tech";
  var API = "https://firestore.googleapis.com/v1/projects/" + PROJECT + "/databases/(default)/documents/";
  var reactionKey = root.getAttribute("data-reaction-key");
  var pending = null;   // a vote clicked while signed out, applied after sign-in
  var myVote = 0;
  var counts = { up: 0, down: 0 };

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function commentSlug() {
    return window.location.pathname.replace(/\//g, "|").replace(/^\|/, "");
  }

  // ── Reactions ─────────────────────────────────────────────────────────────

  var widget = root.querySelector("[data-video-reactions]");
  var hint = root.querySelector("[data-reactions-hint]");

  function paint() {
    root.querySelectorAll("[data-vote]").forEach(function (btn) {
      var dir = btn.getAttribute("data-vote");
      var mine = (dir === "up" && myVote === 1) || (dir === "down" && myVote === -1);
      btn.classList.toggle("is-active", mine);
      btn.setAttribute("aria-pressed", mine ? "true" : "false");
      var out = btn.querySelector("[data-count]");
      if (out) out.textContent = counts[dir];
    });
  }

  function setHint(text) {
    if (!hint) return;
    hint.textContent = text;
    hint.hidden = !text;
  }

  function readCounts() {
    if (!reactionKey) return;
    var url = API + "pageReactions/" + encodeURIComponent(reactionKey) + "/votes?pageSize=300";
    fetch(url).then(function (r) {
      if (!r.ok) throw new Error(String(r.status));
      return r.json();
    }).then(function (data) {
      var docs = data.documents || [];
      counts = { up: 0, down: 0 };
      docs.forEach(function (doc) {
        var value = doc.fields && doc.fields.value && Number(doc.fields.value.integerValue);
        if (value === 1) counts.up += 1;
        else if (value === -1) counts.down += 1;
      });
      paint();
    }).catch(function () {
      // Rules not in place yet, or offline. The buttons stay usable for
      // anyone signed in; the tallies simply have nothing to show.
      paint();
    });
  }

  function watchMyVote(user) {
    if (!user || !reactionKey) { myVote = 0; paint(); return; }
    voteDoc(user.uid).onSnapshot(function (doc) {
      myVote = doc.exists ? Number(doc.data().value) || 0 : 0;
      paint();
    }, function () { });
  }

  function voteDoc(uid) {
    return window.firebase.firestore()
      .collection("pageReactions").doc(reactionKey)
      .collection("votes").doc(uid);
  }

  function applyVote(dir) {
    var user = window.firebase && window.firebase.auth().currentUser;
    if (!user) {
      pending = dir;
      setHint("Sign in to vote.");
      openAccount();
      return;
    }
    var want = dir === "up" ? 1 : -1;
    var next = myVote === want ? 0 : want;
    // Optimistic: the snapshot below confirms or corrects it.
    counts.up += (next === 1 ? 1 : 0) - (myVote === 1 ? 1 : 0);
    counts.down += (next === -1 ? 1 : 0) - (myVote === -1 ? 1 : 0);
    myVote = next;
    paint();

    var ref = voteDoc(user.uid);
    var write = next === 0 ? ref.delete() : ref.set({
      value: next,
      page: window.location.pathname,
      updatedAt: window.firebase.firestore.FieldValue.serverTimestamp()
    });
    write.then(function () { setHint(""); }).catch(function () {
      setHint("Could not save your vote.");
      readCounts();
    });
  }

  if (widget) {
    root.querySelectorAll("[data-vote]").forEach(function (btn) {
      btn.addEventListener("click", function () { applyVote(btn.getAttribute("data-vote")); });
    });
    readCounts();
  }

  // ── Discussion ────────────────────────────────────────────────────────────

  var slot = root.querySelector("[data-discussion-slot]");
  var prompt = root.querySelector("[data-discussion-prompt]");
  var preview = root.querySelector("[data-discussion-preview]");

  function openAccount() {
    if (typeof window.__shougOpenAuthModal === "function") {
      window.__shougOpenAuthModal();
      return;
    }
    window.dispatchEvent(new CustomEvent("shoug:load-account", { detail: { open: true } }));
  }

  var signInBtn = root.querySelector("[data-discussion-signin]");
  if (signInBtn) signInBtn.addEventListener("click", openAccount);

  /** Move the injected comment section into the page instead of after it. */
  function adoptCommentSection() {
    var injected = document.getElementById("shoug-page-comments");
    if (!injected || !slot) return false;
    if (injected.parentNode !== slot) slot.appendChild(injected);
    if (prompt) prompt.hidden = true;
    if (preview) preview.hidden = true;
    return true;
  }

  if (slot) {
    if (!adoptCommentSection()) {
      // firebase-auth.js appends the section to the end of <main>.
      var host = document.querySelector("main") || document.body;
      new MutationObserver(function () { adoptCommentSection(); })
        .observe(host, { childList: true });
    }
  }

  /** Read-only rendering of the thread for visitors who are not signed in. */
  function renderPreview() {
    if (!preview) return;
    var url = API + "pageComments/" + encodeURIComponent(commentSlug()) + "/comments?pageSize=100";
    fetch(url).then(function (r) {
      if (!r.ok) throw new Error(String(r.status));
      return r.json();
    }).then(function (data) {
      if (document.getElementById("shoug-page-comments")) return;
      var docs = (data.documents || []).map(function (doc) {
        var f = doc.fields || {};
        return {
          id: (doc.name || "").split("/").pop(),
          text: f.text && f.text.stringValue,
          author: (f.displayName && f.displayName.stringValue) || (f.username && f.username.stringValue),
          username: f.username && f.username.stringValue,
          color: (f.avatarColor && f.avatarColor.stringValue) || "#b829ea",
          replyTo: f.replyTo && f.replyTo.stringValue,
          at: f.createdAt && f.createdAt.timestampValue
        };
      }).filter(function (c) { return c.text; });

      if (!docs.length) { preview.hidden = true; return; }
      docs.sort(function (a, b) { return String(a.at).localeCompare(String(b.at)); });

      var replies = {};
      docs.forEach(function (c) {
        if (!c.replyTo) return;
        (replies[c.replyTo] = replies[c.replyTo] || []).push(c);
      });

      function item(c, isReply) {
        var when = c.at ? new Date(c.at).toLocaleDateString("en-US",
          { month: "short", day: "numeric", year: "numeric" }) : "";
        return '<li class="video-comment' + (isReply ? " video-comment--reply" : "") + '">'
          + '<div class="video-comment-meta">'
          + '<span class="video-comment-author" style="color:' + esc(c.color) + '">' + esc(c.author || "Unknown") + '</span>'
          + (c.username ? '<span class="video-comment-user">@' + esc(c.username) + '</span>' : "")
          + '<span class="video-comment-time">' + esc(when) + '</span>'
          + '</div><p class="video-comment-text">' + esc(c.text) + '</p></li>';
      }

      var html = docs.filter(function (c) { return !c.replyTo; }).map(function (c) {
        return item(c, false) + (replies[c.id] || []).map(function (r) { return item(r, true); }).join("");
      }).join("");
      preview.innerHTML = '<ul class="video-comment-list">' + html + '</ul>';
      preview.hidden = false;
    }).catch(function () { });
  }

  renderPreview();

  // ── Auth state ────────────────────────────────────────────────────────────

  function onAuth(user) {
    watchMyVote(user);
    if (user) {
      setHint("");
      if (pending) { var dir = pending; pending = null; applyVote(dir); }
    } else {
      myVote = 0;
      paint();
      readCounts();
      // firebase-auth.js pulls its comment section on sign-out; put the
      // read-only view and the prompt back.
      if (prompt) prompt.hidden = false;
      renderPreview();
    }
  }

  function hookAuth() {
    if (!window.firebase || !window.firebase.auth) return;
    // Chain rather than replace: firebase-auth.js calls whatever is here.
    var previous = window.__shoug_onAuth;
    window.__shoug_onAuth = function (user) {
      if (typeof previous === "function") previous(user);
      onAuth(user);
    };
    window.firebase.auth().onAuthStateChanged(onAuth);
  }

  if (window.firebase && window.firebase.auth) hookAuth();
  else window.addEventListener("shoug:fb", hookAuth, { once: true });
})();
