# CLAUDE.md

# Diverga v5.0.0 (Sisyphus Edition)

**Beyond Modal: AI Research Assistant That Thinks Creatively**

AI Research Assistant for the Complete Research Lifecycle - from question formulation to publication.

**Language**: English base with Korean support (한국어 입력 지원)

## Project Overview

Diverga provides **context-persistent research support** through 27 specialized agents across 8 categories (A-H). Unlike other AI tools that suffer from **mode collapse** (always recommending the same predictable options), Diverga uses **Verbalized Sampling (VS) methodology** to guide you toward creative, defensible research choices while maintaining research context across the entire project lifecycle in a single platform.

## Core Value Proposition

1. **Beyond Modal**: VS methodology prevents mode collapse - you get creative alternatives, not just obvious choices
2. **Context Persistence**: No re-explaining your research question, methodology, or decisions
3. **Single Platform**: Claude Code as your unified research environment
4. **Research Pipeline**: Structured workflow from idea to publication
5. **Tool Discovery**: Easy access to tools/platforms you didn't know existed
6. **Human-Centered**: AI assists, humans decide

> **Core Principle**: "Human decisions remain with humans. AI handles what's beyond human scope."
> "인간이 할 일은 인간이, AI는 인간의 범주를 벗어난 것을 수행"

## Quick Start

Simply tell Diverga what you want to do:

```
"I want to conduct a systematic review on AI in education"
"메타분석 연구를 시작하고 싶어"
"Help me design an experimental study"
```

The system guides you through a conversational wizard with clear choice points.

## Core Systems (v4.0)

| System | Purpose | Location |
|--------|---------|----------|
| Project State | Context persistence | `.research/project-state.yaml` |
| Pipeline Templates | PRISMA 2020 workflow | `core/pipeline-templates.md` |
| Integration Hub | Tool connections | `core/integration-hub.md` |
| Guided Wizard | AskUserQuestion UX | `core/guided-wizard.md` |
| Auto-Documentation | Document generation | `core/auto-documentation.md` |

## Agent Structure (v5.0)

### 27 Agents in 8 Categories

| Category | Agents | Paradigm Affinity |
|----------|--------|-------------------|
| **A: Foundation** | A1-ResearchQuestionRefiner, A2-TheoreticalFrameworkArchitect, A3-DevilsAdvocate, A4-ResearchEthicsAdvisor, A5-ParadigmWorldviewAdvisor | All paradigms |
| **B: Evidence** | B1-SystematicLiteratureScout, B2-EvidenceQualityAppraiser, B3-EffectSizeExtractor, B4-ResearchRadar | Quantitative-focused |
| **C: Design** | C1-QuantitativeDesignConsultant, C2-QualitativeDesignConsultant, C3-MixedMethodsDesignConsultant, C4-ExperimentalMaterialsDeveloper | Paradigm-specific |
| **D: Data Collection** | D1-SamplingStrategyAdvisor, D2-InterviewFocusGroupSpecialist, D3-ObservationProtocolDesigner, D4-MeasurementInstrumentDeveloper | Method-specific |
| **E: Analysis** | E1-QuantitativeAnalysisGuide, E2-QualitativeCodingSpecialist, E3-MixedMethodsIntegration, E4-AnalysisCodeGenerator | Paradigm-specific |
| **F: Quality** | F1-SensitivityAnalysisDesigner, F2-ChecklistManager, F3-ReproducibilityAuditor, F4-BiasTrustworthinessDetector | All paradigms |
| **G: Communication** | G1-JournalMatcher, G2-AcademicCommunicator, G3-PeerReviewStrategist, G4-PreregistrationComposer | All paradigms |
| **H: Specialized** | H1-EthnographicResearchAdvisor, H2-NarrativeAnalysisSpecialist, H3-GroundedTheoryAdvisor | Qualitative-focused |

### Research Types Supported

**Quantitative:**
- Experimental designs (RCT, quasi-experimental)
- Survey research
- Meta-analysis and systematic reviews
- Correlational studies
- Psychometric validation

**Qualitative:**
- Phenomenology
- Grounded theory
- Case study
- Ethnography
- Narrative inquiry
- Action research

**Mixed Methods:**
- Sequential (explanatory, exploratory)
- Convergent parallel
- Embedded design
- Transformative frameworks

## Tool Integrations

### Ready to Use (No Setup)
- **Excel**: Data extraction, coding → "Create extraction spreadsheet"
- **PowerPoint**: Presentations → "Create conference slides"
- **Word**: Manuscripts → "Export methods to Word"
- **Python**: Analysis → Built-in
- **Mermaid**: Diagrams → "Create PRISMA flow diagram"

### Needs Setup
- **Semantic Scholar**: API key for literature search
- **OpenAlex**: Email for polite pool
- **Zotero**: MCP server for references
- **R Scripts**: Local R installation
- **Nanobanana**: Gemini API key for visualization

## GitHub Repository

https://github.com/HosungYou/research-coordinator

---

## OMC Integration (v3.2.0+)

Diverga integrates with **oh-my-claudecode** for parallel processing and smart model routing.

### Human Checkpoints

