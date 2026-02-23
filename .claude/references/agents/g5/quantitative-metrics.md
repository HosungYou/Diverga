# Quantitative Metrics for AI Text Detection

## Overview

G5 v2.0 supplements pattern-based detection with four quantitative stylometric metrics that capture statistical properties of text. These metrics measure dimensions that pattern matching alone cannot detect -- specifically, the regularity of sentence production and the diversity of vocabulary and paragraph structure that distinguish human writing from AI generation.

**Version**: 2.0.0
**Reference**: Full literature background at https://github.com/HosungYou/humanizer

### Research Basis

- GPTZero uses perplexity + burstiness as its two primary detection signals
- MTLD is the only length-invariant vocabulary diversity metric (McCarthy & Jarvis, 2010)
- Fano Factor > 1 indicates human-like super-Poissonian variance in sentence production
- A 2024 meta-analysis found stylometric methods alone detect GPT-4-level text at 70-80% precision, rising to ~90% when fused with ML classifiers
- Liang et al. (2023) documented >61% false positive rates for non-native English writers, motivating calibrated thresholds

---

## Metric 1: Burstiness (Coefficient of Variation of Sentence Lengths)

### Purpose

Measures variance in sentence length across the document. Human writers naturally alternate between short punchy sentences (3-5 words) and extended complex constructions (30-50 words), creating high burstiness. LLMs tend toward medium-length sentences with consistent syntactic complexity, producing systematically lower burstiness.

Even high-perplexity AI-generated text exhibits low burstiness, making burstiness a complementary, partially independent signal from vocabulary-based detection.

### Baselines

| Population | CV Value | Interpretation |
|------------|----------|----------------|
| Human academic writing | > 0.45 | Natural rhythm with varied sentence length |
| AI-generated academic text | < 0.30 | Metronomic, narrow sentence length band |
| Non-native English academic | > 0.35 | Lower than native but higher than AI |
| Threshold (default) | 0.45 | Below this, burstiness penalty applies |
| Threshold (non-native calibration) | 0.35 | Adjusted for non-native writers |

### Weight in Composite Score

**15** (highest among quantitative metrics; second only to pattern score in overall contribution through the 0.20 burstiness_penalty weight in the composite formula)

### Calculation Method

```
Input: raw text (string)

Step 1: Sentence Tokenization
  sentences = tokenize_sentences(text)
  # Use rule-based tokenizer that handles:
  #   - Abbreviations (e.g., "et al.", "Fig.", "Dr.")
  #   - Decimal numbers (e.g., "p = .001")
  #   - Parenthetical citations (Author, 2024)
  #   - Quoted material

Step 2: Compute Sentence Lengths
  lengths = []
  FOR each sentence in sentences:
      word_count = count_words(sentence)
      # Exclude:
      #   - Sentences that are purely citations
      #   - Table/figure captions (if identifiable)
      #   - Section headers
      IF word_count >= 3:  # Minimum threshold to exclude fragments
          lengths.append(word_count)

Step 3: Calculate CV
  mean_length = sum(lengths) / len(lengths)
  variance = sum((L - mean_length)^2 for L in lengths) / len(lengths)
  std_dev = sqrt(variance)
  CV = std_dev / mean_length

Step 4: Calculate Penalty
  IF CV >= 0.45:
      burstiness_penalty = 0  # No penalty; human-like variance
  ELSE:
      burstiness_penalty = (0.45 - CV) / 0.45 * 100
      # Linear scaling: CV=0 -> penalty=100, CV=0.45 -> penalty=0

  # Non-native calibration (if enabled):
  IF non_native_calibration.enabled:
      IF CV >= 0.35:
          burstiness_penalty = 0
      ELSE:
          burstiness_penalty = (0.35 - CV) / 0.35 * 100
```

### Interpretation Guide

| CV Range | Label | Interpretation | Action |
|----------|-------|----------------|--------|
| > 0.55 | High burstiness | Strong human signal; highly varied prose | No concern |
| 0.45 - 0.55 | Normal burstiness | Within human range | No concern |
| 0.35 - 0.45 | Low burstiness | Borderline; could be non-native or AI-assisted | Flag for review |
| 0.25 - 0.35 | Very low burstiness | Strong AI signal; metronomic rhythm | Recommend burstiness enhancement |
| < 0.25 | Minimal burstiness | Almost certainly AI-generated text | Strongly recommend structural rewrite |

### Diagnostic Examples

**High burstiness (CV = 0.58, human-like)**:
- "Education mattered. But not in the straightforward way we expected. People with college degrees were more likely to know what large language models actually do, and that awareness amplified their concern about job displacement in ways that varied dramatically across partisan lines."
- Sentence lengths: 2, 9, 35 words -> SD = 14.3, Mean = 15.3, CV = 0.93

