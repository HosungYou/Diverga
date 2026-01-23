# Meta-Agent Workflow Governor

**Version**: 1.0.0
**Based on**: Codex Review (2025-01-22) + Multi-Agent Orchestration Patterns

---

## 개요

Meta-Agent Workflow Governor는 20개 연구 에이전트의 실행을 조율하는 상위 제어 시스템입니다. 워크플로우 최적화, 에이전트 간 충돌 해결, 품질 게이트 관리를 담당합니다.

## 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                  Meta-Agent Workflow Governor                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    Orchestration Layer                    │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐│    │
│  │  │ Workflow │  │ Conflict │  │ Quality  │  │ Resource ││    │
│  │  │ Planner  │  │ Resolver │  │  Gate    │  │ Manager  ││    │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘│    │
│  └───────┼─────────────┼─────────────┼─────────────┼───────┘    │
│          │             │             │             │             │
│  ┌───────┴─────────────┴─────────────┴─────────────┴───────┐    │
│  │                    Execution Engine                       │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │    │
│  │  │ Parallel │  │Sequential│  │Conditional│              │    │
│  │  │ Executor │  │ Executor │  │ Executor  │              │    │
│  │  └──────────┘  └──────────┘  └──────────┘              │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│  ┌───────────────────────────┴───────────────────────────┐      │
│  │                    Agent Pool (20 Agents)               │      │
│  │  ┌────┐┌────┐┌────┐┌────┐┌────┐    ┌────┐┌────┐┌────┐│      │
│  │  │ 01 ││ 02 ││ 03 ││ 04 ││ 05 │ .. │ 18 ││ 19 ││ 20 ││      │
│  │  └────┘└────┘└────┘└────┘└────┘    └────┘└────┘└────┘│      │
│  └───────────────────────────────────────────────────────┘      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 핵심 컴포넌트

### 1. Workflow Planner

사용자 요청을 분석하여 최적의 에이전트 실행 계획을 수립합니다.

```yaml
workflow_planner:
  inputs:
    - user_request: string
    - context: object
    - constraints: object

  outputs:
    - execution_plan: list[AgentTask]
    - estimated_duration: int
    - resource_requirements: object

  strategies:
    dependency_analysis:
      description: "에이전트 간 의존성 분석"
      algorithm: "topological_sort"

    parallel_grouping:
      description: "병렬 실행 가능 에이전트 그룹화"
      algorithm: "graph_coloring"

    critical_path:
      description: "최장 경로 식별 및 최적화"
      algorithm: "CPM"
```

#### 실행 계획 생성

```python
def create_execution_plan(
    user_request: str,
    detected_keywords: list,
    constraints: dict
) -> ExecutionPlan:
    """사용자 요청에 대한 실행 계획 생성"""

    # 1. 필요 에이전트 식별
    required_agents = identify_agents(detected_keywords)

    # 2. 의존성 그래프 구축
    dependency_graph = build_dependency_graph(required_agents)

    # 3. 위상 정렬로 실행 순서 결정
    execution_order = topological_sort(dependency_graph)

    # 4. 병렬 실행 그룹 식별
    parallel_groups = identify_parallel_groups(execution_order, dependency_graph)

    # 5. 리소스 제약 적용
    optimized_plan = apply_constraints(parallel_groups, constraints)

    return ExecutionPlan(
        stages=optimized_plan,
        estimated_tokens=estimate_tokens(optimized_plan),
        critical_path=find_critical_path(dependency_graph)
    )


def identify_agents(keywords: list) -> list:
    """키워드 기반 에이전트 식별"""

    from agent_registry import AGENT_TRIGGERS

    agents = set()
    for keyword in keywords:
        for agent_id, triggers in AGENT_TRIGGERS.items():
            if keyword.lower() in [t.lower() for t in triggers]:
                agents.add(agent_id)

    return list(agents)
```

### 2. Conflict Resolver

에이전트 간 추천 충돌을 감지하고 해결합니다.

```yaml
conflict_resolver:
  conflict_types:
    recommendation_conflict:
      description: "동일 주제에 대한 상반된 추천"
      example: "Agent 02가 SDT 권장, Agent 03이 SDT 비판"
      resolution: "evidence_weighted_synthesis"

    resource_conflict:
      description: "동일 리소스에 대한 경쟁"
      example: "두 에이전트가 동시에 대량 토큰 요청"
      resolution: "priority_based_allocation"

    dependency_conflict:
      description: "순환 의존성"
      example: "Agent A → B → C → A"
      resolution: "break_cycle_at_weakest"

    vs_level_conflict:
      description: "VS 수준 불일치"
      example: "Full VS 결과와 Light VS 결과 통합"
      resolution: "vs_level_harmonization"
```

