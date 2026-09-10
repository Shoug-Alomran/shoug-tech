#!/usr/bin/env python3
"""Build the ETHCS303 video explanation pages.

Each recording gets its own page with an embedded player, a poster thumbnail and
a caption describing what the recording actually covers. The section index
becomes a card grid linking to those pages.

The existing video-explanations/index.html supplies the page chrome (header,
sidebar, tabs, footer, scripts) so the generated pages stay in sync with the
rest of the site.

Usage:
    python3 scripts/build_ethics_video_pages.py              # rebuild pages
    python3 scripts/build_ethics_video_pages.py --thumbnails # also re-cut posters

Run scripts/build_academic_sidebar.py afterwards: the generated pages inherit the
section index's sidebar, so the per-video active item is stamped by that script.

The like/dislike buttons write to Firestore under pageReactions/{key}/votes/{uid},
which needs this rule in the Firebase console (Firestore > Rules):

    match /pageReactions/{page}/votes/{uid} {
      allow read: if true;
      allow write: if request.auth != null && request.auth.uid == uid;
    }

Until that rule exists the buttons render and the counts read as zero.

Thumbnails are cut from the local recordings in --source (the iCloud Ethics
folder); the committed JPEGs are what the pages use, so --thumbnails is only
needed when a recording changes.
"""

import argparse
import html
import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOCS = REPO / 'docs'
SECTION = DOCS / 'academics/other-courses/ethcs303/video-explanations'
SECTION_URL = '/academics/other-courses/ethcs303/video-explanations/'
SITE = 'https://shoug-tech.com'
R2 = 'https://pub-1ae2691df7364eea93afb4e67996d97c.r2.dev'
BREAKDOWNS = '/academics/other-courses/ethcs303/slide-breakdowns/'

# Folder -> the title the slide breakdown page itself carries.
BREAKDOWN_LABELS = {
    '01-moral-systems-ethical-concepts-and-theories/': 'Moral Systems, Ethical Concepts, and Theories',
    '02-kantianism/': 'Kantianism',
    '03-utilitarianism/': 'Utilitarianism',
    '04-social-contract-theory/': 'Social Contract Theory',
    '05-professional-ethics/': 'Professional Ethics',
    '06-ethical-issues-in-systems-analysis-and-software-engineering/':
        'Ethical Issues in Systems Analysis and Software Engineering',
    '09-privacy-issues-in-cyberspace/': 'Privacy Issues in Cyberspace',
    '11-social-engineering/': 'Social Engineering',
    '14-intellectual-property-laws/': 'Intellectual Property Laws',
    '15-cyber-laws-in-saudi-arabia/': 'Cyber Laws in Saudi Arabia',
}

# --------------------------------------------------------------------------- #
# the recordings
#
# `source` is the file inside the iCloud Ethics folder, `at` the fraction of the
# runtime the poster frame is cut from, and `covers` the points the recording
# actually walks through.
# --------------------------------------------------------------------------- #

GROUPS = [
    ('Ethical theories', 'النظريات الأخلاقية'),
    ('Professional practice', 'الممارسة المهنية'),
    ('Privacy in cyberspace', 'الخصوصية في الفضاء السيبراني'),
    ('Social engineering', 'الهندسة الاجتماعية'),
    ('Intellectual property', 'الملكية الفكرية'),
    ('Cyber law', 'القوانين السيبرانية'),
]

