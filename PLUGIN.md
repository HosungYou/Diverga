# Diverga

**Version**: 6.8.0
**Author**: Hosung You
**Repository**: https://github.com/HosungYou/Diverga
**License**: MIT

---

## Description

Diverga is an AI Research Assistant for the complete research lifecycle. 44 specialized agents support researchers from question formulation to publication, with context persistence and creative methodology guidance.

**Key Features:**
- 44 specialized research agents across 9 categories
- **Memory System for context persistence** (v6.8+)
- **Parallel execution via Task tool** (v6.5+)
- Auto-trigger based on conversation context
- Human checkpoints for critical decisions
- Verbalized Sampling (VS) methodology for creative alternatives
- Multi-language support (English, Korean)

---

## Directory Structure (v6.5.2+)

```
diverga/
├── agents/              # 40 agent definitions (Task tool)
│   ├── a1.md           # → Task(subagent_type="diverga:a1", ...)
│   ├── a2.md
│   └── ...
├── skills/              # Skill definitions (Skill tool)
│   ├── research-coordinator/
│   ├── setup/
│   └── ...
└── .claude-plugin/
    └── marketplace.json  # Plugin registration
```

**Important**: Both `/agents/` and `/skills/` are auto-discovered by Claude Code.
Do NOT add explicit `skills` key in marketplace.json.

---

## Quick Start

```
# Step 1: Add to marketplace
/plugin marketplace add https://github.com/HosungYou/Diverga

# Step 2: Install
/plugin install diverga

# Step 3: Setup
/diverga:setup
```

---

## Skills

| Skill | Command | Description |
|-------|---------|-------------|
| Setup | `/diverga:setup` | Initial configuration wizard |
| Help | `/diverga:help` | Agent list and usage guide |
| Memory | `/diverga:memory` | Context persistence for research lifecycle |
| Meta-Analysis | `/diverga:meta-analysis` | Meta-analysis workflow (C5+C6+C7) |
| PDF Extraction | `/diverga:pdf-extract` | Extract data from PDFs (C6) |

---

## Agents (44 total)

### Category A: Foundation (6 agents)

| Agent | Command | Description | Model |
|-------|---------|-------------|-------|
| A1-ResearchQuestionRefiner | `diverga:a1` | Refine and sharpen research questions | opus |
| A2-TheoreticalFrameworkArchitect | `diverga:a2` | Design theoretical frameworks | opus |
| A3-DevilsAdvocate | `diverga:a3` | Critical review and counterarguments | opus |
| A4-ResearchEthicsAdvisor | `diverga:a4` | IRB and ethics guidance | sonnet |
| A5-ParadigmWorldviewAdvisor | `diverga:a5` | Ontology, epistemology guidance | opus |
| A6-ConceptualFrameworkVisualizer | `diverga:a6` | Visualize conceptual frameworks | sonnet |

### Category B: Evidence (5 agents)

| Agent | Command | Description | Model |
|-------|---------|-------------|-------|
| B1-SystematicLiteratureScout | `diverga:b1` | Systematic literature search | sonnet |
| B2-EvidenceQualityAppraiser | `diverga:b2` | Quality appraisal (RoB, GRADE) | sonnet |
| B3-EffectSizeExtractor | `diverga:b3` | Extract effect sizes from papers | haiku |
| B4-ResearchRadar | `diverga:b4` | Track research trends | haiku |
| B5-ParallelDocumentProcessor | `diverga:b5` | Batch PDF processing | opus |

### Category C: Design & Meta-Analysis (7 agents)

| Agent | Command | Description | Model |
|-------|---------|-------------|-------|
| C1-QuantitativeDesignConsultant | `diverga:c1` | Quantitative research design | opus |
| C2-QualitativeDesignConsultant | `diverga:c2` | Qualitative research design | opus |
| C3-MixedMethodsDesignConsultant | `diverga:c3` | Mixed methods design | opus |
| C4-ExperimentalMaterialsDeveloper | `diverga:c4` | Develop intervention materials | sonnet |
| C5-MetaAnalysisMaster | `diverga:c5` | Meta-analysis orchestration | opus |
| C6-DataIntegrityGuard | `diverga:c6` | Data extraction with provenance | sonnet |
| C7-ErrorPreventionEngine | `diverga:c7` | Error detection and validation | sonnet |

### Category D: Data Collection (4 agents)

| Agent | Command | Description | Model |
|-------|---------|-------------|-------|
| D1-SamplingStrategyAdvisor | `diverga:d1` | Sampling strategy guidance | sonnet |
| D2-InterviewFocusGroupSpecialist | `diverga:d2` | Interview/focus group design | sonnet |
| D3-ObservationProtocolDesigner | `diverga:d3` | Observation protocol design | haiku |
| D4-MeasurementInstrumentDeveloper | `diverga:d4` | Instrument development | opus |

### Category E: Analysis (5 agents)

| Agent | Command | Description | Model |
|-------|---------|-------------|-------|
| E1-QuantitativeAnalysisGuide | `diverga:e1` | Statistical analysis guidance | opus |
| E2-QualitativeCodingSpecialist | `diverga:e2` | Qualitative coding support | opus |
| E3-MixedMethodsIntegration | `diverga:e3` | Mixed methods integration | opus |
| E4-AnalysisCodeGenerator | `diverga:e4` | Generate R/Python code | haiku |
| E5-SensitivityAnalysisDesigner | `diverga:e5` | Sensitivity analysis design | sonnet |

### Category F: Quality (5 agents)

