---
name: user-checkpoints
description: |
  Centralized user checkpoint system for Research Coordinator v3.0.
  Implements AskUserQuestion pattern for all major decision points.
version: "3.0.0"
---

# User Checkpoints System v3.0

## Overview

This module defines all user interaction checkpoints using the AskUserQuestion tool pattern. In "Full Collaboration" mode, users are consulted at every major decision point.

## Checkpoint Types

| Type | Icon | Purpose | Example |
|------|------|---------|---------|
| PREFERENCE | 🔵 | User preference selection | Creativity level |
| APPROVAL | 🟡 | Explicit approval needed | Analogy acceptance |
| GUARDRAIL | 🔴 | Risk acknowledgment | Low T-Score warning |
| ITERATION | 🟢 | Process control | Satisfaction check |

## Standard Schema

All checkpoints follow this schema for AskUserQuestion integration:

```yaml
checkpoint:
  id: "CP-{MODULE}-{NUMBER}"
  type: "PREFERENCE | APPROVAL | GUARDRAIL | ITERATION"
  phase: "VS Phase or module name"

  question:
    header: "Max 12 chars label"
    text: "Clear question text"
    context: "Current situation (optional)"

  options:
    - label: "Option display text"
      description: "Detailed explanation"
      risk_level: "low | medium | high"  # GUARDRAIL only
      recommended: true | false

  multiSelect: true | false
  fallback: "Default action if no response"
```

---

## Initialization Checkpoints

### CP-INIT-001: Research Type Selection

```yaml
id: CP-INIT-001
type: PREFERENCE
phase: initialization

question:
  header: "연구 유형"
  text: "이 연구의 유형을 선택해주세요."

options:
  - label: "양적 연구 (Quantitative)"
    description: "통계적 분석 기반 연구"
    recommended: false
  - label: "질적 연구 (Qualitative)"
    description: "심층 인터뷰, 관찰 등 질적 방법"
    recommended: false
  - label: "혼합 연구 (Mixed Methods)"
    description: "양적+질적 방법 통합"
    recommended: false
  - label: "메타분석 (Meta-analysis)"
    description: "기존 연구 통합 분석"
    recommended: false

multiSelect: false
fallback: "양적 연구"
```

### CP-INIT-002: Creativity Level Selection

```yaml
id: CP-INIT-002
type: PREFERENCE
phase: initialization

question:
  header: "창의성 수준"
  text: "이 연구에서 원하시는 창의성 수준을 선택해주세요."
  context: "높은 창의성은 더 독창적인 결과를 제공하지만, 학술적 방어가 더 필요합니다."

options:
  - label: "Conservative (T≥0.5)"
    description: "검증된 접근, 안전한 선택. 첫 출판이나 보수적 저널에 적합."
    risk_level: low
    recommended: false
  - label: "Balanced (T≥0.3) (권장)"
    description: "차별화와 안전성의 균형. 대부분의 연구에 적합."
    risk_level: low
    recommended: true
  - label: "Innovative (T≥0.2)"
    description: "높은 기여 가능성, 추가 정당화 필요. 혁신 지향 저널에 적합."
    risk_level: medium
    recommended: false
  - label: "Extreme (T<0.2)"
    description: "최대 창의성, 높은 위험. 탑티어 저널이나 패러다임 전환 목표."
    risk_level: high
    recommended: false

multiSelect: false
fallback: "Balanced (T≥0.3)"
```

### CP-INIT-003: T-Score Mode Selection

```yaml
id: CP-INIT-003
type: PREFERENCE
phase: initialization

question:
  header: "T-Score 모드"
  text: "T-Score 계산 방식을 선택해주세요."

options:
  - label: "정적 (Static)"
    description: "사전 정의된 테이블 사용. 빠르고 안정적, 오프라인 가능."
    recommended: false
  - label: "동적 (Dynamic) (권장)"
    description: "API로 실시간 데이터 조회. 가장 정확, 약간 느릴 수 있음."
    recommended: true
  - label: "하이브리드 (Hybrid)"
    description: "정적 기준선 + 트렌드 보정. 균형 잡힌 접근."
    recommended: false

multiSelect: false
fallback: "정적 (Static)"
```

