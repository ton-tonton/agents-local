## Repository Overview

Workspace for AI agent skills and subagent definitions. There is no build, test, or lint pipeline — verification is running `python3 scripts/sync_skills.py`.

## Commands

```bash
# Sync skills from upstream repos defined in skills.yaml
python3 scripts/sync_skills.py

# Preview changes without modifying files
python3 scripts/sync_skills.py --dry-run
```

## Skills Architecture

Skills live in `skills/<name>/SKILL.md`. Two types, both tracked in `skills.yaml`:

- **Synced skills** (`skills:` in `skills.yaml`): Mirrored from upstream via `rsync -av --delete`. **Do not edit locally** — changes are overwritten on sync; edit upstream instead.
- **Local skills** (`local_skills:` in `skills.yaml`): Authored and maintained in this repo.

> [!WARNING]
> Any directory in `skills/` not listed in `skills.yaml` (under `skills:` or `local_skills:`) is automatically deleted on sync. Always register new local skills under `local_skills:` in `skills.yaml`.

Commit `skills.lock` whenever `skills.yaml` changes.

## Subagents (`agents/*.md`)

Worker subagents dispatched from the main session.

- Defined in `agents/<name>.md` with YAML frontmatter (`name`, `description`, `model`, optional `tools`).
- **Thin subagent + rich skills pattern**: Subagents stay small and workflow-focused, loading domain skills at runtime rather than embedding knowledge.
