#!/usr/bin/env python3
"""Rewrite only the breakdown HTML files of a course, leaving listings and galleries alone.

    .venv/bin/python scripts/rebuild_breakdown_pages.py cs311 [econ101 ...]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_course_study as bcs  # noqa: E402
import build_new_courses as nc  # noqa: E402

for code in (a.upper() for a in sys.argv[1:]):
    c = next(c for c in nc.COURSES if c["code"] == code)
    course = bcs.Course(c)
    for i, deck in enumerate(course.decks, 1):
        folder = os.path.join(course.out, bcs.KINDS["breakdown"][0], deck["slug"])
        nc.write(os.path.join(folder, course.file_name("breakdown", deck)), course.breakdown_page(i, deck))
    print(code, "breakdown pages:", len(course.decks))
