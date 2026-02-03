# Workflow: Parallel PDF Processing

## Overview

This workflow orchestrates the B5-ParallelDocumentProcessor agent to process large PDF collections efficiently using parallel workers.

## Trigger Patterns

| Trigger | Example |
|---------|---------|
| Batch PDF processing | "Process all PDFs in my review folder" |
| Large document handling | "This PDF is too large, keeps crashing" |
| Systematic review extraction | "Extract data from 127 papers" |
| Korean triggers | "PDF 병렬 처리해줘", "대용량 문서 처리" |

## Workflow Stages

```
┌─────────────────────────────────────────────────────────────────┐
│                   PARALLEL PDF WORKFLOW                          │
│                                                                  │
│  Stage 1: DISCOVERY                                              │
│  ├─ Scan directory for PDFs                                      │
│  ├─ Calculate total file sizes                                   │
│  ├─ Estimate processing time                                     │
│  └─ [CHECKPOINT] Confirm scope with user                         │
│                                                                  │
│  Stage 2: PLANNING                                               │
│  ├─ Determine optimal worker count                               │
│  ├─ Create batch assignments                                     │
│  ├─ Configure extraction parameters                              │
│  └─ Initialize progress tracking                                 │
│                                                                  │
│  Stage 3: PARALLEL EXECUTION                                     │
│  ├─ Launch worker agents (haiku/sonnet by task)                  │
│  ├─ Monitor progress across workers                              │
│  ├─ Handle failures with retry logic                             │
│  └─ [CHECKPOINT] 50% progress check                              │
│                                                                  │
│  Stage 4: AGGREGATION                                            │
│  ├─ Collect results from all workers                             │
│  ├─ Merge extracted data                                         │
│  ├─ Identify and retry failed files                              │
│  └─ Generate summary report                                      │
│                                                                  │
│  Stage 5: VALIDATION                                             │
│  ├─ Verify output completeness                                   │
│  ├─ Check data consistency                                       │
│  ├─ [CHECKPOINT] Review results with user                        │
│  └─ Export to requested format                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Worker Configuration

### Worker Types and Assignment

| PDF Size | Worker Type | Model | Max Concurrent |
|----------|-------------|-------|----------------|
| < 5MB | Light | Haiku | 20 per batch |
| 5-20MB | Standard | Sonnet | 10 per batch |
| > 20MB | Heavy | Opus | 5 per batch |

### Extraction Task Routing

| Task | Recommended Worker | Notes |
|------|-------------------|-------|
| Metadata only | Light (Haiku) | Fast, low cost |
| Abstract extraction | Light (Haiku) | First page focus |
| Full text | Standard (Sonnet) | Balance of speed/quality |
| Table extraction | Standard (Sonnet) | Structure preservation |
| Citation parsing | Standard (Sonnet) | Reference formatting |
| Complex analysis | Heavy (Opus) | Reasoning required |

## Integration Points

### Upstream Agents

```yaml
B1-SystematicLiteratureScout:
  provides: "PDF download list from search results"
  integration: "Pass file paths to B5 for batch processing"

Manual Upload:
  provides: "User-specified directory"
  integration: "Direct path input to B5"
```

### Downstream Agents

```yaml
B2-EvidenceQualityAppraiser:
  receives: "Extracted content for quality assessment"
  integration: "Pass full text to RoB analysis"

B3-EffectSizeExtractor:
  receives: "Statistical sections from PDFs"
  integration: "Feed extracted tables and results sections"

E1-QuantitativeAnalysisGuide:
  receives: "Aggregated numerical data"
  integration: "CSV/JSON export for analysis"
```

## Example Invocations

### Example 1: Systematic Review Full Extraction

```
User: "Extract full text from all 87 PDFs in my SR folder"

B5 Response:
"Scanning systematic review folder...

📊 Discovery Results:
- Total PDFs: 87
- Total size: 342 MB
- Estimated time: 10-15 minutes

Proposed Configuration:
- Workers: 5 (Standard - Sonnet)
- Batch size: 18 PDFs per worker
- Extraction: Full text + metadata

Proceed with parallel extraction? [Confirm/Adjust]"

User: "Proceed"

B5 Execution:
"Starting parallel extraction...

Worker Progress:
[W1] ████████░░ 80% (14/18) - thesis_johnson_2021.pdf
[W2] ██████░░░░ 60% (11/18) - meta_wang_2023.pdf
[W3] ██████████ 100% ✓ Complete
[W4] ████░░░░░░ 40% (7/18) - review_kim_2022.pdf
[W5] ████████░░ 80% (14/18) - empirical_lee_2024.pdf

