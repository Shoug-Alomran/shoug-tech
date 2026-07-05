from __future__ import annotations

import html
import os
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any

import markdown
import yaml


ROOT = Path(__file__).resolve().parents[1]
DOWNLOADS = Path("/Users/shougalomran/Downloads")
OUT = Path(os.environ.get("SHOUG_GENERATED_OUT", str(Path(tempfile.gettempdir()) / "shoug-tech-generated-html")))


TEMPLATES = {
    "home": DOWNLOADS / "design-b0e12069-816f-4e5a-b785-855757b31e65.html",
    "academics": DOWNLOADS / "design-2a18fa88-c913-43d9-8340-837230bd88ab.html",
    "track": DOWNLOADS / "design-695d7aa2-f4df-4ba2-8ac9-94a9655ca80e.html",
    "course": DOWNLOADS / "design-4a1dd9dc-5d1d-4574-9531-21baed952747.html",
    "chapter_index": DOWNLOADS / "design-ea27e387-3079-409c-a5bf-23ecdc9153aa.html",
    "content_viewer": DOWNLOADS / "design-e422699d-3462-48cf-b969-79d2be50c4a6.html",
    "about": DOWNLOADS / "design-1ea76746-41f2-4d84-9654-04ca913aac32.html",
    "projects": DOWNLOADS / "design-768c0db2-f082-4e99-8b32-8bbbe1f9de71.html",
    "work": DOWNLOADS / "design-fc100599-482f-4a71-a454-23a34e1d8cf3.html",
    "workshops": DOWNLOADS / "design-0869ff3b-89af-4282-a957-271d8a465cfa.html",
    "cyber_workshop": DOWNLOADS / "design-69b028d7-b5c8-44b7-8342-6d5c87026221.html",
    "tutor_workshop": DOWNLOADS / "design-0c483eb4-4586-48ae-bed0-c4309821b8e9.html",
    "resources": DOWNLOADS / "design-4f5e3963-3b02-4f39-884c-c6c145874ad9.html",
    "copyright": DOWNLOADS / "design-48c13965-3467-4568-b2ca-04adada93d9d.html",
}


COURSES: dict[str, dict[str, Any]] = {
    "CS101": {
        "track": "Computer Science",
        "path": "docs/Academics/computer-science/CS101/intro.md",
        "url": "/course-cs101.html",
        "sections": {"Overview": "/Academics/computer-science/CS101/intro/", "Slides": "/Academics/computer-science/CS101/slides/overview/"},
    },
    "CS102": {
        "track": "Computer Science",
        "path": "docs/Academics/computer-science/CS102/intro.md",
        "url": "/course-cs102.html",
        "sections": {"Overview": "/Academics/computer-science/CS102/intro/", "Slides": "/Academics/computer-science/CS102/slides/overview/"},
    },
    "CS210": {
        "track": "Computer Science",
        "path": "docs/Academics/computer-science/CS210/intro.md",
        "url": "/course-cs210.html",
        "sections": {
            "Overview": "/Academics/computer-science/CS210/intro/",
            "Topics": "/Academics/computer-science/CS210/topics-overview/",
            "Study Material": "/Academics/computer-science/CS210/study-material-overview/",
            "Slides": "/Academics/computer-science/CS210/slides/overview/",
            "Exams": "/Academics/computer-science/CS210/Exams/overview/",
        },
    },
    "CS285": {
        "track": "Computer Science",
        "path": "docs/Academics/computer-science/CS285/intro.md",
        "url": "/course-cs285.html",
        "sections": {
            "Overview": "/Academics/computer-science/CS285/intro/",
            "Slide Breakdowns": "/Academics/computer-science/CS285/chapters-overview/",
            "Study Material": "/Academics/computer-science/CS285/study-material-overview/",
            "Slides": "/Academics/computer-science/CS285/slides/overview/",
        },
    },
    "CS330": {
        "track": "Computer Science",
        "path": "docs/Academics/computer-science/CS330/intro.md",
        "url": "/course-cs330.html",
        "sections": {"Overview": "/Academics/computer-science/CS330/intro/", "Slide Breakdowns": "/Academics/computer-science/CS330/chapters-overview/", "Study Material": "/Academics/computer-science/CS330/study-material-overview/", "Slides": "/Academics/computer-science/CS330/slides/overview/", "Quizzes": "/Academics/computer-science/CS330/Quizez/overview/"},
    },
    "CS331": {
        "track": "Computer Science",
        "path": "docs/Academics/computer-science/CS331/intro.md",
        "url": "/course-cs331.html",
        "sections": {
            "Overview": "/Academics/computer-science/CS331/intro/",
            "Slide Breakdowns": "/Academics/computer-science/CS331/slide-breakdowns/overview/",
            "Summary": "/Academics/computer-science/CS331/summary/overview/",
            "Mindmap": "/Academics/computer-science/CS331/mindmap/overview/",
            "Slides": "/Academics/computer-science/CS331/slides/overview/",
        },
    },
    "CS340": {
        "track": "Computer Science",
        "path": "docs/Academics/computer-science/CS340/intro.md",
        "url": "/course-cs340.html",
        "sections": {
            "Overview": "/Academics/computer-science/CS340/intro/",
            "Slide Breakdowns": "/Academics/computer-science/CS340/chapters-overview/",
            "Study Material": "/Academics/computer-science/CS340/study-material-overview/",
            "Slides": "/Academics/computer-science/CS340/slides/overview/",
            "Quizzes": "/Academics/computer-science/CS340/quizez/overview/",
            "Mindmap": "/Academics/computer-science/CS340/Mindmap/overview/",
        },
    },
    "SE201": {
        "track": "Software Engineering",
        "path": "docs/Academics/software-engineering/SE201/intro.md",
        "url": "/course-se201.html",
        "sections": {
            "Overview": "/Academics/software-engineering/SE201/intro/",
            "Slide Breakdowns": "/Academics/software-engineering/SE201/chapters-overview/",
            "Study Material": "/Academics/software-engineering/SE201/study-material-overview/",
            "Slides": "/Academics/software-engineering/SE201/slides/overview/",
            "Quizzes": "/Academics/software-engineering/SE201/Quizez/overview/",
        },
    },
    "SE311": {
        "track": "Software Engineering",
        "path": "docs/Academics/software-engineering/SE311/intro.md",
        "url": "/course-se311.html",
        "sections": {
            "Overview": "/Academics/software-engineering/SE311/intro/",
            "Slide Breakdowns": "/Academics/software-engineering/SE311/chapters-overview/",
            "Study Material": "/Academics/software-engineering/SE311/study-material-overview/",
            "Slides": "/Academics/software-engineering/SE311/slides/overview/",
            "Quizzes": "/Academics/software-engineering/SE311/quizez/overview/",
        },
    },
    "CYS401": {
        "track": "Cybersecurity",
        "path": "docs/Academics/cyber-security/CYS401/intro.md",
        "url": "/course-cys401.html",
        "sections": {"Overview": "/Academics/cyber-security/CYS401/intro/", "Slide Breakdowns": "/Academics/cyber-security/CYS401/chapters-overview/", "Slides": "/Academics/cyber-security/CYS401/slides/overview/", "Quizzes": "/Academics/cyber-security/CYS401/Quizez/overview/"},
        "credits": "TBD",
        "prereq": "TBD",
    },
    "CYS402": {
        "track": "Cybersecurity",
        "url": "/Academics/cybersecurity/cys402/",
        "sections": {
            "Overview": "/Academics/cybersecurity/cys402/",
            "Slide Breakdowns": "/Academics/cybersecurity/cys402/slide-breakdowns/",
            "Slides": "/Academics/cybersecurity/cys402/slides/",
            "Study Material": "/Academics/cybersecurity/cys402/extra-resources/",
            "Quizzes": "/Academics/cybersecurity/cys402/quizzes/",
        },
        "title_override": "Cybersecurity",
        "credits": "TBD",
        "prereq": "TBD",
    },
    "CYS403": {
        "track": "Cybersecurity",
        "url": "/Academics/cybersecurity/cys403/",
        "sections": {
            "Overview": "/Academics/cybersecurity/cys403/",
            "Slide Breakdowns": "/Academics/cybersecurity/cys403/slide-breakdowns/",
            "Slides": "/Academics/cybersecurity/cys403/slides/",
            "Study Material": "/Academics/cybersecurity/cys403/extra-resources/",
            "Quizzes": "/Academics/cybersecurity/cys403/quizzes/",
        },
        "title_override": "Cybersecurity",
        "credits": "TBD",
        "prereq": "TBD",
    },
    "CYS406": {
        "track": "Cybersecurity",
        "url": "/Academics/cybersecurity/cys406/",
        "sections": {
            "Overview": "/Academics/cybersecurity/cys406/",
            "Slide Breakdowns": "/Academics/cybersecurity/cys406/slide-breakdowns/",
            "Slides": "/Academics/cybersecurity/cys406/slides/",
            "Study Material": "/Academics/cybersecurity/cys406/extra-resources/",
            "Quizzes": "/Academics/cybersecurity/cys406/quizzes/",
        },
        "title_override": "Cybersecurity",
        "credits": "TBD",
        "prereq": "TBD",
    },
    "ETHCS303": {
        "track": "Other Courses",
        "path": "docs/Academics/other/ethc303/overview.md",
        "url": "/course-ethcs303.html",
        "sections": {
            "Overview": "/Academics/other/ethc303/overview/",
            "Slide Breakdowns": "/Academics/other/ethc303/slide-breakdowns/intro/",
            "Slides": "/Academics/other/ethc303/slides/overview/",
            "Quizzes": "/Academics/other/ethc303/quizez/overview/",
            "Mindmaps": "/Academics/other/ethc303/mindmap/overview/",
            "Extra Resources": "/Academics/other/ethc303/extra-resources/overview/",
        },
        "credits": "3",
        "prereq": "Junior level",
    },
    "PHY205": {
        "track": "Other Courses",
        "path": "docs/Academics/other/phy205/overview.md",
        "url": "/course-phy205.html",
        "sections": {"Overview": "/Academics/other/phy205/overview/", "Slides": "/Academics/other/phy205/slides/overview/"},
        "status": "available",
    },
    "PHY105": {
        "track": "Other Courses",
        "path": "docs/academics/other-courses/phy105/",
        "url": "/academics/other-courses/phy105/",
        "sections": {
            "Overview": "/academics/other-courses/phy105/",
            "Slide Breakdowns": "/academics/other-courses/phy105/slide-breakdowns/",
            "Syllabus": "/academics/other-courses/phy105/syllabus/",
            "Slides": "/academics/other-courses/phy105/slides/",
            "Study Material": "/academics/other-courses/phy105/extra-resources/",
            "Quizzes": "/academics/other-courses/phy105/quizzes/",
        },
        "title_override": "Physics I",
        "credits": "4",
        "prereq": "TBD",
        "status": "available",
    },
    "SCI101": {
        "track": "Other Courses",
        "path": "docs/academics/other-courses/sci101/",
        "url": "/academics/other-courses/sci101/",
        "sections": {
            "Overview": "/academics/other-courses/sci101/",
            "Syllabus": "/academics/other-courses/sci101/syllabus/",
            "Slides": "/academics/other-courses/sci101/slides/",
            "Study Material": "/academics/other-courses/sci101/extra-resources/",
            "Quizzes": "/academics/other-courses/sci101/quizzes/",
        },
        "title_override": "Introduction to Physical Science",
        "credits": "3",
        "prereq": "None",
        "status": "available",
    },
    "ENG101": {
        "track": "Other Courses",
        "path": "docs/Academics/other/english/ENG101/overview.md",
        "url": "/course-eng101.html",
        "sections": {
            "Overview": "/Academics/other-courses/eng101/",
            "Slide Breakdowns": "/Academics/other-courses/eng101/slide-breakdowns/",
            "Slides": "/Academics/other-courses/eng101/slides/",
            "Study Material": "/Academics/other-courses/eng101/extra-resources/",
            "Quizzes": "/Academics/other-courses/eng101/quizzes/",
        },
        "title_override": "Intensive Writing",
        "code_override": "ENG101",
        "prereq": "None",
    },
    "ENG103": {
        "track": "Other Courses",
        "path": "old-design/docs/Academics/other/english/ENG103/overview.md",
        "url": "/Academics/other-courses/eng103/",
        "sections": {
            "Overview": "/Academics/other-courses/eng103/",
            "Study Material": "/Academics/other-courses/eng103/extra-resources/",
            "Quizzes": "/Academics/other-courses/eng103/quizzes/",
        },
        "title_override": "Research Writing Techniques",
        "credits": "3",
        "prereq": "ENG101",
    },
    "ISC113": {
        "track": "Other Courses",
        "path": "old-design/docs/Academics/other/Islamic/Islamic-113/Intro.md",
        "url": "/Academics/other-courses/isc113/",
        "sections": {
            "Overview": "/Academics/other-courses/isc113/",
            "Slide Breakdowns": "/Academics/other-courses/isc113/slide-breakdowns/",
            "Study Material": "/Academics/other-courses/isc113/extra-resources/",
            "Quizzes": "/Academics/other-courses/isc113/quizzes/",
        },
        "credits": "2",
        "prereq": "None",
    },
}


TRACKS: dict[str, dict[str, Any]] = {
    "computer-science": {
        "label": "COMPUTER SCIENCE",
        "title": "7 courses.<br>Structured, documented,<br>and ready to use.",
        "meta": ["CS Track", "7 Courses", "Programming", "Networks", "Databases"],
        "courses": ["CS101", "CS102", "CS210", "CS285", "CS330", "CS331", "CS340"],
        "url": "/track-computer-science.html",
    },
    "software-engineering": {
        "label": "SOFTWARE ENGINEERING",
        "title": "2 courses.<br>Requirements, design,<br>and engineering practice.",
        "meta": ["SE Track", "2 Courses", "Process", "Requirements", "Design"],
        "courses": ["SE201", "SE311"],
        "url": "/track-software-engineering.html",
    },
    "cybersecurity": {
        "label": "CYBERSECURITY",
        "title": "4 courses.<br>Security foundations,<br>threats, and defense.",
        "meta": ["Cyber Track", "4 Courses", "Security", "Risk", "Defense"],
        "courses": ["CYS401", "CYS402", "CYS403", "CYS406"],
        "url": "/track-cybersecurity.html",
    },
    "other-courses": {
        "label": "OTHER COURSES",
        "title": "5 courses.<br>One English hub,<br>and shared resources.",
        "meta": ["General Track", "5 Courses + English Hub", "Writing", "Ethics", "Science"],
        "courses": ["ETHCS303", "PHY105", "PHY205", "SCI101", "ISC113"],
        "url": "/track-other-courses.html",
    },
}


STATIC_OUTPUTS = {
    "home": "index.html",
    "academics": "Academics/index.html",
    "about": "about/index.html",
    "projects": "work/projects/index.html",
    "work": "work/index.html",
    "workshops": "workshops/index.html",
    "cyber_workshop": "workshops/cybersecurity-crash-course/index.html",
    "tutor_workshop": "workshops/student-tutor/index.html",
    "resources": "resources/index.html",
    "copyright": "policy/index.html",
}


def apply_generated_routes() -> None:
    for code, config in COURSES.items():
        config["url"] = f"/Academics/courses/{code.lower()}/"
    for slug, track in TRACKS.items():
        track["url"] = f"/Academics/tracks/{slug}/"


apply_generated_routes()

PROJECTS = [
    {
        "code": "SE311",
        "title": "Software Requirements Analysis - Sillah",
        "category": "Software Engineering",
        "filter": "software-engineering",
        "summary": "Formal requirements engineering project for Sillah, a preventive family cardiac health platform focused on early hereditary-risk awareness.",
        "scope": "Covers the requirements lifecycle from inception through elicitation, analysis, specification, validation, traceability, and change management.",
        "role": "Led requirements structure, documentation flow, modeling organization, and the prevention-oriented requirements baseline.",
        "stack": ["Requirements Engineering", "UML", "GRL", "Traceability", "MkDocs"],
        "outputs": ["Vision and scope", "Stakeholder analysis", "Use cases", "Functional and non-functional requirements", "Traceability baseline"],
        "links": [
            ("Documentation", "https://software-requirements-analysis.shoug-tech.com/"),
            ("Repository", "https://github.com/Shoug-Alomran/SE311-Software-Requirements-Analysis"),
        ],
    },
    {
        "code": "SE201",
        "title": "Sillah - Family Health Management System",
        "category": "Software Engineering",
        "filter": "software-engineering",
        "summary": "Preventive health management system helping Saudi families record medical history, receive risk alerts, and simulate preventive appointment workflows.",
        "scope": "Documents the full software engineering process: proposal, requirements, design, prototype, testing, and final reporting.",
        "role": "Owned system analysis, documentation structure, UML modeling support, and end-to-end project presentation.",
        "stack": ["Java", "UML", "Software Design", "Testing", "MkDocs"],
        "outputs": ["Requirements specification", "Architecture and UML diagrams", "Prototype and testing notes", "Documentation site", "App deployment"],
        "links": [
            ("Documentation", "https://sillah.shoug-tech.com/"),
            ("App", "https://sillah-app.shoug-tech.com/"),
            ("Repository", "https://github.com/Shoug-Alomran/SE201--Sillah-Project"),
        ],
    },
    {
        "code": "CS340",
        "title": "Full Stack Database Web Application",
        "category": "Computer Science",
        "filter": "computer-science",
        "summary": "Database-driven web application documented from project proposal through relational modeling, SQL implementation, backend logic, and frontend integration.",
        "scope": "Moves from EER conceptual design to logical schema, constraints, sample data, CRUD workflows, and application-layer documentation.",
        "role": "Designed core data model, organized documentation, integrated system phases, and handled deployment structure.",
        "stack": ["EER Modeling", "SQL", "Relational Schema", "Backend Logic", "MkDocs"],
        "outputs": ["Project overview", "EER diagram", "Relational schema", "SQL DDL and sample data", "Application layer documentation"],
        "links": [
            ("Documentation", "https://database.shoug-tech.com/"),
            ("Repository", "https://github.com/Shoug-Alomran/cs340-database-web-application"),
        ],
    },
    {
        "code": "CS330",
        "title": "Parallel Performance Evaluation in Linux",
        "category": "Computer Science",
        "filter": "computer-science",
        "summary": "Operating systems project evaluating process-based parallelism and measured performance behavior in a Linux environment.",
        "scope": "Uses fork-based process creation, controlled experiments, timing comparison, and reproducible technical documentation.",
        "role": "Structured experiments, documented execution behavior, and prepared the deployed project site.",
        "stack": ["Linux", "C", "Fork", "Performance Testing", "MkDocs"],
        "outputs": ["Experiment plan", "Parallel execution notes", "Performance measurements", "Analysis writeup", "Documentation site"],
        "links": [
            ("Documentation", "https://operating-systems.shoug-tech.com/"),
            ("Repository", "https://github.com/Shoug-Alomran/CS330-Parallel-Performance-Evaluation-in-Linux-Project"),
        ],
    },
    {
        "code": "CS285",
        "title": "Cryptography Project",
        "category": "Computer Science",
        "filter": "computer-science",
        "summary": "Secure key exchange implementation demonstrating Diffie-Hellman concepts through modular arithmetic and shared secret derivation.",
        "scope": "Connects number theory, key generation, exchange steps, and documented cryptographic workflow in a Java implementation.",
        "role": "Implemented the system and documented the cryptographic process from setup to shared secret output.",
        "stack": ["Java", "Diffie-Hellman", "Modular Arithmetic", "Key Exchange", "MkDocs"],
        "outputs": ["Algorithm explanation", "Java implementation", "Key generation workflow", "Security notes", "Documentation site"],
        "links": [
            ("Documentation", "https://secure-key-exchange.shoug-tech.com/"),
            ("Repository", "https://github.com/Shoug-Alomran/CS285-CryptographyProject"),
        ],
    },
    {
        "code": "CS210",
        "title": "Linked List Implementation and Runtime Analysis",
        "category": "Computer Science",
        "filter": "computer-science",
        "summary": "Data structures project using a custom linked list to process registration records and compare sorting algorithm behavior.",
        "scope": "Implements demand scoring, selection sort, insertion sort, merge sort, quick sort, theoretical analysis, and measured runtime comparison.",
        "role": "Implemented data-structure behavior, contributed runtime analysis, and documented the engineering and results.",
        "stack": ["Java", "Linked Lists", "Sorting Algorithms", "Big-O", "MkDocs"],
        "outputs": ["Custom linked list", "Demand scoring", "Sorting comparison", "Runtime measurements", "Source appendices"],
        "links": [
            ("Documentation", "https://linkedlist.shoug-tech.com/"),
            ("Repository", "https://github.com/Shoug-Alomran/CS210-Project-Linked-List-Implementation-and-Runtime-Analysis"),
        ],
    },
    {
        "code": "CS102",
        "title": "School Course Enrollment System",
        "category": "Computer Science",
        "filter": "computer-science",
        "summary": "Console-based university registration system with multiple user roles, file persistence, and modular object-oriented Java design.",
        "scope": "Handles role-based access, course registration workflows, persisted data, and a complete course-project documentation trail.",
        "role": "Designed and implemented the full system from scratch under difficult team conditions, then documented the result.",
        "stack": ["Java", "OOP", "File Persistence", "Role-Based Access", "MkDocs"],
        "outputs": ["Console application", "Role workflows", "Persistence model", "Implementation notes", "Documentation site"],
        "links": [
            ("Documentation", "https://school-course-enrolment-system.shoug-tech.com/"),
            ("Repository", "https://github.com/Shoug-Alomran/CS102-SchoolCourseEnrolmentSystem"),
        ],
    },
    {
        "code": "MATH221",
        "title": "Numerical Analysis Methods",
        "category": "Mathematics",
        "filter": "mathematics",
        "summary": "Numerical methods project implementing and analyzing computational techniques for approximation, error behavior, and convergence.",
        "scope": "Covers root-finding, interpolation, numerical differentiation and integration, stability, accuracy, and efficiency tradeoffs.",
        "role": "Implemented algorithms, analyzed error behavior, documented derivations, and organized computational results.",
        "stack": ["Numerical Methods", "Root Finding", "Interpolation", "Error Analysis", "MkDocs"],
        "outputs": ["Algorithm implementations", "Derivations", "Error analysis", "Computational results", "Documentation site"],
        "links": [
            ("Documentation", "https://numerical-analysis.shoug-tech.com/"),
            ("Repository", "https://github.com/Shoug-Alomran/Math221_Numerical-Analysis"),
        ],
    },
]