---

## VS Engine Checkpoints

### CP-VS-001: Direction Selection

```yaml
id: CP-VS-001
type: PREFERENCE
phase: "VS Phase 2"

question:
  header: "탐색 방향"
  text: "탐색할 방향을 선택해주세요. 여러 개 선택 가능합니다."
  context: "선택한 방향들을 심층 분석합니다."

options:
  # Options are dynamically generated based on VS Phase 2 output
  # Template:
  - label: "방향 A (T=0.X): [이론/방법명]"
    description: "[간략 설명]. 적합: [타겟]"
    recommended: false  # Typically B or C is recommended

multiSelect: true
fallback: "방향 B, C 자동 선택"
```

### CP-VS-002: Low-Typicality Risk Warning

```yaml
id: CP-VS-002
type: GUARDRAIL
phase: "VS Phase 3"

question:
  header: "위험 확인"
  text: "선택하신 옵션의 T-Score가 [X]로, 학술적 근거가 제한적입니다. 진행하시겠습니까?"
  context: |
    고려사항:
    - 피어리뷰에서 추가 정당화 필요
    - 측정도구 개발/번안 가능성
    - 리뷰어 설득을 위한 강한 논리 필요

options:
  - label: "예, 진행합니다"
    description: "위험을 수용하고 혁신적 접근을 진행합니다."
    risk_level: high
    recommended: false
  - label: "더 안전한 대안 보기"
    description: "T-Score ≥ 0.3인 대안들을 다시 보여드립니다."
    risk_level: low
    recommended: true
  - label: "방어 논리 먼저 보기"
    description: "이 선택에 대한 학술적 방어 논리를 먼저 제시합니다."
    risk_level: medium
    recommended: false

multiSelect: false
fallback: "더 안전한 대안 보기"
```

### CP-VS-003: Satisfaction Check

```yaml
id: CP-VS-003
type: ITERATION
phase: "VS Phase 5"

question:
  header: "만족도 확인"
  text: "결과에 만족하시나요?"

options:
  - label: "예, 완료합니다"
    description: "현재 결과로 진행합니다."
    recommended: true
  - label: "다시 탐색합니다"
    description: "Phase 2로 돌아가 다른 방향을 탐색합니다."
    recommended: false
  - label: "다른 접근을 시도합니다"
    description: "창의적 장치를 활용해 새로운 접근을 시도합니다."
    recommended: false

multiSelect: false
fallback: "예, 완료합니다"
```

---

## Creativity Module Checkpoints

### CP-FA-001: Forced Analogy Source Selection

```yaml
id: CP-FA-001
type: PREFERENCE
phase: "creativity/forced-analogy"

question:
  header: "유추 소스"
  text: "유추할 소스 분야를 선택해주세요."

options:
  - label: "무작위 선택 (권장)"
    description: "시스템이 무작위로 분야를 선택합니다. 최대 창의성."
    recommended: true
  - label: "자연과학 계열"
    description: "생태학, 물리학, 화학, 생물학에서 개념을 가져옵니다."
    recommended: false
  - label: "인문학 계열"
    description: "철학, 역사학, 언어학에서 개념을 가져옵니다."
    recommended: false
  - label: "직접 지정"
    description: "원하는 분야를 직접 입력합니다."
    recommended: false

multiSelect: false
fallback: "무작위 선택"
```

### CP-FA-002: Analogy Approval

