# Diverga Agent Reference (v6.5)

## Complete Agent Registry (44 Agents in 9 Categories)

| ID | Agent | Category | Model | Checkpoint |
|----|-------|----------|-------|------------|
| A1 | research-question-refiner | Foundation | Opus | 🔴 CP_RESEARCH_DIRECTION |
| A2 | theoretical-framework-architect | Foundation | Opus | 🔴 CP_THEORY_SELECTION |
| A3 | devils-advocate | Foundation | Opus | - |
| A4 | research-ethics-advisor | Foundation | Sonnet | 🔴 CP_METHODOLOGY_APPROVAL |
| A5 | paradigm-worldview-advisor | Foundation | Opus | 🔴 CP_PARADIGM_SELECTION |
| A6 | conceptual-framework-visualizer | Foundation | Sonnet | 🟡 CP_VISUALIZATION_PREFERENCE |
| B1 | systematic-literature-scout | Evidence | Sonnet | - |
| B2 | evidence-quality-appraiser | Evidence | Sonnet | - |
| B3 | effect-size-extractor | Evidence | Haiku | - |
| B4 | research-radar | Evidence | Haiku | - |
| C1 | quantitative-design-consultant | Design | Opus | 🔴 CP_METHODOLOGY_APPROVAL |
| C2 | qualitative-design-consultant | Design | Opus | 🔴 CP_METHODOLOGY_APPROVAL |
| C3 | mixed-methods-design-consultant | Design | Opus | 🔴 CP_METHODOLOGY_APPROVAL |
| C4 | experimental-materials-developer | Design | Sonnet | - |
| D1 | sampling-strategy-advisor | Data Collection | Sonnet | - |
| D2 | interview-focus-group-specialist | Data Collection | Sonnet | - |
| D3 | observation-protocol-designer | Data Collection | Haiku | - |
| D4 | measurement-instrument-developer | Data Collection | Opus | 🔴 CP_METHODOLOGY_APPROVAL |
| E1 | quantitative-analysis-guide | Analysis | Opus | 🟠 CP_ANALYSIS_PLAN |
| E2 | qualitative-coding-specialist | Analysis | Opus | - |
| E3 | mixed-methods-integration | Analysis | Opus | 🟠 CP_INTEGRATION_STRATEGY |
| E4 | analysis-code-generator | Analysis | Haiku | - |
| E5 | sensitivity-analysis-designer | Analysis | Sonnet | - |
| F1 | internal-consistency-checker | Quality | Haiku | - |
| F2 | checklist-manager | Quality | Haiku | - |
| F3 | reproducibility-auditor | Quality | Sonnet | - |
| F4 | bias-trustworthiness-detector | Quality | Sonnet | - |
| G1 | journal-matcher | Communication | Sonnet | - |
| G2 | academic-communicator | Communication | Sonnet | - |
| G3 | peer-review-strategist | Communication | Opus | 🟠 CP_RESPONSE_APPROVAL |
| G4 | preregistration-composer | Communication | Sonnet | 🟠 CP_PREREGISTRATION_APPROVAL |
| H1 | ethnographic-research-advisor | Specialized | Opus | 🔴 CP_METHODOLOGY_APPROVAL |
| H2 | action-research-facilitator | Specialized | Opus | 🔴 CP_METHODOLOGY_APPROVAL |
| I0 | scholar-agent-orchestrator | Systematic Review | Opus | 🟡 SCH_PRISMA_GENERATION |
| I1 | paper-retrieval-agent | Systematic Review | Sonnet | 🔴 SCH_DATABASE_SELECTION |
| I2 | screening-assistant | Systematic Review | Sonnet | 🔴 SCH_SCREENING_CRITERIA |
| I3 | rag-builder | Systematic Review | Haiku | 🟠 SCH_RAG_READINESS |

---

## Category A: Foundation (6 Agents)

Establishes theoretical and ethical foundations for research projects.

### A1. Research Question Refiner 🔬

**Purpose**: Develop specific, testable research questions from vague ideas

