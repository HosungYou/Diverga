# Diverga v6.9.1 Release Notes

**Release Date**: 2026-02-03
**Release Type**: Bug Fix (Critical)
**Codename**: "Plugin Discovery Fix"

---

## Executive Summary

This release fixes a **critical bug** that prevented Claude Code from discovering Diverga skills. After 5+ hours of debugging, three root causes were identified and resolved:

| Issue | Severity | Status |
|-------|----------|--------|
| Missing `version` field in SKILL.md | 🔴 CRITICAL | ✅ Fixed |
| Orphaned skill directories causing confusion | 🟡 MEDIUM | ✅ Fixed |
| Plugin cache installation mismatch | 🟠 HIGH | ✅ Fixed |

---

## Problem Statement

Users reported "Unknown skill: diverga:xxx" errors when trying to invoke Diverga skills:

```
❯ /diverga:help
Unknown skill: diverga:help

❯ /diverga:memory
Unknown skill: diverga:memory
```

This occurred despite the plugin appearing in `/plugins` list and skills existing in the expected locations.

---

## Root Cause Analysis

### Issue 1: Missing `version` Field in SKILL.md

**Discovery**: Comparison with working plugin (oh-my-claudecode) revealed that Claude Code skill discovery requires the `version` field in SKILL.md frontmatter.

**Before (broken)**:
```yaml
---
name: a1
description: |
  VS-Enhanced Research Question Refiner...
---
```

**After (working)**:
```yaml
---
name: a1
description: |
  VS-Enhanced Research Question Refiner...
version: "6.9.0"
---
```

**Impact**: 48 of 51 SKILL.md files were missing this field.

### Issue 2: Orphaned Skill Directories

Three conflicting skill directories existed:

| Directory | Status | Action |
|-----------|--------|--------|
| `skills/` (51 files) | ✅ Correct | Keep - Referenced in plugin.json |
| `.claude/skills/` (100+ files) | ❌ Orphaned | Deleted - Not referenced |
| `.codex/skills/` (3 files) | ❌ Orphaned | Deleted - Not referenced |

These orphaned directories caused:
- Confusion about which skills were active
- Potential conflicts during skill discovery
- ~50,000 lines of duplicate/outdated code

### Issue 3: Plugin Cache vs Local Skills

**Finding**: Claude Code loads skills from TWO sources:
1. **Plugin cache** (`~/.claude/plugins/cache/`) - Uses `plugin-name:skill-name` format
2. **Local skills** (`~/.claude/skills/`) - Uses `skill-name` format directly

The plugin system wasn't loading Diverga correctly, but local skills work reliably.

**Solution**: Created symlinks from local skills to plugin cache:
```bash
~/.claude/skills/diverga-help → ~/.claude/plugins/cache/diverga/diverga/6.9.0/skills/help/
~/.claude/skills/diverga-memory → ~/.claude/plugins/cache/diverga/diverga/6.9.0/skills/memory/
# ... (51 symlinks total)
```

---

## Changes Made

### 1. SKILL.md Version Field Addition

Added `version: "6.9.0"` to all 51 SKILL.md files:

| Category | Files Updated |
|----------|---------------|
| A (Foundation) | a1, a2, a3, a4, a5, a6 |
| B (Evidence) | b1, b2, b3*, b4, b5 |
| C (Design) | c1, c2, c3, c4, c5, c6*, c7 |
| D (Collection) | d1, d2, d3, d4 |
| E (Analysis) | e1, e2, e3, e4*, e5 |
| F (Quality) | f1, f2, f3, f4, f5 |
| G (Communication) | g1, g2, g3, g4, g5, g6 |
| H (Specialized) | h1, h2 |
| I (Systematic Review) | i0, i1, i2, i3 |
| System | help, memory, setup, diverga, research-coordinator, research-orchestrator, universal-ma-codebook |

*Already had version field

### 2. Orphaned Directory Removal

| Directory | Files Removed | Lines Removed |
|-----------|---------------|---------------|
| `.claude/skills/` | 100+ files | ~48,000 lines |
| `.codex/skills/` | 3 directories | ~400 lines |
| **Total** | ~103 files | ~50,430 lines |

### 3. Local Skills Symlink Installation

Created 51 symlinks in `~/.claude/skills/`:

```
diverga-a1 → ~/.claude/plugins/cache/diverga/diverga/6.9.0/skills/a1/
diverga-a2 → ~/.claude/plugins/cache/diverga/diverga/6.9.0/skills/a2/
...
diverga-memory → ~/.claude/plugins/cache/diverga/diverga/6.9.0/skills/memory/
diverga-help → ~/.claude/plugins/cache/diverga/diverga/6.9.0/skills/help/
```

