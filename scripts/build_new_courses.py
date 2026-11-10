#!/usr/bin/env python3
"""Build CS311, IS321 and ECON101 from CS340's page shells, and the Information Systems section.

Moves each uploaded deck to slides/<slug>/<slug>.pdf, then writes the overview,
the slides listing and one viewer per deck, and registers each course on the
hubs, in the sidebar and in the course routes. Safe to re-run. Edit COURSES
here, not the generated HTML.

    .venv/bin/python scripts/build_new_courses.py
"""
import html
import json
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_academic_sidebar import DATA_FILE, NAV_RE, render_nav  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, "docs")
SLIDE_INDEX = os.path.join(REPO, "scripts", "course-slide-index.json")
TEMPLATE_DIR = os.path.join(DOCS, "academics/computer-science/cs340")
TEMPLATE_DECK = "chapter-1-introduction-to-databases"
TEMPLATE_DECK_TITLE = "Chapter 1 Introduction To Databases"
TEMPLATE_NAME = "Introduction to Database Systems"

IS_HUB = "/academics/information-system/"
IS_GROUP = "tree-information-systems"
IS_LABEL = "INFORMATION SYSTEMS/"

SECTIONS = {
    "computer-science": ("Computer Science", "علوم الحاسب"),
    "information-system": ("Information Systems", "نظم المعلومات"),
    "other-courses": ("Other Courses", "مواد أخرى"),
}

EXAM_PAGE_COUNTS = {
    "CS311": [
        ("Major Exam I — Lectures 1–4", "الاختبار الفصلي الأول — المحاضرات 1–4",
         [("L1", "Algorithm Analysis and Asymptotic Notation", "lecture-1-algorithm-analysis-and-asymptotic-notation", 66),
          ("L2", "Analysis of Algorithms", "lecture-2-analysis-of-algorithms", 27),
          ("L3", "Recurrences", "lecture-3-recurrences", 35),
          ("L4", "Divide and Conquer", "lecture-4-divide-and-conquer", 34)], 162),
        ("Major Exam II — Lectures 5–NP", "الاختبار الفصلي الثاني — المحاضرات 5–NP",
         [("L5.1", "Greedy Algorithms", "lecture-5-1-greedy-algorithms", 24),
          ("L5.2", "Dijkstra's Algorithm", "lecture-5-2-dijkstras-algorithm", 20),
          ("L5.3", "Minimum Spanning Tree", "lecture-5-3-minimum-spanning-tree", 43),
          ("L6", "Dynamic Programming", "lecture-6-dynamic-programming", 83),
          ("T7", "Graph and Search Algorithms", "topic-7-graph-and-search-algorithms", 68),
          ("BT", "Backtracking and Branch and Bound", "backtracking-and-branch-and-bound", 43),
          ("RAND", "Randomized Algorithms", "randomized-algorithms", 27),
          ("NP", "Complexity Classes: P, NP, NP-Complete and NP-Hard", "complexity-classes-p-np-np-complete-and-np-hard", 41)], 349),
    ],
    "IS321": [
        ("Quiz I — Lectures 1–5", "الاختبار القصير الأول — المحاضرات 1–5",
         [("L1", "Enterprise Architecture Introduction, Purpose and Elements", "lecture-1-enterprise-architecture-introduction", 26),
          ("L2", "EA as an Analysis and Design Method", "lecture-2-ea-as-an-analysis-and-design-method", 31),
          ("L3", "The EA Approach: Core Components", "lecture-3-the-ea-approach-core-components", 18),
          ("L4", "EA as a Management Program", "lecture-4-ea-as-a-management-program", 12),
          ("L5", "The EA Repository", "lecture-5-the-ea-repository", 10)], 97),
        ("Quiz II — Lectures 6–8", "الاختبار القصير الثاني — المحاضرات 6–8",
         [("L6", "EA Value and Risk", "lecture-6-ea-value-and-risk", 18),
          ("L7", "Models of Organizations and Enterprises", "lecture-7-models-of-organizations-and-enterprises", 30),
          ("L8", "Business Continuity Planning", "lecture-8-business-continuity-planning", 18)], 66),
        ("Major Exam — Lectures 1–10", "الاختبار الفصلي — المحاضرات 1–10",
         [("L1", "Enterprise Architecture Introduction, Purpose and Elements", "lecture-1-enterprise-architecture-introduction", 26),
          ("L2", "EA as an Analysis and Design Method", "lecture-2-ea-as-an-analysis-and-design-method", 31),
          ("L3", "The EA Approach: Core Components", "lecture-3-the-ea-approach-core-components", 18),
          ("L4", "EA as a Management Program", "lecture-4-ea-as-a-management-program", 12),
          ("L5", "The EA Repository", "lecture-5-the-ea-repository", 10),
          ("L6", "EA Value and Risk", "lecture-6-ea-value-and-risk", 18),
          ("L7", "Models of Organizations and Enterprises", "lecture-7-models-of-organizations-and-enterprises", 30),
          ("L8", "Business Continuity Planning", "lecture-8-business-continuity-planning", 18),
          ("L9", "Linking Strategy, Business and Technology", "lecture-9-linking-strategy-business-and-technology", 11),
          ("L10", "EA Technology Planning and Intelligent Enterprise Systems", "lecture-10-ea-technology-planning-and-intelligent-systems", 18)], 192),
        ("Final Exam — Comprehensive Lectures 1–14", "الاختبار النهائي — شامل المحاضرات 1–14",
         [("L1", "Enterprise Architecture Introduction, Purpose and Elements", "lecture-1-enterprise-architecture-introduction", 26),
          ("L2", "EA as an Analysis and Design Method", "lecture-2-ea-as-an-analysis-and-design-method", 31),
          ("L3", "The EA Approach: Core Components", "lecture-3-the-ea-approach-core-components", 18),
          ("L4", "EA as a Management Program", "lecture-4-ea-as-a-management-program", 12),
          ("L5", "The EA Repository", "lecture-5-the-ea-repository", 10),
          ("L6", "EA Value and Risk", "lecture-6-ea-value-and-risk", 18),
          ("L7", "Models of Organizations and Enterprises", "lecture-7-models-of-organizations-and-enterprises", 30),
          ("L8", "Business Continuity Planning", "lecture-8-business-continuity-planning", 18),
          ("L9", "Linking Strategy, Business and Technology", "lecture-9-linking-strategy-business-and-technology", 11),
          ("L10", "EA Technology Planning and Intelligent Enterprise Systems", "lecture-10-ea-technology-planning-and-intelligent-systems", 18),
          ("L11", "The Most Significant EA Frameworks", "lecture-11-the-most-significant-ea-frameworks", 14),
          ("L12", "TOGAF and the Architecture Development Method", "lecture-12-togaf-and-the-architecture-development-method", 38),
          ("L13", "The EA3 Cube Framework", "lecture-13-the-ea3-cube-framework", 18),
          ("L14", "AI in Modern Enterprise Architecture", "lecture-14-ai-in-modern-enterprise-architecture", 12)], 274),
    ],
    "ECON101": [
        ("Quiz I — Chapters 1–2", "الاختبار القصير الأول — الفصلان 1–2",
         [("CH 1", "What Is Economics?", "chapter-1-what-is-economics", 90),
          ("CH 2", "The Economic Problem", "chapter-2-the-economic-problem", 72)], 162),
        ("Major I — Chapters 2–4", "الاختبار الفصلي الأول — الفصول 2–4",
         [("CH 2", "The Economic Problem", "chapter-2-the-economic-problem", 72),
          ("CH 3", "Demand and Supply", "chapter-3-demand-and-supply", 52),
          ("CH 4", "Elasticity", "chapter-4-elasticity", 55)], 179),
        ("Quiz II — Chapters 5–6", "الاختبار القصير الثاني — الفصلان 5–6",
         [("CH 5", "Efficiency and Equity", "chapter-5-efficiency-and-equity", 56),
          ("CH 6", "Government Actions in Markets", "chapter-6-government-actions-in-markets", 33)], 89),
        ("Major II — Chapters 6, 8–9", "الاختبار الفصلي الثاني — الفصول 6 و8–9",
         [("CH 6", "Government Actions in Markets", "chapter-6-government-actions-in-markets", 33),
          ("CH 8", "Utility and Demand", "chapter-8-utility-and-demand", 30),
          ("CH 9", "Possibilities, Preferences and Choices",
           "chapter-9-possibilities-preferences-and-choices", 25)], 88),
        ("Final Exam — Comprehensive", "الاختبار النهائي — شامل",
         [("CH 1", "What Is Economics?", "chapter-1-what-is-economics", 90),
          ("CH 2", "The Economic Problem", "chapter-2-the-economic-problem", 72),
          ("CH 3", "Demand and Supply", "chapter-3-demand-and-supply", 52),
          ("CH 4", "Elasticity", "chapter-4-elasticity", 55),
          ("CH 5", "Efficiency and Equity", "chapter-5-efficiency-and-equity", 56),
          ("CH 6", "Government Actions in Markets", "chapter-6-government-actions-in-markets", 33),
          ("CH 8", "Utility and Demand", "chapter-8-utility-and-demand", 30),
          ("CH 9", "Possibilities, Preferences and Choices",
           "chapter-9-possibilities-preferences-and-choices", 25),
          ("CH 11", "Output and Costs", "chapter-11-output-and-costs", 33),
          ("CH 12", "Perfect Competition", "chapter-12-perfect-competition", 24),
          ("CH 13", "Monopoly", "chapter-13-monopoly", 19),
          ("CH 14", "Monopolistic Competition", "chapter-14-monopolistic-competition", 14)], 503),
    ],
}

