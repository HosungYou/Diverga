# Codex CLI Skill System: Technical Documentation

**Version**: 8.3.0
**Last Updated**: 2026-02-12
**Status**: Verified Working

---

## Executive Summary

Diverga v8.3.0 provides full **Codex CLI compatibility** through the SKILL.md-based skill loading system. Each of the 44 agents is represented as an individual skill file. This document explains:

1. How Codex CLI discovers and loads skills
2. Why AGENTS.md alone is insufficient
3. The solution implemented in Diverga
4. Key differences between Codex CLI and Claude Code
5. Recommendations for users

---

## The Problem: AGENTS.md is Not Enough

### Initial Misconception

Many developers assume that placing an `AGENTS.md` file in their project root will enable skill/agent functionality in Codex CLI. **This is incorrect.**

### AGENTS.md vs SKILL.md

| Feature | AGENTS.md | SKILL.md |
|---------|-----------|----------|
| **Purpose** | Passive documentation | Active skill definition |
| **Loading** | Context injection only | Skill system activation |
| **Behavior** | Guidelines for model behavior | Callable skill with triggers |
| **Structure** | Free-form Markdown | YAML frontmatter required |
| **Discovery** | Read during session | Explicit skill discovery |

**AGENTS.md** provides context and guidance to the model but does NOT register capabilities in the skill system.

**SKILL.md** is the actual skill definition file that Codex CLI discovers and loads into its active skill registry.

---

## How Codex CLI Skill Loading Works

### Discovery Paths

Codex CLI looks for SKILL.md files in these locations:

1. **Global**: `~/.codex/skills/<skill-name>/SKILL.md`
2. **Project-local**: `.codex/skills/<skill-name>/SKILL.md`

### SKILL.md Format

```yaml
---
name: skill-name
description: Short description (max 500 chars) that determines trigger keywords
metadata:
  short-description: Brief label
  version: X.Y.Z
---

# Skill Title

[Skill instructions and content follow...]
```

### Key Requirements

| Field | Required | Constraint |
|-------|----------|------------|
| `name` | Yes | Max 100 characters |
| `description` | Yes | Max 500 characters, includes trigger keywords |
| `metadata` | Optional | Additional metadata |

### Activation Methods

1. **Explicit**: Use `$skill-name` or `/skills` command
2. **Implicit**: Model matches user query to skill description keywords
3. **Context**: Skill activates when relevant context detected

---

## Diverga Solution: Individual SKILL.md Files

### Structure (44 Agents + Utilities)

Each Diverga agent has its own individual skill directory:

