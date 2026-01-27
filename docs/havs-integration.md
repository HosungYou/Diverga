# HAVS (Humanization-Adapted VS) Integration

## Overview

HAVS (Humanization-Adapted VS) is a specialized 3-phase methodology designed specifically for text transformation in the G6-Academic-Style-Humanizer agent. This document describes the integration of HAVS into Diverga's VS methodology system.

## Background

### Why HAVS Instead of Standard VS?

Standard VS (Verbalized Sampling) is designed for **research decision-making** - choosing theories, methodologies, and frameworks. Applying the standard 5-phase VS process to text humanization creates a category error:

| Aspect | Standard VS (Research) | HAVS (Humanization) |
|--------|------------------------|---------------------|
| **Purpose** | Theory/methodology selection | Text transformation strategy |
| **T-Score Meaning** | Theory typicality | Transformation pattern typicality |
| **Phase Count** | 5 phases (0-5) | 3 phases (0-2) |
| **Creativity Focus** | Conceptual innovation | Natural expression |

### Design Principles

HAVS adapts the core anti-modal principle from VS methodology:
- **Avoid modal (most common) approaches** that AI detectors easily identify
- **Present differentiated alternatives** with varying risk/reward profiles
- **Enable user choice** based on their specific context and risk tolerance

## HAVS 3-Phase Process

### Phase 0: Transformation Context

Collect contextual information before transformation:

```yaml
inputs:
  g5_analysis: "Pattern analysis from G5-AcademicStyleAuditor"
  target_style: "journal | conference | thesis | informal"
  user_mode: "conservative | balanced | aggressive"
```

### Phase 1: Modal Transformation Warning

Warn against modal transformations (T > 0.7) that are easily detectable:

| Modal Transformation | T-Score | Why It Fails |
|---------------------|---------|--------------|
| Synonym-only replacement | 0.9 | Most common; AI detectors trained for it |
| Sentence reordering only | 0.85 | Structure preserved; patterns remain |
| Passive↔Active only | 0.8 | Inconsistent voice creates new patterns |

### Phase 2: Differentiated Transformation Directions

Present three transformation directions:

| Direction | T-Score | Strategies | Best For |
|-----------|---------|------------|----------|
| **A** | ≈0.6 | Vocabulary + phrase | Conservative mode |
| **B** ⭐ | ≈0.4 | + Sentence recombination, flow | Balanced (recommended) |
| **C** | ≈0.2 | + Paragraph reorganization, style | Aggressive mode |

## New Humanization Modules

### h-style-transfer

Applies discipline-specific writing styles:

- **Education**: Practice-oriented, accessible terminology
- **Psychology**: Person-centered, measurement-conscious
- **Management**: Action-oriented, stakeholder-aware
- **Health Sciences**: Clinical precision, risk-benefit awareness
- **Social Sciences**: Context-sensitive, reflexive

### h-flow-optimizer

Optimizes text flow at three levels:

1. **Sentence Level**: Length variation, complexity variation, opening diversity
2. **Paragraph Level**: Topic sentences, evidence flow, transitions
3. **Document Level**: Argument progression, section balance, cohesion

## Integration Points

### G6-Humanizer YAML Configuration

```yaml
v3_integration:
  dynamic_t_score: true
  creativity_modules:
    - semantic-distance
    - iterative-loop
  humanization_modules:
    - h-style-transfer
    - h-flow-optimizer
  checkpoints:
    - CP-INIT-001
    - CP_HUMANIZATION_REVIEW
    - CP_HAVS_DIRECTION
    - CP_HUMANIZATION_VERIFICATION
  havs:
    enabled: true
    phases: [0, 1, 2]
    max_iterations: 2
```

### Checkpoint Flow

```
G5 Analysis → G6 HAVS Transformation → CP_HUMANIZATION_VERIFICATION → F5 Verification
                    │
                    ├── Phase 0: Context collection
                    ├── Phase 1: Modal warning
                    ├── Phase 2: Direction selection (CP_HAVS_DIRECTION)
                    └── Iterative refinement (if B or C)
```

## Files Modified/Created

| File | Action | Description |
|------|--------|-------------|
| `.claude/skills/research-agents/G6-academic-style-humanizer/SKILL.md` | Modified | Added HAVS integration, new checkpoints, iterative-loop |
| `.claude/skills/research-coordinator/creativity/h-style-transfer.md` | Created | Discipline-specific style transfer module |
| `.claude/skills/research-coordinator/creativity/h-flow-optimizer.md` | Created | Flow optimization module |

## Usage

HAVS activates automatically when G6-Academic-Style-Humanizer processes text:

1. User invokes G6 with text and G5 analysis
2. Phase 0 collects context
3. Phase 1 identifies and warns about modal transformations
4. Phase 2 presents directions; user selects via CP_HAVS_DIRECTION
5. Transformation executes with selected direction
6. Iterative refinement (for B/C modes) checks for self-generated AI patterns
7. F5 verification confirms transformation quality

## Verification Criteria

| Criterion | Target |
|-----------|--------|
| Meaning preservation | ≥95% semantic similarity |
| Citation accuracy | 100% preserved |
| Statistics accuracy | 100% preserved |
| Flow Naturalness Index | ≥0.7 (improved from AI-typical <0.5) |

## References

- VS Engine v3.0: `research-coordinator/core/vs-engine.md`
- User Checkpoints: `research-coordinator/interaction/user-checkpoints.md`
- Creativity Modules: `research-coordinator/creativity/`
