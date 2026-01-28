# Diverga Docs - Roadmap

## Current Status: v1.0 Released 🎉

배포 URL: https://diverga-docs.vercel.app

---

## ✅ Completed (v1.0)

### Phase 1: Foundation
- [x] Next.js 16.1 프로젝트 생성 (TypeScript, App Router)
- [x] Tailwind CSS v4 + OKLCH 컬러 시스템 설정
- [x] next-intl i18n 구성 (영어/한국어)
- [x] 기본 레이아웃 컴포넌트 (Header, Footer, LanguageToggle)

### Phase 2: Core Pages
- [x] Homepage (Hero, Problem/Solution, AgentCategoryGrid, CTA)
- [x] 40개 에이전트 데이터 구조 및 입력 완료
- [x] Agents Catalog (Fuse.js 검색, 카테고리/패러다임/티어 필터)
- [x] Agent Detail 페이지 (80개 = 40 에이전트 × 2 언어)

### Phase 3: Getting Started
- [x] 단계별 설치 가이드
- [x] 플랫폼별 탭 UI (macOS, Windows, Linux)
- [x] 복사 버튼 기능

### Phase 4: Additional Pages
- [x] Workflows 개요 페이지 (4개 연구 패러다임)
- [x] Docs 인덱스 페이지
- [x] Playground (Static Demo - 3개 예시)

### Phase 5: Deploy
- [x] 한국어 번역 완성
- [x] Vercel 배포 (US East region)
- [x] GitHub 저장소: https://github.com/HosungYou/diverga-docs

---

## ✅ Completed (v1.1)

### P1 Features
- [x] VS 방법론 상세 설명 페이지 (`/docs/vs-methodology`)
  - T-Score 시각화
  - Mode Collapse 예시
  - VS 5단계 프로세스 설명

- [x] 문서 검색 API (`/api/search`)
  - Fuse.js 기반 전체 검색
  - 에이전트 + 문서 + 워크플로우 통합 검색
  - SearchBar 컴포넌트 (키보드 내비게이션, 자동완성)

- [x] 다크 모드
  - next-themes 기반 테마 관리
  - 시스템 설정 감지 + 수동 토글
  - CSS 변수 기반 테마

---

## 📋 Planned (v1.2+)

### P1 Features
- [ ] Category 페이지 (`/agents/category/[slug]`)
- [ ] How It Works 페이지 (`/how-it-works`)
- [ ] Workflow 상세 페이지 내용 채우기
- [ ] MDX 기반 문서 시스템

### P2 Features
- [ ] 블로그/튜토리얼 섹션
- [ ] 뉴스레터 구독
- [ ] SEO 최적화
  - [ ] OG 이미지 자동 생성
  - [ ] sitemap.xml
  - [ ] JSON-LD 구조화 데이터

### Technical Debt
- [ ] 에이전트별 실제 예시 입력/출력 추가
- [ ] 성능 최적화 (이미지, 폰트 로딩)
- [ ] E2E 테스트 (Playwright)

---

## 🎯 Success Metrics (Target)

| 지표 | 목표 | 현재 |
|------|------|------|
| 설치 완료율 | 80% | TBD |
| Getting Started 체류 시간 | 8분+ | TBD |
| 한국어 사용자 비율 | 40%+ | TBD |
| Playground 사용률 | 30%+ | TBD |

---

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.1.0 | 2025-01-27 | VS Methodology page, Search API, Dark mode |
| v1.0.0 | 2025-01-27 | Initial release - 40 agents, bilingual, Vercel deployment |

---

## 🤝 Contributing

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for contribution guidelines.

## 📄 Documentation

- [PRD](docs/PRD.md) - Product Requirements
- [SPEC](docs/SPEC.md) - Technical Specification
- [DESIGN](docs/DESIGN.md) - Design System
