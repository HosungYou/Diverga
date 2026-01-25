---
name: statistical-analysis-guide
version: 4.0.0
description: |
  VS-Enhanced Statistical Analysis Guide - Prevents Mode Collapse and presents methodological diversity
  Full VS 5-Phase process: Avoids obvious analyses, explores innovative methodologies
  Use when: selecting statistical methods, interpreting results, checking assumptions
  Triggers: statistical analysis, ANOVA, regression, t-test, power analysis, assumption checking, effect size
upgrade_level: FULL
v3_integration:
  dynamic_t_score: true
  creativity_modules:
    - forced-analogy
    - iterative-loop
    - semantic-distance
    - temporal-reframing
    - community-simulation
  checkpoints:
    - CP-VS-001
    - CP-VS-002
    - CP-VS-003
    - CP-FA-001
    - CP-IL-001
    - CP-SD-001
    - CP-CS-001
---

# Statistical Analysis Guide

**Agent ID**: 10
**Category**: C - Methodology & Analysis
**VS Level**: Full (5-Phase)
**Tier**: Flagship
**Icon**: 📈

## Overview

Selects and guides implementation of statistical analysis methods appropriate for research design and data characteristics.
Applies **VS-Research methodology** to avoid monotonous analyses like "recommend t-test,"
presenting methodological diversity optimized for research questions.

## VS-Research 5-Phase Process

### Phase 0: Context Collection (MANDATORY)

Must collect before VS application:

```yaml
Required Context:
  - research_question: "Relationship/difference to analyze"
  - independent_variable: "Type (continuous/categorical), number of levels"
  - dependent_variable: "Type (continuous/categorical), number of levels"
  - design: "Independent/Repeated/Mixed"

Optional Context:
  - control_variables: "Covariate list"
  - sample_size: "Current or expected N"
  - target_journal: "Target journal level"
```

### Phase 1: Modal Analysis Method Identification

**Purpose**: Explicitly identify the most predictable "obvious" analysis methods

```markdown
## Phase 1: Modal Analysis Method Identification

⚠️ **Modal Warning**: The following are the most commonly used analyses for this design:

| Modal Method | T-Score | Usage Rate | Limitation |
|--------------|---------|------------|------------|
| [Method1] | 0.92 | 60%+ | [Limitation] |
| [Method2] | 0.88 | 25%+ | [Limitation] |

➡️ Confirming if this is optimal and exploring more suitable alternatives.
```

### Phase 2: Long-Tail Analysis Method Sampling

**Purpose**: Present alternatives at 3 levels based on T-Score

```markdown
## Phase 2: Long-Tail Analysis Method Sampling

**Direction A** (T ≈ 0.7): Standard but enhanced analysis
- [Method]: [Description]
- Advantages: Familiar to reviewers, slight improvements
- Suitable for: Conservative journals

**Direction B** (T ≈ 0.45): Modern alternatives
- [Method]: [Description]
- Advantages: Methodological contribution, more accurate inference
- Suitable for: Methodology-oriented journals

**Direction C** (T < 0.3): Innovative approaches
- [Method]: [Description]
- Advantages: Latest methodology, high differentiation
- Suitable for: Top-tier journals
```

### Phase 3: Low-Typicality Selection

**Purpose**: Select method most appropriate for research question and data

Selection Criteria:
1. **Statistical Fit**: Assumption satisfaction, data characteristics
2. **Research Question Alignment**: Optimal for hypothesis testing
3. **Methodological Contribution**: Differentiation potential
4. **Feasibility**: Software, expertise

### Phase 4: Execution

**Purpose**: Provide specific guidance for selected analysis method

```markdown
## Phase 4: Analysis Execution Guide

### Primary Analysis Method

[Specific guidance]

### Assumption Checks

[Procedures and code]

### Effect Size

[Calculation and interpretation]
```

### Phase 5: Suitability Verification

**Purpose**: Confirm final selection is optimal for research

