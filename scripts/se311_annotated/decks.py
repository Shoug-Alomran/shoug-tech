"""SE311 annotated slides — every Software Requirements Engineering deck (Wiegers & Beatty).

One module holds all the decks: each deck is a namespace class with DECK and ANN (and AUTO_SLIDES).
Slides without an ANN entry are shown without notes. past('q1', ...) points at Quiz 1 (Ch. 1–3) in
exams/. See cs331_annotated/ch01_1_introduction.py for the ANN keys."""
from .common import DECKS, mcq, past, see, short, tf, tip, trap, trick


def deck(key, title, chapter, lede):
    slug, file, folder, _ = DECKS[key]
    return {'key': key, 'slug': slug, 'file': file, 'title': title, 'chapter': chapter,
            'pdf': '/academics/software-engineering/se311/slides/%s/' % folder, 'lede': lede}


LEVELS = 'Three levels: BUSINESS requirements (why: objectives) → USER requirements (what users must be able to do) → FUNCTIONAL requirements (what the system must do), plus non-functional requirements and constraints.'


class fundamentals:
    AUTO_SLIDES = True
    DECK = deck('d01', 'Software Requirements Engineering Fundamentals', 'Chapter 1',
                'What a requirement is, the levels and types of requirements (business, user, functional, '
                'non-functional, domain), why requirements engineering matters (Mars Climate Orbiter), the RE '
                'activities and process, requirements development vs. management, and RE challenges.')
    ANN = {
        4: dict(notes=['Requirements errors account for 40–50% of all defects, and they are the most expensive to fix late.'],
                past=[past('q1', 'Q4: share of defects from requirements')],
                exam=[tf('Errors introduced during requirements activities account for 40 to 50 percent of all defects found in software.', True, '')], weight=3),
        11: dict(notes=['A requirement: a statement of a capability or condition the system must have to satisfy a stakeholder need.']),
        13: dict(notes=[LEVELS], tips=[tip(LEVELS)],
                 past=[past('q1', 'Q12: three types of requirements with examples')],
                 exam=[short('List and briefly explain THREE types of requirements, with an example for each.', 'Business requirement: why the organization builds the system (e.g. "reduce order processing time by 30%"). User requirement: a task users must be able to do (e.g. "a clerk can register a new customer"). Functional requirement: a behaviour the system must perform (e.g. "the system shall email a receipt after payment"). Non-functional: a quality or constraint (e.g. "pages load within 2 seconds").')], weight=3),
        14: dict(notes=['Functional requirements describe behaviour under specific conditions ("the system shall…").'],
                 past=[past('q1', 'Q6: picking the functional requirement')],
                 exam=[mcq('Which is a functional requirement?', ['If the passenger has no seating preference, the system shall assign a seat', 'The system shall be available 98% of the time', 'The system shall be compatible with iOS', 'Search results should load within 5 seconds'], 0, '')], weight=3),
        15: dict(notes=['Non-functional: quality attributes (performance, security, usability, availability), external interfaces, constraints. Harder to capture than functional requirements.'],
                 past=[past('q1', 'Q1: which kind is harder to capture')],
                 exam=[tf('Functional requirements are more difficult to capture than non-functional requirements.', False, 'Non-functional requirements are usually harder.')], weight=3),
        21: dict(notes=['Domain requirements: come from the application domain (laws, regulations, domain rules).'],
                 past=[past('q1', 'Q5: an example of a domain requirement')],
                 exam=[mcq('Which is a domain requirement?', ['Only a patient’s designated physician may retrieve the patient’s medical reports', 'The system shall respond within 2 seconds', 'The user shall be able to print reports', 'The system shall be developed in Java'], 0, '')], weight=3),
        23: dict(notes=['Mars Climate Orbiter (1999) was lost because one team used imperial units and another metric: a requirements/interface failure.']),
        26: dict(notes=['RE activities: elicitation, analysis, specification, validation (development) + requirements management.']),
        29: dict(notes=['RE is iterative, not a one-time phase.'], past=[past('q1', 'Q2: is RE iterative?')],
                 exam=[tf('Requirements engineering is not an iterative process.', False, '')], weight=3),
        31: dict(notes=['Requirements development produces the baseline; requirements management controls changes to it (traceability, versions, status).']),
        32: dict(notes=['Challenges: unclear scope, changing requirements, stakeholders who disagree or are unavailable, ambiguity, gold-plating.']),
    }


