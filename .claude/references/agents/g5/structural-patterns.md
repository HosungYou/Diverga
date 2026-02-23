# Structural Detection Patterns (S7-S10)

## Overview

These four structural patterns were discovered through empirical humanization of two academic papers (Paper 1: Occupational Identity Threat, TFSC; Paper 2: Epistemic Cognition, IJAIED). After vocabulary-level patterns were cleaned in Rounds 1-2 (scores dropped from 80%/82% to 62%/61%), the remaining AI probability came almost entirely from structural patterns that word-level humanizers cannot address.

The breakthrough Round 3 (scores dropped to 31%/22%) was achieved by manually dismantling these structural patterns. G5 v2.0 now detects them to guide automated structural transformation in G6.

**Version**: 2.0.0
**Reference**: https://github.com/HosungYou/humanizer

---

## S7: Enumeration as Prose

**Weight**: 12
**Risk**: HIGH
**Category**: Style (Structural)

### Definition

Ordinal markers ("First,...Second,...Third,...Finally,...") embedded within flowing paragraph text, creating a hidden numbered list disguised as prose. This is distinct from S3 (Inline-Header Lists) which covers explicit formatted lists. S7 targets the subtler pattern where enumeration lives inside paragraphs that appear to be continuous prose but follow a rigid sequential structure.

This is one of the most persistent AI structural fingerprints. It survives vocabulary-level paraphrasing because the ordinal structure is preserved even when individual words are replaced.

### Detection Rules

Scan for 3 or more of the following sequential ordinal markers within a single section or across consecutive paragraphs:

**English markers**:
- Explicit ordinals: "First,", "Second,", "Third,", "Fourth,", "Finally,"
- Implicit ordinals: "Additionally,", "Moreover,", "Furthermore," used as sequential connectors
- Numeric preambles: "There are N key [findings/contributions/implications/recommendations]" followed by enumeration
- Contribution claims: "This study makes N contributions" followed by "First,...Second,..."

**Korean markers**:
- 첫째, 둘째, 셋째, 넷째, 마지막으로
- 첫 번째로, 두 번째로, 세 번째로

**Aggravating factors** (increase weight by 1.5x):
- 4 or more sequential ordinals in the same passage
- Enumeration spans multiple paragraphs where each paragraph is one enumerated point
- Combined with "N contributions/findings/implications" preamble

### Example: Violation

```
Education significantly predicted AI concern in three ways. First, higher
education was associated with greater awareness of AI capabilities.
Second, educational attainment correlated with more nuanced understanding
of automation risks. Third, the education-concern relationship was
moderated by partisan identity, suggesting that educational effects
operate differently across political contexts.
```

**What makes this AI-like**: The rigid First/Second/Third skeleton creates a predictable structure. Each point follows the same syntactic template (subject + verb + object + qualifier). A human writer would weave these observations together with varying connective tissue.

### Example: Fix (Narrative Alternative)

```
Education mattered, but not in the straightforward way we expected.
People with college degrees were more likely to know what large language
models actually do -- and that awareness amplified their concern. Yet
the relationship fractured along partisan lines. Among Democrats,
education strengthened worry about job displacement. Among Republicans,
it did the opposite. That interaction was the finding we did not
anticipate.
```

**What makes this human-like**: No ordinal markers. The narrative builds through cause-and-effect connections, includes a short emphatic sentence ("Education mattered"), introduces surprise ("not in the straightforward way we expected"), and varies sentence length dramatically (7 words to 24 words).

### Edge Cases

- **Methods sections**: Sequential procedural steps ("First, participants completed... Second, they were randomly assigned...") are acceptable in Methods because the sequential structure reflects actual temporal ordering of procedures. Apply 0.5x weight reduction in Methods sections.
- **Numbered lists with explicit formatting**: If the text uses actual numbered lists (1. / 2. / 3.), this is S3 (Inline-Header Lists), not S7. S7 specifically targets enumeration disguised as prose.

---

## S8: Repetitive Paragraph Openers

