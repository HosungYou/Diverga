# Diverga Plugin Troubleshooting Guide

This guide documents the complete debugging journey for the "Unknown skill: diverga:xxx" error, including root causes and solutions.

---

## Problem: "Unknown skill: diverga:xxx"

When using Diverga skills, you may see:

```
❯ /diverga:help
Unknown skill: diverga:help

❯ /diverga-help
Unknown skill: diverga-help
```

**Even when the plugin shows as "Installed" with skills listed!**

---

## TL;DR - Quick Fix

```bash
# 1. Update marketplace in Claude Code
/plugin → Marketplaces → Update marketplace

# 2. Uninstall and reinstall
/plugin → Installed → diverga → Uninstall
/plugin → Marketplaces → diverga → Install

# 3. Restart Claude Code
```

If that doesn't work, use the **Manual Fix** below.

---

## Root Cause Analysis

After 6+ hours of debugging, we identified **THREE interconnected issues**:

### Issue 1: Missing `version` Field in SKILL.md (CRITICAL)

**Symptom**: Plugin shows "Installed" but skills show "Unknown skill"

**Cause**: Claude Code requires `version` field in SKILL.md frontmatter:

```yaml
# ❌ WRONG - Skills won't load
---
name: help
description: Diverga help guide
---

# ✅ CORRECT - Skills load properly
---
name: help
description: Diverga help guide
version: "6.9.0"
---
```

**Why this happened**: The `version` field wasn't documented as required until we discovered it through trial and error.

### Issue 2: Marketplace Cache Lag

**Symptom**: `/plugin install diverga` pulls old version without fixes

**Cause**: GitHub marketplace cache doesn't update immediately after push

**Timeline**:
1. We pushed fix to GitHub (commit `efc024a`)
2. User ran `/plugin install diverga`
3. Marketplace pulled OLDER cached version (`08b1ebb`)
4. Old version didn't have `version` field
5. Skills failed to load

**Solution**: Click "Update marketplace" before installing, or wait ~10 minutes after push

### Issue 3: Two Skill Loading Mechanisms

Claude Code has **two separate** skill loading systems:

| Mechanism | Command Format | Source | Reliability |
|-----------|----------------|--------|-------------|
| **Plugin Skills** | `/diverga:help` (colon) | `~/.claude/plugins/cache/` | Depends on marketplace |
| **Local Skills** | `/diverga-help` (hyphen) | `~/.claude/skills/` | High (symlinks) |

**Confusion**: Users expect both formats to work the same way, but they use completely different loading paths.

---

## Complete Debugging Timeline

### Phase 1: Initial Investigation (2+ hours)

