# AGENTS.md

> AI-readable documentation for Diverga v5.0 (Sisyphus Edition)

## Project Overview

**Diverga** is a Claude Code Skills-based AI research assistant system that breaks free from mode collapse through **Verbalized Sampling (VS) methodology**. It provides context-persistent support for the complete research lifecycle with a focus on **creative, defensible research choices**.

**Version**: 5.0.0 (Sisyphus Edition)
**Generated**: 2025-01-25
**Repository**: https://github.com/HosungYou/research-coordinator

---

## Core Philosophy

> "Human decisions remain with humans. AI handles what's beyond human scope."

- Strategic research decisions require human approval (checkpoints)
- AI prevents mode collapse through VS (Verbalized Sampling) methodology
- Context persistence eliminates re-explanation burden

---

## Architecture

### Directory Structure

```
research-coordinator/
├── .claude/skills/
│   ├── research-coordinator/          # Master coordinator
│   │   ├── SKILL.md                   # Main entry point (v4.0)
│   │   └── core/                      # Core systems
│   │       ├── project-state.md       # Context persistence
│   │       ├── pipeline-templates.md  # PRISMA workflows
│   │       ├── integration-hub.md     # Tool connections
│   │       ├── guided-wizard.md       # Conversation UX
│   │       └── auto-documentation.md  # Document generation
│   └── research-agents/               # 21 specialized agents
│       ├── 01-research-question-refiner/
│       ├── 02-theoretical-framework-architect/
│       └── ... (through 21)
├── docs/                              # Documentation
├── scripts/                           # Installation scripts
├── CONTRIBUTING.md                    # Contributor guide
├── CHANGELOG.md                       # Version history
└── README.md                          # Project overview
```

---

## Core Systems (v4.0)

### 1. Project State Management

**Location**: `.research/project-state.yaml`

Maintains research context across the entire lifecycle:
- Research question and PICO elements
- Theoretical framework and hypotheses
- Methodology decisions
- Integration status
- Decision audit trail

### 2. Pipeline Templates

Pre-configured workflows:
- **Systematic Review & Meta-Analysis**: PRISMA 2020 compliant, 8 stages
- **Experimental Study**: Pre-registered workflow
- **Survey Research**: Cross-sectional/longitudinal

### 3. Integration Hub

Available tools:
| Tool | Access | Purpose |
|------|--------|---------|
| Excel | Skill: ms-office-suite | Data extraction |
| PowerPoint | Skill: ms-office-suite | Presentations |
| Word | Skill: ms-office-suite | Manuscripts |
| R Scripts | Generated | Statistical analysis |
| Semantic Scholar | API | Literature search |
| Zotero | MCP | References |
| Nanobanana | API | AI visualization |

### 4. Guided Wizard

Conversation UX using `AskUserQuestion` tool:
- Explicit choice points for decisions
- Natural language between checkpoints
- Bilingual support (EN/KO)

### 5. Auto-Documentation

Generated documents:
- Decision Log (timestamped)
- PRISMA Checklist (auto-tracked)
- Methods Section Draft
- OSF Submission Package

---

## Agent Registry (v5.0)

### 27 Specialized Research Agents Across 8 Categories

Diverga v5.0 introduces comprehensive coverage of all research paradigms through 27 specialized agents organized into 8 functional categories.

---

### Category A: Research Foundation (5 agents)

Establishes theoretical and ethical foundations for research projects.

| ID | Agent | Purpose | Tier | Model |
|----|-------|---------|------|-------|
| A1 | Research Question Refiner | PICO/SPIDER formulation, question clarity | MEDIUM | sonnet |
| A2 | Theoretical Framework Architect | Theory selection, conceptual models, construct definition | HIGH | opus |
| A3 | Devil's Advocate | Critical review, Reviewer 2 simulation, assumption challenge | MEDIUM | sonnet |
| A4 | Research Ethics Advisor | IRB protocols, informed consent, ethical risk assessment | MEDIUM | sonnet |
| A5 | Paradigm & Worldview Advisor | Ontology, epistemology, positionality statements | HIGH | opus |

**Paradigm Coverage**: All paradigms (A5 is paradigm-agnostic)

---

### Category B: Literature & Evidence (4 agents)

Systematic evidence gathering, synthesis, and quality appraisal.

| ID | Agent | Purpose | Tier | Model |
|----|-------|---------|------|-------|
| B1 | Literature Review Strategist | PRISMA workflows, scoping reviews, meta-synthesis | MEDIUM | sonnet |
| B2 | Evidence Quality Appraiser | Risk of Bias (RoB), GRADE, quality scoring | MEDIUM | sonnet |
| B3 | Effect Size Extractor | Calculate/convert effect sizes, meta-analytic data | LOW | haiku |
| B4 | Research Radar | Monitor new publications, automated alerts | LOW | haiku |

