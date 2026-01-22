# Research Coordinator 에이전트 참조 문서

## 전체 에이전트 목록

| ID | 이름 | 카테고리 | 아이콘 | 슬래시 명령어 |
|----|------|----------|--------|---------------|
| 01 | Research Question Refiner | A - 이론/설계 | 🔬 | `/research-question-refiner` |
| 02 | Theoretical Framework Architect | A - 이론/설계 | 🏛️ | `/theoretical-framework-architect` |
| 03 | Devil's Advocate | A - 이론/설계 | 😈 | `/devils-advocate` |
| 04 | Research Ethics Advisor | A - 이론/설계 | ⚖️ | `/research-ethics-advisor` |
| 05 | Systematic Literature Scout | B - 문헌/증거 | 📚 | `/systematic-literature-scout` |
| 06 | Evidence Quality Appraiser | B - 문헌/증거 | ⭐ | `/evidence-quality-appraiser` |
| 07 | Effect Size Extractor | B - 문헌/증거 | 📊 | `/effect-size-extractor` |
| 08 | Research Radar | B - 문헌/증거 | 📡 | `/research-radar` |
| 09 | Research Design Consultant | C - 방법론/분석 | 🎯 | `/research-design-consultant` |
| 10 | Statistical Analysis Guide | C - 방법론/분석 | 📈 | `/statistical-analysis-guide` |
| 11 | Analysis Code Generator | C - 방법론/분석 | 💻 | `/analysis-code-generator` |
| 12 | Sensitivity Analysis Designer | C - 방법론/분석 | 🔍 | `/sensitivity-analysis-designer` |
| 13 | Internal Consistency Checker | D - 품질/검증 | ✅ | `/internal-consistency-checker` |
| 14 | Checklist Manager | D - 품질/검증 | 📋 | `/checklist-manager` |
| 15 | Reproducibility Auditor | D - 품질/검증 | 🔄 | `/reproducibility-auditor` |
| 16 | Bias Detector | D - 품질/검증 | ⚠️ | `/bias-detector` |
| 17 | Journal Matcher | E - 출판/커뮤니케이션 | 📝 | `/journal-matcher` |
| 18 | Academic Communicator | E - 출판/커뮤니케이션 | 🎤 | `/academic-communicator` |
| 19 | Peer Review Strategist | E - 출판/커뮤니케이션 | 🔄 | `/peer-review-strategist` |
| 20 | Pre-registration Composer | E - 출판/커뮤니케이션 | 📄 | `/preregistration-composer` |

---

## Category A: 이론 및 연구 설계

### 01. Research Question Refiner (연구 질문 정제기) 🔬

**목적**: 모호한 연구 아이디어를 구체적이고 검증 가능한 연구 질문으로 발전

**트리거 키워드**: 연구 질문, research question, PICO, SPIDER, 질문 정제

**핵심 기능**:
- PICO (양적) / SPIDER (질적) 프레임워크 적용
- 좁은/중간/넓은 범위 옵션 제공
- 검증 가능성 평가

**입력 요구사항**:
```yaml
필수:
  - 초기 아이디어: "연구하고 싶은 주제"
선택:
  - 연구 유형: "양적/질적/혼합"
  - 분야: "교육/심리/경영 등"
```

**출력 형식**: PICO/SPIDER 분석표 + 3개 수준의 정제된 질문 옵션

---

### 02. Theoretical Framework Architect (이론적 프레임워크 설계자) 🏛️

**목적**: 이론적 토대를 체계화하고 개념적 모델 구축

**트리거 키워드**: 이론적 프레임워크, theoretical framework, conceptual model, 이론 통합

**핵심 기능**:
- 이론 지도(Theory Map) 작성
- 개념적 모델 시각화
- 가설 도출 논리 구조화

**입력 요구사항**:
```yaml
필수:
  - 연구 질문: "정제된 연구 질문"
선택:
  - 관련 이론: "알고 있는 이론들"
  - 핵심 변수: "주요 변수들"
```

**출력 형식**: 이론 비교표 + 통합 개념 모델 다이어그램 + 가설 체계

---

### 03. Devil's Advocate (악마의 옹호자) 😈

**목적**: 연구의 약점과 잠재적 비판을 사전에 식별

**트리거 키워드**: 비판, 약점, Reviewer 2, 반론, 대안 설명

**핵심 기능**:
- 타당도 위협 식별
- Reviewer 2 시뮬레이션
- 대안 설명 제시

