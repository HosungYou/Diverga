# Research Coordinator + OMC (oh-my-claudecode) Integration Guide

**Version**: 3.2.0
**Date**: 2025-01-25
**Status**: Production
**Audience**: Research Coordinator users integrating with OMC multi-agent orchestration system

---

## Overview

Research Coordinator is seamlessly integrated with **OMC (oh-my-claudecode)**, a multi-agent orchestration system that enables intelligent agent delegation, parallel execution, and token-efficient model routing.

This integration allows you to:
- **Leverage 21 research agents** through OMC's delegation system
- **Execute agents in parallel** for faster research workflows
- **Save tokens** through intelligent model tier routing (Haiku/Sonnet/Opus)
- **Maintain human agency** with critical checkpoints that require researcher approval
- **Integrate with other OMC skills** for extended capabilities beyond research

### Core Philosophy

> **"AI supports research decisions; researchers make strategic choices."**

Research Coordinator + OMC preserves the fundamental principle: **strategic research decisions remain with the researcher**, while **routine, computational, and analytical tasks are automated**.

---

## Architecture: Research Coordinator in OMC Ecosystem

### Conceptual Model

```
┌─────────────────────────────────────────────────────────────┐
│                   OMC Orchestration Layer                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Skill Routing  →  Model Selection  →  Execution Control   │
│                                                             │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┴────────────────┐
         │                                │
    ┌────▼─────────────┐    ┌───────────▼──────────┐
    │ Research         │    │ Other OMC Skills     │
    │ Coordinator      │    │ (autopilot, ralph,   │
    │ (21 agents)      │    │  ultrawork, etc.)    │
    │                  │    │                      │
    │ - Agent A (Opus) │    │ - frontend-ui-ux     │
    │ - Agent B (Sonnet)    │ - git-master        │
    │ - Agent C (Haiku)     │ - deepsearch        │
    │ [...]           │    │ [...]               │
    └──────────────────┘    └──────────────────────┘
         │
         ├─ CP_RESEARCH_DIRECTION (human decision point)
         ├─ CP_THEORY_SELECTION (human decision point)
         ├─ CP_METHODOLOGY_APPROVAL (human decision point)
         └─ CP_VISUALIZATION_PREFERENCE (human choice)
```

### Two Integration Modes

#### Mode 1: Direct Agent Activation (Recommended for Research)

Researchers invoke agents directly through Research Coordinator's skill interface:

```bash
/research-coordinator
/research-question-refiner
/theoretical-framework-architect
/statistical-analysis-guide
```

**OMC operates transparently in the background:**
- Detects agent invocation
- Routes to appropriate model tier
- Manages parallel execution
- Handles token efficiency

**You don't need to think about OMC** - it's automatic.

#### Mode 2: OMC-First Orchestration (For Complex Workflows)

For advanced users who want explicit control over execution strategy:

```bash
# Using OMC ultrawork mode
/oh-my-claudecode:ultrawork
"Parallel execute: research-coordinator planning phase"

# Using OMC swarm mode (N coordinated agents)
/oh-my-claudecode:swarm 3:research-coordinator
"Execute literature review with 3 parallel agents"
```

**Note**: Most researchers should use Mode 1 (direct invocation). Mode 2 is for power users optimizing complex workflows.

---

## Human Decision Points (Critical Checkpoints)

Research Coordinator enforces **mandatory pause points** where the researcher must make strategic decisions before automation continues.

### CP_RESEARCH_DIRECTION 🔴 (REQUIRED)

**When**: After initial research question exploration (Stage 1)
**What**: Researcher selects among 3-5 candidate research directions
**System Response**: Pauses and waits for selection before proceeding to theory design

**Example**:
```
System: "Three research directions identified:
  Direction A: AI effects on learning achievement
  Direction B: AI effects on student motivation
  Direction C: Comparative analysis (A+B)

  [CP_RESEARCH_DIRECTION]
  Which direction should we pursue?"

Researcher: "Direction A, please"

System: → Proceeds to theoretical framework design
```

### CP_THEORY_SELECTION 🔴 (REQUIRED)

**When**: After theoretical framework exploration (Stage 2)
**What**: Researcher selects a theoretical foundation
**System Response**: Pauses and waits for approval before methodology design

