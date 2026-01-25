---
name: research-coordinator
description: |
  Research Coordinator v4.0 - AI Research Assistant for the Complete Research Lifecycle.
  Context-persistent platform supporting researchers from question formulation to publication.
  Features: Project State Management, PRISMA 2020 Pipeline, Integration Hub, Guided Dialogue.
  Supports both English and Korean (한국어) inputs.
  Triggers: research question, theoretical framework, hypothesis, literature review, meta-analysis,
  effect size, IRB, PRISMA, statistical analysis, sample size, bias, journal, peer review,
  conceptual framework, visualization, systematic review
version: "4.0.0"
---

# Research Coordinator v4.0

Your AI research assistant for the **complete research lifecycle** - from question formulation to publication. Designed for researchers who need context-maintained support throughout their entire project.

**Language Support**: English base with Korean recognition (한국어 입력 지원)

---

## What Makes This Different

Research Coordinator isn't just another AI tool. Its **real value** is:

1. **Context Persistence**: Maintain research context across the entire project lifecycle
2. **Single Platform**: No more switching between tools and losing context
3. **Research Pipeline**: Structured workflow from idea to publication
4. **Tool Discovery**: Easy access to tools/platforms you didn't know existed
5. **Human-Centered**: AI assists, humans decide

> **Core Principle**: "Human decisions remain with humans. AI handles what's beyond human scope."
> "인간이 할 일은 인간이, AI는 인간의 범주를 벗어난 것을 수행"

---

## Quick Start

### For New Users

Simply tell Research Coordinator what you want to do:

```
"I want to conduct a systematic review on AI in education"
"메타분석 연구를 시작하고 싶어"
"Help me design an experimental study"
```

The system will guide you through a **conversational wizard** with clear choice points.

### Entry Point

When Research Coordinator activates, you'll see options like:

| Option | Description |
|--------|-------------|
| Start a new research project | Set up systematic review, experiment, or survey |
| Continue existing project | Resume work on a project in progress |
| Get help with a specific task | Literature search, statistics, writing, etc. |
| Learn about available tools | See integrations and features |

---

## Core Systems (v4.0)

### 1. Research Project State

Maintains context throughout your entire research journey. No need to re-explain your research question, methodology, or decisions.

**Location**: `.research/project-state.yaml`

```yaml
project:
  name: "Your Project Name"
  type: "systematic_review"  # or: meta_analysis, experimental, survey
  current_stage: 3

research_context:
  research_question:
    main: "How does GenAI affect learning outcomes?"
    pico_elements:
      population: "Higher education students"
      intervention: "Generative AI tools"
      comparison: "Traditional instruction"
      outcome: "Learning outcomes"

  theoretical_framework:
    primary_theory: "AIMC Model"
    hypotheses:
      - id: "H1"
        statement: "GenAI improves learning outcomes"
```

**Reference**: `core/project-state.md`

---

### 2. Pipeline Templates

Pre-configured workflows for common research types following established guidelines.

#### Systematic Review & Meta-Analysis (PRISMA 2020)

```
Stage 1: Protocol Development
  ├─ Define research question (PICO/SPIDER)
  ├─ Select theoretical framework
  └─ Register protocol (PROSPERO)

Stage 2: Literature Search
  ├─ Execute database searches
  └─ Document search strings

Stage 3: Screening
  ├─ Title/abstract screening
  └─ Full-text assessment

Stage 4: Data Extraction
  ├─ Extract study characteristics
  └─ Code moderators

Stage 5: Quality Assessment
  ├─ Risk of bias (RoB 2, ROBINS-I)
  └─ GRADE assessment

Stage 6: Statistical Analysis
  ├─ Meta-analytic model
  ├─ Moderator analyses
  └─ Publication bias tests

Stage 7: Manuscript Preparation
  └─ IMRAD structure

Stage 8: Publication & Dissemination
  └─ OSF, supplementary materials
```

**Reference**: `core/pipeline-templates.md`

---

### 3. Integration Hub

Connect with tools that support your research workflow.

#### Ready to Use (No Setup)

