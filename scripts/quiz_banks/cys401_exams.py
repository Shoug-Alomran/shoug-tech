#!/usr/bin/env python3
"""Question bank for the three CYS401 past papers rendered as interactive exams.

Transcribed from the scanned papers Shoug supplied:
  * Quiz 1, semester 222 (Dr. Rabia Latif, 29 January 2023)
  * Final exam 221, version A (Dr. Suliman Mohamed Fati, 21 December 2022)
  * Final exam 221, version B (Dr. Rabia Latif, 21 December 2022)

Question shapes
---------------
mcq     options + index of the keyed answer; `wrong` explains each distractor
fill    free text matched against `accept` (lowercased substring match)
numeric value + tolerance
match   one dropdown per item, all sharing `options`
short   free text scored by concept groups; every group is a list of synonyms

`why` is shown once an answer is checked, right or wrong.  Where the official
key is arithmetically wrong or ambiguous, the explanation says so rather than
teaching the error: `note` renders as a flagged caveat.
"""

QUIZ_222 = {
    "slug": "09-quiz-1-semester-222",
    "file": "quiz-1-semester-222.html",
    "title": "Quiz 1 (Semester 222)",
    "item": "ITEM_09",
    "meta": "Dr. Rabia Latif · 29 January 2023 · Sections 360, 362, 1398 · 5 marks",
    "intro": "The first CYS401 quiz of semester 222: defence in depth, security "
             "measures, an availability calculation and attacker classification.",
    "sections": [
        {
            "name": "Q1 · Choose the best option",
            "note": "0.25 marks each · 1 mark total",
            "questions": [
                {
                    "type": "mcq",
                    "q": "What is a characteristic of a layered defence-in-depth security approach?",
                    "options": [
                        "Three or more devices are used.",
                        "Routers are replaced with firewalls.",
                        "One safeguard failure does not affect the effectiveness of other safeguards.",
                        "When one device fails, another one takes over.",
                    ],
                    "correct": 2,
                    "why": "Defence in depth stacks independent controls so that the "
                           "attacker has to defeat each one separately. The point is "
                           "independence: one control failing must not weaken the rest.",
                    "wrong": {
                        0: "There is no device count that makes an approach layered. A single "
                           "device can host several independent controls, and three devices "
                           "enforcing the same rule are still one layer.",
                        1: "Swapping one control for another is not layering — it is replacement. "
                           "Layering would mean keeping the router's filtering and adding the firewall.",
                        3: "That describes redundancy or fail-over, which protects availability. "
                           "Defence in depth is about independent safeguards, not standby copies.",
                    },
                },
                {
                    "type": "fill",
                    "q": "In cybersecurity, ICT stands for ______.",
                    "accept": ["information communication technology",
                               "information and communication technology",
                               "information & communication technology"],
                    "answer": "Information and Communication Technology",
                    "why": "ICT is the umbrella term for the computing and networking "
                           "assets an organisation has to defend.",
                },
                {
                    "type": "mcq",
                    "q": "Which of the following is not a physical security measure to protect "
                         "against physical hacking?",
                    "options": [
                        "Create a phishing policy.",
                        "Updating the patches in the software you're working on at your office laptop.",
                        "Add a front desk and restrict unknown access to the back room.",
                        "Analyze how employees maintain their physical data and data storage "
                        "peripheral devices.",
                    ],
                    "correct": 1,
                    "why": "Patching is a technical control: it changes software on the machine "
                           "and does nothing to stop someone who physically walks up to it.",
                    "wrong": {
                        0: "A phishing policy is an administrative control rather than a physical "
                           "one, so this option is arguably also correct — see the note below.",
                        2: "A front desk and access restrictions are the textbook physical control: "
                           "they stop an intruder reaching the hardware.",
                        3: "Auditing how staff handle physical media and storage devices is a "
                           "physical-security practice.",
                    },
                    "note": "This question has two defensible answers. Neither patching (b) nor a "
                            "phishing policy (a) is a physical control. The marked paper treats the "
                            "technical control as the intended answer, so (b) is keyed here — but if "
                            "you picked (a) in the real exam you had a case to argue.",
                },
                {
                    "type": "mcq",
                    "q": "______ limits the execution of files or handling of data by specific "
                         "installed programs.",
                    "options": [
                        "Encryption / Decryption Programs",
                        "Anti-virus Programs",
                        "Application Firewall",
                        "Routers",
                    ],
                    "correct": 2,
                    "why": "An application firewall works at the application layer, so it can "
                           "allow or deny what a named program is permitted to execute or handle.",
                    "wrong": {
                        0: "Encryption protects confidentiality of data at rest or in transit. It "
                           "does not decide which program may run or touch a file.",
                        1: "Anti-virus detects and removes known malicious code. It reacts to "
                           "signatures and behaviour rather than enforcing per-application limits.",
                        3: "A router forwards packets between networks at layer 3 and has no view "
                           "of which application is handling the data.",
                    },
                },
            ],
        },
        {
            "name": "Q2 · Availability calculation",
            "note": "1 mark",
            "questions": [
                {
                    "type": "numeric",
                    "q": "Horizon Solutions hired an ethical hacker, Ms. Park, to find "
                         "vulnerabilities. She tests every week for 3 months starting June 2022. "
                         "Each round needs 45 minutes for the system, 1 hour 20 minutes for the "
                         "network, and 15 more minutes to recover the traces; the systems and "
                         "network are disconnected for that whole time. Calculate the total "
                         "availability as a percentage (1 decimal place).",
                    "answer": 98.6,
                    "tol": 0.4,
                    "unit": "%",
                    "why": "Downtime per test = 45 + 80 + 15 = <strong>140 minutes</strong>. "
                           "A week is 7 × 24 × 60 = <strong>10,080 minutes</strong>, so per week "
                           "MTTR = 140 and MTTF = 10,080 − 140 = 9,940. "
                           "Availability = MTTF ÷ (MTTF + MTTR) × 100 = 9,940 ÷ 10,080 × 100 = "
                           "<strong>98.6%</strong>. Running it over the whole quarter gives the "
                           "same figure: 13 weekly tests × 140 = 1,820 minutes of downtime out of "
                           "13 × 10,080 = 131,040 minutes.",
                    "note": "The marked paper reaches 99.9% from MTTF = 907,200, which is 90 weeks "
                            "of minutes rather than 90 days, and it lost half a mark. Work in one "
                            "consistent window — one week is the easiest.",
                },
            ],
        },
        {
            "name": "Q3 · Defence-in-depth layers",
            "note": "1.75 marks · match each control to the layer it belongs to",
            "questions": [
                {
                    "type": "match",
                    "q": "Place each pair of security controls at the defence-in-depth layer it "
                         "protects.",
                    "options": ["Data", "Application", "Host", "Internal Network",
                                "Perimeter", "Physical", "Policies and Procedures"],
                    "items": [
                        ["Encryption at rest and access control lists on the records themselves",
                         "Data",
                         "The innermost layer protects the information itself, so that a breach of "
                         "every outer layer still yields unreadable data."],
                        ["Input validation and secure coding of the software being used",
                         "Application",
                         "Application-layer controls live inside the program: they stop malformed "
                         "or malicious input being processed."],
                        ["Operating-system patching and host-based antivirus",
                         "Host",
                         "Host controls harden the individual machine — its OS, services and "
                         "local defences."],
                        ["Internal segmentation and auditing of traffic between departments",
                         "Internal Network",
                         "Once inside the perimeter, segmentation and monitoring limit how far an "
                         "intruder can move laterally."],
                        ["Border firewalls and screening routers",
                         "Perimeter",
                         "The perimeter is the boundary with the outside world, guarded by "
                         "firewalls, routers and gateways."],
                        ["Guards, locks and restricted server-room entry",
                         "Physical",
                         "Physical controls stop someone reaching the hardware at all."],
                        ["Security awareness training and a written acceptable-use policy",
                         "Policies and Procedures",
                         "The outermost layer is human and administrative: the rules people follow "
                         "and the training that makes them stick."],
                    ],
                },
            ],
        },
        {
            "name": "Q4 · Type of cyber attacker",
            "note": "0.25 each · 1.25 marks",
            "questions": [
                {
                    "type": "match",
                    "q": "Write the appropriate type of cyber attacker for each scenario.",
                    "options": ["Hacktivists", "Organized crime", "Script kiddies",
                                "State-based attackers", "Hackers"],
                    "items": [
                        ["In the recent Ukraine war, hackers targeted Russian government websites "
                         "and launched a DDoS attack to prevent user access. Most sites are down.",
                         "Hacktivists",
                         "The motive is political protest and the damage is disruption rather than "
                         "profit or espionage — that is hacktivism. A state-based actor would be "
                         "acting on government orders, typically quietly."],
                        ["The Carbanak and Cobalt malware attacks hit 100 financial firms in over "
                         "40 countries, plundering over $11 million per heist and costing the "
                         "banking sector more than a billion dollars.",
                         "Organized crime",
                         "Sustained, coordinated, financially motivated campaigns against banks "
                         "are the signature of organised criminal groups."],
                        ["These attackers lack knowledge and sophistication; their attacks often "
                         "exploit well-known vulnerabilities, and keeping systems up to date "
                         "defends against them.",
                         "Script kiddies",
                         "Low skill, borrowed tools and reliance on unpatched known flaws define "
                         "script kiddies."],
                        ["The U.S. National Security Agency recorded nearly every cell phone "
                         "conversation in the Bahamas without permission, along with similar "
                         "programs in Kenya, the Philippines, Mexico and Afghanistan.",
                         "State-based attackers",
                         "A national intelligence agency conducting mass surveillance is the "
                         "definition of a state-based (nation-state) actor."],
                        ["Attackers take advantage of vulnerabilities in plug-ins, web browsers "
                         "and apps to install malware on your device without your knowledge.",
                         "Hackers",
                         "No political, criminal-syndicate or state motive is given — this is the "
                         "generic skilled attacker exploiting technical vulnerabilities."],
                    ],
                },
            ],
        },
    ],
}

