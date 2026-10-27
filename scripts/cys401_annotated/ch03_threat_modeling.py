"""CYS401 annotated slides — Chapter 3: Threat Modeling.
See ch01_introduction.py for AUTO_SLIDES and the ANN keys."""
from .common import mcq, past, scen, see, short, tf, tip, trap, trick

AUTO_SLIDES = True

DECK = {
    'key': 'ch3',
    'slug': '03-threat-modeling',
    'file': 'threat-modeling',
    'title': 'Threat Modeling',
    'chapter': 'Chapter 3',
    'pdf': '/academics/cybersecurity/cys401/slides/chapter-3-threat-modeling/',
    'lede': ('Threat-modelling vocabulary (asset, threat, vulnerability, exposure, risk, control), proactive vs. '
             'reactive modelling, the ways to identify threats, the threat models (STRIDE, PASTA…), STRIDE with '
             'worked examples, and supply-chain security. A STRIDE table was a full question on Majors A, B and C.'),
}

STRIDE = ('STRIDE → property violated: Spoofing → authentication · Tampering → integrity · Repudiation → non-repudiation · '
          'Information disclosure → confidentiality · Denial of service → availability · Elevation of privilege → authorization.')

ANN = {
    1: dict(kind='title', title='Understand and Apply Threat Modeling', body=[], sub='CYS401 · Lecture 3', tips=[tip(STRIDE)]),
    2: dict(notes=['Terminology → proactive vs. reactive → identifying threats → STRIDE → supply chain.']),
    3: dict(notes=['Threat modelling: a structured process to identify assets, find threats, analyse how they could be exploited, and decide mitigations.']),
    4: dict(notes=['**Asset**: anything of value to the organization.']),
    5: dict(notes=['**Threat**: a potential occurrence that may cause harm.']),
    6: dict(notes=['**Vulnerability**: a weakness. **Exposure**: being open to asset loss through a threat.']),
    7: dict(notes=['**Risk**: likelihood that a threat exploits a vulnerability.']),
    8: dict(notes=['**Control/countermeasure/safeguard**: any action that prevents the exploit or minimizes its damage.'],
            past=[past('mA', 'identify assets, threats, vulnerabilities, controls')], weight=2),
    9: dict(notes=['Risk management reduces vulnerabilities or threat impact with controls. Risk elements: assets, threats, vulnerabilities, exposure, risk, safeguards, attack, breach.'],
            exam=[mcq('The likelihood that a threat will exploit a vulnerability and cause loss is:', ['Risk', 'Exposure', 'Asset value', 'Control'], 0, '')], weight=3),
    10: dict(notes=['Threat modelling can be proactive (during design and development) or reactive (after deployment).']),
    11: dict(notes=['Proactive = defensive approach: predict threats and design defences in. Reactive = adversarial approach: after deployment, e.g., penetration testing, fuzzing.'],
             tips=[trick('Proactive = Prevent in design. Reactive = React after release.')],
             exam=[tf('Penetration testing an already deployed system is a proactive threat modelling approach.', False, 'It is reactive (adversarial).')], weight=3),
    12: dict(notes=['Identify threats by focusing on assets, on attackers, or on software.'],
             exam=[mcq('An organization that lists likely attackers and their goals is using which threat identification focus?', ['Attacker-focused', 'Asset-focused', 'Software-focused', 'Data-focused'], 0, '')], weight=2),
    13: dict(notes=['Approaches, continued.']), 14: dict(notes=['Approaches illustrated.']),
    15: dict(notes=['Modern: system/architecture-focused (components, interactions, trust boundaries).']),
    16: dict(notes=['Data-focused: sensitive data at rest, in transit, in use. Breaches are the most common impact.']),
    17: dict(notes=['Supply chain / third-party focused: vendors, libraries, APIs.']),
    18: dict(notes=['Environment/deployment-focused: cloud, on-prem, configuration, patching, CI/CD pipelines.']),
    19: dict(notes=['Example: a university learning platform: assignments, quizzes, grades.']),
    20: dict(notes=['Three steps: identify technologies (diagram the system), identify attacks against each element, determine reduction (mitigation) analysis.']),
    21: dict(notes=['Threat models: STRIDE, PASTA, VAST, Trike, DREAD…'],
             past=[past('f221b', 'MCQ · PASTA is a risk-centric methodology')],
             exam=[mcq('PASTA aims at selecting countermeasures in relation to the value of the assets. It is a ___ methodology.', ['Risk-centric', 'Application-centric', 'Attacker-centric only', 'Hardware-centric'], 0, 'Final 221 B.')], weight=3),
    22: dict(notes=['**STRIDE** (Microsoft) classifies threats into six categories.'], tips=[tip(STRIDE)], weight=3),
    23: dict(notes=['Spoofing (falsified identity), Tampering (unauthorised change), Repudiation (denying an action), Information disclosure, Denial of service, Elevation of privilege.'],
             past=[past('mA', 'STRIDE table · threats, examples, categories'), past('mB', 'STRIDE table · properties and categories'), past('mC', 'STRIDE table · threats, properties, controls')],
             exam=[mcq('A customer denies making a transfer and there are no logs to prove otherwise. STRIDE category?', ['Repudiation', 'Spoofing', 'Tampering', 'Information disclosure'], 0, 'Major A.'),
                   mcq('Which property does Spoofing violate?', ['Authentication', 'Integrity', 'Availability', 'Authorization'], 0, 'Major C.'),
                   mcq('Elevation of privilege violates:', ['Authorization', 'Confidentiality', 'Availability', 'Non-repudiation'], 0, '')],
             weight=3),
    24: dict(notes=['Table: threat, property, example.'], tips=[tip(STRIDE)],
             exam=[short('For a mobile banking app, give one STRIDE threat example, its violated property and a mitigation for Spoofing, Tampering and Denial of service. (Major C)',
                         'Spoofing: an attacker logs in with stolen credentials → authentication → enforce MFA, strong passwords, account lockout. Tampering: a man in the middle changes the amount of a transfer → integrity → TLS for all API traffic, sign/HMAC requests. Denial of service: flooding the transaction API → availability → rate limiting, WAF rules, DDoS protection, load balancing.')],
             weight=3),
    25: dict(notes=['STRIDE example 1: a web application.']),
    26: dict(notes=['STRIDE example 2: an online banking app (transfers, balances, account updates).']),
    27: dict(notes=['STRIDE example 3.']),
    28: dict(notes=['Threat modelling in the supply chain.']),
    29: dict(notes=['A supply chain is the network between a company and its suppliers that produces and distributes a product.']),
    30: dict(notes=['A secure supply chain: reliable, trustworthy, transparent vendors.']),
    31: dict(notes=['Security assessments must cover external entities too.']),
    32: dict(notes=['Inspect connected systems: on-site assessment, document exchange and review, process/policy review, third-party audit.']),
    33: dict(notes=['End of chapter.']),
}
