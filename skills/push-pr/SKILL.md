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

## Do not use this skill when

- You need comprehensive PR documentation with test plans and risk analysis (use comprehensive-review-pr-enhance instead)
- There is no PR or change list to summarize

## Context
Create focused PR descriptions that clearly communicate what changed and why, keeping descriptions under 4000 characters.

## Requirements
$ARGUMENTS

## Instructions

1. **Check for PR template**: If the project has `.azuredevops/pull_request_template.md`, read this template first and use its structure/sections to format the output
2. Run `git diff [base]...HEAD` to see changes
3. Run `git log [base]...HEAD` to review commits
4. Categorize changes by type (source, test, config, docs)
5. Extract main purpose from commits and code
6. Generate description combining the template structure (if exists) with the analyzed changes
7. Use /azure-open-pr skill with generated description

## Output Format

```markdown
## Summary

[2-3 sentence executive summary of what this PR accomplishes]

**Impact**: X files changed (Y additions, Z deletions)
**Type**: [Feature/Bug Fix/Refactor/etc.]

## What Changed

### Source Code
- Changed/Added/Refactored specific components
- List key modifications with file references

### Tests
- Added/Updated tests for new behavior

### Documentation
- Updated docs, README, or comments

### Configuration
- Modified config, dependencies, or settings
```

## Guidelines

- **Check for existing template**: Always look for `.azuredevops/pull_request_template.md` first and adapt to its format if present
- Be concise and specific
- Use concrete examples and file names
- Explain "why" not just "what"
- Categorize related changes together
- Highlight scope and impact clearly
- Stay focused and scannable

## Example

### Generated Description:
```markdown
## Summary

Adds JWT-based authentication middleware to protect API endpoints, replacing session-based auth for better scalability.

**Impact**: 8 files changed (245 additions, 67 deletions)
**Type**: Feature / Security Enhancement

## What Changed

### Source Code
- Added `AuthMiddleware.ts` with JWT validation
- Updated `routes/api.ts` to use auth middleware
- Refactored `UserController.ts` for JWT token generation
- Removed legacy `SessionManager.ts` code

### Tests
- Added auth middleware tests and integration tests
- Added token refresh flow tests

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

**Impact**: 8 files changed (245 additions, 67 deletions)
**Type**: Feature / Security Enhancement

## What Changed

### Source Code
- Added AuthMiddleware.ts with JWT validation
- Updated routes/api.ts to use auth middleware
- Refactored UserController.ts for JWT token generation
- Removed legacy SessionManager.ts code

### Tests
- Added auth middleware tests and integration tests
- Added token refresh flow tests

### Documentation
- Updated API docs with auth requirements
- Added authentication setup guide
EOF
)" \
  --target-branch main \
  --auto-complete true \
  --delete-source-branch true \
  --open
```
