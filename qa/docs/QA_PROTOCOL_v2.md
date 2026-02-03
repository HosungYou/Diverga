# Diverga QA Protocol v2.2 - 완전 문서

## 개요

Diverga QA Protocol v2.2는 **자동화된 테스트 시뮬레이션**을 통해 Diverga 연구 방법론 플러그인을 검증하는 시스템입니다.

### 버전 비교

| 항목 | v1.0 | v2.0 | v2.1 | v2.2 (현재) |
|------|------|------|------|-------------|
| **실행 방식** | Mock 스크립트 | 실제 대화 | 실제 대화 | **자동화 시뮬레이션** |
| **사용자 입력** | 단답식 선택 | 복잡한 질문 | 복잡한 질문 | **사전 정의 템플릿** |
| **대화 추출** | 수동 기록 | JSONL 파싱 | 세션 폴더 기반 | **자동 생성** |
| **대화 저장** | 없음 | YAML만 | RAW JSON + MD | **RAW JSON + MD** |
| **폴더 구조** | 단일 폴더 | 단일 폴더 | 세션별 폴더 | **세션별 폴더** |
| **수동 개입** | 필수 | 필수 | 필수 | **불필요** |

### v2.2 신규 기능

1. **자동화된 테스트 시뮬레이션** - 사용자 입력 없이 전체 테스트 자동 실행
2. **사전 정의 응답 템플릿** - 각 시나리오별 현실적인 AI 응답 템플릿
3. **CLI 기반 실행** - 단일 명령으로 테스트 실행 및 결과 저장

### v2.1 기능 (유지)

1. **세션 기반 폴더 관리** - 각 테스트 세션을 개별 폴더로 관리
2. **RAW 대화 추출** - 완전한 대화 내용을 JSON 및 Markdown으로 저장
3. **GitHub 배포 가능** - 모든 대화 내용을 버전 관리 및 공유

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

## 디렉토리 구조 (v2.2)

```
qa/
├── README.md                    # 빠른 시작 가이드
├── run_tests.py                 # 메인 테스트 러너
├── .gitignore                   # Git 제외 패턴 (대용량 JSONL 등)
├── docs/
│   ├── QA_PROTOCOL_v2.md        # 이 문서
│   ├── CHECKPOINT_SPEC.md       # 체크포인트 명세
│   └── AGENT_TRIGGER_SPEC.md    # 에이전트 트리거 명세
├── runners/
│   ├── __init__.py              # 모듈 익스포트
│   ├── extract_conversation.py  # 대화 추출기
│   └── automated_test.py        # [v2.2 NEW] 자동화 테스트 시뮬레이터
├── protocol/
│   ├── test_meta_002.yaml       # 메타분석 시나리오
│   ├── test_qual_002.yaml       # 질적연구 시나리오 (한국어)
│   ├── test_mixed_002.yaml      # 혼합방법 시나리오
│   └── test_human_002.yaml      # 휴먼화 시나리오
└── reports/
    ├── README.md                # 리포트 가이드
    ├── sessions/                # 세션별 폴더
    │   ├── META-002/            # META-002 테스트 세션
    │   │   ├── README.md                    # 세션 개요
    │   │   ├── conversation_transcript.md   # 사람이 읽기 쉬운 대화록
    │   │   ├── conversation_raw.json        # RAW 대화 데이터
    │   │   ├── META-002_test_result.yaml    # 테스트 평가 결과
    │   │   └── META-002_report.html         # HTML 보고서
    │   ├── QUAL-002/            # QUAL-002 테스트 세션
    │   └── MIXED-002/           # (예정)
    └── (legacy files...)        # v1.0 레거시 파일
```

---

## 세션 기반 폴더 관리 (v2.1 NEW)

### 개요

v2.1부터 각 테스트 세션은 **독립된 폴더**에서 관리됩니다.
이를 통해 RAW 대화 내용을 GitHub에 배포하고 버전 관리할 수 있습니다.

### 세션 폴더 구조

```
reports/sessions/{SCENARIO-ID}/
├── README.md                    # 세션 개요 및 테스트 결과 요약
├── conversation_transcript.md   # 사람이 읽기 쉬운 마크다운 형식
├── conversation_raw.json        # 프로그래밍 접근용 RAW JSON
├── {SCENARIO-ID}_test_result.yaml   # 평가 결과
├── {SCENARIO-ID}_report.html        # 시각적 HTML 리포트
└── session_{session-id}.jsonl       # [Git 제외] 원본 세션 로그
```

### 파일별 용도

| 파일 | 용도 | Git 포함 | 크기 |
|------|------|----------|------|
| `README.md` | 세션 개요, GitHub 미리보기 | ✅ | ~2KB |
| `conversation_transcript.md` | 전체 대화 읽기 | ✅ | ~500KB |
| `conversation_raw.json` | API/스크립트 접근 | ✅ | ~600KB |
| `*_test_result.yaml` | 테스트 평가 | ✅ | ~6KB |
| `*_report.html` | 브라우저 리포트 | ✅ | ~16KB |
| `session_*.jsonl` | 원본 Claude Code 로그 | ❌ | ~8MB |