FEATURED_WORK = [
    {
        "code": "SE311",
        "title": "Software Requirements Analysis - Sillah",
        "category": "Software Engineering",
        "url": "https://software-requirements-analysis.shoug-tech.com/",
        "image": "/assets/project-previews/se311-sillah.jpg",
    },
    {
        "code": "CS340",
        "title": "Full Stack Database Web Application",
        "category": "Computer Science",
        "url": "https://database.shoug-tech.com/",
        "image": "/assets/project-previews/cs340-database.png",
    },
    {
        "code": "SE201",
        "title": "Sillah - Family Health Management System",
        "category": "Software Engineering",
        "url": "https://sillah.shoug-tech.com/",
        "image": "/assets/project-previews/se201-sillah.png",
    },
]


WORKSHOP_SECTIONS: dict[str, dict[str, Any]] = {
    "cyber_workshop": {
        "base": "/workshops/cybersecurity-crash-course/",
        "title": "Cybersecurity Crash Course",
        "sections": {
            "SCHEDULE &amp; AGENDA": ("schedule-agenda", "docs/career-development/Workshops/cybersecurity-crash-course/agenda.md"),
            "TOPICS &amp; LEARNING OUTCOMES": ("topics-learning-outcomes", "docs/career-development/Workshops/cybersecurity-crash-course/topics.md"),
            "HANDOUTS": ("handouts", "docs/career-development/Workshops/cybersecurity-crash-course/handouts.md"),
            "LABS &amp; BANDIT NOTES": ("labs-bandit-notes", "docs/career-development/Workshops/cybersecurity-crash-course/bandit-notes.md"),
            "REFLECTION &amp; IMPACT": ("reflection-impact", "docs/career-development/Workshops/cybersecurity-crash-course/reflection.md"),
        },
    },
    "tutor_workshop": {
        "base": "/workshops/student-tutor/",
        "title": "My Journey as a Student Tutor",
        "sections": {
            "AGENDA": ("agenda", "docs/career-development/Workshops/My-Journey-as-a-Student-Tutor/agenda.md"),
            "TIMELINE": ("timeline", "docs/career-development/Workshops/My-Journey-as-a-Student-Tutor/timeline.md"),
            "SKILLS": ("skills", "docs/career-development/Workshops/My-Journey-as-a-Student-Tutor/skills.md"),
            "GROWTH": ("growth", "docs/career-development/Workshops/My-Journey-as-a-Student-Tutor/growth.md"),
            "FEEDBACK": ("feedback", "docs/career-development/Workshops/My-Journey-as-a-Student-Tutor/feedback.md"),
            "TIPS": ("tips", "docs/career-development/Workshops/My-Journey-as-a-Student-Tutor/tips.md"),
            "REFLECTION": ("reflection", "docs/career-development/Workshops/My-Journey-as-a-Student-Tutor/reflection.md"),
            "VIDEO": ("video", "docs/career-development/Workshops/My-Journey-as-a-Student-Tutor/video.md"),
        },
    },
}


def workshop_section_url(workshop_key: str, title: str) -> str:
    workshop = WORKSHOP_SECTIONS[workshop_key]
    slug, _ = workshop["sections"][title]
    return f'{workshop["base"]}{slug}/'


COMMON_LINKS = {
    "Home": "/",
    "Academics": "/Academics/",
    "Work": "/work/",
    "Work Experience": "/work/",
    "Workshops": "/workshops/",
    "Workshops & Speaking": "/workshops/",
    "Resources": "/resources/",
    "About": "/about/",
    "About Me": "/about/",
    "Projects": "/work/projects/",
    "View Projects": "/work/projects/",
    "View Services": "/work/",
    "Resume": "/career-development/CV.html",
    "Blueprint Studio": "https://blueprint.shoug-tech.com/",
    "Visit Blueprint": "https://blueprint.shoug-tech.com/",
    "Copyright & Usage Policy": "/policy/",
}


COMMON_HEADER_CSS = r"""
        body {
            padding-top: 68px;
        }

        body:has(.app-layout),
        body:has(.layout-wrapper),
        body:has(.sys-layout),
        body:has(.page-shell) {
            height: auto !important;
            min-height: 100vh;
            display: block !important;
            overflow-y: auto !important;
        }

        body:has(.app-layout) .app-layout,
        body:has(.layout-wrapper) .layout-wrapper {
            min-height: calc(100vh - 68px);
            height: auto !important;
            overflow: visible !important;
            align-items: stretch;
        }

        body:has(.app-layout) .main-wrapper,
        body:has(.layout-wrapper) .main-wrapper {
            min-height: calc(100vh - 68px);
            overflow: visible !important;
        }

        body:has(.app-layout) .sys-main,
        body:has(.layout-wrapper) .sys-main {
            min-height: calc(100vh - 68px);
            overflow: visible !important;
        }

        body:has(.app-layout) .content-scroll-area,
        body:has(.layout-wrapper) .content-scroll-area {
            flex: initial !important;
            overflow: visible !important;
        }

        body:has(.layout-wrapper) .content-area,
        body:has(.app-layout) .content-area,
        body:has(.app-layout) .page-content,
        body:has(.layout-wrapper) .page-content,
        body:has(.layout-wrapper) .embed-area-wrapper,
        body:has(.app-layout) .embed-container {
            overflow: visible !important;
            min-height: auto !important;
        }

        body:has(.layout-wrapper) .content-area {
            flex: 1 1 auto;
            min-width: 0;
        }

        body:has(.layout-wrapper) .embed-area-wrapper {
            flex: initial !important;
        }

        body:has(.app-layout) .sidebar,
        body:has(.layout-wrapper) .sidebar {
            position: sticky;
            top: 68px;
            height: calc(100vh - 68px) !important;
            align-self: flex-start;
        }

        @media (min-width: 761px) {
            body:has(.app-layout),
            body:has(.layout-wrapper) {
                overflow-y: visible !important;
            }

            body:has(.app-layout) .app-layout,
            body:has(.layout-wrapper) .layout-wrapper {
                margin-top: -68px !important;
            }

            body:has(.app-layout) .app-layout > .academic-sidebar,
            body:has(.layout-wrapper) .layout-wrapper > .academic-sidebar {
                top: 68px !important;
            }

            body:has(.app-layout) .app-layout > .main-wrapper,
            body:has(.app-layout) .app-layout > .sys-main,
            body:has(.layout-wrapper) .layout-wrapper > .main-wrapper,
            body:has(.layout-wrapper) .layout-wrapper > .sys-main,
            body:has(.layout-wrapper) .layout-wrapper > .content-area {
                padding-top: 68px !important;
            }
        }

        body:has(.app-layout) .shoug-site-footer,
        body:has(.layout-wrapper) .shoug-site-footer {
            margin-top: 0;
        }

        .shoug-site-header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 68px;
            z-index: 10000;
            background: rgba(5, 5, 8, 0.92);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
        }

        .shoug-header-inner {
            width: min(1440px, calc(100% - 48px));
            height: 100%;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 28px;
        }

        .shoug-header-logo {
            color: #f8f7fb;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.86rem;
            font-weight: 800;
            letter-spacing: 0.16em;
            text-decoration: none;
            white-space: nowrap;
        }

        .shoug-header-nav {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: clamp(14px, 2vw, 30px);
            flex: 1;
        }

        .shoug-header-nav a {
            color: #8f8b9a;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.13em;
            text-transform: uppercase;
            text-decoration: none;
            transition: color 160ms ease, text-shadow 160ms ease;
        }

        .shoug-header-nav a:hover,
        .shoug-header-nav a.active {
            color: #b829ea;
            text-shadow: 0 0 14px rgba(184, 41, 234, 0.35);
        }

        .shoug-header-actions {
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: 10px;
        }

        .shoug-header-menu-btn,
        .shoug-directory-btn {
            min-width: 34px;
            height: 34px;
            display: none;
            align-items: center;
            justify-content: center;
            border: 1px solid rgba(184, 41, 234, 0.45);
            background: rgba(184, 41, 234, 0.08);
            color: #f8f7fb;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.62rem;
            font-weight: 800;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            cursor: pointer;
        }

        .shoug-header-backdrop {
            display: none;
        }

        .shoug-icon-btn,
        .shoug-lang-btn,
        .shoug-theme-btn {
            width: 34px;
            height: 34px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border: 1px solid rgba(255, 255, 255, 0.12);
            background: rgba(255, 255, 255, 0.02);
            color: #f8f7fb;
            text-decoration: none;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.64rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            cursor: pointer;
            transition: border-color 160ms ease, color 160ms ease, background 160ms ease;
        }

        .shoug-icon-btn:hover,
        .shoug-lang-btn:hover,
        .shoug-theme-btn:hover {
            color: #b829ea;
            border-color: rgba(184, 41, 234, 0.55);
            background: rgba(184, 41, 234, 0.08);
        }

        .shoug-icon-btn svg,
        .shoug-theme-btn svg {
            width: 15px;
            height: 15px;
            display: block;
        }

        .shoug-contact-btn {
            height: 34px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0 16px;
            border: 1px solid #ff2a4b;
            background: transparent;
            color: #ff2a4b;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.68rem;
            font-weight: 800;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            text-decoration: none;
            transition: background 160ms ease, color 160ms ease, box-shadow 160ms ease;
        }

        .shoug-contact-btn:hover {
            background: #ff2a4b;
            color: #050508;
            box-shadow: 0 0 24px rgba(255, 42, 75, 0.28);
        }

        .shoug-site-footer {
            position: relative;
            z-index: 5;
            width: 100%;
            display: block !important;
            box-sizing: border-box;
            margin-top: 80px;
            padding: 64px clamp(28px, 5vw, 96px) 52px;
            background: #050508;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            color: #f8f7fb;
            font-family: Inter, sans-serif;
        }

        .shoug-footer-grid {
            width: min(1440px, 100%);
            margin: 0 auto;
            display: grid;
            grid-template-columns: minmax(260px, 1.5fr) repeat(3, minmax(150px, 0.8fr));
            gap: clamp(32px, 5vw, 92px);
            align-items: start;
        }

        .shoug-footer-label {
            margin-bottom: 16px;
            color: #ff2a4b;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.68rem;
            font-weight: 800;
            letter-spacing: 0.18em;
            text-transform: uppercase;
        }

        .shoug-footer-brand {
            color: #f8f7fb;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.92rem;
            font-weight: 800;
            letter-spacing: 0.18em;
            text-decoration: none;
        }

        .shoug-footer-text,
        .shoug-footer-link,
        .shoug-footer-meta {
            display: block;
            color: #8f8b9a;
            font-family: Inter, sans-serif;
            font-size: 0.86rem;
            line-height: 1.85;
            text-decoration: none;
            max-width: 34ch;
        }

        .shoug-footer-link {
            transition: color 160ms ease;
            width: fit-content;
        }

        .shoug-footer-link:hover {
            color: #b829ea;
        }

        .shoug-footer-meta {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
        }

        .tree-course-link,
        a.tree-file,
        a.tree-row,
        .sys-sidebar a {
            color: inherit;
            text-decoration: none;
        }

        .tree-course-link {
            display: inline-block;
            width: 100%;
        }

        .academic-sidebar {
            width: 280px;
            flex: 0 0 280px;
            display: flex !important;
            flex-direction: column;
            background: var(--bg-surface, #0a0514);
            border-right: 1px solid var(--border-dim, rgba(184, 41, 234, 0.24));
            color: var(--text-dim, #8f8b9a);
            font-family: 'JetBrains Mono', monospace;
            z-index: 20;
            transition: width 180ms ease, flex-basis 180ms ease;
        }

        .academic-sidebar .sidebar-header {
            min-height: 56px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
            padding: 0 20px;
            border-bottom: 1px solid var(--border-dim, rgba(184, 41, 234, 0.24));
            color: var(--text-dim, #8f8b9a);
            font-size: 0.66rem;
            font-weight: 700;
            letter-spacing: 0.18em;
            text-transform: uppercase;
        }

        .academic-sidebar .file-tree {
            display: block !important;
            flex: 1 1 auto;
            padding: 28px 0 34px;
            overflow-y: auto;
            max-height: calc(100vh - 124px);
        }

        .sidebar-collapse-button {
            appearance: none;
            width: 30px;
            height: 30px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border: 1px solid rgba(184, 41, 234, 0.34);
            background: rgba(184, 41, 234, 0.06);
            color: var(--brand-purple, #b829ea);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.78rem;
            font-weight: 800;
            cursor: pointer;
            transition: background 160ms ease, border-color 160ms ease, color 160ms ease;
        }

        .sidebar-collapse-button:hover {
            border-color: var(--brand-purple, #b829ea);
            background: rgba(184, 41, 234, 0.14);
            color: var(--text-main, #f8f7fb);
        }

        body.sidebar-collapsed .academic-sidebar {
            width: 58px;
            flex-basis: 58px;
            overflow: hidden;
        }

        body.sidebar-collapsed .academic-sidebar .sidebar-title,
        body.sidebar-collapsed .academic-sidebar .file-tree {
            display: none !important;
        }

        body.sidebar-collapsed .academic-sidebar .sidebar-header {
            justify-content: center;
            padding-inline: 0;
        }

        body.sidebar-collapsed .sidebar-collapse-button::before {
            content: ">";
        }

        body.sidebar-collapsed .sidebar-collapse-button .collapse-icon {
            display: none;
        }

        .academic-sidebar ul {
            list-style: none;
            margin: 0;
            padding: 0;
        }

        .academic-sidebar .tree-node {
            display: block !important;
            align-items: initial !important;
            gap: 0 !important;
            cursor: default !important;
            color: inherit !important;
        }

        .academic-sidebar .tree-node:hover {
            color: inherit !important;
        }

        .academic-sidebar .tree-item {
            min-height: 28px;
            display: flex;
            align-items: center;
            padding: 4px 20px;
            color: var(--text-dim, #8f8b9a);
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            line-height: 1.45;
        }

        .academic-sidebar .root-dir {
            color: var(--text-main, #f8f7fb);
            margin-bottom: 12px;
        }

        .academic-sidebar .tree-course-link,
        .academic-sidebar .tree-file {
            color: inherit;
            text-decoration: none;
            width: 100%;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: color 160ms ease, background 160ms ease, text-shadow 160ms ease;
        }

        .academic-sidebar .tree-toggle-button {
            appearance: none;
            border: 0;
            background: transparent;
            padding: 0;
            font: inherit;
            text-align: left;
            cursor: pointer;
        }

        .academic-sidebar .tree-course-link:hover,
        .academic-sidebar .tree-file:hover {
            color: var(--brand-purple, #b829ea);
        }

        .academic-sidebar .tree-toggle {
            color: var(--brand-purple, #b829ea);
        }

        .academic-sidebar .cyber-track {
            color: var(--alert-red, #ff2a4b);
        }

        .academic-sidebar .tree-children {
            display: none;
            margin: 0 0 10px 20px;
            padding-left: 8px;
            border-left: 1px solid rgba(184, 41, 234, 0.28);
        }

        .academic-sidebar .tree-children.is-open,
        .academic-sidebar .section-children {
            display: block;
        }

        .academic-sidebar .section-children {
            margin-left: 54px;
            margin-bottom: 12px;
        }

        .academic-sidebar .item-children {
            display: block;
            margin-left: 44px;
            margin-bottom: 12px;
            padding-left: 10px;
            max-height: 360px;
            overflow-y: auto;
            border-left-color: rgba(184, 41, 234, 0.42);
        }

        .academic-sidebar .section-children .tree-item {
            padding-left: 14px;
            font-size: 0.68rem;
        }

        .academic-sidebar .tree-viewer {
            font-size: 0.58rem;
            line-height: 1.42;
            letter-spacing: 0.035em;
            text-transform: none;
        }

        .academic-sidebar .tree-viewer .tree-file {
            display: block;
            white-space: normal;
        }

        .academic-sidebar .file-active {
            color: var(--brand-purple, #b829ea);
            background: rgba(184, 41, 234, 0.08);
            text-shadow: 0 0 16px rgba(184, 41, 234, 0.3);
            border-left: 2px solid var(--brand-purple, #b829ea);
        }

        .academic-sidebar .status-dot {
            width: 6px;
            height: 6px;
            flex: 0 0 6px;
            background: var(--alert-red, #ff2a4b);
            box-shadow: 0 0 12px rgba(255, 42, 75, 0.65);
            display: inline-block;
        }

        [data-card-url] {
            cursor: pointer;
        }

        body.shoug-light-mode {
            --bg: #f6f4fb;
            --bg-void: #f6f4fb;
            --bg-surface: #ffffff;
            --bg-elevated: #ebe7f4;
            --surface: rgba(255, 255, 255, 0.88);
            --text-main: #16111f;
            --text-primary: #16111f;
            --text-bright: #16111f;
            --text-high: #241a31;
            --text-secondary: #534a61;
            --text-med: #534a61;
            --text-dim: #6d6478;
            --text-dimmed: #6d6478;
            --text-muted: #776d85;
            --text-low: #81778e;
            --border: rgba(22, 17, 31, 0.14);
            --border-color: rgba(22, 17, 31, 0.14);
            --border-dim: rgba(22, 17, 31, 0.1);
            --border-subtle: rgba(22, 17, 31, 0.1);
            --border-main: rgba(22, 17, 31, 0.18);
            --border-med: rgba(22, 17, 31, 0.2);
            --border-medium: rgba(22, 17, 31, 0.2);
            --border-hard: rgba(22, 17, 31, 0.26);
            --grid-line: rgba(184, 41, 234, 0.08);
            --grid-pattern: rgba(184, 41, 234, 0.08);
            background: #f6f4fb !important;
            color: #16111f !important;
        }

        body.shoug-light-mode canvas,
        body.shoug-light-mode .bg-canvas,
        body.shoug-light-mode #matrix-canvas,
        body.shoug-light-mode #webgl-canvas {
            opacity: 0.18;
        }

        body.shoug-light-mode .shoug-site-header,
        body.shoug-light-mode .shoug-site-footer {
            background: rgba(246, 244, 251, 0.94);
            color: #16111f;
            border-color: rgba(22, 17, 31, 0.14);
        }

        body.shoug-light-mode .shoug-header-logo,
        body.shoug-light-mode .shoug-icon-btn,
        body.shoug-light-mode .shoug-lang-btn,
        body.shoug-light-mode .shoug-theme-btn,
        body.shoug-light-mode .shoug-footer-brand {
            color: #16111f;
        }

        body.shoug-light-mode .shoug-icon-btn,
        body.shoug-light-mode .shoug-lang-btn,
        body.shoug-light-mode .shoug-theme-btn {
            border-color: rgba(22, 17, 31, 0.16);
            background: rgba(255, 255, 255, 0.66);
        }

        body.shoug-light-mode .shoug-footer-text,
        body.shoug-light-mode .shoug-footer-link,
        body.shoug-light-mode .shoug-footer-meta,
        body.shoug-light-mode .shoug-header-nav a {
            color: #6d6478;
        }

        html[dir="rtl"] .shoug-header-inner,
        html[dir="rtl"] .shoug-footer-grid {
            direction: rtl;
        }

        html[dir="rtl"] .shoug-header-actions {
            flex-direction: row-reverse;
        }

        .layout-wrapper,
        .app-layout,
        .content-area,
        .page-content,
        .embed-area-wrapper,
        .embed-container,
        main,
        section,
        article {
            max-width: 100%;
            min-width: 0;
        }

        img,
        svg,
        video,
        canvas,
        iframe {
            max-width: 100%;
        }

        @media (max-width: 980px) {
            .shoug-site-header {
                height: auto;
            }

            .shoug-header-inner {
                width: min(100% - 28px, 720px);
                min-height: 68px;
                flex-wrap: wrap;
                padding: 12px 0;
                gap: 14px;
            }

            .shoug-header-nav {
                order: 3;
                width: 100%;
                justify-content: flex-start;
                overflow-x: auto;
                padding-bottom: 4px;
            }

            .shoug-footer-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }

        @media (max-width: 760px) {
            body {
                overflow-x: hidden;
            }

            .shoug-site-header {
                min-height: 68px;
            }

            .shoug-header-inner {
                width: calc(100% - 28px);
                flex-wrap: nowrap;
                gap: 8px;
                padding: 8px 0;
            }

            .shoug-header-logo {
                max-width: 38vw;
                overflow: hidden;
                text-overflow: ellipsis;
                font-size: 0.74rem;
                letter-spacing: 0.12em;
            }

            .shoug-header-menu-btn {
                display: inline-flex;
            }

            body:has(.academic-sidebar) .shoug-directory-btn {
                display: inline-flex;
            }

            .shoug-header-actions {
                gap: 6px;
                margin-left: auto;
            }

            .shoug-icon-btn,
            .shoug-lang-btn,
            .shoug-theme-btn {
                width: 32px;
                height: 32px;
                flex: 0 0 32px;
            }

            .shoug-contact-btn {
                height: 32px;
                padding-inline: 10px;
                font-size: 0.58rem;
                letter-spacing: 0.12em;
            }

            .shoug-header-nav {
                position: fixed;
                left: 14px;
                right: 14px;
                top: 74px;
                z-index: 10020;
                width: auto;
                max-height: calc(100vh - 96px);
                display: grid !important;
                grid-template-columns: 1fr;
                gap: 0;
                overflow: auto;
                padding: 10px;
                border: 1px solid rgba(184, 41, 234, 0.38);
                background: rgba(5, 5, 8, 0.98);
                box-shadow: 0 22px 70px rgba(0, 0, 0, 0.62);
                opacity: 0;
                pointer-events: none;
                transform: translateY(-8px);
                transition: opacity 160ms ease, transform 160ms ease;
            }

            body.mobile-nav-open .shoug-header-nav {
                opacity: 1;
                pointer-events: auto;
                transform: translateY(0);
            }

            .shoug-header-nav a {
                min-height: 44px;
                display: flex;
                align-items: center;
                padding: 0 14px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
                font-size: 0.76rem;
            }

            .shoug-header-nav a:last-child {
                border-bottom: 0;
            }

            .shoug-header-backdrop {
                position: fixed;
                inset: 68px 0 0;
                z-index: 10010;
                background: rgba(0, 0, 0, 0.54);
                backdrop-filter: blur(2px);
                -webkit-backdrop-filter: blur(2px);
            }

            body.mobile-nav-open .shoug-header-backdrop,
            body.sidebar-open .shoug-header-backdrop {
                display: block;
            }

            .layout-wrapper,
            .app-layout {
                width: 100%;
                overflow-x: hidden !important;
            }

            .content-area,
            .page-content,
            .content-scroll-area {
                width: 100%;
                overflow-x: hidden !important;
            }

            .top-bar,
            .content-topbar {
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
            }

            .page-header,
            .content-header,
            .content-section,
            .embed-area-wrapper {
                padding-left: 16px !important;
                padding-right: 16px !important;
            }

            .embed-container {
                width: 100%;
                overflow: hidden;
            }

            .embed-container iframe,
            .embed-frame {
                width: 100% !important;
                min-height: 72vh !important;
                height: 72vh !important;
            }

            .hero {
                min-height: auto !important;
                padding-top: clamp(72px, 18vh, 132px) !important;
                padding-left: 24px !important;
                padding-right: 24px !important;
            }

            .hero-bg-glow {
                left: 0 !important;
                width: 100vw !important;
                max-width: 100vw !important;
                overflow: hidden !important;
            }

            .ticker-wrap {
                max-width: 100vw !important;
                overflow: hidden !important;
                contain: paint;
            }

            .ticker-content {
                width: 100% !important;
                max-width: 100% !important;
                overflow: hidden !important;
            }

            .hero-ctas {
                flex-wrap: wrap;
            }

            .work-grid,
            .projects-grid,
            .project-grid,
            .explore-grid,
            .panels-grid,
            .proof,
            [class*="cards-grid"],
            [class*="card-grid"] {
                grid-template-columns: 1fr !important;
            }

            .work-card,
            .project-card,
            .card,
            [class*="-card"] {
                max-width: 100% !important;
                min-width: 0 !important;
                overflow-wrap: anywhere;
            }

            table {
                display: block;
                max-width: 100%;
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
            }
        }

        @media (max-width: 640px) {
            .shoug-site-footer {
                padding-inline: 22px;
            }

            .shoug-footer-grid {
                grid-template-columns: 1fr;
            }

            .shoug-header-logo {
                max-width: 32vw;
            }

            .shoug-header-actions a[aria-label="GitHub"],
            .shoug-header-actions a[aria-label="LinkedIn"],
            .shoug-header-actions a[aria-label="جيت هب"],
            .shoug-header-actions a[aria-label="لينكدإن"] {
                display: none;
            }
        }
"""


