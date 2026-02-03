# VS-Research Framework
## Verbalized Sampling for Academic Research

**Based on**: arXiv:2510.01171 - Verbalized Sampling (VS) for creative, high-entropy outputs

---

## Overview

VS-Research는 학술 연구 추천에서 **Mode Collapse**를 방지하기 위한 Verbalized Sampling 방법론의 학술 연구 특화 버전입니다. 일반적인 LLM 응답은 가장 확률 높은 "모달" 답변에 수렴하는 경향이 있으나, VS-Research는 이를 명시적으로 식별하고 회피하여 더 창의적이고 차별화된 연구 추천을 제공합니다.

## Mode Collapse 문제

### 학술 연구에서의 증상

| 영역 | 모달 응답 예시 | 문제점 |
|------|---------------|--------|
| 이론 추천 | TAM, SCT, TPB 반복 | 이론적 기여 부재 |
| 통계 방법 | "회귀분석 추천" | 방법론적 단조로움 |
| 문헌 검색 | 단일 검색 전략 | 낮은 재현율 |
| 비판적 검토 | "선택 편향 주의" | 표면적 비판 |
| 편향 분석 | 모든 편향 동일 취급 | 맥락 무시 |

### VS가 해결하는 문제

```
Without VS:
  "이론적 프레임워크 추천" → TAM (80% 확률)
                          → UTAUT (15%)
                          → 기타 (5%)

With VS:
  Phase 1: "TAM/UTAUT는 80%의 유사 연구가 사용 → 금지"
  Phase 2: Long-tail 탐색 → 이론 통합, 신규 프레임워크
  Phase 3: T-Score 0.3 이하 선택 → 차별화된 기여
```

---

## VS-Research 5단계 프로세스

### Phase 0: 맥락 수집 (MANDATORY)

VS 적용 전 반드시 수집해야 할 정보:

```yaml
필수 맥락:
  - 연구 분야: "교육학/심리학/경영학/..."
  - 연구 질문: "구체적 RQ"
  - 연구 유형: "양적/질적/혼합/메타분석"
  - 대상 저널: "타겟 저널 또는 수준"

선택 맥락:
  - 기존 이론 선호: "있으면 기재"
  - 방법론 제약: "접근 가능한 도구/데이터"
  - 시간적 제약: "긴급 vs 충분"
```

### Phase 1: 모달 응답 식별

**목적**: 가장 예측 가능한 "뻔한" 추천을 명시적으로 식별하고 금지

```markdown
## Phase 1: 모달 응답 식별

⚠️ **모달 경고**: 다음은 [주제]에 대한 가장 예측 가능한 추천입니다:

| 모달 옵션 | T-Score | 사용 비율 | 문제점 |
|----------|---------|----------|--------|
| [옵션1] | 0.9+ | 60%+ | [차별화 불가] |
| [옵션2] | 0.85 | 25% | [이미 포화] |

➡️ 이것은 기준선입니다. 이 이상을 탐색합니다.
```

### Phase 2: Long-Tail 샘플링

**목적**: Typicality Score(T-Score) 기반으로 낮은 확률의 대안 탐색

```markdown
## Phase 2: Long-Tail 샘플링

**방향 A** (T ≈ 0.7): 안전하지만 차별화
- [옵션]: [설명]
- 장점: 피어리뷰에서 방어 가능, 약간의 신선함
- 적합: 보수적 저널, 첫 출판

**방향 B** (T ≈ 0.4): 독특하고 정당화 가능
- [옵션]: [설명]
- 장점: 이론적 기여 명확, 차별화
- 적합: 혁신 지향 저널, 중견 연구자

**방향 C** (T < 0.2): 혁신적/실험적
- [옵션]: [설명]
- 장점: 최대 기여 가능성
- 적합: 탑티어 저널, 패러다임 전환 목표
```

### Phase 3: 저-전형성 선택

