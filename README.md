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
├── skills/                  # Skill collection
│   ├── azure-open-pr/      # [LOCAL] Azure DevOps PR creation
│   ├── push-pr/            # [LOCAL] Quick PR generation
│   ├── code-review-excellence/
│   ├── comprehensive-review-pr-enhance/
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

### 3. Skill Categories

#### Development & Code Quality
- **code-review-excellence** - Structured code review practices
- **code-documentation-code-explain** - Generate clear code explanations
- **kaizen** - Continuous improvement methodology

#### Pull Request Management
- **push-pr** ⭐ *LOCAL* - Quick PR creation for Azure Repos
- **azure-open-pr** ⭐ *LOCAL* - Azure CLI PR automation
- **comprehensive-review-pr-enhance** - Detailed PR descriptions

#### Design & Frontend
- **ui-ux-pro-max** - Comprehensive UI/UX design system (50+ styles, 21 palettes)
- **frontend-design** - Production-grade frontend patterns
- **tailwind-patterns** - Tailwind CSS v4 best practices

#### Infrastructure & Security
- **docker-expert** - Container optimization and security
- **postgres-best-practices** - Database performance tuning
- **vulnerability-scanner** - Security analysis (OWASP 2025)

#### Process & Planning
- **concise-planning** - Atomic task planning
- **prompt-engineering** - Prompt optimization techniques

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