EXAM_COUNT_CSS = '''      .exam-count-group { margin-bottom: 24px; }
          .exam-count-heading {
            display: flex;
            justify-content: space-between;
            gap: 16px;
            margin-bottom: 8px;
            font-family: var(--font-mono);
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.08em;
            color: var(--brand-purple);
            text-transform: uppercase;
          }
          .exam-count-total { color: var(--text-main); }
          .topic-item.exam-total { background-color: var(--bg-surface); font-weight: 700; }
          .topic-item.exam-total .topic-meta { color: var(--brand-purple); }
          .exam-scope-note {
            margin: -8px 0 24px;
            padding: 12px 16px;
            border-left: 2px solid var(--brand-purple);
            background-color: var(--bg-elevated);
            color: var(--text-dim);
            font-family: var(--font-mono);
            font-size: 12px;
            line-height: 1.6;
          }
    '''

COURSES = [
    {
        "code": "CS311",
        "url": "/academics/computer-science/cs311/",
        "section": "computer-science",
        "name": "Design and Analysis of Algorithms",
        "name_ar": "تصميم وتحليل الخوارزميات",
        "prereqs": "CS210, CS285",
        "prereqs_ar": "CS210، CS285",
        "file_id": "261-ALGO",
        "syllabus": True,
        "description": (
            "CS311 covers the fundamental techniques for designing and analyzing algorithms: "
            "asymptotic analysis, recurrences, divide and conquer, greedy algorithms, dynamic "
            "programming, graph algorithms, backtracking, branch and bound, randomized "
            "algorithms, and the complexity classes P, NP, NP-Complete and NP-Hard."
        ),
        "description_ar": (
            "يغطي مقرر CS311 الأساليب الأساسية لتصميم الخوارزميات وتحليلها: التحليل التقاربي، "
            "والعلاقات التكرارية، وفرق تسد، والخوارزميات الجشعة، والبرمجة الديناميكية، وخوارزميات "
            "الرسوم البيانية، والتراجع، والتفرع والتقييد، والخوارزميات العشوائية، وفئات التعقيد "
            "P وNP وNP-Complete وNP-Hard."
        ),
        "outcomes": [
            ("Describe time and space complexity and worst, average and best-case complexity with different notations.",
             "وصف تعقيد الزمن والمساحة وحالات التعقيد الأسوأ والمتوسطة والأفضل باستخدام الترميزات المختلفة."),
            ("Apply important algorithm design paradigms and methods of analysis.",
             "تطبيق أهم أنماط تصميم الخوارزميات وطرق تحليلها."),
            ("Analyze the performance of different algorithms.", "تحليل أداء الخوارزميات المختلفة."),
            ("Compare problems that can be solved by polynomial time algorithms.",
             "المقارنة بين المسائل التي يمكن حلها بخوارزميات زمنها كثير حدود."),
            ("Design an efficient algorithm for a particular task.", "تصميم خوارزمية فعالة لمهمة محددة."),
        ],
        "weights": [
            ("Quizzes", "الاختبارات القصيرة", "10%"),
            ("Major Exams (2)", "الاختبارات الفصلية (2)", "30%"),
            ("Assignments and Class Participation", "الواجبات والمشاركة الصفية", "10%"),
            ("Project", "المشروع", "10%"),
            ("Final Exam", "الاختبار النهائي", "40%"),
        ],
        "after": "CS316",
        # (original upload, slug, title, Arabic title, overview number label; "" keeps a copy off the overview)
        "decks": [
            ("CS311_Lecture 1.pdf", "lecture-1-algorithm-analysis-and-asymptotic-notation",
             "Lecture 1 - Algorithm Analysis and Asymptotic Notation",
             "المحاضرة 1 - تحليل الخوارزميات والترميز التقاربي", "L1"),
            ("CS311_Lecture 1_c147b4948c5aa71af7c01ccebd4bcfca.pdf",
             "lecture-1-algorithm-analysis-and-asymptotic-notation-second-copy",
             "Lecture 1 - Algorithm Analysis and Asymptotic Notation (Second Annotated Copy)",
             "المحاضرة 1 - تحليل الخوارزميات والترميز التقاربي (نسخة مشروحة ثانية)", ""),
            ("Asym excercise_011f6938e2a8cfcd6a18287423d0822c.pdf", "asymptotic-notation-practice",
             "Asymptotic Notation Practice", "تمارين الترميز التقاربي", "EX 1"),
            ("CS311_Lecture 2_a9b546657c09f4032867d8cf13ed3f47.pdf", "lecture-2-analysis-of-algorithms",
             "Lecture 2 - Analysis of Algorithms", "المحاضرة 2 - تحليل الخوارزميات", "L2"),
            ("Lecture 2-Execution Time Exercise_8e04fb231d27a247c0f283d66a2591ce.pdf",
             "lecture-2-execution-time-exercises", "Lecture 2 - Execution Time Exercises",
             "المحاضرة 2 - تمارين زمن التنفيذ", "EX 2"),
            ("Lecture 3_Reccurences Relation_4f6fee889f1d254deb2dfc04cc30a405.pdf", "lecture-3-recurrences",
             "Lecture 3 - Recurrences", "المحاضرة 3 - العلاقات التكرارية", "L3"),
            ("CS311_Lecture 4-DivideConquer_9f9bd0b66b1f787386f688777ee95557.pdf",
             "lecture-4-divide-and-conquer", "Lecture 4 - Divide and Conquer",
             "المحاضرة 4 - فرق تسد", "L4"),
            ("CS311_Lecture 5 part 1-GreedyAlgo_225aa68a1bbc57448e87e371794e5e22.pdf",
             "lecture-5-1-greedy-algorithms", "Lecture 5.1 - Greedy Algorithms",
             "المحاضرة 5.1 - الخوارزميات الجشعة", "L5.1"),
            ("CS311_Lecture 5 part 2-Dijkstra algorithm_f6970c39f0f9fd5d7aa42392a4674b60.pdf",
             "lecture-5-2-dijkstras-algorithm", "Lecture 5.2 - Dijkstra's Algorithm",
             "المحاضرة 5.2 - خوارزمية ديكسترا", "L5.2"),
            ("CS311_Lecture 5 part 3-MST_7e6403fae13c9d42abb489cba0fa0616.pdf",
             "lecture-5-3-minimum-spanning-tree", "Lecture 5.3 - Minimum Spanning Tree",
             "المحاضرة 5.3 - الشجرة الممتدة الصغرى", "L5.3"),
            ("Lecture 6 Dynamic Programming_a9eebce5595bf52a7c4841d2b6033982.pdf",
             "lecture-6-dynamic-programming", "Lecture 6 - Dynamic Programming",
             "المحاضرة 6 - البرمجة الديناميكية", "L6"),
            ("Topic 7_GraphSearchAlgorithms_73844ceb4ddb3905fbf5bea5adefc4da.pdf",
             "topic-7-graph-and-search-algorithms", "Topic 7 - Graph and Search Algorithms",
             "الموضوع 7 - خوارزميات الرسوم البيانية والبحث", "T7"),
            ("Chap6-BacktrackingBB.pdf", "backtracking-and-branch-and-bound",
             "Backtracking and Branch and Bound", "التراجع والتفرع والتقييد", "BT"),
            ("Chap6-BacktrackingBB_d934b178501ab1c0486fc496ebed43ea.pdf",
             "backtracking-and-branch-and-bound-second-copy",
             "Backtracking and Branch and Bound (Second Annotated Copy)",
             "التراجع والتفرع والتقييد (نسخة مشروحة ثانية)", ""),
            ("Randomized-algorithms_9f9c2f658244fe69d5f7f8d3b7bff0b4.pdf", "randomized-algorithms",
             "Randomized Algorithms", "الخوارزميات العشوائية", "RAND"),
            ("ProblemsClassComplexity_03ff706f7b37d65773928532ca50393f.pdf",
             "complexity-classes-p-np-np-complete-and-np-hard",
             "Complexity Classes - P, NP, NP-Complete and NP-Hard",
             "فئات التعقيد - P وNP وNP-Complete وNP-Hard", "NP"),
        ],
    },
    {
        "code": "IS321",
        "url": "/academics/information-system/is321/",
        "section": "information-system",
        "name": "Enterprise Architecture",
        "name_ar": "معمارية المؤسسات",
        "prereqs": "IS205",
        "prereqs_ar": "IS205",
        "file_id": "261-EA",
        "syllabus": True,
        "description": (
            "IS321 explores the design, selection, implementation and management of enterprise "
            "architecture solutions that meet business requirements: EA as a management program, "
            "the EA repository, value and risk, organizational models, business continuity, "
            "linking EA to strategy and technology, the Zachman, TOGAF and EA3 Cube frameworks, "
            "and AI in modern enterprise architecture."
        ),
        "description_ar": (
            "يستكشف مقرر IS321 تصميم حلول معمارية المؤسسات واختيارها وتنفيذها وإدارتها لتلبية "
            "متطلبات الأعمال: معمارية المؤسسات كبرنامج إداري، ومستودع المعمارية، والقيمة والمخاطر، "
            "والنماذج التنظيمية، واستمرارية الأعمال، وربط المعمارية بالاستراتيجية والتقنية، وأطر "
            "Zachman وTOGAF وEA3 Cube، والذكاء الاصطناعي في معمارية المؤسسات الحديثة."
        ),
        "outcomes": [
            ("Describe the core concepts of enterprise architecture and related models.",
             "وصف المفاهيم الأساسية لمعمارية المؤسسات والنماذج المرتبطة بها."),
            ("Evaluate organizational structural and security issues.", "تقييم القضايا الهيكلية والأمنية في المنظمات."),
            ("Demonstrate a suitable solution within an organizational context.", "عرض حل مناسب ضمن سياق تنظيمي."),
            ("Design EA solutions with business continuity taken into consideration.",
             "تصميم حلول معمارية المؤسسات مع مراعاة استمرارية الأعمال."),
            ("Demonstrate EA to integrate strategy, business and technology.",
             "توظيف معمارية المؤسسات لدمج الاستراتيجية والأعمال والتقنية."),
            ("Explain the benefits and risks of enterprise architecture.", "شرح فوائد معمارية المؤسسات ومخاطرها."),
        ],
        "weights": [
            ("Quiz I", "الاختبار القصير الأول", "5%"),
            ("Quiz II", "الاختبار القصير الثاني", "5%"),
            ("Assignments and Tutorials", "الواجبات والتطبيقات", "10%"),
            ("Attendance", "الحضور", "5%"),
            ("Project", "المشروع", "15%"),
            ("Major Exam", "الاختبار الفصلي", "20%"),
            ("Final Exam", "الاختبار النهائي", "40%"),
        ],
        "decks": [
            ("Lecture 1/Lecture 1 Chap001-EA-Part1.pdf", "lecture-1-enterprise-architecture-introduction",
             "Lecture 1 - Enterprise Architecture Introduction, Purpose and Elements",
             "المحاضرة 1 - مقدمة في معمارية المؤسسات وأهدافها وعناصرها", "L1"),
            ("Lecture 2/Lecture 2 Chap001-EA-Part2 (2).pdf", "lecture-2-ea-as-an-analysis-and-design-method",
             "Lecture 2 - EA as an Analysis and Design Method",
             "المحاضرة 2 - معمارية المؤسسات كأسلوب للتحليل والتصميم", "L2"),
            ("Lecture 3/IS321_Lecture 3.pdf", "lecture-3-the-ea-approach-core-components",
             "Lecture 3 - The EA Approach: Core Components", "المحاضرة 3 - منهج معمارية المؤسسات: المكونات الأساسية", "L3"),
            ("Lecture 4 /IS321_Lecture 4.pdf", "lecture-4-ea-as-a-management-program",
             "Lecture 4 - EA as a Management Program", "المحاضرة 4 - معمارية المؤسسات كبرنامج إداري", "L4"),
            ("Lecture 5/IS321_Lecture5.pdf", "lecture-5-the-ea-repository",
             "Lecture 5 - The EA Repository", "المحاضرة 5 - مستودع معمارية المؤسسات", "L5"),
            ("Lecture 6/IS321_Lecture 6.pdf", "lecture-6-ea-value-and-risk",
             "Lecture 6 - EA Value and Risk", "المحاضرة 6 - قيمة معمارية المؤسسات ومخاطرها", "L6"),
            ("Lecture 7/IS321_Lecture 7.pdf", "lecture-7-models-of-organizations-and-enterprises",
             "Lecture 7 - Models of Organizations and Enterprises", "المحاضرة 7 - نماذج المنظمات والمؤسسات", "L7"),
            ("Lecture 8/IS321_Lecture 8.pdf", "lecture-8-business-continuity-planning",
             "Lecture 8 - Business Continuity Planning", "المحاضرة 8 - تخطيط استمرارية الأعمال", "L8"),
            ("Lecture 9/IS321_Lecture 9.pdf", "lecture-9-linking-strategy-business-and-technology",
             "Lecture 9 - Linking Strategy, Business and Technology", "المحاضرة 9 - الربط بين الاستراتيجية والأعمال والتقنية", "L9"),
            ("Lecture 10/IS321_Lecture 10.pdf", "lecture-10-ea-technology-planning-and-intelligent-systems",
             "Lecture 10 - EA Technology Planning and Intelligent Enterprise Systems",
             "المحاضرة 10 - التخطيط التقني للمعمارية وأنظمة المؤسسات الذكية", "L10"),
            ("Lecture 11/IS321_Lecture 11.pdf", "lecture-11-the-most-significant-ea-frameworks",
             "Lecture 11 - The Most Significant EA Frameworks", "المحاضرة 11 - أهم أطر معمارية المؤسسات", "L11"),
            ("Lecture 12/IS321_Lecture 12.pdf", "lecture-12-togaf-and-the-architecture-development-method",
             "Lecture 12 - TOGAF and the Architecture Development Method", "المحاضرة 12 - TOGAF ومنهجية تطوير المعمارية", "L12"),
            ("Lecture 13/IS321_Lecture 13.pdf", "lecture-13-the-ea3-cube-framework",
             "Lecture 13 - The EA3 Cube Framework", "المحاضرة 13 - إطار EA3 Cube", "L13"),
            ("Lecture 14/IS321_Lecture 14.pdf", "lecture-14-ai-in-modern-enterprise-architecture",
             "Lecture 14 - AI in Modern Enterprise Architecture", "المحاضرة 14 - الذكاء الاصطناعي في معمارية المؤسسات الحديثة", "L14"),
        ],
    },
    {
        "code": "ECON101",
        "url": "/academics/other-courses/econ101/",
        "section": "other-courses",
        "name": "Principles of Microeconomics",
        "name_ar": "مبادئ الاقتصاد الجزئي",
        "prereqs": "None",
        "prereqs_ar": "لا يوجد",
        "file_id": "261-MICRO",
        "syllabus": False,
        "description": (
            "ECON101 introduces how individuals, firms and markets make choices under scarcity: "
            "demand and supply, elasticity, efficiency and equity, government actions in markets, "
            "utility and consumer choice, output and costs, and the market structures of perfect "
            "competition, monopoly and monopolistic competition. Textbook: Microeconomics by "
            "Michael Parkin, 14th Global Edition."
        ),
        "description_ar": (
            "يقدم مقرر ECON101 كيفية اتخاذ الأفراد والشركات والأسواق قراراتهم في ظل الندرة: العرض "
            "والطلب، والمرونة، والكفاءة والعدالة، والتدخل الحكومي في الأسواق، والمنفعة واختيار "
            "المستهلك، والإنتاج والتكاليف، وهياكل السوق من منافسة كاملة واحتكار ومنافسة احتكارية. "
            "الكتاب المقرر: Microeconomics لمايكل باركن، الطبعة العالمية الرابعة عشرة."
        ),
        "outcomes": [
            ("Recognize the role of scarcity, trade-offs, opportunity cost, and cost-benefit analysis in economic decision-making.",
             "التعرف على دور الندرة والمفاضلات وتكلفة الفرصة وتحليل التكلفة والمنفعة في اتخاذ القرارات الاقتصادية."),
            ("Recognize fundamental economic theories and concepts at the micro level.",
             "التعرف على النظريات والمفاهيم الاقتصادية الأساسية على المستوى الجزئي."),
            ("Perform demand and supply analysis to analyze the impact of real-world economic events on markets.",
             "إجراء تحليل للطلب والعرض لدراسة أثر الأحداث الاقتصادية الواقعية على الأسواق."),
            ("Analyze consumer behavior in terms of demand for products.",
             "تحليل سلوك المستهلك من حيث الطلب على المنتجات."),
            ("Demonstrate the ability to accomplish required tasks and assignments.",
             "إظهار القدرة على إنجاز المهام والواجبات المطلوبة."),
            ("Interpret basic microeconomic data.",
             "تفسير البيانات الاقتصادية الجزئية الأساسية."),
        ],
        "weights": [
            ("Quiz I", "الاختبار القصير الأول", "5%"),
            ("Major I", "الاختبار الفصلي الأول", "20%"),
            ("Quiz II", "الاختبار القصير الثاني", "5%"),
            ("Major II", "الاختبار الفصلي الثاني", "20%"),
            ("Assignments", "الواجبات", "5%"),
            ("Class Attendance and Participation", "الحضور والمشاركة الصفية", "5%"),
            ("Final Examination", "الاختبار النهائي", "40%"),
        ],
        "decks": [
            ("Chapter 1 - What is Economics_ (EXCLUDED)/Micro_Ch01_Lecture_Presentation 2.pdf",
             "chapter-1-what-is-economics", "Chapter 1 - What Is Economics?",
             "الفصل 1 - ما هو علم الاقتصاد؟", "CH 1"),
            ("Chapter 2 - The Economic Problem (EXCLUDED)/Micro_Ch02_Lecture_Presentation 2.pdf",
             "chapter-2-the-economic-problem", "Chapter 2 - The Economic Problem",
             "الفصل 2 - المشكلة الاقتصادية", "CH 2"),
            ("Chapter 3 - Demand and Supply/Micro_Ch03_Lecture_Presentation.pdf",
             "chapter-3-demand-and-supply", "Chapter 3 - Demand and Supply", "الفصل 3 - العرض والطلب", "CH 3"),
            ("Chapter 4 - Elasticity/Micro_Ch04_Lecture_Presentation.pdf",
             "chapter-4-elasticity", "Chapter 4 - Elasticity", "الفصل 4 - المرونة", "CH 4"),
            ("Chapter 5 - Efficiency and Equity/Note 21 Sep 2027.pdf",
             "chapter-5-efficiency-and-equity", "Chapter 5 - Efficiency and Equity", "الفصل 5 - الكفاءة والعدالة", "CH 5"),
            ("Chapter 6 - Government Actions in the Market/Ch06-Slides (1) 2.pdf",
             "chapter-6-government-actions-in-markets", "Chapter 6 - Government Actions in Markets",
             "الفصل 6 - التدخل الحكومي في الأسواق", "CH 6"),
            ("Chapter 6 - Government Actions in the Market/Micro_Ch06_Lecture_Presentation.pdf",
             "chapter-6-government-actions-in-markets-textbook-slides",
             "Chapter 6 - Government Actions in Markets (Textbook Slides)",
             "الفصل 6 - التدخل الحكومي في الأسواق (شرائح الكتاب)", "CH 6"),
            ("Chapter 8 - Utility and Demand /Ch06-slides 2.pdf",
             "chapter-8-utility-and-demand", "Chapter 8 - Utility and Demand", "الفصل 8 - المنفعة والطلب", "CH 8"),
            ("Chapter 8 - Utility and Demand /Micro_Ch08_Lecture_Presentation.pdf",
             "chapter-8-utility-and-demand-textbook-slides", "Chapter 8 - Utility and Demand (Textbook Slides)",
             "الفصل 8 - المنفعة والطلب (شرائح الكتاب)", "CH 8"),
            ("Chapter 9 - Possibilities, Preferences, and Choices/Ch09-slides 2.pdf",
             "chapter-9-possibilities-preferences-and-choices", "Chapter 9 - Possibilities, Preferences and Choices",
             "الفصل 9 - الإمكانات والتفضيلات والاختيارات", "CH 9"),
            ("Chapter 9 - Possibilities, Preferences, and Choices/Micro_Ch09_Lecture_Presentation.pdf",
             "chapter-9-possibilities-preferences-and-choices-textbook-slides",
             "Chapter 9 - Possibilities, Preferences and Choices (Textbook Slides)",
             "الفصل 9 - الإمكانات والتفضيلات والاختيارات (شرائح الكتاب)", "CH 9"),
            ("Chapter 11 -  Output and Costs/Ch11-slides 2.pdf",
             "chapter-11-output-and-costs", "Chapter 11 - Output and Costs", "الفصل 11 - الإنتاج والتكاليف", "CH 11"),
            ("Chapter 12 - Perfect Competition /Ch12-slides.pdf",
             "chapter-12-perfect-competition", "Chapter 12 - Perfect Competition", "الفصل 12 - المنافسة الكاملة", "CH 12"),
            ("Chapter 13 - Monopoly /Ch13-slides.pdf",
             "chapter-13-monopoly", "Chapter 13 - Monopoly", "الفصل 13 - الاحتكار", "CH 13"),
            ("Chapter 14 - Monopolistic Competition /Ch14-slides.pdf",
             "chapter-14-monopolistic-competition", "Chapter 14 - Monopolistic Competition",
             "الفصل 14 - المنافسة الاحتكارية", "CH 14"),
        ],
    },
]

