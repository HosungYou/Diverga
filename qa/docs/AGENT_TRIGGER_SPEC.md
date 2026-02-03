# Diverga Agent Trigger Specification

## 개요

Diverga는 40개의 전문 에이전트를 키워드 기반으로 자동 호출합니다.

---

## 에이전트 호출 방식

### Task Tool 호출 패턴

```python
Task(
    subagent_type="diverga:<agent_id>",
    model="<opus|sonnet|haiku>",
    prompt="<research context + specific task>"
)
```

### 예시

```python
Task(
    subagent_type="diverga:c5",
    model="opus",
    prompt="""
    User wants to conduct a meta-analysis on AI-powered tutoring.

    Task: Design meta-analysis methodology with:
    1. Effect size selection (Hedges' g recommended)
    2. Model selection (random-effects)
    3. Heterogeneity assessment strategy
    4. Publication bias detection methods

    Present 3 VS options with T-Scores.
    """
)
```

---

## 전체 에이전트 트리거 맵

### Category A: Foundation (6 agents)

| Agent ID | 이름 | 트리거 키워드 (EN) | 트리거 키워드 (KR) | Model |
|----------|------|-------------------|-------------------|-------|
| `diverga:a1` | ResearchQuestionRefiner | research question, RQ, refine | 연구 질문, 연구문제 | opus |
| `diverga:a2` | TheoreticalFrameworkArchitect | theoretical framework, theory, conceptual model | 이론적 프레임워크, 이론적 틀 | opus |
| `diverga:a3` | DevilsAdvocate | devil's advocate, critique, counterargument | 반론, 비판적 검토 | opus |
| `diverga:a4` | ResearchEthicsAdvisor | IRB, ethics, informed consent | 연구 윤리, IRB, 동의서 | sonnet |
| `diverga:a5` | ParadigmWorldviewAdvisor | paradigm, ontology, epistemology | 패러다임, 존재론, 인식론 | opus |
| `diverga:a6` | ConceptualFrameworkVisualizer | conceptual framework, visualize | 개념적 프레임워크 시각화 | sonnet |

### Category B: Evidence (5 agents)

| Agent ID | 이름 | 트리거 키워드 (EN) | 트리거 키워드 (KR) | Model |
|----------|------|-------------------|-------------------|-------|
| `diverga:b1` | LiteratureReviewStrategist | systematic review, PRISMA, literature search | 체계적 문헌고찰, 문헌 검색 | sonnet |
| `diverga:b2` | EvidenceQualityAppraiser | quality appraisal, RoB, GRADE | 품질 평가, 비뚤림 평가 | sonnet |
| `diverga:b3` | EffectSizeExtractor | effect size, Cohen's d, Hedges' g | 효과크기, 효과 크기 | haiku |
| `diverga:b4` | ResearchRadar | research trends, emerging topics | 연구 동향, 트렌드 | haiku |
| `diverga:b5` | ParallelDocumentProcessor | batch PDF, parallel processing | PDF 일괄, 병렬 처리 | opus |

### Category C: Design & Meta-Analysis (7 agents)

| Agent ID | 이름 | 트리거 키워드 (EN) | 트리거 키워드 (KR) | Model |
|----------|------|-------------------|-------------------|-------|
| `diverga:c1` | QuantitativeDesignConsultant | quantitative design, RCT, experimental | 양적 연구 설계, 실험 설계 | opus |
| `diverga:c2` | QualitativeDesignConsultant | qualitative design, phenomenology, grounded theory | 질적 연구 설계, 현상학 | opus |
| `diverga:c3` | MixedMethodsDesignConsultant | mixed methods, sequential, convergent | 혼합방법, 혼합 연구 | opus |
| `diverga:c4` | ExperimentalMaterialsDeveloper | intervention materials, experimental materials | 중재 자료, 실험 자료 | sonnet |
| `diverga:c5` | MetaAnalysisMaster | meta-analysis, pooled effect, heterogeneity | 메타분석, 통합 효과 | opus |
| `diverga:c6` | DataIntegrityGuard | data extraction, PDF extract | 데이터 추출, PDF 추출 | sonnet |
| `diverga:c7` | ErrorPreventionEngine | error prevention, validation, data check | 오류 방지, 검증 | sonnet |

