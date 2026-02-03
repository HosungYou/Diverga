# Agent I/O Contract Schema

**Version**: 1.0.0
**Based on**: Codex Review (2025-01-22)

---

## 개요

모든 Research Coordinator 에이전트는 이 표준 계약을 준수하여 상호 운용성과 추적성을 보장합니다.

## 입력 스키마 (Input Schema)

```yaml
input:
  required:
    task_id: string           # 고유 작업 식별자 (UUID)
    task_type: enum           # research_question | theory | literature | methods | quality | publication
    user_query: string        # 사용자의 원본 요청
    context:
      research_domain: string # 학문 분야 (e.g., "educational psychology")
      stage: enum             # planning | execution | validation | publication

  optional:
    prior_agents: list        # 이전에 실행된 에이전트 목록
    constraints:
      time_budget: integer    # 예상 응답 시간 (초)
      context_budget: integer # 최대 토큰 수
      quality_level: enum     # draft | standard | publication_ready
    user_preferences:
      vs_novelty_dial: float  # 0.0 (안전) ~ 1.0 (혁신적)
      language: enum          # ko | en
```

## 출력 스키마 (Output Schema)

```yaml
output:
  required:
    agent_id: string          # 에이전트 식별자 (e.g., "02-theoretical-framework-architect")
    vs_level: enum            # Full | Enhanced | Light
    execution_timestamp: datetime

    vs_metadata:
      phase_executed: list    # [0, 1, 2, 3, 4, 5]
      modal_identified: list  # 식별된 모달 옵션들
      t_scores:               # T-Score 분포
        - option: string
          score: float        # 0.0 ~ 1.0
          rationale: string
      final_selection:
        option: string
        t_score: float
        justification: string

    content:
      summary: string         # 1-3문장 요약
      main_output: object     # 에이전트별 주요 출력
      confidence: float       # 0.0 ~ 1.0

    provenance:
      sources: list           # 참조한 출처
      reasoning_trace: list   # 추론 과정 기록
      assumptions: list       # 가정 사항

  optional:
    next_agents:              # 권장 후속 에이전트
      - agent_id: string
        reason: string
        priority: enum        # required | recommended | optional

    warnings: list            # 주의사항
    limitations: list         # 한계점

    self_critique:            # Reflexion-style 자기 비판
      strengths: list
      weaknesses: list
      improvement_suggestions: list
```

## VS Phase 표준

```yaml
vs_phases:
  phase_0:
    name: "Context Collection"
    required_for: [Full, Enhanced]
    output: context_summary

  phase_1:
    name: "Modal Identification"
    required_for: [Full, Enhanced, Light]
    output: modal_options_with_t_scores

  phase_2:
    name: "Long-Tail Sampling"
    required_for: [Full, Enhanced]
    output: alternative_directions

  phase_3:
    name: "Low-Typicality Selection"
    required_for: [Full]
    output: selected_option_with_justification

  phase_4:
    name: "Execution"
    required_for: [Full, Enhanced, Light]
    output: main_content

  phase_5:
    name: "Originality Verification"
    required_for: [Full]
    output: novelty_assessment
```

## T-Score 보고 표준

```yaml
t_score_report:
  format: |
    | 옵션 | T-Score | 분류 | 근거 |
    |------|---------|------|------|
    | {option} | {0.XX} | {modal/established/emerging/creative} | {rationale} |

  classification:
    modal: "> 0.8"
    established: "0.5 - 0.8"
    emerging: "0.3 - 0.5"
    creative: "< 0.3"
```

## Self-Critique 표준 (Reflexion-inspired)

모든 Full VS 에이전트는 출력에 자기 비판 섹션을 포함해야 합니다:

```yaml
self_critique:
  template: |
    ### 자기 평가 (Self-Critique)

    **강점**:
    - [이 추천의 장점]

    **약점**:
    - [잠재적 한계 또는 위험]

    **개선 제안**:
    - [후속 작업 또는 보완 필요 사항]

    **대안적 관점**:
    - [다른 연구자가 제기할 수 있는 반론]
```

## 에이전트 간 핸드오프 프로토콜

```yaml
handoff:
  from_agent: string
  to_agent: string
  handoff_type: enum  # sequential | parallel | conditional

  context_transfer:
    summary: string           # 100단어 이내 요약
    key_decisions: list       # 핵심 결정 사항
    open_questions: list      # 미해결 질문
    constraints_inherited: list

  validation:
    required_fields_check: boolean
    schema_compliance: boolean
    vs_phase_completion: boolean
```

## 검증 규칙

```python
def validate_agent_output(output: dict) -> ValidationResult:
    """에이전트 출력 검증"""

    errors = []
    warnings = []

    # 1. 필수 필드 존재 확인
    required = ['agent_id', 'vs_level', 'vs_metadata', 'content']
    for field in required:
        if field not in output:
            errors.append(f"Missing required field: {field}")

    # 2. VS 메타데이터 검증
    vs_meta = output.get('vs_metadata', {})
    if not vs_meta.get('modal_identified'):
        warnings.append("Modal options not identified")

    if not vs_meta.get('t_scores'):
        errors.append("T-scores not provided")

    # 3. T-Score 범위 검증
    for ts in vs_meta.get('t_scores', []):
        if not 0 <= ts.get('score', -1) <= 1:
            errors.append(f"Invalid T-score: {ts.get('score')}")

    # 4. Full VS 에이전트는 self_critique 필수
    if output.get('vs_level') == 'Full':
        if 'self_critique' not in output:
            warnings.append("Full VS agent should include self_critique")

    return ValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        warnings=warnings
    )
```

## 관련 문서

- `VS-Research-Framework.md`: VS 방법론 상세
- `agent-registry.yaml`: 에이전트 레지스트리
- `evaluation-harness.md`: 평가 하네스 가이드
