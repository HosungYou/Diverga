---
name: preregistration-composer
version: 4.0.0
description: |
  VS-Enhanced Preregistration Composer - Prevents Mode Collapse with comprehensive pre-planning
  Light VS applied: Avoids formal registration + ensures practical research transparency
  Use when: creating preregistration documents, planning confirmatory research, writing registered reports
  Triggers: preregistration, registered report, OSF, AsPredicted, research plan registration
upgrade_level: LIGHT
tier: Support
v3_integration:
  dynamic_t_score: false
  creativity_modules: []
  checkpoints:
    - CP-INIT-001
    - CP-VS-003
---

# Preregistration Composer

**Agent ID**: 20
**Category**: E - Publication & Communication
**VS Level**: Light (Modal awareness)
**Tier**: Support
**Icon**: 🗂️

## Overview

Creates preregistration documents for submission to platforms such as OSF and AsPredicted.
Clearly documents hypotheses, analysis plans, and scenario-based decision rules.

Applies **VS-Research methodology** (Light) to move beyond formal preregistration toward
establishing comprehensive plans that ensure practical research transparency and reproducibility.

## VS Modal Awareness (Light)

⚠️ **Modal Preregistration**: These are the most predictable approaches:

| Domain | Modal Approach (T>0.8) | Comprehensive Approach (T<0.5) |
|--------|------------------------|--------------------------------|
| Hypothesis | "H1: X affects Y" | Directionality + effect size prediction + verification criteria |
| Analysis | "Perform regression" | Pre-write analysis code + assumption check procedures |
| Scenario | "Use nonparametric if violated" | Complete decision tree + response by branch |
| Exploratory | "Additional analysis possible" | Clear confirmatory/exploratory distinction + specify conditions |

**Comprehensive Principle**: Preregistration = binding contract with prior constraint on research decisions

## When to Use

- Before starting confirmatory research
- Preparing Registered Report submission
- Preregistering secondary analysis of existing data
- Planning replication studies

## Core Functions

1. **Template Matching**
   - Select template matching research type
   - Meet platform-specific requirements

2. **Hypothesis Specification**
   - Specific hypotheses with directionality
   - Specify verification criteria
   - Distinguish exploratory/confirmatory

3. **Analysis Plan Detailing**
   - Specify statistical methods
   - Assumption check procedures
   - Multiple comparison correction

4. **Scenario Planning**
   - Alternatives when assumptions violated
   - Response to unexpected results
   - Handle data quality issues

## Preregistration Types

| Type | Platform | Features | Suitable Situations |
|------|----------|----------|---------------------|
| **Standard** | OSF, AsPredicted | Basic preregistration | General confirmatory research |
| **Registered Report** | Journals | Acceptance in principle after review | High uncertainty research |
| **Secondary Data** | OSF | Existing data analysis | Secondary data analysis |
| **Replication** | OSF | Dedicated to replication | Replication/reproduction studies |

## Platform Features

### OSF Registries
- **Advantages**: Free, flexible templates, DOI issuance
- **Templates**: OSF Prereg, AsPredicted, Replication Recipe, etc.
- **URL**: osf.io/registries

### AsPredicted
- **Advantages**: Simple (9 questions), quick writing
- **Limitations**: Fixed template, low flexibility
- **URL**: aspredicted.org

### PROSPERO
- **Target**: Systematic reviews/meta-analyses only
- **Features**: International standard database
- **URL**: crd.york.ac.uk/prospero

## Input Requirements

```yaml
Required:
  - Research plan: "Research purpose, design"
  - Hypotheses: "Hypotheses to test"

Optional:
  - Analysis methods: "Statistical analysis plan"
  - Platform: "OSF, AsPredicted, etc."
  - Type: "Standard, Registered Report, etc."
```

## Output Format (OSF Prereg Template)

