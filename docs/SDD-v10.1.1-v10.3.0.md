# Diverga v10.1.1 -- v10.3.0 Software Design Document

**Version**: 1.0
**Date**: 2026-02-23
**Authors**: Hosung You, Claude Opus 4.6
**Versions Covered**: v10.1.1, v10.2.0, v10.3.0
**Previous SDD**: SDD-v9.0.md (v9.0.0 Architecture Release)

---

## 1. 문서 정보 (Document Information)

| 항목 | 내용 |
|------|------|
| 문서 버전 | 1.0 |
| 작성일 | 2026-02-23 |
| 작성자 | Hosung You, Claude Opus 4.6 |
| 대상 버전 | v10.1.1, v10.2.0, v10.3.0 |
| 이전 버전 | v10.1.0 (Humanize Orchestration Skill) |
| 이전 SDD | SDD-v9.0.md |
| 저장소 | https://github.com/HosungYou/Diverga |

---

## 2. 요약 (Executive Summary)

이 문서는 Diverga v10.1.1, v10.2.0, v10.3.0 세 릴리스의 설계 결정과 아키텍처 변경을 기술합니다.

**v10.1.1 (Typographic Enforcement)**: G6 출력과 F5 검증에서 유니코드 타이포그래피 문자 사용을 의무화합니다. 엠 대시(---), 엔 대시(--), 스마트 따옴표를 ASCII 대체 문자 대신 사용해야 하며, ASCII `--`는 F5 FAIL 조건입니다. Zotero MCP 서버가 `.mcp.json`에서 제거되었습니다.

**v10.2.0 (Humanization Pipeline v3.1)**: 풍부한 체크포인트(Rich Checkpoint) v2.0 아키텍처를 도입하여 섹션별 점수 표시, 6개 옵션, 밸런스드(Fast) 모드(L1-3 패스 병합), G5+F5 병렬 실행, 목표 점수 자동 중단, 섹션 선택적 처리를 지원합니다.

**v10.3.0 (Journal Intelligence MCP)**: OpenAlex(기본) 및 Crossref(보조) API를 활용하는 새로운 `journal-server.js` MCP 서버(6개 도구)를 추가합니다. G1 Journal Matcher가 체크포인트 기반 파이프라인으로 재설계되었으며, 총 4개의 MCP 서버가 운영됩니다.

---

## 3. 아키텍처 변경 (Architecture Changes)

### 3.1 MCP 서버 아키텍처 (v10.3.0)

v10.3.0에서 4번째 MCP 서버인 `journal-server.js`가 추가되어 총 4개의 MCP 서버 프로세스를 운영합니다.

```
┌──────────────────────────────────────────────────────────────┐
│                    MCP Server Architecture                    │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  diverga-server.js ──→ tool-registry.js (16 tools)           │
│       │                                                       │
│       ├── checkpoint-server   (3 tools)                      │
│       ├── memory-server       (7 tools)                      │
│       └── comm-server         (6 tools)                      │
│                                                               │
│  journal-server.js ──→ 6 tools (standalone)                  │
│       │                                                       │
│       ├── OpenAlex API (primary) ─── 5 tools                 │
│       └── Crossref API (secondary) ─ 1 tool                 │
│                                                               │
│  humanizer (external) ──→ uvx from GitHub (4 tools)          │
│                                                               │
│  context7 (external) ──→ npx from npm (2 tools)             │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

| 서버 | 도구 수 | 등록 방식 | API 키 필요 |
|------|---------|-----------|------------|
| **diverga** | 16 (checkpoint/memory/comm) | `${CLAUDE_PLUGIN_ROOT}` bundle | No |
| **journal** | 6 (OpenAlex + Crossref) | `${CLAUDE_PLUGIN_ROOT}` bundle | No (이메일 권장) |
| **humanizer** | 4 (stylometric metrics) | `uvx` from GitHub | No |
| **context7** | 2 (docs lookup) | `npx` from npm | No |

**OpenAlex API 통합**:
- 무료, API 키 불필요
- 이메일 제공 시 Polite Pool 접근 (더 빠른 응답, 높은 rate limit)
- RESTful JSON API, `https://api.openalex.org` 기본 URL

**Crossref API 보조 지원**:
- 무료, API 키 불필요
- Special issues 및 최근 출판물 데이터에 활용
- `https://api.crossref.org` 기본 URL

