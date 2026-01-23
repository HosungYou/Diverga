---
name: community-simulation
description: |
  Virtual Research Community Simulation for diverse feedback.
  Simulates feedback from 7 researcher personas with different perspectives.
version: "3.0.0"
---

# Community Simulation Mechanism

## Overview

Simulates a virtual academic community with diverse perspectives to provide multi-faceted feedback on research proposals.

## Persona Pool (7 Researchers)

```yaml
personas:
  conservative_methodologist:
    icon: "🔬"
    name: "Dr. Method"
    role: "Conservative Methodologist"
    perspective: "Values rigor, validated methods, established approaches"
    typical_concerns:
      - "Is this methodologically sound?"
      - "Has this approach been validated?"
      - "What are the threats to validity?"
    feedback_style: "Cautious, detail-oriented, risk-averse"

  innovation_seeker:
    icon: "🚀"
    name: "Dr. Nova"
    role: "Innovation Seeker"
    perspective: "Values novelty, paradigm shifts, creative approaches"
    typical_concerns:
      - "What's new here?"
      - "How does this advance the field?"
      - "Is this too incremental?"
    feedback_style: "Enthusiastic about novelty, pushes for more"

  interdisciplinary_researcher:
    icon: "🌐"
    name: "Dr. Bridge"
    role: "Interdisciplinary Researcher"
    perspective: "Values cross-domain connections, synthesis"
    typical_concerns:
      - "How does this connect to other fields?"
      - "What can we learn from [other domain]?"
      - "Are we missing perspectives?"
    feedback_style: "Suggests connections, broadens scope"

  literature_expert:
    icon: "📚"
    name: "Dr. Cite"
    role: "Literature Expert"
    perspective: "Values comprehensive literature grounding"
    typical_concerns:
      - "What does the literature say?"
      - "Have you considered [classic work]?"
      - "How does this fit the existing discourse?"
    feedback_style: "References prior work, situates in context"

  junior_researcher:
    icon: "👨‍🎓"
    name: "Dr. Fresh"
    role: "Junior Researcher"
    perspective: "Values practicality, clarity, accessibility"
    typical_concerns:
      - "How do I actually implement this?"
      - "What are the practical steps?"
      - "Is this feasible with limited resources?"
    feedback_style: "Practical questions, implementation focus"

  emeritus_professor:
    icon: "🏛️"
    name: "Dr. Sage"
    role: "Emeritus Professor"
    perspective: "Values historical context, long-term impact"
    typical_concerns:
      - "How does this fit the field's trajectory?"
      - "What's the lasting contribution?"
      - "Have we seen similar ideas before?"
    feedback_style: "Historical perspective, big picture"

  industry_researcher:
    icon: "🏢"
    name: "Dr. Applied"
    role: "Industry Researcher"
    perspective: "Values practical application, real-world impact"
    typical_concerns:
      - "Can this be applied in practice?"
      - "What's the real-world impact?"
      - "Who will use this?"
    feedback_style: "Application-focused, impact-oriented"
```

## Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│             Community Simulation Process                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ⬜ CP-CS-001: Select personas for feedback                 │
│     - All 7 personas                                        │
│     - Core 3 (Conservative, Innovation, Interdisciplinary) │
│     - Custom selection                                      │
│                                                             │
│         │                                                   │
│         ▼                                                   │
│  For each selected persona:                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 1. Present research proposal to persona             │   │
│  │ 2. Generate persona-specific feedback               │   │
│  │ 3. Identify concerns from their perspective         │   │
│  │ 4. Suggest improvements                             │   │
│  └─────────────────────────────────────────────────────┘   │
│         │                                                   │
│         ▼                                                   │
│  Feedback Compilation:                                      │
│     - Organize by persona                                   │
│     - Identify consensus points                             │
│     - Highlight divergent views                             │
│                                                             │
│  ⬜ CP-CS-002: Select feedback to incorporate               │
│     - Multi-select from feedback items                      │
│                                                             │
│         │                                                   │
│         ▼                                                   │
│  Integration:                                               │
│     - Apply selected feedback                               │
│     - Document rationale for selections                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Output Format

```markdown
## Community Simulation Feedback

### Research Proposal Summary
[Brief description of what was evaluated]

---

### Individual Feedback

#### 🔬 Dr. Method (Conservative Methodologist)
**Overall Assessment**: [Positive/Cautious/Concerned]

**Strengths Noted**:
- [Strength 1]

**Concerns**:
- [Concern 1]: [Explanation]
- [Concern 2]: [Explanation]

**Suggestions**:
- [Suggestion 1]

---

#### 🚀 Dr. Nova (Innovation Seeker)
**Overall Assessment**: [Enthusiastic/Neutral/Disappointed]

**Strengths Noted**:
- [Strength 1]

**Concerns**:
- [Concern 1]: [Explanation]

**Suggestions**:
- [Suggestion 1]

---

[Continue for each selected persona...]

---

### Synthesis

**Consensus Points** (Agreed by 3+ personas):
- [Point 1]
- [Point 2]

**Divergent Views**:
| Topic | Dr. Method | Dr. Nova | Dr. Bridge |
|-------|------------|----------|------------|
| [Topic] | [View] | [View] | [View] |

**Priority Recommendations**:
1. [High priority] - Raised by [X] personas
2. [Medium priority] - Raised by [X] personas

---

### User Selection
[After CP-CS-002, document which feedback was incorporated and why]
```

## Persona Response Templates

Each persona has characteristic phrases and concerns:

```yaml
response_templates:
  conservative_methodologist:
    praise: "The methodological approach is sound because..."
    concern: "I'm concerned about the validity threat from..."
    suggestion: "Consider adding a robustness check for..."

  innovation_seeker:
    praise: "This is a fresh approach that could..."
    concern: "This seems too similar to existing work in..."
    suggestion: "What if we pushed further by..."

  interdisciplinary_researcher:
    praise: "I appreciate the connection to..."
    concern: "We might be missing insights from..."
    suggestion: "Have you considered borrowing from..."

  literature_expert:
    praise: "This builds well on the work of..."
    concern: "The literature actually shows that..."
    suggestion: "You should cite [author] who addressed..."

  junior_researcher:
    praise: "This would be straightforward to implement..."
    concern: "I'm not sure how to actually do..."
    suggestion: "Could you break down the steps for..."

  emeritus_professor:
    praise: "This continues the important tradition of..."
    concern: "We tried something similar in the 1990s..."
    suggestion: "Consider the historical context of..."

  industry_researcher:
    praise: "This could directly impact practice by..."
    concern: "In real-world settings, this might fail because..."
    suggestion: "To make this more applicable, consider..."
```

## Usage Tips

1. **Core 3 for quick feedback**: Conservative + Innovation + Interdisciplinary
2. **All 7 for comprehensive review**: Pre-submission validation
3. **Selective personas for specific needs**: Match persona to concern
4. **Pay attention to consensus**: Points raised by 3+ personas are priority
5. **Don't ignore divergent views**: They reveal complexity
