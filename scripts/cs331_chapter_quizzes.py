"""CS331 chapter quizzes: one quiz per chapter that tests every concept.

Used by scripts/build_cs331_past_papers.py (which owns the page shell, the Exams
listing, the wrappers and the sidebar). Each quiz is split into concept sections;
every question carries its concept tag. Questions use the shared paper engine
(docs/javascripts/cys401-past-paper.js): radio options, text answers, numbers,
drop-downs, and figure questions where the drawing is filled in through a table.

Answer spec used by gap() and table() cells, written inside [[...]]:
    [[a|b]]           text answer; any listed form is right (letters/digits compared)
    [[#12.5]]         number; the first number typed is compared exactly
    [[/regex/=shown]] regular expression (case-insensitive); "shown" is the model answer
    [[?x|y|z=y]]      drop-down with options x, y, z; y is right
"""
from __future__ import annotations

import html
import math
import re

esc = html.escape
SPEC = re.compile(r"\[\[(.+?)\]\]")

CHAPTER_TITLES = {
    1: "Data Communications, Networks and Layering",
    2: "Physical Layer",
    3: "Data Link Layer: Control and Media Access",
    4: "Ethernet and LANs",
    6: "Connecting Devices and VLANs",
    7: "Network Layer: Data Transfer",
    8: "Network Layer: Routing",
    9: "Transport Layer",
    10: "DNS and the Application Layer",
}