COMMON_HEADER = """
    <header class="shoug-site-header">
        <div class="shoug-header-inner">
            <a class="shoug-header-logo" href="/">SHOUG.TECH</a>
            <nav class="shoug-header-nav" aria-label="Primary">
                <a href="/">Home</a>
                <a href="/Academics/">Academics</a>
                <a href="/work/">Work</a>
                <a href="/workshops/">Workshops</a>
                <a href="/resources/">Resources</a>
                <a href="/about/">About</a>
            </nav>
            <div class="shoug-header-actions">
                <button class="shoug-header-menu-btn" type="button" aria-label="Open site menu" aria-controls="shoug-mobile-nav" aria-expanded="false">Menu</button>
                <button class="shoug-directory-btn" type="button" aria-label="Open academic directory" aria-expanded="false">Dir</button>
                <a class="shoug-icon-btn" href="/?q=" aria-label="Search">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square"><circle cx="11" cy="11" r="7"></circle><path d="m20 20-4-4"></path></svg>
                </a>
                <a class="shoug-icon-btn" href="https://github.com/Shoug-Alomran" aria-label="GitHub">
                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 .5A12 12 0 0 0 8.2 23.9c.6.1.8-.3.8-.6v-2.1c-3.3.7-4-1.4-4-1.4-.5-1.3-1.2-1.7-1.2-1.7-1-.7.1-.7.1-.7 1.1.1 1.8 1.2 1.8 1.2 1 1.8 2.7 1.3 3.3 1 .1-.7.4-1.3.7-1.6-2.6-.3-5.4-1.3-5.4-5.9 0-1.3.5-2.4 1.2-3.2-.1-.3-.5-1.5.1-3.2 0 0 1-.3 3.3 1.2a11.5 11.5 0 0 1 6 0C17.7 4.4 18.7 4.7 18.7 4.7c.6 1.7.2 2.9.1 3.2.8.8 1.2 1.9 1.2 3.2 0 4.6-2.8 5.6-5.4 5.9.4.4.8 1.1.8 2.2v4.1c0 .3.2.7.8.6A12 12 0 0 0 12 .5Z"></path></svg>
                </a>
                <a class="shoug-icon-btn" href="https://www.linkedin.com/in/shoug-alomran/" aria-label="LinkedIn">
                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M20.4 20.4h-3.6v-5.6c0-1.3 0-3-1.9-3s-2.1 1.4-2.1 2.9v5.7H9.3V9h3.4v1.6h.1c.5-.9 1.6-1.9 3.4-1.9 3.6 0 4.3 2.4 4.3 5.5v6.2ZM5.3 7.4a2.1 2.1 0 1 1 0-4.1 2.1 2.1 0 0 1 0 4.1Zm1.8 13H3.6V9h3.5v11.4ZM22.2 0H1.8C.8 0 0 .8 0 1.7v20.5C0 23.2.8 24 1.8 24h20.4c1 0 1.8-.8 1.8-1.8V1.7C24 .8 23.2 0 22.2 0Z"></path></svg>
                </a>
                <button class="shoug-theme-btn" type="button" aria-label="Toggle dark and light mode">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square"><circle cx="12" cy="12" r="4"></circle><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"></path></svg>
                </button>
                <button class="shoug-lang-btn" type="button" data-lang-toggle aria-label="Switch to Arabic">AR</button>
                <a class="shoug-contact-btn" href="mailto:shoug.alomran@shoug-tech.com">Contact</a>
            </div>
        </div>
        <div class="shoug-header-backdrop" data-mobile-overlay></div>
    </header>
"""


COMMON_FOOTER = """
    <footer class="shoug-site-footer">
        <div class="shoug-footer-grid">
            <div>
                <a class="shoug-footer-brand" href="/">SHOUG.TECH</a>
                <p class="shoug-footer-text">Software Engineering and Cybersecurity portfolio. Documenting projects, study systems, workshops, and technical resources.</p>
            </div>
            <div>
                <div class="shoug-footer-label">Navigate</div>
                <a class="shoug-footer-link" href="/Academics/">Academics</a>
                <a class="shoug-footer-link" href="/work/projects/">Projects</a>
                <a class="shoug-footer-link" href="/workshops/">Workshops</a>
                <a class="shoug-footer-link" href="/resources/">Resources</a>
            </div>
            <div>
                <div class="shoug-footer-label">Connect</div>
                <a class="shoug-footer-link" href="https://www.linkedin.com/in/shoug-alomran/">LinkedIn</a>
                <a class="shoug-footer-link" href="https://github.com/Shoug-Alomran">GitHub</a>
                <a class="shoug-footer-link" href="mailto:shoug.alomran@shoug-tech.com">Email</a>
                <a class="shoug-footer-link" href="https://blueprint.shoug-tech.com/">Blueprint Studio</a>
            </div>
            <div>
                <div class="shoug-footer-label">System</div>
                <span class="shoug-footer-meta">Status: Operational</span>
                <span class="shoug-footer-meta">Protocol: HTTPS</span>
                <a class="shoug-footer-link" href="/policy/">Copyright &amp; Policy</a>
            </div>
        </div>
    </footer>
"""


