"""Content for the ECON101 cheat sheets (see build_econ101_cheat_sheets.py).

Written from scripts/study_content/econ101/*.md: the course slides, the
instructor's handwriting on them, and the worked examples the slides use
(Huda, Rakan, Qamar Bakery, Al-Bustan Farm, Sahra Tours, Bunn Café). Every
number below was recomputed when the sheet was written.

Each chapter is a dict: id, n (tab number), tab, num, title, links, lead,
body (HTML), clues [(clue, answer)], qs [(tag, ask, answer HTML)].
"""
from __future__ import annotations

BASE = "/academics/other-courses/econ101/"


# ------------------------------------------------------------------ markup helpers
def card(fn, title, *parts, cls="f"):
    return f'<article class="{cls}"><header><span class="fn">{fn}</span><h4>{title}</h4></header>{"".join(parts)}</article>'


def p(text):
    return f"<p>{text}</p>"


def ul(*items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def steps(*items):
    return '<ol class="steps">' + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


def kv(*pairs):
    return '<dl class="kv">' + "".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in pairs) + "</dl>"


def eq(*exprs):
    return '<div class="eq">' + "".join(f'<span class="expr">{e}</span>' for e in exprs) + "</div>"


def w(word):
    return f'<span class="word">{word}</span>'


def ex(label, work):
    return f'<div class="box ex"><b>{label}</b><div class="work">{work}</div></div>'


def trap(label, text):
    return f'<div class="box trap"><b>{label}</b>{text}</div>'


def hook(label, text):
    return f'<div class="box hook"><b>{label}</b>{text}</div>'


def pc(pro_title, pros, con_title, cons):
    return (f'<div class="pc"><div class="pro"><b>{pro_title}</b>{ul(*pros)}</div>'
            f'<div class="con"><b>{con_title}</b>{ul(*cons)}</div></div>')


def grid(*cards, wide=False):
    return f'<div class="grid{" wide" if wide else ""}">' + "".join(cards) + "</div>"


def group(title):
    return f'<h3 class="group">{title}</h3>'


def tbl(head, rows, numcol=None):
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = ""
    for r in rows:
        tr += "<tr>" + "".join(
            f'<td class="num">{c}</td>' if numcol is not None and i == numcol else f"<td>{c}</td>" for i, c in enumerate(r)
        ) + "</tr>"
    return f'<div class="tbl"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def q(tag, ask, ans):
    return (f'<div class="q"><div class="tagline">{tag}</div><p class="ask">{ask}</p>'
            f'<details><summary>Show answer</summary><div class="ans">{ans}</div></details></div>')


def links(slug, quiz):
    return [("Breakdown", f"{BASE}slide-breakdowns/{slug}/"), ("Mind map", f"{BASE}extra-resources/mindmaps/{slug}/"),
            ("Chapter quiz", f"{BASE}exams/{quiz}/")]


# ------------------------------------------------------------------ chapters
CHAPTERS: dict[int, dict] = {}

CHAPTERS[2] = dict(
    id="ch2", n="2", tab="Economic problem", num="CHAPTER 02 · THE ECONOMIC PROBLEM",
    title="PPF, opportunity cost, efficiency and trade", links=links("02-the-economic-problem", "02-the-economic-problem-quiz"),
    lead="The slide notes say the questions are MCQ, and that you must understand PPF graphs, opportunity cost calculations, and comparative versus absolute advantage.",
    body=grid(
        card("1", "Reading the PPF",
             p("The PPF is the boundary between what can and can't be produced with the resources and technology available."),
             tbl(["Point", "Status", "Why"], [["On the PPF", "Attainable and efficient", "All resources used"],
                                               ["Inside", "Attainable, <b>inefficient</b>", "Unused or misallocated resources"],
                                               ["Outside", "<b>Unattainable</b>", "Not enough resources"]]),
             p("It <b>bows outward</b> because resources aren't equally productive in every activity, so opportunity cost <b>increases</b>.")),
        card("F1", "Opportunity cost",
             eq(f"OC of X = {w('amount of the other good given up')} ÷ {w('amount of X gained')}"),
             ex("Pizza / cola table (slides)", "E (4 pizzas, 5 cola) → F (5, 0)\nPizza +1, cola −5 → OC of 1 pizza = 5 ÷ 1 = 5 cans\nOC of 1 can = 1 ÷ 5 = 1/5 pizza (the inverse)"),
             hook("Mnemonic", "<b>Give-up over Get.</b> The cost of one good is the inverse of the cost of the other.")),
        card("2", "Allocative efficiency",
             p("Every point on the PPF is production-efficient; only one is <b>allocatively</b> efficient: where <b>MB = MC</b>."),
             tbl(["If", "Then"], [["MB &gt; MC", "Produce more"], ["MB &lt; MC", "Produce less"], ["MB = MC", "Allocative efficiency"]]),
             p("MC rises (rising opportunity cost); MB falls (each extra unit is worth less — the handwriting's \"one car is essential, a fourth isn't\")."),
             trap("Trap", "Production efficiency (on the PPF) isn't allocative efficiency (the one point where MB = MC).")),
        card("F2", "Comparative vs absolute advantage",
             kv(("Comparative", "Producing at a <b>lower opportunity cost</b>"), ("Absolute", "Producing <b>more</b> with the same resources")),
             tbl(["Per hour", "Liz", "Joe"], [["Max smoothies", "30", "6"], ["Max salads", "30", "30"],
                                              ["OC of 1 smoothie", "<b>1 salad</b>", "5 salads"], ["OC of 1 salad", "1 smoothie", "<b>1/5 smoothie</b>"]]),
             p("Liz specializes in smoothies, Joe in salads. Trading at 2 salads per smoothie, each gains 5 smoothies and 5 salads an hour and both consume <b>outside their own PPF</b>."),
             hook("Mnemonic", "<b>C</b>omparative is about <b>c</b>osts; <b>A</b>bsolute is about <b>a</b>mounts."),
             trap("Trap", "Nobody has a comparative advantage in everything: the costs are inverses, so each person is cheaper at something.")),
        card("3", "Growth and coordination",
             p("Growth comes from <b>technological change</b> and <b>capital accumulation</b> (including human capital). Its cost is <b>less consumption now</b>; the PPF shifts out later."),
             p("Four coordinating institutions: <b>firms, markets, property rights, money</b>."),
             p("Circular flow: households sell factors (labour, land, capital, entrepreneurship) in <b>factor markets</b> and buy in <b>goods markets</b>; money flows the opposite way to goods. The handwriting: label every flow.")),
    ),
    clues=[("A point inside the PPF", "Attainable but inefficient: unused or misallocated resources"),
           ("The PPF bows outward", "Increasing opportunity cost: resources aren't equally productive"),
           ("Lower opportunity cost of producing a good", "Comparative advantage"),
           ("Produces more of both goods with the same resources", "Absolute advantage"),
           ("MB is greater than MC", "Produce more of the good"),
           ("PPF shifts outward over time", "Economic growth: technology and capital accumulation"),
           ("Firms, markets, property rights, money", "The four coordinating institutions")],
    qs=[("Calculation · Ch 2", "From D (3 pizzas, 9 cola) to E (4 pizzas, 5 cola), what is the opportunity cost of one pizza, and of one can of cola?",
         "<p>Pizza rises by 1 and cola falls by 4. OC of a pizza = 4 ÷ 1 = <b>4 cans</b>. OC of a can = 1 ÷ 4 = <b>1/4 pizza</b> (the inverse).</p>"),
        ("Calculation · Ch 2", "Sara can bake 20 cakes or 10 pies an hour; Omar 12 cakes or 4 pies. Who has the comparative advantage in each good?",
         "<p>OC of a cake: Sara 10/20 = <b>0.5 pie</b>; Omar 4/12 = <b>1/3 pie</b> → Omar has the comparative advantage in <b>cakes</b>.</p>"
         "<p>OC of a pie: Sara 2 cakes; Omar 3 cakes → Sara has it in <b>pies</b>. Sara has the absolute advantage in both.</p>"),
        ("Short answer · Ch 2", "Explain how specialization and trade make both Liz and Joe better off.",
         "<p>Each specializes in the good with the lower opportunity cost (Liz smoothies, Joe salads) and trades at a price between their two costs. Both end up consuming combinations <b>outside their own PPF</b>: 5 more smoothies and 5 more salads each per hour.</p>")],
)

