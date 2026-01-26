---
name: analysis-code-generator
version: 4.1.0
description: |
  E4-Enhanced Analysis Code Generator - Prevents Mode Collapse with diverse implementation options
  Light VS applied: Modal code pattern awareness + alternative implementation presentation
  Use when: generating analysis code, creating reproducible scripts, automating analysis
  Triggers: R code, Python code, SPSS, Stata, NVivo, ATLAS.ti, MAXQDA, qualitative analysis code, analysis script, code generation
upgrade_level: LIGHT
tier: Support
v3_integration:
  dynamic_t_score: false
  creativity_modules: []
  checkpoints:
    - CP-INIT-001
    - CP-VS-003
---

# E4-Analysis Code Generator

**Agent ID**: 11 (E4 in Social Science Research Agent System)
**Category**: E - Publication & Communication (formerly C - Methodology & Analysis)
**VS Level**: Light (Modal awareness)
**Tier**: Support
**Icon**: 💻

## Overview

Automatically generates reproducible code for quantitative and **qualitative** statistical analysis.
Supports multiple languages including R, Python, SPSS, Stata, and **CAQDAS platforms** (NVivo, ATLAS.ti, MAXQDA) with detailed comments.

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
- **When qualitative analysis automation is needed (NVivo, ATLAS.ti, MAXQDA)**
- **When inter-rater reliability calculation is required**
- **When thematic analysis or content analysis code templates are needed**

## Core Functions

1. **Multi-language Support**
   - R (tidyverse, base R)
   - Python (pandas, scipy, statsmodels)
   - SPSS syntax
   - Stata do files
   - **NVivo project setup and query scripts**
   - **ATLAS.ti code-document tables and network scripts**
   - **MAXQDA code system and mixed methods displays**

2. **Package Recommendations**
   - Optimal packages by analysis type
   - Installation commands included
   - Version compatibility consideration
   - **Qualitative analysis R/Python package recommendations**

3. **Reproducibility Guarantee**
   - Includes set.seed()
   - Version information recording
   - Environment settings specification
   - **Inter-rater reliability tracking for qualitative coding**

4. **Detailed Comments**
   - Each code block explanation
   - Korean/English comment support
   - Analysis logic description
   - **CAQDAS workflow documentation**

5. **Visualization Included**
   - Diagnostic plots
   - Results visualization
   - APA style graphs
   - **Word clouds, co-occurrence networks for qualitative data**

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
| **Qualitative text analysis** | nltk, spacy, textblob |
| **Thematic analysis** | quanteda, tidytext |
| **Inter-rater reliability** | sklearn.metrics (cohen_kappa_score) |

### CAQDAS Support

#### NVivo
| Feature | Capability |
|---------|-----------|
| Project setup | Automated project structure creation |
| Auto-coding rules | Pattern-based coding rule generation |
| Query syntax | Matrix coding queries, crosstab generation |
| Export formats | xlsx, docx, spss |

**Example NVivo Query Syntax Generation:**
```vb
' Matrix coding query for theme co-occurrence
Query.MatrixCoding(
  Rows: Nodes["Themes\AI Benefits"],
  Columns: Nodes["Themes\Challenges"],
  Scope: Documents["Interviews\*"]
)
```

#### ATLAS.ti
| Feature | Capability |
|---------|-----------|
| Code-document table | Automated code frequency tables |
| Network view scripts | Co-occurrence network generation |
| Query tool syntax | Boolean query automation |
| Quotation export | Systematic quotation extraction |

**Example ATLAS.ti Query:**
```
Code "AI Adoption" AND Code "Resistance"
WITHIN QUOTATION DISTANCE 50
```

#### MAXQDA
| Feature | Capability |
|---------|-----------|
| Code system setup | Hierarchical code structure generation |
| Mixed methods displays | Joint display table automation |
| Document portrait | Visual summary generation |
| Code relations browser | Relationship mapping |

**Example MAXQDA Code System:**
```
Themes
├── AI Benefits
│   ├── Efficiency
│   └── Accuracy
└── Challenges
    ├── Technical barriers
    └── User resistance
```

## Input Requirements

```yaml
Required:
  - analysis_method: "Statistical analysis to perform (quantitative or qualitative)"
  - language: "R, Python, SPSS, Stata, NVivo, ATLAS.ti, MAXQDA"
  - variable_info: "Variable names, types (for quant) OR coding scheme (for qual)"

Optional:
  - data_file: "File path/format"
  - special_requirements: "APA format, Korean support, inter-rater reliability, etc."
  - caqdas_version: "Software version for compatibility"
  - coding_method: "Thematic analysis, content analysis, grounded theory"
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

## Qualitative Analysis Code Templates

### Thematic Analysis (R)

```r
# ============================================
# Thematic Analysis with R
# Packages: tm, quanteda, tidytext
# ============================================

library(tidyverse)
library(tm)
library(quanteda)
library(tidytext)