COMMON_SCRIPT = """
    <script src="/javascripts/arabic-localization.js"></script>
    <script>
        (function () {
            function normalizeLabel(value) {
                return String(value || '').split('[').join('').split(']').join('').replace(/\\s+/g, ' ').trim().toLowerCase();
            }

            function initialLang() {
                var requestedLang = new URLSearchParams(window.location.search).get('lang');
                if (requestedLang === 'ar' || requestedLang === 'en') return requestedLang;
                var savedLang = localStorage.getItem('shoug-lang');
                if (savedLang === 'ar' || savedLang === 'en') return savedLang;
                var pageLang = String(document.documentElement.lang || '').toLowerCase();
                if (pageLang.indexOf('ar') === 0) return 'ar';
                return 'en';
            }

            function syncLanguagePanels(lang) {
                var panels = Array.prototype.slice.call(document.querySelectorAll('[data-lang-panel]'));
                if (!panels.length) return;
                var hasRequestedPanel = panels.some(function (panel) {
                    return panel.getAttribute('data-lang-panel') === lang;
                });
                panels.forEach(function (panel) {
                    panel.hidden = hasRequestedPanel && panel.getAttribute('data-lang-panel') !== lang;
                });
            }

            var toggle = document.querySelector('.shoug-theme-btn');
            var saved = localStorage.getItem('shoug-theme');
            if (saved === 'light') document.body.classList.add('shoug-light-mode');
            if (toggle) {
                toggle.addEventListener('click', function () {
                    document.body.classList.toggle('shoug-light-mode');
                    localStorage.setItem('shoug-theme', document.body.classList.contains('shoug-light-mode') ? 'light' : 'dark');
                });
            }

            var mobileMenuButton = document.querySelector('.shoug-header-menu-btn');
            var directoryButton = document.querySelector('.shoug-directory-btn');
            var mobileOverlay = document.querySelector('[data-mobile-overlay]');
            var primaryNav = document.querySelector('.shoug-header-nav');
            if (primaryNav && !primaryNav.id) primaryNav.id = 'shoug-mobile-nav';

            function setMobileMenu(open) {
                document.body.classList.toggle('mobile-nav-open', open);
                if (mobileMenuButton) {
                    mobileMenuButton.setAttribute('aria-expanded', open ? 'true' : 'false');
                    mobileMenuButton.setAttribute('aria-label', open ? 'Close site menu' : 'Open site menu');
                }
            }

            function setDirectory(open) {
                document.body.classList.toggle('sidebar-open', open);
                if (directoryButton) {
                    directoryButton.setAttribute('aria-expanded', open ? 'true' : 'false');
                    directoryButton.setAttribute('aria-label', open ? 'Close academic directory' : 'Open academic directory');
                }
            }

            if (mobileMenuButton) {
                mobileMenuButton.addEventListener('click', function () {
                    var next = !document.body.classList.contains('mobile-nav-open');
                    setDirectory(false);
                    setMobileMenu(next);
                });
            }

            if (directoryButton) {
                if (!document.querySelector('.academic-sidebar')) directoryButton.hidden = true;
                directoryButton.addEventListener('click', function () {
                    var next = !document.body.classList.contains('sidebar-open');
                    setMobileMenu(false);
                    setDirectory(next);
                });
            }

            if (mobileOverlay) {
                mobileOverlay.addEventListener('click', function () {
                    setMobileMenu(false);
                    setDirectory(false);
                });
            }

            document.addEventListener('keydown', function (event) {
                if (event.key === 'Escape') {
                    setMobileMenu(false);
                    setDirectory(false);
                }
            });

            document.querySelectorAll('.shoug-header-nav a, .academic-sidebar a').forEach(function (link) {
                link.addEventListener('click', function () {
                    setMobileMenu(false);
                    setDirectory(false);
                });
            });

            document.querySelectorAll('[data-tree-toggle]').forEach(function (button) {
                button.addEventListener('click', function () {
                    var target = document.getElementById(button.getAttribute('data-tree-toggle'));
                    if (!target) return;
                    var isOpen = target.classList.toggle('is-open');
                    button.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
                    var marker = button.querySelector('.tree-toggle');
                    if (marker) marker.textContent = isOpen ? '[-]' : '[+]';
                });
            });

            var sidebarCollapse = document.querySelector('[data-sidebar-collapse]');
            document.body.classList.remove('sidebar-collapsed');
            function syncSidebarCollapseLabel() {
                if (!sidebarCollapse) return;
                var collapsed = document.body.classList.contains('sidebar-collapsed');
                sidebarCollapse.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
                sidebarCollapse.setAttribute('aria-label', collapsed ? 'Expand side navigation' : 'Collapse side navigation');
                sidebarCollapse.setAttribute('title', collapsed ? 'Expand navigation' : 'Collapse navigation');
            }
            syncSidebarCollapseLabel();
            if (sidebarCollapse) {
                sidebarCollapse.addEventListener('click', function () {
                    document.body.classList.toggle('sidebar-collapsed');
                    syncSidebarCollapseLabel();
                });
            }

            document.querySelectorAll('[data-card-url]').forEach(function (card) {
                card.setAttribute('role', 'link');
                card.setAttribute('tabindex', '0');
                card.addEventListener('click', function () {
                    window.location.href = card.getAttribute('data-card-url');
                });
                card.addEventListener('keydown', function (event) {
                    if (event.key === 'Enter' || event.key === ' ') {
                        event.preventDefault();
                        window.location.href = card.getAttribute('data-card-url');
                    }
                });
            });

            var langToggle = document.querySelector('[data-lang-toggle]');
            var labels = {
                en: {
                    htmlLang: 'en',
                    dir: 'ltr',
                    toggle: 'AR',
                    toggleAria: 'Switch to Arabic',
                    searchAria: 'Search',
                    githubAria: 'GitHub',
                    linkedinAria: 'LinkedIn',
                    nav: ['Home', 'Academics', 'Work', 'Workshops', 'Resources', 'About'],
                    contact: 'Contact',
                    footerLabels: ['Navigate', 'Connect', 'System'],
                    footerLinks: ['Academics', 'Projects', 'Workshops', 'Resources', 'LinkedIn', 'GitHub', 'Email', 'Blueprint Studio', 'Copyright & Policy'],
                    status: 'Status: Operational',
                    protocol: 'Protocol: HTTPS',
                    footerText: 'Software Engineering and Cybersecurity portfolio. Documenting projects, study systems, workshops, and technical resources.',
                    breadcrumbAcademics: 'Academics',
                    projectLabels: ['Role', 'Stack', 'Outputs'],
                    projectCategories: {
                        'software engineering': 'Software Engineering',
                        'computer science': 'Computer Science',
                        mathematics: 'Mathematics'
                    },
                    projectActions: {
                        documentation: 'Documentation',
                        repository: 'Repository',
                        app: 'App'
                    },
                    filterLabels: {
                        all: 'ALL',
                        'software-engineering': 'SOFTWARE ENGINEERING',
                        'computer-science': 'COMPUTER SCIENCE',
                        mathematics: 'MATHEMATICS'
                    },
                    sectionLabels: {
                        overview: 'Overview',
                        topics: 'Topics',
                        'study material': 'Study Material',
                        slides: 'Slides',
                        'slides with notes': 'Slides With Notes',
                        syllabus: 'Syllabus',
                        quizzes: 'Exams',
                        'slide breakdowns': 'Slide Breakdowns',
                        summary: 'Summary',
                        mindmap: 'Mindmap',
                        mindmaps: 'Mindmaps',
                        exams: 'Exams',
                        'extra resources': 'Extra Resources',
                        'writing resources': 'Writing Resources'
                    },
                    metaLabels: {
                        'course code': 'Course Code',
                        'credit hours': 'Credit Hours',
                        prerequisites: 'Prerequisites'
                    },
                    statusLabels: {
                        available: 'AVAILABLE',
                        'in progress': 'IN PROGRESS',
                        complete: 'COMPLETE'
                    },
                    trackLabels: {
                        'computer science': 'COMPUTER SCIENCE',
                        'software engineering': 'SOFTWARE ENGINEERING',
                        cybersecurity: 'CYBERSECURITY',
                        'other courses': 'OTHER COURSES'
                    },
                    trackTitles: {
                        'computer science': '7 courses.<br>Structured, documented,<br>and ready to use.',
                        'software engineering': '2 courses.<br>Requirements, design,<br>and engineering practice.',
                        cybersecurity: '1 course.<br>Security foundations,<br>threats, and defense.',
                        'other courses': '5 courses.<br>One English hub,<br>and shared resources.'
                    },
                    trackMeta: {
                        'computer science': ['CS Track', '7 Courses', 'Programming', 'Networks', 'Databases'],
                        'software engineering': ['SE Track', '2 Courses', 'Process', 'Requirements', 'Design'],
                        cybersecurity: ['Cyber Track', '1 Course', 'Security', 'Risk', 'Defense'],
                        'other courses': ['General Track', '5 Courses + English Hub', 'Writing', 'Ethics', 'Science']
                    }
                },
                ar: {
                    htmlLang: 'ar-SA',
                    dir: 'rtl',
                    toggle: 'EN',
                    toggleAria: 'حوّل إلى الإنجليزية',
                    searchAria: 'ابحث',
                    githubAria: 'جيت هب',
                    linkedinAria: 'لينكدإن',
                    nav: ['الرئيسية', 'الدراسة', 'أعمالي', 'الورش', 'الموارد', 'عن شوق'],
                    contact: 'تواصل معي',
                    footerLabels: ['التنقّل', 'التواصل', 'النظام'],
                    footerLinks: ['الدراسة', 'المشاريع', 'الورش', 'الموارد', 'لينكدإن', 'جيت هب', 'البريد', 'بلو برنت ستوديو', 'حقوق النشر والسياسة'],
                    status: 'الحالة: شغّال',
                    protocol: 'البروتوكول: HTTPS',
                    footerText: 'ملف أعمال في هندسة البرمجيات والأمن السيبراني، أوثّق فيه المشاريع والأنظمة الدراسية والورش والموارد التقنية.',
                    breadcrumbAcademics: 'الدراسة',
                    projectLabels: ['الدور', 'التقنيات', 'المخرجات'],
                    projectCategories: {
                        'software engineering': 'هندسة البرمجيات',
                        'computer science': 'علوم الحاسب',
                        mathematics: 'الرياضيات'
                    },
                    projectActions: {
                        documentation: 'الوثائق',
                        repository: 'المستودع',
                        app: 'التطبيق'
                    },
                    filterLabels: {
                        all: 'الكل',
                        'software-engineering': 'هندسة البرمجيات',
                        'computer-science': 'علوم الحاسب',
                        mathematics: 'الرياضيات'
                    },
                    sectionLabels: {
                        overview: 'نظرة عامة',
                        topics: 'الموضوعات',
                        'study material': 'مواد الدراسة',
                        slides: 'الشرائح',
                        'slides with notes': 'شرائح مع ملاحظات',
                        syllabus: 'الخطة الدراسية',
                        quizzes: 'الاختبارات',
                        'slide breakdowns': 'تفكيك الشرائح',
                        summary: 'الملخص',
                        mindmap: 'الخريطة الذهنية',
                        mindmaps: 'الخرائط الذهنية',
                        exams: 'الاختبارات',
                        'extra resources': 'مراجع إضافية',
                        'writing resources': 'موارد الكتابة'
                    },
                    metaLabels: {
                        'course code': 'رمز المقرر',
                        'credit hours': 'الساعات المعتمدة',
                        prerequisites: 'المتطلبات السابقة'
                    },
                    statusLabels: {
                        available: 'متاح',
                        'in progress': 'قيد التنفيذ',
                        complete: 'مكتمل'
                    },
                    trackLabels: {
                        'computer science': 'علوم الحاسب',
                        'software engineering': 'هندسة البرمجيات',
                        cybersecurity: 'الأمن السيبراني',
                        'other courses': 'مواد ثانية'
                    },
                    trackTitles: {
                        'computer science': '7 مواد.<br>مرتبة، موثقة،<br>وجاهزة للاستخدام.',
                        'software engineering': 'مادتين.<br>المتطلبات، التصميم،<br>وممارسة الهندسة.',
                        cybersecurity: 'مادة وحدة.<br>أساسيات الأمن،<br>والتهديدات، والدفاع.',
                        'other courses': '5 مواد.<br>مركز لغة إنجليزية واحد،<br>وموارد مشتركة.'
                    },
                    trackMeta: {
                        'computer science': ['مسار علوم الحاسب', '7 مواد', 'برمجة', 'شبكات', 'قواعد بيانات'],
                        'software engineering': ['مسار هندسة البرمجيات', 'مادتين', 'العمليات', 'المتطلبات', 'التصميم'],
                        cybersecurity: ['مسار الأمن السيبراني', 'مادة وحدة', 'الأمن', 'المخاطر', 'الدفاع'],
                        'other courses': ['مسار عام', '5 مواد + مركز اللغة الإنجليزية', 'الكتابة', 'الأخلاقيات', 'العلوم']
                    }
                }
            };

            function applyLang(lang) {
                var t = labels[lang] || labels.en;
                document.documentElement.lang = t.htmlLang;
                document.documentElement.dir = t.dir;
                document.body.classList.toggle('shoug-arabic-mode', lang === 'ar');
                if (langToggle) langToggle.textContent = t.toggle;
                if (langToggle) langToggle.setAttribute('aria-label', t.toggleAria);
                document.querySelectorAll('.shoug-icon-btn').forEach(function (node) {
                    if (node.getAttribute('aria-label') === 'Search' || node.getAttribute('aria-label') === 'ابحث') {
                        node.setAttribute('aria-label', t.searchAria);
                    }
                    if (node.getAttribute('aria-label') === 'GitHub' || node.getAttribute('aria-label') === 'جيت هب') {
                        node.setAttribute('aria-label', t.githubAria);
                    }
                    if (node.getAttribute('aria-label') === 'LinkedIn' || node.getAttribute('aria-label') === 'لينكدإن') {
                        node.setAttribute('aria-label', t.linkedinAria);
                    }
                });
                document.querySelectorAll('.shoug-header-nav a').forEach(function (link, index) {
                    if (t.nav[index]) link.textContent = t.nav[index];
                });
                var contact = document.querySelector('.shoug-contact-btn');
                if (contact) contact.textContent = t.contact;
                document.querySelectorAll('.shoug-footer-label').forEach(function (node, index) {
                    if (t.footerLabels[index]) node.textContent = t.footerLabels[index];
                });
                document.querySelectorAll('.shoug-footer-link').forEach(function (node, index) {
                    if (t.footerLinks[index]) node.textContent = t.footerLinks[index];
                });
                var metas = document.querySelectorAll('.shoug-footer-meta');
                if (metas[0]) metas[0].textContent = t.status;
                if (metas[1]) metas[1].textContent = t.protocol;
                var footerText = document.querySelector('.shoug-footer-text');
                if (footerText) footerText.textContent = t.footerText;
                document.querySelectorAll('.project-label').forEach(function (node, index) {
                    if (t.projectLabels[index]) node.textContent = t.projectLabels[index];
                });
                document.querySelectorAll('.project-category').forEach(function (node) {
                    var key = normalizeLabel(node.textContent);
                    if (t.projectCategories[key]) node.textContent = t.projectCategories[key];
                });
                document.querySelectorAll('.project-action').forEach(function (node) {
                    var key = normalizeLabel(node.textContent);
                    if (t.projectActions[key]) node.textContent = t.projectActions[key];
                });
                document.querySelectorAll('.filter-btn[data-filter]').forEach(function (node) {
                    var filter = node.getAttribute('data-filter');
                    if (t.filterLabels[filter]) node.textContent = t.filterLabels[filter];
                });
                document.querySelectorAll('.sub-nav-item, .tab, .quick-link-btn').forEach(function (node) {
                    var key = normalizeLabel(node.textContent);
                    if (t.sectionLabels[key]) node.textContent = t.sectionLabels[key];
                });
                document.querySelectorAll('.data-block-label, .meta-key').forEach(function (node) {
                    var key = normalizeLabel(node.textContent);
                    if (t.metaLabels[key]) node.textContent = t.metaLabels[key];
                });
                document.querySelectorAll('.status-tag').forEach(function (node) {
                    var key = normalizeLabel(node.textContent);
                    if (t.statusLabels[key]) node.textContent = t.statusLabels[key];
                });
                document.querySelectorAll('[data-ar-text]').forEach(function (node) {
                    var enText = node.getAttribute('data-en-text');
                    var textNode = node.children.length ? Array.prototype.find.call(node.childNodes, function (child) {
                        return child.nodeType === 3 && child.textContent.trim();
                    }) : null;
                    if (textNode) {
                        if (!node.dataset.i18nEn) node.dataset.i18nEn = enText || textNode.textContent;
                        textNode.textContent = lang === 'ar' ? node.getAttribute('data-ar-text') : node.dataset.i18nEn;
                    } else {
                        if (!node.dataset.i18nEn) node.dataset.i18nEn = enText || node.textContent;
                        node.textContent = lang === 'ar' ? node.getAttribute('data-ar-text') : node.dataset.i18nEn;
                    }
                });
                document.querySelectorAll('.breadcrumb').forEach(function (node) {
                    node.querySelectorAll('a').forEach(function (link) {
                        if (normalizeLabel(link.textContent) === 'academics' || normalizeLabel(link.textContent) === 'الدراسة') {
                            link.textContent = t.breadcrumbAcademics;
                        }
                    });
                });
                document.querySelectorAll('.hero-label').forEach(function (node) {
                    var key = normalizeLabel(node.textContent).replace(/^\\[|\\]$/g, '');
                    if (t.trackLabels[key]) node.textContent = '[ ' + t.trackLabels[key] + ' ]';
                });
                document.querySelectorAll('.hero-title').forEach(function (node) {
                    var key = normalizeLabel(node.textContent);
                    if (t.trackTitles[key]) node.innerHTML = t.trackTitles[key];
                });
                document.querySelectorAll('.hero-metadata-strip').forEach(function (node) {
                    var key = normalizeLabel(document.querySelector('.hero-label') ? document.querySelector('.hero-label').textContent : '').replace(/^\\[|\\]$/g, '');
                    var values = t.trackMeta[key];
                    if (!values) return;
                    node.innerHTML = '<span>' + values[0] + '</span><span class="meta-sep">//</span><span>' + values[1] + '</span><span class="meta-sep">//</span>' + values.slice(2).map(function (value) { return '<span>' + value + '</span><span class="meta-sep">·</span>'; }).join('').replace(/<span class="meta-sep">·<\\/span>$/, '');
                });
                document.querySelectorAll('.dir-row[data-ar-title] .dir-title').forEach(function (node) {
                    var row = node.closest('.dir-row');
                    if (!row) return;
                    if (!row.dataset.enTitle) row.dataset.enTitle = node.textContent;
                    node.textContent = lang === 'ar' && row.dataset.arTitle ? row.dataset.arTitle : row.dataset.enTitle;
                });
                syncLanguagePanels(lang);
                localStorage.setItem('shoug-lang', lang);
            }

            applyLang(initialLang());
            if (langToggle) {
                langToggle.addEventListener('click', function () {
                    applyLang(document.documentElement.lang && document.documentElement.lang.indexOf('ar') === 0 ? 'en' : 'ar');
                });
            }
        })();
    </script>
"""

LIGHT_MODE_STYLESHEET = '    <link rel="stylesheet" href="/styles/light-mode.css">\n'


def read_template(name: str) -> str:
    return TEMPLATES[name].read_text()


def write(name: str, text: str) -> None:
    OUT.mkdir(exist_ok=True)
    target = OUT / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(finalize_html(name, text) if name.endswith(".html") else text)


def inject_common_css(text: str) -> str:
    if ".shoug-site-header" in text:
        return text
    return text.replace("</style>", COMMON_HEADER_CSS + "\n    </style>", 1)


def replace_outer_header(text: str) -> str:
    return re.sub(r"<header\b[^>]*>.*?</header>", COMMON_HEADER, text, count=1, flags=re.S)


def replace_or_append_footer(text: str) -> str:
    if re.search(r"<footer\b[^>]*>.*?</footer>", text, flags=re.S):
        return re.sub(r"<footer\b[^>]*>.*?</footer>", COMMON_FOOTER, text, count=1, flags=re.S)
    return text.replace("</body>", COMMON_FOOTER + "\n</body>", 1)


def add_common_script(text: str) -> str:
    if "/styles/light-mode.css" not in text:
        text = text.replace("</head>", LIGHT_MODE_STYLESHEET + "</head>", 1)
    if "data-lang-toggle" in text and "localStorage.getItem('shoug-theme')" in text:
        return text
    return text.replace("</body>", COMMON_SCRIPT + "\n</body>", 1)


def mark_active_header(name: str, text: str) -> str:
    active_map = {
        "index.html": "/",
        "Academics/": "/Academics/",
        "work/index.html": "/work/",
        "work/projects/": "/work/",
        "workshops/": "/workshops/",
        "resources/": "/resources/",
        "about/": "/about/",
        "policy/": "/about/",
    }
    target = None
    for key, value in active_map.items():
        if name == key or name.startswith(key):
            target = value
            break
    if not target:
        return text
    return text.replace(f'<a href="{target}">', f'<a href="{target}" class="active">', 1)


