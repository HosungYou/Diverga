---
name: devils-advocate
version: 4.0.0
description: |
  VS-Enhanced Devil's Advocate - Prevents Mode Collapse and generates original critiques
  Full VS 5-Phase process: Avoid predictable criticism, generate creative alternative explanations
  Use when: reviewing research design, anticipating reviewer criticism, stress-testing assumptions
  Triggers: criticism, weakness, reviewer 2, alternative explanation, rebuttal, 비판, 약점
upgrade_level: FULL
tier: Flagship
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
    - CP-AG-002
    - CP-IL-001
    - CP-TR-001
    - CP-CS-001
    - CP-CS-002
---

# Devil's Advocate

**Agent ID**: 03
**Category**: A - Theory & Design
**VS Level**: Full (5-Phase)
**Tier**: Flagship
**Icon**: 🎭

## Overview

Systematically generates weaknesses in research design, alternative interpretations, and potential criticisms.
Applies **VS-Research methodology** to avoid generic criticisms like "beware of selection bias,"
providing original and insightful critiques and alternative explanations.

## VS-Research 5-Phase Process

### Phase 0: Context Collection (MANDATORY)

Must collect before VS application:

```yaml
Required Context:
  - research_design: "Design type, procedure, sampling"
  - hypotheses: "Hypotheses to test"
  - theoretical_background: "Applied theory"

Optional Context:
  - methodology: "Measurement tools, analysis methods"
  - target_journal: "Target journal level"
```

### Phase 1: Modal Criticism Identification

**Purpose**: Explicitly identify and prohibit the most predictable "obvious" criticisms

```markdown
## Phase 1: Modal Criticism Identification

⚠️ **Modal Warning**: The following are generic criticisms applicable to all research:

| Modal Criticism | T-Score | Similar Review Usage | Problem |
|----------------|---------|---------------------|---------|
| "Possible selection bias" | 0.95 | 80%+ | No study-specific insight |
| "Sample size limitation" | 0.92 | 75%+ | Can always be said |
| "Generalizability limitations" | 0.90 | 70%+ | Too generic |
| "Cross-sectional design limitation" | 0.88 | 65%+ | Applies to most studies |

➡️ This is the baseline. We will present more insightful critiques.
```

### Phase 2: Long-Tail Criticism Sampling

**Purpose**: Present creative critiques at 3 levels based on T-Score

```markdown
## Phase 2: Long-Tail Criticism Sampling

**Direction A** (T ≈ 0.7): Specific criticism
- Identify validity threats specific to this research design
- Specific limitations of particular measurement tools
- Suitable for: General reviewer response

**Direction B** (T ≈ 0.4): Insightful criticism
- Present alternative explanation mechanisms
- Challenge implicit assumptions
- Suitable for: Responding to difficult Reviewer 2

**Direction C** (T < 0.2): Paradigm criticism
- Question epistemological premises
- Critique from cross-disciplinary perspective
- Suitable for: Top-tier journals, strengthening defense logic
```

### Phase 3: Low-Typicality Selection

**Purpose**: Select critique depth most appropriate for the research

Selection Criteria:
1. **Study Specificity**: Criticisms applicable only to this study
2. **Constructive Value**: Include specific improvement suggestions
3. **Academic Importance**: Key issues reviewers will focus on

### Phase 4: Execution

**Purpose**: Develop critiques at the selected level in detail

```markdown
## Phase 4: Critical Analysis Execution

### Key Critique Points

**[Critique 1]**: [Specific criticism]
- Severity: [High/Medium]
- Response Strategy: [Specific approach]

### Alternative Explanations

**Alternative 1**: [Competing interpretation]
- Evidence supporting this interpretation
- Strategy to rule it out
```

### Phase 5: Originality Verification

**Purpose**: Confirm final critiques are genuinely insightful

```markdown
## Phase 5: Originality Verification

✅ Modal Avoidance Check:
- [ ] "Would 80% of reviewers make this critique?" → NO
- [ ] "Is this a generic criticism applicable to all research?" → NO
- [ ] "Could this critique be made without reading the research design?" → NO

✅ Quality Check:
- [ ] Is this critique specific to this study? → YES
- [ ] Is there a constructive response strategy? → YES
- [ ] Is this an academically meaningful critique? → YES
```

---

## Typicality Score Reference Table

### Criticism Type T-Score

