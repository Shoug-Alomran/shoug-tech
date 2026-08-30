/* Scroll-reveal for the editorial breakdown pages.
   Adds .has-reveal only when it can actually observe, so the page stays
   fully visible if this never runs. Honours prefers-reduced-motion. */
(function () {
    "use strict";
    var root = document.documentElement;
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    function start() {
        var blocks = document.querySelectorAll(".section, .table-of-contents");
        if (!blocks.length) return;

        // stagger index for the cards inside each block
        Array.prototype.forEach.call(blocks, function (b) {
            var kids = b.querySelectorAll(
                ".card, .component-card, .cia-element, .dimension, .aaa-element," +
                ".threat-item, .countermeasure-item, .layer-item, .lifecycle-phase");
            Array.prototype.forEach.call(kids, function (k, i) {
                k.style.setProperty("--i", Math.min(i, 12));
            });
        });

        if (reduce || !("IntersectionObserver" in window)) {
            Array.prototype.forEach.call(blocks, function (b) { b.classList.add("in-view"); });
            return;
        }

        root.classList.add("has-reveal");
        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (e) {
                if (!e.isIntersecting) return;
                e.target.classList.add("in-view");
                io.unobserve(e.target);
            });
        }, { rootMargin: "0px 0px -12% 0px", threshold: 0.06 });

        Array.prototype.forEach.call(blocks, function (b) { io.observe(b); });

        // anything already on screen shows immediately
        requestAnimationFrame(function () {
            Array.prototype.forEach.call(blocks, function (b) {
                if (b.getBoundingClientRect().top < window.innerHeight) b.classList.add("in-view");
            });
        });
    }

    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
    else start();
})();
