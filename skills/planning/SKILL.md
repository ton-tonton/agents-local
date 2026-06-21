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
- **Tasks**: A list of atomic, ordered tasks (Verb-first) — as many as the work needs, no padding or cramming.
- **Validation**: At least one item for testing.

Create file `plan.md` with the plan.

## Plan Template

```markdown
# Plan <name>

## Approach

<High-level approach>

## Tasks

- [ ] **Task 1.1**: <Discovery / context gathering>
- [ ] **Task 2.1**: <Implementation step>
- [ ] **Task 2.2**: <Implementation step>
- [ ] **Task 2.3**: <Implementation step>
- [ ] **Task 2.4**: <Implementation step>
- [ ] **Task 3.1**: <Validation / testing>

<!-- List as many atomic, ordered tasks as the work needs. Group with N.N IDs so do-it can mark [x] + commit SHA. -->

## Notes

<Any important considerations>

## Open Questions

- <Question 1 (max 2)>
```

## Checklist Guidelines

- **Atomic**: Each step should be a single logical unit of work.
- **Ordered**: Sequence by dependency and risk — prerequisites first, riskiest unknowns early, validation last.
- **Verb-first**: "Add...", "Refactor...", "Verify...".
- **Concrete**: Name specific files or modules when possible.
