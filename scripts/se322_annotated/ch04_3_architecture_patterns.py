"""SE322 annotated slides — Chapter 4, Lecture 3: MVC and the layered pattern.
See ch01_introduction.py for AUTO_SLIDES and the ANN keys."""
from .common import mcq, past, scen, see, short, tf, tip, trap, trick

AUTO_SLIDES = 'all'
OVERVIEW = 'This chapter studies reusable architecture patterns and their trade-offs, including data-centered systems, pipes and filters, distributed systems, MVC, and layered architectures. For each pattern, focus on the problem it solves and how its structure affects system qualities.'

DECK = {
    'key': 'ch4.3',
    'slug': '09-architecture-patterns-lecture-3',
    'file': 'architecture-patterns-lecture-3',
    'title': 'Architecture Patterns: Model-View-Controller and Layered',
    'chapter': 'Chapter 4 · Lecture 3',
    'page': 'ch04_3_page',  # notes, highlights and exam questions in the page schema
    'pdf': '/academics/software-engineering/se322/slides/chapter-4-architecture-patterns-lecture-3-extra/',
    'lede': ('Interactive systems and MVC (model, view, controller, with the speech example), then hierarchical '
             'systems and the layered pattern. Final 252 asked for an MVC component diagram (Safari Explorer) and '
             'Midterm 261 matched scenarios to styles.'),
}

ANN = {
    1: dict(kind='title', title='Architecture Patterns', body=[], sub='SE322 · Chapter 4, Lecture 3'),
    2: dict(notes=['This lecture covers interactive systems, especially MVC, and hierarchical systems such as layered architecture. Compare how each style separates responsibilities and what kinds of change it supports.']),
    3: dict(notes=['Interactive systems revolve around user interaction; UI changes often, so separate it from the core data and logic.']),
    4: dict(notes=['The figure illustrates how an interactive system receives user actions and produces feedback. Use it to locate the interface boundary and the underlying application state.']),
    5: dict(notes=['A model can support several synchronized views, such as a table and chart. Both should display the same underlying data; separate copies can drift and show contradictory results.']),
    6: dict(notes=['The model owns state and business rules, the view renders that state, and the controller translates user actions into model operations. This lets a screen change without rewriting the rules that update data.'],
            tips=[trick('Model knows the data, View shows it, Controller handles the clicks.')],
            past=[past('f252', 'Q4 · Safari Explorer = MVC'), past('m261', 'match scenario to style', related=True), past('m261', 'Q6 · match scenarios to architectural styles', related=True)],
            exam=[mcq('In MVC, the component that handles user input is the:', ['Controller', 'Model', 'View', 'Broker'], 0, ''),
                  mcq('Which pattern best fits an app showing the same data in several synchronised views that the user edits?', ['MVC', 'Pipes and filters', 'Blackboard', 'Broker'], 0, '')],
            weight=3),
    7: dict(notes=['MVC component diagram: the model notifies views of changes; controllers update the model.'],
            exam=[short('Name the MVC components and what each does. (Final 252 Safari Explorer)', 'Model: holds the data and business rules and notifies views when it changes. View: displays the model to the user. Controller: receives user input and turns it into updates on the model (and view selection).')],
            weight=3),
    8: dict(notes=['The speech application demonstrates MVC using a user interface for commands, a controller for input handling, and a model that represents speech data or processing state.']),
    9: dict(notes=['Map each speech-system responsibility to model, view, or controller. The model owns application state, the view presents it, and the controller interprets user input and coordinates updates.']),
    10: dict(notes=['The class/component diagram shows the static relationships among the MVC parts. Check that the view does not take over model responsibilities and that user commands reach the model through the controller.']),
    11: dict(notes=['SpeechController methods handle user commands and update the model. Keeping these actions in the controller separates input coordination from data ownership and presentation.']),
    12: dict(notes=['MVC isolates presentation changes and supports multiple views. It also adds objects and update paths, so a tiny static screen may not benefit enough to justify the extra indirection.'],
             exam=[tf('MVC lets the user interface change without changing the model.', True, '')], weight=2),
    13: dict(notes=['A layered system arranges components in levels; each layer uses services from the layer below and provides services to the layer above. This constrains dependencies and allows changes within a layer when its interface remains stable.']),
    14: dict(notes=['OSI layers and operating-system subsystems illustrate hierarchical organization. A layer should communicate through defined services rather than bypassing neighboring layers without a reason.']),
    15: dict(notes=['A layer provides services upward and depends downward, limiting tangled dependencies. The rule aids replacement and testing, but layers should not become arbitrary pass-through wrappers.'],
             exam=[mcq('In a strict layered architecture, a layer may use:', ['Only the layer directly below it', 'Any layer', 'Only the layer above', 'No other layer'], 0, '')], weight=3, past=[past('m261', 'Q6 · match scenarios to architectural styles', related=True)]),
    16: dict(notes=['Layering can localize change—for example, replacing a database adapter while leaving business logic alone. Each boundary adds calls, though, so frequently used operations may pay a performance cost.'],
             exam=[mcq('A drawback of the layered pattern is:', ['Performance overhead from passing through many layers', 'It cannot be modified', 'It has no reuse', 'Components share a blackboard'], 0, '')], weight=2),
    17: dict(notes=['The next chapter moves from architecture patterns to detailed-design principles. Architecture establishes the major structure; detailed design explains how each component fulfills its role.'], seen=[see('ch5.1', 3, 'Principles of detailed design')]),
}
