# CLAUDE.md

Research Coordinator - 사회과학 연구자를 위한 20개 전문 에이전트 시스템

## 프로젝트 개요

이 프로젝트는 Claude Code Skills 시스템을 활용하여 사회과학 연구의 전체 프로세스를 지원하는 20개 전문 에이전트를 제공합니다.

## 스킬 구조

```
.claude/skills/
├── research-coordinator/        # 마스터 스킬 (코디네이터)
│   └── SKILL.md
└── research-agents/             # 20개 개별 에이전트
    ├── 01-research-question-refiner/
    ├── 02-theoretical-framework-architect/
    ...
    └── 20-preregistration-composer/
```

## 에이전트 카테고리

### Category A: 이론 및 연구 설계 (01-04)
- 연구 질문 정제기
- 이론적 프레임워크 설계자
- 악마의 옹호자
- 연구 윤리 자문관

### Category B: 문헌 및 증거 (05-08)
- 체계적 문헌 탐색자
- 증거 품질 평가자
- 효과크기 추출기
- 최신 연구 레이더

### Category C: 방법론 및 분석 (09-12)
- 연구 설계 컨설턴트
- 통계 분석 가이드
- 분석 코드 생성기
- 민감도 분석 설계자

### Category D: 품질 및 검증 (13-16)
- 내적 일관성 검증자
- 체크리스트 관리자
- 재현성 감사자
- 편향 탐지기

### Category E: 출판 및 커뮤니케이션 (17-20)
- 저널 매칭 전문가
- 학술 커뮤니케이터
- 피어 리뷰 대응 전략가
- 사전등록 문서 작성자

## 사용 방법

### 마스터 스킬 호출
```
/research-coordinator
```
마스터 스킬은 사용자의 맥락을 분석하여 적절한 에이전트를 자동으로 선택합니다.

### 개별 에이전트 직접 호출
```
/research-question-refiner
/theoretical-framework-architect
/statistical-analysis-guide
```

## 자동 트리거 키워드

다음 키워드가 감지되면 해당 에이전트가 자동으로 활성화됩니다:

| 키워드 | 에이전트 |
|--------|----------|
| "연구 질문", "research question" | 01-research-question-refiner |
| "이론적 프레임워크", "conceptual model" | 02-theoretical-framework-architect |
| "문헌 검토", "PRISMA" | 05-systematic-literature-scout |
| "통계 분석", "ANOVA", "회귀" | 10-statistical-analysis-guide |
| "저널", "투고" | 17-journal-matcher |

## 설치

```bash
./scripts/install.sh
```

설치 후 `~/.claude/skills/` 디렉토리에 심볼릭 링크가 생성됩니다.

## GitHub Repository

https://github.com/HosungYou/research-coordinator