```markdown
## Preregistration Document

### Basic Information

**Research Title**: [Specific and descriptive title]

**Authors**: [Author name, affiliation]

**Registration Date**: [Date]

**Platform**: OSF Registries

---

## STUDY INFORMATION

### 1. Title
[Research title - specific and descriptive]

### 2. Research Questions
This study aims to answer the following research questions:

**RQ1**: [Research question 1]
**RQ2**: [Research question 2 - if applicable]

### 3. Hypotheses

**H1**: [Independent variable] will have a [direction] effect on [dependent variable].
- Verification criteria: β > 0 (or < 0), p < .05
- Rationale: [Theoretical/empirical basis]

**H2**: [Mediator] will mediate the relationship between [independent variable] and [dependent variable].
- Verification criteria: Indirect effect significant (95% CI does not include 0)
- Rationale: [Theoretical/empirical basis]

**H3**: The effect of [independent variable] on [dependent variable] will differ according to [moderator].
- Verification criteria: Interaction term p < .05
- Rationale: [Theoretical/empirical basis]

**Exploratory Questions** (preregistered but not confirmatory analysis):
- EQ1: [Exploratory question]

---

## DESIGN PLAN

### 4. Study Design

**Design Type**: [Experimental/Quasi-experimental/Observational/Longitudinal, etc.]

**Independent Variables**:
- [Variable name]: [Manipulation method/measurement method]
  - Levels: [Level 1], [Level 2], ...

**Dependent Variables**:
- [Variable name]: [Measurement method]

**Control Variables**:
- [Variable name]: [Measurement method], Control reason: [Reason]

**Design Diagram**:
```
[Treatment group]: O₁ → X → O₂
[Control group]: O₁ → - → O₂
```

### 5. Randomization
[If applicable] Participants will be randomly assigned to conditions by [method].
Randomization method: [Simple/Stratified/Block randomization]
Randomization tool: [random.org/R code/etc.]

### 6. Blinding
[If applicable]
- Participant blinding: [Yes/No], Method: [Explanation]
- Researcher blinding: [Yes/No], Method: [Explanation]
- Analyst blinding: [Yes/No], Method: [Explanation]

---

## SAMPLING PLAN

### 7. Existing Data
[Check applicable]
- [ ] Data does not exist (as of registration)
- [ ] Data exists but not yet examined
- [ ] Examined some of data (Explanation: [])
- [ ] Already collected data but not analyzed
- [ ] Analyzed data (secondary analysis registration)

### 8. Data Collection Procedures
**Recruitment method**: [Online platform/university community/etc.]
**Data collection period**: [Start date] ~ [End date]
**Data collection location**: [Online/laboratory/field]

**Procedure**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

### 9. Sample Size
**Target sample size**: N = [Number]

**Power analysis**:
- Analysis method: [Analysis type]
- Expected effect size: [d = X / r = X / f² = X]
  - Rationale: [Reference to prior studies]
- Significance level (α): .05
- Power (1-β): .80
- Calculation result: N = [Number]

**Power analysis tool**: G*Power 3.1 / R pwr package

### 10. Sample Size Rationale
[Additional rationale beyond power analysis - if applicable]
- Feasibility constraints: [Explanation]
- Prior study samples: [Reference]

### 11. Stopping Rule
**Data collection stopping criteria**:
- Upon reaching target sample N = [Number]
- Or until [Date] (time constraint)

**Interim analysis**: [Not conducted / Conducted (Rule: [])]

---

## VARIABLES

### 12. Manipulated Variables
[For experimental studies]
**[Variable name]**:
- Condition 1 ([Name]): [Description]
- Condition 2 ([Name]): [Description]
- Manipulation check: [Method]

### 13. Measured Variables

**[Dependent variable name]**:
- Measurement tool: [Tool name] ([Author], [Year])
- Number of items: [Number]
- Scale: [X-point Likert, etc.]
- Scoring: [Method]
- Reliability (prior studies): α = [Value]

**[Independent variable name]** (if measured):
[Same format]

**[Control variable name]**:
[Same format]

### 14. Indices
**[Variable name]** score calculation:
- Method: [Mean/Sum/Factor score]
- Reverse-scored items: [Item numbers]
- Missing data handling: [Method]

---

## ANALYSIS PLAN

### 15. Statistical Models

**Hypothesis 1 test** (H1):
- Analysis method: [Regression/t-test/ANOVA, etc.]
- Model specification: DV ~ IV + control variables
- Software: R (version X.X) / SPSS (version X)
- Packages: [Package names]

**Hypothesis 2 test** (H2) - Mediation:
- Analysis method: [Bootstrap mediation]
- Bootstrap iterations: 5,000
- Confidence interval: 95% percentile CI
- Software/packages: [Specify]

**Hypothesis 3 test** (H3) - Moderation:
- Analysis method: [Hierarchical regression/moderated regression]
- Centering: [Whether mean-centered]
- Software/packages: [Specify]

### 16. Transformations
- If normality violated: [log/sqrt transformation/none]
- Transformation decision criteria: [Shapiro-Wilk p < .05]

### 17. Inference Criteria
- Significance level (α): .05 (two-tailed)
- Confidence interval: 95%
- Multiple comparison correction: [Bonferroni/FDR/none]
- Effect size reporting: [Cohen's d/η²/r]

### 18. Data Exclusion
**Participant exclusion**:
- [ ] Careless responding (Criteria: [Straight-lining > X%, Duration < X min])
- [ ] Manipulation check failure
- [ ] Prior knowledge of study purpose
- [ ] Duplicate participation

**Data exclusion**:
- Missing data: [listwise/pairwise/MI]
- Outliers: [3SD criterion/IQR criterion/Cook's D]

### 19. Missing Data
- Missing ratio criterion: [Exclude variable/participant if > X%]
- Handling method: [Listwise deletion/Multiple imputation (m=20)]
- Missing mechanism assumption: [MCAR/MAR]

### 20. Exploratory Analysis
The following analyses will be performed exploratorily and reported separately from confirmatory analyses:
- [Exploratory analysis 1]
- [Exploratory analysis 2]

---

## OTHER

### 21. Other
[Other items to specify]

---

## Scenario-Based Decision Rules

### When Assumptions Violated
| Assumption | Test method | Alternative if violated |
|------------|------------|------------------------|
| Normality | Shapiro-Wilk | Nonparametric test |
| Homogeneity of variance | Levene's test | Welch's test |
| Linearity | Residual plots | Nonlinear model |

### Other Scenarios
| Scenario | Response |
|----------|----------|
| Target N not reached | [Response plan] |
| Effect size below expectation | [Response plan] |
| High manipulation check failure rate | [Response plan] |

---

## Checklist

- [ ] Are all hypotheses specific and directional?
- [ ] Do analysis methods match hypotheses?
- [ ] Is sample size justification present?
- [ ] Are data exclusion criteria clear?
- [ ] Are exploratory/confirmatory analyses distinguished?
- [ ] Are scenario-based decision rules present?
```

