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
├── skills.yaml              # Skill manifest and sync configuration
├── scripts/
│   └── sync_skills.py      # Automated sync utility
├── agents/                  # [LOCAL] Subagent definitions
│   ├── task-smith.md       # Rough request → structured task
│   └── rails-ninja.md    # Version-aware Rails worker
├── skills/                  # Skill collection
│   ├── cooking/            # [LOCAL] Orchestrator (work item → … → PR)
│   ├── ship-it/            # [LOCAL] Test-first implementation loop
│   ├── azure-pr/           # [LOCAL] Azure DevOps PR creation
│   ├── push-pr/            # [LOCAL] PR description + open (host-agnostic)
│   ├── code-review-excellence/
│   ├── ui-ux-pro-max/
│   └── ...                 # Additional synced skills
└── .claude/
    └── settings.local.json # Claude-specific configuration
```

## 🔧 Key Components

### 1. Skills Configuration (skills.yaml)

Defines which skills to sync and their source locations:

```yaml
skills:
  - path: /Users/tontonton/agents/antigravity-awesome-skills/skills
    name:
      - code-review-excellence
      - ui-ux-pro-max
      - docker-expert
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

Worker subagents dispatched from the main session via the `Agent` tool. The `cooking` skill orchestrates them end-to-end.

- **task-smith** ⭐ *LOCAL* - Turns a rough request into a structured, developer-ready task
- **rails-ninja** ⭐ *LOCAL* - Version-aware Rails implementation worker (Rails 7.x/8.x, Hotwire, Solid Queue)

> **Pattern: thin subagent + rich skills.** Agent files stay small ("do this workflow") and pull in skills for the real knowledge. `rails-ninja` loads `rails-way` (patterns) + `ship-it` (test-first loop) at runtime instead of embedding them — so that knowledge stays reusable in the main session too.

### 4. Skill Categories

#### Development & Code Quality
- **code-review-excellence** - Structured code review practices
- **code-documentation-code-explain** - Generate clear code explanations
- **commit** ⭐ *LOCAL* - Concise Conventional Commits (was Sentry upstream, now trimmed + owned here)
- **kaizen** - Continuous improvement methodology
- **mermaid-expert** - Generate Mermaid diagrams (flowcharts, ERDs)
- **rails-way** ⭐ *LOCAL* - Version-aware Rails patterns (7.x/8.x), pulled in by the rails-ninja agent
- **skill-rails-upgrade** - Analyze Rails apps and provide upgrade assessments

#### Pull Request Management
- **push-pr** ⭐ *LOCAL* - Host-agnostic PR description + open (delegates to the host opener)
- **azure-pr** ⭐ *LOCAL* - Azure CLI PR automation (opener for Azure Repos)
- **azure-task** ⭐ *LOCAL* - Manage Azure DevOps work items
- **comprehensive-review-pr-enhance** - Detailed PR descriptions

#### Design & Frontend
- **ui-ux-pro-max** - Comprehensive UI/UX design system (50+ styles, 21 palettes)
- **frontend-design** - Production-grade frontend patterns
- **tailwind-design-system** - Tailwind CSS v4 best practices
- **angular** - Modern Angular (v20+) expert (Signals, Standalone, Zoneless)
- **angular-best-practices** - Angular performance optimization guide

#### Infrastructure & Security
- **docker-expert** - Container optimization and security
- **postgres-best-practices** - Database performance tuning
- **vulnerability-scanner** - Security analysis (OWASP 2025)

#### Process & Planning
- **ship-it** ⭐ *LOCAL* - Stack-agnostic test-first implementation loop, custom from `workflow-patterns`
- **cooking** ⭐ *LOCAL* - Orchestrates Azure work item → plan → build → test → review → PR (tracks state + time)
- **planning** ⭐ *LOCAL* - Atomic task planning, custom from `concise-planning`, `plan-writing`
- **prompt-engineering** - Prompt optimization techniques

#### Content & Research
- **youtube-summarizer** - Extract transcripts and generate detailed summaries from videos

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
1. Create `skills/my-custom-skill/SKILL.md`
2. Do NOT add to skills.yaml
3. Commit to version control
