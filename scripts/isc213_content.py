#!/usr/bin/env python3
"""Content for the ISC213 study pages.

Everything here is drawn from the four ISC213 lecture decks and the lecture
slide-breakdown pages that sit alongside them. Kept apart from the renderer so
adding a lecture means editing data, not markup.

Node = (label, note, [children]) for the mindmap.
MCQ  = (question, source, [options], correct_index, explanation).
Written = (question, source, model_answer_html).
"""

# --------------------------------------------------------------------------- #
# Cheat sheet 1 — Lectures 1 & 2
# --------------------------------------------------------------------------- #

CHEAT_1_META = {
    'slug': 'cheat-sheet-1',
    'title': 'Cheat Sheet 1 — Lectures 1 &amp; 2',
    'brand_sub': 'Concept, Characteristics, Ijtihad &amp; Rights — Lectures 1–2',
    'h1': 'Cheat Sheet 1: Concept, Characteristics, Ijtihad &amp; Rights',
    'lede': ('Everything from Lectures 1 and 2 compressed to what you would want on one page the hour '
             'before Major 1 — definitions in their exam wording, every numbered list with its mnemonic, '
             'and the traps that separate the categories students keep swapping.'),
    'meta': [('2', 'lectures covered'), ('9', 'quick-reference blocks'), ('24', 'flashcards')],
}

CHEAT_1_SECTIONS = [
    {
        'id': 's1', 'tag': 'Lecture 1 · Block 1–3', 'num': '01',
        'h2': 'The three roots of the term',
        'body': '''
<div class="term-row"><span class="term">Transactions</span><span>The lawful rules regulating financial dealings carried out between people.</span></div>
<div class="term-row"><span class="term">Finance</span><span>From "money" — anything with material value among people, whose use is permitted, given ease and free choice.</span></div>
<div class="term-row"><span class="term">Contemporary</span><span>The recent, modern age. A one-line definition — do not overthink it.</span></div>
<div class="callout mnemonic"><div class="callout-label">Mnemonic — T.F.C.</div>
"Trading Follows Custom." Transactions (the rules) + Finance (the value) + Contemporary (the era). If you can say what each word contributes alone, you can rebuild the full definition from scratch.</div>

<h3>Transactions split into four categories</h3>
<div class="card-grid">
  <div class="mini-card"><span class="mini-key">B</span><div class="mini-title">Bargains</div>Sale and leasing.</div>
  <div class="mini-card"><span class="mini-key">D</span><div class="mini-title">Donations</div>Grants, will, and endowment (waqf).</div>
  <div class="mini-card"><span class="mini-key">D</span><div class="mini-title">Dropping</div>Ending an obligation — e.g. abolishing a debt.</div>
  <div class="mini-card"><span class="mini-key">D</span><div class="mini-title">Documentation</div>Mortgage, bail (warranty), draft (transfer of debt).</div>
</div>
<div class="callout mnemonic"><div class="callout-label">Mnemonic — B.D.D.D.</div>
Buy it, Donate it, Drop it, Document it.</div>
<div class="callout mistake"><div class="callout-label">Common mistake</div>
Dropping <em>ends</em> a right (nothing is exchanged). Documentation <em>protects</em> a right (the obligation still stands). Waqf is a gift with no return, so it is a Donation, never a Bargain.</div>
''',
    },
    {
        'id': 's2', 'tag': 'Lecture 1 · Block 4–5', 'num': '02',
        'h2': 'The full definition and its four cases',
        'body': '''
<div class="quote">"They are financial cases which emerged in the contemporary age — cases that changed in their rules because of progress or changed circumstances, and cases that bear new names, or consist of many old forms."<cite>Definition of Current Financial Transactions</cite></div>
<div class="callout mnemonic"><div class="callout-label">Mnemonic</div>
NEW &middot; CHANGED &middot; RENAMED &middot; COMBINED — four words, and you have the definition without memorising it verbatim.</div>

<div class="table-scroll"><table class="rule-table">
<caption>Identifying the definition — the four cases</caption>
<thead><tr><th>#</th><th>Case</th><th>What changed</th><th>Textbook example</th></tr></thead>
<tbody>
<tr><td>1</td><td>Cases unknown in earlier ages</td><td>The transaction itself is new</td><td>Corporate companies, banknotes</td></tr>
<tr><td>2</td><td>Rules updated due to progress</td><td>The <em>procedure</em></td><td>Handing over the key to transfer property is no longer required now that Property Registry Offices exist</td></tr>
<tr><td>3</td><td>New names, same old ruling</td><td>Only the <em>label</em></td><td>Bank "interest" is still riba</td></tr>
<tr><td>4</td><td>Formulated from several old forms</td><td>Classical contracts <em>combined</em></td><td>Murabaha; leasing contracts merging selling and renting</td></tr>
</tbody></table></div>
<div class="callout mnemonic"><div class="callout-label">Mnemonic — N.U.R.C.</div>
New &rarr; Updated procedure &rarr; Renamed &rarr; Combined.</div>
<div class="callout mistake"><div class="callout-label">Common mistake</div>
Cases 2 and 3 get swapped constantly. Ask one question: did the <strong>process</strong> change (case 2, key &rarr; registry), or just the <strong>name</strong> (case 3, interest &rarr; riba)?</div>
<div class="quote">"People among my Ummah will drink Khamr, calling it by another name."<cite>The Prophet &#65018;</cite></div>
''',
    },
    {
        'id': 's3', 'tag': 'Lecture 1 · Block 6', 'num': '03',
        'h2': 'Relevant terms',
        'body': '''
<p>Four near-synonyms jurisprudents use for "a newly emerged issue that needs a ruling." Recognise them as one set; you are not asked to split hairs between them.</p>
<div class="card-grid">
  <div class="mini-card"><div class="mini-title">Emerged cases</div></div>
  <div class="mini-card"><div class="mini-title">Occurrences</div></div>
  <div class="mini-card"><div class="mini-title">Incidences</div></div>
  <div class="mini-card"><div class="mini-title">Fatwa</div></div>
</div>
<div class="callout mnemonic"><div class="callout-label">Mnemonic — E.O.I.F.</div>
Emerged, Occurrences, Incidences, Fatwa.</div>
''',
    },
    {
        'id': 's4', 'tag': 'Lecture 1 · Block 7–11', 'num': '04',
        'h2': 'Four characteristics of transactions in Islamic jurisprudence',
        'body': '''
<div class="callout mnemonic"><div class="callout-label">Mnemonic — "Please Permit Reasonable Flexibility"</div>
<strong>P</strong>rinciples (general, not detailed) &rarr; <strong>P</strong>ermissibility (the default ruling) &rarr; <strong>R</strong>easoning (benefit-driven) &rarr; <strong>F</strong>lexible-yet-fixed.</div>

<h3>1 — Based on general bases and principles</h3>
<p>Same divine source as worship (Qur'an + Sunnah), but legislated as broad principles and integrity rules rather than exhaustive detail — deliberately leaving room for ijtihad on newly introduced forms.</p>
<div class="callout evidence"><div class="callout-label">Evidence</div>
<strong>a.</strong> An-Nisaa 4:29 — do not consume one another's wealth unjustly, but only in lawful business <em>by mutual consent</em>.<br>
<strong>b.</strong> Al-Baqarah 2:275 — "Allah has permitted trade and has forbidden interest (riba)."<br>
<strong>c.</strong> Hadith (Ibn Omar) — the Prophet &#65018; prohibited the <em>gharar</em> sale: no guarantee the seller can deliver (a runaway slave, fish still in the sea, an unborn camel).</div>
<div class="callout mnemonic"><div class="callout-label">Mnemonic</div>
"Mutual Consent, No Riba, No Gharar" — the three evidences map to three red flags.</div>

<h3>2 — The original rule is permissibility (al-ib&#257;&#7717;ah)</h3>
<div class="table-scroll"><table class="rule-table">
<thead><tr><th></th><th>Acts of worship</th><th>Transactions / contracts</th></tr></thead>
<tbody>
<tr><td>Default</td><td>Restricted</td><td>Permitted</td></tr>
<tr><td>Rule</td><td>Nothing added unless a text permits it</td><td>Nothing forbidden unless a truthful, clear text prohibits it</td></tr>
<tr><td>Reason</td><td>Avoids inventing new religious practice (bid'ah)</td><td>No evidence of prohibition = permissible</td></tr>
</tbody></table></div>
<div class="callout evidence"><div class="callout-label">Evidence</div>
"If anyone introduces in our matter something which does not belong to it, it will be rejected." (restriction principle, for worship) &mdash; and the Qur'anic subjection of the sea, heavens, and earth to people, so they may seek His bounty.</div>

<h3>3 — Based on reasons and benefits (ta'l&#299;l / ma&#7779;la&#7717;ah)</h3>
<p>Rulings on transactions are caused and benefit-bearing, which is exactly why they can be extended by analogy to cases the texts never named.</p>

<h3>4 — Both flexible and constant</h3>
<p>Constant in its fixed principles and prohibitions; flexible in the forms and procedures those principles are applied to.</p>
''',
    },
    {
        'id': 's5', 'tag': 'Lecture 2 · Block 1', 'num': '05',
        'h2': 'The nine qualifications of a researcher',
        'body': '''
<p>Resolving an emerging financial issue depends on <strong>ijtihad</strong> — the total effort of a qualified jurist (mujtahid) to deduce a ruling from detailed scriptural evidence. Nine requirements gate that.</p>
<div class="card-grid">
  <div class="mini-card"><span class="mini-key">Q</span><div class="mini-title">Qur'an</div>Comprehensive understanding of it.</div>
  <div class="mini-card"><span class="mini-key">H</span><div class="mini-title">Hadith</div>Comprehensive understanding of the Sunnah.</div>
  <div class="mini-card"><span class="mini-key">I</span><div class="mini-title">Ijma'</div>Knowledge of legal consensus, so no ruling contradicts a settled one.</div>
  <div class="mini-card"><span class="mini-key">A</span><div class="mini-title">Arabic</div>Grammar, rhetoric, vocabulary, linguistic nuance.</div>
  <div class="mini-card"><span class="mini-key">S</span><div class="mini-title">Skill of ijtihad</div>A jurisprudence talent for understanding fiqh issues.</div>
  <div class="mini-card"><span class="mini-key">H</span><div class="mini-title">Honesty</div>In word and action — avoiding major sins, not persisting in minor ones.</div>
  <div class="mini-card"><span class="mini-key">M</span><div class="mini-title">Maqasid awareness</div>Preserving faith, life, intellect, lineage, and wealth.</div>
  <div class="mini-card"><span class="mini-key">R</span><div class="mini-title">Research ability</div>Eliciting rulings from contemporary scholars' books.</div>
  <div class="mini-card"><span class="mini-key">U</span><div class="mini-title">Understanding reality</div>Lived circumstances, so rulings apply effectively.</div>
</div>
<div class="callout mnemonic"><div class="callout-label">Mnemonic — two groups</div>
Knowledge base <strong>QHIA</strong> (Qur'an, Hadith, Ijma', Arabic), then practical qualities <strong>SHMRU</strong> (Skill, Honesty, Maqasid, Research, Understanding reality).</div>
<div class="callout mistake"><div class="callout-label">Common mistake</div>
Listing only the book knowledge and dropping the character items. Honesty, maqasid awareness, and lived reality are graded just as often.</div>
''',
    },
    {
        'id': 's6', 'tag': 'Lecture 2 · Block 2', 'num': '06',
        'h2': 'The eight steps to a ruling',
        'body': '''
<p>Sequence matters — questions ask what comes right after a given step.</p>
<ol>
  <li><strong>Pray</strong> to Allah for inspiration and right foresight on the case.</li>
  <li><strong>Understand</strong> the subject deeply — what allows a confident judgment.</li>
  <li><strong>Search</strong> the legal texts: the Qur'an and the Sunnah.</li>
  <li>Examine the case against the <strong>Companions'</strong> sayings and arguments.</li>
  <li>Search the jurisprudence of the four <strong>imams</strong> / schools.</li>
  <li>Search new <strong>sources</strong> — recent scholars' articles.</li>
  <li>Use his own <strong>opinion</strong>, if steps 1–6 have not settled it.</li>
  <li>If no legitimate rule can be reached at all: <strong>refrain</strong> from ruling — no fatwa.</li>
</ol>
<div class="callout mnemonic"><div class="callout-label">Mnemonic</div>
"Pious Understanding Searches Companions, Imams, Sources, forms an Opinion, or else Refrains."</div>
<div class="callout mistake"><div class="callout-label">Common mistake</div>
Personal opinion is the <em>second-to-last</em> resort, not an early step. And if opinion cannot produce a legitimate rule, the correct move is to refrain — not to guess.</div>
''',
    },
    {
        'id': 's7', 'tag': 'Lecture 2 · Block 3–6', 'num': '07',
        'h2': 'The rights hierarchy',
        'body': '''
<div class="quote">"An exclusive entitlement by which the Law (Shar&#299;'ah) establishes an authority or an obligation."<cite>Definition of Rights</cite></div>
<p>Two possible shapes: an <strong>authority</strong> (you are empowered) or an <strong>obligation</strong> (someone else is bound toward you). Everything below is just: which kind of authority, over what.</p>

<ul class="node-list">
  <li class="node"><span class="node-label">Political rights</span><span class="node-note">Organise governance and its authorities — the right of election and nomination.</span></li>
  <li class="node"><span class="node-label">Civil rights</span><span class="node-note">Establish the individual's interests directly.</span>
    <ul class="node-list">
      <li class="node"><span class="node-label">General rights</span><span class="node-note">Inherent personality rights — bodily safety, inviolability of one's residence. Denying them degrades human dignity.</span></li>
      <li class="node"><span class="node-label">Private rights</span><span class="node-note">Arise from bonds between individuals, under private law.</span>
        <ul class="node-list">
          <li class="node"><span class="node-label">Family rights</span><span class="node-note">Governed by personal-affairs rules — custody, divorce.</span></li>
          <li class="node"><span class="node-label">Financial rights</span><span class="node-note">Rights that could be evaluated with money.</span></li>
        </ul>
      </li>
    </ul>
  </li>
</ul>
<div class="callout mnemonic"><div class="callout-label">Mnemonics down the chain</div>
Political = you and the <em>state</em>; Civil = you and your <em>own interests</em>. General = rights you hold just by being human; Private = rights that need a second party. Family = cannot be priced; Financial = can be priced.</div>
''',
    },
    {
        'id': 's8', 'tag': 'Lecture 2 · Block 7', 'num': '08',
        'h2': 'The three financial rights',
        'body': '''
<div class="card-grid">
  <div class="mini-card"><span class="mini-key">P — People</span><div class="mini-title">Personal rights</div>A law relation between two people, like creditor and debtor. Also called "commitments."</div>
  <div class="mini-card"><span class="mini-key">M — Matter</span><div class="mini-title">Material rights</div>A direct authority given by law over a material thing. Also called "property rights."</div>
  <div class="mini-card"><span class="mini-key">I — Ideas</span><div class="mini-title">Incorporeal rights</div>The "rights of innovation" — authority over something non-physical, like intellectual creations.</div>
</div>
<div class="callout mistake"><div class="callout-label">Common mistake</div>
Personal and Material get confused because both seem to involve another person. The test: does the right point at a person's <strong>obligation</strong> (Personal — someone owes you money) or at a <strong>thing</strong> (Material — you own the land)? If neither a physical thing nor another's debt is involved, it is Incorporeal.</div>
''',
    },
    {
        'id': 's9', 'tag': 'Exam radar', 'num': '09',
        'h2': 'Highest-yield items for Major 1',
        'body': '''
<div class="table-scroll"><table class="rule-table">
<caption>What to check last, in order of how often it is tested</caption>
<thead><tr><th>Item</th><th>Say it in one line</th></tr></thead>
<tbody>
<tr><td>The four cases (N.U.R.C.)</td><td>New &rarr; Updated procedure &rarr; Renamed &rarr; Combined, each with its example.</td></tr>
<tr><td>Worship vs. transactions</td><td>Worship: restricted by default. Transactions: permitted by default.</td></tr>
<tr><td>The four categories (B.D.D.D.)</td><td>Bargains, Donations, Dropping, Documentation.</td></tr>
<tr><td>Step 7 vs. step 8</td><td>Own opinion comes second-to-last; refraining is the true last resort.</td></tr>
<tr><td>P.M.I.</td><td>Personal = people, Material = matter, Incorporeal = ideas.</td></tr>
<tr><td>Gharar examples</td><td>Runaway slave, fish in the sea, an unborn camel's fetus.</td></tr>
</tbody></table></div>
''',
    },
]

