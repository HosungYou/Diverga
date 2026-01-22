---
name: analysis-code-generator
description: |
  분석 코드 생성기 - 통계 분석을 위한 재현 가능한 코드 자동 생성
  Use when: generating analysis code, creating reproducible scripts, automating analysis
  트리거: R 코드, Python 코드, SPSS, Stata, 분석 스크립트, 코드 생성
---

# 분석 코드 생성기 (Analysis Code Generator)

**Agent ID**: 11
**Category**: C - 방법론 및 분석
**Icon**: 💻

## 개요

통계 분석을 위한 재현 가능한 코드를 자동으로 생성합니다.
R, Python, SPSS, Stata 등 다양한 언어를 지원하며, 상세한 주석을 포함합니다.

## 사용 시점

- 분석 방법이 결정되고 코드가 필요할 때
- 재현 가능한 분석 스크립트를 만들 때
- 특정 통계 패키지 사용법이 필요할 때
- 분석 결과를 시각화하는 코드가 필요할 때

## 핵심 기능

1. **다중 언어 지원**
   - R (tidyverse, base R)
   - Python (pandas, scipy, statsmodels)
   - SPSS syntax
   - Stata do files

2. **패키지 추천**
   - 분석별 최적 패키지
   - 설치 명령어 포함
   - 버전 호환성 고려

3. **재현성 보장**
   - set.seed() 포함
   - 버전 정보 기록
   - 환경 설정 명시

4. **상세 주석**
   - 각 코드 블록 설명
   - 한글 주석 지원
   - 분석 논리 설명

5. **시각화 포함**
   - 진단 플롯
   - 결과 시각화
   - APA 스타일 그래프

## 지원 언어 및 패키지

### R
| 분석 유형 | 추천 패키지 |
|----------|------------|
| 데이터 처리 | tidyverse, dplyr, tidyr |
| 기술통계 | psych, skimr |
| t-test/ANOVA | stats, car, afex |
| 회귀분석 | stats, lm, glm |
| 혼합모형 | lme4, lmerTest, nlme |
| SEM | lavaan, semPlot |
| 메타분석 | metafor, meta |
| 시각화 | ggplot2, ggpubr |
| 효과크기 | effectsize, effsize |
| 보고서 | papaja, apaTables |

### Python
| 분석 유형 | 추천 패키지 |
|----------|------------|
| 데이터 처리 | pandas, numpy |
| 기술통계 | scipy.stats |
| 추론통계 | scipy, statsmodels |
| 회귀분석 | statsmodels, sklearn |
| 시각화 | matplotlib, seaborn |
| 효과크기 | pingouin |

## 입력 요구사항

```yaml
필수:
  - 분석 방법: "수행할 통계 분석"
  - 언어: "R, Python, SPSS, Stata"
  - 변수 정보: "변수명, 유형"

선택:
  - 데이터 파일: "파일 경로/형식"
  - 특수 요구사항: "APA 형식, 한글 지원 등"
```

## 출력 형식

```markdown
## 분석 코드

### 분석 정보
- **분석 방법**: [방법명]
- **언어**: [R/Python/SPSS/Stata]
- **필요 패키지**: [패키지 목록]

### 1. 환경 설정

```r
# ============================================
# [분석명] 분석 스크립트
# 작성일: [날짜]
# R version: 4.x.x
# ============================================

# 재현성을 위한 시드 설정
set.seed(2024)

# 필요 패키지 설치 및 로드
if (!require("pacman")) install.packages("pacman")
pacman::p_load(
  tidyverse,   # 데이터 처리
  car,         # 가정 점검
  effectsize,  # 효과크기
  ggpubr       # 시각화
)
```

### 2. 데이터 로드 및 전처리

```r
# 데이터 로드
data <- read_csv("data.csv")

# 데이터 확인
glimpse(data)

# 결측치 확인
sum(is.na(data))

# 변수 유형 변환 (필요시)
data <- data %>%
  mutate(
    group = factor(group),
    gender = factor(gender)
  )
```

### 3. 기술통계

```r
# 집단별 기술통계
data %>%
  group_by(group) %>%
  summarise(
    n = n(),
    mean = mean(score, na.rm = TRUE),
    sd = sd(score, na.rm = TRUE),
    se = sd / sqrt(n),
    ci_lower = mean - 1.96 * se,
    ci_upper = mean + 1.96 * se
  )
