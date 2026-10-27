"""SE365 annotated slides — every Human–Computer Interaction lecture (Rogers, Sharp & Preece).

One module holds all the decks: each deck is a namespace class with DECK and ANN (and AUTO_SLIDES).
Slides without an ANN entry are shown without notes. See cs331_annotated/ch01_1_introduction.py for the ANN keys."""
from .common import DECKS, mcq, see, short, tf, tip, trap, trick


def deck(key, title, chapter, lede):
    slug, file, folder, _ = DECKS[key]
    return {'key': key, 'slug': slug, 'file': file, 'title': title, 'chapter': chapter,
            'pdf': '/academics/software-engineering/se365/slides/%s/' % folder, 'lede': lede}


USABILITY = 'Usability goals: effective, efficient, safe, having good utility, easy to learn (learnability), easy to remember (memorability).'
NORMAN = 'Norman’s design principles: visibility, feedback, constraints, consistency, affordance (and mapping).'


class intro:
    AUTO_SLIDES = True
    DECK = deck('d01', 'Introduction to Human–Computer Interaction', 'Lecture 1',
                'Good and bad design, what HCI and interaction design are and how they relate to UX, accessibility and '
                'inclusiveness, the process of interaction design, usability and user-experience goals, and Norman’s '
                'design principles (visibility, feedback, constraints, consistency, affordance).')
    ANN = {
        7: dict(notes=['Bad design ignores how people actually use things (the confusing vending machine, voice-mail system).']),
        13: dict(notes=['HCI: the design, evaluation and implementation of interactive computing systems for human use, and the study of the phenomena around them.']),
        25: dict(notes=['Interaction design: designing interactive products to support the way people communicate and interact in their everyday and working lives.']),
        29: dict(notes=['Interaction design is the umbrella; HCI, UX, human factors, cognitive ergonomics and others overlap with it.']),
        34: dict(notes=['User experience (UX): how a product behaves and is used by people in the real world: how they FEEL about it. You can’t design a UX, only design FOR one.'],
                 exam=[tf('Designers can design a user experience directly.', False, 'They design for a user experience.')], weight=3),
        39: dict(notes=['Accessibility: how far a product can be used by as many people as possible (including people with disabilities). Inclusiveness: being fair, open and equal to everyone.']),
        45: dict(notes=['Process: discover requirements → design alternatives → prototype → evaluate (iteratively, user-centred).'], seen=[see('d05', 9, 'the four activities')]),
        46: dict(notes=[USABILITY], tips=[tip(USABILITY)],
                 exam=[mcq('"How easy is it to remember how to use a system once learned?" is:', ['Memorability', 'Learnability', 'Utility', 'Efficiency'], 0, ''),
                       mcq('Preventing users from making serious errors relates to which usability goal?', ['Safety', 'Utility', 'Memorability', 'Efficiency'], 0, '')], weight=3),
        48: dict(notes=['UX goals are subjective: desirable (fun, satisfying, engaging) and undesirable (boring, frustrating).']),
        50: dict(notes=[NORMAN], tips=[tip(NORMAN)], weight=3),
        51: dict(notes=['Visibility: the more visible functions are, the more likely users will know what to do next.']),
        52: dict(notes=['Feedback: send back information about what action has been done (sound, highlighting, animation).'],
                 exam=[mcq('A button that changes colour and clicks when pressed demonstrates:', ['Feedback', 'Constraint', 'Affordance', 'Consistency'], 0, '')], weight=3),
        54: dict(notes=['Constraints: restrict the actions possible at a given moment (greyed-out menu options; physical shape).'],
                 exam=[mcq('Greying out unavailable menu items is an example of:', ['Constraints', 'Feedback', 'Visibility', 'Mapping'], 0, '')], weight=3),
        58: dict(notes=['Consistency: similar operations and elements for similar tasks (Ctrl+C everywhere). Internal (within an app) vs. external (across apps/devices).']),
        61: dict(notes=['Affordance: an attribute of an object that tells people how to use it (a button invites pushing). Real (physical) vs. perceived (on screen).'],
                 tips=[trap('Affordance is about what the object suggests; feedback is about what happens AFTER the action.')],
                 exam=[mcq('A door handle that "invites" pulling is an example of:', ['Affordance', 'Feedback', 'Constraint', 'Consistency'], 0, '')], weight=3),
    }


