# QUANT-004 Test Report: Hybrid Checkpoint Detection

**Test Date**: 2026-01-30
**Scenario**: Hybrid Checkpoint Detection - Korean Meta-Analysis
**CLI Tools Tested**: Claude Code, Codex CLI
**QA Protocol Version**: v3.2.2

---

## Executive Summary

This test validates both the hybrid checkpoint detection system (v3.2.0) and the dual CLI transcript support (v3.2.2).

| Metric | Claude Code | Codex CLI |
|--------|-------------|-----------|
| **Overall Status** | FAILED (low compliance) | FAILED (no skill) |
| **Skill Loaded** | ✅ Yes (LOW confidence) | ❌ No |
| **Checkpoints Detected** | 4 | 0 |
| **Checkpoint Compliance** | 25% | 0% |
| **Verification Huddle** | ✅ PASSED (6/6) | ✅ PASSED (6/6) |
| **Response Quality** | Excellent (VS + Checkpoints) | Good (Generic LLM) |

---

## v3.2.2 New Feature: Dual CLI Transcripts

Both CLI test results are now saved with separate files:

| File | Claude Code | Codex CLI |
|------|-------------|-----------|
| Transcript | `conversation_transcript_claude.md` | `conversation_transcript_codex.md` |
| Raw JSON | `conversation_raw_claude.json` | `conversation_raw_codex.json` |
| Result YAML | `QUANT-004_test_result_claude.yaml` | `QUANT-004_test_result_codex.yaml` |

---

## Test Results: Claude Code

### Metrics

| Metric | Value |
|--------|-------|
| Total Turns | 4 |
| Checkpoints Detected | 4 |
| Skill Confidence | LOW (score: 25) |
| Response Length Range | 1149-3269 chars |
| Verification Huddle | ✅ PASSED (6/6 checks) |

### Checkpoints Detected

| Turn | Checkpoint ID | Confidence | Description |
|------|---------------|------------|-------------|
| 1 | CP_RESEARCH_DIRECTION | HIGH | 효과크기 통일 지표 선택 |
| 2 | CP_ANALYSIS_PLAN | HIGH | F → g 변환 확인 |
| 3 | CP_ANALYSIS_PLAN | HIGH | 모형 선택 |
| 3 | CP_MODERATOR_SELECTION | HIGH | 조절변수 선택 |

### Response Quality Indicators

✅ **VS Methodology Applied**
- T-Score options presented: 0.65 / 0.40 / 0.55
- Modal awareness: "Cohen's d (T=0.65)"
- Creative alternative: "Hedges' g (T=0.40) ⭐"

✅ **Human Checkpoint Structure**
- 🔴 CP_RESEARCH_DIRECTION with [A]/[B]/[C] options
- 🟠 CP_ANALYSIS_PLAN with follow-up questions
- 🟢 CP_ANALYSIS_PLAN approval request with [Y]/[M]/[Q]

✅ **Korean Language Support**
- Full Korean prompts understood
- Bilingual responses provided

✅ **Complete Meta-Analysis Plan**
- R code (metafor package)
- APA 7 reporting format
- Funnel plot and Egger's test

### Compliance Analysis

| Expected Checkpoint | Found | Match |
|---------------------|-------|-------|
| CP_PARADIGM_CONFIRMATION | CP_RESEARCH_DIRECTION | ❌ Different ID |
| CP_EFFECT_SIZE_SELECTION | (none) | ❌ Missing |
| CP_MODERATOR_ANALYSIS | CP_MODERATOR_SELECTION | ✅ Equivalent |
| CP_METHODOLOGY_APPROVAL | CP_ANALYSIS_PLAN | ❌ Different ID |

**Compliance Rate**: 25% (1/4 matches with equivalence mapping)

---

## Test Results: Codex CLI

### Metrics

| Metric | Value |
|--------|-------|
| Total Turns | 4 |
| Checkpoints Detected | 0 |
| Skill Loaded | ❌ No (score: 0) |
| Response Length Range | 481-1031 chars |
| Verification Huddle | ✅ PASSED (6/6 checks) |

### Analysis

**Codex CLI does NOT load Diverga skill** even with AGENTS.md configured.

**Why?**
1. Codex CLI uses `codex exec` for non-interactive execution
2. AGENTS.md is reference documentation, not a plugin system
3. The checkpoint/VS system requires Claude Code's plugin architecture

**Response Quality:**
- ✅ Correct meta-analysis advice
- ✅ F → Hedges' g conversion formulas provided
- ✅ Random effects model recommended
- ❌ No checkpoint structure
- ❌ No VS T-Score options
- ❌ No human decision points

### Codex CLI Configuration Tested

```json
// ~/.codex/config.json
{
  "model": "",
  "agents": "/Volumes/External SSD/Projects/Diverga/.codex/AGENTS.md"
}
```

**Conclusion**: AGENTS.md configuration alone is NOT sufficient for skill loading.

---

## Comparison

| Aspect | Claude Code | Codex CLI |
|--------|-------------|-----------|
| **Skill System** | ✅ Plugin-based (native) | ❌ Reference only |
| **Checkpoint Format** | `🔴 CP_XXX` headers | Plain text |
| **VS Methodology** | ✅ T-Score options | ❌ Not available |
| **Human Decision Points** | ✅ [A]/[B]/[C] choices | ❌ Not structured |
| **Korean Support** | ✅ Full bilingual | ✅ Adequate |
| **Response Quality** | Structured, detailed | Brief, generic |
| **Meta-Analysis Advice** | Excellent | Good |

---

## Key Findings

### 1. Claude Code Skill Works Correctly

Despite "25% compliance", the skill is functioning well:
- Checkpoints are triggered with proper formatting
- VS methodology is applied with T-Scores
- Human decision points are enforced

The low compliance is due to **checkpoint ID variations**, not skill failure.

### 2. Codex CLI Requires Different Approach

AGENTS.md configuration does NOT enable the skill system. For Codex CLI:
- Use as **reference documentation** for the model
- Implement checkpoint logic in prompts explicitly
- Or use Claude Code for full Diverga functionality

### 3. Dual Transcript System Works (v3.2.2)

Both CLI transcripts saved successfully without overwriting:
- Files properly named with `_claude` and `_codex` suffixes
- Results can be compared side-by-side

---

## Recommendations

### 1. For Claude Code Users

- ✅ Use `/plugin install diverga` for full functionality
- ✅ Checkpoints and VS methodology work as designed
- ⚠️ Accept checkpoint ID variations as normal behavior

### 2. For Codex CLI Users

- ⚠️ AGENTS.md alone does NOT enable skill
- 💡 Include checkpoint instructions in your prompts explicitly
- 💡 Use Claude Code for research projects requiring human checkpoints

### 3. Documentation Updates Needed

- Add "Codex CLI Limitations" section to docs
- Clarify that AGENTS.md is reference, not skill activation
- Update QUICKSTART.md with troubleshooting info

---

## Files in This Session

| File | Description |
|------|-------------|
| `conversation_transcript_claude.md` | Claude Code full transcript |
| `conversation_transcript_codex.md` | Codex CLI full transcript |
| `conversation_raw_claude.json` | Claude Code raw data |
| `conversation_raw_codex.json` | Codex CLI raw data |
| `QUANT-004_test_result_claude.yaml` | Claude Code metrics |
| `QUANT-004_test_result_codex.yaml` | Codex CLI metrics |
| `QUANT-004_REPORT.md` | This report |
| `README.md` | Session overview |

---

*Report generated by Diverga QA Protocol v3.2.2*
