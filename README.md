# Agent Skills Management System

A structured system for managing, syncing, and organizing AI agent skills from upstream repositories. This workspace maintains a local collection of specialized skills that enhance agent capabilities across development, design, review, and documentation tasks.

## 🎯 Purpose

Maintain a curated set of AI agent skills that can be:
- Synced from upstream repositories
- Extended with custom local skills
- Versioned and tracked independently
- Configured per project or globally

## 📁 Structure

```
agents-local/
├── skills.yaml               # Skill manifest and sync configuration
├── skills.lock               # Tracked synced skills lockfile
├── scripts/
│   └── sync_skills.py        # Automated sync utility
├── agents/                   # Subagent definitions (*.md)
└── skills/                   # Skill collection (<skill-name>/SKILL.md)
```

## 🔧 Key Components

### 1. Skills Configuration (skills.yaml)

Defines which skills to sync and their source locations:

```yaml
skills:
  - path: /path/to/upstream/skills
    name:
      - skill-1
      - skill-2
      # ... more skills
```

**Features:**
- Multiple upstream sources supported
- Per-skill path overrides
- Local skills excluded from sync

### 2. Sync Script (scripts/sync_skills.py)

Automated synchronization utility using `rsync`:

```bash
python3 scripts/sync_skills.py
```

**What it does:**
1. Reads `skills.yaml` configuration
2. Validates upstream paths
3. Syncs each listed skill via `rsync --delete`
4. Preserves local-only skills
5. Reports sync status

### 3. Agents (agents/*.md)

Subagent definitions live in this directory as Markdown files (`agents/<name>.md`).

- Contains worker subagent definitions dispatched from the main session.
- Each agent file defines its role, prompt instructions, and tool access via YAML frontmatter (`name`, `description`, `model`, `tools`).
- Follows the **thin subagent + rich skills** pattern: agent files stay small and load skills at runtime for deep domain knowledge.

### 4. Skills (skills/<skill-name>)

All agent skills live in this directory, each in its own subfolder:

- Each skill is contained in `skills/<skill-name>/SKILL.md` (with optional supporting scripts, data, or reference files).
- **Synced skills**: Mirrored from upstream repositories defined under `skills:` in `skills.yaml`.
- **Local skills**: Authored and maintained directly in this repository (listed under `local_skills:` in `skills.yaml`).

## 🚀 Quick Start

### Prerequisites

```bash
# Install dependencies
pip install pyyaml

# Verify rsync is available
which rsync
```

### Initial Setup

1. **Clone and configure:**
   ```bash
   git clone <your-repo> agents-local
   cd agents-local
   ```

2. **Edit skills.yaml:**
   ```yaml
   skills:
     - path: /path/to/upstream/skills
       name:
         - skill-name-1
         - skill-name-2
   ```

3. **Run sync:**
   ```bash
   python3 scripts/sync_skills.py
   ```

### Usage Patterns

**Check skill availability:**
```bash
ls skills/
```

**Update specific skill:**
Edit skills.yaml, then:
```bash
python3 scripts/sync_skills.py
```

**Add local skill:**
1. Create `skills/<skill-name>/SKILL.md`
2. Add `<skill-name>` under `local_skills:` in `skills.yaml`
3. Commit to version control
