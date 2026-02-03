# Diverga QA Protocol v3.0

**True Automated Testing via CLI**

## Overview

Diverga QA Protocol v3.0은 실제 AI 응답을 CLI 도구를 통해 자동으로 캡처하는 테스트 프레임워크입니다.

### v2.x vs v3.0 비교

| 항목 | v2.x (시뮬레이션) | v3.0 (진정한 자동화) |
|------|------------------|---------------------|
| **AI 응답** | `RESPONSE_TEMPLATES` dict | **실제 AI 생성 응답** |
| **실행 방식** | Python 시뮬레이터 | **CLI 비대화형 모드** |
| **검증 가치** | 프로토콜 형식만 | **실제 기능 검증** |
| **API 호출** | 없음 | 실제 토큰 소비 |

---

## Quick Start

### 단일 시나리오 실행 (v3.0 권장)

```bash
# 실제 AI 테스트
python3 qa/runners/cli_test_runner.py --scenario QUAL-002 --cli claude

# Dry Run (API 호출 없음)
python3 qa/runners/cli_test_runner.py --scenario QUAL-002 --dry-run

# Verbose 모드
python3 qa/runners/cli_test_runner.py --scenario QUAL-002 -v
```

### 모든 시나리오 실행

```bash
# 실제 AI로 모든 시나리오 테스트
./qa/run_all_scenarios.sh

# Dry Run 모드
./qa/run_all_scenarios.sh --dry-run

# 다른 CLI 도구 사용
./qa/run_all_scenarios.sh --cli opencode
```

### v2.x 시뮬레이션 (Legacy)

```bash
# 시뮬레이션 모드 (하드코딩된 응답)
python3 qa/runners/automated_test.py --scenario QUAL-002
```

---

## 디렉토리 구조

```
qa/
├── README.md                    # 이 문서
├── run_all_scenarios.sh         # v3.0 배치 테스트 스크립트
├── run_tests.py                 # v2.x 테스트 러너
│
├── protocol/                    # 테스트 시나리오 정의
│   ├── test_qual_001.yaml       # 기본 질적 연구
│   ├── test_qual_002.yaml       # 고급 현상학 (한국어)
│   ├── test_meta_001.yaml       # 기본 메타분석
│   ├── test_meta_002.yaml       # 고급 메타분석 (영어)
│   ├── test_mixed_001.yaml      # 혼합방법
│   ├── test_mixed_002.yaml      # 고급 혼합방법
│   ├── test_human_001.yaml      # 인간 체크포인트
│   └── test_human_002.yaml      # 고급 체크포인트
│
├── runners/                     # 테스트 실행기
│   ├── __init__.py
│   ├── cli_test_runner.py       # v3.0 CLI 기반 자동화 (NEW)
│   ├── automated_test.py        # v2.x 시뮬레이터
│   ├── extract_conversation.py  # JSONL 세션 파싱
│   ├── checkpoint_validator.py  # 체크포인트 검증
│   └── agent_tracker.py         # 에이전트 추적
│
└── reports/                     # 테스트 결과
    ├── sessions/                # 세션별 결과
    │   └── QUAL-002/
    │       ├── README.md
    │       ├── conversation_transcript.md
    │       ├── conversation_raw.json
    │       └── QUAL-002_test_result.yaml
    └── real-transcripts/        # 실제 대화 기록
```

---

## CLI Test Runner (v3.0)

### CLITestRunner 클래스

```python
from qa.runners import CLITestRunner

runner = CLITestRunner(
    scenario_id='QUAL-002',      # 시나리오 ID
    cli_tool='claude',           # CLI 도구 (claude, opencode, codex)
    verbose=True,                # 상세 출력
    dry_run=False,               # Dry Run 모드
    timeout=300                  # 턴당 타임아웃 (초)
)

session = runner.run()
runner.save_results('qa/reports/sessions')
```

### 지원 CLI 도구

| CLI | 명령 | 세션 지속 |
|-----|------|----------|
| `claude` | `claude -p "message"` | `--continue` |
| `opencode` | `opencode run "message"` | - |
| `codex` | `codex exec "message"` | `--resume` |

### 출력 파일

| 파일 | 설명 |
|------|------|
| `README.md` | 세션 개요 및 메트릭 |
| `conversation_transcript.md` | 실제 AI 응답 포함 대화 기록 |
| `conversation_raw.json` | 메타데이터 포함 RAW 데이터 |
| `{SCENARIO}_test_result.yaml` | 테스트 결과 및 검증 |

---

## 테스트 시나리오

### QUAL-002: 고급 현상학 (한국어)

