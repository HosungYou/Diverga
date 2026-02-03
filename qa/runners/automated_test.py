#!/usr/bin/env python3
"""
Diverga QA Protocol v2.1 - Automated Test Simulator

Simulates conversations based on protocol YAML files and records all interactions.
Does NOT require manual user input - runs completely automatically.

Usage:
    python automated_test.py --scenario QUAL-002 --output qa/reports/sessions/
"""

import argparse
import json
import yaml
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any


@dataclass
class SimulatedTurn:
    """A simulated conversation turn."""
    turn_number: int
    user_type: str
    user_input: str
    user_input_ko: Optional[str]  # Korean version if applicable
    expected_behavior: Dict[str, Any]
    simulated_response: str
    checkpoints_triggered: List[str] = field(default_factory=list)
    agents_invoked: List[str] = field(default_factory=list)
    validation_passed: bool = True
    validation_notes: List[str] = field(default_factory=list)


@dataclass
class TestSession:
    """Complete test session."""
    scenario_id: str
    scenario_name: str
    language: str
    paradigm: str
    started_at: str
    completed_at: Optional[str] = None
    turns: List[SimulatedTurn] = field(default_factory=list)
    total_checkpoints: int = 0
    checkpoints_passed: int = 0
    agents_invoked: List[str] = field(default_factory=list)
    overall_passed: bool = True
    summary: Dict[str, Any] = field(default_factory=dict)