**Paradigm Coverage**: Quantitative (B3), Qualitative (B1 meta-synthesis), Mixed (all)

---

### Category C: Study Design (4 agents)

Paradigm-specific design consultation for methodological rigor.

| ID | Agent | Purpose | Tier | Model |
|----|-------|---------|------|-------|
| C1 | Quantitative Design Consultant | RCTs, quasi-experimental, surveys, power analysis | MEDIUM | sonnet |
| C2 | Qualitative Design Consultant | Phenomenology, grounded theory, case study, ethnography | HIGH | opus |
| C3 | Mixed Methods Design Consultant | Sequential, convergent, embedded designs, integration | HIGH | opus |
| C4 | Experimental Materials Developer | Treatment protocols, control conditions, manipulation checks | MEDIUM | sonnet |

**Paradigm Coverage**: Paradigm-specific (C1, C2, C3), Experimental focus (C4)

---

### Category D: Data Collection (4 agents) [NEW in v5.0]

Comprehensive data collection strategy and instrument development.

| ID | Agent | Purpose | Tier | Model |
|----|-------|---------|------|-------|
| D1 | Sampling Strategy Advisor | Probability, purposive, theoretical sampling strategies | MEDIUM | sonnet |
| D2 | Interview & Focus Group Specialist | Interview protocols, probing techniques, transcription | MEDIUM | sonnet |
| D3 | Observation Protocol Designer | Structured observation, field notes, video analysis | MEDIUM | sonnet |
| D4 | Measurement Instrument Developer | Scale construction, validity evidence, reliability testing | MEDIUM | sonnet |

**Paradigm Coverage**: Quantitative (D1, D4), Qualitative (D2, D3), Mixed (all)

---

### Category E: Analysis (4 agents)

Paradigm-appropriate analytical strategies and implementation.

| ID | Agent | Purpose | Tier | Model |
|----|-------|---------|------|-------|
| E1 | Quantitative Analysis Guide | Frequentist, Bayesian, ML, assumptions checking | MEDIUM | sonnet |
| E2 | Qualitative Coding Specialist | Thematic analysis, grounded theory coding, NVivo/Atlas.ti | HIGH | opus |
| E3 | Mixed Methods Integration Specialist | Joint displays, meta-inferences, convergence analysis | HIGH | opus |
| E4 | Analysis Code Generator | R, Python, SPSS, Stata, CAQDAS scripts | MEDIUM | sonnet |

**Paradigm Coverage**: Paradigm-specific (E1, E2, E3), All (E4)

---

### Category F: Quality & Validation (4 agents)

Methodological rigor, reproducibility, and bias mitigation.

| ID | Agent | Purpose | Tier | Model |
|----|-------|---------|------|-------|
| F1 | Internal Consistency Checker | Logic verification, methodological alignment | LOW | haiku |
| F2 | Checklist Manager | PRISMA, CONSORT, COREQ, reporting standards | LOW | haiku |
| F3 | Reproducibility Auditor | Open Science Framework (OSF), code/data sharing | LOW | haiku |
| F4 | Bias & Trustworthiness Detector | Quantitative bias, qualitative trustworthiness criteria | MEDIUM | sonnet |

**Paradigm Coverage**: All paradigms (F4 adapts to paradigm)

---

### Category G: Publication & Communication (4 agents)

Academic writing, dissemination, and peer review response.

| ID | Agent | Purpose | Tier | Model |
|----|-------|---------|------|-------|
| G1 | Journal Matcher | Target journal selection, fit analysis | LOW | haiku |
| G2 | Academic Communicator | Plain language summaries, infographics | LOW | haiku |
| G3 | Peer Review Strategist | Response to reviewers, rebuttal letters | MEDIUM | sonnet |
| G4 | Pre-registration Composer | OSF pre-registration, registered reports | LOW | haiku |

**Paradigm Coverage**: All paradigms

---

### Category H: Specialized Approaches (2 agents) [NEW in v5.0]

Advanced qualitative and participatory research methodologies.

| ID | Agent | Purpose | Tier | Model |
|----|-------|---------|------|-------|
| H1 | Ethnographic Research Advisor | Fieldwork, thick description, cultural analysis | HIGH | opus |
| H2 | Action Research Facilitator | Participatory Action Research (PAR), CBPR, action cycles | MEDIUM | sonnet |

