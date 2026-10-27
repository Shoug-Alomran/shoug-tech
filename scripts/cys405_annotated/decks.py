"""CYS405 annotated slides — every Penetration Testing and Ethical Hacking deck.

One module holds all the decks: each deck is a namespace class with DECK and ANN (and AUTO_SLIDES).
Slides without an ANN entry are shown without notes. See cs331_annotated/ch01_1_introduction.py for the ANN keys."""
from .common import DECKS, mcq, see, short, tf, tip, trap, trick


def deck(key, title, chapter, lede):
    slug, file, folder, _ = DECKS[key]
    return {'key': key, 'slug': slug, 'file': file, 'title': title, 'chapter': chapter,
            'pdf': '/academics/cybersecurity/cys405/slides/%s/' % folder, 'lede': lede}


PHASES = 'Five phases: 1 Reconnaissance → 2 Scanning → 3 Gaining access → 4 Maintaining access → 5 Clearing tracks.'


class intro:
    AUTO_SLIDES = True
    DECK = deck('d01', 'Introduction to Ethical Hacking and Penetration Testing', 'Chapter 1',
                'Hacker profiles and motives, the TAP principle of controls, ethical hacking vs. penetration testing '
                'vs. audits and vulnerability assessments, ethical hackers and the CIA triad, the five hacking phases, '
                'the skills and ethics of a pen tester, laws and certifications.')
    ANN = {
        4: dict(notes=['Hat colours: black hat (malicious), white hat (authorized, ethical), gray hat (in between, may act without permission). Also script kiddies, hacktivists, suicide hackers, state-sponsored, cyber terrorists.'],
                exam=[mcq('A hacker who works with the owner’s permission to find weaknesses is a:', ['White hat', 'Black hat', 'Gray hat', 'Script kiddie'], 0, '')], weight=3),
        5: dict(notes=['TAP: controls are Technical, Administrative, Physical.']),
        9: dict(notes=['Ethical hacking = authorized hacking to find and fix weaknesses before attackers do. A pen test simulates a real attack within an agreed scope.'],
                exam=[tf('The key difference between an ethical hacker and a criminal hacker is permission (authorization).', True, '')], weight=3),
        11: dict(notes=['Audit: checks compliance with a standard. Vulnerability assessment: finds and lists weaknesses. Pen test: actually exploits them to prove impact.'],
                 tips=[trap('A vulnerability assessment does NOT exploit; a penetration test does.')],
                 exam=[mcq('Which activity actually exploits weaknesses to show their impact?', ['Penetration test', 'Vulnerability assessment', 'Security audit', 'Risk register'], 0, '')], weight=3),
        15: dict(notes=['Attacks map onto the CIA triad: disclosure (confidentiality), alteration (integrity), denial (availability), the DAD triad.'],
                 exam=[mcq('A DoS attack targets:', ['Availability', 'Confidentiality', 'Integrity', 'Non-repudiation'], 0, '')], weight=3),
        17: dict(notes=[PHASES], tips=[tip(PHASES)], weight=3),
        18: dict(notes=['Reconnaissance: gather information. Passive (no direct contact: public sources) vs. active (interacting with the target).'],
                 exam=[mcq('Searching the target’s website and news articles without touching their systems is:', ['Passive reconnaissance', 'Active reconnaissance', 'Scanning', 'Enumeration'], 0, '')], weight=3),
        19: dict(notes=['Scanning: probe the network for live hosts, open ports, services and vulnerabilities.']),
        20: dict(notes=['Gaining access: exploit a vulnerability (password cracking, buffer overflow, session hijacking…).']),
        21: dict(notes=['Maintaining access: backdoors, rootkits, Trojans to come back later.']),
        22: dict(notes=['Clearing tracks: delete logs, hide files, avoid detection.'],
                 exam=[mcq('Deleting log entries happens in which phase?', ['Clearing tracks', 'Reconnaissance', 'Scanning', 'Maintaining access'], 0, '')], weight=3),
        25: dict(notes=['Before testing: written permission (contract), scope, rules of engagement, NDA. Test types: black box (no knowledge), white box (full knowledge), gray box (partial).'],
                 exam=[mcq('A test where the tester has no prior knowledge of the target is:', ['Black-box', 'White-box', 'Gray-box', 'Crystal-box'], 0, ''),
                       tf('An ethical hacker may start testing once the scope is agreed verbally.', False, 'Always get written authorization.')], weight=3),
        27: dict(notes=['Laws (e.g. computer-misuse acts) make unauthorized access a crime regardless of intent.']),
        29: dict(notes=['Certifications: CEH, OSCP, GPEN, CompTIA PenTest+.']),
    }