TABS = [
    ("", "Overview", "نظرة عامة"),
    ("slide-breakdowns/", "Slide Breakdowns", "تفكيك الشرائح"),
    ("slides/", "Slides", "الشرائح"),
    ("annotated-slides/", "Annotated Slides", "الشرائح المشروحة"),
    ("extra-resources/", "Study Material", "المواد الدراسية"),
    ("exams/", "Exams", "الاختبارات"),
]
ARROW = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="square"><path d="M5 12h14M12 5l7 7-7 7" /></svg>'
)


def read(path):
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def esc(text):
    return html.escape(text, quote=True)


def replace_block(pattern, new, text, flags=re.S):
    """Swap the one match of pattern for new; a template change must fail loudly."""
    result, count = re.subn(pattern, lambda _m: new, text, count=1, flags=flags)
    if count != 1:
        raise SystemExit("template no longer matches: " + pattern)
    return result


def course_dir(c):
    return os.path.join(DOCS, c["url"].strip("/"))


def rebrand(text, c):
    lower = c["code"].lower()
    text = text.replace("academics/computer-science/cs340", c["url"].strip("/"))
    text = text.replace(TEMPLATE_NAME, c["name"]).replace("CS340", c["code"]).replace("cs340", lower)
    label, label_ar = SECTIONS[c["section"]]
    text = re.sub(
        r'(<a\s+class="breadcrumb-link"\s+href=")/academics/computer-science/("[^>]*>)\s*Computer Science(</a)',
        lambda m: m.group(1) + "/academics/%s/" % c["section"] + m.group(2) + label + m.group(3),
        text,
    )
    text = re.sub(
        r'(<span class="meta-key"[^>]*>TRACK</span>\s*<span class="meta-val"[^>]*data-ar-text=")[^"]*("\s*>)\s*Computer Science',
        lambda m: m.group(1) + label_ar + m.group(2) + label,
        text, count=1, flags=re.S,
    )
    return text


