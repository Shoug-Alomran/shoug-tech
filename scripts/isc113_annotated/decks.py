"""ISC113 annotated slides — every Islamic Economy lecture.

The Qur'an and hadith quotations are in Arabic script that doesn't survive text extraction, so every slide
is shown as the original image (whole=True) with the notes beside it. Each deck is a namespace class built
by lecture(); see cs331_annotated/ch01_1_introduction.py for the ANN keys."""
from .common import DECKS, mcq, past, see, short, tf, tip, trap, trick


def lecture(key, count, lede, ann):
    slug, file, folder, label = DECKS[key]
    head, title = label.split(': ', 1)
    return type(key, (), {
        'AUTO_SLIDES': True,
        'DECK': {'key': key, 'slug': slug, 'file': file, 'title': title, 'chapter': head,
                 'pdf': '/academics/other-courses/isc113/slides/%s/' % folder, 'lede': lede},
        'ANN': {n: dict(ann.get(n, {}), whole=True) for n in range(1, count + 1)},
    })


concept = lecture('d01', 5, 'The linguistic meaning of economy (moderation), the definition of Islamic economy, its doctrinal, legislative and applied aspects, and its relationship with Shari’a, mathematics and statistics.', {
    2: dict(notes=['Economy (iqtisad) linguistically: moderation, the straight middle path between extravagance and stinginess.',
                   'Islamic economy: knowledge of the Shari’a rules that govern economic activity, drawn from their detailed evidence.'],
            exam=[mcq('Linguistically, "iqtisad" (economy) means:', ['Moderation between extravagance and stinginess', 'Accumulating wealth', 'Free trade only', 'Taxation'], 0, '')], weight=3),
    3: dict(notes=['Rules include protecting both public and private property; the hadith forbids meeting traders outside the market and a city-dweller selling for a desert-dweller (to prevent exploitation).']),
    4: dict(notes=['Three aspects: doctrinal (beliefs and values), legislative (rules), applied (economic policy that handles the community’s problems).']),
})

systems = lecture('d02', 3, 'The characteristics of the Islamic economy (dual property, restricted liberty, social solidarity) compared with capitalism and socialism and their disadvantages.', {
    1: dict(notes=['Islamic economy: dual ownership (private + public, balanced), restricted economic liberty (within Shari’a), social solidarity (zakat, mutual support).'],
            tips=[trick('Capitalism = private property + absolute freedom; socialism = public ownership + state control; Islam = both kinds of ownership with regulated freedom.')],
            exam=[mcq('"Dual property" in the Islamic economy means:', ['Both private and public ownership are recognized in balance', 'Only state ownership', 'Only private ownership', 'Shared ownership of everything'], 0, '')], weight=3),
    2: dict(notes=['Capitalism’s problems: unequal wealth distribution, crises and unemployment, monopoly, absolute freedom in earning and spending. Socialism: public ownership of the means of production, central planning.'],
            exam=[mcq('Which is a disadvantage of capitalism mentioned in the lecture?', ['Imbalance in wealth distribution', 'Abolishing private property', 'Central planning', 'No markets'], 0, '')], weight=3),
})

terms = lecture('d03', 4, 'Wealth at the individual and macro level, consumer vs. production goods, consumer vs. production services, consumption, saving and investment.', {
    1: dict(notes=['Wealth: the productive and consumable economic assets owned at a given moment (individual or national level).']),
    2: dict(notes=['Consumer goods satisfy needs directly (food, clothes); production goods are used to produce other goods (machines). Some goods are either, depending on the user.'],
            exam=[mcq('A factory machine is a:', ['Production good', 'Consumer good', 'Consumer service', 'Saving'], 0, '')], weight=3),
    3: dict(notes=['Services are intangible products: consumer services (transport, education) and production services.']),
    4: dict(notes=['Consumption: income spent on goods that satisfy needs directly. Saving: income NOT spent. Investment: using savings to add to productive capacity.']),
})

