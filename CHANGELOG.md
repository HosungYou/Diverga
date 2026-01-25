# Changelog

All notable changes to Diverga (formerly Research Coordinator) will be documented in this file.

## [5.0.0] - 2025-01-25 (Sisyphus Edition)

### Overview

Diverga v5.0.0 represents a major architectural redesign, expanding from 21 to 27 agents across 8 categories (A-H). This release introduces the Sisyphus continuation enforcement pattern, automatic paradigm detection, and comprehensive support for qualitative and mixed methods research.

**Core Theme**: "Beyond Modal - Creative, Defensible Research Choices"

### Project Renamed: Research Coordinator → Diverga

This release marks the **official renaming** of the project to **Diverga** to better reflect its core mission:

- **"Diverga"** = Divergent thinking, breaking free from the obvious
- **Breaking free from mode collapse** through Verbalized Sampling (VS) methodology
- **T-Score system** for rating typicality of recommendations (0-1 scale)
- **5 Creativity Mechanisms**: Forced Analogy, Iterative Refinement, Semantic Distance, Temporal Reframing, Community Simulation

### New Features

#### Verbalized Sampling (VS) Methodology

Diverga's **core innovation** that prevents mode collapse:

| T-Score | Interpretation | Diverga Behavior |
|---------|----------------|---------------------|
| `T > 0.8` | Modal (predictable) | ⚠️ Flags and warns about differentiation |
| `T 0.5-0.8` | Established alternative | ✅ Suggests as balanced choice |
| `T 0.3-0.5` | Emerging approach | ✅ Recommends for innovation |
| `T < 0.3` | Novel/creative | 🔬 Presents with strong rationale |

#### Sisyphus Protocol

### New Features

#### Sisyphus Protocol

Adopted from oh-my-opencode, the Sisyphus protocol enforces continuation until verified completion:

- **Continuation Enforcement**: Research work never stops until paradigm-specific completion criteria are met
- **Verification Before Completion**: Every claim of "done" requires fresh evidence
- **Paradigm-Specific Criteria**: Different completion checklists for quantitative, qualitative, and mixed methods

**Completion Criteria by Paradigm**:

| Paradigm | Key Criteria |
|----------|-------------|
| Quantitative | Hypotheses tested, power analysis done, effect sizes reported, visualizations generated |
| Qualitative | Saturation documented, themes refined, trustworthiness criteria met, member checking completed |
| Mixed Methods | Both strands complete, integration strategy documented, joint display created, meta-inference generated |

#### Paradigm Auto-Detection

Automatic detection of research paradigm based on conversation keywords:

- **Quantitative Signals**: "hypothesis", "effect size", "p-value", "ANOVA", "regression", "가설", "효과크기"
- **Qualitative Signals**: "lived experience", "saturation", "themes", "phenomenology", "체험", "포화"
- **Mixed Methods Signals**: "sequential", "convergent", "integration", "joint display", "혼합방법"

#### Smart Model Routing (Updated)

| Tier | Model | Agent Types |
|------|-------|-------------|
| HIGH | Opus | Complex interpretive work, philosophical reasoning (A2, A5, C2, C3, E2, E3, H1-H4) |
| MEDIUM | Sonnet | Standard research tasks (A1, A3, A4, B1, B2, C1, C4, D1-D4, E1, E4, F2, F4, G2, G3) |
| LOW | Haiku | Quick lookups, formatting, checklists (B3, B4, F1, F3, G1, G4) |

### Agent Expansion (21 → 33)

#### Category Structure

| Category | Name | Agent Count | Description |
|----------|------|-------------|-------------|
| A | Foundation | 5 | Research question, theory, ethics, paradigm |
| B | Evidence | 4 | Literature review, quality appraisal, effect sizes |
| C | Design | 4 | Quantitative, qualitative, mixed methods design |
| D | Data Collection | 4 | Sampling, interviews, observation, instruments |
| E | Analysis | 4 | Statistical, coding, integration, code generation |
| F | Quality | 4 | Sensitivity, checklists, reproducibility, bias |
| G | Communication | 4 | Journal matching, writing, peer review, preregistration |
| H | Specialized | 4 | Ethnography, narrative, grounded theory, action research |

### New Agents (12 Total)

#### Category A: Foundation (+1)

| Agent ID | Name | Purpose | Tier |
|----------|------|---------|------|
| A5 | Paradigm & Worldview Advisor | Ontology, epistemology, paradigm selection | HIGH |

#### Category C: Design (+3)