def stamp(text, data, url):
    return NAV_RE.sub(lambda _m: render_nav(data, url), text, count=1)


def move_decks(c):
    # The upload arrived as "IS321 " with a trailing space; the site uses a lowercase slug.
    target_dir = course_dir(c)
    upload = os.path.join(os.path.dirname(target_dir), c["code"] + " ")
    if os.path.isdir(upload) and not os.path.exists(target_dir):
        os.rename(upload, target_dir)
    slides = os.path.join(target_dir, "slides")
    for source, slug, *_ in c["decks"]:
        target = os.path.join(slides, slug, slug + ".pdf")
        origin = os.path.join(slides, source)
        if os.path.exists(origin):
            os.makedirs(os.path.dirname(target), exist_ok=True)
            shutil.move(origin, target)
        elif not os.path.exists(target):
            raise SystemExit("missing deck: " + source)
    keep = {slug for _src, slug, *_ in c["decks"]}
    for name in os.listdir(slides):
        path = os.path.join(slides, name)
        if os.path.isdir(path) and name not in keep and not os.listdir(path):
            os.rmdir(path)  # the emptied upload folders


def add_course_entries(data, c):
    url = c["url"]
    data["sections"][url] = [
        {"url": url + path, "attrs": 'data-en-text="%s" data-ar-text="%s"' % (en.upper(), ar), "label": en.upper()}
        for path, en, ar in TABS
    ]

    data["children"][url + "slides/"] = [
        {"url": "%sslides/%s/" % (url, slug), "attrs": "", "label": title}
        for _src, slug, title, *_ in c["decks"]
    ]


