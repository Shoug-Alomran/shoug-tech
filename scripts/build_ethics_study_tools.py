#!/usr/bin/env python3
"""Build transcript-backed listening, transcript and chapter data for lessons."""
import importlib.util,json,re
from pathlib import Path
from urllib.parse import quote
from validate_video_captions import read_cues,seconds
ROOT=Path(__file__).resolve().parent.parent
s=importlib.util.spec_from_file_location('pages',ROOT/'scripts/build_ethics_video_pages.py')
p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
BASE='/academics/other-courses/ethcs303/'
# Chapter links point to an actual mention in the transcript, never an invented
# evenly spaced timestamp. These automatic topic markers can be curated later.
TOPICS=[
 ('Morality and ethics','Morality|morality|الأخلاق|الاخلاق'),('Moral systems','moral system|النظام الأخلاقي|النظام الاخلاقي'),
 ('Relativism','relativism|النسبية'),('Divine Command Theory','divine command|الأمر الإلهي|الامر الالهي'),
 ('Duties','deontolog|الواجب'),('Consequences','consequentialism|العواقب'),('Virtue ethics','virtue|الفضيلة'),
 ('Categorical imperative','categorical imperative|الأمر القطعي'),('Universalizability','universaliz|التعميم'),
 ('Utility and happiness','happiness|السعادة'),('Social contract','social contract|العقد الاجتماعي'),
 ('Responsibilities','responsibilit|مسؤول'),('Codes of ethics','code of ethics|مدونة الأخلاق|ميثاق أخلاقي'),
 ('Conflicts of interest','conflict of interest|تعارض المصالح'),('Reporting wrongdoing','whistleblow|الإبلاغ'),
 ('Privacy','privacy|الخصوصية'),('Personal information','personal information|personal data|المعلومات الشخصية|بيانات شخصية'),
 ('Consent','consent|الموافقة'),('Surveillance','surveillance|المراقبة'),
 ('Phishing','phishing|التصيد'),('Phone scams','vishing|احتيال هاتفي'),('Text-message scams','smishing|احتيال الرسائل'),
 ('Impersonation','impersonation|انتحال'),('Dumpster diving','dumpster|القمامة'),
 ('Intellectual property','intellectual property|الملكية الفكرية'),('Copyright','copyright|حقوق النشر'),
 ('Patents','patent|براءة|براءات'),('Trademarks','trademark|علامة تجارية|العلامات التجارية'),
 ('Trade secrets','trade secret|الأسرار التجارية|الاسرار التجارية'),
 ('Cybercrime','cybercrime|cyber crime|الجرائم السيبرانية|جرائم المعلوماتية'),('Penalties','penalt|عقوبة|عقوبات|السجن'),
 ('Example','example|مثال'),('Protection and prevention','prevent|protect|حماية|نحمي|نتجنب'),
 ('Comparison','compar|مقارنة|الفرق بين'),('Summary','summary|summar|خلاصة|الخلاصة')]