```yaml
id: CP-FA-002
type: APPROVAL
phase: "creativity/forced-analogy"

question:
  header: "유추 승인"
  text: "이 유추가 적절해 보이나요?"
  context: |
    소스: [Source Field] - [Source Concept]
    타겟: [Target Research]
    매핑: [Proposed Mapping]

options:
  - label: "예, 적용합니다"
    description: "이 유추를 연구에 적용합니다."
    recommended: true
  - label: "다른 유추를 요청합니다"
    description: "새로운 유추를 생성합니다."
    recommended: false
  - label: "건너뛰기"
    description: "강제 유추 없이 진행합니다."
    recommended: false

multiSelect: false
fallback: "건너뛰기"
```

### CP-IL-001 to CP-IL-004: Iterative Loop Checkpoints

```yaml
# CP-IL-001: Round 1 Direction Selection
id: CP-IL-001
type: PREFERENCE
phase: "creativity/iterative-loop Round 1"
question:
  header: "관심 방향"
  text: "Wide Exploration 결과 중 관심 있는 방향을 선택해주세요."
multiSelect: true

# CP-IL-002: Round 2 Combination Approval
id: CP-IL-002
type: APPROVAL
phase: "creativity/iterative-loop Round 2"
question:
  header: "조합 승인"
  text: "다음 조합을 진행할까요?"

# CP-IL-003: Round 3 Guardrail Level
id: CP-IL-003
type: PREFERENCE
phase: "creativity/iterative-loop Round 3"
question:
  header: "가드레일 수준"
  text: "적용할 가드레일 수준을 선택해주세요."
options:
  - label: "엄격 (Strict)"
    description: "모든 학술적 기준 적용"
  - label: "균형 (Balanced) (권장)"
    description: "핵심 기준만 적용"
    recommended: true
  - label: "유연 (Flexible)"
    description: "최소 기준만 적용"

# CP-IL-004: Round 4 Final Selection
id: CP-IL-004
type: APPROVAL
phase: "creativity/iterative-loop Round 4"
question:
  header: "최종 선택"
  text: "최종 결과를 승인하시겠습니까?"
```

### CP-SD-001: Semantic Distance Threshold

```yaml
id: CP-SD-001
type: PREFERENCE
phase: "creativity/semantic-distance"

question:
  header: "거리 임계값"
  text: "의미적 거리 임계값을 선택해주세요."

options:
  - label: "가까운 조합 (distance > 0.3)"
    description: "안전한 조합, 낮은 위험"
    recommended: false
  - label: "중간 거리 (distance > 0.5) (권장)"
    description: "균형 잡힌 조합"
    recommended: true
  - label: "먼 조합 (distance > 0.7)"
    description: "혁신적 조합, 강한 정당화 필요"
    recommended: false
  - label: "최대 거리 (distance > 0.85)"
    description: "실험적 조합, 높은 위험"
    recommended: false

multiSelect: false
fallback: "중간 거리"
```

### CP-TR-001: Temporal Reframing Perspective

```yaml
id: CP-TR-001
type: PREFERENCE
phase: "creativity/temporal-reframing"

question:
  header: "시간 관점"
  text: "어떤 시간 관점을 적용할까요?"

options:
  - label: "과거 (1990s)"
    description: "당시 이 연구를 했다면? 역사적 맥락 이해."
    recommended: false
  - label: "미래 (2035)"
    description: "10년 후 이 연구를 본다면? 현재 한계 예측."
    recommended: false
  - label: "평행 우주"
    description: "이 분야가 다르게 발전했다면? 대안 체계 탐색."
    recommended: false
  - label: "전체 적용 (권장)"
    description: "세 관점 모두 분석합니다."
    recommended: true

multiSelect: false
fallback: "전체 적용"
```

### CP-CS-001: Community Simulation Persona Selection

```yaml
id: CP-CS-001
type: PREFERENCE
phase: "creativity/community-simulation"

question:
  header: "페르소나 선택"
  text: "피드백 받을 가상 연구자를 선택해주세요."

options:
  - label: "전체 (7명 모두)"
    description: "모든 페르소나의 피드백을 받습니다."
    recommended: false
  - label: "핵심 3명 (권장)"
    description: "보수적/혁신적/학제간 연구자 피드백."
    recommended: true
  - label: "직접 선택"
    description: "원하는 페르소나를 직접 선택합니다."
    recommended: false

multiSelect: true  # For "직접 선택" case
fallback: "핵심 3명"
```

