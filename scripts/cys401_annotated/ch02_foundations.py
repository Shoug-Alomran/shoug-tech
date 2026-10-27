"""CYS401 annotated slides — Chapter 2: Security Foundations and Principles.
See ch01_introduction.py for AUTO_SLIDES and the ANN keys."""
from .common import mcq, past, scen, see, short, tf, tip, trap, trick

AUTO_SLIDES = True

DECK = {
    'key': 'ch2',
    'slug': '02-security-foundations-and-principles',
    'file': 'security-foundations-and-principles',
    'title': 'Security Foundations and Principles',
    'chapter': 'Chapter 2',
    'pdf': '/academics/cybersecurity/cys401/slides/chapter-2-security-foundations-and-principles/',
    'lede': ('The three pillars, vulnerability vs. threat vs. risk, malware and the threat landscape, social '
             'engineering (phishing, spear phishing, tailgating), the C.I.A. triad with the attacks on each and '
             'the methods that protect it, the AAA services, and the protection mechanisms. Final 221 A/B, Quiz '
             '1 222 and Majors A–C all draw on this deck.'),
}

AAA = ('AAA = five elements: Identification (claim) → Authentication (prove) → Authorization (permissions) → Auditing (record) → Accounting (hold responsible). '
       'Phase 1 (getting in): identification, authentication, authorization. Phase 2 (afterwards): auditing, accountability.')