**Trigger Keywords**: 연구 질문, research question, PICO, SPIDER, FINER

**Core Functions**:
- PICO (Quantitative) / SPIDER (Qualitative) / FINER framework application
- Narrow/Medium/Wide scope options
- Testability assessment

**Input Requirements**:
```yaml
Required:
  - Initial idea: "Topic you want to research"
Optional:
  - Research type: "Quantitative/Qualitative/Mixed"
  - Field: "Education/Psychology/Business, etc."
```

**Output**: PICO/SPIDER analysis + 3 refined question options with T-Scores

**Checkpoint**: 🔴 CP_RESEARCH_DIRECTION

---

### A2. Theoretical Framework Architect 🏛️

**Purpose**: Systematize theoretical foundation and build conceptual models

**Trigger Keywords**: 이론적 프레임워크, theoretical framework, conceptual model, theory

**Core Functions**:
- Theory Map creation with VS methodology
- Conceptual model visualization
- Hypothesis derivation logic

**Input Requirements**:
```yaml
Required:
  - Research question: "Refined research question"
Optional:
  - Related theories: "Known theories"
  - Key variables: "Main variables"
```

**Output**: Theory comparison table + Integrated conceptual model + Hypothesis system

**Checkpoint**: 🔴 CP_THEORY_SELECTION

---

### A3. Devil's Advocate 😈

**Purpose**: Identify weaknesses and potential criticisms proactively

**Trigger Keywords**: 비판, critique, Reviewer 2, weaknesses, counterarguments

**Core Functions**:
- Validity threat identification
- Reviewer 2 simulation
- Alternative explanations

**Output**: Validity threat matrix + Mock review + Response strategies

---

### A4. Research Ethics Advisor ⚖️

**Purpose**: Guide ethical research conduct

**Trigger Keywords**: 윤리, IRB, ethics, informed consent, privacy

**Core Functions**:
- Belmont Report principles check
- IRB application support
- Consent form templates

**Output**: Ethics checklist + Risk assessment + IRB guide

**Checkpoint**: 🔴 CP_METHODOLOGY_APPROVAL

---

### A5. Paradigm & Worldview Advisor 🌐

**Purpose**: Guide paradigm selection and worldview positioning

**Trigger Keywords**: 패러다임, paradigm, ontology, epistemology, positionality

**Core Functions**:
- Quantitative/Qualitative/Mixed methods guidance
- Worldview articulation (Positivist, Interpretive, Critical, Pragmatic)
- Positionality statement support

**Output**: Paradigm recommendation with rationale + Worldview statement template

**Checkpoint**: 🔴 CP_PARADIGM_SELECTION

---

### A6. Conceptual Framework Visualizer 📊

**Purpose**: Create visual representations of conceptual frameworks

**Trigger Keywords**: 개념적 프레임워크, conceptual framework, diagram, visualization

**Core Functions**:
- Code-First approach (Mermaid, Graphviz, NetworkX, D3.js)
- Academic Modern color palette
- Publication-ready figures

**Output**: Visual framework diagram + Code + Caption

**Checkpoint**: 🟡 CP_VISUALIZATION_PREFERENCE

---

## Category B: Evidence (4 Agents)

Systematic evidence gathering, synthesis, and quality appraisal.

### B1. Systematic Literature Scout 📚

**Purpose**: Develop PRISMA-compliant systematic search strategies

**Trigger Keywords**: 문헌 검색, PRISMA, systematic review, search strategy

**Core Functions**:
- Database selection guide
- Boolean search query construction
- Inclusion/exclusion criteria

**Output**: Database-specific queries + Selection criteria + PRISMA flow draft

---

### B2. Evidence Quality Appraiser ⭐

**Purpose**: Assess methodological quality of individual studies

**Trigger Keywords**: 품질 평가, RoB, GRADE, quality assessment

**Core Functions**:
- RoB 2.0 (RCT), ROBINS-I (non-randomized)
- Newcastle-Ottawa Scale (observational)
- GRADE evidence levels

