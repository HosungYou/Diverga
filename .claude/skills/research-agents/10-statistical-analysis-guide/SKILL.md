---
name: statistical-analysis-guide
description: |
  통계 분석 가이드 - 연구 설계와 데이터에 적합한 통계 분석 방법 선택 및 실행 지원
  Use when: selecting statistical methods, interpreting results, checking assumptions
  트리거: 통계 분석, ANOVA, 회귀, t-test, 검정력, 가정 점검, 효과크기
---

# 통계 분석 가이드 (Statistical Analysis Guide)

**Agent ID**: 10
**Category**: C - 방법론 및 분석
**Icon**: 📈

## 개요

연구 설계와 데이터 특성에 적합한 통계 분석 방법을 선택하고 실행을 지원합니다.
가정 점검, 검정력 분석, 효과크기 해석까지 포괄적인 안내를 제공합니다.

## 사용 시점

- 적절한 분석 방법을 선택해야 할 때
- 통계적 가정을 점검해야 할 때
- 표본 크기/검정력을 계산해야 할 때
- 결과를 해석해야 할 때

## 핵심 기능

1. **분석 방법 매칭**
   - 변수 유형 기반 추천
   - 설계 유형 고려
   - 가정 충족 여부 반영

2. **가정 점검**
   - 정규성, 등분산성
   - 독립성, 선형성
   - 위반 시 대안 제시

3. **검정력 분석**
   - 사전 분석: 필요 표본 크기
   - 사후 분석: 달성된 검정력
   - 민감도 분석

4. **효과크기 해석**
   - 적절한 지표 선택
   - 해석 기준 제공
   - 실무적 의미

5. **다중 비교 교정**
   - Bonferroni
   - FDR (Benjamini-Hochberg)
   - Tukey HSD

## 분석 방법 라이브러리

### 집단 비교

| 조건 | 방법 | 비모수 대안 |
|------|------|------------|
| 2집단 독립, 연속 DV | Independent t-test | Mann-Whitney U |
| 2집단 대응, 연속 DV | Paired t-test | Wilcoxon signed-rank |
| 3+ 집단 독립, 연속 DV | One-way ANOVA | Kruskal-Wallis |
| 2+ 요인, 연속 DV | Factorial ANOVA | - |
| 반복측정, 연속 DV | RM-ANOVA | Friedman test |
| 공변인 통제 | ANCOVA | - |
| 다중 DV | MANOVA | - |

### 관계 분석

| 조건 | 방법 | 비모수 대안 |
|------|------|------------|
| 2 연속 변수 | Pearson r | Spearman ρ |
| 통제 변수 있음 | Partial correlation | - |
| 1 IV → 1 DV | Simple regression | - |
| 다중 IV → 1 DV | Multiple regression | - |
| 위계적 모형 | Hierarchical regression | - |
| 매개/조절 | Process/SEM | - |

### 범주형 분석

| 조건 | 방법 |
|------|------|
| 2×2 범주형 | Chi-square / Fisher's exact |
| R×C 범주형 | Chi-square test |
| 이분 DV | Logistic regression |
| 다분 DV | Multinomial logistic |
| 순서 DV | Ordinal regression |

### 고급 분석

| 방법 | 적용 상황 |
|------|----------|
| HLM/MLM | 위계적/군집 데이터 |
| SEM | 잠재변수, 복잡 경로 |
| Meta-analysis | 연구 종합 |
| Factor analysis | 척도 개발/검증 |

## 입력 요구사항

```yaml
필수:
  - 연구 질문: "분석하려는 관계/차이"
  - 독립변수: "유형(연속/범주), 수준 수"
  - 종속변수: "유형(연속/범주), 수준 수"

선택:
  - 통제변수: "공변인 목록"
  - 설계: "독립/대응/혼합"
  - 표본 크기: "현재 또는 예상 N"
```

## 출력 형식

