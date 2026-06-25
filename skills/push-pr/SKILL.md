---
name: push-pr
description: "Generate a concise PR description and open the pull request. Analyzes the diff and commits, formats a clear description, detects the git host, and delegates opening to the host's PR skill."
allowed-tools: Read, Bash, Skill
---

# Generate and Open PR

Write a clear, concise PR description, then open the pull request with the
**host's** PR skill. This skill is host-agnostic: it decides *what to say*; the
host skill decides *how to send it*.

## Use this skill when

- You want to analyze changes and open a PR in one step
- You need a concise PR description generated from the diff

## Instructions

1. **Detect the host** from the remote:
   ```bash
   git remote get-url origin
   ```
   - `dev.azure.com` / `visualstudio.com` → use the **`azure-pr`** skill to open.
   - Any other host → stop and tell the user no opener is wired for that host yet.
2. **Pick the base branch.** Use what the user specified. If they didn't, detect
   the repo's default branch and confirm it:
   ```bash
   git remote show origin | sed -n 's/.*HEAD branch: //p'
   ```
   Don't assume `main` vs `develop` — different repos differ.
3. **Push the current branch**: `git push` so the remote branch is up to date.
4. **Check for a PR template** (host-dependent location, e.g.
   `.azuredevops/pull_request_template.md`). If present, read it and follow its
   sections instead of the default format below.
5. **Review the changes**:
   ```bash
   git diff <base>...HEAD
   git log  <base>...HEAD
   ```
6. **Generate the description** — list only the important changes. Skip whitespace,
   formatting, and trivial refactors. Keep it under ~2000 characters.
7. **Open the PR** by invoking the host skill from step 1 with the title,
   description, and base branch (e.g. the `azure-pr` skill for Azure Repos).
   If you were given a work item / issue ID, pass it so the opener links it
   (Azure: `--work-items <ID>`).

## Output Format

```markdown
## Summary

[1-2 sentence executive summary of what this PR accomplishes]

## What Changed

### Source Code
- Changed/Added/Refactored specific components
- List key modifications with file references

### Documentation
- Updated docs, README, or comments

### Configuration
- Modified config, dependencies, or settings
```

## Guidelines

- **Check for a template first** and adapt to its format if present.
- **Focus on what changed**: list functional changes, not rationale.
- **Be brief**: only important changes; skip trivial updates.
- **Use file references**: name specific files/functions that changed.
- **Group related changes** and keep bullets scannable.

## Example

### Generated description
```markdown
## Summary

Adds JWT-based authentication middleware to protect API endpoints, replacing
session-based auth for better scalability.

## What Changed

### Source Code
- Added `AuthMiddleware.ts` with JWT validation
- Updated `routes/api.ts` to use auth middleware
- Refactored `UserController.ts` for JWT token generation
- Removed legacy `SessionManager.ts` code

### Documentation
- Updated API docs with auth requirements
```

Then hand the title + this description + base branch to the host's PR skill
(`azure-pr` for Azure Repos), which runs the actual create command.
