---
name: azure-task
description: Azure DevOps work item commands - view/update descriptions and add comments using Azure CLI
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
- User mentions work item IDs or `az boards` commands
- User needs to interact with Azure DevOps work items via CLI

---

## Command Examples

### View Task Description

**Basic - Get description only:**
```bash
az boards work-item show --id <WORK_ITEM_ID> --query "fields.['System.Description']" -o tsv
```

**Full details:**
```bash
az boards work-item show --id <WORK_ITEM_ID> --project <PROJECT_NAME>
```

**Specific fields:**
```bash
# Title
az boards work-item show --id <WORK_ITEM_ID> --query "fields.['System.Title']" -o tsv

# State
az boards work-item show --id <WORK_ITEM_ID> --query "fields.['System.State']" -o tsv

# Assigned To
az boards work-item show --id <WORK_ITEM_ID> --query "fields.['System.AssignedTo']" -o tsv
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
First paragraph of the description explaining the task purpose.

Second paragraph with implementation details and requirements.

Third paragraph with additional notes or acceptance criteria.
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
First paragraph of the comment explaining the update.

Second paragraph with additional context or details.

Third paragraph with next steps or questions.
EOF
)"
```

---

## Command Reference

### Show Command

```bash
az boards work-item show --id <ID> [options]
```

| Flag | Required | Description |
|------|----------|-------------|
| `--id` | ✅ Yes | Work item ID |
| `--fields` | No | Comma-separated list of fields to return |
| `--query` | No | JMESPath query to filter output |
| `--project` | No | Project name (if not using default) |
| `--organization` | No | Organization URL (if not using default) |

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
| `--state` | No | Update state (e.g., active, resolved, closed) |
| `--project` | No | Project name (if not using default) |
| `--organization` | No | Organization URL (if not using default) |

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

---

## Best Practices

1. **Use heredocs for multi-line text** - Preserves formatting and line breaks
2. **Use `-o tsv` for clean output** - When querying specific fields
3. **Specify project explicitly** - When working across multiple projects
4. **Test with --query first** - Verify output before updating
5. **Keep descriptions under limit** - While 1M chars is generous, keep it readable

---

## Prerequisites

The `azure-devops` extension is required:

```bash
# Install extension
az extension add --name azure-devops

# Configure defaults (optional)
az devops configure --defaults organization=https://dev.azure.com/ORG project=PROJECT
```