**Paradigm Coverage**: Qualitative/Participatory paradigms

---

## Paradigm Affinity Matrix

Guide for AI agents to select appropriate agents based on research paradigm.

### Quantitative Research

**Primary Agents**: A1-A4, B2, B3, C1, C4, D1, D4, E1, E4, F1-F3, G1-G4

**Typical Workflow**:
1. A1 (Research Question - PICO) → A2 (Theoretical Framework)
2. C1 (Study Design) → D1 (Sampling Strategy) → D4 (Measurement)
3. C4 (Experimental Materials) if RCT/Quasi-experimental
4. E1 (Statistical Analysis) → E4 (Code Generation)
5. F2 (CONSORT/STROBE Checklist) → G1 (Journal Matcher)

### Qualitative Research

**Primary Agents**: A1-A5, B1, B2, C2, D1-D3, E2, F2, F4, G1-G4, H1-H2

**Typical Workflow**:
1. A1 (Research Question - SPIDER) → A2 (Theoretical Framework) → A5 (Paradigm)
2. C2 (Qualitative Design) → D1 (Sampling) → D2 or D3 (Data Collection)
3. H1 (Ethnography) or H2 (Action Research) if specialized approach
4. E2 (Coding/Thematic Analysis) → E4 (CAQDAS Scripts)
5. F2 (COREQ/SRQR Checklist) → F4 (Trustworthiness) → G1 (Journal)

### Mixed Methods Research

**Primary Agents**: ALL agents, especially C3, E3

**Typical Workflow**:
1. A1 → A2 → A5 (Paradigm positioning)
2. C3 (Mixed Design) determines sequence
3. **Sequential Explanatory**: QUAN (C1, E1) → QUAL (C2, E2) → E3 (Integration)
4. **Convergent Parallel**: QUAN (C1, E1) + QUAL (C2, E2) → E3 (Integration)
5. **Embedded**: Primary strand (C1 or C2) + embedded (D2, D3, E2)
6. F2 (Mixed Methods Reporting Standards) → G1 (Journal)

### Ethnographic Research

**Primary Agents**: A1-A5, C2, D3, E2, H1, F4, G2

**Specialized Workflow**:
1. A1 (Ethnographic Question) → A5 (Paradigm - Interpretive/Critical)
2. H1 (Ethnographic Design) → D3 (Observation Protocol) + D2 (Interviews)
3. E2 (Cultural Coding) → G2 (Public Engagement)
4. F4 (Prolonged Engagement, Member Checking)

### Action Research / CBPR

**Primary Agents**: A1-A5, C2, H2, D2, E2, F4, G2

**Specialized Workflow**:
1. H2 (Action Research Cycles) → A1 (Community-defined question)
2. H2 (Participatory Design) → D1 (Community-based sampling) → D2 (Group protocols)
3. E2 (Collaborative coding) → H2 (Action planning)
4. G2 (Community dissemination) + F4 (Catalytic validity)

---

## Sisyphus Protocol

**v5.0 Core Enhancement**: Continuation enforcement for comprehensive research support.

### Philosophy

"Diverga never says 'done' prematurely. Like Sisyphus pushing the boulder, we persist until the research task is genuinely complete."

### Completion Criteria by Paradigm

#### Quantitative Research Completion

- [ ] **Research Design**: RCT/Quasi/Survey design documented with justification
- [ ] **Power Analysis**: Sample size calculation with effect size, alpha, power
- [ ] **Measurement**: Instruments selected/developed with validity evidence
- [ ] **Analysis Plan**: Statistical tests specified with assumptions checking
- [ ] **Reproducibility**: Analysis code (R/Python) generated and documented
- [ ] **Reporting Standards**: CONSORT/STROBE checklist 100% complete

**Incomplete if**: Any checkbox unchecked, analysis plan lacks robustness checks.

#### Qualitative Research Completion

- [ ] **Paradigm Statement**: Ontology, epistemology, positionality clearly articulated
- [ ] **Methodological Coherence**: Design, data collection, analysis aligned with paradigm
- [ ] **Purposive Sampling**: Strategy justified with saturation criteria
- [ ] **Data Collection Protocols**: Interview guides/observation frameworks with rigor
- [ ] **Coding Framework**: Codebook developed with intercoder reliability plan
- [ ] **Trustworthiness**: Credibility, transferability, dependability, confirmability addressed
- [ ] **Reporting Standards**: COREQ/SRQR checklist 100% complete

**Incomplete if**: Paradigm mismatch detected, trustworthiness criteria absent.

#### Mixed Methods Completion

