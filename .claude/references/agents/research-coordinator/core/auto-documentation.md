---
name: auto-documentation
version: "4.0.0"
description: |
  Automatic Documentation System - Generates research documentation as you progress.
  Decision logs, PRISMA diagrams, data extraction sheets, and method sections.
---

# Automatic Documentation System

## Overview

Research Coordinator automatically generates documentation as you progress through your research, reducing the burden of maintaining separate records.

---

## Auto-Generated Documents

### 1. Decision Log

**Generated Automatically When**:
- Research question is refined
- Theory/framework is selected
- Methodology decisions are made
- Inclusion/exclusion criteria applied
- Analysis method chosen

**Format**:
```yaml
# .research/decision-log.yaml

decisions:
  - id: "D001"
    timestamp: "2024-01-15T10:30:00Z"
    stage: "research_design"
    type: "research_question"
    action: "Narrowed scope to higher education context"
    rationale: "Original scope too broad for systematic review timeline"
    evidence: "Discussion with advisor; feasibility assessment"
    reversible: true

  - id: "D002"
    timestamp: "2024-01-18T14:20:00Z"
    stage: "theoretical_framework"
    type: "theory_selection"
    action: "Selected AIMC Model as primary framework"
    options_considered:
      - "TAM (Technology Acceptance Model)" - rejected: overused
      - "SCT (Social Cognitive Theory)" - rejected: insufficient mechanism
      - "AIMC Model" - selected: novel, addresses gap
    vs_diverge_score: 0.35
    rationale: "Provides mechanistic explanation lacking in current literature"
```

**Export Commands**:
```
"Export my decision log"
→ Generates formatted document for methods section

"Summarize decisions for ethics review"
→ Generates IRB-appropriate summary
```

---

### 2. PRISMA Checklist (Auto-Tracked)

**Tracked Automatically**:
- Item completion status
- Supporting evidence location
- Completion timestamp

**Format**:
```yaml
# .research/prisma-checklist.yaml

checklist:
  title:
    item_1:
      description: "Identify the report as a systematic review"
      completed: true
      completed_at: "2024-02-01T09:00:00Z"
      evidence: "manuscript.docx, line 1"

  abstract:
    item_2:
      description: "Structured summary"
      completed: false
      notes: "Will complete after results"

  methods:
    item_5:
      description: "Eligibility criteria"
      completed: true
      completed_at: "2024-01-20T11:30:00Z"
      evidence: ".research/project-state.yaml#eligibility"
```

**Auto-Update Triggers**:
| Action | Items Updated |
|--------|---------------|
| Search executed | Item 6, 7 |
| Screening complete | Item 8, 16 |
| Data extracted | Item 9, 10 |
| Quality assessed | Item 11, 18 |
| Analysis run | Item 12, 13, 20 |

---

### 3. Methods Section Draft

**Generated On Demand**:
```
"Generate my methods section draft"
```

**Output**:
```markdown
## Methods

### Protocol and Registration

This systematic review was conducted following PRISMA 2020 guidelines
(Page et al., 2021). The protocol was registered with PROSPERO
(ID: {prospero_id}).

### Eligibility Criteria

Studies were included if they met the following criteria:
{auto-populated from project-state.yaml}

**Inclusion criteria:**
- {inclusion_1}
- {inclusion_2}

**Exclusion criteria:**
- {exclusion_1}
- {exclusion_2}

### Information Sources and Search Strategy

We searched the following databases: {databases_list}

The search was conducted on {search_date}. The full search strategy
for {primary_database} is provided in Appendix A.

### Selection Process

{screening_description based on actual numbers}

### Data Extraction

Data were extracted using a standardized form (Appendix B).
The following variables were coded: {moderators_list}

### Effect Size Calculation

Effect sizes were calculated as {effect_size_type}.
When not directly reported, {conversion_methods_used}.

### Statistical Analysis

A {model_type} was used to synthesize effect sizes.
Heterogeneity was assessed using {heterogeneity_methods}.
Publication bias was evaluated using {bias_methods}.

---
*This draft was auto-generated from Research Coordinator project state.
Review and customize before submission.*
```

---

### 4. Research Audit Trail

**Comprehensive Activity Log**:
```yaml
# .research/audit-trail.yaml

sessions:
  - session_id: "S001"
    date: "2024-01-15"
    duration_minutes: 45
    activities:
      - time: "10:00:00"
        action: "Project initialized"
        agent: "system"
      - time: "10:05:00"
        action: "Research question discussed"
        agent: "research-question-refiner"
        user_input_summary: "Interest in AI tutoring effects"
      - time: "10:30:00"
        action: "RQ checkpoint reached"
        agent: "research-question-refiner"
        decision: "D001"
        user_choice: "Direction A (Narrow scope)"

  - session_id: "S002"
    date: "2024-01-18"
    duration_minutes: 60
    activities:
      - time: "14:00:00"
        action: "Theory exploration started"
        agent: "theoretical-framework-architect"
      # ...
```