def group_of(data, group_id):
    return next(n for n in data["tree"] if n.get("id") == group_id)


def insert_course(group, c, before_label):
    if any(k.get("url") == c["url"] for k in group["children"]):
        return
    at = next(i for i, k in enumerate(group["children"]) if k.get("label") == before_label)
    group["children"].insert(at, {"type": "course", "url": c["url"], "label": c["code"]})


def update_sidebar_data():
    with open(DATA_FILE, encoding="utf-8") as f:
        data = json.load(f)
    insert_course(group_of(data, "tree-computer-science"), COURSES[0], "CS316")
    if not any(n.get("id") == IS_GROUP for n in data["tree"]):
        at = next(i for i, n in enumerate(data["tree"]) if n.get("id") == "tree-math")
        data["tree"].insert(at, {"type": "group", "id": IS_GROUP, "label": IS_LABEL, "children": [
            {"type": "course", "url": COURSES[1]["url"], "label": "IS321"}]})
    insert_course(group_of(data, "tree-other-courses"), COURSES[2], "ISC113")
    for c in COURSES:
        add_course_entries(data, c)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return data


SLIDE_ANCHORS = {
    "CS311": '  "/academics/computer-science/cs316/": {',
    "IS321": '  "/academics/math/stat101/": {',
    "ECON101": '  "/academics/other-courses/isc113/": {',
}


def update_slide_index(c):
    raw = read(SLIDE_INDEX)
    key = '  "%s": {' % c["url"]
    start = raw.find(key)
    if start >= 0:
        depth, i = 0, raw.index("{", start)
        for j in range(i, len(raw)):
            depth += {"{": 1, "}": -1}.get(raw[j], 0)
            if depth == 0:
                end = raw.index("\n", j) + 1
                break
        raw = raw[:start] + raw[end:]
    counted = [d for d in c["decks"] if d[4]]
    spec = {
        "rows": {str(i): ["%s/%s.pdf" % (d[1], d[1])] for i, d in enumerate(counted, 1)},
        "ignore_decks": ["%s/%s.pdf" % (d[1], d[1]) for d in c["decks"] if not d[4]],
    }
    block = json.dumps({c["url"]: spec}, indent=2, ensure_ascii=False)[2:-2]
    anchor = SLIDE_ANCHORS[c["code"]]
    if anchor not in raw:
        raise SystemExit("course-slide-index.json lost its anchor for " + c["code"])
    write(SLIDE_INDEX, raw.replace(anchor, block + ",\n" + anchor, 1))


def topic_row(num, name, name_ar, url):
    return (
        '<div class="topic-item"><span class="topic-num">%s</span>'
        '<a class="topic-name topic-name-link" href="%s" data-ar-text="%s">%s</a></div>'
        % (esc(num), url, esc(name_ar), esc(name))
    )


def topic_display_title(name, name_ar):
    name = re.sub(r"^(?:Lecture|Chapter|Topic)\s+[\d.]+\s*-\s*", "", name)
    name_ar = re.sub(r"^(?:المحاضرة|الفصل|الموضوع)\s+[\d.]+\s*-\s*", "", name_ar)
    return name, name_ar