VIDEOS = [
    {
        'slug': 'moral-systems-and-ethical-theories',
        'title': 'Moral Systems, Ethical Concepts, and Theories',
        'title_ar': 'النظم الأخلاقية والمفاهيم والنظريات',
        'group': 'Ethical theories',
        'video': 'ethics/moral-systems-ethical-concepts-and-theories-mp4.mp4',
        'source': 'Moral Systems, Ethical Concepts, and Theories.mp4',
        'seconds': 1996,
        'at': 0.06,
        'breakdown': '01-moral-systems-ethical-concepts-and-theories/',
        'caption': 'A walkthrough of the chapter one breakdown: the difference between '
                   'morality and ethics, what a moral system is built from, and all six '
                   'ethical theories side by side.',
        'caption_ar': 'شرح لتفكيك الفصل الأول: الفرق بين الأخلاق وعلم الأخلاق، ومما يتكون '
                      'النظام الأخلاقي، والنظريات الأخلاقية الست جنبًا إلى جنب.',
        'covers': [
            'Morality versus ethics — morality is the rulebook, ethics is the analysis of the rulebook',
            'What a moral system consists of: core values, rules of conduct, principles of evaluation',
            'Why subjective relativism and cultural relativism fail as ethical theories',
            'Divine Command Theory, Deontology, Consequentialism, Social Contract Theory and Virtue Ethics',
            'The four things every ethical theory shares: right action, free choice, human well-being, obligations over preferences',
            'The "Really Determined Dudes Convince Confident Villagers" mnemonic for all six theories',
            'A side-by-side comparison table of moral authority, focus and workability',
        ],
    },
    {
        'slug': 'kantianism',
        'title': 'Kantianism',
        'title_ar': 'الكانطية',
        'group': 'Ethical theories',
        'video': 'ethics/kantianism-mp4.mp4',
        'source': 'Kantianism.mp4',
        'seconds': 1480,
        'at': 0.06,
        'breakdown': '02-kantianism/',
        'caption': 'Duty-based ethics from the ground up: the universalizability test, both '
                   'formulations of the Categorical Imperative, and perfect versus imperfect duties.',
        'caption_ar': 'الأخلاق القائمة على الواجب من الأساس: اختبار قابلية التعميم، وصيغتا '
                      'الأمر القطعي، والواجبات التامة مقابل الناقصة.',
        'covers': [
            'Why Kantianism judges the act and the rule behind it, never the consequences',
            'The four pillars: duty-based, universal, equal, logical',
            'The universalizability test — identify the rule, universalize it, check for self-contradiction',
            'The two Categorical Imperative formulations (universal law, treat people as ends)',
            'Perfect versus imperfect duties, and which one wins when they conflict',
            'Worked cases: Carla\'s plagiarism, the semiconductor plant closure, the murderer at the door',
        ],
    },
    {
        'slug': 'utilitarianism',
        'title': 'Utilitarianism',
        'title_ar': 'النفعية',
        'group': 'Ethical theories',
        'video': 'ethics/utilitarianism-mp4.mp4',
        'source': 'Utilitarianism.mp4',
        'seconds': 1245,
        'at': 0.06,
        'breakdown': '03-utilitarianism/',
        'caption': 'Consequence-based ethics: the Principle of Utility, act versus rule '
                   'utilitarianism, and how a cost-benefit calculation is actually run.',
        'caption_ar': 'الأخلاق القائمة على النتائج: مبدأ المنفعة، والنفعية الفعلية مقابل '
                      'النفعية القاعدية، وكيفية إجراء حساب المنافع والأضرار عمليًا.',
        'covers': [
            'Bentham\'s hedonic calculus and Mill\'s refinement on the quality of happiness',
            'The Principle of Utility — the greatest happiness for the greatest number affected',
            'Act utilitarianism: judging each individual act by its own consequences',
            'Rule utilitarianism: judging the rule behind the act',
            'The highway construction case study, weighed benefit by benefit',
            'Where rule utilitarianism and Kantianism agree on the rule but differ on the reason',
        ],
    },
    {
        'slug': 'social-contract-theory',
        'title': 'Social Contract Theory',
        'title_ar': 'نظرية العقد الاجتماعي',
        'group': 'Ethical theories',
        'video': 'ethics/social-contract-mp4.mp4',
        'source': 'Social Contract.mp4',
        'seconds': 1371,
        'at': 0.06,
        'breakdown': '04-social-contract-theory/',
        'caption': 'From Hobbes\'s state of nature to Rawls\'s difference principle, plus the '
                   'rights vocabulary the theory runs on and where it breaks down.',
        'caption_ar': 'من حالة الطبيعة عند هوبز إلى مبدأ الاختلاف عند رولز، مع مفردات الحقوق '
                      'التي تقوم عليها النظرية وحدود قصورها.',
        'covers': [
            'Hobbes on life without rules — "solitary, poor, nasty, brutish, and short"',
            'How the contract is formed and why no one is above the rules',
            'Rawls\'s two principles, including the difference principle on inequality',
            'Negative rights (leave me alone) versus positive rights (do something for me)',
            'Why some problems need a collective rule rather than individual good behaviour',
            'Conflicting rights, and social contract theory compared with Kantianism',
        ],
    },
    {
        'slug': 'professional-ethics',
        'title': 'Professional Ethics',
        'title_ar': 'أخلاقيات المهنة',
        'group': 'Professional practice',
        'video': 'ethics/professional-ethics-mp4.mp4',
        'source': 'Professional Ethics.mp4',
        'seconds': 2927,
        'at': 0.06,
        'breakdown': '05-professional-ethics/',
        'caption': 'The full chapter three walkthrough — the relationships a professional is '
                   'bound by, the obligations owed to society, whistle-blowing, and codes of ethics.',
        'caption_ar': 'شرح كامل للفصل الثالث: العلاقات التي يلتزم بها المحترف، والالتزامات '
                      'تجاه المجتمع، والإبلاغ عن المخالفات، ومواثيق الأخلاق المهنية.',
        'covers': [
            'The employer-employee relationship: loyalty, trade secrets, NDAs and non-compete clauses',
            'Why loyalty means supporting legitimate goals, not covering up wrongdoing',
            'Obligations to society — the S-N-M-D-E-P mnemonic, including due care and end users',
            'Professional-professional obligations, and why moral responsibility cannot be delegated',
            'The whistle-blower archetypes: altruist, avenger, organization man, alarmist, bounty hunter',
            'How motive affects the moral judgement of whistle-blowing, and typical corporate responses',
            'What a code of ethics is for and the six functions it serves',
        ],
    },
    {
        'slug': 'ethical-issues-in-systems-analysis-and-software-engineering',
        'title': 'Ethical Issues in Systems Analysis and Software Engineering',
        'title_ar': 'القضايا الأخلاقية في تحليل النظم وهندسة البرمجيات',
        'group': 'Professional practice',
        'video': 'ethics/sa-se-mov.mp4',
        'source': 'SA:SE.mov',
        'seconds': 2829,
        'at': 0.06,
        'breakdown': '06-ethical-issues-in-systems-analysis-and-software-engineering/',
        'caption': 'What systems analysts and software engineers each owe the people affected '
                   'by their systems, from safety-critical development practice to the LOPSA code.',
        'caption_ar': 'ما يدين به محللو النظم ومهندسو البرمجيات لمن تتأثر حياتهم بأنظمتهم، '
                      'من ممارسات تطوير الأنظمة الحرجة إلى ميثاق LOPSA.',
        'covers': [
            'The two roles: the systems analyst decides WHAT, the software engineer decides HOW',
            'The six problem areas facing SA/SE — the S-D-P-U-C-I mnemonic',
            'Five practices for safety-critical development: rigorous process, hazard log, thorough testing, risk analysis, N-version redundancy',
            'The three unethical syndromes — red lies, sweep it under the rug, cancelled vacation',
            'Safety-critical scenarios: the anti-missile system and the fighter jet software',
            'Consultation fees, the slippery slope, and the informed consent policy for sysadmins',
            'The LOPSA code of ethics and its ten principles',
        ],
    },
    {
        'slug': 'privacy-in-cyberspace-part-1',
        'title': 'Privacy in Cyberspace — Part 1',
        'title_ar': 'الخصوصية في الفضاء السيبراني — الجزء الأول',
        'group': 'Privacy in cyberspace',
        'video': 'ethics/cyberspace-part-1-mov.mp4',
        'source': 'cyberspace part 1.mov',
        'seconds': 720,
        'at': 0.06,
        'breakdown': '09-privacy-issues-in-cyberspace/',
        'caption': 'What privacy means before the technology enters: the four ways '
                   'cybertechnology changed it, the categories of private information, and the '
                   'three questions every privacy case asks.',
        'caption_ar': 'ما تعنيه الخصوصية قبل دخول التقنية: الطرق الأربع التي غيّرت بها التقنية '
                      'السيبرانية الخصوصية، وفئات المعلومات الخاصة، والأسئلة الثلاثة الأساسية.',
        'covers': [
            'The A-S-D-K mnemonic — amount, speed, duration and kind of data collection',
            'Privacy as freedom from intrusion, and informational privacy as control over data flow',
            'Why privacy is a social value other rights depend on',
            'The four categories of private information — the C-H-I-P mnemonic',
            'The three key cyber-privacy questions on collection, sharing and control',
            'How personal information is collected, merged, matched and mined',
        ],
    },
    {
        'slug': 'privacy-in-cyberspace-part-2',
        'title': 'Privacy in Cyberspace — Part 2',
        'title_ar': 'الخصوصية في الفضاء السيبراني — الجزء الثاني',
        'group': 'Privacy in cyberspace',
        'video': 'ethics/cyberspace-part-2-mov.mp4',
        'source': 'cyberspace part 2.mov',
        'seconds': 1385,
        'at': 0.06,
        'breakdown': '09-privacy-issues-in-cyberspace/',
        'caption': 'The collection technologies themselves — dataveillance, surveillance in '
                   'public and at work, cookies of every kind, behavioural tracking and RFID.',
        'caption_ar': 'تقنيات جمع البيانات نفسها: المراقبة الرقمية، والمراقبة في الأماكن العامة '
                      'وفي العمل، وأنواع ملفات الارتباط، والتتبع السلوكي، وتقنية RFID.',
        'covers': [
            'Dataveillance and "invisible supervisors" monitoring employees around the clock',
            'Government surveillance, surveillance tools and surveillance drones',
            'First-party, third-party tracking and flash cookies — and which ones survive deletion',
            'Privacy concerns with cookies, opt-in versus opt-out, and the limits of each',
            'Online behavioural tracking across sites and advertising networks',
            'RFID technology, smart versus dumb tags, and RFID implanted in humans',
        ],
    },
    {
        'slug': 'social-engineering',
        'title': 'Social Engineering',
        'title_ar': 'الهندسة الاجتماعية',
        'group': 'Social engineering',
        'video': 'ethics/social-engineering/social-engineering-mp4.mp4',
        'source': 'Social Engineering/Social Engineering.mp4',
        'seconds': 346,
        'at': 0.06,
        'breakdown': '11-social-engineering/',
        'caption': 'The opening lesson of the social engineering chapter: manipulating people '
                   'into giving up confidential information, and the damage that follows.',
        'caption_ar': 'الدرس الافتتاحي لفصل الهندسة الاجتماعية: التلاعب بالأشخاص لدفعهم إلى '
                      'الإفصاح عن معلومات سرية، والأضرار الناتجة عن ذلك.',
        'covers': [
            'Social engineering as the art of manipulating people, not systems',
            'What attackers want from an individual target: passwords and bank information',
            'Installing malicious software — keyloggers and trojans — for ongoing access',
            'The dangers: identity theft, data theft, data corruption, unplanned downtime, physical security threats',
        ],
    },
    {
        'slug': 'phishing',
        'title': 'Phishing',
        'title_ar': 'التصيّد الإلكتروني',
        'group': 'Social engineering',
        'video': 'ethics/social-engineering/phishing-mp4.mp4',
        'source': 'Social Engineering/Phishing.mp4',
        'seconds': 647,
        'at': 0.06,
        'breakdown': '11-social-engineering/',
        'caption': 'The email attack: fraudulent messages that look authentic, the difference '
                   'between spear phishing and whaling, and a real phishing email pulled apart.',
        'caption_ar': 'هجوم البريد الإلكتروني: رسائل احتيالية تبدو أصلية، والفرق بين التصيّد '
                      'الموجّه وصيد الحيتان، مع تحليل رسالة تصيّد حقيقية.',
        'covers': [
            'Phishing as obtaining personal information through fraudulent email',
            'Why the messages appear to come from a school, bank, CEO or IT support',
            'Fake links and submission forms that harvest credentials',
            'Spear phishing — one specific individual, like spearing one fish',
            'Whaling — targeting people inside a business or government office',
            'Example 1 walked line by line, then how to gauge authenticity: typos, unofficial documents, false URLs',
        ],
    },
    {
        'slug': 'smishing',
        'title': 'Smishing',
        'title_ar': 'التصيّد عبر الرسائل النصية',
        'group': 'Social engineering',
        'video': 'ethics/social-engineering/smishing-mp4.mp4',
        'source': 'Social Engineering/Smishing.mp4',
        'seconds': 375,
        'at': 0.06,
        'breakdown': '11-social-engineering/',
        'caption': 'The SMS variant: text messages crafted for immediate action, where the '
                   'phone numbers come from, and the prize scam example from the slides.',
        'caption_ar': 'النسخة عبر الرسائل النصية: رسائل مصممة لدفع الضحية إلى تصرّف فوري، ومصدر '
                      'أرقام الهواتف، ومثال احتيال الجائزة من الشرائح.',
        'covers': [
            'Smishing defined — SMS used to lure victims into immediate action',
            'Fear and greed wording: impending account suspension, fraudulent activity detected',
            'Where attackers get numbers: dark web data breaches, web crawlers, random generation',
            'Example 1 — the prize message offering a 200,000 riyal draw',
            'Defending with simulated attacks and security awareness training',
        ],
    },
    {
        'slug': 'vishing',
        'title': 'Vishing',
        'title_ar': 'التصيّد الصوتي',
        'group': 'Social engineering',
        'video': 'ethics/social-engineering/vishing-mp4.mp4',
        'source': 'Social Engineering/Vishing.mp4',
        'seconds': 284,
        'at': 0.06,
        'breakdown': '11-social-engineering/',
        'caption': 'The phone attack: a caller imitating someone in authority, why caller ID is '
                   'not a defence, and why help desks are the softest target.',
        'caption_ar': 'الهجوم الهاتفي: متصل ينتحل صفة شخص ذي سلطة، ولماذا لا يُعد معرّف المتصل '
                      'وسيلة حماية، ولماذا يُعد مكتب المساعدة الهدف الأسهل.',
        'covers': [
            'Vishing as the most prevalent social engineering attack, conducted by phone',
            'Pulling information out of a user gradually by imitating authority',
            'PBX tricks and operator manipulation — caller ID is not always the best defence',
            'Why help desks are particularly vulnerable: trained to be helpful, minimally trained in security',
            'Five protection steps, ending with treating vishing the way you treat smishing',
        ],
    },
    {
        'slug': 'impersonation',
        'title': 'Impersonation',
        'title_ar': 'انتحال الشخصية',
        'group': 'Social engineering',
        'video': 'ethics/social-engineering/impersenation-mp4.mp4',
        'source': 'Social Engineering/impersenation.mp4',
        'seconds': 266,
        'at': 0.06,
        'breakdown': '11-social-engineering/',
        'caption': 'Pretexting as someone else to get physical access — the delivery person and '
                   'the tech support vectors, and why a uniform carries built-in trust.',
        'caption_ar': 'انتحال صفة شخص آخر للحصول على وصول مادي: مسار عامل التوصيل ومسار الدعم '
                      'الفني، ولماذا يمنح الزي الرسمي ثقة تلقائية.',
        'covers': [
            'Impersonation defined as pretexting to obtain information or access',
            'The two common attack vectors: delivery person and tech support',
            'Why the delivery vector needs little acting — credentials, papers and packages in order',
            'The Ministry of Interior uniform example and the trust it buys',
            'Tech support impersonation: physical access to the machine, "anti-virus" installs and onward network access',
        ],
    },
    {
        'slug': 'dumpster-diving',
        'title': 'Dumpster Diving',
        'title_ar': 'التنقيب في النفايات',
        'group': 'Social engineering',
        'video': 'ethics/social-engineering/dumpster-diving-mp4.mp4',
        'source': 'Social Engineering/Dumpster Diving.mp4',
        'seconds': 225,
        'at': 0.30,
        'breakdown': '11-social-engineering/',
        'caption': 'Also called trashing — what an attacker reconstructs about an organisation '
                   'from the paper and hardware it throws away.',
        'caption_ar': 'ويُسمى أيضًا التنقيب في المهملات: ما يستطيع المهاجم استنتاجه عن المنشأة '
                      'من الأوراق والأجهزة التي تتخلص منها.',
        'covers': [
            'Dumpster diving (trashing) as a source of a rich vein of information',
            'Phone books and organisational charts — names, numbers and positions of authority',
            'Memos for authenticity, policy manuals for how secure the company really is',
            'Calendars that reveal which employees are out of town',
            'System manuals and technical data as the keys to the network',
            'Discarded hard drives that can be restored',
        ],
    },
    {
        'slug': 'avoiding-social-engineering-fraud',
        'title': 'How to Avoid Social Engineering Fraud',
        'title_ar': 'كيفية تجنّب احتيال الهندسة الاجتماعية',
        'group': 'Social engineering',
        'video': 'ethics/social-engineering/how-to-avoid-se-fraud-mp4.mp4',
        'source': 'Social Engineering/How to avoid se fraud.mp4',
        'seconds': 494,
        'at': 0.06,
        'breakdown': '11-social-engineering/',
        'caption': 'The defensive close to the chapter: the habits that break a social '
                   'engineering attempt before it lands.',
        'caption_ar': 'الخاتمة الدفاعية للفصل: العادات التي تُفشل محاولة الهندسة الاجتماعية قبل '
                      'أن تنجح.',
        'covers': [
            'Secure your devices, set spam filters high, beware of any download',
            'Delete any request for financial information or passwords',
            'Slow down — urgency and high-pressure tactics are the tell',
            'Research the facts yourself instead of using the links you were sent',
            'Unsolicited help you did not request is a scam, including charity requests',
            'Foreign lottery, sweepstakes and fund transfer offers are fake',
        ],
    },
    {
        'slug': 'intellectual-property-laws',
        'title': 'Intellectual Property Laws',
        'title_ar': 'قوانين الملكية الفكرية',
        'group': 'Intellectual property',
        'video': 'ethics/intellectual-property/intellectual-property-intro-mp4.mp4',
        'source': 'Intellectual Property/Intellectual Property Intro.mp4',
        'seconds': 1685,
        'at': 0.06,
        'breakdown': '14-intellectual-property-laws/',
        'caption': 'The opening of the intellectual property chapter: the three bodies of law, '
                   'the rights a copyright actually grants, fair use, and plagiarism versus infringement.',
        'caption_ar': 'مقدمة فصل الملكية الفكرية: أنواع القوانين الثلاثة، والحقوق التي يمنحها '
                      'حق المؤلف، والاستخدام العادل، والانتحال مقابل انتهاك حق المؤلف.',
        'covers': [
            'Copyright law for authored works, patent law for inventions, trade secret law for critical information',
            'Reproduction, distribution, derivative and performance rights',
            'What counts as a derivative work — translating a novel, filming a book',
            'The four fair use factors: purpose, nature, portion and effect',
            'Why fair use does not apply to unpublished works',
            'Plagiarism versus copyright violation, and why neither one implies the other',
        ],
    },
    {
        'slug': 'patents-and-trademarks',
        'title': 'Patents and Trademarks',
        'title_ar': 'براءات الاختراع والعلامات التجارية',
        'group': 'Intellectual property',
        'video': 'ethics/intellectual-property/patents-mp4.mp4',
        'source': 'Intellectual Property/Patents.mp4',
        'seconds': 1368,
        'at': 0.06,
        'breakdown': '14-intellectual-property-laws/',
        'caption': 'What a patent protects and how it differs from a copyright, the software '
                   'patent question, the three kinds of infringement, and trademarks.',
        'caption_ar': 'ما تحميه براءة الاختراع وكيف تختلف عن حق المؤلف، ومسألة براءات البرمجيات، '
                      'وأنواع الانتهاك الثلاثة، والعلامات التجارية.',
        'covers': [
            'Invention defined — any new and useful process, machine, manufacture or improvement',
            'A patent grants a property right to inventors and excludes others from making, using or selling',
            'Unlike copyright, a patent prevents independent creation as well as copying',
            'Software patents, their cost and enforcement, and USPTO practice',
            'Direct, indirect and induced patent infringement',
            'Trademarks — registered signs that let consumers tell one company\'s products from another\'s',
        ],
    },
    {
        'slug': 'trade-secrets',
        'title': 'Trade Secrets',
        'title_ar': 'الأسرار التجارية',
        'group': 'Intellectual property',
        'video': 'ethics/intellectual-property/trade-secrets-mp4.mp4',
        'source': 'Intellectual Property/Trade Secrets.mp4',
        'seconds': 1934,
        'at': 0.06,
        'breakdown': '14-intellectual-property-laws/',
        'caption': 'Protection by keeping the information undisclosed — what qualifies, how '
                   'competitive intelligence gathers it legally, SAIP, and cybersquatting.',
        'caption_ar': 'الحماية عبر إبقاء المعلومة غير مفصح عنها: ما الذي يُعد سرًا تجاريًا، وكيف '
                      'تجمعه الاستخبارات التنافسية بطرق مشروعة، وهيئة سيب، والاستيلاء على النطاقات.',
        'covers': [
            'A trade secret as a formula, practice, process or compilation not generally known',
            'Trade secrets as the alternative to patent or trademark law — the information stays undisclosed',
            'The Saudi Authority for Intellectual Property (SAIP) and its role in the national IP strategy',
            'Competitive intelligence and the public sources it draws on',
            'Annual reports, press releases, trade press, supplier interviews and patents as CI data',
            'Cybersquatting, the michaeljordan.com style example, and the anti-cybersquatting laws',
        ],
    },
    {
        'slug': 'cyber-laws-in-saudi-arabia',
        'title': 'Cyber Laws in Saudi Arabia',
        'title_ar': 'القوانين السيبرانية في السعودية',
        'group': 'Cyber law',
        'video': 'ethics/cyber-laws/cyber-laws-in-saudi-mp4.mp4',
        'source': 'Cyber Laws/Cyber Laws In Saudi.mp4',
        'seconds': 1786,
        'at': 0.30,
        'breakdown': '15-cyber-laws-in-saudi-arabia/',
        'caption': 'How cybercrime is classified and what the Saudi Anti-Cyber Crime Law says, '
                   'article by article, with the penalty attached to each.',
        'caption_ar': 'كيف تُصنّف الجرائم السيبرانية وما ينص عليه نظام مكافحة الجرائم المعلوماتية '
                      'السعودي، مادة بمادة، مع العقوبة المقررة لكل منها.',
        'covers': [
            'Why legislatures across the world codified laws against cyber-crime',
            'Classification of cybercrimes: against person, against property, against government',
            'Credit card skimming, software piracy, identity theft, DDOS and virus transmission',
            'Cybersquatting, copyright infringement and IPR violations',
            'Web jacking — taking control of a website for ransom or political purpose',
            'The Saudi Anti-Cyber Crime Law articles, including Article 5 on unlawful access',
            'The penalties attached to each article, in prison terms and fines',
        ],
    },
]


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #

def runtime(seconds):
    return '%d:%02d' % divmod(seconds, 60)


def esc(text):
    return html.escape(text, quote=True)


def page_url(video):
    return SECTION_URL + video['slug'] + '/'


def thumb_url(video):
    return SECTION_URL + 'thumbnails/' + video['slug'] + '.jpg'


def group_ar(name):
    return dict(GROUPS)[name]


# --------------------------------------------------------------------------- #
# thumbnails
# --------------------------------------------------------------------------- #

def build_thumbnails(source_root):
    out = SECTION / 'thumbnails'
    out.mkdir(parents=True, exist_ok=True)
    for video in VIDEOS:
        src = source_root / video['source']
        if not src.exists():
            raise SystemExit('Missing recording: ' + str(src))
        dest = out / (video['slug'] + '.jpg')
        subprocess.run([
            'ffmpeg', '-y', '-v', 'error', '-nostdin',
            '-ss', str(video['seconds'] * video['at']), '-i', str(src),
            '-frames:v', '1', '-q:v', '4',
            '-vf', 'scale=640:360:force_original_aspect_ratio=decrease,'
                   'pad=640:360:(ow-iw)/2:(oh-ih)/2:black',
            str(dest),
        ], check=True)
        print('poster: %s (%.0f KB)' % (dest.name, dest.stat().st_size / 1024))