CHEAT_1_FLASH = [
    ("Transactions", "The lawful rules regulating financial dealings between people."),
    ("Finance", "Anything with material value among people whose use is permitted."),
    ("Contemporary", "The recent, modern age."),
    ("B.D.D.D.", "Bargains, Donations, Dropping, Documentation."),
    ("Bargains", "Sale and leasing."),
    ("Donations", "Grants, will, and endowment (waqf)."),
    ("Dropping", "Ending an obligation, e.g. abolishing a debt."),
    ("Documentation", "Mortgage, bail (warranty), draft (transfer of debt)."),
    ("N.U.R.C.", "New, Updated procedure, Renamed, Combined — the four cases."),
    ("Case 1 example", "Corporate companies; banknotes."),
    ("Case 2 example", "Property Registry Office replacing handing over the key."),
    ("Case 3 example", "Bank interest — still riba under a new name."),
    ("Case 4 example", "Murabaha; leasing contracts merging sale and rent."),
    ("Al-Ib&#257;&#7717;ah", "The default ruling for transactions is permissibility."),
    ("Gharar", "An uncertain sale with no guarantee the seller can deliver."),
    ("Riba", "Usury/interest — forbidden even when renamed."),
    ("Ijtihad", "A qualified jurist's total effort to deduce a ruling from detailed evidence."),
    ("Q.H.I.A.", "Qur'an, Hadith, Ijma', Arabic — the mujtahid's knowledge base."),
    ("S.H.M.R.U.", "Skill, Honesty, Maqasid, Research, Understanding reality."),
    ("Step 8", "Refrain from ruling — no fatwa — if no legitimate rule can be reached."),
    ("Rights", "An exclusive entitlement by which the Law establishes an authority or an obligation."),
    ("Political rights", "Organise governance — election and nomination."),
    ("General rights", "Inherent personality rights — bodily safety, home inviolability."),
    ("P.M.I.", "Personal (people), Material (matter), Incorporeal (ideas)."),
]

# --------------------------------------------------------------------------- #
# Cheat sheet 2 — Lectures 3 & 4
# --------------------------------------------------------------------------- #

CHEAT_2_META = {
    'slug': 'cheat-sheet-2',
    'title': 'Cheat Sheet 2 — Lectures 3 &amp; 4',
    'brand_sub': 'Incorporeal Rights &amp; Insurance — Lectures 3–4',
    'h1': 'Cheat Sheet 2: Incorporeal Rights &amp; Insurance',
    'lede': ('Lectures 3 and 4 condensed for Major 2 — the three incorporeal rights with the exact count '
             'of Shariah reasons behind each, and the two insurance systems kept on separate tracks so '
             'their reasoning never blurs together.'),
    'meta': [('2', 'lectures covered'), ('10', 'quick-reference blocks'), ('26', 'flashcards')],
}