**Example**:
```
System: "Proposed frameworks:
  Option A (T=0.65): TAM × SDT integration (Established)
  Option B (T=0.35): Learning Ecosystem model (Innovative)
  Option C (T=0.15): Neuroplasticity-based framework (Creative)

  Recommendations: Option B balances innovation with
  justifiability for your context.

  [CP_THEORY_SELECTION]
  Do you approve?"

Researcher: "Yes, Option B"

System: → Confirms theoretical foundation, proceeds to design
```

### CP_METHODOLOGY_APPROVAL 🔴 (REQUIRED)

**When**: After methodology design proposal (Stage 3)
**What**: Researcher approves research design and statistical approach
**System Response**: Pauses for explicit approval before implementation planning

**Example**:
```
System: "Proposed methodology:
  - Design: RCT with 2×3 between-subjects
  - Sample size: 300 (n=50 per cell)
  - Analysis: Mixed ANOVA + mediation analysis
  - Timeline: 8 weeks

  [CP_METHODOLOGY_APPROVAL]
  Proceed with this design?"

Researcher: "Adjust sample size to 400"

System: → Recalculates, re-presents, waits for final approval
```

### CP_ANALYSIS_PLAN 🟠 (RECOMMENDED)

**When**: Before statistical implementation (Stage 4)
**What**: Researcher reviews and validates analysis specifications
**Default**: Auto-proceeds if not reviewed, but notification is sent

**Recommendation**: Always review before analysis implementation

### CP_VISUALIZATION_PREFERENCE 🟡 (OPTIONAL)

**When**: During framework visualization (Stage 5)
**What**: Researcher selects visualization style (traditional code vs. AI-generated)
**Default**: Hybrid (ASCII structure + AI rendering)

---

## Model Routing: Token Efficiency

Research Coordinator leverages OMC's model tier system to reduce token consumption while maintaining quality.

### Tier Assignment Logic

```
┌───────────────────────────────────────────────────────────────┐
│         Agent Task → Appropriate Model Tier                  │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  TIER 1: HIGH (Opus) - Strategic Research Decisions           │
│  ─────────────────────────────────────────────────────────   │
│  Agents: 01, 02, 03, 09, 10, 16, 19, 21 (Full VS)           │
│  Cost: $$$  →  Preserve for complex reasoning                │
│                                                               │
│  Task Examples:                                               │
│  - Phase 1-3 of VS workflow (modal identification, sampling)  │
│  - Theory selection and framework design                      │
│  - Study design optimization                                  │
│  - Bias detection and risk assessment                         │
│                                                               │
│  ─────────────────────────────────────────────────────────   │
│                                                               │
│  TIER 2: MEDIUM (Sonnet) - Standard Analysis Tasks            │
│  ─────────────────────────────────────────────────────────   │
│  Agents: 04, 05, 06, 07, 08, 11, 12, 13, 14, 15, 17, 18, 20 │
│  Cost: $$  →  Use for most operational work                  │
│                                                               │
│  Task Examples:                                               │
│  - Literature quality assessment                              │
│  - Effect size extraction and conversion                      │
│  - Statistical test selection and explanation                │
│  - Code generation (R, Python, SPSS)                          │
│  - Document validation and checklist completion              │
│  - Journal matching and reviewer response drafting            │
│                                                               │
│  ─────────────────────────────────────────────────────────   │
│                                                               │
│  TIER 3: LOW (Haiku) - Computational & Search Tasks           │
│  ─────────────────────────────────────────────────────────   │
│  Cost: $  →  Maximum efficiency for routine work              │
│                                                               │
│  Task Examples:                                               │
│  - Literature database searches                               │
│  - Paper screening and deduplication                          │
│  - Statistical calculation and formula application            │
│  - Reference extraction and formatting                        │
│  - Checklist item verification                                │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### Token Savings Estimates

Real-world savings from tiered model routing:

| Task Type | Before (all Opus) | After (Tiered) | Savings | Example |
|-----------|-------------------|----------------|---------|---------|
| Literature search (10 papers) | Opus × 10 | Haiku × 10 | ~80% | Screen + deduplicate |
| Quality assessment (10 studies) | Opus × 10 | Sonnet × 10 | ~50% | RoB + GRADE evaluation |
| Analysis design | Opus × 1 | Opus × 1 | 0% | Strategic work - no change |
| Code generation (3 scripts) | Opus × 3 | Haiku × 3 | ~80% | R/Python template generation |
| **Typical workflow (all stages)** | - | - | **~60%** | Full research pipeline |

### How It Works (Transparent)

You invoke an agent normally:
```
/statistical-analysis-guide
"How should I analyze a 2×3 between-subjects design?"
```

OMC automatically:
1. Detects "statistical analysis guide" invocation
2. Routes Phase 1-3 of VS workflow → Opus (strategic decisions)
3. Routes Phase 4 (implementation) → Sonnet (standard analysis)
4. Routes Phase 5 (validation) → Haiku (computational checks)

**Result**: Better token efficiency, no change to your workflow

---

## Parallel Execution: Workflow Acceleration

Research Coordinator + OMC enables parallel execution of independent agents, reducing total time to completion.

### Parallelizable Agent Groups

```
Phase 1: Research Design Foundation
├─ Sequential: 01 (Research Question Refiner)
│  └─ then: 02 + 03 [PARALLEL]
│     ├─ 02: Theoretical Framework Architect (Full VS)
│     └─ 03: Devil's Advocate (Full VS - challenges framework)
│  then: 04 + 09 [PARALLEL]
│     ├─ 04: Research Ethics Advisor
│     └─ 09: Research Design Consultant
│
Phase 2: Literature Review
├─ Sequential: 05 (Literature Scout - Full VS)
│  then: 06 + 07 + 08 [PARALLEL]
│     ├─ 06: Evidence Quality Appraiser
│     ├─ 07: Effect Size Extractor
│     └─ 08: Research Radar (monitoring)
│
Phase 3: Analysis Design
├─ Sequential: 10 (Statistical Analysis Guide - Full VS)
│  then: 11 + 12 [PARALLEL]
│     ├─ 11: Analysis Code Generator
│     └─ 12: Sensitivity Analysis Designer
│  then: 16 [SEQUENTIAL - Full VS]
│     └─ 16: Bias Detector (final review)
│
Phase 4: Quality Assurance
├─ 13 + 14 + 15 + 16 [ALL PARALLEL]
│  ├─ 13: Internal Consistency Checker
│  ├─ 14: Checklist Manager
│  ├─ 15: Reproducibility Auditor
│  └─ 16: Bias Detector
│
Phase 5: Publication
└─ Sequential: 17 (Journal Matcher)
   then: 18 + 19 [PARALLEL]
      ├─ 18: Academic Communicator
      └─ 19: Peer Review Strategist
   then: 20 + 21 [PARALLEL]
      ├─ 20: Preregistration Composer
      └─ 21: Conceptual Framework Visualizer (Full VS)
