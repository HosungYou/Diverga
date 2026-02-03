---
name: temporal-reframing
description: |
  Temporal Reframing mechanism for perspective shifts across time.
  Examines research from past, future, and parallel perspectives.
version: "3.0.0"
---

# Temporal Reframing Mechanism

## Overview

Shifts temporal perspective to reveal hidden assumptions and limitations in current research framing.

## Perspectives

### Past Perspective (1990s)

```yaml
past_perspective:
  timeframe: "1990s"
  question: "If we conducted this research in the 1990s, what would be different?"

  analysis_points:
    - dominant_theories: "What theories were mainstream then?"
    - technology_context: "What technology existed?"
    - methodological_norms: "What methods were standard?"
    - missing_concepts: "What concepts didn't exist yet?"

  insights:
    - historical_constraints: "Why did research evolve this way?"
    - path_dependency: "What alternatives were foreclosed?"
    - theoretical_gaps: "What wasn't explained then that is now?"
```

### Future Perspective (2035)

```yaml
future_perspective:
  timeframe: "2035 (10 years ahead)"
  question: "How will this research be viewed in 10 years?"

  analysis_points:
    - likely_advances: "What will probably change?"
    - current_limitations: "What will seem naive?"
    - emerging_paradigms: "What new frameworks might exist?"
    - technology_evolution: "How will technology change context?"

  insights:
    - temporal_limitations: "What's specific to our current moment?"
    - future_proofing: "How can we make research more durable?"
    - anticipatory_design: "What future developments should we consider?"
```

### Parallel Perspective (Alternate History)

```yaml
parallel_perspective:
  concept: "Alternate developmental trajectory"
  question: "If this field had developed differently, what would we be studying?"

  analysis_points:
    - key_branching_points: "What were pivotal moments?"
    - alternate_outcomes: "What if different choices were made?"
    - suppressed_alternatives: "What approaches were abandoned?"
    - cross_field_imports: "What could we borrow from other fields?"

  insights:
    - hidden_assumptions: "What do we take for granted?"
    - alternative_frameworks: "What other ways of seeing exist?"
    - theoretical_diversity: "What's missing from current discourse?"
```

## Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│                Temporal Reframing Process                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ⬜ CP-TR-001: Select perspective(s)                        │
│     - Past (1990s)                                          │
│     - Future (2035)                                         │
│     - Parallel Universe                                     │
│     - All (recommended)                                     │
│                                                             │
│         │                                                   │
│         ▼                                                   │
│  For each selected perspective:                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 1. Contextualize research in that timeframe         │   │
│  │ 2. Identify what would be different                 │   │
│  │ 3. Extract insights for current research            │   │
│  │ 4. Generate recommendations                         │   │
│  └─────────────────────────────────────────────────────┘   │
│         │                                                   │
│         ▼                                                   │
│  Synthesis:                                                 │
│     - Cross-perspective insights                            │
│     - Recommendations for strengthening research            │
│     - Novel angles revealed                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Output Format

```markdown
## Temporal Reframing Analysis

### Research Topic
[User's research topic]

---

### Past Perspective (1990s)

**Context**: In the 1990s, [describe historical context]

**Key Differences**:
- Dominant theory was [X] instead of [Y]
- Technology context: [description]
- Methodological norms: [description]

**Insights**:
- [Insight 1]: [implication for current research]
- [Insight 2]: [implication for current research]

---

### Future Perspective (2035)

**Projected Context**: By 2035, [anticipated changes]

**Current Limitations Revealed**:
- [Limitation 1]: Will likely seem [X]
- [Limitation 2]: May be superseded by [Y]

**Future-Proofing Recommendations**:
- [Recommendation 1]
- [Recommendation 2]

---

### Parallel Perspective

**Alternate Trajectory**: If [key branching point] had gone differently...

**Suppressed Alternatives**:
- [Alternative 1]: Was abandoned because [reason], but could be revisited
- [Alternative 2]: Never gained traction, but offers [potential]

**Cross-Field Possibilities**:
- From [Field X]: [concept] could inform [aspect of research]

---

### Synthesis

**Cross-Perspective Insights**:
1. [Synthesized insight]
2. [Synthesized insight]

**Recommendations**:
- [Concrete recommendation for strengthening research]
- [Novel angle to consider]
```

## Historical Context Examples

### EdTech Research Timeline

```yaml
historical_context:
  1990s:
    dominant_theory: "Behaviorism, CAI"
    technology: "Desktop PCs, CD-ROMs"
    key_event: "Web 1.0 emergence"
    methodological_norm: "Lab experiments, surveys"

  2000s:
    dominant_theory: "Constructivism, e-Learning"
    technology: "LMS, Web 2.0, early mobile"
    key_event: "Social media, open education"
    methodological_norm: "Design-based research"

  2010s:
    dominant_theory: "Connectivism, MOOCs"
    technology: "Mobile-first, learning analytics"
    key_event: "Big data, AI emergence"
    methodological_norm: "Learning analytics, LA/EDM"

  2020s:
    dominant_theory: "AI-mediated learning, adaptive"
    technology: "GenAI, VR/AR, personalization"
    key_event: "ChatGPT, pandemic disruption"
    methodological_norm: "Mixed methods, human-AI"

  2030s_projected:
    dominant_theory: "Human-AI co-learning?"
    technology: "AGI?, immersive, neural interfaces?"
    key_event: "Unknown paradigm shifts"
    methodological_norm: "AI-assisted research?"
```

## Usage Tips

1. **Past perspective**: Reveals hidden assumptions we inherited
2. **Future perspective**: Tests durability of current approach
3. **Parallel perspective**: Uncovers suppressed alternatives
4. **All three together**: Maximum insight generation