CHEAT_2_SECTIONS = [
    {
        'id': 's1', 'tag': 'Lecture 3 · Block 1–2', 'num': '01',
        'h2': 'Incorporeal rights and the fiqh idea of m&#257;l',
        'body': '''
<p>An <strong>incorporeal right</strong> is the authority of a person over something non-physical. In fiqh, ownership is not restricted to a tangible object: property (<em>m&#257;l</em>) is anything that possesses <strong>recognised value</strong> among people and <strong>may be lawfully utilised</strong>.</p>
<div class="callout mnemonic"><div class="callout-label">Mnemonic</div>
"Value + permitted use = property." Nowhere does that formula say <em>physical</em> — which is exactly why copyright can be owned property in fiqh.</div>
<p>Because incorporeal rights meet that standard they count as m&#257;l: their owners may sell, buy, or lease them, and they are financial rights safeguarded by Shariah.</p>
<div class="card-grid">
  <div class="mini-card"><span class="mini-key">C — 1886</span><div class="mini-title">Copyright</div>Protects a creative <strong>work</strong>.</div>
  <div class="mini-card"><span class="mini-key">P — 1791</span><div class="mini-title">Patent</div>Protects an <strong>invention</strong>.</div>
  <div class="mini-card"><span class="mini-key">T — 1909</span><div class="mini-title">Trade name</div>Protects a business <strong>identity</strong>.</div>
</div>
<div class="callout mistake"><div class="callout-label">Common mistake</div>
The years are not in chronological order as listed. Patent (1791) is oldest, then Copyright (1886), then Trade name (1909). Know both the list order and the real timeline.</div>
''',
    },
    {
        'id': 's2', 'tag': 'Lecture 3 · Block 3–6', 'num': '02',
        'h2': 'Copyright',
        'body': '''
<p>Falls under intellectual property. It gives the author the right to use their work and to prevent others using or benefiting from it without consent; literary and material rights are fully reserved for the creator.</p>
<div class="callout mistake"><div class="callout-label">Common mistake — what does not qualify</div>
Merely abstracting or collecting existing information with no creative contribution is not innovation and is not protected the same way. Interpreting, adding detail, correcting mistakes, or summarising for students <em>does</em> count as creating.</div>

<h3>Who counts as the author</h3>
<ul>
  <li>The person who created the work.</li>
  <li>Whoever has their name published on it — <strong>unless proven otherwise</strong>.</li>
  <li>If no name is given, or a pseudonym is used, the <strong>publisher</strong> acts as the author's representative.</li>
  <li>Also includes anyone contributing to the creation of visual and audio work.</li>
</ul>

<h3>The two rights</h3>
<div class="table-scroll"><table class="rule-table">
<thead><tr><th></th><th>Literary right</th><th>Financial right</th></tr></thead>
<tbody>
<tr><td>Duration</td><td>Permanent</td><td>Temporary — a limited period</td></tr>
<tr><td>Transferable?</td><td>No — may not be permanently assigned to another</td><td>Yes — inheritors may publish after the author's death for financial benefit</td></tr>
</tbody></table></div>
<div class="callout mnemonic"><div class="callout-label">Mnemonic — "L stays, F pays (for a while)"</div>
Literary = permanent, non-transferable. Financial = temporary, inheritable.</div>

<h3>Why it is legally recognised — four reasons</h3>
<ol>
  <li><strong>B</strong>enefits are compensable in Islam; intellectual property benefits society, so it earns compensation like any other benefit.</li>
  <li>General <strong>c</strong>ustom ('urf) already admits the author's right and that it can be compensated.</li>
  <li><strong>P</strong>lagiarism is prohibited — misattributing statements is strictly forbidden.</li>
  <li><strong>R</strong>ights correspond to responsibilities — "the benefit runs with the burden."</li>
</ol>
<div class="callout evidence"><div class="callout-label">Evidence</div>
"Whoever lies upon me deliberately, let him take his seat in the Fire." Accurate attribution lets an author take credit for good, or bear responsibility for harm.</div>
<div class="callout mnemonic"><div class="callout-label">Mnemonic — B.C.P.R.</div>
Benefit &rarr; Custom &rarr; Plagiarism &rarr; Responsibility.</div>
''',
    },
    {
        'id': 's3', 'tag': 'Lecture 3 · Block 7–10', 'num': '03',
        'h2': 'Patent (invention certificate)',
        'body': '''
<p>Intellectual property giving its owner the legal right to <strong>exclude others from making, using, or selling</strong> an invention for a limited period — in exchange for publishing an enabling disclosure of it. In most countries patent rights fall under private law: the holder can sue an infringer.</p>
<div class="callout mnemonic"><div class="callout-label">Mnemonic</div>
"Exclusivity in exchange for disclosure."</div>

<h3>The inventor's rights — only two</h3>
<ul>
  <li>The right to use the invention for a limited period.</li>
  <li>The invention should be registered under the inventor's name.</li>
</ul>

<h3>Four kinds of certificate</h3>
<div class="table-scroll"><table class="rule-table">
<thead><tr><th>Certificate</th><th>Conditions</th><th>Protection</th></tr></thead>
<tbody>
<tr><td><strong>F</strong>ull-Rights</td><td>Strict qualifying conditions</td><td>Complete, comprehensive legal protection</td></tr>
<tr><td><strong>L</strong>imited</td><td>More lenient criteria</td><td>Restricted compared to Full-Rights</td></tr>
<tr><td><strong>A</strong>dditive</td><td>For improvements or modifications to an already-certified invention</td><td>Covers the improvement</td></tr>
<tr><td><strong>I</strong>mportation</td><td>Introducing a foreign-developed invention for the first time</td><td>An exclusive <em>commercial enterprise</em> right — not protection for original inventorship</td></tr>
</tbody></table></div>
<div class="callout mistake"><div class="callout-label">Common mistake</div>
The Importation Certificate is the odd one out: it does not protect an invention at all.</div>

<h3>Shariah ruling — three reasons</h3>
<p>Recognised, because: benefits are compensable; plagiarism / false attribution is forbidden; rights correspond to responsibilities.</p>
<div class="callout mistake"><div class="callout-label">The sharpest trap in the lecture</div>
Patent has <strong>three</strong> reasons — it drops the "general custom ('urf)" reason that Copyright and Trade name both carry. If a question lists four reasons for patent legitimacy, 'urf is the intruder.</div>
''',
    },
    {
        'id': 's4', 'tag': 'Lecture 3 · Block 11–13', 'num': '04',
        'h2': 'Trade name',
        'body': '''
<p>The official name under which an individual or company conducts business. A trademark gives legal protection for a particular brand, which may be associated with a trade name.</p>
<div class="card-grid">
  <div class="mini-card"><span class="mini-key">M</span><div class="mini-title">The Trademark</div><strong>D</strong>istinctiveness (tells your goods from competitors'), <strong>C</strong>onsumer attraction (goodwill and loyalty), <strong>M</strong>arket surveillance (monitor competitors, catch imitation).</div>
  <div class="mini-card"><span class="mini-key">S</span><div class="mini-title">Commercial / shop sign</div>Designates the premises and gains reputational value over time; usually incorporates the trader's civil name, legal title, or another distinctive designation.</div>
  <div class="mini-card"><span class="mini-key">L</span><div class="mini-title">Location</div>The commercial store's place and position.</div>
</div>
<div class="callout mnemonic"><div class="callout-label">Mnemonic — M.S.L., then D.C.M.</div>
Trade name = Mark, Sign, Location. The trademark's own three functions = Distinctiveness, Consumer attraction, Market surveillance.</div>

<h3>Rights and ruling</h3>
<ul>
  <li><strong>Exclusive right</strong> — exclusive use, distinguishing the business and preventing imitation.</li>
  <li><strong>Transferable asset</strong> — measurable financial value; the owner may sell, gift, or transfer it.</li>
</ul>
<p>Legally recognised, on condition it is <strong>not based on cheating or gharar</strong>. The reasoning mirrors Copyright's — all four reasons apply.</p>
<div class="callout mistake"><div class="callout-label">Common mistake</div>
Trade name is the only one of the three with an explicit conditional caveat. Do not drop it when answering a trade-name ruling question.</div>

<div class="table-scroll"><table class="rule-table">
<caption>The three incorporeal rights, side by side</caption>
<thead><tr><th>Feature</th><th>Copyright</th><th>Patent</th><th>Trade name</th></tr></thead>
<tbody>
<tr><td>Year mentioned</td><td>1886</td><td>1791</td><td>1909</td></tr>
<tr><td>Protects</td><td>A creative work</td><td>An invention</td><td>A business identity</td></tr>
<tr><td>Owner's rights</td><td>Literary (permanent) + Financial (temporary)</td><td>Use it for a limited time + name on it</td><td>Exclusive use + transferable asset</td></tr>
<tr><td>Shariah reasons</td><td>4</td><td>3 (no 'urf)</td><td>4, plus the "no cheating / gharar" condition</td></tr>
</tbody></table></div>
<div class="callout mnemonic"><div class="callout-label">Mnemonic</div>
Only Patent drops to three reasons. Only Trade name adds a condition. Copyright is the default four-reason case.</div>
''',
    },
    {
        'id': 's5', 'tag': 'Lecture 4 · Block 1–3', 'num': '05',
        'h2': 'Insurance — definition and the two systems',
        'body': '''
<div class="term-row"><span class="term">Linguistically</span><span>From security against fear — stillness of heart, confidence, trust.</span></div>
<div class="term-row"><span class="term">Technically</span><span>"A contractual system based on the principles of compensation or donation, or a mixture of both. One party commits to provide monetary compensation to another party in the event of an incident or similar occurrence."</span></div>

<h3>The philosophy</h3>
<p>Insurance rests on <strong>collective risk-sharing</strong>: one person could be crushed by a disaster's full cost, but pooling relief expenses across a large group makes the burden manageable. That cooperative ideal was compromised when insurance shifted from mutual aid to a profit-driven commercial enterprise.</p>
<div class="callout mnemonic"><div class="callout-label">Mnemonic</div>
"Started as sharing the burden. Became selling the promise." That sentence is the hinge the whole lecture swings on.</div>

<div class="card-grid">
  <div class="mini-card"><span class="mini-key">Halal</span><div class="mini-title">Collaborative / social</div>Donation-based, mutual solidarity, no profit motive. <span class="verdict halal">Fully lawful</span></div>
  <div class="mini-card"><span class="mini-key">Haram</span><div class="mini-title">Commercial / profitable</div>Compensation-based contract sold by profit-making companies. <span class="verdict haram">Prohibited</span> with three narrow exceptions.</div>
</div>
<div class="callout mnemonic"><div class="callout-label">Mnemonic — C&sup2;</div>
Collaborative = Cooperation. Commercial = Cash-for-risk. Same first letter, opposite rulings.</div>
''',
    },
    {
        'id': 's6', 'tag': 'Lecture 4 · Block 4–7', 'num': '06',
        'h2': 'Collaborative insurance',
        'body': '''
<div class="callout evidence"><div class="callout-label">Evidence</div>
<span class="arabic">&#1608;&#1614;&#1578;&#1614;&#1593;&#1614;&#1575;&#1608;&#1614;&#1606;&#1615;&#1608;&#1575; &#1593;&#1614;&#1604;&#1614;&#1609; &#1575;&#1604;&#1618;&#1576;&#1616;&#1585;&#1617;&#1616; &#1608;&#1614;&#1575;&#1604;&#1578;&#1617;&#1614;&#1602;&#1618;&#1608;&#1614;&#1609;</span><br>
"And cooperate in righteousness and piety, but do not cooperate in sin and aggression." One verse, one word to hold onto: <em>cooperate</em>.</div>

<h3>Three historical forms in Islam</h3>
<div class="card-grid">
  <div class="mini-card"><span class="mini-key">Z</span><div class="mini-title">People of Zakat</div>Those hit by major unavoidable harm — in debt and unable to pay, or extremely poor — helped through the alms of the wealthy. (At-Tawbah 9:60 lists the eight categories.)</div>
  <div class="mini-card"><span class="mini-key">K</span><div class="mini-title">Kinship system (Aqilah)</div>Blood money (diyah) for accidental homicide is distributed among the killer's paternal male relatives, who pay the victim's family.</div>
  <div class="mini-card"><span class="mini-key">S</span><div class="mini-title">Social solidarity</div>The Ash'arites pooled all their food when supplies ran low and redistributed it equally. The Prophet &#65018; praised them.</div>
</div>

<h3>Three modern systems</h3>
<div class="table-scroll"><table class="rule-table">
<thead><tr><th>System</th><th>How it works</th><th>Funded by</th></tr></thead>
<tbody>
<tr><td><strong>R</strong>etirement</td><td>Monthly pension at a set age (e.g. 55) or tenure (e.g. 20 years). No gharar — it is a donation contract, and labour are both insured and insurer.</td><td>Deducting part of the employee's monthly salary</td></tr>
<tr><td><strong>S</strong>ocial Security</td><td>Government-run cover for laborers who live by handcraft or manual work — illness, disability, old age.</td><td>Salary deductions, collected Zakat, and direct government treasury support</td></tr>
<tr><td><strong>R</strong>eciprocal</td><td>Non-profit solidarity run by charitable / mutual associations; members support any member in distress. E.g. a staff or village emergency fund.</td><td>Regular member donations into a pooled fund</td></tr>
</tbody></table></div>

<h3>Legal ruling</h3>
<p>Scholars agree social / cooperative insurance is fully lawful in all its forms, because it fulfils the Islamic objective of mutual solidarity rather than commercial profit.</p>
<div class="callout mnemonic"><div class="callout-label">Mnemonic</div>
"Donation contract &rarr; no riba &rarr; fully lawful." The entire ruling in nine words.</div>

<h3>How a collaborative contract actually works</h3>
<p>Collaborative associations collect donated subscriptions, invest them, and use the pool plus investment profits to cover subscriber risks. Any <strong>surplus</strong> after settling claims belongs entirely to the participants — they can take it back or roll it into future payments.</p>
<div class="callout mistake"><div class="callout-label">Common mistake</div>
The managing company may administer the surplus and its investment interest, but may <strong>not keep any of it</strong>. Ownership stays with the participants.</div>
''',
    },
    {
        'id': 's7', 'tag': 'Lecture 4 · Block 8–10', 'num': '07',
        'h2': 'Commercial insurance — mechanics',
        'body': '''
<p>A contract between an insurance company and an insured person: the company is legally bound to pay the insurance amount covering risk or damage; in return the insured pays regular installments (premiums). The company profits from the gap between premiums collected and claims paid.</p>
<p><strong>Emergence:</strong> began as marine insurance in northern Italy in the <strong>15th century</strong>, then transferred to Islamic countries in the <strong>19th century AD</strong> under the name "Saukarah."</p>

<h3>Five elements of the contract</h3>
<ol>
  <li>The insurer</li>
  <li>The insured</li>
  <li>The specific risk</li>
  <li>The insurance installment — paid by the insured to the company</li>
  <li>The insurance amount — paid by the company</li>
</ol>
<div class="callout mnemonic"><div class="callout-label">Mnemonic</div>
"Two people, a risk, two payments."</div>

<h3>Five conditions of the risk</h3>
<ol>
  <li><strong>U</strong>ncertain — its happening must not be certain.</li>
  <li><strong>N</strong>ot intentional.</li>
  <li>Not <strong>p</strong>rohibited by law.</li>
  <li>A <strong>f</strong>uture event.</li>
  <li>A <strong>r</strong>egular / ordinary danger.</li>
</ol>
<div class="callout mnemonic"><div class="callout-label">Mnemonic — U.N.P.F.R.</div>
Uncertain, Not intentional, not Prohibited, Future, Regular.</div>

<h3>Three types</h3>
<div class="card-grid">
  <div class="mini-card"><span class="mini-key">P</span><div class="mini-title">Insuring people</div><strong>Life</strong> — a monetary benefit to the decedent's family (income, burial, funeral; lump sum or annuity). <strong>Casualty</strong> — accidents not tied to specific property: auto, workers' compensation, some liability.</div>
  <div class="mini-card"><span class="mini-key">P</span><div class="mini-title">Property insurance</div>Physical assets against damage or loss — fire, water damage to goods, theft of cash, livestock death, crop spoilage.</div>
  <div class="mini-card"><span class="mini-key">L</span><div class="mini-title">Liability insurance</div>Against the financial or legal consequences of harming a third party — e.g. a car owner insuring against damage their vehicle causes others.</div>
</div>
<div class="callout mnemonic"><div class="callout-label">Mnemonic — P.P.L.</div>
People, Property, Liability. Notice the direction shifts: People and Property protect <em>you</em>; Liability protects <em>others from you</em>.</div>
''',
    },
    {
        'id': 's8', 'tag': 'Lecture 4 · Block 11–12', 'num': '08',
        'h2': 'Why commercial insurance is prohibited — and the three exceptions',
        'body': '''
<div class="table-scroll"><table class="rule-table">
<caption>Three reasons, not one</caption>
<thead><tr><th>Reason</th><th>The argument</th></tr></thead>
<tbody>
<tr><td><strong>G</strong>harar</td><td>A deceptive contract with heavy uncertainty. Every compensation contract containing deception is corrupted — the Prophet &#65018; forbade the deceptive sale.</td></tr>
<tr><td><strong>G</strong>ambling</td><td>Mirrors wagering: one party gains at the other's unearned expense, on pure chance. An insured may pay one premium and collect a huge payout, or pay indefinitely and get nothing. The insurer assumes liability without having caused the damage.</td></tr>
<tr><td><strong>R</strong>iba</td><td>Both forms. Pays the beneficiary <em>more</em> than was paid in &rarr; rib&#257; al-fa&#7693;l. Pays back <em>exactly</em> what was paid &rarr; rib&#257; al-nas&#299;'ah. Pays <em>nothing</em> because no risk occurred &rarr; the company took the money illegitimately.</td></tr>
</tbody></table></div>
<div class="callout mistake"><div class="callout-label">Common mistake</div>
Naming only gharar. It is a three-part combination — and you must know which riba maps to which payout: more-than-paid = fa&#7693;l; equal-to-paid = nas&#299;'ah; nothing-paid = plain illegitimate taking.</div>

<h3>Three exceptions</h3>
<div class="card-grid">
  <div class="mini-card"><span class="mini-key">D</span><div class="mini-title">Dependent, not original</div>Offered as a bundled service rather than for cash — a plane ticket that includes insurance, a rental car that comes with it.</div>
  <div class="mini-card"><span class="mini-key">N</span><div class="mini-title">Necessity</div>Living where the health system relies on commercial health insurance, or where car insurance is legally mandatory and only commercial cover exists.</div>
  <div class="mini-card"><span class="mini-key">F</span><div class="mini-title">Free</div>Given to employees as a company concession or benefit.</div>
</div>
<div class="callout mnemonic"><div class="callout-label">Mnemonic — D.N.F.</div>
Dependent &rarr; Necessity &rarr; Free. Each exception removes one of the three prohibition reasons: bundling stops it being a standalone compensation-for-cash contract, necessity is a classic fiqh override, and "free" removes the premium-for-payout exchange entirely.</div>
''',
    },
    {
        'id': 's9', 'tag': 'Lecture 4 · Block 14', 'num': '09',
        'h2': 'Commercial vs. collaborative — full comparison',
        'body': '''
<div class="table-scroll"><table class="rule-table">
<thead><tr><th>Dimension</th><th>Commercial insurance</th><th>Collaborative insurance</th></tr></thead>
<tbody>
<tr><td>Ruling</td><td><span class="verdict haram">Prohibited</span></td><td><span class="verdict halal">Encouraged</span></td></tr>
<tr><td>Contract type</td><td>Compensative</td><td>Donation</td></tr>
<tr><td>Target</td><td>Profit</td><td>Collaboration and solidarity</td></tr>
<tr><td>Surplus</td><td>Not recalled to participants</td><td>Recalled — belongs to participants</td></tr>
<tr><td>Structure</td><td>Personal — an individual contract with a company</td><td>Common — a shared pool for the group</td></tr>
</tbody></table></div>
<div class="callout mnemonic"><div class="callout-label">Mnemonic</div>
Five contrasts, one pattern: everything about Commercial is <em>individual and profit-facing</em>; everything about Collaborative is <em>shared and solidarity-facing</em>.</div>
''',
    },
    {
        'id': 's10', 'tag': 'Exam radar', 'num': '10',
        'h2': 'Highest-yield items for Major 2',
        'body': '''
<div class="table-scroll"><table class="rule-table">
<caption>What to check last, in order of how often it is tested</caption>
<thead><tr><th>Item</th><th>Say it in one line</th></tr></thead>
<tbody>
<tr><td>Reason counts</td><td>Copyright 4, Patent 3 (no 'urf), Trade name 4 + condition.</td></tr>
<tr><td>F.L.A.I.</td><td>Full, Limited, Additive, Importation — and Importation protects no invention.</td></tr>
<tr><td>Riba mapping</td><td>More = fa&#7693;l, equal = nas&#299;'ah, nothing = illegitimate taking.</td></tr>
<tr><td>G.G.R.</td><td>Gharar + Gambling + Riba — all three, never just one.</td></tr>
<tr><td>D.N.F.</td><td>Dependent, Necessity, Free.</td></tr>
<tr><td>Surplus rule</td><td>Belongs to participants; the managing company administers but keeps none.</td></tr>
<tr><td>Dates</td><td>Marine insurance: 15th-century northern Italy. Reached Islamic countries: 19th century, as "Saukarah."</td></tr>
<tr><td>L stays, F pays</td><td>Literary right permanent and non-transferable; financial right temporary and inheritable.</td></tr>
</tbody></table></div>
''',
    },
]

