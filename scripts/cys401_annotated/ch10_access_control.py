"""CYS401 annotated slides — Chapter 10: Authentication and Access Control (slides/chapter-10-ics-and-scada-system-security,
which holds this deck despite the folder name). See ch01_introduction.py for AUTO_SLIDES and the ANN keys."""
from .common import mcq, past, scen, see, short, tf, tip, trap, trick

AUTO_SLIDES = True

DECK = {
    'key': 'ch10',
    'slug': '11-authentication-and-access-control',
    'file': 'authentication-and-access-control',
    'title': 'Authentication and Access Control',
    'chapter': 'Chapter 10',
    'pdf': '/academics/cybersecurity/cys401/slides/chapter-10-ics-and-scada-system-security/',
    'lede': ('Identification, authentication (the three factors, biometrics and their error rates, passwords, '
             'one-time passwords) and authorization (access criteria, authorization creep, SSO), the access '
             'control models (DAC, MAC, RBAC) and techniques (rule-based, constrained interfaces, matrices), '
             'centralized administration (RADIUS, TACACS, Diameter) vs. decentralized, and accountability. Both '
             'Final 221 papers had a six-part matching question on these models. (The Slides page lists this PDF '
             'under “ICS and SCADA”.)'),
}

MODELS = ('DAC: the OWNER decides (flexible, little admin) · MAC: SECURITY LABELS and clearances decide (government) · '
          'RBAC (non-discretionary): ROLES/groups decide · Rule-based: global rules (firewalls) · Constrained UI: hide the functions a user can’t use.')

