"""CYS401 annotated slides — Chapter 6.1: asymmetric cryptography, RSA and hashing.
See ch01_introduction.py for AUTO_SLIDES and the ANN keys."""
from .common import mcq, past, scen, see, short, tf, tip, trap, trick

AUTO_SLIDES = True

DECK = {
    'key': 'ch6.1',
    'slug': '06-asymmetric-cryptography-and-pki-part-1',
    'file': 'asymmetric-cryptography-and-pki-part-1',
    'title': 'Asymmetric Cryptography: RSA and Hash Functions',
    'chapter': 'Chapter 6.1',
    'pdf': '/academics/cybersecurity/cys401/slides/chapter-6-1-asymmetric-cryptography-and-pki/',
    'lede': ('Symmetric vs. asymmetric, public and private keys, trapdoor one-way functions, RSA (key generation, '
             'encryption, decryption, signatures, worked examples), and hash functions (SHA, MD, collisions) vs. '
             'MACs vs. signatures. Final 221 B and Major 181 asked about keys, signatures and hash lengths.'),
}

RSA = 'RSA in 5 lines: pick primes p, q · n = p·q · φ(n) = (p−1)(q−1) · pick e coprime with φ(n) · d = e⁻¹ mod φ(n). Encrypt C = Mᵉ mod n; decrypt M = Cᵈ mod n.'
KEYS = 'Which key? ENCRYPT for confidentiality with the RECEIVER’s public key (receiver decrypts with their private key). SIGN with the SENDER’s private key (anyone verifies with the sender’s public key).'

