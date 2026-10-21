"""Check the Markdown documents against the team Definition of Done (docs/definition-of-done.md).

Usage:
    python scripts/check_dod.py                    # what CI can check
    python scripts/check_dod.py --source ../diplom # also compare code excerpts with the LearnLab AI source

Exits with status 1 and one line per problem when a document breaks the DoD.
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = ROOT / ".github" / "workflows" / "docs.yml"

# DoD 3: words that add length but no information.
FILLER = ["simply", "basically", "obviously", "clearly", "actually", "really", "very",
          "in order to", "needless to say", "it should be noted", "please note"]
FILLER_RE = re.compile(r"\b(" + "|".join(re.escape(w) for w in FILLER) + r")\b", re.IGNORECASE)

# An excerpt may skip lines with a line that is only "// ..." or "# ...".
ELISION = {"// ...", "# ..."}

ADR_STATUS_RE = re.compile(
    r"^\* \*\*Status:\*\* (Proposed|Accepted|Superseded) \| \*\*Date:\*\* \d{4}-\d{2}-\d{2} \| \*\*Author:\*\* \S"
)
ADR_SECTIONS = ["## Context & Problem Statement", "## Decision Outcome", "## Consequences"]
ADR_MAX_WORDS = 400


def documents():
    return [ROOT / "README.md", *sorted((ROOT / "docs").rglob("*.md"))]


def split_blocks(lines):
    """Return (prose lines with their numbers, code blocks as (marker, start line, code lines))."""
    prose, blocks = [], []
    in_code, code, start, marker = False, [], 0, None
    for no, line in enumerate(lines, 1):
        if line.startswith("```"):
            if in_code:
                blocks.append((marker, start, code))
                in_code, code = False, []
            else:
                in_code, start = True, no
                previous = next((l for l in reversed(lines[: no - 1]) if l.strip()), "")
                m = re.fullmatch(r"<!-- verify: (.+?) -->", previous.strip())
                marker = m.group(1) if m else None
            continue
        if in_code:
            code.append(line)
        else:
            prose.append((no, line))
    return prose, blocks


def check_audience(rel, lines, errors):
    head = lines[:15]
    for field in ("**Audience:**", "**Purpose:**"):
        if not any(l.startswith(field) for l in head):
            errors.append(f"{rel}: DoD 1: no '{field}' line in the first 15 lines")


def check_excerpt(rel, start, path, code, source, errors):
    target = source / path
    if not target.is_file():
        errors.append(f"{rel}:{start}: DoD 2: verify file not found in source: {path}")
        return
    have = [l.strip() for l in target.read_text(encoding="utf-8").splitlines()]
    pos = 0
    for line in code:
        want = line.strip()
        if not want or want in ELISION:
            continue
        try:
            pos = have.index(want, pos) + 1
        except ValueError:
            errors.append(f"{rel}:{start}: DoD 2: line not found in {path} (or out of order): {want}")
            return


def check_code(rel, blocks, source, errors, compared):
    workflow = WORKFLOW.read_text(encoding="utf-8") if WORKFLOW.is_file() else ""
    for marker, start, code in blocks:
        if marker is None:
            errors.append(f"{rel}:{start}: DoD 2: code block has no <!-- verify: ... --> marker")
        elif marker == "run":
            for line in filter(str.strip, code):
                if line.strip() not in workflow:
                    errors.append(f"{rel}:{start}: DoD 2: command is not run by CI: {line.strip()}")
        elif source:
            check_excerpt(rel, start, marker, code, source, errors)
            compared.append(f"{rel}:{start} = {marker}")


def check_links(rel, doc, prose, errors):
    for no, line in prose:
        for target in re.findall(r"\]\(([^)\s]+)\)", line):
            if re.match(r"[a-z]+:", target) or target.startswith("#"):
                continue
            if not (doc.parent / target.split("#")[0]).exists():
                errors.append(f"{rel}:{no}: DoD 2: broken link: {target}")


def check_filler(rel, prose, errors):
    for no, line in prose:
        text = re.sub(r"`[^`]*`", "", line)  # code spans may quote anything
        for m in FILLER_RE.finditer(text):
            errors.append(f"{rel}:{no}: DoD 3: filler word '{m.group(0)}'")


def section(lines, heading):
    start = lines.index(heading) + 1
    end = next((i for i in range(start, len(lines)) if lines[i].startswith("## ")), len(lines))
    return lines[start:end]


def check_adr(rel, lines, prose, errors):
    if not re.match(r"# ADR-\d{3}: \S", lines[0]):
        errors.append(f"{rel}:1: DoD 3: title must be '# ADR-NNN: <decision>'")
    if not any(ADR_STATUS_RE.match(l) for l in lines[:5]):
        errors.append(f"{rel}: DoD 3: no '* **Status:** ... | **Date:** YYYY-MM-DD | **Author:** ...' line")
    missing = [h for h in ADR_SECTIONS if h not in lines]
    for h in missing:
        errors.append(f"{rel}: DoD 3: missing section '{h}'")
    if missing:
        return
    context = " ".join(l for l in section(lines, ADR_SECTIONS[0]) if l.strip())
    sentences = len(re.findall(r"[.!?](\s|$)", context))
    if not 2 <= sentences <= 3:
        errors.append(f"{rel}: DoD 3: context has {sentences} sentences, the template asks for 2 or 3")
    consequences = "\n".join(section(lines, ADR_SECTIONS[2]))
    for field in ("**Positive:**", "**Trade-offs:**"):
        if field not in consequences:
            errors.append(f"{rel}: DoD 3: consequences have no '{field}'")
    words = sum(len(l.split()) for _, l in prose)
    if words > ADR_MAX_WORDS:
        errors.append(f"{rel}: DoD 3: {words} words of prose, the limit is {ADR_MAX_WORDS}")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--source", type=Path, help="LearnLab AI source folder (diplom)")
    args = parser.parse_args()
    if args.source and not args.source.is_dir():
        parser.error(f"--source is not a folder: {args.source}")

    errors, compared = [], []
    docs = documents()
    for doc in docs:
        rel = doc.relative_to(ROOT).as_posix()
        lines = doc.read_text(encoding="utf-8").splitlines()
        prose, blocks = split_blocks(lines)
        check_audience(rel, lines, errors)
        check_code(rel, blocks, args.source, errors, compared)
        check_links(rel, doc, prose, errors)
        check_filler(rel, prose, errors)
        if doc.parent.name == "adr":
            check_adr(rel, lines, prose, errors)

    for e in errors:
        print(e)
    for c in compared:
        print(f"verified excerpt {c}")
    if not args.source:
        print("code excerpts not compared: run with --source <diplom> to compare them")
    print(f"{len(docs)} documents, {len(errors)} DoD problems")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