- [ ] **Integration Rationale**: Why mixing justified (complementarity, expansion, etc.)
- [ ] **Design Diagram**: Visual representation of QUAN → QUAL or convergent flow
- [ ] **Interface Points**: Where/how integration occurs specified
- [ ] **Joint Displays**: Tables/figures showing QUAN + QUAL integration
- [ ] **Meta-inferences**: Conclusions drawn from integrated findings
- [ ] **Reporting Standards**: Mixed Methods APPRAISAL checklist complete

**Incomplete if**: Integration is superficial (side-by-side, not synthesized).

### Agent Orchestration Patterns

**Pattern 1: Parallel Execution for Independence**

When agents have NO dependencies, run in parallel:

```
# Example: Literature + Ethics review (independent tasks)
[Task: B1-LiteratureScout] + [Task: A4-EthicsAdvisor]
```

**Pattern 2: Sequential for Dependencies**

When Agent B needs Agent A's output:

```
# Example: Design before measurement
[Task: C1-QuantDesign] → wait for completion → [Task: D4-Measurement]
```

**Pattern 3: Validation Loop**

After major agent completion, invoke F1-InternalConsistency:

```
# Example: After statistical analysis
[Task: E1-StatGuide] → [Task: F1-ConsistencyCheck] → if FAIL → [Task: E1 re-run]
```

**Pattern 4: Paradigm-Specific Chains**

For qualitative research (sequential saturation-dependent):

```
[Task: C2-QualDesign] → [Task: D1-Sampling] → [Task: D2-Interviews] →
[Task: E2-Coding] → [Task: F4-Trustworthiness]
```

### Continuation Enforcement Rules

1. **Never claim completion without checklist verification**
   - AI MUST read paradigm-specific completion criteria
   - AI MUST verify EVERY checkbox is complete
   - AI MUST run F1-InternalConsistency if ANY doubt exists

2. **Detect and flag superficial outputs**
   - "Effect size calculated" → Verify: Is it Cohen's d? Hedges' g? Properly interpreted?
   - "Thematic analysis done" → Verify: Codebook? Intercoder reliability? Saturation?
   - "Mixed methods integration" → Verify: Joint display exists? Meta-inferences drawn?

3. **Auto-invoke quality agents**
   - After C1/C2/C3 → Invoke F1 (Consistency Check)
   - After E1/E2 → Invoke F4 (Bias/Trustworthiness)
   - Before claiming "project complete" → Invoke F2 (Checklist Manager)

4. **Handle user "stop" requests gracefully**
   - If user says "stop" mid-process → Save state to `.research/project-state.yaml`
   - Show incomplete checklist with visual progress: "✅✅✅⬜⬜⬜ (3/6 complete)"
   - Offer: "Resume anytime with 'continue my research project'"

---

## VS-Research Methodology

**Purpose**: Prevent mode collapse (AI always recommending the same thing)

### T-Score (Typicality Score)

| T-Score | Label | Meaning |
|---------|-------|---------|
| ≥ 0.7 | Common | Highly typical, safe but limited novelty |
| 0.4-0.7 | Moderate | Balanced risk-novelty |
| 0.2-0.4 | Innovative | Novel, requires strong justification |
| < 0.2 | Experimental | Highly novel, high risk/reward |

### 3-Stage Process (v5.0)

1. **Context & Modal Identification**: Understand context, identify "obvious" recommendations
2. **Divergent Exploration**: Generate alternatives with T-Scores (paradigm-aware)
3. **Selection & Execution**: Human chooses, AI executes with rigor

**v5.0 Enhancement**: T-Scores now paradigm-contextualized (e.g., phenomenology is T=0.7 for qualitative, T=0.3 for quantitative).

---

## Human Checkpoints

| Level | Checkpoints | Behavior |
|-------|-------------|----------|
| 🔴 REQUIRED | CP_RESEARCH_DIRECTION, CP_THEORY_SELECTION, CP_METHODOLOGY_APPROVAL | Must pause for user approval |
| 🟠 RECOMMENDED | CP_ANALYSIS_PLAN, CP_QUALITY_REVIEW | Should pause, can be skipped |
| 🟡 OPTIONAL | CP_VISUALIZATION_PREFERENCE | Defaults available |

---

## Auto-Trigger Keywords (v5.0)

Extended keyword detection for 27 agents across 8 categories.

### Category A: Research Foundation

