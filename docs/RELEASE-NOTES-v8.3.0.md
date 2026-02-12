# Diverga v8.3.0 Release Notes

**Release Date**: 2026-02-12
**Code Name**: Cross-Platform Migration
**Previous Version**: v8.2.0

---

## Overview

Diverga v8.3.0 is the **Cross-Platform Migration** release, bringing full Codex CLI and OpenCode support up to parity with the Claude Code v8.2.0 feature set. This release introduces 47 individual skill files for Codex CLI, updates model routing to the latest GPT-5.3-Codex models, and includes comprehensive cross-platform documentation.

### Key Highlights

- **47 individual SKILL.md files** for Codex CLI (44 agents + 3 utilities)
- **GPT-5.3-Codex model routing** across all tiers (HIGH/MEDIUM/LOW)
- **44 total agents** (Category I: ScholaRAG agents added)
- **Cross-platform compatibility improved**: Codex CLI ~40% → ~75%, OpenCode ~20% → ~70%
- **No breaking changes** for Claude Code users

---

## Platform Compatibility Matrix

| Platform | v8.2.0 Support | v8.3.0 Support | Improvement |
|----------|----------------|----------------|-------------|
| **Claude Code** | 100% | 100% | - |
| **Codex CLI** | ~40% | **~75%** | +35% |
| **OpenCode** | ~20% | **~70%** | +50% |

---

## What's New

### 1. Codex CLI Individual Skill Files

**47 individual SKILL.md files** created for granular skill invocation:

```
.codex/skills/
├── diverga-a1-theorymapper/
│   └── SKILL.md
├── diverga-a2-hypothesisarchitect/
│   └── SKILL.md
...
├── diverga-i3-qualityauditor/
│   └── SKILL.md
├── diverga-setup/
│   └── SKILL.md
├── diverga-memory/
│   └── SKILL.md
└── diverga-help/
    └── SKILL.md
```

**What's Included:**
- ✅ 44 agent skills (A1-A5, B1-B5, C1-C6, D1-D4, E1-E5, F1-F5, G1-G6, H1-H4, I0-I3)
- ✅ 3 utility skills (setup, memory, help)
- ✅ Proper YAML frontmatter (name, description <500 chars, metadata)
- ✅ Codex CLI Degraded Mode instructions
- ✅ Text-based checkpoint protocol (replaces MCP runtime)
- ✅ Tool mapping tables (Claude Code → Codex CLI)
- ✅ Bilingual triggers (English + Korean)

**Previous State**: Only 3 bundled skills (research-coordinator, meta-analysis, checkpoint-system)

**Impact**: Enables fine-grained agent invocation like `/diverga-a1-theorymapper`, `/diverga-c4-metaanalyst` in Codex CLI.

---

### 2. GPT-5.3-Codex Model Routing

Updated all 47 skill files, CLI tools, and templates to use the latest OpenAI agentic coding models:

| Tier | v8.2.0 Model | v8.3.0 Model | Use Case |
|------|--------------|--------------|----------|
| **HIGH** | o3 | **gpt-5.3-codex** | Complex reasoning, architecture, planning |
| **MEDIUM** | gpt-4.1 | **gpt-5.2-codex** | Feature implementation, analysis |
| **LOW** | gpt-4.1-mini | **gpt-5.1-codex-mini** | Quick lookups, simple tasks |

**Why GPT-5.3-Codex?**
- Most capable agentic coding model in OpenAI's lineup
- Superior long-context retrieval (1M token context)
- Enhanced code generation and review capabilities
- Adaptive reasoning mode

**Files Updated**: All 47 SKILL.md files, `diverga-codex.cjs`, `AGENTS.md.template`, `oh-my-opencode.template.json`

---

### 3. AGENTS.md.template v8.3.0 Rewrite

**Major Enhancements:**

#### A. 40 → 44 Agents (Category I Added)

**New Category I: ScholaRAG Integration**

| Agent | Purpose | Checkpoint |
|-------|---------|------------|
| **I0-ScholarAgentOrchestrator** | Pipeline coordination and stage management | - |
| **I1-paper-retrieval-agent** | Database fetching (Semantic Scholar, OpenAlex, arXiv) | 🔴 SCH_DATABASE_SELECTION |
| **I2-screening-assistant** | PRISMA 2020 screening with configurable LLM | 🔴 SCH_SCREENING_CRITERIA |
| **I3-quality-auditor** | PRISMA compliance validation | 🔵 SCH_QUALITY_GATES |