**목적**: 맥락에 가장 적합한 낮은 T-Score 옵션 선택

선택 기준:
1. **학술적 건전성**: 피어리뷰에서 방어 가능
2. **맥락 적합성**: 연구 질문과의 일치도
3. **기여 잠재력**: 이론적/방법론적 기여
4. **실현 가능성**: 연구자의 역량과 자원

### Phase 4: 실행

**목적**: 선택된 대안을 학술적 엄격성을 유지하며 구체화

```markdown
## Phase 4: 추천 실행

**선택된 방향**: [방향 B/C] (T-Score: [X.X])

### 구체적 추천

[상세 내용]

### 이론적/방법론적 근거

[학술 문헌 기반 정당화]

### 실행 가이드

[구체적 단계]
```

### Phase 5: 독창성 검증

**목적**: 최종 추천이 진정으로 차별화되었는지 확인

```markdown
## Phase 5: 독창성 검증

✅ 모달 회피 체크:
- [ ] "80%의 AI가 이 추천을 할까?" → NO여야 함
- [ ] "유사 연구 검색에서 상위 5개에 나올까?" → NO여야 함
- [ ] "리뷰어가 '뻔하다'고 할까?" → NO여야 함

✅ 품질 체크:
- [ ] 피어리뷰에서 방어 가능한가? → YES
- [ ] 이론적/방법론적 근거가 있는가? → YES
- [ ] 재현 가능한가? → YES
```

---

## 학술 연구용 품질 가드레일

### NON-NEGOTIABLE 규칙

VS로 창의성을 추구하더라도 다음은 절대 타협 불가:

| 가드레일 | 설명 | 검증 방법 |
|---------|------|----------|
| **방법론적 건전성** | 피어리뷰에서 방어 가능 | 문헌 근거 제시 |
| **내적 타당도** | 위협 인정 및 대응 | 명시적 한계 섹션 |
| **재현가능성** | 절차 완전 문서화 | 체크리스트 완료 |
| **윤리적 준수** | IRB/연구윤리 충족 | 승인 문서 확인 |

### T-Score 하한선

```
연구 유형별 최소 T-Score:

IRB 관련 → T ≥ 0.7 (윤리는 보수적으로)
통계 방법 → T ≥ 0.5 (검증된 방법만)
이론 프레임워크 → T ≥ 0.3 (혁신 가능)
문헌 검색 전략 → T ≥ 0.4 (재현성 유지)
```

---

## Typicality Score 참조표

### 이론적 프레임워크

```
T > 0.8  (모달 - 회피):
  - Technology Acceptance Model (TAM)
  - Social Cognitive Theory (SCT)
  - Theory of Planned Behavior (TPB)
  - UTAUT/UTAUT2

T 0.5-0.8 (확립 - 차별화 가능):
  - Self-Determination Theory (SDT)
  - Cognitive Load Theory (CLT)
  - Flow Theory
  - Community of Inquiry (CoI)
  - Expectancy-Value Theory
  - Achievement Goal Theory

T 0.3-0.5 (신흥 - 권장):
  - 이론 통합 (예: TAM × SDT)
  - 맥락 특화 변형
  - 다수준 이론 적용
  - 경쟁 이론 비교 프레임워크

T < 0.3 (혁신 - 탑티어용):
  - 새로운 이론적 합성
  - 분야 간 이론 전이
  - 메타-이론적 프레임워크
  - 패러다임 전환 제안
```

### 통계 분석 방법

```
T > 0.8 (모달 - 회피):
  - Independent t-test
  - One-way ANOVA
  - OLS Regression
  - Pearson correlation

T 0.5-0.8 (확립 - 상황에 따라):
  - Hierarchical Linear Modeling (HLM)
  - Structural Equation Modeling (SEM)
  - Traditional Meta-analysis
  - Mixed-effects models

T 0.3-0.5 (신흥 - 권장):
  - Bayesian methods
  - Meta-Analytic SEM (MASEM)
  - Machine Learning + inference
  - Causal inference methods

T < 0.3 (혁신 - 탑티어용):
  - Causal discovery algorithms
  - Network psychometrics
  - Computational modeling
  - Novel hybrid methods
```

