---
name: vs-engine
description: |
  Enhanced VS 5-Phase Engine with user checkpoints and iteration support.
  Core engine for all VS-enabled agents.
version: "3.0.0"
---

# VS Engine v3.0

## Overview

Enhanced Verbalized Sampling engine with:
- Dynamic T-Score integration
- User checkpoints at critical decision points
- Iterative refinement (Phase 5 → Phase 2 loop)
- Creativity module hooks

## Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│                 VS Engine Execution Flow                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ▶ INITIALIZATION                                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ⬜ CP-INIT-001: Research Type Selection              │   │
│  │    Options: Quantitative / Qualitative / Mixed /    │   │
│  │             Meta-analysis                            │   │
│  │                                                      │   │
│  │ ⬜ CP-INIT-002: Creativity Level Selection           │   │
│  │    Options:                                          │   │
│  │    - Conservative (T≥0.5): Safe, validated          │   │
│  │    - Balanced (T≥0.3): Differentiated + safe        │   │
│  │    - Innovative (T≥0.2): High contribution          │   │
│  │    - Extreme (T<0.2): Maximum creativity            │   │
│  │                                                      │   │
│  │ ⬜ CP-INIT-003: T-Score Mode Selection               │   │
│  │    Options: Static / Dynamic (API) / Hybrid         │   │
│  └─────────────────────────────────────────────────────┘   │
│         │                                                   │
│         ▼                                                   │
│  ▶ PHASE 0: Context Collection (MANDATORY)                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Required:                                            │   │
│  │   - Research domain                                  │   │
│  │   - Research question                                │   │
│  │   - Key variables                                    │   │
│  │   - Target journal level                             │   │
│  │                                                      │   │
│  │ Optional:                                            │   │
│  │   - Existing theory preferences                      │   │
│  │   - Methodology constraints                          │   │
│  └─────────────────────────────────────────────────────┘   │
│         │                                                   │
│         ▼                                                   │
│  ▶ PHASE 1: Modal Response Identification                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Process:                                             │   │
│  │   1. Query T-Score system (static or dynamic)        │   │
│  │   2. Identify top 3-5 modal options (T > 0.8)        │   │
│  │   3. Mark as BASELINE (to be exceeded)               │   │
│  │                                                      │   │
│  │ Output Format:                                       │   │
│  │   ⚠️ MODAL WARNING: These are most predictable:     │   │
│  │   | Option | T-Score | Usage Rate | Issue |          │   │
│  │   |--------|---------|------------|-------|          │   │
│  │   | [X]    | 0.9+    | 60%+       | [Y]   |          │   │
│  └─────────────────────────────────────────────────────┘   │
│         │                                                   │
│         ▼                                                   │
│  ▶ PHASE 2: Long-Tail Sampling (EXPANDED)                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Generate 5-7 directions (expanded from 3):           │   │
│  │                                                      │   │
│  │ Direction A (T≈0.7): Safe differentiation           │   │
│  │ Direction B (T≈0.5): Established but specific       │   │
│  │ Direction C (T≈0.4): Unique and justifiable         │   │
│  │ Direction D (T≈0.3): Emerging approach              │   │
│  │ Direction E (T≈0.2): Innovative                     │   │
│  │ Direction F (T<0.2): Experimental (if Extreme mode) │   │
│  │ Direction G: Cross-domain (if creativity enabled)   │   │
│  │                                                      │   │
│  │ ⬜ CP-VS-001: Direction Selection (multi-select)     │   │
│  │    "Select directions you want to explore further"  │   │
│  └─────────────────────────────────────────────────────┘   │
│         │                                                   │
│         ▼                                                   │
│  ▶ PHASE 3: Low-Typicality Selection                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Selection Criteria:                                  │   │
│  │   1. Academic soundness (peer-review defensible)     │   │
│  │   2. Context fit (alignment with RQ)                 │   │
│  │   3. Contribution potential                          │   │
│  │   4. Feasibility                                     │   │
│  │                                                      │   │
│  │ ⬜ CP-VS-002: Risk Warning (if T < 0.3)              │   │
│  │    "Selected option has T-Score [X]. Limited        │   │
│  │     academic evidence. Proceed?"                     │   │
│  │    Options:                                          │   │
│  │    - Yes, proceed (accept risk)                      │   │
│  │    - Show safer alternatives (T≥0.3)                │   │
│  │    - Show defense rationale first                    │   │
│  └─────────────────────────────────────────────────────┘   │
│         │                                                   │
│         ▼                                                   │
│  ▶ PHASE 4: Execution                                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Execute selected approach with:                      │   │
│  │   - Academic rigor maintained                        │   │
│  │   - Creativity module integration (if enabled)       │   │
│  │   - Detailed output generation                       │   │
│  │                                                      │   │
│  │ Creativity Module Hooks:                             │   │
│  │   {{if forced_analogy_enabled}}                      │   │
│  │     → creativity/forced-analogy.md                   │   │
│  │   {{if iterative_loop_enabled}}                      │   │
│  │     → creativity/iterative-loop.md                   │   │
│  │   {{if semantic_distance_enabled}}                   │   │
│  │     → creativity/semantic-distance.md                │   │
│  │   {{if community_simulation_enabled}}                │   │
│  │     → creativity/community-simulation.md             │   │
│  └─────────────────────────────────────────────────────┘   │
│         │                                                   │
│         ▼                                                   │
│  ▶ PHASE 5: Originality Verification                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Checklist:                                           │   │
│  │   ✅ Modal Avoidance:                                │   │
│  │      - [ ] "Would 80% of AIs recommend this?" → NO  │   │
│  │      - [ ] "Top 5 in similar research?" → NO        │   │
│  │      - [ ] "Reviewer would say 'obvious'?" → NO     │   │
│  │                                                      │   │
│  │   ✅ Quality Check:                                  │   │
│  │      - [ ] Peer-review defensible? → YES            │   │
│  │      - [ ] Validated instruments exist? → YES       │   │
│  │      - [ ] Logical hypothesis derivation? → YES     │   │
│  │                                                      │   │
│  │ ⬜ CP-VS-003: Satisfaction Check                     │   │
│  │    "Are you satisfied with this result?"            │   │
│  │    Options:                                          │   │
│  │    - Yes, complete                                   │   │
│  │    - Re-explore (return to Phase 2)                 │   │
│  │    - Try different approach                          │   │
│  └─────────────────────────────────────────────────────┘   │
│         │                                                   │
│         ▼                                                   │
│  ▶ OUTPUT + SELF-CRITIQUE                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Checkpoint Integration

This engine uses checkpoints from `interaction/user-checkpoints.md`:
- CP-INIT-001, CP-INIT-002, CP-INIT-003 (Initialization)
- CP-VS-001 (Direction Selection)
- CP-VS-002 (Risk Warning)
- CP-VS-003 (Satisfaction Check)

## Creativity Module Integration

When creativity modules are enabled, the engine calls:
- `creativity/forced-analogy.md` - Cross-domain concept mapping
- `creativity/iterative-loop.md` - Divergent-convergent cycles
- `creativity/semantic-distance.md` - Embedding-based recommendations
- `creativity/temporal-reframing.md` - Time perspective shifts
- `creativity/community-simulation.md` - Virtual researcher feedback

## Usage in Agents

```markdown
# In agent SKILL.md:

## VS Engine Execution
{{include: ../../core/vs-engine.md}}

Settings:
  creativity_level: {{user_selected}}
  t_score_mode: {{user_selected}}
  creativity_modules: [forced-analogy, iterative-loop]
```
