#!/usr/bin/env python3
"""Slide-audited course model for SE365 (Human-Computer Interaction).

One record per lecture deck. Every renderer in build_se365_study_tools.py reads
from here, so the breakdown page, the mindmap and the exam can never drift apart:

    sections  -> the animated slide-breakdown page (and, folded down, the mindmap)
    branches  -> extra mindmap detail and worked examples
    quiz      -> the pop quiz embedded in the breakdown page
    exam_mcq / exam_short -> the standalone self-graded chapter exam

Block grammar used inside a section's "blocks" list:

    ("p",     "<html paragraph>")
    ("list",  ["item", ...])
    ("cards", [("Card title", "card body html"), ...])
    ("table", (["Header", ...], [["cell", ...], ...]))
    ("note",  ("LABEL", "<html>"))          # neutral callout
    ("warn",  ("LABEL", "<html>"))          # exam-trap callout
    ("hook",  ("LABEL", "<html>"))          # memory trick / analogy callout
    ("steps", [("Step name", "what happens"), ...])
"""

from __future__ import annotations

COURSE_CODE = "SE365"
COURSE_NAME = "Human-Computer Interaction"
TEXTBOOK = ("Sharp, H., Preece, J. and Rogers, Y. (2019). "
            "Interaction Design: Beyond Human-Computer Interaction, 5th Ed. Wiley.")

LECTURES: list[dict] = []


LECTURES.append({
    "num": 1,
    "slug": "introduction-to-human-computer-interaction",
    "title": "Introduction to Human-Computer Interaction",
    "short": "Introduction to HCI",
    "lecture_label": "Lecture 1",
    "theme": "signal",
    "accent": "#5b8def",
    "accent2": "#d9a441",
    "tagline": "What HCI is, why bad design happens, and the goals every interface is judged against.",
    "hero_title": "The computer's needs are alien<br><em>to the needs of the person using it.</em>",
    "hero_sub": ("Every interactive product you touch was designed by someone whose frame of reference was "
                 "<b>themselves</b>. HCI exists to break that loop: study the human, design the interaction, "
                 "measure it against usability and user experience goals rather than against a feature list."),
    "badges": ["HCI definition & scope", "Interaction design process",
               "6 usability goals", "UX goals", "5 design principles"],
    "outcomes": [
        "Define HCI and explain its interdisciplinary scope.",
        "Discuss how HCI evolved from ergonomics to experience design.",
        "Describe the four activities in the interaction design process.",
        "Distinguish usability goals from user experience goals.",
        "Apply the five core design principles to critique a real interface.",
    ],
    "sections": [
        {
            "id": "problem",
            "kicker": "01 - WHY DESIGN GOES WRONG",
            "title": "The problem HCI was invented to solve",
            "lead": ("A good programmer understands the nature and needs of the machine. But the nature and "
                     "needs of the machine are <em>utterly alien</em> to the nature and needs of the human "
                     "who will use it. That gap is where bad products are born."),
            "blocks": [
                ("list", [
                    "Designers see how <b>rich</b> the product is in features and functions, and stop seeing how hard it is to use.",
                    "They ignore how many hours it takes to learn, because they already know it.",
                    "They do work hard to make it easy to use - but their frame of reference is <b>themselves</b>, so it ends up easy for other software engineers and impossible for everyone else.",
                ]),
                ("cards", [
                    ("The elevator panel",
                     "Labels and control buttons on the bottom row all look identical, so people press a label "
                     "by mistake. Nobody makes that error on the top row, where labels and buttons look different. "
                     "The fix was never a manual - it was <b>visual distinction</b>."),
                    ("The vending machine",
                     "You must press a button first to activate the bill reader, but every vending machine on earth "
                     "takes the bill first. It contravenes a well-known convention, so users fail even though "
                     "each individual step is simple."),
                    ("The remote control",
                     "A generic remote is a grid of identical grey buttons. The TiVo remote is peanut-shaped to sit "
                     "in the hand, colour-coded, with distinctive shapes you can find by touch. Same function, "
                     "completely different interaction."),
                ]),
                ("hook", ("MEMORY HOOK", "Three failures, three principles, one sentence: "
                          "<b>elevator = visibility, vending machine = consistency with convention, remote = "
                          "affordance you can feel.</b> If you can retell those three objects you have already "
                          "recalled half of the design-principles section.")),
            ],
        },
        {
            "id": "what",
            "kicker": "02 - DEFINITION & SCOPE",
            "title": "What HCI actually is",
            "lead": ("HCI is the study of all aspects of how people interact with computers, and of the extent to "
                     "which people and computers influence each other. It is a two-way street by definition."),
            "blocks": [
                ("table", (["Source", "Definition worth quoting"], [
                    ["ACM SIGCHI (1992)",
                     "Concerned with the <b>design, evaluation and implementation</b> of interactive computing "
                     "systems for human use, and with the study of major phenomena surrounding them."],
                    ["Shneiderman",
                     "An <b>interdisciplinary design science</b> - it began by combining the data-gathering methods "
                     "and intellectual frameworks of experimental psychology with the tools of computer science."],
                    ["Dix (1998)",
                     "The study of people, computer technology, and the ways these influence each other. We study "
                     "HCI to determine how to make technology <b>more usable</b> by people."],
                    ["Carroll (2002)",
                     "The study and practice of <b>usability</b> - creating technology people will want to use, "
                     "will be able to use, and will find effective when used."],
                ])),
                ("p", "Pull the four words in the name apart, because the exam does:"),
                ("cards", [
                    ("Human", "Not only one person. An individual user, a group working together, or a sequence of "
                              "users inside an organisation."),
                    ("Computer", "Desktop machine, large-scale system, pocket device, embedded system (photocopier, "
                                 "microwave), or pure software (search engine, word processor)."),
                    ("User interface", "The parts of the computer the user actually comes into contact with."),
                    ("Interaction", "A dialogue with feedback and control throughout a task - the user invokes "
                                    "<i>print</i>, the interface replies with a dialog box."),
                ]),
                ("note", ("CONTRIBUTING FIELDS",
                          "Experimental psychology, computer science, educational and industrial psychology, "
                          "industrial and graphic design, technical writing, human factors / ergonomics, "
                          "information architecture, anthropology and sociology. HCI is a bridge discipline; "
                          "no single field owns it.")),
            ],
        },
        {
            "id": "design",
            "kicker": "03 - WHAT TO DESIGN",
            "title": "Who, what, where - then optimise",
            "lead": ("Before you can design an interaction you have to take three things into account: "
                     "<b>who</b> the users are, <b>what</b> activities are being carried out, and "
                     "<b>where</b> the interaction takes place. Only then can you optimise the interaction so "
                     "it matches the users' activities and needs."),
            "blocks": [
                ("list", [
                    "Take into account what people are <b>good and bad at</b> - not what you wish they were good at.",
                    "Consider what might help people in the way they <b>currently</b> do things.",
                    "Think through what might provide a quality user experience, not just a working one.",
                    "Listen to what people want and get them <b>involved</b>.",
                    "Use tried and tested user-centred methods rather than intuition.",
                ]),
                ("note", ("THE SMART TV DILEMMA",
                          "Pecking at a grid keyboard with a remote, swiping two alphanumeric rows on a touchpad, "
                          "or speaking to a smart speaker? There is no universal answer - the right one depends on "
                          "the task (a one-word search versus a password), the user, and the room. "
                          "That is the whole point of the who/what/where triad.")),
            ],
        },
        {
            "id": "accessibility",
            "kicker": "04 - ACCESSIBILITY, INCLUSION & CULTURE",
            "title": "One size fits nobody",
            "lead": ("Interaction design helps designers appreciate that one size does not fit all, identify "
                     "incorrect assumptions about user groups, and stay aware of both people's sensitivities and "
                     "their capabilities."),
            "blocks": [
                ("cards", [
                    ("Accessibility",
                     "The extent to which an interactive product is accessible by as many people as possible. "
                     "The focus is on people with disabilities - Android accessibility services, Apple VoiceOver."),
                    ("Inclusiveness",
                     "Making products and services accommodate the widest possible number of people - smartphones "
                     "designed for all and made available regardless of disability, education, age or income."),
                ]),
                ("p", "Disability is not a fixed property of a person. It changes with age or recovery, its impact "
                      "varies across a single day and across environments, and it is often <em>created</em> by "
                      "technology that demands an interaction some people cannot perform."),
                ("table", (["Classification", "Examples"], [
                    ["Sensory impairment", "Loss of vision or hearing; peripheral vision only, colour blindness, no light perception."],
                    ["Physical impairment", "Loss of function in one or more body parts after a stroke or spinal cord injury."],
                    ["Cognitive impairment", "Learning impairment, or loss of memory / cognitive function with old age."],
                ])),
                ("table", (["Duration category", "Example"], [
                    ["Permanent", "A long-term wheelchair user."],
                    ["Temporary", "Recovery after an accident or illness."],
                    ["Situational", "A noisy environment means a person cannot hear the audio prompt."],
                ])),
                ("p", "Design can also make impairment desirable rather than clinical: prosthetics have moved from "
                      "functional-and-ugly to fashionable, and people now speak of <i>wearing their wheels</i> "
                      "rather than <i>using a wheelchair</i>."),
                ("warn", ("CULTURAL DIFFERENCE TRAP",
                          "Is 5/21/2015 or 21/5/2015 correct for an international form? Neither - the answer is to "
                          "avoid ambiguous formats altogether. And note the asymmetry the slides raise: smartphones "
                          "are accepted almost universally, while websites get very different reactions across "
                          "cultures. Hardware conventions travel; content conventions do not.")),
                ("hook", ("MEMORY HOOK",
                          "<b>P-T-S</b> for duration - <b>P</b>ermanent, <b>T</b>emporary, <b>S</b>ituational - and "
                          "<b>S-P-C</b> for type - <b>S</b>ensory, <b>P</b>hysical, <b>C</b>ognitive. "
                          "Two three-letter chunks beat six loose terms.")),
            ],
        },
        {
            "id": "process",
            "kicker": "05 - THE PROCESS",
            "title": "Four activities of interaction design",
            "lead": "Interaction design is a process, and this lecture states it in its shortest form.",
            "blocks": [
                ("steps", [
                    ("Establishing requirements", "Find out who the users are and what support the product could usefully provide."),
                    ("Developing alternatives", "Generate more than one candidate design rather than defending the first idea."),
                    ("Prototyping", "Build something users can interact with, because designs cannot be judged on paper alone."),
                    ("Evaluating", "Test it, feed what you learn back into the requirements, and go round again."),
                ]),
                ("note", ("THREE CORE CHARACTERISTICS",
                          "Users are involved throughout development; usability and UX goals are identified, "
                          "documented and agreed <b>at the beginning</b>; and iteration runs through all four "
                          "activities. Miss any one and it is no longer interaction design.")),
            ],
        },
        {
            "id": "usability",
            "kicker": "06 - USABILITY GOALS",
            "title": "The six usability goals",
            "lead": ("Usability goals are about performance - can the product be used well? They are the "
                     "measurable half of the picture."),
            "blocks": [
                ("table", (["Goal", "The question it answers"], [
                    ["Effective to use", "How good is the product at doing what it is supposed to do?"],
                    ["Efficient to use", "Does the way the product works support the user in doing their task quickly?"],
                    ["Safe to use", "Does it protect users from undesirable or dangerous situations, including their own errors?"],
                    ["Good utility", "Does it provide the right kind of functionality at all?"],
                    ["Easy to learn", "How easy is the system to learn to use?"],
                    ["Easy to remember", "How easy is it to remember how to use after a period away?"],
                ])),
                ("p", "Which of the six matters most is not a property of the product - it is a property of the "
                      "user in front of it:"),
                ("list", [
                    "<b>Novice users</b> need learnability.",
                    "<b>Infrequent users</b> need memorability.",
                    "<b>Experts</b> need efficiency.",
                ]),
                ("warn", ("THE SUBTLETY THE SLIDES INSIST ON",
                          "No user is uniformly novice or expert. Expertise splits into <b>domain experience</b>, "
                          "<b>application experience</b> and <b>feature experience</b> - a veteran accountant can be "
                          "a total novice in your new accounting app, and an expert in your app can be a novice in "
                          "one obscure feature of it.")),
                ("hook", ("MEMORY HOOK",
                          "<b>E-E-S-U-L-R</b>: Effective, Efficient, Safe, Utility, Learn, Remember. Read it as "
                          "<i>&quot;Every Engineer Should Use Less Repetition&quot;</i>. Then attach the three user "
                          "types: <b>N</b>ovice-learn, <b>I</b>nfrequent-remember, <b>E</b>xpert-efficient.")),
            ],
        },
        {
            "id": "ux",
            "kicker": "07 - USER EXPERIENCE GOALS",
            "title": "UX: what it feels like, not what it does",
            "lead": ("UX is how a product behaves and is used <b>in the real world</b> - how people feel about it, "
                     "their pleasure and satisfaction in using, looking at, holding, opening or closing it. "
                     "Every product used by someone has a user experience: newspapers, ketchup bottles, "
                     "reclining armchairs, cardigan sweaters (Garrett, 2010)."),
            "blocks": [
                ("cards", [
                    ("Nielsen &amp; Norman (2014)", "All aspects of the end-user's interaction with the company, "
                                                    "its services, and its products."),
                    ("Hornb&aelig;k &amp; Hertzum (2017)", "How users perceive a product - whether a smartwatch reads "
                                                           "as sleek or chunky - and their emotional reaction to it."),
                ]),
                ("warn", ("THE ONE-LINE EXAM ANSWER",
                          "You <b>cannot design a user experience</b>. You can only design <b>for</b> a user "
                          "experience. The experience happens inside the person, not inside the product.")),
                ("table", (["Desirable UX qualities", "Undesirable UX qualities"], [
                    ["satisfying, enjoyable, engaging, pleasurable, exciting, entertaining", "boring, frustrating, unpleasant"],
                    ["helpful, motivating, challenging, enhancing sociability, supporting creativity", "patronizing, making one feel guilty, making one feel stupid"],
                    ["cognitively stimulating, fun, provocative, surprising, rewarding, emotionally fulfilling", "annoying, childish, cutesy, gimmicky"],
                ])),
                ("p", "The iPod is the textbook success: a quality experience from the very start - simple, elegant, "
                      "a distinct brand, pleasurable, a must-have fashion item with catchy names. None of those "
                      "words is a usability metric."),
                ("note", ("USABILITY vs UX - THE THREE COMPARISON QUESTIONS",
                          "How do usability goals differ from UX goals? Are there trade-offs between them - can a "
                          "product be both <i>fun</i> and <i>safe</i>? And how easy is each to measure? "
                          "Usability goals are largely objective and measurable; UX goals are subjective and "
                          "measured indirectly through people's own accounts.")),
            ],
        },
        {
            "id": "principles",
            "kicker": "08 - DESIGN PRINCIPLES",
            "title": "The five principles, with the slides' own examples",
            "lead": ("Design principles are generalizable abstractions for thinking about design - the do's and "
                     "don'ts, what to provide and what not to provide at the interface. They come from a mix of "
                     "theory-based knowledge, experience and common sense."),
            "blocks": [
                ("cards", [
                    ("1. Visibility",
                     "Make it visible what can be done. The elevator control panel where you cannot tell what to "
                     "push fails here, and invisible automatic controls (a tap that will not see your hand, "
                     "a sensor that misses you if you are wearing black) fail harder because there is nothing "
                     "to inspect at all."),
                    ("2. Feedback",
                     "Send information back to the user about what has been done - sound, highlighting, animation, "
                     "or combinations. A screen button that flashes red and clicks when pressed is doing feedback."),
                    ("3. Constraints",
                     "Restrict the possible actions so incorrect options cannot be selected: greying out menu items "
                     "so only permissible actions remain, or shaping a key so it enters a lock only one way."),
                    ("4. Consistency",
                     "Use similar operations and similar elements for similar tasks. Ctrl+C for copy, Ctrl+S for "
                     "save. Consistent interfaces are easier to learn and use."),
                    ("5. Affordances",
                     "An attribute of an object that gives a clue to how it is used. <b>Physical</b>: a door affords "
                     "pulling, a cup handle affords grasping. <b>Virtual</b>: an icon affords clicking, a scrollbar "
                     "affords moving up and down."),
                ]),
                ("p", "Consistency is the one the lecture pushes furthest, because it is the one that breaks:"),
                ("list", [
                    "What happens when several commands start with the same letter - save, spelling, select, style? "
                    "You are forced into Ctrl+S, Ctrl+Sp, Ctrl+Shift+L, breaking the very rule that made the "
                    "shortcuts learnable, and increasing the learning burden and error rate.",
                    "<b>Internal consistency</b>: operations behave the same way <i>within</i> one application. "
                    "Hard to achieve as interfaces grow complex.",
                    "<b>External consistency</b>: operations and interfaces are the same <i>across</i> applications "
                    "and devices. Very rarely achieved, because it depends on different designers' preferences.",
                ]),
                ("note", ("THE CONNECTOR EXAMPLE",
                          "Where do you plug in the mouse, top or bottom connector? Colour-coded icons alone may not "
                          "help. Two better designs: (i) place the icon <b>directly adjacent</b> to its connector so "
                          "the mapping is spatial, or (ii) colour-code so each connector is tied to its label. "
                          "This is visibility plus mapping doing the work that a manual otherwise has to do.")),
                ("hook", ("MEMORY HOOK",
                          "<b>V-F-C-C-A</b> - <i>&quot;Very Few Clumsy Cars Accelerate&quot;</i>. Visibility, "
                          "Feedback, Constraints, Consistency, Affordances. Then anchor each to one physical object: "
                          "elevator panel, red flash, greyed menu, Ctrl+C, door handle.")),
            ],
        },
    ],
    "mistakes": [
        ("&quot;HCI means making the interface pretty.&quot;",
         "HCI covers design, evaluation and implementation of interactive systems, and studies the mutual influence "
         "of people and technology. Aesthetics is one input to UX, not the discipline."),
        ("&quot;Usability and user experience are the same thing.&quot;",
         "Usability goals are performance-oriented and measurable (effective, efficient, safe, utility, learnable, "
         "memorable). UX goals are felt qualities (enjoyable, motivating, engaging) and can only be designed "
         "<b>for</b>, never designed directly."),
        ("&quot;We designed the user experience.&quot;",
         "You designed <i>for</i> a user experience. The wording is a graded distinction in this course."),
        ("&quot;A good product should maximise all six usability goals.&quot;",
         "Which goals dominate depends on the user: novices need learnability, infrequent users memorability, "
         "experts efficiency. Goals also trade off - safety measures often cost efficiency."),
        ("Confusing accessibility with inclusiveness.",
         "Accessibility focuses on making a product usable by people with disabilities; inclusiveness is the "
         "broader aim of accommodating the widest possible number of people regardless of disability, education, "
         "age or income."),
        ("Treating affordance and visibility as one principle.",
         "Visibility is about whether you can <i>see</i> what the options are. Affordance is whether the object's "
         "form tells you <i>how</i> to act on it. A visible button with no clue about what it does has visibility "
         "without affordance."),
    ],
    "cheat": (["Concept", "Shortest correct answer"], [
        ["HCI", "Design, evaluation and implementation of interactive computing systems for human use, plus study of the phenomena around them."],
        ["Interaction", "A dialogue with feedback and control while performing a task."],
        ["Interaction design process", "Establish requirements &rarr; develop alternatives &rarr; prototype &rarr; evaluate (iterate)."],
        ["Usability goals (6)", "Effective, efficient, safe, good utility, easy to learn, easy to remember."],
        ["UX goals", "Desirable felt qualities (satisfying, engaging, pleasurable) and undesirable ones (frustrating, patronizing, gimmicky)."],
        ["Design principles (5)", "Visibility, feedback, constraints, consistency, affordances."],
        ["Accessibility", "Extent to which a product is usable by as many people as possible, focusing on disability."],
        ["Inclusiveness", "Accommodating the widest possible number of people regardless of ability, education, age or income."],
        ["Impairment categories", "Sensory / physical / cognitive; permanent / temporary / situational."],
        ["Internal vs external consistency", "Same behaviour within one app vs same behaviour across apps and devices."],
    ]),
    "quiz": [
        {"q": "A microwave greys out the &quot;Start&quot; button until a cooking time has been entered. Which design principle is this?",
         "options": ["Constraints", "Feedback", "Affordance", "Visibility"], "correct": 0,
         "why": "Constraints restrict the possible actions so the user cannot select an incorrect option at that "
                "stage - the slides' own example is deactivating menu options by shading them grey. Feedback is "
                "wrong because nothing is being reported back about a completed action. Affordance is wrong because "
                "the greying does not communicate <i>how</i> to operate the control. Visibility is wrong because "
                "the control is visible either way; what changed is whether it is permitted."},
        {"q": "An expert user complains your app is slow to work with, although they know it perfectly. Which usability goal is failing?",
         "options": ["Efficient to use", "Easy to learn", "Easy to remember how to use", "Safe to use"], "correct": 0,
         "why": "Efficiency is about the way a product supports a user in carrying out their task, and experts are "
                "exactly the group who need it. Learnability is wrong because the user already knows the system. "
                "Memorability is wrong because they have not been away from it. Safety is wrong because nothing "
                "described puts the user at risk of an undesirable state."},
        {"q": "Which statement about user experience is correct as this course defines it?",
         "options": ["You can only design for a user experience, not design one",
                     "UX is measured with the same objective metrics as usability",
                     "UX applies only to digital products",
                     "UX and utility are synonyms"], "correct": 0,
         "why": "The experience happens inside the person, so designers create conditions for it and cannot "
                "guarantee it. The claim about objective metrics is wrong because UX goals are subjective and much harder to measure than usability goals. The digital-only claim is wrong because Garrett's point is that newspapers, ketchup bottles and armchairs all have a UX. Equating UX with utility is wrong because utility is a usability goal about whether the right functionality exists at all."},
        {"q": "A noisy factory floor means a worker cannot hear the machine's audio alert. How is that impairment classified?",
         "options": ["Situational", "Temporary", "Permanent", "Cognitive"], "correct": 0,
         "why": "Situational impairment is caused by the environment rather than the body - the slides use exactly "
                "this noisy-environment example. Temporary is wrong because it refers to impairment after an "
                "accident or illness that will resolve. Permanent is wrong because nothing about the person has "
                "changed. Cognitive is wrong because it names a <i>type</i> of impairment, not its duration."},
        {"q": "Word uses Ctrl+S for save; a second app in the same suite uses Ctrl+S for &quot;send&quot;. Which principle is broken, and at which level?",
         "options": ["External consistency", "Internal consistency", "Feedback", "Constraints"], "correct": 0,
         "why": "External consistency is about operations behaving the same way <i>across</i> applications and "
                "devices, which is exactly what breaks here. Internal consistency would be violated only if the "
                "same app used Ctrl+S for two different things. Feedback and constraints concern reporting results "
                "and limiting actions, neither of which is described."},
        {"q": "Which pair correctly matches a user type to the usability goal they most need?",
         "options": ["Infrequent user &rarr; easy to remember how to use",
                     "Expert &rarr; easy to learn",
                     "Novice &rarr; efficient to use",
                     "Infrequent user &rarr; good utility"], "correct": 0,
         "why": "Infrequent users return after gaps, so memorability dominates. Experts already learned the system "
                "and need efficiency, not learnability. Novices need learnability, not efficiency. Utility is about "
                "whether the right functions exist and is not tied to a frequency of use."},
    ],
    "lab": [
        ("Take the vending machine that requires a button press before it accepts a bill. Name the principle it "
         "violates and give the one-line redesign.",
         "It breaks consistency with a well-known external convention (bill first, then selection) and it fails "
         "visibility, because nothing indicates the reader is inactive. Redesign: accept the bill at any time, and "
         "if activation is genuinely required, make the reader slot physically closed and light it only when live - "
         "a constraint plus feedback rather than an instruction."),
        ("Your team says the new dashboard &quot;has a great user experience because we designed one.&quot; "
         "Rewrite that claim so it is defensible in this course.",
         "&quot;We designed <b>for</b> a user experience: we set UX goals of engaging and satisfying alongside "
         "usability goals of efficient and easy to remember, and we will evaluate with users to see whether the "
         "experience we aimed for actually occurs.&quot;"),
        ("A hospital drug-dosing screen must be usable by both new residents and consultants who use it fifty times "
         "a day. Which usability goals conflict, and how would you resolve it?",
         "Learnability (step-by-step prompts, constrained choices, clear information) conflicts with efficiency "
         "(shortcuts, direct entry) and both sit under safety, which must not be traded away. Resolve it with a "
         "layered interface: a guided default path for novices plus accelerators for experts, with safety "
         "constraints - confirmations on out-of-range doses - applied identically to both."),
    ],
    "branches": [
        ("What is HCI",
         "The study of all aspects of how people interact with computers and the extent to which people and computers influence each other.",
         ["ACM SIGCHI (1992): concerned with the design, evaluation and implementation of interactive computing systems for human use.",
          "Shneiderman calls it an interdisciplinary design science built from experimental psychology plus computer science.",
          "Dix (1998): the study of people, computer technology and the ways these influence each other.",
          "Carroll (2002): the study and practice of usability.",
          "Human means an individual, a group, or a sequence of users in an organisation.",
          "Computer covers desktops, large-scale systems, pocket devices, embedded systems and pure software.",
          "User interface means the parts of the computer the user comes into contact with.",
          "Interaction means a dialogue with feedback and control throughout a task."],
         [("Print dialog", "The user invokes the print command and the interface replies with a dialog box - a complete interaction cycle of command, feedback and control."),
          ("Embedded systems", "A photocopier or microwave counts as the computer in HCI, which is why appliance interfaces are studied in this course.")]),
        ("Why bad design happens",
         "Designers understand the machine, but the machine's nature is alien to the human who must use it, and designers use themselves as the frame of reference.",
         ["Designers see feature richness and stop seeing difficulty of use.",
          "They ignore how many hours the product takes to learn because they already know it.",
          "Making it easy for other software engineers is not the same as making it easy for people."],
         [("Elevator controls", "Labels and buttons on the bottom row look identical, so people press labels by mistake; the top row, where they look different, produces no such error."),
          ("Vending machine", "It requires a button press to activate the bill reader, contravening the convention of inserting the bill first."),
          ("TiVo remote", "Peanut-shaped to fit the hand, logically laid out, colour-coded and distinctive, so buttons are easy to locate without looking.")]),
        ("What to design",
         "Take into account who the users are, what activities are carried out and where the interaction takes place, then optimise the interaction to match users' activities and needs.",
         ["Consider what people are good and bad at.",
          "Consider what would help people in the way they currently do things.",
          "Think through what provides a quality user experience.",
          "Listen to what people want and involve them.",
          "Use tried and tested user-centred methods."],
         [("Smart TV input", "Grid-keyboard pecking, two-row touchpad swiping and voice control are each best for a different task, user and room - the who/what/where triad decides.")]),
        ("Accessibility and inclusiveness",
         "Accessibility is the extent to which a product is accessible by as many people as possible, focusing on disability; inclusiveness is accommodating the widest possible number of people.",
         ["Whether someone is disabled changes over time with age or recovery.",
          "Severity and impact vary within a single day and across environments.",
          "Disability can be created by technology that requires an interaction someone cannot perform.",
          "Types: sensory, physical, cognitive impairment.",
          "Durations: permanent, temporary, situational.",
          "Capability detail matters - peripheral vision only, colour blindness, or no light perception are different design problems."],
         [("Apple VoiceOver / Android accessibility", "Platform-level services that make the same product accessible without redesigning each app."),
          ("Fashionable prosthetics", "Alleles Design Studio leg covers move prosthetics from functional to desirable - people speak of wearing their wheels rather than using a wheelchair.")]),
        ("Process of interaction design",
         "Four activities: establishing requirements, developing alternatives, prototyping, and evaluating - run iteratively with users involved throughout.",
         ["Users should be involved through the development of the project.",
          "Specific usability and UX goals must be identified, documented and agreed at the beginning.",
          "Iteration is needed through the core activities."],
         [("Why iterate", "Designers never get the design right the first time, so evaluation feeds back into requirements rather than closing the project.")]),
        ("Usability goals",
         "Six performance-oriented goals used to judge whether a product can be used well.",
         ["Effective to use - how good the product is at doing what it should.",
          "Efficient to use - the way the product supports the user in doing the task.",
          "Safe to use - protecting users from undesirable conditions.",
          "Good utility - the extent to which the product provides the right kind of functionality.",
          "Easy to learn - how easy the system is to learn to use.",
          "Easy to remember how to use - how easy it is after time away.",
          "Which goal dominates depends on the user, not the product.",
          "No user is uniformly novice or expert: domain, application and feature experience differ."],
         [("Novice vs expert", "Novices need learnability, infrequent users need memorability and experts need efficiency - the same product must often serve all three.")]),
        ("User experience goals",
         "How a product behaves and is used in the real world, and how people feel about using, looking at, holding, opening or closing it.",
         ["Every product used by someone has a user experience (Garrett, 2010).",
          "Nielsen and Norman (2014): all aspects of the end user's interaction with the company, its services and its products.",
          "Hornbaek and Hertzum (2017): how users perceive a product and their emotional reaction to it.",
          "You cannot design a user experience, only design for one.",
          "Desirable: satisfying, enjoyable, engaging, pleasurable, motivating, challenging, cognitively stimulating, rewarding.",
          "Undesirable: boring, frustrating, unpleasant, patronizing, annoying, childish, cutesy, gimmicky.",
          "UX goals are harder to measure than usability goals and can trade off against them."],
         [("The iPod", "A quality experience from the start - simple, elegant, distinct brand, pleasurable, a must-have fashion item with catchy names."),
          ("Fun versus safe", "Asking whether a product can be both is the standard way this course probes the trade-off between UX and usability goals.")]),
        ("Design principles",
         "Generalizable abstractions - the do's and don'ts of interaction design - derived from theory, experience and common sense.",
         ["Visibility: make it visible what can be done; invisible automatic controls are harder to use.",
          "Feedback: send information back about what has been done, using sound, highlighting or animation.",
          "Constraints: restrict possible actions to prevent incorrect selections, such as greying out menu options.",
          "Consistency: similar operations and elements for similar tasks, which makes interfaces easier to learn.",
          "Affordances: an attribute of an object that gives a clue to how it is used.",
          "Internal consistency is sameness within an application; external consistency is sameness across applications and devices.",
          "Consistency breaks when several commands share a first letter, forcing awkward key combinations."],
         [("Physical affordance", "A door affords pulling and a cup handle affords grasping without instruction."),
          ("Virtual affordance", "Icons afford clicking and scrollbars afford moving up and down - learned conventions rather than physical form."),
          ("Connector mapping", "Placing each icon directly adjacent to its connector, or colour-coding connector and label together, fixes an ambiguous port layout.")]),
    ],
    "exam_mcq": [
        {"q": "Which definition of HCI is attributed to ACM SIGCHI (1992)?",
         "options": ["Concerned with the design, evaluation and implementation of interactive computing systems for human use and the study of major phenomena surrounding them",
                     "The study and practice of usability",
                     "An interdisciplinary design science",
                     "The study of people, computer technology and the ways these influence each other"],
         "correct": 0,
         "why": "The design/evaluation/implementation wording is the SIGCHI definition. &quot;The study and practice "
                "of usability&quot; is Carroll (2002). &quot;Interdisciplinary design science&quot; is Shneiderman. "
                "The people/technology/influence phrasing is Dix (1998)."},
        {"q": "Which of the following is NOT one of the six usability goals?",
         "options": ["Motivating to use", "Safe to use", "Good utility", "Easy to remember how to use"],
         "correct": 0,
         "why": "Motivating is a user <i>experience</i> goal in the desirable-qualities list, not a usability goal. "
                "Safe, good utility and easy to remember are three of the six usability goals alongside effective, "
                "efficient and easy to learn."},
        {"q": "A car dashboard uses a raised, ridged dial for volume so the driver can find and turn it without looking. Which principle does the ridging most directly serve?",
         "options": ["Affordance", "Feedback", "Constraint", "External consistency"],
         "correct": 0,
         "why": "The physical form communicates how the object is to be used - grasping and turning - which is the "
                "definition of a physical affordance. Feedback would be the click or the volume changing. A "
                "constraint would be a mechanism preventing an invalid action. External consistency would concern "
                "matching other cars' dashboards, which is not what the ridging does."},
        {"q": "Which statement best captures the difference between accessibility and inclusiveness?",
         "options": ["Accessibility focuses on people with disabilities; inclusiveness aims at the widest possible number of people regardless of disability, education, age or income",
                     "Accessibility is a legal requirement while inclusiveness is a design ideal",
                     "Accessibility applies to hardware and inclusiveness to software",
                     "They are interchangeable terms for the same goal"],
         "correct": 0,
         "why": "That is the distinction the lecture draws. The legal framing is not how the course defines them; "
                "the hardware/software split is invented; and they are explicitly presented as related but distinct."},
        {"q": "Which case is an example of a SITUATIONAL impairment?",
         "options": ["A commuter cannot hear a voice prompt on a loud train",
                     "A user has been a wheelchair user for twenty years",
                     "A user has a broken wrist for six weeks",
                     "A user has red-green colour blindness"],
         "correct": 0,
         "why": "Situational impairment comes from the environment. The long-term wheelchair user is the slides' "
                "permanent example, the broken wrist is temporary, and colour blindness is a permanent sensory "
                "impairment."},
        {"q": "A design team fixes the interface after every round of user testing and tests again. Which characteristic of interaction design is this?",
         "options": ["Iteration", "Empirical measurement", "Triangulation", "Utility"],
         "correct": 0,
         "why": "Iteration is the characteristic that says designers never get it right the first time and must "
                "cycle through the activities. Empirical measurement is the recording and analysis of user "
                "performance, which is what a test produces rather than what repeating it is called. "
                "Triangulation belongs to data gathering, and utility is a usability goal."},
    ],
    "exam_short": [
        {"q": "State the four activities of the interaction design process in order, and give the one-line purpose of each.",
         "keywords": ["requirement", "alternativ", "prototyp", "evaluat"],
         "answer": "Establishing requirements - find out who the users are and what support the product could "
                   "usefully provide. Developing alternatives - generate more than one candidate design. "
                   "Prototyping - build something users can actually interact with. Evaluating - determine the "
                   "usability and acceptability of the design and feed the findings back. The four run "
                   "iteratively, not once."},
        {"q": "Explain why the course insists you can only design FOR a user experience.",
         "keywords": ["experience", "feel", "cannot", "user"],
         "answer": "A user experience is how a person perceives and emotionally reacts to a product; it occurs "
                   "inside the user and depends on their context, expectations and mood. Designers control the "
                   "product's qualities - its look, feel, responsiveness and behaviour - and so create the "
                   "conditions in which a desired experience is likely, but they cannot guarantee or install the "
                   "experience itself."},
        {"q": "Distinguish internal from external consistency and give one example of each breaking.",
         "keywords": ["internal", "external", "consistency", "applicat"],
         "answer": "Internal consistency means operations behave the same way within one application - it breaks "
                   "when the same gesture deletes in one panel and archives in another. External consistency means "
                   "operations, interfaces and conventions are the same across applications and devices - it "
                   "breaks when Ctrl+S saves in one app and sends in another. Internal consistency is hard to "
                   "achieve in complex interfaces; external consistency is rarely achieved because it depends on "
                   "different designers' preferences."},
        {"q": "Why is the classic advice &quot;design for the novice&quot; incomplete, according to the usability-goals section?",
         "keywords": ["novice", "expert", "efficien", "learn"],
         "answer": "Because which usability dimension matters depends on the user: novices need learnability, "
                   "infrequent users need memorability and experts need efficiency. Moreover no user is uniformly "
                   "novice or expert - domain experience, application experience and feature experience are "
                   "separate - so a real product must support several of these profiles at once, usually with a "
                   "guided path plus accelerators."},
        {"q": "Give the five design principles and, for each, one concrete interface example.",
         "keywords": ["visibil", "feedback", "constraint", "consisten", "afford"],
         "answer": "Visibility - an elevator panel where it is clear which button calls the lift. Feedback - a "
                   "button that highlights and clicks when pressed. Constraints - greying out menu options that "
                   "are not permitted at this stage, or a key that fits a lock only one way. Consistency - Ctrl+C "
                   "for copy across the whole product. Affordances - a door handle that affords pulling, or an "
                   "icon that affords clicking."},
        {"q": "A team is designing a public transport ticket kiosk. Name three usability goals and two UX goals you would set, and say how you would measure each kind.",
         "keywords": ["safe", "learn", "efficien", "measur", "goal"],
         "answer": "Usability goals: easy to learn (first-time users must complete a purchase unaided), efficient "
                   "to use (a commuter must buy a known ticket in under thirty seconds) and safe to use (no "
                   "irreversible payment without confirmation). UX goals: satisfying and not frustrating. "
                   "Usability goals are measured objectively - task completion rate, time on task, error counts "
                   "in observed testing. UX goals are measured indirectly through satisfaction questionnaires, "
                   "interviews and observed emotional response, because they are subjective felt qualities."},
    ],
})


LECTURES.append({
    "num": 2,
    "slug": "cognitive-aspects",
    "title": "Cognitive Aspects",
    "short": "Cognitive Aspects",
    "lecture_label": "Lecture 2",
    "theme": "mind",
    "accent": "#7c5cff",
    "accent2": "#38c9a8",
    "tagline": "The six cognitive processes, their design implications, and the frameworks that explain user behaviour.",
    "hero_title": "Interacting with technology<br><em>is a cognitive act.</em>",
    "hero_sub": ("Attention, perception, memory, learning, language and reasoning are not background details - they "
                 "are the constraints your interface must be built around. This lecture gives you what users "
                 "<b>can and cannot</b> be expected to do, and a design implication for every one of them."),
    "badges": ["6 cognitive processes", "Design implications", "Mental models",
               "Gulfs of execution & evaluation", "External & distributed cognition"],
    "outcomes": [
        "Explain what cognition is and why understanding users matters.",
        "Describe the six cognitive processes and the design implication of each.",
        "Explain what mental models are and how to elicit them.",
        "Describe the gulfs of execution and evaluation.",
        "Compare information processing, distributed, external and embodied cognition.",
    ],
    "sections": [
        {
            "id": "what-cognition",
            "kicker": "01 - WHAT COGNITION IS",
            "title": "Fast thinking, slow thinking",
            "lead": ("Cognition is thinking, remembering, learning, daydreaming, decision-making, seeing, reading, "
                     "talking and writing. The lecture classifies it two ways, and both classifications say the "
                     "same thing in different words."),
            "blocks": [
                ("table", (["Classification", "Fast / automatic side", "Slow / deliberate side"], [
                    ["Norman (1993)", "<b>Experiential cognition</b> - effortless, in-the-moment, perceiving and reacting.",
                     "<b>Reflective cognition</b> - thinking, comparing, deciding, requires effort."],
                    ["Kahneman (2011)", "<b>Fast thinking</b> - 2+2, your own eye colour.",
                     "<b>Slow thinking</b> - 21 x 29, how many months have 31 days, the name of your first school."],
                ])),
                ("p", "Sort the lecture's own quiz items and the distinction becomes concrete: <i>2+2</i> and "
                      "<i>what colour are your eyes</i> are retrieved instantly; <i>21 x 29</i> and "
                      "<i>how many months have 31 days</i> require you to run a procedure."),
                ("list", [
                    "Interacting with technology <b>is</b> cognitive, so cognitive limitations are interface constraints.",
                    "Knowing the processes tells you what users <b>can and cannot be expected to do</b>.",
                    "It identifies and explains the nature and causes of the problems users encounter.",
                    "It supplies theories, modelling tools, guidance and methods that lead to better products.",
                ]),
                ("hook", ("MEMORY HOOK", "<b>A-P-M-L-R-P</b>: <b>A</b>ttention, <b>P</b>erception, <b>M</b>emory, "
                          "<b>L</b>earning, <b>R</b>eading-speaking-listening, <b>P</b>roblem-solving. Read it as "
                          "<i>&quot;A Person Might Learn Rather Poorly&quot;</i> - which is exactly the point of the lecture.")),
            ],
        },
        {
            "id": "attention",
            "kicker": "02 - PROCESS 1: ATTENTION",
            "title": "Selecting what to concentrate on",
            "lead": ("Attention is selecting things to concentrate on, at a point in time, from the mass of stimuli "
                     "around us. Focused and divided attention let us be selective, but limit our ability to keep "
                     "track of all events."),
            "blocks": [
                ("cards", [
                    ("Tullis (1987): the spacing study",
                     "Two hotel-price screens with <b>identical</b> information density (31%). The first took an "
                     "average of <b>5.5 seconds</b> to search, the second <b>3.2 seconds</b>. The difference was "
                     "spacing: screen one bunched the information together, screen two grouped characters into "
                     "vertical categories."),
                    ("Ophir et al. (2009): heavy multitaskers",
                     "Heavy multitaskers were <b>more</b> prone to being distracted than infrequent multitaskers, "
                     "and found it harder to filter irrelevant information."),
                    ("Lotteridge et al. (2015): the essay study",
                     "Heavy multitaskers were easily distracted, but could put that to good use when the distracting "
                     "sources were <b>relevant</b> to the task. Irrelevant information hurt performance."),
                ]),
                ("p", "The phone-and-driving argument is the lecture's flagship example, and it is examinable in "
                      "detail because the intuitive answer is wrong:"),
                ("list", [
                    "Reaction times to external events are longer while talking on the phone (Caird et al., 2018).",
                    "Response time is slower to <b>unexpected</b> events (Briggs et al., 2018), because phone drivers "
                    "lean on expectations about what will happen next.",
                    "Drivers try to imagine the other person's face, which competes for the processing resources "
                    "needed to notice what is in front of them.",
                    "<b>Hands-free is not safer</b> - the same cognitive processing happens when talking.",
                    "Talking to a front-seat passenger <em>is</em> less dangerous: both people can stop mid-sentence "
                    "when they see a hazard, whereas a remote person is not privy to what the driver sees and "
                    "carries on talking.",
                ]),
                ("note", ("DESIGN IMPLICATIONS - ATTENTION",
                          "Make information salient when it needs attending to. Use colour, ordering, spacing, "
                          "underlining, sequencing and animation to make things stand out. Avoid cluttering the "
                          "interface. Avoid using techniques just because the software allows it. Design ways of "
                          "supporting effective <b>switching and returning</b> to an interface.")),
                ("warn", ("EXAM TRAP",
                          "The hands-free question is a favourite. The correct answer is <b>no, hands-free is not "
                          "safer</b>, and the reason is cognitive, not manual - it is the conversation, not the "
                          "handset, that consumes attention.")),
            ],
        },
        {
            "id": "perception",
            "kicker": "03 - PROCESS 2: PERCEPTION",
            "title": "How information becomes experience",
            "lead": ("Perception is how information is acquired from the world and transformed into experiences. "
                     "The obvious implication is to design representations that are readily perceivable."),
            "blocks": [
                ("p", "Weller (2004) compared two screens: one that separated information with <b>colour contrast</b> "
                      "and one that used a <b>border</b>. People took less time to locate grouped items - the border "
                      "won. The counter-argument the slides raise: some argue too much white space on web pages is "
                      "detrimental, because it makes information hard to find."),
                ("list", [
                    "Icons should let users readily distinguish their meaning.",
                    "<b>Bordering and spacing</b> are effective visual ways of grouping information.",
                    "Sounds should be audible and distinguishable.",
                    "Speech output should let users distinguish between the set of spoken words.",
                    "Text should be legible and distinguishable from the background.",
                    "Tactile feedback should allow users to recognise and distinguish different meanings.",
                    "Research proper colour contrast: <b>yellow on black or blue is fine; yellow on green or white "
                    "is not</b>. Use haptic feedback judiciously.",
                ]),
                ("hook", ("MEMORY HOOK",
                          "Perception design reduces to one sentence: <b>make it distinguishable</b>. Text from "
                          "background, icon from icon, word from word, group from group. Every implication on the "
                          "slide is that sentence applied to a different sense.")),
            ],
        },
        {
            "id": "memory",
            "kicker": "04 - PROCESS 3: MEMORY",
            "title": "Encode, then retrieve",
            "lead": ("Memory involves first <b>encoding</b> and then <b>retrieving</b> knowledge. We do not remember "
                     "everything - memory filters and processes only what is attended to."),
            "blocks": [
                ("steps", [
                    ("Encoding", "The first stage: it determines which information is attended to and how it is interpreted."),
                    ("Processing depth", "The more attention paid, and the more it is compared with existing knowledge, the more likely it is to be remembered."),
                    ("Context binding", "Where and when you encoded something affects whether you can retrieve it later."),
                    ("Retrieval", "Recognition is far easier than recall."),
                ]),
                ("note", ("WHY YOU SHOULD NOT JUST READ THIS PAGE",
                          "The slides use HCI itself as the example: reflecting on the material, doing exercises, "
                          "discussing it and writing notes beats passively reading a book, listening to a lecture or "
                          "watching a video. Depth of processing, not exposure, drives retention.")),
                ("p", "Context is why the neighbour on the train is unrecognisable for a few seconds: you encoded "
                      "them in the hallway of your apartment block, and the retrieval cue is missing. And Henkel "
                      "(2014) found we remember <b>less</b> about objects we have photographed than about objects we "
                      "simply looked at."),
                ("cards", [
                    ("Recognition &gt; recall",
                     "Command-based interfaces require recalling a name from hundreds. GUIs give visually-based "
                     "options - menus and icons - that users only need to browse until they recognise one. History "
                     "lists, visited URLs, song titles and tabs all exist to support recognition memory."),
                    ("Visual cues beat arbitrary material",
                     "People are very good at remembering the colour of items, the location of objects and marks on "
                     "an object. They are bad at arbitrary material - birthdays and phone numbers. Try recalling "
                     "your grandparents' birthdays versus the covers of the last two films you rented."),
                ]),
                ("warn", ("THE 7 &plusmn; 2 TRAP - THE MOST EXAMINED POINT IN THIS LECTURE",
                          "Miller (1956) showed <b>immediate memory capacity</b> is limited to about seven items. "
                          "Designers then wrongly infer: seven menu options, seven icons, seven bullets, seven tabs. "
                          "That is an <b>inappropriate application of the theory</b> - people <em>scan</em> lists, "
                          "tabs and menu items for the one they want; they do not recall them from memory after "
                          "briefly seeing them. Sometimes a small number is good, but it depends on the task and the "
                          "available screen estate.")),
                ("p", "<b>Personal information management (PIM)</b> is the applied case: vast numbers of documents, "
                      "images, music files, video clips, emails, attachments and bookmarks, all needing to be saved, "
                      "named and found again. Naming is the most common encoding method and the hardest to recall at "
                      "scale."),
                ("steps", [
                    ("Bergman &amp; Whittaker (2016), step 1", "Decide what stuff to keep."),
                    ("Step 2", "Decide how to organise it when storing."),
                    ("Step 3", "Decide which strategies to use to retrieve it later."),
                ]),
                ("list", [
                    "Most people use folders and naming, with a strong preference for <b>scanning</b> across and "
                    "within folders rather than searching.",
                    "Search engines only help if you know the name of the file; smart search helps with partial names "
                    "or first letters (Apple's Spotlight).",
                    "File systems should optimise <b>both</b> recall-directed search and recognition-based scanning.",
                    "Richer encoding helps: colour, flagging, images, flexible text, time stamping.",
                    "<b>SenseCam</b> (Microsoft Research) is a wearable that intermittently takes photos without user "
                    "intervention; revisiting the images improved memory in people with Alzheimer's.",
                    "<b>Multifactor authentication</b> increases memory load - ZIP code, birthplace, a memorable date, "
                    "first school - to increase security. Password managers reduce that load to one master password; "
                    "biometrics may remove passwords entirely.",
                    "<b>Digital forgetting</b> (Sas and Whittaker, 2013): after a break-up, shared photos are "
                    "emotionally painful. Harvesting and transforming content - turning photos of an ex into an "
                    "abstract collage - helps with closure.",
                ]),
                ("note", ("DESIGN IMPLICATIONS - MEMORY",
                          "Do not overload users' memories with complicated procedures. Design interfaces that "
                          "promote <b>recognition rather than recall</b>. Provide various ways of encoding "
                          "information - categories, colour, flagging, time stamping.")),
            ],
        },
        {
            "id": "learning-language",
            "kicker": "05 - PROCESSES 4, 5 & 6",
            "title": "Learning, language, and reflective cognition",
            "lead": ("The remaining three processes are shorter on the slides but each carries its own design "
                     "implications, and the exam treats them as equals."),
            "blocks": [
                ("cards", [
                    ("4. Learning",
                     "Two senses: learning <i>how to use</i> an application, and using an application to <i>understand "
                     "a topic</i>. People find it hard to learn by following instructions in a manual - they prefer "
                     "to <b>learn by doing</b>. Two types: <b>incidental</b> (recognising faces, what you did today) "
                     "and <b>intentional</b> (studying for an exam, learning to cook). Intentional is much harder, "
                     "which is why digital media, animations and VR have been built to support it. "
                     "<i>Implications:</i> design interfaces that encourage exploration; design interfaces that "
                     "constrain and guide learners; dynamically link concepts and representations."),
                    ("5. Reading, speaking &amp; listening",
                     "Ease differs by person and mode. Many prefer listening to reading; reading can be quicker than "
                     "speaking or listening; <b>listening requires less cognitive effort</b> than reading or "
                     "speaking; dyslexic users have difficulty recognising written words. Applications: "
                     "speech-recognition systems, speech-output systems (text-to-speech for blind users), and "
                     "natural-language systems. <i>Implications:</i> keep speech-based menus and instructions short; "
                     "accentuate the intonation of artificial voices because they are harder to understand than "
                     "human ones; let users enlarge text."),
                    ("6. Problem-solving, planning, reasoning &amp; decision-making",
                     "All involve <b>reflective</b> cognition - thinking about what to do, what the options are and "
                     "what the consequences would be. Often conscious, often discussed with others, and often "
                     "supported by artifacts such as maps, books, pen and paper. <i>Implications:</i> provide extra "
                     "information and functions for users who want to understand how to do an activity better; use "
                     "simple computational aids for rapid decision-making on the move."),
                ]),
                ("note", ("THE APP DILEMMA",
                          "Gardner and Davis (2013) argue the &quot;app mentality&quot; makes people risk-averse: "
                          "they rely on a multitude of apps, grow anxious, become unable to decide alone, and resort "
                          "to looking things up and comparing notes on social media. The slides pose it as an open "
                          "question, so an exam answer should present it as a debated claim, not a finding.")),
            ],
        },
        {
            "id": "mental-models",
            "kicker": "06 - COGNITIVE FRAMEWORK 1",
            "title": "Mental models",
            "lead": ("Cognitive frameworks explain and predict user behaviour at the interface, based on theories of "
                     "behaviour, focusing on the mental processes that take place and on the use of artifacts and "
                     "representations. The best known is the mental model."),
            "blocks": [
                ("p", "Craik (1943) described mental models as <b>internal constructions of some aspect of the "
                      "external world that enable predictions to be made</b>. They cover both how to use a system "
                      "(what to do next) and how the system works (what to do with unfamiliar systems or unexpected "
                      "situations). They involve both unconscious and conscious processes, and images and analogies "
                      "get activated."),
                ("table", (["Model depth", "Meaning", "Example"], [
                    ["Deep model", "You understand the underlying mechanism.", "Knowing how a car engine works."],
                    ["Shallow model", "You know the procedure but not the mechanism.", "Knowing how to drive a car."],
                ])),
                ("cards", [
                    ("The thermostat problem (Kempton, 1996)",
                     "You come home to a cold house. Do you set the thermostat to maximum or to the temperature you "
                     "want? Many people set it to maximum, which does not help. The erroneous model is the "
                     "<b>general valve theory</b> - a &quot;more is more&quot; principle generalised from gas pedals, "
                     "gas cookers, taps and volume knobs - whereas a thermostat behaves like an <b>on-off switch</b>."),
                    ("The oven variant",
                     "Starving, with an uncooked pizza and an electric oven: do you preheat to 375 as instructed, or "
                     "turn it higher to warm up faster? Same erroneous valve model, same wrong answer."),
                    ("Buttons pressed twice",
                     "Elevators and pedestrian crossings: people hit the button at least twice because they think it "
                     "will make the lights change faster or the lift arrive sooner. Norman (1983) - models of "
                     "interactive devices are poor, incomplete, easily confusable, and based on inappropriate "
                     "analogies and superstition."),
                ]),
                ("p", "The lecture's ATM exercise is the standard way of exposing how shallow your own model is: how "
                      "much can you withdraw, what would happen at another machine, what is on the magnetic strip, "
                      "what happens if you enter the wrong number, why are there pauses between steps, why does the "
                      "card stay inside, and why do you count the money? Payne (1991) found people frequently resort "
                      "to <b>analogies</b>, and their accounts varied greatly and were often ad hoc."),
                ("note", ("HOW UX HELPS PEOPLE BUILD BETTER MODELS",
                          "Clear and easy-to-use instructions; appropriate tutorials and context-sensitive guidance; "
                          "online videos and chatbot help windows; <b>transparency</b> so interfaces are intuitive; "
                          "and <b>affordances</b> that show what actions the interface allows - swiping, clicking, "
                          "selecting.")),
            ],
        },
        {
            "id": "gulfs",
            "kicker": "07 - COGNITIVE FRAMEWORK 2",
            "title": "The gulfs of execution and evaluation",
            "lead": "The gulfs explicate the gaps that exist between the user and the interface.",
            "blocks": [
                ("table", (["Gulf", "Direction", "The question the user is asking"], [
                    ["Gulf of <b>execution</b>", "User &rarr; physical system",
                     "How do I do what I intend? Is it obvious what to do next?"],
                    ["Gulf of <b>evaluation</b>", "Physical system &rarr; user",
                     "Did it work? Can I tell the system's state from what it shows me?"],
                ])),
                ("list", [
                    "Bridging the gulfs <b>reduces the cognitive effort</b> required to perform tasks.",
                    "The gulfs reveal whether an interface increases or decreases cognitive load.",
                    "They also reveal whether it is obvious what to do next.",
                ]),
                ("hook", ("MEMORY HOOK",
                          "<b>eXecution goes out, eValuation comes back.</b> Execution is the gap on the way "
                          "<i>to</i> the machine; evaluation is the gap on the way <i>back</i> to you. "
                          "Visibility bridges execution; feedback bridges evaluation.")),
            ],
        },
        {
            "id": "other-frameworks",
            "kicker": "08 - COGNITIVE FRAMEWORKS 3, 4, 5 & 6",
            "title": "Beyond the head",
            "lead": ("The remaining frameworks all push in one direction: cognition is not confined to the inside of "
                     "a single skull."),
            "blocks": [
                ("cards", [
                    ("3. Information processing",
                     "Conceptualises human performance in metaphorical terms of information-processing stages. "
                     "<b>Limitation:</b> it models mental activities that happen exclusively inside the head, and so "
                     "does not adequately account for how people interact with computers and other devices in the "
                     "real world."),
                    ("4. Distributed cognition (Hutchins, 1995)",
                     "Concerned with cognitive phenomena <b>across</b> individuals, artifacts, and internal and "
                     "external representations, described as propagation across representational state. Information "
                     "is transformed through different media - computers, displays, paper, heads. It examines the "
                     "distributed problem-solving that takes place, verbal and non-verbal behaviour, coordinating "
                     "mechanisms such as rules and procedures, the communication as collaborative activity "
                     "progresses, and how knowledge is shared and accessed."),
                    ("5. External cognition",
                     "Explains how we interact with external representations - maps, notes, diagrams - what the "
                     "cognitive benefits are, and how they extend our cognition."),
                    ("6. Embodied interaction",
                     "A newer approach in which user interfaces merge seamlessly with the physical world, making use "
                     "of the physical objects that surround us."),
                ]),
                ("p", "External cognition has two examinable mechanisms:"),
                ("table", (["Mechanism", "What it does", "Example"], [
                    ["Externalising to reduce memory load",
                     "Offload what must be remembered onto the world.",
                     "Diaries, reminders, calendars, notes, shopping lists, to-do lists. Post-its, piles and marked "
                     "emails also encode <b>priority</b> by where they are placed. They remind us <i>that</i> we need "
                     "to do something, <i>what</i> to do, and <i>when</i> to do it."],
                    ["Computational offloading",
                     "Using a tool together with an external representation to carry out a computation.",
                     "234 x 456 in your head, on paper, or with a calculator. Now try "
                     "CCXXXIIII x CCCCXXXXXVI - the identical sum in Roman numerals is far harder, proving the "
                     "<b>representation</b>, not the arithmetic, is doing the work."],
                ])),
                ("hook", ("MEMORY HOOK",
                          "The Roman-numeral sum is the single best exam anchor in this lecture. Same numbers, same "
                          "answer, radically different difficulty &rArr; <b>the representation carries part of the "
                          "cognition</b>. That one sentence answers most external-cognition questions.")),
            ],
        },
    ],
    "mistakes": [
        ("&quot;Miller's 7 &plusmn; 2 means menus should have seven items.&quot;",
         "That is the inappropriate application the lecture explicitly warns against. 7 &plusmn; 2 concerns "
         "<b>immediate memory capacity</b> - recalling briefly-seen items. Menus, tabs and bullet lists are "
         "<b>scanned</b>, not recalled, so the limit does not apply. The right number depends on task and screen estate."),
        ("&quot;Hands-free phones are safer for driving.&quot;",
         "No. The same cognitive processing happens whether or not you hold the handset. What makes a front-seat "
         "passenger safer is that they can see the hazard and stop talking; a remote person cannot."),
        ("Treating recall and recognition as interchangeable.",
         "Recognition is much easier. Command interfaces demand recall; GUIs, history lists and menus supply "
         "recognition. &quot;Recognition rather than recall&quot; is a design implication, and later a Nielsen heuristic."),
        ("Confusing the two gulfs.",
         "Execution is the distance from the user to the physical system - doing. Evaluation is the distance from "
         "the physical system back to the user - understanding what happened."),
        ("&quot;Distributed cognition just means teamwork.&quot;",
         "It concerns cognitive phenomena propagating across <b>individuals, artifacts and representations</b>, "
         "including displays, paper and computers - not only people."),
        ("Calling information processing a complete account.",
         "Its stated limitation is that it models activities happening exclusively inside the head and does not "
         "account for real-world interaction with devices."),
    ],
    "cheat": (["Concept", "Shortest correct answer"], [
        ["Cognition", "Thinking, remembering, learning, seeing, reading, deciding - split into experiential vs reflective, or fast vs slow."],
        ["Six processes", "Attention, perception, memory, learning, reading-speaking-listening, problem-solving/planning/reasoning/deciding."],
        ["Attention implication", "Make it salient, avoid clutter, support switching and returning."],
        ["Perception implication", "Make everything distinguishable - text, icons, sounds, groups; borders and spacing group well."],
        ["Memory implication", "Recognition rather than recall; do not overload; give many ways to encode."],
        ["7 &plusmn; 2", "Immediate memory capacity; misapplied when used to cap menu or tab counts."],
        ["Mental model", "Internal construction of part of the external world that enables predictions."],
        ["Gulf of execution", "Distance from the user to the physical system."],
        ["Gulf of evaluation", "Distance from the physical system to the user."],
        ["Distributed cognition", "Cognition propagating across individuals, artifacts and representations."],
        ["External cognition", "How we interact with external representations; includes externalising memory and computational offloading."],
        ["Embodied interaction", "Interfaces merging with the physical world and the objects around us."],
    ]),
    "quiz": [
        {"q": "A designer caps every toolbar at seven icons, citing Miller (1956). What is wrong with the reasoning?",
         "options": ["Toolbar icons are scanned and recognised, not recalled from immediate memory",
                     "Miller's number was actually five",
                     "The limit applies only to auditory information",
                     "Nothing - seven is the correct maximum"], "correct": 0,
         "why": "7 &plusmn; 2 describes immediate memory capacity - items briefly seen or heard and then recalled. "
                "Users browse a toolbar until they recognise the icon they want, so no recall is involved. The number "
                "was seven plus or minus two, not five; the limit is not sense-specific; and the lecture explicitly "
                "lists the seven-item toolbar as a misapplication."},
        {"q": "Tullis (1987) found one hotel screen was searched 2.3 seconds faster than another with identical information density. What explained the difference?",
         "options": ["Spacing - grouping characters into vertical categories",
                     "Colour contrast between fields",
                     "Fewer words on the faster screen",
                     "Larger font size"], "correct": 0,
         "why": "Both screens had 31% density, so the amount of information was not the variable. The faster screen "
                "grouped characters into vertical categories; the slower one bunched everything together. Colour was "
                "Weller's (2004) study, not Tullis's, and word count and font size were held constant."},
        {"q": "You arrive home to a cold house and set the thermostat to maximum to warm it faster. Which error does this illustrate?",
         "options": ["An erroneous mental model based on general valve theory",
                     "A gulf of evaluation",
                     "A failure of computational offloading",
                     "Divided attention"], "correct": 0,
         "why": "Kempton (1996) explains it as generalising a &quot;more is more&quot; valve model from taps and gas "
                "pedals to a device that actually works like an on-off switch. It is not a gulf of evaluation, which "
                "concerns reading the system's state; not offloading, which concerns tools and representations; and "
                "not attention."},
        {"q": "Which of these is an example of computational offloading?",
         "options": ["Doing a multiplication on paper instead of in your head",
                     "Putting a Post-it on the fridge to remember to buy a card",
                     "Recognising a colleague out of context",
                     "Greying out an unavailable menu item"], "correct": 0,
         "why": "Computational offloading is using a tool together with an external representation to carry out a "
                "computation. The Post-it is externalising to reduce memory load - a related but distinct mechanism. "
                "Recognition out of context is a memory-and-context point, and greying out a menu item is the "
                "constraints design principle."},
        {"q": "An interface shows no indication of whether a long upload succeeded. Which gulf is widest?",
         "options": ["The gulf of evaluation", "The gulf of execution",
                     "The gulf of attention", "The gulf of affordance"], "correct": 0,
         "why": "Evaluation is the distance from the physical system back to the user - can they tell what the system "
                "has done? Execution would be the problem if the user could not work out how to start the upload. "
                "The other two options are not gulfs named in this framework."},
        {"q": "Which statement about the information-processing framework is the limitation the lecture states?",
         "options": ["It models mental activities happening exclusively inside the head",
                     "It cannot explain memory encoding",
                     "It requires eye-tracking equipment",
                     "It applies only to expert users"], "correct": 0,
         "why": "The stated limitation is that it is based on modelling activities inside the head and so does not "
                "adequately account for how people interact with computers and devices in the real world - which is "
                "exactly the gap distributed and external cognition were developed to fill."},
    ],
    "lab": [
        ("Your file manager relies entirely on users typing exact file names into a search box. Diagnose the problem "
         "with the memory material and propose three fixes.",
         "It forces <b>recall</b> of arbitrary material, which is what people are worst at, and search engines only "
         "help when the name is known. Fixes: (1) support <b>recognition-based scanning</b> - browsable folders, "
         "thumbnails, recent-items lists; (2) support <b>richer encoding</b> - colour, flags, tags, time stamps and "
         "images so a file has several retrieval cues; (3) add smart partial-name search that lists relevant files "
         "from the first letters, as Spotlight does."),
        ("A hospital operating room adds a fourth real-time monitor. Argue, using attention research, what this does "
         "to the clinician and what the design should do instead.",
         "Multitasking causes people to lose their train of thought, make errors and start over, and clinicians "
         "already need constant attention to check for anomalous data, requiring new attention and scanning "
         "strategies. Adding a screen raises the filtering cost rather than the information supplied. The design "
         "should make anomalies <b>salient</b> - alerting only on deviation, using colour, ordering and spacing - "
         "avoid clutter, and support switching and returning so an interrupted clinician can resume where they left off."),
        ("Explain, using two frameworks from this lecture, why a pilot's paper checklist is not merely a memory aid.",
         "Under <b>external cognition</b> the checklist is an external representation that reduces memory load and "
         "performs computational offloading - the order of items encodes the procedure so the pilot does not have to "
         "derive it. Under <b>distributed cognition</b> the cognitive process is spread across the pilot, co-pilot, "
         "the checklist artifact and the instrument displays, with information propagating across representational "
         "states and coordinating mechanisms - the crew's rules for calling and confirming items - doing work no "
         "individual head is doing alone."),
    ],
    "branches": [
        ("What is cognition",
         "Thinking, remembering, learning, daydreaming, decision-making, seeing, reading, talking and writing, classified as experiential versus reflective, or fast versus slow.",
         ["Norman (1993) distinguishes experiential from reflective cognition.",
          "Kahneman (2011) distinguishes fast from slow thinking.",
          "Interacting with technology is cognitive, so cognitive limits are design constraints.",
          "Understanding cognition tells designers what users can and cannot be expected to do.",
          "It identifies and explains the nature and causes of the problems users encounter.",
          "It supplies theories, modelling tools, guidance and methods for better products."],
         [("Fast items", "2+2 and the colour of your own eyes are retrieved without effort."),
          ("Slow items", "21 x 29, how many months have 31 days, and the name of your first school each require running a procedure.")]),
        ("Attention",
         "Selecting things to concentrate on at a point in time from the mass of stimuli around us, using audio and/or visual senses.",
         ["Focused and divided attention allow selectivity but limit tracking of all events.",
          "Information at the interface should be structured to capture attention using perceptual boundaries, colour, reverse video, sound and flashing lights.",
          "Multitasking can cause people to lose their train of thought, make errors and start over.",
          "Ophir et al. (2009): heavy multitaskers are more easily distracted and filter irrelevant information poorly.",
          "Lotteridge et al. (2015): heavy multitaskers benefit when distracting sources are relevant, and suffer when irrelevant.",
          "Design implications: make information salient, use colour, ordering, spacing, underlining, sequencing and animation, avoid clutter, support switching and returning."],
         [("Tullis (1987)", "Two hotel screens with identical 31% information density took 5.5 versus 3.2 seconds to search; vertical grouping and spacing explained the gap."),
          ("Phones and driving", "Reaction times lengthen, unexpected events are missed, and drivers imagine the other person's face, which competes for processing resources."),
          ("Hands-free", "Not safer, because the same cognitive processing occurs; a front-seat passenger is safer only because they can see the hazard and stop mid-sentence.")]),
        ("Perception",
         "How information is acquired from the world and transformed into experiences; the implication is to design readily perceivable representations.",
         ["Text should be legible and distinguishable from the background.",
          "Icons should be easy to distinguish and read.",
          "Sounds should be audible and distinguishable, and speech output distinguishable word by word.",
          "Tactile feedback should let users recognise and distinguish meanings.",
          "Bordering and spacing are effective visual ways of grouping information.",
          "Yellow on black or blue is acceptable contrast; yellow on green or white is not.",
          "Haptic feedback should be used judiciously."],
         [("Weller (2004)", "People located grouped items faster when a border was used than when colour contrast alone separated them."),
          ("White space debate", "Some argue too much white space on web pages makes information hard to find, so grouping must be deliberate rather than merely airy.")]),
        ("Memory",
         "Encoding then retrieving knowledge, filtered by what is attended to and strongly affected by context.",
         ["Encoding determines which information is attended to and how it is interpreted.",
          "The more something is processed and compared with existing knowledge, the more likely it is remembered.",
          "Context affects the extent to which information can subsequently be retrieved.",
          "Recognition is much better than recall.",
          "People remember visual cues well - colour, location, marks - and arbitrary material badly.",
          "Henkel (2014): we remember less about objects we have photographed than objects we merely observed.",
          "Miller's 7 plus or minus 2 concerns immediate memory capacity and is misapplied to menu, tab and bullet counts.",
          "Personal information management involves deciding what to keep, how to organise it and how to retrieve it (Bergman and Whittaker, 2016).",
          "Design implications: do not overload, promote recognition rather than recall, provide many ways of encoding."],
         [("The neighbour on the train", "Encoded only in the apartment hallway, so out of context the person is briefly unrecognisable."),
          ("SenseCam", "A wearable that intermittently photographs the day without user intervention; revisiting images improved memory in people with Alzheimer's."),
          ("Multifactor authentication", "ZIP code, birthplace, memorable date and first school raise security by raising memory load; password managers reduce it to one master password."),
          ("Digital forgetting", "Sas and Whittaker (2013) suggest harvesting and transforming painful content, such as turning photos of an ex into an abstract collage, to help with closure.")]),
        ("Learning",
         "Accumulating skills and knowledge involving memory; people find it hard to learn from manuals and prefer to learn by doing.",
         ["Incidental learning covers recognising faces or recalling what you did today.",
          "Intentional learning covers studying for an exam or learning to cook, and is much harder.",
          "Technologies developed to help include digital media, animations and VR.",
          "Design implications: encourage exploration, constrain and guide learners, and dynamically link concepts and representations."],
         [("Learning by doing", "Users skip the manual and press buttons, which is why exploration must be safe and reversible rather than punished.")]),
        ("Reading, speaking and listening",
         "The ease of each mode differs by person and situation, which is why interfaces should not assume one channel suits everyone.",
         ["Many people prefer listening to reading.",
          "Reading can be quicker than speaking or listening.",
          "Listening requires less cognitive effort than reading or speaking.",
          "Dyslexic users have difficulties understanding and recognising written words.",
          "Speech-recognition systems accept spoken commands; speech-output systems generate artificial speech; natural-language systems accept typed questions.",
          "Design implications: keep speech menus and instructions short, accentuate intonation in artificial voices, and allow text to be enlarged."],
         [("Text-to-speech", "Written-text-to-speech systems for blind users are the clearest case of matching the channel to the user rather than the content.")]),
        ("Problem solving, planning, reasoning and decision making",
         "Reflective cognition: thinking about what to do, what the options are, and what the consequences would be.",
         ["Often involves conscious processes and discussion with others or oneself.",
          "Often involves artifacts such as maps, books, pen and paper.",
          "May involve working through different scenarios and deciding which is the best option.",
          "Design implications: provide additional information and functions for users who want to carry out an activity more effectively, and simple computational aids for rapid decision-making on the move."],
         [("The app dilemma", "Gardner and Davis (2013) argue reliance on apps makes people risk-averse, anxious and unable to decide alone - presented by the slides as a claim to debate, not a settled finding.")]),
        ("Mental models",
         "Internal constructions of some aspect of the external world that enable predictions to be made (Craik, 1943).",
         ["Cover both how to use the system and how the system works.",
          "Involve unconscious and conscious processes, activating images and analogies.",
          "Deep models explain mechanism; shallow models cover procedure only.",
          "Models of interactive devices are often poor, incomplete, easily confusable and based on inappropriate analogies and superstition (Norman, 1983).",
          "UX can improve models through clear instructions, tutorials, contextual guidance, videos and chatbots, transparency and affordances."],
         [("Thermostat and oven", "Kempton (1996): people apply a general valve, more-is-more model to a device that behaves like an on-off switch."),
          ("Double-pressing buttons", "People press elevator and pedestrian-crossing buttons twice, believing it speeds up the response."),
          ("The ATM exercise", "Asking how an ATM works exposes how shallow a model is; Payne (1991) found people resort to analogies and give varied, ad hoc accounts.")]),
        ("Gulfs of execution and evaluation",
         "The gaps that exist between the user and the interface, in each direction.",
         ["The gulf of execution is the distance from the user to the physical system.",
          "The gulf of evaluation is the distance from the physical system to the user.",
          "Bridging the gulfs reduces the cognitive effort required to perform tasks.",
          "The gulfs reveal whether an interface increases or decreases cognitive load and whether it is obvious what to do next."],
         [("Bridging execution", "Visible, well-labelled controls tell the user how to express their intention."),
          ("Bridging evaluation", "Progress indicators and confirmation messages let the user read the system's new state.")]),
        ("Distributed, external and embodied cognition",
         "Frameworks that place cognition outside a single head, across people, artifacts and representations.",
         ["Information processing conceptualises human performance as metaphorical stages, but models only what happens inside the head.",
          "Distributed cognition (Hutchins, 1995) concerns cognitive phenomena across individuals, artifacts and representations, described as propagation across representational state.",
          "It examines distributed problem solving, verbal and non-verbal behaviour, coordinating mechanisms, communication, and how knowledge is shared and accessed.",
          "External cognition explains how we interact with external representations such as maps, notes and diagrams.",
          "Externalising reduces memory load through diaries, reminders, calendars, lists, Post-its and marked emails.",
          "Computational offloading uses a tool with an external representation to carry out a computation.",
          "Embodied interaction merges user interfaces with the physical world and the objects around us."],
         [("Roman numerals", "234 x 456 versus CCXXXIIII x CCCCXXXXXVI: the identical sum is far harder in the second notation, proving the representation carries part of the cognition."),
          ("Post-it placement", "Where a note is placed encodes priority, so the artifact stores more than its text.")]),
    ],
    "exam_mcq": [
        {"q": "Which pair correctly matches Norman's and Kahneman's classifications of cognition?",
         "options": ["Experiential aligns with fast thinking; reflective aligns with slow thinking",
                     "Experiential aligns with slow thinking; reflective aligns with fast thinking",
                     "Both authors describe the same three-stage model",
                     "Neither classification distinguishes effortful from effortless cognition"],
         "correct": 0,
         "why": "Norman's experiential cognition is effortless and in-the-moment, matching Kahneman's fast thinking; "
                "reflective cognition is effortful comparison and decision-making, matching slow thinking. Pairing experiential with slow thinking reverses them, and the claims of a shared three-stage model or of no effort distinction both contradict the lecture."},
        {"q": "According to the lecture, why is talking to a front-seat passenger less dangerous than talking on a phone?",
         "options": ["The passenger can see a hazard and stop mid-sentence, whereas a remote person carries on talking",
                     "Passengers speak more quietly, so less attention is consumed",
                     "Holding the handset is the main source of danger",
                     "Passengers use fewer words per minute"],
         "correct": 0,
         "why": "Both conversations use the same cognitive processing, so the difference is shared awareness: the "
                "passenger is privy to what the driver sees and pauses; the remote person is not. Holding the handset "
                "is not the main issue - hands-free is explicitly stated to be no safer. Volume and word rate are not "
                "in the slides."},
        {"q": "A GUI shows a history list of recently visited URLs. Which cognitive principle is it exploiting?",
         "options": ["Recognition is better than recall",
                     "Immediate memory capacity is 7 plus or minus 2",
                     "Computational offloading",
                     "Divided attention"],
         "correct": 0,
         "why": "History lists let users browse until they recognise the item, avoiding recall of an exact URL. "
                "7 plus or minus 2 is about immediate memory capacity, not list design. Computational offloading "
                "involves performing a computation with a tool. Divided attention concerns splitting focus across "
                "tasks."},
        {"q": "Which description matches DISTRIBUTED cognition rather than external cognition?",
         "options": ["Cognitive phenomena propagating across individuals, artifacts and representational states",
                     "Using a shopping list to remember what to buy",
                     "Doing a sum on paper rather than in your head",
                     "Placing a Post-it where its position signals priority"],
         "correct": 0,
         "why": "Hutchins' distributed cognition is defined as propagation across representational state, spanning "
                "individuals and artifacts. The other three are external-cognition examples: externalising to reduce "
                "memory load, computational offloading, and externalising priority."},
        {"q": "Which design implication belongs to PERCEPTION rather than memory?",
         "options": ["Ensure text is legible and distinguishable from the background",
                     "Promote recognition rather than recall",
                     "Provide colour, flagging and time stamping so files can be encoded richly",
                     "Avoid complicated procedures for carrying out tasks"],
         "correct": 0,
         "why": "Legibility and distinguishability are perception implications. The remaining three are the memory "
                "implications listed in the lecture."},
        {"q": "Henkel (2014) found that photographing an object affects memory in which way?",
         "options": ["We remember less about photographed objects than about objects observed with the naked eye",
                     "We remember more, because the photograph acts as a retrieval cue",
                     "Memory is unaffected but retrieval is slower",
                     "Only visual details are lost, while names are retained"],
         "correct": 0,
         "why": "The finding is that photographing reduces what is remembered about the object, which the lecture "
                "uses to show that attention and depth of processing, not exposure, drive encoding."},
    ],
    "exam_short": [
        {"q": "List the six cognitive processes and give one design implication for each.",
         "keywords": ["attention", "perception", "memory", "learning", "reading", "problem"],
         "answer": "Attention - make information salient and avoid clutter, support switching and returning. "
                   "Perception - make text, icons, sounds and groups distinguishable, using borders and spacing. "
                   "Memory - promote recognition rather than recall, do not overload, provide many encodings. "
                   "Learning - encourage exploration, constrain and guide learners, link concepts and representations. "
                   "Reading, speaking and listening - keep speech menus short, accentuate artificial intonation, "
                   "allow larger text. Problem-solving, planning, reasoning and decision-making - provide extra "
                   "information for users who want to work more effectively, and computational aids for decisions on "
                   "the move."},
        {"q": "Explain why applying Miller's 7 &plusmn; 2 to menu length is an inappropriate use of the theory.",
         "keywords": ["immediate", "recall", "scan", "memory"],
         "answer": "7 &plusmn; 2 describes immediate memory capacity - how many items people can hold and recall after "
                   "briefly seeing or hearing them. Menu items, tabs, bullets and icons are visible on screen, so "
                   "users scan them and recognise the one they want rather than recalling them from memory. The "
                   "constraint therefore does not apply. Sometimes a small number of items is still good, but the "
                   "right number depends on the task and the available screen estate, not on Miller's figure."},
        {"q": "Define the gulf of execution and the gulf of evaluation, and say how each is bridged.",
         "keywords": ["execution", "evaluation", "distance", "system"],
         "answer": "The gulf of execution is the distance from the user to the physical system - the difficulty of "
                   "turning an intention into an action the system accepts; it is bridged by visible, "
                   "clearly-labelled controls and affordances that show what can be done. The gulf of evaluation is "
                   "the distance from the physical system back to the user - the difficulty of working out what "
                   "state the system is now in; it is bridged by feedback such as progress indicators and "
                   "confirmations. Bridging both reduces the cognitive effort required to perform tasks."},
        {"q": "What is a mental model, and why are people's models of interactive devices usually poor?",
         "keywords": ["model", "predict", "shallow", "analog"],
         "answer": "A mental model is an internal construction of some aspect of the external world that enables "
                   "predictions to be made (Craik, 1943), covering both how to use a system and how it works. "
                   "Models of interactive devices are poor because they are incomplete, easily confusable and based "
                   "on inappropriate analogies and superstition (Norman, 1983): people generalise a "
                   "more-is-more valve model to thermostats, and press elevator buttons twice believing it speeds "
                   "the lift. Models are typically shallow - procedure without mechanism."},
        {"q": "Explain computational offloading using the lecture's own example.",
         "keywords": ["offload", "representation", "roman", "tool"],
         "answer": "Computational offloading is using a tool in conjunction with an external representation to carry "
                   "out a computation. The lecture's example asks you to compute 234 x 456 in your head, on paper "
                   "and with a calculator, then to compute the identical sum written as "
                   "CCXXXIIII x CCCCXXXXXVI. Both sums have the same answer, but the Roman notation is far harder, "
                   "showing that the external representation - not just the tool - performs part of the cognitive "
                   "work."},
        {"q": "A note-taking app wants to help users find notes months later. Apply the memory material to justify three features.",
         "keywords": ["recognition", "encod", "context", "search"],
         "answer": "First, support recognition rather than recall: show browsable previews, thumbnails and recent "
                   "lists rather than relying on the user typing an exact title, because naming is the most common "
                   "encoding method and the hardest to recall at scale. Second, support richer encoding: colour, "
                   "tags, flags, images and time stamps give a note several independent retrieval cues, and people "
                   "remember visual cues such as colour and location far better than arbitrary text. Third, restore "
                   "context: showing where and when a note was created helps retrieval, because context strongly "
                   "affects whether encoded information can be retrieved. Adding smart partial-name search covers "
                   "the recall-directed strategy for the cases where the user does remember the name."},
    ],
})


LECTURES.append({
    "num": 3,
    "slug": "emotional-interaction",
    "title": "Emotional Interaction",
    "short": "Emotional Interaction",
    "lecture_label": "Lecture 3",
    "theme": "ember",
    "accent": "#ff6a5e",
    "accent2": "#ffb454",
    "tagline": "Expressive interfaces, frustration, affective computing, persuasive technology and anthropomorphism.",
    "hero_title": "HCI used to ask <em>does it work.</em><br>Now it asks <em>how does it feel.</em>",
    "hero_sub": ("Emotional interaction is concerned with how we feel and react when interacting with technologies - "
                 "what makes us happy, sad, annoyed, anxious, frustrated or motivated, and how that can be designed "
                 "for, detected, and deliberately used to change behaviour."),
    "badges": ["Ortony's 3 levels", "Expressive interfaces", "Frustrating interfaces",
               "Affective computing & emotional AI", "Persuasive tech", "Anthropomorphism"],
    "outcomes": [
        "Explain how emotion relates to the user experience.",
        "Give examples of interfaces that are both pleasurable and usable.",
        "Explain visceral, behavioural and reflective design.",
        "Describe affective computing and emotional AI, and the techniques they use.",
        "Describe how technologies can be designed to change attitudes and behaviour.",
    ],
    "sections": [
        {
            "id": "emotion-ux",
            "kicker": "01 - EMOTION AND THE USER EXPERIENCE",
            "title": "From efficient systems to felt responses",
            "lead": ("HCI has traditionally been about designing efficient and effective systems. It is now also "
                     "about designing interactive systems that make people <b>respond in certain ways</b> - to be "
                     "happy, to be trusting, to learn, to be motivated."),
            "blocks": [
                ("list", [
                    "What makes us happy, sad, annoyed, anxious, frustrated, motivated or delirious - and how to "
                    "translate that into aspects of the user experience.",
                    "Why people become emotionally attached to certain products, such as virtual pets.",
                    "Whether social robots can reduce loneliness and improve wellbeing.",
                    "How to change human behaviour through emotive feedback.",
                ]),
                ("p", "Emotional intelligence is the starting point: how people express themselves and read each "
                      "other through facial expressions, body language, gestures and tone of voice. When people are "
                      "happy they laugh and relax their body posture; when angry they screw up their face. But "
                      "Baumeister et al. (2007) argue the relationship between emotion and behaviour is "
                      "<b>more complex than a single cause-and-effect model</b> - a point worth quoting in an exam."),
                ("table", (["Emotion type", "Character", "Example"], [
                    ["<b>Automatic (affect)</b>", "Rapid, dissipates quickly.", "A fit of anger."],
                    ["<b>Conscious</b>", "Develops slowly, takes a long time to go, involves reflection.", "Jealousy."],
                ])),
                ("warn", ("THE DESIGN DILEMMA THE SLIDES POSE",
                          "Should an interface be designed to improve how we feel - and if so, how? Our moods change "
                          "continuously, so how would the interface keep track and know when to act? Which moods "
                          "match which kinds of interface? These are posed as <b>open questions</b>; an exam answer "
                          "should treat them as unresolved design problems, not solved ones.")),
            ],
        },
        {
            "id": "ortony",
            "kicker": "02 - THE THREE-LEVEL MODEL",
            "title": "Ortony, Norman et al. (2005): visceral, behavioural, reflective",
            "lead": ("The model's central claim is that our emotional state changes how we <b>think</b>, and "
                     "therefore that design must address three levels at once."),
            "blocks": [
                ("cards", [
                    ("Visceral design",
                     "Making products <b>look, feel and sound good</b>. The immediate, pre-conscious reaction."),
                    ("Behavioural design",
                     "About <b>use</b> - this level equates with the traditional values of usability."),
                    ("Reflective design",
                     "About the <b>meaning and personal value</b> of a product - what owning and using it says."),
                ]),
                ("table", (["Emotional state", "How thinking changes", "Consequence for the interface"], [
                    ["Frightened or angry", "Focus narrows; muscles tense and the body sweats.",
                     "The user is <b>less tolerant</b> - minor flaws become blocking problems."],
                    ["Happy", "Focus widens; the body relaxes.",
                     "The user is <b>more likely to overlook minor problems</b> and to be more creative."],
                ])),
                ("note", ("THE SWATCH WATCH WORKED EXAMPLE",
                          "Brilliant colours and wild design attract attention at the <b>visceral</b> level. "
                          "Affordances of use operate at the <b>behavioural</b> level. Cultural images and graphical "
                          "elements are designed at the <b>reflective</b> level. One object, three levels - this is "
                          "the exact analysis the exam expects you to reproduce for a different product.")),
                ("hook", ("MEMORY HOOK",
                          "<b>V-B-R = Look, Use, Mean.</b> Visceral is what you see in the first second, behavioural "
                          "is what happens in the first minute, reflective is what you still think a year later.")),
            ],
        },
        {
            "id": "expressive",
            "kicker": "03 - EXPRESSIVE INTERFACES",
            "title": "Feedback that carries a feeling",
            "lead": ("Expressive interfaces provide reassuring feedback that can be both informative and fun - but "
                     "which can also be intrusive, causing people to get annoyed and even angry."),
            "blocks": [
                ("list", [
                    "Colour, icons, sounds, graphical elements and animations make the <b>look and feel</b> of an "
                    "interface appealing, and convey an emotional state.",
                    "That in turn affects <b>usability</b>: people will put up with a slow download rate if the end "
                    "result is appealing and aesthetic.",
                    "Users invent their own expressiveness to compensate for text's lack of it - emoticons "
                    "(happy, sad, sick, mad, very angry), plus shorthand such as LOL and <i>I 12 CU 2NITE</i>.",
                ]),
                ("table", (["Era", "Approach", "Example"], [
                    ["1980s", "Emotional, anthropomorphic icons.", "The smiling Apple face on reboot; a sad face on a crash."],
                    ["Now", "More impersonal but aesthetically pleasing.", "The spinning beachball indicating the user must wait."],
                ])),
                ("p", "The thermostat comparison makes the same point in hardware: the <b>Nest</b> is minimalist and "
                      "aesthetically pleasing - a round face, a simple dial, a large font and large numbers - where "
                      "earlier thermostat designs were utilitarian and dull. Identical function; different felt "
                      "experience."),
            ],
        },
        {
            "id": "frustrating",
            "kicker": "04 - FRUSTRATING INTERFACES",
            "title": "The seven causes, and how to write an error message",
            "lead": "Badly designed interfaces make people frustrated, annoyed or angry. The lecture lists the causes.",
            "blocks": [
                ("list", [
                    "An application does not work properly or crashes.",
                    "A system does not do what the user wants it to do.",
                    "A user's expectations are not met.",
                    "A system does not provide sufficient information for the user to know what to do.",
                    "Error messages pop up that are <b>vague, obtuse or condemning</b>.",
                    "The appearance of an interface is garish, noisy, gimmicky or patronizing.",
                    "The system requires too many steps, only for the user to discover a mistake made earlier and "
                    "have to start all over again.",
                ]),
                ("p", "<b>Gimmicks</b> are amusing to the designer and not to the user - clicking a link only to find "
                      "the page is still &quot;under construction&quot;. And the slides' own joke about error "
                      "messages is the sharpest illustration: instead of <i>&quot;The application Word Wonder has "
                      "unexpectedly quit due to a type 2 error&quot;</i>, why not <i>&quot;the application has "
                      "expectedly quit due to poor coding in the operating system&quot;</i>?"),
                ("table", (["Shneiderman's error-message guidelines", "What it means in practice"], [
                    ["Avoid terms like FATAL, INVALID, BAD", "Do not condemn the user for the system's failure."],
                    ["Reconsider audio warnings", "A klaxon adds stress without adding information."],
                    ["Avoid UPPERCASE and long code numbers", "Shouting and hex codes are not diagnosis."],
                    ["Messages should be precise rather than vague", "Say exactly what went wrong and where."],
                    ["Provide context-sensitive help", "Offer the fix at the point of failure."],
                ])),
                ("note", ("SHOULD COMPUTERS SAY SORRY?",
                          "Reeves and Nass (1996) argue computers should apologise and emulate human etiquette - "
                          "&quot;I'm really sorry I crashed. I'll try not to do it again.&quot; The slides raise the "
                          "counter-questions rather than settling them: would users be as forgiving of a computer as "
                          "of a person, and how sincere would they judge it to be? A friendly image in place of the "
                          "impersonal 404 is the mild version of the same idea.")),
                ("warn", ("THE ALEXA ETIQUETTE DILEMMA",
                          "Children talk to Alexa as a friend and learn that please and thank you are unnecessary. "
                          "Would that transfer to real life - &quot;Aunty, get me my drink&quot;? The slides note "
                          "that parents should still teach manners, that Alexa can be configured to be polite, and "
                          "ask how much parental control voice assistants should be given, and whether children "
                          "would find it creepy to be nagged by their friend.")),
            ],
        },
        {
            "id": "affective",
            "kicker": "05 - AFFECTIVE COMPUTING & EMOTIONAL AI",
            "title": "Machines that read feelings",
            "lead": ("Affective computing (Picard, 1998) is concerned with how to use computers to <b>recognise and "
                     "express emotions as humans do</b>. Emotional AI aims to <b>automate the measurement</b> of "
                     "feelings and behaviour, inferring them from facial expressions and voice."),
            "blocks": [
                ("list", [
                    "Involves designing ways for people to communicate their emotional state.",
                    "Uses sensing technologies to measure GSR, facial expressions, gestures and body movement.",
                    "Explores how affect influences personal health.",
                    "Aims to predict a user's emotions and aspects of their behaviour - for example what someone is "
                    "most likely to buy online when feeling sad, bored or happy.",
                ]),
                ("table", (["Technique", "What it measures"], [
                    ["Cameras", "Facial expressions."],
                    ["Biosensors on fingers or palms", "Galvanic skin response (GSR)."],
                    ["Speech analysis", "Affective expression through intonation, pitch and loudness."],
                    ["Accelerometers and motion capture", "Body movement and gestures."],
                ])),
                ("cards", [
                    ("The six core expressions",
                     "<b>Sadness, disgust, fear, anger, contempt, joy.</b> These are the six typically measured."),
                    ("The facial cues AI detects",
                     "Presence or absence of smiling, eye widening, brow raising, brow furrowing, raising a cheek, "
                     "mouth opening, upper-lip raising and wrinkling of the nose - the basis of facial coding "
                     "software such as Affdex."),
                    ("How the data gets used",
                     "Screw up your face at an ad &rarr; disgust. Start smiling &rarr; happy. The website adapts its "
                     "ad, movie storyline or content to match. In a car, a system might detect an angry driver and "
                     "suggest a deep breath. Eye-tracking, finger pulse, speech, and the words and phrases used when "
                     "tweeting or posting are analysed too."),
                ]),
                ("warn", ("INDIRECT EMOTION DETECTION - THE ETHICS QUESTION",
                          "The same techniques are used to <b>infer or predict behaviour</b>: a person's suitability "
                          "for a job, or how they will vote at an election. The slides ask directly whether it is "
                          "ethical for technology to read your emotions from your face or your tweets. An exam "
                          "answer should name the inference leap - from expression, to emotion, to a consequential "
                          "decision - as the point where the ethical problem bites.")),
                ("hook", ("MEMORY HOOK",
                          "Six core expressions: <b>S-D-F-A-C-J</b> - <i>&quot;Sad Dogs Frighten Angry Cats "
                          "Joyfully&quot;</i>. Note that <b>surprise is not on this list</b>; contempt is. "
                          "That swap is a classic distractor.")),
            ],
        },
        {
            "id": "persuasive",
            "kicker": "06 - PERSUASIVE TECHNOLOGY",
            "title": "Designing to change attitudes and behaviour",
            "lead": ("Persuasive technologies are interactive computing systems <b>deliberately designed to change "
                     "people's attitudes and behaviours</b> (Fogg, 2003)."),
            "blocks": [
                ("p", "A diversity of techniques is used: pop-up ads, warning messages, reminders, prompts, "
                      "personalised messages, recommendations, and Amazon 1-click. Collectively these are referred "
                      "to as <b>nudging</b>."),
                ("cards", [
                    ("Virtual pets",
                     "Emotional attachment does the persuading. A happy Pokemon makes a child feel good, a sulking "
                     "one makes them feel bad, and the child changes behaviour to keep it happy. The open question: "
                     "can technologies that monitor, nag or behave like a human keep people interested in looking "
                     "after it - and in doing so, fitter themselves?"),
                    ("Tracking devices",
                     "Mobile apps that help people monitor and change behaviour - fitness, sleeping, weight. "
                     "Comparison with online leaderboards and charts shows performance relative to peers and "
                     "friends. Some apps encourage reflection, which in turn increases wellbeing and happiness."),
                    ("Sustainable HCI",
                     "Designing interventions to reduce energy consumption. The most effective technique is "
                     "<b>feedback on consumption</b>; simple infographics and emoticons are often most powerful; "
                     "peer pressure and social norms are also powerful methods."),
                ]),
                ("note", ("THE TIDY STREET PROJECT (Bird and Rogers, 2010)",
                          "A large-scale visualisation of a whole street's electricity usage, stencilled in chalk on "
                          "the road surface. It gave real-time feedback that everyone could see change each day, and "
                          "<b>reduced electricity consumption by 15%</b>. Remember the number - it is the kind of "
                          "detail that turns a vague answer into a graded one.")),
                ("warn", ("THE DARK SIDE: PHISHING",
                          "The same persuasive machinery deceives. Phishing uses the web to trick people into "
                          "parting with personal details - PayPal, eBay and lottery-win letters - letting fraudsters "
                          "access bank accounts and draw money out. Many vulnerable people fall for it. The art of "
                          "deception is centuries old, but the internet allows ever more ingenious versions. "
                          "Persuasion and deception share a mechanism; only the intent differs.")),
            ],
        },
        {
            "id": "anthropomorphism",
            "kicker": "07 - ANTHROPOMORPHISM",
            "title": "Giving human qualities to things that have none",
            "lead": ("Anthropomorphism is attributing human-like qualities to inanimate objects such as cars and "
                     "computers. It is a well-known phenomenon in advertising - dancing butter, drinks and breakfast "
                     "cereals - and is much exploited in HCI."),
            "blocks": [
                ("list", [
                    "Used to make the user experience more <b>enjoyable and motivating</b>, to make people feel at "
                    "ease, and to reduce anxiety.",
                    "Furnishing technologies with personalities can make them enjoyable to interact with.",
                ]),
                ("table", (["Situation", "Anthropomorphic version", "Neutral version"], [
                    ["Welcome message",
                     "&quot;Hello Chris! Nice to see you again. Welcome back. Now what were we doing last time? "
                     "Oh yes, exercise 5. Let's start again.&quot;",
                     "&quot;User 24, commence exercise 5.&quot;"],
                    ["Feedback on an error",
                     "&quot;Now Chris, that's not right. You can do better than that. Try again.&quot;",
                     "&quot;Incorrect. Try again.&quot;"],
                ])),
                ("p", "The lecture asks whether your preference <b>differs by message type</b> - and it usually does. "
                      "A warm greeting is welcome; a warm rebuke can read as patronising, which is one of the "
                      "undesirable UX qualities from Lecture 1."),
                ("note", ("EVIDENCE FOR ANTHROPOMORPHISM",
                          "Reeves and Nass (1996) found that computers which <b>flatter and praise</b> users in "
                          "educational software have a positive impact - &quot;Your question makes an important and "
                          "useful distinction. Great job!&quot; Students were <b>more willing to continue</b> with "
                          "exercises given this kind of feedback.")),
                ("warn", ("THE ROBOT COMPANION QUESTION",
                          "Increasingly robots are used as companions in the home - remote, domestic, pet and "
                          "sociable. The slides ask whether it is acceptable for senior people to develop an "
                          "emotional attachment to a robot such as Zora. Answer it as a trade-off: measurable gains "
                          "in wellbeing and reduced loneliness, set against deception, dependency and the "
                          "substitution of human contact.")),
            ],
        },
    ],
    "mistakes": [
        ("Mixing up the three levels of the Ortony model.",
         "Visceral = look, feel and sound good. Behavioural = use, equating with traditional usability. "
         "Reflective = meaning and personal value. The Swatch analysis maps all three onto one object."),
        ("&quot;Being happy makes users notice more problems.&quot;",
         "The opposite. When happy, people are less focused, the body relaxes, and they are <b>more likely to "
         "overlook minor problems</b> and be more creative. When frightened or angry they focus narrowly, tense up, "
         "and become less tolerant."),
        ("Treating affective computing and emotional AI as identical.",
         "Affective computing (Picard, 1998) is about computers recognising <b>and expressing</b> emotions as humans "
         "do. Emotional AI specifically aims to <b>automate the measurement</b> of feelings and behaviour and infer "
         "them from expressions and voice."),
        ("Listing surprise among the six core expressions.",
         "The six measured are sadness, disgust, fear, anger, <b>contempt</b> and joy. Surprise is not in the "
         "lecture's list."),
        ("&quot;Persuasive technology is a synonym for advertising.&quot;",
         "It is any interactive system deliberately designed to change attitudes and behaviour - reminders, prompts, "
         "recommendations, fitness trackers, energy feedback and one-click purchasing all qualify. Nudging is the "
         "common term."),
        ("Claiming emotion causes behaviour in a simple line.",
         "Baumeister et al. (2007) argue the relationship is more complex than a single cause-and-effect model. "
         "State it as a two-way, complex relationship."),
    ],
    "cheat": (["Concept", "Shortest correct answer"], [
        ["Emotional interaction", "How we feel and react when interacting with technologies."],
        ["Automatic vs conscious emotion", "Rapid and quickly dissipating (anger) vs slow-developing and long-lasting (jealousy)."],
        ["Visceral design", "Making products look, feel and sound good."],
        ["Behavioural design", "About use; equates with traditional usability."],
        ["Reflective design", "About meaning and personal value."],
        ["Expressive interface", "Uses colour, icons, sound, graphics and animation to convey an emotional state and give reassuring feedback."],
        ["Frustration causes", "Crashes, unmet expectations, insufficient information, vague or condemning errors, garish appearance, too many steps."],
        ["Affective computing", "Using computers to recognise and express emotions as humans do (Picard, 1998)."],
        ["Emotional AI", "Automating the measurement of feelings and behaviour, inferring them from face and voice."],
        ["Six core expressions", "Sadness, disgust, fear, anger, contempt, joy."],
        ["Persuasive technology", "Interactive systems deliberately designed to change attitudes and behaviours (Fogg, 2003); nudging."],
        ["Tidy Street", "Chalk street-level visualisation of electricity use; cut consumption by 15% (Bird and Rogers, 2010)."],
        ["Anthropomorphism", "Attributing human-like qualities to inanimate objects."],
    ]),
    "quiz": [
        {"q": "A phone is chosen because its brushed-metal body feels expensive in the hand at first touch. Which level of Norman's model is this?",
         "options": ["Visceral", "Behavioural", "Reflective", "Cognitive"], "correct": 0,
         "why": "Visceral design is about making products look, feel and sound good - the immediate sensory "
                "reaction. Behavioural would be how easily it is operated, reflective would be what owning that "
                "brand means to the person, and cognitive is not a level in this model."},
        {"q": "According to the Ortony/Norman claims, how does being frightened or angry change a user's tolerance?",
         "options": ["Focus narrows and the user becomes less tolerant of minor problems",
                     "Focus widens and the user overlooks minor problems",
                     "Tolerance is unaffected; only speed changes",
                     "The user becomes more creative"], "correct": 0,
         "why": "Fear and anger narrow focus, tense the muscles and make the user less tolerant. Widened focus, "
                "overlooking minor problems and increased creativity are all the effects of being <i>happy</i>."},
        {"q": "Which error message best follows Shneiderman's guidelines?",
         "options": ["&quot;The date you entered is 31 February. Please choose a day between 1 and 28 for this month.&quot;",
                     "&quot;FATAL: INVALID INPUT (ERR 0x8007005)&quot;",
                     "&quot;Something went wrong. Try again later.&quot;",
                     "&quot;BAD DATE. RE-ENTER.&quot;"], "correct": 0,
         "why": "It is precise about what went wrong and constructively suggests the fix. The second uses FATAL, "
                "INVALID, uppercase and a long code number; the third is vague; the fourth uses BAD and uppercase. "
                "All three violate the guidelines explicitly listed."},
        {"q": "A street-level chalk visualisation of household electricity use cut consumption by 15%. What kind of intervention is this?",
         "options": ["Persuasive technology using feedback and social norms",
                     "Affective computing using biosensors",
                     "Anthropomorphism",
                     "An expressive interface using emoticons only"], "correct": 0,
         "why": "The Tidy Street project is the lecture's sustainable-HCI example of persuasive technology: real-time "
                "feedback on consumption plus visible peer comparison. No emotion sensing is involved, nothing is "
                "given human qualities, and the display is public rather than an interface using emoticons."},
        {"q": "Emotional AI classifies a user as feeling contempt from a wrinkled nose and a raised upper lip, and the system uses this to score their job application. What is the core ethical objection raised in the lecture?",
         "options": ["Inferring consequential decisions from expression-based emotion prediction",
                     "The measurements are not technically possible",
                     "GSR sensors are uncomfortable to wear",
                     "The six core expressions are too many to distinguish"], "correct": 0,
         "why": "The slides raise indirect emotion detection - using inferred emotion to predict suitability for a "
                "job or voting behaviour - and ask directly whether that is ethical. The techniques are technically "
                "feasible, sensor comfort is not the issue raised here, and six expressions are routinely "
                "distinguished by facial coding software."},
        {"q": "Reeves and Nass (1996) found that educational software which praised students had which effect?",
         "options": ["Students were more willing to continue with the exercises",
                     "Students found the praise insincere and disengaged",
                     "Students performed worse but enjoyed it more",
                     "There was no measurable effect"], "correct": 0,
         "why": "The finding was a positive impact: flattery and praise made students more willing to continue. The "
                "lecture raises insincerity as an open question about computers apologising, but the reported "
                "finding for praise is positive."},
    ],
    "lab": [
        ("Analyse a smartwatch using Norman's three levels, then say which level a fitness feature must hit to change behaviour.",
         "<b>Visceral:</b> the case material, the screen's brightness and the haptic tap all produce the first "
         "reaction. <b>Behavioural:</b> whether a workout can be started in one press, whether the display is "
         "readable mid-run - traditional usability. <b>Reflective:</b> what wearing it signals about being the kind "
         "of person who trains, and the personal value of a year's records. Behaviour change lives mainly at the "
         "<b>reflective</b> level, supported by persuasive mechanisms - streaks, leaderboards and social comparison "
         "work because they engage meaning and peer norms, not because the tap feels nice."),
        ("A checkout page shows &quot;INVALID INPUT - ERROR 500&quot; when a card is declined. Rewrite it and justify each change.",
         "&quot;Your bank declined this card. No payment was taken. Check the card number and expiry date, or try a "
         "different card.&quot; Changes: drop INVALID and the uppercase, which condemn the user and shout; drop the "
         "code number, which is not a diagnosis; state precisely what happened and reassure that no money moved, "
         "because unmet expectations and insufficient information are two of the listed causes of frustration; and "
         "offer the fix at the point of failure, which is context-sensitive help."),
        ("A company wants a chatbot that apologises warmly whenever the system fails. Argue both sides using this lecture.",
         "<b>For:</b> Reeves and Nass (1996) argue computers should emulate human etiquette, and their praise study "
         "shows affective feedback measurably increases willingness to continue; anthropomorphism reduces anxiety "
         "and makes the experience more enjoyable. <b>Against:</b> the slides pose two unresolved questions - "
         "whether users would be as forgiving of a computer as of a person, and how sincere they would judge it to "
         "be. An apology that is not backed by a fix is a gimmick, and gimmicks are amusing to the designer and not "
         "the user; over-familiar wording risks reading as patronizing or cutesy, both undesirable UX qualities. "
         "The defensible position: apologise briefly, state precisely what failed, and spend the interaction budget "
         "on the recovery path rather than the sentiment."),
    ],
    "branches": [
        ("Emotions and the user experience",
         "Emotional interaction concerns how we feel and react when interacting with technologies, and how that translates into aspects of the user experience.",
         ["HCI has moved from designing efficient and effective systems to designing systems that make people respond in certain ways.",
          "It examines what makes people happy, sad, annoyed, anxious, frustrated or motivated.",
          "It asks why people become emotionally attached to products such as virtual pets.",
          "It asks whether social robots can reduce loneliness and improve wellbeing.",
          "Emotional intelligence covers reading facial expressions, body language, gestures and tone of voice.",
          "Baumeister et al. (2007) argue the emotion-behaviour relationship is more complex than a single cause-and-effect model.",
          "Automatic emotions are rapid and dissipate quickly; conscious emotions develop slowly and last."],
         [("Fit of anger vs jealousy", "Anger is the automatic, short-lived case; jealousy is the conscious, long-lasting case involving reflection."),
          ("Mood tracking problem", "Moods change continuously, so an interface that adapts to feeling must somehow know when to act - an open design question in the slides.")]),
        ("Ortony's model of emotional design",
         "Three levels of design - visceral, behavioural and reflective - and the claim that emotional state changes how we think.",
         ["Visceral design is about making products look, feel and sound good.",
          "Behavioural design is about use and equates with traditional values of usability.",
          "Reflective design is about the meaning and personal value of a product.",
          "When frightened or angry we focus narrowly, the body tenses and sweats, and we are less tolerant.",
          "When happy we are less focused, the body relaxes, and we overlook minor problems and are more creative."],
         [("The Swatch watch", "Cultural images and graphical elements sit at the reflective level, affordances of use at the behavioural level, and brilliant colours and wild design at the visceral level."),
          ("Design consequence", "A stressful task interface must be more forgiving, because anxious users have narrow focus and low tolerance for minor flaws.")]),
        ("Expressive interfaces",
         "Interfaces that provide reassuring feedback which can be informative and fun, but can also be intrusive and annoying.",
         ["Colour, icons, sounds, graphical elements and animations make the look and feel appealing and convey an emotional state.",
          "Appeal can affect usability, because people tolerate flaws such as slow downloads when the result is aesthetic.",
          "Users invented emoticons to compensate for the lack of expressiveness in text communication.",
          "Icons and shorthand in texting and instant messaging carry emotional connotations."],
         [("Apple face to beachball", "1980s interfaces used a smiling apple face for reboot and a sad face for a crash; modern ones use the impersonal but aesthetically pleasing beachball."),
          ("Nest thermostat", "A minimalist round face, simple dial and large numbers replace the utilitarian, dull designs of earlier thermostats.")]),
        ("Frustrating interfaces",
         "Interfaces that make people frustrated, annoyed or angry, with a defined list of causes and guidelines for error messages.",
         ["Causes include applications that crash, systems that do not do what the user wants, and unmet expectations.",
          "Insufficient information means the user cannot know what to do next.",
          "Error messages that are vague, obtuse or condemning are a major cause.",
          "Garish, noisy, gimmicky or patronizing appearance frustrates users.",
          "Too many steps followed by discovering an earlier mistake forces a restart.",
          "Shneiderman: avoid FATAL, INVALID and BAD; reconsider audio warnings; avoid uppercase and long code numbers; be precise rather than vague; provide context-sensitive help.",
          "Reeves and Nass (1996) argue computers should apologise and emulate human etiquette."],
         [("The under-construction link", "A gimmick amusing to the designer and useless to the user, who came for content."),
          ("Type 2 error joke", "The slides contrast the real message about a type 2 error with an honest one blaming poor coding in the operating system."),
          ("Alexa and manners", "Children learn that please and thank you are unnecessary; the slides ask whether this transfers to real life and how much parental control assistants should have.")]),
        ("Affective computing and emotional AI",
         "Using computers to recognise and express emotions as humans do (Picard, 1998), and automating the measurement of feelings using AI.",
         ["Involves designing ways for people to communicate their emotional state.",
          "Uses sensing technologies to measure GSR, facial expressions, gestures and body movement.",
          "Explores how affect influences personal health.",
          "Aims to predict emotions and behaviour, such as what someone will buy when sad, bored or happy.",
          "Techniques: cameras for facial expressions, biosensors for GSR, speech intonation, pitch and loudness, accelerometers and motion capture.",
          "Six core expressions measured: sadness, disgust, fear, anger, contempt and joy.",
          "Facial cues detected include smiling, eye widening, brow raising, brow furrowing, cheek raising, mouth opening, upper-lip raising and nose wrinkling.",
          "Indirect detection is used to infer suitability for a job or voting behaviour, which raises ethical concerns."],
         [("Adaptive content", "A website that detects disgust at an ad and changes the ad, storyline or content to match the viewer's emotional state."),
          ("Angry driver", "An in-car system detects anger and suggests the driver takes a deep breath."),
          ("Affdex", "Facial coding software that classifies expressions from the presence or absence of specific facial actions.")]),
        ("Persuasive technologies and behavioural change",
         "Interactive computing systems deliberately designed to change people's attitudes and behaviours (Fogg, 2003), commonly called nudging.",
         ["Techniques include pop-up ads, warning messages, reminders, prompts, personalised messages, recommendations and one-click purchasing.",
          "Virtual pets change behaviour through emotional attachment.",
          "Tracking apps help people monitor fitness, sleep and weight, and compare against leaderboards and peers.",
          "Apps that encourage reflection increase wellbeing and happiness.",
          "Sustainable HCI designs interventions to reduce energy consumption.",
          "Feedback on consumption is the most effective technique, and simple infographics and emoticons are often the most powerful form.",
          "Peer pressure and social norms are powerful methods.",
          "Phishing applies the same persuasive machinery deceptively, using fake PayPal, eBay and lottery messages."],
         [("Tidy Street", "Bird and Rogers (2010) chalked a whole street's electricity usage on the road surface, giving daily visible feedback and cutting consumption by 15%."),
          ("Pokemon", "A happy virtual pet makes a child feel good and a sulking one makes them feel bad, driving the child's behaviour.")]),
        ("Anthropomorphism",
         "Attributing human-like qualities to inanimate objects such as cars and computers.",
         ["A well-known phenomenon in advertising, using dancing butter, drinks and breakfast cereals.",
          "Exploited in HCI to make the user experience more enjoyable and motivating, to put people at ease and to reduce anxiety.",
          "Furnishing technologies with personalities can make them enjoyable to interact with.",
          "Preference for anthropomorphic wording can depend on the type of message, since a warm rebuke can read as patronizing.",
          "Robots are increasingly used as companions in the home: remote, domestic, pet and sociable types."],
         [("Welcome message contrast", "\"Hello Chris! Nice to see you again... let's start again\" versus \"User 24, commence exercise 5.\""),
          ("Praise study", "Reeves and Nass (1996) found computers that flatter and praise users in educational software had a positive impact, and students were more willing to continue."),
          ("Robot Zora", "The slides ask whether it is acceptable for senior people to form an emotional attachment to a companion robot.")]),
    ],
    "exam_mcq": [
        {"q": "Which statement correctly describes BEHAVIOURAL design in Norman's three-level model?",
         "options": ["It is about use, and equates with the traditional values of usability",
                     "It is about making products look, feel and sound good",
                     "It is about the meaning and personal value of a product",
                     "It is about the automatic emotions that dissipate quickly"],
         "correct": 0,
         "why": "Behavioural design concerns use and maps onto traditional usability. Looking, feeling and sounding "
                "good is visceral; meaning and personal value is reflective; automatic emotion is a category of "
                "emotion, not a design level."},
        {"q": "Which is NOT listed in the lecture as a cause of frustrating interfaces?",
         "options": ["An interface that offers keyboard shortcuts for expert users",
                     "Error messages that are vague, obtuse or condemning",
                     "A system requiring too many steps before revealing an earlier mistake",
                     "An appearance that is garish, noisy, gimmicky or patronizing"],
         "correct": 0,
         "why": "Accelerators for expert users are a usability benefit, not a frustration cause. The other three "
                "appear verbatim in the lecture's list."},
        {"q": "Picard (1998) defines affective computing as concerned with what?",
         "options": ["How to use computers to recognise and express emotions as humans do",
                     "How to change users' attitudes and behaviours through nudging",
                     "How to attribute human qualities to inanimate objects",
                     "How to reduce energy consumption through visible feedback"],
         "correct": 0,
         "why": "Recognising and expressing emotions as humans do is the definition given. Nudging is persuasive "
                "technology (Fogg), attributing human qualities is anthropomorphism, and energy feedback is "
                "sustainable HCI."},
        {"q": "Which set matches the six core expressions typically measured by emotional AI?",
         "options": ["Sadness, disgust, fear, anger, contempt, joy",
                     "Sadness, surprise, fear, anger, trust, joy",
                     "Happiness, boredom, fear, anger, contempt, disgust",
                     "Joy, sadness, anticipation, trust, fear, surprise"],
         "correct": 0,
         "why": "The lecture lists sadness, disgust, fear, anger, contempt and joy. Surprise, trust, anticipation and "
                "boredom are distractors that do not appear in that list."},
        {"q": "The Tidy Street project reduced electricity consumption by approximately how much, and by what mechanism?",
         "options": ["15%, through real-time public feedback that everyone on the street could see change daily",
                     "50%, through automatic shutdown of high-consumption appliances",
                     "15%, through personalised emails to each household",
                     "5%, through a smartphone leaderboard"],
         "correct": 0,
         "why": "Bird and Rogers (2010) stencilled the street's usage in chalk on the road, giving visible real-time "
                "feedback, and consumption fell by 15%. No appliances were controlled, the display was public rather "
                "than emailed, and the figure was 15% rather than 5%."},
        {"q": "Which of these is an example of ANTHROPOMORPHISM in an interface?",
         "options": ["A tutoring system that says &quot;Now Chris, that's not right. You can do better than that.&quot;",
                     "A dialog that greys out unavailable options",
                     "A progress bar showing 60% complete",
                     "A biosensor measuring galvanic skin response"],
         "correct": 0,
         "why": "Addressing the user by name in a conversational, encouraging tone attributes human qualities to the "
                "system. Greying out options is a constraint, a progress bar is feedback, and a GSR sensor is an "
                "affective-computing measurement technique."},
    ],
    "exam_short": [
        {"q": "Explain the three levels of Norman's emotional design model and apply all three to a single product.",
         "keywords": ["visceral", "behavioural", "reflective", "usab"],
         "answer": "Visceral design is about making a product look, feel and sound good - the immediate sensory "
                   "reaction. Behavioural design is about use and equates with traditional usability. Reflective "
                   "design is about the meaning and personal value of the product. Applied to the Swatch watch: "
                   "brilliant colours and wild design attract attention at the visceral level, affordances of use "
                   "operate at the behavioural level, and cultural images and graphical elements are designed at the "
                   "reflective level."},
        {"q": "State Shneiderman's guidelines for error messages and explain why each matters.",
         "keywords": ["fatal", "precise", "uppercase", "context"],
         "answer": "Avoid terms like FATAL, INVALID and BAD, because they condemn the user for a system failure. "
                   "Reconsider audio warnings, because a klaxon adds stress without adding information. Avoid "
                   "UPPERCASE and long code numbers, because shouting and hex codes are not a diagnosis. Make "
                   "messages precise rather than vague, so the user knows exactly what went wrong and where. "
                   "Provide context-sensitive help, so the fix is offered at the point of failure rather than in a "
                   "manual."},
        {"q": "What is persuasive technology, and what makes feedback effective in sustainable HCI?",
         "keywords": ["persuasiv", "behaviour", "feedback", "norm"],
         "answer": "Persuasive technology means interactive computing systems deliberately designed to change "
                   "people's attitudes and behaviours (Fogg, 2003), using pop-ups, warnings, reminders, prompts, "
                   "personalised messages, recommendations and one-click purchasing - collectively called nudging. "
                   "In sustainable HCI the most effective technique is giving householders feedback on their own "
                   "consumption. Simple infographics and emoticons are often the most powerful form because they "
                   "encourage reflection, and peer pressure and social norms amplify the effect - as in the Tidy "
                   "Street project, where a public chalk visualisation of the street's usage cut consumption by 15%."},
        {"q": "Describe affective computing and emotional AI, naming the sensing techniques used.",
         "keywords": ["affective", "emotion", "facial", "GSR"],
         "answer": "Affective computing (Picard, 1998) is concerned with how to use computers to recognise and "
                   "express emotions as humans do, and involves designing ways for people to communicate their "
                   "emotional state. Emotional AI aims to automate the measurement of feelings and behaviour and "
                   "infer them from facial expressions and voice, in order to predict a user's emotions and "
                   "behaviour. Techniques: cameras for measuring facial expressions, biosensors on fingers or palms "
                   "for galvanic skin response, analysis of intonation, pitch and loudness in speech, and "
                   "accelerometers or motion-capture systems for body movement and gestures. Six core expressions "
                   "are typically measured: sadness, disgust, fear, anger, contempt and joy."},
        {"q": "Why can an appealing interface make users tolerate poor performance? Answer using this lecture's own reasoning.",
         "keywords": ["expressive", "aesthetic", "tolerat", "emotion"],
         "answer": "Expressive interfaces use colour, icons, sounds, graphical elements and animations to make the "
                   "look and feel appealing, and in doing so convey an emotional state. That emotional state "
                   "feeds back into usability: the lecture states that people are prepared to put up with certain "
                   "aspects of an interface, such as a slow download rate, if the end result is appealing and "
                   "aesthetic. The Ortony model explains the mechanism - a happy user is less focused, more "
                   "relaxed, and more likely to overlook minor problems, whereas an angry user focuses narrowly and "
                   "is less tolerant of the very same flaw."},
        {"q": "Give the arguments for and against anthropomorphic interfaces, citing the evidence in the lecture.",
         "keywords": ["anthropomorph", "Reeves", "patroniz", "etiquette"],
         "answer": "For: anthropomorphism makes the user experience more enjoyable and motivating, puts people at "
                   "ease and reduces anxiety, and giving technologies personalities makes them enjoyable to interact "
                   "with. Reeves and Nass (1996) found that computers which flatter and praise users in educational "
                   "software had a positive impact, and students were more willing to continue with the exercises. "
                   "Against: preference depends on message type - a warm greeting is welcome but a warm rebuke such "
                   "as &quot;Now Chris, that's not right&quot; can read as patronizing, one of the undesirable UX "
                   "qualities. The lecture also leaves open whether users would be as forgiving of a computer that "
                   "apologises as they are of a person, and how sincere they would judge it, and raises concerns "
                   "about children learning poor etiquette from voice assistants and about elderly users forming "
                   "emotional attachments to companion robots."},
    ],
})


LECTURES.append({
    "num": 4,
    "slug": "interaction-and-interfaces",
    "title": "Interaction and Interfaces",
    "short": "Interaction & Interfaces",
    "lecture_label": "Lecture 4",
    "theme": "grid",
    "accent": "#2fb8ff",
    "accent2": "#c77dff",
    "tagline": "The problem space, conceptual models, interface metaphors, five interaction types and twenty interface types.",
    "hero_title": "Straighten out your thinking<br><em>before you lay out your widgets.</em>",
    "hero_sub": ("This is the longest deck of the course. It moves from <b>assumptions and claims</b>, through the "
                 "<b>conceptual model</b> and <b>interface metaphors</b>, to the five <b>interaction types</b> and "
                 "twenty <b>interface types</b> - and the recurring question of which one to choose."),
    "badges": ["Problem space", "Assumptions vs claims", "Conceptual models",
               "Interface metaphors", "5 interaction types", "20 interface types", "NUIs"],
    "outcomes": [
        "Explain what is meant by the problem space.",
        "Explain how to conceptualize interaction.",
        "Discuss the use of interface metaphors as part of a conceptual model.",
        "Explain the five interaction types and the twenty interface types.",
        "Discuss advanced interfaces and natural user interfaces.",
    ],
    "sections": [
        {
            "id": "problem-space",
            "kicker": "01 - THE PROBLEM SPACE",
            "title": "Assumptions, claims, and the question nobody asked",
            "lead": ("Before designing anything you must understand the problem space: what you want to create, what "
                     "your assumptions are, and whether it will achieve what you hope."),
            "blocks": [
                ("table", (["Term", "Definition", "Example from the slides"], [
                    ["<b>Assumption</b>", "Taking something for granted when it needs further investigation.",
                     "&quot;People will want to watch TV while driving.&quot;"],
                    ["<b>Claim</b>", "Stating something to be true when it is still open to question.",
                     "&quot;A multimodal style of interaction for controlling GPS - one that involves speaking while "
                     "driving - is safe.&quot;"],
                ])),
                ("cards", [
                    ("The robot waiter case",
                     "<b>The proposed benefits:</b> the robot could take orders and entertain customers by "
                     "conversing with them, and make recommendations for restless children or fussy eaters. "
                     "<b>But those are just assumptions.</b> The real problem being addressed is: <i>&quot;It is "
                     "difficult to recruit good wait staff who provide the level of customer service to which we "
                     "have become accustomed.&quot;</i> Naming the real problem changes which solutions are even "
                     "candidates."),
                    ("The 3D TV case",
                     "There was <b>no existing problem to overcome</b> - it proposed a new way of experiencing TV. "
                     "The <b>assumption</b>: people would really enjoy the enhanced clarity and colour detail. "
                     "The <b>claim</b>: people would not mind paying a lot more for a 3D-enabled screen because of "
                     "the new experience. Both turned out to be false, which is why it is the standing example."),
                ]),
                ("steps", [
                    ("Are there problems with an existing product or user experience?", "If so, what exactly are they?"),
                    ("Why do you think there are problems?", "Name the cause, not the symptom."),
                    ("How might your design ideas overcome these?", "Connect each idea to a named problem."),
                    ("If designing for a new experience", "How do your ideas support, change or extend current ways of doing things?"),
                ]),
                ("note", ("BENEFITS OF CONCEPTUALIZING",
                          "<b>Orientation</b> - lets the team ask specific questions about how the conceptual model "
                          "will be understood. <b>Open-mindedness</b> - prevents the team becoming narrowly focused "
                          "early on. <b>Common ground</b> - lets the team establish a set of commonly agreed terms.")),
                ("hook", ("MEMORY HOOK",
                          "<b>Assumption = taken for granted. Claim = stated as true.</b> An assumption is something "
                          "you did not notice you believed; a claim is something you said out loud. Both need "
                          "investigation before they become requirements.")),
            ],
        },
        {
            "id": "conceptual-models",
            "kicker": "02 - CONCEPTUAL MODELS",
            "title": "A high-level description of how a system is organized and operates",
            "lead": ("A conceptual model enables designers to <b>straighten out their thinking before they start "
                     "laying out their widgets</b>. The best conceptual models appear obvious and simple, and the "
                     "operations they support are intuitive to use."),
            "blocks": [
                ("list", [
                    "<b>Metaphors and analogies</b> - so people understand what a product is for and how to use it "
                    "for an activity.",
                    "<b>Concepts</b> people are exposed to through the product - task-domain objects, their "
                    "attributes and operations.",
                    "<b>Relationships and mappings</b> between these concepts.",
                ]),
                ("steps", [
                    ("What will the users be doing?", "Identify the tasks being carried out."),
                    ("How will the system support these?", "Map system function to user task."),
                    ("What interface metaphor, if any, is appropriate?", "Or is none better than a forced one?"),
                    ("What interaction modes and styles?", "Always keeping in mind how the user will understand the underlying conceptual model."),
                ]),
                ("note", ("THE ONLINE SHOPPING ACTIVITY",
                          "The slides ask you to name the components of the conceptual model behind most shopping "
                          "sites: the <b>shopping cart</b>, <b>proceeding to check-out</b>, <b>1-click</b>, "
                          "<b>gift wrapping</b>, and the <b>cash till</b>. Notice that every one of them is borrowed "
                          "from a physical shop - the conceptual model <i>is</i> a metaphor here.")),
            ],
        },
        {
            "id": "metaphors",
            "kicker": "03 - INTERFACE METAPHORS",
            "title": "Familiar knowledge, unfamiliar functionality",
            "lead": ("An interface metaphor is designed to be similar to a physical entity but also has its own "
                     "properties - the desktop metaphor, web portals. It can be based on an activity, an object, or "
                     "a combination of both."),
            "blocks": [
                ("p", "Metaphors exploit users' familiar knowledge to help them understand <b>the unfamiliar</b>. "
                      "They conjure up the essence of an unfamiliar activity, letting users leverage that to "
                      "understand more aspects of unfamiliar functionality. A conceptual model instantiated at the "
                      "interface <em>is</em> a metaphor - the desktop is the standing example."),
                ("cards", [
                    ("The card metaphor",
                     "Very popular because it has a <b>familiar form factor</b>. Cards can easily be flicked "
                     "through, sorted and themed; they structure content into meaningful chunks, similarly to how "
                     "paragraphs chunk related sentences; and their material properties give the appearance of the "
                     "surface of paper."),
                    ("The calculator example",
                     "Two digital calculators: one designed <b>too literally</b> as a physical calculator, one "
                     "designed more appropriately for a computer screen. A metaphor copied slavishly imports the "
                     "old medium's limitations."),
                ]),
                ("table", (["Benefits", "Problems"], [
                    ["Makes learning new systems easier.", "Breaks conventional and cultural rules - e.g. a recycle bin placed on a desktop."],
                    ["Helps users understand the underlying conceptual model.", "Can constrain designers in how they conceptualize a problem space."],
                    ["Can be innovative and make computing accessible to a greater diversity of users.", "Can conflict with design principles."],
                    ["", "Forces users to understand the system <b>only</b> in terms of the metaphor."],
                    ["", "Designers can inadvertently transfer over the bad parts of an existing bad design."],
                    ["", "Limits designers' imagination in coming up with new conceptual models."],
                ])),
                ("warn", ("EXAM TRAP",
                          "The problems list is longer than the benefits list, and the exam usually asks for "
                          "problems. Remember the recycle bin on the desktop - a bin is not something you keep on "
                          "your desk - as the one-line proof that metaphors break real-world rules.")),
            ],
        },
        {
            "id": "interaction-types",
            "kicker": "04 - THE FIVE INTERACTION TYPES",
            "title": "Instructing, conversing, manipulating, exploring, responding",
            "lead": ("An interaction type describes <b>what the user is doing</b> when interacting with a system. "
                     "An interface type is the kind of interface used to support that mode."),
            "blocks": [
                ("cards", [
                    ("1. Instructing",
                     "Users tell the system what to do - tell the time, print a file, save a file - by issuing "
                     "commands, selecting options, speaking commands, gesturing or pressing buttons. A very common "
                     "model, underlying word processors, VCRs and vending machines. <b>Main benefit:</b> quick and "
                     "efficient interaction, good for repetitive actions performed on multiple objects."),
                    ("2. Conversing",
                     "Interacting as if having a conversation with another human. Ranges from simple voice-recognition "
                     "menu-driven systems to complex natural-language dialogs: timetables, search engines, "
                     "advice-giving systems, help systems, virtual agents, toys and pet robots. <b>Pro:</b> familiar "
                     "to novices, making them comfortable, at ease and less scared. <b>Con:</b> misunderstandings "
                     "arise when the system cannot parse what the user says - voice assistants misunderstanding "
                     "children is the slides' example."),
                    ("3. Manipulating",
                     "Dragging, selecting, opening, closing and zooming on virtual objects, exploiting users' "
                     "knowledge of how they move and manipulate in the physical world. Can involve physical "
                     "controllers (Wii), air gestures (Kinect), or tagged physical objects whose manipulation "
                     "triggers physical/digital events."),
                    ("4. Exploring",
                     "Moving through virtual or physical environments. Users can explore a virtual 3D environment; "
                     "physical environments embedded with sensors trigger digital or physical events when they "
                     "detect someone. Examples include cities, parks, buildings, rooms and datasets that users fly "
                     "over and zoom into."),
                    ("5. Responding",
                     "The <b>system takes the initiative</b> and alerts the user to something it &quot;thinks&quot; "
                     "is of interest, by detecting location or presence, or from what it has learned from repeated "
                     "behaviour. Examples: alerting the user to a nearby coffee bar where friends are meeting, or a "
                     "fitness tracker notifying a milestone. It is an automatic response with <b>no request made by "
                     "the user</b>."),
                ]),
                ("p", "<b>Direct Manipulation (DM)</b> is the sharpened form of manipulating. Shneiderman (1983) "
                      "coined the term, from his fascination with computer games. Its three properties:"),
                ("list", [
                    "Continuous representation of the objects and actions of interest.",
                    "Physical actions and button pressing instead of issuing commands with complex syntax.",
                    "Rapid, reversible actions with immediate feedback on the object of interest.",
                ]),
                ("table", (["Benefits of DM", "Disadvantages of DM"], [
                    ["Novices learn basic functionality quickly.", "Some people take the metaphor of direct manipulation too literally."],
                    ["Experienced users work rapidly across a wide range of tasks, even defining new functions.", "Not all tasks can be described by objects, and not all actions can be done directly."],
                    ["Intermittent users retain operational concepts over time.", "Some tasks are better achieved by <b>delegating</b> - spell checking is the example."],
                    ["Error messages are rarely needed.", "Can become screen-space &quot;gobblers&quot;."],
                    ["Users immediately see whether actions further their goals.", "Moving a mouse around the screen can be slower than pressing function keys."],
                    ["Users experience less anxiety, gain confidence and mastery, and feel in control.", ""],
                ])),
                ("note", ("WHICH CONCEPTUAL MODEL IS BEST?",
                          "<b>Direct manipulation</b> for &quot;doing&quot; tasks - designing, drawing, flying, "
                          "driving, sizing windows. <b>Issuing instructions</b> for repetitive tasks - spell-checking, "
                          "file management. <b>Conversation</b> for children, computer-phobic and disabled users and "
                          "specialised applications such as phone services. <b>Hybrid</b> models are often employed, "
                          "supporting several ways of doing the same action - but they take longer to learn.")),
                ("hook", ("MEMORY HOOK",
                          "<b>I-C-M-E-R</b>: <b>I</b>nstructing, <b>C</b>onversing, <b>M</b>anipulating, "
                          "<b>E</b>xploring, <b>R</b>esponding - <i>&quot;I Can Make Everything Respond&quot;</i>. "
                          "Only the last one starts with the system, which is the distinguishing feature the exam "
                          "tests.")),
            ],
        },
        {
            "id": "interfaces-classic",
            "kicker": "05 - INTERFACE TYPES 1-8",
            "title": "Command line to mobile",
            "lead": ("Twenty interface types are listed. The first eight are the classic and mainstream ones, and "
                     "carry the most detail on the slides."),
            "blocks": [
                ("cards", [
                    ("1. Command-based",
                     "Type abbreviations at a prompt (<code>ls</code>) and the system responds. Some commands are "
                     "hard-wired at the keyboard (delete, enter, undo), others assignable (F11 = print). "
                     "<b>Efficient, precise and fast</b>, but with a large overhead in learning the command set. "
                     "Key research questions concern <b>form, name types and structure</b>; <b>consistency</b> is "
                     "the most important design principle - always use the first letter of the command. Still "
                     "popular for web scripting, and used in Second Life for visually impaired users."),
                    ("2a. WIMP",
                     "The Xerox Star was the first WIMP, giving rise to GUIs. <b>W</b>indows - scrolled, stretched, "
                     "overlapped, opened, closed and moved with the mouse. <b>I</b>cons - representing applications, "
                     "objects, commands and tools, opened when clicked. <b>M</b>enus - lists of options scrolled "
                     "through and selected. <b>P</b>ointing device - a mouse controlling the cursor as the point of "
                     "entry to windows, menus and icons."),
                    ("2b. GUI",
                     "The same building blocks, but more varied: colour, 3D, sound, animation, many types of menus, "
                     "icons and windows, plus new graphical elements - toolbars, docks, rollovers."),
                    ("3. Multimedia",
                     "Combines graphics, text, video, sound and animation within a single interface with various "
                     "forms of interactivity. <b>Pros:</b> rapid access to multiple representations, better "
                     "presentation than any medium alone, easier learning, better understanding, more engagement, "
                     "more pleasure, and encouragement to explore. <b>Con:</b> a tendency to play video clips and "
                     "animations while skimming the accompanying text and diagrams. The design answer is hands-on "
                     "interactivities, simulations, quizzes, electronic notebooks and games that must be completed."),
                    ("4. Virtual reality",
                     "Computer-generated graphical simulations providing &quot;the illusion of participation in a "
                     "synthetic environment rather than external observation of such an environment&quot; "
                     "(Gigante, 1993). <b>Pros:</b> higher fidelity than multimedia; induces a <b>sense of "
                     "presence</b> - &quot;a state of consciousness, the psychological sense of being in the virtual "
                     "environment&quot; (Slater and Wilbur, 1999); provides first- and third-person viewpoints. "
                     "<b>Cons:</b> head-mounted displays are uncomfortable and can cause motion sickness and "
                     "disorientation. Used for flying simulators and for overcoming phobias such as spiders and "
                     "public speaking."),
                    ("5. Information visualization",
                     "Computer-generated interactive graphics of complex data that <b>amplify human cognition</b>, "
                     "letting users see patterns, trends and anomalies (Card et al., 1999). The aim is to enhance "
                     "discovery, decision-making and explanation. Techniques include 3D interactive maps that zoom, "
                     "presenting data via webs, trees, clusters, scatterplots and interconnected nodes."),
                    ("6. Web",
                     "Early sites were largely text with hyperlinks, and the concern was structuring information so "
                     "users could navigate quickly. Now there is more emphasis on making pages distinctive, striking "
                     "and pleasurable - the <b>vanilla versus multi-flavour</b> tension between ease of finding "
                     "something and an aesthetic, enjoyable experience. Veen's three design principles: "
                     "<b>(1) Where am I? (2) Where can I go? (3) What's here?</b>"),
                    ("7. Consumer electronics &amp; appliances",
                     "Everyday devices in the home, public places or cars - washing machines, remotes, photocopiers, "
                     "printers, navigation systems - and personal devices such as MP3 players, digital clocks and "
                     "cameras. Used for <b>short periods</b>, so they must be usable with minimal, if any, learning. "
                     "Design as <b>transient interfaces</b> with short interactions, keep them simple, and consider "
                     "the trade-off between soft and hard controls."),
                    ("8. Mobile",
                     "Handheld devices used while on the move, now pervasive: restaurants take orders, car rentals "
                     "check in returns, supermarkets check stock, streets host multi-user gaming, and education "
                     "supports life-long learning. <b>Challenges:</b> small screens, few keys, restricted controls. "
                     "Innovations include roller wheels, rocker dials, up/down lips, two- and four-way directional "
                     "keypads, softkeys and silk-screened buttons. Tricky for those with poor manual dexterity."),
                ]),
                ("warn", ("VEEN'S THREE QUESTIONS",
                          "<b>Where am I? Where can I go? What's here?</b> Three words each - this is the most "
                          "quotable item in the web section and the one most likely to appear verbatim.")),
            ],
        },
        {
            "id": "interfaces-modern",
            "kicker": "06 - INTERFACE TYPES 9-20",
            "title": "Speech to brain-computer",
            "lead": "The remaining twelve are the post-WIMP interfaces, each with its own research and design issues.",
            "blocks": [
                ("cards", [
                    ("9. Speech",
                     "A person talks with a system that has a spoken-language application - timetables, travel "
                     "planners. Used most for inquiring about specific information (flight times) or performing a "
                     "transaction (buying a ticket), and by people with disabilities. The most popular current use "
                     "is <b>call routing</b> with caller-led speech - &quot;I'm having problems with my voice "
                     "mail&quot;. <b>Directed dialogs</b> put the system in control, asking specific questions "
                     "requiring specific responses; more flexible systems let the user take the initiative "
                     "(&quot;I'd like to go to Paris next Monday for two weeks&quot;) but risk more errors because "
                     "the caller assumes the system is human. <b>Guided prompts</b> get callers back on track. Design "
                     "issues include the type of voice actor - male, female, neutral or dialect."),
                    ("10. Pen",
                     "Lightpens and styluses let people write, draw, select and move objects, capitalising on "
                     "drawing skills honed from childhood. Digital pens such as Anoto combine an ordinary ink pen "
                     "with a digital camera that records everything written on special paper. <b>Pro:</b> quick and "
                     "easy annotation of existing documents. <b>Cons:</b> the hand can occlude part of the screen "
                     "while writing, and there can be lag that feels clunky."),
                    ("11. Touch",
                     "Touch screens such as walk-up kiosks detect presence and location of a touch. Multi-touch "
                     "supports swiping, flicking, pinching, pushing and tapping. Much faster to scroll through "
                     "wheels, carousels and bars of thumbnails by finger flicking, but <b>more cumbersome, "
                     "error-prone and slower</b> to type on a virtual keyboard than a physical one."),
                    ("12. Air-based gestures",
                     "Camera recognition, sensors and computer vision recognise body, arm and hand gestures in a "
                     "room - Kinect and EyeToy. Movements map onto gaming motions: swinging, bowling, hitting, "
                     "punching, with players represented as avatars. Research issues: how the computer recognises "
                     "and <b>delineates</b> gestures (deictic and hand-waving), and whether holding a control device "
                     "feels more intuitive than controller-free gestures."),
                    ("13. Haptic",
                     "Tactile feedback applying vibration and forces to the body using actuators embedded in "
                     "clothing, often with motion capture. Can enrich the experience or nudge users to correct an "
                     "error, and can simulate the sense of touch between remote people. Design issues: where to "
                     "place actuators, whether to use single or sequenced touches, when to buzz and how intensely, "
                     "and how the wearer feels it in different contexts."),
                    ("14. Multimodal",
                     "Multiplies how information is experienced using different modalities - touch, sight, sound, "
                     "speech - to support more flexible, efficient and expressive interaction. The most common "
                     "combination is <b>speech and vision</b>. Research issues: recognising and analysing speech, "
                     "gesture and eye gaze; what is gained by combining inputs and outputs; and whether talking and "
                     "gesturing as humans do with each other is genuinely a natural way to interact with a computer."),
                    ("15. Shareable",
                     "Designed for <b>more than one person</b>, providing multiple inputs and sometimes simultaneous "
                     "input by co-located groups: large wall displays with pens or gestures, interactive tabletops "
                     "using fingertips - DiamondTouch, Smart Table, Surface. <b>Advantages:</b> a large interactional "
                     "space supporting flexible group working; multiple users can point to and touch displayed "
                     "information, view interactions simultaneously and share a point of reference; more equitable "
                     "participation than groups sharing one PC. <b>Findings:</b> horizontal surfaces support more "
                     "turn-taking and collaboration than vertical ones, and larger tabletops do <b>not</b> improve "
                     "group working - they encourage more division of labour."),
                    ("16. Tangible",
                     "Sensor-based interaction where physical objects such as bricks are coupled with digital "
                     "representations, so manipulating the object causes a digital effect. Examples: "
                     "<b>Chromarium cubes</b> (turning them mixes digital colour animations on an adjacent wall), "
                     "<b>Flow Blocks</b> (embedded numbers and lights vary with how blocks are connected), and "
                     "<b>Urp</b> (physical building models on a tabletop with tokens for wind and shadow, changing "
                     "digital shadows over time). <b>Benefits:</b> held in both hands, combined in ways other "
                     "interfaces cannot, explored by more than one person, placed on top of, beside and inside each "
                     "other, encouraging different ways of representing a problem space and leading to greater "
                     "insight, learning, problem-solving, creativity and reflection. <b>Design issue:</b> the "
                     "coupling should be <b>explicit</b> for learning and can be <b>implicit and unexpected</b> for "
                     "entertainment."),
                    ("17. Augmented &amp; mixed reality",
                     "<b>Augmented reality</b> superimposes virtual representations on physical devices and objects; "
                     "<b>mixed reality</b> combines views of the real world with views of a virtual environment. "
                     "Applications in medicine (virtual X-rays and scans), air traffic control (identifying planes "
                     "hard to make out), games, flying and exploring. Design issues: what kind of digital "
                     "augmentation, when and where in the physical environment, how to stand out without distracting "
                     "from the ongoing task, how to align with real-world objects, and which device to use."),
                    ("18. Wearable",
                     "Began with head- and eyewear-mounted cameras recording what was seen and accessing digital "
                     "information; since then jewellery, caps, smart fabrics, glasses, shoes and jackets. "
                     "Applications include automatic diaries, tour guides, cycle indicators and fashion clothing. "
                     "Google Glass was short-lived. Four design issues: <b>comfort</b> (light, small, unobtrusive, "
                     "fashionable, preferably hidden), <b>hygiene</b> (can the clothing be washed?), <b>ease of "
                     "wear</b> (can the electronics be removed and replaced?), and <b>usability</b> (how does the "
                     "user control embedded devices?)."),
                    ("19. Robots",
                     "Four types: <b>remote</b> robots in hazardous settings, <b>domestic</b> robots helping around "
                     "the house, <b>pet</b> robots as human companions, and <b>sociable</b> robots that work "
                     "collaboratively with humans and socialise with them as peers. <b>Drones</b> are unmanned "
                     "aircraft used for entertainment (carrying drinks and food at festivals), agriculture (flying "
                     "over vineyards and fields to collect data), and tracking poachers in African wildlife parks; "
                     "flying low and streaming photos that are stitched into maps to determine crop health and "
                     "harvest timing. Design questions: how humans react to physical versus virtual robots; whether "
                     "robots should look human or clearly robotic; and whether interaction should be human-like or "
                     "human-computer-like."),
                    ("20. Brain-computer",
                     "A BCI provides a communication pathway between a person's brain waves and an external device "
                     "such as a screen cursor. The person is trained to concentrate on the task, and the system "
                     "works by detecting changes in neural functioning. The slides' example is a woman who is "
                     "paralyzed selecting letters on screen."),
                ]),
                ("note", ("NATURAL USER INTERFACES (NUIs)",
                          "A NUI lets users interact with a computer in the same ways they interact with the "
                          "physical world - using voice, hands and bodies: speaking to machines, stroking their "
                          "surfaces, gesturing in the air, dancing on mats that detect feet movements, smiling to "
                          "get a reaction. The slides then ask the sceptical question directly: "
                          "<b>how natural are NUIs?</b>")),
                ("warn", ("WHICH INTERFACE? THE ANSWER IS ALWAYS THE SAME SHAPE",
                          "Is multimedia better than tangible for learning? Is speech as effective as command-based? "
                          "The answer will depend on <b>task, users, context, cost and robustness</b>. Note the "
                          "trends the slides state: mobile platforms taking over from PCs, speech being used more "
                          "for commercial services, appliance and vehicle interfaces becoming more important, and "
                          "shareable and tangible interfaces entering homes, schools, public places and workplaces.")),
            ],
        },
        {
            "id": "gui-components",
            "kicker": "07 - INSIDE THE GUI",
            "title": "Windows, menus and icons in detail",
            "lead": ("The GUI section breaks into three sub-topics that each carry their own design issues, and each "
                     "is examinable separately."),
            "blocks": [
                ("cards", [
                    ("i. Window design",
                     "Windows were invented to overcome the <b>physical constraints of a display</b>, enabling more "
                     "information to be viewed and more tasks performed; scroll bars extend this further. Multiple "
                     "windows make it hard to find the one you want - <b>listing, tabbing, iconizing, shrinking and "
                     "thumbnails</b> help. Research issues: window management letting users move fluidly between "
                     "windows and monitors; how to switch attention without getting distracted; applying spacing, "
                     "grouping and simplicity; which terms to use for options (&quot;Front&quot; versus &quot;bring "
                     "to front&quot;); and the finding that <b>mega menus are easier to navigate than drop-downs</b>."),
                    ("ii. Menu design",
                     "<b>Flat list</b> - good for showing many options at once on a small display. "
                     "<b>Drop-down</b> - shows more options on the same screen, including cascading. "
                     "<b>Pop-up</b> - appears when a command key is pressed. "
                     "<b>Contextual</b> - gives access to often-used commands for a particular item. "
                     "<b>Collapsible</b> - toggles between + and - on a header to expand or contract contents. "
                     "<b>Mega</b> - all options shown in a 2D drop-down layout."),
                    ("iii. Icon design",
                     "Icons are assumed to be easier to learn and remember than commands, can be compact and "
                     "variably positioned, and are now pervasive - desktop objects, tools (paintbrush), applications "
                     "(browser) and operations (cut, paste, next, accept, change). The mapping between "
                     "representation and referent can be <b>similar</b> (a picture of a file for the object file), "
                     "<b>analogical</b> (scissors for cut) or <b>arbitrary</b> (an X for delete). "
                     "<b>The most effective icons are similar ones.</b> Many operations are actions, which are "
                     "harder to represent, so designers combine objects and symbols capturing the salient part of "
                     "the action. Text labels help identification for small icon sets; for large sets - photo "
                     "editing, word processing - use the hover function."),
                ]),
                ("hook", ("MEMORY HOOK",
                          "Icon mappings: <b>S-A-A</b> - <b>S</b>imilar (file &rarr; file), <b>A</b>nalogical "
                          "(scissors &rarr; cut), <b>A</b>rbitrary (X &rarr; delete). Effectiveness falls in exactly "
                          "that order, so the first is best and the last must be learned.")),
            ],
        },
    ],
    "mistakes": [
        ("Confusing an assumption with a claim.",
         "An assumption takes something for granted when it needs further investigation. A claim states something "
         "to be true when it is still open to question. The 3D TV example gives one of each."),
        ("Mixing up interaction type and interface type.",
         "Interaction type is <b>what the user is doing</b> - instructing, conversing, manipulating, exploring, "
         "responding. Interface type is <b>the kind of interface</b> used to support it - speech, menu-based, "
         "gesture. One interaction type can be supported by many interface types."),
        ("Forgetting that Responding starts with the system.",
         "In the other four types the user initiates. In responding, the system takes the initiative and alerts the "
         "user with <b>no request made</b> - a location alert or a fitness milestone."),
        ("Listing only the benefits of interface metaphors.",
         "The slides give six problems: breaking conventional and cultural rules, constraining designers, "
         "conflicting with design principles, forcing users to understand only through the metaphor, transferring "
         "bad parts of existing designs, and limiting imagination."),
        ("&quot;Direct manipulation is always best.&quot;",
         "Not all tasks can be described by objects and not all actions done directly; some are better "
         "<b>delegated</b>, such as spell checking. DM can also gobble screen space, and mouse movement can be "
         "slower than function keys."),
        ("Assuming a bigger shared tabletop improves collaboration.",
         "The stated finding is the opposite: larger tabletops do <b>not</b> improve group working and encourage "
         "more division of labour. Horizontal surfaces do support more turn-taking than vertical ones."),
        ("Calling arbitrary icons the most effective.",
         "The most effective icons are <b>similar</b> ones - a picture of the thing itself. Analogical is second; "
         "arbitrary must simply be learned."),
    ],
    "cheat": (["Concept", "Shortest correct answer"], [
        ["Assumption", "Taking something for granted when it needs further investigation."],
        ["Claim", "Stating something to be true when it is still open to question."],
        ["Conceptual model", "A high-level description of how a system is organized and operates."],
        ["Model components", "Metaphors and analogies, concepts (task-domain objects, attributes, operations), relationships and mappings."],
        ["Interface metaphor", "An interface designed to be similar to a physical entity but with its own properties, e.g. the desktop."],
        ["Interaction types (5)", "Instructing, conversing, manipulating, exploring, responding."],
        ["Direct manipulation", "Continuous representation, physical actions instead of complex syntax, rapid reversible actions with immediate feedback (Shneiderman, 1983)."],
        ["WIMP", "Windows, Icons, Menus, Pointing device - first seen in the Xerox Star."],
        ["Menu kinds", "Flat list, drop-down (cascading), pop-up, contextual, collapsible, mega."],
        ["Icon mappings", "Similar, analogical, arbitrary - similar is most effective."],
        ["Presence (VR)", "The psychological sense of being in the virtual environment (Slater and Wilbur, 1999)."],
        ["Veen's web principles", "Where am I? Where can I go? What's here?"],
        ["Robot types (4)", "Remote, domestic, pet, sociable."],
        ["Wearable design issues", "Comfort, hygiene, ease of wear, usability."],
        ["NUI", "An interface letting users interact using voice, hands and bodies as they do with the physical world."],
        ["Which interface?", "Depends on task, users, context, cost and robustness."],
    ]),
    "quiz": [
        {"q": "A fitness band vibrates to tell the user they have hit 10,000 steps, without being asked. Which interaction type is this?",
         "options": ["Responding", "Instructing", "Conversing", "Exploring"], "correct": 0,
         "why": "Responding is the type where the system takes the initiative and alerts the user to something it "
                "judges relevant, with no request from the user - the fitness-milestone notification is the slides' "
                "own example. Instructing, conversing and exploring are all user-initiated."},
        {"q": "Which is a stated PROBLEM with interface metaphors?",
         "options": ["They can force users to understand the system only in terms of the metaphor",
                     "They make learning new systems harder",
                     "They prevent users from forming a conceptual model",
                     "They cannot be based on objects, only on activities"], "correct": 0,
         "why": "Forcing the user into the metaphor's frame is one of the six listed problems. Metaphors make "
                "learning <i>easier</i> and <i>help</i> users understand the conceptual model, and they can be based "
                "on an activity, an object, or a combination of both."},
        {"q": "Which property is NOT one of Shneiderman's three properties of direct manipulation?",
         "options": ["Commands expressed with a precise, learnable syntax",
                     "Continuous representation of objects and actions of interest",
                     "Physical actions and button pressing instead of complex syntax",
                     "Rapid, reversible actions with immediate feedback"], "correct": 0,
         "why": "Direct manipulation explicitly replaces complex command syntax with physical action, so requiring "
                "a precise syntax is the opposite of DM. The other three are the three properties as stated."},
        {"q": "An icon uses a pair of scissors to represent the cut operation. What kind of mapping is this?",
         "options": ["Analogical", "Similar", "Arbitrary", "Metaphorical"], "correct": 0,
         "why": "Analogical mapping uses something related by analogy - scissors cut, so scissors mean cut. A "
                "similar mapping would be a picture of a file to represent the object file; an arbitrary mapping "
                "would be an X for delete. Metaphorical is not one of the three mapping categories given."},
        {"q": "Research on shareable interfaces found which of the following about larger interactive tabletops?",
         "options": ["They do not improve group working and encourage more division of labour",
                     "They increase turn-taking compared with smaller tables",
                     "They eliminate the need for simultaneous input",
                     "They perform better vertically than horizontally"], "correct": 0,
         "why": "The stated finding is that providing larger tabletops does not improve group working but encourages "
                "division of labour. Shareable interfaces are defined by supporting simultaneous input, so nothing eliminates the need for it, and horizontal surfaces support more turn-taking than vertical ones, which rules out the claim that they perform better vertically."},
        {"q": "Veen's three web design principles are:",
         "options": ["Where am I? Where can I go? What's here?",
                     "Who are you? What do you want? Why are you here?",
                     "Visibility, feedback, consistency",
                     "Clarity, context, pleasure"], "correct": 0,
         "why": "Veen's principles are the three navigation questions. Visibility/feedback/consistency are Norman's "
                "design principles from Lecture 1, and clarity/context/pleasure echo Budd's (2007) website heuristics "
                "from Lecture 13."},
    ],
    "lab": [
        ("A team proposes an in-car voice assistant that reads out incoming messages while driving. Identify the assumption and the claim, and say what the real problem might be.",
         "The <b>assumption</b> is that drivers want to keep up with messages while driving - taken for granted "
         "without investigation. The <b>claim</b> is that voice output is safe while driving because the hands stay "
         "on the wheel - stated as true but open to question, and Lecture 2 shows it is false, since the cognitive "
         "processing, not the handset, consumes attention. Reframing the real problem: drivers feel obliged to be "
         "reachable, which suggests solutions such as automatic do-not-disturb with an auto-reply, rather than "
         "reading messages aloud."),
        ("Choose an interaction type and an interface type for a museum exhibit teaching children how a river system works, and justify both.",
         "<b>Interaction type: manipulating</b>, sharpened as tangible interaction, because children can hold and "
         "combine objects in ways other interfaces do not allow, and because tangible interfaces let more than one "
         "child explore together and encourage different ways of representing a problem space, leading to greater "
         "insight and learning. <b>Interface type: tangible plus shareable</b> - physical blocks on a horizontal "
         "tabletop, since horizontal surfaces support more turn-taking than vertical ones and shareable interfaces "
         "give more equitable participation than a single shared PC. The coupling between physical action and "
         "digital effect should be <b>explicit</b>, because the slides state that explicit mapping is critical when "
         "the goal is learning; implicit and unexpected coupling belongs in entertainment."),
        ("Argue whether a natural user interface is genuinely natural, using this lecture's own material.",
         "A NUI lets users interact using voice, hands and bodies as they do with the physical world, which "
         "leverages the same knowledge that makes manipulating and physical affordances effective. But the slides "
         "ask &quot;how natural are NUIs?&quot; and the deck supplies the counter-evidence: conversational systems "
         "misunderstand what users - especially children - say; air gestures raise the unsolved problem of how the "
         "computer delineates a gesture from ordinary movement, and whether holding a control device actually feels "
         "more intuitive than being controller-free; and multimodal interfaces still leave open whether talking and "
         "gesturing as humans do with each other is a natural way to interact with a <i>computer</i>. The defensible "
         "position is that NUIs are natural in their <i>input vocabulary</i> but not in their <i>conceptual "
         "model</i> - the user still has to learn what the system will accept."),
    ],
    "branches": [
        ("Understanding the problem space",
         "Establishing what you want to create, what your assumptions are, and whether it will achieve what you hope, before moving to design.",
         ["An assumption takes something for granted when it needs further investigation.",
          "A claim states something to be true when it is still open to question.",
          "Ask whether there are problems with an existing product or user experience, and what they are.",
          "Ask why you think there are problems and how proposed ideas might overcome them.",
          "For a new user experience, ask how the ideas support, change or extend current ways of doing things.",
          "During early ideation, ask questions, reconsider assumptions and articulate concerns.",
          "Benefits of conceptualizing: orientation, open-mindedness and common ground."],
         [("Robot waiters", "The stated benefits - taking orders, entertaining customers, recommending for fussy eaters - are assumptions; the real problem is difficulty recruiting good wait staff."),
          ("3D TV", "No existing problem was being solved; the assumption was that people would enjoy the enhanced clarity, and the claim was that they would pay much more for it.")]),
        ("Conceptual models",
         "A high-level description of how a system is organized and operates, letting designers straighten out their thinking before laying out widgets.",
         ["Components are metaphors and analogies, the concepts users are exposed to, and the relationships and mappings between them.",
          "Concepts include task-domain objects, their attributes and their operations.",
          "First steps ask what users will be doing, how the system supports it, which metaphor is appropriate, and which interaction modes and styles to use.",
          "The best conceptual models appear obvious and simple, and the operations they support are intuitive.",
          "A good understanding of the problem space informs the design space - what interface, behaviour and functionality to provide."],
         [("Online shopping", "Shopping cart, proceeding to check-out, 1-click, gift wrapping and the cash till are the model's components, all borrowed from a physical shop."),
          ("Mood board", "Used in conceptual design to capture the intended feel before any layout decisions are made.")]),
        ("Interface metaphors",
         "An interface designed to be similar to a physical entity while having its own properties, exploiting familiar knowledge to help users understand the unfamiliar.",
         ["Can be based on an activity, an object, or a combination of both.",
          "Conjures up the essence of an unfamiliar activity so users can leverage it.",
          "Benefits: easier learning, better understanding of the conceptual model, and greater accessibility to a diversity of users.",
          "Problems: breaking conventional and cultural rules, constraining how designers conceptualize the problem space, conflicting with design principles.",
          "Further problems: forcing users to understand only through the metaphor, transferring bad parts of existing designs, and limiting imagination."],
         [("The desktop", "The canonical conceptual model instantiated at the interface - though a recycle bin on a desk breaks a real-world rule."),
          ("The card metaphor", "A familiar form factor that can be flicked through, sorted and themed, chunking content the way paragraphs chunk sentences."),
          ("Literal calculator", "A calculator designed too literally imports the physical device's limitations instead of exploiting the screen.")]),
        ("Interaction types",
         "Five descriptions of what the user is doing when interacting with a system.",
         ["Instructing: issuing commands and selecting options; quick and efficient, good for repetitive actions on multiple objects.",
          "Conversing: interacting as if having a conversation; comfortable for novices but prone to parsing failures.",
          "Manipulating: dragging, selecting, opening, closing and zooming, exploiting physical-world knowledge.",
          "Exploring: moving through virtual or physical environments, including sensor-triggered physical spaces.",
          "Responding: the system takes the initiative and alerts the user with no request made.",
          "Direct manipulation (Shneiderman, 1983) requires continuous representation, physical actions instead of complex syntax, and rapid reversible actions with immediate feedback.",
          "Direct manipulation suits doing tasks, instructing suits repetitive tasks, and conversing suits children, computer-phobic and disabled users.",
          "Hybrid conceptual models support several ways of doing the same action but take longer to learn."],
         [("DM benefits", "Novices learn quickly, experts work rapidly, intermittent users retain concepts, error messages are rarely needed, and users feel in control."),
          ("DM limits", "Spell checking is better delegated than manipulated directly; DM can gobble screen space and mouse movement can be slower than function keys."),
          ("Responding in practice", "An alert about a nearby coffee bar where friends are meeting, or a fitness tracker announcing a milestone.")]),
        ("Classic interface types",
         "Command-based, WIMP and GUI, multimedia, virtual reality, information visualization, web, consumer electronics and mobile.",
         ["Command-based interfaces are efficient, precise and fast but carry a large learning overhead; consistency is the most important design principle for them.",
          "WIMP means windows, icons, menus and a pointing device, first seen in the Xerox Star.",
          "GUIs add colour, 3D, sound, animation, toolbars, docks and rollovers.",
          "Multimedia combines graphics, text, video, sound and animation, but users tend to play clips while skimming text.",
          "Virtual reality provides the illusion of participation rather than external observation (Gigante, 1993) and induces a sense of presence (Slater and Wilbur, 1999).",
          "Information visualization amplifies human cognition so users can see patterns, trends and anomalies (Card et al., 1999).",
          "Web design balances ease of finding something against an aesthetic, enjoyable experience, guided by Veen's three questions.",
          "Consumer electronics are used for short periods and must be usable with minimal learning, designed as transient interfaces.",
          "Mobile interfaces must cope with small screens, few keys and restricted controls."],
         [("Second Life command interface", "A command-based interface built for visually impaired users, showing that text commands remain an accessibility tool."),
          ("VR therapy", "Virtual environments help people overcome phobias such as spiders and public speaking, and train pilots in flight simulators."),
          ("Mobile in the field", "Handhelds take restaurant orders, check in rental car returns, check supermarket stock and support street gaming and life-long learning.")]),
        ("Post-WIMP interface types",
         "Speech, pen, touch, air gestures, haptic, multimodal, shareable, tangible, augmented and mixed reality, wearable, robots and brain-computer.",
         ["Speech interfaces are used most for call routing, with directed dialogs controlled by the system and flexible dialogs risking more errors.",
          "Pen interfaces capitalise on drawing skills but suffer occlusion by the hand and lag.",
          "Touch and multi-touch support swiping, flicking, pinching, pushing and tapping, but virtual keyboards are slower and more error-prone than physical ones.",
          "Air-based gestures raise the problem of how the computer recognises and delineates a gesture.",
          "Haptic interfaces apply vibration and force through actuators, raising questions of placement, sequencing and intensity.",
          "Multimodal interfaces combine modalities, most commonly speech and vision.",
          "Shareable interfaces support co-located groups, with horizontal surfaces encouraging more turn-taking than vertical ones.",
          "Tangible interfaces couple physical objects with digital representations, using explicit coupling for learning and implicit coupling for entertainment.",
          "Augmented reality superimposes virtual representations on physical objects; mixed reality combines real and virtual views.",
          "Wearables raise comfort, hygiene, ease of wear and usability issues.",
          "Robots come in remote, domestic, pet and sociable types, with drones used in entertainment, agriculture and conservation.",
          "Brain-computer interfaces detect changes in neural functioning to control an external device."],
         [("Tangible examples", "Chromarium cubes mix digital colour animations when turned, Flow Blocks change numbers and lights depending on connection, and Urp casts changing digital shadows around physical building models."),
          ("Drones in agriculture", "Flying low over vineyards and fields, streaming photos that are stitched into maps to judge crop health and harvest timing."),
          ("BCI in use", "A woman who is paralyzed selects letters on a screen by concentrating, with the system reading changes in neural functioning.")]),
        ("GUI components in detail",
         "Windows, menus and icons each carry their own design and research issues.",
         ["Windows overcome the physical constraints of a display and let more information be viewed and more tasks performed.",
          "Listing, tabbing, iconizing, shrinking and thumbnails help users find the window they want.",
          "Window management should let users move fluidly between windows and monitors without being distracted.",
          "Mega menus are easier to navigate than drop-down menus.",
          "Menu kinds are flat list, drop-down and cascading, pop-up, contextual, collapsible and mega.",
          "Icons can map to their referent in a similar, analogical or arbitrary way, and similar icons are most effective.",
          "Actions are harder to represent than objects, so designers combine objects and symbols capturing the salient part of the action.",
          "Text labels help small icon sets; the hover function helps large sets such as photo editing or word processing."],
         [("Flat list", "Good for showing a large number of options at once when the display is small, such as a smartwatch."),
          ("Contextual menu", "Gives access to the commands most often used with one particular item, keeping the main menu shorter.")]),
        ("Natural user interfaces and choosing an interface",
         "NUIs let users interact using voice, hands and bodies as in the physical world, and the choice among interfaces depends on context rather than a ranking.",
         ["Instead of a keyboard, users speak to machines, stroke surfaces, gesture in the air, dance on mats, or smile to get a reaction.",
          "The slides ask directly how natural NUIs really are.",
          "Which interface is best will depend on task, users, context, cost and robustness.",
          "Mobile platforms are taking over from PCs.",
          "Speech interfaces are being used much more for commercial services.",
          "Appliance and vehicle interfaces are becoming more important.",
          "Shareable and tangible interfaces are entering homes, schools, public places and workplaces.",
          "An underlying concern for any interface is how information is represented so the user can carry out the ongoing task."],
         [("Comparison questions", "Is multimedia better than tangible for learning, speech as effective as command-based, or a wearable better than a mobile for finding information in a foreign city? Each answer is conditional."),
          ("Hybrid models", "Supporting several ways of doing the same action at the interface is common, but increases learning time.")]),
    ],
    "exam_mcq": [
        {"q": "Which statement is a CLAIM rather than an assumption?",
         "options": ["&quot;A multimodal style of interaction for controlling GPS that involves speaking while driving is safe&quot;",
                     "&quot;People will want to watch TV while driving&quot;",
                     "&quot;Users prefer larger fonts&quot;",
                     "&quot;Everyone owns a smartphone&quot;"],
         "correct": 0,
         "why": "A claim states something to be true while it is still open to question, and the GPS statement is the "
                "slides' own example. The others are assumptions - things taken for granted without investigation."},
        {"q": "Which is the correct definition of a conceptual model?",
         "options": ["A high-level description of how a system is organized and operates",
                     "A scale prototype of the final product",
                     "A diagram of the system's database tables",
                     "The set of screens a user will see"],
         "correct": 0,
         "why": "The lecture defines it as a high-level description of how a system is organized and operates, "
                "enabling designers to straighten out their thinking before laying out widgets. Prototypes, data "
                "models and screen sets are all later, more concrete artifacts."},
        {"q": "Which interaction type does a Kinect-style bowling game primarily use?",
         "options": ["Manipulating", "Instructing", "Responding", "Conversing"],
         "correct": 0,
         "why": "Manipulating exploits users' knowledge of how they move in the physical world, and the lecture "
                "lists air gestures with Kinect among its examples. Instructing is issuing commands, responding is "
                "system-initiated, and conversing is dialogue-based."},
        {"q": "Which of these is a stated DISADVANTAGE of direct manipulation?",
         "options": ["Some tasks, such as spell checking, are better achieved by delegating",
                     "Novices cannot learn the basic functionality",
                     "Users experience more anxiety than with command interfaces",
                     "Error messages become more frequent"],
         "correct": 0,
         "why": "Delegation is the listed limitation - not all tasks map to objects and direct actions. The other "
                "three reverse the stated benefits: novices learn quickly, users experience less anxiety, and error "
                "messages are rarely needed."},
        {"q": "In VR, the &quot;psychological sense of being in the virtual environment&quot; is called:",
         "options": ["Presence", "Immersion", "Fidelity", "Embodiment"],
         "correct": 0,
         "why": "Slater and Wilbur (1999) define presence as a state of consciousness, the psychological sense of "
                "being in the virtual environment. Fidelity refers to how closely objects match what they represent, "
                "and the other terms are not the definition given."},
        {"q": "Which pair of wearable design issues does the lecture list?",
         "options": ["Hygiene and ease of wear", "Latency and bandwidth",
                     "Fidelity and presence", "Reliability and portability"],
         "correct": 0,
         "why": "The four wearable design issues are comfort, hygiene, ease of wear and usability. Latency and "
                "bandwidth are not raised there; fidelity and presence belong to VR; reliability and portability "
                "belong to the construction qualities in the prototyping lecture."},
    ],
    "exam_short": [
        {"q": "Explain the difference between an assumption and a claim, and illustrate both with the 3D TV example.",
         "keywords": ["assumption", "claim", "granted", "question"],
         "answer": "An assumption takes something for granted when it needs further investigation; a claim states "
                   "something to be true when it is still open to question. With 3D TV there was no existing "
                   "problem to overcome - it proposed a new way of experiencing television. The assumption was that "
                   "people would really enjoy the enhanced clarity and colour detail provided by 3D. The claim was "
                   "that people would not mind paying a lot more for a 3D-enabled screen because of the new "
                   "experience. Both needed evidence and neither got it."},
        {"q": "Name the five interaction types and give one example of each.",
         "keywords": ["instruct", "convers", "manipulat", "explor", "respond"],
         "answer": "Instructing - telling a word processor to print or save a file. Conversing - asking a voice "
                   "assistant or an advice-giving system a question in natural language. Manipulating - dragging, "
                   "zooming or using a Wii controller to move an on-screen avatar. Exploring - flying over a virtual "
                   "3D city or walking through a sensor-equipped physical space that triggers events. Responding - "
                   "a fitness tracker alerting the user to a milestone, or a phone alerting them to a nearby coffee "
                   "bar where friends are meeting, with no request from the user."},
        {"q": "Give three benefits and three problems of interface metaphors.",
         "keywords": ["metaphor", "learn", "constrain", "cultural"],
         "answer": "Benefits: they make learning new systems easier; they help users understand the underlying "
                   "conceptual model; and they can be innovative, making computers and their applications accessible "
                   "to a greater diversity of users. Problems: they break conventional and cultural rules, as with a "
                   "recycle bin placed on a desktop; they can constrain designers in how they conceptualize the "
                   "problem space; and they force users to understand the system only in terms of the metaphor. "
                   "Others include conflicting with design principles, transferring the bad parts of existing "
                   "designs, and limiting designers' imagination."},
        {"q": "State Shneiderman's three properties of direct manipulation and two of its benefits and limitations.",
         "keywords": ["continuous", "reversible", "feedback", "delegat"],
         "answer": "The three properties are continuous representation of the objects and actions of interest; "
                   "physical actions and button pressing instead of issuing commands with complex syntax; and rapid, "
                   "reversible actions with immediate feedback on the object of interest. Benefits: novices learn "
                   "the basic functionality quickly, and users immediately see whether their actions are furthering "
                   "their goals, so they experience less anxiety and feel in control. Limitations: not all tasks can "
                   "be described by objects and some are better delegated, such as spell checking; and direct "
                   "manipulation can gobble screen space, while moving a mouse can be slower than pressing function "
                   "keys."},
        {"q": "Describe the three kinds of mapping between an icon and its referent, and say which is most effective.",
         "keywords": ["similar", "analog", "arbitrar", "icon"],
         "answer": "A <b>similar</b> mapping uses a picture of the thing itself, such as a picture of a file to "
                   "represent the object file. An <b>analogical</b> mapping uses something related by analogy, such "
                   "as a pair of scissors to represent cut. An <b>arbitrary</b> mapping has no natural relation, "
                   "such as an X to represent delete, and must simply be learned. The most effective icons are the "
                   "similar ones. Because many operations are actions rather than objects, and actions are harder to "
                   "depict, designers often combine objects and symbols that capture the salient part of the action."},
        {"q": "You must choose an interface for a public transport information kiosk in a busy station. Which types would you consider, and on what basis would you decide?",
         "keywords": ["touch", "context", "transient", "speech"],
         "answer": "The decision depends on task, users, context, cost and robustness. A kiosk is a consumer-style "
                   "transient interface used for short periods, so it must be usable with minimal or no learning and "
                   "kept simple. A <b>touch</b> interface fits: walk-up kiosks detect the presence and location of a "
                   "touch, and finger flicking is fast for scrolling lists of destinations, though typing on a "
                   "virtual keyboard is slower and more error-prone than on a physical one, so free-text entry "
                   "should be minimised. A <b>speech</b> interface would suit users with visual impairments and "
                   "handles specific enquiries well, but a busy station is a noisy environment - a situational "
                   "impairment - which undermines recognition. A hybrid supporting both, with a physical keypad "
                   "fallback, covers the widest range of users, at the cost of longer learning and higher build "
                   "cost. Robustness matters more than richness because the device is unattended and used by "
                   "everybody."},
    ],
})


LECTURES.append({
    "num": 5,
    "slug": "the-process-of-interaction-design",
    "title": "The Process of Interaction Design",
    "short": "The Design Process",
    "lecture_label": "Lecture 5",
    "theme": "loop",
    "accent": "#3ad29f",
    "accent2": "#5b8def",
    "tagline": "User-centred design, the four basic activities, and the practical questions of users, needs and alternatives.",
    "hero_title": "Designers never get it right<br><em>the first time.</em>",
    "hero_sub": ("Interaction design is a <b>process</b>: discovering requirements, designing to fulfil them, "
                 "producing prototypes and evaluating them - focused on users and their goals, and involving "
                 "trade-offs to balance conflicting requirements. Generating alternatives and choosing between "
                 "them is the key skill."),
    "badges": ["4 design approaches", "User involvement", "3 UCD principles",
               "4 basic activities", "Stakeholder categories", "A/B testing"],
    "outcomes": [
        "Explain the advantages of involving users in development.",
        "Explain the main principles of a user-centered approach.",
        "Present a simple lifecycle model of interaction design.",
        "Identify users and stakeholders and explain what 'needs' means.",
        "Explain where alternatives come from and how to choose among them.",
    ],
    "sections": [
        {
            "id": "process",
            "kicker": "01 - INTERACTION DESIGN AS A PROCESS",
            "title": "Four approaches, one process",
            "lead": ("Interaction design is a process focused on discovering requirements, designing to fulfil them, "
                     "producing prototypes and evaluating them; focused on users and their goals; and involving "
                     "trade-offs to balance conflicting requirements."),
            "blocks": [
                ("table", (["The four approaches", "What drives the design"], [
                    ["<b>User-centered design</b>", "The user is the primary source; the designer studies and involves them."],
                    ["<b>Activity-centered design</b>", "The activity being carried out, rather than any individual user."],
                    ["<b>Systems design</b>", "The system and its context as a whole."],
                    ["<b>Genius design</b>", "The designer's own creative judgement and expertise."],
                ])),
                ("p", "Before designing anything you must <b>explore the problem space</b>: what is the current user "
                      "experience, why is a change needed, and how will this change improve the situation? "
                      "Articulating the problem space is a <b>team effort</b> - it means exploring different "
                      "perspectives and avoiding incorrect assumptions and unsupported claims."),
                ("hook", ("MEMORY HOOK",
                          "Four approaches, four sources of authority: <b>the user, the activity, the system, the "
                          "designer</b>. Only the last one is not a source of evidence - which is why the course "
                          "teaches the first.")),
            ],
        },
        {
            "id": "involvement",
            "kicker": "02 - INVOLVING USERS",
            "title": "Degrees of user involvement",
            "lead": ("There is no single right level of user involvement - each option trades input quality against "
                     "the user's continued representativeness."),
            "blocks": [
                ("table", (["User as team member", "Benefit", "Cost"], [
                    ["<b>Full time</b>", "Constant input.", "They lose touch with the users they represent."],
                    ["<b>Part time</b>", "Keeps one foot in the user community.", "Patchy input, and very stressful."],
                    ["<b>Short term</b>", "Fresh perspective.", "Inconsistent across the project's life."],
                    ["<b>Long term</b>", "Consistent input.", "They lose touch with users."],
                ])),
                ("list", [
                    "Face-to-face group or individual activities.",
                    "Online contributions from thousands of users: <b>Online Feedback Exchange (OFE)</b> systems, "
                    "<b>crowdsourcing</b> design ideas, and <b>citizen science</b>.",
                    "User involvement <b>after product release</b> - the process does not stop at launch.",
                ]),
                ("warn", ("THE CENTRAL TENSION",
                          "Notice that <b>full time</b> and <b>long term</b> have the <i>same</i> drawback: the more "
                          "embedded a user representative becomes in the design team, the less they resemble the "
                          "users they were recruited to represent. That is why user involvement must be "
                          "<b>refreshed</b>, not just secured once.")),
            ],
        },
        {
            "id": "ucd",
            "kicker": "03 - USER-CENTERED DESIGN",
            "title": "The three principles",
            "lead": "A user-centered approach rests on exactly three principles, and the exam expects all three.",
            "blocks": [
                ("steps", [
                    ("Early focus on users and tasks",
                     "Directly studying cognitive, behavioural, anthropomorphic and attitudinal characteristics."),
                    ("Empirical measurement",
                     "Users' reactions and performance to scenarios, manuals, simulations and prototypes are "
                     "observed, recorded and analysed."),
                    ("Iterative design",
                     "When problems are found in user testing, fix them and carry out more tests."),
                ]),
                ("hook", ("MEMORY HOOK",
                          "<b>Study them early, measure them empirically, then do it again.</b> "
                          "Early focus &rarr; empirical measurement &rarr; iteration. Each principle feeds the next, "
                          "and the third feeds back into the first.")),
            ],
        },
        {
            "id": "activities",
            "kicker": "04 - THE FOUR BASIC ACTIVITIES",
            "title": "Requirements, alternatives, prototypes, evaluation",
            "lead": ("These are the same four activities named in Lecture 1, now with their internal detail. "
                     "Three key characteristics permeate all four."),
            "blocks": [
                ("cards", [
                    ("1. Discovering requirements",
                     "To design, you must know your target users and what kind of support an interactive product "
                     "could usefully provide. This is <b>fundamental to the user-centered approach</b>, and these "
                     "needs are understood through <b>data gathering and analysis</b>."),
                    ("2. Designing alternatives",
                     "The core activity: suggesting ideas for meeting the requirements. It breaks into two "
                     "sub-activities. <b>(a) Conceptual design</b> - producing the conceptual model, describing what "
                     "people can do with the product and what concepts are needed to understand how to interact with "
                     "it. <b>(b) Physical design</b> - the details: colours, sounds, images, menu design, icon design."),
                    ("3. Prototyping",
                     "The most sensible way for users to evaluate a design is to <b>interact with it</b>. "
                     "<b>Paper-based prototypes are very quick and cheap to build and very effective at identifying "
                     "problems in the early stages.</b> Through role-playing, users get a real sense of what it will "
                     "be like to interact with the product."),
                    ("4. Evaluating",
                     "The process of determining the <b>usability and acceptability</b> of the product or design - "
                     "testing to make sure the final product is fit-for-purpose."),
                ]),
                ("note", ("THE THREE KEY CHARACTERISTICS",
                          "1. Focus on users <b>early</b> in the design and evaluation of the artefact. "
                          "2. Identify, document and agree <b>specific usability and user experience goals</b>. "
                          "3. <b>Iteration is inevitable</b> - designers never get it right the first time.")),
                ("table", (["Alternative lifecycle model", "Source", "Character"], [
                    ["Simple interaction design lifecycle", "Sharp, Preece &amp; Rogers", "The four activities in an iterative loop."],
                    ["Google Design Sprints", "Knapp et al. (2016)", "A compressed, time-boxed run through the same logic."],
                    ["Research in the Wild", "Rogers &amp; Marshall (2017)", "A framework for studying technology in natural settings."],
                ])),
            ],
        },
        {
            "id": "users",
            "kicker": "05 - WHO ARE THE USERS?",
            "title": "Users, stakeholders, and the three categories",
            "lead": ("&quot;Who are the users?&quot; is not as obvious as it sounds. Sha Zhao et al. (2016) "
                     "identified <b>382 distinct types of users</b> for smartphone apps."),
            "blocks": [
                ("list", [
                    "Many products are intended for large sections of the population, so the user is "
                    "&quot;everybody&quot;. More targeted products are associated with specific <b>roles</b>.",
                    "<b>Stakeholders</b> are a larger group than direct users. Identifying them helps identify which "
                    "groups to include in interaction design activities.",
                    "Stakeholders include: those who interact directly with the product; those who manage direct "
                    "users; those who receive output from the product; those who make the purchasing decision; and "
                    "those who use competitors' products.",
                ]),
                ("table", (["Eason's (1987) three categories", "Definition"], [
                    ["<b>Primary</b>", "Frequent, hands-on users."],
                    ["<b>Secondary</b>", "Occasional users, or people who use it via someone else."],
                    ["<b>Tertiary</b>", "People affected by its introduction, or who will influence its purchase."],
                ])),
                ("hook", ("MEMORY HOOK",
                          "<b>Primary touches it, secondary occasionally touches it, tertiary is touched by it.</b> "
                          "The tertiary category is the one people forget - and it includes the person signing the "
                          "cheque.")),
            ],
        },
        {
            "id": "needs-alternatives",
            "kicker": "06 - NEEDS AND ALTERNATIVES",
            "title": "What 'needs' means, and where alternatives come from",
            "lead": ("<b>Users rarely know what is possible</b>, so you cannot simply ask them to state their "
                     "requirements."),
            "blocks": [
                ("steps", [
                    ("Explore the problem space", "Understand the situation before proposing solutions."),
                    ("Investigate who the users are", "Identify roles, categories and stakeholders."),
                    ("Investigate user activities", "See what can be improved in how things are done now."),
                    ("Try out ideas with potential users", "Test rather than ask."),
                ]),
                ("warn", ("THE KEY SENTENCE",
                          "Focus on people's <b>goals</b>, and on usability and user experience goals, rather than "
                          "expecting stakeholders to articulate requirements. Users are experts in their problems, "
                          "not in your solutions.")),
                ("p", "Humans tend to stick with something that works, so considering alternatives is what identifies "
                      "better designs. The lecture lists where they come from:"),
                ("list", [
                    "<b>Flair and creativity</b> - research and synthesis.",
                    "<b>Cross-fertilisation</b> of ideas from different perspectives.",
                    "<b>Users</b> can generate different designs.",
                    "<b>Product evolution</b> based on changing use.",
                    "<b>Seeking inspiration</b> from similar products and domains, or from different products and "
                    "domains.",
                    "All of it balanced against <b>constraints and trade-offs</b>.",
                ]),
            ],
        },
        {
            "id": "choosing",
            "kicker": "07 - CHOOSING BETWEEN ALTERNATIVES",
            "title": "Externally visible, measurable behaviour",
            "lead": ("Interaction design focuses on <b>externally visible and measurable behaviour</b>, which is why "
                     "the choice between alternatives is made with prototypes rather than documents."),
            "blocks": [
                ("cards", [
                    ("Technical feasibility",
                     "Some ideas are simply not buildable within the project's technology, budget or time."),
                    ("Evaluation with users or peers",
                     "Use <b>prototypes, not static documentation</b>, because behaviour is the thing being judged "
                     "and documentation cannot behave."),
                    ("A/B testing",
                     "An online method for informing the choice between alternatives. It is <b>nontrivial</b> to set "
                     "appropriate metrics and to choose the user group sets."),
                    ("Quality thresholds",
                     "Different stakeholder groups have different quality thresholds. Usability and user experience "
                     "goals lead to the relevant criteria."),
                ]),
                ("hook", ("MEMORY HOOK",
                          "Why prototypes and not documents? Because <b>behaviour is key</b>, and a document does "
                          "not behave. That one clause answers most questions in this section.")),
            ],
        },
    ],
    "mistakes": [
        ("Giving only two user-centred design principles.",
         "There are three: early focus on users and tasks, empirical measurement, and iterative design. Dropping "
         "empirical measurement is the most common omission."),
        ("Confusing conceptual design with physical design.",
         "Both are sub-activities of <b>designing alternatives</b>. Conceptual design produces the conceptual model "
         "- what people can do and what concepts they need. Physical design covers colours, sounds, images, menus "
         "and icons."),
        ("&quot;Ask the users what they need.&quot;",
         "Users rarely know what is possible. Explore the problem space, investigate users and their activities, and "
         "try out ideas with them - focusing on <b>goals</b> rather than stated requirements."),
        ("Treating stakeholders as a synonym for users.",
         "Stakeholders are a larger group: managers of direct users, recipients of the output, purchasers, and users "
         "of competitors' products. Eason's categories are primary, secondary and tertiary."),
        ("Assuming full-time user involvement is best.",
         "Full-time involvement gives constant input but the representative <b>loses touch with users</b> - the same "
         "drawback as long-term involvement."),
        ("Choosing between alternatives using specifications.",
         "Interaction design focuses on externally visible and measurable behaviour, so the choice is made with "
         "prototypes, not static documentation."),
    ],
    "cheat": (["Concept", "Shortest correct answer"], [
        ["Four design approaches", "User-centered, activity-centered, systems design, genius design."],
        ["UCD principles (3)", "Early focus on users and tasks; empirical measurement; iterative design."],
        ["Four basic activities", "Discovering requirements, designing alternatives, prototyping, evaluating."],
        ["Designing alternatives", "Splits into conceptual design (the model) and physical design (colours, sounds, images, menus, icons)."],
        ["Three key characteristics", "Early focus on users; documented usability and UX goals; iteration is inevitable."],
        ["Eason's user categories", "Primary (frequent hands-on), secondary (occasional or via someone else), tertiary (affected by it or influencing purchase)."],
        ["Degrees of involvement", "Full time, part time, short term, long term; plus OFE systems, crowdsourcing, citizen science, and post-release involvement."],
        ["Needs", "Users rarely know what is possible; explore the problem space, investigate users and activities, try ideas out, focus on goals."],
        ["Sources of alternatives", "Flair and creativity, cross-fertilisation, users, product evolution, inspiration from similar and different domains."],
        ["Choosing alternatives", "Technical feasibility, evaluation with users or peers using prototypes, A/B testing, quality thresholds."],
        ["A/B testing", "An online method for choosing between alternatives; setting metrics and user groups is nontrivial."],
        ["Paper prototypes", "Quick, cheap and very effective at identifying problems in early design."],
    ]),
    "quiz": [
        {"q": "Which of these is NOT one of the three principles of a user-centered approach?",
         "options": ["Genius design", "Early focus on users and tasks",
                     "Empirical measurement", "Iterative design"], "correct": 0,
         "why": "Genius design is one of the four design <i>approaches</i>, driven by the designer's own judgement - "
                "it is not a principle of user-centred design. The other three are exactly the three principles."},
        {"q": "A hospital director will not use the new records system but decides whether to buy it. Which of Eason's categories does she fall into?",
         "options": ["Tertiary", "Primary", "Secondary", "She is not a stakeholder"], "correct": 0,
         "why": "Tertiary users are those affected by the product's introduction or who influence its purchase. "
                "Primary users are frequent hands-on users, secondary are occasional users or those who use it "
                "through someone else, and a purchaser is explicitly listed among the stakeholders."},
        {"q": "Why does the lecture insist that prototypes, not static documentation, be used to choose between alternatives?",
         "options": ["Because interaction design focuses on externally visible and measurable behaviour",
                     "Because documentation is more expensive to produce",
                     "Because prototypes are always closer to the final product",
                     "Because stakeholders cannot read specifications"], "correct": 0,
         "why": "The stated reason is that behaviour is key, and documentation cannot behave. Cost is not the "
                "argument; low-fidelity prototypes are deliberately unlike the final product; and stakeholder "
                "literacy is not the issue raised."},
        {"q": "Which pair of user-involvement arrangements shares the same drawback?",
         "options": ["Full time and long term - both lose touch with users",
                     "Part time and short term - both are too expensive",
                     "Full time and part time - both give patchy input",
                     "Short term and long term - both are inconsistent"], "correct": 0,
         "why": "Full-time involvement gives constant input but loses touch with users; long-term involvement gives "
                "consistent input and also loses touch with users. Part time is patchy and stressful; short term is "
                "inconsistent across the project's life."},
        {"q": "Producing the outline of what people can do with a product and the concepts needed to understand it is which sub-activity?",
         "options": ["Conceptual design", "Physical design", "Prototyping", "Evaluating"], "correct": 0,
         "why": "That is the definition of conceptual design, one of the two sub-activities of designing "
                "alternatives. Physical design covers colours, sounds, images, menu design and icon design; "
                "prototyping and evaluating are separate activities."},
        {"q": "Sha Zhao et al. (2016) reported how many distinct types of user for smartphone apps?",
         "options": ["382", "38", "7", "1,024"], "correct": 0,
         "why": "The figure given is 382 distinct types, used to show that 'who are the users' is far less obvious "
                "than it appears."},
    ],
    "lab": [
        ("Your client says &quot;just ask our customers what features they want, then build those.&quot; Explain why this is not what the course means by establishing needs.",
         "Users rarely know what is possible, so asking them to name features returns variations on what already "
         "exists rather than what would actually help. The course's approach is to <b>explore the problem space</b> "
         "(what is the current experience, why is a change needed, how would it improve things), <b>investigate who "
         "the users are</b> including secondary and tertiary stakeholders, <b>investigate user activities</b> to see "
         "what can be improved in the way things are currently done, and <b>try out ideas with potential users</b>. "
         "Throughout, the focus is on people's goals and on agreed usability and UX goals, rather than on "
         "stakeholders articulating requirements. Humans stick with what works, so alternatives have to be "
         "deliberately generated rather than requested."),
        ("Identify primary, secondary and tertiary users for a university course-registration system, and say which you would recruit for testing.",
         "<b>Primary:</b> students registering for courses - frequent hands-on use. <b>Secondary:</b> academic "
         "advisors who occasionally register a student on their behalf, and registry staff who correct entries. "
         "<b>Tertiary:</b> the deans who approve the purchase, the timetabling office affected by the resulting "
         "enrolment data, and IT support who inherit the maintenance. For testing, recruit primary users for task "
         "performance because they generate the volume of use, but include secondary users because their tasks "
         "differ structurally rather than in frequency, and consult tertiary stakeholders on requirements and "
         "quality thresholds - they set constraints even though they never touch the interface."),
        ("Your team is split between two navigation designs. Describe how you would choose, using this lecture's criteria.",
         "First check <b>technical feasibility</b> - can both be built within the project's constraints? Then build "
         "<b>prototypes rather than documents</b>, because interaction design focuses on externally visible and "
         "measurable behaviour and only a prototype behaves; paper prototypes are quick, cheap and effective at "
         "this stage. <b>Evaluate with users or peers</b> against the specific usability and UX goals agreed at the "
         "start, since those goals supply the criteria. If the product is live and the change is small, run an "
         "<b>A/B test</b>, remembering that setting appropriate metrics and choosing the user group sets is "
         "nontrivial. Finally check the result against the <b>quality thresholds</b> of each stakeholder group, "
         "which differ - what satisfies a casual user may fail an expert or a purchaser."),
    ],
    "branches": [
        ("Interaction design as a process",
         "A process focused on discovering requirements, designing to fulfil them, producing prototypes and evaluating them, focused on users and their goals.",
         ["It involves trade-offs to balance conflicting requirements.",
          "Generating alternatives and choosing between them is key.",
          "Four approaches exist: user-centered design, activity-centered design, systems design and genius design.",
          "Understanding the problem space asks what the current user experience is, why a change is needed and how it will improve the situation.",
          "Articulating the problem space is a team effort that explores different perspectives.",
          "It exists to avoid incorrect assumptions and unsupported claims."],
         [("Genius design", "Driven by the designer's own judgement rather than evidence, which is why the course teaches user-centered design instead."),
          ("Trade-offs", "A safety confirmation improves safe-to-use and damages efficient-to-use, so requirements must be balanced rather than all maximised.")]),
        ("Degrees of user involvement",
         "Different arrangements for involving users, each trading input quality against how representative the user remains.",
         ["A full-time team member gives constant input but loses touch with users.",
          "A part-time member gives patchy input and finds the role very stressful.",
          "A short-term member gives input that is inconsistent across the project's life.",
          "A long-term member gives consistent input but loses touch with users.",
          "Face-to-face group or individual activities are an alternative to membership.",
          "Online contributions from thousands of users come through Online Feedback Exchange systems, crowdsourcing of design ideas, and citizen science.",
          "User involvement continues after product release."],
         [("The representativeness problem", "Full-time and long-term involvement share the same failure: the longer someone sits with the design team, the less they resemble the users they represent."),
          ("Crowdsourcing", "Design ideas gathered from thousands of contributors online, rather than a handful of embedded representatives.")]),
        ("User-centered approach",
         "An approach resting on three principles that together make design evidence-driven rather than intuition-driven.",
         ["Early focus on users and tasks means directly studying cognitive, behavioural, anthropomorphic and attitudinal characteristics.",
          "Empirical measurement means users' reactions and performance to scenarios, manuals, simulations and prototypes are observed, recorded and analysed.",
          "Iterative design means fixing problems found in user testing and carrying out more tests."],
         [("Why iteration is a principle", "Because the first two principles keep producing findings, and a process with no loop has nowhere to put them.")]),
        ("Four basic activities of interaction design",
         "Discovering requirements, designing alternatives, prototyping, and evaluating the product and its user experience throughout.",
         ["Establishing requirements means knowing your target users and what support the product could usefully provide, understood through data gathering and analysis.",
          "Designing alternatives is the core activity of suggesting ideas for meeting requirements.",
          "Conceptual design produces the conceptual model and outlines what people can do with the product.",
          "Physical design covers colours, sounds, images, menu design and icon design.",
          "Prototyping lets users evaluate a design by interacting with it.",
          "Paper-based prototypes are quick, cheap and very effective at identifying problems early.",
          "Role-playing gives users a real sense of what interacting with the product will be like.",
          "Evaluating determines the usability and acceptability of the product and whether it is fit-for-purpose.",
          "Three characteristics permeate all four: early focus on users, documented and agreed usability and UX goals, and inevitable iteration."],
         [("Google Design Sprints", "Knapp et al. (2016) offer an alternative, time-boxed lifecycle model over the same underlying activities."),
          ("Research in the Wild", "Rogers and Marshall (2017) provide a framework for studying technology in natural settings rather than in the lab.")]),
        ("Users and stakeholders",
         "Identifying who the product is for, which is far less obvious than it appears.",
         ["Sha Zhao et al. (2016) identified 382 distinct types of user for smartphone apps.",
          "Many products target large sections of the population, so the user is everybody.",
          "More targeted products are associated with specific roles.",
          "Stakeholders form a larger group than direct users, and identifying them shows which groups to include in design activities.",
          "Stakeholders include direct users, their managers, recipients of output, purchasers, and users of competitors' products.",
          "Eason (1987) categorises users as primary (frequent hands-on), secondary (occasional or via someone else) and tertiary (affected by introduction or influencing purchase)."],
         [("The forgotten tertiary user", "The person who signs the purchase order never touches the interface but sets the constraints the design must satisfy.")]),
        ("What are needs",
         "Requirements cannot simply be requested, because users rarely know what is possible.",
         ["Explore the problem space before proposing solutions.",
          "Investigate who the users are.",
          "Investigate user activities to see what can be improved.",
          "Try out ideas with potential users.",
          "Focus on people's goals and on usability and user experience goals rather than expecting stakeholders to articulate requirements."],
         [("Goals versus features", "A user asking for a faster search box may actually need fewer results to sift, which only surfaces when the goal is investigated rather than the request taken literally.")]),
        ("Where alternatives come from",
         "Deliberate sources of alternative designs, needed because humans tend to stick with something that works.",
         ["Considering alternatives helps identify better designs.",
          "Flair and creativity through research and synthesis.",
          "Cross-fertilisation of ideas from different perspectives.",
          "Users can generate different designs themselves.",
          "Product evolution based on changing use.",
          "Seeking inspiration from similar products and domains, or from different products and domains.",
          "All alternatives must balance constraints and trade-offs."],
         [("Cross-domain inspiration", "Borrowing the card metaphor from physical index cards, or pull-to-refresh from a slot machine lever, are cases of looking outside the domain.")]),
        ("How to choose among alternatives",
         "Interaction design focuses on externally visible and measurable behaviour, which determines how choices are made.",
         ["Check technical feasibility first.",
          "Evaluate with users or with peers.",
          "Use prototypes rather than static documentation, because behaviour is key.",
          "A/B testing is an online method to inform the choice between alternatives.",
          "It is nontrivial to set appropriate metrics and choose user group sets for A/B testing.",
          "Different stakeholder groups have different quality thresholds.",
          "Usability and user experience goals lead to the relevant criteria."],
         [("A/B testing risk", "Choosing the wrong metric can make the worse design win - a change that raises clicks may raise confusion rather than value."),
          ("Threshold conflict", "A response time acceptable to a casual user may fall below an expert's threshold for the same screen.")]),
    ],
    "exam_mcq": [
        {"q": "Which list gives the four approaches to interaction design named in this lecture?",
         "options": ["User-centered, activity-centered, systems design, genius design",
                     "Waterfall, agile, spiral, incremental",
                     "Conceptual, physical, logical, deployment",
                     "Visceral, behavioural, reflective, emotional"],
         "correct": 0,
         "why": "Those four are the approaches stated. Waterfall, agile, spiral and incremental are software-process models; conceptual, physical, logical and deployment are view types; and visceral, behavioural and reflective are Norman's emotional design levels from Lecture 3."},
        {"q": "&quot;Users' reactions and performance to scenarios, manuals, simulations and prototypes are observed, recorded and analysed.&quot; Which UCD principle is this?",
         "options": ["Empirical measurement", "Early focus on users and tasks",
                     "Iterative design", "Triangulation"],
         "correct": 0,
         "why": "That is the definition of empirical measurement. Early focus is about directly studying users' "
                "characteristics; iterative design is about fixing and retesting; triangulation is a data-gathering "
                "issue from the requirements lecture."},
        {"q": "Which activity does conceptual design belong to?",
         "options": ["Designing alternatives", "Discovering requirements",
                     "Prototyping", "Evaluating"],
         "correct": 0,
         "why": "Designing alternatives breaks into conceptual design and physical design. Requirements precede it, "
                "and prototyping and evaluation follow."},
        {"q": "Which statement about paper prototypes matches the lecture?",
         "options": ["They are quick and cheap to build and very effective at identifying problems in early design",
                     "They are used only after a high-fidelity version has been tested",
                     "They cannot be used for role-playing",
                     "They give users an accurate sense of final response times"],
         "correct": 0,
         "why": "The lecture states that paper-based prototypes are very quick and cheap to build and very effective "
                "at identifying problems in the early stages of design, and that role-playing with them gives users "
                "a real sense of the interaction. They are early rather than late, and response time is a "
                "compromise low-fidelity prototypes cannot represent."},
        {"q": "A/B testing is described as which of the following?",
         "options": ["An online method to inform the choice between alternatives, where metrics and user groups are nontrivial to set",
                     "A laboratory technique requiring 5-10 participants",
                     "A form of heuristic inspection carried out by experts",
                     "A method for gathering requirements before design begins"],
         "correct": 0,
         "why": "That is the description given. The 5-10 participant figure belongs to usability testing; expert "
                "inspection is heuristic evaluation from Lecture 13; and A/B testing chooses between built "
                "alternatives rather than gathering requirements."},
        {"q": "Which of the following is NOT listed as a source of alternative designs?",
         "options": ["Copying the market leader's interface exactly",
                     "Cross-fertilisation of ideas from different perspectives",
                     "Product evolution based on changing use",
                     "Seeking inspiration from a different product domain"],
         "correct": 0,
         "why": "The listed sources are flair and creativity, cross-fertilisation, users generating designs, product "
                "evolution, and inspiration from similar or different products and domains. Copying a competitor "
                "outright is not among them, and it also risks the metaphor problem of transferring bad parts of an "
                "existing design."},
    ],
    "exam_short": [
        {"q": "State the three principles of a user-centered approach and explain what each requires in practice.",
         "keywords": ["early", "empirical", "iterativ", "user"],
         "answer": "Early focus on users and tasks: directly study users' cognitive, behavioural, anthropomorphic "
                   "and attitudinal characteristics from the start, rather than designing first and consulting "
                   "later. Empirical measurement: observe, record and analyse users' reactions and performance with "
                   "scenarios, manuals, simulations and prototypes, so claims about the design are backed by data. "
                   "Iterative design: when problems are found in user testing, fix them and carry out more tests, "
                   "because designers never get it right the first time."},
        {"q": "Describe the four basic activities of interaction design and the two sub-activities of the second one.",
         "keywords": ["requirement", "alternativ", "prototyp", "evaluat"],
         "answer": "Discovering requirements - know your target users and what support an interactive product could "
                   "usefully provide, understood through data gathering and analysis. Designing alternatives - the "
                   "core activity of suggesting ideas for meeting the requirements, split into (a) conceptual "
                   "design, producing the conceptual model that outlines what people can do with the product and "
                   "what concepts they need to understand the interaction, and (b) physical design, covering "
                   "colours, sounds, images, menu design and icon design. Prototyping - build something users can "
                   "interact with, since that is the only sensible way for them to evaluate a design. Evaluating - "
                   "determine the usability and acceptability of the product and whether it is fit-for-purpose."},
        {"q": "Explain Eason's three categories of user and why identifying stakeholders matters.",
         "keywords": ["primary", "secondary", "tertiary", "stakeholder"],
         "answer": "Primary users are frequent, hands-on users. Secondary users use the product occasionally, or via "
                   "someone else. Tertiary users are people affected by its introduction, or who will influence its "
                   "purchase. Identifying stakeholders matters because the stakeholder group is larger than the "
                   "group of direct users - it includes those who manage direct users, those who receive output, "
                   "those who make the purchasing decision, and those who use competitors' products - and "
                   "identifying them determines which groups should be included in interaction design activities. "
                   "Different stakeholder groups also hold different quality thresholds, which become criteria for "
                   "choosing between designs."},
        {"q": "Why can designers not simply ask stakeholders for requirements, and what should they do instead?",
         "keywords": ["possible", "goal", "problem space", "activit"],
         "answer": "Because users rarely know what is possible, so asking them to state requirements returns "
                   "variations on what already exists. Instead: explore the problem space; investigate who the users "
                   "are; investigate user activities to see what can be improved in how things are currently done; "
                   "and try out ideas with potential users. The focus should be on people's goals and on usability "
                   "and user experience goals, rather than expecting stakeholders to articulate requirements "
                   "directly."},
        {"q": "Compare the four degrees of user involvement as a member of the design team.",
         "keywords": ["full", "part", "short", "long"],
         "answer": "Full time gives constant input, but the representative loses touch with the users they "
                   "represent. Part time keeps them closer to the user community but produces patchy input and is "
                   "very stressful for the individual. Short term brings a fresh perspective but is inconsistent "
                   "across the project's life. Long term gives consistent input but, like full time, means losing "
                   "touch with users. Beyond team membership there are face-to-face group or individual activities, "
                   "online contributions from thousands of users through OFE systems, crowdsourcing and citizen "
                   "science, and user involvement after product release."},
        {"q": "How should a team choose among alternative designs? Name four considerations.",
         "keywords": ["feasib", "prototyp", "A/B", "threshold"],
         "answer": "Interaction design focuses on externally visible and measurable behaviour, so the choice is made "
                   "by observing behaviour rather than reading specifications. First, technical feasibility - can it "
                   "be built at all within the constraints? Second, evaluation with users or with peers, using "
                   "prototypes rather than static documentation, because behaviour is key and a document cannot "
                   "behave. Third, A/B testing, an online method for informing the choice between alternatives, "
                   "noting that setting appropriate metrics and choosing the user group sets is nontrivial. Fourth, "
                   "quality thresholds: different stakeholder groups hold different thresholds, and the usability "
                   "and user experience goals agreed at the start supply the relevant criteria."},
    ],
})


LECTURES.append({
    "num": 6,
    "slug": "establishing-requirements",
    "title": "Establishing Requirements",
    "short": "Establishing Requirements",
    "lecture_label": "Lectures 6 & 7",
    "theme": "field",
    "accent": "#e8a33d",
    "accent2": "#4fb0c6",
    "tagline": "Data gathering techniques, kinds of requirements, personas, scenarios, use cases, HTA, and data analysis.",
    "hero_title": "Requirements definition is<br><em>where failure occurs most commonly.</em>",
    "hero_sub": ("Two lectures in one deck. It covers the five key issues of data gathering, the six techniques, the "
                 "kinds of requirements, the artifacts used to express them - personas, scenarios, use cases, HTA - "
                 "and the qualitative and quantitative analysis that turns data into requirements."),
    "badges": ["5 key issues", "Interviews & questionnaires", "Observation & ethnography",
               "Kinds of requirements", "Personas & scenarios", "HTA", "Grounded theory"],
    "outcomes": [
        "Explain and describe the process of data gathering.",
        "Plan and run a successful data gathering programme.",
        "Distinguish the different kinds of requirements.",
        "Use scenarios, use cases and essential use cases to articulate work practices.",
        "Apply hierarchical task analysis and simple qualitative and quantitative analysis.",
    ],
    "sections": [
        {
            "id": "why",
            "kicker": "01 - WHAT, HOW AND WHY",
            "title": "Getting requirements right is crucial",
            "lead": ("Requirements work has two aims: understand as much as possible about <b>users, task and "
                     "context</b>, and produce a <b>stable set of requirements</b>."),
            "blocks": [
                ("steps", [
                    ("Data gathering activities", "Collect evidence from users, documents and existing products."),
                    ("Data analysis activities", "Interpret, categorise and structure what was collected."),
                    ("Expression as 'requirements'", "Turn findings into statements that can be checked."),
                    ("All of this is iterative", "None of the three happens once."),
                ]),
                ("warn", ("WHY IT MATTERS",
                          "<b>Requirements definition is the stage where failure occurs most commonly.</b> That "
                          "single sentence is the justification for the whole deck, and it is worth quoting.")),
                ("p", "&quot;<b>Establish</b>&quot; is used deliberately rather than &quot;collect&quot;: "
                      "requirements need clarification, refinement, completion and re-scoping. The input is a "
                      "requirements document (maybe); the output is <b>stable requirements</b>. Requirements arise "
                      "from understanding users' needs, and can be justified and related back to the data."),
            ],
        },
        {
            "id": "five-issues",
            "kicker": "02 - DATA GATHERING",
            "title": "The five key issues",
            "lead": "Every data-gathering exercise, whichever technique is used, must settle these five things first.",
            "blocks": [
                ("table", (["Issue", "What it means"], [
                    ["1. <b>Setting goals</b>", "Decide how you will analyze the data once it is collected - before you collect it."],
                    ["2. <b>Identifying participants</b>", "Decide who to gather data from."],
                    ["3. <b>Relationship with participants</b>", "Keep it clear and professional; obtain informed consent when appropriate."],
                    ["4. <b>Triangulation</b>", "Look at the data from more than one perspective."],
                    ["5. <b>Pilot studies</b>", "Run a small trial of the main study first."],
                ])),
                ("hook", ("MEMORY HOOK",
                          "<b>G-P-R-T-P</b>: <b>G</b>oals, <b>P</b>articipants, <b>R</b>elationship, "
                          "<b>T</b>riangulation, <b>P</b>ilot. Read it as <i>&quot;Good Planning Really Takes "
                          "Practice&quot;</i>. Notice the first and last are both about doing work <b>before</b> the "
                          "real study.")),
            ],
        },
        {
            "id": "techniques",
            "kicker": "03 - THE SIX TECHNIQUES",
            "title": "Interviews, questionnaires, similar products, observation, ethnography, documentation",
            "lead": "Each technique has a stated strength and a stated weakness. The exam pairs them.",
            "blocks": [
                ("cards", [
                    ("1. Interviews",
                     "Props such as sample scenarios of use and prototypes can be used. <b>Good for exploring "
                     "issues</b>, but <b>time consuming</b> and it may be infeasible to visit everyone. "
                     "<b>Focus groups</b> are group interviews - good at gaining a consensus view and/or "
                     "highlighting areas of conflict, but can be <b>dominated by individuals</b>."),
                    ("2. Questionnaires",
                     "Often used in conjunction with other techniques. Can give quantitative or qualitative data. "
                     "<b>Good for answering specific questions from a large, dispersed group.</b> Closed questions "
                     "are easier to analyze and can be processed by computer. Distributed by paper, email or web. "
                     "<b>Sampling is a problem when the population size is unknown</b>, as is common online."),
                    ("3. Researching similar products",
                     "<b>Good for prompting requirements</b> - a cheap way to surface what a domain normally provides."),
                    ("4. Observation",
                     "The action or process of observing something in order to gain information. "
                     "<b>Direct:</b> gains insights into stakeholders' tasks and is good for understanding the "
                     "nature and context of tasks, but requires time and commitment from a design team member and "
                     "produces a huge amount of data; includes <b>think-aloud</b> techniques. "
                     "<b>Indirect:</b> not often used in the requirements activity, but good for logging current "
                     "tasks - diaries, interaction logs and web analytics."),
                    ("5. Ethnography",
                     "A <b>philosophy with a set of techniques</b> including participant observation and interviews. "
                     "Ethnographers immerse themselves in the culture they study, and their degree of participation "
                     "varies along a scale from 'outside' to 'inside'."),
                    ("6. Studying documentation",
                     "Procedures and rules are often written down in manuals. Good for understanding the steps in an "
                     "activity, legislation and background information. <b>Not to be used in isolation.</b> Its "
                     "unique advantage: <b>no stakeholder time</b>, which is the limiting factor on every other "
                     "technique."),
                ]),
                ("table", (["Interview structure", "Character"], [
                    ["<b>Unstructured / open-ended</b>", "Not directed by a script. Rich but <b>not replicable</b>."],
                    ["<b>Structured</b>", "Tightly scripted, often like a questionnaire. Replicable but <b>may lack richness</b>."],
                    ["<b>Semi-structured</b>", "Guided by a script, but interesting issues can be explored in depth. A good <b>balance</b> between richness and replicability."],
                    ["<b>Group interview</b>", "A small group guided by a facilitator."],
                ])),
                ("steps", [
                    ("Introduction", "Introduce yourself, explain the goals, reassure about ethical issues, ask to record, present the informed consent form."),
                    ("Warm-up", "Make the first questions easy and non-threatening."),
                    ("Main body", "Present questions in a logical order."),
                    ("Cool-off period", "A few easy questions to defuse tension at the end."),
                    ("Closure", "Thank the interviewee and signal the end - switch the recorder off."),
                ]),
                ("warn", ("WHAT TO AVOID IN QUESTIONS",
                          "Long questions. Compound sentences - split them into two. Jargon and language the "
                          "interviewee may not understand. <b>Leading questions that make assumptions</b> - "
                          "&quot;why do you like...?&quot;. Unconscious biases such as gender stereotypes.")),
                ("p", "<b>Questionnaire design:</b> the impact of a question can be influenced by question order; "
                      "you may need different versions for different populations; give clear completion "
                      "instructions; strike a balance between white space and compactness; and decide whether "
                      "phrases will be all positive, all negative or mixed. Response formats include yes/no "
                      "checkboxes, multi-option checkboxes, rating scales (Likert, semantic - 3, 5, 7 or more "
                      "points) and open-ended responses."),
                ("table", (["Encouraging a good response", "Online questionnaires: advantages", "Online: problems"], [
                    ["Make the purpose of the study clear; promise anonymity.", "Responses received quickly.", "Sampling is problematic if population size is unknown."],
                    ["Ensure it is well designed; offer a short version.", "No copying or postage costs.", "Preventing individuals from responding more than once."],
                    ["Include a stamped addressed envelope if mailed; follow up; provide an incentive.", "Data collected straight into a database, reducing analysis time; errors easily corrected.", "Individuals have been known to change questions in email questionnaires."],
                ])),
                ("note", ("RESPONSE RATES",
                          "<b>40% is high; 20% is often acceptable.</b> A concrete number the exam can ask for.")),
            ],
        },
        {
            "id": "observation-frameworks",
            "kicker": "04 - STRUCTURING OBSERVATION",
            "title": "Frameworks, ethnography and contextual inquiry",
            "lead": "Observation without a framework produces notes; with one it produces data.",
            "blocks": [
                ("cards", [
                    ("The simple framework",
                     "<b>The person - who? The place - where? The thing - what?</b>"),
                    ("Goetz and LeCompte (1984)",
                     "Who is present? What is their role? What is happening? When does the activity occur? Where is "
                     "it happening? Why is it happening? How is the activity organized?"),
                ]),
                ("list", [
                    "<b>Web analytics</b> is a system of tools and techniques for optimizing web usage by "
                    "<b>measuring, collecting, analyzing and reporting</b> web data - typically focused on the "
                    "number of visitors and page views.",
                    "Ethnography requires the <b>co-operation</b> of the people being observed; <b>informants</b> are "
                    "useful; data analysis is <b>continuous</b>; it is an <b>interpretivist</b> technique; questions "
                    "get refined as understanding grows; and reports usually contain examples.",
                    "<b>Online ethnography</b> (virtual, online, netnography) covers online and offline activity. "
                    "Online interaction differs from face-to-face, virtual worlds have a <b>persistence</b> that "
                    "physical worlds do not, and ethical considerations and presentation issues are different.",
                ]),
                ("table", (["Contextual inquiry: four principles", "What it means"], [
                    ["<b>Context</b>", "See the workplace and what happens there."],
                    ["<b>Partnership</b>", "User and developer collaborate."],
                    ["<b>Interpretation</b>", "Observations are interpreted by user and developer <b>together</b>."],
                    ["<b>Focus</b>", "A project focus determines what to look for."],
                ])),
                ("note", ("THE CONTEXTUAL INQUIRY FRAME",
                          "It is an approach to ethnographic study in which the <b>user is the expert and the "
                          "designer is the apprentice</b>. It is a form of interview, but held at the user's own "
                          "workplace or workstation, and lasting two to three hours.")),
                ("hook", ("MEMORY HOOK",
                          "Contextual inquiry = <b>C-P-I-F</b>: <b>C</b>ontext, <b>P</b>artnership, "
                          "<b>I</b>nterpretation, <b>F</b>ocus. And the one-line frame that generates all four: "
                          "<i>the user is the master craftsman, you are the apprentice</i>.")),
            ],
        },
        {
            "id": "problems",
            "kicker": "05 - PROBLEMS AND GUIDELINES",
            "title": "What goes wrong, and how to plan around it",
            "lead": "The lecture lists the practical failures of data gathering before giving the guidelines.",
            "blocks": [
                ("list", [
                    "<b>Identifying and involving stakeholders</b> - users, managers, developers, customer reps, "
                    "union reps, shareholders - through workshops, interviews, workplace studies, or co-opting them "
                    "onto the development team.",
                    "Getting <b>'real' users, not managers</b> - traditionally a problem in software engineering, "
                    "though better now.",
                    "<b>Requirements management</b> - version control and ownership.",
                    "<b>Communication between parties</b> - within the development team, with the customer or user, "
                    "and between users, since different parts of an organisation use different terminology.",
                    "<b>Domain knowledge distributed and implicit</b> - difficult to dig up and understand. The "
                    "knowledge-articulation problem: <i>how do you walk?</i>",
                    "<b>Availability of key people.</b>",
                    "<b>Political problems</b> within the organisation, and <b>dominance of certain stakeholders</b>.",
                    "<b>Economic and business environment changes.</b>",
                    "<b>Balancing functional and usability demands.</b>",
                ]),
                ("table", (["Data gathering guidelines", "Data recording options"], [
                    ["Focus on identifying the stakeholders' needs.",
                     "<b>Notes + still camera</b> - less intrusive than a keyboard and flexible, but tiring; hard to write and listen and observe at once; concentration lapses; biases creep in; handwriting is hard to read; writing speed is limited. Solution: a partner or second observer."],
                    ["Involve all the stakeholder groups, and more than one representative from each.",
                     "<b>Audio + photographs</b> - less intrusive than video; in observation it lets observers focus on the activity rather than the words; in interviews it lets the interviewer attend to the interviewee. Transcribing is time consuming, though not all sections may be needed."],
                    ["Use a combination of data gathering techniques; support with props such as prototypes and task descriptions; run a pilot session; and consider carefully how to record the data.",
                     "<b>Video</b> - captures both audio and video, but raises where to fix the camera or whether to rove, where to point it, and the impact of recording on participants' behaviour."],
                ])),
                ("warn", ("THE COMPROMISE SENTENCE",
                          "&quot;You will need to compromise on the data you collect and the analysis to be done, "
                          "<b>but before you can make sensible compromises, you need to know what you'd really "
                          "like</b>.&quot; Plan the ideal study, then cut it - not the reverse.")),
            ],
        },
        {
            "id": "kinds",
            "kicker": "06 - KINDS OF REQUIREMENTS",
            "title": "Functional, data, environment, users",
            "lead": "Different kinds of requirement matter for interaction design, and each has its own sub-structure.",
            "blocks": [
                ("cards", [
                    ("Functional",
                     "What the system should do. Historically the main focus of requirements activities. "
                     "(Non-functional requirements cover memory size, response time and similar.)"),
                    ("Data",
                     "What kinds of data need to be stored, and how they will be stored - for example in a database."),
                    ("Environment / context of use",
                     "<b>Physical:</b> dusty, noisy, vibration, light, heat, humidity - an outdoor kiosk or an ATM. "
                     "<b>Social:</b> sharing of files, displays, paper; across great distances; working individually; "
                     "privacy for clients. <b>Organisational:</b> hierarchy, the IT department's attitude and remit, "
                     "user support, communications structure and infrastructure, availability of training."),
                    ("Users",
                     "Characteristics - ability, background, attitude to computers. System use - novice, expert, "
                     "casual, frequent. <b>Novice:</b> step-by-step prompted interaction, constrained, clear "
                     "information. <b>Expert:</b> flexibility, access and power. <b>Frequent:</b> short cuts. "
                     "<b>Casual/infrequent:</b> clear instructions, e.g. menu paths."),
                ]),
                ("p", "<b>Users' capabilities</b> vary in many dimensions, and each dimension is a design constraint: "
                      "<b>size of hands</b> affects the size and positioning of input buttons; <b>motor abilities</b> "
                      "affect the suitability of input and output devices; <b>height</b> matters when designing a "
                      "physical kiosk; <b>strength</b> matters - a child's toy needs little strength to operate but "
                      "greater strength to change the batteries; and <b>disabilities</b> of sight, hearing and "
                      "dexterity change everything."),
                ("note", ("THE THREE-SYSTEM ACTIVITY",
                          "The slides ask which environmental, user and usability factors would affect: a "
                          "<b>self-service petrol filling and payment system</b> (physical: weather, gloves, fumes; "
                          "users: everybody; usability: safety and learnability); an <b>on-board ship data analysis "
                          "system for geologists</b> (physical: vibration, motion; users: domain experts; usability: "
                          "efficiency and utility); and a <b>fashion clothes website</b> (environment: anywhere, any "
                          "device; users: casual; UX goals dominate).")),
            ],
        },
        {
            "id": "artifacts",
            "kicker": "07 - EXPRESSING REQUIREMENTS",
            "title": "Personas, scenarios, use cases and task analysis",
            "lead": "Four artifacts, each answering a different question about the work being supported.",
            "blocks": [
                ("cards", [
                    ("Personas",
                     "Capture user characteristics. They are <b>not real people</b>, but are synthesised from real "
                     "user characteristics. They should <b>not be idealised</b>. Bring them to life with a name, "
                     "characteristics, goals and personal background, and develop <b>multiple</b> personas."),
                    ("Scenarios",
                     "An <b>informal narrative story</b> - simple, 'natural', personal, and <b>not generalisable</b>. "
                     "The Thomson family sailing-holiday scenario is the slides' worked example: four family members "
                     "of different ages gather round a travel organizer, the system suggests a flotilla, the "
                     "children object, descriptions from other children persuade them, and Will asks for the details "
                     "to be printed because it is getting late."),
                    ("Use cases",
                     "<b>Assume interaction with a system</b> and assume a detailed understanding of the "
                     "interaction. Written as a numbered sequence of system and user steps, plus <b>alternative "
                     "courses</b> for the failure paths - if the country name is invalid, display an error and "
                     "return to step 3; if no visa information is found, display a message and return to step 1."),
                    ("Essential use cases",
                     "<b>Abstract away from the details</b> and do <b>not</b> carry the same assumptions as use cases."),
                ]),
                ("p", "<b>Task analysis</b> completes the set. Task descriptions are often used to <b>envision new</b> "
                      "systems or devices; task analysis is used mainly to <b>investigate an existing</b> situation. "
                      "It is important not to focus on superficial activities: ask what people are trying to "
                      "achieve, <b>why</b> they are trying to achieve it, and <b>how</b> they are going about it. "
                      "The most popular technique is <b>Hierarchical Task Analysis (HTA)</b>."),
                ("list", [
                    "HTA breaks a task into subtasks, then sub-sub-tasks, grouped as <b>plans</b> specifying how the "
                    "tasks might be performed in practice.",
                    "It focuses on <b>physical and observable actions</b>, and includes actions <b>not</b> related to "
                    "software or an interaction device.",
                    "Start with a user goal, examine it, and identify the main tasks for achieving it; then subdivide "
                    "the tasks into subtasks.",
                ]),
                ("note", ("THE HTA WORKED EXAMPLE - LEARN THIS ONE",
                          "<b>0. In order to buy a DVD</b> &rarr; 1. locate DVD &rarr; 2. add DVD to shopping basket "
                          "&rarr; 3. enter payment details &rarr; 4. complete address &rarr; 5. confirm order. "
                          "<b>plan 0: If regular user do 1-2-5. If new user do 1-2-3-4-5.</b> The plan is the part "
                          "students forget, and it is the part that carries the analysis.")),
                ("hook", ("MEMORY HOOK",
                          "<b>Persona = who. Scenario = a story about them. Use case = the exact steps. "
                          "Essential use case = the steps with the details stripped out. HTA = the goal broken down, "
                          "plus a plan.</b>")),
            ],
        },
        {
            "id": "analysis",
            "kicker": "08 - DATA INTERPRETATION AND ANALYSIS",
            "title": "Quantitative, qualitative, and three theoretical frameworks",
            "lead": ("Analysis starts <b>soon after</b> the data gathering session, with initial interpretation "
                     "before deeper analysis. Different approaches emphasize different elements - class diagrams for "
                     "object-oriented systems, entity-relationship diagrams for data-intensive systems."),
            "blocks": [
                ("table", (["", "Quantitative", "Qualitative"], [
                    ["Data", "Expressed as numbers.", "Difficult to measure sensibly as numbers - counting words to measure dissatisfaction is the lecture's warning example."],
                    ["Analysis", "Numerical methods to ascertain size, magnitude and amount.", "Expresses the nature of elements, represented as themes, patterns and stories."],
                    ["Simple techniques", "Averages - <b>mean</b> (add and divide), <b>median</b> (middle value when ranked), <b>mode</b> (most frequent). Percentages. Graphical representations.", "Recurring patterns or themes; categorizing data with an emergent or pre-specified scheme; looking for <b>critical incidents</b> to focus on key events."],
                ])),
                ("warn", ("THE THREE AVERAGES",
                          "Mean, median and mode are <b>different kinds of average and can give very different "
                          "answers for the same data</b>. And the standing warning: be careful how you manipulate "
                          "data and numbers.")),
                ("cards", [
                    ("Grounded theory",
                     "Aims to derive theory from systematic analysis of data, based on a categorization approach "
                     "called <b>coding</b>, in three levels: <b>open</b> - identify categories; <b>axial</b> - flesh "
                     "out and link to subcategories; <b>selective</b> - form a theoretical scheme. Researchers are "
                     "encouraged to draw on their own theoretical backgrounds to inform analysis."),
                    ("Distributed cognition",
                     "Used as an analytic framework - the same framework introduced in Lecture 2."),
                    ("Activity theory",
                     "Explains human behaviour in terms of our practical activity in the world. Provides a framework "
                     "focusing analysis around the concept of an <b>activity</b> and helps identify <b>tensions</b> "
                     "between the different elements of the system. Two key models: one outlining what constitutes "
                     "an activity, and one modelling the <b>mediating role of artifacts</b>."),
                ]),
                ("list", [
                    "Tools: spreadsheets (simple, basic graphs); statistical packages such as SPSS; qualitative data "
                    "analysis tools for categorization and theme-based analysis such as N6; and the CAQDAS "
                    "Networking Project at the University of Surrey.",
                    "<b>Presenting the findings:</b> only make claims your data can support. The best presentation "
                    "depends on the audience, the purpose, and the gathering and analysis undertaken. Techniques "
                    "include rigorous notations such as UML, using stories to create scenarios, and summarizing the "
                    "findings.",
                ]),
                ("note", ("THE CLOSING RULE",
                          "<b>Presentation of the findings should not overstate the evidence.</b> The data analysis "
                          "that can be done depends on the data gathering that was done - you cannot analyse your "
                          "way out of a badly designed study.")),
            ],
        },
    ],
    "mistakes": [
        ("Confusing structured and unstructured interviews.",
         "Unstructured is not script-directed - rich but <b>not replicable</b>. Structured is tightly scripted - "
         "<b>replicable but may lack richness</b>. Semi-structured balances the two and is usually the right answer "
         "when a question asks which to choose."),
        ("Listing only some of the five key data-gathering issues.",
         "All five: setting goals, identifying participants, relationship with participants, triangulation, and "
         "pilot studies. Triangulation - looking at data from more than one perspective - is the one most often "
         "dropped."),
        ("&quot;Ethnography is just observation.&quot;",
         "It is a <b>philosophy with a set of techniques</b> including participant observation and interviews. "
         "Ethnographers immerse themselves in the culture, participation varies from outside to inside, analysis is "
         "continuous, and it is interpretivist."),
        ("Treating a persona as a real user or an ideal user.",
         "Personas are not real people; they are <b>synthesised from real user characteristics</b> and should "
         "<b>not be idealised</b>. Develop multiple personas."),
        ("Writing an HTA without a plan.",
         "The plan is what specifies how the tasks might be performed in practice - <i>if regular user do 1-2-5, if "
         "new user do 1-2-3-4-5</i>. Without it you have a list, not an analysis."),
        ("Assuming mean, median and mode are interchangeable.",
         "They are different kinds of average and can give very different answers for the same set of data."),
        ("Ignoring the environment requirement.",
         "Environment splits three ways: physical (dust, noise, vibration, light, heat, humidity), social (sharing, "
         "distance, privacy) and organisational (hierarchy, IT attitude, support, training availability)."),
    ],
    "cheat": (["Concept", "Shortest correct answer"], [
        ["Two aims of requirements", "Understand users, task and context; produce a stable set of requirements."],
        ["Five key issues", "Setting goals, identifying participants, relationship with participants, triangulation, pilot studies."],
        ["Interview types", "Unstructured (rich, not replicable), structured (replicable, may lack richness), semi-structured (balanced), group."],
        ["Interview stages", "Introduction, warm-up, main body, cool-off, closure."],
        ["Response rate", "40% is high; 20% is often acceptable."],
        ["Observation types", "Direct (think-aloud) and indirect (diaries, interaction logs, web analytics)."],
        ["Web analytics", "Measuring, collecting, analyzing and reporting web data to optimize web usage."],
        ["Goetz &amp; LeCompte", "Who is present, what is their role, what is happening, when, where, why, how is it organized."],
        ["Contextual inquiry", "Ethnographic interview at the user's workplace, 2-3 hours; context, partnership, interpretation, focus; user is expert, designer is apprentice."],
        ["Kinds of requirements", "Functional, non-functional, data, environment (physical/social/organisational), users."],
        ["Persona", "Not a real person; synthesised from real user characteristics; not idealised; multiple personas."],
        ["Scenario", "Informal narrative story - simple, natural, personal, not generalisable."],
        ["Use case", "Assumes interaction with a system and detailed understanding; numbered steps plus alternative courses."],
        ["Essential use case", "Abstracts away from the details and drops the use case's assumptions."],
        ["HTA", "Break a task into subtasks grouped as plans; focuses on physical and observable actions."],
        ["Averages", "Mean (add and divide), median (middle when ranked), mode (most frequent)."],
        ["Grounded theory coding", "Open (identify categories), axial (flesh out and link subcategories), selective (form theoretical scheme)."],
        ["Activity theory", "Explains behaviour through practical activity; identifies tensions; models the mediating role of artifacts."],
    ]),
    "quiz": [
        {"q": "You need rich detail but also want to compare answers across twenty participants. Which interview type fits?",
         "options": ["Semi-structured", "Unstructured", "Structured", "Focus group"], "correct": 0,
         "why": "Semi-structured interviews are guided by a script so answers are comparable, while allowing "
                "interesting issues to be explored in more depth - a good balance between richness and "
                "replicability. Unstructured is rich but not replicable, structured is replicable but may lack "
                "richness, and a focus group risks domination by individuals."},
        {"q": "Which technique is the only one that consumes no stakeholder time?",
         "options": ["Studying documentation", "Direct observation",
                     "Focus groups", "Contextual inquiry"], "correct": 0,
         "why": "The lecture explicitly notes that studying documentation requires no stakeholder time, which is the "
                "limiting factor on the other techniques. Observation requires design-team and participant time, and "
                "focus groups and contextual inquiry both require participants directly."},
        {"q": "In an HTA of buying a DVD, what does &quot;plan 0: if regular user do 1-2-5, if new user do 1-2-3-4-5&quot; represent?",
         "options": ["The plan specifying how the subtasks are performed in practice",
                     "The alternative course of a use case",
                     "A persona's goals",
                     "The selective coding stage of grounded theory"], "correct": 0,
         "why": "Plans specify how the tasks might be performed in practice and are grouped with the subtasks in "
                "HTA. Alternative courses belong to use cases, personas capture user characteristics, and selective "
                "coding forms a theoretical scheme in grounded theory."},
        {"q": "Which is the correct description of TRIANGULATION as a data-gathering issue?",
         "options": ["Looking at the data from more than one perspective",
                     "Running a small trial of the main study",
                     "Recruiting three participants per stakeholder group",
                     "Using three recording media simultaneously"], "correct": 0,
         "why": "Triangulation means examining the data from more than one perspective. Running a small trial is the "
                "pilot study; the other two options invent numerical rules that the lecture does not state."},
        {"q": "A team is designing an on-board ship data analysis system for geologists. Which requirement category covers vibration and motion?",
         "options": ["Environment - physical", "Environment - organisational",
                     "Data", "Non-functional"], "correct": 0,
         "why": "Physical environment covers dust, noise, vibration, light, heat and humidity. Organisational "
                "environment covers hierarchy, IT attitude, support and training; data requirements cover what is "
                "stored and how; non-functional covers memory size and response time."},
        {"q": "Which sequence gives the three levels of coding in grounded theory?",
         "options": ["Open, axial, selective", "Selective, axial, open",
                     "Open, selective, thematic", "Descriptive, analytic, theoretical"], "correct": 0,
         "why": "Open coding identifies categories, axial coding fleshes them out and links to subcategories, and "
                "selective coding forms a theoretical scheme. The other orders and labels are not the lecture's."},
    ],
    "lab": [
        ("You have two weeks and no budget to establish requirements for a hospital shift-handover tool. Design the programme, justifying each technique.",
         "Settle the <b>five key issues</b> first: state the goals and how the data will be analysed, identify "
         "participants across all stakeholder groups, agree a clear professional relationship with informed consent, "
         "plan to <b>triangulate</b>, and run a <b>pilot</b>. Start with <b>studying documentation</b> - handover "
         "protocols and regulations - because it consumes no stakeholder time and gives background before you spend "
         "the scarce clinical hours. Then <b>research similar products</b> to prompt requirements cheaply. Spend the "
         "clinical time on <b>direct observation</b> of two handovers, which is good for understanding the nature "
         "and context of the task, followed by <b>semi-structured interviews</b> with props - a paper prototype - "
         "since these balance richness and replicability. Add a short <b>questionnaire</b> with mostly closed "
         "questions to reach nurses on other shifts, remembering that 20% response is often acceptable. Record with "
         "<b>audio plus photographs</b> rather than video: it is less intrusive, and in observation it lets you "
         "focus on the activity rather than the words."),
        ("Write a persona, a scenario fragment and a use-case step for a pharmacy stock app, and say what each one adds that the others do not.",
         "<b>Persona:</b> Layla, 34, senior pharmacy technician, eight years' experience, comfortable with "
         "technology but works standing with one hand occupied; her goal is to never run out of a controlled "
         "medicine. Not real, not idealised, synthesised from observed characteristics. <b>Scenario:</b> "
         "&quot;Late on Thursday the ward calls for a drug Layla thinks is low. She has one hand on the shelf and "
         "the tablet on the trolley; she wants to know the stock level and whether an order is already in transit "
         "before she promises anything.&quot; Informal, personal, not generalisable. <b>Use case step:</b> "
         "&quot;3. The system prompts the user for the medicine name. 4. The user enters the name. 5. The system "
         "checks the name is valid. <i>Alternative: 5a. If the name is invalid the system displays an error and "
         "returns to step 3.</i>&quot; Each adds something different: the persona fixes <b>who</b> and their "
         "capabilities, the scenario fixes <b>context and motivation</b> in a form stakeholders can argue with, and "
         "the use case fixes the <b>exact interaction sequence including failure paths</b> - which the scenario "
         "deliberately does not."),
        ("A colleague reports &quot;the average task time was 4 minutes&quot; from ten trials, eight of which took about 2 minutes and two of which took 15. Critique this, then say what analysis you would present.",
         "The mean is being used where it misrepresents the data: mean, median and mode are different kinds of "
         "average and can give very different answers for the same set, and the lecture warns explicitly to be "
         "careful how data and numbers are manipulated. Here the mean of about 4 minutes describes nobody - the "
         "<b>median</b> is about 2 minutes and the <b>mode</b> sits near it, while the two 15-minute trials are "
         "<b>critical incidents</b> that deserve qualitative attention rather than being averaged away. I would "
         "present the median with the full distribution as a graphical representation, report the two outliers "
         "separately as critical incidents with the qualitative account of what went wrong in each, and state only "
         "claims the data can support - ten trials cannot support a general performance claim, and presentation "
         "should not overstate the evidence."),
    ],
    "branches": [
        ("The importance of requirements",
         "Understanding as much as possible about users, task and context, and producing a stable set of requirements.",
         ["Requirements definition is the stage where failure occurs most commonly.",
          "The work is done through data gathering activities, data analysis activities and expression as requirements.",
          "All of this is iterative.",
          "Requirements need clarification, refinement, completion and re-scoping, which is why the word is establish rather than collect.",
          "The input may be a requirements document and the output is stable requirements.",
          "Requirements arise from understanding users' needs and can be justified and related back to data."],
         [("Why establish", "A stated requirement is a starting point to be tested against evidence, not a fact to be transcribed.")]),
        ("Five key issues of data gathering",
         "Decisions that must be settled before any technique is applied.",
         ["Setting goals means deciding how to analyze the data once it is collected.",
          "Identifying participants means deciding who to gather data from.",
          "The relationship with participants must be clear and professional, with informed consent where appropriate.",
          "Triangulation means looking at data from more than one perspective.",
          "Pilot studies are a small trial of the main study."],
         [("Pilot value", "A pilot exposes ambiguous questions and broken recording setups while they are still cheap to fix.")]),
        ("Interviews and focus groups",
         "Techniques good for exploring issues, using props such as sample scenarios of use and prototypes.",
         ["Interviews are good for exploring issues but are time consuming and it may be infeasible to visit everyone.",
          "Unstructured interviews are not directed by a script - rich but not replicable.",
          "Structured interviews are tightly scripted, often like a questionnaire - replicable but may lack richness.",
          "Semi-structured interviews are guided by a script while allowing depth, balancing richness and replicability.",
          "Group interviews are small groups guided by a facilitator.",
          "Closed questions have a predetermined answer format and are easier to analyze; open questions do not.",
          "Avoid long questions, compound sentences, jargon, leading questions that make assumptions, and unconscious biases.",
          "Run the interview as introduction, warm-up, main body, cool-off period and closure.",
          "Focus groups are good at gaining a consensus view or highlighting conflict, but can be dominated by individuals."],
         [("Closed question", "\"How often do you visit this web site: every day, once a week?\" - standardized, short and identically worded for all participants."),
          ("Open question", "\"Which music websites do you visit most frequently?\" followed by \"Why?\" and \"Tell me more.\"")]),
        ("Questionnaires",
         "Often used with other techniques, giving quantitative or qualitative data from a large, dispersed group.",
         ["Good for answering specific questions from a large, dispersed group of people.",
          "Closed questions are easier to analyze and may be processed by computer.",
          "Distributed by paper, email or the web.",
          "Sampling is a problem when the population size is unknown, as is common online.",
          "Question order can influence a question's impact, and different populations may need different versions.",
          "Provide clear instructions and balance white space against compactness.",
          "Decide whether phrases will be all positive, all negative or mixed.",
          "Response formats include yes/no checkboxes, multi-option checkboxes, Likert and semantic rating scales with 3, 5, 7 or more points, and open-ended responses.",
          "Encourage responses by making the purpose clear, promising anonymity, designing well, offering a short version, including a stamped addressed envelope, following up and providing an incentive.",
          "A 40% response rate is high and 20% is often acceptable."],
         [("Online advantages", "Fast responses, no copying or postage costs, data collected straight into a database, reduced analysis time and easily corrected errors."),
          ("Online problems", "Unknown population size makes sampling hard, individuals may respond more than once, and people have been known to change questions in email questionnaires.")]),
        ("Observation and web analytics",
         "The action or process of observing something in order to gain information, either directly or indirectly.",
         ["Direct observation gains insights into stakeholders' tasks and is good for understanding their nature and context.",
          "Direct observation requires time and commitment from a design team member and produces a huge amount of data.",
          "Think-aloud techniques are used in direct observation.",
          "Indirect observation is not often used in the requirements activity but is good for logging current tasks.",
          "Indirect methods include diaries, interaction logs and web analytics.",
          "Web analytics measures, collects, analyzes and reports web data to optimize web usage, typically focusing on visitors and page views.",
          "Video, audio, photos and notes capture data in both types of observation.",
          "A simple framework asks about the person, the place and the thing.",
          "Goetz and LeCompte (1984) ask who is present, what their role is, what is happening, when, where, why, and how the activity is organized."],
         [("Recording trade-off", "Notes plus a still camera are unintrusive but tiring and biased; audio plus photographs let the observer attend to the activity; video captures everything but changes participants' behaviour.")]),
        ("Ethnography and contextual inquiry",
         "A philosophy with a set of techniques, including participant observation and interviews, in which researchers immerse themselves in the culture they study.",
         ["A researcher's degree of participation varies along a scale from outside to inside.",
          "Analyzing video and data logs can be time consuming.",
          "Collections of comments, incidents and artifacts are made.",
          "Co-operation of the people being observed is required, and informants are useful.",
          "Data analysis is continuous and the technique is interpretivist.",
          "Questions get refined as understanding grows, and reports usually contain examples.",
          "Online ethnography covers online and offline activity, and virtual worlds have a persistence physical worlds do not.",
          "Contextual inquiry treats the user as expert and the designer as apprentice, in a two-to-three-hour interview at the user's workplace.",
          "Its four principles are context, partnership, interpretation and focus."],
         [("Persistence online", "A chat room's history remains inspectable long after the conversation, which changes both the method and its ethics."),
          ("Interpretation principle", "Observations are interpreted by user and developer together, so the analyst's reading is checked against the practitioner's.")]),
        ("Problems and guidelines for data gathering",
         "Practical obstacles to gathering requirements, and the guidelines that plan around them.",
         ["Identifying and involving stakeholders spans users, managers, developers, customer reps, union reps and shareholders.",
          "Getting real users rather than managers has traditionally been a problem in software engineering.",
          "Requirements management raises version control and ownership.",
          "Communication problems occur within the team, with the customer, and between users who use different terminology.",
          "Domain knowledge is distributed and implicit and hard to articulate - the knowledge articulation problem asks how you walk.",
          "Availability of key people, political problems, dominance of certain stakeholders and business changes all interfere.",
          "Functional and usability demands must be balanced.",
          "Guidelines: focus on stakeholders' needs, involve all stakeholder groups and more than one representative from each, and combine techniques.",
          "Support the process with props such as prototypes and task descriptions, run a pilot session, and consider carefully how to record data.",
          "Compromise on data and analysis is inevitable, but you must first know what you would really like."],
         [("Knowledge articulation", "Asking an expert how they walk shows why implicit domain knowledge cannot simply be requested in an interview.")]),
        ("Different kinds of requirements",
         "Functional, data, environmental and user requirements, each significant for interaction design.",
         ["Functional requirements state what the system should do and were historically the main focus.",
          "Non-functional requirements cover memory size, response time and similar qualities.",
          "Data requirements ask what kinds of data need to be stored and how.",
          "Physical environment covers dust, noise, vibration, light, heat and humidity.",
          "Social environment covers sharing of files and displays, distance, individual work and privacy for clients.",
          "Organisational environment covers hierarchy, the IT department's attitude and remit, user support, communications infrastructure and availability of training.",
          "User requirements cover characteristics such as ability, background and attitude to computers.",
          "System use splits users into novice, expert, casual and frequent, each needing different support.",
          "Users' capabilities vary in hand size, motor ability, height, strength and disability."],
         [("Novice versus expert support", "Novices need step-by-step prompted, constrained interaction with clear information; experts need flexibility, access and power; frequent users need short cuts; casual users need clear instructions such as menu paths."),
          ("Strength requirement", "A child's toy needs little strength to operate but greater strength to change the batteries, so the same product has two strength requirements for two user groups.")]),
        ("Personas, scenarios and use cases",
         "Artifacts for capturing user characteristics and articulating existing and envisioned work practices.",
         ["Personas capture user characteristics and are synthesised from real users rather than being real people.",
          "Personas should not be idealised, should be brought to life with a name, characteristics, goals and background, and should be developed in multiples.",
          "Scenarios are informal narrative stories - simple, natural, personal and not generalisable.",
          "Use cases assume interaction with a system and a detailed understanding of that interaction.",
          "Use cases are written as numbered steps with alternative courses for failure paths.",
          "Essential use cases abstract away from the details and do not carry the same assumptions as use cases."],
         [("The Thomson family scenario", "A family of four explores a sailing holiday with a travel organizer, rejects and then accepts a flotilla after seeing other children's descriptions, and asks for details to be printed."),
          ("Alternative courses", "If the country name is invalid the system displays an error and returns to step 3; if no visa information is found it displays a message and returns to step 1.")]),
        ("Task analysis and HTA",
         "Investigating an existing situation by breaking a goal down into tasks, subtasks and plans.",
         ["Task descriptions are often used to envision new systems; task analysis mainly investigates existing situations.",
          "It is important not to focus on superficial activities but to ask what people are trying to achieve, why, and how.",
          "Hierarchical Task Analysis is the most popular technique.",
          "HTA breaks a task into subtasks and sub-sub-tasks, grouped as plans that specify how tasks are performed in practice.",
          "HTA focuses on physical and observable actions and includes actions not related to software or an interaction device.",
          "Start with a user goal, examine it, identify the main tasks for achieving it, then subdivide."],
         [("Buying a DVD", "0. In order to buy a DVD: 1 locate DVD, 2 add to basket, 3 enter payment details, 4 complete address, 5 confirm order - plan 0: regular users do 1-2-5, new users do 1-2-3-4-5.")]),
        ("Data interpretation and analysis",
         "Turning gathered data into findings, using quantitative and qualitative methods and theoretical frameworks.",
         ["Analysis starts soon after the gathering session, with initial interpretation before deeper analysis.",
          "Different approaches emphasize different elements, such as class diagrams for object-oriented systems and entity-relationship diagrams for data-intensive systems.",
          "Quantitative data is expressed as numbers; qualitative data is difficult to measure sensibly as numbers.",
          "Quantitative analysis uses numerical methods to ascertain size, magnitude and amount.",
          "Qualitative analysis expresses the nature of elements as themes, patterns and stories.",
          "Mean, median and mode are different kinds of average and can give very different answers for the same data.",
          "Qualitative techniques include finding recurring patterns or themes, categorizing data with emergent or pre-specified schemes, and looking for critical incidents.",
          "Grounded theory derives theory from systematic analysis using open, axial and selective coding.",
          "Activity theory explains behaviour through practical activity, identifies tensions between system elements, and models the mediating role of artifacts.",
          "Tools include spreadsheets, statistical packages such as SPSS, qualitative tools such as N6, and the CAQDAS Networking Project.",
          "Only make claims the data can support, and do not overstate the evidence."],
         [("Log visualization", "Interaction profiles of players in an online game and logs of web page activity are graphical representations that give an overview of quantitative data."),
          ("Critical incidents", "Focusing on the few key events where something went badly wrong often yields more design value than the average of all the trials.")]),
    ],
    "exam_mcq": [
        {"q": "Which is the stated reason the lecture gives for why requirements work matters so much?",
         "options": ["Requirements definition is the stage where failure occurs most commonly",
                     "Requirements are the cheapest artifact to produce",
                     "Requirements are legally binding on the development team",
                     "Requirements replace the need for evaluation"],
         "correct": 0,
         "why": "The slides state that requirements definition is where failure occurs most commonly and that getting "
                "requirements right is crucial. The other options are not claims the lecture makes - and evaluation "
                "runs throughout the process regardless."},
        {"q": "Which technique is described as good for gaining a consensus view and highlighting areas of conflict, but risks domination by individuals?",
         "options": ["Focus groups", "Structured interviews",
                     "Online questionnaires", "Contextual inquiry"],
         "correct": 0,
         "why": "That is exactly the description of focus groups - group interviews. Structured interviews are "
                "one-to-one and scripted, questionnaires reach dispersed individuals, and contextual inquiry is a "
                "one-to-one workplace interview."},
        {"q": "In contextual inquiry, what is the relationship between user and designer?",
         "options": ["The user is the expert and the designer is the apprentice",
                     "The designer is the expert and the user is the subject",
                     "Both are peers with equal domain knowledge",
                     "A facilitator mediates between them"],
         "correct": 0,
         "why": "Contextual inquiry frames the user as expert and the designer as apprentice, held at the user's own "
                "workplace for two to three hours. Facilitation belongs to group interviews, and reversing the "
                "expertise inverts the whole approach."},
        {"q": "Which requirement type covers &quot;the IT department's attitude and remit, user support, and availability of training&quot;?",
         "options": ["Organisational environment", "Social environment",
                     "Physical environment", "Data"],
         "correct": 0,
         "why": "Organisational environment covers hierarchy, the IT department's attitude and remit, user support, "
                "communications structure and infrastructure, and availability of training. Social environment "
                "covers sharing and privacy; physical covers dust, noise and vibration; data covers what is stored."},
        {"q": "What distinguishes an ESSENTIAL use case from an ordinary use case?",
         "options": ["It abstracts away from the details and does not carry the same assumptions",
                     "It includes the alternative courses that ordinary use cases omit",
                     "It is written as an informal narrative story",
                     "It is derived from a persona rather than from observation"],
         "correct": 0,
         "why": "Essential use cases abstract away from the details and do not share the ordinary use case's "
                "assumptions about interaction with a system. Alternative courses belong to ordinary use cases, "
                "informal narrative describes a scenario, and neither form is defined by its source."},
        {"q": "Which statement about the three averages is correct?",
         "options": ["They are different kinds of average and can give very different answers for the same data",
                     "The mean is always the most representative for usability data",
                     "The mode is the middle value when the data is ranked",
                     "The median is the value that appears most often"],
         "correct": 0,
         "why": "The lecture stresses that mean, median and mode are different kinds of average that can produce very "
                "different answers. The median is the middle value when ranked and the mode is the most frequent value, so the two options that call the mode the middle value and the median the most frequent value have swapped those definitions."},
    ],
    "exam_short": [
        {"q": "List the five key issues in data gathering and explain why each must be settled in advance.",
         "keywords": ["goal", "participant", "triangulat", "pilot"],
         "answer": "Setting goals - decide how you will analyze the data once collected, because the analysis method "
                   "determines what must be collected. Identifying participants - decide who to gather data from, "
                   "since the sample bounds what can be claimed. Relationship with participants - keep it clear and "
                   "professional and obtain informed consent where appropriate, which is both ethical and practical. "
                   "Triangulation - plan to look at the data from more than one perspective, because a single "
                   "technique carries a single bias. Pilot studies - run a small trial of the main study, so "
                   "ambiguous questions and broken recording setups are found while they are still cheap to fix."},
        {"q": "Compare unstructured, structured and semi-structured interviews, and say when you would use each.",
         "keywords": ["unstructured", "structured", "semi", "replicab"],
         "answer": "Unstructured interviews are not directed by a script; they produce rich data but are not "
                   "replicable, so they suit early exploration when you do not yet know what to ask. Structured "
                   "interviews are tightly scripted, often like a questionnaire; they are replicable but may lack "
                   "richness, so they suit comparing many participants on known questions. Semi-structured "
                   "interviews are guided by a script while allowing interesting issues to be explored in more "
                   "depth, giving a good balance between richness and replicability, which is why they are the usual "
                   "choice for requirements work. Group interviews add a facilitator and a small group, and are good "
                   "for consensus and conflict but can be dominated by individuals."},
        {"q": "Explain hierarchical task analysis using the DVD example, and say what a plan adds.",
         "keywords": ["subtask", "plan", "goal", "observable"],
         "answer": "HTA involves breaking a task down into subtasks, then sub-sub-tasks, starting from a user goal "
                   "whose main achieving tasks are identified and then subdivided. It focuses on physical and "
                   "observable actions, including actions not related to software or an interaction device. The "
                   "example: 0. In order to buy a DVD - 1. locate DVD, 2. add DVD to shopping basket, 3. enter "
                   "payment details, 4. complete address, 5. confirm order. The <b>plan</b> specifies how the "
                   "subtasks are actually performed: plan 0 says if a regular user, do 1-2-5; if a new user, do "
                   "1-2-3-4-5. Without the plan the analysis is only a list of steps; the plan is what captures "
                   "conditional real-world practice."},
        {"q": "What is a persona, what is a scenario, and how do they differ from a use case?",
         "keywords": ["persona", "scenario", "use case", "narrat"],
         "answer": "A persona captures user characteristics. It is not a real person but is synthesised from real "
                   "user characteristics, should not be idealised, and is brought to life with a name, "
                   "characteristics, goals and personal background; multiple personas are developed. A scenario is "
                   "an informal narrative story - simple, natural, personal and not generalisable - describing a "
                   "situation of use. A use case differs from both: it assumes interaction with a system and a "
                   "detailed understanding of that interaction, and is written as a numbered sequence of system and "
                   "user steps with alternative courses for failure paths. Essential use cases abstract away from "
                   "those details and drop the assumptions."},
        {"q": "Describe direct and indirect observation and give the advantages and disadvantages of each.",
         "keywords": ["direct", "indirect", "think aloud", "log"],
         "answer": "Direct observation means watching the activity as it happens, including think-aloud techniques. "
                   "It gains insights into stakeholders' tasks and is good for understanding the nature and context "
                   "of the tasks, but it requires time and commitment from a member of the design team and can "
                   "result in a huge amount of data. Indirect observation tracks users' activities without watching "
                   "them - diaries, interaction logs and web analytics. It is not often used in the requirements "
                   "activity but is good for logging current tasks and scales to many users, though it records what "
                   "happened without explaining why. Video, audio, photos and notes are used to capture data in "
                   "both types."},
        {"q": "Explain the difference between quantitative and qualitative data and analysis, and name a theoretical framework for qualitative analysis.",
         "keywords": ["quantitativ", "qualitativ", "theme", "grounded"],
         "answer": "Quantitative data is expressed as numbers, and quantitative analysis uses numerical methods to "
                   "ascertain size, magnitude and amount - averages, percentages and graphical representations. "
                   "Qualitative data is difficult to measure sensibly as numbers, and qualitative analysis expresses "
                   "the nature of elements, represented as themes, patterns and stories - identifying recurring "
                   "themes, categorizing data with an emergent or pre-specified scheme, and looking for critical "
                   "incidents. Three theoretical frameworks support qualitative analysis: grounded theory, which "
                   "derives theory from systematic analysis using open, axial and selective coding; distributed "
                   "cognition; and activity theory, which explains behaviour in terms of practical activity, focuses "
                   "analysis around an activity, and identifies tensions between elements of the system while "
                   "modelling the mediating role of artifacts."},
    ],
})


LECTURES.append({
    "num": 8,
    "slug": "design-principles-and-guidelines",
    "title": "Design Principles and Guidelines",
    "short": "Principles & Guidelines",
    "lecture_label": "Lecture 8",
    "theme": "rule",
    "accent": "#9b7bff",
    "accent2": "#3ad29f",
    "tagline": "Principles vs guidelines vs standards, Dix's usability principles, and the three famous rule sets.",
    "hero_title": "Abstract and general,<br><em>or specific and authoritative.</em>",
    "hero_sub": ("Design rules are rules a designer follows to increase the usability of a system. They differ along "
                 "two axes - <b>level of abstraction/generality</b> and <b>level of authority</b> - and this lecture "
                 "places principles, guidelines and standards on those axes before giving you the three rule sets "
                 "everyone quotes."),
    "badges": ["Principles vs guidelines vs standards", "Learnability", "Flexibility",
               "Robustness", "Nielsen's 10", "Shneiderman's 8", "Norman's 7"],
    "outcomes": [
        "Distinguish principles, guidelines and standards by abstraction and authority.",
        "Describe Dix et al.'s three usability principles and their sub-principles.",
        "State Nielsen's 10 usability heuristics.",
        "State Shneiderman's 8 golden rules.",
        "State Norman's 7 principles and apply them to increase usability.",
    ],
    "sections": [
        {
            "id": "rules",
            "kicker": "01 - INTRODUCTION",
            "title": "Three kinds of design rule",
            "lead": ("Design rules (or usability rules) are rules a designer can follow in order to increase the "
                     "usability of the system or product. They differ on <b>level of abstraction/generality</b> and "
                     "<b>level of authority</b>."),
            "blocks": [
                ("table", (["Rule type", "Abstraction / generality", "Authority", "Example"], [
                    ["<b>Principles</b>", "Abstract, high generality. Widely applicable and enduring.", "Low authority.",
                     "&quot;The interface should be easy to navigate.&quot; - Dix et al.'s usability principles."],
                    ["<b>Guidelines</b>", "Narrowly focused. Can be too specific, incomplete and hard to apply.",
                     "More general and lower authority than standards.",
                     "&quot;Use colour to highlight links.&quot; - Smith and Mosier's <i>Guidelines for User Interface "
                     "Software</i> (MITRE Corporation, 1986)."],
                    ["<b>Standards</b>", "Very specific.", "High authority. Set by national or international bodies.",
                     "&quot;Use colour RGB #1010D0 on home links.&quot; - ISO 9241 <i>Ergonomic Requirements for "
                     "Office Work with Visual Display Terminals</i>; British Standards Institution; ISO."],
                ])),
                ("list", [
                    "Guidelines can <b>guide or advise on how to achieve a principle</b> - they sit between the two.",
                    "Design rules should be used <b>early in the lifecycle</b>, during design - though they can also "
                    "be used to <b>evaluate</b> the usability of a system.",
                    "<b>Heuristics</b> or <b>golden rules</b> provide a succinct summary of the essential "
                    "characteristics of good design: Nielsen's heuristics, Shneiderman's golden rules and Norman's "
                    "principles.",
                ]),
                ("hook", ("MEMORY HOOK",
                          "As you go <b>principle &rarr; guideline &rarr; standard</b>, generality falls and "
                          "authority rises. A principle applies everywhere and forces nothing; a standard applies "
                          "narrowly and forces everything.")),
            ],
        },
        {
            "id": "learnability",
            "kicker": "02 - DIX: PRINCIPLE 1",
            "title": "Learnability - and its five sub-principles",
            "lead": ("<b>Learnability:</b> the ease with which new users can begin effective interaction and achieve "
                     "maximal performance."),
            "blocks": [
                ("cards", [
                    ("Predictability",
                     "Support for the user to determine the effect of <b>future</b> action based on past interaction "
                     "history. <i>Can I tell what will happen based on what I have gone through in the past?</i>"),
                    ("Synthesizability",
                     "Support for the user to assess the effect of <b>past</b> operations on the <b>current</b> "
                     "state. <i>Can I tell why I am here based on what I have gone through in the past?</i>"),
                    ("Familiarity",
                     "The extent to which a user's knowledge and experience in <b>other real-world or "
                     "computer-based domains</b> can be applied when interacting with a new system."),
                    ("Generalizability",
                     "Support for the user to extend knowledge of specific interaction <b>within and across "
                     "applications</b> to other similar situations."),
                    ("Consistency",
                     "Likeness in <b>input-output behaviour</b> arising from similar situations or similar task "
                     "objectives - size, layout, colour, language and so on."),
                ]),
                ("warn", ("PREDICTABILITY vs SYNTHESIZABILITY - THE MOST CONFUSED PAIR IN THE COURSE",
                          "Both look at past interaction history. <b>Predictability looks forward</b> - what will "
                          "happen next. <b>Synthesizability looks backward</b> - why am I here now. The lecture "
                          "gives you the two questions verbatim; memorise them as a pair, not separately.")),
                ("hook", ("MEMORY HOOK",
                          "Learnability = <b>P-S-F-G-C</b>: <b>P</b>redictability, <b>S</b>ynthesizability, "
                          "<b>F</b>amiliarity, <b>G</b>eneralizability, <b>C</b>onsistency. "
                          "<i>&quot;Please Say Familiar Generic Commands&quot;</i>.")),
            ],
        },
        {
            "id": "flexibility",
            "kicker": "03 - DIX: PRINCIPLE 2",
            "title": "Flexibility - and its five sub-principles",
            "lead": "<b>Flexibility:</b> the multiplicity of ways the user and system exchange information.",
            "blocks": [
                ("cards", [
                    ("Dialogue initiative",
                     "User freedom from artificial constraints on the input dialog imposed by the system. "
                     "<i>Who has the initiative in the dialog - the user or the system?</i>"),
                    ("Multithreading",
                     "The ability of the system to support user interaction for <b>more than one task at a time</b>."),
                    ("Task migratability",
                     "The ability to <b>transfer control</b> for the execution of tasks between the system and the "
                     "user - spell-checking is the lecture's example, since it can be done by the user, by the "
                     "system, or by both."),
                    ("Substitutivity",
                     "The extent to which an application allows <b>equivalent input and output values to be "
                     "substituted</b> for each other: input values such as fractions or decimals; output values "
                     "such as digital and analog; and output that can be reused as input."),
                    ("Customizability",
                     "The ability of the <b>user or the system</b> to modify the user interface. "
                     "<b>Adaptability</b> is user-initiated modification; <b>adaptivity</b> is system-initiated "
                     "modification."),
                ]),
                ("hook", ("MEMORY HOOK",
                          "Flexibility = <b>D-M-T-S-C</b>: <b>D</b>ialogue initiative, <b>M</b>ultithreading, "
                          "<b>T</b>ask migratability, <b>S</b>ubstitutivity, <b>C</b>ustomizability. And for the "
                          "last one: <b>adaptABILITY = user does it; adaptIVITY = system does it.</b> "
                          "The word with -ability is the one the person has.")),
            ],
        },
        {
            "id": "robustness",
            "kicker": "04 - DIX: PRINCIPLE 3",
            "title": "Robustness - and its four sub-principles",
            "lead": ("<b>Robustness:</b> the level of support provided to the user in determining successful "
                     "achievement and assessment of goal-directed behaviour."),
            "blocks": [
                ("cards", [
                    ("Observability",
                     "The extent to which the user can evaluate the <b>internal state</b> of the system from the "
                     "representation on the user interface."),
                    ("Recoverability",
                     "The extent to which the user can reach the intended goal <b>after recognizing an error</b> in "
                     "the previous interaction."),
                    ("Responsiveness",
                     "A measure of the <b>rate of communication</b> between the user and the system."),
                    ("Task conformance",
                     "The extent to which the system services support <b>all the tasks</b> the user would wish to "
                     "perform, <b>and in the way</b> the user would wish to perform them."),
                ]),
                ("note", ("HOW ROBUSTNESS CONNECTS TO EARLIER LECTURES",
                          "<b>Observability</b> is the gulf of evaluation solved. <b>Recoverability</b> is "
                          "Shneiderman's &quot;permit easy reversal of actions&quot; and Nielsen's &quot;user "
                          "control and freedom&quot;. <b>Task conformance</b> is the usability goal <i>good "
                          "utility</i> restated - does the right functionality exist at all, and in the right shape?")),
                ("hook", ("MEMORY HOOK",
                          "Robustness = <b>O-R-R-T</b>: <b>O</b>bservability, <b>R</b>ecoverability, "
                          "<b>R</b>esponsiveness, <b>T</b>ask conformance. Two Rs in the middle: one is about "
                          "<i>errors</i>, the other about <i>speed</i>.")),
            ],
        },
        {
            "id": "nielsen",
            "kicker": "05 - RULE SET 1",
            "title": "Jakob Nielsen's 10 usability heuristics",
            "lead": ("The most quoted list in HCI. Each heuristic below carries the lecture's own wording, because "
                     "that is what the exam marks against."),
            "blocks": [
                ("table", (["#", "Heuristic", "What it requires"], [
                    ["1", "<b>Visibility of system status</b>", "Always keep users informed about what is going on, through appropriate feedback within reasonable time."],
                    ["2", "<b>Match between system and the real world</b>", "Speak the users' language with familiar words, phrases and concepts rather than system-oriented terms; follow real-world conventions so information appears in a natural and logical order."],
                    ["3", "<b>User control and freedom</b>", "Users often choose functions by mistake and need a clearly marked <b>emergency exit</b> to leave the unwanted state without an extended dialogue. Support undo and redo."],
                    ["4", "<b>Consistency and standards</b>", "Users should not have to wonder whether different words, situations or actions mean the same thing. Follow platform conventions."],
                    ["5", "<b>Error prevention</b>", "Even better than good error messages is a careful design which prevents a problem from occurring in the first place."],
                    ["6", "<b>Recognition rather than recall</b>", "Make objects, actions and options visible. The user should not have to remember information from one part of the dialogue to another; instructions should be visible or easily retrievable."],
                    ["7", "<b>Flexibility and efficiency of use</b>", "Accelerators - unseen by the novice - speed up interaction for the expert, so the system caters to both. Allow users to tailor frequent actions."],
                    ["8", "<b>Aesthetic and minimalist design</b>", "Dialogues should not contain irrelevant or rarely needed information. Every extra unit competes with the relevant units and diminishes their relative visibility."],
                    ["9", "<b>Help users recognize, diagnose and recover from errors</b>", "Error messages in plain language, no codes, precisely indicating the problem and constructively suggesting a solution."],
                    ["10", "<b>Help and documentation</b>", "Better if the system can be used without documentation, but where provided it should be easy to search, focused on the user's task, list concrete steps, and not be too large."],
                ])),
                ("hook", ("MEMORY HOOK",
                          "Group the ten into four themes and the list becomes four items: "
                          "<b>Tell me</b> (1 status, 9 errors, 10 help), <b>Speak my language</b> (2 real world, "
                          "4 consistency), <b>Let me out</b> (3 control, 5 prevention), "
                          "<b>Don't make me work</b> (6 recognition, 7 flexibility, 8 minimalism).")),
            ],
        },
        {
            "id": "shneiderman",
            "kicker": "06 - RULE SET 2",
            "title": "Ben Shneiderman's 8 golden rules",
            "lead": "Eight rules, several of which deliberately overlap Nielsen - which is itself an exam point.",
            "blocks": [
                ("table", (["#", "Golden rule", "What it requires"], [
                    ["1", "<b>Strive for consistency</b>", "In layout, terminology, command usage and so on."],
                    ["2", "<b>Cater for universal usability</b>", "Recognize the requirements of diverse users and technology - add features for novices such as explanations, and support experts with shortcuts."],
                    ["3", "<b>Offer informative feedback</b>", "For every user action, offer relevant feedback and information; keep the user appropriately informed."],
                    ["4", "<b>Design dialogs to yield closure</b>", "Help the user know when they have completed a task."],
                    ["5", "<b>Offer error prevention and simple error handling</b>", "Prevention plus clear and informative guidance to recovery - error management."],
                    ["6", "<b>Permit easy reversal of actions</b>", "To relieve anxiety and encourage exploration, because the user knows they can always go back to previous states."],
                    ["7", "<b>Support internal locus of control</b>", "Make the user feel that they are in control of the system, which responds to their instructions and commands."],
                    ["8", "<b>Reduce short-term memory load</b>", "Make menus and UI elements visible and easily available or retrievable."],
                ])),
                ("warn", ("THE OVERLAP QUESTION",
                          "Consistency, error prevention and memory load appear in <b>both</b> Nielsen and "
                          "Shneiderman. What is <b>unique to Shneiderman</b> is <b>design dialogs to yield "
                          "closure</b> and <b>support internal locus of control</b>. If a question asks which rule "
                          "set a statement comes from, look for those two first.")),
                ("hook", ("MEMORY HOOK",
                          "<b>C-U-F-C-E-R-L-M</b>: Consistency, Universal usability, Feedback, Closure, Error "
                          "handling, Reversal, Locus of control, Memory load. The two in the middle - "
                          "<b>Closure</b> and <b>Locus of control</b> - are the Shneiderman fingerprints.")),
            ],
        },
        {
            "id": "norman",
            "kicker": "07 - RULE SET 3",
            "title": "Donald Norman's 7 principles",
            "lead": "The shortest list, and the one that ties directly back to Lectures 1 and 2.",
            "blocks": [
                ("steps", [
                    ("1. Use both knowledge in the world and knowledge in the head",
                     "Do not force everything into memory, and do not force everything onto the screen."),
                    ("2. Simplify the structure of tasks", "Reduce what the user must plan and hold in mind."),
                    ("3. Make things visible: bridge the gulfs of execution and evaluation",
                     "Directly the Lecture 2 framework, restated as a design rule."),
                    ("4. Get the mappings right", "The connector-and-icon example from Lecture 1."),
                    ("5. Exploit the power of constraints, both natural and artificial",
                     "Physical shape and greyed-out options both prevent wrong actions."),
                    ("6. Design for error", "Assume errors will occur and make them recoverable."),
                    ("7. When all else fails, standardize", "If no natural mapping exists, impose a convention and keep it."),
                ]),
                ("note", ("THE CROSS-LECTURE LINK",
                          "Norman's principle 3 <b>is</b> the gulfs framework from Lecture 2, and principles 4 and 5 "
                          "<b>are</b> mapping and constraints from Lecture 1. This deck is deliberately a "
                          "consolidation, so questions can legitimately cross lecture boundaries.")),
                ("hook", ("MEMORY HOOK",
                          "Norman's seven end on a shrug - <i>&quot;when all else fails, standardize&quot;</i> - "
                          "which makes number 7 the easiest to recall and a useful anchor for counting backwards to "
                          "check you have all seven.")),
            ],
        },
    ],
    "mistakes": [
        ("Swapping predictability and synthesizability.",
         "Predictability = determine the effect of <b>future</b> action from past history (<i>what will happen?</i>). "
         "Synthesizability = assess the effect of <b>past</b> operations on the <b>current</b> state "
         "(<i>why am I here?</i>)."),
        ("Swapping adaptability and adaptivity.",
         "Both are forms of customizability. <b>Adaptability</b> is user-initiated modification; <b>adaptivity</b> "
         "is system-initiated."),
        ("Getting the abstraction/authority axes backwards.",
         "Principles are <b>abstract, general and low in authority</b>. Standards are <b>very specific and high in "
         "authority</b>. Guidelines sit between, narrowly focused but lower in authority than standards."),
        ("Attributing &quot;design dialogs to yield closure&quot; to Nielsen.",
         "Closure and internal locus of control are <b>Shneiderman's</b>. Nielsen's nearest equivalents are "
         "visibility of system status and user control and freedom."),
        ("Listing only Nielsen when asked for design rules.",
         "The lecture gives three sets: <b>Nielsen's 10 heuristics, Shneiderman's 8 golden rules, Norman's 7 "
         "principles</b> - plus Dix et al.'s three usability principles with their fourteen sub-principles."),
        ("Confusing task migratability with multithreading.",
         "Multithreading is supporting <b>more than one task at a time</b>. Task migratability is transferring "
         "<b>control of a task</b> between system and user."),
        ("Treating robustness as reliability.",
         "In Dix's sense robustness is the level of support for determining <b>successful achievement and assessment "
         "of goal-directed behaviour</b> - observability, recoverability, responsiveness and task conformance - not "
         "crash-resistance."),
    ],
    "cheat": (["Concept", "Shortest correct answer"], [
        ["Design rules", "Rules a designer follows to increase usability; differ by abstraction/generality and authority."],
        ["Principles", "Abstract, high generality, low authority, widely applicable and enduring."],
        ["Guidelines", "Narrowly focused advice on how to achieve a principle; lower authority than standards."],
        ["Standards", "Very specific and high in authority; set by bodies such as BSI and ISO (e.g. ISO 9241)."],
        ["Learnability", "Ease with which new users begin effective interaction and achieve maximal performance."],
        ["Learnability sub-principles", "Predictability, synthesizability, familiarity, generalizability, consistency."],
        ["Flexibility", "The multiplicity of ways the user and system exchange information."],
        ["Flexibility sub-principles", "Dialogue initiative, multithreading, task migratability, substitutivity, customizability."],
        ["Robustness", "Level of support in determining successful achievement and assessment of goal-directed behaviour."],
        ["Robustness sub-principles", "Observability, recoverability, responsiveness, task conformance."],
        ["Adaptability vs adaptivity", "User-initiated vs system-initiated interface modification."],
        ["Nielsen's 10", "Status, real-world match, control and freedom, consistency and standards, error prevention, recognition over recall, flexibility and efficiency, aesthetic and minimalist, help with errors, help and documentation."],
        ["Shneiderman's 8", "Consistency, universal usability, informative feedback, closure, error prevention and handling, easy reversal, internal locus of control, reduced short-term memory load."],
        ["Norman's 7", "Knowledge in world and head, simplify tasks, make things visible, get mappings right, exploit constraints, design for error, standardize."],
    ]),
    "quiz": [
        {"q": "&quot;Use colour RGB #1010D0 on home links&quot; is an example of which kind of design rule?",
         "options": ["A standard", "A guideline", "A principle", "A heuristic"], "correct": 0,
         "why": "It is very specific and would be set with high authority, which is the definition of a standard. A "
                "guideline would be the more general &quot;use colour to highlight links&quot;; a principle would be "
                "&quot;the interface should be easy to navigate&quot;; heuristics are the succinct summaries of good "
                "design such as Nielsen's."},
        {"q": "A user asks &quot;why am I on this screen - what did my last three actions do?&quot; Which sub-principle of learnability addresses this?",
         "options": ["Synthesizability", "Predictability", "Familiarity", "Generalizability"], "correct": 0,
         "why": "Synthesizability is support for the user to assess the effect of past operations on the current "
                "state. Predictability is the forward-looking twin - determining the effect of future action. "
                "Familiarity concerns knowledge from other domains, and generalizability concerns extending "
                "knowledge to similar situations."},
        {"q": "A word processor lets the user run the spell check themselves, or hand it to the system to run automatically. Which flexibility sub-principle is this?",
         "options": ["Task migratability", "Multithreading", "Substitutivity", "Dialogue initiative"], "correct": 0,
         "why": "Task migratability is the ability to transfer control for the execution of tasks between the system "
                "and the user, and spell checking is the lecture's own example. Multithreading is supporting more "
                "than one task at a time; substitutivity concerns equivalent input and output values; dialogue "
                "initiative concerns who leads the input dialog."},
        {"q": "Which pair of rules is unique to Shneiderman rather than shared with Nielsen?",
         "options": ["Design dialogs to yield closure; support internal locus of control",
                     "Strive for consistency; offer informative feedback",
                     "Error prevention; reduce short-term memory load",
                     "Permit easy reversal of actions; cater for universal usability"], "correct": 0,
         "why": "Closure and internal locus of control have no direct Nielsen counterpart. Consistency, feedback, "
                "error prevention, memory load and reversal all map onto Nielsen heuristics 4, 1, 5, 6 and 3 "
                "respectively, and universal usability maps closely onto flexibility and efficiency of use."},
        {"q": "A settings screen where the SYSTEM rearranges options based on what the user opens most is an example of:",
         "options": ["Adaptivity", "Adaptability", "Substitutivity", "Observability"], "correct": 0,
         "why": "Adaptivity is system-initiated modification of the interface; adaptability is user-initiated. Both "
                "are forms of customizability. Substitutivity concerns equivalent values, and observability concerns "
                "evaluating the system's internal state."},
        {"q": "Which of Norman's seven principles directly restates a framework from the cognitive aspects lecture?",
         "options": ["Make things visible: bridge the gulfs of execution and evaluation",
                     "When all else fails, standardize",
                     "Simplify the structure of tasks",
                     "Design for error"], "correct": 0,
         "why": "The gulfs of execution and evaluation are the framework introduced in Lecture 2, restated here as a "
                "design principle. The others are related to earlier material but do not name a cognitive framework "
                "directly."},
    ],
    "lab": [
        ("Evaluate an online banking transfer screen against four of Nielsen's heuristics, naming a concrete failure and fix for each.",
         "<b>1. Visibility of system status:</b> after pressing Transfer, the page hangs with no indicator; the user "
         "cannot tell whether money moved. Fix: a progress state and an explicit confirmation with a reference "
         "number, within a reasonable time. <b>3. User control and freedom:</b> once the beneficiary form opens, "
         "there is no way back without losing the entered data; the user needs a clearly marked emergency exit and "
         "undo. Fix: a Cancel that preserves the draft. <b>5. Error prevention:</b> the IBAN field accepts any "
         "string and fails only on submit. Fix: validate the checksum and the length as the field is completed, "
         "which the heuristic says is better than any error message. <b>9. Help users recognize, diagnose and "
         "recover from errors:</b> the message reads &quot;Transaction failed (code 51)&quot;. Fix: plain language, "
         "no codes, precise about the problem - &quot;Insufficient funds: this transfer needs 250 SAR more&quot; - "
         "and constructively suggesting a solution."),
        ("Take Dix's robustness and use its four sub-principles to specify requirements for a self-checkout machine.",
         "<b>Observability:</b> the user must be able to evaluate the machine's internal state from the interface - "
         "show the running basket, the weight-check status, and whether the machine is waiting for staff approval, "
         "rather than a generic &quot;please wait&quot;. <b>Recoverability:</b> after recognizing an error - the "
         "wrong item scanned - the user must still be able to reach the goal, so provide item removal without "
         "restarting the basket. <b>Responsiveness:</b> the rate of communication must match the user's pace - a "
         "scan must be acknowledged immediately with sound and display, since a slow response causes double "
         "scanning. <b>Task conformance:</b> the services must support all the tasks the user wishes to perform and "
         "in the way they wish - own bags, loose produce, vouchers and split payment - because a machine that "
         "handles only the simplest basket forces the user back to a staffed till."),
        ("A junior designer says &quot;we follow Nielsen, so we don't need standards.&quot; Respond using this lecture's framework.",
         "The two are not substitutes because they sit at different points on both axes. Nielsen's heuristics are "
         "<b>principles</b>: abstract, high in generality, widely applicable and enduring, but <b>low in "
         "authority</b> - they tell you that the system should speak the users' language, not which contrast ratio "
         "to hit. <b>Standards</b> such as ISO 9241 are very specific and high in authority, set by national and "
         "international bodies, and are what an organisation is actually held to. <b>Guidelines</b> bridge them, "
         "advising on how to achieve a principle while being narrowly focused, sometimes too specific, incomplete "
         "and hard to apply. In practice you need all three: principles to reason with during early design, "
         "guidelines to turn a principle into a decision, and standards where conformance must be demonstrable. "
         "Design rules should be used early in the lifecycle, though they can also be used to evaluate an existing "
         "system."),
    ],
    "branches": [
        ("Design rules: principles, guidelines and standards",
         "Rules a designer can follow to increase the usability of the system or product, differing by level of abstraction or generality and level of authority.",
         ["Principles are abstract with high generality and low authority, widely applicable and enduring.",
          "An example principle is that the interface should be easy to navigate; Dix et al. give a full set.",
          "Guidelines can guide or advise on how to achieve a principle.",
          "Guidelines are narrowly focused and can be too specific, incomplete and hard to apply.",
          "Guidelines are more general and lower in authority than standards.",
          "Standards are very specific and high in authority, set by national bodies such as the British Standards Institution or international bodies such as ISO.",
          "Design rules should be used early in the lifecycle during design, and can also be used to evaluate usability.",
          "Heuristics or golden rules provide a succinct summary of the essential characteristics of good design."],
         [("ISO 9241", "Ergonomic Requirements for Office Work with Visual Display Terminals - the standards example given."),
          ("Smith and Mosier", "Guidelines for User Interface Software, MITRE Corporation 1986 - the guidelines example given.")]),
        ("Learnability",
         "The ease with which new users can begin effective interaction and achieve maximal performance.",
         ["Predictability is support for the user to determine the effect of future action based on past interaction history.",
          "Synthesizability is support for the user to assess the effect of past operations on the current state.",
          "Familiarity is the extent to which knowledge and experience in other real-world or computer-based domains can be applied to a new system.",
          "Generalizability is support for extending knowledge of specific interaction within and across applications to other similar situations.",
          "Consistency is likeness in input-output behaviour arising from similar situations or task objectives, covering size, layout, colour and language."],
         [("Predictability question", "Can I tell what will happen based on what I have gone through in the past?"),
          ("Synthesizability question", "Can I tell why I am here based on what I have gone through in the past?")]),
        ("Flexibility",
         "The multiplicity of ways the user and system exchange information.",
         ["Dialogue initiative is user freedom from artificial constraints on the input dialog imposed by the system.",
          "Multithreading is the ability of the system to support user interaction for more than one task at a time.",
          "Task migratability is the ability to transfer control for execution of tasks between the system and the user.",
          "Substitutivity is the extent to which equivalent input and output values can be substituted for each other.",
          "Substitutivity covers input values such as fractions or decimals, output values such as digital and analog, and output that can be reused as input.",
          "Customizability is the ability of the user or the system to modify the user interface.",
          "Adaptability is user-initiated modification and adaptivity is system-initiated modification."],
         [("Spell checking", "The standing example of task migratability, since control of the task can sit with the user, the system, or move between them."),
          ("Who has the initiative", "A system asking a fixed sequence of questions holds the initiative; letting the user state a whole request in their own words gives it to them.")]),
        ("Robustness",
         "The level of support provided to the user in determining successful achievement and assessment of goal-directed behaviour.",
         ["Observability is the extent to which the user can evaluate the internal state of the system from the representation on the user interface.",
          "Recoverability is the extent to which the user can reach the intended goal after recognizing an error in the previous interaction.",
          "Responsiveness is a measure of the rate of communication between the user and the system.",
          "Task conformance is the extent to which system services support all the tasks the user would wish to perform, and in the way they would wish to perform them."],
         [("Observability in practice", "A progress state showing what the system is doing answers the gulf of evaluation directly."),
          ("Task conformance failure", "A checkout that cannot split a payment forces the user to abandon the task even though every screen works correctly.")]),
        ("Nielsen's 10 usability heuristics",
         "Ten heuristics providing a succinct summary of the essential characteristics of good interface design.",
         ["Visibility of system status: always keep users informed about what is going on through appropriate feedback within reasonable time.",
          "Match between system and the real world: speak the users' language with familiar words, phrases and concepts, following real-world conventions in a natural and logical order.",
          "User control and freedom: provide a clearly marked emergency exit from mistakenly chosen functions, and support undo and redo.",
          "Consistency and standards: users should not have to wonder whether different words, situations or actions mean the same thing; follow platform conventions.",
          "Error prevention: a careful design that prevents a problem occurring is better than a good error message.",
          "Recognition rather than recall: make objects, actions and options visible so users need not remember information across the dialogue.",
          "Flexibility and efficiency of use: accelerators unseen by novices speed up interaction for experts, and users should be able to tailor frequent actions.",
          "Aesthetic and minimalist design: every extra unit of information competes with the relevant units and diminishes their relative visibility.",
          "Help users recognize, diagnose and recover from errors: plain language, no codes, precise about the problem and constructively suggesting a solution.",
          "Help and documentation: easy to search, focused on the user's task, listing concrete steps, and not too large."],
         [("Emergency exit", "A clearly marked way out of an unwanted state without going through an extended dialogue - the phrase the heuristic actually uses."),
          ("Accelerators", "Keyboard shortcuts that novices never notice but that let experts work far faster, so one interface serves both.")]),
        ("Shneiderman's 8 golden rules",
         "Eight rules summarising good interaction design, several overlapping Nielsen's heuristics.",
         ["Strive for consistency in layout, terminology and command usage.",
          "Cater for universal usability by recognizing the requirements of diverse users and technology, adding explanations for novices and shortcuts for experts.",
          "Offer informative feedback for every user action, keeping the user appropriately informed.",
          "Design dialogs to yield closure, helping the user know when a task has been completed.",
          "Offer error prevention and simple error handling, with clear and informative guidance to recovery.",
          "Permit easy reversal of actions to relieve anxiety and encourage exploration.",
          "Support internal locus of control so the user feels in control of a system that responds to their commands.",
          "Reduce short-term memory load by making menus and interface elements visible and easily retrievable."],
         [("Closure", "A confirmation page ending a checkout tells the user the task is over, which is the rule's whole purpose."),
          ("Locus of control", "Auto-playing video or unrequested redirects break this rule because the system, not the user, is acting.")]),
        ("Norman's 7 principles",
         "Seven principles that consolidate the visibility, mapping and constraint material from earlier lectures into design rules.",
         ["Use both knowledge in the world and knowledge in the head.",
          "Simplify the structure of tasks.",
          "Make things visible: bridge the gulfs of execution and evaluation.",
          "Get the mappings right.",
          "Exploit the power of constraints, both natural and artificial.",
          "Design for error.",
          "When all else fails, standardize."],
         [("Knowledge in the world", "A labelled control needs no memorised command, while a shortcut key relies on knowledge in the head - good designs use both."),
          ("Natural and artificial constraints", "A key that fits a lock one way is a natural constraint; a greyed-out menu item is an artificial one.")]),
    ],
    "exam_mcq": [
        {"q": "Which statement correctly places principles, guidelines and standards?",
         "options": ["Principles are abstract and low in authority; standards are very specific and high in authority",
                     "Principles are specific and high in authority; standards are abstract and low in authority",
                     "Guidelines are higher in authority than standards",
                     "All three have equal authority but differ in length"],
         "correct": 0,
         "why": "Principles are abstract, widely applicable, enduring and low in authority. Standards are very "
                "specific and high in authority, set by bodies such as BSI and ISO. Guidelines sit between and are "
                "explicitly lower in authority than standards."},
        {"q": "Dix's FLEXIBILITY is defined as:",
         "options": ["The multiplicity of ways the user and system exchange information",
                     "The ease with which new users can begin effective interaction",
                     "The level of support in assessing goal-directed behaviour",
                     "The ability of the system to recover from crashes"],
         "correct": 0,
         "why": "That is the definition given. The second is learnability, the third is robustness, and crash "
                "recovery is not what Dix means by robustness."},
        {"q": "&quot;Even better than good error messages is a careful design which prevents a problem from occurring in the first place&quot; is which of Nielsen's heuristics?",
         "options": ["Error prevention", "Help users recognize, diagnose and recover from errors",
                     "User control and freedom", "Visibility of system status"],
         "correct": 0,
         "why": "That is the wording of heuristic 5, error prevention. Heuristic 9 concerns the message itself once "
                "an error has occurred; heuristic 3 concerns the emergency exit; heuristic 1 concerns keeping users "
                "informed."},
        {"q": "Which sub-principle covers an application that accepts a value as either a fraction or a decimal?",
         "options": ["Substitutivity", "Customizability", "Predictability", "Task conformance"],
         "correct": 0,
         "why": "Substitutivity is the extent to which equivalent input and output values can be substituted for "
                "each other, and fractions versus decimals is the lecture's own input example. Customizability is "
                "modifying the interface, predictability concerns anticipating future effects, and task conformance "
                "concerns whether all desired tasks are supported."},
        {"q": "&quot;Support internal locus of control&quot; means:",
         "options": ["Make the user feel they are in control of a system that responds to their instructions",
                     "Keep all system state internal and hidden from the user",
                     "Let the system decide when to intervene on the user's behalf",
                     "Restrict the actions available to prevent errors"],
         "correct": 0,
         "why": "Shneiderman's rule 7 is about the user feeling in control of a system that responds to their "
                "commands. Hiding state contradicts observability, system-initiated intervention is closer to "
                "adaptivity, and restricting actions is the constraints principle."},
        {"q": "Which is NOT one of Norman's seven principles?",
         "options": ["Cater for universal usability", "Get the mappings right",
                     "Design for error", "When all else fails, standardize"],
         "correct": 0,
         "why": "Cater for universal usability is Shneiderman's second golden rule. The other three are Norman's "
                "principles 4, 6 and 7."},
    ],
    "exam_short": [
        {"q": "Explain how principles, guidelines and standards differ, with an example of each.",
         "keywords": ["principle", "guideline", "standard", "authority"],
         "answer": "They differ on two axes: level of abstraction or generality, and level of authority. "
                   "<b>Principles</b> are abstract with high generality and low authority, widely applicable and "
                   "enduring - for example &quot;the interface should be easy to navigate&quot;, or Dix et al.'s "
                   "usability principles. <b>Guidelines</b> guide or advise on how to achieve a principle; they are "
                   "narrowly focused and can be too specific, incomplete and hard to apply, and are more general and "
                   "lower in authority than standards - for example &quot;use colour to highlight links&quot;, or "
                   "Smith and Mosier's <i>Guidelines for User Interface Software</i>. <b>Standards</b> are very "
                   "specific and high in authority, set by national bodies such as the British Standards Institution "
                   "or international bodies such as ISO - for example &quot;use colour RGB #1010D0 on home "
                   "links&quot;, or ISO 9241."},
        {"q": "Define learnability and describe its five sub-principles.",
         "keywords": ["predictab", "synthesiz", "familiar", "generaliz"],
         "answer": "Learnability is the ease with which new users can begin effective interaction and achieve "
                   "maximal performance. <b>Predictability</b> is support for the user to determine the effect of "
                   "future action based on past interaction history - can I tell what will happen? "
                   "<b>Synthesizability</b> is support for the user to assess the effect of past operations on the "
                   "current state - can I tell why I am here? <b>Familiarity</b> is the extent to which a user's "
                   "knowledge and experience in other real-world or computer-based domains can be applied to a new "
                   "system. <b>Generalizability</b> is support for extending knowledge of specific interaction "
                   "within and across applications to other similar situations. <b>Consistency</b> is likeness in "
                   "input-output behaviour arising from similar situations or similar task objectives, covering "
                   "size, layout, colour and language."},
        {"q": "Define robustness and its four sub-principles.",
         "keywords": ["observab", "recoverab", "responsiv", "conformance"],
         "answer": "Robustness is the level of support provided to the user in determining successful achievement "
                   "and assessment of goal-directed behaviour. <b>Observability</b> is the extent to which the user "
                   "can evaluate the internal state of the system from the representation on the user interface. "
                   "<b>Recoverability</b> is the extent to which the user can reach the intended goal after "
                   "recognizing an error in the previous interaction. <b>Responsiveness</b> is a measure of the rate "
                   "of communication between the user and the system. <b>Task conformance</b> is the extent to which "
                   "the system services support all the tasks the user would wish to perform, and in the way the "
                   "user would wish to perform them."},
        {"q": "List Nielsen's ten usability heuristics.",
         "keywords": ["visibility", "recall", "minimalist", "documentation"],
         "answer": "1. Visibility of system status. 2. Match between system and the real world. 3. User control and "
                   "freedom. 4. Consistency and standards. 5. Error prevention. 6. Recognition rather than recall. "
                   "7. Flexibility and efficiency of use. 8. Aesthetic and minimalist design. 9. Help users "
                   "recognize, diagnose and recover from errors. 10. Help and documentation."},
        {"q": "List Shneiderman's eight golden rules and identify which two have no direct Nielsen counterpart.",
         "keywords": ["consistency", "closure", "locus", "reversal"],
         "answer": "1. Strive for consistency. 2. Cater for universal usability. 3. Offer informative feedback. "
                   "4. Design dialogs to yield closure. 5. Offer error prevention and simple error handling. "
                   "6. Permit easy reversal of actions. 7. Support internal locus of control. 8. Reduce short-term "
                   "memory load. The two without a direct Nielsen counterpart are <b>design dialogs to yield "
                   "closure</b> and <b>support internal locus of control</b>; the rest map onto Nielsen's "
                   "consistency and standards, flexibility and efficiency, visibility of system status, error "
                   "prevention, user control and freedom, and recognition rather than recall."},
        {"q": "State Norman's seven principles and explain how three of them connect to earlier lectures.",
         "keywords": ["knowledge", "visible", "mapping", "constraint"],
         "answer": "1. Use both knowledge in the world and knowledge in the head. 2. Simplify the structure of "
                   "tasks. 3. Make things visible: bridge the gulfs of execution and evaluation. 4. Get the mappings "
                   "right. 5. Exploit the power of constraints, both natural and artificial. 6. Design for error. "
                   "7. When all else fails, standardize. Connections: principle 3 restates the gulfs of execution "
                   "and evaluation framework from the cognitive aspects lecture, where execution is the distance "
                   "from user to system and evaluation the distance back. Principle 4 restates the mapping problem "
                   "from the introductory lecture, illustrated by placing each connector icon directly adjacent to "
                   "its port. Principle 5 restates the constraints design principle, covering both natural "
                   "constraints such as a key that fits one way and artificial ones such as greyed-out menu options. "
                   "Principle 1 also connects to external cognition, since knowledge in the world is exactly what "
                   "externalising and computational offloading exploit."},
    ],
})


LECTURES.append({
    "num": 9,
    "slug": "design-prototyping-and-construction",
    "title": "Design, Prototyping and Construction",
    "short": "Prototyping & Construction",
    "lecture_label": "Lectures 9 & 10",
    "theme": "sketch",
    "accent": "#ff8a3d",
    "accent2": "#5bc8ff",
    "tagline": "What a prototype is, low vs high fidelity, compromises, conceptual and concrete design, and construction.",
    "hero_title": "Prototypes answer questions.<br><em>So prototype appropriately.</em>",
    "hero_sub": ("A prototype can be a lump of wood, a slide show, a paper sketch or working software. What matters "
                 "is which question it is being built to answer - and what compromise you accepted to build it that "
                 "quickly."),
    "badges": ["What is a prototype", "Why prototype", "Low fidelity", "High fidelity",
               "Horizontal vs vertical", "Wizard of Oz", "Conceptual design", "Construction"],
    "outcomes": [
        "Describe prototyping and different types of prototyping activity.",
        "Produce a simple prototype from the models developed during the requirements activity.",
        "Explain conceptual design and its steps from requirements to design.",
        "Evaluate an interface metaphor against the five stated criteria.",
        "Generate storyboards from scenarios and card-based prototypes from use cases.",
    ],
    "sections": [
        {
            "id": "what-why",
            "kicker": "01 - WHAT AND WHY",
            "title": "A prototype is anything users can react to",
            "lead": ("In other design fields a prototype is a small-scale model - a miniature car, a miniature "
                     "building, a 3D-printed part. In interaction design it can be many other things."),
            "blocks": [
                ("list", [
                    "A series of <b>screen sketches</b>.",
                    "A <b>storyboard</b> - a cartoon-like series of scenes.",
                    "A <b>PowerPoint slide show</b>.",
                    "A <b>video</b> simulating the use of a system.",
                    "A <b>lump of wood</b> - the PalmPilot is the famous case.",
                    "A <b>cardboard mock-up</b>.",
                    "A piece of <b>software with limited functionality</b>, written in the target language or in "
                    "another language.",
                ]),
                ("table", (["Why prototype?", "What it buys you"], [
                    ["Evaluation and feedback are central to interaction design.", "A prototype is the object those activities act on."],
                    ["Stakeholders can see, hold and interact with a prototype.", "Far easier than reacting to a document or a drawing."],
                    ["Team members can communicate effectively.", "A shared concrete referent instead of competing mental models."],
                    ["You can test out ideas for yourself.", "Cheap disproof before expensive commitment."],
                    ["It encourages reflection.", "A very important aspect of design."],
                    ["Prototypes answer questions.", "And support designers in choosing between alternatives."],
                ])),
                ("p", "<b>What to prototype:</b> technical issues; work flow and task design; screen layouts and "
                      "information display; and difficult, controversial or critical areas. Prototyping is also "
                      "described along <b>filtering</b> and <b>manifestation</b> dimensions - which aspects of the "
                      "design the prototype keeps, and in what form it appears."),
                ("hook", ("MEMORY HOOK",
                          "The single most useful sentence in this deck: <b>&quot;Prototypes answer questions, so "
                          "prototype appropriately.&quot;</b> Every choice below - fidelity, horizontal or vertical, "
                          "paper or code - follows from asking which question you are trying to answer.")),
            ],
        },
        {
            "id": "low-fi",
            "kicker": "02 - LOW-FIDELITY PROTOTYPES",
            "title": "Unlike the final medium, on purpose",
            "lead": ("A low-fidelity prototype uses a medium which is <b>unlike</b> the final medium - paper, "
                     "cardboard. It is quick, cheap and easily changed."),
            "blocks": [
                ("cards", [
                    ("a. Storyboards",
                     "Often used <b>with scenarios</b>, bringing more detail and a chance to role play. A "
                     "<b>series of sketches showing how a user might progress through a task</b> using the device. "
                     "Used <b>early</b> in design."),
                    ("b. Sketching",
                     "Important to low-fidelity prototyping. <b>Don't be inhibited about drawing ability</b> - "
                     "practise simple symbols. The point is the idea, not the draughtsmanship."),
                    ("c. Card-based",
                     "Index cards (3 x 5 inches), each representing <b>one screen or part of a screen</b>. Often "
                     "used in website development, and generated from use cases."),
                ]),
                ("note", ("THE GENERATION RULE",
                          "The deck states two direct mappings you should be able to reproduce: "
                          "<b>storyboards are generated from scenarios</b>, and <b>card-based prototypes are "
                          "generated from use cases</b>. Narrative &rarr; storyboard; step sequence &rarr; cards.")),
            ],
        },
        {
            "id": "high-fi",
            "kicker": "03 - HIGH-FIDELITY PROTOTYPES",
            "title": "Materials you expect in the final product",
            "lead": ("A high-fidelity prototype uses materials you would expect to be in the final product, and "
                     "looks more like the final system than a low-fidelity version."),
            "blocks": [
                ("list", [
                    "Common software-prototyping environments named in the deck: <b>Macromedia Director, Visual "
                    "Basic, Smalltalk</b>.",
                    "<b>Danger:</b> users think they have a full system.",
                ]),
                ("cards", [
                    ("Wizard of Oz",
                     "The user thinks they are interacting with a computer, but a <b>developer is responding to "
                     "output rather than the system</b>. Usually done <b>early</b> in design to understand users' "
                     "expectations. The lecture asks what is 'wrong' with this approach - the answer is that it "
                     "tests the interaction concept while proving nothing about feasibility, and it depends on a "
                     "human able to respond as no real system yet can."),
                ]),
                ("table", (["Compromise type", "What it provides"], [
                    ["<b>Horizontal</b>", "A <b>wide range of functions</b>, but with little detail."],
                    ["<b>Vertical</b>", "A <b>lot of detail for only a few functions</b>."],
                ])),
                ("warn", ("THE COMPROMISE RULE",
                          "<b>All prototypes involve compromises</b> - a slow response, sketchy icons, limited "
                          "functionality. And: <b>compromises in prototypes must not be ignored. The product needs "
                          "engineering.</b> A prototype that quietly becomes the product ships every compromise "
                          "with it.")),
                ("hook", ("MEMORY HOOK",
                          "<b>Horizontal is wide and shallow; vertical is narrow and deep.</b> Picture the letter: "
                          "the horizontal bar stretches across everything, the vertical bar drills down through one "
                          "spot.")),
            ],
        },
        {
            "id": "construction",
            "kicker": "04 - CONSTRUCTION",
            "title": "Taking the prototypes and creating a whole",
            "lead": ("Construction means taking the prototypes - or learning from them - and creating a whole. "
                     "Quality must be attended to."),
            "blocks": [
                ("list", [
                    "<b>Usability</b> - of course.",
                    "<b>Reliability</b>.",
                    "<b>Robustness</b>.",
                    "<b>Maintainability</b>.",
                    "<b>Integrity</b>.",
                    "<b>Portability</b>.",
                    "<b>Efficiency</b>.",
                ]),
                ("p", "<b>Physical computing</b> is the hardware side of construction: building and coding "
                      "prototypes using electronics. The toolkits named are <b>Arduino</b>, <b>LilyPad</b> (for "
                      "fabrics), <b>Senseboard</b> and <b>MaKey MaKey</b>. All are designed for use by a wide range "
                      "of people, not only engineers."),
                ("hook", ("MEMORY HOOK",
                          "Construction qualities: <b>U-R-R-M-I-P-E</b>. The first is usability and the rest are the "
                          "software-engineering qualities you already know - the point of the list is that usability "
                          "sits <i>among</i> them, not after them.")),
            ],
        },
        {
            "id": "conceptual-design",
            "kicker": "05 - CONCEPTUAL DESIGN",
            "title": "From requirements to design",
            "lead": ("Conceptual design transforms user requirements and needs into a conceptual model - "
                     "<b>the first step of design</b>."),
            "blocks": [
                ("note", ("THE DEFINITION TO QUOTE",
                          "A conceptual model is &quot;a description of the proposed system in terms of a set of "
                          "<b>integrated ideas and concepts</b> about what it should do, behave and look like, that "
                          "will be <b>understandable by the users</b> in the manner intended.&quot;")),
                ("list", [
                    "A <b>mood board</b> may be used to capture the intended feel.",
                    "<b>Don't move to a solution too quickly. Iterate, iterate, iterate.</b>",
                    "Which <b>metaphors</b> would be suitable to help users understand the product?",
                    "Which <b>interaction type(s)</b> would best support the users' activities?",
                    "Do different <b>interface types</b> suggest alternative design insights or options?",
                ]),
                ("steps", [
                    ("Understand the functionality", "Step 1 of finding a metaphor."),
                    ("Identify potential problem areas", "Step 2."),
                    ("Generate metaphors", "Step 3."),
                ]),
                ("table", (["Evaluating a metaphor - five questions", "What it probes"], [
                    ["How much <b>structure</b> does it provide?", "A thin metaphor explains nothing."],
                    ["How much is <b>relevant</b> to the problem?", "Borrowed structure that does not apply becomes misleading."],
                    ["Is it <b>easy to represent</b>?", "If it cannot be drawn or built, it cannot be shown at the interface."],
                    ["Will the <b>audience understand</b> it?", "A metaphor is only familiar knowledge if the audience has it."],
                    ["How <b>extensible</b> is it?", "Will it still work when the product grows?"],
                ])),
                ("p", "<b>Expanding the initial conceptual model</b> asks three groups of question. "
                      "<b>What functions will the product perform</b> - and what will the product do versus what "
                      "will the human do (<b>task allocation</b>)? <b>How are the functions related</b> - sequential "
                      "or parallel, and how are they categorised, such as all actions related to privacy on a "
                      "smartphone? <b>What information is needed</b> - what data is required to perform the task, "
                      "and how is that data to be transformed by the system?"),
                ("cards", [
                    ("Concrete design",
                     "The many detailed aspects: colour, icons, buttons, interaction devices. It must account for "
                     "<b>user characteristics and context</b> - accessibility and cross-cultural design - and follow "
                     "cultural website guidelines. The quotation to remember: successful products &quot;are ... "
                     "<b>bundles of social solutions</b>. Inventors succeed in a particular culture because they "
                     "understand the values, institutional arrangements, and economic notions of that culture.&quot;"),
                ]),
            ],
        },
        {
            "id": "scenarios-in-design",
            "kicker": "06 - SCENARIOS IN CONCEPTUAL DESIGN",
            "title": "Expressing proposed or imagined situations",
            "lead": "Scenarios return here, but doing a different job than in requirements.",
            "blocks": [
                ("list", [
                    "Used as <b>scripts for user evaluation</b> of prototypes.",
                    "Used as <b>concrete examples of tasks</b>.",
                    "Used as <b>a means of co-operation across professional boundaries</b>.",
                    "<b>Plus and minus scenarios</b> explore extreme cases - the best and worst that could happen.",
                ]),
                ("note", ("THE TWO GENERATION PATHS",
                          "<b>Scenario &rarr; storyboard.</b> <b>Use case &rarr; card-based prototype.</b> "
                          "Both appear as worked examples in the deck, and both are the kind of thing an exam asks "
                          "you to demonstrate rather than define.")),
                ("hook", ("MEMORY HOOK",
                          "A scenario is a <b>story</b>, so it becomes a <b>picture strip</b> (storyboard). A use "
                          "case is a <b>numbered sequence</b>, so it becomes a <b>stack of numbered cards</b>. The "
                          "artifact keeps the shape of its source.")),
            ],
        },
    ],
    "mistakes": [
        ("&quot;High fidelity is always better.&quot;",
         "High-fidelity prototypes carry the danger that <b>users think they have a full system</b>, and they are "
         "slower and more expensive to change. Paper prototypes are quick, cheap and very effective at identifying "
         "problems in early design."),
        ("Swapping horizontal and vertical compromises.",
         "<b>Horizontal</b> = wide range of functions with little detail. <b>Vertical</b> = a lot of detail for only "
         "a few functions."),
        ("Ignoring prototype compromises when building the product.",
         "&quot;Compromises in prototypes mustn't be ignored. Product needs engineering.&quot; A slow response or "
         "sketchy icon accepted in a prototype is a defect if it survives into the product."),
        ("Thinking Wizard of Oz means the system is partly built.",
         "The user believes they are interacting with a computer, but a <b>developer</b> is producing the responses. "
         "It is done early to understand users' expectations, and proves nothing about technical feasibility."),
        ("Generating a storyboard from a use case.",
         "The stated mappings are <b>scenario &rarr; storyboard</b> and <b>use case &rarr; card-based prototype</b>."),
        ("Listing only usability as a construction quality.",
         "The list is usability, reliability, robustness, maintainability, integrity, portability and efficiency."),
        ("Treating conceptual design as screen design.",
         "Conceptual design produces the integrated ideas and concepts about what the system should do, behave and "
         "look like, understandable by users. Colour, icons and buttons belong to <b>concrete design</b>."),
    ],
    "cheat": (["Concept", "Shortest correct answer"], [
        ["Prototype", "Anything from screen sketches, a storyboard, a slide show, a video, a lump of wood or a cardboard mock-up to limited-functionality software."],
        ["Why prototype", "Prototypes answer questions, support choosing between alternatives, enable stakeholder feedback, aid team communication and encourage reflection."],
        ["What to prototype", "Technical issues; work flow and task design; screen layouts and information display; difficult, controversial or critical areas."],
        ["Low fidelity", "Uses a medium unlike the final one - paper, cardboard. Quick, cheap, easily changed."],
        ["Low-fi forms", "Storyboards, sketching, card-based prototypes."],
        ["Storyboard", "A series of sketches showing how a user might progress through a task; used early, often with scenarios."],
        ["High fidelity", "Uses materials expected in the final product; danger that users think they have a full system."],
        ["Wizard of Oz", "The user thinks they interact with a computer, but a developer produces the responses; used early to understand expectations."],
        ["Horizontal prototype", "Wide range of functions with little detail."],
        ["Vertical prototype", "A lot of detail for only a few functions."],
        ["Construction qualities", "Usability, reliability, robustness, maintainability, integrity, portability, efficiency."],
        ["Physical computing kits", "Arduino, LilyPad (fabrics), Senseboard, MaKey MaKey."],
        ["Conceptual model", "A description of the proposed system as integrated ideas and concepts about what it should do, behave and look like, understandable by users."],
        ["Metaphor evaluation", "Structure, relevance, ease of representation, audience understanding, extensibility."],
        ["Task allocation", "Deciding what the product will do and what the human will do."],
        ["Concrete design", "Colour, icons, buttons, interaction devices, plus accessibility and cross-cultural design."],
    ]),
    "quiz": [
        {"q": "A team builds a working screen for the single checkout flow, with every edge case handled, and nothing else. Which compromise is this?",
         "options": ["Vertical", "Horizontal", "Wizard of Oz", "Low fidelity"], "correct": 0,
         "why": "Vertical prototypes provide a lot of detail for only a few functions - exactly one deep flow here. "
                "Horizontal would provide a wide range of functions with little detail. Wizard of Oz concerns who "
                "produces the responses, and fidelity concerns the medium used."},
        {"q": "In a Wizard of Oz prototype, who produces the system's responses?",
         "options": ["A developer, while the user believes it is the computer",
                     "The system, using a limited rule set",
                     "The user, thinking aloud",
                     "A second participant acting as a peer"], "correct": 0,
         "why": "The defining property is that the user thinks they are interacting with a computer while a "
                "developer is responding. It is used early in design to understand users' expectations before any "
                "capability exists."},
        {"q": "Which mapping does the lecture state?",
         "options": ["Use cases generate card-based prototypes",
                     "Use cases generate storyboards",
                     "Scenarios generate use cases",
                     "Personas generate storyboards"], "correct": 0,
         "why": "The two stated generation paths are scenario to storyboard and use case to card-based prototype. "
                "Each artifact keeps the shape of its source - a narrative becomes a picture strip, a numbered "
                "sequence becomes numbered cards."},
        {"q": "Which of these is NOT one of the five questions for evaluating an interface metaphor?",
         "options": ["How much does it cost to implement?",
                     "How much structure does it provide?",
                     "Will the audience understand it?",
                     "How extensible is it?"], "correct": 0,
         "why": "The five questions are structure, relevance to the problem, ease of representation, audience "
                "understanding and extensibility. Implementation cost is a real constraint but is not one of the "
                "five stated criteria."},
        {"q": "What is the stated danger of high-fidelity prototypes?",
         "options": ["Users think they have a full system",
                     "They cannot be evaluated with real users",
                     "They take longer to evaluate than to build",
                     "They cannot represent screen layouts"], "correct": 0,
         "why": "That is the danger the lecture names. High-fidelity prototypes are perfectly evaluable and can "
                "represent layouts in detail; the risk is the expectation they create."},
        {"q": "Which quality is NOT listed among the construction qualities?",
         "options": ["Extensibility", "Integrity", "Portability", "Maintainability"], "correct": 0,
         "why": "The list is usability, reliability, robustness, maintainability, integrity, portability and "
                "efficiency. Extensibility appears instead as one of the five metaphor-evaluation questions."},
    ],
    "lab": [
        ("You have one week to decide between three navigation concepts for a banking app. Choose a prototyping strategy and justify every choice.",
         "The question being answered is <b>which structure users can navigate</b>, not whether it can be built, so "
         "prototype appropriately: use <b>low fidelity</b>, since it is quick, cheap and easily changed, and a "
         "medium unlike the final one keeps stakeholders discussing structure rather than colour. Build "
         "<b>card-based prototypes</b> - one card per screen or part of a screen - generated from the use cases, "
         "plus <b>storyboards</b> generated from two scenarios so users can role play the whole journey. Take the "
         "<b>horizontal</b> compromise: a wide range of functions with little detail, because the comparison is "
         "across the breadth of the navigation. Note the compromises explicitly - no real response times, sketchy "
         "icons - because compromises must not be ignored when the product is engineered. Do <b>not</b> build high "
         "fidelity here: it is slower to change and carries the danger that users think they have a full system and "
         "start commenting on polish instead of structure."),
        ("Evaluate a 'filing cabinet' metaphor for a cloud storage product against the five criteria.",
         "<b>Structure:</b> strong - drawers, folders, hanging files and labels give a rich set of relationships to "
         "borrow. <b>Relevance:</b> partly - hierarchy and naming transfer, but a physical file exists in exactly "
         "one drawer, whereas cloud files are shared, versioned and appear in several places, so the metaphor "
         "actively misleads about the most important new behaviours. <b>Ease of representation:</b> high - drawers "
         "and folders are trivially drawable and already conventional. <b>Audience understanding:</b> falling - "
         "younger users may never have used a physical filing cabinet, so the familiar knowledge the metaphor "
         "depends on is not universal. <b>Extensibility:</b> poor - sharing, sync conflicts and collaborative "
         "editing have no cabinet equivalent, so the metaphor breaks exactly where the product grows. Conclusion: "
         "borrow folders and naming, but do not commit to the cabinet, or it will constrain how the team "
         "conceptualizes the problem space - one of the stated problems with metaphors."),
        ("Explain why a successful prototype is not a product, using the lecture's own vocabulary.",
         "Because <b>all prototypes involve compromises</b>. For software-based prototyping that may mean a slow "
         "response, sketchy icons or limited functionality, and structurally it means either a <b>horizontal</b> "
         "compromise - a wide range of functions with little detail - or a <b>vertical</b> one - a lot of detail for "
         "only a few functions. Neither is a whole system. The lecture states the rule directly: compromises in "
         "prototypes must not be ignored, and the product needs engineering. <b>Construction</b> is the separate "
         "activity of taking the prototypes, or learning from them, and creating a whole in which quality is "
         "attended to - usability, reliability, robustness, maintainability, integrity, portability and efficiency. "
         "A high-fidelity prototype is especially dangerous here, because users already think they have a full "
         "system, which makes it politically hard to admit that the engineering has not been done."),
    ],
    "branches": [
        ("What is a prototype",
         "In interaction design, anything from a sketch to limited-functionality software that lets stakeholders see, hold and interact with a design.",
         ["In other design fields a prototype is a small-scale model such as a miniature car or building.",
          "In interaction design it can be a series of screen sketches.",
          "It can be a storyboard - a cartoon-like series of scenes.",
          "It can be a PowerPoint slide show or a video simulating the use of a system.",
          "It can be a lump of wood, as with the PalmPilot, or a cardboard mock-up.",
          "It can be a piece of software with limited functionality written in the target language or another language.",
          "Prototyping is described along filtering and manifestation dimensions."],
         [("The PalmPilot block", "A pocket-sized lump of wood carried around to test whether the form factor fitted into daily life before any electronics existed."),
          ("Video prototype", "Simulating use on film answers questions about context and flow without building anything interactive.")]),
        ("Why and what to prototype",
         "Prototypes answer questions and support designers in choosing between alternatives.",
         ["Evaluation and feedback are central to interaction design.",
          "Stakeholders can see, hold and interact with a prototype more easily than with a document or drawing.",
          "Team members can communicate effectively through a shared concrete artifact.",
          "Designers can test out ideas for themselves.",
          "Prototyping encourages reflection, a very important aspect of design.",
          "What to prototype: technical issues; work flow and task design; screen layouts and information display; and difficult, controversial or critical areas."],
         [("Choosing between alternatives", "Because interaction design judges externally visible behaviour, only a prototype can settle a disagreement that a specification cannot.")]),
        ("Low-fidelity prototypes",
         "Prototypes using a medium unlike the final medium, such as paper or cardboard - quick, cheap and easily changed.",
         ["Examples include sketches of screens and task sequences, Post-it notes and storyboards.",
          "Storyboards are a series of sketches showing how a user might progress through a task using the device.",
          "Storyboards are often used with scenarios, bringing more detail and a chance to role play, and are used early in design.",
          "Sketching is important to low-fidelity prototyping and designers should not be inhibited about drawing ability.",
          "Card-based prototypes use index cards of about 3 by 5 inches, each representing one screen or part of a screen.",
          "Card-based prototypes are often used in website development."],
         [("Practising symbols", "The advice is to practise simple symbols rather than improve draughtsmanship, since the sketch carries the idea, not the artwork."),
          ("Role play", "Walking through a storyboard aloud gives users a real sense of the interaction before anything is built.")]),
        ("High-fidelity prototypes and compromises",
         "Prototypes using materials expected in the final product, which look more like the final system but carry real risks.",
         ["Common software prototyping environments include Macromedia Director, Visual Basic and Smalltalk.",
          "The danger is that users think they have a full system.",
          "In Wizard of Oz prototyping the user thinks they are interacting with a computer, but a developer is responding to output rather than the system.",
          "Wizard of Oz is usually done early in design to understand users' expectations.",
          "All prototypes involve compromises, such as slow response, sketchy icons or limited functionality.",
          "Horizontal prototypes provide a wide range of functions with little detail.",
          "Vertical prototypes provide a lot of detail for only a few functions.",
          "Compromises in prototypes must not be ignored, because the product needs engineering."],
         [("Horizontal in practice", "Every menu present but nothing behind it - useful for testing whether users can find things."),
          ("Vertical in practice", "One complete purchase flow with every error path - useful for testing whether users can finish a task.")]),
        ("Construction",
         "Taking the prototypes, or learning from them, and creating a whole in which quality is attended to.",
         ["Usability must be attended to, along with reliability and robustness.",
          "Maintainability and integrity are construction qualities.",
          "Portability and efficiency complete the list.",
          "Physical computing means building and coding prototypes using electronics.",
          "Toolkits include Arduino, LilyPad for fabrics, Senseboard and MaKey MaKey.",
          "These toolkits are designed for use by a wide range of people, not only engineers."],
         [("LilyPad", "A sewable microcontroller designed for fabric prototypes, which puts wearable interaction design within reach of non-engineers.")]),
        ("Conceptual design",
         "The first step of design: transforming user requirements and needs into a conceptual model.",
         ["A conceptual model is a description of the proposed system in terms of a set of integrated ideas and concepts about what it should do, behave and look like, understandable by users in the manner intended.",
          "A mood board may be used to capture the intended feel.",
          "Do not move to a solution too quickly - iterate.",
          "Ask which metaphors would help users understand the product, which interaction types would support their activities, and whether different interface types suggest alternative options.",
          "Finding a metaphor has three steps: understand the functionality, identify potential problem areas, and generate metaphors.",
          "Evaluate a metaphor by asking how much structure it provides, how much is relevant to the problem, whether it is easy to represent, whether the audience will understand it, and how extensible it is.",
          "Expanding the model asks what functions the product will perform and how tasks are allocated between product and human.",
          "It also asks how functions relate - sequential or parallel - and how they are categorised.",
          "It also asks what information is needed, what data is required, and how the system transforms it."],
         [("Task allocation", "Deciding what the product does and what the human does is an explicit design decision, not a leftover."),
          ("Privacy category", "Grouping all actions related to privacy on a smartphone is the lecture's example of categorising related functions.")]),
        ("Concrete design and scenarios",
         "The detailed design layer, and the use of scenarios to express proposed or imagined situations.",
         ["Concrete design covers colour, icons, buttons and interaction devices.",
          "It must account for user characteristics and context, including accessibility and cross-cultural design.",
          "Cultural website guidelines apply, since successful products are bundles of social solutions.",
          "Inventors succeed in a particular culture because they understand its values, institutional arrangements and economic notions.",
          "Scenarios are used as scripts for user evaluation of prototypes.",
          "Scenarios serve as concrete examples of tasks and as a means of co-operation across professional boundaries.",
          "Plus and minus scenarios explore extreme cases.",
          "Storyboards are generated from scenarios and card-based prototypes are generated from use cases."],
         [("Plus and minus scenarios", "Writing the best and worst version of the same situation surfaces requirements that the neutral version hides."),
          ("Cross-boundary use", "A scenario is readable by a marketer, an engineer and a clinician alike, which is why it works as a co-operation device.")]),
    ],
    "exam_mcq": [
        {"q": "Which statement best defines a low-fidelity prototype?",
         "options": ["It uses a medium unlike the final medium, such as paper or cardboard",
                     "It uses the materials expected in the final product",
                     "It is any prototype with fewer than ten screens",
                     "It is a prototype produced after user testing has begun"],
         "correct": 0,
         "why": "Low fidelity is defined by using a medium unlike the final one, which is what makes it quick, cheap "
                "and easily changed. Using the final materials is high fidelity; screen count and timing are not "
                "part of the definition."},
        {"q": "Which is a stated benefit of prototyping?",
         "options": ["Stakeholders can see, hold and interact with a prototype more easily than with a document",
                     "Prototypes remove the need for evaluation",
                     "Prototypes eliminate the need to engineer the final product",
                     "Prototypes guarantee technical feasibility"],
         "correct": 0,
         "why": "That benefit is stated directly. Evaluation and feedback remain central; the product still needs "
                "engineering because prototypes involve compromises; and a Wizard of Oz prototype in particular "
                "proves nothing about feasibility."},
        {"q": "A prototype offering every menu and screen in the product, but with no working detail behind them, is:",
         "options": ["A horizontal prototype", "A vertical prototype",
                     "A high-fidelity prototype", "A Wizard of Oz prototype"],
         "correct": 0,
         "why": "Horizontal prototypes provide a wide range of functions with little detail. Vertical is the "
                "opposite; fidelity concerns the medium; Wizard of Oz concerns who generates the responses."},
        {"q": "Which quotation matches the lecture's definition of a conceptual model in this deck?",
         "options": ["A description of the proposed system in terms of a set of integrated ideas and concepts about what it should do, behave and look like, understandable by users",
                     "A scale model of the final product used for user testing",
                     "The set of screens, colours and icons chosen for the interface",
                     "A numbered sequence of user and system steps with alternative courses"],
         "correct": 0,
         "why": "That is the definition given. A scale model is a prototype, screens and colours are concrete design, "
                "and the numbered sequence with alternative courses is a use case."},
        {"q": "Which toolkit is specifically named for fabric-based physical computing?",
         "options": ["LilyPad", "Arduino", "Senseboard", "MaKey MaKey"],
         "correct": 0,
         "why": "LilyPad is the one described as being for fabrics. Arduino, Senseboard and MaKey MaKey are the "
                "other named kits, all designed for use by a wide range of people."},
        {"q": "Which is NOT one of the three steps for finding a suitable metaphor?",
         "options": ["Test the metaphor with a high-fidelity prototype",
                     "Understand the functionality",
                     "Identify potential problem areas",
                     "Generate metaphors"],
         "correct": 0,
         "why": "The three steps are understand functionality, identify potential problem areas, and generate "
                "metaphors, after which the metaphor is evaluated against five criteria. Building a high-fidelity "
                "prototype is not one of the steps."},
    ],
    "exam_short": [
        {"q": "What is a prototype in interaction design, and why do teams build them?",
         "keywords": ["prototype", "question", "feedback", "alternativ"],
         "answer": "In interaction design a prototype can be a series of screen sketches, a storyboard, a PowerPoint "
                   "slide show, a video simulating use, a lump of wood as with the PalmPilot, a cardboard mock-up, "
                   "or software with limited functionality. Teams build them because evaluation and feedback are "
                   "central to interaction design; stakeholders can see, hold and interact with a prototype far more "
                   "easily than with a document or drawing; team members can communicate effectively around a shared "
                   "concrete artifact; designers can test ideas for themselves; and prototyping encourages "
                   "reflection, a very important aspect of design. Above all, prototypes answer questions and "
                   "support designers in choosing between alternatives."},
        {"q": "Compare low-fidelity and high-fidelity prototypes, including the danger of each.",
         "keywords": ["low", "high", "medium", "danger"],
         "answer": "A low-fidelity prototype uses a medium unlike the final medium - paper or cardboard - and is "
                   "quick, cheap and easily changed; its forms are storyboards, sketching and card-based "
                   "prototypes. It is very effective at identifying problems in early design, but it cannot "
                   "represent real response times or fine visual detail. A high-fidelity prototype uses materials "
                   "you would expect in the final product and looks much more like the final system, built in "
                   "environments such as Macromedia Director, Visual Basic or Smalltalk; its stated danger is that "
                   "users think they have a full system. Both involve compromises, and those compromises must not be "
                   "ignored, because the product still needs engineering."},
        {"q": "Explain horizontal and vertical prototyping compromises and when each is appropriate.",
         "keywords": ["horizontal", "vertical", "detail", "function"],
         "answer": "A horizontal prototype provides a wide range of functions but with little detail; a vertical "
                   "prototype provides a lot of detail for only a few functions. Horizontal suits questions about "
                   "breadth - can users find things, does the overall structure make sense, how do the parts relate? "
                   "Vertical suits questions about depth - can a user actually complete this task, including the "
                   "error paths and edge cases? Since prototypes answer questions, the choice follows from which "
                   "question is being asked. Both are compromises and both must be recorded, because a compromise "
                   "carried silently into the product becomes a defect."},
        {"q": "What is a Wizard of Oz prototype, when is it used, and what is 'wrong' with it?",
         "keywords": ["wizard", "developer", "expectation", "early"],
         "answer": "In a Wizard of Oz prototype the user thinks they are interacting with a computer, but a "
                   "developer is responding to their input rather than the system. It is usually done early in "
                   "design to understand users' expectations - what people will try to say or do when they believe "
                   "an intelligent system is listening. What is 'wrong' with it is that it tests the interaction "
                   "concept while proving nothing about technical feasibility: the human wizard can respond in ways "
                   "no existing system can, so it can validate a design that cannot actually be built, and it "
                   "involves a degree of deception that must be handled ethically in debriefing."},
        {"q": "Describe conceptual design and the five criteria for evaluating a metaphor.",
         "keywords": ["conceptual", "metaphor", "structure", "extensib"],
         "answer": "Conceptual design is the first step of design: transforming user requirements and needs into a "
                   "conceptual model, described as a set of integrated ideas and concepts about what the system "
                   "should do, behave and look like, understandable by users in the manner intended. A mood board "
                   "may capture the intended feel, and the rule is not to move to a solution too quickly but to "
                   "iterate. Finding a metaphor has three steps - understand the functionality, identify potential "
                   "problem areas, generate metaphors - and each candidate is then evaluated by asking: how much "
                   "structure does it provide; how much of it is relevant to the problem; is it easy to represent; "
                   "will the audience understand it; and how extensible is it?"},
        {"q": "How are storyboards and card-based prototypes generated, and what is construction?",
         "keywords": ["storyboard", "scenario", "use case", "construction"],
         "answer": "Storyboards are generated from <b>scenarios</b>: the informal narrative is turned into a series "
                   "of sketches showing how a user might progress through the task, bringing more detail and "
                   "allowing role play. Card-based prototypes are generated from <b>use cases</b>: each numbered "
                   "step or screen becomes an index card representing one screen or part of a screen, a technique "
                   "often used in website development. Construction is the separate activity of taking the "
                   "prototypes, or learning from them, and creating a whole. Quality must be attended to: usability, "
                   "reliability, robustness, maintainability, integrity, portability and efficiency. Where hardware "
                   "is involved, physical computing kits such as Arduino, LilyPad for fabrics, Senseboard and MaKey "
                   "MaKey let a wide range of people build and code electronic prototypes."},
    ],
})


LECTURES.append({
    "num": 11,
    "slug": "evaluation-foundations",
    "title": "Evaluation: Foundations",
    "short": "Evaluation (Part 1)",
    "lecture_label": "Lecture 11",
    "theme": "lens",
    "accent": "#4fc3f7",
    "accent2": "#a5d64c",
    "tagline": "Why, what, where and when to evaluate; the three types of evaluation; running a usability test session.",
    "hero_title": "You are not your user.<br><em>Testing with one is better than none.</em>",
    "hero_sub": ("Evaluation is integral to the design process. Evaluators collect information about users' "
                 "experiences with a prototype, system, application or design artifact - and they do it "
                 "<b>in order to improve design</b>."),
    "badges": ["Why/what/where/when", "3 types of evaluation", "Living labs",
               "Task instructions", "Tester / moderator / observer", "Reliability & validity"],
    "outcomes": [
        "Explain the key concepts and terms used in evaluation.",
        "Describe the range of different types of evaluation method.",
        "Explain how methods suit different purposes, stages and contexts of use.",
        "Show how evaluators mix and modify methods for novel systems.",
        "Discuss the practical challenges of doing evaluation.",
    ],
    "sections": [
        {
            "id": "intro",
            "kicker": "01 - WHAT EVALUATION IS",
            "title": "Integral to the design process",
            "lead": ("Evaluators collect information about users' or potential users' experiences when interacting "
                     "with a prototype, a computer system, an application or a design artifact. They do this "
                     "<b>because it improves design</b>."),
            "blocks": [
                ("list", [
                    "Evaluation focuses on the <b>usability</b> of the system - how easy it is to learn and use.",
                    "And on the <b>user experience</b> when interacting with it - how satisfying, enjoyable or "
                    "motivating the interaction is.",
                ]),
                ("note", ("THE UXPA DEFINITION",
                          "&quot;User experience (UX) is an approach to product development that incorporates "
                          "<b>direct user feedback throughout the development cycle</b> (human-centered design) in "
                          "order to <b>reduce costs</b> and create products and tools that meet user needs and have "
                          "a high level of usability.&quot; - User Experience Professionals Association. "
                          "Note the cost argument: UX work is justified economically, not only ethically.")),
            ],
        },
        {
            "id": "wwww",
            "kicker": "02 - THE FOUR QUESTIONS",
            "title": "Why, what, where and when to evaluate",
            "lead": ("Iterative design and evaluation is a <b>continuous process</b>, and these four questions "
                     "frame every study."),
            "blocks": [
                ("table", (["Question", "Answer"], [
                    ["<b>Why</b>", "To check users' requirements, that users <i>can</i> use the product, and that they like it."],
                    ["<b>What</b>", "A conceptual model, early prototypes of a new system, and later, more complete prototypes."],
                    ["<b>Where</b>", "In natural <b>and</b> laboratory settings."],
                    ["<b>When</b>", "Throughout design. Finished products can also be evaluated, to collect information that informs new products."],
                ])),
                ("hook", ("MEMORY HOOK",
                          "The four answers all resist narrowing: <b>why</b> is three things not one, <b>what</b> "
                          "starts before there is a system, <b>where</b> is both settings, and <b>when</b> includes "
                          "after shipping. Evaluation is bigger than 'test the finished product'.")),
            ],
        },
        {
            "id": "types",
            "kicker": "03 - THE THREE TYPES",
            "title": "Controlled, natural, and without users",
            "lead": "Every evaluation method the course covers falls into one of exactly three types.",
            "blocks": [
                ("cards", [
                    ("1. Controlled settings that directly involve users",
                     "Usability labs and research labs. Conditions are controlled as much as possible, and the same "
                     "conditions apply to every participant."),
                    ("2. Natural settings involving users",
                     "Online communities and products used in public places. There is often <b>little or no "
                     "control</b> over what users do, especially in <b>in-the-wild</b> settings."),
                    ("3. Any setting that does not directly involve users",
                     "Consultants and researchers critique the prototypes, and may <b>predict and model</b> how "
                     "successful they will be when used by users."),
                ]),
                ("p", "<b>Living labs</b> extend the idea of a lab: people's use of technology in their everyday "
                      "lives can be evaluated there, when such evaluations are too difficult to do in a usability "
                      "lab. The <b>Aware Home</b> (Abowd et al., 2000) was embedded with a complex network of "
                      "sensors and audio/video recording devices. More recent examples include whole blocks and "
                      "cities housing hundreds of people (Verma et al., 2017, in Switzerland). Many citizen science "
                      "projects such as iNaturalist.com can also be thought of as living labs. The concept of a lab "
                      "is changing to include other spaces where technology use can be studied in realistic "
                      "environments."),
                ("table", (["Case study type", "Example from the deck"], [
                    ["Classic experiment", "An investigation into the <b>physiological responses</b> of players of a computer game."],
                    ["Ethnographic study", "Visitors at the <b>Royal Highland Show</b>, directed and tracked using a cell phone app."],
                    ["Crowdsourcing", "The opinions and reactions of volunteers - the crowd - inform technology evaluation."],
                ])),
                ("note", ("COMPLEMENTARY, NOT COMPETING",
                          "Usability testing and field studies <b>complement</b> each other. Lab work gives control "
                          "and comparable measures; field work gives ecological validity and surprises. Neither "
                          "substitutes for the other.")),
            ],
        },
        {
            "id": "tasks",
            "kicker": "04 - CASE STUDY: AIRLINE BOOKING",
            "title": "Writing task instructions",
            "lead": ("Task instructions must be <b>goal-oriented</b> and <b>non-leading</b>. This is the part of "
                     "test design that most often invalidates a study before it starts."),
            "blocks": [
                ("table", (["", "Example"], [
                    ["<b>Non-leading (correct)</b>", "&quot;Try to buy plane tickets for your family vacation.&quot;"],
                    ["<b>Leading (wrong)</b>", "&quot;Press the red button and then click the first top-right button with an airplane icon...&quot;"],
                ])),
                ("list", [
                    "Task-oriented: &quot;Get a ticket to London on a certain date.&quot;",
                    "The sample instructions from the deck: <b>What impression does this website give you compared "
                    "to other airline websites?</b> / <b>You want to fly to Chicago this January for 5 days - find "
                    "suitable flight times (return tickets) for you and your family.</b> / <b>Decide on suitable "
                    "flight times and try to buy the tickets. Tell us if anything will affect you from completing "
                    "the purchase.</b> / <b>How much luggage can you bring with you on this flight?</b>",
                ]),
                ("warn", ("WHY LEADING TASKS RUIN A TEST",
                          "A leading instruction tells the user where to look, which is exactly the knowledge the "
                          "test is supposed to measure. If you name the button, you have tested nothing but their "
                          "ability to follow directions.")),
            ],
        },
        {
            "id": "roles",
            "kicker": "05 - RUNNING THE SESSION",
            "title": "Tester, moderator, observer",
            "lead": "Three roles, three sets of rules. The exam asks which rule belongs to which role.",
            "blocks": [
                ("cards", [
                    ("Tester (the participant)",
                     "1. <b>Think aloud.</b> 2. Be more than 100% honest about likes and dislikes, and about what is "
                     "difficult or easy. 3. Remember <b>it is not an IQ test</b>. 4. Give suggestions."),
                    ("Moderator",
                     "1. Act as a <b>tour guide</b>. 2. <b>Interrupt only when necessary.</b> 3. <b>Don't answer "
                     "questions</b> for the tester. 4. Ask questions starting with <b>&quot;What&quot;</b> or "
                     "<b>&quot;How&quot;</b> if the tester becomes quiet."),
                    ("Observer",
                     "1. <b>Watch.</b> 2. <b>Listen.</b> 3. <b>Take notes.</b>"),
                ]),
                ("p", "Testing can be done <b>in person</b>, with the three roles in one of two room setups, or "
                      "<b>remotely by crowdsourcing</b> - conducting the test with crowdsourced testers so clients "
                      "can watch and listen. In the remote case the people involved are the <b>observer</b> and the "
                      "<b>tester</b>."),
                ("note", ("PARTICIPANTS' RIGHTS AND CONSENT",
                          "Participants need to be told <b>why</b> the evaluation is being done, <b>what</b> they "
                          "will be asked to do, and <b>their rights</b>. Informed consent forms provide this "
                          "information and act as a <b>contract</b> between participants and researchers. The design "
                          "of the form, the evaluation process, the data analysis and the data storage methods are "
                          "typically approved by a higher authority such as an <b>Institutional Review Board</b>.")),
                ("hook", ("MEMORY HOOK",
                          "The moderator's job is defined entirely by <b>restraint</b>: guide, don't interrupt, "
                          "don't answer, and when the silence gets awkward ask <i>what</i> or <i>how</i> - never "
                          "<i>why don't you click there</i>.")),
            ],
        },
        {
            "id": "analysis",
            "kicker": "06 - ANALYSIS AND INTERPRETATION",
            "title": "From session to finding",
            "lead": "The lecture gives a four-step common practice, and five things to watch when interpreting data.",
            "blocks": [
                ("steps", [
                    ("Transcribe the evaluation sessions", "Verbal and actions, from both the tester and the moderator."),
                    ("Analyze the transcript", "Based on the objective of the evaluation - usability, user behaviour and so on."),
                    ("Highlight other issues", "Anything else observed during the sessions."),
                    ("Report findings", "Present what the data supports."),
                ]),
                ("table", (["Consideration", "The question it asks"], [
                    ["<b>Reliability</b>", "Does the method produce the same results on separate occasions?"],
                    ["<b>Validity</b>", "Does the method measure what it is intended to measure?"],
                    ["<b>Ecological validity</b>", "Does the <b>environment</b> of the evaluation distort the results?"],
                    ["<b>Biases</b>", "Are there biases that distort the results?"],
                    ["<b>Scope</b>", "How generalizable are the results?"],
                ])),
                ("warn", ("VALIDITY vs ECOLOGICAL VALIDITY",
                          "Plain <b>validity</b> asks whether the <i>method</i> measures the right thing. "
                          "<b>Ecological validity</b> asks whether the <i>setting</i> distorts the result - a lab "
                          "task done perfectly in silence may fail on a noisy train. They are separate marks.")),
            ],
        },
        {
            "id": "keypoints",
            "kicker": "07 - KEY POINTS",
            "title": "The summary the deck itself gives",
            "lead": "Both summary slides in this deck are quotable, and both are examinable.",
            "blocks": [
                ("list", [
                    "Evaluation and design are <b>closely integrated</b> in user-centered design.",
                    "Some of the <b>same techniques</b> are used in evaluation as for establishing requirements, but "
                    "they are used <b>differently</b> - observation, interviews and questionnaires.",
                    "Three types of evaluation: <b>laboratory based with users, in the field with users, and studies "
                    "that do not involve users</b>.",
                    "The main methods are <b>observing, asking users, asking experts, user testing, inspection, "
                    "modeling users' task performance, and analytics</b>.",
                    "<b>Dealing with constraints</b> is an important skill for evaluators to develop.",
                ]),
                ("cards", [
                    ("The six closing rules",
                     "<b>Test instructions: goal oriented.</b> <b>Usability testing can be done easily.</b> "
                     "<b>User's action speaks louder than words.</b> <b>Testing can be done in any stage.</b> "
                     "<b>You are not your user.</b> <b>Testing with one user is better than none.</b>"),
                ]),
                ("hook", ("MEMORY HOOK",
                          "&quot;<b>You are not your user</b>&quot; is the entire course compressed into five words - "
                          "it is Lecture 1's frame-of-reference problem stated as an evaluation rule. Pair it with "
                          "&quot;<b>action speaks louder than words</b>&quot;: what users <i>do</i> in a test "
                          "outranks what they <i>say</i> in a questionnaire.")),
            ],
        },
    ],
    "mistakes": [
        ("Naming only two types of evaluation.",
         "There are three: controlled settings that directly involve users; natural settings involving users; and "
         "any setting that does <b>not</b> directly involve users."),
        ("Confusing validity with ecological validity.",
         "Validity asks whether the <b>method</b> measures what it is intended to measure. Ecological validity asks "
         "whether the <b>environment</b> of the evaluation distorts the results."),
        ("Confusing reliability with validity.",
         "Reliability asks whether the method produces the <b>same results on separate occasions</b>. A method can "
         "be perfectly reliable and still measure the wrong thing."),
        ("Writing leading task instructions.",
         "&quot;Press the red button then click the airplane icon&quot; tests nothing. The non-leading version is "
         "&quot;try to buy plane tickets for your family vacation&quot;."),
        ("Letting the moderator answer the tester's questions.",
         "The moderator is a tour guide who interrupts only when necessary, does <b>not</b> answer questions for the "
         "tester, and asks &quot;What&quot; or &quot;How&quot; questions if the tester goes quiet."),
        ("&quot;A living lab is just a bigger usability lab.&quot;",
         "Living labs evaluate people's use of technology in their <b>everyday lives</b>, for evaluations too "
         "difficult to do in a usability lab - the Aware Home, whole city blocks, and citizen science projects."),
        ("Treating consent as a formality.",
         "Informed consent forms tell participants why the evaluation is being done, what they will do and what "
         "their rights are, and act as a <b>contract</b>. The form, process, analysis and storage methods are "
         "typically approved by a body such as an Institutional Review Board."),
    ],
    "cheat": (["Concept", "Shortest correct answer"], [
        ["Evaluation", "Collecting information about users' experiences with a prototype, system, application or artifact, in order to improve design."],
        ["Why evaluate", "To check users' requirements, that users can use the product, and that they like it."],
        ["What to evaluate", "A conceptual model, early prototypes, and later more complete prototypes."],
        ["Where", "Natural and laboratory settings."],
        ["When", "Throughout design; finished products too, to inform new products."],
        ["Three types", "Controlled settings with users; natural settings with users; any setting without users."],
        ["Living lab", "Evaluating everyday technology use in realistic environments - the Aware Home, city blocks, citizen science."],
        ["Task instructions", "Goal oriented and non-leading."],
        ["Tester rules", "Think aloud, be honest, remember it is not an IQ test, give suggestions."],
        ["Moderator rules", "Tour guide, interrupt only when necessary, don't answer questions, ask What or How when the tester goes quiet."],
        ["Observer rules", "Watch, listen, take notes."],
        ["Informed consent", "Tells participants why, what they will do, and their rights; acts as a contract; typically approved by an IRB."],
        ["Reliability", "Does the method produce the same results on separate occasions?"],
        ["Validity", "Does the method measure what it is intended to measure?"],
        ["Ecological validity", "Does the environment of the evaluation distort the results?"],
        ["Main methods", "Observing, asking users, asking experts, user testing, inspection, modeling task performance, analytics."],
    ]),
    "quiz": [
        {"q": "An expert reviews a prototype against a checklist without any participants present. Which type of evaluation is this?",
         "options": ["A setting that does not directly involve users",
                     "A controlled setting involving users",
                     "A natural setting involving users",
                     "An in-the-wild study"], "correct": 0,
         "why": "The third type covers any setting that does not directly involve users, where consultants and "
                "researchers critique prototypes and may predict and model success. The other three options all "
                "require participants."},
        {"q": "A task completes reliably in a silent lab but fails on a crowded bus. Which consideration does this expose?",
         "options": ["Ecological validity", "Reliability", "Scope", "Bias"], "correct": 0,
         "why": "Ecological validity asks whether the environment of the evaluation distorts the results. "
                "Reliability is about repeatability across occasions, scope is about generalizability of the "
                "findings, and bias is about distortion introduced by the process or the people."},
        {"q": "Which is a moderator's rule rather than a tester's?",
         "options": ["Ask questions starting with &quot;What&quot; or &quot;How&quot; if the tester becomes quiet",
                     "Think aloud",
                     "Be more than 100% honest about likes and dislikes",
                     "Remember it is not an IQ test"], "correct": 0,
         "why": "Asking What or How when the tester goes quiet is a moderator rule, alongside acting as a tour "
                "guide, interrupting only when necessary and not answering questions. The other three are the "
                "tester's rules."},
        {"q": "The Aware Home (Abowd et al., 2000) is an example of what?",
         "options": ["A living lab", "A usability lab",
                     "A crowdsourced remote test", "An inspection method"], "correct": 0,
         "why": "The Aware Home was embedded with a complex network of sensors and audio/video recording devices and "
                "is the deck's example of a living lab - evaluating everyday technology use where a usability lab "
                "would be too difficult."},
        {"q": "Which of these is a NON-LEADING task instruction?",
         "options": ["&quot;Try to buy plane tickets for your family vacation&quot;",
                     "&quot;Press the red button and then click the top-right airplane icon&quot;",
                     "&quot;Use the search box at the top of the page to find flights&quot;",
                     "&quot;Click Book Now, then select Return&quot;"], "correct": 0,
         "why": "Only the first states a goal without naming the interface elements. The other three tell the user "
                "where to look and what to press, which is exactly the knowledge the test is meant to measure."},
        {"q": "Which statement matches the deck's closing key points?",
         "options": ["Testing with one user is better than none",
                     "Testing should only begin once the product is complete",
                     "What users say is more reliable than what they do",
                     "Evaluation is separate from the design process"], "correct": 0,
         "why": "The closing points state that testing with one user beats none, that testing can be done at any "
                "stage, that the user's action speaks louder than words, and that evaluation and design are closely "
                "integrated in user-centered design. The other three options reverse each of those."},
    ],
    "lab": [
        ("Design a usability test session for a new pharmacy app. Specify the type of evaluation, three task instructions and the roles.",
         "<b>Type:</b> a controlled setting that directly involves users, so conditions are the same for every "
         "participant and errors and times are comparable - complemented later by a field study, since the two "
         "complement each other. <b>Tasks (goal-oriented, non-leading):</b> (1) &quot;You need to refill a "
         "prescription you collected last month - do that.&quot; (2) &quot;Find out whether this medicine can be "
         "taken with the one you already have.&quot; (3) &quot;What impression does this app give you compared with "
         "others you have used?&quot; None names a button or a screen. <b>Roles:</b> the <b>tester</b> thinks aloud, "
         "is more than honest about likes, dislikes and difficulty, is reminded it is not an IQ test, and is invited "
         "to suggest improvements; the <b>moderator</b> acts as a tour guide, interrupts only when necessary, never "
         "answers the tester's questions, and asks &quot;What are you thinking?&quot; or &quot;How would you expect "
         "that to work?&quot; during silences; the <b>observer</b> watches, listens and takes notes. Before any of "
         "it, an informed consent form tells participants why the study is happening, what they will do and what "
         "their rights are."),
        ("A colleague reports that 8 of 10 users rated the interface 4/5, so the redesign is a success. Critique this using the interpretation considerations.",
         "<b>Validity:</b> a satisfaction rating measures how users feel about the interface, not whether they could "
         "use it - if the study's objective was usability, the method does not measure what it was intended to "
         "measure. The deck's own rule applies: the <b>user's action speaks louder than words</b>, so completion "
         "rates, times and error counts should carry the finding, with the rating as supporting data. "
         "<b>Reliability:</b> would the same ratings appear on another occasion, or did the novelty of the redesign "
         "inflate them? <b>Ecological validity:</b> if the ratings came from a quiet lab, they may not survive the "
         "real setting. <b>Bias:</b> ratings given to the person who built the interface are systematically "
         "generous, which is one reason the moderator should not be the designer. <b>Scope:</b> ten participants "
         "cannot support a general claim about the user population. Report what the data supports and no more."),
        ("Explain why the same techniques appear in both the requirements and evaluation lectures, and what changes between them.",
         "Observation, interviews and questionnaires appear in both, because both activities need evidence about "
         "real users - but the deck stresses that they are <b>used differently</b>. In requirements the goal is to "
         "understand users, tasks and context in order to produce a stable set of requirements, so the questions are "
         "open and exploratory and the setting is the user's own world. In evaluation the goal is to judge a "
         "specific artifact - a conceptual model, an early prototype or a more complete one - against agreed "
         "usability and UX goals, so tasks are predefined and goal-oriented, conditions are held constant across "
         "participants where control is wanted, and performance is measured rather than described. The framing "
         "questions also change: evaluation asks why, what, where and when, and the answers span both natural and "
         "laboratory settings and continue after the product ships, where findings feed into new products."),
    ],
    "branches": [
        ("Introduction to evaluation",
         "Collecting information about users' or potential users' experiences with a prototype, system, application or design artifact, in order to improve design.",
         ["Evaluation is integral to the design process.",
          "It focuses on the usability of the system, such as how easy it is to learn and use.",
          "It also focuses on the user experience, such as how satisfying, enjoyable or motivating the interaction is.",
          "UXPA defines UX as an approach to product development incorporating direct user feedback throughout the development cycle.",
          "That definition frames human-centered design as a way to reduce costs as well as meet user needs."],
         [("The cost argument", "UX work is justified economically - direct feedback throughout development reduces the cost of building the wrong thing.")]),
        ("Why, what, where and when to evaluate",
         "Four framing questions for a continuous, iterative process of design and evaluation.",
         ["Why: to check users' requirements, that users can use the product, and that they like it.",
          "What: a conceptual model, early prototypes of a new system, and later more complete prototypes.",
          "Where: in natural and laboratory settings.",
          "When: throughout design, and on finished products to collect information that informs new products."],
         [("Evaluating a conceptual model", "Evaluation begins before any interface exists, which is why the what question starts with the model rather than the product.")]),
        ("Types of evaluation",
         "Three categories covering every method in the course.",
         ["Controlled settings that directly involve users, such as usability and research labs.",
          "Natural settings involving users, such as online communities and products used in public places.",
          "In natural settings there is often little or no control over what users do, especially in-the-wild.",
          "Any setting that does not directly involve users, where consultants and researchers critique prototypes.",
          "Methods without users may predict and model how successful a design will be.",
          "Living labs evaluate people's use of technology in their everyday lives where a usability lab would be too difficult.",
          "Usability testing and field studies complement each other."],
         [("The Aware Home", "Abowd et al. (2000) embedded a home with a complex network of sensors and audio/video recording devices."),
          ("City-scale living labs", "Verma et al. (2017) studied whole blocks and cities housing hundreds of people in Switzerland."),
          ("Citizen science", "Projects such as iNaturalist.com can be thought of as living labs, showing how the idea of a lab is changing.")]),
        ("Evaluation case studies",
         "Three contrasting studies showing the range of what evaluation can mean.",
         ["A classic experimental investigation into the physiological responses of players of a computer game.",
          "An ethnographic study of visitors at the Royal Highland Show, directed and tracked using a cell phone app.",
          "Crowdsourcing, in which the opinions and reactions of volunteers inform technology evaluation."],
         [("Physiological measures", "Measuring the body's response rather than asking the player extends evaluation beyond self-report."),
          ("Tracking with a phone app", "The app both directs visitors and records where they went, combining intervention with observation.")]),
        ("Task instructions",
         "Instructions for a usability test must be goal-oriented and non-leading.",
         ["A task-oriented instruction states the goal, such as getting a ticket to London on a certain date.",
          "A non-leading instruction is \"try to buy plane tickets for your family vacation\".",
          "A leading instruction names the controls, such as pressing the red button then clicking the airplane icon.",
          "Sample instructions ask for an impression compared with other sites, for suitable return flight times, for an attempted purchase, and for the luggage allowance."],
         [("Why leading fails", "Naming the button supplies the very knowledge the test exists to measure, so the session tests only the ability to follow directions.")]),
        ("Roles in testing",
         "Three roles with distinct rules, used in person or remotely through crowdsourcing.",
         ["The tester thinks aloud.",
          "The tester should be more than 100% honest about likes, dislikes and what is difficult or easy.",
          "The tester should remember it is not an IQ test, and should give suggestions.",
          "The moderator acts as a tour guide.",
          "The moderator interrupts only when necessary and does not answer questions for the tester.",
          "The moderator asks questions starting with What or How if the tester becomes quiet.",
          "The observer watches, listens and takes notes.",
          "Remote UX testing by crowdsourcing lets clients watch and listen, involving an observer and a tester."],
         [("Two room setups", "In-person testing can arrange tester, moderator and observer in more than one physical configuration, depending on space and intrusiveness."),
          ("Moderator restraint", "Every moderator rule is a restriction - the role is defined by what it does not do.")]),
        ("Ethics and consent",
         "Participants' rights and the informed consent process that protects them.",
         ["Participants must be told why the evaluation is being done and what they will be asked to do.",
          "Participants must be told their rights.",
          "Informed consent forms provide this information and act as a contract between participants and researchers.",
          "The design of the form, the evaluation process, the data analysis and the data storage methods are typically approved by a high authority such as an Institutional Review Board."],
         [("Consent as contract", "Framing the form as a contract makes explicit that obligations run in both directions, not only from participant to researcher.")]),
        ("Analysis and interpreting data",
         "Turning evaluation sessions into defensible findings.",
         ["Transcribe the sessions, capturing verbal content and actions from both tester and moderator.",
          "Analyze the transcript based on the objective of the evaluation, such as usability or user behaviour.",
          "Highlight other issues observed during the sessions.",
          "Report the findings.",
          "Quantitative analysis expresses results as numbers; qualitative analysis inquires into the reasoning behind human behaviour.",
          "Reliability asks whether the method produces the same results on separate occasions.",
          "Validity asks whether the method measures what it is intended to measure.",
          "Ecological validity asks whether the environment of the evaluation distorts the results.",
          "Biases ask whether the process distorts the results, and scope asks how generalizable they are."],
         [("Validity versus ecological validity", "A satisfaction rating may be a valid measure of feeling but an invalid measure of usability; a silent lab may distort a task designed for a noisy street.")]),
        ("Key points of evaluation",
         "The summary claims the deck itself makes about evaluation practice.",
         ["Evaluation and design are closely integrated in user-centered design.",
          "Some of the same techniques are used as for establishing requirements, but they are used differently.",
          "Three types of evaluation exist: laboratory based with users, in the field with users, and studies that do not involve users.",
          "The main methods are observing, asking users, asking experts, user testing, inspection, modeling users' task performance, and analytics.",
          "Dealing with constraints is an important skill for evaluators to develop.",
          "Test instructions should be goal oriented, and usability testing can be done easily.",
          "The user's action speaks louder than words, and testing can be done at any stage.",
          "You are not your user, and testing with one user is better than none."],
         [("Same technique, different use", "An interview in requirements explores an unknown world; an interview in evaluation probes a specific artifact against agreed goals."),
          ("One user beats none", "The rule exists to defeat the excuse that a proper study cannot be afforded.")]),
    ],
    "exam_mcq": [
        {"q": "Which of the following is the deck's stated reason for carrying out evaluation?",
         "options": ["To improve design", "To prove the requirements were correct",
                     "To satisfy a legal obligation", "To replace the need for requirements gathering"],
         "correct": 0,
         "why": "Evaluators collect information about users' experiences because it improves design. Evaluation does "
                "check requirements, but that is one of three purposes under 'why', not the overall reason, and it "
                "never replaces requirements work."},
        {"q": "&quot;Products used in public places and online communities, with little or no control over what users do&quot; describes which type of evaluation?",
         "options": ["Natural settings involving users", "Controlled settings involving users",
                     "Settings that do not involve users", "Inspection"],
         "correct": 0,
         "why": "That is the natural-settings type, which includes in-the-wild studies. Controlled settings are "
                "usability and research labs; settings without users involve experts critiquing prototypes; "
                "inspection is a specific method within that third type."},
        {"q": "Which question does RELIABILITY ask?",
         "options": ["Does the method produce the same results on separate occasions?",
                     "Does the method measure what it is intended to measure?",
                     "Does the environment distort the results?",
                     "How generalizable are the results?"],
         "correct": 0,
         "why": "Reliability is repeatability. The second is validity, the third is ecological validity, and the "
                "fourth is scope."},
        {"q": "Which is NOT one of the tester's four rules?",
         "options": ["Interrupt only when necessary", "Think aloud",
                     "Be more than 100% honest", "Remember it is not an IQ test"],
         "correct": 0,
         "why": "Interrupting only when necessary is a moderator rule. The tester thinks aloud, is more than honest "
                "about likes and difficulties, remembers it is not an IQ test, and gives suggestions."},
        {"q": "Which list gives the main evaluation methods as stated in the key points?",
         "options": ["Observing, asking users, asking experts, user testing, inspection, modeling task performance, analytics",
                     "Interviews, questionnaires, focus groups, ethnography",
                     "Heuristic evaluation, cognitive walkthrough, pluralistic walkthrough",
                     "Visceral, behavioural and reflective assessment"],
         "correct": 0,
         "why": "That seven-item list is the one given. Interviews, questionnaires, focus groups and ethnography are the requirements-gathering techniques; heuristic evaluation and the walkthroughs are the inspection methods from Lecture 13; and visceral, behavioural and reflective are Norman's emotional design levels."},
        {"q": "Informed consent forms are described as:",
         "options": ["A contract between participants and researchers",
                     "An optional courtesy for laboratory studies",
                     "A record kept only by the moderator",
                     "A substitute for institutional approval"],
         "correct": 0,
         "why": "They provide the information about why the study is happening, what participants will do and what "
                "their rights are, and act as a contract. Institutional approval by a body such as an IRB is "
                "additional, not replaced by the form."},
    ],
    "exam_short": [
        {"q": "Answer the why, what, where and when questions of evaluation.",
         "keywords": ["requirement", "prototyp", "natural", "throughout"],
         "answer": "<b>Why:</b> to check users' requirements, to check that users can use the product, and to check "
                   "that they like it. <b>What:</b> a conceptual model, early prototypes of a new system, and later "
                   "more complete prototypes. <b>Where:</b> in natural and in laboratory settings. <b>When:</b> "
                   "throughout design; finished products can also be evaluated to collect information that informs "
                   "new products. Together these make iterative design and evaluation a continuous process."},
        {"q": "Describe the three types of evaluation with an example of each.",
         "keywords": ["controlled", "natural", "without users", "lab"],
         "answer": "First, <b>controlled settings that directly involve users</b> - usability labs and research "
                   "labs, where conditions are held as constant as possible across participants. Second, "
                   "<b>natural settings involving users</b> - online communities and products used in public "
                   "places, where there is often little or no control over what users do, especially in in-the-wild "
                   "studies. Third, <b>any setting that does not directly involve users</b> - consultants and "
                   "researchers critique the prototypes and may predict and model how successful they will be. "
                   "Living labs sit between the first two: the Aware Home, whole city blocks, and citizen science "
                   "projects evaluate everyday use in realistic environments where a usability lab would be too "
                   "difficult."},
        {"q": "State the rules for each of the three roles in a usability test session.",
         "keywords": ["tester", "moderator", "observer", "aloud"],
         "answer": "<b>Tester:</b> think aloud; be more than 100% honest about likes and dislikes and about what is "
                   "difficult or easy; remember that it is not an IQ test; and give suggestions. <b>Moderator:</b> "
                   "act as a tour guide; interrupt only when necessary; do not answer questions for the tester; and "
                   "ask questions starting with &quot;What&quot; or &quot;How&quot; if the tester becomes quiet. "
                   "<b>Observer:</b> watch, listen and take notes. Testing may be conducted in person with these "
                   "three roles, or remotely through crowdsourcing, where clients can watch and listen and the "
                   "people involved are the observer and the tester."},
        {"q": "Explain reliability, validity, ecological validity, bias and scope.",
         "keywords": ["reliab", "valid", "ecolog", "scope"],
         "answer": "<b>Reliability</b> asks whether the method produces the same results on separate occasions. "
                   "<b>Validity</b> asks whether the method measures what it is intended to measure - a satisfaction "
                   "rating is not a valid measure of task performance. <b>Ecological validity</b> asks whether the "
                   "environment of the evaluation distorts the results - a task that succeeds in a silent lab may "
                   "fail on a crowded train. <b>Biases</b> asks whether anything in the process or the people "
                   "distorts the results. <b>Scope</b> asks how generalizable the results are - a study of ten "
                   "participants cannot support a claim about a whole population."},
        {"q": "Why must task instructions be non-leading, and give one leading and one non-leading example.",
         "keywords": ["leading", "goal", "instruction", "measur"],
         "answer": "Because a leading instruction supplies the very knowledge the test is meant to measure - if the "
                   "instruction names the button, the session tests only the participant's ability to follow "
                   "directions, not whether the interface can be understood. Instructions should therefore be "
                   "goal-oriented. <b>Leading:</b> &quot;Press the red button and then click the first top-right "
                   "button with an airplane icon.&quot; <b>Non-leading:</b> &quot;Try to buy plane tickets for your "
                   "family vacation.&quot;"},
        {"q": "Summarise the deck's key points about evaluation practice.",
         "keywords": ["integrated", "three types", "constraint", "your user"],
         "answer": "Evaluation and design are closely integrated in user-centered design. Some of the same "
                   "techniques used for establishing requirements - observation, interviews and questionnaires - are "
                   "used in evaluation, but differently. There are three types of evaluation: laboratory based with "
                   "users, in the field with users, and studies that do not involve users. The main methods are "
                   "observing, asking users, asking experts, user testing, inspection, modeling users' task "
                   "performance, and analytics. Dealing with constraints is an important skill for evaluators. "
                   "Finally: test instructions should be goal oriented; usability testing can be done easily; the "
                   "user's action speaks louder than words; testing can be done at any stage; you are not your user; "
                   "and testing with one user is better than none."},
    ],
})


LECTURES.append({
    "num": 12,
    "slug": "evaluation-decide-usability-testing-and-experiments",
    "title": "Evaluation: DECIDE, Usability Testing and Experiments",
    "short": "DECIDE & Experiments",
    "lecture_label": "Lecture 12",
    "theme": "trial",
    "accent": "#f06292",
    "accent2": "#7986ff",
    "tagline": "The DECIDE framework, usability testing versus research experiments, experimental design, and field studies.",
    "hero_title": "Determine. Explore. Choose.<br><em>Identify. Decide. Evaluate.</em>",
    "hero_sub": ("DECIDE is a checklist for planning an evaluation study. This lecture then separates "
                 "<b>usability testing</b> - applied experimentation to improve a product - from <b>experiments for "
                 "research</b>, which test hypotheses to discover new knowledge, and closes with field studies."),
    "badges": ["DECIDE framework", "Usability testing", "Testing vs research",
               "Experimental design", "Independent & dependent variables", "Field studies"],
    "outcomes": [
        "Explain the DECIDE framework and apply it to plan an evaluation.",
        "Explain how to do usability testing and what data it produces.",
        "Outline the basics of experimental design.",
        "Distinguish independent from dependent variables.",
        "Describe how to do field studies and why they matter.",
    ],
    "sections": [
        {
            "id": "decide",
            "kicker": "01 - THE DECIDE FRAMEWORK",
            "title": "Six steps for planning an evaluation study",
            "lead": "A framework to guide evaluation - and a useful checklist for planning any study.",
            "blocks": [
                ("steps", [
                    ("D - Determine the goals", "What are the high-level goals of the evaluation? Who wants it and why? The goals influence the methods used."),
                    ("E - Explore the questions", "Questions guide the evaluation, and high-level goals break down into sub-questions."),
                    ("C - Choose the evaluation methods", "The method influences how data is collected, analyzed and presented."),
                    ("I - Identify the practical issues", "How to select users, find evaluators, select equipment, stay on budget and stay on schedule."),
                    ("D - Decide how to deal with the ethical issues", "Develop an informed consent form and honour participants' rights."),
                    ("E - Evaluate, analyze, interpret and present the data", "Considering reliability, validity, biases, scope and ecological validity."),
                ]),
                ("cards", [
                    ("1. Determine the goals - what they might be",
                     "Identify the best metaphor for the design; check that user requirements are met; check for "
                     "consistency; investigate how technology affects working practices; improve the usability of an "
                     "existing product."),
                    ("2. Explore the questions - worked example",
                     "The goal of finding out <b>why some customers prefer paper airline tickets to e-tickets</b> "
                     "breaks into sub-questions: What are customers' attitudes to e-tickets? Are they concerned "
                     "about security? Is the interface for obtaining them poor?"),
                    ("3. Choose the methods - what follows",
                     "Field studies typically involve observation and interviews; involve users in natural settings; "
                     "do <b>not</b> involve controlled tests; and produce <b>qualitative</b> data."),
                    ("5. Ethical issues - participants' rights",
                     "To know the goals of the study; to know what will happen to the findings; to privacy of "
                     "personal information; to <b>leave when they wish</b>; and to be treated politely."),
                ]),
                ("hook", ("MEMORY HOOK",
                          "The acronym is the answer sheet: <b>D</b>etermine goals, <b>E</b>xplore questions, "
                          "<b>C</b>hoose methods, <b>I</b>dentify practical issues, <b>D</b>ecide on ethics, "
                          "<b>E</b>valuate and present. Note the shape - goals narrow into questions, questions "
                          "select methods, and everything else is execution.")),
                ("warn", ("THE ORDER MATTERS",
                          "Goals come <b>before</b> questions, and questions come <b>before</b> methods. Choosing "
                          "the method first - &quot;let's run a usability test&quot; - is the most common planning "
                          "error, and DECIDE exists to prevent it.")),
            ],
        },
        {
            "id": "usability-testing",
            "kicker": "02 - USABILITY TESTING",
            "title": "Recording performance of typical users doing typical tasks",
            "lead": ("Usability testing involves recording the performance of typical users doing typical tasks in "
                     "controlled settings. Users are observed and timed."),
            "blocks": [
                ("list", [
                    "Data is recorded on <b>video</b> and <b>key presses are logged</b>.",
                    "The data is used to calculate <b>performance times</b>, and to <b>identify and explain errors</b>.",
                    "<b>User satisfaction</b> is evaluated using questionnaires and interviews.",
                    "<b>Field observations</b> may be used to provide contextual understanding.",
                    "Goals and questions focus on <b>how well users perform tasks</b> with the product.",
                    "<b>Comparison</b> of products or prototypes is common.",
                    "The focus is on <b>time to complete a task</b> and the <b>number and type of errors</b>.",
                    "<b>Testing is central</b>; questionnaires and interviews provide data about users' opinions.",
                ]),
                ("table", (["Testing conditions", "Detail"], [
                    ["Setting", "A usability lab or other controlled space."],
                    ["Emphasis", "Selecting <b>representative users</b> and developing <b>representative tasks</b>."],
                    ["Participants", "<b>5-10 users</b> typically selected."],
                    ["Task length", "Usually no more than <b>30 minutes</b>."],
                    ["Consistency", "The test conditions should be <b>the same for every participant</b>."],
                    ["Ethics", "An informed consent form explains procedures and deals with ethical issues."],
                ])),
                ("cards", [
                    ("Types of data collected",
                     "Time to complete a task. Time to complete a task <b>after a specified time away</b> from the "
                     "product. Number and type of errors per task. Number of errors per unit of time. Number of "
                     "navigations to online help or manuals. Number of users making a particular error. Number of "
                     "users completing the task successfully."),
                    ("How many participants?",
                     "The number is a <b>practical issue</b>, depending on the schedule for testing, the "
                     "availability of participants and the cost of running tests. Typically <b>5-10</b>. Some "
                     "experts argue testing should continue <b>until no new insights are gained</b>."),
                    ("Equipment and remote testing",
                     "Usability labs have observers watching a user and an assistant. Portable equipment is used in "
                     "the field, including the <b>Tobii Glasses</b> mobile eye-tracking system. Remote usability "
                     "testing is also supported. Affordable remote testing systems are <b>more portable</b> than "
                     "usability labs, and many contain mobile eye-tracking and other devices."),
                ]),
                ("hook", ("MEMORY HOOK",
                          "Usability testing measures exactly two families of thing: <b>how long</b> and <b>how "
                          "wrong</b>. Every data type in the list is a variation on time or errors - plus help "
                          "lookups, which are a proxy for both.")),
            ],
        },
        {
            "id": "testing-vs-research",
            "kicker": "03 - TESTING VS RESEARCH",
            "title": "Applied experimentation, not science",
            "lead": ("Experiments test hypotheses to <b>discover new knowledge</b> by investigating the relationship "
                     "between two or more <b>variables</b>. <b>Usability testing is applied experimentation.</b>"),
            "blocks": [
                ("table", (["Usability testing", "Experiments for research"], [
                    ["Improve <b>products</b>.", "Discover <b>knowledge</b>."],
                    ["<b>Few</b> participants.", "<b>Many</b> participants."],
                    ["Results <b>inform design</b>.", "Results <b>validated statistically</b>."],
                    ["Usually <b>not completely replicable</b>.", "<b>Must be replicable</b>."],
                    ["Conditions controlled <b>as much as possible</b>.", "<b>Strongly controlled</b> conditions."],
                    ["<b>Procedure planned</b>.", "<b>Experimental design</b>."],
                    ["Results reported to <b>developers</b>.", "<b>Scientific report</b> to the scientific community."],
                ])),
                ("p", "In usability testing, developers check that the system is usable by the intended user "
                      "population for their tasks. Experiments may also be done <b>within</b> usability testing - "
                      "the two are not mutually exclusive, they differ in purpose, rigour and audience."),
                ("warn", ("THE SEVEN-ROW TABLE IS THE EXAM QUESTION",
                          "This comparison appears almost verbatim on exams. Learn it as seven contrasts - "
                          "<b>purpose, numbers, validation, replicability, control, planning, audience</b> - rather "
                          "than as fourteen separate facts.")),
            ],
        },
        {
            "id": "experiments",
            "kicker": "04 - EXPERIMENTS AND EXPERIMENTAL DESIGN",
            "title": "Variables, and the three participant designs",
            "lead": "An experiment tests a hypothesis by predicting the relationship between two or more variables.",
            "blocks": [
                ("table", (["Variable", "Definition"], [
                    ["<b>Independent variable</b>", "The one <b>manipulated by the researcher</b>."],
                    ["<b>Dependent variable</b>", "The one that <b>depends on</b> the independent variable."],
                ])),
                ("list", [
                    "Typical experimental designs have <b>one or two</b> independent variables.",
                    "Results are <b>validated statistically</b> and the study is <b>replicable</b>.",
                ]),
                ("cards", [
                    ("Different participants (between subjects)",
                     "A single group of participants is <b>allocated randomly</b> to the experimental conditions - "
                     "each person sees only one condition."),
                    ("Same participants (within subjects)",
                     "<b>All participants appear in both conditions</b>."),
                    ("Matched participants (pairwise)",
                     "Participants are <b>matched in pairs</b>, for example on expertise or gender, with one of each "
                     "pair in each condition."),
                ]),
                ("hook", ("MEMORY HOOK",
                          "<b>I</b>ndependent is what <b>I</b> change; <b>D</b>ependent is what <b>D</b>epends on it. "
                          "And the three designs: <b>different people, same people, matched people</b> - the whole "
                          "distinction is who appears in which condition.")),
            ],
        },
        {
            "id": "field",
            "kicker": "05 - FIELD STUDIES",
            "title": "In the wild",
            "lead": ("Field studies are done in <b>natural settings</b>. <b>In the wild</b> is the term for "
                     "prototypes being used freely in natural settings."),
            "blocks": [
                ("p", "They aim to understand <b>what users do naturally</b> and how technology impacts them. In "
                      "product design they are used to:"),
                ("list", [
                    "Identify <b>opportunities</b> for new technology.",
                    "Determine <b>design requirements</b>.",
                    "Decide how best to <b>introduce</b> new technology.",
                    "<b>Evaluate</b> technology in use.",
                ]),
                ("note", ("THE UNEXPECTED FINDING",
                          "Sometimes the findings of a field study are <b>unexpected</b>, especially for in-the-wild "
                          "studies exploring how novel technologies are used by participants in their own homes, "
                          "places of work, or outside. That capacity for surprise is precisely what a controlled lab "
                          "study cannot deliver, and it is why the two complement each other.")),
                ("hook", ("MEMORY HOOK",
                          "Field studies do <b>four jobs across the whole lifecycle</b>: find the opportunity, "
                          "set the requirements, plan the rollout, evaluate the result. They are not only an "
                          "evaluation method - they bracket the entire process.")),
            ],
        },
    ],
    "mistakes": [
        ("Getting the DECIDE letters out of order or wrong.",
         "<b>D</b>etermine the goals, <b>E</b>xplore the questions, <b>C</b>hoose the evaluation methods, "
         "<b>I</b>dentify the practical issues, <b>D</b>ecide how to deal with ethical issues, <b>E</b>valuate, "
         "analyze, interpret and present the data."),
        ("Choosing a method before setting goals.",
         "The goals influence the methods used, and questions guide the evaluation. Method-first planning is the "
         "error DECIDE exists to prevent."),
        ("Swapping independent and dependent variables.",
         "The <b>independent</b> variable is manipulated by the researcher; the <b>dependent</b> variable depends on "
         "it. Typical designs have one or two independent variables."),
        ("Confusing between-subjects and within-subjects designs.",
         "<b>Different participants (between subjects)</b>: a single group allocated <b>randomly</b> to conditions. "
         "<b>Same participants (within subjects)</b>: all participants appear in <b>both</b> conditions. "
         "<b>Matched (pairwise)</b>: participants matched in pairs on expertise, gender and so on."),
        ("Treating usability testing as scientific research.",
         "Usability testing improves products, uses few participants, informs design, is usually not completely "
         "replicable, controls conditions as far as possible, follows a planned procedure and reports to developers. "
         "Research experiments discover knowledge, use many participants, are statistically validated and "
         "replicable, are strongly controlled, use experimental design and produce a scientific report."),
        ("Giving the wrong participant count.",
         "Typically <b>5-10 users</b>, with tasks usually lasting no more than <b>30 minutes</b>. The number is a "
         "practical issue driven by schedule, availability and cost; some experts say continue until no new insights "
         "are gained."),
        ("&quot;Field studies are just uncontrolled usability tests.&quot;",
         "They aim to understand what users do naturally and how technology impacts them, and are used to identify "
         "opportunities, determine requirements, decide how to introduce technology and evaluate it in use."),
    ],
    "cheat": (["Concept", "Shortest correct answer"], [
        ["DECIDE", "Determine goals, Explore questions, Choose methods, Identify practical issues, Decide on ethics, Evaluate and present."],
        ["Participants' rights", "Know the goals, know what happens to the findings, privacy of personal information, leave when they wish, be treated politely."],
        ["Usability testing", "Recording performance of typical users doing typical tasks in controlled settings; users observed and timed."],
        ["Data recorded", "Video and key-press logs, used to calculate performance times and identify and explain errors."],
        ["Testing focus", "Time to complete a task, and the number and type of errors."],
        ["Participants", "Typically 5-10; tasks usually no more than 30 minutes; conditions the same for everyone."],
        ["How many is enough", "A practical issue of schedule, availability and cost; some experts say continue until no new insights are gained."],
        ["Experiment", "Tests hypotheses to discover new knowledge by investigating the relationship between two or more variables."],
        ["Independent variable", "The variable manipulated by the researcher."],
        ["Dependent variable", "The variable that depends on the independent variable."],
        ["Between subjects", "Different participants; a single group allocated randomly to the conditions."],
        ["Within subjects", "Same participants; all appear in both conditions."],
        ["Matched pairs", "Participants matched in pairs, e.g. on expertise or gender."],
        ["Field studies", "Done in natural settings to understand what users do naturally and how technology impacts them."],
        ["In the wild", "Prototypes being used freely in natural settings."],
        ["Field study uses", "Identify opportunities, determine requirements, decide how to introduce technology, evaluate technology in use."],
    ]),
    "quiz": [
        {"q": "In DECIDE, what does the letter I stand for?",
         "options": ["Identify the practical issues", "Interpret the data",
                     "Involve the users", "Investigate the questions"], "correct": 0,
         "why": "I is identify the practical issues - selecting users, finding evaluators, selecting equipment, "
                "staying on budget and on schedule. Interpreting data belongs to the final E; the others are not "
                "steps in the framework."},
        {"q": "A researcher compares completion times for a menu design with two levels versus three. What is the DEPENDENT variable?",
         "options": ["Completion time", "The number of menu levels",
                     "The number of participants", "The order of conditions"], "correct": 0,
         "why": "The dependent variable depends on the independent one. Here the researcher manipulates the number "
                "of menu levels (independent) and measures completion time (dependent). Participant count and "
                "condition order are design decisions, not variables under test."},
        {"q": "All twelve participants try both interface versions. Which experimental design is this?",
         "options": ["Same participants (within subjects)", "Different participants (between subjects)",
                     "Matched participants (pairwise)", "A field study"], "correct": 0,
         "why": "Within subjects means all participants appear in both conditions. Between subjects allocates a "
                "single group randomly so each person sees one condition; matched pairs pairs people on "
                "characteristics such as expertise or gender."},
        {"q": "Which row correctly describes usability testing rather than research experimentation?",
         "options": ["Results inform design and are reported to developers",
                     "Results are validated statistically and reported to the scientific community",
                     "Conditions are strongly controlled and the study must be replicable",
                     "Many participants are recruited to support statistical power"], "correct": 0,
         "why": "Usability testing improves products with few participants, informs design, and reports to "
                "developers. The other three rows describe experiments for research: statistical validation, strong "
                "control and replicability, and many participants."},
        {"q": "Which is NOT listed among participants' rights in the DECIDE ethics step?",
         "options": ["The right to see other participants' results",
                     "The right to know the goals of the study",
                     "The right to leave when they wish",
                     "The right to privacy of personal information"], "correct": 0,
         "why": "The listed rights are to know the goals, to know what will happen to the findings, to privacy of "
                "personal information, to leave when they wish, and to be treated politely. Access to other "
                "participants' data would in fact violate the privacy right."},
        {"q": "What is the typical number of participants and task length in usability testing?",
         "options": ["5-10 participants, tasks usually no more than 30 minutes",
                     "20-30 participants, tasks of about an hour",
                     "3 participants, tasks of 10 minutes",
                     "50 participants, tasks of any length"], "correct": 0,
         "why": "The stated figures are 5-10 users with tasks usually lasting no more than 30 minutes, with the same "
                "conditions for every participant. The number is a practical issue of schedule, availability and "
                "cost."},
    ],
    "lab": [
        ("Apply the full DECIDE framework to plan an evaluation of a new hospital medication-ordering screen.",
         "<b>D - Determine the goals:</b> improve the usability of the ordering screen and check that safety "
         "requirements are met; the goals come from the clinical safety lead, and they push the study towards "
         "performance measurement rather than opinion. <b>E - Explore the questions:</b> can a resident complete a "
         "first order unaided? Where do dosing errors occur? Does the confirmation step actually get read? "
         "<b>C - Choose the methods:</b> usability testing in a controlled setting for the performance measures, "
         "complemented by a short field observation for contextual understanding, since field studies do not involve "
         "controlled tests and produce qualitative data. <b>I - Identify practical issues:</b> recruit "
         "representative users across residents and consultants, find evaluators, book a quiet room with video and "
         "logging, and keep tasks under 30 minutes to fit clinical schedules. <b>D - Decide on ethics:</b> an "
         "informed consent form covering the goals, what happens to the findings, privacy of personal information, "
         "the right to leave at any time and polite treatment; approval from the appropriate review board. "
         "<b>E - Evaluate, analyze, interpret and present:</b> report completion rates, times and error types with "
         "explicit statements about reliability, validity, ecological validity, biases and scope - five to ten "
         "participants cannot support a population-level safety claim."),
        ("A team runs the same twelve participants through two search interfaces, always A then B. Identify the design, the risk, and two fixes.",
         "The design is <b>same participants (within subjects)</b> - all participants appear in both conditions. The "
         "risk is that the order itself becomes an uncontrolled variable: by the time participants reach B they know "
         "the task, the vocabulary and the dataset, so B benefits from practice regardless of its design, and the "
         "measured difference in completion time confounds interface with learning. <b>Fix 1:</b> counterbalance the "
         "order, with half the participants doing B then A, which keeps the statistical power of a within-subjects "
         "design while cancelling the practice effect. <b>Fix 2:</b> switch to <b>different participants (between "
         "subjects)</b>, allocating a single group randomly to the two conditions so nobody sees both - at the cost "
         "of needing more participants to detect the same difference. A third option is <b>matched pairs</b>, "
         "pairing participants on expertise so the groups are comparable without anyone repeating the task."),
        ("Explain why a field study can produce findings a usability test never would, and when you would still choose the lab.",
         "Field studies are done in natural settings, and in-the-wild studies let prototypes be used freely; they aim "
         "to understand what users do <b>naturally</b> and how technology impacts them. Because there is little or "
         "no control, users bring their own goals, interruptions, environments and workarounds, and the deck notes "
         "that findings are sometimes <b>unexpected</b>, particularly when novel technologies are used in "
         "participants' own homes, workplaces or outdoors. They also serve the whole lifecycle: identifying "
         "opportunities for new technology, determining design requirements, deciding how best to introduce it, and "
         "evaluating it in use. The lab is still the right choice when the question is comparative and "
         "performance-based - which of two designs is faster or produces fewer errors - because usability testing "
         "holds the conditions the same for every participant, records video and key presses, and yields "
         "comparable times and error counts that a natural setting cannot. The two complement each other rather "
         "than compete."),
    ],
    "branches": [
        ("The DECIDE framework",
         "A six-step framework to guide the planning of an evaluation study.",
         ["Determine the goals: what the high-level goals are, who wants the evaluation and why, since goals influence the methods used.",
          "Goals may be to identify the best metaphor, check user requirements are met, check for consistency, investigate how technology affects working practices, or improve usability of an existing product.",
          "Explore the questions: questions guide the evaluation and high-level goals break into sub-questions.",
          "Choose the evaluation methods, since the method influences how data is collected, analyzed and presented.",
          "Identify the practical issues: selecting users, finding evaluators, selecting equipment, staying on budget and on schedule.",
          "Decide how to deal with ethical issues by developing an informed consent form.",
          "Participants have the right to know the goals of the study, to know what will happen to the findings, to privacy of personal information, to leave when they wish, and to be treated politely.",
          "Evaluate, interpret and present the data considering reliability, validity, biases, scope and ecological validity."],
         [("The e-ticket example", "The goal of finding out why some customers prefer paper tickets breaks into sub-questions about attitudes, security concerns and whether the interface is poor."),
          ("What a method commits you to", "Choosing a field study commits you to observation and interviews with users in natural settings, no controlled tests, and qualitative data.")]),
        ("Usability testing",
         "Recording the performance of typical users doing typical tasks in controlled settings, where users are observed and timed.",
         ["Data is recorded on video and key presses are logged.",
          "The data is used to calculate performance times and to identify and explain errors.",
          "User satisfaction is evaluated using questionnaires and interviews.",
          "Field observations may be used to provide contextual understanding.",
          "Goals and questions focus on how well users perform tasks with the product.",
          "Comparison of products or prototypes is common.",
          "The focus is on time to complete a task and the number and type of errors.",
          "Testing takes place in a usability lab or other controlled space, emphasising representative users and representative tasks.",
          "Typically 5-10 users are selected and tasks usually last no more than 30 minutes.",
          "Test conditions should be the same for every participant, and an informed consent form explains procedures and ethical issues.",
          "How many participants is a practical issue depending on schedule, availability and cost, and some experts argue testing should continue until no new insights are gained."],
         [("Types of data", "Time to complete a task, time after a period away from the product, errors per task, errors per unit of time, navigations to online help, users making a particular error, and users completing the task successfully."),
          ("Remote and portable testing", "Affordable remote testing systems are more portable than usability labs, and many include mobile eye-tracking devices such as Tobii Glasses.")]),
        ("Usability testing versus research experiments",
         "Both are experimental in character, but they differ in purpose, scale, rigour and audience.",
         ["Usability testing improves products; experiments for research discover knowledge.",
          "Usability testing uses few participants; research uses many.",
          "Usability testing results inform design; research results are validated statistically.",
          "Usability testing is usually not completely replicable; research must be replicable.",
          "Usability testing controls conditions as much as possible; research uses strongly controlled conditions.",
          "Usability testing follows a planned procedure; research follows an experimental design.",
          "Usability testing results are reported to developers; research produces a scientific report for the scientific community.",
          "Usability testing is applied experimentation, and experiments may also be done within usability testing."],
         [("Applied experimentation", "Developers check that the system is usable by the intended user population for their tasks, rather than testing a general hypothesis about people.")]),
        ("Experiments and experimental design",
         "Testing a hypothesis by predicting the relationship between two or more variables.",
         ["The independent variable is manipulated by the researcher.",
          "The dependent variable depends on the independent variable.",
          "Typical experimental designs have one or two independent variables.",
          "Experiments are validated statistically and are replicable.",
          "Different participants, or between subjects, allocates a single group randomly to the experimental conditions.",
          "Same participants, or within subjects, means all participants appear in both conditions.",
          "Matched participants, or pairwise, matches participants in pairs on characteristics such as expertise or gender."],
         [("Order effects", "In a within-subjects design the second condition benefits from practice unless the order is counterbalanced."),
          ("Why match", "Pairing participants on expertise makes two groups comparable without anyone having to repeat the task.")]),
        ("Field studies",
         "Evaluation studies carried out in natural settings to discover how people interact with technology in the real world.",
         ["In the wild is the term for prototypes being used freely in natural settings.",
          "Field studies aim to understand what users do naturally and how technology impacts them.",
          "They identify opportunities for new technology.",
          "They determine design requirements.",
          "They help decide how best to introduce new technology.",
          "They evaluate technology in use.",
          "Findings are sometimes unexpected, especially in-the-wild studies of novel technologies in participants' homes, workplaces or outdoors."],
         [("Whole-lifecycle role", "Field studies bracket the process: they find the opportunity before design starts and evaluate the result after it ships."),
          ("Value of surprise", "A controlled study can only answer the question it was designed around; a field study can reveal that the question was wrong.")]),
    ],
    "exam_mcq": [
        {"q": "What does the first D in DECIDE stand for?",
         "options": ["Determine the goals", "Decide the ethical issues",
                     "Design the experiment", "Describe the users"],
         "correct": 0,
         "why": "The first D is determine the goals; the second D is decide how to deal with the ethical issues. "
                "Designing an experiment and describing users are not steps in the framework."},
        {"q": "Which statement about the independent variable is correct?",
         "options": ["It is manipulated by the researcher",
                     "It is measured as the outcome of the study",
                     "It is held constant across all conditions",
                     "It is the number of participants recruited"],
         "correct": 0,
         "why": "The independent variable is the one the researcher manipulates; the dependent variable is what "
                "depends on it and is measured. Variables held constant are controls, and participant count is a "
                "design decision."},
        {"q": "A study allocates a single group of participants randomly to two conditions, so each person sees only one. This is:",
         "options": ["Different participants (between subjects)", "Same participants (within subjects)",
                     "Matched participants (pairwise)", "A pluralistic walkthrough"],
         "correct": 0,
         "why": "Random allocation of one group to conditions, with each person in one condition, is the "
                "between-subjects design. Within subjects has everyone in both conditions; matched pairs pairs "
                "participants on characteristics; a pluralistic walkthrough is an inspection method."},
        {"q": "Which is a stated use of field studies in product design?",
         "options": ["Identifying opportunities for new technology",
                     "Statistically validating a hypothesis",
                     "Holding conditions constant across participants",
                     "Replacing informed consent with observation"],
         "correct": 0,
         "why": "Field studies identify opportunities, determine design requirements, decide how best to introduce "
                "technology, and evaluate technology in use. Statistical validation and constant conditions belong "
                "to controlled experiments, and consent is required regardless of setting."},
        {"q": "Which of these data types would a usability test typically collect?",
         "options": ["Number of navigations to online help or manuals",
                     "The theoretical basis of the users' mental models",
                     "The number of heuristics violated by the interface",
                     "The statistical significance of a population difference"],
         "correct": 0,
         "why": "Help navigations appear in the deck's list alongside completion times, error counts and success "
                "rates. Heuristic violations come from inspection methods, and population-level statistical claims "
                "belong to research experiments with many participants."},
        {"q": "Which describes the relationship between usability testing and experimentation?",
         "options": ["Usability testing is applied experimentation, and experiments may also be done within it",
                     "They are mutually exclusive approaches",
                     "Usability testing replaces experimentation in industry",
                     "Experiments are a subtype of field study"],
         "correct": 0,
         "why": "The deck states that usability testing is applied experimentation and that experiments may also be "
                "done in usability testing. Field studies are a separate category done in natural settings without "
                "controlled tests."},
    ],
    "exam_short": [
        {"q": "Explain the DECIDE framework, saying what each step involves.",
         "keywords": ["determine", "explore", "choose", "ethical"],
         "answer": "<b>Determine the goals</b> - establish the high-level goals of the evaluation, who wants it and "
                   "why, since the goals influence the methods used; they might be to identify the best metaphor, "
                   "check requirements are met, check consistency, investigate effects on working practices, or "
                   "improve an existing product's usability. <b>Explore the questions</b> - break the goals into "
                   "sub-questions that guide the evaluation. <b>Choose the evaluation methods</b> - the method "
                   "determines how data is collected, analyzed and presented. <b>Identify the practical issues</b> - "
                   "selecting users, finding evaluators, selecting equipment, staying on budget and on schedule. "
                   "<b>Decide how to deal with the ethical issues</b> - develop an informed consent form covering "
                   "participants' rights to know the goals, to know what happens to the findings, to privacy, to "
                   "leave when they wish and to be treated politely. <b>Evaluate, analyze, interpret and present the "
                   "data</b> - considering reliability, validity, biases, scope and ecological validity."},
        {"q": "Describe usability testing: what is recorded, what the focus is, and what conditions apply.",
         "keywords": ["typical", "video", "error", "controlled"],
         "answer": "Usability testing records the performance of typical users doing typical tasks in controlled "
                   "settings, with users observed and timed. Data is recorded on video and key presses are logged, "
                   "and this data is used to calculate performance times and to identify and explain errors. User "
                   "satisfaction is evaluated with questionnaires and interviews, and field observations may provide "
                   "contextual understanding. The focus is time to complete a task and the number and type of "
                   "errors, and comparison of products or prototypes is common. Testing takes place in a usability "
                   "lab or other controlled space, emphasising representative users and representative tasks; "
                   "typically 5-10 users are selected; tasks usually last no more than 30 minutes; test conditions "
                   "are the same for every participant; and an informed consent form explains procedures and ethical "
                   "issues."},
        {"q": "Compare usability testing with experiments for research across at least five dimensions.",
         "keywords": ["improve", "knowledge", "replicab", "statistic"],
         "answer": "Purpose: usability testing improves products, while experiments for research discover knowledge. "
                   "Participants: usability testing uses few, research uses many. Validation: testing results inform "
                   "design, research results are validated statistically. Replicability: testing is usually not "
                   "completely replicable, research must be replicable. Control: testing controls conditions as much "
                   "as possible, research uses strongly controlled conditions. Planning: testing follows a planned "
                   "procedure, research follows an experimental design. Audience: testing results go to developers, "
                   "research produces a scientific report for the scientific community. Usability testing is applied "
                   "experimentation, and experiments may also be done within usability testing."},
        {"q": "Define independent and dependent variables, and describe the three experimental participant designs.",
         "keywords": ["independent", "dependent", "between", "within"],
         "answer": "The <b>independent variable</b> is the one manipulated by the researcher; the <b>dependent "
                   "variable</b> is the one that depends on the independent variable. Typical experimental designs "
                   "have one or two independent variables, and results are validated statistically and are "
                   "replicable. <b>Different participants (between subjects):</b> a single group of participants is "
                   "allocated randomly to the experimental conditions, so each person experiences one condition. "
                   "<b>Same participants (within subjects):</b> all participants appear in both conditions. "
                   "<b>Matched participants (pairwise):</b> participants are matched in pairs, for example on "
                   "expertise or gender, with one of each pair in each condition."},
        {"q": "What is a field study, what does 'in the wild' mean, and what are field studies used for?",
         "keywords": ["natural", "wild", "opportunit", "requirement"],
         "answer": "A field study is an evaluation study carried out in natural settings, aiming to understand what "
                   "users do naturally and how technology impacts them. <b>In the wild</b> is the term for "
                   "prototypes being used freely in natural settings. In product design, field studies are used to "
                   "identify opportunities for new technology, determine design requirements, decide how best to "
                   "introduce new technology, and evaluate technology in use. Their findings are sometimes "
                   "unexpected, especially in in-the-wild studies exploring how novel technologies are used by "
                   "participants in their own homes, places of work, or outside."},
        {"q": "How many participants are enough for user testing, and what determines the answer?",
         "keywords": ["practical", "schedule", "availab", "insight"],
         "answer": "The number is a <b>practical issue</b> rather than a fixed rule. It depends on the schedule for "
                   "testing, the availability of participants and the cost of running tests. Typically 5-10 "
                   "participants are used, with tasks usually lasting no more than 30 minutes and the same "
                   "conditions applied to every participant. Some experts argue that testing should continue "
                   "<b>until no new insights are gained</b>, which makes the stopping point a property of the "
                   "findings rather than of the budget. This contrasts with experiments for research, which recruit "
                   "many participants because their results must be validated statistically."},
    ],
})


LECTURES.append({
    "num": 13,
    "slug": "evaluation-inspections-heuristics-and-walkthroughs",
    "title": "Evaluation: Inspections, Heuristics and Walkthroughs",
    "short": "Inspections & Walkthroughs",
    "lecture_label": "Lecture 13",
    "theme": "audit",
    "accent": "#63d2a2",
    "accent2": "#ffa94d",
    "tagline": "Evaluating without users: expert inspections, heuristic evaluation, cognitive and pluralistic walkthroughs, A/B testing.",
    "hero_title": "Methods that need<br><em>no users present.</em>",
    "hero_sub": ("Inspection methods use knowledge codified in <b>heuristics</b>, or models that predict users' "
                 "performance. An expert role-plays the users the product was designed for and identifies potential "
                 "usability problems using a set of guidelines."),
    "badges": ["Inspections", "Nielsen's revised heuristics", "3-stage process",
               "Cognitive walkthrough", "Pluralistic walkthrough", "A/B testing"],
    "outcomes": [
        "Describe the key concepts associated with inspection methods.",
        "Explain how to carry out a heuristic evaluation.",
        "Explain how to carry out cognitive and pluralistic walkthroughs.",
        "Turn design guidelines and golden rules into heuristics.",
        "Describe A/B testing and its ethical dilemmas.",
    ],
    "sections": [
        {
            "id": "inspections",
            "kicker": "01 - INSPECTIONS",
            "title": "Experts instead of users",
            "lead": ("Inspection methods typically involve an <b>expert role-playing the users</b> for whom the "
                     "product is designed, and identifying any potential usability problems by using a set of "
                     "guidelines. Users are <b>not required to be present</b>."),
            "blocks": [
                ("list", [
                    "Experts use their knowledge of <b>users and technology</b> to review software usability.",
                    "Expert critiques can be <b>formal or informal</b>.",
                    "They can be used at <b>any stage</b> of a design, and can <b>complement user testing</b>.",
                    "<b>Heuristic evaluation</b> is a review guided by a set of heuristics.",
                    "<b>Walkthroughs</b> involve stepping through a <b>pre-planned scenario</b>, noting potential "
                    "problems.",
                ]),
                ("note", ("WHAT INSPECTIONS CAN BE APPLIED TO",
                          "Inspections can be used to evaluate <b>requirements, mockups, functional prototypes, or "
                          "systems</b>. That breadth is the reason they can be used at any stage - there is nothing "
                          "they need that only a finished product provides.")),
            ],
        },
        {
            "id": "heuristic",
            "kicker": "02 - HEURISTIC EVALUATION",
            "title": "Nielsen's method, and the revised heuristics",
            "lead": ("A usability inspection method developed by Jakob Nielsen in the early 1990s, derived "
                     "<b>empirically from an analysis of 249 usability problems</b>. The heuristics have since been "
                     "revised for current technology by Nielsen and others - for mobile devices, wearables, virtual "
                     "worlds and more."),
            "blocks": [
                ("table", (["#", "Revised heuristic (2014)", "The one-line requirement"], [
                    ["1", "<b>Visibility of system status</b>", "The system should always keep users informed about what is going on."],
                    ["2", "<b>Match between system and real world</b>", "Follow real-world conventions, making information appear in natural and logical order."],
                    ["3", "<b>User control and freedom</b>", "Support undo and redo."],
                    ["4", "<b>Consistency and standards</b>", "Follow platform conventions."],
                    ["5", "<b>Error prevention</b>", "Present users with a confirmation option before they commit to the action."],
                    ["6", "<b>Recognition rather than recall</b>", "Minimize memory load by making objects, actions and options visible."],
                    ["7", "<b>Flexibility and efficiency of use</b>", "Cater to both inexperienced and experienced users."],
                    ["8", "<b>Aesthetic and minimalist design</b>", "Avoid information that is irrelevant."],
                    ["9", "<b>Help users recognize, diagnose and recover from errors</b>", "Error messages should precisely indicate the problem."],
                    ["10", "<b>Help and documentation</b>", "It may be necessary to provide help and documentation."],
                ])),
                ("steps", [
                    ("Briefing session", "Tell the experts what to do."),
                    ("Evaluation period of 1-2 hours", "Each expert works <b>separately</b>. One pass to get a feel for the product; a second pass to focus on specific features."),
                    ("Debriefing session", "Experts work <b>together</b> to <b>prioritize</b> the problems."),
                ]),
                ("cards", [
                    ("Budd (2007): heuristics for websites",
                     "A narrower set focused on key criteria: <b>clarity</b>; <b>minimize unnecessary complexity and "
                     "cognitive load</b>; <b>provide users with context</b>; and <b>promote a positive and "
                     "pleasurable user experience</b>."),
                    ("Turning guidelines into heuristics (Granollers, 2018)",
                     "Ask questions such as: &quot;Does the application include a visible title page, section or "
                     "site? Does the user always know where they are located? Does the user always know what the "
                     "system or application is doing? Are the links clearly defined? Can all actions be visualized "
                     "directly (i.e., no other actions are required)?&quot; Design guidelines and golden rules can "
                     "be <b>converted into heuristics</b> this way."),
                ]),
                ("table", (["Advantages", "Problems"], [
                    ["<b>Few ethical and practical issues</b> to consider, because users are not involved.", "It can be difficult and expensive to <b>find experts</b>."],
                    ["Can be used at any stage and complements user testing.", "It <b>requires knowledge and experience</b> to apply heuristics."],
                    ["The best experts have knowledge of the <b>application domain and the users</b>.", "Trained usability experts are sometimes hard to find and can be expensive."],
                    ["", "You <b>should use multiple experts</b> and aggregate their results."],
                ])),
                ("warn", ("THE NUMBER-OF-EVALUATORS POINT",
                          "The deck's chart on evaluators versus problems found is the reason for the last row: one "
                          "expert finds only a fraction of the problems, so <b>multiple experts must be used and "
                          "their results aggregated</b>. That, plus the fact that user testing and heuristic "
                          "evaluation <b>may reveal different usability problems</b>, is why inspections complement "
                          "rather than replace testing.")),
                ("hook", ("MEMORY HOOK",
                          "The three stages are <b>brief &rarr; alone &rarr; together</b>. Experts work "
                          "<i>separately</i> during evaluation so they do not anchor on each other, and "
                          "<i>together</i> at debriefing so the problems get prioritised. Getting that "
                          "alone/together split the wrong way round is the classic mistake.")),
            ],
        },
        {
            "id": "cognitive-walkthrough",
            "kicker": "03 - COGNITIVE WALKTHROUGHS",
            "title": "Focused on ease of learning",
            "lead": ("A cognitive walkthrough focuses on <b>ease of learning</b>. The designer presents an aspect of "
                     "the design and usage scenarios; the expert is told the assumptions about the user population, "
                     "the context of use and the task details."),
            "blocks": [
                ("steps", [
                    ("The designer presents the design and scenarios", "Along with the assumptions about users, context and tasks."),
                    ("One or more experts walk through the design prototype with the scenario", "Step by step, in role."),
                    ("Experts are guided by 3 questions", "Asked at every step."),
                    ("Experts note problems as they work through", "The output is the list of noted problems."),
                ]),
                ("cards", [
                    ("The three questions",
                     "1. Will the <b>correct action be sufficiently evident</b> to the user? "
                     "2. Will the user <b>notice that the correct action is available</b>? "
                     "3. Will the user <b>associate and interpret the response</b> from the action correctly?"),
                    ("Pluralistic walkthrough",
                     "A variation on the cognitive walkthrough theme, performed by a <b>carefully managed team</b>. "
                     "The panel of experts <b>begins by working separately</b>, then there is a <b>managed "
                     "discussion</b> leading to <b>agreed decisions</b>. The approach lends itself well to "
                     "<b>participatory design</b>."),
                ]),
                ("hook", ("MEMORY HOOK",
                          "The three questions map onto the gulfs: questions 1 and 2 are the <b>gulf of "
                          "execution</b> (can they see what to do, and see that it is available?), question 3 is the "
                          "<b>gulf of evaluation</b> (can they read what happened?). Two out, one back.")),
                ("warn", ("SCOPE OF WALKTHROUGHS",
                          "Walkthroughs are <b>focused</b>, so they are suitable for evaluating <b>small parts</b> "
                          "of a product. Do not propose one to evaluate an entire system.")),
            ],
        },
        {
            "id": "ab",
            "kicker": "04 - A/B TESTING",
            "title": "A large-scale experiment",
            "lead": ("A/B testing offers another way to evaluate a website or an application running on a mobile "
                     "device, and is often used for evaluating design changes in social media applications."),
            "blocks": [
                ("list", [
                    "It is a <b>large-scale experiment</b>.",
                    "It <b>compares how two groups of users perform on two versions of a design</b>.",
                    "It can involve <b>thousands of users</b>.",
                    "It <b>may create ethical dilemmas if users don't know they are part of the test</b>.",
                    "<b>Care is needed</b> to ensure that other issues are not affecting users' behaviour.",
                ]),
                ("note", ("HOW IT CONNECTS BACK",
                          "A/B testing appeared in Lecture 5 as an online method for informing the choice between "
                          "alternatives, where setting appropriate metrics and choosing user group sets was called "
                          "nontrivial. Here it returns as a form of large-scale experiment - the same technique seen "
                          "from the evaluation side rather than the design-choice side.")),
                ("warn", ("THE ETHICS LINE",
                          "The dilemma is <b>consent</b>. Every other method in this course obtains informed consent, "
                          "which tells participants why the study is happening, what they will do and what their "
                          "rights are. A/B test participants typically know none of that, which is exactly why the "
                          "deck flags it.")),
            ],
        },
        {
            "id": "keypoints",
            "kicker": "05 - KEY POINTS",
            "title": "What this deck wants you to walk away with",
            "lead": "Five statements, all directly examinable.",
            "blocks": [
                ("list", [
                    "Inspections can be used to evaluate <b>requirements, mockups, functional prototypes, or "
                    "systems</b>.",
                    "<b>User testing and heuristic evaluation may reveal different usability problems.</b>",
                    "<b>Design guidelines can be used to develop heuristics.</b>",
                    "<b>Walkthroughs are focused</b>, so they are suitable for evaluating <b>small parts</b> of a "
                    "product.",
                    "<b>A/B testing is a form of large-scale experiment.</b>",
                ]),
                ("note", ("THE DISCUSSION THE DECK LEAVES OPEN",
                          "After the heuristic-evaluation activity the slides ask two questions worth having an "
                          "answer for: do the heuristics help you focus on a website more intently than you would "
                          "without them, and - if the activity was done on a smartphone - were <b>all</b> the "
                          "heuristics relevant and useful? The expected observation is that heuristics act as a "
                          "structured attention device, and that some general heuristics fit small-screen contexts "
                          "poorly, which is precisely why the set has been revised for mobile devices, wearables and "
                          "virtual worlds.")),
            ],
        },
    ],
    "mistakes": [
        ("Having the experts work together during the evaluation period.",
         "In heuristic evaluation each expert works <b>separately</b> during the 1-2 hour evaluation period, taking "
         "one pass for a feel and a second pass for specific features. They work <b>together</b> only in the "
         "<b>debriefing</b> session, to prioritize problems."),
        ("Using a single expert.",
         "The biggest problem list ends with <b>should use multiple experts and aggregate their results</b>, because "
         "one evaluator finds only a fraction of the problems."),
        ("&quot;Heuristic evaluation replaces user testing.&quot;",
         "User testing and heuristic evaluation <b>may reveal different usability problems</b>. Inspections "
         "<b>complement</b> user testing; they do not substitute for it."),
        ("Getting the three cognitive-walkthrough questions wrong.",
         "1. Will the correct action be sufficiently evident? 2. Will the user notice that the correct action is "
         "available? 3. Will the user associate and interpret the response from the action correctly?"),
        ("Proposing a walkthrough to evaluate a whole system.",
         "Walkthroughs are <b>focused</b>, so they suit <b>small parts</b> of a product."),
        ("Forgetting the A/B testing ethical issue.",
         "It may create ethical dilemmas <b>if users don't know they are part of the test</b>, and care is needed to "
         "ensure other issues are not affecting behaviour."),
        ("Treating the heuristics as fixed since 1990.",
         "They were derived empirically from an analysis of <b>249 usability problems</b> and have been "
         "<b>revised</b> for current technology - mobile devices, wearables, virtual worlds - by Nielsen and others."),
    ],
    "cheat": (["Concept", "Shortest correct answer"], [
        ["Inspection methods", "An expert role-plays the users and identifies potential usability problems using a set of guidelines; no users present."],
        ["What inspections evaluate", "Requirements, mockups, functional prototypes, or systems - at any stage."],
        ["Heuristic evaluation", "A usability inspection developed by Nielsen in the early 1990s, derived empirically from an analysis of 249 usability problems."],
        ["Three stages", "Briefing session; 1-2 hour evaluation with experts working separately (one pass for feel, one for features); debriefing to prioritize problems together."],
        ["Advantages", "Few ethical and practical issues because users are not involved; usable at any stage; complements user testing."],
        ["Problems", "Experts are difficult and expensive to find; applying heuristics requires knowledge and experience; multiple experts must be used and results aggregated."],
        ["Budd (2007) web heuristics", "Clarity; minimize unnecessary complexity and cognitive load; provide users with context; promote a positive and pleasurable user experience."],
        ["Cognitive walkthrough", "An inspection focused on ease of learning, stepping through a design prototype with a usage scenario."],
        ["The 3 questions", "Will the correct action be sufficiently evident? Will the user notice it is available? Will the user associate and interpret the response correctly?"],
        ["Pluralistic walkthrough", "A managed team variation: experts begin separately, then a managed discussion leads to agreed decisions; suits participatory design."],
        ["Walkthrough scope", "Focused, so suitable for evaluating small parts of a product."],
        ["A/B testing", "A large-scale experiment comparing how two groups perform on two versions of a design; can involve thousands of users."],
        ["A/B ethics", "May create dilemmas if users do not know they are part of the test."],
    ]),
    "quiz": [
        {"q": "During which stage of a heuristic evaluation do the experts work together?",
         "options": ["The debriefing session, to prioritize problems",
                     "The briefing session, to agree the heuristics",
                     "The first pass of the evaluation period",
                     "They never work together"], "correct": 0,
         "why": "Experts work separately throughout the 1-2 hour evaluation period, then come together in the "
                "debriefing session to prioritize the problems found. The briefing session tells them what to do "
                "rather than involving joint evaluation."},
        {"q": "&quot;Will the user notice that the correct action is available?&quot; belongs to which method?",
         "options": ["Cognitive walkthrough", "Heuristic evaluation",
                     "Pluralistic walkthrough only", "A/B testing"], "correct": 0,
         "why": "It is the second of the three questions guiding a cognitive walkthrough. A pluralistic walkthrough "
                "is a team variation on the same theme rather than the source of the questions, heuristic evaluation "
                "uses the ten heuristics, and A/B testing compares performance across two live versions."},
        {"q": "Nielsen's heuristics were originally derived from what?",
         "options": ["An empirical analysis of 249 usability problems",
                     "A survey of 249 usability experts",
                     "The ISO 9241 standard",
                     "Shneiderman's eight golden rules"], "correct": 0,
         "view": "",
         "why": "They were derived empirically from an analysis of 249 usability problems in the early 1990s, and "
                "were later revised for current technology such as mobile devices, wearables and virtual worlds."},
        {"q": "Which is listed as an ADVANTAGE of heuristic evaluation?",
         "options": ["Few ethical and practical issues, because users are not involved",
                     "It guarantees all usability problems will be found",
                     "It requires no knowledge or experience to apply",
                     "It is always cheaper than user testing"], "correct": 0,
         "view": "",
         "why": "Not involving users removes most ethical and practical issues. Applying heuristics explicitly "
                "requires knowledge and experience, multiple experts are needed because one finds only a fraction of "
                "problems, and finding trained experts can be difficult and expensive."},
        {"q": "Which set of criteria is Budd's (2007) website heuristics?",
         "options": ["Clarity; minimize complexity and cognitive load; provide context; promote a positive and pleasurable UX",
                     "Visibility; feedback; constraints; consistency; affordance",
                     "Learnability; flexibility; robustness",
                     "Where am I? Where can I go? What's here?"], "correct": 0,
         "why": "Those four are Budd's criteria. Visibility, feedback, constraints, consistency and affordance are Norman's design principles from Lecture 1; learnability, flexibility and robustness are Dix's usability principles from Lecture 8; and the three where-am-I questions are Veen's web principles from Lecture 4."},
        {"q": "What makes A/B testing ethically distinctive among the methods in this course?",
         "options": ["Users typically do not know they are part of the test",
                     "It requires participants to be paid",
                     "It cannot be approved by a review board",
                     "It always reveals personal data"], "correct": 0,
         "why": "Every other method obtains informed consent telling participants why the study is happening, what "
                "they will do and what their rights are; A/B test participants usually know none of this, which is "
                "the dilemma the deck flags. Payment, approval and personal data are not the stated issue."},
    ],
    "lab": [
        ("Plan a heuristic evaluation of a mobile banking app, specifying the process, the heuristics and the staffing.",
         "<b>Process - three stages.</b> A <b>briefing session</b> tells the experts what to do, gives them the "
         "assumptions about the user population and the context of use, and fixes the heuristic set. An "
         "<b>evaluation period of 1-2 hours</b> in which each expert works <b>separately</b>, taking one pass to get "
         "a feel for the product and a second pass to focus on specific features. A <b>debriefing session</b> in "
         "which the experts work <b>together</b> to prioritize the problems found. <b>Heuristics:</b> use Nielsen's "
         "revised 2014 set, but note the deck's own discussion question - not all general heuristics are relevant "
         "and useful on a smartphone, which is why revised sets exist for mobile devices; supplement with Budd's "
         "web criteria of clarity, minimizing complexity and cognitive load, providing context and promoting a "
         "positive experience. Design guidelines can be turned into heuristics with Granollers-style questions such "
         "as &quot;does the user always know where they are located?&quot;. <b>Staffing:</b> multiple experts, "
         "because a single evaluator finds only a fraction of the problems and results must be aggregated; the best "
         "experts have knowledge of both the application domain and the users - so recruit at least one with banking "
         "domain knowledge. Finally, plan user testing alongside it, because the two may reveal different usability "
         "problems."),
        ("Run a cognitive walkthrough, in writing, over a single step: a user must change their delivery address before checkout.",
         "<b>Setup:</b> the designer presents the checkout prototype and the scenario, and the expert is told the "
         "assumptions - first-time customer, on a phone, in a hurry. <b>Step: locate the address change.</b> "
         "<i>Q1 - Will the correct action be sufficiently evident?</i> No: the address appears as plain text with no "
         "affordance suggesting it can be edited, so the user has no cue that changing it is even possible here. "
         "<i>Q2 - Will the user notice that the correct action is available?</i> No: the Edit control sits below the "
         "fold on a phone, so it is not merely unlabelled but unseen - a visibility failure distinct from the "
         "affordance failure in Q1. <i>Q3 - Will the user associate and interpret the response correctly?</i> "
         "Partially: tapping Edit opens a full-page form with no indication that the checkout is preserved, so the "
         "user may believe they have left the purchase. <b>Note the scope:</b> this is one small part of the "
         "product, which is exactly what walkthroughs are suitable for."),
        ("A product manager wants to skip user testing because two experts already ran a heuristic evaluation. Respond.",
         "The two are complementary, not interchangeable. The deck states plainly that <b>user testing and heuristic "
         "evaluation may reveal different usability problems</b>: an expert role-plays the intended user using "
         "codified guidelines, which catches violations of known principles, but cannot produce the behaviour of "
         "real users pursuing their own goals - the completion rates, task times, error types and unexpected "
         "workarounds that usability testing records on video and in key-press logs. Inspections also have their own "
         "limits: applying heuristics requires knowledge and experience; the best experts need knowledge of the "
         "application domain and the users, and such people are difficult and expensive to find; and because one "
         "evaluator finds only a fraction of the problems, multiple experts must be used and their results "
         "aggregated - two may not be enough. The honest framing is that the inspection has cheaply removed a class "
         "of known problems at any stage of design, and that a small usability test with five to ten representative "
         "users on representative tasks is what will now reveal the problems the heuristics could not predict."),
    ],
    "branches": [
        ("Inspection methods",
         "Evaluation methods based on knowledge codified in heuristics, or models that predict users' performance, which do not require users to be present.",
         ["An expert typically role-plays the users for whom the product is designed.",
          "The expert identifies potential usability problems by using a set of guidelines.",
          "Experts use their knowledge of users and technology to review software usability.",
          "Expert critiques can be formal or informal.",
          "Inspections can be used at any stage of a design and can complement user testing.",
          "Inspections can evaluate requirements, mockups, functional prototypes, or systems.",
          "Heuristic evaluation is a review guided by a set of heuristics.",
          "Walkthroughs involve stepping through a pre-planned scenario noting potential problems."],
         [("Any stage", "Because inspections need only an artifact and an expert, they can begin at the requirements stage, long before anything runs."),
          ("Complementing testing", "User testing and heuristic evaluation may reveal different usability problems, so neither substitutes for the other.")]),
        ("Heuristic evaluation",
         "A usability inspection method developed by Jakob Nielsen in the early 1990s, derived empirically from an analysis of 249 usability problems.",
         ["The heuristics have been revised for current technology by Nielsen and others, for mobile devices, wearables and virtual worlds.",
          "Visibility of system status: the system should always keep users informed about what is going on.",
          "Match between system and real world: follow real-world conventions in a natural and logical order.",
          "User control and freedom: support undo and redo.",
          "Consistency and standards: follow platform conventions.",
          "Error prevention: present users with a confirmation option before they commit to an action.",
          "Recognition rather than recall: minimize memory load by making objects, actions and options visible.",
          "Flexibility and efficiency of use: cater to both inexperienced and experienced users.",
          "Aesthetic and minimalist design: avoid information that is irrelevant.",
          "Help users recognize, diagnose and recover from errors: messages should precisely indicate the problem.",
          "Help and documentation: it may be necessary to provide help and documentation."],
         [("Revision for context", "The set has been re-cut for mobile, wearables and virtual worlds because not every general heuristic is relevant on a small screen."),
          ("Budd (2007)", "Website heuristics focus on clarity, minimizing unnecessary complexity and cognitive load, providing users with context, and promoting a positive and pleasurable user experience.")]),
        ("The three stages of heuristic evaluation",
         "A briefing session, an evaluation period, and a debriefing session.",
         ["The briefing session tells the experts what to do.",
          "The evaluation period lasts 1-2 hours.",
          "During the evaluation period each expert works separately.",
          "Each expert takes one pass to get a feel for the product.",
          "Each expert takes a second pass to focus on specific features.",
          "In the debriefing session the experts work together to prioritize problems."],
         [("Why separately", "Working alone during evaluation prevents experts anchoring on each other's findings, which would shrink the total set of problems found."),
          ("Why together at the end", "Prioritisation requires comparing severity across the whole aggregated list, which no single evaluator can do.")]),
        ("Advantages and problems of heuristic evaluation",
         "The trade-offs of an inspection method that dispenses with users.",
         ["There are few ethical and practical issues to consider because users are not involved.",
          "It can be difficult and expensive to find experts.",
          "The best experts have knowledge of the application domain and of the users.",
          "It requires knowledge and experience to apply heuristics.",
          "Trained usability experts can be hard to find and expensive.",
          "Multiple experts should be used and their results aggregated.",
          "Design guidelines and golden rules can be turned into heuristics by asking targeted questions."],
         [("Number of evaluators", "The deck's chart of evaluators against problems found is the argument for aggregating multiple experts rather than trusting one."),
          ("Granollers (2018)", "Questions such as whether the user always knows where they are located, and whether all actions can be visualized directly, convert guidelines into usable heuristics.")]),
        ("Cognitive walkthroughs",
         "An inspection method focused on ease of learning, in which experts step through a design prototype with a usage scenario.",
         ["The designer presents an aspect of the design and usage scenarios.",
          "The expert is told the assumptions about the user population, the context of use and the task details.",
          "One or more experts walk through the design prototype with the scenario.",
          "Experts are guided by three questions and note problems as they work through.",
          "Question 1: will the correct action be sufficiently evident to the user?",
          "Question 2: will the user notice that the correct action is available?",
          "Question 3: will the user associate and interpret the response from the action correctly?",
          "Walkthroughs are focused, so they are suitable for evaluating small parts of a product."],
         [("Mapping to the gulfs", "Questions 1 and 2 probe the gulf of execution and question 3 probes the gulf of evaluation."),
          ("Why ease of learning", "The three questions all concern a user meeting the step for the first time, which is what makes the method a learnability instrument.")]),
        ("Pluralistic walkthroughs",
         "A variation on the cognitive walkthrough theme performed by a carefully managed team.",
         ["The panel of experts begins by working separately.",
          "There is then a managed discussion that leads to agreed decisions.",
          "The approach lends itself well to participatory design.",
          "Other adaptations of basic cognitive walkthroughs also exist."],
         [("Participatory fit", "Because the discussion is managed toward agreed decisions, users and other stakeholders can sit on the panel alongside experts.")]),
        ("A/B testing",
         "A large-scale experiment offering another way to evaluate a website or an application running on a mobile device.",
         ["It is often used for evaluating changes in design on social media applications.",
          "It compares how two groups of users perform on two versions of a design.",
          "It can involve thousands of users.",
          "It may create ethical dilemmas if users do not know they are part of the test.",
          "Care is needed to ensure that other issues are not affecting users' behaviour."],
         [("Confounds", "A promotion, a news event or a seasonal peak running during the test can move the metric more than the design does."),
          ("Consent gap", "Every other method in the course obtains informed consent; A/B participants typically receive none, which is the dilemma flagged.")]),
    ],
    "exam_mcq": [
        {"q": "Which statement describes inspection methods correctly?",
         "options": ["An expert role-plays the users and identifies usability problems using guidelines, with no users present",
                     "Users are observed and timed performing typical tasks",
                     "Two groups of users are compared on two versions of a design",
                     "Participants are matched in pairs on expertise"],
         "correct": 0,
         "why": "That is the definition of inspection methods. Observing and timing users is usability testing, "
                "comparing two live versions is A/B testing, and matched pairs is an experimental participant "
                "design."},
        {"q": "How many usability problems were analysed to derive Nielsen's original heuristics?",
         "options": ["249", "10", "1,000", "56"],
         "correct": 0,
         "why": "The heuristics were derived empirically from an analysis of 249 usability problems in the early "
                "1990s. Ten is the number of heuristics that resulted, not the number of problems analysed."},
        {"q": "In the revised heuristics, which one is summarised as &quot;present users with a confirmation option before they commit to the action&quot;?",
         "options": ["Error prevention", "User control and freedom",
                     "Help users recognize, diagnose and recover from errors", "Visibility of system status"],
         "correct": 0,
         "why": "That is the revised wording of error prevention. User control and freedom is about supporting undo "
                "and redo; heuristic 9 concerns messages after an error has occurred; heuristic 1 concerns keeping "
                "users informed of what is going on."},
        {"q": "Which is the correct order of the three stages of heuristic evaluation?",
         "options": ["Briefing, evaluation with experts working separately, debriefing to prioritize together",
                     "Briefing, joint evaluation, individual reporting",
                     "Individual evaluation, briefing, debriefing",
                     "Debriefing, evaluation, briefing"],
         "correct": 0,
         "why": "Briefing tells the experts what to do; during the 1-2 hour evaluation each works separately, one "
                "pass for feel and one for features; the debriefing brings them together to prioritize."},
        {"q": "Which method is described as suitable for evaluating SMALL PARTS of a product?",
         "options": ["Walkthroughs", "A/B testing",
                     "Field studies", "Living lab evaluation"],
         "correct": 0,
         "why": "The key points state that walkthroughs are focused, so they are suitable for evaluating small parts "
                "of a product. A/B testing is large-scale, and field studies and living labs cover whole systems in "
                "natural settings."},
        {"q": "Which of Budd's (2007) website criteria is stated in the lecture?",
         "options": ["Minimize unnecessary complexity and cognitive load",
                     "Support undo and redo",
                     "Follow platform conventions",
                     "Design dialogs to yield closure"],
         "correct": 0,
         "why": "Budd's four criteria are clarity, minimizing unnecessary complexity and cognitive load, providing "
                "users with context, and promoting a positive and pleasurable user experience. Undo/redo and "
                "platform conventions are Nielsen heuristics 3 and 4; closure is Shneiderman's fourth golden rule."},
    ],
    "exam_short": [
        {"q": "What are inspection methods, and what can they be used to evaluate?",
         "keywords": ["expert", "role", "guideline", "prototyp"],
         "answer": "Inspection methods are based on understanding users through knowledge codified in heuristics, or "
                   "models that predict users' performance, and they do not require users to be present. They "
                   "typically involve an expert role-playing the users for whom the product is designed and "
                   "identifying potential usability problems by using a set of guidelines. Experts use their "
                   "knowledge of users and technology to review software usability, and expert critiques can be "
                   "formal or informal. They can be used at any stage of a design and can complement user testing. "
                   "They can be used to evaluate requirements, mockups, functional prototypes, or systems."},
        {"q": "Describe the three stages of a heuristic evaluation.",
         "keywords": ["briefing", "separately", "debriefing", "prioriti"],
         "answer": "First, a <b>briefing session</b> to tell the experts what to do. Second, an <b>evaluation "
                   "period of 1-2 hours</b> in which each expert works <b>separately</b>, taking one pass to get a "
                   "feel for the product and a second pass to focus on specific features - working alone prevents "
                   "the evaluators anchoring on each other and shrinking the total set of problems found. Third, a "
                   "<b>debriefing session</b> in which the experts work <b>together</b> to prioritize the problems, "
                   "since prioritisation requires comparing severity across the whole aggregated list."},
        {"q": "Give the advantages and problems of heuristic evaluation.",
         "keywords": ["ethical", "expert", "experience", "multiple"],
         "answer": "<b>Advantages:</b> there are few ethical and practical issues to consider because users are not "
                   "involved; the method can be used at any stage of design; and it complements user testing, since "
                   "the two may reveal different usability problems. <b>Problems:</b> it can be difficult and "
                   "expensive to find experts, and the best ones need knowledge of both the application domain and "
                   "the users; applying heuristics requires knowledge and experience; trained usability experts are "
                   "sometimes hard to find and can be expensive; and because a single evaluator finds only a "
                   "fraction of the problems, multiple experts should be used and their results aggregated."},
        {"q": "Explain the cognitive walkthrough method and state its three questions.",
         "keywords": ["learning", "scenario", "evident", "response"],
         "answer": "A cognitive walkthrough focuses on <b>ease of learning</b>. The designer presents an aspect of "
                   "the design together with usage scenarios, and the expert is told the assumptions about the user "
                   "population, the context of use and the task details. One or more experts then walk through the "
                   "design prototype with the scenario, guided by three questions and noting problems as they go: "
                   "1. Will the correct action be sufficiently evident to the user? 2. Will the user notice that the "
                   "correct action is available? 3. Will the user associate and interpret the response from the "
                   "action correctly? Because walkthroughs are focused, they suit evaluating small parts of a "
                   "product."},
        {"q": "What is a pluralistic walkthrough and how does it differ from a cognitive walkthrough?",
         "keywords": ["pluralistic", "team", "separately", "participatory"],
         "answer": "A pluralistic walkthrough is a variation on the cognitive walkthrough theme, performed by a "
                   "<b>carefully managed team</b> rather than by one or more experts working independently. The "
                   "panel of experts begins by working separately, and there is then a <b>managed discussion</b> "
                   "that leads to <b>agreed decisions</b>. Because the discussion is deliberately steered toward "
                   "agreement, the approach lends itself well to <b>participatory design</b>, where users and other "
                   "stakeholders can sit on the panel alongside experts. Other adaptations of the basic cognitive "
                   "walkthrough also exist."},
        {"q": "Describe A/B testing and its ethical dilemma.",
         "keywords": ["large-scale", "two", "thousands", "ethic"],
         "answer": "A/B testing is a <b>large-scale experiment</b> offering another way to evaluate a website or an "
                   "application running on a mobile device, and it is often used for evaluating changes in design on "
                   "social media applications. It compares how <b>two groups of users perform on two versions of a "
                   "design</b>, and can involve <b>thousands of users</b>. Two cautions apply. First, it may create "
                   "<b>ethical dilemmas if users do not know they are part of the test</b> - every other method in "
                   "the course obtains informed consent telling participants why the study is happening, what they "
                   "will do and what their rights are, and A/B participants typically receive none of that. Second, "
                   "care is needed to ensure that other issues are not affecting users' behaviour, since a "
                   "promotion, news event or seasonal peak can move the metric more than the design change does."},
    ],
})
