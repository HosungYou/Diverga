# AI Pattern Detection Rules v2.0

## Overview

This document consolidates detection rules, scoring algorithms, and threshold settings for the G5-AcademicStyleAuditor agent.

v2.0 adds quantitative stylometric metrics (burstiness, MTLD, sentence length range, paragraph opener diversity), four structural detection patterns (S7-S10), a composite scoring formula, and non-native speaker calibration.

**Reference**: Full literature background at https://github.com/HosungYou/humanizer

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

### Phase 2: Quantitative Metric Calculation

```
# Burstiness (CV of sentence lengths)
sentences = tokenize_into_sentences(text)
lengths = [word_count(s) for s in sentences]
CV = std_dev(lengths) / mean(lengths)
burstiness_penalty = max(0, (0.45 - CV) / 0.45 * 100)

# MTLD (Measure of Textual Lexical Diversity)
mtld_value = calculate_MTLD(text, ttr_threshold=0.72)
vocab_diversity_penalty = max(0, (80 - mtld_value) / 80 * 100)

# Sentence Length Range
length_range = max(lengths) - min(lengths)
# Scoring: 0 penalty if range > 25, scaled penalty up to range = 0

# Paragraph Opener Diversity
paragraphs = split_into_paragraphs(text)
first_3_words = [get_first_n_words(p, 3) for p in paragraphs]
opener_diversity = len(set(first_3_words)) / len(paragraphs)
# Scoring: 0 penalty if diversity > 0.70, scaled penalty below
```

### Phase 3: Structural Pattern Detection

```
FOR each structural pattern (S7, S8, S9, S10):
    SCAN text for structural indicators
    IF indicator found:
        LOG structural pattern instance with:
            - Pattern ID
            - Location (section, paragraph range)
            - Matched structure description
            - Risk level
            - Suggested narrative alternative

structural_penalty = normalize_0_100(
    S7_score * 12 + S8_score * 10 + S9_score * 8 + S10_score * 10
)
```

### Phase 4: Composite Scoring

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

# Normalize pattern score to 0-100 scale
pattern_score = min(100, total_score / max_expected_score * 100)

# Composite formula (v2.0)
AI_Probability = (0.60 * pattern_score)
              + (0.20 * burstiness_penalty)
              + (0.10 * vocab_diversity_penalty)
              + (0.10 * structural_penalty)
```

---

## Quantitative Metrics

Four stylometric metrics supplement pattern-based detection. These capture statistical properties of text that pattern matching alone cannot detect.

### Metric Definitions

| Metric | Method | Human Baseline | AI Typical | Weight | Scoring |
|--------|--------|----------------|------------|--------|---------|
| **Burstiness (CV)** | SD(sentence_lengths) / Mean(sentence_lengths) | > 0.45 | < 0.30 | 15 | `max(0, (0.45 - CV) / 0.45 * 100)` |
| **MTLD** | Mean length of sequential word strings maintaining TTR > 0.72 | > 80 | < 60 | 10 | `max(0, (80 - MTLD) / 80 * 100)` |
| **Sentence Length Range** | max(word_count) - min(word_count) | > 25 words | < 15 words | 5 | `max(0, (25 - range) / 25 * 100)` |
| **Paragraph Opener Diversity** | unique_first_3_words / total_paragraphs | > 0.70 | < 0.50 | 8 | `max(0, (0.70 - diversity) / 0.70 * 100)` |

### Supplementary Metric: Fano Factor

```
Fano_Factor = Variance(sentence_lengths) / Mean(sentence_lengths)

Interpretation:
  Fano > 1  : super-Poissonian (bursty, human-like)
  Fano = 1  : Poisson (random baseline)
  Fano < 1  : sub-Poissonian (regular, AI-like)