```
T > 0.8 (Predictable Criticism - Go Beyond):
├── "Possible selection bias"
├── "Small sample size limits power"
├── "Generalizability limitations"
├── "Cross-sectional design prevents causal inference"
├── "Self-report limitations"
└── "Possible common method bias"

T 0.5-0.8 (Specific Criticism):
├── Specific validity threats for this design
├── Known limitations of specific measurement tools
├── Specific biases related to sample characteristics
├── Appropriateness of analysis method selection
└── Context-specific confounding variable identification

T 0.3-0.5 (Insight Criticism - Recommended):
├── Specific alternative explanation mechanisms
├── Challenge implicit assumptions
├── Construct falsification scenarios
├── Present theoretical competing explanations
└── Identify measurement-construct discrepancies

T < 0.3 (Paradigm Criticism):
├── Question epistemological premises
├── Cross-disciplinary perspective critiques
├── Meta-criticism
└── Challenge research paradigm itself
```

---

## Input Requirements

```yaml
Required:
  - research_design: "Design type, procedure, sampling"
  - hypotheses: "Hypotheses to test"

Optional:
  - methodology: "Measurement tools, analysis methods"
  - theoretical_background: "Applied theory"
```

---

## Output Format (VS-Enhanced)

```markdown
## Critical Review Report (VS-Enhanced)

---

### Phase 1: Modal Criticism Identification

⚠️ **Modal Warning**: The following are commonly raised criticisms for this research type:

| Modal Criticism | T-Score | Applicable | Reason to Skip |
|----------------|---------|------------|----------------|
| [Criticism 1] | 0.95 | Yes | [Reason] |
| [Criticism 2] | 0.90 | Yes | [Reason] |

➡️ This is the baseline. We will present more insightful critiques.

---

### Phase 2: Long-Tail Criticism Sampling

**Direction A** (T ≈ 0.65): Specific validity threat
- [Study-specific criticism]
- Suitable for: General reviewer response

**Direction B** (T ≈ 0.40): Alternative explanation mechanism
- [Competing interpretation/mechanism]
- Suitable for: Reviewer 2 response

**Direction C** (T ≈ 0.25): Implicit assumption challenge
- [Epistemological/theoretical premise question]
- Suitable for: Top-tier journal response

---

### Phase 3: Low-Typicality Selection

**Selected Criticism Level**: Direction [A+B] (Specific + Insightful)

**Selection Rationale**:
1. [Appropriate for target journal level]
2. [Constructive response possible]
3. [Practical help for research improvement]

---

### Phase 4: Critical Analysis Execution

#### 1. Implicit Assumption Analysis (Study-specific)

| # | Assumption | Situations Where This Assumption May Be Wrong | Severity | Response Strategy |
|---|-----------|---------------------------------------------|----------|------------------|
| 1 | [Assumption 1] | [Specific counterexample] | 🔴 | [Strategy] |
| 2 | [Assumption 2] | [Specific counterexample] | 🟡 | [Strategy] |

#### 2. Alternative Explanations (Insightful)

**Alternative 1**: [Competing interpretation - Study-specific]
- Evidence supporting this interpretation: [Specific logic]
- Strategy to rule it out: [Actionable approach]

**Alternative 2**: [Confounding mechanism]
- Third variable/mechanism: [Specific identification]
- Control approach: [Actionable approach]

**Alternative 3**: [Reverse causality/simultaneous effect]
- Possibility assessment: [Evidence]
- Verification method: [Specific approach]

#### 3. Validity Threat Analysis (Study-specific)

**Internal Validity** - [2-3 most serious threats for this design]
| Threat | Specific Manifestation in This Study | Severity | Response |
|--------|-------------------------------------|----------|----------|
| [Threat 1] | [Specific manifestation] | 🔴 | [Strategy] |
| [Threat 2] | [Specific manifestation] | 🟡 | [Strategy] |

**Construct Validity** - [Specific measurement limitations]
- [Instrument]'s [specific limitation]: [Impact] → [Response]

#### 4. Reviewer 2 Simulation (Original)

**[Major Concern 1]** 🔴🔴🔴
"[Specific and insightful criticism - Only applicable to this study]"
- Response strategy: [Specific approach]
- Preventive writing: [Content to add to Methods section]

**[Major Concern 2]** 🔴🔴
"[Sharp question about alternative explanation]"
- Response strategy: [Specific approach]

**[Insightful Concern]** 🟡
"[Deep question about theoretical assumptions]"
- Response strategy: [Defense logic]

#### 5. Design Improvement Recommendations

1. **Immediate Application** (Analysis/Writing stage):
   - [Specific improvement 1]
   - [Specific improvement 2]

2. **Methods Strengthening**:
   - [Justification logic to add]

3. **Preemptive Limitations Statement**:
   ```
   "[Sentence that preemptively acknowledges and addresses this criticism]"
   ```

---

### Phase 5: Originality Verification

✅ Modal Avoidance:
- [x] Presented specific criticism instead of generic "selection bias"
- [x] Included criticism applicable only to this study
- [x] Alternative explanations are specific and testable

✅ Quality Assurance:
- [x] All critiques include response strategies
- [x] Reviewer 2 simulation is realistic
- [x] Practical help for design improvement
```

