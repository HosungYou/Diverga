# Diverga 크로스 플랫폼 사용성 강화 계획

**작성일**: 2026-01-28
**버전**: v6.6.1
**상태**: P0-P2 완료, P3 대기

---

## 📊 현황 분석

### 플랫폼별 상태

| 플랫폼 | 위치 | 형식 | 상태 | 문제점 |
|--------|------|------|------|--------|
| **Codex CLI** | `.codex/` | JavaScript (CommonJS) | ❌ 실패 | ESM/CJS 충돌 |
| **OpenCode** | `.opencode/plugins/diverga/` | TypeScript | ⚠️ 미완료 | 컴파일 필요, 타입 정의 누락 |
| **Claude Code** | `.claude/skills/` | Markdown + YAML | ✅ 작동 | 기준 플랫폼 |

### 발견된 문제점

```
┌─────────────────────────────────────────────────────────────────┐
│                     CRITICAL ISSUES                             │
├─────────────────────────────────────────────────────────────────┤
│ 1. Codex: package.json "type": "module" ↔ require() 충돌       │
│ 2. OpenCode: TypeScript 미컴파일 → 런타임 오류 예상             │
│ 3. OpenCode: types.ts에서 Plugin, PluginContext 미정의          │
│ 4. 플랫폼별 설치 가이드 부재                                    │
│ 5. 자동화된 빌드/배포 파이프라인 없음                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Phase 1: 즉시 수정 (P0)

### 1.1 Codex CLI 수정

**문제**: `package.json`에 `"type": "module"` 설정으로 인해 `.js` 파일이 ESM으로 처리되지만, `diverga-codex.js`는 CommonJS `require()` 문법 사용

**해결**: 파일 확장자를 `.cjs`로 변경하여 CommonJS 강제 적용

```bash
# 변경 전
.codex/diverga-codex.js

# 변경 후
.codex/diverga-codex.cjs
```

### 1.2 OpenCode 타입 정의 완성

**문제**: `types.ts`에서 `Plugin`, `PluginContext`, `HookResult` 인터페이스가 정의되지 않음

**해결**: 완전한 타입 정의 추가

### 1.3 OpenCode 빌드 설정

**문제**: TypeScript 컴파일 설정 없음

**해결**: `tsconfig.json` 및 `package.json` 추가

---

## 🔧 Phase 2: 통합 빌드 시스템 (P1)

### 2.1 Monorepo 구조 재편

```
Diverga/
├── packages/
│   ├── core/                    # 공유 로직
│   │   ├── agents.ts            # 에이전트 정의
│   │   ├── checkpoints.ts       # 체크포인트 정의
│   │   └── tscore.ts            # T-Score 로직
│   │
│   ├── codex/                   # Codex CLI 플러그인
│   │   ├── diverga-codex.cjs    # CommonJS 진입점
│   │   └── package.json
│   │
│   ├── opencode/                # OpenCode 플러그인
│   │   ├── index.ts
│   │   ├── hooks/
│   │   └── package.json
│   │
│   └── claude-code/             # Claude Code 스킬
│       └── skills/
│
├── scripts/
│   ├── build-all.sh             # 전체 빌드
│   ├── install-codex.sh         # Codex 설치
│   └── install-opencode.sh      # OpenCode 설치
│
└── package.json                  # Workspace root
```

### 2.2 통합 설치 스크립트

```bash
#!/bin/bash
# Diverga Universal Installer

detect_platform() {
  if command -v codex &> /dev/null; then echo "codex"; fi
  if command -v opencode &> /dev/null; then echo "opencode"; fi
  if command -v claude &> /dev/null; then echo "claude-code"; fi
}