| Keywords | Korean | Agent |
|----------|--------|-------|
| research question, PICO, SPIDER, formulation | 연구 질문, 연구문제 | A1 |
| theoretical framework, conceptual model, theory | 이론, 개념적 모형, 이론적 틀 | A2 |
| critique, reviewer 2, devil's advocate, critical | 비판, 리뷰어, 반대 의견 | A3 |
| IRB, ethics, informed consent, risk assessment | 윤리, IRB, 동의서 | A4 |
| paradigm, ontology, epistemology, worldview, positivism | 패러다임, 존재론, 인식론, 세계관 | A5 |

### Category B: Literature & Evidence

| Keywords | Korean | Agent |
|----------|--------|-------|
| literature review, PRISMA, scoping review, meta-synthesis | 문헌 검토, 체계적 리뷰, 문헌고찰 | B1 |
| quality appraisal, risk of bias, GRADE, RoB | 질 평가, 편향 위험 | B2 |
| effect size, Cohen's d, Hedges g, odds ratio | 효과크기 | B3 |
| publication alerts, new research, monitoring | 출판 알림, 신규 연구 | B4 |

### Category C: Study Design

| Keywords | Korean | Agent |
|----------|--------|-------|
| RCT, quasi-experimental, survey, power analysis | 무작위 대조, 준실험, 설문, 검정력 | C1 |
| phenomenology, grounded theory, case study, narrative | 현상학, 근거이론, 사례연구 | C2 |
| mixed methods, sequential, convergent, embedded | 혼합연구, 순차적, 수렴적 | C3 |
| experimental materials, treatment, manipulation check | 실험 자료, 처치, 조작 점검 | C4 |

### Category D: Data Collection

| Keywords | Korean | Agent |
|----------|--------|-------|
| sampling, probability, purposive, theoretical sampling | 표집, 확률, 의도적, 이론적 표집 | D1 |
| interview, focus group, probing, transcription | 인터뷰, 초점집단, 전사 | D2 |
| observation, field notes, video analysis | 관찰, 현장노트, 영상 분석 | D3 |
| scale, instrument, validity, reliability, Cronbach | 척도, 도구, 타당도, 신뢰도 | D4 |

### Category E: Analysis

| Keywords | Korean | Agent |
|----------|--------|-------|
| statistics, ANOVA, regression, Bayesian, frequentist | 통계, 분산분석, 회귀, 베이지안 | E1 |
| coding, thematic analysis, NVivo, Atlas.ti, saturation | 코딩, 주제분석, 포화 | E2 |
| integration, joint display, meta-inference, convergence | 통합, 메타추론, 수렴 | E3 |
| R code, Python, SPSS, Stata, CAQDAS | R 코드, 파이썬, SPSS | E4 |

### Category F: Quality & Validation

| Keywords | Korean | Agent |
|----------|--------|-------|
| consistency, logic, alignment, coherence | 일관성, 논리, 정합성 | F1 |
| CONSORT, STROBE, COREQ, SRQR, checklist | 체크리스트, 보고 기준 | F2 |
| reproducibility, OSF, open science, code sharing | 재현성, 오픈사이언스 | F3 |
| bias, trustworthiness, credibility, transferability | 편향, 신뢰성, 전이가능성 | F4 |

### Category G: Publication & Communication

| Keywords | Korean | Agent |
|----------|--------|-------|
| journal, submission, impact factor, fit analysis | 저널, 투고, 영향력 지수 | G1 |
| plain language, infographic, public engagement | 쉬운 언어, 인포그래픽 | G2 |
| reviewer, peer review, rebuttal, response letter | 리뷰어, 동료평가, 반박 | G3 |
| pre-registration, OSF, registered report | 사전등록, 등록보고서 | G4 |

### Category H: Specialized Approaches

| Keywords | Korean | Agent |
|----------|--------|-------|
| ethnography, fieldwork, thick description, culture | 민족지학, 현장연구, 두터운 기술 | H1 |
| action research, PAR, CBPR, participatory, cycles | 실행연구, 참여적 실행연구 | H2 |

---

## Model Routing (OMC Integration)

Updated for 27 agents in v5.0.

| Tier | Model | Agents | Use Cases |
|------|-------|--------|-----------|
| HIGH | Opus | A2, A5, C2, C3, E2, E3, H1 | Strategic decisions, paradigm selection, qualitative depth |
| MEDIUM | Sonnet | A1, A3, A4, B1, B2, C1, C4, D1-D4, E1, E4, F4, G3, H2 | Core research tasks, standard workflows |
| LOW | Haiku | B3, B4, F1-F3, G1, G2, G4 | Routine tasks, checklist management, quick calculations |

### Temperature Settings by Agent Type