### Category D: Data Collection (4 agents)

| Agent ID | 이름 | 트리거 키워드 (EN) | 트리거 키워드 (KR) | Model |
|----------|------|-------------------|-------------------|-------|
| `diverga:d1` | SamplingStrategyAdvisor | sampling, sample size, G*Power | 표집, 표본 크기 | sonnet |
| `diverga:d2` | InterviewFocusGroupSpecialist | interview, focus group, interview protocol | 인터뷰, 면담, 포커스 그룹 | sonnet |
| `diverga:d3` | ObservationProtocolDesigner | observation, observation protocol | 관찰, 관찰 프로토콜 | haiku |
| `diverga:d4` | MeasurementInstrumentDeveloper | instrument, measurement, scale development | 측정 도구, 척도 개발 | opus |

### Category E: Analysis (5 agents)

| Agent ID | 이름 | 트리거 키워드 (EN) | 트리거 키워드 (KR) | Model |
|----------|------|-------------------|-------------------|-------|
| `diverga:e1` | QuantitativeAnalysisGuide | statistical analysis, ANOVA, regression, SEM | 통계 분석, 회귀 | opus |
| `diverga:e2` | QualitativeCodingSpecialist | qualitative coding, thematic analysis | 질적 코딩, 주제 분석 | opus |
| `diverga:e3` | MixedMethodsIntegration | mixed methods integration, joint display | 혼합방법 통합 | opus |
| `diverga:e4` | AnalysisCodeGenerator | R code, Python code, analysis code | R 코드, 분석 코드 | haiku |
| `diverga:e5` | SensitivityAnalysisDesigner | sensitivity analysis, robustness check | 민감도 분석 | sonnet |

### Category F: Quality (5 agents)

| Agent ID | 이름 | 트리거 키워드 (EN) | 트리거 키워드 (KR) | Model |
|----------|------|-------------------|-------------------|-------|
| `diverga:f1` | InternalConsistencyChecker | consistency check, internal consistency | 일관성 검토 | haiku |
| `diverga:f2` | ChecklistManager | checklist, CONSORT, STROBE, COREQ | 체크리스트, 보고 지침 | haiku |
| `diverga:f3` | ReproducibilityAuditor | reproducibility, replication, OSF | 재현성, 반복가능성 | sonnet |
| `diverga:f4` | BiasTrustworthinessDetector | bias detection, trustworthiness | 편향 탐지, 신뢰성 | sonnet |
| `diverga:f5` | HumanizationVerifier | humanization verify, AI text check | 휴먼화 검증 | haiku |

### Category G: Communication (6 agents)

| Agent ID | 이름 | 트리거 키워드 (EN) | 트리거 키워드 (KR) | Model |
|----------|------|-------------------|-------------------|-------|
| `diverga:g1` | JournalMatcher | journal match, where to publish | 저널 매칭, 투고처 | sonnet |
| `diverga:g2` | AcademicCommunicator | academic writing, manuscript | 학술 글쓰기, 논문 작성 | sonnet |
| `diverga:g3` | PeerReviewStrategist | peer review, reviewer response | 동료 심사, 리뷰어 | sonnet |
| `diverga:g4` | PreregistrationComposer | preregistration, OSF, pre-register | 사전등록, OSF | sonnet |
| `diverga:g5` | AcademicStyleAuditor | AI pattern, check AI writing | AI 패턴, AI 글쓰기 | sonnet |
| `diverga:g6` | AcademicStyleHumanizer | humanize, humanization | 휴먼화, 자연스러운 | opus |

### Category H: Specialized (2 agents)

