# CLAUDE.md

# Diverga v6.7.0 (Systematic Review Automation)

**Beyond Modal: AI Research Assistant That Thinks Creatively**

**v6.7.0**: Systematic Review Automation - Category I agents (I0-I3) for PRISMA 2020 pipeline
**v6.6.3**: Codex CLI SKILL.md implementation - actual skill loading via `.codex/skills/`
**v6.6.2**: Multi-CLI Compatibility - unified install script, NPM package (@diverga/codex-setup)
**v6.5.0**: Parallel execution via Task tool - `Task(subagent_type="diverga:a1", ...)`
**v6.4**: Plugin Marketplace Registration - Install via `/plugin marketplace add`
**v6.3**: Meta-Analysis Agent System (C5/C6/C7) - Multi-gate validation, Hedges' g calculation

AI Research Assistant for the Complete Research Lifecycle - from question formulation to publication.

**Language**: English base with Korean support (한국어 입력 지원)

---

## Installation

```bash
# Step 1: Add to marketplace
/plugin marketplace add https://github.com/HosungYou/Diverga

# Step 2: Install
/plugin install diverga

# Step 3: Configure
/diverga:setup
```

---

## v6.0 Clean Slate Changes

| Change | v5.0 (Sisyphus) | v6.0 (Human-Centered) |
|--------|-----------------|----------------------|
| **Sisyphus Protocol** | "Work never stops" | ❌ REMOVED |
| **Iron Law** | "agent OR checkpoint" | ❌ REMOVED |
| **ralph/ultrawork/ecomode** | Autonomous modes | ❌ REMOVED |
| **Human Checkpoints** | Could be bypassed | ✅ MANDATORY |
| **Model Routing** | haiku/sonnet/opus | ✅ KEPT |
| **VS Methodology** | Creative alternatives | ✅ ENHANCED |

---

## Project Overview

Diverga provides **context-persistent research support** through **44 specialized agents** across 9 categories (A-I). Unlike other AI tools that suffer from **mode collapse** (always recommending the same predictable options), Diverga uses **Verbalized Sampling (VS) methodology** to guide you toward creative, defensible research choices while maintaining research context across the entire project lifecycle in a single platform.

## Core Value Proposition

1. **Human-Centered**: AI assists, humans decide at EVERY critical point
2. **Beyond Modal**: VS methodology prevents mode collapse - creative alternatives, not obvious choices
3. **Context Persistence**: No re-explaining your research question, methodology, or decisions
4. **Single Platform**: Claude Code as your unified research environment
5. **Research Pipeline**: Structured workflow from idea to publication
6. **Tool Discovery**: Easy access to tools/platforms you didn't know existed

> **Core Principle**: "Human decisions remain with humans. AI handles what's beyond human scope."
> "인간이 할 일은 인간이, AI는 인간의 범주를 벗어난 것을 수행"

---

## Quick Start

Simply tell Diverga what you want to do:

```
"I want to conduct a systematic review on AI in education"
"메타분석 연구를 시작하고 싶어"
"Help me design an experimental study"
```

The system will:
1. Detect your paradigm
2. **ASK for confirmation** (🔴 CHECKPOINT)
3. Present VS alternatives with T-Scores
4. **WAIT for your selection**
5. Guide you through the pipeline with checkpoints

---

## Human Checkpoint System (v6.0 Core Feature)

### Checkpoint Types

| Level | Icon | Behavior |
|-------|------|----------|
| **REQUIRED** | 🔴 | System STOPS - Cannot proceed without explicit approval |
| **RECOMMENDED** | 🟠 | System PAUSES - Strongly suggests approval |
| **OPTIONAL** | 🟡 | System ASKS - Defaults available if skipped |

### Required Checkpoints (🔴 MANDATORY)

| Checkpoint | When | What Happens |
|------------|------|--------------|
| CP_RESEARCH_DIRECTION | Research question finalized | Present VS options, WAIT for selection |
| CP_PARADIGM_SELECTION | Methodology approach | Ask Quantitative/Qualitative/Mixed |
| CP_THEORY_SELECTION | Framework chosen | Present alternatives with T-Scores |
| CP_METHODOLOGY_APPROVAL | Design complete | Detailed review required |

### Checkpoint Behavior

