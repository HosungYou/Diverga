# Theory & Construct Knowledge Graph

**Version**: 1.0.0
**Based on**: Codex Review (2025-01-22) + Academic Knowledge Management

---

## 개요

Knowledge Graph는 사회과학 연구에서 사용되는 이론, 구성개념, 측정도구 간의 관계를 구조화하여 에이전트들이 맥락에 맞는 추천을 할 수 있도록 지원합니다.

## 그래프 구조

```
┌─────────────────────────────────────────────────────────────────┐
│                    Knowledge Graph Architecture                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                      ┌─────────────┐                            │
│                      │   Domain    │                            │
│                      │ (Psychology │                            │
│                      │  Education) │                            │
│                      └──────┬──────┘                            │
│                             │ contains                          │
│              ┌──────────────┼──────────────┐                    │
│              ▼              ▼              ▼                    │
│       ┌──────────┐   ┌──────────┐   ┌──────────┐               │
│       │  Theory  │   │  Theory  │   │  Theory  │               │
│       │  (TAM)   │   │  (SDT)   │   │  (CLT)   │               │
│       └────┬─────┘   └────┬─────┘   └────┬─────┘               │
│            │ defines      │ defines      │ defines             │
│            ▼              ▼              ▼                      │
│       ┌──────────┐   ┌──────────┐   ┌──────────┐               │
│       │Construct │   │Construct │   │Construct │               │
│       │(Perceived│   │(Autonomy)│   │(Cognitive│               │
│       │Usefulness│   │          │   │  Load)   │               │
│       └────┬─────┘   └────┬─────┘   └────┬─────┘               │
│            │ measured_by  │ measured_by  │ measured_by         │
│            ▼              ▼              ▼                      │
│       ┌──────────┐   ┌──────────┐   ┌──────────┐               │
│       │  Scale   │   │  Scale   │   │  Scale   │               │
│       │ (Davis   │   │ (BPNS)   │   │ (Paas)   │               │
│       │  1989)   │   │          │   │          │               │
│       └──────────┘   └──────────┘   └──────────┘               │
│                                                                  │
│  Relationships:                                                  │
│  ─────────── extends                                            │
│  - - - - - - competes_with                                      │
│  ═══════════ integrates_with                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 노드 스키마

### 1. Theory (이론)

```yaml
theory_node:
  id: string              # 고유 식별자 (예: "SDT")
  name: string            # Self-Determination Theory
  full_name: string       # 전체 이름
  authors: list[string]   # [Deci, Ryan]
  year: int               # 1985
  domain: list[string]    # [psychology, education, management]

  t_score: float          # 0.0-1.0 (VS 전형성 점수)
  usage_count: int        # 최근 5년 인용/사용 빈도

  core_constructs: list[string]  # [autonomy, competence, relatedness]

  relationships:
    extends: list[string]        # 확장한 이론
    competes_with: list[string]  # 경쟁 이론
    integrates_with: list[string] # 통합 가능 이론

  metadata:
    seminal_paper: string  # DOI
    review_papers: list[string]
    validated_contexts: list[string]  # 검증된 맥락
```

### 2. Construct (구성개념)

```yaml
construct_node:
  id: string              # 고유 식별자 (예: "perceived_autonomy")
  name: string            # Perceived Autonomy
  definition: string      # 정의

  parent_theory: string   # SDT
  related_constructs: list[string]  # 관련 구성개념

  measurement:
    validated_scales: list[string]  # 검증된 측정도구
    typical_items: int    # 일반적 문항 수
    response_format: string  # Likert 5-point

  role:
    can_be: list[string]  # [IV, DV, mediator, moderator]
    typical_role: string  # mediator

  metadata:
    cross_cultural_validity: list[string]  # 문화적 타당화 국가
    age_groups: list[string]  # 적용 가능 연령대
```

### 3. Scale (측정도구)

```yaml
scale_node:
  id: string              # 고유 식별자 (예: "BPNS")
  name: string            # Basic Psychological Needs Scale
  authors: list[string]   # [Deci, Ryan]
  year: int               # 2000

  measures: string        # 측정하는 구성개념 ID
  items: int              # 21
  subscales: list[string] # [autonomy, competence, relatedness]
  response_format: string # 7-point Likert

  psychometrics:
    cronbach_alpha: float  # 0.85
    test_retest: float     # 0.78
    factor_structure: string  # 3-factor

  availability:
    languages: list[string]  # [English, Korean, Chinese, ...]
    open_access: boolean
    citation: string       # APA citation
```

## 관계 스키마

### 1. 이론 간 관계

```yaml
theory_relationships:
  extends:
    description: "기존 이론을 확장/발전"
    example:
      from: "UTAUT"
      to: "TAM"
      note: "TAM의 4개 구성개념을 확장"

  competes_with:
    description: "동일 현상에 대한 경쟁 설명"
    example:
      from: "SDT"
      to: "expectancy_value"
      note: "동기 설명에서 경쟁"

  integrates_with:
    description: "통합 가능한 보완적 이론"
    example:
      from: "SDT"
      to: "TAM"
      note: "동기-수용 통합 프레임워크 가능"
      t_score_when_integrated: 0.45