ANN = {
    1: dict(kind='title', title='Encryption and Cryptography (2)', body=[], sub='CYS401 · Lecture 6.1', tips=[tip(KEYS)]),
    2: dict(notes=['Symmetric vs. asymmetric → RSA → hashes.']),
    3: dict(notes=['Objectives.']),
    4: dict(notes=['Symmetric: one shared key, fast, key distribution problem. Asymmetric: key pair, slower, solves key exchange and enables signatures.'],
            exam=[mcq('Compared with symmetric encryption, asymmetric encryption is:', ['Slower but solves key distribution', 'Faster and needs one key', 'Unable to sign messages', 'Only for hashing'], 0, '')], weight=3),
    5: dict(notes=['Comparison table, continued.']),
    6: dict(notes=['Asymmetric crypto gives confidentiality, authentication, or both; separate keys for encryption and decryption.']),
    7: dict(notes=['Two keys: the public key (shared) and the private key (secret).'], tips=[tip(KEYS)],
            past=[past('m181', 'MCQ · how the two keys relate'), past('f221a', 'MCQ · which key decrypts the sports channel', related=True)],
            exam=[mcq('Which statement about an asymmetric key pair is correct?', ['Whatever one key encrypts, only the other key can decrypt', 'Only the private key can encrypt', 'Only the public key can encrypt', 'The public key both encrypts and decrypts'], 0, 'Major 181.')],
            weight=3),
    8: dict(notes=['General idea: C = f(K_public, P); P = g(K_private, C).']),
    9: dict(notes=['Trapdoor one-way function: easy to compute, infeasible to invert without the trapdoor (the private key).'],
            exam=[mcq('The core idea behind public-key cryptography is the:', ['Trapdoor one-way function', 'Caesar shift', 'Feistel network', 'XOR keystream'], 0, '')], weight=2),
    10: dict(notes=['RSA (Rivest, Shamir, Adleman), the most common public-key algorithm, based on factoring large primes.']),
    11: dict(notes=['RSA encryption: C = Mᵉ mod n (public key e, n).']),
    12: dict(notes=['RSA decryption: M = Cᵈ mod n (private key d).']),
    13: dict(notes=['Encryption and decryption together.']),
    14: dict(notes=['Key generation steps.'], tips=[tip(RSA)],
             exam=[mcq('With p = 5, q = 11, φ(n) equals:', ['40', '55', '54', '16'], 0, '(5 − 1)(11 − 1) = 40.'),
                   mcq('With p = 5, q = 11 and e = 7, the private exponent d is:', ['23', '7', '17', '33'], 0, '7 × 23 = 161 = 4 × 40 + 1.')],
             weight=3),
    15: dict(notes=['RSA procedure figure.']),
    16: dict(notes=['Extended Euclid to find d with e·d mod φ(n) = 1. Example p = 5, q = 11, e = 7 → n = 55, φ = 40, d = 23.']),
    17: dict(notes=['RSA application.']),
    18: dict(notes=['Example 1: p = 7, q = 11 → n = 77, φ = 60, e = 13, d = 37.']),
    19: dict(notes=['Example 2: p = 3, q = 11 → n = 33, φ = 20, e = 7, d = 3.'],
             exam=[short('RSA with p = 3, q = 11, e = 7. Find n, φ(n), d, and encrypt M = 2.', 'n = 33, φ(n) = 20, d = 3 (7 × 3 = 21 ≡ 1 mod 20). C = 2⁷ mod 33 = 128 mod 33 = 29. Check: 29³ mod 33 = 2.')],
             weight=3),
    20: dict(notes=['Homework: find the key pair for given factors.']),
    21: dict(notes=['Encryption vs. signature.']), 22: dict(notes=['Encryption vs. signature, continued.']),
    23: dict(notes=['Encrypt with the public key, decrypt with the private key. Sign with the private key, verify with the public key.'], tips=[tip(KEYS)],
             past=[past('m181', 'MCQ · digital signature uses the sender’s private key')],
             exam=[mcq('A digital signature is created by encrypting the message digest with:', ['The sender’s private key', 'The receiver’s public key', 'The receiver’s private key', 'The sender’s public key'], 0, 'Major 181.')], weight=3),
    24: dict(notes=['Signature example: p = 7, q = 13, n = 91, φ = 72, e = 5, d = 29.']),
    25: dict(notes=['RSA security rests on how hard it is to factor n; key sizes keep growing (2048+ bits).']),
    26: dict(kind='section', title='Data Integrity: Hash Functions'),
    27: dict(notes=['A hash maps any input to a fixed-length digest; one-way (you can’t get the plaintext back).']),
    28: dict(notes=['Uses: storing passwords, integrity checks, signatures.'],
             past=[past('f221b', 'written · two differences between hashing and encryption')],
             exam=[short('How is hashing different from encryption? Give two differences. (Final 221 B)', 'Hashing is one-way (no key, cannot be reversed) while encryption is reversible with a key; a hash always has a fixed-length output, while ciphertext length depends on the input.')],
             weight=3),
    29: dict(notes=['Hash (no key, integrity only) vs. MAC (shared key: integrity + authenticity).']),
    30: dict(notes=['Collision attack: two different messages with the same hash.']),
    31: dict(notes=['SHA (NSA, NIST standard). SHA-1: 160-bit digest. SHA-2: 224–512. SHA-3: 224, 256, 384, 512 with a different internal structure (Keccak).'],
             past=[past('f221b', 'MCQ · SHA-3 hash lengths')],
             exam=[mcq('SHA-1 produces a digest of:', ['160 bits', '128 bits', '256 bits', '512 bits'], 0, '')], weight=3),
    32: dict(notes=['MD (Message Digest) family: 128-bit hashes. MD4 is older and LESS secure than MD5.'],
             past=[past('f221b', 'MCQ · MD4 is older and less secure than MD5')],
             exam=[mcq('MD5 produces a hash of:', ['128 bits', '160 bits', '256 bits', '64 bits'], 0, '')], weight=3),
    33: dict(notes=['Try hashing text online.']),
    34: dict(notes=['Hash = integrity. MAC = integrity + authentication (shared key). Signature = integrity + authentication + non-repudiation (private key).'],
             exam=[mcq('Which provides non-repudiation?', ['A digital signature', 'A hash', 'A MAC', 'Symmetric encryption'], 0, '')], weight=3),
    35: dict(notes=['Comparison continued.']), 36: dict(notes=['Summary.']), 37: dict(notes=['End.'], seen=[see('ch6.2', 6, 'Digital certificates and PKI')]),
}
