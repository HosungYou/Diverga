<div align="center">

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     ██████╗ ██╗██╗   ██╗███████╗██████╗  ██████╗  █████╗                    ║
║     ██╔══██╗██║██║   ██║██╔════╝██╔══██╗██╔════╝ ██╔══██╗                   ║
║     ██║  ██║██║██║   ██║█████╗  ██████╔╝██║  ███╗███████║                   ║
║     ██║  ██║██║╚██╗ ██╔╝██╔══╝  ██╔══██╗██║   ██║██╔══██║                   ║
║     ██████╔╝██║ ╚████╔╝ ███████╗██║  ██║╚██████╔╝██║  ██║                   ║
║     ╚═════╝ ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝                   ║
║                                                                               ║
║              🎯 Diverge from the Modal · Discover the Exceptional            ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

              ┌─────────────────────────────────────────────────┐
              │  Research Methodology AI Assistant for          │
              │  Claude Code · 40 Specialized Agents · VS+HAVS  │
              └─────────────────────────────────────────────────┘
```

[![Version](https://img.shields.io/badge/version-6.6.1-7c3aed?style=for-the-badge&logo=semantic-release&logoColor=white)](https://github.com/HosungYou/Diverga)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Plugin-FF6B00?style=for-the-badge&logo=anthropic&logoColor=white)](https://claude.ai/code)
[![Codex CLI](https://img.shields.io/badge/Codex_CLI-Support-412991?style=for-the-badge&logo=openai&logoColor=white)](docs/DESIGN_SYSTEM.md)
[![OpenCode](https://img.shields.io/badge/OpenCode-Plugin-0969da?style=for-the-badge&logo=github&logoColor=white)](docs/DESIGN_SYSTEM.md)
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge&logo=open-source-initiative&logoColor=white)](LICENSE)
[![Methodology](https://img.shields.io/badge/Powered_by-VS+HAVS-violet?style=for-the-badge&logo=academia&logoColor=white)](docs/methodology.md)
[![Language](https://img.shields.io/badge/language-English%20%7C%20한국어-orange?style=for-the-badge)](docs/i18n/ko/README-ko.md)
[![Agents](https://img.shields.io/badge/agents-40-purple?style=for-the-badge)](docs/AGENTS.md)

```
         ╭──────────────────────────────────────────────────────────╮
         │                                                          │
         │  "When AI recommendations converge on the modal,         │
         │   Diverga helps you explore the exceptional."            │
         │                                                          │
         │               — Verbalized Sampling Principle            │
         │                                                          │
         ╰──────────────────────────────────────────────────────────╯
```

</div>

---

## ✨ What is Diverga?

**Diverga** is a research methodology assistant that transforms Claude Code into a 40-agent orchestra for social science research. Built on **Verbalized Sampling (VS)** and **HAVS** (Humanization-Adapted VS) methodologies, it prevents AI "mode collapse" — the tendency to recommend only safe, modal solutions.

<div align="center">

![VS Methodology - Modal AI vs Diverga](docs/images/vs-methodology-infographic.svg)

</div>

<div align="center">

### 🎯 Perfect For

**Education** • **Psychology** • **Management** • **Sociology** • **HRD** • **Communication**

</div>

---

## 🚀 Quick Start (3 Steps)

```bash
# Step 1: Add to Claude Code marketplace
/plugin marketplace add https://github.com/HosungYou/Diverga

# Step 2: Install the plugin
/plugin install diverga

# Step 3: Run setup wizard
/diverga:setup
```

Then just say what you want:
```
"I want to conduct a meta-analysis on AI in education"
"체계적 문헌고찰을 시작하고 싶어"
"Help me design an experimental study"
```

Diverga auto-detects context and activates the right agents.

---

## 🌟 Why "Diverga"? Breaking Free from Mode Collapse

Most AI research assistants suffer from **mode collapse** - they always recommend the same predictable options:

> ❌ "For technology adoption, I recommend TAM." (every single time)
> ❌ "For your meta-analysis, use random effects model." (always)
> ❌ "Try thematic analysis for your qualitative study." (the obvious choice)

**Diverga is different.** Built on **Verbalized Sampling (VS) methodology** (arXiv:2510.01171), it actively prevents mode collapse and guides you toward **creative, defensible research choices**.

<table>
<tr>
<td width="50%">

### 🤖 Standard AI Assistant

```
User: "Suggest a research design"

