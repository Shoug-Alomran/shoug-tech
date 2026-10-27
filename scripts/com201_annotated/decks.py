"""COM201 annotated slides — every Introduction to Communication Skills chapter (Pearson & Nelson, Human Communication).

The decks are photographed textbook pages with no text layer, so every slide is shown as the original
image (whole=True) and the notes, tips and practice questions sit beside it. Each deck is a namespace
class built by chapter(); see cs331_annotated/ch01_1_introduction.py for the ANN keys."""
from .common import DECKS, mcq, see, short, tf, tip, trap, trick


def chapter(key, count, lede, ann):
    slug, file, folder, label = DECKS[key]
    head, title = label.split(': ', 1)
    return type(key, (), {
        'AUTO_SLIDES': True,
        'DECK': {'key': key, 'slug': slug, 'file': file, 'title': title, 'chapter': head,
                 'pdf': '/academics/other-courses/com201/slides/%s/' % folder, 'lede': lede},
        'ANN': {n: dict(ann.get(n, {}), whole=True) for n in range(1, count + 1)},
    })


intro = chapter('d01', 26, 'Why studying communication matters, defining communication, its components (people, message, channel, encoding/decoding, feedback, code, noise, situation), communication principles, the contexts (intrapersonal, interpersonal, small-group, public, mass), ethics, theory and careers.', {
    8: dict(notes=['Communication: the process of using messages to generate meaning.']),
    9: dict(notes=['Components: people (source/receiver), message, channel, encoding and decoding, feedback, code, noise (internal or external), situation.'],
            exam=[mcq('Translating thoughts into a message is:', ['Encoding', 'Decoding', 'Feedback', 'Noise'], 0, ''),
                  mcq('A loud air conditioner that distracts you during a lecture is:', ['External noise', 'Internal noise', 'Feedback', 'A channel'], 0, '')], weight=3),
    11: dict(notes=['Principles: begins with the self, involves others, has content AND relational dimensions, involves choices, more quantity ≠ more quality, is pervasive.'],
             tips=[trick('Content = WHAT is said; relational = how it defines the relationship (tone, who is in charge).')],
             exam=[tf('Communicating more always improves a relationship.', False, 'Quantity does not increase quality.')], weight=3),
    15: dict(notes=['Contexts: intrapersonal (with yourself), interpersonal (two people), small-group (3–9), public speaking (one to many, live), mass (through media to large audiences).'],
             exam=[mcq('Thinking through a decision in your own head is which context?', ['Intrapersonal', 'Interpersonal', 'Small-group', 'Public'], 0, ''),
                   mcq('A TV news broadcast is:', ['Mass communication', 'Public speaking', 'Interpersonal', 'Intrapersonal'], 0, '')], weight=3),
    20: dict(notes=['Communication ethics: the moral standards guiding what we say and how; theory explains and predicts communication.']),
    21: dict(notes=['Employers rank communication skills among the most important qualities in candidates.']),
})

perception = chapter('d02', 20, 'Defining perception, why perceptions differ, the perceptual process (selection, organization by figure–ground, closure, proximity and similarity, interpretation), perception errors (stereotyping, first impressions), and self-concept.', {
    1: dict(notes=['Perception: the process of becoming aware of objects and events through the senses, and interpreting them.']),
    3: dict(notes=['Differences come from physiological factors, identity, temporal conditions, past experiences and roles, present feelings, and current social/political events.']),
    7: dict(notes=['Three stages: SELECTION (what we notice) → ORGANIZATION (grouping) → INTERPRETATION (assigning meaning).'],
            tips=[trick('Select → Organize → Interpret.')],
            exam=[mcq('The perceptual stage in which we assign meaning is:', ['Interpretation', 'Selection', 'Organization', 'Closure'], 0, '')], weight=3),
    9: dict(notes=['Organization: figure and ground (focus vs. background), closure (filling in missing parts), proximity (near things belong together), similarity (alike things belong together).'],
            exam=[mcq('Seeing a broken circle as a complete circle illustrates:', ['Closure', 'Proximity', 'Similarity', 'Figure and ground'], 0, '')], weight=3),
    14: dict(notes=['Errors: stereotyping (judging a person by a group generalization), first impressions that resist new information, prejudice.'],
             exam=[mcq('Assuming every engineer is shy is an example of:', ['Stereotyping', 'Closure', 'Selective attention', 'Feedback'], 0, '')], weight=3),
    17: dict(notes=['Self-concept forms through how others treat us, comparisons, and roles; self-esteem is how we evaluate that concept.']),
})

