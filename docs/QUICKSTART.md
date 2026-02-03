# Diverga Quick Start Guide

Get Diverga running in under 5 minutes on any platform.

---

## 🚀 One-Line Installation

### Auto-Detect (Recommended)

Automatically detects and installs for all available platforms:

```bash
curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install.sh | bash
```

### Platform-Specific

| Platform | Command |
|----------|---------|
| **Codex CLI** | `curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-codex.sh \| bash` |
| **OpenCode** | `curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-opencode.sh \| bash` |
| **Claude Code** | `/plugin marketplace add https://github.com/HosungYou/Diverga` |

---

## 📦 Claude Code (Recommended)

### Step 1: Add to Marketplace

```bash
/plugin marketplace add https://github.com/HosungYou/Diverga
```

### Step 2: Install

```bash
/plugin install diverga
```

### Step 3: Setup

```bash
/diverga:setup
```

### Step 4: Start Using

Just describe your research:

```
"I want to conduct a systematic review on AI in education"
"메타분석을 시작하고 싶어"
"Help me design an experimental study"
```

---

## 🤖 OpenAI Codex CLI

### Option A: One-Line Install

```bash
curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-codex.sh | bash
```

### Option B: Manual Install

```bash
# Clone repository
git clone https://github.com/HosungYou/Diverga.git ~/.codex/diverga

# Run setup
node ~/.codex/diverga/.codex/diverga-codex.cjs setup
```

### Usage

```bash
# List all 40 agents
node ~/.codex/diverga/.codex/diverga-codex.cjs list

# Get agent details
node ~/.codex/diverga/.codex/diverga-codex.cjs agent A1

# Show checkpoints
node ~/.codex/diverga/.codex/diverga-codex.cjs checkpoint

# Show T-Score reference
node ~/.codex/diverga/.codex/diverga-codex.cjs tscore

# VS Methodology explanation
node ~/.codex/diverga/.codex/diverga-codex.cjs vs
```

### ⚠️ Important: Enable AGENTS.md in Codex Sessions

For Diverga agents to work in Codex CLI sessions, you must configure AGENTS.md loading:

**Option 1: Project-level (Recommended)**

Create or edit `codex.json` in your project root:

```json
{
  "agents": ".codex/AGENTS.md"
}
```

**Option 2: Global Configuration**

Edit `~/.codex/config.json`:

```json
{
  "agents": "~/.codex/diverga/.codex/AGENTS.md"
}
```

**Option 3: Command-line Flag**

```bash
codex --agents-file .codex/AGENTS.md
```

### Verify Installation

```bash
# Check if AGENTS.md exists
cat ~/.codex/diverga/.codex/AGENTS.md | head -20

# Test in Codex CLI
codex "List all Diverga agents available"
```

### In Codex Sessions

Once configured, Diverga agents are triggered by keywords:

```
"Help me refine my research question"  → A1-research-question-refiner
"I need a theoretical framework"       → A2-theoretical-framework-architect
"Let's do a meta-analysis"             → C5-meta-analysis-master
```

---

## 💻 OpenCode

### Option A: One-Line Install

```bash
curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-opencode.sh | bash
```

### Option B: Manual Install

```bash
# Clone repository
git clone https://github.com/HosungYou/Diverga.git /tmp/diverga

# Build plugin
cd /tmp/diverga/.opencode/plugins/diverga
npm install
npm run build

# Install to OpenCode
mkdir -p ~/.opencode/plugins/diverga
cp -r dist/* ~/.opencode/plugins/diverga/
```

### Usage

```bash
# List agents
opencode "diverga:list"

# Get agent details
opencode "diverga:agent A1"

# Show checkpoints
opencode "diverga:checkpoint"
```

---

## ⚡ Quick Commands Reference

| Platform | List Agents | Agent Details | Checkpoints |
|----------|-------------|---------------|-------------|
| **Claude Code** | `/diverga:help` | `/diverga:A1-...` | `/diverga:checkpoint` |
| **Codex CLI** | `diverga-codex.cjs list` | `diverga-codex.cjs agent A1` | `diverga-codex.cjs checkpoint` |
| **OpenCode** | `diverga:list` | `diverga:agent A1` | `diverga:checkpoint` |

---

## 🎯 What's Next?

### 1. Explore Agents

Diverga has 40 specialized agents across 8 categories:

- **A: Foundation** (6) - Research questions, theory, ethics
- **B: Evidence** (5) - Literature, quality appraisal
- **C: Design** (7) - Quantitative, qualitative, mixed methods, meta-analysis
- **D: Data Collection** (4) - Sampling, interviews, observation
- **E: Analysis** (5) - Statistical, coding, integration
- **F: Quality** (5) - Consistency, checklists, bias
- **G: Communication** (6) - Journals, writing, peer review
- **H: Specialized** (2) - Ethnography, action research

### 2. Understand VS Methodology

Diverga uses **Verbalized Sampling (VS)** to prevent AI mode collapse:

- T-Score measures "typicality" of recommendations
- High T-Score (>0.7) = common/modal choice
- Low T-Score (<0.3) = creative/novel choice
- Human checkpoints enforce deliberate choice

### 3. Try a Workflow

**Meta-Analysis Example:**
```
"I want to conduct a meta-analysis on AI tutoring effects on learning outcomes"
```

Diverga will:
1. 🔴 CHECKPOINT: Confirm research direction
2. Activate C5-meta-analysis-master
3. Guide through PRISMA workflow
4. Present VS alternatives at each decision point

---

## 📚 More Documentation

- [Full Documentation (CLAUDE.md)](../CLAUDE.md)
- [All 40 Agents (AGENTS.md)](../AGENTS.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [VS Methodology](VS-METHODOLOGY.md)
- [Cross-Platform Guide](DESIGN_SYSTEM.md)

---

## ❓ Need Help?

- **Issues**: https://github.com/HosungYou/Diverga/issues
- **Documentation**: https://github.com/HosungYou/Diverga

---

*Diverga v6.6.2 - Where creativity meets rigor*