| Agent Category | Temperature | Rationale |
|----------------|-------------|-----------|
| A (Foundation) | 0.3-0.5 | Strategic but needs creativity for alternatives |
| B (Literature) | 0.1-0.3 | Precision in evidence synthesis |
| C (Design) | 0.5-0.7 | Balance rigor with design creativity |
| D (Collection) | 0.3-0.5 | Structured but adaptive protocols |
| E (Analysis) | 0.1-0.3 | Analytical precision required |
| F (Quality) | 0.1 | Maximum consistency for validation |
| G (Publication) | 0.5-0.7 | Creative communication, strategic messaging |
| H (Specialized) | 0.7-0.9 | High contextual sensitivity, cultural nuance |

---

## Key Files for AI Understanding

| File | Purpose |
|------|---------|
| `SKILL.md` | Master coordinator entry point |
| `core/project-state.md` | Context persistence schema |
| `core/pipeline-templates.md` | PRISMA workflow definitions |
| `core/integration-hub.md` | Tool connection guide |
| `.research/project-state.yaml` | Active project context (runtime) |
| `.research/decision-log.yaml` | Decision audit trail (runtime) |

---

## Usage Patterns

### Starting a Project
```
User: "I want to conduct a systematic review on AI in education"
→ Activates guided wizard
→ Creates .research/project-state.yaml
→ Begins Stage 1: Protocol Development
```

### Resuming a Project
```
User: "Continue my research project"
→ Reads .research/project-state.yaml
→ Injects context into conversation
→ Resumes from current stage
```

### Requesting Tool Integration
```
User: "Create an Excel spreadsheet for data extraction"
→ Uses ms-office-suite:excel skill
→ Generates formatted template
```

---

## Research Workflows by Paradigm (v5.0)

Detailed agent orchestration sequences for common research types.

### Workflow 1: Quantitative Systematic Review & Meta-Analysis

**Stages and Agents**:

1. **Protocol Development** (Stage 1)
   - A1 (PICO question) → A2 (Theoretical framework)
   - B1 (PRISMA protocol) → G4 (Pre-registration)
   - **Checkpoint**: Research direction approval

2. **Literature Search** (Stage 2-3)
   - B1 (Search strategy) → [Execute searches]
   - B3 (Extract effect sizes) → B2 (Quality appraisal)