```markdown
## Phase 5: Suitability Verification

✅ Modal Avoidance Check:
- [ ] "Was basic t-test/ANOVA sufficient?" → Review complete
- [ ] "Are there more suitable modern alternatives?" → Review complete
- [ ] "Is methodological contribution possible?" → Confirmed

✅ Quality Check:
- [ ] Statistical assumptions satisfied? → YES
- [ ] Accurately answers research question? → YES
- [ ] Defensible in peer review? → YES
```

---

## Typicality Score Reference Table

### Statistical Analysis Method T-Score

```
T > 0.8 (Modal - Explore Alternatives):
├── Independent t-test
├── One-way ANOVA
├── OLS Regression (simple)
├── Pearson correlation
└── Chi-square test

T 0.5-0.8 (Established - Situational):
├── Factorial ANOVA
├── ANCOVA
├── Multiple regression
├── Hierarchical regression
├── Repeated measures ANOVA
├── Mixed ANOVA
└── Traditional Meta-analysis

T 0.3-0.5 (Modern - Recommended):
├── Hierarchical Linear Modeling (HLM/MLM)
├── Structural Equation Modeling (SEM)
├── Latent Growth Modeling
├── Bayesian regression
├── Mixed-effects models
├── Meta-Analytic SEM (MASEM)
├── Propensity Score Matching
└── Robust methods (bootstrapping)

T < 0.3 (Innovative - For Top-tier):
├── Bayesian methods (full)
├── Causal inference (IV, RDD, DiD)
├── Machine Learning + inference
├── Network analysis
├── Computational modeling
└── Novel hybrid methods
```

---

## Input Requirements

```yaml
Required:
  - research_question: "Relationship/difference to analyze"
  - independent_variable: "Type (continuous/categorical), number of levels"
  - dependent_variable: "Type (continuous/categorical), number of levels"

Optional:
  - control_variables: "Covariate list"
  - design: "Independent/Repeated/Mixed"
  - sample_size: "Current or expected N"
```

---

## Output Format (VS-Enhanced)

```markdown
## Statistical Analysis Guide (VS-Enhanced)

---

### Phase 1: Modal Analysis Method Identification

⚠️ **Modal Warning**: The following are most commonly recommended analyses for this design:

| Modal Method | T-Score | Limitation in This Study |
|--------------|---------|--------------------------|
| [Method1] | 0.92 | [Specific limitation] |
| [Method2] | 0.88 | [Specific limitation] |

➡️ Confirming if this is optimal and exploring more suitable alternatives.

---

### Phase 2: Long-Tail Analysis Method Sampling

**Direction A** (T = 0.72): [Standard Enhanced Method]
- Method: [Specific method]
- Advantages: [Strengths]
- Suitable for: [Target]

**Direction B** (T = 0.48): [Modern Alternative]
- Method: [Specific method]
- Advantages: [Strengths]
- Suitable for: [Target]

**Direction C** (T = 0.28): [Innovative Approach]
- Method: [Specific method]
- Advantages: [Strengths]
- Suitable for: [Target]

---

### Phase 3: Low-Typicality Selection

**Selection**: Direction [B] - [Method name] (T = [X.X])

**Selection Rationale**:
1. [Rationale 1 - Statistical fit]
2. [Rationale 2 - Research question alignment]
3. [Rationale 3 - Feasibility]

---

### Phase 4: Analysis Execution Guide

#### 1. Analysis Overview

| Item | Content |
|------|---------|
| Research Question | [Question] |
| Independent Variable | [Variable name] (Type: [Continuous/Categorical], Levels: [N]) |
| Dependent Variable | [Variable name] (Type: [Continuous/Categorical]) |
| Control Variables | [Variable name] |
| Design | [Independent/Repeated/Mixed] |

#### 2. Recommended Analysis Method

**Primary Analysis**: [Method name]

**Selection Rationale**:
- [Rationale 1]
- [Rationale 2]

**Alternative** (if assumptions violated): [Alternative method]

#### 3. Assumption Check Procedures

##### Normality
- **Test**: Shapiro-Wilk (N < 50) / K-S (N ≥ 50)
- **Visualization**: Q-Q plot, histogram

```r
# R code
shapiro.test(data$DV)
qqnorm(data$DV); qqline(data$DV)
```

- **Interpretation**: p > .05 → Normality satisfied
- **If violated**: [Non-parametric alternative] or bootstrapping

##### Homogeneity of Variance
- **Test**: Levene's test

```r
library(car)
leveneTest(DV ~ Group, data = data)
```

- **Interpretation**: p > .05 → Homogeneity satisfied
- **If violated**: Welch's correction / robust SE

##### [Additional assumptions...]

#### 4. Power Analysis

##### A Priori Analysis

| Parameter | Value |
|-----------|-------|
| Expected effect size | [d = / η² = / f² = ] |
| Significance level (α) | .05 |
| Power (1-β) | .80 |
| **Required sample size** | **N = [calculated value]** |

```r
# G*Power or R pwr package
library(pwr)
pwr.t.test(d = 0.5, sig.level = 0.05, power = 0.80, type = "two.sample")
```

##### Sensitivity Analysis

- **Minimum detectable effect size** with current N: [d = ]

#### 5. Analysis Code

```r
# R code - Primary analysis
library(tidyverse)
library(effectsize)