**Low burstiness (CV = 0.22, AI-like)**:
- "Education was positively associated with concern about AI. Higher educational attainment predicted greater awareness of AI capabilities. The relationship between education and concern was moderated by partisan identity. These findings suggest that educational effects operate differently across political contexts."
- Sentence lengths: 8, 8, 11, 11 words -> SD = 1.5, Mean = 9.5, CV = 0.16

---

## Metric 2: MTLD (Measure of Textual Lexical Diversity)

### Purpose

Measures vocabulary diversity -- the range of different words used relative to text length. AI-generated academic text tends to cycle through a narrower set of "safe" vocabulary, producing lower lexical diversity. MTLD is specifically chosen because it is the only index validated as not varying as a function of text length (McCarthy & Jarvis, 2010), making it suitable for comparing texts of different lengths.

### Baselines

| Population | MTLD Value | Interpretation |
|------------|------------|----------------|
| Human academic writing | > 80 | Rich, varied vocabulary |
| AI-generated academic text | < 60 | Narrower vocabulary cycling |
| Threshold | 80 | Below this, diversity penalty applies |

### Weight in Composite Score

**10** (contributes through the 0.10 vocab_diversity_penalty weight in the composite formula)

### Calculation Method

```
Input: raw text (string)

Step 1: Tokenization
  tokens = tokenize_words(text)
  # Lowercase all tokens
  # Remove punctuation tokens
  # Keep all content words (nouns, verbs, adjectives, adverbs)
  # Keep function words (they contribute to diversity measurement)

Step 2: Forward MTLD Pass
  ttr_threshold = 0.72  # Standard threshold (McCarthy & Jarvis, 2010)
  factors_forward = 0
  token_count = 0
  type_set = set()

  FOR each token in tokens:
      token_count += 1
      type_set.add(token)
      current_ttr = len(type_set) / token_count

      IF current_ttr <= ttr_threshold:
          factors_forward += 1
          token_count = 0
          type_set = set()

  # Handle remainder (partial factor)
  IF token_count > 0:
      current_ttr = len(type_set) / token_count
      partial_factor = (1.0 - current_ttr) / (1.0 - ttr_threshold)
      factors_forward += partial_factor

  mtld_forward = len(tokens) / factors_forward

Step 3: Backward MTLD Pass
  # Repeat Step 2 with tokens reversed
  reversed_tokens = tokens[::-1]
  # ... (same algorithm as forward pass)
  mtld_backward = len(tokens) / factors_backward

Step 4: Average
  mtld_value = (mtld_forward + mtld_backward) / 2

Step 5: Calculate Penalty
  IF mtld_value >= 80:
      vocab_diversity_penalty = 0
  ELSE:
      vocab_diversity_penalty = (80 - mtld_value) / 80 * 100
      # Linear scaling: MTLD=0 -> penalty=100, MTLD=80 -> penalty=0
```

### Comparison with Other Vocabulary Diversity Metrics

| Metric | Method | Length Invariant | Recommended |
|--------|--------|-----------------|-------------|
| **TTR** (Type-Token Ratio) | Unique words / Total words | No -- decreases with length | Not for cross-document comparison |
| **MATTR** (Moving Average TTR) | Rolling-window TTR average | Partially -- window size is free parameter | Acceptable alternative |
| **MTLD** | Mean factor length maintaining TTR > threshold | **Yes** -- validated across 4 dimensions | **Recommended (primary)** |
| **vocd-D / HD-D** | Curve-fitting to hypergeometric distribution | Yes -- statistically principled | Good alternative; complex to implement |
| **Maas** | Log-based TTR transformation | Partially | Less intuitive interpretation |

**Key reference**: McCarthy, P. M., & Jarvis, S. (2010). MTLD, vocd-D, and HD-D: A validation study of sophisticated approaches to lexical diversity assessment. *Behavior Research Methods*, 42(2), 381-392.

### Interpretation Guide

| MTLD Range | Label | Interpretation | Action |
|------------|-------|----------------|--------|
| > 100 | Very high diversity | Rich vocabulary; strong human signal | No concern |
| 80 - 100 | Normal diversity | Within human range | No concern |
| 60 - 80 | Low diversity | Borderline; may indicate AI assistance or non-native writing | Flag for review |
| 40 - 60 | Very low diversity | Strong AI signal; vocabulary cycling | Recommend vocabulary diversification |
| < 40 | Minimal diversity | Very likely AI-generated or heavily templated | Strongly recommend rewrite |

---

## Metric 3: Sentence Length Range

### Purpose

A simple but effective measure of whether the text contains both very short and very long sentences. Human academic writers naturally produce sentences ranging from brief declaratives ("That gap is real.") to extended complex constructions with multiple subordinate clauses. AI text tends to cluster in a narrow band around medium length (15-30 words).

### Baselines

