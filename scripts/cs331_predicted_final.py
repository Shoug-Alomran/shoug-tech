"""CS331 predicted final exam (Term 261), rendered by build_cs331_past_papers.py.

Not a past paper: a prediction written in the format the instructors used in the
Term 261 majors (sections per chapter group, scenario stems with lettered parts,
0.25 and 0.5 mark pieces, word boxes, OSI matching tables, parity and bit-stuffing
working, VLAN tables, subnetting on a drawn network, domain counting and switch
learning tables). Chapters 8, 9 and 10 have not been examined by a major yet, so
they get their own parts. Every number was recomputed.

Final scope: the Physical Layer (Chapter 2) and CRC/checksum calculations are not
on the final, so the paper has no Chapter 2 questions and asks about CRC and the
checksum as concepts only.

The questions are not registered in ALL, so the questions-by-chapter page keeps
listing real past questions only.
"""


def build(h):
    txt, num, sel, written, mcq_html, S, ip = h.txt, h.num, h.sel, h.written, h.choose, h.S, h.ip
    OSI, word_box, grid_table, sheet = h.OSI, h.word_box, h.grid_table, h.sheet

    class PQ(h.Q):
        def __init__(self, ch, no, marks, body, why=""):
            self.ch, self.src, self.no, self.marks = ch, "pf", no, marks
            self.body, self.why, self.ctx = body, why, ""

    def mc(ch, no, stem, options, answer, why, marks=0.5):
        return PQ(ch, no, marks, lambda: f'<p class="q-text">{stem}</p>{mcq_html(options, answer, marks, h.ABCD)}', why)

    q = {}

    # ---------------------------------------------------------- Part 1: MCQs
    mcqs = [
        (1, "A company connects its office in Riyadh to its office in Dammam (about 400 km away) so employees can share files and printers. What type of network is this?",
         ["LAN, because only one company owns it.", "MAN, because both offices are in Saudi Arabia.", "WAN, because it connects sites in different cities over a long distance.", "PAN, because only employees use it."], 2,
         "Size decides the type: LAN = a building or campus, MAN = one city, WAN = across cities or countries. Riyadh to Dammam spans two cities, so it is a WAN. Ownership doesn't decide it."),
        (1, "Two branch offices use a link on which both sides can send and receive at the same moment, like a telephone call. What is this data flow mode?",
         ["Simplex", "Half-duplex", "Full-duplex", "Multipoint"], 2,
         "Full-duplex = both directions at the same time (telephone). Half-duplex = both directions but one at a time (walkie-talkie). Simplex = one direction only (keyboard). Multipoint describes how many devices share a link, not the direction."),
        (3, "In byte-oriented framing, the data contains a byte with the same pattern as the flag. What does the sender do?",
         ["Discards the frame and sends a NAK.", "Inserts an escape (ESC) byte before it (byte stuffing).", "Inserts a 0 after five consecutive 1s (bit stuffing).", "Changes the flag to a different pattern."], 1,
         "Byte stuffing: an ESC byte goes in front of any flag or ESC pattern in the data, and the receiver removes it. Inserting a 0 after five 1s is bit stuffing, used in bit-oriented framing."),
        (3, "A code has a minimum Hamming distance of 4. How many bit errors can it guarantee to DETECT?",
         ["1", "2", "3", "4"], 2,
         "To detect s errors you need d<sub>min</sub> = s + 1, so s = 4 − 1 = 3. (To correct t errors you need d<sub>min</sub> = 2t + 1, so this code corrects only 1.)"),
        (4, "A frame arrives with destination address 4A:30:10:21:10:1A. What type of address is it?",
         ["Unicast, because the second hex digit of the first byte is even.", "Multicast, because the address starts with 4.", "Broadcast, because it contains the digit A.", "Multicast, because the last byte is odd."], 0,
         "Look at the least significant bit of the <b>first</b> byte: 4A = 0100 1010, last bit 0 → unicast. If it were 1, it would be multicast. Broadcast is all Fs."),
        (6, "Which device can join two LAN segments and forward a frame only to the segment where the destination MAC address is?",
         ["Hub", "Repeater", "Link-layer switch", "Passive hub"], 2,
         "A switch has a MAC table and filters: it forwards only out of the port where the destination was learned. Hubs and repeaters work at layer 1 and copy bits to every port."),
        (7, "Why does a new computer send its DHCPDISCOVER message as a broadcast?",
         ["Because DHCP only works with broadcasts.", "Because it does not yet have an IP address and does not know the DHCP server's address.", "To find the default gateway's MAC address.", "To ask the DNS server for its name."], 1,
         "Before DHCP the client has no IP and doesn't know where the server is, so it uses source 0.0.0.0 and destination 255.255.255.255. Finding a MAC address is ARP's job."),
        (8, "RIP is an example of which routing approach, and what metric does it use?",
         ["Link state, using bandwidth", "Distance vector, using hop count", "Path vector, using AS paths", "Link state, using delay"], 1,
         "RIP = distance vector with hop count (maximum 15; 16 = unreachable). OSPF is link state (Dijkstra); BGP is path vector between autonomous systems."),
        (9, "A video-calling application must keep delay low and can tolerate a few lost packets. Which transport protocol suits it?",
         ["TCP, because it retransmits every lost segment.", "UDP, because it has no handshake or retransmission delay.", "TCP, because it guarantees order.", "Neither: video calls use IP directly."], 1,
         "Real-time audio and video prefer UDP: a retransmitted packet would arrive too late to play. File transfer, email and the web need TCP's reliability."),
        (10, "A local DNS server answers a repeated query for www.psu.edu.sa from its cache. What stops it from using that answer forever?",
         ["The root server deletes it every hour.", "Each cached record has a Time-To-Live (TTL); it is removed when the TTL expires.", "The client sends an ARP request to refresh it.", "Caching is not allowed in DNS."], 1,
         "Cached records carry a TTL set by the authoritative server. When it runs out the entry is dropped, and the next query goes to the hierarchy again."),
    ]
    for i, (ch, stem, opts, a, why) in enumerate(mcqs, 1):
        q[f"mc{i}"] = mc(ch, f"MCQ {i}", stem, opts, a, why)

    # ---------------------------------------------------------- Part 2: Ch 1-2
    def fig_campus():
        s = S(620, 190, "Three department switches joined in a ring; Admin has 5 computers, Finance 4, IT 6")
        sw = {"Admin": (150, 60), "Finance": (470, 60), "IT": (310, 150)}
        for a, b in (("Admin", "Finance"), ("Finance", "IT"), ("IT", "Admin")):
            s.line(*sw[a], *sw[b], sw=2.2)
        for name, (x, y) in sw.items():
            s.rect(x - 40, y - 12, 80, 24, 3, solid=True)
            s.text(x, y + (40 if y > 100 else -20), f"{name} switch", bold=True)
        return s.out()

    def p2_topology():
        return (
            '<p class="q-text">A college building has three departments. <b>Admin</b> has 5 computers, <b>Finance</b> has 4 and <b>IT</b> has 6; each department\'s computers connect to their own switch. '
            "The three switches are cabled to each other in a closed ring, as shown.</p>" + fig_campus()
            + f'<p class="q-text sub">a) Name the hybrid topology. (0.5 mark) {txt("", 0.5, "Hybrid topology", pattern=r"star.{0,12}ring|ring.{0,12}star", show="Star-ring hybrid (stars joined in a ring)", wide=True)}</p>'
            + f'<p class="q-text sub">b) Calculate the total number of cable links. (0.5 mark) {num(18, 0.5, "Number of links")}</p>'
            + '<p class="q-text sub">c) The whole building belongs to one college. Classify the network. (0.5 mark) '
            + sel(["LAN", "MAN", "WAN"], "LAN", 0.5, "Network type") + "</p>"
        )

    q["p2-1"] = PQ(1, "Q2", 1.5, p2_topology,
                   "Each department is a star; the switches form a ring → star-ring. Links: 5 + 4 + 6 = 15 computer cables + 3 ring cables = <b>18</b>. "
                   "One building is a LAN. Note that switches cabled in a loop need the Spanning Tree Protocol (Part 4).")

    def p2_osi():
        rows = (("Frame", "Data Link"), ("Segment", "Transport"), ("Choosing the best path through routers", "Network"),
                ("Dialog control (who talks, half or full duplex)", "Session"), ("Compression", "Presentation"), ("Bit synchronization", "Physical"))
        body = "".join(f"<tr><td>{t}</td><td>{sel(OSI, a, 0.25, 'OSI layer for ' + t)}</td></tr>" for t, a in rows)
        return '<p class="q-text">Find the corresponding OSI layer for each networking term. (0.25 each)</p><table class="ptable"><thead><tr><th>Networking Term</th><th>OSI Layer</th></tr></thead><tbody>' + body + "</tbody></table>"

    q["p2-2"] = PQ(1, "Q3", 1.5, p2_osi,
                   "PDUs: bits (physical), frame (data link), packet/datagram (network), segment (transport). Routing = network. Dialog control and synchronization points = session. "
                   "Translation, encryption and compression = presentation. Bit synchronization = physical.")

    def p2_router():
        macs = ["MAC A", "MAC R1", "MAC R2", "MAC B"]
        ips = ["10.0.1.5 (Host A)", "10.0.1.1 (router R, LAN 1)", "10.0.2.1 (router R, LAN 2)", "10.0.2.9 (Server B)"]
        return (
            '<p class="q-text">Host A (<span class="mono">10.0.1.5</span>, MAC A) on LAN 1 sends a request to Server B (<span class="mono">10.0.2.9</span>, MAC B) on LAN 2. '
            "Router R joins the two LANs: its LAN 1 interface has MAC R1 and its LAN 2 interface has MAC R2.</p>"
            f'<p class="q-text sub">a) Destination MAC address of the frame on LAN 1: {sel(macs, "MAC R1", 0.5, "Destination MAC on LAN 1")}</p>'
            f'<p class="q-text sub">b) Destination IP address of the packet on LAN 1: {sel(ips, ips[3], 0.5, "Destination IP on LAN 1")}</p>'
            f'<p class="q-text sub">c) Source MAC address of the frame on LAN 2: {sel(macs, "MAC R2", 0.5, "Source MAC on LAN 2")}</p>'
            f'<p class="q-text sub">d) Up to which OSI layer does the router decapsulate before forwarding? {sel(OSI, "Network", 0.5, "Router decapsulates up to")}</p>'
        )

    q["p2-3"] = PQ(1, "Q4", 2, p2_router,
                   "IP addresses stay the same end to end, so the packet is addressed to <b>10.0.2.9</b> on both LANs. MAC addresses change at every hop: on LAN 1 the frame goes to the router (<b>MAC R1</b>); "
                   "on LAN 2 the router sends it from <b>MAC R2</b> to MAC B. A router opens the frame up to the <b>network</b> layer, reads the destination IP, then builds a new frame.")

    # ---------------------------------------------------------- Part 3: Ch 3-4
    def p3_methods():
        methods = ["Parity", "Checksum", "CRC"]
        rows = (("Divides the data by a generator using modulo-2 (XOR); accepts when the remainder is 0", "CRC"),
                ("One's complement sum of the words, inverted; used in the IPv4, TCP and UDP headers", "Checksum"),
                ("The error-detection field in the Ethernet frame trailer", "CRC"),
                ("Detects any odd number of flipped bits but cannot locate them", "Parity"))
        body = "".join(f"<tr><td>{t}</td><td>{sel(methods, a, 0.25, 'Method: ' + t)}</td></tr>" for t, a in rows)
        return ('<p class="q-text">(a) Match each description to its error-detection method. (0.25 each)</p>'
                '<table class="ptable"><thead><tr><th>Description</th><th>Method</th></tr></thead><tbody>' + body + "</tbody></table>")

    q["p3-1"] = PQ(3, "Q5a", 1, p3_methods,
                   "CRC = modulo-2 division by a generator, remainder 0 = accept; it is the 4-byte CRC-32 in the Ethernet trailer. "
                   "Checksum = one's complement sum, inverted; the receiver accepts when the sum is all 1s; used in IPv4, TCP and UDP. "
                   "Parity counts 1s, so it catches an odd number of errors but cannot say which bit flipped.")

    def p3_stuffing():
        return (
            '<p class="q-text">(b) A bit-oriented protocol uses the flag <span class="mono">01111110</span>. The data to send is <span class="mono">0111111011111100</span>.</p>'
            f'<p class="q-text sub">1. Data after bit stuffing: {txt("011111010111110100", 0.75, "Stuffed data", wide=True)}</p>'
            f'<p class="q-text sub">2. How many 0s were inserted? {num(2, 0.25, "Zeros inserted")}</p>'
        )

    q["p3-2"] = PQ(3, "Q5b", 1, p3_stuffing,
                   "Insert a 0 after every five consecutive 1s: <span class='mono'>0 11111<b>0</b> 1 0 11111<b>0</b> 1 0 0</span> → <b class='mono'>011111010111110100</b>. "
                   "Two 0s are inserted, so a flag pattern can never appear inside the data; the receiver removes any 0 that follows five 1s.")

    parity = [[1, 1, 0, 1, 1], [0, 1, 0, 0, 0], [1, 0, 0, 1, 0], [0, 1, 0, 0, 1], [0, 1, 1, 0, 0]]

    def p3_parity():
        return (
            '<p class="q-text">(c) The receiver gets this block (even parity; the last column and last row are parity bits).</p>' + grid_table(parity, "Last column and last row are parity bits.")
            + f'<p class="q-text sub">Row of the error: {num(2, 0.25, "Row")} Column: {num(3, 0.25, "Column")} Corrected bit: {num(1, 0.5, "Corrected bit")}</p>'
        )

    q["p3-3"] = PQ(3, "Q5c", 1, p3_parity,
                   "Row 2 = 0 1 0 0 | 0 has one 1 (odd); every other row is even. Column 3 = 0, 0, 0, 0 | 1 has one 1 (odd). They cross at <b>row 2, column 3</b>: the received 0 should be <b>1</b>.")

    def p3_mac():
        return (
            '<p class="q-text">Stations on a shared Ethernet bus use <b>CSMA/CD</b>.</p>'
            '<p class="q-text sub">a) Station A detects a collision while sending. List what it does next, in order. (0.75 mark)</p>'
            + written(0.75, "<ol><li>Stops transmitting its frame.</li><li>Sends a short <b>jamming signal</b> so every station knows there was a collision.</li><li>Waits a random <b>backoff</b> time (binary exponential backoff, 0 to 2<sup>K</sup> − 1 slots after K collisions).</li><li>Senses the medium again and retries; it gives up after too many attempts.</li></ol>", lines=3)
            + f'<p class="q-text sub">b) Why must an Ethernet frame be at least 64 bytes? (0.5 mark)</p>'
            + written(0.5, "<p>So the sender is <b>still transmitting when news of a collision gets back</b>. Frame transmission time must be at least twice the maximum propagation time (2 × T<sub>p</sub>); otherwise the sender could finish, miss the collision, and think the frame was delivered.</p>", lines=2)
            + f'<p class="q-text sub">c) In a <b>token passing</b> network, what gives a station the right to send? (0.25 mark) {txt("", 0.25, "Right to send", pattern="token", show="Holding the token")}</p>'
        )

    q["p3-4"] = PQ(3, "Q6", 1.5, p3_mac,
                   "CSMA/CD: sense → send while monitoring → collision → stop, jam, random backoff, retry. Minimum frame 64 bytes (512 bits) so T<sub>fr</sub> ≥ 2T<sub>p</sub>. "
                   "Controlled access: reservation (reserve a slot), polling (poll/select), token passing (the token).")

    def p3_eth():
        rows = (("FF:FF:FF:FF:FF:FF", "Broadcast"), ("47:20:1B:2E:08:EE", "Multicast"), ("A4:6E:F4:59:83:AB", "Unicast"))
        types = ["Unicast", "Multicast", "Broadcast"]
        body = "".join(f"<tr><td class=\"mono\">{a}</td><td>{sel(types, t, 0.25, 'Type of ' + a)}</td></tr>" for a, t in rows)
        return ('<p class="q-text">Classify each Ethernet destination address. (0.25 each)</p><table class="ptable"><thead><tr><th>Address</th><th>Type</th></tr></thead><tbody>' + body + "</tbody></table>"
                f'<p class="q-text sub">How many bytes is the data field at most, and why is padding added? (0.75 mark)</p>'
                + written(0.75, "<p>The data field carries <b>46 to 1500 bytes</b>. If the upper-layer data is shorter than 46 bytes, <b>padding</b> is added so the frame reaches the 64-byte minimum.</p>", lines=2))

    q["p3-5"] = PQ(4, "Q7", 1.5, p3_eth,
                   "Look at the last bit of the first byte: 47 = 0100 011<b>1</b> → multicast; A4 = 1010 010<b>0</b> → unicast; all Fs = broadcast. Frame = 64 to 1518 bytes; data 46 to 1500.")

    access = ["ALOHA", "CSMA/CA", "Polling", "Reservation", "FDMA", "TDMA", "CDMA", "Token passing"]

    def p3_access():
        pick = lambda a, n: sel(access, a, 0.25, f"Blank {n}")
        return ('<p class="q-text">Fill the blanks from these choices (0.25 each):</p>' + word_box(access)
                + f'<p class="q-text sub">Wireless LANs cannot detect collisions while sending, so they avoid them with (1) {pick("CSMA/CA", 1)}. '
                f'A primary station asks each secondary station in turn whether it has data to send: this is (2) {pick("Polling", 2)}. '
                f'Each station gets its own repeating time slot in (3) {pick("TDMA", 3)}, while in (4) {pick("CDMA", 4)} all stations send at the same time using different codes.</p>')

    q["p3-6"] = PQ(3, "Q8", 1, p3_access,
                   "Random access: ALOHA, CSMA, CSMA/CD (wired Ethernet), CSMA/CA (wireless). Controlled access: reservation, polling (primary asks the secondaries), token passing. "
                   "Channelization: FDMA (frequency bands), TDMA (time slots), CDMA (codes, everyone at once).")

    # ---------------------------------------------------------- Part 4: Ch 6
    def fig_domains2():
        s = S(640, 170, "Hub H1 with PC1, PC2, PC3 joined to switch S1, which also has PC4, PC5 and router port A; router port B to switch S2 with PC6, PC7 and hub H2 with PC8 and PC9")
        for name, x, solid in (("H1", 80, False), ("S1", 220, True), ("S2", 440, True), ("H2", 570, False)):
            s.rect(x - 32, 46, 64, 18, 2, solid=solid)
            s.text(x, 36, name, bold=True)
        s.router(330, 55, 18, 14)
        s.text(330, 30, "R1", bold=True)
        for a, b in ((112, 188), (252, 312), (348, 408), (472, 538)):
            s.line(a, 55, b, 55)
        for x, label, hx in ((40, "PC1", 66), (80, "PC2", 80), (120, "PC3", 94), (200, "PC4", 210), (240, "PC5", 230), (420, "PC6", 430), (460, "PC7", 450), (550, "PC8", 560), (595, "PC9", 580)):
            s.line(hx, 64, x, 112)
            s.pc(x, 122, 22, 16)
            s.text(x, 150, label)
        return s.out()

    def p4_domains():
        return ('<p class="q-text">Consider the network below: hubs H1 and H2, switches S1 and S2 and router R1. (0.5 each)</p>' + fig_domains2()
                + f'<p class="q-text sub">1. Total number of collision domains: {num(8, 0.5, "Collision domains")}</p>'
                + f'<p class="q-text sub">2. Total number of broadcast domains: {num(2, 0.5, "Broadcast domains")}</p>')

    q["p4-1"] = PQ(6, "Q9", 1, p4_domains,
                   "S1 ports: H1 group, PC4, PC5, R1-A = 4. S2 ports: R1-B, PC6, PC7, H2 group = 4. Total <b>8</b>. One broadcast domain per router interface = <b>2</b>.")

    def p4_learning():
        act = ["Send to specific destination port", "Send to all ports (flooding)", "Drop the frame"]
        return ('<p class="q-text">A new switch (empty table) has A on port 1, B on port 2, C on port 3 and D on port 4. For each frame, in order, give the entry the switch learns and what it does with the frame. (0.25 each)</p>'
                '<table class="ptable center"><thead><tr><th>Frame</th><th>New entry (MAC → port)</th><th>Action</th></tr></thead><tbody>'
                f'<tr><td>1. A → D</td><td>A → {num(1, 0.25, "Port learned for A")}</td><td>{sel(act, act[1], 0.25, "Action for frame 1")}</td></tr>'
                f'<tr><td>2. D → A</td><td>D → {num(4, 0.25, "Port learned for D")}</td><td>{sel(act, act[0], 0.25, "Action for frame 2")}</td></tr>'
                f'<tr><td>3. A → D</td><td>{sel(["No new entry", "A → port 1 again", "D → port 4 again"], "No new entry", 0.25, "Entry for frame 3")}</td><td>{sel(act, act[0], 0.25, "Action for frame 3")}</td></tr>'
                "</tbody></table>")

    q["p4-2"] = PQ(6, "Q10", 1.5, p4_learning,
                   "Learn the source, decide by the destination. Frame 1: learn A/1, D unknown → flood. Frame 2: learn D/4, A known → port 1 only. Frame 3: both already in the table → nothing new, forward to port 4.")

    def p4_vlan():
        tbl = ('<table class="ptable center narrow"><thead><tr><th>VLAN</th><th>Computers</th></tr></thead><tbody>'
               "<tr><td>VLAN 10</td><td>A, B (Switch 1), F (Switch 2)</td></tr><tr><td>VLAN 20</td><td>C (Switch 1), G, H (Switch 2)</td></tr>"
               "<tr><td>VLAN 30</td><td>D, E (Switch 1), I, J (Switch 2)</td></tr><tr><td>VLAN 40</td><td>K (Switch 2)</td></tr></tbody></table>")
        return ('<p class="q-text">Two switches are joined by one backbone (trunk) link that carries every VLAN.</p>' + tbl
                + f'<p class="q-text sub">a) How many broadcast domains? {num(4, 0.5, "Broadcast domains")}</p>'
                + f'<p class="q-text sub">b) A sends a broadcast. Which computers receive it? {txt("B,F|F,B|B and F|F and B", 0.5, "Receivers of A's broadcast", show="B and F")}</p>'
                + f'<p class="q-text sub">c) What device is needed for A to talk to C? {txt("", 0.5, "Device for inter-VLAN traffic", pattern=r"router|layer\s*3|l3", show="A router (layer-3 device)")}</p>')

    q["p4-3"] = PQ(6, "Q11", 1.5, p4_vlan,
                   "One broadcast domain per VLAN = 4 (K alone is still a VLAN). VLAN 10 spans both switches over the backbone, so B and F receive A's broadcast. Different VLANs need a router.")

    def p4_stp():
        words = ["broadcast storm", "Spanning Tree Protocol", "blocking", "forwarding", "loop", "collision domain"]
        return ('<p class="q-text">Choose from the box (0.25 each).</p>' + word_box(words)
                + f'<p class="q-text sub">Redundant switches create a {sel(words, "loop", 0.25, "Blank 1")}. Broadcast frames circulate forever, a {sel(words, "broadcast storm", 0.25, "Blank 2")}. '
                f'{sel(words, "Spanning Tree Protocol", 0.25, "Blank 3")} prevents this by putting some ports in the {sel(words, "blocking", 0.25, "Blank 4")} state.</p>')

    q["p4-4"] = PQ(6, "Q12", 1, p4_stp, "Term 261 Major II asked the same chain with these words: loop → broadcast storm → spanning tree → blocked ports.")

    # ---------------------------------------------------------- Part 5: Ch 7
    def p5_classes():
        rows = (("10.20.130.9", "A", "255.0.0.0", "8", "10.0.0.0"), ("172.31.7.200", "B", "255.255.0.0", "16", "172.31.0.0"), ("223.1.2.3", "C", "255.255.255.0", "24", "223.1.2.0"))
        body = ""
        for addr, c, m, p, net in rows:
            mp = r"^\s*(" + m.replace(".", r"\.") + r"(\s*/\s*" + p + r")?|/?\s*" + p + r")\s*$"
            body += (f"<tr><td>{addr}</td><td>{sel(['A', 'B', 'C', 'D', 'E'], c, 0.125, 'Class of ' + addr, cls='blank short')}</td>"
                     f"<td>{txt('', 0.125, 'Mask of ' + addr, pattern=mp, show=f'{m} /{p}')}</td><td>{txt('', 0.25, 'Network of ' + addr, pattern=ip(net), show=net)}</td></tr>")
        return ('<p class="q-text">Identify the class, default mask and classful network address. </p>'
                '<table class="ptable"><thead><tr><th>IP address</th><th>Class</th><th>Default mask</th><th>Network address</th></tr></thead><tbody>' + body + "</tbody></table>")

    q["p5-1"] = PQ(7, "Q13", 1.5, p5_classes, "0–127 A, 128–191 B, 192–223 C. Zero the host part: 10.0.0.0 · 172.31.0.0 · 223.1.2.0.")

    def p5_block():
        return ('<p class="q-text">One address of a classless block is <b>172.16.40.77/20</b>. Find:</p>'
                f'<p class="q-text sub">a) First address: {txt("", 0.5, "First address", pattern=ip("172.16.32.0"), show="172.16.32.0")}</p>'
                f'<p class="q-text sub">b) Last address: {txt("", 0.5, "Last address", pattern=ip("172.16.47.255"), show="172.16.47.255")}</p>'
                f'<p class="q-text sub">c) Number of addresses: {num(4096, 0.5, "Number of addresses")}</p>')

    q["p5-2"] = PQ(7, "Q14", 1.5, p5_block,
                   "/20 → the third byte keeps 4 network bits, block size 256 − 240 = 16 in that byte. 40 lies in 32–47. First = <b>172.16.32.0</b>, last = <b>172.16.47.255</b>, count = 2<sup>32−20</sup> = <b>4096</b>.")

    def p5_subnet():
        a = lambda net, m, label: txt("", m, label, pattern=ip(net), show=net)
        return ('<p class="q-text">The administrator divides <b>200.10.5.0/24</b> into <b>4 equal subnets</b> for four labs.</p>'
                f'<p class="q-text sub">a) Subnet mask: {txt("", 0.25, "Subnet mask", pattern=r"^\s*(255\.255\.255\.192(\s*\(?\s*/\s*26\s*\)?)?|/\s*26)\s*$", show="255.255.255.192 (/26)")} &nbsp; b) Hosts per subnet: {num(62, 0.25, "Hosts per subnet")}</p>'
                f'<p class="q-text sub">c) The four subnet addresses: {a("200.10.5.0", 0.125, "Subnet 1")} {a("200.10.5.64", 0.125, "Subnet 2")} {a("200.10.5.128", 0.125, "Subnet 3")} {a("200.10.5.192", 0.125, "Subnet 4")}</p>'
                f'<p class="q-text sub">d) For subnet 3: default gateway (first usable) {a("200.10.5.129", 0.25, "Gateway of subnet 3")}, last usable host {a("200.10.5.190", 0.25, "Last host of subnet 3")}, broadcast {a("200.10.5.191", 0.5, "Broadcast of subnet 3")}</p>')

    q["p5-3"] = PQ(7, "Q15", 2, p5_subnet,
                   "4 subnets → borrow 2 bits → /26 = 255.255.255.192, block 64, hosts 2<sup>6</sup> − 2 = 62. Subnets .0, .64, .128, .192. Subnet 3 = 200.10.5.128: hosts .129–.190, broadcast .191.")

    def p5_services():
        return ('<p class="q-text">A host in a LAN has private IP <b>10.1.1.25</b>. The router\'s public IP is <b>130.50.60.8</b>.</p>'
                f'<p class="q-text sub">a) The host knows 10.1.1.40 is on its LAN but not its MAC address. Which protocol finds it, and is the request unicast or broadcast? {txt("", 0.5, "Protocol and delivery", pattern=r"arp.*broad|broad.*arp", show="ARP; the request is broadcast (the reply is unicast)", wide=True)}</p>'
                f'<p class="q-text sub">b) Put the four DHCP messages in order. {sel(["Discover, Offer, Request, Ack", "Request, Offer, Discover, Ack", "Offer, Discover, Ack, Request", "Discover, Request, Offer, Ack"], "Discover, Offer, Request, Ack", 0.5, "DHCP order")}</p>'
                f'<p class="q-text sub">c) The host opens a web page on 200.53.25.67. What source IP does the web server see, and which technique changed it? {txt("", 0.5, "Source IP seen by server", pattern=r"130\.50\.60\.8.*nat|nat.*130\.50\.60\.8", show="130.50.60.8, changed by NAT", wide=True)}</p>')

    q["p5-4"] = PQ(7, "Q16", 1.5, p5_services,
                   "ARP request = broadcast, reply = unicast. DHCP = DORA: Discover, Offer, Request, Ack. NAT replaces the private source with the router's public address and remembers the mapping (with ports) for the reply.")

    def p5_nat():
        return ('<p class="q-text">Complete the NAT translation table after host 10.1.1.25 (port 3345) contacts the web server 200.53.25.67 (port 80). The router uses port 50001.</p>'
                '<table class="ptable center"><thead><tr><th>Private address</th><th>Private port</th><th>External (public) address</th><th>External port</th><th>Transport</th></tr></thead><tbody>'
                f'<tr><td>{txt("", 0.25, "Private address", pattern=ip("10.1.1.25"), show="10.1.1.25")}</td><td>{num(3345, 0.25, "Private port")}</td>'
                f'<td>{txt("", 0.5, "Public address", pattern=ip("130.50.60.8"), show="130.50.60.8")}</td><td>{num(50001, 0.25, "External port")}</td><td>{sel(["TCP", "UDP"], "TCP", 0.25, "Transport")}</td></tr></tbody></table>')

    q["p5-5"] = PQ(7, "Q17", 1.5, p5_nat, "The router rewrites 10.1.1.25:3345 as 130.50.60.8:50001. HTTP runs over TCP. The reply to port 50001 is translated back using this row.")

    # ---------------------------------------------------------- Part 6: Ch 8
    def p6_forward():
        rows = [("140.24.7.0/26", "m0"), ("140.24.7.64/26", "m1"), ("140.24.7.128/25", "m2"), ("180.70.65.0/24", "m3"), ("Default (0.0.0.0/0)", "m4")]
        table = '<table class="ptable center narrow"><thead><tr><th>Network address / mask</th><th>Interface</th></tr></thead><tbody>' + "".join(f"<tr><td>{n}</td><td>{i}</td></tr>" for n, i in rows) + "</tbody></table>"
        ifs = ["m0", "m1", "m2", "m3", "m4"]
        return ('<p class="q-text">Router R1 has this forwarding table. Find the outgoing interface for each destination. (0.5 each)</p>' + table
                + f'<p class="q-text sub">a) 140.24.7.70 → {sel(ifs, "m1", 0.5, "Interface for 140.24.7.70")} &nbsp; b) 140.24.7.200 → {sel(ifs, "m2", 0.5, "Interface for 140.24.7.200")} &nbsp; c) 180.70.66.9 → {sel(ifs, "m4", 0.5, "Interface for 180.70.66.9")}</p>')

    q["p6-1"] = PQ(8, "Q18", 1.5, p6_forward,
                   "AND the destination with each mask, longest mask first. 140.24.7.70 AND /26 = 140.24.7.64 → <b>m1</b>. 140.24.7.200: /26 gives .192 (no match), /25 gives .128 → <b>m2</b>. "
                   "180.70.66.9 AND /24 = 180.70.66.0 ≠ 180.70.65.0 → no match → default <b>m4</b>.")

    def p6_dv():
        vec = {"B": (0, 3, 4, 6, 9), "C": (3, 0, 5, 2, 1), "D": (4, 5, 0, 7, 4)}
        dests = ["B", "C", "D", "E", "F"]
        head = "<tr><th>To</th>" + "".join(f"<th>{n}'s vector</th>" for n in vec) + "</tr>"
        body = "".join("<tr><td>" + d + "</td>" + "".join(f"<td>{vec[n][i]}</td>" for n in vec) + "</tr>" for i, d in enumerate(dests))
        ans = {"B": (2, "B"), "C": (5, "B"), "D": (3, "D"), "E": (8, "B"), "F": (7, "D")}
        rows = "".join(f"<tr><td>{d}</td><td>{num(c, 0.2, 'Cost to ' + d)}</td><td>{sel(['B', 'C', 'D'], n, 0.2, 'Next hop to ' + d, cls='blank short')}</td></tr>" for d, (c, n) in ans.items())
        return ('<p class="q-text">Router A uses distance vector routing. Its link costs are A–B = 2, A–C = 7, A–D = 3. It receives these vectors from its neighbours:</p>'
                f'<table class="ptable center narrow"><thead>{head}</thead><tbody>{body}</tbody></table>'
                '<p class="q-text sub">Using Bellman-Ford, complete A\'s new table. (0.2 each)</p>'
                f'<table class="ptable center narrow"><thead><tr><th>To</th><th>Cost</th><th>Next hop</th></tr></thead><tbody>{rows}</tbody></table>')

    q["p6-2"] = PQ(8, "Q19", 2, p6_dv,
                   "D<sub>A</sub>(y) = min { c(A,v) + D<sub>v</sub>(y) }. B: min(2+0, 7+3, 3+4) = 2 via B. C: min(2+3, 7+0, 3+5) = 5 via B. D: min(2+4, 7+5, 3+0) = 3 via D. "
                   "E: min(2+6, 7+2, 3+7) = 8 via B. F: min(2+9, 7+1, 3+4) = 7 via D. The direct link isn't always best: A reaches C more cheaply through B.")

    def p6_compare():
        words = ["RIP", "OSPF", "BGP", "Dijkstra", "Bellman-Ford", "count to infinity", "flooding"]
        pick = lambda a, n: sel(words, a, 0.25, f"Blank {n}")
        return ('<p class="q-text">Fill the blanks from the box (0.25 each).</p>' + word_box(words)
                + f'<p class="q-text sub">Distance vector routers apply {pick("Bellman-Ford", 1)} to their neighbours\' vectors; their weakness is slow convergence, the {pick("count to infinity", 2)} problem. '
                f'Link state routers send their link costs to every router by {pick("flooding", 3)} and then run {pick("Dijkstra", 4)}. '
                f'Inside an autonomous system, {pick("OSPF", 5)} is a link state protocol; between autonomous systems, {pick("BGP", 6)} is used.</p>')

    q["p6-3"] = PQ(8, "Q20", 1.5, p6_compare,
                   "DV: Bellman-Ford, neighbours only, count to infinity, RIP (hop count). LS: flooding of LSPs, Dijkstra, OSPF. Inter-AS: BGP (path vector).")

    # ---------------------------------------------------------- Part 7: Ch 9
    def p7_seq():
        return ('<p class="q-text">A TCP sender transfers a <b>4,000-byte</b> file in <b>1,000-byte</b> segments. The first byte is numbered <b>20,001</b>.</p>'
                f'<p class="q-text sub">a) Sequence number of the third segment: {num(22001, 0.5, "Third segment sequence number")}</p>'
                f'<p class="q-text sub">b) ACK number after the receiver gets the first two segments: {num(22001, 0.5, "ACK after two segments")}</p>')

    q["p7-1"] = PQ(9, "Q21", 1, p7_seq,
                   "Segments start at 20,001, 21,001, 22,001, 23,001 → third = <b>22,001</b>. After bytes 20,001–22,000 arrive, the ACK is the next byte expected: <b>22,001</b>.")

    def p7_choose():
        rows = (("File download (FTP)", "TCP"), ("DNS query", "UDP"), ("Online video call", "UDP"), ("Sending an email (SMTP)", "TCP"))
        body = "".join(f"<tr><td>{a}</td><td>{sel(['TCP', 'UDP'], p, 0.25, 'Transport for ' + a)}</td></tr>" for a, p in rows)
        return '<p class="q-text">Choose TCP or UDP for each application. (0.25 each)</p><table class="ptable"><tbody>' + body + "</tbody></table>"

    q["p7-2"] = PQ(9, "Q22", 1, p7_choose, "Needs every byte (files, email, web) → TCP. Short request/reply or real-time (DNS, voice, video) → UDP.")

    def p7_hand():
        return ('<p class="q-text">Write the three segments of the TCP three-way handshake in order, and give the well-known port of HTTP and of DNS. (0.25 each)</p>'
                f'<p class="q-text sub">1. {txt("SYN", 0.25, "First segment")} 2. {txt("SYN+ACK|SYN ACK|SYN-ACK|SYNACK", 0.25, "Second segment", show="SYN + ACK")} 3. {txt("ACK", 0.25, "Third segment")}</p>'
                f'<p class="q-text sub">HTTP port: {num(80, 0.125, "HTTP port")} DNS port: {num(53, 0.125, "DNS port")}</p>')

    q["p7-3"] = PQ(9, "Q23", 1, p7_hand, "SYN → SYN + ACK → ACK. Ports: FTP 20/21, Telnet 23, SMTP 25, DNS 53, HTTP 80, HTTPS 443.")

    # ---------------------------------------------------------- Part 8: Ch 10
    def p8_dns():
        steps = ["Client → local DNS server → root → .sa TLD → psu.edu.sa authoritative → local DNS server → client",
                 "Client → root → local DNS server → authoritative → client",
                 "Client → .sa TLD → root → local DNS server → client",
                 "Client → authoritative → .sa TLD → root → client"]
        rec = ["Each server contacts the next one on the client's behalf", "The local server contacts every server itself", "The client contacts every server"]
        return ('<p class="q-text">A student types <b>lms.psu.edu.sa</b>. Nothing is cached.</p>'
                f'<p class="q-text sub">a) Which label is the top-level domain? {txt("sa|.sa", 0.25, "Top-level domain", show=".sa")} Which is the host? {txt("lms", 0.25, "Host label", show="lms")}</p>'
                f'<p class="q-text sub">b) Which sequence is a correct iterative lookup? {sel(steps, steps[0], 0.5, "Lookup order")}</p>'
                f'<p class="q-text sub">c) In <b>recursive</b> resolution, who contacts the next server at each step? {sel(rec, rec[0], 0.5, "Recursive")}</p>'
                f'<p class="q-text sub">d) DNS normally runs over which transport protocol and port? {txt("", 0.5, "Transport and port", pattern=r"udp.*53|53.*udp", show="UDP port 53")}</p>')

    q["p8-1"] = PQ(10, "Q24", 2, p8_dns,
                   "Read right to left: sa (TLD) → edu → psu → lms (host). Iterative: the local server asks root, then the TLD server, then the authoritative server, each returning a referral. "
                   "Recursive: each server passes the query on and the answer travels back. DNS queries use UDP port 53 (TCP for zone transfers and large replies).")

    # ---------------------------------------------------------- layout
    head = ('<div class="paper-title">CS331 - Data Communications &amp; Networking - Final Exam (Predicted) - Term 261</div>'
            '<div class="paper-meta center"><b>Chapters 1, 3, 4, 6, 7, 8, 9, 10</b><b>Marks = 40</b>'
            '<b class="marks">Score: <span class="got" data-q="all"></span>/40</b></div>')
    bar = lambda title, key, m: f'<div class="clo-bar"><span>{title}</span><span>Total ( <span class="got" data-q="{key}"></span> /{m})</span></div>'
    on = lambda keys, part, lab=True: "".join(q[k].on_paper(f"{q[k].no[1:]}." if lab else "", part) for k in keys)
    p1 = head + bar("Part 1: Multiple choice [0.5 each, 5 Marks]", "f1", 5) + "".join(q[f"mc{i}"].on_paper(f"{i}.", "f1") for i in range(1, 11))
    p2 = bar("Part 2: Overview and Layering [5 Marks]", "f2", 5) + on(["p2-1", "p2-2", "p2-3"], "f2")
    p3 = bar("Part 3: Data Link Layer and Ethernet [7 Marks]", "f3", 7) + on(["p3-1", "p3-2", "p3-3"], "f3") + on(["p3-4", "p3-5", "p3-6"], "f3")
    p4 = bar("Part 4: Connecting Devices and VLANs [5 Marks]", "f4", 5) + on(["p4-1", "p4-2", "p4-3", "p4-4"], "f4")
    p5 = bar("Part 5: Network Layer: IPv4 [8 Marks]", "f5", 8) + on(["p5-1", "p5-2", "p5-3", "p5-4", "p5-5"], "f5")
    p6 = bar("Part 6: Routing [5 Marks]", "f6", 5) + on(["p6-1", "p6-2", "p6-3"], "f6")
    p7 = bar("Part 7: Transport Layer [3 Marks]", "f7", 3) + on(["p7-1", "p7-2", "p7-3"], "f7") + bar("Part 8: DNS and the Application Layer [2 Marks]", "f8", 2) + on(["p8-1"], "f8")
    pages = (p1, p2, p3, p4, p5, p6, p7)
    return "".join(sheet(i + 1, len(pages), b) for i, b in enumerate(pages))