**Output**: Quality checklist + Domain ratings + Overall quality grade

---

### B3. Effect Size Extractor 📊

**Purpose**: Calculate and convert effect sizes from various statistics

**Trigger Keywords**: 효과크기, effect size, Cohen's d, OR, correlation

**Core Functions**:
- 32+ statistic conversions
- Confidence intervals, variance calculation
- Meta-analysis data formatting

**Output**: Conversion results + Formulas + Interpretation guide

---

### B4. Research Radar 📡

**Purpose**: Monitor research trends and identify key papers

**Trigger Keywords**: 최신 연구, trends, seminal work, citations

**Core Functions**:
- Citation network analysis
- Time-series trends
- Hot topic identification

**Output**: Key paper list + Trend graphs + Research gap analysis

---

## Category C: Design (4 Agents)

Paradigm-specific design consultation for methodological rigor.

### C1. Quantitative Design Consultant 🎯

**Purpose**: Guide quantitative research design selection

**Trigger Keywords**: 연구 설계, RCT, quasi-experimental, survey design, power analysis

**Core Functions**:
- Design type decision tree
- Validity threat analysis
- Control strategy recommendations
- Power analysis guidance

**Output**: Design comparison + Recommended design + Validity matrix

**Checkpoint**: 🔴 CP_METHODOLOGY_APPROVAL

---

### C2. Qualitative Design Consultant 🔍

**Purpose**: Guide qualitative research design

**Trigger Keywords**: 현상학, phenomenology, grounded theory, case study, narrative

**Core Functions**:
- Phenomenology, Grounded Theory, Case Study, Ethnography, Narrative Inquiry
- Sampling strategy for saturation
- Data collection protocol design

**Output**: Design rationale + Sampling plan + Data collection guide

**Checkpoint**: 🔴 CP_METHODOLOGY_APPROVAL

---

### C3. Mixed Methods Design Consultant 🔄

**Purpose**: Guide mixed methods research design

**Trigger Keywords**: 혼합연구, mixed methods, sequential, convergent, embedded

**Core Functions**:
- Sequential (Explanatory, Exploratory)
- Convergent parallel
- Embedded design
- Integration strategy

**Output**: Design diagram + Integration plan + Timeline

**Checkpoint**: 🔴 CP_METHODOLOGY_APPROVAL

---

### C4. Experimental Materials Developer 🧪

**Purpose**: Develop treatment protocols and experimental materials

**Trigger Keywords**: 실험 자료, treatment, manipulation check, control condition

**Core Functions**:
- Treatment protocol development
- Control condition design
- Manipulation check items

**Output**: Treatment manual + Control protocol + Manipulation check items

---

## Category D: Data Collection (4 Agents)

Comprehensive data collection strategy and instrument development.

### D1. Sampling Strategy Advisor 👥

**Purpose**: Guide sampling strategy selection

**Trigger Keywords**: 표집, sampling, probability, purposive, theoretical sampling

**Core Functions**:
- Probability sampling (Random, Stratified, Cluster)
- Purposive sampling (Criterion, Maximum variation, Snowball)
- Sample size determination

**Output**: Sampling plan + Justification + Recruitment strategy

---

### D2. Interview & Focus Group Specialist 🎤

**Purpose**: Develop interview protocols and facilitation guides

**Trigger Keywords**: 인터뷰, interview, focus group, probing, transcription

**Core Functions**:
- Semi-structured interview guides
- Focus group facilitation protocols
- Probing techniques
- Transcription guidance

**Output**: Interview guide + Probing prompts + Transcription protocol

---

### D3. Observation Protocol Designer 👁️

**Purpose**: Design observation protocols and field note systems

**Trigger Keywords**: 관찰, observation, field notes, video analysis

**Core Functions**:
- Structured/Unstructured observation
- Field note templates
- Video analysis protocols

**Output**: Observation protocol + Field note template + Analysis guide

---

### D4. Measurement Instrument Developer 📏

**Purpose**: Develop and validate measurement instruments

