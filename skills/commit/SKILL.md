---
name: commit
description: Creates concise Conventional Commits. Use for any git commit.
---

# Commit

Create small, focused commits with a **concise** Conventional Commit message.

## 1. Branch safety (check first)

```bash
git branch --show-current
```

If on `main` or `master`, stop and ask the user before committing, unless they
already said to commit to the default branch.

## 2. Format

```
<type>(<scope>): <subject>

<optional short body>

<optional footer>
```

- **Subject**: imperative, capitalized, no period. Short and clear: a reviewer
  should grasp the change from the subject alone. Scope optional.
- **Default to header only.** Most commits need no body.
- **Add a body only when the "why" isn't obvious** — keep it to 1–3 short lines.
  Explain *why*, not *how*. Never restate the diff line by line.
- One logical change per commit; the repo stays working after each.

## 3. Types

| Type | Use for |
|------|---------|
| `feat` | Features |
| `fix` | Bug fixes |
| `docs` | Documentation |
| `style` | Styles (formatting, no logic change) |
| `refactor` | Code refactoring (no behavior change) |
| `perf` | Performance improvements |
| `test` | Tests |
| `build` | Builds / dependencies |
| `ci` | Continuous integration |
| `chore` | Chores / maintenance |
| `revert` | Reverts |

Use `!` after the type for a breaking change (e.g. `feat(api)!:`) and add a
`BREAKING CHANGE:` footer (see below).

## 4. Footer (optional)

Add a footer line only for these cases:

**Issue ref** — only when there is a known issue ID (from the user, or the task):
`Refs <ID>`, with the ID exactly as given (e.g. `Refs AB#1234`, `Refs #123`).

**Breaking change** — `BREAKING CHANGE: <what changed and how to migrate>`.

## Examples

**Header only — most commits:**
```
fix(api): Handle null user in dashboard endpoint
```

**Short why + issue ref — when it helps:**
```
feat(assets): Self-host Font Awesome 7 via npm

Replaces the CDN kit so assets are fingerprinted by Propshaft.

Refs AB#22117
```