### 3.2 휴머니제이션 파이프라인 v3.1 (v10.2.0)

v10.1.0의 파이프라인 v3.0에서 v3.1로 업그레이드되었습니다. 핵심 변경 사항:

```
┌───────────────────────────────────────────────────────────────┐
│            Humanization Pipeline v3.1 Architecture            │
├───────────────────────────────────────────────────────────────┤
│                                                                │
│  STAGE 0: G5 Analysis ──→ CP_HUMANIZATION_REVIEW              │
│    │                        (5 options + "Balanced Fast")      │
│    │                                                           │
│  ┌─┴── Standard Path ─────────── Fast Path ──────────────┐   │
│  │                                                        │   │
│  │  Pass 1: G6 (L1-2 Vocab)    G6 (L1-3 Merged)         │   │
│  │    → [G5 rescan ‖ F5 verify]  → [G5 rescan ‖ F5 verify]│  │
│  │    → CP_PASS1_REVIEW          → CP_PASS2_REVIEW        │   │
│  │                                                        │   │
│  │  Pass 2: G6 (L3 Structural)                           │   │
│  │    → [G5 rescan ‖ F5 verify]                          │   │
│  │    → CP_PASS2_REVIEW                                   │   │
│  │                                                        │   │
│  │  Pass 3: G6 (L4 Discourse DT1-DT4)                   │   │
│  │    → [G5 rescan ‖ F5 verify]                          │   │
│  │    → CP_PASS3_REVIEW                                   │   │
│  │                                                        │   │
│  │  [Pass 4: G6 (Polish) → G5+F5 → CP_FINAL_REVIEW]     │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                │
│  ‖ = parallel execution (G5+F5 are both read-only)            │
└───────────────────────────────────────────────────────────────┘
```

**Rich Checkpoint v2.0 아키텍처**:

체크포인트 데이터 구조가 확장되어 섹션별 점수를 포함합니다:

```
CP_PASSn_REVIEW:
  ├── section_scores:
  │     ├── abstract:     { before: 62%, after: 45%, patterns_remaining: 3 }
  │     ├── introduction: { before: 58%, after: 38%, patterns_remaining: 5 }
  │     ├── methods:      { before: 35%, after: 28%, patterns_remaining: 2 }
  │     ├── results:      { before: 40%, after: 30%, patterns_remaining: 1 }
  │     ├── discussion:   { before: 70%, after: 48%, patterns_remaining: 8 }
  │     └── conclusion:   { before: 55%, after: 35%, patterns_remaining: 4 }
  │
  ├── options (6):
  │     ├── [1] Continue all sections
  │     ├── [2] Select specific sections
  │     ├── [3] Per-section intensity
  │     ├── [4] Preserve specific sentences
  │     ├── [5] Accept current result
  │     └── [6] Show diff
  │
  └── target_score: 30% (auto-stop when reached)
```

**G5+F5 병렬 실행**:

각 G6 변환 후 G5 재스캔과 F5 검증이 병렬로 실행됩니다. 두 에이전트 모두 동일한 G6 출력에 대한 읽기 전용 작업이므로 데이터 무결성 위험 없이 패스당 검증 시간을 약 50% 절감합니다.

**밸런스드(Fast) 모드**:

CP_HUMANIZATION_REVIEW에서 5번째 옵션으로 추가. Pass 1 (L1-2 Vocabulary)과 Pass 2 (L3 Structural)을 단일 G6 호출로 병합하여 1회의 G5 재스캔, 1회의 F5 검증, 1회의 체크포인트 대기를 절약합니다.

**섹션 선택적 처리**:

`sections` 파라미터를 통해 특정 원고 섹션만 변환할 수 있습니다 (예: `["discussion", "conclusion"]`). 선택되지 않은 섹션은 변경 없이 통과합니다.

**목표 점수 자동 중단**:

STAGE 0에서 `target_score`를 설정 (기본값: 30%). 점수가 목표에 도달하면 다음 체크포인트에서 자동으로 "Accept"를 권장합니다.

### 3.3 타이포그래피 강제 (v10.1.1)

G6 출력의 모든 텍스트에서 유니코드 타이포그래피 문자를 의무적으로 사용합니다:

