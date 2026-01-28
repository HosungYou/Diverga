# Diverga Troubleshooting Guide

Common issues and solutions for all platforms.

---

## 🔴 Critical Issues

### `require is not defined` (Codex CLI)

**Symptom:**
```
ReferenceError: require is not defined in ES module scope
```

**Cause:** Node.js treats `.js` files as ESM when `package.json` has `"type": "module"`

**Solution:**
```bash
# Use the .cjs file instead
node ~/.codex/diverga/.codex/diverga-codex.cjs setup

# Or reinstall
curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-codex.sh | bash
```

---

### `Cannot find module` (OpenCode)

**Symptom:**
```
Error: Cannot find module './agents'
```

**Cause:** TypeScript not compiled

**Solution:**
```bash
cd ~/.opencode/plugins/diverga
npm install
npm run build
```

---

### Plugin Not Found (Claude Code)

**Symptom:**
```
Plugin 'diverga' not found
```

**Solution:**
```bash
# Re-add to marketplace
/plugin marketplace add https://github.com/HosungYou/Diverga

# Re-install
/plugin install diverga

# Verify
/plugin list
```

---

## ⚠️ Platform-Specific Issues

### Codex CLI

| Issue | Cause | Solution |
|-------|-------|----------|
| `AGENTS.md not found` | Wrong directory | `cd ~/.codex/diverga` then run setup |
| Agent not triggering | Keywords not detected | Use explicit keywords like "research question" |
| Slow startup | Large AGENTS.md | Normal - loads on first use |

### OpenCode

| Issue | Cause | Solution |
|-------|-------|----------|
| TypeScript errors | Missing types | `npm install` in plugin directory |
| Build fails | Node version | Requires Node.js 18+ |
| Hooks not firing | Plugin not loaded | Check `oh-my-opencode.json` config |

### Claude Code

| Issue | Cause | Solution |
|-------|-------|----------|
| Skill not available | Not installed | `/plugin install diverga` |
| Agent loop | Checkpoint bypass | Restart session |
| Context lost | Session timeout | Use `/diverga:setup` to reinitialize |

---

## 🔧 General Solutions

### Reset Installation

**Codex CLI:**
```bash
rm -rf ~/.codex/diverga
curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-codex.sh | bash
```

**OpenCode:**
```bash
rm -rf ~/.opencode/plugins/diverga
curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-opencode.sh | bash
```

**Claude Code:**
```bash
/plugin uninstall diverga
/plugin install diverga
```

### Check Installation

**Codex CLI:**
```bash
node ~/.codex/diverga/.codex/diverga-codex.cjs setup
```

**OpenCode:**
```bash
ls -la ~/.opencode/plugins/diverga/
```

**Claude Code:**
```bash
/plugin list
```

### Update to Latest Version

**All Platforms:**
```bash
# Universal installer handles updates
curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install.sh | bash
```

---

## 🐛 Node.js Version Issues

### Minimum Version

Diverga requires **Node.js 18+**

**Check version:**
```bash
node --version
```

**If version is too old:**
```bash
# Using nvm
nvm install 18
nvm use 18

# Or update Node.js directly
# macOS: brew upgrade node
# Linux: See https://nodejs.org/
```

### ESM vs CommonJS

Diverga uses ESM for the main package but provides CommonJS compatibility:

| File | Type | Usage |
|------|------|-------|
| `diverga-codex.cjs` | CommonJS | Codex CLI (recommended) |
| `diverga-codex.js` | ESM | Not recommended |
| `*.ts` → `dist/*.js` | ESM | OpenCode (compiled) |

---

## 📊 Diagnostic Commands

### Check System

```bash
# Node.js version
node --version

# npm version
npm --version

# Git version
git --version

# Check if platforms exist
ls -la ~/.codex 2>/dev/null || echo "Codex not found"
ls -la ~/.opencode 2>/dev/null || echo "OpenCode not found"
ls -la ~/.claude 2>/dev/null || echo "Claude Code not found"
```

### Test Codex Plugin

```bash
# Full diagnostic
node ~/.codex/diverga/.codex/diverga-codex.cjs setup

# Test specific commands
node ~/.codex/diverga/.codex/diverga-codex.cjs list
node ~/.codex/diverga/.codex/diverga-codex.cjs agent A1
node ~/.codex/diverga/.codex/diverga-codex.cjs tscore
```

### Test OpenCode Plugin

```bash
# Check build
ls -la ~/.opencode/plugins/diverga/dist/

# Check types
cd ~/.opencode/plugins/diverga && npm run typecheck
```

---

## 🆘 Getting Help

### Before Reporting

1. **Check this guide** for common solutions
2. **Update to latest version** using install scripts
3. **Try a clean reinstall** if problems persist

### Report an Issue

Include the following information:

```
Platform: [Codex CLI / OpenCode / Claude Code]
OS: [macOS / Linux / Windows]
Node.js: [version]
Diverga: [version]

Steps to reproduce:
1. ...
2. ...

Expected behavior:
...

Actual behavior:
...

Error message (if any):
...
```

**Report at:** https://github.com/HosungYou/Diverga/issues

---

## 📚 Related Documentation

- [Quick Start](QUICKSTART.md)
- [Cross-Platform Guide](DESIGN_SYSTEM.md)
- [Full Documentation](../CLAUDE.md)

---

*Diverga v6.6.1 - Where creativity meets rigor*