**Auto-Trigger Keywords:**
- English: "systematic review", "PRISMA", "ScholaRAG", "literature review automation"
- Korean: "체계적 문헌고찰", "프리즈마", "스콜라랙", "문헌고찰 자동화"

#### B. Full Agent Prerequisite Map

Visual dependency graph showing which checkpoints each agent requires:

```
Level 0 (No prerequisites):
  A1-TheoryMapper, A2-HypothesisArchitect, B1-LiteratureScout, E5-KoreanLanguageAdvisor, I0-ScholarAgentOrchestrator

Level 1 (Requires Level 0):
  A3-VariableDesigner [REQ_HYPOTHESIS], C1-SampleCalculator [REQ_HYPOTHESIS]

Level 2 (Requires Level 1):
  C2-StatisticalAdvisor [REQ_VARIABLES, REQ_SAMPLE_SIZE]

...

Level 5 (Final Stage):
  E4-PeerResponseDrafter [OPT_PUBLICATION_READY, OPT_PEER_FEEDBACK]
```

#### C. Checkpoint Dependency Order

Detailed checkpoint hierarchy from Level 0 through Level 5:

- **Level 0**: Foundation checkpoints (THEORY_SELECTED, RESEARCH_QUESTION, DATABASE_SELECTED)
- **Level 1**: Design checkpoints (HYPOTHESIS, METHOD_CHOSEN, LITERATURE_MAPPED)
- **Level 2**: Analysis checkpoints (VARIABLES, SAMPLE_SIZE, CITATION_MAP)
- **Level 3**: Validation checkpoints (EVIDENCE_SYNTHESIZED, EFFECT_SIZE, STATISTICAL_PLAN)
- **Level 4**: Quality checkpoints (BIAS_CHECK, VALIDITY_CHECK, QUALITY_ASSURANCE)
- **Level 5**: Publication checkpoints (PUBLICATION_READY, PRISMA_COMPLIANT)

#### D. SCH_* Checkpoints for Systematic Reviews

New checkpoint family for ScholaRAG automation:

| Checkpoint | Trigger Agent | Description |
|------------|---------------|-------------|
| 🔴 SCH_DATABASE_SELECTION | I1 | Database APIs validated |
| 🔴 SCH_SCREENING_CRITERIA | I2 | Inclusion/exclusion criteria defined |
| 🟠 SCH_RAG_READINESS | I3 | PDF collection complete, embeddings ready |
| 🔵 SCH_QUALITY_GATES | I3 | PRISMA compliance validated |

#### E. Memory System Reference

Documents `.research/` directory structure for persistent project state:

```
.research/
├── checkpoints.json        # Checkpoint state
├── metadata.json          # Project metadata
├── conversations/         # Session logs
├── agents/               # Agent outputs
└── plans/               # Research plans
```

---

### 4. OpenCode Integration Update

**oh-my-opencode.template.json v8.3.0:**

- ✅ I0-I3 triggers with English + Korean keywords
- ✅ Model routing includes all 44 agents
- ✅ SCH_* checkpoints in required/recommended sections
- ✅ Category I: ScholaRAG Integration section

**Example Trigger Configuration:**

```json
{
  "triggers": {
    "i0-scholeragentorchestrator": {
      "en": ["systematic review", "PRISMA", "ScholaRAG"],
      "ko": ["체계적 문헌고찰", "프리즈마", "스콜라랙"]
    }
  }
}
```

---

### 5. CLI Tool Updates

#### A. diverga-codex.cjs v6.6.1 → v8.3.0

**Changes:**

- **44 agents** (was 40), **9 categories** (was 8)
- **New command**: `diverga prereq` showing Agent Prerequisite Map
- **SCH_* checkpoints** added to checkpoint list
- **Fixed agent tier assignments**:
  - A3-VariableDesigner: MEDIUM → **HIGH**
  - B5-DivergenceAnalyst: MEDIUM → **HIGH**
  - F5-OpenScienceAdvocate: MEDIUM → **LOW**
  - G6-EquityGuard: MEDIUM → **HIGH**

**Example Usage:**

```bash
# Show agent prerequisites
diverga prereq

# Launch specific agent
diverga agent C4-MetaAnalyst --tier HIGH

# List all 44 agents
diverga list --category all
```

#### B. install-multi-cli.sh v6.6.2 → v8.3.0

**Enhancements:**

- ✅ Copies individual `.codex/skills/` directories
- ✅ `.research/` directory initialization
- ✅ Node.js >= 18 version check
- ✅ Post-install verification script
- ✅ Platform-specific install modes (`--codex`, `--opencode`, `--all`)