### CP-CS-002: Feedback Incorporation

```yaml
id: CP-CS-002
type: APPROVAL
phase: "creativity/community-simulation"

question:
  header: "피드백 반영"
  text: "어떤 피드백을 반영할까요?"
  context: "[각 페르소나 피드백 표시]"

options:
  # Dynamically generated based on feedback
  - label: "[페르소나 이름]: [피드백 요약]"
    description: "[상세 피드백]"

multiSelect: true
fallback: "모든 피드백 반영"
```

---

## Agent-Specific Checkpoints

### CP-AG-001: Ethics Confirmation (Agent 04)

```yaml
id: CP-AG-001
type: GUARDRAIL
phase: "Agent 04 - Research Ethics Advisor"

question:
  header: "윤리 확인"
  text: "다음 윤리적 고려사항을 확인하셨습니까?"
  context: "[식별된 윤리적 이슈 목록]"

options:
  - label: "예, 확인했습니다"
    description: "모든 윤리적 고려사항을 인지하고 대응 계획이 있습니다."
    recommended: true
  - label: "추가 가이드 필요"
    description: "윤리적 대응 방안에 대한 상세 가이드를 요청합니다."
    recommended: false

multiSelect: false
fallback: "추가 가이드 필요"
```

### CP-AG-002: Critique Acceptance (Agent 03)

```yaml
id: CP-AG-002
type: APPROVAL
phase: "Agent 03 - Devil's Advocate"

question:
  header: "비판 수용"
  text: "다음 비판 중 어떤 것을 수용/반영하시겠습니까?"
  context: "[비판 목록]"

options:
  # Dynamically generated based on critiques

multiSelect: true
fallback: "모든 비판 검토 후 선택적 반영"
```

### CP-AG-003: Bias Acknowledgment (Agent 16)

```yaml
id: CP-AG-003
type: GUARDRAIL
phase: "Agent 16 - Bias Detector"

question:
  header: "편향 인지"
  text: "다음 잠재적 편향을 인지하셨습니까?"
  context: "[식별된 편향 목록]"

options:
  - label: "예, 인지하고 대응 계획이 있습니다"
    description: "각 편향에 대한 완화 전략이 준비되어 있습니다."
    recommended: true
  - label: "완화 전략 가이드 필요"
    description: "각 편향에 대한 구체적 완화 전략을 요청합니다."
    recommended: false

multiSelect: false
fallback: "완화 전략 가이드 필요"
```

---

## End Checkpoint

### CP-END-001: Overall Satisfaction

```yaml
id: CP-END-001
type: ITERATION
phase: "research completion"

question:
  header: "최종 확인"
  text: "전체 결과에 만족하시나요?"

options:
  - label: "예, 완료합니다"
    description: "연구 설계/분석을 완료합니다."
    recommended: true
  - label: "특정 단계 재실행"
    description: "특정 에이전트나 단계를 다시 실행합니다."
    recommended: false
  - label: "전체 재시작"
    description: "처음부터 다시 시작합니다."
    recommended: false

multiSelect: false
fallback: "예, 완료합니다"
```

---

## Implementation Notes

### AskUserQuestion Integration

Each checkpoint translates to an AskUserQuestion call:

```markdown
**AskUserQuestion 호출**:
- header: "{checkpoint.question.header}"
- question: "{checkpoint.question.text}"
- options: [
    {
      label: "{option.label}",
      description: "{option.description}"
    },
    ...
  ]
- multiSelect: {checkpoint.multiSelect}
```

### Checkpoint Flow Control

