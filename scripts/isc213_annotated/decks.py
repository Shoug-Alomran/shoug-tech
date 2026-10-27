"""ISC213 annotated slides — every Islamic Financial Transactions lecture.

Midterm 1 covers Lectures 1–4 and Midterm 2 covers Lectures 5–9. The Arabic quotations don't survive text
extraction, so every slide is shown as the original image (whole=True) with the notes beside it. Each deck
is a namespace class built by lecture(); see cs331_annotated/ch01_1_introduction.py for the ANN keys."""
from .common import DECKS, mcq, past, see, short, tf, tip, trap, trick


def lecture(key, count, lede, ann, exams):
    slug, file, folder, label = DECKS[key]
    head, title = label.split(': ', 1)
    ann = {n: dict(a, whole=True) for n, a in ann.items()}
    ann.setdefault(1, {'whole': True})
    ann[1]['past'] = ann[1].get('past', []) + [past(p, 'examined on this paper', related=True) for p in exams]
    return type(key, (), {
        'AUTO_SLIDES': True,
        'DECK': {'key': key, 'slug': slug, 'file': file, 'title': title, 'chapter': head,
                 'pdf': '/academics/other-courses/isc213/slides/%s/' % folder, 'lede': lede},
        'ANN': {n: ann.get(n, {'whole': True}) for n in range(1, count + 1)},
    })


MID1 = ('mid1', 'mid1c')
MID2 = ('mid2',)

transactions = lecture('d01', 6, 'The concept of contemporary financial transactions, how they are defined, the characteristics of transactions in Islamic jurisprudence, and their goal of protecting wealth.', {
    2: dict(notes=['Transactions: the Shari’a rules regulating financial dealings between people. Contemporary: cases that arose in the modern age and were unknown to earlier jurists (companies, banknotes…).']),
    4: dict(notes=['Characteristics: built on general principles; the default ruling of transactions is PERMISSIBILITY unless evidence forbids; they consider benefit and justice.'],
            tips=[trick('Worship: forbidden unless prescribed. Transactions: permitted unless prohibited.')],
            exam=[mcq('The default ruling in financial transactions is:', ['Permissibility', 'Prohibition', 'Obligation', 'Dislike'], 0, '')], weight=3),
    6: dict(notes=['Goal: preserve wealth (one of the five necessities): forbid unlawful gain (theft, riba) and encourage growth through investment and contracts.']),
}, MID1)

rights = lecture('d02', 4, 'The qualifications and steps for issuing a ruling on a contemporary case (ijtihad), and the definition and types of rights (political and civil).', {
    1: dict(notes=['The researcher must be qualified for ijtihad and devote time to the contemporary case.']),
    2: dict(notes=['Steps: pray for guidance, understand the case deeply (consult specialists), search the legal sources and similar cases, then issue the ruling.'],
            exam=[short('List the steps a scholar follows to reach a ruling on a contemporary case.', 'Ask Allah for guidance; understand the case thoroughly (consulting experts); search the Qur’an, Sunnah and earlier jurisprudence for it or similar cases (analogy); then form and state the ruling.')], weight=3),
    3: dict(notes=['Right: an entitlement established by Shari’a giving authority or imposing an obligation. Types: political and civil (public and private).']),
}, MID1)

incorporeal = lecture('d03', 8, 'Incorporeal (intellectual) rights: authorship rights, patents, trade names, their definitions and Shari’a rulings, and their basis (benefits are compensable).', {
    1: dict(notes=['Incorporeal right: authority over something intangible (a work, an invention, a name). Property in fiqh is not limited to physical objects.']),
    2: dict(notes=['Author: whoever created the work; the person named on it is presumed the author.']),
    3: dict(notes=['Ruling: authorship rights are recognized and can be compensated with money: benefits count as property, custom recognizes them, and they serve society.'],
            exam=[tf('In Islamic jurisprudence, intellectual property rights can have financial value.', True, 'Benefits are compensable.')], weight=3),
    4: dict(notes=['Patent: the legal right to exclude others from making/using/selling an invention for a limited time; recognized in Shari’a.']),
    6: dict(notes=['Trade name: the official name under which a business operates; it is an exclusive, transferable asset.']),
}, MID1)

insurance = lecture('d04', 9, 'Collaborative (cooperative/takaful) insurance and its legitimacy, commercial insurance and its types, why commercial insurance is prohibited (gharar, gambling, riba), and the exceptions.', {
    2: dict(notes=['Collaborative (cooperative) insurance: members donate to a common fund that compensates whoever is harmed: based on “cooperate in righteousness and piety.” The Ash’arites shared their food equally.'],
            exam=[mcq('Cooperative (takaful) insurance is permissible because it is based on:', ['Donation and mutual support', 'Profit from premiums', 'Interest', 'Gambling on risk'], 0, '')], weight=3),
    5: dict(notes=['Commercial insurance: a compensation contract with a profit-making company; the insured pays premiums, the company pays on the insured event.']),
    7: dict(notes=['Prohibited because of excessive uncertainty (gharar), gambling (maysir), and both kinds of riba (paying more = riba al-fadl; with delay = riba al-nasi’ah).'],
            tips=[trap('Commercial = compensation contract for profit (prohibited); cooperative = donation contract (permitted).')],
            exam=[short('Give two reasons why commercial insurance is prohibited.', 'It contains excessive uncertainty (gharar) about whether and how much will be paid; it resembles gambling; and it involves riba, since the payout can exceed what was paid and is delayed.')], weight=3),
    8: dict(notes=['Exceptions: insurance that is a dependent add-on to another contract (a plane ticket or car rental) or legally compulsory.']),
}, MID1)