```

The Fano Factor is reported for diagnostic purposes but not included in the composite score formula.

### Research Basis

- GPTZero uses perplexity + burstiness as its two primary signals
- MTLD is the only length-invariant vocabulary diversity metric (McCarthy & Jarvis, 2010)
- Fano Factor > 1 indicates human-like variance in sentence production
- Paragraph opener repetition is a strong structural indicator of AI generation

See `.claude/references/agents/g5/quantitative-metrics.md` for full calculation methods and pseudocode.

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
| **Style (Original)** |
| S1 | 5 | Em Dash Overuse |
| S2 | 3 | Excessive Boldface |
| S3 | 6 | Inline-Header Lists |
| S4 | 2 | Title Case Overuse |
| S5 | 20 | Emoji Usage |
| S6 | 2 | Quote Inconsistency |
| **Style (Structural — v2.0)** |
| S7 | 12 | Enumeration as Prose |
| S8 | 10 | Repetitive Paragraph Openers |
| S9 | 8 | Formulaic Section Structure |
| S10 | 10 | Hypothesis Checklist Pattern |
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

## Structural Detection Patterns (S7-S10)

These patterns were discovered empirically: after vocabulary-level cleaning (Rounds 1-2), these structural patterns accounted for the remaining 60%+ AI probability. They operate at paragraph/section level and resist word-level humanization.

### S7: Enumeration as Prose (Weight: 12, Risk: HIGH)

**Definition**: Ordinal markers ("First,...Second,...Third,...Finally,...") embedded within flowing paragraph text, not formatted as bullet or numbered lists. This creates a hidden list structure that AI detectors recognize as a generation fingerprint.

**Detection**: Scan for 3+ sequential ordinal markers (First/Second/Third/Additionally/Finally/Moreover; Korean: 첫째/둘째/셋째) within paragraph prose. Also detect "There are N key [findings/contributions/implications]" followed by enumeration.

### S8: Repetitive Paragraph Openers (Weight: 10, Risk: HIGH)

**Definition**: More than 3 paragraphs in the same section starting with the same syntactic template, most commonly "The [noun]..." (e.g., "The results showed...", "The analysis revealed...", "The findings suggest...").

**Detection**: Extract first 3 words of each paragraph. Flag if >3 paragraphs share the pattern "The [X]..." or any other repeated opening template within a single section.

### S9: Formulaic Section Structure (Weight: 8, Risk: MEDIUM)

**Definition**: Discussion section following a rigid template without deviation: (1) restate findings, (2) compare to prior literature, (3) state implications, (4) acknowledge limitations, (5) suggest future research. Each subsection mechanically repeats this sequence.

**Detection**: Analyze rhetorical move sequence in Discussion. Flag if section follows the restate-compare-implications-limitations-future template with predictable transitions ("Consistent with prior research...", "These findings have implications for...", "Several limitations warrant acknowledgment...").

### S10: Hypothesis Checklist Pattern (Weight: 10, Risk: HIGH)

**Definition**: Sequential hypothesis confirmation statements in mechanical list format: "H1 was supported (p < .001). H2 was partially supported. H3 was not supported."

**Detection**: Find sequential hypothesis labels (H1, H2, H3... or Hypothesis 1, Hypothesis 2...) each followed by a support/non-support verdict within 2-3 sentences. Flag when 3+ hypotheses are listed sequentially with mechanical confirmation language.

See `.claude/references/agents/g5/structural-patterns.md` for full pattern definitions with examples.

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
| **High** | C1, C4, C5, L1-tier1, S5, S7, S8, S10, M1, M2, A3, A4 |
| **Medium** | C2, C3, L1-tier2, L2, L3, L5, S1, S3, S9, M3, H2, H3 |
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

## Non-Native Speaker Calibration

**Research basis**: Liang et al. (2023) found >61% of TOEFL essays misclassified as AI. Non-native academic English naturally shares surface features with AI text -- simpler vocabulary, more regular sentence structures, less idiomatic usage. Stanford (2025) found >20% false positive rates for non-native speakers across major detectors.

This calibration is **opt-in only**.

```yaml
non_native_calibration:
  enabled: false  # User must explicitly opt in
  adjustments:
    L1_weight: "x 0.7"         # Reduce AI vocabulary flagging by 30%
    H1_weight: "x 0.8"         # Reduce verbose phrase flagging by 20%
    burstiness_threshold: 0.35  # Lower baseline from 0.45 for non-native
  scoring_impact:
    burstiness_penalty: "max(0, (0.35 - CV) / 0.35 * 100)"  # Adjusted threshold
    vocab_diversity_penalty: "unchanged"  # MTLD threshold remains at 80
    pattern_score: "L1 and H1 weights reduced per adjustments above"
  rationale: >
    Non-native academic English naturally has lower lexical diversity
    and more regular sentence patterns. Without calibration, these
    writers face systematically higher false positive rates exceeding
    61% in documented studies. The calibration reduces sensitivity to
    patterns that overlap between non-native human writing and AI
    generation, while maintaining detection of genuine AI structural
    fingerprints (S7-S10, M1, M2).
