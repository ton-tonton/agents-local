---
name: azure-task
description: Azure DevOps work item commands - view/update descriptions, comments, state, assignee, and title using Azure CLI
allowed-tools: Read, Bash
---

# Azure Task

Manage Azure DevOps work items (tasks/tickets) using Azure CLI commands.

---

## When to Use

Invoke this skill when:
- User wants to view a task/ticket description
- User wants to update a task description
- User wants to add a comment to a task
- User wants to create a task (optionally under a story URL)
- User wants to update state, estimate, or assignee
- User mentions work item IDs or `az boards` commands
- User needs to interact with Azure DevOps work items via CLI

---

## Verify Prerequisites

Check before running commands:

```bash
# 1. Azure CLI installed
az --version

# 2. DevOps extension installed
az extension list --query "[?name=='azure-devops'].version" -o tsv

# 3. Authenticated
az account show
```

**If missing, install and authenticate:**
```bash
az extension add --name azure-devops
az login
az devops configure --defaults organization=https://dev.azure.com/ORG project=PROJECT
```

> **Auth:** authenticate with `az login`, or set the `AZURE_DEVOPS_EXT_PAT` environment variable.
> Never hardcode a PAT in commands.

---

## Command Examples

### View Task Description

**Basic - Get description only:**
```bash
az boards work-item show --id <WORK_ITEM_ID> --query 'fields."System.Description"' -o tsv
```

**Full details:**
```bash
az boards work-item show --id <WORK_ITEM_ID> --expand all
```

> `show` does **not** accept `--project` — work item IDs are unique across the org.
> Use `--org` only if no default is configured.

**Specific fields:**
```bash
# Title
az boards work-item show --id <WORK_ITEM_ID> --query 'fields."System.Title"' -o tsv

# State
az boards work-item show --id <WORK_ITEM_ID> --query 'fields."System.State"' -o tsv

# Assigned To (it's an object — pick a sub-field, else tsv prints messy output)
az boards work-item show --id <WORK_ITEM_ID> --query 'fields."System.AssignedTo".uniqueName' -o tsv
```

> **Note:** `System.Description` and comments are stored as **HTML rich text**.
> Reading with `-o tsv` returns raw HTML tags (`<div>`, `<br>`, etc.).

**Read the latest comment** (comments live in the `System.History` field):
```bash
az boards work-item show --id <WORK_ITEM_ID> --query 'fields."System.History"' -o tsv
```

**Read the full comment thread** (needs the REST API — no `az boards` command exists):
```bash
az devops invoke --area wit --resource comments \
  --route-parameters project=<PROJECT> workItemId=<WORK_ITEM_ID> \
  --api-version 7.1-preview -o json
```

### Update Task Description

**Simple update:**
```bash
az boards work-item update --id <WORK_ITEM_ID> --description "New description text"
```

**Multi-line description with paragraphs:**
```bash
az boards work-item update --id <WORK_ITEM_ID> \
  --description "$(cat <<'EOF'
<b>Status Update:</b><br><br>
<b>1. Issue Analysis</b><br>
• Root Cause: Identification of the underlying problem.<br>
• Impact: Description of affected components.<br><br>
<b>2. Proposed Solution</b><br>
• Implementation details affecting the API.<br>
• Required configuration changes.<br>
• Verification steps for QA.
EOF
)"
```

**Using fields parameter:**
```bash
az boards work-item update --id <WORK_ITEM_ID> \
  --fields "System.Description=Updated description text"
```

### Add Comment to Task

**Simple comment:**
```bash
az boards work-item update --id <WORK_ITEM_ID> --discussion "Comment text here"
```

**Multi-line comment with paragraphs:**
```bash
az boards work-item update --id <WORK_ITEM_ID> \
  --discussion "$(cat <<'EOF'
<b>Daily Scrum Update:</b><br><br>
<b>Completed:</b><br>
• Refactored the authentication service.<br>
• Added unit tests for the login flow.<br><br>
<b>In Progress:</b><br>
• Working on the user profile update endpoint.<br>
• Debugging the timeout issue in the staging environment.<br><br>
<b>Blockers:</b><br>
• Waiting for API documentation from the third-party provider.
EOF
)"
```

### Create a Task

**Basic:**
```bash
az boards work-item create --title "Implement login endpoint" --type Task
```

**Capture the new ID into a variable:**
```bash
TASK_ID=$(az boards work-item create --title "Implement login endpoint" --type Task --query "id" -o tsv)
```

### Link a Task to a Story

**Get the story ID from its URL** (format: `https://dev.azure.com/{org}/{project}/_workitems/edit/{id}`):
```bash
STORY_ID=$(echo "$STORY_URL" | grep -oE 'edit/[0-9]+' | grep -oE '[0-9]+')
```