CHEAT_2_FLASH = [
    ("M&#257;l (property)", "Anything with recognised value among people that may be lawfully utilised."),
    ("Incorporeal right", "The authority of a person over something non-physical."),
    ("C.P.T.", "Copyright protects a creation, Patent an invention, Trade name an identity."),
    ("Copyright year", "1886."),
    ("Patent year", "1791 — actually the oldest of the three."),
    ("Trade name year", "1909."),
    ("Literary right", "Permanent; may not be permanently assigned to another person."),
    ("Financial right", "Temporary; inheritors may publish after the author's death for a limited period."),
    ("No name on the work", "The publisher acts as the author's representative."),
    ("Not innovation", "Merely abstracting or collecting existing information with no creative contribution."),
    ("B.C.P.R.", "Benefit compensable, Custom ('urf), Plagiarism banned, Responsibility earns reward."),
    ("Patent's ruling", "Recognised for 3 reasons — it drops the 'urf reason."),
    ("F.L.A.I.", "Full-Rights, Limited, Additive, Importation certificates."),
    ("Importation certificate", "An exclusive commercial enterprise right — protects no invention."),
    ("M.S.L.", "Trade name = Mark, Sign, Location."),
    ("D.C.M.", "Trademark functions: Distinctiveness, Consumer attraction, Market surveillance."),
    ("Trade name condition", "Recognised provided it is not based on cheating or gharar."),
    ("Insurance, linguistically", "Security against fear — stillness of heart, confidence, trust."),
    ("Z.K.S.", "Zakat, Kinship (Aqilah), Social solidarity — three historical forms."),
    ("Aqilah", "Blood money for accidental homicide, paid by the killer's paternal male relatives."),
    ("R.S.R.", "Retirement, Social Security, Reciprocal — three modern collaborative systems."),
    ("U.N.P.F.R.", "Uncertain, Not intentional, not Prohibited, Future, Regular — the risk conditions."),
    ("P.P.L.", "People, Property, Liability — the three commercial types."),
    ("G.G.R.", "Gharar, Gambling, Riba — why commercial insurance is prohibited."),
    ("D.N.F.", "Dependent, Necessity, Free — the three exceptions."),
    ("Surplus", "Belongs entirely to participants; the company administers but keeps none."),
]