```

---

## Scoring

### Composite Formula (v2.0)

```
AI_Probability = (0.60 * pattern_score)
              + (0.20 * burstiness_penalty)
              + (0.10 * vocab_diversity_penalty)
              + (0.10 * structural_penalty)

Where:
  pattern_score           = Normalized 0-100 from Phase 1 pattern detection
  burstiness_penalty      = max(0, (0.45 - CV) / 0.45 * 100)
  vocab_diversity_penalty = max(0, (80 - MTLD) / 80 * 100)
  structural_penalty      = Normalized 0-100 from S7+S8+S9+S10 weighted scores
```

### Component Weights Rationale

| Component | Weight | Rationale |
|-----------|--------|-----------|
| Pattern score | 60% | Core detection signal; 28 validated pattern categories |
| Burstiness penalty | 20% | Strongest single quantitative discriminator; partially independent of vocabulary patterns |
| Vocabulary diversity penalty | 10% | Complementary lexical signal; less discriminative in academic text |
| Structural penalty | 10% | Captures section/paragraph-level AI fingerprints missed by word-level analysis |

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
  show: score, risk_level, pattern_count, burstiness_cv

standard:  # Default
  show: score, risk_level, high_risk_patterns, quantitative_metrics, recommendation

detailed:  # Full analysis
  show: all_patterns, quantitative_metrics, structural_patterns, transformations, before_after, category_breakdown

expert:  # For debugging
  show: all_above + scoring_breakdown + context_analysis + composite_formula_components
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
score +/- confidence_margin

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
| S9 formulaic structure | High in IMRAD papers | Check for variation within template |
| S7 enumeration | Moderate in methods | Acceptable for procedural steps |

### Adjustment Rules

```
IF text is from established academic author:
    score *= 0.8  # Reduce suspicion

IF journal has strict style guide:
    exempt S1, S2, S4 patterns  # Style may be required

IF text is from non-native English speaker:
    apply non_native_calibration  # See Non-Native Speaker Calibration section
```

---

## Reporting Format

### Quick Summary

```
AI Pattern Analysis: 47% probability (composite)
   Pattern score: 52% | Burstiness CV: 0.31 | MTLD: 58 | Structural: 3 flags
   Patterns: 15 found (4 high, 6 medium, 5 low)
   Recommendation: Review medium-risk patterns + improve sentence length variation
```

### Standard Report

```
## AI Pattern Analysis Report v2.0

### Summary
| Metric | Value |
|--------|-------|
| AI Probability (composite) | 47% |
| Pattern Score | 52% |
| Burstiness CV | 0.31 (AI-typical; human baseline > 0.45) |
| MTLD | 58 (AI-typical; human baseline > 80) |
| Sentence Length Range | 18 words (AI-typical; human baseline > 25) |
| Paragraph Opener Diversity | 0.48 (AI-typical; human baseline > 0.70) |
| Total Patterns | 15 |
| High Risk | 4 |
| Structural Patterns | S7 x2, S8 x1 |

### High-Risk Patterns (Fix These)
1. [C1] "pivotal study" -> "this study" (line 3)
2. [L1] "delve", "tapestry" clustered (para 2)
3. [S7] "First,...Second,...Third,..." enumeration (para 5-6)
4. [S10] "H1 was supported. H2 was partially..." (Discussion)

### Quantitative Recommendations
- Increase sentence length variation (current CV: 0.31, target: > 0.45)
- Add short declarative sentences (3-8 words) at impact points
- Vary paragraph openers (current diversity: 0.48, target: > 0.70)

### Recommendation
[B] Humanize (Balanced) recommended
```

---

## Version History

- **v2.0.0**: Quantitative stylometric metrics (burstiness CV, MTLD, sentence length range, paragraph opener diversity), structural detection patterns S7-S10, composite scoring formula, non-native speaker calibration, updated risk classifications
- **v1.0.0**: Initial detection rules based on Wikipedia AI Cleanup
- Calibrated for academic writing contexts
- Integrated with Diverga v6.0 checkpoint system
