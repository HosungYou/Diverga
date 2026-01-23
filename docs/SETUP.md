# Research Coordinator 설치 가이드

## 목차

1. [시스템 요구사항](#시스템-요구사항)
2. [마켓플레이스 설치 (권장)](#마켓플레이스-설치-권장)
3. [로컬 설치 (개발용)](#로컬-설치-개발용)
4. [설치 확인](#설치-확인)
5. [업데이트](#업데이트)
6. [제거](#제거)
7. [문제 해결](#문제-해결)

---

## 시스템 요구사항

### 필수 요구사항

- **Claude Code CLI**: v1.0 이상 ([설치 방법](https://claude.ai/code))
- **운영체제**: macOS, Linux, Windows (WSL)

### 확인 방법

```bash
# Claude Code 버전 확인
claude --version
```

---

## 마켓플레이스 설치 (권장)

> **v2.1.0 신규**: 단일 플러그인 설치로 21개 스킬 모두 사용 가능!

### 설치 (단 2줄)

```bash
# Step 1: 마켓플레이스 추가 (최초 1회)
claude plugin marketplace add HosungYou/research-coordinator

# Step 2: 플러그인 설치 (21개 스킬 모두 포함)
claude plugin install research-coordinator
```

### 설치 스크립트 사용 (대안)

```bash
curl -sL https://raw.githubusercontent.com/HosungYou/research-coordinator/main/scripts/install-all-plugins.sh | bash
```

### 설치 확인

```bash
claude plugin list | grep research-coordinator
```

출력 예시:
```
❯ research-coordinator@research-coordinator-skills
  Version: 50d43876e8c5
  Scope: user
  Status: ✔ enabled
```

### 포함된 스킬 (21개)

| 카테고리 | 스킬 명령어 |
|----------|------------|
| **마스터** | `/research-coordinator` |
| **A: 연구 설계** | `/research-question-refiner`, `/theoretical-framework-architect`, `/devils-advocate`, `/research-ethics-advisor` |
| **B: 문헌 검토** | `/systematic-literature-scout`, `/evidence-quality-appraiser`, `/effect-size-extractor`, `/research-radar` |
| **C: 방법론** | `/research-design-consultant`, `/statistical-analysis-guide`, `/analysis-code-generator`, `/sensitivity-analysis-designer` |
| **D: 품질 검증** | `/internal-consistency-checker`, `/checklist-manager`, `/reproducibility-auditor`, `/bias-detector` |
| **E: 출판** | `/journal-matcher`, `/academic-communicator`, `/peer-review-strategist`, `/preregistration-composer` |

---

## 로컬 설치 (개발용)

마켓플레이스가 아닌 로컬 개발 환경에서 사용하려는 경우:

### 자동 설치

```bash
git clone https://github.com/HosungYou/research-coordinator.git
cd research-coordinator
./scripts/install.sh
```

### 수동 설치

```bash
git clone https://github.com/HosungYou/research-coordinator.git
cd research-coordinator

# 스킬 디렉토리 생성
mkdir -p ~/.claude/skills

# 심볼릭 링크 생성
ln -sf "$(pwd)/.claude/skills/research-coordinator" ~/.claude/skills/
ln -sf "$(pwd)/.claude/skills/research-agents" ~/.claude/skills/
```

---

## 설치 확인

### Claude Code에서 테스트

```
/research-coordinator
```

마스터 코디네이터가 활성화되면 성공입니다.

### 개별 스킬 테스트

```
/statistical-analysis-guide
```

```
/systematic-literature-scout
```

---

## 업데이트

### 마켓플레이스 설치 업데이트

```bash
# 마켓플레이스 캐시 업데이트
claude plugin marketplace update research-coordinator-skills

# 플러그인 업데이트
claude plugin update research-coordinator
```

### 로컬 설치 업데이트

```bash
cd /path/to/research-coordinator
git pull origin main
```

---

## 제거

### 마켓플레이스 플러그인 제거

```bash
# 플러그인 제거
claude plugin uninstall research-coordinator

# (선택) 마켓플레이스 제거
claude plugin marketplace remove research-coordinator-skills
```

### 로컬 설치 제거

```bash
# 심볼릭 링크 제거
rm ~/.claude/skills/research-coordinator
rm -rf ~/.claude/skills/research-agents

# (선택) 레포지토리 삭제
rm -rf /path/to/research-coordinator
```

---

## 문제 해결

### 문제: 마켓플레이스 추가 실패

**증상**: `Plugin not found in any configured marketplace`

**해결 방법**:
```bash
# 마켓플레이스 목록 확인
claude plugin marketplace list

# 마켓플레이스 다시 추가
claude plugin marketplace remove research-coordinator-skills 2>/dev/null
claude plugin marketplace add HosungYou/research-coordinator
```

### 문제: 스킬 명령어 인식 안됨

**증상**: `/research-coordinator` 등 명령어 미작동

**해결 방법**:
1. 플러그인 설치 상태 확인:
```bash
claude plugin list | grep research-coordinator
```

2. 플러그인 재설치:
```bash
claude plugin uninstall research-coordinator
claude plugin install research-coordinator
```

3. Claude Code 재시작

### 문제: 업데이트 후 작동 안함

**해결 방법**:
```bash
# 캐시 업데이트
claude plugin marketplace update research-coordinator-skills

# 플러그인 재설치
claude plugin uninstall research-coordinator
claude plugin install research-coordinator
```

### 추가 도움

- [GitHub Issues](https://github.com/HosungYou/research-coordinator/issues)
- [CHANGELOG.md](./CHANGELOG.md) - 버전별 변경사항
- [USAGE-EXAMPLES.md](./USAGE-EXAMPLES.md) - 사용 예시
