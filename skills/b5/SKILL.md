---
name: b5
description: |
  Parallel Document Processor - High-throughput PDF/document reading with distributed workload
  Handles large PDF collections by splitting work across multiple parallel workers
  Prevents memory/context overflow errors from processing large documents sequentially
  Use when: processing multiple PDFs, large document collections, systematic review data extraction
  Triggers: batch PDF, parallel reading, multiple documents, large files, document extraction
version: "6.9.0"
---

# B5-Parallel Document Processor

**Agent ID**: B5 (new in v6.2)
**Category**: B - Literature & Evidence
**VS Level**: Enhanced
**Tier**: HIGH (Opus for coordination)
**Icon**: 📄⚡

## Overview

The Parallel Document Processor is designed to handle **large PDF collections** that would overwhelm single-threaded processing. Based on the `oh-my-claudecode:executor` parallel execution pattern, this agent coordinates multiple workers to:

1. **Chunk PDF collections** into manageable batches
2. **Distribute workload** across parallel workers
3. **Aggregate results** into unified output
4. **Handle failures gracefully** with retry logic

### Problem Solved

When processing many PDFs sequentially:
- Context window fills up quickly
- Memory errors occur with large files
- Total processing time becomes prohibitive
- A single error can halt the entire pipeline

### Solution

```
┌─────────────────────────────────────────────────────────────────┐
│                   B5-ParallelDocumentProcessor                   │
│                                                                  │
│   PDF Collection (N files)                                       │
│         │                                                        │
│         ▼                                                        │
│   ┌─────────────────┐                                            │
│   │  Coordinator    │  (Opus - orchestration)                    │
│   │  - Partition    │                                            │
│   │  - Distribute   │                                            │
│   │  - Aggregate    │                                            │
│   └────────┬────────┘                                            │
│            │                                                     │
│    ┌───────┼───────┬───────┬───────┐                             │
│    ▼       ▼       ▼       ▼       ▼                             │
│  Worker  Worker  Worker  Worker  Worker  (Haiku - extraction)    │
│   1-10   11-20   21-30   31-40   41-50                           │
│    │       │       │       │       │                             │
│    └───────┴───────┴───────┴───────┘                             │
│                    │                                             │
│                    ▼                                             │
│            Aggregated Results                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Capabilities

- **Batch PDF Processing**: Process 50-500 PDFs in parallel batches
- **Intelligent Chunking**: Automatically determine optimal batch sizes based on file sizes
- **Context-Safe Extraction**: Each worker stays within context limits
- **Fault Tolerance**: Failed files are retried in isolation
- **Progress Tracking**: Real-time status updates during processing
- **Result Aggregation**: Combine extracted data into unified format

## Input Schema

```yaml
Required:
  - pdf_directory: "Path to directory containing PDFs"
  - extraction_task: "enum[full_text, abstract, metadata, tables, citations, specific_sections]"

Optional:
  - max_workers: "int (default: 5, max: 10)"
  - batch_size: "int (default: 10 PDFs per worker)"
  - output_format: "enum[json, yaml, csv, markdown]"
  - specific_fields: "list[string] - for targeted extraction"
  - retry_failed: "bool (default: true)"
  - file_filter: "glob pattern (e.g., '*.pdf', '2024*.pdf')"
```

## Output Schema

```yaml
main_output:
  summary:
    total_files: int
    successful: int
    failed: int
    processing_time: string

  results:
    - file: string
      status: "success | failed | skipped"
      extracted_data: object
      error_message: string | null

  aggregated_data:
    combined_text: string | null
    metadata_table: object | null
    citation_list: list | null
```

## Execution Flow

### Phase 1: Discovery & Planning

```markdown
1. Scan PDF directory
2. Calculate total file sizes
3. Determine optimal batch distribution
4. Create worker assignment plan
```

### Phase 2: Parallel Extraction

```markdown
For each worker batch (in parallel):
  1. Read assigned PDFs
  2. Extract requested data
  3. Return structured results
  4. Report progress
```

### Phase 3: Aggregation & Validation

```markdown
1. Collect all worker results
2. Identify failed extractions
3. Retry failed files (max 2 attempts)
4. Combine successful extractions
5. Generate summary report
```

## Worker Types

| Worker Type | Model | Use Case | Max Files/Batch |
|-------------|-------|----------|-----------------|
| **Light** | Haiku | Metadata, abstracts | 20 |
| **Standard** | Sonnet | Full text, tables | 10 |
| **Heavy** | Opus | Complex extraction, analysis | 5 |

## Usage Examples

### Example 1: Systematic Review PDF Extraction

```
User: "Process all 127 PDFs in my systematic review folder"