FINAL_221_A = {
    "slug": "10-final-exam-221-version-a",
    "file": "final-exam-221-version-a.html",
    "title": "Final Exam 221 (Version A)",
    "item": "ITEM_10",
    "meta": "Dr. Suliman Mohamed Fati · 21 December 2022 · 3 hours · 40 marks",
    "intro": "Version A of the 221 final: security pillars and attacks, cryptography, "
             "access-control models, and attack identification from scenarios.",
    "sections": [
        {
            "name": "Q1 Part 1 · Multiple choice",
            "note": "0.5 marks each",
            "questions": [
                {
                    "type": "mcq",
                    "q": "To achieve security we combine three key elements, the cybersecurity "
                         "pillars. All of the following are pillars except ______.",
                    "options": ["People", "Policies", "Technologies", "Data"],
                    "correct": 3,
                    "why": "The three pillars are people, policies (process) and technology. "
                           "Data is what those pillars protect, not one of them.",
                    "wrong": {
                        0: "People are a pillar — staff, training and human error sit at the "
                           "centre of most incidents.",
                        1: "Policies and processes are a pillar: they define what secure "
                           "behaviour means before any technology is chosen.",
                        2: "Technology is a pillar — the tools that enforce the policies.",
                    },
                },
                {
                    "type": "mcq",
                    "q": "______ is the attack that causes company assets to become unusable or "
                         "unavailable on a temporary or permanent basis.",
                    "options": ["Interruption", "Interception", "Modification", "Fabrication"],
                    "correct": 0,
                    "why": "Interruption attacks availability: the asset still exists but can no "
                           "longer be reached or used.",
                    "wrong": {
                        1: "Interception is an attack on confidentiality — the attacker reads the "
                           "data while it stays available to its owner.",
                        2: "Modification attacks integrity: the asset is altered, not made "
                           "unavailable.",
                        3: "Fabrication inserts counterfeit data or transactions; it also targets "
                           "integrity and authenticity.",
                    },
                },
                {
                    "type": "mcq",
                    "q": "______ is social-engineering-based malware that asks the victim to pay "
                         "in order to unlock or decrypt the system or the data.",
                    "options": ["Worm", "Virus", "Ransomware", "Adware"],
                    "correct": 2,
                    "why": "Ransomware encrypts or locks the victim's data and demands payment "
                           "for the key.",
                    "wrong": {
                        0: "A worm spreads itself across a network without user action and "
                           "without demanding payment.",
                        1: "A virus attaches to a host file and needs that file to be run; the "
                           "defining trait is infection, not extortion.",
                        3: "Adware displays unwanted advertising. It is a nuisance and a privacy "
                           "problem, but it does not hold data hostage.",
                    },
                },
                {
                    "type": "mcq",
                    "q": "In the governmental context, data should be classified rigidly into one "
                         "of the following classes except ______.",
                    "options": ["Top Secret", "Critical", "Secret", "Unclassified"],
                    "correct": 1,
                    "why": "Government classification runs Top Secret, Secret, Confidential, "
                           "Unclassified. 'Critical' belongs to the commercial scheme, not the "
                           "government one.",
                    "wrong": {
                        0: "Top Secret is the highest government classification.",
                        2: "Secret is a standard government level.",
                        3: "Unclassified is the lowest government level — still a defined class.",
                    },
                },
                {
                    "type": "mcq",
                    "q": "The ______ is an advanced version of the Caesar cipher in which the "
                         "alphabetic text is encrypted by matching the plaintext with ciphertext "
                         "based on a provided keyword.",
                    "options": ["Vigenère cipher", "Keyword Cipher", "One Time Pad", "Hill Cipher"],
                    "correct": 0,
                    "why": "The Vigenère cipher applies a repeating keyword so each letter gets "
                           "its own Caesar shift — a polyalphabetic Caesar.",
                    "wrong": {
                        1: "A keyword cipher uses the keyword to build one fixed substitution "
                           "alphabet, so it stays monoalphabetic.",
                        2: "A one-time pad uses a truly random key as long as the message, used "
                           "once. That is what makes it unbreakable, not a keyword.",
                        3: "The Hill cipher encrypts blocks of letters with matrix multiplication, "
                           "not with a repeating keyword shift.",
                    },
                },
                {
                    "type": "mcq",
                    "q": "Triple DES applies three phases of encryption to the plaintext with "
                         "different keys. Which order is correct for decryption?",
                    "options": [
                        "Encrypt using first key, decrypt using the second key, encrypt using the third key",
                        "Encrypt using third key, decrypt using the second key, encrypt using the first key",
                        "Decrypt using first key, encrypt using the second key, decrypt using the third key",
                        "Decrypt using third key, encrypt using the second key, decrypt using the first key",
                    ],
                    "correct": 3,
                    "why": "Encryption runs E(K1) → D(K2) → E(K3), so decryption reverses it "
                           "exactly: D(K3) → E(K2) → D(K1). Undo the last step first.",
                    "wrong": {
                        0: "That is the encryption order, not the decryption order.",
                        1: "The operations are right but the keys run in the wrong direction — "
                           "you must undo K3 before K1.",
                        2: "The keys run in encryption order while the operations are inverted; "
                           "decryption has to start from the key used last.",
                    },
                },
                {
                    "type": "mcq",
                    "q": "To watch the World Cup final you subscribe to a sports channel, which "
                         "gives you a licence to decrypt the scrambled channel. Which key does "
                         "the decryption use?",
                    "options": [
                        "A private key of their server",
                        "A private key generated in my device to be used by me only",
                        "A public key sent by their server to everyone",
                        "My public key generated in my device",
                    ],
                    "correct": 1,
                    "why": "The broadcaster encrypts the content key to each subscriber, and only "
                           "the private key held inside your own device or card can unwrap it. "
                           "That is what makes the licence yours and non-transferable.",
                    "wrong": {
                        0: "The server's private key never leaves the broadcaster. If it were "
                           "needed on your side, a single leak would break every subscriber.",
                        2: "A public key everybody holds cannot protect anything — non-subscribers "
                           "would decrypt the channel too.",
                        3: "Public keys encrypt or verify; they never decrypt material addressed "
                           "to you.",
                    },
                },
                {
                    "type": "mcq",
                    "q": "Which is a generally accepted implementation of a role-based "
                         "authentication model?",
                    "options": [
                        "People are assigned access to an application through certain communication paths.",
                        "People are assigned access to an application by group identifiers, not individual accounts.",
                        "People are assigned access to an application through groups by job function.",
                        "People are assigned access to an application directly by their own account.",
                    ],
                    "correct": 2,
                    "why": "RBAC ties permissions to the job function; a person gets rights by "
                           "holding the role, and loses them when the role changes.",
                    "wrong": {
                        0: "Granting access by communication path is closer to rule-based or "
                           "network-based control, not a role.",
                        1: "Grouping accounts is only half of it. RBAC requires the group to "
                           "represent a job function, otherwise it is an arbitrary group.",
                        3: "Assigning rights account by account is exactly what RBAC replaces — "
                           "it is the source of authorization creep.",
                    },
                },
                {
                    "type": "mcq",
                    "q": "______ allows the systems admin to grant users the exact privileges "
                         "they need to accomplish a task, with no additions.",
                    "options": ["Least privilege", "Need to know", "Access control list",
                                "Security clearance level"],
                    "correct": 0,
                    "why": "Least privilege is about the rights required to perform the task — no "
                           "more than the minimum, for no longer than needed.",
                    "wrong": {
                        1: "Need to know restricts access to the data a person must see. It is "
                           "about information, while least privilege is about actions.",
                        2: "An ACL is the mechanism that records permissions; it does not itself "
                           "say how generous those permissions should be.",
                        3: "A clearance level says how sensitive a subject may go; it does not "
                           "restrict them to a task's exact needs.",
                    },
                },
                {
                    "type": "mcq",
                    "q": "______ is an access-control model that lets you reason about the access "
                         "rights in a system and find whether a leakage of rights has occurred.",
                    "options": ["Take-Grant Model", "Access Control Matrix",
                                "Bell-LaPadula Model", "Biba Model"],
                    "correct": 0,
                    "why": "The take-grant model represents rights as a graph with take, grant, "
                           "create and remove rules, so you can prove whether a right can ever "
                           "leak to a subject.",
                    "wrong": {
                        1: "An access control matrix is a snapshot of who may do what right now. "
                           "It does not model how rights propagate over time.",
                        2: "Bell-LaPadula governs confidentiality through read-down and write-up "
                           "rules.",
                        3: "Biba governs integrity, the mirror image of Bell-LaPadula.",
                    },
                },
                {
                    "type": "mcq",
                    "q": "New access rights are assigned to an employee without the old "
                         "permissions being reviewed and removed. This is called ______.",
                    "options": ["Default to Zero", "Need to Know Principle",
                                "Authorization Creep", "Declassification"],
                    "correct": 2,
                    "why": "Rights accumulate as someone moves between roles and nobody revokes "
                           "the old ones — authorization creep, and a direct violation of least "
                           "privilege.",
                    "wrong": {
                        0: "Default to zero means a subject starts with no access until rights "
                           "are granted — the opposite situation.",
                        1: "Need to know limits access to required information; it is the "
                           "principle being broken here, not the name of the problem.",
                        3: "Declassification lowers the sensitivity label of data, which has "
                           "nothing to do with a user's accumulated rights.",
                    },
                },
                {
                    "type": "mcq",
                    "q": "______ is the security measure whereby a process is allowed to read "
                         "from and write to only certain memory locations and resources.",
                    "options": ["Process confinement", "Process isolation", "Process bound",
                                "All of the above"],
                    "correct": 0,
                    "why": "Confinement restricts where a process may read and write, so a "
                           "compromised process cannot reach beyond its sandbox.",
                    "wrong": {
                        1: "Isolation keeps processes from interfering with each other's memory. "
                           "Related, but it is about separation between processes rather than "
                           "the bounds placed on one.",
                        2: "The bounds are the limits themselves; confinement is the enforcement "
                           "of those limits.",
                        3: "The three terms are distinct, so the catch-all is wrong.",
                    },
                },
                {
                    "type": "mcq",
                    "q": "A separate authentication server validates the login once, and the user "
                         "then reaches all services without re-entering credentials. This is:",
                    "options": ["Two-factor Authentication", "Single Sign On (SSO)",
                                "Google Authenticator", "Abstraction"],
                    "correct": 1,
                    "why": "One authentication event granting access to many services is single "
                           "sign-on.",
                    "wrong": {
                        0: "Two-factor is about how strongly one login is proven, not how many "
                           "services that login covers.",
                        2: "Google Authenticator generates one-time codes — a second factor, not "
                           "an SSO architecture.",
                        3: "Abstraction is a design concept for hiding complexity; it is not an "
                           "authentication mechanism.",
                    },
                },
                {
                    "type": "mcq",
                    "q": "Frequent emails from someone impersonating a bank, with a story about "
                         "an account breach, trying to convince you specifically to disclose your "
                         "credentials, is called ______.",
                    "options": ["Phishing", "Spear phishing", "Whaling", "Pretexting"],
                    "correct": 1,
                    "why": "The word that decides it is 'specifically': the message is aimed at "
                           "one chosen target, which makes it spear phishing.",
                    "wrong": {
                        0: "Plain phishing is untargeted — the same mail goes to thousands in the "
                           "hope that someone bites.",
                        2: "Whaling is spear phishing aimed at a senior executive. Nothing here "
                           "says the target is a high-value executive.",
                        3: "Pretexting is the invented scenario used to build trust. It is the "
                           "technique inside the attack rather than the name of this attack.",
                    },
                },
            ],
        },
        {
            "name": "Q1 Part 2 · Match the access-control concept",
            "note": "3 marks · an option may be used twice",
            "questions": [
                {
                    "type": "match",
                    "q": "Choose the concept that matches each description.",
                    "options": ["Discretionary Access Control", "Non-Discretionary Access",
                                "Rule-based Access control", "Mandatory Access Control",
                                "Role-based Access control", "Constrained user interfaces"],
                    "items": [
                        ["As the sole owner of a very small startup's website, with no assistance, "
                         "you monitor user registrations and grant access based on what you think "
                         "is good for your company.",
                         "Discretionary Access Control",
                         "The owner of the resource decides personally who gets in. Owner "
                         "discretion is the definition of DAC."],
                        ["You are the security admin in a ministry responsible for a classified "
                         "resource, and you assign internal users based on their security "
                         "clearance levels.",
                         "Mandatory Access Control",
                         "Clearance levels and classification labels enforced by the system, not "
                         "by the data owner, is MAC."],
                        ["As an LMS admin you ensure that the 'edit' buttons for creating a quiz "
                         "only appear according to the user's privilege.",
                         "Constrained user interfaces",
                         "Hiding the controls a user may not use restricts access through the "
                         "interface itself."],
                        ["In a supermarket, the cashier needs the supervisor's approval to cancel "
                         "a bill and refund a customer, following a predefined refund policy.",
                         "Role-based Access control",
                         "The permission belongs to the supervisor role rather than the person; "
                         "whoever holds that role can approve."],
                        ["A small business has 10 computers in a peer-to-peer network. All users "
                         "are responsible for their own security and set file and folder "
                         "privileges as they see fit.",
                         "Discretionary Access Control",
                         "Each user controls their own resources — DAC again, which is why the "
                         "paper says an option may be used twice."],
                        ["Filtering traffic in a firewall to block blacklisted websites based on "
                         "preconfigured rules.",
                         "Rule-based Access control",
                         "The decision comes from rules applied uniformly to everyone, regardless "
                         "of identity or role."],
                    ],
                },
            ],
        },
        {
            "name": "Q2 · Short answers",
            "note": "15 marks",
            "questions": [
                {
                    "type": "short",
                    "q": "Explain how IPSec in tunnel mode provides confidentiality, integrity, "
                         "authentication and non-repudiation. (3 marks)",
                    "concepts": [
                        ["esp", "encrypt", "payload"],
                        ["authentication header", "ah", "integrity"],
                        ["non-repudiation", "nonrepudiation", "origin"],
                    ],
                    "answer": "In tunnel mode the whole original packet, header included, is "
                              "encapsulated in a new packet. ESP encrypts that payload, giving "
                              "confidentiality. The Authentication Header provides data integrity "
                              "and data-origin authentication, so the receiver knows the packet "
                              "was not altered and who sent it. Integrity plus origin "
                              "authentication together give non-repudiation — the sender cannot "
                              "deny having sent it.",
                    "why": "Mention each of the four properties and the mechanism that delivers "
                           "it: ESP encryption for confidentiality, AH for integrity and origin "
                           "authentication, and the combination for non-repudiation. A mark is "
                           "for the tunnel-mode drawing.",
                },
                {
                    "type": "short",
                    "q": "Explain how the accuracy of biometric devices is measured using FAR, "
                         "FRR and CER. (3 marks)",
                    "concepts": [
                        ["false rejection", "frr", "type i", "type 1"],
                        ["false acceptance", "far", "type ii", "type 2"],
                        ["crossover", "cer", "equal"],
                    ],
                    "answer": "False Rejection Rate (FRR, a Type I error): a valid subject is "
                              "refused — a registered user's fingerprint is rejected. False "
                              "Acceptance Rate (FAR, a Type II error): an invalid subject is "
                              "accepted — an unregistered attacker is recognised. Crossover Error "
                              "Rate (CER): the sensitivity setting at which FRR equals FAR, "
                              "stated as a percentage. A lower CER means a more accurate device.",
                    "why": "The examiner wants all three defined and the link between them: FRR "
                           "annoys legitimate users, FAR lets attackers in, and CER is the "
                           "single number used to compare devices.",
                },
                {
                    "type": "short",
                    "q": "Sniffing can be carried out by duplicating MAC records through MAC "
                         "poisoning. Give one way to detect sniffing on your network and one way "
                         "to prevent MAC poisoning. (2 marks)",
                    "concepts": [
                        ["arpwatch", "arp watch", "ping", "detect", "monitor"],
                        ["static", "port security", "dhcp snooping"],
                    ],
                    "answer": "Detect: run ARP watch to alert on changed MAC-to-IP bindings, or "
                              "ping a suspect device and watch which interface replies. Prevent: "
                              "configure static MAC entries or enable port security on the switch "
                              "so a port only accepts its known address.",
                    "why": "One detection method and one prevention method — the paper awards a "
                           "mark for each half.",
                },
                {
                    "type": "short",
                    "q": "You want to reuse a hard disk (HDD). What is the best sanitization "
                         "technique to ensure no single bit can be recovered? Explain. (2 marks)",
                    "concepts": [
                        ["degauss"],
                        ["magnetic", "electromagnetic", "field"],
                    ],
                    "answer": "Degaussing. Exposing the platters to a strong electromagnetic field "
                              "resets the magnetic domains that store the bits, so no residual "
                              "data remains to be recovered.",
                    "why": "Name the technique and say why it works — the magnetic field destroys "
                           "the stored pattern itself, which is what defeats data remanence.",
                },
                {
                    "type": "short",
                    "q": "Differentiate between the Biba model and the Bell-LaPadula model, in "
                         "terms of the aim and the mechanism of each. (2 marks)",
                    "concepts": [
                        ["biba", "integrity"],
                        ["lapadula", "confidentiality"],
                    ],
                    "answer": "Biba protects integrity: it stops information flowing up from a low "
                              "integrity level to a high one, so trusted data is never "
                              "contaminated (no read down, no write up). Bell-LaPadula protects "
                              "confidentiality: it stops information flowing down from a high "
                              "security level to a lower one (no read up, no write down).",
                    "why": "Name the goal of each model and the direction of flow it forbids. "
                           "Biba is integrity, Bell-LaPadula is confidentiality; they are mirror "
                           "images of each other.",
                },
                {
                    "type": "short",
                    "q": "Using an example, differentiate between due care and due diligence, and "
                         "show the relation between the two. (3 marks)",
                    "concepts": [
                        ["due care", "reasonable"],
                        ["due diligence", "ongoing", "continued", "maintain"],
                        ["example", "policy", "structure", "standard"],
                    ],
                    "answer": "Due care is taking the reasonable steps a prudent organisation "
                              "would take to protect its interests — for example building a "
                              "formal security structure of policy, standards, baselines, "
                              "guidelines and procedures. Due diligence is the continuing "
                              "activity that keeps that effort alive: applying the structure "
                              "across the IT estate and maintaining it. Due care sets it up; due "
                              "diligence keeps it working.",
                    "why": "The distinction is do the right thing (due care) versus keep checking "
                           "that it is still being done (due diligence), plus a concrete example.",
                },
            ],
        },
        {
            "name": "Q3 · Cryptography and attack identification",
            "note": "15 marks",
            "questions": [
                {
                    "type": "numeric",
                    "q": "Given P = 5 and Q = 7, use RSA to sign the message \"B\" (M = 2) with "
                         "e = 5. What is the signature S?",
                    "answer": 32,
                    "tol": 0,
                    "unit": "",
                    "why": "N = P × Q = 35 and φ(N) = (5−1)(7−1) = 24. With e = 5, "
                           "gcd(5, 24) = 1, so d = 5 because 5 × 5 = 25 ≡ 1 (mod 24). Signing "
                           "uses the private key: S = M<sup>d</sup> mod N = 2<sup>5</sup> mod 35 "
                           "= 32. Verify with the public key: 32<sup>5</sup> mod 35 = 2, which is "
                           "the original message, so the signature checks out.",
                    "note": "The official key writes S = 29 and then verifies with mod 33, mixing "
                            "in an N from a different question. The method it shows is right; the "
                            "arithmetic is not. 2⁵ = 32, and 32 < 35, so the signature is 32.",
                },
                {
                    "type": "mcq",
                    "q": "A manager complains that an employee who moved to another team still "
                         "reaches her department's sensitive data. Staff keep gaining new rights "
                         "while retaining the old ones. Which term describes this?",
                    "options": ["Least privilege", "Authorization creep",
                                "Mandatory access control", "Discretionary access control"],
                    "correct": 1,
                    "why": "Permissions accumulate across role changes because the old ones are "
                           "never revoked. The fix is a review at every transfer, enforcing least "
                           "privilege.",
                    "wrong": {
                        0: "Least privilege is the principle being violated, not the name of the "
                           "situation.",
                        2: "MAC assigns labels and clearances; it describes a model, not this "
                           "accumulation problem.",
                        3: "DAC may have enabled it by letting owners hand out rights, but the "
                           "term for the result is authorization creep.",
                    },
                },
                {
                    "type": "match",
                    "q": "Identify the attack behind each scenario.",
                    "options": ["Smurf attack", "Salami theft", "Zero-day attack",
                                "Keylogger", "Reverse social engineering"],
                    "items": [
                        ["A flood of ICMP responses from every PC in the company targets the web "
                         "server. The server never sent any ICMP requests, and the network log "
                         "shows the source address of those requests was the server's own IP.",
                         "Smurf attack",
                         "The attacker broadcast ICMP echo requests spoofed with the server's "
                         "address, so every machine replied to the server at once — an amplified "
                         "denial of service."],
                        ["A staff member subscribed to three free magazines. One asked for his "
                         "birth details, another for his national ID, the third for his bank "
                         "account. He suspects one entity collected all of it.",
                         "Salami theft",
                         "Each request looks harmless on its own; the attack is in slicing the "
                         "collection into small pieces that together build a complete profile."],
                        ["Malware has run in the background for a week. Antivirus, firewall and "
                         "every other control missed it, no information exists online, and the "
                         "relevant organisations are still investigating.",
                         "Zero-day attack",
                         "No signature, no public information and no patch yet — the flaw is "
                         "unknown to defenders, which is what zero-day means."],
                        ["Mukhtar logged out of Gmail in a computer lab and cleared the browsing "
                         "history. Someone later used the same PC, obtained his credentials and "
                         "sent unwanted emails.",
                         "Keylogger",
                         "Logging out and clearing history cannot help if the keystrokes were "
                         "captured as they were typed. An on-screen keyboard defeats a hardware "
                         "or software key logger."],
                        ["Malicious pop-ups appeared and the PC behaved strangely. The victim "
                         "recalled a technician who had warned him about exactly this, called "
                         "him for help, handed over credentials and confidential data, and the "
                         "technician vanished.",
                         "Reverse social engineering",
                         "The attacker caused the problem, advertised himself as the fix, and "
                         "made the victim initiate contact. Because the victim made the call, he "
                         "trusted the attacker completely."],
                    ],
                },
            ],
        },
    ],
}