```

### 2. 구성개념 간 관계

```yaml
construct_relationships:
  predicts:
    description: "예측 관계"
    strength: float  # 메타분석 기반 효과크기

  mediates:
    description: "매개 관계"
    path: [IV, mediator, DV]

  moderates:
    description: "조절 관계"
    interaction: string

  overlaps_with:
    description: "개념적 중복"
    overlap_degree: float  # 0-1
```

## 도메인별 이론 카탈로그

### Psychology (심리학)

```yaml
psychology_theories:
  modal_tier:  # T > 0.8
    - id: "SCT"
      name: "Social Cognitive Theory"
      t_score: 0.90
      core_constructs: [self_efficacy, outcome_expectations, observational_learning]

    - id: "TPB"
      name: "Theory of Planned Behavior"
      t_score: 0.88
      core_constructs: [attitude, subjective_norm, perceived_behavioral_control, intention]

  established_tier:  # T 0.5-0.8
    - id: "SDT"
      name: "Self-Determination Theory"
      t_score: 0.70
      core_constructs: [autonomy, competence, relatedness, intrinsic_motivation]
      integrates_with: [TAM, flow_theory]

    - id: "flow_theory"
      name: "Flow Theory"
      t_score: 0.65
      core_constructs: [flow_state, challenge_skill_balance, clear_goals]

  emerging_tier:  # T 0.3-0.5
    - id: "control_value"
      name: "Control-Value Theory of Achievement Emotions"
      t_score: 0.45
      core_constructs: [control_appraisals, value_appraisals, achievement_emotions]

  creative_tier:  # T < 0.3
    - id: "SDT_TAM_integration"
      name: "SDT × TAM Integration"
      t_score: 0.25
      description: "자율성 지지가 기술 수용에 미치는 영향"
      parent_theories: [SDT, TAM]
```

### Education (교육학)

```yaml
education_theories:
  modal_tier:
    - id: "constructivism"
      name: "Constructivism"
      t_score: 0.85
      core_constructs: [knowledge_construction, prior_knowledge, social_interaction]

  established_tier:
    - id: "CLT"
      name: "Cognitive Load Theory"
      t_score: 0.60
      core_constructs: [intrinsic_load, extraneous_load, germane_load]
      measures: [paas_scale, nasa_tlx]

    - id: "CoI"
      name: "Community of Inquiry"
      t_score: 0.60
      core_constructs: [cognitive_presence, social_presence, teaching_presence]

  emerging_tier:
    - id: "threshold_concepts"
      name: "Threshold Concepts"
      t_score: 0.35
      core_constructs: [troublesome_knowledge, liminality, transformation]

    - id: "transformative_learning"
      name: "Transformative Learning Theory"
      t_score: 0.50
      core_constructs: [disorienting_dilemma, critical_reflection, perspective_transformation]
```

### Management/HRD (경영학/HRD)

```yaml
management_theories:
  modal_tier:
    - id: "TAM"
      name: "Technology Acceptance Model"
      t_score: 0.95
      warning: "극단적 모달 - 반드시 회피 또는 확장"
      core_constructs: [perceived_usefulness, perceived_ease_of_use, behavioral_intention]

    - id: "UTAUT"
      name: "Unified Theory of Acceptance and Use of Technology"
      t_score: 0.88
      core_constructs: [performance_expectancy, effort_expectancy, social_influence, facilitating_conditions]

  established_tier:
    - id: "JDR"
      name: "Job Demands-Resources Model"
      t_score: 0.55
      core_constructs: [job_demands, job_resources, burnout, engagement]

  emerging_tier:
    - id: "PsyCap"
      name: "Psychological Capital"
      t_score: 0.45
      core_constructs: [self_efficacy, hope, optimism, resilience]
      integrates_with: [SCT, positive_psychology]
```

## 쿼리 인터페이스

### 1. 이론 추천 쿼리

```python
def recommend_theory(
    domain: str,
    research_question: str,
    target_t_score: tuple = (0.3, 0.6),  # VS 권장 범위
    existing_theories: list = None,
    innovation_level: float = 0.5
) -> list:
    """연구 질문에 적합한 이론 추천 (VS 적용)"""

    candidates = query_graph(f"""
        MATCH (t:Theory)-[:BELONGS_TO]->(d:Domain {{name: '{domain}'}})
        WHERE t.t_score >= {target_t_score[0]}
          AND t.t_score <= {target_t_score[1]}
        RETURN t
        ORDER BY t.t_score ASC
    """)

    # 통합 가능 이론 탐색
    if innovation_level > 0.6:
        integrations = find_theory_integrations(candidates, existing_theories)
        candidates.extend(integrations)

    return rank_by_relevance(candidates, research_question)


