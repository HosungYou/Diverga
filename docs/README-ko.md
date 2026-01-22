# Research Coordinator - 사회과학 연구 에이전트 시스템

## 목차

1. [소개](#소개)
2. [시스템 구성](#시스템-구성)
3. [에이전트 카테고리](#에이전트-카테고리)
4. [설치 방법](#설치-방법)
5. [사용 방법](#사용-방법)
6. [자동 트리거 시스템](#자동-트리거-시스템)
7. [병렬 실행](#병렬-실행)
8. [FAQ](#faq)

---

## 소개

**Research Coordinator**는 사회과학 연구자를 위한 20개의 전문 AI 에이전트를 제공하는 Claude Code Skills 시스템입니다. 연구의 전체 생애주기를 지원합니다:

- **아이디어 구체화**: 연구 질문 정제, 이론적 프레임워크 설계
- **문헌 검토**: 체계적 검색, 품질 평가, 근거 종합
- **연구 설계**: 방법론 선택, 표본 크기 계산, 분석 계획
- **품질 검증**: 편향 탐지, 일관성 점검, 재현성 감사
- **출판 준비**: 저널 매칭, 초록 작성, 리뷰어 대응

### 핵심 특징

1. **자동 맥락 인식**: 대화 내용을 분석하여 적절한 에이전트 자동 선택
2. **병렬 실행 지원**: 관련 에이전트들의 동시 실행으로 효율성 극대화
3. **표준 가이드라인 내장**: PRISMA, CONSORT, STROBE, APA 7 등 준수
4. **다국어 지원**: 한국어/영어 연구 모두 지원

---

## 시스템 구성

```
research-coordinator/
├── .claude/skills/
│   ├── research-coordinator/           # 마스터 코디네이터
│   │   └── SKILL.md
│   └── research-agents/                # 20개 전문 에이전트
│       ├── 01-research-question-refiner/
│       ├── 02-theoretical-framework-architect/
│       ├── 03-devils-advocate/
│       ├── 04-research-ethics-advisor/
│       ├── 05-systematic-literature-scout/
│       ├── 06-evidence-quality-appraiser/
│       ├── 07-effect-size-extractor/
│       ├── 08-research-radar/
│       ├── 09-research-design-consultant/
│       ├── 10-statistical-analysis-guide/
│       ├── 11-analysis-code-generator/
│       ├── 12-sensitivity-analysis-designer/
│       ├── 13-internal-consistency-checker/
│       ├── 14-checklist-manager/
│       ├── 15-reproducibility-auditor/
│       ├── 16-bias-detector/
│       ├── 17-journal-matcher/
│       ├── 18-academic-communicator/
│       ├── 19-peer-review-strategist/
│       └── 20-preregistration-composer/
├── docs/
├── scripts/
└── README.md
```

---

## 에이전트 카테고리

### Category A: 이론 및 연구 설계 (01-04)

| ID | 에이전트명 | 주요 기능 |
|----|-----------|----------|
| 01 | **연구 질문 정제기** | PICO/SPIDER 프레임워크로 연구 질문 구체화 |
| 02 | **이론적 프레임워크 설계자** | 이론 지도 작성, 개념적 모델 구축 |
| 03 | **악마의 옹호자** | 비판적 검토, 약점 식별, Reviewer 2 시뮬레이션 |
| 04 | **연구 윤리 자문관** | IRB 준비, 윤리적 고려사항, 동의서 검토 |

### Category B: 문헌 및 증거 (05-08)

| ID | 에이전트명 | 주요 기능 |
|----|-----------|----------|
| 05 | **체계적 문헌 탐색자** | PRISMA 기반 검색 전략, 데이터베이스 선정 |
| 06 | **증거 품질 평가자** | RoB 2.0, NOS, GRADE 평가 |
| 07 | **효과크기 추출기** | 효과크기 계산 및 변환, 메타분석 데이터 추출 |
| 08 | **최신 연구 레이더** | 최신 동향 모니터링, 핵심 논문 식별 |

### Category C: 방법론 및 분석 (09-12)

| ID | 에이전트명 | 주요 기능 |
|----|-----------|----------|
| 09 | **연구 설계 컨설턴트** | 연구 설계 선택, 타당도 위협 분석 |
| 10 | **통계 분석 가이드** | 분석 방법 선택, 가정 점검, 해석 지원 |
| 11 | **분석 코드 생성기** | R/Python/SPSS/Stata 코드 생성 |
| 12 | **민감도 분석 설계자** | 민감도 분석 설계, 강건성 검증 |

### Category D: 품질 및 검증 (13-16)

| ID | 에이전트명 | 주요 기능 |
|----|-----------|----------|
| 13 | **내적 일관성 검증자** | 논문 내 수치/진술 일관성 점검 |
| 14 | **체크리스트 관리자** | PRISMA/CONSORT/STROBE 등 준수 검토 |
| 15 | **재현성 감사자** | Open Science 수준 평가, 재현성 점검 |
| 16 | **편향 탐지기** | p-hacking, HARKing, 선택적 보고 탐지 |

### Category E: 출판 및 커뮤니케이션 (17-20)

| ID | 에이전트명 | 주요 기능 |
|----|-----------|----------|
| 17 | **저널 매칭 전문가** | 타겟 저널 선정, 투고 전략 수립 |
| 18 | **학술 커뮤니케이터** | 초록, plain language 요약, SNS 콘텐츠 |
| 19 | **피어 리뷰 대응 전략가** | 심사평 분석, 회신문 작성 |
| 20 | **사전등록 문서 작성자** | OSF/AsPredicted 사전등록 문서 |

---

## 설치 방법

### 자동 설치 (권장)

```bash
git clone https://github.com/HosungYou/research-coordinator.git
cd research-coordinator
./scripts/install.sh
```

### 수동 설치

```bash
# 1. 레포지토리 클론
git clone https://github.com/HosungYou/research-coordinator.git

# 2. 심볼릭 링크 생성
mkdir -p ~/.claude/skills
ln -sf "$(pwd)/.claude/skills/research-coordinator" ~/.claude/skills/
ln -sf "$(pwd)/.claude/skills/research-agents" ~/.claude/skills/
```

### 설치 확인

```bash
ls -la ~/.claude/skills/research-coordinator/
ls -la ~/.claude/skills/research-agents/
```

---

## 사용 방법

### 1. 마스터 코디네이터 호출

```
/research-coordinator
```

마스터 코디네이터는 대화 맥락을 분석하여 적절한 에이전트를 자동 선택합니다.

### 2. 개별 에이전트 직접 호출

특정 에이전트가 필요한 경우 직접 호출:

```
/research-question-refiner
/theoretical-framework-architect
/devils-advocate
/statistical-analysis-guide
/journal-matcher
```

### 3. 자연어 트리거

특정 키워드가 포함된 메시지를 작성하면 자동으로 해당 에이전트 활성화:

```
"연구 질문을 더 구체적으로 다듬고 싶어요"
→ 01-research-question-refiner 자동 활성화

"메타분석을 위한 효과크기를 계산해야 해요"
→ 07-effect-size-extractor 자동 활성화
```

---

## 자동 트리거 시스템

### 키워드 매핑 테이블

| 키워드 | 트리거되는 에이전트 |
|--------|---------------------|
| 연구 질문, research question, PICO, SPIDER | 01-research-question-refiner |
| 이론적 프레임워크, theoretical framework, conceptual model | 02-theoretical-framework-architect |
| 비판, 약점, Reviewer 2, 반론 | 03-devils-advocate |
| 윤리, IRB, 동의서, 개인정보 | 04-research-ethics-advisor |
| 문헌 검색, PRISMA, 체계적 리뷰 | 05-systematic-literature-scout |
| 품질 평가, RoB, GRADE | 06-evidence-quality-appraiser |
| 효과크기, Cohen's d, OR, effect size | 07-effect-size-extractor |
| 최신 연구, 트렌드, 핵심 논문 | 08-research-radar |
| 연구 설계, RCT, 준실험 | 09-research-design-consultant |
| 통계 분석, ANOVA, 회귀, SEM | 10-statistical-analysis-guide |
| R 코드, Python, SPSS | 11-analysis-code-generator |
| 민감도 분석, robustness | 12-sensitivity-analysis-designer |
| 일관성, 수치 검증 | 13-internal-consistency-checker |
| 체크리스트, CONSORT, STROBE | 14-checklist-manager |
| 재현성, OSF, Open Science | 15-reproducibility-auditor |
| 편향, p-hacking, HARKing | 16-bias-detector |
| 저널, 투고, Impact Factor | 17-journal-matcher |
| 초록, plain language, 요약 | 18-academic-communicator |
| 리뷰어, 수정 요청, response letter | 19-peer-review-strategist |
| 사전등록, preregistration | 20-preregistration-composer |

---

## 병렬 실행

관련된 에이전트들을 동시에 실행하여 효율성을 높일 수 있습니다.

### 사전 정의된 병렬 그룹

```
그룹 1 - 초기 설계: 01 + 02 + 03
그룹 2 - 문헌 검토: 05 + 06 + 08
그룹 3 - 분석 설계: 09 + 10 + 12
그룹 4 - 품질 검증: 13 + 14 + 15 + 16
그룹 5 - 출판 준비: 17 + 18 + 19
```

### 예시

```
"메타분석 논문을 준비하고 있는데, 검색 전략부터 품질 평가까지 검토해주세요"
→ 05 + 06 + 07 병렬 실행
```

---

## FAQ

### Q: 어떤 연구 분야에 적합한가요?

A: 사회과학 전반에 적합합니다:
- 교육학
- 심리학
- 경영학 (HRD, 조직심리)
- 사회학
- 커뮤니케이션학

### Q: 양적 연구만 지원하나요?

A: 아닙니다. 양적, 질적, 혼합 방법 연구 모두 지원합니다. 다만 현재 버전은 양적 연구 분석 도구가 더 풍부합니다.

### Q: 영어 논문도 지원하나요?

A: 네, 한국어와 영어 모두 완벽히 지원합니다. 저널 매칭, 초록 작성, 리뷰어 대응 등 모든 기능이 이중 언어로 제공됩니다.

### Q: 에이전트를 커스터마이징할 수 있나요?

A: 네, 각 SKILL.md 파일을 수정하여 프롬프트 템플릿, 출력 형식 등을 커스터마이징할 수 있습니다.

### Q: 제거하려면?

A:
```bash
./scripts/uninstall.sh
```

---

## 지원 및 기여

- **GitHub Issues**: 버그 리포트 및 기능 요청
- **Pull Requests**: 기여 환영

---

## 라이센스

MIT License - 자유롭게 사용, 수정, 배포 가능