```
.codex/
└── skills/
    ├── diverga-a1/SKILL.md      # A1-ResearchQuestionRefiner
    ├── diverga-a2/SKILL.md      # A2-TheoreticalFrameworkArchitect
    ├── diverga-a3/SKILL.md      # A3-DevilsAdvocate
    ├── diverga-a4/SKILL.md      # A4-ResearchEthicsAdvisor
    ├── diverga-a5/SKILL.md      # A5-ParadigmWorldviewAdvisor
    ├── diverga-a6/SKILL.md      # A6-ConceptualFrameworkVisualizer
    ├── diverga-b1/SKILL.md      # B1-SystematicLiteratureScout
    ├── diverga-b2/SKILL.md      # B2-EvidenceQualityAppraiser
    ├── diverga-b3/SKILL.md      # B3-EffectSizeExtractor
    ├── diverga-b4/SKILL.md      # B4-ResearchRadar
    ├── diverga-b5/SKILL.md      # B5-ParallelDocumentProcessor
    ├── diverga-c1/SKILL.md      # C1-QuantitativeDesignConsultant
    ├── diverga-c2/SKILL.md      # C2-QualitativeDesignConsultant
    ├── diverga-c3/SKILL.md      # C3-MixedMethodsDesignConsultant
    ├── diverga-c4/SKILL.md      # C4-ExperimentalMaterialsDeveloper
    ├── diverga-c5/SKILL.md      # C5-MetaAnalysisMaster
    ├── diverga-c6/SKILL.md      # C6-DataIntegrityGuard
    ├── diverga-c7/SKILL.md      # C7-ErrorPreventionEngine
    ├── diverga-d1/SKILL.md      # D1-SamplingStrategyAdvisor
    ├── diverga-d2/SKILL.md      # D2-InterviewFocusGroupSpecialist
    ├── diverga-d3/SKILL.md      # D3-ObservationProtocolDesigner
    ├── diverga-d4/SKILL.md      # D4-MeasurementInstrumentDeveloper
    ├── diverga-e1/SKILL.md      # E1-QuantitativeAnalysisGuide
    ├── diverga-e2/SKILL.md      # E2-QualitativeCodingSpecialist
    ├── diverga-e3/SKILL.md      # E3-MixedMethodsIntegration
    ├── diverga-e4/SKILL.md      # E4-AnalysisCodeGenerator
    ├── diverga-e5/SKILL.md      # E5-SensitivityAnalysisDesigner
    ├── diverga-f1/SKILL.md      # F1-InternalConsistencyChecker
    ├── diverga-f2/SKILL.md      # F2-ChecklistManager
    ├── diverga-f3/SKILL.md      # F3-ReproducibilityAuditor
    ├── diverga-f4/SKILL.md      # F4-BiasTrustworthinessDetector
    ├── diverga-f5/SKILL.md      # F5-HumanizationVerifier
    ├── diverga-g1/SKILL.md      # G1-JournalMatcher
    ├── diverga-g2/SKILL.md      # G2-AcademicCommunicator
    ├── diverga-g3/SKILL.md      # G3-PeerReviewStrategist
    ├── diverga-g4/SKILL.md      # G4-PreregistrationComposer
    ├── diverga-g5/SKILL.md      # G5-AcademicStyleAuditor
    ├── diverga-g6/SKILL.md      # G6-AcademicStyleHumanizer
    ├── diverga-h1/SKILL.md      # H1-EthnographicResearchAdvisor
    ├── diverga-h2/SKILL.md      # H2-ActionResearchFacilitator
    ├── diverga-i0/SKILL.md      # I0-ReviewPipelineOrchestrator
    ├── diverga-i1/SKILL.md      # I1-PaperRetrievalAgent
    ├── diverga-i2/SKILL.md      # I2-ScreeningAssistant
    ├── diverga-i3/SKILL.md      # I3-RAGBuilder
    ├── diverga-setup/SKILL.md   # Setup wizard
    ├── diverga-memory/SKILL.md  # Memory system
    └── diverga-help/SKILL.md    # Help guide
```

### Skill Definitions

#### Example: diverga-a1/SKILL.md

```yaml
---
name: diverga-a1
description: Research question refinement agent. Helps formulate clear, answerable
             research questions with VS methodology. Triggers on research question,
             RQ, refine question, 연구 질문, 연구문제
metadata:
  short-description: A1-ResearchQuestionRefiner
  version: 8.3.0
---
```

#### Example: diverga-c5/SKILL.md

```yaml
---
name: diverga-c5
description: Meta-analysis specialist for effect size extraction, heterogeneity
             analysis, and PRISMA workflow. Triggers on meta-analysis, effect size,
             Hedges g, Cohen d, I-squared, heterogeneity, forest plot, funnel plot,
             메타분석, 효과크기
metadata:
  short-description: C5-MetaAnalysisMaster Agent
  version: 8.3.0
---
```

#### Example: diverga-i0/SKILL.md (Category I - New)

```yaml
---
name: diverga-i0
description: Systematic review pipeline orchestrator for PRISMA 2020 automation.
             Coordinates I1-I3 agents for paper retrieval, screening, and RAG building.
             Triggers on systematic review, PRISMA, literature review automation,
             체계적 문헌고찰, 프리즈마, 문헌고찰 자동화
metadata:
  short-description: I0-ReviewPipelineOrchestrator
  version: 8.3.0
---
```

