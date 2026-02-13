---
name: push-pr
description: "Generate concise PR descriptions and create Azure Repos pull requests. Analyzes changes, formats description, and opens PR via Azure CLI."
allowed-tools: Read, Bash
---

# Generate and Open PR

Generate clear, concise PR descriptions and create the pull request in Azure Repos. Analyzes changes, formats description, and opens PR via Azure CLI.

## Use this skill when

- Creating and opening pull requests in Azure Repos
- Need to quickly analyze changes and create a PR
- Want automated PR creation with concise descriptions

## Context
Create focused PR descriptions that clearly communicate what changed and why, keeping descriptions under 2000 characters.

- **Base Branch**: Defaults to `develop` if not specified
- **PR Type**: Defaults to `--draft true` if not specified

## Instructions

- Use `develop` as [base] if not specified by user

1. **Push current branch**: Run `git push` to ensure the remote branch is up to date
2. **Check for PR template**: If the project has `.azuredevops/pull_request_template.md`, read this template first and use its structure/sections to format the output
3. Run `git diff [base]...HEAD` to see changes
4. Run `git log [base]...HEAD` to review commits
5. Analyze changes and identify **only the important/significant modifications**
6. Generate a concise description listing what changed, omitting minor changes (whitespace, formatting, trivial refactors)
7. Use /azure-open-pr skill with generated description

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

- **Check for existing template**: Always look for `.azuredevops/pull_request_template.md` first and adapt to its format if present
- **Focus on what changed**: List functional changes, not why or rationale
- **Be brief**: Include only important changes, skip trivial updates
- **Use file references**: Mention specific files/functions that changed
- **Skip obvious items**: Don't mention formatting, whitespace, minor refactors
- **Group related changes**: Combine similar modifications
- **Keep it scannable**: Short bullet points, easy to read quickly

## Example

### Generated Description:
```markdown
## Summary

Adds JWT-based authentication middleware to protect API endpoints, replacing session-based auth for better scalability.

## What Changed

### Source Code
- Added `AuthMiddleware.ts` with JWT validation
- Updated `routes/api.ts` to use auth middleware
- Refactored `UserController.ts` for JWT token generation
- Removed legacy `SessionManager.ts` code

### Documentation
- Updated API docs with auth requirements
- Added authentication setup guide
```

### PR Creation Command:
```bash
az repos pr create \
  --title "feat: Add JWT-based authentication middleware" \
  --description "$(cat <<'EOF'
## Summary

Adds JWT-based authentication middleware to protect API endpoints, replacing session-based auth for better scalability.

## What Changed

### Source Code
- Added AuthMiddleware.ts with JWT validation
- Updated routes/api.ts to use auth middleware
- Refactored UserController.ts for JWT token generation
- Removed legacy SessionManager.ts code

### Documentation
- Updated API docs with auth requirements
- Added authentication setup guide
EOF
)" \
  --target-branch develop \
  --delete-source-branch true \
  --draft true
```