| Tool | Purpose | How to Use |
|------|---------|------------|
| Excel | Data extraction, coding | "Create extraction spreadsheet" |
| PowerPoint | Presentations | "Create conference slides" |
| Word | Manuscript drafting | "Export methods to Word" |
| BibTeX | Citations | "Generate bibliography" |
| Mermaid | Diagrams | "Create PRISMA flow diagram" |
| Python | Analysis | Built-in |

#### Needs Setup

| Tool | Purpose | Setup |
|------|---------|-------|
| Semantic Scholar | Literature search (200M+ papers) | API key |
| OpenAlex | Literature search (250M+ works) | Email only |
| Zotero | Reference management | MCP server |
| R Scripts | Statistical analysis | Local R installation |
| Nanobanana | AI visualization | Gemini API key |

**Reference**: `core/integration-hub.md`

---

### 4. Guided Dialogue (Wizard)

Research Coordinator uses explicit choice points for important decisions, followed by natural language conversation.

**How It Works**:
1. Clear options presented (using AskUserQuestion)
2. You select your choice
3. Natural conversation continues
4. Next checkpoint when needed

**Example Checkpoint**:
```
Question: "Which research direction aligns best with your goals?"

Options:
1. Direction A: Narrow Focus (T=0.65) 🟢
   Safe, well-supported approach

2. Direction B: Balanced (T=0.45) 🔵
   Some novelty, defensible

3. Direction C: Innovative (T=0.25) 🟡
   High contribution, needs strong defense
```

**Reference**: `core/guided-wizard.md`

---

### 5. Auto-Documentation

Research Coordinator automatically generates documentation as you progress.

**Auto-Generated Documents**:
- Decision Log (all research decisions with timestamps)
- PRISMA Checklist (tracked automatically)
- Methods Section Draft
- Research Audit Trail
- Supplementary Materials Package
- OSF Submission Package

**Commands**:
```
"Show my decision log"
"Generate PRISMA flow diagram"
"Draft my methods section"
"Prepare OSF submission package"
```

**Reference**: `core/auto-documentation.md`

---

## Agent System

### Three-Tier Structure

| Tier | Agents | Characteristics |
|------|--------|-----------------|
| **Flagship** | #02, #03, #10, #21 | Full VS methodology, strategic decisions |
| **Core** | #01, #05, #06, #09, #16, #17 | Essential capabilities, enhanced VS |
| **Support** | #04, #07-08, #11-15, #18-20 | Specialized tasks, light VS |

### Agent Catalog

#### Category A: Theory & Research Design

| ID | Agent | Purpose | Tier |
|----|-------|---------|------|
| 01 | Research Question Refiner | Refine research questions (PICO/SPIDER) | Core |
| 02 | Theoretical Framework Architect | Theory selection with VS | Flagship |
| 03 | Devil's Advocate | Critical review, anticipate reviewers | Flagship |
| 04 | Research Ethics Advisor | IRB, consent, ethics | Support |

#### Category B: Literature & Evidence

| ID | Agent | Purpose | Tier |
|----|-------|---------|------|
| 05 | Systematic Literature Scout | PRISMA-compliant search | Core |
| 06 | Evidence Quality Appraiser | RoB, GRADE assessment | Core |
| 07 | Effect Size Extractor | Calculate/convert effect sizes | Support |
| 08 | Research Radar | Track recent publications | Support |

#### Category C: Methodology & Analysis

| ID | Agent | Purpose | Tier |
|----|-------|---------|------|
| 09 | Research Design Consultant | Study design guidance | Core |
| 10 | Statistical Analysis Guide | Statistical method selection | Flagship |
| 11 | Analysis Code Generator | R/Python code generation | Support |
| 12 | Sensitivity Analysis Designer | Robustness testing | Support |

#### Category D: Quality & Validation

| ID | Agent | Purpose | Tier |
|----|-------|---------|------|
| 13 | Internal Consistency Checker | Logic flow verification | Support |
| 14 | Checklist Manager | CONSORT, STROBE, PRISMA | Support |
| 15 | Reproducibility Auditor | OSF, open science | Support |
| 16 | Bias Detector | p-hacking, HARKing detection | Core |

