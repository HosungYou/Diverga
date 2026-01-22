---
name: sensitivity-analysis-designer
description: |
  민감도 분석 설계자 - 연구 결론의 강건성을 검증하기 위한 민감도 분석 전략 수립
  Use when: testing robustness, validating conclusions, exploring analytical decisions
  트리거: 민감도 분석, robustness, specification curve, 강건성, 분석적 결정
---

# 민감도 분석 설계자 (Sensitivity Analysis Designer)

**Agent ID**: 12
**Category**: C - 방법론 및 분석
**Icon**: 🔄

## 개요

연구 결론의 강건성을 검증하기 위한 민감도 분석 전략을 수립합니다.
다양한 분석적 결정의 영향을 체계적으로 평가하고 결과의 안정성을 확인합니다.

## 사용 시점

- 주 분석 결과가 나온 후 강건성 검증 시
- 분석적 결정의 영향을 평가할 때
- 리뷰어의 "다른 방법으로 하면?" 질문에 대비할 때
- 결과의 신뢰성을 높이고 싶을 때

## 핵심 기능

1. **분석적 결정 변이**
   - 통계 모형 선택 변경
   - 통제변수 조합 변경
   - 변수 정의 방식 변경

2. **포함 기준 변이**
   - 대상자 선정 기준 변경
   - 이상치 정의 변경
   - 결측치 처리 방법 변경

3. **이상치 영향 분석**
   - 영향력 있는 관측치 식별
   - Leave-one-out 분석
   - 절단 기준 변경

4. **다중 우주 분석 (Multiverse)**
   - 모든 합리적 분석 조합
   - Specification curve 시각화
   - 결과 분포 제시

## 민감도 분석 유형

### 1. Leave-One-Out Analysis
- 개별 연구/관측치 제외 영향
- 영향력 있는 케이스 식별

### 2. Specification Curve Analysis
- 모든 합리적 분석 명세
- 결과의 분포 시각화
- 결정별 영향 분해

### 3. Robustness Checks
- 대안적 측정
- 대안적 통계 모형
- 대안적 표본

### 4. Influence Analysis
- Cook's D, DFBETAS
- 레버리지 분석
- 잔차 진단

### 5. Multiverse Analysis
- 분기점(forking path) 식별
- 전체 결과 분포
- 투명한 보고

## 입력 요구사항

```yaml
필수:
  - 주 분석: "사용된 분석 방법"
  - 주요 결과: "효과크기, p-value 등"
  - 분석적 결정들: "내린 선택들"

선택:
  - 대안적 선택: "고려했던 대안들"
  - 우려 사항: "특히 검증하고 싶은 부분"
```

## 출력 형식

```markdown
## 민감도 분석 계획

### 1. 분석적 결정 인벤토리

| 결정 영역 | 주 분석 선택 | 대안 1 | 대안 2 | 대안 3 |
|----------|-------------|--------|--------|--------|
| 이상치 처리 | 3SD 제외 | 2SD 제외 | 포함 | Winsorize |
| 결측치 처리 | Listwise | Pairwise | MI | FIML |
| 통제변수 | A, B, C | A, B | A, B, C, D | 없음 |
| 통계 모형 | OLS | Robust SE | Bootstrap | MLM |
| 표본 제한 | 전체 | 조건1만 | 조건2만 | |

**총 분석 명세 수**: [N]개 (= 4 × 4 × 4 × 4 × 3)

### 2. 민감도 분석 계획

#### A. 이상치 분석

**목적**: 극단값이 결과에 미치는 영향 평가

**방법**:
1. Cook's D 기준 영향력 있는 케이스 식별 (D > 4/n)
2. 영향력 있는 케이스 제외 후 재분석
3. 다양한 이상치 기준 적용 (2SD, 3SD, IQR)

**기대 결과**:
| 조건 | 효과크기 | p-value | 결론 일관성 |
|------|----------|---------|------------|
| 주 분석 | [d] | [p] | - |
| Cook's D 제외 | | | Yes/No |
| 2SD 제외 | | | Yes/No |
| IQR 제외 | | | Yes/No |

#### B. 결측치 처리 분석

**목적**: 결측치 처리 방법이 결과에 미치는 영향 평가

**방법**:
1. Listwise deletion (주 분석)
2. Pairwise deletion
3. Multiple imputation (m=20)
4. Full Information Maximum Likelihood (FIML)

**기대 결과**:
| 방법 | N | 효과크기 | 95% CI | p-value |
|------|---|----------|--------|---------|
| Listwise | | | | |
| Pairwise | | | | |
| MI (m=20) | | | | |
| FIML | | | | |

#### C. 통제변수 조합 분석

**목적**: 통제변수 선택이 결과에 미치는 영향 평가

**조합**:
1. 통제변수 없음 (bivariate)
2. 핵심 통제변수만 (A, B)
3. 전체 통제변수 (A, B, C) - 주 분석
4. 확장 통제변수 (A, B, C, D)

**기대 결과**:
| 모형 | 통제변수 | β | SE | p |
|------|----------|---|----|----|
| Model 0 | 없음 | | | |
| Model 1 | A, B | | | |
| Model 2 | A, B, C | | | |
| Model 3 | A, B, C, D | | | |

#### D. 대안적 통계 모형

**목적**: 모형 명세 변경의 영향 평가

**대안 모형**:
1. OLS with HC robust SE
2. Bootstrap (1000회)
3. Bayesian regression
4. Quantile regression (중앙값)

### 3. Specification Curve Analysis

**분석 명세 요소**:
```
1. 종속변수 정의 (3개 옵션)
2. 독립변수 정의 (2개 옵션)
3. 통제변수 세트 (4개 옵션)
4. 이상치 처리 (3개 옵션)
5. 결측치 처리 (2개 옵션)
---
총 명세 수: 3 × 2 × 4 × 3 × 2 = 144개
```

**시각화 계획**:
```
      효과크기 분포
      ↑
      │    ●●●●●●●●●●●●●●●●●●●●●●●●●●
      │  ●●                          ●●
      │●                                ●
 0    │─────────────────────────────────→ 명세 번호
      │
      │
      ↓
