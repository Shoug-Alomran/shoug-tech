#!/usr/bin/env python3
"""Update all HTML links after Academics restructure."""

import os
import re
import glob

html_roots = [
    "/Users/shougalomran/Desktop/My-Garden/docs/Academics",
    "/Users/shougalomran/Desktop/My-Garden/docs/about",
    "/Users/shougalomran/Desktop/My-Garden/docs/work",
    "/Users/shougalomran/Desktop/My-Garden/docs/workshops",
    "/Users/shougalomran/Desktop/My-Garden/docs/resources",
    "/Users/shougalomran/Desktop/My-Garden/docs/policy",
]
root_html_files = glob.glob("/Users/shougalomran/Desktop/My-Garden/docs/*.html")

def find_html_files(roots):
    found = []
    for root in roots:
        if not os.path.exists(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            for fn in filenames:
                if fn.endswith(".html"):
                    found.append(os.path.join(dirpath, fn))
    return found

html_files = list(set(find_html_files(html_roots) + root_html_files))
print(f"Found {len(html_files)} HTML files to process")

all_replacements = [
    # A. courses/ -> track paths
    ("/Academics/courses/cs101/",    "/Academics/computer-science/cs101/"),
    ("/Academics/courses/cs102/",    "/Academics/computer-science/cs102/"),
    ("/Academics/courses/cs210/",    "/Academics/computer-science/cs210/"),
    ("/Academics/courses/cs285/",    "/Academics/computer-science/cs285/"),
    ("/Academics/courses/cs330/",    "/Academics/computer-science/cs330/"),
    ("/Academics/courses/cs331/",    "/Academics/computer-science/cs331/"),
    ("/Academics/courses/cs340/",    "/Academics/computer-science/cs340/"),
    ("/Academics/courses/cys401/",   "/Academics/cybersecurity/cys401/"),
    ("/Academics/courses/eng101/",  "/Academics/other-courses/eng101/"),
    ("/Academics/courses/ethcs303/", "/Academics/other-courses/ethcs303/"),
    ("/Academics/courses/islm113/",  "/Academics/other-courses/isc113/"),
    ("/Academics/courses/isc113/",   "/Academics/other-courses/isc113/"),
    ("/Academics/courses/phy205/",   "/Academics/other-courses/phy205/"),
    ("/Academics/courses/se201/",    "/Academics/software-engineering/se201/"),
    ("/Academics/courses/se311/",    "/Academics/software-engineering/se311/"),
    ("/Academics/courses/se322/",    "/Academics/software-engineering/se322/"),
    ("/Academics/courses/se401/",    "/Academics/software-engineering/se401/"),
    ("/Academics/courses/se423/",    "/Academics/software-engineering/se423/"),
    # B. uppercase asset paths
    ("/Academics/computer-science/CS101/", "/Academics/computer-science/cs101/"),
    ("/Academics/computer-science/CS102/", "/Academics/computer-science/cs102/"),
    ("/Academics/computer-science/CS210/", "/Academics/computer-science/cs210/"),
    ("/Academics/computer-science/CS285/", "/Academics/computer-science/cs285/"),
    ("/Academics/computer-science/CS330/", "/Academics/computer-science/cs330/"),
    ("/Academics/computer-science/CS331/", "/Academics/computer-science/cs331/"),
    ("/Academics/computer-science/CS340/", "/Academics/computer-science/cs340/"),
    ("/Academics/software-engineering/SE201/", "/Academics/software-engineering/se201/"),
    ("/Academics/software-engineering/SE311/", "/Academics/software-engineering/se311/"),
    ("/Academics/software-engineering/SE322/", "/Academics/software-engineering/se322/"),
    ("/Academics/software-engineering/SE401/", "/Academics/software-engineering/se401/"),
    ("/Academics/software-engineering/SE423/", "/Academics/software-engineering/se423/"),
    ("/Academics/cyber-security/CYS401/", "/Academics/cybersecurity/cys401/"),
    ("/Academics/cyber-security/CYS402/", "/Academics/cybersecurity/cys402/"),
    ("/Academics/other/ethc303/",         "/Academics/other-courses/ethcs303/"),
    ("/Academics/other/phy205/",          "/Academics/other-courses/phy205/"),
    ("/Academics/other/english/ENG101/",  "/Academics/other-courses/eng101/"),
    ("/Academics/other/english/ENG103/",  "/Academics/other-courses/eng103/"),
    ("/Academics/other/Islamic/",         "/Academics/other-courses/isc113/"),
    # C. track paths
    ("/Academics/tracks/computer-science/",     "/Academics/computer-science/"),
    ("/Academics/tracks/software-engineering/", "/Academics/software-engineering/"),
    ("/Academics/tracks/cybersecurity/",        "/Academics/cybersecurity/"),
    ("/Academics/tracks/other-courses/",        "/Academics/other-courses/"),
    # E. study-material -> extra-resources
    ("/study-material/", "/extra-resources/"),
    # F. quizez -> quizzes
    ("/quizez/",  "/quizzes/"),
    ("/Quizez/",  "/quizzes/"),
    # Fix extra-resorces typo in links
    ("/extra-resorces/", "/extra-resources/"),
]

total_updated = 0
for fpath in sorted(html_files):
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  [ERROR] {fpath}: {e}")
        continue

    original = content
    for old, new in all_replacements:
        content = content.replace(old, new)

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        total_updated += 1
        print(f"  [UPDATED] {fpath}")

print(f"\nTotal HTML files updated: {total_updated}")

# Count remaining old path refs
import subprocess

checks = [
    ("/Academics/courses/", "courses/"),
    ("/Academics/tracks/", "tracks/"),
    ("/Academics/cyber-security/", "cyber-security/"),
    ("/Academics/other/", "other/"),
    ("/study-material/", "study-material/"),
    ("/quizez/", "quizez/"),
]

print("\n=== VERIFICATION ===")
for pattern, label in checks:
    result = subprocess.run(
        ["grep", "-r", pattern, "/Users/shougalomran/Desktop/My-Garden/docs", "--include=*.html", "-l"],
        capture_output=True, text=True
    )
    files = [l for l in result.stdout.strip().split('\n') if l]
    count = len(files)
    print(f"  '{label}' remaining in HTML: {count} files")
    if count > 0 and count <= 5:
        for f in files:
            print(f"    {f}")
