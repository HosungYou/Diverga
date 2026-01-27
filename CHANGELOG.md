# Changelog

All notable changes to Diverga (formerly Research Coordinator) will be documented in this file.

---

## [6.5.1] - 2026-01-27 (Bugfix Release)

### Overview

Fixes critical plugin installation error caused by invalid `runtime` key in marketplace.json schema, and integrates artistic README design with v6.5 content.

### Bug Fixes

#### 🐛 Fixed: `runtime` Key Schema Validation Error

**Error Message**:
```
Error: Invalid schema: plugins.0: Unrecognized key: "runtime"
```

**Root Cause**: The `runtime` object in `marketplace.json` was not part of Claude Code's plugin schema. Unlike expected, Claude Code plugins don't require explicit runtime declarations.

**Solution**: Removed the invalid `runtime` object. The `/agents/` directory alone is sufficient for Task tool registration (same pattern as oh-my-claudecode).

**Before** (❌ Caused Error):
```json
{
  "plugins": [{
    "name": "diverga",
    "source": "./",
    "runtime": {
      "type": "typescript",
      "entry": "./dist/index.js",
      "agents": "./dist/agents/definitions.js"
    },
    "strict": false
  }]
}
```

**After** (✅ Fixed):
```json
{
  "plugins": [{
    "name": "diverga",
    "source": "./",
    "strict": false
  }]
}
```

### Documentation

#### README.md Redesign

Integrated artistic design from v6.4 with v6.5 content:

| Element | Status |
|---------|--------|
| ASCII hero banner (DIVERGA logo) | ✅ Restored |
| VS distribution diagram | ✅ Restored |
| Quote box (Verbalized Sampling) | ✅ Restored |
| Human checkpoint flowchart | ✅ Restored |
| Agent ecosystem diagram (40 agents) | ✅ Restored |
| v6.5 parallel execution content | ✅ Integrated |
| for-the-badge style badges | ✅ Kept |

### Files Changed

| File | Change |
|------|--------|
| `.claude-plugin/marketplace.json` | Removed `runtime` object (5 lines) |
| `README.md` | Integrated artistic design + v6.5 content |

### Verification

```bash
# Test plugin installation
/plugin uninstall diverga
/plugin marketplace add https://github.com/HosungYou/Diverga
/plugin install diverga

# Verify Skill tool
/diverga:setup

# Verify Task tool
Task(subagent_type="diverga:a1", prompt="Test")
```

---

## [6.5.0] - 2026-01-27 (Parallel Execution Edition)

### Overview

Diverga v6.5.0 introduces **Parallel Agent Execution via Task tool**, enabling oh-my-claudecode-compatible agent invocation for simultaneous multi-agent research workflows.

**Core Theme**: "Run multiple research agents in parallel, just like oh-my-claudecode"

### New Features

#### `/agents/` Directory (40 Agent Files)

Direct agent files for Task tool registration, compatible with Claude Code's agent discovery system:

```
agents/
├── a1.md - a6.md    # Category A: Foundation (6 agents)
├── b1.md - b5.md    # Category B: Evidence (5 agents)
├── c1.md - c7.md    # Category C: Design & Meta-Analysis (7 agents)
├── d1.md - d4.md    # Category D: Data Collection (4 agents)
├── e1.md - e5.md    # Category E: Analysis (5 agents)
├── f1.md - f5.md    # Category F: Quality (5 agents)
├── g1.md - g6.md    # Category G: Communication (6 agents)
└── h1.md - h2.md    # Category H: Specialized (2 agents)
```

**Total: 40 agent .md files**

#### Parallel Execution via Task Tool

Run multiple agents simultaneously in a single message:

```python
# Single agent
Task(subagent_type="diverga:a1", prompt="Refine my research question...")

# Parallel execution (single message, multiple Tasks)
Task(subagent_type="diverga:a1", prompt="Research question...")
Task(subagent_type="diverga:a2", prompt="Theoretical framework...")
Task(subagent_type="diverga:a3", prompt="Critical evaluation...")
```

#### oh-my-claudecode Compatible

Same invocation pattern as oh-my-claudecode:

| Feature | Pattern |
|---------|---------|
| Agent invocation | `Task(subagent_type="diverga:a1")` |
| Model specification | `model="opus"` / `"sonnet"` / `"haiku"` |
| Parallel execution | Multiple Task calls in single message |

#### TypeScript Runtime

Programmatic agent access for advanced integrations:

```typescript
import { getAgentDefinitions, getAgent, findAgentByTrigger } from 'diverga';

const agents = getAgentDefinitions();  // All 40 agents
const a1 = getAgent('a1');             // Single agent
const agent = findAgentByTrigger('meta-analysis');  // By keyword
```

