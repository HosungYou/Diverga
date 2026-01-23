# Claude Code Marketplace 등록 가이드

이 문서는 Claude Code 플러그인을 마켓플레이스에 등록하는 방법을 설명합니다.
Research Coordinator 등록 과정에서 얻은 경험을 바탕으로 작성되었습니다.

---

## 목차

1. [디렉토리 구조](#디렉토리-구조)
2. [marketplace.json 스키마](#marketplacejson-스키마)
3. [단일 vs 다중 스킬 플러그인](#단일-vs-다중-스킬-플러그인)
4. [SKILL.md 작성법](#skillmd-작성법)
5. [등록 및 테스트](#등록-및-테스트)
6. [일반적인 오류와 해결책](#일반적인-오류와-해결책)

---

## 디렉토리 구조

### 필수 구조

```
your-plugin/
├── .claude-plugin/
│   └── marketplace.json    # 필수: 마켓플레이스 매니페스트
├── .claude/
│   └── skills/
│       └── your-skill/
│           └── SKILL.md    # 필수: 스킬 정의 파일
├── README.md
└── LICENSE
```

### 다중 스킬 구조 예시

```
research-coordinator/
├── .claude-plugin/
│   └── marketplace.json
├── .claude/
│   └── skills/
│       ├── research-coordinator/     # 마스터 스킬
│       │   └── SKILL.md
│       └── research-agents/          # 개별 에이전트
│           ├── 01-agent/
│           │   └── SKILL.md
│           ├── 02-agent/
│           │   └── SKILL.md
│           └── ...
└── README.md
```

---

## marketplace.json 스키마

### 기본 템플릿

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "your-marketplace-name",
  "owner": {
    "name": "Your Name",
    "github": "YourGitHubUsername"
  },
  "metadata": {
    "description": "Plugin description",
    "version": "1.0.0",
    "keywords": ["keyword1", "keyword2"],
    "repository": "https://github.com/user/repo",
    "license": "MIT"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "description": "Plugin description",
      "source": "./",
      "strict": false,
      "skills": ["./.claude/skills/your-skill"]
    }
  ]
}
```

### 필수 필드

| 필드 | 설명 | 예시 |
|------|------|------|
| `$schema` | 스키마 참조 | `"https://anthropic.com/claude-code/marketplace.schema.json"` |
| `name` | 마켓플레이스 이름 | `"my-awesome-skills"` |
| `plugins[].name` | 플러그인 이름 | `"my-plugin"` |
| `plugins[].source` | 소스 경로 | `"./"` |
| `plugins[].skills` | 스킬 경로 배열 | `["./.claude/skills/my-skill"]` |

### ⚠️ 중요: source 필드

**반드시 `source` 필드를 포함해야 합니다!**

```json
// ❌ 오류: source 필드 누락
{
  "plugins": [{
    "name": "my-plugin",
    "skills": ["./.claude/skills/my-skill"]
  }]
}

// ✅ 정상: source 필드 포함
{
  "plugins": [{
    "name": "my-plugin",
    "source": "./",
    "strict": false,
    "skills": ["./.claude/skills/my-skill"]
  }]
}
```

---

## 단일 vs 다중 스킬 플러그인

### 단일 스킬 플러그인

하나의 플러그인에 하나의 스킬:

```json
{
  "plugins": [
    {
      "name": "code-reviewer",
      "source": "./.claude/skills/code-reviewer",
      "strict": false,
      "skills": ["./"]
    }
  ]
}
```

### 다중 스킬 플러그인 (권장)

하나의 플러그인에 여러 스킬 포함:

```json
{
  "plugins": [
    {
      "name": "document-skills",
      "description": "Collection of document processing skills",
      "source": "./",
      "strict": false,
      "skills": [
        "./.claude/skills/xlsx",
        "./.claude/skills/docx",
        "./.claude/skills/pptx",
        "./.claude/skills/pdf"
      ]
    }
  ]
}
```

**장점:**
- 사용자가 한 번에 여러 스킬 설치
- 관련 스킬을 논리적으로 그룹화
- 설치/관리 간편

---

## SKILL.md 작성법

### 기본 템플릿

```markdown
---
name: skill-name
description: |
  스킬에 대한 간단한 설명.
  Use when: [사용 시점]
  트리거: [키워드1], [키워드2]
---

# 스킬 제목

## 개요

스킬이 무엇을 하는지 설명합니다.

## 사용 시점

- 상황 1
- 상황 2

## 워크플로우

1. 단계 1
2. 단계 2
3. 단계 3

## 출력 형식

예상 출력 형식을 설명합니다.
```

### Front Matter 필수 필드

```yaml
---
name: skill-name          # 스킬 호출 시 사용되는 이름 (예: /skill-name)
description: |            # 스킬 설명 (트리거 키워드 포함)
  설명 텍스트
---
```

---

## 등록 및 테스트

### Step 1: GitHub 리포지토리 준비

```bash
# 리포지토리 생성 후
git add .
git commit -m "Initial commit"
git push origin main
```

### Step 2: 마켓플레이스 등록

```bash
# 마켓플레이스 추가
claude plugin marketplace add YourUsername/your-repo

# 성공 시 출력:
# ✔ Successfully added marketplace: your-marketplace-name
```

### Step 3: 플러그인 설치 테스트

```bash
# 플러그인 설치
claude plugin install your-plugin-name

# 설치 확인
claude plugin list | grep your-plugin-name
```

### Step 4: 스킬 테스트

Claude Code에서:
```
/your-skill-name
```

### Step 5: 업데이트 배포

```bash
# 변경사항 푸시
git add .
git commit -m "Update"
git push origin main

# 마켓플레이스 캐시 업데이트
claude plugin marketplace update your-marketplace-name

# 사용자 측 업데이트
claude plugin update your-plugin-name
```

---

## 일반적인 오류와 해결책

### 오류 1: Invalid schema

```
✘ Failed to add marketplace: Invalid schema: plugins.0.skills: Invalid input,
plugins.0.source: Invalid input
```

**원인**: `source` 필드 누락 또는 잘못된 형식

**해결**:
```json
// 각 플러그인에 source 추가
{
  "plugins": [{
    "name": "...",
    "source": "./",           // ← 추가
    "strict": false,          // ← 추가 권장
    "skills": ["./..."]
  }]
}
```

### 오류 2: Plugin not found

```
✘ Plugin "my-plugin" not found in any configured marketplace
```

**원인**: 마켓플레이스가 추가되지 않음

**해결**:
```bash
# 마켓플레이스 먼저 추가
claude plugin marketplace add YourUsername/your-repo

# 그 다음 플러그인 설치
claude plugin install my-plugin
```

### 오류 3: SKILL.md not found

**원인**: 스킬 경로가 marketplace.json의 skills 배열과 일치하지 않음

**해결**:
1. marketplace.json의 skills 경로 확인
2. 해당 경로에 SKILL.md 존재 확인
3. 경로 대소문자 일치 확인

### 오류 4: 스킬이 로드되지 않음

**원인**: SKILL.md의 front matter 형식 오류

**해결**:
```yaml
# ❌ 잘못된 형식
---
name:skill-name    # 콜론 뒤 공백 없음
---

# ✅ 올바른 형식
---
name: skill-name   # 콜론 뒤 공백 있음
---
```

---

## 참고 자료

### Anthropic 공식 마켓플레이스

- [anthropics/skills](https://github.com/anthropics/skills) - 스킬 마켓플레이스 예시
- [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) - 공식 플러그인

### 유용한 명령어

```bash
# 마켓플레이스 목록
claude plugin marketplace list

# 플러그인 목록
claude plugin list

# 플러그인 상세 정보
claude plugin list --verbose

# 마켓플레이스 업데이트
claude plugin marketplace update [marketplace-name]

# 플러그인 업데이트
claude plugin update [plugin-name]

# 플러그인 제거
claude plugin uninstall [plugin-name]

# 마켓플레이스 제거
claude plugin marketplace remove [marketplace-name]
```

---

## Research Coordinator 사례 연구

### 문제

```
✘ Failed to add marketplace: Invalid schema: plugins.0.skills: Invalid input,
plugins.0.source: Invalid input
```

### 원인 분석

1. `source` 필드 누락
2. `skills` 배열 형식이 올바르지 않음
3. 여러 플러그인을 개별 정의했으나 단일 설치 불가

### 해결 과정

1. Anthropic 공식 마켓플레이스 스키마 분석
2. `source` 및 `strict` 필드 추가
3. 다중 스킬 패턴 적용 (document-skills 참고)

### 최종 결과

```json
{
  "plugins": [{
    "name": "research-coordinator",
    "source": "./",
    "strict": false,
    "skills": [
      "./.claude/skills/research-coordinator",
      "./.claude/skills/research-agents/01-...",
      // ... 20개 더
    ]
  }]
}
```

**성과**: 단일 `claude plugin install research-coordinator`로 21개 스킬 모두 설치