3. **Statistical Analysis** (Stage 4)
   - E1 (Meta-analytic model selection: Fixed vs. Random)
   - E1 (Heterogeneity: I², τ²)
   - E1 (Publication bias: Funnel plot, Egger's test)
   - E4 (R code generation: metafor package)

4. **Quality & Reporting** (Stage 5)
   - F1 (Internal consistency) → F2 (PRISMA checklist)
   - F3 (Reproducibility: OSF upload)

5. **Publication** (Stage 6)
   - G1 (Journal matcher) → G2 (Plain language summary)

**Total Agents**: 10 (A1, A2, B1, B2, B3, E1, E4, F1, F2, G1, G2, G4)

---

### Workflow 2: Qualitative Phenomenological Study

**Stages and Agents**:

1. **Research Foundations** (Stage 1)
   - A1 (SPIDER question) → A5 (Paradigm: Interpretive phenomenology)
   - A2 (Theoretical framework: Lived experience)
   - **Checkpoint**: Paradigm and theory alignment

2. **Study Design** (Stage 2)
   - C2 (Phenomenological design: Descriptive vs. Interpretive)
   - D1 (Purposive sampling: Criterion-based)
   - D2 (Interview protocol: Open-ended, probing)

3. **Data Collection** (Stage 3)
   - D2 (Interview guide development)
   - [Execute interviews - researcher task]
   - D2 (Transcription guidance)

4. **Data Analysis** (Stage 4)
   - E2 (Phenomenological coding: Horizonalization → Themes)
   - E2 (Essence statements, composite descriptions)
   - E4 (NVivo workflow if needed)

5. **Trustworthiness** (Stage 5)
   - F4 (Credibility: Member checking, peer debriefing)
   - F4 (Transferability: Thick description)
   - F1 (Coherence check: Paradigm-data-interpretation)

6. **Reporting** (Stage 6)
   - F2 (COREQ checklist) → G1 (Journal matcher)
   - G2 (Visual representation of themes)

**Total Agents**: 11 (A1, A2, A5, C2, D1, D2, E2, E4, F1, F2, F4, G1, G2)

---

### Workflow 3: Mixed Methods Explanatory Sequential Design

**Stages and Agents**:

1. **Integration Rationale** (Stage 1)
   - A1 (Research question: Quantitative + Qualitative)
   - C3 (Mixed methods design: Sequential explanatory)
   - A5 (Paradigm: Pragmatism)
   - **Checkpoint**: Integration justification approved

2. **QUANTITATIVE Phase** (Stage 2)
   - C1 (Survey design) → D1 (Probability sampling)
   - D4 (Scale development/selection)
   - E1 (Regression/ANOVA) → E4 (Code generation)

3. **Interface Point** (Stage 3)
   - E3 (Identify QUAN findings needing explanation)
   - C3 (Design QUAL phase based on QUAN results)

4. **QUALITATIVE Phase** (Stage 4)
   - D1 (Purposive sampling: Based on QUAN outliers/extremes)
   - D2 (Interview protocol: Explain QUAN patterns)
   - E2 (Thematic analysis)

5. **Integration** (Stage 5)
   - E3 (Joint display: QUAN variables × QUAL themes)
   - E3 (Meta-inferences: How QUAL explains QUAN)
   - F1 (Coherence check)

6. **Reporting** (Stage 6)
   - F2 (Mixed Methods APPRAISAL) → G1 (Journal)
   - G2 (Visual: Flow diagram + joint display)

**Total Agents**: 13 (A1, A5, C1, C3, D1, D2, D4, E1, E2, E3, E4, F1, F2, G1, G2)

---

### Workflow 4: Ethnographic Fieldwork Study

**Stages and Agents**:

1. **Research Foundations** (Stage 1)
   - A1 (Ethnographic question) → A5 (Paradigm: Interpretive/Critical)
   - H1 (Ethnographic design: Focus on culture, setting selection)
   - **Checkpoint**: Cultural access and ethical considerations

2. **Fieldwork Planning** (Stage 2)
   - H1 (Fieldwork strategy: Emic/etic perspectives)
   - D3 (Observation protocol: Structured vs. unstructured)
   - D2 (Interview protocol: Ethnographic interviews)
   - A4 (Ethics: Informed consent in naturalistic settings)

3. **Data Collection** (Stage 3)
   - [Execute fieldwork - researcher immersion]
   - D3 (Field note guidance: Descriptive, reflective, analytic)
   - H1 (Prolonged engagement monitoring)

4. **Data Analysis** (Stage 4)
   - E2 (Cultural coding: Patterns, norms, symbols)
   - H1 (Thick description development)
   - E4 (Atlas.ti workflow if needed)

5. **Trustworthiness** (Stage 5)
   - F4 (Prolonged engagement, persistent observation)
   - F4 (Triangulation: Observations + interviews + artifacts)
   - H1 (Cultural member checking)

6. **Reporting & Dissemination** (Stage 6)
   - G2 (Public engagement: Community presentations)
   - F2 (Ethnographic reporting standards)
   - G1 (Journal: Cultural anthropology, qualitative inquiry)

**Total Agents**: 12 (A1, A4, A5, D2, D3, E2, E4, F2, F4, G1, G2, H1)

---

### Workflow 5: Participatory Action Research (PAR)

**Stages and Agents**:

1. **Community Engagement** (Stage 1)
   - H2 (PAR design: Identify community partners)
   - A1 (Research question: Co-created with community)
   - A5 (Paradigm: Critical/Transformative)
   - **Checkpoint**: Community approval and co-ownership

2. **Collaborative Planning** (Stage 2)
   - H2 (Action research cycles: Plan → Act → Observe → Reflect)
   - D1 (Sampling: Community-based recruitment)
   - D2 (Focus group protocol: Participatory methods)

3. **Cycle 1: Action & Observation** (Stage 3)
   - [Implement intervention - community-led]
   - D3 (Observation: Community members as co-researchers)
   - H2 (Action documentation)

4. **Cycle 1: Reflection & Analysis** (Stage 4)
   - E2 (Collaborative coding: Community members participate)
   - H2 (Reflection sessions: What worked? What didn't?)

5. **Cycle 2+: Iteration** (Stage 5)
   - H2 (Revised action plan based on Cycle 1 learning)
   - [Repeat Cycle 2, 3... until change achieved]

6. **Trustworthiness & Dissemination** (Stage 6)
   - F4 (Catalytic validity: Did research create change?)
   - G2 (Community dissemination: Accessible formats)
   - F2 (PAR reporting standards)

**Total Agents**: 10 (A1, A5, D1, D2, D3, E2, F2, F4, G2, H2)

---

## AI Orchestration Guidelines (Sisyphus Protocol)

**For Claude Code and AI assistants using Diverga v5.0**

### 1. Detecting Research Paradigm

**ALWAYS determine paradigm FIRST before agent selection.**

Read user message for paradigm indicators:

| Indicator | Paradigm |
|-----------|----------|
| RCT, quasi-experimental, survey, effect size, power analysis | Quantitative |
| Phenomenology, grounded theory, lived experience, meaning | Qualitative |
| Sequential, convergent, integration, joint display | Mixed Methods |
| Culture, fieldwork, thick description, emic/etic | Ethnographic |
| Community, participatory, action cycles, catalytic validity | Action Research |

**If unclear**, invoke **A5-Paradigm Advisor** FIRST to clarify.

### 2. Agent Selection Logic

```
IF paradigm == "Quantitative":
    Use agents: A1-A4, B2-B3, C1, C4, D1, D4, E1, E4, F1-F3, G1-G4

ELIF paradigm == "Qualitative":
    Use agents: A1-A5, B1, C2, D1-D3, E2, F2, F4, G1-G4
    IF specialized == "Ethnography":
        Add: H1
    ELIF specialized == "Action Research":
        Add: H2

ELIF paradigm == "Mixed Methods":
    Use agents: ALL (emphasize C3, E3 for integration)
```

### 3. Parallel vs. Sequential Execution

**Parallel Execution** (use multiple Task calls in ONE message):
- Independent agents with NO data dependencies
- Example: `[Task: B1-LitReview] + [Task: A4-Ethics]`

**Sequential Execution** (wait for previous Task completion):
- When Agent B needs Agent A's output
- Example: `[Task: C1-Design] → [WAIT] → [Task: D4-Measurement]`

### 4. Continuation Enforcement

**NEVER claim "done" until ALL checkboxes complete.**

After ANY major agent invocation:
1. Read paradigm-specific completion criteria (see Sisyphus Protocol section)
2. Verify EVERY checkbox is complete
3. If ANY unchecked → Continue working
4. If user says "stop" → Save state to `.research/project-state.yaml` and show progress: "✅✅✅⬜⬜⬜ (3/6 complete)"

### 5. Quality Agent Auto-Invocation

**Mandatory quality checks** (run automatically, don't ask permission):

| After Agent | Auto-Invoke | Purpose |
|-------------|-------------|---------|
| C1/C2/C3 (Design) | F1 (Consistency) | Check methodological coherence |
| E1/E2 (Analysis) | F4 (Bias/Trustworthiness) | Validate rigor |
| Any completion claim | F2 (Checklist Manager) | Verify reporting standards |

### 6. Handling Incomplete Work

If agent output is superficial, AI MUST:
1. Detect superficiality (e.g., "Effect size: d=0.5" without interpretation)
2. Re-invoke agent with explicit prompt: "Provide FULL interpretation: What does d=0.5 mean? Is it small/medium/large? Practical significance?"
3. Validate output meets depth criteria

### 7. State Persistence

**Always update** `.research/project-state.yaml` after:
- Paradigm selection (A5)
- Research question finalization (A1)
- Design approval (C1/C2/C3)
- Analysis completion (E1/E2)

**Format**:
```yaml
project:
  paradigm: "Qualitative - Phenomenology"
  research_question: "What are the lived experiences of..."
  current_stage: "Data Analysis (E2 in progress)"
  completion_percentage: 65
  completed_agents:
    - A1: "SPIDER question formulated"
    - A5: "Interpretive phenomenology selected"
    - C2: "Descriptive phenomenology design"
    - D1: "Criterion-based sampling (n=12)"
    - D2: "Interview protocol developed"
  pending_agents:
    - E2: "Phenomenological coding (in progress)"
    - F4: "Trustworthiness criteria"
    - F2: "COREQ checklist"
```

### 8. Error Recovery

If agent execution fails:
1. Log error to `.research/error-log.yaml`
2. Attempt recovery: Try lower model tier (Opus → Sonnet → Haiku)
3. If persistent failure: Notify user with fallback options
4. NEVER silently skip failed agents

### 9. User Communication Style

- **Progress Updates**: Show visual progress bars for multi-stage workflows
- **Agent Activity**: "🔄 Invoking B1-Literature Strategist (Sonnet)..." then "✅ B1 complete"
- **Checkpoints**: Use `AskUserQuestion` tool for REQUIRED checkpoints (🔴)
- **Completion**: "✅ All 6 completion criteria met. Research project complete!"

### 10. Bilingual Support (EN/KO)

Detect user language:
- If Korean detected → Respond in Korean, use Korean keywords for triggers
- If English → Respond in English
- Agent invocations → Always English (internal)
- User-facing outputs → Match user language

---

*This file enables AI assistants to understand Diverga v5.0's architecture and operate effectively within it.*