### Agent Model Distribution

| Model | Tier | Count | Agents |
|-------|------|-------|--------|
| opus | HIGH | 16 | a1, a2, a3, a5, b5, c1, c2, c3, c5, d4, e1, e2, e3, g6, h1, h2 |
| sonnet | MEDIUM | 17 | a4, a6, b1, b2, c4, c6, c7, d1, d2, e5, f3, f4, g1, g2, g3, g4, g5 |
| haiku | LOW | 7 | b3, b4, d3, e4, f1, f2, f5 |

### Agent File Format

Each agent file uses YAML frontmatter + Markdown:

```markdown
---
name: a1
description: VS-Enhanced Research Question Refiner
model: opus
tools: Read, Glob, Grep, WebSearch
---

# Research Question Refiner

**Agent ID**: A1
**Category**: A - Theory & Design
**VS Level**: Enhanced (3-Phase)
**Tier**: HIGH (Opus)

## Overview
...

## Human Checkpoint Protocol
...
```

### Dual Invocation Support

Both invocation patterns work:

| Method | Pattern | Status |
|--------|---------|--------|
| **Skill tool** | `/diverga:A1-research-question-refiner` | ✅ Works |
| **Task tool** | `Task(subagent_type="diverga:a1")` | ✅ Works (after v6.5.0) |

### New Files

| File | Purpose |
|------|---------|
| `agents/*.md` (40 files) | Task tool agent definitions |
| `src/agents/types.ts` | TypeScript type definitions |
| `src/agents/definitions.ts` | Agent registry and API |
| `src/agents/prompt-loader.ts` | SKILL.md parser with VS injection |
| `package.json` | npm package configuration |
| `tsconfig.json` | TypeScript configuration |

### Installation Note

After updating to v6.5.0, reinstall the plugin to enable Task tool agents:

```bash
/plugin reinstall diverga
```

### No Breaking Changes

Existing Skill-based workflows continue unchanged. Task tool is additive.

---

## [6.4.0] - 2026-01-27 (Plugin Marketplace Edition)

### Overview

Diverga v6.4.0 introduces **Plugin Marketplace Registration**, enabling installation via Claude Code's plugin system with auto-trigger agent dispatch.

**Core Theme**: "Install once, auto-execute everywhere"

### Installation (NEW)

```bash
# Step 1: Add to marketplace
/plugin marketplace add https://github.com/HosungYou/Diverga

# Step 2: Install
/plugin install diverga

# Step 3: Setup
/diverga:setup
```

### New Skills

| Skill | Command | Description |
|-------|---------|-------------|
| Setup | `/diverga:setup` | Interactive configuration wizard |
| Help | `/diverga:help` | Comprehensive 40-agent reference |
| Meta-Analysis | `/diverga:meta-analysis` | C5+C6+C7 workflow |
| PDF Extract | `/diverga:pdf-extract` | C6 data extraction |

### New Files

| File | Purpose |
|------|---------|
| `PLUGIN.md` | Plugin marketplace definition |
| `.claude/skills/setup/SKILL.md` | Setup wizard implementation |
| `.claude/skills/help/SKILL.md` | Help skill implementation |

### Auto-Trigger Agent Dispatch

All 40 agents now have keyword-based auto-trigger patterns in CLAUDE.md:

| Example Keywords | Agent Triggered |
|------------------|-----------------|
| "research question", "RQ", "연구 질문" | diverga:a1 |
| "meta-analysis", "메타분석" | diverga:c5 |
| "data extraction", "PDF extract" | diverga:c6 |
| "systematic review", "PRISMA" | diverga:b1 |
| "qualitative", "interview" | diverga:c2 |

### Task Tool Invocation

Agents invoked via Task tool with `subagent_type` parameter:

```python
Task(
    subagent_type="diverga:c5",
    model="opus",
    description="Meta-analysis orchestration",
    prompt="Validate the extracted effect sizes..."
)
```

### Model Routing Reference

| Tier | Model | Agents |
|------|-------|--------|
| HIGH | opus | A1,A2,A3,A5,B5,C1,C2,C3,C5,D4,E1,E2,E3,G6,H1,H2 |
| MEDIUM | sonnet | A4,A6,B1,B2,C4,C6,C7,D1,D2,E5,F3,F4,G1-G5 |
| LOW | haiku | B3,B4,D3,E4,F1,F2,F5 |

### Setup Wizard Flow

1. **LLM API Selection**: Anthropic/OpenAI/Groq/Local
2. **Human Checkpoints**: Enable/Disable mandatory stops
3. **Research Paradigm**: Quantitative/Qualitative/Mixed/Auto
4. **Language**: English/Korean/Auto