# --------------------------------------------------------------------------- #
# Mindmap
# --------------------------------------------------------------------------- #

MINDMAP_META = {
    'slug': 'mindmap',
    'title': 'Mindmap',
    'brand_sub': 'Course Mindmap — Lectures 1–4',
    'h1': 'ISC213 Mindmap',
    'lede': ('The whole delivered course as one collapsible tree. Open a branch to walk from a heading '
             'down to its examples; collapse everything and try to rebuild a branch out loud before you '
             'reopen it.'),
    'meta': [('4', 'lecture branches'), ('27', 'slides mapped'), ('9', 'mnemonics')],
}

# (label, note, children)
MINDMAP = [
    ('Lecture 1 — The Concept of Contemporary Financial Transactions', 'Definition, four cases, four characteristics.', [
        ('Term analysis (T.F.C.)', 'Three roots stacked into one phrase.', [
            ('Transactions', 'The lawful rules regulating financial dealings between people.', []),
            ('Finance', 'Anything with material value among people, permitted to use.', []),
            ('Contemporary', 'The recent, modern age.', []),
        ]),
        ('Transactions: four categories (B.D.D.D.)', '', [
            ('Bargains', 'Sale and leasing.', []),
            ('Donations', 'Grants, will, endowment (waqf).', []),
            ('Dropping', 'Ending an obligation, e.g. abolishing a debt.', []),
            ('Documentation', 'Mortgage, bail, draft.', []),
        ]),
        ('Full definition', 'NEW · CHANGED · RENAMED · COMBINED.', []),
        ('Identifying the definition (N.U.R.C.)', 'Four cases, each with its example.', [
            ('New — unknown in earlier ages', 'Corporate companies, banknotes.', []),
            ('Updated procedure', 'Property Registry Office replaced handing over the key.', []),
            ('Renamed, ruling unchanged', 'Bank interest is still riba.', []),
            ('Combined old forms', 'Murabaha; leasing merging sale and rent.', []),
        ]),
        ('Relevant terms (E.O.I.F.)', 'Emerged cases, Occurrences, Incidences, Fatwa.', []),
        ('Four characteristics', '"Please Permit Reasonable Flexibility."', [
            ('General bases and principles', 'Not detailed like acts of worship; leaves room for ijtihad. Evidence: mutual consent (4:29), no riba (2:275), no gharar (hadith).', []),
            ('Permissibility is the default', 'Worship is restricted by default; transactions are permitted unless a clear text forbids.', []),
            ('Based on reasons and benefits', "Ta'līl / maṣlaḥah — which is what lets analogy reach new cases.", []),
            ('Flexible yet constant', 'Fixed in principle, adaptable in form.', []),
        ]),
    ]),
    ('Lecture 2 — Methodology of Ijtihad &amp; Incorporeal Rights', 'Who may rule, how they rule, and how rights are classified.', [
        ('Nine qualifications of a researcher', 'Knowledge base then character.', [
            ('Q.H.I.A.', "Qur'an, Hadith, Ijma', Arabic language.", []),
            ('S.H.M.R.U.', 'Skill of ijtihad, Honesty, Maqasid awareness, Research ability, Understanding lived reality.', []),
        ]),
        ('Eight steps to a ruling', 'Sequence is examinable.', [
            ('1–3', 'Pray, understand the subject, search Qur\'an and Sunnah.', []),
            ('4–6', "Companions' sayings, the four imams, recent scholars' articles.", []),
            ('7', 'His own opinion — second-to-last resort only.', []),
            ('8', 'Refrain from ruling if no legitimate rule can be reached.', []),
        ]),
        ('Rights', 'An exclusive entitlement establishing an authority or an obligation.', [
            ('Political rights', 'Organising governance — election, nomination.', []),
            ('Civil rights', "Establish the individual's interests directly.", [
                ('General rights', 'Inherent personality rights — bodily safety, home inviolability.', []),
                ('Private rights', 'Arise from bonds between individuals.', [
                    ('Family rights', 'Custody, divorce — cannot be priced.', []),
                    ('Financial rights', 'Can be evaluated with money.', [
                        ('Personal (People)', 'A bond between two persons — creditor and debtor.', []),
                        ('Material (Matter)', 'Authority over a physical thing — property.', []),
                        ('Incorporeal (Ideas)', 'Authority over something intangible — innovation.', []),
                    ]),
                ]),
            ]),
        ]),
    ]),
    ('Lecture 3 — Incorporeal Rights: Copyright, Patent, Trade Name', 'Value + permitted use = property, physical or not.', [
        ('Copyright — 1886', 'Protects a creative work.', [
            ('Who is the author', 'The creator; name on the work unless proven otherwise; else the publisher represents them.', []),
            ('Two rights', 'Literary — permanent, non-transferable. Financial — temporary, inheritable.', []),
            ('Four Shariah reasons (B.C.P.R.)', "Benefit compensable, Custom ('urf), Plagiarism banned, Responsibility earns reward.", []),
            ('Not protected', 'Abstracting or collecting existing information with no creative contribution.', []),
        ]),
        ('Patent — 1791', 'Exclusivity in exchange for disclosure.', [
            ("Inventor's rights", 'Use it for a limited period; register it under his name.', []),
            ('Four certificates (F.L.A.I.)', 'Full-Rights, Limited, Additive, Importation.', []),
            ('Importation certificate', 'An enterprise right — protects no invention.', []),
            ('Three Shariah reasons', "Drops the 'urf reason that Copyright and Trade name keep.", []),
        ]),
        ('Trade name — 1909', 'Protects a business identity.', [
            ('Three components (M.S.L.)', 'Mark, Sign, Location.', []),
            ('Trademark functions (D.C.M.)', 'Distinctiveness, Consumer attraction, Market surveillance.', []),
            ('Two rights', 'Exclusive use; transferable asset with measurable value.', []),
            ('Ruling', 'Four reasons, plus the condition: not based on cheating or gharar.', []),
        ]),
    ]),
    ('Lecture 4 — Insurance', 'Two systems, two verdicts. Keep the tracks separate.', [
        ('Definition', 'Linguistically: security against fear. Technically: a contract paying compensation on an incident.', []),
        ('Philosophy', 'Started as sharing the burden; became selling the promise.', []),
        ('Collaborative insurance', 'Donation-based, solidarity, no profit. Fully lawful.', [
            ('Evidence', '"And cooperate in righteousness and piety."', []),
            ('Three historical forms (Z.K.S.)', "Zakat, Kinship (Aqilah), Social solidarity (the Ash'arites).", []),
            ('Three modern systems (R.S.R.)', 'Retirement, Social Security, Reciprocal.', []),
            ('Ruling', 'Donation contract → no riba → fully lawful.', []),
            ('Surplus', 'Belongs to participants; the company administers but keeps none.', []),
        ]),
        ('Commercial insurance', 'Compensation-based, profit-making. Prohibited, with narrow exceptions.', [
            ('Emergence', 'Marine insurance, 15th-century northern Italy; reached Islamic countries in the 19th century as "Saukarah."', []),
            ('Five elements', 'Insurer, insured, the risk, the installment, the amount.', []),
            ('Five risk conditions (U.N.P.F.R.)', 'Uncertain, Not intentional, not Prohibited, Future, Regular.', []),
            ('Three types (P.P.L.)', 'People (life + casualty), Property, Liability.', []),
            ('Why prohibited (G.G.R.)', 'Gharar, Gambling, Riba — both fadl and nasī\'ah.', []),
            ('Three exceptions (D.N.F.)', 'Dependent (bundled), Necessity, Free.', []),
        ]),
        ('Full comparison', 'Commercial is individual and profit-facing; collaborative is shared and solidarity-facing.', []),
    ]),
]

