"""CYS406 annotated slides — every Data and Network Security deck.

One module holds all the decks: each deck is a namespace class with DECK and ANN (and AUTO_SLIDES).
Slides without an ANN entry are shown without notes. See cs331_annotated/ch01_1_introduction.py for the ANN keys."""
from .common import DECKS, mcq, see, short, tf, tip, trap, trick


def deck(key, title, chapter, lede):
    slug, file, folder, _ = DECKS[key]
    return {'key': key, 'slug': slug, 'file': file, 'title': title, 'chapter': chapter,
            'pdf': '/academics/cybersecurity/cys406/slides/%s/' % folder, 'lede': lede}


class fundamentals:
    AUTO_SLIDES = True
    DECK = deck('d01', 'Network Security Fundamentals', 'Chapter 1',
                'Threats, vulnerabilities, attacks and threat actors, attacker methodologies, the goals and principles '
                'of network defense (information assurance), defense approaches, administrative controls: regulatory '
                'frameworks, ISO standards, security policies and awareness training, then physical and technical controls.')
    ANN = {
        6: dict(notes=['Threat: potential harm. Vulnerability: weakness. Attack: an attempt to exploit a vulnerability. Risk: threat × vulnerability × impact.']),
        8: dict(notes=['Threat actors: script kiddies, hacktivists, organized crime, nation states, insiders, cyber terrorists.']),
        10: dict(notes=['Vulnerabilities come from misconfiguration, design flaws, unpatched software, weak policies and human error.']),
        22: dict(notes=['Goal of network defense: protect information, resources and services from unauthorized access, misuse and disruption.']),
        23: dict(notes=['Information Assurance principles: confidentiality, integrity, availability, authentication, non-repudiation.'],
                 exam=[mcq('Proving a sender cannot deny having sent a message is:', ['Non-repudiation', 'Confidentiality', 'Availability', 'Authorization'], 0, '')], weight=3),
        27: dict(notes=['Defense approaches: preventive, reactive, retrospective, proactive.'],
                 exam=[mcq('Analysing past incidents to find what went wrong is which approach?', ['Retrospective', 'Preventive', 'Reactive', 'Proactive'], 0, '')], weight=2),
        28: dict(notes=['Three control families: administrative (policies, training), physical (locks, guards), technical (firewalls, encryption, access control).']),
        29: dict(notes=['Regulatory frameworks: PCI DSS (cards), HIPAA (health), SOX (finance), GDPR (EU personal data), ISO 27001.'],
                 exam=[mcq('Which standard governs organizations that process payment cards?', ['PCI DSS', 'HIPAA', 'SOX', 'GDPR'], 0, '')], weight=3),
        32: dict(notes=['ISO/IEC 27001: requirements for an Information Security Management System (ISMS); 27002: the controls.']),
        33: dict(notes=['Security policy: a document stating how the organization protects its assets; sets rules and responsibilities.']),
        36: dict(notes=['Policy types by strictness: promiscuous (no restrictions), permissive (block known-bad), prudent (block most, allow needed), paranoid (block everything).'],
                 exam=[mcq('A policy that allows everything except known dangerous services is:', ['Permissive', 'Promiscuous', 'Prudent', 'Paranoid'], 0, '')], weight=3),
        38: dict(notes=['Password policy: length, complexity, history, expiry, lockout.']),
        40: dict(notes=['Awareness training reduces social engineering and policy violations: people are the weakest link.']),
    }


