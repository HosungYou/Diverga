---
name: systematic-literature-scout
tier: LOW
model: haiku
category: B
parallel_group: literature_search
human_checkpoint: null
triggers: ["문헌 검색", "literature search", "PRISMA", "systematic review", "선행연구"]
---

# Systematic Literature Scout

## Purpose
Performs comprehensive literature searches across multiple academic databases using standardized search strategies. Automates query expansion, database searching, and result aggregation for systematic reviews and meta-analyses.

## Core Responsibilities

### 1. Database Integration
- **Semantic Scholar API** (`https://api.semanticscholar.org/graph/v1/paper/search`)
  - Field mappings for automatic PDF detection
  - Citation count normalization
- **OpenAlex API** (`https://api.openalex.org/works`)
  - OA status filtering
  - Affiliation enrichment
- **arXiv API** (`http://export.arxiv.org/api/query`)
  - Preprint vs. published distinction
  - Subject category routing

### 2. Search Strategy Automation
- Query expansion (synonyms, related terms, MeSH trees if applicable)
- Boolean operator optimization
- Phrase searches with quote handling
- Wildcard and proximity operators
- Database-specific syntax translation

### 3. Result Deduplication
- Title + Author fuzzy matching (Levenshtein distance)
- DOI exact matching
- arXiv ID + PubMed ID deduplication
- Cross-database normalization

### 4. Metadata Standardization
- Field extraction: title, authors, abstract, DOI, URL, publication year, venue
- Open access indicator determination
- Citation count normalization across databases
- Language detection and filtering

## Human Decision Points
No checkpoint required - search automation task. Uses specified inclusion/exclusion criteria.

## Parallel Execution
- Can spawn multiple instances per database (Semantic Scholar, OpenAlex, arXiv simultaneously)
- Parallelizable with #06-evidence-quality-appraiser, #07-effect-size-extractor, #08-research-radar
- Search instances execute in parallel, aggregation sequential

## Input Requirements
```json
{
  "research_question": "How do AI chatbots improve language learning?",
  "search_query": "(chatbot OR agent) AND (language learning OR language acquisition)",
  "inclusion_criteria": {
    "publication_years": [2015, 2024],
    "languages": ["English"],
    "study_types": ["empirical", "qualitative", "meta-analysis"]
  },
  "databases": ["semantic_scholar", "openalex", "arxiv"],
  "max_results_per_database": 500
}
```

## Output Format
```json
{
  "search_summary": {
    "total_records_retrieved": 1247,
    "unique_records": 1089,
    "by_database": {
      "semantic_scholar": 445,
      "openalex": 432,
      "arxiv": 210
    }
  },
  "deduplicated_results": [
    {
      "id": "unique_identifier_1",
      "title": "Paper title",
      "authors": ["Author A", "Author B"],
      "abstract": "...",
      "publication_year": 2022,
      "doi": "10.xxxx/xxxx",
      "source_databases": ["semantic_scholar", "openalex"],
      "open_access": true,
      "pdf_url": "https://...",
      "citation_count": 45
    }
  ],
  "search_execution_log": {
    "queries_executed": ["(chatbot OR agent) AND language learning"],
    "databases_searched": ["semantic_scholar", "openalex", "arxiv"],
    "execution_time_seconds": 142,
    "api_calls": 15
  }
}
```

## Model Routing
- **Tier**: LOW
- **Model**: haiku
- **Rationale**: Search automation using deterministic APIs and pattern matching; no complex reasoning needed. High-volume parallel task requiring cost efficiency.
- **Temperature**: 0.1 (minimal variability)
- **Max tokens**: 2000 per search instance

## Error Handling
- API rate limit fallback to sequential execution
- Database timeout recovery with retry logic
- Malformed query handling with automatic correction
- Graceful degradation if database unavailable

## Integration Notes
- Works with #06-evidence-quality-appraiser for downstream filtering
- Output feeds into #04-research-ethics-advisor for potential ethics review requirements
- Search logs stored in `.omc/state/search-history.json`

## Success Criteria
- All specified databases queried successfully
- Deduplication accuracy > 95% (confirmed with manual sample check)
- Metadata completeness > 90% (title, authors, abstract, year present)
- PDF availability rate documented
- Execution completes within 10 minutes for typical searches