# --------------------------------------------------------------------------- #
# Exams
# --------------------------------------------------------------------------- #

EXAM_1_META = {
    'slug': 'exam-1',
    'title': 'Exam 1',
    'brand_sub': 'Practice Major 1 — Lectures 1–2',
    'h1': 'Practice Exam 1',
    'lede': ('A practice Major 1 over Lectures 1 and 2: twenty multiple-choice questions marked as you '
             'answer, then six written questions with model answers you can reveal one at a time. Every '
             'item is traceable to a specific lecture block.'),
    'meta': [('20', 'multiple choice'), ('6', 'written questions'), ('L1–L2', 'coverage')],
    'scope': 'Lectures 1–2',
}

EXAM_1_MCQ = [
    ("Which of the four categories of transactions does an endowment (waqf) belong to?",
     "L1 · Block 2",
     ["Bargains", "Donations", "Dropping", "Documentation"], 1,
     "Waqf is a gift with no return, so it sits with grants and wills under Donations."),
    ("Forgiving a debt owed to you falls under which category?",
     "L1 · Block 2",
     ["Documentation", "Bargains", "Dropping", "Donations"], 2,
     "Dropping ends a right. Documentation, by contrast, protects one."),
    ("A mortgage is an example of:",
     "L1 · Block 2",
     ["Dropping", "Documentation", "Donations", "Bargains"], 1,
     "Documentation covers mortgage, bail (warranty), and draft — instruments that secure an obligation."),
    ("Property ownership no longer requires physically handing over the key because Property Registry "
     "Offices exist. Which of the four cases is this?",
     "L1 · Block 5",
     ["Cases unknown in earlier ages",
      "Rules updated due to progress or changed circumstances",
      "New names, same old ruling",
      "Transactions formulated from several old forms"], 1,
     "The procedure changed; the underlying transaction did not. That is case 2."),
    ("Calling usury \"bank interest\" is an example of:",
     "L1 · Block 5",
     ["A new case unknown in earlier ages",
      "An updated procedure",
      "A new name for a transaction already ruled on",
      "Several old forms combined"], 2,
     "Only the label changed; the ruling is unaffected. Hence the hadith about drinking khamr under another name."),
    ("Murabaha is cited as an example of which case?",
     "L1 · Block 5",
     ["Transactions formulated from several old forms combined",
      "Cases unknown in earlier ages",
      "New names, same old ruling",
      "Rules updated due to progress"], 0,
     "Murabaha merges more than one classical contract type into a single modern contract."),
    ("Banknotes and corporate companies are given as examples of:",
     "L1 · Block 5",
     ["Renamed transactions", "Cases unknown in earlier ages",
      "Combined old forms", "Updated procedures"], 1,
     "Neither existed for earlier jurisprudents to rule on."),
    ("Which statement correctly contrasts acts of worship with transactions?",
     "L1 · Block 9",
     ["Both are restricted by default",
      "Worship is permitted by default; transactions are restricted by default",
      "Worship is restricted by default; transactions are permitted by default",
      "Both are permitted by default"], 2,
     "Nothing is added to worship without a permitting text; nothing is forbidden in transactions without a clear prohibiting text."),
    ("The hadith \"If anyone introduces in our matter something which does not belong to it, it will be "
     "rejected\" supports which principle?",
     "L1 · Block 9",
     ["Permissibility in transactions", "The restriction principle for acts of worship",
      "The prohibition of gharar", "The requirement of mutual consent"], 1,
     "It is the restriction principle, aimed at bid'ah in worship — not at transactions."),
    ("Selling fish still in the sea is a textbook example of:",
     "L1 · Block 8",
     ["Riba al-fadl", "Gharar", "Maslahah", "Ijma'"], 1,
     "Gharar: there is no guarantee the seller can deliver the goods paid for."),
    ("Surah Al-Baqarah 2:275 is cited for which point?",
     "L1 · Block 8",
     ["Trade is permitted and riba forbidden",
      "Wealth must not be consumed unjustly",
      "The sea and earth are subjected to people",
      "Cooperation in righteousness"], 0,
     "2:275 is the trade-permitted / riba-forbidden verse. 4:29 is the mutual-consent verse."),
    ("Which set names the near-synonyms for newly emerged issues needing a ruling?",
     "L1 · Block 6",
     ["Bargains, Donations, Dropping, Documentation",
      "Emerged cases, Occurrences, Incidences, Fatwa",
      "Qur'an, Hadith, Ijma', Qiyas",
      "Personal, Material, Incorporeal"], 1,
     "E.O.I.F. — all four point at the same idea."),
    ("Which of the following is NOT one of the nine qualifications of a researcher?",
     "L2 · Block 1",
     ["Deep mastery of the Arabic language",
      "Honesty in word and action",
      "Holding a formal judicial appointment",
      "Awareness of the higher objectives of religion"], 2,
     "A judicial appointment is never listed. The nine are Q.H.I.A. plus S.H.M.R.U."),
    ("In the eight steps to a ruling, what immediately follows searching the Qur'an and Sunnah?",
     "L2 · Block 2",
     ["Searching the four imams' jurisprudence",
      "Examining the Companions' sayings and arguments",
      "Using his own opinion",
      "Refraining from ruling"], 1,
     "Order: pray, understand, texts, Companions, four imams, new sources, own opinion, refrain."),
    ("A scholar has exhausted every source and still cannot reach a legitimate rule. What should he do?",
     "L2 · Block 2",
     ["Follow the closest school of thought",
      "Issue the most cautious fatwa available",
      "Refrain from ruling — issue no fatwa",
      "Defer to general custom"], 2,
     "Step 8 is explicit: refrain rather than guess."),
    ("Which pair are the two shapes a right can take, per the lecture's definition?",
     "L2 · Block 3",
     ["Authority or obligation", "General or private",
      "Political or civil", "Family or financial"], 0,
     "\"An exclusive entitlement by which the Law establishes an authority or an obligation.\""),
    ("The right of election and nomination is classified as:",
     "L2 · Block 4",
     ["A civil right", "A general right", "A political right", "A private right"], 2,
     "Political rights organise governance and its authorities."),
    ("The inviolability of one's residence is an example of:",
     "L2 · Block 5",
     ["A private right", "A general right", "A family right", "A financial right"], 1,
     "General rights — inherent personality rights — need no second party."),
    ("You are owed money by a debtor. Which financial right is that?",
     "L2 · Block 7",
     ["Material", "Incorporeal", "Personal", "General"], 2,
     "The right points at a person's obligation, so it is Personal — also called a commitment."),
    ("Which test sorts a private right into Family versus Financial?",
     "L2 · Block 6",
     ["Whether a second party is involved",
      "Whether it could be evaluated with money",
      "Whether it is established by the state",
      "Whether it is permanent or temporary"], 1,
     "Family rights cannot be priced; financial rights can."),
]

