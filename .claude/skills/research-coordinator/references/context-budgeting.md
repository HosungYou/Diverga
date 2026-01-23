# Context Budgeting Strategy

**Version**: 1.0.0
**Based on**: Codex Review (2025-01-22) + Large Context Management Best Practices

---

## 개요

Context Budgeting은 20개 에이전트 시스템에서 LLM 컨텍스트 윈도우를 효율적으로 관리하여 정보 손실을 최소화하고 비용을 최적화합니다.

## 문제 정의

```
┌─────────────────────────────────────────────────────────────────┐
│                    Context Window Challenge                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  에이전트 체인 실행 시:                                           │
│                                                                  │
│  Agent 01 → Agent 02 → Agent 05 → Agent 10 → Agent 16           │
│     ↓           ↓           ↓           ↓           ↓           │
│  [출력 A]   [출력 B]    [출력 C]   [출력 D]   [출력 E]           │
│                                                                  │
│  누적 컨텍스트: A + B + C + D + E = 컨텍스트 한계 초과 위험      │
│                                                                  │
│  문제:                                                           │
│  1. 컨텍스트 오버플로우                                          │
│  2. 초기 에이전트 출력 정보 손실                                 │
│  3. 비용 증가 (토큰 수 비례)                                     │
│  4. 응답 지연                                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 예산 할당 전략

### 1. 에이전트별 컨텍스트 예산

```yaml
context_budget:
  total_available: 200000  # 예: Claude의 컨텍스트 윈도우

  allocation:
    system_prompt: 5000      # 시스템 프롬프트 (고정)
    user_context: 10000      # 사용자 입력 및 대화
    agent_outputs: 150000    # 에이전트 출력용
    buffer: 35000            # 버퍼 (안전 마진)

  per_agent_limits:
    full_vs:
      max_output: 8000       # Full VS 에이전트 최대 출력
      summary_threshold: 6000 # 이 이상이면 요약
      agents: [02, 03, 05, 10, 16]

    enhanced_vs:
      max_output: 5000       # Enhanced VS 에이전트 최대 출력
      summary_threshold: 4000
      agents: [01, 04, 06, 07, 08, 09]

    light_vs:
      max_output: 3000       # Light VS 에이전트 최대 출력
      summary_threshold: 2500
      agents: [11, 12, 13, 14, 15, 17, 18, 19, 20]
```

### 2. 동적 예산 조정

```python
def allocate_context_budget(workflow: list, total_budget: int = 150000) -> dict:
    """워크플로우에 따른 동적 컨텍스트 예산 할당"""

    agent_weights = {
        "full_vs": 3.0,      # Full VS는 더 많은 예산
        "enhanced_vs": 2.0,
        "light_vs": 1.0
    }

    vs_levels = {
        "02": "full_vs", "03": "full_vs", "05": "full_vs",
        "10": "full_vs", "16": "full_vs",
        "01": "enhanced_vs", "04": "enhanced_vs", "06": "enhanced_vs",
        "07": "enhanced_vs", "08": "enhanced_vs", "09": "enhanced_vs",
        # Light VS: 나머지
    }

    # 가중치 합계 계산
    total_weight = sum(
        agent_weights.get(vs_levels.get(agent, "light_vs"), 1.0)
        for agent in workflow
    )

    # 에이전트별 예산 할당
    budget_allocation = {}
    for agent in workflow:
        vs_level = vs_levels.get(agent, "light_vs")
        weight = agent_weights[vs_level]
        budget_allocation[agent] = int((weight / total_weight) * total_budget)

    return budget_allocation
```

## 컨텍스트 압축 전략

### 1. 계층적 요약 (Hierarchical Summarization)

```
┌─────────────────────────────────────────────────────────────────┐
│                   Hierarchical Summarization                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Level 0 (Full): 원본 출력 (~8000 tokens)                       │
│    │                                                            │
│    ▼                                                            │
│  Level 1 (Detailed): 상세 요약 (~3000 tokens)                   │
│    - 주요 결정사항                                               │
│    - T-Score 분포                                               │
│    - Self-Critique 핵심                                         │
│    │                                                            │
│    ▼                                                            │
│  Level 2 (Brief): 간략 요약 (~1000 tokens)                      │
│    - 최종 추천                                                   │
│    - 핵심 근거 3개                                              │
│    │                                                            │
│    ▼                                                            │
│  Level 3 (Key): 핵심만 (~300 tokens)                            │
│    - 결정: [X]                                                  │
│    - 신뢰도: [Y]/100                                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2. 요약 템플릿