def exam_page_counts_html(c):
    groups = []
    for heading, heading_ar, rows, total in EXAM_PAGE_COUNTS.get(c["code"], []):
        items = "".join(
            '<div class="topic-item"><span class="topic-num">%s</span>'
            '<a class="topic-name topic-name-link" href="%sslides/%s/" '
            'data-ar-text="%s">%s</a><span class="topic-meta">%d SLIDES</span></div>'
            % (esc(num), c["url"], slug, esc(title), esc(title), count)
            for num, title, slug, count in rows
        )
        items += (
            '<div class="topic-item exam-total"><span class="topic-num">&Sigma;</span>'
            '<a class="topic-name topic-name-link" href="%sslides/" '
            'data-ar-text="المجموع">Total</a><span class="topic-meta">%d SLIDES</span></div>'
            % (c["url"], total)
        )
        groups.append(
            '<div class="exam-count-group"><div class="exam-count-heading">'
            '<span data-ar-text="%s">%s</span><span class="exam-count-total">%d SLIDES</span></div>'
            '<div class="topics-list">%s</div></div>'
            % (esc(heading_ar), heading, total, items)
        )
    if not groups:
        return (
            '<div class="exam-scope-note" data-ar-text="لم تتم إضافة توزيع عدد صفحات الشرائح حسب الاختبار بعد.">'
            'No page-count breakdown by exam has been added yet.</div>'
        )
    scope = (
        "SCOPE — Taken from the course syllabus: Quiz I covers Lectures 1–5, "
        "Quiz II covers Lectures 6–8, the Major Exam covers Lectures 1–10, and "
        "the Final is comprehensive over Lectures 1–14. Slide counts are the real "
        "page counts of the lecture PDFs."
        if c["code"] == "IS321"
        else "SCOPE — Taken from the course syllabus: Quiz I covers Chapters 1–2, Major I covers Chapters 2–4, "
        "Quiz II covers Chapters 5–6, Major II covers Chapters 6 and 8–9, and the Final is comprehensive. "
        "Counts use the primary course deck for each chapter; alternate textbook and extra-resource PDFs are excluded."
        if c["code"] == "ECON101"
        else "SCOPE — Taken from the course syllabus. Slide counts are the real page counts of the lecture PDFs."
    )
    scope_ar = (
        "النطاق مأخوذ من الخطة الدراسية: الاختبار القصير الأول يغطي المحاضرات 1–5، "
        "والاختبار القصير الثاني المحاضرات 6–8، والاختبار الفصلي المحاضرات 1–10، "
        "والاختبار النهائي شامل للمحاضرات 1–14. أعداد الشرائح هي أعداد صفحات ملفات PDF الفعلية."
        if c["code"] == "IS321"
        else "النطاق مأخوذ من الخطة الدراسية: الاختبار القصير الأول يغطي الفصلين 1–2، والاختبار الفصلي الأول الفصول 2–4، "
        "والاختبار القصير الثاني الفصلين 5–6، والاختبار الفصلي الثاني الفصول 6 و8–9، والاختبار النهائي شامل. "
        "تستخدم الأعداد شريحة المقرر الأساسية لكل فصل، مع استبعاد شرائح الكتاب والمصادر الإضافية البديلة."
        if c["code"] == "ECON101"
        else "النطاق مأخوذ من الخطة الدراسية. أعداد الشرائح هي أعداد صفحات ملفات PDF الفعلية."
    )
    return '<div class="exam-scope-note" data-ar-text="%s">%s</div>%s' % (
        esc(scope_ar), scope, "".join(groups)
    )


def overview_body(c):
    rows = "".join(
        topic_row(num, *topic_display_title(title, ar), "%sslides/%s/" % (c["url"], slug))
        for _src, slug, title, ar, num in c["decks"] if num
    )
    blocks = "".join(
        '<div class="data-block"><span class="data-block-label">%s</span>%s</div>' % b for b in [
            ("Course Code", '<span class="data-block-val">%s</span>' % c["code"]),
            ("Credit Hours", '<span class="data-block-val">3</span>'),
            ("Prerequisites",
             '<span class="data-block-val" data-ar-text="%s" style="font-family: var(--font-mono); '
             'font-size: 1.1rem; padding-top: 6px">%s</span>' % (c["prereqs_ar"], c["prereqs"])),
        ]
    )
    out = [
        '<div class="content-section"><div class="grid-data-blocks">', blocks, "</div>",
        '<div class="section-label" id="section-description">01_DESCRIPTION</div>',
        '<div class="text-block"><p data-ar-text="%s">%s</p></div>' % (esc(c["description_ar"]), esc(c["description"])),
        '<div class="section-label" id="section-syllabus-index">02_SYLLABUS_INDEX</div>',
        '<div class="topics-list" style="margin-bottom: 48px">', rows, "</div>",
    ]
    if c["outcomes"]:
        items = "".join('<li data-ar-text="%s">%s</li>' % (esc(ar), esc(en)) for en, ar in c["outcomes"])
        out += ['<div class="section-label" id="section-learning-outcomes">03_LEARNING_OUTCOMES</div>',
                '<div class="text-block"><ul class="learning-outcomes">', items, "</ul></div>"]
    if c["weights"]:
        items = "".join(
            '<div class="topic-item"><span class="topic-num">0x%02X</span>'
            '<span class="topic-name" data-ar-text="%s">%s</span><span class="topic-meta">%s</span></div>'
            % (i, esc(ar), esc(en), pct) for i, (en, ar, pct) in enumerate(c["weights"], 1)
        )
        out += ['<div class="section-label" id="section-weight-of-assessments">04_WEIGHT_OF_ASSESSMENTS</div>',
                '<div class="topics-list" style="margin-bottom: 48px">', items, "</div>"]
    out += [
        '<div class="section-label" id="section-page-count-by-exam">05_PAGE_COUNT_BY_EXAM</div>',
        exam_page_counts_html(c),
    ]
    out.append("</div>")
    return "".join(out)


def build_overview(data, c):
    t = rebrand(read(os.path.join(TEMPLATE_DIR, "index.html")), c)
    t = t.replace("</style>", EXAM_COUNT_CSS + "    </style>", 1)
    t = t.replace(".tag-complete {", ".tag-available,\n      .tag-complete {", 1)
    t = replace_block(
        r'<span class="tag-complete"[^>]*>COMPLETE</span>',
        '<span class="tag-available" data-en-text="AVAILABLE" data-ar-text="متاح">AVAILABLE</span>', t)
    t = replace_block(r'<h2\s+class="course-name".*?</h2>',
                      '<h2 class="course-name" data-ar-text="%s">%s</h2>' % (c["name_ar"], c["name"]), t)
    t = replace_block(r'<p\s+class="course-desc-brief".*?</p>',
                      '<p class="course-desc-brief" data-ar-text="%s">%s</p>' % (esc(c["description_ar"]), esc(c["description"])), t)
    links = "".join(
        '<a href="%s%s" class="sub-nav-item%s" data-en-text="[ %s ]" data-ar-text="[ %s ]">[ %s ]</a>'
        % (c["url"], path, " active" if not path else "", en.upper(), ar, en.upper())
        for path, en, ar in TABS
    )
    t = replace_block(r'<nav class="sub-nav">.*?</nav>', '<nav class="sub-nav">%s</nav>' % links, t)
    t = replace_block(r'<div class="content-section".*?(?=\s*</article>)', overview_body(c), t)
    t = re.sub(r'(class="meta-val highlight"[^>]*>)\s*COMPLETE', r"\1AVAILABLE", t, count=1, flags=re.S)
    t = re.sub(
        r'(<span class="meta-key"[^>]*>PREREQUISITES</span>\s*<span\s+class="meta-val"[^>]*?)'
        r'\s*data-ar-text="[^"]*"\s*>[^<]*',
        lambda m: '%s data-ar-text="%s">%s' % (m.group(1), c["prereqs_ar"], c["prereqs"]),
        t, count=1, flags=re.S,
    )
    t = re.sub(r'(<span class="meta-key"[^>]*>FILE_ID</span>.*?>)\s*04012023-DB',
               lambda m: m.group(1) + c["file_id"], t, count=1, flags=re.S)
    quick = []
    if c["syllabus"]:
        quick.append((c["url"] + "syllabus.docx", "Syllabus", "الخطة الدراسية", True))
    quick.append(("#section-description", "Description", "الوصف", False))
    if c["outcomes"]:
        quick.append(("#section-learning-outcomes", "Learning Outcomes", "نواتج التعلم", False))
    if c["weights"]:
        quick.append(("#section-weight-of-assessments", "Weight Of Assessments", "أوزان التقييمات", False))
    else:
        quick.append(("#section-syllabus-index", "Topics", "الموضوعات", False))
    quick.append(("#section-page-count-by-exam", "Page Count By Exam", "عدد الشرائح حسب الاختبار", False))
    quick_html = "".join(
        '<a href="%s" class="quick-link-btn"%s data-en-text="%s" data-ar-text="%s">%s</a>'
        % (href, ' target="_blank" rel="noopener noreferrer"' if new_tab else "", en, ar, en)
        for href, en, ar, new_tab in quick
    )
    t = replace_block(r'<div class="quick-links">.*?</div>', '<div class="quick-links">%s</div>' % quick_html, t)
    write(os.path.join(course_dir(c), "index.html"), stamp(t, data, c["url"]))


def tabs_html(c, active):
    return "".join(
        '<a href="%s%s" class="tab%s" data-en-text="%s" data-ar-text="%s">%s</a>'
        % (c["url"], path, " active" if path == active else "", en, ar, en)
        for path, en, ar in TABS
    )