### Configuration

Generated config file: `~/.claude/plugins/diverga/config/diverga-config.json`

### No Breaking Changes

Existing workflows continue unchanged. Plugin installation is additive.

---

## [6.3.0] - 2026-01-26 (Multi-Gate Validation Pipeline)

### Overview

Diverga v6.3.0 introduces the **Multi-Gate Validation Pipeline** for meta-analysis extraction, incorporating lessons learned from the V7 project to prevent common extraction errors.

**Core Theme**: "Every effect size must pass through all 4 gates before inclusion"

### Added

#### Multi-Gate Validation Pipeline

4-gate validation system to ensure extraction quality:

| Gate | Name | Key Checks |
|------|------|------------|
| Gate 1 | Extraction Validation | Data completeness, design classification, source verification |
| Gate 2 | Classification Validation | Outcome type, comparison type, **Effect Size Hierarchy** |
| Gate 3 | Statistical Validation | Hedges' g verification, SE calculation, outlier detection |
| Gate 4 | Independence Validation | Pre-test exclusion, dependency handling |

#### Effect Size Selection Hierarchy (V7 Lesson)

Priority-based selection when multiple effect sizes are available:

| Priority | Type | Use When |
|----------|------|----------|
| 1 (Best) | Post-test between-groups | Control group exists |
| 2 | ANCOVA-adjusted | Pre-test as covariate |
| 3 | Change score | No between-group post available |
| 4 (Last) | Single-group pre-post | No control group |

**Critical Rule**: Pre-test scores NEVER as independent outcomes

#### New Checkpoints

| Checkpoint | Level | Trigger |
|------------|-------|---------|
| CP_SOURCE_VERIFY | REQUIRED | After data extraction |
| CP_ES_HIERARCHY | REQUIRED | Study has >1 potential ES |
| CP_PRETEST_REJECT | AUTO | Pre-test detected as outcome |
| CP_EXTREME_VALUE | CONDITIONAL | \|g\| > 2.0 |
| CP_DEPENDENCY_HANDLING | REQUIRED | >1 ES from same study |

#### Hedges' g Verification

Mandatory verification with tolerance < 0.01:

```python
def verify_hedges_g(d, n1, n2):
    df = n1 + n2 - 2
    J = 1 - (3 / (4 * df - 1))
    g = d * J
    SE_g = sqrt((n1 + n2) / (n1 * n2) + g**2 / (2 * (n1 + n2)))
    return {'g': g, 'SE': SE_g, 'J': J}
```

### Changed

#### B3-EffectSizeExtractor

- Added Effect Size Selection Hierarchy section
- Added Pre-test Exclusion Patterns (regex)
- Added Cohen's d to Hedges' g verification requirement
- Added CP_ES_HIERARCHY checkpoint integration

#### B2-EvidenceQualityAppraiser

- Added Extraction Quality Validation section
- Added Statistical Consistency Checks table
- Added Effect Size Quality Rating (HIGH/MEDIUM/LOW/UNACCEPTABLE)
- Added Quality Validation Checklist

#### pipeline-templates.md

- Added Template 4: Multi-Gate Meta-Analysis Extraction Pipeline
- Added 4-gate workflow structure with checkpoints
- Added forbidden patterns section

#### user-checkpoints.md

- Added 5 new meta-analysis checkpoints
- Added Meta-Analysis Checkpoint Sequence
- Updated Checkpoint Registry

### V7 Lessons Integrated

| Lesson | Implementation |
|--------|----------------|
| Pre-test as outcome | AUTO-REJECT with CP_PRETEST_REJECT |
| Hierarchy violation | Mandatory CP_ES_HIERARCHY checkpoint |
| Unverified conversion | Tolerance check (< 0.01) required |
| Missing dependency handling | CP_DEPENDENCY_HANDLING enforced |

### No Breaking Changes

Existing workflows continue unchanged. Multi-Gate Pipeline is an additional template for meta-analysis projects.

---

## [6.1.0] - 2025-01-26 (Human-Centered Edition + Humanization Pipeline)

### Overview

Diverga v6.1.0 introduces the **Humanization Pipeline**, a comprehensive system for transforming AI-generated academic text into natural, human-sounding prose while preserving scholarly integrity.

**Core Theme**: "Humanization improves expression, not deception"

### New Agents (+3)

| Agent ID | Name | Model | Purpose |
|----------|------|-------|---------|
| G5 | Academic Style Auditor | Sonnet | AI pattern detection (24 categories) |
| G6 | Academic Style Humanizer | Opus | Pattern transformation |
| F5 | Humanization Verifier | Haiku | Quality verification |

**Total Agents**: 33 → 36