| Agent ID | Name | Purpose | Tier |
|----------|------|---------|------|
| C2 | Qualitative Design Consultant | Phenomenology, grounded theory, case study, narrative | HIGH |
| C3 | Mixed Methods Design Consultant | Sequential, convergent, embedded, transformative designs | HIGH |
| C4 | Experimental Materials Developer | Treatment protocols, control conditions, manipulation checks | MEDIUM |

#### Category D: Data Collection (+4, New Category)

| Agent ID | Name | Purpose | Tier |
|----------|------|---------|------|
| D1 | Sampling Strategy Advisor | Probability, purposive, theoretical sampling | MEDIUM |
| D2 | Interview & Focus Group Specialist | Interview protocols, focus groups, transcription | MEDIUM |
| D3 | Observation Protocol Designer | Field notes, structured observation, video analysis | MEDIUM |
| D4 | Measurement Instrument Developer | Scale construction, validity, reliability | MEDIUM |

#### Category E: Analysis (+2)

| Agent ID | Name | Purpose | Tier |
|----------|------|---------|------|
| E2 | Qualitative Coding Specialist | Thematic analysis, grounded theory coding, saturation | HIGH |
| E3 | Mixed Methods Integration Specialist | Joint displays, meta-inference, legitimation | HIGH |

#### Category H: Specialized (+4, New Category)

| Agent ID | Name | Purpose | Tier |
|----------|------|---------|------|
| H1 | Ethnographic Research Advisor | Fieldwork, participant observation, thick description | HIGH |
| H2 | Action Research Facilitator | PAR, CBPR, action cycles, community engagement | MEDIUM |
| H3 | Grounded Theory Advisor | Constant comparison, theoretical sampling, theory development | HIGH |
| H4 | Narrative Analysis Specialist | Narrative inquiry, life history, autoethnography | HIGH |

### Extended Agents (5 Total)

#### B1: Systematic Literature Scout → Literature Review Strategist

**Added Capabilities**:
- Scoping reviews (JBI, PRISMA-ScR)
- Meta-synthesis (meta-ethnography, thematic synthesis)
- Realist synthesis (RAMESES)
- Narrative reviews (critical, integrative)
- Rapid reviews

#### C1: Research Design Consultant → Quantitative Design Consultant

**Changes**:
- Focused exclusively on quantitative research designs
- Split qualitative and mixed methods to C2 and C3
- Added paradigm_affinity: [quantitative]

#### E1: Statistical Analysis Guide → Quantitative Analysis Guide

**Added Capabilities**:
- Qualitative analysis methods (thematic, grounded theory, content, narrative)
- Bayesian statistics section
- Machine learning for research

#### E4: Analysis Code Generator

**Added Capabilities**:
- CAQDAS support: NVivo, ATLAS.ti, MAXQDA
- R qualitative packages: RQDA, qualitativeR
- Mixed methods visualization code

#### F4: Bias Detector → Bias & Trustworthiness Detector

**Added Capabilities**:
- Qualitative trustworthiness criteria (Lincoln & Guba)
  - Credibility, Transferability, Dependability, Confirmability
- Reflexivity guidelines
- COREQ, SRQR, GRAMMS checklists

### Core Infrastructure Changes

#### New Files Created

| File | Purpose |
|------|---------|
| `.claude/skills/research-coordinator/core/paradigm-detector.md` | Auto-detection rules and agent pack activation |
| `.claude/skills/research-agents/A5-paradigm-worldview-advisor/SKILL.md` | Paradigm/worldview selection |
| `.claude/skills/research-agents/C2-qualitative-design-consultant/SKILL.md` | Qualitative design support |
| `.claude/skills/research-agents/C3-mixed-methods-design-consultant/SKILL.md` | Mixed methods design |
| `.claude/skills/research-agents/C4-experimental-materials-developer/SKILL.md` | Experimental materials |
| `.claude/skills/research-agents/D1-sampling-strategy-advisor/SKILL.md` | Sampling strategies |
| `.claude/skills/research-agents/D2-interview-focus-group-specialist/SKILL.md` | Interviews/focus groups |
| `.claude/skills/research-agents/D3-observation-protocol-designer/SKILL.md` | Observation protocols |
| `.claude/skills/research-agents/D4-measurement-instrument-developer/SKILL.md` | Instrument development |
| `.claude/skills/research-agents/E2-qualitative-coding-specialist/SKILL.md` | Qualitative coding |
| `.claude/skills/research-agents/E3-mixed-methods-integration/SKILL.md` | Mixed methods integration |
| `.claude/skills/research-agents/H1-ethnographic-research-advisor/SKILL.md` | Ethnographic research |
| `.claude/skills/research-agents/H2-action-research-facilitator/SKILL.md` | Action research |

#### Modified Files