```
┌────────────────────────────────────────────────────────────────┐
│                   CHECKPOINT PROTOCOL                          │
│                                                                │
│   When AI reaches a checkpoint:                                │
│                                                                │
│   1. STOP immediately                                          │
│   2. Present options with VS alternatives                      │
│   3. WAIT for explicit human approval                          │
│   4. DO NOT proceed until approval received                    │
│   5. DO NOT assume approval based on context                   │
│                                                                │
│   ❌ NEVER: "진행하겠습니다" without asking                     │
│   ✅ ALWAYS: "어떤 방향으로 진행하시겠습니까?"                  │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## Core Systems

| System | Purpose | Location |
|--------|---------|----------|
| Project State | Context persistence | `.research/project-state.yaml` |
| Decision Log | Human decisions | `.research/decision-log.yaml` |
| Research Coordinator | Main skill definition | `.claude/skills/research-coordinator/SKILL.md` |
| Orchestrator | Agent management | `.claude/skills/research-orchestrator/SKILL.md` |

---

## Agent Structure (44 Agents in 9 Categories)

| Category | Count | Agents | Paradigm |
|----------|-------|--------|----------|
| **A: Foundation** | 6 | A1-ResearchQuestionRefiner, A2-TheoreticalFrameworkArchitect, A3-DevilsAdvocate, A4-ResearchEthicsAdvisor, A5-ParadigmWorldviewAdvisor, **A6-ConceptualFrameworkVisualizer** | All |
| **B: Evidence** | 5 | B1-SystematicLiteratureScout, B2-EvidenceQualityAppraiser, B3-EffectSizeExtractor, B4-ResearchRadar, **B5-ParallelDocumentProcessor** | All |
| **C: Design & Meta-Analysis** | 7 | C1-QuantitativeDesignConsultant, C2-QualitativeDesignConsultant, C3-MixedMethodsDesignConsultant, C4-ExperimentalMaterialsDeveloper, **C5-MetaAnalysisMaster**, **C6-DataIntegrityGuard**, **C7-ErrorPreventionEngine** | Paradigm-specific + Meta-analysis |
| **D: Data Collection** | 4 | D1-SamplingStrategyAdvisor, D2-InterviewFocusGroupSpecialist, D3-ObservationProtocolDesigner, D4-MeasurementInstrumentDeveloper | Method-specific |
| **E: Analysis** | 5 | E1-QuantitativeAnalysisGuide, E2-QualitativeCodingSpecialist, E3-MixedMethodsIntegration, E4-AnalysisCodeGenerator, **E5-SensitivityAnalysisDesigner** | Paradigm-specific |
| **F: Quality** | 5 | F1-InternalConsistencyChecker, F2-ChecklistManager, F3-ReproducibilityAuditor, F4-BiasTrustworthinessDetector, **F5-HumanizationVerifier** | All |
| **G: Communication** | 6 | G1-JournalMatcher, G2-AcademicCommunicator, G3-PeerReviewStrategist, G4-PreregistrationComposer, **G5-AcademicStyleAuditor**, **G6-AcademicStyleHumanizer** | All |
| **H: Specialized** | 2 | H1-EthnographicResearchAdvisor, H2-ActionResearchFacilitator | Qual |
| **I: Systematic Review Automation** | 4 | **I0-ScholarAgentOrchestrator**, **I1-PaperRetrievalAgent**, **I2-ScreeningAssistant**, **I3-RAGBuilder** | All |

**Total: 6 + 5 + 7 + 4 + 5 + 5 + 6 + 2 + 4 = 44 agents**

### New in v6.3: Meta-Analysis Agent System (C5/C6/C7)

Based on V7 GenAI meta-analysis lessons learned:

| Agent | Purpose | Model |
|-------|---------|-------|
| **C5-MetaAnalysisMaster** | Multi-gate validation, workflow orchestration | Opus |
| **C6-DataIntegrityGuard** | Data completeness, Hedges' g calculation, SD recovery | Sonnet |
| **C7-ErrorPreventionEngine** | Pattern detection, anomaly alerts, error prevention | Sonnet |

**Authority Model**:
- C5 = Decision Authority (gate pass/fail)
- C6 = Service Provider (data integrity reports)
- C7 = Advisory (warnings, recommendations)

### New in v6.1: Humanization Pipeline Agents

| Agent | Purpose | Model |
|-------|---------|-------|
| **G5-AcademicStyleAuditor** | AI pattern detection (24 categories) | Sonnet |
| **G6-AcademicStyleHumanizer** | Transform AI patterns to natural prose | Opus |
| **F5-HumanizationVerifier** | Verify transformation integrity | Haiku |

### New in v6.2: Parallel Document Processing

| Agent | Purpose | Model |
|-------|---------|-------|
| **B5-ParallelDocumentProcessor** | Batch PDF processing with parallel workers | Opus |

### New in v6.7.0: Systematic Review Automation (Category I)

PRISMA 2020 compliant systematic literature review pipeline with automated paper retrieval, screening, and RAG building.

| Agent | Purpose | Model | Checkpoint |
|-------|---------|-------|------------|
| **I0-ScholarAgentOrchestrator** | Pipeline coordination, stage management | Opus | - |
| **I1-PaperRetrievalAgent** | Multi-database fetching (Semantic Scholar, OpenAlex, arXiv) | Sonnet | 🔴 SCH_DATABASE_SELECTION |
| **I2-ScreeningAssistant** | AI-PRISMA 6-dimension screening | Sonnet | 🔴 SCH_SCREENING_CRITERIA |
| **I3-RAGBuilder** | Vector database construction (zero cost) | Haiku | 🟠 SCH_RAG_READINESS |

**Human Checkpoints**:
- 🔴 **SCH_DATABASE_SELECTION**: User must approve database selection before retrieval
- 🔴 **SCH_SCREENING_CRITERIA**: User must approve inclusion/exclusion criteria
- 🟠 **SCH_RAG_READINESS**: Recommended checkpoint before RAG queries

---

## Model Routing (v6.7)

| Tier | Model | Agents (44 total) |
|------|-------|-------------------|
| HIGH | Opus | A1, A2, A3, A5, **B5**, C1, C2, C3, D4, E1, E2, E3, G3, **G6**, H1, H2, **I0** (17) |
| MEDIUM | Sonnet | A4, A6, B1, B2, C4, D1, D2, E5, F3, F4, G1, G2, G4, **G5**, **I1**, **I2** (16) |
| LOW | Haiku | B3, B4, D3, E4, F1, F2, **F5**, **I3** (8) |

---

## Research Types Supported

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

---

## VS Methodology (Enhanced in v6.0)

### T-Score (Typicality Score)

| T-Score | Label | Meaning |
|---------|-------|---------|
| >= 0.7 | Common | Highly typical, safe but limited novelty |
| 0.4-0.7 | Moderate | Balanced risk-novelty |
| 0.2-0.4 | Innovative | Novel, requires strong justification |
| < 0.2 | Experimental | Highly novel, high risk/reward |

### VS Process with Human Decision

```
Stage 1: Context & Modal Identification
  └─ Identify "obvious" recommendations

