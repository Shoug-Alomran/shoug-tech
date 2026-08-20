/**
 * Registers the service worker that keeps already-visited pages readable
 * offline. Registration is deliberately deferred to the load event so it never
 * competes with the page's own requests on a slow connection.
 */
(function () {
    'use strict';

    if (!('serviceWorker' in navigator)) return;
    // file:// previews have an opaque origin and registration always throws.
    if (location.protocol !== 'https:' && location.hostname !== 'localhost') return;

    window.addEventListener('load', function () {
        navigator.serviceWorker.register('/sw.js').then(function (reg) {
            reg.addEventListener('updatefound', function () {
                var incoming = reg.installing;
                if (!incoming) return;
                incoming.addEventListener('statechange', function () {
                    // A worker that reaches "installed" while one is already
                    // controlling the page is a pending update; activate it so
                    // the next navigation gets fresh content.
                    if (incoming.state === 'installed' && navigator.serviceWorker.controller) {
                        incoming.postMessage('skip-waiting');
                    }
                });
            });
        }).catch(function () {
            // An unavailable service worker is not worth surfacing; the site
            // works exactly as before without one.
        });
    });
})();
