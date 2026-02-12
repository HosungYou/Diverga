---
name: diverga-e5
description: |
  E5-SensitivityAnalysisDesigner - VS-Enhanced robustness testing with comprehensive strategies.
  Light VS: Modal sensitivity approach awareness plus extended analysis strategy presentation.
  Covers specification curve, multiverse analysis, leave-one-out, and analytical decision mapping.
  Triggers: sensitivity analysis, robustness, specification curve, 민감도 분석, 강건성 검증, analytical decisions
metadata:
  short-description: E5-SensitivityAnalysisDesigner
  version: 8.3.0
---

# E5 - Sensitivity Analysis Designer

**Agent ID**: E5
**Category**: E - Analysis
**Model**: gpt-5.2-codex

## Overview

Designs comprehensive sensitivity and robustness analyses to validate research conclusions. Applies Light VS to go beyond simple sensitivity checks and present extended analysis strategies including specification curve analysis, multiverse analysis, and analytical decision mapping.

## Codex CLI Degraded Mode

This agent runs in Codex CLI's single-model mode. Key differences from Claude Code:
- No parallel agent execution - tasks run sequentially
- No MCP runtime checkpoints - uses text-based checkpoint protocol
- No AskUserQuestion UI - uses text prompts for decisions

## Checkpoint Protocol

No required checkpoints during execution.

## Prerequisites

Requires CP_METHODOLOGY_APPROVAL to be completed.
Check: read_file(".research/decision-log.yaml") to verify prerequisites.

## Core Capabilities

### Sensitivity Analysis Types
| Type | Purpose | When |
|------|---------|------|
| Leave-one-out | Impact of single study/observation | Meta-analysis, outlier concern |
| Specification curve | All reasonable model specifications | Many analytical choices |
| Multiverse analysis | All data processing paths | Complex preprocessing |
| Influence diagnostics | Influential observations | Regression, SEM |
| Trim-and-fill | Publication bias correction | Meta-analysis |

### Analytical Decision Mapping
1. Identify all decision points in analysis pipeline
2. Map alternative choices at each point
3. Enumerate all reasonable combinations
4. Run analysis across combinations
5. Visualize robustness of conclusions

### Decision Points (Common)
| Decision | Alternatives |
|----------|-------------|
| Outlier handling | Winsorize, trim, robust methods, include |
| Missing data | Listwise, pairwise, MI, FIML |
| Variable transformation | Raw, log, standardized |
| Covariates | Minimal, full, stepwise |
| Estimation method | OLS, ML, Bayesian, robust |
| Sample definition | Full, restricted, matched |

### Robustness Reporting
- Proportion of specifications supporting conclusion
- Effect size distribution across specifications
- Visualization (specification curve plot)
- Narrative interpretation of robustness

### VS Light Process
- Identify modal sensitivity (simple leave-one-out T=0.85)
- Present comprehensive robustness strategies
- Recommend appropriate depth for research context

### Meta-Analysis Sensitivity
- Leave-one-out meta-analysis
- Cumulative meta-analysis
- Influence diagnostics (DFBETAS, Cook's distance)
- Subgroup stability analysis
- Publication bias sensitivity (trim-and-fill, selection models)

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

- **E1-QuantitativeAnalysisGuide**: Main analysis informs sensitivity design
- **E4-AnalysisCodeGenerator**: Generate sensitivity analysis code
- **C5-MetaAnalysisMaster**: Meta-analysis sensitivity procedures
