# VS Behavior Evaluation Harness

**Version**: 1.0.0
**Based on**: Codex Review (2025-01-22) + VS Methodology (arXiv:2510.01171)

---

## 개요

VS 행동 평가 하네스는 Research Coordinator의 20개 에이전트가 VS 방법론을 올바르게 적용하는지 자동으로 검증합니다.

## 평가 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                    VS Evaluation Harness                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │ Test Cases   │───▶│ Agent Under  │───▶│ Validator    │       │
│  │ (Golden Set) │    │ Test (AUT)   │    │ Engine       │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│         │                   │                   │                │
│         ▼                   ▼                   ▼                │
│  ┌──────────────────────────────────────────────────────┐       │
│  │                 Metrics Collector                      │       │
│  │  • VS Phase Completion                                │       │
│  │  • T-Score Distribution                               │       │
│  │  • Modal Diversity                                    │       │
│  │  • Self-Critique Quality                              │       │
│  └──────────────────────────────────────────────────────┘       │
│                            │                                     │
│                            ▼                                     │
│  ┌──────────────────────────────────────────────────────┐       │
│  │                 Report Generator                       │       │
│  └──────────────────────────────────────────────────────┘       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 테스트 케이스 구조

### Golden Set: 표준 테스트 입력

```yaml
test_cases:
  # Full VS 에이전트 테스트 (02, 03, 05, 10, 16)
  full_vs_tests:
    - id: "FULL-01"
      agent: "02-theoretical-framework-architect"
      input:
        research_question: "AI 기반 학습 지원 시스템이 학습자의 자기조절학습에 미치는 영향"
        domain: "educational psychology"
        innovation_level: 0.6
      expected:
        vs_phases: [0, 1, 2, 3, 4, 5]
        modal_count: ">= 3"
        t_score_range: [0.0, 1.0]
        has_self_critique: true
        has_alternatives: true

    - id: "FULL-02"
      agent: "03-devils-advocate"
      input:
        research_design:
          type: "quasi-experimental"
          sample_size: 120
          variables: ["AI_support", "self_regulation", "learning_outcome"]
        critique_intensity: "moderate"
      expected:
        vs_phases: [0, 1, 2, 3, 4, 5]
        critique_count: ">= 5"
        has_rebuttals: true
        has_self_critique: true

  # Enhanced VS 에이전트 테스트 (01, 04, 06, 07, 08, 09)
  enhanced_vs_tests:
    - id: "ENH-01"
      agent: "01-research-question-refiner"
      input:
        research_idea: "AI가 교육에 좋은지 연구하고 싶어요"
        domain: "education"
      expected:
        vs_phases: [0, 1, 2, 4]
        refined_questions: ">= 2"
        pico_elements: true

  # Light VS 에이전트 테스트 (11-15, 17-20)
  light_vs_tests:
    - id: "LIGHT-01"
      agent: "11-analysis-code-generator"
      input:
        analysis_type: "mediation"
        software: "R"
        variables: ["X", "M", "Y"]
      expected:
        vs_phases: [0, 1, 4]
        code_generated: true
        modal_awareness: true
```

## 검증 규칙

### 1. VS Phase Completion

```python
def validate_vs_phases(output: dict, expected_level: str) -> ValidationResult:
    """VS 단계 완료 검증"""

    required_phases = {
        "Full": [0, 1, 2, 3, 4, 5],
        "Enhanced": [0, 1, 2, 4],
        "Light": [0, 1, 4]
    }

    actual_phases = output.get('vs_metadata', {}).get('phase_executed', [])
    expected = required_phases[expected_level]

    missing = set(expected) - set(actual_phases)
    extra = set(actual_phases) - set(expected)

    return ValidationResult(
        passed=len(missing) == 0,
        missing_phases=list(missing),
        extra_phases=list(extra),
        score=len(set(actual_phases) & set(expected)) / len(expected)
    )
```

### 2. T-Score Distribution

```python
def validate_t_score_distribution(output: dict) -> ValidationResult:
    """T-Score 분포 검증 - Mode Collapse 탐지"""

    t_scores = output.get('vs_metadata', {}).get('t_scores', [])

    if not t_scores:
        return ValidationResult(passed=False, reason="No T-scores provided")

    scores = [ts['score'] for ts in t_scores]

    # Mode Collapse 탐지: 모든 점수가 0.8 이상이면 문제
    modal_only = all(s > 0.8 for s in scores)

    # 다양성 체크: 적어도 하나는 0.6 미만이어야 함
    has_diversity = any(s < 0.6 for s in scores)

    # 최종 선택이 Modal이 아닌지 확인
    final = output.get('vs_metadata', {}).get('final_selection', {})
    final_is_modal = final.get('t_score', 1.0) > 0.8

    return ValidationResult(
        passed=has_diversity and not final_is_modal,
        modal_collapse_detected=modal_only,
        diversity_score=1 - (max(scores) - min(scores)),
        final_selection_t_score=final.get('t_score')
    )
```

### 3. Self-Critique Quality

```python
def validate_self_critique(output: dict) -> ValidationResult:
    """Self-Critique 품질 검증 (Full VS만)"""

    critique = output.get('self_critique', {})

    if not critique:
        return ValidationResult(passed=False, reason="No self-critique provided")

    checks = {
        'has_strengths': len(critique.get('strengths', [])) >= 2,
        'has_weaknesses': len(critique.get('weaknesses', [])) >= 2,
        'has_improvements': len(critique.get('improvement_suggestions', [])) >= 1,
        'has_alternatives': 'alternative_perspectives' in critique or
                           len(critique.get('weaknesses', [])) >= 1
    }

    score = sum(checks.values()) / len(checks)

    return ValidationResult(
        passed=score >= 0.75,
        checks=checks,
        quality_score=score
    )
```

