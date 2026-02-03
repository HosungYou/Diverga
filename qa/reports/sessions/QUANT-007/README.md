# QUANT-007: Meta-Analysis Systematic Review (Category I + C5 Integration)

**Test Date**: 2026-01-30
**Status**: ✅ Claude Code PASSED | ✅ Codex CLI PASSED
**CLI Tools**: Claude Code (Opus 4.5), Codex CLI (v0.92.0)

## Test Objective

Verify that a meta-analysis request properly triggers **both**:
1. Category I agents (I0-I3) for systematic literature review automation
2. Category C5 (MetaAnalysisMaster) for effect size analysis

## Test Prompt (동일한 프롬프트로 양쪽 CLI 테스트)

```
AI 학습 도우미(chatbots/tutors)가 외국어 말하기 능력에 미치는 효과에 대한
체계적 문헌고찰과 메타분석을 수행하려고 합니다.

PRISMA 2020 가이드라인에 따라 진행해 주세요.

현재 가지고 있는 정보:
- 연구 주제: AI chatbots for speaking skills in language learning
- 예상 논문 수: 약 50-100편
- 효과크기: Cohen's d, Hedges' g, 상관계수 r 혼재
- 데이터베이스: Semantic Scholar, OpenAlex, arXiv 사용 예정
```

## Expected Agent Activations

| Agent | Trigger | Expected Checkpoint |
|-------|---------|---------------------|
| **I0-ScholarAgentOrchestrator** | "체계적 문헌고찰", "PRISMA" | Pipeline coordination |
| **I1-PaperRetrievalAgent** | Database selection | 🔴 SCH_DATABASE_SELECTION |
| **I2-ScreeningAssistant** | "PRISMA 2020" | 🔴 SCH_SCREENING_CRITERIA |
| **C5-MetaAnalysisMaster** | "메타분석", "효과크기" | 🔴 CP_EFFECT_SIZE_SELECTION |

## Files

| File | Status | Description |
|------|--------|-------------|
| `README.md` | ✅ | This file |
| `claude_code_turn1_raw.txt` | ✅ | Claude Code Turn 1: I0 invocation |
| `claude_code_turn2_raw.txt` | ✅ | Claude Code Turn 2: C5 invocation |
| `codex_turn1_raw.txt` | ✅ | Codex CLI Turn 1: Meta-analysis prompt |
| `codex_test_instructions.md` | ✅ | Manual test guide (backup) |
| `QUANT-007_REPORT.md` | ✅ | Final analysis report |

## Raw Transcript Format

Each turn file captures:
```
=== SESSION METADATA ===
CLI: Claude Code / Codex CLI
Model: opus-4.5 / gpt-5.2-codex
Session ID: [auto-generated]
Timestamp: [ISO 8601]

=== USER INPUT ===
[The test prompt]

=== TOOL CALLS ===
[Actual tool invocations with parameters]

=== TOOL RESULTS ===
[Actual responses from tools/agents]

=== FINAL OUTPUT ===
[What the user sees]

=== TOKEN USAGE ===
[If available]
```

## Success Criteria

1. ✅ I0-I3 agents recognized and invocable
2. ✅ C5 agent activates for meta-analysis component
3. ✅ Human checkpoints displayed (SCH_* and CP_*)
4. ✅ VS T-Score options presented
5. ✅ Behavioral halt enforced (waiting for user approval)
6. ✅ Korean language support confirmed

## Related

- QUANT-005: Codex CLI skill loading verification
- QUANT-006: Category I agent registration verification