class cognition:
    AUTO_SLIDES = True
    DECK = deck('d02', 'Cognitive Aspects', 'Lecture 2',
                'What cognition is (fast vs. slow thinking), the cognitive processes (attention, perception, memory, '
                'learning, reading/speaking/listening, problem-solving) with design implications, and cognitive '
                'frameworks: mental models, the gulfs of execution and evaluation, information processing, distributed, '
                'external and embodied cognition.')
    ANN = {
        4: dict(notes=['Cognition: what goes on in our heads when we carry out everyday activities: thinking, remembering, learning, deciding, seeing, reading…']),
        5: dict(notes=['Fast thinking (experiential, automatic) vs. slow thinking (reflective, effortful).']),
        8: dict(notes=['Attention: selecting things to concentrate on; depends on clear goals and how information is displayed.']),
        12: dict(notes=['Multitasking hurts attention: heavy multitaskers are more easily distracted.']),
        19: dict(notes=['Perception: how information is acquired through the senses and turned into experiences. Use contrast, white space and grouping.']),
        26: dict(notes=['Memory: encoding, then retrieval. Context matters; the more attention and processing, the better remembered.']),
        31: dict(notes=['Recognition is easier than recall: GUIs show options so users recognize rather than remember commands.'],
                 tips=[trick('Menus and icons = recognition; command lines = recall.')],
                 exam=[mcq('Graphical menus are easier than command lines mainly because:', ['Recognition is easier than recall', 'They are faster to type', 'They use less memory', 'They need no learning at all'], 0, '')], weight=3),
        41: dict(notes=['Memory load: 7 ± 2 (Miller) is about short-term memory items, NOT a rule for menu length.'],
                 tips=[trap('Don’t use "7 ± 2" to limit menu items or tabs: the items are visible, so no recall is needed.')],
                 exam=[tf('Miller’s 7 ± 2 means menus should never have more than 7 items.', False, 'Menus rely on recognition, not short-term memory.')], weight=3),
        44: dict(notes=['Learning: people prefer learning by doing; design for exploration and undo.']),
        50: dict(notes=['Problem solving / planning / reasoning / decision-making: reflective cognition; show information needed for comparisons.']),
        54: dict(notes=['Mental model: a user’s internal model of how a system works; often wrong (turning the thermostat up higher heats faster).'],
                 exam=[mcq('Setting the thermostat to maximum to heat a room faster reflects a faulty:', ['Mental model', 'Affordance', 'Feedback loop', 'Constraint'], 0, '')], weight=3),
        62: dict(notes=['Gulf of execution: gap between what users want to do and what the system lets them do. Gulf of evaluation: gap between the system state and the user’s ability to interpret it.'],
                 exam=[mcq('Users can’t tell whether their file was saved. This is a gulf of:', ['Evaluation', 'Execution', 'Attention', 'Learning'], 0, '')], weight=3),
        64: dict(notes=['Information processing: mind as a series of stages: encode → compare → select response → execute.']),
        66: dict(notes=['Distributed cognition: cognition spread across people, tools and the environment (e.g. an air-traffic control team).']),
        69: dict(notes=['External cognition: using external representations (notes, calendars) to reduce memory load and do computational offloading.']),
        72: dict(notes=['Embodied interaction: thinking through the body and physical interaction.']),
    }