| File | Changes |
|------|---------|
| `.claude/skills/research-coordinator/SKILL.md` | v5.0.0 with Sisyphus protocol, paradigm detection |
| `.claude/skills/research-coordinator/references/agent-registry.yaml` | Complete rewrite for 33 agents |
| `.claude/skills/research-agents/05-systematic-literature-scout/SKILL.md` | Extended review types |
| `.claude/skills/research-agents/09-research-design-consultant/SKILL.md` | Quantitative focus |
| `.claude/skills/research-agents/10-statistical-analysis-guide/SKILL.md` | Added qualitative methods |
| `.claude/skills/research-agents/11-analysis-code-generator/SKILL.md` | CAQDAS support |
| `.claude/skills/research-agents/16-bias-detector/SKILL.md` | Trustworthiness criteria |
| `README.md` | Updated to v5.0.0 |
| `AGENTS.md` | AI-readable registry update |
| `CLAUDE.md` | Project instructions update |

### Research Types Now Supported

#### Quantitative Research
- Experimental designs (RCT, quasi-experimental)
- Survey research
- Meta-analysis and systematic reviews
- Correlational studies
- Psychometric validation

#### Qualitative Research (NEW)
- Phenomenology (descriptive, interpretive, hermeneutic)
- Grounded theory (Straussian, Charmazian, classic)
- Case study (single, multiple, intrinsic, instrumental)
- Ethnography (traditional, focused, critical, digital)
- Narrative inquiry (life history, autoethnography)
- Action research (PAR, CBPR)

#### Mixed Methods Research (NEW)
- Sequential explanatory
- Sequential exploratory
- Convergent parallel
- Embedded design
- Transformative frameworks

### Human Checkpoints (Updated)

| Level | Checkpoints | Action |
|-------|-------------|--------|
| 🔴 REQUIRED | CP_RESEARCH_DIRECTION, CP_THEORY_SELECTION, CP_METHODOLOGY_APPROVAL | User approval required |
| 🟠 RECOMMENDED | CP_ANALYSIS_PLAN, CP_QUALITY_REVIEW | Review recommended |
| 🟡 OPTIONAL | CP_VISUALIZATION_PREFERENCE, CP_RENDERING_METHOD | Defaults available |

### Validation

All 33 agents pass contract validation:

```bash
python scripts/validate_agents.py
# Summary: 33/33 agents passed validation
# ✅ All agents passed validation!
```

### Breaking Changes

- Agent IDs changed from numeric (01-21) to include category-based (A1-H4)
- Some agents split or renamed (see Extended Agents section)
- New required frontmatter fields: `upgrade_level`, `v3_integration`

### Migration from v4.x

1. **Agent Registry**: The 21 agents remain with original IDs; new agents use category IDs (A5, C2-C4, D1-D4, E2-E3, H1-H4)
2. **Paradigm Detection**: Automatically activates appropriate agent packs
3. **Sisyphus Protocol**: All workflows now include verification-before-completion
4. **Frontmatter**: All SKILL.md files require `upgrade_level` and `v3_integration` fields

---

## [3.2.0] - 2025-01-25

### Added

#### OMC (oh-my-claudecode) Integration
- **21 OMC Agent Definition Files** (`.omc/agents/research/01-21`)
  - Each agent has: tier, model, category, parallel_group, human_checkpoint, triggers
  - Follows OMC agent specification format

- **Human Checkpoint System** (`.omc/checkpoints/`)
  - `checkpoint-definitions.yaml`: 7 checkpoints across 3 levels
    - 🔴 REQUIRED: CP_RESEARCH_DIRECTION, CP_THEORY_SELECTION, CP_METHODOLOGY_APPROVAL
    - 🟠 RECOMMENDED: CP_ANALYSIS_PLAN, CP_QUALITY_REVIEW
    - 🟡 OPTIONAL: CP_VISUALIZATION_PREFERENCE, CP_RENDERING_METHOD
  - `checkpoint-handler.md`: Implementation protocol for checkpoint handling
  - `parallel-execution-rules.yaml`: 10 parallel execution groups with checkpoint boundaries

- **Model Routing Configuration** (`.omc/config/research-coordinator-routing.yaml`)
  - HIGH tier (Opus): #01, #02, #03, #09, #19 - Strategic decisions
  - MEDIUM tier (Sonnet): #04, #06, #10, #12, #15-18, #20, #21 - Standard analysis
  - LOW tier (Haiku): #05, #07, #08, #11, #13, #14 - Search, calculation, code
  - ~60% token savings compared to all-Opus approach

- **Research Orchestrator Skill** (`.omc/skills/research-orchestrator/SKILL.md`)
  - Coordinates Diverga with OMC execution modes
  - Agent-tier quick reference table
  - Integration with ultrawork, ecomode, ralph modes