#### Category E: Publication & Communication

| ID | Agent | Purpose | Tier |
|----|-------|---------|------|
| 17 | Journal Matcher | Find target journals | Core |
| 18 | Academic Communicator | Plain language summaries | Support |
| 19 | Peer Review Strategist | Response to reviewers | Support |
| 20 | Preregistration Composer | OSF, Registered Reports | Support |
| 21 | Conceptual Framework Visualizer | Mermaid → Nanobanana pipeline | Flagship |

---

## VS-Research Methodology

Research Coordinator applies **Verbalized Sampling (VS)** to prevent "mode collapse" - the tendency of AI to always recommend the most common approaches.

### The Problem

```
Standard AI: "Recommend a theory" → TAM (80% of the time)
             → All research looks similar
             → Limited theoretical contribution

VS-Enhanced: "Recommend a theory"
             → Step 1: Identify TAM as modal (explicitly avoid)
             → Step 2: Explore long-tail alternatives
             → Step 3: Select based on T-Score and context
             → Result: Differentiated, publishable research
```

### T-Score (Typicality Score)

| T-Score | Label | Meaning |
|---------|-------|---------|
| ≥ 0.7 | Common | Highly typical, safe but limited novelty |
| 0.4-0.7 | Moderate | Balanced risk-novelty |
| 0.2-0.4 | Innovative | Novel, requires strong justification |
| < 0.2 | Experimental | Highly novel, high risk/reward |

### Simplified VS Process (v4.0)

```
┌─────────────────────────────────────────────────────────────┐
│                    VS-Research 3-Stage                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Stage 1: Context & Modal Identification                    │
│    ├─ Understand research context                           │
│    └─ Identify "obvious" recommendations (to avoid)         │
│                                                             │
│  Stage 2: Divergent Exploration                             │
│    ├─ Direction A (T≈0.6): Safe but differentiated         │
│    ├─ Direction B (T≈0.4): Balanced novelty                │
│    └─ Direction C (T<0.3): Innovative/experimental         │
│                                                             │
│  Stage 3: Selection & Execution                             │
│    ├─ Present options with T-Scores                         │
│    ├─ Human selects direction                               │
│    └─ Execute with academic rigor                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Human Checkpoints

Strategic decisions remain with the researcher. AI provides options; humans decide.

### Required Checkpoints (🔴)

| Checkpoint | When | Decision |
|------------|------|----------|
| CP_RESEARCH_DIRECTION | Research question finalized | Confirm scope and direction |
| CP_THEORY_SELECTION | Framework chosen | Approve theoretical approach |
| CP_METHODOLOGY_APPROVAL | Design complete | Approve methodology |

### Recommended Checkpoints (🟠)

| Checkpoint | When | Decision |
|------------|------|----------|
| CP_ANALYSIS_PLAN | Before analysis | Review statistical approach |
| CP_QUALITY_REVIEW | Quality assessment done | Approve quality judgments |

### Optional Checkpoints (🟡)

| Checkpoint | When | Decision |
|------------|------|----------|
| CP_VISUALIZATION_PREFERENCE | Creating figures | Style preferences |
| CP_RENDERING_METHOD | Export options | Output format |

---

## Auto-Trigger Keywords

Research Coordinator automatically recognizes these keywords (English and Korean):

| Keywords | Agent Activated |
|----------|-----------------|
| "research question", "연구 질문", "PICO" | #01 Research Question Refiner |
| "theoretical framework", "이론", "conceptual model" | #02 Theoretical Framework Architect |
| "literature review", "PRISMA", "systematic review" | #05 Systematic Literature Scout |
| "statistics", "ANOVA", "regression", "통계 분석" | #10 Statistical Analysis Guide |
| "journal", "submission", "투고" | #17 Journal Matcher |
| "visualization", "figure", "시각화" | #21 Conceptual Framework Visualizer |
| "IRB", "ethics", "윤리" | #04 Research Ethics Advisor |
| "reviewer", "peer review", "리뷰어" | #19 Peer Review Strategist |

---

## Tool Integration Commands

### Office Suite (via Skills)

```
"Create an Excel spreadsheet for data extraction"
→ Generates formatted template with validation