CHAPTERS[3] = dict(
    id="ch3", n="3", tab="Demand & supply", num="CHAPTER 03 · DEMAND AND SUPPLY",
    title="Shifters, equilibrium and predicting changes", links=links("03-demand-and-supply", "03-demand-and-supply-quiz"),
    lead="The most important chapter of the course: every later topic uses this model. Expect a headline and \"what happens to price and quantity?\".",
    body=grid(
        card("1", "Movement along vs shift",
             tbl(["", "Change in quantity demanded", "Change in demand"], [["Caused by", "The good's <b>own price</b>", "Anything else"],
                                                                           ["Graph", "<b>Movement along</b> the curve", "<b>Whole curve shifts</b>"]]),
             p("Law of demand: higher price, smaller quantity demanded (substitution effect + income effect). Law of supply: higher price, greater quantity supplied (rising MC)."),
             trap("Trap", "\"Price rose so demand fell\" is wrong: price changes <i>quantity demanded</i>, a movement along the curve.")),
        card("2", "Demand shifters — RIPE",
             tbl(["Factor", "Demand increases when"], [["<b>R</b>elated goods", "Substitute's price rises / complement's price falls"],
                                                     ["<b>I</b>ncome", "Income rises (normal good); falls (inferior good)"],
                                                     ["<b>P</b>references, <b>P</b>opulation", "Tastes favour it / more buyers"],
                                                     ["<b>E</b>xpected prices", "Price expected to rise"], ["<b>E</b>xpected income / credit", "Expected to rise / easy credit"]])),
        card("3", "Supply shifters — FRETS, N",
             tbl(["Factor", "Supply increases when"], [["<b>F</b>actor prices", "Input costs fall"],
                                                     ["<b>R</b>elated goods produced", "Substitute in production cheaper / complement dearer"],
                                                     ["<b>E</b>xpected prices", "Price expected to <b>fall</b> (sell now)"], ["<b>T</b>echnology", "Improves"],
                                                     ["<b>S</b>uppliers", "More sellers"], ["<b>N</b>ature", "Good weather, no disasters"]]),
             trap("Trap", "Expected <b>higher</b> price: demand rises today <i>and</i> supply falls today. Both push today's price up.")),
        card("F1", "Equilibrium",
             eq("Q<sub>d</sub> = Q<sub>s</sub>"),
             ex("From equations", "Qd = 19 − 3P, Qs = 1 + 3P\n19 − 3P = 1 + 3P → 6P = 18 → P = 3, Q = 10\nAt P = 2: Qd = 13, Qs = 7 → shortage of 6, price rises"),
             p("Below equilibrium: <b>shortage</b>, price rises. Above: <b>surplus</b>, price falls.")),
        card("F2", "Predicting price and quantity",
             tbl(["Change", "Price", "Quantity"], [["Demand ↑", "↑", "↑"], ["Demand ↓", "↓", "↓"], ["Supply ↑", "<b>↓</b>", "↑"], ["Supply ↓", "<b>↑</b>", "↓"]]),
             tbl(["Both shift", "Price", "Quantity"], [["D ↑, S ↑", "<b>?</b>", "↑"], ["D ↓, S ↓", "<b>?</b>", "↓"], ["D ↑, S ↓", "↑", "<b>?</b>"], ["D ↓, S ↑", "↓", "<b>?</b>"]]),
             hook("Mnemonic", "<b>Same way: Quantity's sure. Opposite: Price is sure.</b> The handwriting: write \"ambiguous\" unless the question says which shift is bigger.")),
        card("4", "Four-step method for any headline",
             steps("Buyers (demand) or sellers (supply)?", "Which factor, and does the curve shift right or left?", "Draw it or use the table.",
                   "Read the new price and quantity."),
             ex("Headlines", "\"Drought cuts date harvest\" → supply ↓ → P ↑, Q ↓\n\"Incomes rise; new machine cuts cost (normal good)\" → D ↑, S ↑ → Q ↑, P ambiguous")),
    ),
    clues=[("The good's own price changes", "Movement along the curve (change in quantity demanded / supplied)"),
           ("Price of a substitute rises", "Demand increases (shifts right)"),
           ("Price of a complement rises", "Demand decreases (shifts left)"),
           ("Income rises and demand falls", "Inferior good"),
           ("Input prices rise / drought / disaster", "Supply decreases (shifts left)"),
           ("Price below equilibrium", "Shortage; price rises"),
           ("Demand and supply both increase", "Quantity rises; price ambiguous"),
           ("Demand falls while supply rises", "Price falls; quantity ambiguous")],
    qs=[("Headline · Ch 3", "\"The price of coffee rises sharply.\" What happens to the demand for tea, and for sugar used in coffee?",
         "<p>Tea is a substitute: demand for tea <b>increases</b> (shifts right). Sugar is a complement: demand for sugar <b>decreases</b> (shifts left).</p>"),
        ("Calculation · Ch 3", "Qd = 19 − 3P and Qs = 1 + 3P. Find the equilibrium, then the situation at P = 4.",
         "<p>19 − 3P = 1 + 3P → P = <b>3</b>, Q = <b>10</b>. At P = 4: Qd = 7, Qs = 13 → a <b>surplus of 6</b>, so the price falls back toward 3.</p>"),
        ("Short answer · Ch 3", "Explain the difference between a change in demand and a change in quantity demanded.",
         "<p>A change in the good's own price causes a change in <b>quantity demanded</b>, a movement along the curve. A change in any other factor (RIPE) causes a change in <b>demand</b>, a shift of the whole curve.</p>")],
)

