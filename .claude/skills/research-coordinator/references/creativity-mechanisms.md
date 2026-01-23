---
name: creativity-mechanisms-reference
description: Reference documentation for v3.0 creativity mechanisms
version: "3.0.0"
---

# Creativity Mechanisms Reference

## Overview

This document provides quick reference for all 5 creativity mechanisms in Research Coordinator v3.0.

## Mechanism Summary

| Mechanism | Purpose | Key Checkpoints | Best For |
|-----------|---------|-----------------|----------|
| Forced Analogy | Cross-domain concept mapping | CP-FA-001, CP-FA-002 | Novel framework generation |
| Iterative Loop | Divergent-convergent cycles | CP-IL-001 to 004 | Idea refinement |
| Semantic Distance | Embedding-based combinations | CP-SD-001, CP-SD-002 | Theory integration |
| Temporal Reframing | Time perspective shifts | CP-TR-001 | Assumption surfacing |
| Community Simulation | Virtual researcher feedback | CP-CS-001, CP-CS-002 | Pre-submission review |

## Integration with VS Engine

Creativity mechanisms are invoked in VS Phase 4 (Execution):

```
VS Phase 4: Execution
├── Standard execution
├── IF creativity_level >= "Innovative":
│   ├── Check enabled mechanisms
│   └── Execute selected mechanisms
└── Continue to Phase 5
```

## Mechanism Activation Matrix

| Creativity Level | Forced Analogy | Iterative Loop | Semantic Distance | Temporal | Community |
|-----------------|----------------|----------------|-------------------|----------|-----------|
| Conservative | - | - | - | - | - |
| Balanced | Optional | Optional | Optional | - | - |
| Innovative | Yes | Yes | Yes | Optional | Optional |
| Extreme | Yes | Yes | Yes | Yes | Yes |

## File Locations

```
.claude/skills/research-coordinator/
├── creativity/
│   ├── forced-analogy.md
│   ├── iterative-loop.md
│   ├── semantic-distance.md
│   ├── temporal-reframing.md
│   └── community-simulation.md
```

## Quick Start

To enable creativity mechanisms in an agent:

```yaml
# In agent SKILL.md
creativity_config:
  enabled: true
  level: "Innovative"  # Conservative | Balanced | Innovative | Extreme
  mechanisms:
    - forced-analogy
    - iterative-loop
    - semantic-distance
```

## Detailed Mechanism Reference

### 1. Forced Analogy (forced-analogy.md)

**Purpose**: Generate novel insights by mapping concepts from distant domains.

**Process Flow**:
```
1. Identify source domain (user's research area)
2. Select target domain (distant but structurally similar)
3. Map structural relationships
4. Generate novel hypotheses from mapping
5. Validate analogical coherence
```

**Checkpoints**:
- `CP-FA-001`: Domain selection approval
- `CP-FA-002`: Analogy validation

**Example Output**:
```yaml
analogy:
  source: "Employee learning in organizations"
  target: "Immune system adaptation"
  mappings:
    - source_concept: "Training program"
      target_concept: "Antigen exposure"
      insight: "Repeated, varied exposure strengthens response"
    - source_concept: "Knowledge transfer"
      target_concept: "Antibody memory"
      insight: "Past learning enables rapid future response"
```

### 2. Iterative Loop (iterative-loop.md)

**Purpose**: Refine ideas through cycles of divergent and convergent thinking.

**Process Flow**:
```
Loop (max 3 iterations):
  1. Diverge: Generate multiple alternatives
  2. Evaluate: Score against criteria
  3. Converge: Select top candidates
  4. Check: User satisfaction?
     - Yes → Exit loop
     - No → Continue iteration
```

**Checkpoints**:
- `CP-IL-001`: Initial direction confirmation
- `CP-IL-002`: Iteration 1 satisfaction check
- `CP-IL-003`: Iteration 2 satisfaction check
- `CP-IL-004`: Final selection approval

**Iteration Metrics**:
```yaml
iteration_tracking:
  max_iterations: 3
  candidates_per_iteration: 5
  convergence_threshold: 0.8
  user_satisfaction_required: true
```

### 3. Semantic Distance (semantic-distance.md)

**Purpose**: Combine theories using embedding-based semantic relationships.