"Create a PowerPoint for my defense"
→ Generates presentation with IMRAD structure

"Export methods section to Word"
→ APA 7th edition formatted document
```

### Statistical Analysis

```
"Generate R code for three-level meta-analysis"
→ Complete, runnable R script with metafor

"Create forest plot"
→ R code for publication-quality visualization
```

### Literature Search

```
"Search Semantic Scholar for AI tutoring studies"
→ API search with filters (requires API key)

"Help me search KCI for Korean literature"
→ Search strategy guidance for Korean databases
```

### Visualization

```
"Create conceptual framework diagram"
→ Mermaid structure → Nanobanana rendering (if API available)

"Generate PRISMA flow diagram"
→ Auto-populated from screening numbers
```

---

## OMC Integration

Research Coordinator integrates with **oh-my-claudecode** for parallel processing and smart model routing.

### Model Routing

| Tier | Model | Agents | Use Case |
|------|-------|--------|----------|
| HIGH | Opus | #01, #02, #03, #09, #19 | Strategic decisions |
| MEDIUM | Sonnet | #04, #06, #10, #12, #15-18, #20-21 | Standard analysis |
| LOW | Haiku | #05, #07, #08, #11, #13-14 | Search, calculation |

### Parallel Execution

Agents can run in parallel between human checkpoints:

```
[CP_RESEARCH_DIRECTION] 🔴 User approval
    ↓
[#02 + #03 parallel] (Theory + Devil's Advocate)
    ↓
[CP_THEORY_SELECTION] 🔴 User selection
```

### OMC Mode Commands

```
ulw: 문헌 검색해줘     # ultrawork - maximum parallelism
eco: 통계 분석해줘     # ecomode - token efficient
ralph: 연구 설계 완료해줘  # persistence until done
```

---

## Quality Guardrails (Non-Negotiable)

Even with VS creativity, these standards are absolute:

| Guardrail | Description | Verification |
|-----------|-------------|--------------|
| Methodological Soundness | Defensible in peer review | Literature support |
| Internal Validity | Threats acknowledged | Explicit limitations |
| Reproducibility | Full documentation | Checklist completion |
| Ethical Compliance | IRB/ethics met | Approval documentation |

---

## Module Reference

### Core Modules

| Module | Path | Purpose |
|--------|------|---------|
| Project State | `core/project-state.md` | Context persistence |
| Pipeline Templates | `core/pipeline-templates.md` | Research workflows |
| Integration Hub | `core/integration-hub.md` | Tool connections |
| Guided Wizard | `core/guided-wizard.md` | Conversation UX |
| Auto-Documentation | `core/auto-documentation.md` | Document generation |

### Configuration Files

| File | Path | Purpose |
|------|------|---------|
| Project State | `.research/project-state.yaml` | Current project context |
| Decision Log | `.research/decision-log.yaml` | Research decisions |
| PRISMA Checklist | `.research/prisma-checklist.yaml` | Checklist tracking |
| Routing Config | `.omc/config/research-coordinator-routing.yaml` | Model routing |
| Checkpoints | `.omc/checkpoints/checkpoint-definitions.yaml` | Human checkpoints |

---

## Version History

- **v4.0.0**: Context persistence, pipeline templates, integration hub, guided wizard, auto-documentation, English base
- **v3.2.0**: OMC integration, model routing, parallel execution
- **v3.1.0**: Conceptual Framework Visualizer (#21)
- **v3.0.0**: Creativity modules, user checkpoints, dynamic T-Score

---

## Getting Started

1. **Start a conversation** with your research topic
2. **Follow the guided wizard** through choice points
3. **Let Research Coordinator maintain context** throughout your project
4. **Use tool integrations** when needed (Excel, R, etc.)
5. **Export documentation** when ready

```
"I want to start a systematic review on AI in higher education"
```

Research Coordinator will guide you from there.