```yaml
scenario_id: QUAL-002
name: "Advanced Phenomenology with Paradigm Debates"
paradigm: qualitative
complexity_level: HIGH
language: "Korean (user input) -> Korean (response)"
expected_turns: 8-12

checkpoints_expected:
  - CP_PARADIGM_SELECTION (RED)
  - CP_METHODOLOGY_APPROVAL (RED)
  - CP_PARADIGM_RECONSIDERATION (ORANGE)
  - CP_ANALYSIS_APPROACH (ORANGE)

agents_involved:
  - A1-ResearchQuestionRefiner
  - A5-ParadigmWorldviewAdvisor
  - C2-QualitativeDesignConsultant
  - D2-InterviewFocusGroupSpecialist
  - E2-QualitativeCodingSpecialist
  - A3-DevilsAdvocate
```

### META-002: 고급 메타분석 (영어)

```yaml
scenario_id: META-002
name: "Advanced Meta-Analysis with Theoretical Debates"
paradigm: quantitative
language: English
expected_turns: 8-12
```

### MIXED-002: 혼합방법

```yaml
scenario_id: MIXED-002
paradigm: mixed
language: English
expected_turns: 8-10
```

### HUMAN-002: 학술 휴먼화

```yaml
scenario_id: HUMAN-002
paradigm: qualitative
language: English
expected_turns: 6-8
```

---

## 검증 메트릭

### 체크포인트 탐지

```python
# 체크포인트 패턴
patterns = [
    r'🔴\s*CHECKPOINT[:\s]+(\w+)',   # RED
    r'🟠\s*CHECKPOINT[:\s]+(\w+)',   # ORANGE
    r'🟡\s*CHECKPOINT[:\s]+(\w+)',   # YELLOW
    r'CHECKPOINT[:\s]+(CP_\w+)',
]
```

### 에이전트 탐지

```python
# 에이전트 참조 패턴
patterns = [
    r'diverga:([a-z]\d+)',           # diverga:a1
    r'([A-Z]\d+)-\w+',               # A1-ResearchQuestionRefiner
    r'Task.*subagent_type.*diverga:(\w+)',
]
```

### VS 옵션 추출

```python
# T-Score 포함 옵션
pattern = r'\[([A-Z])\]\s*([^(]+?)\s*\(T\s*=\s*(\d+\.?\d*)\)'
# 결과: {'option': 'B', 'label': '해석학적 현상학', 't_score': 0.40}
```

---

## 테스트 결과 예시

### QUAL-002 실행 결과 (2026-01-29)

```
============================================================
Diverga QA Protocol v3.0 - True Automated Testing
Scenario: QUAL-002
CLI Tool: claude
Mode: LIVE
============================================================

[Turn 1] INITIAL_REQUEST
  Received: 792 chars
  ✓ Completed (CP: 1, Agents: 0)

[Turn 2] METHODOLOGICAL_CHALLENGE
  Received: 1810 chars
  ✓ Completed (CP: 1, Agents: 0)

[Turn 3] SELECTION
  Received: 2469 chars
  ✓ Completed (CP: 1, Agents: 0)

[Turn 4] ALTERNATIVE_EXPLORATION
  Received: 3348 chars
  ✓ Completed (CP: 1, Agents: 0)

[Turn 5] PRACTICAL_CONSTRAINT
  Received: 2966 chars
  ✓ Completed (CP: 1, Agents: 0)

[Turn 6] PARADIGM_QUESTIONING
  Received: 3315 chars
  ✓ Completed (CP: 1, Agents: 0)

[Turn 7] SELECTION
  Received: 5327 chars
  ✓ Completed (CP: 1, Agents: 0)

[Turn 8] APPROVAL
  Received: 889 chars
  ✓ Completed (CP: 1, Agents: 0)

============================================================
Test Completed: QUAL-002
Turns: 8
Checkpoints: 8
============================================================
```

### 메트릭 요약

| 메트릭 | 값 |
|--------|-----|
| Total Turns | 8 |
| Checkpoints Found | 8 |
| Total Response Chars | ~21,000 |
| Test Duration | ~4 minutes |

---

## User Input Types

| Type | Description | Example |
|------|-------------|---------|
| `INITIAL_REQUEST` | 연구 주제 제시 | "교사들이 AI 도구를 경험하는 현상을 탐구하고 싶습니다" |
| `TECHNICAL_FOLLOW_UP` | 기술적 질문 | "Husserl의 bracket과 Heidegger의 hermeneutic circle 차이는?" |
| `METHODOLOGICAL_CHALLENGE` | 방법론적 도전 | "왜 IPA 대신 van Manen인가요?" |
| `SELECTION` | 옵션 선택 | "[B] 해석학적 현상학 (van Manen)" |
| `PRACTICAL_CONSTRAINT` | 현실적 제약 | "참여자가 5명밖에 안 되는데 충분할까요?" |
| `PARADIGM_QUESTIONING` | 패러다임 재고 | "혼합 방법으로 가는 게 더 나을까요?" |
| `APPROVAL` | 승인 | "승인합니다. 이 방법론으로 진행하겠습니다." |