# --------------------------------------------------------------------------- #
# page chrome
# --------------------------------------------------------------------------- #

STYLE_RE = re.compile(r'<style>\n#section-video-explanations.*?</style>(?=</head>)', re.S)
SECTION_RE = re.compile(r'<section id="section-video-explanations".*?</section>', re.S)
CRUMB_RE = re.compile(r'<span class="current" data-en-text="Video Explanations"[^>]*>[^<]*</span>')
LAZY_RE = re.compile(r'<script>\n\(\(\) => \{\n  const section = document\.getElementById.*?</script>\n', re.S)

BASE_TITLE = 'SHOUG.TECH | ETHCS303 Video Explanations'
BASE_DESC = ('SHOUG.TECH | ETHCS303 Video Explanations study material from '
             'Shoug&#x27;s Digital Garden.')
BASE_URL = SITE + SECTION_URL
BASE_IMAGE = SITE + '/assets/og-banner.png'

PAGE_CSS = """<style>
#section-video-explanations { margin: 32px 0 56px; padding: 0 32px; scroll-margin-top: 24px; }
#section-video-explanations .text-block { max-width: 70ch; color: var(--text-secondary); line-height: 1.7; }

.video-group { margin-top: 36px; }
.video-group-label {
    display: flex; align-items: baseline; gap: 12px;
    font-family: var(--font-mono); font-size: 11px; font-weight: 500;
    letter-spacing: 0.16em; text-transform: uppercase;
    color: var(--text-tertiary); margin-bottom: 16px;
}
.video-group-label::after { content: ''; flex: 1; height: 1px; background: var(--border-dim); }
.video-group-count { font-size: 10px; letter-spacing: 0.1em; color: var(--text-tertiary); }

.video-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(288px, 1fr)); gap: 20px; }
.video-card {
    display: flex; flex-direction: column;
    border: 1px solid var(--border-dim); border-radius: 10px;
    background: var(--bg-elevated); overflow: hidden;
    transition: border-color 0.18s ease, transform 0.18s ease;
}
.video-card:hover, .video-card:focus-visible {
    border-color: var(--border-purple); transform: translateY(-2px);
}
.video-card:focus-visible { outline: 2px solid var(--brand-purple); outline-offset: 2px; }
.video-card-thumb { position: relative; display: block; background: #000; aspect-ratio: 16 / 9; }
.video-card-thumb img { display: block; width: 100%; height: 100%; object-fit: cover; }
.video-card-play {
    position: absolute; inset: 0; display: flex; align-items: center; justify-content: center;
    background: linear-gradient(180deg, rgba(5, 2, 10, 0) 45%, rgba(5, 2, 10, 0.55) 100%);
}
.video-card-play svg { width: 44px; height: 44px; opacity: 0.9; filter: drop-shadow(0 2px 6px rgba(0,0,0,0.5)); }
.video-card-duration {
    position: absolute; right: 8px; bottom: 8px;
    padding: 2px 6px; border-radius: 4px;
    background: rgba(5, 2, 10, 0.82); color: #fff;
    font-family: var(--font-mono); font-size: 11px; letter-spacing: 0.04em;
}
.video-card-body { display: block; padding: 14px 16px 18px; }
.video-card-title {
    display: block; font-family: var(--font-display); font-size: 17px; font-weight: 600;
    letter-spacing: 0.01em; color: var(--text-primary); margin-bottom: 6px;
}
.video-card-caption { display: block; font-size: 13px; line-height: 1.6; color: var(--text-secondary); }

.video-detail-head { margin-bottom: 20px; }
.video-back {
    display: inline-flex; align-items: center; gap: 8px;
    font-family: var(--font-mono); font-size: 11px; letter-spacing: 0.12em; text-transform: uppercase;
    color: var(--text-tertiary); margin-bottom: 18px;
}
.video-back:hover { color: var(--text-purple-bright); }
.video-title {
    font-family: var(--font-display); font-size: 30px; font-weight: 600;
    line-height: 1.25; color: var(--text-primary); margin-bottom: 12px;
}
.video-meta {
    display: flex; flex-wrap: wrap; align-items: center; gap: 10px;
    font-family: var(--font-mono); font-size: 11px; letter-spacing: 0.08em;
    text-transform: uppercase; color: var(--text-tertiary);
}
.video-meta-tag {
    padding: 3px 9px; border: 1px solid var(--border-purple); border-radius: 999px;
    color: var(--text-purple-bright);
}
.video-player { border: 1px solid var(--border-med); border-radius: 10px; overflow: hidden; background: #000; }
.video-player video { display: block; width: 100%; max-height: 78vh; background: #000; }
.video-underplayer {
    display: grid; grid-template-columns: minmax(0, 1fr) auto;
    gap: 24px 32px; align-items: start; margin-top: 18px;
}
.video-caption {
    max-width: 72ch; margin: 0;
    font-size: 15px; line-height: 1.75; color: var(--text-secondary);
}

.video-reactions {
    display: flex; flex-direction: column; gap: 10px; min-width: 190px;
    padding: 14px 16px; border: 1px solid var(--border-dim); border-radius: 10px;
    background: var(--bg-elevated);
}
.video-reactions-label {
    font-family: var(--font-mono); font-size: 10px; letter-spacing: 0.14em;
    text-transform: uppercase; color: var(--text-tertiary);
}
.video-reactions-row { display: flex; gap: 10px; }
.video-vote {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 8px 14px; border: 1px solid var(--border-med); border-radius: 999px;
    background: transparent; color: var(--text-secondary);
    font-family: var(--font-mono); font-size: 12px; cursor: pointer;
    transition: border-color 0.15s ease, color 0.15s ease, background 0.15s ease;
}
.video-vote svg { width: 16px; height: 16px; }
.video-vote:hover { border-color: var(--border-purple); color: var(--text-primary); }
.video-vote:focus-visible { outline: 2px solid var(--brand-purple); outline-offset: 2px; }
.video-vote.is-active {
    border-color: var(--brand-purple); color: var(--text-purple-bright);
    background: rgba(184, 41, 234, 0.12);
}
.video-vote[data-vote="down"].is-active {
    border-color: var(--alert-red); color: var(--alert-red);
    background: rgba(255, 42, 75, 0.1);
}
.video-vote-count { font-variant-numeric: tabular-nums; }
.video-reactions-hint { font-size: 11px; line-height: 1.5; color: var(--text-tertiary); }

.video-discussion { margin-top: 40px; padding-top: 28px; border-top: 1px solid var(--border-dim); }
.video-discussion > h3 {
    font-family: var(--font-mono); font-size: 11px; font-weight: 500;
    letter-spacing: 0.16em; text-transform: uppercase; color: var(--text-tertiary);
    margin-bottom: 16px;
}
.video-discussion > h3::before { content: '// '; color: var(--brand-purple); }
.video-discussion-prompt {
    display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 16px;
    padding: 18px 20px; border: 1px solid var(--border-dim); border-radius: 10px;
    background: var(--bg-elevated);
}
.video-discussion-prompt p { max-width: 60ch; font-size: 14px; line-height: 1.65; color: var(--text-secondary); }
.video-discussion-btn {
    padding: 10px 18px; border: 1px solid var(--border-purple); border-radius: 6px;
    background: rgba(184, 41, 234, 0.1); color: var(--text-purple-bright);
    font-family: var(--font-mono); font-size: 11px; letter-spacing: 0.12em;
    text-transform: uppercase; cursor: pointer;
}
.video-discussion-btn:hover { background: rgba(184, 41, 234, 0.2); }
.video-comment-list { list-style: none; display: grid; gap: 16px; margin-bottom: 20px; }
.video-comment {
    padding: 14px 16px; border: 1px solid var(--border-dim); border-radius: 8px;
    background: var(--bg-elevated);
}
.video-comment--reply { margin-left: 28px; border-left: 2px solid var(--border-purple); }
.video-comment-meta {
    display: flex; flex-wrap: wrap; align-items: baseline; gap: 10px; margin-bottom: 6px;
    font-family: var(--font-mono); font-size: 11px;
}
.video-comment-author { font-weight: 600; }
.video-comment-user, .video-comment-time { color: var(--text-tertiary); }
.video-comment-text { font-size: 14px; line-height: 1.65; color: var(--text-secondary); white-space: pre-wrap; }
/* The site-wide comment section is moved into the slot; drop its standalone framing. */
.video-discussion-slot #shoug-page-comments {
    margin: 0; padding: 0; border-top: none; max-width: none;
}
.video-covers {
    margin-top: 28px; padding: 20px 22px;
    border: 1px solid var(--border-dim); border-radius: 10px; background: var(--bg-elevated);
}
.video-covers h3 {
    font-family: var(--font-mono); font-size: 11px; font-weight: 500;
    letter-spacing: 0.16em; text-transform: uppercase; color: var(--text-tertiary);
    margin-bottom: 14px;
}
.video-covers ul { list-style: none; display: grid; gap: 10px; }
.video-covers li {
    position: relative; padding-left: 20px;
    font-size: 14px; line-height: 1.65; color: var(--text-secondary);
}
.video-covers li::before {
    content: ''; position: absolute; left: 2px; top: 9px;
    width: 6px; height: 6px; background: var(--brand-purple); border-radius: 1px;
}
.video-related {
    display: inline-flex; align-items: center; gap: 10px; margin-top: 20px;
    padding: 12px 16px; border: 1px solid var(--border-dim); border-radius: 8px;
    font-size: 13px; color: var(--text-secondary);
}
.video-related:hover { border-color: var(--border-purple); color: var(--text-primary); }
.video-related span { font-family: var(--font-mono); font-size: 10px; letter-spacing: 0.14em; text-transform: uppercase; color: var(--text-tertiary); }

.video-pager { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 32px; }
.video-pager a {
    flex: 1 1 240px; padding: 14px 16px;
    border: 1px solid var(--border-dim); border-radius: 8px; background: var(--bg-elevated);
}
.video-pager a:hover { border-color: var(--border-purple); }
.video-pager .pager-label {
    display: block; font-family: var(--font-mono); font-size: 10px;
    letter-spacing: 0.14em; text-transform: uppercase; color: var(--text-tertiary); margin-bottom: 6px;
}
.video-pager .pager-title { display: block; font-size: 14px; color: var(--text-primary); line-height: 1.5; }
.video-pager .pager-next { text-align: right; }

@media (max-width: 980px) {
    .video-underplayer { grid-template-columns: 1fr; }
    .video-reactions { flex-direction: row; align-items: center; flex-wrap: wrap; gap: 12px; }
}

@media (max-width: 720px) {
    #section-video-explanations { padding: 0 16px; }
    .video-grid { grid-template-columns: 1fr; gap: 16px; }
    .video-title { font-size: 24px; }
    .video-discussion-prompt { flex-direction: column; align-items: flex-start; }
}
</style>"""

