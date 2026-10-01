(function () {
  "use strict";
  let initialized = false;
  const destination = location.pathname + location.search;
  const gate = "/course-access/?next=" + encodeURIComponent(destination);
  function conceal() {
    document.querySelectorAll("video,audio").forEach((media) => {
      media.pause();
      media.removeAttribute("src");
      media.load();
    });
    document.documentElement.style.visibility = "hidden";
  }
  function boot() {
    if (initialized) return;
    initialized = true;
    window.__shoug_fb.auth().onIdTokenChanged(async (user) => {
      if (!user) {
        conceal();
        await fetch("/course-access/session", {
          method: "DELETE",
          credentials: "same-origin",
        }).catch(() => {});
        location.replace(gate);
        return;
      }
      try {
        const result = await fetch("/course-access/session", {
          method: "POST",
          credentials: "same-origin",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ idToken: await user.getIdToken() }),
        });
        if (!result.ok) {
          conceal();
          location.replace(gate);
        }
      } catch {
        conceal();
        location.replace(gate);
      }
    });
  }
  if (window.__shoug_fb) boot();
  else window.addEventListener("shoug:fb", boot, { once: true });
  // A restored page must recheck the server rather than reveal a back/forward cache.
  window.addEventListener("pageshow", (event) => {
    if (event.persisted) {
      conceal();
      location.reload();
    }
  });
})();
