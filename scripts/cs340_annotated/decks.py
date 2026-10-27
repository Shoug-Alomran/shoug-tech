"""CS340 annotated slides — every Database Systems deck (Elmasri & Navathe, chapters 1–7, 9, 10).

One module holds all the decks: each deck is a namespace class with DECK and ANN (and AUTO_SLIDES).
Slides without an ANN entry are shown without notes. past('mid', ...) and past('f251', ...) point at
the midterm and the Final 251 replica in exams/. See cs331_annotated/ch01_1_introduction.py for the ANN keys."""
from .common import DECKS, mcq, past, see, short, tf, tip, trap, trick


def deck(key, title, chapter, lede):
    slug, file, folder, _ = DECKS[key]
    return {'key': key, 'slug': slug, 'file': file, 'title': title, 'chapter': chapter,
            'pdf': '/academics/computer-science/cs340/slides/%s/' % folder, 'lede': lede}


def cover(title, chapter):
    return dict(kind='title', title=title, body=[], sub='CS340 · %s' % chapter)


class intro:
    AUTO_SLIDES = True
    DECK = deck('d01', 'Introduction to Databases', 'Chapter 1',
                'What a database and a DBMS are, why a DBMS beats a file-based system, what a DBMS does, the steps '
                'for designing a database (conceptual, logical, optimization, querying, applications), and the main '
                'characteristics of the database approach.')
    ANN = {
        1: cover('Introduction to Databases', 'Chapter 1'),
        3: dict(notes=['Database: an organized collection of related data. DBMS: the software that defines, builds, manipulates and shares it (Oracle, PostgreSQL, MySQL, MongoDB).']),
        5: dict(notes=['File-based systems: each application owns its files → redundancy, inconsistency, hard access, no concurrency control, weak security.'],
                past=[past('mid', 'Q2: storing the same data in many places')],
                exam=[mcq('Storing the same data in many places is called:', ['Redundancy', 'Iteration', 'Concurrency', 'Multiplication'], 0, '')], weight=3),
        6: dict(notes=['Database = the data; DBMS = what manages it. Data = entities + relationships.']),
        8: dict(notes=['DBMS functions: define (structure, types, constraints), construct, manipulate (query, update), share, protect, maintain.']),
        9: dict(notes=['Objectives: data availability, integrity (correct data), security (authorized users only), independence.']),
        10: dict(notes=['Characteristics: self-describing (catalog / metadata), program–data independence, multiple views, sharing and multi-user transactions.'],
                 exam=[mcq('A database is "self-describing" because it stores:', ['Its own metadata in a catalog', 'Only application code', 'Backups of itself', 'User passwords'], 0, '')], weight=3),
        11: dict(notes=['Design steps in order: conceptual modeling → logical modeling → optimization → querying → build the application.'],
                 past=[past('mid', 'Q1: the design steps in order')],
                 exam=[mcq('Correct order for designing a database:', ['Conceptual, logical, optimize, query, application', 'Logical, conceptual, query, optimize, application', 'Application, query, logical, conceptual, optimize', 'Conceptual, optimize, logical, application, query'], 0, '')], weight=3),
        12: dict(notes=['Conceptual modeling = ER diagrams.']), 13: dict(notes=['Logical modeling = the relational model (tables).']),
        14: dict(notes=['Optimization = normalization: capture everything, take less space, avoid anomalies.'], seen=[see('d08', 8, 'normalization')]),
        15: dict(notes=['Querying uses SQL.']),
        27: dict(notes=['Transactions must be ACID: Atomicity, Consistency, Isolation, Durability.'],
                 past=[past('mid', 'Q6: the property that survives failures')],
                 tips=[trick('Durability = Doesn’t disappear after commit.')],
                 exam=[mcq('Which ACID property ensures committed changes persist despite failures?', ['Durability', 'Atomicity', 'Consistency', 'Isolation'], 0, ''),
                       mcq('All of a transaction’s operations happen or none do. This is:', ['Atomicity', 'Durability', 'Isolation', 'Consistency'], 0, '')], weight=3),
        28: dict(notes=['You may not need a DBMS for small, simple, single-user, fixed data, or when the overhead isn’t worth it.']),
    }