```

### Practical Impact

**Without Parallel Execution (Sequential)**:
- Research planning: 1 hour (01→02→03→04→09)
- Literature review: 3 hours (05→06→07→08)
- Analysis design: 1.5 hours (10→11→12→16)
- Quality review: 45 min (13→14→15→16)
- **Total: ~6.25 hours**

**With OMC Parallel Execution**:
- Research planning: 35 min (02+03 in parallel, 04+09 in parallel)
- Literature review: 1.5 hours (06+07+08 in parallel)
- Analysis design: 1 hour (11+12 in parallel)
- Quality review: 15 min (all 4 parallel)
- **Total: ~3.5 hours** ✅ **44% time savings**

### Enabling Parallel Execution

OMC automatically detects parallelizable tasks. No manual configuration needed - just use Research Coordinator normally.

For explicit parallel control:
```bash
# OMC ultrawork mode: maximize parallelism
/oh-my-claudecode:ultrawork
"Help me design my research study"

# OMC ecomode: parallel but token-efficient
/oh-my-claudecode:ecomode
"Conduct systematic literature review"
```

---

## Configuration Files

Research Coordinator + OMC integration is defined through two configuration files:

### 1. Checkpoint Definitions

**Location**: `.omc/checkpoints/checkpoint-definitions.yaml`
**Purpose**: Define mandatory pause points and approval requirements

**Structure**:
```yaml
checkpoints:
  CP_RESEARCH_DIRECTION:
    type: REQUIRED
    stage: "Research Planning"
    description: "Researcher selects among proposed research directions"
    options_format: "3-5 candidate directions with T-scores"
    action_required: "Human selection"

  CP_THEORY_SELECTION:
    type: REQUIRED
    stage: "Theoretical Framework Design"
    description: "Researcher approves theoretical foundation"
    action_required: "Explicit approval or modification request"

  CP_METHODOLOGY_APPROVAL:
    type: REQUIRED
    stage: "Research Design"
    description: "Researcher confirms methodology, sample size, analysis plan"
    action_required: "Approval or design revision request"

  CP_ANALYSIS_PLAN:
    type: RECOMMENDED
    stage: "Statistical Analysis"
    description: "Review analysis specifications"
    default_action: "Auto-proceed with notification"
