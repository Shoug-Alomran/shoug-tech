"""SE322 annotated slides — Chapter 9: Documenting Software Architectures.
See ch01_introduction.py for AUTO_SLIDES and the ANN keys."""
from .common import mcq, past, scen, see, short, tf, tip, trap, trick

AUTO_SLIDES = 'all'
OVERVIEW = 'This chapter explains how to document software architecture for stakeholder education, communication, and analysis. It covers choosing views, documenting their elements and relationships, recording rationale, mapping across views, and writing for the intended audience.'

DECK = {
    'key': 'ch9',
    'slug': '19-documentation',
    'file': 'documentation',
    'title': 'Documenting Software Architectures',
    'chapter': 'Chapter 9',
    'page': 'ch09_page',  # notes, highlights and exam questions in the page schema
    'pdf': '/academics/software-engineering/se322/slides/chapter-9-documentation/',
    'lede': ('Why architecture must be documented, the three uses of documentation, choosing views (4+1, Siemens, '
             'Software Cost Reduction), stakeholder concerns, templates (RUP and SEI), and what goes into each '
             'view and beyond the views. Final 252 asked for two templates and the minimum necessary information.'),
}

VIEW = 'Documenting a view: 1 primary presentation · 2 element catalog · 3 context diagram · 4 variability guide · 5 architecture background (rationale) · plus other information.'

ANN = {
    1: dict(kind='title', title='Documenting Software Architectures', body=[], sub='SE322 · Chapter 9', tips=[tip(VIEW)]),
    2: dict(notes=['The lecture covers why architecture documentation matters, how to document individual views, and what information belongs across views. Documentation should make the architecture understandable and usable for its audience.']),
    3: dict(notes=['Architecture documentation is the shared explanation people use to build, test, operate, and change a system. If it is unclear or stale, different roles make incompatible assumptions even when the design itself is sound.']),
    4: dict(notes=['Even the best architecture is useless if people don’t know it, can’t understand it, or misunderstand it.']),
    5: dict(notes=['Start from readers’ questions, choose views that answer them, document those views, then record decisions spanning multiple views. This avoids one unreadable diagram and disconnected diagrams with no shared explanation.']),
    6: dict(notes=['Education introduces newcomers; communication coordinates stakeholder decisions; analysis provides evidence for evaluation. Each purpose needs the right level of detail and audience.'],
            exam=[mcq('Which is NOT one of the three primary uses of architecture documentation?', ['Marketing the product', 'Education', 'Communication among stakeholders', 'Analysis'], 0, '')], weight=3),
    7: dict(notes=['A Software Architecture Document (SAD) is an organized set of views and supporting explanations. Select views by stakeholder need first; the SAD is not a requirement to include every diagram type.']),
    8: dict(notes=['The 4+1 model is one reusable view set: logical, process, development, and physical views are connected by scenarios. Choose it when those perspectives answer the system’s stakeholder questions.'], seen=[see('ch2.3', 4, 'The 4+1 views')]),
    9: dict(notes=['Siemens’ views separate conceptual responsibilities, code modules, runtime execution, and code organization. The separation helps readers move from what the system does to how it is built and run.']),
    10: dict(notes=['The Software Cost Reduction approach selects views such as module, process, and uses according to the questions the architecture must answer. Different view sets organize the same system for different kinds of analysis.']),
    11: dict(notes=['Choose views by asking who will use the document and what decisions they need to make. Developers may need module dependencies while operators need runtime and deployment behavior; every possible view would add noise.']),
    12: dict(notes=['List real stakeholder groups because they need different information: developers need dependencies, testers need behavior, and maintainers need change rationale. A single undifferentiated audience often leads to either missing detail or unnecessary bulk.']),
    13: dict(notes=['A stakeholder-concern-view table exposes missing coverage. If operators care about recovery but no view explains deployment or failover, the document cannot answer their question.']),
    14: dict(notes=['A template provides consistent headings and prompts so authors do not forget important architectural information. Tailor it to the system; filling every heading mechanically can produce material readers do not need.'],
             past=[past('f252', 'Q8 · two documentation templates')],
             exam=[short('State two templates that can be used to document an architecture. (Final 252)', 'The Rational Unified Process (RUP) Software Architecture Document template, and the Software Engineering Institute (SEI) “Views and Beyond” template.')],
             weight=3),
    15: dict(notes=['The SEI template is another structure for organizing architectural views and their documentation. Compare templates by whether they help the intended readers find rationale, element details, and cross-view relationships.'], weight=3),
    16: dict(notes=['Minimum documentation means enough to answer stakeholder questions without burying decisions in irrelevant detail. It does not mean omitting rationale or constraints needed to change the system safely.'],
             past=[past('f252', 'Q8 · the major necessary information')],
             exam=[short('What is the major necessary information in a software architecture document? (Final 252)', 'The selected views (each with a primary presentation and element catalog), the system overview and context, the mapping between views, the rationale for the key decisions, and how quality attribute requirements are met — the minimum needed to understand the system.')],
             weight=3),
    17: dict(notes=['The primary presentation is the main diagram or table for a view. Give it a clear scope and legend so readers do not have to guess what symbols or connections mean.'], tips=[tip(VIEW)]),
    18: dict(notes=['An element catalog explains what diagram parts represent; a context diagram shows the system boundary and external actors. Together they prevent readers from guessing what a box means or what lies outside the system.']),
    19: dict(notes=['A variability guide records choices that can differ by installation or environment; background records why the design was chosen and its assumptions. This helps future teams change it without repeating old debates.'],
             exam=[mcq('The part of a view’s documentation explaining the elements shown in the diagram is the:', ['Element catalog', 'Variability guide', 'Context diagram', 'Roadmap'], 0, '')], weight=2),
    20: dict(notes=['A documentation roadmap explains how the document is organized and where to find information; a view template keeps each view description consistent. Both reduce the effort readers spend navigating the SAD.']),
    21: dict(notes=['A mapping links the same real element across views—for example, a logical service to the process and deployment that implement it. Without mappings, one view can quietly contradict another.']),
    22: dict(notes=['Record decisions that span views in one discoverable place, and provide a directory or glossary for navigation and terminology. This prevents readers from interpreting the same term differently across sections.']),
    23: dict(notes=['Document quality goals alongside the decisions and constraints that support them, including trade-offs. A response-time target is more useful when readers can see which components own it and what choices make it plausible.']),
    24: dict(notes=['Write for the audience and purpose: executives may need rationale and trade-offs, developers need interfaces and structures, and maintainers need constraints and change implications.']),
    25: dict(notes=['Review why to document, how to select and describe views, and what cross-view information is needed. Keep the document complete enough to understand and evaluate the architecture without adding irrelevant detail.']),
}
