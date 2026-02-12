---
name: diverga-help
description: |
  Diverga help guide for Codex CLI - displays all 44 agents across 9 categories,
  available commands, usage examples, and quick start instructions.
  Triggers: help, guide, how to use, agents list, 도움말
metadata:
  short-description: Help-Guide
  version: 8.3.0
---

# Diverga Help Guide (Codex CLI)

**Version**: 8.3.0

## Overview

Displays comprehensive guide for Diverga on Codex CLI, including all 44 agents, commands, and usage examples.

## Codex CLI Degraded Mode
On Codex CLI, agents run sequentially (no parallel execution). Use skill files in `.codex/skills/diverga-{id}/SKILL.md` to load agent instructions.

## Quick Start

Describe your research and the system will guide you:
```
"I want to conduct a systematic review on AI in education"
"Help me design a qualitative study"
"I need to do a meta-analysis on technology adoption"
```

## Commands

| Command | Description |
|---------|-------------|
| diverga-setup | Initial configuration wizard |
| diverga-help | This help guide |
| diverga-memory status | Show project status |
| diverga-memory context | Display full context |
| diverga-memory init | Initialize new project |
| diverga-memory decision list | List decisions |

## All 44 Agents (9 Categories)

### Category A: Foundation (6 agents)
| ID | Name | Model | Purpose |
|----|------|-------|---------|
| A1 | ResearchQuestionRefiner | gpt-5.3-codex | Refine research questions |
| A2 | TheoreticalFrameworkArchitect | gpt-5.3-codex | Design theoretical frameworks |
| A3 | DevilsAdvocate | gpt-5.3-codex | Critical review and counterarguments |
| A4 | ResearchEthicsAdvisor | gpt-5.2-codex | IRB, ethics guidance |
| A5 | ParadigmWorldviewAdvisor | gpt-5.3-codex | Ontology/epistemology guidance |
| A6 | ConceptualFrameworkVisualizer | gpt-5.2-codex | Visualize conceptual frameworks |

### Category B: Evidence (5 agents)
| ID | Name | Model | Purpose |
|----|------|-------|---------|
| B1 | SystematicLiteratureScout | gpt-5.2-codex | Literature search strategy |
| B2 | EvidenceQualityAppraiser | gpt-5.2-codex | RoB, GRADE appraisal |
| B3 | EffectSizeExtractor | gpt-5.1-codex-mini | Extract effect sizes |
| B4 | ResearchRadar | gpt-5.1-codex-mini | Track research trends |
| B5 | ParallelDocumentProcessor | gpt-5.3-codex | Batch PDF processing |

### Category C: Design & Meta-Analysis (7 agents)
| ID | Name | Model | Purpose |
|----|------|-------|---------|
| C1 | QuantitativeDesignConsultant | gpt-5.3-codex | Quantitative design |
| C2 | QualitativeDesignConsultant | gpt-5.3-codex | Qualitative design |
| C3 | MixedMethodsDesignConsultant | gpt-5.3-codex | Mixed methods design |
| C4 | ExperimentalMaterialsDeveloper | gpt-5.2-codex | Intervention materials |
| C5 | MetaAnalysisMaster | gpt-5.3-codex | Meta-analysis orchestration |
| C6 | DataIntegrityGuard | gpt-5.2-codex | Data extraction, Hedges' g |
| C7 | ErrorPreventionEngine | gpt-5.2-codex | Error detection, anomaly alerts |

### Category D: Data Collection (4 agents)
| ID | Name | Model | Purpose |
|----|------|-------|---------|
| D1 | SamplingStrategyAdvisor | gpt-5.2-codex | Sample size, G*Power |
| D2 | InterviewFocusGroupSpecialist | gpt-5.2-codex | Interview protocols |
| D3 | ObservationProtocolDesigner | gpt-5.1-codex-mini | Observation protocols |
| D4 | MeasurementInstrumentDeveloper | gpt-5.3-codex | Scale development |

### Category E: Analysis (5 agents)
| ID | Name | Model | Purpose |
|----|------|-------|---------|
| E1 | QuantitativeAnalysisGuide | gpt-5.3-codex | Statistical analysis |
| E2 | QualitativeCodingSpecialist | gpt-5.3-codex | Thematic analysis, coding |
| E3 | MixedMethodsIntegration | gpt-5.3-codex | Integration analysis |
| E4 | AnalysisCodeGenerator | gpt-5.1-codex-mini | R/Python code generation |
| E5 | SensitivityAnalysisDesigner | gpt-5.2-codex | Robustness checks |

### Category F: Quality (5 agents)
| ID | Name | Model | Purpose |
|----|------|-------|---------|
| F1 | InternalConsistencyChecker | gpt-5.1-codex-mini | Consistency verification |
| F2 | ChecklistManager | gpt-5.1-codex-mini | PRISMA/CONSORT/STROBE |
| F3 | ReproducibilityAuditor | gpt-5.2-codex | Open Science audit |
| F4 | BiasTrustworthinessDetector | gpt-5.2-codex | Bias and trustworthiness |
| F5 | HumanizationVerifier | gpt-5.1-codex-mini | Transformation verification |

### Category G: Communication (6 agents)
| ID | Name | Model | Purpose |
|----|------|-------|---------|
| G1 | JournalMatcher | gpt-5.2-codex | Target journal selection |
| G2 | AcademicCommunicator | gpt-5.2-codex | Abstracts, summaries |
| G3 | PeerReviewStrategist | gpt-5.3-codex | Reviewer responses |
| G4 | PreregistrationComposer | gpt-5.2-codex | OSF preregistration |
| G5 | AcademicStyleAuditor | gpt-5.2-codex | AI pattern detection |
| G6 | AcademicStyleHumanizer | gpt-5.3-codex | Natural prose transformation |

### Category H: Specialized (2 agents)
| ID | Name | Model | Purpose |
|----|------|-------|---------|
| H1 | EthnographicResearchAdvisor | gpt-5.3-codex | Ethnographic design |
| H2 | ActionResearchFacilitator | gpt-5.3-codex | Action research cycles |

### Category I: Systematic Review Automation (4 agents)
| ID | Name | Model | Purpose |
|----|------|-------|---------|
| I0 | ReviewPipelineOrchestrator | gpt-5.3-codex | Pipeline coordination |
| I1 | PaperRetrievalAgent | gpt-5.2-codex | Database paper fetching |
| I2 | ScreeningAssistant | gpt-5.2-codex | PRISMA AI screening |
| I3 | RAGBuilder | gpt-5.1-codex-mini | Vector DB construction |

## Using an Agent

To use any agent in Codex CLI:
1. Read the agent's skill file: `read_file(".codex/skills/diverga-{id}/SKILL.md")`
2. Follow the instructions in the skill file
3. Check prerequisites in `.research/decision-log.yaml`
4. Stop at checkpoints and wait for user decisions

## Model Mapping
| Claude Code | Codex CLI |
|-------------|-----------|
| Opus (HIGH) | gpt-5.3-codex |
| Sonnet (MEDIUM) | gpt-5.2-codex |
| Haiku (LOW) | gpt-5.1-codex-mini |

## Related Skills
- **diverga-setup**: First-time configuration
- **diverga-memory**: Memory system management