### New Features

#### Humanization Pipeline

```
Content Generation → G5 Analysis → Checkpoint → G6 Transform → F5 Verify → Export
```

- **24 AI Pattern Categories**: Content (C1-C6), Language (L1-L6), Style (S1-S6), Communication (M1-M3), Hedging (H1-H3), Academic (A1-A6)
- **3 Transformation Modes**: Conservative (journal submissions), Balanced (default), Aggressive (informal)
- **Preservation Rules**: 100% citation and statistics integrity

#### New Checkpoints

| Checkpoint | Level | Trigger |
|------------|-------|---------|
| CP_HUMANIZATION_REVIEW | 🟠 Recommended | After G5 analysis |
| CP_HUMANIZATION_VERIFY | 🟡 Optional | After G6 transformation |

#### Ethics Framework

- AI writing ethics guidelines
- Disclosure templates (journal, conference, thesis)
- Red lines for prohibited uses

### New Files Created

| File | Purpose |
|------|---------|
| `G5-academic-style-auditor/SKILL.md` | Main skill definition |
| `G5-academic-style-auditor/patterns/*.yaml` | Pattern definitions (4 files) |
| `G5-academic-style-auditor/detection-rules.md` | Detection algorithm |
| `G6-academic-style-humanizer/SKILL.md` | Main skill definition |
| `G6-academic-style-humanizer/transformations/*.yaml` | Mode definitions (3 files) |
| `G6-academic-style-humanizer/academic-exceptions.md` | Preservation rules |
| `F5-humanization-verifier/SKILL.md` | Verification skill |
| `research-coordinator/core/humanization-pipeline.md` | Pipeline architecture |
| `research-coordinator/ethics/ai-writing-ethics.md` | Ethics framework |
| `docs/v6.1.0-humanization-pipeline.md` | Comprehensive documentation |

### Modified Files

| File | Changes |
|------|---------|
| `CLAUDE.md` | v6.1.0, 36 agents, Humanization Pipeline section |
| `agent-registry.yaml` | Added G5, G6, F5; updated model routing and checkpoints |
| `G2-academic-communicator/SKILL.md` | Humanization integration |
| `G3-peer-review-strategist/SKILL.md` | Humanization for response letters |
| `integration-hub.md` | Humanization tools section |

### Model Routing (Updated)

| Tier | Model | Agents |
|------|-------|--------|
| HIGH | Opus | A2, A5, B1, C2, C3, E1, E2, E3, F4, **G6**, H1 |
| MEDIUM | Sonnet | A1, A3, A4, B2, B3, B4, C1, C4, D1, D2, D3, D4, E4, G3, **G5**, H2 |
| LOW | Haiku | F1, F2, F3, **F5**, G1, G2, G4 |

### Usage

```
"Check AI patterns"           → G5 analysis only
"Humanize my draft"           → Full pipeline (balanced)
"Humanize (conservative)"     → Minimal changes
"Export with humanization"    → Pipeline before export
```

### No Breaking Changes

Existing workflows continue unchanged. Humanization is opt-in.

---

## [6.0.1] - 2025-01-25 (Human-Centered Edition - Restructure)

### Overview

Agent restructuring with category-based naming convention (A1-H2).

### Changes

- Agent IDs standardized: A1-A5, B1-B4, C1-C4, D1-D4, E1-E4, F1-F4, G1-G4, H1-H2
- Legacy numeric IDs (01-21) deprecated but retained for compatibility
- 33 total agents across 8 categories

---

## [6.0.0] - 2025-01-25 (Human-Centered Edition - Clean Slate)

### Overview

**Clean Slate Release** - Removed autonomous modes to enforce mandatory human checkpoints.

**Core Theme**: "Human decisions remain with humans. AI handles what's beyond human scope."

### Removed

| Component | Reason |
|-----------|--------|
| ❌ Sisyphus Protocol | Bypassed human checkpoints |
| ❌ Iron Law of Continuation | "OR" made checkpoints optional |
| ❌ ralph/ultrawork/autopilot/ecomode | Enabled checkpoint bypass |

### Kept

| Component | Purpose |
|-----------|---------|
| ✅ Model Routing | haiku/sonnet/opus selection |
| ✅ VS Methodology | Creative alternatives, T-Scores |
| ✅ Paradigm Detection | Auto-detection with confirmation |
| ✅ Human Checkpoints | Now MANDATORY |

### Checkpoint Behavior (Strict)

```
When AI reaches a checkpoint:
1. STOP immediately
2. Present options with VS alternatives
3. WAIT for explicit human approval
4. DO NOT proceed until approval received
5. DO NOT assume approval based on context

❌ NEVER: "진행하겠습니다" without asking
✅ ALWAYS: "어떤 방향으로 진행하시겠습니까?"
```