class inception:
    AUTO_SLIDES = True
    DECK = deck('d02', 'Requirements Inception', 'Chapter 2',
                'Why inception matters, business requirements (problems, objectives, success metrics), the vision '
                'statement, scope and limitations, the Vision and Scope document, stakeholders, and scope '
                'representations: context diagrams, ecosystem maps, feature trees and event lists.')
    ANN = {
        3: dict(notes=['Inception establishes a shared understanding of the product’s context, problem, solution, boundaries and benefits.'],
                past=[past('q1', 'Q7: the goal of inception')],
                exam=[mcq('The primary goal of requirements inception is to:', ['Establish a shared understanding of the product’s context, problem, solution, boundaries and benefits', 'Write the complete SRS', 'Develop detailed use cases', 'Validate all requirements'], 0, '')], weight=3),
        6: dict(notes=['Business requirements: the business problem, the objectives (measurable), and how success will be measured.']),
        11: dict(notes=['Success metrics: measurable indicators that the objectives were achieved.']),
        12: dict(notes=['Vision statement: a short summary of the long-term purpose: For [customer] who [need], the [product] is a [category] that [benefit]. Unlike [alternative], our product [differentiator].']),
        13: dict(notes=['Vision and Scope document = the main OUTPUT of inception: business requirements, vision, scope and limitations, business context (stakeholders, priorities).'],
                 past=[past('q1', 'Q8, Q13: inception output and its components')],
                 exam=[mcq('The primary output of requirements inception is the:', ['Vision and Scope document', 'SRS', 'Use-case diagram', 'Test plan'], 0, ''),
                       short('List four components of a Vision and Scope document.', 'Business requirements (background, opportunity, objectives, success metrics), the vision statement, scope and limitations (major features, scope of initial and later releases, what is excluded), and business context (stakeholder profiles, project priorities, deployment considerations); also business risks and assumptions.')], weight=3),
        14: dict(notes=['Scope: what is in the release. Limitations: what is explicitly OUT.']),
        20: dict(notes=['Stakeholders: anyone who affects or is affected by the project, not only buyers.'],
                 past=[past('q1', 'Q3: who is a stakeholder')],
                 tips=[trap('A stakeholder is not just whoever purchases the system.')],
                 exam=[tf('A stakeholder is anyone who will purchase the completed software.', False, 'Anyone actively involved, affected by, or able to influence the project.')], weight=3),
        23: dict(notes=['Context diagram: the system as ONE circle, external entities around it, data flows in and out. Shows the boundary, NOT internals.'],
                 past=[past('q1', 'Q10: what a context diagram does NOT show')],
                 exam=[mcq('A context diagram does NOT show:', ['Internal objects and processes of the system', 'External entities', 'Data flows to/from the system', 'The system boundary'], 0, '')], weight=3),
        25: dict(notes=['Ecosystem map: all the systems that interact with this one, including indirect ones (no data flows detail).']),
        27: dict(notes=['Feature tree: features in levels (fishbone): level-1 features → sub-features.']),
        29: dict(notes=['Event list: external events (business, signal, temporal) the system must respond to.'],
                 exam=[mcq('"At 2 a.m. every night the system backs up data" is which kind of event?', ['Temporal', 'Business', 'Signal', 'User'], 0, '')], weight=3),
    }