```python
def process_checkpoint(checkpoint_id, context):
    """
    Process a user checkpoint and return user's selection.
    """
    checkpoint = get_checkpoint(checkpoint_id)

    # Build AskUserQuestion parameters
    question_params = {
        "header": checkpoint.question.header,
        "text": checkpoint.question.text,
        "options": checkpoint.options,
        "multiSelect": checkpoint.multiSelect
    }

    # If context is provided, add it
    if checkpoint.question.context:
        question_params["context"] = checkpoint.question.context

    # Call AskUserQuestion
    response = ask_user_question(**question_params)

    # Handle response
    if response is None:
        return checkpoint.fallback

    return response
```

### Checkpoint Registry

All checkpoints are registered in the system for quick lookup:

```python
CHECKPOINT_REGISTRY = {
    # Initialization
    "CP-INIT-001": "Research Type Selection",
    "CP-INIT-002": "Creativity Level Selection",
    "CP-INIT-003": "T-Score Mode Selection",

    # VS Engine
    "CP-VS-001": "Direction Selection",
    "CP-VS-002": "Low-Typicality Risk Warning",
    "CP-VS-003": "Satisfaction Check",

    # Creativity Modules
    "CP-FA-001": "Forced Analogy Source Selection",
    "CP-FA-002": "Analogy Approval",
    "CP-IL-001": "Iterative Loop Round 1",
    "CP-IL-002": "Iterative Loop Round 2",
    "CP-IL-003": "Iterative Loop Round 3",
    "CP-IL-004": "Iterative Loop Round 4",
    "CP-SD-001": "Semantic Distance Threshold",
    "CP-TR-001": "Temporal Reframing Perspective",
    "CP-CS-001": "Community Simulation Persona",
    "CP-CS-002": "Feedback Incorporation",

    # Agent-Specific
    "CP-AG-001": "Ethics Confirmation",
    "CP-AG-002": "Critique Acceptance",
    "CP-AG-003": "Bias Acknowledgment",

    # End
    "CP-END-001": "Overall Satisfaction"
}
```

### Type-Based Behavior

Each checkpoint type has specific behavior patterns:

```python
CHECKPOINT_BEHAVIORS = {
    "PREFERENCE": {
        "icon": "🔵",
        "blocking": False,
        "can_skip": True,
        "requires_reason": False
    },
    "APPROVAL": {
        "icon": "🟡",
        "blocking": True,
        "can_skip": False,
        "requires_reason": False
    },
    "GUARDRAIL": {
        "icon": "🔴",
        "blocking": True,
        "can_skip": False,
        "requires_reason": True  # User must acknowledge risk
    },
    "ITERATION": {
        "icon": "🟢",
        "blocking": False,
        "can_skip": True,
        "requires_reason": False
    }
}
```

### Conditional Checkpoint Triggering

Some checkpoints are only triggered under certain conditions:

```python
CONDITIONAL_TRIGGERS = {
    "CP-VS-002": {
        "condition": "selected_option.t_score < 0.3",
        "description": "Only trigger when low T-Score option selected"
    },
    "CP-AG-001": {
        "condition": "research_involves_human_subjects == True",
        "description": "Only trigger for human subjects research"
    },
    "CP-AG-003": {
        "condition": "bias_detector_findings.count > 0",
        "description": "Only trigger when biases are detected"
    }
}
```

---

## Checkpoint Sequences

### Standard Research Flow

```
CP-INIT-001 → CP-INIT-002 → CP-INIT-003
                    ↓
              CP-VS-001 → [CP-VS-002] → CP-VS-003
                    ↓
         [Creativity Checkpoints as needed]
                    ↓
         [Agent Checkpoints as needed]
                    ↓
              CP-END-001
```

### Meta-Analysis Flow

```
CP-INIT-001 (메타분석 선택) → CP-INIT-002 → CP-INIT-003
                    ↓
          CP-VS-001 (효과크기 방향)
                    ↓
          CP-AG-003 (출판편향 체크)
                    ↓
              CP-END-001
```

### High-Creativity Flow