```

### 2. Parallel Execution Rules

**Location**: `.omc/checkpoints/parallel-execution-rules.yaml`
**Purpose**: Define which agents can execute in parallel

**Structure**:
```yaml
parallel_groups:
  - name: "Research Design Phase 2"
    agents: ["02-theoretical-framework-architect", "03-devils-advocate"]
    dependencies: ["01-research-question-refiner"]
    max_concurrent: 2

  - name: "Literature Review Phase 2"
    agents: ["06-evidence-quality-appraiser", "07-effect-size-extractor", "08-research-radar"]
    dependencies: ["05-systematic-literature-scout"]
    max_concurrent: 3
```

---

## Usage Scenarios

### Scenario 1: Single Agent, OMC Transparency

**Researcher action**:
```
/research-question-refiner

"I want to research AI effects on student learning,
but I'm not sure how to phrase it specifically."
```

**OMC Actions** (transparent, you don't see these):
- Detects agent: research-question-refiner (Enhanced VS)
- Routes to: Sonnet (standard analysis tier)
- Manages: Parallel checks with ethics advisor if needed
- Records: Checkpoint status for workflow tracking

**Outcome**: Clear, PICO/SPIDER-formatted research question, ready for framework design

---

### Scenario 2: Multi-Agent Workflow with Human Decisions

**Researcher action**:
```
/research-coordinator

"I'm designing a study on AI tutors and motivation.
Please help me with the full research planning phase."
```

**System flow**:
```
┌─ Agent 01: Research Question Refinement
│  └─ Result: Specific research question on motivation mediator
│
├─ [CP_RESEARCH_DIRECTION]
│  └─ Researcher selects: "Focus on intrinsic motivation"
│
├─ Agent 02 + 03 [PARALLEL]: Framework Design + Devil's Advocate
│  ├─ 02: Full VS → 3 frameworks proposed (Self-Determination Theory focus)
│  └─ 03: Full VS → Critiques each, identifies gaps
│  └─ Result: Framework validated against challenges
│
├─ [CP_THEORY_SELECTION]
│  └─ Researcher approves: SDT + TAM integration
│
├─ Agent 04 + 09 [PARALLEL]: Ethics Review + Design Consultation
│  ├─ 04: Prepares IRB documentation
│  └─ 09: Proposes RCT design with sample size
│  └─ Result: Methodology plan ready
│
└─ [CP_METHODOLOGY_APPROVAL]
   └─ Researcher reviews and approves design
   └─ System: Ready to proceed to literature review
```

---

### Scenario 3: Token-Efficient Literature Review

**Researcher action**:
```
/systematic-literature-scout

"I need to review studies on AI tutors and motivation.
Help me design a PRISMA-compliant search strategy."
```

**OMC routing**:
- Phase 1-3 (VS workflow): Opus (strategic search strategy)
- Phase 4 (Database screening): Sonnet (quality evaluation)
- Phase 5 (Extraction): Haiku (computational extraction)

**Result**: Comprehensive literature review with 60% lower token usage than all-Opus approach

---

## Migration Guide: Using OMC Features Gradually

If you're new to Research Coordinator + OMC integration, adopt gradually:

### Month 1: Direct Agent Invocation

```bash
# Just call agents normally - no OMC thinking needed
/research-question-refiner
/theoretical-framework-architect
/systematic-literature-scout
```

**OMC benefit you get automatically**: Token-efficient model routing

---

### Month 2: Awareness of Checkpoints

Learn about the critical decision points:
- **CP_RESEARCH_DIRECTION**: What research focus?
- **CP_THEORY_SELECTION**: Which theory?
- **CP_METHODOLOGY_APPROVAL**: What design?

**Your role**: Take time to thoughtfully choose at these checkpoints (don't rush)

---

### Month 3: Parallel Workflows

Use OMC modes for complex projects:
```bash
# For speed on big projects
/oh-my-claudecode:ultrawork
"Design comprehensive research protocol"

# For token efficiency
/oh-my-claudecode:ecomode
"Conduct meta-analysis"
```

---

### Month 4+: Advanced Integration

Combine Research Coordinator with other OMC skills:
```bash
# Integrate with documentation system
/oh-my-claudecode:ultrawork
"Setup: research-coordinator + frontend-ui-ux
for interactive research protocol builder"