---

## Checkpoint Levels

| Level | Symbol | Behavior |
|-------|--------|----------|
| RED | 🔴 | MUST HALT, wait for approval |
| ORANGE | 🟠 | SHOULD HALT |
| YELLOW | 🟡 | MAY proceed |

---

## 문제 해결

### CLI 도구를 찾을 수 없음

```bash
# Claude Code 설치 확인
which claude

# 설치되지 않은 경우
npm install -g @anthropic-ai/claude-code
```

### 타임아웃 오류

```bash
# 타임아웃 증가 (10분)
python3 qa/runners/cli_test_runner.py --scenario QUAL-002 --timeout 600
```

---

## Raw Transcript Requirements (v3.2.3)

**모든 QA 테스트는 실제 raw transcript 파일을 생성해야 합니다.** 시뮬레이션 데이터는 허용되지 않습니다.

### 필수 파일 형식

#### Claude Code Raw Transcript (`claude_code_turn{N}_raw.txt`)

```
=== SESSION METADATA ===
CLI: Claude Code
Model: claude-opus-4-5-20251101
Working Directory: /path/to/project
Timestamp: 2026-01-30T21:15:00+09:00
Test ID: QUANT-007

=== USER INPUT ===
[실제 테스트 프롬프트]

=== TOOL CALL ===
Tool: Task
Parameters:
  subagent_type: "diverga:i0"
  model: "opus"
  prompt: "[프롬프트 내용]"

=== TOOL RESULT ===
Agent ID: a1e8ab0
[실제 에이전트 응답 - 시뮬레이션 아님]

=== VERIFICATION CHECKLIST ===
[✓] 체크포인트 표시됨
[✓] VS T-Score 옵션 제시됨
...
```

#### Codex CLI Raw Transcript (`codex_turn{N}_raw.txt`)

```
OpenAI Codex v0.92.0 (research preview)
--------
workdir: /path/to/project
model: gpt-5.2-codex
provider: openai
session id: [자동 생성]
--------
user
[테스트 프롬프트]

mcp: [MCP 연결 상태]

exec
[실행된 명령]

thinking
[Codex 내부 추론]

codex
[최종 응답]

tokens used
[토큰 수]
```

### CLI 호출 방법

| CLI | 호출 명령 | 세션 지속 |
|-----|----------|----------|
| **Claude Code** | `Task(subagent_type="diverga:xxx", ...)` | Agent ID로 resume |
| **Codex CLI** | `codex exec "message"` | `--resume` |
| **OpenCode** | `opencode run "message"` | - |

### Codex CLI 호출 예시 (Claude Code 내에서)

```bash
# Bash tool을 사용하여 Codex CLI 호출
cd /project/path && codex exec "테스트 프롬프트" 2>&1
```

**중요**: Claude Code 내에서 Codex CLI를 호출할 때는 반드시 `2>&1`로 stderr를 포함해야 합니다.

### Cross-CLI 테스트 의무

모든 QUANT 시나리오는 **최소 2개 CLI**에서 테스트해야 합니다:

| 시나리오 | Claude Code | Codex CLI | 필수 |
|---------|-------------|-----------|------|
| QUANT-007 | ✅ Required | ✅ Required | 둘 다 |
| QUANT-006 | ✅ Required | ✅ Required | 둘 다 |
| QUANT-005 | ✅ Required | ✅ Required | 둘 다 |

### Raw Transcript 검증 규칙

1. **시뮬레이션 금지**: 응답이 실제 AI에서 생성되어야 함
2. **메타데이터 필수**: Session ID, Timestamp, Model 포함
3. **Tool Call 기록**: 실제 호출된 도구/파라미터 기록
4. **Verification Checklist**: 각 turn에서 검증된 항목 명시
5. **Token Usage**: 토큰 사용량 기록 (가능한 경우)

---

## Changelog

### v3.0 (2026-01-29)
- **True automated testing via CLI** - 실제 AI 응답 캡처
- **CLITestRunner 클래스** - subprocess 기반 CLI 실행
- **Multi-turn 세션 지원** - `--continue` 플래그로 대화 지속
- **Dry run 모드** - API 호출 없이 테스트 구조 확인
- **run_all_scenarios.sh** - 배치 테스트 스크립트

### v2.2 (2026-01-29)
- **Automated test simulation** - `RESPONSE_TEMPLATES` 기반 시뮬레이션
- **CLI-based execution** - `python3 qa/runners/automated_test.py`

### v2.1 (2026-01-29)
- **Session-based folder management** - `reports/sessions/{SCENARIO-ID}/`
- **RAW conversation extraction** - `conversation_raw.json`

### v2.0 (2026-01-29)
- Migrated to real Claude Code conversations
- Added complex user input types
- Implemented JSONL session log extraction
