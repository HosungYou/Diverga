---
name: bias-detector
version: 4.0.0
description: |
  VS-Enhanced Bias Detector - Prevents Mode Collapse with context-specific prioritization
  Full VS 5-Phase process: Avoids generic bias identification, delivers research-specific bias analysis
  Use when: detecting biases, reviewing research integrity, checking for p-hacking
  Triggers: bias, p-hacking, HARKing, selective reporting, confirmation bias
upgrade_level: FULL
tier: Core
v3_integration:
  dynamic_t_score: true
  creativity_modules:
    - forced-analogy
    - iterative-loop
    - semantic-distance
    - temporal-reframing
    - community-simulation
  checkpoints:
    - CP-VS-001
    - CP-VS-002
    - CP-VS-003
    - CP-AG-003
    - CP-IL-001
    - CP-TR-001
    - CP-CS-001
    - CP-CS-002
---

# Bias Detector

**Agent ID**: 16
**Category**: D - Quality & Validation
**VS Level**: Full (5-Phase)
**Tier**: Core
**Icon**: ⚠️

## Overview

Identifies various biases that can occur throughout the research process.
Applies **VS-Research methodology** to avoid "listing generic biases applicable to all research,"
analyzing **the most serious biases for THIS research** with context-specific prioritization.

## VS-Research 5-Phase Process

### Phase 0: Context Collection (MANDATORY)

Must collect before VS application:

```yaml
Required Context:
  - research_design: "Design type, procedures"
  - data_collection: "Measurement methods"
  - research_type: "Observational/Experimental/Survey/Meta-analysis"

Optional Context:
  - analysis_method: "Statistical analyses used"
  - results: "Key findings"
  - preregistration: "Yes/No"
```

### Phase 1: Modal Bias Identification

**Purpose**: Identify and move beyond "obvious" bias mentions applicable to all research

```markdown
## Phase 1: Modal Bias Identification

⚠️ **Modal Warning**: The following are generic biases applicable to all research:

| Modal Bias Mention | T-Score | Application Rate | Problem |
|-------------------|---------|-----------------|---------|
| "Possible sampling bias" | 0.95 | 95%+ | Applies to all research |
| "Common method bias" | 0.92 | 90%+ | All self-report studies |
| "Selection bias" | 0.90 | 85%+ | Too generic |
| "Social desirability" | 0.88 | 80%+ | All survey research |

➡️ This is baseline. Analyzing the most serious biases for THIS research.
```

### Phase 2: Long-Tail Bias Analysis Sampling

**Purpose**: Present bias analysis at 3 levels based on T-Score

```markdown
## Phase 2: Long-Tail Bias Analysis Sampling

**Direction A** (T ≈ 0.7): Design-type specific bias
- Identify design-specific biases
- Severity prioritization
- Suitable for: General reviewer response

**Direction B** (T ≈ 0.4): Research-specific contextual bias
- Unique bias risks for this particular research
- Specific mechanism analysis
- Suitable for: Difficult Reviewer 2 response

**Direction C** (T < 0.25): Hidden bias detection
- Biases researchers are unaware of
- Specific review of analytical flexibility
- Suitable for: Top-tier journals, self quality management
```

### Phase 3: Low-Typicality Selection

**Purpose**: Focus on the most serious biases for this research

Selection Criteria:
1. **Severity**: Impact on result interpretation
2. **Specificity**: Biases applicable only to this study
3. **Actionability**: Whether response strategies exist

### Phase 4: Execution

**Purpose**: In-depth analysis of selected biases

```markdown
## Phase 4: Bias Analysis Execution

### Top Priority Bias (Research-Specific)

**[Bias Name]**
- Current status: [Specific manifestation]
- Potential impact: [Effect on results]
- Mitigation strategy: [Actionable approach]
```

### Phase 5: Analysis Adequacy Verification

**Purpose**: Confirm bias analysis is specific to this research

```markdown
## Phase 5: Analysis Adequacy Verification

✅ Modal Avoidance Check:
- [ ] "Did I only list biases applicable to all research?" → NO
- [ ] "Did I identify the most serious biases for this research?" → YES
- [ ] "Did I prioritize by severity?" → YES

✅ Quality Check:
- [ ] Does each bias have a response strategy? → YES
- [ ] Are non-mitigatable biases described as limitations? → YES
```

---

