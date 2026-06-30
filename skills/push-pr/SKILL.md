---
name: push-pr
description: "Generate a concise PR description and open the pull request. Analyzes the diff and commits, formats a clear description, detects the git host, and delegates opening to the host's PR skill."
allowed-tools: Read, Bash, Skill
---

# Generate and Open PR

Write a clear, concise PR description, then open the pull request with the **host's** PR skill.
This skill is host-agnostic: it decides *what to say*; the host skill decides *how to send it*.

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
2. **Pick the base branch.** Use what the user specified. If they didn't, detect the repo's default branch and confirm it:
   ```bash
   git remote show origin | sed -n 's/.*HEAD branch: //p'
   ```
   Don't assume `main` vs `develop` — different repos differ.
3. **Push the current branch**: `git push` so the remote branch is up to date.
4. **Check for a PR template** (host-dependent location, e.g. `.azuredevops/pull_request_template.md`). If present, read it and follow its sections instead of the default format below.
5. **Review the changes** — exclude dependency lock files; they're noise:
   ```bash
   git diff <base>...HEAD -- . ':(exclude)*.lock' ':(exclude)package-lock.json' ':(exclude)pnpm-lock.yaml'
   git log  <base>...HEAD
   ```
6. **Generate the description** — list only the important changes. Skip whitespace, formatting, and trivial refactors. Keep it under ~2000 characters.
7. **Open the PR** by invoking the host skill from step 1 with the title, description, and base branch (e.g. the `azure-pr` skill for Azure Repos). If you were given a work item / issue ID, pass it so the opener links it (Azure: `--work-items <ID>`).

## Output Format

```markdown
## Summary
[1-3 short sentences — what this PR does and what stays out of scope. One idea per sentence.]

## What Changed
- **[Theme]**
  - [<verb> <what> — one fact, no trailing clause]
  - [<verb> <what> — one fact, no trailing clause]
- **[Theme]**
  - [<verb> <what> — one fact, no trailing clause]
```

## Do not include

Never add these sections — CI reports them, not the PR:
**Tests, Verification, Test Plan, How to test, Checklist.**

## Guidelines

- **Check for a template first** and adapt to its format if present.
- **Group by theme**, not by file type. Use buckets like the area of the app or kind of work (e.g. "Auth", "Routes").
- **One change per bullet**, as a short fragment. No "and ... and" chains.
- **Terse bullets.** Write each as `<verb> <what>` — one fact. Drop trailing how/why clauses.
- **Keep sentences short** — aim ≤ 15 words. Write for fast scanning.
- **No process framing.** Reviewers read the final diff, not your history. Drop "round 1", "latest round", "after feedback", etc.
- **Keep facts, cut prose.** Cut the explanation around them, not the fact itself.
- **Ignore lock files.** Never mention dependency lock files (`Gemfile.lock`, `yarn.lock`, `package-lock.json`, `pnpm-lock.yaml`, etc.). They're auto-generated noise.
- **Focus on what changed**, not rationale. Add a one-line "why" only when the change is surprising.

## Example

### Generated description
```markdown
## Summary
Adds JWT auth middleware to protect API endpoints. Replaces session-based auth for better scaling.

## What Changed
- **Auth**
  - Add `AuthMiddleware` for JWT validation
  - Issue JWT tokens from `UserController`
  - Remove legacy `SessionManager`
- **Routes**
  - Apply auth middleware to API routes
- **Docs**
  - Document auth requirements
<!-- no Tests/Verification section — CI covers it -->
```

Then hand the title + this description + base branch to the host's PR skill (`azure-pr` for Azure Repos), which runs the actual create command.