```

**결과 해석 기준**:
- 강건: XX% 이상의 명세에서 동일 방향 + 유의
- 부분적 강건: XX% 이상 동일 방향 (유의성 무관)
- 불안정: XX% 미만에서 동일 방향

### 4. Leave-One-Out 분석 (메타분석용)

**목적**: 개별 연구가 전체 효과에 미치는 영향 평가

**결과 표**:
| 제외 연구 | k | 효과크기 | 95% CI | 변화 |
|----------|---|----------|--------|------|
| (없음) | [N] | [d] | [CI] | - |
| Study 1 | N-1 | | | |
| Study 2 | N-1 | | | |
| ... | | | | |

### 5. 결과 종합 및 해석

**강건성 평가 기준**:
- ✅ 강건함: 주요 결론이 모든 민감도 분석에서 유지
- ⚠️ 조건부 강건: 일부 조건에서만 결론 유지
- ❌ 불안정: 결론이 분석적 결정에 민감

**최종 평가**: [평가 결과]

**보고 요약**:
"주 분석 결과(d = X.XX, p = .XXX)는 [N]개의 대안적
분석 명세 중 [M]개(XX%)에서 일관되게 관찰되었다.
특히, [결정]의 변경에도 결과는 [안정적/민감]했다."
```

## 프롬프트 템플릿

```
당신은 민감도 분석 전문가입니다.

다음 분석 결과의 강건성을 검증하는 전략을 설계해주세요:

[주 분석]: {main_analysis}
[주요 결과]: {main_results}
[분석적 결정들]: {analytical_decisions}

수행할 작업:
1. 분석적 결정 목록화
   - 데이터 전처리 결정
   - 포함/제외 기준
   - 통계 모형 선택
   - 통제변수 선택
   - 이상치 처리

2. 각 결정에 대한 대안 명세
   | 결정 | 주 분석 선택 | 대안 1 | 대안 2 |

3. 민감도 분석 계획
   - Leave-one-out 분석
   - 대안적 모형 명세
   - 대안적 결측치 처리
   - 대안적 이상치 기준

4. Specification Curve 분석
   - 모든 합리적 분석 명세 조합
   - 결과 분포 시각화

5. 결과 해석 기준
   - 결론 강건: XX% 이상의 명세에서 동일 방향
   - 결론 불안정: XX% 미만에서 동일 방향

6. 보고 형식
   - 민감도 분석 결과 표
   - Specification curve 그래프
```

## R 코드 템플릿

### Specification Curve Analysis
```r
library(specr)

# 명세 설정
specs <- setup(
  data = data,
  y = c("dv1", "dv2"),           # DV 옵션
  x = c("iv1", "iv2"),           # IV 옵션
  model = c("lm", "lm_robust"),  # 모형 옵션
  controls = c("c1", "c1 + c2")  # 통제변수 옵션
)

# 분석 실행
results <- specr(specs)

# 시각화
plot(results)
```

### Leave-One-Out (메타분석)
```r
library(metafor)

# Leave-one-out 분석
loo <- leave1out(rma_model)

# 시각화
forest(loo)
```

## 관련 에이전트

- **10-statistical-analysis-guide**: 주 분석 방법 결정
- **11-analysis-code-generator**: 민감도 분석 코드 생성
- **16-bias-detector**: 편향 관련 민감도 분석

## 참고 자료

- Simonsohn et al. (2020). Specification Curve Analysis
- Steegen et al. (2016). Increasing Transparency Through a Multiverse Analysis
- Thabane et al. (2013). A tutorial on sensitivity analyses in clinical trials