class recon:
    AUTO_SLIDES = True
    DECK = deck('d02', 'Information Gathering, Footprinting and Reconnaissance', 'Chapter 2',
                'What footprinting is and why it matters, the information-gathering process, what a company website '
                'leaks, Google hacking and the GHDB, registrar and WHOIS queries, nslookup, network ranges and '
                'traceroute, tracking employees and social networks, and countermeasures.')
    ANN = {
        4: dict(notes=['Footprinting: collecting as much information as possible about a target before an attack.']),
        5: dict(notes=['Why: learn the security posture, reduce the attack area, build a network map, find vulnerabilities.']),
        7: dict(notes=['The process: gather initial info → find the network range → find active machines → open ports and access points → OS fingerprinting → map the network.']),
        10: dict(notes=['Company websites leak employee names, emails, technologies, locations, job postings that reveal systems.']),
        16: dict(notes=['Google operators: site:, filetype:, inurl:, intitle:, intext:, cache:, link:.'],
                 exam=[mcq('Which query finds PDF files only on example.com?', ['site:example.com filetype:pdf', 'inurl:pdf example.com', 'cache:example.com pdf', 'link:example.com pdf'], 0, '')], weight=3),
        24: dict(notes=['Google Hacking Database (GHDB): a catalogue of search queries ("dorks") that find exposed data.']),
        28: dict(notes=['WHOIS: registrant names, emails, phone numbers, name servers, registration dates.'],
                 exam=[mcq('Which tool reveals a domain’s registrant and name servers?', ['WHOIS', 'Traceroute', 'Nmap', 'Netstat'], 0, '')], weight=3),
        29: dict(notes=['nslookup / dig query DNS records: A (IPv4), AAAA, MX (mail), NS (name server), CNAME, SOA, PTR.'],
                 exam=[mcq('Which DNS record identifies a domain’s mail servers?', ['MX', 'A', 'NS', 'PTR'], 0, '')], weight=3),
        33: dict(notes=['Traceroute lists the routers (hops) to a host using increasing TTL values: reveals network topology.']),
        38: dict(notes=['Social networks (LinkedIn, etc.) reveal employees, roles, technologies: material for social engineering.'],
                 seen=[see('d09', 3, 'social engineering')]),
        39: dict(notes=['Countermeasures: limit what’s published, private WHOIS, staff awareness, remove sensitive metadata, monitor search engines.']),
    }