class concepts:
    AUTO_SLIDES = True
    DECK = deck('d02', 'Concepts, Architecture and Conceptual Design (ER Model)', 'Chapter 2',
                'Levels of abstraction, schemas and instances, logical and physical data independence, then the ER '
                'model: entities and attribute types, keys, relationships, degree and cardinality ratios, total vs. '
                'partial participation, recursive relationships, weak entities, (min, max) notation and ternary '
                'relationships.')
    ANN = {
        1: cover('Conceptual Design (Entity–Relationship Model)', 'Chapter 2'),
        4: dict(notes=['Three levels: physical (how data is stored), logical / conceptual (what data and relationships), view (part of the database for one user group).']),
        6: dict(notes=['Conceptual level hides the storage details and describes the whole database’s entities, data types, relationships and constraints.'],
                past=[past('mid', 'Q4: the conceptual level')],
                exam=[mcq('What is TRUE about the conceptual level?', ['All of these', 'It describes the database structure conceptually', 'It describes what data is stored and the relationships', 'It hides implementation details'], 0, '')], weight=3),
        7: dict(notes=['Schema = the design (changes rarely). Instance (state) = the data at a moment (changes often).'],
                exam=[tf('The database schema changes every time a row is inserted.', False, 'The instance (state) changes; the schema stays.')], weight=3),
        10: dict(notes=['Data independence: change the schema at one level without changing the next higher level.'],
                 past=[past('mid', 'Q3: changing structures without breaking programs')],
                 exam=[mcq('Which lets you modify data structures without affecting existing programs?', ['Data independence', 'Data dependence', 'Data integration', 'Data relationships'], 0, '')], weight=3),
        11: dict(notes=['Logical data independence: change the conceptual schema (add a column) without changing external views/apps. Harder to achieve.']),
        12: dict(notes=['Physical data independence: change the internal schema (indexes, storage) without changing the conceptual schema.'],
                 exam=[mcq('Adding an index to speed up a query without changing the tables is an example of:', ['Physical data independence', 'Logical data independence', 'Referential integrity', 'Normalization'], 0, '')], weight=3),
        14: dict(notes=['Entity: a distinguishable real-world object. Attributes describe it.']),
        15: dict(notes=['Attribute types: simple vs. composite, single- vs. multi-valued, stored vs. derived, complex.']),
        17: dict(notes=['Multi-valued attribute (double oval): several values, e.g. Colors of a car, Degrees.']),
        18: dict(notes=['Derived attribute (dashed oval): computed from another, e.g. Age from BirthDate.'],
                 exam=[mcq('Age computed from BirthDate is a:', ['Derived attribute', 'Multi-valued attribute', 'Composite attribute', 'Key attribute'], 0, '')], weight=3),
        20: dict(notes=['Key attribute (underlined): unique for every entity in the set. An entity type may have several keys.']),
        31: dict(notes=['Relationship: an association among entities (EMPLOYEE works_for DEPARTMENT).']),
        33: dict(notes=['Degree = number of participating entity types: unary (recursive), binary, ternary.']),
        35: dict(notes=['Cardinality ratio: 1:1, 1:N, M:N, the max number of relationship instances an entity can join.'],
                 exam=[mcq('Students take many courses and courses have many students. The cardinality is:', ['M:N', '1:N', '1:1', 'N:1'], 0, '')], weight=3),
        40: dict(notes=['Total participation (double line): every entity must take part (existence dependency). Partial (single line): some may not.'],
                 exam=[mcq('"Every department must have a manager" is shown with:', ['Total participation (double line) of DEPARTMENT in MANAGES', 'Partial participation', 'A weak entity', 'A derived attribute'], 0, '')], weight=3),
        41: dict(notes=['Recursive relationship: the same entity type in two roles (EMPLOYEE supervises EMPLOYEE).']),
        45: dict(notes=['Weak entity (double rectangle): no key of its own; identified by its owner through an identifying relationship (double diamond) + its partial key (dashed underline).'],
                 past=[past('mid', 'Q7: weak entity participation')],
                 tips=[trap('A weak entity ALWAYS has total participation in its identifying relationship.')],
                 exam=[mcq('A weak entity type always has ____ participation in its identifying relationship.', ['Total', 'Partial', 'Overlapping', 'Disjoint'], 0, '')], weight=3),
        47: dict(notes=['Relationships can have attributes (Hours on WORKS_ON). For M:N they must stay on the relationship.']),
        55: dict(notes=['(min, max) notation: each entity takes part in at least min and at most max instances; min = 0 → partial, min ≥ 1 → total.'],
                 exam=[mcq('(1, N) next to EMPLOYEE on WORKS_FOR means each employee works for:', ['At least one, possibly many', 'Exactly one', 'Zero or one', 'None'], 0, '')], weight=3),
        60: dict(notes=['Ternary relationship: three entity types at once (SUPPLIER supplies PART to PROJECT). Not equivalent to three binary ones.']),
    }


