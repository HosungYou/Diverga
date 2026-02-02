# Diverga Plugin Troubleshooting Guide

This guide addresses the "Unknown skill: diverga:xxx" error and explains the workaround.

---

## Problem: "Unknown skill: diverga:xxx"

When using Diverga skills with the colon prefix, you may see:

```
❯ /diverga:help
Unknown skill: diverga:help
```

---

## Root Cause

Claude Code has **two skill loading mechanisms**:

| Mechanism | Format | Reliability | Notes |
|-----------|--------|-------------|-------|
| **Local Skills** | `/diverga-help` (hyphen) | ✅ High | Loaded from `~/.claude/skills/` |
| **Plugin Skills** | `/diverga:help` (colon) | ⚠️ Variable | Requires plugin system to load correctly |

The plugin system loads skills at Claude Code startup. If the plugin cache is modified after startup, or if there's a registration issue, the colon-prefix skills won't be recognized until restart.

---

## Solution: Use Local Skills (Recommended)

### Step 1: Create Symlinks

Run this command to create local skill symlinks:

```bash
# Option A: From plugin cache
for skill_dir in ~/.claude/plugins/cache/diverga/diverga/*/skills/*/; do
  skill_name=$(basename "$skill_dir")
  ln -sf "$skill_dir" ~/.claude/skills/diverga-${skill_name}
done

# Option B: From cloned repository
cd /path/to/Diverga
for skill_dir in skills/*/; do
  skill_name=$(basename "$skill_dir")
  ln -sf "$(pwd)/$skill_dir" ~/.claude/skills/diverga-${skill_name}
done
```

### Step 2: Restart Claude Code

After creating symlinks, restart Claude Code for skills to be discovered.

### Step 3: Use Hyphen Prefix

```bash
/diverga-help       # ✅ Works reliably
/diverga-memory     # ✅ Works reliably
/diverga-a1         # ✅ Works reliably
```

---

## Why Colon Prefix May Not Work

### Timing Issue

- Plugin skills are loaded at **session start**
- If you install/update Diverga during a session, changes won't be visible
- Solution: Restart Claude Code after installation

### Plugin Registration

- Plugin must be properly registered in `~/.claude/plugins/installed_plugins.json`
- The `installPath` must point to a valid directory with `.claude-plugin/plugin.json`
- The `skills` path in plugin.json must be correct

### Verification

Check plugin registration:

```bash
# Check installed plugins
cat ~/.claude/plugins/installed_plugins.json | grep -A 10 diverga

# Check plugin structure
ls ~/.claude/plugins/cache/diverga/diverga/*/
ls ~/.claude/plugins/cache/diverga/diverga/*/.claude-plugin/
ls ~/.claude/plugins/cache/diverga/diverga/*/skills/
```

---

## Comparison: OMC vs Diverga

Both plugins have the same structure:

| Component | oh-my-claudecode | Diverga |
|-----------|-----------------|---------|
| `plugin.json` | ✅ Present | ✅ Present |
| `skills/` directory | ✅ 35 skills | ✅ 51 skills |
| SKILL.md format | name, description | name, description, version |
| Colon prefix | ✅ Works | ⚠️ May not work |

The difference in behavior may be due to:
- Installation timing
- Plugin registration sequence
- Session state when skills were loaded

---

## Diagnostics

### Check Skill Files

```bash
# Verify skills have required fields
for f in ~/.claude/plugins/cache/diverga/diverga/*/skills/*/SKILL.md; do
  echo "=== $f ==="
  head -10 "$f"
done
```

### Check Local Skills

```bash
# List local skills
ls -la ~/.claude/skills/ | grep diverga
```

### Verify Symlinks

```bash
# Check symlinks point to valid targets
for link in ~/.claude/skills/diverga-*; do
  if [[ -L "$link" ]]; then
    target=$(readlink "$link")
    if [[ -d "$target" ]]; then
      echo "✅ $link -> $target"
    else
      echo "❌ $link -> $target (broken)"
    fi
  fi
done
```

---

## Setup Wizard

Run the setup wizard to automatically configure symlinks:

```
/diverga-setup
```

This will:
1. Detect Diverga installation location
2. Create 51 symlinks in `~/.claude/skills/`
3. Configure LLM provider, checkpoints, and language
4. Verify installation

---

## Still Not Working?

If skills still don't work after following this guide:

1. **Check Claude Code version**: Ensure you're using a recent version
2. **Clear cache**: `rm -rf ~/.claude/plugins/cache/diverga/`
3. **Reinstall plugin**: Clone Diverga and run setup again
4. **Report issue**: https://github.com/HosungYou/Diverga/issues

Include in your report:
- Claude Code version
- OS and version
- Output of diagnostic commands above
- Error messages