#### 충돌 해결 알고리즘

```python
def resolve_recommendation_conflict(
    recommendations: list[AgentOutput],
    conflict_type: str
) -> ResolvedRecommendation:
    """추천 충돌 해결"""

    if conflict_type == "recommendation_conflict":
        # 신뢰도 가중 합성
        weights = [r.confidence for r in recommendations]
        total_weight = sum(weights)

        synthesis = {
            "primary": max(recommendations, key=lambda r: r.confidence),
            "alternatives": [r for r in recommendations if r != primary],
            "confidence": weighted_average([r.confidence for r in recommendations], weights),
            "conflict_acknowledged": True,
            "resolution_rationale": generate_rationale(recommendations)
        }

        return ResolvedRecommendation(**synthesis)

    elif conflict_type == "vs_level_conflict":
        # Full VS 결과 우선
        full_vs = [r for r in recommendations if r.vs_level == "Full"]
        if full_vs:
            return full_vs[0].with_supplements(
                [r for r in recommendations if r.vs_level != "Full"]
            )

    return default_resolution(recommendations)


def detect_conflicts(outputs: list[AgentOutput]) -> list[Conflict]:
    """에이전트 출력 간 충돌 감지"""

    conflicts = []

    # 동일 주제에 대한 상반된 T-Score
    for i, o1 in enumerate(outputs):
        for o2 in outputs[i+1:]:
            if o1.topic == o2.topic:
                t_diff = abs(o1.t_score - o2.t_score)
                if t_diff > 0.3:  # T-Score 차이가 0.3 이상
                    conflicts.append(Conflict(
                        type="t_score_divergence",
                        agents=[o1.agent_id, o2.agent_id],
                        severity=t_diff
                    ))

    return conflicts
```

### 3. Quality Gate

각 단계에서 품질 기준 충족 여부를 검증합니다.

```yaml
quality_gate:
  gates:
    pre_execution:
      checks:
        - input_schema_valid
        - required_context_present
        - vs_level_appropriate
      action_on_fail: "request_missing_info"

    post_execution:
      checks:
        - output_schema_valid
        - t_score_present (for VS agents)
        - confidence_above_threshold
        - self_critique_present (for Full VS)
      action_on_fail: "retry_or_fallback"

    workflow_completion:
      checks:
        - all_required_agents_executed
        - no_unresolved_conflicts
        - overall_confidence_acceptable
      action_on_fail: "human_review_required"
```

#### 품질 게이트 구현

```python
class QualityGate:
    def __init__(self, gate_config: dict):
        self.config = gate_config

    def check_pre_execution(self, agent_input: dict) -> GateResult:
        """실행 전 품질 검사"""

        checks = {
            "input_schema_valid": self._validate_input_schema(agent_input),
            "required_context_present": self._check_context(agent_input),
            "vs_level_appropriate": self._check_vs_level(agent_input)
        }

        passed = all(checks.values())
        return GateResult(
            passed=passed,
            checks=checks,
            action="proceed" if passed else "request_missing_info"
        )

    def check_post_execution(self, agent_output: dict, vs_level: str) -> GateResult:
        """실행 후 품질 검사"""

        checks = {
            "output_schema_valid": self._validate_output_schema(agent_output),
            "confidence_above_threshold": agent_output.get("confidence", 0) >= 0.5
        }

        # VS 수준별 추가 검사
        if vs_level in ["Full", "Enhanced"]:
            checks["t_score_present"] = "t_scores" in agent_output.get("vs_metadata", {})

        if vs_level == "Full":
            checks["self_critique_present"] = "self_critique" in agent_output

        passed = all(checks.values())
        return GateResult(
            passed=passed,
            checks=checks,
            action="proceed" if passed else "retry_or_fallback"
        )

    def check_workflow_completion(self, workflow_result: dict) -> GateResult:
        """워크플로우 완료 품질 검사"""

        checks = {
            "all_agents_executed": self._check_completion(workflow_result),
            "no_unresolved_conflicts": len(workflow_result.get("conflicts", [])) == 0,
            "overall_confidence": self._calculate_overall_confidence(workflow_result) >= 0.6
        }

        passed = all(checks.values())
        return GateResult(
            passed=passed,
            checks=checks,
            action="complete" if passed else "human_review_required"
        )
```

### 4. Resource Manager

컨텍스트 예산, 시간, 병렬 실행 슬롯을 관리합니다.

```yaml
resource_manager:
  resources:
    context_budget:
      total: 150000
      allocation_strategy: "dynamic_proportional"

    parallel_slots:
      max_concurrent: 5
      allocation_strategy: "priority_queue"

    time_budget:
      default_timeout: 120  # seconds per agent
      workflow_timeout: 600  # seconds total

  policies:
    overrun_handling:
      context: "compress_previous_outputs"
      time: "skip_optional_agents"
      parallel: "queue_with_priority"
```