Stage 2: Divergent Exploration
  ├─ Direction A (T~0.6): Safe but differentiated
  ├─ Direction B (T~0.4): Balanced novelty ⭐
  └─ Direction C (T<0.3): Innovative/experimental

Stage 3: Human Selection (🔴 CHECKPOINT)
  ├─ Present ALL options with T-Scores
  ├─ WAIT for human decision
  └─ Execute ONLY selected direction
```

---

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

---

## Paradigm Detection (Auto-Activation + Confirmation)

### Auto-Detection Triggers

**Quantitative signals:** "hypothesis", "effect size", "p-value", "experiment", "ANOVA", "regression", "가설", "효과크기", "통계"

**Qualitative signals:** "lived experience", "saturation", "themes", "phenomenology", "coding", "체험", "포화", "현상학"

**Mixed methods signals:** "sequential", "convergent", "integration", "joint display", "혼합방법", "통합"

### Confirmation (Always Ask)

When paradigm is detected, **ALWAYS ask for confirmation**:

```
"연구 맥락에서 [양적 연구] 접근이 감지되었습니다.
이 패러다임으로 진행해도 될까요?

 [Q] 예, 양적 연구로 진행
 [L] 아니요, 질적 연구로 변경
 [M] 아니요, 혼합방법으로 변경
 [?] 잘 모르겠어요, 도움이 필요해요"