class eer:
    AUTO_SLIDES = True
    DECK = deck('d03', 'The Enhanced ER (EER) Model', 'Chapter 3',
                'Subclasses and superclasses, attribute inheritance, specialization and generalization, attribute-'
                'defined specialization, disjoint vs. overlapping and total vs. partial constraints, hierarchies and '
                'lattices, categories (union types) and aggregation.')
    ANN = {
        1: cover('The Enhanced Entity–Relationship (EER) Model', 'Chapter 3'),
        7: dict(notes=['A subclass is a subset of a superclass (SECRETARY ⊂ EMPLOYEE): IS-A relationship.']),
        14: dict(notes=['A subclass inherits all attributes and relationships of its superclass, and can add its own.']),
        16: dict(notes=['Specialization: top-down, define subclasses of a superclass by distinguishing characteristics.']),
        17: dict(notes=['Generalization: bottom-up, find a common superclass for existing entity types (CAR, TRUCK → VEHICLE).'],
                 exam=[mcq('Combining CAR and TRUCK into a VEHICLE superclass is:', ['Generalization', 'Specialization', 'Aggregation', 'Categorization'], 0, '')], weight=3),
        20: dict(notes=['Attribute-defined (predicate-defined) specialization: membership decided by an attribute value (JobType).']),
        22: dict(notes=['Disjointness: d = disjoint (at most one subclass), o = overlapping (may be in several). Completeness: total (double line, must be in one) or partial.'],
                 tips=[trick('Two independent questions: "can it be in two?" (d/o) and "must it be in one?" (total/partial).')],
                 exam=[mcq('A person can be both a STUDENT and an EMPLOYEE, and some people are neither. The specialization is:', ['Overlapping, partial', 'Disjoint, total', 'Disjoint, partial', 'Overlapping, total'], 0, '')], weight=3),
        32: dict(notes=['Hierarchy: each subclass has one superclass. Lattice: a shared subclass has several superclasses (multiple inheritance).'],
                 exam=[mcq('A STUDENT_ASSISTANT that is both an EMPLOYEE and a STUDENT is a:', ['Shared subclass (lattice)', 'Category', 'Weak entity', 'Disjoint subclass'], 0, '')], weight=3),
        36: dict(notes=['Category (union type): a subclass of the UNION of different superclasses (OWNER is a PERSON or BANK or COMPANY). Inherits from only the one it belongs to.'],
                 tips=[trap('Shared subclass = in ALL its superclasses (intersection). Category = in ONE of them (union).')], weight=3),
        44: dict(notes=['Aggregation: treat a relationship as a higher-level entity so it can join other relationships.']),
    }