language = chapter('d03', 23, 'Defining language and its features (rules, culture, organizing reality, arbitrary, abstract), language to avoid (grammatical errors, clichés, euphemisms, profanity, regionalisms, biased language), and improving language skills.', {
    3: dict(notes=['Language: a collection of symbols, letters or words with arbitrary meanings, governed by rules, used to communicate.']),
    6: dict(notes=['Arbitrary: words have no natural connection to what they name; meaning is agreed by convention.'],
            exam=[mcq('That "dog" and "kalb" both name the same animal shows language is:', ['Arbitrary', 'Concrete', 'Biased', 'Universal'], 0, '')], weight=3),
    7: dict(notes=['Abstract vs. concrete: the ladder of abstraction runs from "living creature" down to "my dog Max".']),
    10: dict(notes=['Clichés: overused expressions ("at the end of the day").']),
    11: dict(notes=['Euphemisms: softer substitutes for unpleasant words ("passed away").'],
             exam=[mcq('Saying "let go" instead of "fired" is a:', ['Euphemism', 'Cliché', 'Regionalism', 'Profanity'], 0, '')], weight=3),
    13: dict(notes=['Regionalisms: words used only in a region. Avoid gender-biased, racist, heterosexist and ageist language.']),
    17: dict(notes=['Improve: use descriptiveness (check perceptions, paraphrase), operational definitions, concrete language, and separate observations from inferences.'],
             tips=[trap('An observation is what you saw; an inference is your conclusion about it.')],
             exam=[mcq('"She arrived at 9:20" is an:', ['Observation', 'Inference', 'Euphemism', 'Opinion'], 0, '')], weight=3),
})

nonverbal = chapter('d04', 21, 'Defining nonverbal communication, how it relates to verbal messages, the codes (bodily movement and facial expression, physical attractiveness, space, time, touch, voice, clothing and artifacts), their ambiguity, and how to improve.', {
    3: dict(notes=['Nonverbal communication: messages expressed without words (body, face, space, time, voice, touch, objects).']),
    5: dict(notes=['Nonverbal cues can repeat, emphasize, complement, contradict, substitute for or regulate verbal messages.'],
            exam=[mcq('Nodding while saying "yes" is nonverbal communication that:', ['Repeats the verbal message', 'Contradicts it', 'Substitutes for it', 'Regulates it'], 0, '')], weight=3),
    6: dict(notes=['Kinesics: bodily movement, gestures and facial expressions.']),
    14: dict(notes=['Chronemics (time), proxemics (space: intimate, personal, social, public distances), haptics (touch), vocalics (paralanguage).'],
             exam=[mcq('The study of how people use space is:', ['Proxemics', 'Chronemics', 'Kinesics', 'Haptics'], 0, '')], weight=3),
    17: dict(notes=['Ambiguity: one code can mean many things, and many codes can mean the same thing; context and culture decide.']),
    21: dict(notes=['Nonverbal codes differ across cultures (eye contact, touch, personal space).']),
})

listening = chapter('d05', 27, 'The importance of listening, defining it (vs. hearing), types (active, empathic, critical, for enjoyment), the process (attention, working, short- and long-term memory), barriers, effective listening (nonverbal and verbal), note-taking and ethical listening.', {
    7: dict(notes=['We spend more time listening than speaking, reading or writing.']),
    9: dict(notes=['Hearing: the physical reception of sound. Listening: the active process of receiving, constructing meaning from and responding to messages.'],
            tips=[trap('Hearing is passive and physical; listening is active and mental.')],
            exam=[tf('Hearing and listening are the same thing.', False, '')], weight=3),
    11: dict(notes=['Process: attention (selective, automatic) → working memory → short-term memory → long-term memory.']),
    13: dict(notes=['Barriers: noise (physical, mental, multitasking, factual, semantic distractions), perceptions of others (status, stereotypes), and yourself (egocentrism, defensiveness, experiential superiority, personal bias, pseudolistening).'],
             exam=[mcq('Pretending to listen while thinking about something else is:', ['Pseudolistening', 'Empathic listening', 'Critical listening', 'Paraphrasing'], 0, '')], weight=3),
    20: dict(notes=['Use nonverbal cues effectively: eye contact, forward lean, open posture, nodding.']),
    22: dict(notes=['Check your understanding: ask questions, paraphrase, identify the main points, summarize.']),
    23: dict(notes=['Note-taking methods: outline, mind map, Cornell method.']),
    27: dict(notes=['Ethical listening: recognize your habits, give fair attention, respond appropriately and respectfully.']),
})

