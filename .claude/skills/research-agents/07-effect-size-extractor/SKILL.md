---
name: effect-size-extractor
description: |
  효과크기 추출기 - 연구 논문에서 다양한 형태의 통계치를 표준화된 효과크기로 변환
  Use when: extracting effect sizes, converting statistics, preparing meta-analysis data
  트리거: 효과크기, Cohen's d, Hedges' g, 상관계수, 변환, 메타분석 데이터
---

# 효과크기 추출기 (Effect Size Extractor)

**Agent ID**: 07
**Category**: B - 문헌 및 증거
**Icon**: 📊

## 개요

연구 논문에서 다양한 형태의 통계치를 표준화된 효과크기로 변환합니다.
메타분석에 필요한 효과크기와 분산/표준오차를 정확하게 계산합니다.

## 사용 시점

- 메타분석을 위한 데이터 추출 시
- 연구 간 효과 비교가 필요할 때
- 다양한 통계치를 표준화해야 할 때
- 효과크기 해석이 필요할 때

## 핵심 기능

1. **다양한 입력 처리**
   - 평균과 표준편차
   - t-value, F-value
   - 상관계수 (r)
   - 카이제곱, 오즈비
   - p-value와 표본크기

2. **효과크기 변환**
   - Cohen's d ↔ Hedges' g
   - d ↔ r
   - OR ↔ d
   - 다양한 상호 변환

3. **분산/표준오차 계산**
   - 메타분석 가중치용
   - 신뢰구간 계산

4. **의존성 처리**
   - 반복측정 설계
   - 군집 설계
   - 다중 결과변수

## 변환 공식 라이브러리

### 기본 효과크기 계산

**Cohen's d (독립 집단)**
```
d = (M₁ - M₂) / SD_pooled

SD_pooled = √[((n₁-1)SD₁² + (n₂-1)SD₂²) / (n₁ + n₂ - 2)]
```

**Hedges' g (소표본 교정)**
```
g = d × J

J = 1 - 3/(4(n₁ + n₂) - 9)
```

**Cohen's d (대응 집단)**
```
d = M_diff / SD_diff

또는

d = (M_pre - M_post) / SD_pooled × √(2(1-r))
```

### 변환 공식

**t → d**
```
d = t × √(1/n₁ + 1/n₂)
```

**F → d (2집단)**
```
d = √(F × (n₁ + n₂) / (n₁ × n₂))
```

**r → d**
```
d = 2r / √(1 - r²)
```

**d → r**
```
r = d / √(d² + 4)
```

**OR → d**
```
d = ln(OR) × √3 / π
```

**η² → d**
```
d = 2 × √(η² / (1 - η²))
```

**r → Fisher's z**
```
z = 0.5 × ln[(1 + r) / (1 - r)]
```

### 분산 계산

**d의 분산**
```
V_d = (n₁ + n₂)/(n₁ × n₂) + d²/(2(n₁ + n₂))
```

**r의 분산**
```
V_r = (1 - r²)² / (n - 1)
```

**Fisher's z의 분산**
```
V_z = 1 / (n - 3)
```

## 입력 요구사항

```yaml
필수:
  - 원 통계치: "보고된 통계 값"
  - 표본 크기: "각 집단 또는 전체 N"

선택:
  - 목표 효과크기: "d, r, OR 중 선택"
  - 연구 설계: "독립/대응/반복측정"
  - 사전-사후 상관: "대응 설계 시"
```

## 출력 형식

```markdown
## 효과크기 변환 보고서

### 1. 입력 정보

| 항목 | 값 |
|------|-----|
| 원 통계치 | [값] |
| 통계치 유형 | [t/F/r/χ²/M&SD 등] |
| n₁ | [값] |
| n₂ | [값] |
| 설계 유형 | [독립/대응] |

### 2. 변환 과정

**적용 공식:**
```
[공식 명시]
```

**계산 과정:**
```
Step 1: [중간 계산]
Step 2: [중간 계산]
...
최종: [결과]
```

### 3. 결과

| 효과크기 | 값 | SE | 95% CI |
|----------|-----|-----|--------|
| Cohen's d | [값] | [SE] | [lower, upper] |
| Hedges' g | [값] | [SE] | [lower, upper] |
| r | [값] | [SE] | [lower, upper] |

### 4. 해석

**Cohen (1988) 기준:**
- Small: d = 0.2, r = .10
- Medium: d = 0.5, r = .30
- Large: d = 0.8, r = .50

**본 연구 효과크기**: [Small/Medium/Large] 수준

### 5. 메타분석 입력 데이터

```csv
study_id, yi, vi, ni
[study], [effect], [variance], [n]
```
```

## 프롬프트 템플릿

```
당신은 메타분석 효과크기 계산 전문가입니다.

다음 통계치를 표준화된 효과크기로 변환해주세요:

[원 통계치]: {original_statistic}
[표본 크기]: {sample_size}
[목표 효과크기]: {target_es} (d, r, OR 중 선택)

수행할 작업:
1. 원 통계치 유형 식별
   - Cohen's d / Hedges' g
   - Pearson r
   - t-value
   - F-value (df1, df2 포함)
   - χ² (chi-square)
   - η² / η²_partial
   - Odds Ratio / Risk Ratio
   - 평균과 표준편차

2. 변환 수행
   - 적용할 공식 명시
   - 계산 과정 상세 기술
   - 중간 값 모두 표시

3. 분산/표준오차 계산
   - 효과크기의 표본 분산 공식
   - 메타분석 가중치 계산용

4. 95% 신뢰구간 계산

5. 결과 요약
   | 원 통계치 | 변환된 ES | SE | 95% CI |
```

## 효과크기 해석 기준

### Cohen (1988) 일반 기준
| 효과크기 | Small | Medium | Large |
|----------|-------|--------|-------|
| d | 0.2 | 0.5 | 0.8 |
| r | .10 | .30 | .50 |
| η² | .01 | .06 | .14 |
| OR | 1.5 | 2.5 | 4.0 |

### 분야별 기준 (교육/심리학)
| 중재 유형 | 평균 d | 기준 조정 |
|----------|--------|----------|
| 교육적 중재 | 0.40 | Small: 0.15, Med: 0.40, Large: 0.65 |
| 심리치료 | 0.50 | 일반 기준 적용 |
| 약물 치료 | 0.30 | Small: 0.10, Med: 0.30, Large: 0.50 |

## 특수 상황 처리

### 다중 처치군 (3+ groups)
- 쌍별 비교 vs. 통합 비교
- 분산 풀링 방법

### 반복 측정
- 사전-사후 상관 필요
- 의존성 교정

### 군집 설계
- 설계 효과 (Design Effect) 적용
- ICC 기반 교정

### 누락 정보 추정
- p-value에서 t 역산
- CI에서 SE 역산

## 관련 에이전트

- **05-systematic-literature-scout**: 연구 검색 및 수집
- **06-evidence-quality-appraiser**: 품질 평가
- **10-statistical-analysis-guide**: 메타분석 방법 안내

## 참고 자료

- Borenstein et al. (2009). Introduction to Meta-Analysis
- Cooper et al. (2019). Handbook of Research Synthesis
- Lipsey & Wilson (2001). Practical Meta-Analysis
- metafor R package documentation
