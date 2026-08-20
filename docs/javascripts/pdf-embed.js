/**
 * Click-to-load PDF embeds.
 *
 * Slide decks run 2-30 MB. Embedding them in an eager <iframe> meant every
 * visit paid for the whole deck before the page settled, which on phone data
 * often meant the page never settled at all. Each embed now renders as a card
 * and only fetches the PDF once the reader asks for it.
 *
 * Markup contract (see scripts/lazyload_pdf_embeds.py):
 *   <div class="pdf-embed" data-pdf-src="..." data-pdf-title="..."></div>
 */
(function () {
    'use strict';

    var STYLE_ID = 'pdf-embed-styles';
    var CSS = [
        '.pdf-embed{flex:1;width:100%;min-height:80vh;display:flex;align-items:center;justify-content:center;padding:32px}',
        '.pdf-embed__card{width:min(520px,100%);display:flex;flex-direction:column;align-items:center;gap:18px;text-align:center;',
        'border:1px solid var(--border-hard,rgba(184,41,234,0.24));background:var(--bg-surface,rgba(10,5,20,0.6));padding:38px 30px}',
        '.pdf-embed__icon{font-family:"JetBrains Mono",monospace;font-size:0.62rem;font-weight:800;letter-spacing:0.2em;',
        'color:#ff2a4b;border:1px solid #ff2a4b;padding:6px 12px}',
        '.pdf-embed__title{font-family:"JetBrains Mono",monospace;font-size:0.92rem;font-weight:700;line-height:1.5;color:var(--text-main,#f8f7fb);margin:0}',
        '.pdf-embed__meta{font-family:"JetBrains Mono",monospace;font-size:0.68rem;letter-spacing:0.08em;color:var(--text-dim,#8f8b9a);margin:0}',
        '.pdf-embed__actions{display:flex;flex-wrap:wrap;gap:10px;justify-content:center}',
        '.pdf-embed__btn{appearance:none;display:inline-flex;align-items:center;height:38px;padding:0 20px;cursor:pointer;',
        'font-family:"JetBrains Mono",monospace;font-size:0.68rem;font-weight:800;letter-spacing:0.14em;text-transform:uppercase;',
        'text-decoration:none;border:1px solid #ff2a4b;background:transparent;color:#ff2a4b;transition:background 160ms ease,color 160ms ease}',
        '.pdf-embed__btn:hover{background:#ff2a4b;color:#050508}',
        '.pdf-embed__btn--ghost{border-color:var(--border-hard,rgba(184,41,234,0.34));color:var(--text-dim,#8f8b9a)}',
        '.pdf-embed__btn--ghost:hover{background:rgba(184,41,234,0.1);color:#ff2a4b}',
        '.pdf-embed__btn:focus-visible{outline:2px solid #b829ea;outline-offset:3px}',
        '.pdf-embed.is-loaded{padding:0;display:block}',
        '.pdf-embed iframe{flex:1;width:100%;border:none;min-height:80vh;display:block}',
        'body.shoug-light-mode .pdf-embed__card{background:#ffffff;border-color:rgba(22,17,31,0.15)}',
        'body.shoug-light-mode .pdf-embed__title{color:#16111f}',
        'body.shoug-light-mode .pdf-embed__meta{color:#534a61}'
    ].join('');

    function injectStyles() {
        if (document.getElementById(STYLE_ID)) return;
        var el = document.createElement('style');
        el.id = STYLE_ID;
        el.textContent = CSS;
        document.head.appendChild(el);
    }

    function humanSize(bytes) {
        if (!bytes || bytes < 1024) return '';
        var mb = bytes / (1024 * 1024);
        return mb >= 1 ? mb.toFixed(1) + ' MB' : Math.round(bytes / 1024) + ' KB';
    }

    /* A HEAD request tells the reader what the deck will cost before they
       commit to it. It is best-effort: same-origin only, and any failure just
       leaves the size line reading "PDF document". */
    function fillSize(host, src, meta) {
        try {
            var url = new URL(src, window.location.href);
            if (url.origin !== window.location.origin) return;
        } catch (e) { return; }
        fetch(src, { method: 'HEAD' }).then(function (res) {
            var size = humanSize(parseInt(res.headers.get('content-length'), 10));
            if (size) meta.textContent = 'PDF document · ' + size;
        }).catch(function () { /* keep the default label */ });
    }

    function load(host, src, title) {
        var frame = document.createElement('iframe');
        frame.src = src;
        frame.title = title || 'PDF document';
        frame.setAttribute('width', '100%');
        frame.setAttribute('height', '100%');
        host.innerHTML = '';
        host.classList.add('is-loaded');
        host.appendChild(frame);
        frame.focus();
    }

    function build(host) {
        var src = host.getAttribute('data-pdf-src');
        if (!src) return;
        var title = host.getAttribute('data-pdf-title') || 'PDF document';

        var card = document.createElement('div');
        card.className = 'pdf-embed__card';

        var icon = document.createElement('span');
        icon.className = 'pdf-embed__icon';
        icon.textContent = 'PDF';

        var heading = document.createElement('p');
        heading.className = 'pdf-embed__title';
        heading.textContent = title;

        var meta = document.createElement('p');
        meta.className = 'pdf-embed__meta';
        meta.textContent = 'PDF document';

        var actions = document.createElement('div');
        actions.className = 'pdf-embed__actions';

        var open = document.createElement('button');
        open.type = 'button';
        open.className = 'pdf-embed__btn';
        open.textContent = 'Open document';
        open.addEventListener('click', function () { load(host, src, title); });

        var tab = document.createElement('a');
        tab.className = 'pdf-embed__btn pdf-embed__btn--ghost';
        tab.href = src;
        tab.target = '_blank';
        tab.rel = 'noopener';
        tab.textContent = 'New tab';

        var dl = document.createElement('a');
        dl.className = 'pdf-embed__btn pdf-embed__btn--ghost';
        dl.href = src;
        dl.setAttribute('download', '');
        dl.textContent = 'Download';

        actions.appendChild(open);
        actions.appendChild(tab);
        actions.appendChild(dl);
        card.appendChild(icon);
        card.appendChild(heading);
        card.appendChild(meta);
        card.appendChild(actions);
        host.innerHTML = '';
        host.appendChild(card);

        fillSize(host, src, meta);
    }

    function init() {
        var hosts = document.querySelectorAll('.pdf-embed:not([data-pdf-ready])');
        if (!hosts.length) return;
        injectStyles();
        Array.prototype.forEach.call(hosts, function (host) {
            host.setAttribute('data-pdf-ready', '');
            build(host);
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
