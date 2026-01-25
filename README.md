# Research Coordinator 🧬

**AI Research Assistant for the Complete Research Lifecycle**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-4.0.0-brightgreen)](https://github.com/HosungYou/research-coordinator)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skills-blue)](https://claude.ai/code)
[![VS Methodology](https://img.shields.io/badge/VS-Verbalized%20Sampling-green)](https://arxiv.org/abs/2510.01171)
[![Language](https://img.shields.io/badge/language-English%20%7C%20한국어-orange)](docs/README-ko.md)

---

## 🎯 Overview

Research Coordinator is a specialized AI assistant system that supports the complete research lifecycle through **21 context-aware agents**. Built on Claude Code Skills, it maintains project context from initial question formulation through to publication.

### What Makes This Different?

**Context Persistence Across Research Lifecycle** - Unlike general AI tools that require re-explaining your research every conversation, Research Coordinator maintains:
- Your research question and theoretical framework
- Methodological decisions and their rationale
- Literature search strategies and results
- Analysis plans and intermediate findings
- Review history and revision decisions

All in a single platform, accessible throughout your project.

## ✨ New in v4.0.0

### 🗂️ Project State Management
Persistent research context stored in `.research/project-state.yaml`:
```yaml
research_question: "How do AI chatbots improve speaking skills?"
theoretical_framework: "Social Cognitive Theory"
methodology: "Systematic Review (PRISMA 2020)"
stage: "Stage 3: Screening"
```

### 📋 Pipeline Templates
Pre-configured workflows for common research types:
- **PRISMA 2020 Systematic Review** (7-stage workflow)
- **Meta-Analysis** (quantitative synthesis)
- **Experimental Studies** (RCT/Quasi-experimental)
- **Survey Research** (design to analysis)

### 🔗 Integration Hub
Direct connections to research tools:
- **Zotero MCP**: Reference management in Claude Code
- **Semantic Scholar API**: Automated literature retrieval
- **Nanobanana**: Gemini-powered data visualization
- **Office Suite**: Excel/Word/PowerPoint generation
- **R/Python**: Statistical analysis code

### 🧭 Guided Wizard
Conversational research setup using `AskUserQuestion` tool:
- Clear choice points with clickable options
- Progressive disclosure of complexity
- Context-aware suggestions
- Validation at each step

### 📄 Auto-Documentation
Automatic generation of:
- PRISMA 2020 flow diagrams (Mermaid)
- Data extraction spreadsheets (Excel)
- Conference presentations (PowerPoint)
- Method sections (Word)
- Analysis scripts (R/Python)

## 🏗️ Architecture (3-Tier Agent System)

### 🌟 Flagship Agents (Strategic Decisions)
| # | Agent | Purpose | VS Level |
|---|-------|---------|----------|
| **02** | **Theoretical Framework Architect** | Theory selection, conceptual model design | Full |
| **03** | **Devil's Advocate** | Critical evaluation, alternative perspectives | Full |
| **10** | **Statistical Analysis Guide** | Analysis method selection, interpretation | Full |
| **21** | **Research Coordinator Master** | Auto-dispatch, workflow orchestration | - |

### 🔧 Core Agents (Essential Capabilities)
| # | Agent | Purpose |
|---|-------|---------|
| 01 | Research Question Refiner | FINER/PICO framework application |
| 05 | Systematic Literature Scout | PRISMA search strategy |
| 06 | Evidence Quality Appraiser | Methodological quality assessment |
| 09 | Research Design Consultant | Study design optimization |
| 16 | Bias Detector | Identification and mitigation |
| 17 | Journal Matcher | Target journal identification |

### 🛠️ Support Agents (Specialized Tasks)
Agents #04, #07-08, #11-15, #18-20 handle specific tasks like ethics review, effect size extraction, code generation, and reproducibility audit.

## 🚀 Getting Started

### Installation

**Option 1: Marketplace Install (Recommended)**
```bash
# Add marketplace (one-time setup)
claude plugin marketplace add HosungYou/research-coordinator

# Install all 21 skills
claude plugin install research-coordinator
```

**Option 2: Local Development**
```bash
git clone https://github.com/HosungYou/research-coordinator.git
cd research-coordinator
./scripts/install.sh
```

### Verify Installation
```bash
claude plugin list | grep research-coordinator
```

Expected output:
```
❯ research-coordinator@research-coordinator-skills
  Version: 4.0.0
  Status: ✔ enabled
```

## 📖 Usage

### Natural Language Interface

Simply describe what you want to do:

```
"I want to conduct a systematic review on AI in education"
→ Activates PRISMA 2020 pipeline template

"메타분석 연구를 시작하고 싶어요"
→ Launches meta-analysis workflow (Korean support)

"Help me design an experimental study comparing two interventions"
→ Guides through experimental design wizard
```

### Master Skill Command

```bash
/research-coordinator
```

The master skill analyzes conversation context and automatically dispatches appropriate agents.

### Direct Agent Invocation

```bash
/theoretical-framework-architect    # Theory selection
/systematic-literature-scout        # PRISMA search
/statistical-analysis-guide         # Analysis planning
/journal-matcher                    # Publication targeting
```

### Auto-Trigger Example

```
User: "Planning a meta-analysis on effectiveness of AI tutoring systems"

Claude: [Auto-detected: "meta-analysis", "effectiveness"]
        → Activating agents:
          #05 Systematic Literature Scout
          #07 Effect Size Extractor
          #10 Statistical Analysis Guide
        → Initializing PRISMA 2020 workflow...
```

## 🧠 VS-Research Methodology (v3.0)

**Verbalized Sampling (VS)** prevents AI "mode collapse" - the tendency to always recommend the same obvious options.

### Dynamic T-Score (Typicality Score)

All recommendations include 0-1 typicality scores:

| T-Score | Interpretation | Recommendation |
|---------|----------------|----------------|
| `T > 0.8` | Modal (most common) | ⚠️ Avoid for differentiation |
| `T 0.5-0.8` | Established alternative | ✅ Safe choice |
| `T 0.3-0.5` | Emerging approach | ✅ Innovative, justifiable |
| `T < 0.3` | Creative/novel | ⚠️ Requires strong rationale |

### 5 Creativity Mechanisms

| Mechanism | Description | Example |
|-----------|-------------|---------|
| **Forced Analogy** | Borrow concepts from distant fields | "TAM → Ecosystem Theory" |
| **Iterative Loop** | 3-5 refinement cycles | "Initial → Improved → Optimized" |
| **Semantic Distance** | Explore conceptually distant ideas | "Learning effect → Neuroplasticity" |
| **Temporal Reframing** | Shift temporal perspective | "10-year retrospective view" |
| **Community Simulation** | Simulate scholarly debate | "Conservative vs. Innovative scholars" |

### 14 User Checkpoints

| Code | Checkpoint | Purpose |
|------|-----------|---------|
| CP-INIT-001 | Initial context confirmation | Research field/experience level |
| CP-INIT-002 | Goal clarification | Research objectives/expected outcomes |
| CP-VS-001 | Modal awareness check | Acknowledge modal options |
| CP-VS-003 | Final choice confirmation | Approve recommendation |
| CP-FA-001 | Forced analogy validation | Check analogy appropriateness |
| CP-IL-001 | Iteration loop gate | Continue refinement? |
| CP-SD-001 | Semantic distance validation | Confirm concept expansion |

### VS Application Levels

| Level | Agents | Description | Mechanisms |
|-------|--------|-------------|------------|
| **FULL** | 02, 03, 05, 10, 16 | Complete VS process | All 5 |
| **ENHANCED** | 01, 04, 06, 07, 08, 09 | Streamlined VS | FA, IL, SD |
| **LIGHT** | 11-15, 17-20 | Modal awareness + alternatives | None |

### Example: Avoiding Mode Collapse in Theory Selection

```
❌ Before VS (Mode Collapse):
   "For AI adoption research, I recommend TAM." (every time)

✅ After VS v3.0:
   [CP-INIT-001] Context check: Learning motivation study, prefers innovation

   Phase 1 - Modal Identification:
   "TAM (T=0.92) and UTAUT (T=0.85) are the most predictable choices."
   [CP-VS-001] Modal awareness confirmed

   Phase 2 - Creativity Mechanisms:
   [Forced Analogy] "Adaptive Learning Ecosystem" from ecological theory
   [Semantic Distance] "Plasticity" from neuroscience applied to learning

   Options:
   - Direction A (T≈0.6): Self-Determination Theory × TAM integration
   - Direction B (T≈0.4): Cognitive Load Theory + Adaptive Ecosystem
   - Direction C (T≈0.2): Neuroplasticity-based learning framework
   [CP-FA-001] Analogy appropriateness validated

   Phase 3 - Contextual Recommendation:
   [CP-VS-003] "For your context, Direction B (T=0.4) is recommended. Proceed?"
```

## 🔧 Core Principle: Human-AI Division of Labor

> **"Human decisions remain with humans. AI handles what's beyond human scope."**
> **"인간이 할 일은 인간이, AI는 인간의 범주를 벗어난 것을 수행"**

### What Humans Decide
- Research direction and theoretical stance
- Inclusion/exclusion criteria for studies
- Interpretation of findings
- Ethical trade-offs
- Publication strategy

### What AI Handles
- Searching 20,000+ papers across databases
- Calculating inter-rater reliability
- Generating PRISMA flow diagrams
- Extracting effect sizes from tables
- Formatting references to journal style

**All AI recommendations include checkpoints for human validation.**

## 📦 Complete Skill List (21 Skills)

| Skill Command | Category | VS Level | Description |
|---------------|----------|----------|-------------|
| `/research-coordinator` | Master | - | Auto-dispatch coordinator |
| `/research-question-refiner` | A: Design | Enhanced | FINER/PICO framework |
| `/theoretical-framework-architect` | A: Design | **Full** | Theory selection |
| `/devils-advocate` | A: Design | **Full** | Critical evaluation |
| `/research-ethics-advisor` | A: Design | Enhanced | IRB guidance |
| `/systematic-literature-scout` | B: Literature | **Full** | PRISMA search |
| `/evidence-quality-appraiser` | B: Literature | Enhanced | Quality assessment |
| `/effect-size-extractor` | B: Literature | Enhanced | Effect size conversion |
| `/research-radar` | B: Literature | Enhanced | Trend monitoring |
| `/research-design-consultant` | C: Method | Enhanced | Design optimization |
| `/statistical-analysis-guide` | C: Method | **Full** | Analysis planning |
| `/analysis-code-generator` | C: Method | Light | R/Python code |
| `/sensitivity-analysis-designer` | C: Method | Light | Sensitivity analysis |
| `/internal-consistency-checker` | D: Quality | Light | Logical consistency |
| `/checklist-manager` | D: Quality | Light | PRISMA/CONSORT |
| `/reproducibility-auditor` | D: Quality | Light | Reproducibility check |
| `/bias-detector` | D: Quality | **Full** | Bias identification |
| `/journal-matcher` | E: Publish | Light | Journal targeting |
| `/academic-communicator` | E: Publish | Light | Audience adaptation |
| `/peer-review-strategist` | E: Publish | Light | Review response |
| `/preregistration-composer` | E: Publish | Light | OSF/AsPredicted |

## 🔗 Integration Hub

### No Setup Required
| Tool | Use Case | Trigger |
|------|----------|---------|
| **Excel** | Data extraction sheets | "Create extraction spreadsheet" |
| **PowerPoint** | Presentations | "Generate conference slides" |
| **Word** | Manuscripts | "Export method section" |
| **Python** | Data analysis | Built-in |
| **Mermaid** | Flow diagrams | "Create PRISMA diagram" |

### Requires Setup
| Tool | Purpose | Setup Command |
|------|---------|---------------|
| **Semantic Scholar** | Literature retrieval | Add API key to `.env` |
| **OpenAlex** | Open access search | Add email for polite pool |
| **Zotero MCP** | Reference management | `/oh-my-claudecode:mcp-setup` |
| **Nanobanana** | Gemini visualization | Add Gemini API key |
| **R Scripts** | Statistical analysis | Install R locally |

## 🌐 Multilingual Support

Research Coordinator fully supports **Korean and English** input:

```
English: "I want to conduct a systematic review"
Korean: "체계적 문헌고찰을 하고 싶어요"
Mixed: "메타분석을 하려는데, can you help?"
```

All agents understand both languages and respond appropriately.

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Quick Start](docs/QUICKSTART.md) | Get started in 5 minutes |
| [Installation](docs/SETUP.md) | Full setup instructions |
| [Usage Examples](docs/USAGE-EXAMPLES.md) | Common use cases |
| [Agent Reference](docs/AGENT-REFERENCE.md) | 21 agents detailed reference |
| [OMC Integration](docs/OMC-INTEGRATION.md) | oh-my-claudecode integration |
| [Roadmap](docs/ROADMAP.md) | Future development plans |
| [Changelog](docs/CHANGELOG.md) | Version history |
| [한국어 문서](docs/i18n/ko/README-ko.md) | Korean documentation |

## 🔧 Requirements

- [Claude Code CLI](https://claude.ai/code)
- Bash shell (macOS/Linux, WSL for Windows)
- Optional: R (for statistical code generation), Python 3.8+ (for data analysis)

## 🤝 Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md).

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Claude Code](https://claude.ai/code) by Anthropic - AI-powered coding assistant
- [Verbalized Sampling (arXiv:2510.01171)](https://arxiv.org/abs/2510.01171) - VS methodology foundation
- Social science research community for feedback and validation

## 📖 Citation

If you use Research Coordinator in your research, please cite:

```bibtex
@software{research_coordinator,
  author = {You, Hosung},
  title = {Research Coordinator: AI Research Assistant for the Complete Research Lifecycle},
  year = {2025},
  version = {4.0.0},
  url = {https://github.com/HosungYou/research-coordinator},
  note = {Integrates Verbalized Sampling methodology from arXiv:2510.01171}
}
```

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=HosungYou/research-coordinator&type=Date)](https://star-history.com/#HosungYou/research-coordinator&Date)

---

**Made with ❤️ for Social Science Researchers**

*Empowering human researchers with AI assistance that respects human judgment.*
