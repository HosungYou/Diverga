# Diverga v6.6.1 - Cross-Platform Enhancement Release

**릴리스 날짜**: 2026-01-28
**버전**: v6.6.1
**코드네임**: Cross-Platform Enhancement Edition

---

## 📋 릴리스 요약

이 릴리스는 Diverga를 Codex CLI, OpenCode, Claude Code 세 가지 AI 코딩 플랫폼에서 원활하게 사용할 수 있도록 크로스 플랫폼 지원을 대폭 강화했습니다.

### 주요 변경사항

| 영역 | 변경 내용 |
|------|----------|
| **Codex CLI** | ESM/CommonJS 충돌 해결 (.cjs 파일 추가), ASCII 아트 배너 추가 |
| **OpenCode** | TypeScript 빌드 시스템 완성, ASCII 아트 배너 추가 |
| **설치** | 원라인 설치 스크립트 3종 추가 |
| **문서** | QUICKSTART.md, TROUBLESHOOTING.md 신규, diverga-docs 업데이트 |
| **CI/CD** | GitHub Actions 워크플로우 추가 |
| **UX** | ANSI 컬러 출력, 티어별 색상 표시 |

---

## 🔧 기술적 변경사항

### P0: 즉시 수정 (Critical Fixes)

#### 1. Codex CLI ESM/CommonJS 충돌 해결

**문제**: `package.json`에 `"type": "module"` 설정으로 인해 Node.js가 `.js` 파일을 ESM으로 처리하지만, `diverga-codex.js`는 CommonJS `require()` 문법 사용

**해결**: `.cjs` 확장자 파일 추가로 CommonJS 강제 적용

```
변경 전: .codex/diverga-codex.js (ESM 오류 발생)
변경 후: .codex/diverga-codex.cjs (정상 작동)
```

**커밋**: `b0eee65`

#### 2. OpenCode TypeScript 빌드 시스템

**문제**: TypeScript 파일들이 컴파일되지 않아 런타임 오류 발생

**해결**: 
- `tsconfig.json` 추가 (ES2022 타겟, ESNext 모듈)
- `package.json` 추가 (빌드 스크립트 포함)
- `index.ts` 타입 오류 수정

```json
// .opencode/plugins/diverga/tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "outDir": "./dist",
    "strict": true
  }
}
```

**커밋**: `b0eee65`

---

### P1: 통합 설치 시스템

#### 1. 유니버설 인스톨러 (`scripts/install.sh`)

플랫폼 자동 감지 및 설치:

```bash
# 사용법
curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install.sh | bash

# 특정 플랫폼만 설치
./scripts/install.sh codex
./scripts/install.sh opencode
./scripts/install.sh claude-code
./scripts/install.sh all
```

**기능**:
- `~/.codex`, `~/.opencode`, `~/.claude` 디렉토리 감지
- 컬러 출력 및 진행 표시
- 설치 후 자동 검증
- 임시 파일 자동 정리

#### 2. Codex 전용 인스톨러 (`scripts/install-codex.sh`)

```bash
curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-codex.sh | bash
```

#### 3. OpenCode 전용 인스톨러 (`scripts/install-opencode.sh`)

```bash
curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-opencode.sh | bash
```

**특징**: npm이 있으면 TypeScript 자동 빌드, 없으면 소스 파일 복사

**커밋**: `2138224`

---

### P2: 문서화 강화

#### 1. QUICKSTART.md

플랫폼별 빠른 시작 가이드:

| 섹션 | 내용 |
|------|------|
| 원라인 설치 | 모든 플랫폼 curl 명령어 |
| Claude Code | 3단계 설치 가이드 |
| Codex CLI | 수동/자동 설치 + 명령어 |
| OpenCode | 빌드 포함 설치 가이드 |
| 명령어 레퍼런스 | 플랫폼별 명령어 비교표 |

#### 2. TROUBLESHOOTING.md

문제 해결 가이드:

| 섹션 | 내용 |
|------|------|
| Critical Issues | `require is not defined`, `Cannot find module` |
| Platform-Specific | Codex, OpenCode, Claude Code 별 이슈 |
| General Solutions | 재설치, 업데이트, 진단 명령어 |
| Node.js Issues | 버전 요구사항, ESM/CJS 설명 |

**커밋**: `b7349d8`

---

### P3: CI/CD 자동화

#### GitHub Actions 워크플로우

`.github/workflows/test-plugins.yml`:

```yaml
jobs:
  test-codex:        # Node.js 18/20/22 매트릭스
  test-opencode:     # TypeScript 빌드 + 타입체크
  test-install-scripts:  # Bash 문법 검증
  lint-docs:         # 문서 존재 확인
```

**테스트 항목**:

| Job | 테스트 내용 |
|-----|------------|
| test-codex | help, setup, list, agent, tscore, checkpoint 명령어 |
| test-opencode | npm install, typecheck, build, 출력 파일 확인 |
| test-install-scripts | bash -n 문법 검증 |
| lint-docs | QUICKSTART, TROUBLESHOOTING, README, CLAUDE, AGENTS 존재 |

**트리거 조건**:
- `main` 브랜치 push/PR
- `.codex/**`, `.opencode/**`, `scripts/**` 경로 변경 시

