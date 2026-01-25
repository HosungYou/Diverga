---
name: checklist-manager
version: 4.0.0
description: |
  VS-Enhanced Checklist Manager - Prevents Mode Collapse with context-adaptive checking
  Light VS applied: Avoids mechanical checking + research-specific guideline application
  Use when: checking reporting guidelines, preparing submissions, ensuring compliance
  Triggers: checklist, PRISMA, CONSORT, STROBE, COREQ, reporting guidelines
upgrade_level: LIGHT
tier: Support
v3_integration:
  dynamic_t_score: false
  creativity_modules: []
  checkpoints:
    - CP-INIT-001
    - CP-VS-003
---

# Checklist Manager

**Agent ID**: 14
**Category**: D - Quality & Validation
**VS Level**: Light (Modal awareness)
**Tier**: Support
**Icon**: 📋

## Overview

Systematically checks compliance with reporting guidelines (PRISMA, CONSORT, STROBE, etc.) by research type.
Identifies missing items and provides specific supplementation guidance.

**VS-Research methodology** (Light) is applied to provide contextualized guideline interpretation
and application beyond mechanical checklist application.

## VS Modal Awareness (Light)

⚠️ **Modal Checklist Approaches**: The following are the most predictable approaches:

| Area | Modal Approach (T>0.8) | Contextualized Approach (T<0.5) |
|------|------------------------|----------------------------------|
| Guideline selection | "Study type → Standard checklist" | Multi-guideline integration (PRISMA+COSMIN) |
| Item checking | "Yes/No binary check" | Fulfillment level + supplementation priority |
| Missing items | "List missing items" | Context-specific essential/recommended distinction |
| Reporting | "Complete checklist" | Item-specific improvement specification |

**Contextualization Principle**: Flexible application reflecting the spirit of guidelines

## When to Use

- Checking guidelines before paper submission
- Writing systematic review/meta-analysis reports
- Reporting RCT or observational studies
- Confirming journal requirements

## Core Functions

1. **Guideline Matching**
   - Select appropriate checklist for study type
   - Apply latest version

2. **Item-by-Item Checking**
   - Evaluate each item fulfillment
   - Record location (page/section)

3. **Missing Item Identification**
   - List unfulfilled items
   - Assess severity

4. **Improvement Suggestions**
   - Specific supplementation guidance
   - Provide example phrases

## Checklist Library

| Study Type | Checklist | Item Count |
|------------|-----------|------------|
| Systematic review/Meta-analysis | PRISMA 2020 | 27 |
| RCT | CONSORT 2010 | 25 |
| Observational (cohort/case-control/cross-sectional) | STROBE | 22 |
| Qualitative research | COREQ / SRQR | 32 / 21 |
| Mixed methods | GRAMMS | 6 |
| Survey instrument development | COSMIN | Multiple |
| Diagnostic accuracy | STARD | 30 |
| Prognostic research | TRIPOD | 22 |
| Animal studies | ARRIVE | 20 |
| Case reports | CARE | 13 |

## PRISMA 2020 Checklist (for Systematic Reviews)

### Title
- [ ] 1. Identify as systematic review/meta-analysis in title

### Abstract
- [ ] 2. Structured abstract (background, objectives, methods, results, conclusions)

### Introduction
- [ ] 3. Rationale for the review
- [ ] 4. Objectives - including PICO

### Methods
- [ ] 5. Protocol registration information
- [ ] 6. Eligibility criteria
- [ ] 7. Information sources
- [ ] 8. Search strategy
- [ ] 9. Selection process
- [ ] 10. Data collection process
- [ ] 11. Data items
- [ ] 12. Risk of bias assessment
- [ ] 13. Effect measures
- [ ] 14. Synthesis methods
- [ ] 15. Reporting bias assessment
- [ ] 16. Certainty assessment (GRADE, etc.)

### Results
- [ ] 17. Study selection (PRISMA flow diagram)
- [ ] 18. Study characteristics
- [ ] 19. Risk of bias results
- [ ] 20. Individual study results
- [ ] 21. Synthesis results
- [ ] 22. Reporting bias results
- [ ] 23. Certainty results

### Discussion
- [ ] 24. Discussion (key findings, limitations, interpretation)

### Other
- [ ] 25. Registration and protocol
- [ ] 26. Support (Funding)
- [ ] 27. Conflicts of interest

## Input Requirements

```yaml
Required:
  - study_type: "Systematic review, RCT, cohort, etc."
  - manuscript_or_protocol: "Document to check"

Optional:
  - guideline: "Specify particular checklist"
  - check_level: "Basic/detailed"
```

## Output Format