CHAPTERS[4] = dict(
    id="ch4", n="4", tab="Elasticity", num="CHAPTER 04 · ELASTICITY",
    title="Price, income, cross and supply elasticity", links=links("04-elasticity", "04-elasticity-quiz"),
    lead="Almost every question is a calculation. The handwriting: solve step by step, never round early, and report elasticity as a positive number.",
    body=grid(
        card("F1", "Price elasticity of demand (midpoint)",
             eq(f"ε = {w('% change in quantity demanded')} ÷ {w('% change in price')}", f"% change = Δ ÷ {w('average')} × 100"),
             ex("Slide 9", "P 20.50 → 19.50, Q 9 → 11\n%ΔQ = 2 ÷ 10 = 20%   %ΔP = 1 ÷ 20 = 5%\nε = 20 ÷ 5 = 4 → elastic"),
             ex("Slide 25", "P 15 → 10, Q 20 → 30\n%ΔQ = 10 ÷ 25 = 40%   %ΔP = 5 ÷ 12.5 = 40%\nε = 1 → unit elastic"),
             hook("How to write it", "Positive number, every step shown, then interpret: \"a 1% price rise lowers quantity demanded by 4%\".")),
        card("1", "The ranges",
             tbl(["ε", "Type", "Curve"], [["0", "Perfectly inelastic", "Vertical"], ["0 – 1", "<b>Inelastic</b>", "Steep"], ["1", "<b>Unit elastic</b>", ""],
                                          ["&gt; 1", "<b>Elastic</b>", "Flatter"], ["∞", "Perfectly elastic", "Horizontal"]]),
             trap("Trap", "Slope isn't elasticity. Along a straight-line demand curve: elastic at high prices, unit elastic at the midpoint, inelastic at low prices."),
             hook("Mnemonic", "<b>Insulin is Inelastic</b> (the handwriting's diabetic example).")),
        card("F2", "Total revenue test",
             eq("TR = P × Q"),
             tbl(["Demand", "P ↑ → TR", "P ↓ → TR"], [["Elastic", "<b>falls</b>", "<b>rises</b>"], ["Inelastic", "<b>rises</b>", "<b>falls</b>"], ["Unit", "no change", "no change"]]),
             hook("Mnemonic", "<b>In</b>elastic: TR moves <b>in</b> the same direction as price.")),
        card("2", "What makes demand elastic",
             tbl(["Factor", "More elastic when"], [["Closeness of substitutes", "Close substitutes exist"], ["Share of income", "Large share (cars vs salt)"],
                                                  ["Time since the change", "More time has passed"]]),
             p("Necessities tend to be inelastic, luxuries elastic. Right after a price change demand can be almost perfectly inelastic.")),
        card("F3", "Income, cross and supply elasticity",
             tbl(["Elasticity", "Formula", "Sign means"], [["Income", "%ΔQd ÷ %Δincome", "+ normal (&gt;1 income elastic), <b>− inferior</b>"],
                                                          ["Cross", "%ΔQd(A) ÷ %ΔP(B)", "<b>+ substitutes</b>, <b>− complements</b>"],
                                                          ["Supply", "%ΔQs ÷ %ΔP", "Always +; larger with more time"]]),
             ex("Cross", "Pepsi price +10%, Coke sales +5% → +0.5 → substitutes\nBurgers +10%, fries −4% → −0.4 → complements"),
             p("Supply: momentary perfectly inelastic → short run inelastic → long run most elastic."),
             hook("Mnemonic", "<b>S</b>ubstitutes <b>S</b>hare a sign; <b>C</b>omplements <b>c</b>ontradict.")),
    ),
    clues=[("ε greater than 1", "Elastic: quantity changes by a larger % than price"),
           ("Price rises and total revenue rises", "Demand is inelastic"),
           ("Price rises and total revenue falls", "Demand is elastic"),
           ("Vertical demand curve", "Perfectly inelastic (ε = 0)"),
           ("Negative income elasticity", "Inferior good"),
           ("Positive cross elasticity", "Substitutes"),
           ("Long time since the price change", "Demand and supply more elastic")],
    qs=[("Calculation · Ch 4", "Price rises from 8 to 12 and quantity falls from 50 to 30. Find ε, classify demand, and check with total revenue.",
         "<p>%ΔQ = 20 ÷ 40 = 50%. %ΔP = 4 ÷ 10 = 40%. ε = 50 ÷ 40 = <b>1.25 → elastic</b>.</p>"
         "<p>TR falls from 8 × 50 = 400 to 12 × 30 = 360: price up, revenue down, which confirms elastic demand.</p>"),
        ("Calculation · Ch 4", "Income rises 10% and the quantity of bus rides demanded falls 5%. Income elasticity? What kind of good?",
         "<p>−5 ÷ 10 = <b>−0.5</b>. Negative, so bus rides are an <b>inferior good</b>.</p>"),
        ("Short answer · Ch 4", "State three factors that influence the price elasticity of demand.",
         "<p>The <b>closeness of substitutes</b>, the <b>proportion of income</b> spent on the good, and the <b>time elapsed</b> since the price change.</p>")],
)

CHAPTERS[5] = dict(
    id="ch5", n="5", tab="Efficiency & equity", num="CHAPTER 05 · EFFICIENCY AND EQUITY",
    title="Surplus, deadweight loss and fairness", links=links("05-efficiency-and-equity", "05-efficiency-and-equity-quiz"),
    lead="Consumer and producer surplus as triangle areas is the skill you'll use most; Chapter 6 judges every policy with it.",
    body=grid(
        card("1", "Eight allocation methods",
             p("Market price, command, majority rule, contest, first-come first-served, lottery, personal characteristics, force."),
             hook("Mnemonic", "<b>My Cat Must Catch Five Little Purring Fish.</b>"),
             p("Contests reward effort that is hard to monitor directly; force (theft) is the last resort.")),
        card("F1", "Surplus",
             eq("Demand = MB", "Supply = MC"),
             kv(("Consumer surplus", "Value (willingness to pay) − price paid: triangle <b>below demand, above price</b>"),
                ("Producer surplus", "Price received − MC: triangle <b>above supply, below price</b>"), ("Total surplus", "CS + PS")),
             ex("Triangles (½ × base × height)", "Equilibrium P = 5, Q = 5; demand starts at 9, supply at 1\nCS = ½ × 5 × (9 − 5) = 10\nPS = ½ × 5 × (5 − 1) = 10   Total = 20"),
             ex("One buyer at a time", "Willing to pay 30, 25, 15; price 15 → CS = 15 + 10 + 0 = 25")),
        card("2", "Is the competitive market efficient?",
             tbl(["Quantity", "MB vs MC", "Result"], [["Below equilibrium", "MB &gt; MC", "Underproduction, deadweight loss"],
                                                      ["Equilibrium", "MB = MC", "Efficient, total surplus max"], ["Above", "MB &lt; MC", "Overproduction, deadweight loss"]]),
             p("<b>Obstacles:</b> price and quantity regulations, taxes and subsidies, externalities, public goods and common resources, monopoly, high transaction costs.")),
        card("3", "Is it fair?",
             tbl(["View", "Unfair if"], [["\"Results\" view", "Incomes are very unequal (utilitarianism, the big tradeoff)"],
                                       ["\"Rules\" view", "The rules are unfair (symmetry principle, property rights, voluntary exchange)"]]),
             trap("Trap", "Efficient isn't the same as fair.")),
    ),
    clues=[("Area below demand and above price", "Consumer surplus"),
           ("Area above supply and below price", "Producer surplus"),
           ("Quantity below equilibrium (MB > MC)", "Underproduction and deadweight loss"),
           ("Surplus lost because quantity isn't efficient", "Deadweight loss")],
    qs=[("Calculation · Ch 5", "Demand starts at a price of 12, supply at 2, and equilibrium is P = 7, Q = 10. Find CS, PS and total surplus.",
         "<p>CS = ½ × 10 × (12 − 7) = <b>25</b>. PS = ½ × 10 × (7 − 2) = <b>25</b>. Total surplus = <b>50</b>.</p>")],
)