### RAW 대화 추출 프로토콜

세션 JSONL에서 RAW 대화를 추출하는 절차:

**Step 1: Claude Code 세션 로그 찾기**
```bash
# 세션 로그 위치
~/.claude/projects/{project-id}/{session-id}.jsonl
```

**Step 2: 세션 폴더 생성**
```bash
mkdir -p qa/reports/sessions/{SCENARIO-ID}
```

**Step 3: RAW 대화 추출**
```python
import json
from pathlib import Path
from datetime import datetime

session_file = '~/.claude/projects/.../session.jsonl'
output_dir = Path('qa/reports/sessions/{SCENARIO-ID}')

# JSONL 파싱
entries = []
with open(session_file, 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():
            entries.append(json.loads(line))

# user/assistant 메시지만 추출
conversation = []
for e in entries:
    if e.get('type') in ['user', 'assistant']:
        conversation.append({
            'type': e['type'],
            'timestamp': e.get('timestamp', ''),
            'content': e.get('message', {}).get('content', '')
        })

# JSON 저장
with open(output_dir / 'conversation_raw.json', 'w') as f:
    json.dump(conversation, f, indent=2, ensure_ascii=False)

# Markdown 저장
with open(output_dir / 'conversation_transcript.md', 'w') as f:
    f.write("# Session Transcript\n\n")
    for i, msg in enumerate(conversation, 1):
        role = "👤 USER" if msg['type'] == 'user' else "🤖 ASSISTANT"
        f.write(f"## Turn {i}: {role}\n\n")
        f.write(f"{msg['content']}\n\n---\n\n")
```

**Step 4: 자동 추출 CLI**
```bash
python qa/runners/extract_conversation.py \
  --session ~/.claude/projects/{project-id}/{session-id}.jsonl \
  --output qa/reports/sessions/{SCENARIO-ID}/ \
  --scenario-id {SCENARIO-ID}
```

### 새 세션 추가 워크플로우

```
1. Claude Code에서 테스트 대화 진행
   └─ /diverga:research-coordinator 호출
   └─ 시나리오 대로 대화 진행

2. 세션 완료 후 폴더 생성
   └─ mkdir -p qa/reports/sessions/{SCENARIO-ID}

3. 대화 추출
   └─ python extract_conversation.py ...

4. 평가 실행
   └─ python run_tests.py --evaluate-extracted ...

5. README.md 생성 (자동 또는 수동)
   └─ 세션 요약, 테스트 결과 포함

6. Git 커밋 및 푸시
   └─ git add qa/reports/sessions/{SCENARIO-ID}/
   └─ git commit -m "feat(qa): Add {SCENARIO-ID} session"
   └─ git push
```

### .gitignore 설정

대용량 원본 JSONL 파일은 Git에서 제외합니다:

```gitignore
# qa/.gitignore
reports/sessions/**/session_*.jsonl
```

---

## 자동화된 테스트 시뮬레이션 (v2.2 NEW)

### 개요

v2.2부터 **완전 자동화된 테스트**가 가능합니다. 사용자 입력 없이 프로토콜 YAML 파일을 기반으로 전체 대화를 시뮬레이션하고 결과를 저장합니다.

### 작동 원리

```
┌─────────────────────────────────────────────────────────────────┐
│                AUTOMATED TEST SIMULATION FLOW                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Protocol YAML 로드                                          │
│     └─ qa/protocol/test_{scenario}.yaml                         │
│                                                                  │
│  2. 응답 템플릿 매칭                                             │
│     └─ RESPONSE_TEMPLATES[scenario][turn_number]                │
│                                                                  │
│  3. 턴별 시뮬레이션                                              │
│     ├─ User input → Protocol YAML                               │
│     └─ Assistant response → Pre-defined Template                │
│                                                                  │
│  4. 검증 및 탐지                                                 │
│     ├─ 체크포인트 탐지 (🔴, 🟠, 🟡)                              │
│     ├─ 에이전트 호출 추적                                        │
│     └─ VS 옵션 및 T-Score 추출                                  │
│                                                                  │
│  5. 결과 저장                                                    │
│     ├─ conversation_transcript.md                               │
│     ├─ conversation_raw.json                                    │
│     ├─ {SCENARIO}_test_result.yaml                              │
│     └─ README.md                                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### CLI 사용법

```bash
# 특정 시나리오 실행
python3 qa/runners/automated_test.py --scenario QUAL-002

# 모든 시나리오 실행
python3 qa/runners/automated_test.py --all