### Breaking Changes

- Autonomous execution modes no longer available
- All critical decisions require explicit user approval
- Workflow continues only after checkpoint approval

---

## [5.0.0] - 2025-01-25 (Sisyphus Edition)

### Overview

Diverga v5.0.0 represents a major architectural redesign, expanding from 21 to 27 agents across 8 categories (A-H). This release introduces the Sisyphus continuation enforcement pattern, automatic paradigm detection, and comprehensive support for qualitative and mixed methods research.

**Core Theme**: "Beyond Modal - Creative, Defensible Research Choices"

### Project Renamed: Research Coordinator → Diverga

This release marks the **official renaming** of the project to **Diverga** to better reflect its core mission:

- **"Diverga"** = Divergent thinking, breaking free from the obvious
- **Breaking free from mode collapse** through Verbalized Sampling (VS) methodology
- **T-Score system** for rating typicality of recommendations (0-1 scale)
- **5 Creativity Mechanisms**: Forced Analogy, Iterative Refinement, Semantic Distance, Temporal Reframing, Community Simulation

### New Features

#### Verbalized Sampling (VS) Methodology

Diverga's **core innovation** that prevents mode collapse:

| T-Score | Interpretation | Diverga Behavior |
|---------|----------------|---------------------|
| `T > 0.8` | Modal (predictable) | ⚠️ Flags and warns about differentiation |
| `T 0.5-0.8` | Established alternative | ✅ Suggests as balanced choice |
| `T 0.3-0.5` | Emerging approach | ✅ Recommends for innovation |
| `T < 0.3` | Novel/creative | 🔬 Presents with strong rationale |

#### Sisyphus Protocol

### New Features

#### Sisyphus Protocol

Adopted from oh-my-opencode, the Sisyphus protocol enforces continuation until verified completion:

- **Continuation Enforcement**: Research work never stops until paradigm-specific completion criteria are met
- **Verification Before Completion**: Every claim of "done" requires fresh evidence
- **Paradigm-Specific Criteria**: Different completion checklists for quantitative, qualitative, and mixed methods

**Completion Criteria by Paradigm**:

| Paradigm | Key Criteria |
|----------|-------------|
| Quantitative | Hypotheses tested, power analysis done, effect sizes reported, visualizations generated |
| Qualitative | Saturation documented, themes refined, trustworthiness criteria met, member checking completed |
| Mixed Methods | Both strands complete, integration strategy documented, joint display created, meta-inference generated |

#### Paradigm Auto-Detection

Automatic detection of research paradigm based on conversation keywords:

- **Quantitative Signals**: "hypothesis", "effect size", "p-value", "ANOVA", "regression", "가설", "효과크기"
- **Qualitative Signals**: "lived experience", "saturation", "themes", "phenomenology", "체험", "포화"
- **Mixed Methods Signals**: "sequential", "convergent", "integration", "joint display", "혼합방법"

#### Smart Model Routing (Updated)

| Tier | Model | Agent Types |
|------|-------|-------------|
| HIGH | Opus | Complex interpretive work, philosophical reasoning (A2, A5, C2, C3, E2, E3, H1-H4) |
| MEDIUM | Sonnet | Standard research tasks (A1, A3, A4, B1, B2, C1, C4, D1-D4, E1, E4, F2, F4, G2, G3) |
| LOW | Haiku | Quick lookups, formatting, checklists (B3, B4, F1, F3, G1, G4) |

### Agent Expansion (21 → 33)

#### Category Structure

| Category | Name | Agent Count | Description |
|----------|------|-------------|-------------|
| A | Foundation | 5 | Research question, theory, ethics, paradigm |
| B | Evidence | 4 | Literature review, quality appraisal, effect sizes |
| C | Design | 4 | Quantitative, qualitative, mixed methods design |
| D | Data Collection | 4 | Sampling, interviews, observation, instruments |
| E | Analysis | 4 | Statistical, coding, integration, code generation |
| F | Quality | 4 | Sensitivity, checklists, reproducibility, bias |
| G | Communication | 4 | Journal matching, writing, peer review, preregistration |
| H | Specialized | 4 | Ethnography, narrative, grounded theory, action research |

### New Agents (12 Total)

#### Category A: Foundation (+1)

| Agent ID | Name | Purpose | Tier |
|----------|------|---------|------|
| A5 | Paradigm & Worldview Advisor | Ontology, epistemology, paradigm selection | HIGH |

#### Category C: Design (+3)