**Process Flow**:
```
1. Embed input theories in semantic space
2. Calculate pairwise distances
3. Identify bridging concepts
4. Generate integration proposals
5. Validate theoretical coherence
```

**Checkpoints**:
- `CP-SD-001`: Distance threshold approval
- `CP-SD-002`: Integration proposal selection

**Distance Thresholds**:
```yaml
semantic_thresholds:
  very_close: 0.0 - 0.3    # Same theoretical family
  close: 0.3 - 0.5         # Related constructs
  moderate: 0.5 - 0.7      # Different but connectable
  distant: 0.7 - 0.9       # Novel combination potential
  very_distant: 0.9 - 1.0  # Requires careful bridging
```

### 4. Temporal Reframing (temporal-reframing.md)

**Purpose**: Surface hidden assumptions by shifting time perspectives.

**Process Flow**:
```
1. State current research assumption
2. Apply temporal shift:
   - Historical: "How was this viewed 50 years ago?"
   - Future: "How might this change in 20 years?"
   - Compressed: "What if this happened instantly?"
   - Extended: "What if this took 100 years?"
3. Identify assumption violations
4. Generate alternative framings
```

**Checkpoints**:
- `CP-TR-001`: Temporal frame selection

**Temporal Frames**:
```yaml
temporal_frames:
  historical_distant: -50 years
  historical_recent: -10 years
  present: 0
  near_future: +10 years
  distant_future: +50 years
  compressed: instant
  extended: centuries
```

### 5. Community Simulation (community-simulation.md)

**Purpose**: Simulate diverse reviewer feedback before submission.

**Process Flow**:
```
1. Define researcher personas (3-5)
2. Present research to each persona
3. Collect simulated feedback
4. Synthesize critiques
5. Prioritize revisions
```

**Checkpoints**:
- `CP-CS-001`: Persona selection
- `CP-CS-002`: Feedback integration approval

**Default Personas**:
```yaml
simulated_reviewers:
  - id: "methodologist"
    focus: "Research design, validity, statistical approach"
    strictness: high

  - id: "theorist"
    focus: "Theoretical grounding, conceptual clarity"
    strictness: medium

  - id: "practitioner"
    focus: "Real-world applicability, practical implications"
    strictness: low

  - id: "skeptic"
    focus: "Alternative explanations, limitations"
    strictness: very_high

  - id: "domain_expert"
    focus: "Domain-specific accuracy, literature coverage"
    strictness: high
```

## Mechanism Combination Patterns

### Pattern 1: Deep Exploration
```yaml
combination: "iterative-loop + semantic-distance"
use_case: "Exploring theoretical integration options"
flow:
  1. Semantic distance identifies candidate theories
  2. Iterative loop refines integration approach
```

### Pattern 2: Novel Framework Generation
```yaml
combination: "forced-analogy + community-simulation"
use_case: "Creating and validating new frameworks"
flow:
  1. Forced analogy generates novel framework
  2. Community simulation stress-tests validity
```

### Pattern 3: Assumption Challenge
```yaml
combination: "temporal-reframing + iterative-loop"
use_case: "Questioning fundamental assumptions"
flow:
  1. Temporal reframing surfaces hidden assumptions
  2. Iterative loop explores alternative foundations
```

## Performance Considerations

| Mechanism | Avg Duration | Token Cost | Checkpoint Count |
|-----------|-------------|------------|------------------|
| Forced Analogy | 30-60s | 2-4K | 2 |
| Iterative Loop | 60-180s | 5-15K | 4 |
| Semantic Distance | 20-40s | 1-3K | 2 |
| Temporal Reframing | 15-30s | 1-2K | 1 |
| Community Simulation | 45-90s | 3-8K | 2 |

## Error Handling

```yaml
error_handling:
  mechanism_timeout:
    threshold: 120s
    action: "Graceful degradation to simpler approach"

  low_quality_output:
    threshold: "satisfaction < 0.5"
    action: "Offer mechanism switch or manual mode"

  api_failure:
    action: "Fall back to heuristic-based approach"
```

## Version History

| Version | Changes |
|---------|---------|
| 3.0.0 | Initial release with 5 mechanisms |
| 3.0.1 | Added combination patterns |
| 3.0.2 | Performance optimization |
