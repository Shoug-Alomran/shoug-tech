"""Shared display names and syllabus ordering; URLs remain stable."""
import re
CHAPTERS = [
 ('Introduction · Moral Systems & Ethical Concepts', 'مقدمة · الأنظمة والمفاهيم الأخلاقية'),
 ('Chapter 2 · Ethical Theories', 'الفصل الثاني · النظريات الأخلاقية'),
 ('Professional Ethics', 'الأخلاقيات المهنية'),
 ('Chapter 4 · Systems Analysis & Software Development', 'الفصل الرابع · تحليل النظم وتطوير البرمجيات'),
 ('Network Security & Privacy', 'أمن الشبكات والخصوصية'),
 ('Chapter 7 · Privacy in Cyberspace & Cloud Computing', 'الفصل السابع · الخصوصية في الفضاء السيبراني والحوسبة السحابية'),
 ('Chapter 8 · Social Media Ethics & Security', 'الفصل الثامن · أخلاقيات وأمن وسائل التواصل الاجتماعي'),
 ('Chapter 9 · Business Ethics', 'الفصل التاسع · أخلاقيات الأعمال'),
 ('Chapter 9 · Social Engineering', 'الفصل التاسع · الهندسة الاجتماعية'),
 ('Chapter 9 · Ethical Hacking', 'الفصل التاسع · الاختراق الأخلاقي'),
 ('Chapter 10 · Intellectual Property', 'الفصل العاشر · الملكية الفكرية'),
 ('Chapter 11 · Cyber Law in Saudi Arabia', 'الفصل الحادي عشر · القوانين السيبرانية في السعودية'),
 ('Course-wide Resources & Exam Preparation', 'مراجع المقرر والاستعداد للاختبارات'),
]

def chapter(path, title=''):
    value = (str(path) + ' ' + title).lower().replace('-', ' ')
    rules = [
      (9, ['ethical hacking']), (7, ['business ethics']),
      (6, ['social media']), (5, ['cloud', 'cyberspace', 'privacy policies']),
      (3, ['systems analysis', 'software engineering', 'ethical security issues', 'sa and sd']),
      (2, ['professional', 'acm', 'ieee', 'whistle']),
      (4, ['network security']),
      (8, ['social engineering', 'phishing', 'smishing', 'vishing', 'impersonation', 'dumpster', 'fraud']),
      (10, ['intellectual property', 'patent', 'trademark', 'trade secret', 'chapter 10']),
      (11, ['cyber law']),
      (1, ['kant', 'utilitarian', 'social contract', 'divine command', 'virtue ethics', 'ethical theories', 'moral theories']),
      (0, ['moral systems', 'introduction to ethics', 'ethical concepts']),
    ]
    if 'moral systems' in value: return 0
    for index, terms in rules:
        if any(term in value for term in terms): return index
    return 12

def clean_title(title):
    title = re.sub(r'\s+', ' ', title).strip()
    title = re.sub(r'^SHOUG\.TECH\s*\|\s*', '', title, flags=re.I)
    title = re.sub(r'^ETHCS\s*303\s*(?:[|:/—–-]+\s*)?', '', title, flags=re.I)
    title = re.sub(r'\s*[|—–]\s*(?:SHOUG\.TECH|ETHCS\s*303).*$', '', title, flags=re.I)
    title = re.sub(r'\s*[—–-]\s*New Explanation', '', title, flags=re.I)
    title = re.sub(r'\s*[-–—:]\s*Part\s*(\d+)', r' — Part \1', title, flags=re.I)
    return title.strip()

def sort_key(title):
    return [int(p) if p.isdigit() else p.lower() for p in re.split(r'(\d+)', title)]