#### Example: diverga-i1/SKILL.md (Category I - New)

```yaml
---
name: diverga-i1
description: Paper retrieval agent for multi-database fetching from Semantic Scholar,
             OpenAlex, and arXiv. Triggers on fetch papers, retrieve papers,
             database search, 논문 수집, 논문 검색, 데이터베이스 검색
metadata:
  short-description: I1-PaperRetrievalAgent
  version: 8.3.0
---
```

#### Example: diverga-i2/SKILL.md (Category I - New)

```yaml
---
name: diverga-i2
description: PRISMA 2020 screening assistant with AI-assisted 6-dimension screening.
             Triggers on screen papers, PRISMA screening, inclusion criteria,
             논문 스크리닝, 선별, 포함 기준
metadata:
  short-description: I2-ScreeningAssistant
  version: 8.3.0
---
```

#### Example: diverga-i3/SKILL.md (Category I - New)

```yaml
---
name: diverga-i3
description: RAG builder for vector database construction and document indexing.
             Zero-cost local embedding pipeline. Triggers on build RAG,
             vector database, embed documents, RAG 구축, 벡터 DB, 문서 임베딩
metadata:
  short-description: I3-RAGBuilder
  version: 8.3.0
---
```

#### Utility Skills

```yaml
# diverga-setup/SKILL.md
---
name: diverga-setup
description: Diverga setup wizard. Configure checkpoint levels, HUD settings,
             and project initialization. Triggers on setup, configure, initialize
metadata:
  short-description: Diverga Setup Wizard
  version: 8.3.0
---

# diverga-memory/SKILL.md
---
name: diverga-memory
description: Diverga memory system for persistent research context. Search,
             status, context, history, and export commands. Triggers on memory,
             context, recall, session, 기억, 맥락
metadata:
  short-description: Diverga Memory System
  version: 8.3.0
---

# diverga-help/SKILL.md
---
name: diverga-help
description: Diverga help guide. Shows available agents, commands, and usage
             instructions. Triggers on help, guide, documentation
metadata:
  short-description: Diverga Help Guide
  version: 8.3.0
---
```

### Prerequisite Checking

Each agent skill file includes prerequisite instructions that reference `.research/decision-log.yaml`. When an agent activates on Codex CLI, the model should:

1. Read `.research/decision-log.yaml` for prior checkpoint decisions
2. Verify all prerequisite checkpoints for the agent are approved
3. If prerequisites are missing, display the checkpoint prompt before proceeding
4. Record new decisions to `.research/decision-log.yaml`

Example prerequisite block in a SKILL.md:

```markdown
## Prerequisites

Before executing this agent, verify the following checkpoints are approved
in `.research/decision-log.yaml`:

- CP_RESEARCH_DIRECTION (required)
- CP_METHODOLOGY_APPROVAL (required)

If any prerequisite is missing, stop and ask the user to make that decision first.
```

---

## Verification

### Agent Count Verification

```bash
# Verify all 44 agent skills are installed
ls ~/.codex/skills/diverga-[a-i]*/SKILL.md | wc -l
# Expected: 44

# Verify utility skills
ls ~/.codex/skills/diverga-{setup,memory,help}/SKILL.md | wc -l
# Expected: 3

# Total skill files
ls ~/.codex/skills/diverga-*/SKILL.md | wc -l
# Expected: 47 (44 agents + 3 utilities)
```

### Category Verification