CURATED_CHAPTERS = {
    'social-contract-theory-new-explanation': [
        (0, 'Hobbes and social contracts'), (195.58, 'Implicit agreement'),
        (295.56, 'Social Contract Theory versus Kantianism'),
        (441.7, 'Negative and positive rights'), (519.74, 'Rawls and principles of justice'),
        (662.24, 'Income and fairness example'), (791.8, 'The veil of ignorance'),
        (823.8, 'The difference principle'), (936.24, 'Customer information example'),
        (1140.4, 'The language of rights'), (1270.44, 'Is the theory workable?'),
        (1390.2, 'Conflicting rights'),
    ],
    'virtue-ethics-new-explanation': [
        (0, 'Introduction to virtue ethics'), (87.96, 'Virtues and vices'),
        (204.16, 'The virtuous person'), (345.18, 'Moral decision-making'),
        (397.94, 'Workplace example'), (525.38, 'Intellectual and moral virtues'),
        (586.94, 'Developing virtues through habit'), (694.34, 'Character and emotions'),
        (745.04, 'Courage and fear'), (829.82, 'Vices and the mean'),
        (914.24, 'Arguments for virtue ethics'),
    ],
    'utilitarianism-part-2': [
        (0, 'Rule utilitarianism'), (62.54, 'Evaluating a rule'),
        (155.32, 'Contrast with act utilitarianism'), (165.44, 'Classroom example'),
        (225.76, 'Rules and collective happiness'), (346.3, 'Rule utilitarianism versus Kantianism'),
    ],
    'moral-systems-and-ethical-theories': [
        (0, 'Morality and ethics'), (206.74, 'Justifying moral rules'),
        (411.52, 'Four features of moral systems'), (525.62, 'Autonomy and justice'),
        (1012.3, 'Criticisms of subjective relativism'), (1049.68, 'Criticisms of cultural relativism'),
        (1363.32, 'Consequentialism'), (1448.92, 'The greatest good'), (1939.4, 'Lesson review'),
    ],
    'professional-ethics': [
        (0, 'Professional relationships'), (158.84, 'Employer and employee'),
        (395.62, 'Clients and professionals'), (718.86, 'Obligations to society'),
        (1075.34, 'Whistleblowing'), (1149.22, 'Internal and external reporting'),
        (1455.58, 'Types of whistleblowers'), (1675.76, 'Corporate responses'),
        (1906.06, 'Protecting internal reporting'), (2129.52, 'Moral responsibility'),
        (2441.72, 'Codes of ethics'), (2615.86, 'Limits of ethical codes'), (2865.76, 'ACM code of ethics'),
    ],
    'ethical-issues-in-systems-analysis-and-software-engineering': [
        (0, 'Systems analysis and software engineering'), (314.9, 'Incomplete requirements'),
        (450.3, 'Quality and time-to-market pressure'), (514.98, 'Intellectual property'),
        (660.72, 'Incompetent staff'), (1102.52, 'Safety-critical systems'),
        (1188.16, 'Testing'), (1508.02, 'N-version programming'),
        (1648.1, 'Quality assurance example'), (1751.64, 'System administrators'),
        (1831.84, 'Six ethical issues'), (2321.86, 'LOPSA code of ethics'),
    ],
    'privacy-in-cyberspace-part-1': [
        (0, 'Privacy in cyberspace'), (170.54, 'Information privacy'), (193.46, 'Privacy as a social value'),
        (216.46, 'Categories of private information'), (345.42, 'Questions about data collection'),
        (443.56, 'Cloud storage and location'), (492.26, 'How long information is kept'),
        (577.26, 'Electronic profiles'),
    ],
    'privacy-in-cyberspace-part-2': [
        (0, 'Data collection'), (204.52, 'Surveillance drones'), (333.14, 'Internet cookies'),
        (390.34, 'First-party cookies'), (431.64, 'Third-party and tracking cookies'),
        (479.74, 'Flash cookies'), (612.4, 'Privacy concerns with cookies'),
        (858.42, 'Fingerprinting'), (1120.74, 'RFID technology'), (1378.32, 'Tracking technology'),
    ],
    'intellectual-property-laws': [
        (0, 'Types of intellectual property'), (129.06, 'Protecting intellectual works'),
        (207.6, 'Copyright and creative works'), (333.22, 'Automatic copyright protection'),
        (423.52, 'Copyright owner rights'), (577.02, 'Saudi copyright law'),
        (642.04, 'Copyright infringement'), (741.36, 'Fair use'),
        (934.98, 'Software protection'), (1148.2, 'Digital rights management'),
        (1300.9, 'Plagiarism and infringement'), (1447.42, 'Tetris example'), (1588.46, 'Sharing versus selling'),
    ],
    'patents-and-trademarks': [
        (0, 'Patents'), (174.2, 'What cannot be patented'), (208.24, 'Patent costs and rights'),
        (260.86, 'Software patents'), (632.92, 'Patent infringement'),
        (812.98, 'Types of infringement'), (906.48, 'Penalties'),
        (1042.4, 'Mobile-phone patent agreements'), (1083.72, 'Trademarks'),
        (1212.12, 'Trade dress'), (1265.48, 'Registration and protection'),
    ],
    'trade-secrets': [
        (0, 'What is a trade secret?'), (141.22, 'Requirements for protection'),
        (250.5, 'Non-disclosure agreements'), (441.44, 'Advantages over patents and copyright'),
        (522.6, 'Saudi intellectual property authority'), (645.08, 'Plagiarism'),
        (812.06, 'Competitive intelligence'), (943.34, 'Sources of competitive information'),
        (1237.872, 'Cybersquatting'), (1517.18, 'Cybersquatting example'),
        (1709.64, 'Anti-cybersquatting protections'), (1774.16, 'Reverse engineering'),
    ],
    'cyber-laws-in-saudi-arabia': [
        (0, 'Introduction to cyber law'), (130.94, 'Cybercrime and other crime'),
        (175.82, 'Crimes against individuals'), (414.02, 'Property and intellectual property crimes'),
        (685.78, 'Data diddling'), (1080.48, 'Saudi anti-cybercrime law'),
        (1220.82, 'Article 3'), (1350, 'Article 4'), (1467.92, 'Article 5'), (1508.8, 'Article 6'),
    ],
    'kantianism': [
        (0, 'Introduction'), (194.66, 'Reason and good will'), (358.96, 'Universalizability'),
        (504.02, 'Categorical imperatives'), (650.02, 'Treating people as ends'),
        (731.2, 'Perfect and imperfect duties'), (908.08, 'Conflicting duties'),
        (1001.82, 'Worked cases'), (1199.6, 'The murderer-at-the-door example'),
    ],
    'utilitarianism': [
        (0, 'Utility and happiness'), (158.8, 'The greatest happiness principle'),
        (289.3, 'Act and rule utilitarianism'), (494.56, 'Highway cost-benefit example'),
        (575.98, 'Limits of utility calculations'), (620.04, 'Difficulties with act utilitarianism'),
        (725.7, 'Applying rule utilitarianism'), (988.92, 'Rule utilitarianism versus Kantianism'),
    ],
    'social-contract-theory': [
        (0, 'Hobbes and social contracts'), (60.6, 'Life without a social contract'),
        (140.4, 'How the social contract arises'), (182.04, 'Traffic-light example'),
        (275, 'Implicit agreement'), (439.64, 'Negative and positive rights'),
        (575.46, 'Rawls and principles of justice'), (921.94, 'Confidentiality and rights'),
        (1030.2, 'Conflicting rights'), (1287.02, 'The hypothetical contract'),
    ],
    'utilitarianism-part-1': [
        (0, 'Consequences and utility'), (84.64, 'Happiness and its synonyms'),
        (132.78, 'The greatest happiness principle'), (316.84, 'Act and rule utilitarianism'),
        (375.96, 'Medical triage example'), (587, 'Highway cost-benefit example'),
        (721.3, 'Arguments for utilitarianism'),
    ],
    'social-engineering': [
        (0, 'Introduction'), (17.72, 'What is social engineering?'),
        (65.92, 'What attackers seek'), (126, 'Why social engineering works'),
        (174.32, 'Identity theft and other risks'), (287.1, 'Benefits of awareness'),
    ],
    'phishing': [
        (0, 'Introduction'), (20.92, 'What is phishing?'), (116.14, 'Fake links'),
        (153.14, 'Spear phishing'), (192.14, 'Whaling'), (227.14, 'Email phishing'),
        (309.14, 'Urgent requests for help'), (355.14, 'Worked example'),
    ],
    'vishing': [
        (0, 'Voice phishing'), (48, 'Caller ID spoofing'), (73, 'Why help desks are targeted'),
        (174, 'Protecting yourself'), (208, 'Sensitive information on calls'),
        (232, 'Caller ID apps and their limits'),
    ],
    'smishing': [
        (0, 'What is smishing?'), (58.6, 'Fear and greed'), (93.56, 'How numbers are obtained'),
        (140.84, 'Messages, calls and links'), (184.12, 'Prize scam example'),
        (240.84, 'Mobile banking and convincing messages'), (295.48, 'Simulated attacks and training'),
    ],
    'impersonation': [
        (0, 'What is impersonation?'), (47.44, 'Delivery person impersonation'),
        (156.32, 'Tech support impersonation'), (201.34, 'Tech support example'),
    ],
    'avoiding-social-engineering-fraud': [
        (0, 'Secure your devices'), (39, 'Spam filters'), (93, 'Downloads and sensitive requests'),
        (117, 'Slow down under pressure'), (166, 'Research the facts'),
        (203, 'Unexpected offers of help'), (367, 'Fake offers'), (437, 'Device security and updates'),
    ],
    'moral-systems-and-ethical-theories-part-1': [
        (0, 'Introduction'), (16, 'Morality'), (120.4, 'Ethics and morality'),
        (452, 'Four features of a moral system'),
        (672.04, 'Deriving and justifying moral principles'), (958.02, 'Comparing ethical theories'),
    ],
    'moral-systems-and-ethical-theories-part-2': [
        (0, 'What ethical theories share'), (58.9, 'Obligations and personal choice'),
        (114.02, 'Beneficence'), (155.12, 'Least harm'), (248.92, 'Respect for autonomy'),
        (329.22, 'Justice'), (358.26, 'Theories covered next'),
    ],
    'moral-systems-and-ethical-theories-part-3': [
        (0, 'Ethical relativism'), (172.02, 'Subjective relativism'),
        (316.86, 'Criticisms of subjective relativism'), (479.78, 'Cultural relativism'),
        (713.22, 'Personal moral codes and bias'), (826.38, 'Is cultural relativism workable?'),
        (924.78, 'Comparing the two forms'),
    ],
    'divine-command-theory-new-explanation': [
        (0, 'Divine Command Theory'), (57.34, 'Moral and immoral actions'),
        (157.96, 'Punishment and reward'), (218.14, 'Universal moral rules'),
        (304.94, 'Objectivity'), (370.62, 'Is the theory workable?'),
    ],
    'kantianism-part-1': [
        (0, 'Kantianism'), (91.38, 'Universal moral laws'), (290.24, 'Good will'),
        (456.42, 'Acting from duty'), (525.68, 'Testing universalizability'),
        (620.1, 'Categorical imperatives'),
    ],
    'kantianism-part-2': [
        (0, 'Applying universalizability'), (194.78, 'The categorical imperative'),
        (445.74, 'Self-defeating rules'), (487.76, 'Perfect and imperfect duties'),
        (525.76, 'Perfect duties'), (633.58, 'Imperfect duties'), (737.38, 'Comparing duties'),
    ],
    'kantianism-part-3': [
        (0, 'Arguments for Kantianism'), (57.78, 'Is Kantianism workable?'),
        (105.18, 'Moral obligations'), (184.3, 'Conflicts between duties'),
        (222.3, 'No exceptions to perfect duties'),
    ],
    'professional-ethics-part-1': [
        (0, 'Professional relationships'), (50.32, 'Employer and employee'),
        (190.92, 'Confidentiality and non-compete clauses'),
        (249.22, 'Clients and professionals'), (432.46, 'Society and professionals'),
        (627.02, 'Obligations to other professionals'),
    ],
    'professional-ethics-part-2': [
        (0, 'Whistleblowing'), (143.5, 'Internal and external whistleblowing'),
        (238.9, 'Organizational culture'), (312.08, 'Motives and morality'),
        (380.96, 'Types of whistleblowers'), (519.341, 'Company responses'),
        (749.7, 'Ethical values in organizations'), (839.5, 'Evaluating the means and ends'),
    ],
    'professional-ethics-part-3': [
        (0, 'Moral responsibility'), (45.544, 'Role responsibility'),
        (66.22, 'Causal responsibility'), (160.42, 'Legal responsibility'),
        (174.98, 'How responsibilities overlap'), (362.22, 'Professional codes of ethics'),
        (564.92, 'Why codes of ethics matter'), (841.86, 'Limits of ethical codes'),
        (961.58, 'Functions of a code of ethics'), (1185.26, 'Examples of professional codes'),
    ],
    'dumpster-diving': [
        (0, 'Introduction'), (28.24, 'What is dumpster diving?'),
        (64.48, 'Organizational charts'), (110.48, 'Memos and authenticity'),
        (128.48, 'Policy manuals'), (154.48, 'Calendars'),
        (173.48, 'System manuals'), (202.48, 'Discarded hardware'),
    ],
}