```yaml
summary_templates:
  level_1_detailed:
    format: |
      ## Agent {id} 요약 (상세)

      **최종 결정**: {decision}
      **T-Score**: {t_score}
      **신뢰도**: {confidence}/100

      ### 핵심 근거
      1. {reason_1}
      2. {reason_2}
      3. {reason_3}

      ### 주요 대안
      - {alternative_1} (T={t1})
      - {alternative_2} (T={t2})

      ### Self-Critique 요점
      - 강점: {strength}
      - 약점: {weakness}
      - 개선: {improvement}

      ### 후속 에이전트 권고
      - {next_agent}: {reason}

    target_tokens: 3000

  level_2_brief:
    format: |
      ## Agent {id} 요약

      **결정**: {decision} (T={t_score}, 신뢰도={confidence})
      **근거**: {key_reasons}
      **대안**: {alternatives}
      **후속**: {next_agents}

    target_tokens: 1000

  level_3_key:
    format: |
      [{id}] {decision} | T={t_score} | {confidence}/100

    target_tokens: 300
```

### 3. 선택적 컨텍스트 보존

```python
def select_context_to_preserve(agent_outputs: list, budget: int) -> list:
    """예산 내에서 보존할 컨텍스트 선택"""

    # 우선순위 점수 계산
    priority_scores = []
    for output in agent_outputs:
        score = calculate_priority(output)
        priority_scores.append((output, score))

    # 우선순위순 정렬
    priority_scores.sort(key=lambda x: x[1], reverse=True)

    # 예산 내에서 선택
    preserved = []
    current_tokens = 0

    for output, score in priority_scores:
        tokens = estimate_tokens(output)
        if current_tokens + tokens <= budget:
            preserved.append(output)
            current_tokens += tokens
        else:
            # 요약본으로 대체
            summary = summarize_output(output, level=2)
            preserved.append(summary)
            current_tokens += estimate_tokens(summary)

    return preserved


def calculate_priority(output: dict) -> float:
    """컨텍스트 보존 우선순위 계산"""

    factors = {
        "recency": 0.3,        # 최신 출력일수록 중요
        "vs_level": 0.25,      # Full VS > Enhanced > Light
        "confidence": 0.2,      # 신뢰도 높을수록 중요
        "dependencies": 0.15,   # 후속 에이전트가 참조하면 중요
        "user_relevance": 0.1   # 사용자 질문과의 관련성
    }

    score = 0
    score += factors["recency"] * output.get("recency_score", 0.5)
    score += factors["vs_level"] * {"full": 1.0, "enhanced": 0.7, "light": 0.4}[output.get("vs_level", "light")]
    score += factors["confidence"] * output.get("confidence", 0.5)
    score += factors["dependencies"] * (1.0 if output.get("has_dependents") else 0.3)
    score += factors["user_relevance"] * output.get("relevance_score", 0.5)

    return score
```

## 워크플로우별 예산 전략

### 1. Full Research Cycle

```yaml
full_research_cycle:
  stages:
    planning:
      agents: [01, 02, 03, 04]
      budget: 30000
      compression: level_1  # 상세 요약 유지
      rationale: "이론적 결정이 후속 단계에 중요"

    literature:
      agents: [05, 06, 07, 08]
      budget: 35000
      compression: level_1
      rationale: "검색 전략이 분석에 영향"

    methods:
      agents: [09, 10, 11, 12]
      budget: 30000
      compression: level_2  # 간략 요약 가능
      rationale: "코드는 별도 저장, 결정만 보존"

    validation:
      agents: [13, 14, 15, 16]
      budget: 25000
      compression: level_2
      rationale: "체크리스트 결과는 간략하게"

    publication:
      agents: [17, 18, 19, 20]
      budget: 20000
      compression: level_3  # 핵심만
      rationale: "최종 단계, 이전 맥락 최소화 가능"
```