AI: ✓ Use quasi-experimental design
    ✓ Pretest-posttest control group
    ✓ ANOVA for analysis

Result: Safe, common, modal ✓
        But not optimal for you ✗
```

</td>
<td width="50%">

### ⚡ Diverga with VS/HAVS

```
User: "Suggest a research design"

Diverga:
  ◆ Option A (Modal): Quasi-experimental
  ◆ Option B (Creative): Design-based research
  ◆ Option C (Mixed): Sequential explanatory
  ◆ Option D (Novel): Computational simulation

  → Human checkpoints enforce choice
  → Forces divergence from modal
  → Preserves methodological rigor
```

</td>
</tr>
</table>

---

## ✨ v6.5 (Parallel Execution Edition)

### Core Principle

> **"Human decisions remain with humans. AI handles what's beyond human scope."**
> **"인간이 할 일은 인간이, AI는 인간의 범주를 벗어난 것을 수행"**

### 🆕 What's New in v6.5

| Feature | Description |
|---------|-------------|
| **🚀 Parallel Agent Execution** | Run multiple agents simultaneously via Task tool |
| **📁 /agents/ Directory** | Direct agent files for Task tool registration |
| **⚡ oh-my-claudecode Compatible** | Same invocation pattern: `Task(subagent_type="diverga:a1")` |
| **🔧 TypeScript Runtime** | Programmatic agent access via `getAgentDefinitions()` |
| **🔄 Dual Invocation** | Both Skill (`/diverga:A1-...`) and Task (`diverga:a1`) supported |

### Parallel Execution Quick Start

```python
# Single agent
Task(subagent_type="diverga:a1", prompt="Refine my research question...")

# Parallel execution (single message, multiple Tasks)
Task(subagent_type="diverga:a1", prompt="Research question...")
Task(subagent_type="diverga:a2", prompt="Theoretical framework...")
Task(subagent_type="diverga:a3", prompt="Critical evaluation...")
```

---

## 🎯 Human Checkpoint System

Diverga implements **forced divergence** through human checkpoints:

<div align="center">

```
                    ╭─────────────────────────────╮
                    │   User Research Question    │
                    ╰──────────────┬──────────────╯
                                   │
                                   ▼
                    ╭─────────────────────────────╮
                    │  Agent Generates Multiple   │
                    │  Diverse Options (VS/HAVS)  │
                    │                             │
                    │  ◆ Option A (Modal)         │
                    │  ◆ Option B (Creative)      │
                    │  ◆ Option C (Rigorous)      │
                    │  ◆ Option D (Novel)         │
                    ╰──────────────┬──────────────╯
                                   │
                                   ▼
                    ╭─────────────────────────────╮
                    │  👤 HUMAN CHECKPOINT 👤    │
                    │                             │
                    │  Required: Explicit Choice  │
                    │  No default selection       │
                    │  Forces consideration       │
                    ╰──────────────┬──────────────╯
                                   │
                                   ▼
                    ╭─────────────────────────────╮
                    │  Selected Path Continues    │
                    │  (Prevents mode collapse)   │
                    ╰─────────────────────────────╯