**Link the Task as a child of the Story:**
```bash
az boards work-item relation add --id <TASK_ID> --relation-type parent --target-id <STORY_ID>
```

> Verify the relation-type name on your install: `az boards work-item relation list-type -o table`.

### Update State

```bash
az boards work-item update --id <WORK_ITEM_ID> --state "Active"
```

### Update Estimate (person hours)

**Original + Remaining (initial estimate):**
```bash
az boards work-item update --id <WORK_ITEM_ID> \
  --fields "Microsoft.VSTS.Scheduling.OriginalEstimate=8" \
           "Microsoft.VSTS.Scheduling.RemainingWork=8"
```

**All three (track progress):**
```bash
az boards work-item update --id <WORK_ITEM_ID> \
  --fields "Microsoft.VSTS.Scheduling.OriginalEstimate=8" \
           "Microsoft.VSTS.Scheduling.CompletedWork=3" \
           "Microsoft.VSTS.Scheduling.RemainingWork=5"
```

> The three fields are independent — Azure does **not** auto-calculate them.
> Update Remaining Work as you progress; it drives the sprint burndown.

---

## Command Reference

### Show Command

```bash
az boards work-item show --id <ID> [options]
```

| Flag | Required | Description |
|------|----------|-------------|
| `--id` | ✅ Yes | Work item ID |
| `--fields` `-f` | No | Comma-separated list of fields to return |
| `--expand` | No | Attributes to expand: `all`, `fields`, `links`, `relations`, `none` |
| `--query` | No | JMESPath query to filter output |
| `--organization` | No | Organization URL (if not using default) |

> `show` has **no** `--project` flag — work item IDs are unique across the org.

### Update Command

```bash
az boards work-item update --id <ID> [options]
```

| Flag | Required | Description |
|------|----------|-------------|
| `--id` | ✅ Yes | Work item ID |
| `--description` | No | Update description field |
| `--discussion` | No | Add a comment to the discussion |
| `--fields` | No | Space-separated field=value pairs |
| `--title` | No | Update title |
| `--assigned-to` | No | Update assignee |
| `--state` | No | Update state — capitalized, process-dependent (e.g., New, Active, Resolved, Closed) |
| `--project` | No | Project name (if not using default) |
| `--organization` | No | Organization URL (if not using default) |

### Create Command

```bash
az boards work-item create --title <TITLE> --type <TYPE> [options]
```

| Flag | Required | Description |
|------|----------|-------------|
| `--title` | ✅ Yes | Work item title |
| `--type` | ✅ Yes | Work item type (e.g., Task, Bug, User Story) |
| `--assigned-to` | No | Assignee email |
| `--description` | No | Description (HTML) |
| `--discussion` | No | Initial comment |
| `--fields` | No | Space-separated field=value pairs (e.g., estimate) |
| `--project` | No | Project name (if not using default) |
| `--organization` | No | Organization URL (if not using default) |

> Tip: add `--query "id" -o tsv` to capture the new ID into a variable.

### Relation Command

```bash
az boards work-item relation add --id <ID> --relation-type <TYPE> --target-id <TARGET_ID>
```

| Flag | Required | Description |
|------|----------|-------------|
| `--id` | ✅ Yes | Work item to add the relation on |
| `--relation-type` | ✅ Yes | Relation type (e.g., `parent`, `child`, `related`) |
| `--target-id` | ✅ Yes | The other work item's ID |

> List the exact relation-type names on your install: `az boards work-item relation list-type -o table`.

---

## Common Field Names

| Field | System Name | Example Value |
|-------|-------------|---------------|
| Title | `System.Title` | "Fix login bug" |
| Description | `System.Description` | "Detailed description..." |
| State | `System.State` | "Active", "Resolved", "Closed" |
| Assigned To | `System.AssignedTo` | "user@example.com" |
| Area Path | `System.AreaPath` | "Project\Team" |
| Iteration Path | `System.IterationPath` | "Project\Sprint 1" |
| Work Item Type | `System.WorkItemType` | "Task", "Bug", "User Story" |
| Original Estimate | `Microsoft.VSTS.Scheduling.OriginalEstimate` | "8" (person hours) |
| Remaining Work | `Microsoft.VSTS.Scheduling.RemainingWork` | "8" (person hours) |
| Completed Work | `Microsoft.VSTS.Scheduling.CompletedWork` | "3" (person hours) |

---

## Best Practices

1. **Use heredocs for multi-line HTML text** - Preserves formatting and line breaks
2. **Use `-o tsv` to extract single field values cleanly**
3. **`create`/`update` accept `--project`; `show` does not** - work item IDs are org-unique
4. **Read with `--query` before updating** - confirm the field first