```

---

## Humanization Pipeline (v6.1 New Feature)

### Overview

Transform AI-generated academic text into natural, human-sounding prose while preserving scholarly integrity. Based on Wikipedia's AI Cleanup initiative's 24 pattern categories, adapted for academic writing.

### Pipeline Stages

```
Content Generation (G2/G3) → G5 Analysis → Checkpoint → G6 Transform → F5 Verify → Export
```

### Commands

| Command | Description |
|---------|-------------|
| `"Check AI patterns"` | Run G5 analysis, show pattern report |
| `"Humanize my draft"` | Full pipeline with balanced mode |
| `"Humanize (conservative)"` | Minimal changes, high-risk only |
| `"Humanize (aggressive)"` | Maximum naturalness |
| `"Export with humanization"` | Run pipeline before export |

### Transformation Modes

| Mode | Target | Best For |
|------|--------|----------|
| **Conservative** | High-risk patterns only | Journal submissions |
| **Balanced** ⭐ | High + medium-risk | Most academic writing |
| **Aggressive** | All patterns | Blog posts, informal |

### New Checkpoint

| Checkpoint | Level | When |
|------------|-------|------|
| CP_HUMANIZATION_REVIEW | 🟠 Recommended | After content generation |
| CP_HUMANIZATION_VERIFY | 🟡 Optional | Before final export |

### Ethics Note

Humanization helps express ideas naturally—it does NOT make AI use "undetectable."
Researchers should follow institutional and journal AI disclosure policies.

See: `.claude/skills/research-coordinator/ethics/ai-writing-ethics.md`

---

## What Was Removed in v6.0

### ❌ Sisyphus Protocol
- **Was**: "Work never stops until complete"
- **Problem**: Bypassed human checkpoints
- **Now**: AI stops at every checkpoint and waits

### ❌ Iron Law of Continuation
- **Was**: "Move to next agent OR human checkpoint"
- **Problem**: "OR" made checkpoints optional
- **Now**: Checkpoint THEN next agent (sequential)

### ❌ OMC Autonomous Modes
- **Removed**: ralph, ultrawork, autopilot, ecomode
- **Problem**: These modes enabled checkpoint bypass
- **Kept**: Model routing (haiku/sonnet/opus) only

---

## GitHub Repository

https://github.com/HosungYou/Diverga

---

## Auto-Trigger Agent Dispatch (v6.4 Core Feature)

Diverga automatically detects keywords and context to activate appropriate agents via Task tool.

### Agent Invocation Pattern

When Claude Code detects trigger keywords, it automatically invokes agents:

```python
Task(
    subagent_type="diverga:<agent_id>",
    model="<opus|sonnet|haiku>",
    prompt="<research context + specific task>"
)
```

### Complete Auto-Trigger Reference

#### Category A: Foundation (6 agents)

| Agent | Trigger Keywords (EN) | 트리거 키워드 (KR) | Model |
|-------|----------------------|-------------------|-------|
| `diverga:a1` | "research question", "RQ", "refine question" | "연구 질문", "연구문제", "RQ" | opus |
| `diverga:a2` | "theoretical framework", "theory", "conceptual model" | "이론적 프레임워크", "이론적 틀" | opus |
| `diverga:a3` | "devil's advocate", "critique", "counterargument" | "반론", "비판적 검토", "반대 의견" | opus |
| `diverga:a4` | "IRB", "ethics", "informed consent", "research ethics" | "연구 윤리", "IRB", "동의서" | sonnet |
| `diverga:a5` | "paradigm", "ontology", "epistemology", "worldview" | "패러다임", "존재론", "인식론" | opus |
| `diverga:a6` | "conceptual framework", "visualize framework" | "개념적 프레임워크", "프레임워크 시각화" | sonnet |

#### Category B: Evidence (5 agents)

| Agent | Trigger Keywords (EN) | 트리거 키워드 (KR) | Model |
|-------|----------------------|-------------------|-------|
| `diverga:b1` | "systematic review", "literature search", "PRISMA" | "체계적 문헌고찰", "문헌 검색" | sonnet |
| `diverga:b2` | "quality appraisal", "RoB", "GRADE", "bias assessment" | "품질 평가", "비뚤림 평가" | sonnet |
| `diverga:b3` | "effect size", "extract effect", "Cohen's d", "Hedges' g" | "효과크기", "효과 크기 추출" | haiku |
| `diverga:b4` | "research trends", "emerging topics", "research radar" | "연구 동향", "트렌드" | haiku |
| `diverga:b5` | "batch PDF", "parallel processing", "multiple PDFs" | "PDF 일괄 처리", "병렬 처리" | opus |

#### Category C: Design & Meta-Analysis (7 agents)

| Agent | Trigger Keywords (EN) | 트리거 키워드 (KR) | Model |
|-------|----------------------|-------------------|-------|
| `diverga:c1` | "quantitative design", "experimental design", "RCT" | "양적 연구 설계", "실험 설계" | opus |
| `diverga:c2` | "qualitative design", "phenomenology", "grounded theory" | "질적 연구 설계", "현상학", "근거이론" | opus |
| `diverga:c3` | "mixed methods", "sequential design", "convergent" | "혼합방법", "혼합 연구", "통합 설계" | opus |
| `diverga:c4` | "intervention materials", "experimental materials" | "중재 자료", "실험 자료 개발" | sonnet |
| `diverga:c5` | "meta-analysis", "pooled effect", "heterogeneity" | "메타분석", "메타 분석", "통합 효과" | opus |
| `diverga:c6` | "data extraction", "PDF extract", "extract data" | "데이터 추출", "PDF 추출", "자료 추출" | sonnet |
| `diverga:c7` | "error prevention", "validation", "data check" | "오류 방지", "검증", "데이터 확인" | sonnet |

#### Category D: Data Collection (4 agents)

| Agent | Trigger Keywords (EN) | 트리거 키워드 (KR) | Model |
|-------|----------------------|-------------------|-------|
| `diverga:d1` | "sampling", "sample size", "G*Power" | "표집", "표본 크기", "샘플링" | sonnet |
| `diverga:d2` | "interview", "focus group", "interview protocol" | "인터뷰", "면담", "포커스 그룹" | sonnet |
| `diverga:d3` | "observation", "observation protocol" | "관찰", "관찰 프로토콜" | haiku |
| `diverga:d4` | "instrument", "measurement", "scale development" | "측정 도구", "척도 개발" | opus |

#### Category E: Analysis (5 agents)

| Agent | Trigger Keywords (EN) | 트리거 키워드 (KR) | Model |
|-------|----------------------|-------------------|-------|
| `diverga:e1` | "statistical analysis", "ANOVA", "regression", "SEM" | "통계 분석", "회귀", "분산분석" | opus |
| `diverga:e2` | "qualitative coding", "thematic analysis", "coding" | "질적 코딩", "주제 분석", "코딩" | opus |
| `diverga:e3` | "mixed methods integration", "joint display" | "혼합방법 통합", "통합 분석" | opus |
| `diverga:e4` | "R code", "Python code", "analysis code" | "R 코드", "Python 코드", "분석 코드" | haiku |
| `diverga:e5` | "sensitivity analysis", "robustness check" | "민감도 분석", "강건성 검증" | sonnet |

#### Category F: Quality (5 agents)

| Agent | Trigger Keywords (EN) | 트리거 키워드 (KR) | Model |
|-------|----------------------|-------------------|-------|
| `diverga:f1` | "consistency check", "internal consistency" | "일관성 검토", "내적 일관성" | haiku |
| `diverga:f2` | "checklist", "CONSORT", "STROBE", "COREQ" | "체크리스트", "보고 지침" | haiku |
| `diverga:f3` | "reproducibility", "replication", "OSF" | "재현성", "반복가능성" | sonnet |
| `diverga:f4` | "bias detection", "trustworthiness" | "편향 탐지", "신뢰성" | sonnet |
| `diverga:f5` | "humanization verify", "AI text check" | "휴먼화 검증", "AI 텍스트 확인" | haiku |

#### Category G: Communication (6 agents)

| Agent | Trigger Keywords (EN) | 트리거 키워드 (KR) | Model |
|-------|----------------------|-------------------|-------|
| `diverga:g1` | "journal match", "where to publish", "target journal" | "저널 매칭", "투고처", "학술지" | sonnet |
| `diverga:g2` | "academic writing", "manuscript", "write paper" | "학술 글쓰기", "논문 작성" | sonnet |
| `diverga:g3` | "peer review", "reviewer response", "revision" | "동료 심사", "리뷰어 응답", "수정" | sonnet |
| `diverga:g4` | "preregistration", "OSF", "pre-register" | "사전등록", "OSF" | sonnet |
| `diverga:g5` | "AI pattern", "check AI writing", "style audit" | "AI 패턴", "AI 글쓰기 검토" | sonnet |
| `diverga:g6` | "humanize", "humanization", "natural writing" | "휴먼화", "자연스러운 글쓰기" | opus |

#### Category H: Specialized (2 agents)

| Agent | Trigger Keywords (EN) | 트리거 키워드 (KR) | Model |
|-------|----------------------|-------------------|-------|
| `diverga:h1` | "ethnography", "fieldwork", "participant observation" | "민족지학", "현장연구", "참여관찰" | opus |
| `diverga:h2` | "action research", "participatory", "practitioner" | "실행연구", "참여적 연구" | opus |

#### Category I: Systematic Review Automation (4 agents)

| Agent | Trigger Keywords (EN) | 트리거 키워드 (KR) | Model |
|-------|----------------------|-------------------|-------|
| `diverga:i0` | "systematic review", "PRISMA", "literature review automation" | "체계적 문헌고찰", "프리즈마", "문헌고찰 자동화" | opus |
| `diverga:i1` | "fetch papers", "retrieve papers", "database search" | "논문 수집", "논문 검색", "데이터베이스 검색" | sonnet |
| `diverga:i2` | "screen papers", "PRISMA screening", "inclusion criteria" | "논문 스크리닝", "선별", "포함 기준" | sonnet |
| `diverga:i3` | "build RAG", "vector database", "embed documents" | "RAG 구축", "벡터 DB", "문서 임베딩" | haiku |

### Parallel Execution Groups

Diverga can run multiple agents in parallel when tasks are independent:

```
┌─────────────────────────────────────────────────────────────────┐
│                  PARALLEL EXECUTION GROUPS                       │
├─────────────────────────────────────────────────────────────────┤
│ Group 1: Research Design                                        │
│   diverga:a1 + diverga:a2 + diverga:a5                         │
│                                                                  │
│ Group 2: Literature & Evidence                                   │
│   diverga:b1 + diverga:b2 + diverga:b3                         │
│                                                                  │
│ Group 3: Meta-Analysis Pipeline                                  │
│   diverga:c5 → diverga:c6 → diverga:c7 (sequential)            │
│                                                                  │
│ Group 4: Quality Assurance                                       │
│   diverga:f1 + diverga:f3 + diverga:f4                         │
│                                                                  │
│ Group 5: Publication Prep                                        │
│   diverga:g1 + diverga:g2 + diverga:g5                         │
│                                                                  │
│ Group 6: Systematic Review Screening (NEW in v6.7)              │
│   diverga:i1 + diverga:i2 (parallel)                           │
│   diverga:i0 → diverga:i1 → diverga:i2 → diverga:i3 (pipeline) │
└─────────────────────────────────────────────────────────────────┘
```

### Sequential Execution Rules

Some agents must run in order:

```
Meta-Analysis Pipeline:
  diverga:c5 (orchestration)
    → diverga:c6 (extraction)
    → diverga:c7 (validation)