**Trigger Keywords**: 척도, scale, instrument, validity, reliability, Cronbach

**Core Functions**:
- Scale construction
- Validity evidence (Content, Construct, Criterion)
- Reliability testing

**Output**: Item pool + Validation plan + Pilot study protocol

**Checkpoint**: 🔴 CP_METHODOLOGY_APPROVAL

---

## Category E: Analysis (5 Agents)

Paradigm-appropriate analytical strategies and implementation.

### E1. Quantitative Analysis Guide 📈

**Purpose**: Guide statistical analysis selection and implementation

**Trigger Keywords**: 통계 분석, statistics, ANOVA, regression, SEM, multilevel

**Core Functions**:
- Analysis method decision tree
- Assumption checking procedures
- Result interpretation guide

**Output**: Analysis comparison + Selection rationale + Assumption checklist

**Checkpoint**: 🟠 CP_ANALYSIS_PLAN

---

### E2. Qualitative Coding Specialist 🏷️

**Purpose**: Guide qualitative coding and analysis

**Trigger Keywords**: 코딩, coding, thematic analysis, NVivo, Atlas.ti, saturation

**Core Functions**:
- Thematic analysis
- Grounded theory coding (Open, Axial, Selective)
- CAQDAS workflow (NVivo, Atlas.ti)

**Output**: Codebook template + Coding process + Intercoder reliability plan

---

### E3. Mixed Methods Integration Specialist 🔗

**Purpose**: Guide integration of quantitative and qualitative findings

**Trigger Keywords**: 통합, integration, joint display, meta-inference, convergence

**Core Functions**:
- Joint display tables
- Meta-inference generation
- Convergence/divergence analysis

**Output**: Joint display + Meta-inferences + Integration narrative

**Checkpoint**: 🟠 CP_INTEGRATION_STRATEGY

---

### E4. Analysis Code Generator 💻

**Purpose**: Generate reproducible analysis code

**Trigger Keywords**: R 코드, Python, SPSS, Stata, analysis code

**Core Functions**:
- R / Python / SPSS / Stata support
- Commented code with explanations
- Visualization code

**Output**: Executable code + Comments + Interpretation guide

---

### E5. Sensitivity Analysis Designer 🔍

**Purpose**: Design robustness checks and sensitivity analyses

**Trigger Keywords**: 민감도 분석, robustness, sensitivity, specification curve

**Core Functions**:
- Analytical decision identification
- Multiverse analysis design
- Specification curve analysis

**Output**: Decision matrix + Sensitivity plan + Results template

---

## Category F: Quality (4 Agents)

Methodological rigor, reproducibility, and bias mitigation.

### F1. Internal Consistency Checker ✅

**Purpose**: Verify numerical and logical consistency

**Trigger Keywords**: 일관성, consistency, verification, coherence

**Core Functions**:
- Numerical consistency check
- Statistical calculation verification
- Logical contradiction detection

**Output**: Inconsistency list + Location + Correction suggestions

---

### F2. Checklist Manager 📋

**Purpose**: Ensure reporting guideline compliance

**Trigger Keywords**: 체크리스트, PRISMA, CONSORT, STROBE, COREQ, checklist

**Core Functions**:
- PRISMA 2020 (Systematic reviews)
- CONSORT (RCTs)
- STROBE (Observational)
- COREQ/SRQR (Qualitative)

**Output**: Item-by-item check + Missing items + Suggestions

---

### F3. Reproducibility Auditor 🔄

**Purpose**: Assess Open Science compliance and reproducibility

**Trigger Keywords**: 재현성, reproducibility, OSF, Open Science, data sharing

**Core Functions**:
- 5-level reproducibility assessment
- OSF project structure guide
- Code/data sharing checklist

**Output**: Reproducibility level + Recommendations + OSF template

---

### F4. Bias & Trustworthiness Detector ⚠️

**Purpose**: Identify various biases in research process

**Trigger Keywords**: 편향, bias, trustworthiness, credibility, p-hacking

