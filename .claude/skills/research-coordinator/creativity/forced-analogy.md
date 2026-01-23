---
name: forced-analogy
description: |
  Forced Analogy creative mechanism for cross-domain concept mapping.
  Brings concepts from unrelated fields to generate novel frameworks.
version: "3.0.0"
---

# Forced Analogy Mechanism

## Overview

Forces creative thinking by mapping concepts from unrelated domains to the research topic, generating novel theoretical frameworks and perspectives.

## Source Domain Pool

```yaml
natural_sciences:
  ecology:
    - ecological_succession: "Pioneer → Climax stages"
    - food_web: "Energy transfer networks"
    - niche_theory: "Resource partitioning"
    - symbiosis: "Mutualism, parasitism, commensalism"

  physics:
    - entropy: "Disorder and equilibrium"
    - quantum_superposition: "Multiple states until observed"
    - relativity: "Frame-dependent perspectives"
    - wave_particle_duality: "Dual nature phenomena"

  chemistry:
    - catalysis: "Accelerators without consumption"
    - equilibrium: "Dynamic balance"
    - phase_transition: "State changes at thresholds"

  biology:
    - evolution: "Selection and adaptation"
    - homeostasis: "Self-regulation"
    - emergence: "Complex from simple"

humanities:
  philosophy:
    - dialectics: "Thesis-antithesis-synthesis"
    - phenomenology: "Lived experience focus"
    - pragmatism: "Truth through utility"

  history:
    - punctuated_equilibrium: "Stability interrupted by change"
    - path_dependency: "Historical constraints on present"

  linguistics:
    - semiotics: "Sign systems and meaning"
    - speech_acts: "Language as action"

arts:
  music_theory:
    - harmony_dissonance: "Tension and resolution"
    - rhythm_patterns: "Temporal structures"

  architecture:
    - form_follows_function: "Purpose-driven design"
    - negative_space: "Importance of absence"

  design:
    - affordance: "Perceived possibilities"
    - gestalt: "Whole greater than parts"

other:
  economics:
    - supply_demand: "Market equilibrium"
    - externalities: "Unintended consequences"

  anthropology:
    - liminality: "Threshold states"
    - rites_of_passage: "Transition rituals"
```

## Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│                  Forced Analogy Process                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Step 1: Source Selection                                   │
│  ⬜ CP-FA-001: Select source domain                         │
│     - Random (maximum creativity)                           │
│     - Natural Sciences                                      │
│     - Humanities                                            │
│     - Custom specification                                  │
│                                                             │
│  Step 2: Concept Extraction                                 │
│     - Select 2-3 concepts from source domain                │
│     - Identify key characteristics                          │
│     - Note structural relationships                         │
│                                                             │
│  Step 3: Mapping Generation                                 │
│     - Map source concepts to target research                │
│     - Identify parallel structures                          │
│     - Generate novel terminology                            │
│                                                             │
│  Step 4: Framework Synthesis                                │
│     - Construct new theoretical framework                   │
│     - Define key constructs                                 │
│     - Specify relationships                                 │
│                                                             │
│  Step 5: Approval                                           │
│  ⬜ CP-FA-002: Review and approve analogy                   │
│     - Accept and apply                                      │
│     - Request alternative                                   │
│     - Skip                                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Output Format

```markdown
## Forced Analogy Result

### Source Domain
**Field**: [e.g., Ecology]
**Concept**: [e.g., Ecological Succession]
**Key Characteristics**:
- [Characteristic 1]
- [Characteristic 2]

### Target Domain
**Research Topic**: [User's research topic]
**Current Framing**: [Existing approach]

### Mapping

| Source Element | Target Element | Rationale |
|---------------|----------------|-----------|
| [Pioneer stage] | [Early adopters] | [Explanation] |
| [Climax community] | [Mainstream adoption] | [Explanation] |

### Proposed Framework

**Name**: "[Generated Framework Name]"
(e.g., "Ecological Succession Model of EdTech Adoption")

**Core Constructs**:
1. [Construct 1]: Definition
2. [Construct 2]: Definition

**Relationships**:
- [Construct 1] → [Construct 2]: [Nature of relationship]

**Theoretical Contribution**:
[How this framework advances understanding]

### T-Score Assessment
Estimated T-Score: [0.15-0.25] (Innovative)
Justification: [Why this is novel]
```

## Example

**Research Topic**: AI chatbots for language learning anxiety reduction

**Source**: Ecology - Ecological Succession

**Mapping**:
- Pioneer species → Early adopter students (risk-tolerant)
- Facilitation → Peer influence and scaffolding
- Inhibition → Technology resistance
- Climax community → Full integration into learning ecosystem

**Generated Framework**: "Ecological Succession Model of Educational Technology Integration (ESMETI)"

**T-Score**: 0.18 (Highly innovative, requires strong justification)

## Usage Tips

1. **For maximum creativity**: Select "Random" source domain
2. **For safer innovation**: Select domain with known parallels to target
3. **For specific needs**: Custom specify source domain and concept
4. **Document thoroughly**: Novel frameworks require strong justification
