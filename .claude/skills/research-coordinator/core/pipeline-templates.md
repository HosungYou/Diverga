---
name: pipeline-templates
version: "4.0.0"
description: |
  Research Pipeline Templates - Pre-configured workflows for systematic reviews, meta-analyses,
  experimental studies, and surveys. Implements PRISMA 2020 compliance.
---

# Research Pipeline Templates

## Overview

Pre-configured workflows for common research types. Each template sets up:
- Relevant agents
- Stage progression
- Checklists (PRISMA, GRADE, etc.)
- Recommended integrations
- Output documents

---

## Template 1: Systematic Review & Meta-Analysis (PRISMA 2020)

### Workflow Stages

```
┌─────────────────────────────────────────────────────────────┐
│     PRISMA 2020 Systematic Review Pipeline                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Stage 1: Protocol Development                              │
│  ├─ Define research question (PICO/SPIDER)                 │
│  ├─ Select theoretical framework                            │
│  ├─ Draft eligibility criteria                              │
│  ├─ Plan search strategy                                    │
│  └─ 📋 Register protocol (PROSPERO)                         │
│                                                             │
│  Stage 2: Literature Search                                 │
│  ├─ Execute database searches                               │
│  ├─ Document search strings                                 │
│  ├─ Export results to reference manager                     │
│  └─ 📊 Generate identification numbers                      │
│                                                             │
│  Stage 3: Screening                                         │
│  ├─ Remove duplicates                                       │
│  ├─ Title/abstract screening                                │
│  ├─ Full-text assessment                                    │
│  ├─ Document exclusion reasons                              │
│  └─ 📊 Update PRISMA flow diagram                           │
│                                                             │
│  Stage 4: Data Extraction                                   │
│  ├─ Design extraction form                                  │
│  ├─ Extract study characteristics                           │
│  ├─ Extract effect sizes                                    │
│  ├─ Code moderators                                         │
│  └─ 📄 Export to Excel for verification                     │
│                                                             │
│  Stage 5: Quality Assessment                                │
│  ├─ Apply risk of bias tool (RoB 2, ROBINS-I)              │
│  ├─ Assess certainty (GRADE)                                │
│  └─ 📊 Generate quality summary table                       │
│                                                             │
│  Stage 6: Statistical Analysis                              │
│  ├─ Select meta-analytic model                              │
│  ├─ Calculate pooled effects                                │
│  ├─ Assess heterogeneity                                    │
│  ├─ Conduct moderator analyses                              │
│  ├─ Test publication bias                                   │
│  ├─ Run sensitivity analyses                                │
│  └─ 📊 Generate forest/funnel plots                         │
│                                                             │
│  Stage 7: Manuscript Preparation                            │
│  ├─ Draft sections (IMRAD)                                  │
│  ├─ Create figures and tables                               │
│  ├─ Write abstract                                          │
│  └─ 📝 Export to Word                                       │
│                                                             │
│  Stage 8: Publication & Dissemination                       │
│  ├─ Select target journal                                   │
│  ├─ Format for submission                                   │
│  ├─ Prepare supplementary materials                         │
│  ├─ Create OSF project                                      │
│  └─ 📤 Generate submission package                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Agents Activated

| Stage | Primary Agents | Support Agents |
|-------|----------------|----------------|
| 1 | #01, #02, #03, #04 | #21 (framework viz) |
| 2 | #05, #08 | - |
| 3 | #05, #16 | - |
| 4 | #07 | - |
| 5 | #06, #16 | #14 |
| 6 | #10, #11, #12 | #07 |
| 7 | #18, #21 | #03 |
| 8 | #17, #19, #20 | - |

### PRISMA 2020 Checklist (27 Items)

```yaml
prisma_checklist:
  title:
    - item: 1
      section: "Title"
      description: "Identify the report as a systematic review"
      completed: false

  abstract:
    - item: 2
      section: "Abstract"
      description: "Structured summary including background, objectives, methods, results, conclusions"
      completed: false

  introduction:
    - item: 3
      section: "Rationale"
      description: "Describe the rationale for the review"
      completed: false
    - item: 4
      section: "Objectives"
      description: "Provide explicit statement of objectives/questions"
      completed: false

  methods:
    - item: 5
      section: "Eligibility criteria"
      description: "Specify inclusion/exclusion criteria"
      completed: false
    - item: 6
      section: "Information sources"
      description: "Specify all databases and date last searched"
      completed: false
    - item: 7
      section: "Search strategy"
      description: "Present full search strategy for at least one database"
      completed: false
    - item: 8
      section: "Selection process"
      description: "Specify methods for selection"
      completed: false
    - item: 9
      section: "Data collection"
      description: "Specify methods for data extraction"
      completed: false
    - item: 10
      section: "Data items"
      description: "List all variables for which data were sought"
      completed: false
    - item: 11
      section: "Study risk of bias"
      description: "Specify methods for assessing risk of bias"
      completed: false
    - item: 12
      section: "Effect measures"
      description: "Specify effect measures used"
      completed: false
    - item: 13
      section: "Synthesis methods"
      description: "Describe methods for synthesis"
      completed: false
    - item: 14
      section: "Reporting bias"
      description: "Describe methods for assessing publication bias"
      completed: false
    - item: 15
      section: "Certainty assessment"
      description: "Describe methods for certainty assessment"
      completed: false

  results:
    - item: 16
      section: "Study selection"
      description: "Report numbers at each stage with flow diagram"
      completed: false
    - item: 17
      section: "Study characteristics"
      description: "Cite each study and present characteristics"
      completed: false
    - item: 18
      section: "Risk of bias in studies"
      description: "Present risk of bias assessments"
      completed: false
    - item: 19
      section: "Results of individual studies"
      description: "Present all individual study data"
      completed: false
    - item: 20
      section: "Results of syntheses"
      description: "Present synthesis results including heterogeneity"
      completed: false
    - item: 21
      section: "Reporting biases"
      description: "Present publication bias assessment"
      completed: false
    - item: 22
      section: "Certainty of evidence"
      description: "Present certainty assessments"
      completed: false

  discussion:
    - item: 23
      section: "Discussion"
      description: "Provide interpretation, limitations, and conclusions"
      completed: false

  other:
    - item: 24
      section: "Registration"
      description: "Provide registration number"
      completed: false
    - item: 25
      section: "Protocol"
      description: "Indicate where protocol can be accessed"
      completed: false
    - item: 26
      section: "Support"
      description: "Describe funding sources"
      completed: false
    - item: 27
      section: "Competing interests"
      description: "Declare competing interests"
      completed: false