def find_theory_integrations(theories: list, existing: list) -> list:
    """이론 통합 가능성 탐색"""

    integrations = []
    for t1 in theories:
        for t2 in existing or []:
            if has_integration_potential(t1, t2):
                integration = {
                    "type": "integration",
                    "theories": [t1["id"], t2["id"]],
                    "t_score": calculate_integration_t_score(t1, t2),
                    "rationale": generate_integration_rationale(t1, t2)
                }
                integrations.append(integration)

    return integrations
```

### 2. 측정도구 추천 쿼리

```python
def recommend_scales(
    constructs: list,
    language: str = "English",
    context: str = None
) -> dict:
    """구성개념에 대한 측정도구 추천"""

    recommendations = {}

    for construct in constructs:
        scales = query_graph(f"""
            MATCH (c:Construct {{id: '{construct}'}})<-[:MEASURES]-(s:Scale)
            WHERE '{language}' IN s.languages
            RETURN s
            ORDER BY s.psychometrics.cronbach_alpha DESC
        """)

        # 맥락 적합성 필터링
        if context:
            scales = filter_by_context(scales, context)

        recommendations[construct] = scales

    return recommendations
```

### 3. T-Score 조회

```python
def get_t_score(theory_id: str) -> dict:
    """이론의 T-Score 및 관련 정보 조회"""

    result = query_graph(f"""
        MATCH (t:Theory {{id: '{theory_id}'}})
        RETURN t.t_score, t.usage_count,
               t.core_constructs, t.integrates_with
    """)

    return {
        "theory_id": theory_id,
        "t_score": result["t_score"],
        "classification": classify_t_score(result["t_score"]),
        "usage_count": result["usage_count"],
        "recommendation": generate_vs_recommendation(result)
    }


def classify_t_score(score: float) -> str:
    if score > 0.8:
        return "modal (회피 권장)"
    elif score > 0.5:
        return "established (차별화 가능)"
    elif score > 0.3:
        return "emerging (권장)"
    else:
        return "creative (강한 근거 필요)"
```

## 에이전트 통합

### Agent 02 (Theoretical Framework Architect) 연동

```yaml
agent_02_integration:
  query_on_startup:
    - "Get modal theories for {domain}"
    - "Find emerging theories for {research_question}"
    - "Check integration potential for {existing_theories}"

  output_enrichment:
    - Add T-Score to all recommended theories
    - Include validated scales for constructs
    - Flag modal theories with warnings
```

### Agent 05 (Systematic Literature Scout) 연동

```yaml
agent_05_integration:
  query_for_keywords:
    - "Get all synonyms for {construct}"
    - "Find related constructs for {theory}"
    - "Get validated scale names for search"

  citation_tracking:
    - "Get seminal papers for {theory}"
    - "Find review papers for {construct}"
```

## 그래프 업데이트

### 자동 업데이트 트리거

```yaml
update_triggers:
  new_publication:
    condition: "Agent 08 detects new seminal paper"
    action: "Update usage_count, recalculate t_score"

  new_scale_validation:
    condition: "New cultural validation published"
    action: "Add language to scale.languages"

  theory_integration:
    condition: "New integration framework published"
    action: "Add integration node with calculated t_score"
```

### 수동 큐레이션

```yaml
curation_process:
  frequency: "quarterly"
  tasks:
    - Verify T-Score calculations against citation data
    - Add newly emerging theories
    - Update scale psychometrics from meta-analyses
    - Review integration potentials
```

## 시각화

```
┌─────────────────────────────────────────────────────────────────┐
│              Theory Network Visualization                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                        ┌─────┐                                  │
│                   ┌────│ TAM │────┐                             │
│                   │    │T=.95│    │                             │
│                   │    └──┬──┘    │                             │
│              extends     │     extends                          │
│                   │      │        │                             │
│              ┌────▼───┐  │   ┌────▼───┐                        │
│              │ UTAUT  │  │   │ UTAUT2 │                        │
│              │ T=.88  │  │   │ T=.82  │                        │
│              └────────┘  │   └────────┘                        │
│                          │                                      │
│                   integrates                                    │
│                          │                                      │
│                     ┌────▼───┐                                  │
│                     │  SDT   │                                  │
│                     │ T=.70  │                                  │
│                     └────┬───┘                                  │
│                          │                                      │
│                   ┌──────┴──────┐                               │
│                   │             │                               │
│              ┌────▼───┐   ┌────▼───┐                           │
│              │SDT×TAM │   │SDT×CLT │                           │
│              │ T=.25  │   │ T=.30  │                           │
│              └────────┘   └────────┘                           │
│                                                                  │
│  Legend: ──── extends  ════ integrates  ---- competes          │
│  Color:  🔴 Modal  🟡 Established  🟢 Emerging  🔵 Creative    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 관련 문서

- `agent-registry.yaml`: 에이전트별 knowledge graph 활용 방법
- `evaluation-harness.md`: T-Score 검증 방법
- `VS-Research-Framework.md`: VS 방법론과 T-Score 통합