securities = lecture('d05', 3, 'Securities (shares and bonds), the stock exchange (brokers and dealers), and how it differs from a regular market.', {
    1: dict(notes=['Security: a financial instrument representing ownership (shares) or a loan (bonds), issued by companies or governments and traded on the stock exchange.']),
    2: dict(notes=['Stock exchange (bourse): marketplace where brokers trade for clients and dealers trade for their own account.']),
    3: dict(notes=['Unlike a regular market, goods aren’t present or inspected, and many trades are speculative rather than real exchanges.'],
            exam=[mcq('A broker in the stock exchange trades:', ['On behalf of clients', 'Only for his own account', 'Only government bonds', 'Only commodities'], 0, '')], weight=3),
}, MID2)

shares = lecture('d06', 4, 'Shares as units of ownership, classifications by rights (ordinary, preferred) and by recouping value, and the Shari’a ruling on dealing in shares.', {
    1: dict(notes=['Share: an equal, indivisible, tradable unit of ownership in a company’s capital.']),
    2: dict(notes=['Ordinary shares: equal rights (to stay, vote, profits, assets at liquidation). Preferred shares give special privileges.'],
            exam=[mcq('Preferred shares that guarantee a fixed profit regardless of results are:', ['Not permissible', 'Permissible', 'Recommended', 'Only for governments'], 0, 'A guaranteed return is riba.')], weight=3),
    4: dict(notes=['Dealing in shares is permissible when the company’s activity is lawful (halal), shares carry no guaranteed fixed return, and trading is real, not interest-based.'], weight=3),
}, MID2)

bonds = lecture('d07', 4, 'Bonds as interest-bearing loans, prize bonds and treasury bills, bonds vs. shares, and the lawful alternatives for companies and governments.', {
    1: dict(notes=['Bonds: tradable deeds representing long-term loans with a fixed return: interest, so they are prohibited.']),
    3: dict(notes=['Bond vs. share: a bond is a DEBT on the company with a fixed return whether it profits or not; a share is a PART of the capital sharing profit and loss.'],
            tips=[trick('Bondholder = lender (fixed interest); shareholder = owner (profit and loss).')],
            exam=[mcq('Which is TRUE?', ['A bondholder is a creditor; a shareholder is an owner', 'Both are owners', 'Both are creditors', 'A shareholder gets a fixed return'], 0, '')], weight=3),
    4: dict(notes=['Alternatives: companies issue new shares or form partnerships; governments use lawful revenue, sukuk and similar instruments instead of interest-bearing debt.']),
}, MID2)

lease = lecture('d08', 3, 'Ijarah (leasing), the lease ending with ownership transfer, how it differs from an installment sale, and the problems that make some forms impermissible.', {
    1: dict(notes=['Ijarah: a contract transferring a known benefit of an asset for a set period and payment.']),
    2: dict(notes=['Installment sale: ONE contract, ownership passes immediately, payment deferred. Lease ending with ownership: a lease contract PLUS a separate promise of transfer at the end.'],
            exam=[short('How does an installment sale differ from a lease ending with ownership?', 'In an installment sale ownership transfers immediately under one sale contract and only payment is deferred. In a lease ending with ownership the asset stays the lessor’s during a lease contract, and ownership passes at the end under a separate contract or promise.')], weight=3),
    3: dict(notes=['Problems: inflated rent above market value, the lessee may lose both payments and asset, and mixing two contracts makes the reality unclear; it is permissible only if the contracts are kept separate with fair terms.']),
}, MID2)

murabaha = lecture('d09', 3, 'Sale contracts, salam (advance payment), and murabaha for the purchase orderer as practised by Islamic banks, with its conditions.', {
    1: dict(notes=['Sale is permissible: “Allah has permitted trade and forbidden riba.”']),
    2: dict(notes=['Salam: pay now for goods delivered later, with known quantity, quality and date.']),
    3: dict(notes=['Murabaha for the purchase orderer: the bank buys and OWNS the item, then sells it to the client at cost plus a known profit, paid now or in installments.'],
            tips=[trap('The bank must own and possess the item before selling it, and the installment price can’t increase for late payment.')],
            exam=[mcq('In a valid murabaha, the bank must:', ['Own the item before selling it to the client', 'Lend cash to the client', 'Charge extra for every late payment', 'Sell before buying'], 0, '')], weight=3),
}, MID2)

DECKS_HERE = [transactions, rights, incorporeal, insurance, securities, shares, bonds, lease, murabaha]
