# Diverga QA Protocol v2.0 - 완전 문서

## 개요

Diverga QA Protocol v2.0은 **실제 Claude Code 대화**를 통해 Diverga 연구 방법론 플러그인을 검증하는 시스템입니다.

### v1.0 vs v2.0 비교

| 항목 | v1.0 (이전) | v2.0 (현재) |
|------|-------------|-------------|
| **실행 방식** | Mock Python 스크립트 | Claude Code 내 실제 대화 |
| **사용자 입력** | 단답식 선택 | 복잡한 기술적 질문 및 도전 |
| **응답 언어** | 한영 혼합 | 사용자 입력 언어 따라가기 |
| **대화 추출** | 수동 기록 | JSONL 자동 파싱 |
| **평가 방식** | 수동 체크리스트 | 자동화된 검증 스크립트 |

---

## 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                     QA Protocol v2.0 Architecture                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   Protocol   │    │   Claude     │    │   Session    │       │
│  │    YAML      │───▶│    Code      │───▶│    JSONL     │       │
│  │  (expected)  │    │  (실제대화)   │    │   (로그)     │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│         │                                       │                │
│         │            ┌──────────────┐           │                │
│         └───────────▶│  Extractor   │◀──────────┘                │
│                      │   Script     │                            │
│                      └──────────────┘                            │
│                             │                                    │
│                      ┌──────────────┐                            │
│                      │  Evaluator   │                            │
│                      │   Report     │                            │
│                      └──────────────┘                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 디렉토리 구조

```
qa/
├── README.md                    # 빠른 시작 가이드
├── run_tests.py                 # 메인 테스트 러너
├── docs/
│   ├── QA_PROTOCOL_v2.md        # 이 문서
│   ├── CHECKPOINT_SPEC.md       # 체크포인트 명세
│   └── AGENT_TRIGGER_SPEC.md    # 에이전트 트리거 명세
├── runners/
│   ├── __init__.py              # 모듈 익스포트
│   └── extract_conversation.py  # 대화 추출기 (650+ lines)
├── protocol/
│   ├── test_meta_002.yaml       # 메타분석 시나리오
│   ├── test_qual_002.yaml       # 질적연구 시나리오 (한국어)
│   ├── test_mixed_002.yaml      # 혼합방법 시나리오
│   └── test_human_002.yaml      # 휴먼화 시나리오
└── reports/
    ├── real-transcripts/        # 추출된 대화
    └── evaluations/             # 평가 결과
```

---

## 핵심 컴포넌트

### 1. ConversationExtractor

Claude Code 세션 로그(JSONL)를 파싱하여 구조화된 대화 데이터를 추출합니다.

**주요 기능:**
- JSONL 파싱 및 턴별 구조화
- 체크포인트 탐지 및 추적
- 에이전트 호출 추적 (Task tool)
- 사용자 입력 유형 분류
- VS 옵션 및 T-Score 추출
- 언어 자동 감지

**사용법:**
```python
from qa.runners import ConversationExtractor

extractor = ConversationExtractor(
    session_path="~/.claude/projects/xxx/session.jsonl",
    scenario_id="META-002"
)
result = extractor.extract()

print(f"Total turns: {result.total_turns}")
print(f"Checkpoints: {len(result.checkpoints)}")
print(f"Agents: {len(result.agents_invoked)}")
```

### 2. ConversationEvaluator

추출된 대화를 기대 시나리오와 비교하여 평가합니다.

**평가 항목:**
- 체크포인트 컴플라이언스 (100% 필수)
- 언어 일관성
- 에이전트 호출 정확도
- 기술적 깊이
- 컨텍스트 유지

**사용법:**
```python
from qa.runners import ConversationEvaluator

evaluator = ConversationEvaluator(
    extracted=result,
    expected_path="qa/protocol/test_meta_002.yaml"
)
report = evaluator.evaluate()

print(f"Pass rate: {report['summary']['pass_rate']}%")
```

### 3. DivergaQARunner