| 문자 | 유니코드 | 코드포인트 | 금지되는 ASCII 대체 |
|------|---------|-----------|-------------------|
| Em dash | --- | U+2014 | `--` |
| En dash | -- | U+2013 | `-` (범위 표기 시) |
| Left double quote | \u201C | U+201C | `"` (열린 따옴표) |
| Right double quote | \u201D | U+201D | `"` (닫힌 따옴표) |
| Left single quote | \u2018 | U+2018 | `'` (열린 작은따옴표) |
| Right single quote | \u2019 | U+2019 | `'` (닫힌 작은따옴표) |

**F5 검증 FAIL 조건**: 출력에 `--` (더블 하이픈)이 남아있으면 F5 검증이 FAIL을 반환합니다.

**Zotero MCP 제거**: `.mcp.json`에서 `zotero` 서버 항목이 삭제되어 3개 서버에서 이후 v10.3.0에서 4개 서버(journal 추가)로 변경됩니다.

---

## 4. 컴포넌트 설계 (Component Design)

### 4.1 journal-server.js

독립형 MCP 서버로 6개의 저널 인텔리전스 도구를 제공합니다.

**서버 메타데이터**:
```
Server Name: journal
Version: 10.3.0
Transport: StdioServerTransport
Capabilities: { tools: {} }
User-Agent: Diverga/10.3.0 (Journal Intelligence MCP)
```

**6개 도구**:

| 도구 | API | 설명 | 필수 파라미터 |
|------|-----|------|-------------|
| `journal_search_by_field` | OpenAlex | 연구 분야별 저널 검색, 인용 수 기준 정렬 | `field` |
| `journal_metrics` | OpenAlex | 상세 저널 지표 (h-index, 인용, OA, APC 등) | `journal_id` or `issn` or `journal_name` (최소 1개) |
| `journal_publication_trends` | OpenAlex | 연도별 출판/인용 추이 | `journal_id` |
| `journal_editor_info` | OpenAlex | 저널 내 논문 수 기준 상위 저자 | `journal_id` |
| `journal_compare` | OpenAlex | 2-5개 저널 병렬 비교 | `journal_ids` (배열, 2-5개) |
| `journal_special_issues` | Crossref | 최근 주제별 출판물/특별호 | `journal_name` or `issn` (최소 1개) |

**API 통합 패턴**:

```
                    ┌─────────────────────┐
                    │   journal-server.js  │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
    ┌─────────▼─────────┐  ┌──▼──┐  ┌─────────▼─────────┐
    │  buildOpenAlexUrl  │  │     │  │   Crossref URL    │
    │  + fetchJSON       │  │email│  │   (direct build)  │
    └─────────┬─────────┘  │ res.│  └─────────┬─────────┘
              │            └──┬──┘            │
    ┌─────────▼─────────┐    │     ┌─────────▼─────────┐
    │  api.openalex.org  │◄──┘     │ api.crossref.org   │
    │  /sources          │         │ /journals/{issn}/  │
    │  /works            │         │ /works             │
    └───────────────────┘         └───────────────────┘
```

**이메일 해석 (3-tier)**:

```
resolveEmail():
  1. process.env.OPENALEX_EMAIL → 최우선
  2. .omc/config.json → openalex_email 필드
  3. null → 작동하지만 느린 rate limit (경고 로그)
```

**오류 처리 전략**:

모든 도구 핸들러는 try-catch로 감싸져 있으며, 오류 발생 시 `{ isError: true, content: [{ type: 'text', text: 'Error: ...' }] }` 형태로 반환합니다.

| 오류 유형 | 처리 방식 |
|----------|----------|
| 알 수 없는 도구 이름 | `isError: true` + "Unknown tool" 메시지 |
| HTTP 오류 (4xx/5xx) | `Error: HTTP {status}: {statusText}` |
| 필수 파라미터 누락 | 도구별 구체적 오류 메시지 |
| 검색 결과 없음 | `Error: No journal found with ISSN: ...` |
| 네트워크 오류 | fetch 예외가 catch로 전파 |

**Rate Limiting 접근**:

OpenAlex API는 이메일 없이도 작동하지만, 이메일을 제공하면 Polite Pool에 접근하여 더 높은 rate limit을 받습니다. journal-server는 `per_page`를 도구별로 제한합니다:
- `journal_search_by_field`: max 50
- `journal_editor_info`: max 25

### 4.2 G1 Journal Matcher 파이프라인

v10.3.0에서 G1이 정적 단일 실행 에이전트에서 체크포인트 기반 파이프라인으로 재설계되었습니다.