| Level | Checkpoints | Action |
|-------|-------------|--------|
| 🔴 REQUIRED | CP_RESEARCH_DIRECTION, CP_THEORY_SELECTION, CP_METHODOLOGY_APPROVAL | User approval required |
| 🟠 RECOMMENDED | CP_ANALYSIS_PLAN, CP_QUALITY_REVIEW | Review recommended |
| 🟡 OPTIONAL | CP_VISUALIZATION_PREFERENCE, CP_RENDERING_METHOD | Defaults available |

### Model Routing (v5.0)

| Tier | Model | Agents |
|------|-------|--------|
| HIGH | Opus | A2, A5, C2, C3, E2, E3, H1-H3 (Complex interpretive work, philosophical reasoning) |
| MEDIUM | Sonnet | A1, A3, A4, B1, B2, C1, C4, D1-D4, E1, E4, F2, F4, G2, G3 (Standard research tasks) |
| LOW | Haiku | B3, B4, F1, F3, G1, G4 (Quick lookups, formatting, checklists) |

### OMC Modes

```bash
ulw: 문헌 검색해줘     # ultrawork - maximum parallelism
eco: 통계 분석해줘     # ecomode - token efficient
ralph: 연구 설계 완료해줘  # persistence until done
```

---

## Sisyphus Protocol (v5.0)

Diverga embodies the **Sisyphus philosophy**: **Never claim completion without verification**.

### Continuation Enforcement

The system is bound to its task list and paradigm-specific completion criteria. It CANNOT stop until:

**Universal Criteria (All Paradigms):**
- [ ] All TODO items marked complete
- [ ] All human checkpoints approved
- [ ] Project state file updated
- [ ] Documentation generated
- [ ] No unaddressed errors or warnings

**Quantitative Research:**
- [ ] Hypotheses formulated and testable
- [ ] Variables defined with operational definitions
- [ ] Sample size justified with power analysis
- [ ] Statistical analysis plan documented
- [ ] Analysis code generated and tested
- [ ] Results interpreted with effect sizes
- [ ] Visualizations generated (tables, figures)

**Qualitative Research:**
- [ ] Research questions aligned with qualitative approach
- [ ] Participant selection strategy justified
- [ ] Data collection protocol developed
- [ ] Coding framework established
- [ ] Saturation reached and documented
- [ ] Themes refined and verified
- [ ] Trustworthiness criteria met (credibility, transferability, dependability, confirmability)
- [ ] Member checking or peer debriefing completed

**Mixed Methods Research:**
- [ ] Quantitative strand completed (all quantitative criteria)
- [ ] Qualitative strand completed (all qualitative criteria)
- [ ] Integration strategy documented (when, how, why)
- [ ] Joint display created showing integration
- [ ] Meta-inference generated from integrated findings
- [ ] Methodological coherence verified

### Verification Before Completion

Before ANY claim of "done", "fixed", or "complete":

1. **IDENTIFY**: What evidence proves this claim?
2. **RUN**: Execute verification (test, validation, review)
3. **READ**: Check output - did it pass?
4. **ONLY THEN**: Make the claim with evidence

**Red Flags (STOP and verify):**
- Using "should", "probably", "seems to"
- Expressing satisfaction before verification
- Claiming completion without fresh evidence

---

## Paradigm Detection (Auto-Activation)

Diverga automatically detects research paradigm and activates appropriate agent packs.

### Auto-Detection Triggers

**Quantitative signals:** "hypothesis", "effect size", "p-value", "experiment", "ANOVA", "regression", "가설", "효과크기", "통계"

**Qualitative signals:** "lived experience", "saturation", "themes", "phenomenology", "coding", "체험", "포화", "현상학"

**Mixed methods signals:** "sequential", "convergent", "integration", "joint display", "혼합방법", "통합"

### Agent Pack Activation

When paradigm is detected:

**Quantitative Pack:**
- Primary: C1-QuantitativeDesignConsultant, E1-QuantitativeAnalysisGuide, E4-AnalysisCodeGenerator
- Secondary: B3-EffectSizeExtractor, D4-MeasurementInstrumentDeveloper
- Support: F2-ChecklistManager (CONSORT/STROBE), F4-BiasTrustworthinessDetector

**Qualitative Pack:**
- Primary: C2-QualitativeDesignConsultant, E2-QualitativeCodingSpecialist, D2-InterviewFocusGroupSpecialist
- Secondary: A5-ParadigmWorldviewAdvisor, H1-EthnographicResearchAdvisor, H2-NarrativeAnalysisSpecialist
- Support: F2-ChecklistManager (COREQ/SRQR), F4-BiasTrustworthinessDetector

**Mixed Methods Pack:**
- Primary: C3-MixedMethodsDesignConsultant, E3-MixedMethodsIntegrationSpecialist
- Includes: ALL agents from both quantitative and qualitative packs
- Support: F2-ChecklistManager (GRAMMS)

### User Clarification

If paradigm is undetermined (confidence < 0.7), ask:

> "Which research approach are you using?"
> 1. Quantitative (hypothesis testing, statistics)
> 2. Qualitative (interviews, themes, lived experiences)
> 3. Mixed Methods (combining both)
> 4. Not decided yet (need help choosing)

---