class relational:
    AUTO_SLIDES = True
    DECK = deck('d04', 'The Relational Model and DBMS Architecture', 'Chapter 4',
                'DBMS languages (DDL, DML, DCL, TCL), relations, tuples, attributes and domains, characteristics of '
                'relations, domain, key, NULL, entity-integrity and referential-integrity constraints, update '
                'operations and their violations, DBMS modules, and centralized, two-tier and three-tier architectures.')
    ANN = {
        1: cover('The Relational Model', 'Chapter 4'),
        8: dict(notes=['DDL defines structure (CREATE, ALTER, DROP). DML queries and changes data (SELECT, INSERT, UPDATE, DELETE). DCL: GRANT/REVOKE. TCL: COMMIT/ROLLBACK.'],
                past=[past('mid', 'Q8: the language that queries and manipulates data')],
                exam=[mcq('Which language queries and manipulates data?', ['DML', 'DDL', 'DCL', 'TCL'], 0, ''),
                      mcq('ALTER TABLE belongs to:', ['DDL', 'DML', 'DCL', 'TCL'], 0, '')], weight=3),
        14: dict(notes=['Relation = table; tuple = row; attribute = column; domain = set of allowed values; degree = number of attributes; cardinality = number of tuples.'],
                 exam=[mcq('The number of attributes in a relation is its:', ['Degree', 'Cardinality', 'Domain', 'Key'], 0, '')], weight=3),
        19: dict(notes=['Tuples are unordered; values are atomic (1NF); NULL means unknown or not applicable.']),
        23: dict(notes=['Constraint families: inherent (model-based), schema-based (DDL), application-based (business rules).']),
        27: dict(notes=['Domain constraint: each value must come from the attribute’s domain (type, range).']),
        30: dict(notes=['Superkey: any set of attributes that is unique. Key (candidate key): a MINIMAL superkey. Primary key: the chosen candidate key (underlined).'],
                 tips=[trap('Every key is a superkey, but a superkey is a key only if no attribute can be removed.')],
                 exam=[mcq('A minimal superkey is a:', ['Candidate key', 'Foreign key', 'Composite attribute', 'Domain'], 0, '')], weight=3),
        26: dict(notes=['Entity integrity: the primary key can’t be NULL.'],
                 exam=[tf('A primary-key attribute may be NULL if it is unknown.', False, 'Entity integrity.')], weight=3),
        41: dict(notes=['Referential integrity: a foreign key value must match an existing primary key in the referenced relation, or be NULL.'],
                 past=[past('mid', 'Q9, Q11: what a foreign key does')],
                 exam=[mcq('The primary function of a foreign key is to:', ['Link tuples between relations', 'Uniquely identify a tuple', 'Enforce domain constraints', 'Prevent NULLs'], 0, '')], weight=3),
        47: dict(notes=['Insert, delete, update can violate constraints. Insert: domain, key, entity, referential. Delete: only referential.'],
                 exam=[mcq('Deleting a DEPARTMENT row that employees still reference violates:', ['Referential integrity', 'Entity integrity', 'Domain constraint', 'Key constraint'], 0, '')], weight=3),
        50: dict(notes=['On a referential violation from delete: RESTRICT (reject), CASCADE (delete the referencing rows), SET NULL / SET DEFAULT.']),
        56: dict(notes=['DBMS modules: DDL compiler, query compiler and optimizer, runtime processor, stored data manager, concurrency/recovery.']),
        61: dict(notes=['Two-tier: client (UI + application) talks directly to the DB server.']),
        66: dict(notes=['Three-tier: client → application (web) server with business logic → database server. Typical for web apps.'],
                 past=[past('mid', 'Q5: the architecture used by web apps'), past('f251', 'where business logic lives')],
                 exam=[mcq('In a three-tier architecture, business logic lives in:', ['The application (middle) tier', 'The client', 'The database server', 'The DDL compiler'], 0, '')], weight=3),
    }


class mapping:
    AUTO_SLIDES = True
    DECK = deck('d05', 'ER-to-Relational Mapping and DDL', 'Chapter 5',
                'The 7-step ER-to-relational mapping algorithm (strong and weak entities, 1:1, 1:N and M:N '
                'relationships, multivalued attributes, n-ary relationships), basic DDL (CREATE TABLE, keys, foreign '
                'keys, data types, constraints), and step 8 options for mapping specialization.')
    ANN = {
        1: cover('ER-to-Relational Mapping and DDL', 'Chapter 5'),
        7: dict(notes=['Step 1: each strong entity → a relation with its simple attributes; composite attributes → their components; pick a primary key.']),
        15: dict(notes=['Step 2 weak entity: relation with its attributes + the owner’s primary key as a foreign key; PK = owner PK + partial key.'],
                 past=[past('f251', 'mapping a weak entity (Blog_Posting)')],
                 exam=[mcq('The primary key of a relation mapped from a weak entity is:', ['Owner’s PK + the partial key', 'The partial key alone', 'A new surrogate key only', 'The owner’s PK alone'], 0, '')], weight=3),
        16: dict(notes=['CREATE TABLE name (col type constraints, …, PRIMARY KEY (…), FOREIGN KEY (…) REFERENCES other(…));']),
        19: dict(notes=['FOREIGN KEY (Dno) REFERENCES DEPARTMENT(Dnumber) ON DELETE CASCADE / SET NULL.'],
                 exam=[mcq('Which defines a foreign key?', ['FOREIGN KEY (Dno) REFERENCES DEPARTMENT(Dnumber)', 'PRIMARY KEY (Dno) REFERENCES DEPARTMENT', 'Dno REFERENCES KEY', 'FOREIGN (Dno) TO DEPARTMENT'], 0, '')], weight=3),
        24: dict(notes=['Constraints: NOT NULL, UNIQUE, DEFAULT, CHECK (e.g. CHECK (Salary > 0)).']),
        26: dict(notes=['1:1: three choices. Foreign-key approach (best): put the PK of one side as FK in the side with TOTAL participation. Merged relation (both total). Relationship relation.'],
                 exam=[mcq('For 1:1 MANAGES where DEPARTMENT participates totally, the FK goes in:', ['DEPARTMENT', 'EMPLOYEE', 'A new relation', 'Both'], 0, 'The total side avoids NULLs.')], weight=3),
        34: dict(notes=['1:N: put the PK of the "1" side as an FK in the "N" side (plus any relationship attributes).'],
                 tips=[trick('1:N → the FK goes on the MANY side.')],
                 exam=[mcq('EMPLOYEE (N) works for DEPARTMENT (1). Map it by:', ['Adding Dno as a foreign key in EMPLOYEE', 'Adding Ssn as a foreign key in DEPARTMENT', 'Creating a new relation always', 'Merging both relations'], 0, '')], weight=3),
        37: dict(notes=['M:N: a NEW relation with both PKs as FKs; its PK is the combination; relationship attributes go here.'],
                 exam=[mcq('WORKS_ON (M:N, attribute Hours) becomes:', ['WORKS_ON(Essn, Pno, Hours) with PK (Essn, Pno)', 'Pno added to EMPLOYEE', 'Essn added to PROJECT', 'Hours added to EMPLOYEE'], 0, '')], weight=3),
        40: dict(notes=['Multivalued attribute: new relation (attribute + owner PK), PK = both.']),
        43: dict(notes=['n-ary relationship: new relation with all participating PKs as FKs.']),
        46: dict(notes=['Unary 1:N: FK to the same table (Super_ssn → EMPLOYEE.Ssn). Unary M:N: new relation with two FKs to the same table.']),
        52: dict(notes=['Step 8 specialization options: 8A superclass + subclass relations (any case); 8B subclass relations only (total, disjoint); 8C one relation + type attribute (disjoint); 8D one relation + Boolean flags (overlapping).'],
                 exam=[mcq('Mapping option that uses ONE relation with a Boolean flag per subclass suits:', ['Overlapping subclasses', 'Only disjoint subclasses', 'Only total specialization', 'Weak entities'], 0, '')], weight=3),
    }