### 문헌 검색 전략

```
T > 0.8 (모달 - 확장 필요):
  - 단일 데이터베이스
  - 키워드만 사용
  - 제목/초록 검색

T 0.5-0.8 (확립 - 보완):
  - 다중 데이터베이스
  - Boolean 연산자 활용
  - MeSH/Thesaurus 사용

T 0.3-0.5 (포괄적 - 권장):
  - 인용 추적 (전방/후방)
  - 전문가 상담
  - Grey literature 포함

T < 0.3 (혁신 - 특수 상황):
  - Semantic search
  - AI-assisted screening
  - Living review 방법론
```

### 비판적 검토 (Devil's Advocate)

```
T > 0.8 (뻔한 비판 - 넘어서야 함):
  - "선택 편향 가능성"
  - "표본 크기 제한"
  - "일반화 한계"

T 0.5-0.8 (구체적 비판):
  - 특정 설계 위협 식별
  - 맥락 특화 한계
  - 대안적 분석 제안

T 0.3-0.5 (통찰 비판 - 권장):
  - 대안적 설명 제시
  - 가정 도전
  - 반증 시나리오 구성

T < 0.3 (패러다임 비판):
  - 인식론적 전제 질문
  - 분야 간 관점 적용
  - 메타-비판
```

---

## VS 적용 수준별 가이드

### Full VS (5단계 전체)

**적용 에이전트**: 02, 03, 05, 10, 16

**특징**:
- 완전한 Phase 0-5 실행
- 명시적 T-Score 계산 및 제시
- 3개 이상 대안 제시
- 독창성 검증 필수

### Enhanced VS (3단계 간소화)

**적용 에이전트**: 01, 04, 06, 07, 08, 09

**특징**:
- Phase 1 (모달 식별) + Phase 2 (대안 제시) + Phase 4 (실행)
- T-Score 대략적 범위 표시
- 2개 이상 대안 제시
- 간소화된 검증

### Light VS (모달 인식만)

**적용 에이전트**: 11, 12, 13, 14, 15, 17, 18, 19, 20

**특징**:
- Phase 1 (모달 식별) + 대안 언급
- "가장 일반적인 접근"을 명시하고 대안 제시
- T-Score 미제시 (대신 "일반적/독특한" 표현)
- 맥락에 따라 모달 허용

---

## VS 실행 예시

### 예시: 이론적 프레임워크 추천 (Full VS)

**연구 질문**: "AI 챗봇이 언어 학습자의 말하기 불안에 미치는 효과"