**파이프라인 흐름**:

```
사용자 요청
    │
    ▼
┌──────────────────────────────────────────────────────────┐
│ Stage 1: 초기 검색 (병렬)                                  │
│   journal_search_by_field + journal_metrics               │
└──────────────────────┬───────────────────────────────────┘
                       │
                       ▼
            🟠 CP_JOURNAL_PRIORITIES
            (IF / Speed / OA / Scope Fit / Balanced)
                       │
                       ▼
┌──────────────────────────────────────────────────────────┐
│ Stage 2: 심층 비교 (병렬)                                  │
│   journal_compare + journal_publication_trends             │
└──────────────────────┬───────────────────────────────────┘
                       │
                       ▼
            🟠 CP_JOURNAL_SELECTION
            (저널 선택 / 다중 투고 / 추가 검색 / 재검색)
                       │
                       ▼
┌──────────────────────────────────────────────────────────┐
│ Stage 3: 상세 정보 수집 (병렬)                             │
│   journal_editor_info + journal_special_issues             │
└──────────────────────┬───────────────────────────────────┘
                       │
                       ▼
              Report + Cover Letter
              + Sequential Submission Plan
```

**자연어 라우팅 테이블**:

G1은 사용자 입력의 자연어를 분석하여 적절한 MCP 도구 조합을 선택합니다:

| 사용자 의도 | 호출되는 도구 |
|-----------|-------------|
| "OO 분야 저널 찾기" | `journal_search_by_field` |
| "이 저널의 지표" | `journal_metrics` |
| "저널 A와 B 비교" | `journal_compare` |
| "투고처 추천" | 전체 파이프라인 실행 |

### 4.3 Humanize Pipeline v3.1

**Rich Checkpoint v2.0 데이터 흐름**:

```
G6 Transform Output
    │
    ├──────────────────┐
    │                  │
    ▼                  ▼
G5 Rescan          F5 Verify
(section_scores)   (pass/fail + domains)
    │                  │
    ├──────────────────┘
    │
    ▼
Rich Checkpoint v2.0
    ├── overall_score: 42%
    ├── section_scores: { abstract: 45%, intro: 38%, ... }
    ├── top_patterns: [P1, P2, P3]
    ├── target_score: 30%
    ├── target_reached: false
    └── options: [continue_all, select_sections, per_section,
                  preserve_sentences, accept, show_diff]
```

**Fast Mode 병합 로직**:

밸런스드(Fast) 모드에서는 Pass 1과 Pass 2의 G6 지시사항이 단일 프롬프트로 병합됩니다:

```
Standard:  G6(L1-2) → G5+F5 → CP → G6(L3) → G5+F5 → CP
Fast:      G6(L1-2+L3) → G5+F5 → CP
절약:      1x G6 + 1x G5 + 1x F5 + 1x Checkpoint
```

**병렬 실행 모델**:

```
Sequential (v3.0):  G6 → G5 → F5 → Checkpoint
Parallel (v3.1):    G6 → [G5 ‖ F5] → Checkpoint

시간 절약: F5 실행 시간만큼 (각 패스마다)
안전성: G5와 F5 모두 G6 출력을 읽기만 하므로 경합 없음
```

---

## 5. 데이터 흐름 다이어그램 (Data Flow Diagrams)

### 5.1 저널 매칭 파이프라인

```
┌─────────┐    field,     ┌──────────────────┐
│  User   │───subfield───▶│ journal_search_  │──▶ journal list
│ Request │               │   by_field       │    (sorted by citations)
└────┬────┘               └──────────────────┘
     │                              │
     │  journal_id   ┌──────────────┘
     │      or       │
     │    issn       ▼
     │         ┌──────────────┐
     ├────────▶│ journal_     │──▶ h-index, citations,
     │         │   metrics    │    OA, APC, country
     │         └──────────────┘
     │
     │   🟠 CP_JOURNAL_PRIORITIES (user decides ranking criteria)
     │
     │  journal_ids  ┌──────────────┐
     ├──────────────▶│ journal_     │──▶ side-by-side
     │   (2-5)       │   compare    │    comparison table
     │               └──────────────┘
     │
     │  journal_id   ┌──────────────────┐
     ├──────────────▶│ journal_         │──▶ works/citations
     │               │ publication_     │    per year
     │               │   trends         │
     │               └──────────────────┘
     │
     │   🟠 CP_JOURNAL_SELECTION (user selects target journal)
     │
     │  journal_id   ┌──────────────┐
     ├──────────────▶│ journal_     │──▶ top authors
     │               │ editor_info  │    by pub count
     │               └──────────────┘
     │
     │  issn or      ┌──────────────────┐
     │  journal_name │ journal_special_ │──▶ recent themed
     └──────────────▶│   issues         │    publications
                     └──────────────────┘
```