def preview_style(c):
    return (
        ' style="--strip-dark: url(&quot;/assets/previews/%s/slides-university.jpg&quot;);'
        '--strip-light: url(&quot;/assets/previews/%s/slides-university.jpg&quot;)"'
        % (c["code"].lower(), c["code"].lower())
    )


def build_listing(data, c):
    t = rebrand(read(os.path.join(TEMPLATE_DIR, "slides/index.html")), c)
    t = replace_block(r'<nav class="content-tabs">.*?</nav>',
                      '<nav class="content-tabs">%s</nav>' % tabs_html(c, "slides/"), t)
    count = len(c["decks"])
    new = "".join(
        '<a href="%sslides/%s/" class="deck-preview"><span class="deck-thumb"'
        ' style="background-position: 0 %.4f%%"></span>'
        '<div class="deck-name">%s</div></a>'
        % (c["url"], slug, (i * 100 / max(1, count - 1)), esc(title))
        for i, (_src, slug, title, *_rest) in enumerate(c["decks"])
    )
    gallery = (
        '<div class="directory-container slide-hub">'
        '<p class="slide-hub-intro" data-en-text="Lecture slides for this course." '
        'data-ar-text="شرائح محاضرات هذا المقرر.">Lecture slides for this course.</p>'
        '<section class="slide-gallery" id="university"%s>'
        '<h2 data-en-text="Course Slides" data-ar-text="شرائح المقرر">Course Slides</h2>'
        '<div class="slide-gallery-grid">%s</div></section></div>' % (preview_style(c), new)
    )
    t = replace_block(r'<div class="directory-container slide-hub"[^>]*>.*?(?=\s*</main>)', gallery, t)
    url = c["url"] + "slides/"
    write(os.path.join(course_dir(c), "slides/index.html"), stamp(t, data, url))


def build_viewers(data, c):
    decks = c["decks"]
    shell = rebrand(read(os.path.join(TEMPLATE_DIR, "slides", TEMPLATE_DECK, "index.html")), c)
    for i, (_src, slug, title, *_rest) in enumerate(decks):
        t = shell.replace(TEMPLATE_DECK, slug).replace(TEMPLATE_DECK_TITLE, esc(title))
        t = t.replace("ITEM_01", "ITEM_%02d" % (i + 1))
        prev_link = (
            '<a href="%sslides/%s/" class="nav-link prev">&lt;- PREVIOUS</a>' % (c["url"], decks[i - 1][1])
            if i else '<span class="nav-link prev disabled">&lt;- PREVIOUS</span>'
        )
        next_link = (
            '<a href="%sslides/%s/" class="nav-link next">NEXT -&gt;</a>' % (c["url"], decks[i + 1][1])
            if i + 1 < len(decks) else '<span class="nav-link next disabled">NEXT -&gt;</span>'
        )
        t = replace_block(r'<div class="nav-strip">.*?</div>',
                          '<div class="nav-strip">%s%s</div>' % (prev_link, next_link), t)
        url = "%sslides/%s/" % (c["url"], slug)
        write(os.path.join(course_dir(c), "slides", slug, "index.html"), stamp(t, data, url))


def course_li(c):
    return '<li class="tree-item"><a class="tree-file" href="%s">%s</a></li>' % (c["url"], c["code"])


IS_LI = (
    '<li class="tree-item"><button class="tree-course-link tree-toggle-button" type="button" '
    'data-tree-toggle="%s" aria-expanded="false"><span class="tree-toggle">[+]</span> %s</button></li>'
    '<ul id="%s" class="tree-children">%s</ul>' % (IS_GROUP, IS_LABEL, IS_GROUP, course_li(COURSES[1]))
)
CS311_ANCHOR = re.compile(r'<li class="tree-item[^"]*">\s*<a class="tree-file[^"]*"[^>]*href="/academics/computer-science/cs316/"')
ECON_ANCHOR = re.compile(r'<li class="tree-item[^"]*">\s*<a class="tree-file[^"]*"[^>]*href="/academics/other-courses/isc113/"')
IS_ANCHOR = re.compile(r'<li class="tree-item[^"]*">\s*<button[^>]*data-tree-toggle="tree-math"')


def register_everywhere():
    """Add only the new sidebar rows; never re-stamp other pages."""
    skip = tuple(course_dir(c) for c in COURSES) + (os.path.join(DOCS, IS_HUB.strip("/")),)
    changed = 0
    for dirpath, _dirs, files in os.walk(DOCS):
        if dirpath.startswith(skip):
            continue
        for name in files:
            if not name.endswith(".html"):
                continue
            path = os.path.join(dirpath, name)
            text = read(path)
            if "academic-sidebar" not in text:
                continue
            new = text
            if COURSES[0]["url"] + '"' not in new:
                new = CS311_ANCHOR.sub(lambda m: course_li(COURSES[0]) + m.group(0), new, count=1)
            if COURSES[2]["url"] + '"' not in new:
                new = ECON_ANCHOR.sub(lambda m: course_li(COURSES[2]) + m.group(0), new, count=1)
            if 'data-tree-toggle="%s"' % IS_GROUP not in new:
                new = IS_ANCHOR.sub(lambda m: IS_LI + m.group(0), new, count=1)
            if new != text:
                write(path, new)
                changed += 1
    return changed


def course_row(c):
    return (
        '<a class="course-row" href="%s"><div class="course-code">%s</div>'
        '<div class="course-name"><span data-ar-text="%s">%s</span></div>'
        '<div class="course-status-area"><div class="status-tag status-available">AVAILABLE</div>'
        '<div class="row-arrow">-&gt;</div></div></a\n            >' % (c["url"], c["code"], c["name_ar"], c["name"])
    )


def add_hub_row(path, c, anchor):
    t = read(path)
    row_pattern = r'<a class="course-row" href="%s">.*?</a\s*>' % re.escape(c["url"])
    if re.search(row_pattern, t, flags=re.S):
        t = re.sub(row_pattern, course_row(c), t, count=1, flags=re.S)
    else:
        if anchor not in t:
            raise SystemExit("hub has no anchor row: " + anchor)
        t = t.replace(anchor, course_row(c) + anchor, 1)
    return t


def update_cs_hub():
    path = os.path.join(DOCS, "academics/computer-science/index.html")
    t = add_hub_row(path, COURSES[0], '<a class="course-row" href="/academics/computer-science/cs316/"')
    t = t.replace("8 courses.<br />Structured", "9 courses.<br />Structured")
    t = t.replace("<span>8 Courses</span>", "<span>9 Courses</span>")
    t = re.sub(r'("computer science":\s*")8 courses\.', r"\g<1>9 courses.", t)
    t = re.sub(r'("computer science":\s*\[\s*"CS Track",\s*")8 Courses"', r'\g<1>9 Courses"', t)
    write(path, t)


def update_other_hub():
    path = os.path.join(DOCS, "academics/other-courses/index.html")
    t = add_hub_row(path, COURSES[2], '<a class="course-row" href="/academics/other-courses/isc113/"')
    # The listing shows 7 rows with ECON101; the old 3 and 4 counts were already stale.
    t = t.replace("4 courses.<br />One English hub", "7 courses.<br />One English hub")
    t = re.sub(r'(?:3|4) courses\.<br>One English hub', "7 courses.<br>One English hub", t)
    t = re.sub(r'<span>[34] Courses</span>', "<span>7 Courses</span>", t, count=1)
    write(path, t)


def use_track_styles(text):
    """Give a hub cloned from the red Cybersecurity page a normal track's CSS."""
    pattern = re.compile(r"<style\b[^>]*>.*?</style>", re.S | re.I)
    styles = iter(pattern.findall(read(os.path.join(DOCS, "academics/computer-science/index.html"))))
    text = pattern.sub(lambda m: next(styles, m.group(0)), text)
    return re.sub(r'[ \t]*<link rel="stylesheet" href="/styles/cyber-track\.css"\s*/?>\n?', "", text)