### 2. Meta-Analysis Workflow

```yaml
meta_analysis:
  agents: [01, 02, 05, 06, 07, 10, 12, 16, 17]
  total_budget: 100000

  critical_agents:  # 압축 최소화
    - 05: "검색 전략 전체 보존"
    - 07: "효과크기 데이터 전체 보존"
    - 10: "분석 방법 상세 보존"

  compressible_agents:  # level_2 이상 압축 가능
    - 01, 02, 16, 17
```

## 컨텍스트 캐싱

### 1. 캐시 구조

```yaml
context_cache:
  storage: ".researcherrag/context_cache/"

  cache_levels:
    session:
      location: "memory"
      ttl: "session_duration"
      content: "full_outputs"

    project:
      location: "disk"
      ttl: "7_days"
      content: "level_1_summaries"

    persistent:
      location: "disk"
      ttl: "indefinite"
      content: "key_decisions_only"
```

### 2. 캐시 활용

```python
def load_from_cache(agent_id: str, cache_level: str = "session") -> dict:
    """캐시에서 에이전트 출력 로드"""

    cache_path = get_cache_path(agent_id, cache_level)

    if cache_path.exists():
        cached = load_json(cache_path)

        # 유효성 검증
        if is_cache_valid(cached):
            return cached

    return None


def save_to_cache(agent_id: str, output: dict, levels: list = ["session"]):
    """에이전트 출력을 캐시에 저장"""

    for level in levels:
        if level == "session":
            content = output  # 전체
        elif level == "project":
            content = summarize_output(output, level=1)
        else:
            content = summarize_output(output, level=3)

        cache_path = get_cache_path(agent_id, level)
        save_json(cache_path, {
            "agent_id": agent_id,
            "timestamp": datetime.now().isoformat(),
            "content": content
        })
```

## 예산 모니터링

### 1. 실시간 토큰 추적

```python
class ContextBudgetTracker:
    def __init__(self, total_budget: int = 150000):
        self.total_budget = total_budget
        self.used = 0
        self.agent_usage = {}

    def track(self, agent_id: str, tokens: int):
        """에이전트 토큰 사용량 추적"""
        self.used += tokens
        self.agent_usage[agent_id] = tokens

        # 경고 임계값
        if self.used > self.total_budget * 0.8:
            self.trigger_compression_mode()

    def trigger_compression_mode(self):
        """압축 모드 활성화"""
        print("⚠️ Context budget at 80%. Activating compression.")
        # 이후 에이전트는 level_2 요약으로 제한

    def get_remaining(self) -> int:
        return self.total_budget - self.used

    def report(self) -> dict:
        return {
            "total_budget": self.total_budget,
            "used": self.used,
            "remaining": self.get_remaining(),
            "usage_percent": (self.used / self.total_budget) * 100,
            "per_agent": self.agent_usage
        }
```

### 2. 예산 대시보드

```
┌─────────────────────────────────────────────────────────────────┐
│                  Context Budget Dashboard                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Total Budget: 150,000 tokens                                   │
│  Used: 87,500 tokens (58.3%)                                    │
│  Remaining: 62,500 tokens                                       │
│                                                                  │
│  ████████████████████░░░░░░░░░░░░░░ 58.3%                       │
│                                                                  │
│  Per Agent Usage:                                                │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ 02-theoretical    ████████████████░░░░ 8,200 (5.5%)   │     │
│  │ 05-literature     ██████████████████░░ 9,100 (6.1%)   │     │
│  │ 10-statistical    ████████████████░░░░ 7,800 (5.2%)   │     │
│  │ 03-devils         ██████████████░░░░░░ 6,500 (4.3%)   │     │
│  │ Others            ████████████████████ 55,900 (37.3%) │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  Compression Status: Normal                                      │
│  Next Agent Budget: 8,000 tokens (Full VS)                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 관련 문서

- `agent-contract-schema.md`: 에이전트 출력 스키마 (요약 기준)
- `agent-registry.yaml`: 에이전트별 VS 레벨
- `evaluation-harness.md`: 압축 후 품질 검증