THUMB_UP = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            '<path d="M7 22V10l5-8a2.2 2.2 0 0 1 2 2.4L13 9h5.5a2 2 0 0 1 2 2.4l-1.5 8a2 2 0 0 1-2 1.6Z"/>'
            '<path d="M7 10H4v12h3"/></svg>')

THUMB_DOWN = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
              'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
              '<path d="M17 2v12l-5 8a2.2 2.2 0 0 1-2-2.4L11 15H5.5a2 2 0 0 1-2-2.4l1.5-8A2 2 0 0 1 7 3Z"/>'
              '<path d="M17 14h3V2h-3"/></svg>')

REACTIONS = (
    '<div class="video-reactions" data-video-reactions>'
    '<span class="video-reactions-label" data-en-text="WAS THIS HELPFUL?" '
    'data-ar-text="هل كان هذا مفيدًا؟">WAS THIS HELPFUL?</span>'
    '<div class="video-reactions-row">'
    '<button class="video-vote" type="button" data-vote="up" aria-pressed="false" aria-label="Like this video">'
    '%s<span class="video-vote-count" data-count="up">0</span></button>'
    '<button class="video-vote" type="button" data-vote="down" aria-pressed="false" aria-label="Dislike this video">'
    '%s<span class="video-vote-count" data-count="down">0</span></button>'
    '</div>'
    '<span class="video-reactions-hint" data-reactions-hint hidden></span>'
    '</div>'
) % (THUMB_UP, THUMB_DOWN)