**입력 요구사항**:
```yaml
필수:
  - 연구 설계: "계획 또는 완료된 연구 설명"
선택:
  - 주요 발견: "예비 결과"
```

**출력 형식**: 타당도 위협 매트릭스 + 모의 심사평 + 대응 전략

---

### 04. Research Ethics Advisor (연구 윤리 자문관) ⚖️

**목적**: 윤리적 연구 수행을 위한 가이드 제공

**트리거 키워드**: 윤리, IRB, 동의서, 개인정보, 취약계층, informed consent

**핵심 기능**:
- Belmont Report 원칙 점검
- IRB 신청서 준비 지원
- 동의서 템플릿 제공

**입력 요구사항**:
```yaml
필수:
  - 연구 설계: "연구 방법 개요"
  - 참가자 특성: "대상자 정보"
선택:
  - 데이터 유형: "수집 데이터 종류"
```

**출력 형식**: 윤리 점검 체크리스트 + 위험 평가 + IRB 신청 가이드

---

## Category B: 문헌 및 증거

### 05. Systematic Literature Scout (체계적 문헌 탐색자) 📚

**목적**: PRISMA 기반 체계적 문헌 검색 전략 수립

**트리거 키워드**: 문헌 검색, PRISMA, 체계적 리뷰, systematic review, 검색 전략

**핵심 기능**:
- 데이터베이스 선정 가이드
- 검색식 작성 (Boolean, PCC)
- 포함/배제 기준 설정

**입력 요구사항**:
```yaml
필수:
  - 연구 질문: "체계적 리뷰 질문"
선택:
  - 분야: "학문 영역"
  - 제한 조건: "언어, 기간 등"
```

**출력 형식**: 데이터베이스별 검색식 + 선정 기준표 + PRISMA 플로우 초안

---

### 06. Evidence Quality Appraiser (증거 품질 평가자) ⭐

**목적**: 개별 연구의 방법론적 품질 평가

**트리거 키워드**: 품질 평가, RoB, GRADE, bias risk, 방법론 평가

**핵심 기능**:
- RoB 2.0 (RCT), ROBINS-I (비무작위)
- NOS (관찰 연구)
- GRADE 근거 수준

**입력 요구사항**:
```yaml
필수:
  - 연구 정보: "평가할 연구의 방법론 정보"
선택:
  - 연구 유형: "RCT/관찰/질적"
```

**출력 형식**: 품질 평가 체크리스트 + 영역별 판정 + 전체 품질 등급

---

### 07. Effect Size Extractor (효과크기 추출기) 📊

**목적**: 다양한 통계량에서 효과크기 계산 및 변환

**트리거 키워드**: 효과크기, effect size, Cohen's d, OR, 상관, 메타분석 데이터

**핵심 기능**:
- 32+ 통계량 변환 지원
- 신뢰구간, 분산 계산
- 메타분석용 데이터 형식화

**입력 요구사항**:
```yaml
필수:
  - 통계량: "보고된 통계 (t, F, r, p, 평균/SD 등)"
선택:
  - 표본 크기: "n1, n2"
  - 목표 효과크기: "d, g, r, OR"
```

**출력 형식**: 변환 결과 + 공식 + 해석 가이드 + 메타분석용 테이블

---

### 08. Research Radar (최신 연구 레이더) 📡

**목적**: 연구 동향 파악 및 핵심 논문 식별

**트리거 키워드**: 최신 연구, 트렌드, 핵심 논문, 인용, seminal work

**핵심 기능**:
- 인용 네트워크 분석
- 시계열 트렌드
- 핫토픽 식별

**입력 요구사항**:
```yaml
필수:
  - 연구 주제: "모니터링할 분야"
선택:
  - 기간: "관심 기간"
  - 핵심 저자: "추적할 연구자"
```

**출력 형식**: 핵심 논문 목록 + 트렌드 그래프 + 연구 갭 분석

---

## Category C: 방법론 및 분석

### 09. Research Design Consultant (연구 설계 컨설턴트) 🎯

**목적**: 최적의 연구 설계 선택 및 타당도 확보

**트리거 키워드**: 연구 설계, RCT, 준실험, 조사 설계, 실험 설계

**핵심 기능**:
- 설계 유형 결정 트리
- 타당도 위협 분석
- 통제 전략 권장

