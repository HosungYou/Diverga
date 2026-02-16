---
name: diverga-i1
description: |
  I1-PaperRetrievalAgent - Multi-database paper fetching from Semantic Scholar, OpenAlex, arXiv.
  Handles rate limiting, deduplication, and PDF URL extraction for systematic reviews.
  Open access databases require no API keys. Optional Scopus/WoS with institutional access.
  Triggers: fetch papers, retrieve papers, database search, Semantic Scholar, OpenAlex, arXiv,
  논문 수집, 논문 검색, 데이터베이스 검색
metadata:
  short-description: I1-PaperRetrieval
  version: 9.0.0
---

# I1-PaperRetrievalAgent

**Agent ID**: I1
**Category**: I - Systematic Review Automation
**Model**: gpt-5.2-codex

## Overview

Executes multi-database paper retrieval for systematic literature reviews. Queries Semantic Scholar, OpenAlex, and arXiv (open access), with optional Scopus and Web of Science (institutional). Handles rate limiting, deduplication, and PDF URL extraction.

## Codex CLI Degraded Mode
This agent runs in Codex CLI's single-model mode. Key differences from Claude Code:
- No parallel agent execution - database queries run sequentially
- No MCP runtime checkpoints - uses text-based checkpoint protocol
- No AskUserQuestion UI - uses text prompts for decisions

## Checkpoint Protocol

### Checkpoints During Execution
- SCH_DATABASE_SELECTION (Required): User must approve which databases to query.

When reaching checkpoint:
1. STOP and clearly mark: "CHECKPOINT: SCH_DATABASE_SELECTION"
2. Present available databases with coverage info
3. Ask: "Which databases would you like to search? (select all that apply)"
4. WAIT for user response before continuing
5. Log decision: write_file(".research/decision-log.yaml") to record

## Prerequisites
None required. This agent can be called directly or via I0 orchestrator.

## Core Capabilities

### Open Access Databases (No API Key Required)
| Database | API | PDF Availability | Rate Limit |
|----------|-----|------------------|------------|
| Semantic Scholar | REST | ~40% open access | 100 req/5min |
| OpenAlex | REST | ~50% open access | Polite pool (email) |
| arXiv | OAI-PMH | 100% | 3s delay |

### Institutional Databases (API Key Required)
| Database | Env Variable | Coverage |
|----------|-------------|----------|
| Scopus | SCOPUS_API_KEY | Comprehensive metadata |
| Web of Science | WOS_API_KEY | Citation data |

### Retrieval Features
- Boolean query translation per database API syntax
- Rate limit compliance with automatic throttling
- PDF URL extraction from open access fields
- Cross-database deduplication by DOI, arXiv ID, title similarity
- Progress tracking with paper counts per database
- Error handling with retry logic

### Input Schema
```yaml
Required:
  - query: "Boolean search string"
  - databases: "list of database names"
Optional:
  - year_range: [start_year, end_year]
  - max_results_per_db: integer
  - fields: "list of metadata fields to retrieve"
```

## Output Format

Produces retrieval results:
- Per-database paper counts and retrieval status
- Combined paper list with metadata (title, authors, year, DOI, abstract, PDF URL)
- Deduplication summary (duplicates found and removed)
- Database coverage report
- Errors and rate limit events log

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
- **I2-ScreeningAssistant**: Screens retrieved papers
- **B1-SystematicLiteratureScout**: Search strategy design
