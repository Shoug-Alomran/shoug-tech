"""CYS401 annotated slides — Chapter 1: Introduction to Cybersecurity.

Slide text comes from the PDF (cys401_annotated.pdftext). AUTO_SLIDES shows slides whose layout is too rich
to retype as the original slide image and crops the picture of the rest (see annotated_slides.auto_figure).
See cs331_annotated/ch01_1_introduction.py for the ANN keys; `whole=True` forces the slide image."""
from .common import mcq, past, scen, see, short, tf, tip, trap, trick

AUTO_SLIDES = True

DECK = {
    'key': 'ch1',
    'slug': '01-introduction-to-cybersecurity',
    'file': 'introduction-to-cybersecurity',
    'title': 'Introduction to Cybersecurity',
    'chapter': 'Chapter 1',
    'pdf': '/academics/cybersecurity/cys401/slides/chapter-1-introduction-to-cybersecurity/',
    'lede': ('What cybersecurity is, defence in depth and the layers of security, the critical characteristics of '
             'information (C.I.A. plus accuracy, authenticity, utility, possession), the McCumber cube, the '
             'components of an information system, and the SDLC vs. the SecSDLC. Both Quiz 1 papers (222 and '
             '232) and Major A were built almost entirely from this deck.'),
}

CHARS = ('Characteristics of information: Confidentiality (no disclosure) · Integrity (accurate, complete, unaltered) · Availability (access when needed) · '
         'Accuracy (no errors, the value expected) · Authenticity (genuine, as originally created) · Utility (useful for a purpose) · Possession (ownership/control).')