B5 Response:
"Processing 127 PDFs across 5 parallel workers (26 PDFs each).
Estimated time: 8-12 minutes.

Worker Status:
[1] ████████░░ 80% (21/26)
[2] ██████░░░░ 60% (16/26)
[3] ██████████ 100% (26/26) ✓
[4] ████░░░░░░ 40% (11/26)
[5] ████████░░ 80% (21/26)

Progress: 95/127 (75%)"
```

### Example 2: Targeted Data Extraction

```
User: "Extract sample sizes and effect sizes from these meta-analysis PDFs"

B5 Configuration:
  extraction_task: specific_sections
  specific_fields: ["sample_size", "effect_size", "confidence_interval"]
  output_format: csv
```

### Example 3: Large File Handling

```
User: "This 500-page PDF keeps crashing. Can you process it?"

B5 Strategy:
1. Split into 50-page chunks
2. Process chunks in parallel
3. Reconstruct in order
4. Validate continuity
```

## Error Handling

| Error Type | Strategy |
|------------|----------|
| **Memory overflow** | Reduce batch size, retry with Light worker |
| **Corrupted PDF** | Skip and log, continue with others |
| **Timeout** | Retry with extended timeout |
| **Parse failure** | Try alternative extraction method (OCR fallback) |

## Integration with Other Agents

### Upstream (provides input)

- **B1-SystematicLiteratureScout**: Provides PDF download list
- **Manual Upload**: User provides PDF directory

### Downstream (uses output)

- **B2-EvidenceQualityAppraiser**: Quality assessment of extracted content
- **B3-EffectSizeExtractor**: Statistical data extraction from aggregated text
- **E1-QuantitativeAnalysisGuide**: Analysis of extracted data tables

### Parallel Compatible

- **B4-ResearchRadar**: Monitor for new PDFs to process

## Performance Guidelines

| Collection Size | Recommended Workers | Expected Time |
|-----------------|---------------------|---------------|
| 1-10 PDFs | 2 | 1-2 min |
| 11-50 PDFs | 3 | 3-5 min |
| 51-100 PDFs | 5 | 8-12 min |
| 101-200 PDFs | 7 | 15-25 min |
| 200+ PDFs | 10 | 30+ min |

## Triggers

| Trigger Keywords | Context |
|------------------|---------|
| "batch PDF", "multiple PDFs" | Document collection processing |
| "parallel reading", "병렬 처리" | Performance optimization |
| "large document", "큰 파일" | Memory/context issues |
| "extract from all", "모든 PDF에서" | Bulk extraction |
| "systematic review PDFs" | Literature review workflow |

## Configuration Options

### Default Configuration

```yaml
parallel_processing:
  default_workers: 5
  max_workers: 10
  batch_size_per_worker: 10
  timeout_per_file_seconds: 60
  retry_attempts: 2

extraction:
  default_format: json
  include_metadata: true
  include_page_numbers: true
  preserve_formatting: false

error_handling:
  skip_on_failure: true
  log_errors: true
  retry_failed: true
```

### Memory-Safe Configuration (for limited environments)

```yaml
parallel_processing:
  default_workers: 3
  batch_size_per_worker: 5
  timeout_per_file_seconds: 120
```

## Checkpoint Integration

| Checkpoint | When | Purpose |
|------------|------|---------|
| CP-INIT-001 | Before processing | Confirm file count and extraction type |
| CP-PROGRESS-001 | At 50% completion | Allow user to adjust or cancel |
| CP-COMPLETE-001 | After processing | Review summary, handle failures |

## Self-Monitoring

The coordinator tracks:

```yaml
metrics:
  - files_processed: int
  - files_remaining: int
  - current_throughput: "files/minute"
  - estimated_completion: "timestamp"
  - memory_usage: "percentage"
  - error_rate: "percentage"
```

## Limitations

1. **Maximum concurrent workers**: 10 (to prevent rate limiting)
2. **File size limit per worker**: 50MB (larger files auto-chunked)
3. **Total collection limit**: 500 PDFs (batch processing for larger)
4. **OCR not included**: Plain PDF extraction only (use external OCR first)

## Future Enhancements (Roadmap)

- [ ] Integrated OCR for scanned PDFs
- [ ] Table extraction with structure preservation
- [ ] Citation network extraction
- [ ] Image/figure extraction
- [ ] Real-time streaming results

---

## References

### Internal
- oh-my-claudecode:executor - Parallel execution pattern
- B1-SystematicLiteratureScout - Upstream PDF provider
- B3-EffectSizeExtractor - Downstream consumer

### External
- PyMuPDF (fitz) - PDF parsing library
- pdfplumber - Table extraction
- Unstructured - Document parsing