```markdown
## Phase 1: 모달 응답 식별

⚠️ **모달 경고**: 다음은 AI 언어 학습 연구의 가장 예측 가능한 이론입니다:

| 모달 옵션 | T-Score | 사용 비율 | 문제점 |
|----------|---------|----------|--------|
| TAM | 0.92 | 45% | 기술 수용에만 초점, 불안 미설명 |
| Social Cognitive Theory | 0.88 | 30% | 과도하게 일반적 |
| UTAUT | 0.85 | 15% | 조직 맥락 중심 |

➡️ 이들은 기준선입니다. 이 이상을 탐색합니다.

---

## Phase 2: Long-Tail 샘플링

**방향 A** (T = 0.65): Affective Filter Hypothesis × SDT 통합
- Krashen의 정의적 여과 가설 + 자기결정이론
- 장점: 언어학습 맥락 특화, 동기-불안 연결
- 적합: 응용언어학 저널

**방향 B** (T = 0.45): Control-Value Theory of Achievement Emotions
- Pekrun의 성취 감정 이론
- 장점: 통제감-가치-감정 메커니즘 명확
- 적합: 교육심리학 저널, 차별화 높음

**방향 C** (T = 0.28): Flow × Emotional Design 통합 프레임워크
- Csikszentmihalyi + Norman의 감성 디자인
- 장점: 최적 경험과 기술 설계 연결
- 적합: HCI/교육공학 탑티어

---

## Phase 3: 저-전형성 선택

**선택**: 방향 B - Control-Value Theory (T = 0.45)

**선택 근거**:
1. 불안의 선행요인(통제감, 과제가치)을 직접 설명
2. AI 챗봇의 즉각적 피드백 → 통제감 증가 → 불안 감소 경로 설정 가능
3. 가설 도출이 명확
4. 교육심리학 저널에서 환영받는 프레임워크

---

## Phase 4: 실행

### 추천 이론적 프레임워크

**Control-Value Theory of Achievement Emotions (Pekrun, 2006)**

[구체적 적용 방안...]

---

## Phase 5: 독창성 검증

✅ 모달 회피:
- [x] TAM/SCT/UTAUT 대신 CVT 선택
- [x] 유사 연구 상위 5개에 없음
- [x] 리뷰어에게 신선하게 보일 것

✅ 품질 확보:
- [x] Pekrun(2006) 등 핵심 문헌 근거
- [x] 검증된 측정도구 존재 (AEQ)
- [x] 경로 모형 논리적
```

---

## 에이전트별 VS 통합 가이드

### Full VS 에이전트용 템플릿

```markdown
## VS-Research 프로세스

<vs-phase-1>
### Phase 1: 모달 응답 식별
[모달 테이블 + 경고 메시지]
</vs-phase-1>

<vs-phase-2>
### Phase 2: Long-Tail 샘플링
[방향 A, B, C 제시]
</vs-phase-2>

<vs-phase-3>
### Phase 3: 저-전형성 선택
[선택 및 근거]
</vs-phase-3>

<vs-phase-4>
### Phase 4: 실행
[구체적 추천]
</vs-phase-4>

<vs-phase-5>
### Phase 5: 독창성 검증
[체크리스트]
</vs-phase-5>
```

### Enhanced VS 에이전트용 템플릿

```markdown
## VS-Research 프로세스 (Enhanced)

### 일반적 접근 (회피 또는 보완 필요)
[모달 옵션 1-2개]

### 대안적 접근 (권장)
**옵션 A**: [설명]
**옵션 B**: [설명]

### 추천
[선택 및 근거]
```

### Light VS 에이전트용 템플릿

```markdown
## 접근 방식

> 💡 **참고**: 가장 일반적인 접근은 [X]입니다.
> 그러나 [맥락]을 고려하면 [대안]도 고려해 볼 수 있습니다.

[본문 내용]
```

---

## 측정 및 평가

### VS 효과 측정 지표

```yaml
모드 회피율:
  정의: "(비-모달 응답 수) / (전체 응답 수)"
  목표: "> 80%"
  측정: 동일 쿼리 10회 실행 후 계산

다양성 점수:
  정의: "응답 간 코사인 유사도의 역수 평균"
  목표: "> 0.6"
  측정: 임베딩 기반 분석

전문가 평가:
  - 놀라움 점수 (1-5): "예상 밖의 유용한 추천"
  - 유용성 점수 (1-5): "실제 연구에 적용 가능"
  목표: 둘 다 ≥ 3.5

가드레일 준수:
  정의: "품질 기준 충족 비율"
  목표: "100%"
  측정: 체크리스트 기반
```

---

## 참고 문헌

- arXiv:2510.01171 - Verbalized Sampling for creative outputs
- VS Design Diverge PR: https://github.com/anthropics/skills/pull/242
- Pekrun, R. (2006). The control-value theory of achievement emotions
- Csikszentmihalyi, M. (1990). Flow: The psychology of optimal experience