def fix_visible_links(text: str) -> str:
    replacements = {
        'href="#" class="cta-primary"': 'href="/work/" class="cta-primary"',
        'href="#" style="font-family: var(--font-mono); color: var(--text-dim); text-decoration: none; font-size: 12px;"': 'href="/work/projects/" style="font-family: var(--font-mono); color: var(--text-dim); text-decoration: none; font-size: 12px;"',
        'href="#" vid="107">Services': 'href="https://blueprint.shoug-tech.com/" vid="107">Services',
        'href="#" class="footer-link" vid="123">PSU CCIS': 'href="https://www.psu.edu.sa/" class="footer-link" vid="123">PSU CCIS',
        'href="#" class="footer-link" vid="124">ACM Chapter': 'href="https://www.acm.org/" class="footer-link" vid="124">ACM Chapter',
        'href="/career-development/CV/"': 'href="/career-development/CV.html"',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    explore_links = [
        (r'(<a href=")[^"]*("[^>]*class="explore-item"[^>]*>\s*<h4[^>]*>Academics</h4>)', "/Academics/"),
        (r'(<a href=")[^"]*("[^>]*class="explore-item"[^>]*>\s*<h4[^>]*>Cybersecurity</h4>)', "/Academics/tracks/cybersecurity/"),
        (r'(<a href=")[^"]*("[^>]*class="explore-item"[^>]*>\s*<h4[^>]*>Career Portfolio</h4>)', "/work/"),
        (r'(<a href=")[^"]*("[^>]*class="explore-item"[^>]*>\s*<h4[^>]*>Blueprint Studio</h4>)', "https://blueprint.shoug-tech.com/"),
        (r'(<a href=")[^"]*("[^>]*class="explore-item"[^>]*>\s*<h4[^>]*>Academic Plan</h4>)', "/academic-plan-themes/academic-plan/"),
        (r'(<a href=")[^"]*("[^>]*class="explore-item"[^>]*>\s*<h4[^>]*>Resources</h4>)', "/resources/"),
    ]
    for pattern, url in explore_links:
        text = re.sub(pattern, lambda match, u=url: f"{match.group(1)}{u}{match.group(2)}", text, count=1, flags=re.S)

    dossier_links = [
        (r'(<a href=")[^"]*("[^>]*class="dossier-card"[^>]*data-accent="red")', "/workshops/cybersecurity-crash-course/"),
        (r'(<a href=")[^"]*("[^>]*class="dossier-card"[^>]*data-accent="purple")', "/workshops/student-tutor/"),
    ]
    for pattern, url in dossier_links:
        text = re.sub(pattern, lambda match, u=url: f"{match.group(1)}{u}{match.group(2)}", text, count=1, flags=re.S)

    resource_urls = {
        "W3Schools": "https://www.w3schools.com/",
        "W3Schools Java": "https://www.w3schools.com/java/",
        "freeCodeCamp": "https://www.freecodecamp.org/",
        "InfoQ": "https://www.infoq.com/",
        "Git by Bit": "https://gitbybit.com/",
        "MDN HTTP": "https://developer.mozilla.org/en-US/docs/Web/HTTP",
        "Robots.txt Dev": "https://developers.google.com/search/docs/crawling-indexing/robots/intro",
        "NIST Framework": "https://www.nist.gov/cyberframework",
        "Introducing JSX": "https://react.dev/learn/writing-markup-with-jsx",
        "SQLite Tutorial": "https://www.sqlitetutorial.net/",
        "Tuwaiq Academy": "https://tuwaiq.edu.sa/",
        "Neovim": "https://neovim.io/",
        "Helix": "https://helix-editor.com/",
        "Lovable": "https://lovable.dev/",
        "LMarena AI": "https://lmarena.ai/",
        "Homebrew": "https://brew.sh/",
        "Docker": "https://www.docker.com/",
        "Podman": "https://podman.io/",
        "AlmaLinux": "https://almalinux.org/",
        "Mosh": "https://mosh.org/",
        "DSA Visualizer": "https://www.cs.usfca.edu/~galles/visualization/Algorithms.html",
        "Regexr": "https://regexr.com/",
        "CoderHub": "https://coderhub.sa/",
        "MITRE ATT&amp;CK": "https://attack.mitre.org/",
        "CyberChef": "https://gchq.github.io/CyberChef/",
        "urlscan.io": "https://urlscan.io/",
        "masscan": "https://github.com/robertdavidgraham/masscan",
        "Fail2Ban": "https://github.com/fail2ban/fail2ban",
        "Evilginx2": "https://github.com/kgretzky/evilginx2",
        "msfvenom": "https://docs.metasploit.com/docs/using-metasploit/basics/how-to-use-msfvenom.html",
        "Bettercap": "https://www.bettercap.org/",
        "Hacking the Cloud": "https://hackingthe.cloud/",
        "NGINX": "https://nginx.org/",
        "GitHub Actions": "https://github.com/features/actions",
        "MkDocs Material": "https://squidfunk.github.io/mkdocs-material/",
        "TOML": "https://toml.io/",
        "Certbot": "https://certbot.eff.org/",
        "Netdata": "https://www.netdata.cloud/",
        "Open Banking SA": "https://www.sama.gov.sa/en-US/Pages/OpenBanking.aspx",
        "Demozoo": "https://demozoo.org/",
    }
    for title, url in resource_urls.items():
        pattern = rf'(<a href=")[^"]*("[^>]*class="card"[^>]*>(?:(?!</a>).)*?<h3[^>]*>{re.escape(title)}</h3>)'
        text = re.sub(pattern, lambda match, u=url: f"{match.group(1)}{u}{match.group(2)}", text, count=1, flags=re.S)

    project_urls = {
        "SE311": "/work/projects/#project-se311",
        "SE201": "/work/projects/#project-se201",
        "CS340": "/work/projects/#project-cs340",
        "CS330": "/work/projects/#project-cs330",
        "CS285": "/work/projects/#project-cs285",
        "CS210": "/work/projects/#project-cs210",
        "CS102": "/work/projects/#project-cs102",
        "MATH221": "/work/projects/",
    }
    for code, url in project_urls.items():
        pattern = rf'(<a href=")[^"]*("[^>]*class="project-row"[^>]*>(?:(?!</a>).)*?<span class="row-code[^"]*"[^>]*>{re.escape(code)}</span>)'
        text = re.sub(pattern, lambda match, u=url: f"{match.group(1)}{u}{match.group(2)}", text, count=1, flags=re.S)

    workshop_urls = {
        title: workshop_section_url("cyber_workshop", title)
        for title in WORKSHOP_SECTIONS["cyber_workshop"]["sections"]
    }
    workshop_urls.update({
        title: workshop_section_url("tutor_workshop", title)
        for title in WORKSHOP_SECTIONS["tutor_workshop"]["sections"]
    })
    for title, url in workshop_urls.items():
        pattern = rf'(<a href=")[^"]*("[^>]*class="workshop-card"[^>]*>(?:(?!</a>).)*?<h3 class="card-title"[^>]*>{title}</h3>)'
        text = re.sub(pattern, lambda match, u=url: f"{match.group(1)}{u}{match.group(2)}", text, count=1, flags=re.S)
        div_pattern = rf'(<div class="card"[^>]*)(>)(?=(?:(?!<div class="card").)*?<h3 class="card-title"[^>]*>{title}</h3>)'
        text = re.sub(div_pattern, lambda match, u=url: f'{match.group(1)} data-card-url="{html.escape(u)}"{match.group(2)}', text, count=1, flags=re.S)

    tab_urls = {
        "Overview": "/Academics/courses/se311/",
        "Slide Breakdowns": "/Academics/courses/se311/slide-breakdowns/",
        "Study Material": "/Academics/courses/se311/study-material/",
        "Slides": "/Academics/courses/se311/slides/",
        "Quizzes": "/Academics/courses/se311/quizzes/",
    }
    for title, url in tab_urls.items():
        text = re.sub(rf'href="#"([^>]*class="tab[^"]*"[^>]*>{re.escape(title)}</a>)', f'href="{url}"\\1', text, count=1)

    text = text.replace('<a href="#" class="nav-link prev"', '<a href="/Academics/courses/se311/slide-breakdowns/" class="nav-link prev"')
    text = text.replace('<a href="#" class="nav-link next"', '<a href="/Academics/courses/se311/slide-breakdowns/02-chapter-2-documentation-standards/" class="nav-link next"')
    text = text.replace('<a href="#" class="dir-row">', '<a href="/Academics/courses/se311/slide-breakdowns/01-chapter-1-basics-of-requirements-engineering/" class="dir-row">', 1)
    text = text.replace('<a href="#" class="dir-row">', '<a href="/Academics/courses/se311/slide-breakdowns/02-chapter-2-documentation-standards/" class="dir-row">', 1)

    return text


def finalize_html(name: str, text: str) -> str:
    text = replace_common_links(text)
    text = fix_visible_links(text)
    text = normalize_generated_routes(text)
    text = inject_common_css(text)
    text = replace_outer_header(text)
    text = replace_or_append_footer(text)
    text = add_common_script(text)
    text = mark_active_header(name, text)
    if name == "workshops/index.html":
        text = optimize_workshops_light_mode(text)
    return text


def optimize_workshops_light_mode(text: str) -> str:
    text = text.replace(
        '    <script vid="109">\n        const canvas = document.getElementById(\'glcanvas\');',
        '    <script vid="109">\n    (() => {\n        const canvas = document.getElementById(\'glcanvas\');',
        1,
    )
    text = text.replace(
        "                uniform float u_time;",
        "                uniform float u_time;\n                uniform float u_light;",
        1,
    )
    text = text.replace(
        """                    // Colors based on user system: #05020a, #b829ea, #ff2a4b
                    vec3 color1 = vec3(0.02, 0.01, 0.04); // void
                    vec3 color2 = vec3(0.72, 0.16, 0.92); // purple
                    vec3 color3 = vec3(1.0, 0.16, 0.29);  // red

                    vec3 finalColor = mix(color1, color2, clamp((f*f)*4.0,0.0,1.0));
                    finalColor = mix(finalColor, color3, clamp(length(q),0.0,1.0) * 0.2);
                    
                    // Darken overall to act as a backdrop
                    finalColor *= f * 1.5;""",
        """                    vec3 darkBase = vec3(0.02, 0.01, 0.04);
                    vec3 darkPurple = vec3(0.72, 0.16, 0.92);
                    vec3 darkRed = vec3(1.0, 0.16, 0.29);
                    vec3 lightBase = vec3(1.0, 0.99, 0.97);
                    vec3 lightPurple = vec3(0.88, 0.68, 1.0);
                    vec3 lightRose = vec3(1.0, 0.72, 0.8);

                    vec3 darkFog = mix(darkBase, darkPurple, clamp((f*f)*4.0,0.0,1.0));
                    darkFog = mix(darkFog, darkRed, clamp(length(q),0.0,1.0) * 0.2);
                    darkFog *= f * 1.5;

                    vec3 lightFog = mix(lightBase, lightPurple, clamp(f * 0.72, 0.0, 1.0));
                    lightFog = mix(lightFog, lightRose, clamp(length(q),0.0,1.0) * 0.18);

                    vec3 finalColor = mix(darkFog, lightFog, u_light);""",
        1,
    )
    text = text.replace(
        "            const resolutionUniform = gl.getUniformLocation(shaderProgram, 'u_resolution');",
        "            const resolutionUniform = gl.getUniformLocation(shaderProgram, 'u_resolution');\n            const lightUniform = gl.getUniformLocation(shaderProgram, 'u_light');",
        1,
    )
    text = text.replace(
        """            let startTime = Date.now();
            const render = () => {
                const currentTime = (Date.now() - startTime) / 1000.0;
                gl.uniform1f(timeUniform, currentTime);""",
        """            let startTime = Date.now();
            let lastLightFrame = 0;
            const render = () => {
                if (!canvas.isConnected) return;
                canvas.style.display = '';
                const isLight = document.body.classList.contains('shoug-light-mode');
                const now = performance.now();
                if (isLight && now - lastLightFrame < 32) {
                    requestAnimationFrame(render);
                    return;
                }
                lastLightFrame = now;
                const currentTime = (Date.now() - startTime) / 1000.0;
                gl.uniform1f(timeUniform, currentTime);
                gl.uniform1f(lightUniform, isLight ? 1.0 : 0.0);""",
        1,
    )
    text = text.replace(
        "        }\n    </script>\n\n\n    <script>",
        "        }\n    })();\n    </script>\n\n\n    <script>",
        1,
    )
    return text


def normalize_generated_routes(text: str) -> str:
    aliases = {
        "/homepage.html": "/",
        "/index.html": "/",
        "/academics-hub.html": "/Academics/",
        "/about-me.html": "/about/",
        "/projects.html": "/work/projects/",
        "/work-hub.html": "/work/",
        "/workshops-hub.html": "/workshops/",
        "/workshop-cybersecurity-crash-course.html": "/workshops/cybersecurity-crash-course/",
        "/workshop-my-journey-as-student-tutor.html": "/workshops/student-tutor/",
        "/resources.html": "/resources/",
        "/copyright-policy.html": "/policy/",
        "/chapter-index-se311-slide-breakdowns.html": "/Academics/courses/se311/slide-breakdowns/",
        "/content-viewer-se311-ch1.html": "/Academics/courses/se311/slide-breakdowns/01-chapter-1-basics-of-requirements-engineering/",
    }
    for slug, track in TRACKS.items():
        aliases[f"/track-{slug}.html"] = str(track["url"])
    for code, config in COURSES.items():
        aliases[f"/course-{code.lower()}.html"] = str(config["url"])
        for label in config["sections"]:
            if label != "Overview":
                aliases[f"/generated/academics/section-{code.lower()}-{slugify(label)}.html"] = section_url(code, label)
    for old, new in sorted(aliases.items(), key=lambda item: len(item[0]), reverse=True):
        text = text.replace(old, new)
    return text


def md_to_url(md_path: str) -> str:
    p = md_path.replace("docs/", "").replace(".md", "/")
    return "/" + p


def source_to_url(source: str) -> str:
    if source.endswith(".md"):
        return md_to_url("docs/" + source)
    return "/" + source.lstrip("/")


def slugify(value: str) -> str:
    value = clean_text(value).lower()
    value = value.replace("&", "and")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "item"


def section_url(code: str, label: str) -> str:
    if label == "Overview":
        return str(COURSES[code]["url"])
    return f"/Academics/courses/{code.lower()}/{slugify(label)}/"


def viewer_url(code: str, section_label: str, item_label: str, index: int) -> str:
    return f"/Academics/courses/{code.lower()}/{slugify(section_label)}/{index:02d}-{slugify(item_label)}/"


def generated_sections(code: str) -> dict[str, str]:
    return {label: section_url(code, label) for label in COURSES[code]["sections"]}


SECTION_AR_LABELS = {
    "Overview": "نظرة عامة",
    "Slide Breakdowns": "تفكيك الشرائح",
    "Slides": "الشرائح",
    "Slides With Notes": "شرائح مع ملاحظات",
    "Syllabus": "الخطة الدراسية",
    "Study Material": "المواد الدراسية",
    "Quizzes": "الاختبارات",
    "Exams": "الاختبارات",
    "Extra Resources": "موارد إضافية",
    "Writing Resources": "موارد الكتابة",
    "Mindmap": "الخريطة الذهنية",
    "Mindmaps": "الخرائط الذهنية",
    "Summary": "الملخص",
    "Topics": "الموضوعات",
}


def display_section_label(label: str) -> str:
    return "Exams" if label == "Quizzes" else label


def section_i18n_attrs(label: str, uppercase: bool = False, bracketed: bool = False) -> str:
    display_label = display_section_label(label)
    english = display_label.upper() if uppercase else display_label
    arabic = SECTION_AR_LABELS.get(display_label) or SECTION_AR_LABELS.get(label)
    if not arabic:
        return ""
    if bracketed:
        english = f"[ {english.upper()} ]"
        arabic = f"[ {arabic} ]"
    return f' data-en-text="{html.escape(english)}" data-ar-text="{html.escape(arabic)}"'


def track_for_course(code: str) -> str:
    for slug, track in TRACKS.items():
        if code in track["courses"]:
            return slug
    return ""


def academic_sidebar(active_code: str | None = None, active_section: str | None = None, active_item: str | None = None, active_track: str | None = None) -> str:
    track_rows: list[str] = []
    for slug, track in TRACKS.items():
        is_track_active = bool((active_code and active_code in track["courses"]) or slug == active_track)
        track_label = str(track["label"])
        track_modifier = " dir-open" if is_track_active else ""
        if track_label == "CYBERSECURITY":
            track_modifier += " cyber-track"
        children: list[str] = []
        child_id = f"tree-{slug}"
        if slug == "other-courses":
            children.append(
                '<li class="tree-item"><a class="tree-file" '
                'href="/academics/other-courses/english/">ENGLISH HUB</a></li>'
            )
        for code in track["courses"]:
            config = COURSES[code]
            display = html.escape(str(config.get("code_override") or code))
            is_course_active = code == active_code
            if is_course_active:
                section_children = []
                for section_label, url in generated_sections(code).items():
                    section_active = clean_text(section_label).lower() == clean_text(active_section or "").lower()
                    section_classes = "tree-item tree-section"
                    if section_active:
                        section_classes += " file-active"
                    item_children = ""
                    if section_active and section_label != "Overview":
                        item_rows = []
                        for item_index, (item_label, _source_url) in enumerate(section_items(code, section_label), start=1):
                            item_active = clean_text(item_label).lower() == clean_text(active_item or "").lower()
                            item_classes = "tree-item tree-viewer"
                            if item_active:
                                item_classes += " file-active"
                            item_rows.append(
                                f'<li class="{item_classes}"><a class="tree-file" href="{html.escape(viewer_url(code, section_label, item_label, item_index))}">'
                                f'{"<span class=\"status-dot\"></span>" if item_active else ""}{html.escape(item_label)}</a></li>'
                            )
                        item_children = f'<ul class="tree-children item-children is-open">{"".join(item_rows)}</ul>' if item_rows else ""
                    section_children.append(
                        f'<li class="{section_classes}"><a class="tree-file" href="{html.escape(url)}"{section_i18n_attrs(section_label, uppercase=True)}>'
                        f'{"<span class=\"status-dot\"></span>" if section_active and not active_item else ""}{html.escape(section_label.upper())}</a></li>{item_children}'
                    )
                children.append(
                    f'<li class="tree-item file-active"><a class="tree-file" href="{html.escape(str(config["url"]))}">'
                    f'{"<span class=\"status-dot\"></span>" if active_section == "Overview" else ""}{display}</a></li>'
                    f'<ul class="tree-children section-children">{"".join(section_children)}</ul>'
                )
            else:
                children.append(
                    f'<li class="tree-item"><a class="tree-file" href="{html.escape(str(config["url"]))}">{display}</a></li>'
                )
        track_rows.append(
            f'<li class="tree-item{track_modifier}"><button class="tree-course-link tree-toggle-button" type="button" data-tree-toggle="{child_id}" aria-expanded="{str(is_track_active).lower()}">'
            f'<span class="tree-toggle">{"[-]" if is_track_active else "[+]"}</span> {html.escape(track_label)}/</button></li>'
            f'<ul id="{child_id}" class="tree-children{" is-open" if is_track_active else ""}">{"".join(children)}</ul>'
        )
    return f'''
                <nav class="sidebar academic-sidebar" aria-label="Academic directory">
                    <div class="sidebar-header"><span class="sidebar-title">SYSTEM_DIRECTORY</span><button class="sidebar-collapse-button" type="button" data-sidebar-collapse aria-expanded="true"><span class="collapse-icon">&lt;</span></button></div>
                    <div class="file-tree">
                        <ul class="tree-node">
                            <li class="tree-item root-dir"><a class="tree-course-link" href="/Academics/">ACADEMICS/</a></li>
                            {"".join(track_rows)}
                        </ul>
                    </div>
                </nav>'''


def replace_academic_sidebar(text: str, active_code: str | None = None, active_section: str | None = None, active_item: str | None = None, active_track: str | None = None) -> str:
    sidebar = academic_sidebar(active_code, active_section, active_item, active_track)
    return replace_design_sidebar(text, sidebar)


def replace_design_sidebar(text: str, sidebar: str) -> str:
    text = re.sub(
        r'<nav\b[^>]*class="[^"]*\bsidebar\b[^"]*"[^>]*>.*?</nav>',
        sidebar,
        text,
        count=1,
        flags=re.S,
    )
    text = re.sub(
        r'<aside\b[^>]*class="[^"]*\bsys-sidebar\b[^"]*"[^>]*>.*?</aside>',
        sidebar,
        text,
        count=1,
        flags=re.S,
    )
    text = re.sub(
        r'<aside\b[^>]*class="[^"]*\bsidebar\b[^"]*"[^>]*>.*?</aside>',
        sidebar,
        text,
        count=1,
        flags=re.S,
    )
    return text


def workshop_sidebar(workshop_key: str, active_section: str | None = None) -> str:
    rows: list[str] = []
    active_dot = '<span class="status-dot"></span>'
    for key, workshop in WORKSHOP_SECTIONS.items():
        is_active_workshop = key == workshop_key
        workshop_title = str(workshop["title"])
        workshop_base = str(workshop["base"])
        child_id = f"tree-{key.replace('_', '-')}"
        section_rows: list[str] = []
        for section_title in workshop["sections"]:
            section_label = clean_text(str(section_title))
            section_active = is_active_workshop and section_label.lower() == clean_text(active_section or "").lower()
            classes = "tree-item tree-section"
            if section_active:
                classes += " file-active"
            section_rows.append(
                f'<li class="{classes}"><a class="tree-file" href="{html.escape(workshop_section_url(key, str(section_title)))}">'
                f'{active_dot if section_active else ""}{html.escape(section_label.upper())}</a></li>'
            )
        overview_active = is_active_workshop and not active_section
        rows.append(
            f'<li class="tree-item{" dir-open" if is_active_workshop else ""}"><button class="tree-course-link tree-toggle-button" type="button" data-tree-toggle="{child_id}" aria-expanded="{str(is_active_workshop).lower()}">'
            f'<span class="tree-toggle">{"[-]" if is_active_workshop else "[+]"}</span> {html.escape(workshop_title.upper())}/</button></li>'
            f'<ul id="{child_id}" class="tree-children{" is-open" if is_active_workshop else ""}">'
            f'<li class="tree-item{" file-active" if overview_active else ""}"><a class="tree-file" href="{html.escape(workshop_base)}">'
            f'{active_dot if overview_active else ""}OVERVIEW</a></li>'
            f'<ul class="tree-children section-children{" is-open" if is_active_workshop else ""}">{"".join(section_rows)}</ul></ul>'
        )
    return f'''
                <nav class="sidebar academic-sidebar" aria-label="Workshop directory">
                    <div class="sidebar-header"><span class="sidebar-title">WORKSHOP_DIRECTORY</span><button class="sidebar-collapse-button" type="button" data-sidebar-collapse aria-expanded="true"><span class="collapse-icon">&lt;</span></button></div>
                    <div class="file-tree">
                        <ul class="tree-node">
                            <li class="tree-item root-dir"><a class="tree-course-link" href="/workshops/">WORKSHOPS/</a></li>
                            {"".join(rows)}
                        </ul>
                    </div>
                </nav>'''


def course_nav_label(code: str) -> str:
    overrides = {
        "CYS401": "CYS 401",
        "ETHCS303": "ETHCS 303",
        "ENG101": "ENG 101",
        "ENG103": "ENG 103",
        "PHY105": "PHY105",
        "PHY205": "PHY205",
        "ISC113": "ISC 113",
    }
    if code in overrides:
        return overrides[code]
    match = re.match(r"([A-Z]+)(\d+)", code)
    return f"{match.group(1)} {match.group(2)}" if match else code


_MKDOCS_NAV: list[object] | None = None


def mkdocs_nav() -> list[object]:
    global _MKDOCS_NAV
    if _MKDOCS_NAV is None:
        data = yaml.load((ROOT / "mkdocs.yml").read_text(), Loader=yaml.Loader)
        _MKDOCS_NAV = list(data.get("nav", []))
    return _MKDOCS_NAV


def find_nav_node(items: object, target: str) -> object | None:
    if isinstance(items, list):
        for item in items:
            found = find_nav_node(item, target)
            if found is not None:
                return found
    elif isinstance(items, dict):
        for key, value in items.items():
            if clean_text(str(key)).lower() == clean_text(target).lower():
                return value
            found = find_nav_node(value, target)
            if found is not None:
                return found
    return None


def flatten_nav_entries(items: object) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    if isinstance(items, str):
        entries.append(("Open", source_to_url(items)))
    elif isinstance(items, list):
        for item in items:
            entries.extend(flatten_nav_entries(item))
    elif isinstance(items, dict):
        for label, value in items.items():
            if isinstance(value, str):
                entries.append((str(label), source_to_url(value)))
            else:
                entries.extend(flatten_nav_entries(value))
    return entries


def course_nav_sections(code: str) -> dict[str, list[tuple[str, str]]]:
    node = find_nav_node(mkdocs_nav(), course_nav_label(code))
    sections: dict[str, list[tuple[str, str]]] = {}
    if isinstance(node, list):
        for item in node:
            if not isinstance(item, dict):
                continue
            for label, value in item.items():
                sections[str(label)] = flatten_nav_entries(value)
    return sections


def docs_file_to_source_url(path: Path) -> str:
    rel = path.relative_to(ROOT / "docs").as_posix()
    if path.suffix.lower() == ".md":
        return md_to_url(f"docs/{rel}")
    if path.name == "index.html":
        return f"/{rel.removesuffix('index.html')}"
    return f"/{rel}"


def natural_key(value: str) -> list[object]:
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", value)]


def markdown_title(path: Path) -> str | None:
    try:
        text = path.read_text(errors="ignore")
    except OSError:
        return None
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            try:
                meta = yaml.safe_load(text[3:end]) or {}
            except yaml.YAMLError:
                meta = {}
            title = meta.get("title") if isinstance(meta, dict) else None
            if title:
                return clean_text(str(title))
    heading = re.search(r"^#\s+(.+)$", text, re.M)
    if heading:
        return clean_text(heading.group(1))
    return None


def prettify_filename(path: Path) -> str:
    stem = re.sub(r"\.ar$", "", path.stem, flags=re.I)
    stem = re.sub(r"[-_]+", " ", stem).strip()
    return clean_text(stem.title()) or "Open"


def section_candidate_dirs(code: str, label: str) -> list[Path]:
    url = str(COURSES[code]["sections"].get(label, ""))
    section_path = source_url_to_docs_path(url)
    candidates: list[Path] = []
    if section_path:
        if section_path.is_dir():
            candidates.append(section_path)
        elif section_path.stem.lower() in {"overview", "intro", "index"}:
            candidates.append(section_path.parent)
    course_root = (ROOT / str(COURSES[code].get("path", ""))).parent
    lower = clean_text(label).lower()
    aliases = {
        "slide breakdowns": ["slide-breakdowns", "chapters", "Chapter-*", "chapter-*"],
        "slides": ["slides"],
        "quizzes": ["quizez", "Quizez", "quizzes", "Quizzes"],
        "mindmap": ["Mindmap", "mindmap"],
        "mindmaps": ["Mindmap", "mindmap"],
        "summary": ["summary"],
        "study material": ["study-material"],
        "topics": ["topics"],
        "exams": ["Exams", "exams"],
        "extra resources": ["extra-resources"],
    }
    for alias in aliases.get(lower, [slugify(label)]):
        for path in course_root.glob(alias):
            if path.is_dir():
                candidates.append(path)
    seen: set[Path] = set()
    unique: list[Path] = []
    for path in candidates:
        resolved = path.resolve()
        if resolved not in seen and path.exists():
            seen.add(resolved)
            unique.append(path)
    return unique


def discovered_section_items(code: str, label: str) -> list[tuple[str, str]]:
    candidates = section_candidate_dirs(code, label)
    if not candidates:
        return []
    files: list[Path] = []
    lower_label = clean_text(label).lower()
    allowed_suffixes = {".md", ".pdf"}
    if lower_label == "slide breakdowns":
        allowed_suffixes = {".md", ".html"}
    for directory in candidates:
        files.extend(path for path in directory.rglob("*") if path.is_file() and path.suffix.lower() in allowed_suffixes)

    chosen: dict[str, Path] = {}
    for path in sorted(files, key=lambda p: natural_key(p.relative_to(ROOT / "docs").as_posix())):
        name = path.name
        stem_lower = path.stem.lower()
        if name.startswith(".") or ".ar." in name.lower() or stem_lower in {"overview", "intro"}:
            continue
        if path.name == "index.html" and any(path.parent == candidate for candidate in candidates):
            continue
        if stem_lower.endswith("-overview") or stem_lower.endswith("_overview"):
            continue
        key_path = path.parent if path.name == "index.html" else path.with_suffix("")
        rel_key = key_path.relative_to(ROOT / "docs").as_posix().lower()
        if rel_key.endswith(".ar"):
            continue
        current = chosen.get(rel_key)
        if current is None or (current.suffix.lower() == ".pdf" and path.suffix.lower() == ".md"):
            chosen[rel_key] = path

    items: list[tuple[str, str]] = []
    for path in sorted(chosen.values(), key=lambda p: natural_key(p.relative_to(ROOT / "docs").as_posix())):
        label_text = markdown_title(path) if path.suffix.lower() == ".md" else None
        items.append((label_text or prettify_filename(path), docs_file_to_source_url(path)))
    return items


def section_items(code: str, label: str) -> list[tuple[str, str]]:
    nav_sections = course_nav_sections(code)
    items = nav_sections.get(label, [])
    discovered = discovered_section_items(code, label)
    if discovered:
        items = discovered
    if not items:
        return []
    filtered = [(item_label, url) for item_label, url in items if clean_text(item_label).lower() != "overview"]
    return filtered or items


def clean_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"[:*_`#\\[\\]()]", "", value)
    value = value.replace("&amp;", "&")
    return " ".join(value.split())


