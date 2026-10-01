(function () {
  "use strict";
  // Verification links remain single-use. Reload the actual Firebase user before
  // sending or showing an error, and never infer verification from URL parameters.
  const AUTO_COOLDOWN = 10 * 60 * 1000;
  const RESEND_COOLDOWN = 60 * 1000;
  window.ShougEmailVerification = {
    start({ user, isCurrent, onVerified, onStatus, onCooldown = () => {} }) {
      let stopped = false,
        checking = false,
        sending = false,
        finished = false;
      let lastSent = 0;
      const key = "shoug-verification-sent:" + user.uid;
      try {
        lastSent = Number(localStorage.getItem(key)) || 0;
      } catch {}
      const active = () => !stopped && isCurrent();
      function remember(time) {
        lastSent = time;
        try {
          localStorage.setItem(key, String(time));
        } catch {}
      }
      function cooldown() {
        if (active())
          onCooldown(
            Math.max(
              0,
              Math.ceil((lastSent + RESEND_COOLDOWN - Date.now()) / 1000),
            ),
            sending,
          );
      }
      async function refresh() {
        if (!active() || checking || finished) return false;
        checking = true;
        try {
          await user.reload();
          if (!active()) return false;
          if (!user.emailVerified) return false;
          await user.getIdToken(true);
          if (!active()) return false;
          finished = true;
          stop();
          onVerified(user);
          return true;
        } catch {
          return false;
        } finally {
          checking = false;
        }
      }
      async function send(manual = false) {
        if (!active() || sending || finished) return;
        if (await refresh()) return;
        if (!active()) return;
        try {
          lastSent = Math.max(lastSent, Number(localStorage.getItem(key)) || 0);
        } catch {}
        const wait = manual ? RESEND_COOLDOWN : AUTO_COOLDOWN;
        if (Date.now() - lastSent < wait) {
          onStatus(
            "Check your inbox for the latest verification email. This page will continue automatically after you open the link.",
          );
          cooldown();
          return;
        }
        sending = true;
        // Reserve before sending to avoid repeat emails on reload or in another tab.
        remember(Date.now());
        cooldown();
        onStatus("Sending a verification link to " + user.email + "…");
        try {
          try {
            await user.sendEmailVerification({
              url: "https://shoug-tech.com/checkout/ethics/",
              handleCodeInApp: false,
            });
          } catch (error) {
            if (
              ![
                "auth/unauthorized-continue-uri",
                "auth/invalid-continue-uri",
              ].includes(error.code)
            )
              throw error;
            // Some existing Firebase projects have not authorized a continue URL.
            // Default Firebase email handling still works with the automatic watcher.
            await user.sendEmailVerification();
          }
          if (active())
            onStatus(
              "We sent a link to " +
                user.email +
                ". Open it in your inbox; this page will continue automatically.",
            );
        } catch (error) {
          if (active())
            onStatus(
              error.code === "auth/too-many-requests"
                ? "An email was requested recently. Use the latest link in your inbox, or wait a minute before requesting a new one."
                : "We couldn’t send the email. Check your connection, then use ‘Send a new link’ below.",
            );
        } finally {
          sending = false;
          cooldown();
        }
      }
      function wake() {
        if (document.visibilityState !== "hidden") refresh();
      }
      function storage(event) {
        if (event.key === key) {
          lastSent = Number(event.newValue) || 0;
          cooldown();
        }
      }
      const poll = setInterval(wake, 5000);
      const tick = setInterval(cooldown, 1000);
      window.addEventListener("focus", wake);
      document.addEventListener("visibilitychange", wake);
      window.addEventListener("storage", storage);
      function stop() {
        stopped = true;
        clearInterval(poll);
        clearInterval(tick);
        window.removeEventListener("focus", wake);
        document.removeEventListener("visibilitychange", wake);
        window.removeEventListener("storage", storage);
      }
      send();
      return { stop, resend: () => send(true), refresh };
    },
  };
})();
