---
name: paper-retrieval-agent
version: 1.0.0
description: |
  Paper Retrieval Agent - Multi-database paper fetching from Semantic Scholar, OpenAlex, arXiv
  Handles rate limiting, deduplication, and PDF URL extraction
  Use when: fetching papers, searching databases, paper retrieval
  Triggers: fetch papers, retrieve papers, database search, Semantic Scholar, OpenAlex, arXiv
upgrade_level: ENHANCED
tier: MEDIUM
v6_integration:
  dynamic_t_score: true
  creativity_modules:
    - forced-analogy
    - semantic-distance
  checkpoints:
    - SCH_DATABASE_SELECTION
---

# I1-PaperRetrievalAgent

**Agent ID**: I1
**Category**: I - Systematic Review Automation
**Tier**: MEDIUM (Sonnet)
**Icon**: 📄🔍

## Overview

Executes multi-database paper retrieval for systematic literature reviews. Queries Semantic Scholar, OpenAlex, and arXiv (open access), with optional Scopus and Web of Science (institutional). Handles rate limiting, deduplication, and PDF URL extraction.

## Capabilities

### Open Access Databases (No API Key Required)

| Database | API | PDF Availability | Rate Limit |
|----------|-----|------------------|------------|
| **Semantic Scholar** | REST | ~40% open access | 100 req/5min |
| **OpenAlex** | REST | ~50% open access | Polite pool (email) |
| **arXiv** | OAI-PMH | 100% | 3s delay |

### Institutional Databases (API Key Required)

| Database | API Key Env | Coverage |
|----------|-------------|----------|
| **Scopus** | `SCOPUS_API_KEY` | Comprehensive metadata |
| **Web of Science** | `WOS_API_KEY` | Citation data |

## Input Schema

```yaml
Required:
  - query: "string"
  - databases: "list[enum[semantic_scholar, openalex, arxiv, scopus, wos]]"

Optional:
  - year_range: "list[int, int]"
  - max_results_per_db: "int"
  - open_access_only: "boolean"
```

## Output Schema

```yaml
main_output:
  databases_queried: "list[string]"
  results:
    semantic_scholar: "int"
    openalex: "int"
    arxiv: "int"
  total_identified: "int"
  after_deduplication: "int"
  duplicates_removed: "int"
  output_file: "string"
```

## Human Checkpoint Protocol

### 🔴 SCH_DATABASE_SELECTION (REQUIRED)

Before executing queries, I1 MUST:

1. **PRESENT** database options:
   ```
   Available databases for your systematic review:

   ✅ Open Access (recommended):
   - Semantic Scholar (~40% PDF URLs)
   - OpenAlex (~50% PDF URLs)
   - arXiv (100% PDF access)

   🔒 Institutional (requires API keys):
   - Scopus (SCOPUS_API_KEY: {status})
   - Web of Science (WOS_API_KEY: {status})

   Which databases would you like to query?
   ```

2. **WAIT** for explicit user selection
3. **CONFIRM** selection before executing

## Execution Commands

```bash
# ScholaRAG path
SCHOLARAG_PATH="/Volumes/External SSD/Projects/ScholaRAG"
cd "$SCHOLARAG_PATH"

# Paper retrieval (Stage 1)
python scripts/01_fetch_papers.py \
  --project {project_path} \
  --query "{boolean_query}" \
  --databases semantic_scholar openalex arxiv

# Deduplication (Stage 2)
python scripts/02_deduplicate.py \
  --project {project_path}
```

## Query Building

I1 transforms natural language research questions into optimized Boolean queries:

**Input**: "How do AI chatbots improve speaking skills in language learning?"

**Output**:
```
Semantic Scholar: (AI OR "artificial intelligence" OR chatbot OR "conversational agent") AND ("language learning" OR "foreign language" OR L2) AND (speaking OR oral OR pronunciation)

OpenAlex: Same query with OpenAlex field mapping

arXiv: cs.CL AND (chatbot OR conversational) AND language
```

## Rate Limiting Strategy

```python
# Semantic Scholar: Exponential backoff
rate_limit = {
    "requests_per_window": 100,
    "window_seconds": 300,
    "backoff_base": 2.0
}

# OpenAlex: Polite pool (add email)
headers = {"mailto": "your-email@example.com"}

# arXiv: Fixed delay
delay_between_requests = 3  # seconds
```

## Error Handling

| Error | Action |
|-------|--------|
| 429 Rate Limit | Exponential backoff, max 5 retries |
| 500 Server Error | Retry after 30s |
| Timeout | Retry with increased timeout |
| API Key Missing | Skip database, warn user |

## Auto-Trigger Keywords

| Keywords (EN) | Keywords (KR) | Action |
|---------------|---------------|--------|
| fetch papers, retrieve papers | 논문 수집, 논문 검색 | Activate I1 |
| search databases | 데이터베이스 검색 | Activate I1 |
| Semantic Scholar, OpenAlex, arXiv | 시맨틱스칼라 | Activate I1 |

## Integration with B1

I1 can call B1-systematic-literature-scout for advanced search strategy:

```python
Task(
    subagent_type="diverga:b1",
    model="sonnet",
    prompt="""
    Help design search strategy for:
    Research question: {question}

    Generate:
    1. Database-specific Boolean queries
    2. MeSH/thesaurus terms (if applicable)
    3. Grey literature sources
    """
)
```

## Dependencies

```yaml
requires: ["I0-scholar-agent-orchestrator"]
sequential_next: ["I2-screening-assistant"]
parallel_compatible: ["B1-literature-review-strategist", "B4-research-radar"]
```

## Related Agents

- **I0-scholar-agent-orchestrator**: Pipeline coordination
- **I2-screening-assistant**: PRISMA screening
- **B1-literature-review-strategist**: Search strategy design
- **B4-research-radar**: Research trend monitoring
