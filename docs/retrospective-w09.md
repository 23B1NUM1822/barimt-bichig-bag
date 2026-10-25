# Retrospective: Week 09 mini-sprint

**Audience:** the team and the ICSI438 instructor.
**Purpose:** what we learned this sprint, the one change for next week, and the answer to the documentation-waste question.

Sprint Goal: "Our project documentation is lean, audience-tailored, and 'done'." Result: met. Stories #1 to #4
(13 points) are closed, and the ADR passes every DoD check.

## Timeboxes

Sprint date: 2026-10-21. Times are from GitHub (UTC+8) and show when each item was published, not how long the
work took.
| Phase | Output | Evidence |
| --- | --- | --- |
| Kick-off and Sprint Goal | Roles and goal in the README, milestone "W09 Mini-Sprint" | Milestone created 19:16 |
| Sprint Planning | 4 `doc-task` stories with acceptance criteria and points 3, 5, 3, 2 | Issues #1 to #4, created 19:16 |
| Sprint Part 1: DoD and draft | DoD, `check_dod.py`, CI | PR #5, merged 19:19 |
| Sprint Part 2: finalization | ADR-001, reviewed against the DoD checklist | PR #6, merged 19:20 |
| Sprint Review | Live demo of ADR-001 | Feedback below |
| Retrospective | This note | Closes #4 |

## Sprint Review feedback

Filled in during the class Sprint Review.

| From | Feedback | Our response |
| --- | --- | --- |
| | | |

## Retro questions

**What went well?** Every DoD item has a check that a machine or a reviewer can run. A test with five planted
defects (missing audience line, a changed code line, a filler word, a fourth context sentence, a missing
Trade-offs field) failed on all five. The same test found a bug in the checker, which reported a mismatched excerpt
as verified; PR #5 fixed it before merge.

**What did not go well?** Peer review came late. The author ticked the review checklist himself when PR #6 was
merged, so at merge time DoD item 4 proved that the checklist was used, not that a second person had read the
document. The Scrum Master reviewed ADR-001 against the DoD after the sprint and left four comments on PR #6. From
Week 10 the review happens before the merge, not after. CI also cannot compare code excerpts,
because the LearnLab AI source is not public, so that check runs only on the author's computer. We did not log the start and end of each phase, so the timebox
table shows publishing times only.

**What will we change?** See the action item.

## Action item for Week 10

Delete the hand-written library reference `lab07/docs/reference/library.md` in
[barimt-bichig](https://github.com/23B1NUM1822/barimt-bichig) and leave a one-paragraph page that links to the
generated TypeDoc reference.

- **Owner:** T. Sodnomdamba
- **Due:** Week 10 lab session
- **Done when:** the page has at most 100 words, `mkdocs build --strict` passes, and no other page links to an anchor
  that was removed.

## Reflection: what could we have omitted?

> "Which documentation artifact or section could we have omitted completely without any stakeholder or developer
> missing it?"

**The hand-written "Library functions" reference** from Lab 07 (`lab07/docs/reference/library.md`, about 1,400 words).

Its only readers are developers, and they already have the TypeDoc reference from Lab 06. The page says so itself:
TypeDoc "has the same symbols with type details, source links, and longer examples that CI compiles against the real
code." So the page repeats a reference that is generated from the code, and nothing checks the copy. When a signature
changes, TypeDoc changes with it and the copy goes stale.

"Just Enough Documentation" asks for each document to have a reader who needs it, and for the same information not
to be kept in two places. The library page fails both: its reader is served better elsewhere, and it is a second copy
that someone has to maintain. Removing it loses nothing, and the action item above does that.

This sprint we applied the same rule up front. We wrote one artifact (the ADR) instead of an ADR and a README, because
the course only needs one and the repository README already says where everything is.