**Weight**: 10
**Risk**: HIGH
**Category**: Style (Structural)

### Definition

More than 3 paragraphs within the same section starting with the same syntactic pattern. The most common AI pattern is "The [noun]..." where each paragraph opens with a different noun but the same syntactic frame:

- "The results for education..."
- "The partisan gap..."
- "The interaction between age and awareness..."
- "The Blinder-Oaxaca decomposition..."

This creates a rhythmic monotony that human writers instinctively avoid.

### Detection Rules

1. Extract the first 3 words of each paragraph in every section
2. Normalize by removing articles for comparison (e.g., "The results showed" and "The analysis revealed" both match "The [X] [verb]")
3. Flag if >3 paragraphs in a single section share the same opening pattern

**Common repetitive patterns to detect**:
- "The [noun] [verb]..." (most common)
- "[Noun] [verb] that..."
- "In [context],..."
- "This [noun] [verb]..."
- "Our [noun] [verb]..."
- "These [noun] [verb]..."

**Severity scaling**:
- 3 matching openers: base weight (10)
- 4 matching openers: weight x 1.3
- 5+ matching openers: weight x 1.6

### Example: Violation

```
The results for education revealed a significant positive association
with AI concern (beta = 0.23, p < .001)...

The partisan gap emerged as the strongest predictor in the model,
with Republicans showing 14 percentage points higher concern...

The interaction between age and awareness complicated the picture,
as older respondents who had heard of ChatGPT expressed less concern...

The Blinder-Oaxaca decomposition showed that demographic differences
explained only 31% of the partisan gap...

The sensitivity analysis using alternative model specifications
confirmed the robustness of these findings...
```

**What makes this AI-like**: Every paragraph starts with "The [noun phrase]..." creating a metronomic rhythm. The reader can predict the opening structure before reading each paragraph.

### Example: Fix (Varied Openers)

```
Education's role proved more complicated than a simple linear gradient.
Each additional year of schooling raised concern by roughly 2 percentage
points -- but only among respondents who had actually heard of ChatGPT...

What explains the partisan gap? Not demographics alone. Even after
adjusting for age, income, education, and region, Republicans remained
14 points more concerned about job displacement...

Age and awareness interacted in ways that complicate any simple
generational narrative. Among the aware, older Americans worried less,
not more...

Decomposing the partisan gap revealed something unexpected: fully 69%
of the difference could not be attributed to observable characteristics...

None of these patterns dissolved when we switched model specifications.
The sensitivity analysis confirmed every major finding...
```

**What makes this human-like**: Five different opening strategies -- a noun phrase, a question, a subject-verb pair, a gerund phrase, and a pronoun. The reader cannot predict the next paragraph's opening.

---

## S9: Formulaic Section Structure

**Weight**: 8
**Risk**: MEDIUM
**Category**: Style (Structural)

### Definition

The Discussion section follows a rigid, predictable template without deviation:

1. **Restate**: Summarize findings ("The present study examined... Our results showed...")
2. **Compare**: Relate to prior literature ("Consistent with prior research by [Author]...")
3. **Implications**: State practical significance ("These findings have implications for...")
4. **Limitations**: Acknowledge weaknesses ("Several limitations warrant acknowledgment...")
5. **Future**: Suggest next steps ("Future research should...")

Each subsection or major paragraph mechanically follows this sequence, and the Discussion as a whole follows this exact order. Human-written Discussions often deviate -- starting with a provocative question, weaving limitations into the findings narrative, or building an argument that does not follow the canonical order.

### Detection Rules

Analyze the Discussion section for the following rhetorical move sequence:

1. **Restate markers**: "The present study examined", "Our findings showed", "This study found", "The results demonstrated"
2. **Compare markers**: "Consistent with", "In line with", "Contrary to", "This aligns with", "Prior research by [Author] also found"
3. **Implications markers**: "These findings have implications for", "Practically, this means", "For practitioners", "These results suggest that policymakers"
4. **Limitations markers**: "Several limitations", "This study is not without limitations", "Future research should address", "One limitation is"
5. **Future markers**: "Future research should", "Further investigation is needed", "Subsequent studies could"