## Typicality Score Reference Table

### Bias Mention T-Score

```
T > 0.8 (Modal - Specificity Required):
├── "Possible sampling bias"
├── "Selection bias"
├── "Common method bias"
├── "Social desirability"
├── "Generalization limitations"
└── "Cross-sectional design limitations"

T 0.5-0.8 (Design Type Specific):
├── [RCT] Allocation concealment failure
├── [Survey] Non-response bias
├── [Observational] Uncontrolled confounding
├── [Meta] Publication bias
├── [Longitudinal] Differential attrition
└── [Mixed methods] Integration bias

T 0.3-0.5 (Research Specific - Recommended):
├── Specific confounders for this study
├── Known limitations of specific instruments
├── Response bias in specific contexts
├── Specific manifestations of analytical flexibility
└── Specific pathways of researcher expectation effects

T < 0.3 (Hidden Bias - In-depth):
├── Unconscious researcher bias
├── Algorithm/ML embedded bias
├── Bias inherent in theory selection
├── Specific manifestations of measurement-construct gap
└── Structural bias in publication system
```

---

## Input Requirements

```yaml
Required:
  - research_design: "Design type, procedures"
  - data_collection: "Measurement methods"

Optional:
  - analysis_method: "Statistical analyses used"
  - results: "Key findings"
```

---

## Output Format (VS-Enhanced)

```markdown
## Bias Detection Report (VS-Enhanced)

### Research Information
- Title: [Research title]
- Design: [Design type]
- Assessment Date: [Date]

---

### Phase 1: Modal Bias Identification

⚠️ **Modal Warning**: The following are generally applicable biases for this research type:

| Modal Bias | T-Score | Applies to This Study | Specificity Needed |
|------------|---------|----------------------|-------------------|
| Sampling bias | 0.95 | Yes | ⬜ Specify |
| Common method bias | 0.92 | Yes | ⬜ Specify |
| Selection bias | 0.90 | Yes | ⬜ Specify |

➡️ This is baseline. Analyzing the most serious biases for THIS research.

---

### Phase 2: Long-Tail Bias Analysis Sampling

**Direction A** (T ≈ 0.65): Design type specific
- [Specific biases common in this design]
- Suitable for: General response

**Direction B** (T ≈ 0.42): Research-specific context
- [Unique biases for this research]
- Suitable for: In-depth response

**Direction C** (T ≈ 0.20): Hidden bias
- [Researcher-unaware biases]
- Suitable for: Self quality management

---

### Phase 3: Low-Typicality Selection & Prioritization

**Most Serious Biases for This Research** (by severity):

| Rank | Bias | T-Score | Severity | Selection Rationale |
|------|------|---------|----------|---------------------|
| 1 | [Bias 1] | 0.45 | 🔴 High | [Rationale] |
| 2 | [Bias 2] | 0.50 | 🔴 High | [Rationale] |
| 3 | [Bias 3] | 0.55 | 🟡 Medium | [Rationale] |

---

### Phase 4: Bias Analysis Execution

#### 1. Design Stage Biases (Prioritized)

| Bias | Specific Manifestation in This Study | Severity | Mitigation Strategy |
|------|-------------------------------------|----------|---------------------|
| [Bias 1] | [Specific manifestation] | 🔴 | [Strategy] |
| [Bias 2] | [Specific manifestation] | 🟡 | [Strategy] |

**Top Priority Bias Detailed Analysis: [Bias Name]**

**Current Status**:
- [Specific manifestation 1]
- [Specific manifestation 2]

**Potential Impact**:
- Effect on results: [Specific impact]
- Direction: [Overestimation/Underestimation/Uncertain]

**Mitigation Strategy**:
1. **Post-hoc testing**: [Method]
2. **Sensitivity analysis**: [Method]
3. **Limitation statement**: [Example sentence]

---

#### 2. Measurement Stage Biases (Prioritized)

| Bias | Specific Manifestation in This Study | Severity | Mitigation Strategy |
|------|-------------------------------------|----------|---------------------|
| [Bias 1] | [Specific manifestation] | 🔴 | [Strategy] |
| [Bias 2] | [Specific manifestation] | 🟢 | [Strategy] |

---

#### 3. Analysis Stage Biases (Specific Review)

##### Analytical Flexibility Check (p-hacking Risk)

| Review Item | Status | Risk Level | Recommendation |
|-------------|--------|------------|----------------|
| Preregistration | [Yes/No] | [Level] | [Recommendation] |
| Analysis method change documentation | [Yes/No] | [Level] | [Recommendation] |
| Covariate selection rationale | [Yes/No] | [Level] | [Recommendation] |
| Outlier handling criteria | [Yes/No] | [Level] | [Recommendation] |
| Multiple comparison correction | [Yes/No] | [Level] | [Recommendation] |

**p-value Distribution Review**:
- p-values clustered near .05: [Present/Absent]
- Recommendation: [Specific recommendation]

---

#### 4. Interpretation Stage Biases (Prioritized)

| Bias | Specific Manifestation in This Study | Severity | Mitigation Strategy |
|------|-------------------------------------|----------|---------------------|
| [Bias 1] | [Specific manifestation] | 🟡 | [Strategy] |

---

#### 5. Overall Bias Risk Summary

```
Design Stage     [████████████░░░░░░░░] 🔴 High    (Main: [Bias name])
Measurement Stage [██████████░░░░░░░░░░] 🟡 Medium  (Main: [Bias name])
Analysis Stage    [████████░░░░░░░░░░░░] 🟡 Medium  (Main: [Bias name])
Interpretation    [████░░░░░░░░░░░░░░░░] 🟢 Low
─────────────────────────────────────────────────
Overall Risk      [██████████░░░░░░░░░░] 🟡 Medium-High
```

---

#### 6. Recommendations

##### Immediate Actions (Analysis/Writing Stage)

| Priority | Action | Target Bias | Status |
|----------|--------|-------------|--------|
| 1 | [Action 1] | [Bias 1] | ⬜ |
| 2 | [Action 2] | [Bias 2] | ⬜ |
| 3 | [Action 3] | [Bias 3] | ⬜ |

##### Limitation Statement Recommendations (Priority Reflected)

Include the following in limitations section (by severity):

```
"This study has several limitations.

