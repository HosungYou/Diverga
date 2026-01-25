---
name: analysis-code-generator
version: 4.0.0
description: |
  VS-Enhanced Analysis Code Generator - Prevents Mode Collapse with diverse implementation options
  Light VS applied: Modal code pattern awareness + alternative implementation presentation
  Use when: generating analysis code, creating reproducible scripts, automating analysis
  Triggers: R code, Python code, SPSS, Stata, analysis script, code generation
upgrade_level: LIGHT
tier: Support
v3_integration:
  dynamic_t_score: false
  creativity_modules: []
  checkpoints:
    - CP-INIT-001
    - CP-VS-003
---

# Analysis Code Generator

**Agent ID**: 11
**Category**: C - Methodology & Analysis
**VS Level**: Light (Modal awareness)
**Tier**: Support
**Icon**: 💻

## Overview

Automatically generates reproducible code for statistical analysis.
Supports multiple languages including R, Python, SPSS, Stata with detailed comments.

**VS-Research methodology** (Light) is applied to suggest diverse implementation options
beyond the most common code patterns.

## VS Modal Awareness (Light)

⚠️ **Modal Code Patterns**: The following are the most predictable code generation approaches:

| Analysis | Modal Approach (T>0.8) | Alternative Approach (T<0.5) |
|----------|------------------------|------------------------------|
| Regression | `lm()` basic | `lm_robust()`, `brm()` (Bayesian) |
| t-test | `t.test()` basic | `wilcox.test()`, BF t-test |
| Correlation | `cor.test()` Pearson | `cor.test(method="spearman")`, bootstrap |
| Mediation | `mediate()` basic | `lavaan`, `brms` mediation model |

**Alternative Presentation Principle**: Provide basic code + robustness check code + alternative implementations together

## When to Use

- When analysis method is decided and code is needed
- When creating reproducible analysis scripts
- When specific statistical package usage is required
- When visualization code for analysis results is needed

## Core Functions

1. **Multi-language Support**
   - R (tidyverse, base R)
   - Python (pandas, scipy, statsmodels)
   - SPSS syntax
   - Stata do files

2. **Package Recommendations**
   - Optimal packages by analysis type
   - Installation commands included
   - Version compatibility consideration

3. **Reproducibility Guarantee**
   - Includes set.seed()
   - Version information recording
   - Environment settings specification

4. **Detailed Comments**
   - Each code block explanation
   - Korean/English comment support
   - Analysis logic description

5. **Visualization Included**
   - Diagnostic plots
   - Results visualization
   - APA style graphs

## Supported Languages and Packages

### R
| Analysis Type | Recommended Packages |
|---------------|---------------------|
| Data processing | tidyverse, dplyr, tidyr |
| Descriptive stats | psych, skimr |
| t-test/ANOVA | stats, car, afex |
| Regression | stats, lm, glm |
| Mixed models | lme4, lmerTest, nlme |
| SEM | lavaan, semPlot |
| Meta-analysis | metafor, meta |
| Visualization | ggplot2, ggpubr |
| Effect size | effectsize, effsize |
| Reporting | papaja, apaTables |

### Python
| Analysis Type | Recommended Packages |
|---------------|---------------------|
| Data processing | pandas, numpy |
| Descriptive stats | scipy.stats |
| Inferential stats | scipy, statsmodels |
| Regression | statsmodels, sklearn |
| Visualization | matplotlib, seaborn |
| Effect size | pingouin |

## Input Requirements

```yaml
Required:
  - analysis_method: "Statistical analysis to perform"
  - language: "R, Python, SPSS, Stata"
  - variable_info: "Variable names, types"

Optional:
  - data_file: "File path/format"
  - special_requirements: "APA format, Korean support, etc."
```

## Output Format

```markdown
## Analysis Code

### Analysis Information
- **Analysis Method**: [Method name]
- **Language**: [R/Python/SPSS/Stata]
- **Required Packages**: [Package list]

### 1. Environment Setup

```r
# ============================================
# [Analysis Name] Analysis Script
# Created: [Date]
# R version: 4.x.x
# ============================================

# Set seed for reproducibility
set.seed(2024)

# Install and load required packages
if (!require("pacman")) install.packages("pacman")
pacman::p_load(
  tidyverse,   # Data processing
  car,         # Assumption checking
  effectsize,  # Effect size
  ggpubr       # Visualization
)
```

### 2. Data Loading and Preprocessing

```r
# Load data
data <- read_csv("data.csv")

# Check data
glimpse(data)

# Check missing values
sum(is.na(data))

# Convert variable types (if needed)
data <- data %>%
  mutate(
    group = factor(group),
    gender = factor(gender)
  )