class emotion:
    AUTO_SLIDES = True
    DECK = deck('d03', 'Emotional Interaction', 'Lecture 3',
                'Emotions and the user experience, the three levels of emotional design (visceral, behavioral, '
                'reflective), expressive and frustrating interfaces and error messages, affective computing and emotion '
                'detection, persuasive technologies, and anthropomorphism.')
    ANN = {
        5: dict(notes=['Emotional interaction: what makes people feel happy, sad, annoyed, anxious, frustrated, and how that affects how they use a product.']),
        11: dict(notes=['Automatic (affect) responses are fast; conscious appraisal is slower and reflective.']),
        12: dict(notes=['Norman / Ortony: three levels: VISCERAL (looks and feel), BEHAVIORAL (use: usability), REFLECTIVE (meaning, self-image, memories).'],
                 tips=[trick('Visceral = first look; Behavioral = while using; Reflective = afterwards, what it says about me.')],
                 exam=[mcq('Buying a watch because of what it says about your status is at which level?', ['Reflective', 'Visceral', 'Behavioral', 'Automatic'], 0, '')], weight=3),
        16: dict(notes=['Expressive interfaces: colours, icons, sounds, animations that convey emotion and make interaction pleasurable.']),
        20: dict(notes=['Frustrating interfaces: gimmicks, vague error messages, too many steps, bad appearance.']),
        22: dict(notes=['Good error messages: say what went wrong and how to fix it, in plain language, without blaming the user.'],
                 exam=[mcq('Which is the best error message?', ['"Your password must be at least 8 characters. Please try again."', '"Error 0x80070057"', '"Invalid input!!!"', '"Fatal exception occurred"'], 0, '')], weight=3),
        28: dict(notes=['Affective computing: systems that recognize and express emotions (facial coding, voice, body signals).']),
        34: dict(notes=['Persuasive technologies: designed to change attitudes or behaviour (fitness trackers, energy displays, nudges).']),
        39: dict(notes=['Phishing exploits trust: emotional design can be used against users.']),
        41: dict(notes=['Anthropomorphism: giving human qualities to objects (cuddly robots, chatbots). Can make interaction enjoyable, but can also deceive or annoy.']),
    }


class interfaces:
    AUTO_SLIDES = True
    DECK = deck('d04', 'Interaction and Interfaces', 'Lecture 4',
                'Understanding the problem space (assumptions and claims), conceptual models and interface metaphors, the '
                'interaction types (instructing, conversing, manipulating, exploring, responding) and direct manipulation, '
                'then a tour of 20 interface types from command-based and WIMP to VR, mobile, speech, touch, '
                'tangible, wearable and brain–computer interfaces.')
    ANN = {
        5: dict(notes=['Problem space: understand what you are designing and why before how; make assumptions and claims explicit.']),
        6: dict(notes=['Assumption: something taken for granted that needs checking. Claim: something stated as true that is open to question.']),
        15: dict(notes=['Conceptual model: a high-level description of how a system is organized and operates: metaphors, concepts, relationships, mappings.']),
        18: dict(notes=['Interface metaphor: uses familiar knowledge (desktop, shopping cart, cards) to help users understand.'],
                 exam=[mcq('An online "shopping cart" is an example of:', ['An interface metaphor', 'A mental model', 'An affordance', 'A constraint'], 0, '')], weight=3),
        24: dict(notes=['Interaction types: instructing (commands), conversing (dialog), manipulating (direct manipulation), exploring (moving through space), responding (system takes the initiative).'],
                 exam=[mcq('Asking a voice assistant "What’s the weather?" is which interaction type?', ['Conversing', 'Instructing', 'Manipulating', 'Exploring'], 0, ''),
                       mcq('Dragging a file to the trash is:', ['Manipulating', 'Instructing', 'Conversing', 'Responding'], 0, '')], weight=3),
        32: dict(notes=['Direct manipulation (Shneiderman): visible objects, rapid reversible incremental actions, physical actions instead of commands. Easy to learn; can be slow for experts.']),
        40: dict(notes=['Command-based: powerful and fast for experts; hard to learn (recall).']),
        43: dict(notes=['WIMP: Windows, Icons, Menus, Pointer. GUI extends it with toolbars, dialog boxes, etc.']),
        62: dict(notes=['VR: computer-generated immersive environments; presence; risk of motion sickness.']),
        73: dict(notes=['Mobile: small screens, touch, context of use; keep it simple, big targets.']),
        77: dict(notes=['Speech interfaces: good for hands-busy situations; problems with recognition and long menus.']),
        83: dict(notes=['Touch: single and multi-touch gestures (swipe, pinch).']),
        97: dict(notes=['Tangible interfaces: physical objects coupled with digital representations.']),
        101: dict(notes=['AR overlays digital information on the real world; mixed reality blends both.'],
                  exam=[mcq('Overlaying directions on a live camera view of the street is:', ['Augmented reality', 'Virtual reality', 'A tangible interface', 'A command-based interface'], 0, '')], weight=3),
        112: dict(notes=['Natural user interfaces (NUIs): interact with speech, gestures, touch as we do with the physical world.']),
        113: dict(notes=['Choose the interface by the users, their tasks, context and the product’s goals, not by novelty.']),
    }


