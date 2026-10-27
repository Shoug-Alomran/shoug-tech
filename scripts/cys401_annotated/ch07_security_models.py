"""CYS401 annotated slides — Chapter 7: Security Design Models and Capabilities.
See ch01_introduction.py for AUTO_SLIDES and the ANN keys."""
from .common import mcq, past, scen, see, short, tf, tip, trap, trick

AUTO_SLIDES = True

DECK = {
    'key': 'ch7',
    'slug': '08-security-design-models-and-capabilities',
    'file': 'security-design-models-and-capabilities',
    'title': 'Security Design Models and Capabilities',
    'chapter': 'Chapter 7',
    'pdf': '/academics/cybersecurity/cys401/slides/chapter-7-security-design-models-and-capabilities/',
    'lede': ('Security architecture principles (security by design, least privilege, default deny, separation '
             'of duties, zero trust, micro-segmentation…), architecture flaws (covert channels, maintenance hooks), '
             'process isolation and protection rings, and the security models: TCB, access control matrix, '
             'take-grant, Bell-LaPadula, Biba. Both Final 221 papers asked about least privilege, isolation, '
             'take-grant and Bell-LaPadula.'),
}

MODELS = ('Bell-LaPadula (CONFIDENTIALITY): no read up (simple), no write down (*-property). '
          'Biba (INTEGRITY): no read down, no write up. Mnemonic: BLP protects secrets from leaking down; Biba stops dirt flowing up.')

