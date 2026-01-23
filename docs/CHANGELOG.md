# Changelog

All notable changes to Research Coordinator will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.1.0] - 2025-01-23

### Changed
- **Single plugin, all skills**: `research-coordinator` 플러그인 하나에 21개 스킬 모두 포함
- 설치 방법 대폭 간소화 (2줄로 완료)
- marketplace.json 구조 변경 (Anthropic document-skills 패턴 적용)

### Technical Details
```json
// Before: 21개 개별 플러그인
"plugins": [
  { "name": "research-coordinator", "skills": ["./"] },
  { "name": "01-research-question-refiner", "skills": ["./"] },
  ...
]

// After: 1개 플러그인에 21개 스킬 포함
"plugins": [
  {
    "name": "research-coordinator",
    "source": "./",
    "skills": [
      "./.claude/skills/research-coordinator",
      "./.claude/skills/research-agents/01-research-question-refiner",
      ... (19개 더)
    ]
  }
]
```

### Installation (v2.1.0+)
```bash
claude plugin marketplace add HosungYou/research-coordinator
claude plugin install research-coordinator  # 21개 스킬 모두 설치됨
```

---

## [2.0.1] - 2025-01-23

### Fixed
- marketplace.json 스키마 오류 수정
- Claude Code marketplace 호환성 확보

### Added
- `$schema` 참조 추가
- 각 플러그인에 `source` 필드 추가 (필수)
- 각 플러그인에 `strict: false` 추가
- 일괄 설치 스크립트 (`scripts/install-all-plugins.sh`)

### Technical Details
- 이전: `skills` 배열만 사용 → 스키마 오류
- 이후: `source` + `skills: ["./"]` 구조로 변경

---

## [2.0.0] - 2025-01-22

### Added
- **Verbalized Sampling (VS) 방법론** 통합
  - arXiv:2510.01171 기반 Mode Collapse 방지
  - T-Score (Typicality Score) 시스템
- VS 적용 수준 3단계
  - **Full VS**: 에이전트 02, 03, 05, 10, 16 (5단계 전체 프로세스)
  - **Enhanced VS**: 에이전트 01, 04, 06, 07, 08, 09 (3단계 간소화)
  - **Light VS**: 에이전트 11-15, 17-20 (모달 인식 + 대안 제시)

### Changed
- 모든 에이전트 SKILL.md에 VS 방법론 섹션 추가
- 추천 시 T-Score 범위 명시
- 모달(가장 흔한) 선택 회피 로직 내장

### Agents with Full VS
| ID | Agent | VS Feature |
|----|-------|------------|
| 02 | Theoretical Framework Architect | 이론 추천 시 TAM/UTAUT 등 모달 회피 |
| 03 | Devil's Advocate | 비판 관점 다양화 |
| 05 | Systematic Literature Scout | 검색 전략 차별화 |
| 10 | Statistical Analysis Guide | 분석 방법 대안 제시 |
| 16 | Bias Detector | 편향 유형 포괄적 탐지 |

---

## [1.0.0] - 2025-01-22

### Added
- 초기 릴리스
- 20개 전문 연구 에이전트
- 마스터 코디네이터 (자동 디스패치)
- 5개 카테고리 구성
  - A: 이론 및 연구 설계 (01-04)
  - B: 문헌 및 증거 (05-08)
  - C: 방법론 및 분석 (09-12)
  - D: 품질 및 검증 (13-16)
  - E: 출판 및 커뮤니케이션 (17-20)

### Features
- 맥락 인식 자동 에이전트 활성화
- 트리거 키워드 시스템
- 한국어/영어 이중 언어 지원
- Claude Code Skills 시스템 통합

---

## Version History Summary

| Version | Date | Key Changes |
|---------|------|-------------|
| 2.1.0 | 2025-01-23 | Single plugin with all 21 skills |
| 2.0.1 | 2025-01-23 | Marketplace schema fix |
| 2.0.0 | 2025-01-22 | VS methodology integration |
| 1.0.0 | 2025-01-22 | Initial release |

---

## Upgrading

### From 2.0.x to 2.1.0

```bash
# 기존 개별 플러그인 제거 (있는 경우)
claude plugin uninstall research-coordinator
claude plugin uninstall 01-research-question-refiner
# ... (기타 개별 플러그인)

# 마켓플레이스 업데이트
claude plugin marketplace update research-coordinator-skills

# 새 통합 플러그인 설치
claude plugin install research-coordinator
```

### From 1.x to 2.x

```bash
# 로컬 설치 사용자
cd /path/to/research-coordinator
git pull origin main

# 마켓플레이스 사용자
claude plugin marketplace update research-coordinator-skills
claude plugin update research-coordinator
```