| Agent ID | Name | Purpose | Tier |
|----------|------|---------|------|
| C2 | Qualitative Design Consultant | Phenomenology, grounded theory, case study, narrative | HIGH |
| C3 | Mixed Methods Design Consultant | Sequential, convergent, embedded, transformative designs | HIGH |
| C4 | Experimental Materials Developer | Treatment protocols, control conditions, manipulation checks | MEDIUM |

#### Category D: Data Collection (+4, New Category)

| Agent ID | Name | Purpose | Tier |
|----------|------|---------|------|
| D1 | Sampling Strategy Advisor | Probability, purposive, theoretical sampling | MEDIUM |
| D2 | Interview & Focus Group Specialist | Interview protocols, focus groups, transcription | MEDIUM |
| D3 | Observation Protocol Designer | Field notes, structured observation, video analysis | MEDIUM |
| D4 | Measurement Instrument Developer | Scale construction, validity, reliability | MEDIUM |

#### Category E: Analysis (+2)

| Agent ID | Name | Purpose | Tier |
|----------|------|---------|------|
| E2 | Qualitative Coding Specialist | Thematic analysis, grounded theory coding, saturation | HIGH |
| E3 | Mixed Methods Integration Specialist | Joint displays, meta-inference, legitimation | HIGH |

#### Category H: Specialized (+4, New Category)

| Agent ID | Name | Purpose | Tier |
|----------|------|---------|------|
| H1 | Ethnographic Research Advisor | Fieldwork, participant observation, thick description | HIGH |
| H2 | Action Research Facilitator | PAR, CBPR, action cycles, community engagement | MEDIUM |
| H3 | Grounded Theory Advisor | Constant comparison, theoretical sampling, theory development | HIGH |
| H4 | Narrative Analysis Specialist | Narrative inquiry, life history, autoethnography | HIGH |

### Extended Agents (5 Total)

#### B1: Systematic Literature Scout → Literature Review Strategist

**Added Capabilities**:
- Scoping reviews (JBI, PRISMA-ScR)
- Meta-synthesis (meta-ethnography, thematic synthesis)
- Realist synthesis (RAMESES)
- Narrative reviews (critical, integrative)
- Rapid reviews

#### C1: Research Design Consultant → Quantitative Design Consultant

**Changes**:
- Focused exclusively on quantitative research designs
- Split qualitative and mixed methods to C2 and C3
- Added paradigm_affinity: [quantitative]

#### E1: Statistical Analysis Guide → Quantitative Analysis Guide

**Added Capabilities**:
- Qualitative analysis methods (thematic, grounded theory, content, narrative)
- Bayesian statistics section
- Machine learning for research

#### E4: Analysis Code Generator

**Added Capabilities**:
- CAQDAS support: NVivo, ATLAS.ti, MAXQDA
- R qualitative packages: RQDA, qualitativeR
- Mixed methods visualization code

#### F4: Bias Detector → Bias & Trustworthiness Detector

**Added Capabilities**:
- Qualitative trustworthiness criteria (Lincoln & Guba)
  - Credibility, Transferability, Dependability, Confirmability
- Reflexivity guidelines
- COREQ, SRQR, GRAMMS checklists

### Core Infrastructure Changes

#### New Files Created

| File | Purpose |
|------|---------|
| `.claude/skills/research-coordinator/core/paradigm-detector.md` | Auto-detection rules and agent pack activation |
| `.claude/skills/research-agents/A5-paradigm-worldview-advisor/SKILL.md` | Paradigm/worldview selection |
| `.claude/skills/research-agents/C2-qualitative-design-consultant/SKILL.md` | Qualitative design support |
| `.claude/skills/research-agents/C3-mixed-methods-design-consultant/SKILL.md` | Mixed methods design |
| `.claude/skills/research-agents/C4-experimental-materials-developer/SKILL.md` | Experimental materials |
| `.claude/skills/research-agents/D1-sampling-strategy-advisor/SKILL.md` | Sampling strategies |
| `.claude/skills/research-agents/D2-interview-focus-group-specialist/SKILL.md` | Interviews/focus groups |
| `.claude/skills/research-agents/D3-observation-protocol-designer/SKILL.md` | Observation protocols |
| `.claude/skills/research-agents/D4-measurement-instrument-developer/SKILL.md` | Instrument development |
| `.claude/skills/research-agents/E2-qualitative-coding-specialist/SKILL.md` | Qualitative coding |
| `.claude/skills/research-agents/E3-mixed-methods-integration/SKILL.md` | Mixed methods integration |
| `.claude/skills/research-agents/H1-ethnographic-research-advisor/SKILL.md` | Ethnographic research |
| `.claude/skills/research-agents/H2-action-research-facilitator/SKILL.md` | Action research |

#### Modified Files