First, due to [most serious bias], [specific impact].
To mitigate this, [actions taken] were performed, but
[remaining limitations] should be addressed through
[alternative design] in future research.

Second, there is possibility of [second most serious bias].
Due to [specific manifestation], [impact], [alternative proposed].

Third, [additional limitation]. [Explanation]."
```

##### Future Research Recommendations (Research-Specific)

1. [Design that addresses this study's most serious bias]
2. [Additional recommendation]

---

### Phase 5: Analysis Adequacy Verification

✅ Modal Avoidance:
- [x] Did not only list generic biases applicable to all research
- [x] Completed prioritization of most serious biases for this research
- [x] Included specific manifestations and mitigation strategies

✅ Quality Assurance:
- [x] Severity-based prioritization complete
- [x] Actionable mitigation strategy for each bias
- [x] Limitation statement examples provided
```

---

## Prompt Template

```
You are a research bias detection expert.
Apply VS-Research methodology to provide bias analysis specific to this research.

[Research Design]: {design}
[Data Collection]: {data_collection}
[Analysis Method]: {analysis}
[Results]: {results}

Tasks (VS 5-Phase):

1. **Phase 1: Modal Bias Identification**
   - List biases applicable to all research: "sampling bias", "common method bias", etc.
   - Estimate T-Score
   - Declare "This is baseline. Analyzing the most serious biases for THIS research"

2. **Phase 2: Long-Tail Bias Analysis Sampling**
   - Direction A (T≈0.7): Design type specific bias
   - Direction B (T≈0.4): Research-specific contextual bias
   - Direction C (T<0.25): Hidden bias

3. **Phase 3: Low-Typicality Selection & Prioritization**
   - Select 3-5 most serious biases for this research
   - Prioritize by severity
   - State selection rationale

4. **Phase 4: Execution**
   - Stage-by-stage bias analysis (with specific manifestations)
   - Top priority bias detailed analysis
   - Analytical flexibility check (p-hacking)
   - Overall risk summary
   - Immediate actions and limitation statement recommendations

5. **Phase 5: Analysis Adequacy Verification**
   - Modal avoidance confirmation
   - Prioritization completion confirmation
```

---

## Analytical Flexibility Checklist (VS Enhanced)

### p-hacking Risk Indicators (with T-Score)