class basic_sql:
    AUTO_SLIDES = True
    DECK = deck('d06', 'Basic SQL', 'Chapter 6',
                'SQL as a declarative language, SELECT–FROM–WHERE with projection and selection, duplicates and '
                'DISTINCT, renaming, LIKE patterns, arithmetic, BETWEEN, ORDER BY, the set operators UNION / '
                'INTERSECT / EXCEPT, and INSERT, DELETE and UPDATE.')
    ANN = {
        1: cover('Basic SQL', 'Chapter 6'),
        7: dict(notes=['SQL is declarative: say WHAT you want, not how to get it.']),
        17: dict(notes=['Projection = choose columns in SELECT.']),
        18: dict(notes=['Selection = choose rows in WHERE (=, <>, <, >, AND, OR, NOT).'],
                 exam=[mcq('In SQL, rows are filtered in the:', ['WHERE clause', 'SELECT clause', 'FROM clause', 'ORDER BY clause'], 0, '')], weight=3),
        23: dict(notes=['SQL tables are multisets (bags): duplicates are kept unless you write SELECT DISTINCT.'],
                 exam=[tf('SELECT removes duplicate rows by default.', False, 'Use DISTINCT.')], weight=3),
        25: dict(notes=['Rename with AS: SELECT S.sname AS name FROM Sailors AS S.']),
        26: dict(notes=['LIKE: % = any number of characters, _ = exactly one. \'_A%\' = second letter is A.'],
                 exam=[mcq('WHERE name LIKE \'_a%\' matches names whose:', ['Second letter is a', 'First letter is a', 'Last letter is a', 'Length is 2'], 0, '')], weight=3),
        28: dict(notes=['BETWEEN a AND b is INCLUSIVE of both ends.'],
                 exam=[tf('rating BETWEEN 5 AND 7 includes ratings 5 and 7.', True, '')], weight=2),
        30: dict(notes=['ORDER BY col [ASC | DESC]; ascending is the default.']),
        32: dict(notes=['UNION removes duplicates; UNION ALL keeps them. Both queries must be union-compatible (same number and types of columns).']),
        33: dict(notes=['INTERSECT: rows in both. EXCEPT (MINUS): rows in the first but not the second.'],
                 exam=[mcq('Sailors who reserved a red boat but NOT a green boat:', ['Red query EXCEPT green query', 'Red query UNION green query', 'Red query INTERSECT green query', 'Red query UNION ALL green query'], 0, '')], weight=3),
        37: dict(notes=['INSERT INTO T VALUES (…) or INSERT INTO T (cols) VALUES (…); values must respect the constraints.'],
                 past=[past('mid', 'Q16: insert a customer, update an address')]),
        41: dict(notes=['DELETE FROM T WHERE …; without WHERE it deletes every row (the table stays).'],
                 tips=[trap('DELETE FROM T removes the rows; DROP TABLE T removes the table itself.')], weight=3),
        42: dict(notes=['UPDATE T SET col = value WHERE …;'],
                 exam=[mcq('Give every employee in department 5 a 10% raise:', ['UPDATE EMPLOYEE SET Salary = Salary * 1.1 WHERE Dno = 5;', 'UPDATE EMPLOYEE Salary = 1.1 WHERE Dno = 5;', 'ALTER EMPLOYEE SET Salary * 1.1;', 'INSERT INTO EMPLOYEE Salary * 1.1;'], 0, '')], weight=3),
    }