| File | Changes |
|------|---------|
| `.claude/skills/research-coordinator/SKILL.md` | v5.0.0 with Sisyphus protocol, paradigm detection |
| `.claude/skills/research-coordinator/references/agent-registry.yaml` | Complete rewrite for 33 agents |
| `.claude/skills/research-agents/05-systematic-literature-scout/SKILL.md` | Extended review types |
| `.claude/skills/research-agents/09-research-design-consultant/SKILL.md` | Quantitative focus |
| `.claude/skills/research-agents/10-statistical-analysis-guide/SKILL.md` | Added qualitative methods |
| `.claude/skills/research-agents/11-analysis-code-generator/SKILL.md` | CAQDAS support |
| `.claude/skills/research-agents/16-bias-detector/SKILL.md` | Trustworthiness criteria |
| `README.md` | Updated to v5.0.0 |
| `AGENTS.md` | AI-readable registry update |
| `CLAUDE.md` | Project instructions update |

### Research Types Now Supported

#### Quantitative Research
- Experimental designs (RCT, quasi-experimental)
- Survey research
- Meta-analysis and systematic reviews
- Correlational studies
- Psychometric validation

#### Qualitative Research (NEW)
- Phenomenology (descriptive, interpretive, hermeneutic)
- Grounded theory (Straussian, Charmazian, classic)
- Case study (single, multiple, intrinsic, instrumental)
- Ethnography (traditional, focused, critical, digital)
- Narrative inquiry (life history, autoethnography)
- Action research (PAR, CBPR)

#### Mixed Methods Research (NEW)
- Sequential explanatory
- Sequential exploratory
- Convergent parallel
- Embedded design
- Transformative frameworks

### Human Checkpoints (Updated)

| Level | Checkpoints | Action |
|-------|-------------|--------|
| 🔴 REQUIRED | CP_RESEARCH_DIRECTION, CP_THEORY_SELECTION, CP_METHODOLOGY_APPROVAL | User approval required |
| 🟠 RECOMMENDED | CP_ANALYSIS_PLAN, CP_QUALITY_REVIEW | Review recommended |
| 🟡 OPTIONAL | CP_VISUALIZATION_PREFERENCE, CP_RENDERING_METHOD | Defaults available |

### Validation

All 33 agents pass contract validation:

```bash
python scripts/validate_agents.py
# Summary: 33/33 agents passed validation
# ✅ All agents passed validation!
```

### Breaking Changes

- Agent IDs changed from numeric (01-21) to include category-based (A1-H4)
- Some agents split or renamed (see Extended Agents section)
- New required frontmatter fields: `upgrade_level`, `v3_integration`

### Migration from v4.x

1. **Agent Registry**: The 21 agents remain with original IDs; new agents use category IDs (A5, C2-C4, D1-D4, E2-E3, H1-H4)
2. **Paradigm Detection**: Automatically activates appropriate agent packs
3. **Sisyphus Protocol**: All workflows now include verification-before-completion
4. **Frontmatter**: All SKILL.md files require `upgrade_level` and `v3_integration` fields

---

## [3.2.0] - 2025-01-25

### Added

#### OMC (oh-my-claudecode) Integration
- **21 OMC Agent Definition Files** (`.omc/agents/research/01-21`)
  - Each agent has: tier, model, category, parallel_group, human_checkpoint, triggers
  - Follows OMC agent specification format

- **Human Checkpoint System** (`.omc/checkpoints/`)
  - `checkpoint-definitions.yaml`: 7 checkpoints across 3 levels
    - 🔴 REQUIRED: CP_RESEARCH_DIRECTION, CP_THEORY_SELECTION, CP_METHODOLOGY_APPROVAL
    - 🟠 RECOMMENDED: CP_ANALYSIS_PLAN, CP_QUALITY_REVIEW
    - 🟡 OPTIONAL: CP_VISUALIZATION_PREFERENCE, CP_RENDERING_METHOD
  - `checkpoint-handler.md`: Implementation protocol for checkpoint handling
  - `parallel-execution-rules.yaml`: 10 parallel execution groups with checkpoint boundaries

- **Model Routing Configuration** (`.omc/config/research-coordinator-routing.yaml`)
  - HIGH tier (Opus): #01, #02, #03, #09, #19 - Strategic decisions
  - MEDIUM tier (Sonnet): #04, #06, #10, #12, #15-18, #20, #21 - Standard analysis
  - LOW tier (Haiku): #05, #07, #08, #11, #13, #14 - Search, calculation, code
  - ~60% token savings compared to all-Opus approach

- **Research Orchestrator Skill** (`.omc/skills/research-orchestrator/SKILL.md`)
  - Coordinates Diverga with OMC execution modes
  - Agent-tier quick reference table
  - Integration with ultrawork, ecomode, ralph modes