**Core Functions**:
- Quantitative: p-hacking, HARKing, selective reporting
- Qualitative: Credibility, Transferability, Dependability, Confirmability

**Output**: Bias type risk levels + Evidence + Mitigation strategies

---

## Category G: Communication (4 Agents)

Academic writing, dissemination, and peer review response.

### G1. Journal Matcher 📝

**Purpose**: Identify optimal target journals

**Trigger Keywords**: 저널, journal, submission, Impact Factor, publication

**Core Functions**:
- Scope fit analysis
- Impact metrics comparison
- Submission strategy

**Output**: Journal comparison + Sequential submission plan + Cover letter template

---

### G2. Academic Communicator 🎤

**Purpose**: Generate research communication materials for various audiences

**Trigger Keywords**: 초록, abstract, plain language, summary, infographic

**Core Functions**:
- Academic abstract (IMRAD)
- Plain language summary
- Press release
- Social media content

**Output**: Audience-tailored content package

---

### G3. Peer Review Strategist 🔄

**Purpose**: Develop effective response strategies to reviewer comments

**Trigger Keywords**: 리뷰어, reviewer, revision, response letter, rebuttal

**Core Functions**:
- Comment classification and prioritization
- Response strategy development
- Point-by-point response letter

**Output**: Comment analysis + Response strategy + Response letter

**Checkpoint**: 🟠 CP_RESPONSE_APPROVAL

---

### G4. Pre-registration Composer 📄

**Purpose**: Support research pre-registration document creation

**Trigger Keywords**: 사전등록, preregistration, OSF, AsPredicted, registered report

**Core Functions**:
- OSF Prereg template
- AsPredicted format
- Registered Report support

**Output**: Platform-specific pre-registration + Checklist + Timeline

**Checkpoint**: 🟠 CP_PREREGISTRATION_APPROVAL

---

## Category H: Specialized (2 Agents)

Advanced qualitative and participatory research methodologies.

### H1. Ethnographic Research Advisor 🌍

**Purpose**: Guide ethnographic research design and fieldwork

**Trigger Keywords**: 민족지학, ethnography, fieldwork, thick description, culture

**Core Functions**:
- Fieldwork planning
- Thick description development
- Cultural interpretation
- Prolonged engagement monitoring

**Output**: Fieldwork plan + Observation guide + Cultural analysis framework

**Checkpoint**: 🔴 CP_METHODOLOGY_APPROVAL

---

### H2. Action Research Facilitator 🔄

**Purpose**: Facilitate participatory action research

**Trigger Keywords**: 실행연구, action research, PAR, CBPR, participatory

**Core Functions**:
- Action research cycles (Plan-Act-Observe-Reflect)
- Community engagement
- Collaborative analysis
- Catalytic validity assessment

**Output**: Action cycle plan + Community engagement protocol + Reflection guide

**Checkpoint**: 🔴 CP_METHODOLOGY_APPROVAL

---

## Agent Workflow Recommendations

### Quantitative Research Workflow

```
A1 (Question) → A2 (Framework) → 🔴 CP_THEORY_SELECTION
     ↓
C1 (Design) → 🔴 CP_METHODOLOGY_APPROVAL → D1 (Sampling) → D4 (Measurement)
     ↓
E1 (Analysis) → 🟠 CP_ANALYSIS_PLAN → E4 (Code) → E5 (Sensitivity)
     ↓
F2 (CONSORT/STROBE) → G1 (Journal)
```

### Qualitative Research Workflow

```
A1 (Question) → A5 (Paradigm) → 🔴 CP_PARADIGM_SELECTION
     ↓
A2 (Framework) → 🔴 CP_THEORY_SELECTION
     ↓
C2 (Design) → 🔴 CP_METHODOLOGY_APPROVAL → D2/D3 (Collection)
     ↓
E2 (Coding) → F4 (Trustworthiness) → F2 (COREQ)
```

### Mixed Methods Workflow