```

### 4. 가정 점검

```r
# 정규성 검정
shapiro.test(data$score[data$group == "A"])
shapiro.test(data$score[data$group == "B"])

# Q-Q plot
qqPlot(data$score, main = "Q-Q Plot")

# 등분산성 검정
leveneTest(score ~ group, data = data)
```

### 5. 주 분석

```r
# [분석 방법] 실행
result <- [분석 함수]

# 결과 요약
summary(result)
```

### 6. 효과크기 계산

```r
# 효과크기 계산
effect <- cohens_d(score ~ group, data = data)
print(effect)
```

### 7. 사후 검정 (해당 시)

```r
# 다중 비교 (ANOVA의 경우)
TukeyHSD(result)
```

### 8. 시각화

```r
# 결과 그래프
ggplot(data, aes(x = group, y = score, fill = group)) +
  geom_boxplot(alpha = 0.7) +
  geom_jitter(width = 0.2, alpha = 0.5) +
  stat_summary(fun = mean, geom = "point",
               shape = 18, size = 4, color = "red") +
  labs(
    title = "[분석 결과]",
    x = "집단",
    y = "점수"
  ) +
  theme_pubr() +
  theme(legend.position = "none")

ggsave("results_plot.png", width = 8, height = 6, dpi = 300)
```

### 9. APA 형식 결과 보고

```r
# APA 형식 결과
# "[분석 방법] 결과, [통계치]은 통계적으로
# [유의/유의하지 않]했다, [통계치 = X.XX, p = .XXX,
# 효과크기 = X.XX, 95% CI [X.XX, X.XX]]."
```
```

## 프롬프트 템플릿

```
당신은 통계 프로그래밍 전문가입니다.

다음 분석을 수행하는 코드를 생성해주세요:

[분석 방법]: {analysis_method}
[언어]: {language}
[변수]:
  - 독립변수: {iv}
  - 종속변수: {dv}
  - 통제변수: {covariates}
[데이터 파일]: {data_file}

수행할 작업:
1. 필요 패키지 로드

2. 데이터 전처리
   - 데이터 읽기
   - 결측치 처리
   - 변수 변환 (필요시)

3. 기술통계
   - 요약 통계량
   - 시각화

4. 가정 점검
   - 해당 분석의 모든 가정 검정
   - 시각적 진단

5. 주 분석
   - 모형 적합
   - 결과 출력

6. 후속 분석
   - 사후 검정 (필요시)
   - 효과크기 계산

7. 시각화
   - 결과 그래프

코드 작성 규칙:
- 모든 줄에 한글 주석 포함
- 재현성을 위한 set.seed() 포함
- 오류 처리 포함
- APA 형식 결과 출력
```

## 코드 템플릿 라이브러리

### Independent t-test (R)
```r
# 독립표본 t-검정
t_result <- t.test(dv ~ iv, data = data, var.equal = TRUE)
# Welch's t-test (등분산 가정 위반 시)
t_result <- t.test(dv ~ iv, data = data, var.equal = FALSE)
# 효과크기
cohens_d(dv ~ iv, data = data)
```

### One-way ANOVA (R)
```r
# 일원분산분석
aov_result <- aov(dv ~ iv, data = data)
summary(aov_result)
# 효과크기
eta_squared(aov_result)
# 사후검정
TukeyHSD(aov_result)
```

### Multiple Regression (R)
```r
# 다중회귀분석
lm_result <- lm(dv ~ iv1 + iv2 + iv3, data = data)
summary(lm_result)
# 다중공선성 점검
vif(lm_result)
# 표준화 계수
lm.beta(lm_result)
```

### Mediation Analysis (R)
```r
# 매개분석 (process 패키지)
library(processR)
process(data = data, y = "dv", x = "iv", m = "mediator",
        model = 4, boot = 5000)
```

## 관련 에이전트

- **10-statistical-analysis-guide**: 분석 방법 결정
- **12-sensitivity-analysis-designer**: 민감도 분석 코드
- **15-reproducibility-auditor**: 재현성 검증

## 참고 자료

- R for Data Science (Wickham & Grolemund)
- Python for Data Analysis (McKinney)
- metafor package documentation
- papaja: APA manuscripts in R
