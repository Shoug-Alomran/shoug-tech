"""SE423 chapter quiz content (scripts/build_se423_quizzes.py renders it).

Writing rules (the user's, see build_se423_quizzes.py for the checks):
- multiple choice: options[0] is the correct answer; the page spreads answers evenly over A–D.
  Keep every option about the same length, and never add a hint (brackets, extra detail) that
  only the correct option has;
- short answer: ask exactly what the rubric grades. If the question names two things, the rubric
  has those two points and nothing else;
- mix the types: multiple choice, true/false, matching, ordering, calculation, scenario, short answer.
"""


def MCQ(q, correct, *wrong, why="", tag=None, wrong_why=None):
    return {"type": "mcq", "q": q, "options": [correct, *wrong], "why": why, "tag": tag, "wrong": wrong_why or []}


def TF(q, a, why, tag=None):
    return {"type": "tf", "q": q, "a": bool(a), "why": why, "tag": tag}


def MATCH(q, pairs, why="", extra=None, tag=None, each=0.5):
    return {"type": "match", "q": q, "pairs": [list(p) for p in pairs], "why": why, "extra": extra or [], "tag": tag, "each": each}


def ORDER(q, items, why="", tag=None, pts=2):
    return {"type": "order", "q": q, "items": items, "why": why, "tag": tag, "pts": pts}


def NUM(q, answer, unit="", work="", tol=None, tag=None, pts=1):
    return {"type": "num", "q": q, "answer": round(answer, 4), "unit": unit, "work": work, "tol": tol, "tag": tag, "pts": pts}


def SHORT(q, rubric, model, pts=None, need=None, tag=None, rows=3):
    return {"type": "short", "q": q, "rubric": [[label, kws] for label, kws in rubric], "model": model,
            "pts": pts, "need": need, "tag": tag, "rows": rows}


def SCENARIO(title, text, parts, tag=None):
    return {"type": "scenario", "title": title, "text": text, "parts": parts, "tag": tag}
