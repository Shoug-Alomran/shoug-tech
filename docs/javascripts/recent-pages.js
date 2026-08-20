/**
 * "Continue where you left off".
 *
 * Records the last page visited in each course and offers them back on the
 * Academics hub. Deliberately localStorage-only and signed-out friendly: the
 * Firestore progress system in firebase-auth.js tracks completion for people
 * with an account, whereas this is about getting anyone back to the deck they
 * were reading ten minutes ago.
 *
 * Anything under /academics/<track>/<course>/ counts, keyed by course so a
 * term's browsing does not collapse into one long undifferentiated list.
 */
(function () {
    'use strict';

    var KEY = 'shoug-recent-pages';
    var MAX = 6;
    var COURSE = /^\/academics\/([^/]+)\/([^/]+)\//;

    function read() {
        try {
            var raw = JSON.parse(localStorage.getItem(KEY));
            return Array.isArray(raw) ? raw : [];
        } catch (e) {
            return [];
        }
    }

    function write(entries) {
        try {
            localStorage.setItem(KEY, JSON.stringify(entries.slice(0, MAX)));
        } catch (e) {
            // Private browsing or a full quota; the feature just goes quiet.
        }
    }

    function pageTitle() {
        var h1 = document.querySelector('h1:not(.shoug-visually-hidden)');
        if (h1 && h1.textContent.trim()) return h1.textContent.trim();
        return (document.title || '').split('—')[0].split('//')[0].trim();
    }

    function record() {
        var path = window.location.pathname;
        var m = path.match(COURSE);
        if (!m) return;

        // The course landing page is where the hub already sends people, so
        // recording it would make every entry point back to the same place.
        if (path === '/academics/' + m[1] + '/' + m[2] + '/') return;

        var entry = {
            url: path,
            title: pageTitle(),
            course: m[2].toUpperCase(),
            track: m[1],
            at: Date.now()
        };
        if (!entry.title) return;

        var entries = read().filter(function (e) { return e.course !== entry.course; });
        entries.unshift(entry);
        write(entries);
    }

    var CSS = [
        '.shoug-resume{margin:0 0 34px}',
        '.shoug-resume__head{display:flex;align-items:center;gap:12px;margin-bottom:14px;',
        'font-family:"JetBrains Mono",ui-monospace,monospace;font-size:0.66rem;font-weight:800;',
        'letter-spacing:0.18em;text-transform:uppercase;color:#8f8b9a}',
        '.shoug-resume__head button{appearance:none;background:none;border:none;padding:0;cursor:pointer;',
        'font:inherit;letter-spacing:inherit;color:#8f8b9a;text-decoration:underline;text-underline-offset:3px}',
        '.shoug-resume__head button:hover{color:#ff2a4b}',
        '.shoug-resume__grid{display:grid;gap:10px;grid-template-columns:repeat(auto-fill,minmax(240px,1fr))}',
        '.shoug-resume__card{display:flex;flex-direction:column;gap:6px;padding:14px 16px;text-decoration:none;',
        'border:1px solid rgba(184,41,234,0.24);background:rgba(10,5,20,0.5);',
        'transition:border-color 160ms ease,background 160ms ease}',
        '.shoug-resume__card:hover{border-color:#ff2a4b;background:rgba(184,41,234,0.08)}',
        '.shoug-resume__course{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:0.62rem;',
        'font-weight:800;letter-spacing:0.16em;color:#ff2a4b}',
        '.shoug-resume__title{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:0.78rem;',
        'line-height:1.5;color:#f8f7fb;overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}',
        'body.shoug-light-mode .shoug-resume__card{background:#fff;border-color:rgba(22,17,31,0.15)}',
        'body.shoug-light-mode .shoug-resume__title{color:#16111f}',
        'body.shoug-light-mode .shoug-resume__head,body.shoug-light-mode .shoug-resume__head button{color:#534a61}'
    ].join('');

    function injectStyles() {
        if (document.getElementById('shoug-resume-styles')) return;
        var el = document.createElement('style');
        el.id = 'shoug-resume-styles';
        el.textContent = CSS;
        document.head.appendChild(el);
    }

    function render() {
        if (window.location.pathname !== '/academics/') return;
        var entries = read();
        if (!entries.length) return;

        var host = document.querySelector('main .container') || document.querySelector('main');
        if (!host) return;

        injectStyles();

        var section = document.createElement('section');
        section.className = 'shoug-resume';
        section.setAttribute('aria-label', 'Continue where you left off');

        var head = document.createElement('div');
        head.className = 'shoug-resume__head';
        var label = document.createElement('span');
        label.textContent = '[ Continue where you left off ]';
        var clear = document.createElement('button');
        clear.type = 'button';
        clear.textContent = 'Clear';
        clear.addEventListener('click', function () {
            write([]);
            section.remove();
        });
        head.appendChild(label);
        head.appendChild(clear);

        var grid = document.createElement('div');
        grid.className = 'shoug-resume__grid';
        entries.forEach(function (e) {
            var a = document.createElement('a');
            a.className = 'shoug-resume__card';
            a.href = e.url;
            var c = document.createElement('span');
            c.className = 'shoug-resume__course';
            c.textContent = e.course;
            var t = document.createElement('span');
            t.className = 'shoug-resume__title';
            t.textContent = e.title;
            a.appendChild(c);
            a.appendChild(t);
            grid.appendChild(a);
        });

        section.appendChild(head);
        section.appendChild(grid);

        // Sits after the hero so the page still leads with its own heading.
        var hero = host.querySelector('.hero');
        if (hero && hero.nextSibling) {
            host.insertBefore(section, hero.nextSibling);
        } else {
            host.insertBefore(section, host.firstChild);
        }
    }

    function init() {
        record();
        render();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
