# ADR-001: Answer with a demo tutor when no Anthropic API key is set

* **Status:** Accepted | **Date:** 2026-10-21 | **Author:** T. Sodnomdamba (Developer)

**Audience:** developers who change the AI grading code of LearnLab AI.
**Purpose:** record why the problem page works without an API key and the HTTP API does not, so neither is "fixed" by mistake.

## Context & Problem Statement

LearnLab AI grades answers with Claude through the Anthropic API, which needs a paid `ANTHROPIC_API_KEY`. Students,
teachers, and new developers run the app on their own computers without a key, and then every submission would fail.
We had to decide what the app does when the key is missing.

## Decision Outcome

Chosen option: **demo tutor on the problem page, real AI only on the HTTP API**, because the page must work for anyone
who runs the project, while an API client must never mistake a sample reply for a real grade.

The server action `askTutor` sends graded answers to the AI only when the key is set:

<!-- verify: app/problems/[id]/actions.ts -->
```ts
  if (process.env.ANTHROPIC_API_KEY) {
    switch (req.kind) {
      case "code-review":
// ...
  await new Promise((r) => setTimeout(r, 900));
  return mockTutorResponse(problem, req);
```

Every demo reply ends with a note that tells the student it is a sample:

<!-- verify: lib/tutor.ts -->
```ts
const DEMO_NOTE = "\n\n---\n_Демо горим: AI хараахан холбогдоогүй тул жишээ хариу харуулж байна._";
```

`POST /api/evaluate` has no fallback. Without a key it answers `500` with "AI үнэлгээ хийхэд алдаа гарлаа."

## Consequences

* **Positive:** the app runs end to end with no paid account, and the demo replies are fixed, so a tutorial can
  promise an exact result (78/100). API clients get an error instead of a fake score.
* **Trade-offs:** the two entry points behave differently without a key, which surprises new developers. Chat replies
  and hints use the demo tutor even when a key is set. The 900 ms delay only imitates the AI, so it says nothing about
  real response times.