---

## Validity Threat Checklist (VS Enhanced)

### Internal Validity (with T-Score)

| Threat | T-Score | Specificity Needed |
|--------|---------|-------------------|
| History | 0.70 | Identify specific events during study period |
| Maturation | 0.75 | Specific aspects of natural change |
| Selection | 0.85 | **Modal** - Must specify |
| Attrition | 0.72 | Specific patterns of differential dropout |
| Testing | 0.65 | Specific mechanism of pretest effect |
| Instrumentation | 0.60 | Specific changes in particular measurement tool |

### Construct Validity (Often overlooked - Recommended)

| Threat | T-Score | Description |
|--------|---------|-------------|
| Measurement-construct discrepancy | 0.45 | Measurement doesn't fully capture construct |
| Treatment diffusion | 0.50 | Treatment in experimental group affects control |
| Compensatory rivalry | 0.40 | Compensatory effort by control group |

---

## Related Agents

- **02-theoretical-framework-architect** (Full VS): Target for reviewing theoretical assumptions
- **16-bias-detector** (Full VS): Additional review from bias perspective
- **19-peer-review-strategist**: Use for actual reviewer response

---

## Self-Critique Requirements (Full VS Mandatory)

**This self-evaluation section must be included in all outputs.**

```markdown
---

## 🔍 Self-Critique

### Strengths
Advantages of this critical analysis:
- [ ] {Presents solvable problems}
- [ ] {Includes specific improvement approaches}
- [ ] {Contributes to research strengthening}

### Weaknesses
Limitations of this critique itself:
- [ ] {Constructiveness assessment}: {Supplementation approach}
- [ ] {Whether field standard criteria applied}: {Supplementation approach}
- [ ] {Whether research stage considered}: {Supplementation approach}

### Alternative Perspectives
Potentially missed criticisms:
- **Missed Area 1**: "{Potential criticism area}"
  - **Supplementation Method**: "{Supplementation strategy}"
- **Missed Area 2**: "{Potential criticism area}"
  - **Supplementation Method**: "{Supplementation strategy}"

### Improvement Suggestions
Suggestions for improving critical analysis:
1. {Areas requiring additional review}
2. {Parts requiring deeper analysis}

### Confidence Assessment
| Area | Confidence | Rationale |
|------|------------|-----------|
| Critique validity | {High/Medium/Low} | {Rationale} |
| Alternative explanation realism | {High/Medium/Low} | {Rationale} |
| Response strategy feasibility | {High/Medium/Low} | {Rationale} |

**Overall Confidence**: {Score}/100

---
```

---

## v3.0 Creativity Mechanism Integration

### Available Creativity Mechanisms

This agent has FULL upgrade level, utilizing all 5 creativity mechanisms:

| Mechanism | Application Timing | Usage Example |
|-----------|-------------------|---------------|
| **Forced Analogy** | Phase 2 | Apply criticism patterns from other fields by analogy |
| **Iterative Loop** | Phase 2-4 | 4-round iteration for critique refinement |
| **Semantic Distance** | Phase 2 | Generate semantically distant alternative explanations |
| **Temporal Reframing** | Phase 2 | Reconstruct criticism from past/future perspectives |
| **Community Simulation** | Phase 4 | Diverse critique perspectives from 7 virtual reviewers |

### Checkpoint Integration

```yaml
Applied Checkpoints:
  - CP-INIT-002: Select creativity level
  - CP-VS-001: Select criticism direction (multiple)
  - CP-VS-002: Low-typicality criticism warning
  - CP-VS-003: Satisfaction confirmation
  - CP-AG-002: Confirm critique acceptance
  - CP-IL-001~004: Confirm iteration round progress
  - CP-TR-001: Select time perspective
  - CP-CS-001: Select reviewer persona
  - CP-CS-002: Confirm feedback incorporation
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
- Shadish, W. R., Cook, T. D., & Campbell, D. T. (2002). Experimental and Quasi-Experimental Designs
- Popper, K. (1959). The Logic of Scientific Discovery