```markdown
## Reporting Guideline Compliance Check Report

### Document Information
- Study Type: [Type]
- Applied Guideline: [PRISMA 2020 / CONSORT / STROBE, etc.]
- Check Date: [Date]

---

### Check Results Summary

| Section | Total Items | Fulfilled | Partially Fulfilled | Not Fulfilled | N/A |
|---------|------------|-----------|-------------------|---------------|-----|
| Title/Abstract | X | X | X | X | X |
| Introduction | X | X | X | X | X |
| Methods | X | X | X | X | X |
| Results | X | X | X | X | X |
| Discussion/Other | X | X | X | X | X |
| **Total** | **X** | **X** | **X** | **X** | **X** |

**Overall Compliance Rate**: [X]%

---

### Detailed Check Results

#### Section 1: Title

| # | Item | Fulfilled | Location | Notes |
|---|------|-----------|----------|-------|
| 1 | Identify as systematic review in title | ✅ | Title | - |

#### Section 2: Abstract

| # | Item | Fulfilled | Location | Notes |
|---|------|-----------|----------|-------|
| 2 | Structured abstract | ⚠️ | p.1 | Objectives unclear |

[Remaining sections continue...]

---

### Unfulfilled/Partially Fulfilled Items Detail

#### ❌ Not Fulfilled Items

**Item 5: Protocol Registration**
- Current status: No protocol registration information
- Guideline requirement: "Whether protocol was registered, registration number, access"
- **Revision plan**:
  1. Retrospective registration in PROSPERO (systematic reviews)
  2. Upload protocol to OSF
  3. Describe reason if not registered
- **Example phrase**: "The protocol for this study was prospectively registered in PROSPERO (Registration number: CRD42024XXXXXX)."

**Item 15: Publication Bias Assessment**
- Current status: Publication bias assessment method not described
- Guideline requirement: "Methods to assess publication bias or missing results"
- **Revision plan**:
  1. Add funnel plot analysis
  2. Perform Egger's test
  3. Apply trim-and-fill method
- **Example phrase**: "Publication bias was assessed visually through funnel plots and tested for asymmetry using Egger's regression test."

#### ⚠️ Partially Fulfilled Items

**Item 2: Structured Abstract**
- Current status: Abstract present but objectives unclear
- Deficiency: Comparison not specified among PICO elements
- **Revision plan**: Add comparison target to objectives sentence
- **Before**: "This study analyzed the effects of AI tutors."
- **After**: "This study meta-analyzed differences in academic achievement between groups using AI tutors and traditional instruction."

---

### Revision Recommendations by Priority

#### 🔴 Immediate Revision Needed (Essential Items)
1. **Item 17**: Add PRISMA flow diagram
2. **Item 5**: Add protocol registration information

#### 🟡 Revision Recommended (Recommended Items)
1. **Item 15**: Describe publication bias assessment method
2. **Item 16**: Add GRADE certainty assessment

#### 🟢 Optional Improvement
1. **Item 2**: Clarify abstract PICO

---

### Pre-submission Checklist

- [ ] Create and insert PRISMA flow diagram
- [ ] Add protocol registration number
- [ ] Perform and report publication bias analysis
- [ ] Create GRADE assessment table
- [ ] Prepare checklist file (for journal submission)
```

## Prompt Template

```
You are a research reporting guideline expert.

Please check the following research against the applicable guideline:

[Study Type]: {study_type}
[Applied Guideline]: {guideline}
[Manuscript/Protocol]: {document}

Tasks to perform:
1. List all items in the checklist

2. For each item:
   - Fulfillment status (Yes / No / Partial / N/A)
   - Location (page, section)
   - Deficiencies

3. Results summary table
   | Section | Item | Fulfilled | Location | Notes |

4. Specific supplementation guidance for missing/deficient items
   - What needs to be added?
   - How should it be written?
   - Provide example phrases

5. Overall compliance rate (%)
```

## Guideline Selection Flowchart

```
Study Type?
    │
    ├── Systematic review/Meta-analysis → PRISMA 2020
    │
    ├── Intervention study
    │       │
    │       ├── Randomized → CONSORT
    │       └── Non-randomized → TIDieR + applicable observational guideline
    │
    ├── Observational study
    │       │
    │       ├── Cohort → STROBE (cohort)
    │       ├── Case-control → STROBE (case-control)
    │       └── Cross-sectional → STROBE (cross-sectional)
    │
    ├── Qualitative research → COREQ or SRQR
    │
    ├── Mixed methods → GRAMMS
    │
    └── Other
            │
            ├── Diagnostic study → STARD
            ├── Prognostic model → TRIPOD
            └── Case report → CARE
```

## Related Agents

- **06-evidence-quality-appraiser**: Linked with quality assessment
- **13-internal-consistency-checker**: Consistency verification
- **15-reproducibility-auditor**: Reproducibility checking

## References

- **VS Engine v3.0**: `../../research-coordinator/core/vs-engine.md`
- **Dynamic T-Score**: `../../research-coordinator/core/t-score-dynamic.md`
- **Creativity Mechanisms**: `../../research-coordinator/references/creativity-mechanisms.md`
- **Project State v4.0**: `../../research-coordinator/core/project-state.md`
- **Pipeline Templates v4.0**: `../../research-coordinator/core/pipeline-templates.md`
- **Integration Hub v4.0**: `../../research-coordinator/core/integration-hub.md`
- **Guided Wizard v4.0**: `../../research-coordinator/core/guided-wizard.md`
- **Auto-Documentation v4.0**: `../../research-coordinator/core/auto-documentation.md`
- EQUATOR Network: https://www.equator-network.org/
- PRISMA 2020: Page et al. (2021)
- CONSORT: Schulz et al. (2010)
- STROBE: von Elm et al. (2007)