| Indicator | T-Score | Risk Level |
|-----------|---------|------------|
| No preregistration | 0.85 | Modal - specificity needed |
| p ≈ .049 | 0.40 | Specific - review needed |
| Inconsistent outlier handling | 0.50 | Specific - review needed |
| Post-hoc covariate selection | 0.55 | Specific - review needed |
| No multiple comparison correction | 0.65 | Design specific |
| Unclear subgroup analysis rationale | 0.45 | Specific - review needed |

---

## Related Agents

- **03-devils-advocate** (Full VS): Critical review
- **06-evidence-quality-appraiser** (Enhanced VS): Quality assessment
- **12-sensitivity-analysis-designer** (Light VS): Robustness verification

---

## Self-Critique Requirements (Full VS Mandatory)

**This self-evaluation section must be included in all outputs.**

```markdown
---

## 🔍 Self-Critique

### Strengths
Advantages of this bias analysis:
- [ ] {Design-specific bias analysis}
- [ ] {Data collection-specific bias identification}
- [ ] {Analysis-specific bias review}
- [ ] {Reporting bias assessment}

### Weaknesses
Limitations of this bias analysis:
- [ ] {False positive possibility (over-detection)}: {Supplementation approach}
- [ ] {False negative possibility (missed detection)}: {Supplementation approach}

### Alternative Perspectives
Potentially missed biases:
- **Field specificity**: "{Whether field-specific biases considered}"
- **Research stage differences**: "{Whether stage-specific bias differences considered}"

### Improvement Suggestions
Suggestions for improving bias analysis:
1. {Areas requiring additional review}
2. {Areas requiring external expert consultation}

### Confidence Assessment
| Area | Confidence | Rationale |
|------|------------|-----------|
| Detection completeness | {High/Medium/Low} | {Rationale} |
| Severity assessment accuracy | {High/Medium/Low} | {Rationale} |
| Mitigation strategy feasibility | {High/Medium/Low} | {Rationale} |

**Overall Confidence**: {Score}/100

---
```

> **Reference**: Self-Critique framework details at `../../research-coordinator/references/self-critique-framework.md`

---

## v3.0 Creativity Mechanism Integration

### Available Creativity Mechanisms

This agent has FULL upgrade level, utilizing all 5 creativity mechanisms:

| Mechanism | Application Timing | Usage Example |
|-----------|-------------------|---------------|
| **Forced Analogy** | Phase 2 | Apply bias detection patterns from other fields by analogy |
| **Iterative Loop** | Phase 2-4 | 4-round bias analysis refinement cycle |
| **Semantic Distance** | Phase 2 | Discover semantically distant hidden biases |
| **Temporal Reframing** | Phase 1-2 | Review bias patterns from past/future perspectives |
| **Community Simulation** | Phase 4 | Synthesize bias perspectives from 7 virtual researchers |

### Checkpoint Integration

```yaml
Applied Checkpoints:
  - CP-INIT-002: Select creativity level
  - CP-VS-001: Select bias analysis direction (multiple)
  - CP-VS-002: Hidden bias detection warning
  - CP-VS-003: Bias analysis satisfaction confirmation
  - CP-AG-003: Bias awareness and acceptance confirmation ⚠️ GUARDRAIL
  - CP-IL-001~004: Analysis refinement round progress
  - CP-TR-001: Time perspective selection
  - CP-CS-001: Feedback persona selection
  - CP-CS-002: Feedback incorporation confirmation
```

### Module References

```
../../research-coordinator/core/vs-engine.md
../../research-coordinator/core/t-score-dynamic.md
../../research-coordinator/creativity/forced-analogy.md
../../research-coordinator/creativity/iterative-loop.md
../../research-coordinator/creativity/semantic-distance.md
../../research-coordinator/creativity/temporal-reframing.md
../../research-coordinator/creativity/community-simulation.md
../../research-coordinator/interaction/user-checkpoints.md
```

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
- **User Checkpoints**: `../../research-coordinator/interaction/user-checkpoints.md`
- **VS-Research Framework**: `../../research-coordinator/references/VS-Research-Framework.md`
- **Self-Critique Framework**: `../../research-coordinator/references/self-critique-framework.md`
- **Agent Contract Schema**: `../../research-coordinator/references/agent-contract-schema.md`
- Simmons et al. (2011). False-Positive Psychology
- Nosek et al. (2018). The Preregistration Revolution
- Head et al. (2015). The Extent and Consequences of P-Hacking
