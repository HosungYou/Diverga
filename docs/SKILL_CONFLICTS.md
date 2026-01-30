# Skill Conflicts and Resolution Guide

## Overview

When multiple plugins/skills have the same or similar command names, conflicts can occur. This document explains the identified conflicts and how to resolve them.

---

## Conflict: `/review` Command

### Issue

Three different skills respond to "review":

| Skill | Full Name | Purpose |
|-------|-----------|---------|
| OMC Review | `/oh-my-claudecode:review` | Plan review using **Critic agent** (Opus) |
| OMC Code Review | `/oh-my-claudecode:code-review` | Code review using **code-reviewer agent** (Opus) |
| Codex Reviewer | `/code-reviewer` | Code review using **Codex CLI** (gpt-5.2-codex) |

### What Happens

When you type `/review`, the **OMC Review** skill takes priority because:
1. OMC is registered as a plugin with explicit command mappings
2. Local skills have lower priority than plugin commands
3. Short command names match first

### Resolution: Use Fully Qualified Names

| Task | Command to Use |
|------|----------------|
| Plan review (Critic) | `/oh-my-claudecode:review` |
| Code review (OMC agent) | `/oh-my-claudecode:code-review` |
| Code review (Codex CLI) | `/code-reviewer` |

---

## How to Call Codex CLI Directly

### Option 1: Use the Skill (Recommended)

```
/code-reviewer
```

This invokes the local skill at `~/.claude/skills/code-reviewer/SKILL.md` which:
1. Verifies Codex authentication
2. Runs `codex exec -m gpt-5.2-codex` with review prompt
3. Returns structured review report

### Option 2: Direct CLI Call

If the skill doesn't activate, you can call Codex directly:

```bash
# Full review
codex exec -m gpt-5.2-codex -C "$(pwd)" "
Conduct a comprehensive code and architecture review of this project.
Focus on:
1. Code Quality
2. Architecture
3. Security
4. Performance
5. Maintainability
"

# Quick security review
codex exec -m gpt-5.2-codex -C "$(pwd)" "
Perform security-focused review:
1. OWASP Top 10 vulnerabilities
2. Input validation
3. Authentication issues
"
```

### Option 3: Create a Distinct Skill

To avoid conflicts entirely, create a uniquely named skill:

```bash
mkdir -p ~/.claude/skills/codex-review
```

Create `~/.claude/skills/codex-review/SKILL.md`:

```markdown
---
name: codex-review
description: Code review using OpenAI Codex CLI (gpt-5.2-codex)
---

# Codex Review

When triggered by `/codex-review`, execute:

```bash
codex exec -m gpt-5.2-codex -C "$(pwd)" "
[review prompt here]
"
```
```

---

## Skill Priority Order

Claude Code resolves skill conflicts in this order:

1. **Plugin commands** (highest priority)
   - `oh-my-claudecode:*`
   - `diverga:*`
   - Other installed plugins

2. **Local skills** (lower priority)
   - `~/.claude/skills/*/SKILL.md`

3. **Implicit matching** (lowest priority)
   - Keyword detection in conversation

---

## OMC vs Diverga Review Commands

### OMC Review Commands

| Command | Agent | Model | Purpose |
|---------|-------|-------|---------|
| `/oh-my-claudecode:review` | Critic | Opus | Review plans for quality |
| `/oh-my-claudecode:code-review` | code-reviewer | Opus | Review code for quality |
| `/oh-my-claudecode:security-review` | security-reviewer | Opus | Security audit |

### Diverga Review Agents (Task Tool)

| Agent | Model | Purpose |
|-------|-------|---------|
| `diverga:f1` | Haiku | Internal consistency check |
| `diverga:f3` | Sonnet | Reproducibility audit |
| `diverga:f4` | Sonnet | Bias/trustworthiness detection |
| `diverga:g3` | Sonnet | Peer review strategy |

### Codex CLI

| Command | Model | Purpose |
|---------|-------|---------|
| `/code-reviewer` | gpt-5.2-codex | Full code/architecture review |
| Direct `codex exec` | gpt-5.2-codex | Custom prompts |

---

## Recommendations

1. **For plan review**: Use `/oh-my-claudecode:review`
2. **For code review with Claude agents**: Use `/oh-my-claudecode:code-review`
3. **For code review with Codex**: Use `/code-reviewer` or direct `codex exec`
4. **For security audit**: Use `/oh-my-claudecode:security-review`
5. **For Diverga-specific review**: Use Task tool with `diverga:f*` or `diverga:g3`

---

## Debugging Skill Loading

To verify which skill was loaded:

```
/help
```

Or check the session reminder for active skills:

```
The following skills were invoked in this session...
```

If the wrong skill is activated, use the fully qualified name as shown above.
