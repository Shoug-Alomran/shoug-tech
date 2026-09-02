/* SE311 standalone-page behaviour.

   Purely additive: every page is fully readable with this file blocked. It
   only adds the motion and the wayfinding that the stylesheet leaves hooks
   for -- scroll reveals, the active anchor in the topbar/sidebar, and the
   back-to-top affordance. Theming is not handled here; that is resolved
   before first paint by the inline boot script on each page. */
(function () {
    "use strict";

    var reduced = window.matchMedia &&
        window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    /* ---------------------------------------------------------- reveal -- */

    function markReveals() {
        if (reduced || !("IntersectionObserver" in window)) return;

        /* Top-level blocks only: revealing nested cards individually makes
           long study pages feel like they are loading forever. */
        var blocks = document.querySelectorAll(
            ".section, .page-section, .question, .question-block, .q-card, " +
            ".chapter-card, .card-grid, .process-flow, .table-wrap, .toc, " +
            ".quick-ref, .callout, .hero-stats"
        );
        if (!blocks.length) return;

        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (!entry.isIntersecting) return;
                entry.target.setAttribute("data-se-reveal", "in");
                io.unobserve(entry.target);
            });
        }, { rootMargin: "0px 0px -8% 0px", threshold: 0.04 });

        blocks.forEach(function (el, i) {
            /* A block already on screen at load gets a short stagger; the
               rest reveal as they are scrolled to, with no delay. */
            if (el.closest("[data-se-reveal]")) return;
            el.setAttribute("data-se-reveal", "");
            var rect = el.getBoundingClientRect();
            if (rect.top < window.innerHeight) {
                el.style.setProperty("--se-delay", Math.min(i, 6) * 55 + "ms");
            }
            io.observe(el);
        });
    }

    /* ------------------------------------------------------ active link -- */

    function trackActiveSection() {
        var links = document.querySelectorAll(
            '.topbar-nav a[href^="#"], .sidebar a[href^="#"], .toc a[href^="#"]'
        );
        if (!links.length || !("IntersectionObserver" in window)) return;

        var byId = {};
        links.forEach(function (link) {
            var id = link.getAttribute("href").slice(1);
            if (!id) return;
            (byId[id] = byId[id] || []).push(link);
        });

        var targets = Object.keys(byId)
            .map(function (id) { return document.getElementById(id); })
            .filter(Boolean);
        if (!targets.length) return;

        var visible = new Set();

        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) visible.add(entry.target.id);
                else visible.delete(entry.target.id);
            });

            /* Highlight the first target in document order that is on screen,
               so scrolling up and down lands on the same link. */
            var current = null;
            for (var i = 0; i < targets.length; i += 1) {
                if (visible.has(targets[i].id)) { current = targets[i].id; break; }
            }

            links.forEach(function (link) { link.classList.remove("active"); });
            if (current && byId[current]) {
                byId[current].forEach(function (link) { link.classList.add("active"); });
            }
        }, { rootMargin: "-15% 0px -70% 0px", threshold: 0 });

        targets.forEach(function (target) { io.observe(target); });
    }

    /* ----------------------------------------------------- back to top -- */

    function backToTop() {
        var btn = document.querySelector(".scroll-top, .scrollToTop, #scrollTop, .back-to-top");
        if (!btn) return;

        var ticking = false;
        function update() {
            ticking = false;
            btn.classList.toggle("visible", window.scrollY > 420);
        }

        window.addEventListener("scroll", function () {
            if (ticking) return;
            ticking = true;
            window.requestAnimationFrame(update);
        }, { passive: true });

        update();

        if (!btn.getAttribute("onclick")) {
            btn.addEventListener("click", function () {
                window.scrollTo({ top: 0, behavior: reduced ? "auto" : "smooth" });
            });
        }
    }

    /* ------------------------------------------------------- wide tables -- */

    function wrapTables() {
        document.querySelectorAll("table").forEach(function (table) {
            if (table.closest(".table-wrap, .tbl-wrap, .sg-table-scroll, .diagram-scroll")) return;
            var wrap = document.createElement("div");
            wrap.className = "table-wrap";
            table.parentNode.insertBefore(wrap, table);
            wrap.appendChild(table);
        });
    }

    function init() {
        wrapTables();
        markReveals();
        trackActiveSection();
        backToTop();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