# Integrate with version control
/oh-my-claudecode:git-master
"Commit final research protocol: RC Stage 3 complete"
```

---

## Troubleshooting

### Issue: Checkpoints Not Working

**Symptom**: System proceeds without asking for approval at CP_RESEARCH_DIRECTION or CP_THEORY_SELECTION

**Solution**:
1. Verify configuration file exists: `.omc/checkpoints/checkpoint-definitions.yaml`
2. Check OMC plugin status: `claude plugin list | grep omc`
3. Review checkpoint state: `.omc/state/checkpoints.json`

### Issue: Parallel Execution Not Activating

**Symptom**: Agents execute sequentially even when they should run in parallel

**Solution**:
1. Check parallel-execution-rules.yaml configuration
2. Verify agents don't have hidden dependencies
3. Use explicit OMC mode: `/oh-my-claudecode:ultrawork`

### Issue: Token Usage Not Improving

**Symptom**: Using Research Coordinator but tokens still high

**Solution**:
1. Verify model routing is active: Check OMC logs
2. For research planning (02, 03, 10, 16, 21): Opus is correct (don't optimize these)
3. For routine tasks (11-15, 17-20): Should see Haiku/Sonnet usage
4. Check if Full VS agents are being used when Light VS would suffice

### Issue: "CP_RESEARCH_DIRECTION not recognized"

**Symptom**: Error when checkpoint is referenced

**Solution**:
1. Ensure working directory is inside research-coordinator folder
2. Verify `.omc/` directory exists in project root
3. Run initialization: `./scripts/install.sh`

---

## Advanced: Custom Checkpoint Configuration

For users who want custom decision points:

**File**: `.omc/checkpoints/custom-checkpoints.yaml`

```yaml
custom_checkpoints:
  CP_CUSTOM_001:
    name: "Literature Selection Strategy"
    type: PREFERENCE
    trigger_agent: "05-systematic-literature-scout"
    trigger_phase: 2
    options:
      - "Comprehensive (all 5 databases)"
      - "Focused (top 3 databases)"
      - "Targeted (grey literature only)"
```

---

## References

### Official Documentation
- [Research Coordinator README](../README.md)
- [Agent Reference Guide](../AGENT-REFERENCE.md)
- [Usage Examples](../USAGE-EXAMPLES.md)
- [OMC Official Docs](https://github.com/Yeachan-Heo/oh-my-claudecode)

### Research Coordinator Internal Docs
- [VS-Research Framework](../.claude/skills/research-coordinator/core/vs-engine.md)
- [User Checkpoints Specification](../.claude/skills/research-coordinator/interaction/user-checkpoints.md)
- [Agent Registry v3.0](../.claude/skills/research-coordinator/references/agent-registry.yaml)

### Key Papers & Specifications
- **Verbalized Sampling**: arXiv:2510.01171 - Foundation for VS methodology
- **Claude Code Skills**: https://claude.ai/code - Skill system documentation
- **OMC Orchestration**: https://github.com/Yeachan-Heo/oh-my-claudecode - Multi-agent system

---

## Summary Table: Research Coordinator + OMC Integration

| Feature | Without OMC | With OMC | Benefit |
|---------|-------------|----------|---------|
| Agent invocation | Normal | Same | Transparent benefit |
| Model tier routing | All Opus | Haiku/Sonnet/Opus | 60% token savings |
| Parallel execution | Sequential | Parallel groups | 40-50% time savings |
| Human decision points | Manual | Structured checkpoints | Enforced thoughtful selection |
| Cross-skill integration | Limited | Full OMC ecosystem | Extended capabilities |

---

## Getting Started

1. **Install Research Coordinator** (if not already installed):
   ```bash
   git clone https://github.com/HosungYou/research-coordinator.git
   cd research-coordinator
   ./scripts/install.sh
   ```

2. **Verify OMC is active**:
   ```bash
   claude plugin list | grep omc
   ```

3. **Start your first research project**:
   ```
   /research-coordinator
   "Help me design a research study on [your topic]"
   ```

4. **At checkpoints**: Make thoughtful strategic decisions
5. **Let OMC work**: Model routing and parallelism happen automatically

---

**Made for researchers by researchers. Happy researching!** 🧬

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 3.1.0 | 2025-01-25 | Initial OMC integration guide. Added checkpoint definitions, model routing, parallel execution rules. |

