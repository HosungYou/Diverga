---
name: b3
description: |
  VS-Enhanced Effect Size Extractor - Prevents Mode Collapse with optimal effect size strategy
  Enhanced VS 3-Phase process: Avoids simple conversions, delivers context-appropriate effect size selection
  Use when: extracting effect sizes, converting statistics, preparing meta-analysis data
  Triggers: effect size, Cohen's d, Hedges' g, correlation, conversion, meta-analysis data
---

# Effect Size Extractor

**Agent ID**: 07
**Category**: B - Literature & Evidence
**VS Level**: Enhanced (3-Phase)
**Tier**: Support
**Icon**: 📊

## Overview

Converts various forms of statistics from research papers into standardized effect sizes.
Accurately calculates effect sizes and variances/standard errors needed for meta-analysis.

**VS-Research methodology** is applied to go beyond simple formula application and provide
effect size strategies optimized for research design and meta-analysis purposes.

## VS-Research 3-Phase Process (Enhanced)

### Phase 1: Identify Modal Effect Size Approaches

**Purpose**: Recognize limitations of simple formula application

```markdown
⚠️ **Modal Warning**: These are the most predictable effect size extraction approaches:

| Modal Approach | T-Score | Limitations |
|----------------|---------|-------------|
| "Apply t → d formula" | 0.90 | Ignores design specificity |
| "Standardize to Cohen's d" | 0.88 | May not be optimal scale |
| "Reverse calculate p → t when missing" | 0.85 | Information loss, increased uncertainty |

➡️ Formula application is baseline. Exploring optimal effect size strategy.
```

### Phase 2: Context-Optimal Effect Size Strategy

**Purpose**: Effect size strategy matched to research design and meta-analysis purpose

```markdown
**Direction A** (T ≈ 0.7): Standard Conversion + Design Correction
- Standard formulas + Hedges' g correction
- Matched/repeated measures design correction
- Suitable for: General meta-analyses

**Direction B** (T ≈ 0.4): Purpose-Specific Scales
- Select optimal scale by meta-analysis type
- Consider clustered/multilevel designs
- Dependency handling strategies
- Suitable for: Complex designs, education/psychology research

**Direction C** (T < 0.3): Information Maximization Strategy
- Multiple estimation methods from incomplete reporting
- Bayesian effect size estimation
- Uncertainty propagation analysis
- Suitable for: Methodological research, precision meta-analysis
```

### Phase 4: Execute Recommendation

**Based on selected effect size strategy**:
1. Rationale for optimal scale selection
2. Conversion formulas and calculation process
3. Variance/SE calculations
4. Meta-analysis data format

---

## Effect Size Extraction Typicality Score Reference Table

```
T > 0.8 (Modal - Needs Enhancement):
├── Statistics → automatic standard formula application
├── Uniform conversion to Cohen's d
├── Simple estimation of missing information
└── Ignore design specificity

T 0.5-0.8 (Established - Needs Refinement):
├── Hedges' g small sample correction
├── Matched/repeated measures correction
├── Reverse calculate SE from confidence intervals
└── Apply field-specific interpretation criteria

T 0.3-0.5 (Deep - Recommended):
├── Optimal scale by meta-analysis type
├── Clustered design effect correction
├── Multiple outcome dependency handling
└── Quantify conversion uncertainty

T < 0.3 (Innovation - For Leading Research):
├── Bayesian effect size estimation
├── Multiple imputation for incomplete reporting
├── Model effect size as function
└── Integrate measurement error
```

## When to Use

- When extracting data for meta-analysis
- When cross-study effect comparison is needed
- When standardizing various statistics is required
- When effect size interpretation is needed

## Core Functions

1. **Process Various Inputs**
   - Means and standard deviations
   - t-values, F-values
   - Correlation coefficients (r)
   - Chi-square, odds ratios
   - p-values and sample sizes

2. **Effect Size Conversions**
   - Cohen's d ↔ Hedges' g
   - d ↔ r
   - OR ↔ d
   - Various mutual conversions

3. **Variance/Standard Error Calculation**
   - For meta-analysis weighting
   - Confidence interval calculation

4. **Dependency Handling**
   - Repeated measures designs
   - Clustered designs
   - Multiple outcome variables

## Conversion Formula Library

### Basic Effect Size Calculations

**Cohen's d (Independent Groups)**
```
d = (M₁ - M₂) / SD_pooled

SD_pooled = √[((n₁-1)SD₁² + (n₂-1)SD₂²) / (n₁ + n₂ - 2)]
```

