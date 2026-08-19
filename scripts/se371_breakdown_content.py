#!/usr/bin/env python3
"""Content for the SE371 slide breakdowns.

One dict per chapter, matching the PDFs in se371/slides/. Each chapter carries:
  stats    - the chips under the title
  sections - id / nav / label / title / html
  quiz     - self-check questions

Code samples are reconstructed to be runnable and are cross-linked, where one
exists, to the matching live example under extra-resources/resource-viewers/.
"""

R = '/academics/software-engineering/se371/extra-resources/'
V = R + 'resource-viewers/'


def code(file, body, note='', run=''):
    """One code block.

    `run` is either a resource-viewer slug or, for examples that have no
    generated viewer, a path relative to extra-resources/.
    """
    head = '<span class="code-file">%s</span>' % file
    if note:
        head += '<span class="code-note">%s</span>' % note
    if run:
        url = (R + run + '/') if '/' in run else (V + run + '/')
        head += '<a class="code-run" href="%s" target="_blank" rel="noopener">[ RUN IT &rarr; ]</a>' % url
    return ('<div class="code-block"><div class="code-head">%s</div>'
            '<pre>%s</pre></div>' % (head, body.strip('\n')))


def trap(title, wrong, fix):
    return ('<div class="trap"><div class="trap-title">%s</div><p>%s</p>'
            '<p><span class="fix">Fix:</span> %s</p></div>' % (title, wrong, fix))


def hook(text):
    return '<div class="hook">%s</div>' % text


def table(headers, rows):
    th = ''.join('<th>%s</th>' % h for h in headers)
    tr = ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % c for c in r) for r in rows)
    return ('<div class="table-wrap"><table><thead><tr>%s</tr></thead>'
            '<tbody>%s</tbody></table></div>' % (th, tr))


def slidemap(rows):
    """rows: (slides, topic, weight, note) - weight in MEMORIZE/WRITE/SKIM."""
    cls = {'MEMORIZE': 'w-memorize', 'WRITE': 'w-write', 'SKIM': 'w-skim'}
    lbl = {'MEMORIZE': 'Memorize', 'WRITE': 'Write it', 'SKIM': 'Skim'}
    rows2 = [('<strong>%s</strong>' % s, '<strong>%s</strong>' % t,
              '<span class="%s">%s</span>' % (cls[w], lbl[w]), n)
             for s, t, w, n in rows]
    return table(['Slides', 'Topic', 'Weight', 'What to do with it'], rows2)


def drills(items):
    return '<ol class="drill">%s</ol>' % ''.join('<li>%s</li>' % i for i in items)


def cheat(cols):
    out = ''.join('<div class="cheat-col"><h4>%s</h4><ul>%s</ul></div>'
                  % (t, ''.join('<li>%s</li>' % i for i in items))
                  for t, items in cols)
    return '<div class="cheat">%s</div>' % out


CHAPTERS = []


# ═══════════════════════════════════════════════════════════════════════════ #
# CHAPTER 01 — Introduction to the Web
# ═══════════════════════════════════════════════════════════════════════════ #

CHAPTERS.append({
    'num': 1,
    'slug': '01-introduction-to-the-web',
    'file': 'introduction-to-the-web.html',
    'title': 'Introduction to the Web',
    'desc': ('Slide-by-slide breakdown of SE371 Chapter 1 — internet history, the client-server '
             'model, the four-layer TCP/IP stack, DNS resolution, URL anatomy and HTTP.'),
    'sub': ('This is the only chapter in SE371 with almost no code in it, and that is exactly why '
            'people lose marks on it. It is pure recall: layers, codes, acronyms, and the order of '
            'a DNS lookup. Treat it like a vocabulary exam, not a programming one.'),
    'stats': ['59 slides', 'Two decks in one', 'Mostly recall', 'Book ch. 1 + 2'],
    'sections': [
        {
            'id': 'orient', 'nav': 'Start Here', 'label': 'Orientation',
            'title': 'What this chapter is really for',
            'html': """
<p>The PDF is <strong>two decks stapled together</strong>. Slide 1&ndash;21 is <em>Chapter 1-a: Introduction
to Web Development</em> and slide 22&ndash;58 is <em>Chapter 1-b: How the Web Works</em>. They are graded
very differently, so study them differently.</p>

<div class="grid-2">
  <div class="card">
    <h4>Part A (slides 1&ndash;21) &mdash; context</h4>
    <p>History, circuit vs packet switching, web vs desktop apps, static vs dynamic, Web 2.0,
    client-server, internet infrastructure. Almost entirely narrative. Skim it once, memorize five
    dates and one comparison table, move on.</p>
  </div>
  <div class="card">
    <h4>Part B (slides 22&ndash;58) &mdash; the machinery</h4>
    <p>The four-layer model, IP, TCP vs UDP, DNS, URL anatomy, HTTP methods, headers, status codes.
    <strong>This is where the marks are</strong>, and it is also the foundation you will silently rely
    on in every later chapter &mdash; GET vs POST in ch. 2 forms, ports in ch. 6 Node, status codes
    in ch. 7 REST APIs.</p>
  </div>
</div>

<p>The single most useful thing you can take out of this chapter is a mental picture of what happens
between typing a URL and seeing a page. Everything else in the chapter hangs off that one story.</p>

<div class="hook"><strong>The whole chapter in one sentence:</strong> you type a URL &rarr; DNS turns
the name into an IP &rarr; TCP opens a connection on a port &rarr; HTTP sends a request with headers
&rarr; the server replies with a status code and a body &rarr; the browser parses the HTML and fetches
every referenced asset.</div>
"""
        },
        {
            'id': 'map', 'nav': 'Slide Map', 'label': 'Navigation',
            'title': 'All 59 slides, weighted',
            'html': slidemap([
                ('1&ndash;4', 'Title, syllabus, prerequisites', 'SKIM',
                 'Slide 3 lists the technical prerequisites: zip/unzip, <code>cd</code> navigation, conditionals, loops, try/catch, objects. If any of those are shaky, fix them now &mdash; ch. 4 assumes all of them.'),
                ('5&ndash;8', 'Internet vs WWW, circuit vs packet switching, birth of the web', 'MEMORIZE',
                 'Know that the Internet is the network and the WWW is one service on it. Memorize the five things Berners-Lee defined (slide 8): URL, HTTP, web server software, HTML, browser.'),
                ('9&ndash;11', 'Web apps vs desktop apps; KSA personal data protection law', 'MEMORIZE',
                 'Classic "list three advantages / three disadvantages" question. Build the two-column table once and reread it.'),
                ('12&ndash;14', 'Static &rarr; dynamic &rarr; Web 2.0', 'MEMORIZE',
                 'The key line on slide 14: Web 2.0 moved programming logic from the server into the browser, which is why you have to learn JavaScript.'),
                ('15&ndash;17', 'Why programs are needed; the client-server model', 'MEMORIZE',
                 'The examinable sentence is on slide 17: the essential characteristic of a server is that it <em>listens</em> for requests and responds.'),
                ('18&ndash;21', 'Physical internet, undersea cables, Tier 1 backbone', 'SKIM',
                 'Read once. Only "Tier 1 networks = the backbone" is likely to be asked.'),
                ('22&ndash;24', 'Part B title, objectives, what a protocol is', 'SKIM',
                 'A protocol is a set of rules partners use when they communicate. One line, learn it verbatim.'),
                ('25', 'The four-layer TCP/IP model', 'MEMORIZE',
                 'Highest-value single slide in Part A/B. Know all four layers, in order, and one job each.'),
                ('26&ndash;29', 'Link layer, internet layer, IPv4/IPv6, PAT', 'MEMORIZE',
                 'IPv4 = four 8-bit integers, dotted. IPv6 = eight 16-bit integers, hex. IPv4 exhausted in 2011; PAT is the workaround.'),
                ('30&ndash;32', 'Transport layer: TCP guarantees, UDP trade-off', 'MEMORIZE',
                 'TCP = sequence numbers + ACK + retransmit = ordered and guaranteed. UDP = no guarantee, used for streaming, VoIP, games and DNS.'),
                ('33', 'Application layer protocols', 'MEMORIZE',
                 'HTTP, SSH, FTP, POP/IMAP/SMTP, DNS. Know one sentence each.'),
                ('34&ndash;39', 'DNS, name levels, gTLD vs ccTLD', 'MEMORIZE',
                 'The three gTLD subtypes (unrestricted / sponsored / new) are a favourite. So is the fact that <code>.arpa</code> is the third TLD category, used for reverse lookups.'),
                ('40&ndash;42', 'Registrars, ICANN, KSA registration', 'MEMORIZE',
                 'ICANN oversees TLDs and accredits registrars. In KSA, <code>.sa</code> started 1995 and the Arabic TLD in 2010; government domains go through the DGA.'),
                ('43&ndash;44', 'Address resolution, all ten steps', 'MEMORIZE',
                 'Cache &rarr; primary DNS &rarr; root &rarr; TLD server &rarr; authoritative server &rarr; IP. Draw the arrows from memory; that is the exam answer.'),
                ('45&ndash;48', 'URL anatomy: protocol, domain, port, path, query string', 'WRITE',
                 'You must be able to label a URL part-by-part and say which parts are optional. Port 80 is the HTTP default; query strings are <code>?key=value&amp;key=value</code>.'),
                ('49&ndash;51', 'HTTP, headers, request methods', 'MEMORIZE',
                 'Request headers describe the client (Host, User-Agent, Cache-Control). Response headers describe the server and payload (Server, Last-Modified, Content-Type, Encoding).'),
                ('52&ndash;53', 'GET vs POST', 'MEMORIZE',
                 'This reappears in ch. 2 (forms), ch. 5 (submit handling) and ch. 7 (CRUD). Learn it properly once here.'),
                ('54&ndash;55', 'Response codes and the code table', 'MEMORIZE',
                 'Know the four families by first digit, plus 200, 301, 304, 401, 404, 414, 500 individually.'),
                ('56&ndash;58', 'How browsers render; web servers and stacks', 'MEMORIZE',
                 'A web server is "nothing more than a process that responds to HTTP requests". The five stack layers on slide 57 preview the whole course.'),
            ])
        },
        {
            'id': 'context', 'nav': 'Part A', 'label': 'Slides 1&ndash;21',
            'title': 'Context: how the web got here, and why it matters to you',
            'html': """
<h3>Internet &ne; WWW</h3>
<p>The <strong>Internet</strong> is the global network of connected machines and the protocols that
run on it. The <strong>World Wide Web</strong> is one service delivered over that network, the one
that speaks HTTP and exchanges HTML. Email, SSH and file transfer are also on the Internet and are
not the Web. The slides open with this distinction because the rest of Part B is about the Internet,
not the Web.</p>

<h3>Circuit switching vs packet switching</h3>
""" + table(['', 'Circuit switched', 'Packet switched'], [
                ('<strong>Model</strong>', 'A continuous physical circuit is held open for the whole conversation, as with an operator plugging a wire into a switchboard.', 'The message is split into packets that are routed independently and reassembled at the far end.'),
                ('<strong>Bandwidth</strong>', 'Inefficient &mdash; the line is reserved even when nobody is speaking.', 'Efficient &mdash; the line carries other traffic between your packets.'),
                ('<strong>Scaling</strong>', 'Difficult to scale.', 'Scales to the modern Internet.'),
                ('<strong>Era</strong>', 'Early telephony.', '1960s ARPANET &rarr; 1974 X.25 &rarr; 1979 USENET &rarr; 1981 TCP/IP &rarr; adopted across ARPANET on 1 Jan 1983.'),
            ]) + """
<h3>The five things Berners-Lee defined (1992)</h3>
<p>Slide 8 is a list that maps almost perfectly onto the rest of this course, which makes it easy to
remember and easy to examine:</p>
<ol>
  <li><strong>URL</strong> &mdash; uniquely identifies a resource (chapter 1)</li>
  <li><strong>HTTP</strong> &mdash; describes how requests and responses operate (chapter 1)</li>
  <li><strong>Web server software</strong> &mdash; responds to HTTP requests (chapter 6)</li>
  <li><strong>HTML</strong> &mdash; publishes documents (chapter 2)</li>
  <li><strong>A browser</strong> &mdash; makes requests and displays what it receives (chapters 3&ndash;5)</li>
</ol>
""" + hook("<strong>Memory hook for the five:</strong> <em>&ldquo;You Have Some Web Bits&rdquo;</em> &mdash; "
           "<strong>U</strong>RL, <strong>H</strong>TTP, <strong>S</strong>erver, "
           "<strong>W</strong>eb page (HTML), <strong>B</strong>rowser.") + """

<h3>Web apps vs desktop apps</h3>
""" + table(['Advantages', 'Disadvantages'], [
                ('Accessible from any Internet-enabled computer', 'Requires an active Internet connection'),
                ('Work across operating systems and browsers', 'Sensitive data travels over the Internet'),
                ('Updates roll out by changing the server only', 'Storage, licensing and use of uploaded data raise concerns'),
                ('Centralised storage means fewer local-storage security concerns', 'Appearance differs across browsers'),
                ('&mdash;', 'Restrictions on installing software or accessing hardware (Flash on iOS)'),
                ('&mdash;', 'Plugins can interfere with JavaScript, cookies and advertisements'),
            ]) + """
<h3>Static &rarr; dynamic &rarr; Web 2.0</h3>
<div class="grid-2">
  <div class="card"><h4>Static site</h4><p>The server sends a file that was already written. Every
  visitor gets identical bytes.</p></div>
  <div class="card"><h4>Dynamic server-side site</h4><p>A program on the server generates the page
  per request, usually from a database. This is what you build in chapters 6 and 7.</p></div>
  <div class="card"><h4>Web 2.0</h4><p>Users both contribute and consume content. For a developer,
  the important half is that <strong>logic moved from the server into the browser</strong> &mdash;
  which is the reason chapters 4 and 5 exist.</p></div>
  <div class="card"><h4>Client-server</h4><p>Clients vary wildly in OS, speed, screen size, memory and
  storage. Servers are built for traffic and bandwidth. The defining property of a server is that it
  <strong>listens</strong> for requests and responds.</p></div>
</div>
"""
        },
        {
            'id': 'stack', 'nav': 'Layers &amp; DNS', 'label': 'Slides 22&ndash;44',
            'title': 'The machinery: layers, addresses, and name resolution',
            'html': """
<h3>The four-layer model</h3>
<p>TCP/IP was originally abstracted as four layers. Later models subdivide it into five or seven, but
this course uses the four-layer version, and questions are phrased in its terms.</p>
""" + table(['Layer', 'Job', 'Key terms'], [
                ('<strong>4. Application</strong>', 'Process-to-process communication &mdash; the protocols developers actually touch.', 'HTTP, SSH, FTP, POP/IMAP/SMTP, DNS'),
                ('<strong>3. Transport</strong>', 'Ensures transmissions arrive in order and without error.', 'TCP (sequence numbers, ACK, retransmit), UDP (no guarantee)'),
                ('<strong>2. Internet</strong>', 'Routes packets between partners across networks. Best-effort only &mdash; no reply expected, no guarantee of arrival.', 'IP, IPv4, IPv6, PAT'),
                ('<strong>1. Link</strong>', 'Physical transmission across the medium and logical links: packet creation, transmission, reception, error detection, collisions, line sharing.', 'MAC address'),
            ]) + hook(
                "<strong>Mnemonic (bottom &rarr; top):</strong> <em>Link, Internet, Transport, Application</em> "
                "&rarr; <strong>&ldquo;Little Imps Take Aim&rdquo;</strong>. Or remember the job words in order: "
                "<em>wire &rarr; route &rarr; reliable &rarr; readable</em>.") + """

<h3>IP addresses</h3>
<div class="grid-2">
  <div class="card"><h4>IPv4</h4><p>Four 8-bit integers separated by dots, e.g. <code>129.89.23.1</code>.
  The address space was effectively depleted in <strong>2011</strong>.</p></div>
  <div class="card"><h4>IPv6</h4><p>Eight 16-bit integers, each written in hexadecimal for readability.
  Over a billion billion times as many addresses as IPv4.</p></div>
</div>
<p><strong>PAT (Port Address Translation)</strong> lets multiple unrelated networks share one public
IP address, which is how the coffee shop, your home and the university all keep working despite IPv4
exhaustion. It is a stopgap; IPv6 is the long-term answer.</p>

<h3>TCP vs UDP &mdash; the trade-off</h3>
""" + table(['', 'TCP', 'UDP'], [
                ('<strong>Guarantee</strong>', 'Messages arrive, and arrive in order.', 'No guarantee at all.'),
                ('<strong>How</strong>', 'Each packet has a sequence number; each arrival is acknowledged (ACK); missing packets are retransmitted.', 'Fire and forget.'),
                ('<strong>Cost</strong>', 'Overhead of tracking and retransmitting.', 'Fast and cheap.'),
                ('<strong>Used for</strong>', 'The web (HTTP), file transfer, email.', 'Live streaming, VoIP, online games, <strong>DNS</strong>.'),
            ]) + """
<p>The slide&rsquo;s example is worth keeping: a broadcaster streaming a match to millions cannot afford
to track and retransmit every lost packet, and a small amount of loss is acceptable because viewers
still see the game.</p>

<h3>DNS: why it exists</h3>
<p>Humans do not remember numeric addresses. In the ARPANET era a single downloadable <code>hosts</code>
file mapped names to IPs; that stopped scaling, so it was replaced by the distributed Domain Name
System. A second, less obvious benefit: because the name is separate from the address,
<strong>a site can move to a different host without changing its name</strong>.</p>

<h3>Name levels and TLD categories</h3>
""" + table(['Category', 'Meaning', 'Examples'], [
                ('<strong>gTLD</strong> &mdash; unrestricted', 'Anyone may register.', '<code>.com</code> <code>.net</code> <code>.org</code> <code>.info</code>'),
                ('<strong>gTLD</strong> &mdash; sponsored', 'Restricted to a sponsoring community.', '<code>.gov</code> <code>.mil</code> <code>.edu</code>'),
                ('<strong>gTLD</strong> &mdash; new', 'Opened by ICANN from June 2012; over 1000 created.', '<code>.art</code> <code>.cash</code> <code>.cool</code> <code>.jobs</code> <code>.tax</code>'),
                ('<strong>ccTLD</strong>', 'Controlled by the country it represents, so each is administered differently. UK businesses register under <code>co.uk</code>; <code>.ca</code> is open to anyone living or doing business in Canada.', '<code>.sa</code> <code>.uk</code> <code>.ca</code>'),
                ('<strong>.arpa</strong>', 'Reserved for reverse DNS lookups.', '&mdash;'),
            ]) + """
<p><strong>IDN</strong> (Internationalized Domain Names) allow non-ASCII characters and have been
deployed since 2009 &mdash; over 9 million exist. Registration in KSA: <code>.sa</code> from 1995, the
Arabic-script TLD from 2010; since February 2021 accredited registrars serve individuals and
non-government entities, while government entities register through the Digital Government Authority.
<strong>ICANN</strong> oversees top-level domains, accredits registrars and coordinates DNS.</p>

<h3>Address resolution &mdash; the ten steps</h3>
<p>Draw this from memory. It is the most likely long-answer question in the chapter.</p>
<ol>
  <li>Client requests a domain.</li>
  <li>The client computer checks its <strong>local DNS cache</strong>.</li>
  <li>If it is not cached, the computer asks its <strong>primary DNS server</strong>.</li>
  <li>If that server has no cached record, it asks a <strong>root name server</strong>.</li>
  <li>The root server returns the address of the relevant <strong>TLD server</strong>.</li>
  <li>The DNS server requests the record from that TLD server.</li>
  <li>The TLD server returns the addresses of the domain&rsquo;s <strong>authoritative DNS servers</strong>.</li>
  <li>The DNS server asks one of those authoritative servers for the IP.</li>
  <li>The authoritative server returns the IP address.</li>
  <li>The client finally makes its actual request to that IP.</li>
</ol>
""" + hook("<strong>Shortcut for the chain:</strong> <em>Cache &rarr; Primary &rarr; Root &rarr; TLD "
           "&rarr; Authoritative &rarr; done.</em> Five hops, then the real request. If you can say "
           "those five words in order you can reconstruct all ten steps.") + """

<h3>Domain registration, in order</h3>
<ol>
  <li>Registrant searches for a domain via a registrar or reseller portal.</li>
  <li>The registrar queries the TLD registry operator for availability.</li>
  <li>If available, the registrant pays and supplies WHOIS information.</li>
  <li>The registrar pushes the WHOIS data to the TLD registry operator.</li>
  <li>The registry operator adds it to its authoritative list.</li>
  <li>The registry operator pushes DNS information out to the TLD name servers.</li>
</ol>
"""
        },
        {
            'id': 'http', 'nav': 'URL &amp; HTTP', 'label': 'Slides 45&ndash;58',
            'title': 'URL anatomy and HTTP — the part you keep using all semester',
            'html': """
<h3>Label every part of a URL</h3>
""" + code('URL anatomy', """
<span class="k">https</span>://<span class="t">www.funwebdev.com</span>:<span class="k">8080</span>/<span class="t">pages/search</span>?<span class="s">term=css&amp;page=2</span>#<span class="c">results</span>
<span class="c">└─┬─┘   └────────┬───────┘ └─┬─┘ └─────┬────┘ └───────┬───────┘ └───┬──┘</span>
<span class="c">  │              │            │        │             │             │</span>
<span class="c">  │              │            │        │             │             └─ fragment (browser only, never sent to the server)</span>
<span class="c">  │              │            │        │             └─ query string: key=value pairs, ? starts it, &amp; joins them</span>
<span class="c">  │              │            │        └─ path: maps to a location under the server root</span>
<span class="c">  │              │            └─ port: OPTIONAL. Defaults to 80 for http, 443 for https</span>
<span class="c">  │              └─ domain (or IP address) to connect to        ← REQUIRED</span>
<span class="c">  └─ protocol used to connect                                   ← REQUIRED</span>
""", note='Only protocol + domain are required') + """
<p>Two details the slides call out explicitly. <strong>Port:</strong> not commonly used on production
sites, but useful to route requests to a test server, to stress test, or to get around filters;
<code>http://funwebdev.com:8080/</code> connects on port 8080. <strong>Path:</strong> the server root
corresponds to a real folder on the server &mdash; often <code>/var/www/html/</code> on Linux or
<code>/inetpub/wwwroot/</code> on Windows &mdash; and when you request a folder rather than a file, the
server decides which file to send you.</p>

<h3>The request/response cycle</h3>
""" + code('What actually crosses the wire', """
<span class="c">── REQUEST ─────────────────────────────────────────────</span>
<span class="k">GET</span> /pages/search?term=css HTTP/1.1
<span class="t">Host</span>: www.funwebdev.com          <span class="c">← which site, on a shared IP</span>
<span class="t">User-Agent</span>: Mozilla/5.0 ...       <span class="c">← data about the client machine</span>
<span class="t">Cache-Control</span>: max-age=0

<span class="c">── RESPONSE ────────────────────────────────────────────</span>
HTTP/1.1 <span class="k">200 OK</span>                    <span class="c">← status code</span>
<span class="t">Server</span>: nginx/1.24.0             <span class="c">← data about the server</span>
<span class="t">Content-Type</span>: text/html; charset=utf-8
<span class="t">Last-Modified</span>: Tue, 18 Feb 2026 09:14:02 GMT
<span class="t">Content-Encoding</span>: gzip

&lt;!DOCTYPE html&gt;                    <span class="c">← optional message body</span>
&lt;html&gt; ... &lt;/html&gt;
""", note='HTTP defaults to TCP port 80') + """
<p>HTTP establishes a TCP connection on port 80 by default, the server waits for the request, then
responds with <strong>headers, a response code, and an optional message</strong> which may include
files. Headers are described by the slides as one of the most powerful aspects of HTTP: request
headers carry data about the client machine, response headers carry data about the server and the
data being sent.</p>

<h3>GET vs POST</h3>
""" + table(['', 'GET', 'POST'], [
                ('<strong>Purpose</strong>', 'Ask for the resource at a URL.', 'Transmit data to the server, normally from an HTML form.'),
                ('<strong>When it happens</strong>', 'Clicking a link, typing a URL, using a bookmark.', 'Submitting a form declared with <code>method="post"</code>.'),
                ('<strong>Where data goes</strong>', 'In the query string, visible in the URL.', 'In the request body, not shown in the URL.'),
                ('<strong>Consequences</strong>', 'Bookmarkable, cacheable, appears in history and server logs; length-limited (see 414).', 'Not bookmarkable, not length-limited in the same way, re-submits on refresh.'),
            ]) + """
<p>The other methods the slides name but do not cover are <code>HEAD</code>, <code>CONNECT</code>,
<code>TRACE</code> and <code>OPTIONS</code>. You meet <code>PUT</code> and <code>DELETE</code> properly
in chapter 7.</p>

<h3>Status codes</h3>
<p>The first digit gives the family: <strong>2xx</strong> success, <strong>3xx</strong> redirection,
<strong>4xx</strong> client error, <strong>5xx</strong> server error.</p>
""" + table(['Code', 'Name', 'What it actually means'], [
                ('<code>200</code>', 'OK', 'The request was successful.'),
                ('<code>301</code>', 'Moved Permanently', 'The requested resource has permanently moved.'),
                ('<code>304</code>', 'Not Modified', 'With appropriate Cache-Control headers, the server says its copy is no newer than the one in the client cache.'),
                ('<code>401</code>', 'Unauthorized', 'The resource is protected and requires credentials.'),
                ('<code>404</code>', 'Not Found', 'The requested resource was not found. The one code end users recognise.'),
                ('<code>414</code>', 'Request URI Too Long', 'Too much data is being submitted through the URL &mdash; i.e. a GET that should have been a POST.'),
                ('<code>500</code>', 'Internal Server Error', 'The server hit an error and tells the client almost nothing about it.'),
            ]) + hook(
                "<strong>Hook for 414:</strong> it is the code that <em>proves</em> the GET/POST rule. "
                "If you push form data through the URL and it is large, the server refuses with 414. "
                "That is the exam-ready justification for using POST.") + """

<h3>How a page actually loads</h3>
<p>The browser requests the initial HTML page, parses it to find every referenced resource &mdash;
images, style sheets, scripts &mdash; and requests those too. <strong>The page is only fully loaded
once all the files have been retrieved.</strong> The whole set of algorithms to download, parse, lay
out, fetch assets and produce the final interactive page is collectively called
<strong>rendering</strong>. Remember this: it is the reason chapter 4 tells you where to put your
<code>&lt;script&gt;</code> tag, and the reason chapter 5 uses <code>DOMContentLoaded</code>.</p>

<h3>The application stack</h3>
<p>Slide 57 defines a web server as "nothing more than a process that responds to HTTP requests", and
lists the five parts of an application stack. This is a preview of your whole semester:</p>
""" + table(['Stack layer', 'Where you meet it in SE371'], [
                ('Operating system', 'Assumed &mdash; not assessed'),
                ('Web server software', 'Chapter 6 &mdash; Node&rsquo;s <code>http</code> module and Express'),
                ('Database', 'Chapter 7 &mdash; MongoDB/Mongoose and MySQL/Sequelize'),
                ('Backend language and runtime', 'Chapter 6 &mdash; JavaScript on Node.js'),
                ('Front-end languages/frameworks/libraries', 'Chapters 2&ndash;5 &mdash; HTML, CSS, JavaScript, the DOM'),
            ])
        },
        {
            'id': 'practice', 'nav': 'Do This', 'label': 'Active Practice',
            'title': 'How to make an all-theory chapter stick',
            'html': """
<p>You cannot code your way through chapter 1, but you can <em>observe</em> everything in it in about
fifteen minutes. Reading the slides again is the worst use of your time; doing this instead is the
best.</p>

<div class="card">
  <h4>1. Watch a real request/response pair</h4>
  <p>Open any site &rarr; DevTools (<code>F12</code>) &rarr; <strong>Network</strong> tab &rarr; reload.
  Click the first document row. You are now looking at exactly what slides 49&ndash;55 describe: the
  request method, the request headers, the status code, and the response headers. Find
  <code>Host</code>, <code>User-Agent</code>, <code>Server</code>, <code>Content-Type</code> and
  <code>Last-Modified</code> with your own eyes once and you will not forget which side each belongs to.</p>
</div>

<div class="card">
  <h4>2. Count the requests</h4>
  <p>Still in the Network tab, look at the request count at the bottom. That number <em>is</em> slide
  56 &mdash; the browser fetched the HTML, parsed it, and then fetched every stylesheet, script and
  image it referenced. Sort by Type to see the categories.</p>
</div>

<div class="card">
  <h4>3. Trigger the status codes yourself</h4>
""" + code('Terminal — see the codes from slide 55', """
curl -I https://example.com                 <span class="c"># 200 OK, plus every response header</span>
curl -I https://example.com/no-such-page    <span class="c"># 404 Not Found</span>
curl -I http://github.com                   <span class="c"># 301 Moved Permanently → https</span>
curl -I https://httpbin.org/status/500      <span class="c"># 500 Internal Server Error</span>
curl -I https://httpbin.org/status/401      <span class="c"># 401 Unauthorized</span>
""", note='-I sends a HEAD request: headers only, no body') + """
</div>

<div class="card">
  <h4>4. Do a DNS lookup by hand</h4>
""" + code('Terminal — slides 43–44, live', """
nslookup psu.edu.sa          <span class="c"># name → IP, exactly what step 9 returns</span>
dig +trace psu.edu.sa        <span class="c"># the whole chain: root → TLD → authoritative</span>
ping psu.edu.sa              <span class="c"># shows the resolved IP before the first reply</span>
""", note='dig +trace prints the ten steps as they happen') + """
  <p>The <code>+trace</code> output is the ten-step diagram, printed live. Run it once and the diagram
  stops being something you memorised and becomes something you watched.</p>
</div>

<div class="card">
  <h4>5. Prove GET puts data in the URL</h4>
  <p>Search for something on any site and read the address bar. The <code>?</code>, the
  <code>key=value</code> pairs and the <code>&amp;</code> separators from slide 48 are right there.
  Change a value in the URL and press Enter &mdash; the page responds to your edit. That is why
  slide 65 of chapter 2 will tell you client-side validation is not security.</p>
</div>
"""
        },
        {
            'id': 'traps', 'nav': 'Traps', 'label': 'Marks Lost Here',
            'title': 'The five things people get wrong',
            'html': (
                trap('&ldquo;The Internet and the Web are the same thing&rdquo;',
                     'They are not, and slide 5 opens with the distinction specifically so it can be tested. '
                     'The Internet is the network of networks; the Web is one application-layer service running on it, alongside email, FTP and SSH.',
                     'The Web needs the Internet. The Internet does not need the Web.') +
                trap('Putting DNS under TCP',
                     'DNS is an <strong>application layer</strong> protocol, listed on slide 33 next to HTTP and FTP. '
                     'Separately, it is one of the services that runs over <strong>UDP</strong>, not TCP (slide 32). Both facts get mixed up.',
                     'DNS lives at the application layer and is carried by UDP. Two different questions, two different answers.') +
                trap('Confusing the two "best effort" claims',
                     'The <strong>Internet layer</strong> is the best-effort one &mdash; it sends a message, expects no reply, and guarantees nothing. '
                     'The <strong>transport layer</strong> is the one that adds guarantees, via TCP. People swap these.',
                     'Internet layer = route it and hope. Transport layer = make sure it got there.') +
                trap('Answering "404" for everything that goes wrong',
                     '404 means the resource was not found &mdash; a client-side mistake about <em>what</em> was asked for. '
                     'A crashed server is 500. A missing login is 401. A too-long query string is 414. A cached copy still being valid is 304.',
                     'Read the first digit first: 4xx is your fault, 5xx is the server&rsquo;s fault.') +
                trap('Saying POST is "secure"',
                     'POST only moves the data from the URL into the request body. Over plain HTTP it is still readable on the wire, '
                     'and anyone can open DevTools and read or change it before sending.',
                     'POST is about <em>where the data goes</em> and how much of it fits, not about security. HTTPS is what makes it private.')
            )
        },
        {
            'id': 'cheat', 'nav': 'Cheat Sheet', 'label': 'One Screen',
            'title': 'Chapter 1 on a single screen',
            'html': cheat([
                ('Four layers (top &rarr; bottom)', [
                    '<strong>Application</strong> &mdash; HTTP, SSH, FTP, SMTP/POP/IMAP, DNS',
                    '<strong>Transport</strong> &mdash; TCP (ordered, ACKed), UDP (no guarantee)',
                    '<strong>Internet</strong> &mdash; IP routing, best effort',
                    '<strong>Link</strong> &mdash; physical media, MAC addresses',
                ]),
                ('Status codes', [
                    '<code>2xx</code> success &middot; <code>3xx</code> redirect',
                    '<code>4xx</code> client error &middot; <code>5xx</code> server error',
                    '<code>200</code> OK &middot; <code>301</code> Moved Permanently',
                    '<code>304</code> Not Modified &middot; <code>401</code> Unauthorized',
                    '<code>404</code> Not Found &middot; <code>414</code> URI Too Long',
                    '<code>500</code> Internal Server Error',
                ]),
                ('URL parts', [
                    '<code>protocol</code> &mdash; required',
                    '<code>domain</code> or IP &mdash; required',
                    '<code>:port</code> &mdash; optional, HTTP defaults to 80',
                    '<code>/path</code> &mdash; optional, maps to a server folder',
                    '<code>?k=v&amp;k=v</code> &mdash; query string',
                ]),
                ('DNS chain', [
                    'local cache &rarr; primary DNS',
                    '&rarr; root name server',
                    '&rarr; TLD server',
                    '&rarr; authoritative server',
                    '&rarr; IP returned, real request sent',
                ]),
                ('TLD categories', [
                    'gTLD unrestricted: <code>.com .net .org .info</code>',
                    'gTLD sponsored: <code>.gov .mil .edu</code>',
                    'gTLD new: since June 2012, 1000+',
                    'ccTLD: per-country rules, e.g. <code>.sa</code>',
                    '<code>.arpa</code>: reverse DNS lookups',
                ]),
                ('Dates worth knowing', [
                    '<strong>1960s</strong> ARPANET &middot; <strong>1974</strong> X.25',
                    '<strong>1979</strong> USENET &middot; <strong>1981</strong> TCP/IP introduced',
                    '<strong>1 Jan 1983</strong> TCP/IP across ARPANET',
                    '<strong>1992</strong> Berners-Lee publishes the web',
                    '<strong>2011</strong> IPv4 space depleted',
                ]),
            ])
        },
        {
            'id': 'drills', 'nav': 'Drills', 'label': 'Recall Practice',
            'title': 'Close the slides and answer these out loud',
            'html': drills([
                'Name the four layers bottom to top, and give one job for each.',
                'A packet arrives out of order. Which layer fixes it, and by what mechanism?',
                'Give three services that use UDP and say why guaranteed delivery is not worth its cost for them.',
                'Write out a URL that uses all six parts, then label each one and say which two are required.',
                'List the ten steps of address resolution without looking. Check yourself with <code>dig +trace</code>.',
                'Name the three subtypes of gTLD and give two examples of each.',
                'Give four HTTP status codes from four different families and say what each one tells the client.',
                'Explain why submitting a long form with GET can produce a 414, and what to do instead.',
                'List four request headers and four response headers, and say which side sends each.',
                'Describe what the browser does between receiving the HTML and finishing the page load.',
                'Name the five layers of an application stack and say which SE371 chapter covers each.',
                'State the difference between the Internet and the WWW in one sentence.',
            ])
        },
    ],
    'quiz': [
        {'tag': 'Layers', 'q': 'Which layer is described as providing only "best effort" communication — it sends a message but expects no reply and guarantees nothing?',
         'opts': ['The link layer', 'The internet layer', 'The transport layer', 'The application layer'],
         'a': 1,
         'why': 'The internet (IP) layer routes packets best-effort. The transport layer is the one that adds ordering and delivery guarantees through TCP.'},
        {'tag': 'Protocols', 'q': 'DNS appears twice in this chapter. Which pair of statements is correct?',
         'opts': ['It is a transport-layer protocol carried over TCP',
                  'It is an application-layer protocol carried over UDP',
                  'It is an internet-layer protocol carried over TCP',
                  'It is an application-layer protocol carried over TCP'],
         'a': 1,
         'why': 'Slide 33 lists DNS among the application-layer protocols; slide 32 gives DNS as an example of a service that uses UDP rather than TCP.'},
        {'tag': 'HTTP', 'q': 'A form submits a very large amount of data through the URL and the server rejects it. Which status code is it most likely returning?',
         'opts': ['400 Bad Request', '414 Request URI Too Long', '500 Internal Server Error', '304 Not Modified'],
         'a': 1,
         'why': '414 means too much data is being submitted through the URL — the textbook argument for using POST instead of GET for form data.'},
        {'tag': 'URL', 'q': 'Which two parts of a URL are required?',
         'opts': ['Protocol and path', 'Domain and port', 'Protocol and domain', 'Domain and path'],
         'a': 2,
         'why': 'A URL requires the protocol used to connect and the domain (or IP) to connect to. Port, path, query string and fragment are all optional.'},
        {'tag': 'DNS', 'q': 'Your DNS server has no cached record for a domain. Which server does it contact next?',
         'opts': ['The authoritative DNS server for the domain', 'The TLD name server', 'The root name server', 'The registrar'],
         'a': 2,
         'why': 'The order is cache → primary DNS → root name server → TLD server → authoritative server. The root server returns the address of the relevant TLD server.'},
        {'tag': 'Domains', 'q': 'Which of these is a sponsored gTLD?',
         'opts': ['<code>.info</code>', '<code>.edu</code>', '<code>.sa</code>', '<code>.cool</code>'],
         'a': 1,
         'why': '.edu is sponsored, along with .gov and .mil. .info is unrestricted, .cool is one of the new TLDs from 2012, and .sa is a country code TLD.'},
        {'tag': 'Concepts', 'q': 'What does the chapter give as the essential characteristic of a server?',
         'opts': ['It has more memory and processing power than a client',
                  'It stores a database',
                  'It listens for requests and responds to them',
                  'It has a permanent IP address'],
         'a': 2,
         'why': 'Powerful hardware is typical but not definitional. Slide 17 defines a server by behaviour: it listens for requests and, on getting one, responds with a message.'},
        {'tag': 'Web 2.0', 'q': 'For a software developer, what change does Web 2.0 represent?',
         'opts': ['Databases replaced flat files on the server',
                  'Programming logic migrated from the server into the browser',
                  'HTTP replaced FTP for page delivery',
                  'Static sites replaced dynamic sites'],
         'a': 1,
         'why': 'Slide 14 makes exactly this point — logic that previously existed only on the server moved into the browser, which is why JavaScript became essential.'},
    ],
})


# ═══════════════════════════════════════════════════════════════════════════ #
# CHAPTER 02 — HTML: Documents, Tables and Forms
# ═══════════════════════════════════════════════════════════════════════════ #

CHAPTERS.append({
    'num': 2,
    'slug': '02-html',
    'file': 'html.html',
    'title': 'HTML: Documents, Tables and Forms',
    'desc': ('Slide-by-slide breakdown of SE371 Chapter 2 — HTML syntax, semantic structure, links, '
             'lists, tables, forms, every input control, and where validation belongs.'),
    'sub': ('The first chapter you can actually be asked to write by hand. Everything here is muscle '
            'memory: document skeleton, table skeleton, form skeleton. If you can type those three '
            'from a blank file without thinking, most of this chapter is already done.'),
    'stats': ['73 slides', 'Two decks in one', 'Write-it heavy', 'Book ch. 3 + 4 + 5'],
    'sections': [
        {
            'id': 'orient', 'nav': 'Start Here', 'label': 'Orientation',
            'title': 'What this chapter is really for',
            'html': """
<p>Another merged deck. <strong>Part 1 (slides 1&ndash;33)</strong> is HTML documents and content
elements; <strong>Part 2 (slides 34&ndash;71)</strong> is tables, forms and validation. The title slide
even admits it covers three chapters of the textbook.</p>

<p>The whole chapter reduces to <strong>three skeletons</strong> you should be able to type from
memory, plus a vocabulary of elements you recognise on sight. Learn the skeletons first &mdash; every
lab, every later chapter and most exam questions start by writing one of them.</p>

<div class="grid-2">
  <div class="card">
    <h4>The one idea that ties it together</h4>
    <p><strong>Semantic markup.</strong> HTML describes <em>what content is</em>, never <em>how it
    looks</em>. Appearance is CSS&rsquo;s job (chapter 3). This is why you pick <code>&lt;h3&gt;</code>
    because it is a third-level heading, not because you want bold 16pt text, and why HTML5 gave you
    <code>&lt;header&gt;</code>, <code>&lt;nav&gt;</code>, <code>&lt;main&gt;</code> and friends to
    replace anonymous <code>&lt;div&gt;</code>s.</p>
  </div>
  <div class="card">
    <h4>Where it connects</h4>
    <p>Nesting on slide 14 is literally called <strong>the DOM</strong> &mdash; that is chapter 5.
    GET vs POST on slides 45&ndash;46 is chapter 1&rsquo;s HTTP methods. The <code>action</code>
    attribute points at a server-side resource, which you write in chapter 6. Validation on slides
    64&ndash;69 splits into HTML5, JavaScript (chapter 5) and server-side (chapters 6&ndash;7).</p>
  </div>
</div>
"""
        },
        {
            'id': 'map', 'nav': 'Slide Map', 'label': 'Navigation',
            'title': 'All 73 slides, weighted',
            'html': slidemap([
                ('1&ndash;3', 'Title, objectives, what HTML is', 'SKIM',
                 'One definition worth keeping: a markup language annotates a document so the annotations stay distinct from the text.'),
                ('4&ndash;5', 'Tags, attributes, empty elements', 'MEMORIZE',
                 'An attribute is a <code>name="value"</code> pair. An empty element has no text content &mdash; it instructs the browser. In HTML5 the trailing slash is optional.'),
                ('6', 'Semantic markup', 'MEMORIZE',
                 'The single most quotable slide in the chapter. Structure in HTML, presentation in CSS.'),
                ('7&ndash;13', 'Document skeleton: DOCTYPE, html, head, body, title/SEO', 'WRITE',
                 'Type the skeleton from memory until it is automatic. DOCTYPE says what type of document, <em>not</em> which HTML version.'),
                ('14&ndash;15', 'Nesting, parent/child/ancestor/descendant, correct nesting', 'MEMORIZE',
                 'The vocabulary here is reused all through chapter 5. The rule: a child&rsquo;s closing tag comes before its parent&rsquo;s.'),
                ('16&ndash;18', 'Quick tour of the ten element groups', 'SKIM',
                 'A checklist, not new material. Use it to test yourself on what each element is for.'),
                ('19&ndash;20', 'Headings, paragraphs, divisions, horizontal rule', 'WRITE',
                 'Six heading levels. Pick by meaning, not by appearance. <code>&lt;div&gt;</code> has no intrinsic semantic value &mdash; that is the point of it.'),
                ('21&ndash;22', 'Hyperlinks and the eight kinds of link', 'WRITE',
                 'A link has two parts: destination and label. Know <code>#fragment</code>, <code>mailto:</code>, <code>tel:</code> and <code>javascript:</code> forms.'),
                ('23', 'Class task &mdash; build a basic page', 'WRITE',
                 'Do it. This is the exact shape of the practical exam question.'),
                ('24&ndash;25', 'Absolute vs relative URLs, all six relative forms', 'MEMORIZE',
                 'Same directory / child / descendant / parent (<code>../</code>) / sibling / root (<code>/</code>). Guaranteed to appear.'),
                ('26', 'Inline text elements', 'MEMORIZE',
                 'Inline elements do not break the flow of text. Know <code>&lt;span&gt;</code> as the inline twin of <code>&lt;div&gt;</code>.'),
                ('27&ndash;28', 'Images and character entities', 'MEMORIZE',
                 '<code>src</code> and <code>alt</code> are the key attributes; <code>title</code>, <code>width</code>, <code>height</code> are optional. Learn six entities by name and number.'),
                ('29', 'Ordered, unordered and description lists', 'WRITE',
                 'Three list types, three tag families. <code>&lt;dl&gt;/&lt;dt&gt;/&lt;dd&gt;</code> is the one people forget.'),
                ('30&ndash;33', 'HTML5 semantic structure elements, figure/figcaption', 'WRITE',
                 'Nine semantic elements. The <code>&lt;figure&gt;</code> rule: content that could move elsewhere on the page and the document would still make sense.'),
                ('34&ndash;35', 'Part 2 title and objectives', 'SKIM', 'Transition slides.'),
                ('36&ndash;38', 'Tables: table/tr/td, thead/tbody/tfoot, basic structure', 'WRITE',
                 'All content must sit inside <code>&lt;td&gt;</code> or <code>&lt;th&gt;</code>. Type the full skeleton from memory.'),
                ('39&ndash;40', 'colspan and rowspan', 'WRITE',
                 'The classic exam question is "draw the table this markup produces" or the reverse. Practise both directions.'),
                ('41&ndash;43', 'Forms: why they exist, structure, action and method', 'MEMORIZE',
                 '<code>action</code> = URL of the server-side resource. <code>method</code> = how the data travels. HTML forms only support GET and POST.'),
                ('44&ndash;46', 'Query strings, GET vs POST', 'MEMORIZE',
                 'Four bullets each. Note the explicit warning: POST is <strong>not</strong> sufficient from a security standpoint.'),
                ('47', 'The eleven form control elements', 'MEMORIZE',
                 'Know one line for each of button, datalist, fieldset, form, input, label, legend, optgroup, option, output, select, textarea.'),
                ('48&ndash;54', 'Text inputs, select lists, radio buttons, checkboxes', 'WRITE',
                 'The attribute details are the marks: <code>multiple</code>, <code>selected</code>, <code>checked</code>, and what happens when <code>value</code> is omitted.'),
                ('55&ndash;58', 'Button controls and the revision checklist', 'WRITE',
                 'Slide 58 is the instructor telling you exactly what to revise. Treat it as the spec for this half of the chapter.'),
                ('59&ndash;62', 'number, range, color, date and time controls', 'MEMORIZE',
                 'Learn the six date/time types and their formats &mdash; <code>yyyy-mm-dd</code>, <code>HH:MM:SS</code>, <code>yyyy-mm</code>, <code>yyyy-W##</code>.'),
                ('63', 'Associating labels with inputs', 'WRITE',
                 'Small slide, real marks. Accessibility is in the chapter objectives.'),
                ('64&ndash;69', 'Validation: where, what types, how to notify, how to reduce errors', 'MEMORIZE',
                 'Three levels, six validation types, three notification questions. The line to quote: server-side validation is the only validation guaranteed to run.'),
                ('70&ndash;71', 'Color models and RGB', 'SKIM',
                 'Feeds straight into chapter 3. RGB are additive colours; they combine to white.'),
                ('73', 'Live Server tip', 'SKIM',
                 'Practical: if Live Server does not open, go to <code>http://127.0.0.1:PORT</code> manually.'),
            ])
        },
        {
            'id': 'skeleton', 'nav': 'Skeletons', 'label': 'Write From Memory',
            'title': 'The three skeletons',
            'html': """
<p>If you learn nothing else this chapter, learn these three by hand. Type them into a blank file
until you stop thinking about them.</p>

<h3>1. The document</h3>
""" + code('index.html', """
<span class="k">&lt;!DOCTYPE html&gt;</span>                        <span class="c">&lt;!-- what TYPE of document, not which HTML version --&gt;</span>
<span class="k">&lt;html</span> <span class="t">lang</span>=<span class="s">"en"</span><span class="k">&gt;</span>                     <span class="c">&lt;!-- root element; lang is optional but tells the browser the language --&gt;</span>
<span class="k">&lt;head&gt;</span>                                <span class="c">&lt;!-- DESCRIBES the document: nothing here is displayed --&gt;</span>
    <span class="k">&lt;meta</span> <span class="t">charset</span>=<span class="s">"UTF-8"</span><span class="k">&gt;</span>
    <span class="k">&lt;meta</span> <span class="t">name</span>=<span class="s">"viewport"</span> <span class="t">content</span>=<span class="s">"width=device-width, initial-scale=1.0"</span><span class="k">&gt;</span>
    <span class="k">&lt;title&gt;</span>Riyadh Sewing Supplies<span class="k">&lt;/title&gt;</span>   <span class="c">&lt;!-- matters for SEO --&gt;</span>
    <span class="k">&lt;meta</span> <span class="t">name</span>=<span class="s">"description"</span> <span class="t">content</span>=<span class="s">"Get everything you need to sew your next garment.
                 Open Saturday-Thursday, located in Al Olaya District, Riyadh."</span><span class="k">&gt;</span>
    <span class="k">&lt;link</span> <span class="t">rel</span>=<span class="s">"stylesheet"</span> <span class="t">href</span>=<span class="s">"css/styles.css"</span><span class="k">&gt;</span>
<span class="k">&lt;/head&gt;</span>
<span class="k">&lt;body&gt;</span>                                <span class="c">&lt;!-- CONTAINS what the browser displays --&gt;</span>
    <span class="k">&lt;h1&gt;</span>Hello<span class="k">&lt;/h1&gt;</span>
<span class="k">&lt;/body&gt;</span>
<span class="k">&lt;/html&gt;</span>
""", note='Slides 7–13', run='02-index-e7813d14') + """
<p>Slide 8 gives Google&rsquo;s own rule for a title: unique to the page, clear, concise, accurately
describing the contents. The slides contrast a bad and a good meta description &mdash;
<em>&ldquo;Sewing supplies, sewing machines, bobbins, needles&rdquo;</em> (a keyword dump) against a
sentence that tells a human what the page offers and where the shop is. Expect to be asked to
improve a bad one.</p>

<h3>2. The table</h3>
""" + code('tables.html', """
<span class="k">&lt;table&gt;</span>
  <span class="k">&lt;thead&gt;</span>                        <span class="c">&lt;!-- header rows --&gt;</span>
    <span class="k">&lt;tr&gt;</span>
      <span class="k">&lt;th&gt;</span>Month<span class="k">&lt;/th&gt;</span>              <span class="c">&lt;!-- th = header cell --&gt;</span>
      <span class="k">&lt;th&gt;</span>Savings<span class="k">&lt;/th&gt;</span>
    <span class="k">&lt;/tr&gt;</span>
  <span class="k">&lt;/thead&gt;</span>
  <span class="k">&lt;tbody&gt;</span>                        <span class="c">&lt;!-- the data --&gt;</span>
    <span class="k">&lt;tr&gt;</span>
      <span class="k">&lt;td&gt;</span>January<span class="k">&lt;/td&gt;</span>            <span class="c">&lt;!-- ALL content must be inside td or th --&gt;</span>
      <span class="k">&lt;td&gt;</span>100 SAR<span class="k">&lt;/td&gt;</span>
    <span class="k">&lt;/tr&gt;</span>
    <span class="k">&lt;tr&gt;</span>
      <span class="k">&lt;td&gt;</span>February<span class="k">&lt;/td&gt;</span>
      <span class="k">&lt;td&gt;</span>180 SAR<span class="k">&lt;/td&gt;</span>
    <span class="k">&lt;/tr&gt;</span>
  <span class="k">&lt;/tbody&gt;</span>
  <span class="k">&lt;tfoot&gt;</span>                        <span class="c">&lt;!-- summary rows --&gt;</span>
    <span class="k">&lt;tr&gt;</span>
      <span class="k">&lt;td&gt;</span>Total<span class="k">&lt;/td&gt;</span>
      <span class="k">&lt;td&gt;</span>280 SAR<span class="k">&lt;/td&gt;</span>
    <span class="k">&lt;/tr&gt;</span>
  <span class="k">&lt;/tfoot&gt;</span>
<span class="k">&lt;/table&gt;</span>
""", note='Slides 36–38', run='022-table-7bbf8bcc') + """

<h3>3. The form</h3>
""" + code('register.html', """
<span class="c">&lt;!-- action = URL of the server-side resource that PROCESSES the data
     method = how the data is TRANSMITTED. HTML forms allow only get or post. --&gt;</span>
<span class="k">&lt;form</span> <span class="t">action</span>=<span class="s">"action-page.html"</span> <span class="t">method</span>=<span class="s">"get"</span><span class="k">&gt;</span>

  <span class="c">&lt;!-- for="" must match the input's id="" — this is what makes the label clickable --&gt;</span>
  <span class="k">&lt;label</span> <span class="t">for</span>=<span class="s">"firstname"</span><span class="k">&gt;</span>First name:<span class="k">&lt;/label&gt;</span>
  <span class="k">&lt;input</span> <span class="t">type</span>=<span class="s">"text"</span> <span class="t">id</span>=<span class="s">"firstname"</span> <span class="t">name</span>=<span class="s">"fname"</span><span class="k">&gt;</span><span class="k">&lt;br&gt;&lt;br&gt;</span>

  <span class="k">&lt;label</span> <span class="t">for</span>=<span class="s">"lastname"</span><span class="k">&gt;</span>Last name:<span class="k">&lt;/label&gt;</span>
  <span class="k">&lt;input</span> <span class="t">type</span>=<span class="s">"text"</span> <span class="t">id</span>=<span class="s">"lastname"</span> <span class="t">name</span>=<span class="s">"lname"</span><span class="k">&gt;</span><span class="k">&lt;br&gt;&lt;br&gt;</span>

  <span class="k">&lt;input</span> <span class="t">type</span>=<span class="s">"submit"</span> <span class="t">value</span>=<span class="s">"Submit"</span><span class="k">&gt;</span>
<span class="k">&lt;/form&gt;</span>

<span class="c">&lt;!-- Submitting sends:  action-page.html?fname=Shoug&amp;lname=Alomran
     name=  becomes the KEY in the query string. No name attribute = not sent. --&gt;</span>
""", note='Slides 41–46', run='1-getmethod-8c61dffd') + hook(
                "<strong>The attribute that gets forgotten:</strong> <code>name</code>. "
                "<code>id</code> is for the label and for CSS/JavaScript. <code>name</code> is what "
                "becomes the key in the query string. An input without a <code>name</code> is simply "
                "never submitted &mdash; and this is the single most common reason a lab form "
                "&ldquo;does nothing&rdquo;.")
        },
        {
            'id': 'content', 'nav': 'Content', 'label': 'Slides 14&ndash;33',
            'title': 'Content elements: links, lists, images, semantics',
            'html': """
<h3>Nesting and the family vocabulary</h3>
<p>Slide 14 introduces terms you will use constantly in chapter 5, and names the concept outright:
this hierarchy <strong>is the Document Object Model</strong>.</p>
""" + code('nesting.html', """
<span class="k">&lt;body&gt;</span>                              <span class="c">← ancestor of everything below</span>
  <span class="k">&lt;article&gt;</span>                        <span class="c">← child of body, parent of h1 and p</span>
    <span class="k">&lt;h1&gt;</span>Title<span class="k">&lt;/h1&gt;</span>                 <span class="c">← child of article, descendant of body</span>
    <span class="k">&lt;p&gt;</span>Text with <span class="k">&lt;strong&gt;</span>emphasis<span class="k">&lt;/strong&gt;</span><span class="k">&lt;/p&gt;</span>
  <span class="k">&lt;/article&gt;</span>
<span class="k">&lt;/body&gt;</span>

<span class="c">RULE: a child's closing tag must come BEFORE its parent's.</span>
<span class="c">  ✓  &lt;p&gt;&lt;strong&gt;hi&lt;/strong&gt;&lt;/p&gt;      correct</span>
<span class="c">  ✗  &lt;p&gt;&lt;strong&gt;hi&lt;/p&gt;&lt;/strong&gt;      overlapping — invalid</span>
""", note='Slide 14–15', run='03-index-dbeb9734') + """

<h3>Links &mdash; all eight kinds on one slide</h3>
""" + code('hyperlinks.html', """
<span class="c">&lt;!-- destination = href, label = the text between the tags --&gt;</span>
<span class="k">&lt;a</span> <span class="t">href</span>=<span class="s">"https://google.com"</span><span class="k">&gt;</span>external site<span class="k">&lt;/a&gt;</span>
<span class="k">&lt;a</span> <span class="t">href</span>=<span class="s">"about.html"</span><span class="k">&gt;</span>another page on this site<span class="k">&lt;/a&gt;</span>
<span class="k">&lt;a</span> <span class="t">href</span>=<span class="s">"#links"</span><span class="k">&gt;</span>a place on THIS page<span class="k">&lt;/a&gt;</span>
<span class="k">&lt;a</span> <span class="t">href</span>=<span class="s">"https://google.com/#links"</span><span class="k">&gt;</span>a place on ANOTHER page<span class="k">&lt;/a&gt;</span>
<span class="k">&lt;a</span> <span class="t">href</span>=<span class="s">"mailto:shoug@example.com"</span><span class="k">&gt;</span>open the email program<span class="k">&lt;/a&gt;</span>
<span class="k">&lt;a</span> <span class="t">href</span>=<span class="s">"javascript:runProgram()"</span><span class="k">&gt;</span>run a JavaScript function<span class="k">&lt;/a&gt;</span>
<span class="k">&lt;a</span> <span class="t">href</span>=<span class="s">"tel:0521212121"</span><span class="k">&gt;</span>make a phone call<span class="k">&lt;/a&gt;</span>
<span class="k">&lt;a</span> <span class="t">href</span>=<span class="s">"http://m.me/PAGE_USERNAME"</span><span class="k">&gt;</span>open another program<span class="k">&lt;/a&gt;</span>

<span class="c">&lt;!-- the target of a #fragment is any element with a matching id --&gt;</span>
<span class="k">&lt;h2</span> <span class="t">id</span>=<span class="s">"links"</span><span class="k">&gt;</span>Links section<span class="k">&lt;/h2&gt;</span>

<span class="c">&lt;!-- an image can be the label — this is the "clickable image" home task --&gt;</span>
<span class="k">&lt;a</span> <span class="t">href</span>=<span class="s">"gallery.html"</span><span class="k">&gt;&lt;img</span> <span class="t">src</span>=<span class="s">"trulli.jpg"</span> <span class="t">alt</span>=<span class="s">"Trulli houses"</span><span class="k">&gt;&lt;/a&gt;</span>
""", note='Slides 21–22 + the slide 33 home task', run='06-hyperlink-d7300218') + """

<h3>Relative URLs &mdash; all six forms</h3>
<p>Absolute means the full URL: protocol, domain, path, filename. It is <em>required</em> when the
resource is on another site. Relative means the browser asks the current server, and comes in exactly
six shapes:</p>
""" + table(['Form', 'Written as', 'Meaning'], [
                ('1. Same directory', '<code>page.html</code>', 'Just the file name.'),
                ('2. Child directory', '<code>images/photo.jpg</code>', 'Subdirectory name, slash, file name.'),
                ('3. Grandchild / descendant', '<code>assets/img/icons/x.svg</code>', 'Each subdirectory name in turn, separated by slashes.'),
                ('4. Parent / ancestor', '<code>../styles.css</code> &middot; <code>../../a.html</code>', '<code>../</code> goes up one level; string several together to go higher.'),
                ('5. Sibling', '<code>../css/styles.css</code>', 'Up with <code>../</code>, then down like a child directory.'),
                ('6. Root reference', '<code>/images/logo.png</code>', 'Leading <code>/</code> starts from the server root, then down as normal.'),
            ]) + hook(
                "<strong>Root vs relative, the practical difference:</strong> a root reference "
                "(<code>/css/styles.css</code>) keeps working no matter how deep the page is, which is "
                "why it is safer for a shared stylesheet. A same-directory reference breaks the moment "
                "you move the file into a subfolder.") + """

<h3>Lists &mdash; three kinds</h3>
""" + code('lists.html', """
<span class="c">&lt;!-- 1. ORDERED: items with a set order. type = I, A, a, i --&gt;</span>
<span class="k">&lt;ol</span> <span class="t">type</span>=<span class="s">"I"</span><span class="k">&gt;</span>
  <span class="k">&lt;li&gt;</span>First<span class="k">&lt;/li&gt;</span>
  <span class="k">&lt;li&gt;</span>Second<span class="k">&lt;/li&gt;</span>
<span class="k">&lt;/ol&gt;</span>

<span class="c">&lt;!-- 2. UNORDERED: no particular order --&gt;</span>
<span class="k">&lt;ul</span> <span class="t">style</span>=<span class="s">"list-style-type:square"</span><span class="k">&gt;</span>   <span class="c">&lt;!-- disc | circle | square --&gt;</span>
  <span class="k">&lt;li&gt;</span>Chrome<span class="k">&lt;/li&gt;</span>
  <span class="k">&lt;li&gt;</span>Firefox<span class="k">&lt;/li&gt;</span>
<span class="k">&lt;/ul&gt;</span>

<span class="c">&lt;!-- 3. DESCRIPTION: name + description pairs. dt = term, dd = definition --&gt;</span>
<span class="k">&lt;dl&gt;</span>
  <span class="k">&lt;dt&gt;</span>HTTP<span class="k">&lt;/dt&gt;</span>
  <span class="k">&lt;dd&gt;</span>The protocol used for web communication.<span class="k">&lt;/dd&gt;</span>
  <span class="k">&lt;dt&gt;</span>DNS<span class="k">&lt;/dt&gt;</span>
  <span class="k">&lt;dd&gt;</span>Resolves domain names to IP addresses.<span class="k">&lt;/dd&gt;</span>
<span class="k">&lt;/dl&gt;</span>
""", note='Slide 29') + """

<h3>Images and character entities</h3>
""" + code('images-entities.html', """
<span class="c">&lt;!-- img is an EMPTY element: no closing tag, no text content.
     src and alt are the key attributes; title/width/height are optional. --&gt;</span>
<span class="k">&lt;img</span> <span class="t">src</span>=<span class="s">"trulli.jpg"</span> <span class="t">alt</span>=<span class="s">"Trulli houses in Puglia"</span> <span class="t">width</span>=<span class="s">"500"</span> <span class="t">height</span>=<span class="s">"333"</span><span class="k">&gt;</span>

<span class="c">&lt;!-- Entities: characters you cannot type, or that HTML has reserved.
     Use the NAME or the NUMBER — both work. --&gt;</span>
<span class="c">   &amp;nbsp;   &amp;#160;    non-breaking space</span>
<span class="c">   &amp;lt;     &amp;#60;     &lt;   ← reserved: HTML would read it as a tag</span>
<span class="c">   &amp;gt;     &amp;#62;     &gt;</span>
<span class="c">   &amp;copy;   &amp;#169;    ©</span>
<span class="c">   &amp;euro;   &amp;#8364;   €</span>
<span class="c">   &amp;trade;  &amp;#8482;   ™</span>

<span class="k">&lt;p&gt;</span>To write a tag in text: <span class="k">&lt;code&gt;</span>&amp;lt;div&amp;gt;<span class="k">&lt;/code&gt;</span> renders as &lt;div&gt;<span class="k">&lt;/p&gt;</span>
""", note='Slides 27–28') + """

<h3>Inline elements &mdash; do not break the flow of text</h3>
""" + table(['Element', 'Use'], [
                ('<code>&lt;a&gt;</code>', 'Anchor, used for hyperlinks.'),
                ('<code>&lt;abbr&gt;</code>', 'An abbreviation.'),
                ('<code>&lt;br&gt;</code>', 'Line break.'),
                ('<code>&lt;cite&gt;</code>', 'A citation &mdash; a reference to another work.'),
                ('<code>&lt;code&gt;</code>', 'Displaying markup or programming code.'),
                ('<code>&lt;em&gt;</code>', 'Emphasis.'),
                ('<code>&lt;small&gt;</code>', 'Fine print &mdash; nonvital text such as copyright or legal notices.'),
                ('<code>&lt;span&gt;</code>', 'The inline equivalent of <code>&lt;div&gt;</code>; marks text for CSS.'),
                ('<code>&lt;strong&gt;</code>', 'Content that is strongly important.'),
                ('<code>&lt;time&gt;</code>', 'Time and date data.'),
            ]) + """

<h3>HTML5 semantic structure</h3>
""" + code('semantic-page.html', """
<span class="k">&lt;body&gt;</span>
  <span class="k">&lt;header&gt;</span>                        <span class="c">&lt;!-- intro content for the page or a section --&gt;</span>
    <span class="k">&lt;nav&gt;</span>                          <span class="c">&lt;!-- a block of navigation links --&gt;</span>
      <span class="k">&lt;a</span> <span class="t">href</span>=<span class="s">"pagehtml.html"</span><span class="k">&gt;</span>HTML<span class="k">&lt;/a&gt;</span> |
      <span class="k">&lt;a</span> <span class="t">href</span>=<span class="s">"pagecss.html"</span><span class="k">&gt;</span>CSS<span class="k">&lt;/a&gt;</span> |
      <span class="k">&lt;a</span> <span class="t">href</span>=<span class="s">"pagejs.html"</span><span class="k">&gt;</span>JavaScript<span class="k">&lt;/a&gt;</span>
    <span class="k">&lt;/nav&gt;</span>
  <span class="k">&lt;/header&gt;</span>

  <span class="k">&lt;main&gt;</span>                          <span class="c">&lt;!-- the dominant content. Only ONE per page. --&gt;</span>
    <span class="k">&lt;h1&gt;</span>Survey<span class="k">&lt;/h1&gt;</span>
    <span class="k">&lt;section&gt;</span>                     <span class="c">&lt;!-- a thematic grouping, usually with a heading --&gt;</span>
      <span class="k">&lt;h2&gt;</span>Most Popular Browsers<span class="k">&lt;/h2&gt;</span>
      <span class="k">&lt;article&gt;</span>                   <span class="c">&lt;!-- self-contained: makes sense on its own --&gt;</span>
        <span class="k">&lt;h3&gt;</span>Google Chrome<span class="k">&lt;/h3&gt;</span>
        <span class="k">&lt;p&gt;</span>Released by Google in 2008.<span class="k">&lt;/p&gt;</span>
      <span class="k">&lt;/article&gt;</span>
    <span class="k">&lt;/section&gt;</span>

    <span class="k">&lt;figure&gt;</span>                      <span class="c">&lt;!-- content that could MOVE and the document still makes sense --&gt;</span>
      <span class="k">&lt;img</span> <span class="t">src</span>=<span class="s">"chart.png"</span> <span class="t">alt</span>=<span class="s">"Browser market share"</span><span class="k">&gt;</span>
      <span class="k">&lt;figcaption&gt;</span>Fig 1. Market share, 2026.<span class="k">&lt;/figcaption&gt;</span>
    <span class="k">&lt;/figure&gt;</span>
  <span class="k">&lt;/main&gt;</span>

  <span class="k">&lt;aside&gt;</span>Related links<span class="k">&lt;/aside&gt;</span>       <span class="c">&lt;!-- tangential content --&gt;</span>
  <span class="k">&lt;footer&gt;</span>&amp;copy; 2026 Shoug<span class="k">&lt;/footer&gt;</span>
<span class="k">&lt;/body&gt;</span>
""", note='Slides 30–32', run='08-html5elemnts-691fadaf') + hook(
                "<strong>The <code>&lt;figure&gt;</code> test, stated exactly as the slide does:</strong> "
                "could this content be moved to a different place in the document and the rest still "
                "make sense? If yes, it is a figure &mdash; and it need not be an image.")
        },
        {
            'id': 'forms', 'nav': 'Forms', 'label': 'Slides 41&ndash;63',
            'title': 'Every form control, with the attributes that carry the marks',
            'html': """
<h3>GET vs POST, as this chapter states it</h3>
""" + table(['GET', 'POST'], [
                ('Data is clearly visible in the address bar &mdash; helpful in development, a problem in production.', 'Data can contain binary data.'),
                ('Data remains in browser history and cache &mdash; a security risk on public computers.', 'Data is hidden from the user (though visible in the DevTools Network/Payload tab).'),
                ('Data can be bookmarked.', 'Submitted data is not stored in cache, history or bookmarks.'),
                ('There is a limit on the number of characters returned.', 'No comparable character limit.'),
            ]) + """
<p>The slides add two warnings worth quoting back in an exam. First: HTML forms accept
<strong>only</strong> <code>get</code> or <code>post</code> &mdash; DELETE and UPDATE have to be sent
with JavaScript. Second, verbatim: <em>&ldquo;while the POST method hides form data, any user could
easily inspect the HTTP header. As a result, the POST method is NOT sufficient from a security
standpoint.&rdquo;</em></p>

<h3>Text input controls</h3>
""" + code('text-controls.html', """
<span class="k">&lt;input</span> <span class="t">type</span>=<span class="s">"text"</span>     <span class="t">name</span>=<span class="s">"fname"</span>  <span class="t">placeholder</span>=<span class="s">"Shoug"</span><span class="k">&gt;</span>
<span class="k">&lt;input</span> <span class="t">type</span>=<span class="s">"password"</span> <span class="t">name</span>=<span class="s">"pwd"</span>    <span class="t">required</span><span class="k">&gt;</span>      <span class="c">&lt;!-- required = HTML5 built-in validation --&gt;</span>
<span class="k">&lt;input</span> <span class="t">type</span>=<span class="s">"email"</span>    <span class="t">name</span>=<span class="s">"mail"</span><span class="k">&gt;</span>                 <span class="c">&lt;!-- browser checks the @ format --&gt;</span>
<span class="k">&lt;input</span> <span class="t">type</span>=<span class="s">"tel"</span>      <span class="t">name</span>=<span class="s">"phone"</span><span class="k">&gt;</span>
<span class="k">&lt;input</span> <span class="t">type</span>=<span class="s">"search"</span>   <span class="t">name</span>=<span class="s">"q"</span><span class="k">&gt;</span>
<span class="k">&lt;input</span> <span class="t">type</span>=<span class="s">"url"</span>      <span class="t">name</span>=<span class="s">"site"</span><span class="k">&gt;</span>
<span class="k">&lt;input</span> <span class="t">type</span>=<span class="s">"hidden"</span>   <span class="t">name</span>=<span class="s">"id"</span> <span class="t">value</span>=<span class="s">"42"</span><span class="k">&gt;</span>     <span class="c">&lt;!-- sent, but not shown --&gt;</span>

<span class="c">&lt;!-- multiline text: a CONTAINER, not an empty element --&gt;</span>
<span class="k">&lt;textarea</span> <span class="t">name</span>=<span class="s">"bio"</span> <span class="t">rows</span>=<span class="s">"5"</span> <span class="t">cols</span>=<span class="s">"40"</span><span class="k">&gt;&lt;/textarea&gt;</span>
""", note='Slide 48', run='2-example-form-input-control-ffcd1087') + """

<h3>Choice controls: select, radio, checkbox</h3>
""" + code('select.html', """
<span class="c">&lt;!-- SELECT: a drop-down list --&gt;</span>
<span class="k">&lt;label</span> <span class="t">for</span>=<span class="s">"cars"</span><span class="k">&gt;</span>Choose a car:<span class="k">&lt;/label&gt;</span>
<span class="k">&lt;select</span> <span class="t">name</span>=<span class="s">"cars"</span> <span class="t">id</span>=<span class="s">"cars"</span><span class="k">&gt;</span>
  <span class="k">&lt;option</span> <span class="t">value</span>=<span class="s">"volvo"</span><span class="k">&gt;</span>Volvo<span class="k">&lt;/option&gt;</span>
  <span class="k">&lt;option</span> <span class="t">value</span>=<span class="s">"saab"</span> <span class="t">selected</span><span class="k">&gt;</span>Saab<span class="k">&lt;/option&gt;</span>   <span class="c">&lt;!-- selected = the DEFAULT --&gt;</span>
  <span class="k">&lt;option</span> <span class="t">value</span>=<span class="s">"audi"</span><span class="k">&gt;</span>Audi<span class="k">&lt;/option&gt;</span>
<span class="k">&lt;/select&gt;</span>

<span class="c">&lt;!-- multiple = more than one item can be chosen.
     No value attribute? The text inside the container is sent instead. --&gt;</span>
<span class="k">&lt;select</span> <span class="t">name</span>=<span class="s">"mult_cars_var"</span> <span class="t">id</span>=<span class="s">"multipl_cars"</span> <span class="t">multiple</span><span class="k">&gt;</span>
  <span class="k">&lt;option&gt;</span>Volvo<span class="k">&lt;/option&gt;</span>        <span class="c">&lt;!-- sends cars=Volvo --&gt;</span>
  <span class="k">&lt;option&gt;</span>Saab<span class="k">&lt;/option&gt;</span>
<span class="k">&lt;/select&gt;</span>

<span class="c">&lt;!-- optgroup groups related options --&gt;</span>
<span class="k">&lt;select</span> <span class="t">name</span>=<span class="s">"cars_optg_var"</span> <span class="t">multiple</span><span class="k">&gt;</span>
  <span class="k">&lt;optgroup</span> <span class="t">label</span>=<span class="s">"Swedish Cars"</span><span class="k">&gt;</span>
    <span class="k">&lt;option</span> <span class="t">value</span>=<span class="s">"volvo"</span><span class="k">&gt;</span>Volvo<span class="k">&lt;/option&gt;</span>
    <span class="k">&lt;option</span> <span class="t">value</span>=<span class="s">"saab"</span><span class="k">&gt;</span>Saab<span class="k">&lt;/option&gt;</span>
  <span class="k">&lt;/optgroup&gt;</span>
  <span class="k">&lt;optgroup</span> <span class="t">label</span>=<span class="s">"German Cars"</span><span class="k">&gt;</span>
    <span class="k">&lt;option</span> <span class="t">value</span>=<span class="s">"audi"</span><span class="k">&gt;</span>Audi<span class="k">&lt;/option&gt;</span>
  <span class="k">&lt;/optgroup&gt;</span>
<span class="k">&lt;/select&gt;</span>
""", note='Slides 50–51', run='3-select-fad7b8d3') + code('radio-checkbox.html', """
<span class="c">&lt;!-- RADIO: pick ONE from a small, visible list.
     The SHARED name is what makes them mutually exclusive.
     value is what gets sent:  city=1  if Riyadh is selected. --&gt;</span>
<span class="k">&lt;input</span> <span class="t">type</span>=<span class="s">"radio"</span> <span class="t">id</span>=<span class="s">"riyadh"</span> <span class="t">name</span>=<span class="s">"city"</span> <span class="t">value</span>=<span class="s">"1"</span> <span class="t">checked</span><span class="k">&gt;</span>
<span class="k">&lt;label</span> <span class="t">for</span>=<span class="s">"riyadh"</span><span class="k">&gt;</span>Riyadh<span class="k">&lt;/label&gt;</span>
<span class="k">&lt;input</span> <span class="t">type</span>=<span class="s">"radio"</span> <span class="t">id</span>=<span class="s">"jeddah"</span> <span class="t">name</span>=<span class="s">"city"</span> <span class="t">value</span>=<span class="s">"2"</span><span class="k">&gt;</span>
<span class="k">&lt;label</span> <span class="t">for</span>=<span class="s">"jeddah"</span><span class="k">&gt;</span>Jeddah<span class="k">&lt;/label&gt;</span>

<span class="c">&lt;!-- CHECKBOX: a yes/no, on/off answer. Each CHECKED box sends its value.
     Different names = independent answers. --&gt;</span>
<span class="k">&lt;input</span> <span class="t">type</span>=<span class="s">"checkbox"</span> <span class="t">id</span>=<span class="s">"news"</span> <span class="t">name</span>=<span class="s">"news"</span> <span class="t">value</span>=<span class="s">"yes"</span> <span class="t">checked</span><span class="k">&gt;</span>
<span class="k">&lt;label</span> <span class="t">for</span>=<span class="s">"news"</span><span class="k">&gt;</span>Send me the newsletter<span class="k">&lt;/label&gt;</span>
""", note='Slides 53–54', run='4-radio-button-6f09bd46') + hook(
                "<strong>radio vs checkbox in one line:</strong> radios share a <code>name</code> so "
                "only one can win; checkboxes each keep their own <code>name</code> so each answers "
                "independently. Both use <code>checked</code> for the default.") + """

<h3>Buttons &mdash; five ways, three behaviours</h3>
""" + code('buttons.html', """
<span class="k">&lt;input</span> <span class="t">type</span>=<span class="s">"submit"</span> <span class="t">value</span>=<span class="s">"Send"</span><span class="k">&gt;</span>    <span class="c">&lt;!-- submits the form data to the server --&gt;</span>
<span class="k">&lt;input</span> <span class="t">type</span>=<span class="s">"reset"</span>  <span class="t">value</span>=<span class="s">"Clear"</span><span class="k">&gt;</span>   <span class="c">&lt;!-- clears data the user already entered --&gt;</span>
<span class="k">&lt;input</span> <span class="t">type</span>=<span class="s">"button"</span> <span class="t">value</span>=<span class="s">"Count"</span><span class="k">&gt;</span>   <span class="c">&lt;!-- does NOTHING without JavaScript --&gt;</span>
<span class="k">&lt;input</span> <span class="t">type</span>=<span class="s">"image"</span>  <span class="t">src</span>=<span class="s">"go.png"</span> <span class="t">alt</span>=<span class="s">"Go"</span><span class="k">&gt;</span> <span class="c">&lt;!-- a submit button drawn as an image --&gt;</span>

<span class="c">&lt;!-- &lt;button&gt; is a CONTAINER, so it allows far more customisation:
     you can put markup, icons and images inside it. --&gt;</span>
<span class="k">&lt;button</span> <span class="t">type</span>=<span class="s">"submit"</span><span class="k">&gt;&lt;strong&gt;</span>Send<span class="k">&lt;/strong&gt;</span> <span class="k">&lt;img</span> <span class="t">src</span>=<span class="s">"plane.png"</span> <span class="t">alt</span>=<span class="s">""</span><span class="k">&gt;&lt;/button&gt;</span>

<span class="c">&lt;!-- WARNING from slide 57: type="submit" is the DEFAULT for &lt;button&gt;.
     A &lt;button&gt; with no type inside a form will submit it. --&gt;</span>
<span class="k">&lt;button</span> <span class="t">type</span>=<span class="s">"button"</span> <span class="t">onclick</span>=<span class="s">"doSomething()"</span><span class="k">&gt;</span>Safe<span class="k">&lt;/button&gt;</span>
""", note='Slides 55–57', run='04b-button-7b639bc4') + """

<h3>HTML5 numeric, colour, date and time controls</h3>
""" + code('html5-controls.html', """
<span class="c">&lt;!-- number and range reduce the need for client-side numeric validation.
     You still validate on the SERVER for security. --&gt;</span>
<span class="k">&lt;input</span> <span class="t">type</span>=<span class="s">"number"</span> <span class="t">name</span>=<span class="s">"qty"</span>  <span class="t">min</span>=<span class="s">"1"</span> <span class="t">max</span>=<span class="s">"10"</span> <span class="t">step</span>=<span class="s">"1"</span><span class="k">&gt;</span>
<span class="k">&lt;input</span> <span class="t">type</span>=<span class="s">"range"</span>  <span class="t">name</span>=<span class="s">"vol"</span>  <span class="t">min</span>=<span class="s">"0"</span> <span class="t">max</span>=<span class="s">"100"</span> <span class="t">value</span>=<span class="s">"50"</span><span class="k">&gt;</span>
<span class="k">&lt;input</span> <span class="t">type</span>=<span class="s">"color"</span>  <span class="t">name</span>=<span class="s">"theme"</span> <span class="t">value</span>=<span class="s">"#b829ea"</span><span class="k">&gt;</span>
""", note='Slides 59–60', run='5-num-range-color-28e1eeea') + table(
                ['Type', 'What it collects', 'Format'], [
                    ('<code>date</code>', 'A general date.', '<code>yyyy-mm-dd</code>'),
                    ('<code>time</code>', 'A time.', '<code>HH:MM:SS</code>'),
                    ('<code>datetime</code>', 'A date and time.', '&mdash;'),
                    ('<code>datetime-local</code>', 'A date and time with no time zone.', '&mdash;'),
                    ('<code>month</code>', 'A month within a year.', '<code>yyyy-mm</code>'),
                    ('<code>week</code>', 'A week within a year.', '<code>yyyy-W##</code>'),
                ]) + """
<p>The live example for these is <a href="/academics/software-engineering/se371/extra-resources/resource-viewers/6-date-7877ac85/" target="_blank" rel="noopener">6-date.html</a>.</p>

<h3>Labels, properly</h3>
""" + code('labels.html', """
<span class="c">&lt;!-- Method 1: for= matches id=. The two elements can be anywhere. --&gt;</span>
<span class="k">&lt;label</span> <span class="t">for</span>=<span class="s">"email"</span><span class="k">&gt;</span>Email address<span class="k">&lt;/label&gt;</span>
<span class="k">&lt;input</span> <span class="t">type</span>=<span class="s">"email"</span> <span class="t">id</span>=<span class="s">"email"</span> <span class="t">name</span>=<span class="s">"email"</span><span class="k">&gt;</span>

<span class="c">&lt;!-- Method 2: wrap the input. No for/id needed. --&gt;</span>
<span class="k">&lt;label&gt;</span>Email address <span class="k">&lt;input</span> <span class="t">type</span>=<span class="s">"email"</span> <span class="t">name</span>=<span class="s">"email"</span><span class="k">&gt;&lt;/label&gt;</span>

<span class="c">Why it matters (it is in the chapter objectives — "improve accessibility"):
  • screen readers announce the label when the field is focused
  • clicking the label focuses the field — a much larger click target
  • it is the accessible way to label a radio button or checkbox</span>

<span class="c">&lt;!-- fieldset + legend group related controls, e.g. a set of radio buttons --&gt;</span>
<span class="k">&lt;fieldset&gt;</span>
  <span class="k">&lt;legend&gt;</span>Choose your city<span class="k">&lt;/legend&gt;</span>
  <span class="c">&lt;!-- radios here --&gt;</span>
<span class="k">&lt;/fieldset&gt;</span>
""", note='Slide 63')
        },
        {
            'id': 'validation', 'nav': 'Validation', 'label': 'Slides 64&ndash;69',
            'title': 'Validation — the concept that spans the whole course',
            'html': """
<p>Slide 64 opens with the line to remember: <strong>user input must never be trusted.</strong> It may
be missing, wrongly formatted, or contain JavaScript or SQL intended as an attack.</p>

<h3>The three levels</h3>
""" + table(['Level', 'What it is', 'Why it is not enough'], [
                ('<strong>1. HTML5</strong> <span class="w-skim">client</span>',
                 'The browser performs basic validation from attributes like <code>required</code>, <code>type="email"</code>, <code>min</code>/<code>max</code> and <code>pattern</code>.',
                 'Free, but trivially bypassed &mdash; the user can edit the markup in DevTools.'),
                ('<strong>2. JavaScript</strong> <span class="w-skim">client</span>',
                 'Dramatically improves the user experience of data-entry forms; the slides call it an essential feature of any real-world site that uses forms. This is chapter 5.',
                 'Explicitly stated on the slide: <em>not sufficient</em>. The user can disable JavaScript or send the request directly.'),
                ('<strong>3. Server-side</strong> <span class="w-write">server</span>',
                 'Arguably the most important, because it is the only validation <strong>guaranteed to run</strong>. This is chapters 6 and 7.',
                 '&mdash; Develop server-side functionality as if no client-side validation happened at all.'),
            ]) + hook(
                "<strong>Say this sentence in the exam:</strong> &ldquo;Client-side validation exists for "
                "the user&rsquo;s convenience; server-side validation exists for correctness and "
                "security, because it is the only one guaranteed to run.&rdquo; It answers most "
                "validation questions on its own.") + """

<h3>The six types of validation</h3>
""" + table(['Type', 'Example'], [
                ('<strong>Required information</strong>', 'Some fields simply cannot be left empty.'),
                ('<strong>Correct data type</strong>', 'Numbers and dates must obey their type&rsquo;s rules.'),
                ('<strong>Correct format</strong>', 'Postal codes, credit card numbers and ID numbers follow pattern rules.'),
                ('<strong>Comparison</strong>', 'A value judged against another value &mdash; confirm password, or end date after start date.'),
                ('<strong>Range check</strong>', 'A number that must fall between a minimum and a maximum.'),
                ('<strong>Custom</strong>', 'Any rule specific to the application.'),
            ]) + """
<h3>Notifying the user &mdash; three questions the message must answer</h3>
<ol>
  <li><strong>What is the problem?</strong> Users will not read a lengthy message to work out what to change.</li>
  <li><strong>Where is the problem?</strong> The indication belongs near the field that caused it.</li>
  <li><strong>How do I fix it?</strong> Do not just say the date is wrong &mdash; say what format you expect.</li>
</ol>

<h3>Five ways to reduce errors before they happen</h3>
<ul>
  <li>Put textual hints on the form itself.</li>
  <li>Use tool tips or pop-overs for context-sensitive help &mdash; via CSS or the <code>title</code> attribute.</li>
  <li>Provide a JavaScript input mask, e.g. <code>(999)-999-9999</code>.</li>
  <li>Choose good default values for text fields.</li>
  <li><strong>Pick a better input type than <code>text</code>.</strong> A <code>type="date"</code> field cannot be given a badly formatted date in the first place.</li>
</ul>
""" + code('validation-by-attribute.html', """
<span class="c">&lt;!-- Level 1 in practice: every one of these is a validation rule the
     browser enforces for free, before a single line of JavaScript. --&gt;</span>
<span class="k">&lt;input</span> <span class="t">type</span>=<span class="s">"text"</span>   <span class="t">name</span>=<span class="s">"user"</span>  <span class="t">required</span>
       <span class="t">minlength</span>=<span class="s">"3"</span> <span class="t">maxlength</span>=<span class="s">"20"</span><span class="k">&gt;</span>              <span class="c">← required + length</span>

<span class="k">&lt;input</span> <span class="t">type</span>=<span class="s">"email"</span>  <span class="t">name</span>=<span class="s">"mail"</span>  <span class="t">required</span><span class="k">&gt;</span>          <span class="c">← correct data type</span>

<span class="k">&lt;input</span> <span class="t">type</span>=<span class="s">"number"</span> <span class="t">name</span>=<span class="s">"age"</span>   <span class="t">min</span>=<span class="s">"18"</span> <span class="t">max</span>=<span class="s">"99"</span><span class="k">&gt;</span>   <span class="c">← range check</span>

<span class="k">&lt;input</span> <span class="t">type</span>=<span class="s">"tel"</span>    <span class="t">name</span>=<span class="s">"phone"</span>
       <span class="t">pattern</span>=<span class="s">"05[0-9]{8}"</span>                        <span class="c">← correct format</span>
       <span class="t">title</span>=<span class="s">"Saudi mobile: 05 followed by 8 digits"</span><span class="k">&gt;</span>  <span class="c">← "how do I fix it?"</span>

<span class="c">&lt;!-- Turn the browser's checks off to test your own:  &lt;form novalidate&gt; --&gt;</span>
""", note='Slides 64–69 as code') + """

<h3>Colour models (slides 70&ndash;71)</h3>
<p>Three ways to describe colour: <strong>names</strong>, <strong>RGB</strong> and <strong>HSL</strong>
(hue, saturation, lightness). RGB works because the visible spectrum can be reproduced by combining
red, green and blue light, and each pixel is made of tiny red, green and blue subpixels. Because the
three combine to produce white, they are called <strong>additive</strong> colours. Chapter 3 picks
this up on its colour-values slide.</p>
"""
        },
        {
            'id': 'traps', 'nav': 'Traps', 'label': 'Marks Lost Here',
            'title': 'The seven things people get wrong',
            'html': (
                trap('Using <code>id</code> where the form needs <code>name</code>',
                     'An input with an <code>id</code> but no <code>name</code> is styled fine, selectable from JavaScript, and <strong>never submitted</strong>. The query string simply will not contain it.',
                     '<code>name</code> is for the server. <code>id</code> is for the label, CSS and JavaScript. Real forms usually need both.') +
                trap('Radio buttons that do not deselect each other',
                     'If each radio has a different <code>name</code>, the browser treats them as unrelated single-option groups, so all of them can be selected at once.',
                     'Radios in one group must <strong>share the same <code>name</code></strong>. Different <code>value</code>, same <code>name</code>.') +
                trap('A <code>&lt;button&gt;</code> that reloads the page',
                     'You add <code>&lt;button onclick="calc()"&gt;</code> inside a form and the page flashes and resets. The default <code>type</code> for <code>&lt;button&gt;</code> is <code>submit</code>, so it submitted the form.',
                     'Write <code>&lt;button type="button"&gt;</code> for anything that is not meant to submit. Slide 57 says this explicitly.') +
                trap('Choosing heading levels for their size',
                     'Picking <code>&lt;h3&gt;</code> because you want smaller bold text is exactly the anti-example on slide 19. It breaks the document outline and the semantic-markup principle from slide 6.',
                     'Choose the level that is semantically right, then resize it in CSS.') +
                trap('Mixing up <code>colspan</code> and <code>rowspan</code>',
                     '<code>colspan</code> makes a cell wider &mdash; it eats cells to its right. <code>rowspan</code> makes it taller &mdash; it eats cells below. People reliably swap them under pressure.',
                     'Read them as instructions: <em>span this many <strong>col</strong>umns</em> = horizontal; <em>span this many <strong>row</strong>s</em> = vertical. And remember the spanned-over cells must be <strong>deleted</strong> from the following rows, or the table grows extra columns.') +
                trap('Believing POST is secure',
                     'It appears again here because the slides warn about it twice. POST hides data from the address bar, not from the user &mdash; the Network/Payload tab in DevTools shows it in full.',
                     'POST controls <em>where</em> the data travels. HTTPS controls whether anyone else can read it. Server-side validation controls whether you can trust it.') +
                trap('Assuming <code>required</code> is enough',
                     'HTML5 validation runs in the browser, and the browser belongs to the user. Deleting the attribute in DevTools, or sending the request with <code>curl</code>, skips it entirely.',
                     'Treat every client-side check as a convenience. Re-validate everything on the server &mdash; the only validation guaranteed to run.')
            )
        },
        {
            'id': 'cheat', 'nav': 'Cheat Sheet', 'label': 'One Screen',
            'title': 'Chapter 2 on a single screen',
            'html': cheat([
                ('Document', [
                    '<code>&lt;!DOCTYPE html&gt;</code> &mdash; type, not version',
                    '<code>&lt;html lang="en"&gt;</code> &mdash; root element',
                    '<code>&lt;head&gt;</code> &mdash; describes the document',
                    '<code>&lt;body&gt;</code> &mdash; what is displayed',
                    '<code>&lt;meta charset&gt;</code>, <code>&lt;title&gt;</code>, <code>&lt;meta name="description"&gt;</code>',
                ]),
                ('Semantic HTML5', [
                    '<code>header</code> <code>nav</code> <code>main</code> <code>section</code>',
                    '<code>article</code> <code>aside</code> <code>footer</code>',
                    '<code>figure</code> + <code>figcaption</code>',
                    'Use these instead of anonymous <code>div</code>s',
                ]),
                ('Tables', [
                    '<code>table &gt; thead/tbody/tfoot &gt; tr &gt; th/td</code>',
                    'All content lives in <code>td</code> or <code>th</code>',
                    '<code>colspan="2"</code> &mdash; wider, eats cells to the right',
                    '<code>rowspan="2"</code> &mdash; taller, eats cells below',
                    'Delete the cells that got spanned over',
                ]),
                ('Form basics', [
                    '<code>action</code> &mdash; URL that processes the data',
                    '<code>method</code> &mdash; <code>get</code> or <code>post</code> only',
                    '<code>name</code> &mdash; becomes the query-string key',
                    '<code>id</code> &mdash; for <code>label for=</code>, CSS, JS',
                    'Query string: <code>?k=v&amp;k=v</code>, URL-encoded',
                ]),
                ('Controls', [
                    '<code>input</code>: text, password, email, tel, url, search, hidden',
                    '<code>input</code>: number, range, color, date, time, month, week',
                    '<code>textarea</code> &mdash; multiline, a container',
                    '<code>select</code> + <code>option</code> + <code>optgroup</code>',
                    '<code>multiple</code> &middot; <code>selected</code> &middot; <code>checked</code> &middot; <code>required</code>',
                ]),
                ('Buttons', [
                    '<code>submit</code> &mdash; sends the form',
                    '<code>reset</code> &mdash; clears entered data',
                    '<code>button</code> &mdash; needs JavaScript',
                    '<code>image</code> &mdash; submit drawn as an image',
                    '<code>&lt;button&gt;</code> &mdash; container, defaults to submit',
                ]),
                ('Relative URLs', [
                    '<code>page.html</code> &mdash; same directory',
                    '<code>img/x.jpg</code> &mdash; child',
                    '<code>../x.css</code> &mdash; parent',
                    '<code>../css/x.css</code> &mdash; sibling',
                    '<code>/css/x.css</code> &mdash; from the server root',
                ]),
                ('Entities', [
                    '<code>&amp;nbsp;</code> <code>&amp;#160;</code> non-breaking space',
                    '<code>&amp;lt;</code> <code>&amp;#60;</code> &nbsp; <code>&amp;gt;</code> <code>&amp;#62;</code>',
                    '<code>&amp;copy;</code> <code>&amp;#169;</code> &nbsp; <code>&amp;euro;</code> <code>&amp;#8364;</code>',
                    '<code>&amp;trade;</code> <code>&amp;#8482;</code>',
                ]),
                ('Validation', [
                    '1. HTML5 &mdash; free, bypassable',
                    '2. JavaScript &mdash; good UX, not sufficient',
                    '3. Server &mdash; the only one guaranteed to run',
                    'Types: required, data type, format, comparison, range, custom',
                ]),
            ])
        },
        {
            'id': 'drills', 'nav': 'Drills', 'label': 'Type It Blind',
            'title': 'Open a blank file and type these without looking',
            'html': """
<p>This chapter is graded on production, not recognition. Reading the slides again will not help;
typing will. Work through the list in a blank <code>.html</code> file with Live Server running.</p>
""" + drills([
                'The full HTML5 document skeleton, including <code>charset</code>, <code>viewport</code>, <code>title</code> and a meta description.',
                'A table with <code>thead</code>, <code>tbody</code> and <code>tfoot</code>, three columns and three data rows.',
                'The same table, but with the first cell of row 2 spanning two columns &mdash; and remember to delete the displaced cell.',
                'A table where the first column spans three rows.',
                'A registration form with text, email, password, a date, a number with min/max and a submit button &mdash; every field labelled.',
                'A select list with an <code>optgroup</code>, a default <code>selected</code> option, and one option with no <code>value</code>.',
                'A group of three radio buttons that actually behave as a group, with the second one checked by default.',
                'Two checkboxes that answer independently, with one checked by default.',
                'A page using all nine HTML5 semantic elements at least once.',
                'A <code>figure</code> with a <code>figcaption</code>, and a one-line justification of why that content qualifies as a figure.',
                'Six links: external, internal page, same-page fragment, mailto, tel, and an image used as the link label.',
                'A description list defining four terms from chapter 1.',
                'The same stylesheet referenced four ways: same directory, child, parent and root reference.',
                'A form that demonstrates all six validation types using HTML5 attributes only.',
                'Write out what query string <code>?</code> the browser builds when your registration form is submitted with GET, then check it in the address bar.',
            ]) + """
<p>Two printable cheat sheets already sit in your study material:
<a href="/academics/software-engineering/se371/extra-resources/resource-viewers/html-cheat-sheet-q1-1f7fac94/" target="_blank" rel="noopener">HTML cheat sheet Q1</a> and
<a href="/academics/software-engineering/se371/extra-resources/resource-viewers/html-cheat-sheet-2-q1-bfbd321f/" target="_blank" rel="noopener">HTML cheat sheet 2</a>.</p>
"""
        },
    ],
    'quiz': [
        {'tag': 'Forms', 'q': 'A text input has id="email" and no name attribute. The form is submitted with GET. What appears in the query string?',
         'opts': ['email=whatever the user typed', 'Nothing — the field is not submitted at all',
                  'An empty value: email=', 'The id is used as the key only if name is missing'],
         'a': 1,
         'why': 'name is what becomes the key in the query string. Without it the control is not successful and the browser does not send it. id only serves the label, CSS and JavaScript.'},
        {'tag': 'Forms', 'q': 'Three radio buttons each have a different name attribute. What happens?',
         'opts': ['They work normally as a group', 'All three can be selected at the same time',
                  'Only the last one can be selected', 'The form refuses to submit'],
         'a': 1,
         'why': 'The shared name is what makes radio buttons mutually exclusive. Different names means three independent one-option groups, so all three can be checked at once.'},
        {'tag': 'Semantics', 'q': 'Why does the chapter tell you not to choose a heading level based on how it looks?',
         'opts': ['Because browsers render heading sizes differently',
                  'Because HTML describes structure and meaning, and presentation belongs to CSS',
                  'Because h3 is deprecated in HTML5',
                  'Because headings below h3 are ignored by search engines'],
         'a': 1,
         'why': 'This is the semantic-markup principle from slide 6. Headings also build the document outline, so the wrong level damages that outline for browsers and screen readers.'},
        {'tag': 'Validation', 'q': 'Which statement about validation matches the slides?',
         'opts': ['JavaScript validation is sufficient if it covers every field',
                  'HTML5 validation cannot be bypassed by the user',
                  'Server-side validation is the only validation guaranteed to run',
                  'Server-side validation can be skipped if the client validates first'],
         'a': 2,
         'why': 'Slide 65 states it directly and adds the practical consequence: server-side functionality should be developed as if no validation happened on the client at all.'},
        {'tag': 'Tables', 'q': 'A row has three cells and you set colspan="2" on the first one. What else must you do?',
         'opts': ['Add rowspan="1" to the other cells', 'Delete one of the remaining cells in that row',
                  'Add an empty td at the end of the row', 'Nothing — the browser adjusts automatically'],
         'a': 1,
         'why': 'The first cell now occupies two column positions, so the row needs one fewer cell. Leaving all three makes the row four columns wide and the table ragged.'},
        {'tag': 'HTTP', 'q': 'Which HTTP methods can be used in the method attribute of an HTML form?',
         'opts': ['GET and POST only', 'GET, POST and PUT', 'GET, POST, PUT and DELETE', 'Any HTTP method'],
         'a': 0,
         'why': 'Slide 43 is explicit: only GET or POST may be used in HTML forms. DELETE and UPDATE have to be sent using JavaScript, which is what you do from chapter 6 onwards.'},
        {'tag': 'URLs', 'q': 'Your page is at /shop/items/detail.html and you need /shop/css/styles.css. Which reference is correct?',
         'opts': ['<code>css/styles.css</code>', '<code>../css/styles.css</code>',
                  '<code>../../css/styles.css</code>', '<code>./styles.css</code>'],
         'a': 1,
         'why': 'This is the sibling-directory case: go up one level with ../ to reach /shop/, then down into css/. The root reference /shop/css/styles.css would also work.'},
        {'tag': 'Buttons', 'q': 'You put <button onclick="calculate()">Go</button> inside a form and the page reloads when clicked. Why?',
         'opts': ['onclick is not valid on button elements',
                  'The default type of a button element is submit',
                  'The function threw an error so the browser fell back to submitting',
                  'Buttons must be outside the form element'],
         'a': 1,
         'why': 'A button element defaults to type="submit", so it submits the form and the page navigates. Write type="button" for anything that only runs JavaScript.'},
    ],
})


# ═══════════════════════════════════════════════════════════════════════════ #
# CHAPTER 03 — CSS: Selectors, the Cascade, the Box Model, Layout
# ═══════════════════════════════════════════════════════════════════════════ #

CHAPTERS.append({
    'num': 3,
    'slug': '03-css',
    'file': 'css.html',
    'title': 'CSS: Selectors, Cascade and Layout',
    'desc': ('Slide-by-slide breakdown of SE371 Chapter 3 — CSS syntax, all selector types, the '
             'cascade and specificity, the box model, text styling, flexbox, grid and responsive design.'),
    'sub': ('The longest deck in the course and the one with the most missing content: the flexbox and '
            'grid property tables are screenshots, so the slide text alone will not teach you them. '
            'Everything those slides skipped is reconstructed here as code you can run.'),
    'stats': ['85 slides', 'Two decks in one', 'Most screenshot-heavy', 'Book ch. 4 + 5 + 7'],
    'sections': [
        {
            'id': 'orient', 'nav': 'Start Here', 'label': 'Orientation',
            'title': 'What this chapter is really for',
            'html': """
<p>Split again: <strong>Part 1 (slides 1&ndash;60)</strong> is selectors, the cascade, the box model
and text/table/form styling; <strong>Part 2 (slides 61&ndash;84)</strong> is flexbox, grid and
responsive design.</p>

<p>Be warned about this deck specifically. A large share of its most important slides &mdash; the
flexbox container properties (65&ndash;66), the flex item properties (67), the grid structure slides
(69&ndash;71) &mdash; are <strong>images with almost no text on them</strong>. If you revise from the
slide text alone you will have a chapter with a hole in the middle exactly where the layout marks are.
That gap is what the code sections below are for.</p>

<div class="grid-2">
  <div class="card">
    <h4>The two ideas everything hangs off</h4>
    <p><strong>The cascade</strong> decides which rule wins when several apply: inheritance, then
    specificity, then location. <strong>The box model</strong> decides how big things are: content,
    padding, border, margin. Almost every "why does my page look wrong" question is one of these two.</p>
  </div>
  <div class="card">
    <h4>Engineering framing worth quoting</h4>
    <p>Slide 3 gives the reason CSS exists in engineering terms: <strong>separation of concerns and
    reuse</strong>. The listed benefits &mdash; control over formatting, maintainability,
    accessibility, download speed, output flexibility &mdash; all follow from those two.</p>
  </div>
</div>
"""
        },
        {
            'id': 'map', 'nav': 'Slide Map', 'label': 'Navigation',
            'title': 'All 85 slides, weighted',
            'html': slidemap([
                ('1&ndash;3', 'What CSS is; benefits', 'MEMORIZE',
                 'Separation of concerns + reuse, then five benefits. A likely short-answer question.'),
                ('4&ndash;5', 'Rule, selector, declaration, declaration block, values', 'MEMORIZE',
                 'Get the vocabulary exactly right &mdash; questions are worded using these terms.'),
                ('6', 'The five ways to write a colour', 'MEMORIZE',
                 'Name, RGB, hexadecimal, RGBa, HSL/HSLA. Know which are CSS3-only.'),
                ('7', 'Units: relative vs absolute', 'MEMORIZE',
                 '<code>px</code>, <code>em</code>, <code>vw</code> are the ones asked about; <code>in</code> and <code>cm</code> are absolute.'),
                ('8&ndash;11', 'Inline, embedded and external styles', 'WRITE',
                 'Know the syntax of all three and why external wins: one change updates every page, and the browser can cache it.'),
                ('12&ndash;15', 'Element, class and ID selectors', 'WRITE',
                 'The <code>id</code> is unique to one element; a <code>class</code> targets many. An element can carry several classes.'),
                ('16&ndash;18', 'Attribute selectors &mdash; all six operators', 'WRITE',
                 '<code>[]</code> <code>[=]</code> <code>[~=]</code> <code>[^=]</code> <code>[*=]</code> <code>[$=]</code>. Very examinable, and easy marks once memorised.'),
                ('19&ndash;22', 'Pseudo-classes and pseudo-elements', 'WRITE',
                 'Link states in order, <code>:hover</code>, <code>:active</code>, <code>:first-child</code>, <code>:first-letter</code>, <code>:first-line</code>, <code>:is()</code>.'),
                ('23', 'Task: last child red; links whose href contains "example"', 'WRITE',
                 'Do it. It is two lines and it tests both halves of the selector material.'),
                ('25&ndash;26', 'Contextual selectors / combinators', 'WRITE',
                 'Space, <code>&gt;</code>, <code>+</code>, <code>~</code>. Learn what each one actually matches, not just its name.'),
                ('27', 'Nested CSS rules', 'SKIM',
                 'New, and shown side by side with the flat equivalent. Understand the translation both ways.'),
                ('28&ndash;32', 'The cascade: inheritance, specificity, location', 'MEMORIZE',
                 'The highest-value block in Part 1. Slide 31 gives the a-b-c-d specificity algorithm &mdash; learn to compute it.'),
                ('33&ndash;36', 'Block vs inline elements', 'MEMORIZE',
                 'Two block elements cannot share a line without styling. Inline elements flow within lines and wrap.'),
                ('37&ndash;42', 'Margins, padding, the box model, dimensions, overflow', 'WRITE',
                 'Learn the four-value / two-value / one-value shorthand rules and how total element size is calculated.'),
                ('43&ndash;50', 'Text and font properties, web font stacks, @import, rem', 'WRITE',
                 'A font stack exists because your font may not be on the user&rsquo;s machine. <code>rem</code> is relative to the root element.'),
                ('51&ndash;53', 'CSS variables / custom properties', 'WRITE',
                 'Declared in <code>:root</code>, named with <code>--</code>, read with <code>var()</code>. Almost certain to appear in a lab.'),
                ('54&ndash;57', 'Styling tables: borders, border-collapse, zebra striping', 'WRITE',
                 'Borders can go on <code>table</code>, <code>th</code> and <code>td</code> only &mdash; <em>not</em> on <code>tr</code>, <code>thead</code>, <code>tbody</code>, <code>tfoot</code>. That exact fact is examinable.'),
                ('58&ndash;60', 'Styling forms, placeholders, labels, form design', 'WRITE',
                 'Ties chapter 2 forms to CSS. <code>::placeholder</code> is the pseudo-element to remember.'),
                ('61&ndash;62', 'Part 2 title and objectives', 'SKIM', 'Transition slides.'),
                ('63&ndash;67', 'Flexbox: containers and items', 'WRITE',
                 '<strong>Screenshot slides.</strong> The property tables are images. Use the reconstruction below.'),
                ('68&ndash;77', 'Grid: structure, column widths, placement, cells, nesting, named areas', 'WRITE',
                 '<strong>Mostly screenshots too</strong>, except the named-areas listing on slide 76. Highest-value practical block in the chapter.'),
                ('78', 'Grid and flexbox together', 'MEMORIZE',
                 'One sentence that answers the "which do I use" question: grid for the page structure, flexbox for the contents of a cell.'),
                ('79&ndash;84', 'Responsive design, viewports, media queries, &lt;picture&gt;', 'WRITE',
                 'Memorize the viewport meta tag verbatim. Know why <code>max-width:100%</code> is not enough on its own.'),
                ('85', 'Supporting material and links', 'SKIM',
                 'The code repository for every chapter: <code>github.com/skanderturki/se371</code>.'),
            ])
        },
        {
            'id': 'selectors', 'nav': 'Selectors', 'label': 'Slides 4&ndash;27',
            'title': 'Syntax and every selector type',
            'html': """
<h3>The vocabulary, precisely</h3>
""" + code('anatomy.css', """
<span class="c">/*  ── one RULE ──────────────────────────────── */</span>
<span class="t">h1, h2</span> {                    <span class="c">← SELECTOR  (comma groups several)</span>
    <span class="k">color</span>: <span class="s">#431c5d</span>;         <span class="c">← DECLARATION: property : value</span>
    <span class="k">font-size</span>: <span class="s">24pt</span>;        <span class="c">← another declaration</span>
}                            <span class="c">← the { } is the DECLARATION BLOCK</span>

<span class="c">/*  A stylesheet is one or more rules.
    The unit of a value depends on the property: keywords, percentages,
    lengths, unitless numbers, colour values and URLs are all possible.  */</span>
""", note='Slides 4–5') + """

<h3>Colour: five ways to say red</h3>
""" + table(['Method', 'Description', 'Example'], [
                ('<strong>Name</strong>', '17 standard names; CSS3 has 140.', '<code>color: red;</code> &middot; <code>color: hotpink;</code> <em>(CSS3)</em>'),
                ('<strong>RGB</strong>', 'Three numbers 0&ndash;255 for red, green and blue.', '<code>color: rgb(255,0,0);</code>'),
                ('<strong>Hexadecimal</strong>', 'A six-digit hex number for the same three values.', '<code>color: #FF0000;</code>'),
                ('<strong>RGBa</strong>', 'Adds alpha &mdash; transparency.', '<code>color: rgba(255,0,0,0.5);</code>'),
                ('<strong>HSL / HSLA</strong>', 'Hue, saturation, lightness. CSS3 only.', '<code>color: hsl(0,100%,100%);</code>'),
            ]) + """

<h3>Units</h3>
<p>Units are either <strong>relative</strong> (based on the value of something else) or
<strong>absolute</strong> (a real-world size).</p>
""" + table(['Unit', 'Kind', 'Meaning'], [
                ('<code>px</code>', 'Relative in CSS2, <strong>absolute</strong> in CSS3', '1/96 of an inch, so roughly 1.06&nbsp;mm.'),
                ('<code>em</code>', 'Relative', 'The computed <code>font-size</code> of the element it is used on. <code>2em</code> = twice the current font size.'),
                ('<code>rem</code>', 'Relative', 'Always relative to the root <code>&lt;html&gt;</code> element &mdash; introduced because nested <code>em</code>s become impossible to calculate.'),
                ('<code>vw</code>', 'Relative', '1% of the viewport width. If the viewport is 30&nbsp;cm wide, <code>1vw</code> = 0.3&nbsp;cm.'),
                ('<code>in</code>, <code>cm</code>', 'Absolute', 'Real-world inches and centimetres.'),
            ]) + """

<h3>Where styles live &mdash; three locations, not mutually exclusive</h3>
""" + code('the three locations', """
<span class="c">&lt;!-- 1. INLINE — style attribute. Affects only this element.
        Overrides other definitions for the properties it sets. --&gt;</span>
<span class="k">&lt;h2</span> <span class="t">style</span>=<span class="s">"font-size: 24pt; font-weight: bold;"</span><span class="k">&gt;</span>Reviews<span class="k">&lt;/h2&gt;</span>

<span class="c">&lt;!-- 2. EMBEDDED (internal) — a &lt;style&gt; element in the &lt;head&gt;.
        Better than inline, but still discouraged. --&gt;</span>
<span class="k">&lt;head&gt;</span>
  <span class="k">&lt;style&gt;</span>
    <span class="t">h1</span> { <span class="k">font-size</span>: <span class="s">24pt</span>; }
    <span class="t">h2</span> { <span class="k">font-size</span>: <span class="s">18pt</span>; <span class="k">font-weight</span>: <span class="s">bold</span>; }
  <span class="k">&lt;/style&gt;</span>
<span class="k">&lt;/head&gt;</span>

<span class="c">&lt;!-- 3. EXTERNAL — a .css file. THE ONE TO USE.
        • change it once, every page that links it updates
        • the browser can CACHE it, which improves performance --&gt;</span>
<span class="k">&lt;head&gt;</span>
  <span class="k">&lt;link</span> <span class="t">rel</span>=<span class="s">"stylesheet"</span> <span class="t">href</span>=<span class="s">"styles.css"</span><span class="k">&gt;</span>
<span class="k">&lt;/head&gt;</span>
""", note='Slides 8–11', run='inline-external-embed-829ff562') + """

<h3>Basic selectors</h3>
""" + code('selectors.css', """
<span class="c">/* ELEMENT — every instance of the element */</span>
<span class="t">p</span> { <span class="k">margin</span>: <span class="s">0</span>; }

<span class="c">/* UNIVERSAL — every element */</span>
<span class="t">*</span> { <span class="k">box-sizing</span>: <span class="s">border-box</span>; }

<span class="c">/* GROUPED — commas. These two are exactly equivalent: */</span>
<span class="t">p, div, aside</span> { <span class="k">margin</span>: <span class="s">0</span>; <span class="k">padding</span>: <span class="s">0</span>; }
<span class="c">/*   ≡  p{margin:0;padding:0} div{...} aside{...}  */</span>

<span class="c">/* CLASS — a period. Targets MANY elements. */</span>
<span class="t">.orange</span> { <span class="k">background-color</span>: <span class="s">orange</span>; }
<span class="t">.circle</span> { <span class="k">border-radius</span>: <span class="s">50%</span>; }

<span class="c">/* ID — a hash. UNIQUE: one element per document. */</span>
<span class="t">#first</span> { <span class="k">border</span>: <span class="s">2px solid black</span>; }
""", note='Slides 12–15', run='class-and-id-style-7197e8c4') + """
<p>An element may carry several classes &mdash; <code>&lt;div class="orange circle"&gt;</code> &mdash;
and where two of its classes set the same property, priority goes to whichever rule appears
<strong>last in the document</strong>. That is the location principle, arriving early.</p>

<h3>Attribute selectors &mdash; all six operators</h3>
""" + code('attribute-selectors.css', """
<span class="t">[title]</span>                          <span class="c">/* has the attribute at all                        */</span>
<span class="t">a[title="posts from this country"]</span>  <span class="c">/* exact value                                     */</span>
<span class="t">[title~="Countries City"]</span>         <span class="c">/* value contains this WORD in a space-separated list */</span>
<span class="t">a[href^="mailto"]</span>                <span class="c">/* value BEGINS with  (^ = start, like regex)      */</span>
<span class="t">img[src*="flag"]</span>                 <span class="c">/* value CONTAINS the substring anywhere           */</span>
<span class="t">a[href$=".pdf"]</span>                  <span class="c">/* value ENDS with    ($ = end, like regex)        */</span>

<span class="c">/* The slide's own example: mark PDF links with an icon */</span>
<span class="t">a[href$=".pdf"]</span> {
    <span class="k">background</span>: <span class="s">url(pdf.jpg) no-repeat left center</span>;
    <span class="k">padding-left</span>: <span class="s">20px</span>;
}
""", note='Slides 16–18', run='class-and-id-style-7197e8c4') + hook(
                "<strong>Remember the three symbol operators through regex:</strong> <code>^</code> is "
                "&ldquo;starts with&rdquo; and <code>$</code> is &ldquo;ends with&rdquo; in regular "
                "expressions too (chapter 5), and <code>*</code> is the greedy one &mdash; anywhere at "
                "all. Only <code>~=</code> is CSS-specific: a whole <em>word</em> in a space-separated list.") + """

<h3>Pseudo-classes and pseudo-elements</h3>
<p>A <strong>pseudo-element</strong> selects something that does not exist as an element in the
document tree &mdash; the first line or first letter of a block. A <strong>pseudo-class</strong>
targets a state or a family relationship.</p>
""" + code('pseudo.css', """
<span class="c">/* LINK STATES — write them in this order or later ones stop working */</span>
<span class="t">a:link</span>    { <span class="k">color</span>: <span class="s">#0000EE</span>; }   <span class="c">/* not yet visited            */</span>
<span class="t">a:visited</span> { <span class="k">color</span>: <span class="s">#551A8B</span>; }   <span class="c">/* already visited            */</span>
<span class="t">a:hover</span>   { <span class="k">color</span>: <span class="s">#b829ea</span>; }   <span class="c">/* pointer is currently above */</span>
<span class="t">a:active</span>  { <span class="k">color</span>: <span class="s">red</span>; }       <span class="c">/* being activated / clicked  */</span>

<span class="c">/* FAMILY + TEXT */</span>
<span class="t">li:first-child</span>   { <span class="k">font-weight</span>: <span class="s">bold</span>; }  <span class="c">/* first child of its parent */</span>
<span class="t">li:last-child</span>    { <span class="k">color</span>: <span class="s">red</span>; }           <span class="c">/* ← the slide 23 task       */</span>
<span class="t">p::first-letter</span>  { <span class="k">font-size</span>: <span class="s">3em</span>; }       <span class="c">/* pseudo-ELEMENT: ::        */</span>
<span class="t">p::first-line</span>    { <span class="k">font-variant</span>: <span class="s">small-caps</span>; }

<span class="c">/* :is() takes a selector LIST — far shorter than repeating :hover */</span>
<span class="t">:is(input, label, button, select):hover</span> { <span class="k">outline</span>: <span class="s">2px solid #b829ea</span>; }
<span class="c">/*   instead of  input:hover, label:hover, button:hover, select:hover  */</span>

<span class="c">/* The other half of the slide 23 task */</span>
<span class="t">a[href*="example"]</span> { <span class="k">color</span>: <span class="s">red</span>; }
""", note='Slides 19–23', run='pseudocode-ab37dddc') + """

<h3>Contextual selectors (combinators)</h3>
""" + code('combinators.css', """
<span class="c">/* Given this markup:
   &lt;section&gt;
     &lt;h2&gt;Title&lt;/h2&gt;
     &lt;p&gt;One&lt;/p&gt;
     &lt;div&gt;&lt;p&gt;Nested&lt;/p&gt;&lt;/div&gt;
     &lt;p&gt;Two&lt;/p&gt;
   &lt;/section&gt;                                                    */</span>

<span class="t">section p</span>    { }   <span class="c">/* DESCENDANT, a SPACE. Matches One, Nested AND Two —</span>
<span class="c">                       every p contained anywhere inside section.       */</span>

<span class="t">section &gt; p</span>  { }   <span class="c">/* CHILD, a &gt;. Matches One and Two only —</span>
<span class="c">                       Nested is a child of div, not of section.        */</span>

<span class="t">h2 + p</span>       { }   <span class="c">/* ADJACENT, a +. Matches One only —</span>
<span class="c">                       the NEXT SIBLING immediately after h2.           */</span>

<span class="t">h2 ~ p</span>       { }   <span class="c">/* GENERAL SIBLING, a ~. Matches One and Two —</span>
<span class="c">                       ALL following siblings sharing the same parent.  */</span>
""", note='Slides 25–26') + hook(
                "<strong>Four combinators, four questions:</strong> space = <em>anywhere inside?</em> "
                "&middot; <code>&gt;</code> = <em>directly inside?</em> &middot; <code>+</code> = "
                "<em>immediately after?</em> &middot; <code>~</code> = <em>anywhere after, same "
                "parent?</em>") + """

<h3>Nested rules (new)</h3>
""" + code('nesting.css', """
<span class="c">/* NESTED — implemented by all major browsers, still a W3C draft */</span>
<span class="t">.card</span> {
    <span class="k">padding</span>: <span class="s">1rem</span>;
    <span class="t">&amp; h2</span>   { <span class="k">margin</span>: <span class="s">0</span>; }
    <span class="t">&amp; p</span>    { <span class="k">color</span>: <span class="s">gray</span>; }
    <span class="t">&amp;:hover</span> { <span class="k">border-color</span>: <span class="s">#b829ea</span>; }
}

<span class="c">/* ── is exactly equivalent to ── */</span>
<span class="t">.card</span>       { <span class="k">padding</span>: <span class="s">1rem</span>; }
<span class="t">.card h2</span>    { <span class="k">margin</span>: <span class="s">0</span>; }
<span class="t">.card p</span>     { <span class="k">color</span>: <span class="s">gray</span>; }
<span class="t">.card:hover</span> { <span class="k">border-color</span>: <span class="s">#b829ea</span>; }
""", note='Slide 27')
        },
        {
            'id': 'cascade', 'nav': 'Cascade', 'label': 'Slides 28&ndash;32',
            'title': 'The cascade — the most examinable idea in CSS',
            'html': """
<p>The cascade is how conflicting rules are resolved, and it applies three principles
<strong>in this order</strong>: inheritance, specificity, location.</p>

<h3>1. Inheritance</h3>
<p>Many CSS properties affect descendants as well as the element itself. The division is not arbitrary
and is worth learning as two lists:</p>
""" + table(['Inherited', 'Not inherited'], [
                ('<strong>Font</strong> properties &mdash; <code>font-family</code>, <code>font-size</code>, <code>font-weight</code>',
                 '<strong>Layout</strong> properties &mdash; <code>display</code>, <code>position</code>, <code>float</code>'),
                ('<strong>Color</strong> &mdash; <code>color</code>',
                 '<strong>Sizing</strong> &mdash; <code>width</code>, <code>height</code>'),
                ('<strong>List</strong> properties &mdash; <code>list-style-type</code>',
                 '<strong>Border</strong> properties'),
                ('<strong>Text</strong> properties &mdash; <code>text-align</code>, <code>line-height</code>',
                 '<strong>Background</strong> and <strong>spacing</strong> &mdash; <code>margin</code>, <code>padding</code>'),
            ]) + code('inherit.css', """
<span class="c">/* You can FORCE inheritance of a property that normally does not inherit */</span>
<span class="t">button</span> { <span class="k">color</span>: <span class="s">inherit</span>; <span class="k">font-family</span>: <span class="s">inherit</span>; }
<span class="c">/* ↑ the classic use: form controls do not inherit page fonts by default */</span>
""", note='Slide 29', run='inhertiexample-2ce8822d') + """

<h3>2. Specificity &mdash; and how to actually compute it</h3>
<p>The more specific selector wins: id beats class, class beats element. Slide 31 gives the simplified
algorithm as four counters, written as <code>abcd</code>:</p>
""" + code('specificity — compute it, do not guess', """
<span class="c">  a = is it an INLINE style?         (1 or 0)
  b = count the IDs                  (#)
  c = count the CLASSES + ATTRIBUTES + pseudo-classes   (. [ ] :)
  d = count the ELEMENTS             (tag names + pseudo-elements)

  Read a-b-c-d as one number, LEFT TO RIGHT. Higher wins.
  A single id beats any number of classes: 0-1-0-0 &gt; 0-0-9-9.</span>

<span class="c">─── worked examples ───────────────────────────────────────────</span>
<span class="t">p</span>                       <span class="c">a=0 b=0 c=0 d=1  →  0001</span>
<span class="t">.orange</span>                 <span class="c">a=0 b=0 c=1 d=0  →  0010</span>
<span class="t">div p</span>                   <span class="c">a=0 b=0 c=0 d=2  →  0002</span>
<span class="t">div p.intro</span>             <span class="c">a=0 b=0 c=1 d=2  →  0012</span>
<span class="t">#first</span>                  <span class="c">a=0 b=1 c=0 d=0  →  0100   ← beats all of the above</span>
<span class="t">#first p.intro:hover</span>    <span class="c">a=0 b=1 c=2 d=1  →  0121</span>
<span class="t">style="color:red"</span>       <span class="c">a=1 b=0 c=0 d=0  →  1000   ← beats everything</span>

<span class="c">Question style: "which colour is applied?" — compute abcd for each
rule that could match, take the largest. If TWO tie, go to location.</span>
""", note='Slide 31') + """

<h3>3. Location</h3>
<p>When inheritance and specificity cannot decide, location does: <strong>with equal specificity, the
later rule wins</strong>. Which is why an inline style overrides an embedded or external stylesheet,
and why the last of two competing classes on an element is the one that applies.</p>
""" + hook("<strong>Order of resolution, in three words:</strong> <em>inherit &rarr; specificity "
           "&rarr; location.</em> Ask them in that order and you can answer any &ldquo;which rule "
           "wins&rdquo; question mechanically instead of by intuition.")
        },
        {
            'id': 'box', 'nav': 'Box Model', 'label': 'Slides 33&ndash;60',
            'title': 'Box model, text, variables, tables and forms',
            'html': """
<h3>Block vs inline</h3>
""" + table(['Block-level', 'Inline'], [
                ('<code>&lt;p&gt;</code> <code>&lt;div&gt;</code> <code>&lt;h2&gt;</code> <code>&lt;ul&gt;</code> <code>&lt;table&gt;</code>',
                 'normal text, <code>&lt;em&gt;</code> <code>&lt;a&gt;</code> <code>&lt;img&gt;</code> <code>&lt;span&gt;</code>'),
                ('Each sits on its own line. Without styling, two block elements cannot share a line.',
                 'Displayed within lines; does not form its own block.'),
                ('Uses the normal CSS box model, with <code>width</code> and <code>height</code>.',
                 'When there is not enough room on the line, content moves to a new line.'),
            ]) + """

<h3>The box model</h3>
""" + code('box model', """
<span class="c">   ┌─────────────────── MARGIN ──────────────────────┐  ← space AROUND the element
   │  ┌──────────────── BORDER ────────────────────┐ │     (divides margin from padding)
   │  │  ┌───────────── PADDING ─────────────────┐ │ │  ← space INSIDE the element
   │  │  │                                       │ │ │
   │  │  │             CONTENT                   │ │ │  ← width and height apply HERE ONLY
   │  │  │        (width × height)               │ │ │
   │  │  └───────────────────────────────────────┘ │ │
   │  └────────────────────────────────────────────┘ │
   └─────────────────────────────────────────────────┘

   TOTAL WIDTH = width + padding-left/right + border-left/right + margin-left/right
   ← this is why a 100%-wide box with padding overflows its parent.</span>

<span class="c">/* Shorthand: 4 values, 2 values, or 1 */</span>
<span class="t">.a</span> { <span class="k">border-color</span>: <span class="s">red green orange blue</span>; }  <span class="c">/* top right bottom left — clockwise */</span>
<span class="t">.b</span> { <span class="k">border-color</span>: <span class="s">red yellow</span>; }             <span class="c">/* top+bottom = red, right+left = yellow */</span>
<span class="t">.c</span> { <span class="k">border-color</span>: <span class="s">red</span>; }                     <span class="c">/* all four sides */</span>

<span class="c">/* Or set one side at a time */</span>
<span class="t">.d</span> { <span class="k">border-top-color</span>: <span class="s">red</span>; <span class="k">border-right-color</span>: <span class="s">green</span>;
     <span class="k">border-bottom-color</span>: <span class="s">yellow</span>; <span class="k">border-left-color</span>: <span class="s">blue</span>; }

<span class="c">/* The fix everybody uses: make width MEAN total width */</span>
<span class="t">*</span> { <span class="k">box-sizing</span>: <span class="s">border-box</span>; }
""", note='Slides 37–42', run='04-box-sizing-7dea49bb') + """
<p>Block-level elements also have <code>min-width</code>, <code>min-height</code>,
<code>max-width</code> and <code>max-height</code>, which matter when a width is expressed as a
percentage of the parent. And <code>overflow</code> controls what happens when the box is not large
enough for its content: <code>visible</code> (default), <code>hidden</code>, <code>scroll</code>,
<code>auto</code>.</p>

<h3>Text and fonts</h3>
""" + code('text.css', """
<span class="c">/* A WEB FONT STACK: fallbacks, because your font may not be installed
   on the user's computer. Always end with a generic family. */</span>
<span class="t">body</span> {
    <span class="k">font-family</span>: <span class="s">'Roboto Slab', Georgia, 'Times New Roman', serif</span>;
    <span class="k">font-size</span>: <span class="s">1rem</span>;        <span class="c">/* rem = relative to the ROOT html element */</span>
    <span class="k">font-weight</span>: <span class="s">400</span>;        <span class="c">/* 100–900, or normal / bold */</span>
    <span class="k">font-style</span>: <span class="s">normal</span>;      <span class="c">/* normal | italic | oblique */</span>
    <span class="k">line-height</span>: <span class="s">1.7</span>;
    <span class="k">text-align</span>: <span class="s">left</span>;
    <span class="k">text-decoration</span>: <span class="s">none</span>;
    <span class="k">text-transform</span>: <span class="s">uppercase</span>;
    <span class="k">letter-spacing</span>: <span class="s">0.05em</span>;
}

<span class="c">/* Using a font that is NOT installed anywhere — two ways */</span>
<span class="c">/* 1. a link in &lt;head&gt;:
      &lt;link href="https://fonts.googleapis.com/css?family=Droid+Sans" rel="stylesheet"&gt;   */</span>
<span class="c">/* 2. an @import at the TOP of a CSS file: */</span>
<span class="k">@import</span> <span class="s">url('https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@400&amp;display=swap')</span>;
""", note='Slides 43–50') + """

<h3>CSS variables (custom properties)</h3>
<p>Slide 52 shows a stylesheet where <code>#431c5d</code>, <code>4px</code>, <code>5px</code>,
<code>18px</code> and one long <code>box-shadow</code> are each repeated several times. Slide 53
rewrites it. This is the pattern to reproduce in labs.</p>
""" + code('variables.css', """
<span class="c">/* Declare in :root — names MUST begin with a double hyphen */</span>
<span class="t">:root</span> {
    <span class="k">--bg-color-main</span>: <span class="s">#431c5d</span>;
    <span class="k">--bg-color-secondary</span>: <span class="s">#e05915</span>;
    <span class="k">--fg-color-main</span>: <span class="s">#e6e9f0</span>;
    <span class="k">--radius-boxes</span>: <span class="s">5px</span>;
    <span class="k">--padding-boxes</span>: <span class="s">4px</span>;
    <span class="k">--fontsize-default</span>: <span class="s">18px</span>;
    <span class="k">--shadow-color</span>: <span class="s">rgba(0,0,0,0.22)</span>;
    <span class="k">--dropshadow</span>: <span class="s">6px 5px 20px 1px var(--shadow-color)</span>;  <span class="c">/* variables can use variables */</span>
}

<span class="c">/* Read with the var() function */</span>
<span class="t">header</span> {
    <span class="k">background-color</span>: <span class="s">var(--bg-color-main)</span>;
    <span class="k">color</span>: <span class="s">var(--bg-color-secondary)</span>;
    <span class="k">padding</span>: <span class="s">var(--padding-boxes)</span>;
    <span class="k">box-shadow</span>: <span class="s">var(--dropshadow)</span>;
    <span class="k">margin</span>: <span class="s">0</span>;
}
<span class="t">header button</span> {
    <span class="k">background-color</span>: <span class="s">var(--bg-color-secondary)</span>;
    <span class="k">border-radius</span>: <span class="s">var(--radius-boxes)</span>;
    <span class="k">border-color</span>: <span class="s">var(--fg-color-main)</span>;
    <span class="k">font-size</span>: <span class="s">var(--fontsize-default)</span>;
    <span class="k">margin-top</span>: <span class="s">calc(var(--fontsize-default) / 2)</span>;   <span class="c">/* note: var() INSIDE calc() */</span>
}
""", note='Slides 51–53') + """

<h3>Styling tables</h3>
""" + code('tables.css', """
<span class="c">/* WHERE BORDERS CAN GO — an examinable fact:
   ✓ table, th, td
   ✗ tr, thead, tbody, tfoot   ← borders CANNOT be assigned to these */</span>

<span class="t">table</span> {
    <span class="k">border-collapse</span>: <span class="s">collapse</span>;   <span class="c">/* adjacent cells SHARE one border      */</span>
    <span class="c">/* border-collapse: separate;  ← the DEFAULT: each cell has its own */</span>
    <span class="k">width</span>: <span class="s">100%</span>;
}
<span class="t">th, td</span> { <span class="k">border</span>: <span class="s">1px solid #ccc</span>; <span class="k">padding</span>: <span class="s">0.6rem</span>; <span class="k">text-align</span>: <span class="s">left</span>; }

<span class="c">/* ZEBRA STRIPING with the nth-child pseudo-class */</span>
<span class="t">tbody tr:nth-child(even)</span> { <span class="k">background-color</span>: <span class="s">#f4f0fa</span>; }

<span class="c">/* ROW HIGHLIGHT on hover */</span>
<span class="t">tbody tr:hover</span> { <span class="k">background-color</span>: <span class="s">#e6d8f5</span>; }
""", note='Slides 54–57', run='tablescss-step3-6f72b48f') + """

<h3>Styling forms</h3>
""" + code('forms.css', """
<span class="c">/* The common change described on slide 58: drop the border,
   round the corners, add padding. */</span>
<span class="t">input[type="text"], input[type="email"], textarea</span> {
    <span class="k">border</span>: <span class="s">none</span>;
    <span class="k">border-bottom</span>: <span class="s">2px solid #ccc</span>;
    <span class="k">border-radius</span>: <span class="s">8px</span>;
    <span class="k">padding</span>: <span class="s">0.6rem 0.8rem</span>;
    <span class="k">font</span>: <span class="s">inherit</span>;              <span class="c">/* controls do NOT inherit fonts by default */</span>
}

<span class="t">input:focus</span> { <span class="k">outline</span>: <span class="s">2px solid #b829ea</span>; }

<span class="c">/* ::placeholder — the pseudo-element for the placeholder text */</span>
<span class="t">input::placeholder</span> { <span class="k">color</span>: <span class="s">#948da3</span>; <span class="k">font-style</span>: <span class="s">italic</span>; }

<span class="c">/* Labels on their own line, with a click target */</span>
<span class="t">label</span> { <span class="k">display</span>: <span class="s">block</span>; <span class="k">margin-bottom</span>: <span class="s">0.3rem</span>; <span class="k">font-weight</span>: <span class="s">600</span>; }
""", note='Slides 58–60')
        },
        {
            'id': 'layout', 'nav': 'Flexbox &amp; Grid', 'label': 'Slides 61&ndash;78',
            'title': 'Layout — the screenshot slides, reconstructed',
            'html': """
<p>Slide 63 opens with a rule: tables were once used for page layout and <strong>this should never be
done</strong> &mdash; it pollutes the HTML, makes SEO harder and is not maintainable.</p>

<p>Everything below this point is what the slide images contained. Nothing here is in the slide text,
which is why this section is the one to work through with a browser open.</p>

<h3>Flexbox &mdash; for one-dimensional layouts</h3>
<p>Properties go in two places: on the <strong>flex container</strong> and on the <strong>flex
items</strong> inside it. Any direct child of a flex container automatically becomes a flex item.</p>
""" + code('flex-intro.html', """
<span class="k">&lt;style&gt;</span>
  <span class="t">.flex-container</span> {
      <span class="k">display</span>: <span class="s">flex</span>;                <span class="c">/* this ONE line creates the flex context */</span>
      <span class="k">background-color</span>: <span class="s">DodgerBlue</span>;
      <span class="k">flex-direction</span>: <span class="s">row</span>;           <span class="c">/* row | row-reverse | column | column-reverse */</span>
      <span class="k">flex-wrap</span>: <span class="s">wrap</span>;               <span class="c">/* wrap | nowrap (default) | wrap-reverse */</span>
  }
  <span class="t">.flex-container &gt; div</span> {           <span class="c">/* direct children ARE the flex items */</span>
      <span class="k">background-color</span>: <span class="s">#f1f1f1</span>;
      <span class="k">margin</span>: <span class="s">10px</span>;
      <span class="k">font-size</span>: <span class="s">30px</span>;
  }
<span class="k">&lt;/style&gt;</span>

<span class="k">&lt;div</span> <span class="t">class</span>=<span class="s">"flex-container"</span><span class="k">&gt;</span>
  <span class="k">&lt;div&gt;</span>1<span class="k">&lt;/div&gt;&lt;div&gt;</span>2<span class="k">&lt;/div&gt;&lt;div&gt;</span>3<span class="k">&lt;/div&gt;</span>
<span class="k">&lt;/div&gt;</span>
""", note='Slides 63–65 — the example the slide names', run='flex-intro-1dbbddb9') + """

<h4>Container properties &mdash; the table from slides 65&ndash;66</h4>
""" + table(['Property', 'Values', 'What it does'], [
                ('<code>display</code>', '<code>flex</code> &middot; <code>inline-flex</code>', 'Makes the element a flex container. Nothing else works without it.'),
                ('<code>flex-direction</code>', '<code>row</code> &middot; <code>row-reverse</code> &middot; <code>column</code> &middot; <code>column-reverse</code>', 'Sets the <strong>main axis</strong>. Everything else is described relative to it.'),
                ('<code>flex-wrap</code>', '<code>nowrap</code> (default) &middot; <code>wrap</code> &middot; <code>wrap-reverse</code>', 'Whether items may overflow onto more lines.'),
                ('<code>flex-flow</code>', '<code>row wrap</code>', 'Shorthand for direction + wrap.'),
                ('<code>justify-content</code>', '<code>flex-start</code> &middot; <code>flex-end</code> &middot; <code>center</code> &middot; <code>space-between</code> &middot; <code>space-around</code> &middot; <code>space-evenly</code>', 'Aligns items <strong>along the main axis</strong>.'),
                ('<code>align-items</code>', '<code>stretch</code> (default) &middot; <code>flex-start</code> &middot; <code>flex-end</code> &middot; <code>center</code> &middot; <code>baseline</code>', 'Aligns items <strong>across the cross axis</strong>.'),
                ('<code>align-content</code>', 'Same values as <code>justify-content</code>', 'Aligns the <strong>lines</strong> when content has wrapped. No effect on a single line.'),
                ('<code>gap</code>', 'A length', 'Space between items, without margin arithmetic.'),
            ]) + """
<h4>Item properties &mdash; slide 67</h4>
""" + table(['Property', 'Default', 'What it does'], [
                ('<code>order</code>', '<code>0</code>', 'Reorders items visually without touching the HTML. Lower first.'),
                ('<code>flex-grow</code>', '<code>0</code>', 'Share of the <em>leftover</em> space this item takes. This is the fraction the slide mentions: grow 2 takes twice as much extra space as grow 1.'),
                ('<code>flex-shrink</code>', '<code>1</code>', 'How readily the item shrinks when there is not enough room. <code>0</code> = never shrink.'),
                ('<code>flex-basis</code>', '<code>auto</code>', 'The item&rsquo;s size <em>before</em> growing or shrinking &mdash; its starting width on a row.'),
                ('<code>flex</code>', '<code>0 1 auto</code>', 'Shorthand for grow / shrink / basis. <code>flex: 1</code> is the everyday one.'),
                ('<code>align-self</code>', '<code>auto</code>', 'Overrides the container&rsquo;s <code>align-items</code> for this item alone.'),
            ]) + code('flex-basis.html', """
<span class="t">.flex-container</span> { <span class="k">display</span>: <span class="s">flex</span>; }

<span class="c">/* Give each child a FRACTION of the container — the slide 67 note */</span>
<span class="t">.item-a</span> { <span class="k">flex</span>: <span class="s">1</span>; }   <span class="c">/* 1 share  → 1/6 of the free space */</span>
<span class="t">.item-b</span> { <span class="k">flex</span>: <span class="s">2</span>; }   <span class="c">/* 2 shares → 2/6                    */</span>
<span class="t">.item-c</span> { <span class="k">flex</span>: <span class="s">3</span>; }   <span class="c">/* 3 shares → 3/6                    */</span>

<span class="c">/* Longhand equivalent of flex: 2 */</span>
<span class="t">.item-b</span> { <span class="k">flex-grow</span>: <span class="s">2</span>; <span class="k">flex-shrink</span>: <span class="s">1</span>; <span class="k">flex-basis</span>: <span class="s">0%</span>; }

<span class="c">/* The centring everyone memorises: dead centre, both axes */</span>
<span class="t">.centre</span> { <span class="k">display</span>: <span class="s">flex</span>; <span class="k">justify-content</span>: <span class="s">center</span>; <span class="k">align-items</span>: <span class="s">center</span>; }
""", note='Slide 67', run='flex-basis-40129d97') + hook(
                "<strong>The one confusion to settle now:</strong> <code>justify-content</code> works "
                "along the <em>main</em> axis, <code>align-items</code> across the <em>cross</em> axis. "
                "With <code>flex-direction: row</code> that means justify = horizontal, align = "
                "vertical &mdash; but switch to <code>column</code> and <strong>they swap</strong>. "
                "Learn them as main/cross, never as horizontal/vertical.") + """

<h3>Grid &mdash; for two-dimensional layouts</h3>
<p>Every block-level child of a container with <code>display: grid</code> is automatically placed into
a grid cell.</p>
""" + code('grid-structure.css', """
<span class="t">.container</span> {
    <span class="k">display</span>: <span class="s">grid</span>;

    <span class="c">/* COLUMNS — the fr unit is a FRACTION of the free space */</span>
    <span class="k">grid-template-columns</span>: <span class="s">1fr 1fr 1fr</span>;        <span class="c">/* three equal columns   */</span>
    <span class="k">grid-template-columns</span>: <span class="s">200px 1fr 1fr</span>;      <span class="c">/* fixed + two flexible  */</span>
    <span class="k">grid-template-columns</span>: <span class="s">repeat(3, 1fr)</span>;     <span class="c">/* repeat() — same thing */</span>
    <span class="k">grid-template-columns</span>: <span class="s">repeat(auto-fit, minmax(240px, 1fr))</span>;
    <span class="c">/*   ↑ responsive with NO media query: as many 240px-min columns as fit  */</span>

    <span class="c">/* ROWS work identically */</span>
    <span class="k">grid-template-rows</span>: <span class="s">100px 150px 100px</span>;

    <span class="k">gap</span>: <span class="s">10px</span>;                <span class="c">/* or row-gap / column-gap / grid-gap */</span>
}
""", note='Slides 68–71') + code('grid-placement.css', """
<span class="c">/* EXPLICIT PLACEMENT — count grid LINES, not cells.
   3 columns means 4 vertical lines: 1 2 3 4                       */</span>

<span class="t">.header</span> { <span class="k">grid-column</span>: <span class="s">1 / 4</span>; }        <span class="c">/* from line 1 to line 4 = all 3 columns */</span>
<span class="t">.header</span> { <span class="k">grid-column</span>: <span class="s">1 / span 3</span>; }   <span class="c">/* identical, written as a span         */</span>
<span class="t">.header</span> { <span class="k">grid-column</span>: <span class="s">1 / -1</span>; }       <span class="c">/* identical: -1 is the LAST line       */</span>

<span class="t">.sidebar</span> { <span class="k">grid-row</span>: <span class="s">2 / 4</span>; }          <span class="c">/* two rows tall                        */</span>

<span class="c">/* CELL ALIGNMENT — slide 74.
   *-items on the CONTAINER sets the default for every cell;
   *-self  on an ITEM overrides it for that one cell.             */</span>
<span class="t">.container</span> { <span class="k">justify-items</span>: <span class="s">center</span>; <span class="k">align-items</span>: <span class="s">center</span>; }
<span class="t">.blue</span>      { <span class="k">justify-self</span>: <span class="s">start</span>;  <span class="k">align-self</span>: <span class="s">end</span>; }
<span class="c">/*   justify = horizontal (along the row), align = vertical (down the column) */</span>
""", note='Slides 72–74', run='grid-justify-cdbaf760') + """
<h4>Named areas &mdash; the full listing from slide 76</h4>
""" + code('grid-areas.html', """
<span class="k">&lt;style&gt;</span>
<span class="t">.container</span> {
    <span class="k">display</span>: <span class="s">grid</span>;
    <span class="k">grid-gap</span>: <span class="s">10px</span>;
    <span class="k">grid-template-rows</span>: <span class="s">100px 150px 100px</span>;
    <span class="k">grid-template-columns</span>: <span class="s">75px 1fr 1fr 1fr 1fr</span>;

    <span class="c">/* Each STRING is a row; each WORD is a column.
       A name repeated across adjacent cells makes one merged area.
       A dot ( . ) leaves that cell empty.                         */</span>
    <span class="k">grid-template-areas</span>: <span class="s">".  a1 a2 a3 a4"</span>
                         <span class="s">"b1 b2 b2 b2 b3"</span>     <span class="c">/* b2 spans 3 columns */</span>
                         <span class="s">"b1 c1 c2 c2 c2"</span>;    <span class="c">/* b1 spans 2 rows    */</span>
}
<span class="t">.a1</span> { <span class="k">grid-area</span>: <span class="s">a1</span>; }   <span class="t">.b1</span> { <span class="k">grid-area</span>: <span class="s">b1</span>; }   <span class="t">.c1</span> { <span class="k">grid-area</span>: <span class="s">c1</span>; }
<span class="t">.a2</span> { <span class="k">grid-area</span>: <span class="s">a2</span>; }   <span class="t">.b2</span> { <span class="k">grid-area</span>: <span class="s">b2</span>; }   <span class="t">.c2</span> { <span class="k">grid-area</span>: <span class="s">c2</span>; }
<span class="t">.a3</span> { <span class="k">grid-area</span>: <span class="s">a3</span>; }   <span class="t">.b3</span> { <span class="k">grid-area</span>: <span class="s">b3</span>; }
<span class="t">.a4</span> { <span class="k">grid-area</span>: <span class="s">a4</span>; }
<span class="k">&lt;/style&gt;</span>

<span class="k">&lt;section</span> <span class="t">class</span>=<span class="s">"container"</span><span class="k">&gt;</span>
  <span class="k">&lt;div</span> <span class="t">class</span>=<span class="s">"yellow a1"</span><span class="k">&gt;</span>A1<span class="k">&lt;/div&gt;</span>  <span class="k">&lt;div</span> <span class="t">class</span>=<span class="s">"yellow a2"</span><span class="k">&gt;</span>A2<span class="k">&lt;/div&gt;</span>
  <span class="k">&lt;div</span> <span class="t">class</span>=<span class="s">"yellow a3"</span><span class="k">&gt;</span>A3<span class="k">&lt;/div&gt;</span>  <span class="k">&lt;div</span> <span class="t">class</span>=<span class="s">"yellow a4"</span><span class="k">&gt;</span>A4<span class="k">&lt;/div&gt;</span>
  <span class="k">&lt;div</span> <span class="t">class</span>=<span class="s">"orange b1"</span><span class="k">&gt;</span>B1<span class="k">&lt;/div&gt;</span>  <span class="k">&lt;div</span> <span class="t">class</span>=<span class="s">"orange b2"</span><span class="k">&gt;</span>B2<span class="k">&lt;/div&gt;</span>
  <span class="k">&lt;div</span> <span class="t">class</span>=<span class="s">"orange b3"</span><span class="k">&gt;</span>B3<span class="k">&lt;/div&gt;</span>  <span class="k">&lt;div</span> <span class="t">class</span>=<span class="s">"cyan c1"</span><span class="k">&gt;</span>C1<span class="k">&lt;/div&gt;</span>
  <span class="k">&lt;div</span> <span class="t">class</span>=<span class="s">"cyan c2"</span><span class="k">&gt;</span>C2<span class="k">&lt;/div&gt;</span>
<span class="k">&lt;/section&gt;</span>
""", note='Slides 76–77 — LISTING 7.2', run='nested-grid-example-79bf386e') + """

<h3>Grid and flexbox together &mdash; the decision rule</h3>
<div class="card">
  <p><strong>Grid builds the layout structure of the page. Flexbox lays out the contents of a grid
  cell.</strong> That single sentence from slide 78 answers the "which should I use" question in an
  exam, and it is also just good practice: grid is two-dimensional, flexbox is one-dimensional.</p>
</div>
""" + code('together.css', """
<span class="c">/* GRID for the page skeleton */</span>
<span class="t">.page</span> {
    <span class="k">display</span>: <span class="s">grid</span>;
    <span class="k">grid-template-columns</span>: <span class="s">240px 1fr</span>;
    <span class="k">grid-template-rows</span>: <span class="s">64px 1fr auto</span>;
    <span class="k">grid-template-areas</span>: <span class="s">"head head"</span>
                         <span class="s">"side main"</span>
                         <span class="s">"foot foot"</span>;
    <span class="k">min-height</span>: <span class="s">100vh</span>;
}

<span class="c">/* FLEXBOX inside one of those cells */</span>
<span class="t">.page &gt; header</span> {
    <span class="k">grid-area</span>: <span class="s">head</span>;
    <span class="k">display</span>: <span class="s">flex</span>;
    <span class="k">align-items</span>: <span class="s">center</span>;             <span class="c">/* vertical centring within the bar */</span>
    <span class="k">justify-content</span>: <span class="s">space-between</span>;  <span class="c">/* logo left, actions right         */</span>
    <span class="k">gap</span>: <span class="s">1rem</span>;
}
""", note='Slide 78', run='homepage-56c59859')
        },
        {
            'id': 'responsive', 'nav': 'Responsive', 'label': 'Slides 79&ndash;84',
            'title': 'Responsive design',
            'html': """
<p>In a responsive design the page <em>responds</em> to changes in browser size beyond simple
percentage scaling: smaller images are served, and navigation elements are replaced as the window
shrinks.</p>

<h3>The viewport &mdash; memorize this tag</h3>
""" + code('every page you write', """
<span class="k">&lt;meta</span> <span class="t">name</span>=<span class="s">"viewport"</span> <span class="t">content</span>=<span class="s">"width=device-width, initial-scale=1"</span><span class="k">&gt;</span>
<span class="c">                              ↑ size of the viewport   ↑ zoom level</span>

<span class="c">WHY: the viewport is the part of the browser window that shows web content.
Mobile browsers DEFAULT to scaling a whole desktop-width page down to fit the
screen. The result works, but is very difficult to read and use. This tag tells
the browser to use the device's real width instead — after which your media
queries actually fire.</span>
""", note='Slides 80–81') + """

<h3>Media queries</h3>
<p>A media query applies style rules based on the medium displaying the file. Contemporary responsive
sites give rules for phones first, then tablets, then desktops &mdash; an approach the slide names
<strong>progressive enhancement</strong>.</p>
""" + code('responsive.css', """
<span class="c">/* MOBILE FIRST: the base rules are the phone layout.
   No media query needed — this is the default. */</span>
<span class="t">.page</span> { <span class="k">display</span>: <span class="s">grid</span>; <span class="k">grid-template-columns</span>: <span class="s">1fr</span>; }
<span class="t">nav ul</span> { <span class="k">display</span>: <span class="s">none</span>; }          <span class="c">/* nav replaced by a menu button */</span>

<span class="c">/* TABLET and up */</span>
<span class="k">@media</span> <span class="s">(min-width: 600px)</span> {
    <span class="t">.page</span> { <span class="k">grid-template-columns</span>: <span class="s">200px 1fr</span>; }
    <span class="t">nav ul</span> { <span class="k">display</span>: <span class="s">flex</span>; <span class="k">gap</span>: <span class="s">1.5rem</span>; }
}

<span class="c">/* DESKTOP and up */</span>
<span class="k">@media</span> <span class="s">(min-width: 1024px)</span> {
    <span class="t">.page</span> { <span class="k">grid-template-columns</span>: <span class="s">240px 1fr 300px</span>; }
}

<span class="c">/* Other media types and features you can query */</span>
<span class="k">@media</span> <span class="s">print</span>                    { <span class="t">nav, footer</span> { <span class="k">display</span>: <span class="s">none</span>; } }
<span class="k">@media</span> <span class="s">(orientation: landscape)</span> { <span class="c">/* … */</span> }
<span class="k">@media</span> <span class="s">(prefers-color-scheme: dark)</span> { <span class="c">/* … */</span> }
""", note='Slides 82–83') + """

<h3>Images: scaling is not the same as downloading less</h3>
""" + code('picture.html', """
<span class="c">/* Making an image SCALE is one line — but the browser still downloads
   the full-size file. On a phone that is wasted bandwidth. */</span>
<span class="t">img</span> { <span class="k">max-width</span>: <span class="s">100%</span>; }

<span class="c">&lt;!-- &lt;picture&gt; (HTML5.1) lets you offer SEVERAL images and lets the
     browser choose which one to download, based on viewport size. --&gt;</span>
<span class="k">&lt;picture&gt;</span>
  <span class="k">&lt;source</span> <span class="t">media</span>=<span class="s">"(min-width: 1024px)"</span> <span class="t">srcset</span>=<span class="s">"banner-large.jpg"</span><span class="k">&gt;</span>
  <span class="k">&lt;source</span> <span class="t">media</span>=<span class="s">"(min-width: 600px)"</span>  <span class="t">srcset</span>=<span class="s">"banner-medium.jpg"</span><span class="k">&gt;</span>
  <span class="k">&lt;img</span> <span class="t">src</span>=<span class="s">"banner-small.jpg"</span> <span class="t">alt</span>=<span class="s">"Campus banner"</span><span class="k">&gt;</span>  <span class="c">&lt;!-- fallback, always last --&gt;</span>
<span class="k">&lt;/picture&gt;</span>
""", note='Slide 84') + hook(
                "<strong>The distinction slide 84 is testing:</strong> <code>max-width: 100%</code> "
                "changes how big the image <em>looks</em>. <code>&lt;picture&gt;</code> changes which "
                "file gets <em>downloaded</em>. Only the second one saves the user's data.")
        },
        {
            'id': 'traps', 'nav': 'Traps', 'label': 'Marks Lost Here',
            'title': 'The eight things people get wrong',
            'html': (
                trap('Guessing specificity instead of computing it',
                     'You assume the last rule wins, but a rule further up with an id in it is beating it. Location only applies <strong>after</strong> specificity ties.',
                     'Compute <code>a-b-c-d</code> for every competing rule and compare left to right. One id (0-1-0-0) beats nine classes (0-0-9-0).') +
                trap('A 100%-wide box that overflows its parent',
                     '<code>width: 100%</code> plus <code>padding: 1rem</code> plus a border is <em>wider</em> than the parent, because <code>width</code> sizes the content area only.',
                     'Either subtract the padding yourself, or set <code>box-sizing: border-box</code> so <code>width</code> means the full outside width. This is why almost every stylesheet starts with <code>* { box-sizing: border-box; }</code>.') +
                trap('Treating <code>justify-content</code> as "horizontal"',
                     'It is horizontal only while <code>flex-direction</code> is <code>row</code>. Switch the container to <code>column</code> and <code>justify-content</code> becomes vertical, so a layout that centred correctly suddenly does not.',
                     'Learn them as <strong>main axis</strong> (justify) and <strong>cross axis</strong> (align). The direction sets which is which.') +
                trap('Counting grid cells instead of grid lines',
                     '<code>grid-column: 1 / 3</code> spans <strong>two</strong> columns, not three, because those numbers are line numbers. Three columns are bounded by four lines.',
                     'Sketch the lines and number them, or avoid the arithmetic entirely with <code>span</code>: <code>grid-column: 1 / span 3</code>. And <code>-1</code> always means the last line.') +
                trap('Media queries that never fire on a phone',
                     'Your breakpoints work perfectly when you resize the desktop browser but do nothing on an actual phone. The viewport meta tag is missing, so the mobile browser is rendering at a fake desktop width and scaling the result down.',
                     'Put <code>&lt;meta name="viewport" content="width=device-width, initial-scale=1"&gt;</code> in the <code>&lt;head&gt;</code> of every page. Nothing responsive works reliably without it.') +
                trap('Putting a border on a <code>&lt;tr&gt;</code>',
                     'Nothing happens, and it looks like a CSS bug. Slide 54 states it directly: borders can be assigned to <code>&lt;table&gt;</code>, <code>&lt;th&gt;</code> and <code>&lt;td&gt;</code>, and <em>cannot</em> be assigned to <code>&lt;tr&gt;</code>, <code>&lt;thead&gt;</code>, <code>&lt;tfoot&gt;</code> or <code>&lt;tbody&gt;</code>.',
                     'Style the cells instead: <code>tr:hover td { ... }</code> or a <code>border-bottom</code> on every <code>td</code> in the row.') +
                trap('Link styles that stop working when you reorder them',
                     'Writing <code>a:hover</code> before <code>a:visited</code> means a visited link never shows its hover colour &mdash; both selectors have the same specificity, so the later one wins.',
                     'Keep the order <code>:link</code>, <code>:visited</code>, <code>:hover</code>, <code>:active</code>. It is a location problem wearing a costume.') +
                trap('Expecting form controls to inherit the page font',
                     'You set <code>font-family</code> on <code>body</code> and every input still renders in the browser&rsquo;s default. Font properties inherit, but form controls are a documented exception.',
                     'Add <code>input, select, textarea, button { font: inherit; }</code> &mdash; this is exactly the use case for the <code>inherit</code> keyword on slide 29.')
            )
        },
        {
            'id': 'cheat', 'nav': 'Cheat Sheet', 'label': 'One Screen',
            'title': 'Chapter 3 on a single screen',
            'html': cheat([
                ('Selector types', [
                    '<code>p</code> element &middot; <code>*</code> universal',
                    '<code>.class</code> many &middot; <code>#id</code> one',
                    '<code>p, div</code> group',
                    '<code>[attr]</code> <code>[a="v"]</code> <code>[a~="w"]</code>',
                    '<code>[a^=]</code> starts &middot; <code>[a*=]</code> contains &middot; <code>[a$=]</code> ends',
                ]),
                ('Combinators', [
                    '<code>a b</code> &mdash; descendant, anywhere inside',
                    '<code>a &gt; b</code> &mdash; direct child',
                    '<code>a + b</code> &mdash; next sibling',
                    '<code>a ~ b</code> &mdash; all following siblings',
                ]),
                ('Cascade order', [
                    '1. <strong>Inheritance</strong> &mdash; font/color/list/text yes; layout/size/border/background/spacing no',
                    '2. <strong>Specificity</strong> &mdash; <code>a</code>=inline <code>b</code>=id <code>c</code>=class/attr <code>d</code>=element',
                    '3. <strong>Location</strong> &mdash; later wins on a tie',
                ]),
                ('Box model', [
                    'content &rarr; padding &rarr; border &rarr; margin',
                    '<code>width</code> sizes the <em>content</em> only',
                    '4 values = top right bottom left',
                    '2 values = top/bottom, right/left',
                    '<code>box-sizing: border-box</code> fixes the maths',
                ]),
                ('Flex container', [
                    '<code>display: flex</code>',
                    '<code>flex-direction</code> row | column (+reverse)',
                    '<code>flex-wrap</code> nowrap | wrap',
                    '<code>justify-content</code> &mdash; main axis',
                    '<code>align-items</code> &mdash; cross axis',
                    '<code>gap</code>',
                ]),
                ('Flex item', [
                    '<code>flex: grow shrink basis</code> (<code>0 1 auto</code>)',
                    '<code>flex: 1</code> &mdash; equal share of free space',
                    '<code>order</code> &mdash; visual reordering',
                    '<code>align-self</code> &mdash; override for one item',
                ]),
                ('Grid', [
                    '<code>display: grid</code>',
                    '<code>grid-template-columns: 1fr 1fr</code>',
                    '<code>repeat(3, 1fr)</code> &middot; <code>minmax(240px, 1fr)</code>',
                    '<code>grid-column: 1 / 4</code> &mdash; LINE numbers',
                    '<code>1 / span 3</code> &middot; <code>1 / -1</code>',
                    '<code>grid-template-areas</code> + <code>grid-area</code>',
                ]),
                ('Responsive', [
                    '<code>&lt;meta name="viewport" content="width=device-width, initial-scale=1"&gt;</code>',
                    '<code>@media (min-width: 600px) { }</code>',
                    'Phone first, then tablet, then desktop',
                    '<code>img { max-width: 100% }</code> scales',
                    '<code>&lt;picture&gt;</code> downloads less',
                ]),
                ('Variables', [
                    'Declare in <code>:root</code>, names start <code>--</code>',
                    'Read with <code>var(--name)</code>',
                    'Variables may reference variables',
                    '<code>calc(var(--x) / 2)</code>',
                ]),
            ])
        },
        {
            'id': 'drills', 'nav': 'Drills', 'label': 'Type It Blind',
            'title': 'Build these, do not read about them',
            'html': """
<p>Layout is not learnable by reading, and this is the chapter where that bites hardest, because the
layout slides are pictures. Open a file, open the browser, and build.</p>
""" + drills([
                'Write the same rule three ways: inline, embedded and external. Then explain in one sentence why external wins.',
                'Write one selector for each of the six attribute operators, and say in words what each matches.',
                'Style a link&rsquo;s four states in the correct order, then deliberately reorder them and observe what breaks.',
                'Complete the slide 23 task: colour the last child of a <code>ul</code> red, and style every <code>&lt;a&gt;</code> whose <code>href</code> contains &ldquo;example&rdquo;.',
                'Given four rules that all match one element, compute <code>abcd</code> for each and predict the winner. Then check in DevTools &mdash; the Styles panel strikes through the losers.',
                'Build a box with an explicit width, padding and border. Measure the real rendered width in DevTools, then add <code>box-sizing: border-box</code> and measure again.',
                'Convert a stylesheet with five repeated values into CSS variables declared in <code>:root</code>.',
                'Style a table: collapsed borders, zebra striping with <code>nth-child</code>, and a hover highlight on rows.',
                'Build a flex row of five items, then use <code>flex: 1 / 2 / 3</code> to give three of them different shares of the free space.',
                'Centre a box perfectly in the viewport using three lines of flexbox.',
                'Take that same flex container, switch it to <code>column</code>, and predict what happens to <code>justify-content</code> before you reload.',
                'Build a three-column grid with <code>repeat(auto-fit, minmax(240px, 1fr))</code> and resize the window &mdash; a responsive layout with no media query.',
                'Reproduce the slide 76 named-areas layout exactly, then move one area by editing only the <code>grid-template-areas</code> strings.',
                'Build a page skeleton with grid and lay out its header with flexbox, following the slide 78 rule.',
                'Write a mobile-first stylesheet with breakpoints at 600px and 1024px, then delete the viewport meta tag and test it on a phone to see what happens.',
            ]) + """
<p>Worked examples for almost all of this already sit in your study material: the
<a href="/academics/software-engineering/se371/extra-resources/chapter-3/example-codes-css/" target="_blank" rel="noopener">CSS example folder</a>,
the <a href="/academics/software-engineering/se371/extra-resources/resource-viewers/css-layout-tutorial-handout-with-starter-and-exercises-507e502d/" target="_blank" rel="noopener">CSS layout handout with exercises</a>,
and the two solved CSS labs
(<a href="/academics/software-engineering/se371/extra-resources/resource-viewers/home-e140c164/" target="_blank" rel="noopener">lab 03a</a>,
<a href="/academics/software-engineering/se371/extra-resources/resource-viewers/home-e35bd0d8/" target="_blank" rel="noopener">lab 03b</a>).
Slide 85 also gives the repository for every chapter&rsquo;s code:
<code>github.com/skanderturki/se371</code>.</p>
"""
        },
    ],
    'quiz': [
        {'tag': 'Cascade', 'q': 'Two rules both set the colour of one element: #main p { color: blue } and .intro.highlight p { color: red }. Which wins?',
         'opts': ['Red — two classes outweigh one id', 'Blue — the id gives 0-1-0-1 against 0-0-2-1',
                  'Red — it appears later in the file', 'Neither — the conflict is ignored'],
         'a': 1,
         'why': 'Compare a-b-c-d left to right. The id rule scores 0-1-0-1 and the class rule 0-0-2-1. The b column decides it immediately: one id beats any number of classes, and location never gets consulted.'},
        {'tag': 'Box model', 'q': 'A div has width: 300px, padding: 20px and a 5px border. How wide is it on screen by default?',
         'opts': ['300px', '325px', '350px', '345px'],
         'a': 2,
         'why': 'width sizes the content area only, so add padding and border on both sides: 300 + 20 + 20 + 5 + 5 = 350px. Setting box-sizing: border-box makes 300px mean the total instead.'},
        {'tag': 'Flexbox', 'q': 'A flex container has flex-direction: column. What does justify-content: center now do?',
         'opts': ['Centres items horizontally', 'Centres items vertically',
                  'Has no effect in column direction', 'Centres the container itself'],
         'a': 1,
         'why': 'justify-content always works along the main axis, and flex-direction sets the main axis. In a column the main axis is vertical, so justify and align swap their apparent directions.'},
        {'tag': 'Grid', 'q': 'In a four-column grid, how many columns does grid-column: 2 / 4 span?',
         'opts': ['Four', 'Three', 'Two', 'One'],
         'a': 2,
         'why': 'Those are grid line numbers, not column numbers. Lines 2 to 4 enclose columns 2 and 3, so it spans two. Writing 2 / span 2 says the same thing without the arithmetic.'},
        {'tag': 'Tables', 'q': 'You add border: 1px solid black to a tr and nothing appears. Why?',
         'opts': ['border-collapse must be set to separate first',
                  'Borders cannot be assigned to tr, thead, tbody or tfoot',
                  'The border is hidden behind the cell backgrounds',
                  'tr needs display: block for borders to work'],
         'a': 1,
         'why': 'Slide 54 states it directly: borders can be assigned to table, th and td, and cannot be assigned to tr, thead, tfoot or tbody. Style the cells instead.'},
        {'tag': 'Selectors', 'q': 'Which selector matches every <a> whose href ends in .pdf?',
         'opts': ['<code>a[href*=".pdf"]</code>', '<code>a[href^=".pdf"]</code>',
                  '<code>a[href$=".pdf"]</code>', '<code>a[href~=".pdf"]</code>'],
         'a': 2,
         'why': '$= means "ends with", exactly as in a regular expression. *= would also match a link containing .pdf in the middle, and ^= matches the start.'},
        {'tag': 'Inheritance', 'q': 'Which group of properties is inherited by descendants?',
         'opts': ['Width, height and padding', 'Border, background and margin',
                  'Font, color, list and text properties', 'Display, position and float'],
         'a': 2,
         'why': 'Slide 29 divides them exactly this way: font, colour, list and text properties inherit; layout, sizing, border, background and spacing properties do not. The inherit keyword can force the others.'},
        {'tag': 'Responsive', 'q': 'Your media queries work when you resize the desktop browser but do nothing on a phone. What is missing?',
         'opts': ['A separate mobile stylesheet', 'The viewport meta tag',
                  'max-width: 100% on images', 'A @media print rule'],
         'a': 1,
         'why': 'Without <meta name="viewport" content="width=device-width, initial-scale=1"> a mobile browser renders at a fake desktop width and scales the page down, so the breakpoints never fire.'},
    ],
})


# ═══════════════════════════════════════════════════════════════════════════ #
# CHAPTER 04 — JavaScript: Language Fundamentals + Array Functions
# ═══════════════════════════════════════════════════════════════════════════ #

CHAPTERS.append({
    'num': 4,
    'slug': '04-javascript',
    'file': 'javascript.html',
    'title': 'JavaScript Fundamentals',
    'desc': ('Slide-by-slide breakdown of SE371 Chapter 4 — JavaScript types, truthiness, arrays, '
             'objects, JSON, functions, callbacks, hoisting, scope, arrow syntax and array methods.'),
    'sub': ('The turning point of the course. Everything from here to chapter 7 is JavaScript, so a '
            'gap left in this chapter reappears in the DOM, in Node, and in your database queries. '
            'The array-function slides at the end are the ones you will use every single week.'),
    'stats': ['64 slides', 'Two decks in one', 'Pure write-it', 'Book ch. 8 + 9'],
    'sections': [
        {
            'id': 'orient', 'nav': 'Start Here', 'label': 'Orientation',
            'title': 'What this chapter is really for',
            'html': """
<p>Split at slide 55: <strong>Part 1 (1&ndash;54)</strong> is the language, <strong>Part 2
(55&ndash;64)</strong> is the six array functions. Part 2 is short, dense, and used constantly &mdash;
do not let it get squeezed out by revision time.</p>

<p>Four properties of JavaScript are stated on slide 3 and they explain nearly every surprise in this
chapter:</p>
<ol>
  <li>It is an <strong>interpreted, object-oriented scripting language</strong>.</li>
  <li>It is <strong>primarily client-side</strong>. (Chapter 6 breaks this assumption with Node.)</li>
  <li><strong>Functions are objects too</strong> &mdash; unlike Java, C# or C++. This is what makes callbacks, <code>map</code>, <code>filter</code> and event handlers possible.</li>
  <li>It is <strong>dynamically (weakly) typed</strong>: variables convert implicitly between types. This is what makes <code>==</code> dangerous and truthiness a topic.</li>
</ol>

<div class="grid-2">
  <div class="card">
    <h4>Where the marks concentrate</h4>
    <p>Predict-the-output questions. Hoisting, truthiness, <code>var</code> vs <code>let</code> scope,
    <code>==</code> vs <code>===</code>, primitive vs reference copying, and what
    <code>sort()</code> does to numbers. Each is a small slide and a reliable question.</p>
  </div>
  <div class="card">
    <h4>Where it connects</h4>
    <p>Objects and JSON here become the data your fetch calls return in chapter 6 and your database
    documents in chapter 7. Callbacks here become event handlers in chapter 5 and asynchronous code
    in chapter 6. This chapter is the spine.</p>
  </div>
</div>
"""
        },
        {
            'id': 'map', 'nav': 'Slide Map', 'label': 'Navigation',
            'title': 'All 64 slides, weighted',
            'html': slidemap([
                ('1&ndash;3', 'Objectives; what JavaScript is', 'MEMORIZE',
                 'Four properties: interpreted and object-oriented, primarily client-side, functions are objects, dynamically typed.'),
                ('4&ndash;6', 'Client-side scripting advantages and disadvantages', 'MEMORIZE',
                 'Three advantages, four disadvantages. The sharpest one: JavaScript is <strong>not fault tolerant</strong> &mdash; browsers forgive bad HTML and CSS but stop at an invalid line of JS.'),
                ('7&ndash;9', 'Inline, embedded and external JavaScript; execution order', 'WRITE',
                 'External is recommended. Scripts run <em>in the order encountered on the page</em>, whether inline or external.'),
                ('10&ndash;12', 'Variables; alert/prompt/confirm; document.write/console.log', 'WRITE',
                 'Know all five output methods. Note the copy-paste warning about smart quotes &mdash; it is a real cause of lab errors.'),
                ('13&ndash;15', 'Primitive vs reference types; copying', 'MEMORIZE',
                 'Six primitives. Primitives hold the value; objects hold a reference. <code>structuredClone()</code> deep copies, <code>[...foo]</code> copies shallowly.'),
                ('16', 'let vs const', 'MEMORIZE',
                 'Screenshot slide &mdash; the comparison is reconstructed below.'),
                ('17', 'Built-in objects', 'MEMORIZE',
                 'Object, Function, Boolean, Error, Number, Math, Date, String, RegExp. Browser-only: document, console, navigator, window.'),
                ('18', 'Concatenation and template strings', 'WRITE',
                 'The console.log outputs on this slide are a predict-the-output question waiting to happen.'),
                ('19&ndash;21', 'Conditionals, switch, ternary, truthy and falsy', 'MEMORIZE',
                 'Learn the falsy list exactly &mdash; there are seven values and everything else is truthy.'),
                ('22&ndash;24', 'while, do…while, for, try…catch', 'WRITE',
                 'Standard, but write them once so the syntax is automatic.'),
                ('25&ndash;29', 'Arrays: literal and constructor, iteration, destructuring', 'WRITE',
                 'Slide 29 is a trick question about <code>length</code> &mdash; work out why before reading the answer.'),
                ('30&ndash;36', 'Objects: literal notation, constructor, nesting, destructuring', 'WRITE',
                 'JavaScript is <strong>prototype based</strong>: objects come from other objects, not from classes. Literal notation is preferred.'),
                ('37&ndash;38', 'JSON and the JSON object', 'MEMORIZE',
                 'The difference from object literals is exactly one thing: JSON property names are quoted. And JSON is a <em>string</em> until you parse it.'),
                ('39&ndash;43', 'Functions, expressions, default and rest parameters', 'WRITE',
                 'Declaration vs expression matters for hoisting on the next slide. <code>...args</code> is the rest operator.'),
                ('44', 'Hoisting', 'MEMORIZE',
                 'Declarations are hoisted; <strong>assignments are not</strong>. That second half is where the marks are.'),
                ('45&ndash;48', 'Callback functions; the map exercise', 'WRITE',
                 'Slide 46 is flagged on the slide itself as <em>very important &mdash; the basis of all functional programming</em>. Implement it.'),
                ('49&ndash;50', 'Objects with function properties; constructors as functions', 'WRITE',
                 'The <code>this</code> keyword. Without it, the properties are simply not defined inside the method.'),
                ('51', 'Arrow syntax', 'WRITE',
                 'Concise anonymous functions. One restriction stated on the slide: arrow functions cannot be used as constructors.'),
                ('52&ndash;54', 'Scope: function, block, module, global', 'MEMORIZE',
                 'The examinable contrast: <code>let</code>/<code>const</code> respect block scope, <code>var</code> does not.'),
                ('55&ndash;56', 'Part 2 title; the six array functions', 'MEMORIZE',
                 'One line each for forEach, find, filter, map, reduce, sort. Learn what each <em>returns</em>.'),
                ('57&ndash;62', 'Each array function with worked examples', 'WRITE',
                 'The paintings array on slide 62 is the reference example. Reproduce every operation on it.'),
                ('63&ndash;64', 'Home task; array syntax overview', 'WRITE',
                 'Do the reduce task &mdash; it is five minutes and it locks in the hardest of the six.'),
            ])
        },
        {
            'id': 'basics', 'nav': 'Basics', 'label': 'Slides 7&ndash;24',
            'title': 'Placement, output, types and truthiness',
            'html': """
<h3>Where JavaScript goes</h3>
""" + code('js-placement.html', """
<span class="c">&lt;!-- 1. INLINE — inside an HTML attribute --&gt;</span>
<span class="k">&lt;button</span> <span class="t">onclick</span>=<span class="s">"alert('hi')"</span><span class="k">&gt;</span>Click<span class="k">&lt;/button&gt;</span>

<span class="c">&lt;!-- 2. EMBEDDED — a &lt;script&gt; element in the document --&gt;</span>
<span class="k">&lt;script&gt;</span>
    console.log(<span class="s">'runs where it sits'</span>);
<span class="k">&lt;/script&gt;</span>

<span class="c">&lt;!-- 3. EXTERNAL — RECOMMENDED --&gt;</span>
<span class="k">&lt;script</span> <span class="t">src</span>=<span class="s">"myscripts/external.js"</span><span class="k">&gt;&lt;/script&gt;</span>

<span class="c">EXECUTION ORDER: it does not matter whether a script is external or
inline — they execute IN THE ORDER ENCOUNTERED on the page. Which is why
a script that touches the DOM belongs at the END of &lt;body&gt;, or must wait
for DOMContentLoaded (chapter 5).</span>
""", note='Slides 7–9', run='js-placement-96ca889f') + """

<h3>Five ways to produce output</h3>
""" + code('output.js', """
<span class="k">let</span> answer = prompt(<span class="s">"Please enter your name:"</span>);   <span class="c">// message + input field</span>
alert(<span class="s">'your name is '</span> + answer);                    <span class="c">// pop-up / modal</span>
<span class="k">let</span> ok = confirm(<span class="s">"Are you sure?"</span>);                 <span class="c">// ok / cancel → true or false</span>

document.write(<span class="s">'&lt;h1&gt;your name is '</span> + answer + <span class="s">'&lt;/h1&gt;'</span>);  <span class="c">// writes MARKUP into the page</span>
console.log(answer);                                 <span class="c">// the browser's JS console</span>

<span class="c">// WARNING from slide 10: copying code can turn straight quotes into
// smart quotes ( ' " ) which are NOT valid JavaScript. If a pasted line
// throws for no visible reason, retype the quotes.</span>
""", note='Slides 11–12') + """

<h3>Types</h3>
<p>Two basic kinds: <strong>reference types</strong> (objects) and <strong>primitive types</strong>.</p>
""" + table(['Primitive', 'Meaning'], [
                ('<code>boolean</code>', 'True or false.'),
                ('<code>number</code>', 'A double precision 64-bit floating point value.'),
                ('<code>bigint</code>', 'An integer that can be very large (greater than 2<sup>53</sup>).'),
                ('<code>string</code>', 'A sequence of characters delimited by single or double quotes.'),
                ('<code>null</code>', 'Has exactly one value: <code>null</code>.'),
                ('<code>undefined</code>', 'Has exactly one value. Assigned to variables that are not initialised. <strong>Different from <code>null</code>.</strong>'),
            ]) + code('primitive-vs-reference.js', """
<span class="c">// PRIMITIVE variables hold the VALUE directly in memory.</span>
<span class="k">let</span> a = <span class="s">5</span>;
<span class="k">let</span> b = a;      <span class="c">// b gets its own copy</span>
b = <span class="s">10</span>;
console.log(a);  <span class="c">// 5  — unaffected</span>

<span class="c">// OBJECT variables hold a REFERENCE (a pointer) to the block of memory.</span>
<span class="k">const</span> years = [<span class="s">1855</span>, <span class="s">1648</span>, <span class="s">1420</span>];
<span class="k">const</span> myYear2 = years;        <span class="c">// BOTH names point at the SAME array</span>
myYear2.push(<span class="s">2026</span>);
console.log(years.length);   <span class="c">// 4  — the "other" array changed too</span>

<span class="c">// Copying properly:</span>
<span class="k">const</span> shallow = [...years];               <span class="c">// spread — a new array, one level deep</span>
<span class="k">let</span> deepCopy = structuredClone(original); <span class="c">// a full, independent deep copy</span>
""", note='Slides 13–15', run='chapter-4/javascript-codes/ex-02-var') + """

<h3><code>var</code> vs <code>let</code> vs <code>const</code></h3>
""" + table(['', '<code>var</code>', '<code>let</code>', '<code>const</code>'], [
                ('<strong>Scope</strong>', 'Function scope &mdash; leaks out of <code>if</code> and <code>for</code> blocks.', 'Block scope.', 'Block scope.'),
                ('<strong>Reassign?</strong>', 'Yes.', 'Yes.', 'No &mdash; the binding cannot be reassigned.'),
                ('<strong>Redeclare?</strong>', 'Yes, silently.', 'No.', 'No.'),
                ('<strong>Hoisted?</strong>', 'Declaration hoisted, initialised as <code>undefined</code>.', 'Hoisted but unusable before its line.', 'Same as <code>let</code>.'),
                ('<strong>Use it?</strong>', 'Avoid.', 'When the value changes.', 'Default choice.'),
            ]) + hook(
                "<strong>Careful with <code>const</code> and objects:</strong> <code>const</code> "
                "freezes the <em>binding</em>, not the contents. "
                "<code>const a = [1,2]; a.push(3);</code> is perfectly legal &mdash; you changed what "
                "the reference points to, not which object it points at. <code>a = [4]</code> is the "
                "error.") + """

<h3>Truthy and falsy</h3>
""" + code('truthy.js', """
<span class="c">// Everything in JavaScript has an inherent boolean value.
// EXACTLY SEVEN values are falsy. Everything else is truthy.</span>

<span class="c">//   false      null      ""      ''      0      NaN      undefined</span>

<span class="c">// Consequences that catch people out — all of these are TRUTHY:</span>
Boolean([]);          <span class="c">// true  ← an empty array</span>
Boolean({});          <span class="c">// true  ← an empty object</span>
Boolean(<span class="s">"0"</span>);       <span class="c">// true  ← a non-empty STRING</span>
Boolean(<span class="s">"false"</span>);   <span class="c">// true  ← also just a string</span>
Boolean(-<span class="s">1</span>);         <span class="c">// true  ← only ZERO is falsy</span>

<span class="c">// The slide's own test — !! converts to a boolean:</span>
<span class="k">let</span> a = <span class="s">2</span>;
<span class="k">let</span> b;              <span class="c">// declared but not initialised → undefined</span>
!!a;               <span class="c">// true   → a is truthy</span>
!a;                <span class="c">// false</span>
!!b;               <span class="c">// false  → undefined is falsy</span>

<span class="c">// Practical use, straight from slide 19:</span>
<span class="k">if</span> (!answer) console.log(<span class="s">'the answer is empty'</span>);
<span class="k">else</span>        console.log(<span class="s">'Great: '</span> + answer);

<span class="c">// Same thing as a ternary (slide 20):</span>
console.log( (!answer) ? <span class="s">'the answer is empty'</span> : <span class="s">'Great: '</span> + answer );
""", note='Slide 21') + """
<p>Slide 20 also gives an opinion worth repeating in an exam: <em>better to avoid the
<code>switch</code> syntax because it can easily lead to errors</em> &mdash; the fall-through problem
when a <code>break</code> is forgotten.</p>

<h3>Loops and exceptions</h3>
""" + code('loops.js', """
<span class="c">// while — initialise before, test in the condition, modify inside</span>
<span class="k">let</span> count = <span class="s">0</span>;
<span class="k">while</span> (count &lt; <span class="s">10</span>) { count++; }

<span class="c">// do…while — the body always runs AT LEAST ONCE</span>
count = <span class="s">0</span>;
<span class="k">do</span> { count++; } <span class="k">while</span> (count &lt; <span class="s">10</span>);

<span class="c">// for — initialisation ; condition ; post-loop, all in one statement</span>
<span class="k">for</span> (<span class="k">let</span> i = <span class="s">0</span>; i &lt; <span class="s">10</span>; i++) { }

<span class="c">// try…catch — JavaScript is NOT fault tolerant: an uncaught runtime
// error stops execution at that line. This is how you prevent that.</span>
<span class="k">try</span> {
    nonexistantfunction(<span class="s">"hello"</span>);
} <span class="k">catch</span> (err) {
    alert(<span class="s">"An exception was caught:"</span> + err);
}
""", note='Slides 22–24', run='chapter-4/javascript-codes/ex-05-try-catch')
        },
        {
            'id': 'data', 'nav': 'Arrays &amp; Objects', 'label': 'Slides 25&ndash;38',
            'title': 'Arrays, objects and JSON',
            'html': """
<h3>Arrays</h3>
""" + code('arrays.js', """
<span class="c">// TWO ways to define one</span>
<span class="k">const</span> years = [<span class="s">1855</span>, <span class="s">1648</span>, <span class="s">1420</span>];              <span class="c">// literal notation — preferred</span>
<span class="k">const</span> years2 = <span class="k">new</span> Array(<span class="s">1855</span>, <span class="s">1648</span>, <span class="s">1420</span>);   <span class="c">// Array() constructor</span>

<span class="c">// Copy vs alias — slide 26</span>
<span class="k">const</span> myyear  = [...years];  <span class="c">// a NEW array with the same elements</span>
<span class="k">const</span> myyear2 = years;       <span class="c">// BOTH variables point to the SAME array</span>

<span class="c">// Arrays may hold mixed types, and may be multi-dimensional</span>
<span class="k">const</span> mess = [<span class="s">53</span>, <span class="s">"Canada"</span>, <span class="k">true</span>, <span class="s">1420</span>];
<span class="k">const</span> twoWeeks = [
    [<span class="s">"Mon"</span>,<span class="s">"Tue"</span>,<span class="s">"Wed"</span>,<span class="s">"Thu"</span>,<span class="s">"Fri"</span>],
    [<span class="s">"Mon"</span>,<span class="s">"Tue"</span>,<span class="s">"Wed"</span>]
];

<span class="c">// ITERATION — for…of (ES6) and its classic equivalent</span>
<span class="k">for</span> (<span class="k">let</span> yr <span class="k">of</span> years) console.log(yr);
<span class="k">for</span> (<span class="k">let</span> i = <span class="s">0</span>; i &lt; years.length; i++) console.log(years[i]);

<span class="c">// DESTRUCTURING — slide 28. These two blocks are equivalent.</span>
<span class="k">const</span> league = [<span class="s">"Liverpool"</span>, <span class="s">"Man City"</span>, <span class="s">"Arsenal"</span>, <span class="s">"Chelsea"</span>];
<span class="k">let</span> first = league[<span class="s">0</span>], second = league[<span class="s">1</span>], third = league[<span class="s">2</span>];
<span class="k">let</span> [a, b, c] = league;   <span class="c">// one line instead of three</span>
""", note='Slides 25–28', run='homepage-40c21c49') + """
<div class="card">
  <h4>Slide 29 &mdash; "who will answer?"</h4>
  <p>Given the ragged <code>twoWeeks</code> array above, the slide asks for
  <code>twoWeeks.length()</code>, <code>twoWeeks[0].length()</code> and
  <code>twoWeeks[1].length()</code>. <strong>All three as written throw a TypeError</strong>, because
  <code>length</code> is a <em>property</em>, not a method &mdash; there are no parentheses. Written
  correctly, <code>twoWeeks.length</code> is <strong>2</strong> (two rows),
  <code>twoWeeks[0].length</code> is <strong>5</strong> and <code>twoWeeks[1].length</code> is
  <strong>3</strong>. The array being ragged is the whole point of the question.</p>
</div>

<h3>Objects</h3>
<p>JavaScript objects are a collection of named values, called <strong>properties</strong>. Unlike C++
or Java, they are not created from classes &mdash; JavaScript is <strong>prototype based</strong>, and
new objects come from existing prototype objects.</p>
""" + code('01-creation.js', """
<span class="c">// LITERAL NOTATION — the most common way, and the preferred one</span>
<span class="k">const</span> objName = {
    name1: <span class="s">'value1'</span>,      <span class="c">// key : value, pairs separated by commas</span>
    name2: <span class="s">'value2'</span>
};

<span class="c">// Two ways to reach a property</span>
objName.name1;         <span class="c">// dot notation</span>
objName[<span class="s">"name1"</span>];      <span class="c">// square bracket notation (needed for dynamic keys)</span>

<span class="c">// OBJECT CONSTRUCTOR — the other way. Literal notation is preferred.</span>
<span class="k">const</span> obj2 = <span class="k">new</span> Object();
obj2.name1 = <span class="s">'value1'</span>;

<span class="c">// NESTED OBJECTS — the slide 34 exercise, done</span>
<span class="k">let</span> ksa = {
    id: <span class="s">'966'</span>,
    name: <span class="s">'KSA'</span>,
    currency: {
        name: <span class="s">'riyal'</span>,
        valueAgainstDollar: <span class="s">0.2666</span>,
        coins:      [<span class="s">0.01</span>, <span class="s">0.05</span>, <span class="s">0.1</span>, <span class="s">0.2</span>, <span class="s">0.5</span>],
        banknotes:  [<span class="s">1</span>, <span class="s">5</span>, <span class="s">10</span>, <span class="s">20</span>, <span class="s">50</span>, <span class="s">100</span>, <span class="s">200</span>, <span class="s">500</span>]
    }
};
console.log(ksa.currency.coins[<span class="s">0</span>]);   <span class="c">// 0.01</span>
""", note='Slides 30–34', run='01-creation-e9333e42') + code('03-object-destructuring.js', """
<span class="k">const</span> photo = {
    id: <span class="s">1</span>,
    title: <span class="s">"Central Library"</span>,
    location: { country: <span class="s">"Canada"</span>, city: <span class="s">"Calgary"</span> }
};

<span class="c">// The long way</span>
<span class="k">let</span> id = photo.id;
<span class="k">let</span> title = photo.title;
<span class="k">let</span> country = photo.location.country;
<span class="k">let</span> city = photo.location.city;

<span class="c">// Destructured — YOU MUST USE THE PROPERTY NAME. Unlike arrays,
// objects are matched by NAME, not by position.</span>
<span class="k">let</span> { id, title } = photo;
<span class="k">let</span> { country, city } = photo.location;

<span class="c">// …and both in one statement</span>
<span class="k">let</span> { id, title, location: { country, city } } = photo;
""", note='Slides 35–36', run='03-object-destructuring-75f32c73') + """

<h3>JSON</h3>
""" + code('json.js', """
<span class="c">// JSON = a language-independent data interchange format, used the way
// XML is used. The ONE syntactic difference from an object literal:
// PROPERTY NAMES ARE ENCLOSED IN QUOTES.</span>

<span class="c">// This is a STRING that happens to look like an object:</span>
<span class="k">const</span> text = <span class="s">'{ "name1": "value1", "name2": "value2" }'</span>;
text.name1;   <span class="c">// undefined — it is still just a string!</span>

<span class="c">// JSON.parse turns the string into a real JavaScript object</span>
<span class="k">const</span> anObj = JSON.parse(text);
console.log(anObj.name1);      <span class="c">// "value1"</span>

<span class="c">// …and JSON.stringify goes the other way, for sending data to a server</span>
<span class="k">const</span> back = JSON.stringify(anObj);

<span class="c">// The slide 38 example: an array of JSON strings into an HTML table</span>
<span class="k">const</span> countries = [<span class="s">'{"id": "01", "name": "KSA"}'</span>,
                   <span class="s">'{"id": "02", "name": "Japan"}'</span>,
                   <span class="s">'{"id": "03", "name": "Oman"}'</span>];

document.write(<span class="s">'&lt;table&gt;&lt;tr&gt;&lt;th&gt;ID&lt;/th&gt;&lt;th&gt;Country&lt;/th&gt;&lt;/tr&gt;'</span>);
<span class="k">for</span> (<span class="k">let</span> c <span class="k">of</span> countries) {
    <span class="k">let</span> co = JSON.parse(c);
    document.write(<span class="s">'&lt;tr&gt;&lt;td&gt;'</span> + co.id + <span class="s">'&lt;/td&gt;&lt;td&gt;'</span> + co.name + <span class="s">'&lt;/td&gt;&lt;/tr&gt;'</span>);
}
document.write(<span class="s">'&lt;/table&gt;'</span>);
""", note='Slides 37–38', run='chapter-4/javascript-codes/ex-07-json04') + hook(
                "<strong>The JSON question, every time:</strong> is it a string or an object? "
                "Quoted keys and wrapped in <code>' '</code> means it is a <em>string</em> and you "
                "cannot use dot notation until <code>JSON.parse()</code> has run. Everything a "
                "<code>fetch()</code> returns in chapter 6 arrives in exactly this state.")
        },
        {
            'id': 'functions', 'nav': 'Functions', 'label': 'Slides 39&ndash;54',
            'title': 'Functions, callbacks, hoisting and scope',
            'html': """
<h3>Declarations, expressions, defaults and rest</h3>
""" + code('functions.js', """
<span class="c">// FUNCTION DECLARATION</span>
<span class="k">function</span> subtotal(price, quantity) {
    <span class="k">return</span> price * quantity;
}
<span class="k">let</span> result = subtotal(<span class="s">10</span>, <span class="s">2</span>);   <span class="c">// invoked with the () operator</span>

<span class="c">// FUNCTION EXPRESSION — an ANONYMOUS function assigned to a variable</span>
<span class="k">const</span> calculateSubtotal = <span class="k">function</span> (price, quantity) {
    <span class="k">return</span> price * quantity;
};

<span class="c">// DEFAULT PARAMETERS — slide 41</span>
<span class="k">function</span> foo(a, b) { <span class="k">return</span> a + b; }
<span class="k">let</span> bar = foo(<span class="s">3</span>);              <span class="c">// 3 + undefined  →  NaN</span>

<span class="k">function</span> foo2(a = <span class="s">10</span>, b = <span class="s">0</span>) { <span class="k">return</span> a + b; }
<span class="k">let</span> bar2 = foo2(<span class="s">3</span>);            <span class="c">// 3 + 0  →  3</span>

<span class="c">// REST PARAMETERS — an indeterminate number of arguments, via ...</span>
<span class="k">function</span> concatenate(...args) {
    <span class="k">let</span> s = <span class="s">""</span>;
    <span class="k">for</span> (<span class="k">let</span> a <span class="k">of</span> args) s += a + <span class="s">" "</span>;
    <span class="k">return</span> s;
}
concatenate(<span class="s">"fatima"</span>, <span class="s">"hema"</span>, <span class="s">"jane"</span>, <span class="s">"alia"</span>);  <span class="c">// "fatima hema jane alia "</span>
concatenate(<span class="s">"jamal"</span>, <span class="s">"nasir"</span>);                    <span class="c">// "jamal nasir "</span>

<span class="k">let</span> sum = <span class="k">function</span> (...args) { <span class="k">let</span> s = <span class="s">0</span>; <span class="k">for</span> (<span class="k">let</span> e <span class="k">of</span> args) s += e; <span class="k">return</span> s; };
""", note='Slides 39–42', run='restfunc-a613209f') + """

<h3>Hoisting &mdash; the half people forget</h3>
""" + code('hoisted.js', """
<span class="c">// Function DECLARATIONS are hoisted to the top of their level,
// so this works even though the call comes first:</span>
greet();                          <span class="c">// "hi"  ✓</span>
<span class="k">function</span> greet() { console.log(<span class="s">"hi"</span>); }

<span class="c">// Function EXPRESSIONS are not — the VARIABLE is hoisted, the
// ASSIGNMENT is not. THE ASSIGNMENTS ARE NOT HOISTED.</span>
greet2();                         <span class="c">// TypeError: greet2 is not a function  ✗</span>
<span class="k">const</span> greet2 = <span class="k">function</span> () { console.log(<span class="s">"hi"</span>); };

<span class="c">// Same rule for variables:</span>
console.log(x);                   <span class="c">// undefined  ← declaration hoisted, value not</span>
<span class="k">var</span> x = <span class="s">5</span>;
console.log(x);                   <span class="c">// 5</span>

<span class="c">// with let/const you get an error instead of undefined:</span>
console.log(y);                   <span class="c">// ReferenceError</span>
<span class="k">let</span> y = <span class="s">5</span>;
""", note='Slide 44', run='hoisted-be401812') + """

<h3>Callbacks &mdash; and the exercise the slides call essential</h3>
<p>Because functions are objects, a function can be passed as an argument to another function. That
passed function is a <strong>callback</strong>. Slide 46 marks its exercise as <em>very important to
understand &mdash; the basis of all functional programming</em>, so here it is in full.</p>
""" + code('map-exercise.js', """
<span class="c">// A map function that applies any given function to any number of
// input lists, returning an array of the results.</span>
<span class="k">let</span> map = <span class="k">function</span> (f, ...args) {      <span class="c">// f is the CALLBACK; ...args the lists</span>
    <span class="k">let</span> s = [], i = <span class="s">0</span>;
    <span class="k">for</span> (<span class="k">let</span> e <span class="k">of</span> args) s[i++] = f(e);  <span class="c">// call f on each list</span>
    <span class="k">return</span> s;
};

<span class="k">let</span> sum = <span class="k">function</span> (a) {
    <span class="k">let</span> s = <span class="s">0</span>;
    <span class="k">for</span> (<span class="k">let</span> e <span class="k">of</span> a) s += e;
    <span class="k">return</span> s;
};

map(sum, [<span class="s">3</span>, <span class="s">5</span>, <span class="s">6</span>], [<span class="s">4</span>, <span class="s">7</span>, <span class="s">8</span>], [<span class="s">8</span>, <span class="s">5</span>]);   <span class="c">// → [14, 19, 13]</span>

<span class="c">// The home task on slide 47: write three more callbacks for the same map.</span>
<span class="k">let</span> multiply = a =&gt; a.reduce((p, e) =&gt; p * e, <span class="s">1</span>);
<span class="k">let</span> average  = a =&gt; sum(a) / a.length;
<span class="k">let</span> max      = <span class="k">function</span> (a) { <span class="k">let</span> m = a[<span class="s">0</span>]; <span class="k">for</span> (<span class="k">let</span> e <span class="k">of</span> a) <span class="k">if</span> (e &gt; m) m = e; <span class="k">return</span> m; };

map(multiply, [<span class="s">3</span>, <span class="s">5</span>, <span class="s">6</span>], [<span class="s">4</span>, <span class="s">7</span>, <span class="s">8</span>]);   <span class="c">// → [90, 224]</span>
map(average,  [<span class="s">3</span>, <span class="s">5</span>, <span class="s">6</span>]);                <span class="c">// → [4.666…]</span>
map(max,      [<span class="s">3</span>, <span class="s">5</span>, <span class="s">6</span>], [<span class="s">8</span>, <span class="s">5</span>]);         <span class="c">// → [6, 8]</span>

<span class="c">// Slide 48: you can define the callback DIRECTLY in the invocation</span>
map(<span class="k">function</span> (a) { <span class="k">return</span> a.length; }, [<span class="s">3</span>, <span class="s">5</span>, <span class="s">6</span>], [<span class="s">4</span>]);  <span class="c">// → [3, 1]</span>
""", note='Slides 45–48', run='map-reduce-10031ff7') + """

<h3><code>this</code>, and constructors as functions</h3>
""" + code('this-and-constructors.js', """
<span class="c">// Objects can have properties that ARE functions.
// Inside them, `this` refers to the object that owns the function.
// WITHOUT `this`, brand and price are simply NOT DEFINED.</span>
<span class="k">const</span> order = {
    salesDate: <span class="s">"May 5, 2016"</span>,
    product: {
        price: <span class="s">500.00</span>,
        brand: <span class="s">"Acer"</span>,
        output: <span class="k">function</span> () { <span class="k">return</span> `${<span class="k">this</span>.brand}, ${<span class="k">this</span>.price}$`; }
    },
    customer: {
        name: <span class="s">"Ward Jondob"</span>,
        address: <span class="s">"123 Chamal St, Najran"</span>,
        output: <span class="k">function</span> () { <span class="k">return</span> `${<span class="k">this</span>.name}, ${<span class="k">this</span>.address}`; }
    }
};
alert(order.product.output());     <span class="c">// "Acer, 500$"</span>
alert(order.customer.output());

<span class="c">// A CONSTRUCTOR is just a function that assigns to `this`.
// Convention: capitalise its name. Create instances with `new`.</span>
<span class="k">function</span> Customer(name, address, city) {
    <span class="k">this</span>.name = name;
    <span class="k">this</span>.address = address;
    <span class="k">this</span>.city = city;
    <span class="k">this</span>.output = <span class="k">function</span> () { <span class="k">return</span> `${<span class="k">this</span>.name}, ${<span class="k">this</span>.address}, ${<span class="k">this</span>.city}`; };
}
<span class="k">const</span> cust1 = <span class="k">new</span> Customer(<span class="s">"Ward Jondob"</span>, <span class="s">"123 Chamal Street"</span>, <span class="s">"Najran"</span>);
alert(cust1.output());
""", note='Slides 49–50', run='constructor-61d6ade6') + """

<h3>Arrow syntax</h3>
""" + code('arrows.js', """
<span class="c">// The same function, three ways</span>
<span class="k">const</span> taxRate = <span class="k">function</span> () { <span class="k">return</span> <span class="s">0.05</span>; };   <span class="c">// expression</span>
<span class="k">const</span> taxRate = () =&gt; { <span class="k">return</span> <span class="s">0.05</span>; };          <span class="c">// arrow, explicit return</span>
<span class="k">const</span> taxRate = () =&gt; <span class="s">0.05</span>;                     <span class="c">// arrow, IMPLICIT return</span>

<span class="c">// With parameters</span>
(a, b) =&gt; { <span class="k">return</span> a + b; }
(a, b) =&gt; a + b                <span class="c">// no braces = the expression IS the return value</span>
a =&gt; a * <span class="s">2</span>                    <span class="c">// one parameter: the parentheses are optional</span>

<span class="c">// RESTRICTION stated on the slide: arrow functions CANNOT be used as
// constructors. `new` on an arrow function throws.</span>
""", note='Slide 51') + """

<h3>Scope</h3>
<p>JavaScript has four scopes: <strong>function</strong> (local), <strong>block</strong>,
<strong>module</strong> and <strong>global</strong>.</p>
""" + code('scope.js', """
<span class="c">// BLOCK SCOPE — let and const are confined to the { } they appear in.
// var is NOT: declared with var inside a block, it is available outside.</span>
<span class="k">if</span> (<span class="k">true</span>) {
    <span class="k">let</span>   blockOnly = <span class="s">"invisible outside"</span>;
    <span class="k">const</span> alsoBlock = <span class="s">"invisible outside"</span>;
    <span class="k">var</span>   leaks     = <span class="s">"visible outside!"</span>;
}
console.log(leaks);       <span class="c">// "visible outside!"  ← the var problem</span>
console.log(blockOnly);   <span class="c">// ReferenceError</span>

<span class="c">// FUNCTION / LOCAL SCOPE — everything declared in a function is
// invisible outside it, whichever keyword you use.</span>
<span class="k">function</span> f() { <span class="k">var</span> local = <span class="s">1</span>; }
console.log(local);       <span class="c">// ReferenceError</span>

<span class="c">// The classic loop demonstration</span>
<span class="k">for</span> (<span class="k">var</span> i = <span class="s">0</span>; i &lt; <span class="s">3</span>; i++) { }
console.log(i);           <span class="c">// 3   ← var survives the loop</span>
<span class="k">for</span> (<span class="k">let</span> j = <span class="s">0</span>; j &lt; <span class="s">3</span>; j++) { }
console.log(j);           <span class="c">// ReferenceError  ← let does not</span>
""", note='Slides 52–54', run='global-95bd7f63')
        },
        {
            'id': 'arrays', 'nav': 'Array Functions', 'label': 'Slides 55&ndash;64',
            'title': 'The six array functions — Part 2',
            'html': """
<p>Short deck, enormous payoff. These six replace almost every loop you would otherwise write, and
they appear again in chapter 5 (transforming NodeLists) and chapter 7 (shaping database results).</p>

<p>The slides use one reference array throughout. Everything below runs against it.</p>
""" + code('paintings.js — the reference data', """
<span class="k">const</span> paintings = [
    {title: <span class="s">"Girl with a pearl earring"</span>,  artist: <span class="s">"Vermeer"</span>,  value: <span class="s">10</span>},
    {title: <span class="s">"Artists Holding a Thistle"</span>,  artist: <span class="s">"Durer"</span>,    value: <span class="s">7</span>},
    {title: <span class="s">"Wheat field with Crows"</span>,     artist: <span class="s">"Van Gogh"</span>, value: <span class="s">16</span>},
    {title: <span class="s">"Burial at Ornans"</span>,           artist: <span class="s">"Courbet"</span>,  value: <span class="s">18</span>},
    {title: <span class="s">"Wheat field with Crows"</span>,     artist: <span class="s">"Van Gogh"</span>, value: <span class="s">9</span>}
];
""", note='Slide 62') + table(
                ['Function', 'What it does', 'What it RETURNS'], [
                    ('<code>forEach()</code>', 'Iterates through the array.', '<strong>Nothing</strong> (<code>undefined</code>). Use it for side effects only.'),
                    ('<code>find()</code>', 'Finds the <em>first</em> element whose property matches a condition.', 'That one element, or <code>undefined</code>.'),
                    ('<code>filter()</code>', 'Finds <em>all</em> elements matching a condition.', 'A new <strong>array</strong> &mdash; possibly empty.'),
                    ('<code>map()</code>', 'Transforms every element by the passed function.', 'A new array of <strong>the same size</strong>.'),
                    ('<code>reduce()</code>', 'Collapses the array by combining elements.', 'A <strong>single value</strong>.'),
                    ('<code>sort()</code>', 'Sorts a one-dimensional array <strong>in place</strong>, ascending, converting to strings by default.', 'The same (now mutated) array.'),
                ]) + code('array-functions.js', """
<span class="c">// ── forEach: iterate. Returns nothing. ──────────────────────────</span>
paintings.forEach(p =&gt; console.log(p.title));

<span class="c">// ── find: the FIRST match, or undefined ─────────────────────────</span>
<span class="k">const</span> courbet = paintings.find( p =&gt; p.artist === <span class="s">'Courbet'</span> );
console.log(courbet.title);            <span class="c">// "Burial at Ornans"</span>
<span class="c">// the callback must return TRUE (matches) or FALSE (does not).</span>

<span class="c">// ── filter: ALL matches, as a new array ─────────────────────────</span>
<span class="k">const</span> vanGoghs = paintings.filter( p =&gt; p.artist === <span class="s">'Van Gogh'</span> );
console.log(vanGoghs.length);          <span class="c">// 2</span>

<span class="c">// ── map: same size, transformed values ──────────────────────────</span>
<span class="k">const</span> titles = paintings.map( p =&gt; p.title );   <span class="c">// 5 strings</span>

<span class="c">// The slide 59 example, with a regular expression (chapter 5)</span>
<span class="k">const</span> arr = [<span class="s">"hello"</span>, <span class="s">"selem"</span>, <span class="s">"ciao"</span>, <span class="s">"hallo"</span>, <span class="s">"gutentag"</span>];
<span class="k">const</span> pat = /el/;
arr.map(o =&gt; pat.test(o));      <span class="c">// [true, true, false, false, false]  ← SAME SIZE</span>
arr.filter(o =&gt; pat.test(o));   <span class="c">// ['hello', 'selem']                ← FEWER</span>

<span class="c">// ── reduce: array → one value ───────────────────────────────────
//   (prev, current) => …          prev carries the running result
//   the last argument is the INITIAL value of prev</span>
<span class="k">let</span> initial = <span class="s">0</span>;
<span class="k">const</span> total = paintings.reduce( (prev, p) =&gt; prev + p.value, initial );
console.log(total);                    <span class="c">// 60</span>

<span class="k">const</span> all = arr.reduce( (prev, p) =&gt; prev + <span class="s">" "</span> + p );
<span class="c">// 'hello selem ciao hallo gutentag'  ← no initial value: prev starts as arr[0]</span>

<span class="c">// the slide 63 home task: multiply every element</span>
<span class="k">const</span> product = [<span class="s">2</span>, <span class="s">3</span>, <span class="s">4</span>].reduce( (prev, e) =&gt; prev * e, <span class="s">1</span> );   <span class="c">// 24</span>

<span class="c">// ── sort: IN PLACE, and stringly by default ─────────────────────</span>
arr.sort();     <span class="c">// ['ciao','gutentag','hallo','hello','selem']  — fine for strings</span>

<span class="k">const</span> numberArray = [<span class="s">40</span>, <span class="s">5</span>, <span class="s">200</span>, <span class="s">1</span>];
numberArray.sort();                    <span class="c">// [1, 200, 40, 5]   ← WRONG. Sorted as text!</span>

<span class="k">function</span> compareNumbers(a, b) { <span class="k">return</span> a - b; }
numberArray.sort(compareNumbers);      <span class="c">// [1, 5, 40, 200]   ← correct</span>

<span class="c">// A comparator returns:  0 if equal,  positive if a &gt; b,  negative if a &lt; b</span>
<span class="k">const</span> compareFn = (a, b) =&gt; a.value - b.value;
paintings.sort(compareFn);             <span class="c">// by value, ascending</span>

<span class="c">// sort() MUTATES. Use toSorted() to leave the original alone.</span>
<span class="k">const</span> sortedCopy = paintings.toSorted(compareFn);
""", note='Slides 56–63', run='index-b0f56432') + hook(
                "<strong>Pick the right one by asking what you want back.</strong> Nothing &rarr; "
                "<code>forEach</code>. One element &rarr; <code>find</code>. Fewer elements &rarr; "
                "<code>filter</code>. The same number, changed &rarr; <code>map</code>. One value "
                "&rarr; <code>reduce</code>. The same array, reordered &rarr; <code>sort</code>.")
        },
        {
            'id': 'traps', 'nav': 'Traps', 'label': 'Marks Lost Here',
            'title': 'The eight things people get wrong',
            'html': (
                trap('<code>sort()</code> on numbers',
                     '<code>[40, 5, 200, 1].sort()</code> gives <code>[1, 200, 40, 5]</code>. By default <code>sort()</code> converts elements to strings, and "200" sorts before "40" because "2" comes before "4".',
                     'Always pass a comparator for numbers: <code>arr.sort((a,b) =&gt; a - b)</code>. And remember it sorts <strong>in place</strong> &mdash; the original array is modified. Use <code>toSorted()</code> if you need it intact.') +
                trap('Expecting <code>forEach</code> to return something',
                     '<code>const doubled = arr.forEach(x =&gt; x * 2)</code> leaves <code>doubled</code> as <code>undefined</code>. <code>forEach</code> exists for side effects and returns nothing.',
                     'If you want a result, use <code>map</code>. If you want fewer items, use <code>filter</code>. If you want one value, use <code>reduce</code>.') +
                trap('Hoisting only half-remembered',
                     'People learn "declarations are hoisted" and assume everything works. But calling a function <em>expression</em> before its line gives <em>TypeError: not a function</em>, and reading a <code>var</code> before its line gives <code>undefined</code> rather than an error.',
                     'Declarations move; <strong>assignments do not</strong>. Function declarations are callable early; function expressions are not.') +
                trap('<code>var</code> escaping a block',
                     'A <code>var</code> declared inside an <code>if</code> or a <code>for</code> is visible after the block ends, and a loop counter declared with <code>var</code> still exists afterwards. This is exactly the contrast slide 53 draws.',
                     'Use <code>const</code> by default and <code>let</code> when the value changes. Both respect block scope.') +
                trap('Forgetting <code>this</code> inside an object method',
                     'Writing <code>return `${brand}, ${price}`</code> instead of <code>${this.brand}</code> throws, because <code>brand</code> is not a variable in scope &mdash; it is a property of the object. The slide says so explicitly.',
                     'Inside a method, reach the object&rsquo;s own properties through <code>this</code>. And do not use an arrow function as an object method if you need <code>this</code>.') +
                trap('Treating a JSON string as an object',
                     '<code>text.name1</code> on a JSON string is <code>undefined</code>, silently. The quotes around the whole thing make it a string, and strings do not have your properties.',
                     '<code>JSON.parse()</code> first, then use dot notation. <code>JSON.stringify()</code> to go back.') +
                trap('Copying an array by assigning it',
                     '<code>const copy = original</code> creates a second name for the <em>same</em> array. Changing one changes both, because object variables hold a reference, not the value.',
                     '<code>[...original]</code> for a shallow copy, <code>structuredClone(original)</code> for a deep one.') +
                trap('Assuming empty things are falsy',
                     '<code>[]</code> and <code>{}</code> are <strong>truthy</strong>, so <code>if (myArray)</code> is true even for an empty array. So is the string <code>"0"</code>.',
                     'There are exactly seven falsy values: <code>false</code>, <code>null</code>, <code>""</code>, <code>\'\'</code>, <code>0</code>, <code>NaN</code>, <code>undefined</code>. Test emptiness with <code>arr.length === 0</code>.')
            )
        },
        {
            'id': 'cheat', 'nav': 'Cheat Sheet', 'label': 'One Screen',
            'title': 'Chapter 4 on a single screen',
            'html': cheat([
                ('Primitives', [
                    '<code>boolean</code> <code>number</code> <code>bigint</code>',
                    '<code>string</code> <code>null</code> <code>undefined</code>',
                    'Everything else is a reference type (object)',
                    'Primitive holds the value; object holds a reference',
                ]),
                ('Falsy — all seven', [
                    '<code>false</code>',
                    '<code>null</code> &middot; <code>undefined</code>',
                    '<code>""</code> &middot; <code>\'\'</code>',
                    '<code>0</code> &middot; <code>NaN</code>',
                    'Everything else is truthy, including <code>[]</code> and <code>{}</code>',
                ]),
                ('Declarations', [
                    '<code>const</code> &mdash; block scope, no reassign (default)',
                    '<code>let</code> &mdash; block scope, reassignable',
                    '<code>var</code> &mdash; function scope, leaks. Avoid.',
                    'Declarations hoist; assignments do not',
                ]),
                ('Output', [
                    '<code>alert()</code> &mdash; modal message',
                    '<code>prompt()</code> &mdash; message + input',
                    '<code>confirm()</code> &mdash; ok / cancel',
                    '<code>document.write()</code> &mdash; markup into the page',
                    '<code>console.log()</code> &mdash; the JS console',
                ]),
                ('Arrays', [
                    '<code>[a, b]</code> literal &middot; <code>new Array(a, b)</code>',
                    '<code>for (let x of arr)</code>',
                    '<code>let [a, b] = arr</code> destructure by POSITION',
                    '<code>[...arr]</code> shallow copy',
                    '<code>arr.length</code> &mdash; a property, no <code>()</code>',
                ]),
                ('Objects', [
                    '<code>{ key: value }</code> literal (preferred)',
                    '<code>obj.key</code> or <code>obj["key"]</code>',
                    '<code>let {a, b} = obj</code> destructure by NAME',
                    'Prototype based &mdash; no classes',
                    '<code>this</code> inside a method',
                ]),
                ('JSON', [
                    'Keys are <strong>quoted</strong>',
                    'A JSON string is a <em>string</em>',
                    '<code>JSON.parse(str)</code> &rarr; object',
                    '<code>JSON.stringify(obj)</code> &rarr; string',
                ]),
                ('Functions', [
                    '<code>function f() {}</code> declaration (hoisted)',
                    '<code>const f = function () {}</code> expression',
                    '<code>const f = (a) =&gt; a * 2</code> arrow',
                    '<code>function f(a = 10)</code> default',
                    '<code>function f(...args)</code> rest',
                    'Arrows cannot be constructors',
                ]),
                ('Array functions', [
                    '<code>forEach</code> &rarr; nothing',
                    '<code>find</code> &rarr; first match',
                    '<code>filter</code> &rarr; array of matches',
                    '<code>map</code> &rarr; same size, transformed',
                    '<code>reduce(fn, init)</code> &rarr; one value',
                    '<code>sort(cmp)</code> &rarr; in place; needs a comparator for numbers',
                ]),
            ])
        },
        {
            'id': 'drills', 'nav': 'Drills', 'label': 'Type It Blind',
            'title': 'Predict the output, then run it',
            'html': """
<p>This chapter is examined with predict-the-output questions, so practise it that way: write your
answer down <em>before</em> pressing run. Being wrong and knowing why is the whole exercise.</p>
""" + drills([
                'Write down what <code>[40, 5, 200, 1].sort()</code> produces, then run it, then fix it with a comparator.',
                'Predict the output of the concatenation example on slide 18 &mdash; both <code>console.log</code> calls &mdash; before you run it.',
                'Write six expressions, three truthy and three falsy, that a classmate would guess wrong. Use <code>[]</code>, <code>{}</code> and <code>"0"</code>.',
                'Call a function declaration before its definition, then convert it to an expression and observe the different error.',
                'Write the same loop with <code>var</code> and with <code>let</code>, then log the counter after the loop in each case.',
                'Copy an array by assignment, mutate the copy, and prove the original changed. Then fix it two ways.',
                'Build the KSA object from slide 34 from memory, then read <code>ksa.currency.banknotes[3]</code>.',
                'Destructure that object&rsquo;s <code>name</code> and its currency&rsquo;s <code>name</code> in one statement &mdash; work out what to do about the name collision.',
                'Take a JSON string, try to read a property directly, then parse it and read the same property.',
                'Implement the slide 46 map function from memory, then write <code>multiply</code>, <code>average</code> and <code>max</code> callbacks for it.',
                'Write an object with a method that uses <code>this</code>, then delete the <code>this</code> and read the error message carefully.',
                'Write a constructor function, create two instances, and give each one a different value.',
                'Convert three function expressions to arrow syntax, one with implicit return.',
                'On the paintings array: total the values with <code>reduce</code>, list the Van Goghs with <code>filter</code>, get all titles with <code>map</code>, and sort by value.',
                'Write the same "find all paintings worth more than 10" three ways &mdash; a <code>for</code> loop, <code>filter</code>, and <code>reduce</code> &mdash; and decide which reads best.',
            ]) + """
<p>The full example set for this chapter is at
<a href="/academics/software-engineering/se371/extra-resources/chapter-4/javascript-codes/" target="_blank" rel="noopener">chapter-4/javascript-codes/</a>,
and there are three graded tutorials in your study material:
<a href="/academics/software-engineering/se371/extra-resources/resource-viewers/3-variables-if-loops-with-examples-v1-da2ad2a5/" target="_blank" rel="noopener">variables, if and loops</a>,
<a href="/academics/software-engineering/se371/extra-resources/resource-viewers/2-javascript-tutorial-functions-and-json-objects-8fc2f70e/" target="_blank" rel="noopener">functions and JSON objects</a>, and
<a href="/academics/software-engineering/se371/extra-resources/resource-viewers/4-2-javascript-tutorial-more-on-array-methods-49eb0bc1/" target="_blank" rel="noopener">more on array methods</a>.
There is also an <a href="/academics/software-engineering/se371/extra-resources/resource-viewers/3-javascript-exercises-set-1-questions-88131c0e/" target="_blank" rel="noopener">exercise set with questions</a>.</p>
"""
        },
    ],
    'quiz': [
        {'tag': 'Arrays', 'q': 'What does [40, 5, 200, 1].sort() return?',
         'opts': ['[1, 5, 40, 200]', '[1, 200, 40, 5]', '[200, 40, 5, 1]', 'An error — sort needs a comparator'],
         'a': 1,
         'why': 'By default sort() converts elements to strings before comparing, so "200" sorts before "40". Pass a comparator such as (a,b) => a - b for numeric order.'},
        {'tag': 'Types', 'q': 'Which of these values is truthy?',
         'opts': ['<code>0</code>', '<code>""</code>', '<code>[]</code>', '<code>NaN</code>'],
         'a': 2,
         'why': 'The falsy list is exactly false, null, "", \'\', 0, NaN and undefined. An empty array is an object, and every object is truthy — which is why if (arr) does not test for emptiness.'},
        {'tag': 'Functions', 'q': 'What happens when you call a function expression before the line that defines it?',
         'opts': ['It works — declarations are hoisted', 'TypeError: it is not a function',
                  'It returns undefined', 'SyntaxError at parse time'],
         'a': 1,
         'why': 'The variable is hoisted but the assignment is not, so at call time the name exists and holds undefined. Calling undefined gives a TypeError. A function declaration would have worked.'},
        {'tag': 'Scope', 'q': 'A variable is declared with var inside an if block. Where can it be read?',
         'opts': ['Only inside that block', 'Anywhere in the enclosing function',
                  'Only after the block finishes', 'Nowhere — var is not allowed in blocks'],
         'a': 1,
         'why': 'var has function scope, not block scope, so it leaks out of if and for blocks. let and const are confined to the block, which is why the slides recommend them.'},
        {'tag': 'Objects', 'q': 'const arr = [1,2]; const copy = arr; copy.push(3); What is arr.length?',
         'opts': ['2 — copy is an independent array', '3 — both names point at the same array',
                  'An error — arr is const', '0 — push replaced the array'],
         'a': 1,
         'why': 'Object variables hold a reference, so both names point at one array. const only prevents reassigning the binding, not mutating the object. Use [...arr] or structuredClone() to copy.'},
        {'tag': 'JSON', 'q': 'const text = \'{"name": "KSA"}\'; What is text.name?',
         'opts': ['"KSA"', 'undefined', 'null', 'A TypeError'],
         'a': 1,
         'why': 'text is a string that happens to look like an object. Reading an unknown property of a string gives undefined, silently. JSON.parse(text).name returns "KSA".'},
        {'tag': 'Array functions', 'q': 'Which method returns a new array of the same length as the original?',
         'opts': ['<code>filter()</code>', '<code>find()</code>', '<code>map()</code>', '<code>reduce()</code>'],
         'a': 2,
         'why': 'map() transforms every element and always returns the same number of elements. filter() returns only the matches, find() returns a single element, and reduce() collapses to one value.'},
        {'tag': 'this', 'q': 'Inside an object method, why must you write this.brand rather than brand?',
         'opts': ['this is required by strict mode',
                  'brand is a property of the object, not a variable in scope',
                  'brand would refer to the global variable of the same name',
                  'Template strings only accept this expressions'],
         'a': 1,
         'why': 'The slide states it directly: without the this keyword, brand and price are not defined. Properties live on the object and are reached through this, not through the scope chain.'},
    ],
})


# ═══════════════════════════════════════════════════════════════════════════ #
# CHAPTER 05 — JavaScript in the Front End
# ═══════════════════════════════════════════════════════════════════════════ #

CHAPTERS.append({
    'num': 5,
    'slug': '05-javascript-in-the-front-end',
    'file': 'javascript-in-the-front-end.html',
    'title': 'JavaScript in the Front End',
    'desc': ('Slide-by-slide breakdown of SE371 Chapter 5 — the DOM, selection methods, element '
             'manipulation, event handling, propagation and delegation, form validation and regular '
             'expressions.'),
    'sub': ('Where JavaScript stops being a language exercise and starts changing pages. Every lab '
            'from here uses this chapter, and three of its ideas — DOM timing, event propagation and '
            'preventDefault — cause most of the bugs you will hit all semester.'),
    'stats': ['58 slides', 'Single deck', 'Pure write-it', 'Book ch. 9'],
    'sections': [
        {
            'id': 'orient', 'nav': 'Start Here', 'label': 'Orientation',
            'title': 'What this chapter is really for',
            'html': """
<p>One continuous deck, and it moves in a straight line: <strong>find nodes &rarr; change nodes &rarr;
respond to events &rarr; validate forms</strong>. Read it in that order and each section explains the
next.</p>

<div class="grid-2">
  <div class="card">
    <h4>The three ideas that cause every bug</h4>
    <p><strong>1. Timing</strong> &mdash; you cannot touch the DOM before it exists (slides 23, 28).
    <strong>2. Propagation</strong> &mdash; a click on a button also fires the handlers of everything
    around it (slides 32&ndash;35). <strong>3. <code>preventDefault</code></strong> &mdash; without it
    a form submits regardless of what your validation decided (slides 43, 48, 54).</p>
  </div>
  <div class="card">
    <h4>Where it connects</h4>
    <p>The callbacks from chapter 4 become event handlers here. The forms from chapter 2 become
    interactive here. The regular expressions at the end reappear as Sequelize validators in chapter 7.
    And the "validate on the server too" warning from chapter 2 slide 65 is repeated on slide 47 for
    the same reason.</p>
  </div>
</div>
"""
        },
        {
            'id': 'map', 'nav': 'Slide Map', 'label': 'Navigation',
            'title': 'All 58 slides, weighted',
            'html': slidemap([
                ('1&ndash;2', 'Title; SweetAlert as a third-party output library', 'SKIM',
                 'A CDN script tag and a <code>Swal.fire({...})</code> call. Nice for labs, unlikely to be examined.'),
                ('3&ndash;4', 'The DOM; the document object', 'MEMORIZE',
                 '<code>document</code> is the root object representing the entire HTML document, globally accessible.'),
                ('5&ndash;6', 'Nodes, NodeLists, node properties', 'MEMORIZE',
                 'A NodeList behaves like an array. The examinable footnote: <code>forEach</code> works on a NodeList but <strong>not</strong> on an HTMLCollection.'),
                ('7&ndash;8', 'Selection methods, old and new', 'WRITE',
                 'The three old ones and the two query methods. <code>querySelector</code> returns the <em>first</em> match.'),
                ('9&ndash;11', 'Element node properties; tag-specific properties', 'WRITE',
                 '<code>classList</code>, <code>className</code>, <code>id</code>, <code>innerHTML</code>, <code>style</code>, <code>tagName</code>, plus <code>href</code>/<code>name</code>/<code>src</code>/<code>value</code>.'),
                ('12&ndash;13', 'Changing an element&rsquo;s style', 'WRITE',
                 'You <em>can</em> set <code>.style.x</code> directly, but the slides say it is preferable to change <code>className</code> or <code>classList</code>.'),
                ('14&ndash;15', 'innerHTML vs textContent vs DOM manipulation', 'MEMORIZE',
                 'The performance argument is given explicitly: every time <code>innerHTML</code> is set, the HTML must be parsed, a DOM constructed and inserted. Also flagged <em>not secure</em>.'),
                ('16&ndash;20', 'Family relations; DOM manipulation methods; the exercise', 'WRITE',
                 'Seven manipulation methods. Slide 20 asks you to redo the makeArticle exercise with them &mdash; do both versions and compare.'),
                ('21', 'The dataset property and data-* attributes', 'WRITE',
                 'Note the naming rule: <code>data-user-name</code> becomes <code>dataset.userName</code>.'),
                ('22&ndash;23', 'Handling events; DOM timing', 'MEMORIZE',
                 'You cannot access or modify the DOM until it has loaded. This is the setup for slide 28.'),
                ('24&ndash;27', 'Event handlers, anonymous functions, NodeList arrays', 'WRITE',
                 'Register with <code>addEventListener()</code>, passing a callback. Three equivalent forms on slide 26.'),
                ('28&ndash;29', 'window.load vs DOMContentLoaded', 'MEMORIZE',
                 '<code>load</code> waits for images and stylesheets too; <code>DOMContentLoaded</code> fires when the HTML is downloaded and parsed. <strong>Generally the one you want.</strong>'),
                ('30&ndash;31', 'The event object', 'WRITE',
                 'Add a parameter, conventionally <code>e</code>, to the callback. <code>e.target</code> matters for delegation.'),
                ('32&ndash;35', 'Propagation: capturing, bubbling, stopPropagation', 'MEMORIZE',
                 'The most conceptually examinable block in the chapter. Learn the two phases and their directions.'),
                ('36&ndash;38', 'Event delegation', 'WRITE',
                 'One listener on the parent instead of one per child. Note the warning: <code>nodeName</code> always returns <strong>upper case</strong>.'),
                ('39&ndash;42', 'Event types: mouse, keyboard, form', 'MEMORIZE',
                 'Five categories. Learn the seven mouse events, the two keyboard events and the six form events.'),
                ('43&ndash;46', 'The submit event; the three form event interests', 'WRITE',
                 'Movement between elements, data changing, and final submission. <code>e.preventDefault()</code> is the whole trick.'),
                ('47&ndash;54', 'Validation: empty fields, multiselect, numbers, matching emails', 'WRITE',
                 'Copy each listing out. Slide 47 repeats the rule: validate on the server for security, on the client for speed and perceived responsiveness.'),
                ('55&ndash;58', 'Regular expressions: literals, metacharacters, syntax, methods', 'MEMORIZE',
                 'The fourteen metacharacters, the quantifiers, and the five methods on slide 58. Reappears in chapter 7 as Sequelize validators.'),
            ])
        },
        {
            'id': 'dom', 'nav': 'The DOM', 'label': 'Slides 3&ndash;21',
            'title': 'Finding and changing nodes',
            'html': """
<h3>Selecting elements &mdash; five methods</h3>
""" + code('selection.js', """
<span class="c">// ── the three original methods ─────────────────────────────────</span>
document.getElementById(<span class="s">"here"</span>);              <span class="c">// ONE element (ids are unique)</span>
document.getElementsByClassName(<span class="s">"thumb"</span>);     <span class="c">// an HTMLCollection</span>
document.getElementsByTagName(<span class="s">"li"</span>);          <span class="c">// an HTMLCollection</span>

<span class="c">// ── the newer query methods: you write CSS SELECTORS ───────────</span>
document.querySelector(<span class="s">"#main a"</span>);             <span class="c">// the FIRST element that matches</span>
document.querySelectorAll(<span class="s">"#menu li"</span>);         <span class="c">// a NodeList of ALL matches</span>

<span class="c">// Anything you can write in a stylesheet works here:</span>
document.querySelectorAll(<span class="s">"section &gt; p.intro:first-child"</span>);
document.querySelectorAll(<span class="s">'a[href$=".pdf"]'</span>);

<span class="c">// ── THE COLLECTION TRAP (slide 6) ──────────────────────────────
//   querySelectorAll  → NodeList      → forEach WORKS
//   getElementsBy*    → HTMLCollection → forEach DOES NOT</span>
document.querySelectorAll(<span class="s">"li"</span>).forEach(li =&gt; console.log(li.textContent));   <span class="c">// ✓</span>
document.getElementsByTagName(<span class="s">"li"</span>).forEach(...);                          <span class="c">// ✗ TypeError</span>

<span class="c">// Two ways round it:</span>
[...document.getElementsByTagName(<span class="s">"li"</span>)].forEach(li =&gt; { });   <span class="c">// spread into an array</span>
<span class="k">for</span> (<span class="k">let</span> li <span class="k">of</span> document.getElementsByTagName(<span class="s">"li"</span>)) { }       <span class="c">// for…of works on both</span>
""", note='Slides 7–8', run='i-collection-vs-node-list-165b7600') + """

<h3>Node and element properties</h3>
""" + table(['Property', 'What it gives you'], [
                ('<code>childNodes</code>', 'A NodeList of this node&rsquo;s children.'),
                ('<code>firstChild</code> &middot; <code>lastChild</code>', 'First and last child node.'),
                ('<code>nextSibling</code> &middot; <code>previousSibling</code>', 'The neighbouring nodes.'),
                ('<code>parentNode</code>', 'The parent node.'),
                ('<code>nodeName</code>', 'The name of the node &mdash; <strong>always upper case</strong> for elements.'),
                ('<code>textContent</code>', 'The text content, stripped of any tags.'),
                ('<code>classList</code>', 'A read-only list of the element&rsquo;s CSS classes, with helper methods (<code>add</code>, <code>remove</code>, <code>toggle</code>, <code>contains</code>).'),
                ('<code>className</code>', 'The raw string value of the <code>class</code> attribute.'),
                ('<code>id</code>', 'The element&rsquo;s id.'),
                ('<code>innerHTML</code>', 'All the content of the element &mdash; text <em>and</em> tags. Flagged on the slide as <strong>not secure</strong>.'),
                ('<code>style</code>', 'A <code>CSSStyleDeclaration</code> whose sub-properties map to CSS properties.'),
                ('<code>tagName</code>', 'The element&rsquo;s tag name.'),
            ]) + """
<p>Some properties exist only on certain tags: <code>href</code> on <code>&lt;a&gt;</code>;
<code>name</code> on <code>a</code>, <code>input</code>, <code>textarea</code> and <code>form</code>
only (unlike <code>id</code>, which every tag has); <code>src</code> on <code>img</code>,
<code>input</code>, <code>iframe</code> and <code>script</code>; and <code>value</code> on
<code>input</code>, <code>textarea</code> and <code>submit</code> &mdash; which is how you read what
the user typed.</p>

""" + code('accessing-elements.js', """
<span class="c">&lt;!-- given this markup --&gt;
&lt;p id="here"&gt;hello &lt;span&gt;there&lt;/span&gt;&lt;/p&gt;
&lt;ul&gt;&lt;li&gt;France&lt;/li&gt;&lt;li&gt;Spain&lt;/li&gt;&lt;li&gt;Thailand&lt;/li&gt;&lt;/ul&gt;
&lt;div id="main"&gt;
  &lt;a href="somewhere.html"&gt;&lt;img src="whatever.gif" class="thumb"&gt;&lt;/a&gt;
&lt;/div&gt;</span>

<span class="k">const</span> node = document.getElementById(<span class="s">"here"</span>);
console.log(node.innerHTML);    <span class="c">// hello &lt;span&gt;there&lt;/span&gt;   ← tags INCLUDED</span>
console.log(node.textContent);  <span class="c">// "hello there"              ← tags STRIPPED</span>

<span class="k">const</span> items = document.getElementsByTagName(<span class="s">"li"</span>);
<span class="k">for</span> (<span class="k">let</span> i = <span class="s">0</span>; i &lt; items.length; i++) console.log(items[i].textContent);
<span class="c">// France, Spain, Thailand</span>

<span class="k">const</span> link = document.querySelector(<span class="s">"#main a"</span>);
console.log(link.href);         <span class="c">// somewhere.html</span>
<span class="k">const</span> img  = document.querySelector(<span class="s">"#main img"</span>);
console.log(img.src);           <span class="c">// whatever.gif</span>
console.log(img.className);     <span class="c">// thumb</span>
""", note='Slide 11', run='iv-index-d768e469') + """

<h3>Changing appearance &mdash; three ways, in order of preference</h3>
""" + code('styling.js', """
<span class="c">// ── 1. Direct style property. Works, but sets an INLINE style.
//      Note the naming: CSS background-color → JS backgroundColor.</span>
<span class="k">const</span> node = document.getElementById(<span class="s">"someId"</span>);
node.style.backgroundColor = <span class="s">"#FFFF00"</span>;
node.style.borderWidth = <span class="s">"3px"</span>;

<span class="c">// ── 2. className — replaces the WHOLE class attribute</span>
node.className = <span class="s">"card active"</span>;

<span class="c">// ── 3. classList — PREFERRED. Surgical, and reads better.</span>
node.classList.add(<span class="s">"active"</span>);
node.classList.remove(<span class="s">"hidden"</span>);
node.classList.toggle(<span class="s">"shadow"</span>);      <span class="c">// on if off, off if on</span>
node.classList.contains(<span class="s">"active"</span>);    <span class="c">// true / false</span>

<span class="c">// WHY 3 beats 1: the styling stays in the stylesheet where it belongs,
// so you change the element's STATE and let CSS decide what that looks like.
// It is the same separation-of-concerns argument from chapter 3.</span>
""", note='Slides 12–13', run='ii-classlist-27f5e3be') + """

<h3><code>innerHTML</code> vs <code>textContent</code> vs DOM methods</h3>
""" + table(['Approach', 'Cost', 'When to use it'], [
                ('<code>innerHTML</code>', 'Every time it is set, the HTML must be <strong>parsed, a DOM constructed, and inserted</strong> into the document. This takes time. Also <strong>not secure</strong> &mdash; user-supplied text can inject markup.', 'Quick prototypes, and content you generated yourself.'),
                ('<code>textContent</code>', 'Cheap, and safe &mdash; it inserts text, never markup.', 'Any time you are inserting <em>text</em>. Should be your default.'),
                ('<code>createElement</code> + <code>appendChild</code>', 'More lines, but no reparse and no injection risk.', 'Building structure, especially inside a loop.'),
            ]) + code('three-ways.js', """
<span class="c">// The slide 15 exercise, all three ways.
// makeArticle("manager", "Director", "Salah", "Abed", "salah@abc.com")</span>

<span class="c">// ── 1. innerHTML, as a declaration ─────────────────────────────</span>
<span class="k">function</span> makeArticle(id, position, name, lastName, email) {
    document.getElementById(id).innerHTML = `
        &lt;article&gt;
            &lt;h2&gt;Position: ${position}&lt;/h2&gt;
            &lt;p&gt;Name: ${name}&lt;/p&gt;
            &lt;p&gt;Last Name: ${lastName}&lt;/p&gt;
            &lt;p&gt;Email: ${email}&lt;/p&gt;
        &lt;/article&gt;`;
}

<span class="c">// ── 2. the same thing as an ARROW function ─────────────────────</span>
<span class="k">const</span> makeArticle2 = (id, position, name, lastName, email) =&gt; {
    document.getElementById(id).innerHTML =
        `&lt;article&gt;&lt;h2&gt;Position: ${position}&lt;/h2&gt;&lt;p&gt;Name: ${name}&lt;/p&gt;` +
        `&lt;p&gt;Last Name: ${lastName}&lt;/p&gt;&lt;p&gt;Email: ${email}&lt;/p&gt;&lt;/article&gt;`;
};

<span class="c">// ── 3. as a CONSTRUCTOR with a method (chapter 4, slide 50) ────</span>
<span class="k">function</span> Employee(position, name, lastName, email) {
    <span class="k">this</span>.position = position; <span class="k">this</span>.name = name;
    <span class="k">this</span>.lastName = lastName; <span class="k">this</span>.email = email;
    <span class="k">this</span>.toHTML = <span class="k">function</span> () {
        <span class="k">return</span> `&lt;article&gt;&lt;h2&gt;Position: ${<span class="k">this</span>.position}&lt;/h2&gt;` +
               `&lt;p&gt;Name: ${<span class="k">this</span>.name}&lt;/p&gt;&lt;p&gt;Last Name: ${<span class="k">this</span>.lastName}&lt;/p&gt;` +
               `&lt;p&gt;Email: ${<span class="k">this</span>.email}&lt;/p&gt;&lt;/article&gt;`;
    };
}
document.getElementById(<span class="s">"manager"</span>).innerHTML =
    <span class="k">new</span> Employee(<span class="s">"Director"</span>, <span class="s">"Salah"</span>, <span class="s">"Abed"</span>, <span class="s">"salah@abc.com"</span>).toHTML();
""", note='Slide 15', run='chapter-5/js-front-end-all-examples/03-ex-inner-html') + """

<h3>DOM manipulation methods &mdash; the slide 20 version of the same exercise</h3>
""" + table(['Method', 'What it does'], [
                ('<code>createElement</code>', 'Creates an HTML element node.'),
                ('<code>createTextNode</code>', 'Creates a text node.'),
                ('<code>appendChild</code>', 'Adds a new child node to the <strong>end</strong> of the current node.'),
                ('<code>insertAdjacentElement</code>', 'Inserts a new child node at one of four positions relative to the current node.'),
                ('<code>insertAdjacentText</code>', 'The same, for a text node.'),
                ('<code>removeChild</code>', 'Removes a child from the current node.'),
                ('<code>replaceChild</code>', 'Replaces a child node with a different one.'),
            ]) + code('dom-manipulation.js', """
<span class="c">// The four insertAdjacent* positions:
//   &lt;!-- beforebegin --&gt;
//   &lt;p&gt;
//     &lt;!-- afterbegin --&gt;   foo   &lt;!-- beforeend --&gt;
//   &lt;/p&gt;
//   &lt;!-- afterend --&gt;</span>

<span class="c">// The slide 20 exercise: makeArticle with DOM methods instead of innerHTML.
// More lines, but no reparse and nothing can be injected.</span>
<span class="k">function</span> makeArticleDOM(id, position, name, lastName, email) {
    <span class="k">const</span> target  = document.getElementById(id);
    <span class="k">const</span> article = document.createElement(<span class="s">"article"</span>);

    <span class="k">const</span> h2 = document.createElement(<span class="s">"h2"</span>);
    h2.textContent = `Position: ${position}`;         <span class="c">// textContent, not innerHTML</span>
    article.appendChild(h2);

    [[<span class="s">"Name"</span>, name], [<span class="s">"Last Name"</span>, lastName], [<span class="s">"Email"</span>, email]]
        .forEach(([label, val]) =&gt; {
            <span class="k">const</span> p = document.createElement(<span class="s">"p"</span>);
            p.appendChild(document.createTextNode(`${label}: ${val}`));
            article.appendChild(p);
        });

    target.replaceChildren(article);   <span class="c">// or: target.innerHTML = ""; target.appendChild(article);</span>
}
""", note='Slides 17–20') + """

<h3>The dataset property</h3>
""" + code('dataset.html', """
<span class="c">&lt;!-- Custom data-* attributes let you attach data to an element --&gt;</span>
<span class="k">&lt;div</span> <span class="t">id</span>=<span class="s">"container"</span> <span class="t">data-userid</span>=<span class="s">"2356"</span> <span class="t">data-user-name</span>=<span class="s">"Salah"</span><span class="k">&gt;</span>
  <span class="k">&lt;p</span> <span class="t">id</span>=<span class="s">"display"</span><span class="k">&gt;</span>The user ID is:<span class="k">&lt;/p&gt;</span>
<span class="k">&lt;/div&gt;</span>

<span class="k">&lt;script&gt;</span>
<span class="k">const</span> container = document.getElementById(<span class="s">"container"</span>);
<span class="k">const</span> user_id   = container.dataset.userid;    <span class="c">// data-userid    → userid</span>
<span class="k">const</span> user_name = container.dataset.userName;  <span class="c">// data-user-NAME → userName  ← camelCase!</span>

container.appendChild(document.createTextNode(`User info: ${user_id}, ${user_name}`));
<span class="k">&lt;/script&gt;</span>

<span class="c">// NAMING RULE: hyphens in the attribute become camelCase in dataset.
// data-user-name → dataset.userName. Getting this wrong gives undefined
// with no error, which makes it a nasty bug to find.</span>
""", note='Slide 21', run='chapter-5/js-front-end-all-examples/05-dataset')
        },
        {
            'id': 'events', 'nav': 'Events', 'label': 'Slides 22&ndash;42',
            'title': 'Event handling, timing, propagation and delegation',
            'html': """
<h3>Timing &mdash; read this before anything else breaks</h3>
<p>Slide 23 states it plainly: <strong>you cannot access or modify the DOM until it has been
loaded.</strong> Putting your script after the markup is one way to be sure the elements exist. The
robust way is to wait for an event.</p>
""" + table(['Event', 'Fires when', 'Use it?'], [
                ('<code>window.load</code>', 'The <strong>entire</strong> page has loaded, including images and stylesheets. On a slow connection or an image-heavy page this can take a long time.', 'Only when you genuinely need images measured.'),
                ('<code>document.DOMContentLoaded</code>', 'The HTML document has been completely <strong>downloaded and parsed</strong>.', '<strong>Generally the one you want.</strong>'),
            ]) + code('dom-timing.js', """
<span class="c">// With one of these, your DOM code can live ANYWHERE — even in &lt;head&gt; —
// as long as it does not touch the DOM outside the handler.</span>
document.addEventListener(<span class="s">'DOMContentLoaded'</span>, <span class="k">function</span> () {

    <span class="k">const</span> menu = document.querySelectorAll(<span class="s">"#menu li"</span>);
    <span class="k">for</span> (<span class="k">let</span> item <span class="k">of</span> menu) {
        item.addEventListener(<span class="s">"click"</span>, <span class="k">function</span> () {
            item.classList.toggle(<span class="s">'shadow'</span>);
        });
    }

    <span class="k">const</span> heading = document.querySelector(<span class="s">"h3"</span>);
    heading.addEventListener(<span class="s">'click'</span>, <span class="k">function</span> () {
        heading.classList.toggle(<span class="s">'shadow'</span>);
    });
});
""", note='Slides 28–29', run='chapter-5/js-front-end-all-examples/06-eventwindows') + hook(
                "<strong>Diagnostic worth memorising:</strong> if a selector returns <code>null</code> "
                "and the element is definitely in the HTML, it is a timing problem, not a typo. Your "
                "script ran before the parser reached that element.") + """

<h3>Registering a handler</h3>
""" + code('handlers.js', """
<span class="c">// Define a handler, then REGISTER it on an element node by passing
// the callback to addEventListener().</span>
<span class="k">function</span> named() { alert(<span class="s">"a named handler"</span>); }
document.getElementById(<span class="s">"btn"</span>).addEventListener(<span class="s">"click"</span>, named);
<span class="c">//                                                        ↑ NO parentheses.
//   named   passes the function.   named()  CALLS it and passes the result.</span>

<span class="c">// Far more common: an ANONYMOUS function. Three equivalent versions:</span>
<span class="k">const</span> btn = document.getElementById(<span class="s">"btn"</span>);
btn.addEventListener(<span class="s">"click"</span>, <span class="k">function</span> () { alert(<span class="s">"anonymous function"</span>); });

document.querySelector(<span class="s">"#btn"</span>).addEventListener(<span class="s">"click"</span>, <span class="k">function</span> () {
    alert(<span class="s">"a different approach, same result"</span>);
});

document.querySelector(<span class="s">"#btn"</span>).addEventListener(<span class="s">"click"</span>, () =&gt; {
    alert(<span class="s">"arrow syntax, same result"</span>);
});

<span class="c">// THE EVENT OBJECT: add a parameter (conventionally e) and the browser
// hands you an object describing what happened.</span>
btn.addEventListener(<span class="s">"click"</span>, <span class="k">function</span> (e) {
    console.log(e.type);           <span class="c">// "click"</span>
    console.log(e.target);         <span class="c">// the element that GENERATED the event</span>
    console.log(e.currentTarget);  <span class="c">// the element the handler is ATTACHED to</span>
});
""", note='Slides 24–26, 30–31', run='chapter-5/js-front-end-all-examples/07-event-handler') + """

<h3>Propagation: capturing and bubbling</h3>
<p>When an event fires on an element that has ancestors, it propagates to those ancestors in
<strong>two phases</strong>.</p>
""" + code('propagation', """
<span class="c">   &lt;html&gt;
     &lt;aside id="cart"&gt;
       &lt;div class="item"&gt;
         &lt;button class="plus"&gt;+&lt;/button&gt;   ← you click HERE (the event TARGET)
       &lt;/div&gt;
     &lt;/aside&gt;
   &lt;/html&gt;

   ① CAPTURING PHASE  — outermost inward
        html → aside → div → button
        The browser checks each ancestor starting from the OUTERMOST
        (&lt;html&gt;) and runs any handler registered FOR THIS PHASE,
        until it reaches the element that triggered the event.

   ② BUBBLING PHASE   — target outward   ← THE DEFAULT
        button → div → aside → html
        The opposite: it checks the triggering element first, then
        works back out through every ancestor.</span>

<span class="c">// addEventListener's third argument picks the phase:</span>
el.addEventListener(<span class="s">"click"</span>, handler);          <span class="c">// bubbling  (default)</span>
el.addEventListener(<span class="s">"click"</span>, handler, <span class="k">true</span>);    <span class="c">// capturing</span>
""", note='Slides 32–33', run='event-propagation-0aa36bf7') + code('stop-propagation.js', """
<span class="c">// THE PROBLEM (slide 34): nested elements each with their own click
// behaviour. Clicking the increment button fires the button's handler —
// and then the div's, and then the aside's. The cart minimises itself
// every time you add an item.</span>

<span class="c">// THE FIX: e.stopPropagation()</span>
<span class="k">const</span> btns = document.querySelectorAll(<span class="s">".plus"</span>);
<span class="k">for</span> (<span class="k">let</span> b <span class="k">of</span> btns) {
    b.addEventListener(<span class="s">"click"</span>, <span class="k">function</span> (e) {
        e.stopPropagation();       <span class="c">// ← the event stops here</span>
        incrementCount(e);
    });
}

<span class="k">const</span> items = document.querySelectorAll(<span class="s">".item"</span>);
<span class="k">for</span> (<span class="k">let</span> it <span class="k">of</span> items) {
    it.addEventListener(<span class="s">"click"</span>, <span class="k">function</span> (e) {
        e.stopPropagation();
        removeItemFromCart(e);
    });
}

<span class="k">const</span> aside = document.querySelector(<span class="s">"aside#cart"</span>);
aside.addEventListener(<span class="s">"click"</span>, <span class="k">function</span> () { minimizeCart(); });

<span class="c">// DO NOT CONFUSE THESE TWO:
//   e.stopPropagation()  stops the event travelling to other ELEMENTS
//   e.preventDefault()   stops the BROWSER's default action (submitting,
//                        following a link). They are unrelated.</span>
""", note='Slides 34–35', run='chapter-5/js-front-end-all-examples/08-eventprop') + """

<h3>Event delegation &mdash; bubbling used deliberately</h3>
""" + code('event-delegation.js', """
<span class="c">// THE NAIVE WAY: one listener per element. With 200 thumbnails that is
// 200 listeners — and any image added later has none at all.</span>
<span class="k">const</span> images = document.querySelectorAll(<span class="s">"#list img"</span>);
<span class="k">for</span> (<span class="k">let</span> img <span class="k">of</span> images) {
    img.addEventListener(<span class="s">"click"</span>, someHandler);
}

<span class="c">// DELEGATION: ONE listener on the parent, using bubbling. Since the user
// can click on any element inside the section, the handler must work out
// whether an &lt;img&gt; was clicked.</span>
<span class="k">const</span> parent = document.querySelector(<span class="s">"#list"</span>);
parent.addEventListener(<span class="s">"click"</span>, <span class="k">function</span> (e) {
    <span class="c">// e.target is the object that GENERATED the event.
    // NOTE: nodeName ALWAYS RETURNS UPPER CASE.</span>
    <span class="k">if</span> (e.target &amp;&amp; e.target.nodeName === <span class="s">"IMG"</span>) {
        doSomething(e.target);
    }
});

<span class="c">// Two wins: one listener instead of hundreds, and elements added to the
// list LATER are handled automatically — no re-registration needed.</span>
""", note='Slides 36–38', run='chapter-5/js-front-end-all-examples/08b-event-delegation') + """

<h3>Event types</h3>
<p>Five categories: <strong>mouse</strong>, <strong>keyboard</strong>, <strong>touch</strong>,
<strong>form</strong> and <strong>frame</strong> events.</p>
""" + table(['Mouse (slide 40)', 'Keyboard (41)', 'Form (42)'], [
                ('<code>click</code> &mdash; clicked on an element', '<code>keydown</code> &mdash; a key is being pressed (<strong>first</strong>)', '<code>focus</code> &mdash; an element gains focus'),
                ('<code>dblclick</code> &mdash; double clicked', '<code>keyup</code> &mdash; a key is released (<strong>last</strong>)', '<code>blur</code> &mdash; an element lost focus, by click or Tab'),
                ('<code>mousedown</code> &mdash; pressed down over an element', '<code>e.key</code> gives the key pressed', '<code>change</code> &mdash; an input, textarea or select had its value changed'),
                ('<code>mouseup</code> &mdash; released over an element', '', '<code>select</code> &mdash; the user selected some text'),
                ('<code>mouseover</code> &mdash; moved (not clicked) over an element', '', '<code>reset</code> &mdash; the form was reset'),
                ('<code>mouseout</code> &mdash; moved off an element', '', '<code>submit</code> &mdash; the form was submitted'),
                ('<code>mousemove</code> &mdash; moved while over an element', '', ''),
            ]) + code('key-event.js', """
document.getElementById(<span class="s">"pagebody"</span>).addEventListener(<span class="s">"keydown"</span>, <span class="k">function</span> (e) {
    <span class="k">let</span> keyPressed = e.key;
    alert(<span class="s">"Key "</span> + keyPressed + <span class="s">" was pressed"</span>);
});
""", note='Slide 41', run='key-event-0e280756') + """
<p>Slide 40 also sets a practice task: build a board game where tiles change colour on a mouse event.
The worked version is in your study material as
<a href="/academics/software-engineering/se371/extra-resources/chapter-5/js-front-end-all-examples/09-tiles-game/" target="_blank" rel="noopener">09-tiles-game</a>.</p>
"""
        },
        {
            'id': 'forms', 'nav': 'Forms &amp; Regex', 'label': 'Slides 43&ndash;58',
            'title': 'Form validation and regular expressions',
            'html': """
<p>Slide 44 frames it: with forms in JavaScript you care about three kinds of event &mdash;
<strong>movement between elements</strong>, <strong>data being changed</strong>, and <strong>the final
submission</strong>. And slide 47 restates the rule from chapter 2: validation <em>must</em> happen on
the server for security, in case JavaScript was circumvented; doing it on the client as well
<strong>reduces server load and increases the perceived speed and responsiveness</strong> of the form.</p>

<h3><code>preventDefault</code> &mdash; the single most useful line in the chapter</h3>
""" + code('submit-validation.js', """
<span class="c">// Slide 43: block submission when the password is empty</span>
document.querySelector(<span class="s">"#loginForm"</span>).addEventListener(<span class="s">"submit"</span>, <span class="k">function</span> (e) {
    <span class="k">let</span> pass = document.querySelector(<span class="s">"#pw"</span>).value;
    <span class="k">if</span> (pass == <span class="s">""</span>) {
        alert(<span class="s">"enter a password"</span>);
        e.preventDefault();          <span class="c">// ← prevents form submission</span>
    }
});

<span class="c">// Slide 48: the same pattern, with an arrow function</span>
<span class="k">const</span> form = document.querySelector(<span class="s">"#loginForm"</span>);
form.addEventListener(<span class="s">"submit"</span>, (e) =&gt; {
    <span class="k">const</span> fieldValue = document.querySelector(<span class="s">"#username"</span>).value;
    <span class="k">if</span> (fieldValue == <span class="k">null</span> || fieldValue == <span class="s">""</span>) {
        e.preventDefault();          <span class="c">// stop the submission FIRST</span>
        console.log(<span class="s">"you must enter a username"</span>);   <span class="c">// then tell the user</span>
    }
});

<span class="c">// To submit a form FROM JavaScript — often paired with preventDefault:</span>
<span class="k">const</span> formExample = document.getElementById(<span class="s">"loginForm"</span>);
formExample.submit();
""", note='Slides 43, 48, 52', run='chapter-5/js-front-end-all-examples/10b-form-submit-event') + """

<h3>Reading a multiselect list</h3>
""" + code('multiselect.js', """
<span class="k">const</span> multi = document.querySelector(<span class="s">"#listbox"</span>);

<span class="c">// Technique 1: loop EVERY option and test .selected</span>
<span class="k">for</span> (<span class="k">let</span> i = <span class="s">0</span>; i &lt; multi.options.length; i++) {
    <span class="k">if</span> (multi.options[i].selected) {
        console.log(multi.options[i].textContent);
    }
}

<span class="c">// Technique 2: SIMPLER — selectedOptions only contains the chosen ones</span>
<span class="k">for</span> (<span class="k">let</span> i = <span class="s">0</span>; i &lt; multi.selectedOptions.length; i++) {
    console.log(multi.selectedOptions[i].textContent);
}
""", note='Slide 49', run='chapter-5/js-front-end-all-examples/11-multiselect-validation') + """

<h3>Number validation, and the HTML5 validity object</h3>
""" + code('number-validation.js', """
<span class="c">// No simple built-in exists. Build one from parseFloat, isNaN and isFinite.</span>
<span class="k">function</span> isNumeric(n) {
    <span class="k">return</span> !isNaN(parseFloat(n)) &amp;&amp; isFinite(n);
}
<span class="c">// You need BOTH: 1/0 is Infinity, which isNaN() considers a number.</span>

isNumeric(<span class="s">"42"</span>);       <span class="c">// true</span>
isNumeric(<span class="s">"abc"</span>);      <span class="c">// false — parseFloat gives NaN</span>
isNumeric(<span class="s">1</span>/<span class="s">0</span>);        <span class="c">// false — Infinity is not finite</span>

<span class="c">// You can also read the browser's own verdict via the validity object.
// Slide 50: some browsers may not support HTML5 validation, and you want
// more control over how you react to bad input — so prefer JS validation.</span>
<span class="k">function</span> validateTextA() {
    <span class="k">let</span> value = <span class="s">""</span>;
    <span class="k">if</span> (document.getElementById(<span class="s">"textA"</span>).validity.rangeOverflow) {
        value = <span class="s">"The value must not be greater than 100"</span>;
    }
    document.getElementById(<span class="s">"output"</span>).innerHTML = value;
}
<span class="c">// other validity flags: valueMissing, typeMismatch, patternMismatch,
// rangeUnderflow, tooLong, stepMismatch</span>
""", note='Slides 50–51') + """

<h3>Comparison validation &mdash; and the mistake slides 53&ndash;54 walk you through</h3>
""" + code('matching-emails.js', """
<span class="c">// SLIDE 53 — first attempt. onchange fires when you leave the field,
// so the user is warned early. BUT the form can still be submitted:
// nothing blocks the request.</span>
<span class="k">function</span> check(e) {
    <span class="k">var</span> email1 = document.getElementById(<span class="s">'email_addr'</span>);
    <span class="k">var</span> email2 = document.getElementById(<span class="s">'email_repeat'</span>);
    <span class="k">if</span> (email1.value !== email2.value) {
        e.preventDefault();
        alert(<span class="s">"The two emails have to match"</span>);
    }
}

<span class="c">// SLIDE 54 — the fix is a SECOND check that blocks the HTTP request,
// wired to the submit button as well as to onchange.</span>
<span class="c">//   &lt;input type="email" id="email_repeat" name="email2" required onchange="check(e)"&gt;
//   &lt;input type="submit" value="Send" onclick="check(e);"&gt;</span>

<span class="c">// CLEANER — one handler on the form's submit event, no inline attributes:</span>
document.querySelector(<span class="s">"form"</span>).addEventListener(<span class="s">"submit"</span>, <span class="k">function</span> (e) {
    <span class="k">const</span> a = document.getElementById(<span class="s">'email_addr'</span>).value;
    <span class="k">const</span> b = document.getElementById(<span class="s">'email_repeat'</span>).value;
    <span class="k">if</span> (a !== b) {
        e.preventDefault();
        alert(<span class="s">"The two emails have to match"</span>);
    }
});
""", note='Slides 53–54') + """

<h3>Regular expressions</h3>
<p>A regular expression is a set of special characters defining a pattern, built from two kinds of
character: <strong>literals</strong> (a character you want to match in the target text) and
<strong>metacharacters</strong> (a symbol that commands the parser). There are fourteen
metacharacters:</p>
""" + code('regex.js', """
<span class="c">// THE FOURTEEN METACHARACTERS:    . [ ] \\ ( ) ^ $ | * ? { } +</span>

<span class="c">// In JavaScript a regex is CASE SENSITIVE and lives between forward slashes.</span>
<span class="k">let</span> pattern = /ala/;
<span class="c">// matches inside:  'Salah Althobeiti'   and   'Al malaz district'</span>

<span class="s">"Salah Althobeiti"</span>.match(/ala/);      <span class="c">// matched text, or null</span>
/ala/.test(<span class="s">"Salah Althobeiti"</span>);       <span class="c">// true / false</span>

<span class="c">// ── CHARACTER CLASSES (slide 57, left) ─────────────────────────
//   [abc]      any one of a, b or c
//   [^abc]     any character EXCEPT a, b or c
//   [a-z]      any lower-case letter
//   [A-Z]      any upper-case letter
//   [a-zA-Z]   any letter
//   [0-9]      any digit</span>

<span class="c">// ── QUANTIFIERS AND ANCHORS (slide 57, right) ──────────────────
//   a?         0 or 1 times
//   a+         1 or more times
//   a*         0 or more times
//   a{n}       exactly n times
//   a{n,}      n or more times
//   a{x,y}     at least x, at most y times
//   ^a         STARTS with a
//   a$         ENDS with a
//   (?=ae)     any string FOLLOWED BY "ae"      (lookahead)
//   (?!ae)     any string NOT followed by "ae"  (negative lookahead)</span>

<span class="c">// ── /pattern/modifier ──────────────────────────────────────────
//   /[a-z][0-9]/ig     i = case-insensitive,  g = global (all matches)</span>

<span class="c">// ── THE FIVE METHODS (slide 58) ────────────────────────────────</span>
pattern.exec(text);                <span class="c">// 1. matched text, or null</span>
pattern.test(text);                <span class="c">// 2. true or false</span>
text.match(pattern);               <span class="c">// 3. matched text or null; ALL matches with /g</span>
text.search(pattern);              <span class="c">// 4. the INDEX of the match</span>
text.replace(pattern, <span class="s">"newvalue"</span>);  <span class="c">// 5. a new string with replacements</span>

<span class="c">// The slide's own phone-number example, as an HTML5 pattern attribute:
//   &lt;input pattern="[+]?[0-9]{10,14}"&gt;
//   optional +, then 10 to 14 digits</span>

<span class="c">// Practical validators built the same way:</span>
<span class="k">const</span> saudiMobile = /^05[0-9]{8}$/;                <span class="c">// exactly 05 + 8 digits</span>
<span class="k">const</span> simpleEmail = /^[^@\\s]+@[^@\\s]+\\.[a-z]{2,}$/i;
""", note='Slides 55–58') + hook(
                "<strong>Which regex method?</strong> Just need yes or no &rarr; <code>test()</code>. "
                "Need the matched text &rarr; <code>match()</code>. Need where it is &rarr; "
                "<code>search()</code>. Need to change it &rarr; <code>replace()</code>. "
                "For validation you almost always want <code>test()</code>, and you almost always want "
                "<code>^</code> and <code>$</code> so the pattern must match the <em>whole</em> value.")
        },
        {
            'id': 'traps', 'nav': 'Traps', 'label': 'Marks Lost Here',
            'title': 'The eight things people get wrong',
            'html': (
                trap('Running DOM code before the DOM exists',
                     'A <code>querySelector</code> returns <code>null</code> and the next line throws "cannot read property of null" &mdash; but the element is right there in the HTML. The script simply ran before the parser reached it.',
                     'Wrap the code in <code>document.addEventListener(\'DOMContentLoaded\', ...)</code>, or put the script at the end of <code>&lt;body&gt;</code>. Use <code>DOMContentLoaded</code> rather than <code>window.load</code> &mdash; the latter also waits for every image.') +
                trap('Confusing <code>stopPropagation</code> with <code>preventDefault</code>',
                     'They sound similar and do unrelated things. Calling <code>stopPropagation()</code> in a submit handler will not stop the form submitting, and <code>preventDefault()</code> will not stop the parent&rsquo;s click handler firing.',
                     '<code>stopPropagation()</code> stops the event reaching other <em>elements</em>. <code>preventDefault()</code> stops the <em>browser</em> doing its default thing &mdash; submitting, following a link, checking a box.') +
                trap('Calling the handler instead of passing it',
                     '<code>btn.addEventListener("click", myHandler())</code> runs <code>myHandler</code> immediately, at registration time, and then registers whatever it <em>returned</em> &mdash; usually <code>undefined</code>.',
                     'Pass the function, do not call it: <code>addEventListener("click", myHandler)</code>. No parentheses.') +
                trap('<code>forEach</code> on the result of <code>getElementsBy*</code>',
                     'Those methods return an <strong>HTMLCollection</strong>, not a NodeList, and slide 6 notes the difference explicitly: <code>forEach</code> works on a NodeList, not on an HTMLCollection.',
                     'Use <code>querySelectorAll</code> (which returns a NodeList), or spread the collection into an array with <code>[...collection]</code>, or just use <code>for…of</code> &mdash; which works on both.') +
                trap('Case-sensitive <code>nodeName</code> in delegation',
                     '<code>if (e.target.nodeName === "img")</code> is silently never true. The slide warns about this in the code comment: <strong>nodeName always returns upper case.</strong>',
                     'Compare against <code>"IMG"</code>, or use <code>e.target.matches("img")</code> which takes a CSS selector and is case-insensitive.') +
                trap('Building markup in a loop with <code>innerHTML</code>',
                     'Setting <code>innerHTML</code> inside a loop re-parses the HTML and rebuilds a DOM on every iteration. Slide 14 explains exactly this cost. It also opens an injection hole if any of the values came from a user.',
                     'Build the string once and assign at the end, or use <code>createElement</code> + <code>appendChild</code>. Use <code>textContent</code> for anything that is only text.') +
                trap('Wrong dataset name',
                     '<code>data-user-name</code> is <strong>not</strong> <code>dataset.user-name</code> or <code>dataset.username</code> &mdash; it is <code>dataset.userName</code>. The wrong name gives <code>undefined</code> silently.',
                     'Hyphens become camelCase. <code>data-user-name</code> &rarr; <code>userName</code>; single-word <code>data-userid</code> stays <code>userid</code>.') +
                trap('Believing client-side validation is enough',
                     'The third time this appears in the course, because it is the point that most often loses marks. Slide 47 spells out the reasoning: check on the server for security, <em>in case JavaScript was circumvented</em>.',
                     'Client-side validation buys you reduced server load and perceived responsiveness. Server-side validation buys you correctness. You need both, and only one of them is optional.')
            )
        },
        {
            'id': 'cheat', 'nav': 'Cheat Sheet', 'label': 'One Screen',
            'title': 'Chapter 5 on a single screen',
            'html': cheat([
                ('Selecting', [
                    '<code>getElementById("id")</code>',
                    '<code>getElementsByClassName()</code> &rarr; HTMLCollection',
                    '<code>getElementsByTagName()</code> &rarr; HTMLCollection',
                    '<code>querySelector(css)</code> &rarr; first match',
                    '<code>querySelectorAll(css)</code> &rarr; NodeList',
                    'forEach: NodeList yes, HTMLCollection no',
                ]),
                ('Reading &amp; writing', [
                    '<code>.textContent</code> &mdash; text, tags stripped',
                    '<code>.innerHTML</code> &mdash; text + tags, reparses, unsafe',
                    '<code>.value</code> &mdash; what the user typed',
                    '<code>.classList.add/remove/toggle/contains</code>',
                    '<code>.style.backgroundColor</code> (camelCase)',
                    '<code>.dataset.userName</code> &larr; <code>data-user-name</code>',
                ]),
                ('Building', [
                    '<code>createElement("p")</code>',
                    '<code>createTextNode("hi")</code>',
                    '<code>appendChild(node)</code>',
                    '<code>insertAdjacentElement/Text</code>',
                    '<code>removeChild</code> &middot; <code>replaceChild</code>',
                ]),
                ('Events', [
                    '<code>el.addEventListener("click", fn)</code>',
                    'Pass <code>fn</code>, never <code>fn()</code>',
                    '<code>e.target</code> &mdash; what generated it',
                    '<code>e.currentTarget</code> &mdash; where the handler is',
                    '<code>e.key</code> &mdash; the key pressed',
                ]),
                ('Timing', [
                    '<code>DOMContentLoaded</code> &mdash; HTML parsed. <strong>Use this.</strong>',
                    '<code>window.load</code> &mdash; images and CSS too',
                    'Or put the script at the end of <code>&lt;body&gt;</code>',
                ]),
                ('Propagation', [
                    '① capturing: <code>html</code> &rarr; target',
                    '② bubbling: target &rarr; <code>html</code> (default)',
                    '<code>e.stopPropagation()</code> &mdash; stop travelling',
                    '<code>e.preventDefault()</code> &mdash; stop the browser',
                    'Delegation: one listener on the parent + <code>e.target</code>',
                ]),
                ('Event types', [
                    'Mouse: <code>click dblclick mousedown mouseup</code>',
                    '<code>mouseover mouseout mousemove</code>',
                    'Keyboard: <code>keydown</code> then <code>keyup</code>',
                    'Form: <code>focus blur change select reset submit</code>',
                ]),
                ('Regex', [
                    'Metacharacters: <code>. [ ] \\ ( ) ^ $ | * ? { } +</code>',
                    '<code>[a-z] [A-Z] [0-9] [^abc]</code>',
                    '<code>? + *</code> &middot; <code>{n} {n,} {x,y}</code>',
                    '<code>^</code> starts &middot; <code>$</code> ends',
                    '<code>/pattern/ig</code>',
                    '<code>test exec match search replace</code>',
                ]),
            ])
        },
        {
            'id': 'drills', 'nav': 'Drills', 'label': 'Type It Blind',
            'title': 'Build these with the browser open',
            'html': """
<p>Every one of these takes under ten minutes and each corresponds to a real slide. The DevTools
console is the tool for this chapter &mdash; select things, poke at them, watch what changes.</p>
""" + drills([
                'Select the same element five ways: by id, by class, by tag, and with both query methods.',
                'Prove the collection trap to yourself: call <code>forEach</code> on the result of <code>querySelectorAll</code> and on <code>getElementsByTagName</code>, and read the error.',
                'Log the same element&rsquo;s <code>innerHTML</code> and <code>textContent</code> side by side and explain the difference in one sentence.',
                'Change one element&rsquo;s appearance three ways: <code>style</code>, <code>className</code> and <code>classList.toggle</code>. Say why the third is preferred.',
                'Write the slide 15 <code>makeArticle</code> function with <code>innerHTML</code>, then as an arrow function, then as a constructor with a method.',
                'Rewrite it again with <code>createElement</code> and <code>appendChild</code> only &mdash; the slide 20 version.',
                'Put three <code>data-*</code> attributes on an element, including a hyphenated one, and read all three through <code>dataset</code>.',
                'Break your own page: put a <code>querySelector</code> in <code>&lt;head&gt;</code> with no wrapper, read the error, then fix it with <code>DOMContentLoaded</code>.',
                'Nest a button inside a div inside an aside, give each a click handler that logs its name, and click the button. Write down the order before you run it.',
                'Add <code>true</code> as the third argument to one of those listeners and observe the order change.',
                'Add <code>stopPropagation()</code> to the innermost handler and watch the other two go quiet.',
                'Replace ten per-image listeners with one delegated listener on the parent, using <code>e.target.nodeName</code>.',
                'Write a submit handler that blocks submission when a field is empty, then delete <code>preventDefault()</code> and watch the page navigate away.',
                'Read every selected option out of a multiselect, both ways from slide 49.',
                'Write <code>isNumeric</code> from memory and test it with <code>"42"</code>, <code>"abc"</code> and <code>1/0</code>.',
                'Write regular expressions for: a Saudi mobile number, a string of exactly four digits, and a string that starts with a capital letter.',
                'Test each of those three with all five regex methods and note what each returns.',
            ]) + """
<p>The complete example set is at
<a href="/academics/software-engineering/se371/extra-resources/chapter-5/js-front-end-all-examples/" target="_blank" rel="noopener">chapter-5/js-front-end-all-examples/</a>,
including the <a href="/academics/software-engineering/se371/extra-resources/resource-viewers/event-propagation-0aa36bf7/" target="_blank" rel="noopener">event propagation demo</a>
and the tiles game from the slide 40 practice task.</p>
"""
        },
    ],
    'quiz': [
        {'tag': 'Timing', 'q': 'A script in <head> does document.querySelector("#box") and gets null, but #box is definitely in the HTML. Why?',
         'opts': ['The selector syntax is wrong for ids',
                  'The script ran before the parser reached that element',
                  'querySelector cannot select by id',
                  'The element needs a class as well as an id'],
         'a': 1,
         'why': 'You cannot access the DOM until it has loaded. Wrap the code in a DOMContentLoaded handler, or move the script to the end of body.'},
        {'tag': 'Events', 'q': 'What is the difference between e.stopPropagation() and e.preventDefault()?',
         'opts': ['They are aliases for the same thing',
                  'stopPropagation stops the event reaching other elements; preventDefault stops the browser default action',
                  'preventDefault works on forms only; stopPropagation works everywhere',
                  'stopPropagation cancels the event entirely, preventDefault only delays it'],
         'a': 1,
         'why': 'They are unrelated. stopPropagation halts travel through the element tree; preventDefault cancels the browser behaviour such as submitting a form or following a link.'},
        {'tag': 'Propagation', 'q': 'In which order does the capturing phase visit elements?',
         'opts': ['From the target outward to <html>', 'From <html> inward to the target',
                  'Only the target, then it stops', 'In document source order'],
         'a': 1,
         'why': 'Capturing runs outermost inward — the browser checks <html> first and works down to the element that triggered the event. Bubbling is the opposite and is the default phase.'},
        {'tag': 'DOM', 'q': 'Why do the slides prefer classList over setting .style properties directly?',
         'opts': ['classList is faster to execute',
                  'style properties do not work on all browsers',
                  'It keeps the appearance in the stylesheet and changes only the element state',
                  'style can only set one property at a time'],
         'a': 2,
         'why': 'Slide 13 says it is preferable to change appearance through className or classList. Your JavaScript changes the element state and CSS decides what that state looks like — the same separation of concerns as chapter 3.'},
        {'tag': 'Collections', 'q': 'Why does forEach fail on the result of getElementsByTagName?',
         'opts': ['It returns a plain array with no methods',
                  'It returns an HTMLCollection, and forEach exists on NodeList only',
                  'The collection is empty until the page loads',
                  'forEach requires an arrow function'],
         'a': 1,
         'why': 'Slide 6 notes it directly. querySelectorAll returns a NodeList which has forEach; getElementsBy* returns an HTMLCollection which does not. Spread it into an array or use for…of.'},
        {'tag': 'Delegation', 'q': 'In a delegated handler, why does if (e.target.nodeName === "img") never match?',
         'opts': ['e.target is always the parent element', 'nodeName always returns upper case',
                  'nodeName returns the id, not the tag', 'Images do not bubble click events'],
         'a': 1,
         'why': 'The slide 38 code comment warns about it explicitly. Compare against "IMG", or use e.target.matches("img") which takes a CSS selector.'},
        {'tag': 'Forms', 'q': 'Which event fires when a select or input has its value changed by the user?',
         'opts': ['<code>focus</code>', '<code>blur</code>', '<code>change</code>', '<code>select</code>'],
         'a': 2,
         'why': 'change fires when an input, textarea or select had its value changed. focus and blur are about gaining and losing focus, and select fires when the user selects some text.'},
        {'tag': 'Regex', 'q': 'What does the pattern /^05[0-9]{8}$/ match?',
         'opts': ['Any string containing 05 followed by digits',
                  'A string that is exactly 05 followed by exactly eight digits',
                  'A string starting with 0 or 5', 'Between 0 and 5 repeated eight times'],
         'a': 1,
         'why': '^ anchors the start and $ anchors the end, so the whole string must match. {8} means exactly eight, and [0-9] is any digit. Without ^ and $ it would match anywhere inside a longer string.'},
    ],
})


# ═══════════════════════════════════════════════════════════════════════════ #
# CHAPTER 06 — Server-Side: Node.js and Express
# ═══════════════════════════════════════════════════════════════════════════ #

CHAPTERS.append({
    'num': 6,
    'slug': '06-server-side-node',
    'file': 'server-side-node.html',
    'title': 'Server-Side: Node.js and Express',
    'desc': ('Slide-by-slide breakdown of SE371 Chapter 6 — Node modules, the fs and http modules, '
             'blocking vs non-blocking architecture, callbacks, promises, fetch, CORS, npm, Express '
             'routing, middleware and EJS templates.'),
    'sub': ('JavaScript moves to the server. This is the chapter where the course stops being about '
            'pages and starts being about applications — and where asynchronous code stops being '
            'optional. Everything in chapter 7 is built on top of the Express app you write here.'),
    'stats': ['51 slides', 'Single deck', 'Pure write-it', 'Book ch. 13'],
    'sections': [
        {
            'id': 'orient', 'nav': 'Start Here', 'label': 'Orientation',
            'title': 'What this chapter is really for',
            'html': """
<p>Slide 1 is a leftover chapter 5 task (make a table appear when a heading is clicked using DOM
manipulation) &mdash; do it, then start here.</p>

<p>The deck moves through four stages, and each one exists because the previous one hit a wall:</p>
<ol>
  <li><strong>Node basics</strong> (3&ndash;14) &mdash; modules, <code>fs</code>, <code>http</code>. You build a server by hand and immediately see how tedious routing is.</li>
  <li><strong>Async</strong> (15&ndash;28) &mdash; why Node is non-blocking, callback hell, promises, <code>fetch</code>. Because the raw callbacks in stage 1 do not scale.</li>
  <li><strong>npm and Express</strong> (29&ndash;45) &mdash; packages, middleware, routing, three ways to receive parameters. Because hand-written routing does not scale either.</li>
  <li><strong>EJS</strong> (46&ndash;50) &mdash; generating HTML from data on the server.</li>
</ol>

<div class="grid-2">
  <div class="card">
    <h4>The idea that makes Node make sense</h4>
    <p>Node is <strong>non-blocking, asynchronous and single-threaded</strong>. One worker services
    every request in one event loop, delegating slow work to other agents. That single sentence
    explains the advantages, the disadvantages, and why every file operation takes a callback.</p>
  </div>
  <div class="card">
    <h4>Where it connects</h4>
    <p>Chapter 1&rsquo;s HTTP methods and ports become <code>app.get</code> and
    <code>app.listen</code>. Chapter 2&rsquo;s form <code>action</code> and <code>method</code>
    finally point somewhere real. Chapter 4&rsquo;s callbacks become promises. And chapter 7 plugs a
    database into the routes you write here.</p>
  </div>
</div>
"""
        },
        {
            'id': 'map', 'nav': 'Slide Map', 'label': 'Navigation',
            'title': 'All 51 slides, weighted',
            'html': slidemap([
                ('1', 'Chapter 5 leftover task', 'WRITE',
                 'DOM manipulation to show a table on click. Ten minutes, and it revises the previous chapter.'),
                ('2&ndash;4', 'Introducing Node; JavaScript everywhere', 'MEMORIZE',
                 'Five advantages: JavaScript everywhere, push architectures, non-blocking architectures, a rich tool ecosystem, broad adoption.'),
                ('5&ndash;6', 'Name conflicts; what a module is', 'MEMORIZE',
                 'There is <strong>no function overloading in JavaScript</strong> &mdash; the second declaration simply replaces the first. Modules solve the resulting name conflicts.'),
                ('7&ndash;8', 'Running a Node app; import/export', 'WRITE',
                 '<code>node app.js</code> or just <code>node app</code>; <code>Ctrl-C</code> to stop. <code>module.exports</code> and <code>require</code>.'),
                ('9', 'Node core modules', 'MEMORIZE',
                 'Six to know: <code>http</code>, <code>url</code>, <code>querystring</code>, <code>path</code>, <code>fs</code>, <code>util</code>.'),
                ('10&ndash;14', 'fs module; http module; simple and static servers', 'WRITE',
                 'Type the simplest HTTP server from memory. It is nine lines and it is the most likely practical question in the first half.'),
                ('15&ndash;18', 'Blocking vs non-blocking; high volume; disadvantages', 'MEMORIZE',
                 'The restaurant analogy is the exam answer. Learn both disadvantages: relational databases were awkward, and computation-heavy work blocks the single thread.'),
                ('19&ndash;21', 'Asynchronous coding; the async fs example; callback hell', 'MEMORIZE',
                 'Slide 21 is the deliberate demonstration of callback hell &mdash; nested <code>readFile</code>s so the second can see the first result.'),
                ('22&ndash;23', 'Promises', 'WRITE',
                 'The single most important construct in the chapter. Know <code>resolve</code>/<code>reject</code>, <code>then</code>/<code>catch</code>, and how to wrap a callback API in one.'),
                ('24&ndash;28', 'fetch; what it returns; common mistakes', 'WRITE',
                 '<code>fetch</code> does <strong>not</strong> return the data &mdash; it returns a Promise. A web API is a web resource that returns data instead of HTML, CSS, JavaScript or images.'),
                ('29', 'npm, package.json, dependencies', 'MEMORIZE',
                 '<code>npm init -y</code> then <code>npm install express</code>. Know what each does.'),
                ('30', 'CORS', 'MEMORIZE',
                 'Browsers block cross-origin requests by default. <code>Access-Control-Allow-Origin: *</code>, or <code>app.use(cors())</code> in Node.'),
                ('31&ndash;33', 'Semantic versioning; .gitignore; dev dependencies', 'MEMORIZE',
                 'MAJOR.MINOR.PATCH, and what <code>~</code> and <code>^</code> each allow. Never commit <code>node_modules</code>.'),
                ('34&ndash;36', 'Express, static files, middleware', 'WRITE',
                 'Middleware is the <strong>chain of responsibility</strong> pattern. <code>app.use()</code> installs a function on that chain.'),
                ('37&ndash;38', 'Routing; chained middleware', 'WRITE',
                 'The four-handler pattern &mdash; static, two routes, and a catch-all 404 &mdash; is the shape of every Express app you will write.'),
                ('39&ndash;40', 'Environment variables; a simple API', 'WRITE',
                 '<code>dotenv</code>, a <code>.env</code> file, and <code>process.env.PORT</code>. Used in every later example.'),
                ('41&ndash;42', 'Separating functionality into modules', 'WRITE',
                 'Once you have five or six routes a single file becomes too complex. This is the refactor pattern for the project.'),
                ('43&ndash;45', 'Three ways to receive parameters', 'WRITE',
                 'Route params <code>:word</code>, query params <code>?first=</code>, and form bodies. <strong>Know which object each lands in.</strong>'),
                ('46&ndash;50', 'View engines and EJS, including partials', 'WRITE',
                 'Learn the two tag forms &mdash; <code>&lt;% %&gt;</code> runs code, <code>&lt;%= %&gt;</code> prints a value &mdash; and the <code>&lt;%- include %&gt;</code> partial.'),
                ('51', 'Supporting material', 'SKIM', 'Installation links and a video walkthrough.'),
            ])
        },
        {
            'id': 'node', 'nav': 'Node Basics', 'label': 'Slides 3&ndash;14',
            'title': 'Modules, files and a server by hand',
            'html': """
<h3>Why modules exist</h3>
""" + code('the problem — slide 5', """
<span class="c">// JavaScript has NO FUNCTION OVERLOADING. The second declaration
// simply replaces the first — silently.</span>
<span class="k">let</span> product = (x, y)    =&gt; x * y;
<span class="k">let</span> product = (x, y, z) =&gt; x * y * z;

console.log(product(<span class="s">2</span>, <span class="s">3</span>));   <span class="c">// NaN  — z is undefined, and 6 * undefined = NaN</span>

<span class="c">// With hundreds of literals across dozens of .js files, you need some
// way to prevent name conflicts. That way is MODULES: literals defined
// within a module are SCOPED TO THAT MODULE.</span>
""", note='Slide 5') + code('modules — CommonJS', """
<span class="c">// ── mod-names.js ───────────────────────────────────────────────</span>
<span class="k">const</span> secret = <span class="s">'SECRET PHRASE'</span>;      <span class="c">// local — NOT exported, stays private</span>

<span class="k">const</span> first_name = <span class="s">'salah'</span>;
<span class="k">const</span> last_name  = <span class="s">'abid'</span>;
module.exports = { first_name, last_name };   <span class="c">// export an OBJECT</span>

<span class="c">// ── mod-utils.js ───────────────────────────────────────────────</span>
<span class="k">const</span> saySelem = (name) =&gt; { console.log(`Selem Mr ${name}`); };
module.exports = saySelem;                    <span class="c">// export a FUNCTION (default style)</span>

<span class="c">// ── app.js ─────────────────────────────────────────────────────</span>
<span class="k">const</span> names = require(<span class="s">'./mod-names'</span>);    <span class="c">// ./ — a LOCAL file, not an npm package</span>
<span class="k">const</span> selem = require(<span class="s">'./mod-utils'</span>);

selem(names.first_name);   <span class="c">// "Selem Mr salah"</span>
selem(names.secret);       <span class="c">// "Selem Mr undefined"  ← not exported = not visible</span>

<span class="c">// RUN IT:   node app.js     or just   node app
// STOP IT:  Ctrl-C</span>

<span class="c">// On the CLIENT side you must tell the browser a file is a module:
//   &lt;script src="art.js" type="module"&gt;&lt;/script&gt;
// In Node every file is a module by default (CommonJS).</span>
""", note='Slides 6–8') + """

<h3>Core modules</h3>
""" + table(['Module', 'What it gives you'], [
                ('<code>http</code>', 'Classes, methods and events to create a Node HTTP server.'),
                ('<code>url</code>', 'Methods for URL resolution and parsing.'),
                ('<code>querystring</code>', 'Methods to deal with query strings.'),
                ('<code>path</code>', 'Methods to deal with file paths.'),
                ('<code>fs</code>', 'Classes, methods and events for file I/O.'),
                ('<code>util</code>', 'Utility functions.'),
            ]) + """

<h3>The <code>fs</code> module &mdash; synchronous first</h3>
""" + code('app.js — 02-files', """
<span class="k">const</span> { readFileSync, writeFileSync } = require(<span class="s">'fs'</span>);   <span class="c">// destructured import</span>

console.log(<span class="s">'start'</span>);

<span class="k">const</span> first  = readFileSync(<span class="s">'./content/first.txt'</span>,  <span class="s">'utf8'</span>);
<span class="k">const</span> second = readFileSync(<span class="s">'./content/second.txt'</span>, <span class="s">'utf8'</span>);

writeFileSync(
    <span class="s">'./content/result.txt'</span>,
    `Here is the result : ${first}, ${second}` + <span class="s">"\\n"</span>,
    { flag: <span class="s">'a'</span> }        <span class="c">// 'a' for APPENDING (default would overwrite)</span>
);

console.log(<span class="s">'Task completed!'</span>);

<span class="c">// OUTPUT:  start
//          Task completed!
// …in that order, because Sync versions BLOCK until they finish.</span>
""", note='Slide 10') + """

<h3>A server by hand &mdash; the <code>http</code> module</h3>
""" + code('simplest-server.js', """
<span class="k">const</span> http = require(<span class="s">'http'</span>);

<span class="k">const</span> server = http.createServer((req, res) =&gt; {
    res.write(<span class="s">"This is my response to your request!"</span>);
    res.end();                     <span class="c">// end() is REQUIRED — without it the browser hangs</span>
    <span class="k">return</span>;
});

server.listen(<span class="s">5000</span>);
console.log(<span class="s">"Listening on port 5000"</span>);

<span class="c">// &gt; node simplest-server
// Then open http://127.0.0.1:5000 in the browser.
//
// NOTE: http://127.0.0.1:5000/anything/at/all gives the SAME response.
// There is no routing here at all — which is the point of the next slide.</span>
""", note='Slide 12') + code('simplest-server-2.js — routing by hand', """
<span class="k">const</span> http = require(<span class="s">'http'</span>);

<span class="k">const</span> server = http.createServer((req, res) =&gt; {
    <span class="k">if</span> (req.url === <span class="s">'/'</span>) {
        res.end(<span class="s">"This is the homepage!"</span>);
    } <span class="k">else</span> <span class="k">if</span> (req.url === <span class="s">'/about'</span>) {
        res.end(<span class="s">"This is the ABOUT page!"</span>);
    } <span class="k">else</span> {
        res.end(`&lt;h1&gt;Page not Found!&lt;/h1&gt;
                 &lt;p&gt;&lt;a href="/"&gt;Homepage&lt;/a&gt;&lt;/p&gt;`);
    }
    <span class="k">return</span>;
});

server.listen(<span class="s">5000</span>);

<span class="c">// A fuller version writes headers explicitly:
//   res.writeHead(200, {"Content-Type": "text/plain"});
//
// Now imagine twenty routes in this if/else chain. That is why Express
// exists — and why slide 34 arrives when it does.</span>
""", note='Slide 13')
        },
        {
            'id': 'async', 'nav': 'Async', 'label': 'Slides 15&ndash;28',
            'title': 'Non-blocking architecture, promises and fetch',
            'html': """
<h3>Blocking vs non-blocking &mdash; the restaurant analogy</h3>
""" + table(['Blocking (Apache with JEE or PHP)', 'Non-blocking (Node)'], [
                ('A blocking multiprocessing or multithreaded model.', 'A single worker services all requests in a single <strong>event loop</strong> thread.'),
                ('As though <strong>a single person had to handle every task for each table</strong> &mdash; so you need one person per table.', 'The worker can only do one thing at a time, but <strong>delegates other tasks to other agents</strong> and carries on.'),
                ('Scales by adding processes or threads.', 'Node is <strong>non-blocking, asynchronous and single-threaded</strong>.'),
            ]) + """
<p><strong>Where Node shines:</strong> data-intensive real-time applications talking to distributed
computers, with NoSQL data sources. The slide&rsquo;s example is a Like button handling a massive
number of concurrent writes &mdash; a memory-based message queue records the changes and they are
persisted eventually.</p>
<p><strong>Where Node does not:</strong> sites whose data lives in a traditional relational database
such as MySQL, where access was a complex programming task; and computationally heavy work such as
video processing or scientific computing, which stalls the single thread.</p>

<h3>Callback hell &mdash; the problem, demonstrated</h3>
""" + code('app.js — 04-files-async', """
<span class="k">const</span> { readFile, writeFile } = require(<span class="s">'fs'</span>);   <span class="c">// the ASYNC versions</span>

console.log(<span class="s">'Starting task A...'</span>);

readFile(<span class="s">'./content/first.txt'</span>, <span class="s">'utf8'</span>, (err, result) =&gt; {
    <span class="k">if</span> (err) { console.log(err); <span class="k">return</span>; }      <span class="c">// error-first callback convention</span>

    writeFile(<span class="s">'./content/result-async.txt'</span>,
        `Here is the Async result : ${result}`,
        (err, result) =&gt; {
            <span class="k">if</span> (err) { console.log(err); <span class="k">return</span>; }
            console.log(<span class="s">'Task A completed!'</span>);
        }
    );
});

console.log(<span class="s">'starting next task...'</span>);

<span class="c">// OUTPUT ORDER — the whole point:
//   Starting task A...
//   starting next task...     ← this line runs BEFORE the file is read
//   Task A completed!         ← the callback fires last</span>
""", note='Slide 20') + code('the same thing with TWO files — slide 21', """
<span class="c">// To let the second read see the first result, the second readFile has
// to be called INSIDE the first callback. Add a third file and a fourth
// and you get a staircase drifting off the right of the screen.</span>
readFile(<span class="s">'./content/first.txt'</span>, <span class="s">'utf8'</span>, (err, result) =&gt; {
    <span class="k">if</span> (err) { console.log(err); <span class="k">return</span>; }
    <span class="k">const</span> first = result;

    readFile(<span class="s">'./content/second.txt'</span>, <span class="s">'utf8'</span>, (err, result) =&gt; {
        <span class="k">if</span> (err) { console.log(err); <span class="k">return</span>; }
        <span class="k">const</span> second = result;

        writeFile(<span class="s">'./content/result-async.txt'</span>,
            `Here is the result : ${first}, ${second}`,
            (err, result) =&gt; {
                <span class="k">if</span> (err) { console.log(err); <span class="k">return</span>; }
                console.log(<span class="s">'done with this task'</span>);
            }
        );
    });
});

<span class="c">//                    ← ← ←   CALLBACK HELL   → → →</span>
""", note='Slide 21') + """

<h3>Promises &mdash; the solution</h3>
<p>A Promise object <strong>represents the eventual completion (or failure) of an asynchronous
operation and its resulting value.</strong> Probably the promise will complete and you receive the
data; or it will not, and you receive an error instead.</p>
""" + code('promises.js', """
<span class="c">// ── DECLARATION AND INSTANTIATION ──────────────────────────────
// The handler passed to the constructor takes TWO parameters. </span>
<span class="k">const</span> promiseObj = <span class="k">new</span> Promise((resolve, reject) =&gt; {
    doWork();
    <span class="k">if</span> (someCondition)
        resolve(someValue);      <span class="c">// works like a return</span>
    <span class="k">else</span>
        reject(someMessage);     <span class="c">// works like a throw</span>
});

<span class="c">// ── CONSUMING IT ───────────────────────────────────────────────</span>
promiseObj
    .then(someValue =&gt; {
        <span class="c">// success — the promise was achieved</span>
    })
    .catch(someMessage =&gt; {
        <span class="c">// the promise was not satisfied</span>
    });

<span class="c">// ── WRAPPING A CALLBACK API IN A PROMISE (slide 23) ────────────</span>
<span class="k">const</span> { readFile } = require(<span class="s">'fs'</span>);

<span class="k">const</span> read = (path) =&gt; {
    <span class="k">return</span> <span class="k">new</span> Promise((resolve, reject) =&gt; {
        readFile(path, <span class="s">'utf8'</span>, (err, data) =&gt; {
            <span class="k">if</span> (err) reject(err);
            <span class="k">else</span>     resolve(data);
        });
    });
};

read(<span class="s">'./content/first.txt'</span>)
    .then(data =&gt; console.log(data))
    .catch(err  =&gt; console.log(err));

<span class="c">// ── CHAINING beats nesting — the whole payoff ──────────────────</span>
read(<span class="s">'./content/first.txt'</span>)
    .then(first  =&gt; read(<span class="s">'./content/second.txt'</span>))
    .then(second =&gt; console.log(second))
    .catch(err   =&gt; console.log(err));      <span class="c">// ONE catch for the whole chain</span>
""", note='Slides 22–23') + """

<h3><code>fetch</code> &mdash; asynchronous data requests</h3>
<p>A <strong>web API is simply a web resource that returns data</strong> instead of HTML, CSS,
JavaScript or images. <code>fetch</code> is done from the client side to get that data
asynchronously, and it replaces the older AJAX technology.</p>
""" + code('fetch.js', """
<span class="k">let</span> cities = fetch(<span class="s">'/api/cities?country=italy'</span>);

<span class="c">// What does `cities` contain? NOT the JSON data. It takes time for the
// service to execute and respond, so fetch returns a PROMISE object.</span>

fetch(<span class="s">'/api/cities?country=italy'</span>)
    .then(response =&gt; {
        console.warn(<span class="s">'response received!!!'</span>);
        <span class="k">return</span> response.json();      <span class="c">// ← ALSO returns a promise</span>
    })
    .then(data =&gt; {
        console.log(data);              <span class="c">// finally the actual data</span>
    })
    .catch(err =&gt; console.log(err));

<span class="c">// COMMON MISTAKES (slide 28):
//   1. expecting fetch to return the data directly
//   2. forgetting that response.json() is ALSO asynchronous
//   3. nesting multiple fetches inside each other — callback hell again.
//      CHAIN them with .then, or use async/await:</span>

<span class="k">async</span> <span class="k">function</span> load() {
    <span class="k">try</span> {
        <span class="k">const</span> response = <span class="k">await</span> fetch(<span class="s">'/api/cities?country=italy'</span>);
        <span class="k">const</span> data     = <span class="k">await</span> response.json();
        console.log(data);
    } <span class="k">catch</span> (err) {
        console.log(err);
    }
}
""", note='Slides 25–28') + hook(
                "<strong>The single sentence to remember about <code>fetch</code>:</strong> it returns "
                "a Promise, not data &mdash; and <code>response.json()</code> returns another one. "
                "Two <code>await</code>s, or two <code>.then()</code>s. Nearly every broken fetch in a "
                "lab is one of those two missing.") + """

<h3>CORS</h3>
""" + code('cors', """
<span class="c">// Modern browsers PREVENT cross-origin requests by default, which makes
// legitimate sharing between two domains harder.
//
// An ORIGIN is a protocol + domain + port. All three must match.
//   https://a.com      vs  http://a.com       ← different (protocol)
//   https://a.com      vs  https://b.com      ← different (domain)
//   http://a.com:3000  vs  http://a.com:5000  ← different (port)</span>

<span class="c">// An API that wants to allow ANY domain adds this header to responses:
//   Access-Control-Allow-Origin: *</span>

<span class="c">// In Node:</span>
<span class="c">// &gt; npm install cors</span>
<span class="k">const</span> cors = require(<span class="s">'cors'</span>);
app.use(cors());   <span class="c">// allows the API to be accessed through JavaScript</span>
""", note='Slide 30')
        },
        {
            'id': 'express', 'nav': 'npm &amp; Express', 'label': 'Slides 29&ndash;45',
            'title': 'Packages, routing, middleware and parameters',
            'html': """
<h3>npm and <code>package.json</code></h3>
""" + code('terminal + package.json', """
<span class="c"># npm = Node Package Manager</span>
npm init -y                <span class="c"># creates a basic package.json (-y skips the questionnaire)</span>
npm install express        <span class="c"># installs into node_modules AND adds it to dependencies</span>
npm install nodemon -D     <span class="c"># a DEV dependency — needed at development time only</span>
npm install -g nodemon     <span class="c"># or globally</span>
npm install                <span class="c"># restores node_modules from package.json</span>
npm run start              <span class="c"># runs the "start" script</span>
npm run dev                <span class="c"># runs the "dev" script — nodemon restarts on save</span>

<span class="c">// package.json</span>
{
  <span class="s">"name"</span>: <span class="s">"05-npm-demo"</span>,
  <span class="s">"version"</span>: <span class="s">"1.0.0"</span>,
  <span class="s">"main"</span>: <span class="s">"index.js"</span>,
  <span class="s">"scripts"</span>: {
    <span class="s">"start"</span>: <span class="s">"node app.js"</span>,
    <span class="s">"dev"</span>:   <span class="s">"nodemon app.js"</span>
  },
  <span class="s">"dependencies"</span>:    { <span class="s">"express"</span>: <span class="s">"^4.18.2"</span> },
  <span class="s">"devDependencies"</span>: { <span class="s">"nodemon"</span>: <span class="s">"^2.0.20"</span> }
}

<span class="c"># .gitignore — node_modules is NEVER shared. Teammates recreate it
# from package.json with `npm install`.</span>
/node-modules
""", note='Slides 29, 32–33') + """
<h4>Semantic versioning &mdash; <code>MAJOR.MINOR.PATCH</code></h4>
""" + table(['Part', 'Increments when&hellip;', 'Breaks your code?'], [
                ('<strong>MAJOR</strong>', 'You make incompatible API changes.', 'Yes &mdash; will not work with earlier versions.'),
                ('<strong>MINOR</strong>', 'You add functionality in a backwards-compatible way.', 'No.'),
                ('<strong>PATCH</strong>', 'You make backwards-compatible bug fixes.', 'No.'),
                ('<code>~1.3.8</code>', 'Allows automatic update to the latest <strong>PATCH</strong>.', 'No.'),
                ('<code>^1.3.8</code>', 'Allows automatic update to the latest <strong>MINOR</strong>.', 'No.'),
            ]) + """

<h3>Express: static files, routing and the 404</h3>
""" + code('app.js — 08-express-server', """
<span class="k">const</span> express = require(<span class="s">'express'</span>);
<span class="k">const</span> app = express();

<span class="c">// A — the public folder becomes visible to HTTP requests, so
//     http://localhost:3000/css/styles.css works if css/ is inside public/</span>
app.use( express.static(<span class="s">'public'</span>) );

<span class="c">// B — a route is a URL: a series of folders, files, or parameter data</span>
app.get(<span class="s">'/'</span>, (request, response) =&gt; {
    response.sendFile(<span class="s">'./pages/index.html'</span>);
});

<span class="c">// C</span>
app.get(<span class="s">'/about'</span>, (request, response) =&gt; {
    response.sendFile(<span class="s">'./pages/about.html'</span>);
});

<span class="c">// D — ANY other request falls through to here. Order matters:
//     this must come LAST or it swallows everything.</span>
app.use( (request, response) =&gt; {
    response.status(<span class="s">404</span>).sendFile(<span class="s">'./pages/404.html'</span>);
});

app.listen(<span class="s">3000</span>, () =&gt; { console.log(<span class="s">'listening on 3000'</span>); });

<span class="c">// A request tries A, then B, then C, then D — the FIRST match wins.</span>
""", note='Slides 34, 37') + """

<h3>Middleware &mdash; the chain of responsibility</h3>
<p>Middleware is <strong>software that is a bridge between an application and the data</strong>, and
Express arranges it as a chain of responsibility. The slides give the reason to use it: it splits
server operations into smaller units, such as performing validation on the data, which leads to
better app structure and reuse &mdash; and you can block the execution of the current chain and pass
control to functions that handle errors.</p>
""" + code('middleware.js', """
<span class="c">// app.use() INSTALLS a middleware function on the chain.</span>

<span class="c">// At the ROOT of the route — runs for EVERY request</span>
app.use( (req, res, next) =&gt; {
    console.log(`${req.method} ${req.path} - ${req.ip}`);
    next();          <span class="c">// ← WITHOUT next() the request HANGS FOREVER</span>
});

<span class="c">// Mounted at a SPECIFIC route:  app.METHOD(path, middleware, callback)</span>
app.get(<span class="s">'/now'</span>,
    <span class="k">function</span> (req, res, next) {
        req.time = <span class="k">new</span> Date().toString();    <span class="c">// attach data to the request</span>
        next();                                <span class="c">// hand on to the next function</span>
    },
    <span class="k">function</span> (req, res) {
        res.json({ time: req.time });          <span class="c">// the last one SENDS the response</span>
    }
);

<span class="c">// Built-in and third-party middleware you have already met:</span>
app.use(express.static(<span class="s">'public'</span>));                        <span class="c">// serve static files</span>
app.use(cors());                                          <span class="c">// allow cross-origin</span>
app.use(bodyParser.urlencoded({ extended: <span class="k">false</span> }));     <span class="c">// parse form bodies</span>
""", note='Slides 35–36, 38') + hook(
                "<strong>The bug that will cost you an hour:</strong> a middleware function that "
                "forgets <code>next()</code>. There is no error, no crash, no log &mdash; the browser "
                "just spins until it times out. If a request hangs, look for a missing "
                "<code>next()</code> before you look anywhere else.") + """

<h3>Environment variables</h3>
""" + code('.env + app.js — 09-env-variables', """
<span class="c"># .env — any number of key=value pairs</span>
PORT=8080
BUILD=development

<span class="c">// &gt; npm install dotenv</span>
require(<span class="s">'dotenv'</span>).config();          <span class="c">// load .env into process.env</span>

console.log(process.env);            <span class="c">// see everything available</span>
console.log(<span class="s">"build type="</span> + process.env.BUILD);

app.listen(process.env.PORT);        <span class="c">// never hard-code the port again</span>

<span class="c">// .env belongs in .gitignore too — it holds secrets.</span>
""", note='Slide 39') + """

<h3>A simple API, and splitting it into modules</h3>
""" + code('app.js + data-module.js — 10-simple-api', """
<span class="c">// ── data-module.js — slide 42 ──────────────────────────────────</span>
<span class="k">const</span> fs   = require(<span class="s">'fs'</span>);
<span class="k">const</span> path = require(<span class="s">'path'</span>);

<span class="k">const</span> jsonPath = path.join(__dirname, <span class="s">'data'</span>, <span class="s">'SE2022.json'</span>);
<span class="c">//   __dirname = the folder THIS file is in. path.join builds a path
//   that works on Windows and Linux alike.</span>

<span class="k">let</span> curriculum;
fs.readFile(jsonPath, (err, data) =&gt; {
    <span class="k">if</span> (err) console.log(<span class="s">'Unable to read json data file'</span>);
    <span class="k">else</span>     curriculum = JSON.parse(data);
});

<span class="k">const</span> getData = () =&gt; { <span class="k">return</span> curriculum; };
module.exports = getData;

<span class="c">// ── app.js ─────────────────────────────────────────────────────</span>
<span class="k">const</span> express = require(<span class="s">'express'</span>);
require(<span class="s">'dotenv'</span>).config();
<span class="k">const</span> getData = require(<span class="s">'./data-module'</span>);

<span class="k">const</span> app = express();

app.get(<span class="s">'/'</span>, (req, resp) =&gt; { resp.json(getData()); });   <span class="c">// res.json sends JSON</span>

app.listen(process.env.PORT, () =&gt; {
    console.log(<span class="s">"Listening at port… "</span> + process.env.PORT);
});

<span class="c">// WHY: with five or six routes a single Node file becomes too complex.
// Separate the routing, and separate the handler logic, into modules.</span>
""", note='Slides 40–42') + """

<h3>Three ways to receive parameters &mdash; know which object each lands in</h3>
""" + table(['Way', 'URL / source', 'Read it from', 'Needs'], [
                ('<strong>Route params</strong>', '<code>/echo/hello</code>', '<code>req.params.word</code>', 'The <code>:param</code> syntax in the route.'),
                ('<strong>Query params</strong>', '<code>/employee?first=skander&amp;last=turki</code>', '<code>req.query.first</code>', 'Nothing &mdash; no library needed.'),
                ('<strong>Form body</strong>', 'A POSTed <code>&lt;form&gt;</code>', '<code>req.body.first</code>', '<code>body-parser</code> middleware.'),
            ]) + code('parameters.js', """
<span class="c">// ── 1. ROUTE PARAMS — the :param syntax (slide 43) ─────────────</span>
app.get(<span class="s">'/echo/:word'</span>, (req, res) =&gt; {
    <span class="k">let</span> param = req.params.word;
    res.json({ echo: param });
});
<span class="c">// GET https://ip:port/echo/hello  →  'hello' lands in req.params.word</span>

<span class="c">// ── 2. QUERY PARAMS — URL-encoded queries (slide 44) ───────────</span>
app.get(<span class="s">'/employee'</span>, (req, res) =&gt; {
    res.json({ employee: `${req.query.first} ${req.query.last}` });
});
app.post(<span class="s">'/employee'</span>, (req, res) =&gt; {
    res.json({ employee: `${req.query.first} ${req.query.last}` });
});
<span class="c">// http://ip:port/employee?first=skander&amp;last=turki</span>

<span class="c">// ── 3. FORM BODY (slide 45) ────────────────────────────────────
//   &lt;form action="/name" method="post"&gt;
//     &lt;label&gt;First Name :&lt;/label&gt;&lt;input type="text" name="first"&gt;&lt;br&gt;
//     &lt;label&gt;Last Name :&lt;/label&gt;&lt;input type="text" name="last"&gt;&lt;br&gt;
//     &lt;input type="submit" value="Submit"&gt;
//   &lt;/form&gt;

// A payload (POST, DELETE…) needs middleware to be parsed:</span>
<span class="k">const</span> bodyParser = require(<span class="s">'body-parser'</span>);
app.use(bodyParser.urlencoded({ extended: <span class="k">false</span> }));

app.post(<span class="s">'/name'</span>, (req, res) =&gt; {
    <span class="k">let</span> p_first = req.body.first;      <span class="c">// ← req.BODY, not query, not params</span>
    res.send(`Hello ${p_first}`);
});

<span class="c">// Modern Express has this built in: app.use(express.urlencoded({extended:false}))</span>
""", note='Slides 43–45')
        },
        {
            'id': 'ejs', 'nav': 'EJS', 'label': 'Slides 46&ndash;50',
            'title': 'View engines: generating HTML on the server',
            'html': """
<p>A view engine lets Node generate HTML from data. Install the package, tell Express which engine to
use and which folder holds the views, and render instead of sending files.</p>
""" + code('setting up EJS', """
<span class="c">// &gt; npm install ejs</span>

<span class="c">// register the view engine</span>
app.set(<span class="s">'view engine'</span>, <span class="s">'ejs'</span>);

<span class="c">// templates go in /views by DEFAULT — configure only if you want another</span>
app.set(<span class="s">'views'</span>, <span class="s">'otherThanViewsFolder'</span>);

<span class="c">// response.render() sends the template — 'index' means views/index.ejs</span>
app.get(<span class="s">'/'</span>, (request, response) =&gt; {
    response.render(<span class="s">'index'</span>);
});
""", note='Slides 46–47') + code('app.js — injecting data', """
<span class="k">const</span> express = require(<span class="s">'express'</span>);
<span class="k">const</span> app = express();

app.set(<span class="s">'view engine'</span>, <span class="s">'ejs'</span>);
app.use(express.static(<span class="s">'public'</span>));

app.get(<span class="s">'/'</span>, (req, res) =&gt; {
    <span class="k">const</span> blogs = [
        { title: <span class="s">'First post'</span>,  snippet: <span class="s">'…'</span> },
        { title: <span class="s">'Second post'</span>, snippet: <span class="s">'…'</span> },
    ];
    <span class="c">// SECOND ARGUMENT = the data sent to the template</span>
    res.render(<span class="s">'index'</span>, { title: <span class="s">'Home'</span>, blogs: blogs });
});

app.get(<span class="s">'/about'</span>,  (req, res) =&gt; res.render(<span class="s">'about'</span>,  { title: <span class="s">'About'</span> }));
app.get(<span class="s">'/create'</span>, (req, res) =&gt; res.render(<span class="s">'create'</span>, { title: <span class="s">'Create a new blog'</span> }));

<span class="c">// catch-all 404, rendered rather than sent as a file</span>
app.use((req, res) =&gt; {
    res.status(<span class="s">404</span>).render(<span class="s">'404'</span>, { title: <span class="s">'404'</span> });
});

app.listen(<span class="s">3000</span>);
""", note='Slide 48') + """

<h3>The two EJS tag forms &mdash; and partials</h3>
""" + code('views/index.ejs', """
<span class="k">&lt;html</span> <span class="t">lang</span>=<span class="s">"en"</span><span class="k">&gt;</span>
<span class="s">&lt;%- include("./partials/head.ejs") %&gt;</span>

<span class="k">&lt;body&gt;</span>
  <span class="s">&lt;%- include("./partials/nav.ejs") %&gt;</span>

  <span class="k">&lt;div</span> <span class="t">class</span>=<span class="s">"blogs content"</span><span class="k">&gt;</span>
    <span class="k">&lt;h2&gt;</span><span class="s">&lt;%= title %&gt;</span>: All Blogs<span class="k">&lt;/h2&gt;</span>

    <span class="s">&lt;% if (blogs.length &gt; 0) { %&gt;</span>
      <span class="s">&lt;% blogs.forEach(blog =&gt; { %&gt;</span>
        <span class="k">&lt;h3</span> <span class="t">class</span>=<span class="s">"title"</span><span class="k">&gt;</span><span class="s">&lt;%= blog.title %&gt;</span><span class="k">&lt;/h3&gt;</span>
        <span class="k">&lt;p</span> <span class="t">class</span>=<span class="s">"snippet"</span><span class="k">&gt;</span><span class="s">&lt;%= blog.snippet %&gt;</span><span class="k">&lt;/p&gt;</span>
      <span class="s">&lt;% }) %&gt;</span>
    <span class="s">&lt;% } else { %&gt;</span>
      <span class="k">&lt;p&gt;</span>There are no blogs to display...<span class="k">&lt;/p&gt;</span>
    <span class="s">&lt;% } %&gt;</span>
  <span class="k">&lt;/div&gt;</span>

  <span class="s">&lt;%- include("./partials/footer.ejs") %&gt;</span>
<span class="k">&lt;/body&gt;</span>
<span class="k">&lt;/html&gt;</span>

<span class="c">&lt;!-- THE THREE TAGS:
     &lt;%  %&gt;   runs JavaScript, outputs NOTHING       (if, forEach, loops)
     &lt;%= %&gt;   outputs the VALUE of an expression      (escaped — safe)
     &lt;%- %&gt;   outputs UNESCAPED — used for include()

     PARTIALS let one .ejs file be included in another so shared parts
     are reused. Organise them under views/partials/ :
        /views/partials/head.ejs
        /views/partials/header.ejs
        /views/partials/footer.ejs                                 --&gt;</span>
""", note='Slides 49–50') + hook(
                "<strong>The EJS tag you will get wrong once:</strong> <code>&lt;% %&gt;</code> versus "
                "<code>&lt;%= %&gt;</code>. Anything that <em>controls flow</em> uses the plain form; "
                "anything that <em>appears on the page</em> needs the equals sign. Writing "
                "<code>&lt;% title %&gt;</code> renders nothing at all, silently.")
        },
        {
            'id': 'traps', 'nav': 'Traps', 'label': 'Marks Lost Here',
            'title': 'The eight things people get wrong',
            'html': (
                trap('Middleware with no <code>next()</code>',
                     'The request hangs. No error, no stack trace, no log line &mdash; the browser spins until it times out. The chain of responsibility simply stopped.',
                     'Every middleware function either calls <code>next()</code> or sends a response. Exactly one of the two, never neither.') +
                trap('The 404 handler placed too early',
                     '<code>app.use((req,res) =&gt; res.status(404)...)</code> written before your routes catches <strong>every</strong> request, and your real routes never run.',
                     'Order is everything in Express: static, then specific routes, then the catch-all last. The first match wins.') +
                trap('Expecting <code>fetch</code> to return data',
                     '<code>let cities = fetch(url)</code> gives you a Promise object, not the cities. Logging it shows <code>Promise { &lt;pending&gt; }</code> and people conclude the API is broken.',
                     'Chain <code>.then(r =&gt; r.json()).then(data =&gt; ...)</code>, or <code>await</code> twice. Slide 26 asks this exact question.') +
                trap('Reading a form body from <code>req.query</code>',
                     'A POSTed form puts its data in the request <strong>body</strong>, not the URL. <code>req.query.first</code> is <code>undefined</code> and so is <code>req.body.first</code> until the parser is installed.',
                     'Three sources, three objects: <code>req.params</code> for <code>:route</code> params, <code>req.query</code> for <code>?query=</code> strings, <code>req.body</code> for form payloads &mdash; and the last one needs <code>body-parser</code> or <code>express.urlencoded</code>.') +
                trap('Committing <code>node_modules</code>',
                     'Thousands of files in the repository, huge diffs, and merge conflicts in code nobody wrote. Slide 32 is explicit that the folder does not have to be shared.',
                     'Add <code>/node_modules</code> to <code>.gitignore</code>. Teammates run <code>npm install</code> and get the same tree from <code>package.json</code>.') +
                trap('Hard-coding the port',
                     '<code>app.listen(3000)</code> works on your laptop and fails wherever the platform assigns a port. It also means every teammate edits the same line.',
                     '<code>require(\'dotenv\').config()</code> and <code>app.listen(process.env.PORT)</code>. Put <code>.env</code> in <code>.gitignore</code> as well &mdash; it holds secrets.') +
                trap('Blaming the API for a CORS error',
                     'The request works in Postman and in the address bar but fails from your page. That is the browser enforcing the same-origin policy, not the API refusing you.',
                     'The <em>server</em> must send <code>Access-Control-Allow-Origin</code>. In your own Node app: <code>npm install cors</code>, then <code>app.use(cors())</code>. Remember an origin is protocol + domain + port &mdash; a different port is a different origin.') +
                trap('<code>&lt;% %&gt;</code> where <code>&lt;%= %&gt;</code> was needed',
                     '<code>&lt;h2&gt;&lt;% title %&gt;&lt;/h2&gt;</code> renders an empty heading. The tag evaluated the expression and threw the result away.',
                     '<code>&lt;% %&gt;</code> runs code. <code>&lt;%= %&gt;</code> prints a value. <code>&lt;%- %&gt;</code> prints unescaped, which is what <code>include()</code> needs.')
            )
        },
        {
            'id': 'cheat', 'nav': 'Cheat Sheet', 'label': 'One Screen',
            'title': 'Chapter 6 on a single screen',
            'html': cheat([
                ('Modules', [
                    '<code>module.exports = { a, b }</code>',
                    '<code>module.exports = fn</code>',
                    '<code>const x = require(\'./file\')</code>',
                    'Not exported = not visible',
                    'Client side: <code>&lt;script type="module"&gt;</code>',
                ]),
                ('Core modules', [
                    '<code>http</code> &mdash; create a server',
                    '<code>url</code> &mdash; parse URLs',
                    '<code>querystring</code> &mdash; query strings',
                    '<code>path</code> &mdash; file paths',
                    '<code>fs</code> &mdash; file I/O',
                    '<code>util</code> &mdash; utilities',
                ]),
                ('Terminal', [
                    '<code>node app</code> &middot; <code>Ctrl-C</code>',
                    '<code>npm init -y</code>',
                    '<code>npm install express</code>',
                    '<code>npm install nodemon -D</code>',
                    '<code>npm install</code> &mdash; restore modules',
                    '<code>npm run dev</code>',
                ]),
                ('Async', [
                    'Node: non-blocking, async, single-threaded',
                    'Callback: <code>(err, result) =&gt; {}</code>',
                    '<code>new Promise((resolve, reject) =&gt; {})</code>',
                    '<code>.then()</code> &middot; <code>.catch()</code>',
                    '<code>await</code> inside <code>async function</code>',
                    '<code>fetch</code> returns a Promise, not data',
                ]),
                ('Express', [
                    '<code>app.use(express.static(\'public\'))</code>',
                    '<code>app.get(path, (req, res) =&gt; {})</code>',
                    '<code>app.post</code> <code>app.put</code> <code>app.delete</code>',
                    '<code>res.send</code> <code>res.json</code> <code>res.sendFile</code> <code>res.render</code>',
                    '<code>res.status(404)</code>',
                    '<code>app.listen(process.env.PORT)</code>',
                ]),
                ('Middleware', [
                    'Chain of responsibility',
                    '<code>app.use((req,res,next) =&gt; { next(); })</code>',
                    'Always <code>next()</code> or send a response',
                    'Order matters &mdash; 404 handler goes LAST',
                    '<code>cors()</code> &middot; <code>bodyParser.urlencoded()</code>',
                ]),
                ('Parameters', [
                    '<code>/echo/:word</code> &rarr; <code>req.params.word</code>',
                    '<code>?first=x</code> &rarr; <code>req.query.first</code>',
                    'POSTed form &rarr; <code>req.body.first</code>',
                    'Bodies need a parser middleware',
                ]),
                ('EJS', [
                    '<code>app.set(\'view engine\', \'ejs\')</code>',
                    'Templates live in <code>/views</code>',
                    '<code>res.render(\'index\', { title })</code>',
                    '<code>&lt;% %&gt;</code> run &middot; <code>&lt;%= %&gt;</code> print',
                    '<code>&lt;%- include("./partials/head.ejs") %&gt;</code>',
                ]),
                ('SemVer', [
                    '<code>MAJOR.MINOR.PATCH</code>',
                    'MAJOR &mdash; breaking changes',
                    'MINOR &mdash; new features, compatible',
                    'PATCH &mdash; bug fixes, compatible',
                    '<code>~1.3.8</code> latest patch &middot; <code>^1.3.8</code> latest minor',
                ]),
            ])
        },
        {
            'id': 'drills', 'nav': 'Drills', 'label': 'Build It',
            'title': 'Build one app, one slide at a time',
            'html': """
<p>This chapter cannot be revised from paper &mdash; every idea in it is something a server either
does or fails to do. Work through the list as <em>one growing project</em> rather than fifteen
throwaway files, and by the end you will have the skeleton chapter 7 needs.</p>
""" + drills([
                'Do the slide 1 leftover task first: show a table when a heading is clicked, using DOM manipulation methods.',
                'Write two modules and an app that imports both. Deliberately leave one constant unexported and confirm it reads as <code>undefined</code>.',
                'Read two files with <code>readFileSync</code> and append the result to a third with <code>{ flag: \'a\' }</code>.',
                'Write the simplest HTTP server from memory in nine lines, then visit a nonsense URL and confirm it gives the same response.',
                'Add hand-written routing with <code>req.url</code>, including a 404 branch. Then imagine twenty routes and decide you want Express.',
                'Rewrite the same two-file read asynchronously and log the output order &mdash; predict it before running.',
                'Nest a second <code>readFile</code> inside the first callback so it can see the first result. That is callback hell; look at the indentation.',
                'Wrap <code>readFile</code> in a Promise and chain two reads with <code>.then</code>. Compare the shape to the previous drill.',
                'Fetch from a public API, log the raw <code>fetch</code> return value, then fix it with two <code>.then</code>s, then rewrite with <code>async/await</code>.',
                'Run <code>npm init -y</code>, install express and nodemon (one as a dev dependency), and read the resulting <code>package.json</code> line by line.',
                'Add <code>start</code> and <code>dev</code> scripts, run <code>npm run dev</code>, and edit a file while it is running.',
                'Build the four-handler Express app: static, two routes, catch-all 404. Then move the 404 to the top and watch everything break.',
                'Add a logging middleware that prints method, path and IP. Then delete its <code>next()</code> and watch the request hang.',
                'Move the port into a <code>.env</code> file and read it with <code>dotenv</code>.',
                'Write three endpoints that take a parameter three different ways &mdash; route, query, and a POSTed form &mdash; and note which <code>req</code> object each uses.',
                'Split the routes and the data loading into separate modules, as slides 41&ndash;42 describe.',
                'Convert the pages to EJS templates, pass real data into one, and factor the header and footer into partials.',
            ]) + """
<p>There is no chapter-6 example folder in your study material, but two solved labs cover exactly this
ground: <a href="/academics/software-engineering/se371/extra-resources/resource-viewers/lab-09-express-ejs-solution-b6cf6ffc/" target="_blank" rel="noopener">lab 09 &mdash; Express and EJS</a>
and <a href="/academics/software-engineering/se371/extra-resources/resource-viewers/lab-08-solution-5a3bdaf0/" target="_blank" rel="noopener">lab 08</a>.
Slide 51 and chapter 3 slide 85 both point to the full code repository at
<code>github.com/skanderturki/se371</code>.</p>
"""
        },
    ],
    'quiz': [
        {'tag': 'Express', 'q': 'A middleware function runs but the browser never receives a response and eventually times out. What is the most likely cause?',
         'opts': ['The port is already in use', 'The middleware did not call next() or send a response',
                  'CORS blocked the response', 'express.static was not configured'],
         'a': 1,
         'why': 'app.use() installs the function on a chain of responsibility. If it neither passes control on with next() nor sends a response itself, the request simply stops there — with no error at all.'},
        {'tag': 'Async', 'q': 'let cities = fetch(\'/api/cities\'); What does cities contain?',
         'opts': ['The JSON data from the API', 'A Promise object', 'The raw response text', 'undefined until the request finishes'],
         'a': 1,
         'why': 'It takes time for the service to respond, so fetch returns a Promise. Handle it with .then() for success and .catch() for failure — and remember response.json() returns another promise.'},
        {'tag': 'Express', 'q': 'A form posts to /name with <input name="first">. Where do you read the value?',
         'opts': ['<code>req.params.first</code>', '<code>req.query.first</code>',
                  '<code>req.body.first</code>, with a body parser installed', '<code>req.form.first</code>'],
         'a': 2,
         'why': 'A POSTed form sends its data in the request payload, so it arrives in req.body — but only after middleware such as bodyParser.urlencoded() has parsed it. req.params is for :route params and req.query for ?query strings.'},
        {'tag': 'Node', 'q': 'Which describes Node\'s architecture?',
         'opts': ['Blocking and multithreaded', 'Non-blocking, asynchronous and single-threaded',
                  'Non-blocking and multiprocess', 'Blocking with an event loop'],
         'a': 1,
         'why': 'A single worker services all requests in one event loop thread, delegating other tasks to other agents. It is also why Node is a poor fit for computationally heavy work such as video processing.'},
        {'tag': 'Modules', 'q': 'A module defines a constant but does not include it in module.exports. What does the importing file see?',
         'opts': ['The value, since everything in a file is exported',
                  'undefined — literals are scoped to their module',
                  'A ReferenceError', 'An empty string'],
         'a': 1,
         'why': 'Literals defined within a module are scoped to that module. The slide 8 example does exactly this: names.secret prints "Selem Mr undefined" because secret was never exported.'},
        {'tag': 'CORS', 'q': 'Your page cannot call an API that works fine in the address bar. Which header must the API send?',
         'opts': ['<code>Content-Type: application/json</code>', '<code>Access-Control-Allow-Origin</code>',
                  '<code>Cache-Control: no-store</code>', '<code>X-Requested-With</code>'],
         'a': 1,
         'why': 'Browsers block cross-origin requests by default. The server has to opt in with Access-Control-Allow-Origin — in a Node app, npm install cors then app.use(cors()).'},
        {'tag': 'npm', 'q': 'In "express": "^4.18.2", what does the caret allow npm to update to?',
         'opts': ['Patch versions only', 'The latest minor version', 'The latest major version', 'Nothing — it pins the version'],
         'a': 1,
         'why': 'Under semantic versioning, ^ allows updates to the latest MINOR version (new features, backwards compatible) and ~ allows the latest PATCH only. MAJOR changes are never taken automatically because they break compatibility.'},
        {'tag': 'EJS', 'q': 'You write <h2><% title %></h2> and the heading renders empty. Why?',
         'opts': ['title was not passed to render', '<% %> runs code but outputs nothing',
                  'EJS needs double quotes around variables', 'Headings cannot contain EJS tags'],
         'a': 1,
         'why': '<% %> executes JavaScript without printing anything. To output a value you need <%= title %>. The third form, <%- %>, prints unescaped and is what include() uses.'},
    ],
})


# ═══════════════════════════════════════════════════════════════════════════ #
# CHAPTER 07 — Working with Databases
# ═══════════════════════════════════════════════════════════════════════════ #

CHAPTERS.append({
    'num': 7,
    'slug': '07-working-with-databases',
    'file': 'working-with-databases.html',
    'title': 'Working with Databases',
    'desc': ('Slide-by-slide breakdown of SE371 Chapter 7 — MVC, SQL vs NoSQL, MongoDB, ORMs, '
             'Sequelize models, CRUD and HTTP verbs, query operators, associations and validators.'),
    'sub': ('The last chapter, and the one that turns your Express routes into a real application. '
            'Half of it is conceptual and very examinable — MVC, SQL vs NoSQL, CRUD verbs — and half '
            'is Sequelize code you will be asked to write.'),
    'stats': ['47 slides', 'Two decks in one', 'Half concept, half code', 'Book ch. 15'],
    'sections': [
        {
            'id': 'orient', 'nav': 'Start Here', 'label': 'Orientation',
            'title': 'What this chapter is really for',
            'html': """
<p>Split at slide 30: <strong>Part 1 (1&ndash;29)</strong> is MVC, database theory and basic Sequelize
CRUD; <strong>Part 2 (30&ndash;46)</strong> is richer queries, associations and validators.</p>

<p>Notice the shape of the chapter. It opens with a <em>problem</em> &mdash; many API endpoints in one
file becomes difficult to maintain and debug &mdash; and its answer is MVC, which is presented as an
application of <strong>separation of concerns</strong>, called on slide 4 &ldquo;probably the most
important principle in software engineering&rdquo;. That is the same principle CSS was justified with
back in chapter 3. It is a very likely exam question precisely because it ties the whole course
together.</p>

<div class="grid-2">
  <div class="card">
    <h4>The conceptual half</h4>
    <p>MVC and its three parts. SQL vs NoSQL, and what data integrity and data consistency actually
    mean. Key-value stores vs document stores. Why an ORM is worth using. The CRUD-to-HTTP-verb table.
    All short slides, all easy marks if learned.</p>
  </div>
  <div class="card">
    <h4>The code half</h4>
    <p>Configure, connect, define a model, sync. Then five route handlers, the <code>Op</code>
    operators, associations, and validators. Every handler has the same shape &mdash; learn that shape
    once and the rest is filling in a blank.</p>
  </div>
</div>

<div class="hook"><strong>Every Sequelize route in this chapter is the same five lines:</strong>
<code>router.METHOD(path, async (req, res) =&gt; {</code> &rarr; <code>try {</code> &rarr;
<code>await Model.someQuery({...})</code> &rarr; <code>res.status(n).json(result)</code> &rarr;
<code>} catch (error) { res.json(error) }</code>. If you can type that skeleton blind, every code
question in the chapter reduces to knowing which query and which options object.</div>
"""
        },
        {
            'id': 'map', 'nav': 'Slide Map', 'label': 'Navigation',
            'title': 'All 47 slides, weighted',
            'html': slidemap([
                ('1&ndash;2', 'Title; technical notes', 'SKIM',
                 'Use a local MySQL server, or the free online service at <code>aiven.io</code>. You need this for the slide 46 task.'),
                ('3&ndash;5', 'The complex server problem; MVC', 'MEMORIZE',
                 'Highest-value conceptual slide in the chapter. Learn all three roles and the separation-of-concerns justification.'),
                ('6&ndash;7', 'The role of databases; DBMS options', 'MEMORIZE',
                 'The design principle: separate static content from dynamic content. Appearance (HTML/CSS) is static; data is dynamic.'),
                ('8&ndash;9', 'NoSQL; why and why not', 'MEMORIZE',
                 'NoSQL = <strong>Not-only-SQL</strong>. Learn the definitions of data integrity and data consistency word for word &mdash; they are given as formal definitions.'),
                ('10&ndash;11', 'Key-value stores; document stores', 'MEMORIZE',
                 'Key-value stores are analogous to Maps. A document store calls the value a <em>document</em> &mdash; a binary file, or semi-structured XML or JSON.'),
                ('12&ndash;14', 'MongoDB; relational vs document data', 'MEMORIZE',
                 'Data goes in as JSON and is stored as BSON. Know what MongoDB does <strong>not</strong> support: transactions (before 4.0) and joins &mdash; it uses nested documents instead.'),
                ('15&ndash;16', 'How websites use databases; ORM libraries', 'MEMORIZE',
                 'Three ORM advantages: fewer injection risks, simpler database communication, and the ability to change database system without changing your code.'),
                ('17&ndash;19', 'Sequelize; configuring and connecting', 'WRITE',
                 '<code>npm install sequelize mysql2</code> &mdash; you need a driver as well as the ORM. Learn the four constructor arguments.'),
                ('20', 'Creating the data model', 'WRITE',
                 'The densest code slide in Part 1. Note that a model called <code>Employee</code> produces a table called <code>employees</code>, and what <code>sync({alter:true})</code> does.'),
                ('21', 'CRUD and HTTP methods', 'MEMORIZE',
                 'The four-row table. Guaranteed to appear in some form, and it reaches back to chapter 1.'),
                ('22', 'Designing the API routes', 'MEMORIZE',
                 'Note which routes return web pages and which return JSON, and the modularity argument for the shared <code>/api/employees/v1/</code> prefix.'),
                ('23&ndash;24', 'Creating a record; testing the endpoint', 'WRITE',
                 '<code>build()</code> then <code>save()</code>. Status <strong>201</strong> means "resource created" &mdash; not 200.'),
                ('25&ndash;28', 'findAll, findOne, criteria, projections', 'WRITE',
                 'A projection means selecting which properties you want back &mdash; because some properties should stay secret.'),
                ('29&ndash;31', 'VS Code extensions; connecting from VS Code', 'SKIM',
                 'Practical setup for the class task. MySQL and Thunder Client extensions.'),
                ('32&ndash;33', 'Generating mock data', 'SKIM',
                 'Useful for testing, but read it &mdash; the mock config shows the full Employee schema including <code>city</code>, <code>age</code> and the timestamps.'),
                ('34&ndash;38', 'WHERE clauses: AND, OR, delete, not equal, gt/lt', 'WRITE',
                 'All five use the <code>Op</code> object, which must be imported. Learn the operator names.'),
                ('39', 'Bulk create at table creation', 'WRITE',
                 'The <code>count()</code> guard is the interesting part &mdash; only seed if the table is empty.'),
                ('40&ndash;41', 'Model associations', 'WRITE',
                 '<code>hasMany</code> + <code>belongsTo</code>. Know which side gets the foreign key and what it is named.'),
                ('42&ndash;45', 'Validation vs constraints; the validator list', 'MEMORIZE',
                 'The distinction on slide 42 is the examinable one. Validations run in JavaScript before any SQL is sent; constraints are enforced by the database.'),
                ('46', 'Class task', 'WRITE',
                 'Do it end to end. It is the practical exam in miniature.'),
            ])
        },
        {
            'id': 'concepts', 'nav': 'Concepts', 'label': 'Slides 3&ndash;16',
            'title': 'MVC, SQL vs NoSQL, and why an ORM',
            'html': """
<h3>MVC &mdash; learn all three roles</h3>
<p>The problem it solves, stated on slide 3: when you have many API endpoints you end up with a
complex file that becomes difficult to maintain and debug.</p>
""" + table(['Part', 'Responsibility', 'In this course'], [
                ('<strong>Model</strong>', 'The parts of the application that <strong>store</strong> the data (the database) and <strong>manipulate</strong> it &mdash; save, update, delete, retrieve.', 'Your Sequelize models and queries.'),
                ('<strong>View</strong>', 'The code responsible for <strong>presenting</strong> data to the user &mdash; web pages, mobile interface, GUI.', 'Your EJS templates from chapter 6, and the HTML/CSS from chapters 2&ndash;3.'),
                ('<strong>Controller</strong>', '<strong>Links</strong> model and view. Selects the view that will present the data, selects the model operation to execute, and returns the results to the view.', 'The Express router plus your business logic &mdash; the slides say so explicitly.'),
            ]) + hook(
                "<strong>The sentence to write in an exam:</strong> MVC is an application of "
                "<em>separation of concerns</em>, probably the most important principle in software "
                "engineering. Its advantages: the code is more maintainable, and it is easier to "
                "provide different views of the same data &mdash; adding a mobile app to an existing "
                "web app, for instance. That is the same principle used to justify CSS in chapter 3.") + """

<h3>Why databases at all</h3>
<p>Databases implement an important software design principle: <strong>separate static content from
dynamic content</strong>. On the web, the visual appearance &mdash; the HTML and CSS &mdash; is
static, while the data content changes.</p>

<h3>SQL vs NoSQL</h3>
<p><strong>NoSQL stands for Not-only-SQL</strong>: a category of database software that does not use
the relational table model. These systems rely on a different set of ideas for data modelling that
<strong>put fast retrieval ahead of other considerations like consistency</strong>.</p>
""" + table(['', 'Relational (SQL)', 'NoSQL'], [
                ('<strong>Examples</strong>', 'SQLite, MySQL, PostgreSQL, Oracle Database, IBM DB2, Microsoft SQL Server.', 'Cassandra, Firebase, MongoDB, DynamoDB.'),
                ('<strong>Model</strong>', 'Tables with a schema.', 'Key-value stores, document stores and others.'),
                ('<strong>Strength</strong>', 'Schemas ensure <strong>data integrity</strong> and <strong>data consistency</strong>.', 'Handles huge datasets better than relational systems.'),
                ('<strong>Trade-off</strong>', 'Less comfortable with very large datasets.', 'Not the best answer for all scenarios &mdash; you give up the guarantees a schema provides.'),
            ]) + """
<div class="card">
  <h4>Two definitions to learn verbatim</h4>
  <p><strong>Data integrity:</strong> the guarantee of all data constraints &mdash; primary and
  foreign keys, data types, and so on.</p>
  <p><strong>Data consistency:</strong> the guarantee that database constraints are not violated when
  executing transactions.</p>
</div>

<h3>Two NoSQL families</h3>
""" + table(['Key-value store', 'Document store'], [
                ('Every value &mdash; integer, string, or other data structure &mdash; has an associated key. <strong>Analogous to Maps.</strong>',
                 'Also associates keys with values, but calls the value a <strong>document</strong>.'),
                ('Allows fast retrieval through means such as a hash function, so there is no need for indexes on multiple fields as there is in SQL.',
                 'A document can be a binary file such as a <code>.doc</code> or <code>.pdf</code>, or a semi-structured XML or JSON document.'),
                ('Examples: DBM, Berkeley DB.',
                 '<strong>Most NoSQL systems are of this type.</strong> MongoDB, AWS DynamoDB, Google Firebase, Cloud Datastore.'),
            ]) + """
<h4>MongoDB specifically</h4>
<ul>
  <li>Open-source, NoSQL, <strong>document-oriented</strong>. Usable with any backend, but much more commonly used with Node.</li>
  <li>You package data as a <strong>JSON</strong> object and MongoDB stores it as a binary JavaScript object &mdash; <strong>BSON</strong>.</li>
  <li>It does <strong>not support transactions</strong> (before version 4.0) and does <strong>not support joins</strong> &mdash; it uses <strong>nested documents</strong> instead.</li>
  <li>Running on multiple servers means it handles large datasets: <strong>replication gives redundancy and high availability</strong>.</li>
</ul>

<h3>ORM libraries</h3>
<p>An Object Relational Mapping library lets you use an API to query databases <strong>without using
database-specific queries</strong>, giving a layer of abstraction that makes your code independent of
the database system underneath.</p>
""" + table(['ORM advantage', 'What it means in practice'], [
                ('Reduces security risks', 'SQL and non-SQL injection are much harder when you never concatenate a query string yourself.'),
                ('Simplifies database communication', 'You write <code>Employee.findAll()</code> rather than SQL plus connection plumbing.'),
                ('Allows changing the database system without changing your code', 'Swap the <code>dialect</code>, keep the queries.'),
            ]) + """
<p><strong>Sequelize</strong> supports MySQL, DB2, SQL Server and more. It needs a
<strong>database driver</strong> as well &mdash; the API Sequelize uses to reach a particular system.
The stack is: Express server app &rarr; Sequelize &rarr; DB driver for MySQL &rarr; MySQL DB server.</p>
""" + code('terminal', """
npm install sequelize mysql2      <span class="c"># the ORM AND the driver — both are needed</span>
""", note='Slide 17')
        },
        {
            'id': 'setup', 'nav': 'Model &amp; CRUD', 'label': 'Slides 18&ndash;28',
            'title': 'Configure, model, and the five CRUD handlers',
            'html': """
<h3>Configure and connect</h3>
""" + code('config/database.js', """
<span class="c">// 1 — import the sequelize library</span>
<span class="k">const</span> Sequelize = require(<span class="s">'sequelize'</span>);

<span class="c">// 2 — create a configured Sequelize object with our connection data</span>
<span class="k">const</span> sequelize = <span class="k">new</span> Sequelize(
    <span class="s">'se371db'</span>,      <span class="c">// database name</span>
    <span class="s">'se371'</span>,        <span class="c">// database user</span>
    <span class="s">'se371pwd'</span>,     <span class="c">// user password</span>
    {
        dialect: <span class="s">'mysql'</span>,     <span class="c">// which database server — change this to switch DBMS</span>
        host: <span class="s">'localhost'</span>     <span class="c">// a local db, so localhost</span>
    }
);

<span class="c">// 3 — connect. authenticate() is async, so await it inside try/catch.</span>
<span class="k">const</span> connectToDB = <span class="k">async</span> () =&gt; {
    <span class="k">try</span> {
        <span class="k">await</span> sequelize.authenticate();
        console.log(`Successfully connected to database server...`);
    } <span class="k">catch</span> (error) {
        console.log(error);
    }
};

module.exports = { sequelize, connectToDB };
""", note='Slides 18–19') + """

<h3>The data model</h3>
""" + code('models/employee.js', """
<span class="k">const</span> db = require(<span class="s">"../config/database"</span>);          <span class="c">// the connection object</span>
<span class="k">const</span> { DataTypes } = require(<span class="s">'sequelize'</span>);       <span class="c">// the type definitions</span>

<span class="k">const</span> Employee = db.sequelize.define(<span class="s">'Employee'</span>, {

    id: {
        type: DataTypes.INTEGER,
        primaryKey: <span class="k">true</span>
    },
    <span class="c">// ↑ NOTE: a model named 'Employee' creates a table named 'employees'
    //   — Sequelize pluralises and lower-cases it automatically.</span>

    name: {
        type: DataTypes.STRING,
        allowNull: <span class="k">false</span>,          <span class="c">// a CONSTRAINT — enforced by the database</span>
        validate: { max: <span class="s">100</span> }      <span class="c">// a VALIDATION — enforced by Sequelize</span>
    },

    position: {
        type: DataTypes.STRING,
        defaultValue: <span class="s">"Developer"</span>
    }
});

<span class="c">// Apply the model to the actual database.
//   table missing  → it is CREATED
//   table exists   → changes are APPLIED to its structure</span>
db.sequelize.sync({ alter: <span class="k">true</span> });

module.exports = Employee;
""", note='Slide 20') + """

<h3>CRUD &rarr; HTTP verb &rarr; Express function</h3>
""" + table(['Database operation', 'HTTP method', 'Why', 'Express function'], [
                ('<strong>Create</strong>', '<code>POST</code>', 'Used to create new data in the backend.', '<code>app.post()</code>'),
                ('<strong>Read</strong>', '<code>GET</code>', 'The default &mdash; used to get a resource from the server: a webpage, CSS file, image, data.', '<code>app.get()</code>'),
                ('<strong>Update</strong>', '<code>PUT</code>', 'Used to update existing data in the backend.', '<code>app.put()</code>'),
                ('<strong>Delete</strong>', '<code>DELETE</code>', 'Used to delete data.', '<code>app.delete()</code>'),
            ]) + hook(
                "<strong>Remember chapter 2 slide 43:</strong> an HTML form can only use "
                "<code>get</code> or <code>post</code>. PUT and DELETE have to be sent from "
                "JavaScript &mdash; which is exactly what <code>fetch</code> from chapter 6 is for. "
                "The two facts are one question waiting to be asked together.") + """

<h3>Designing the routes</h3>
""" + table(['Operation', 'Route', 'Method', 'Returns'], [
                ('Open the home page', '<code>/</code>', '<code>GET</code>', 'A web page'),
                ('Open the form page', '<code>/employees/</code>', '<code>GET</code>', 'A web page'),
                ('Retrieve', '<code>/api/employees/v1/</code><br><code>/api/employees/v1/id/:id</code><br><code>/api/employees/v1/position/:position</code>', '<code>GET</code>', 'JSON'),
                ('Create', '<code>/api/employees/v1/</code> (using a form)<br><code>/api/employees/v1/id/:id/name/:name/position/:position</code>', '<code>POST</code>', 'JSON'),
                ('Update', '<code>/api/employees/v1/id/:id/name/:name/position/:position</code>', '<code>PUT</code>', 'JSON'),
                ('Delete', '<code>/api/employees/v1/id/:id</code>', '<code>DELETE</code>', 'JSON'),
            ]) + """
<p>The reason for the shared <code>/api/employees/v1/</code> prefix is given on the slide:
<strong>you can create a router that handles only employee-related operations, which gives better
modularity in your code</strong>. The <code>v1</code> is API versioning &mdash; it lets you ship a
<code>v2</code> later without breaking existing clients.</p>

<h3>The five handlers</h3>
""" + code('CREATE — slide 23', """
app.post(<span class="s">'/api/employees/v1/'</span>, <span class="k">async</span> (request, response) =&gt; {
    <span class="k">const</span> { id, name, position } = request.body;    <span class="c">// destructuring (ch. 4)</span>

    <span class="k">const</span> newEmployee = Employee.build({
        <span class="s">"id"</span>: id, <span class="s">"name"</span>: name, <span class="s">"position"</span>: position
    });

    <span class="k">try</span> {
        <span class="k">await</span> newEmployee.save();
        response.status(<span class="s">201</span>).json(newEmployee);      <span class="c">// 201 = RESOURCE CREATED, not 200</span>
    } <span class="k">catch</span> (error) {
        response.json(error);
    }
});

<span class="c">// build() makes the object in memory; save() writes it to the database.
// Employee.create({...}) does both in one call.
//
// Testing it (slide 24): change the method to POST, set the URL, and send
// the test data as a JSON body. The 201 response comes back with the
// record plus metadata Sequelize added (createdAt, updatedAt).</span>
""", note='Slides 23–24') + code('READ — slides 25–28', """
<span class="c">// ── SELECT ALL ─────────────────────────────────────────────────</span>
router.get(<span class="s">'/api/employees/v1/'</span>, <span class="k">async</span> (request, response) =&gt; {
    <span class="k">const</span> employees = <span class="k">await</span> Employee.findAll();
    response.status(<span class="s">200</span>).json({ employees: employees });   <span class="c">// a JSON ARRAY</span>
});

<span class="c">// ── SEARCH BY ID — findOne returns ONE object ──────────────────</span>
router.get(<span class="s">'/employees/v1/:id'</span>, <span class="k">async</span> (request, response) =&gt; {
    <span class="k">try</span> {
        <span class="k">const</span> employee = <span class="k">await</span> Employee.findOne({
            where: { id: request.params.id }         <span class="c">// req.params — chapter 6</span>
        });
        response.status(<span class="s">200</span>).json(employee);
    } <span class="k">catch</span> (error) {
        response.json(error);
    }
});

<span class="c">// ── SEARCH BY CRITERIA — findAll returns an ARRAY ──────────────</span>
router.get(<span class="s">'/employees/v1/position/:position'</span>, <span class="k">async</span> (request, response) =&gt; {
    <span class="k">try</span> {
        <span class="k">const</span> employee = <span class="k">await</span> Employee.findAll({
            where: { position: request.params.position }
        });
        response.status(<span class="s">200</span>).json(employee);
    } <span class="k">catch</span> (error) {
        response.json(error);
    }
});

<span class="c">// ── PROJECTION — choose WHICH properties come back ─────────────
//    "some properties should stay secret"</span>
router.get(<span class="s">'/employees/v1/position/:position'</span>, <span class="k">async</span> (request, response) =&gt; {
    <span class="k">try</span> {
        <span class="k">const</span> employee = <span class="k">await</span> Employee.findAll({
            attributes: [<span class="s">'id'</span>, <span class="s">'name'</span>],           <span class="c">// ← the projection</span>
            where: { position: request.params.position }
        });
        response.status(<span class="s">200</span>).json(employee);
    } <span class="k">catch</span> (error) {
        response.json(error);
    }
});
""", note='Slides 25–28')
        },
        {
            'id': 'queries', 'nav': 'Queries', 'label': 'Slides 34&ndash;45',
            'title': 'Operators, associations and validators — Part 2',
            'html': """
<h3>The <code>Op</code> object &mdash; richer WHERE clauses</h3>
""" + code('operators.js', """
<span class="k">const</span> { Op } = require(<span class="s">'sequelize'</span>);   <span class="c">// MUST be imported — it defines the operations</span>

<span class="c">// ── AND — slide 34 ─────────────────────────────────────────────</span>
<span class="k">const</span> employee = <span class="k">await</span> Employee.findAll({
    where: {
        [Op.and]: [{ city: request.params.city },
                   { position: request.params.position }]
    }
});
<span class="c">//   the [Op.and] square brackets are a COMPUTED PROPERTY NAME — Op.and
//   is a symbol, not the literal text "Op.and".</span>

<span class="c">// ── OR — slide 35 ──────────────────────────────────────────────</span>
<span class="k">await</span> Employee.findAll({
    where: {
        [Op.or]: [{ city: request.params.city },
                  { position: request.params.position }]
    }
});

<span class="c">// ── NOT EQUAL — slide 37. Note it nests INSIDE the column. ─────</span>
<span class="k">await</span> Employee.findAll({
    where: { city: { [Op.ne]: request.params.city } }     <span class="c">// ne = not equal</span>
});

<span class="c">// ── LESS THAN — slide 38 ───────────────────────────────────────</span>
<span class="k">await</span> Employee.findAll({
    where: { age: { [Op.lt]: request.params.age } }       <span class="c">// lt / gt / lte / gte</span>
});

<span class="c">// ── DELETE, with a WHERE — slide 36 ────────────────────────────</span>
router.delete(<span class="s">'/employees/v1/city/:city'</span>, <span class="k">async</span> (request, response) =&gt; {
    <span class="k">try</span> {
        <span class="k">const</span> employee = <span class="k">await</span> Employee.destroy({
            where: { city: request.params.city }
        });
        response.status(<span class="s">200</span>).json(employee);   <span class="c">// returns the NUMBER of rows deleted</span>
    } <span class="k">catch</span> (error) {
        response.json(error);
    }
});
""", note='Slides 34–38') + """
<div class="card">
  <h4>Where the operator goes</h4>
  <p><strong>Combining conditions</strong> (<code>Op.and</code>, <code>Op.or</code>) &mdash; the
  operator is the <em>outer</em> key and takes an <strong>array</strong> of conditions.
  <strong>Comparing one column</strong> (<code>Op.ne</code>, <code>Op.lt</code>, <code>Op.gt</code>)
  &mdash; the operator goes <em>inside</em> that column&rsquo;s object. Getting this backwards is the
  most common Sequelize error in the chapter.</p>
</div>

<h3>Seeding data at creation</h3>
""" + code('bulk-create.js', """
db.sequelize.sync({ alter: <span class="k">true</span> })
    .then(<span class="k">async</span> () =&gt; {
        Country.count()                    <span class="c">// how many records are there?</span>
            .then(<span class="k">async</span> (count) =&gt; {
                <span class="k">if</span> (!count) {              <span class="c">// 0 is FALSY (chapter 4) → table empty</span>
                    <span class="k">await</span> Country.bulkCreate([
                        { name: <span class="s">"KSA"</span> },
                        { name: <span class="s">"Oman"</span> },
                        { name: <span class="s">"Egypt"</span> }
                    ]);
                }
            });
    });

<span class="c">// The count() guard is the point: re-run this whenever tables are
// deleted and recreated, without duplicating the seed data.</span>
""", note='Slide 39') + """

<h3>Model associations</h3>
""" + code('associations.js', """
<span class="k">const</span> Employee = db.sequelize.define(<span class="s">'Employee'</span>, { <span class="c">/* … */</span> });

<span class="c">// Every employee is associated with exactly one country</span>
<span class="k">const</span> Country = db.sequelize.define(<span class="s">'Country'</span>, {
    name: {
        type: DataTypes.STRING,
        unique: <span class="k">true</span>
    }
}, {
    timestamps: <span class="k">false</span>     <span class="c">// no createdAt/updatedAt — static, non-critical data</span>
});

<span class="c">// ── DECLARE THE RELATIONSHIP FROM BOTH SIDES ───────────────────</span>
Country.hasMany(Employee);      <span class="c">// one country → many employees</span>
Employee.belongsTo(Country);    <span class="c">// each employee → one country</span>

<span class="c">// CONSEQUENCES:
//   • Employee gets the FOREIGN KEY, named CountryId  (Model + Id)
//   • Employee instances gain a getter:  .getCountry()</span>

<span class="c">// ── USING IT — slide 41 ────────────────────────────────────────</span>
router.get(<span class="s">'/employees/v1/:id'</span>, <span class="k">async</span> (request, response) =&gt; {
    <span class="k">try</span> {
        <span class="k">const</span> employee = <span class="k">await</span> Employee.findOne({
            where: { id: request.params.id }
        });
        <span class="k">const</span> country = <span class="k">await</span> employee.getCountry();   <span class="c">// ← the enriched API</span>

        response.status(<span class="s">200</span>).json({ employee, country });
    } <span class="k">catch</span> (error) {
        response.json(error);
    }
});
""", note='Slides 40–41') + hook(
                "<strong>Which side gets the foreign key?</strong> The <em>many</em> side &mdash; the "
                "one that <code>belongsTo</code>. One country has many employees, so the key lives on "
                "<code>Employee</code> and is called <code>CountryId</code>. Compare this with MongoDB, "
                "which has no joins at all and nests the document instead.") + """

<h3>Validations vs constraints &mdash; the distinction to learn</h3>
""" + table(['', 'Validation', 'Constraint'], [
                ('<strong>Where</strong>', 'At the Sequelize level, in <strong>pure JavaScript</strong>.', 'At <strong>SQL level</strong> &mdash; rules defined in the database.'),
                ('<strong>On failure</strong>', '<strong>No SQL query is sent to the database at all.</strong>', 'An error is thrown <strong>by the database</strong>.'),
                ('<strong>Written as</strong>', 'A <code>validate: { … }</code> block.', 'Field options such as <code>allowNull: false</code> and <code>unique: true</code>.'),
            ]) + code('validation-vs-constraint.js', """
<span class="k">const</span> User = sequelize.define(<span class="s">'user'</span>, {
    username: {
        type: DataTypes.STRING,
        allowNull: <span class="k">false</span>,           <span class="c">// ← CONSTRAINT: not null, at SQL level</span>
        unique: <span class="k">true</span>,               <span class="c">// ← CONSTRAINT: unique, at SQL level</span>
    },
    hashedPassword: {
        type: DataTypes.STRING(<span class="s">64</span>),
        validate: {
            is: /^[<span class="s">0</span>-<span class="s">9</span>a-f]{<span class="s">64</span>}$/i,      <span class="c">// ← VALIDATION: enforced by Sequelize</span>
        },
    },
});

<span class="c">// The regex is chapter 5 material: ^ start, $ end, {64} exactly 64,
// [0-9a-f] hex characters, /i case-insensitive.</span>

<span class="c">// ── Using a validator — slide 45 ───────────────────────────────</span>
<span class="k">const</span> User = sequelize.define(<span class="s">'user'</span>, {
    email: {
        type: DataTypes.STRING,
        validate: { isEmail: <span class="k">true</span> }
    },
});

<span class="c">// Then in the controller:</span>
<span class="k">const</span> user = User.build({ username: <span class="s">'Salah'</span>, email: <span class="s">'salah'</span> });
<span class="k">if</span> (user.validate()) {
    <span class="k">try</span> {
        <span class="k">await</span> user.save();
    } <span class="k">catch</span> (error) { <span class="c">/* … */</span> }
}
""", note='Slides 42, 45') + """

<h4>The validator list &mdash; slides 43&ndash;44</h4>
""" + table(['Group', 'Validators'], [
                ('<strong>Pattern</strong>', '<code>is: /^[a-z]+$/i</code> matches this RegExp &middot; <code>not: /^[a-z]+$/i</code> does not match it'),
                ('<strong>Format</strong>', '<code>isEmail</code> &middot; <code>isUrl</code> &middot; <code>isIP</code> (IPv4 or IPv6) &middot; <code>isDate</code>'),
                ('<strong>Character type</strong>', '<code>isAlpha</code> letters only &middot; <code>isAlphanumeric</code> (so <code>"_abc"</code> fails) &middot; <code>isLowercase</code> &middot; <code>isUppercase</code>'),
                ('<strong>Numeric</strong>', '<code>isNumeric</code> &middot; <code>isInt</code> &middot; <code>isFloat</code> &middot; <code>isDecimal</code>'),
                ('<strong>Emptiness</strong>', '<code>notNull</code> &middot; <code>isNull</code> only allows null &middot; <code>notEmpty</code> no empty strings'),
                ('<strong>Value</strong>', '<code>equals: \'specific value\'</code> &middot; <code>contains: \'foo\'</code> &middot; <code>notContains: \'bar\'</code> &middot; <code>isIn: [[\'foo\',\'bar\']]</code> &middot; <code>notIn: [[\'foo\',\'bar\']]</code>'),
                ('<strong>Range</strong>', '<code>len: [2,10]</code> &middot; <code>min: 23</code> allows values &ge; 23 &middot; <code>max: 23</code> allows values &le; 23 &middot; <code>isAfter: "2011-11-05"</code> &middot; <code>isBefore: "2011-11-05"</code>'),
            ]) + """
<p>Map these back onto the six validation types from chapter 2 slide 66 &mdash; required, correct data
type, correct format, comparison, range check, custom. Every one of them has a Sequelize validator,
and that is the full-circle answer to "where should validation happen".</p>
"""
        },
        {
            'id': 'traps', 'nav': 'Traps', 'label': 'Marks Lost Here',
            'title': 'The seven things people get wrong',
            'html': (
                trap('Returning 200 for a created resource',
                     'Slide 23 sends <code>response.status(201)</code> and slide 24 spells out why: 201 means "resource created". Returning 200 is not an error the code will catch, but it is wrong and it is marked.',
                     '<code>201</code> for a successful create, <code>200</code> for a successful read or update. Chapter 1&rsquo;s status-code families are being tested again here.') +
                trap('Putting <code>Op.ne</code> in the wrong place',
                     '<code>where: { [Op.ne]: { city: x } }</code> does not work. Column-comparison operators nest <em>inside</em> the column, while <code>Op.and</code> and <code>Op.or</code> sit outside and take an array.',
                     'Combining conditions &rarr; operator outside, array inside. Comparing a column &rarr; column outside, operator inside: <code>where: { city: { [Op.ne]: x } }</code>.') +
                trap('Forgetting to import <code>Op</code>',
                     'Slide 34 opens with the import for a reason. Without <code>const { Op } = require(\'sequelize\')</code> the symbol is undefined and the where clause silently does not filter the way you meant.',
                     'Import it at the top of any file that uses an operator.') +
                trap('Confusing a validation with a constraint',
                     'Both prevent bad data, but the exam asks <em>where</em> the check happens. A validation fails in JavaScript and <strong>no SQL query is sent at all</strong>; a constraint fails at the database, which throws the error back.',
                     'Field-level options (<code>allowNull</code>, <code>unique</code>) are constraints. Anything inside <code>validate: {}</code> is a validation.') +
                trap('Expecting the foreign key on the wrong table',
                     'With <code>Country.hasMany(Employee)</code> and <code>Employee.belongsTo(Country)</code>, people look for an employees column on <code>Country</code>. It is not there.',
                     'The foreign key goes on the <em>many</em> side &mdash; on <code>Employee</code>, named <code>CountryId</code>. The convention is model name plus <code>Id</code>.') +
                trap('Trying to send PUT or DELETE from an HTML form',
                     'The route is <code>app.delete(...)</code>, the form says <code>method="delete"</code>, and the browser quietly sends a GET instead. Chapter 2 slide 43 already warned that forms accept only GET and POST.',
                     'Send PUT and DELETE with <code>fetch</code> from JavaScript, or test them with a client such as Thunder Client.') +
                trap('Getting <code>findOne</code> and <code>findAll</code> the wrong way round',
                     '<code>findAll</code> always returns an <strong>array</strong>, even when it matches exactly one row &mdash; so <code>result.name</code> is <code>undefined</code>. <code>findOne</code> returns the object itself, or <code>null</code>.',
                     'Searching by primary key &rarr; <code>findOne</code>. Searching by any other criteria &rarr; <code>findAll</code>, then index into the array.')
            )
        },
        {
            'id': 'cheat', 'nav': 'Cheat Sheet', 'label': 'One Screen',
            'title': 'Chapter 7 on a single screen',
            'html': cheat([
                ('MVC', [
                    '<strong>Model</strong> &mdash; stores and manipulates data',
                    '<strong>View</strong> &mdash; presents data to the user',
                    '<strong>Controller</strong> &mdash; links the two (Express router + logic)',
                    'An application of separation of concerns',
                ]),
                ('SQL vs NoSQL', [
                    'NoSQL = <strong>Not-only-SQL</strong>',
                    'Puts fast retrieval ahead of consistency',
                    'Schemas give integrity + consistency',
                    'Key-value store &asymp; a Map',
                    'Document store &mdash; most NoSQL systems',
                ]),
                ('MongoDB', [
                    'Document-oriented, JSON in, <strong>BSON</strong> stored',
                    'No transactions (before 4.0)',
                    'No joins &mdash; uses nested documents',
                    'Replication &rarr; redundancy + high availability',
                ]),
                ('CRUD', [
                    'Create &rarr; <code>POST</code> &rarr; <code>app.post()</code>',
                    'Read &rarr; <code>GET</code> &rarr; <code>app.get()</code>',
                    'Update &rarr; <code>PUT</code> &rarr; <code>app.put()</code>',
                    'Delete &rarr; <code>DELETE</code> &rarr; <code>app.delete()</code>',
                    'Forms can only send GET and POST',
                ]),
                ('Sequelize setup', [
                    '<code>npm install sequelize mysql2</code>',
                    '<code>new Sequelize(db, user, pwd, {dialect, host})</code>',
                    '<code>await sequelize.authenticate()</code>',
                    '<code>db.sequelize.define(\'Employee\', {…})</code>',
                    '<code>sync({ alter: true })</code>',
                    '<code>Employee</code> model &rarr; <code>employees</code> table',
                ]),
                ('Queries', [
                    '<code>Model.build({}) </code> then <code>.save()</code>',
                    '<code>Model.findAll()</code> &rarr; array',
                    '<code>Model.findOne({where})</code> &rarr; object or null',
                    '<code>Model.destroy({where})</code> &rarr; rows deleted',
                    '<code>attributes: [\'id\',\'name\']</code> &mdash; projection',
                    '<code>Model.bulkCreate([…])</code>',
                ]),
                ('Operators', [
                    '<code>const { Op } = require(\'sequelize\')</code>',
                    '<code>[Op.and]: [ {}, {} ]</code> &mdash; outside',
                    '<code>[Op.or]: [ {}, {} ]</code> &mdash; outside',
                    '<code>col: { [Op.ne]: v }</code> &mdash; inside',
                    '<code>[Op.lt]</code> <code>[Op.gt]</code> <code>[Op.lte]</code> <code>[Op.gte]</code>',
                ]),
                ('Associations', [
                    '<code>Country.hasMany(Employee)</code>',
                    '<code>Employee.belongsTo(Country)</code>',
                    'Foreign key on the MANY side: <code>CountryId</code>',
                    'Gives <code>employee.getCountry()</code>',
                ]),
                ('Validation vs constraint', [
                    '<strong>Validation</strong> &mdash; JavaScript, no SQL sent',
                    '<strong>Constraint</strong> &mdash; SQL level, DB throws',
                    '<code>allowNull</code> <code>unique</code> &rarr; constraints',
                    '<code>validate: { isEmail, len, min, max, is }</code>',
                ]),
            ])
        },
        {
            'id': 'drills', 'nav': 'Drills', 'label': 'Build It',
            'title': 'Do the class task, then extend it',
            'html': """
<p>Slide 46 sets the task and it is worth treating as the practical exam: create an account on
<code>aiven.io</code>, create <code>se371db</code>, install the MySQL and Thunder Client extensions,
connect, and exercise GET, POST, DELETE and PUT. Everything below builds on that.</p>
""" + drills([
                'Write the MVC definition from memory, then label which files in your chapter 6 project are model, view and controller.',
                'Define data integrity and data consistency in one sentence each, without looking.',
                'Complete the class task end to end: aiven account, database, extensions, connection, and all four verbs tested.',
                'Write the Sequelize configuration and connection code from memory, including the try/catch.',
                'Define the <code>Employee</code> model with an id primary key, a non-null name with a max length, and a position with a default value.',
                'Run <code>sync({alter: true})</code>, then add a field to the model and run it again &mdash; watch the table structure change.',
                'Generate a hundred mock rows using the slide 32 configuration, including <code>city</code> and <code>age</code>.',
                'Write all four CRUD handlers and confirm the create route returns <strong>201</strong>, not 200.',
                'Add a projection so one route returns only <code>id</code> and <code>name</code>, and explain in a comment why you would want that.',
                'Write an AND query and an OR query, then swap where the operator sits and read the error.',
                'Write a not-equal query and a less-than query &mdash; note that these operators go <em>inside</em> the column.',
                'Write a delete-by-criteria route and check what the return value actually is.',
                'Add a <code>Country</code> model with a unique name and no timestamps, associate it both ways, and find the foreign key column in the employees table.',
                'Seed three countries with <code>bulkCreate</code>, guarded by <code>count()</code>, then drop the table and restart to confirm the guard works.',
                'Add one validation and one constraint to the same model, break each in turn, and compare the two error messages.',
                'Take the six validation types from chapter 2 slide 66 and write a Sequelize validator for each one.',
                'Finally: wire an EJS page from chapter 6 to display <code>findAll()</code> results in a table. That is the whole course in one file.',
            ]) + """
<p>There is no chapter-7 example folder in your study material, but two solved labs cover this ground:
<a href="/academics/software-engineering/se371/extra-resources/resource-viewers/lab-10-solution-4dbe568d/" target="_blank" rel="noopener">lab 10</a> and
<a href="/academics/software-engineering/se371/extra-resources/resource-viewers/lab-11-solution-405367e1/" target="_blank" rel="noopener">lab 11</a>.
The full code repository for every chapter is at <code>github.com/skanderturki/se371</code>.</p>
"""
        },
    ],
    'quiz': [
        {'tag': 'MVC', 'q': 'In this course\'s MVC breakdown, what plays the role of the controller?',
         'opts': ['The Sequelize models', 'The EJS templates',
                  'The Express router plus the business logic', 'The database driver'],
         'a': 2,
         'why': 'Slide 4 says so directly. The controller links model and view: it selects which view presents the data, selects the model operation to run, and returns the results.'},
        {'tag': 'NoSQL', 'q': 'What does NoSQL stand for?',
         'opts': ['No SQL allowed', 'Not-only-SQL', 'Non-Structured Query Language', 'Nested Object SQL'],
         'a': 1,
         'why': 'Not-only-SQL — a category of database software that does not use the relational table model, prioritising fast retrieval over considerations such as consistency.'},
        {'tag': 'MongoDB', 'q': 'Which does MongoDB NOT support?',
         'opts': ['Replication', 'Storing JSON data', 'Joins', 'Running on multiple servers'],
         'a': 2,
         'why': 'MongoDB has no joins — it uses nested documents instead — and had no transactions before version 4.0. Replication across multiple servers is one of its strengths.'},
        {'tag': 'CRUD', 'q': 'Which HTTP method should be used to update existing data in the backend?',
         'opts': ['<code>POST</code>', '<code>GET</code>', '<code>PUT</code>', '<code>PATCH</code>'],
         'a': 2,
         'why': 'PUT for update, POST for create, GET for read and DELETE for delete. Note that an HTML form can only send GET or POST, so PUT and DELETE must go through fetch.'},
        {'tag': 'Sequelize', 'q': 'Which status code does the create endpoint return on success?',
         'opts': ['<code>200</code>', '<code>201</code>', '<code>204</code>', '<code>301</code>'],
         'a': 1,
         'why': 'Slide 24 states it: the client receives 201, meaning "resource created", along with the record and the metadata Sequelize added.'},
        {'tag': 'Queries', 'q': 'Which where clause finds employees NOT in a given city?',
         'opts': ['<code>where: { [Op.ne]: { city: x } }</code>', '<code>where: { city: { [Op.ne]: x } }</code>',
                  '<code>where: { [Op.not]: [{ city: x }] }</code>', '<code>where: { city: !x }</code>'],
         'a': 1,
         'why': 'Comparison operators nest inside the column object. Only the combining operators, Op.and and Op.or, sit at the outer level and take an array of conditions.'},
        {'tag': 'Associations', 'q': 'After Country.hasMany(Employee) and Employee.belongsTo(Country), where does the foreign key live?',
         'opts': ['On Country, as EmployeeId', 'On Employee, as CountryId',
                  'In a separate join table', 'On both models'],
         'a': 1,
         'why': 'The foreign key goes on the many side — the one that belongsTo — and is named after the model plus Id. Employee instances also gain a getCountry() getter.'},
        {'tag': 'Validation', 'q': 'A Sequelize validation fails. What happens next?',
         'opts': ['The database throws a constraint error', 'No SQL query is sent to the database at all',
                  'The row is inserted and then rolled back', 'The value is silently replaced by the default'],
         'a': 1,
         'why': 'Validations are checks performed at the Sequelize level in pure JavaScript, so nothing reaches the database. Constraints are the SQL-level rules, and those fail at the database.'},
    ],
})