class iam:
    AUTO_SLIDES = True
    DECK = deck('d02', 'Identification, Authentication and Authorization', 'Chapter 2',
                'Access-control terminology and principles, the DAC, MAC, RBAC and rule-based models, identity and access '
                'management, the types of authentication (password, two-factor, biometrics, smart cards, SSO), '
                'authorization and accounting.')
    ANN = {
        4: dict(notes=['Access control: who (subject) can do what (operation) to which resource (object).']),
        5: dict(notes=['Identification (claim who you are) → Authentication (prove it) → Authorization (what you may do) → Accounting (log what you did).'],
                tips=[trick('I-A-A-A: Identify, Authenticate, Authorize, Account.')],
                exam=[mcq('Entering a username is:', ['Identification', 'Authentication', 'Authorization', 'Accounting'], 0, ''),
                      mcq('Deciding which files a logged-in user may open is:', ['Authorization', 'Authentication', 'Identification', 'Accounting'], 0, '')], weight=3),
        6: dict(notes=['Principles: least privilege, separation of duties, need to know.'],
                exam=[mcq('Giving users only the access they need for their job is:', ['Least privilege', 'Separation of duties', 'Defense in depth', 'Need for speed'], 0, '')], weight=3),
        7: dict(notes=['DAC: the owner decides access. MAC: the system decides by labels/clearances (military). RBAC: by job role. Rule-based: by rules (e.g. time of day).'],
                exam=[mcq('Access decided by security labels and clearance levels is:', ['MAC', 'DAC', 'RBAC', 'Rule-based'], 0, ''),
                      mcq('A file owner granting a colleague read access is:', ['DAC', 'MAC', 'RBAC', 'Rule-based'], 0, '')], weight=3),
        19: dict(notes=['IAM: managing digital identities and their access (provisioning, authentication, authorization, de-provisioning).']),
        23: dict(notes=['Factors: something you KNOW (password), HAVE (token, smart card), ARE (biometric). Two-factor = two DIFFERENT categories.'],
                 tips=[trap('A password + a PIN is still ONE factor (both are something you know).')],
                 exam=[mcq('Which is two-factor authentication?', ['Smart card + PIN', 'Password + security question', 'Password + PIN', 'Two passwords'], 0, '')], weight=3),
        25: dict(notes=['Biometrics: fingerprint, face, iris, retina, voice, vein. Errors: false acceptance (FAR) and false rejection (FRR); CER is where they are equal.'],
                 exam=[mcq('A biometric system letting in an unauthorized person is a:', ['False acceptance', 'False rejection', 'True positive', 'Crossover error'], 0, '')], weight=3),
        27: dict(notes=['Single sign-on (SSO): authenticate once to access many systems.']),
    }


class symmetric:
    AUTO_SLIDES = True
    DECK = deck('d03', 'Cryptography Basics: DES and AES', 'Chapter 3',
                'Cryptography and encryption, symmetric vs. asymmetric encryption, government access to keys, ciphers '
                '(block and stream), DES and its Feistel structure, and AES (Rijndael): key expansion and the four '
                'round transformations.')
    ANN = {
        4: dict(notes=['Cryptography protects confidentiality, integrity, authentication and non-repudiation.']),
        6: dict(notes=['Symmetric: ONE shared secret key for encryption and decryption. Fast; the problem is key distribution.'],
                exam=[mcq('How many keys do n users need for pairwise symmetric encryption?', ['n(n − 1)/2', 'n', '2n', 'n²'], 0, '')], weight=3),
        7: dict(notes=['Asymmetric: a public key and a private key. Slower; solves key distribution and enables digital signatures.']),
        10: dict(notes=['Block ciphers encrypt fixed-size blocks (DES 64-bit, AES 128-bit); stream ciphers encrypt bit by bit (RC4).'],
                 exam=[mcq('AES encrypts blocks of:', ['128 bits', '64 bits', '56 bits', '256 bits only'], 0, 'Keys may be 128, 192 or 256 bits.')], weight=3),
        13: dict(notes=['DES: 64-bit blocks, 56-bit effective key, 16 Feistel rounds. Broken by brute force; 3DES applies it three times.'],
                 exam=[mcq('DES’s effective key length is:', ['56 bits', '64 bits', '128 bits', '168 bits'], 0, '')], weight=3),
        20: dict(notes=['AES (Rijndael) replaced DES: 128-bit block; 128/192/256-bit keys with 10/12/14 rounds.'],
                 exam=[mcq('AES-256 uses how many rounds?', ['14', '10', '12', '16'], 0, '')], weight=3),
        26: dict(notes=['Key expansion turns the cipher key into a round key for each round.']),
        28: dict(notes=['Each round: SubBytes (S-box substitution), ShiftRows (permutation), MixColumns (mixing), AddRoundKey (XOR with the round key). The last round skips MixColumns.'],
                 tips=[trick('Sub, Shift, Mix, Add.')],
                 exam=[mcq('Which AES step is omitted in the final round?', ['MixColumns', 'SubBytes', 'ShiftRows', 'AddRoundKey'], 0, '')], weight=3),
        37: dict(notes=['AES is not a Feistel cipher: every round processes the whole block.']),
    }