class process:
    AUTO_SLIDES = True
    DECK = deck('d05', 'The Process of Interaction Design', 'Lecture 5',
                'What interaction design involves, the problem space, degrees of user involvement, the user-centred '
                'approach, the four basic activities and lifecycle models (simple, Google design sprint, research and '
                'design), three key characteristics, and practical issues: users, needs, alternatives and choosing between them.')
    ANN = {
        6: dict(notes=['User involvement ranges from full-time members of the team to occasional consultation; involvement manages expectations and creates ownership.']),
        8: dict(notes=['User-centred approach: early focus on users and tasks, empirical measurement, iterative design.'],
                 exam=[mcq('Which is NOT a principle of user-centred design?', ['Design once, test at the end', 'Early focus on users and tasks', 'Empirical measurement', 'Iterative design'], 0, '')], weight=3),
        9: dict(notes=['Four activities: 1 discover requirements, 2 design alternatives, 3 prototype, 4 evaluate.'],
                tips=[trick('Discover → Design → Prototype → Evaluate → repeat.')], weight=3),
        11: dict(notes=['Google Design Sprint (5 days): unpack, sketch, decide, prototype, test.']),
        17: dict(notes=['Three key characteristics: focus on users, specific usability and UX goals, iteration.']),
        19: dict(notes=['Stakeholders: everyone affected by the product’s success or failure, not only the direct users.']),
        22: dict(notes=['Users rarely know what is possible; find needs by understanding their characteristics and capabilities, what they want to achieve, and how they do it now.']),
        23: dict(notes=['Alternatives come from designers’ creativity, users’ suggestions, other products, other domains.']),
        24: dict(notes=['Choose alternatives with evaluation: prototypes tested with users, and quality thresholds from the usability goals.']),
    }


class requirements:
    AUTO_SLIDES = True
    DECK = deck('d06', 'Establishing Requirements', 'Lectures 6–7',
                'Data gathering (interviews, questionnaires, observation, ethnography, contextual inquiry), recording '
                'and guidelines, kinds of requirements, personas and scenarios, use cases and hierarchical task '
                'analysis, then data analysis: quantitative and qualitative, grounded theory and activity theory.')
    ANN = {
        6: dict(notes=['Five key issues in data gathering: setting goals, identifying participants, relationship with participants (consent), triangulation, pilot studies.'],
                exam=[mcq('Using more than one data-gathering technique to confirm findings is:', ['Triangulation', 'Piloting', 'Coding', 'Sampling'], 0, '')], weight=3),
        8: dict(notes=['Interviews: unstructured (open), structured (fixed questions), semi-structured (mix), group interviews / focus groups.'],
                exam=[mcq('An interview with a script of set questions plus probing follow-ups is:', ['Semi-structured', 'Structured', 'Unstructured', 'A focus group'], 0, '')], weight=3),
        15: dict(notes=['Questionnaires: reach many people; closed (easy to analyse) vs. open questions; Likert scales.']),
        23: dict(notes=['Observation: direct (in the field or controlled) or indirect (diaries, logs, web analytics).']),
        28: dict(notes=['Ethnography: observing and taking part in a group’s everyday life over time.']),
        34: dict(notes=['Contextual inquiry: interviewing users in their own work environment while they work (master–apprentice).']),
        39: dict(notes=['Recording: notes, audio, video, photographs.']),
        48: dict(notes=['Kinds of requirements: functional, data, environment/context (physical, social, organizational, technical), user characteristics, usability and UX goals.']),
        53: dict(notes=['Persona: a rich, fictional but realistic description of a typical user, built from research data.'],
                 exam=[mcq('A fictional, data-based description of a typical user with a name and goals is a:', ['Persona', 'Scenario', 'Use case', 'Storyboard'], 0, '')], weight=3),
        57: dict(notes=['Scenario: an informal narrative story about how people use a product to carry out a task.']),
        58: dict(notes=['Use case: actor–system interaction for one goal; essential use case: abstract user intention vs. system responsibility.']),
        63: dict(notes=['Hierarchical task analysis (HTA): break a task into subtasks and plans (in what order).'],
                 exam=[mcq('Breaking "borrow a book" into numbered subtasks with plans is:', ['Hierarchical task analysis', 'A persona', 'Grounded theory', 'A heuristic evaluation'], 0, '')], weight=3),
        68: dict(notes=['Quantitative data: numbers (averages, percentages). Qualitative: words and themes.']),
        76: dict(notes=['Grounded theory: develop theory from the data through open, axial and selective coding.']),
        79: dict(notes=['Activity theory: subject, object, tools, rules, community, division of labour.']),
    }


