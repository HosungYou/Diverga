# Checkpoint Rules — v12.0.0

Human Checkpoint System enforcement rules for Diverga agents.

---

## Checkpoint Types

| Level | Behavior |
|-------|----------|
| **REQUIRED** | System STOPS. Cannot proceed without explicit approval. |
| **RECOMMENDED** | System PAUSES. Strongly suggests approval. |
| **OPTIONAL** | System ASKS. Defaults available if skipped. |

### Required Checkpoints (5 total)

| Checkpoint | When | What Happens |
|------------|------|--------------|
| `CP_RESEARCH_DIRECTION` | Research question finalized | Present VS options, WAIT for selection |
| `CP_PARADIGM_SELECTION` | Methodology approach | Ask Quantitative/Qualitative/Mixed |
| `CP_THEORY_SELECTION` | Framework chosen | Present alternatives with T-Scores |
| `CP_METHODOLOGY_APPROVAL` | Design complete | Detailed review required |

| Checkpoint | Gates |
|------------|-------|
| `CP_RESEARCH_DIRECTION` | 7 downstream agents |
| `CP_PARADIGM_SELECTION` | C1, C2, C3, V1-V5 |
| `CP_METHODOLOGY_APPROVAL` | D2, D4, E1, E2, E3, C5 |
| `SCH_DATABASE_SELECTION` | I2 |
| `SCH_SCREENING_CRITERIA` | I3 |

### Entry-Point Agents (always allowed)

A1, A5, G1, X1 — these agents have no prerequisites and can run without a checkpoint database.

---

## Rule 1: AskUserQuestion 도구 사용 의무

체크포인트 도달 시 반드시 `AskUserQuestion` 도구를 호출합니다.
텍스트로 묻는 것은 체크포인트 충족으로 인정되지 않습니다.

금지: "어떻게 하시겠습니까?" (텍스트 질문)
필수: AskUserQuestion 도구 호출 (구조화된 선택지)

---

## Rule 2: 전제조건 Gate (스킵 불가)

에이전트 호출 시, 해당 에이전트의 prerequisite 체크포인트가
이전에 사용자의 명시적 승인을 받았는지 확인합니다.
승인 이력이 없으면 해당 체크포인트부터 순서대로 진행합니다.
REQUIRED 체크포인트는 사용자 요청으로도 건너뛸 수 없습니다.

---

## Rule 3: Ad-hoc 호출 처리

에이전트를 직접 호출했을 때 (예: /diverga:c5):
1. Agent Prerequisite Map에서 전제조건 확인
2. 미완료 전제조건이 있으면 AskUserQuestion으로 해당 결정 요청
3. 모든 전제조건 통과 후 에이전트 본연의 작업 시작

---

## Rule 4: 동시 다중 에이전트 호출 처리

자연어로 다수 에이전트가 동시 트리거될 때:
1. 모든 트리거된 에이전트의 전제조건을 합집합(Union)으로 수집
2. 중복 제거 후 의존성 순서(dependency order)로 정렬
3. 각 전제조건을 순서대로 AskUserQuestion으로 질문 (한 번에 최대 4개)
4. 모든 전제조건 통과 후 에이전트들을 병렬 실행
5. 각 에이전트 실행 중 자체 체크포인트도 반드시 AskUserQuestion 호출

---

## Rule 5: Override Refusal

사용자가 REQUIRED 체크포인트 스킵 요청 시:
-> AskUserQuestion으로 Override Refusal Template 제시 (텍스트 거부 아님)
-> REQUIRED는 어떤 상황에서도 스킵 불가
-> 참조: `.claude/references/checkpoint-templates.md` -> Override Refusal Template

---

## Rule 6: MCP-First Verification (v8.2)

에이전트 실행 전: `diverga_check_prerequisites(agent_id)` 호출
-> `approved: true` -> 에이전트 실행 진행
-> `approved: false` -> `missing` 배열의 각 체크포인트에 대해 AskUserQuestion 호출
-> MCP 미가용 시: `research/decision-log.yaml` 직접 읽기
-> 대화 이력은 최후 수단 (세션 간 유지 안 됨)