1. **Observed**: `/diverga:help` returns "Unknown skill"
2. **Checked**: Plugin is registered in `installed_plugins.json` ✅
3. **Checked**: `~/.claude/plugins/cache/diverga/` exists ✅
4. **Checked**: `skills/` directory has 51 skills ✅
5. **Compared**: oh-my-claudecode (works) vs Diverga (doesn't)
6. **Finding**: Both have identical structure

### Phase 2: SKILL.md Format Discovery (1 hour)

1. **Compared**: SKILL.md files between OMC and Diverga
2. **Finding**: OMC has only `name`, `description` - Diverga same
3. **Hypothesis**: Maybe `version` field is needed?
4. **Test**: Added `version: "6.9.0"` to all 51 SKILL.md files
5. **Result**: Still didn't work after restart

### Phase 3: Symlink Workaround (1 hour)

1. **Discovery**: Local skills (`~/.claude/skills/`) use different loader
2. **Created**: 51 symlinks: `diverga-xxx` → plugin cache
3. **Result**: `/diverga-help` (hyphen) works!
4. **But**: `/diverga:help` (colon) still fails

### Phase 4: Cache Investigation (1 hour)

1. **Removed**: Diverga from `installed_plugins.json`
2. **Deleted**: `~/.claude/plugins/cache/diverga/`
3. **Reinstalled**: Via `/plugin install diverga`
4. **Result**: Plugin shows installed, skills listed
5. **But**: Still "Unknown skill" on invocation

### Phase 5: Root Cause Found (30 min)

1. **Checked**: Plugin cache SKILL.md files
2. **Finding**: `version` field MISSING in cache!
3. **Compared**: Source repo has `version`, cache doesn't
4. **Root cause**: Marketplace pulled OLD cached version
5. **Solution**: Manually copy latest skills to cache

---

## Solutions

### Solution A: Wait and Reinstall (Recommended)

```bash
# Wait 10-15 minutes after pushing changes to GitHub
# Then in Claude Code:
/plugin → Marketplaces → Update marketplace
/plugin → Installed → diverga → Uninstall
/plugin → Marketplaces → diverga → Install
# Restart Claude Code
```

### Solution B: Manual Cache Update

```bash
# If you have the source repo locally:
cd /path/to/Diverga
cp -R skills/* ~/.claude/plugins/cache/diverga/diverga/*/skills/

# Restart Claude Code
```

### Solution C: Use Local Symlinks (Most Reliable)

```bash
# Create symlinks for hyphen-prefix access
cd /path/to/Diverga
for skill_dir in skills/*/; do
  skill_name=$(basename "$skill_dir")
  ln -sf "$(pwd)/$skill_dir" ~/.claude/skills/diverga-${skill_name}
done

# Restart Claude Code
# Use: /diverga-help (hyphen) instead of /diverga:help (colon)
```

---

## Diagnostic Commands

### Check Plugin Registration

```bash
cat ~/.claude/plugins/installed_plugins.json | jq '.plugins["diverga@diverga"]'
```

Expected output:
```json
[{
  "scope": "user",
  "installPath": "/Users/xxx/.claude/plugins/cache/diverga/diverga/6.9.0",
  "version": "6.9.0",
  "gitCommitSha": "..."
}]
```

### Check SKILL.md Format

```bash
head -10 ~/.claude/plugins/cache/diverga/diverga/*/skills/help/SKILL.md
```

**Must have `version` field:**
```yaml
---
name: help
description: ...
version: "6.9.0"    # ← REQUIRED!
---
```

### Check Symlinks

```bash
ls -la ~/.claude/skills/ | grep diverga
```

### Verify Symlink Targets

```bash
for link in ~/.claude/skills/diverga-*; do
  target=$(readlink "$link")
  [[ -d "$target" ]] && echo "✅ $link" || echo "❌ $link (broken)"
done
```

---

## Comparison: Working vs Non-Working

| Component | oh-my-claudecode (Works) | Diverga (Fixed) |
|-----------|-------------------------|-----------------|
| `plugin.json` | ✅ name, version, description, skills | ✅ Same |
| `marketplace.json` | ✅ Standard format | ✅ Same |
| SKILL.md fields | name, description | name, description, **version** |
| Skills count | 35 | 51 |
| Colon prefix | ✅ Works | ✅ Works (after fix) |
| Hyphen prefix | N/A | ✅ Works (via symlinks) |

---

## SKILL.md Format Reference

### Required Fields

```yaml
---
name: skill-name          # Must match directory name
description: |            # Can be multiline
  Brief description.
  Include triggers here.
version: "1.0.0"          # REQUIRED - semver format
---
```

### NOT Supported (Will Break Parsing)

```yaml
---
name: skill-name
command: /plugin:skill    # ❌ Breaks parsing
category: system          # ❌ Not supported
model_tier: medium        # ❌ Not supported
triggers:                 # ❌ Not supported as array
  - keyword1
---
```

---

## Prevention Checklist

For plugin developers:

- [ ] All SKILL.md files have `name`, `description`, `version` fields
- [ ] `version` follows semver format (e.g., "1.0.0")
- [ ] No unsupported fields in frontmatter
- [ ] Test with fresh install after GitHub push
- [ ] Wait for marketplace cache to update (~10-15 min)

---

## FAQ

### Q: Why does OMC work without `version` field?

OMC's SKILL.md files also lack `version` field, but it was installed at a different time when the caching behavior may have been different. The safest approach is to always include `version`.

### Q: Why use hyphen vs colon prefix?

| Format | System | Use When |
|--------|--------|----------|
| `/diverga:help` | Plugin loader | Plugin is properly installed and cached |
| `/diverga-help` | Local skills | Want guaranteed reliability via symlinks |

### Q: How do I know which version is cached?

```bash
cat ~/.claude/plugins/installed_plugins.json | jq '.plugins["diverga@diverga"][0].gitCommitSha'
```

Compare with your repo's latest commit: `git rev-parse HEAD`

---

## Getting Help

If issues persist after following this guide:

1. **Check Claude Code version**: `v2.1.15` or newer recommended
2. **Clear all caches**:
   ```bash
   rm -rf ~/.claude/plugins/cache/diverga/
   rm ~/.claude/skills/diverga-*
   ```
3. **Report issue**: https://github.com/HosungYou/Diverga/issues

Include:
- Claude Code version
- OS and version
- Output of diagnostic commands
- Screenshots of error messages

---

## Version History

- **v6.9.2**: Fixed marketplace cache issue, comprehensive troubleshooting guide
- **v6.9.1**: Added `version` field to all SKILL.md files
- **v6.9.0**: Initial plugin marketplace release
