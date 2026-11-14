"""CS331 chapter quizzes, Chapters 6–10. See cs331_chapter_quizzes.py for the answer spec."""
from __future__ import annotations

import math


def define(h, chapter, concept, mc, tf, gap, table, S):
    # ================================================================ figures
    def fig_domains():
        s = S(560, 220, "Router with two interfaces: one to a switch with three PCs, one to a hub with two PCs")
        s.router(280, 40, 30, 14)
        s.text(280, 18, "Router")
        s.line(256, 48, 150, 100, sw=2)
        s.line(304, 48, 410, 100, sw=2)
        s.rect(110, 100, 80, 26, 3)
        s.text(150, 118, "Switch")
        s.rect(370, 100, 80, 26, 3)
        s.text(410, 118, "Hub")
        for x in (60, 150, 240):
            s.line(150, 126, x, 170)
            s.pc(x, 182)
        for x in (360, 460):
            s.line(410, 126, x, 170)
            s.pc(x, 182)
        return s.out()

    def fig_switch():
        s = S(520, 200, "Switch with ports 1 to 4: A on port 1, B on port 2, C on port 3, D on port 4")
        s.rect(200, 80, 120, 36, 4)
        s.text(260, 103, "Switch")
        pos = {"A": (70, 40, "1"), "B": (70, 160, "2"), "C": (450, 40, "3"), "D": (450, 160, "4")}
        for name, (x, y, port) in pos.items():
            s.pc(x, y)
            ex = 200 if x < 260 else 320
            s.line(x + (22 if x < 260 else -22), y, ex, 98)
            s.text((x + ex) / 2, (y + 98) / 2 - 6, "port " + port)
            s.text(x, y + 34, name)
        return s.out()

    def fig_graph():
        s = S(470, 260, "Weighted graph: A-B 2, A-C 5, B-C 1, B-D 4, C-D 1, C-E 6, D-E 2")
        n = {"A": (50, 130), "B": (210, 40), "C": (210, 220), "D": (410, 40), "E": (410, 220)}
        edges = [("A", "B", 2, -10, -8), ("A", "C", 5, -10, 16), ("B", "C", 1, -12, 4), ("B", "D", 4, 0, -8),
                 ("C", "D", 1, 12, 4), ("C", "E", 6, 0, 18), ("D", "E", 2, 14, 4)]
        r = 18
        for a, b, w, dx, dy in edges:
            (x1, y1), (x2, y2) = n[a], n[b]
            L = math.hypot(x2 - x1, y2 - y1)
            ux, uy = (x2 - x1) / L, (y2 - y1) / L
            s.line(x1 + ux * r, y1 + uy * r, x2 - ux * r, y2 - uy * r, sw=1.8)
            s.text((x1 + x2) / 2 + dx, (y1 + y2) / 2 + dy, str(w), bold=True)
        for k, (x, y) in n.items():
            s.circle(x, y, 18)
            s.text(x, y + 5, k, bold=True)
        return s.out()

    def fig_handshake():
        s = S(560, 360, "TCP timeline between client and server with five numbered segments")
        s.text(130, 22, "Client (ISN 8000)", bold=True)
        s.text(430, 22, "Server (ISN 15000)", bold=True)
        s.line(130, 34, 130, 345, sw=2)
        s.line(430, 34, 430, 345, sw=2)
        segs = [(1, 50, ""), (2, 110, ""), (3, 170, ""), (4, 230, "500 bytes of data"), (5, 290, "")]
        for no, y, label in segs:
            left_to_right = no in (1, 3, 4)
            x1, x2 = (130, 430) if left_to_right else (430, 130)
            s.arrow(x1, y, x2, y + 40)
            s.text(280, y + 8, f"Segment {no}" + (f": {label}" if label else ""), bold=True)
        return s.out()

    def fig_dns():
        s = S(600, 250, "Host A, its local DNS server, the root server, the .com server and the mcgraw.com server")
        boxes = {"Host A": (70, 200), "Local server": (230, 200), "Root server": (230, 50), ".com server": (420, 50), "mcgraw.com server": (490, 200)}
        for name, (x, y) in boxes.items():
            w = 8 * len(name) + 30
            s.rect(x - w / 2, y - 18, w, 36, 4)
            s.text(x, y + 5, name)
        s.text(300, 140, "Numbered messages 1–8 travel between these servers.")
        s.text(300, 160, "Answer for iterative and for recursive resolution below.")
        return s.out()

    def fig_tree():
        s = S(520, 250, "DNS name space: root, then com, edu, sa; under sa: edu; under edu.sa: psu; under psu: cs")
        n = {"root (.)": (260, 30), "com": (110, 90), "edu": (260, 90), "sa": (410, 90), "edu ": (410, 150), "psu": (410, 205), "cs": (300, 205)}
        for a, b in [("root (.)", "com"), ("root (.)", "edu"), ("root (.)", "sa"), ("sa", "edu "), ("edu ", "psu"), ("psu", "cs")]:
            (x1, y1), (x2, y2) = n[a], n[b]
            s.line(x1, y1 + 10, x2, y2 - 10)
        for k, (x, y) in n.items():
            s.text(x, y + 4, k.strip(), bold=True)
        return s.out()

    # ================================================================ Chapter 6
    chapter(6)
    concept("Devices and layers")
    table("Fill the layer and the data unit of each device.", ["Device", "Layer", "Data unit"],
          [["Hub (repeater)", "[[?Physical|Data link|Network=Physical]]", "[[?Bits|Frames|Packets=Bits]]"],
           ["Link-layer switch (bridge)", "[[?Physical|Data link|Network=Data link]]", "[[?Bits|Frames|Packets=Frames]]"],
           ["Router", "[[?Physical|Data link|Network=Network]]", "[[?Bits|Frames|Packets=Packets]]"]],
          "Hub hears bits, switch studies frames, router reads packets.")
    tf("A hub filters frames by their destination MAC address.", False, "A hub copies every bit out of every other port; it does not look at addresses.")
    tf("A router interface has both an IP address and a MAC address.", True, "It is a network-layer device that also sits on a link.")
    mc("A network built with a hub is physically a ___ but behaves logically like a ___.", ["bus, star", "star, bus", "ring, mesh", "mesh, star"], 1,
       "Cables form a star around the hub, but every station hears every transmission, like a bus.")

    concept("Collision and broadcast domains")
    gap("In the figure there are [[#5]] collision domains and [[#2]] broadcast domains.",
        "Every switch port is its own collision domain: 3 PCs + the uplink to the router = 4. The hub and everything on it (2 PCs + its link to the router) share 1. Total 5. Each router interface is one broadcast domain: 2.",
        fig=fig_domains)
    tf("A switch with 8 connected ports creates 8 collision domains but only 1 broadcast domain.", True,
       "Switches split collision domains; routers and VLANs split broadcast domains.")
    mc("Which device (or feature) separates broadcast domains?", ["Hub", "Repeater", "Router or VLANs", "Switch without VLANs"], 2,
       "Broadcasts stop at a router interface; VLANs make separate broadcast domains on one switch.")

    concept("Switch learning and forwarding")
    table("The switch table starts empty. For each frame, fill what the switch learns and what it does.",
          ["Frame", "Entry learned (station : port)", "Action"],
          [["A → D", "[[A1|A:1|A port 1]]", "[[?Flood out ports 2, 3, 4|Forward out port 4 only|Drop=Flood out ports 2, 3, 4]]"],
           ["D → A", "[[D4|D:4|D port 4]]", "[[?Flood out ports 1, 2, 3|Forward out port 1 only|Drop=Forward out port 1 only]]"],
           ["B → A", "[[B2|B:2|B port 2]]", "[[?Flood out ports 1, 3, 4|Forward out port 1 only|Drop=Forward out port 1 only]]"]],
          "A switch learns the source address and its incoming port. An unknown destination is flooded to every other port; a known one goes out its port only.",
          marks=2, fig=fig_switch)
    mc("Redundant links between switches without spanning tree cause…", ["Faster delivery", "Broadcast storms (frames loop forever)", "Fewer collisions", "Smaller MAC tables"], 1,
       "Broadcasts circulate endlessly around the loop.")
    tf("Spanning tree removes loops by logically blocking some ports while keeping the physical links.", True,
       "Blocked links stay as backups.")
    table("Store-and-forward or cut-through?", ["Behaviour", "Switching"],
          [["Receives the whole frame and checks the CRC before sending it on", "[[?Store-and-forward|Cut-through=Store-and-forward]]"],
           ["Starts forwarding as soon as it reads the destination address", "[[?Store-and-forward|Cut-through=Cut-through]]"]],
          "Store-and-forward is safer; cut-through is faster.")

    concept("Bandwidth and cabling")
    gap("10 hosts share a 100 Mbps hub: each gets about [[#10]] Mbps. On a full-duplex 100 Mbps switch each host gets [[#200]] Mbps.",
        "A hub shares its bandwidth (100 / 10). A full-duplex switch port gives 100 Mbps each way.")
    gap("In a star LAN the cable from a host NIC to the hub can be at most [[#100]] m, and any two nodes at most [[#200]] m apart.",
        "100 m per segment, 200 m between nodes.")

    concept("VLANs")
    mc("A VLAN creates a separate…", ["Collision domain", "Broadcast domain", "IP header", "Physical cable"], 1, "VLANs are broadcast domains defined in software.")
    gap("Three advantages of VLANs: lower [[cost]] and installation time, more [[security]], and virtual [[workgroups|workgroup]].",
        "Cost and time reduction, security, virtual workgroups.")
    tf("Moving a station to another VLAN requires rewiring the building.", False, "Membership is changed in software.")

    # ================================================================ Chapter 7
    chapter(7)
    concept("Network layer duties and switching")
    table("Match the duty.", ["Description", "Duty"],
          [["Encapsulating the payload in a packet at the source", "[[?Packetizing|Routing|Forwarding=Packetizing]]"],
           ["Running protocols to build the routing table", "[[?Packetizing|Routing|Forwarding=Routing]]"],
           ["Choosing the output interface for one arriving packet", "[[?Packetizing|Routing|Forwarding=Forwarding]]"]],
          "Packetizing wraps, routing plans paths, forwarding moves each packet.")
    mc("The Internet's network layer uses…", ["Virtual-circuit switching", "Datagram (connectionless) switching", "Circuit switching", "Token passing"], 1,
       "Each datagram is routed independently, with no network-layer handshake.")
    tf("In datagram switching, packets of one message can arrive out of order.", True, "They may take different paths.")
    gap("The four delays a packet meets are [[transmission]], [[propagation]], [[processing]] and [[queuing|queueing]] delay.",
        "Transmission, propagation, processing, queuing.")

    concept("IPv4 addresses and classes")
    gap("An IPv4 address has [[#32]] bits, giving 2^32 = [[#4294967296]] addresses.", "32 bits, 4,294,967,296 addresses.")
    gap("11000000 10101000 00000001 00001010 in dotted decimal is [[/^\\s*192\\.168\\.1\\.10\\s*$/=192.168.1.10]].",
        "11000000 = 192, 10101000 = 168, 00000001 = 1, 00001010 = 10.")
    table("Find the class.", ["Address", "Class"],
          [["10.20.30.40", "[[?A|B|C|D|E=A]]"], ["172.16.5.4", "[[?A|B|C|D|E=B]]"], ["200.1.2.3", "[[?A|B|C|D|E=C]]"],
           ["230.0.0.1", "[[?A|B|C|D|E=D]]"], ["245.1.1.1", "[[?A|B|C|D|E=E]]"]],
          "First byte: A 0–127, B 128–191, C 192–223, D 224–239 (multicast), E 240–255.")
    mc("Which address is invalid?", ["192.168.30.1", "10.0.0.255", "192.168.300.1", "172.31.0.9"], 2, "300 is larger than 255, so it cannot be an octet.")
    table("Private or public?", ["Address", "Kind"],
          [["10.5.6.7", "[[?Private|Public=Private]]"], ["172.20.1.1", "[[?Private|Public=Private]]"], ["172.32.1.1", "[[?Private|Public=Public]]"],
           ["192.168.9.9", "[[?Private|Public=Private]]"], ["8.8.8.8", "[[?Private|Public=Public]]"]],
          "Private ranges: 10.0.0.0/8, 172.16.0.0–172.31.255.255, 192.168.0.0/16.")
    gap("The default mask of class B is [[/^\\s*255\\.255\\.0\\.0\\s*$/=255.255.0.0]], written as /[[#16]].", "Class B: 16 network bits.")

    concept("Network address, masks and CIDR")
    gap("For 192.168.10.77/24 the network address is [[/^\\s*192\\.168\\.10\\.0\\s*$/=192.168.10.0]] and the broadcast is [[/^\\s*192\\.168\\.10\\.255\\s*$/=192.168.10.255]].",
        "Zero the host byte for the network, set it to all 1s (255) for the broadcast.")
    gap("172.16.45.200 AND 255.255.240.0 = [[/^\\s*172\\.16\\.32\\.0\\s*$/=172.16.32.0]].", "45 AND 240 = 00101101 AND 11110000 = 00100000 = 32.")
    gap("The block containing 205.16.37.39/28 starts at [[/^\\s*205\\.16\\.37\\.32\\s*$/=205.16.37.32]], ends at [[/^\\s*205\\.16\\.37\\.47\\s*$/=205.16.37.47]] and has [[#16]] addresses.",
        "/28 leaves 4 host bits (16 addresses). 39 AND 240 = 32, so 32 to 47.")
    table("Hosts per subnet.", ["Prefix", "Usable hosts"], [["/24", "[[#254]]"], ["/26", "[[#62]]"], ["/27", "[[#30]]"], ["/30", "[[#2]]"]],
          "2^(32 − prefix) − 2.")
    gap("/27 written as a dotted mask is [[/^\\s*255\\.255\\.255\\.224\\s*$/=255.255.255.224]].", "27 ones: the last byte is 11100000 = 224.")
    mc("255.255.255.255 is…", ["A directed broadcast", "The limited broadcast (this network only)", "A loopback address", "A class A network"], 1,
       "Limited broadcast stays on the local network; a directed broadcast targets all hosts of a named network.")

    concept("Subnetting")
    table("Split 192.168.10.0/24 into 4 equal subnets. Fill the first two.", ["Subnet", "Network", "First host", "Last host", "Broadcast"],
          [["1", "[[/^\\s*192\\.168\\.10\\.0\\s*$/=192.168.10.0]]", "[[/^\\s*192\\.168\\.10\\.1\\s*$/=192.168.10.1]]", "[[/^\\s*192\\.168\\.10\\.62\\s*$/=192.168.10.62]]", "[[/^\\s*192\\.168\\.10\\.63\\s*$/=192.168.10.63]]"],
           ["2", "[[/^\\s*192\\.168\\.10\\.64\\s*$/=192.168.10.64]]", "[[/^\\s*192\\.168\\.10\\.65\\s*$/=192.168.10.65]]", "[[/^\\s*192\\.168\\.10\\.126\\s*$/=192.168.10.126]]", "[[/^\\s*192\\.168\\.10\\.127\\s*$/=192.168.10.127]]"]],
          "4 subnets need 2 borrowed bits → /26, blocks of 64: .0–.63 and .64–.127.", marks=2)
    gap("Splitting a class C network into 6 subnets needs [[#3]] borrowed bits, giving a /[[#27]] mask.", "6 − 1 = 5 = 101 in binary: 3 bits. 24 + 3 = 27.")
    gap("Borrowing 4 bits from a class B network creates [[#16]] subnets.", "2^(new prefix − classful prefix) = 2⁴ = 16.")

    concept("DHCP, ARP, NAT and the IPv4 header")
    gap("DHCP gives a host four settings: IP [[address]], subnet [[mask]], default [[gateway|router]] and [[DNS]] server.", "IP address, mask, gateway, DNS server.")
    table("Broadcast or unicast?", ["Message", "Sent as"],
          [["ARP request", "[[?Broadcast|Unicast=Broadcast]]"], ["ARP reply", "[[?Broadcast|Unicast=Unicast]]"]],
          "The requester does not know the MAC yet, so it asks everyone; the owner answers it directly.")
    mc("Host 10.1.1.5/24 sends to 10.1.2.9. Whose MAC address does it ask for with ARP?", ["10.1.2.9", "Its default gateway", "The DNS server", "The broadcast address"], 1,
       "The destination is on another network, so the frame goes to the router.")
    mc("NAT mainly…", ["Encrypts packets", "Lets many private hosts share a public IP address", "Assigns IP addresses", "Finds MAC addresses"], 1,
       "It translates private addresses to a public one using a table.")
    table("IPv4 header facts.", ["Question", "Answer"],
          [["HLEN field value 5 means a header of … bytes", "[[#20]]"], ["Protocol field value for TCP", "[[#6]]"],
           ["Protocol field value for UDP", "[[#17]]"], ["Maximum total length (bytes)", "[[#65535]]"]],
          "HLEN counts 4-byte words (5 × 4 = 20); protocol 6 = TCP, 17 = UDP; total length is 16 bits.")
    tf("Every router decrements TTL and recomputes the header checksum.", True, "TTL changes, so the header checksum must be recomputed.")
    gap("A fragment has offset value 100: its first byte is byte number [[#800]] of the original data.", "The offset counts 8-byte units: 100 × 8 = 800.")
    table("Fragmentation flags.", ["Flag set", "Meaning"],
          [["D = 1", "[[?Do not fragment|More fragments follow|Last fragment=Do not fragment]]"],
           ["M = 1", "[[?Do not fragment|More fragments follow|Last fragment=More fragments follow]]"],
           ["M = 0 with a non-zero offset", "[[?Do not fragment|More fragments follow|Last fragment=Last fragment]]"]],
          "D forbids fragmentation, M = 1 means more fragments follow, M = 0 marks the last one.")
    tf("Fragments are reassembled by each router along the path.", False, "Only the destination reassembles them.")

    # ================================================================ Chapter 8
    chapter(8)
    concept("Routing vs forwarding")
    table("Routing or forwarding?", ["Activity", "Which"],
          [["Building the table with a protocol", "[[?Routing|Forwarding=Routing]]"],
           ["Looking up one packet's destination to pick an interface", "[[?Routing|Forwarding=Forwarding]]"]],
          "Routing plans; forwarding acts per packet.")
    tf("Internet routing is hierarchical because one flat table for every router would be far too large.", True, "Autonomous systems split the problem.")
    table("Static or dynamic routing?", ["Description", "Type"],
          [["Entered by an administrator, changes slowly", "[[?Static|Dynamic=Static]]"], ["Updated automatically by a protocol", "[[?Static|Dynamic=Dynamic]]"]],
          "Static routes are manual; dynamic routes adapt.")

    concept("Least-cost paths")
    table("From node A, find the least cost and the next hop to each node.", ["Destination", "Least cost", "Next hop"],
          [["B", "[[#2]]", "[[B]]"], ["C", "[[#3]]", "[[B]]"], ["D", "[[#4]]", "[[B]]"], ["E", "[[#6]]", "[[B]]"]],
          "A→B = 2; A→C via B = 2 + 1 = 3 (direct is 5); A→D via B, C = 4; A→E via B, C, D = 6 (other paths cost 8).", marks=2, fig=fig_graph)
    tf("The shortest path always has the fewest hops.", False, "It has the least total cost; a longer path can be cheaper.")

    concept("Forwarding tables")
    table("A router has these entries, checked longest mask first: 200.10.8.128/25 → m2, 200.10.8.0/21 → m1, 200.10.0.0/16 → m0, default → m3. Which interface for each destination?",
          ["Destination", "Interface"],
          [["200.10.8.200", "[[?m0|m1|m2|m3=m2]]"], ["200.10.12.5", "[[?m0|m1|m2|m3=m1]]"], ["200.10.99.1", "[[?m0|m1|m2|m3=m0]]"],
           ["201.1.1.1", "[[?m0|m1|m2|m3=m3]]"], ["200.10.8.100", "[[?m0|m1|m2|m3=m1]]"]],
          "200 AND 128 = 128 → /25 match. 12 AND 248 = 8 → /21 match. 99 AND 248 = 96 → only /16 matches. 201.x matches nothing → default. 100 AND 128 = 0 → not the /25, but /21 matches.",
          marks=2)
    table("Name the route type.", ["Entry", "Type"],
          [["0.0.0.0/0", "[[?Network-specific|Host-specific|Default=Default]]"], ["192.168.5.0/24", "[[?Network-specific|Host-specific|Default=Network-specific]]"],
           ["192.168.5.7/32", "[[?Network-specific|Host-specific|Default=Host-specific]]"]],
          "/0 matches everything (default); /32 is one host.")

    concept("Distance vector and link state")
    table("Node X has neighbours Y (link cost 3) and Z (link cost 1). Y reports distances P 4, Q 7, R 2; Z reports P 8, Q 2, R 5. Fill X's new table.",
          ["Destination", "Cost", "Next hop"],
          [["P", "[[#7]]", "[[Y]]"], ["Q", "[[#3]]", "[[Z]]"], ["R", "[[#5]]", "[[Y]]"]],
          "P: min(3 + 4, 1 + 8) = 7 via Y. Q: min(3 + 7, 1 + 2) = 3 via Z. R: min(3 + 2, 1 + 5) = 5 via Y.", marks=2)
    table("Distance vector or link state?", ["Feature", "Algorithm"],
          [["Shares its whole table with neighbours only", "[[?Distance vector|Link state=Distance vector]]"],
           ["Floods LSPs and builds a full map (LSDB)", "[[?Distance vector|Link state=Link state]]"],
           ["Uses Dijkstra's algorithm", "[[?Distance vector|Link state=Link state]]"],
           ["Uses the Bellman-Ford equation", "[[?Distance vector|Link state=Distance vector]]"],
           ["RIP", "[[?Distance vector|Link state=Distance vector]]"], ["OSPF", "[[?Distance vector|Link state=Link state]]"]],
          "DV = neighbour gossip (Bellman-Ford, RIP); LS = everyone builds the same map (LSPs, Dijkstra, OSPF).")

    concept("Autonomous systems")
    table("Interior or exterior routing protocol?", ["Protocol", "Kind"],
          [["RIP", "[[?Interior|Exterior=Interior]]"], ["OSPF", "[[?Interior|Exterior=Interior]]"], ["EIGRP", "[[?Interior|Exterior=Interior]]"], ["BGP", "[[?Interior|Exterior=Exterior]]"]],
          "Interior protocols work inside one AS; BGP connects autonomous systems.")
    mc("A router at the edge of an AS that connects it to a neighbouring AS runs…", ["Only RIP", "Only BGP", "An interior protocol inside and BGP outside", "No routing protocol"], 2,
       "Border routers run both.")
    tf("An autonomous system is a group of networks under one administration with a unique AS number.", True, "That is the definition.")

    # ================================================================ Chapter 9
    chapter(9)
    concept("Transport services")
    table("Which delivery?", ["Delivery", "Layer"],
          [["Process to process", "[[?Data link|Network|Transport=Transport]]"], ["Host to host", "[[?Data link|Network|Transport=Network]]"],
           ["Node to node (hop)", "[[?Data link|Network|Transport=Data link]]"]], "IP finds the host; the port finds the process.")
    gap("Transport duties include process-to-process delivery, [[addressing]] with port numbers, encapsulation, [[multiplexing]] and demultiplexing, connection control, flow and error control, and [[congestion]] control.",
        "Addressing, multiplexing, congestion control (plus the others listed).")
    table("Multiplexing or demultiplexing?", ["Description", "Which"],
          [["Many processes' messages go down into one network layer at the sender", "[[?Multiplexing|Demultiplexing=Multiplexing]]"],
           ["Arriving segments are handed to the right process by port", "[[?Multiplexing|Demultiplexing=Demultiplexing]]"]],
          "Many-to-one going down, one-to-many going up.")

    concept("Ports and sockets")
    gap("A port number is [[#16]] bits, so ports range from 0 to [[#65535]]. Well-known ports are 0 to [[#1023]].", "16 bits; well-known 0–1023 (IANA).")
    table("Well-known ports.", ["Service", "Port"],
          [["HTTP", "[[#80]]"], ["DNS", "[[#53]]"], ["SMTP", "[[#25]]"], ["Telnet", "[[#23]]"], ["FTP (control)", "[[#21]]"], ["HTTPS", "[[#443]]"]],
          "HTTP 80, DNS 53, SMTP 25, Telnet 23, FTP 21 (20 data), HTTPS 443.")
    gap("A socket address is an IP [[address]] plus a [[port]] number.", "IP + port identifies one process endpoint.")
    mc("Which four values identify one TCP connection?", ["Source IP, destination IP, source MAC, destination MAC", "Source IP, source port, destination IP, destination port",
       "Source port, destination port, sequence number, ACK", "Destination IP and destination port only"], 1,
       "Different source ports let one client open several connections to the same server.")

    concept("UDP vs TCP")
    table("TCP or UDP?", ["Feature or use", "Protocol"],
          [["Connection-oriented with a handshake", "[[?TCP|UDP=TCP]]"], ["No flow or error control, low overhead", "[[?TCP|UDP=UDP]]"],
           ["Reliable, ordered byte stream", "[[?TCP|UDP=TCP]]"], ["DNS queries", "[[?TCP|UDP=UDP]]"],
           ["Live video streaming", "[[?TCP|UDP=UDP]]"], ["Downloading a large file exactly", "[[?TCP|UDP=TCP]]"], ["Web pages (HTTP)", "[[?TCP|UDP=TCP]]"]],
          "TCP when every byte must arrive in order; UDP when speed matters or one short request is enough.")
    table("Flow control or congestion control?", ["Purpose", "Mechanism"],
          [["Stops the sender from overflowing the receiver's buffer", "[[?Flow control|Congestion control=Flow control]]"],
           ["Reduces load when the network itself is overloaded", "[[?Flow control|Congestion control=Congestion control]]"]],
          "Flow control protects the receiver; congestion control protects the network.")

    concept("TCP sequence numbers and connections")
    table("Fill the flags, sequence number and acknowledgment number of each segment in the timeline.",
          ["Segment", "Flags", "Sequence number", "Acknowledgment number"],
          [["1", "[[?SYN|SYN + ACK|ACK|FIN=SYN]]", "[[#8000]]", "— (none)"],
           ["2", "[[?SYN|SYN + ACK|ACK|FIN=SYN + ACK]]", "[[#15000]]", "[[#8001]]"],
           ["3", "[[?SYN|SYN + ACK|ACK|FIN=ACK]]", "[[#8001]]", "[[#15001]]"],
           ["4 (500 data bytes)", "ACK + data", "[[#8001]]", "[[#15001]]"],
           ["5", "[[?SYN|SYN + ACK|ACK|FIN=ACK]]", "[[#15001]]", "[[#8501]]"]],
          "SYN consumes one sequence number, so the server acknowledges 8001. A pure ACK consumes none, so the first data byte is still 8001. After 500 bytes (8001–8500) the server acknowledges 8501.",
          marks=3, fig=fig_handshake)
    gap("A 6,000-byte file is sent in 1,000-byte segments, the first byte numbered 10001. Segment 3 has sequence number [[#12001]], and segment 6 carries bytes 15001 to [[#16000]].",
        "Segment k starts at 10001 + (k − 1) × 1000.")
    gap("A receiver has correctly received bytes up to 13000. Its acknowledgment number is [[#13001]].", "ACK = next byte expected = last byte received + 1.")
    gap("Connection termination uses [[FIN]] segments: FIN → ACK → FIN → ACK.", "Each side closes its direction with a FIN that the other acknowledges.")
    tf("TCP sequence numbers count segments, not bytes.", False, "They number bytes; each segment's number is the number of its first byte.")
    tf("The receive window (rwnd) tells the sender how many bytes it may send before waiting for an acknowledgment.", True, "That is how TCP does flow control.")

    # ================================================================ Chapter 10
    chapter(10)
    concept("Purpose of DNS")
    mc("Which question does DNS answer?", ["Which MAC belongs to an IP?", "Which IP address belongs to this host name?", "Which port does a process use?", "Which route is shortest?"], 1,
       "DNS maps names to IP addresses (ARP maps IP to MAC).")
    gap("DNS is a client-server application that uses port [[#53]] over UDP or TCP.", "Port 53; UDP for normal queries, TCP for zone transfers or large replies.")
    table("Which protocol maps what?", ["Mapping", "Protocol"],
          [["Host name → IP address", "[[?DNS|ARP|DHCP=DNS]]"], ["IP address → MAC address", "[[?DNS|ARP|DHCP=ARP]]"],
           ["Gives a host its IP settings", "[[?DNS|ARP|DHCP=DHCP]]"]], "DNS names, ARP links, DHCP configuration.")

    concept("Name space, domains and labels")
    gap("Using the tree, the full domain name of the node cs is [[/^\\s*cs\\.psu\\.edu\\.sa\\.?\\s*$/=cs.psu.edu.sa.]]", "Read the labels from the node up to the root, separated by dots.", fig=fig_tree)
    tf("The root of the DNS tree has an empty label, written as a dot.", True, "That is why an FQDN ends with a dot.")
    tf("Two children of the same node can have the same label.", False, "Children of one node must have different labels; that keeps names unique.")
    mc("A domain is…", ["One host", "A subtree of the domain name space", "A port number", "An IP block"], 1, "The domain name is the name of the node at the top of that subtree.")
    table("Generic or country domain?", ["Label", "Kind"],
          [["edu", "[[?Generic|Country=Generic]]"], ["org", "[[?Generic|Country=Generic]]"], ["sa", "[[?Generic|Country=Country]]"], ["mil", "[[?Generic|Country=Generic]]"]],
          "Generic labels describe the organization type; two-letter labels are countries.")
    table("Match the generic label.", ["Organization", "Label"],
          [["Non-profit organizations", "[[org]]"], ["Educational institutions", "[[edu]]"], ["Commercial organizations", "[[com]]"], ["Network support centres", "[[net]]"]],
          "org, edu, com, net.")

    concept("FQDN vs PQDN")
    table("FQDN or PQDN?", ["Name", "Kind"],
          [["challenger.atc.fhda.edu.", "[[?FQDN|PQDN=FQDN]]"], ["challenger", "[[?FQDN|PQDN=PQDN]]"], ["cs.hmme", "[[?FQDN|PQDN=PQDN]]"], ["www.funny.int.", "[[?FQDN|PQDN=FQDN]]"]],
          "Only a name that ends with the root dot is fully qualified.")
    mc("Who completes a PQDN?", ["The root server", "The DNS resolver on the client", "The secondary server", "The router"], 1,
       "The resolver adds the missing suffix; only an FQDN can be mapped to an address.")

    concept("Name servers, zones and caching")
    table("Match the server or process.", ["Description", "Term"],
          [["Holds pointers to every top-level domain server (13 worldwide)", "[[?Root server|Primary server|Secondary server|Zone transfer|Caching=Root server]]"],
           ["Loads its zone data from a disk file and is where records are changed", "[[?Root server|Primary server|Secondary server|Zone transfer|Caching=Primary server]]"],
           ["Copies all its data from the primary server", "[[?Root server|Primary server|Secondary server|Zone transfer|Caching=Secondary server]]"],
           ["The download from primary to secondary", "[[?Root server|Primary server|Secondary server|Zone transfer|Caching=Zone transfer]]"],
           ["Remembering recent answers to reply faster next time", "[[?Root server|Primary server|Secondary server|Zone transfer|Caching=Caching]]"]],
          "Root servers point to TLD servers; primary loads from disk; secondary copies by zone transfer; caching keeps answers for their TTL.")
    gap("There are [[#13]] root servers.", "13 logical root servers, spread worldwide.")
    tf("DNS is a centralized database stored on one server.", False, "It is distributed and hierarchical, so there is no single point of failure.")
    tf("Cached DNS answers carry a time-to-live so out-of-date mappings expire.", True, "TTL limits how long an answer is reused.")

    concept("Recursive and iterative resolution")
    table("Iterative resolution: for each message, who sends it and what does it carry?", ["Message", "Sent by", "Carries"],
          [["1", "[[?Host A|Local server|Root server|.com server|mcgraw.com server=Host A]]", "[[?Query|Referral|Final IP address=Query]]"],
           ["3", "[[?Host A|Local server|Root server|.com server|mcgraw.com server=Root server]]", "[[?Query|Referral|Final IP address=Referral]]"],
           ["4", "[[?Host A|Local server|Root server|.com server|mcgraw.com server=Local server]]", "[[?Query|Referral|Final IP address=Query]]"],
           ["5", "[[?Host A|Local server|Root server|.com server|mcgraw.com server=.com server]]", "[[?Query|Referral|Final IP address=Referral]]"],
           ["7", "[[?Host A|Local server|Root server|.com server|mcgraw.com server=mcgraw.com server]]", "[[?Query|Referral|Final IP address=Final IP address]]"],
           ["8", "[[?Host A|Local server|Root server|.com server|mcgraw.com server=Local server]]", "[[?Query|Referral|Final IP address=Final IP address]]"]],
          "Iterative: the local server asks root (1–3), then .com (4–5), then mcgraw.com (6–7) itself; each server replies with a referral to the next one until mcgraw.com gives the address, which goes back to A (8).",
          marks=3, fig=fig_dns)
    table("Recursive resolution: who sends each message?", ["Message", "Sent by", "Sent to"],
          [["3", "[[?Host A|Local server|Root server|.com server|mcgraw.com server=Root server]]", "[[?Host A|Local server|Root server|.com server|mcgraw.com server=.com server]]"],
           ["5", "[[?Host A|Local server|Root server|.com server|mcgraw.com server=mcgraw.com server]]", "[[?Host A|Local server|Root server|.com server|mcgraw.com server=.com server]]"],
           ["7", "[[?Host A|Local server|Root server|.com server|mcgraw.com server=Root server]]", "[[?Host A|Local server|Root server|.com server|mcgraw.com server=Local server]]"]],
          "Recursive: each server asks the next one for you (1 A→local, 2 local→root, 3 root→.com, 4 .com→mcgraw.com), and the answer travels back the same way (5 mcgraw.com→.com, 6 .com→root, 7 root→local, 8 local→A).",
          marks=2)
    table("Recursive or iterative?", ["Description", "Method"],
          [["The local server receives referrals and contacts every server itself", "[[?Recursive|Iterative=Iterative]]"],
           ["Each server forwards the query and the answer returns along the same chain", "[[?Recursive|Iterative=Recursive]]"]],
          "Recursive is a relay race; iterative is \"I do it myself\".")