class advanced_sql:
    AUTO_SLIDES = True
    DECK = deck('d07', 'Advanced SQL', 'Chapter 7',
                'NULLs and three-valued logic, nested and correlated subqueries (IN, ANY/ALL, EXISTS, UNIQUE), joins '
                '(inner, natural, outer, multiway), aggregation, GROUP BY and HAVING, views, schema changes with DROP '
                'and ALTER, and running queries from Java with JDBC.')
    ANN = {
        1: cover('Advanced SQL', 'Chapter 7'),
        4: dict(notes=['NULL = unknown, unavailable or not applicable. Test with IS NULL / IS NOT NULL, never = NULL.'],
                tips=[trap('WHERE x = NULL is never true; write WHERE x IS NULL.')],
                exam=[mcq('Which finds employees with no supervisor?', ['WHERE Super_ssn IS NULL', 'WHERE Super_ssn = NULL', 'WHERE Super_ssn = 0', 'WHERE Super_ssn == NULL'], 0, '')], weight=3),
        6: dict(notes=['Three-valued logic: TRUE, FALSE, UNKNOWN. Any comparison with NULL is UNKNOWN; WHERE keeps only TRUE rows.']),
        12: dict(notes=['Nested query: a SELECT inside WHERE (… IN (SELECT …)).']),
        13: dict(notes=['= ANY (SOME) is like IN; > ALL means greater than every value returned.'],
                 exam=[mcq('Salary > ALL (SELECT Salary FROM EMPLOYEE WHERE Dno = 5) finds employees who earn:', ['More than everyone in department 5', 'More than someone in department 5', 'The same as department 5', 'Less than everyone in department 5'], 0, '')], weight=3),
        18: dict(notes=['Correlated subquery: refers to the outer query’s row, so it is re-evaluated for each outer row.']),
        23: dict(notes=['EXISTS (subquery) is TRUE if it returns at least one row; NOT EXISTS if it returns none.'],
                 past=[past('f251', 'borrowers who never borrowed / orders without a Mouse')],
                 exam=[short('Find employees who have no dependents.', 'SELECT Fname, Lname FROM EMPLOYEE E WHERE NOT EXISTS (SELECT * FROM DEPENDENT D WHERE D.Essn = E.Ssn);')], weight=3),
        32: dict(notes=['NATURAL JOIN joins on all same-named columns and keeps one copy of each.']),
        33: dict(notes=['INNER JOIN (the default JOIN): only matching rows.']),
        34: dict(notes=['LEFT/RIGHT/FULL OUTER JOIN also keep unmatched rows from the left/right/both side, padded with NULLs.'],
                 exam=[mcq('List all employees, with their department name if they have one:', ['EMPLOYEE LEFT OUTER JOIN DEPARTMENT', 'EMPLOYEE INNER JOIN DEPARTMENT', 'EMPLOYEE NATURAL JOIN DEPARTMENT', 'EMPLOYEE RIGHT OUTER JOIN DEPARTMENT'], 0, '')], weight=3),
        40: dict(notes=['Aggregates: COUNT, SUM, MAX, MIN, AVG. COUNT(*) counts rows; COUNT(col) ignores NULLs.'],
                 exam=[mcq('COUNT(Super_ssn) on a table where 2 of 8 rows have NULL Super_ssn returns:', ['6', '8', '2', 'NULL'], 0, '')], weight=3),
        49: dict(notes=['GROUP BY splits rows into groups; aggregates are computed per group. Every non-aggregated SELECT column must be in GROUP BY.']),
        53: dict(notes=['HAVING filters GROUPS (after grouping); WHERE filters ROWS (before grouping).'],
                 past=[past('mid', 'Q15: customers whose orders total over $500')],
                 tips=[trick('Condition on an aggregate (SUM, COUNT…) → HAVING.')],
                 exam=[mcq('Departments with more than 5 employees:', ['GROUP BY Dno HAVING COUNT(*) > 5', 'WHERE COUNT(*) > 5 GROUP BY Dno', 'GROUP BY Dno WHERE COUNT(*) > 5', 'HAVING Dno > 5'], 0, '')], weight=3),
        55: dict(notes=['View: a virtual table defined by a query (CREATE VIEW v AS SELECT …).'],
                 past=[past('f251', 'create view AVAILABLE_BOOKS')]),
        57: dict(notes=['Non-materialized views are recomputed on each use; materialized views store the result and must be refreshed.']),
        59: dict(notes=['DROP TABLE removes a table (CASCADE / RESTRICT). ALTER TABLE adds/drops columns or constraints.'],
                 past=[past('f251', 'drop a constraint, rename and resize columns')],
                 exam=[mcq('Remove the foreign-key constraint fk_publisher from BOOK:', ['ALTER TABLE BOOK DROP CONSTRAINT fk_publisher;', 'DROP CONSTRAINT fk_publisher;', 'DELETE fk_publisher FROM BOOK;', 'ALTER BOOK REMOVE fk_publisher;'], 0, '')], weight=3),
        61: dict(notes=['From code: connect (JDBC), prepare a statement, execute, read the ResultSet.']),
    }