budget = lecture('d04', 2, 'The concept of the state budget, public revenues and expenditure, and public loans (national or sovereign debt).', {
    1: dict(notes=['State budget: the government’s plan for obtaining public revenues and spending them to meet public needs and social and economic goals.']),
    2: dict(notes=['Public loans: money the government borrows (banks, individuals, international bodies) to finance spending or deficits: the national (sovereign) debt.']),
})

revenues = lecture('d05', 6, 'Periodic revenues (zakat, jizya, kharaj) and non-periodic ones (khums, endowments), the eight zakat recipients, waqf, and the goals and rules of public expenditure in Islam.', {
    1: dict(notes=['Periodic revenues: zakat, jizya, kharaj (land tax) → Bayt al-Mal. Non-periodic: one-fifth of spoils, inheritances without heirs, endowments, etc.'],
            exam=[mcq('Which is a PERIODIC public revenue in Islam?', ['Zakat', 'One-fifth of the spoils', 'Property without heirs', 'Lost property'], 0, '')], weight=3),
    2: dict(notes=['Zakat goes to eight categories (At-Tawbah 9:60): the poor, the needy, zakat administrators, those whose hearts are to be reconciled, freeing captives, debtors, in the cause of Allah, the stranded traveller.'],
            exam=[short('List four of the eight categories of zakat recipients.', 'The poor, the needy, those employed to collect it, those whose hearts are to be reconciled, freeing captives, debtors, in the cause of Allah, and the stranded traveller (any four).')], weight=3),
    3: dict(notes=['Jizya: an annual per-capita tax on non-Muslim subjects (dhimmi) in return for protection and exemption from military service.']),
    4: dict(notes=['Waqf (endowment): an inalienable charitable endowment: the asset is held and its yield spent on religious or charitable purposes.']),
    6: dict(notes=['Rules of public expenditure: beneficial use (maximum utility at minimum cost), economy (no waste), and priorities (necessities first).']),
})

dilemma = lecture('d06', 4, 'The economic dilemma and relative scarcity, human needs in the Islamic concept, the adequacy of Allah’s resources, and the real causes of starvation.', {
    1: dict(notes=['Economic problem = relative scarcity: resources can’t meet all needs at the right time, place and form.']),
    3: dict(notes=['Islam’s view: resources are sufficient (“there is not a thing but that with Us are its depositories”); scarcity is relative, not absolute.']),
    4: dict(notes=['Starvation is caused by unequal distribution, failure to use resources, excessive wants and a spiritual crisis, not by an absolute lack of resources.'],
            exam=[mcq('According to the lecture, starvation in poor countries is mainly caused by:', ['Poor distribution and misuse of resources', 'An absolute lack of resources on Earth', 'Zakat', 'Too much production'], 0, '')], weight=3),
})

production = lecture('d07', 5, 'The concept and motives of production in Islam, the elements of production (land, labour, capital), the role of the community and the ruler, and forms of cash and real capital (partnerships, mudaraba, leasing).', {
    1: dict(notes=['Production in Islam: persistent effort to invest resources and increase yield for society’s prosperity; Islam encourages work and developing the earth.']),
    3: dict(notes=['The ruler provides jobs and training, supervises worker–employer relations, and can compel people in necessary professions to work at a fair wage.']),
    4: dict(notes=['Cash capital earns through partnership (both contribute capital and work, profit as agreed) or mudaraba (one gives capital, the other works; loss falls on capital), never through fixed interest.'],
            tips=[trap('In mudaraba the capital owner bears financial loss; the worker loses only his effort.')], weight=3),
    5: dict(notes=['Real capital (machines, buildings) earns through use or leasing (rent).']),
})

consumption = lecture('d08', 3, 'Consumption and consumer conduct in Islam: lawful goods, moderation in spending, and Islamic vs. Western concepts of utility and satisfaction.', {
    1: dict(notes=['Consumption theory elements in Islam: consume only lawful (halal) goods, moderation, and a broader concept of satisfaction.']),
    2: dict(notes=['Moderation: “do not make your hand chained to your neck nor extend it completely”: neither stinginess nor extravagance.'],
            exam=[mcq('The Qur’anic rule on spending emphasized in the lecture is:', ['Moderation', 'Maximizing consumption', 'Total abstention', 'Spending only on oneself'], 0, '')], weight=3),
    3: dict(notes=['Utility in Western economics is material; in Islam it is material AND spiritual, tied to lawful benefit and reward.']),
})

