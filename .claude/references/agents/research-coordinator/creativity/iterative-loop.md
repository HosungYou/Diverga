---
name: iterative-loop
description: |
  Iterative Divergent-Convergent Loop for idea refinement.
  Cycles through exploration and synthesis phases.
version: "3.0.0"
---

# Iterative Loop Mechanism

## Overview

Implements multiple rounds of divergent (exploration) and convergent (synthesis) thinking to refine ideas progressively.

## Process Structure

```
┌─────────────────────────────────────────────────────────────┐
│                    Iterative Loop (4 Rounds)                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ROUND 1: Wide Exploration (Divergent)                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Goal: Generate maximum options without constraints    │   │
│  │                                                      │   │
│  │ Process:                                             │   │
│  │   - Suspend all guardrails temporarily               │   │
│  │   - Generate 10-15 diverse ideas                     │   │
│  │   - Include unconventional approaches                │   │
│  │   - No evaluation at this stage                      │   │
│  │                                                      │   │
│  │ ⬜ CP-IL-001: "Select interesting directions"        │   │
│  │    (Multi-select from generated options)             │   │
│  └─────────────────────────────────────────────────────┘   │
│         │                                                   │
│         ▼                                                   │
│  ROUND 2: Cross-Pollination (Combinatorial)                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Goal: Combine and synthesize selected directions     │   │
│  │                                                      │   │
│  │ Process:                                             │   │
│  │   - Take 2-3 most interesting directions             │   │
│  │   - Find unexpected combinations                     │   │
│  │   - Generate hybrid approaches                       │   │
│  │   - Create novel integrations                        │   │
│  │                                                      │   │
│  │ ⬜ CP-IL-002: "Approve combination?"                 │   │
│  │    (Review and approve proposed combination)         │   │
│  └─────────────────────────────────────────────────────┘   │
│         │                                                   │
│         ▼                                                   │
│  ROUND 3: Constraint Application (Convergent)              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Goal: Apply academic guardrails and feasibility      │   │
│  │                                                      │   │
│  │ Process:                                             │   │
│  │   - Re-enable guardrails                             │   │
│  │   - Evaluate methodological soundness                │   │
│  │   - Check feasibility constraints                    │   │
│  │   - Identify required justifications                 │   │
│  │                                                      │   │
│  │ ⬜ CP-IL-003: "Select guardrail level"               │   │
│  │    Options: Strict / Balanced / Flexible             │   │
│  └─────────────────────────────────────────────────────┘   │
│         │                                                   │
│         ▼                                                   │
│  ROUND 4: Synthesis (Final Convergent)                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Goal: Produce refined, defensible output             │   │
│  │                                                      │   │
│  │ Process:                                             │   │
│  │   - Synthesize best elements                         │   │
│  │   - Create coherent framework                        │   │
│  │   - Document rationale                               │   │
│  │   - Prepare defense arguments                        │   │
│  │                                                      │   │
│  │ ⬜ CP-IL-004: "Approve final result?"                │   │
│  │    Options: Approve / Another round / Start over     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Configuration

```yaml
iterative_loop_config:
  max_rounds: 4
  round_1_options: 10-15
  round_2_combinations: 3-5

  guardrail_levels:
    strict:
      - peer_review_defensible: required
      - validated_instruments: required
      - established_methods: required
    balanced:
      - peer_review_defensible: required
      - validated_instruments: preferred
      - established_methods: flexible
    flexible:
      - peer_review_defensible: preferred
      - validated_instruments: optional
      - established_methods: optional

  user_can_extend: true
  max_total_rounds: 6
```

## Output Format

```markdown
## Iterative Loop Results

### Round 1: Wide Exploration
**Generated Options** (15):
1. [Option description] - T-Score: [X.X]
2. [Option description] - T-Score: [X.X]
...

**User Selected**: [Options X, Y, Z]

### Round 2: Cross-Pollination
**Combinations Generated**:
- Combo A: [Option X] × [Option Y] → [Hybrid description]
- Combo B: [Option Y] × [Option Z] → [Hybrid description]

**User Approved**: Combo A

### Round 3: Constraint Application
**Guardrail Level**: Balanced

**Evaluation**:
| Criterion | Status | Notes |
|-----------|--------|-------|
| Peer-review defensible | ✅ | [Justification] |
| Validated instruments | ⚠️ | [Adaptation needed] |
| Methodological soundness | ✅ | [Justification] |

### Round 4: Synthesis
**Final Output**:
[Refined, defensible recommendation with full rationale]

**Defense Arguments**:
1. [Argument 1]
2. [Argument 2]
```

## Cognitive Science Basis

This mechanism is based on the dual-process model of creativity:

```
Divergent Thinking (Guilford, 1967):
├── Fluency: Generate many ideas
├── Flexibility: Vary categories/approaches
├── Originality: Produce novel ideas
└── Elaboration: Develop ideas in detail

Convergent Thinking:
├── Evaluation: Assess feasibility
├── Selection: Choose best options
├── Integration: Combine elements
└── Refinement: Polish final output

Creative Process (Wallas, 1926):
├── Preparation → Round 1 setup
├── Incubation → Round 1-2 exploration
├── Illumination → Round 2-3 synthesis
└── Verification → Round 4 evaluation
```

## Usage Tips

1. **Don't rush Round 1**: Maximum divergence needs time
2. **Be open in Round 2**: Unexpected combinations yield innovation
3. **Be honest in Round 3**: Guardrails protect quality
4. **Document everything in Round 4**: Reviewers need rationale