class elicitation_process:
    AUTO_SLIDES = True
    DECK = deck('d03', 'The Requirements Elicitation Process', 'Chapter 3',
                'Elicitation goals and sources of requirements, the process (plan, prepare, perform, follow up), '
                'classifying customer input, knowing when you are done, challenges and best practices.')
    ANN = {
        3: dict(notes=['Elicitation: discovering requirements from stakeholders and other sources (not just "gathering").']),
        4: dict(notes=['Sources: stakeholders and users, documents, existing systems, regulations, competitors, problem reports.']),
        6: dict(notes=['Process: plan → prepare → perform → follow up (organize, share notes, record open issues).']),
        13: dict(notes=['Classify input as: business requirement, user requirement, business rule, functional, quality attribute, external interface, constraint, data definition, solution idea.']),
        14: dict(notes=['Done when: users can’t think of more use cases; new ideas are out of scope or low priority; proposed requirements repeat earlier ones; ideas are future, not current; the remaining issues are understood.'],
                 past=[past('q1', 'Q11: when elicitation is done')],
                 exam=[short('When do you know you are done with elicitation? Give two signs.', 'Users can’t think of any more use cases or user stories; new suggestions are out of scope or already captured (repeating earlier requirements); remaining ideas are “nice to have” for future releases; the team can explain the requirements well enough to build and test.')], weight=3),
        15: dict(notes=['Challenges: stakeholders unavailable, don’t know what they want, use jargon, conflict; scope creep; solution ideas disguised as requirements.']),
        17: dict(notes=['Best practices: define scope first, identify user classes, select product champions, use several techniques, document as you go.']),
    }


class elicitation_techniques:
    AUTO_SLIDES = True
    DECK = deck('d04', 'Requirements Elicitation Techniques', 'Chapter 4',
                'Interviews, workshops, focus groups, observation, questionnaires, system- and user-interface analysis, '
                'document analysis, use cases and usage scenarios, misuse cases, and prototyping (purpose, fidelity, '
                'risks and success factors), with a comparison of techniques.')
    ANN = {
        9: dict(notes=['Interviews: one-on-one or small group; good for detail. Prepare questions, stay in scope, listen, take notes.']),
        12: dict(notes=['Workshops: structured, facilitated sessions with many stakeholders to resolve conflicts and define requirements fast.']),
        15: dict(notes=['Focus groups: representative users discussing attitudes, impressions, preferences and needs: suited to COMMERCIAL products.'],
                 past=[past('q1', 'Q9: exploring attitudes and preferences')],
                 exam=[mcq('Best technique for exploring users’ attitudes, impressions and preferences for a commercial product:', ['Focus groups', 'Document analysis', 'Interviews', 'Observation'], 0, '')], weight=3),
        17: dict(notes=['Observation: watch users do their real work; reveals tacit steps they forget to mention. Silent or interactive.'],
                 exam=[mcq('Users can’t explain a complex task they do automatically. Best technique:', ['Observation', 'Questionnaire', 'Focus group', 'Document analysis'], 0, '')], weight=3),
        19: dict(notes=['Questionnaires: reach many users cheaply; hard to write well; no follow-up.']),
        21: dict(notes=['System interface analysis: study the systems this one connects to.']),
        22: dict(notes=['User interface analysis: study existing screens and how they are used.']),
        24: dict(notes=['Document analysis: existing documentation, regulations, manuals, reports.']),
        25: dict(notes=['Use case: a goal-oriented interaction between an actor and the system (normal flow, alternatives, exceptions).']),
        30: dict(notes=['Misuse case: what an attacker (or careless user) wants to do; reveals security requirements.'],
                 exam=[mcq('Misuse cases help discover mainly:', ['Security requirements', 'Performance requirements', 'Business objectives', 'Usability metrics'], 0, '')], weight=3),
        35: dict(notes=['Prototype: a partial implementation to clarify requirements. Throwaway vs. evolutionary; low fidelity (paper) vs. high fidelity (looks real).'],
                 tips=[trap('Risk: stakeholders see a polished prototype and think the system is nearly done.')],
                 exam=[mcq('A paper sketch of screens is a:', ['Low-fidelity prototype', 'High-fidelity prototype', 'Evolutionary prototype', 'Final design'], 0, '')], weight=3),
    }