## 워크플로우 실행 모드

### 1. 자동 모드 (Automatic)

```yaml
automatic_mode:
  description: "사용자 요청 기반 완전 자동 실행"

  flow:
    1. parse_request: "키워드 감지 및 의도 분석"
    2. create_plan: "실행 계획 생성"
    3. execute_plan: "에이전트 순차/병렬 실행"
    4. resolve_conflicts: "충돌 자동 해결"
    5. synthesize_output: "결과 통합"

  example:
    user_request: "AI 기반 학습 지원 시스템의 효과를 메타분석하려고 해"
    detected_agents: [05, 06, 07, 10, 12, 16]
    execution_plan:
      - parallel: [05]
      - parallel: [06, 07]
      - sequential: [10, 12]
      - parallel: [16]
```

### 2. 인터랙티브 모드 (Interactive)

```yaml
interactive_mode:
  description: "단계별 사용자 확인 및 피드백 수렴"

  flow:
    1. propose_plan: "실행 계획 제안"
    2. await_approval: "사용자 승인 대기"
    3. execute_step: "단계별 실행"
    4. present_interim: "중간 결과 제시"
    5. await_feedback: "피드백 수렴"
    6. adjust_plan: "계획 조정"
    7. continue_or_complete: "계속 또는 완료"

  checkpoints:
    - after_theory_selection: "이론적 프레임워크 선택 후"
    - after_search_strategy: "검색 전략 수립 후"
    - after_analysis_plan: "분석 계획 수립 후"
```

### 3. 하이브리드 모드 (Hybrid)

```yaml
hybrid_mode:
  description: "중요 결정점에서만 사용자 확인"

  auto_proceed:
    - Light VS 에이전트
    - Enhanced VS 에이전트 (신뢰도 > 0.8)

  require_confirmation:
    - Full VS 에이전트 최종 선택
    - 충돌 해결 결과
    - 낮은 신뢰도 결과 (< 0.6)
```

## 실행 상태 관리

### 상태 전이 다이어그램

```
┌──────────────────────────────────────────────────────────────────┐
│                    Workflow State Machine                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│                        ┌─────────┐                               │
│                        │ CREATED │                               │
│                        └────┬────┘                               │
│                             │ start()                            │
│                             ▼                                    │
│                        ┌─────────┐                               │
│               ┌────────│ PLANNING│────────┐                      │
│               │        └────┬────┘        │                      │
│               │ error       │ plan_ready  │ cancel               │
│               ▼             ▼             ▼                      │
│          ┌────────┐   ┌──────────┐   ┌──────────┐               │
│          │ FAILED │   │ EXECUTING│   │ CANCELLED│               │
│          └────────┘   └────┬─────┘   └──────────┘               │
│               ▲            │                                     │
│               │ error      │ complete                            │
│               │            ▼                                     │
│               │       ┌──────────┐                               │
│               └───────│ CHECKING │                               │
│                       └────┬─────┘                               │
│                            │                                     │
│               ┌────────────┼────────────┐                        │
│               ▼            ▼            ▼                        │
│          ┌────────┐  ┌──────────┐  ┌──────────┐                 │
│          │ FAILED │  │ COMPLETED│  │ REVIEW   │                 │
│          └────────┘  └──────────┘  │ REQUIRED │                 │
│                                    └──────────┘                 │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### 상태 저장소

```yaml
workflow_state:
  id: string              # 워크플로우 고유 ID
  status: enum            # CREATED | PLANNING | EXECUTING | ...
  created_at: datetime
  updated_at: datetime

  plan:
    stages: list[Stage]
    current_stage: int
    total_stages: int

  execution:
    completed_agents: list[string]
    pending_agents: list[string]
    failed_agents: list[string]
    outputs: dict[string, AgentOutput]

  resources:
    tokens_used: int
    tokens_remaining: int
    time_elapsed: int

  conflicts:
    detected: list[Conflict]
    resolved: list[ResolvedConflict]
    pending: list[Conflict]

  quality:
    gate_results: list[GateResult]
    overall_confidence: float
```

## 에러 핸들링

### 에러 유형별 처리

```yaml
error_handling:
  agent_failure:
    retry_count: 2
    fallback: "use_cached_or_skip"
    notification: "log_and_continue"

  timeout:
    action: "terminate_current_agent"
    recovery: "use_partial_result_or_skip"

  quality_gate_failure:
    pre_execution: "request_additional_input"
    post_execution: "retry_with_adjusted_params"
    completion: "flag_for_human_review"

  resource_exhaustion:
    context_budget: "compress_and_continue"
    time_budget: "skip_optional_stages"
