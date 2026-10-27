"""CS102 annotated slides — Java Collection Framework (parts 1 and 2) and Linked Lists.
See decks_a.py for how several decks share one module."""
from .common import mcq, scen, short, tf, tip, trap, trick


class collections:
    AUTO_SLIDES = True
    DECK = {'key': 'collections', 'slug': '06-java-collection-framework', 'file': 'java-collection-framework', 'title': 'Java Collection Framework',
            'chapter': 'Collections', 'pdf': '/academics/computer-science/cs102/slides/java-collection-framework/',
            'lede': ('The Collections Framework (interfaces, implementations, algorithms), Collection vs. Map, Set vs. List, '
                     'ArrayList and its methods, iterators, the diamond <>, Collections.sort and Collections.binarySearch.')}
    ANN = {
        3: dict(notes=['Java Collections Framework: interfaces + classes that implement common data structures and algorithms (java.util).']),
        4: dict(notes=['Three parts: interfaces, implementations (classes), algorithms (static methods in Collections).']),
        5: dict(notes=['Core interfaces: Collection, Set (no duplicates), List (ordered, duplicates allowed), Queue, Map (key → value).'],
                exam=[mcq('Which collection type does NOT allow duplicate elements?', ['Set', 'List', 'ArrayList', 'LinkedList'], 0, '')], weight=3),
        8: dict(notes=['Map is NOT a Collection: it stores key–value pairs.'],
                exam=[tf('Map extends the Collection interface.', False, '')], weight=3),
        13: dict(notes=['List: ordered, duplicates allowed, zero-based indexes (ArrayList, LinkedList).']),
        15: dict(notes=['ArrayList: like an array but resizes automatically; holds objects only (Integer, not int).'],
                 exam=[mcq('An ArrayList<int> declaration:', ['Does not compile (use ArrayList<Integer>)', 'Works fine', 'Creates an int array', 'Is a runtime error'], 0, '')], weight=3),
        19: dict(notes=['Methods: add, add(index, e), get, set, remove, size, contains, indexOf, clear, isEmpty.'],
                 exam=[mcq('Which returns the number of elements in an ArrayList list?', ['list.size()', 'list.length', 'list.length()', 'list.count()'], 0, '')], weight=3),
        24: dict(notes=['Iterator: hasNext(), next(), remove(): the safe way to remove while iterating.'],
                 exam=[tf('Removing elements from a list inside a for-each loop is safe.', False, 'Use an Iterator’s remove() (else ConcurrentModificationException).')], weight=3),
        27: dict(notes=['Java 7 diamond: List<String> list = new ArrayList<>();']),
        28: dict(notes=['Collections.sort(list) sorts a List (natural order or with a Comparator).']),
        32: dict(notes=['Collections.binarySearch(sortedList, key) returns the index, or −(insertion point) − 1 if absent. The list must be sorted first.'],
                 exam=[mcq('Collections.binarySearch requires the list to be:', ['Sorted', 'Unsorted', 'A Set', 'Synchronized'], 0, '')], weight=3),
    }


class collections_2:
    AUTO_SLIDES = True
    DECK = {'key': 'collections-2', 'slug': '10-java-collection-framework-part-2', 'file': 'java-collection-framework-part-2',
            'title': 'Java Collection Framework Part 2', 'chapter': 'Collections', 'pdf': '/academics/computer-science/cs102/slides/java-collection-framework-part-2/',
            'lede': 'Sets (HashSet, TreeSet / SortedSet) and maps (HashMap, TreeMap): how they store data, ordering, and their main methods.'}
    ANN = {
        4: dict(notes=['Set: no duplicates. HashSet: no order. TreeSet: sorted.']),
        6: dict(notes=['TreeSet implements SortedSet: elements kept in ascending order; first(), last(), headSet, tailSet.'],
                exam=[mcq('Which set keeps its elements in sorted order?', ['TreeSet', 'HashSet', 'ArrayList', 'HashMap'], 0, '')], weight=3),
        10: dict(notes=['HashSet: fast add/contains/remove by hashing, no ordering, duplicates ignored.'],
                 exam=[mcq('Adding "a" twice to a HashSet<String> gives a size of:', ['1', '2', '0', 'Exception'], 0, '')], weight=3),
        15: dict(notes=['HashMap: key → value lookups; put, get, containsKey, remove, keySet; keys unique.'],
                 exam=[mcq('map.put("x", 1); map.put("x", 2); map.get("x") returns:', ['2', '1', 'null', '[1, 2]'], 0, 'The second put replaces the value.')], weight=3),
        19: dict(notes=['TreeMap: like HashMap but keys are kept sorted; HashMap has no order.'],
                 tips=[trick('Hash = fast, no order. Tree = sorted.')], weight=3),
    }


class linked_lists:
    AUTO_SLIDES = True
    DECK = {'key': 'linked-lists', 'slug': '07-linked-lists', 'file': 'linked-lists', 'title': 'Linked Lists', 'chapter': 'Linked Lists',
            'pdf': '/academics/computer-science/cs102/slides/linked-lists/',
            'lede': 'Linked data structures, the generic LinkedList<E> class and its operations, iterators, sorting a LinkedList with a Comparator, and PriorityQueue.'}
    ANN = {
        2: dict(notes=['A linked structure: nodes holding data and a reference to the next node.']),
        4: dict(notes=['Dynamic: grows and shrinks one node at a time; no fixed size.'],
                exam=[mcq('Compared with ArrayList, LinkedList is better at:', ['Inserting and removing at the ends or in the middle via an iterator', 'Random access by index', 'Using less memory per element', 'Sorting faster'], 0, '')], weight=3),
        6: dict(notes=['LinkedList<E> is generic; E = element type.']),
        8: dict(notes=['Methods: add, addFirst, addLast, getFirst, getLast, removeFirst, removeLast, get, size.'],
                exam=[mcq('Which method inserts at the front of a LinkedList?', ['addFirst', 'push_front', 'insert(0)', 'prepend'], 0, '')], weight=2),
        10: dict(notes=['Iterators traverse the list: hasNext(), next(); ListIterator goes both ways.']),
        17: dict(notes=['Sort a LinkedList of objects with Collections.sort(list, comparator).']),
        23: dict(notes=['PriorityQueue: poll() always returns the smallest (highest-priority) element.'],
                 exam=[mcq('A PriorityQueue<Integer> holding 5, 1, 3: poll() returns:', ['1', '5', '3', 'The first inserted'], 0, '')], weight=3),
    }


DECKS_HERE = [collections, collections_2, linked_lists]