class rsa:
    AUTO_SLIDES = True
    DECK = deck('d04', 'Public-Key Cryptography and RSA', 'Chapter 4',
                'Why public-key cryptography, how it gives confidentiality and authentication, its requirements and '
                'applications, RSA key setup, encryption and decryption with a worked example, fast exponentiation, '
                'and the security of RSA (factoring, timing and chosen-ciphertext attacks).')
    ANN = {
        6: dict(notes=['Public-key: encrypt with the receiver’s PUBLIC key for confidentiality; sign with your PRIVATE key for authentication.'],
                tips=[trap('Confidentiality: encrypt with the RECEIVER’s public key. Signature: encrypt (sign) with the SENDER’s private key.')],
                exam=[mcq('To send Bob a confidential message, Alice encrypts with:', ['Bob’s public key', 'Alice’s private key', 'Bob’s private key', 'Alice’s public key'], 0, ''),
                      mcq('A digital signature is created with:', ['The sender’s private key', 'The sender’s public key', 'The receiver’s public key', 'A shared secret key'], 0, '')], weight=3),
        12: dict(notes=['Applications: encryption/decryption, digital signatures, key exchange.']),
        16: dict(notes=['RSA (Rivest–Shamir–Adleman): security rests on the difficulty of factoring large n = pq.']),
        19: dict(notes=['Key setup: pick primes p, q; n = pq; φ(n) = (p−1)(q−1); choose e with gcd(e, φ) = 1; d = e⁻¹ mod φ. Public (e, n), private (d, n).'], weight=3),
        21: dict(notes=['Example: p = 17, q = 11 → n = 187, φ = 160, e = 7, d = 23 (7·23 = 161 ≡ 1 mod 160).'],
                 exam=[short('p = 5, q = 11, e = 3. Find n, φ(n) and d.', 'n = 55, φ = 4·10 = 40. d = 3⁻¹ mod 40 = 27 (3·27 = 81 = 2·40 + 1).')], weight=3),
        22: dict(notes=['Encrypt C = Mᵉ mod n; decrypt M = Cᵈ mod n. With the example, M = 88 → C = 88⁷ mod 187 = 11.'],
                 exam=[mcq('In RSA, decryption computes:', ['M = Cᵈ mod n', 'M = Cᵉ mod n', 'M = C·d mod n', 'M = Cᵈ mod φ(n)'], 0, '')], weight=3),
        23: dict(notes=['Square-and-multiply makes huge exponents fast.']),
        30: dict(notes=['Attacks: brute force on d, factoring n (keys ≥ 2048 bits), timing attacks (constant-time code, blinding), chosen-ciphertext attacks (OAEP padding).']),
    }


class ecc:
    AUTO_SLIDES = True
    DECK = deck('d05', 'Elliptic Curve Cryptography', 'Chapter 5',
                'Elliptic curves and their properties, trapdoor functions, groups and point addition, finite fields, '
                'scalar multiplication and cyclic subgroups, the elliptic-curve discrete logarithm problem, ECC '
                'encryption, ECDH key exchange, and why ECC gives the same security with smaller keys.')
    ANN = {
        2: dict(notes=['Elliptic curve: y² = x³ + ax + b (with 4a³ + 27b² ≠ 0). Symmetric about the x-axis.']),
        5: dict(notes=['Trapdoor function: easy one way, hard to reverse without secret information.']),
        9: dict(notes=['Point addition: the line through P and Q meets the curve at a third point; reflect it to get P + Q. The inverse of (x, y) is (x, −y).']),
        12: dict(notes=['Scalar multiplication nP = P + P + … + P (n times), computed fast with double-and-add.']),
        18: dict(notes=['ECDLP: given P and Q = kP, finding k is infeasible. That is ECC’s hard problem.'],
                 exam=[mcq('ECC’s security relies on the difficulty of:', ['The elliptic-curve discrete logarithm problem', 'Factoring large integers', 'Brute-forcing AES', 'Hash collisions'], 0, '')], weight=3),
        27: dict(notes=['ECDH: Alice sends aG, Bob sends bG; both compute the shared point abG.'], seen=[see('d08', 6, 'classic Diffie–Hellman')]),
        29: dict(notes=['A 256-bit ECC key ≈ 3072-bit RSA security: smaller keys, faster, less power and bandwidth (good for mobile and IoT).'],
                 exam=[mcq('The main advantage of ECC over RSA is:', ['Equal security with much smaller keys', 'It needs no private key', 'It is symmetric', 'It cannot be used for signatures'], 0, '')], weight=3),
        31: dict(notes=['Applications: TLS key exchange, ECDSA signatures, Bitcoin, mobile devices.']),
    }