def parse_course(code: str) -> dict[str, Any]:
    config = COURSES[code]
    raw_path = str(config.get("path", ""))
    path = ROOT / raw_path if raw_path else None
    text = path.read_text() if path and path.exists() and path.is_file() else ""
    title = str(config.get("title_override") or "TBD")
    desc = str(config.get("description") or "TBD")
    credits = str(config.get("credits") or "TBD")
    prereq = str(config.get("prereq") or "TBD")
    outcomes: list[str] = []
    topics: list[str] = []

    if text:
        heading = re.search(r"^#\s+(.+)$", text, re.M)
        if heading:
            heading_text = clean_text(heading.group(1))
            if " - " in heading_text:
                title = heading_text.split(" - ", 1)[1]
            elif code in heading_text:
                title = heading_text.replace(code, "").strip(" -") or heading_text
            else:
                title = heading_text

        after_heading = text[heading.end() :] if heading else text
        desc_parts = []
        for paragraph in re.split(r"\n\s*\n", after_heading):
            stripped = paragraph.strip()
            if not stripped:
                continue
            if stripped.startswith("---") or stripped.startswith("!!!") or stripped.startswith("##"):
                break
            if not stripped.startswith("|") and not stripped.startswith("<"):
                desc_parts.append(clean_text(stripped))
        if desc_parts:
            desc = " ".join(desc_parts[:2])

        for key, val in re.findall(r"\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|", text):
            k = clean_text(key).lower()
            v = clean_text(val)
            if k in {"course title", "title"}:
                title = v
            elif "credit" in k:
                credits = v
            elif "prerequisite" in k:
                prereq = v

        learning = re.search(r"## Course Learning Outcomes(?P<body>.*?)(?:\n## |\Z)", text, re.S)
        if learning:
            outcomes = [clean_text(item) for item in re.findall(r"^\d+\.\s+(.+?)(?=\n\d+\.\s+|\n\n---|\Z)", learning.group("body"), re.M | re.S)]
        if not outcomes:
            learn = re.search(r"## What You Will Learn(?P<body>.*?)(?:\n## |\Z)", text, re.S)
            if learn:
                outcomes = [clean_text(item) for item in re.findall(r"^-\s+(.+)$", learn.group("body"), re.M)]

        topics = [clean_text(m) for m in re.findall(r"-\s+(?::[^:]+:\s+)?\*\*(.+?)\*\*", text)]
        if "<div class=\"overview-hero\"" in text:
            hero_title = re.search(r"<h1>(.*?)</h1>", text, re.S)
            hero_desc = re.search(r"<p>(.*?)</p>", text, re.S)
            if hero_title and not config.get("title_override"):
                title = clean_text(hero_title.group(1))
            if hero_desc:
                desc = clean_text(hero_desc.group(1))
            credit = re.search(r"<strong>Credits</strong><span>(.*?)</span>", text, re.S)
            if credit:
                credits = clean_text(credit.group(1))
            topics = [clean_text(m) for m in re.findall(r"<strong>(.*?)</strong><span>.*?</span>", text, re.S) if clean_text(m).lower() not in {"course", "credits", "textbook"}]

    return {
        "code": str(config.get("code_override") or code),
        "slug": code.lower(),
        "title": title,
        "description": desc,
        "credits": credits,
        "prereq": prereq,
        "track": str(config["track"]),
        "url": str(config["url"]),
        "sections": dict(config["sections"]),
        "outcomes": outcomes[:7] or ["TBD"],
        "topics": topics[:10] or ["TBD"],
    }


def replace_first(pattern: str, repl: str, text: str, flags: int = re.S) -> str:
    return re.sub(pattern, repl, text, count=1, flags=flags)


def replace_between(text: str, start: str, end: str, replacement: str) -> str:
    start_i = text.find(start)
    if start_i == -1:
        return text
    end_i = text.find(end, start_i)
    if end_i == -1:
        return text
    return text[:start_i] + replacement + text[end_i:]


PROJECTS_CSS = r"""
        .project-list {
            display: grid;
            gap: 0;
        }

        .project-record {
            display: grid;
            grid-template-columns: 72px minmax(220px, 0.88fr) minmax(280px, 1.2fr) auto;
            gap: clamp(20px, 3vw, 52px);
            align-items: start;
            padding: 34px 32px;
            border-top: 1px solid rgba(255, 255, 255, 0.11);
            color: var(--text-primary);
            background: rgba(255, 255, 255, 0.006);
            transition: border-color 180ms ease, background 180ms ease, box-shadow 180ms ease;
        }

        .project-record:first-child {
            border-top-color: rgba(184, 41, 234, 0.48);
        }

        .project-record:hover {
            border-color: rgba(184, 41, 234, 0.52);
            background: rgba(184, 41, 234, 0.035);
            box-shadow: inset 2px 0 0 var(--brand-purple);
        }

        .project-record.is-hidden {
            display: none;
        }

        .project-index {
            color: var(--text-dim);
            font-family: var(--font-mono);
            font-size: 0.82rem;
            line-height: 1.8;
        }

        .project-heading {
            min-width: 0;
        }

        .project-heading .row-code {
            display: block;
            margin-bottom: 10px;
        }

        .project-heading h2 {
            margin: 0;
            color: var(--text-primary);
            font-family: var(--font-display);
            font-size: clamp(1.1rem, 1.6vw, 1.45rem);
            line-height: 1.15;
            letter-spacing: 0;
        }

        .project-category {
            display: inline-flex;
            align-items: center;
            margin-top: 18px;
            padding: 9px 12px;
            border: 1px solid rgba(184, 41, 234, 0.34);
            color: var(--text-primary);
            font-family: var(--font-mono);
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }

        .project-detail {
            min-width: 0;
        }

        .project-summary,
        .project-scope {
            margin: 0;
            color: var(--text-secondary);
            font-family: Inter, sans-serif;
            font-size: clamp(0.92rem, 1.1vw, 1.02rem);
            line-height: 1.65;
        }

        .project-scope {
            margin-top: 14px;
            color: var(--text-dim);
        }

        .project-role {
            margin-top: 18px;
            padding-left: 18px;
            border-left: 2px solid var(--brand-purple);
            color: var(--text-secondary);
            font-family: Inter, sans-serif;
            font-size: 0.9rem;
            line-height: 1.6;
        }

        .project-label {
            display: block;
            margin-bottom: 6px;
            color: var(--brand-purple);
            font-family: var(--font-mono);
            font-size: 0.66rem;
            font-weight: 800;
            letter-spacing: 0.16em;
            text-transform: uppercase;
        }

        .project-meta {
            display: grid;
            gap: 18px;
            justify-items: end;
            min-width: 220px;
        }

        .project-chip-grid {
            display: flex;
            flex-wrap: wrap;
            justify-content: flex-end;
            gap: 8px;
        }

        .project-chip {
            display: inline-flex;
            padding: 7px 9px;
            border: 1px solid rgba(255, 255, 255, 0.12);
            color: var(--text-secondary);
            font-family: var(--font-mono);
            font-size: 0.62rem;
            letter-spacing: 0.09em;
            text-transform: uppercase;
            white-space: nowrap;
        }

        .project-output-list {
            margin: 0;
            padding: 0;
            list-style: none;
            display: grid;
            gap: 8px;
            text-align: right;
        }

        .project-output-list li {
            color: var(--text-dim);
            font-family: Inter, sans-serif;
            font-size: 0.82rem;
            line-height: 1.45;
        }

        .project-actions {
            display: flex;
            flex-wrap: wrap;
            justify-content: flex-end;
            gap: 10px;
        }

        .project-action {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-height: 36px;
            padding: 0 12px;
            border: 1px solid rgba(184, 41, 234, 0.48);
            color: var(--text-primary);
            font-family: var(--font-mono);
            font-size: 0.68rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-decoration: none;
            text-transform: uppercase;
            transition: background 160ms ease, color 160ms ease, border-color 160ms ease;
        }

        .project-action:hover {
            background: var(--brand-purple);
            border-color: var(--brand-purple);
            color: var(--bg-void);
        }

        .filter-btn {
            cursor: pointer;
        }

        @media (max-width: 1100px) {
            .project-record {
                grid-template-columns: 54px 1fr;
            }

            .project-detail,
            .project-meta {
                grid-column: 2;
            }

            .project-meta {
                justify-items: start;
            }

            .project-chip-grid,
            .project-actions {
                justify-content: flex-start;
            }

            .project-output-list {
                text-align: left;
            }
        }

        @media (max-width: 680px) {
            .project-record {
                grid-template-columns: 1fr;
                padding: 28px 0;
            }

            .project-index,
            .project-detail,
            .project-meta {
                grid-column: auto;
            }

            .project-actions {
                width: 100%;
            }

            .project-action {
                flex: 1 1 140px;
            }
        }
"""


PROJECTS_FILTER_SCRIPT = """
    <script>
        (function () {
            var buttons = Array.prototype.slice.call(document.querySelectorAll('.filter-btn[data-filter]'));
            var records = Array.prototype.slice.call(document.querySelectorAll('.project-record[data-category]'));
            if (!buttons.length || !records.length) return;
            buttons.forEach(function (button) {
                button.addEventListener('click', function () {
                    var filter = button.getAttribute('data-filter');
                    buttons.forEach(function (item) { item.classList.remove('active'); });
                    button.classList.add('active');
                    records.forEach(function (record) {
                        var show = filter === 'all' || record.getAttribute('data-category') === filter;
                        record.classList.toggle('is-hidden', !show);
                    });
                });
            });
        })();
    </script>
"""


def render_project_record(project: dict[str, Any], index: int) -> str:
    links = "".join(
        f'<a class="project-action" href="{html.escape(url)}">{html.escape(label)}</a>'
        for label, url in project["links"]
    )
    stack = "".join(f'<span class="project-chip">{html.escape(item)}</span>' for item in project["stack"])
    outputs = "".join(f'<li>{html.escape(item)}</li>' for item in project["outputs"])
    return f'''
                <article class="project-record" id="project-{slugify(str(project["code"]))}" data-category="{html.escape(str(project["filter"]))}">
                    <div class="project-index">{index:02d}</div>
                    <div class="project-heading">
                        <span class="row-code">{html.escape(str(project["code"]))}</span>
                        <h2>{html.escape(str(project["title"]))}</h2>
                        <span class="project-category">{html.escape(str(project["category"]))}</span>
                    </div>
                    <div class="project-detail">
                        <p class="project-summary">{html.escape(str(project["summary"]))}</p>
                        <p class="project-scope">{html.escape(str(project["scope"]))}</p>
                        <div class="project-role"><span class="project-label">Role</span>{html.escape(str(project["role"]))}</div>
                    </div>
                    <div class="project-meta">
                        <div>
                            <span class="project-label">Stack</span>
                            <div class="project-chip-grid">{stack}</div>
                        </div>
                        <div>
                            <span class="project-label">Outputs</span>
                            <ul class="project-output-list">{outputs}</ul>
                        </div>
                        <div class="project-actions">{links}</div>
                    </div>
                </article>'''


def enhance_projects_page(text: str) -> str:
    if "project-record" in text:
        return text
    text = text.replace("</style>", PROJECTS_CSS + "\n    </style>", 1)
    text = re.sub(r'<button class="filter-btn active"[^>]*>ALL</button>', '<button class="filter-btn active" type="button" data-filter="all">ALL</button>', text, count=1)
    text = re.sub(r'<button class="filter-btn"[^>]*>SOFTWARE ENGINEERING</button>', '<button class="filter-btn" type="button" data-filter="software-engineering">SOFTWARE ENGINEERING</button>', text, count=1)
    text = re.sub(r'<button class="filter-btn"[^>]*>COMPUTER SCIENCE</button>', '<button class="filter-btn" type="button" data-filter="computer-science">COMPUTER SCIENCE</button>', text, count=1)
    text = re.sub(r'<button class="filter-btn"[^>]*>MATHEMATICS</button>', '<button class="filter-btn" type="button" data-filter="mathematics">MATHEMATICS</button>', text, count=1)
    records = "".join(render_project_record(project, index) for index, project in enumerate(PROJECTS, start=1))
    section = f'<section class="project-list">{records}\n        </section>'
    text = re.sub(r'<section class="project-list"[^>]*>.*?</section>', section, text, count=1, flags=re.S)
    return text.replace("</body>", PROJECTS_FILTER_SCRIPT + "\n</body>", 1)


def enhance_work_page(text: str) -> str:
    text = text.replace("6+ Projects", "8 Projects").replace("8+ Projects", "8 Projects")
    links = {
        "SE311 Requirements Analysis": "/work/projects/#project-se311",
        "Sillah Health System": "/work/projects/#project-se201",
        "CS340 Database Web App": "/work/projects/#project-cs340",
    }
    if ".work-card {" in text and "text-decoration: none" not in text[text.find(".work-card {"):text.find(".work-card {") + 260]:
        text = text.replace(
            ".work-card {\n",
            ".work-card {\n            color: inherit;\n            text-decoration: none;\n",
            1,
        )
    for title, url in links.items():
        pattern = rf'<div class="work-card"([^>]*)>(?:(?!</div>\s*</section>).)*?<h3 class="card-title"[^>]*>{re.escape(title)}</h3>.*?</div>'

        def replace_card(match: re.Match[str], target_url: str = url) -> str:
            card = match.group(0)
            card = card.replace('<div class="work-card"', f'<a class="work-card" href="{target_url}"', 1)
            return card[:-6] + "</a>"

        text = re.sub(pattern, replace_card, text, count=1, flags=re.S)
    return text


def enhance_homepage(text: str) -> str:
    if ".work-card-preview" not in text:
        text = text.replace(
            "</style>",
            """
        .work-card {
            text-decoration: none !important;
            isolation: isolate;
        }

        .work-card *,
        .work-card h3,
        .work-card .tag {
            text-decoration: none !important;
        }

        .work-card-preview {
            position: absolute;
            inset: 0;
            z-index: -2;
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: center top;
            filter: saturate(0.9) brightness(0.74);
            transform: scale(1.01);
            transition: transform 0.5s cubic-bezier(0.165, 0.84, 0.44, 1), filter 0.5s ease;
        }

        .work-card::before {
            content: "";
            position: absolute;
            inset: 0;
            z-index: -1;
            background: linear-gradient(180deg, rgba(5, 5, 8, 0.12) 0%, rgba(5, 5, 8, 0.56) 48%, rgba(5, 5, 8, 0.95) 100%);
        }

        .work-card:hover .work-card-preview {
            transform: scale(1.06);
            filter: saturate(1) brightness(0.88);
        }

        .work-card h3 {
            color: var(--text-main);
        }

</style>""",
            1,
        )
    cards = []
    arrow = '<svg class="work-arrow" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 17L17 7M17 7H7M17 7V17"></path></svg>'
    for item in FEATURED_WORK:
        cards.append(
            f'''
                <a class="work-card" href="{html.escape(item["url"])}">
                    <img class="work-card-preview" src="{html.escape(str(item["image"]))}" alt="{html.escape(str(item["title"]))} preview" loading="lazy">
                    {arrow}
                    <span class="tag">{html.escape(str(item["category"]).upper())}</span>
                    <h3>{html.escape(str(item["title"]))}</h3>
                </a>'''
        )
    return replace_between(
        text,
        '<div class="work-grid"',
        '\n        </section>',
        f'<div class="work-grid">{"".join(cards)}\n            </div>',
    )


def section_nav(sections: dict[str, str], class_name: str, active: str = "Overview") -> str:
    links = []
    for label, url in sections.items():
        active_class = " active" if label == active else ""
        display_label = display_section_label(label)
        content = f"[ {display_label.upper()} ]" if class_name == "sub-nav-item" else display_label
        links.append(f'<a href="{html.escape(url)}" class="{class_name}{active_class}"{section_i18n_attrs(label, uppercase=False, bracketed=class_name == "sub-nav-item")}>{content}</a>')
    return "\\n                        ".join(links)