**커밋**: `ccfbe17`

---

### P5: UX 개선 (ASCII Art Banner)

#### 1. Codex CLI ASCII Art 배너

```
    ██████╗ ██╗██╗   ██╗███████╗██████╗  ██████╗  █████╗
    ██╔══██╗██║██║   ██║██╔════╝██╔══██╗██╔════╝ ██╔══██╗
    ██║  ██║██║██║   ██║█████╗  ██████╔╝██║  ███╗███████║
    ██║  ██║██║╚██╗ ██╔╝██╔══╝  ██╔══██╗██║   ██║██╔══██║
    ██████╔╝██║ ╚████╔╝ ███████╗██║  ██║╚██████╔╝██║  ██║
    ╚═════╝ ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝

    🎯 Diverge from the Modal · Discover the Exceptional
```

**기능**:
- ANSI 컬러 출력 (Cyan, Yellow, Green, Red)
- 티어별 색상 구분 (HIGH=Red, MEDIUM=Yellow, LOW=Green)
- 모든 명령어에서 배너 표시

**커밋**: `f5b557b`, `9a5dd64`

---

## 📁 변경된 파일 목록

### 신규 파일 (9개)

```
.codex/diverga-codex.cjs                    # Codex CLI (CommonJS)
.opencode/plugins/diverga/tsconfig.json     # TypeScript 설정
.opencode/plugins/diverga/package.json      # 패키지 설정
scripts/install.sh                          # 유니버설 인스톨러
scripts/install-codex.sh                    # Codex 인스톨러
scripts/install-opencode.sh                 # OpenCode 인스톨러
docs/QUICKSTART.md                          # 빠른 시작 가이드
docs/TROUBLESHOOTING.md                     # 문제 해결 가이드
.github/workflows/test-plugins.yml          # CI/CD 워크플로우
```

### 수정된 파일 (4개)

```
.opencode/plugins/diverga/index.ts          # TypeScript 오류 수정
.gitignore                                  # dist/, package-lock.json 추가
README.md                                   # 버전 및 설치 명령어 업데이트
docs/CROSS_PLATFORM_ENHANCEMENT_PLAN.md     # 진행 상태 업데이트
```

---

## 🚀 사용 방법

### 원라인 설치

```bash
# 자동 감지 (권장)
curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install.sh | bash

# Codex CLI
curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-codex.sh | bash

# OpenCode
curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-opencode.sh | bash

# Claude Code
/plugin marketplace add https://github.com/HosungYou/Diverga
/plugin install diverga
```

### Codex CLI 명령어

```bash
node ~/.codex/diverga/diverga-codex.cjs setup      # 설정 확인
node ~/.codex/diverga/diverga-codex.cjs list       # 에이전트 목록
node ~/.codex/diverga/diverga-codex.cjs agent A1   # 에이전트 상세
node ~/.codex/diverga/diverga-codex.cjs tscore     # T-Score 참조
node ~/.codex/diverga/diverga-codex.cjs checkpoint # 체크포인트
node ~/.codex/diverga/diverga-codex.cjs vs         # VS 방법론
```

### OpenCode 명령어

```bash
opencode "diverga:list"
opencode "diverga:agent A1"
opencode "diverga:checkpoint"
```

---

## 📊 커밋 히스토리

| Hash | Phase | 메시지 |
|------|:-----:|--------|
| `b0eee65` | P0 | fix(v6.6.1): Resolve ESM/CommonJS conflict for Codex CLI |
| `2138224` | P1 | feat(v6.6.1): Add unified install scripts for cross-platform support |
| `b7349d8` | P2 | docs(v6.6.1): Add comprehensive platform documentation |
| `ccfbe17` | P3 | ci(v6.6.1): Add GitHub Actions workflow for cross-platform testing |
| `f19586c` | P4 | docs: Add comprehensive v6.6.1 release changelog |
| `f5b557b` | P5 | feat(v6.6.1): Add ASCII art banner and colored output to Codex CLI |
| `9a5dd64` | P5 | feat(v6.6.1): Add ASCII art banner and colored output to OpenCode plugin |

---

## ✅ 테스트 결과

### Codex CLI
```
✅ diverga-codex.cjs setup - AGENTS.md found, Skills directory found
✅ diverga-codex.cjs list - 40 agents displayed
✅ diverga-codex.cjs agent A1 - Agent details shown
```

### OpenCode
```
✅ npm run typecheck - No errors
✅ npm run build - dist/ generated (13 files)
```

### 설치 스크립트
```
✅ install.sh - Syntax valid
✅ install-codex.sh - Syntax valid
✅ install-opencode.sh - Syntax valid
```

---

## 🔗 관련 링크

- **GitHub Repository**: https://github.com/HosungYou/Diverga
- **GitHub Actions**: https://github.com/HosungYou/Diverga/actions
- **Issues**: https://github.com/HosungYou/Diverga/issues

---

## 📝 기여자

- **개발**: Claude Opus 4.5 (Anthropic)
- **프로젝트 소유자**: Hosung You

---

*Diverga v6.6.1 - Where creativity meets rigor*
