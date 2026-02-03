---
name: semantic-distance
description: |
  Semantic Distance Scorer for recommending conceptually distant combinations.
  Uses embedding-based distance to prioritize innovative pairings.
version: "3.0.0"
---

# Semantic Distance Mechanism

## Overview

Calculates semantic distance between theories/concepts using embeddings and prioritizes combinations that are far apart, encouraging innovative cross-pollination.

## Distance Calculation

```python
def calculate_semantic_distance(concept_a, concept_b):
    """
    Calculate semantic distance between two concepts.

    Returns:
        float: Distance score (0.0 = identical, 1.0 = maximally different)
    """
    embedding_a = get_embedding(concept_a)
    embedding_b = get_embedding(concept_b)

    cosine_similarity = dot(embedding_a, embedding_b) / (norm(a) * norm(b))
    distance = 1 - cosine_similarity

    return distance
```

## Distance Thresholds

```yaml
distance_thresholds:
  close:
    range: "0.0 - 0.3"
    description: "Very similar concepts, low innovation"
    risk: low
    recommendation: "Safe but limited differentiation"

  moderate:
    range: "0.3 - 0.5"
    description: "Related but distinct"
    risk: low
    recommendation: "Good balance"

  far:
    range: "0.5 - 0.7"
    description: "Meaningfully different"
    risk: medium
    recommendation: "Recommended for innovation"

  very_far:
    range: "0.7 - 0.85"
    description: "Substantially different domains"
    risk: medium-high
    recommendation: "Strong justification needed"

  extreme:
    range: "0.85 - 1.0"
    description: "Maximally different"
    risk: high
    recommendation: "Experimental, very strong justification"
```

## Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│                Semantic Distance Process                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Step 1: Input Collection                                   │
│     - User's base theory/concept                            │
│     - Research domain                                       │
│     - Target creativity level                               │
│                                                             │
│  Step 2: Candidate Generation                               │
│     - Query theory database for candidates                  │
│     - Include cross-domain options                          │
│                                                             │
│  Step 3: Distance Calculation                               │
│     - Calculate distance for all pairs                      │
│     - Rank by distance (descending)                         │
│                                                             │
│  Step 4: Threshold Selection                                │
│  ⬜ CP-SD-001: Select distance threshold                    │
│     - Close (>0.3): Safe                                    │
│     - Moderate (>0.5): Balanced (recommended)               │
│     - Far (>0.7): Innovative                                │
│     - Extreme (>0.85): Experimental                         │
│                                                             │
│  Step 5: Recommendation                                     │
│     - Present top 5 combinations above threshold            │
│                                                             │
│  Step 6: Selection                                          │
│  ⬜ CP-SD-002: Select combination(s)                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Pre-computed Theory Embeddings

```yaml
# Example theory embeddings (simplified representation)
theory_embeddings:
  TAM:
    domain: "technology_adoption"
    cluster: "acceptance_models"

  SDT:
    domain: "motivation"
    cluster: "psychological_needs"

  Ecological_Succession:
    domain: "ecology"
    cluster: "temporal_change"

  Dialectics:
    domain: "philosophy"
    cluster: "synthesis_processes"

# Pre-computed distances (sample)
distance_matrix:
  TAM_to_SDT: 0.35
  TAM_to_Ecological_Succession: 0.82
  TAM_to_Dialectics: 0.78
  SDT_to_Ecological_Succession: 0.75
  SDT_to_Dialectics: 0.65
```

## Output Format

```markdown
## Semantic Distance Analysis

### Base Concept
**Theory/Concept**: [User's base theory]
**Domain**: [Domain]

### Candidate Combinations (sorted by distance)

| Rank | Candidate | Distance | Risk | Potential |
|------|-----------|----------|------|-----------|
| 1 | [Theory A] | 0.85 | High | ★★★★★ |
| 2 | [Theory B] | 0.78 | Medium-High | ★★★★ |
| 3 | [Theory C] | 0.65 | Medium | ★★★ |
| 4 | [Theory D] | 0.52 | Low-Medium | ★★ |
| 5 | [Theory E] | 0.38 | Low | ★ |

### Recommended Combination
**Selected**: [Base] × [Candidate]
**Distance**: [X.XX]
**Rationale**: [Why this combination is promising]

### Integration Proposal
[How to integrate the two concepts]
```

## Theory Database

For semantic distance calculation, the system maintains embeddings for:

```yaml
theory_categories:
  psychology:
    - Social Cognitive Theory (SCT)
    - Self-Determination Theory (SDT)
    - Theory of Planned Behavior (TPB)
    - Cognitive Load Theory (CLT)
    - Flow Theory
    - Attribution Theory
    - Expectancy-Value Theory

  technology:
    - Technology Acceptance Model (TAM)
    - UTAUT/UTAUT2
    - Innovation Diffusion Theory
    - Technological Pedagogical Content Knowledge (TPACK)

  education:
    - Constructivism
    - Connectivism
    - Community of Inquiry (CoI)
    - Social Presence Theory
    - Transactional Distance Theory

  organizational:
    - Job Demands-Resources (JD-R)
    - Organizational Commitment Theory
    - Knowledge Management Theory
    - Dynamic Capabilities Theory

  natural_sciences:
    - Ecological Succession
    - Systems Theory
    - Complexity Theory
    - Network Theory
    - Evolutionary Theory
```

## Usage Tips

1. **Start with moderate distance** for first-time users
2. **Higher distance = higher risk** but also higher potential contribution
3. **Document the bridging logic** between distant concepts
4. **Consider multiple candidates** before final selection