```
CP-INIT-002 (Extreme 선택) → CP-VS-002 (위험 경고)
                    ↓
        CP-FA-001 → CP-FA-002 (강제 유추)
                    ↓
        CP-SD-001 (먼 거리 조합)
                    ↓
        CP-CS-001 → CP-CS-002 (커뮤니티 검증)
                    ↓
              CP-END-001
```

---

## Localization Support

All checkpoints support bilingual display (Korean/English):

```yaml
localization:
  ko:
    CP-INIT-001:
      header: "연구 유형"
      text: "이 연구의 유형을 선택해주세요."
  en:
    CP-INIT-001:
      header: "Research Type"
      text: "Please select the type of your research."
```

---

---

## Meta-Analysis Extraction Checkpoints (V7)

### CP_SOURCE_VERIFY: Source Verification

```yaml
id: CP_SOURCE_VERIFY
type: GUARDRAIL
phase: "Gate 1 - Extraction Validation"

question:
  header: "Source Verify"
  text: "Verify extracted values match original paper source."
  context: |
    Extracted data:
    - Study: [study_name]
    - n1: [value], n2: [value]
    - M1: [value], M2: [value]
    - SD1: [value], SD2: [value]
    - Source: Page [X], Table [Y]

options:
  - label: "Verified - values match source"
    description: "All extracted values confirmed against original paper."
    recommended: true
  - label: "Correction needed"
    description: "Values need correction. Specify corrections below."
    recommended: false
  - label: "Unable to verify - original unclear"
    description: "Original source is ambiguous. Flag for sensitivity analysis."
    recommended: false

multiSelect: false
fallback: "Flag for manual review"
```

### CP_ES_HIERARCHY: Effect Size Selection

```yaml
id: CP_ES_HIERARCHY
type: GUARDRAIL
phase: "Gate 2 - Classification Validation"

question:
  header: "ES Selection"
  text: "Multiple effect sizes detected. Select based on hierarchy."
  context: |
    Study: [study_name]

    Multiple effect sizes detected:
    ┌─────────┬─────────────────┬───────────┬──────────────┐
    │ ES_ID   │ Comparison      │ Timepoint │ Priority     │
    │ ES_01   │ AI vs Control   │ Post-test │ ⭐ Priority 1 │
    │ ES_02   │ Pre vs Post     │ Change    │ Priority 3   │
    │ ES_03   │ Baseline        │ Pre-test  │ ⛔ EXCLUDED  │
    └─────────┴─────────────────┴───────────┴──────────────┘

    Recommendation: Select ES_01 (highest priority)

options:
  - label: "Accept recommendation"
    description: "Use highest priority ES as recommended."
    recommended: true
  - label: "Select different ES"
    description: "Specify which ES to use with rationale."
    recommended: false
  - label: "Include multiple (specify handling)"
    description: "Include multiple ES with clustering/averaging strategy."
    recommended: false

multiSelect: false
fallback: "Accept recommendation"

required_fields:
  - selected_es_id
  - selection_rationale
  - excluded_es_handling  # document | sensitivity | none
```

### CP_PRETEST_REJECT: Pre-test Exclusion Alert

```yaml
id: CP_PRETEST_REJECT
type: GUARDRAIL
phase: "Gate 4 - Independence Validation"

question:
  header: "Pre-test Alert"
  text: "AUTOMATIC REJECTION: Pre-test detected as potential outcome."
  context: |
    ⛔ AUTOMATIC REJECTION

    Effect size [es_id] appears to be a pre-test measurement.

    Detected pattern: "[pattern]"

    Pre-test scores represent baseline equivalence, NOT treatment effects.
    They MUST NOT be included as independent outcomes.

    Action: EXCLUDED from analysis
    Rationale: V7 Protocol - Pre-test Independence Rule

options:
  - label: "Acknowledge - Exclude pre-test"
    description: "Confirm exclusion of pre-test from analysis."
    recommended: true
  - label: "Override (requires strong justification)"
    description: "Override exclusion with documented rationale. Use with extreme caution."
    risk_level: high
    recommended: false

multiSelect: false
fallback: "Acknowledge - Exclude pre-test"
```