class rc4_modes:
    AUTO_SLIDES = True
    DECK = deck('d06', 'PRNGs, RC4 and Block-Cipher Modes of Operation', 'Chapter 6',
                'Random vs. pseudorandom numbers, PRNGs, stream ciphers and RC4 (key schedule, encryption, security), '
                'then the modes of operation: ECB, CBC, CFB, OFB and CTR with their advantages and limitations.')
    ANN = {
        5: dict(notes=['PRNG: a deterministic algorithm that produces random-looking numbers from a seed.']),
        8: dict(notes=['Stream cipher: keystream XOR plaintext. Never reuse a keystream (same key + IV).'],
                exam=[tf('Reusing the same keystream for two messages is safe if the messages differ.', False, 'C1 ⊕ C2 = P1 ⊕ P2 leaks information.')], weight=3),
        10: dict(notes=['RC4: variable-length key, byte-oriented stream cipher, simple and fast. Used in WEP and old TLS; now considered broken.']),
        11: dict(notes=['RC4 key schedule (KSA) permutes the 256-byte state S using the key; the PRGA then outputs keystream bytes.']),
        23: dict(notes=['ECB: each block encrypted independently. Identical plaintext blocks → identical ciphertext blocks (patterns leak).'],
                 tips=[trap('ECB leaks patterns (the "ECB penguin"); never use it for more than one block.')],
                 exam=[mcq('Which mode produces identical ciphertext for identical plaintext blocks?', ['ECB', 'CBC', 'CTR', 'OFB'], 0, '')], weight=3),
        26: dict(notes=['CBC: each plaintext block is XORed with the previous ciphertext block (first with an IV) before encryption. Sequential encryption; an error affects two blocks.'],
                 exam=[mcq('In CBC, the first plaintext block is XORed with:', ['The IV', 'The key', 'The last ciphertext block', 'Zero'], 0, '')], weight=3),
        31: dict(notes=['CFB: turns a block cipher into a self-synchronizing stream cipher.']),
        34: dict(notes=['OFB: keystream from repeatedly encrypting the IV; bit errors don’t propagate.']),
        37: dict(notes=['CTR: encrypt a counter for each block and XOR. Parallel, random access, needs a unique nonce per message.'],
                 exam=[mcq('Which mode allows parallel encryption and random access to blocks?', ['CTR', 'CBC', 'CFB', 'OFB'], 0, '')], weight=3),
    }


class hashing:
    AUTO_SLIDES = True
    DECK = deck('d07', 'MACs and Hash Functions', 'Chapter 7',
                'Message authentication, MACs and their requirements, HMAC, one-way hash functions and their '
                'properties (preimage, second-preimage and collision resistance), attacks and the birthday paradox, '
                'UNIX password storage with salt, dictionary attacks, MD5 and the SHA family.')
    ANN = {
        5: dict(notes=['MAC: a short tag computed from the message AND a shared secret key; proves integrity and origin.'],
                exam=[mcq('A MAC provides:', ['Integrity and authentication', 'Confidentiality only', 'Non-repudiation', 'Key exchange'], 0, 'Both parties share the key, so it can’t give non-repudiation.')], weight=3),
        11: dict(notes=['HMAC = H((K ⊕ opad) ‖ H((K ⊕ ipad) ‖ M)): a MAC built from any hash function.']),
        13: dict(notes=['Hash function: any-length input → fixed-length digest; no key.']),
        17: dict(notes=['Properties: preimage resistance (one-way), second-preimage resistance (weak collision), collision resistance (strong collision).'],
                 exam=[mcq('Finding ANY two messages with the same hash breaks:', ['Collision resistance', 'Preimage resistance', 'Second-preimage resistance', 'Confidentiality'], 0, '')], weight=3),
        22: dict(notes=['Birthday attack: collisions take about 2^(n/2) tries for an n-bit hash, so 128-bit hashes give only ~64-bit collision security.'],
                 exam=[mcq('For a 160-bit hash, a birthday attack needs about:', ['2⁸⁰ tries', '2¹⁶⁰ tries', '2⁴⁰ tries', '160 tries'], 0, '')], weight=3),
        26: dict(notes=['Salt: a random value stored with each password hash; identical passwords give different hashes and precomputed tables fail.'],
                 seen=[see('d07', 31, 'dictionary attacks')]),
        31: dict(notes=['Dictionary attack: hash common words and compare. Salt + slow hashes make it expensive.']),
        35: dict(notes=['MD5: 128-bit digest, 512-bit blocks. Broken (collisions); don’t use for security.']),
        44: dict(notes=['SHA-1: 160-bit (broken). SHA-2: SHA-224/256/384/512. SHA-512 processes 1024-bit blocks in 80 rounds.'],
                 exam=[mcq('The digest size of SHA-256 is:', ['256 bits', '160 bits', '128 bits', '512 bits'], 0, '')], weight=3),
    }