def link_course_sidebar(text: str, active_code: str | None = None) -> str:
    for code, config in COURSES.items():
        display = str(config.get("code_override") or code)
        url = str(config["url"])
        text = re.sub(
            rf'(<li class="tree-item"[^>]*>\s*){re.escape(display)}(\s*</li>)',
            lambda match, u=url, d=display: f'{match.group(1)}<a class="tree-course-link" href="{u}">{d}</a>{match.group(2)}',
            text,
            count=1,
            flags=re.S,
        )
        text = re.sub(
            rf'(<li class="tree-item file-active"[^>]*>\s*<span class="status-dot"[^>]*></span>){re.escape(display)}(\s*</li>)',
            lambda match, u=url, d=display: f'{match.group(1)}<a class="tree-course-link" href="{u}">{d}</a>{match.group(2)}',
            text,
            count=1,
            flags=re.S,
        )
    for slug, track in TRACKS.items():
        label = str(track["label"])
        url = str(track["url"])
        text = re.sub(
            rf'(<li class="tree-item[^"]*"[^>]*>\s*)(<span class="tree-icon"[^>]*>\[[+\-]\]</span>\s*{re.escape(label)}/)(\s*</li>)',
            lambda match, u=url: f'{match.group(1)}<a class="tree-course-link" href="{u}">{match.group(2)}</a>{match.group(3)}',
            text,
            count=1,
            flags=re.S,
        )
    return text


def link_track_sidebar(text: str) -> str:
    for code, config in COURSES.items():
        display = str(config.get("code_override") or code)
        url = str(config["url"])
        text = re.sub(
            rf'<div class="tree-file"([^>]*)>{re.escape(display)}</div>',
            lambda match, u=url, d=display: f'<a class="tree-file"{match.group(1)} href="{u}">{d}</a>',
            text,
            count=1,
        )
    for slug, track in TRACKS.items():
        label = str(track["label"])
        url = str(track["url"])
        text = re.sub(
            rf'<div class="tree-row([^"]*)"([^>]*)>(\s*<span class="icon"[^>]*>\[[+\-]\]</span>\s*{re.escape(label)}/\s*)</div>',
            lambda match, u=url: f'<a class="tree-row{match.group(1)}"{match.group(2)} href="{u}">{match.group(3)}</a>',
            text,
            count=1,
            flags=re.S,
        )
    return text


def track_url_for_label(label: str) -> str:
    for track in TRACKS.values():
        if clean_text(str(track["label"])).lower() == clean_text(label).lower():
            return str(track["url"])
    return "/Academics/"


def render_breadcrumb(parts: list[tuple[str, str | None]], separator_html: str = '<span class="separator">/</span>') -> str:
    chunks = []
    for index, (label, url) in enumerate(parts):
        escaped = html.escape(label)
        if url and index != len(parts) - 1:
            chunks.append(f'<a class="breadcrumb-link" href="{html.escape(url)}">{escaped}</a>')
        elif index == len(parts) - 1:
            chunks.append(f'<span class="current">{escaped}</span>')
        else:
            chunks.append(f'<span>{escaped}</span>')
    return f'<div class="breadcrumb">{f" {separator_html} ".join(chunks)}</div>'


def course_page(code: str) -> str:
    data = parse_course(code)
    nav_sections = generated_sections(code)
    text = read_template("course")
    text = replace_common_links(text)
    text = replace_first(r"<title[^>]*>.*?</title>", f"<title>{data['code']} // {html.escape(str(data['title']))}</title>", text)
    text = replace_first(
        r'<div class="breadcrumb"[^>]*>.*?</div>',
        render_breadcrumb([
            ("Academics", "/Academics/"),
            (str(data["track"]), track_url_for_label(str(data["track"]))),
            (str(data["code"]), None),
        ]),
        text,
    )
    text = replace_first(r'<h1 class="course-code"[^>]*>.*?</h1>', f'<h1 class="course-code">{data["code"]}</h1>', text)
    text = replace_first(r'<h2 class="course-name"[^>]*>.*?</h2>', f'<h2 class="course-name">{html.escape(str(data["title"]))}</h2>', text)
    text = replace_first(r'<p class="course-desc-brief"[^>]*>.*?</p>', f'<p class="course-desc-brief">{html.escape(str(data["description"]))}</p>', text)
    text = replace_first(r'<nav class="sub-nav"[^>]*>.*?</nav>', f'<nav class="sub-nav">\\n                        {section_nav(nav_sections, "sub-nav-item")}\\n                    </nav>', text)
    blocks = f'''
                        <div class="grid-data-blocks">
                            <div class="data-block">
                                <span class="data-block-label">Course Code</span>
                                <span class="data-block-val">{data["code"]}</span>
                            </div>
                            <div class="data-block">
                                <span class="data-block-label">Credit Hours</span>
                                <span class="data-block-val">{html.escape(str(data["credits"]))}</span>
                            </div>
                            <div class="data-block">
                                <span class="data-block-label">Prerequisites</span>
                                <span class="data-block-val" style="font-family: var(--font-mono); font-size: 1.1rem; padding-top: 6px;">{html.escape(str(data["prereq"]))}</span>
                            </div>
                        </div>'''
    text = replace_between(text, '<div class="grid-data-blocks"', '<div class="section-label" vid="96">01_DESCRIPTION</div>', blocks + "\n\n                        ")

    desc_html = "".join(f"<p>{html.escape(part)}</p>" for part in [str(data["description"])])
    text = replace_first(r'<div class="text-block"[^>]*>\s*<p[^>]*>.*?</p>\s*<p[^>]*>.*?</p>\s*</div>', f'<div class="text-block">{desc_html}</div>', text)

    topics_html = []
    for index, topic in enumerate(data["topics"], start=1):
        topics_html.append(
            f'<div class="topic-item"><span class="topic-num">0x{index:02X}</span><span class="topic-name">{html.escape(topic)}</span><span class="topic-meta">IDX_{index:02d}</span></div>'
        )
    text = replace_between(
        text,
        '<div class="topics-list"',
        '<div class="section-label" vid="126">03_LEARNING_OUTCOMES</div>',
        f'<div class="topics-list" style="margin-bottom: 48px;">{"".join(topics_html)}</div>\n\n                        ',
    )

    outcomes_html = "".join(f"<li>{html.escape(outcome)}</li>" for outcome in data["outcomes"])
    text = replace_first(r'<ul class="learning-outcomes"[^>]*>.*?</ul>', f'<ul class="learning-outcomes">{outcomes_html}</ul>', text)
    text = replace_between(
        text,
        '<div class="section-label" vid="134">04_INSTRUCTOR_NODE</div>',
        '</div>\n                </article>',
        '',
    )

    text = re.sub(r'(<span class="meta-key"[^>]*>CREDIT HOURS</span>\s*<span class="meta-val"[^>]*>).*?(</span>)', lambda m: f'{m.group(1)}{html.escape(str(data["credits"]))}{m.group(2)}', text, count=1, flags=re.S)
    text = re.sub(r'(<span class="meta-key"[^>]*>TRACK</span>\s*<span class="meta-val"[^>]*>).*?(</span>)', lambda m: f'{m.group(1)}{html.escape(str(data["track"]))}{m.group(2)}', text, count=1, flags=re.S)
    text = re.sub(r'(<span class="meta-key"[^>]*>PREREQUISITES</span>\s*<span class="meta-val"[^>]*>).*?(</span>)', lambda m: f'{m.group(1)}{html.escape(str(data["prereq"]))}{m.group(2)}', text, count=1, flags=re.S)
    text = replace_first(r'\s*<div class="meta-row"[^>]*>\s*<span class="meta-key"[^>]*>SEMESTER</span>\s*<span class="meta-val"[^>]*>.*?</span>\s*</div>', "", text)
    quick = "".join(f'<a href="{html.escape(url)}" class="quick-link-btn">{html.escape(label)}</a>' for label, url in nav_sections.items())
    text = replace_first(r'<div class="quick-links"[^>]*>.*?</div>', f'<div class="quick-links">{quick}</div>', text)
    text = replace_academic_sidebar(text, str(data["code"]), "Overview")
    return text


def track_page(slug: str) -> str:
    track = TRACKS[slug]
    text = read_template("track")
    text = replace_common_links(text)
    status_legend_css = """

        .status-legend-card {
            width: min(100%, 860px);
            margin: -8px auto var(--spacing-lg);
            border: 1px solid var(--border-main);
            border-top: 2px solid var(--brand-purple);
            background: rgba(10, 2, 18, 0.82);
            padding: 14px 18px 16px;
            position: relative;
            z-index: 2;
        }

        .status-legend-kicker {
            font-family: var(--font-mono);
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 0.18em;
            color: var(--brand-purple);
            text-transform: uppercase;
            margin-bottom: 10px;
        }

        .status-legend-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 10px;
        }

        .status-legend-row {
            display: grid;
            grid-template-columns: 104px 1fr;
            gap: 10px;
            align-items: start;
            min-width: 0;
        }

        .status-legend-row .status-tag {
            justify-content: center;
            width: 104px;
            white-space: nowrap;
            text-align: center;
        }

        .status-legend-row p {
            margin: 0;
            color: var(--text-muted);
            font-size: 0.78rem;
            line-height: 1.45;
            overflow-wrap: anywhere;
        }

        html[dir="rtl"] .status-legend-card,
        body.shoug-arabic-mode .status-legend-card {
            direction: rtl;
            text-align: right;
        }

        html[dir="rtl"] .status-legend-row p,
        body.shoug-arabic-mode .status-legend-row p,
        html[dir="rtl"] .status-legend-note,
        body.shoug-arabic-mode .status-legend-note {
            text-align: right;
        }

        .status-legend-note {
            margin: 12px 0 0;
            padding-top: 10px;
            border-top: 1px dashed var(--border-main);
            color: var(--text-muted);
            font-family: var(--font-mono);
            font-size: 0.68rem;
            line-height: 1.5;
        }

        .status-pending {
            color: #f5a623;
        }

        .status-available,
        .status-active {
            color: var(--alert-red);
        }
"""
    status_legend_mobile_css = """

            .status-legend-card {
                width: 100%;
                margin: 0 0 18px;
                padding: 14px;
            }

            .status-legend-grid {
                grid-template-columns: 1fr;
                gap: 10px;
            }

            .status-legend-row {
                grid-template-columns: 104px 1fr;
                gap: 10px;
            }

            .status-legend-row p {
                font-size: 0.76rem;
            }
"""
    status_legend_html = """                <section class="status-legend-card" aria-labelledby="course-status-legend-title">
                    <div class="status-legend-kicker" id="course-status-legend-title" data-en-text="// COURSE STATUS GUIDE" data-ar-text="// دليل حالة المقرر">// COURSE STATUS GUIDE</div>
                    <div class="status-legend-grid">
                        <div class="status-legend-row">
                            <span class="status-tag status-active" data-en-text="AVAILABLE" data-ar-text="متاح">AVAILABLE</span>
                            <p data-en-text="Slides are available; personal notes have not yet been prepared." data-ar-text="الشرائح متوفرة، ولم يتم إعداد الملاحظات الشخصية بعد.">Slides are available; personal notes have not yet been prepared.</p>
                        </div>
                        <div class="status-legend-row">
                            <span class="status-tag status-pending" data-en-text="IN PROGRESS" data-ar-text="قيد التنفيذ">IN PROGRESS</span>
                            <p data-en-text="Slides and personal notes have not yet been added." data-ar-text="لم تتم إضافة الشرائح أو الملاحظات الشخصية بعد.">Slides and personal notes have not yet been added.</p>
                        </div>
                        <div class="status-legend-row">
                            <span class="status-tag status-complete" data-en-text="COMPLETE" data-ar-text="مكتمل">COMPLETE</span>
                            <p data-en-text="Slides are available and personal notes have been prepared." data-ar-text="الشرائح متوفرة، وقد تم إعداد الملاحظات الشخصية.">Slides are available and personal notes have been prepared.</p>
                        </div>
                    </div>
                    <p class="status-legend-note" data-en-text="Personal notes refer to slide breakdowns and extra resources prepared for independent study and revision." data-ar-text="تشير الملاحظات الشخصية إلى تفصيل الشرائح والموارد الإضافية المعدّة للدراسة والمراجعة الذاتية.">Personal notes refer to slide breakdowns and extra resources prepared for independent study and revision.</p>
                </section>

"""
    text = text.replace("\n\n\n\n        .course-list {", status_legend_css + "\n\n\n\n        .course-list {", 1)
    text = text.replace("\n\n            /* ── Course rows: allow wrapping ── */", status_legend_mobile_css + "\n\n            /* ── Course rows: allow wrapping ── */", 1)
    text = replace_first(r"<title[^>]*>.*?</title>", f"<title>SHOUG.TECH // {track['label']}</title>", text)
    text = re.sub(r"Computer Science", str(track["label"]).title(), text)
    text = replace_first(r'<div class="hero-label"[^>]*>.*?</div>', f'<div class="hero-label">[ {track["label"]} ]</div>', text)
    text = replace_first(r'<h1 class="hero-title"[^>]*>.*?</h1>', f'<h1 class="hero-title">{track["title"]}</h1>', text)
    meta = track["meta"]
    meta_html = f'<span>{meta[0]}</span><span class="meta-sep">//</span><span>{meta[1]}</span><span class="meta-sep">//</span>'
    meta_html += "".join(f'<span>{html.escape(m)}</span><span class="meta-sep">·</span>' for m in meta[2:]).removesuffix('<span class="meta-sep">·</span>')
    text = replace_first(r'<div class="hero-metadata-strip"[^>]*>.*?</div>', f'<div class="hero-metadata-strip">{meta_html}</div>', text)
    rows = []
    if slug == "other-courses":
        rows.append(
            '<a class="course-row" href="/academics/other-courses/english/">'
            '<div class="course-code">ENGLISH</div>'
            '<div class="course-name"><span data-ar-text="مركز تعلم اللغة الإنجليزية">English Learning Hub</span></div>'
            '<div class="course-status-area"><div class="status-tag status-complete">HUB</div>'
            '<div class="row-arrow">-&gt;</div></div></a>'
        )
    for code in track["courses"]:
        c = parse_course(code)
        status = str(COURSES.get(code, {}).get("status", "complete"))
        status_label = "AVAILABLE" if status == "available" else "COMPLETE"
        rows.append(
            f'<a class="course-row" href="{html.escape(str(c["url"]))}"><div class="course-code">{c["code"]}</div><div class="course-name"><span>{html.escape(str(c["title"]))}</span></div><div class="course-status-area"><div class="status-tag status-{status}">{status_label}</div><div class="row-arrow">-&gt;</div></div></a>'
        )
    text = replace_between(
        text,
        '<div class="course-list"',
        '\n\n        </div>\n    </main>',
        f'{status_legend_html}<div class="course-list">{"".join(rows)}</div>',
    )
    text = link_track_sidebar(text)
    text = replace_academic_sidebar(text, active_track=slug)
    return text


def section_page(code: str, label: str) -> str:
    data = parse_course(code)
    text = read_template("chapter_index")
    tabs = generated_sections(code)
    items = section_items(code, label)
    rows = []
    for index, (item_label, source_url) in enumerate(items, start=1):
        source_path = source_url_to_docs_path(source_url)
        arabic_title = ""
        if source_path and source_path.suffix.lower() == ".md":
            _, arabic_path = paired_markdown_paths(source_path)
            if arabic_path is not None:
                arabic_title = markdown_title(arabic_path) or prettify_filename(arabic_path)
        row_url = viewer_url(code, label, item_label, index)
        status = "COMING SOON" if is_coming_soon_slide_breakdown(label, source_url) else "AVAILABLE"
        rows.append(
            f'''
                            <a href="{html.escape(row_url)}" class="dir-row" data-ar-title="{html.escape(arabic_title)}">
                                <div class="dir-num">{index:02d}</div>
                                <div class="dir-title">{html.escape(item_label)}</div>
                                <div class="dir-status"><span class="status-tag">{status}</span></div>
                                <div class="dir-arrow">
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                                </div>
                            </a>'''
        )
    text = replace_first(r"<title[^>]*>.*?</title>", f"<title>SHOUG.TECH | {data['code']} {html.escape(label)}</title>", text)
    text = replace_first(
        r'<div class="breadcrumb"[^>]*>.*?</div>',
        render_breadcrumb([
            ("Academics", "/Academics/"),
            (str(data["track"]), track_url_for_label(str(data["track"]))),
            (str(data["code"]), str(data["url"])),
            (label, None),
        ], "/"),
        text,
    )
    text = replace_first(r'<h1 class="course-code"[^>]*>.*?</h1>', f'<h1 class="course-code">{data["code"]}</h1>', text)
    text = replace_first(r'<div class="type-label"[^>]*>.*?</div>', f'<div class="type-label">{html.escape(label.upper())}</div>', text)
    text = replace_first(r'<nav class="content-tabs"[^>]*>.*?</nav>', f'<nav class="content-tabs">\\n                        {section_nav(tabs, "tab", label)}\\n                    </nav>', text)
    replacement = empty_section_state() if not items else f'''
            <div class="directory-container">
                <div class="dir-header">
                    <span>SEQ</span>
                    <span>DESCRIPTOR</span>
                    <span>SYS_STATE</span>
                    <span></span>
                </div>
                {"".join(rows)}
            </div>'''
    text = re.sub(r'<div class="directory-container"[^>]*>.*?</script>\s*</div>', replacement, text, count=1, flags=re.S)
    text = re.sub(r'>SE311<', f'>{data["code"]}<', text)
    text = re.sub(r'>SOFTWARE_ENGINEERING<', f'>{html.escape(str(data["track"]).upper().replace(" ", "_"))}<', text)
    text = replace_academic_sidebar(text, str(data["code"]), label)
    return text


def empty_section_state() -> str:
    return '''
            <style id="empty-section-state-style">
                .coming-soon-container {
                    flex-grow: 1;
                    min-height: clamp(520px, 65vh, 900px);
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    padding: 80px 40px;
                    gap: 24px;
                    text-align: center;
                }
                .coming-soon-icon {
                    font-family: var(--font-mono);
                    font-size: 3rem;
                    color: var(--text-tertiary);
                    opacity: 0.4;
                }
                .coming-soon-title {
                    font-family: var(--font-display);
                    font-size: 2rem;
                    font-weight: 700;
                    color: var(--text-secondary);
                    text-transform: uppercase;
                }
                .coming-soon-text {
                    max-width: 520px;
                    font-family: var(--font-mono);
                    font-size: 0.95rem;
                    line-height: 1.8;
                    color: var(--text-tertiary);
                }
            </style>
            <div class="coming-soon-container" role="status">
                <div class="coming-soon-icon" aria-hidden="true">[ _ ]</div>
                <div class="coming-soon-title">COMING SOON</div>
                <div class="coming-soon-text">Content for this section is being prepared and will be available soon.</div>
            </div>'''


VIEWER_CSS = r"""
        .content-area {
            overflow: visible !important;
            min-width: 0;
        }

        .embed-area-wrapper {
            flex: initial !important;
            width: 100%;
            overflow: visible !important;
        }

        .page-content {
            flex: initial !important;
            min-height: auto !important;
            overflow: visible !important;
            padding-bottom: clamp(48px, 7vw, 112px);
        }

        .embed-container {
            flex: initial !important;
            display: block !important;
            align-items: stretch !important;
            justify-content: flex-start !important;
            min-height: min(760px, calc(100vh - 120px)) !important;
            height: auto !important;
            overflow: visible !important;
        }

        .embed-frame {
            position: relative;
            z-index: 2;
            width: 100%;
            min-height: min(860px, calc(100vh - 96px));
            height: min(1100px, max(82vh, 760px));
            border: 0;
            background: #fff;
            display: block;
        }

        .rendered-content iframe,
        .rendered-content video {
            position: relative;
            z-index: 2;
            display: block;
            width: 100%;
            max-width: 100%;
        }

        .rendered-content iframe {
            min-height: min(860px, calc(100vh - 96px));
            height: min(1100px, max(82vh, 760px));
            border: 0;
            background: #fff;
        }

        .rendered-content video {
            height: auto;
            background: #050508;
        }

        .action-buttons a.btn {
            text-decoration: none;
        }

        .btn-disabled {
            opacity: 0.62;
            cursor: default;
            pointer-events: none;
        }

        .coming-soon-panel {
            min-height: 320px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .rendered-content {
            position: relative;
            z-index: 2;
            min-height: auto;
            max-height: none;
            padding: clamp(24px, 4vw, 56px);
            background: rgba(5, 2, 10, 0.72);
            border: 1px solid rgba(184, 41, 234, 0.26);
            color: var(--text-main);
            font-family: var(--font-sans);
            line-height: 1.75;
            overflow: visible;
        }

        .rendered-content h1,
        .rendered-content h2,
        .rendered-content h3 {
            margin: 1.35em 0 0.65em;
            color: var(--text-main);
            font-family: var(--font-display);
            letter-spacing: 0;
        }

        .rendered-content h1:first-child,
        .rendered-content h2:first-child,
        .rendered-content h3:first-child {
            margin-top: 0;
        }

        .rendered-content p,
        .rendered-content ul,
        .rendered-content ol,
        .rendered-content table,
        .rendered-content blockquote {
            margin: 0 0 1rem;
        }

        .rendered-content a {
            color: var(--brand-purple);
            text-decoration: underline;
            text-underline-offset: 4px;
        }

        .rendered-content code,
        .rendered-content pre {
            font-family: var(--font-mono);
        }

        .rendered-content pre {
            overflow: auto;
            padding: 16px;
            border: 1px solid rgba(255, 255, 255, 0.12);
            background: rgba(0, 0, 0, 0.32);
        }

        .legacy-embed-placeholder {
            margin: 20px 0;
            padding: 20px;
            border: 1px solid rgba(184, 41, 234, 0.36);
            color: var(--text-dimmed);
            font-family: var(--font-mono);
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
"""