class scanning:
    AUTO_SLIDES = True
    DECK = deck('d03', 'Scanning', 'Chapter 3',
                'Port, network and vulnerability scanning, TCP flags and the three-way handshake, ICMP and ping sweeps, '
                'full-connect, stealth (half-open), inverse-flag, Xmas, ACK, idle and UDP scans, countermeasures, '
                'banner grabbing and OS fingerprinting, and Nmap and other scanners.')
    ANN = {
        6: dict(notes=['Types: port scanning (open ports/services), network scanning (live IPs), vulnerability scanning (known weaknesses).']),
        9: dict(notes=['TCP flags: SYN (start), ACK (acknowledge), FIN (finish), RST (reset), PSH (push), URG (urgent).']),
        12: dict(notes=['Three-way handshake: SYN → SYN/ACK → ACK.']),
        18: dict(notes=['Ping sweep: ICMP echo requests to a range of addresses to find live hosts.']),
        20: dict(notes=['TCP connect (full open) scan: completes the handshake. Reliable but logged.'],
                 exam=[mcq('Which scan completes the full three-way handshake?', ['TCP connect scan', 'SYN (half-open) scan', 'Xmas scan', 'NULL scan'], 0, '')], weight=3),
        21: dict(notes=['Stealth / half-open (SYN) scan: SYN → SYN/ACK means open → send RST instead of ACK. Less likely to be logged. nmap -sS.'],
                 exam=[mcq('In a SYN scan, an open port replies with:', ['SYN/ACK', 'RST', 'No response', 'FIN'], 0, ''),
                       mcq('Nmap option for a SYN (stealth) scan:', ['-sS', '-sT', '-sU', '-sX'], 0, '')], weight=3),
        22: dict(notes=['Inverse TCP flag scans (FIN, NULL, URG/PSH): no response = open (or filtered); RST = closed. Do not work against Windows.']),
        23: dict(notes=['Xmas scan: FIN + URG + PSH set ("lit up like a Christmas tree"). No reply → open; RST → closed.'],
                 tips=[trap('In SYN scans a reply means OPEN; in Xmas/FIN/NULL scans NO reply means open.')],
                 exam=[mcq('An Xmas scan sets which flags?', ['FIN, URG, PSH', 'SYN, ACK', 'SYN only', 'No flags'], 0, '')], weight=3),
        24: dict(notes=['ACK scan: maps firewall rules (filtered vs. unfiltered), not open ports.']),
        26: dict(notes=['Idle (zombie) scan: uses a third host’s predictable IP ID to scan without revealing your address.'],
                 exam=[mcq('The scan that hides the attacker’s IP by using a zombie host’s IP ID is the:', ['Idle scan', 'ACK scan', 'UDP scan', 'Connect scan'], 0, '')], weight=3),
        27: dict(notes=['UDP scan: no reply → open|filtered; ICMP port unreachable → closed. Slow.']),
        29: dict(notes=['Banner grabbing (telnet, netcat) reveals service names and versions; OS fingerprinting identifies the OS (active with Nmap -O, passive by sniffing).'],
                 exam=[mcq('Connecting with netcat to read a server’s version string is:', ['Banner grabbing', 'Ping sweep', 'ARP poisoning', 'Enumeration of SNMP'], 0, '')], weight=3),
        34: dict(notes=['Nmap: -sT connect, -sS SYN, -sU UDP, -sX Xmas, -sN NULL, -sF FIN, -sA ACK, -O OS detection, -sV version, -p ports, -Pn skip ping.'], weight=3),
    }


class enumeration:
    AUTO_SLIDES = True
    DECK = deck('d04', 'Enumeration', 'Chapter 4',
                'What enumeration extracts and why it matters, NetBIOS, SNMP, LDAP, NTP and DNS enumeration, the ports '
                'and services to know, NULL sessions, and UNIX/Linux enumeration commands.')
    ANN = {
        3: dict(notes=['Enumeration: active connections to the target to extract usernames, machine names, shares, services, groups. Happens after scanning.'],
                exam=[mcq('Extracting user names and share names through active connections is:', ['Enumeration', 'Footprinting', 'Scanning', 'Sniffing'], 0, '')], weight=3),
        9: dict(notes=['NetBIOS (UDP 137, 138, TCP 139): 16-character names; the 16th character is the service suffix (e.g. <20> file server).'],
                exam=[mcq('NetBIOS names are how many characters long?', ['16 (15 + a suffix)', '8', '32', '64'], 0, '')], weight=3),
        13: dict(notes=['SNMP (UDP 161/162) uses community strings: "public" (read) and "private" (read/write) by default.'],
                 tips=[trap('Default community strings public/private are a classic misconfiguration.')],
                 exam=[mcq('SNMP’s default read-only community string is:', ['public', 'private', 'admin', 'snmp'], 0, '')], weight=3),
        17: dict(notes=['LDAP (TCP/UDP 389) queries directory services such as Active Directory.']),
        18: dict(notes=['NTP (UDP 123) enumeration reveals hosts and time servers.']),
        19: dict(notes=['DNS zone transfer (TCP 53, AXFR) dumps every record of a zone if not restricted.'],
                 exam=[mcq('A DNS zone transfer uses:', ['TCP 53', 'UDP 161', 'TCP 139', 'UDP 123'], 0, '')], weight=3),
        22: dict(notes=['Ports to know: 21 FTP, 22 SSH, 23 Telnet, 25 SMTP, 53 DNS, 80 HTTP, 110 POP3, 135 RPC, 137–139 NetBIOS, 161 SNMP, 389 LDAP, 443 HTTPS, 445 SMB, 3389 RDP.'], weight=3),
        23: dict(notes=['NULL session: an anonymous connection to IPC$ with empty user and password (net use \\\\target\\IPC$ "" /u:"") that leaks user and share lists.'],
                 exam=[mcq('A NULL session connects to which share?', ['IPC$', 'C$', 'ADMIN$', 'PRINT$'], 0, '')], weight=3),
        26: dict(notes=['UNIX/Linux: finger, rpcinfo, showmount, rusers, enum4linux.']),
    }


