---
name: doctor
description: |
  System diagnostics and health checks for Diverga plugin.
  OpenClaw-style Check-Report-Fix pattern with 5-layer diagnostics.
  Triggers: /diverga:doctor, diverga doctor, system check, diagnose, 진단
version: "9.0.0"
---

# Diverga Doctor

**Version**: 8.4.0
**Trigger**: `/diverga:doctor`

## Description

System diagnostics for the Diverga plugin. Checks plugin health, skill sync, configuration validity, API keys, and project state. Reports issues with actionable fix commands.

Follows OpenClaw Check-Report-Fix pattern: every detected issue includes a fix recommendation.

## Instructions

When user invokes `/diverga:doctor`, execute all 5 diagnostic layers sequentially and display results.

### Layer 1: Plugin Health

**Check plugin registration:**
- Read `/Users/hosung/.claude/plugins/installed_plugins.json`
- Verify `diverga@diverga` entry exists
- Extract version and install date

**Check config JSON validity:**
- Read `/Users/hosung/.claude/plugins/diverga/config/diverga-config.json`
- Verify it parses as valid JSON
- Check required fields exist: `version`, `human_checkpoints`, `language`

**Report format:**
```
PLUGIN HEALTH
  Registration:    [PASS - diverga@diverga v8.4.0 | FAIL - not found in installed_plugins.json]
  Config file:     [PASS - valid JSON | FAIL - missing or invalid]
  Config fields:   [PASS - all required fields present | WARN - missing: field1, field2]
```

**Fix if FAIL:**
- Registration missing: "Run: /plugin install diverga"
- Config missing: "Run: /diverga:setup to regenerate configuration"
- Config invalid JSON: "Config file is corrupted. Run: /diverga:setup to regenerate"

### Layer 2: Skill Sync

**Check skill counts match between plugin and local cache:**
- Use Glob to count directories in `/Users/hosung/.claude/plugins/diverga/skills/*/SKILL.md`
- Use Glob to count directories in `/Users/hosung/.claude/skills/diverga-*/SKILL.md` (exclude `diverga-diverga` prefix duplication — count unique skill names)
- Compare counts

**Check for missing skills in local cache:**
- For each skill in plugin directory, check if corresponding `diverga-{name}` exists in local skills
- List any missing skills

**Report format:**
```
SKILL SYNC
  Plugin skills:   [count] skills in plugin directory
  Local skills:    [count] skills in local cache
  Sync status:     [PASS - all synced | WARN - X skills missing locally]
  Missing:         [list of missing skill names, if any]
```

**Fix if WARN:**
- "Missing local skills. To resync, reinstall the plugin or manually copy:"
- For each missing skill: "  cp -r ~/.claude/plugins/diverga/skills/{name} ~/.claude/skills/diverga-{name}"

### Layer 3: Config Validity

**Deep validation of diverga-config.json:**
- Read `/Users/hosung/.claude/plugins/diverga/config/diverga-config.json`
- Check `version` field matches "8.4.0"
- Check `human_checkpoints` object exists and has `enabled` (boolean) and `required` (array)
- Check `language` is one of: "en", "ko", "auto"
- Check `model_routing` has `high`, `medium`, `low` keys if present

**Report format:**
```
CONFIG VALIDITY
  Version field:   [PASS - 8.4.0 | WARN - version mismatch: found X.Y.Z]
  Checkpoints:     [PASS - configured | FAIL - missing or malformed]
  Language:        [PASS - "en" | WARN - unexpected value: "XX"]
  Model routing:   [PASS - configured | SKIP - not set (using defaults)]
```

**Fix if issues found:**
- Version mismatch: "Config version X.Y.Z doesn't match plugin 8.4.0. Run: /diverga:setup to update"
- Checkpoints malformed: "Run: /diverga:setup to reconfigure checkpoints"

### Layer 4: API Keys

**Check 8 environment variables using Bash tool (`echo $VAR_NAME`):**

| Variable | Purpose | Required? |
|----------|---------|-----------|
| `GROQ_API_KEY` | LLM screening (recommended) | Recommended |
| `ANTHROPIC_API_KEY` | Claude API | Recommended |
| `OPENAI_API_KEY` | OpenAI screening | Optional |
| `GEMINI_API_KEY` | Gemini visualization | Optional |
| `SEMANTIC_SCHOLAR_API_KEY` | Paper retrieval | Optional |
| `OPENALEX_EMAIL` | OpenAlex polite pool | Optional |
| `SCOPUS_API_KEY` | Scopus access | Optional |
| `WOS_API_KEY` | Web of Science | Optional |

For each variable, use Bash: `echo "${VAR_NAME:+configured}"` — if output is "configured", it's set; if empty, it's not set.

**Report format:**
```
API STATUS
  Groq:              [configured | NOT SET -> export GROQ_API_KEY=your_key]
  Anthropic:         [configured | NOT SET -> export ANTHROPIC_API_KEY=your_key]
  OpenAI:            [configured | not set (optional)]
  Gemini:            [configured | not set (optional)]
  Semantic Scholar:  [configured | not set (optional)]
  OpenAlex:          [configured | not set (optional)]
  Scopus:            [configured | not set (optional)]
  Web of Science:    [configured | not set (optional)]
```

**Fix if NOT SET (recommended keys):**
- Show `export VAR_NAME=your_key_here` for each missing recommended key
- For optional keys, just note "(optional)" — no urgent fix needed

### Layer 5: Project State

**Check for active research project:**
- Use Glob to check if `.research/project-state.yaml` exists in current working directory
- If exists: Read it and validate YAML structure (has `project_name`, `current_stage`)
- Also check if `.research/` directory exists with expected subdirectories

**Report format:**
```
PROJECT STATE
  Active project:  [project name | No active project]
  State file:      [PASS - valid | WARN - invalid YAML | SKIP - no project]
  Research dir:    [PASS - structure intact | WARN - missing subdirs | SKIP - no project]
```

**Fix if issues:**
- Invalid YAML: "Project state file is corrupted. Run: /diverga:setup in your project directory"
- Missing subdirs: "Run: /diverga:setup to reinitialize project structure"
- No project: "Start a new project with: /diverga:setup or describe your research topic"

### Final Summary

After all 5 layers, display overall status:

```
══════════════════════════════════════════════
DIVERGA SYSTEM DIAGNOSTICS v8.4.0
══════════════════════════════════════════════

[Layer 1-5 results as shown above]

------------------------------------------
OVERALL: [HEALTHY | X WARNING(S) | X ERROR(S)]

[If issues found, numbered list:]
  1. [Issue description] -> [Fix command]
  2. [Issue description] -> [Fix command]
  ...

[If healthy:]
  All systems operational. Diverga is ready to use.
  Run /diverga:help to see all 44 agents and commands.
══════════════════════════════════════════════
```

## Implementation Notes

- Execute all Bash commands for API key checks in PARALLEL (single message, multiple Bash calls)
- Use Read tool for JSON/YAML file checks
- Use Glob tool for skill counting
- This skill is READ-ONLY — it does not modify any files
- If any individual check encounters an error (file not readable, etc.), show "UNABLE TO CHECK" rather than crashing
- Total execution target: under 10 seconds