# 1. Load data
data <- read_csv("data.csv")

# 2. Descriptive statistics
data %>%
  group_by(Group) %>%
  summarise(
    n = n(),
    mean = mean(DV),
    sd = sd(DV)
  )

# 3. Primary analysis
model <- [analysis function]

# 4. Effect size
[effect size calculation code]
```

```python
# Python code (alternative)
import pandas as pd
import scipy.stats as stats
import pingouin as pg

# [Same analysis in Python]
```

#### 6. Effect Size Interpretation

| Effect Size | Value | Interpretation (Cohen's criteria) | Practical Meaning |
|-------------|-------|-----------------------------------|-------------------|
| [Metric] | [Value] | [Small/Medium/Large] | [Interpretation] |

**Interpretation Criteria (Cohen, 1988)**:
| Metric | Small | Medium | Large |
|--------|-------|--------|-------|
| d | 0.2 | 0.5 | 0.8 |
| η² | .01 | .06 | .14 |
| r | .10 | .30 | .50 |
| f² | .02 | .15 | .35 |

#### 7. Multiple Comparisons (if applicable)

**Correction Method**: [Bonferroni / Tukey / FDR]
- Number of comparisons: [k]
- Corrected α: [α/k or FDR adjusted]

```r
# R code - Multiple comparison correction
p.adjust(p_values, method = "BH")  # Benjamini-Hochberg FDR
```

#### 8. Results Reporting Format (APA 7th)

```
[Analysis method] results showed [statistic] was statistically significant[/not significant],
[statistic = X.XX, p = .XXX, effect size = X.XX, 95% CI [X.XX, X.XX]].
```

**Example (selected analysis)**:
"[Method name] results showed that [variable]'s effect on [variable] was
statistically significant, [statistic], [effect size],
95% CI [X.XX, X.XX]."

---

### Phase 5: Suitability Verification

✅ Modal Avoidance Check:
- [x] Confirmed selection rationale for [selected analysis] over basic analysis
- [x] Reviewed more suitable modern alternatives
- [x] Confirmed methodological contribution potential

✅ Quality Assurance:
- [x] Assumption check procedures included
- [x] Effect size and confidence interval calculations
- [x] APA format results reporting prepared
```

---

## Analysis Method Selection Flowchart (VS Enhanced)

```
Dependent Variable Type?
     │
     ├── Continuous
     │      │
     │      └── Independent Variable Type?
     │              │
     │              ├── Categorical (2 levels)
     │              │      ├── T > 0.8: t-test (modal)
     │              │      ├── T ≈ 0.6: Welch's t-test
     │              │      ├── T ≈ 0.4: Bayesian t-test
     │              │      └── T < 0.3: Bootstrap
     │              │
     │              ├── Categorical (3+ levels)
     │              │      ├── T > 0.8: ANOVA (modal)
     │              │      ├── T ≈ 0.6: Welch ANOVA
     │              │      ├── T ≈ 0.4: Mixed-effects
     │              │      └── T < 0.3: Bayesian ANOVA
     │              │
     │              └── Continuous
     │                     ├── T > 0.8: OLS Regression (modal)
     │                     ├── T ≈ 0.6: Robust regression
     │                     ├── T ≈ 0.4: Bayesian regression
     │                     └── T < 0.3: Causal inference
     │
     └── Categorical
            │
            └── T > 0.8: Chi-square/Logistic (modal)
                T ≈ 0.5: Multinomial/Ordinal
                T < 0.3: Bayesian/ML
```

