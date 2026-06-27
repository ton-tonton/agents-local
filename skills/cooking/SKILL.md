---
name: cooking
description: Orchestrate a coding task from intent to PR. Run in the main session. Takes a plain request or an optional Azure work item link; dispatches the eren and levi subagents and composes skills (planning, push-pr, and azure-task when a link is given) in a verify-gated loop. Tracks work item state and completed time when the link is a Task. Use when you want one command to drive intent → plan → build → test → review → PR.
---

# Cooking — Task Orchestrator

**You are the head chef.** You hold the goal, the plan, and the state. You delegate
every build and review step, and you gate on real results. You never write the
feature code yourself.

## How to run

- **Main session only.** You need the `Agent` tool to dispatch subagents and `Bash`
  to run the gate (and the Azure CLI when a work item link is given).
- **`bc` is needed only for Azure time tracking.** If you pass an Azure Task link
  and `bc` is missing, install it (`brew install bc` / `apt-get install bc`). The
  no-link path doesn't use it.

## At a glance

| # | Step   | Who acts                    | Output                          |
|---|--------|-----------------------------|---------------------------------|
| 0 | Intake | you (+ `azure-task` if link)| the goal                        |
| 1 | Plan   | you (+ `planning`)          | plan file, branch, start time   |
| 2 | Build  | `eren` builds, **you** gate | green, tested code (loop ≤3)    |
| 3 | Review | `levi` reviews, **you** decide | a verdict                    |
| 4 | Ship   | `push-pr`, then you close out | PR + work-item tracking       |

Loop-backs: step 2 retries on red (≤3); step 3 sends fixes back to step 2 (fresh ≤3).

## Core rules

- **Start from the goal.** A plain request is enough. An Azure work item link is
  optional — it's just where the goal comes from, and (if it's a Task) what you
  track at PR.
- **You own the intent.** Subagents lose their *context* on return but share the
  *filesystem*. Re-pass only what lives in context: the goal and the exact failure.
  Files on disk (the plan in `.agent/plans/`, the code) the worker reads itself.
- **Never edit code yourself.** Delegate *all* code changes to the worker — first
  build and review fixes alike. You hold intent and gate; you never touch the code.
- **Delegate commits and the push too.** The worker commits each green task itself
  (`ship-it` → `commit`); `push-pr` runs the final `git push` and opens the PR.
- **Gate on evidence, not vibes.** "Done" means tests pass with real output — never
  a subagent's say-so. **Never push on red.** Confidence = green tests + clean review.
- **Cap each fix loop at 3 tries.** If still red, stop and report. Do not thrash.

> **State names are process-dependent.** When tracking a Task, this skill uses
> `Pull Requested`. Confirm the exact string on your board and change it here if it
> differs.

---

## 0 — Intake: understand the goal

Get the goal from whichever source applies:

- **No link (default).** The user's request **is** the goal. Nothing to track —
  skip the work-item update at PR.
- **Azure work item link (optional).** Load it once with `azure-task` and keep it:
  ```bash
  az boards work-item show --id <ID> --expand all -o json   # ID from .../_workitems/edit/<id>
  ```
  Then branch on `System.WorkItemType`:
  - **Task** → its description is the goal; track this Task for state + time.
  - **Story / Feature / Epic** → its text is the goal; nothing is tracked.

Clarify only if a gap would change the plan — ask 1–2 questions, no more. Then go
to planning. No code, no spec ceremony.

## 1 — Plan (`planning`)

**Turn the goal into an atomic checklist.** Run `planning` yourself, feeding it the
goal from step 0. It writes a plan file under `.agent/plans/`
(e.g. `.agent/plans/2026-06-25-1430-favorite-articles.md`).

Then, before building:

1. **Create the feature branch** (named from the goal) if you're on `main`/`master`.
   Doing it now keeps the stamp below correct and stops the worker's `commit` skill
   from pausing to ask for a branch mid-loop.
2. **Stamp tracking metadata** into the plan file. Read the start epoch from the
   `SessionStart` hook file — so any clarification you did *before* triggering
   cooking is counted (fallback to now if the file is missing):
   ```bash
   START=$(cat "$CLAUDE_PROJECT_DIR/.claude/cooking-session-start" 2>/dev/null || date +%s)
   ```
   ```markdown
   ## Tracking
   - Work item: <ID> (<type>)   # omit this line when there's no link
   - Branch: <current branch>
   - Started: <format %Y-%m-%dT%H:%M:%S%z of START>  (epoch <START>)
   ```