- **Comprehensive Documentation** (`docs/omc-integration.md`)
  - 450+ line guide for OMC integration
  - Usage scenarios, configuration references
  - Migration guide and troubleshooting

### Changed

- **CLAUDE.md**: Added OMC Integration v3.2.0 section
- **SKILL.md**: Updated to v3.2.0 with OMC integration, model routing table, checkpoint references

### Core Principle

> **"인간이 할 일은 인간이, AI는 인간의 범주를 벗어난 것을 수행"**
> (Human decisions MUST be respected, AI only handles tasks beyond human scope)

### Compatibility

- **Backwards Compatible**: Works with Claude Code alone (no OMC required)
- **Enhanced with OMC**: Parallel execution, smart model routing, token efficiency

---

## [3.1.0] - Previous Release

- 21 research agents across 5 categories (A-E)
- VS-Research (Verbalized Sampling) methodology
- Nanobanana integration for visualizations
- Claude Code Skills system support

---

## File Structure (v5.0.0)

```
research-coordinator/
├── .claude/skills/
│   ├── research-coordinator/         # Master skill
│   │   ├── SKILL.md                  # v5.0.0 Sisyphus Edition
│   │   ├── core/
│   │   │   └── paradigm-detector.md  # Auto-detection rules
│   │   └── references/
│   │       └── agent-registry.yaml   # 33 agents
│   └── research-agents/              # 33 individual agents
│       ├── 01-21/                    # Original agents (extended)
│       ├── A5-paradigm-worldview-advisor/
│       ├── C2-qualitative-design-consultant/
│       ├── C3-mixed-methods-design-consultant/
│       ├── C4-experimental-materials-developer/
│       ├── D1-sampling-strategy-advisor/
│       ├── D2-interview-focus-group-specialist/
│       ├── D3-observation-protocol-designer/
│       ├── D4-measurement-instrument-developer/
│       ├── E2-qualitative-coding-specialist/
│       ├── E3-mixed-methods-integration/
│       ├── H1-ethnographic-research-advisor/
│       └── H2-action-research-facilitator/
├── .omc/                             # OMC Integration
│   ├── agents/research/              # OMC agent definitions
│   ├── checkpoints/                  # Human checkpoint system
│   ├── config/                       # Model routing
│   └── skills/                       # Research orchestrator
├── docs/
│   └── omc-integration.md            # OMC integration guide
├── scripts/
│   └── validate_agents.py            # Agent validation script
├── CHANGELOG.md                      # This file
├── CLAUDE.md                         # Project instructions
├── AGENTS.md                         # AI-readable registry
└── README.md
```

---

## Agent Summary (v5.0.0)

| Category | ID Range | Count | Tier Distribution |
|----------|----------|-------|-------------------|
| A: Foundation | A1-A5 (01-04 + A5) | 5 | 2 HIGH, 3 MEDIUM |
| B: Evidence | B1-B4 (05-08) | 4 | 2 MEDIUM, 2 LOW |
| C: Design | C1-C4 (09 + C2-C4) | 4 | 2 HIGH, 2 MEDIUM |
| D: Data Collection | D1-D4 | 4 | 4 MEDIUM |
| E: Analysis | E1-E4 (10-11 + E2-E3) | 4 | 2 HIGH, 2 MEDIUM |
| F: Quality | F1-F4 (12-16) | 4 | 1 MEDIUM, 3 LOW |
| G: Communication | G1-G4 (17-20) | 4 | 2 MEDIUM, 2 LOW |
| H: Specialized | H1-H4 | 4 | 3 HIGH, 1 MEDIUM |
| **Total** | | **33** | **11 HIGH, 14 MEDIUM, 8 LOW** |

---

## Usage (v5.0.0)

### Basic Mode
```bash
/research-coordinator
```

### With OMC (Enhanced Mode)
```bash
ulw: 문헌 검색해줘     # Maximum parallelism
eco: 통계 분석해줘     # Token efficient
ralph: 연구 설계해줘   # Persistence until done
```

### Paradigm-Specific Invocation
```
"현상학적 연구 설계해줘"      # → Qualitative pack activated (C2, E2, D2)
"혼합방법 연구 통합해줘"      # → Mixed methods pack activated (C3, E3)
"메타분석 효과크기 추출"      # → Quantitative pack activated (C1, E1, B3)
```

---

## Contributors

- Diverga v5.0.0 design based on oh-my-opencode Sisyphus pattern
- Benchmarked against: Agent Laboratory, LLM-SLR, Agentic Research Lab
- Implementation: Claude Opus 4.5 with OMC orchestration
- Architect Verification: Passed