market = lecture('d09', 3, 'The market in Islamic thought and its ethics: fairness in weights and measures, honesty, no cheating, no false bidding (najash), no monopoly, leniency in buying and selling.', {
    1: dict(notes=['Market: where buyers and sellers meet and prices are formed. Ethics: fair measures, honesty, no hoarding, no interception of traders.']),
    2: dict(notes=['“Whoever cheats is not one of us.” False bidding (najash): raising the price with no intention to buy, to trick the buyer: forbidden.'],
            exam=[mcq('Bidding up a price with no intention to buy, to deceive others, is called:', ['Najash (false bidding)', 'Murabaha', 'Ijarah', 'Mudaraba'], 0, '')], weight=3),
    3: dict(notes=['“May Allah have mercy on one who is lenient when he buys, sells and asks for repayment.”']),
})

pricing = lecture('d10', 2, 'Price freedom in Islam, the Prophet’s refusal to fix prices, and when the ruler may intervene against monopoly and exploitation.', {
    1: dict(notes=['Default: prices are free (set by supply and demand); the Prophet ﷺ refused to fix prices: “Allah is the one who sets prices.”'],
            exam=[tf('In principle, Islam lets prices be set freely by the market.', True, '')], weight=3),
    2: dict(notes=['Exception: the ruler may set prices when traders monopolize or exploit, to prevent harm.']),
})

money = lecture('d11', 4, 'Money and its main and secondary functions, commodity and fiat money (coins, banknotes, bank money), rules of cash money, riba al-fadl and riba al-nasi’ah, currency exchange, and zakat on money.', {
    1: dict(notes=['Money: anything generally accepted as a medium of exchange; main functions: medium of exchange and measure of value (also store of value, standard of deferred payment).'],
            exam=[mcq('A main function of money is:', ['Medium of exchange', 'Production good', 'Taxation', 'Insurance'], 0, '')], weight=3),
    3: dict(notes=['Usury (riba) applies to money as to gold and silver: riba al-fadl (unequal exchange of the same kind) and riba al-nasi’ah (delay).'],
            tips=[trick('Same currency: equal AND hand-to-hand. Different currencies: any rate, but hand-to-hand.')]),
    4: dict(notes=['Exchanging different currencies is allowed at any rate if done on the spot (e.g. 1 USD for 3.75 SAR instantly). Zakat is due when money reaches the nisab and a year passes.'],
            exam=[mcq('Selling 1 US dollar for 3.75 riyals is permissible if:', ['Exchanged on the spot', 'Delivered next month', 'Interest is added', 'Never permissible'], 0, '')], weight=3),
})

banks = lecture('d12', 5, 'Banks and their types, the functions of commercial banks (deposits, loans, services), and Islamic banks: why they exist and how they work without riba.', {
    1: dict(notes=['Bank: an institution dealing in money and credit (central, commercial, specialized, Islamic).']),
    2: dict(notes=['Commercial banks: accept current (demand) and time deposits, give interest-bearing loans, and provide banking services.']),
    4: dict(notes=['Islamic banks let Muslims avoid riba; they invest through murabaha, mudaraba, musharaka and ijarah instead of interest.'],
            exam=[mcq('The main reason for establishing Islamic banks is to:', ['Avoid riba (interest)', 'Avoid all banking services', 'Print money', 'Collect jizya'], 0, '')], weight=3),
    5: dict(notes=['Functions: current and investment accounts, interest-free services (letters of credit, guarantees, transfers), and investment based on profit and loss sharing.']),
})

DECKS_HERE = [concept, systems, terms, budget, revenues, dilemma, production, consumption, market, pricing, money, banks]