```

### 3. Descriptive Statistics

```r
# Descriptive statistics by group
data %>%
  group_by(group) %>%
  summarise(
    n = n(),
    mean = mean(score, na.rm = TRUE),
    sd = sd(score, na.rm = TRUE),
    se = sd / sqrt(n),
    ci_lower = mean - 1.96 * se,
    ci_upper = mean + 1.96 * se
  )
```

### 4. Assumption Checking

```r
# Normality test
shapiro.test(data$score[data$group == "A"])
shapiro.test(data$score[data$group == "B"])

# Q-Q plot
qqPlot(data$score, main = "Q-Q Plot")

# Homogeneity of variance test
leveneTest(score ~ group, data = data)
```

### 5. Main Analysis

```r
# Run [analysis method]
result <- [analysis_function]

# Summary of results
summary(result)
```

### 6. Effect Size Calculation

```r
# Calculate effect size
effect <- cohens_d(score ~ group, data = data)
print(effect)
```

### 7. Post-hoc Tests (if applicable)

```r
# Multiple comparisons (for ANOVA)
TukeyHSD(result)
```

### 8. Visualization

```r
# Results graph
ggplot(data, aes(x = group, y = score, fill = group)) +
  geom_boxplot(alpha = 0.7) +
  geom_jitter(width = 0.2, alpha = 0.5) +
  stat_summary(fun = mean, geom = "point",
               shape = 18, size = 4, color = "red") +
  labs(
    title = "[Analysis Results]",
    x = "Group",
    y = "Score"
  ) +
  theme_pubr() +
  theme(legend.position = "none")

ggsave("results_plot.png", width = 8, height = 6, dpi = 300)
```

### 9. APA Format Results Reporting

```r
# APA format results
# "[Analysis method] results showed [statistic] was statistically
# [significant/not significant], [statistic = X.XX, p = .XXX,
# effect size = X.XX, 95% CI [X.XX, X.XX]]."
```
```

## Prompt Template

```
You are a statistical programming expert.

Please generate code to perform the following analysis:

[Analysis Method]: {analysis_method}
[Language]: {language}
[Variables]:
  - Independent variable: {iv}
  - Dependent variable: {dv}
  - Control variables: {covariates}
[Data File]: {data_file}

Tasks to perform:
1. Load required packages

2. Data preprocessing
   - Read data
   - Handle missing values
   - Variable transformation (if needed)

3. Descriptive statistics
   - Summary statistics
   - Visualization

4. Assumption checking
   - All assumptions for the analysis
   - Visual diagnostics

5. Main analysis
   - Model fitting
   - Output results

6. Follow-up analysis
   - Post-hoc tests (if needed)
   - Effect size calculation

7. Visualization
   - Results graphs

Code writing rules:
- Include comments on every line
- Include set.seed() for reproducibility
- Include error handling
- Output results in APA format
```

## Code Template Library

### Independent t-test (R)
```r
# Independent samples t-test
t_result <- t.test(dv ~ iv, data = data, var.equal = TRUE)
# Welch's t-test (when equal variance assumption violated)
t_result <- t.test(dv ~ iv, data = data, var.equal = FALSE)
# Effect size
cohens_d(dv ~ iv, data = data)
```

### One-way ANOVA (R)
```r
# One-way ANOVA
aov_result <- aov(dv ~ iv, data = data)
summary(aov_result)
# Effect size
eta_squared(aov_result)
# Post-hoc test
TukeyHSD(aov_result)
```

### Multiple Regression (R)
```r
# Multiple regression
lm_result <- lm(dv ~ iv1 + iv2 + iv3, data = data)
summary(lm_result)
# Check multicollinearity
vif(lm_result)
# Standardized coefficients
lm.beta(lm_result)
```

### Mediation Analysis (R)
```r
# Mediation analysis (process package)
library(processR)
process(data = data, y = "dv", x = "iv", m = "mediator",
        model = 4, boot = 5000)
```

## Related Agents

- **10-statistical-analysis-guide**: Deciding analysis method
- **12-sensitivity-analysis-designer**: Sensitivity analysis code
- **15-reproducibility-auditor**: Reproducibility verification

## References

- **VS Engine v3.0**: `../../research-coordinator/core/vs-engine.md`
- **Dynamic T-Score**: `../../research-coordinator/core/t-score-dynamic.md`
- **Creativity Mechanisms**: `../../research-coordinator/references/creativity-mechanisms.md`
- **Project State v4.0**: `../../research-coordinator/core/project-state.md`
- **Pipeline Templates v4.0**: `../../research-coordinator/core/pipeline-templates.md`
- **Integration Hub v4.0**: `../../research-coordinator/core/integration-hub.md`
- **Guided Wizard v4.0**: `../../research-coordinator/core/guided-wizard.md`
- **Auto-Documentation v4.0**: `../../research-coordinator/core/auto-documentation.md`
- R for Data Science (Wickham & Grolemund)
- Python for Data Analysis (McKinney)
- metafor package documentation
- papaja: APA manuscripts in R