# 출력 디렉토리 지정
python3 qa/runners/automated_test.py --scenario META-002 --output qa/reports/sessions
```

### 응답 템플릿 구조

`automated_test.py`에 각 시나리오별 응답 템플릿이 정의되어 있습니다:

```python
RESPONSE_TEMPLATES = {
    "QUAL-002": {
        1: """🔴 CHECKPOINT: CP_PARADIGM_SELECTION

연구 맥락에서 **질적 연구 (현상학)** 접근이 감지되었습니다.

[A] 기술적 현상학 (Husserl) - T=0.55
[B] 해석학적 현상학 (van Manen) - T=0.40 ⭐
[C] 실존적 현상학 (Heidegger) - T=0.30

어떤 방향으로 진행하시겠습니까?""",

        2: """Husserl과 Heidegger의 차이에 대해 설명드리겠습니다...

어떤 현상학적 접근을 선택하시겠습니까?""",

        # ... 각 턴별 응답
    },

    "META-002": {
        1: """🔴 CHECKPOINT: CP_RESEARCH_DIRECTION

Based on your research question, I'll present three approaches...

Which direction would you like to pursue?""",

        # ... 각 턴별 응답
    }
}
```

### 새 시나리오 추가하기

1. **Protocol YAML 작성**
   ```yaml
   # qa/protocol/test_new_scenario.yaml
   scenario_id: NEW-001
   name: "New Scenario"
   conversation_flow:
     - turn: 1
       user: "Initial user message"
       expected_behavior:
         checkpoint: CP_SOME_CHECKPOINT
         halt: true
   ```

2. **응답 템플릿 추가**
   ```python
   # automated_test.py
   RESPONSE_TEMPLATES["NEW-001"] = {
       1: """🔴 CHECKPOINT: CP_SOME_CHECKPOINT

       Your simulated response here...""",
       2: """Next turn response..."""
   }
   ```

3. **테스트 실행**
   ```bash
   python3 qa/runners/automated_test.py --scenario NEW-001
   ```

### 출력 파일

자동 테스트는 다음 파일들을 생성합니다:

| 파일 | 설명 |
|------|------|
| `conversation_transcript.md` | 마크다운 형식의 전체 대화록 |
| `conversation_raw.json` | 프로그래밍 접근용 JSON 데이터 |
| `{SCENARIO}_test_result.yaml` | 테스트 평가 결과 (PASSED/FAILED) |
| `README.md` | 세션 개요 및 요약 |

### 검증 항목

자동 테스트는 다음을 검증합니다:

| 항목 | 설명 | 자동 탐지 |
|------|------|----------|
| **체크포인트** | 🔴/🟠/🟡 체크포인트 트리거 | ✅ 패턴 매칭 |
| **에이전트 호출** | Task tool 호출 추적 | ✅ 응답 파싱 |
| **VS 옵션** | T-Score 기반 대안 제시 | ✅ 정규식 추출 |
| **언어 일관성** | 입력-출력 언어 매칭 | ✅ 자동 감지 |

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
| **v2.2** | 2026-01-29 | 자동화된 테스트 시뮬레이션, 사전 정의 응답 템플릿, CLI 기반 실행 |
| v2.1 | 2026-01-29 | 세션 기반 폴더 관리, RAW 대화 추출 프로토콜, GitHub 배포 지원 |
| v2.0 | 2026-01-29 | 실제 대화 테스트, 복잡한 입력 유형, JSONL 추출 |
| v1.0 | 2026-01-15 | 초기 Mock 스크립트 버전 |

### v2.2 변경 상세

1. **자동화된 테스트 시뮬레이션**
   - `automated_test.py`: 사용자 입력 없이 전체 테스트 자동 실행
   - Protocol YAML의 `conversation_flow`를 기반으로 대화 시뮬레이션
   - 각 턴별 사전 정의된 응답 템플릿 사용

2. **사전 정의 응답 템플릿**
   - `RESPONSE_TEMPLATES` 딕셔너리에 시나리오별 응답 정의
   - 현실적인 체크포인트, VS 옵션, T-Score 포함
   - 다국어 지원 (QUAL-002는 한국어)

3. **CLI 기반 실행**
   - `--scenario`: 특정 시나리오 실행
   - `--all`: 모든 시나리오 실행
   - `--output`: 출력 디렉토리 지정

### v2.1 변경 상세

1. **세션 기반 폴더 관리**
   - 각 테스트 세션을 `reports/sessions/{SCENARIO-ID}/` 폴더에 저장
   - 모든 관련 파일 (대화록, 평가, 리포트)을 한 곳에 관리

2. **RAW 대화 추출**
   - `conversation_raw.json`: 프로그래밍 접근용 완전한 대화 데이터
   - `conversation_transcript.md`: 사람이 읽기 쉬운 마크다운 형식
   - JSONL → JSON/Markdown 변환 자동화

3. **GitHub 배포 최적화**
   - 대용량 JSONL 파일 Git 제외 (`.gitignore`)
   - 추출된 JSON/Markdown 파일만 버전 관리
   - 각 세션 폴더에 README.md로 GitHub 미리보기 지원

---

## 라이선스

MIT License - Diverga Project