class domain_modeling:
    AUTO_SLIDES = True
    DECK = deck('d05', 'Requirements Analysis: Domain Modeling', 'Chapter 5.1',
                'Requirements analysis activities, the system requirements specification and ways to write it, and '
                'domain modeling: identifying and evaluating classes, associations and attributes, then adding detail.')
    ANN = {
        3: dict(notes=['Analysis: model, decompose, prioritize and refine requirements so they are complete and understood.']),
        5: dict(notes=['SRS: the system requirements specification; written in natural language, structured templates, or models.']),
        8: dict(notes=['Domain model: a class diagram of real-world concepts (no methods/implementation) in the problem domain.']),
        10: dict(notes=['Find candidate classes from NOUNS in the requirements; associations from verbs/relationships.'],
                 tips=[trick('Nouns → classes or attributes; verbs → associations or operations.')],
                 exam=[mcq('When building a domain model, candidate classes come mostly from:', ['Nouns in the requirements', 'Verbs', 'Adjectives', 'Test cases'], 0, '')], weight=3),
        11: dict(notes=['Evaluate classes: drop redundant, irrelevant, vague, implementation, or attribute-like ones.'],
                 exam=[mcq('"Email address" in a domain model is most likely:', ['An attribute of Customer', 'A class', 'An association', 'An actor'], 0, '')], weight=3),
        12: dict(notes=['Evaluate associations: keep those that are needed and lasting; add multiplicities, names, roles.']),
        14: dict(notes=['Detail: association classes, aggregation/composition, generalization.']),
    }


class domain_exercise:
    AUTO_SLIDES = True
    DECK = deck('d06', 'Domain Model Exercise: the Movie Shop', 'Chapter 5.2',
                'A worked case study: from the Movie Shop requirements statement to a domain model, analysing each '
                'requirement for classes, attributes, associations and generalizations, the solution diagram, and '
                'common errors.')
    ANN = {
        2: dict(notes=['Read the requirements once for the big picture, then line by line for classes, attributes and associations.']),
        5: dict(notes=['Analysis: each requirement → the classes, attributes and associations it implies (e.g. Movie, PhysicalMovie, DigitalMovie, Customer, Member, Rental, Reservation, Review).']),
        11: dict(notes=['Solution: Movie generalizes into physical and digital movies; Rental and Reservation link customers to physical copies.']),
        18: dict(notes=['Common errors: modelling actions as classes, putting methods in a domain model, missing multiplicities, attributes that should be classes (and vice versa).'],
                 exam=[mcq('Which is a common domain-model error?', ['Showing operations/methods for classes', 'Using generalization', 'Adding multiplicities', 'Naming associations'], 0, 'A domain model shows concepts, not implementation.')], weight=3),
    }


class usecase_exercise:
    AUTO_SLIDES = True
    DECK = deck('d07', 'Use-Case Model Exercise: the Movie Shop', 'Chapter 5.5',
                'From the Movie Shop requirements to a use-case model: identifying actors and their functionality, '
                'grouping functionality into use cases, the initial and refined use-case diagrams, common errors, and '
                'the Reserve Movie use case.')
    ANN = {
        4: dict(notes=['Identify actors (roles outside the system: Customer, Member, Clerk, Manager) and what each needs to do.'],
                exam=[mcq('In a use-case model, an actor is:', ['A role played by someone or something outside the system', 'A class inside the system', 'A screen', 'A database table'], 0, '')], weight=3),
        10: dict(notes=['Group related functionality into use cases (one user goal each), not one use case per button.']),
        13: dict(notes=['Initial diagram: actors linked to the use cases they start.']),
        14: dict(notes=['Refined diagram: generalize actors (Member is a Customer), factor shared steps with <<include>>, optional ones with <<extend>>.']),
        15: dict(notes=['Common errors: use cases that are steps rather than goals, the system shown as an actor, functional decomposition, missing actors.'],
                 exam=[mcq('Which is a use-case modelling error?', ['Making "Enter password" a separate use case', 'Generalizing actors', 'Using <<include>> for shared steps', 'Naming use cases with verb phrases'], 0, '')], weight=3),
    }


class usecase_spec:
    AUTO_SLIDES = True
    DECK = deck('d08', 'Use-Case Detailed Specification', 'Chapter 5.6',
                'Two templates (styles) for writing a detailed use-case specification: ID, actors, description, '
                'preconditions, postconditions, normal flow, alternative flows and exceptions.')
    ANN = {
        1: dict(notes=['Fields: ID and name, primary/secondary actors, description, trigger, preconditions, postconditions, normal flow, alternative flows, exceptions, priority, business rules.'],
                exam=[mcq('A condition that must be true BEFORE a use case starts is a:', ['Precondition', 'Postcondition', 'Trigger', 'Exception'], 0, ''),
                      mcq('An error path such as "card declined" belongs in the:', ['Exception flow', 'Normal flow', 'Preconditions', 'Description'], 0, '')], weight=3),
        4: dict(notes=['Style 2 writes the flows as numbered actor-action / system-response pairs.']),
    }