class normalization:
    AUTO_SLIDES = True
    DECK = deck('d08', 'Functional Dependencies and Normalization', 'Chapter 9',
                'Informal design guidelines (clear semantics, no anomalies, few NULLs, no spurious tuples), '
                'functional dependencies, keys and prime attributes, 1NF, 2NF, 3NF and BCNF with their general '
                'definitions, lossless decomposition, inference rules and attribute closure, and a full worked example.')
    NF = '1NF: atomic values. 2NF: no PARTIAL dependency on the key. 3NF: no TRANSITIVE dependency. BCNF: every determinant is a superkey.'
    ANN = {
        1: cover('Functional Dependencies and Normalization', 'Chapter 9'),
        2: dict(notes=[NF]),
        9: dict(notes=['Redundancy causes update anomalies.']),
        15: dict(notes=['Update anomaly: changing one fact means changing many rows.']),
        16: dict(notes=['Insert anomaly: can’t add a fact without unrelated data (a new project with no employees).'],
                 past=[past('f251', 'which option shows an insert anomaly')],
                 exam=[mcq('You can’t record a new department until it has an employee. This is a(n):', ['Insertion anomaly', 'Deletion anomaly', 'Update anomaly', 'Spurious tuple'], 0, '')], weight=3),
        17: dict(notes=['Delete anomaly: deleting one fact loses another (last employee of a department deletes the department).']),
        21: dict(notes=['Spurious tuples: wrong rows produced by joining a bad decomposition; join on PK–FK pairs to avoid them.']),
        24: dict(notes=['FD X → Y: whenever two tuples agree on X, they agree on Y.'],
                 exam=[mcq('Ssn → Ename means:', ['Each Ssn has exactly one Ename', 'Each Ename has one Ssn', 'Ssn and Ename are keys', 'Ename determines Ssn'], 0, '')], weight=3),
        35: dict(notes=['An instance can DISPROVE an FD (two rows agree on X but differ on Y) but can never prove one holds.'],
                 exam=[tf('A sample table can prove that an FD holds for all possible data.', False, 'It can only rule FDs out.')], weight=3),
        42: dict(notes=['Prime attribute: member of some candidate key. Nonprime: not in any candidate key.']),
        47: dict(notes=['1NF: every attribute is atomic (no multivalued or composite values, no nested relations).'],
                 past=[past('mid', 'Q12: 1NF and its violations')], weight=3),
        53: dict(notes=['2NF: 1NF + every nonprime attribute is FULLY dependent on the primary key (no partial dependency on part of a composite key).'],
                 past=[past('mid', 'Q13: what 2NF eliminates')],
                 tips=[trap('A relation with a single-attribute primary key is automatically in 2NF.')],
                 exam=[mcq('2NF removes:', ['Partial dependencies on the key', 'Transitive dependencies', 'Multivalued attributes', 'All redundancy'], 0, '')], weight=3),
        56: dict(notes=['3NF: 2NF + no nonprime attribute transitively dependent on the key (key → X → Y with X not a key).'],
                 past=[past('mid', 'Q10, Q14: 3NF'), past('mid', 'Q17: normalize LIBRARY to 3NF', related=True)],
                 exam=[short('EMP_DEPT(Ssn, Ename, Dnumber, Dname) with Ssn → Ename, Dnumber and Dnumber → Dname. Normalize to 3NF.', 'Dname depends transitively on Ssn through Dnumber. Split into EMP(Ssn, Ename, Dnumber) with Dnumber as an FK, and DEPT(Dnumber, Dname).')], weight=3),
        69: dict(notes=['BCNF: for every nontrivial FD X → A, X is a superkey. Stricter than 3NF.'],
                 tips=[tip(NF)],
                 exam=[mcq('A relation is in BCNF if for every nontrivial FD X → A:', ['X is a superkey', 'A is prime', 'X is prime', 'A is a key'], 0, '')], weight=3),
        75: dict(notes=['TEACH(Student, Course, Instructor): in 3NF but not BCNF because Instructor → Course and Instructor is not a key.']),
        78: dict(notes=['Non-additive (lossless) join test for R → R1, R2: (R1 ∩ R2) → (R1 − R2) or (R1 ∩ R2) → (R2 − R1).'], weight=2),
        82: dict(notes=['Armstrong’s axioms: reflexivity (Y ⊆ X ⇒ X → Y), augmentation (X → Y ⇒ XZ → YZ), transitivity (X → Y, Y → Z ⇒ X → Z).']),
        84: dict(notes=['Closure X⁺: all attributes determined by X. If X⁺ contains every attribute, X is a superkey.'],
                 past=[past('f251', 'candidate key of R(A, B, C, D) with A → B → C → D')],
                 exam=[mcq('R(A, B, C, D) with A → B, B → C, C → D. A candidate key is:', ['A', 'B', 'AB', 'D'], 0, 'A⁺ = ABCD.')], weight=3),
        86: dict(notes=['Find a key: start with attributes on no right-hand side (they must be in every key), compute the closure, add attributes until it covers R.']),
    }