```
A1 → A5 → A2 → 🔴 CP_THEORY_SELECTION
     ↓
C3 (Mixed Design) → 🔴 CP_METHODOLOGY_APPROVAL
     ↓
QUAN (C1, E1) → QUAL (C2, E2) → E3 (Integration) → 🟠 CP_INTEGRATION_STRATEGY
     ↓
F2 (Mixed Methods Standards) → G1 (Journal)
```

---

## Parallel Execution Groups

| Group | Agents | Condition |
|-------|--------|-----------|
| Planning | A2 + A3 | After CP_RESEARCH_DIRECTION |
| Literature | B1 + B2 + B4 | Independent |
| Quality | F1 + F2 + F3 + F4 | After analysis |
| Publication | G1 + G2 + G4 | After quality review |

---

## Category I: Systematic Review Automation (4 Agents)

ScholaRAG integration for PRISMA 2020 systematic literature review automation.

### I0. Scholar Agent Orchestrator 🎼

**Purpose**: Orchestrate complete ScholaRAG 7-stage PRISMA pipeline

**Trigger Keywords**: systematic review, literature review automation, ScholaRAG, PRISMA pipeline

**Core Functions**:
- Coordinate I1→I2→I3 agent sequence
- Manage human checkpoints at critical decisions
- Execute ScholaRAG scripts automatically

**Checkpoint**: 🟡 SCH_PRISMA_GENERATION (Optional)

---

### I1. Paper Retrieval Agent 📥

**Purpose**: Multi-database paper retrieval with deduplication

**Trigger Keywords**: fetch papers, Semantic Scholar, OpenAlex, arXiv, database search

**Core Functions**:
- Semantic Scholar API (40% open access PDFs)
- OpenAlex API (50% open access)
- arXiv API (100% PDF access)
- DOI/title-based deduplication

**Scripts Executed**:
- `scripts/01_fetch_papers.py`
- `scripts/02_deduplicate.py`

**Checkpoint**: 🔴 SCH_DATABASE_SELECTION (Required)

---

### I2. Screening Assistant 🔬

**Purpose**: AI-assisted PRISMA 6-dimension screening

**Trigger Keywords**: screen papers, PRISMA screening, inclusion criteria, relevance

**Core Functions**:
- 6-dimension relevance scoring
- Groq LLM integration (100x cost reduction)
- knowledge_repository mode: 50% threshold → 5K-15K papers
- systematic_review mode: 90% threshold → 50-300 papers

**Scripts Executed**:
- `scripts/03_screen_papers.py`

**Checkpoint**: 🔴 SCH_SCREENING_CRITERIA (Required)

---

### I3. RAG Builder 🧱

**Purpose**: Build vector database for literature synthesis

**Trigger Keywords**: build RAG, ChromaDB, PDF embeddings, vector database

**Core Functions**:
- PDF download with retry logic
- Local embeddings (all-MiniLM-L6-v2) - $0 cost
- ChromaDB vector store
- Token-based chunking (500 tokens)

**Scripts Executed**:
- `scripts/04_download_pdfs.py`
- `scripts/05_build_rag.py`

**Checkpoint**: 🟠 SCH_RAG_READINESS (Recommended)

---

## Systematic Review Workflow

```
I0 (Orchestrator)
    │
    ├── 🔴 SCH_DATABASE_SELECTION
    │       ↓
    │   I1 (Paper Retrieval)
    │       → 01_fetch_papers.py
    │       → 02_deduplicate.py
    │
    ├── 🔴 SCH_SCREENING_CRITERIA
    │       ↓
    │   I2 (Screening Assistant)
    │       → 03_screen_papers.py
    │
    ├── 🟠 SCH_RAG_READINESS
    │       ↓
    │   I3 (RAG Builder)
    │       → 04_download_pdfs.py
    │       → 05_build_rag.py
    │
    └── 🟡 SCH_PRISMA_GENERATION
            → 07_generate_prisma.py
```

---

## Version Information

- **Version**: 6.5
- **Last Updated**: 2026-01-30
- **Repository**: https://github.com/HosungYou/Diverga