**Scoring**:
- All 5 moves in exact canonical order: full weight (8)
- 4 of 5 in order: weight x 0.7
- 3 of 5 in order: weight x 0.4
- Additional penalty (+3) if each subsection internally repeats the restate-compare-imply pattern

### Example: Violation

```
## Discussion

The present study examined the relationship between partisan identity
and AI concern. Our results showed that Republicans expressed
significantly higher concern about job displacement.

These findings are consistent with prior research on partisan
differences in technology attitudes (Author1, 2023; Author2, 2024).
However, the magnitude of the gap exceeded that reported by Author3
(2022).

These findings have important implications for policymakers designing
workforce transition programs. Programs should account for partisan
differences in receptivity to retraining initiatives.

Several limitations warrant acknowledgment. First, the cross-sectional
design prevents causal inference. Second, self-reported concern may
differ from behavioral responses to automation.

Future research should employ longitudinal designs to track how
partisan AI attitudes evolve. Additionally, experimental methods
could test whether framing effects moderate the partisan gap.
```

**What makes this AI-like**: Textbook restate-compare-implications-limitations-future sequence. Each paragraph serves exactly one rhetorical function. The transitions are formulaic ("These findings are consistent with", "Several limitations warrant acknowledgment").

### Example: Fix (Non-Formulaic Discussion)

```
## Discussion

Why do Democrats and Republicans -- who agree on almost nothing --
both worry about AI at nearly identical rates? That is the puzzle this
study did not set out to solve, yet it may be the most important finding
we report.

The partisan gap we predicted materialized. Republicans were 14
percentage points more likely to express concern about job displacement.
But the gap shrank to statistical noise when we restricted the sample
to respondents who had never heard of ChatGPT. That conditional pattern
complicates the interpretation considerably -- and it is one that neither
Author1 (2023) nor Author2 (2024) had the data to test...

We cannot make causal claims from a cross-sectional survey, and we
suspect that the framing of our concern question biased responses
toward economic threats rather than social ones. A longitudinal design
tracking the same respondents across the next two years of AI deployment
would help, but the question we most want answered is whether actual
job loss changes partisan attitudes or simply hardens them.
```

**What makes this human-like**: Opens with a question, not a summary. Limitations are woven into the findings narrative rather than isolated in a separate section. Future research arises naturally from the limitations discussion. The author's voice and intellectual curiosity are present throughout.

---

## S10: Hypothesis Checklist Pattern

**Weight**: 10
**Risk**: HIGH
**Category**: Style (Structural)

### Definition

Sequential hypothesis confirmation statements presented as a mechanical checklist:

- "H1 was supported (p < .001)."
- "H2 was partially supported."
- "H3 was not supported."

This pattern appears in Discussion sections and sometimes in Results. It reduces complex empirical findings to binary verdicts, losing the narrative thread that connects hypotheses to each other and to the broader research question.

### Detection Rules

Scan for sequential hypothesis labels followed by support verdicts:

**Hypothesis labels**:
- H1, H2, H3, H4, H5 (or higher)
- Hypothesis 1, Hypothesis 2, Hypothesis 3
- "Our first hypothesis", "Our second hypothesis"

**Support verdicts**:
- "was supported"
- "was partially supported"
- "was not supported"
- "was confirmed"
- "was rejected"
- "received support"
- "did not receive support"

**Trigger threshold**: 3 or more sequential hypothesis verdicts within the same section or across consecutive paragraphs.

**Aggravating factors** (increase weight by 1.5x):
- All hypotheses listed in a single paragraph
- Verdicts use identical syntactic structure ("H[N] was [verdict]")
- No narrative connecting the hypothesis outcomes to each other

### Example: Violation

