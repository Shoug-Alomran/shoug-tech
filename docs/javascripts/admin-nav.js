/**
 * Adds an "Admin" tab after "About" in the site header, for the site
 * administrator only (the account in courseCommerce/ethics.adminUid, with a
 * verified email). Added to every page by functions/_middleware.js.
 *
 * This only decides what the menu shows. Every admin page and the analytics
 * worker check the account again on the server side, so hiding or revealing
 * this link grants nothing.
 */
(function () {
  "use strict";
  if (window.__shougAdminNav) return;
  window.__shougAdminNav = true;

  var CACHE = "shoug-admin-uid";

  function get(key) {
    try {
      return localStorage.getItem(key);
    } catch (e) {
      return null;
    }
  }
  function set(key, value) {
    try {
      if (value === null) localStorage.removeItem(key);
      else localStorage.setItem(key, value);
    } catch (e) {}
  }

  function navs() {
    return document.querySelectorAll(".shoug-header-nav");
  }

  function show() {
    navs().forEach(function (nav) {
      if (nav.querySelector(".shoug-admin-tab")) return;
      var link = document.createElement("a");
      link.href = "/admin/";
      link.className = "shoug-admin-tab";
      link.textContent = "Admin";
      link.setAttribute("data-ar-text", "الإدارة");
      if (location.pathname.indexOf("/admin") === 0) {
        link.classList.add("active");
        link.setAttribute("aria-current", "page");
      }
      var about = nav.querySelector('a[href="/about/"]');
      if (about) about.after(link);
      else nav.appendChild(link);
    });
  }

  function hide() {
    document.querySelectorAll(".shoug-admin-tab").forEach(function (el) {
      el.remove();
    });
  }

  function check(fb, user) {
    if (!user || !user.emailVerified) {
      set(CACHE, null);
      hide();
      return;
    }
    // Show at once for the account last confirmed as admin, then re-check.
    if (get(CACHE) === user.uid) show();
    fb.firestore()
      .collection("courseCommerce")
      .doc("ethics")
      .get()
      .then(function (snap) {
        var current = fb.auth().currentUser;
        if (!current || current.uid !== user.uid) return;
        var admin = snap.exists && snap.data().adminUid === user.uid;
        set(CACHE, admin ? user.uid : null);
        if (admin) show();
        else hide();
      })
      .catch(function () {});
  }

  function boot() {
    var fb = window.__shoug_fb;
    if (!fb || !fb.auth) return;
    fb.auth().onAuthStateChanged(function (user) {
      check(fb, user);
    });
  }

  function start() {
    if (window.__shoug_fb) boot();
    else window.addEventListener("shoug:fb", boot, { once: true });
  }
  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", start);
  else start();
})();
