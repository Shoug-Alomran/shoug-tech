"""CS101 annotated slides — Chapter 12: Exception Handling and Text I/O. See ch01_introduction.py for the setup."""
from .common import mcq, scen, short, tf, tip, trap, trick

AUTO_SLIDES = True

DECK = {
    'key': 'ch12',
    'slug': '08-exception-handling-and-text-io',
    'file': 'exception-handling-and-text-io',
    'title': 'Exception Handling and Text I/O',
    'chapter': 'Chapter 12',
    'pdf': '/academics/computer-science/cs101/slides/chapter-12/',
    'lede': ('The File class, writing text with PrintWriter, try-with-resources that closes files automatically, '
             'and reading text with Scanner.'),
}

ANN = {
    1: dict(kind='title', title='Exception Handling and Text I/O', body=[], sub='CS101 · Chapter 12'),
    2: dict(notes=['Objectives: File class, PrintWriter, Scanner, try-with-resources.']),
    3: dict(notes=['File represents a file or directory path; it does NOT read or write contents.'],
            exam=[tf('The File class is used to read the contents of a file.', False, 'It only describes a path; use Scanner/PrintWriter for contents.')], weight=3),
    4: dict(notes=['File methods: exists(), length(), canRead(), isDirectory(), getName(), delete().']),
    5: dict(notes=['Explore file properties.']), 6: dict(notes=['Example code.']),
    7: dict(notes=['Text I/O: PrintWriter writes, Scanner reads.']),
    8: dict(notes=['PrintWriter output = new PrintWriter(file); print/println/printf; close() at the end.'],
            exam=[mcq('Which class writes text data to a file?', ['PrintWriter', 'File', 'Scanner', 'Math'], 0, '')], weight=3),
    9: dict(notes=['Example writing data.']),
    10: dict(notes=['try (PrintWriter out = new PrintWriter(file)) { … } closes the file automatically.'],
             exam=[mcq('try-with-resources is used to:', ['Close resources automatically', 'Create files', 'Catch only syntax errors', 'Sort data'], 0, '')], weight=3),
    11: dict(notes=['Example with try-with-resources.']),
    12: dict(notes=['Scanner input = new Scanner(new File("scores.txt")); while (input.hasNext()) …'],
             tips=[trap('new Scanner("scores.txt") reads the STRING, not the file. Wrap it in new File(...).')], weight=3),
    13: dict(notes=['Example: read from a file and display.']),
    14: dict(notes=['Example code.']), 15: dict(notes=['Example output.']),
}
