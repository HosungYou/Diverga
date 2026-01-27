---
name: h-flow-optimizer
description: |
  Humanization-specific flow optimization module.
  Improves text flow at sentence, paragraph, and document levels.
  Part of HAVS (Humanization-Adapted VS) methodology.
version: "3.0.0"
type: humanization
---

# H-Flow-Optimizer Module

## Overview

Optimizes the natural flow of academic text at multiple levels: sentence rhythm, paragraph coherence, and document structure. AI-generated text often exhibits unnaturally consistent patterns that trained reviewers (and detectors) recognize. This module introduces natural variation while maintaining scholarly quality.

## Purpose

> "Human writing breathes—it varies in rhythm, pauses at natural breaks, and builds momentum through deliberate structural choices. AI writing often marches at a uniform pace."

This module analyzes and improves flow patterns to match natural academic writing, reducing detectability while enhancing readability.

## Flow Analysis Levels

### Level 1: Sentence-Level Flow

```yaml
sentence_flow:
  analysis:
    length_variation:
      description: "Natural writing varies sentence length"
      ai_pattern: "Consistent 15-25 word sentences"
      human_pattern: "Mix of 5-10, 15-20, 25-35 word sentences"
      target_coefficient_of_variation: "> 0.30"

    complexity_variation:
      description: "Mix of simple and complex structures"
      ai_pattern: "Consistent compound-complex sentences"
      human_pattern: "Strategic use of simple sentences for emphasis"

    opening_variation:
      description: "Sentence beginnings should vary"
      ai_pattern: "This..., The..., It..., These..."
      human_pattern: "Varied openings including subordinate clauses"

  transformations:
    inject_short_sentence:
      trigger: "3+ consecutive sentences > 20 words"
      action: "Split one sentence or add brief transitional sentence"
      example:
        before: |
          The results demonstrated significant improvement across all metrics.
          Furthermore, participants reported higher satisfaction levels than anticipated.
        after: |
          The results demonstrated significant improvement across all metrics.
          This was unexpected. Participants also reported higher satisfaction
          levels than anticipated.

    vary_complexity:
      trigger: "3+ consecutive complex sentences"
      action: "Simplify one sentence structure"
      example:
        before: |
          Although the intervention showed promise, which was evidenced by
          the significant effect sizes, there remain questions about
          long-term sustainability.
        after: |
          The intervention showed promise. Effect sizes were significant.
          However, questions remain about long-term sustainability.

    diversify_openings:
      trigger: "2+ sentences starting with same word pattern"
      action: "Restructure one sentence opening"
      patterns:
        - "The → [noun/topic] ..."
        - "This → [Specific referent] ..."
        - "It → [Explicit subject] ..."
```

### Level 2: Paragraph-Level Flow

```yaml
paragraph_flow:
  analysis:
    topic_sentence_clarity:
      description: "Clear topic sentence placement"
      ai_pattern: "Always first sentence, formulaic"
      human_pattern: "Usually first, occasionally second with hook"

    evidence_integration:
      description: "How evidence connects to claims"
      ai_pattern: "Claim-evidence-claim-evidence (mechanical)"
      human_pattern: "Claim-evidence-analysis-synthesis (organic)"

    transition_placement:
      description: "Where transitions occur"
      ai_pattern: "Start of every paragraph (formulaic)"
      human_pattern: "Varied: some start, some end, some mid-paragraph"

    paragraph_length_variation:
      description: "Paragraph size distribution"
      ai_pattern: "Consistent 5-7 sentences"
      human_pattern: "Mix of 3-4, 5-7, 8-10 sentence paragraphs"

  transformations:
    improve_evidence_flow:
      trigger: "Mechanical claim-evidence pattern detected"
      action: "Add analysis/synthesis layer"
      example:
        before: |
          Studies show X leads to Y (Smith, 2020). Research also indicates
          that Y affects Z (Jones, 2021). Additionally, Z correlates with
          outcome A (Brown, 2019).
        after: |
          Smith (2020) demonstrated that X leads to Y—a finding that helps
          explain why subsequent research found Y affecting Z (Jones, 2021).
          Building on both findings, Brown (2019) showed the downstream
          effects on outcome A, suggesting a coherent pathway.

    vary_transition_placement:
      trigger: "3+ paragraphs starting with transition words"
      action: "Move transition to previous paragraph end or mid-paragraph"
      example:
        before: |
          [End para 1]... the results were significant.

          However, limitations must be considered.
        after: |
          [End para 1]... the results were significant, though limitations
          warrant consideration.

          The primary concern involves...

    balance_paragraph_length:
      trigger: "3+ consecutive paragraphs of similar length"
      action: "Merge short paragraphs or split long ones"
```