class diffie_hellman:
    AUTO_SLIDES = True
    DECK = deck('d08', 'Diffie–Hellman Key Exchange', 'Chapter 8',
                'Primitive roots, Diffie–Hellman setup and the key exchange with a worked example, key-exchange '
                'protocols, and the man-in-the-middle attack on unauthenticated Diffie–Hellman.')
    ANN = {
        2: dict(notes=['Diffie–Hellman lets two parties agree on a shared secret over an insecure channel. It exchanges a KEY; it doesn’t encrypt messages.'],
                exam=[mcq('Diffie–Hellman is used for:', ['Key exchange', 'Encrypting messages directly', 'Digital signatures', 'Hashing'], 0, '')], weight=3),
        4: dict(notes=['A primitive root g of prime q: its powers g¹ … g^(q−1) mod q produce every number 1 … q−1.']),
        6: dict(notes=['Alice: private a, sends A = gᵃ mod q. Bob: private b, sends B = gᵇ mod q. Shared K = Bᵃ = Aᵇ = gᵃᵇ mod q.'],
                exam=[short('q = 23, g = 5, a = 6, b = 15. Find A, B and the shared key.', 'A = 5⁶ mod 23 = 8. B = 5¹⁵ mod 23 = 19. K = 19⁶ mod 23 = 8¹⁵ mod 23 = 2.')], weight=3),
        8: dict(notes=['Security rests on the discrete logarithm problem: from gᵃ mod q it is infeasible to find a.']),
        11: dict(notes=['MITM: Darth swaps in his own values and shares one key with Alice and another with Bob. Plain DH has no authentication; fix with signatures or certificates.'],
                 tips=[trap('Diffie–Hellman alone is vulnerable to man-in-the-middle because the public values are not authenticated.')],
                 exam=[mcq('Unauthenticated Diffie–Hellman is vulnerable to:', ['Man-in-the-middle attacks', 'Birthday attacks', 'Padding-oracle attacks', 'Rainbow tables'], 0, '')], weight=3),
    }


class key_management:
    AUTO_SLIDES = True
    DECK = deck('d09', 'Key Distribution and Management', 'Chapter 9',
                'Key management and its protocols, key hierarchies (master and session keys), symmetric key distribution '
                'with a KDC and its MITM risk, hybrid schemes, distributing public keys (announcement, directory, authority, '
                'certificates), X.509 certificates and CA hierarchies, revocation (CRL, OCSP) and PKI.')
    ANN = {
        9: dict(notes=['Key hierarchy: long-term master keys (shared with the KDC) protect short-lived session keys.'],
                exam=[mcq('Keys used for a single communication session and then discarded are:', ['Session keys', 'Master keys', 'Private keys', 'Root keys'], 0, '')], weight=3),
        11: dict(notes=['KDC (Key Distribution Center): a trusted third party that creates session keys and sends them encrypted with each user’s master key.']),
        14: dict(notes=['Merkle’s simple scheme (A sends a public key, B returns a secret key encrypted with it) is open to man-in-the-middle.']),
        18: dict(notes=['Distributing public keys: public announcement (forgeable), public directory, public-key authority, certificates (best).']),
        23: dict(notes=['Certificate: binds an identity to a public key, signed by a Certificate Authority (CA).'],
                 exam=[mcq('A digital certificate binds:', ['An identity to a public key', 'A password to a user', 'A session key to a server', 'A hash to a file'], 0, '')], weight=3),
        27: dict(notes=['X.509 fields: version, serial number, signature algorithm, issuer, validity period, subject, subject’s public key, extensions, CA signature.']),
        30: dict(notes=['CA hierarchy: root CA → intermediate CAs → end entities; trust flows down a certificate chain.']),
        32: dict(notes=['Revocation: compromised key, changed affiliation, superseded. Checked with CRLs or OCSP.']),
        35: dict(notes=['PKI: the hardware, software, people, policies and procedures to create, manage, distribute, use, store and revoke certificates. Parts: CA, RA, repository, end entities.'],
                 exam=[mcq('The PKI component that verifies a requester’s identity before the CA issues a certificate is the:', ['Registration Authority (RA)', 'CRL', 'OCSP responder', 'KDC'], 0, '')], weight=3),
        43: dict(notes=['CRL: a periodically published, signed list of revoked serial numbers.']),
        44: dict(notes=['OCSP: ask a responder in real time about ONE certificate (good / revoked / unknown).'],
                 exam=[mcq('Which checks a certificate’s revocation status in real time?', ['OCSP', 'CRL', 'X.509 v1', 'RA'], 0, '')], weight=3),
    }


