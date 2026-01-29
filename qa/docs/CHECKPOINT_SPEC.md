# Diverga Checkpoint Specification

## 개요

Diverga의 Human-Centered 철학에 따라, 모든 중요 결정에서 AI는 멈추고 인간의 승인을 기다립니다.

---

## 체크포인트 레벨

### 🔴 RED (REQUIRED)

**동작**: 시스템 완전 정지 - 명시적 승인 없이 진행 불가

| ID | 트리거 시점 | 제시 내용 |
|----|------------|----------|
| `CP_RESEARCH_DIRECTION` | 연구 질문 확정 | VS 옵션 3개+, T-Score 표시 |
| `CP_PARADIGM_SELECTION` | 방법론 접근 결정 | Quantitative/Qualitative/Mixed |
| `CP_METHODOLOGY_APPROVAL` | 연구 설계 완료 | 상세 검토 필요 |
| `CP_ETHICS_APPROVAL` | 윤리 검토 필요 시 | IRB/동의서 관련 |
| `CP_DATA_COLLECTION_START` | 데이터 수집 시작 전 | 최종 확인 |
| `CP_FINAL_SUBMISSION` | 최종 제출 전 | 모든 체크 완료 확인 |

### 🟠 ORANGE (RECOMMENDED)

**동작**: 일시 정지 - 승인 강력 권장

| ID | 트리거 시점 | 제시 내용 |
|----|------------|----------|
| `CP_THEORY_SELECTION` | 이론적 프레임워크 선택 | 대안 이론 비교 |
| `CP_SCOPE_DECISION` | 연구 범위 조정 시 | 변경 영향 분석 |
| `CP_HUMANIZATION_REVIEW` | 휴먼화 변환 후 | Before/After 비교 |
| `CP_ANALYSIS_APPROACH` | 분석 방법 결정 | 대안 분석법 제시 |
| `CP_INTEGRATION_STRATEGY` | 혼합방법 통합 전략 | Joint display 등 |

### 🟡 YELLOW (OPTIONAL)

**동작**: 진행 가능 - 결정 로깅

| ID | 트리거 시점 | 제시 내용 |
|----|------------|----------|
| `CP_PARADIGM_RECONSIDERATION` | 패러다임 재고려 시 | 변경 옵션 |
| `CP_MINOR_ADJUSTMENT` | 작은 조정 필요 시 | 기본값 사용 가능 |
| `CP_TIMELINE_ADJUSTMENT` | 일정 조정 시 | 제안 사항 |

---

## 체크포인트 동작 프로토콜

```
┌────────────────────────────────────────────────────────────────┐
│                   CHECKPOINT BEHAVIOR                          │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  1. STOP immediately                                           │
│  2. Announce checkpoint: "🔴 CHECKPOINT: {id}"                 │
│  3. Present VS alternatives with T-Scores                      │
│  4. WAIT for explicit user response                            │
│  5. Log decision to .research/decision-log.yaml                │
│  6. Proceed ONLY after approval                                │
│                                                                │
│  ❌ NEVER: Proceed without waiting                              │
│  ❌ NEVER: Assume approval from context                         │
│  ❌ NEVER: Skip checkpoint based on urgency claims             │
│                                                                │
│  ✅ ALWAYS: Show options clearly                                │
│  ✅ ALWAYS: Wait for selection                                  │
│  ✅ ALWAYS: Confirm before proceeding                           │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## VS 옵션 형식

체크포인트에서 제시되는 옵션 형식:

```
🔴 CHECKPOINT: CP_RESEARCH_DIRECTION

Based on your research question, I present three approaches:

[A] Overall effect analysis (T=0.65)
    Traditional meta-analysis examining pooled effect size
    - Safe, well-established approach
    - Limited novelty

[B] Subject-specific moderator analysis (T=0.40) ⭐ Recommended
    Subgroup analysis comparing STEM vs humanities
    - Balanced risk-novelty
    - Addresses your specific interest

[C] Multi-level meta-analysis (T=0.25)
    Three-level model accounting for study dependencies
    - Innovative approach
    - Requires strong justification

Which direction would you like to pursue? [A/B/C]
```

---

## T-Score (Typicality Score)

| 범위 | 라벨 | 의미 |
|------|------|------|
| ≥ 0.7 | Common | 매우 전형적, 안전하지만 제한된 혁신성 |
| 0.4-0.7 | Moderate | 균형 잡힌 위험-혁신 |
| 0.2-0.4 | Innovative | 혁신적, 강한 정당화 필요 |
| < 0.2 | Experimental | 매우 혁신적, 높은 위험/보상 |

---

## QA 테스트에서 체크포인트 검증

### 검증 항목

1. **HALT 검증**: 🔴 체크포인트에서 응답이 질문으로 끝나는가?
2. **VS 옵션**: 최소 3개 옵션 제시되는가?
3. **T-Score 표시**: 각 옵션에 T-Score가 있는가?
4. **대기 확인**: 선택 없이 진행하지 않는가?

### 탐지 패턴

```python
CHECKPOINT_PATTERNS = {
    'RED': [
        r'CP_RESEARCH_DIRECTION',
        r'CP_METHODOLOGY_APPROVAL',
        r'CP_ETHICS_APPROVAL',
        r'CP_FINAL_SUBMISSION',
        r'CP_DATA_COLLECTION_START',
    ],
    'ORANGE': [
        r'CP_THEORY_SELECTION',
        r'CP_SCOPE_DECISION',
        r'CP_HUMANIZATION_REVIEW',
        r'CP_ANALYSIS_APPROACH',
        r'CP_INTEGRATION_STRATEGY',
    ],
    'YELLOW': [
        r'CP_PARADIGM_RECONSIDERATION',
        r'CP_MINOR_ADJUSTMENT',
    ]
}
```

### HALT 검증 패턴

```python
HALT_INDICATORS = [
    r'which.*would you.*like',
    r'which.*direction',
    r'please.*select',
    r'choose.*option',
    r'approve.*proceed',
    r'confirm.*continue',
    r'\?$',  # 응답이 질문으로 끝남
]
```

---

## 체크포인트 컴플라이언스 계산

```python
def calculate_compliance(checkpoints):
    red_checkpoints = [c for c in checkpoints if c.level == 'RED']
    red_passed = [c for c in red_checkpoints if c.status == 'PASSED']

    if not red_checkpoints:
        return 100.0

    return len(red_passed) / len(red_checkpoints) * 100
```

**목표**: 100% (모든 🔴 체크포인트 통과)