# Load qualitative data
interviews <- read_csv("interviews.csv")

# Create corpus
corpus <- corpus(interviews, text_field = "transcript")

# Tokenize
tokens <- tokens(corpus,
                remove_punct = TRUE,
                remove_numbers = TRUE,
                remove_symbols = TRUE)

# Create document-feature matrix
dfm <- dfm(tokens) %>%
  dfm_remove(stopwords("english"))

# Word frequency analysis
word_freq <- textstat_frequency(dfm, n = 50)

# Visualize top words
ggplot(word_freq[1:20,], aes(x = reorder(feature, frequency), y = frequency)) +
  geom_col() +
  coord_flip() +
  labs(title = "Top 20 Most Frequent Words",
       x = "Word", y = "Frequency") +
  theme_minimal()

# Co-occurrence network
fcm <- fcm(dfm, context = "window", window = 5)
textplot_network(fcm, min_freq = 10, edge_alpha = 0.5)
```

### Thematic Analysis (Python)

```python
# ============================================
# Thematic Analysis with Python
# Packages: nltk, spacy, textblob
# ============================================

import pandas as pd
import nltk
from nltk.corpus import stopwords
from collections import Counter
import spacy
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load data
df = pd.read_csv("interviews.csv")

# Preprocess text
stop_words = set(stopwords.words('english'))

def preprocess(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc
             if not token.is_stop and not token.is_punct]
    return tokens

df['tokens'] = df['transcript'].apply(preprocess)

# Word frequency
all_words = [word for tokens in df['tokens'] for word in tokens]
word_freq = Counter(all_words)
top_20 = word_freq.most_common(20)

# Visualize
words, counts = zip(*top_20)
plt.figure(figsize=(12, 6))
plt.barh(words, counts)
plt.xlabel('Frequency')
plt.title('Top 20 Most Frequent Words')
plt.tight_layout()
plt.show()

# Word cloud
wordcloud = WordCloud(width=800, height=400,
                     background_color='white').generate(' '.join(all_words))