install_codex() {
  echo "📦 Installing Diverga for Codex CLI..."
  mkdir -p ~/.codex/diverga
  cp -r packages/codex/* ~/.codex/diverga/
  echo "✅ Codex installation complete"
}

install_opencode() {
  echo "📦 Installing Diverga for OpenCode..."
  cd packages/opencode && npm run build
  mkdir -p ~/.opencode/plugins/diverga
  cp -r dist/* ~/.opencode/plugins/diverga/
  echo "✅ OpenCode installation complete"
}

install_claude_code() {
  echo "📦 Installing Diverga for Claude Code..."
  echo "Run: /plugin marketplace add https://github.com/HosungYou/Diverga"
}

# Main
for platform in $(detect_platform); do
  install_$platform
done
```

---

## 📚 Phase 3: 문서화 강화 (P2)

### 3.1 플랫폼별 퀵스타트 가이드

#### Codex CLI

```bash
# 1. Clone & Install
git clone https://github.com/HosungYou/Diverga.git ~/.codex/diverga

# 2. Run setup
node ~/.codex/diverga/.codex/diverga-codex.cjs setup

# 3. Verify
codex "diverga:list"
```

#### OpenCode

```bash
# 1. Clone
git clone https://github.com/HosungYou/Diverga.git /tmp/diverga

# 2. Build & Install
cd /tmp/diverga/.opencode/plugins/diverga
npm install && npm run build
cp -r dist ~/.opencode/plugins/diverga

# 3. Verify
opencode "diverga:list"
```

#### Claude Code

```bash
# 1. Add to marketplace
/plugin marketplace add https://github.com/HosungYou/Diverga

# 2. Install
/plugin install diverga

# 3. Setup
/diverga:setup
```

### 3.2 트러블슈팅 가이드

| 오류 | 플랫폼 | 원인 | 해결책 |
|------|--------|------|--------|
| `require is not defined` | Codex | ESM/CJS 충돌 | `.cjs` 확장자 사용 |
| `Cannot find module` | OpenCode | 미컴파일 | `npm run build` 실행 |
| `Plugin not found` | Claude Code | 경로 오류 | `/plugin list`로 확인 |

---

## 🧪 Phase 4: 테스트 자동화 (P3)

### 4.1 크로스 플랫폼 테스트 매트릭스

```yaml
# .github/workflows/test-plugins.yml
name: Plugin Tests

on: [push, pull_request]

jobs:
  test-codex:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Test Codex Plugin
        run: |
          node --version
          node .codex/diverga-codex.cjs help
          node .codex/diverga-codex.cjs list

  test-opencode:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build OpenCode Plugin
        run: |
          cd .opencode/plugins/diverga
          npm install
          npm run build
      - name: Verify Build
        run: ls -la .opencode/plugins/diverga/dist/
```

### 4.2 통합 테스트

```typescript
// tests/integration/agent-trigger.test.ts
describe('Agent Auto-Trigger', () => {
  const testCases = [
    { input: 'meta-analysis', expected: 'c5' },
    { input: '메타분석', expected: 'c5' },
    { input: 'research question', expected: 'a1' },
    { input: 'phenomenology', expected: 'c2' },
  ];

  testCases.forEach(({ input, expected }) => {
    it(`should trigger ${expected} for "${input}"`, () => {
      const result = autoTrigger(input);
      expect(result?.id.toLowerCase()).toBe(expected);
    });
  });
});
```

---

## 🚀 Phase 5: UX 개선 (지속적)

### 5.1 원클릭 설치

**목표**: 모든 플랫폼에서 한 줄 명령어로 설치

```bash
# Codex
curl -sSL https://diverga.dev/install.sh | bash -s codex

# OpenCode
curl -sSL https://diverga.dev/install.sh | bash -s opencode

# Claude Code
/plugin install diverga  # 이미 지원됨
```

### 5.2 자동 플랫폼 감지

```javascript
// 실행 환경 자동 감지
function detectRuntime() {
  if (process.env.CODEX_CLI) return 'codex';
  if (process.env.OPENCODE_PLUGINS) return 'opencode';
  if (process.env.CLAUDE_CODE) return 'claude-code';
  return 'standalone';
}
```

### 5.3 통합 상태 대시보드

```
╔═══════════════════════════════════════════════════════════════╗
║                 Diverga v6.0 - Status Dashboard               ║
╠═══════════════════════════════════════════════════════════════╣
║ Platform:        Codex CLI                                    ║
║ Node Version:    v25.2.1                                      ║
║ Plugin Status:   ✅ Loaded                                    ║
║ Agents:          40/40 available                              ║
║ Last Updated:    2026-01-28                                   ║
╠═══════════════════════════════════════════════════════════════╣
║ Recent Activity:                                              ║
║   • C5-MetaAnalysisMaster invoked (2 min ago)                ║
║   • Checkpoint CP_METHODOLOGY_APPROVAL pending               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## 📋 실행 우선순위

| 우선순위 | 작업 | 영향도 | 난이도 | 예상 시간 | 상태 |
|:--------:|------|:------:|:------:|:---------:|:----:|
| **P0** | Codex ESM 수정 | 🔴 Critical | 🟢 Easy | 10분 | ✅ 완료 |
| **P0** | OpenCode types.ts 완성 | 🔴 Critical | 🟢 Easy | 30분 | ✅ 완료 |
| **P1** | OpenCode tsconfig 추가 | 🟠 High | 🟢 Easy | 15분 | ✅ 완료 |
| **P1** | 통합 설치 스크립트 | 🟠 High | 🟡 Medium | 2시간 | ✅ 완료 |
| **P2** | 문서화 (QUICKSTART, TROUBLESHOOTING) | 🟡 Medium | 🟡 Medium | 4시간 | ✅ 완료 |
| **P3** | CI/CD 테스트 | 🟢 Low | 🟠 Hard | 1일 | ⏳ 대기 |

---

## 변경 이력

| 날짜 | 버전 | 변경 내용 |
|------|------|----------|
| 2026-01-28 | 1.0 | 초안 작성 |
| 2026-01-28 | 1.1 | P0 완료 - Codex .cjs, OpenCode 빌드 시스템 |
| 2026-01-28 | 1.2 | P1 완료 - 통합 설치 스크립트 (install.sh, install-codex.sh, install-opencode.sh) |
| 2026-01-28 | 1.3 | P2 완료 - QUICKSTART.md, TROUBLESHOOTING.md |