class protocols:
    AUTO_SLIDES = True
    DECK = deck('d10', 'Network Security Protocols', 'Chapter 10',
                'RADIUS and TACACS+ for AAA, Kerberos, email security with PGP and S/MIME, HTTPS, TLS and SSL, and '
                'IPsec.')
    ANN = {
        8: dict(notes=['RADIUS: centralized AAA over UDP (1812/1813); encrypts only the password.']),
        11: dict(notes=['TACACS+ (Cisco): TCP 49, encrypts the whole body, separates authentication, authorization and accounting.'],
                 exam=[mcq('Compared with RADIUS, TACACS+:', ['Uses TCP and encrypts the entire payload', 'Uses UDP and encrypts only the password', 'Has no accounting', 'Is used only for wireless'], 0, '')], weight=3),
        14: dict(notes=['Kerberos: ticket-based authentication with a KDC (AS + TGS); uses symmetric keys and timestamps; needs synchronized clocks.'],
                 exam=[mcq('Kerberos issues users a:', ['Ticket-granting ticket', 'Digital certificate', 'One-time password', 'Session cookie'], 0, '')], weight=3),
        15: dict(notes=['PGP: email/file confidentiality, integrity, authentication; web of trust.']),
        17: dict(notes=['S/MIME: secure email using X.509 certificates (hierarchical CA trust).'],
                 tips=[trick('PGP = web of trust; S/MIME = certificate authorities.')], weight=3),
        21: dict(notes=['HTTPS = HTTP over TLS (port 443).']),
        24: dict(notes=['TLS (successor to SSL): handshake negotiates ciphers, authenticates the server with a certificate, and derives session keys.'],
                 exam=[tf('SSL is still considered secure and preferred over TLS.', False, 'SSL is deprecated; use TLS 1.2/1.3.')], weight=3),
        27: dict(notes=['IPsec: network-layer security. AH = integrity/authentication (no encryption); ESP = encryption (+ integrity). Transport mode protects the payload; tunnel mode protects the whole packet.'],
                 exam=[mcq('Which IPsec protocol provides encryption?', ['ESP', 'AH', 'IKE only', 'GRE'], 0, ''),
                       mcq('IPsec mode that encapsulates the entire original IP packet (used for site-to-site VPNs):', ['Tunnel mode', 'Transport mode', 'Promiscuous mode', 'Monitor mode'], 0, '')], weight=3),
    }


class firewalls:
    AUTO_SLIDES = True
    DECK = deck('d11', 'Network Segmentation and Firewalls', 'Chapter 11',
                'Network segmentation and its types, bastion hosts and where to place them, the DMZ, then firewalls: '
                'hardware, software and host-based types, packet filtering, circuit-level and application-level '
                'gateways, stateful inspection, proxies, NAT, NGFWs, capabilities, limitations and secure deployment.')
    ANN = {
        4: dict(notes=['Segmentation splits the network into zones so a breach in one doesn’t expose everything (physical, logical/VLAN, network virtualization).']),
        8: dict(notes=['Bastion host: a hardened system exposed to attack, e.g. in the DMZ, running only essential services.']),
        16: dict(notes=['DMZ: a buffer network between the internet and the internal LAN that hosts public servers (web, mail, DNS).'],
                 exam=[mcq('A company’s public web server should be placed in the:', ['DMZ', 'Internal LAN', 'Database segment', 'Management VLAN'], 0, '')], weight=3),
        20: dict(notes=['Firewall: enforces a policy on traffic between networks; default-deny is best practice.']),
        26: dict(notes=['Packet filter (layer 3/4): checks IPs, ports, protocol of each packet independently. Fast but stateless.']),
        27: dict(notes=['Circuit-level gateway (session layer): validates the TCP handshake, not the content.']),
        28: dict(notes=['Application-level gateway (proxy, layer 7): inspects content for specific applications.']),
        29: dict(notes=['Stateful multilayer inspection: tracks connection state and examines multiple layers.'],
                 exam=[mcq('A firewall that tracks the state of connections in a table is a:', ['Stateful inspection firewall', 'Packet filter', 'Circuit-level gateway', 'Bastion host'], 0, ''),
                       mcq('Which firewall type can inspect HTTP content?', ['Application-level gateway', 'Packet filter', 'Circuit-level gateway', 'NAT'], 0, '')], weight=3),
        31: dict(notes=['NAT hides internal addresses behind one public IP.']),
        33: dict(notes=['NGFW: stateful firewall + deep packet inspection, application awareness, IPS, user identity.']),
        35: dict(notes=['Limitations: can’t stop insider attacks, malware in allowed traffic, social engineering, encrypted payloads it can’t inspect.'],
                 exam=[tf('A firewall protects against attacks from inside the network.', False, 'Traffic that never crosses it isn’t filtered.')], weight=3),
    }