| Population | Range (words) | Interpretation |
|------------|---------------|----------------|
| Human academic writing | > 25 | Wide spread (e.g., 4-word to 45-word sentences) |
| AI-generated academic text | < 15 | Narrow band (e.g., 18-word to 32-word sentences) |
| Threshold | 25 | Below this, range penalty applies |

### Weight in Composite Score

**5** (lowest weight; serves as a simple sanity check complementing CV)

### Calculation Method

```
Input: sentence_lengths (array of integers, from Burstiness calculation Step 2)

Step 1: Compute Range
  min_length = min(sentence_lengths)
  max_length = max(sentence_lengths)
  length_range = max_length - min_length

Step 2: Calculate Penalty
  IF length_range >= 25:
      range_penalty = 0
  ELSE:
      range_penalty = (25 - length_range) / 25 * 100
      # Linear scaling: range=0 -> penalty=100, range=25 -> penalty=0
```

### Interpretation Guide

| Range (words) | Label | Interpretation |
|---------------|-------|----------------|
| > 35 | Very wide | Strong human signal; dramatic variation |
| 25 - 35 | Normal | Within human range |
| 15 - 25 | Narrow | Borderline; limited variation |
| 5 - 15 | Very narrow | Strong AI signal |
| < 5 | Minimal | Almost certainly AI; all sentences similar length |

### Relationship to Burstiness

Sentence length range and burstiness (CV) are correlated but not redundant:
- **Range** captures the extremes (minimum and maximum sentence lengths)
- **CV** captures the distribution across all sentences

A text could have a wide range (one very short and one very long sentence) but low CV (most sentences are medium length). Conversely, a text could have moderate range but high CV if sentence lengths are evenly distributed across that range. Both signals contribute complementary information.

---

## Metric 4: Paragraph Opener Diversity

### Purpose

Detects the AI tendency to start consecutive paragraphs with the same syntactic pattern. The most common pattern is "The [noun]..." but any repetitive opener counts. Human writers instinctively vary paragraph openings, using questions, subordinate clauses, adverbial phrases, short declarations, and other structures.

### Baselines

| Population | Diversity Ratio | Interpretation |
|------------|-----------------|----------------|
| Human academic writing | > 0.70 | Most paragraphs start differently |
| AI-generated academic text | < 0.50 | Many paragraphs share opening patterns |
| Threshold | 0.70 | Below this, diversity penalty applies |

### Weight in Composite Score

**8** (second-highest quantitative weight; paragraph openers are a strong structural signal)

### Calculation Method

```
Input: raw text (string)

Step 1: Split into Paragraphs
  paragraphs = split_paragraphs(text)
  # A paragraph is text separated by blank lines or indentation
  # Exclude:
  #   - Section headers
  #   - Table/figure content
  #   - Reference list entries
  #   - Paragraphs with fewer than 2 sentences

Step 2: Extract First N Words
  first_words = []
  FOR each paragraph in paragraphs:
      words = get_first_n_words(paragraph, n=3)
      # Normalize: lowercase, strip punctuation
      first_words.append(tuple(words))

Step 3: Calculate Diversity
  unique_openers = len(set(first_words))
  total_paragraphs = len(first_words)
  opener_diversity = unique_openers / total_paragraphs

Step 4: Calculate Penalty
  IF opener_diversity >= 0.70:
      opener_penalty = 0
  ELSE:
      opener_penalty = (0.70 - opener_diversity) / 0.70 * 100
      # Linear scaling: diversity=0 -> penalty=100, diversity=0.70 -> penalty=0
```

### Pattern Detection Detail

Beyond the simple diversity ratio, flag specific repetitive patterns:

| Pattern | Example | Detection |
|---------|---------|-----------|
| "The [X] [verb]" | "The results showed", "The analysis revealed" | First word = "The", third word is verb |
| "[Noun] [verb] that" | "Results showed that", "Findings indicated that" | Third word = "that" |
| "In [context]," | "In this study,", "In the current analysis," | First word = "In" |
| "This [noun]" | "This study", "This finding", "This analysis" | First word = "This" |
| "Our [noun]" | "Our results", "Our analysis", "Our findings" | First word = "Our" |

### Interaction with S8

Paragraph opener diversity (this metric) and S8 (Repetitive Paragraph Openers pattern) detect overlapping signals:
- **This metric** provides a quantitative score (the diversity ratio) that feeds into the composite formula
- **S8** provides a qualitative pattern detection with specific flagged locations and suggested fixes

Both are calculated but they are not double-counted. The structural_penalty in the composite formula uses S8's weighted score. The opener_diversity score contributes independently through paragraph opener diversity's weight.

---

## Supplementary Metric: Fano Factor

### Purpose