ANN = {
    1: dict(kind='title', title='Cyber Security Foundations and Principles', body=[], sub='CYS401 · Lecture 2', tips=[tip(AAA)]),
    2: dict(notes=['The three CYS pillars: **people, policies (processes), technology**.'],
            past=[past('f221a', 'MCQ · all are pillars except')],
            exam=[mcq('All of the following are cybersecurity pillars EXCEPT:', ['Profit', 'People', 'Policies/processes', 'Technology'], 0, 'Final 221 A.')], weight=3),
    3: dict(notes=['Three entities to protect: endpoint devices, networks, and the cloud/data.']),
    4: dict(notes=['**Vulnerability** = a weakness that can be exploited. **Threat** = circumstances with the potential to cause harm. **Countermeasure** = a control that removes or reduces the vulnerability.'],
            tips=[trap('“Data breach” is a threat or an impact, never a vulnerability. A vulnerability is the WEAKNESS (weak passwords, misconfigured buckets).')],
            past=[past('mA', 'scenario · two assets, threats and vulnerabilities')],
            exam=[mcq('A misconfigured, publicly accessible storage bucket is a(n):', ['Vulnerability', 'Threat', 'Asset', 'Control'], 0, 'Major A.'),
                  mcq('A ransomware attacker who could exploit weak passwords is a(n):', ['Threat', 'Vulnerability', 'Asset', 'Countermeasure'], 0, 'Major A.')],
            weight=3),
    5: dict(notes=['Risk exists only when a threat meets a vulnerability.'], tips=[trick('Risk = threat × vulnerability (× impact).')], weight=2),
    6: dict(notes=['Types of threat damage.']),
    7: dict(notes=['Threats overview.']),
    8: dict(notes=['Common threats (Get Cyber Safe list).']),
    9: dict(notes=['Modern landscape: supply-chain and third-party threats (compromised vendors, malicious updates) are external human threats with indirect access.']),
    10: dict(notes=['Vectors: malware, ransomware, social engineering, phishing, DDoS, insider threats…']),
    11: dict(notes=['Malware types: virus, worm, Trojan, spyware, adware, rootkit, ransomware.']),
    12: dict(notes=['Symptoms: high CPU, slow browser, network problems, freezing, unknown programs, pop-ups.']),
    13: dict(notes=['Countermeasures: good antivirus with updated definitions, don’t open untrusted attachments, patch, back up.']),
    14: dict(notes=['**Ransomware**: socially engineered malware that locks or encrypts data and demands payment.'],
             past=[past('f221a', 'MCQ · malware asking the victim to pay')],
             exam=[mcq('Social-engineering-based malware that demands payment to unlock or decrypt data is:', ['Ransomware', 'Spyware', 'Adware', 'A worm'], 0, 'Final 221 A.')], weight=3),
    15: dict(notes=['Social engineering tricks people. Phishing: fake emails from reputable-looking sources. **Spear phishing/whaling**: targeted at a specific person or organization.'],
             past=[past('f221a', 'MCQ · emails targeting you specifically = spear phishing')],
             exam=[mcq('Frequent emails impersonating your bank, crafted to convince YOU specifically to give your credentials, are:', ['Spear phishing', 'Spam', 'Vishing', 'Pharming'], 0, 'Final 221 A.')], weight=3),
    16: dict(notes=['More social engineering: vishing, smishing, baiting, pretexting, tailgating.'],
             past=[past('mB', 'A · following someone through a door = tailgating')],
             exam=[mcq('Following an authorised person through a secured door without authenticating is:', ['Tailgating', 'Phishing', 'Doxing', 'Whaling'], 0, 'Major B.')], weight=3),
    17: dict(notes=['Doxing: publishing private information about someone.']),
    18: dict(notes=['Social engineering countermeasures: password policies (change, complexity), physical security, training.']),
    19: dict(notes=['Training, operational guidelines, information classification (top secret, proprietary, internal, public).']),
    20: dict(notes=['AI-driven threats: AI-generated malware, deepfakes, automated phishing.']),
    21: dict(notes=['Threats exist at every level: personal, enterprise, Internet of Things, critical infrastructure.']),
    22: dict(notes=['**C.I.A.**: confidentiality (secrets stay secret), integrity (accurate, unmodified), availability (accessible when needed).'],
             seen=[see('ch1', 14, 'C.I.A. definitions')], weight=3),
    23: dict(notes=['Confidentiality controls: encryption, access control, steganography.']),
    24: dict(notes=['Attacks on confidentiality: stealing password files, port scanning, social engineering.']),
    25: dict(notes=['Eavesdropping (man in the middle), sniffing, privilege escalation.']),
    26: dict(notes=['Ensure confidentiality: encryption, user IDs and passwords, 2FA, biometrics.']),
    27: dict(notes=['Soft tokens, key fobs (2FA/MFA), and storing sensitive documents offline.'],
             past=[past('mB', 'A · what stops access even with a stolen password = MFA')],
             exam=[mcq('Which control still blocks access when a user’s password is stolen?', ['Two-factor / multifactor authentication', 'Longer passwords', 'Port scanning', 'Steganography'], 0, 'Major B.')], weight=3),
    28: dict(notes=['Integrity: reliable and accurate information. Attacks: viruses, logic bombs, unauthorised access. Controls: file permissions, user access controls, version control.']),
    29: dict(notes=['Ensure integrity: cryptographic checksums (hashes), digital signatures, backups.'], seen=[see('ch6.2', 3, 'Hashing')]),
    30: dict(notes=['Availability threats: device failure, software errors, environment (heat, floods, power), DoS. Prevent data loss: backups, redundancy, disaster recovery.'],
             past=[past('f221b', 'MCQ · backups restore lost data'), past('q222', 'Q2 · availability calculation'), past('f221a', 'MCQ · attack making assets unavailable', related=True)],
             exam=[mcq('An attack that makes company assets unusable or unavailable is a(n):', ['Denial-of-service attack', 'Eavesdropping attack', 'Spoofing attack', 'Sniffing attack'], 0, 'Final 221 A.'),
                   short('A system is offline 2 h 20 min a week for 13 weeks for testing. What is its availability over those 13 weeks (1 d.p.)? (Quiz 1 222 style)', 'Downtime = 140 min × 13 = 1820 min. Total time = 13 weeks × 7 × 24 × 60 = 131,040 min. Availability = (131,040 − 1,820) / 131,040 = 98.6%.')],
             weight=3),
    31: dict(notes=['Beyond C.I.A.: the AAA services.'], tips=[tip(AAA)]),
    32: dict(notes=['Identification (claim), authentication (prove), authorization (permissions), auditing (record activity), accounting/accountability (hold responsible).'],
             past=[past('f221b', 'written · the two phases of IAAA')],
             exam=[short('Identification, authentication, authorization and accountability are divided into two phases. What are they? (Final 221 B)', 'Phase 1, gaining access: identification, authentication and authorization. Phase 2, after access: auditing and accountability (accounting), which record and tie actions to the user.'),
                   mcq('Proving that you are the identity you claimed is:', ['Authentication', 'Identification', 'Authorization', 'Accounting'], 0, '')],
             weight=3),
    33: dict(notes=['Protection mechanisms: layering (defence in depth), abstraction, data hiding, encryption.']),
    34: dict(notes=['Data hiding: keep data out of reach of unauthorised subjects. Encryption: hide the meaning of a communication.']),
}