```

</div>

### Checkpoint Types

| Level | Icon | Behavior |
|-------|------|----------|
| **REQUIRED** | 🔴 | System STOPS - Cannot proceed without explicit approval |
| **RECOMMENDED** | 🟠 | System PAUSES - Strongly suggests approval |
| **OPTIONAL** | 🟡 | System ASKS - Defaults available if skipped |

### Required Checkpoints

| Checkpoint | When | What Happens |
|------------|------|--------------|
| CP_RESEARCH_DIRECTION | Research question finalized | Present VS options, WAIT for selection |
| CP_PARADIGM_SELECTION | Methodology approach | Ask Quantitative/Qualitative/Mixed |
| CP_THEORY_SELECTION | Framework chosen | Present alternatives with T-Scores |
| CP_METHODOLOGY_APPROVAL | Design complete | Detailed review required |

---

## 🧠 Core Innovation: Verbalized Sampling (VS) Methodology

### The Problem: Modal Recommendations

AI systems tend to recommend the most statistically common options - what we call **modal recommendations**. While safe, these lead to:
- Homogenized research landscapes
- Missed innovative opportunities
- Difficulty differentiating your work

### The Solution: Dynamic T-Score System

Diverga assigns **Typicality Scores (T-Score)** to all recommendations:

| T-Score | Interpretation | Diverga Behavior |
|---------|----------------|------------------|
| `T > 0.8` | **Modal** (most common) | ⚠️ Flags as "predictable" |
| `T 0.5-0.8` | **Established alternative** | ✅ Suggests as balanced choice |
| `T 0.3-0.5` | **Emerging approach** | ✅ Recommends for innovation |
| `T < 0.3` | **Novel/creative** | 🔬 Presents with strong rationale |

### VS in Action: Before vs. After

```
❌ WITHOUT VS (Mode Collapse):
   User: "Help me choose a theoretical framework for AI adoption study"
   AI: "I recommend Technology Acceptance Model (TAM)."
   (Same answer every time, T=0.92)

✅ WITH VS (Diverga):
   User: "Help me choose a theoretical framework for AI adoption study"

   🔴 CHECKPOINT: CP_THEORY_SELECTION

   Diverga: "Let me analyze options across the typicality spectrum:

   [Modal Awareness] TAM (T=0.92) and UTAUT (T=0.85) are predictable choices.

   Recommended Options:
   • Direction A (T≈0.6): Self-Determination Theory × TAM integration
   • Direction B (T≈0.4): Cognitive Load Theory + Adaptive Ecosystem ⭐
   • Direction C (T≈0.2): Neuroplasticity-based technology learning

   Which direction would you like to proceed?"
   (WAITS for human selection)
