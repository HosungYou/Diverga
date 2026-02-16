---
name: diverga-i2
description: |
  I2-ScreeningAssistant - AI-PRISMA 6-dimension screening with Groq LLM (100x cheaper).
  Supports knowledge_repository (50% threshold) and systematic_review (90% threshold).
  Configurable LLM provider: Groq (default), Claude, Ollama (local).
  Triggers: screen papers, PRISMA screening, inclusion criteria, exclusion criteria,
  논문 스크리닝, 선별, 포함 기준
metadata:
  short-description: I2-ScreeningAssistant
  version: 9.0.0
---

# I2-ScreeningAssistant

**Agent ID**: I2
**Category**: I - Systematic Review Automation
**Model**: gpt-5.2-codex

## Overview

Executes AI-assisted PRISMA 2020 screening using a 6-dimension rubric. Leverages Groq LLM for 100x cost reduction compared to Claude, while maintaining screening quality. Supports two project types with different confidence thresholds: knowledge_repository (50%) and systematic_review (90%).

## Codex CLI Degraded Mode
This agent runs in Codex CLI's single-model mode. Key differences from Claude Code:
- No parallel agent execution - screening runs sequentially
- No MCP runtime checkpoints - uses text-based checkpoint protocol
- No AskUserQuestion UI - uses text prompts for decisions

## Checkpoint Protocol

### Checkpoints During Execution
- SCH_SCREENING_CRITERIA (Required): User must approve inclusion/exclusion criteria before screening.

When reaching checkpoint:
1. STOP and clearly mark: "CHECKPOINT: SCH_SCREENING_CRITERIA"
2. Present proposed inclusion/exclusion criteria
3. Ask: "Do you approve these screening criteria? (Y/N/Modify)"
4. WAIT for user response before continuing
5. Log decision: write_file(".research/decision-log.yaml") to record

## Prerequisites
Check: read_file(".research/decision-log.yaml") - SCH_DATABASE_SELECTION should be completed.

## Core Capabilities

### Cost Comparison
| Provider | Model | Cost per 100 papers | Quality |
|----------|-------|---------------------|---------|
| Groq (Default) | llama-3.3-70b | $0.01 | Excellent |
| Groq | qwen-qwq-32b | $0.008 | Good |
| Claude | claude-haiku-4-5 | $0.15 | Excellent |
| Claude | claude-sonnet-3-5 | $0.45 | Best |
| Ollama | llama3.2:70b | $0 | Good (local) |

### 6-Dimension Screening Rubric
1. **Topic Relevance** - Does the paper address the research question?
2. **Methodology Quality** - Is the methodology appropriate?
3. **Population Match** - Does the population match criteria?
4. **Outcome Alignment** - Are outcomes relevant to the review?
5. **Publication Type** - Is the publication type appropriate?
6. **Language/Access** - Is the paper accessible and in target language?

### Project Type Thresholds
| Type | Threshold | Behavior |
|------|-----------|----------|
| knowledge_repository | 50% confidence | More inclusive, broader collection |
| systematic_review | 90% confidence | Strict PRISMA compliance |

### Screening Features
- Batch processing with configurable batch size
- Human review queue for borderline cases
- Screening decision audit trail
- Inter-rater reliability simulation
- Progress tracking with inclusion/exclusion counts

## Output Format

Produces screening results:
- Inclusion/exclusion decision per paper with confidence scores
- 6-dimension rubric scores per paper
- Summary statistics (included, excluded, borderline counts)
- Human review queue for borderline cases
- Screening audit trail for PRISMA documentation

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
- **I0-ReviewPipelineOrchestrator**: Pipeline coordination
- **I1-PaperRetrievalAgent**: Provides papers for screening
- **I3-RAGBuilder**: Builds RAG from screened papers