DISCUSSION = (
    '<section class="video-discussion" aria-labelledby="video-discussion-heading">'
    '<h3 id="video-discussion-heading" data-en-text="DISCUSSION" '
    'data-ar-text="النقاش">DISCUSSION</h3>'
    '<div class="video-discussion-preview" data-discussion-preview hidden></div>'
    '<div class="video-discussion-prompt" data-discussion-prompt>'
    '<p data-en-text="Ask about anything in this recording, or answer a classmate. '
    'Sign in with your community profile to post." '
    'data-ar-text="اسأل عن أي جزء في هذا التسجيل أو أجب زميلًا. '
    'سجّل الدخول بحسابك في المجتمع للمشاركة.">'
    'Ask about anything in this recording, or answer a classmate. '
    'Sign in with your community profile to post.</p>'
    '<button class="video-discussion-btn" type="button" data-discussion-signin '
    'data-en-text="Sign in to join" data-ar-text="سجّل الدخول للمشاركة">Sign in to join</button>'
    '</div>'
    '<div class="video-discussion-slot" data-discussion-slot></div>'
    '</section>'
)

PLAY_ICON = ('<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">'
             '<circle cx="12" cy="12" r="11" fill="rgba(5,2,10,0.55)" stroke="rgba(255,255,255,0.8)" stroke-width="1.2"/>'
             '<path d="M10 8.2 16 12l-6 3.8Z" fill="#fff"/></svg>')