**입력 요구사항**:
```yaml
필수:
  - 연구 질문: "검증할 질문"
  - 제약 조건: "시간, 예산, 접근성"
선택:
  - 변수: "IV, DV, 통제변수"
```

**출력 형식**: 설계 비교표 + 권장 설계 + 타당도 매트릭스

---

### 10. Statistical Analysis Guide (통계 분석 가이드) 📈

**목적**: 적절한 통계 방법 선택 및 가정 점검

**트리거 키워드**: 통계 분석, ANOVA, 회귀, t-test, SEM, 다층모형

**핵심 기능**:
- 분석 방법 결정 트리
- 가정 점검 절차
- 결과 해석 가이드

**입력 요구사항**:
```yaml
필수:
  - 연구 질문: "분석 목적"
  - 변수 정보: "유형, 수준, 분포"
선택:
  - 데이터 구조: "독립/종속, 다층 등"
```

**출력 형식**: 분석 방법 비교 + 선택 근거 + 가정 점검 체크리스트

---

### 11. Analysis Code Generator (분석 코드 생성기) 💻

**목적**: 재현 가능한 분석 코드 생성

**트리거 키워드**: R 코드, Python, SPSS, Stata, 분석 코드

**핵심 기능**:
- R / Python / SPSS / Stata 지원
- 주석 포함 코드
- 결과 시각화 코드

**입력 요구사항**:
```yaml
필수:
  - 분석 방법: "수행할 분석"
  - 변수명: "데이터셋 변수명"
선택:
  - 소프트웨어: "R/Python/SPSS/Stata"
  - 데이터 형식: "wide/long"
```

**출력 형식**: 실행 가능한 코드 + 주석 + 결과 해석 가이드

---

### 12. Sensitivity Analysis Designer (민감도 분석 설계자) 🔍

**목적**: 결과의 강건성 검증 전략 수립

**트리거 키워드**: 민감도 분석, robustness, 강건성, sensitivity, 사양 곡선

**핵심 기능**:
- 분석적 결정 식별
- 다중우주 분석 설계
- 사양 곡선 분석

**입력 요구사항**:
```yaml
필수:
  - 주 분석: "기본 분석 방법과 결과"
선택:
  - 분석적 결정: "선택한 옵션들"
```

**출력 형식**: 분석 결정 매트릭스 + 민감도 분석 계획 + 결과 요약 템플릿

---

## Category D: 품질 및 검증

### 13. Internal Consistency Checker (내적 일관성 검증자) ✅

**목적**: 논문 내 수치와 진술의 일관성 점검

**트리거 키워드**: 일관성, 수치 검증, 오류 점검, 정합성

**핵심 기능**:
- 숫자 일관성 검증
- 통계적 계산 확인
- 논리적 모순 탐지

**입력 요구사항**:
```yaml
필수:
  - 원고: "점검할 문서"
선택:
  - 데이터: "원시 데이터 (확인용)"
```

**출력 형식**: 불일치 목록 + 위치 + 수정 제안

---

### 14. Checklist Manager (체크리스트 관리자) 📋

**목적**: 보고 가이드라인 준수 점검

**트리거 키워드**: 체크리스트, PRISMA, CONSORT, STROBE, ARRIVE, 보고 가이드라인

**핵심 기능**:
- PRISMA 2020 (체계적 리뷰)
- CONSORT (RCT)
- STROBE (관찰연구)
- APA 7 스타일

**입력 요구사항**:
```yaml
필수:
  - 연구 유형: "RCT/관찰/리뷰/질적"
  - 원고: "점검할 문서"
```

**출력 형식**: 항목별 체크 + 누락 항목 + 수정 제안

---

### 15. Reproducibility Auditor (재현성 감사자) 🔄

**목적**: Open Science 원칙 준수 및 재현성 평가

**트리거 키워드**: 재현성, reproducibility, OSF, Open Science, 데이터 공유

**핵심 기능**:
- 5단계 재현성 수준 평가
- OSF 프로젝트 구조 가이드
- 코드/데이터 공유 체크

**입력 요구사항**:
```yaml
필수:
  - 연구 정보: "연구 설계 및 분석 정보"
선택:
  - 공유 계획: "데이터/코드 공개 여부"
```

**출력 형식**: 재현성 수준 평가 + 개선 권장사항 + OSF 구조 템플릿

---

### 16. Bias Detector (편향 탐지기) ⚠️

**목적**: 연구 과정의 다양한 편향 식별

**트리거 키워드**: 편향, bias, p-hacking, HARKing, 선택적 보고

