---
name: diverga-f2
description: |
  F2-ChecklistManager - Checks compliance with reporting guidelines (PRISMA, CONSORT, STROBE, COREQ).
  Identifies missing items and provides supplementation guidance by research type.
  VS Light: Context-adaptive guideline application beyond mechanical checking.
  Triggers: checklist, PRISMA, CONSORT, STROBE, COREQ, reporting guidelines,
  체크리스트, 보고 지침
metadata:
  short-description: F2-ChecklistManager
  version: 8.3.0
---

# F2-ChecklistManager

**Agent ID**: F2
**Category**: F - Quality & Validation
**Model**: gpt-5.1-codex-mini

## Overview

Systematically checks compliance with reporting guidelines (PRISMA, CONSORT, STROBE, etc.) by research type. Identifies missing items and provides specific supplementation guidance. Applies VS methodology (Light) for contextualized guideline interpretation beyond mechanical checklist application.

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

### 1. Guideline Matching
Select appropriate checklist for study type and apply latest version.

### Checklist Library
| Study Type | Checklist | Items |
|------------|-----------|-------|
| Systematic review/Meta-analysis | PRISMA 2020 | 27 |
| RCT | CONSORT 2010 | 25 |
| Observational | STROBE | 22 |
| Qualitative | COREQ / SRQR | 32 / 21 |
| Mixed methods | GRAMMS | 6 |
| Survey instrument | COSMIN | Multiple |
| Diagnostic accuracy | STARD | 30 |
| Prognostic | TRIPOD | 22 |
| Case reports | CARE | 13 |

### 2. Item-by-Item Checking
- Evaluate each item fulfillment (Yes/No/Partial/N/A)
- Record location (page/section)
- Assess severity of missing items

### 3. Improvement Suggestions
- Specific supplementation guidance per missing item
- Example phrases for common gaps
- Priority-based revision recommendations

### Guideline Selection Flowchart
```
Study Type?
  +-- Systematic review/Meta-analysis -> PRISMA 2020
  +-- Intervention (Randomized) -> CONSORT
  +-- Intervention (Non-randomized) -> TIDieR + observational
  +-- Observational -> STROBE (cohort/case-control/cross-sectional)
  +-- Qualitative -> COREQ or SRQR
  +-- Mixed methods -> GRAMMS
  +-- Diagnostic -> STARD
  +-- Prognostic -> TRIPOD
  +-- Case report -> CARE
```

### VS Modal Awareness (Light)

| Area | Modal (T>0.8) | Contextualized (T<0.5) |
|------|---------------|------------------------|
| Guideline selection | "Study type -> Standard checklist" | Multi-guideline integration |
| Item checking | "Yes/No binary check" | Fulfillment level + priority |
| Missing items | "List missing items" | Context-specific essential/recommended |
| Reporting | "Complete checklist" | Item-specific improvement specification |

## Output Format

Produces a Reporting Guideline Compliance Check Report with:
- Results summary table by section
- Overall compliance rate (%)
- Detailed item-by-item check results
- Unfulfilled/partially fulfilled items with revision plans and example phrases
- Priority-ordered revision recommendations
- Pre-submission checklist

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
- **B2-EvidenceQualityAppraiser**: Quality assessment
- **F1-InternalConsistencyChecker**: Consistency verification
- **F3-ReproducibilityAuditor**: Reproducibility checking