def chrome():
    """The section index page, used as the template for every generated page."""
    source = (SECTION / 'index.html').read_text(encoding='utf-8')
    source = LAZY_RE.sub('', source)
    source = STYLE_RE.sub(PAGE_CSS, source)
    return source


LESSON_SCRIPT = '<script src="/javascripts/video-lesson.js" defer></script>'


NAV_RE = re.compile(r'<nav class="[^"]*academic-sidebar[^"]*"[^>]*>.*?</nav>', re.S)


def keep_existing_nav(rendered, target):
    """Carry over the page's own sidebar rather than the section index's.

    Every generated page starts from the section index's chrome, and that chrome
    carries the index's sidebar — the wrong active item, and (after a site-wide
    formatting pass) the wrong whitespace. Reusing what the page already has
    keeps a rebuild from undoing build_academic_sidebar.py or a format run.
    """
    if not target.exists():
        return rendered
    current = NAV_RE.search(target.read_text(encoding='utf-8'))
    if not current:
        return rendered
    return NAV_RE.sub(lambda _m: current.group(0), rendered, count=1)


def render(template, *, url, title, description, body, crumb, image=BASE_IMAGE, scripts=''):
    out = template.replace(BASE_DESC, esc(description))
    out = out.replace(BASE_TITLE, esc(title))
    out = out.replace(BASE_URL, SITE + url)
    if image != BASE_IMAGE:
        out = out.replace(BASE_IMAGE, image)
    out = CRUMB_RE.sub(crumb, out)
    out = SECTION_RE.sub(lambda _m: body, out)
    out = out.replace(LESSON_SCRIPT, '')            # keep re-runs idempotent
    if scripts:
        out = out.replace('</body>', scripts + '</body>')
    return out


# --------------------------------------------------------------------------- #
# bodies
# --------------------------------------------------------------------------- #

INTRO = ('Recorded walkthroughs of the ETHCS303 material. Each lesson has its own page '
         'with the full recording, so pick a topic below.')
INTRO_AR = ('شروحات مسجلة لمادة ETHCS303. لكل درس صفحة خاصة تحتوي التسجيل كاملًا، '
            'فاختر الموضوع من الأسفل.')