**Hedges' g (Small Sample Correction)**
```
g = d × J

J = 1 - 3/(4(n₁ + n₂) - 9)
```

**Cohen's d (Matched Groups)**
```
d = M_diff / SD_diff

or

d = (M_pre - M_post) / SD_pooled × √(2(1-r))
```

### Conversion Formulas

**t → d**
```
d = t × √(1/n₁ + 1/n₂)
```

**F → d (2 groups)**
```
d = √(F × (n₁ + n₂) / (n₁ × n₂))
```

**r → d**
```
d = 2r / √(1 - r²)
```

**d → r**
```
r = d / √(d² + 4)
```

**OR → d**
```
d = ln(OR) × √3 / π
```

**η² → d**
```
d = 2 × √(η² / (1 - η²))
```

**r → Fisher's z**
```
z = 0.5 × ln[(1 + r) / (1 - r)]
```

### Variance Calculations

**Variance of d**
```
V_d = (n₁ + n₂)/(n₁ × n₂) + d²/(2(n₁ + n₂))
```

**Variance of r**
```
V_r = (1 - r²)² / (n - 1)
```

**Variance of Fisher's z**
```
V_z = 1 / (n - 3)
```

## Input Requirements

```yaml
Required:
  - Original statistic: "Reported statistical value"
  - Sample size: "Each group or total N"

Optional:
  - Target effect size: "Choose from d, r, OR"
  - Research design: "Independent/matched/repeated measures"
  - Pre-post correlation: "For matched designs"
```

## Output Format

```markdown
## Effect Size Conversion Report

### 1. Input Information

| Item | Value |
|------|-------|
| Original statistic | [value] |
| Statistic type | [t/F/r/χ²/M&SD, etc.] |
| n₁ | [value] |
| n₂ | [value] |
| Design type | [Independent/Matched] |

### 2. Conversion Process

**Applied Formula:**
```
[Specify formula]
```

**Calculation Steps:**
```
Step 1: [Intermediate calculation]
Step 2: [Intermediate calculation]
...
Final: [Result]
```

### 3. Results

| Effect Size | Value | SE | 95% CI |
|-------------|-------|-----|--------|
| Cohen's d | [value] | [SE] | [lower, upper] |
| Hedges' g | [value] | [SE] | [lower, upper] |
| r | [value] | [SE] | [lower, upper] |

### 4. Interpretation

**Cohen (1988) Criteria:**
- Small: d = 0.2, r = .10
- Medium: d = 0.5, r = .30
- Large: d = 0.8, r = .50

**Current Study Effect Size**: [Small/Medium/Large] level

### 5. Meta-Analysis Input Data

```csv
study_id, yi, vi, ni
[study], [effect], [variance], [n]
```
```

## Prompt Template

```
You are a meta-analysis effect size calculation expert.

Please convert the following statistics to standardized effect sizes:

[Original Statistic]: {original_statistic}
[Sample Size]: {sample_size}
[Target Effect Size]: {target_es} (choose from d, r, OR)

Tasks to perform:
1. Identify original statistic type
   - Cohen's d / Hedges' g
   - Pearson r
   - t-value
   - F-value (include df1, df2)
   - χ² (chi-square)
   - η² / η²_partial
   - Odds Ratio / Risk Ratio
   - Means and standard deviations

2. Perform conversion
   - Specify formula to apply
   - Detail calculation process
   - Show all intermediate values

3. Calculate variance/standard error
   - Sample variance formula for effect size
   - For meta-analysis weighting

4. Calculate 95% confidence interval

5. Summarize results
   | Original Statistic | Converted ES | SE | 95% CI |
```

## Effect Size Interpretation Criteria

### Cohen (1988) General Criteria
| Effect Size | Small | Medium | Large |
|-------------|-------|--------|-------|
| d | 0.2 | 0.5 | 0.8 |
| r | .10 | .30 | .50 |
| η² | .01 | .06 | .14 |
| OR | 1.5 | 2.5 | 4.0 |

### Field-Specific Criteria (Education/Psychology)
| Intervention Type | Average d | Adjusted Criteria |
|-------------------|-----------|-------------------|
| Educational interventions | 0.40 | Small: 0.15, Med: 0.40, Large: 0.65 |
| Psychotherapy | 0.50 | Use general criteria |
| Pharmacological treatment | 0.30 | Small: 0.10, Med: 0.30, Large: 0.50 |

## Special Situation Handling

