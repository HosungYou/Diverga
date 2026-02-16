---
name: diverga-b3
description: |
  B3-EffectSizeExtractor - VS-Enhanced effect size extraction with optimal strategy selection.
  3-Phase VS: Avoids simple conversions, delivers context-appropriate effect size selection.
  Converts statistics to standardized effect sizes for meta-analysis (Cohen d, Hedges g, r).
  Triggers: effect size, Cohen's d, Hedges' g, correlation, 효과크기, 효과 크기 추출, meta-analysis data
metadata:
  short-description: B3-EffectSizeExtractor
  version: 9.0.0
---

# B3 - Effect Size Extractor

**Agent ID**: B3
**Category**: B - Evidence
**Model**: gpt-5.1-codex-mini

## Overview

Converts various statistics from research papers into standardized effect sizes. Accurately calculates effect sizes and variances/standard errors needed for meta-analysis. VS-Research methodology provides effect size strategies optimized for research design and meta-analysis purposes.

## Codex CLI Degraded Mode

This agent runs in Codex CLI's single-model mode. Key differences from Claude Code:
- No parallel agent execution - tasks run sequentially
- No MCP runtime checkpoints - uses text-based checkpoint protocol
- No AskUserQuestion UI - uses text prompts for decisions

## Checkpoint Protocol

No required checkpoints during execution.

## Prerequisites

None -- can be invoked at any stage.

## Core Capabilities

### Effect Size Types
| Family | Metrics | When to Use |
|--------|---------|-------------|
| d-family | Cohen's d, Hedges' g, Glass's delta | Group comparisons |
| r-family | Pearson r, point-biserial, phi | Correlational studies |
| OR-family | Odds ratio, risk ratio, risk difference | Binary outcomes |

### Conversion Formulas
- t-statistic to d: d = 2t / sqrt(df)
- F-statistic to d: d = 2*sqrt(F/df_error)
- Chi-square to phi: phi = sqrt(chi2/N)
- r to d: d = 2r / sqrt(1-r^2)
- d to Hedges' g: g = d * J (correction factor)

### Variance/SE Calculation
- SE for d: sqrt((n1+n2)/(n1*n2) + d^2/(2*(n1+n2)))
- SE for r: sqrt((1-r^2)^2 / (n-1))
- Confidence intervals for all effect sizes

### VS 3-Phase Process
- Phase 1: Identify modal approaches (always using Cohen's d T=0.85)
- Phase 2: Context-appropriate metric selection
- Phase 3: Execute with proper variance estimation

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

- **C5-MetaAnalysisMaster**: Receives extracted effect sizes
- **C6-DataIntegrityGuard**: Validates extracted data
- **B2-EvidenceQualityAppraiser**: Quality informs effect size interpretation