EXAM_1_WRITTEN = [
    ("Define \"Contemporary Financial Transactions\" and name the four cases the definition covers.",
     "L1 · Blocks 4–5",
     '''<p>They are financial cases which emerged in the contemporary age — cases that changed in their
     rules because of progress or changed circumstances, and cases that bear new names, or consist of many
     old forms.</p>
     <p>The four cases are: <strong>(1)</strong> cases unknown in earlier ages (corporate companies,
     banknotes); <strong>(2)</strong> rules updated due to progress or changed circumstances (the Property
     Registry Office replacing the handing over of the key); <strong>(3)</strong> new names for the same
     old ruling (bank interest is still riba); <strong>(4)</strong> transactions formulated from several
     old forms combined (murabaha, leasing contracts merging sale and rent).</p>'''),
    ("List the four categories of transactions with one example each.",
     "L1 · Block 2",
     '''<p><strong>Bargains</strong> — sale and leasing. <strong>Donations</strong> — grants, will, and
     endowment (waqf). <strong>Dropping</strong> — abolishing or ending a debt. <strong>Documentation</strong>
     — mortgage, bail (warranty), and draft (transfer of debt).</p>
     <p>Dropping ends a right; documentation protects one.</p>'''),
    ("State the four characteristics of transactions in Islamic jurisprudence, and give the evidence for "
     "the first one.",
     "L1 · Blocks 7–11",
     '''<p><strong>(1)</strong> Based on general bases and principles rather than exhaustive detail;
     <strong>(2)</strong> the original rule is permissibility (al-ibāḥah); <strong>(3)</strong> based on
     reasons and benefits; <strong>(4)</strong> both flexible and constant.</p>
     <p>Evidence for the first: An-Nisaa 4:29 (wealth is consumed only in lawful business by mutual
     consent); Al-Baqarah 2:275 ("Allah has permitted trade and has forbidden interest"); and the hadith
     narrated by Ibn Omar that the Prophet ﷺ prohibited the gharar sale — a transaction with no guarantee
     the seller can deliver, such as a runaway slave, fish still in the sea, or an unborn camel's
     fetus.</p>'''),
    ("Explain the difference between the default ruling for acts of worship and for transactions, and why "
     "the difference exists.",
     "L1 · Block 9",
     '''<p>Acts of worship are <strong>restricted</strong> by default: nothing is added unless a text
     permits it, which prevents people inventing new religious practice. Transactions and contracts are
     <strong>permitted</strong> by default: nothing is forbidden unless a truthful, clear text prohibits
     it, so an absence of prohibiting evidence means the transaction is permissible.</p>
     <p>This is what allows jurisprudents to accommodate newly emerged financial forms without needing a
     specific text for each one.</p>'''),
    ("List the nine qualifications a researcher must meet before attempting ijtihad on an emerging "
     "financial issue.",
     "L2 · Block 1",
     '''<p>Comprehensive understanding of the Qur'an; comprehensive understanding of the Prophetic Hadith;
     knowledge of legal consensus (ijma'); deep mastery of the Arabic language; the skill of ijtihad
     itself; honesty in word and action; awareness of the higher objectives of religion (maqasid
     al-Shari'ah); the ability to elicit rulings from contemporary scholars' books; and an understanding
     of lived reality and its surrounding circumstances.</p>
     <p>Group them as Q.H.I.A. (the knowledge base) plus S.H.M.R.U. (the practical qualities).</p>'''),
    ("Draw the full classification of rights from the top down, ending in the three financial rights.",
     "L2 · Blocks 3–8",
     '''<p><strong>Rights</strong> — an exclusive entitlement by which the Law establishes an authority or
     an obligation — divide into <strong>Political</strong> (organising governance; election and
     nomination) and <strong>Civil</strong> (establishing the individual's interests directly).</p>
     <p>Civil rights divide into <strong>General</strong> (inherent personality rights: bodily safety, the
     inviolability of one's residence) and <strong>Private</strong> (arising from bonds between
     individuals).</p>
     <p>Private rights divide into <strong>Family</strong> (custody, divorce) and <strong>Financial</strong>
     (rights that could be evaluated with money).</p>
     <p>Financial rights are <strong>Personal</strong> (a relation between two people, like creditor and
     debtor), <strong>Material</strong> (direct authority over a physical thing — property), and
     <strong>Incorporeal</strong> (authority over something intangible — the rights of innovation).</p>'''),
]

EXAM_2_META = {
    'slug': 'exam-2',
    'title': 'Exam 2',
    'brand_sub': 'Practice Major 2 — Lectures 3–4',
    'h1': 'Practice Exam 2',
    'lede': ('A practice Major 2 over Lectures 3 and 4: twenty multiple-choice questions marked as you '
             'answer, then six written questions with model answers. Weighted toward the two traps this '
             'material is built around — reason counts and the two insurance tracks.'),
    'meta': [('20', 'multiple choice'), ('6', 'written questions'), ('L3–L4', 'coverage')],
    'scope': 'Lectures 3–4',
}

EXAM_2_MCQ = [
    ("How does fiqh define property (māl)?",
     "L3 · Block 1",
     ["Any tangible object that can be physically possessed",
      "Anything with recognised value among people that may be lawfully utilised",
      "Anything that can be bought and sold in a market",
      "Any asset registered under an owner's name"], 1,
     "Value plus permissible utility — nothing in the formula requires the thing to be physical."),
    ("Which of the three incorporeal rights is actually the oldest by the years given?",
     "L3 · Block 2",
     ["Copyright (1886)", "Patent (1791)", "Trade name (1909)", "They share the same year"], 1,
     "The lecture lists them 1886, 1791, 1909 — so the list order is not the timeline."),
    ("A book that only collects and abstracts existing information with no creative contribution is:",
     "L3 · Block 3",
     ["Protected exactly like any other work",
      "Protected only for the financial right",
      "Not considered innovation, so not protected the same way",
      "Protected only if the author's name appears on it"], 2,
     "Interpreting, adding detail, correcting mistakes, or summarising for students would count as creating; mere collection does not."),
    ("A work is published under a pseudonym. Who acts as the author's representative?",
     "L3 · Block 4",
     ["The publisher", "The copyright office", "The first purchaser", "No one — the work is unprotected"], 0,
     "Name on the work means presumed author; no name means the publisher stands in."),
    ("Which describes the author's literary right?",
     "L3 · Block 5",
     ["Temporary and inheritable", "Permanent and non-transferable",
      "Temporary and transferable", "Permanent but transferable by sale"], 1,
     "\"L stays, F pays.\" The financial right is the temporary, inheritable one."),
    ("How many Shariah reasons are given for recognising the patent right?",
     "L3 · Block 10",
     ["Two", "Three", "Four", "Five"], 1,
     "Patent drops the \"general custom ('urf)\" reason that copyright and trade name both carry."),
    ("Which reason is NOT given for the legitimacy of the patent right?",
     "L3 · Block 10",
     ["Benefits are compensable in Islam",
      "General custom ('urf) admits the right",
      "Plagiarism and false attribution are forbidden",
      "Rights correspond to responsibilities"], 1,
     "'Urf is the intruder — this is the sharpest trap in Lecture 3."),
    ("Which patent certificate does NOT protect an invention?",
     "L3 · Block 9",
     ["Full-Rights Certificate", "Limited Certificate",
      "Additive Certificate", "Importation Certificate"], 3,
     "The importation certificate is an exclusive commercial enterprise right for whoever first brings a foreign invention in."),
    ("A certificate issued for an improvement to an already-certified invention is:",
     "L3 · Block 9",
     ["Additive", "Limited", "Full-Rights", "Importation"], 0,
     "F.L.A.I.: Full, Limited, Additive, Importation."),
    ("What does a patent holder give in exchange for the right to exclude others?",
     "L3 · Block 7",
     ["A registration fee", "An enabling disclosure of how the invention works",
      "A share of the profits", "A limited licence to the state"], 1,
     "\"Exclusivity in exchange for disclosure.\""),
    ("The three components of a trade name are:",
     "L3 · Block 11",
     ["Mark, Sign, Location", "Name, Logo, Slogan",
      "Distinctiveness, Attraction, Surveillance", "Brand, Goodwill, Premises"], 0,
     "M.S.L. Distinctiveness / attraction / surveillance are the trademark's three functions, one level down."),
    ("Which condition is attached specifically to the trade name's Shariah ruling?",
     "L3 · Block 12",
     ["That it be registered with the state",
      "That it not be based on cheating or gharar",
      "That it be renewed periodically",
      "That it not be sold or transferred"], 1,
     "Trade name is the only one of the three carrying an explicit stated caveat."),
    ("Which verse is the textual root for collaborative insurance?",
     "L4 · Block 4",
     ["\"Allah has permitted trade and has forbidden interest\"",
      "\"And cooperate in righteousness and piety\"",
      "\"Do not consume one another's wealth unjustly\"",
      "\"Zakat expenditures are only for the poor and the needy\""], 1,
     "One verse, one word: cooperate."),
    ("In the Aqilah system, who pays the blood money for accidental homicide?",
     "L4 · Block 5",
     ["The state treasury", "The killer alone",
      "The killer's paternal male relatives", "The victim's tribe"], 2,
     "The diyah is distributed among the paternal male relatives, who then pay the victim's family."),
    ("Which is NOT one of the three modern collaborative insurance systems?",
     "L4 · Block 6",
     ["Retirement System", "Social Security System",
      "Reciprocal Insurance", "Marine Insurance"], 3,
     "R.S.R. Marine insurance is where commercial insurance began, in 15th-century northern Italy."),
    ("Commercial insurance reached Islamic countries in which century, and under what name?",
     "L4 · Block 8",
     ["15th century, as \"Aqilah\"", "17th century, as \"Takaful\"",
      "19th century, as \"Saukarah\"", "20th century, as \"Ta'min\""], 2,
     "It began as marine insurance in 15th-century northern Italy and transferred in the 19th century AD."),
    ("Which is NOT one of the five conditions of the risk?",
     "L4 · Block 9",
     ["The risk must be uncertain", "The risk must not be intentional",
      "The risk must be insurable at a fixed premium", "The risk must be a future event"], 2,
     "U.N.P.F.R.: Uncertain, Not intentional, not Prohibited by law, Future, Regular/ordinary."),
    ("A company insures its car against liability for damage the vehicle causes others. This is:",
     "L4 · Block 10",
     ["Property insurance", "Casualty insurance under insuring people",
      "Liability insurance", "Life insurance"], 2,
     "P.P.L. — People and Property protect you; Liability protects others from you."),
    ("If a commercial insurer pays the beneficiary back exactly what was paid in, which riba is involved?",
     "L4 · Block 11",
     ["Ribā al-fadl", "Ribā al-nasī'ah",
      "Neither — the exchange is equal", "Both simultaneously"], 1,
     "More than paid = fadl; exactly what was paid = nasī'ah; nothing paid = the company took the money illegitimately."),
    ("An employer gives staff health insurance free as a company benefit. Under which exception is this "
     "permitted?",
     "L4 · Block 12",
     ["Dependent, not original", "Necessity", "Free", "No exception applies"], 2,
     "D.N.F. \"Free\" removes the premium-for-payout exchange entirely."),
]