| Agent ID | 이름 | 트리거 키워드 (EN) | 트리거 키워드 (KR) | Model |
|----------|------|-------------------|-------------------|-------|
| `diverga:h1` | EthnographicResearchAdvisor | ethnography, fieldwork | 민족지학, 현장연구 | opus |
| `diverga:h2` | ActionResearchFacilitator | action research, participatory | 실행연구, 참여적 | opus |

---

## 병렬 실행 그룹

독립적인 태스크는 병렬로 실행됩니다:

```
┌─────────────────────────────────────────────────────────────────┐
│                  PARALLEL EXECUTION GROUPS                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Group 1: Research Foundation                                     │
│   diverga:a1 + diverga:a2 + diverga:a5                          │
│                                                                  │
│ Group 2: Literature & Evidence                                   │
│   diverga:b1 + diverga:b2 + diverga:b3                          │
│                                                                  │
│ Group 3: Quality Assurance                                       │
│   diverga:f1 + diverga:f3 + diverga:f4                          │
│                                                                  │
│ Group 4: Publication Preparation                                 │
│   diverga:g1 + diverga:g2 + diverga:g5                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 순차 실행 규칙

일부 에이전트는 순서대로 실행되어야 합니다:

### Meta-Analysis Pipeline

```
diverga:c5 (MetaAnalysisMaster - 오케스트레이션)
    ↓
diverga:c6 (DataIntegrityGuard - 데이터 추출)
    ↓
diverga:c7 (ErrorPreventionEngine - 검증)
```

### Humanization Pipeline

```
diverga:g5 (AcademicStyleAuditor - AI 패턴 탐지)
    ↓
diverga:g6 (AcademicStyleHumanizer - 휴먼화 변환)
    ↓
diverga:f5 (HumanizationVerifier - 검증)
```

---

## QA 테스트에서 에이전트 추적

### 탐지 패턴

```python
AGENT_PATTERNS = {
    'C5-MetaAnalysisMaster': r'diverga:c5|meta.*analysis',
    'A2-TheoreticalFrameworkArchitect': r'diverga:a2|theoret.*framework',
    'G5-AcademicStyleAuditor': r'diverga:g5|style.*audit|AI.*pattern',
    # ... 전체 40개 에이전트
}
```

### Tool Call에서 에이전트 탐지

```python
def detect_agent_from_tool_call(tool_call):
    tool_name = tool_call.get('name', '')
    args = tool_call.get('arguments', {})

    # Tool 이름에서 탐지
    for agent, pattern in AGENT_PATTERNS.items():
        if re.search(pattern, tool_name, re.IGNORECASE):
            return agent

    # Arguments에서 탐지
    prompt = args.get('prompt', '')
    for agent, pattern in AGENT_PATTERNS.items():
        if re.search(pattern, prompt, re.IGNORECASE):
            return agent

    return None
```

---

## 에이전트 전환 검증

### 컨텍스트 유지 확인

에이전트가 전환될 때 이전 결정이 유지되어야 합니다:

```yaml
validation:
  agent_transition:
    from: C5-MetaAnalysisMaster
    to: A2-TheoreticalFrameworkArchitect
    context_preserved:
      - "subject-specific effects"  # 이전 선택
      - "age moderation"            # 이전 논의
      - "small sample concern"      # 이전 제기된 우려
```

### 전환 요청 패턴

```python
TRANSITION_PATTERNS = [
    r'\bwait\b',
    r'\bbefore we\b',
    r'\bstep back\b',
    r'\bfirst\b.*\bcan we\b',
    r'\bactually\b.*\bfirst\b',
]
```

---

## 모델 라우팅

| 모델 | 에이전트 수 | 사용 시점 |
|------|------------|----------|
| **opus** | 16 | 복잡한 추론, 아키텍처, 깊은 분석 |
| **sonnet** | 17 | 표준 작업, 구조화된 출력 |
| **haiku** | 7 | 빠른 조회, 간단한 작업 |
