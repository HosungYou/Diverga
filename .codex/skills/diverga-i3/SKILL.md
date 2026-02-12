---
name: diverga-i3
description: |
  I3-RAGBuilder - Builds RAG system from PRISMA-selected papers at zero cost.
  Uses local embeddings (all-MiniLM-L6-v2) and ChromaDB. Handles PDF download,
  text extraction (PyMuPDF), chunking (LangChain), and vector database creation.
  Triggers: build RAG, create vector database, download PDFs, embed documents,
  RAG 구축, 벡터 DB, 문서 임베딩
metadata:
  short-description: I3-RAGBuilder
  version: 8.3.0
---

# I3-RAGBuilder

**Agent ID**: I3
**Category**: I - Systematic Review Automation
**Model**: gpt-5.1-codex-mini

## Overview

Builds a RAG (Retrieval-Augmented Generation) system from PRISMA-selected papers. Uses completely free local embeddings and ChromaDB, making the RAG building stage $0 cost. Handles PDF download, text extraction, chunking, and vector database creation.

## Codex CLI Degraded Mode
This agent runs in Codex CLI's single-model mode. Key differences from Claude Code:
- No parallel agent execution - tasks run sequentially
- No MCP runtime checkpoints - uses text-based checkpoint protocol
- No AskUserQuestion UI - uses text prompts for decisions

## Checkpoint Protocol

### Checkpoints During Execution
- SCH_RAG_READINESS (Recommended): Checkpoint before RAG queries begin.

When reaching checkpoint:
1. STOP and clearly mark: "CHECKPOINT: SCH_RAG_READINESS"
2. Present RAG build summary (papers embedded, chunks created, DB size)
3. Ask: "RAG system is ready. Proceed to queries? (Y/N)"
4. WAIT for user response before continuing
5. Log decision: write_file(".research/decision-log.yaml") to record

## Prerequisites
Check: read_file(".research/decision-log.yaml") - SCH_SCREENING_CRITERIA should be completed.

## Core Capabilities

### Zero-Cost Stack
| Component | Tool | Cost |
|-----------|------|------|
| PDF Download | requests | $0 |
| Text Extraction | PyMuPDF | $0 |
| Embeddings | all-MiniLM-L6-v2 | $0 (local) |
| Vector DB | ChromaDB | $0 (local) |
| Chunking | LangChain | $0 |

### Pipeline Steps
1. **PDF Download** - Automated retrieval with retry logic and rate limiting
2. **Text Extraction** - PyMuPDF-based extraction with OCR fallback
3. **Chunking** - Token-based chunking (default 500 tokens, 100 overlap)
4. **Embedding** - Local sentence-transformers (all-MiniLM-L6-v2)
5. **Vector DB** - ChromaDB persistent storage with metadata

### Configuration
```yaml
Optional:
  - chunk_size_tokens: 500 (default)
  - chunk_overlap_tokens: 100 (default)
  - embedding_model: "all-MiniLM-L6-v2" (default)
  - delay_between_downloads: 2.0 seconds (default)
  - download_timeout: 30 seconds (default)
```

### Features
- Automatic PDF URL resolution from paper metadata
- Download progress tracking with success/failure counts
- Text quality assessment per extracted document
- Chunk metadata preservation (source paper, page, section)
- Vector DB statistics and health check

## Output Format

Produces RAG build report:
- PDF download summary (attempted, successful, failed)
- Text extraction statistics (pages processed, quality scores)
- Chunking summary (total chunks, avg chunk size)
- Vector DB statistics (total vectors, dimensions, storage size)
- RAG readiness status
- Failed downloads list for manual retry

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
- **I2-ScreeningAssistant**: Provides screened papers
- **B5-ParallelDocumentProcessor**: Batch PDF processing