| Agent | Command | Description | Model |
|-------|---------|-------------|-------|
| F1-InternalConsistencyChecker | `diverga:f1` | Check internal consistency | haiku |
| F2-ChecklistManager | `diverga:f2` | Manage research checklists | haiku |
| F3-ReproducibilityAuditor | `diverga:f3` | Audit reproducibility | sonnet |
| F4-BiasTrustworthinessDetector | `diverga:f4` | Detect bias and trustworthiness | sonnet |
| F5-HumanizationVerifier | `diverga:f5` | Verify humanization quality | haiku |

### Category G: Communication (6 agents)

| Agent | Command | Description | Model |
|-------|---------|-------------|-------|
| G1-JournalMatcher | `diverga:g1` | Match journals to manuscripts | sonnet |
| G2-AcademicCommunicator | `diverga:g2` | Academic writing support | sonnet |
| G3-PeerReviewStrategist | `diverga:g3` | Peer review response strategy | sonnet |
| G4-PreregistrationComposer | `diverga:g4` | Compose preregistrations | sonnet |
| G5-AcademicStyleAuditor | `diverga:g5` | Audit academic style | sonnet |
| G6-AcademicStyleHumanizer | `diverga:g6` | Humanize AI-generated text | opus |

### Category H: Specialized (2 agents)

| Agent | Command | Description | Model |
|-------|---------|-------------|-------|
| H1-EthnographicResearchAdvisor | `diverga:h1` | Ethnographic research guidance | opus |
| H2-ActionResearchFacilitator | `diverga:h2` | Action research facilitation | opus |

### Category I: Systematic Review Automation (4 agents)

| Agent | Command | Description | Model |
|-------|---------|-------------|-------|
| I0-ScholarAgentOrchestrator | `diverga:i0` | Pipeline coordination and stage management | opus |
| I1-PaperRetrievalAgent | `diverga:i1` | Multi-database fetching (Semantic Scholar, OpenAlex, arXiv) | sonnet |
| I2-ScreeningAssistant | `diverga:i2` | AI-PRISMA 6-dimension screening | sonnet |
| I3-RAGBuilder | `diverga:i3` | Vector database construction (zero cost) | haiku |

---

## Auto-Trigger Keywords

Diverga automatically detects keywords and activates appropriate agents:

| Keywords (English) | Keywords (Korean) | Agent |
|-------------------|-------------------|-------|
| "research question", "RQ" | "연구 질문", "연구문제" | diverga:a1 |
| "theoretical framework" | "이론적 프레임워크" | diverga:a2 |
| "devil's advocate", "critique" | "반론", "비판적 검토" | diverga:a3 |
| "IRB", "ethics" | "연구 윤리", "IRB" | diverga:a4 |
| "meta-analysis", "effect size" | "메타분석", "효과크기" | diverga:c5 |
| "data extraction", "PDF extract" | "데이터 추출", "PDF 추출" | diverga:c6 |
| "systematic review", "PRISMA" | "체계적 문헌고찰" | diverga:b1 |
| "qualitative", "interview" | "질적 연구", "인터뷰" | diverga:c2 |

---

## Agent Invocation (Task Tool)

Agents are invoked via the Task tool with `subagent_type` parameter:

```python
# Single agent invocation
Task(
    subagent_type="diverga:c5",
    model="opus",
    description="Meta-analysis orchestration",
    prompt="Validate the extracted effect sizes from 50 studies..."
)

# Parallel agents (independent tasks)
Task(subagent_type="diverga:b1", model="sonnet", prompt="Literature search...")
Task(subagent_type="diverga:b2", model="sonnet", prompt="Quality appraisal...")

# Sequential pipeline (dependent tasks)
# 1. First: C5 orchestration
# 2. Then: C6 extraction
# 3. Finally: C7 validation
```

### Model Routing

| Tier | Model | Use For |
|------|-------|---------|
| HIGH | `opus` | Complex reasoning, architecture decisions |
| MEDIUM | `sonnet` | Standard implementation, extraction |
| LOW | `haiku` | Simple lookups, quick tasks |

### Agent-Model Mapping

```
opus:   A1, A2, A3, A5, B5, C1, C2, C3, C5, D4, E1, E2, E3, G6, H1, H2, I0
sonnet: A4, A6, B1, B2, C4, C6, C7, D1, D2, E5, F3, F4, G1, G2, G3, G4, G5, I1, I2
haiku:  B3, B4, D3, E4, F1, F2, F5, I3
```

---

## Configuration

Configuration file: `~/.claude/plugins/diverga/config/diverga-config.json`

```json
{
  "version": "6.4.0",
  "llm_provider": "anthropic",
  "llm_api_key_env": "ANTHROPIC_API_KEY",
  "human_checkpoints": {
    "enabled": true,
    "required": ["CP_PARADIGM", "CP_METHODOLOGY"]
  },
  "default_paradigm": "auto",
  "language": "auto"
}
```

---

## Human Checkpoints

| Checkpoint | When | Required |
|------------|------|----------|
| CP_PARADIGM | Research paradigm selection | Yes |
| CP_METHODOLOGY | Methodology approval | Yes |
| CP_THEORY | Theory framework selection | Optional |
| CP_DATA_VALIDATION | Data extraction validation | Optional |

---

## Requirements

- Claude Code CLI
- LLM API Key (one of: Anthropic, OpenAI, Groq)

---

## Support

- GitHub Issues: https://github.com/HosungYou/Diverga/issues
- Documentation: https://github.com/HosungYou/Diverga/docs

---

*Version 6.8.0 - Memory System Edition*