### Level 3: Document-Level Flow

```yaml
document_flow:
  analysis:
    argument_progression:
      description: "How argument builds across sections"
      ai_pattern: "Linear progression, equal section weight"
      human_pattern: "Building momentum, strategic emphasis"

    section_balance:
      description: "Proportion of document sections"
      ai_pattern: "Even distribution (20-20-20-20-20)"
      human_pattern: "Weighted by importance (15-25-30-20-10)"

    introduction_conclusion_echo:
      description: "Connection between opening and closing"
      ai_pattern: "Summary repetition"
      human_pattern: "Thematic echo with progression shown"

    cohesive_device_distribution:
      description: "How cohesion is maintained"
      ai_pattern: "Explicit connectors everywhere"
      human_pattern: "Mix of explicit connectors and implicit reference"

  transformations:
    build_momentum:
      trigger: "Even section weights detected"
      action: "Adjust emphasis to match argument importance"
      guidance:
        - "Front-load methodology justification if novel"
        - "Expand results section for complex findings"
        - "Reduce background for established topics"

    improve_conclusion_echo:
      trigger: "Conclusion merely summarizes"
      action: "Add progression/transformation element"
      example:
        before: |
          In conclusion, this study examined X, found Y, and contributes Z.
        after: |
          Where this investigation began with a question about X, the
          findings reveal not just Y, but a more nuanced picture of how
          Z operates in context—opening new questions about...
```

## Flow Patterns Catalog

### Natural Academic Flow Patterns

```yaml
flow_patterns:
  the_funnel:
    description: "Broad → specific → focused"
    use_for: "Introductions, literature review sections"
    structure:
      - "General context (1-2 sentences)"
      - "Narrowing focus (2-3 sentences)"
      - "Specific gap/question (1-2 sentences)"

  the_claim_stack:
    description: "Claim → evidence → analysis → implication"
    use_for: "Results discussion, argument paragraphs"
    structure:
      - "Main claim (1 sentence)"
      - "Supporting evidence (2-3 sentences)"
      - "Analysis/interpretation (2-3 sentences)"
      - "Implications or transition (1-2 sentences)"

  the_contrast:
    description: "Position A → Position B → Synthesis"
    use_for: "Literature debates, theoretical tensions"
    structure:
      - "First perspective (2-3 sentences)"
      - "Contrasting perspective (2-3 sentences)"
      - "Integration or resolution (2-3 sentences)"

  the_zoom:
    description: "Specific example → broader pattern"
    use_for: "Case studies, qualitative findings"
    structure:
      - "Specific instance/quote (1-2 sentences)"
      - "Pattern identification (2-3 sentences)"
      - "Theoretical connection (2-3 sentences)"

  the_spiral:
    description: "Return to key concept with deeper understanding"
    use_for: "Discussion sections, theoretical development"
    structure:
      - "Initial concept introduction"
      - "New evidence/perspective"
      - "Revisit concept with enriched meaning"
```

## Application Process

