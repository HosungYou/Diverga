# QUANT-003 Test Session Transcript

**CLI Tool**: claude
**Session ID**: 13a518a2-3d1f-44bf-8550-a8a34959eea2
**Start Time**: 2026-01-30T13:33:55.753358
**End Time**: 2026-01-30T13:37:02.505551
**Status**: completed

---

## Turn 1: 👤 USER

I want to conduct a meta-analysis on the effectiveness of AI tutoring
systems on student learning outcomes. I have 25 studies with various
effect sizes reported (Cohen's d, Hedges' g, correlation r, and some
only report means/SDs). How should I standardize these effect sizes?

---

## Turn 1: 🤖 ASSISTANT

I see this is a meta-analysis on AI tutoring systems with mixed effect size formats. This is a core competency of the **Effect Size Extractor (B3)** agent with support from the **Meta-Analysis Master (C5)** for complex conversions.

---

## 🔴 CHECKPOINT: CP_PARADIGM_CONFIRMATION

Your request signals a **Quantitative research** approach (meta-analysis, effect sizes).

**Confirm paradigm:**
- [Y] Yes, proceed with quantitative meta-analysis approach
- [?] I need clarification first

---

## Effect Size Standardization Strategy

For your 25 studies with mixed effect size formats, here's the standardization approach:

### Current Data Inventory

| Format | Studies | Conversion Needed |
|--------|---------|-------------------|
| Cohen's d | ? | Convert to Hedges' g (bias correction) |
| Hedges' g | ? | ✅ Target metric (no conversion) |
| Correlation r | ? | Convert via Fisher's z transformation |
| Means/SDs only | ? | Calculate d, then g |

### Recommended Target: **Hedges' g**

**Why Hedges' g instead of Cohen's d?**
1. **Small sample correction** - Cohen's d overestimates effects in small samples (n < 20)
2. **Meta-analysis standard** - Most meta-analysis software expects g
3. **Unbiased estimator** - Correction factor J = 1 - 3/(4df - 1)

### Conversion Formulas

**1. Cohen's d → Hedges' g:**
```
g = d × J
where J = 1 - (3 / (4(n₁ + n₂ - 2) - 1))
```

**2. Means/SDs → Cohen's d → Hedges' g:**
```
d = (M₁ - M₂) / SD_pooled
SD_pooled = √[((n₁-1)×SD₁² + (n₂-1)×SD₂²) / (n₁ + n₂ - 2)]
Then apply J correction for g
```

**3. Correlation r → Hedges' g:**
```
d = 2r / √(1 - r²)
Then apply J correction for g
SE(g) = √[(4 + d²) / 2n × J²]
```

**4. For correlational data (optional alternative):**
- Keep as r and use Fisher's z transformation: z = 0.5 × ln[(1+r)/(1-r)]
- Analyze separately if mixing experimental vs. correlational designs

---

## 🟠 CHECKPOINT: Effect Size Target Selection

**Which standardization approach do you prefer?**