def index_body():
    parts = [
        '<section id="section-video-explanations" aria-labelledby="ethics-video-heading">',
        '<h2 class="section-label" id="ethics-video-heading" data-en-text="VIDEO EXPLANATIONS" '
        'data-ar-text="شروحات الفيديو">VIDEO EXPLANATIONS</h2>',
        '<p class="text-block" data-en-text="%s" data-ar-text="%s">%s</p>'
        % (esc(INTRO), esc(INTRO_AR), esc(INTRO)),
    ]
    for name, name_ar in GROUPS:
        items = [v for v in VIDEOS if v['group'] == name]
        if not items:
            continue
        count = '%d video%s' % (len(items), '' if len(items) == 1 else 's')
        parts.append('<div class="video-group">')
        parts.append(
            '<h3 class="video-group-label" data-en-text="%s" data-ar-text="%s">%s'
            '<span class="video-group-count">%s</span></h3>'
            % (esc(name), esc(name_ar), esc(name), count))
        parts.append('<div class="video-grid">')
        for video in items:
            parts.append(
                '<a class="video-card" href="%s" data-ar-title="%s">'
                '<span class="video-card-thumb">'
                '<img src="%s" alt="Slide from the %s recording" width="640" height="360" loading="lazy" decoding="async">'
                '<span class="video-card-play">%s</span>'
                '<span class="video-card-duration">%s</span>'
                '</span>'
                '<span class="video-card-body">'
                '<span class="video-card-title">%s</span>'
                '<span class="video-card-caption">%s</span>'
                '</span></a>'
                % (page_url(video), esc(video['title_ar']), thumb_url(video),
                   esc(video['title']), PLAY_ICON, runtime(video['seconds']),
                   esc(video['title']), esc(video['caption'])))
        parts.append('</div></div>')
    parts.append('</section>')
    return ''.join(parts)


def detail_body(video, previous, following):
    covers = ''.join('<li>%s</li>' % esc(point) for point in video['covers'])
    track = ''
    if (SECTION / 'captions' / (video['slug'] + '.vtt')).exists():
        track = ('<track kind="captions" srclang="en" label="English" default '
                 'src="%scaptions/%s.vtt">' % (SECTION_URL, video['slug']))
    parts = [
        '<section id="section-video-explanations" class="video-detail" data-video-lesson '
        'data-reaction-key="ethcs303-%s" aria-labelledby="video-heading">' % video['slug'],
        '<div class="video-detail-head">',
        '<a class="video-back" href="%s" data-en-text="Back to Video Explanations" '
        'data-ar-text="العودة إلى شروحات الفيديو">Back to Video Explanations</a>' % SECTION_URL,
        '<h2 class="video-title section-label" id="video-heading" data-en-text="%s" data-ar-text="%s">%s</h2>'
        % (esc(video['title']), esc(video['title_ar']), esc(video['title'])),
        '<div class="video-meta"><span class="video-meta-tag">%s</span>'
        '<span>Runtime %s</span></div>' % (esc(video['group']), runtime(video['seconds'])),
        '</div>',
        '<div class="video-player">'
        '<video controls playsinline preload="none" poster="%s" src="%s/%s" aria-label="%s">%s'
        'Your browser does not support video playback.</video></div>'
        % (thumb_url(video), R2, video['video'], esc(video['title']), track),
        '<div class="video-underplayer">',
        '<p class="video-caption" data-en-text="%s" data-ar-text="%s">%s</p>'
        % (esc(video['caption']), esc(video['caption_ar']), esc(video['caption'])),
        REACTIONS,
        '</div>',
        '<div class="video-covers"><h3 data-en-text="IN THIS RECORDING" '
        'data-ar-text="في هذا التسجيل">IN THIS RECORDING</h3><ul>%s</ul></div>' % covers,
    ]
    if video.get('breakdown'):
        parts.append(
            '<a class="video-related" href="%s%s"><span>Slide breakdown</span>%s</a>'
            % (BREAKDOWNS, video['breakdown'], esc(BREAKDOWN_LABELS[video['breakdown']])))
    pager = []
    if previous:
        pager.append('<a class="pager-prev" rel="prev" href="%s">'
                     '<span class="pager-label">Previous</span>'
                     '<span class="pager-title">%s</span></a>'
                     % (page_url(previous), esc(previous['title'])))
    if following:
        pager.append('<a class="pager-next" rel="next" href="%s">'
                     '<span class="pager-label">Next</span>'
                     '<span class="pager-title">%s</span></a>'
                     % (page_url(following), esc(following['title'])))
    if pager:
        parts.append('<nav class="video-pager" aria-label="Video navigation">%s</nav>' % ''.join(pager))
    parts.append(DISCUSSION)
    parts.append('</section>')
    return ''.join(parts)


# --------------------------------------------------------------------------- #
# build
# --------------------------------------------------------------------------- #

def build_pages():
    template = chrome()
    ordered = sorted(VIDEOS, key=lambda v: [g[0] for g in GROUPS].index(v['group']))

    index = render(
        template,
        url=SECTION_URL,
        title=BASE_TITLE,
        description='Recorded ETHCS303 walkthroughs: ethical theories, professional ethics, '
                    'privacy in cyberspace, social engineering, intellectual property and Saudi cyber law.',
        crumb='<span class="current" data-en-text="Video Explanations" '
              'data-ar-text="شروحات الفيديو">Video Explanations</span>',
        body=index_body(),
    )
    index = keep_existing_nav(index, SECTION / 'index.html')
    (SECTION / 'index.html').write_text(index, encoding='utf-8')
    print('index: %s' % SECTION_URL)

    for position, video in enumerate(ordered):
        previous = ordered[position - 1] if position else None
        following = ordered[position + 1] if position + 1 < len(ordered) else None
        crumb = ('<a class="breadcrumb-link" href="%s" data-en-text="Video Explanations" '
                 'data-ar-text="شروحات الفيديو">Video Explanations</a> / '
                 '<span class="current">%s</span>' % (SECTION_URL, esc(video['title'])))
        page = render(
            template,
            url=page_url(video),
            title='SHOUG.TECH | ETHCS303 %s' % video['title'],
            description=video['caption'],
            crumb=crumb,
            body=detail_body(video, previous, following),
            image=SITE + thumb_url(video),
            scripts=LESSON_SCRIPT,
        )
        target = SECTION / video['slug'] / 'index.html'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(keep_existing_nav(page, target), encoding='utf-8')
        print('page:  %s' % page_url(video))


def sidebar_entries():
    """The JSON fragment for scripts/academic-sidebar.json."""
    ordered = sorted(VIDEOS, key=lambda v: [g[0] for g in GROUPS].index(v['group']))
    return [{'url': page_url(v), 'attrs': '', 'label': v['title']} for v in ordered]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--thumbnails', action='store_true', help='re-cut the poster frames')
    parser.add_argument('--source', type=Path,
                        default=Path.home() / 'Library/Mobile Documents/com~apple~CloudDocs/Ethics')
    parser.add_argument('--print-sidebar', action='store_true',
                        help='print the sidebar entries for academic-sidebar.json')
    args = parser.parse_args()
    if args.print_sidebar:
        print(json.dumps(sidebar_entries(), indent=2, ensure_ascii=False))
        return
    if args.thumbnails:
        build_thumbnails(args.source)
    build_pages()


if __name__ == '__main__':
    main()