```
┌─────────────────────────────────────────────────────────────────┐
│                 H-Flow-Optimizer Process                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Step 1: Flow Analysis                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Analyze text at all three levels:                        │   │
│  │   - Sentence: length, complexity, opening variation      │   │
│  │   - Paragraph: structure, transitions, evidence flow     │   │
│  │   - Document: progression, balance, cohesion             │   │
│  │                                                          │   │
│  │ Output: Flow analysis report with issue identification   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  Step 2: Pattern Detection                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Identify AI-typical flow patterns:                       │   │
│  │   - Mechanical uniformity                                │   │
│  │   - Formulaic transitions                                │   │
│  │   - Even distribution                                    │   │
│  │                                                          │   │
│  │ Score: Flow Naturalness Index (0-1)                      │   │
│  │   > 0.8 = Natural, < 0.5 = AI-typical                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  Step 3: Transformation Planning                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Prioritize transformations by:                           │   │
│  │   1. Impact on naturalness                               │   │
│  │   2. Minimal meaning disruption                          │   │
│  │   3. Preservation of academic tone                       │   │
│  │                                                          │   │
│  │ Generate transformation queue                            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  Step 4: Transformation Execution                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Apply transformations:                                   │   │
│  │   - Sentence restructuring                               │   │
│  │   - Paragraph rebalancing                                │   │
│  │   - Transition redistribution                            │   │
│  │                                                          │   │
│  │ ⚠️ Preserve: Citations, statistics, key terms           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  Step 5: Flow Verification                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Verify:                                                  │   │
│  │   ✓ Meaning preserved                                   │   │
│  │   ✓ Flow Naturalness Index improved                     │   │
│  │   ✓ Readability maintained or improved                  │   │
│  │   ✓ Academic tone preserved                             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Integration with HAVS

H-Flow-Optimizer activates in HAVS Direction B and C:

```yaml
havs_integration:
  direction_a: false  # Conservative: vocabulary/phrase only
  direction_b: true   # Balanced: includes flow optimization
  direction_c: true   # Aggressive: comprehensive flow restructuring

  interaction_with_other_modules:
    semantic_distance:
      - "Vocabulary changes respect sentence rhythm needs"

    h_style_transfer:
      - "Flow patterns matched to discipline conventions"

    iterative_loop:
      - "Flow naturalness checked in self-review iteration"

  level_activation:
    direction_b:
      - sentence_flow: full
      - paragraph_flow: partial
      - document_flow: minimal

    direction_c:
      - sentence_flow: full
      - paragraph_flow: full
      - document_flow: full
```

## Metrics

```yaml
flow_metrics:
  sentence_level:
    length_cv:
      description: "Coefficient of variation in sentence length"
      target: "> 0.30"
      ai_typical: "< 0.20"

    opening_diversity:
      description: "Unique opening patterns / total sentences"
      target: "> 0.60"
      ai_typical: "< 0.40"

  paragraph_level:
    structure_diversity:
      description: "Unique paragraph structures used"
      target: "> 3 patterns"
      ai_typical: "1-2 patterns"

    transition_distribution:
      description: "Variance in transition placement"
      target: "Mixed positions"
      ai_typical: "Always paragraph-initial"

  document_level:
    section_weight_variance:
      description: "Standard deviation of section lengths"
      target: "> 0.15 of mean"
      ai_typical: "< 0.10 of mean"

    cohesive_device_ratio:
      description: "Implicit / explicit cohesion"
      target: "> 0.40 implicit"
      ai_typical: "< 0.20 implicit"
```

## Output Format

```markdown
## Flow Optimization Report

### Flow Naturalness Index
**Before**: 0.42 (AI-typical patterns detected)
**After**: 0.78 (Natural flow achieved)

### Level Analysis

#### Sentence Level
| Metric | Before | After | Target |
|--------|--------|-------|--------|
| Length CV | 0.15 | 0.35 | > 0.30 |
| Opening Diversity | 0.32 | 0.68 | > 0.60 |
| Complexity Variation | Low | Medium | Medium |

#### Paragraph Level
| Metric | Before | After | Target |
|--------|--------|-------|--------|
| Structure Diversity | 1 pattern | 4 patterns | > 3 |
| Transition Distribution | All initial | Mixed | Mixed |
| Evidence Flow | Mechanical | Organic | Organic |

#### Document Level
| Metric | Before | After | Target |
|--------|--------|-------|--------|
| Section Balance | Even | Weighted | Weighted |
| Cohesive Ratio | 0.15 | 0.45 | > 0.40 |

### Transformations Applied

**Sentence Level (12 changes)**
1. Line 15: Added short sentence for rhythm variation
2. Line 28: Varied sentence opening from "The" to "Among..."
...

**Paragraph Level (5 changes)**
1. Para 3: Restructured to claim-stack pattern
2. Para 5-6: Merged short paragraphs
...

**Document Level (2 changes)**
1. Section 3: Expanded from 15% to 25% (key findings)
2. Conclusion: Added echo to introduction theme
...

### Preserved Elements
- ✓ All citations (14/14)
- ✓ All statistics (8/8)
- ✓ Core meaning
- ✓ Academic formality
```

## Limitations

1. **Genre variation**: Academic genres (empirical, theoretical, review) have different flow norms
2. **Length constraints**: Very short texts have limited transformation options
3. **Collaborative writing**: Multi-author texts may intentionally vary in style
4. **Translation artifacts**: Texts translated to English may have non-standard flow patterns

## References

- Biber, D. (1988). Variation across speech and writing
- Halliday, M.A.K. & Hasan, R. (1976). Cohesion in English
- Grabe, W. & Kaplan, R.B. (1996). Theory and Practice of Writing