## Prompt Template

```
You are a research preregistration expert.

Please write a preregistration document for the following research:

[Research plan]: {plan}
[Hypotheses]: {hypotheses}
[Analysis methods]: {analysis}
[Platform]: {platform}

Tasks to perform:
1. Research information
   - Title
   - Researcher information
   - Research questions

2. Hypotheses
   - H1: [Specific, directional prediction]
   - H2: ...
   - Specify verification criteria for each hypothesis

3. Research design
   - Design type
   - Sampling plan
   - Sample size justification
   - Inclusion/exclusion criteria

4. Variables
   - Independent variables: Definition, measurement, manipulation
   - Dependent variables: Definition, measurement
   - Control variables: Selection rationale

5. Analysis plan
   - Main analysis: [Specific statistical method]
   - Assumption checks: [Tests to perform]
   - Inference criteria: [α level, one/two-tailed]

6. Scenario-based decision rules
   - If assumptions violated: [Alternative analysis]
   - If sample size not reached: [Response]
   - If unexpected results: [Interpretation guidelines]

7. Confirmatory vs. exploratory analysis distinction
   - Confirmatory: [Pre-planned analyses]
   - Exploratory: [Possible additional analyses]
```

## Preregistration Checklist

### Required Elements
- [ ] Specific and directional hypotheses
- [ ] Sample size and justification
- [ ] Data collection procedures
- [ ] Analysis methods specified
- [ ] Data exclusion criteria
- [ ] Inference criteria (α, one/two-tailed)

### Recommended Elements
- [ ] Detailed power analysis
- [ ] Scenario-based decision rules
- [ ] Exploratory/confirmatory distinction
- [ ] Measurement tool reliability/validity

## Related Agents

- **01-research-question-refiner**: Refine questions before hypothesis formulation
- **09-research-design-consultant**: Optimize design
- **15-reproducibility-auditor**: Check reproducibility

## References

- **VS Engine v3.0**: `../../research-coordinator/core/vs-engine.md`
- **Dynamic T-Score**: `../../research-coordinator/core/t-score-dynamic.md`
- **Creativity Mechanisms**: `../../research-coordinator/references/creativity-mechanisms.md`
- **Project State v4.0**: `../../research-coordinator/core/project-state.md`
- **Pipeline Templates v4.0**: `../../research-coordinator/core/pipeline-templates.md`
- **Integration Hub v4.0**: `../../research-coordinator/core/integration-hub.md`
- **Guided Wizard v4.0**: `../../research-coordinator/core/guided-wizard.md`
- **Auto-Documentation v4.0**: `../../research-coordinator/core/auto-documentation.md`
- OSF Registries: https://osf.io/registries
- AsPredicted: https://aspredicted.org
- Nosek et al. (2018). The Preregistration Revolution
- van 't Veer & Giner-Sorolla (2016). Pre-registration in Social Psychology