### 5.2 Humanize Pipeline v3.1 (병렬 경로 포함)

```
Input Draft
    │
    ▼
┌──────────┐
│ G5 v3.0  │──▶ 28 patterns, 13 metrics, composite score
│ Analysis │    section_scores (v3.1)
└────┬─────┘
     │
     ▼
🟠 CP_HUMANIZATION_REVIEW
     │
     ├── [1] Conservative (L1-2)
     ├── [2] Balanced (L1-3)
     ├── [3] Aggressive (L1-4)
     ├── [4] Target-based
     └── [5] Balanced (Fast) ← NEW in v3.1
     │
     ▼
┌──────────────────── Standard Path ─────────────────────┐
│                                                         │
│  Pass 1: G6 (Layer 1-2: Vocab + Phrase)                │
│     │                                                   │
│     ├──────────────┐                                    │
│     ▼              ▼                                    │
│   G5 Rescan    F5 Verify    ← parallel (v3.1)         │
│     │              │                                    │
│     └──────┬───────┘                                    │
│            ▼                                            │
│     🟠 CP_PASS1_REVIEW (Rich v2.0)                     │
│     target_reached? ──▶ auto-recommend Accept (v3.1)   │
│            │                                            │
│  Pass 2: G6 (Layer 3: Structure)                       │
│     → [G5 ‖ F5] → CP_PASS2_REVIEW                     │
│            │                                            │
│  Pass 3: G6 (Layer 4: Discourse DT1-DT4)              │
│     → [G5 ‖ F5] → CP_PASS3_REVIEW                     │
│            │                                            │
│  [Pass 4: G6 (Polish) → G5+F5 → CP_FINAL_REVIEW]     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 5.3 MCP 서버 아키텍처 (4개 서버)

```
┌────────────────────────────────────────────────────────────┐
│                     Claude Code Runtime                     │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌────────┐  ┌────────┐│
│  │   diverga    │  │   journal   │  │humanizer│  │context7││
│  │ (16 tools)  │  │  (6 tools)  │  │(4 tools)│  │(2 tools)││
│  └──────┬──────┘  └──────┬──────┘  └────┬───┘  └────┬───┘│
│         │                │              │            │     │
│    StdioTransport   StdioTransport    uvx          npx    │
│         │                │              │            │     │
│  ┌──────▼──────┐  ┌──────▼──────┐      │            │     │
│  │diverga-     │  │journal-     │      │            │     │
│  │server.js    │  │server.js    │      │            │     │
│  │(bundled)    │  │(bundled)    │      │            │     │
│  └──────┬──────┘  └──────┬──────┘      │            │     │
│         │                │              │            │     │
│  ┌──────▼──────┐  ┌──────▼──────┐  ┌───▼────┐  ┌───▼───┐│
│  │YAML/SQLite  │  │OpenAlex API │  │GitHub  │  │npm    ││
│  │Local State  │  │Crossref API │  │repo    │  │registry││
│  └─────────────┘  └─────────────┘  └────────┘  └───────┘│
└────────────────────────────────────────────────────────────┘
```

---

## 6. API 명세 (API Specifications)

### 6.1 OpenAlex 엔드포인트

| 엔드포인트 | HTTP | 사용 도구 | 설명 |
|-----------|------|----------|------|
| `/sources` | GET | search_by_field, metrics (ISSN/name) | 저널 검색 및 필터링 |
| `/sources/{id}` | GET | metrics (ID), trends | 특정 저널 상세 |
| `/works` | GET | editor_info | 저널 내 저작물 그룹핑 |

**요청 헤더**:
```
User-Agent: Diverga/10.3.0 (Journal Intelligence MCP)
```

**공통 파라미터**:
- `mailto`: OpenAlex 이메일 (Polite Pool 접근)
- `per_page`: 결과 수 제한
- `filter`: 필터 조건 (예: `type:journal`, `issn:{issn}`)
- `search`: 검색어
- `sort`: 정렬 기준 (예: `cited_by_count:desc`)
- `group_by`: 그룹핑 기준 (editor_info에서 사용)

**응답 형식** (sources 검색):
```json
{
  "meta": { "count": 1234, "per_page": 10 },
  "results": [
    {
      "id": "https://openalex.org/S137773608",
      "display_name": "Computers & Education",
      "issn": ["0360-1315"],
      "cited_by_count": 123456,
      "works_count": 5000,
      "summary_stats": {
        "h_index": 200,
        "i10_index": 3000,
        "2yr_mean_citedness": 8.5
      },
      "is_oa": false,
      "type": "journal",
      "country_code": "GB",
      "counts_by_year": [...]
    }
  ]
}
```

### 6.2 Crossref 엔드포인트

| 엔드포인트 | HTTP | 사용 도구 | 설명 |
|-----------|------|----------|------|
| `/journals/{issn}/works` | GET | special_issues (ISSN) | 특정 저널 내 저작물 |
| `/works` | GET | special_issues (name) | 저작물 검색 |

**공통 파라미터**:
- `query`: 검색어
- `query.container-title`: 저널명 필터
- `sort`: `published`
- `order`: `desc`
- `rows`: 결과 수 (기본 10)
- `select`: 반환 필드 선택

**응답 형식**:
```json
{
  "message": {
    "items": [
      {
        "DOI": "10.1016/...",
        "title": ["Article Title"],
        "published": { "date-parts": [[2026, 1, 15]] },
        "subject": ["Education"],
        "type": "journal-article",
        "container-title": ["Computers & Education"]
      }
    ]
  }
}
```

### 6.3 Rate Limiting 동작

| API | 이메일 없음 | 이메일 있음 |
|-----|-----------|-----------|
| OpenAlex | ~10 req/s | ~100 req/s (Polite Pool) |
| Crossref | ~50 req/s | N/A (이메일 불필요) |

journal-server는 요청 간 인위적 지연을 추가하지 않습니다. API 측의 rate limiting에 의존하며, HTTP 429 응답은 일반 HTTP 오류로 처리됩니다.

---

## 7. 체크포인트 설계 (Checkpoint Design)

### 7.1 신규 체크포인트

**v10.3.0에서 추가**:

| 체크포인트 | 수준 | 에이전트 | 옵션 |
|-----------|------|--------|------|
| CP_JOURNAL_PRIORITIES | 🟠 Recommended | G1 | IF / Speed / OA / Scope Fit / Balanced |
| CP_JOURNAL_SELECTION | 🟠 Recommended | G1 | 저널 선택 / 다중 투고 / 추가 검색 / 재검색 |

**Rich Checkpoint v2.0 형식 명세** (v10.2.0):

```yaml
checkpoint:
  id: CP_PASS1_REVIEW
  version: "2.0"
  level: recommended
  data:
    overall_score:
      before: 58
      after: 42
    section_scores:
      abstract:
        before: 62
        after: 45
        patterns_remaining: 3
      introduction:
        before: 58
        after: 38
        patterns_remaining: 5
      methods:
        before: 35
        after: 28
        patterns_remaining: 2
      results:
        before: 40
        after: 30
        patterns_remaining: 1
      discussion:
        before: 70
        after: 48
        patterns_remaining: 8
      conclusion:
        before: 55
        after: 35
        patterns_remaining: 4
    top_patterns:
      - id: P001
        name: "Formulaic hedging"
        count: 12
      - id: P002
        name: "Excessive moreover"
        count: 8
    target_score: 30
    target_reached: false
  options:
    - id: continue_all
      label: "Continue with all sections"
    - id: select_sections
      label: "Select specific sections to continue"
    - id: per_section_intensity
      label: "Set per-section intensity"
    - id: preserve_sentences
      label: "Mark sentences to preserve"
    - id: accept
      label: "Accept current result"
    - id: show_diff
      label: "Show detailed diff"