테스트 실행 및 리포트 생성을 오케스트레이션합니다.

**사용법:**
```bash
# 프로토콜 검증
python qa/run_tests.py --all

# 추출된 대화 평가
python qa/run_tests.py --evaluate-extracted \
  --input qa/reports/real-transcripts/META-002.yaml \
  --expected qa/protocol/test_meta_002.yaml

# HTML 리포트 생성
python qa/run_tests.py --all --report-format html --output qa/reports/
```

---

## 테스트 시나리오 명세

### META-002: Advanced Meta-Analysis

| 속성 | 값 |
|------|-----|
| **복잡도** | HIGH |
| **예상 턴 수** | 10-15 |
| **언어** | English |
| **패러다임** | Quantitative |
| **관련 에이전트** | C5, C6, C7, B1, B3, E1, E5, A2 |

**테스트 항목:**
1. Hedges' g vs Cohen's d 기술적 질문
2. 소표본 random-effects 가정 도전
3. 이론적 프레임워크로 에이전트 전환
4. Gray literature 포함 결정
5. Bayesian 대안 탐색
6. Subgroup 분석 실현 가능성

### QUAL-002: Advanced Phenomenology (Korean)

| 속성 | 값 |
|------|-----|
| **복잡도** | HIGH |
| **예상 턴 수** | 8-12 |
| **언어** | Korean |
| **패러다임** | Qualitative |
| **관련 에이전트** | A1, A5, C2, D2, E2, A3, C3 |

**테스트 항목:**
1. Husserl vs Heidegger 철학적 비교
2. van Manen 해석학적 현상학 선택
3. Devil's advocate 리뷰어 대비
4. n=5 표본 크기 정당화
5. 패러다임 재고려 (혼합 방법)
6. 한국어 응답 일관성

### MIXED-002: Complex Mixed Methods

| 속성 | 값 |
|------|-----|
| **복잡도** | HIGH |
| **예상 턴 수** | 8-10 |
| **언어** | English |
| **패러다임** | Mixed Methods |
| **관련 에이전트** | A1, C3, E3, D1, D2 |

**테스트 항목:**
1. Morse notation 설명
2. Joint display 구조 예시
3. 타임라인 제약 처리
4. 표본 크기 비율 권장

### HUMAN-002: Academic Humanization

| 속성 | 값 |
|------|-----|
| **복잡도** | MEDIUM |
| **예상 턴 수** | 6-8 |
| **언어** | English |
| **패러다임** | Any |
| **관련 에이전트** | G5, G6, F5, A4 |

**테스트 항목:**
1. AI 패턴 탐지 및 분류
2. 탐지 로직 설명
3. 휴먼화 변환 모드
4. AI 공개 윤리 논의

---

## 사용자 입력 유형

QA 프로토콜은 다음 복잡한 사용자 상호작용을 테스트합니다:

| 유형 | 설명 | 탐지 패턴 |
|------|------|----------|
| `TECHNICAL_FOLLOW_UP` | 통계/방법론 심화 질문 | "why", "how", "explain", "difference" |
| `METHODOLOGICAL_CHALLENGE` | 접근법 비판 | "but", "concern", "assumption", "violated" |
| `AGENT_TRANSITION_REQUEST` | 에이전트 전환 요청 | "wait", "before we", "step back", "first" |
| `SCOPE_CHANGE` | 연구 범위 수정 | "actually", "include", "add" |
| `ALTERNATIVE_EXPLORATION` | 미제시 옵션 질문 | "what about", "why not", "didn't mention" |
| `PRACTICAL_CONSTRAINT` | 실무적 제약 | "only have", "minimum", "enough" |
| `SELECTION` | 옵션 선택 | `[A]`, `[B]`, "I choose" |
| `APPROVAL` | 승인 및 진행 | "approved", "proceed", "confirm" |

---

## 체크포인트 시스템

### 레벨 정의