CHAPTERS[6] = dict(
    id="ch6", n="6", tab="Government actions", num="CHAPTER 06 · GOVERNMENT ACTIONS IN MARKETS",
    title="Ceilings, floors, taxes, quotas, subsidies, illegal goods", links=links("06-government-actions-in-markets", "06-government-actions-in-markets-quiz"),
    lead="The most calculation-heavy chapter. The slides solve every example with equations, always the same way: find the free-market equilibrium first, then apply the policy.",
    body=grid(
        card("1", "Ceilings and floors",
             tbl(["", "Rent ceiling", "Minimum wage"], [["Rule", "Illegal to charge more", "Illegal to pay less"],
                                                       ["Binds when set", "<b>Below</b> equilibrium", "<b>Above</b> equilibrium"],
                                                       ["Creates", "<b>Shortage</b>, search, black market", "<b>Unemployment</b>, job search"],
                                                       ["Fair?", "No, on both views", "No, on both views"]]),
             hook("Mnemonic", "<b>Ceilings bind Below, floors bind Above</b>; otherwise they change nothing.")),
        card("F1", "Rent ceiling (slide 6)",
             ex("D: P = 5,000 − 50Q   S: P = 1,000 + 50Q", "Equilibrium: Q = 40 (thousand), P = 3,000\nCeiling 2,500: Qd = (5,000 − 2,500)/50 = 50\n               Qs = (2,500 − 1,000)/50 = 30\nShortage = 20 thousand\nBuyers would pay 5,000 − 50(30) = 3,500 for the 30th\nDWL = ½ × 10 × (3,500 − 2,500) = 5,000 (thousand SAR)")),
        card("F2", "Minimum wage (slide 10)",
             ex("D: W = 44 − 0.6L   S: W = 8 + 0.3L", "Equilibrium: L = 40, W = 20\nMinimum wage 26: Ld = (44 − 26)/0.6 = 30\n                  Ls = (26 − 8)/0.3 = 60\nUnemployment = 30 thousand hours\nLast hour hired supplied for 8 + 0.3(30) = 17")),
        card("F3", "Taxes: the wedge",
             eq(f"{w('buyers price')} − {w('sellers price')} = {w('tax')}"),
             ex("8 SAR tax (slide 14): D: P = 30 − 0.06Q  S: P = 6 + 0.02Q", "No tax: Q = 300, P = 12\n(30 − 0.06Q) − (6 + 0.02Q) = 8 → Q = 200\nBuyers pay 18 (+6), sellers get 10 (−2)\nRevenue = 8 × 200 = 1,600   DWL = ½ × 8 × 100 = 400"),
             p("Same outcome whether the law taxes buyers or sellers."),
             hook("Mnemonic", "<b>The less flexible side pays.</b> More inelastic demand → buyers pay more; more inelastic supply → sellers pay more."),
             trap("Trap", "No deadweight loss if demand or supply is perfectly inelastic: quantity doesn't change.")),
        card("4", "Who pays a 2 SAR tax",
             tbl(["Case", "Buyers pay", "Sellers get", "Paid by"], [["Perfectly inelastic demand", "12", "10", "Buyers"],
                                                                   ["Perfectly elastic demand", "10", "8", "Sellers"],
                                                                   ["Perfectly inelastic supply", "10", "8", "Sellers"],
                                                                   ["Perfectly elastic supply", "12", "10", "Buyers"]]),
             p("Fairness principles: <b>benefits</b> (pay for what you use) and <b>ability to pay</b> (the rich pay more).")),
        card("F4", "Quota vs subsidy (tomatoes: D P = 54 − Q, S P = 14 + Q → Q 20, P 34)",
             tbl(["", "Quota of 15", "Subsidy of 10"], [["Quantity", "15", "25"], ["Price", "54 − 15 = 39", "29 (S becomes P = 4 + Q)"],
                                                       ["MC", "14 + 15 = 29", "14 + 25 = 39"], ["Result", "<b>Under</b>production", "<b>Over</b>production"],
                                                       ["DWL", "½ × 5 × 10 = 25", "½ × 5 × 10 = 25"], ["Extra", "Incentive to cheat (P &gt; MC)", "Costs 10 × 25 = 250"]])),
        card("5", "Illegal goods (D: P = 100 − Q, S: P = 20 + Q, CBL = 20)",
             tbl(["Penalty on", "Q", "Buyer pays", "Seller gets"], [["Sellers (S + 20)", "30", "70", "50"], ["Buyers (D − 20)", "30", "70 (50 + 20)", "50"],
                                                                   ["Both", "20", "80", "40"]]),
             p("Legalize with a 40 tax: same 20 units, revenue 800 thousand.")),
    ),
    clues=[("Price ceiling set below equilibrium", "Shortage, search activity, black market"),
           ("Price floor (minimum wage) above equilibrium", "Unemployment (surplus of labour)"),
           ("Ceiling set above equilibrium", "No effect"),
           ("Buyers bear most of a tax", "Demand is more inelastic than supply"),
           ("Tax with perfectly inelastic demand", "Buyers pay it all; no deadweight loss"),
           ("Production quota", "Underproduction, price above MC, incentive to cheat"),
           ("Subsidy to producers", "Overproduction, MC above price, government cost")],
    qs=[("Calculation · Ch 6", "Demand P = 50 − Q, supply P = 10 + Q. A tax of 10 per unit is imposed. Find the quantity, buyers' and sellers' prices, revenue and deadweight loss.",
         "<p>No tax: 50 − Q = 10 + Q → Q = 20, P = 30.</p><p>Wedge: (50 − Q) − (10 + Q) = 10 → 40 − 2Q = 10 → <b>Q = 15</b>.</p>"
         "<p>Buyers pay 50 − 15 = <b>35</b>; sellers get 10 + 15 = <b>25</b> (split 5 / 5 because the slopes are equal).</p>"
         "<p>Revenue = 10 × 15 = <b>150</b>. DWL = ½ × 10 × (20 − 15) = <b>25</b>.</p>"),
        ("Calculation · Ch 6", "In the rent example (D: P = 5,000 − 50Q, S: P = 1,000 + 50Q), a ceiling of 3,500 is set. What happens?",
         "<p>Equilibrium rent is 3,000, so a ceiling of 3,500 is <b>above</b> equilibrium: it doesn't bind and <b>nothing changes</b> (40 thousand apartments at 3,000).</p>"),
        ("Short answer · Ch 6", "Explain why a production quota gives farmers an incentive to cheat.",
         "<p>The quota cuts output below equilibrium, so the price (39) is above the marginal cost of the last crate (29). Each farmer could earn more than the extra crate costs by producing over the quota.</p>")],
)