```

### Recommended Integrations

| Tool | Purpose | Setup |
|------|---------|-------|
| Semantic Scholar | Literature search | API key |
| OpenAlex | Literature search | Email (polite pool) |
| Zotero | Reference management | MCP server |
| Excel | Data extraction verification | Skill: ms-office-suite |
| R | Meta-analysis | Local installation |
| Nanobanana | PRISMA diagram | API key |
| Word | Manuscript drafting | Skill: ms-office-suite |
| OSF | Open science | Account |

### Output Documents

| Document | Format | Generated By |
|----------|--------|--------------|
| PRISMA Flow Diagram | PNG/SVG | #21 + Nanobanana |
| Forest Plot | PNG/R | #11 (R script) |
| Funnel Plot | PNG/R | #11 (R script) |
| Summary Table | Excel | Skill: ms-office-suite |
| Manuscript | Word | Skill: ms-office-suite |
| Supplementary Materials | Multiple | Auto-generated |

---

## Template 2: Experimental Study (Pre-registered)

### Workflow Stages

```
┌─────────────────────────────────────────────────────────────┐
│     Pre-registered Experimental Study Pipeline              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Stage 1: Study Design                                      │
│  ├─ Define research questions/hypotheses                    │
│  ├─ Select theoretical framework                            │
│  ├─ Design experimental conditions                          │
│  ├─ Conduct power analysis                                  │
│  └─ 📋 Pre-register on OSF/AsPredicted                      │
│                                                             │
│  Stage 2: Ethics & IRB                                      │
│  ├─ Prepare IRB application                                 │
│  ├─ Draft consent forms                                     │
│  ├─ Plan data management                                    │
│  └─ 📄 Submit IRB                                           │
│                                                             │
│  Stage 3: Materials Development                             │
│  ├─ Develop instruments/measures                            │
│  ├─ Design intervention materials                           │
│  ├─ Plan manipulation checks                                │
│  └─ 📊 Pilot testing                                        │
│                                                             │
│  Stage 4: Data Collection                                   │
│  ├─ Recruit participants                                    │
│  ├─ Conduct experiment                                      │
│  ├─ Monitor data quality                                    │
│  └─ 📊 Track attrition                                      │
│                                                             │
│  Stage 5: Data Analysis                                     │
│  ├─ Clean and prepare data                                  │
│  ├─ Check assumptions                                       │
│  ├─ Run pre-registered analyses                             │
│  ├─ Conduct exploratory analyses (labeled)                  │
│  └─ 📊 Generate results tables                              │
│                                                             │
│  Stage 6: Manuscript & Dissemination                        │
│  ├─ Write manuscript sections                               │
│  ├─ Create figures                                          │
│  ├─ Prepare supplementary materials                         │
│  └─ 📤 Submit to journal                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Agents Activated