def chapters(cues, slug):
    if slug in CURATED_CHAPTERS:
        return [{'time':t,'title':title} for t,title in CURATED_CHAPTERS[slug]]
    result=[{'time':0,'title':'Introduction'}];used=set()
    for start,end,text in cues:
        t=seconds(start)
        if t < result[-1]['time']+60:continue
        for title,pattern in TOPICS:
            if title not in used and re.search(pattern,text,re.I):
                result.append({'time':t,'title':title});used.add(title);break
        if len(result)>=10:break
    return result


def main():
    lessons=[];routes={}
    for v in p.VIDEOS:
        if not (p.SECTION/v['slug']/'index.html').exists():continue
        f=p.SECTION/'captions'/(v['slug']+'.vtt')
        if not f.exists():continue
        _,cues=read_cues(f)
        data={'id':v['slug'],'title':v['title'],'url':p.R2+'/'+quote(v['video'],safe='/'),
              'page':p.SECTION_URL+v['slug']+'/', 'caption':p.SECTION_URL+'captions/'+v['slug']+'.vtt',
              'chapters':chapters(cues,v['slug']),'transcript':[{'start':seconds(a),'end':seconds(b),'text':t} for a,b,t in cues]}
        detail_dir=p.SECTION/'lesson-data'
        detail_dir.mkdir(exist_ok=True)
        (detail_dir/(v['slug']+'.json')).write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')))
        lessons.append({k:value for k,value in data.items() if k!='transcript'})
        bd=v.get('breakdown')
        if bd:
            route=BASE+'slide-breakdowns/'+bd
            routes.setdefault(route,[]).append(v['slug'])
            slide=re.sub(r'^\d+-','',bd)
            if slide=='intellectual-property-laws/':pass
            route=BASE+'slides/'+slide
            if (ROOT/'docs'/route.strip('/')/'index.html').exists():routes.setdefault(route,[]).append(v['slug'])
    out=ROOT/'docs/academics/other-courses/ethcs303/video-explanations/study-tools.json'
    out.write_text(json.dumps({'lessons':lessons,'routes':routes},ensure_ascii=False,separators=(',',':')))
    assets='<link rel="stylesheet" href="/styles/ethics-study-tools.css">\n<script src="/javascripts/ethics-study-tools.js" defer></script>\n'
    paths={p.SECTION/v['slug']/'index.html' for v in p.VIDEOS}
    for route in routes:
        directory=ROOT/'docs'/route.strip('/')
        paths.update(directory.glob('*.html'))
    for path in paths:
        if not path.exists():continue
        text=path.read_text()
        if '/javascripts/ethics-study-tools.js' not in text:path.write_text(text.replace('</body>',assets+'</body>'))
    print('Prepared study tools for',len(lessons),'videos and',len(routes),'slide/breakdown routes.')

if __name__=='__main__':main()