```

---

## 🏗️ Architecture (40 Agents in 8 Categories)

<div align="center">

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                         🎯 AGENT ECOSYSTEM (40 AGENTS)                        ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   📐 Category A: Foundation (6)         🔍 Category B: Evidence (5)          ║
║   ─────────────────────────────         ────────────────────────             ║
║   ◆ A1-research-question-refiner        ◆ B1-systematic-literature-scout    ║
║   ◆ A2-theoretical-framework-architect  ◆ B2-evidence-quality-appraiser     ║
║   ◆ A3-devils-advocate                  ◆ B3-effect-size-extractor          ║
║   ◆ A4-research-ethics-advisor          ◆ B4-research-radar                  ║
║   ◆ A5-paradigm-worldview-advisor       ◆ B5-parallel-document-processor    ║
║   ◆ A6-conceptual-framework-visualizer                                       ║
║                                                                               ║
║   📊 Category C: Design (7)             📋 Category D: Data Collection (4)   ║
║   ─────────────────────────             ─────────────────────────────────    ║
║   ◆ C1-quantitative-design-consultant   ◆ D1-sampling-strategy-advisor      ║
║   ◆ C2-qualitative-design-consultant    ◆ D2-interview-focus-group-specialist║
║   ◆ C3-mixed-methods-design-consultant  ◆ D3-observation-protocol-designer  ║
║   ◆ C4-experimental-materials-developer ◆ D4-measurement-instrument-developer║
║   ◆ C5-meta-analysis-master                                                  ║
║   ◆ C6-data-integrity-guard                                                  ║
║   ◆ C7-error-prevention-engine                                               ║
║                                                                               ║
║   📈 Category E: Analysis (5)           ✅ Category F: Quality (5)           ║
║   ───────────────────────               ─────────────────────                ║
║   ◆ E1-quantitative-analysis-guide      ◆ F1-internal-consistency-checker   ║
║   ◆ E2-qualitative-coding-specialist    ◆ F2-checklist-manager              ║
║   ◆ E3-mixed-methods-integration        ◆ F3-reproducibility-auditor        ║
║   ◆ E4-analysis-code-generator          ◆ F4-bias-trustworthiness-detector  ║
║   ◆ E5-sensitivity-analysis-designer    ◆ F5-humanization-verifier          ║
║                                                                               ║
║   📝 Category G: Communication (6)      🎓 Category H: Specialized (2)       ║
║   ─────────────────────────────         ──────────────────────────           ║
║   ◆ G1-journal-matcher                  ◆ H1-ethnographic-research-advisor  ║
║   ◆ G2-academic-communicator            ◆ H2-action-research-facilitator    ║
║   ◆ G3-peer-review-strategist                                                ║
║   ◆ G4-preregistration-composer                                              ║
║   ◆ G5-academic-style-auditor                                                ║
║   ◆ G6-academic-style-humanizer 🆕 HAVS                                      ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

</div>

### Agent Details by Category

#### Category A: Foundation (6 Agents)
| Agent | Model | Purpose |
|-------|-------|---------|
| A1-research-question-refiner | Opus | FINER/PICO/SPIDER framework |
| A2-theoretical-framework-architect | Opus | Theory selection with VS |
| A3-devils-advocate | Opus | Critical evaluation |
| A4-research-ethics-advisor | Sonnet | IRB, ethical considerations |
| A5-paradigm-worldview-advisor | Opus | Quant/qual/mixed guidance |
| A6-conceptual-framework-visualizer | Sonnet | Visual framework design |

#### Category B: Evidence (5 Agents)
| Agent | Model | Purpose |
|-------|-------|---------|
| B1-systematic-literature-scout | Sonnet | PRISMA/qualitative search |
| B2-evidence-quality-appraiser | Sonnet | RoB, GRADE assessment |
| B3-effect-size-extractor | Haiku | Effect size calculations |
| B4-research-radar | Haiku | Trend monitoring |
| **B5-parallel-document-processor** | Opus | Batch PDF processing with parallel workers |

#### Category C: Design & Meta-Analysis (7 Agents)
| Agent | Model | Purpose |
|-------|-------|---------|
| C1-quantitative-design-consultant | Opus | Experimental, survey design |
| C2-qualitative-design-consultant | Opus | Phenomenology, GT, case study |
| C3-mixed-methods-design-consultant | Opus | Sequential, convergent |
| C4-experimental-materials-developer | Sonnet | Treatment materials |
| **C5-meta-analysis-master** | Opus | Multi-gate validation, workflow orchestration |
| **C6-data-integrity-guard** | Sonnet | Data extraction with provenance |
| **C7-error-prevention-engine** | Sonnet | Pattern detection, error prevention |

#### Category D: Data Collection (4 Agents)
| Agent | Model | Purpose |
|-------|-------|---------|
| D1-sampling-strategy-advisor | Sonnet | Probability/purposive sampling |
| D2-interview-focus-group-specialist | Sonnet | Protocols, transcription |
| D3-observation-protocol-designer | Haiku | Field notes |
| D4-measurement-instrument-developer | Opus | Scale construction |

#### Category E: Analysis (5 Agents)
| Agent | Model | Purpose |
|-------|-------|---------|
| E1-quantitative-analysis-guide | Opus | Statistical analysis |
| E2-qualitative-coding-specialist | Opus | Thematic, GT coding |
| E3-mixed-methods-integration | Opus | Joint displays, meta-inference |
| E4-analysis-code-generator | Haiku | R/Python/NVivo code |
| E5-sensitivity-analysis-designer | Sonnet | Robustness checks |

#### Category F: Quality (5 Agents)
| Agent | Model | Purpose |
|-------|-------|---------|
| F1-internal-consistency-checker | Haiku | Internal validity |
| F2-checklist-manager | Haiku | PRISMA/CONSORT/COREQ |
| F3-reproducibility-auditor | Sonnet | Open Science |
| F4-bias-trustworthiness-detector | Sonnet | Bias detection |
| **F5-humanization-verifier** | Haiku | Transformation verification |

#### Category G: Communication (6 Agents)
| Agent | Model | Purpose |
|-------|-------|---------|
| G1-journal-matcher | Sonnet | Target journal selection |
| G2-academic-communicator | Sonnet | Audience adaptation |
| G3-peer-review-strategist | Opus | Review response |
| G4-preregistration-composer | Sonnet | OSF/AsPredicted |
| **G5-academic-style-auditor** | Sonnet | AI pattern detection (24 categories) |
| **G6-academic-style-humanizer** | Opus | Pattern transformation (HAVS) |

#### Category H: Specialized (2 Agents)
| Agent | Model | Purpose |
|-------|-------|---------|
| H1-ethnographic-research-advisor | Opus | Fieldwork, thick description |
| H2-action-research-facilitator | Opus | PAR, CBPR cycles |

---

## 🚀 Getting Started

### Installation (Claude Code Plugin)

```bash
# Install via Claude Code marketplace
/plugin marketplace add https://github.com/HosungYou/Diverga
/plugin install diverga
/diverga:setup
```

### Alternative: Manual Installation

```bash
git clone https://github.com/HosungYou/Diverga.git
cd Diverga
```

### Usage

**Natural Language** (auto-triggers agents):
```
"I want to conduct a systematic review on AI in education"
"메타분석 연구를 시작하고 싶어요"
"Help me design an experimental study"
```

**Direct Commands**:
```
/diverga:setup          # Configuration wizard
/diverga:help           # Show all 40 agents
/diverga:meta-analysis  # Start meta-analysis workflow
diverga:c5              # Invoke specific agent
```

The system will:
1. Detect your paradigm
2. **ASK for confirmation** (🔴 CHECKPOINT)
3. Present VS alternatives with T-Scores
4. **WAIT for your selection**
5. Guide you through the pipeline with checkpoints

---

## 📚 Version History

| Version | Feature |
|---------|---------|
| **v6.6.0** | Cross-Platform Edition - Codex CLI & OpenCode support, shared lib/ |
| **v6.5.0** | Parallel Execution Edition - Task tool support, /agents/ directory |
| **v6.4.0** | Plugin Marketplace - `/plugin marketplace add`, auto-trigger dispatch |
| **v6.3.0** | Meta-Analysis Agent System - C5/C6/C7 for Hedges' g calculation |
| **v6.2.0** | Parallel Document Processing - B5 for batch PDF handling |
| **v6.1.0** | Humanization Pipeline - G5/G6/F5 for natural academic prose |
| **v6.0.0** | Human-Centered Edition - Mandatory checkpoints, removed autonomous modes |

---

## 🔗 Integration Hub

### Built-in (No Setup)
| Tool | Use Case |
|------|----------|
| Excel | Data extraction, coding sheets |
| PowerPoint | Conference presentations |
| Word | Manuscripts, method sections |
| Python | Analysis scripts |
| Mermaid | Flow diagrams |

### Requires Setup
| Tool | Purpose |
|------|---------|
| Semantic Scholar | Literature retrieval |
| OpenAlex | Open access search |
| Zotero MCP | Reference management |
| R Scripts | Statistical analysis |

---

## 🌐 Multilingual Support

Diverga fully supports **Korean and English**:

```
English: "I want to conduct a systematic review"
Korean: "체계적 문헌고찰을 하고 싶어요"
Mixed: "메타분석을 하려는데, can you help?"
```

---

## 🌐 Cross-Platform Support (v6.6.1)

Diverga now works across **three AI coding platforms** with unified install scripts:

| Platform | Status | One-Line Install |
|----------|--------|------------------|
| **Claude Code** | ✅ Full Support | `/plugin install diverga` |
| **OpenAI Codex CLI** | ✅ Full Support | `curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-codex.sh \| bash` |
| **OpenCode** | ✅ Full Support | `curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-opencode.sh \| bash` |
| **Auto-Detect All** | ✅ Universal | `curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install.sh \| bash` |

### Architecture

```
Diverga/
├── lib/                         # 🆕 Shared Core Module
│   ├── agents/                  # Agent discovery & registry
│   ├── checkpoints/             # Checkpoint definitions
│   └── tscore/                  # T-Score reference
├── .claude/skills/              # Claude Code (source of truth)
├── .codex/                      # 🆕 Codex CLI Adapter
│   ├── AGENTS.md               # Bootstrap markdown
│   └── diverga-codex.js        # CLI wrapper
└── .opencode/                   # 🆕 OpenCode Plugin
    ├── oh-my-opencode.json     # Config
    └── plugins/diverga/        # JavaScript plugin