class ids_ips:
    AUTO_SLIDES = True
    DECK = deck('d12', 'Intrusion Detection and Prevention Systems', 'Chapter 12',
                'How an IDS works and what it can and can’t do, indications of intrusion, IDS classifications '
                '(signature vs. anomaly, active vs. passive, network vs. host), IDS components, deployment, alert types '
                '(true/false positives and negatives), choosing an IDS/IPS, and Snort.')
    ANN = {
        2: dict(notes=['IDS detects and alerts (passive, out of band); IPS sits inline and can block.'],
                exam=[mcq('The key difference between an IDS and an IPS is that an IPS:', ['Sits inline and can block traffic', 'Only logs traffic', 'Is always host-based', 'Uses only signatures'], 0, '')], weight=3),
        11: dict(notes=['Signature (misuse) detection: matches known attack patterns. Low false positives; misses new (zero-day) attacks.']),
        13: dict(notes=['Anomaly detection: learns normal behaviour and flags deviations. Can catch new attacks; more false positives.'],
                 tips=[trick('Signature = known bad. Anomaly = not normal.')],
                 exam=[mcq('Which IDS approach can detect zero-day attacks?', ['Anomaly-based', 'Signature-based', 'Both equally', 'Neither'], 0, '')], weight=3),
        17: dict(notes=['NIDS monitors network traffic (sensors on segments); HIDS monitors one host (logs, files, system calls).'],
                 exam=[mcq('An IDS that monitors a server’s system files and logs is:', ['Host-based (HIDS)', 'Network-based (NIDS)', 'A packet filter', 'A honeypot'], 0, '')], weight=3),
        21: dict(notes=['Components: network sensors, command console, alert system, response system, attack-signature database.']),
        36: dict(notes=['True positive: real attack, alert. False positive: no attack, alert. False negative: real attack, NO alert (the most dangerous). True negative: no attack, no alert.'],
                 exam=[mcq('An IDS missing a real attack is a:', ['False negative', 'False positive', 'True negative', 'True positive'], 0, '')], weight=3),
        39: dict(notes=['Snort: open-source NIDS/IPS; rules: action protocol src_ip src_port -> dst_ip dst_port (options).']),
    }


class vpn:
    AUTO_SLIDES = True
    DECK = deck('d13', 'VPN Fundamentals', 'Chapter 13',
                'How a VPN works and why to use one, VPN components and concentrators, remote-access vs. site-to-site '
                'VPNs, hardware vs. software VPNs, encapsulation, encryption and authentication, VPN technologies and '
                'topologies (hub-and-spoke, point-to-point, full mesh, star), security risks, and the AAA/RADIUS setup.')
    ANN = {
        3: dict(notes=['A VPN builds an encrypted tunnel over a public network so remote users or sites act as if on the private LAN.']),
        5: dict(notes=['Components: VPN client, network access server (NAS), tunnel terminating device / concentrator, protocols.']),
        9: dict(notes=['Remote-access (client-to-site): one user to the company network.']),
        10: dict(notes=['Site-to-site: connects whole networks (branch to HQ), gateway to gateway.'],
                 exam=[mcq('Connecting a branch office network to headquarters is a:', ['Site-to-site VPN', 'Remote-access VPN', 'SSL portal only', 'Proxy'], 0, '')], weight=3),
        16: dict(notes=['Core functions: encapsulation, encryption, authentication (plus integrity).']),
        19: dict(notes=['Technologies: IPsec, SSL/TLS VPNs, PPTP (obsolete), L2TP (with IPsec).'],
                 exam=[mcq('Which VPN protocol is considered insecure today?', ['PPTP', 'IPsec', 'TLS', 'L2TP/IPsec'], 0, '')], weight=3),
        21: dict(notes=['Topologies: hub-and-spoke (sites via a central hub), point-to-point, full mesh (every site to every site), star.'],
                 exam=[mcq('n sites in a full-mesh VPN need how many tunnels?', ['n(n − 1)/2', 'n − 1', 'n', '2n'], 0, '')], weight=3),
        26: dict(notes=['Risks: weak authentication, compromised endpoints, split tunneling, outdated protocols.']),
    }


class honeypots:
    AUTO_SLIDES = True
    DECK = deck('d14', 'Honeypots and Proxy Servers', 'Chapter 14',
                'Honeypots and their types (low, medium and high interaction, production vs. research), honeypot tools, '
                'then proxy servers: benefits, how they work, proxy vs. packet filter, transparent, non-transparent, '
                'SOCKS, anonymous and reverse proxies, configuration and limitations.')
    ANN = {
        2: dict(notes=['Honeypot: a decoy system with no production value; any interaction with it is suspicious. Used to detect and study attackers.'],
                exam=[mcq('The purpose of a honeypot is to:', ['Lure attackers so they can be detected and studied', 'Speed up the network', 'Encrypt traffic', 'Replace the firewall'], 0, '')], weight=3),
        3: dict(notes=['Low-interaction: emulates a few services (safe, limited data). High-interaction: real OS and services (rich data, more risk). Production vs. research honeypots.'],
                exam=[mcq('Which honeypot gives the most information but carries the most risk?', ['High-interaction', 'Low-interaction', 'Medium-interaction', 'Passive'], 0, '')], weight=3),
        8: dict(notes=['Proxy server: an intermediary that makes requests on behalf of clients (hides them, filters content, caches).']),
        12: dict(notes=['Proxy vs. packet filter: a proxy inspects application data; a packet filter only headers.']),
        14: dict(notes=['Transparent proxy: clients don’t know it’s there (no configuration).']),
        16: dict(notes=['SOCKS proxy: generic, works for any TCP/UDP application.']),
        17: dict(notes=['Anonymous proxy hides the client’s IP from the server.']),
        18: dict(notes=['Reverse proxy: sits in front of SERVERS (load balancing, TLS termination, protection).'],
                 tips=[trap('Forward proxy protects/represents clients; reverse proxy protects/represents servers.')],
                 exam=[mcq('A proxy that receives requests on behalf of a company’s web servers is a:', ['Reverse proxy', 'Transparent proxy', 'Anonymous proxy', 'SOCKS proxy'], 0, '')], weight=3),
        24: dict(notes=['Squid: a common caching proxy server.']),
    }


