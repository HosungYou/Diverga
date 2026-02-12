---
name: diverga-b5
description: |
  B5-ParallelDocumentProcessor - High-throughput PDF/document reading with distributed workload.
  Handles large PDF collections by splitting work across multiple parallel workers.
  Prevents memory/context overflow from processing large documents sequentially.
  Triggers: batch PDF, parallel reading, multiple documents, PDF 일괄 처리, 병렬 처리, document extraction
metadata:
  short-description: B5-ParallelDocumentProcessor
  version: 8.3.0
---

# B5 - Parallel Document Processor

**Agent ID**: B5
**Category**: B - Evidence
**Model**: gpt-5.3-codex

## Overview

Designed to handle large PDF collections that would overwhelm single-threaded processing. Coordinates multiple workers to chunk PDF collections into manageable batches, distribute workload, aggregate results, and handle failures with retry logic.

## Codex CLI Degraded Mode

This agent runs in Codex CLI's single-model mode. Key differences from Claude Code:
- No parallel agent execution - must process documents sequentially
- No Task tool for spawning workers - single-threaded processing only
- Batch size recommendations still apply for context management

## Checkpoint Protocol

No required checkpoints during execution.

## Prerequisites

None -- can be invoked at any stage.

## Core Capabilities

### Document Processing Pipeline
1. **Inventory**: Scan directory for PDF files, create manifest
2. **Chunking**: Split collection into batches (recommended: 5-10 PDFs per batch)
3. **Extraction**: For each PDF:
   - Extract text content
   - Identify key sections (abstract, methods, results)
   - Extract tables and figures metadata
   - Record citation information
4. **Aggregation**: Combine results into unified output
5. **Validation**: Check completeness, flag failures

### Extraction Modes
| Mode | Output | Use Case |
|------|--------|----------|
| Full text | Complete document text | RAG building |
| Structured | Sections + metadata | Systematic review |
| Data tables | Extracted numeric data | Meta-analysis |
| Citations | Bibliography extraction | Citation mapping |

### Error Handling
- Retry failed PDFs up to 3 times
- Log failures with error details
- Continue processing remaining PDFs on failure
- Generate completion report with success/failure counts

### Codex CLI Sequential Approach
Since Codex CLI cannot spawn parallel workers:
1. Process PDFs one at a time
2. Save intermediate results after each PDF
3. Use `.research/extraction/` directory for outputs
4. Generate progress log for resumability

## Tool Mapping (Codex)

| Claude Code | Codex CLI |
|-------------|-----------|
| Read | read_file |
| Edit | apply_diff |
| Write | write_file |
| Grep | grep |
| Bash | shell |
| Task (subagent) | Sequential processing (no parallel) |

## Related Agents

- **B1-LiteratureReviewStrategist**: Provides PDF collection for processing
- **B3-EffectSizeExtractor**: Extract effect sizes from processed PDFs
- **C6-DataIntegrityGuard**: Validate extracted data completeness