```

### 7.2 agent-prerequisite-map.json 통합

`mcp/agent-prerequisite-map.json`에 추가된 항목:

```json
{
  "g1": {
    "prerequisites": [],
    "own_checkpoints": [
      { "id": "CP_JOURNAL_PRIORITIES", "level": "recommended" },
      { "id": "CP_JOURNAL_SELECTION", "level": "recommended" }
    ],
    "entry_point": true
  }
}
```

체크포인트 의존성 순서 (Level 0):
```
Level 0: CP_RESEARCH_DIRECTION, CP_PARADIGM_SELECTION,
         CP_JOURNAL_PRIORITIES, CP_JOURNAL_SELECTION
```

---

## 8. 테스팅 전략 (Testing Strategy)

### 8.1 단위 테스트: journal-server 도구 핸들러

`mcp/test/journal-server.test.js` (신규):

| 테스트 카테고리 | 테스트 수 | 설명 |
|---------------|---------|------|
| Tool Definitions | 8 | 6개 도구 이름, 필수 파라미터 검증 |
| OpenAlex URL Construction | 10 | URL 빌드, 파라미터 인코딩, mailto 포함/제외 |
| Crossref URL Construction | 2 | ISSN/이름 기반 URL 빌드 |
| Email Resolution | 5 | 3-tier 이메일 해석 로직 |
| Error Handling | 7 | 필수 파라미터 누락, ID 수 제한, per_page 상한 |
| Response Parsing | 6 | OpenAlex/Crossref 응답 변환 |
| MCP Handler Simulation | 8 | 디스패치, 오류 래핑, JSON 포맷 |

**테스트 패턴**: `node:test` + `node:assert/strict` (프로젝트 표준)

### 8.2 통합 테스트: OpenAlex API 연결

네트워크 접근이 필요한 통합 테스트는 주석 처리되어 있으며, `// INTEGRATION: requires network` 표시와 함께 선택적으로 실행할 수 있습니다.

