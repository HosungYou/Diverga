# Research Coordinator 설치 가이드

## 목차

1. [시스템 요구사항](#시스템-요구사항)
2. [설치 방법](#설치-방법)
3. [설치 확인](#설치-확인)
4. [설정](#설정)
5. [업데이트](#업데이트)
6. [제거](#제거)
7. [문제 해결](#문제-해결)

---

## 시스템 요구사항

### 필수 요구사항

- **Claude Code**: v1.0 이상
- **Git**: 레포지토리 클론용
- **운영체제**: macOS, Linux, Windows (WSL)

### 권장 환경

- Claude Code가 Skills 시스템을 지원하는 최신 버전
- `~/.claude/skills/` 디렉토리 접근 권한

---

## 설치 방법

### 방법 1: 자동 설치 (권장)

```bash
# 1. 레포지토리 클론
git clone https://github.com/HosungYou/research-coordinator.git

# 2. 프로젝트 디렉토리로 이동
cd research-coordinator

# 3. 설치 스크립트 실행
chmod +x scripts/install.sh
./scripts/install.sh
```

설치 스크립트가 자동으로:
- `~/.claude/skills/` 디렉토리 생성 (없는 경우)
- 마스터 스킬 심볼릭 링크 생성
- 개별 에이전트 스킬 심볼릭 링크 생성

### 방법 2: 수동 설치

```bash
# 1. 레포지토리 클론
git clone https://github.com/HosungYou/research-coordinator.git
cd research-coordinator

# 2. 스킬 디렉토리 생성
mkdir -p ~/.claude/skills

# 3. 심볼릭 링크 생성
ln -sf "$(pwd)/.claude/skills/research-coordinator" ~/.claude/skills/research-coordinator
ln -sf "$(pwd)/.claude/skills/research-agents" ~/.claude/skills/research-agents
```

### 방법 3: 직접 복사 (심볼릭 링크 미지원 환경)

```bash
# 스킬 파일 직접 복사
cp -r .claude/skills/research-coordinator ~/.claude/skills/
cp -r .claude/skills/research-agents ~/.claude/skills/
```

**주의**: 직접 복사의 경우 업데이트 시 수동으로 다시 복사해야 합니다.

---

## 설치 확인

### 디렉토리 구조 확인

```bash
# 마스터 스킬 확인
ls -la ~/.claude/skills/research-coordinator/
# 출력: SKILL.md

# 개별 에이전트 확인
ls ~/.claude/skills/research-agents/
# 출력: 01-research-question-refiner/ ~ 20-preregistration-composer/
```

### 스킬 파일 확인

```bash
# 마스터 스킬 내용 확인
head -20 ~/.claude/skills/research-coordinator/SKILL.md

# 개별 에이전트 확인
head -10 ~/.claude/skills/research-agents/01-research-question-refiner/SKILL.md
```

### Claude Code에서 확인

Claude Code를 실행하고 다음 명령어로 테스트:

```
/research-coordinator
```

정상적으로 마스터 코디네이터가 활성화되면 설치 완료입니다.

---

## 설정

### 기본 설정

Research Coordinator는 기본 설정으로 바로 사용 가능합니다.
추가 설정이 필요한 경우 아래를 참조하세요.

### 에이전트 커스터마이징

개별 에이전트의 동작을 수정하려면 해당 SKILL.md 파일을 편집합니다:

```bash
# 예: 연구 질문 정제기 커스터마이징
code ~/.claude/skills/research-agents/01-research-question-refiner/SKILL.md
```

커스터마이징 가능한 항목:
- **description**: 트리거 키워드 수정
- **프롬프트 템플릿**: 에이전트 동작 방식 변경
- **출력 형식**: 결과물 구조 변경

### 새 에이전트 추가

1. 새 디렉토리 생성:
```bash
mkdir -p ~/.claude/skills/research-agents/21-custom-agent
```

2. SKILL.md 파일 작성:
```markdown
---
name: custom-agent
description: |
  커스텀 에이전트 설명
  Use when: [트리거 조건]
  트리거: [키워드1], [키워드2]
---

# 커스텀 에이전트

## 개요
[에이전트 설명]

## 사용 시점
- [상황 1]
- [상황 2]

## 프롬프트 템플릿
[실행 프롬프트]
```

---

## 업데이트

### 심볼릭 링크 설치의 경우

```bash
# 레포지토리 디렉토리로 이동
cd /path/to/research-coordinator

# 최신 버전 가져오기
git pull origin main
```

심볼릭 링크가 자동으로 업데이트된 내용을 반영합니다.

### 직접 복사 설치의 경우

```bash
# 레포지토리 업데이트
cd /path/to/research-coordinator
git pull origin main

# 스킬 재복사
cp -r .claude/skills/research-coordinator ~/.claude/skills/
cp -r .claude/skills/research-agents ~/.claude/skills/
```

---

## 제거

### 자동 제거

```bash
cd /path/to/research-coordinator
chmod +x scripts/uninstall.sh
./scripts/uninstall.sh
```

### 수동 제거

```bash
# 심볼릭 링크 제거
rm ~/.claude/skills/research-coordinator
rm ~/.claude/skills/research-agents

# (선택) 레포지토리 삭제
rm -rf /path/to/research-coordinator
```

---

## 문제 해결

### 문제: 스킬이 인식되지 않음

**증상**: `/research-coordinator` 명령이 작동하지 않음

**해결 방법**:
1. 심볼릭 링크 상태 확인:
```bash
ls -la ~/.claude/skills/
```

2. SKILL.md 파일 존재 확인:
```bash
cat ~/.claude/skills/research-coordinator/SKILL.md | head -20
```

3. Claude Code 재시작

### 문제: 심볼릭 링크 오류

**증상**: "Too many levels of symbolic links" 오류

**해결 방법**:
```bash
# 기존 링크 제거
rm ~/.claude/skills/research-coordinator
rm ~/.claude/skills/research-agents

# 절대 경로로 재생성
ln -sf "/absolute/path/to/research-coordinator/.claude/skills/research-coordinator" ~/.claude/skills/
ln -sf "/absolute/path/to/research-coordinator/.claude/skills/research-agents" ~/.claude/skills/
```

### 문제: 권한 오류

**증상**: "Permission denied" 오류

**해결 방법**:
```bash
# 디렉토리 권한 확인 및 수정
chmod 755 ~/.claude/skills
chmod -R 644 ~/.claude/skills/research-coordinator
chmod -R 644 ~/.claude/skills/research-agents
```

### 문제: Windows에서 심볼릭 링크 실패

**증상**: Windows에서 심볼릭 링크 생성 불가

**해결 방법**:
1. 관리자 권한으로 PowerShell 실행
2. 개발자 모드 활성화: Settings > For developers > Developer Mode 켜기
3. 또는 직접 복사 방식 사용

### 추가 도움

문제가 지속되면:
- [GitHub Issues](https://github.com/HosungYou/research-coordinator/issues)에 문제 보고
- 오류 메시지와 환경 정보 포함