```

### 복구 전략

```python
def handle_agent_failure(
    agent_id: str,
    error: Exception,
    workflow_state: WorkflowState
) -> RecoveryAction:
    """에이전트 실패 처리"""

    # 재시도
    if workflow_state.retry_count[agent_id] < MAX_RETRIES:
        return RecoveryAction(
            type="retry",
            agent_id=agent_id,
            adjusted_params=adjust_params_for_retry(agent_id, error)
        )

    # 캐시 사용
    cached = get_cached_output(agent_id, workflow_state.context)
    if cached and cached.is_valid():
        return RecoveryAction(
            type="use_cache",
            agent_id=agent_id,
            cached_output=cached
        )

    # 건너뛰기 (선택적 에이전트만)
    if is_optional_agent(agent_id, workflow_state.plan):
        return RecoveryAction(
            type="skip",
            agent_id=agent_id,
            impact_assessment=assess_skip_impact(agent_id)
        )

    # 워크플로우 실패
    return RecoveryAction(
        type="fail_workflow",
        reason=f"Critical agent {agent_id} failed after all recovery attempts"
    )
```

## 모니터링 및 관찰성

### 메트릭 수집

```yaml
metrics:
  workflow_level:
    - workflow_duration_seconds
    - workflow_success_rate
    - agents_executed_count
    - conflicts_detected_count
    - quality_gate_pass_rate

  agent_level:
    - agent_execution_time_seconds
    - agent_token_usage
    - agent_confidence_score
    - agent_t_score_distribution

  resource_level:
    - context_budget_utilization
    - parallel_slot_utilization
    - cache_hit_rate
```

### 로깅

```python
class WorkflowLogger:
    def log_stage_start(self, stage: Stage):
        logger.info(f"[Workflow] Stage {stage.id} started", extra={
            "workflow_id": self.workflow_id,
            "stage": stage.id,
            "agents": stage.agents,
            "mode": stage.execution_mode
        })

    def log_agent_complete(self, agent_id: str, output: AgentOutput):
        logger.info(f"[Agent] {agent_id} completed", extra={
            "workflow_id": self.workflow_id,
            "agent_id": agent_id,
            "confidence": output.confidence,
            "t_score": output.vs_metadata.get("final_t_score"),
            "tokens_used": output.token_count
        })

    def log_conflict_detected(self, conflict: Conflict):
        logger.warning(f"[Conflict] {conflict.type} detected", extra={
            "workflow_id": self.workflow_id,
            "conflict_type": conflict.type,
            "involved_agents": conflict.agents,
            "severity": conflict.severity
        })
```

## 통합 예시

### 전체 연구 사이클 실행

```python
async def run_full_research_cycle(user_request: str, context: dict):
    """전체 연구 사이클 실행"""

    # 1. Governor 초기화
    governor = MetaAgentGovernor(
        mode="hybrid",
        resource_config={
            "context_budget": 150000,
            "parallel_slots": 3,
            "timeout": 600
        }
    )

    # 2. 워크플로우 생성
    workflow = governor.create_workflow(user_request, context)

    # 3. 실행 계획 수립
    plan = governor.planner.create_plan(workflow)
    logger.info(f"Execution plan: {plan.summary()}")

    # 4. 단계별 실행
    for stage in plan.stages:
        # Pre-execution 품질 검사
        pre_check = governor.quality_gate.check_pre_execution(stage)
        if not pre_check.passed:
            await governor.handle_gate_failure(pre_check)
            continue

        # 에이전트 실행
        if stage.is_parallel:
            results = await governor.execute_parallel(stage.agents)
        else:
            results = await governor.execute_sequential(stage.agents)

        # Post-execution 품질 검사
        for agent_id, result in results.items():
            post_check = governor.quality_gate.check_post_execution(
                result, get_vs_level(agent_id)
            )
            if not post_check.passed:
                result = await governor.handle_post_failure(agent_id, post_check)

        # 충돌 감지 및 해결
        conflicts = governor.conflict_resolver.detect_conflicts(list(results.values()))
        if conflicts:
            resolved = governor.conflict_resolver.resolve_all(conflicts)
            workflow.apply_resolutions(resolved)

    # 5. 최종 품질 검사
    completion_check = governor.quality_gate.check_workflow_completion(workflow)
    if not completion_check.passed:
        return await governor.request_human_review(workflow)

    # 6. 결과 합성 및 반환
    return governor.synthesize_output(workflow)
```

## 관련 문서

- `agent-registry.yaml`: 에이전트 의존성 및 병렬 그룹
- `agent-contract-schema.md`: 에이전트 I/O 스키마
- `context-budgeting.md`: 리소스 관리 상세
- `evaluation-harness.md`: 품질 검증 기준