def build(h):
    """h is the build_cs331_past_papers module. Returns {chapter: [(concept, [questions])]}."""
    txt, num, sel, S = h.txt, h.num, h.sel, h.S

    class CQ(h.Q):
        # Same rendering as a past-paper question, but not registered in h.ALL
        # (the questions-by-chapter page lists past papers only).
        def __init__(self, ch, concept, marks, body, why=""):
            self.ch, self.src, self.no, self.marks = ch, "quiz", concept, marks
            self.body, self.why, self.ctx, self.concept = body, why, "", concept

    bank: dict[int, list] = {}
    cur = {"ch": 0, "concept": ""}

    def chapter(n):
        cur["ch"] = n
        bank[n] = []

    def concept(name):
        cur["concept"] = name
        bank[cur["ch"]].append((name, []))

    def add(marks, body, why):
        q = CQ(cur["ch"], cur["concept"], marks, body, why)
        bank[cur["ch"]][-1][1].append(q)
        return q

    def widget(spec, marks, label="Answer"):
        if spec.startswith("#"):
            return num(spec[1:], marks, label)
        if spec.startswith("/"):
            pat, show = spec[1:].rsplit("/=", 1)
            return txt("", marks, label, show=show, pattern=pat)
        if spec.startswith("?"):
            opts, ans = spec[1:].rsplit("=", 1)
            return sel(opts.split("|"), ans, marks, label)
        return txt(spec, marks, label)

    def fill(text, marks):
        specs = SPEC.findall(text)
        each = marks / max(1, len(specs))
        return SPEC.sub(lambda m: widget(m.group(1), round(each, 4)), text)

    def mc(stem, opts, ans, why, marks=1, fig=None):
        labels = "|".join("abcdefgh"[i] + "." for i in range(len(opts)))
        return add(marks, lambda: f'<p class="q-text">{stem}</p>{fig() if fig else ""}{h.choose(opts, ans, marks, labels)}', why)

    def tf(stem, truth, why, marks=1):
        return add(marks, lambda: f'<p class="q-text"><b>True or false:</b> {stem}</p>{h.choose(["True", "False"], 0 if truth else 1, marks, "i.|ii.")}', why)

    def gap(stem, why, marks=1, fig=None):
        return add(marks, lambda: f'<p class="q-text">{fill(stem, marks)}</p>{fig() if fig else ""}', why)

    def table(stem, head, rows, why, marks=1, fig=None):
        cells = sum(len(SPEC.findall(c)) for r in rows for c in r)
        each = marks / max(1, cells)

        def body():
            th = "".join(f"<th>{c}</th>" for c in head)
            tr = "".join(
                "<tr>" + "".join(f"<td>{SPEC.sub(lambda m: widget(m.group(1), round(each, 4), head[j] if j < len(head) else 'Answer'), c)}</td>" for j, c in enumerate(r)) + "</tr>"
                for r in rows
            )
            return (f'<p class="q-text">{stem}</p>{fig() if fig else ""}'
                    f'<table class="ptable stack table-stack-labels center"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>')

        return add(marks, body, why)

    # ================================================================ figures
    def fig_two_routers():
        s = S(560, 170, "Host A on LAN 1, router R1, LAN 2, router R2, LAN 3, host B")
        s.pc(40, 60)
        s.text(40, 100, "A")
        s.text(40, 116, "phys 11")
        s.line(65, 66, 140, 66, sw=2.2)
        s.router(170, 66, 26, 13)
        s.text(170, 40, "R1")
        s.text(130, 92, "phys 22")
        s.text(212, 92, "phys 33")
        s.line(196, 66, 340, 66, sw=2.2)
        s.text(268, 58, "LAN 2")
        s.router(370, 66, 26, 13)
        s.text(370, 40, "R2")
        s.text(330, 92, "phys 44")
        s.text(412, 92, "phys 55")
        s.line(396, 66, 490, 66, sw=2.2)
        s.pc(520, 60)
        s.text(520, 100, "B")
        s.text(520, 116, "phys 66")
        s.text(100, 58, "LAN 1")
        s.text(445, 58, "LAN 3")
        s.text(280, 150, "Logical (IP) addresses: A and B. Process on A uses port 51000; web server on B uses port 80.")
        return s.out()

    def fig_wave():
        s = S(520, 190, "Sine wave completing two full cycles between 0 and 1 millisecond")
        s.line(40, 95, 500, 95)
        s.line(40, 20, 40, 170)
        pts = []
        for i in range(0, 201):
            x = 40 + i * 2.3
            y = 95 - 55 * math.sin(2 * math.pi * 2 * i / 200)
            pts.append(f"{'M' if i == 0 else 'L'}{x:.1f} {y:.1f}")
        s.path(" ".join(pts), sw=2.2)
        s.text(40, 186, "0")
        s.text(270, 186, "0.5 ms")
        s.text(500, 186, "1 ms")
        s.line(270, 90, 270, 100)
        s.line(500, 90, 500, 100)
        s.text(30, 44, "+A", "end")
        s.text(30, 154, "−A", "end")
        return s.out()

    def fig_ethernet():
        s = S(600, 90, "Ethernet frame: preamble, SFD, destination, source, type/length, data and padding, CRC")
        fields = ["Preamble", "SFD", "Destination", "Source", "Type", "Data + padding", "CRC"]
        widths = [80, 40, 90, 90, 60, 160, 60]
        x = 10
        for f, w in zip(fields, widths):
            s.rect(x, 20, w, 40)
            s.text(x + w / 2, 45, f)
            x += w
        s.text(300, 82, "Fill the size of each field below (in bytes).")
        return s.out()

    # ================================================================ Chapter 1
    chapter(1)
    concept("Data communication")
    gap("The five components of a data communication system are the message, the [[sender|source]], the [[receiver|destination]], the [[transmission medium|medium]] and the [[protocol|protocols]].",
        "Message, sender, receiver, transmission medium and protocol.")
    table("Match each data flow mode to an example.", ["Device", "Data flow"],
          [["Keyboard to computer", "[[?Simplex|Half-duplex|Full-duplex=Simplex]]"],
           ["Walkie-talkie", "[[?Simplex|Half-duplex|Full-duplex=Half-duplex]]"],
           ["Telephone call", "[[?Simplex|Half-duplex|Full-duplex=Full-duplex]]"]],
          "Simplex is one way only; half-duplex is both ways but one at a time; full-duplex is both ways at once.")
    mc("Which network criterion covers the frequency of failures and the time a network takes to recover?",
       ["Performance", "Reliability", "Security", "Topology"], 1,
       "Reliability is measured by how often failures happen, the recovery time and robustness in a catastrophe.")
    tf("Throughput and delay are both performance measures, and raising throughput usually increases delay.", True,
       "More throughput means more traffic in the network, which increases queuing, so the two often conflict.")
    mc("A link shared by more than two devices is a…",
       ["Point-to-point connection", "Multipoint (multidrop) connection", "Mesh link", "Simplex link"], 1,
       "Multipoint links are shared by several devices; point-to-point links connect exactly two.")

    concept("Topologies")
    gap("A full mesh of 7 devices needs [[#21]] links, and each device needs [[#6]] I/O ports.",
        "Links = n(n − 1)/2 = 7 × 6 / 2 = 21; ports per device = n − 1 = 6.")
    table("Fill the number of links needed for 10 devices.", ["Topology", "Links"],
          [["Star (to a hub)", "[[#10]]"], ["Ring", "[[#10]]"], ["Full mesh", "[[#45]]"]],
          "Star: one link per device. Ring: n links. Mesh: n(n − 1)/2 = 45.")
    mc("In which topology does one broken cable in the main backbone stop the whole network?",
       ["Star", "Mesh", "Bus", "Hybrid star"], 2,
       "Every device taps the single bus backbone, so a break in it disconnects everyone.")
    mc("Which topology gives privacy, robustness and easy fault isolation but needs the most cabling?",
       ["Mesh", "Star", "Bus", "Ring"], 0, "Dedicated links between every pair of devices: robust and private, but expensive.")
    tf("In a star topology, if the hub fails the whole network fails.", True, "Every link goes through the hub.")

    concept("Network types, Internet and standards")
    table("Classify each network.", ["Network", "Type"],
          [["The computers in one school building", "[[?LAN|MAN|WAN=LAN]]"],
           ["A cable TV network covering a city", "[[?LAN|MAN|WAN=MAN]]"],
           ["A company's offices in Riyadh, Dubai and London joined together", "[[?LAN|MAN|WAN=WAN]]"]],
          "LAN = building or campus, MAN = city, WAN = country or continent.")
    mc("STC and Mobily are examples of which ISP level?", ["Tier 1 (international backbone)", "Tier 2 (national)", "Tier 3 (local)", "Customer network"], 1,
       "National ISPs are tier 2; Sprint and AT&T are tier 1 backbones.")
    tf("National (tier 2) ISPs connect to each other at private peering points.", False,
       "National ISPs meet at Internet Exchange Points (public peering). Private peering points join international ISPs.")
    gap("The three elements of a protocol are [[syntax]] (format of the data), [[semantics]] (meaning of each section) and [[timing]] (when and how fast).",
        "Syntax, semantics, timing.")
    mc("Which organization creates standards for LANs and MANs (802.x)?", ["ISO", "ITU-T", "IEEE", "W3C"], 2, "IEEE 802 covers LANs and MANs.")

    concept("Layering and the OSI model")
    table("Put the OSI layers in order (7 = top).", ["Number", "Layer"],
          [["7", "[[Application]]"], ["6", "[[Presentation]]"], ["5", "[[Session]]"], ["4", "[[Transport]]"],
           ["3", "[[Network]]"], ["2", "[[Data link|Datalink]]"], ["1", "[[Physical]]"]],
          "All People Seem To Need Data Processing.")
    table("Which OSI layer is responsible for each job?", ["Job", "Layer"],
          [["Encryption, compression and translation", "[[?Physical|Data link|Network|Transport|Session|Presentation|Application=Presentation]]"],
           ["Dialog control and synchronization points", "[[?Physical|Data link|Network|Transport|Session|Presentation|Application=Session]]"],
           ["Routing packets across networks", "[[?Physical|Data link|Network|Transport|Session|Presentation|Application=Network]]"],
           ["Node-to-node delivery of frames", "[[?Physical|Data link|Network|Transport|Session|Presentation|Application=Data link]]"],
           ["Process-to-process delivery, segmentation", "[[?Physical|Data link|Network|Transport|Session|Presentation|Application=Transport]]"],
           ["Transmitting bits over the medium", "[[?Physical|Data link|Network|Transport|Session|Presentation|Application=Physical]]"]],
          "Presentation translates and encrypts; session manages dialogs; network routes; data link delivers frames hop to hop; transport delivers to processes; physical sends bits.")
    tf("Well-defined interfaces let one layer's implementation be replaced without affecting the other layers.", True,
       "Layers only use the services of the layer below through its interface.")
    tf("The physical and data link layers are implemented in hardware on the network interface card.", True,
       "The NIC holds layers 1 and 2; upper layers run in software.")
    mc("Peer-to-peer communication between layers means that…",
       ["Each layer talks directly to the same layer on the other machine through headers", "Two computers share one cable",
        "Layers skip the layers below them", "Every layer adds a trailer"], 0,
       "Logically, layer n on one machine communicates with layer n on the other, using the headers it adds.")

    concept("TCP/IP, encapsulation and addresses")
    table("Fill the TCP/IP layer, its data unit and the address it uses.", ["Layer", "Data unit", "Address"],
          [["Application", "[[Message|Messages]]", "[[?Physical|Logical (IP)|Port|Specific (URL/email)=Specific (URL/email)]]"],
           ["Transport", "[[Segment|User datagram|Segments]]", "[[?Physical|Logical (IP)|Port|Specific (URL/email)=Port]]"],
           ["Network", "[[Packet|Datagram]]", "[[?Physical|Logical (IP)|Port|Specific (URL/email)=Logical (IP)]]"],
           ["Data link", "[[Frame|Frames]]", "[[?Physical|Logical (IP)|Port|Specific (URL/email)=Physical]]"],
           ["Physical", "[[Bits|Bit]]", "—"]],
          "Message → segment → packet → frame → bits; specific, port, logical and physical addresses.")
    tf("During encapsulation every layer adds a header, and the data link layer usually adds a trailer too.", True,
       "The trailer carries the error-detection field (for example the CRC).")
    table("Host A sends a packet to host B through two routers. Fill the addresses in each frame.",
          ["Link", "Source physical", "Destination physical", "Source IP", "Destination IP", "Destination port"],
          [["LAN 1 (A → R1)", "[[11]]", "[[22]]", "[[A]]", "[[B]]", "[[80]]"],
           ["LAN 2 (R1 → R2)", "[[33]]", "[[44]]", "[[A]]", "[[B]]", "[[80]]"],
           ["LAN 3 (R2 → B)", "[[55]]", "[[66]]", "[[A]]", "[[B]]", "[[80]]"]],
          "Physical addresses change on every link (sending interface → next interface). The IP addresses A and B and the port 80 stay the same end to end.",
          marks=3, fig=fig_two_routers)
    mc("Which delivery is the network layer responsible for?", ["Hop-to-hop", "Host-to-host (source to destination)", "Process-to-process", "Bit-to-bit"], 1,
       "Data link = hop to hop, network = host to host, transport = process to process.")
    tf("OSI has seven layers while the original TCP/IP suite has five, because session and presentation are folded into the application layer.", True,
       "TCP/IP merges session and presentation into application.")

    # ================================================================ Chapter 2
    chapter(2)
    concept("Signals")
    table("Classify each signal or data.", ["Item", "Kind"],
          [["Human voice", "[[?Analog|Digital=Analog]]"], ["Data stored in computer memory", "[[?Analog|Digital=Digital]]"],
           ["A sine wave repeating forever", "[[?Periodic|Aperiodic=Periodic]]"], ["A single burst of noise", "[[?Periodic|Aperiodic=Aperiodic]]"]],
          "Analog takes continuous values, digital takes discrete values; periodic signals repeat a pattern.")
    gap("A signal has a period of 0.2 ms. Its frequency is [[#5]] kHz.", "f = 1 / T = 1 / 0.0002 s = 5,000 Hz = 5 kHz.")
    gap("A signal has a frequency of 4 MHz. Its period is [[#0.25]] µs.", "T = 1 / f = 1 / 4,000,000 = 0.25 µs.")
    gap("Read the figure: the wave has a period of [[#0.5]] ms and a frequency of [[#2]] kHz.",
        "Two full cycles fit in 1 ms, so one cycle (the period) is 0.5 ms and f = 1 / 0.5 ms = 2 kHz.", fig=fig_wave)
    tf("A composite signal is made of many simple sine waves with different frequencies.", True,
       "A simple signal is one sine wave; a composite signal is a sum of many.")
    gap("A signal of 1 MHz travelling at 3 × 10⁸ m/s has a wavelength of [[#300]] m.", "λ = speed / f = 3 × 10⁸ / 10⁶ = 300 m.")

    concept("Bit rate and digital transmission")
    gap("A bit rate of 2 Mbps gives a bit interval of [[#0.5]] µs.", "Bit interval = 1 / bit rate = 1 / 2,000,000 = 0.5 µs.")
    gap("A bit interval of 100 µs gives a bit rate of [[#10]] kbps.", "Bit rate = 1 / 0.0001 = 10,000 bps = 10 kbps.")
    mc("Which is an advantage of digital transmission?", ["It needs no bandwidth", "Signals can be regenerated by repeaters, so noise does not build up",
       "It cannot be encrypted", "It never suffers attenuation"], 1, "Repeaters regenerate the bits, removing noise instead of amplifying it.")
    gap("1 byte = [[#8]] bits, 1 Mbps = [[#1000]] kbps, and 1 Gbps = [[#1000]] Mbps.", "Rate prefixes step by × 1000; bytes to bits × 8.")

    concept("Impairments")
    table("Name the impairment.", ["Symptom", "Impairment"],
          [["Signal energy is lost as it travels along the cable", "[[?Attenuation|Distortion|Noise=Attenuation]]"],
           ["The signal changes shape because frequencies travel at different speeds", "[[?Attenuation|Distortion|Noise=Distortion]]"],
           ["You hear another conversation faintly on your call", "[[?Thermal noise|Induced noise|Crosstalk|Impulse noise=Crosstalk]]"],
           ["A motor next to the cable adds errors", "[[?Thermal noise|Induced noise|Crosstalk|Impulse noise=Induced noise]]"],
           ["A lightning spike corrupts a burst of bits", "[[?Thermal noise|Induced noise|Crosstalk|Impulse noise=Impulse noise]]"]],
          "Attenuation loses energy, distortion changes shape, and noise adds unwanted energy (thermal, induced, crosstalk, impulse).")
    gap("If a signal's power drops to half, the loss is [[/^\\s*[-−]?\\s*3(\\.0+)?\\s*(db)?\\s*$/=−3 dB]] dB.",
        "dB = 10 log₁₀(P₂/P₁) = 10 log₁₀(0.5) ≈ −3 dB.")
    mc("Attenuation of a digital signal is fixed with…", ["An amplifier", "A repeater that regenerates the signal", "A modem", "A filter"], 1,
       "Analog signals use amplifiers; digital signals use repeaters.")

    concept("Delay and performance")
    gap("A signal travels 12,000 km through cable at 2.4 × 10⁸ m/s. The propagation time is [[#50]] ms.",
        "1.2 × 10⁷ m / 2.4 × 10⁸ m/s = 0.05 s = 50 ms.")
    gap("Sending a 5,000-byte message on a 1 Mbps link takes [[#40]] ms (transmission time).",
        "5,000 × 8 = 40,000 bits; 40,000 / 10⁶ = 0.04 s = 40 ms.")
    gap("With propagation 50 ms, transmission 40 ms, queuing 5 ms and processing 1 ms, the latency is [[#96]] ms.",
        "Latency = propagation + transmission + queuing + processing = 96 ms.")
    gap("A 10 Mbps link with a 20 ms delay holds [[#200000]] bits (bandwidth-delay product).", "10⁷ × 0.02 = 200,000 bits.")
    tf("Doubling the bandwidth halves the propagation time.", False,
       "Bandwidth changes the transmission time; propagation depends only on distance and speed.")

    concept("Transmission media")
    table("Pick the medium.", ["Description", "Medium"],
          [["Light kept inside a core by total internal reflection", "[[?Twisted pair|Coaxial|Fiber optic=Fiber optic]]"],
           ["Two insulated copper wires twisted to cancel noise", "[[?Twisted pair|Coaxial|Fiber optic=Twisted pair]]"],
           ["Central conductor with a metal shield, used for cable TV", "[[?Twisted pair|Coaxial|Fiber optic=Coaxial]]"]],
          "Fibre carries light; twisted pair cancels noise by twisting; coax has a shielded central conductor.")
    gap("A fibre optic cable has three parts: the [[core]], the [[cladding]] and the outer [[jacket]].", "Core, cladding, jacket.")
    table("Straight-through or crossover cable?", ["Connection", "Cable"],
          [["PC to switch", "[[?Straight-through|Crossover=Straight-through]]"], ["PC to PC", "[[?Straight-through|Crossover=Crossover]]"],
           ["Switch to switch", "[[?Straight-through|Crossover=Crossover]]"], ["Switch to router", "[[?Straight-through|Crossover=Straight-through]]"],
           ["Router to PC", "[[?Straight-through|Crossover=Crossover]]"]],
          "Like devices (PC–PC, switch–switch, router–PC) need crossover; unlike devices use straight-through.")
    table("Match each wireless band.", ["Property", "Band"],
          [["Omnidirectional, passes through walls, used for broadcast", "[[?Radio waves|Microwaves|Infrared=Radio waves]]"],
           ["Line of sight with dish antennas, unicast", "[[?Radio waves|Microwaves|Infrared=Microwaves]]"],
           ["Short range, cannot pass walls (TV remote)", "[[?Radio waves|Microwaves|Infrared=Infrared]]"]],
          "Radio < 300 MHz omnidirectional; microwave 300 MHz–300 GHz line of sight; infrared short range.")
    mc("Which UTP category supports 10 Gbps and 500 MHz?", ["CAT5e", "CAT6", "CAT6a", "CAT3"], 2, "CAT6a: 500 MHz, 10 Gbps.")

    # ================================================================ Chapter 3
    chapter(3)
    concept("Data link services and framing")
    mc("Which is NOT a data link layer service?", ["Framing", "Flow control", "Error control", "Routing between networks"], 3,
       "Routing belongs to the network layer. Data link: framing, addressing, flow control, error control, media access.")
    tf("The data link layer delivers frames only across one link (node to node), not across the whole Internet.", True,
       "It works hop by hop; the network layer handles end-to-end delivery.")
    gap("Bit stuffing: the data 0111111011111100 is sent as [[011111010111110100]].",
        "Insert a 0 after every five consecutive 1s, even when a sixth 1 follows: 011111·0·1·0·11111·0·100 → 011111010111110100.")
    gap("Byte stuffing: data A FLAG B ESC C is sent as A [[ESC]] FLAG B [[ESC]] ESC C.",
        "An ESC byte is inserted before every FLAG or ESC that appears inside the data.")
    mc("The flag 01111110 marks frame boundaries in…", ["Bit-oriented framing", "Character-oriented framing only", "CSMA/CD", "Checksum"], 0,
       "Bit-oriented protocols use the 01111110 flag and bit stuffing.")

    concept("Error types")
    table("Single-bit or burst error?", ["Situation", "Error"],
          [["Only bit 5 of the frame is flipped", "[[?Single-bit|Burst=Single-bit]]"],
           ["Bits 3 to 9 are damaged by noise", "[[?Single-bit|Burst=Burst]]"]],
          "A burst error affects two or more bits; its length runs from the first to the last corrupted bit.")
    gap("A 1 ms burst of noise on a 10 kbps link affects [[#10]] bits; on a 100 Mbps link it affects [[#100000]] bits.",
        "Bits affected = rate × duration: 10,000 × 0.001 = 10; 10⁸ × 0.001 = 100,000.")

    concept("Parity")
    gap("With even parity, the dataword 1100101 is sent as [[11001010]].", "It already has four 1s (even), so the parity bit is 0.")
    tf("A simple parity check can detect and correct a single-bit error.", False, "Parity only detects an odd number of errors; it cannot locate or correct them.")
    table("Complete the two-dimensional even-parity block.", ["Row", "Data", "Row parity"],
          [["1", "1011", "[[1]]"], ["2", "0110", "[[0]]"], ["3", "1110", "[[1]]"], ["Column parity", "[[0011]]", "[[0]]"]],
          "Row parities make each row even (1011 → 1, 0110 → 0, 1110 → 1). Column parities: 0, 0, 1, 1 → 0011. The corner bit makes both the parity row and column even: 0.")

    concept("CRC")
    gap("Dataword 1010 with generator 1011: the CRC is [[011]] and the codeword sent is [[1010011]].",
        "Append three 0s: 1010000 ÷ 1011 (modulo 2) leaves remainder 011, so the codeword is 1010 011.")
    gap("Dataword 1001 with generator 1011: the CRC is [[110]].", "1001000 → 0010000 → 0000110: remainder 110.")
    mc("The receiver divides the received codeword by the generator. It accepts the frame when…",
       ["The quotient is 1", "The remainder is all zeros", "The remainder equals the generator", "The parity is even"], 1,
       "A zero remainder means no error was detected.")
    tf("A generator of degree r detects every burst error of length r or less.", True, "That is the burst-detection property of CRC.")

    concept("Checksum")
    gap("8-bit checksum of the words 10011001 and 11100010: their one's-complement sum is [[01111100]] and the checksum is [[10000011]].",
        "10011001 + 11100010 = 1 01111011; wrap the carry: 01111011 + 1 = 01111100. The checksum is its complement: 10000011.")
    mc("At the receiver, the one's-complement sum of all words including the checksum is all 1s. The packet is…",
       ["Rejected", "Accepted", "Retransmitted twice", "Sent back"], 1, "All 1s (whose complement is 0) means no error detected.")

    concept("Error correction and flow control")
    gap("FEC with XOR: blocks C1 = 1011, C2 = 0110, C3 = 1100. The redundant block R = [[0001]]. If C2 is lost, C2 = R ⊕ C1 ⊕ C3 = [[0110]].",
        "R = 1011 ⊕ 0110 ⊕ 1100 = 0001; 0001 ⊕ 1011 ⊕ 1100 = 0110.")
    mc("Which method is better for real-time multimedia where retransmission is too slow?", ["Retransmission (ARQ)", "Forward error correction", "Stop-and-Wait", "Polling"], 1,
       "FEC repairs data at the receiver without waiting for a resend.")
    tf("In Stop-and-Wait, the sender sends one frame and waits for its acknowledgment before sending the next.", True,
       "That is the whole protocol; it is simple but uses the link poorly on long delays.")

    concept("Media access control")
    table("Classify each multiple-access method.", ["Method", "Family"],
          [["CSMA/CD", "[[?Random access|Controlled access|Channelization=Random access]]"],
           ["Token passing", "[[?Random access|Controlled access|Channelization=Controlled access]]"],
           ["Polling (select/poll)", "[[?Random access|Controlled access|Channelization=Controlled access]]"],
           ["Reservation", "[[?Random access|Controlled access|Channelization=Controlled access]]"],
           ["TDMA", "[[?Random access|Controlled access|Channelization=Channelization]]"],
           ["CDMA", "[[?Random access|Controlled access|Channelization=Channelization]]"]],
          "Random: ALOHA, CSMA, CSMA/CD, CSMA/CA. Controlled: reservation, polling, token passing. Channelization: FDMA, TDMA, CDMA.")
    table("Which persistence method?", ["Behaviour when the channel is busy / idle", "Method"],
          [["Sends immediately as soon as the line is idle", "[[?1-persistent|Non-persistent|p-persistent=1-persistent]]"],
           ["If busy, waits a random time and senses again", "[[?1-persistent|Non-persistent|p-persistent=Non-persistent]]"],
           ["When idle, sends with probability p in the next slot", "[[?1-persistent|Non-persistent|p-persistent=p-persistent]]"]],
          "1-persistent sends at once (most collisions); non-persistent backs off; p-persistent uses slots and a probability.")
    mc("In CSMA, the vulnerable time equals…", ["The transmission time", "The maximum propagation time", "Twice the frame size", "The backoff time"], 1,
       "A station that starts within one propagation time cannot yet hear the other signal.")
    gap("In CSMA/CD, when a collision is detected the station aborts and sends a [[#48]]-bit jam signal, then waits a random backoff time.",
        "The 48-bit jam makes sure every station notices the collision.")
    table("FDMA, TDMA or CDMA?", ["How the channel is shared", "Method"],
          [["Each station gets its own frequency band", "[[?FDMA|TDMA|CDMA=FDMA]]"],
           ["Each station gets its own time slot", "[[?FDMA|TDMA|CDMA=TDMA]]"],
           ["All stations send at once, separated by codes", "[[?FDMA|TDMA|CDMA=CDMA]]"]],
          "Frequency, time or code.")
    gap("A 10 Mbps channel shared fairly by 5 nodes gives each node [[#2]] Mbps on average.", "R / M = 10 / 5 = 2 Mbps.")

    # ================================================================ Chapter 4
    chapter(4)
    concept("IEEE 802 and Ethernet sublayers")
    table("Which sublayer does each job?", ["Job", "Sublayer"],
          [["Framing and the access method (CSMA/CD)", "[[?MAC|LLC=MAC]]"],
           ["Flow and error control common to all LANs", "[[?MAC|LLC=LLC]]"]],
          "IEEE splits the data link layer into LLC (common) and MAC (specific to each LAN technology).")
    tf("Ethernet is the dominant wired LAN technology and is standardized as IEEE 802.3.", True, "Ethernet = IEEE 802.3.")

    concept("Frame format")
    table("Fill the size of each Ethernet frame field in bytes.", ["Field", "Bytes"],
          [["Preamble", "[[#7]]"], ["SFD", "[[#1]]"], ["Destination address", "[[#6]]"], ["Source address", "[[#6]]"],
           ["Type / length", "[[#2]]"], ["CRC", "[[#4]]"]],
          "Preamble 7, SFD 1, destination 6, source 6, type 2, CRC 4.", fig=fig_ethernet)
    gap("The data field carries [[#46]] to [[#1500]] bytes, so a frame (without preamble and SFD) is [[#64]] to [[#1518]] bytes.",
        "Minimum 46 data bytes (64-byte frame); maximum 1500 (1518-byte frame).")
    gap("An upper layer gives only 30 bytes of data. The MAC adds [[#16]] bytes of padding.", "46 − 30 = 16 bytes of padding.")
    mc("The SFD byte 10101011 tells the receiver that…", ["The frame has ended", "The next field is the destination address", "A collision happened", "Padding follows"], 1,
       "The start frame delimiter's final 11 marks the end of synchronization.")
    tf("A type/length value of 0x0800 is a type (IPv4) because it is at least 1536.", True,
       "Values ≥ 0x0600 (1536) are types; values ≤ 1500 are lengths.")

    concept("MAC addresses")
    gap("An Ethernet address is [[#48]] bits long, written as [[#12]] hexadecimal digits.", "6 bytes = 48 bits = 12 hex digits.")
    table("Unicast, multicast or broadcast?", ["Destination address", "Type"],
          [["4A:30:10:21:10:1A", "[[?Unicast|Multicast|Broadcast=Unicast]]"],
           ["47:20:1B:2E:08:EE", "[[?Unicast|Multicast|Broadcast=Multicast]]"],
           ["FF:FF:FF:FF:FF:FF", "[[?Unicast|Multicast|Broadcast=Broadcast]]"],
           ["A2:34:45:11:92:F1", "[[?Unicast|Multicast|Broadcast=Unicast]]"]],
          "Look at the second hex digit: even (A, 2) = unicast, odd (7) = multicast; all Fs = broadcast.")
    tf("A source MAC address can be a multicast address.", False, "The source is always unicast.")

    concept("Standards and duplex")
    table("Decode the standard.", ["Name", "Speed (Mbps)", "Medium"],
          [["10Base-T", "[[#10]]", "[[?Twisted pair|Thick coax|Thin coax|Fiber=Twisted pair]]"],
           ["10Base5", "[[#10]]", "[[?Twisted pair|Thick coax|Thin coax|Fiber=Thick coax]]"],
           ["10Base2", "[[#10]]", "[[?Twisted pair|Thick coax|Thin coax|Fiber=Thin coax]]"],
           ["1000Base-F / -SX", "[[#1000]]", "[[?Twisted pair|Thick coax|Thin coax|Fiber=Fiber]]"]],
          "The number is the rate in Mbps, Base means baseband, and the suffix is the medium (T twisted pair, F/SX/LX fibre, 5 thick coax 500 m, 2 thin coax ~185 m).")
    gap("A full-duplex 100 Mbps switched link can carry a total of [[#200]] Mbps.", "100 Mbps in each direction at once.")
    mc("Which is NOT needed for full-duplex Ethernet?", ["Full-duplex NICs", "A switch instead of a hub", "Point-to-point links", "CSMA/CD"], 3,
       "With dedicated full-duplex links there are no collisions, so CSMA/CD is turned off.")
    tf("Half-duplex Ethernet (hub or shared medium) uses CSMA/CD.", True, "Stations share the medium, so collisions are possible and must be detected.")
    mc("Why does Ethernet have a minimum frame length of 64 bytes?", ["To fit the IP header", "So a sender is still transmitting when a collision comes back, letting CSMA/CD detect it",
       "To make the CRC stronger", "To match the 1500-byte maximum"], 1,
       "A frame shorter than the round-trip collision window could finish before the collision is heard.")
    table("Which Ethernet generation?", ["Speed", "Generation"],
          [["10 Mbps", "[[?Standard Ethernet|Fast Ethernet|Gigabit Ethernet|10-Gigabit Ethernet=Standard Ethernet]]"],
           ["100 Mbps", "[[?Standard Ethernet|Fast Ethernet|Gigabit Ethernet|10-Gigabit Ethernet=Fast Ethernet]]"],
           ["1000 Mbps", "[[?Standard Ethernet|Fast Ethernet|Gigabit Ethernet|10-Gigabit Ethernet=Gigabit Ethernet]]"]],
          "Standard 10, Fast 100, Gigabit 1000, 10-Gigabit 10,000 Mbps.")

    _rest(h, bank, chapter, concept, mc, tf, gap, table, S)
    return bank


def _rest(h, bank, chapter, concept, mc, tf, gap, table, S):
    """Chapters 6–10 (kept apart so each half stays readable)."""
    import cs331_chapter_quizzes_b as b
    b.define(h, chapter, concept, mc, tf, gap, table, S)