| Category | Agent Range | Count | Verified |
|----------|-------------|-------|----------|
| A: Foundation | a1-a6 | 6 | `ls ~/.codex/skills/diverga-a*/SKILL.md \| wc -l` |
| B: Evidence | b1-b5 | 5 | `ls ~/.codex/skills/diverga-b*/SKILL.md \| wc -l` |
| C: Design & Meta-Analysis | c1-c7 | 7 | `ls ~/.codex/skills/diverga-c*/SKILL.md \| wc -l` |
| D: Data Collection | d1-d4 | 4 | `ls ~/.codex/skills/diverga-d*/SKILL.md \| wc -l` |
| E: Analysis | e1-e5 | 5 | `ls ~/.codex/skills/diverga-e*/SKILL.md \| wc -l` |
| F: Quality | f1-f5 | 5 | `ls ~/.codex/skills/diverga-f*/SKILL.md \| wc -l` |
| G: Communication | g1-g6 | 6 | `ls ~/.codex/skills/diverga-g*/SKILL.md \| wc -l` |
| H: Specialized | h1-h2 | 2 | `ls ~/.codex/skills/diverga-h*/SKILL.md \| wc -l` |
| I: Systematic Review | i0-i3 | 4 | `ls ~/.codex/skills/diverga-i*/SKILL.md \| wc -l` |
| **Total** | | **44** | |

### QUANT-005 Test Results

The QUANT-005 test verified that Codex CLI properly:
1. Discovers skills from `.codex/skills/`
2. Activates skills based on trigger keywords
3. Displays checkpoint markers
4. Presents VS T-Score options
5. Supports Korean language

#### Turn 1 Results

**User Query**: "AI 튜터링 시스템이 학생 성취도에 미치는 효과에 대한 메타분석을 수행하려고 합니다."

**Codex Response**:
```
meta-analysis 스킬(C5-MetaAnalysisMaster) 사용 -- 효과크기 통일 체크포인트 진행

CHECKPOINT: CP_EFFECT_SIZE_SELECTION
효과크기 지표 옵션입니다:

[A] Cohen's d (T=0.65) - 가장 일반적
[B] Hedges' g (T=0.40) - 소표본 편향 보정, 메타분석 표준
[C] Glass's Delta (T=0.25) - 대조군 SD만 사용

어떤 지표로 통일하시겠습니까?
```

#### Verification Summary

| Verification Point | QUANT-004 (No SKILL.md) | QUANT-005 (With SKILL.md) |
|--------------------|-------------------------|---------------------------|
| Skill activation message | Not present | "meta-analysis 스킬 사용" |
| Checkpoint marker | Not present | "CHECKPOINT: CP_EFFECT_SIZE_SELECTION" |
| VS T-Score options | Not present | [A] T=0.65, [B] T=0.40, [C] T=0.25 |
| Behavioral halt | Continued without asking | "어떤 지표로 통일하시겠습니까?" |
| Korean language | Supported | Supported |

---

## Claude Code vs Codex CLI: Feature Comparison

### Capability Matrix (v8.3.0)

| Feature | Claude Code | Codex CLI |
|---------|-------------|-----------|
| **Skill Loading** | Native plugin system | SKILL.md files (44 individual skills) |
| **Task Tool** | Full support (parallel agents) | Not available |
| **AskUserQuestion Tool** | Clickable UI | Text-only |
| **MCP Checkpoints** | 7 MCP tools for runtime enforcement | Behavioral only |
| **Checkpoint Enforcement** | Tool-level blocking (cannot bypass) | Behavioral (model should wait) |
| **Agent Dispatch** | `Task(subagent_type="diverga:a1")` | Main model follows skill instructions |
| **Parallel Agents** | Multiple Task calls simultaneously | Sequential only |
| **Model Routing** | opus/sonnet/haiku per agent | gpt-5.3-codex/gpt-5.2-codex/gpt-5.1-codex-mini (session model) |
| **Prerequisite Gate** | MCP `diverga_check_prerequisites()` | Manual `.research/decision-log.yaml` check |
| **Memory System** | 3-layer auto-loading | Manual file reading |
| **Context Persistence** | Full session context + MCP state | Session context + file-based state |
| **VS Methodology** | T-Score options | T-Score options |
| **Korean Support** | Full | Full |
| **Category I (ScholaRAG)** | Full with SCH_* MCP checkpoints | Behavioral SCH_* checkpoints |