class vulnerability:
    AUTO_SLIDES = True
    DECK = deck('d05', 'Vulnerability Analysis', 'Chapter 5',
                'Vulnerability research and classification (misconfiguration, defaults, buffer overflows, unpatched '
                'servers, design flaws…), network, host, wireless and application scans, scan targets and frequency, '
                'scanner pros and cons, PCI DSS, CVSS, CVE and assessment tools.')
    ANN = {
        6: dict(notes=['Vulnerability research: keep up with newly discovered weaknesses (advisories, CVE, vendor bulletins).']),
        7: dict(notes=['Classes: misconfiguration, default installations, buffer overflows, unpatched servers, design flaws, OS and application flaws, open services, default passwords.'],
                 exam=[mcq('Leaving "admin/admin" on a router is which class of vulnerability?', ['Default passwords', 'Buffer overflow', 'Design flaw', 'Unpatched server'], 0, '')], weight=3),
        10: dict(notes=['Buffer overflow: writing more data than a buffer holds overwrites memory and can run attacker code.']),
        20: dict(notes=['Assessment types: network-based, host-based, wireless, application scans.']),
        26: dict(notes=['Network-based scans see services exposed over the network; host-based scans (with an agent or credentials) see local config, patches and accounts.'],
                 exam=[mcq('Which scan type best finds missing local patches and weak file permissions?', ['Host-based', 'Network-based', 'Wireless', 'Ping sweep'], 0, '')], weight=3),
        30: dict(notes=['Scan frequency depends on risk appetite, regulations (PCI DSS: quarterly), resources and licensing.']),
        32: dict(notes=['Scanners are fast and repeatable but give false positives, miss logic flaws and can disrupt systems.'],
                 exam=[tf('A clean vulnerability scan proves a system is secure.', False, 'Scanners miss unknown and logic flaws.')], weight=3),
        35: dict(notes=['PCI DSS (card payments) requires quarterly internal and external scans (external by an Approved Scanning Vendor).']),
        39: dict(notes=['CVSS scores 0–10 from base, temporal and environmental metric groups.'],
                 exam=[mcq('CVSS is used to:', ['Score vulnerability severity', 'Name vulnerabilities', 'Scan ports', 'Encrypt data'], 0, '')], weight=3),
        43: dict(notes=['Tools: Nessus, OpenVAS, Qualys, Nexpose, Nikto (web).']),
    }


