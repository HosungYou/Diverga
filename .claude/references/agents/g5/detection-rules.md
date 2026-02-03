# AI Pattern Detection Rules

## Overview

This document consolidates detection rules, scoring algorithms, and threshold settings for the G5-AcademicStyleAuditor agent.

---

## Detection Algorithm

### Phase 1: Pattern Scanning

```
FOR each pattern category (C, L, S, M, H, A):
    FOR each pattern in category:
        SCAN text for indicators
        IF indicator found:
            CHECK academic context exceptions
            IF not excepted:
                LOG pattern instance with:
                    - Pattern ID
                    - Location (paragraph, sentence)
                    - Matched text
                    - Risk level
                    - Suggested transformation
```

### Phase 2: Scoring

```
total_score = 0
category_scores = {}

FOR each detected pattern:
    base_score = pattern_weights[pattern_id]

    # Apply modifiers
    IF pattern is clustered with others:
        base_score *= 1.5  # Clustering bonus

    IF context makes pattern more suspicious:
        base_score *= context_multiplier

    IF multiple instances of same pattern:
        base_score *= (1 + 0.2 * (count - 1))  # Diminishing returns

    total_score += base_score
    category_scores[category] += base_score

# Normalize to 0-100 scale
ai_probability = min(100, total_score / max_expected_score * 100)
```

---

## Pattern Weights

| Pattern ID | Base Weight | Category |
|------------|-------------|----------|
| **Content** |
| C1 | 10 | Significance Inflation |
| C2 | 7 | Notability Claims |
| C3 | 6 | Superficial -ing |
| C4 | 10 | Promotional Language |
| C5 | 12 | Vague Attributions |
| C6 | 3 | Formulaic Sections |
| **Language** |
| L1-tier1 | 15 | AI Vocabulary (high alert) |
| L1-tier2 | 8 | AI Vocabulary (moderate) |
| L1-cluster | 20 | AI Vocab Clustering Bonus |
| L2 | 8 | Copula Avoidance |
| L3 | 6 | Negative Parallelism |
| L4 | 4 | Rule of Three |
| L5 | 7 | Elegant Variation |
| L6 | 3 | False Ranges |
| **Style** |
| S1 | 5 | Em Dash Overuse |
| S2 | 3 | Excessive Boldface |
| S3 | 6 | Inline-Header Lists |
| S4 | 2 | Title Case Overuse |
| S5 | 20 | Emoji Usage |
| S6 | 2 | Quote Inconsistency |
| **Communication** |
| M1 | 25 | Chatbot Artifacts |
| M2 | 30 | Knowledge Disclaimers |
| M3 | 10 | Sycophantic Tone |
| **Filler** |
| H1 | 2 | Verbose Phrases (per instance) |
| H2 | 8 | Hedge Stacking |
| H3 | 6 | Generic Conclusions |
| **Academic** |
| A1 | 4 | Abstract Template |
| A2 | 4 | Methods Boilerplate |
| A3 | 12 | Discussion Inflation |
| A4 | 15 | Citation Hedging |
| A5 | 3 | Contribution Enumeration |
| A6 | 3 | Limitation Disclaimers |

---

## Risk Classification

### Risk Levels by Score

| Score Range | Risk Level | Label | Action |
|-------------|------------|-------|--------|
| 0-20 | Low | Likely Human | Optional review |
| 21-40 | Moderate | Mixed Signals | Recommended review |
| 41-60 | Elevated | Probably AI-Assisted | Review needed |
| 61-80 | High | Likely AI-Generated | Humanization recommended |
| 81-100 | Critical | Obviously AI | Humanization required |

### Risk Level by Pattern

| Risk Level | Patterns |
|------------|----------|
| **High** | C1, C4, C5, L1-tier1, S5, M1, M2, A3, A4 |
| **Medium** | C2, C3, L1-tier2, L2, L3, L5, S1, S3, M3, H2, H3 |
| **Low** | C6, L4, L6, S2, S4, S6, H1, A1, A2, A5, A6 |

---

## Context Modifiers

Different document sections have different acceptable baselines:

### Section-Based Multipliers

| Section | Multiplier | Rationale |
|---------|------------|-----------|
| Abstract | 1.2 | Highest scrutiny |
| Introduction | 1.1 | Important for first impression |
| Literature Review | 1.0 | Some formality expected |
| Methods | 0.8 | Boilerplate somewhat acceptable |
| Results | 1.0 | Standard |
| Discussion | 1.1 | Claims scrutinized |
| Conclusion | 1.1 | Final impression matters |
| Response Letter | 0.9 | Some formality expected |

### Document Type Multipliers

| Type | Multiplier | Notes |
|------|------------|-------|
| Journal Article | 1.0 | Standard |
| Conference Paper | 0.9 | Slightly less formal |
| Thesis/Dissertation | 1.1 | Higher scrutiny |
| Grant Proposal | 1.0 | Standard |
| Blog Post | 0.5 | Informal OK |
| Social Media | 0.3 | Very informal OK |

