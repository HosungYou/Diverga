# Research Coordinator 개발 히스토리

**문서 버전**: 1.0.0
**최종 업데이트**: 2025-01-23
**작성자**: Claude Code + Hosung You

---

## 목차

1. [프로젝트 개요](#1-프로젝트-개요)
2. [버전 히스토리 요약](#2-버전-히스토리-요약)
3. [Phase 1: 초기 설계 및 구현](#3-phase-1-초기-설계-및-구현)
4. [Phase 2: VS 방법론 통합](#4-phase-2-vs-방법론-통합)
5. [Phase 3: Codex 리뷰 기반 업그레이드](#5-phase-3-codex-리뷰-기반-업그레이드)
6. [아키텍처 결정 기록 (ADR)](#6-아키텍처-결정-기록-adr)
7. [파일 생성 타임라인](#7-파일-생성-타임라인)
8. [향후 로드맵](#8-향후-로드맵)

---

## 1. 프로젝트 개요

### 1.1 프로젝트 목적

Research Coordinator는 **사회과학 연구자를 위한 20개 전문 AI 에이전트 시스템**입니다. 연구의 전체 라이프사이클(질문 정제 → 문헌 검토 → 분석 → 출판)을 지원하며, Claude Code Skills 시스템을 활용합니다.

### 1.2 핵심 가치

```
┌─────────────────────────────────────────────────────────────────┐
│                    Research Coordinator 핵심 가치               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 전문성 (Expertise)                                          │
│     - 20개 에이전트가 각각 연구 프로세스의 특정 영역 담당        │
│     - 사회과학 방법론에 특화된 도메인 지식                       │
│                                                                 │
│  2. 다양성 (Diversity) - VS 방법론                              │
│     - Mode Collapse 방지를 통한 창의적 추천                     │
│     - T-Score 기반 비전형적 옵션 탐색                           │
│                                                                 │
│  3. 품질 (Quality)                                              │
│     - Self-Critique 메커니즘으로 자기 검증                      │
│     - 다단계 품질 게이트                                        │
│                                                                 │
│  4. 협업 (Collaboration)                                        │
│     - 에이전트 간 표준화된 I/O 계약                             │
│     - Meta-Agent Governor를 통한 오케스트레이션                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 기술 스택

| 영역 | 기술 |
|------|------|
| 기반 플랫폼 | Claude Code Skills System |
| AI 모델 | Claude (Anthropic) |
| VS 방법론 | arXiv:2510.01171 기반 |
| 품질 보증 | Codex CLI (gpt-5.2-codex) |
| 버전 관리 | Git + GitHub |

---

## 2. 버전 히스토리 요약

```
┌─────────────────────────────────────────────────────────────────┐
│                      Version Timeline                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  v1.0.0 (2025-01-22 초기)                                       │
│    └── 20개 에이전트 기본 구조 설계                              │
│                                                                 │
│  v1.5.0 (2025-01-22 중반)                                       │
│    └── VS 방법론 통합 시작                                       │
│    └── Full/Enhanced/Light 레벨 분류                            │
│                                                                 │
│  v2.0.0 (2025-01-22 후반)                                       │
│    └── VS 방법론 전체 적용 완료                                  │
│    └── GitHub 초기 푸시                                          │
│                                                                 │
│  v2.1.0 (2025-01-23) ← 현재                                     │
│    └── Codex 리뷰 기반 P0-P3 업그레이드                         │
│    └── 아키텍처 문서 7종 추가                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Phase 1: 초기 설계 및 구현

### 3.1 시기

**2025-01-22 (오전~오후 초반)**

### 3.2 작업 내용

#### 3.2.1 에이전트 구조 설계

```
작업: 20개 에이전트를 5개 카테고리로 분류
시간: 약 2시간
목적: 연구 프로세스 전체를 커버하는 전문가 시스템 구축
```

**카테고리 분류 결정**:

| 카테고리 | 에이전트 | 역할 |
|---------|---------|------|
| A: 이론 및 연구 설계 | 01-04 | 연구 초기 단계 지원 |
| B: 문헌 및 증거 | 05-08 | 선행연구 탐색 및 평가 |
| C: 방법론 및 분석 | 09-12 | 통계 분석 및 코드 생성 |
| D: 품질 및 검증 | 13-16 | 품질 보증 및 편향 탐지 |
| E: 출판 및 커뮤니케이션 | 17-20 | 논문 작성 및 투고 |

**결정 이유**:
- 연구 프로세스의 자연스러운 흐름 반영
- 각 단계에서 필요한 전문성 명확화
- 병렬 실행 가능한 그룹 식별

#### 3.2.2 SKILL.md 템플릿 표준화

```markdown
# 표준 템플릿 구조
---
name: [agent-name]
description: [description]
---

## 개요
## 핵심 역량
## 작업 프로세스
## 출력 형식
## 관련 에이전트
```

**결정 이유**:
- 일관된 사용자 경험 제공
- 에이전트 간 상호 참조 용이
- 유지보수 효율성

### 3.3 산출물

- 20개 에이전트 디렉토리 구조
- 각 에이전트별 기본 SKILL.md
- 마스터 코디네이터 SKILL.md

---

## 4. Phase 2: VS 방법론 통합

### 4.1 시기

**2025-01-22 (오후)**

### 4.2 배경 및 동기

#### 4.2.1 문제 인식

```
┌─────────────────────────────────────────────────────────────────┐
│                    Mode Collapse 문제                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  현상: LLM이 항상 "가장 일반적인" 답변만 제공                    │
│                                                                 │
│  예시 (연구 설계 질문):                                         │
│  Q: "AI 학습 효과 연구에 적합한 이론은?"                        │
│  A: "인지부하이론을 추천합니다" (항상 동일)                      │
│                                                                 │
│  문제점:                                                        │
│  - 창의적/혁신적 대안 무시                                      │
│  - 연구자의 탐색 범위 제한                                      │
│  - 동일한 이론/방법만 반복 권장                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 4.2.2 VS 방법론 (Verbalized Sampling)

**출처**: arXiv:2510.01171

**핵심 원리**:
```
1. 옵션 열거: 모든 가능한 대안 명시적 나열
2. T-Score 계산: 각 옵션의 "전형성(Typicality)" 점수화
3. 비전형적 옵션 탐색: 낮은 T-Score 옵션 적극 고려
4. 근거 기반 선택: 최종 선택에 대한 명확한 근거 제시
```

### 4.3 작업 내용

#### 4.3.1 VS 레벨 분류

```yaml
# VS 적용 수준 결정
full_vs:    # 완전 적용 (5개)
  agents: [02, 03, 05, 10, 16]
  rationale: "핵심 의사결정 에이전트 - 다양성 극대화 필요"

enhanced_vs:  # 강화 적용 (6개)
  agents: [01, 04, 06, 07, 08, 09]
  rationale: "중요 분석 에이전트 - 옵션 다양화 필요"

light_vs:   # 경량 적용 (9개)
  agents: [11, 12, 13, 14, 15, 17, 18, 19, 20]
  rationale: "실행/검증 에이전트 - 모달 인식 수준"
```

**결정 이유**:

| 레벨 | 대상 | 이유 |
|------|------|------|
| Full VS | 이론 설계, 문헌 탐색, 분석 방법, 편향 탐지 | 연구의 방향성을 결정하는 핵심 에이전트 |
| Enhanced VS | 질문 정제, 윤리, 평가, 효과크기 | 중요하지만 Full 수준까지 불필요 |
| Light VS | 코드 생성, 체크리스트, 저널 매칭 | 실행 중심, 모달 인식만으로 충분 |

#### 4.3.2 VS 통합 구현

각 에이전트 SKILL.md에 다음 섹션 추가:

```markdown
## VS (Verbalized Sampling) 적용

### VS Level: [Full/Enhanced/Light]

### Phase 1: 옵션 열거 (Enumerate Options)
[가능한 모든 대안 나열]

### Phase 2: T-Score 평가 (Evaluate Typicality)
| 옵션 | T-Score | 특성 |
|------|---------|------|
| A    | 0.85    | 전형적 |
| B    | 0.45    | 균형적 |
| C    | 0.15    | 비전형적 |

### Phase 3: 비전형적 탐색 (Explore Non-Typical)
[T < 0.3 옵션에 대한 심층 분석]

### Phase 4: 최종 선택 (Final Selection)
[근거 기반 추천]
```

### 4.4 산출물

- 20개 에이전트 전체 VS 방법론 적용
- VS-Research-Framework.md 참조 문서
- GitHub 초기 커밋

---

## 5. Phase 3: Codex 리뷰 기반 업그레이드

### 5.1 시기

**2025-01-22 (저녁) ~ 2025-01-23 (새벽)**

### 5.2 Codex 리뷰 실행

#### 5.2.1 리뷰 도구

```bash
codex exec -m gpt-5.2-codex -C "$(pwd)" "
Conduct a comprehensive code and architecture review...
"
```

#### 5.2.2 리뷰 결과 요약

| 영역 | 점수 | 상태 |
|------|------|------|
| Code Quality | 9/10 | 🟢 |
| Architecture | 9/10 | 🟢 |
| Documentation | 9/10 | 🟢 |
| Maintainability | 8/10 | 🟢 |

**주요 피드백**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Codex 리뷰 핵심 피드백                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  P0 (Critical):                                                 │
│  - VS 행동을 검증할 평가 하네스 필요                            │
│  - 에이전트 간 I/O 계약 표준화 필요                             │
│                                                                 │
│  P1 (High):                                                     │
│  - Full VS 에이전트에 Self-Critique 메커니즘 추가               │
│  - 중앙 에이전트 레지스트리 생성                                │
│                                                                 │
│  P2 (Medium):                                                   │
│  - 컨텍스트 윈도우 예산 관리 전략                               │
│  - 이론/구성개념 지식 그래프                                    │
│                                                                 │
│  P3 (Low):                                                      │
│  - Meta-Agent 워크플로우 거버너                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.3 P0 작업: Critical Priority

#### 5.3.1 VS 행동 평가 하네스 (evaluation-harness.md)

```
작업 시간: 2025-01-23 02:30 ~ 03:00
소요 시간: 약 30분
```

**목적**:
- VS 방법론이 실제로 Mode Collapse를 방지하는지 검증
- 회귀 테스트를 통한 품질 유지

**구현 내용**:

```python
# Mode Collapse 탐지 알고리즘
def detect_mode_collapse(agent_outputs: list) -> ModeCollapseReport:
    """다중 실행에서 Mode Collapse 패턴 탐지"""
    recommendations = [o['vs_metadata']['final_selection']['option']
                       for o in agent_outputs]

    # 엔트로피 기반 다양성 측정
    from collections import Counter
    counts = Counter(recommendations)
    entropy = -sum((c/total) * log2(c/total) for c in counts.values())

    return ModeCollapseReport(
        diversity_score=entropy / max_entropy,
        mode_collapse_detected=diversity < 0.3
    )
```

**결정 이유**:
- VS 적용 효과를 객관적으로 측정 가능
- 에이전트 업데이트 시 품질 저하 방지
- CI/CD 파이프라인 통합 가능

#### 5.3.2 Agent I/O 계약 스키마 (agent-contract-schema.md)

```
작업 시간: 2025-01-23 03:00 ~ 03:30
소요 시간: 약 30분
```

**목적**:
- 에이전트 간 표준화된 데이터 교환
- 워크플로우 자동화 기반 마련

**구현 내용**:

```yaml
# 표준 입력 스키마
input_schema:
  context:
    research_question: string (required)
    domain: string (required)
    constraints: object (optional)
  previous_outputs: array[AgentOutput]
  user_preferences: object

# 표준 출력 스키마
output_schema:
  agent_id: string
  timestamp: ISO8601
  vs_metadata:
    level: enum[full, enhanced, light]
    options_considered: array
    t_scores: object
    final_selection: object
  content: object
  confidence: number (0-100)
  next_agents: array[string]
```

**결정 이유**:
- 에이전트 체인 실행 시 데이터 호환성 보장
- 디버깅 및 모니터링 용이
- 새 에이전트 추가 시 통합 용이

### 5.4 P1 작업: High Priority

#### 5.4.1 Self-Critique 메커니즘 (self-critique-framework.md)

```
작업 시간: 2025-01-23 03:30 ~ 04:00
소요 시간: 약 30분
```

**목적**:
- Reflexion 패턴 적용으로 출력 품질 향상
- 에이전트의 자기 검증 능력 부여

**적용 대상**: Full VS 에이전트 5개
- 02-theoretical-framework-architect
- 03-devils-advocate
- 05-systematic-literature-scout
- 10-statistical-analysis-guide
- 16-bias-detector

**구현 내용**:

```markdown
## Self-Critique 요구사항 (Full VS 필수)

### 강점 (Strengths)
- 이 분석/추천의 가장 강력한 근거는?
- 어떤 점에서 신뢰할 수 있는가?

### 약점 (Weaknesses)
- 이 분석의 한계점은?
- 어떤 가정에 의존하는가?

### 대안적 관점 (Alternative Perspectives)
- 다른 관점에서 보면?
- 반대 의견은 무엇인가?

### 개선 제안 (Improvement Suggestions)
- 추가 정보가 있다면 무엇이 유용한가?
- 어떻게 더 나은 분석이 가능한가?

### 신뢰도 평가 (Confidence Assessment)
| 영역 | 신뢰도 | 근거 |
|------|--------|------|
| 이론적 근거 | X/100 | ... |
| 방법론적 적합성 | X/100 | ... |
| 데이터 충분성 | X/100 | ... |

**전체 신뢰도**: {점수}/100
```

**결정 이유**:
- Full VS 에이전트는 핵심 의사결정 담당
- 자기 비평을 통한 blind spot 감소
- 사용자에게 신뢰도 정보 제공

#### 5.4.2 Agent Registry (agent-registry.yaml)

```
작업 시간: 2025-01-23 04:00 ~ 04:20
소요 시간: 약 20분
```

**목적**:
- 20개 에이전트 메타데이터 중앙 관리
- 프로그래매틱 접근 지원

**구현 내용**:

```yaml
agents:
  - id: "02"
    name: "theoretical-framework-architect"
    category: "A"
    vs_level: "full"
    triggers: ["이론적 프레임워크", "theoretical framework"]
    dependencies: ["01"]
    parallel_group: ["02", "03"]
    outputs: ["framework_recommendation", "theory_mapping"]
```

**결정 이유**:
- 동적 에이전트 선택 로직 구현 기반
- 워크플로우 자동화 지원
- 문서화와 코드의 일관성 유지

### 5.5 P2 작업: Medium Priority

#### 5.5.1 Context Budgeting 전략 (context-budgeting.md)

```
작업 시간: 2025-01-23 04:20 ~ 05:00
소요 시간: 약 40분
```

**목적**:
- 20개 에이전트 실행 시 컨텍스트 윈도우 효율적 관리
- 정보 손실 최소화하면서 비용 최적화

**문제 정의**:

```
에이전트 체인 실행 시:
Agent 01 → Agent 02 → Agent 05 → Agent 10 → Agent 16
   ↓           ↓           ↓           ↓           ↓
[출력 A]   [출력 B]    [출력 C]   [출력 D]   [출력 E]

누적 컨텍스트: A + B + C + D + E = 컨텍스트 한계 초과 위험
```

**구현 내용**:

```yaml
# 에이전트별 컨텍스트 예산
per_agent_limits:
  full_vs:
    max_output: 8000 tokens
    summary_threshold: 6000
    agents: [02, 03, 05, 10, 16]
  enhanced_vs:
    max_output: 5000 tokens
    agents: [01, 04, 06, 07, 08, 09]
  light_vs:
    max_output: 3000 tokens
    agents: [11-20]

# 계층적 요약
Level 0: 원본 (~8000 tokens)
Level 1: 상세 요약 (~3000 tokens)
Level 2: 간략 요약 (~1000 tokens)
Level 3: 핵심만 (~300 tokens)
```

**결정 이유**:
- 긴 워크플로우에서도 초기 정보 보존
- API 비용 최적화
- 응답 지연 감소

#### 5.5.2 Knowledge Graph (knowledge-graph.md)

```
작업 시간: 2025-01-23 05:00 ~ 05:40
소요 시간: 약 40분
```

**목적**:
- 사회과학 이론/구성개념/측정도구 관계 표현
- VS 방법론과 연계한 이론 추천

**구현 내용**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Knowledge Graph 구조                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [Theory Node]                                                  │
│    ├── name: "Technology Acceptance Model"                     │
│    ├── t_score: 0.85 (매우 전형적)                             │
│    ├── domain: "Education Technology"                          │
│    └── relations:                                               │
│        ├── CONTAINS → [Construct: Perceived Usefulness]        │
│        ├── CONTAINS → [Construct: Perceived Ease of Use]       │
│        └── EXTENDS ← [Theory: UTAUT]                           │
│                                                                 │
│  [Construct Node]                                               │
│    ├── name: "Perceived Usefulness"                            │
│    └── relations:                                               │
│        ├── MEASURED_BY → [Scale: Davis PU Scale]               │
│        └── CORRELATES → [Construct: Behavioral Intention]      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**결정 이유**:
- 이론 추천의 체계화 (Agent 02 지원)
- 구성개념 간 관계 가시화 (Agent 03 지원)
- T-Score 기반 비전형적 이론 탐색 지원

### 5.6 P3 작업: Low Priority

#### 5.6.1 Meta-Agent Workflow Governor (meta-agent-governor.md)

```
작업 시간: 2025-01-23 05:40 ~ 06:30
소요 시간: 약 50분
```

**목적**:
- 복잡한 멀티에이전트 워크플로우 오케스트레이션
- 에이전트 간 충돌 해결 및 품질 관리

**구현 내용**:

```
┌─────────────────────────────────────────────────────────────────┐
│                Meta-Agent Governor Architecture                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                    ┌──────────────────┐                         │
│                    │  Workflow        │                         │
│                    │  Planner         │                         │
│                    └────────┬─────────┘                         │
│                             │                                   │
│         ┌───────────────────┼───────────────────┐               │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐        │
│  │  Conflict    │   │  Quality     │   │  Resource    │        │
│  │  Resolver    │   │  Gate        │   │  Manager     │        │
│  └──────────────┘   └──────────────┘   └──────────────┘        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**핵심 컴포넌트**:

| 컴포넌트 | 역할 |
|---------|------|
| Workflow Planner | 사용자 요청 분석, 에이전트 실행 계획 생성 |
| Conflict Resolver | 에이전트 간 의견 충돌 탐지 및 해결 |
| Quality Gate | 실행 전/후 품질 검증 |
| Resource Manager | 컨텍스트 예산, 실행 시간 관리 |

**실행 모드**:

```yaml
execution_modes:
  automatic:
    description: "모든 결정을 시스템이 자동 처리"
    use_case: "반복적 워크플로우, 배치 처리"

  interactive:
    description: "주요 결정마다 사용자 확인"
    use_case: "중요 연구, 학습 목적"

  hybrid:
    description: "신뢰도 기반 자동/수동 전환"
    use_case: "일반적인 연구 작업"
    threshold: 70  # 70 미만이면 사용자 확인
```

**결정 이유**:
- 복잡한 연구 프로젝트 지원
- 에이전트 간 일관성 보장
- 사용자 개입 수준 조절 가능

### 5.7 Git 커밋 기록

```bash
# 커밋 1: P0-P1 완료
commit 2bef67b
Author: Hosung You
Date: 2025-01-23 04:30
Message: "feat: Add VS evaluation harness, Self-Critique framework,
          and Agent Registry for P0-P1 upgrades"

# 커밋 2: P2-P3 완료
commit 46741d9
Author: Hosung You
Date: 2025-01-23 06:45
Message: "feat: Add P2-P3 architectural components for
          multi-agent orchestration"
```

---

## 6. 아키텍처 결정 기록 (ADR)

### ADR-001: VS 레벨 분류 기준

**상태**: 승인됨
**일자**: 2025-01-22
**결정**: 에이전트를 Full/Enhanced/Light VS 3단계로 분류

**맥락**:
- 20개 에이전트에 동일한 VS 수준 적용 시 오버헤드 발생
- 에이전트별 의사결정 중요도가 다름

**결정**:
- Full VS (5개): 핵심 의사결정 에이전트
- Enhanced VS (6개): 중요 분석 에이전트
- Light VS (9개): 실행/검증 에이전트

**결과**:
- 리소스 효율적 사용
- 중요 에이전트에 다양성 집중

---

### ADR-002: Self-Critique 적용 범위

**상태**: 승인됨
**일자**: 2025-01-23
**결정**: Full VS 에이전트에만 Self-Critique 필수 적용

**맥락**:
- 모든 에이전트에 Self-Critique 적용 시 출력 길이 증가
- 실행 에이전트는 자기 비평보다 정확성이 중요

**결정**:
- Full VS 5개 에이전트: Self-Critique 필수
- Enhanced VS: 선택적 (복잡한 분석 시)
- Light VS: 적용 안 함

**결과**:
- 핵심 에이전트의 품질 향상
- 출력 길이 합리적 유지

---

### ADR-003: Context Budgeting 전략

**상태**: 승인됨
**일자**: 2025-01-23
**결정**: 계층적 요약 + 동적 예산 할당

**맥락**:
- 긴 워크플로우에서 컨텍스트 오버플로우 위험
- 모든 에이전트 출력을 원본으로 유지하면 비용 증가

**결정**:
- 4단계 계층적 요약 (Full → Detailed → Brief → Key)
- VS 레벨별 차등 예산 할당
- 80% 사용 시 자동 압축 모드 활성화

**결과**:
- 컨텍스트 효율적 사용
- 중요 정보 우선 보존

---

## 7. 파일 생성 타임라인

```
┌─────────────────────────────────────────────────────────────────┐
│                    File Creation Timeline                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  2025-01-22                                                     │
│  ─────────                                                      │
│  10:00  20개 에이전트 SKILL.md 생성                             │
│  14:00  VS-Research-Framework.md 생성                           │
│  16:00  VS 방법론 통합 (20개 파일 수정)                         │
│  18:00  마스터 코디네이터 SKILL.md 완성                         │
│  19:00  GitHub 초기 푸시                                        │
│                                                                 │
│  2025-01-23                                                     │
│  ─────────                                                      │
│  02:30  evaluation-harness.md 생성                              │
│  03:00  agent-contract-schema.md 생성                           │
│  03:30  self-critique-framework.md 생성                         │
│  03:45  Full VS 에이전트 5개 Self-Critique 추가                 │
│  04:00  agent-registry.yaml 생성                                │
│  04:30  GitHub 푸시 (2bef67b)                                   │
│  04:40  context-budgeting.md 생성                               │
│  05:20  knowledge-graph.md 생성                                 │
│  06:00  meta-agent-governor.md 생성                             │
│  06:45  GitHub 푸시 (46741d9)                                   │
│  07:00  DEVELOPMENT_HISTORY.md 생성 (현재 문서)                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. 향후 로드맵

### 8.1 단기 (v2.2.0)

| 작업 | 우선순위 | 예상 시간 |
|------|---------|----------|
| Light VS 출력 형식 표준화 | P1 | 2시간 |
| 코드 예시 실행성 강화 | P1 | 2시간 |
| YAML frontmatter 강화 | P2 | 1시간 |
| 상호 참조 양방향화 | P3 | 1시간 |

### 8.2 중기 (v3.0.0)

| 작업 | 설명 |
|------|------|
| Marketplace 플러그인 확장 | ScholaRAG, ResearcherRAG 통합 |
| 실시간 협업 지원 | 다중 사용자 워크플로우 |
| 대시보드 UI | 에이전트 상태 모니터링 |

### 8.3 장기 (v4.0.0)

| 작업 | 설명 |
|------|------|
| 자가 학습 에이전트 | 피드백 기반 개선 |
| 도메인 특화 확장 | 의학, 심리학, 경영학 버전 |
| 오픈소스 커뮤니티 | 사용자 기여 에이전트 |

---

## 부록: 참조 문서 목록

| 문서 | 경로 | 용도 |
|------|------|------|
| VS Framework | `references/VS-Research-Framework.md` | VS 방법론 상세 |
| Agent Contract | `references/agent-contract-schema.md` | I/O 스키마 |
| Agent Registry | `references/agent-registry.yaml` | 에이전트 메타데이터 |
| Evaluation Harness | `references/evaluation-harness.md` | VS 평가 |
| Self-Critique | `references/self-critique-framework.md` | 자기 비평 |
| Context Budget | `references/context-budgeting.md` | 컨텍스트 관리 |
| Knowledge Graph | `references/knowledge-graph.md` | 지식 그래프 |
| Meta-Agent Governor | `references/meta-agent-governor.md` | 오케스트레이션 |

---

*이 문서는 Research Coordinator 프로젝트의 공식 개발 히스토리입니다.*