- **Comprehensive Documentation** (`docs/omc-integration.md`)
  - 450+ line guide for OMC integration
  - Usage scenarios, configuration references
  - Migration guide and troubleshooting

### Changed

- **CLAUDE.md**: Added OMC Integration v3.2.0 section
- **SKILL.md**: Updated to v3.2.0 with OMC integration, model routing table, checkpoint references

### Core Principle

> **"인간이 할 일은 인간이, AI는 인간의 범주를 벗어난 것을 수행"**
> (Human decisions MUST be respected, AI only handles tasks beyond human scope)

### Compatibility

- **Backwards Compatible**: Works with Claude Code alone (no OMC required)
- **Enhanced with OMC**: Parallel execution, smart model routing, token efficiency

---

## [3.1.0] - Previous Release

- 21 research agents across 5 categories (A-E)
- VS-Research (Verbalized Sampling) methodology
- Nanobanana integration for visualizations
- Claude Code Skills system support

---

## File Structure (v5.0.0)

```
research-coordinator/
├── .claude/skills/
│   ├── research-coordinator/         # Master skill
│   │   ├── SKILL.md                  # v5.0.0 Sisyphus Edition
│   │   ├── core/
│   │   │   └── paradigm-detector.md  # Auto-detection rules
│   │   └── references/
│   │       └── agent-registry.yaml   # 33 agents
│   └── research-agents/              # 33 individual agents
│       ├── 01-21/                    # Original agents (extended)
│       ├── A5-paradigm-worldview-advisor/
│       ├── C2-qualitative-design-consultant/
│       ├── C3-mixed-methods-design-consultant/
│       ├── C4-experimental-materials-developer/
│       ├── D1-sampling-strategy-advisor/
│       ├── D2-interview-focus-group-specialist/
│       ├── D3-observation-protocol-designer/
│       ├── D4-measurement-instrument-developer/
│       ├── E2-qualitative-coding-specialist/
│       ├── E3-mixed-methods-integration/
│       ├── H1-ethnographic-research-advisor/
│       └── H2-action-research-facilitator/
├── .omc/                             # OMC Integration
│   ├── agents/research/              # OMC agent definitions
│   ├── checkpoints/                  # Human checkpoint system
│   ├── config/                       # Model routing
│   └── skills/                       # Research orchestrator
├── docs/
│   └── omc-integration.md            # OMC integration guide
├── scripts/
│   └── validate_agents.py            # Agent validation script
├── CHANGELOG.md                      # This file
├── CLAUDE.md                         # Project instructions
├── AGENTS.md                         # AI-readable registry
└── README.md
```

---

## Agent Summary (v5.0.0)

| Category | ID Range | Count | Tier Distribution |
|----------|----------|-------|-------------------|
| A: Foundation | A1-A5 (01-04 + A5) | 5 | 2 HIGH, 3 MEDIUM |
| B: Evidence | B1-B4 (05-08) | 4 | 2 MEDIUM, 2 LOW |
| C: Design | C1-C4 (09 + C2-C4) | 4 | 2 HIGH, 2 MEDIUM |
| D: Data Collection | D1-D4 | 4 | 4 MEDIUM |
| E: Analysis | E1-E4 (10-11 + E2-E3) | 4 | 2 HIGH, 2 MEDIUM |
| F: Quality | F1-F4 (12-16) | 4 | 1 MEDIUM, 3 LOW |
| G: Communication | G1-G4 (17-20) | 4 | 2 MEDIUM, 2 LOW |
| H: Specialized | H1-H4 | 4 | 3 HIGH, 1 MEDIUM |
| **Total** | | **33** | **11 HIGH, 14 MEDIUM, 8 LOW** |

---

## Usage (v5.0.0)

### Basic Mode
```bash
/research-coordinator
```

### With OMC (Enhanced Mode)
```bash
ulw: 문헌 검색해줘     # Maximum parallelism
eco: 통계 분석해줘     # Token efficient
ralph: 연구 설계해줘   # Persistence until done
```

### Paradigm-Specific Invocation
```
"현상학적 연구 설계해줘"      # → Qualitative pack activated (C2, E2, D2)
"혼합방법 연구 통합해줘"      # → Mixed methods pack activated (C3, E3)
"메타분석 효과크기 추출"      # → Quantitative pack activated (C1, E1, B3)
```

---

## Contributors

- Diverga v5.0.0 design based on oh-my-opencode Sisyphus pattern
- Benchmarked against: Agent Laboratory, LLM-SLR, Agentic Research Lab
- Implementation: Claude Opus 4.5 with OMC orchestration
- Architect Verification: Passed