def source_url_to_docs_path(source_url: str) -> Path | None:
    if not source_url.startswith("/"):
        return None
    path = source_url.lstrip("/")
    if path.endswith("/"):
        md_candidate = ROOT / "docs" / f"{path.rstrip('/')}.md"
        html_candidate = ROOT / "docs" / path / "index.html"
        candidate = md_candidate if md_candidate.exists() else html_candidate
    else:
        candidate = ROOT / "docs" / path
    return candidate if candidate.exists() else None


def paired_markdown_paths(path: Path) -> tuple[Path | None, Path | None]:
    if path.suffix.lower() != ".md":
        return None, None
    if path.name.endswith(".ar.md"):
        english = path.with_name(path.name[: -len(".ar.md")] + ".md")
        arabic = path
    else:
        english = path
        arabic = path.with_name(f"{path.stem}.ar.md")
    return (english if english.exists() else None, arabic if arabic.exists() else None)


def render_markdown_panel(path: Path, lang: str) -> str:
    raw = strip_markdown_front_matter(path.read_text())
    rendered = markdown.markdown(raw, extensions=["extra", "tables", "toc", "fenced_code"])
    rendered = resolve_rendered_relative_assets(rendered, path)
    rendered = keep_rendered_links_in_shell(rendered)
    rendered = strip_embed_intro(rendered)
    hidden = ' hidden' if lang == 'ar' else ''
    return f'<div class="rendered-content" data-lang-panel="{lang}"{hidden}>{rendered}</div>'


def strip_markdown_front_matter(text: str) -> str:
    return re.sub(r"\A---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.S)


def resolve_rendered_relative_assets(rendered: str, source_path: Path) -> str:
    def replace_attr(match: re.Match[str]) -> str:
        attr = match.group(1)
        quote = match.group(2)
        value = match.group(3)
        if (
            not value
            or value.startswith(("#", "/", "mailto:", "tel:", "javascript:", "data:"))
            or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", value)
        ):
            return match.group(0)
        clean = value.split("#", 1)[0].split("?", 1)[0]
        if not clean:
            return match.group(0)
        candidate = (source_path.parent / clean).resolve()
        docs_root = (ROOT / "docs").resolve()
        try:
            rel = candidate.relative_to(docs_root)
        except ValueError:
            return match.group(0)
        if not candidate.exists():
            return match.group(0)
        suffix = value[len(clean):]
        return f'{attr}={quote}/{html.escape(rel.as_posix() + suffix, quote=True)}{quote}'

    return re.sub(r'\b(href|src|poster)=(["\'])([^"\']+)\2', replace_attr, rendered)


def keep_rendered_links_in_shell(rendered: str) -> str:
    rendered = re.sub(
        r'<iframe\b(?=[^>]*\bsrc="(/(?:Academics|career-development)/(?!CV\.html)[^"]*?\.html(?:[#?][^"]*)?)")[^>]*>\s*</iframe>',
        lambda match: f'<iframe class="embed-frame legacy-html-frame" src="{html.escape(match.group(1), quote=True)}" loading="lazy"></iframe>',
        rendered,
        flags=re.S,
    )
    rendered = re.sub(
        r'href="(/(?:Academics|career-development)/(?!CV\.html)[^"]*?)(?<!\.pdf)(?<!\.html)"',
        'href="#embedded-content"',
        rendered,
    )
    def replace_legacy_iframe(match: re.Match[str]) -> str:
        src_match = re.search(r'\bsrc=(["\'])(.*?)\1', match.group(0), flags=re.S)
        if src_match and re.search(r'\.html(?:[#?].*)?$', src_match.group(2)):
            return f'<iframe class="embed-frame legacy-html-frame" src="{html.escape(src_match.group(2), quote=True)}" loading="lazy"></iframe>'
        return '<div class="legacy-embed-placeholder">Embedded legacy page replaced by the new viewer shell.</div>'

    rendered = re.sub(
        r'<iframe\b(?=[^>]*\bsrc=["\']/(?:Academics|career-development)/(?!CV\.html)(?![^"\']*\.pdf)[^"\']*["\'])[^>]*>\s*</iframe>',
        replace_legacy_iframe,
        rendered,
        flags=re.S,
    )
    return rendered


def strip_embed_intro(rendered: str) -> str:
    rendered = re.sub(
        r'\A.*?(?=(?:<div class="iframe-wrap">\s*)?<iframe class="embed-frame)',
        "",
        rendered,
        count=1,
        flags=re.S,
    )
    rendered = re.sub(
        r'\A.*?(<div class="iframe-wrap">\s*<iframe class="embed-frame[^>]*>\s*</iframe>\s*</div>)',
        r"\1",
        rendered,
        count=1,
        flags=re.S,
    )
    rendered = re.sub(
        r'\A.*?(<iframe class="embed-frame[^>]*>\s*</iframe>)',
        r"\1",
        rendered,
        count=1,
        flags=re.S,
    )
    return re.sub(
        r'\A\s*<p><a href="(?P<src>/Academics/[^"]+\.pdf)"[^>]*>[^<]*</a></p>\s*\Z',
        lambda match: f'<iframe class="embed-frame" src="{html.escape(match.group("src"))}" title="PDF"></iframe>',
        rendered,
        flags=re.S,
    )


def markdown_contains_html_embed(path: Path) -> bool:
    raw = strip_markdown_front_matter(path.read_text())
    raw = resolve_rendered_relative_assets(raw, path)
    return bool(re.search(r'<iframe\b[^>]*\bsrc=["\']/[^"\']+\.html["\']', raw, flags=re.S))


def source_has_html_embed(source_url: str) -> bool:
    path = source_url_to_docs_path(source_url)
    if path is None:
        return False
    if path.suffix.lower() == ".html":
        return True
    if path.suffix.lower() == ".md":
        return markdown_contains_html_embed(path)
    return False


def is_coming_soon_slide_breakdown(section_label: str, source_url: str) -> bool:
    return clean_text(section_label).lower() == "slide breakdowns" and not source_has_html_embed(source_url)


def render_coming_soon_panel() -> tuple[str, str]:
    return (
        '<div class="embed-container" id="embedded-content">'
        '<div class="rendered-content coming-soon-panel">'
        '<h2>Coming Soon</h2>'
        '<p>This HTML slide breakdown is coming soon.</p>'
        '</div></div></div>',
        "#coming-soon",
    )


def render_source_panel(source_url: str, item_label: str) -> tuple[str, str]:
    path = source_url_to_docs_path(source_url)
    if path and path.suffix.lower() == ".md":
        english_path, arabic_path = paired_markdown_paths(path)
        if english_path is not None or arabic_path is not None:
            panels = []
            if english_path is not None:
                panels.append(render_markdown_panel(english_path, "en"))
            if arabic_path is not None:
                panels.append(render_markdown_panel(arabic_path, "ar"))
            return (
                f'<div class="embed-container" id="embedded-content">{"".join(panels)}</div></div>',
                "#embedded-content",
            )
        raw = strip_markdown_front_matter(path.read_text())
        rendered = markdown.markdown(raw, extensions=["extra", "tables", "toc", "fenced_code"])
        rendered = resolve_rendered_relative_assets(rendered, path)
        rendered = keep_rendered_links_in_shell(rendered)
        rendered = strip_embed_intro(rendered)
        return (
            f'<div class="embed-container" id="embedded-content"><div class="rendered-content">{rendered}</div></div></div>',
            "#embedded-content",
        )
    if path and path.suffix.lower() == ".pdf":
        return (
            f'<div class="embed-container" id="embedded-content"><iframe class="embed-frame" src="{html.escape(source_url)}" title="{html.escape(item_label)}"></iframe></div></div>',
            source_url,
        )
    if path and path.suffix.lower() == ".html":
        return (
            f'<div class="embed-container" id="embedded-content"><iframe class="embed-frame legacy-html-frame" src="{html.escape(source_url)}" title="{html.escape(item_label)}" loading="lazy"></iframe></div></div>',
            source_url,
        )
    return (
        f'<div class="embed-container" id="embedded-content"><div class="rendered-content"><h2>{html.escape(item_label)}</h2><p>Content is available in the new directory index. The source file could not be rendered automatically.</p></div></div></div>',
        "#embedded-content",
    )


def viewer_page(code: str, section_label: str, item_label: str, source_url: str, index: int, total: int) -> str:
    data = parse_course(code)
    text = read_template("content_viewer")
    text = text.replace("</style>", VIEWER_CSS + "\n    </style>", 1)
    if is_coming_soon_slide_breakdown(section_label, source_url):
        source_panel, open_url = render_coming_soon_panel()
    else:
        source_panel, open_url = render_source_panel(source_url, item_label)
    previous_url = section_url(code, section_label)
    next_url = section_url(code, section_label)
    items = section_items(code, section_label)
    if index > 1:
        previous_label, _ = items[index - 2]
        previous_url = viewer_url(code, section_label, previous_label, index - 1)
    if index < total:
        next_label, _ = items[index]
        next_url = viewer_url(code, section_label, next_label, index + 1)
    text = replace_first(r"<title[^>]*>.*?</title>", f"<title>{data['code']} | {html.escape(item_label)}</title>", text)
    text = replace_first(
        r'<div class="breadcrumb"[^>]*>.*?</div>',
        render_breadcrumb([
            ("Academics", "/Academics/"),
            (str(data["track"]), track_url_for_label(str(data["track"]))),
            (str(data["code"]), str(data["url"])),
            (section_label, section_url(code, section_label)),
            (item_label, None),
        ]),
        text,
    )
    text = replace_first(r'<div class="ch-label uppercase"[^>]*>.*?</div>', f'<div class="ch-label uppercase">ITEM_{index:02d} // {html.escape(section_label.upper())}</div>', text)
    text = replace_first(r'<h1 class="ch-title uppercase"[^>]*>.*?</h1>', f'<h1 class="ch-title uppercase">{html.escape(item_label)}</h1>', text)
    text = replace_first(
        r'<div class="action-buttons"[^>]*>.*?</div>',
        render_viewer_actions(open_url, section_url(code, section_label)),
        text,
    )
    text = replace_first(
        r'<div class="nav-strip uppercase"[^>]*>.*?</div>',
        f'<div class="nav-strip uppercase"><a href="{html.escape(previous_url)}" class="nav-link prev"><- PREVIOUS</a><a href="{html.escape(next_url)}" class="nav-link next">NEXT -></a></div>',
        text,
    )
    text = replace_first(
        r'<div class="embed-container"[^>]*>.*?</div>\s*</div>',
        source_panel,
        text,
    )
    text = re.sub(r'>SE311<', f'>{data["code"]}<', text)
    text = re.sub(r'>Software Engineering<', f'>{html.escape(str(data["track"]))}<', text)
    text = replace_academic_sidebar(text, str(data["code"]), section_label, item_label)
    return text


def render_viewer_actions(open_url: str, back_url: str) -> str:
    if open_url == "#coming-soon":
        return (
            '<div class="action-buttons"><span class="btn btn-primary btn-disabled" aria-disabled="true">[ COMING SOON ]</span>'
            f'<a class="btn btn-secondary" href="{html.escape(back_url)}">[ <- BACK TO INDEX ]</a></div>'
        )
    external_attrs = ' target="_blank" rel="noopener"' if open_url != "#embedded-content" else ""
    primary_label = "[ OPEN IN NEW TAB -> ]" if open_url != "#embedded-content" else "[ VIEW CONTENT -> ]"
    return (
        f'<div class="action-buttons"><a class="btn btn-primary" href="{html.escape(open_url)}"{external_attrs}>{primary_label}</a>'
        f'<a class="btn btn-secondary" href="{html.escape(back_url)}">[ <- BACK TO INDEX ]</a></div>'
    )


def replace_common_links(text: str) -> str:
    for label, url in sorted(COMMON_LINKS.items(), key=lambda item: len(item[0]), reverse=True):
        text = re.sub(
            rf'href="#"([^>]*)>{re.escape(label)}(?=\s*<|</a>)',
            lambda match, u=url, l=label: f'href="{u}"{match.group(1)}>{l}',
            text,
        )
    social = {
        "LinkedIn": "https://www.linkedin.com/in/shoug-alomran/",
        "GitHub": "https://github.com/Shoug-Alomran",
        "Email": "mailto:shoug.alomran@shoug-tech.com",
        "Email Me": "mailto:shoug.alomran@shoug-tech.com",
    }
    for label, url in social.items():
        text = re.sub(
            rf'href="#"([^>]*)>{re.escape(label)}',
            lambda match, u=url, l=label: f'href="{u}"{match.group(1)}>{l}',
            text,
        )
    text = re.sub(r'href="#"([^>]*class="[^"]*logo[^"]*")', r'href="/"\1', text)
    text = re.sub(r'href="#"([^>]*aria-label="Search")', r'href="/?q="\1', text)
    text = re.sub(r'href="#"([^>]*aria-label="Github")', r'href="https://github.com/Shoug-Alomran"\1', text)
    text = re.sub(r'href="#"([^>]*class="contact-btn")', r'href="mailto:shoug.alomran@shoug-tech.com"\1', text)
    text = re.sub(r'href="#"([^>]*class="icon-btn"[^>]*>\s*<svg[^>]*>\s*<path d="M20\.447)', r'href="https://www.linkedin.com/in/shoug-alomran/"\1', text)
    text = re.sub(r'href="#"([^>]*class="icon-btn"[^>]*>\s*<svg[^>]*>\s*<path d="M12 0c-6\.626)', r'href="https://github.com/Shoug-Alomran"\1', text)
    return text


def update_academics_hub() -> str:
    text = replace_common_links(read_template("academics"))
    for data in TRACKS.values():
        label = str(data["label"])
        pattern = rf'<a href="#"([^>]*class="track-card[^"]*"[^>]*>(?:(?!</a>).)*?<h2 class="card-title display"[^>]*>{re.escape(label)}</h2>)'
        text = re.sub(pattern, lambda match, u=data["url"]: f'<a href="{u}"{match.group(1)}', text, count=1, flags=re.S)
    return text


def static_file(template: str) -> str:
    text = replace_common_links(read_template(template))
    if template == "home":
        text = enhance_homepage(text)
    if template == "work":
        text = enhance_work_page(text)
    if template == "projects":
        text = enhance_projects_page(text)
    if template == "tutor_workshop":
        text = re.sub(
            r'<img\b([^>]*?)src="[^"]*"([^>]*?)>',
            r'<img\1src="/career-development/Workshops/My-Journey-as-a-Student-Tutor/pics/poster.png"\2>',
            text,
            count=1,
            flags=re.S,
        )
    return text


def workshop_content_page(workshop_key: str, section_title: str) -> str:
    workshop = WORKSHOP_SECTIONS[workshop_key]
    slug, source = workshop["sections"][section_title]
    source_url = source_to_url(source.replace("docs/", ""))
    text = read_template("content_viewer")
    text = text.replace("</style>", VIEWER_CSS + "\n    </style>", 1)
    source_panel, open_url = render_source_panel(source_url, section_title)
    base = str(workshop["base"])
    text = replace_first(r"<title[^>]*>.*?</title>", f"<title>{html.escape(str(workshop['title']))} | {html.escape(clean_text(section_title))}</title>", text)
    text = replace_first(
        r'<div class="breadcrumb"[^>]*>.*?</div>',
        render_breadcrumb([
            ("Workshops", "/workshops/"),
            (str(workshop["title"]), base),
            (clean_text(section_title), None),
        ]),
        text,
    )
    text = replace_first(r'<div class="ch-label uppercase"[^>]*>.*?</div>', f'<div class="ch-label uppercase">WORKSHOP // {html.escape(str(workshop["title"]).upper())}</div>', text)
    text = replace_first(r'<h1 class="ch-title uppercase"[^>]*>.*?</h1>', f'<h1 class="ch-title uppercase">{html.escape(clean_text(section_title))}</h1>', text)
    text = replace_first(
        r'<div class="action-buttons"[^>]*>.*?</div>',
        render_viewer_actions(open_url, base).replace("[ <- BACK TO INDEX ]", "[ <- BACK TO WORKSHOP ]"),
        text,
    )
    sections = list(workshop["sections"].items())
    current_index = [title for title, _data in sections].index(section_title)
    previous_url = base if current_index == 0 else workshop_section_url(workshop_key, sections[current_index - 1][0])
    next_url = base if current_index == len(sections) - 1 else workshop_section_url(workshop_key, sections[current_index + 1][0])
    text = replace_first(
        r'<div class="nav-strip uppercase"[^>]*>.*?</div>',
        f'<div class="nav-strip uppercase"><a href="{html.escape(previous_url)}" class="nav-link prev"><- PREVIOUS</a><a href="{html.escape(next_url)}" class="nav-link next">NEXT -></a></div>',
        text,
    )
    text = replace_first(
        r'<div class="embed-container"[^>]*>.*?</div>\s*</div>',
        source_panel,
        text,
    )
    text = replace_design_sidebar(text, workshop_sidebar(workshop_key, clean_text(section_title)))
    return text


def route_to_output_path(url_or_path: str) -> str:
    value = url_or_path.lstrip("/")
    if not value:
        return "index.html"
    if value.endswith("/"):
        return value + "index.html"
    return value


def write_url(url: str, text: str) -> None:
    write(route_to_output_path(url), text)


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(exist_ok=True)
    for template, filename in STATIC_OUTPUTS.items():
        if template == "academics":
            write(filename, update_academics_hub())
        else:
            html_text = static_file(template)
            write(filename, html_text)

    for slug in TRACKS:
        write_url(str(TRACKS[slug]["url"]), track_page(slug))

    for code in COURSES:
        write_url(str(COURSES[code]["url"]), course_page(code))
        for label in generated_sections(code):
            if label == "Overview":
                continue
            write_url(section_url(code, label), section_page(code, label))
            items = section_items(code, label)
            for index, (item_label, source_url) in enumerate(items, start=1):
                write_url(viewer_url(code, label, item_label, index), viewer_page(code, label, item_label, source_url, index, len(items)))

    for workshop_key, workshop in WORKSHOP_SECTIONS.items():
        for section_title, (slug, _source) in workshop["sections"].items():
            write_url(f'{workshop["base"]}{slug}/', workshop_content_page(workshop_key, section_title))

    html_files = sorted(p.relative_to(OUT).as_posix() for p in OUT.rglob("*.html"))
    manifest = "\n".join(html_files)
    (OUT / "MANIFEST.txt").write_text(manifest + "\n")
    print(f"Generated {len(html_files)} HTML files in {OUT}")


if __name__ == "__main__":
    main()
