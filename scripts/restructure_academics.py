#!/usr/bin/env python3
"""
Restructure the Academics section of My-Garden docs.
macOS is case-insensitive so CS101 == cs101 on disk.
Strategy: rename uppercase dirs to temp names, then to lowercase.
"""

import os
import re
import shutil
import glob
import subprocess
import tempfile

BASE = "/Users/shougalomran/Desktop/My-Garden/docs/Academics"


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def copy_contents(src, dst):
    """Copy contents of src directory into dst directory (merge)."""
    if not os.path.exists(src):
        return
    ensure_dir(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copy_contents(s, d)
        else:
            shutil.copy2(s, d)
    print(f"  [MERGED] {src} -> {dst}")


def copy_file(src, dst):
    """Copy a single file, skip if source doesn't exist."""
    if not os.path.exists(src):
        return
    ensure_dir(os.path.dirname(dst))
    shutil.copy2(src, dst)
    print(f"  [FILE] {os.path.basename(src)} -> {dst}")


def rename_case(path, new_name):
    """
    Rename a directory to new_name (handles case-only renames on macOS
    by going via a temp name).
    path: full path to existing dir (e.g. .../CS101)
    new_name: just the new basename (e.g. cs101)
    """
    parent = os.path.dirname(path)
    old_name = os.path.basename(path)
    if old_name == new_name:
        return path  # already correct
    new_path = os.path.join(parent, new_name)
    if old_name.lower() == new_name.lower():
        # Case-only rename: go via temp
        tmp = os.path.join(parent, f"__tmp_rename_{old_name}__")
        os.rename(path, tmp)
        os.rename(tmp, new_path)
    else:
        os.rename(path, new_path)
    print(f"  [RENAMED] {old_name} -> {new_name}")
    return new_path


# ============================================================
# STEP 1: COMPUTER SCIENCE - rename uppercase dirs to lowercase
# ============================================================
print("\n=== CS: rename uppercase to lowercase ===")
cs = os.path.join(BASE, "computer-science")

for upper, lower in [
    ("CS101", "cs101"), ("CS102", "cs102"), ("CS210", "cs210"),
    ("CS285", "cs285"), ("CS330", "cs330"), ("CS331", "cs331"),
    ("CS340", "cs340"),
]:
    p = os.path.join(cs, upper)
    if os.path.exists(p):
        rename_case(p, lower)

# Now fix internal subdir names inside each course
# cs210: Exams -> extra-resources
print("\n-- cs210 internal renames --")
exams_path = os.path.join(cs, "cs210", "Exams")
if os.path.exists(exams_path):
    # Rename to extra-resources (not case-only, so direct rename)
    er_path = os.path.join(cs, "cs210", "extra-resources")
    ensure_dir(er_path)
    copy_contents(exams_path, er_path)
    shutil.rmtree(exams_path)

# cs285: Cheat-Sheet files are loose in cs285/ - move to extra-resources/
print("\n-- cs285 cheat sheet files --")
for fn in ["Cheat-Sheet.html", "Cheat-Sheet.ar.html"]:
    src = os.path.join(cs, "cs285", fn)
    dst = os.path.join(cs, "cs285", "extra-resources", fn)
    if os.path.exists(src):
        ensure_dir(os.path.dirname(dst))
        shutil.move(src, dst)
        print(f"  [MOVED] {fn} -> extra-resources/")

# cs330: Quizez -> quizzes, Images -> extra-resources, extra-resorces -> extra-resources
print("\n-- cs330 internal renames --")
cs330 = os.path.join(cs, "cs330")
q_old = os.path.join(cs330, "Quizez")
q_new = os.path.join(cs330, "quizzes")
if os.path.exists(q_old):
    rename_case(q_old, "quizzes_tmp")
    os.rename(os.path.join(cs330, "quizzes_tmp"), q_new)

img_path = os.path.join(cs330, "Images")
if os.path.exists(img_path):
    er_path = os.path.join(cs330, "extra-resources")
    ensure_dir(er_path)
    copy_contents(img_path, er_path)
    shutil.rmtree(img_path)

er_misspelled = os.path.join(cs330, "extra-resorces")
if os.path.exists(er_misspelled):
    er_path = os.path.join(cs330, "extra-resources")
    ensure_dir(er_path)
    copy_contents(er_misspelled, er_path)
    shutil.rmtree(er_misspelled)

# cs331: mindmap, summary -> extra-resources/
print("\n-- cs331 internal renames --")
cs331 = os.path.join(cs, "cs331")
for subdir in ["mindmap", "summary"]:
    src = os.path.join(cs331, subdir)
    if os.path.exists(src):
        dst = os.path.join(cs331, "extra-resources", subdir)
        ensure_dir(dst)
        copy_contents(src, dst)
        shutil.rmtree(src)

# cs340: Mindmap -> extra-resources/mindmap, extra-resorces -> extra-resources, quizez -> quizzes
print("\n-- cs340 internal renames --")
cs340 = os.path.join(cs, "cs340")
mindmap_path = os.path.join(cs340, "Mindmap")
if os.path.exists(mindmap_path):
    dst = os.path.join(cs340, "extra-resources", "mindmap")
    ensure_dir(dst)
    copy_contents(mindmap_path, dst)
    shutil.rmtree(mindmap_path)

er_mis = os.path.join(cs340, "extra-resorces")
if os.path.exists(er_mis):
    dst = os.path.join(cs340, "extra-resources")
    ensure_dir(dst)
    copy_contents(er_mis, dst)
    shutil.rmtree(er_mis)

qz_old = os.path.join(cs340, "quizez")
qz_new = os.path.join(cs340, "quizzes")
if os.path.exists(qz_old):
    os.rename(qz_old, os.path.join(cs340, "__qztmp__"))
    os.rename(os.path.join(cs340, "__qztmp__"), qz_new)
    print("  [RENAMED] quizez -> quizzes")

# ============================================================
# STEP 2: MERGE courses/ content into CS course dirs
# ============================================================
print("\n=== Merging courses/ into CS ===")
courses = os.path.join(BASE, "courses")

# cs101
copy_file(f"{courses}/cs101/index.html", f"{cs}/cs101/index.html")

# cs102
copy_file(f"{courses}/cs102/index.html", f"{cs}/cs102/index.html")

# cs210
copy_file(f"{courses}/cs210/index.html", f"{cs}/cs210/index.html")
copy_contents(f"{courses}/cs210/study-material", f"{cs}/cs210/extra-resources")
copy_contents(f"{courses}/cs210/exams", f"{cs}/cs210/extra-resources")
copy_contents(f"{courses}/cs210/topics", f"{cs}/cs210/extra-resources/topics")

# cs285
copy_file(f"{courses}/cs285/index.html", f"{cs}/cs285/index.html")
copy_contents(f"{courses}/cs285/slide-breakdowns", f"{cs}/cs285/slide-breakdowns")
copy_contents(f"{courses}/cs285/study-material", f"{cs}/cs285/extra-resources")

# cs330
copy_file(f"{courses}/cs330/index.html", f"{cs}/cs330/index.html")
copy_contents(f"{courses}/cs330/slide-breakdowns", f"{cs}/cs330/slide-breakdowns")
copy_contents(f"{courses}/cs330/study-material", f"{cs}/cs330/extra-resources")
copy_contents(f"{courses}/cs330/quizzes", f"{cs}/cs330/quizzes")

# cs331
copy_file(f"{courses}/cs331/index.html", f"{cs}/cs331/index.html")
copy_contents(f"{courses}/cs331/slide-breakdowns", f"{cs}/cs331/slide-breakdowns")
copy_contents(f"{courses}/cs331/mindmap", f"{cs}/cs331/extra-resources/mindmap")
copy_contents(f"{courses}/cs331/summary", f"{cs}/cs331/extra-resources/summary")

# cs340
copy_file(f"{courses}/cs340/index.html", f"{cs}/cs340/index.html")
copy_contents(f"{courses}/cs340/slide-breakdowns", f"{cs}/cs340/slide-breakdowns")
copy_contents(f"{courses}/cs340/study-material", f"{cs}/cs340/extra-resources")
copy_contents(f"{courses}/cs340/mindmap", f"{cs}/cs340/extra-resources/mindmap")
copy_contents(f"{courses}/cs340/quizzes", f"{cs}/cs340/quizzes")

# ============================================================
# STEP 3: SOFTWARE ENGINEERING - rename uppercase to lowercase
# ============================================================
print("\n=== SE: rename uppercase to lowercase ===")
se = os.path.join(BASE, "software-engineering")

for upper, lower in [
    ("SE201", "se201"), ("SE311", "se311"), ("SE322", "se322"),
    ("SE401", "se401"), ("SE423", "se423"),
]:
    p = os.path.join(se, upper)
    if os.path.exists(p):
        rename_case(p, lower)

# se201: Images -> extra-resources/Images, Quizez -> quizzes, slide-breakdowns stays
print("\n-- se201 internal renames --")
se201 = os.path.join(se, "se201")
img_p = os.path.join(se201, "Images")
if os.path.exists(img_p):
    dst = os.path.join(se201, "extra-resources", "Images")
    ensure_dir(dst)
    copy_contents(img_p, dst)
    shutil.rmtree(img_p)

qz_p = os.path.join(se201, "Quizez")
if os.path.exists(qz_p):
    dst = os.path.join(se201, "quizzes")
    ensure_dir(dst)
    copy_contents(qz_p, dst)
    shutil.rmtree(qz_p)

# se311: quizez -> quizzes
print("\n-- se311 internal renames --")
se311 = os.path.join(se, "se311")
qz_p = os.path.join(se311, "quizez")
if os.path.exists(qz_p):
    dst = os.path.join(se311, "quizzes")
    os.rename(qz_p, os.path.join(se311, "__qztmp__"))
    os.rename(os.path.join(se311, "__qztmp__"), dst)
    print("  [RENAMED] quizez -> quizzes")

# se311: se-311-summary.pdf -> extra-resources/
pdf_p = os.path.join(se311, "se-311-summary.pdf")
if os.path.exists(pdf_p):
    dst = os.path.join(se311, "extra-resources", "se-311-summary.pdf")
    ensure_dir(os.path.dirname(dst))
    shutil.move(pdf_p, dst)
    print("  [MOVED] se-311-summary.pdf -> extra-resources/")

# ============================================================
# STEP 4: MERGE courses/ into SE
# ============================================================
print("\n=== Merging courses/ into SE ===")

# se201
copy_file(f"{courses}/se201/index.html", f"{se}/se201/index.html")
copy_contents(f"{courses}/se201/slide-breakdowns", f"{se}/se201/slide-breakdowns")
copy_contents(f"{courses}/se201/study-material", f"{se}/se201/extra-resources")
copy_contents(f"{courses}/se201/quizzes", f"{se}/se201/quizzes")

# se311
copy_file(f"{courses}/se311/index.html", f"{se}/se311/index.html")
copy_contents(f"{courses}/se311/slide-breakdowns", f"{se}/se311/slide-breakdowns")
copy_contents(f"{courses}/se311/study-material", f"{se}/se311/extra-resources")
copy_contents(f"{courses}/se311/quizzes", f"{se}/se311/quizzes")

# se322 (no course page likely)
copy_file(f"{courses}/se322/index.html", f"{se}/se322/index.html")

# se401
copy_file(f"{courses}/se401/index.html", f"{se}/se401/index.html")

# se423
copy_file(f"{courses}/se423/index.html", f"{se}/se423/index.html")

# ============================================================
# STEP 5: CYBERSECURITY
# ============================================================
print("\n=== CYBERSECURITY ===")
cyber_old = os.path.join(BASE, "cyber-security")
cyber_new = os.path.join(BASE, "cybersecurity")

# cyber-security -> cybersecurity (not a case-only change)
if os.path.exists(cyber_old) and not os.path.exists(cyber_new):
    os.rename(cyber_old, cyber_new)
    print(f"  [RENAMED] cyber-security -> cybersecurity")
elif os.path.exists(cyber_old):
    copy_contents(cyber_old, cyber_new)
    shutil.rmtree(cyber_old)

# Now rename CYS401 -> cys401, CYS402 -> cys402
for upper, lower in [("CYS401", "cys401"), ("CYS402", "cys402")]:
    p = os.path.join(cyber_new, upper)
    if os.path.exists(p):
        rename_case(p, lower)

# cys401 internal: Quizez -> quizzes
cys401 = os.path.join(cyber_new, "cys401")
qz_p = os.path.join(cys401, "Quizez")
if os.path.exists(qz_p):
    dst = os.path.join(cys401, "quizzes")
    ensure_dir(dst)
    copy_contents(qz_p, dst)
    shutil.rmtree(qz_p)
    print("  [RENAMED] Quizez -> quizzes in cys401")

# Merge courses/cys401
copy_file(f"{courses}/cys401/index.html", f"{cyber_new}/cys401/index.html")
copy_contents(f"{courses}/cys401/slide-breakdowns", f"{cyber_new}/cys401/slide-breakdowns")
copy_contents(f"{courses}/cys401/quizzes", f"{cyber_new}/cys401/quizzes")

# ============================================================
# STEP 6: OTHER COURSES
# ============================================================
print("\n=== OTHER COURSES ===")
other_old = os.path.join(BASE, "other")
other_new = os.path.join(BASE, "other-courses")
ensure_dir(other_new)

# ethcs303
print("\n-- ethcs303 --")
src_base = os.path.join(other_old, "ethc303")
dst_base = os.path.join(other_new, "ethcs303")
copy_contents(f"{src_base}/slides", f"{dst_base}/slides")
copy_contents(f"{src_base}/slide-breakdowns", f"{dst_base}/slide-breakdowns")
copy_contents(f"{src_base}/extra-resources", f"{dst_base}/extra-resources")
copy_contents(f"{src_base}/mindmap", f"{dst_base}/extra-resources/mindmap")
copy_contents(f"{src_base}/quizez", f"{dst_base}/quizzes")
copy_file(f"{courses}/ethcs303/index.html", f"{dst_base}/index.html")
copy_contents(f"{courses}/ethcs303/slide-breakdowns", f"{dst_base}/slide-breakdowns")
copy_contents(f"{courses}/ethcs303/extra-resources", f"{dst_base}/extra-resources")
copy_contents(f"{courses}/ethcs303/mindmaps", f"{dst_base}/extra-resources/mindmap")
copy_contents(f"{courses}/ethcs303/quizzes", f"{dst_base}/quizzes")

# phy205
print("\n-- phy205 --")
copy_contents(f"{other_old}/phy205/slides", f"{other_new}/phy205/slides")
copy_file(f"{courses}/phy205/index.html", f"{other_new}/phy205/index.html")

# eng101
print("\n-- eng101 --")
copy_contents(f"{other_old}/english/ENG101", f"{other_new}/eng101/slides")
copy_contents(f"{other_old}/english/resources", f"{other_new}/eng101/extra-resources")
copy_file(f"{courses}/eng101/index.html", f"{other_new}/eng101/index.html")
copy_contents(f"{courses}/eng101/slides", f"{other_new}/eng101/slide-breakdowns")
copy_contents(f"{courses}/eng101/writing-resources", f"{other_new}/eng101/extra-resources/writing-resources")

# eng103
print("\n-- eng103 --")
copy_contents(f"{other_old}/english/ENG103", f"{other_new}/eng103/slides")

# isc113
print("\n-- isc113 --")
copy_contents(f"{other_old}/Islamic/Islamic-113", f"{other_new}/isc113")
copy_file(f"{courses}/isc113/index.html", f"{other_new}/isc113/index.html")

# Delete old other dir
print("\n-- Removing old 'other' dir --")
if os.path.exists(other_old):
    shutil.rmtree(other_old)
    print(f"  [REMOVED] {other_old}")

# ============================================================
# STEP 7: TRACK PAGES
# ============================================================
print("\n=== TRACK PAGES ===")
tracks = os.path.join(BASE, "tracks")

copy_file(f"{tracks}/computer-science/index.html", f"{cs}/index.html")
copy_file(f"{tracks}/software-engineering/index.html", f"{se}/index.html")
copy_file(f"{tracks}/cybersecurity/index.html", f"{cyber_new}/index.html")
copy_file(f"{tracks}/other-courses/index.html", f"{other_new}/index.html")

print("\n-- Removing tracks dir --")
if os.path.exists(tracks):
    shutil.rmtree(tracks)
    print(f"  [REMOVED] {tracks}")

# ============================================================
# STEP 8: DELETE COURSES DIR
# ============================================================
print("\n-- Removing courses dir --")
if os.path.exists(courses):
    shutil.rmtree(courses)
    print(f"  [REMOVED] {courses}")

# ============================================================
# STEP 9: UPDATE ALL HTML LINKS
# ============================================================
print("\n=== UPDATING HTML LINKS ===")

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

# Order matters: more specific first
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
    # Also fix extra-resorces typo in links
    ("/extra-resorces/", "/extra-resources/"),
]

# D. slide-breakdowns pattern for sub-nav items
tracks_list = ["computer-science", "software-engineering", "cybersecurity", "other-courses"]
courses_list = [
    "cs101", "cs102", "cs210", "cs285", "cs330", "cs331", "cs340",
    "se201", "se311", "se322", "se401", "se423",
    "cys401", "cys402",
    "eng101", "eng103", "ethcs303", "isc113", "phy205"
]
tracks_pattern = "|".join(re.escape(t) for t in tracks_list)
courses_pattern = "|".join(re.escape(c) for c in courses_list)
slide_href_re = re.compile(
    r'(href="/Academics/(?:' + tracks_pattern + r')/(?:' + courses_pattern + r')/)(slides/)(")'
)

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
print("\n=== DONE ===")
