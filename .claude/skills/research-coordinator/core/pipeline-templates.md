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

---

## Template 4: Multi-Gate Meta-Analysis Extraction Pipeline (V7)

### Overview

4-gate validation pipeline to prevent extraction errors in meta-analysis. Based on lessons learned from V7 project.

**Core Principle**: Every effect size must pass through all 4 gates before inclusion.

### Pipeline Structure

```yaml
meta_analysis_multigate:
  name: "Multi-Gate Extraction Validation (V7)"
  description: "4-gate validation to prevent extraction errors"

  gates:
    - gate: 1
      name: "Extraction Validation"
      checks:
        - G1.1: "Data completeness (n, M, SD)"
        - G1.2: "Design classification"
        - G1.3: "Timepoint identification"
        - G1.4: "Source verification"
      checkpoint: "CP_SOURCE_VERIFY (REQUIRED)"

    - gate: 2
      name: "Classification Validation"
      checks:
        - G2.1: "Outcome type classification"
        - G2.2: "Comparison type validation"
        - G2.3: "Effect size hierarchy (CRITICAL)"
        - G2.4: "Dependency detection"
      checkpoint: "CP_ES_HIERARCHY (REQUIRED when >1 ES)"

    - gate: 3
      name: "Statistical Validation"
      checks:
        - G3.1: "Cohen's d calculation"
        - G3.2: "Hedges' g conversion"
        - G3.3: "Variance/SE calculation"
        - G3.4: "CI sanity check"
        - G3.5: "Outlier detection (|g| > 3.0)"
      checkpoint: "CP_EXTREME_VALUE (CONDITIONAL)"

    - gate: 4
      name: "Independence Validation"
      checks:
        - G4.1: "Within-study dependency"
        - G4.2: "Pre-test exclusion (AUTO-REJECT)"
        - G4.3: "Multiple outcome handling"
        - G4.4: "Independence certification"
      checkpoint: "CP_DEPENDENCY_HANDLING (REQUIRED when >1 ES)"

  forbidden_patterns:
    - pattern: "Pre-test as independent outcome"
      action: "NEVER include"
    - pattern: "Uncorrected Cohen's d"
      action: "NEVER include (must use Hedges' g)"
    - pattern: "Multiple ES same participants without clustering"
      action: "NEVER include"
```

### Gate 1: Extraction Validation

```
┌─────────────────────────────────────────────────────────────────┐
│  GATE 1: Extraction Validation                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  G1.1 Data Completeness                                         │
│  ├─ Sample size (n) per group                                  │
│  ├─ Means (M) or effect statistics                             │
│  ├─ Standard deviations (SD) or variance                       │
│  └─ Degrees of freedom (df) if applicable                      │
│                                                                 │
│  G1.2 Design Classification                                     │
│  ├─ Between-groups (independent)                               │
│  ├─ Within-subjects (repeated measures)                        │
│  ├─ Mixed design                                               │
│  └─ Clustered/multilevel                                       │
│                                                                 │
│  G1.3 Timepoint Identification                                  │
│  ├─ Pre-test (baseline) - FLAG                                 │
│  ├─ Post-test (outcome)                                        │
│  ├─ Follow-up                                                  │
│  └─ Multiple timepoints                                        │
│                                                                 │
│  G1.4 Source Verification                                       │
│  ├─ Page number documented                                     │
│  ├─ Table/figure reference                                     │
│  └─ Direct quote if ambiguous                                  │
│                                                                 │
│  🔴 CHECKPOINT: CP_SOURCE_VERIFY                               │
│  "Verify extracted values match original source"               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Gate 2: Classification Validation

```
┌─────────────────────────────────────────────────────────────────┐
│  GATE 2: Classification Validation                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  G2.3 Effect Size Hierarchy (CRITICAL)                          │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ Priority 1: Post-test between-groups                   │    │
│  │   d = (M_post_T - M_post_C) / SD_pooled               │    │
│  │   Use when: Control group exists                       │    │
│  ├────────────────────────────────────────────────────────┤    │
│  │ Priority 2: ANCOVA-adjusted means                      │    │
│  │   Use adjusted means with pre-test covariate          │    │
│  ├────────────────────────────────────────────────────────┤    │
│  │ Priority 3: Change score                               │    │
│  │   d = (ΔM_T - ΔM_C) / SD_pooled_change                │    │
│  │   Use when: No between-group post available           │    │
│  ├────────────────────────────────────────────────────────┤    │
│  │ Priority 4: Single-group pre-post                      │    │
│  │   d = (M_post - M_pre) / SD_pre                       │    │
│  │   Use when: No control group (LAST RESORT)            │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
│  🔴 CHECKPOINT: CP_ES_HIERARCHY                                │
│  Trigger: Study has >1 potential effect size                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Gate 3: Statistical Validation