**핵심 기능**:
- p-hacking 탐지
- HARKing 식별
- 선택적 보고 점검

**입력 요구사항**:
```yaml
필수:
  - 연구 설계: "설계 및 분석 정보"
선택:
  - 결과: "보고된 결과"
  - 사전등록: "사전등록 내용 (있는 경우)"
```

**출력 형식**: 편향 유형별 위험도 + 증거 + 완화 전략

---

## Category E: 출판 및 커뮤니케이션

### 17. Journal Matcher (저널 매칭 전문가) 📝

**목적**: 연구에 최적화된 타겟 저널 식별

**트리거 키워드**: 저널, journal, 투고, Impact Factor, 출판

**핵심 기능**:
- 범위 적합성 분석
- 영향력 지표 비교
- 투고 전략 수립

**입력 요구사항**:
```yaml
필수:
  - 연구 초록: "연구 내용 요약"
  - 분야: "학문 영역"
선택:
  - 우선순위: "IF vs. 속도 vs. OA"
```

**출력 형식**: 저널 비교표 + 순차적 투고 계획 + 커버레터 템플릿

---

### 18. Academic Communicator (학술 커뮤니케이터) 🎤

**목적**: 다양한 청중을 위한 연구 커뮤니케이션 자료 생성

**트리거 키워드**: 초록, abstract, plain language, 요약, SNS, 프레스릴리즈

**핵심 기능**:
- 학술 초록 (IMRAD)
- Plain language summary
- 프레스 릴리즈
- SNS 콘텐츠

**입력 요구사항**:
```yaml
필수:
  - 연구 결과: "주요 발견 요약"
선택:
  - 타겟 청중: "동료/정책/대중/언론"
  - 형식: "초록/요약/SNS"
```

**출력 형식**: 청중별 맞춤 콘텐츠 패키지

---

### 19. Peer Review Strategist (피어 리뷰 대응 전략가) 🔄

**목적**: 심사평에 대한 효과적인 대응 전략 수립

**트리거 키워드**: 리뷰어, reviewer, 수정 요청, response letter, 회신문

**핵심 기능**:
- 코멘트 분류 및 우선순위
- 대응 전략 수립
- 회신문 작성

**입력 요구사항**:
```yaml
필수:
  - 심사평: "리뷰어 코멘트"
선택:
  - 원고: "현재 원고"
  - 결정: "Major/Minor/Reject"
```

**출력 형식**: 코멘트 분석표 + 대응 전략 + Point-by-point 회신문

---

### 20. Pre-registration Composer (사전등록 문서 작성자) 📄

**목적**: 연구 사전등록 문서 작성 지원

**트리거 키워드**: 사전등록, preregistration, OSF, AsPredicted, registered report

**핵심 기능**:
- OSF Prereg 템플릿
- AsPredicted 형식
- Registered Report 지원

**입력 요구사항**:
```yaml
필수:
  - 연구 계획: "연구 설계 및 분석 계획"
선택:
  - 플랫폼: "OSF/AsPredicted"
  - 유형: "표준/Registered Report"
```

**출력 형식**: 플랫폼별 사전등록 문서 + 체크리스트 + 타임라인

---

## 에이전트 간 연계

### 권장 워크플로우

```
연구 초기:
01 → 02 → 03 → 04

문헌 검토:
05 → 06 → 07 → 08

연구 수행:
09 → 10 → 11 → 12

품질 검증:
13 → 14 → 15 → 16

출판 준비:
17 → 18 → 19 (→ 20 if 사전등록 필요)
```

### 병렬 실행 가능 조합

| 그룹 | 에이전트 | 상황 |
|------|----------|------|
| 초기 설계 | 01 + 02 + 03 | 연구 계획 단계 |
| 문헌 검토 | 05 + 06 + 08 | 체계적 리뷰 |
| 메타분석 | 05 + 06 + 07 | 메타분석 데이터 수집 |
| 분석 설계 | 09 + 10 + 12 | 분석 계획 |
| 품질 검증 | 13 + 14 + 15 + 16 | 투고 전 점검 |
| 출판 준비 | 17 + 18 + 19 | 투고 준비 |

---

## 버전 정보

- **버전**: 1.0.0
- **최종 업데이트**: 2025-01-22
- **호환성**: Claude Code Skills System

## 기여 및 피드백

- [GitHub Issues](https://github.com/HosungYou/research-coordinator/issues)