### 8.3 기존 테스트 스위트

| 스위트 | 테스트 수 | 설명 |
|-------|---------|------|
| sqlite-state-v9 | 48 | SQLite 상태 저장소 |
| messaging-v9 | 45 | 에이전트 메시징 |
| checkpoint-server-v9 | 37 | 체크포인트 서버 |
| memory-server-v9 | 55 | 메모리 서버 |
| comm-server-v9 | 85 | 통신 서버 |
| tool-registry-v9 | 43 | 도구 등록 |
| sqlite-servers-v9 | 72 | SQLite 백엔드 + 마이그레이션 |
| integration-v9 | 23 | E2E (양쪽 백엔드) |
| checkpoint-server (legacy) | 56 | v8 호환성 |
| **journal-server** | **46** | **저널 MCP (신규)** |
| **Total** | **510+** | |

---

## 9. 배포 (Deployment)

### 9.1 플러그인 마켓플레이스 업데이트

```bash
# 플러그인 업데이트
/plugin marketplace update diverga

# 또는 재설치
/plugin uninstall diverga
/plugin install diverga
```

### 9.2 로컬 스킬 복사

```bash
# 저장소 업데이트
cd ~/.claude/plugins/diverga
git pull origin main

# 스킬 재복사
for skill_dir in skills/*/; do
  skill_name=$(basename "$skill_dir")
  cp -r "$skill_dir" ~/.claude/skills/diverga-${skill_name}
done
```

### 9.3 MCP 서버 자동 등록

`.mcp.json` 설정으로 4개 서버가 자동 등록됩니다:

```json
{
  "mcpServers": {
    "diverga": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/mcp/diverga-server.js"]
    },
    "journal": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/mcp/journal-server.js"]
    },
    "humanizer": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/HosungYou/humanizer.git", "humanizer-mcp"]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

수동 `settings.json` 구성이 필요 없습니다. 플러그인 설치만으로 전체 MCP 스택이 활성화됩니다.

### 9.4 OpenAlex 이메일 설정 (선택 사항)

```bash
# 방법 1: 환경 변수
export OPENALEX_EMAIL="your@email.com"