```
┌─────────────────────────────────────────────────────────────────┐
│  GATE 3: Statistical Validation                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  G3.2 Hedges' g Verification                                    │
│                                                                 │
│  def verify_hedges_g(d, n1, n2):                               │
│      df = n1 + n2 - 2                                          │
│      J = 1 - (3 / (4 * df - 1))                                │
│      g = d * J                                                  │
│      SE_g = sqrt((n1+n2)/(n1*n2) + g**2/(2*(n1+n2)))          │
│      return {'g': g, 'SE': SE_g, 'J': J}                       │
│                                                                 │
│  Tolerance: |calculated_g - reported_g| < 0.01                 │
│                                                                 │
│  G3.5 Outlier Detection                                         │
│  ├─ |g| > 2.0: Review recommended                              │
│  ├─ |g| > 3.0: Checkpoint required                             │
│  └─ |g| > 5.0: Auto-flag for exclusion consideration          │
│                                                                 │
│  🟠 CHECKPOINT: CP_EXTREME_VALUE (CONDITIONAL)                 │
│  Trigger: |g| > 2.0                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Gate 4: Independence Validation

```
┌─────────────────────────────────────────────────────────────────┐
│  GATE 4: Independence Validation                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  G4.2 Pre-test Exclusion (AUTO-REJECT)                          │
│                                                                 │
│  EXCLUDE_PATTERNS = [                                           │
│      r'pre[- ]?test', r'pretest', r'baseline',                 │
│      r'pre[- ]?intervention', r'pre[- ]?training',             │
│      r'time\s*1', r'T1(?!\d)', r'before\s+treatment'           │
│  ]                                                              │
│                                                                 │
│  ⛔ Pre-test scores = baseline equivalence check               │
│     NOT treatment effect → NEVER include as outcome            │
│                                                                 │
│  G4.3 Multiple Outcome Handling                                 │
│  ├─ Same construct: Average or select primary                  │
│  ├─ Different constructs: Include with clustering             │
│  └─ Same participants: 3-level model required                  │
│                                                                 │
│  🔴 CHECKPOINT: CP_DEPENDENCY_HANDLING                         │
│  Trigger: >1 ES from same study                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Workflow Stages

```
┌─────────────────────────────────────────────────────────────────┐
│     Multi-Gate Meta-Analysis Extraction Pipeline                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Stage 1: Raw Extraction                                        │
│  ├─ Extract all potential statistics from paper                │
│  ├─ Document source (page, table, figure)                      │
│  ├─ Flag pre-test values                                       │
│  └─ 📋 Pass to Gate 1                                          │
│                                                                 │
│  Gate 1: Extraction Validation                                  │
│  ├─ Verify completeness                                        │
│  ├─ Classify design                                            │
│  ├─ Identify timepoints                                        │
│  └─ 🔴 CP_SOURCE_VERIFY                                        │
│                                                                 │
│  Gate 2: Classification Validation                              │
│  ├─ Apply ES hierarchy                                         │
│  ├─ Select optimal ES                                          │
│  ├─ Document exclusions                                        │
│  └─ 🔴 CP_ES_HIERARCHY (if >1 ES)                              │
│                                                                 │
│  Gate 3: Statistical Validation                                 │
│  ├─ Calculate d                                                │
│  ├─ Convert to g (verify)                                      │
│  ├─ Calculate SE                                               │
│  └─ 🟠 CP_EXTREME_VALUE (if |g|>2)                             │
│                                                                 │
│  Gate 4: Independence Validation                                │
│  ├─ Check within-study dependency                              │
│  ├─ ⛔ AUTO-REJECT pre-test as outcome                         │
│  ├─ Plan clustering if needed                                  │
│  └─ 🔴 CP_DEPENDENCY_HANDLING (if >1 ES)                       │
│                                                                 │
│  Stage 2: Final Dataset                                         │
│  ├─ Only gate-passed ES included                               │
│  ├─ All exclusions documented                                  │
│  └─ Ready for meta-analysis                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Agents Activated

| Gate | Primary Agents | Support Agents |
|------|----------------|----------------|
| 1 | B3-EffectSizeExtractor | B1-SystematicLiteratureScout |
| 2 | B3-EffectSizeExtractor | B2-EvidenceQualityAppraiser |
| 3 | B3-EffectSizeExtractor | E1-QuantitativeAnalysisGuide |
| 4 | B2-EvidenceQualityAppraiser | E5-SensitivityAnalysisDesigner |

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