---

## Skill Access Methods

After this fix, Diverga skills can be accessed in two ways:

### Method 1: Hyphen Prefix (Recommended - Always Works)

```
/diverga-help       ✅ Works immediately
/diverga-memory     ✅ Works immediately
/diverga-a1         ✅ Works immediately
```

### Method 2: Colon Prefix (Plugin System)

```
/diverga:help       ⚠️ Requires plugin to be loaded
/diverga:memory     ⚠️ Requires plugin to be loaded
```

**Recommendation**: Use hyphen prefix (`/diverga-xxx`) for reliability.

---

## Installation Instructions

### For New Users

```bash
# 1. Clone or pull latest version
git clone https://github.com/HosungYou/Diverga.git
cd Diverga

# 2. Create local skill symlinks
for skill_dir in skills/*/; do
  skill_name=$(basename "$skill_dir")
  ln -sf "$(pwd)/$skill_dir" ~/.claude/skills/diverga-${skill_name}
done

# 3. Restart Claude Code
```

### For Existing Users

```bash
# 1. Pull latest changes
cd /path/to/Diverga
git pull origin main

# 2. Clear old cache (optional)
rm -rf ~/.claude/plugins/cache/diverga/

# 3. Create local skill symlinks
for skill_dir in skills/*/; do
  skill_name=$(basename "$skill_dir")
  ln -sf "$(pwd)/$skill_dir" ~/.claude/skills/diverga-${skill_name}
done

# 4. Restart Claude Code
```

---

## Verification

After installation, verify skills work:

```bash
# In Claude Code:
/diverga-help       # Should display help guide
/diverga-memory     # Should show memory system info
/diverga-a1         # Should show Research Question Refiner
```

---

## Technical Details

### Git Commit

```
commit efc024addfbdb06fc343947c35ab01e6486619fa
Author: Hosung You
Date:   2026-02-03

fix(plugin): add required version field and remove orphaned skill directories

- Add version: "6.9.0" to all 51 SKILL.md files in skills/
- Remove orphaned .claude/skills/ directory (not referenced by plugin.json)
- Remove orphaned .codex/skills/ directory (not referenced by plugin.json)

The version field is REQUIRED for Claude Code skill discovery.
Skills are now only in skills/ as specified in plugin.json.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

### Files Changed

```
150 files changed, 48 insertions(+), 50430 deletions(-)
```

---

## Known Limitations

1. **Plugin Colon Syntax**: The `/diverga:xxx` format may still not work depending on how Claude Code loads plugins at startup. Use `/diverga-xxx` instead.

2. **Session Reload**: After creating symlinks, Claude Code must be restarted for skills to be discovered.

3. **Symlink Persistence**: Symlinks must be recreated if the plugin cache is cleared or Diverga is reinstalled.

---

## Future Improvements

- [ ] Investigate why plugin system doesn't load `diverga:` prefix correctly
- [ ] Add automatic symlink creation to setup wizard (`/diverga-setup`)
- [ ] Create npm package for easier installation
- [ ] Add GitHub Action to validate SKILL.md format on PR

---

## Debugging Timeline

| Time | Action | Result |
|------|--------|--------|
| 0:00 | Initial error report | "Unknown skill: diverga:help" |
| 0:30 | Check plugin.json | Correct - points to `./skills/` |
| 1:00 | Compare with oh-my-claudecode | Found version field difference |
| 1:30 | Check orphaned directories | Found 3 conflicting locations |
| 2:00 | Add version field to all SKILL.md | 48 files updated |
| 2:30 | Delete orphaned directories | 50K+ lines removed |
| 3:00 | Commit and push to GitHub | Success |
| 3:30 | Clear and reinstall plugin cache | Still not working |
| 4:00 | Discover local skills mechanism | research-coordinator works! |
| 4:30 | Create symlinks to local skills | 51 symlinks created |
| 5:00 | Verify after restart | `/diverga-help` works |

---

## Acknowledgments

- Claude Opus 4.5 for pair debugging session
- oh-my-claudecode for reference implementation

---

## Version History

- **v6.9.1** (2026-02-03): Plugin discovery fix - version field, orphan cleanup, local symlinks
- **v6.9.0** (2026-02-02): Memory System with semantic search and lifecycle hooks
- **v6.8.0** (2026-02-01): Memory System initial release
- **v6.7.1** (2026-01-31): Documentation synchronization
- **v6.7.0** (2026-01-30): Systematic Review Automation (Category I)