class system_hacking:
    AUTO_SLIDES = True
    DECK = deck('d06', 'System Hacking', 'Chapter 6',
                'Windows authentication (SAM, NTLM, Kerberos), the CEH system-hacking goals, password cracking '
                '(non-electronic, active online, passive online, offline rainbow-table attacks, defaults), defenses, '
                'privilege escalation, executing applications and keyloggers, and covering tracks.')
    ANN = {
        7: dict(notes=['Windows stores password hashes (LM/NTLM) in the SAM file (C:\\Windows\\System32\\config\\SAM), locked while Windows runs.']),
        5: dict(notes=['NTLM: challenge–response with the password hash. Kerberos (default in domains): tickets from a KDC.']),
        9: dict(notes=['Goals: gain access, escalate privileges, execute applications, hide files, cover tracks.']),
        15: dict(notes=['Password attacks: non-electronic (shoulder surfing, social engineering, dumpster diving), active online, passive online, offline.']),
        18: dict(notes=['Dictionary attack: try words from a list. Brute force: every combination. Hybrid: words + numbers/symbols.'],
                 exam=[mcq('Trying every possible combination of characters is a:', ['Brute-force attack', 'Dictionary attack', 'Rainbow-table attack', 'Hybrid attack'], 0, '')], weight=3),
        23: dict(notes=['Passive online: sniff the wire, man-in-the-middle, replay captured credentials.']),
        26: dict(notes=['Rainbow tables: precomputed hash → password tables; fast lookups. Defeated by salting.'],
                 tips=[trick('Salt = a random value added before hashing, so the same password hashes differently and precomputed tables fail.')],
                 exam=[mcq('The best defense against rainbow-table attacks is:', ['Salting the password hashes', 'Longer usernames', 'Disabling ICMP', 'Using HTTP'], 0, '')], weight=3),
        31: dict(notes=['Defenses: long complex passwords, lockout policies, MFA, salted hashes, no defaults, monitoring.']),
        32: dict(notes=['Privilege escalation: vertical (user → admin) or horizontal (access another user’s resources at the same level).'],
                 exam=[mcq('A normal user gaining administrator rights is:', ['Vertical privilege escalation', 'Horizontal privilege escalation', 'Enumeration', 'Footprinting'], 0, '')], weight=3),
        37: dict(notes=['Keyloggers (hardware or software) record keystrokes; spyware hides and reports activity.']),
        39: dict(notes=['Covering tracks: clear or edit logs (auditpol, clearing event logs), hide files (ADS, steganography), rootkits.']),
    }


class malware:
    AUTO_SLIDES = True
    DECK = deck('d07', 'Malware', 'Chapter 7',
                'Malware types (spyware, adware, scareware, ransomware), viruses and how they spread, worms, Trojans '
                'and how they get onto systems, infection symptoms and detection, netstat, wrappers, construction kits, '
                'backdoors, keyloggers, port redirection and pen testing for Trojans.')
    ANN = {
        5: dict(notes=['Malware = software designed to harm or abuse a system: viruses, worms, Trojans, spyware, adware, ransomware, rootkits.']),
        6: dict(notes=['Spyware: secretly gathers information about the user and sends it out.']),
        10: dict(notes=['Ransomware: encrypts the victim’s files and demands payment for the key.'],
                 exam=[mcq('Malware that encrypts files and demands payment is:', ['Ransomware', 'Adware', 'Spyware', 'A worm'], 0, '')], weight=3),
        13: dict(notes=['A virus attaches to a host file and needs USER ACTION to spread.']),
        16: dict(notes=['A worm self-replicates across networks WITHOUT user action.'],
                 tips=[trick('Virus needs a host and a user; worm spreads by itself; Trojan pretends to be useful.')],
                 exam=[mcq('Which spreads on its own without attaching to a file or needing user action?', ['Worm', 'Virus', 'Trojan', 'Adware'], 0, '')], weight=3),
        18: dict(notes=['Trojan: looks legitimate but hides a malicious payload (often a remote-access backdoor).'],
                 exam=[mcq('A "free game" that secretly opens a backdoor is a:', ['Trojan', 'Worm', 'Virus', 'Logic bomb'], 0, '')], weight=3),
        23: dict(notes=['Symptoms: slow system, strange pop-ups, disabled antivirus, unknown processes, unexpected network traffic.']),
        28: dict(notes=['netstat -an lists open ports and connections: look for unknown listening ports.']),
        29: dict(notes=['Wrappers bind a Trojan to a legitimate program so both run together.']),
        33: dict(notes=['Backdoor: a hidden way to bypass normal authentication and return later.']),
        35: dict(notes=['Port redirection (e.g. netcat, fpipe) forwards traffic from an allowed port to another host/port to bypass firewalls.']),
    }