### Multiple Treatment Groups (3+ groups)
- Pairwise vs. pooled comparisons
- Variance pooling methods

### Repeated Measures
- Pre-post correlation needed
- Dependency correction

### Clustered Designs
- Apply Design Effect
- ICC-based correction

### Missing Information Estimation
- Reverse calculate t from p-value
- Reverse calculate SE from CI

## Related Agents

- **05-systematic-literature-scout**: Research search and collection
- **06-evidence-quality-appraiser**: Quality assessment
- **10-statistical-analysis-guide**: Meta-analysis method guidance

## v3.0 Creative Device Integration

### Available Creative Devices (ENHANCED)

| Device | Application Point | Usage Example |
|--------|-------------------|---------------|
| **Forced Analogy** | Phase 2 | Apply effect size scales from other fields by analogy |
| **Iterative Loop** | Phase 2 | 4-round divergence-convergence to refine optimal conversion strategy |
| **Semantic Distance** | Phase 2 | Discover new effect size interpretation criteria |

### Checkpoint Integration

```yaml
Applied Checkpoints:
  - CP-INIT-002: Select creativity level
  - CP-VS-001: Select effect size strategy direction (multiple)
  - CP-VS-003: Confirm final effect size strategy satisfaction
  - CP-IL-001: Set iteration round count
```

### Module References

```
../../research-coordinator/core/vs-engine.md
../../research-coordinator/core/t-score-dynamic.md
../../research-coordinator/creativity/forced-analogy.md
../../research-coordinator/creativity/iterative-loop.md
../../research-coordinator/creativity/semantic-distance.md
../../research-coordinator/interaction/user-checkpoints.md
```

---

---

## Effect Size Selection Hierarchy (V7 Lesson)

### Mandatory Selection Rules

When a study reports multiple statistics, apply this hierarchy:

| Priority | Type | Formula | Use When |
|----------|------|---------|----------|
| **1 (Best)** | Post-test between-groups | d = (M_post_T - M_post_C) / SD_pooled | Control group exists |
| **2** | ANCOVA-adjusted | Use adjusted means | Pre-test as covariate |
| **3** | Change score | d = (delta_M_T - delta_M_C) / SD_pooled_change | No between-group post |
| **4 (Last)** | Single-group pre-post | d = (M_post - M_pre) / SD_pre | No control group |

### NEVER Include

- Pre-test scores as independent outcomes
- Baseline equivalence checks (these verify, not measure effect)
- Multiple timepoints without 3-level modeling

### Human Checkpoint: CP_ES_HIERARCHY

**Trigger**: Study has >1 potential effect size

**Required Decision**:
1. Which ES best represents treatment effect?
2. Rationale for selection
3. How to handle excluded ES (document or sensitivity analysis)

### Pre-test Exclusion Patterns

```python
EXCLUDE_PATTERNS = [
    r'pre[- ]?test', r'pretest', r'baseline',
    r'pre[- ]?intervention', r'pre[- ]?training',
    r'time\s*1', r'T1(?!\d)', r'before\s+treatment'
]
```

### Cohen's d to Hedges' g Verification

**ALWAYS verify the conversion:**

```python
def verify_hedges_g(d, n1, n2):
    df = n1 + n2 - 2
    J = 1 - (3 / (4 * df - 1))
    g = d * J
    SE_g = sqrt((n1 + n2) / (n1 * n2) + g**2 / (2 * (n1 + n2)))
    return {'g': g, 'SE': SE_g, 'J': J}
```

**Tolerance**: |calculated_g - reported_g| < 0.01

---

## References

- **VS Engine v3.0**: `../../research-coordinator/core/vs-engine.md`
- **Dynamic T-Score**: `../../research-coordinator/core/t-score-dynamic.md`
- **Creativity Mechanisms**: `../../research-coordinator/references/creativity-mechanisms.md`
- **Project State v4.0**: `../../research-coordinator/core/project-state.md`
- **Pipeline Templates v4.0**: `../../research-coordinator/core/pipeline-templates.md`
- **Integration Hub v4.0**: `../../research-coordinator/core/integration-hub.md`
- **Guided Wizard v4.0**: `../../research-coordinator/core/guided-wizard.md`
- **Auto-Documentation v4.0**: `../../research-coordinator/core/auto-documentation.md`
- Borenstein et al. (2009). Introduction to Meta-Analysis
- Cooper et al. (2019). Handbook of Research Synthesis
- Lipsey & Wilson (2001). Practical Meta-Analysis
- metafor R package documentation