# 방법 2: /diverga:setup (Step 2)
# → .omc/config.json에 openalex_email 저장
```

---

## 10. 위험 평가 (Risk Assessment)

### 10.1 OpenAlex API 가용성

| 위험 | 영향 | 완화 방안 |
|------|------|----------|
| OpenAlex API 다운타임 | journal 도구 5개 사용 불가 | Crossref 대체 가능 (제한적), 오류 메시지로 사용자에게 알림 |
| Rate Limiting (이메일 없음) | 응답 지연, 간헐적 429 오류 | `/diverga:setup` Step 2에서 이메일 설정 안내 |
| API 응답 스키마 변경 | 파싱 실패 | Optional chaining (`?.`) 및 nullish coalescing (`??`) 사용으로 방어적 파싱 |
| OpenAlex SLA 없음 | 프로덕션 보장 없음 | 무료 서비스이므로 SLA가 없는 점을 사용자에게 안내, 캐싱 고려 (향후) |

### 10.2 이메일 없는 Rate Limiting

이메일을 제공하지 않으면 OpenAlex의 일반 풀(~10 req/s)에서 작동합니다. 단일 G1 파이프라인 실행은 최대 6-8개의 API 호출을 발생시키므로 일반적인 사용에서는 문제가 되지 않습니다. 그러나 여러 저널을 동시에 비교하거나 반복 검색 시 rate limit에 도달할 수 있습니다.

### 10.3 Crossref Special Issues 데이터 품질

Crossref API는 "special issue" 라벨을 직접 제공하지 않습니다. `journal_special_issues` 도구는 최근 주제별 출판물을 반환하며, 이는 실제 special issue와 일치하지 않을 수 있습니다. `subject` 태그와 출판 날짜를 기반으로 추론합니다.

### 10.4 타이포그래피 강제 호환성

일부 출판 시스템이나 LaTeX 템플릿에서 유니코드 타이포그래피 문자가 올바르게 렌더링되지 않을 수 있습니다. F5 검증의 FAIL 조건(ASCII `--`)은 엄격하지만, 사용자가 최종 출력에서 필요에 따라 조정할 수 있습니다.

### 10.5 파이프라인 복잡도 증가

v3.1 파이프라인은 Rich Checkpoint, 병렬 실행, 섹션 선택 등 여러 기능이 추가되어 복잡도가 증가했습니다. 주요 위험:

| 위험 | 완화 방안 |
|------|----------|
| 체크포인트 옵션 과다 (6개) | 기본 옵션(continue/accept) 강조 |
| 병렬 G5+F5 결과 불일치 | 두 결과를 독립적으로 처리, 합의 불필요 |
| Fast 모드 품질 저하 | 동일 Layer 적용, 순서만 병합 |
| 목표 점수 자동 중단 오류 | 사용자 오버라이드 항상 가능 |

---

## 부록 A: 변경 파일 요약

### v10.1.1

| 파일 | 변경 |
|------|------|
| `CLAUDE.md` | 타이포그래피 강제 섹션 추가, MCP 서버 수 업데이트 |
| `.mcp.json` | `zotero` 서버 항목 제거 |
| `CHANGELOG.md` | v10.1.1 항목 |

### v10.2.0

| 파일 | 변경 |
|------|------|
| `skills/humanize/SKILL.md` | v1.0.0 -> v1.1.0 (Rich CP v2.0, Fast 모드, 병렬 G5+F5) |
| `skills/g5/SKILL.md` | Section-Level Scores v3.1 서브섹션 추가 |
| `skills/g6/SKILL.md` | `sections` 입력 파라미터 추가 |
| `CLAUDE.md` | v10.2.0 업데이트 |
| `CHANGELOG.md` | v10.2.0 항목 |

### v10.3.0

| 파일 | 변경 |
|------|------|
| `mcp/journal-server.js` | **신규** -- Journal Intelligence MCP 서버 |
| `mcp/test/journal-server.test.js` | **신규** -- 46개 단위 테스트 |
| `.mcp.json` | `journal` 서버 추가 (4개 서버) |
| `skills/g1/SKILL.md` | v10.0.0 (MCP 파이프라인, 체크포인트) |
| `mcp/agent-prerequisite-map.json` | G1 체크포인트 + dependency_order |
| `skills/setup/SKILL.md` | Step 2 (OpenAlex 이메일) 추가 |
| `CLAUDE.md` | v10.3.0 업데이트 |
| `CHANGELOG.md` | v10.3.0 항목 |

---

## 부록 B: 버전 간 MCP 도구 수 변화

| 버전 | diverga | journal | humanizer | context7 | zotero | 합계 |
|------|---------|---------|-----------|----------|--------|------|
| v9.2.1 | 16 | -- | 4 | 2 | ~20 | ~42 |
| v10.1.0 | 16 | -- | 4 | 2 | ~20 | ~42 |
| v10.1.1 | 16 | -- | 4 | 2 | -- | 22 |
| v10.2.0 | 16 | -- | 4 | 2 | -- | 22 |
| v10.3.0 | 16 | **6** | 4 | 2 | -- | **28** |
