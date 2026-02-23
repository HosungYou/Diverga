---
name: help
description: |
  Diverga help guide - displays all 44 agents, commands, and usage examples.
  Triggers: help, guide, how to use, 도움말
version: "10.3.0"
---

# /diverga:help

**Version**: 1.0.0
**Trigger**: `/diverga:help`

## Description

Displays comprehensive guide for Diverga, including all 40 agents, commands, and usage examples.

## Output

When user invokes `/diverga:help`, display:

```
╔══════════════════════════════════════════════════════════════════╗
║                     Diverga v6.4.0 Help                          ║
║         AI Research Assistant - 40 Agents, 8 Categories          ║
╚══════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────┐
│                        QUICK START                               │
├─────────────────────────────────────────────────────────────────┤
│ Just describe your research:                                     │
│   "I want to conduct a meta-analysis on AI in education"        │
│   "Help me design a qualitative study"                          │
│   "메타분석 연구를 시작하고 싶어"                                  │
│                                                                  │
│ Diverga auto-detects context and activates relevant agents.      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         COMMANDS                                 │
├─────────────────────────────────────────────────────────────────┤
│ /diverga:setup          Initial configuration wizard            │
│ /diverga:doctor         System diagnostics & health check       │
│ /diverga:help           This help guide                         │
│ /diverga:meta-analysis  Meta-analysis workflow (C5+C6+C7)       │
│ /diverga:pdf-extract    Extract data from PDFs (C6)             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│              CATEGORY A: FOUNDATION (6 agents)                   │
├─────────────────────────────────────────────────────────────────┤
│ diverga:a1  ResearchQuestionRefiner     Refine research Qs      │
│ diverga:a2  TheoreticalFrameworkArchitect  Design frameworks    │
│ diverga:a3  DevilsAdvocate              Critical review         │
│ diverga:a4  ResearchEthicsAdvisor       IRB, ethics guidance    │
│ diverga:a5  ParadigmWorldviewAdvisor    Ontology guidance       │
│ diverga:a6  ConceptualFrameworkVisualizer  Visualize concepts   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│              CATEGORY B: EVIDENCE (5 agents)                     │
├─────────────────────────────────────────────────────────────────┤
│ diverga:b1  SystematicLiteratureScout   Literature search       │
│ diverga:b2  EvidenceQualityAppraiser    RoB, GRADE appraisal    │
│ diverga:b3  EffectSizeExtractor         Extract effect sizes    │
│ diverga:b4  ResearchRadar               Track research trends   │
│ diverga:b5  ParallelDocumentProcessor   Batch PDF processing    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│         CATEGORY C: DESIGN & META-ANALYSIS (7 agents)            │
├─────────────────────────────────────────────────────────────────┤
│ diverga:c1  QuantitativeDesignConsultant  Quant design          │
│ diverga:c2  QualitativeDesignConsultant   Qual design           │
│ diverga:c3  MixedMethodsDesignConsultant  Mixed methods         │
│ diverga:c4  ExperimentalMaterialsDeveloper  Interventions       │
│ diverga:c5  MetaAnalysisMaster ⭐         Meta-analysis lead    │
│ diverga:c6  DataIntegrityGuard ⭐         Data extraction       │
│ diverga:c7  ErrorPreventionEngine ⭐      Error detection       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│            CATEGORY D: DATA COLLECTION (4 agents)                │
├─────────────────────────────────────────────────────────────────┤
│ diverga:d1  SamplingStrategyAdvisor     Sampling guidance       │
│ diverga:d2  InterviewFocusGroupSpecialist  Interview design     │
│ diverga:d3  ObservationProtocolDesigner  Observation protocol   │
│ diverga:d4  MeasurementInstrumentDeveloper  Instrument dev      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│              CATEGORY E: ANALYSIS (5 agents)                     │
├─────────────────────────────────────────────────────────────────┤
│ diverga:e1  QuantitativeAnalysisGuide   Statistical guidance    │
│ diverga:e2  QualitativeCodingSpecialist  Qualitative coding     │
│ diverga:e3  MixedMethodsIntegration     Integration methods     │
│ diverga:e4  AnalysisCodeGenerator       R/Python code           │
│ diverga:e5  SensitivityAnalysisDesigner  Sensitivity analysis   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│               CATEGORY F: QUALITY (5 agents)                     │
├─────────────────────────────────────────────────────────────────┤
│ diverga:f1  InternalConsistencyChecker  Check consistency       │
│ diverga:f2  ChecklistManager            Research checklists     │
│ diverga:f3  ReproducibilityAuditor      Audit reproducibility   │
│ diverga:f4  BiasTrustworthinessDetector  Detect bias            │
│ diverga:f5  HumanizationVerifier        Verify humanization     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│            CATEGORY G: COMMUNICATION (6 agents)                  │
├─────────────────────────────────────────────────────────────────┤
│ diverga:g1  JournalMatcher              Match journals          │
│ diverga:g2  AcademicCommunicator        Academic writing        │
│ diverga:g3  PeerReviewStrategist        Review response         │
│ diverga:g4  PreregistrationComposer     Compose preregistration │
│ diverga:g5  AcademicStyleAuditor        AI pattern detection    │
│ diverga:g6  AcademicStyleHumanizer      Humanize AI text        │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│             CATEGORY H: SPECIALIZED (2 agents)                   │
├─────────────────────────────────────────────────────────────────┤
│ diverga:h1  EthnographicResearchAdvisor  Ethnography guidance   │
│ diverga:h2  ActionResearchFacilitator   Action research         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    HUMAN CHECKPOINTS                             │
├─────────────────────────────────────────────────────────────────┤
│ 🔴 REQUIRED (System STOPS):                                      │
│    CP_PARADIGM       Research paradigm selection                 │
│    CP_METHODOLOGY    Methodology approval                        │
│                                                                  │
│ 🟠 RECOMMENDED (System PAUSES):                                  │
│    CP_THEORY         Theory framework selection                  │
│    CP_DATA_VALIDATION Data extraction validation                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                   MODEL ROUTING                                  │
├─────────────────────────────────────────────────────────────────┤
│ HIGH (Opus):   A1,A2,A3,A5,B5,C1,C2,C3,C5,D4,E1,E2,E3,G6,H1,H2 │
│ MEDIUM (Sonnet): A4,A6,B1,B2,C4,C6,C7,D1,D2,E5,F3,F4,G1-G5     │
│ LOW (Haiku):   B3,B4,D3,E4,F1,F2,F5                             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                 AUTO-TRIGGER KEYWORDS                            │
├─────────────────────────────────────────────────────────────────┤
│ "research question", "RQ", "연구 질문"        → diverga:a1      │
│ "theoretical framework", "이론적 프레임워크"  → diverga:a2      │
│ "devil's advocate", "critique", "반론"       → diverga:a3      │
│ "IRB", "ethics", "연구 윤리"                 → diverga:a4      │
│ "meta-analysis", "메타분석", "효과크기"       → diverga:c5      │
│ "data extraction", "PDF extract"            → diverga:c6      │
│ "systematic review", "PRISMA"               → diverga:b1      │
│ "qualitative", "interview", "질적 연구"      → diverga:c2      │
└─────────────────────────────────────────────────────────────────┘

For more info: https://github.com/HosungYou/Diverga
```

## Direct Agent Invocation

Users can invoke specific agents:

```
diverga:c5   # Invoke Meta-Analysis Master directly
diverga:a1   # Invoke Research Question Refiner
```

## Implementation Notes

- Help content adapts to user's language preference
- Agent recommendations based on detected research context
- Links to GitHub for full documentation
