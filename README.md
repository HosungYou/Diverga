# Diverga 🌟

**Beyond Modal: AI Research Assistant That Thinks Creatively**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-5.0.0-brightgreen)](https://github.com/HosungYou/research-coordinator)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skills-blue)](https://claude.ai/code)
[![VS Methodology](https://img.shields.io/badge/VS-Verbalized%20Sampling-green)](https://arxiv.org/abs/2510.01171)
[![Language](https://img.shields.io/badge/language-English%20%7C%20한국어-orange)](docs/i18n/ko/README-ko.md)

---

## 🌟 Why "Diverga"? Breaking Free from Mode Collapse

Most AI research assistants suffer from **mode collapse** - they always recommend the same predictable options:

> ❌ "For technology adoption, I recommend TAM." (every single time)
> ❌ "For your meta-analysis, use random effects model." (always)
> ❌ "Try thematic analysis for your qualitative study." (the obvious choice)

**Diverga is different.** Built on **Verbalized Sampling (VS) methodology** (arXiv:2510.01171), it actively prevents mode collapse and guides you toward **creative, defensible research choices**.

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
|---------|----------------|---------------------|
| `T > 0.8` | **Modal** (most common) | ⚠️ Flags as "predictable" - warns about differentiation |
| `T 0.5-0.8` | **Established alternative** | ✅ Suggests as balanced choice |
| `T 0.3-0.5` | **Emerging approach** | ✅ Recommends for innovation with justification |
| `T < 0.3` | **Novel/creative** | 🔬 Presents with strong rationale required |

### 5 Creativity Mechanisms

Diverga uses five cognitive mechanisms to generate non-obvious options:

| Mechanism | Description | Example |
|-----------|-------------|---------|
| **Forced Analogy** | Borrow concepts from distant fields | "Apply ecosystem theory to technology adoption" |
| **Iterative Refinement** | 3-5 cycles of improvement | "Initial → Improved → Optimized framework" |
| **Semantic Distance** | Explore conceptually distant ideas | "Connect learning motivation to neuroplasticity" |
| **Temporal Reframing** | Shift temporal perspective | "How will this look in 10 years?" |
| **Community Simulation** | Simulate scholarly debate | "What would critics vs. innovators say?" |

### VS in Action: Before vs. After

```
❌ WITHOUT VS (Mode Collapse):
   User: "Help me choose a theoretical framework for AI adoption study"
   AI: "I recommend Technology Acceptance Model (TAM)."
   (Same answer every time, T=0.92)

✅ WITH VS (Diverga):
   User: "Help me choose a theoretical framework for AI adoption study"

   Diverga: "Let me analyze options across the typicality spectrum:

   [Modal Awareness] TAM (T=0.92) and UTAUT (T=0.85) are predictable choices.
   Most reviewers expect these, but they offer limited differentiation.

   [Forced Analogy Applied] From ecological theory:
   → 'Adaptive Learning Ecosystem' framework (T=0.35)

   [Semantic Distance Applied] From neuroscience:
   → 'Cognitive Plasticity in Technology Use' model (T=0.28)

   Recommended Options:
   • Direction A (T≈0.6): Self-Determination Theory × TAM integration
   • Direction B (T≈0.4): Cognitive Load Theory + Adaptive Ecosystem
   • Direction C (T≈0.2): Neuroplasticity-based technology learning

   For your context (innovative journal, novel contribution needed),
   I recommend Direction B. Shall I elaborate?"
```

---

## 🎯 What Makes Diverga Different

### 1. **Creative Guidance, Not Just Answers**
Diverga doesn't just answer questions - it expands your thinking by showing options you didn't know existed.

### 2. **Context Persistence**
Unlike general AI tools, Diverga maintains your research context:
- Research question and theoretical framework
- Methodological decisions and rationale
- Literature search strategies and results
- Analysis plans and intermediate findings

### 3. **27 Specialized Agents**
Expert agents for every research phase, from question formulation to publication.

### 4. **Paradigm-Aware**
Automatic detection of quantitative/qualitative/mixed methods with appropriate agent activation.

### 5. **Sisyphus Protocol**
Never claims completion without verification evidence.

---

## 🔬 VS Application Levels

Different agents apply VS at different intensities:

| Level | Agents | VS Mechanisms | Use Case |
|-------|--------|---------------|----------|
| **FULL** | A2, A4, B1, E1, E3, F4, H1, H2 | All 5 mechanisms + checkpoints | Theory selection, analysis design |
| **ENHANCED** | A1, A3, A5, B2-B4, C1-C4, D1-D4, E2 | FA, IL, SD + modal awareness | Design, data collection |
| **LIGHT** | E4, F1-F3, G1-G4 | Modal awareness only | Code generation, checklists |

### 14 User Checkpoints

Diverga confirms decisions at critical points:

| Code | Checkpoint | Purpose |
|------|-----------|---------|
| CP-INIT-001 | Initial context | Research field, experience level |
| CP-VS-001 | Modal awareness | Acknowledge predictable options |
| CP-VS-003 | Final choice | Approve selected approach |
| CP-FA-001 | Forced analogy | Validate cross-domain concepts |
| CP-IL-001 | Iteration gate | Continue refinement? |
| CP-SD-001 | Semantic distance | Confirm concept expansion |

---

## ✨ v5.0.0 (Sisyphus Edition)

### Sisyphus Protocol: Continuation Enforcement
Research tasks must be **completed** before moving on:
- **Agent-Based Orchestration**: Work delegated to specialized agents
- **Paradigm-Aware Completion**: Different criteria for quant/qual/mixed
- **Iron Law**: NO completion claims without fresh evidence

### Paradigm Detection & Agent Packs
Automatic detection activates appropriate agent sets:

| Paradigm | Auto-Detected Keywords | Agent Pack |
|----------|------------------------|------------|
| **Quantitative** | "effect size", "meta-analysis", "statistical power" | A1-A5, C1, E1, E4 |
| **Qualitative** | "phenomenology", "grounded theory", "thematic" | A1-A5, C2, D2, E2 |
| **Mixed Methods** | "convergent", "sequential", "joint display" | All 27 agents |

### Full Qualitative Research Support (NEW)
- **Phenomenology**: Bracketing, essence identification, meaning units
- **Grounded Theory**: Open/axial/selective coding, theoretical saturation
- **Case Study**: Thick description, pattern matching
- **Ethnography**: Fieldwork protocols, cultural interpretation
- **Action Research**: PDSA cycles, participatory engagement

### Mixed Methods Integration (NEW)
- Joint Display Tables
- Meta-Inference Generation
- Convergent/Sequential Design Support

---

## 🏗️ Architecture (27 Agents in 8 Categories)

### Category A: Research Foundation (5 Agents)
| # | Agent | VS Level | Purpose |
|---|-------|----------|---------|
| A1 | Research Question Refiner | Enhanced | FINER/PICO/SPIDER framework |
| A2 | Theoretical Framework Architect | **Full** | Theory selection with creativity |
| A3 | Hypothesis Generator | Enhanced | Testable hypotheses |
| A4 | Devil's Advocate | **Full** | Critical evaluation |
| A5 | Paradigm Advisor | Enhanced | Quant/qual/mixed guidance |

### Category B: Literature & Evidence (4 Agents)
| # | Agent | VS Level | Purpose |
|---|-------|----------|---------|
| B1 | Systematic Literature Scout | **Full** | PRISMA/qualitative search |
| B2 | Evidence Quality Appraiser | Enhanced | Quality assessment |
| B3 | Effect Size Extractor | Enhanced | Effect sizes/themes |
| B4 | Research Radar | Enhanced | Trend monitoring |

### Category C: Study Design (4 Agents)
| # | Agent | VS Level | Purpose |
|---|-------|----------|---------|
| C1 | Quantitative Design Consultant | Enhanced | Experimental design |
| C2 | Qualitative Design Consultant | Enhanced | Phenomenology, GT, case study |
| C3 | Mixed Methods Design Consultant | Enhanced | Sequential, convergent |
| C4 | Experimental Materials Developer | Enhanced | Treatment, control conditions |

### Category D: Data Collection (4 Agents)
| # | Agent | VS Level | Purpose |
|---|-------|----------|---------|
| D1 | Sampling Strategy Advisor | Enhanced | Probability/purposive sampling |
| D2 | Interview/Focus Group Specialist | Enhanced | Protocols, transcription |
| D3 | Observation Protocol Designer | Enhanced | Field notes, structured observation |
| D4 | Measurement Instrument Developer | Enhanced | Scale construction |

### Category E: Analysis (4 Agents)
| # | Agent | VS Level | Purpose |
|---|-------|----------|---------|
| E1 | Quantitative Analysis Guide | **Full** | Statistical analysis |
| E2 | Qualitative Coding Specialist | Enhanced | Thematic, GT coding |
| E3 | Mixed Methods Integrator | **Full** | Joint displays, meta-inference |
| E4 | Analysis Code Generator | Light | R/Python/NVivo code |

### Category F: Quality & Validation (4 Agents)
| # | Agent | VS Level | Purpose |
|---|-------|----------|---------|
| F1 | Sensitivity Analysis Designer | Light | Robustness checks |
| F2 | Checklist Manager | Light | PRISMA/CONSORT/COREQ |
| F3 | Reproducibility Auditor | Light | Open Science |
| F4 | Bias & Trustworthiness Detector | **Full** | Bias detection |

### Category G: Publication & Communication (4 Agents)
| # | Agent | VS Level | Purpose |
|---|-------|----------|---------|
| G1 | Journal Matcher | Light | Target journal selection |
| G2 | Academic Communicator | Light | Audience adaptation |
| G3 | Peer Review Strategist | Light | Review response |
| G4 | Preregistration Composer | Light | OSF/AsPredicted |

### Category H: Specialized Approaches (4 Agents)
| # | Agent | VS Level | Purpose |
|---|-------|----------|---------|
| H1 | Ethnographic Research Advisor | **Full** | Fieldwork, thick description |
| H2 | Action Research Facilitator | **Full** | PAR, CBPR cycles |
| H3 | Grounded Theory Advisor | **Full** | Constant comparison |
| H4 | Narrative Analysis Specialist | **Full** | Life history, autoethnography |

---

## 🚀 Getting Started

### Installation

```bash
git clone https://github.com/HosungYou/research-coordinator.git
cd research-coordinator
./scripts/install.sh
```

### Usage

**Natural Language**:
```
"I want to conduct a systematic review on AI in education"
"메타분석 연구를 시작하고 싶어요"
"Help me design an experimental study"
```

**Master Skill**:
```bash
/research-coordinator
```

**With OMC (oh-my-claudecode)**:
```bash
ulw: 문헌 검색해줘     # Maximum parallelism
eco: 통계 분석해줘     # Token efficient
ralph: 연구 설계해줘   # Persistence until done
```

---

## 🔧 Core Principle: Human-AI Division of Labor

> **"Human decisions remain with humans. AI handles what's beyond human scope."**
> **"인간이 할 일은 인간이, AI는 인간의 범주를 벗어난 것을 수행"**

### What Humans Decide
- Research direction and theoretical stance
- Inclusion/exclusion criteria
- Interpretation of findings
- Ethical trade-offs

### What Diverga Handles
- Searching 20,000+ papers across databases
- Calculating inter-rater reliability
- Generating PRISMA flow diagrams
- Formatting references to journal style
- **Expanding your options beyond the obvious**

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

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Quick Start](docs/QUICKSTART.md) | Get started in 5 minutes |
| [VS Methodology](docs/VS-METHODOLOGY.md) | Deep dive into Verbalized Sampling |
| [Agent Reference](docs/AGENT-REFERENCE.md) | 27 agents detailed reference |
| [OMC Integration](docs/OMC-INTEGRATION.md) | oh-my-claudecode integration |
| [한국어 문서](docs/i18n/ko/README-ko.md) | Korean documentation |

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
  year = {2025},
  version = {5.0.0},
  url = {https://github.com/HosungYou/research-coordinator},
  note = {27 agents with VS Methodology and Sisyphus Protocol. Prevents mode collapse through Verbalized Sampling (arXiv:2510.01171)}
}
```

---

**Made with 🌟 for Social Science Researchers**

*Diverga: Where creativity meets rigor. Beyond the obvious, toward the innovative.*