FINAL_221_B = {
    "slug": "11-final-exam-221-version-b",
    "file": "final-exam-221-version-b.html",
    "title": "Final Exam 221 (Version B)",
    "item": "ITEM_11",
    "meta": "Dr. Rabia Latif · 21 December 2022 · 3 hours · 40 marks",
    "intro": "Version B of the 221 final: hashing and PKI, access-control models and "
             "rings, Bell-LaPadula, Diffie-Hellman with a man in the middle, and RSA.",
    "sections": [
        {
            "name": "Q1 Part 1 · Multiple choice",
            "note": "0.5 marks each",
            "questions": [
                {
                    "type": "mcq",
                    "q": "In case of data loss, ______ must be available to restore the affected "
                         "data to its correct state.",
                    "options": ["Backup", "Redundancies", "Checksum", "Both (a) and (b)"],
                    "correct": 3,
                    "why": "Backups restore an earlier good copy and redundancy keeps a live "
                           "second copy available; recovery planning uses both.",
                    "wrong": {
                        0: "Backup alone is part of the answer, but the option that includes "
                           "redundancy is more complete.",
                        1: "Redundancy alone is part of the answer too — read the options to the "
                           "end before choosing.",
                        2: "A checksum only detects that data changed. It cannot restore anything.",
                    },
                },
                {
                    "type": "mcq",
                    "q": "PASTA is a ______ that aims at selecting or developing countermeasures "
                         "in relation to the value of the assets to be protected.",
                    "options": ["Attacker-centric approach", "Risk-centric approach",
                                "Software-centric approach", "Application-centric approach"],
                    "correct": 1,
                    "why": "PASTA — Process for Attack Simulation and Threat Analysis — is the "
                           "risk-centric threat-modelling method: countermeasures are chosen "
                           "against the value of the asset at risk.",
                    "wrong": {
                        0: "Attacker-centric modelling starts from the adversary's goals and "
                           "capability. That is closer to attack trees.",
                        2: "Software-centric modelling starts from the design of the system, as "
                           "STRIDE typically does.",
                        3: "Application-centric is not one of the standard categories; the phrase "
                           "'in relation to the value of the assets' points to risk.",
                    },
                },
                {
                    "type": "mcq",
                    "q": "SHA-3 supports hash lengths of ______, and its internal structure "
                         "differs significantly from the rest of the SHA family.",
                    "options": ["256 & 512 bits", "192 & 160 bits", "160 & 256 bits",
                                "Only 512 bits"],
                    "correct": 0,
                    "why": "SHA-3 is built on the Keccak sponge construction rather than the "
                           "Merkle-Damgård structure of SHA-1 and SHA-2, and the course lists its "
                           "lengths as 256 and 512 bits.",
                    "wrong": {
                        1: "160 bits is SHA-1's digest length; 192 is not a SHA-3 length.",
                        2: "160 again belongs to SHA-1.",
                        3: "SHA-3 is not limited to a single length.",
                    },
                },
                {
                    "type": "mcq",
                    "q": "MD4 is the ______ algorithm and ______ secure than MD5.",
                    "options": ["Fast, more", "Slow, less", "Fast, less", "Slow, more"],
                    "correct": 2,
                    "why": "MD4 is the faster of the two and the weaker: MD5 was designed "
                           "specifically to repair MD4's weaknesses, at some cost in speed.",
                    "wrong": {
                        0: "The speed is right but the security is not — MD4 is the weaker one.",
                        1: "MD4 is faster than MD5, not slower.",
                        3: "Both halves are wrong: MD4 is faster and less secure.",
                    },
                },
                {
                    "type": "mcq",
                    "q": "Which of the following is not a key step while doing threat modeling?",
                    "options": ["Visualize", "Identify threats", "Execute", "Validate"],
                    "correct": 2,
                    "why": "Threat modelling is visualize, identify threats, then validate. "
                           "Execution is what happens afterwards, when the countermeasures are "
                           "implemented.",
                    "wrong": {
                        0: "Visualizing the system — diagramming components and data flows — is "
                           "the first step.",
                        1: "Identifying threats against that picture is the core of the exercise.",
                        3: "Validating the model and the mitigations closes the loop.",
                    },
                },
                {
                    "type": "mcq",
                    "q": "______ can be used to control what data is accessed during certain "
                         "types of functions and what commands can be carried out on the data.",
                    "options": ["Groups", "Roles", "Transaction types", "User Interface"],
                    "correct": 2,
                    "why": "Restricting by transaction type binds the permission to the operation "
                           "being performed, so it controls both the data touched and the "
                           "commands allowed.",
                    "wrong": {
                        0: "Groups collect users; they do not describe the operation performed.",
                        1: "Roles describe the job function of the user, not the transaction.",
                        3: "Constraining the interface hides options, but the control here is "
                           "over the operation itself.",
                    },
                },
                {
                    "type": "mcq",
                    "q": "______ gives control of access to the people who are closer to the "
                         "resources and lacks proper consistency.",
                    "options": ["Decentralized Access Control", "Subject-Oriented Capability Table",
                                "Object-Oriented Capability Table", "Centralized Access Control"],
                    "correct": 0,
                    "why": "Decentralizing puts the decision with local owners near the resource. "
                           "That is responsive but inconsistent, because no single authority "
                           "applies the same standard everywhere.",
                    "wrong": {
                        1: "A capability table lists the rights a subject holds; it is a data "
                           "structure, not a governance approach.",
                        2: "Same again from the object's side — a structure, not a model of who "
                           "decides.",
                        3: "Centralized control is the opposite: one authority, consistent "
                           "decisions, slower response.",
                    },
                },
                {
                    "type": "mcq",
                    "q": "Processes in ______ can access more resources and interact with the "
                         "operating system more directly than processes in ______.",
                    "options": ["RING-2, RING-1", "RING-1, RING-2", "RING-3, RING-2",
                                "RING-3, RING-0"],
                    "correct": 1,
                    "why": "Lower ring numbers are more privileged. Ring 0 is the kernel, ring 3 "
                           "is user mode, so ring 1 outranks ring 2.",
                    "wrong": {
                        0: "Reversed — ring 2 is less privileged than ring 1.",
                        2: "Ring 3 is the least privileged of all, so it cannot outrank ring 2.",
                        3: "Ring 3 against ring 0 is the largest gap in the wrong direction.",
                    },
                },
                {
                    "type": "mcq",
                    "q": "Operating in what is called the problem state is associated with ______.",
                    "options": ["Supervisor mode", "Kernel mode", "User mode", "Operation mode"],
                    "correct": 2,
                    "why": "The problem state is the historical name for user mode, where "
                           "application code runs without direct access to privileged "
                           "instructions.",
                    "wrong": {
                        0: "Supervisor mode is the privileged state, the opposite of the problem "
                           "state.",
                        1: "Kernel mode is another name for that same privileged state.",
                        3: "Operation mode is not one of the processor states in this taxonomy.",
                    },
                },
                {
                    "type": "mcq",
                    "q": "Which is not an appropriate technique to protect web applications "
                         "against SQL injection?",
                    "options": ["Limit account privileges", "Cloud hosting", "Input validation",
                                "Both (a) and (b)"],
                    "correct": 1,
                    "why": "Where the application is hosted makes no difference to SQL injection. "
                           "The flaw is in how the application builds its queries, and it moves "
                           "to the cloud with the code.",
                    "wrong": {
                        0: "Limiting the database account's privileges is a real mitigation — it "
                           "caps the damage of a successful injection.",
                        2: "Validating and parameterising input is the primary defence.",
                        3: "Limiting privileges is a genuine defence, so this pairing is wrong.",
                    },
                },
                {
                    "type": "mcq",
                    "q": "The ______ model makes sure conflicts of interest are recognised and "
                         "that people are prevented from taking advantage of data they should not "
                         "have access to.",
                    "options": ["Biba Model", "Clark-Wilson Model", "Bell-LaPadula Model",
                                "Brewer and Nash Model"],
                    "correct": 3,
                    "why": "Brewer and Nash — the Chinese Wall model — changes what you may see "
                           "based on what you have already seen, precisely to prevent conflicts "
                           "of interest.",
                    "wrong": {
                        0: "Biba is about integrity levels.",
                        1: "Clark-Wilson enforces integrity through well-formed transactions and "
                           "separation of duties.",
                        2: "Bell-LaPadula is about confidentiality levels, not commercial "
                           "conflicts of interest.",
                    },
                },
                {
                    "type": "mcq",
                    "q": "S/MIME relies on the use of ______ for exchanging cryptographic keys.",
                    "options": ["RSA", "Diffie-Hellman key exchange protocol", "Digital Signatures",
                                "X.509 certificates"],
                    "correct": 3,
                    "why": "S/MIME binds a public key to an identity with an X.509 certificate, "
                           "which is what lets two mail clients trust each other's keys.",
                    "wrong": {
                        0: "RSA may be the algorithm inside the certificate, but the exchange "
                           "mechanism is the certificate.",
                        1: "Diffie-Hellman agrees a shared secret; S/MIME distributes keys via "
                           "certificates.",
                        2: "Signatures prove authenticity of a message, they do not distribute "
                           "the keys.",
                    },
                },
                {
                    "type": "mcq",
                    "q": "Which reason is not appropriate for a Certificate Authority to revoke a "
                         "certificate?",
                    "options": ["Compromised", "Hosting a new website",
                                "Security association changed", "Erroneously issued"],
                    "correct": 1,
                    "why": "Launching another website is ordinary business. You request an "
                           "additional certificate; the existing one is still valid for its own "
                           "subject.",
                    "wrong": {
                        0: "A compromised private key is the most urgent reason to revoke.",
                        2: "If the association the certificate attests to has changed, it no "
                           "longer states the truth.",
                        3: "A certificate issued in error must be withdrawn.",
                    },
                },
                {
                    "type": "mcq",
                    "q": "A coworker suggests reducing the number of logins and passwords by "
                         "investigating single sign-on. Which of the following is a type of "
                         "single sign-on system?",
                    "options": ["DAC", "SAML", "Security Domains", "RBAC"],
                    "correct": 2,
                    "why": "The course keys this to security domains: a group of systems under a "
                           "common trust and security policy, so one authentication is honoured "
                           "across the domain.",
                    "wrong": {
                        0: "DAC is an access-control model, not an authentication architecture.",
                        3: "RBAC is also an access-control model — it decides what you may do "
                           "after you have authenticated.",
                    },
                    "note": "SAML is in practice the standard protocol used to implement federated "
                            "SSO, so option (b) is defensible in the real world. The marked key "
                            "chooses Security Domains, which is what this page scores.",
                },
            ],
        },
        {
            "name": "Q1 Part 2 · Match the access-control concept",
            "note": "3 marks · an option may be used twice",
            "questions": [
                {
                    "type": "match",
                    "q": "Answer each description by choosing the appropriate option.",
                    "options": ["Discretionary Access Control", "Non-Discretionary Access",
                                "Rule-based Access control", "Mandatory Access Control",
                                "Logical Access Control", "Constrained user interfaces"],
                    "items": [
                        ["Data has a 'top secret' confidentiality level and an 'engineering "
                         "project' security label, and is available only to users with both top "
                         "secret clearance and authorization for engineering documents.",
                         "Mandatory Access Control",
                         "Classification plus category, enforced by the system, is textbook MAC."],
                        ["This model is popular because it allows users a lot of freedom to "
                         "choose access rights and causes little administrative overhead.",
                         "Discretionary Access Control",
                         "Freedom for the owner to decide, at the cost of consistency, is DAC."],
                        ["Computer-system managers use these controls to decide who can get into "
                         "a system and what tasks they can perform.",
                         "Logical Access Control",
                         "Logical (technical) controls are the software mechanisms — passwords, "
                         "ACLs, encryption — as opposed to physical ones."],
                        ["As an administrator you designate user groups such as staff, "
                         "specialists or end users, and limit access to specific resources or "
                         "tasks.",
                         "Non-Discretionary Access",
                         "A central administrator sets the rights rather than the resource owner, "
                         "which makes it non-discretionary."],
                        ["Restrict users' abilities by not allowing them certain types of access "
                         "or the ability to request certain functions or information.",
                         "Constrained user interfaces",
                         "The restriction is delivered by limiting what the interface offers."],
                        ["What type of access control has been used in MAC systems as an "
                         "enforcement mechanism?",
                         "Rule-based Access control",
                         "MAC is enforced through rules comparing the subject's clearance with "
                         "the object's label, applied uniformly."],
                    ],
                },
            ],
        },
        {
            "name": "Q2 · Short answers",
            "note": "15 marks",
            "questions": [
                {
                    "type": "short",
                    "q": "Identification, authentication, authorization and accountability are "
                         "divided into two phases. What are those phases, and how do they divide "
                         "these parts? (2 marks)",
                    "concepts": [
                        ["policy definition", "definition"],
                        ["policy enforcement", "enforcement"],
                        ["authorization"],
                    ],
                    "answer": "The policy definition phase determines who has access and what "
                              "systems or resources they may use — authorization operates here. "
                              "The policy enforcement phase grants or rejects each request "
                              "against those definitions — identification, authentication and "
                              "accountability operate here.",
                    "why": "Name both phases and sort the four parts between them: authorization "
                           "is defined up front, while the other three happen at the moment of "
                           "access.",
                },
                {
                    "type": "short",
                    "q": "How is hashing different from encryption? Give two differences. (1 mark)",
                    "concepts": [
                        ["fixed", "same size", "length"],
                        ["irreversible", "one way", "one-way", "cannot"],
                    ],
                    "answer": "A hash always produces a fixed-size output determined by the "
                              "algorithm, whatever the input size, while ciphertext grows with "
                              "the plaintext. Hashing is one-way and irreversible — there is no "
                              "key that recovers the input — whereas encryption is designed to be "
                              "reversed with the right key.",
                    "why": "The two differences the paper wants are fixed-length output and "
                           "irreversibility.",
                },
                {
                    "type": "short",
                    "q": "Where can you search for a revoked certificate? Briefly explain. (2 marks)",
                    "concepts": [
                        ["crl", "revocation list"],
                        ["ocsp", "online certificate status"],
                    ],
                    "answer": "A Certificate Revocation List (CRL) is published by the CA, but it "
                              "has to be downloaded and cross-referenced periodically, which "
                              "leaves a window between a revocation and the client noticing it. "
                              "The Online Certificate Status Protocol (OCSP) removes that latency "
                              "by answering a status query for one certificate in real time.",
                    "why": "Name both mechanisms and contrast them: CRL is a periodic list with "
                           "latency, OCSP is a real-time query.",
                },
                {
                    "type": "short",
                    "q": "Which keys are used for the issuance and signature validation of an "
                         "X.509 certificate, and who is responsible for issuing it? (1 mark)",
                    "concepts": [
                        ["private key"],
                        ["public key"],
                        ["root ca", "certificate authority", "ca"],
                    ],
                    "answer": "The CA signs — issues — the certificate with its private key, and "
                              "anyone validates that signature with the CA's public key. The root "
                              "CA is responsible for signing and issuing certificates.",
                    "why": "Private key signs, public key verifies, and the root CA is the "
                           "authority. Getting the two keys the wrong way round is the usual slip.",
                },
                {
                    "type": "short",
                    "q": "Briefly explain the Type I and Type II errors generated by biometric "
                         "devices, and what CER is used for. (4 marks)",
                    "concepts": [
                        ["type i", "type 1", "false rejection", "frr"],
                        ["type ii", "type 2", "false acceptance", "far"],
                        ["cer", "crossover", "compare"],
                    ],
                    "answer": "Type I error — false rejection: a valid subject is not "
                              "authenticated. The ratio of false rejections to valid "
                              "authentications is the FRR. Type II error — false acceptance: an "
                              "invalid subject is authenticated; that ratio is the FAR. The "
                              "Crossover Error Rate is where the two curves meet, and it is used "
                              "to compare devices: a lower CER means a more accurate device.",
                    "why": "Type I is rejection of the genuine user, Type II is acceptance of the "
                           "impostor, and CER is the single comparison figure.",
                },
                {
                    "type": "short",
                    "q": "Why is RADIUS considered less secure than TACACS? Give two reasons. "
                         "(2 marks)",
                    "concepts": [
                        ["password", "only encrypts"],
                        ["udp"],
                        ["tacacs", "all", "tcp"],
                    ],
                    "answer": "RADIUS encrypts only the user's password as it travels from client "
                              "to server, leaving the rest of the exchange in the clear, and it "
                              "runs over UDP, which is unreliable. TACACS+ encrypts the entire "
                              "payload and runs over TCP, so it is both more confidential and "
                              "more reliable.",
                    "why": "Two contrasts carry the marks: how much of the traffic is encrypted, "
                           "and UDP against TCP.",
                },
            ],
        },
        {
            "name": "Q3 · Models, key exchange and RSA",
            "note": "15 marks",
            "questions": [
                {
                    "type": "match",
                    "q": "Bell-LaPadula. Top Secret: Duke (Patents, Trade Secrets). Secret: "
                         "Claire (Project plans, Contracts). Confidential: Kevin (E-Mails, "
                         "Project files). Unclassified: Emme (Telephone List, Newsletters). "
                         "Apply each rule.",
                    "options": [
                        "Own level and everything below it",
                        "Own level and everything above it",
                        "Own level only",
                    ],
                    "items": [
                        ["Simple Confidentiality Rule (read) applied to Claire — which objects "
                         "may she read?",
                         "Own level and everything below it",
                         "The simple security property is no read up. Claire is Secret, so she "
                         "reads Secret, Confidential and Unclassified: project plans, contracts, "
                         "e-mails, project files, telephone list and newsletters."],
                        ["Star Confidentiality Rule (write) applied to Kevin — where may he write?",
                         "Own level and everything above it",
                         "The star property is no write down, to stop data leaking to a lower "
                         "level. Kevin is Confidential, so he writes at Confidential, Secret and "
                         "Top Secret."],
                        ["Strong Star Confidentiality Rule applied to Duke — what may he access?",
                         "Own level only",
                         "The strong star property allows reading and writing at exactly the "
                         "subject's own level. Duke is Top Secret, so patents and trade secrets "
                         "only."],
                    ],
                },
                {
                    "type": "short",
                    "q": "A company blocks www.youtube.com, but employees still reach it. Is that "
                         "possible, how, and which trust property does it exploit? (1 mark)",
                    "concepts": [
                        ["vpn", "proxy", "tor", "tunnel"],
                        ["transitive", "trust"],
                    ],
                    "answer": "Yes. A VPN redirects the traffic through an outside network, and "
                              "proxies, SSH tunnels, browser extensions or TOR do the same. It "
                              "exploits the non-transitive trust property — the company trusts "
                              "the endpoint it can see, not the far end of the tunnel. "
                              "Intelligent firewalls that inspect or block tunnelled traffic "
                              "detect and prevent it.",
                    "why": "Name a bypass method and the trust property, then say how the "
                           "organisation detects it.",
                },
                {
                    "type": "numeric",
                    "q": "Diffie-Hellman with P = 13 and G = 5. Mark's secret is 4 and Malory's "
                         "first secret is 6. Malory intercepts and completes the exchange with "
                         "Mark. What is the shared secret K1 between Mark and Malory?",
                    "answer": 1,
                    "tol": 0,
                    "unit": "",
                    "why": "Malory sends Y<sub>D1</sub> = 5<sup>6</sup> mod 13 = 15,625 mod 13 = "
                           "8… careful: work it down step by step. 5² = 25 ≡ 12, 5³ ≡ 60 ≡ 8, "
                           "5⁶ ≡ 8² = 64 ≡ 12 (mod 13). Mark computes K1 = "
                           "Y<sub>D1</sub><sup>4</sup> mod 13 = 12⁴ mod 13. Since 12 ≡ −1, "
                           "(−1)⁴ = 1, so <strong>K1 = 1</strong>. Malory gets the same value "
                           "from Y<sub>M</sub><sup>6</sup> mod 13, which is how a man in the "
                           "middle ends up sharing a key with each party separately.",
                },
                {
                    "type": "numeric",
                    "q": "Same exchange: Ava's secret is 3 and Malory's second secret is 2. What "
                         "is the shared secret K2 between Ava and Malory?",
                    "answer": 12,
                    "tol": 0,
                    "unit": "",
                    "why": "Ava's public key Y<sub>A</sub> = 5³ mod 13 = 125 mod 13 = 8. Malory "
                           "computes K2 = Y<sub>A</sub><sup>2</sup> mod 13 = 64 mod 13 = "
                           "<strong>12</strong>. Ava computes the same from "
                           "Y<sub>D2</sub> = 5² mod 13 = 12, giving 12³ mod 13 = 12. Ava and Mark "
                           "now hold different keys, each shared with Malory, who relays and "
                           "reads everything.",
                },
                {
                    "type": "mcq",
                    "q": "You want to secure email with RSA where n = 33. Which value is usable "
                         "to generate a public key: e = 10 or e = 11?",
                    "options": ["e = 10", "e = 11", "Both work", "Neither works"],
                    "correct": 1,
                    "why": "φ(33) = (11−1)(3−1) = 20. The exponent must be coprime with φ(n): "
                           "gcd(10, 20) = 10, so 10 is unusable, while gcd(11, 20) = 1, so e = 11 "
                           "works.",
                    "wrong": {
                        0: "10 shares the factors 2 and 5 with 20, so no modular inverse d "
                           "exists and the key cannot be completed.",
                        2: "Only one of them is coprime with φ(n) = 20.",
                        3: "e = 11 is perfectly usable.",
                    },
                    "note": "The official key's wording here is garbled ('E=12 is not a prime "
                            "number'). The test that matters is gcd(e, φ(n)) = 1, not whether e "
                            "is prime.",
                },
                {
                    "type": "numeric",
                    "q": "Dexter chooses p = 11 and q = 3 with e = 3 (the smallest odd prime). "
                         "Find d such that e × d ≡ 1 (mod φ(n)).",
                    "answer": 7,
                    "tol": 0,
                    "unit": "",
                    "why": "n = 33 and φ(n) = 10 × 2 = 20. We need 3d ≡ 1 (mod 20); "
                           "3 × 7 = 21 = 20 + 1, so <strong>d = 7</strong>. The public key is "
                           "(3, 33) and the private key is (7, 33).",
                },
                {
                    "type": "numeric",
                    "q": "Using that key pair, Dexter signs the message M = 3. What is the signed "
                         "value S?",
                    "answer": 9,
                    "tol": 0,
                    "unit": "",
                    "why": "Signing uses the private exponent modulo n: S = M<sup>d</sup> mod n = "
                           "3<sup>7</sup> mod 33. 3⁷ = 2,187 and 2,187 = 33 × 66 + 9, so "
                           "<strong>S = 9</strong>. Verification: 9³ = 729 = 33 × 22 + 3, "
                           "recovering M = 3.",
                    "note": "The official key computes 3⁷ mod 20 and gets 7. The modulus for "
                            "signing and verifying is n = 33; φ(n) = 20 is only used to find d.",
                },
                {
                    "type": "numeric",
                    "q": "Alice and Bob use p = 13 and g = 7. Alice's public key is Pₐ = 8. "
                         "Bob's secret is 3. What shared secret do they establish?",
                    "answer": 5,
                    "tol": 0,
                    "unit": "",
                    "why": "Bob's public key is 7³ mod 13 = 343 mod 13 = 5. The shared secret is "
                           "Alice's public key raised to Bob's secret: 8³ mod 13 = 512 mod 13 = "
                           "<strong>5</strong>. Alice reaches the same value from Bob's public "
                           "key and her own secret, which is the point of the protocol.",
                },
            ],
        },
    ],
}

EXAMS = [QUIZ_222, FINAL_221_A, FINAL_221_B]
