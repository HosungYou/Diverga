# In-Codex Setup

## Goal

LongTable should let a researcher begin setup without leaving Codex, but this
must match the actual Codex runtime surface.

## Constraint

Current Codex builds may reject `/prompts`. Installed prompt files under
`~/.codex/prompts/` are therefore not a reliable product surface.

Codex skills under `~/.codex/skills/` are the preferred native adapter surface.

## Current Approach

Install Codex skills:

```bash
longtable codex install-skills
```

Then invoke naturally inside Codex:

```text
longtable: help me set up my research workspace
lt explore: I need to narrow this topic
lt panel: review this methods section before I commit
```

If a Codex build exposes explicit skill shortcuts, `$longtable` is the manual
entry.

Persistence still belongs to the setup/runtime layer. In-session setup should
produce either:

1. the exact `longtable codex persist-init ... --install-skills` command to
   persist setup
2. a strict JSON block that can be piped into
   `longtable codex persist-init --stdin --install-skills`

## Product Rule

The default onboarding story remains:

- `longtable init`
- then `longtable start`
- then `cd "<project-path>" && codex`

The important distinction is:

- `init` and `start` are terminal commands
- the research conversation begins after Codex is opened inside the created
  project directory

In-Codex setup is an optional integration path, not the baseline user journey.