class excellent:
    AUTO_SLIDES = True
    DECK = deck('d09', 'Writing Excellent Requirements', 'Chapter 6',
                'Characteristics of excellent individual requirements and requirement sets, guidelines on perspective, '
                'writing style, level of detail, representation techniques and avoiding ambiguity, and sample '
                'requirements before and after improvement.')
    ANN = {
        4: dict(notes=['Excellent requirement statements: complete, correct, feasible, necessary, prioritized, unambiguous, verifiable.'],
                exam=[mcq('"The system shall be user-friendly" mainly fails to be:', ['Verifiable (and unambiguous)', 'Necessary', 'Feasible', 'Prioritized'], 0, '')], weight=3),
        11: dict(notes=['Excellent requirement SETS: complete, consistent, modifiable, traceable.'],
                 tips=[trick('Statements: C-C-F-N-P-U-V. Sets: Complete, Consistent, Modifiable, Traceable.')], weight=3),
        18: dict(notes=['Write from the system’s view ("The system shall…") or the user’s ("The user shall be able to…"), consistently.']),
        21: dict(notes=['Style: one requirement per statement, active voice, "shall" for mandatory, consistent terms (glossary), avoid "and/or", "etc.".']),
        30: dict(notes=['Level of detail: enough that developers and testers share the same understanding; more detail for outsourced or safety-critical work.']),
        36: dict(notes=['Use tables, decision tables, diagrams when text gets complicated.']),
        39: dict(notes=['Ambiguity sources: vague words (fast, user-friendly, flexible, robust, efficient), "support", "etc.", "and/or", negative requirements, boundary values.'],
                 tips=[trap('Words like "fast", "easy", "flexible", "minimize", "several" are unverifiable until quantified.')],
                 exam=[mcq('Which is unambiguous?', ['The system shall display search results within 2 seconds for 95% of queries', 'The system shall be fast', 'The system shall support many users', 'The system shall be flexible'], 0, '')], weight=3),
        48: dict(notes=['Before/after samples: split compound requirements, quantify quality attributes, remove design details, define terms.']),
    }


class specification:
    AUTO_SLIDES = True
    DECK = deck('d10', 'Requirements Specification', 'Chapter 7',
                'What the SRS is and who reads it, labeling requirements (sequence numbers, hierarchical numbering, '
                'hierarchical textual tags), handling TBDs, user interfaces in the SRS, readability tips and best '
                'practices.')
    ANN = {
        5: dict(notes=['SRS: functional and non-functional requirements the system must satisfy; the basis for design, testing, planning and contracts.']),
        7: dict(notes=['Audience: customers, marketing, project managers, developers, testers, maintainers, documentation writers, legal.']),
        8: dict(notes=['Every requirement needs a unique, persistent label so it can be traced and referenced.']),
        9: dict(notes=['Labeling methods: sequence numbers (UR-9), hierarchical numbering (3.2.4.1, breaks when edited), hierarchical textual tags (Print.ConfirmCopies).'],
                 exam=[mcq('Which labeling method is most stable when requirements are inserted or deleted?', ['Hierarchical textual tags', 'Hierarchical numbering', 'Page numbers', 'Bullet points'], 0, '')], weight=3),
        17: dict(notes=['TBD ("to be determined") marks gaps: give each an owner and a date, and resolve them before building.']),
        19: dict(notes=['Screen layouts don’t replace functional requirements; keep UI design details out of the SRS (or in an appendix).']),
        22: dict(notes=['Best practices: use a template (e.g. IEEE 830 / ISO 29148), label requirements, keep it current, review it.']),
    }


DECKS_HERE = [fundamentals, inception, elicitation_process, elicitation_techniques, domain_modeling, domain_exercise,
              usecase_exercise, usecase_spec, excellent, specification]