| 레벨 | 아이콘 | 동작 | 예시 |
|------|--------|------|------|
| **RED** | 🔴 | 반드시 HALT, 승인 대기 | CP_RESEARCH_DIRECTION |
| **ORANGE** | 🟠 | HALT 권장 | CP_SCOPE_DECISION |
| **YELLOW** | 🟡 | 진행 가능, 로깅 | CP_MINOR_ADJUSTMENT |

### 검증 규칙

```yaml
checkpoint_compliance:
  target: 100%
  red_checkpoints_must_halt: true
  behavior:
    - STOP immediately at checkpoint
    - Present VS options with T-Scores
    - WAIT for explicit user selection
    - DO NOT proceed without approval
```

---

## 평가 지표

| 지표 | 목표 | 설명 |
|------|------|------|
| **Checkpoint Compliance** | 100% | 모든 🔴 체크포인트 HALT |
| **Technical Depth** | ≥90% | 후속 질문 정확 응답 |
| **Methodological Accuracy** | ≥90% | 도전에 유효한 응답 |
| **Context Retention** | ≥95% | 에이전트 전환 후 맥락 유지 |
| **Language Consistency** | 100% | 응답 언어 = 입력 언어 |
| **Agent Transition** | ≥90% | 매끄러운 핸드오프 |

---

## CLI 명령어

### 프로토콜 검증

```bash
# 모든 시나리오 검증
python qa/run_tests.py --all

# 상세 출력
python qa/run_tests.py --all --verbose
```

### 대화 추출

```bash
# 기본 추출
python qa/runners/extract_conversation.py \
  --session ~/.claude/projects/{project-id}/{session}.jsonl \
  --output qa/reports/real-transcripts/

# 시나리오 ID 지정
python qa/runners/extract_conversation.py \
  --session ~/.claude/projects/{project-id}/{session}.jsonl \
  --scenario-id META-002 \
  --output qa/reports/real-transcripts/
```

### 평가 실행

```bash
# 추출된 대화 평가
python qa/run_tests.py --evaluate-extracted \
  --input qa/reports/real-transcripts/META-002.yaml \
  --expected qa/protocol/test_meta_002.yaml

# 세션 직접 평가 (추출 + 평가)
python qa/run_tests.py --evaluate-session \
  --input ~/.claude/projects/{id}/{session}.jsonl \
  --expected qa/protocol/test_meta_002.yaml \
  --scenario-id META-002
```

### 리포트 생성

```bash
# YAML 리포트 (기본)
python qa/run_tests.py --all --output qa/reports/

# HTML 리포트
python qa/run_tests.py --all --report-format html --output qa/reports/

# JSON 리포트
python qa/run_tests.py --all --report-format json --output qa/reports/
```

---

## 세션 로그 위치

Claude Code 세션 로그는 다음 위치에 저장됩니다:

```
~/.claude/projects/{project-id}/{session-id}.jsonl
```

### JSONL 형식

```json
{"type": "user", "content": "...", "timestamp": "..."}
{"type": "assistant", "content": "...", "tool_calls": [...], "timestamp": "..."}
{"type": "tool_result", "tool_name": "...", "result": {...}}
```

---

## 문제 해결

### 일반적인 문제

| 문제 | 해결 방법 |
|------|----------|
| `ModuleNotFoundError: yaml` | `pip install pyyaml` |
| 세션 파일 없음 | 올바른 project-id 확인 |
| 체크포인트 미탐지 | 패턴 정규식 확인 |
| 에이전트 미인식 | Tool call 구조 확인 |

### 디버깅

```python
# 상세 추출 로그
extractor = ConversationExtractor(session_path, scenario_id)
extractor.verbose = True  # 추가 로깅
result = extractor.extract()
```

---

## 버전 히스토리

| 버전 | 날짜 | 변경 사항 |
|------|------|----------|
| v2.0 | 2026-01-29 | 실제 대화 테스트, 복잡한 입력 유형, JSONL 추출 |
| v1.0 | 2026-01-15 | 초기 Mock 스크립트 버전 |

---

## 라이선스

MIT License - Diverga Project
