#!/usr/bin/env python3
"""Refresh what the About page assistant knows from LinkedIn.

LinkedIn blocks automated reads, so this works from LinkedIn's own data
export: LinkedIn > Settings > Data privacy > Get a copy of your data. Pick
the files you want (Profile, Positions, Education, Certifications, Skills),
download the archive when LinkedIn emails it, then run:

    python3 scripts/sync_linkedin_profile.py ~/Downloads/Basic_LinkedInDataExport_*.zip

It writes docs/ai-context/about/linkedin.json, which the Worker reads (cached
for an hour) once the site is published. No Worker redeploy is needed.

Only an allowlist of public fields is copied. The export also holds things
like your address, birth date, phone numbers, messages and education notes;
none of those are read. Review the printed summary before publishing.
"""
from __future__ import annotations

import csv
import io
import json
import sys
import zipfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "ai-context" / "about" / "linkedin.json"

# file -> {output key: export column}. Nothing outside this map is read.
FIELDS = {
    "Profile.csv": {"headline": "Headline", "summary": "Summary"},
    "Positions.csv": {
        "company": "Company Name",
        "title": "Title",
        "description": "Description",
        "start": "Started On",
        "end": "Finished On",
    },
    "Education.csv": {"school": "School Name", "degree": "Degree Name"},
    "Certifications.csv": {"name": "Name", "authority": "Authority"},
    "Skills.csv": {"name": "Name"},
}


def read_tables(source: Path) -> dict[str, list[dict[str, str]]]:
    files: dict[str, str] = {}
    if source.is_dir():
        for name in FIELDS:
            path = source / name
            if path.exists():
                files[name] = path.read_text(encoding="utf-8-sig")
    else:
        with zipfile.ZipFile(source) as archive:
            for info in archive.infolist():
                name = Path(info.filename).name
                if name in FIELDS:
                    files[name] = archive.read(info).decode("utf-8-sig")
    tables = {}
    for name, text in files.items():
        # Some exports start with a "Notes:" preamble before the header row.
        lines = text.splitlines()
        wanted = set(FIELDS[name].values())
        start = next(
            (i for i, line in enumerate(lines) if wanted & set(next(csv.reader([line]), []))),
            0,
        )
        rows = csv.DictReader(io.StringIO("\n".join(lines[start:])))
        tables[name] = [
            {key: (row.get(col) or "").strip() for key, col in FIELDS[name].items()}
            for row in rows
        ]
    return tables


def build(tables: dict[str, list[dict[str, str]]]) -> dict:
    profile = (tables.get("Profile.csv") or [{}])[0]
    return {
        "syncedAt": date.today().isoformat(),
        "headline": profile.get("headline", ""),
        "summary": profile.get("summary", ""),
        "positions": [p for p in tables.get("Positions.csv", []) if p["title"] or p["company"]],
        "education": [e for e in tables.get("Education.csv", []) if e["school"]],
        "certifications": [c for c in tables.get("Certifications.csv", []) if c["name"]],
        "skills": [s["name"] for s in tables.get("Skills.csv", []) if s["name"]],
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    source = Path(sys.argv[1]).expanduser()
    if not source.exists():
        print(f"Not found: {source}")
        return 1
    tables = read_tables(source)
    if not tables:
        print("No Profile/Positions/Education/Certifications/Skills CSVs found in the export.")
        return 1
    data = build(tables)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")
    print(f"  headline: {data['headline'] or '(none)'}")
    for p in data["positions"]:
        print(f"  position: {p['title']} at {p['company']} ({p['start']} - {p['end'] or 'present'})")
    print(
        f"  {len(data['education'])} education, {len(data['certifications'])} certifications, "
        f"{len(data['skills'])} skills"
    )
    print("This file is public once published. Check it, then commit and push.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