class principles:
    AUTO_SLIDES = True
    DECK = deck('d07', 'Design Principles and Guidelines', 'Lecture 8',
                'Principles vs. guidelines vs. standards, usability principles (learnability, flexibility, robustness '
                'and their sub-principles), and heuristics and golden rules (Shneiderman’s eight golden rules, Nielsen’s '
                'heuristics).')
    ANN = {
        5: dict(notes=['Principles: abstract design rules. Guidelines: more specific advice. Standards: specific and authoritative rules.']),
        9: dict(notes=['Usability principles in three groups: LEARNABILITY (predictability, synthesizability, familiarity, generalizability, consistency), FLEXIBILITY (dialog initiative, multithreading, substitutivity, customizability), ROBUSTNESS (observability, recoverability, responsiveness, task conformance).'],
                 exam=[mcq('Being able to undo an action belongs to which principle group?', ['Robustness (recoverability)', 'Learnability', 'Flexibility', 'Familiarity'], 0, ''),
                       mcq('Letting users customize toolbars belongs to:', ['Flexibility', 'Robustness', 'Learnability', 'Predictability'], 0, '')], weight=3),
        27: dict(notes=['Shneiderman’s 8 golden rules: strive for consistency, universal usability (shortcuts), informative feedback, dialogs that yield closure, prevent errors, permit easy reversal, keep users in control, reduce short-term memory load.'],
                 exam=[mcq('Which is one of Shneiderman’s golden rules?', ['Permit easy reversal of actions', 'Hide system status', 'Maximize short-term memory load', 'Avoid shortcuts'], 0, '')], weight=3),
        31: dict(notes=['Nielsen’s heuristics (see Lecture 13).'], seen=[see('d11', 8, 'Nielsen’s heuristics')]),
    }