CHAPTERS[8] = dict(
    id="ch8", n="8", tab="Utility & demand", num="CHAPTER 08 · UTILITY AND DEMAND",
    title="Budget line, marginal utility and the best choice", links=links("08-utility-and-demand", "08-utility-and-demand-quiz"),
    lead="The handwriting on slide 1: this is section D, with <b>no graphing</b>. Expect calculations from utility tables, and the water–diamond paradox as an MCQ.",
    body=grid(
        card("F1", "Budget line (Huda: 96 SAR, novel 24, juice 12)",
             eq("24N + 12J = 96"),
             p("At most 4 novels or 8 cups. <b>Income rises</b> → parallel shift out (120 SAR: 5 novels or 10 cups). <b>A price rises</b> → rotates inward on that good's axis (juice at 24: only 4 cups).")),
        card("F2", "Marginal utility",
             eq(f"MU = {w('Δ total utility')} ÷ {w('Δ quantity')}"),
             tbl(["Cups", "1", "2", "3", "4", "5"], [["TU", "48", "90", "120", "144", "162"], ["MU", "48", "42", "30", "24", "18"]]),
             tbl(["Novels", "1", "2", "3", "4", "5"], [["TU", "60", "108", "150", "186", "216"], ["MU", "60", "48", "42", "36", "30"]]),
             trap("Trap", "Diminishing MU doesn't mean TU falls: TU keeps rising, more slowly.")),
        card("F3", "Best choice — two methods",
             p("<b>Spreadsheet:</b> list the combinations that spend all 96 and add TU."),
             tbl(["Row", "Novels", "Juice", "Total TU"], [["A", "0", "8", "189"], ["B", "1", "6", "234"], ["<b>C</b>", "<b>2</b>", "<b>4</b>", "<b>252</b>"],
                                                          ["D", "3", "2", "240"], ["E", "4", "0", "186"]]),
             eq("MU<sub>N</sub>/P<sub>N</sub> = MU<sub>J</sub>/P<sub>J</sub>, all income spent"),
             ex("Marginal rule at C", "48/24 = 2   and   24/12 = 2 → equal → best choice"),
             hook("Mnemonic", "<b>Bang for your Buck is Balanced</b>: every good gives the same MU per riyal.")),
        card("4", "Predictions",
             tbl(["Situation", "Novels", "Juice"], [["Start (24, 12, 96)", "2", "4"], ["Novel price falls to 12", "<b>5</b>", "<b>3</b>"],
                                                   ["Juice rises to 24", "6", "1"], ["Income rises to 120", "6", "4"]]),
             ex("Novel price falls to 12", "Old choice leaves 24 SAR unspent; MU_N/P_N = 48/12 = 4 > 2\nBuy more novels, less juice → 5 novels, 3 cups\nBoth ratios 2.5, total utility 336"),
             p("Own price falls → quantity demanded rises (demand slopes down). Another good's price changes → demand shifts. Income rises → demand for normal goods rises.")),
        card("5", "Paradox of value and behavioural economics",
             tbl(["", "Water", "Diamonds"], [["Total utility", "<b>Large</b>", "Small"], ["Marginal utility", "<b>Small</b>", "Large"], ["Price", "Low", "High"]]),
             hook("Mnemonic", "<b>Price follows the Margin</b>, not total utility."),
             kv(("Bounded rationality", "Limited computing ability → rules of thumb"), ("Bounded willpower", "Choices we'll regret"),
                ("Bounded self-interest", "Suppressing self-interest (charity)"), ("Endowment effect", "Valuing what you own more"))),
    ),
    clues=[("Income rises, prices unchanged", "Budget line shifts outward, parallel"),
           ("One good's price rises", "Budget line rotates inward on that good's axis"),
           ("MU per riyal higher for juice than novels", "Buy more juice, fewer novels"),
           ("Water cheap, diamonds expensive", "Price reflects marginal utility, not total utility"),
           ("Valuing a mug more once you own it", "Endowment effect")],
    qs=[("Calculation · Ch 8", "Using Huda's tables (novel 24, juice 12, income 96), show that 3 novels and 2 cups is not the best choice.",
         "<p>At 3 novels and 2 cups: MU<sub>N</sub>/P<sub>N</sub> = 42/24 = <b>1.75</b>; MU<sub>J</sub>/P<sub>J</sub> = 42/12 = <b>3.5</b>.</p>"
         "<p>Juice gives more utility per riyal, so she should move spending from novels to juice, reaching 2 novels and 4 cups (both ratios 2, TU 252 vs 240).</p>"),
        ("Short answer · Ch 8", "Explain the paradox of value.",
         "<p>Water gives a large <b>total</b> utility but, because we consume so much, a small <b>marginal</b> utility; diamonds the opposite. Price reflects marginal utility, so water is cheap and diamonds are expensive.</p>")],
)

CHAPTERS[9] = dict(
    id="ch9", n="9", tab="Preferences & choices", num="CHAPTER 09 · POSSIBILITIES, PREFERENCES AND CHOICES",
    title="Budget equation, indifference curves and the effects of a price change", links=links("09-possibilities-preferences-and-choices", "09-possibilities-preferences-and-choices-quiz"),
    lead="The handwriting on slide 1: practise the calculations and the graphs, and it's easy. It's the graph version of Chapter 8.",
    body=grid(
        card("F1", "Budget equation (Rakan: 144 SAR, swim 18, fruit 12/kg)",
             eq("18Q<sub>s</sub> + 12Q<sub>f</sub> = 144", "Q<sub>f</sub> = 12 − 1.5Q<sub>s</sub>"),
             tbl(["Term", "Formula", "Rakan", "Graph"], [["Real income (in fruit)", "Y / P<sub>f</sub>", "144/12 = <b>12 kg</b>", "y-intercept"],
                                                        ["Relative price of a session", "P<sub>s</sub> / P<sub>f</sub>", "18/12 = <b>1.5</b>", "slope (magnitude)"]]),
             p("Session price falls to 8 → rotates out (up to 18 sessions). Income falls to 72 → parallel shift in (real income 6 kg).")),
        card("2", "Indifference curves and MRS",
             p("An indifference curve joins combinations liked <b>equally</b>; higher curves are preferred. <b>MRS</b> = fruit given up for one more session, staying on the curve = the curve's steepness."),
             ex("Diminishing MRS (slide 13)", "At C (4 sessions, 6 kg): MRS = 12/8 = 1.5\nAt G (8 sessions, 3 kg): MRS = 6/16 = 0.375"),
             tbl(["Goods", "Shape"], [["Ordinary", "Bowed toward the origin, MRS diminishes"], ["Perfect substitutes", "Straight lines, constant MRS"],
                                     ["Perfect complements", "L-shaped"]])),
        card("F2", "Best affordable choice",
             steps("On the budget line (all income spent).", "On the highest reachable indifference curve.", "<b>MRS = relative price</b>: the curve just touches the line."),
             p("Rakan: <b>C, 4 sessions and 6 kg</b>, MRS = 1.5 = relative price. MRS &gt; relative price → buy more sessions; MRS &lt; → fewer.")),
        card("F3", "Price, substitution and income effects",
             tbl(["Point", "Session price", "Income", "Sessions"], [["C", "18", "144", "4"], ["J", "8", "144", "9"], ["K", "8", "96", "6"]]),
             ex("Price falls 18 → 8", "Price effect  C → J: 4 → 9  (+5)\nSubstitution  C → K: 4 → 6  (+2)  (income cut 48 to stay on old curve)\nIncome effect K → J: 6 → 9  (+3)\nCheck: 2 + 3 = 5"),
             tbl(["Good", "Substitution effect of a price fall", "Income effect"], [["Normal", "Buy more", "Buy more"], ["Inferior", "Buy more", "<b>Buy less</b>"]]),
             hook("Mnemonic", "<b>Substitution always Sides with the cheaper good</b>; only the income effect can reverse."),
             trap("Trap", "An upward-sloping demand curve needs an inferior good whose income effect outweighs the substitution effect: extremely rare.")),
    ),
    clues=[("Income ÷ price of the good on the y-axis", "Real income (the y-intercept)"),
           ("Ratio of the two prices", "Relative price (slope of the budget line)"),
           ("Straight-line indifference curves", "Perfect substitutes"),
           ("L-shaped indifference curves", "Perfect complements"),
           ("MRS equals relative price, on the budget line", "Best affordable choice"),
           ("Price falls but income adjusted to stay on the old curve", "Substitution effect")],
    qs=[("Calculation · Ch 9", "Rakan's income is 144, a session costs 18 and fruit 12/kg. Write the budget equation, his real income in fruit and the relative price. What happens if income falls to 72?",
         "<p>18Q<sub>s</sub> + 12Q<sub>f</sub> = 144, so Q<sub>f</sub> = 12 − 1.5Q<sub>s</sub>. Real income = 144/12 = <b>12 kg</b>; relative price = 18/12 = <b>1.5</b>.</p>"
         "<p>At 72: parallel shift inward, same slope 1.5, real income <b>6 kg</b> (at most 4 sessions).</p>"),
        ("Short answer · Ch 9", "Split the effect of the session price falling from 18 to 8 into substitution and income effects.",
         "<p>Total price effect: 4 → 9 sessions (+5). Cutting income to 96 keeps him on the original curve: he picks 6 sessions, so the <b>substitution effect is +2</b>. Restoring the 48 SAR moves him to 9: <b>income effect +3</b>. Both positive, so sessions are a normal good.</p>")],
)

