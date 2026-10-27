"""Constructors for CYS406 annotated-slide content. The markup is the SE423 one (see se423_annotated/ch01_introduction.py)."""
from se423_annotated.common import mcq, scen, section, short, slide, tf, tip, trap, trick  # noqa: F401
from cs331_annotated.common import fig  # noqa: F401

# Every CYS406 deck, in course order: key -> (annotated slug, standalone file, slides folder, label).
DECKS = {
    'd01': ('01-network-security-fundamentals', 'network-security-fundamentals', 'chapter-1-network-security-fundamentals', 'Chapter 1: Network Security Fundamentals'),
    'd02': ('02-identification-authentication-and-authorization', 'identification-authentication-and-authorization', 'chapter-2-identification-authentication-and-authorization', 'Chapter 2: Identification, Authentication and Authorization'),
    'd03': ('03-cryptography-basics-des-and-aes', 'cryptography-basics-des-and-aes', 'chapter-3-cryptography-basics-des-and-aes', 'Chapter 3: Cryptography Basics (DES and AES)'),
    'd04': ('04-public-key-cryptography-and-rsa', 'public-key-cryptography-and-rsa', 'chapter-4-public-key-cryptography-and-rsa', 'Chapter 4: Public-Key Cryptography and RSA'),
    'd05': ('05-elliptic-curve-cryptography', 'elliptic-curve-cryptography', 'chapter-5-elliptic-curve-cryptography', 'Chapter 5: Elliptic Curve Cryptography'),
    'd06': ('06-rc4-and-modes-of-operation', 'rc4-and-modes-of-operation', 'chapter-6-rc4-and-modes-of-operation', 'Chapter 6: RC4 and Modes of Operation'),
    'd07': ('07-hash-functions', 'hash-functions', 'chapter-7-hash-functions', 'Chapter 7: Hash Functions'),
    'd08': ('08-diffie-hellman-key-exchange', 'diffie-hellman-key-exchange', 'chapter-8-diffie-hellman-key-exchange', 'Chapter 8: Diffie-Hellman Key Exchange'),
    'd09': ('09-key-distribution-and-management', 'key-distribution-and-management', 'chapter-9-key-distribution-and-management', 'Chapter 9: Key Distribution and Management'),
    'd10': ('10-network-security-protocols', 'network-security-protocols', 'chapter-10-network-security-protocols', 'Chapter 10: Network Security Protocols'),
    'd11': ('11-network-segmentation-and-firewalls', 'network-segmentation-and-firewalls', 'chapter-11-network-segmentation-and-firewalls', 'Chapter 11: Network Segmentation and Firewalls'),
    'd12': ('12-ids-and-ips', 'ids-and-ips', 'chapter-12-ids-and-ips', 'Chapter 12: IDS and IPS'),
    'd13': ('13-vpn-fundamentals', 'vpn-fundamentals', 'chapter-13-vpn-fundamentals', 'Chapter 13: VPN Fundamentals'),
    'd14': ('14-honeypots-and-proxy-servers', 'honeypots-and-proxy-servers', 'chapter-14-honeypots-and-proxy-servers', 'Chapter 14: Honeypots and Proxy Servers'),
    'd15': ('15-siem-and-uba', 'siem-and-uba', 'chapter-15-siem-and-uba', 'Chapter 15: SIEM and UBA'),
    'd16': ('16-data-security', 'data-security', 'chapter-16-data-security', 'Chapter 16: Data Security'),
}

# The real CYS406 papers in exams/.
PAPERS = {
}


def past(paper, label, related=False):
    assert paper in PAPERS, paper
    return {'paper': paper, 'label': label, 'related': related}


def see(deck, n, label):
    assert deck in DECKS, deck
    return {'deck': deck, 'n': n, 'label': label}
