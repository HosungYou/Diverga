# Diverga v6.9.2 Release Notes

**Release Date**: 2026-02-03
**Type**: Critical Bug Fix
**Debugging Time**: 6+ hours

---

## Summary

This release fixes the **marketplace cache synchronization issue** that caused "Unknown skill" errors even when Diverga appeared as properly installed in Claude Code.

---

## The Problem

Users experienced this confusing situation:

```
❯ /plugin install diverga
(no content)

❯ /plugin
→ Shows "Installed" tab with diverga @ diverga
→ Lists all 51 skills!

❯ /diverga:help
Unknown skill: diverga:help

❯ /diverga-help
Unknown skill: diverga-help
```

**Plugin appeared installed with skills listed, but all skill invocations failed.**

---

## Root Causes Identified

After extensive debugging, we discovered **three interconnected issues**:

### 1. Marketplace Cache Lag (PRIMARY)

| What Happened | Why |
|---------------|-----|
| User ran `/plugin install diverga` | Expected behavior |
| Marketplace pulled OLD cached version | Cache lag after GitHub push |
| Old version missing `version` field | Causes skill load failure |
| Skills show in list but won't invoke | Partial parsing succeeded |

**The Smoking Gun**: Plugin cache had commit `08b1ebb` (old) instead of `efc024a` (fixed)

### 2. Missing `version` Field in SKILL.md

Claude Code requires this format:
```yaml
---
name: help
description: Diverga help guide
version: "6.9.0"    # ← REQUIRED!
---
```

Without `version`, skills appear in the list but fail to load properly.

### 3. Two Separate Skill Loading Systems

| System | Command | Source Directory |
|--------|---------|------------------|
| Plugin Loader | `/diverga:help` (colon) | `~/.claude/plugins/cache/` |
| Local Loader | `/diverga-help` (hyphen) | `~/.claude/skills/` |

Users assumed both would work the same way - they don't!

---

## Complete Debugging Journey

### Phase 1: Initial Investigation (2+ hours)
- Verified plugin registration in `installed_plugins.json` ✅
- Checked cache directory structure ✅
- Compared with oh-my-claudecode (which works) ✅
- Both plugins have identical structure!

### Phase 2: SKILL.md Discovery (1 hour)
- Hypothesized `version` field might be required
- Added to all 51 SKILL.md files
- Still didn't work after restart

### Phase 3: Symlink Workaround (1 hour)
- Created symlinks in `~/.claude/skills/`
- `/diverga-help` (hyphen) started working!
- `/diverga:help` (colon) still failed

### Phase 4: Cache Mystery (1 hour)
- Removed plugin completely from JSON
- Deleted cache directory
- Fresh install via `/plugin install`
- Plugin shows installed... but skills still fail!

### Phase 5: Eureka Moment (30 min)
- Checked SKILL.md files IN THE CACHE
- **No `version` field!**
- Cache had OLD version before our fix
- Marketplace wasn't pulling latest from GitHub

---

## Changes in v6.9.2

### 1. Comprehensive Troubleshooting Guide

`docs/TROUBLESHOOTING-PLUGIN.md` now includes:
- Complete debugging timeline
- Three root causes explained
- Multiple solution approaches
- Diagnostic commands
- SKILL.md format reference
- FAQ section

### 2. Enhanced Setup Wizard

`/diverga-setup` now automatically creates symlinks:
```bash
# During setup, creates 51 symlinks:
~/.claude/skills/diverga-help → skills/help/
~/.claude/skills/diverga-a1 → skills/a1/
# ... etc
```

### 3. GitHub Action Validation

`.github/workflows/validate-skills.yml`:
- Validates all SKILL.md have required fields
- Checks version follows semver
- Verifies skill count (51)
- Runs on push/PR to main

---

## Solutions

### Solution A: Update Marketplace (Recommended)

```
1. /plugin → Marketplaces → Update marketplace
2. /plugin → Installed → diverga → Uninstall
3. /plugin → Marketplaces → diverga → Install
4. Restart Claude Code
```

### Solution B: Manual Cache Update

```bash
cd /path/to/Diverga
cp -R skills/* ~/.claude/plugins/cache/diverga/diverga/*/skills/
# Restart Claude Code
```

### Solution C: Local Symlinks (Most Reliable)

```bash
cd /path/to/Diverga
for skill_dir in skills/*/; do
  skill_name=$(basename "$skill_dir")
  ln -sf "$(pwd)/$skill_dir" ~/.claude/skills/diverga-${skill_name}
done
# Restart Claude Code
# Use /diverga-help (hyphen) instead of /diverga:help (colon)
```

---

## Verification

After applying any solution:

```
/diverga:help     ✅ Should work (colon prefix)
/diverga-help     ✅ Should work (hyphen prefix)
/diverga-memory   ✅ Should work
/diverga-a1       ✅ Should work
```

---

## Key Learnings for Plugin Developers

1. **Always include `version` field** in SKILL.md frontmatter
2. **Wait for marketplace cache** (~10-15 min) after GitHub push
3. **Test fresh install** from marketplace, not local
4. **Document workarounds** for caching issues
5. **Provide diagnostic commands** for troubleshooting

---

## Files Changed

| File | Change |
|------|--------|
| `docs/TROUBLESHOOTING-PLUGIN.md` | Complete rewrite with debugging journey |
| `CHANGELOG.md` | Added v6.9.2 entry |
| `skills/setup/SKILL.md` | Added automatic symlink installation |
| `.github/workflows/validate-skills.yml` | Created for CI validation |

---

## Commits

```
97ffb99 docs: add deep investigation results to troubleshooting guide
6d79645 docs: add plugin troubleshooting guide for skill loading issues
05de44b feat: add symlink installation to setup wizard and SKILL.md validation CI
efc024a fix(plugin): add required version field and remove orphaned skill directories
```

---

## Acknowledgments

This debugging session took 6+ hours of investigation. Special thanks to:
- The oh-my-claudecode plugin for providing a working reference
- Claude Code's plugin system documentation (where it exists)
- Trial and error methodology

---

## Links

- **GitHub**: https://github.com/HosungYou/Diverga
- **Troubleshooting Guide**: docs/TROUBLESHOOTING-PLUGIN.md
- **Previous Release**: docs/releases/RELEASE_v6.9.1.md
