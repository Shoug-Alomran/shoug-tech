/**
 * Registers the offline service worker and checks for a fresh worker after
 * page load. An activated update reloads an already-controlled page once so
 * cached markup and assets are replaced together.
 */
(function () {
  "use strict";

  if (!("serviceWorker" in navigator)) return;
  // file:// previews have an opaque origin and registration always throws.
  if (location.protocol !== "https:" && location.hostname !== "localhost")
    return;

  window.addEventListener("load", function () {
    navigator.serviceWorker
      .register("/sw.js", { updateViaCache: "none" })
      .then(function (reg) {
        function activateUpdate(incoming) {
          if (!incoming) return;
          incoming.addEventListener("statechange", function () {
            // A worker that reaches "installed" while one is already
            // controlling the page is a pending update; activate it so
            // the next navigation gets fresh content.
            if (
              incoming.state === "installed" &&
              navigator.serviceWorker.controller
            ) {
              incoming.postMessage("skip-waiting");
            }
          });
          // Registration may resolve after the browser already found an
          // update, so handle an installing worker that is already present.
          if (
            incoming.state === "installed" &&
            navigator.serviceWorker.controller
          ) {
            incoming.postMessage("skip-waiting");
          }
        }

        reg.addEventListener("updatefound", function () {
          activateUpdate(reg.installing);
        });
        activateUpdate(reg.installing);

        // Once a new worker takes control, reload only pages that were already
        // controlled. First-time registration should not interrupt the user.
        if (navigator.serviceWorker.controller) {
          navigator.serviceWorker.addEventListener(
            "controllerchange",
            function () {
              window.location.reload();
            },
            { once: true },
          );
        }

        // Don't let the browser's HTTP cache delay delivery of an updated
        // worker after a site deployment. Install listeners first so a quick
        // update cannot take control before the page is ready to react.
        reg.update().catch(function () {});
      })
      .catch(function () {
        // An unavailable service worker is not worth surfacing; the site
        // works exactly as before without one.
      });
  });
})();
