/* ==========================================================================
   CYS401 slide-breakdown shared theme + chrome controller
   · resolves the theme from the site key ('shoug-theme'), the embedding
     wrapper, or the OS preference — in that order
   · keeps the page in sync with the wrapper when the site theme is toggled
   · injects the floating rail (theme toggle, back to top, print) and the
     reading-progress bar
   · wraps wide tables so they scroll instead of breaking the layout
   ========================================================================== */
(function () {
    "use strict";

    var KEY = "shoug-theme";
    var root = document.documentElement;

    function osTheme() {
        return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    }

    function stored() {
        try {
            var v = localStorage.getItem(KEY);
            return v === "light" || v === "dark" ? v : null;
        } catch (e) { return null; }
    }

    function apply(theme, persist) {
        if (theme !== "light" && theme !== "dark") return;
        root.setAttribute("data-theme", theme);
        root.style.colorScheme = theme;
        if (persist) { try { localStorage.setItem(KEY, theme); } catch (e) {} }
        var btn = document.getElementById("bdThemeBtn");
        if (btn) {
            btn.innerHTML = theme === "dark" ? SUN + tip("Light mode") : MOON + tip("Dark mode");
            btn.setAttribute("aria-label", theme === "dark" ? "Switch to light mode" : "Switch to dark mode");
        }
    }

    function current() { return root.getAttribute("data-theme") === "dark" ? "dark" : "light"; }

    /* ---- initial resolve: stored choice, else OS ---- */
    apply(stored() || osTheme(), false);

    /* ---- follow the OS while no explicit choice has been made ---- */
    if (window.matchMedia) {
        var mq = window.matchMedia("(prefers-color-scheme: dark)");
        var onMQ = function (e) { if (!stored()) apply(e.matches ? "dark" : "light", false); };
        if (mq.addEventListener) mq.addEventListener("change", onMQ);
        else if (mq.addListener) mq.addListener(onMQ);
    }

    /* ---- follow the site chrome when embedded, and other tabs ---- */
    window.addEventListener("message", function (e) {
        if (!e.data || e.data.type !== "shoug-theme") return;
        apply(e.data.theme, false);
    });
    window.addEventListener("storage", function (e) {
        if (e.key === KEY && e.newValue) apply(e.newValue, false);
    });

    var SUN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>';
    var MOON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"/></svg>';
    var UP = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg>';
    var PRINT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round"><path d="M6 9V3h12v6M6 18H4v-6h16v6h-2M8 14h8v7H8z"/></svg>';

    function tip(t) { return '<span class="bd-tip">' + t + "</span>"; }

    function build() {
        root.classList.add("bd-ready");

        /* reading progress */
        var bar = document.createElement("div");
        bar.className = "bd-progress";
        bar.innerHTML = "<i></i>";
        document.body.appendChild(bar);
        var fill = bar.firstChild;

        /* control rail */
        var rail = document.createElement("div");
        rail.className = "bd-rail";

        var themeBtn = document.createElement("button");
        themeBtn.id = "bdThemeBtn";
        themeBtn.type = "button";
        themeBtn.addEventListener("click", function () {
            var next = current() === "dark" ? "light" : "dark";
            apply(next, true);
            /* tell the wrapper so the site chrome follows too */
            try {
                if (window.parent && window.parent !== window) {
                    window.parent.postMessage({ type: "shoug-theme", theme: next }, "*");
                }
            } catch (e) {}
        });

        var topBtn = document.createElement("button");
        topBtn.type = "button";
        topBtn.className = "bd-hidden";
        topBtn.setAttribute("aria-label", "Back to top");
        topBtn.innerHTML = UP + tip("Back to top");
        topBtn.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });

        var printBtn = document.createElement("button");
        printBtn.type = "button";
        printBtn.setAttribute("aria-label", "Print this breakdown");
        printBtn.innerHTML = PRINT + tip("Print");
        printBtn.addEventListener("click", function () { window.print(); });

        rail.appendChild(themeBtn);
        rail.appendChild(topBtn);
        rail.appendChild(printBtn);
        document.body.appendChild(rail);
        apply(current(), false);

        /* wide tables scroll instead of overflowing */
        Array.prototype.forEach.call(document.querySelectorAll("table"), function (t) {
            if (t.parentElement && t.parentElement.classList.contains("bd-table-scroll")) return;
            var w = document.createElement("div");
            w.className = "bd-table-scroll";
            t.parentNode.insertBefore(w, t);
            w.appendChild(t);
        });

        var ticking = false;
        function onScroll() {
            if (ticking) return;
            ticking = true;
            requestAnimationFrame(function () {
                var h = document.documentElement.scrollHeight - window.innerHeight;
                var y = window.scrollY || document.documentElement.scrollTop;
                fill.style.width = (h > 0 ? Math.min(100, (y / h) * 100) : 0) + "%";
                topBtn.classList.toggle("bd-hidden", y < 400);
                ticking = false;
            });
        }
        window.addEventListener("scroll", onScroll, { passive: true });
        window.addEventListener("resize", onScroll);
        onScroll();
    }

    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", build);
    else build();
})();
