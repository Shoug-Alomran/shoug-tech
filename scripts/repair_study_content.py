#!/usr/bin/env python3
"""Undo Prettier's Markdown formatting of study_engine teaching files.

`prettier --write .` treats scripts/study_content/<course>/*.md as Markdown and breaks
the study_engine format:
  - directives after a list get indented ("  @vocab") or pulled into a quote ("> @mcq 6")
  - an MCQ's "+ right" / "- wrong" lines become two lists, re-marked "-" and "*"
  - the question and the "~ keywords" line of a written question get a "> " prefix

The right answer is always written first, so option order identifies it. Safe to re-run
on a file that isn't damaged. Add the folder to .prettierignore to stop it happening.

    python scripts/repair_study_content.py scripts/study_content/econ102/*.md
"""
import re
import sys

DIRECTIVE = re.compile(r"^\s*(?:>\s*)?(@\w+)(.*)$")
BLOCKS = ("vocab", "map", "goals", "cheat")


def repair(text):
    out, mode, opts_seen, in_question = [], None, 0, False
    for raw in text.split("\n"):
        m = DIRECTIVE.match(raw)
        if m and m.group(1)[1:] in ("head", "title", "sources", "count", "tldr", "why", "connect",
                                    "vocab", "map", "goals", "cheat", "mcq", "short"):
            mode = m.group(1)[1:]
            opts_seen, in_question = 0, mode in ("mcq", "short")
            out.append(m.group(1) + m.group(2))
            continue
        if raw.startswith("## "):
            mode = "lesson"
            out.append(raw)
            continue
        line = raw
        if mode == "lesson":
            # Teaching files use no nested lists or code, so indentation is always Prettier's.
            line = raw.strip() if raw.strip().startswith("::") or raw.startswith("   ") else raw
        elif mode in BLOCKS:
            line = raw.strip()
            if mode == "goals" and line and not line.startswith("- "):
                line = "- " + line.lstrip("*+ ")
        elif mode == "mcq":
            line = raw.strip()
            if not line:
                continue
            option = re.match(r"^[-*+]\s+(.*)$", line)
            if option:
                line = ("+ " if opts_seen == 0 else "- ") + option.group(1)
                opts_seen += 1
                in_question = False
            elif in_question:
                line = re.sub(r"^>\s?", "", line)
            elif not line.startswith("> "):
                line = "> " + line
        elif mode == "short":
            line = raw.strip()
            if not line:
                continue
            body = re.sub(r"^>\s?", "", line)
            if body.startswith("~ "):
                line, in_question = body, False
            elif in_question:
                line = body
            else:
                line = "> " + body
        out.append(line)
    return "\n".join(out)


def main():
    for path in sys.argv[1:]:
        with open(path, encoding="utf-8", newline="") as f:
            text = f.read()
        fixed = repair(text.replace("\r\n", "\n"))
        if fixed != text:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(fixed)
            print("repaired", path)


if __name__ == "__main__":
    main()