EXAM_2_WRITTEN = [
    ("Explain why incorporeal rights count as property (māl) in fiqh, and what that entitles their owners "
     "to do.",
     "L3 · Block 1",
     '''<p>In fiqh, property is defined as anything that possesses recognised value among people and may be
     lawfully utilised. That standard says nothing about being physical, so an intangible thing satisfying
     value plus permissible utility qualifies as māl.</p>
     <p>Because incorporeal rights meet the standard, their owners may sell, buy, or lease them, and the
     rights are financial rights safeguarded by Shariah.</p>'''),
    ("Compare copyright, patent, and trade name across what they protect, the owner's rights, and the "
     "number of Shariah reasons behind each.",
     "L3 · Block 13",
     '''<p><strong>Copyright (1886)</strong> protects a creative work; the owner holds a literary right
     (permanent, non-transferable) and a financial right (temporary, inheritable); four Shariah reasons.</p>
     <p><strong>Patent (1791)</strong> protects an invention; the inventor may use it for a limited period
     and register it under his name; three Shariah reasons — it drops the 'urf reason.</p>
     <p><strong>Trade name (1909)</strong> protects a business identity; the owner holds exclusive use and
     a transferable asset; four Shariah reasons, plus the condition that it not be based on cheating or
     gharar.</p>
     <p>Only patent drops to three reasons; only trade name adds a condition.</p>'''),
    ("Name the four kinds of invention certificate and explain which one is the odd one out.",
     "L3 · Block 9",
     '''<p><strong>Full-Rights</strong> — strict qualifying conditions, complete legal protection.
     <strong>Limited</strong> — more lenient criteria, restricted protection. <strong>Additive</strong> —
     issued for improvements or modifications to an already-certified invention. <strong>Importation</strong>
     — for introducing a foreign-developed invention for the first time.</p>
     <p>The importation certificate is the odd one out: it does not protect an invention at all. It is an
     exclusive commercial enterprise right for whoever first brings the foreign invention in, not
     protection for original inventorship.</p>'''),
    ("State the three historical forms of collaborative insurance in Islam and the three modern systems.",
     "L4 · Blocks 5–6",
     '''<p><strong>Historical (Z.K.S.):</strong> the People of Zakat — those in unpayable debt or extreme
     poverty helped through the alms of the wealthy; the Kinship system (Aqilah) — blood money for
     accidental homicide distributed among the killer's paternal male relatives; and Social solidarity —
     the Ash'arites pooling and equally redistributing their food when supplies ran low.</p>
     <p><strong>Modern (R.S.R.):</strong> the Retirement System (a monthly state pension at a set age or
     tenure, funded by salary deductions); the Social Security System (state cover for manual laborers
     against illness, disability, and old age, funded by deductions plus Zakat and treasury support); and
     Reciprocal Insurance (a non-profit mutual fund of member donations supporting any member in
     distress).</p>'''),
    ("Give the three reasons commercial insurance is prohibited, and map each riba scenario to its payout.",
     "L4 · Block 11",
     '''<p><strong>Excessive uncertainty (gharar):</strong> a deceptive contract with heavy uncertainty,
     and every compensation contract containing deception is corrupted — the Prophet ﷺ forbade the
     deceptive sale.</p>
     <p><strong>Elements of gambling:</strong> one party gains at the other's unearned expense on pure
     chance; an insured may pay one premium and collect a huge payout, or pay indefinitely and receive
     nothing, while the insurer assumes liability without having caused the damage.</p>
     <p><strong>Both forms of riba:</strong> if the company pays more than what was paid in, ribā al-fadl;
     if it pays back exactly what was paid, ribā al-nasī'ah; if it pays nothing because no risk occurred,
     it took the money illegitimately.</p>
     <p>It is the combination of all three, not gharar alone.</p>'''),
    ("Compare commercial and collaborative insurance across the five dimensions given in the lecture.",
     "L4 · Block 14",
     '''<p><strong>Ruling:</strong> commercial is prohibited; collaborative is encouraged.
     <strong>Contract type:</strong> compensative versus donation. <strong>Target:</strong> profit versus
     collaboration and solidarity. <strong>Surplus:</strong> not recalled to participants versus recalled —
     it belongs to them. <strong>Structure:</strong> personal, an individual contract with a company,
     versus common, a shared pool for the group.</p>
     <p>The pattern: commercial is individual and profit-facing; collaborative is shared and
     solidarity-facing.</p>'''),
]

FINAL_META = {
    'slug': 'final-exam',
    'title': 'Final Exam',
    'brand_sub': 'Practice Final — Lectures 1–4',
    'h1': 'Practice Final Exam',
    'lede': ('A comprehensive practice final across all four delivered lectures: thirty multiple-choice '
             'questions drawn evenly from the course, then eight written questions with model answers. '
             'Sit it in one pass without the cheat sheets open.'),
    'meta': [('30', 'multiple choice'), ('8', 'written questions'), ('L1–L4', 'coverage')],
    'scope': 'Lectures 1–4',
}

# The final draws a spread from both halves plus synthesis items unique to it.
FINAL_EXTRA_MCQ = [
    ("Which characteristic of transactions explains why analogy can extend a ruling to a case no text "
     "ever named?",
     "L1 · Block 10",
     ["They rest on general bases and principles",
      "They are based on reasons and benefits",
      "Permissibility is the default",
      "They are both flexible and constant"], 1,
     "Because the rulings are caused and benefit-bearing, the cause can be found in a new case."),
    ("Incorporeal rights sit at the bottom of the rights hierarchy. Trace their full path from the top.",
     "L2 · Block 8 · L3 · Block 1",
     ["Rights → Political → Financial → Incorporeal",
      "Rights → Civil → General → Incorporeal",
      "Rights → Civil → Private → Financial → Incorporeal",
      "Rights → Civil → Private → Family → Incorporeal"], 2,
     "Civil, then private, then financial, then the third of the three financial rights."),
    ("A single modern contract that merges selling and renting is both a Lecture 1 category and a Lecture "
     "3 topic. Which case of the definition does it illustrate?",
     "L1 · Block 5",
     ["Cases unknown in earlier ages",
      "Rules updated due to progress",
      "New names, same old ruling",
      "Transactions formulated from several old forms combined"], 3,
     "Leasing contracts merging sale and rent are the textbook example of case 4, alongside murabaha."),
    ("Retirement insurance is said to contain no gharar. Why?",
     "L4 · Block 6",
     ["Because the state guarantees the payout",
      "Because it is a donation contract, and labour are both insured and insurer",
      "Because the pension amount is fixed in advance",
      "Because participation is compulsory"], 1,
     "A donation contract removes the compensation-for-price exchange that gharar attaches to."),
    ("Which of these is prohibited even though the name suggests otherwise — per the hadith about drinking "
     "khamr under another name?",
     "L1 · Block 5",
     ["Murabaha", "Bank interest", "Waqf", "Collaborative insurance"], 1,
     "Changing the name never changes the ruling; interest remains riba."),
    ("Both copyright and trade name include a Shariah reason that patent omits. Which is it?",
     "L3 · Blocks 6, 10, 12",
     ["Benefits are compensable in Islam",
      "General custom ('urf) admits the right",
      "Plagiarism is prohibited",
      "Rights correspond to responsibilities"], 1,
     "Patent is recognised for three reasons only; 'urf is the one it drops."),
    ("The Ash'arites pooling their food is cited as an example of:",
     "L4 · Block 5",
     ["The kinship system (Aqilah)", "The social solidarity system",
      "Reciprocal insurance", "The People of Zakat"], 1,
     "The Prophet ﷺ praised them: \"they are of me, and I am of them.\""),
    ("What happens to a collaborative insurance fund's surplus after all claims are settled?",
     "L4 · Block 13",
     ["The managing company keeps it as its administration fee",
      "It is donated to charity",
      "It belongs entirely to the participants, who may take it back or roll it forward",
      "It is split evenly between the company and participants"], 2,
     "The company may administer the surplus and its investment interest, but keeps none of it."),
    ("Which principle allows a jurisprudent to treat a newly invented financial instrument as permissible "
     "in the absence of any text about it?",
     "L1 · Block 9",
     ["Ijma'", "Al-ibāḥah — permissibility is the original rule",
      "Maqasid al-Shari'ah", "The restriction principle"], 1,
     "No evidence of prohibition means permissible — for transactions, not for worship."),
    ("Mandatory car insurance in a country where only commercial cover is available falls under which "
     "exception?",
     "L4 · Block 12",
     ["Dependent, not original", "Necessity", "Free", "None — it remains prohibited"], 1,
     "Necessity is a classic fiqh override; the lecture names exactly this scenario."),
]

FINAL_EXTRA_WRITTEN = [
    ("Trace a single thread through the whole course: how does the fiqh definition of property (māl) "
     "connect Lecture 1's characteristics to Lecture 3's incorporeal rights?",
     "L1 · Blocks 7–11 · L3 · Block 1",
     '''<p>Lecture 1 establishes that transactions rest on general bases and principles rather than
     exhaustive detail, that permissibility is their original rule, and that their rulings are based on
     reasons and benefits. Those three characteristics together mean a jurisprudent does not need a text
     naming a new instrument in order to rule on it.</p>
     <p>Lecture 3 then applies exactly that machinery. Property (māl) is defined by a principle — recognised
     value among people plus lawful utility — not by an enumerated list of physical objects. Because the
     standard is a principle, an intangible creation satisfies it, so copyright, patent, and trade name are
     property, may be sold, bought, or leased, and are financial rights safeguarded by Shariah.</p>'''),
    ("A student answers that commercial insurance is prohibited \"because of gharar.\" Correct and "
     "complete the answer.",
     "L4 · Block 11",
     '''<p>Gharar is only one of three reasons. The full answer is gharar, gambling, and riba (G.G.R.).</p>
     <p><strong>Gharar:</strong> the contract carries heavy uncertainty and deception, and every
     compensation contract containing deception is corrupted. <strong>Gambling:</strong> one party gains at
     the other's unearned expense on pure chance — an insured may pay one premium and collect a large
     payout, or pay indefinitely and receive nothing. <strong>Riba:</strong> both forms, depending on the
     payout — more than paid in is ribā al-fadl, exactly what was paid is ribā al-nasī'ah, and nothing paid
     means the company took the money illegitimately.</p>'''),
]