### CP_EXTREME_VALUE: Outlier Review

```yaml
id: CP_EXTREME_VALUE
type: GUARDRAIL
phase: "Gate 3 - Statistical Validation"

question:
  header: "Outlier Review"
  text: "Extreme effect size detected. Review required."
  context: |
    Study: [study_name]
    Calculated g: [value]

    ⚠️ This effect size is unusually large (|g| > 2.0).

    Possible explanations:
    1. Genuine large effect (rare but possible)
    2. Calculation error
    3. Reporting error in original study
    4. Small sample inflation

options:
  - label: "Include - verified as correct"
    description: "Effect size verified, include in analysis with note."
    recommended: false
  - label: "Include - flag for sensitivity analysis"
    description: "Include but run sensitivity analysis without this study."
    recommended: true
  - label: "Exclude - suspected error"
    description: "Exclude from main analysis due to suspected error."
    recommended: false
  - label: "Recalculate - need verification"
    description: "Return to extraction for recalculation."
    recommended: false

multiSelect: false
fallback: "Include - flag for sensitivity analysis"
```

### CP_DEPENDENCY_HANDLING: Multiple ES Handling

```yaml
id: CP_DEPENDENCY_HANDLING
type: APPROVAL
phase: "Gate 4 - Independence Validation"

question:
  header: "Dependency"
  text: "Multiple effect sizes from same study. Specify handling."
  context: |
    Study: [study_name]

    Multiple ES from same participants detected:
    - ES_01: [description] (g = X.XX)
    - ES_02: [description] (g = X.XX)
    - ES_03: [description] (g = X.XX)

    Independence violation if included separately.

options:
  - label: "Average (same construct)"
    description: "Average ES if measuring same construct."
    recommended: false
  - label: "Select primary outcome"
    description: "Use only the primary/most relevant outcome."
    recommended: false
  - label: "3-level model (different constructs)"
    description: "Include all with robust variance estimation."
    recommended: true
  - label: "Sensitivity analysis"
    description: "Run separate analyses for each outcome."
    recommended: false

multiSelect: false
fallback: "Select primary outcome"
```

---

## Checkpoint Registry Update

```python
CHECKPOINT_REGISTRY.update({
    # Meta-Analysis Extraction (V7)
    "CP_SOURCE_VERIFY": "Source Verification",
    "CP_ES_HIERARCHY": "Effect Size Selection",
    "CP_PRETEST_REJECT": "Pre-test Exclusion Alert",
    "CP_EXTREME_VALUE": "Outlier Review",
    "CP_DEPENDENCY_HANDLING": "Multiple ES Handling",
})
```

---

## Meta-Analysis Checkpoint Sequence

```
Gate 1: Extraction
├─ CP_SOURCE_VERIFY (REQUIRED for each study)
│
Gate 2: Classification
├─ CP_ES_HIERARCHY (REQUIRED when >1 ES available)
│
Gate 3: Statistical
├─ CP_EXTREME_VALUE (CONDITIONAL when |g| > 2.0)
│
Gate 4: Independence
├─ CP_PRETEST_REJECT (AUTO-TRIGGER when pre-test detected)
└─ CP_DEPENDENCY_HANDLING (REQUIRED when >1 ES from same study)
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 3.0.0 | 2025-01 | Initial comprehensive checkpoint system |
| - | - | Added 4 checkpoint types |
| - | - | Integrated AskUserQuestion pattern |
| - | - | Added conditional triggering |
| - | - | Added checkpoint sequences |
| 3.1.0 | 2026-01 | V7 Meta-Analysis Checkpoints |
| - | - | Added CP_SOURCE_VERIFY |
| - | - | Added CP_ES_HIERARCHY |
| - | - | Added CP_PRETEST_REJECT |
| - | - | Added CP_EXTREME_VALUE |
| - | - | Added CP_DEPENDENCY_HANDLING |