class web_db:
    AUTO_SLIDES = True
    DECK = deck('d08', 'Web and Database Hacking', 'Chapter 8',
                'Web server operations and why servers get compromised, DNS hijacking and amplification, directory '
                'traversal, MITM, cache poisoning, DoS, session hijacking with cookies, the web-server attack '
                'methodology, web application and session attacks, database vulnerabilities and attacks, and testing.')
    ANN = {
        9: dict(notes=['Why web servers are compromised: default settings, unpatched software, misconfiguration, weak permissions, unnecessary services, poor input validation.']),
        22: dict(notes=['DNS server hijacking: attacker changes DNS records so users are sent to a malicious server.']),
        23: dict(notes=['DNS amplification: spoofed small queries to open resolvers produce large replies aimed at the victim (DDoS).'],
                 exam=[mcq('Spoofed DNS queries that make open resolvers flood a victim with large responses are:', ['DNS amplification', 'DNS hijacking', 'Directory traversal', 'Cache poisoning'], 0, '')], weight=3),
        25: dict(notes=['Directory traversal: "../" sequences to read files outside the web root (../../etc/passwd).'],
                 exam=[mcq('The request /view?file=../../../etc/passwd is a:', ['Directory traversal attack', 'SQL injection', 'XSS', 'CSRF'], 0, '')], weight=3),
        27: dict(notes=['Web cache poisoning: inject malicious content into a cache so other users receive it.']),
        29: dict(notes=['Session hijacking with cookies: steal the session ID (sniffing, XSS) and replay it.']),
        31: dict(notes=['Banner information reveals server type and version: hide or change it.']),
        36: dict(notes=['Web app attacks: SQL injection, XSS, CSRF, parameter tampering, cookie poisoning, input validation flaws.'],
                 exam=[mcq('Injecting a script into a page that runs in other users’ browsers is:', ['Cross-site scripting (XSS)', 'SQL injection', 'Directory traversal', 'DNS hijacking'], 0, '')], weight=3),
        38: dict(notes=['Session management issues: predictable IDs, IDs in URLs, no timeout, no regeneration after login.']),
        46: dict(notes=['SQL injection: user input changes the query (\' OR 1=1 --). Defense: parameterized queries, input validation, least privilege.'],
                 tips=[trick('\' OR \'1\'=\'1 makes the WHERE clause always true.')],
                 exam=[mcq('The best defense against SQL injection is:', ['Parameterized (prepared) queries', 'Longer passwords', 'Hiding the server banner', 'HTTPS only'], 0, '')], weight=3),
        49: dict(notes=['Locate databases with port scans: 1433 MS SQL, 3306 MySQL, 1521 Oracle, 5432 PostgreSQL.']),
    }


class social:
    AUTO_SLIDES = True
    DECK = deck('d09', 'Social Engineering', 'Chapter 9',
                'What social engineering is and why it works, common targets and vulnerable behaviours, attack phases, '
                'human-, computer- and mobile-based techniques (impersonation, vishing, eavesdropping, phishing…), '
                'insider threats, countermeasures and social-engineering pen tests.')
    ANN = {
        3: dict(notes=['Social engineering: manipulating people into revealing information or performing actions. Exploits trust, not technology.']),
        7: dict(notes=['Targets: help desk, technical support, system administrators, executives, receptionists.'], weight=2),
        11: dict(notes=['Behaviours exploited: authority, intimidation, consensus/social proof, scarcity, urgency, familiarity, trust, greed.'],
                 exam=[mcq('"I’m the CEO and need this password NOW" exploits:', ['Authority and urgency', 'Scarcity', 'Consensus', 'Reciprocity'], 0, '')], weight=3),
        15: dict(notes=['Why it works: no software stops it, people want to help, lack of training, no detection.']),
        16: dict(notes=['Phases: research the target → select a victim → develop a relationship → exploit it.']),
        17: dict(notes=['Types: human-based, computer-based, mobile-based.']),
        19: dict(notes=['Impersonation: pretending to be someone (IT, a vendor, an executive). Vishing = voice phishing over the phone.']),
        21: dict(notes=['Eavesdropping, shoulder surfing, dumpster diving, tailgating (following someone through a door), piggybacking (with permission).'],
                 tips=[trap('Tailgating = without the employee’s consent; piggybacking = the employee knowingly lets you in.')],
                 exam=[mcq('Following an employee through a secure door without their knowledge is:', ['Tailgating', 'Piggybacking', 'Shoulder surfing', 'Vishing'], 0, '')], weight=3),
        24: dict(notes=['Computer-based: phishing (mass email), spear phishing (targeted), whaling (executives), pop-ups, fake software.'],
                 exam=[mcq('A phishing email crafted for one specific CFO is:', ['Whaling', 'Spam', 'Vishing', 'Smishing'], 0, 'Spear phishing aimed at an executive.')], weight=3),
        27: dict(notes=['Mobile-based: malicious apps, repackaged apps, fake security apps, SMiShing (SMS phishing).']),
        31: dict(notes=['Insider threat: current or former employees, contractors with legitimate access: the hardest to detect.']),
        36: dict(notes=['Countermeasures: training and awareness, policies, verification procedures, least privilege, physical controls, shredding.'], weight=3),
        39: dict(notes=['Spot phishing: mismatched sender or link URLs, urgency, spelling errors, unexpected attachments, requests for credentials.']),
        41: dict(notes=['SE pen testing: phishing campaigns, phone pretexting, physical entry, USB drops (with written authorization).']),
    }


