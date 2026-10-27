"""Constructors for CS330 annotated-slide content. The markup is the SE423 one (see se423_annotated/ch01_introduction.py)."""
from se423_annotated.common import mcq, scen, section, short, slide, tf, tip, trap, trick  # noqa: F401
from cs331_annotated.common import fig  # noqa: F401

# Every CS330 deck, in course order: key -> (annotated slug, standalone file, slides folder, label).
DECKS = {
    'd01': ('01-introduction-to-operating-systems', 'introduction-to-operating-systems', 'chapter-1-introduction-to-operating-systems', 'Chapter 1: Introduction to Operating Systems'),
    'd02': ('02-operating-system-services', 'operating-system-services', 'chapter-2-operating-system-services', 'Chapter 2: Operating System Services'),
    'd03': ('03-process-management', 'process-management', 'chapter-3-process-management', 'Chapter 3: Process Management'),
    'd04': ('04-threads', 'threads', 'chapter-4-threads', 'Chapter 4: Threads'),
    'd05': ('05-cpu-scheduling', 'cpu-scheduling', 'chapter-5-cpu-scheduling', 'Chapter 5: CPU Scheduling'),
    'd06': ('06-synchronization', 'synchronization', 'chapter-6-synchronization', 'Chapter 6: Synchronization'),
    'd07': ('07-memory-management', 'memory-management', 'chapter-8-memory-management', 'Chapter 8: Memory Management'),
    'd08': ('08-virtual-memory', 'virtual-memory', 'chapter-9-virtual-memory', 'Chapter 9: Virtual Memory'),
    'd09': ('09-file-system-interface', 'file-system-interface', 'chapter-11-file-system-interface', 'Chapter 11: File System Interface'),
    'd10': ('10-file-system-implementation', 'file-system-implementation', 'chapter-12-file-system-implementation', 'Chapter 12: File System Implementation'),
}

# The real CS330 papers in exams/.
PAPERS = {
    'q1': ('Quiz 1 (Ch. 1 & 2)', '08-quiz-1-ch-1-and-2'),
}


def past(paper, label, related=False):
    assert paper in PAPERS, paper
    return {'paper': paper, 'label': label, 'related': related}


def see(deck, n, label):
    assert deck in DECKS, deck
    return {'deck': deck, 'n': n, 'label': label}