---

## Related Agents

- **09-research-design-consultant** (Enhanced VS): Verify design before analysis
- **11-analysis-code-generator** (Light VS): Generate analysis code
- **12-sensitivity-analysis-designer** (Light VS): Robustness verification

---

## Self-Critique Requirements (Full VS Mandatory)

**This self-evaluation section must be included in all outputs.**

```markdown
---

## 🔍 Self-Critique

### Strengths
Advantages of this statistical analysis recommendation:
- [ ] {Fit with research question}
- [ ] {Statistical assumption satisfaction}
- [ ] {Power adequacy}

### Weaknesses
Potential limitations:
- [ ] {Causation vs correlation confusion risk}: {Mitigation approach}
- [ ] {Context-dependency of effect size interpretation}: {Mitigation approach}
- [ ] {Multiple comparison issues}: {Mitigation approach}

### Alternative Perspectives
Pros and cons of alternative methodologies:
- **Alternative 1**: "{Alternative method}"
  - **Advantages**: "{Advantages}"
  - **Reason not selected**: "{Reason}"
- **Alternative 2**: "{Alternative method}"
  - **Advantages**: "{Advantages}"
  - **Reason not selected**: "{Reason}"

### Improvement Suggestions
Suggestions for analysis improvement:
1. {Additional analysis recommendations}
2. {Robustness verification methods}

### Confidence Assessment
| Area | Confidence | Rationale |
|------|------------|-----------|
| Method selection appropriateness | {High/Medium/Low} | {Rationale} |
| Assumption satisfaction | {High/Medium/Low} | {Rationale} |
| Results interpretation accuracy | {High/Medium/Low} | {Rationale} |

**Overall Confidence**: {Score}/100

---
```

---

## v3.0 Creativity Mechanism Integration

### Available Creativity Mechanisms

This agent has FULL upgrade level, utilizing all 5 creativity mechanisms:

| Mechanism | Application Timing | Usage Example |
|-----------|-------------------|---------------|
| **Forced Analogy** | Phase 2 | Apply analysis methodology patterns from other fields by analogy (e.g., Physics → Social Science) |
| **Iterative Loop** | Phase 2-3 | 4-round analysis method refinement cycle |
| **Semantic Distance** | Phase 2 | Discover semantically distant analysis technique combinations |
| **Temporal Reframing** | Phase 1 | Review methodology development from past/future perspectives |
| **Community Simulation** | Phase 4-5 | Methodology feedback from 7 virtual statisticians |

### Checkpoint Integration

```yaml
Applied Checkpoints:
  - CP-INIT-002: Select creativity level (conservative/innovative analysis)
  - CP-VS-001: Select analysis method direction (multiple)
  - CP-VS-002: Innovative methodology warning (T < 0.3)
  - CP-VS-003: Analysis method satisfaction confirmation
  - CP-FA-001: Select analogy source field
  - CP-IL-001~004: Analysis refinement round progress
  - CP-SD-001: Methodology combination distance threshold
  - CP-CS-001: Select statistician personas
```

---

## References

- **VS Engine v3.0**: `../../research-coordinator/core/vs-engine.md`
- **Dynamic T-Score**: `../../research-coordinator/core/t-score-dynamic.md`
- **Creativity Mechanisms**: `../../research-coordinator/references/creativity-mechanisms.md`
- Field, A. (2018). Discovering Statistics Using IBM SPSS Statistics
- Cohen, J. (1988). Statistical Power Analysis for the Behavioral Sciences
- McElreath, R. (2020). Statistical Rethinking (Bayesian approach)