### What This Means

| Aspect | Claude Code | Codex CLI |
|--------|-------------|-----------|
| **Checkpoint Blocking** | System prevents proceeding | Model chooses to wait |
| **Agent Execution** | Dedicated agent instances | Main model follows instructions |
| **User Interaction** | Rich UI components | Plain text prompts |
| **Reliability** | Tool-enforced behavior | Prompt-guided behavior |
| **Prerequisite Verification** | Automated via MCP | Manual via file reading |

---

## Recommendations

### For Full Diverga Experience

**Use Claude Code** when you need:
- Tool-level checkpoint enforcement (cannot bypass)
- 44 specialized agents via Task tool
- AskUserQuestion with clickable options
- Parallel agent execution
- MCP runtime checkpoint verification
- Highest reliability research workflows
- Category I systematic review automation with SCH_* checkpoints

### For Basic Research Assistance

**Codex CLI works well** for:
- Effect size calculations and conversions
- Literature review guidance
- Methodology consultation
- VS methodology (creative alternatives)
- Korean language support
- Individual agent consultations

### Installation Guide

#### Claude Code (Recommended)

```bash
# Full plugin installation
/plugin marketplace add https://github.com/HosungYou/Diverga
/plugin install diverga
```

#### Codex CLI

```bash
# Option 1: Install script (recommended)
curl -fsSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-multi-cli.sh | bash -s -- --codex

# Option 2: NPM package
npx @diverga/codex-setup

# Option 3: Manual
# Copy individual skill directories to ~/.codex/skills/
git clone https://github.com/HosungYou/Diverga.git
cp -r Diverga/.codex/skills/diverga-* ~/.codex/skills/
```

---

## Technical Notes

### Why Behavioral vs Tool-Level Matters

**Tool-Level Checkpoint (Claude Code)**:
```
System: CHECKPOINT triggered via MCP
-> Claude Code UI blocks further input
-> User MUST click option to continue
-> Impossible to bypass without user action
-> Decision auto-recorded to .research/decision-log.yaml
```

**Behavioral Checkpoint (Codex CLI)**:
```
Model: CHECKPOINT displayed in text
-> Model asks "어떤 방향으로 진행하시겠습니까?"
-> Model SHOULD wait for response
-> Technically model could continue (rare, but possible)
-> Model should write decision to .research/decision-log.yaml
```

### SKILL.md Best Practices

1. **Keep description under 500 characters** - Codex truncates longer descriptions
2. **Include all trigger keywords** - These determine when skill activates
3. **Use clear activation messages** - Help users confirm skill loading
4. **Provide behavioral instructions** - Clear "DO" and "DON'T" sections
5. **Include prerequisite checks** - Reference `.research/decision-log.yaml` for gate verification
6. **One agent per skill file** - Individual files for each of the 44 agents

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 8.3.0 | 2026-02-12 | Updated to 44 agents (added Category I: I0-I3), individual skill files per agent, prerequisite checking via `.research/decision-log.yaml`, model mapping updated to gpt-5.3-codex/gpt-5.2-codex/gpt-5.1-codex-mini |
| 6.6.2 | 2026-01-30 | Initial Codex SKILL.md implementation with 3 bundled skills, QUANT-005 verification complete |

---

## Related Documents

- [README.md](../README.md) - Main Diverga documentation
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [CROSS-PLATFORM-GUIDE.md](CROSS-PLATFORM-GUIDE.md) - Multi-platform installation and usage
- [PLATFORM-LIMITATIONS.md](PLATFORM-LIMITATIONS.md) - Feature portability analysis
- [qa/protocol/test_quant_005.yaml](../qa/protocol/test_quant_005.yaml) - Test protocol
