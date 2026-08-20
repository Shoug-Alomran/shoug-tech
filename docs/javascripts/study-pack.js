/**
 * Study pack builder.
 *
 * Reads COURSE_PAGES (javascripts/course-manifest.js) and compiles one course's
 * material into a checklist grouped by section. Everything is derived from the
 * manifest the rest of the site already uses, so a pack can never list a page
 * that does not exist.
 */
(function () {
    'use strict';

    var SECTION_ORDER = ['slide-breakdowns', 'slides', 'extra-resources', 'exams'];
    var SECTION_LABELS = {
        'slide-breakdowns': 'Slide breakdowns',
        'slides': 'Slide decks',
        'extra-resources': 'Study material',
        'exams': 'Practice exams'
    };

    var select, output, meta, printBtn;

    function courses() {
        if (typeof COURSE_PAGES === 'undefined') return [];
        var seen = {};
        COURSE_PAGES.forEach(function (p) {
            if (!p.course) return;
            if (!seen[p.course]) {
                seen[p.course] = { code: p.course, track: p.track, url: p.courseUrl, count: 0 };
            }
            seen[p.course].count++;
        });
        return Object.keys(seen).sort().map(function (k) { return seen[k]; });
    }

    function pagesFor(code) {
        return COURSE_PAGES.filter(function (p) { return p.course === code; });
    }

    function sectionRank(s) {
        var i = SECTION_ORDER.indexOf(s);
        return i === -1 ? SECTION_ORDER.length : i;
    }

    /* Titles arrive as "SE322 | Chapter 4 Architecture Patterns"; the course
       code is already the heading, so drop the repeated prefix. */
    function cleanTitle(title, code) {
        var t = String(title || '').trim();
        var prefix = code.toUpperCase();
        if (t.toUpperCase().indexOf(prefix) === 0) {
            t = t.slice(prefix.length).replace(/^\s*[|/·—-]+\s*/, '');
        }
        return t || title;
    }

    function build(code) {
        output.innerHTML = '';
        meta.textContent = '';

        if (!code) {
            output.innerHTML = '<p class="pack-empty">Choose a course to build its pack.</p>';
            printBtn.disabled = true;
            return;
        }

        var pages = pagesFor(code);
        if (!pages.length) {
            output.innerHTML = '<p class="pack-empty">Nothing indexed for this course yet.</p>';
            printBtn.disabled = true;
            return;
        }

        var groups = {};
        pages.forEach(function (p) {
            var s = p.section || 'other';
            (groups[s] = groups[s] || []).push(p);
        });

        var sections = Object.keys(groups).sort(function (a, b) {
            return sectionRank(a) - sectionRank(b) || a.localeCompare(b);
        });

        var frag = document.createDocumentFragment();
        var total = 0;

        sections.forEach(function (s) {
            var wrap = document.createElement('section');
            wrap.className = 'pack-section';

            var h2 = document.createElement('h2');
            h2.textContent = (SECTION_LABELS[s] || s) + ' (' + groups[s].length + ')';
            wrap.appendChild(h2);

            groups[s]
                .sort(function (a, b) { return a.url.localeCompare(b.url); })
                .forEach(function (p) {
                    var row = document.createElement('div');
                    row.className = 'pack-row';

                    var box = document.createElement('span');
                    box.className = 'pack-box';
                    box.setAttribute('aria-hidden', 'true');

                    var a = document.createElement('a');
                    a.href = p.url;
                    a.textContent = cleanTitle(p.title, code);

                    row.appendChild(box);
                    row.appendChild(a);
                    wrap.appendChild(row);
                    total++;
                });

            frag.appendChild(wrap);
        });

        output.appendChild(frag);
        printBtn.disabled = false;
        meta.textContent = code.toUpperCase() + ' study pack — ' + total +
            ' items — shoug-tech.com';

        // Keep the chosen course in the URL so a pack can be linked or reopened.
        try {
            var url = new URL(window.location.href);
            url.searchParams.set('course', code);
            history.replaceState(null, '', url);
        } catch (e) { /* history is unavailable in some embedded contexts */ }
    }

    function init() {
        select = document.getElementById('pack-course');
        output = document.getElementById('pack-output');
        meta = document.getElementById('pack-meta');
        printBtn = document.getElementById('pack-print');
        if (!select || !output || !printBtn) return;

        var list = courses();
        if (!list.length) {
            output.innerHTML = '<p class="pack-empty">Course index unavailable.</p>';
            return;
        }

        list.forEach(function (c) {
            var opt = document.createElement('option');
            opt.value = c.code;
            opt.textContent = c.code.toUpperCase() + '  ·  ' + c.count + ' pages';
            select.appendChild(opt);
        });

        select.addEventListener('change', function () { build(select.value); });
        printBtn.addEventListener('click', function () { window.print(); });

        var preset = new URLSearchParams(window.location.search).get('course');
        if (preset && list.some(function (c) { return c.code === preset; })) {
            select.value = preset;
            build(preset);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