Humanization Pipeline:
  diverga:g5 (audit)
    → diverga:g6 (humanize)
    → diverga:f5 (verify)
```

### Example Auto-Trigger

**User Message**: "I want to conduct a meta-analysis on AI-assisted learning. Need to extract effect sizes from 50 PDFs."

**Diverga Auto-Detection**:
```
Detected Keywords:
- "meta-analysis" → diverga:c5 (MetaAnalysisMaster)
- "extract effect sizes" → diverga:b3 (EffectSizeExtractor)
- "50 PDFs" → diverga:b5 (ParallelDocumentProcessor)

Execution Plan:
1. [PARALLEL] diverga:c5 + diverga:b5
2. [SEQUENTIAL] diverga:c6 → diverga:c7
```

---

## Version History

- **v6.7.0**: Systematic Review Automation - Category I agents (I0-I3) for PRISMA 2020 pipeline (44 agents total)
- **v6.6.3**: Codex CLI SKILL.md Implementation - actual skill loading via `.codex/skills/`, QUANT-005 verified
- **v6.6.2**: Multi-CLI Compatibility Edition - unified install script, NPM package (@diverga/codex-setup)
- **v6.5.0**: Parallel Execution Edition - Task tool support via `/agents/` directory
- **v6.4.0**: Plugin Marketplace Edition - `/plugin marketplace add`, auto-trigger dispatch, /diverga:setup wizard
- **v6.3.0**: Meta-Analysis Agent System - C5-MetaAnalysisMaster, C6-DataIntegrityGuard, C7-ErrorPreventionEngine (40 agents total)
- **v6.2.0**: Parallel Document Processing - B5-ParallelDocumentProcessor for batch PDF handling (37 agents total)
- **v6.1.0**: Humanization Pipeline - G5-AcademicStyleAuditor, G6-AcademicStyleHumanizer, F5-HumanizationVerifier (36 agents total)
- **v6.0.1**: Agent restructuring - 33 agents with category-based naming (A1-H2)
- **v6.0.0**: Clean Slate - Removed Sisyphus/OMC modes, mandatory checkpoints
- **v5.0.0**: Sisyphus protocol, paradigm detection, 27 agents
- **v4.0.0**: Context persistence, pipeline templates, integration hub
- **v3.2.0**: OMC integration, model routing
- **v3.0.0**: Creativity modules, user checkpoints, dynamic T-Score
