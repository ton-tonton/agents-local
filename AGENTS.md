## What this repo is

A curated collection of AI agent **skills** and **subagent definitions**, plus a sync utility that pulls skills from upstream repositories. This is not an application — it's a configuration/content workspace. The "code" is almost entirely Markdown (`SKILL.md`, agent definitions) with one Python sync script.

## Commands

```bash
# Sync skills from upstream repos defined in skills.yaml (requires pyyaml + rsync)
python3 scripts/sync_skills.py

# Python version is pinned via mise
mise install
```

There is no build, test, or lint setup — verification means re-running the sync and inspecting the result.

## Architecture

**Two kinds of skills, distinguished by whether they appear in `skills.yaml`:**

- **Synced skills** — listed under `skills:` in `skills.yaml`. `sync_skills.py` mirrors them from an upstream `path` into `skills/<name>/` using `rsync -av --delete`. **Local edits to these are destroyed on next sync** — change them upstream instead.
- **Local skills** — present in `skills/` but absent from `skills.yaml` (currently: `azure-pr`, `azure-task`, `commit`, `cooking`, `planning`, `push-pr`, `rails-way`, `ship-it`). These are authored/owned here and version-controlled. `--delete` only touches directories the script syncs, so local skills are untouched.

Before editing anything in `skills/`, check whether its name is in `skills.yaml`. If it is, edits are temporary.

**`sync_skills.py` resolution order** for each skill name: the per-entry `path` (tried as `path/<name>` then as a direct path), then a global `upstream_path` (string or list). Missing sources warn and skip rather than fail the run.

**Skill format:** each `skills/<name>/SKILL.md` starts with YAML frontmatter (`name`, `description`) followed by the skill body. Some skills carry supporting `data/` and `scripts/` subdirectories (e.g. `ui-ux-pro-max`).

**Agents** (`agents/*.md`): subagent definitions with YAML frontmatter — `name`, `description`, `model` (`inherit`/`sonnet`/`opus`/`haiku`), optional `tools` (array, e.g. `["Read", "Grep"]`; omit for all), optional `color`. A file is a subagent because it lives in `agents/` — there is no `mode` field. Current agents:

- `task-smith` — turns a rough request into a structured, developer-ready task.
- `rails-ninja` — version-aware Rails implementation worker (adapts to Rails 7.x/8.x).

**Pattern: thin subagent + rich skills.** An agent file stays small and just says
"do this workflow"; the real knowledge lives in skills it pulls in. `rails-ninja`
is thin — it has the `Skill` tool and loads `rails-way` (patterns) + `ship-it`
(test-first loop) at runtime rather than embedding them. This keeps the knowledge
reusable in the main session too, and the agent easy to read.

These are worker subagents, dispatched from the main session via the `Agent` tool. The `cooking` skill orchestrates them end-to-end from a **required Azure work item link**: load item (`azure-task`) → spec (`task-smith`, story only) → plan (`planning`) → build (`rails-ninja`, following `ship-it`) → test → review (`code-review-excellence`) → PR (`push-pr`), updating the work item's state and completed time along the way. The orchestrator lives as a **skill**, not an agent, because only the main session can reliably dispatch subagents.

## Conventions

- `.editorconfig` governs formatting: LF endings, final newline, 2-space indent (4 for Python).
- Adding a new local skill: create `skills/<name>/SKILL.md`, do **not** add it to `skills.yaml`, and commit it.
- `.claude/` and `.github/` are gitignored.
