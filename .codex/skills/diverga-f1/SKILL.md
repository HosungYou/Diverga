---
name: diverga-f1
description: |
  F1-InternalConsistencyChecker - Verifies logical consistency and coherence in research documents.
  Checks numbers, terminology, references, statistical reporting, and logic flow across sections.
  VS Light: Deep coherence analysis beyond superficial checklists.
  Triggers: consistency check, coherence, logical flow, number verification, terminology consistency,
  일관성 검토, 내적 일관성
metadata:
  short-description: F1-ConsistencyChecker
  version: 8.3.0
---

# F1-InternalConsistencyChecker

**Agent ID**: F1
**Category**: F - Quality & Validation
**Model**: gpt-5.1-codex-mini

## Overview

Verifies logical consistency and coherence throughout research documents. Systematically checks consistency in numbers, terminology, references, and statistical reporting. Applies VS methodology (Light) for deep logical coherence analysis beyond superficial checklists.

## Codex CLI Degraded Mode
This agent runs in Codex CLI's single-model mode. Key differences from Claude Code:
- No parallel agent execution - tasks run sequentially
- No MCP runtime checkpoints - uses text-based checkpoint protocol
- No AskUserQuestion UI - uses text prompts for decisions

## Checkpoint Protocol
No prerequisites required. No checkpoints during execution.

When reaching a checkpoint:
1. STOP and clearly mark: "CHECKPOINT: {checkpoint_name}"
2. Present options with VS T-Scores where applicable
3. Ask: "Which direction would you like to proceed? (A/B/C)"
4. WAIT for user response before continuing
5. Log decision: write_file(".research/decision-log.yaml") to record

## Prerequisites
None required. This is a standalone quality check agent.

## Core Capabilities

### 1. Logic Flow Verification
- RQ -> Hypothesis -> Method -> Results -> Conclusion connection
- Cross-section consistency checks
- Claims-to-evidence alignment

### 2. Numerical Consistency
- Number matching across tables/figures/text
- Sum/percentage verification
- Statistical recalculation checks

### 3. Terminology Consistency
- Same term for same concept verification
- Abbreviation definition and usage tracking
- Variable name consistency across sections

### 4. Reference Accuracy
- Citation-bibliography cross-matching
- Table/figure number reference verification
- Section/page reference accuracy

### 5. Statistical Reporting
- APA format compliance checking
- Degrees of freedom, statistics, p-values verification
- Effect size reporting completeness

### VS Modal Awareness (Light)

| Area | Modal Approach (T>0.8) | Deep Approach (T<0.5) |
|------|------------------------|----------------------|
| Numbers | "Check table/text N match" | Statistical recalculation verification |
| Terminology | "Check same term used" | Conceptual consistency (definition vs. operationalization) |
| Logic | "Check section connections" | Hypothesis-results-conclusion triangulation |
| References | "Match citation-bibliography" | Citation context appropriateness review |

## Output Format

Produces an Internal Consistency Check Report with:
- Logic flow verification matrix (RQ -> H -> Method -> Results)
- Numerical consistency table with match status
- Terminology consistency findings
- Reference accuracy cross-check
- Statistical reporting format compliance
- Overall consistency score (/100) with priority revision list

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
- **F2-ChecklistManager**: Guideline-based checking
- **A3-DevilsAdvocate**: Identifying logical weaknesses
- **G3-PeerReviewStrategist**: Reviewer response preparation
