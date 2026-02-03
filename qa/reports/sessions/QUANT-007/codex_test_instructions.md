# QUANT-007: Codex CLI 테스트 가이드

## 테스트 목적

Category I 에이전트와 C5 메타분석 에이전트가 Codex CLI에서 정상 작동하는지 검증합니다.

## 테스트 실행 방법

### 1. Codex CLI 시작

```bash
cd /Volumes/External\ SSD/Projects/Diverga
codex
```

### 2. 테스트 프롬프트 입력

다음 프롬프트를 복사하여 Codex CLI에 붙여넣기:

```
AI 학습 도우미(chatbots/tutors)가 외국어 말하기 능력에 미치는 효과에 대한
체계적 문헌고찰과 메타분석을 수행하려고 합니다.

PRISMA 2020 가이드라인에 따라 진행해 주세요.

현재 가지고 있는 정보:
- 연구 주제: AI chatbots for speaking skills in language learning
- 예상 논문 수: 약 50-100편
- 효과크기: Cohen's d, Hedges' g, 상관계수 r 혼재
- 데이터베이스: Semantic Scholar, OpenAlex, arXiv 사용 예정
```

### 3. Raw Output 캡처

Codex CLI 출력을 파일로 저장:

```bash
# 방법 1: 터미널 출력 복사
# 방법 2: script 명령 사용
script codex_session.txt
codex
# (테스트 프롬프트 입력)
exit
```

### 4. 예상 결과

Codex CLI가 정상 작동하면 다음을 확인해야 합니다:

1. **Skill 활성화**: `Using skill: research-coordinator` 또는 `meta-analysis`
2. **Category I 에이전트 참조**: I0, I1, I2, I3 언급
3. **체크포인트 표시**: SCH_DATABASE_SELECTION 또는 CP_EFFECT_SIZE_SELECTION
4. **VS T-Score**: T=0.70, T=0.45, T=0.25 등의 옵션
5. **한국어 프롬프트**: "어떤 방향으로 진행하시겠습니까?"

## 결과 파일 생성

테스트 후 다음 파일을 생성해 주세요:

### codex_turn1_raw.txt 형식

```
OpenAI Codex v0.92.0 (research preview)
--------
workdir: /Volumes/External SSD/Projects/Diverga
model: gpt-5.2-codex
provider: openai
session id: [자동 생성]
--------
user

[테스트 프롬프트]

mcp: context7 starting
mcp: render starting
...

thinking
[Codex 내부 추론 과정]

exec
[실행된 명령]

codex
[최종 응답]

tokens used
[토큰 수]
```

## 비교 기준

| 항목 | Claude Code | Codex CLI |
|------|-------------|-----------|
| I0 에이전트 인식 | ✅ diverga:i0 | ✅/❌ |
| 체크포인트 표시 | ✅ SCH_DATABASE_SELECTION | ✅/❌ |
| VS T-Score | ✅ 0.70, 0.45, 0.25 | ✅/❌ |
| 한국어 지원 | ✅ | ✅/❌ |
| 행동 정지 | ✅ "승인 후..." | ✅/❌ |

## 문제 발생 시

1. **Skill 미인식**: `.codex/skills/` 디렉토리 확인
2. **에이전트 미발견**: `agents/` 디렉토리 확인
3. **MCP 연결 실패**: `mcp startup` 메시지 확인

## 저장 위치

테스트 결과를 다음 위치에 저장:
```
/Volumes/External SSD/Projects/Diverga/qa/reports/sessions/QUANT-007/
├── codex_turn1_raw.txt
├── codex_turn2_raw.txt (있는 경우)
└── codex_session_notes.txt (관찰 사항)
```