class nosql:
    AUTO_SLIDES = True
    DECK = deck('d09', 'NoSQL and Object-Oriented Databases', 'Chapter 10',
                'Relational vs. non-relational databases, NoSQL families, MongoDB documents and collections, JSON '
                'and BSON, CRUD operations in MongoDB, Compass and Atlas, and object-oriented DBMSs compared with '
                'RDBMSs.')
    ANN = {
        1: cover('NoSQL and Object-Oriented Databases', 'Chapter 10'),
        5: dict(notes=['NoSQL ("not only SQL"): flexible or no schema, horizontal scaling, high availability, often relaxed consistency.'],
                past=[past('f251', 'horizontal scaling and why NoSQL is used')],
                exam=[mcq('Horizontal scaling (scaling out) means:', ['Adding more servers', 'Adding more CPU to one server', 'Adding more columns', 'Normalizing the data'], 0, '')], weight=3),
        7: dict(notes=['Families: document (MongoDB), key–value (Redis), column-family (Cassandra), graph (Neo4j).'],
                exam=[mcq('MongoDB is a:', ['Document store', 'Graph database', 'Key–value store only', 'Relational DBMS'], 0, '')], weight=3),
        12: dict(notes=['MongoDB ↔ relational: database ↔ database, collection ↔ table, document ↔ row, field ↔ column, embedding/linking ↔ joins.'],
                 exam=[mcq('In MongoDB, a collection corresponds to a relational:', ['Table', 'Row', 'Column', 'Schema'], 0, '')], weight=3),
        15: dict(notes=['Documents are JSON-like (stored as BSON): objects { } and arrays [ ].']),
        24: dict(notes=['CRUD: insertOne/insertMany, find, updateOne/updateMany ($set), deleteOne/deleteMany.'],
                 exam=[mcq('Which MongoDB call changes a field in matching documents?', ['updateMany({…}, {$set: {…}})', 'find({…})', 'insertMany([…])', 'drop()'], 0, '')], weight=3),
        31: dict(notes=['OODBMS: stores objects directly (identity, encapsulation, inheritance); good for complex objects (CAD, multimedia).'],
                 past=[past('f251', 'what OODBMSs suit')]),
        33: dict(notes=['RDBMS: tables, SQL, simple types. OODBMS: objects with methods, OIDs, no impedance mismatch with OO code.']),
    }


DECKS_HERE = [intro, concepts, eer, relational, mapping, basic_sql, advanced_sql, normalization, nosql]
