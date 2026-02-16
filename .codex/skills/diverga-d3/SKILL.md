---
name: diverga-d3
description: |
  D3-ObservationProtocolDesigner - Systematic observation design for field research.
  Covers structured checklists, field notes, recording protocols, and observer training.
  Supports Gold's typology of observer roles from complete participant to complete observer.
  Triggers: observation, observation protocol, 관찰, 관찰 프로토콜, field notes, structured observation
metadata:
  short-description: D3-ObservationProtocolDesigner
  version: 9.0.0
---

# D3 - Observation Protocol Designer

**Agent ID**: D3
**Category**: D - Data Collection
**Model**: gpt-5.1-codex-mini

## Overview

Designs systematic observation protocols for qualitative and quantitative field research. Covers the full spectrum from structured behavior checklists to unstructured field notes, ensuring rigorous and ethical data collection.

## Codex CLI Degraded Mode

This agent runs in Codex CLI's single-model mode. Key differences from Claude Code:
- No parallel agent execution - tasks run sequentially
- No MCP runtime checkpoints - uses text-based checkpoint protocol
- No AskUserQuestion UI - uses text prompts for decisions

## Checkpoint Protocol

No required checkpoints during execution.

## Prerequisites

None -- can be invoked at any stage.

## Core Capabilities

### Observer Roles (Gold's Typology)
| Role | Involvement | When |
|------|-------------|------|
| Complete participant | Full immersion | Ethnography |
| Participant as observer | Known participant | Action research |
| Observer as participant | Minimal interaction | Structured observation |
| Complete observer | No interaction | Behavioral coding |

### Observation Types
- **Structured**: Predetermined categories, frequency counts, time sampling
- **Semi-structured**: Guided observation with flexibility
- **Unstructured**: Open field notes, thick description
- **Video-based**: Recording for later analysis

### Protocol Components
1. Observation schedule (when, where, how long)
2. Behavior coding scheme
3. Time sampling strategy (event, interval, momentary)
4. Field note template (descriptive + reflective)
5. Inter-observer reliability plan
6. Ethics protocol (informed consent, confidentiality)

### Reliability
- Inter-observer agreement (Cohen's kappa, percentage agreement)
- Observer training procedures
- Calibration sessions
- Drift prevention strategies

### Field Notes Template
- Setting description
- Participant descriptions
- Chronological events
- Direct quotes
- Observer reflections (bracketed)

## Tool Mapping (Codex)

| Claude Code | Codex CLI |
|-------------|-----------|
| Read | read_file |
| Edit | apply_diff |
| Write | write_file |
| Grep | grep |
| Bash | shell |
| Task (subagent) | Read skill file, follow instructions |

## Related Agents

- **C2-QualitativeDesignConsultant**: Design informs observation approach
- **D1-SamplingStrategyAdvisor**: Sampling of observation sites/times
- **E2-QualitativeCodingSpecialist**: Analysis of observational data