---

## Clustering Detection

Patterns become more suspicious when they cluster together:

### Vocabulary Clustering

```
IF (tier1_words >= 2) OR (tier2_words >= 4):
    cluster_detected = true
    bonus_score = 20

IF (patterns_in_same_paragraph >= 3):
    paragraph_cluster = true
    bonus_score += 10 * (pattern_count - 2)
```

### Pattern Type Clustering

When multiple pattern categories appear together:

| Combination | Bonus |
|-------------|-------|
| Content + Language | +10 |
| Language + Style | +5 |
| Content + Communication | +15 |
| Any 3 categories | +20 |
| 4+ categories | +30 |

---

## Density Calculations

### Words Per Pattern

```
pattern_density = total_patterns / (word_count / 100)

IF pattern_density > 3:
    density_flag = "high"
    score_multiplier = 1.3
ELIF pattern_density > 2:
    density_flag = "moderate"
    score_multiplier = 1.1
ELSE:
    density_flag = "normal"
    score_multiplier = 1.0
```

### Specific Density Rules

| Metric | Threshold | Action |
|--------|-----------|--------|
| AI vocabulary per 100 words | > 3 | Flag as high AI |
| Em dashes per paragraph | > 2 | Flag S1 |
| Hedges per sentence | > 2 | Flag H2 |
| Bold terms per paragraph | > 3 | Flag S2 |
| Verbose phrases per page | > 5 | Flag H1 |

---

## Exception Rules

### Automatic Exceptions

These contexts exempt certain patterns:

| Context | Exempted Patterns | Reason |
|---------|------------------|--------|
| Direct quotes | All | Preserving source |
| Code blocks | All | Not prose |
| Tables/Figures | S1, S2, S3 | Different format |
| References section | All | Formatting required |
| Statistical reporting | L1 ("significant", "robust") | Technical terms |

### Partial Exceptions

| Pattern | Partial Exception | When |
|---------|------------------|------|
| A1 | Template phrases | Standard IMRAD |
| A2 | Methods boilerplate | If followed by specifics |
| H1 | "In order to" | Complex nested clauses |

---

## Output Thresholds

### When to Show Warnings

| Condition | Warning Level |
|-----------|---------------|
| score > 20 | Show summary |
| score > 40 | Recommend review |
| score > 60 | Recommend humanization |
| score > 80 | Strongly recommend humanization |

### Report Detail Levels

```yaml
minimal:  # Quick check
  show: score, risk_level, pattern_count

standard:  # Default
  show: score, risk_level, high_risk_patterns, recommendation

detailed:  # Full analysis
  show: all_patterns, transformations, before_after, category_breakdown

expert:  # For debugging
  show: all_above + scoring_breakdown + context_analysis
```

---

## Confidence Calibration

The AI probability score is calibrated against human judgment:

### Calibration Targets

| Predicted | Expected Outcome |
|-----------|------------------|
| 0-20% | 90%+ of texts are human-written |
| 21-40% | Mixed, needs manual review |
| 41-60% | 60%+ are AI-assisted |
| 61-80% | 80%+ are AI-generated |
| 81-100% | 95%+ are AI-generated |

### Confidence Intervals

```
score ± confidence_margin

Where confidence_margin = 10 for most texts
      confidence_margin = 15 for very short texts (<200 words)
      confidence_margin = 5 for long texts (>2000 words)
```

---

## False Positive Mitigation

### Known False Positive Triggers

| Pattern | False Positive Risk | Mitigation |
|---------|---------------------|------------|
| L1 "framework" | High in theory papers | Context check |
| L1 "significant" | High in stats papers | Check for p-values |
| A1 template | High in abstracts | Expected structure |
| H3 future research | Expected in discussion | Check specificity |

### Adjustment Rules

```
IF text is from established academic author:
    score *= 0.8  # Reduce suspicion

IF journal has strict style guide:
    exempt S1, S2, S4 patterns  # Style may be required

IF text is from non-native English speaker:
    reduce L1 weight by 30%  # Some AI words are ESL patterns too
```

---

## Reporting Format

### Quick Summary

```
📊 AI Pattern Analysis: 47% probability
   Patterns: 12 found (3 high, 5 medium, 4 low)
   Recommendation: Review medium-risk patterns
```

### Standard Report

```
## AI Pattern Analysis Report

### Summary
| Metric | Value |
|--------|-------|
| AI Probability | 47% |
| Total Patterns | 12 |
| High Risk | 3 |

### High-Risk Patterns (Fix These)
1. [C1] "pivotal study" → "this study" (line 3)
2. [L1] "delve", "tapestry" clustered (para 2)
3. [M3] Sycophantic opening (line 1)

### Recommendation
[B] Humanize (Balanced) recommended
```

---

## Version History

- v1.0.0: Initial detection rules based on Wikipedia AI Cleanup
- Calibrated for academic writing contexts
- Integrated with Diverga v6.0 checkpoint system