CHAPTERS[11] = dict(
    id="ch11", n="11", tab="Output & costs", num="CHAPTER 11 · OUTPUT AND COSTS",
    title="Product curves, cost curves and Qamar Bakery", links=links("11-output-and-costs", "11-output-and-costs-quiz") + [("Qamar step by step", f"{BASE}extra-resources/chapter-11-qamar-bakery-step-by-step/")],
    lead="The handwriting: \"all cost curves and shapes are important\", and you \"will be asked why MC is important\". Practise filling in the Qamar table.",
    body=grid(
        card("1", "Time frames and sunk cost",
             tbl(["", "Short run", "Long run"], [["Inputs", "At least one <b>fixed</b> (the plant)", "<b>All</b> variable"], ["Qamar", "Fixed kitchen, choose bakers", "Could move kitchen"]]),
             p("A <b>sunk cost</b> can't be recovered and shouldn't affect today's decisions (the 25,000 SAR counter).")),
        card("F1", "Product (rent 960/day, baker 360/day)",
             tbl(["Bakers", "TP", "MP", "AP"], [["1", "12", "12", "12"], ["2", "30", "<b>18</b>", "<b>15</b>"], ["3", "40", "10", "13.3"], ["4", "48", "8", "12"], ["5", "54", "6", "10.8"]]),
             eq("MP = ΔTP ÷ ΔL", "AP = TP ÷ L"),
             p("Increasing then <b>diminishing marginal returns</b> (shared ovens). MP crosses AP at AP's maximum.")),
        card("F2", "Cost formulas",
             eq("TC = TFC + TVC", "MC = ΔTC ÷ ΔQ", "ATC = AFC + AVC"),
             tbl(["Bakers", "Q", "TC", "AFC", "AVC", "ATC", "MC"], [["1", "12", "1,320", "80", "30", "110", "30"], ["2", "30", "1,680", "32", "<b>24</b>", "56", "20"],
                                                                     ["3", "40", "2,040", "24", "27", "51", "36"], ["4", "48", "2,400", "20", "30", "<b>50</b>", "45"],
                                                                     ["5", "54", "2,760", "17.8", "33.3", "51.1", "60"]]),
             ex("MC of the 2nd baker's cakes", "ΔTC = 1,680 − 1,320 = 360   ΔQ = 30 − 12 = 18\nMC = 360 ÷ 18 = 20 SAR per cake")),
        card("2", "Shapes",
             tbl(["Curve", "Shape", "Why"], [["TFC", "Horizontal", "Doesn't change"], ["AFC", "Always falls", "960 spread over more"],
                                            ["AVC", "U, min 24 at 30 cakes", "Mirror of AP"], ["ATC", "U, min 50 at 48 cakes", "AFC falls vs AVC rises"], ["MC", "Falls then rises", "Mirror of MP"]]),
             hook("Mnemonic", "<b>Marginal Meets the Minimum</b>: MC cuts AVC and ATC at their lowest points."),
             p("<b>Why MC matters:</b> it decides whether one more unit is worth producing; every later chapter compares it with MR.")),
        card("3", "Shifts",
             tbl(["Change", "Shifts", "Doesn't shift"], [["Fixed cost up (rent 960 → 1,200)", "TFC, TC, AFC, ATC", "<b>MC, AVC</b>"],
                                                        ["Wages up", "TVC, TC, AVC, ATC, <b>MC</b>", "AFC"], ["Better technology", "All cost curves down", ""]]),
             ex("Rent rises to 1,200", "At 48 cakes: AFC 20 → 25, ATC 50 → 55; MC and AVC unchanged"),
             trap("Trap", "A fixed-cost rise never moves MC: fixed cost doesn't change with output.")),
    ),
    clues=[("At least one input fixed", "Short run"),
           ("Past cost that can't be recovered", "Sunk cost: ignore it"),
           ("Each extra worker adds less output", "Diminishing marginal returns"),
           ("Curve that always falls", "AFC"),
           ("Where MC meets AVC and ATC", "At their minimum points"),
           ("Rent rises", "TFC, TC, AFC, ATC shift; MC and AVC don't")],
    qs=[("Calculation · Ch 11", "Qamar Bakery: what is the MC of the cakes made by the 3rd baker, and the ATC with 4 bakers?",
         "<p>3rd baker: ΔTC = 2,040 − 1,680 = 360, ΔQ = 40 − 30 = 10 → MC = <b>36 SAR</b>.</p><p>4 bakers: ATC = 2,400 ÷ 48 = <b>50 SAR</b> (the minimum).</p>"),
        ("Short answer · Ch 11", "Why is the ATC curve U-shaped?",
         "<p>Two forces: <b>AFC falls</b> as the fixed cost is spread over more output, and <b>AVC eventually rises</b> because of diminishing returns. Up to 48 cakes the falling AFC wins, then the rising AVC wins.</p>")],
)

CHAPTERS[12] = dict(
    id="ch12", n="12", tab="Perfect competition", num="CHAPTER 12 · PERFECT COMPETITION",
    title="Price taker, MR = MC, profit and shutdown", links=links("12-perfect-competition", "12-perfect-competition-quiz"),
    lead="Every cost curve from Chapter 11 comes together here; profit, break-even, loss and shutdown are exam staples. Al-Bustan Farm's numbers check each rule.",
    body=grid(
        card("1", "Conditions and the price taker",
             steps("Many firms, <b>identical</b> products", "Free entry and exit", "No advantage for existing firms", "Well-informed buyers and sellers"),
             p("Al-Bustan sells dates at 60 SAR a box: its demand is <b>horizontal</b> at 60, so <b>MR = P = 60</b>. Economic profit = TR − TC, where TC includes <b>normal profit</b>."),
             trap("Trap", "Only the single firm's demand is horizontal; the market demand slopes down.")),
        card("F1", "Output rule",
             eq("MR = MC (on the rising part of MC)"),
             tbl(["Boxes", "TR", "TC", "Profit", "MC"], [["5", "300", "210", "90", "32"], ["6", "360", "246", "114", "36"], ["<b>7</b>", "420", "294", "<b>126</b>", "48"],
                                                         ["8", "480", "366", "114", "72"]]),
             p("7th box: +60 revenue, 48 cost → profit +12. 8th: costs 72 &gt; 60 → stop at <b>7 boxes, profit 126</b>. Rising MC above min AVC = the firm's <b>supply curve</b>.")),
        card("F2", "Profit, break even, loss",
             eq("Profit = (P − ATC) × Q"),
             tbl(["Price", "Output", "ATC", "Result"], [["60", "7", "42", "Profit (60 − 42) × 7 = 126"], ["41", "6", "41 (min)", "Break even"],
                                                       ["34", "5", "42", "Loss (42 − 34) × 5 = 40 = TFC"]])),
        card("2", "Shutdown",
             tbl(["Price vs costs", "Decision"], [["P &gt; ATC", "Produce, profit"], ["ATC &gt; P &gt; AVC", "Produce in the short run (loss &lt; TFC)"],
                                                  ["P = min AVC", "Shutdown point (indifferent)"], ["P &lt; AVC", "<b>Shut down</b>"]]),
             p("Al-Bustan's shutdown point: <b>34 SAR at 5 boxes</b>, where the loss equals TFC (40)."),
             hook("Mnemonic", "<b>Cover Variable, or Close.</b>"),
             trap("Trap", "A loss doesn't mean shut down: stay open while price covers AVC.")),
    ),
    clues=[("Firm's demand is horizontal at the market price", "Perfect competition: price taker, MR = P"),
           ("P greater than ATC at MR = MC", "Economic profit"),
           ("P between AVC and ATC", "Produce in the short run at a loss"),
           ("P below minimum AVC", "Shut down"),
           ("Zero economic profit", "Break even: still earning normal profit")],
    qs=[("Decision · Ch 12", "The date price falls to 38. Should Al-Bustan produce, and why?",
         "<p>Yes. 38 is above minimum AVC (34), so producing (6 boxes) loses less than shutting down, which would lose the whole TFC of 40.</p>"),
        ("Short answer · Ch 12", "Why is MR equal to price for a perfectly competitive firm?",
         "<p>The firm is a price taker: it can sell any amount at the market price, so each extra unit adds exactly the price to total revenue.</p>")],
)