**Installation Command:**

```bash
# All platforms
curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-multi-cli.sh | bash

# Codex CLI only
curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-multi-cli.sh | bash -s -- --codex

# OpenCode only
curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-multi-cli.sh | bash -s -- --opencode
```

---

### 6. New Documentation

#### A. docs/CROSS-PLATFORM-GUIDE.md (NEW)

Unified guide comparing all three platforms:

| Section | Content |
|---------|---------|
| Feature Matrix | Side-by-side comparison (Claude Code vs Codex CLI vs OpenCode) |
| Installation | Platform-specific setup instructions |
| Usage Patterns | Skill invocation syntax for each platform |
| Limitations | Known gaps and workarounds |
| Migration | Moving projects between platforms |

**Target Audience**: Researchers switching between platforms or evaluating options.

#### B. docs/PLATFORM-LIMITATIONS.md (NEW)

Detailed limitation specifications with workarounds and quality ratings:

| Feature | Claude Code | Codex CLI | OpenCode | Workaround Quality |
|---------|-------------|-----------|----------|-------------------|
| Parallel Agents | ✅ Yes | ❌ No | ❌ No | ⭐⭐ (sequential fallback) |
| MCP Runtime | ✅ Yes | ❌ No | ❌ No | ⭐⭐⭐ (text protocol) |
| AskUserQuestion | ✅ Yes | ❌ No | ❌ No | ⭐⭐ (text prompts) |
| HUD Statusline | ✅ Yes | ❌ No | ❌ No | ⭐ (no alternative) |
| Per-Agent Models | ✅ Yes | ❌ No | ❌ No | ⭐ (session-level only) |

**Quality Ratings:**
- ⭐⭐⭐ = Full parity
- ⭐⭐ = Functional but degraded
- ⭐ = Significant limitation

---

### 7. Updated Documentation

#### A. docs/CODEX-SKILL-SYSTEM.md v6.6.2 → v8.3.0

- Individual skill file structure documented
- GPT-5.3-Codex model routing
- Degraded mode instructions
- Text-based checkpoint protocol

#### B. adapters/README.md

- Cross-platform compatibility table
- Platform-specific limitations
- Installation instructions for all platforms

#### C. CLAUDE.md

- Research Coordinator v8.3.0 integration
- Category I: ScholaRAG Integration section
- Auto-trigger rules updated for 44 agents

---

## Migration from v8.2.0

### Breaking Changes

**None.** v8.3.0 is fully backward compatible with v8.2.0 for Claude Code users.

### Recommended Actions

#### For Claude Code Users

1. **Update AGENTS.md** (optional but recommended):
   ```bash
   cd /your/project
   cp /Volumes/External\ SSD/Projects/Diverga/AGENTS.md.template AGENTS.md
   ```

2. **No code changes required** - existing checkpoints and agent triggers remain compatible.

#### For Codex CLI Users (NEW)

1. **Install individual skills**:
   ```bash
   curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-multi-cli.sh | bash -s -- --codex
   ```

2. **Invoke skills by name**:
   ```bash
   /diverga-c4-metaanalyst
   /diverga-a1-theorymapper
   ```

3. **Check agent prerequisites**:
   ```bash
   diverga prereq
   ```

#### For OpenCode Users (NEW)

1. **Install configuration**:
   ```bash
   curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-multi-cli.sh | bash -s -- --opencode
   ```

2. **Update oh-my-opencode.json**:
   ```bash
   cp /Volumes/External\ SSD/Projects/Diverga/adapters/oh-my-opencode/oh-my-opencode.template.json ~/.config/oh-my-opencode.json
   ```

---

## File Inventory

### New Files (49 total)

| Category | Count | Path |
|----------|-------|------|
| Codex Skills | 47 | `.codex/skills/diverga-*/SKILL.md` |
| Documentation | 2 | `docs/CROSS-PLATFORM-GUIDE.md`, `docs/PLATFORM-LIMITATIONS.md` |

### Updated Files (8 total)