```
H1 predicted that education would positively predict AI concern.
This hypothesis was supported (beta = 0.23, p < .001).

H2 predicted that partisan identity would moderate the
education-concern relationship. This hypothesis was partially
supported; the interaction was significant for Republicans
(p = .03) but not for Democrats (p = .41).

H3 predicted that AI awareness would mediate the age-concern
relationship. This hypothesis was not supported; the indirect
effect was non-significant (beta = 0.02, 95% CI [-0.01, 0.05]).

H4 predicted that occupational identity threat would predict
concern above and beyond demographic controls. This hypothesis
was supported (delta R-squared = .04, p < .01).

H5 predicted that the partisan gap would be larger for blue-collar
workers. This hypothesis was not supported (interaction p = .67).
```

**What makes this AI-like**: Five hypotheses presented in identical format -- label, prediction restatement, verdict, evidence in parentheses. A reader can predict the structure of H3 after reading H1 and H2. The findings are treated as isolated verdicts rather than a coherent narrative.

### Example: Fix (Narrative Alternative)

```
The partisan divide we predicted materialized clearly --
Republicans were 14 percentage points more likely to express
concern (AME = 0.14, p < .001). But the education gradient
surprised us. We expected a simple positive slope, and the
aggregate data delivered one (beta = 0.23, p < .001). Look
closer, though, and the slope fractures along party lines.
Among Democrats, each additional year of education increased
concern. Among Republicans, it had no detectable effect. That
interaction -- which we had not hypothesized -- may be the most
substantively interesting pattern in the data.

Two predictions fell flat. We thought AI awareness would explain
why younger people worried more, but the mediation path was a
dead end (indirect effect: 0.02, 95% CI crossing zero). And the
blue-collar amplification hypothesis? The interaction term was
nowhere close to significance (p = .67). Whatever drives the
partisan gap, it is not concentrated in the occupations most
directly threatened by automation.

What did hold up was the role of occupational identity threat.
Even after controlling for demographics, job characteristics,
and political variables, threat perceptions added 4% of explained
variance (p < .01). That is a modest but real increment -- and it
suggests that how people feel about their professional identity
matters independently of how likely their job actually is to be
automated.
```

**What makes this human-like**: Hypotheses are grouped thematically (partisan divide, null findings, identity threat) rather than sequentially (H1, H2, H3, H4, H5). The narrative builds an argument -- surprise, complication, resolution. Statistical evidence is woven into sentences rather than parenthesized at the end of verdict statements. The author's voice is present ("surprised us", "fell flat", "a dead end"). Short sentences create emphasis ("That is a modest but real increment").

---

## Cross-Pattern Interactions

Structural patterns often co-occur, amplifying each other:

| Combination | Interaction | Bonus |
|-------------|-------------|-------|
| S7 + S10 | Enumerated hypotheses in prose | +8 |
| S8 + S9 | Repetitive openers within formulaic structure | +5 |
| S7 + S8 | Enumeration with repetitive paragraph starts | +6 |
| S7 + S8 + S9 + S10 | Full structural AI fingerprint | +15 |

When all four structural patterns appear in the same document, the combined signal is extremely strong evidence of AI generation. In the empirical case studies, this full combination was present in both papers at Round 1 (80%/82% AI probability).

---

## Relationship to Other Patterns

| Structural Pattern | Related Original Pattern | Distinction |
|--------------------|-------------------------|-------------|
| S7 (Enumeration as Prose) | S3 (Inline-Header Lists) | S3 = formatted lists; S7 = hidden enumeration in prose |
| S8 (Repetitive Openers) | Pattern #18 (Repetitive sentence starts) | #18 = sentence level; S8 = paragraph level |
| S9 (Formulaic Structure) | A5 (Discussion Formula) | A5 = presence of formula; S9 = rigid adherence to canonical order |
| S10 (Hypothesis Checklist) | A5 (Contribution Enumeration) | A5 = contributions listed; S10 = hypothesis verdicts listed |

---

## Version History

- **v2.0.0**: Initial structural pattern definitions based on empirical humanization rounds
