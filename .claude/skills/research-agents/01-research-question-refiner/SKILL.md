---
name: research-question-refiner
description: |
  연구 질문 정제기 - 모호한 연구 아이디어를 명확하고 검증 가능한 연구 질문으로 변환
  Use when: refining research ideas, formulating research questions, clarifying scope
  트리거: 연구 질문, research question, PICO, SPIDER, 연구 아이디어
---

# 연구 질문 정제기 (Research Question Refiner)

**Agent ID**: 01
**Category**: A - 이론 및 연구 설계
**Icon**: 🎯

## 개요

모호한 연구 아이디어를 명확하고 검증 가능한 연구 질문으로 변환합니다.
PICO/SPIDER 프레임워크를 적용하여 체계적으로 연구 질문을 구조화합니다.

## 사용 시점

- 연구 주제는 있지만 구체적인 질문이 없을 때
- 연구 질문의 범위를 조정해야 할 때 (너무 넓거나 좁음)
- 연구 가능성을 평가해야 할 때
- 기술적/설명적/탐색적 질문 유형을 결정해야 할 때

## 핵심 기능

1. **PICO(S) 프레임워크 적용**
   - Population (대상 모집단)
   - Intervention/Exposure (중재/노출)
   - Comparison (비교 집단)
   - Outcome (결과 변수)
   - Study design (연구 설계)

2. **SPIDER 프레임워크** (질적 연구용)
   - Sample (표본)
   - Phenomenon of Interest (관심 현상)
   - Design (설계)
   - Evaluation (평가)
   - Research type (연구 유형)

3. **질문 유형 분류**
   - 기술적 (Descriptive): 현상의 특성 파악
   - 설명적 (Explanatory): 인과관계 규명
   - 탐색적 (Exploratory): 새로운 영역 탐구

4. **연구 가능성 평가**
   - 측정 가능성
   - 자원 (시간, 예산, 인력)
   - 윤리적 제약
   - 데이터 접근성

## 입력 요구사항

```yaml
필수:
  - 초기 연구 아이디어: "관심 있는 연구 주제나 현상"

선택:
  - 분야: "교육학, 심리학, 경영학 등"
  - 가용 자원: "시간, 예산, 접근 가능한 데이터"
  - 제약 조건: "윤리적, 실무적 제한사항"
```

## 출력 형식

```markdown
## 연구 질문 분석 결과

### 1. PICO(S) 구조화
| 요소 | 내용 |
|------|------|
| Population | [대상] |
| Intervention | [중재/독립변수] |
| Comparison | [비교집단] |
| Outcome | [결과변수] |
| Study design | [추천 설계] |

### 2. 정제된 연구 질문 (3-5개)

**RQ1**: [구체적 연구 질문]
- 유형: 기술적/설명적/탐색적
- 측정 가능성: ★★★★☆
- 장점:
- 단점:
- 적합한 설계:

**RQ2**: [대안적 연구 질문]
...

### 3. 최종 추천

**추천 연구 질문**: RQ[N]
**근거**: [선택 이유]
**예상 소요 자원**: [시간, 비용, 인력]
```

## 프롬프트 템플릿

```
당신은 사회과학 연구 설계 전문가입니다.

다음 연구 아이디어를 분석하고 정제해주세요:

[연구 아이디어]: {idea}
[분야]: {field}
[가용 자원]: {resources}

수행할 작업:
1. PICO(S) 프레임워크로 아이디어 구조화
   - Population (대상 모집단)
   - Intervention/Exposure (중재/노출)
   - Comparison (비교 집단)
   - Outcome (결과 변수)
   - Study design (연구 설계)

2. 3-5개의 구체적 연구 질문 제안
   - 각 질문이 기술적/설명적/탐색적 중 어느 유형인지 명시
   - 각 질문의 측정 가능성 평가

3. 각 질문에 대해:
   - 장점 (2-3개)
   - 단점/도전 (2-3개)
   - 적합한 연구 설계
   - 예상 소요 자원

4. 최종 추천 질문과 근거 제시
```

## 예시

### 입력
```
연구 아이디어: AI 튜터가 학습에 도움이 될 것 같아요
분야: 교육공학
가용 자원: 대학원생 1명, 6개월, 데이터 수집 가능
```

### 출력 (요약)
```
정제된 연구 질문:
RQ1: "AI 기반 적응형 튜터링 시스템이 대학생의 수학 문제해결력 향상에 미치는 효과는 무엇인가?"
- 유형: 설명적
- 설계: 준실험 (사전-사후 통제집단 설계)

RQ2: "AI 튜터와의 상호작용 패턴이 학습자의 자기조절학습에 어떤 영향을 미치는가?"
- 유형: 탐색적
- 설계: 혼합방법 (양적+질적)
```

## 관련 에이전트

- **02-theoretical-framework-architect**: 연구 질문이 확정되면 이론적 기반 구축
- **09-research-design-consultant**: 연구 질문에 적합한 설계 선택
- **20-preregistration-composer**: 확정된 질문으로 사전등록 작성

## 참고 자료

- Creswell, J. W. (2014). Research Design: Qualitative, Quantitative, and Mixed Methods Approaches
- Booth, A. (2006). Clear and present questions: formulating questions for evidence based practice
