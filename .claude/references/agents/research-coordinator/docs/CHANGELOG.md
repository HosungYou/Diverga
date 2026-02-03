# Changelog

All notable changes to Research Coordinator are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- Light VS 에이전트 출력 형식 표준화
- 코드 예시 패키지 설치 및 에러 처리 추가
- YAML frontmatter 필드 확장 (icon, category)
- 에이전트 간 양방향 상호 참조

---

## [2.1.0] - 2025-01-23

### Added
- **evaluation-harness.md**: VS 행동 평가 하네스
  - Mode Collapse 탐지 알고리즘
  - 회귀 테스트 케이스 구조
  - 테스트 실행 프레임워크

- **agent-contract-schema.md**: Agent I/O 계약 스키마
  - 표준화된 입력/출력 스키마 정의
  - VS 메타데이터 구조
  - 에이전트 체인 호환성 보장

- **self-critique-framework.md**: Self-Critique 프레임워크
  - Reflexion 패턴 기반 자기 비평 메커니즘
  - 5개 Full VS 에이전트 적용

- **agent-registry.yaml**: 에이전트 중앙 레지스트리
  - 20개 에이전트 메타데이터
  - VS 레벨, 트리거, 의존성 정보

- **context-budgeting.md**: 컨텍스트 예산 관리 전략
  - 에이전트별 토큰 예산 할당
  - 계층적 요약 (4단계)
  - 실시간 예산 모니터링

- **knowledge-graph.md**: 이론/구성개념 지식 그래프
  - 노드 스키마 (Theory, Construct, Scale)
  - T-Score 기반 이론 추천
  - 도메인별 이론 카탈로그

- **meta-agent-governor.md**: Meta-Agent 워크플로우 거버너
  - Workflow Planner
  - Conflict Resolver
  - Quality Gate
  - Resource Manager

### Changed
- **02-theoretical-framework-architect/SKILL.md**: Self-Critique 섹션 추가
- **03-devils-advocate/SKILL.md**: Self-Critique 섹션 추가
- **05-systematic-literature-scout/SKILL.md**: Self-Critique 섹션 추가
- **10-statistical-analysis-guide/SKILL.md**: Self-Critique 섹션 추가
- **16-bias-detector/SKILL.md**: Self-Critique 섹션 추가
- **research-coordinator/SKILL.md**: 참조 문서 링크 업데이트

### Git Commits
- `2bef67b`: P0-P1 업그레이드 (평가 하네스, Self-Critique, Registry)
- `46741d9`: P2-P3 아키텍처 컴포넌트 추가

---

## [2.0.0] - 2025-01-22

### Added
- **VS 방법론 완전 통합**: arXiv:2510.01171 기반
  - Full VS: 5개 에이전트 (02, 03, 05, 10, 16)
  - Enhanced VS: 6개 에이전트 (01, 04, 06, 07, 08, 09)
  - Light VS: 9개 에이전트 (11-20)

- **VS-Research-Framework.md**: VS 방법론 참조 문서
  - T-Score 계산 방법
  - 4단계 VS 프로세스
  - Mode Collapse 개념 설명

- **GitHub Repository**: https://github.com/HosungYou/research-coordinator

### Changed
- 20개 에이전트 SKILL.md 전체 업데이트
  - VS 섹션 추가
  - 옵션 열거 템플릿
  - T-Score 평가 테이블

---

## [1.5.0] - 2025-01-22

### Added
- VS 방법론 통합 시작
- Full/Enhanced/Light 레벨 분류 설계

### Changed
- 마스터 코디네이터 SKILL.md 구조 개선
- 에이전트 카테고리 명확화

---

## [1.0.0] - 2025-01-22

### Added
- **초기 프로젝트 구조**
  - 20개 에이전트 디렉토리
  - 마스터 코디네이터

- **5개 카테고리 분류**
  - A: 이론 및 연구 설계 (01-04)
  - B: 문헌 및 증거 (05-08)
  - C: 방법론 및 분석 (09-12)
  - D: 품질 및 검증 (13-16)
  - E: 출판 및 커뮤니케이션 (17-20)

- **개별 에이전트 SKILL.md**
  - 01-research-question-refiner
  - 02-theoretical-framework-architect
  - 03-devils-advocate
  - 04-research-ethics-advisor
  - 05-systematic-literature-scout
  - 06-evidence-quality-assessor
  - 07-effect-size-extractor
  - 08-research-trend-radar
  - 09-research-design-consultant
  - 10-statistical-analysis-guide
  - 11-analysis-code-generator
  - 12-sensitivity-analysis-designer
  - 13-internal-consistency-checker
  - 14-checklist-manager
  - 15-reproducibility-auditor
  - 16-bias-detector
  - 17-journal-matcher
  - 18-academic-communicator
  - 19-peer-review-strategist
  - 20-preregistration-composer

- **마스터 코디네이터**
  - 자동 에이전트 트리거 시스템
  - 병렬 실행 그룹 정의
  - 순차 실행 규칙

---

## Version Comparison

| 버전 | 에이전트 수 | VS 적용 | 참조 문서 | 자동화 수준 |
|------|-----------|--------|----------|------------|
| 1.0.0 | 20 | ❌ | 0 | 기본 |
| 1.5.0 | 20 | 부분 | 1 | 기본 |
| 2.0.0 | 20 | ✅ 전체 | 2 | 중간 |
| 2.1.0 | 20 | ✅ 전체 | 9 | 고급 |

---

## Migration Guide

### From 1.x to 2.0

1. 에이전트 SKILL.md에 VS 섹션 추가됨
2. 출력 형식에 T-Score 정보 포함
3. 마스터 코디네이터 트리거 규칙 확장

### From 2.0 to 2.1

1. Full VS 에이전트에 Self-Critique 섹션 추가됨
2. 새로운 참조 문서 7개 추가
3. agent-registry.yaml로 프로그래매틱 접근 가능

---

*Maintained by Hosung You*