**Export Options**:
```
"Export my research audit trail"
→ PDF with all activities, decisions, timestamps

"Generate reproducibility report"
→ Structured report for open science requirements

"Create timeline visualization"
→ Visual representation of research progress
```

---

### 5. Supplementary Materials Package

**Auto-Generated Package Structure**:
```
supplementary/
├── Appendix_A_Search_Strategy.docx
│   └─ Full search strings for all databases
│
├── Appendix_B_Extraction_Form.xlsx
│   └─ Template used for data extraction
│
├── Appendix_C_Excluded_Studies.docx
│   └─ List with exclusion reasons
│
├── Appendix_D_Quality_Assessment.xlsx
│   └─ RoB ratings for all studies
│
├── Appendix_E_Sensitivity_Analyses.docx
│   └─ Results of all sensitivity tests
│
├── Appendix_F_PRISMA_Checklist.docx
│   └─ Completed PRISMA checklist
│
└── Appendix_G_Analysis_Code.R
    └─ Full analysis script
```

**Command**:
```
"Generate supplementary materials package"
```

---

### 6. OSF Submission Package

**Auto-Generated for Open Science Framework**:
```
osf_package/
├── README.md
│   └─ Project overview, file descriptions
│
├── preregistration/
│   ├── protocol.md
│   └── analysis_plan.md
│
├── data/
│   ├── README.md (data dictionary)
│   ├── raw/ (if sharing)
│   └── processed/
│       └─ effects_anonymized.csv
│
├── analysis/
│   ├── meta_analysis.R
│   └── requirements.txt
│
├── materials/
│   ├── search_strategy.md
│   ├── extraction_form.xlsx
│   └── quality_assessment_tool.md
│
└── output/
    ├── figures/
    │   ├── forest_plot.png
    │   └─ funnel_plot.png
    └── tables/
        └─ summary_statistics.csv
```

**Command**:
```
"Prepare OSF submission package"
```

---

## Integration with Tools

### Excel Export

When data extraction is complete:
```
"Export extraction data to Excel"

→ Generates: data_extraction_verified.xlsx
  ├─ Study Characteristics (formatted table)
  ├─ Effect Sizes (with formulas)
  ├─ Moderators (with coding guide)
  └─ Summary Statistics (pivot tables)
```

### Word Export

For manuscript drafts:
```
"Export methods section to Word"

→ Generates: methods_draft.docx
  ├─ APA 7th edition formatting
  ├─ Table placeholders
  ├─ Citation placeholders (for Zotero)
  └─ Track changes enabled
```

### PowerPoint Generation

For presentations:
```
"Create presentation of my results"

→ Generates: results_presentation.pptx
  ├─ Title slide
  ├─ Background (2-3 slides)
  ├─ Methods overview
  ├─ PRISMA diagram
  ├─ Main results (forest plot)
  ├─ Moderator analyses
  ├─ Discussion points
  └─ Conclusion
```

---

## Triggered Documentation

### On Project Milestones

| Milestone | Auto-Generated |
|-----------|----------------|
| Search complete | Search documentation, database yields |
| Screening complete | PRISMA flow numbers, exclusion summary |
| Extraction complete | Data summary, moderator overview |
| Analysis complete | Results summary, sensitivity report |
| Manuscript ready | Complete supplementary package |

### On Human Checkpoints

| Checkpoint | Auto-Generated |
|------------|----------------|
| CP_RESEARCH_DIRECTION | RQ evolution document |
| CP_THEORY_SELECTION | Framework justification note |
| CP_METHODOLOGY_APPROVAL | Methods rationale document |
| CP_ANALYSIS_PLAN | Analysis plan summary |

---

## Version Control

All auto-generated documents include version tracking:

```yaml
# Document header
metadata:
  version: "1.2"
  generated: "2024-02-15T14:30:00Z"
  generator: "Research Coordinator v4.0"
  project: "GenAI-HE-MetaAnalysis"
  stage: "analysis_complete"
  previous_version: "1.1"
  changes:
    - "Added sensitivity analysis results"
    - "Updated forest plot with moderators"
```

---

## Export Formats

| Document Type | Available Formats |
|---------------|-------------------|
| Methods draft | Word (.docx), Markdown (.md) |
| Data extraction | Excel (.xlsx), CSV |
| Analysis code | R (.R), Python (.py) |
| Figures | PNG, SVG, PDF |
| Checklists | Word, Excel, PDF |
| Audit trail | PDF, JSON, YAML |
| Full package | ZIP archive |

---

## Commands Reference

```
# Decision tracking
"Show my decision log"
"Export decisions for methods section"

# PRISMA
"Show PRISMA checklist progress"
"What PRISMA items are incomplete?"
"Generate PRISMA flow diagram"

# Methods
"Draft my methods section"
"Update methods with current data"

# Supplementary
"Generate supplementary materials"
"Create Appendix A (search strategy)"

# Open Science
"Prepare OSF package"
"Generate data availability statement"

# Presentations
"Create conference presentation"
"Generate defense slides"

# Full export
"Export complete project documentation"
```
