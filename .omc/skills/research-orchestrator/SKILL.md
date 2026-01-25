---
name: research-orchestrator
version: 1.0.0
description: |
  OMC-powered orchestrator for Research Coordinator
  Manages 21 research agents with human checkpoints and parallel execution
---

# Research Orchestrator

**Core Principle**: 인간이 할 일은 인간이, AI는 인간 범위를 벗어난 작업 수행

## Purpose

Research Coordinator의 21개 에이전트를 OMC 시스템과 통합하여 관리합니다.

## Workflow

### 1. Request Analysis

```
User Request
    ↓
Pattern Matching (auto_triggers)
    ↓
Identify Required Agents
    ↓
Check for Checkpoints
```

### 2. Checkpoint Handling

**REQUIRED (🔴)** - System STOPS
- CP_RESEARCH_DIRECTION
- CP_THEORY_SELECTION
- CP_METHODOLOGY_APPROVAL

**RECOMMENDED (🟠)** - System pauses
- CP_ANALYSIS_PLAN
- CP_QUALITY_REVIEW

**OPTIONAL (🟡)** - Default if skipped
- CP_VISUALIZATION_PREFERENCE
- CP_RENDERING_METHOD

### 3. Parallel Execution

When multiple agents can run in parallel:

```
[Checkpoint Approved]
    ↓
Spawn Parallel Agents:
├── Task(agent_01, model=tier, run_in_background=true)
├── Task(agent_02, model=tier, run_in_background=true)
└── Task(agent_03, model=tier, run_in_background=true)
    ↓
Wait for Completion
    ↓
Integrate Results
    ↓
[Next Checkpoint or Output]
```

### 4. Model Routing

Always pass `model` parameter explicitly:

```
# HIGH tier agents
Task(subagent_type="oh-my-claudecode:architect", model="opus", ...)

# MEDIUM tier agents
Task(subagent_type="oh-my-claudecode:executor", model="sonnet", ...)

# LOW tier agents
Task(subagent_type="oh-my-claudecode:executor-low", model="haiku", ...)
```

## Agent-Tier Quick Reference

| Agent | Tier | Model | Parallel |
|-------|------|-------|----------|
| #01 Research Question | HIGH | opus | No |
| #02 Theoretical Framework | HIGH | opus | Yes (#03) |
| #03 Devil's Advocate | HIGH | opus | Yes (#02) |
| #04 Ethics Advisor | MEDIUM | sonnet | Yes (#09) |
| #05 Literature Scout | LOW | haiku | Yes (multi) |
| #06 Quality Appraiser | MEDIUM | sonnet | Yes (multi) |
| #07 Effect Size Extractor | LOW | haiku | Yes (multi) |
| #08 Research Radar | LOW | haiku | Yes |
| #09 Design Consultant | HIGH | opus | Yes (#04) |
| #10 Statistical Guide | MEDIUM | sonnet | No |
| #11 Code Generator | LOW | haiku | Yes |
| #12 Sensitivity Designer | MEDIUM | sonnet | Yes (#11) |
| #13 Consistency Checker | LOW | haiku | Yes |
| #14 Checklist Manager | LOW | haiku | Yes |
| #15 Reproducibility Auditor | MEDIUM | sonnet | Yes |
| #16 Bias Detector | MEDIUM | sonnet | No |
| #17 Journal Matcher | MEDIUM | sonnet | No |
| #18 Academic Communicator | MEDIUM | sonnet | Yes (multi) |
| #19 Peer Review Strategist | HIGH | opus | No |
| #20 Preregistration Composer | MEDIUM | sonnet | No |
| #21 Visualization | MEDIUM | sonnet | No |

## Example Orchestration

### User: "AI 튜터 효과 연구 시작하고 싶어"

```
1. Pattern Match: "연구" → Research Question
2. Route: #01 (HIGH/opus)
3. Execute #01
4. 🔴 CP_RESEARCH_DIRECTION - STOP & ASK USER
5. User Approves Direction B
6. Route: #02 + #03 (HIGH/opus) PARALLEL
7. Execute in parallel
8. 🔴 CP_THEORY_SELECTION - STOP & ASK USER
9. User Selects Framework
10. Route: #09 + #04 (HIGH/opus, MEDIUM/sonnet) PARALLEL
11. Execute in parallel
12. 🔴 CP_METHODOLOGY_APPROVAL - STOP & ASK USER
13. User Approves Design
14. Continue to Literature Phase...
```

## Configuration Files

- Routing: `.omc/config/research-coordinator-routing.yaml`
- Checkpoints: `.omc/checkpoints/checkpoint-definitions.yaml`
- Parallel Rules: `.omc/checkpoints/parallel-execution-rules.yaml`

## Integration with OMC Modes

### ultrawork
- Maximizes parallel execution
- Uses all available parallel groups

### ecomode
- Prefers LOW tier when possible
- Batches similar tasks

### ralph
- Persists until all checkpoints approved
- Architect verification at end