class sniffing_dos:
    AUTO_SLIDES = True
    DECK = deck('d10', 'Sniffing, Session Hijacking and DoS Attacks', 'Chapter 10',
                'Sniffers and passive vs. active sniffing, protocols vulnerable to sniffing, switch CAM tables and MAC '
                'flooding, ARP poisoning and its prevention, session hijacking (prediction, active-session '
                'identification, spoofing vs. hijacking), and DoS/DDoS techniques and botnets.')
    ANN = {
        4: dict(notes=['A sniffer captures packets on the network; the NIC runs in promiscuous mode.']),
        7: dict(notes=['Passive sniffing: just listen (works on hubs). Active sniffing: inject traffic to sniff a switched network (MAC flooding, ARP poisoning).'],
                exam=[mcq('Sniffing on a switched network requires:', ['Active sniffing', 'Passive sniffing', 'No special technique', 'A hub only'], 0, '')], weight=3),
        13: dict(notes=['Plaintext protocols leak credentials: Telnet, FTP, HTTP, POP3, IMAP, SMTP, SNMPv1.'],
                 exam=[mcq('Which protocol sends credentials in clear text?', ['Telnet', 'SSH', 'HTTPS', 'SFTP'], 0, '')], weight=3),
        14: dict(notes=['A switch’s CAM table maps MAC addresses to ports.']),
        17: dict(notes=['MAC flooding: fill the CAM table with fake MACs so the switch fails open and floods frames like a hub. Defense: port security.'],
                 exam=[mcq('Port security on a switch defends against:', ['MAC flooding', 'SQL injection', 'Phishing', 'DNS amplification'], 0, '')], weight=3),
        22: dict(notes=['ARP poisoning: send forged ARP replies linking the attacker’s MAC to the gateway’s IP → man in the middle.'],
                 exam=[mcq('ARP poisoning works because ARP:', ['Accepts replies without authentication', 'Uses TCP', 'Encrypts replies', 'Only runs on routers'], 0, '')], weight=3),
        26: dict(notes=['ARP spoofing prevention: static ARP entries, Dynamic ARP Inspection (DAI) with DHCP snooping, encryption.']),
        33: dict(notes=['Session hijacking: take over an authenticated session by stealing or predicting the session ID.']),
        36: dict(notes=['Predictable (linear) session IDs can be guessed; use long, random IDs.']),
        44: dict(notes=['Spoofing pretends to be another user to START a session; hijacking takes over an EXISTING session.'],
                 exam=[mcq('Taking over a session that a user has already authenticated is:', ['Session hijacking', 'Spoofing', 'Sniffing', 'Enumeration'], 0, '')], weight=3),
        47: dict(notes=['Thwart hijacking: encryption (HTTPS, IPsec), random session IDs, timeouts, re-authentication.']),
        49: dict(notes=['DoS: make a resource unavailable. DDoS: from many sources (a botnet).']),
        53: dict(notes=['ICMP flood / Smurf (spoofed broadcast pings). Ping of death: oversized packets.']),
        55: dict(notes=['SYN flood: many SYNs without the final ACK fill the half-open connection queue. Defense: SYN cookies.'],
                 exam=[mcq('A SYN flood exploits:', ['The TCP three-way handshake', 'ARP', 'DNS zone transfers', 'SNMP community strings'], 0, ''),
                       mcq('SYN cookies defend against:', ['SYN floods', 'ARP poisoning', 'XSS', 'Phishing'], 0, '')], weight=3),
        59: dict(notes=['Botnet: compromised "zombie" machines controlled by a command-and-control (C&C) server.']),
    }


