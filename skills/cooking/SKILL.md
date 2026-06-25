---
name: cooking
description: Orchestrate a full Azure DevOps task from work item link to PR. Run in the main session. Requires a task or story link; dispatches worker subagents (task-smith, rails-ninja) and composes skills (azure-task, planning, code-review-excellence, push-pr) in a verify-gated loop. Tracks work item state and completed time. Use when you want one command to drive link → spec → plan → build → test → review → PR.
---

# Cooking — Task Orchestrator

You are the head chef. You do **not** write the feature yourself.
You hold the spec + plan + state, delegate each step, and gate on real results.

Run this in the **main session** only — it needs the `Agent` tool to dispatch
worker subagents and `Bash` to run the gate and the Azure CLI.

## Core rules

- **A work item link is required.** No task or story URL → stop and ask. Don't run
  without one. This workflow is Azure-centric by design.
- **You are the single source of truth for intent.** Subagents lose their *context*
  after they return, but they share the *filesystem*. Re-pass only what lives in
  context — the spec and the exact failure. Files on disk (the plan file in
  `.agent/plans/`, the code) the worker reads itself; don't re-send them.
- **Gate on evidence, not vibes.** "Done" means tests pass with real output —
  never a subagent's say-so.
- **Cap every fix loop at 3 tries.** If still red, stop and report. Do not thrash.
- **You delegate commits and the push — you don't do them by hand.** The worker
  commits each green task itself (via `ship-it` → `commit` skill); `push-pr` runs
  the final `git push` and opens the PR. Your *direct* jobs are only: gate on
  tests, and update the work item (state + time).
- **Never push on red.** Confidence = green tests + clean review.
- **Only move the work item forward.** Read the current state before changing it;
  never push it backward (e.g. don't drag a Closed item back to Active).

> **State names are process-dependent.** This skill uses `Active` and
> `Pull Request`. Confirm the exact strings on your board — different processes
> differ. Change them here if yours don't match.

## The flow

### 0. Intake — require & load the work item (skill: `azure-task`)
- No task/story link → **STOP, ask for one.** Do not proceed.
- Parse the ID from the URL (`.../_workitems/edit/<id>`).
- Load the **full** item once and keep it — you reuse the type, title, description,
  and state across later steps:
  ```bash
  az boards work-item show --id <ID> --expand all -o json
  ```
  Branch on `System.WorkItemType`:
  - **Task** → its description **is** your spec. Skip step 1.
  - **User Story** (or Feature/Epic) → use the story text; sharpen it in step 1.

### 1. Sharpen the story → `task-smith` (subagent) — story only
Only when the link was a story:
1. Pass the story text to `task-smith` → a structured spec (Context, Goal,
   Acceptance Criteria, Technical Notes, Out of Scope). `task-smith` has no
   `Bash`, so **you** fetch the story text and hand it over.
2. Create a **Task under the story** with `azure-task` and capture its ID:
   ```bash
   TASK_ID=$(az boards work-item create --title "<short title>" --type Task --query id -o tsv)
   az boards work-item relation add --id $TASK_ID --relation-type parent --target-id <STORY_ID>
   ```
   From here, **this Task ID is the work item** you track for state + time.

### 2. Plan → `planning` (skill, in your context)
Run `planning` yourself. It writes a plan file under `.agent/plans/`
(e.g. `.agent/plans/2026-06-25-1430-favorite-articles.md`) — an atomic checklist.

**Create the feature branch now** (named from the task) if you're on
`main`/`master`. Doing it here means the stamp below is correct and the worker's
`commit` skill won't stop to ask for a branch mid-loop.

Then **stamp tracking metadata** into that plan file — this records the start of
work:
```markdown
## Tracking
- Work item: <ID> (<type>)
- Branch: <current branch>
- Started: <date +%Y-%m-%dT%H:%M:%S%z>  (epoch <date +%s>)
```
Keep the start epoch — you'll use it for completed time at PR. Review the plan and
fix obvious gaps before building.

### 3. Start work → state `Active` (skill: `azure-task`)
Move the work item to `Active` (only if it isn't already past it):
```bash
az boards work-item update --id <ID> --state "Active"
```

### 4. Build + test loop (max 3 rounds)
For each round:
1. **Dispatch the dev worker.**
   - For Rails: dispatch `rails-ninja`. It loads the `rails-way` and `ship-it`
     skills itself and builds test-first — you don't tell it how.
   - For a stack with no expert agent: implement in the main session using the
     `ship-it` skill directly.
   Pass only what lives in context: the spec, the plan file path + which task, and — if
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

### 5. Review → `code-review-excellence` (skill)
Run `code-review-excellence` on the diff. Send any real findings back to the dev worker —
re-run the build + test loop (step 4, still capped at 3). Re-gate after fixes.

### 6. Ship → `push-pr` (skill), then close out the work item
Only when green + reviewed.
1. Run `push-pr` to write the description and open the PR. Pass it the work item
   ID so the opener links it (Azure: `azure-pr --work-items <ID>`).
2. Update the work item with `azure-task` — **state + completed time only**:
   - **State → `Pull Request`.**
   - **Add completed time.** Wall-clock from the start stamp, *added* to any
     existing `CompletedWork` (re-read it fresh — Azure does not auto-sum):
     ```bash
     NOW=$(date +%s)
     ADD=$(echo "scale=2; ($NOW - <start_epoch>) / 3600" | bc)
     CUR=$(az boards work-item show --id <ID> \
       --query 'fields."Microsoft.VSTS.Scheduling.CompletedWork"' -o tsv); CUR=${CUR:-0}
     NEW=$(echo "$CUR + $ADD" | bc)
     az boards work-item update --id <ID> \
       --state "Pull Request" \
       --fields "Microsoft.VSTS.Scheduling.CompletedWork=$NEW"
     ```

## The shape

```
work item link (required)
  │ azure-task                 → load item, read type
  ▼   task? spec = description   story? ▼
  │ task-smith (subagent)      → spec  →  azure-task: create Task under story
  ▼
  │ planning (skill)           → plan file  + stamp start time   [your context]
  ▼
  │ azure-task                 → state: Active
  ▼
  ├── LOOP ≤3 ───────────────────────────────────────────┐
  │   rails-ninja (subagent)   → loads rails-way + ship-it │
  │   Bash (you)               → test + lint = GATE        │
  │   red? feed failure back ──────────────────────────────┘
  ▼  exhausted? STOP + report (leave Active)
  │ code-review-excellence      → findings → back to loop
  ▼
  │ push-pr (skill)            → PR  (links work item)
  ▼  green only
  │ azure-task                 → state: Pull Request, CompletedWork += elapsed
```

## What stays separate (and reusable)

| Piece          | Kind     | Reuse alone in main session?        |
|----------------|----------|-------------------------------------|
| `task-smith`   | subagent | Yes — "write a task for X"          |
| `rails-ninja`  | subagent | Yes — dispatch for any Rails work   |
| `rails-way`    | skill    | Yes — Rails patterns, in any session|
| `planning`     | skill    | Yes — "plan this"                   |
| `ship-it`      | skill    | Yes — implement a task yourself     |
| `code-review-excellence` | skill | Yes — review any diff          |
| `azure-task`   | skill    | Yes — read/update any work item     |
| `push-pr`      | skill    | Yes — open a PR (any host)          |

The `cooking` skill composes them — it owns none of them. Edit any piece without touching
the rest; use any piece without `cooking`.