ANN = {
    1: dict(kind='title', title='Authentication and Access Control', body=[], sub='CYS401 · Chapter 10', tips=[tip(MODELS)]),
    2: dict(notes=['Access control → I/A/A → models → techniques → administration → accountability.']),
    3: dict(notes=['Access control: a technique that regulates who or what can view or use resources.']),
    4: dict(notes=['Access controls = security features that control how subjects interact with objects.']),
    5: dict(notes=['Identification, authentication and authorization are distinct.'], seen=[see('ch2', 32, 'The AAA elements')]),
    6: dict(notes=['Identification: claim an identity (username, ID).']),
    7: dict(notes=['Authentication factors: something you KNOW (password), HAVE (token), ARE (biometric).'],
             tips=[trick('Know – Have – Are.')],
             exam=[mcq('A fingerprint is which authentication factor?', ['Something you are', 'Something you know', 'Something you have', 'Somewhere you are'], 0, '')], weight=3),
    8: dict(notes=['Biometrics: fingerprint, iris, retina, face, voice, hand geometry.']),
    9: dict(notes=['Biometric errors: Type I = false rejection (FRR); Type II = false acceptance (FAR); compare systems by the CER (crossover error rate) — lower is better.'],
            exam=[mcq('A biometric system accepting someone who should have been rejected is a:', ['Type II error', 'Type I error', 'Crossover error', 'Enrolment error'], 0, ''),
                  mcq('Biometric systems are compared using the:', ['Crossover error rate', 'False rejection rate only', 'Number of users', 'Enrolment time'], 0, '')],
            weight=3),
    10: dict(notes=['Passwords: the most common method and the weakest; enforce length, complexity, history, lockout.']),
    11: dict(notes=['One-time (dynamic) passwords: used once (tokens, SMS codes).']),
    12: dict(notes=['Authorization: what an authenticated subject is allowed to do.']),
    13: dict(notes=['Access criteria: roles, groups, location, time, transaction type.'],
             past=[past('f221b', 'MCQ · controlling data access during certain functions', related=True)]),
    14: dict(notes=['**Authorization creep**: new rights are added without removing old ones. Also need-to-know, least privilege, default no access.'],
             past=[past('f221a', 'MCQ · new rights without removing old = authorization creep')],
             exam=[mcq('An employee gets new access rights without the old ones being reviewed and removed. This is:', ['Authorization creep', 'Least privilege', 'Separation of duties', 'Need to know'], 0, 'Final 221 A.')], weight=3),
    15: dict(notes=['**SSO**: enter credentials once, access all authorized systems.'],
             past=[past('f221a', 'MCQ · one login for all services = SSO'), past('f221b', 'MCQ · a type of SSO')],
             exam=[mcq('A separate authentication server validates the login once and the user reaches all services without logging in again. This is:', ['Single sign-on', 'Multifactor authentication', 'Federation only', 'Kerberos tickets only'], 0, 'Final 221 A.')], weight=3),
    16: dict(notes=['SSO process: log on to the authentication server, then access other systems without re-authenticating (e.g., Kerberos).']),
    17: dict(notes=['SSO pros: fewer passwords, convenience. Cons: one compromised credential opens everything (single point of failure).'],
             exam=[short('Give one advantage and one disadvantage of SSO.', 'Advantage: users remember one strong credential and log in once, reducing password fatigue and admin work. Disadvantage: if that one credential (or the authentication server) is compromised, the attacker gets access to every system.')], weight=2),
    18: dict(notes=['Three main models: discretionary (DAC), mandatory (MAC), non-discretionary / role-based (RBAC).'], tips=[tip(MODELS)],
             past=[past('f221a', 'Q1 Part 2 · match access-control concepts', question={
                       'prompt': 'Choose the concept that matches each description. An option may be used twice.',
                       'items': [
                           "As the sole owner of a very small startup's website, with no assistance, you monitor user registrations and grant access based on what you think is good for your company.",
                           'You are the security admin in a ministry responsible for a classified resource, and you assign internal users based on their security clearance levels.',
                           "As an LMS admin you ensure that the 'edit' buttons for creating a quiz only appear according to the user's privilege.",
                           "In a supermarket, the cashier needs the supervisor's approval to cancel a bill and refund a customer, following a predefined refund policy.",
                           'A small business has 10 computers in a peer-to-peer network. All users are responsible for their own security and set file and folder privileges as they see fit.',
                           'Filtering traffic in a firewall to block blacklisted websites based on preconfigured rules.',
                       ],
                       'choices': ['Discretionary Access Control', 'Non-Discretionary Access', 'Rule-based Access Control', 'Mandatory Access Control', 'Role-based Access Control', 'Constrained User Interfaces'],
                   }),
                   past('f221b', 'Q1 Part 2 · match access-control concepts', question={
                       'prompt': 'Answer each description by choosing the appropriate option. An option may be used twice.',
                       'items': [
                           "Data has a 'top secret' confidentiality level and an 'engineering project' security label, and is available only to users with both top secret clearance and authorization for engineering documents.",
                           'This model is popular because it allows users a lot of freedom to choose access rights and causes little administrative overhead.',
                           'Computer-system managers use these controls to decide who can get into a system and what tasks they can perform.',
                           'As an administrator you designate user groups such as staff, specialists or end users, and limit access to specific resources or tasks.',
                           "Restrict users' abilities by not allowing them certain types of access or the ability to request certain functions or information.",
                           'What type of access control has been used in MAC systems as an enforcement mechanism?',
                       ],
                       'choices': ['Discretionary Access Control', 'Non-Discretionary Access', 'Rule-based Access Control', 'Mandatory Access Control', 'Logical Access Control', 'Constrained User Interfaces'],
                   })],
             exam=[mcq('The sole owner of a small startup website grants access based on what they think is good. This is:', ['Discretionary Access Control', 'Mandatory Access Control', 'Role-based Access Control', 'Rule-based Access Control'], 0, 'Final 221 A.'),
                   mcq('A ministry admin assigns users to a classified resource by their security clearance. This is:', ['Mandatory Access Control', 'Discretionary Access Control', 'Role-based Access Control', 'Constrained user interface'], 0, 'Final 221 A.'),
                   mcq('An admin defines groups such as staff and specialists and limits access by group. This is:', ['Role-based Access Control', 'Mandatory Access Control', 'Discretionary Access Control', 'Rule-based Access Control'], 0, 'Final 221 B.')],
             weight=3),
    19: dict(notes=['MAC: access decided by labels (classification + categories) and clearances; users can’t change it.'],
             past=[past('f221b', 'match · top secret + engineering label')],
             exam=[mcq('Data labelled “top secret / engineering project” is available only to users with top-secret clearance AND engineering authorization. Which model?', ['Mandatory Access Control', 'Discretionary Access Control', 'Role-based Access Control', 'Constrained user interface'], 0, 'Final 221 B.')], weight=3),
    20: dict(notes=['Techniques: rule-based access control, constrained user interfaces, access control matrix, content- and context-dependent control.']),
    21: dict(notes=['Rule-based: global rules (not identity-based) decide what can happen, e.g., firewall rules.']),
    22: dict(notes=['Constrained user interfaces: restrict what users can request by hiding functions (greyed-out menus, views).'],
             past=[past('f221a', 'match · LMS shows edit buttons by privilege'), past('f221b', 'match · restrict users by not allowing certain functions')],
             exam=[mcq('An LMS shows the quiz “edit” buttons only to users with that privilege. This is:', ['Constrained user interface', 'Discretionary Access Control', 'Mandatory Access Control', 'Rule-based Access Control'], 0, 'Final 221 A.')], weight=3),
    23: dict(notes=['Access control matrix: what each subject can do to each object.']),
    24: dict(notes=['Capability tables (rows, tied to subjects) vs. ACLs (columns, tied to objects).'], seen=[see('ch7', 27, 'Access control matrix')]),
    25: dict(notes=['Centralized administration: one entity manages access for all resources: consistent and uniform.']),
    26: dict(notes=['**RADIUS**: centralized authentication for remote/dial-in users; UDP, encrypts only the password.']),
    27: dict(notes=['**TACACS+**: Cisco; TCP, encrypts the whole payload, separates authentication, authorization and accounting.'],
             exam=[mcq('Which encrypts the entire packet body and separates AAA functions?', ['TACACS+', 'RADIUS', 'Diameter', 'LDAP'], 0, '')], weight=3),
    28: dict(notes=['RADIUS vs. TACACS+ comparison.']),
    29: dict(notes=['Diameter: builds on RADIUS and fixes its limitations (more reliable, extensible).']),
    30: dict(notes=['Decentralized administration: control is given to people closer to the resources; lacks consistency.'],
             past=[past('f221b', 'MCQ · control near the resources, lacks consistency')],
             exam=[mcq('Which gives control of access to the people closest to the resources but lacks consistency?', ['Decentralized access control', 'Centralized access control', 'Subject-oriented capability table', 'Object-oriented capability table'], 0, 'Final 221 B.')], weight=3),
    31: dict(notes=['Accountability: record user, system and application activity; review audit logs.']),
    32: dict(notes=['Keystroke monitoring, protecting audit data, clipping levels.']),
    33: dict(notes=['Best practices: least privilege, deny by default, review accounts, remove unused accounts, separate duties.']),
    34: dict(notes=['RADIUS flow figure.']), 35: dict(notes=['End.']),
}