class wireless:
    AUTO_SLIDES = True
    DECK = deck('d11', 'Wireless Network Hacking', 'Chapter 11',
                'Wireless modes and components, threats and the SSID, IEEE 802.11 frames and services, WEP and its '
                'flaws, WPA, WPA2 and WPA3, securing transmissions and access points, the wireless hacking methodology '
                '(discovery, GPS mapping, traffic analysis, attacks such as rogue AP and evil twin, cracking) and defenses.')
    ANN = {
        3: dict(notes=['Modes: infrastructure (clients through an access point) and ad hoc (device to device).']),
        8: dict(notes=['SSID: the network name. Hiding it is NOT real security (it still appears in probe traffic).'],
                tips=[trap('Hiding the SSID and MAC filtering are easily bypassed; use WPA2/WPA3.')],
                exam=[tf('Disabling SSID broadcast makes a wireless network secure.', False, '')], weight=3),
        16: dict(notes=['WEP: RC4 with a 24-bit IV. IVs repeat quickly, so keys can be cracked in minutes. Never use WEP.'],
                 exam=[mcq('WEP’s main weakness is its:', ['Short 24-bit IV that repeats', 'Use of AES', 'Long keys', 'Use of 802.1X'], 0, '')], weight=3),
        20: dict(notes=['WPA: TKIP (still RC4), per-packet keys, MIC. An interim fix.']),
        21: dict(notes=['WPA2: AES-CCMP. Personal (PSK) or Enterprise (802.1X/RADIUS).'],
                 exam=[mcq('WPA2 uses which encryption?', ['AES-CCMP', 'RC4 with TKIP only', 'DES', 'No encryption'], 0, '')], weight=3),
        23: dict(notes=['WPA3: SAE handshake (resists offline dictionary attacks), forward secrecy, 192-bit enterprise mode.']),
        26: dict(notes=['Secure the AP: change defaults, update firmware, strong encryption, disable WPS, limit admin access.']),
        29: dict(notes=['Methodology: Wi-Fi discovery → GPS mapping → traffic analysis → launch attacks → crack encryption.']),
        32: dict(notes=['War driving: searching for Wi-Fi from a moving car; war chalking: marking found networks with symbols.']),
        41: dict(notes=['De-authentication attack: forged deauth frames disconnect clients (DoS, or to capture the WPA handshake).']),
        43: dict(notes=['Rogue AP: an unauthorized access point plugged into the corporate network.']),
        44: dict(notes=['Evil twin: a fake AP with the SAME SSID as a legitimate one to lure clients.'],
                 exam=[mcq('An attacker’s AP broadcasting the coffee shop’s exact SSID is a(n):', ['Evil twin', 'Rogue AP inside the company', 'Ad hoc network', 'Jamming attack'], 0, '')], weight=3),
        48: dict(notes=['Jamming: radio interference that denies service.']),
        49: dict(notes=['Cracking: WEP by collecting IVs (aircrack-ng); WPA/WPA2-PSK by capturing the 4-way handshake and running a dictionary attack.']),
        50: dict(notes=['Defenses: WPA2/WPA3 with strong passphrases, 802.1X, WIDS/WIPS, rogue-AP detection, disable WPS.']),
    }


DECKS_HERE = [intro, recon, scanning, enumeration, vulnerability, system_hacking, malware, web_db, social, sniffing_dos, wireless]