ANN = {
    1: dict(kind='title', title='Security Design Models and Capabilities', body=[], sub='CYS401 · Chapter 7', tips=[tip(MODELS)]),
    2: dict(notes=['Learning objectives.']),
    3: dict(notes=['Security architecture = the overall system that protects an organization’s IT infrastructure.']),
    4: dict(notes=['Security failures are design failures; retrofitting security is costly.']),
    5: dict(notes=['Core principles: security by design, simplicity, defence in depth, least privilege, default deny, fail securely, separation of duties, zero trust, micro-segmentation, assume breach, automation…']),
    6: dict(notes=['#1 Security by design: security requirements are part of the requirements, not an afterthought. #2 Simplicity: simpler systems have fewer flaws.']),
    7: dict(notes=['#3 Defence in depth: layers raise the attacker’s effort.'], seen=[see('ch1', 9, 'Defence in depth')]),
    8: dict(notes=['#4 **Least privilege**: grant only the minimum privileges needed.'],
            past=[past('f221a', 'MCQ · exact privileges, no additions = least privilege')],
            exam=[mcq('Granting users exactly the privileges they need for a task, nothing more, is:', ['Least privilege', 'Separation of duties', 'Default deny', 'Zero trust'], 0, 'Final 221 A.')], weight=3),
    9: dict(notes=['#5 Default deny: access is denied unless explicitly granted. #6 Fail securely.'], weight=2),
    10: dict(notes=['#7 Separation of duties: no single person controls a whole transaction (cashier needs a supervisor to refund).'],
             past=[past('f221a', 'match · supervisor approval for refunds', related=True)],
             exam=[mcq('A cashier needs a supervisor’s approval to cancel a bill and refund. This applies:', ['Separation of duties', 'Least privilege', 'Default deny', 'Simplicity'], 0, '')], weight=3),
    11: dict(notes=['#9 **Zero trust**: trust nobody, inside or outside; verify every request.'],
             exam=[mcq('Which model assumes no user or device is trusted, even inside the network?', ['Zero trust', 'Defence in depth', 'Default allow', 'Perimeter security'], 0, '')], weight=3),
    12: dict(notes=['#10 Micro-segmentation: small isolated segments to stop lateral movement.']),
    13: dict(notes=['Example: university lab networks separated from admin networks.']),
    14: dict(notes=['#11 Assume breach: design as if the attacker is already inside.']),
    15: dict(notes=['#13 Security automation: automate detection and response.']),
    16: dict(notes=['Security is a process: every system has vulnerabilities.']),
    17: dict(notes=['**Covert channel**: transferring information secretly through an unintended path (timing, storage).'],
             exam=[mcq('Transferring information through an unintended, secret path is a:', ['Covert channel', 'Maintenance hook', 'Trojan horse', 'Buffer overflow'], 0, '')], weight=3),
    18: dict(notes=['**Maintenance hook** (backdoor/trapdoor): a hidden entry point left by developers; also TOCTOU, buffer overflows.'],
             exam=[mcq('A hidden entry point left in software for easy maintenance is a:', ['Maintenance hook', 'Covert channel', 'Salami attack', 'Logic bomb'], 0, '')], weight=3),
    19: dict(kind='section', title='Techniques for Ensuring Confidentiality, Integrity, and Availability'),
    20: dict(notes=['Design programs to do only what is required.']),
    21: dict(notes=['Concepts: confinement, bounds, isolation, controls, trust and assurance.']),
    22: dict(notes=['**Process isolation**: a process may only read and write its own memory locations and resources.'],
             past=[past('f221a', 'MCQ · process restricted to certain memory locations')],
             exam=[mcq('Allowing a process to read and write only certain memory locations and resources is:', ['Isolation (confinement/bounds)', 'Least privilege', 'Polyinstantiation', 'Accountability'], 0, 'Final 221 A.')], weight=3),
    23: dict(notes=['Each process gets an authority level (protection rings): ring 0 = kernel (most privileged); user processes run in outer rings.'],
             past=[past('f221b', 'MCQ · processes in ring 0 vs ring 3'), past('f221b', 'MCQ · problem state = user mode')],
             exam=[mcq('Processes in ___ can access more resources and interact with the OS more directly than processes in ___.', ['Ring 0; ring 3', 'Ring 3; ring 0', 'User mode; kernel mode', 'Ring 2; ring 1'], 0, 'Final 221 B.'),
                   mcq('Operating in the “problem state” means running in:', ['User mode', 'Kernel mode', 'Ring 0', 'Supervisor mode'], 0, 'Final 221 B.')],
             weight=3),
    24: dict(kind='section', title='Security Models'),
    25: dict(notes=['A security model specifies and enforces security policy.']),
    26: dict(notes=['Models: TCB, state machine, information flow, take-grant, access control matrix, Bell-LaPadula, Biba, Clark-Wilson, Brewer-Nash.'],
             past=[past('f221b', 'MCQ · conflict-of-interest model = Brewer-Nash', related=True)],
             exam=[mcq('Which model prevents conflicts of interest (e.g., a consultant serving two competitors)?', ['Brewer-Nash (Chinese Wall)', 'Biba', 'Bell-LaPadula', 'Take-Grant'], 0, 'Final 221 B.')], weight=3),
    27: dict(notes=['Access control matrix: subjects × objects. Columns = ACLs (per object); rows = capability lists (per subject).'],
             exam=[mcq('In an access control matrix, a column tied to an object is a(n):', ['Access control list', 'Capability list', 'Security label', 'Ring'], 0, '')], weight=3),
    28: dict(notes=['**Take-Grant**: how rights pass between subjects (take, grant, create, remove); lets you find where rights can leak.'],
             past=[past('f221a', 'MCQ · model to find leakage of rights = take-grant')],
             exam=[mcq('Which access-control model lets you reason about rights and find whether a leakage of rights can occur?', ['Take-Grant', 'Biba', 'Clark-Wilson', 'Brewer-Nash'], 0, 'Final 221 A.')], weight=3),
    29: dict(notes=['**Bell-LaPadula** (confidentiality): no read up, no write down.'], tips=[tip(MODELS)],
             past=[past('f221b', 'Bell-LaPadula question')],
             exam=[mcq('Under Bell-LaPadula, a SECRET user may NOT:', ['Read a TOP SECRET file', 'Write to a TOP SECRET file', 'Read a CONFIDENTIAL file', 'Read a SECRET file'], 0, 'No read up.'),
                   mcq('Bell-LaPadula’s *-property forbids:', ['Writing down', 'Reading down', 'Writing up', 'Reading at the same level'], 0, '')],
             weight=3),
    30: dict(notes=['**Biba** (integrity): no read down, no write up.'], tips=[tip(MODELS)],
             exam=[mcq('The Biba model protects:', ['Integrity', 'Confidentiality', 'Availability', 'Non-repudiation'], 0, '')], weight=3),
    31: dict(notes=['End.']),
}
