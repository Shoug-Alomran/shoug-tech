(function () {
  "use strict";
  const status = document.getElementById("access-status");
  const signIn = document.getElementById("access-signin");
  const check = document.getElementById("access-check");
  let firebase,
    generation = 0;
  const ROOT = "/academics/other-courses/ethcs303/";
  const next = new URLSearchParams(location.search).get("next");
  let destination = location.pathname.startsWith("/course-access")
    ? ROOT
    : location.pathname + location.search;
  if (next) {
    try {
      const url = new URL(next, location.origin);
      if (
        url.origin === location.origin &&
        (url.pathname.startsWith(ROOT) ||
          url.pathname.startsWith("/course-media/ethics/"))
      )
        destination = url.pathname + url.search;
    } catch {}
  }
  // Static previews cannot set the live site's secure, host-only session cookie.
  // Do not request a token or POST it to a server that cannot handle sessions.
  if (!["shoug-tech.com", "www.shoug-tech.com"].includes(location.hostname)) {
    signIn.hidden = true;
    check.hidden = true;
    status.textContent = "You’re viewing a local preview. Open the live website and sign in with your approved account to access the course.";
    const live = document.createElement("a");
    live.className = "button primary";
    live.href = "https://shoug-tech.com/course-access/?next=" + encodeURIComponent(destination);
    live.textContent = "Open my course on shoug-tech.com →";
    check.parentElement.append(live);
    return;
  }
  async function verify(user) {
    const version = ++generation;
    if (!user) {
      await fetch("/course-access/session", {
        method: "DELETE",
        credentials: "same-origin",
      }).catch(() => {});
      if (version !== generation) return;
      signIn.hidden = false;
      check.hidden = true;
      status.textContent =
        "Sign in with the account you used to purchase the course.";
      return;
    }
    signIn.hidden = true;
    check.hidden = false;
    check.disabled = true;
    status.textContent = "Checking your approved purchase…";
    try {
      const response = await fetch("/course-access/session", {
        method: "POST",
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ idToken: await user.getIdToken(true) }),
      });
      if (version !== generation) return;
      const result = await response.json();
      if (response.ok && result.approved === true) {
        // Public GitHub Pages mirrors and localhost must not serve private content.
        if (
          !["shoug-tech.com", "www.shoug-tech.com"].includes(location.hostname)
        ) {
          status.textContent =
            "Open shoug-tech.com to access your course securely.";
          return;
        }
        location.replace(destination);
        return;
      }
      status.textContent =
        response.status === 403
          ? "Your course purchase is not approved yet. Complete the bank transfer, or wait for your submitted receipt to be reviewed."
          : response.status === 401
            ? "Please verify your email and sign in again."
            : "Access verification is temporarily unavailable. Your material remains protected. Please try again.";
    } catch {
      if (version === generation)
        status.textContent =
          "We couldn’t check your access. Please try again, or open shoug-tech.com if you are viewing a preview.";
    } finally {
      if (version === generation) check.disabled = false;
    }
  }
  signIn.addEventListener("click", () => window.__shougOpenAuthModal?.());
  check.addEventListener("click", () => verify(firebase.auth().currentUser));
  function boot() {
    if (firebase) return;
    firebase = window.__shoug_fb;
    firebase.auth().onAuthStateChanged(verify);
  }
  if (window.__shoug_fb) boot();
  else window.addEventListener("shoug:fb", boot, { once: true });
})();