### 4. Provenance Completeness

```python
def validate_provenance(output: dict) -> ValidationResult:
    """출처 추적성 검증"""

    provenance = output.get('provenance', {})

    checks = {
        'has_sources': len(provenance.get('sources', [])) >= 1,
        'has_reasoning': len(provenance.get('reasoning_trace', [])) >= 1,
        'has_assumptions': 'assumptions' in provenance
    }

    return ValidationResult(
        passed=all(checks.values()),
        checks=checks
    )
```

## 회귀 테스트 실행

### CLI 인터페이스

```bash
# 전체 테스트 실행
./scripts/run_vs_tests.sh --all

# 특정 에이전트만 테스트
./scripts/run_vs_tests.sh --agent 02-theoretical-framework-architect

# VS 레벨별 테스트
./scripts/run_vs_tests.sh --level Full

# CI/CD 통합용 (JSON 출력)
./scripts/run_vs_tests.sh --all --format json > test_results.json
```

### 테스트 결과 포맷

```yaml
test_run:
  timestamp: "2025-01-22T15:30:00Z"
  total_tests: 20
  passed: 18
  failed: 2

  summary:
    full_vs:
      agents_tested: 5
      pass_rate: 100%
      avg_t_score_diversity: 0.72

    enhanced_vs:
      agents_tested: 6
      pass_rate: 83.3%
      issues:
        - agent: "04-research-ethics-advisor"
          issue: "Phase 3 missing"

    light_vs:
      agents_tested: 9
      pass_rate: 100%

  detailed_results:
    - test_id: "FULL-01"
      agent: "02-theoretical-framework-architect"
      status: "PASSED"
      metrics:
        vs_phase_score: 1.0
        t_score_diversity: 0.75
        self_critique_quality: 0.88
        provenance_completeness: 1.0

    - test_id: "ENH-03"
      agent: "04-research-ethics-advisor"
      status: "FAILED"
      metrics:
        vs_phase_score: 0.75
        issue: "Phase 3 (Low-Typicality Selection) not executed"
      remediation: "Add Phase 3 to Enhanced VS agents or reclassify"
```

## Mode Collapse 탐지 알고리즘

```python
def detect_mode_collapse(agent_outputs: list) -> ModeCollapseReport:
    """다중 실행에서 Mode Collapse 패턴 탐지"""

    # 동일 입력에 대한 여러 출력 비교
    recommendations = [
        o['vs_metadata']['final_selection']['option']
        for o in agent_outputs
    ]

    # 엔트로피 계산
    from collections import Counter
    counts = Counter(recommendations)
    total = len(recommendations)
    entropy = -sum((c/total) * log2(c/total) for c in counts.values())

    # 최대 엔트로피 (완전 균등 분포)
    max_entropy = log2(len(set(recommendations)))

    # 정규화된 다양성 점수
    diversity = entropy / max_entropy if max_entropy > 0 else 0

    return ModeCollapseReport(
        unique_recommendations=len(set(recommendations)),
        total_runs=len(recommendations),
        diversity_score=diversity,
        mode_collapse_detected=diversity < 0.3,
        most_common=counts.most_common(3)
    )
```

## 지속적 모니터링

### GitHub Actions 통합

```yaml
# .github/workflows/vs-evaluation.yml
name: VS Behavior Evaluation

on:
  push:
    paths:
      - '.claude/skills/research-agents/**'
  pull_request:
    paths:
      - '.claude/skills/research-agents/**'

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run VS Evaluation
        run: |
          ./scripts/run_vs_tests.sh --all --format json > results.json

      - name: Check for Regressions
        run: |
          python scripts/check_regressions.py results.json

      - name: Upload Results
        uses: actions/upload-artifact@v4
        with:
          name: vs-evaluation-results
          path: results.json
```

## 평가 메트릭 대시보드

```
┌─────────────────────────────────────────────────────────────────┐
│                VS Evaluation Dashboard                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Overall Health: ████████░░ 85%                                 │
│                                                                  │
│  ┌─────────────────┬─────────────────┬─────────────────┐        │
│  │   Full VS (5)   │ Enhanced VS (6) │  Light VS (9)   │        │
│  ├─────────────────┼─────────────────┼─────────────────┤        │
│  │  Phase: 100%    │  Phase: 83%     │  Phase: 100%    │        │
│  │  T-Score: 0.72  │  T-Score: 0.65  │  T-Score: N/A   │        │
│  │  Critique: 88%  │  Critique: N/A  │  Critique: N/A  │        │
│  └─────────────────┴─────────────────┴─────────────────┘        │
│                                                                  │
│  Recent Issues:                                                  │
│  ⚠️ Agent 04: Phase 3 missing                                   │
│  ⚠️ Agent 07: T-Score diversity below threshold                 │
│                                                                  │
│  Mode Collapse Status: ✅ Not Detected                          │
│  Last 10 runs diversity: 0.78                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 관련 문서

- `agent-contract-schema.md`: 출력 스키마 정의
- `agent-registry.yaml`: 에이전트 레지스트리
- `self-critique-framework.md`: Self-Critique 프레임워크
- `VS-Research-Framework.md`: VS 방법론 상세