ANN = {
    1: dict(kind='title', title='Cyber Security: Introduction', body=[], sub='CYS401 · Lecture 1', tips=[tip(CHARS)]),
    2: dict(notes=['What is security → characteristics of information → components of an IS → SDLC → SecSDLC.']),
    3: dict(notes=['Ice-breaker quiz (Pew Research cybersecurity knowledge quiz).']),
    4: dict(notes=['Why cybersecurity matters: everything is connected, attacks are constant and costly.']),
    5: dict(notes=['Getting started.']),
    6: dict(notes=['Cybersecurity = protecting systems, networks and data from digital attacks.'],
            past=[past('q222', 'Q1 · ICT stands for', related=True)]),
    7: dict(notes=['“Cyber” = anything related to computers, networks and the internet (ICT = Information and Communication Technology).']),
    8: dict(notes=['Security is a process, not a product.']),
    9: dict(notes=['**Defence in depth**: layered safeguards: physical (guards, locks), perimeter (firewalls, border routers, VPN), network (segments, NIDS), host (OS hardening, patching, antivirus), application, data (encryption, ACLs), plus policies and awareness.',
                   'If one layer fails, the others still protect.'],
            tips=[trap('Defence in depth ≠ fail-over. “When one device fails another takes over” is redundancy (availability), not layering.')],
            past=[past('q222', 'Q1 · characteristic of defence in depth'), past('q222', 'Q3 · match controls to layers'), past('q232', 'Q1 · characteristic of defence in depth'),
                  past('q232', 'Q5 · one control per layer')],
            exam=[mcq('What is a characteristic of a layered defence-in-depth approach?', ['One safeguard failing does not affect the effectiveness of the others', 'Three or more devices are used', 'Routers are replaced with firewalls', 'When one device fails, another takes over'], 0, 'Quiz 1 222 and 232.'),
                  mcq('Border firewalls and screening routers belong to which defence-in-depth layer?', ['Perimeter', 'Host', 'Application', 'Data'], 0, 'Quiz 1 222, Q3.'),
                  mcq('Encryption at rest and ACLs on records belong to the ___ layer.', ['Data', 'Perimeter', 'Physical', 'Network'], 0, 'Quiz 1 222, Q3.')],
            weight=3),
    10: dict(notes=['Multiple layers of security in an organization: physical, personnel, operations, communications, network, information security.'],
             past=[past('q222', 'Q1 · not a physical security measure'), past('q232', 'Q1 · not a physical security measure')],
             exam=[mcq('Which is NOT a physical security measure against physical hacking?', ['Updating the software patches on your computer', 'Adding a front desk and restricting access to the back', 'Locking the server room', 'Checking how employees store data and storage devices'], 0, 'Quiz 1 222 and 232. Patching is a technical control.')],
             weight=3),
    11: dict(notes=['Cybersecurity covers information security, network security, application security…']),
    12: dict(notes=['The goal of cybersecurity: the **C.I.A.** triad: confidentiality, integrity, availability.'],
             past=[past('f221a', 'MCQ · cybersecurity pillars', related=True)], weight=3),
    13: dict(notes=['C.I.A. are the critical characteristics, but accuracy, authenticity, utility and possession matter too.'], tips=[tip(CHARS)]),
    14: dict(notes=['Confidentiality: no disclosure to unauthorised people. Integrity: accurate, complete, authorised (no corruption). Availability: authorised users get access without obstruction.'],
             past=[past('mA', 'A · protection from modification = integrity'), past('mB', 'A · preventing disclosure = confidentiality')],
             exam=[mcq('Protection of data from modification by unauthorised users is:', ['Integrity', 'Confidentiality', 'Availability', 'Utility'], 0, 'Major A.'),
                   mcq('Preventing disclosure or exposure to unauthorised individuals is:', ['Confidentiality', 'Integrity', 'Accuracy', 'Possession'], 0, 'Major B.')],
             weight=3),
    15: dict(notes=['Accuracy: no errors, the value the user expects. Authenticity: genuine, the same as originally created. Utility: has value for a purpose (a readable format).'],
             past=[past('q232', 'Q2 · authenticity, accuracy, utility'), past('mB', 'A · raw hex instead of a report = utility')],
             exam=[mcq('Information that is the same as when originally created, placed, stored or transferred is:', ['Authentic', 'Accurate', 'Available', 'Useful'], 0, 'Quiz 1 232.'),
                   mcq('A value different from what the user expects because of a modification means the information is no longer:', ['Accurate', 'Authentic', 'Available', 'Confidential'], 0, 'Quiz 1 232.'),
                   mcq('A doctor receives a patient file as raw hexadecimal instead of a readable report. Which characteristic is lost?', ['Utility', 'Integrity', 'Confidentiality', 'Possession'], 0, 'Major B.')],
             weight=3),
    16: dict(notes=['Possession = ownership/control. A breach of confidentiality always breaches possession, but losing possession (a stolen encrypted disk) doesn’t always breach confidentiality.'],
             past=[past('q232', 'Q2 · unauthorised user obtains the procedure = possession', related=True)],
             exam=[tf('A breach of possession always results in a breach of confidentiality.', False, 'Stolen but encrypted data is possessed by the thief but not disclosed.')], weight=3),
    17: dict(notes=['Three dimensions: security goals (C.I.A.), security measures (policy, education/training, technology), information states (storage, transmission, processing) → the McCumber cube.']),
    18: dict(notes=['**McCumber cube**: 3 × 3 × 3 = 27 cells; each cell is a goal × state × measure combination to secure.'],
             tips=[trick('McCumber axes: GOALS (C, I, A) · STATES (storage, transmission, processing) · MEASURES (technology, policy, education).')],
             past=[past('q232', 'Q3 · label the McCumber cube'), past('mA', 'B · T/F McCumber: data protected only in one state', related=True)],
             exam=[mcq('Which is NOT an information state on the McCumber cube?', ['Deletion', 'Storage', 'Transmission', 'Processing'], 0, ''),
                   tf('In the McCumber cube, data needs to be protected only while it is stored.', False, 'Major A. It must be protected in storage, transmission AND processing.')],
             weight=3),
    19: dict(notes=['States: storage (data at rest), transmission (data in transit), processing (data in use).']),
    20: dict(notes=['Five components of an IS: software, hardware, data, people, procedures (and networks).'],
             exam=[mcq('Which IS component is often the weakest link?', ['People', 'Hardware', 'Data', 'Procedures'], 0, '')], weight=2),
    21: dict(notes=['Software: the hardest to secure (bugs and errors).']),
    22: dict(notes=['Hardware: protect physical assets (locks, biometrics).']),
    23: dict(notes=['People: often the weakest component; policy, education and training help.']),
    24: dict(notes=['SDLC: a methodology for designing and implementing an IS; most common is the waterfall model.']),
    25: dict(notes=['SDLC phases: investigation, analysis, logical design, physical design, implementation, maintenance and change.']),
    26: dict(notes=['Analysis phase.']), 27: dict(notes=['Design phases.']), 28: dict(notes=['Implementation.']), 29: dict(notes=['Maintenance and change.']),
    30: dict(notes=['**SecSDLC**: the SDLC with security built into every phase.'],
             past=[past('mA', 'B · T/F secure SDLC only applies to requirements and testing (false)')],
             exam=[tf('A secure SDLC applies security only to the requirements and testing phases.', False, 'Major A. Every phase.')], weight=3),
    31: dict(notes=['Each SecSDLC phase must consider security so nothing harms the C.I.A. of information assets.']),
    32: dict(notes=['SecSDLC investigation: management defines the security project, goals and budget.'],
             past=[past('q232', 'Q4 · two security points for each SDLC phase')]),
    33: dict(notes=['SecSDLC analysis: study threats, existing controls, legal issues; risk management starts.']),
    34: dict(notes=['SecSDLC logical design: security blueprint, incident response and continuity plans.']),
    35: dict(notes=['SecSDLC physical design and implementation: choose and install the technology; test.']),
    36: dict(notes=['SecSDLC maintenance: monitor, test, update, respond to incidents.'],
             exam=[short('Give two security activities for the design and maintenance phases of the SecSDLC. (Quiz 1 232, Q4)', 'Design: threat modelling and a secure architecture/security blueprint; review the design against the security requirements. Maintenance: apply patches and security updates; continuously monitor logs and run periodic vulnerability assessments and incident response.')],
             weight=3),
    37: dict(notes=['SecSDLC follows the same phases as SDLC but also identifies specific threats and creates controls for them.']),
    38: dict(notes=['Recap.']),
}
