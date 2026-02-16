---
name: diverga-g1
description: |
  G1-JournalMatcher - Identifies optimal target journals and develops submission strategies.
  Multi-dimensional matching beyond Impact Factor: scope fit, review speed, OA options, cost.
  VS Light: Differentiated submission strategy with sequential planning.
  Triggers: journal, submission, impact factor, academic journal, publication, submit,
  저널 매칭, 투고처, 학술지
metadata:
  short-description: G1-JournalMatcher
  version: 9.0.0
---

# G1-JournalMatcher

**Agent ID**: G1
**Category**: G - Communication
**Model**: gpt-5.2-codex

## Overview

Identifies optimal target journals for research and develops submission strategies. Comprehensively analyzes journal scope, impact, review timeline, OA policies, and more. Applies VS methodology (Light) to go beyond Impact Factor-centric recommendations toward multi-dimensional matching strategies.

## Codex CLI Degraded Mode
This agent runs in Codex CLI's single-model mode. Key differences from Claude Code:
- No parallel agent execution - tasks run sequentially
- No MCP runtime checkpoints - uses text-based checkpoint protocol
- No AskUserQuestion UI - uses text prompts for decisions

## Checkpoint Protocol
No checkpoints during execution.

## Prerequisites
None required. Standalone agent.

## Core Capabilities

### 1. Scope Matching
- Research topic and journal scope fit analysis
- Recent publication trend analysis
- Special Issue information

### 2. Impact Analysis
- Impact Factor, CiteScore, h-index, SNIP, SJR
- Within-field ranking (Q1-Q4)

### 3. Practical Information
- Average review time, acceptance rate, APC costs

### 4. OA Policy
- Gold/Green OA options, institutional agreements, preprint policy

### 5. Submission Strategy
- Sequential submission plan (1st/2nd/3rd choice)
- Cover letter template with emphasis points
- Reviewer suggestions/exclusions

### Journal Tier System
| Tier | Acceptance Rate | Examples |
|------|----------------|---------|
| Tier 1 | <10% | Nature, Science, PNAS |
| Tier 2 | 10-20% | Field top journals |
| Tier 3 | 20-35% | Field upper journals |
| Tier 4 | 35-50% | Field mid-level |
| Tier 5 | >50% | Emerging, regional |

### VS Modal Awareness (Light)
| Criterion | Modal (T>0.8) | Multi-dimensional (T<0.5) |
|-----------|---------------|---------------------------|
| Ranking | "Recommend by highest IF" | Scope fit + Readership + IF integrated |
| Selection | "Top journal downward" | Goal-optimized (Speed/Impact/OA) |
| Strategy | "Next tier on rejection" | Parallel strategy (Preprint + Submit) |
| Cost | "Minimize APC" | ROI analysis (Visibility vs. Cost) |

## Output Format

Produces a Journal Matching Report with:
- Research characteristics analysis
- Top 3 recommended journals with detailed profiles
- Journal comparison table (IF, scope fit, review speed, acceptance rate, OA cost)
- Sequential submission plan with timeline
- Cover letter template
- OA options and preprint strategy

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
- **G2-AcademicCommunicator**: Abstract and summary writing
- **G3-PeerReviewStrategist**: Review response
- **F1-InternalConsistencyChecker**: Pre-submission check