class prototyping:
    AUTO_SLIDES = True
    DECK = deck('d08', 'Design, Prototyping and Construction', 'Lectures 9–10',
                'What a prototype is and why build one, filtering and manifestation dimensions, low- vs. high-fidelity '
                'prototypes and the compromises involved, construction, conceptual design (metaphors, interaction types, '
                'expanding the concept), concrete design, scenarios and storyboards, card-based prototypes and physical '
                'computing kits.')
    ANN = {
        5: dict(notes=['Prototype: a manifestation of a design that lets stakeholders interact with it and explore its suitability.']),
        8: dict(notes=['Why prototype: evaluation and feedback, communicate ideas, test technical feasibility, clarify requirements, choose between alternatives.']),
        12: dict(notes=['Low fidelity: paper, sketches, storyboards, cards, Wizard of Oz. Quick, cheap, easy to change; good early.'],
                 exam=[mcq('A storyboard on paper is a:', ['Low-fidelity prototype', 'High-fidelity prototype', 'Final product', 'Usability test'], 0, '')], weight=3),
        16: dict(notes=['High fidelity: looks and works like the final product (built with tools such as Figma or code). More expensive; users may focus on details; developers may resist throwing it away.']),
        17: dict(notes=['Compromises: horizontal (wide range of functions, little detail) vs. vertical (few functions in depth). Throwaway vs. evolutionary prototyping.'],
                 exam=[mcq('A prototype with many features but little detail in each is:', ['Horizontal', 'Vertical', 'Evolutionary', 'High-fidelity'], 0, '')], weight=3),
        21: dict(notes=['Conceptual design: what the product will do and how it behaves (concepts, metaphors, interaction types). Concrete design: colours, layout, icons, details.'],
                 tips=[trap('Conceptual design = WHAT and how it behaves; concrete design = how it LOOKS.')], weight=3),
        27: dict(notes=['Scenarios → storyboards → card-based prototypes.']),
        31: dict(notes=['Physical computing: Arduino, MaKey MaKey, micro:bit for prototyping physical interaction.']),
    }


class evaluation:
    AUTO_SLIDES = True
    DECK = deck('d09', 'Evaluation Foundations', 'Lecture 11',
                'Why, what, where and when to evaluate, the types of evaluation (controlled settings with users, natural '
                'settings, settings without users), usability and living labs, an airline-booking usability case study, '
                'evaluation methods, participants’ rights and interpreting data.')
    ANN = {
        6: dict(notes=['Why: check users can use the product and like it. What: prototypes to full systems. Where: lab, field, remotely. When: formative (during design) and summative (to assess a finished product).'],
                exam=[mcq('Evaluation during design to improve the product is:', ['Formative', 'Summative', 'Heuristic', 'Analytical'], 0, '')], weight=3),
        7: dict(notes=['Types: controlled settings with users (usability testing, experiments), natural settings with users (field studies), any setting without users (inspections, heuristics, walkthroughs, models, analytics).'],
                 exam=[mcq('Heuristic evaluation is done:', ['Without users, by experts', 'With users in a lab', 'In the field with users', 'Only after release'], 0, '')], weight=3),
        8: dict(notes=['Usability lab: controlled environment with recording equipment; living lab: real everyday environment instrumented for study.']),
        11: dict(notes=['Usability testing: users do typical tasks; measure time, errors, satisfaction. Field studies: real use in context.']),
        23: dict(notes=['Participants’ rights: informed consent, privacy, the right to stop at any time.']),
        24: dict(notes=['Interpreting data: reliability (consistent), validity (measures what it should), ecological validity (environment affects results), biases, scope.'],
                 exam=[mcq('A lab study’s results may not reflect real-world use. This concerns:', ['Ecological validity', 'Reliability', 'Scope', 'Consent'], 0, '')], weight=3),
    }


