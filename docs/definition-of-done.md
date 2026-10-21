# Team Definition of Done (DoD): Documentation

**Audience:** everyone who writes or reviews a `doc-task` item in this repository.
**Purpose:** one shared meaning of "done" for documents, so a reviewer can check it without asking the author.

A documentation task labeled `doc-task` is DONE if and only if all four items hold. The "Checked by" column says how
each item is proven. `scripts/check_dod.py` runs in CI on every pull request.

| # | Criterion | Done when | Checked by |
| --- | --- | --- | --- |
| 1 | **Target audience fit** | The document starts with an `**Audience:**` line and a `**Purpose:**` line. Every section serves that audience; anything else is cut or linked | `check_dod.py` (both lines present), reviewer (sections fit) |
| 2 | **Technical verifiability** | Every code block has a marker. `<!-- verify: path -->` names the LearnLab AI file that a code excerpt is copied from. `<!-- verify: run -->` marks commands that CI runs word for word. Every repository link resolves | `check_dod.py --source <diplom>` compares each excerpt line with the named file; CI checks markers, links, and that each `run` command is in the workflow |
| 3 | **Structure and clarity** | Valid Markdown, no spelling errors, no filler words from the list in `check_dod.py`. An ADR follows the template and its context is 2 or 3 sentences | `markdownlint-cli2`, `codespell`, `check_dod.py` |
| 4 | **Review and pipeline** | Merged into `main` through a pull request whose DoD checklist is ticked by the reviewer, with a green CI run | Pull request history |

## Out of scope

A `doc-task` does not need diagrams, translations, or a published website. Add them only when a story asks for them.

## Run the checks locally

These are the commands CI runs:

<!-- verify: run -->
```bash
pip install codespell==2.4.3
python scripts/check_dod.py
npx --yes markdownlint-cli2@0.24.0 "**/*.md"
codespell
```

CI cannot compare code excerpts, because the LearnLab AI source is not public. The author also runs
`python scripts/check_dod.py --source ../diplom` and pastes its output into the pull request.
