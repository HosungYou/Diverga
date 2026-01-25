---
name: project-state
version: "4.0.0"
description: |
  Research Project State System - Maintains context throughout the entire research lifecycle.
  Core v4.0 feature enabling context persistence across agents and stages.
---

# Research Project State System

## Overview

The Research Project State system maintains context throughout the entire research lifecycle, eliminating the need to re-explain information across different stages and agents.

## State File Location

```
your-project/
└── .research/
    ├── project-state.yaml      # Core project state
    ├── decision-log.yaml       # All decisions with timestamps
    ├── checklist-progress.yaml # PRISMA/GRADE/etc. tracking
    └── integration-status.yaml # Connected tools status
```

## Project State Schema

```yaml
# .research/project-state.yaml

# ═══════════════════════════════════════════════════════════
# RESEARCH PROJECT STATE
# Auto-maintained by Research Coordinator
# Last updated: {timestamp}
# ═══════════════════════════════════════════════════════════

project:
  name: ""
  type: ""  # systematic_review | meta_analysis | experimental | survey | qualitative | mixed_methods
  created: ""
  last_modified: ""
  current_stage: ""  # 1-8 for systematic review
  language: "en"  # en | ko | bilingual

# ───────────────────────────────────────────────────────────
# CORE RESEARCH CONTEXT
# This section is injected into every agent conversation
# ───────────────────────────────────────────────────────────

research_context:
  research_question:
    main: ""
    sub_questions: []
    pico_elements:  # For systematic reviews
      population: ""
      intervention: ""
      comparison: ""
      outcome: ""
    last_refined: ""

  theoretical_framework:
    primary_theory: ""
    supporting_theories: []
    hypotheses:
      - id: "H1"
        statement: ""
        variables:
          independent: ""
          dependent: ""
          mediators: []
          moderators: []
    vs_diverge:
      t_score: null
      creativity_device: ""
      rationale: ""

  methodology:
    design: ""  # RCT | quasi-experimental | correlational | etc.
    approach: ""  # quantitative | qualitative | mixed
    sampling:
      strategy: ""
      target_size: null
      power_analysis: ""

# ───────────────────────────────────────────────────────────
# SYSTEMATIC REVIEW SPECIFIC
# ───────────────────────────────────────────────────────────

systematic_review:
  protocol:
    registration: ""  # PROSPERO ID
    pre_registered: false
    deviations: []

  eligibility:
    inclusion_criteria: []
    exclusion_criteria: []
    date_range:
      start: null
      end: null
    languages: []
    study_types: []

  search:
    databases: []
    search_string: ""
    date_executed: ""
    results_by_database: {}

  screening:
    identified: 0
    duplicates_removed: 0
    screened: 0
    excluded_screening: 0
    full_text_assessed: 0
    excluded_full_text: 0
    included_final: 0

  extraction:
    studies_extracted: 0
    effect_size_type: ""  # hedges_g | cohens_d | OR | RR | r
    moderators_coded: []

  analysis:
    model: ""  # random_effects | fixed_effects | three_level
    heterogeneity:
      i_squared: null
      tau_squared: null
    publication_bias:
      method: ""
      result: ""

# ───────────────────────────────────────────────────────────
# CONNECTED INTEGRATIONS
# ───────────────────────────────────────────────────────────

integrations:
  literature_search:
    semantic_scholar:
      connected: false
      api_key_set: false
    openalex:
      connected: false
      email_set: false
    arxiv:
      connected: true  # No key needed

  reference_management:
    zotero:
      connected: false
      mcp_configured: false
    bibtex:
      connected: true  # Built-in

  office_tools:
    excel:
      available: true
      skill: "ms-office-suite:excel"
    powerpoint:
      available: true
      skill: "ms-office-suite:powerpoint"
    word:
      available: true
      skill: "ms-office-suite:word"

  statistical:
    r_integration:
      available: false
      path: ""
    python:
      available: true  # Built-in

  visualization:
    nanobanana:
      connected: false
      api_key_set: false
    mermaid:
      connected: true  # Built-in

# ───────────────────────────────────────────────────────────
# PUBLICATION TARGET
# ───────────────────────────────────────────────────────────

publication:
  target_journal:
    name: ""
    impact_factor: null
    formatting_style: ""  # APA | MLA | Chicago | Vancouver

  manuscript:
    current_version: ""
    word_count: 0
    sections_complete: []

  open_science:
    osf_project: ""
    data_availability: ""
    preprint: ""
```

