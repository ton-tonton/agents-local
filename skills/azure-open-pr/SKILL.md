---
name: azure-open-pr
description: Create Azure Repos pull requests via CLI with az repos pr create
allowed-tools: Read, Bash
---

# Azure Open PR

Create and manage pull requests in Azure Repos using the Azure CLI.

---

## When to Use

Invoke this skill when:
- User requests creating a pull request in Azure Repos
- User mentions "az repos pr create" or Azure DevOps PR workflows
- Task involves submitting code changes to Azure Repos for review

---

## Agent Workflow

### Step 1: Verify Prerequisites

Check in this order:

```bash
# 1. Check Azure CLI installed
az --version

# 2. Check DevOps extension installed
az extension list --query "[?name=='azure-devops'].version" -o tsv

# 3. Check authentication status
az account show

# 4. Check defaults configured
az devops configure --list
```

**If missing, install:**
```bash
az extension add --name azure-devops
az login
az devops configure --defaults organization=https://dev.azure.com/ORG project=PROJECT
```

### Step 2: Validate Git State

```bash
# 1. Verify in git repository
git rev-parse --git-dir

# 2. Get current branch name
git branch --show-current

# 3. Check if branch exists on remote
git ls-remote --heads origin $(git branch --show-current)

# 4. Check for unpushed commits
git status -sb
```

**If branch not on remote:**
```bash
git push -u origin $(git branch --show-current)
```

### Step 3: Gather PR Information

**Required:**
- `--title`: PR title (short, descriptive)
- `--description`: Detailed description with context

**Recommended:**
- `--target-branch`: Target branch (usually `main` or `develop`)
- `--draft`: Set `true` for work-in-progress
- `--auto-complete`: Set `true` to auto-merge when policies pass
- `--delete-source-branch`: Set `true` to cleanup after merge

**Optional:**
- `--reviewers`: Space-separated reviewer emails/aliases
- `--work-items`: Space-separated work item IDs (e.g., `123 456`)

### Step 4: Create Pull Request

**Basic PR:**
```bash
az repos pr create \
  --title "Brief descriptive title" \
  --description "Detailed description of changes"
```

**Production-ready PR:**
```bash
az repos pr create \
  --title "feat: Add user authentication" \
  --description "$(cat <<'EOF'
## Summary
Implements OAuth2 authentication flow

## Changes
- Added auth middleware
- Updated user model
- Added login/logout endpoints
EOF
)" \
  --target-branch main \
  --auto-complete true \
  --delete-source-branch true \
  --work-items 1234 5678
```

**Draft PR:**
```bash
az repos pr create \
  --title "WIP: Feature implementation" \
  --description "Early draft for feedback" \
  --draft true
```

---

## Command Reference

### Essential Flags

| Flag | Required | Default | Purpose |
|------|----------|---------|---------|
| `--title` | ✅ Yes | - | PR title (concise summary) |
| `--description` | ⚠️ Recommended | Empty | Detailed PR description |
| `--source-branch` | No | Current branch | Source branch name |
| `--target-branch` | No | Repo default | Target branch (main/develop) |
| `--draft` | No | `false` | Mark as draft PR |
| `--auto-complete` | No | `false` | Auto-merge when policies pass |
| `--delete-source-branch` | No | `false` | Delete source after merge |
| `--reviewers` | No | None | Required reviewers (emails) |
| `--work-items` | No | None | Link work items by ID |
| `--open` | No | - | Open in browser after creation |
| `-r` / `--repository` | No | Current repo | Specify repository |
| `-p` / `--project` | No | Default | Override project |

### Common Patterns

**With reviewers:**
```bash
az repos pr create \
  --title "Fix critical bug" \
  --description "Resolves issue #123" \
  --reviewers user1@example.com user2@example.com
```

**Link work items:**
```bash
az repos pr create \
  --title "Feature XYZ" \
  --description "Implements feature XYZ" \
  --work-items 1234 5678
```

**Cross-repository PR:**
```bash
az repos pr create \
  --title "Shared component update" \
  --repository shared-components \
  --project MyProject
```

---

## Best Practices

### For Agents

1. **Always verify prerequisites** before attempting PR creation
2. **Check branch is pushed** to avoid remote branch errors
3. **Use heredocs** for multi-line descriptions to preserve formatting
5. **Set `--auto-complete true`** for automated workflows
6. **Always specify `--target-branch`** explicitly to avoid surprises

### For PR Quality

1. **Title format**: Use conventional commits (`feat:`, `fix:`, `docs:`, etc.)
2. **Description structure**:
   - Summary: What and why
   - Changes: Bullet list of modifications
3. **Link work items** when available for traceability
4. **Use draft PRs** for early feedback or incomplete work
5. **Enable auto-complete** for routine changes that pass CI

---

## Additional Commands

**List open PRs:**
```bash
az repos pr list --status active
```

**Update PR:**
```bash
az repos pr update --id <pr-id> --title "New title" --description "New description"
```

**Set auto-complete on existing PR:**
```bash
az repos pr update --id <pr-id> --auto-complete true --delete-source-branch true
```

**Check PR status:**
```bash
az repos pr show --id <pr-id>
```
