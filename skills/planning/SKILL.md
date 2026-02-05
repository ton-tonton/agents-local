---
name: planning
description: Use when a user asks for a plan for a coding task, to generate a clear, actionable, and atomic checklist.
---

# Concise Planning

## Goal

Turn a user request into a **single, actionable plan** with atomic steps.

## Workflow

### 1. Scan Context

- Read `AGENTS.md`, docs, and relevant code files.
- Identify constraints (language, frameworks, tests).

**Research & Documentation**
If unsure about syntax or need more information, search documentation using the MCP `context7` server.

**For FEATURE ADDITION:**
- Which files are affected?
- What dependencies needed?
- How to verify it works?

**For BUG FIX:**
- What's the root cause?
- What file/line to change?
- How to test the fix?

### 2. Minimal Interaction

- Ask **at most 1–2 questions** and only if truly blocking.
- Make reasonable assumptions for non-blocking unknowns.

### 3. Generate Plan

Use the following structure:

- **Approach**: 1-3 sentences on what and why.
- **Tasks**: A list of 6-10 atomic, ordered tasks (Verb-first).
- **Validation**: At least one item for testing.

## Plan Template

```markdown
# Plan <name>

## Approach

<High-level approach>

## Tasks

[ ] <Task 1: Discovery>
[ ] <Task 2: Implementation>
[ ] <Task 3: Implementation>
[ ] <Task 4: Validation/Testing>
[ ] <Task 5: Rollout/Commit>

## Notes

<Any important considerations>

## Open Questions

- <Question 1 (max 3)>
```

## Checklist Guidelines

- **Atomic**: Each step should be a single logical unit of work.
- **Verb-first**: "Add...", "Refactor...", "Verify...".
- **Concrete**: Name specific files or modules when possible.