| Option | T-Score | Description |
|--------|---------|-------------|
| **[A]** | 0.65 | **Hedges' g for all** - Convert everything to g (recommended for experimental designs) |
| **[B]** | 0.45 | **Separate by design type** - g for experimental, r (via Fisher's z) for correlational ⭐ |
| **[C]** | 0.30 | **d-to-r conversion** - Convert all to correlation scale for path modeling |

---

### Before I proceed with detailed calculations, please confirm:

1. **Paradigm**: [Y] to confirm quantitative meta-analysis?
2. **Target metric**: Which option (A/B/C) for standardization?
3. **Sample sizes available?** (needed for Hedges' g correction)

I can then invoke the **C5-MetaAnalysisMaster** and **B3-EffectSizeExtractor** agents in parallel to:
- Generate your extraction template
- Calculate exact conversions for each study
- Produce variance estimates for meta-analytic pooling


**Checkpoints Detected**: CP_PARADIGM_CONFIRMATION
  - Details: CP_PARADIGM_CONFIRMATION(HIGH)

**Skill Loaded**: ✅ (Confidence: HIGH)

---

## Turn 2: 👤 USER

Why is Hedges' g preferred over Cohen's d for meta-analysis? Some of
my studies have small samples (n < 20). Also, one study only reports
F-statistics from ANOVA. How do I convert that to Hedges' g?

---

## Turn 2: 🤖 ASSISTANT

Great questions. Let me address both directly.

---

## Why Hedges' g Over Cohen's d for Meta-Analysis

### The Small Sample Bias Problem

Cohen's d systematically **overestimates** the true population effect size when samples are small. This is a mathematical bias, not a random error.

| Sample Size (per group) | Bias in Cohen's d | Hedges' g Correction (J) |
|-------------------------|-------------------|--------------------------|
| n = 5 | +12% overestimate | J = 0.8407 |
| n = 10 | +6% overestimate | J = 0.9227 |
| n = 15 | +4% overestimate | J = 0.9474 |
| n = 20 | +3% overestimate | J = 0.9620 |
| n = 50 | +1% overestimate | J = 0.9849 |
| n = 100+ | negligible | J ≈ 0.99+ |

**Your situation**: With studies n < 20, using uncorrected Cohen's d would inflate your pooled effect estimate. Hedges' g applies a correction factor:

```
g = d × J
J = 1 - (3 / (4 × df - 1))

where df = n₁ + n₂ - 2 (for two independent groups)
```

### Practical Example

Study with n₁ = 10, n₂ = 10 reports d = 0.80:
```
df = 10 + 10 - 2 = 18
J = 1 - (3 / (4 × 18 - 1)) = 1 - (3/71) = 0.9577
g = 0.80 × 0.9577 = 0.766
```

The "true" unbiased estimate is **g = 0.77**, not d = 0.80.

---

## Converting F-statistic from ANOVA to Hedges' g

This depends on your ANOVA design.

### Case 1: Two-group comparison (F from one-way ANOVA with 2 groups)

When F has df₁ = 1 (numerator), it's equivalent to a t-test:

```
t = √F
d = t × √(1/n₁ + 1/n₂)
```

Or directly:
```
d = √(F × (n₁ + n₂) / (n₁ × n₂))
```

Then convert to g with the J correction.

**Example**: F(1, 38) = 6.25, with n₁ = 20, n₂ = 20
```
d = √(6.25 × (20 + 20) / (20 × 20))
d = √(6.25 × 40 / 400)
d = √0.625 = 0.791

J = 1 - 3/(4 × 38 - 1) = 0.9803
g = 0.791 × 0.9803 = 0.775
```

### Case 2: F from ANOVA with 3+ groups

If your study compared AI tutoring vs. traditional vs. control (k = 3 groups), you have two options:

**Option A: Request contrast-specific statistics**
- Contact authors for pairwise comparisons (AI vs. control)
- This gives you the specific effect you need

**Option B: Use partial eta-squared (η²ₚ)**

If the paper reports η²ₚ:
```
d = √(η²ₚ / (1 - η²ₚ)) × √2    (for two-group contrast)
```

Or from F directly:
```
η²ₚ = (df₁ × F) / (df₁ × F + df₂)
```

Then convert η²ₚ to d, then to g.

---

## 🟠 CHECKPOINT: F-Statistic Details

To give you the exact conversion for your study, I need:

| Information Needed | Your Study |
|--------------------|------------|
| F-value | ? |
| df numerator (df₁) | ? |
| df denominator (df₂) | ? |
| Number of groups compared | ? |
| Sample sizes per group | ? |
| Is η²ₚ reported? | ? |

**Can you provide these details for the F-statistic study?**

Once you share this, I can calculate the exact Hedges' g with variance estimate for your meta-analysis.


---

## Turn 3: 👤 USER

I've extracted the effect sizes. The Q-statistic shows significant
heterogeneity (Q = 89.34, df = 24, p < .001). I2 is 73%. Should I
use random effects model? And how do I explore the heterogeneity -
moderator analysis or meta-regression?

---

## Turn 3: 🤖 ASSISTANT

Your heterogeneity statistics indicate substantial variability that **cannot** be explained by sampling error alone. Let me address your questions directly.

---

## Random Effects Model: Yes, Definitely

### Why Random Effects is Appropriate Here

| Statistic | Your Value | Interpretation |
|-----------|------------|----------------|
| Q | 89.34 (p < .001) | Significant heterogeneity - rejects null of homogeneous effects |
| I² | 73% | **Substantial** - 73% of variance is true heterogeneity, not sampling error |
| df | 24 | 25 studies |

**I² Benchmarks (Higgins et al., 2003):**
- 25% = Low heterogeneity
- 50% = Moderate heterogeneity
- **75% = Substantial heterogeneity** ← You're here

### Fixed vs. Random Effects

| Model | Assumption | Your Situation |
|-------|------------|----------------|
| Fixed Effects | One true effect size; all studies estimate the same parameter | ❌ Violated - significant Q, high I² |
| **Random Effects** | True effects vary across studies; estimates distribution of effects | ✅ Appropriate |

Random effects model adds between-study variance (τ²) to the weighting:
```
w_i = 1 / (V_i + τ²)

where V_i = within-study variance
      τ² = between-study variance (estimated via REML, DL, or PM)
```

---

## Exploring Heterogeneity: Moderator Analysis vs. Meta-Regression

Both are valid. The choice depends on your moderator types.

### Decision Framework

| Moderator Type | Method | When to Use |
|----------------|--------|-------------|
| **Categorical** (e.g., AI type, grade level, study design) | Subgroup analysis (analog to ANOVA) | Few categories (2-4), sufficient k per subgroup |
| **Continuous** (e.g., treatment duration, age, year) | Meta-regression | Continuous predictors, or many categorical levels |
| **Mixed** (both types) | Meta-regression | Multiple predictors of different types |

### Your Likely Moderators for AI Tutoring

| Potential Moderator | Type | Method |
|---------------------|------|--------|
| AI system type (ITS, chatbot, adaptive) | Categorical | Subgroup |
| Learning domain (math, language, science) | Categorical | Subgroup |
| Grade level (elementary, secondary, higher ed) | Categorical | Subgroup |
| Treatment duration (weeks) | Continuous | Meta-regression |
| Publication year | Continuous | Meta-regression |
| Study quality (RoB score) | Continuous | Meta-regression |
| Sample size | Continuous | Meta-regression |

---

## 🟠 CHECKPOINT: Moderator Analysis Strategy

**Which approach fits your research question?**

| Option | T-Score | Description |
|--------|---------|-------------|
| **[A]** | 0.60 | **Subgroup analysis only** - Test 2-3 categorical moderators (simpler, common) |
| **[B]** | 0.45 | **Meta-regression only** - Model continuous predictors (more powerful) ⭐ |
| **[C]** | 0.35 | **Both + multivariate** - Subgroups first, then meta-regression with significant moderators |

---

## Practical Considerations

### Minimum Studies per Analysis

| Analysis | Rule of Thumb | Your Budget (k=25) |
|----------|---------------|-------------------|
| Subgroup | k ≥ 4 per subgroup | Can test ~3-4 moderators |
| Meta-regression | k ≥ 10 per covariate | Can include 2 covariates safely |

With 25 studies, avoid overfitting:
- **Subgroups**: Ensure at least 4 studies per category
- **Meta-regression**: Limit to 2-3 predictors maximum

### Recommended Estimation Methods

| Component | Recommended Method |
|-----------|-------------------|
| τ² estimation | REML (Restricted Maximum Likelihood) |
| Confidence intervals | Knapp-Hartung adjustment (more accurate than z-based) |
| Meta-regression | Mixed-effects with REML |

---

## Before Proceeding

**Please confirm:**

1. **Model choice**: [Y] to confirm random effects model?
2. **Moderator strategy**: Which option (A/B/C)?
3. **What moderators do you have coded?** (List your study-level variables)

Once confirmed, I can invoke the **E1-QuantitativeAnalysisGuide** agent to generate your analysis code (R metafor or Stata) with proper syntax for your chosen approach.


---

## Turn 4: 👤 USER

For moderator analysis, I want to test: (1) tutoring modality
(text-based vs voice-based vs multimodal), (2) subject domain
(STEM vs humanities), and (3) study quality (low vs high RoB).
How many subgroups can I test without inflating Type I error?

---

## Turn 4: 🤖 ASSISTANT

Excellent moderator selection. Let me address the multiple testing concern directly.

---

## Type I Error Inflation in Subgroup Analyses

### The Problem

Each subgroup test is an independent hypothesis test at α = .05. With multiple tests, family-wise error rate (FWER) increases:

| Number of Tests | FWER (uncorrected) | Probability of ≥1 False Positive |
|-----------------|--------------------|---------------------------------|
| 1 | 5.0% | 5.0% |
| 2 | 9.8% | 9.8% |
| **3** | **14.3%** | **14.3%** ← Your situation |
| 5 | 22.6% | 22.6% |
| 10 | 40.1% | 40.1% |

Formula: FWER = 1 - (1 - α)^k

With your 3 moderators, you have **14.3% chance** of at least one false positive if all null hypotheses are true.

---

## Your Moderator Structure

| Moderator | Levels | Comparisons | Studies Needed |
|-----------|--------|-------------|----------------|
| Tutoring modality | 3 (text, voice, multimodal) | 2 df | k ≥ 4 per level = 12 minimum |
| Subject domain | 2 (STEM, humanities) | 1 df | k ≥ 4 per level = 8 minimum |
| Study quality | 2 (low, high RoB) | 1 df | k ≥ 4 per level = 8 minimum |
| **Total** | - | **4 df** | - |

With k = 25 studies, this is feasible **if** your studies distribute reasonably across categories.

---

## Correction Strategies

### Option A: Bonferroni Correction (Conservative)

```
Adjusted α = 0.05 / number of tests
```

| Scenario | Adjusted α | Interpretation |
|----------|------------|----------------|
| 3 moderators | 0.05 / 3 = **0.017** | Report as significant only if p < .017 |
| 4 comparisons (3 + 2×1) | 0.05 / 4 = **0.0125** | More conservative |

**Limitation**: Bonferroni is overly conservative, increases Type II error (missing true effects).

### Option B: Benjamini-Hochberg FDR (Recommended) ⭐

Controls **False Discovery Rate** rather than FWER. Less conservative, more power.

Procedure:
1. Rank p-values from smallest to largest
2. Compare each p(i) to (i/m) × α
3. Largest p(i) ≤ (i/m) × α and all smaller p-values are significant

**Example with your 3 moderators:**

| Rank (i) | Moderator | p-value | BH threshold (i/3 × .05) | Significant? |
|----------|-----------|---------|--------------------------|--------------|
| 1 | Modality | .008 | .017 | ✅ Yes |
| 2 | Domain | .032 | .033 | ✅ Yes |
| 3 | Quality | .089 | .050 | ❌ No |

### Option C: Pre-specify Primary Moderator (Best Practice)

Designate **one primary moderator** (no correction needed) and treat others as exploratory.

| Classification | Moderator | α Level | Reporting |
|----------------|-----------|---------|-----------|
| **Primary** | Tutoring modality | .05 | Confirmatory |
| Exploratory | Subject domain | .05 | Interpret cautiously |
| Exploratory | Study quality | .05 | Sensitivity analysis |

This approach is methodologically defensible and commonly accepted in meta-analyses.

---

## 🟠 CHECKPOINT: Multiple Testing Strategy

**Which approach do you prefer?**

| Option | T-Score | Description |
|--------|---------|-------------|
| **[A]** | 0.55 | **Bonferroni** - Conservative, α = .017 for each test |
| **[B]** | 0.40 | **Benjamini-Hochberg FDR** - Balanced, controls false discovery rate ⭐ |
| **[C]** | 0.45 | **Pre-specified primary** - One confirmatory + exploratory moderators |
| **[D]** | 0.30 | **No correction** - Report all at α = .05 with transparent acknowledgment |

---

## Additional Recommendations

### Check Subgroup Distribution First

Before running analyses, verify adequate k per cell:

```
Modality:     Text (k=?) | Voice (k=?) | Multimodal (k=?)
Domain:       STEM (k=?) | Humanities (k=?)
Quality:      Low RoB (k=?) | High RoB (k=?)
```

**Minimum**: k ≥ 4 per subgroup (Cochrane guideline)
**Preferred**: k ≥ 10 per subgroup for stable estimates

### Report Checklist

Regardless of correction method, report:
- [ ] Number of planned moderator tests
- [ ] Correction method used (or justification for none)
- [ ] Exact p-values (not just < .05)
- [ ] Effect sizes with CIs for each subgroup
- [ ] Q-between and Q-within statistics
- [ ] Residual heterogeneity (I² within subgroups)

---

## Before Proceeding

**Please provide:**

1. **Correction strategy**: Which option (A/B/C/D)?
2. **Subgroup distribution**: How many studies in each category?

| Moderator | Level 1 (k=?) | Level 2 (k=?) | Level 3 (k=?) |
|-----------|---------------|---------------|---------------|
| Modality | Text: | Voice: | Multimodal: |
| Domain | STEM: | Humanities: | - |
| Quality | Low RoB: | High RoB: | - |

Once I have the distribution, I can assess whether all subgroup analyses are feasible or if some cells are underpowered.


---

## Turn 5: 👤 USER

Some of my studies don't report SDs, only SEs or 95% CIs. Also, two
studies report pre-post effect sizes without control groups. Should
I include these single-group studies or exclude them?

---

## Turn 5: 🤖 ASSISTANT

Two separate issues here. Let me address both.

---

## Converting SE and 95% CI to SD

This is straightforward. You can recover SD from either statistic.

### From Standard Error (SE)

```
SD = SE × √n
```

**Example**: SE = 2.5, n = 40
```
SD = 2.5 × √40 = 2.5 × 6.32 = 15.81
```

### From 95% Confidence Interval

```
SE = (Upper CI - Lower CI) / 3.92

SD = SE × √n
```

**Why 3.92?** The 95% CI spans ±1.96 SE, so the total width = 2 × 1.96 = 3.92

**Example**: 95% CI [12.5, 18.3], n = 50
```
SE = (18.3 - 12.5) / 3.92 = 5.8 / 3.92 = 1.48
SD = 1.48 × √50 = 1.48 × 7.07 = 10.46
```

### Quick Reference Table

| Reported Statistic | Formula to Get SD |
|--------------------|-------------------|
| SE | SD = SE × √n |
| 95% CI | SD = [(Upper - Lower) / 3.92] × √n |
| 99% CI | SD = [(Upper - Lower) / 5.15] × √n |
| IQR (non-normal) | SD ≈ IQR / 1.35 (approximation) |

---

## Single-Group Pre-Post Studies: Include or Exclude?

This is a more consequential methodological decision.

### The Core Problem

| Design | What It Measures | Threat |
|--------|------------------|--------|
| **Two-group (RCT/quasi)** | Effect of AI tutoring vs. comparison | Controls for maturation, history, testing effects |
| **Single-group pre-post** | Change over time | Confounded with maturation, practice effects, regression to mean |

Pre-post effect sizes from single-group studies estimate **d_ppc** (pre-post change), not **d_ig** (between-group difference). These are fundamentally different parameters.

### Effect Size Formulas Differ

**Two-group (independent groups):**
```
d_ig = (M_treatment - M_control) / SD_pooled
```

**Single-group pre-post:**
```
d_ppc = (M_post - M_pre) / SD_pre

or

d_ppc = (M_post - M_pre) / SD_pooled_within
```

**Critical issue**: d_ppc is typically **larger** than d_ig because it doesn't account for changes that would occur without intervention.

### Three Options

| Option | Approach | Consequence |
|--------|----------|-------------|
| **Exclude** | Remove single-group studies entirely | Smaller k, but cleaner estimate |
| **Include with adjustment** | Apply Morris & DeShon (2002) correction | Requires correlation between pre-post (often unreported) |
| **Sensitivity analysis** | Run both ways, compare results | Transparent, shows impact of decision |

---

## 🔴 CHECKPOINT: Single-Group Study Decision

**This affects your pooled estimate. Which approach?**

| Option | T-Score | Description | Recommendation |
|--------|---------|-------------|----------------|
| **[A]** | 0.55 | **Exclude** - Remove 2 single-group studies, analyze k=23 | Cleanest, most defensible |
| **[B]** | 0.40 | **Sensitivity analysis** - Primary analysis excludes, secondary includes ⭐ | Best of both worlds |
| **[C]** | 0.30 | **Include with moderator** - Code study design as moderator, test difference | Tests whether design affects results |
| **[D]** | 0.25 | **Include all** - Combine both designs without adjustment | Not recommended (mixes parameters) |

---

## My Recommendation: Option B (Sensitivity Analysis)

Here's why:

```
┌─────────────────────────────────────────────────────────────────┐
│                   SENSITIVITY ANALYSIS APPROACH                  │
│                                                                  │
│   Primary Analysis (k=23):                                       │
│   - Two-group studies only                                       │
│   - Report as main finding                                       │
│   - "AI tutoring effect: g = X.XX [CI]"                         │
│                                                                  │
│   Sensitivity Analysis (k=25):                                   │
│   - Include single-group studies                                 │
│   - Compare to primary                                           │
│   - "Results robust/not robust to inclusion of pre-post designs" │
│                                                                  │
│   Reporting:                                                     │
│   - If estimates similar → strengthens conclusions               │
│   - If estimates differ → discuss why, favor primary             │
└─────────────────────────────────────────────────────────────────┘
```

### If You Include Single-Group Studies

You need the **pre-post correlation (r)** to calculate correct variance:

```
Var(d_ppc) = [(2(1-r))/n] + [d²/(2n)]
```

**Do your 2 single-group studies report pre-post correlation?**

| Study | Pre-post r reported? | If not reported |
|-------|---------------------|-----------------|
| Study A | ? | Assume r = 0.50 (conservative) |
| Study B | ? | Assume r = 0.50 (conservative) |

---

## Summary of Data Transformations

| Issue | Solution |
|-------|----------|
| SE reported | SD = SE × √n |
| 95% CI reported | SD = [(Upper - Lower) / 3.92] × √n |
| Single-group pre-post | Sensitivity analysis: primary excludes, secondary includes |

---

## Before Proceeding

**Please confirm:**

1. **SE/CI conversion**: [Y] Clear on how to recover SDs?
2. **Single-group decision**: Which option (A/B/C/D)?
3. **Pre-post correlation**: Do your 2 single-group studies report r?

Once confirmed, I can provide the complete data preparation checklist and R/Stata code for your analysis.


---

## Turn 6: 👤 USER

This is very helpful. I'll use Hedges' g for all effect sizes, random
effects model with REML estimation, and run moderator analysis for the
3 a priori moderators with Bonferroni correction. I'll also conduct
sensitivity analysis excluding single-group studies. Please summarize
my analysis plan and suggest R packages to use.

---

## Turn 6: 🤖 ASSISTANT

Excellent decisions. Here's your complete analysis plan summary and R implementation guide.

---

## Meta-Analysis Plan Summary

### Study Characteristics

| Parameter | Your Specification |
|-----------|-------------------|
| Total studies | k = 25 |
| Primary studies (two-group) | k = 23 |
| Sensitivity inclusion | k = 25 (adds 2 single-group pre-post) |
| Effect size metric | Hedges' g (bias-corrected) |
| Research question | Effectiveness of AI tutoring on student learning outcomes |

### Statistical Decisions

| Component | Decision | Rationale |
|-----------|----------|-----------|
| **Effect size** | Hedges' g | Corrects small-sample bias (n < 20 in some studies) |
| **Model** | Random effects | Significant heterogeneity (Q = 89.34, p < .001; I² = 73%) |
| **τ² estimator** | REML | Gold standard, less biased than DerSimonian-Laird |
| **Confidence intervals** | Knapp-Hartung | More accurate than z-based for random effects |
| **Multiple testing** | Bonferroni (α = .017) | Controls FWER for 3 moderator tests |

### Moderator Analyses

| Moderator | Type | Levels | Adjusted α |
|-----------|------|--------|------------|
| Tutoring modality | Categorical | Text / Voice / Multimodal | .017 |
| Subject domain | Categorical | STEM / Humanities | .017 |
| Study quality | Categorical | Low RoB / High RoB | .017 |

### Sensitivity Analyses

| Analysis | Description |
|----------|-------------|
| **Primary** | Two-group controlled studies only (k = 23) |
| **Sensitivity 1** | Include single-group pre-post studies (k = 25) |
| **Sensitivity 2** | Exclude high RoB studies (k = ?) |
| **Sensitivity 3** | Leave-one-out analysis (influence diagnostics) |

---

## R Packages

### Core Packages

| Package | Purpose | Installation |
|---------|---------|--------------|
| **metafor** | Primary meta-analysis engine | `install.packages("metafor")` |
| **dplyr** | Data manipulation | `install.packages("dplyr")` |
| **ggplot2** | Visualization | `install.packages("ggplot2")` |

### Supplementary Packages

| Package | Purpose | Installation |
|---------|---------|--------------|
| **esc** | Effect size conversion (d, r, F → g) | `install.packages("esc")` |
| **meta** | Alternative forest plots | `install.packages("meta")` |
| **metaviz** | Publication bias visualization | `install.packages("metaviz")` |
| **clubSandwich** | Robust variance estimation | `install.packages("clubSandwich")` |
| **dmetar** | Helper functions for meta-analysis | `devtools::install_github("MathiasHarrer/dmetar")` |

---

## R Code Template

### 1. Setup and Data Preparation

```r
# Load packages
library(metafor)
library(esc)
library(dplyr)
library(ggplot2)

# Load your data
dat <- read.csv("meta_analysis_data.csv")

# Data structure should include:
# study_id, author, year, n1, n2, g, g_var, 
# modality, domain, rob_quality, design_type
```

### 2. Effect Size Conversions (if needed)

```r
# Cohen's d to Hedges' g
convert_d_to_g <- function(d, n1, n2) {
  df <- n1 + n2 - 2
  j <- 1 - (3 / (4 * df - 1))
  g <- d * j
  return(g)
}

# Variance of Hedges' g
var_g <- function(g, n1, n2) {
  df <- n1 + n2 - 2
  j <- 1 - (3 / (4 * df - 1))
  v <- ((n1 + n2) / (n1 * n2) + (g^2 / (2 * (n1 + n2)))) * j^2
  return(v)
}

# Correlation r to Hedges' g (using esc package)
esc_r_to_g <- function(r, n) {
  result <- esc_rpb(r = r, totaln = n, es.type = "g")
  return(list(g = result$es, var = result$var))
}

# F-statistic to Hedges' g (two-group ANOVA)
f_to_g <- function(f, n1, n2) {
  d <- sqrt(f * (n1 + n2) / (n1 * n2))
  g <- convert_d_to_g(d, n1, n2)
  v <- var_g(g, n1, n2)
  return(list(g = g, var = v))
}

# SE to SD
se_to_sd <- function(se, n) {
  sd <- se * sqrt(n)
  return(sd)
}

# 95% CI to SD
ci_to_sd <- function(lower, upper, n) {
  se <- (upper - lower) / 3.92
  sd <- se * sqrt(n)
  return(sd)
}
```

### 3. Primary Analysis (Random Effects)

```r
# Subset to two-group studies only
dat_primary <- dat %>% filter(design_type == "two_group")

# Random effects model with REML
res_primary <- rma(
  yi = g,
  vi = g_var,
  data = dat_primary,
  method = "REML",
  test = "knha"  # Knapp-Hartung adjustment
)

# View results
summary(res_primary)

# Key outputs:
# - Pooled effect (g) with 95% CI
# - τ² (between-study variance)
# - I² (heterogeneity percentage)
# - Q-statistic and p-value
```

### 4. Heterogeneity Assessment

```r
# Heterogeneity statistics
cat("Q =", res_primary$QE, ", df =", res_primary$k - 1, 
    ", p =", res_primary$QEp, "\n")
cat("I² =", round(res_primary$I2, 1), "%\n")
cat("τ² =", round(res_primary$tau2, 4), "\n")
cat("τ =", round(sqrt(res_primary$tau2), 4), "\n")

# Prediction interval (range of true effects)
predict(res_primary)
```

### 5. Moderator Analyses (Subgroup)

```r
# Bonferroni-adjusted α
alpha_adjusted <- 0.05 / 3  # = 0.017

# Moderator 1: Tutoring Modality
res_modality <- rma(
  yi = g, vi = g_var,
  mods = ~ factor(modality) - 1,  # -1 removes intercept, gives subgroup means
  data = dat_primary,
  method = "REML",
  test = "knha"
)
summary(res_modality)

# Test for subgroup differences (Q-between)
anova(res_modality, btt = 1:3)  # Omnibus test

# Moderator 2: Subject Domain
res_domain <- rma(
  yi = g, vi = g_var,
  mods = ~ factor(domain) - 1,
  data = dat_primary,
  method = "REML",
  test = "knha"
)
summary(res_domain)

# Moderator 3: Study Quality (RoB)
res_quality <- rma(
  yi = g, vi = g_var,
  mods = ~ factor(rob_quality) - 1,
  data = dat_primary,
  method = "REML",
  test = "knha"
)
summary(res_quality)

# Compile moderator results
moderator_results <- data.frame(
  Moderator = c("Modality", "Domain", "Quality"),
  Q_between = c(
    anova(res_modality)$QM,
    anova(res_domain)$QM,
    anova(res_quality)$QM
  ),
  p_value = c(
    anova(res_modality)$QMp,
    anova(res_domain)$QMp,
    anova(res_quality)$QMp
  ),
  Significant = c(
    anova(res_modality)$QMp < alpha_adjusted,
    anova(res_domain)$QMp < alpha_adjusted,
    anova(res_quality)$QMp < alpha_adjusted
  )
)
print(moderator_results)
```

### 6. Sensitivity Analyses

```r
# Sensitivity 1: Include single-group studies
res_sensitivity1 <- rma(
  yi = g, vi = g_var,
  data = dat,  # Full dataset
  method = "REML",
  test = "knha"
)
summary(res_sensitivity1)

# Compare primary vs sensitivity
cat("Primary (k=23): g =", round(res_primary$b, 3), 
    "[", round(res_primary$ci.lb, 3), ",", 
    round(res_primary$ci.ub, 3), "]\n")
cat("Sensitivity (k=25): g =", round(res_sensitivity1$b, 3),
    "[", round(res_sensitivity1$ci.lb, 3), ",",
    round(res_sensitivity1$ci.ub, 3), "]\n")

# Sensitivity 2: Exclude high RoB studies
dat_low_rob <- dat_primary %>% filter(rob_quality == "low")
res_sensitivity2 <- rma(
  yi = g, vi = g_var,
  data = dat_low_rob,
  method = "REML",
  test = "knha"
)

# Sensitivity 3: Leave-one-out analysis
res_loo <- leave1out(res_primary)
print(res_loo)

# Identify influential studies
influence_stats <- influence(res_primary)
plot(influence_stats)
```

### 7. Publication Bias Assessment

```r
# Funnel plot
funnel(res_primary, main = "Funnel Plot")

# Egger's regression test
regtest(res_primary, model = "lm")

# Trim-and-fill
res_tf <- trimfill(res_primary)
summary(res_tf)
funnel(res_tf)

# Fail-safe N (Rosenthal)
fsn(yi = g, vi = g_var, data = dat_primary, type = "Rosenthal")

# P-curve (requires significant studies only)
# Use dmetar package
library(dmetar)
pcurve(res_primary)
```

### 8. Forest Plot

```r
# Basic forest plot
forest(res_primary, 
       slab = paste(dat_primary$author, dat_primary$year),
       header = "Author(s) and Year",
       xlab = "Hedges' g",
       mlab = "Random Effects Model")

# Enhanced forest plot with subgroups
forest(res_primary,
       order = dat_primary$modality,
       rows = c(3:8, 13:18, 23:28),
       ylim = c(1, 32),
       header = TRUE)

# Add subgroup labels
text(-4, c(9, 19, 29), pos = 4, font = 2,
     c("Text-based", "Voice-based", "Multimodal"))
```

---

## Reporting Checklist (PRISMA-MA)

| Section | Required Elements | ✓ |
|---------|-------------------|---|
| **Methods** | | |
| | Effect size metric (Hedges' g) | ☐ |
| | Model specification (random effects, REML) | ☐ |
| | Heterogeneity assessment (Q, I², τ²) | ☐ |
| | Moderator analysis plan (a priori, Bonferroni) | ☐ |
| | Sensitivity analyses planned | ☐ |
| | Software and packages (R metafor) | ☐ |
| **Results** | | |
| | Pooled effect with 95% CI | ☐ |
| | Prediction interval | ☐ |
| | Heterogeneity statistics | ☐ |
| | Moderator results (Q-between, p-values) | ☐ |
| | Sensitivity analysis comparison | ☐ |
| | Publication bias assessment | ☐ |
| | Forest plot | ☐ |
| | Funnel plot | ☐ |

---

## 🟢 Analysis Plan Complete

**Your finalized plan:**

| Component | Specification |
|-----------|---------------|
| Effect size | Hedges' g |
| Model | Random effects (REML, Knapp-Hartung) |
| Primary analysis | k = 23 (two-group studies) |
| Moderators | 3 categorical (Bonferroni α = .017) |
| Sensitivity | Include single-group (k = 25), exclude high RoB, leave-one-out |
| Publication bias | Funnel, Egger's, trim-and-fill, fail-safe N |
| Software | R metafor package |

---

**Ready to proceed with data analysis?**

If you'd like, I can:
1. Generate a complete R script file for your analysis
2. Help interpret specific results once you run the code
3. Review your forest plot or funnel plot outputs
4. Assist with writing the Methods section for your manuscript

What would be most helpful next?


---