def build_is_hub(data):
    """Clone the Cybersecurity hub for the new section."""
    path = os.path.join(DOCS, IS_HUB.strip("/"), "index.html")
    t = read(os.path.join(DOCS, "academics/cybersecurity/index.html"))
    t = t.replace("--bg-elevated: #140a0c;", "--bg-elevated: #110822;")
    t = t.replace("--brand-purple: #ff2a4b;", "--brand-purple: #b829ea;")
    t = t.replace("--brand-purple-dim: rgba(255, 42, 75, 0.2);",
                  "--brand-purple-dim: rgba(184, 41, 234, 0.15);")
    t = t.replace("--brand-purple-mute: rgba(255, 42, 75, 0.1);",
                  "--brand-purple-mute: rgba(184, 41, 234, 0.1);")
    t = t.replace("#ff2a4b", "#b829ea").replace("rgba(255, 42, 75", "rgba(184, 41, 234")
    t = t.replace("/academics/cybersecurity/", IS_HUB)
    t = t.replace("SHOUG.TECH // CYBERSECURITY", "SHOUG.TECH // INFORMATION SYSTEMS")
    t = replace_block(r'<span vid="73">Cybersecurity</span>', '<span vid="73">Information Systems</span>', t)
    t = replace_block(r'<div class="hero-label">\[ CYBERSECURITY \]</div>', '<div class="hero-label">[ INFORMATION SYSTEMS ]</div>', t)
    t = replace_block(r'TRACK\.ID: 0xCS_99', "TRACK.ID: 0xIS_01", t)
    t = replace_block(r'<h1 class="hero-title">.*?</h1>',
                      '<h1 class="hero-title">Information systems.<br />Architecture, strategy,<br />and planning.</h1>', t)
    t = replace_block(
        r'<div class="hero-metadata-strip">.*?</div>',
        '<div class="hero-metadata-strip"><span>IS Track</span><span class="meta-sep">//</span>'
        '<span>Architecture</span><span class="meta-sep">·</span><span>Strategy</span>'
        '<span class="meta-sep">·</span><span>Planning</span></div>', t)
    t = replace_block(r'<div class="course-list">.*?(?=\n\s*</div>\s*(?:<footer|</div>\s*</main>|</main>))',
                      '<div class="course-list">' + course_row(COURSES[1]), t)
    # The hero is re-written from these tables, keyed by the hero label, on load.
    for en, label, title, meta in (
        (True, "INFORMATION SYSTEMS", "Information systems.<br>Architecture, strategy,<br>and planning.",
         ["IS Track", "Architecture", "Strategy", "Planning"]),
        (False, "نظم المعلومات", "نظم المعلومات.<br>المعمارية، والاستراتيجية،<br>والتخطيط.",
         ["مسار نظم المعلومات", "المعمارية", "الاستراتيجية", "التخطيط"]),
    ):
        def fill(block):
            body = block.group(0)
            body = re.sub(r'cybersecurity:\s*"[^"]*",', lambda _m: '"information systems": %s,' % json.dumps(label, ensure_ascii=False), body, count=1)
            body = re.sub(r'cybersecurity:\s*"[^"]*",', lambda _m: '"information systems": %s,' % json.dumps(title, ensure_ascii=False), body, count=1)
            body = re.sub(r'cybersecurity:\s*\[[^\]]*\],', lambda _m: '"information systems": %s,' % json.dumps(meta, ensure_ascii=False), body, count=1)
            return body
        pattern = r'trackLabels:\s*\{\s*"computer science":\s*"%s".*?trackMeta:\s*\{.*?\n\s*\},' % ("COMPUTER SCIENCE" if en else "علوم الحاسب")
        t, n = re.subn(pattern, fill, t, count=1, flags=re.S)
        if n != 1:
            raise SystemExit("hub translation table not found")
    write(path, stamp(use_track_styles(t), data, IS_HUB))


def update_academics_hub():
    path = os.path.join(DOCS, "academics/index.html")
    t = read(path)
    if 'href="%s" class="track-card"' % IS_HUB not in t:
        match = re.search(r'<a href="/academics/math/" class="track-card"[^>]*>.*?</a>', t, re.S)
        if not match:
            raise SystemExit("academics hub has no math card")
        card = re.sub(r'\s+vid="\d+"', "", match.group(0))
        card = card.replace("/academics/math/", IS_HUB)
        card = re.sub(r'(<h2 class="card-title display")[^>]*>.*?</h2>',
                      lambda m: m.group(1) + ' data-ar-text="نظم المعلومات">INFORMATION SYSTEMS</h2>', card, count=1, flags=re.S)
        card = re.sub(r'(<div class="card-count mono">)\s*\d+\s*', r"\g<1>01", card, count=1)
        tags = "".join('<span class="tag-item" data-ar-text="%s">%s</span>' % (ar, en) for en, ar in (
            ("Architecture", "المعمارية"), ("Strategy", "الاستراتيجية"), ("Planning", "التخطيط")))
        card, n = re.subn(r'(<div class="card-tags mono">).*?(</div>)', lambda m: m.group(1) + tags + m.group(2), card, count=1, flags=re.S)
        if n != 1:
            raise SystemExit("math card has no tags")
        t = t[: match.start()] + card + "\n\n          " + t[match.start() :]
    t = re.sub(r'("computer science":\s*")8 courses\.', r"\g<1>9 courses.", t)
    t = re.sub(r'("computer science":\s*\[\s*"CS Track",\s*")8 Courses"', r'\g<1>9 Courses"', t)
    t = re.sub(r'("other courses":\s*")\d courses\.', r"\g<1>7 courses.", t)
    t = re.sub(r'("other courses":\s*\[\s*"General Track",\s*")\d Courses"', r'\g<1>7 Courses"', t)
    t = re.sub(r'(href="/academics/computer-science/" class="track-card".*?<div class="card-count mono"[^>]*>)\d+', r"\g<1>09", t, count=1, flags=re.S)
    t = re.sub(r'(href="/academics/other-courses/" class="track-card".*?<div class="card-count mono"[^>]*>)\d+', r"\g<1>07", t, count=1, flags=re.S)
    write(path, t)


def update_routes():
    path = os.path.join(DOCS, "javascripts/course-routes.js")
    t = read(path)
    for key, before, c in (("cs311", "cs316", COURSES[0]), ("econ101", "ethcs303", COURSES[2]), ("is321", "isc113", COURSES[1])):
        if key + ":" not in t:
            anchor = "  %s: " % before
            if anchor not in t:
                raise SystemExit("course-routes.js has no route for " + before)
            t = t.replace(anchor, '  %s: "%s",\n' % (key, c["url"]) + anchor, 1)
    write(path, t)


def update_arabic():
    path = os.path.join(DOCS, "javascripts/arabic-localization.js")
    t = read(path)
    if '"%s"' % IS_LABEL not in t:
        anchor = '    "OTHER COURSES/": "مواد أخرى/",\n'
        if anchor not in t:
            raise SystemExit("arabic-localization.js lost its sidebar table")
        t = t.replace(anchor, '    "%s": "نظم المعلومات/",\n    "Information Systems": "نظم المعلومات",\n' % IS_LABEL + anchor, 1)
        write(path, t)


def main():
    for c in COURSES:
        move_decks(c)
    data = update_sidebar_data()
    for c in COURSES:
        update_slide_index(c)
        build_overview(data, c)
        build_listing(data, c)
        build_viewers(data, c)
    update_cs_hub()
    update_other_hub()
    build_is_hub(data)
    update_academics_hub()
    update_routes()
    update_arabic()
    print("pages updated with the new sidebar rows:", register_everywhere())
    for c in COURSES:
        subprocess.run([sys.executable, os.path.join(REPO, "scripts/build_slide_counts.py"), "--only", c["url"]], check=True)


if __name__ == "__main__":
    main()
