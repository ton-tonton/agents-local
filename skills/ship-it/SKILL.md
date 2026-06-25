---
name: ship-it
description: Stack-agnostic implementation workflow. Drives a single task through a test-first loop — write a failing test, implement to green, refactor, gate on tests + lint, commit, update the plan. Use when implementing tasks in any project (Rails, Node, Python, Go, etc.).
---

# Ship It — Implementation Workflow

Implement one task at a time with a fast, test-first loop:
write the test → make it pass → refactor → gate → commit → repeat.

Stack-agnostic. Detect this project's commands first (below); the loop is the same
everywhere.

## 0. Detect project commands (do this first)

Don't assume the toolchain. Find the real test and lint commands:

- **Ruby/Rails** → `bundle exec rspec`, `bundle exec rubocop`
- **Node** → check `package.json` scripts (`npm test`, `npm run lint`)
- **Python** → `pytest`, `ruff`/`flake8` (check `pyproject.toml` / `Makefile`)
- **Go** → `go test ./...`, `go vet`
- **Anything** → check `Makefile`, CI config, or `AGENTS.md` for the canonical commands

Use what the project actually uses. The examples below show Ruby; substitute yours.

## Instructions

- Clarify goals, constraints, and required inputs.
- If unsure about syntax or APIs, look it up (e.g. the `context7` MCP server).
- Follow this cycle for each task in `plan.md`.

### 1. Select task

1. Pick the next pending `[ ]` task from `plan.md`.
2. Mark it in-progress `[~]`.

### 2. Fast development cycle

**Test first — define behavior.**
Write the test before the implementation. Scope it to the code *this task* adds —
not whole-app coverage.

- Cover the happy path, the error/validation path, and meaningful edge cases.
- Run the test — it should **fail (red)**, proving it exercises new behavior.

```ruby
# Example (Ruby/RSpec) — substitute your stack's test framework
describe User do
  it "rejects an invalid email" do
    user = User.new(email: "bad-format")
    expect(user).not_to be_valid
    expect(user.errors[:email]).to include("is invalid")
  end
end
```

> **Exception — prototype then lock.** When test-first is awkward (migrations,
> generators, spikes, config), build the prototype first, then write tests that
> pin the resulting behavior **before** the commit. The green-commit gate still holds.

**Implement.** Write the minimum code to make the test pass. No premature
optimization. Run the test — it should now **pass (green)**.

**Refactor.** Improve naming, remove duplication, simplify. Run the test — still green.

### 3. Gate & finalize

**Gate** — run the project's real commands:
- Full test suite (e.g. `bundle exec rspec`)
- Linter (e.g. `bundle exec rubocop`)

**Commit & update** — only after the suite is green:
1. Create the commit with the `commit` skill — it owns the message format, branch
   safety, and the Co-Authored-By trailer. One focused commit per task, including
   both the tests and the implementation. Don't write the commit by hand.
2. Mark the task `[x]` in `plan.md` and append the short commit SHA.
   ```markdown
   - [x] **Task 2.1**: Implement user validation `abc1234`
   ```

### 4. Iterate

Return to step 1 for the next task.

## Quality gates

- **Tests pass**: the full suite is green.
- **Style**: no linter offenses.
- **Security**: no hardcoded secrets — use env vars or a secrets manager.

## Error recovery

**Tests fail after refactoring:** find which test broke, check the recent change,
revert to the last green state, re-approach.

**Can't reach green after ~2–3 tries:** stop thrashing.
1. Revert to the last green state.
2. Reassess — the task may be mis-scoped or a plan assumption may be wrong.
3. Surface the blocker (or ask) before looping on the same fix.

## Working with existing tests

- **Extend, don't replace.** Keep existing tests passing; add new ones for new behavior.
- Update existing tests only when requirements actually change.
- When refactoring changes structure: run existing tests (green) → add new tests →
  migrate cases → remove old tests only after the new ones pass.