interpersonal = chapter('d06', 31, 'Defining interpersonal communication and relationships, their importance and dark side, self-disclosure and the Johari window, friendship and technology, motivations for initiating, maintaining and ending relationships, reducing defensiveness, and essential interpersonal behaviors.', {
    2: dict(notes=['Interpersonal communication: the process of using messages to generate meaning between at least two people in a situation that allows mutual opportunities for speaking and listening.']),
    6: dict(notes=['Interpersonal needs (Schutz): inclusion, affection, control.'],
            exam=[mcq('Schutz’s three interpersonal needs are:', ['Inclusion, affection, control', 'Safety, love, esteem', 'Power, money, fame', 'Trust, respect, honesty'], 0, '')], weight=3),
    7: dict(notes=['Self-disclosure: intentionally sharing personal information. Johari window: open (known to self and others), blind (others know, you don’t), hidden (you know, others don’t), unknown.'],
            exam=[mcq('Information others know about you but you don’t is in the Johari window’s:', ['Blind area', 'Open area', 'Hidden area', 'Unknown area'], 0, '')], weight=3),
    10: dict(notes=['Disclose gradually, reciprocally, appropriately for the relationship and context.']),
    14: dict(notes=['Motivations: initiating (attraction, proximity), maintaining (satisfaction, commitment), terminating (conflict, unmet needs).']),
    20: dict(notes=['Reduce defensiveness (Gibb): description not evaluation, problem orientation not control, spontaneity not strategy, empathy not neutrality, equality not superiority, provisionalism not certainty.'],
             tips=[trick('Supportive climate: describe, solve together, be genuine, empathize, treat as equal, stay open.')], weight=3),
    26: dict(notes=['Essential behaviors: affectionate and supportive communication, influencing others, developing a unique relationship, behavioral flexibility.']),
})

inclusive = chapter('d07', 6, 'Prejudice, unconscious bias and how to manage it, microaggressions, and strategies for more inclusive communication.', {
    1: dict(notes=['Prejudice: an unfair, usually negative attitude toward a group, formed without sufficient knowledge.']),
    2: dict(notes=['Unconscious (implicit) bias: automatic attitudes we aren’t aware of, e.g. affinity bias (favoring people like us). Manage it by noticing it, slowing decisions and seeking diverse contact.'],
            exam=[mcq('Favoring a job candidate because they went to your university is:', ['Affinity bias', 'A microaggression', 'Ethnocentrism', 'Closure'], 0, '')], weight=3),
    3: dict(notes=['Microaggressions: everyday comments or actions that subtly demean a group ("you speak English so well").']),
    4: dict(notes=['Inclusive communication: listen, ask rather than assume, use respectful language and names, learn about other identities.']),
})

groups = chapter('d08', 23, 'Why small groups matter, defining small-group communication, types and functions of groups, group culture and roles, leadership styles and power, problem solving (problem vs. solution questions, criteria), technology in groups, ethics and conflict.', {
    3: dict(notes=['Small group: 3 to about 9 people with a common goal, interdependence, a sense of belonging, and norms.'],
            exam=[mcq('A small group typically has:', ['3 to 9 members', '2 members', '20 or more members', 'Exactly 5 members'], 0, '')], weight=3),
    4: dict(notes=['Types: primary (family, friends) vs. secondary (task) groups; problem-solving, support, learning, social groups.']),
    6: dict(notes=['Roles: task roles (information giver, initiator), maintenance roles (supporter, harmonizer), self-centered roles (blocker, dominator).'],
            exam=[mcq('A member who keeps rejecting every idea without offering alternatives plays a:', ['Self-centered (blocker) role', 'Task role', 'Maintenance role', 'Leadership role'], 0, '')], weight=3),
    11: dict(notes=['Leadership: influencing the group toward its goal.']),
    13: dict(notes=['Styles: autocratic (leader decides), democratic (group decides), laissez-faire (hands-off).'],
             exam=[mcq('A leader who lets the group decide by discussion and voting is:', ['Democratic', 'Autocratic', 'Laissez-faire', 'Coercive'], 0, '')], weight=3),
    15: dict(notes=['Problem solving: define the question → identify criteria → generate potential solutions (brainstorm) → evaluate them → choose and implement.']),
    16: dict(notes=['Discussion questions: of fact, value or policy; problem questions vs. solution questions.']),
    23: dict(notes=['Ethical members: share information honestly, respect others, keep confidences; resolve conflict by focusing on issues, not people.']),
})

DECKS_HERE = [intro, perception, language, nonverbal, listening, interpersonal, inclusive, groups]
