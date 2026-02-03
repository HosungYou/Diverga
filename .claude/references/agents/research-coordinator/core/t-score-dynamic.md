---
name: t-score-dynamic
description: |
  Dynamic T-Score calculation system with API integration.
  Provides real-time typicality scoring based on recent usage.
version: "3.0.0"
---

# Dynamic T-Score System v3.0

## Overview

Replaces static T-Score tables with dynamic calculation based on:
- Real-time API queries (Semantic Scholar, OpenAlex)
- Recency-weighted usage frequency
- Domain-specific adjustments
- Trend detection (rising/falling popularity)

## T-Score Calculation Formula

```
dynamic_t_score = base_score + recency_modifier + domain_modifier + trend_modifier

Where:
  base_score: Static baseline from reference tables (0.0-1.0)
  recency_modifier: Recent 3-year usage adjustment (-0.15 to +0.15)
  domain_modifier: Domain-specific weight (-0.1 to +0.1)
  trend_modifier: Popularity trend adjustment (-0.1 to +0.1)
```

## Modes

### 1. Static Mode (Default Fallback)

Uses pre-defined T-Score tables from `references/VS-Research-Framework.md`.

```yaml
static_tables:
  theoretical_frameworks:
    TAM: 0.95
    SCT: 0.90
    UTAUT: 0.88
    SDT: 0.70
    CLT: 0.65
    # ... more in reference file

  statistical_methods:
    t-test: 0.92
    ANOVA: 0.88
    OLS_regression: 0.85
    HLM: 0.65
    SEM: 0.60
    Bayesian: 0.40
    # ... more in reference file
```

### 2. Dynamic Mode (API-Based)

Queries external APIs to calculate real-time T-Score.

```yaml
api_configuration:
  primary: semantic_scholar
  fallback: openalex
  cache_duration: 24h
  timeout: 5s

  semantic_scholar:
    endpoint: "https://api.semanticscholar.org/graph/v1/paper/search"
    fields: ["title", "year", "citationCount"]
    rate_limit: 100/minute

  openalex:
    endpoint: "https://api.openalex.org/works"
    mailto: "research-coordinator@example.com"
    rate_limit: 10/second
```

**Query Template:**

```
Search: "{theory_name}" AND "{domain}" AND year:[{current_year-3} TO {current_year}]
Count: Total papers using this theory in domain
```

**Recency Modifier Calculation:**

```python
def calculate_recency_modifier(theory, domain):
    """
    Calculate recency modifier based on recent usage.

    Returns:
      -0.15 to +0.15 adjustment to base T-Score
    """
    recent_count = query_api(theory, domain, years=3)
    historical_avg = get_historical_average(theory, domain)

    ratio = recent_count / historical_avg if historical_avg > 0 else 1.0

    if ratio > 1.5:
        # Rapidly increasing usage → higher T-Score (more modal)
        return min(0.15, (ratio - 1.0) * 0.1)
    elif ratio < 0.5:
        # Declining usage → lower T-Score (less modal)
        return max(-0.15, (ratio - 1.0) * 0.1)
    else:
        return 0.0
```

### 3. Hybrid Mode (Recommended)

Combines static baseline with trend adjustments.

```yaml
hybrid_calculation:
  base: static_table
  adjustments:
    - recency_modifier (API-based, cached)
    - trend_modifier (3-year slope analysis)

  fallback_on_api_failure: static_only
```

## User Checkpoint Integration

```markdown
⬜ CP-INIT-003: T-Score Mode Selection

"How should T-Score be calculated?"

Options:
  ○ Static (Fast, stable)
    Use pre-defined tables. Best for offline use.

  ○ Dynamic (Recommended)
    Query APIs for real-time data. Most accurate.

  ○ Hybrid
    Static baseline with trend adjustments. Balanced.
```

## Domain-Specific Adjustments

```yaml
domain_modifiers:
  education:
    TAM: +0.05    # Even more overused in EdTech
    SDT: -0.05    # Less common, good differentiation

  psychology:
    SCT: +0.05    # Very dominant
    ACT: -0.10    # Underutilized

  HRD:
    TAM: +0.10    # Extremely overused
    JD-R: -0.05   # Growing but not saturated

  healthcare:
    TPB: +0.05    # Dominant in health behavior
    COM-B: -0.10  # Newer, less saturated
```

## T-Score Reference Tables

### Theoretical Frameworks (Default Static Values)

```
T > 0.8 (MODAL - AVOID):
├── Technology Acceptance Model (TAM): 0.95
├── Social Cognitive Theory (SCT): 0.90
├── Theory of Planned Behavior (TPB): 0.88
├── UTAUT/UTAUT2: 0.85
└── Self-Efficacy Theory (standalone): 0.82

T 0.5-0.8 (ESTABLISHED - DIFFERENTIATE):
├── Self-Determination Theory (SDT): 0.70
├── Cognitive Load Theory (CLT): 0.65
├── Flow Theory: 0.62
├── Community of Inquiry (CoI): 0.58
├── Expectancy-Value Theory: 0.55
└── Achievement Goal Theory: 0.52

T 0.3-0.5 (EMERGING - RECOMMENDED):
├── Control-Value Theory: 0.45
├── Theory Integration (e.g., TAM×SDT): 0.42
├── Context-Specific Adaptations: 0.40
├── Multi-level Theory Applications: 0.38
└── Competing Theory Comparison: 0.35

T < 0.3 (INNOVATIVE - TOP-TIER):
├── Novel Theoretical Synthesis: 0.25
├── Cross-Domain Theory Transfer: 0.22
├── Meta-Theoretical Frameworks: 0.18
└── Paradigm Shift Proposals: 0.15
```

### Statistical Methods

```
T > 0.8 (MODAL - AVOID):
├── Independent t-test: 0.92
├── One-way ANOVA: 0.88
├── OLS Regression: 0.85
└── Pearson correlation: 0.82

T 0.5-0.8 (ESTABLISHED):
├── Hierarchical Linear Modeling (HLM): 0.65
├── Structural Equation Modeling (SEM): 0.60
├── Traditional Meta-analysis: 0.58
└── Mixed-effects models: 0.55

T 0.3-0.5 (EMERGING - RECOMMENDED):
├── Bayesian methods: 0.45
├── Meta-Analytic SEM (MASEM): 0.42
├── Machine Learning + inference: 0.40
└── Causal inference methods: 0.38

T < 0.3 (INNOVATIVE):
├── Causal discovery algorithms: 0.28
├── Network psychometrics: 0.25
├── Computational modeling: 0.22
└── Novel hybrid methods: 0.18
```

## Error Handling

```yaml
error_handling:
  api_timeout:
    action: fallback_to_static
    log: "API timeout, using static T-Score"

  api_rate_limit:
    action: use_cached_or_static
    retry_after: 60s

  invalid_query:
    action: fallback_to_static
    log: "Invalid query, check theory/domain names"

  no_results:
    action: use_base_score_only
    note: "No recent papers found, theory may be novel"
```

## Usage Example

```markdown
# In agent execution:

1. User selects T-Score mode (CP-INIT-003)
2. Engine queries T-Score for requested theory/method
3. Returns: { theory: "SDT", t_score: 0.68, mode: "dynamic", confidence: "high" }
4. Agent uses T-Score for modal identification and sampling
```