| Stage | Primary Agents |
|-------|----------------|
| 1 | #01, #02, #09, #10 |
| 2 | #04 |
| 3 | #09 |
| 4 | - (data collection) |
| 5 | #10, #11, #12, #16 |
| 6 | #17, #18, #21 |

---

## Template 3: Survey Research

### Workflow Stages

```
┌─────────────────────────────────────────────────────────────┐
│     Survey Research Pipeline                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Stage 1: Conceptualization                                 │
│  ├─ Define research questions                               │
│  ├─ Identify constructs to measure                          │
│  ├─ Review existing instruments                             │
│  └─ 📋 Select/adapt instruments                             │
│                                                             │
│  Stage 2: Instrument Development                            │
│  ├─ Draft survey items                                      │
│  ├─ Expert review                                           │
│  ├─ Cognitive interviews                                    │
│  └─ 📊 Pilot test                                           │
│                                                             │
│  Stage 3: Sampling & Ethics                                 │
│  ├─ Define target population                                │
│  ├─ Select sampling strategy                                │
│  ├─ Calculate sample size                                   │
│  ├─ Prepare IRB                                             │
│  └─ 📄 Plan data collection logistics                       │
│                                                             │
│  Stage 4: Data Collection                                   │
│  ├─ Distribute survey                                       │
│  ├─ Send reminders                                          │
│  ├─ Monitor response rate                                   │
│  └─ 📊 Track completion                                     │
│                                                             │
│  Stage 5: Data Analysis                                     │
│  ├─ Clean data                                              │
│  ├─ Assess reliability (Cronbach's α)                       │
│  ├─ Check validity (CFA)                                    │
│  ├─ Conduct main analyses                                   │
│  └─ 📊 Generate results                                     │
│                                                             │
│  Stage 6: Reporting                                         │
│  ├─ Write manuscript                                        │
│  ├─ Create figures/tables                                   │
│  └─ 📤 Submit                                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Template Initialization

When user selects a template:

```yaml
# Auto-generated .research/project-state.yaml

project:
  name: "User's Project Name"
  type: "systematic_review"  # From template selection
  template: "prisma_2020"
  created: "2024-01-15T10:00:00Z"
  current_stage: 1

stages:
  - number: 1
    name: "Protocol Development"
    status: "in_progress"
    checklist_items: 5
    completed_items: 0
  - number: 2
    name: "Literature Search"
    status: "pending"
    # ...

recommended_integrations:
  - tool: "semantic_scholar"
    priority: "high"
    setup_guide: "docs/setup/semantic-scholar.md"
  - tool: "excel"
    priority: "high"
    skill: "ms-office-suite:excel"
    when_needed: "Stage 4: Data extraction verification"
  - tool: "r"
    priority: "high"
    when_needed: "Stage 6: Meta-analysis"
  # ...
```

---

## Stage Transitions

```
Stage completion requires:

1. All required checklist items completed
2. Human checkpoint approved (if applicable)
3. Outputs generated (if applicable)

Example: Stage 1 → Stage 2
├─ ✅ Research question finalized (CP_RESEARCH_DIRECTION)
├─ ✅ Eligibility criteria documented
├─ ✅ Search strategy drafted
└─ ✅ Protocol registered (or waived)

→ Automatically advances to Stage 2
→ Activates Literature Search agents
→ Suggests database integrations
```