3. **Review the plan** and fix obvious gaps.

## 2 — Build + test loop (≤3 rounds)

Each round:

1. **Dispatch the dev worker.**
   - **Rails** → dispatch `eren`. It loads `rails-way` + `ship-it` itself and builds
     test-first — you don't tell it how.
   - **Other stacks** → dispatch a worker that uses the `ship-it` skill.

   Pass only what lives in context: the goal, the plan file path + which task, and —
   if retrying — the exact failure. The worker reads the code from disk.
2. **Run the gate yourself** via `Bash` — no subagent. Use the project's real test +
   lint commands (the ones `ship-it` step 0 detects, e.g. `bundle exec rspec` +
   `bundle exec rubocop` for Rails). Capture the real output.
3. **Decide:**
   - **Green** → exit the loop.
   - **Red** → feed the failure into the next round.
   - **3 rounds spent** → stop, report the blocker, do not push.

> **Why you gate, not a subagent:** running commands is deterministic. Keeping it in
> your context gives you the real output with zero loss and one less round trip.
> Delegate *fixing*, not *checking*.

## 3 — Review (`levi`)

**Dispatch the `levi` subagent.** It loads `code-review-excellence`, runs the diff
itself, reviews read-only, and returns findings with a verdict (`clean` /
`changes-requested`). It never edits code or re-runs lint/tests — it only reports.

Pass it:
- the **goal**,
- the **plan file path** (so it checks goal fit against the tasks + validation items),
- the **base branch** to diff against.

`levi` runs `git diff` itself — keep the full diff out of your context. Then **you
decide** on what it returns:

- **No real findings** → proceed to ship.
- **Real findings** → send the fixes back to the dev worker (re-enter step 2 with a
  **fresh cap of 3** — review fixes are new work, not the build's spent tries), then
  **re-gate**. Never push on red.

## 4 — Ship (`push-pr`) + close out

Only when green **and** reviewed.

1. **Open the PR.** Run `push-pr` to write the description and open it. If you have
   a work item ID, pass it so the opener links it — for Azure Repos, `push-pr` hands
   off to `azure-pr`, which runs `az repos pr create --work-items <ID>`. If a PR
   already exists for the branch, **update it — don't open a second one.**
2. **Log elapsed time in chat** — always, e.g. "Time spent in cooking: 2h 14m".
   Compute it from the `START` epoch in plan file.
3. **Update the work item — only if tracking a Task** (skip otherwise). Set state +
   completed time only:
   - **State** → `Pull Requested`.
   - **Completed time** → wall-clock since the start stamp, *added* to any existing
     `CompletedWork` (re-read it fresh — Azure does not auto-sum):
     ```bash
     NOW=$(date +%s)
     ADD=$(echo "scale=2; ($NOW - <start_epoch>) / 3600" | bc)
     CUR=$(az boards work-item show --id <ID> \
       --query 'fields."Microsoft.VSTS.Scheduling.CompletedWork"' -o tsv); CUR=${CUR:-0}
     NEW=$(echo "$CUR + $ADD" | bc)
     az boards work-item update --id <ID> \
       --state "Pull Requested" \
       --fields "Microsoft.VSTS.Scheduling.CompletedWork=$NEW"
     ```

---

## What stays separate (and reusable)

`cooking` composes these — it owns none of them. Edit any piece without touching the
rest; use any piece without `cooking`.

| Piece                    | Kind     | Reuse alone in main session?          |
|--------------------------|----------|---------------------------------------|
| `eren`                   | subagent | Yes — dispatch for any Rails work     |
| `levi`                   | subagent | Yes — review any diff, get a verdict  |
| `rails-way`              | skill    | Yes — Rails patterns, in any session  |
| `planning`               | skill    | Yes — "plan this"                     |
| `ship-it`                | skill    | Yes — implement a task yourself       |
| `code-review-excellence` | skill    | Yes — review any diff (what `levi` loads) |
| `azure-task`             | skill    | Yes — read/update any work item       |
| `push-pr`                | skill    | Yes — open a PR (any host)            |
