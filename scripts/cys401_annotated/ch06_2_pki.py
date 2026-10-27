"""CYS401 annotated slides — Chapter 6.2: Public Key Infrastructure.
See ch01_introduction.py for AUTO_SLIDES and the ANN keys."""
from .common import mcq, past, scen, see, short, tf, tip, trap, trick

AUTO_SLIDES = True

DECK = {
    'key': 'ch6.2',
    'slug': '07-asymmetric-cryptography-and-pki-part-2',
    'file': 'asymmetric-cryptography-and-pki-part-2',
    'title': 'Public Key Infrastructure',
    'chapter': 'Chapter 6.2',
    'pdf': '/academics/cybersecurity/cys401/slides/chapter-6-2-asymmetric-cryptography-and-pki/',
    'lede': ('Why PKI is needed (can you trust a public key?), digital certificates (X.509), the certificate life '
             'cycle and revocation lists, the PKI players (CA, RA, repositories), certificate policy, and '
             'certificates in SSL/TLS. Final 221 B asked where to find revoked certificates and which keys sign '
             'and validate an X.509 certificate.'),
}

ANN = {
    1: dict(kind='title', title='Public Key Infrastructure', body=[], sub='CYS401 · Lecture 6.2'),
    2: dict(notes=['PKI overview, digital signatures, certificates.']),
    3: dict(notes=['Security issues: privacy (interception), integrity (modification), authentication (impersonation), non-repudiation.'], seen=[see('ch2', 29, 'Integrity methods')]),
    4: dict(notes=['The critical question: how do I KNOW a public key really belongs to that person? → certificates from a trusted CA.'], weight=2),
    5: dict(notes=['Receiver’s public and private key in use.']),
    6: dict(notes=['A digital certificate binds an identity to a public key, signed by a CA.']),
    7: dict(notes=['Certificate contents.']),
    8: dict(notes=['X.509 certificate: owner, issuer (CA), validity, public key, signed by the CA. The CA signs with ITS private key; anyone validates with the CA’s public key.'],
             past=[past('f221b', 'written · keys for issuing and validating an X.509 certificate')],
             exam=[short('Which keys are used to issue and validate an X.509 certificate, and who issues it? (Final 221 B)', 'The Certificate Authority issues it and signs it with the CA’s private key; anyone validates the signature with the CA’s public key.')],
             weight=3),
    9: dict(notes=['Life cycle states: in use (valid), expired, revoked (e.g., the private key was compromised).']),
    10: dict(notes=['CRL (Certificate Revocation List): published periodically by the CA (X.509). Also OCSP for online checks.'],
             past=[past('f221b', 'written · where to search for a revoked certificate'), past('m181', 'MCQ · why a CA revokes a certificate'), past('f221b', 'MCQ · reason not appropriate for revocation')],
             exam=[short('Where can you search for a revoked certificate? (Final 221 B)', 'In the Certificate Revocation List (CRL) that the CA periodically publishes (or by querying the CA’s OCSP responder).'),
                   mcq('A CA revokes a user’s certificate when:', ['The user’s private key is compromised', 'The user moves to a new location', 'The user’s public key is published', 'The user switches browsers'], 0, 'Major 181.')],
             weight=3),
    11: dict(notes=['A real certificate viewed in a browser.']),
    12: dict(notes=['PKI players: RA (verifies identity, approves), CA (issues certificates and CRLs), repositories, users.'],
             exam=[mcq('Which PKI component verifies a user’s identity before a certificate is issued?', ['Registration Authority', 'Certificate Authority', 'Repository', 'Relying party'], 0, '')], weight=3),
    13: dict(notes=['CA: the trusted third party that issues, signs and revokes certificates.']),
    14: dict(notes=['RA: enrols and de-enrols subscribers, validates applications.']),
    15: dict(notes=['Certificate Policy: the basis for trust between unrelated parties.']),
    16: dict(notes=['Public-key security relies on the private key staying private.']),
    17: dict(notes=['Certificates in SSL/TLS: the server sends its certificate; the browser checks it against trusted CAs.']),
    18: dict(notes=['TLS handshake uses the certificate to set up a shared symmetric session key (hybrid encryption).'],
             past=[past('f221b', 'MCQ · S/MIME relies on certificates', related=True)]),
    19: dict(notes=['End.']),
}