CHAPTERS[13] = dict(
    id="ch13", n="13", tab="Monopoly", num="CHAPTER 13 · MONOPOLY",
    title="Barriers, MR below price, and the four-step graph", links=links("13-monopoly", "13-monopoly-quiz"),
    lead="The graph is the heart of this chapter. The handwriting: find where MR and MC intersect, go up to demand for the price, profit = (P − ATC) × Q.",
    body=grid(
        card("1", "How monopoly arises",
             p("No close substitutes (Saudi Electricity) + a <b>barrier to entry</b>:"),
             tbl(["Barrier", "Example"], [["<b>N</b>atural (economies of scale)", "Electricity, water"], ["<b>O</b>wnership of a key resource", "Diamond mines"],
                                         ["<b>Le</b>gal", "Franchise, licence, patent, copyright"]]),
             hook("Mnemonic", "<b>NOLe</b> barriers.")),
        card("F1", "Why MR &lt; P (Sahra Tours)",
             tbl(["Tours", "P", "TR", "MR", "MC", "ATC", "Profit"], [["2", "160", "320", "140", "15", "125", "70"], ["3", "140", "420", "100", "20", "90", "150"],
                                                                     ["<b>4</b>", "<b>120</b>", "480", "60", "30", "<b>75</b>", "<b>180</b>"], ["5", "100", "500", "20", "50", "70", "150"],
                                                                     ["6", "80", "480", "−20", "90", "73.3", "40"]]),
             ex("2 → 3 tours", "Gain: 3rd tour sells for 140\nLoss: first 2 now 20 cheaper → −40\nMR = 140 − 40 = 100 < price 140")),
        card("F2", "Four-step graph",
             steps("Output where <b>MR = MC</b>: 4 tours.", "Go <b>up to demand</b> for the price: 120.", "ATC at that output: 75.", "Profit = (120 − 75) × 4 = <b>180</b>."),
             hook("Mnemonic", "<b>Cross, then Climb.</b>"),
             trap("Trap", "The MR = MC intersection gives the <b>quantity</b>, not the price. Reading 40 as the price is the most common graph mistake.")),
        card("2", "Monopoly vs perfect competition",
             tbl(["", "Perfect competition", "Monopoly"], [["P vs MR", "P = MR", "P &gt; MR"], ["At best output", "P = MC", "<b>P &gt; MC</b>"],
                                                          ["Profit lasts?", "No: entry", "<b>Yes: barriers</b>"]])),
    ),
    clues=[("Only seller, no close substitutes, barrier to entry", "Monopoly"),
           ("Economies of scale let one firm supply the market", "Natural monopoly"),
           ("Patent, licence, public franchise", "Legal barrier"),
           ("Must cut price on all units to sell one more", "MR below price"),
           ("Price read from the demand curve above MR = MC", "Monopoly price")],
    qs=[("Calculation · Ch 13", "From Sahra's table, find MR from 4 to 5 tours and explain why the 5th tour isn't run.",
         "<p>TR rises from 480 to 500 → <b>MR = 20</b>. MC of the 5th tour is 50 &gt; 20, so profit falls by 30 (180 → 150).</p>"),
        ("Short answer · Ch 13", "Why can a monopoly keep its economic profit in the long run?",
         "<p>Barriers to entry (natural, ownership or legal) stop new firms entering, so nothing competes the profit away.</p>")],
)

CHAPTERS[14] = dict(
    id="ch14", n="14", tab="Monopolistic competition", num="CHAPTER 14 · MONOPOLISTIC COMPETITION",
    title="Differentiated products and the three market structures", links=links("14-monopolistic-competition", "14-monopolistic-competition-quiz"),
    lead="Short, and it ends with the comparison table of all three market structures: a natural final-exam question.",
    body=grid(
        card("1", "Features",
             ul("A large number of firms (small shares, no collusion)", "Compete on <b>quality, price and marketing</b>", "Free entry and exit"),
             p("Bunn Café's coffee is a close but imperfect substitute for others', so it faces a <b>downward-sloping demand</b> and has some control over price.")),
        card("F1", "Short run (acts like a monopoly)",
             tbl(["Season", "Output", "P", "ATC", "Result"], [["Busy", "200", "30", "14", "Profit (30 − 14) × 200 = 3,200"], ["Slow (summer)", "50", "10", "14", "Loss (14 − 10) × 50 = 200"]]),
             steps("MR = MC for output", "Up to demand for price", "ATC at that output", "(P − ATC) × Q")),
        card("2", "Long run",
             p("Profit attracts new cafés; losses make some exit. Either way, firms <b>break even</b> in the long run."),
             hook("Mnemonic", "<b>Profit Pulls entrants, Loss Lets firms leave.</b>"),
             trap("Trap", "\"Monopoly\" is in the name, but free entry removes profit in the long run.")),
        card("3", "The three market structures",
             tbl(["", "Perfect comp.", "Monopolistic comp.", "Monopoly"], [["Firms", "Many", "Many", "One"], ["Product", "Identical", "<b>Differentiated</b>", "No close substitutes"],
                                                                         ["Barriers", "None", "None", "Natural, ownership, legal"],
                                                                         ["Firm's demand", "Horizontal", "<b>Slopes down</b>", "Market demand"],
                                                                         ["Output rule", "MR = MC", "MR = MC", "MR = MC"], ["Profit lasts?", "No", "<b>No</b>", "<b>Yes</b>"],
                                                                         ["Example", "Date farms", "Cafés, abaya shops", "Only water supplier"]]),
             hook("Mnemonic", "<b>Everyone uses MR = MC.</b> What changes is the demand curve and whether entry is possible.")),
    ),
    clues=[("Many firms, differentiated products, free entry", "Monopolistic competition"),
           ("Firms compete on quality, price and marketing", "Monopolistic competition"),
           ("Profit in the short run attracts entry", "Long-run break even (monopolistic or perfect competition)"),
           ("Only structure that keeps profit in the long run", "Monopoly")],
    qs=[("Calculation · Ch 14", "In summer Bunn Café sells 50 cups at 10 SAR with ATC 14. Profit or loss, and what happens in the long run if this lasts?",
         "<p>(10 − 14) × 50 = <b>−200 SAR a day</b>, a loss. If losses persist, some cafés exit; the rest gain customers until they break even.</p>"),
        ("Compare · Ch 14", "Name two ways monopolistic competition is like monopoly and two ways it is like perfect competition.",
         "<p>Like monopoly: <b>downward-sloping demand</b> and the same short-run graph (MR = MC, price from demand). Like perfect competition: <b>many firms</b> and <b>free entry</b>, so profit disappears in the long run.</p>")],
)