## Decision Log Schema

```yaml
# .research/decision-log.yaml

decisions:
  - id: "D001"
    timestamp: "2024-01-15T10:30:00Z"
    stage: "research_design"
    agent: "research-question-refiner"
    type: "refinement"  # refinement | selection | exclusion | deviation
    description: "Narrowed research question to focus on higher education"
    before: "How does AI affect learning?"
    after: "How does GenAI affect learning outcomes in higher education?"
    rationale: "Scope was too broad for systematic review"
    reversible: true

  - id: "D002"
    timestamp: "2024-01-20T14:15:00Z"
    stage: "theoretical_framework"
    agent: "theoretical-framework-architect"
    type: "selection"
    description: "Selected AIMC Model as primary framework"
    options_considered:
      - name: "TAM"
        t_score: 0.75
        rejected_reason: "Too common, limited theoretical contribution"
      - name: "AIMC Model"
        t_score: 0.35
        selected: true
        rationale: "Novel integration addressing mechanism gap"
    vs_diverge_applied: true
```

## Context Injection Protocol

When any agent is activated, the following context is automatically injected:

```markdown
## Current Research Context

**Project**: {project.name}
**Type**: {project.type}
**Stage**: {project.current_stage}

**Research Question**: {research_context.research_question.main}

**Theoretical Framework**: {research_context.theoretical_framework.primary_theory}

**Key Decisions Made**:
{recent_decisions_summary}

**Connected Tools**: {active_integrations_list}

---
Continue from this context. Do not ask for information already established above.
```

## Auto-Update Triggers

The project state is automatically updated when:

| Event | Updated Fields |
|-------|----------------|
| Research question refined | `research_context.research_question.*` |
| Theory selected | `research_context.theoretical_framework.*` |
| Hypothesis added | `research_context.theoretical_framework.hypotheses[]` |
| Search executed | `systematic_review.search.*` |
| Paper screened | `systematic_review.screening.*` |
| Effect size extracted | `systematic_review.extraction.*` |
| Analysis completed | `systematic_review.analysis.*` |
| Tool connected | `integrations.*` |
| Decision made | `decision-log.yaml` appended |

## Commands

```bash
# Initialize new research project
"Start a new systematic review project"
→ Creates .research/ directory with initialized state

# View current state
"Show my research project status"
→ Displays current stage, progress, and recent decisions

# Export state
"Export my research context"
→ Generates summary for manuscript methods section
```

## Integration with Agents

Each agent receives the relevant subset of project state:

| Agent | Receives |
|-------|----------|
| Research Question Refiner | `research_context.research_question` |
| Theoretical Framework Architect | `research_context.theoretical_framework` |
| Literature Scout | `systematic_review.eligibility`, `systematic_review.search` |
| Statistical Analysis Guide | `systematic_review.extraction`, `systematic_review.analysis` |
| Journal Matcher | `publication.*`, `research_context.research_question` |

## Human Checkpoints

Project state changes at these points require explicit approval:

| Checkpoint | State Change |
|------------|--------------|
| CP_RESEARCH_DIRECTION | `research_context.research_question` |
| CP_THEORY_SELECTION | `research_context.theoretical_framework` |
| CP_METHODOLOGY_APPROVAL | `research_context.methodology` |
| CP_ANALYSIS_PLAN | `systematic_review.analysis.model` |
