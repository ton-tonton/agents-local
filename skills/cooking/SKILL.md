---
name: cooking
description: Orchestrate a full task from rough request to PR. Run in the main session. Dispatches worker subagents (task-smith, rails-ninja) and composes skills (planning, code-review, push-pr) in a verify-gated loop; the dev worker loads rails-way + ship-it itself. Use when you want one command to drive spec → plan → build → test → review → PR.
---

# Cooking — Task Orchestrator

You are the head chef. You do **not** write the feature yourself.
You hold the spec + plan + state, delegate each step, and gate on real results.

Run this in the **main session** only — it needs the `Agent` tool to dispatch
worker subagents. Subagents cannot reliably do this.

## Core rules

- **You are the single source of truth for intent.** Subagents lose their *context*
  after they return, but they share the *filesystem*. Re-pass only what lives in
  context — the spec and the exact failure. Files on disk (`plan.md`, the code) the
  worker reads itself; don't re-send them.
- **Gate on evidence, not vibes.** "Done" means tests pass with real output —
  never a subagent's say-so.
- **Cap every fix loop at 3 tries.** If still red, stop and report. Do not thrash.
- **You don't commit; you don't push.** The worker commits each green task itself
  (via `ship-it`, which uses the `commit` skill). You only gate. `push-pr` does the
  final push at the end.
- **Match cost to size.** For a one-file change, skip this — just run `ship-it`
  directly. Use the full orchestra only for real features.
- **Never push on red.** Confidence = green tests + clean review.

## The flow

### 1. Sharpen the request → `task-smith` (subagent)
If the request is vague, dispatch `task-smith` to produce a structured spec
(Context, Goal, Acceptance Criteria, Technical Notes, Out of Scope).
Hold the returned spec. Skip this only if the request is already a clear spec.

### 2. Plan → `planning` (skill, in your context)
Run the `planning` skill yourself. It writes `plan.md` — an atomic checklist.
The plan must live in *your* context so you can drive and check each step.
Review it; fix obvious gaps before building.

### 3. Build + test loop (max 3 rounds)
For each round:
1. **Dispatch the dev worker.**
   - For Rails: dispatch `rails-ninja`. It loads the `rails-way` and `ship-it`
     skills itself and builds test-first — you don't tell it how.
   - For a stack with no expert agent: implement in the main session using the
     `ship-it` skill directly.
   Pass only what lives in context: the spec, the `plan.md` task, and — if
   retrying — the exact failure. The worker reads the current code from disk.
2. **Run the gate yourself** via `Bash` — directly, no subagent. Use the project's
   real test + lint commands (the same ones `ship-it` step 0 detects — e.g.
   `bundle exec rspec` + `bundle exec rubocop` for Rails). Capture the real output.
3. **Decide:**
   - Green → exit the loop.
   - Red → feed the failure back into round N+1.
   - 3 rounds exhausted → **stop, report the blocker, do not push.**

> Why run the gate yourself instead of a "tester" subagent: running commands is
> deterministic. Keeping it in your context gives you the real output with zero
> loss and one less round trip. Delegate *fixing*, not *checking*.

### 4. Review → `code-review` (skill)
Run `code-review` on the diff. Send any real findings back to the dev worker —
re-run the build + test loop (step 3, still capped at 3). Re-gate after fixes.

### 5. Ship → `push-pr` (skill)
Only when green + reviewed. Run `push-pr` to write the description and open the PR.

## The shape

```
request
  │ task-smith (subagent)      → spec        [own context]
  ▼
  │ planning (skill)           → plan.md     [your context]
  ▼
  ├── LOOP ≤3 ───────────────────────────────────────────┐
  │   rails-ninja (subagent)   → loads rails-way + ship-it │
  │   Bash (you)               → test + lint = GATE        │
  │   red? feed failure back ──────────────────────────────┘
  ▼  exhausted? STOP + report
  │ code-review (skill)        → findings → back to loop
  ▼
  │ push-pr (skill)            → PR
  ▼  green only
```

## What stays separate (and reusable)

| Piece          | Kind     | Reuse alone in main session?        |
|----------------|----------|-------------------------------------|
| `task-smith`   | subagent | Yes — "write a task for X"          |
| `rails-ninja`  | subagent | Yes — dispatch for any Rails work   |
| `rails-way`    | skill    | Yes — Rails patterns, in any session|
| `planning`     | skill    | Yes — "plan this"                   |
| `ship-it`      | skill    | Yes — implement a task yourself     |
| `code-review`  | skill    | Yes — review any diff               |
| `push-pr`      | skill    | Yes — open a PR                     |

The `cooking` skill composes them — it owns none of them. Edit any piece without touching
the rest; use any piece without `cooking`.