| File | v8.2.0 | v8.3.0 | Changes |
|------|--------|--------|---------|
| `AGENTS.md.template` | v8.2.0 | v8.3.0 | +4 agents (I0-I3), prerequisite map, SCH_* checkpoints |
| `diverga-codex.cjs` | v6.6.1 | v8.3.0 | 44 agents, `prereq` command, tier fixes |
| `install-multi-cli.sh` | v6.6.2 | v8.3.0 | .codex/skills/ copy, .research/ init, version check |
| `oh-my-opencode.template.json` | v8.2.0 | v8.3.0 | I0-I3 triggers, SCH_* checkpoints |
| `docs/CODEX-SKILL-SYSTEM.md` | v6.6.2 | v8.3.0 | Individual skills, GPT-5.3-Codex |
| `adapters/README.md` | v8.2.0 | v8.3.0 | Cross-platform table |
| `CLAUDE.md` | v8.2.0 | v8.3.0 | Category I integration |
| `claude-settings/settings.json` | v8.2.0 | v8.3.0 | Model routing update |

**Total Files Modified**: 57+

---

## Known Limitations

### Codex CLI / OpenCode

These platforms have the following limitations compared to Claude Code:

| Feature | Status | Impact | Workaround |
|---------|--------|--------|------------|
| **Parallel Agent Execution** | ❌ Not Available | Slower multi-agent workflows | Sequential execution (⭐⭐) |
| **MCP Runtime Checkpoints** | ❌ Not Available | No programmatic state validation | Text-based behavioral protocol (⭐⭐⭐) |
| **AskUserQuestion UI** | ❌ Not Available | Less structured user input | Text prompts (⭐⭐) |
| **HUD Statusline** | ❌ Not Available | No visual progress tracking | None (⭐) |
| **Per-Agent Model Isolation** | ❌ Not Available | All agents use session model | Session-level model selection (⭐) |

**Quality Rating Legend:**
- ⭐⭐⭐ = Full parity with Claude Code
- ⭐⭐ = Functional but degraded experience
- ⭐ = Significant limitation, minimal workaround

---

## Installation

### All Platforms (Recommended)

```bash
curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-multi-cli.sh | bash
```

### Platform-Specific

```bash
# Codex CLI only
curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-multi-cli.sh | bash -s -- --codex

# OpenCode only
curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-multi-cli.sh | bash -s -- --opencode

# Claude Code only (default)
curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-multi-cli.sh | bash -s -- --claude
```

### Verification

After installation, verify:

```bash
# Check CLI tool
diverga --version
# Expected: v8.3.0

# List all agents
diverga list
# Expected: 44 agents across 9 categories

# Check skills (Codex CLI)
ls ~/.codex/skills/diverga-*
# Expected: 47 directories
```

---

## What's Next: v9.0 Roadmap

### Planned Features

1. **MCP Server for Codex CLI** (pending OpenAI MCP support)
   - Programmatic checkpoint validation
   - Structured user input forms
   - Real-time progress tracking

2. **Codex Cloud Integration**
   - Shared .research/ state across sessions
   - Multi-researcher collaboration
   - Persistent agent memory

3. **Automated Platform Testing**
   - CI/CD pipeline for all 3 platforms
   - Regression tests for 44 agents
   - Cross-platform parity validation

4. **Agent Performance Profiling**
   - Benchmark response quality across models
   - Cost analysis (GPT-5.3-Codex vs Claude Opus 4.6)
   - Optimal model tier recommendations

### Community Contributions

We welcome contributions in these areas:
- Additional platform adapters (Cursor, Continue, etc.)
- Agent skill improvements
- Checkpoint protocol enhancements
- Documentation translations

---

## Support

### Getting Help

- **Documentation**: [docs/CROSS-PLATFORM-GUIDE.md](./CROSS-PLATFORM-GUIDE.md)
- **Issues**: GitHub Issues (https://github.com/HosungYou/Diverga/issues)
- **Discussions**: GitHub Discussions

### Reporting Bugs

When reporting bugs, please include:
1. Platform (Claude Code / Codex CLI / OpenCode)
2. Diverga version (`diverga --version`)
3. Agent being used (e.g., C4-MetaAnalyst)
4. Checkpoint state (if applicable)
5. Error messages or unexpected behavior

---

## Acknowledgments

Special thanks to:
- OpenAI team for GPT-5.3-Codex agentic models
- Claude Code team for MCP runtime and agent framework
- Codex CLI and OpenCode communities for cross-platform testing
- Social science researchers providing feedback on agent workflows

---

**Full Changelog**: [CHANGELOG.md](../CHANGELOG.md)
**Upgrade Guide**: [UPGRADE-GUIDE.md](./UPGRADE-GUIDE.md)
**Platform Comparison**: [CROSS-PLATFORM-GUIDE.md](./CROSS-PLATFORM-GUIDE.md)