```markdown
## 통계 분석 가이드

### 1. 분석 개요

| 항목 | 내용 |
|------|------|
| 연구 질문 | [질문] |
| 독립변수 | [변수명] (유형: [연속/범주], 수준: [N]) |
| 종속변수 | [변수명] (유형: [연속/범주]) |
| 통제변수 | [변수명] |
| 설계 | [독립/대응/혼합] |

### 2. 추천 분석 방법

**주 분석**: [방법명]
- 근거: [선택 이유]
- 대안: [대안 방법] (이유: [])

### 3. 가정 점검 절차

#### 정규성 (Normality)
- **검정 방법**: Shapiro-Wilk test (N < 50) / K-S test (N ≥ 50)
- **시각화**: Q-Q plot, histogram
- **해석 기준**: p > .05 → 정규성 가정 충족
- **위반 시**: [비모수 대안] 또는 중심극한정리 적용 (N > 30)

#### 등분산성 (Homogeneity of Variance)
- **검정 방법**: Levene's test
- **해석 기준**: p > .05 → 등분산 가정 충족
- **위반 시**: Welch's t-test / Brown-Forsythe

#### 독립성 (Independence)
- **확인 방법**: 연구 설계 검토
- **위반 시**: 군집 분석, MLM 고려

#### 선형성 (Linearity) - 회귀분석 시
- **확인 방법**: 잔차 산점도
- **위반 시**: 변환, 다항회귀, 비선형 모형

#### 다중공선성 (Multicollinearity) - 다중회귀 시
- **검정 방법**: VIF (Variance Inflation Factor)
- **해석 기준**: VIF < 10 (또는 < 5 보수적)
- **위반 시**: 변수 제거, 중심화, 차원축소

### 4. 검정력 분석

#### 사전 분석 (A Priori)
- **기대 효과크기**: [d = / η² = / f² = ]
- **유의수준 (α)**: .05
- **검정력 (1-β)**: .80
- **필요 표본 크기**: **N = [계산값]**

#### 사후 분석 (Post Hoc)
- **현재 표본 크기**: N = [N]
- **관찰된 효과크기**: [값]
- **달성된 검정력**: [값]

### 5. 분석 실행 가이드

```r
# R 코드 예시
# 1. 데이터 로드
data <- read.csv("data.csv")

# 2. 가정 점검
shapiro.test(data$DV)
leveneTest(DV ~ Group, data = data)

# 3. 주 분석
model <- t.test(DV ~ Group, data = data)
# 또는
model <- aov(DV ~ Group, data = data)

# 4. 효과크기
library(effectsize)
cohens_d(DV ~ Group, data = data)
```

### 6. 효과크기 해석

| 효과크기 | 값 | 해석 (Cohen 기준) |
|----------|-----|-------------------|
| Cohen's d | [값] | Small/Medium/Large |
| η² | [값] | Small/Medium/Large |
| r | [값] | Small/Medium/Large |

**해석 기준:**
| 지표 | Small | Medium | Large |
|------|-------|--------|-------|
| d | 0.2 | 0.5 | 0.8 |
| η² | .01 | .06 | .14 |
| r | .10 | .30 | .50 |

### 7. 다중 비교 (해당 시)

**교정 방법**: [Bonferroni / Tukey / FDR]
- 비교 횟수: [k]
- 교정된 α: [α/k 또는 조정된 p-value]

### 8. 결과 보고 형식 (APA)

```
[분석 방법] 결과, [통계치 형식]은 통계적으로
[유의/유의하지 않]했다, [통계치 = X.XX, p = .XXX,
효과크기 = X.XX, 95% CI [X.XX, X.XX]].
```

**예시:**
"Independent samples t-test 결과, 두 집단 간 차이는
통계적으로 유의했다, t(98) = 2.45, p = .016,
d = 0.49, 95% CI [0.09, 0.89]."
```

## 프롬프트 템플릿

```
당신은 사회과학 통계 분석 전문가입니다.

다음 연구에 적합한 분석 방법을 안내해주세요:

[연구 질문]: {research_question}
[독립변수]: {iv} (유형: 연속/범주, 수준)
[종속변수]: {dv} (유형: 연속/범주, 수준)
[통제변수]: {covariates}
[설계]: {design}
[표본 크기]: {n}

수행할 작업:
1. 분석 방법 선택
   - 추천 방법 및 근거
   - 대안적 방법

2. 가정 점검 절차
   - 정규성 검정 (Shapiro-Wilk, Q-Q plot)
   - 등분산성 검정 (Levene's test)
   - 독립성 검정
   - 선형성 검정 (회귀 시)
   - 다중공선성 (VIF)
   - 가정 위반 시 대안

3. 검정력 분석
   - 기대 효과크기
   - 필요 표본 크기 (α=.05, power=.80)
   - 현재 표본의 검정력

4. 효과크기 해석 가이드
   - 적절한 효과크기 지표
   - Cohen의 해석 기준
   - 실무적 의미 해석

5. 다중 비교 이슈
   - 필요시 교정 방법 (Bonferroni, FDR 등)
```

## 분석 방법 선택 플로차트

```
종속변수 유형?
     │
     ├── 연속형
     │      │
     │      └── 독립변수 유형?
     │              │
     │              ├── 범주형 (2수준) → t-test
     │              ├── 범주형 (3+수준) → ANOVA
     │              └── 연속형 → Correlation/Regression
     │
     └── 범주형
            │
            └── 독립변수 유형?
                    │
                    ├── 범주형 → Chi-square
                    └── 연속형/혼합 → Logistic Regression
```

## 관련 에이전트

- **09-research-design-consultant**: 분석에 앞서 설계 확인
- **11-analysis-code-generator**: 분석 코드 생성
- **12-sensitivity-analysis-designer**: 강건성 검증

## 참고 자료

- Field, A. (2018). Discovering Statistics Using IBM SPSS Statistics
- Cohen, J. (1988). Statistical Power Analysis for the Behavioral Sciences
- Tabachnick & Fidell (2019). Using Multivariate Statistics