class decide:
    AUTO_SLIDES = True
    DECK = deck('d10', 'DECIDE, Usability Testing and Experiments', 'Lecture 12',
                'The DECIDE framework, usability testing (labs, portable and remote testing, eye tracking, data types, '
                'how many participants), experiments and experimental design (different, same or matched '
                'participants), and field studies.')
    DECIDE = 'DECIDE: Determine the goals, Explore the questions, Choose the approach and methods, Identify practical issues, Decide about ethical issues, Evaluate, interpret and present the data.'
    ANN = {
        4: dict(notes=[DECIDE], tips=[tip(DECIDE)],
                exam=[mcq('In DECIDE, the "I" stands for:', ['Identify the practical issues', 'Interpret the data', 'Investigate users', 'Iterate the design'], 0, '')], weight=3),
        12: dict(notes=['Usability testing: measure users’ performance on typical tasks in controlled conditions (time, errors, satisfaction, think-aloud).']),
        18: dict(notes=['Eye tracking shows where users look (heat maps, gaze plots).']),
        19: dict(notes=['Remote usability testing: users test from their own location; recorded online.']),
        22: dict(notes=['About 5–12 participants are often enough for a usability test (Nielsen: 5 users find most problems).'],
                 exam=[mcq('According to Nielsen, about how many users find most usability problems in a test?', ['5', '50', '1', '100'], 0, '')], weight=3),
        23: dict(notes=['Experiments test a hypothesis: independent variable (what you change) → dependent variable (what you measure).'],
                 exam=[mcq('In an experiment comparing two menu designs on task time, the menu design is the:', ['Independent variable', 'Dependent variable', 'Control group', 'Hypothesis'], 0, '')], weight=3),
        25: dict(notes=['Designs: different participants (between-subjects: no order effects, needs more people), same participants (within-subjects: fewer people, order effects → counterbalance), matched participants.'],
                 tips=[trap('Within-subjects (same participants) designs suffer from ORDER effects; fix with counterbalancing.')],
                 exam=[mcq('Each participant tries both designs. This is a:', ['Same-participant (within-subjects) design', 'Different-participant design', 'Matched-participant design', 'Field study'], 0, '')], weight=3),
        26: dict(notes=['Field studies: observe real use in natural settings; less control, more realism.']),
    }


class inspections:
    AUTO_SLIDES = True
    DECK = deck('d11', 'Inspections, Heuristics and Walkthroughs', 'Lecture 13',
                'Inspection methods without users: heuristic evaluation with Nielsen’s revised heuristics, number of '
                'evaluators, the three stages, advantages and problems, cognitive and pluralistic walkthroughs, and A/B testing.')
    NIELSEN = ('Nielsen’s 10: visibility of system status · match with the real world · user control and freedom · consistency '
               'and standards · error prevention · recognition rather than recall · flexibility and efficiency · aesthetic and '
               'minimalist design · help users recognize, diagnose and recover from errors · help and documentation.')
    ANN = {
        6: dict(notes=['Inspections: experts role-play users to find problems (no users needed).']),
        7: dict(notes=['Heuristic evaluation: experts check the interface against usability principles (heuristics).']),
        8: dict(notes=[NIELSEN], tips=[tip(NIELSEN)],
                exam=[mcq('A progress bar while uploading supports which heuristic?', ['Visibility of system status', 'Aesthetic and minimalist design', 'Help and documentation', 'Error prevention'], 0, ''),
                      mcq('An "Undo" button supports:', ['User control and freedom', 'Recognition rather than recall', 'Consistency and standards', 'Match with the real world'], 0, '')], weight=3),
        12: dict(notes=['One evaluator finds ~35% of problems; 3–5 evaluators find ~75%.'],
                 exam=[mcq('How many evaluators are typically recommended for heuristic evaluation?', ['3–5', '1', '20', '50'], 0, '')], weight=3),
        14: dict(notes=['Three stages: briefing session → evaluation period (each expert alone, two passes) → debriefing session (prioritize problems).']),
        17: dict(notes=['Advantages: cheap, quick, no users. Problems: false alarms, misses, experts aren’t real users.']),
        19: dict(notes=['Cognitive walkthrough: simulate a user’s problem solving step by step; focuses on LEARNABILITY (ease of learning).'],
                 tips=[trick('Three questions: Will the user know what to do? Will they see how to do it? Will they understand from the feedback whether it worked?')],
                 exam=[mcq('Cognitive walkthroughs mainly evaluate:', ['Ease of learning', 'Aesthetics', 'Performance', 'Security'], 0, '')], weight=3),
        22: dict(notes=['Pluralistic walkthrough: users, developers and usability experts step through a scenario together.']),
        23: dict(notes=['A/B testing: show two versions to different groups of real users online and compare a metric (clicks, conversions).'],
                 exam=[mcq('Showing half of visitors a green button and half a blue one, then comparing clicks, is:', ['A/B testing', 'Heuristic evaluation', 'Cognitive walkthrough', 'Ethnography'], 0, '')], weight=3),
    }


DECKS_HERE = [intro, cognition, emotion, interfaces, process, requirements, principles, prototyping, evaluation, decide, inspections]
