"""CS101 annotated slides — Chapter 4: Mathematical Functions, Characters, and Strings. See ch01_introduction.py for the setup."""
from .common import mcq, scen, short, tf, tip, trap, trick

AUTO_SLIDES = True

DECK = {
    'key': 'ch4',
    'slug': '04-mathematical-functions-characters-and-strings',
    'file': 'mathematical-functions-characters-and-strings',
    'title': 'Mathematical Functions, Characters, and Strings',
    'chapter': 'Chapter 4',
    'pdf': '/academics/computer-science/cs101/slides/chapter-4/',
    'lede': ('The Math class (trigonometric, exponent, rounding, min/max/abs, random), the char type, Unicode and '
             'ASCII, escape sequences, casting between char and numbers, the Character methods, String methods '
             '(length, charAt, concatenation, comparison, substring, indexOf), conversions, and printf formatting.'),
}

ROUND = 'Rounding: Math.ceil(2.1) = 3.0 · Math.floor(2.9) = 2.0 · Math.rint(2.5) = 2.0 (nearest even) · Math.round(2.5) = 3 (returns int/long).'

ANN = {
    1: dict(kind='title', title='Mathematical Functions, Characters, and Strings', body=[], sub='CS101 · Chapter 4', tips=[tip(ROUND)]),
    2: dict(notes=['Motivation: compute triangle angles, work with characters and text.']),
    3: dict(notes=['Objectives.']),
    4: dict(notes=['Java provides common math functions in the Math class.']),
    5: dict(notes=['Math class: constants PI and E; methods are static (Math.sqrt(4)).']),
    6: dict(notes=['Trigonometric methods use radians: sin, cos, tan, asin, toRadians, toDegrees.']),
    7: dict(notes=['Exponent methods: exp, log (natural), log10, pow, sqrt.'],
            exam=[mcq('Math.pow(2, 3) returns:', ['8.0', '6.0', '9.0', '8 (int)'], 0, 'pow returns a double.')], weight=2),
    8: dict(notes=['Rounding: ceil, floor, rint, round.'], tips=[tip(ROUND)]),
    9: dict(notes=['Rounding examples.'],
            exam=[mcq('Math.round(-2.5) returns:', ['-2', '-3', '-2.0', '-3.0'], 0, 'round(x) = floor(x + 0.5).'),
                  mcq('Math.ceil(4.1) returns:', ['5.0', '4.0', '5', '4'], 0, '')], weight=3),
    10: dict(notes=['min, max, abs.']),
    11: dict(notes=['Math.random() returns a double in [0.0, 1.0). a + Math.random() * b gives [a, a + b).'],
             exam=[short('Write an expression for a random int between 10 and 49 inclusive.', '10 + (int)(Math.random() * 40)')], weight=3),
    12: dict(notes=['Case study: angles of a triangle with Math.acos and the law of cosines.']),
    13: dict(notes=['char holds one character: char letter = \'A\';']),
    14: dict(notes=['Java uses Unicode (16-bit): \\u0041 = A.']),
    15: dict(notes=['ASCII: \'0\'–\'9\' = 48–57, \'A\'–\'Z\' = 65–90, \'a\'–\'z\' = 97–122.'],
             exam=[mcq('The ASCII/Unicode value of \'a\' is:', ['97', '65', '48', '122'], 0, '')], weight=3),
    16: dict(notes=['Escape sequences: \\b \\t \\n \\f \\r \\\\ \\" .']),
    17: dict(notes=['ASCII table.']), 18: dict(notes=['ASCII table continued.']),
    19: dict(notes=['char ↔ int: (int)\'A\' = 65, (char)97 = \'a\'; \'a\' + 1 = 98.'],
             exam=[mcq('What does System.out.println((char)(\'a\' + 2)); print?', ['c', '99', 'a2', 'b'], 0, '')], weight=3),
    20: dict(notes=['Characters compare by their codes: \'a\' < \'b\' is true.']),
    21: dict(notes=['Character methods: isDigit, isLetter, isLetterOrDigit, isLowerCase, isUpperCase, toLowerCase, toUpperCase.']),
    22: dict(notes=['String is a reference type (a class), not primitive.']),
    23: dict(notes=['String methods: length(), charAt(i), concat(s), toUpperCase(), toLowerCase(), trim().']),
    24: dict(notes=['Instance methods are called on a string object: message.length().']),
    25: dict(notes=['length() returns the number of characters.']),
    26: dict(notes=['charAt(index): indexes start at 0; the last is length() − 1.'],
             tips=[trap('s.charAt(s.length()) throws StringIndexOutOfBoundsException.')],
             exam=[mcq('For s = "Welcome", s.charAt(3) is:', ['c', 'l', 'o', 'e'], 0, 'W0 e1 l2 c3.')], weight=3),
    27: dict(notes=['toUpperCase, toLowerCase, trim (removes leading/trailing whitespace).']),
    28: dict(notes=['+ concatenates: "Chapter" + 2 = "Chapter2"; s1.concat(s2).'],
             exam=[mcq('What is "1" + 2 + 3?', ['"123"', '"6"', '6', '"15"'], 0, 'Left to right: "1" + 2 = "12", then "123".')], weight=3),
    29: dict(notes=['next() reads a word; nextLine() reads the whole line.']),
    30: dict(notes=['Read a char: input.nextLine().charAt(0).']),
    31: dict(notes=['Compare strings with equals / equalsIgnoreCase / compareTo, never ==.'],
             tips=[trap('== compares references, not contents.')],
             exam=[mcq('Which correctly checks that two Strings have the same contents?', ['s1.equals(s2)', 's1 == s2', 's1 = s2', 's1.compare(s2)'], 0, '')], weight=3),
    32: dict(notes=['substring(begin) and substring(begin, end), end exclusive.'],
             exam=[mcq('"Welcome to Java".substring(0, 7) returns:', ['"Welcome"', '"Welcome "', '"Welcom"', '"Welcome t"'], 0, '')], weight=3),
    33: dict(notes=['indexOf(ch), indexOf(s), lastIndexOf(...) return −1 if not found.']),
    34: dict(notes=['More indexOf examples.']),
    35: dict(notes=['Integer.parseInt("12"), Double.parseDouble("1.5"); number to String: "" + number.']),
    36: dict(notes=['Guessing a birthday with five sets.']), 37: dict(notes=['The math behind it: binary digits.']),
    38: dict(notes=['Hex digit to decimal: \'A\'–\'F\' → 10–15.']), 39: dict(notes=['Revised lottery with strings.']),
    40: dict(notes=['printf formats output: System.out.printf("%.2f", x);']),
    41: dict(notes=['Specifiers: %b boolean, %c char, %d int, %f float/double, %e scientific, %s string; width and precision: %8.2f.'],
             exam=[mcq('System.out.printf("%.2f", 3.14159) prints:', ['3.14', '3.142', '3.14159', '3'], 0, '')], weight=3),
    42: dict(notes=['FormatDemo: a formatted table.']),
}