class siem:
    AUTO_SLIDES = True
    DECK = deck('d15', 'SIEM, UBA and Anti-Malware', 'Chapter 15',
                'Security Information and Event Management (architecture, functions, products), User Behavior Analytics, '
                'and anti-Trojan and antivirus software.')
    ANN = {
        4: dict(notes=['SIEM: collects and correlates logs and events from many sources in real time; alerts, dashboards, compliance reports.'],
                exam=[mcq('A system that aggregates and correlates logs from many devices to raise alerts is a:', ['SIEM', 'Proxy', 'VPN concentrator', 'Honeypot'], 0, '')], weight=3),
        6: dict(notes=['Functions: log collection, aggregation, normalization, correlation, alerting, retention, forensics, reporting.']),
        9: dict(notes=['UBA/UEBA: builds a baseline of normal user behaviour and flags anomalies (insider threats, compromised accounts).'],
                 exam=[mcq('An employee suddenly downloading gigabytes at 3 a.m. would most likely be flagged by:', ['UBA', 'A packet filter', 'NAT', 'A CRL'], 0, '')], weight=3),
        14: dict(notes=['Antivirus: signature, heuristic and behaviour-based detection; keep definitions updated.']),
    }


class data_security:
    AUTO_SLIDES = True
    DECK = deck('d16', 'Data Security', 'Chapter 16',
                'Business-critical data and data at rest vs. in transit vs. in use, disk, file and removable-media '
                'encryption, backup strategy and media, RAID levels, SAN and NAS, backup types (full, incremental, '
                'differential), retention, recovery, and data loss prevention.')
    ANN = {
        7: dict(notes=['Data at rest (stored), in transit (moving over a network), in use (being processed): each needs its own protection.'],
                exam=[mcq('An encrypted laptop hard drive protects data:', ['At rest', 'In transit', 'In use', 'In memory only'], 0, '')], weight=3),
        11: dict(notes=['Full-disk encryption (e.g. BitLocker) protects everything on a lost or stolen device.']),
        19: dict(notes=['Backup strategy: what, how often, which media, where (offsite/cloud), how long, test restores. 3-2-1 rule: 3 copies, 2 media, 1 offsite.']),
        22: dict(notes=['RAID combines disks for performance and/or redundancy (not a backup!).'], tips=[trap('RAID protects against disk failure, not deletion or ransomware: it is not a backup.')]),
        27: dict(notes=['RAID 0: striping, no redundancy (fast, any disk failure loses all).']),
        28: dict(notes=['RAID 1: mirroring (two copies; 50% capacity).']),
        30: dict(notes=['RAID 5: block striping with distributed parity; survives one disk failure; needs ≥ 3 disks.'],
                 exam=[mcq('Which RAID level offers striping with distributed parity and survives one disk failure?', ['RAID 5', 'RAID 0', 'RAID 1', 'RAID 3'], 0, ''),
                       mcq('RAID 0 provides:', ['Performance with no redundancy', 'Mirroring', 'Parity', 'Hot spares'], 0, '')], weight=3),
        31: dict(notes=['RAID 10: mirrored pairs that are then striped (fast and redundant; ≥ 4 disks).']),
        33: dict(notes=['SAN: dedicated block-level storage network. NAS: file-level storage on the LAN.']),
        38: dict(notes=['Full: everything (slow backup, fast restore). Incremental: changes since the LAST backup (fast backup, slow restore: full + every incremental). Differential: changes since the last FULL (restore = full + latest differential).'],
                 exam=[mcq('Restoring from full + differential backups needs:', ['The last full and the latest differential', 'The last full and every differential', 'Only the latest differential', 'Every incremental'], 0, ''),
                       mcq('Which backup type is fastest to perform each day?', ['Incremental', 'Full', 'Differential', 'Mirror'], 0, '')], weight=3),
        45: dict(notes=['DLP: tools and policies that detect and block sensitive data leaving the organization (network, endpoint, storage).'],
                 exam=[mcq('Software that blocks an employee from emailing a file of credit-card numbers outside is:', ['DLP', 'IDS', 'RAID', 'NAT'], 0, '')], weight=3),
    }


DECKS_HERE = [fundamentals, iam, symmetric, rsa, ecc, rc4_modes, hashing, diffie_hellman, key_management, protocols,
              firewalls, ids_ips, vpn, honeypots, siem, data_security]