```

### Codex CLI Quick Start

> ⚠️ **Important**: Unlike Claude Code, Codex CLI installation runs in a **regular terminal**, not inside Codex CLI.

```bash
# Step 1: Install from regular terminal (NOT inside Codex CLI)
npx @diverga/codex-setup

# Step 2: Start Codex CLI
codex

# Step 3: Use naturally - agents activate automatically
> "I want to conduct a meta-analysis on AI in education"
# → C5-MetaAnalysisMaster activates automatically
```

**Installation Difference:**
| Platform | Where to Install | Command |
|----------|------------------|---------|
| Claude Code | Inside Claude Code | `/plugin install diverga` |
| Codex CLI | Regular terminal | `npx @diverga/codex-setup` |
| OpenCode | Regular terminal | `curl ... \| bash` (see below) |

### OpenCode Quick Start

> ⚠️ **Important**: Like Codex CLI, OpenCode installation runs in a **regular terminal**, not inside OpenCode.

```bash
# Step 1: Install OpenCode (if not installed)
brew install anomalyco/tap/opencode   # macOS/Linux
# or: npm i -g opencode-ai@latest

# Step 2: Install Diverga from regular terminal
curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-opencode.sh | bash

# Step 3: Start OpenCode and use
opencode
> "I want to conduct a meta-analysis"
# → Agents activate automatically
```

### Model Mapping

| Tier | Claude Code | Codex CLI | OpenCode |
|------|-------------|-----------|----------|
| HIGH | opus | o3 / codex-mini | *provider 설정* |
| MEDIUM | sonnet | gpt-4.1 | *provider 설정* |
| LOW | haiku | gpt-4o-mini | *provider 설정* |

> **Note**: OpenCode is provider-agnostic (75+ models supported). Use `/connect` command to configure your preferred provider (Claude, OpenAI, Gemini, local models, etc.).

### Tool Mapping (Claude → Codex)

| Claude Tool | Codex Equivalent |
|-------------|------------------|
| `TodoWrite` | `update_plan` |
| `Task` | Direct execution |
| `Read` | `read_file` |
| `Edit` | `apply_diff` |
| `Grep` | `grep` |
| `Bash` | `shell` |

All 40 agents work identically across all platforms with VS methodology and human checkpoints enforced.

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [CLAUDE.md](CLAUDE.md) | Full system documentation |
| [PLUGIN.md](PLUGIN.md) | Plugin marketplace definition |
| [AGENTS.md](AGENTS.md) | 40 agents detailed reference |
| [Agent Orchestration Guide](docs/AGENT-ORCHESTRATION-GUIDE.md) | Comprehensive multi-agent pipelines (EN) |
| [에이전트 오케스트레이션 가이드](docs/AGENT-ORCHESTRATION-GUIDE-ko.md) | 종합 멀티에이전트 파이프라인 (KO) |
| [B5 Parallel Processing](docs/B5-PARALLEL-PROCESSING.md) | v6.2 parallel document processing |
| [Quick Start](docs/QUICKSTART.md) | Get started in 5 minutes |
| [VS Methodology](docs/VS-METHODOLOGY.md) | Deep dive into Verbalized Sampling |
| [Humanization Pipeline](docs/v6.1.0-humanization-pipeline.md) | v6.1 humanization documentation |
| [Cross-Platform Guide](docs/DESIGN_SYSTEM.md) | Cross-platform support details |
| [CHANGELOG](CHANGELOG.md) | Version history |

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- [Claude Code](https://claude.ai/code) by Anthropic
- [Verbalized Sampling (arXiv:2510.01171)](https://arxiv.org/abs/2510.01171) - VS methodology foundation
- Social science research community for feedback

---

## 📖 Citation

```bibtex
@software{diverga,
  author = {You, Hosung},
  title = {Diverga: Beyond Modal AI Research Assistant},
  year = {2026},
  version = {6.6.1},
  url = {https://github.com/HosungYou/Diverga},
  note = {40 agents with VS Methodology, Human-Centered Design, Meta-Analysis System, Humanization Pipeline, Plugin Marketplace, Parallel Execution, and Cross-Platform Support (Claude Code, Codex CLI, OpenCode). Prevents mode collapse through Verbalized Sampling (arXiv:2510.01171)}
}
```

---

<div align="center">

**Made with 🌟 for Social Science Researchers**

*Diverga: Where creativity meets rigor. Beyond the obvious, toward the innovative.*

</div>