plt.figure(figsize=(15, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
```

### Content Analysis with Inter-Rater Reliability (R)

```r
# ============================================
# Content Analysis: Inter-Rater Reliability
# Package: irr
# ============================================

library(irr)

# Load coding data (2 raters)
# Format: Each row = document, each column = rater's code
coding_data <- read_csv("coding_ratings.csv")

# Cohen's Kappa (2 raters, nominal categories)
kappa_result <- kappa2(coding_data[, c("rater1", "rater2")])
print(kappa_result)
# Interpretation:
# < 0.00: Poor agreement
# 0.00-0.20: Slight agreement
# 0.21-0.40: Fair agreement
# 0.41-0.60: Moderate agreement
# 0.61-0.80: Substantial agreement
# 0.81-1.00: Almost perfect agreement

# Krippendorff's Alpha (multiple raters, any measurement level)
# Data format: rows = raters, columns = documents
kripp_result <- kripp.alpha(t(coding_data[, -1]), method = "nominal")
print(kripp_result)

# Percent Agreement
agree(coding_data[, c("rater1", "rater2")])
```

### Content Analysis with Inter-Rater Reliability (Python)

```python
# ============================================
# Content Analysis: Inter-Rater Reliability
# Package: sklearn.metrics
# ============================================

import pandas as pd
from sklearn.metrics import cohen_kappa_score, confusion_matrix
import numpy as np

# Load coding data
df = pd.read_csv("coding_ratings.csv")

# Cohen's Kappa (2 raters)
kappa = cohen_kappa_score(df['rater1'], df['rater2'])
print(f"Cohen's Kappa: {kappa:.3f}")

# Percent Agreement
agreement = (df['rater1'] == df['rater2']).sum() / len(df)
print(f"Percent Agreement: {agreement:.1%}")

# Confusion matrix
cm = confusion_matrix(df['rater1'], df['rater2'])
print("Confusion Matrix:")
print(cm)

# Krippendorff's Alpha (requires simpledorff package)
# pip install simpledorff
import simpledorff

# Format: rows = documents, columns = raters
reliability_data = df[['rater1', 'rater2']].values.T
alpha = simpledorff.calculate_krippendorffs_alpha_for_df(
    pd.DataFrame(reliability_data)
)
print(f"Krippendorff's Alpha: {alpha:.3f}")
```

### NVivo Automation Script Template

```python
# ============================================
# NVivo Project Setup Automation
# Requires: NVivo API or manual import
# ============================================

import pandas as pd

# Generate NVivo classification sheet
nvivo_setup = {
    'Name': ['Interview_01', 'Interview_02', 'Interview_03'],
    'Type': ['Interview', 'Interview', 'Interview'],
    'Participant_ID': ['P001', 'P002', 'P003'],
    'Gender': ['Female', 'Male', 'Female'],
    'Years_Experience': [5, 10, 3]
}

df = pd.DataFrame(nvivo_setup)
df.to_excel('nvivo_classification_import.xlsx', index=False)

# Generate auto-coding rules template
autocoding_rules = """
# NVivo Auto-Coding Rules

## Rule 1: Keyword-based coding
Node: Themes\\AI Benefits
Keywords: benefit, advantage, positive, improve, enhance
Context: NEAR (within 10 words)

## Rule 2: Pattern-based coding
Node: Themes\\Challenges
Pattern: difficult*, challenge*, barrier*, obstacle*

## Rule 3: Sentiment-based coding
Node: Sentiment\\Positive
Criteria: Sentences containing: love, great, excellent, wonderful
Exclude: NOT, but, however (within 5 words)
"""

with open('nvivo_autocoding_rules.txt', 'w') as f:
    f.write(autocoding_rules)

print("NVivo project setup files created!")
```

### ATLAS.ti Code-Document Table Generator

```python
# ============================================
# ATLAS.ti Code-Document Frequency Table
# ============================================

import pandas as pd

# Simulated coding data
# Format: document_id, code, quotation_count
atlas_data = {
    'Document': ['Interview_01', 'Interview_01', 'Interview_02',
                'Interview_02', 'Interview_03', 'Interview_03'],
    'Code': ['AI_Benefits', 'Challenges', 'AI_Benefits',
            'User_Resistance', 'Efficiency', 'Challenges'],
    'Count': [5, 3, 7, 2, 4, 6]
}

df = pd.DataFrame(atlas_data)

# Pivot to code-document matrix
code_doc_matrix = df.pivot_table(
    values='Count',
    index='Document',
    columns='Code',
    fill_value=0
)

print("Code-Document Frequency Matrix:")
print(code_doc_matrix)

# Export for ATLAS.ti import
code_doc_matrix.to_excel('atlas_code_document_matrix.xlsx')

# Co-occurrence calculation
from itertools import combinations

codes_per_doc = df.groupby('Document')['Code'].apply(list)
cooccurrence = {}

for doc, codes in codes_per_doc.items():
    for code1, code2 in combinations(set(codes), 2):
        pair = tuple(sorted([code1, code2]))
        cooccurrence[pair] = cooccurrence.get(pair, 0) + 1

print("\nCode Co-occurrence:")
for pair, count in sorted(cooccurrence.items(), key=lambda x: -x[1]):
    print(f"{pair[0]} <-> {pair[1]}: {count}")
```

## Qualitative Analysis Summary Reference

### R Packages for Qualitative Analysis
| Package | Purpose | Key Functions |
|---------|---------|---------------|
| **tm** | Text mining | `Corpus()`, `tm_map()`, `DocumentTermMatrix()` |
| **quanteda** | Quantitative text analysis | `corpus()`, `tokens()`, `dfm()`, `textstat_frequency()` |
| **tidytext** | Tidy text mining | `unnest_tokens()`, `bind_tf_idf()` |
| **irr** | Inter-rater reliability | `kappa2()`, `kripp.alpha()`, `agree()` |

### Python Packages for Qualitative Analysis
| Package | Purpose | Key Functions |
|---------|---------|---------------|
| **nltk** | Natural language toolkit | `word_tokenize()`, `stopwords`, `FreqDist()` |
| **spacy** | NLP | `nlp()`, `.lemma_`, `.pos_` |
| **textblob** | Text processing | `TextBlob()`, `.sentiment`, `.noun_phrases` |
| **sklearn.metrics** | Inter-rater reliability | `cohen_kappa_score()`, `confusion_matrix()` |
| **wordcloud** | Word cloud generation | `WordCloud().generate()` |

### CAQDAS Export Formats

| Software | Export Formats | Use Case |
|----------|---------------|----------|
| **NVivo** | `.xlsx`, `.docx`, `.spss` | Code frequency tables, crosstabs |
| **ATLAS.ti** | `.xlsx`, `.txt`, `.graphml` | Code-document tables, network data |
| **MAXQDA** | `.xlsx`, `.txt`, `.csv` | Joint displays, code matrices |

### Inter-Rater Reliability Thresholds

| Coefficient | Poor | Fair | Moderate | Substantial | Almost Perfect |
|-------------|------|------|----------|-------------|----------------|
| **Cohen's Kappa** | < 0.00 | 0.00-0.20 | 0.21-0.60 | 0.61-0.80 | 0.81-1.00 |
| **Krippendorff's α** | < 0.667 | 0.667-0.75 | 0.75-0.85 | 0.85-0.95 | > 0.95 |

**Recommended minimum**: Kappa > 0.60 or α > 0.75 for publication

## Related Agents

- **10-statistical-analysis-guide**: Deciding analysis method (quantitative and qualitative)
- **12-sensitivity-analysis-designer**: Sensitivity analysis code
- **15-reproducibility-auditor**: Reproducibility verification
- **E2-Abstract Writer**: Methodology section for qualitative studies
- **E3-Visualization Expert**: Word clouds, thematic maps for presentations

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