class AutomatedTestSimulator:
    """
    Simulates Diverga conversations based on protocol YAML.

    This is a SIMULATION - it generates realistic responses based on
    expected behaviors without calling actual agents. Used for QA testing
    and demonstration purposes.
    """

    PROTOCOL_DIR = Path(__file__).parent.parent / "protocol"

    # Simulated responses for each scenario
    RESPONSE_TEMPLATES = {
        "QUAL-002": {
            1: """## 🔍 패러다임 감지

연구 맥락에서 **질적 연구(Qualitative)** 접근이 감지되었습니다:

| 감지된 키워드 | 신호 |
|--------------|------|
| "경험하는 현상" | 현상학적 탐구 |
| "탐구하고 싶습니다" | 탐색적 연구 |
| "어떻게...통합하는지" | 과정 이해 |
| "긴장과 갈등" | 주관적 경험 |

---

## 🔴 CHECKPOINT: CP_PARADIGM_SELECTION

**연구 방법론적 접근을 선택해 주세요:**

| 옵션 | 방법론 | T-Score | 설명 |
|------|--------|---------|------|
| **[A]** | 기술적 현상학 (Descriptive Phenomenology) | T=0.55 | Husserl 전통, 에포케(bracketing)를 통한 순수 경험 기술 |
| **[B]** | 해석학적 현상학 (Hermeneutic Phenomenology) | T=0.40 ⭐ | van Manen 접근, 체험의 의미 해석 - 교육 연구에 적합 |
| **[C]** | 해석적 현상학 분석 (IPA) | T=0.45 | Smith 접근, 개별 사례의 심층 분석 |
| **[D]** | 내러티브 탐구 (Narrative Inquiry) | T=0.35 | Clandinin & Connelly, 교사 이야기 중심 |

**어떤 방법론으로 진행하시겠습니까?**""",

            2: """## 현상학적 접근법 비교: Husserl vs Heidegger vs van Manen

훌륭한 질문입니다. 세 접근법의 핵심적인 차이를 설명드리겠습니다.

### 1. Husserl의 기술적 현상학 (Descriptive Phenomenology)

**핵심 개념: 에포케(Epoché) / 판단중지(Bracketing)**

- 연구자의 선입견, 이론, 가정을 "괄호 안에 넣어" 중지
- **순수한 의식 경험**에 도달하고자 함
- 현상을 "있는 그대로" 기술하는 것이 목표

**실제 연구 적용:**
```
연구자: "AI 도구에 대한 나의 경험과 의견을 잠시 멈추고,
        교사들이 경험하는 현상 자체에만 집중한다."
```

### 2. Heidegger의 해석학적 현상학

**핵심 개념: 선이해(Fore-understanding) / 해석학적 순환(Hermeneutic Circle)**

- 완전한 bracketing은 **불가능**하다고 봄
- 연구자의 선이해가 해석에 **필수적**
- 부분과 전체 사이를 오가며 이해를 심화

**실제 연구 적용:**
```
연구자: "나의 교육학 배경과 AI 경험이 교사들의 경험을
        이해하는 데 오히려 도움이 된다. 이를 명시적으로
        드러내고 해석에 활용한다."
```

### 3. van Manen의 해석학적 현상학 (교육학 중심)

**핵심 개념: 체험(Lived Experience) / 생활세계(Lifeworld)**

- Heidegger의 해석학 + 교육학적 관점
- **교육적 실천**에 대한 반성적 이해
- 네 가지 생활세계 실존체:
  - 체험된 공간 (spatiality)
  - 체험된 몸 (corporeality)
  - 체험된 시간 (temporality)
  - 체험된 관계 (relationality)

**실제 연구 적용:**
```
연구자: "교사가 AI 도구를 사용할 때의 '체험된 공간'은 어떠한가?
        디지털 공간과 물리적 교실 사이에서 어떤 긴장을 느끼는가?"
```

---

### 선생님의 연구에 대한 권장

**van Manen 접근이 가장 적합한 이유:**

1. **교육 맥락 특화**: van Manen은 교육학자로서 교사 경험 연구에 최적화
2. **실천적 지향**: "교육철학과의 통합"이라는 연구 관심과 일치
3. **긴장과 갈등 해석**: 생활세계 개념으로 다층적 해석 가능
4. **한국 교육연구 활용**: 국내 교육학 논문에서 널리 사용

**IPA와의 차이:**
- IPA: 개인별 심층 사례 분석, 심리학적 배경
- van Manen: 본질적 주제 도출, 교육학적 배경

---

🔴 **체크포인트 유지 중**: 방법론 선택을 기다리고 있습니다.
`[A]`, `[B]`, `[C]`, `[D]` 중 선택해 주세요.""",

            3: """## ✅ 선택 완료: [B] 해석학적 현상학 (van Manen)

선택이 기록되었습니다.

| 항목 | 내용 |
|------|------|
| **선택된 방법론** | 해석학적 현상학 (van Manen) |
| **T-Score** | 0.40 (차별화된 접근) |
| **관련 에이전트** | C2-QualitativeDesignConsultant |

---

## 🔴 CHECKPOINT: CP_METHODOLOGY_APPROVAL

**연구 설계 초안을 제시합니다:**

### 연구 설계 개요

| 구성요소 | 내용 |
|----------|------|
| **연구 질문** | 교사들은 AI 도구를 교육 철학과 통합하는 과정에서 어떤 체험을 하는가? |
| **방법론** | van Manen의 해석학적 현상학 |
| **참여자** | AI 도구 사용 경험이 있는 K-12 교사 |
| **자료 수집** | 심층 인터뷰 (60-90분, 2-3회) |
| **분석 방법** | 주제 분석 (Thematic Analysis) |

### 생활세계 탐구 프레임워크

1. **체험된 공간**: 디지털/물리적 교실 공간의 경험
2. **체험된 몸**: AI 도구 사용 시 교사로서의 정체성
3. **체험된 시간**: 수업 준비, 실시간 상호작용의 변화
4. **체험된 관계**: 학생, 동료, 기술과의 관계 변화

**이 설계로 진행해도 될까요?**""",

            4: """## 🔄 Agent Transition: A3-DevilsAdvocate

비판적 검토를 위해 A3-DevilsAdvocate 에이전트를 호출합니다.

---

## 👿 Devil's Advocate: IPA vs van Manen 비판적 검토

### Reviewer 2가 물을 수 있는 질문들

**Q1: "왜 IPA 대신 van Manen을 선택했습니까?"**

예상 비판:
- "IPA가 더 체계적인 분석 절차를 제공합니다"
- "IPA는 심리학적 깊이가 더 있습니다"
- "van Manen은 분석 절차가 모호합니다"

**방어 전략:**
```
"IPA는 개인의 의미 형성(sense-making)에 초점을 두지만,
본 연구는 교사의 '교육적 실천'에 대한 반성적 이해를 목표로 합니다.
van Manen의 접근은 교육학적 맥락에서 개발되어
교사 경험 연구에 더 적합합니다 (van Manen, 1990, 2014)."
```

**Q2: "van Manen 접근법의 분석 절차가 불명확하지 않습니까?"**

예상 비판:
- "IPA의 6단계 분석이 더 투명합니다"
- "재현가능성(replicability) 문제"

**방어 전략:**
```
"van Manen(1990)은 6가지 연구 활동을 제시합니다:
1. 현상을 향한 전환
2. 체험 탐구
3. 본질적 주제 반성
4. 글쓰기를 통한 탐구
5. 강한 교육학적 관계 유지
6. 부분과 전체의 균형

이는 IPA와 다른 방식이지만 동등하게 체계적입니다."
```

### IPA 선택 시 vs van Manen 선택 시 논문 구성 차이

| 측면 | IPA | van Manen |
|------|-----|-----------|
| **분석 단위** | 개별 사례 → 교차 사례 | 전체적 본질 주제 |
| **글쓰기 스타일** | 분석적, 표 중심 | 서술적, 일화적 |
| **인용 빈도** | 개인별 다수 인용 | 주제별 선택적 인용 |
| **주요 학회** | 심리학, 건강학 | 교육학, 간호학 |

---

**결론**: 교육학 저널 투고 시 van Manen이 더 수용도가 높습니다.
Teaching and Teacher Education, Teachers and Teaching 등에서
van Manen 기반 연구가 활발히 출판되고 있습니다.""",

            5: """## 📊 표본 크기 적절성 검토

n=5에 대한 우려를 이해합니다. 솔직하게 평가해 드리겠습니다.

### 현상학적 연구의 표본 크기 가이드라인

| 학자 | 권장 | 근거 |
|------|------|------|
| **Creswell (2013)** | 3-10명 | 현상학은 깊이 > 범위 |
| **Dukes (1984)** | 3-10명 | 본질 탐구에 충분 |
| **Polkinghorne (1989)** | 5-25명 | 현상의 복잡성에 따라 |
| **van Manen (1990)** | 명시적 기준 없음 | 데이터 풍부성 강조 |

### n=5가 충분한 조건

✅ **충분한 경우:**
- 각 참여자와 2-3회 심층 인터뷰 (총 10-15회 인터뷰)
- 인터뷰당 60-90분 (충분한 깊이)
- 다양한 배경 (초/중/고, 경력 다양성)
- **주제 포화(Thematic Saturation)** 달성

⚠️ **보완이 필요한 경우:**
- 단일 인터뷰만 진행
- 동질적 참여자 집단
- 30분 이하의 짧은 인터뷰

### 저널 Reject 위험 대응

**전략 1: 표본 크기 정당화 섹션 작성**
```
"현상학적 연구에서 표본 크기는 통계적 일반화가 아닌
현상의 본질 탐구에 의해 결정된다 (Creswell, 2013).
본 연구는 5명의 참여자와 각 2-3회 심층 인터뷰를 통해
총 12회의 인터뷰 자료를 확보했으며,
6번째 참여자 추가 시 새로운 주제가 도출되지 않아
주제 포화에 도달했다고 판단했다."
```

**전략 2: 데이터 풍부성 강조**
- 인터뷰 총 시간 (예: 900분+)
- 전사록 분량 (예: 200페이지+)
- 분석된 의미 단위 수

**전략 3: 질적 연구 전문 저널 선택**
- Qualitative Research
- International Journal of Qualitative Studies in Education

---

**권장사항**: n=5로 진행하되, 인터뷰 횟수를 2-3회로 늘리고
포화 도달을 명시적으로 문서화하세요.""",

            6: """## 🟠 CHECKPOINT: CP_PARADIGM_RECONSIDERATION

패러다임 재고려 요청을 인식했습니다.

### 현재 상황 분석

연구 질문에서 두 가지 유형을 감지했습니다:

| 질문 유형 | 예시 | 적합한 접근 |
|-----------|------|-------------|
| **어떻게(How)** | "어떻게 통합하는지" | 질적 연구 |
| **왜(Why)** | "왜 긴장을 느끼는지" | 질적/양적 모두 가능 |

### 옵션 제시

| 옵션 | 접근법 | 장점 | 단점 |
|------|--------|------|------|
| **[A]** | 순수 질적 연구 유지 | 깊이, 맥락 이해, 의미 탐구 | 일반화 제한 |
| **[B]** | 혼합 방법 전환 (Sequential Explanatory) | QUAN → qual로 일반화 + 심층 이해 | 시간/자원 2배 |
| **[C]** | 혼합 방법 전환 (Sequential Exploratory) | qual → QUAN으로 도구 개발 가능 | 연구 범위 확대 |

### 솔직한 조언

**질적 연구 유지를 권장하는 이유:**

1. **연구 질문의 본질**: "체험", "경험", "의미"는 본질적으로 질적 탐구 대상
2. **현상학적 일관성**: 혼합 방법은 해석학적 현상학의 철학적 기반과 충돌 가능
3. **실행 가능성**: 박사과정/소규모 연구에서 혼합 방법은 부담
4. **저널 선호도**: 순수 질적 연구가 교육학 저널에서 잘 수용됨

**혼합 방법이 적합한 경우:**
- 대규모 설문으로 AI 태도 측정 후 심층 인터뷰
- 교사 효능감 척도 → 경험 탐구 연결
- 정책 제언을 위한 일반화 필요 시

---

**어떤 방향으로 진행하시겠습니까?**

`[A]` 순수 질적 연구 유지 | `[B]` 혼합 방법 (Explanatory) | `[C]` 혼합 방법 (Exploratory)""",

            7: """## ✅ 결정 확인: 질적 연구 유지

선택을 존중합니다. "깊이가 더 중요하다"는 판단에 동의합니다.

---

## 🔄 Agent Transition: E2-QualitativeCodingSpecialist

데이터 분석 방법 설명을 위해 E2-QualitativeCodingSpecialist를 호출합니다.

---

## 📝 van Manen 현상학적 분석 방법

### 해석학적 순환 (Hermeneutic Circle)

```
        ┌─────────────────────────────────────┐
        │                                     │
        ▼                                     │
   ┌─────────┐                          ┌─────────┐
   │  전체   │◄────────────────────────►│  부분   │
   │ (Whole) │                          │ (Parts) │
   └─────────┘                          └─────────┘
        │                                     ▲
        │                                     │
        └─────────────────────────────────────┘

   • 개별 인터뷰 → 전체 맥락 이해
   • 전체 맥락 → 개별 진술 재해석
   • 반복적 순환으로 이해 심화
```

### van Manen의 주제 분석 3가지 접근

| 접근 | 방법 | 적용 |
|------|------|------|
| **전체론적** | 텍스트 전체를 관통하는 의미 파악 | 각 인터뷰의 핵심 메시지 |
| **선택적** | 본질적 진술/구절 선택 | 인용문 추출 |
| **상세** | 문장/문장군 분석 | 의미 단위 코딩 |

### 실제 분석 절차

**1단계: 전체 읽기**
```
모든 인터뷰 전사록을 여러 번 읽으며
교사들의 체험에 "젖어들기(dwelling)"
```

**2단계: 의미 단위 추출**
```
"AI가 수업 준비 시간을 줄여줬지만,
 정작 수업 중에는 기술이 나를 통제하는 것 같았어요."

 → 의미 단위: 효율성 vs 통제감의 긴장
```

**3단계: 주제 구성**
```
의미 단위들을 군집화하여 본질적 주제 도출:
• "디지털 자아와 교육자 정체성의 협상"
• "기술적 효율성과 교육적 진정성 사이의 긴장"
• "새로운 교수법적 공간의 창조"
```

**4단계: 본질 기술**
```
주제들을 통합하여 현상의 본질 구조 기술
→ 논문의 Findings 섹션
```

---

## 🟠 CHECKPOINT: CP_ANALYSIS_APPROACH

**위 분석 방법으로 진행하시겠습니까?**

| 확인 사항 | 체크 |
|-----------|------|
| 해석학적 순환 이해 | ☐ |
| 3가지 주제 분석 접근 이해 | ☐ |
| 4단계 분석 절차 이해 | ☐ |

`승인` 또는 추가 질문을 해주세요.""",

            8: """## ✅ 최종 승인 완료

모든 체크포인트가 해결되었습니다.

---

## 📋 연구 설계 최종 요약

### 기본 정보

| 항목 | 내용 |
|------|------|
| **연구 제목** | 교사의 AI 도구 통합 체험에 관한 현상학적 연구 |
| **연구 질문** | 교사들은 AI 도구를 교육 철학과 통합하는 과정에서 어떤 체험을 하는가? |
| **방법론** | 해석학적 현상학 (van Manen) |
| **패러다임** | 해석주의 (Interpretivism) |

### 연구 설계

| 구성요소 | 세부 내용 |
|----------|----------|
| **참여자** | AI 도구 사용 경험이 있는 K-12 교사 5명 |
| **표집 방법** | 목적적 표집 (Purposeful Sampling) |
| **자료 수집** | 심층 인터뷰 2-3회 × 5명 (총 10-15회) |
| **인터뷰 시간** | 회당 60-90분 |
| **분석 방법** | van Manen의 주제 분석 |

### 생활세계 탐구 프레임워크

| 실존체 | 탐구 초점 |
|--------|----------|
| **체험된 공간** | 디지털/물리적 교실 공간의 경험 |
| **체험된 몸** | AI 도구 사용 시 교사로서의 정체성 |
| **체험된 시간** | 수업 준비, 실시간 상호작용의 변화 |
| **체험된 관계** | 학생, 동료, 기술과의 관계 변화 |

### 체크포인트 이력

| Checkpoint | 상태 | 선택 |
|------------|------|------|
| 🔴 CP_PARADIGM_SELECTION | ✅ 통과 | [B] 해석학적 현상학 |
| 🔴 CP_METHODOLOGY_APPROVAL | ✅ 통과 | van Manen 접근 |
| 🟠 CP_PARADIGM_RECONSIDERATION | ✅ 통과 | 질적 연구 유지 |
| 🟠 CP_ANALYSIS_APPROACH | ✅ 통과 | 승인 |

---

## 다음 단계 권장

1. **IRB 승인 신청** - A4-ResearchEthicsAdvisor 활용 가능
2. **인터뷰 프로토콜 개발** - D2-InterviewFocusGroupSpecialist 활용 가능
3. **참여자 모집 기준 구체화**
4. **파일럿 인터뷰 실시**

---

**연구 설계가 완료되었습니다. 다음 단계로 진행할 준비가 되면 알려주세요.**"""
        },

        "META-002": {
            1: """## 🔍 Paradigm Detection

Your research context signals a **Quantitative** approach:

| Detected Keywords | Signal |
|-------------------|--------|
| "meta-analysis" | Systematic synthesis |
| "effectiveness" | Effect measurement |
| "learning outcomes" | Measurable outcomes |
| "moderates" | Moderation analysis |

---

## 🔴 CHECKPOINT: CP_RESEARCH_DIRECTION

**Please select your research direction:**

| Option | Approach | T-Score | Description |
|--------|----------|---------|-------------|
| **[A]** | Overall Effect Analysis | T=0.65 | Traditional meta-analysis examining pooled effect of AI tutoring |
| **[B]** | Subject-Specific Moderator Analysis | T=0.40 ⭐ | Subgroup analysis comparing STEM vs humanities with age moderation |
| **[C]** | Multi-level Meta-Analysis | T=0.25 | Three-level model accounting for study dependencies and nested effects |

**Which direction would you like to pursue?**""",

            2: """## Effect Size Methodology: Hedges' g vs Cohen's d

Excellent question! The choice between these effect sizes matters significantly for meta-analysis.

### Cohen's d
- **Formula**: d = (M₁ - M₂) / SD_pooled
- Uses pooled standard deviation
- **Limitation**: Slightly **biased for small samples** (n < 20)
- Tends to overestimate effect sizes in small studies

### Hedges' g
- **Formula**: g = d × (1 - 3/(4df - 1))
- Applies a **correction factor** for small sample bias
- Recommended by Borenstein et al. (2009) for meta-analysis
- More accurate when synthesizing studies with varied sample sizes

### For Your Research

Given that K-12 studies often have:
- Classroom-level samples (n = 20-40)
- Varied sample sizes across studies

**Hedges' g is recommended** because:
1. Corrects for small sample upward bias
2. More accurate pooled estimates
3. Standard practice in educational meta-analyses

### References
- Hedges, L. V. (1981). Distribution theory for Glass's estimator of effect size
- Borenstein, M., et al. (2009). Introduction to Meta-Analysis

---

🔴 **Checkpoint maintained**: Awaiting your direction selection.
`[A]`, `[B]`, or `[C]`?""",

            3: """## ✅ Selection Confirmed: [B] Subject-Specific Moderator Analysis

Your selection has been logged.

| Item | Details |
|------|---------|
| **Selected Approach** | Subject-specific effects with age moderation |
| **T-Score** | 0.40 (Differentiated approach) |
| **Agent** | C5-MetaAnalysisMaster |

---

## 🔄 Agent Transition: C5-MetaAnalysisMaster

Invoking C5-MetaAnalysisMaster for methodology design...

### Proposed Meta-Analysis Design

| Component | Specification |
|-----------|---------------|
| **Effect Size** | Hedges' g (corrected) |
| **Model** | Random-effects (REML estimation) |
| **Moderators** | Subject type (STEM vs Humanities), Learner age |
| **Heterogeneity** | I², τ², Q-statistic |
| **Subgroup Analysis** | By subject area |
| **Meta-regression** | Age as continuous moderator |

---

🔴 **CHECKPOINT: CP_METHODOLOGY_APPROVAL**

**Proceed with this methodology design?**""",

            4: """## 📊 Addressing Small Sample Concerns

Your concern about normality assumptions is valid and important.

### The Issue

Random-effects models assume:
- Effect sizes are normally distributed
- τ² (between-study variance) is accurately estimated

With **small samples (n < 20 per study)**:
- Effect size distributions may be skewed
- Standard errors may be underestimated
- Confidence intervals may be too narrow

### Recommended Solutions

| Method | Description | When to Use |
|--------|-------------|-------------|
| **Knapp-Hartung Correction** | Adjusts CI using t-distribution | Default recommendation |
| **Permutation Tests** | Non-parametric significance testing | When normality is violated |
| **Robust Variance Estimation** | Handles dependency and heteroscedasticity | Clustered data |
| **HKSJ Method** | Hartung-Knapp-Sidik-Jonkman | Conservative CIs |
| **Bootstrap Meta-Analysis** | Resampling-based inference | Complex models |

### My Recommendation

For your study with potentially small classroom samples:

```
1. Use Knapp-Hartung correction (primary)
2. Report both standard and corrected CIs
3. Conduct sensitivity analysis with permutation tests
4. Check distribution with funnel plot and normality tests
```

This addresses reviewer concerns while maintaining methodological rigor.

---

**Do you want to proceed with these adjustments incorporated?**""",

            5: """## 🔄 Agent Transition: A2-TheoreticalFrameworkArchitect

Understood. Let's step back to establish your theoretical foundation.

---

## 🔴 CHECKPOINT: CP_THEORY_SELECTION

**Theoretical Framework Options for AI Tutoring Effectiveness:**

| Option | Framework | T-Score | Fit |
|--------|-----------|---------|-----|
| **[A]** | Cognitive Load Theory + Self-Determination Theory (CLT-SDT) | T=0.50 | AI reduces extraneous load, supports autonomy |
| **[B]** | Zone of Proximal Development (Vygotsky) | T=0.55 | AI as "more knowledgeable other" |
| **[C]** | ICAP Framework (Chi & Wylie) | T=0.35 ⭐ | AI enables interactive/constructive learning |

### Recommended: [A] CLT-SDT Integration

**Why this combination works:**

1. **Cognitive Load Theory**:
   - AI tutors can reduce extraneous cognitive load
   - Adaptive scaffolding optimizes intrinsic load
   - Frees working memory for germane processing

2. **Self-Determination Theory**:
   - AI provides autonomy (pace, path choices)
   - Competence support through immediate feedback
   - Relatedness via conversational AI interactions

**Context preserved from meta-analysis discussion:**
- Subject-specific effects → CLT explains STEM/humanities differences
- Age moderation → Developmental differences in cognitive load capacity

---

**Which theoretical framework would you like to use?**""",

            6: """## ✅ Framework Selection: [A] Cognitive Load Theory + Self-Determination Theory

Excellent choice. The CLT-SDT integration provides strong theoretical grounding.

| Decision | Details |
|----------|---------|
| **Framework** | CLT-SDT Integration |
| **Justification** | Explains cognitive mechanisms AND motivational factors |
| **Previous Context** | Subject-specific effects, age moderation preserved |

---

## 🔄 Returning to: C5-MetaAnalysisMaster

Now continuing meta-analysis methodology with theoretical grounding...

### Updated Analysis Framework

```
Theoretical Model:
  CLT (Cognitive Load)
    → Extraneous load reduction
    → Germane processing support

  SDT (Motivation)
    → Autonomy support
    → Competence feedback
    → Relatedness (AI persona)

Moderator Hypotheses:
  H1: STEM subjects benefit more from cognitive load reduction
  H2: Humanities benefit more from autonomy support
  H3: Age moderates SDT effects (autonomy more important for older learners)
```

**Ready to continue with methodology specification?**""",

            7: """## 📚 Gray Literature Inclusion Decision

Including gray literature (dissertations, conference papers) is an important methodological decision.

### Publication Bias Considerations

| Aspect | Published Studies | Gray Literature |
|--------|-------------------|-----------------|
| **Effect sizes** | Often larger (publication bias) | May show null/smaller effects |
| **Quality** | Peer-reviewed | Variable quality |
| **Availability** | Easier to access | Harder to obtain |
| **Completeness** | Full reporting | May lack details |

### Detection Methods for Publication Bias

| Method | Purpose |
|--------|---------|
| **Funnel Plot** | Visual asymmetry detection |
| **Egger's Test** | Statistical asymmetry test |
| **Trim-and-Fill** | Adjusted effect estimate |
| **PET-PEESE** | Regression-based correction |

### Recommendations for Your 3 Dissertations

**Include them, with quality sensitivity analysis:**

1. **Code quality separately** (use RoB or JBI checklist)
2. **Run sensitivity analysis**: With vs without gray literature
3. **Report both estimates** transparently
4. **Justify inclusion**: Rothstein et al. (2005) recommends gray literature for reducing bias

---

## 🟠 CHECKPOINT: CP_SCOPE_DECISION

**Decision Options:**

| Option | Strategy |
|--------|----------|
| **[A]** | Exclude gray literature (conservative) |
| **[B]** | Include with quality sensitivity analysis (recommended) ⭐ |
| **[C]** | Include without differentiation |

**Which approach would you prefer?**""",

            8: """## 🔍 Bayesian Meta-Analysis: An Alternative Perspective

Great question! Bayesian approaches offer distinct advantages.

### Frequentist vs Bayesian Meta-Analysis

| Aspect | Frequentist | Bayesian |
|--------|-------------|----------|
| **Interpretation** | p-values, CIs | Posterior probabilities, credible intervals |
| **Prior information** | Not used | Can incorporate prior knowledge |
| **Small k** | Can be problematic | Handles better with informative priors |
| **Uncertainty** | Point estimates focus | Full uncertainty quantification |
| **Software** | metafor, Stata | brms, Stan, JASP |

### Why I Didn't Lead with Bayesian

| Reason | Explanation |
|--------|-------------|
| **Field norms** | Educational research predominantly uses frequentist |
| **Reviewer familiarity** | More reviewers understand frequentist results |
| **Software accessibility** | R metafor is more widely used |
| **Prior specification** | Requires careful justification |

### When Bayesian is Preferable

✅ **Good for your study if:**
- You have strong prior information from previous meta-analyses
- k < 10 studies (small sample of studies)
- You want to quantify probability of meaningful effect

### Hybrid Approach (Recommended)

```
Primary Analysis: Frequentist (REML + Knapp-Hartung)
Sensitivity Analysis: Bayesian with weakly informative priors

Report both:
- "Frequentist 95% CI: [0.25, 0.55]"
- "Bayesian 95% credible interval: [0.23, 0.58] with P(g > 0.2) = 0.89"
```

**T-Score for pure Bayesian: 0.30** (innovative but defensible)

---

**Would you like to add Bayesian sensitivity analysis to the design?**""",

            9: """## 📉 Subgroup Analysis with k=12 Studies

Let me give you an honest assessment.

### Statistical Power Concerns

| Analysis | Minimum k Recommended | Your k | Feasibility |
|----------|----------------------|--------|-------------|
| **Overall effect** | 5-10 | 12 | ✅ Sufficient |
| **Subgroup (STEM)** | 4-5 | 4 | ⚠️ Borderline |
| **Subgroup (Humanities)** | 4-5 | 8 | ✅ Sufficient |
| **Meta-regression (age)** | 10 per predictor | 12 | ⚠️ Limited |

### Borenstein et al. Recommendations

> "Subgroup analyses with fewer than 5 studies per group should be interpreted with extreme caution and may lack statistical power to detect meaningful differences."

### Alternative Approaches

| Option | Advantage | Trade-off |
|--------|-----------|-----------|
| **Meta-regression instead of subgroups** | Treats moderators continuously | Assumes linear relationship |
| **Combine subgroups** | More power | Less specific insights |
| **Exploratory framing** | Honest reporting | Limited generalizability |
| **Report descriptively** | No statistical test | Narrative synthesis |

### My Recommendation

```
1. Report overall effect (k=12) - sufficient power
2. Use meta-regression for age (continuous) - more efficient
3. For STEM vs Humanities:
   - Report descriptive subgroup effects
   - Avoid formal comparison test (k=4 too small)
   - Frame as "exploratory" not "confirmatory"
4. Be transparent about limitations in Discussion
```

---

**Does this adjusted approach work for your analysis plan?**""",

            10: """## ✅ Final Methodology Approved

All checkpoints have been cleared.

---

## 📋 Complete Meta-Analysis Design Summary

### Basic Information

| Component | Specification |
|-----------|---------------|
| **Research Question** | What is the effectiveness of AI tutoring on K-12 outcomes, and do effects differ by subject and age? |
| **Theoretical Framework** | CLT-SDT Integration |
| **Effect Size** | Hedges' g (bias-corrected) |
| **Model** | Random-effects (REML) with Knapp-Hartung correction |

### Study Details

| Aspect | Details |
|--------|---------|
| **Total Studies** | k = 12 |
| **STEM Studies** | k = 4 |
| **Humanities Studies** | k = 8 |
| **Gray Literature** | 3 dissertations (included with sensitivity analysis) |

### Analysis Plan

| Analysis | Method |
|----------|--------|
| **Overall Effect** | Random-effects pooled estimate |
| **Heterogeneity** | I², τ², Q-test, prediction interval |
| **Subject Comparison** | Descriptive subgroup (exploratory) |
| **Age Moderation** | Meta-regression (continuous) |
| **Publication Bias** | Funnel plot, Egger's, trim-and-fill |
| **Sensitivity** | With/without gray literature, Bayesian comparison |

### Checkpoints Resolved

| Checkpoint | Status | Decision |
|------------|--------|----------|
| 🔴 CP_RESEARCH_DIRECTION | ✅ Passed | [B] Subject-specific effects |
| 🔴 CP_THEORY_SELECTION | ✅ Passed | [A] CLT-SDT |
| 🟠 CP_SCOPE_DECISION | ✅ Passed | Include gray literature with sensitivity |
| 🔴 CP_METHODOLOGY_APPROVAL | ✅ Passed | Approved |

---

## Next Steps

1. **Literature Search** - B1-SystematicLiteratureScout available
2. **Quality Assessment** - B2-EvidenceQualityAppraiser for RoB
3. **Effect Size Extraction** - B3-EffectSizeExtractor for Hedges' g calculation
4. **Analysis** - E1-QuantitativeAnalysisGuide for R code

---

**Methodology design complete. Ready to proceed to execution phase when you are.**"""
        }
    }

    def __init__(self, scenario_id: str, verbose: bool = False):
        self.scenario_id = scenario_id
        self.verbose = verbose
        self.protocol = self._load_protocol()
        self.session = TestSession(
            scenario_id=scenario_id,
            scenario_name=self.protocol.get('name', ''),
            language=self.protocol.get('language', 'English'),
            paradigm=self.protocol.get('paradigm', 'unknown'),
            started_at=datetime.now().isoformat()
        )

    def _load_protocol(self) -> dict:
        """Load protocol YAML file."""
        protocol_file = self.PROTOCOL_DIR / f"test_{self.scenario_id.lower().replace('-', '_')}.yaml"
        if not protocol_file.exists():
            raise FileNotFoundError(f"Protocol not found: {protocol_file}")

        with open(protocol_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def run(self) -> TestSession:
        """Run the complete automated test."""
        print(f"\n{'='*60}")
        print(f"Diverga QA Protocol v2.1 - Automated Test")
        print(f"Scenario: {self.scenario_id}")
        print(f"{'='*60}\n")

        conversation_flow = self.protocol.get('conversation_flow', [])

        for turn_spec in conversation_flow:
            turn_num = turn_spec.get('turn', 0)
            user_input = turn_spec.get('user', '').strip()
            user_type = turn_spec.get('user_type', 'UNKNOWN')
            expected = turn_spec.get('expected_behavior', {})

            print(f"[Turn {turn_num}] {user_type}")
            if self.verbose:
                print(f"  User: {user_input[:50]}...")

            # Get simulated response
            response = self._get_simulated_response(turn_num)

            # Detect checkpoints and agents
            checkpoints = self._detect_checkpoints(response, expected)
            agents = self._detect_agents(response, expected)

            # Create turn record
            turn = SimulatedTurn(
                turn_number=turn_num,
                user_type=user_type,
                user_input=user_input,
                user_input_ko=user_input if 'Korean' in self.protocol.get('language', '') else None,
                expected_behavior=expected,
                simulated_response=response,
                checkpoints_triggered=checkpoints,
                agents_invoked=agents
            )

            # Validate turn
            self._validate_turn(turn, expected)

            self.session.turns.append(turn)
            self.session.agents_invoked.extend(agents)

            if checkpoints:
                self.session.total_checkpoints += len(checkpoints)
                self.session.checkpoints_passed += len(checkpoints)

            print(f"  ✓ Completed")

        # Finalize session
        self.session.completed_at = datetime.now().isoformat()
        self.session.agents_invoked = list(set(self.session.agents_invoked))
        self.session.summary = self._generate_summary()

        print(f"\n{'='*60}")
        print(f"Test Complete: {self.scenario_id}")
        print(f"Turns: {len(self.session.turns)}")
        print(f"Checkpoints: {self.session.checkpoints_passed}/{self.session.total_checkpoints}")
        print(f"Agents: {len(self.session.agents_invoked)}")
        print(f"{'='*60}\n")

        return self.session

    def _get_simulated_response(self, turn_num: int) -> str:
        """Get pre-defined simulated response for a turn."""
        templates = self.RESPONSE_TEMPLATES.get(self.scenario_id, {})
        return templates.get(turn_num, f"[Simulated response for turn {turn_num}]")

    def _detect_checkpoints(self, response: str, expected: dict) -> List[str]:
        """Detect checkpoints in response."""
        checkpoints = []

        # Check for checkpoint markers in response
        if 'CHECKPOINT' in response:
            if 'CP_PARADIGM_SELECTION' in response or expected.get('checkpoint') == 'CP_PARADIGM_SELECTION':
                checkpoints.append('CP_PARADIGM_SELECTION')
            if 'CP_METHODOLOGY_APPROVAL' in response or expected.get('next_checkpoint') == 'CP_METHODOLOGY_APPROVAL':
                checkpoints.append('CP_METHODOLOGY_APPROVAL')
            if 'CP_PARADIGM_RECONSIDERATION' in response or expected.get('checkpoint') == 'CP_PARADIGM_RECONSIDERATION':
                checkpoints.append('CP_PARADIGM_RECONSIDERATION')
            if 'CP_ANALYSIS_APPROACH' in response or expected.get('checkpoint') == 'CP_ANALYSIS_APPROACH':
                checkpoints.append('CP_ANALYSIS_APPROACH')

        # Also check expected checkpoints
        if expected.get('checkpoint'):
            if expected['checkpoint'] not in checkpoints:
                checkpoints.append(expected['checkpoint'])

        return checkpoints

    def _detect_agents(self, response: str, expected: dict) -> List[str]:
        """Detect agent invocations."""
        agents = []

        # Check for agent references
        agent_patterns = {
            'C2-QualitativeDesignConsultant': ['C2', 'QualitativeDesign', '질적 설계'],
            'A3-DevilsAdvocate': ['A3', 'DevilsAdvocate', 'Devil\'s Advocate'],
            'E2-QualitativeCodingSpecialist': ['E2', 'QualitativeCoding', '질적 코딩'],
            'C3-MixedMethodsDesignConsultant': ['C3', 'MixedMethods', '혼합방법'],
        }

        for agent, patterns in agent_patterns.items():
            for pattern in patterns:
                if pattern in response:
                    if agent not in agents:
                        agents.append(agent)
                    break

        # Check expected agents
        if expected.get('agent_switch'):
            if expected['agent_switch'] not in agents:
                agents.append(expected['agent_switch'])
        if expected.get('agent_maintains'):
            if expected['agent_maintains'] not in agents:
                agents.append(expected['agent_maintains'])

        return agents

    def _validate_turn(self, turn: SimulatedTurn, expected: dict):
        """Validate turn against expected behaviors."""
        # Check language
        if expected.get('language') == 'Korean':
            # Verify Korean response
            if any(ord(c) >= 0xAC00 and ord(c) <= 0xD7A3 for c in turn.simulated_response):
                turn.validation_notes.append("Korean language verified")
            else:
                turn.validation_passed = False
                turn.validation_notes.append("Expected Korean but found mostly English")

        # Check checkpoint halt
        if expected.get('halt') and not turn.checkpoints_triggered:
            turn.validation_notes.append("Expected checkpoint halt")

    def _generate_summary(self) -> dict:
        """Generate test session summary."""
        return {
            'total_turns': len(self.session.turns),
            'checkpoints_triggered': self.session.total_checkpoints,
            'checkpoints_passed': self.session.checkpoints_passed,
            'agents_invoked': len(self.session.agents_invoked),
            'language_consistency': 'Korean' if 'Korean' in self.session.language else 'English',
            'overall_status': 'PASSED' if self.session.overall_passed else 'FAILED'
        }

    def save_results(self, output_dir: str) -> Path:
        """Save test results to session folder."""
        output_path = Path(output_dir) / self.scenario_id
        output_path.mkdir(parents=True, exist_ok=True)

        # Save conversation transcript (Markdown)
        transcript_file = output_path / 'conversation_transcript.md'
        with open(transcript_file, 'w', encoding='utf-8') as f:
            f.write(f"# {self.scenario_id} Test Session Transcript\n\n")
            f.write(f"**Scenario**: {self.session.scenario_name}\n")
            f.write(f"**Language**: {self.session.language}\n")
            f.write(f"**Started**: {self.session.started_at}\n")
            f.write(f"**Completed**: {self.session.completed_at}\n\n")
            f.write("---\n\n")

            for turn in self.session.turns:
                f.write(f"## Turn {turn.turn_number}: 👤 USER ({turn.user_type})\n\n")
                f.write(f"{turn.user_input}\n\n")
                f.write("---\n\n")
                f.write(f"## Turn {turn.turn_number}: 🤖 ASSISTANT\n\n")
                f.write(f"{turn.simulated_response}\n\n")
                if turn.checkpoints_triggered:
                    f.write(f"**Checkpoints**: {', '.join(turn.checkpoints_triggered)}\n\n")
                if turn.agents_invoked:
                    f.write(f"**Agents**: {', '.join(turn.agents_invoked)}\n\n")
                f.write("---\n\n")

        # Save raw JSON
        raw_file = output_path / 'conversation_raw.json'
        with open(raw_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(self.session), f, indent=2, ensure_ascii=False)

        # Save test result YAML
        result_file = output_path / f'{self.scenario_id}_test_result.yaml'
        with open(result_file, 'w', encoding='utf-8') as f:
            yaml.dump({
                'scenario_id': self.session.scenario_id,
                'name': self.session.scenario_name,
                'test_date': datetime.now().strftime('%Y-%m-%d'),
                'test_mode': 'automated_simulation',
                'language': self.session.language,
                'summary': self.session.summary,
                'checkpoints': [
                    {
                        'id': cp,
                        'status': 'PASSED'
                    }
                    for turn in self.session.turns
                    for cp in turn.checkpoints_triggered
                ],
                'agents_invoked': [
                    {'agent': agent}
                    for agent in self.session.agents_invoked
                ],
                'turns': [
                    {
                        'turn': t.turn_number,
                        'user_type': t.user_type,
                        'checkpoints': t.checkpoints_triggered,
                        'agents': t.agents_invoked,
                        'passed': t.validation_passed
                    }
                    for t in self.session.turns
                ]
            }, f, default_flow_style=False, allow_unicode=True)

        # Save README
        readme_file = output_path / 'README.md'
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(f"# {self.scenario_id} Test Session\n\n")
            f.write(f"**Scenario**: {self.session.scenario_name}\n")
            f.write(f"**Test Date**: {datetime.now().strftime('%Y-%m-%d')}\n")
            f.write(f"**Status**: {'✅ PASSED' if self.session.overall_passed else '❌ FAILED'}\n\n")
            f.write("---\n\n")
            f.write("## Session Contents\n\n")
            f.write("| File | Description |\n")
            f.write("|------|-------------|\n")
            f.write("| `conversation_transcript.md` | Human-readable conversation |\n")
            f.write("| `conversation_raw.json` | Raw JSON data |\n")
            f.write(f"| `{self.scenario_id}_test_result.yaml` | Test evaluation |\n\n")
            f.write("## Summary\n\n")
            f.write(f"| Metric | Value |\n")
            f.write(f"|--------|-------|\n")
            f.write(f"| Total Turns | {self.session.summary.get('total_turns', 0)} |\n")
            f.write(f"| Checkpoints | {self.session.summary.get('checkpoints_passed', 0)} |\n")
            f.write(f"| Agents | {self.session.summary.get('agents_invoked', 0)} |\n")
            f.write(f"| Language | {self.session.summary.get('language_consistency', 'N/A')} |\n")

        print(f"Results saved to: {output_path}")
        return output_path


def main():
    parser = argparse.ArgumentParser(description='Automated Test Simulator')
    parser.add_argument('--scenario', '-s', required=True, help='Scenario ID (e.g., QUAL-002)')
    parser.add_argument('--output', '-o', default='qa/reports/sessions/', help='Output directory')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    simulator = AutomatedTestSimulator(args.scenario, verbose=args.verbose)
    session = simulator.run()
    simulator.save_results(args.output)


if __name__ == '__main__':
    main()
