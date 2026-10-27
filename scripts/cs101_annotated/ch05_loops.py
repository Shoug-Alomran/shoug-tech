"""CS101 annotated slides — Chapter 5: Loops. See ch01_introduction.py for the setup."""
from .common import mcq, scen, short, tf, tip, trap, trick

AUTO_SLIDES = True

DECK = {
    'key': 'ch5',
    'slug': '05-loops',
    'file': 'loops',
    'title': 'Loops',
    'chapter': 'Chapter 5',
    'pdf': '/academics/computer-science/cs101/slides/chapter-5/',
    'lede': ('while, do-while and for loops, sentinel values, which loop to use, nested loops, numerical errors, '
             'break and continue, and the classic loop problems: guessing numbers, GCD, future tuition, '
             'palindromes and primes.'),
}

LOOPS = 'while: test first, may run 0 times · do-while: test after, runs at least once · for: counter loops (init; condition; update).'

ANN = {
    1: dict(kind='title', title='Loops', body=[], sub='CS101 · Chapter 5', tips=[tip(LOOPS)]),
    2: dict(notes=['Loops repeat statements instead of copying them 100 times.']),
    3: dict(notes=['Opening problem: print a string 100 times.']),
    4: dict(notes=['while (count < 100) { …; count++; }']),
    5: dict(notes=['while loop: checks the condition before each iteration.']),
    6: dict(notes=['while flowchart.'],
            exam=[mcq('How many times does int i = 0; while (i < 5) i++; run the body?', ['5', '4', '6', 'Infinite'], 0, '')], weight=3),
    7: dict(notes=['Trace.']), 8: dict(notes=['Trace.']), 9: dict(notes=['Trace.']), 10: dict(notes=['Trace.']), 11: dict(notes=['Trace.']),
    12: dict(notes=['Trace.']), 13: dict(notes=['Trace.']), 14: dict(notes=['Trace.']), 15: dict(notes=['Trace.']),
    16: dict(notes=['Repeat a question until the answer is correct.']),
    17: dict(notes=['Sentinel value: a special input (e.g., 0) that ends the loop.']),
    18: dict(notes=['Advanced math tool: ten questions, count correct answers.']),
    19: dict(notes=['Guessing numbers: higher/lower until correct.']),
    20: dict(notes=['Caution: don’t compare floating-point values for equality in loop conditions.'],
             tips=[trap('while (item != 0) with doubles may never stop because of round-off.')], weight=2),
    21: dict(notes=['do-while: body first, then test: runs at least once.'],
             exam=[mcq('Which loop always executes its body at least once?', ['do-while', 'while', 'for', 'for-each'], 0, '')], weight=3),
    22: dict(notes=['Exercise: read an ASCII code and print its character.']),
    23: dict(notes=['for (initial-action; continuation-condition; action-after-each-iteration).'],
             exam=[mcq('How many lines does for (int i = 1; i <= 10; i += 3) print?', ['4', '3', '10', '5'], 0, 'i = 1, 4, 7, 10.')], weight=3),
    24: dict(notes=['Trace.']), 25: dict(notes=['Trace.']), 26: dict(notes=['Trace.']), 27: dict(notes=['Trace.']), 28: dict(notes=['Trace.']),
    29: dict(notes=['Trace.']), 30: dict(notes=['Trace.']), 31: dict(notes=['Trace.']), 32: dict(notes=['Trace.']), 33: dict(notes=['Trace.']),
    34: dict(notes=['The initial and update parts may hold several comma-separated statements.']),
    35: dict(notes=['If the condition is omitted it is implicitly true: for ( ; ; ) is infinite.']),
    36: dict(notes=['Caution: a semicolon right after for (...) ; makes an empty body.'],
             exam=[short('What is wrong with: for (int i = 0; i < 10; i++); { System.out.println("i is " + i); }', 'The semicolon gives the loop an empty body; the block runs once afterwards (and i is out of scope there, so it does not even compile).')], weight=3),
    37: dict(notes=['Same caution for while.']),
    38: dict(notes=['The three loops are equivalent; use for when the count is known, while for unknown counts, do-while when the body must run first.'], weight=2),
    39: dict(notes=['Recommendations on choosing loops.']),
    40: dict(notes=['Nested loops: the inner loop runs fully for each outer iteration (multiplication table).'],
             exam=[mcq('for (i = 0; i < 3; i++) for (j = 0; j < 4; j++) print. How many prints?', ['12', '7', '3', '4'], 0, '')], weight=3),
    41: dict(notes=['Minimize numerical errors: accumulate small numbers first, use integer counters.']),
    42: dict(notes=['GCD by testing k from 2 up while k ≤ n1 and k ≤ n2.']),
    43: dict(notes=['Future tuition: years until tuition doubles at 7% a year.']),
    44: dict(notes=['break exits the loop; continue skips to the next iteration.']),
    45: dict(notes=['break example: stop when sum > 100.'],
             exam=[mcq('Which statement immediately ends the innermost loop?', ['break', 'continue', 'return 0', 'exit'], 0, '')], weight=3),
    46: dict(notes=['continue example: skip 10 and 11 in the sum.'],
             exam=[mcq('continue in a loop:', ['Skips the rest of the current iteration', 'Ends the loop', 'Restarts the program', 'Ends the method'], 0, '')], weight=3),
    47: dict(notes=['Guessing number with break.']),
    48: dict(notes=['Palindrome: compare characters from both ends moving inward.']),
    49: dict(notes=['Prime test: divide by 2 … sqrt(n); prime if no divisor found.'],
             exam=[short('Write a loop that checks whether n > 1 is prime.', 'boolean isPrime = true; for (int d = 2; d <= Math.sqrt(n); d++) { if (n % d == 0) { isPrime = false; break; } }')], weight=3),
    50: dict(notes=['Display the first 50 primes, 10 per line.']),
}