The Fano Factor provides an alternative characterization of sentence length variance based on the Poisson distribution. While CV normalizes standard deviation by the mean, the Fano Factor normalizes variance by the mean. This provides a natural comparison point: a Fano Factor of 1 corresponds to a Poisson process (random), values above 1 indicate "bursty" (clustered) behavior, and values below 1 indicate "regular" (evenly-spaced) behavior.

### Calculation

```
Input: sentence_lengths (array of integers)

variance = sum((L - mean)^2 for L in lengths) / len(lengths)
mean = sum(lengths) / len(lengths)

fano_factor = variance / mean
```

### Interpretation

| Fano Factor | Distribution Type | Interpretation |
|-------------|-------------------|----------------|
| > 2.0 | Strongly super-Poissonian | Highly bursty; strong human signal |
| 1.0 - 2.0 | Mildly super-Poissonian | Moderate burstiness; likely human |
| ~1.0 | Poisson | Random baseline |
| 0.5 - 1.0 | Mildly sub-Poissonian | Somewhat regular; possible AI |
| < 0.5 | Strongly sub-Poissonian | Highly regular; strong AI signal |

### Role in Scoring

The Fano Factor is **reported for diagnostic purposes** but is **not included in the composite score formula**. The CV (burstiness metric) already captures variance information and is more interpretable. The Fano Factor is provided as a supplementary signal for expert-level analysis and as a cross-check on the CV value.

### Relationship to CV

For sentence lengths with mean M and standard deviation S:
- CV = S / M
- Fano = S^2 / M = CV^2 * M

The Fano Factor scales with the mean sentence length, so longer-sentence documents will tend to have higher Fano Factors. CV is preferred for the composite score because it is scale-independent.

---

## Composite Scoring Integration

### Formula

```
AI_Probability = (0.60 * pattern_score)
              + (0.20 * burstiness_penalty)
              + (0.10 * vocab_diversity_penalty)
              + (0.10 * structural_penalty)
```

### Component Calculation Summary

| Component | Source | Range | Weight in Formula |
|-----------|--------|-------|-------------------|
| pattern_score | Phase 1 pattern detection (28 categories) | 0-100 | 0.60 |
| burstiness_penalty | `max(0, (0.45 - CV) / 0.45 * 100)` | 0-100 | 0.20 |
| vocab_diversity_penalty | `max(0, (80 - MTLD) / 80 * 100)` | 0-100 | 0.10 |
| structural_penalty | S7+S8+S9+S10 weighted scores, normalized | 0-100 | 0.10 |

### Worked Example

Given a text with:
- Pattern detection: 34 patterns found, normalized score = 62
- Burstiness CV: 0.31
- MTLD: 58
- Structural: S7 found (1 instance), S8 found (1 instance), S9 not found, S10 not found

Calculation:
```
pattern_score = 62

burstiness_penalty = max(0, (0.45 - 0.31) / 0.45 * 100)
                   = max(0, 0.14 / 0.45 * 100)
                   = max(0, 31.1)
                   = 31.1

vocab_diversity_penalty = max(0, (80 - 58) / 80 * 100)
                        = max(0, 22 / 80 * 100)
                        = max(0, 27.5)
                        = 27.5

structural_penalty:
  S7: 1 instance * weight 12 = 12
  S8: 1 instance * weight 10 = 10
  S9: 0
  S10: 0
  raw = 22, max_possible = 40 (12+10+8+10)
  structural_penalty = 22 / 40 * 100 = 55.0

AI_Probability = (0.60 * 62) + (0.20 * 31.1) + (0.10 * 27.5) + (0.10 * 55.0)
               = 37.2 + 6.22 + 2.75 + 5.50
               = 51.67
               = 52% (rounded)
```

Risk level: **Elevated** (Probably AI-Assisted) -- review needed.

---

## Metric Summary Table

| Metric | Method | Human Baseline | AI Typical | Weight | Penalty Formula |
|--------|--------|----------------|------------|--------|-----------------|
| **Burstiness (CV)** | SD / Mean of sentence lengths | > 0.45 | < 0.30 | 15 | `max(0, (0.45 - CV) / 0.45 * 100)` |
| **MTLD** | Mean factor length at TTR > 0.72 | > 80 | < 60 | 10 | `max(0, (80 - MTLD) / 80 * 100)` |
| **Sentence Length Range** | max - min word count | > 25 words | < 15 words | 5 | `max(0, (25 - range) / 25 * 100)` |
| **Paragraph Opener Diversity** | unique_first_3 / total_paragraphs | > 0.70 | < 0.50 | 8 | `max(0, (0.70 - div) / 0.70 * 100)` |
| **Fano Factor** (supplementary) | Variance / Mean of sentence lengths | > 1.0 | < 1.0 | -- | Diagnostic only; not in composite |

---

## Version History

- **v2.0.0**: Initial quantitative metrics module with burstiness CV, MTLD, sentence length range, paragraph opener diversity, and Fano Factor