Overall: 65/87 (75%) | ETA: 4 min | Errors: 1"
```

### Example 2: Targeted Data Extraction

```
User: "Get sample sizes and effect sizes from these meta-analysis papers"

B5 Configuration:
- Extraction task: specific_sections
- Target fields: ["sample_size", "effect_size", "confidence_interval"]
- Output format: CSV

B5 Response:
"Configuring targeted extraction...

Extraction Template:
| Field | Pattern | Location |
|-------|---------|----------|
| Sample size | N=, n=, participants | Methods, Results |
| Effect size | d=, r=, Cohen's, Hedge's | Results, Tables |
| CI | 95% CI, [x, y] | Results, Tables |

Ready to process 45 PDFs. Proceed?"
```

### Example 3: Large Single File

```
User: "This 500-page dissertation keeps crashing. Help!"

B5 Strategy:
"Large file detected (89 MB, 500 pages).

Strategy: Page-based chunking
1. Split into 10 chunks (50 pages each)
2. Process chunks in parallel
3. Reassemble with continuity check

Estimated time: 8-12 minutes

Proceed with chunked processing?"
```

## Error Handling

### Common Errors and Recovery

| Error | Detection | Recovery |
|-------|-----------|----------|
| Memory overflow | Worker crash | Reduce batch size, retry with Light worker |
| Corrupted PDF | Parse failure | Skip file, log for manual review |
| OCR required | No extractable text | Flag for OCR preprocessing |
| Timeout | 60s+ no response | Retry with extended timeout |
| Rate limit | API 429 | Reduce concurrency, add delays |

### Failure Report Format

```yaml
failed_files:
  - file: "corrupted_scan_2019.pdf"
    error: "PDF parse error: Invalid structure"
    action: "Skipped - needs manual OCR"

  - file: "locked_thesis_2021.pdf"
    error: "Password protected"
    action: "Skipped - requires password"

  - file: "huge_appendix_2020.pdf"
    error: "Timeout after 120s"
    action: "Retry with chunking"
```

## Output Formats

### JSON (Default)

```json
{
  "summary": {
    "total_files": 87,
    "successful": 84,
    "failed": 3,
    "processing_time": "12m 34s"
  },
  "results": [
    {
      "file": "smith_2021.pdf",
      "status": "success",
      "metadata": {
        "title": "AI in Education: A Meta-Analysis",
        "authors": ["Smith, J.", "Lee, K."],
        "year": 2021
      },
      "extracted_text": "...",
      "page_count": 28
    }
  ]
}
```

### CSV (for Analysis)

```csv
file,title,authors,year,sample_size,effect_size,effect_type
smith_2021.pdf,AI in Education,Smith J.; Lee K.,2021,1234,0.45,Cohen's d
wang_2022.pdf,Chatbot Learning,Wang L.,2022,567,0.62,Hedge's g
```

### Markdown (for Reports)

```markdown
# Extraction Summary

## Overview
- **Total Files**: 87
- **Successful**: 84 (97%)
- **Failed**: 3 (3%)

## Extracted Data

### smith_2021.pdf
- **Title**: AI in Education: A Meta-Analysis
- **Sample Size**: N=1,234
- **Effect Size**: d=0.45 [0.32, 0.58]
```

## Checkpoints

| Checkpoint | Level | When | Purpose |
|------------|-------|------|---------|
| CP-INIT-001 | 🔴 Required | Before processing | Confirm file count, extraction type |
| CP-PROGRESS-001 | 🟠 Recommended | At 50% | Allow adjustment or cancellation |
| CP-COMPLETE-001 | 🟡 Optional | After processing | Review results, handle failures |

## Performance Tuning

### Optimization Guidelines

| Scenario | Adjustment |
|----------|------------|
| Many small PDFs (< 2MB) | Increase workers to 10, batch size 25 |
| Few large PDFs (> 50MB) | Reduce workers to 3, use chunking |
| Mixed sizes | Auto-partition by size category |
| Rate limit concerns | Add 2s delay between batches |
| Memory constraints | Use Light workers only |

## Related Workflows

- `workflow-systematic-review.md` - End-to-end SR pipeline
- `workflow-meta-analysis.md` - Meta-analysis data extraction
- `workflow-literature-search.md` - PDF acquisition from databases
