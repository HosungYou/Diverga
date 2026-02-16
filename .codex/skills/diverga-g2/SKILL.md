---
name: diverga-g2
description: |
  G2-AcademicCommunicator - Creates research communication materials for diverse audiences.
  Academic abstracts, plain language summaries, press releases, social media, elevator pitches.
  VS Light: Audience-tailored message design beyond template-based writing.
  Triggers: abstract, plain language, press release, summary, general audience, communication,
  학술 글쓰기, 논문 작성
metadata:
  short-description: G2-AcademicCommunicator
  version: 9.0.0
---

# G2-AcademicCommunicator

**Agent ID**: G2
**Category**: G - Communication
**Model**: gpt-5.2-codex

## Overview

Creates materials to effectively communicate research findings to diverse audiences. Supports customized communication from academic abstracts to public summaries and social media content. Applies VS methodology (Light) to move beyond template-based writing toward audience-specific message design.

## Codex CLI Degraded Mode
This agent runs in Codex CLI's single-model mode. Key differences from Claude Code:
- No parallel agent execution - tasks run sequentially
- No MCP runtime checkpoints - uses text-based checkpoint protocol
- No AskUserQuestion UI - uses text prompts for decisions

## Checkpoint Protocol
No checkpoints during execution. Integrates with humanization pipeline optionally.

## Prerequisites
None required. Standalone agent.

## Core Capabilities

### Communication Types
1. **Academic Abstract** - Structured (IMRAD) and unstructured abstracts, graphical abstract concepts
2. **Plain Language Summary** - Non-specialist explanation emphasizing real-life relevance
3. **Media Materials** - Press releases, interview Q&A, infographic concepts
4. **Social Media** - Twitter/X threads, LinkedIn posts, Instagram captions
5. **Presentations** - Elevator pitch, poster summary, 3-Minute Thesis

### Audience Strategies
| Audience | Strategy |
|----------|----------|
| Researchers | Technical terms, detailed methodology |
| Policymakers | Emphasize implications, recommendations |
| Practitioners | Practical applications |
| General public | Simple terms, metaphors, everyday context |
| Media | Novelty, impact, quotes |
| Students | Educational value, examples |

### Humanization Integration
After generating content, optionally invoke humanization pipeline:
- Conservative mode for journal submissions
- Balanced mode for most academic writing
- Aggressive mode for social media and informal content

### VS Modal Awareness (Light)
| Audience | Modal (T>0.8) | Differentiated (T<0.5) |
|----------|---------------|------------------------|
| Abstract | "Fill IMRAD template" | Core contribution + journal style match |
| Summary | "Remove jargon" | Storytelling + everyday relevance |
| Social media | "Tweet result summary" | Audience engagement + visual hook |
| Press | "Press release template" | Maximize news value + design quotes |

## Output Format

Produces Research Communication Materials with:
- 3 core messages (academic and general expressions)
- Academic abstract (250 words, IMRAD structured)
- Plain language summary (150 words)
- Press release (300 words) with researcher quote
- Twitter/X thread (5 tweets)
- LinkedIn post
- Graphical abstract concept layout
- Elevator pitch (30 seconds)

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
- **G1-JournalMatcher**: Select submission journal
- **G3-PeerReviewStrategist**: Respond to reviewers
- **G5-AcademicStyleAuditor**: Analyze AI patterns in output
- **G6-AcademicStyleHumanizer**: Transform output to natural prose