# ------------------------------------------------------------------ sheets
def plan_panel(code, title, lead, cards, chapters):
    rows = [[c, a, str(n)] for n in chapters for c, a in CHAPTERS[n]["clues"]]
    body = grid(*cards) + group("Question clue → answer") + tbl(["If the question says…", "Answer", "Chapter"], rows, numcol=2)
    return dict(id="plan", n="00", tab="Exam plan", num="EXAM PLAN", title=title, lead=lead, body=body)


def practice_panel(chapters):
    body = "".join(q(tag, ask, ans) for n in chapters for tag, ask, ans in CHAPTERS[n]["qs"])
    return dict(id="practice", n="Q", tab="Practice", num="PRACTICE", title="Exam-style questions with worked answers",
                lead="Answer each one on paper first, then open the answer. <b>Show all answers</b> at the top opens every one.", body=body)


MCQ = card("A", "Multiple choice",
           steps("Underline the trigger word: <i>own price</i>, <i>substitute</i>, <i>inferior</i>, <i>below equilibrium</i>, <i>elastic</i>.",
                 "Decide the curve or the formula <b>before</b> reading the options.", "Cross out options that confuse a movement with a shift, or MR with price.",
                 "For a number, compute it in the margin; most wrong options are the inverse or the forgotten average."))
SHORT = card("B", "Short answer",
             steps("<b>Define</b> the term in one sentence from the slides.", "<b>Apply</b> it to the case in the question (name the curve, the shift, the direction).",
                   "<b>Show</b> the numbers or the steps if there are any.", "<b>Conclude</b> with the effect on price, quantity, revenue or profit."))
CALC = card("C", "Calculations",
            steps("Write the formula in words first.", "Show each step on its own line; <b>never round in the middle</b> (the handwriting).",
                  "Report elasticity as a <b>positive</b> number, and interpret it.", "State the unit (SAR, units, %)."),
            hook("Check", "Elasticity with the midpoint method: going up or down must give the same answer."))
EQN = card("C", "Equation questions (Chapter 6)",
           steps("Solve the free market first: set demand = supply.", "Apply the policy: plug the ceiling / floor into both equations, or use the wedge for a tax.",
                 "Read buyers' and sellers' prices from each equation.", "Revenue = tax × Q; DWL = ½ × tax (or price gap) × ΔQ."),
           hook("Check", "A ceiling above equilibrium or a floor below it changes nothing."))
GRAPH = card("D", "Graph questions",
             steps("Label both axes and every curve.", "MR = MC gives quantity; climb to demand for price (monopoly, monopolistic competition).",
                   "Shade profit as (P − ATC) × Q.", "For indifference curves: tangency where MRS = relative price."))

SHEETS = [
    dict(slug="major-1", brand="Major 1", title="ECON101 | Major 1 Cheat Sheet", h1="Major 1 cheat sheet",
         eyebrow="ECON101 · Major 1 · Chapters 2, 3, 4",
         desc="ECON101 Major 1 cheat sheet for chapters 2 to 4: PPF and opportunity cost, comparative advantage, demand and supply shifters, equilibrium, elasticity calculations and the total revenue test, with exam-style practice and worked answers.",
         intro="Built around how the instructor tests these chapters: MCQ on PPF graphs, opportunity cost and comparative versus absolute advantage; headline questions on shifts; and step-by-step elasticity calculations reported as positive numbers. Covers Chapter 2, Chapter 3 and Chapter 4.",
         chapters=[2, 3, 4],
         plan=plan_panel("Major 1", "How each question type is marked, and how to answer it",
                         "The practice major mirrors the format: mostly multiple choice, plus a few short answers that ask you to explain and connect.",
                         [MCQ, SHORT, CALC], [2, 3, 4]),
         practice=practice_panel([2, 3, 4]),
         footer="Built from the ECON101 slides for chapters 2–4 (Parkin, <i>Microeconomics</i>, 14th Global Edition), the instructor's handwriting on them, and the course's worked examples. Every number was recomputed. Shoug Alomran."),
    dict(slug="major-2", brand="Major 2", title="ECON101 | Major 2 Cheat Sheet", h1="Major 2 cheat sheet",
         eyebrow="ECON101 · Major 2 · Chapters 6, 8, 9",
         desc="ECON101 Major 2 cheat sheet for chapters 6, 8 and 9: ceilings, floors, taxes, quotas and subsidies with the equation method, utility tables and the marginal rule, budget lines, indifference curves and income and substitution effects, with worked answers.",
         intro="Built around the instructor's notes: Chapter 6 is solved with equations every time, Chapter 8 is section D with no graphing (calculations from utility tables), and Chapter 9 needs both the calculations and the graphs. Covers Chapter 6, Chapter 8 and Chapter 9.",
         chapters=[6, 8, 9],
         plan=plan_panel("Major 2", "How each question type is marked, and how to answer it",
                         "Expect equation work for government policies, table work for utility, and graph reading for indifference curves.",
                         [MCQ, EQN, CALC, GRAPH], [6, 8, 9]),
         practice=practice_panel([6, 8, 9]),
         footer="Built from the ECON101 slides for chapters 6, 8 and 9 (Parkin, <i>Microeconomics</i>, 14th Global Edition), the instructor's handwriting on them, and the course's worked examples (Huda, Rakan). Every number was recomputed. Shoug Alomran."),
    dict(slug="final", brand="Final", title="ECON101 | Final Exam Cheat Sheet", h1="Final exam cheat sheet",
         eyebrow="ECON101 · Final · Chapters 3–6, 8, 9, 11–14",
         desc="ECON101 final exam cheat sheet: demand and supply, elasticity, efficiency, government actions, utility and indifference curves, costs, perfect competition, monopoly and monopolistic competition, with a clue-to-answer table and worked practice.",
         intro="The whole course on one page: the market model (Chapters 3–6), consumer choice (Chapters 8–9), and firms and market structures (Chapters 11–14). Start with the exam plan and the clue table, then work through each chapter's tab and finish with the practice questions.",
         chapters=[3, 4, 5, 6, 8, 9, 11, 12, 13, 14],
         plan=plan_panel("Final", "How each question type is marked, and how to answer it",
                         "A comprehensive paper: MCQ across every chapter, calculations (elasticity, policies, utility, costs, profit), and graph reading for indifference curves and market structures.",
                         [MCQ, SHORT, CALC, GRAPH], [3, 4, 5, 6, 8, 9, 11, 12, 13, 14]),
         practice=practice_panel([3, 4, 5, 6, 8, 9, 11, 12, 13, 14]),
         footer="Built from the ECON101 slides for chapters 3–6, 8, 9 and 11–14 (Parkin, <i>Microeconomics</i>, 14th Global Edition), the instructor's handwriting on them, and the course's worked examples (Huda, Rakan, Qamar Bakery, Al-Bustan Farm, Sahra Tours, Bunn Café). Every number was recomputed. Shoug Alomran."),
]
