# Research Coordinator v3.0 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Upgrade Research Coordinator from v2.x to v3.0 with modular architecture, 5 creative mechanisms, and full user collaboration mode via AskUserQuestion pattern.

**Architecture:** Modular skill structure (core/creativity/interaction) with centralized checkpoint system. All FULL VS agents get complete creative suite; ENHANCED get selective; LIGHT get minimal upgrades. Single installation maintained via marketplace.json.

**Tech Stack:** Claude Code Skills (SKILL.md), YAML (agent-registry), Markdown templates, AskUserQuestion tool integration

---

## Phase 1: Core Infrastructure

### Task 1.1: Create Directory Structure

**Files:**
- Create: `.claude/skills/research-coordinator/core/` (directory)
- Create: `.claude/skills/research-coordinator/creativity/` (directory)
- Create: `.claude/skills/research-coordinator/interaction/` (directory)

**Step 1: Create module directories**

```bash
mkdir -p ".claude/skills/research-coordinator/core"
mkdir -p ".claude/skills/research-coordinator/creativity"
mkdir -p ".claude/skills/research-coordinator/interaction"
```

**Step 2: Verify structure**

Run: `ls -la .claude/skills/research-coordinator/`
Expected: core/, creativity/, interaction/, references/, SKILL.md

**Step 3: Commit**

```bash
git add .claude/skills/research-coordinator/
git commit -m "chore: create v3.0 modular directory structure"
```

---

### Task 1.2: Create VS Engine (core/vs-engine.md)

**Files:**
- Create: `.claude/skills/research-coordinator/core/vs-engine.md`

**Step 1: Write vs-engine.md**

```markdown
---
name: vs-engine
description: |
  Enhanced VS 5-Phase Engine with user checkpoints and iteration support.
  Core engine for all VS-enabled agents.
version: "3.0.0"
---

# VS Engine v3.0

## Overview

Enhanced Verbalized Sampling engine with:
- Dynamic T-Score integration
- User checkpoints at critical decision points
- Iterative refinement (Phase 5 → Phase 2 loop)
- Creativity module hooks

## Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│                 VS Engine Execution Flow                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ▶ INITIALIZATION                                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ⬜ CP-INIT-001: Research Type Selection              │   │
│  │    Options: Quantitative / Qualitative / Mixed /    │   │
│  │             Meta-analysis                            │   │
│  │                                                      │   │
│  │ ⬜ CP-INIT-002: Creativity Level Selection           │   │
│  │    Options:                                          │   │
│  │    - Conservative (T≥0.5): Safe, validated          │   │
│  │    - Balanced (T≥0.3): Differentiated + safe        │   │
│  │    - Innovative (T≥0.2): High contribution          │   │
│  │    - Extreme (T<0.2): Maximum creativity            │   │
│  │                                                      │   │
│  │ ⬜ CP-INIT-003: T-Score Mode Selection               │   │
│  │    Options: Static / Dynamic (API) / Hybrid         │   │
│  └─────────────────────────────────────────────────────┘   │
│         │                                                   │
│         ▼                                                   │
│  ▶ PHASE 0: Context Collection (MANDATORY)                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Required:                                            │   │
│  │   - Research domain                                  │   │
│  │   - Research question                                │   │
│  │   - Key variables                                    │   │
│  │   - Target journal level                             │   │
│  │                                                      │   │
│  │ Optional:                                            │   │
│  │   - Existing theory preferences                      │   │
│  │   - Methodology constraints                          │   │
│  └─────────────────────────────────────────────────────┘   │
│         │                                                   │
│         ▼                                                   │
│  ▶ PHASE 1: Modal Response Identification                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Process:                                             │   │
│  │   1. Query T-Score system (static or dynamic)        │   │
│  │   2. Identify top 3-5 modal options (T > 0.8)        │   │
│  │   3. Mark as BASELINE (to be exceeded)               │   │
│  │                                                      │   │
│  │ Output Format:                                       │   │
│  │   ⚠️ MODAL WARNING: These are most predictable:     │   │
│  │   | Option | T-Score | Usage Rate | Issue |          │   │
│  │   |--------|---------|------------|-------|          │   │
│  │   | [X]    | 0.9+    | 60%+       | [Y]   |          │   │
│  └─────────────────────────────────────────────────────┘   │
│         │                                                   │
│         ▼                                                   │
│  ▶ PHASE 2: Long-Tail Sampling (EXPANDED)                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Generate 5-7 directions (expanded from 3):           │   │
│  │                                                      │   │
│  │ Direction A (T≈0.7): Safe differentiation           │   │
│  │ Direction B (T≈0.5): Established but specific       │   │
│  │ Direction C (T≈0.4): Unique and justifiable         │   │
│  │ Direction D (T≈0.3): Emerging approach              │   │
│  │ Direction E (T≈0.2): Innovative                     │   │
│  │ Direction F (T<0.2): Experimental (if Extreme mode) │   │
│  │ Direction G: Cross-domain (if creativity enabled)   │   │
│  │                                                      │   │
│  │ ⬜ CP-VS-001: Direction Selection (multi-select)     │   │
│  │    "Select directions you want to explore further"  │   │
│  └─────────────────────────────────────────────────────┘   │
│         │                                                   │
│         ▼                                                   │
│  ▶ PHASE 3: Low-Typicality Selection                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Selection Criteria:                                  │   │
│  │   1. Academic soundness (peer-review defensible)     │   │
│  │   2. Context fit (alignment with RQ)                 │   │
│  │   3. Contribution potential                          │   │
│  │   4. Feasibility                                     │   │
│  │                                                      │   │
│  │ ⬜ CP-VS-002: Risk Warning (if T < 0.3)              │   │
│  │    "Selected option has T-Score [X]. Limited        │   │
│  │     academic evidence. Proceed?"                     │   │
│  │    Options:                                          │   │
│  │    - Yes, proceed (accept risk)                      │   │
│  │    - Show safer alternatives (T≥0.3)                │   │
│  │    - Show defense rationale first                    │   │
│  └─────────────────────────────────────────────────────┘   │
│         │                                                   │
│         ▼                                                   │
│  ▶ PHASE 4: Execution                                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Execute selected approach with:                      │   │
│  │   - Academic rigor maintained                        │   │
│  │   - Creativity module integration (if enabled)       │   │
│  │   - Detailed output generation                       │   │
│  │                                                      │   │
│  │ Creativity Module Hooks:                             │   │
│  │   {{if forced_analogy_enabled}}                      │   │
│  │     → creativity/forced-analogy.md                   │   │
│  │   {{if iterative_loop_enabled}}                      │   │
│  │     → creativity/iterative-loop.md                   │   │
│  │   {{if semantic_distance_enabled}}                   │   │
│  │     → creativity/semantic-distance.md                │   │
│  │   {{if community_simulation_enabled}}                │   │
│  │     → creativity/community-simulation.md             │   │
│  └─────────────────────────────────────────────────────┘   │
│         │                                                   │
│         ▼                                                   │
│  ▶ PHASE 5: Originality Verification                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Checklist:                                           │   │
│  │   ✅ Modal Avoidance:                                │   │
│  │      - [ ] "Would 80% of AIs recommend this?" → NO  │   │
│  │      - [ ] "Top 5 in similar research?" → NO        │   │
│  │      - [ ] "Reviewer would say 'obvious'?" → NO     │   │
│  │                                                      │   │
│  │   ✅ Quality Check:                                  │   │
│  │      - [ ] Peer-review defensible? → YES            │   │
│  │      - [ ] Validated instruments exist? → YES       │   │
│  │      - [ ] Logical hypothesis derivation? → YES     │   │
│  │                                                      │   │
│  │ ⬜ CP-VS-003: Satisfaction Check                     │   │
│  │    "Are you satisfied with this result?"            │   │
│  │    Options:                                          │   │
│  │    - Yes, complete                                   │   │
│  │    - Re-explore (return to Phase 2)                 │   │
│  │    - Try different approach                          │   │
│  └─────────────────────────────────────────────────────┘   │
│         │                                                   │
│         ▼                                                   │
│  ▶ OUTPUT + SELF-CRITIQUE                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Checkpoint Integration

This engine uses checkpoints from `interaction/user-checkpoints.md`:
- CP-INIT-001, CP-INIT-002, CP-INIT-003 (Initialization)
- CP-VS-001 (Direction Selection)
- CP-VS-002 (Risk Warning)
- CP-VS-003 (Satisfaction Check)

## Creativity Module Integration

When creativity modules are enabled, the engine calls:
- `creativity/forced-analogy.md` - Cross-domain concept mapping
- `creativity/iterative-loop.md` - Divergent-convergent cycles
- `creativity/semantic-distance.md` - Embedding-based recommendations
- `creativity/temporal-reframing.md` - Time perspective shifts
- `creativity/community-simulation.md` - Virtual researcher feedback

## Usage in Agents

```markdown
# In agent SKILL.md:

## VS Engine Execution
{{include: ../../core/vs-engine.md}}

Settings:
  creativity_level: {{user_selected}}
  t_score_mode: {{user_selected}}
  creativity_modules: [forced-analogy, iterative-loop]
```
```

**Step 2: Verify file created**

Run: `cat .claude/skills/research-coordinator/core/vs-engine.md | head -20`
Expected: File content with YAML frontmatter

**Step 3: Commit**

```bash
git add .claude/skills/research-coordinator/core/vs-engine.md
git commit -m "feat(core): add VS Engine v3.0 with checkpoints and iteration"
```

---

### Task 1.3: Create Dynamic T-Score System (core/t-score-dynamic.md)

**Files:**
- Create: `.claude/skills/research-coordinator/core/t-score-dynamic.md`

**Step 1: Write t-score-dynamic.md**

```markdown
---
name: t-score-dynamic
description: |
  Dynamic T-Score calculation system with API integration.
  Provides real-time typicality scoring based on recent usage.
version: "3.0.0"
---

# Dynamic T-Score System v3.0

## Overview

Replaces static T-Score tables with dynamic calculation based on:
- Real-time API queries (Semantic Scholar, OpenAlex)
- Recency-weighted usage frequency
- Domain-specific adjustments
- Trend detection (rising/falling popularity)

## T-Score Calculation Formula

```
dynamic_t_score = base_score + recency_modifier + domain_modifier + trend_modifier

Where:
  base_score: Static baseline from reference tables (0.0-1.0)
  recency_modifier: Recent 3-year usage adjustment (-0.15 to +0.15)
  domain_modifier: Domain-specific weight (-0.1 to +0.1)
  trend_modifier: Popularity trend adjustment (-0.1 to +0.1)
```

## Modes

### 1. Static Mode (Default Fallback)

Uses pre-defined T-Score tables from `references/VS-Research-Framework.md`.

```yaml
static_tables:
  theoretical_frameworks:
    TAM: 0.95
    SCT: 0.90
    UTAUT: 0.88
    SDT: 0.70
    CLT: 0.65
    # ... more in reference file

  statistical_methods:
    t-test: 0.92
    ANOVA: 0.88
    OLS_regression: 0.85
    HLM: 0.65
    SEM: 0.60
    Bayesian: 0.40
    # ... more in reference file
```

### 2. Dynamic Mode (API-Based)

Queries external APIs to calculate real-time T-Score.

```yaml
api_configuration:
  primary: semantic_scholar
  fallback: openalex
  cache_duration: 24h
  timeout: 5s

  semantic_scholar:
    endpoint: "https://api.semanticscholar.org/graph/v1/paper/search"
    fields: ["title", "year", "citationCount"]
    rate_limit: 100/minute

  openalex:
    endpoint: "https://api.openalex.org/works"
    mailto: "research-coordinator@example.com"
    rate_limit: 10/second
```

**Query Template:**

```
Search: "{theory_name}" AND "{domain}" AND year:[{current_year-3} TO {current_year}]
Count: Total papers using this theory in domain
```

**Recency Modifier Calculation:**

```python
def calculate_recency_modifier(theory, domain):
    """
    Calculate recency modifier based on recent usage.

    Returns:
      -0.15 to +0.15 adjustment to base T-Score
    """
    recent_count = query_api(theory, domain, years=3)
    historical_avg = get_historical_average(theory, domain)

    ratio = recent_count / historical_avg if historical_avg > 0 else 1.0

    if ratio > 1.5:
        # Rapidly increasing usage → higher T-Score (more modal)
        return min(0.15, (ratio - 1.0) * 0.1)
    elif ratio < 0.5:
        # Declining usage → lower T-Score (less modal)
        return max(-0.15, (ratio - 1.0) * 0.1)
    else:
        return 0.0
```

### 3. Hybrid Mode (Recommended)

Combines static baseline with trend adjustments.

```yaml
hybrid_calculation:
  base: static_table
  adjustments:
    - recency_modifier (API-based, cached)
    - trend_modifier (3-year slope analysis)

  fallback_on_api_failure: static_only
```

## User Checkpoint Integration

```markdown
⬜ CP-INIT-003: T-Score Mode Selection

"How should T-Score be calculated?"

Options:
  ○ Static (Fast, stable)
    Use pre-defined tables. Best for offline use.

  ○ Dynamic (Recommended)
    Query APIs for real-time data. Most accurate.

  ○ Hybrid
    Static baseline with trend adjustments. Balanced.
```

## Domain-Specific Adjustments

```yaml
domain_modifiers:
  education:
    TAM: +0.05    # Even more overused in EdTech
    SDT: -0.05    # Less common, good differentiation

  psychology:
    SCT: +0.05    # Very dominant
    ACT: -0.10    # Underutilized

  HRD:
    TAM: +0.10    # Extremely overused
    JD-R: -0.05   # Growing but not saturated

  healthcare:
    TPB: +0.05    # Dominant in health behavior
    COM-B: -0.10  # Newer, less saturated
```

## T-Score Reference Tables

### Theoretical Frameworks (Default Static Values)

```
T > 0.8 (MODAL - AVOID):
├── Technology Acceptance Model (TAM): 0.95
├── Social Cognitive Theory (SCT): 0.90
├── Theory of Planned Behavior (TPB): 0.88
├── UTAUT/UTAUT2: 0.85
└── Self-Efficacy Theory (standalone): 0.82

T 0.5-0.8 (ESTABLISHED - DIFFERENTIATE):
├── Self-Determination Theory (SDT): 0.70
├── Cognitive Load Theory (CLT): 0.65
├── Flow Theory: 0.62
├── Community of Inquiry (CoI): 0.58
├── Expectancy-Value Theory: 0.55
└── Achievement Goal Theory: 0.52

T 0.3-0.5 (EMERGING - RECOMMENDED):
├── Control-Value Theory: 0.45
├── Theory Integration (e.g., TAM×SDT): 0.42
├── Context-Specific Adaptations: 0.40
├── Multi-level Theory Applications: 0.38
└── Competing Theory Comparison: 0.35

T < 0.3 (INNOVATIVE - TOP-TIER):
├── Novel Theoretical Synthesis: 0.25
├── Cross-Domain Theory Transfer: 0.22
├── Meta-Theoretical Frameworks: 0.18
└── Paradigm Shift Proposals: 0.15
```

### Statistical Methods

```
T > 0.8 (MODAL - AVOID):
├── Independent t-test: 0.92
├── One-way ANOVA: 0.88
├── OLS Regression: 0.85
└── Pearson correlation: 0.82

T 0.5-0.8 (ESTABLISHED):
├── Hierarchical Linear Modeling (HLM): 0.65
├── Structural Equation Modeling (SEM): 0.60
├── Traditional Meta-analysis: 0.58
└── Mixed-effects models: 0.55

T 0.3-0.5 (EMERGING - RECOMMENDED):
├── Bayesian methods: 0.45
├── Meta-Analytic SEM (MASEM): 0.42
├── Machine Learning + inference: 0.40
└── Causal inference methods: 0.38

T < 0.3 (INNOVATIVE):
├── Causal discovery algorithms: 0.28
├── Network psychometrics: 0.25
├── Computational modeling: 0.22
└── Novel hybrid methods: 0.18
```

## Error Handling

```yaml
error_handling:
  api_timeout:
    action: fallback_to_static
    log: "API timeout, using static T-Score"

  api_rate_limit:
    action: use_cached_or_static
    retry_after: 60s

  invalid_query:
    action: fallback_to_static
    log: "Invalid query, check theory/domain names"

  no_results:
    action: use_base_score_only
    note: "No recent papers found, theory may be novel"
```

## Usage Example

```markdown
# In agent execution:

1. User selects T-Score mode (CP-INIT-003)
2. Engine queries T-Score for requested theory/method
3. Returns: { theory: "SDT", t_score: 0.68, mode: "dynamic", confidence: "high" }
4. Agent uses T-Score for modal identification and sampling
```
```

**Step 2: Verify file created**

Run: `cat .claude/skills/research-coordinator/core/t-score-dynamic.md | head -20`
Expected: File content with YAML frontmatter

**Step 3: Commit**

```bash
git add .claude/skills/research-coordinator/core/t-score-dynamic.md
git commit -m "feat(core): add dynamic T-Score system with API integration"
```

---

## Phase 2: Interaction Module

### Task 2.1: Create User Checkpoints System (interaction/user-checkpoints.md)

**Files:**
- Create: `.claude/skills/research-coordinator/interaction/user-checkpoints.md`

**Step 1: Write user-checkpoints.md**

```markdown
---
name: user-checkpoints
description: |
  Centralized user checkpoint system for Research Coordinator v3.0.
  Implements AskUserQuestion pattern for all major decision points.
version: "3.0.0"
---

# User Checkpoints System v3.0

## Overview

This module defines all user interaction checkpoints using the AskUserQuestion tool pattern. In "Full Collaboration" mode, users are consulted at every major decision point.

## Checkpoint Types

| Type | Icon | Purpose | Example |
|------|------|---------|---------|
| PREFERENCE | 🔵 | User preference selection | Creativity level |
| APPROVAL | 🟡 | Explicit approval needed | Analogy acceptance |
| GUARDRAIL | 🔴 | Risk acknowledgment | Low T-Score warning |
| ITERATION | 🟢 | Process control | Satisfaction check |

## Standard Schema

All checkpoints follow this schema for AskUserQuestion integration:

```yaml
checkpoint:
  id: "CP-{MODULE}-{NUMBER}"
  type: "PREFERENCE | APPROVAL | GUARDRAIL | ITERATION"
  phase: "VS Phase or module name"

  question:
    header: "Max 12 chars label"
    text: "Clear question text"
    context: "Current situation (optional)"

  options:
    - label: "Option display text"
      description: "Detailed explanation"
      risk_level: "low | medium | high"  # GUARDRAIL only
      recommended: true | false

  multiSelect: true | false
  fallback: "Default action if no response"
```

---

## Initialization Checkpoints

### CP-INIT-001: Research Type Selection

```yaml
id: CP-INIT-001
type: PREFERENCE
phase: initialization

question:
  header: "연구 유형"
  text: "이 연구의 유형을 선택해주세요."

options:
  - label: "양적 연구 (Quantitative)"
    description: "통계적 분석 기반 연구"
    recommended: false
  - label: "질적 연구 (Qualitative)"
    description: "심층 인터뷰, 관찰 등 질적 방법"
    recommended: false
  - label: "혼합 연구 (Mixed Methods)"
    description: "양적+질적 방법 통합"
    recommended: false
  - label: "메타분석 (Meta-analysis)"
    description: "기존 연구 통합 분석"
    recommended: false

multiSelect: false
fallback: "양적 연구"
```

### CP-INIT-002: Creativity Level Selection

```yaml
id: CP-INIT-002
type: PREFERENCE
phase: initialization

question:
  header: "창의성 수준"
  text: "이 연구에서 원하시는 창의성 수준을 선택해주세요."
  context: "높은 창의성은 더 독창적인 결과를 제공하지만, 학술적 방어가 더 필요합니다."

options:
  - label: "Conservative (T≥0.5)"
    description: "검증된 접근, 안전한 선택. 첫 출판이나 보수적 저널에 적합."
    risk_level: low
    recommended: false
  - label: "Balanced (T≥0.3) (권장)"
    description: "차별화와 안전성의 균형. 대부분의 연구에 적합."
    risk_level: low
    recommended: true
  - label: "Innovative (T≥0.2)"
    description: "높은 기여 가능성, 추가 정당화 필요. 혁신 지향 저널에 적합."
    risk_level: medium
    recommended: false
  - label: "Extreme (T<0.2)"
    description: "최대 창의성, 높은 위험. 탑티어 저널이나 패러다임 전환 목표."
    risk_level: high
    recommended: false

multiSelect: false
fallback: "Balanced (T≥0.3)"
```

### CP-INIT-003: T-Score Mode Selection

```yaml
id: CP-INIT-003
type: PREFERENCE
phase: initialization

question:
  header: "T-Score 모드"
  text: "T-Score 계산 방식을 선택해주세요."

options:
  - label: "정적 (Static)"
    description: "사전 정의된 테이블 사용. 빠르고 안정적, 오프라인 가능."
    recommended: false
  - label: "동적 (Dynamic) (권장)"
    description: "API로 실시간 데이터 조회. 가장 정확, 약간 느릴 수 있음."
    recommended: true
  - label: "하이브리드 (Hybrid)"
    description: "정적 기준선 + 트렌드 보정. 균형 잡힌 접근."
    recommended: false

multiSelect: false
fallback: "정적 (Static)"
```

---

## VS Engine Checkpoints

### CP-VS-001: Direction Selection

```yaml
id: CP-VS-001
type: PREFERENCE
phase: "VS Phase 2"

question:
  header: "탐색 방향"
  text: "탐색할 방향을 선택해주세요. 여러 개 선택 가능합니다."
  context: "선택한 방향들을 심층 분석합니다."

options:
  # Options are dynamically generated based on VS Phase 2 output
  # Template:
  - label: "방향 A (T=0.X): [이론/방법명]"
    description: "[간략 설명]. 적합: [타겟]"
    recommended: false  # Typically B or C is recommended

multiSelect: true
fallback: "방향 B, C 자동 선택"
```

### CP-VS-002: Low-Typicality Risk Warning

```yaml
id: CP-VS-002
type: GUARDRAIL
phase: "VS Phase 3"

question:
  header: "위험 확인"
  text: "선택하신 옵션의 T-Score가 [X]로, 학술적 근거가 제한적입니다. 진행하시겠습니까?"
  context: |
    고려사항:
    - 피어리뷰에서 추가 정당화 필요
    - 측정도구 개발/번안 가능성
    - 리뷰어 설득을 위한 강한 논리 필요

options:
  - label: "예, 진행합니다"
    description: "위험을 수용하고 혁신적 접근을 진행합니다."
    risk_level: high
    recommended: false
  - label: "더 안전한 대안 보기"
    description: "T-Score ≥ 0.3인 대안들을 다시 보여드립니다."
    risk_level: low
    recommended: true
  - label: "방어 논리 먼저 보기"
    description: "이 선택에 대한 학술적 방어 논리를 먼저 제시합니다."
    risk_level: medium
    recommended: false

multiSelect: false
fallback: "더 안전한 대안 보기"
```

### CP-VS-003: Satisfaction Check

```yaml
id: CP-VS-003
type: ITERATION
phase: "VS Phase 5"

question:
  header: "만족도 확인"
  text: "결과에 만족하시나요?"

options:
  - label: "예, 완료합니다"
    description: "현재 결과로 진행합니다."
    recommended: true
  - label: "다시 탐색합니다"
    description: "Phase 2로 돌아가 다른 방향을 탐색합니다."
    recommended: false
  - label: "다른 접근을 시도합니다"
    description: "창의적 장치를 활용해 새로운 접근을 시도합니다."
    recommended: false

multiSelect: false
fallback: "예, 완료합니다"
```

---

## Creativity Module Checkpoints

### CP-FA-001: Forced Analogy Source Selection

```yaml
id: CP-FA-001
type: PREFERENCE
phase: "creativity/forced-analogy"

question:
  header: "유추 소스"
  text: "유추할 소스 분야를 선택해주세요."

options:
  - label: "무작위 선택 (권장)"
    description: "시스템이 무작위로 분야를 선택합니다. 최대 창의성."
    recommended: true
  - label: "자연과학 계열"
    description: "생태학, 물리학, 화학, 생물학에서 개념을 가져옵니다."
    recommended: false
  - label: "인문학 계열"
    description: "철학, 역사학, 언어학에서 개념을 가져옵니다."
    recommended: false
  - label: "직접 지정"
    description: "원하는 분야를 직접 입력합니다."
    recommended: false

multiSelect: false
fallback: "무작위 선택"
```

### CP-FA-002: Analogy Approval

```yaml
id: CP-FA-002
type: APPROVAL
phase: "creativity/forced-analogy"

question:
  header: "유추 승인"
  text: "이 유추가 적절해 보이나요?"
  context: |
    소스: [Source Field] - [Source Concept]
    타겟: [Target Research]
    매핑: [Proposed Mapping]

options:
  - label: "예, 적용합니다"
    description: "이 유추를 연구에 적용합니다."
    recommended: true
  - label: "다른 유추를 요청합니다"
    description: "새로운 유추를 생성합니다."
    recommended: false
  - label: "건너뛰기"
    description: "강제 유추 없이 진행합니다."
    recommended: false

multiSelect: false
fallback: "건너뛰기"
```

### CP-IL-001 to CP-IL-004: Iterative Loop Checkpoints

```yaml
# CP-IL-001: Round 1 Direction Selection
id: CP-IL-001
type: PREFERENCE
phase: "creativity/iterative-loop Round 1"
question:
  header: "관심 방향"
  text: "Wide Exploration 결과 중 관심 있는 방향을 선택해주세요."
multiSelect: true

# CP-IL-002: Round 2 Combination Approval
id: CP-IL-002
type: APPROVAL
phase: "creativity/iterative-loop Round 2"
question:
  header: "조합 승인"
  text: "다음 조합을 진행할까요?"

# CP-IL-003: Round 3 Guardrail Level
id: CP-IL-003
type: PREFERENCE
phase: "creativity/iterative-loop Round 3"
question:
  header: "가드레일 수준"
  text: "적용할 가드레일 수준을 선택해주세요."
options:
  - label: "엄격 (Strict)"
    description: "모든 학술적 기준 적용"
  - label: "균형 (Balanced) (권장)"
    description: "핵심 기준만 적용"
    recommended: true
  - label: "유연 (Flexible)"
    description: "최소 기준만 적용"

# CP-IL-004: Round 4 Final Selection
id: CP-IL-004
type: APPROVAL
phase: "creativity/iterative-loop Round 4"
question:
  header: "최종 선택"
  text: "최종 결과를 승인하시겠습니까?"
```

### CP-SD-001: Semantic Distance Threshold

```yaml
id: CP-SD-001
type: PREFERENCE
phase: "creativity/semantic-distance"

question:
  header: "거리 임계값"
  text: "의미적 거리 임계값을 선택해주세요."

options:
  - label: "가까운 조합 (distance > 0.3)"
    description: "안전한 조합, 낮은 위험"
    recommended: false
  - label: "중간 거리 (distance > 0.5) (권장)"
    description: "균형 잡힌 조합"
    recommended: true
  - label: "먼 조합 (distance > 0.7)"
    description: "혁신적 조합, 강한 정당화 필요"
    recommended: false
  - label: "최대 거리 (distance > 0.85)"
    description: "실험적 조합, 높은 위험"
    recommended: false

multiSelect: false
fallback: "중간 거리"
```

### CP-TR-001: Temporal Reframing Perspective

```yaml
id: CP-TR-001
type: PREFERENCE
phase: "creativity/temporal-reframing"

question:
  header: "시간 관점"
  text: "어떤 시간 관점을 적용할까요?"

options:
  - label: "과거 (1990s)"
    description: "당시 이 연구를 했다면? 역사적 맥락 이해."
    recommended: false
  - label: "미래 (2035)"
    description: "10년 후 이 연구를 본다면? 현재 한계 예측."
    recommended: false
  - label: "평행 우주"
    description: "이 분야가 다르게 발전했다면? 대안 체계 탐색."
    recommended: false
  - label: "전체 적용 (권장)"
    description: "세 관점 모두 분석합니다."
    recommended: true

multiSelect: false
fallback: "전체 적용"
```

### CP-CS-001: Community Simulation Persona Selection

```yaml
id: CP-CS-001
type: PREFERENCE
phase: "creativity/community-simulation"

question:
  header: "페르소나 선택"
  text: "피드백 받을 가상 연구자를 선택해주세요."

options:
  - label: "전체 (7명 모두)"
    description: "모든 페르소나의 피드백을 받습니다."
    recommended: false
  - label: "핵심 3명 (권장)"
    description: "보수적/혁신적/학제간 연구자 피드백."
    recommended: true
  - label: "직접 선택"
    description: "원하는 페르소나를 직접 선택합니다."
    recommended: false

multiSelect: true  # For "직접 선택" case
fallback: "핵심 3명"
```

### CP-CS-002: Feedback Incorporation

```yaml
id: CP-CS-002
type: APPROVAL
phase: "creativity/community-simulation"

question:
  header: "피드백 반영"
  text: "어떤 피드백을 반영할까요?"
  context: "[각 페르소나 피드백 표시]"

options:
  # Dynamically generated based on feedback
  - label: "[페르소나 이름]: [피드백 요약]"
    description: "[상세 피드백]"

multiSelect: true
fallback: "모든 피드백 반영"
```

---

## Agent-Specific Checkpoints

### CP-AG-001: Ethics Confirmation (Agent 04)

```yaml
id: CP-AG-001
type: GUARDRAIL
phase: "Agent 04 - Research Ethics Advisor"

question:
  header: "윤리 확인"
  text: "다음 윤리적 고려사항을 확인하셨습니까?"
  context: "[식별된 윤리적 이슈 목록]"

options:
  - label: "예, 확인했습니다"
    description: "모든 윤리적 고려사항을 인지하고 대응 계획이 있습니다."
    recommended: true
  - label: "추가 가이드 필요"
    description: "윤리적 대응 방안에 대한 상세 가이드를 요청합니다."
    recommended: false

multiSelect: false
fallback: "추가 가이드 필요"
```

### CP-AG-002: Critique Acceptance (Agent 03)

```yaml
id: CP-AG-002
type: APPROVAL
phase: "Agent 03 - Devil's Advocate"

question:
  header: "비판 수용"
  text: "다음 비판 중 어떤 것을 수용/반영하시겠습니까?"
  context: "[비판 목록]"

options:
  # Dynamically generated based on critiques

multiSelect: true
fallback: "모든 비판 검토 후 선택적 반영"
```

### CP-AG-003: Bias Acknowledgment (Agent 16)

```yaml
id: CP-AG-003
type: GUARDRAIL
phase: "Agent 16 - Bias Detector"

question:
  header: "편향 인지"
  text: "다음 잠재적 편향을 인지하셨습니까?"
  context: "[식별된 편향 목록]"

options:
  - label: "예, 인지하고 대응 계획이 있습니다"
    description: "각 편향에 대한 완화 전략이 준비되어 있습니다."
    recommended: true
  - label: "완화 전략 가이드 필요"
    description: "각 편향에 대한 구체적 완화 전략을 요청합니다."
    recommended: false

multiSelect: false
fallback: "완화 전략 가이드 필요"
```

---

## End Checkpoint

### CP-END-001: Overall Satisfaction

```yaml
id: CP-END-001
type: ITERATION
phase: "research completion"

question:
  header: "최종 확인"
  text: "전체 결과에 만족하시나요?"

options:
  - label: "예, 완료합니다"
    description: "연구 설계/분석을 완료합니다."
    recommended: true
  - label: "특정 단계 재실행"
    description: "특정 에이전트나 단계를 다시 실행합니다."
    recommended: false
  - label: "전체 재시작"
    description: "처음부터 다시 시작합니다."
    recommended: false

multiSelect: false
fallback: "예, 완료합니다"
```

---

## Implementation Notes

### AskUserQuestion Integration

Each checkpoint translates to an AskUserQuestion call:

```markdown
**AskUserQuestion 호출**:
- header: "{checkpoint.question.header}"
- question: "{checkpoint.question.text}"
- options: [
    {
      label: "{option.label}",
      description: "{option.description}"
    },
    ...
  ]
- multiSelect: {checkpoint.multiSelect}
```

### Checkpoint Flow Control

```python
def process_checkpoint(checkpoint_id, context):
    """
    Process a user checkpoint and return user's selection.
    """
    checkpoint = get_checkpoint(checkpoint_id)

    # Build AskUserQuestion parameters
    question_params = {
        "header": checkpoint.question.header,
        "text": checkpoint.question.text,
        "options": checkpoint.options,
        "multiSelect": checkpoint.multiSelect
    }

    # If context is provided, add it
    if checkpoint.question.context:
        question_params["context"] = checkpoint.question.context

    # Call AskUserQuestion
    response = ask_user_question(**question_params)

    # Handle response
    if response is None:
        return checkpoint.fallback

    return response
```
```

**Step 2: Verify file created**

Run: `wc -l .claude/skills/research-coordinator/interaction/user-checkpoints.md`
Expected: ~500+ lines

**Step 3: Commit**

```bash
git add .claude/skills/research-coordinator/interaction/user-checkpoints.md
git commit -m "feat(interaction): add comprehensive user checkpoint system"
```

---

## Phase 3: Creativity Modules

### Task 3.1: Create Forced Analogy Module

**Files:**
- Create: `.claude/skills/research-coordinator/creativity/forced-analogy.md`

**Step 1: Write forced-analogy.md**

```markdown
---
name: forced-analogy
description: |
  Forced Analogy creative mechanism for cross-domain concept mapping.
  Brings concepts from unrelated fields to generate novel frameworks.
version: "3.0.0"
---

# Forced Analogy Mechanism

## Overview

Forces creative thinking by mapping concepts from unrelated domains to the research topic, generating novel theoretical frameworks and perspectives.

## Source Domain Pool

```yaml
natural_sciences:
  ecology:
    - ecological_succession: "Pioneer → Climax stages"
    - food_web: "Energy transfer networks"
    - niche_theory: "Resource partitioning"
    - symbiosis: "Mutualism, parasitism, commensalism"

  physics:
    - entropy: "Disorder and equilibrium"
    - quantum_superposition: "Multiple states until observed"
    - relativity: "Frame-dependent perspectives"
    - wave_particle_duality: "Dual nature phenomena"

  chemistry:
    - catalysis: "Accelerators without consumption"
    - equilibrium: "Dynamic balance"
    - phase_transition: "State changes at thresholds"

  biology:
    - evolution: "Selection and adaptation"
    - homeostasis: "Self-regulation"
    - emergence: "Complex from simple"

humanities:
  philosophy:
    - dialectics: "Thesis-antithesis-synthesis"
    - phenomenology: "Lived experience focus"
    - pragmatism: "Truth through utility"

  history:
    - punctuated_equilibrium: "Stability interrupted by change"
    - path_dependency: "Historical constraints on present"

  linguistics:
    - semiotics: "Sign systems and meaning"
    - speech_acts: "Language as action"

arts:
  music_theory:
    - harmony_dissonance: "Tension and resolution"
    - rhythm_patterns: "Temporal structures"

  architecture:
    - form_follows_function: "Purpose-driven design"
    - negative_space: "Importance of absence"

  design:
    - affordance: "Perceived possibilities"
    - gestalt: "Whole greater than parts"

other:
  economics:
    - supply_demand: "Market equilibrium"
    - externalities: "Unintended consequences"

  anthropology:
    - liminality: "Threshold states"
    - rites_of_passage: "Transition rituals"
```

## Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│                  Forced Analogy Process                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Step 1: Source Selection                                   │
│  ⬜ CP-FA-001: Select source domain                         │
│     - Random (maximum creativity)                           │
│     - Natural Sciences                                      │
│     - Humanities                                            │
│     - Custom specification                                  │
│                                                             │
│  Step 2: Concept Extraction                                 │
│     - Select 2-3 concepts from source domain                │
│     - Identify key characteristics                          │
│     - Note structural relationships                         │
│                                                             │
│  Step 3: Mapping Generation                                 │
│     - Map source concepts to target research                │
│     - Identify parallel structures                          │
│     - Generate novel terminology                            │
│                                                             │
│  Step 4: Framework Synthesis                                │
│     - Construct new theoretical framework                   │
│     - Define key constructs                                 │
│     - Specify relationships                                 │
│                                                             │
│  Step 5: Approval                                           │
│  ⬜ CP-FA-002: Review and approve analogy                   │
│     - Accept and apply                                      │
│     - Request alternative                                   │
│     - Skip                                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Output Format

```markdown
## Forced Analogy Result

### Source Domain
**Field**: [e.g., Ecology]
**Concept**: [e.g., Ecological Succession]
**Key Characteristics**:
- [Characteristic 1]
- [Characteristic 2]

### Target Domain
**Research Topic**: [User's research topic]
**Current Framing**: [Existing approach]

### Mapping

| Source Element | Target Element | Rationale |
|---------------|----------------|-----------|
| [Pioneer stage] | [Early adopters] | [Explanation] |
| [Climax community] | [Mainstream adoption] | [Explanation] |

### Proposed Framework

**Name**: "[Generated Framework Name]"
(e.g., "Ecological Succession Model of EdTech Adoption")

**Core Constructs**:
1. [Construct 1]: Definition
2. [Construct 2]: Definition

**Relationships**:
- [Construct 1] → [Construct 2]: [Nature of relationship]

**Theoretical Contribution**:
[How this framework advances understanding]

### T-Score Assessment
Estimated T-Score: [0.15-0.25] (Innovative)
Justification: [Why this is novel]
```

## Example

**Research Topic**: AI chatbots for language learning anxiety reduction

**Source**: Ecology - Ecological Succession

**Mapping**:
- Pioneer species → Early adopter students (risk-tolerant)
- Facilitation → Peer influence and scaffolding
- Inhibition → Technology resistance
- Climax community → Full integration into learning ecosystem

**Generated Framework**: "Ecological Succession Model of Educational Technology Integration (ESMETI)"

**T-Score**: 0.18 (Highly innovative, requires strong justification)
```

**Step 2: Commit**

```bash
git add .claude/skills/research-coordinator/creativity/forced-analogy.md
git commit -m "feat(creativity): add forced analogy mechanism"
```

---

### Task 3.2: Create Iterative Loop Module

**Files:**
- Create: `.claude/skills/research-coordinator/creativity/iterative-loop.md`

**Step 1: Write iterative-loop.md**

```markdown
---
name: iterative-loop
description: |
  Iterative Divergent-Convergent Loop for idea refinement.
  Cycles through exploration and synthesis phases.
version: "3.0.0"
---

# Iterative Loop Mechanism

## Overview

Implements multiple rounds of divergent (exploration) and convergent (synthesis) thinking to refine ideas progressively.

## Process Structure

```
┌─────────────────────────────────────────────────────────────┐
│                    Iterative Loop (4 Rounds)                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ROUND 1: Wide Exploration (Divergent)                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Goal: Generate maximum options without constraints    │   │
│  │                                                      │   │
│  │ Process:                                             │   │
│  │   - Suspend all guardrails temporarily               │   │
│  │   - Generate 10-15 diverse ideas                     │   │
│  │   - Include unconventional approaches                │   │
│  │   - No evaluation at this stage                      │   │
│  │                                                      │   │
│  │ ⬜ CP-IL-001: "Select interesting directions"        │   │
│  │    (Multi-select from generated options)             │   │
│  └─────────────────────────────────────────────────────┘   │
│         │                                                   │
│         ▼                                                   │
│  ROUND 2: Cross-Pollination (Combinatorial)                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Goal: Combine and synthesize selected directions     │   │
│  │                                                      │   │
│  │ Process:                                             │   │
│  │   - Take 2-3 most interesting directions             │   │
│  │   - Find unexpected combinations                     │   │
│  │   - Generate hybrid approaches                       │   │
│  │   - Create novel integrations                        │   │
│  │                                                      │   │
│  │ ⬜ CP-IL-002: "Approve combination?"                 │   │
│  │    (Review and approve proposed combination)         │   │
│  └─────────────────────────────────────────────────────┘   │
│         │                                                   │
│         ▼                                                   │
│  ROUND 3: Constraint Application (Convergent)              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Goal: Apply academic guardrails and feasibility      │   │
│  │                                                      │   │
│  │ Process:                                             │   │
│  │   - Re-enable guardrails                             │   │
│  │   - Evaluate methodological soundness                │   │
│  │   - Check feasibility constraints                    │   │
│  │   - Identify required justifications                 │   │
│  │                                                      │   │
│  │ ⬜ CP-IL-003: "Select guardrail level"               │   │
│  │    Options: Strict / Balanced / Flexible             │   │
│  └─────────────────────────────────────────────────────┘   │
│         │                                                   │
│         ▼                                                   │
│  ROUND 4: Synthesis (Final Convergent)                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Goal: Produce refined, defensible output             │   │
│  │                                                      │   │
│  │ Process:                                             │   │
│  │   - Synthesize best elements                         │   │
│  │   - Create coherent framework                        │   │
│  │   - Document rationale                               │   │
│  │   - Prepare defense arguments                        │   │
│  │                                                      │   │
│  │ ⬜ CP-IL-004: "Approve final result?"                │   │
│  │    Options: Approve / Another round / Start over     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Configuration

```yaml
iterative_loop_config:
  max_rounds: 4
  round_1_options: 10-15
  round_2_combinations: 3-5

  guardrail_levels:
    strict:
      - peer_review_defensible: required
      - validated_instruments: required
      - established_methods: required
    balanced:
      - peer_review_defensible: required
      - validated_instruments: preferred
      - established_methods: flexible
    flexible:
      - peer_review_defensible: preferred
      - validated_instruments: optional
      - established_methods: optional

  user_can_extend: true
  max_total_rounds: 6
```

## Output Format

```markdown
## Iterative Loop Results

### Round 1: Wide Exploration
**Generated Options** (15):
1. [Option description] - T-Score: [X.X]
2. [Option description] - T-Score: [X.X]
...

**User Selected**: [Options X, Y, Z]

### Round 2: Cross-Pollination
**Combinations Generated**:
- Combo A: [Option X] × [Option Y] → [Hybrid description]
- Combo B: [Option Y] × [Option Z] → [Hybrid description]

**User Approved**: Combo A

### Round 3: Constraint Application
**Guardrail Level**: Balanced

**Evaluation**:
| Criterion | Status | Notes |
|-----------|--------|-------|
| Peer-review defensible | ✅ | [Justification] |
| Validated instruments | ⚠️ | [Adaptation needed] |
| Methodological soundness | ✅ | [Justification] |

### Round 4: Synthesis
**Final Output**:
[Refined, defensible recommendation with full rationale]

**Defense Arguments**:
1. [Argument 1]
2. [Argument 2]
```
```

**Step 2: Commit**

```bash
git add .claude/skills/research-coordinator/creativity/iterative-loop.md
git commit -m "feat(creativity): add iterative divergent-convergent loop"
```

---

### Task 3.3: Create Semantic Distance Module

**Files:**
- Create: `.claude/skills/research-coordinator/creativity/semantic-distance.md`

**Step 1: Write semantic-distance.md**

```markdown
---
name: semantic-distance
description: |
  Semantic Distance Scorer for recommending conceptually distant combinations.
  Uses embedding-based distance to prioritize innovative pairings.
version: "3.0.0"
---

# Semantic Distance Mechanism

## Overview

Calculates semantic distance between theories/concepts using embeddings and prioritizes combinations that are far apart, encouraging innovative cross-pollination.

## Distance Calculation

```python
def calculate_semantic_distance(concept_a, concept_b):
    """
    Calculate semantic distance between two concepts.

    Returns:
        float: Distance score (0.0 = identical, 1.0 = maximally different)
    """
    embedding_a = get_embedding(concept_a)
    embedding_b = get_embedding(concept_b)

    cosine_similarity = dot(embedding_a, embedding_b) / (norm(a) * norm(b))
    distance = 1 - cosine_similarity

    return distance
```

## Distance Thresholds

```yaml
distance_thresholds:
  close:
    range: "0.0 - 0.3"
    description: "Very similar concepts, low innovation"
    risk: low
    recommendation: "Safe but limited differentiation"

  moderate:
    range: "0.3 - 0.5"
    description: "Related but distinct"
    risk: low
    recommendation: "Good balance"

  far:
    range: "0.5 - 0.7"
    description: "Meaningfully different"
    risk: medium
    recommendation: "Recommended for innovation"

  very_far:
    range: "0.7 - 0.85"
    description: "Substantially different domains"
    risk: medium-high
    recommendation: "Strong justification needed"

  extreme:
    range: "0.85 - 1.0"
    description: "Maximally different"
    risk: high
    recommendation: "Experimental, very strong justification"
```

## Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│                Semantic Distance Process                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Step 1: Input Collection                                   │
│     - User's base theory/concept                            │
│     - Research domain                                       │
│     - Target creativity level                               │
│                                                             │
│  Step 2: Candidate Generation                               │
│     - Query theory database for candidates                  │
│     - Include cross-domain options                          │
│                                                             │
│  Step 3: Distance Calculation                               │
│     - Calculate distance for all pairs                      │
│     - Rank by distance (descending)                         │
│                                                             │
│  Step 4: Threshold Selection                                │
│  ⬜ CP-SD-001: Select distance threshold                    │
│     - Close (>0.3): Safe                                    │
│     - Moderate (>0.5): Balanced (recommended)               │
│     - Far (>0.7): Innovative                                │
│     - Extreme (>0.85): Experimental                         │
│                                                             │
│  Step 5: Recommendation                                     │
│     - Present top 5 combinations above threshold            │
│                                                             │
│  Step 6: Selection                                          │
│  ⬜ CP-SD-002: Select combination(s)                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Pre-computed Theory Embeddings

```yaml
# Example theory embeddings (simplified representation)
theory_embeddings:
  TAM:
    domain: "technology_adoption"
    cluster: "acceptance_models"

  SDT:
    domain: "motivation"
    cluster: "psychological_needs"

  Ecological_Succession:
    domain: "ecology"
    cluster: "temporal_change"

  Dialectics:
    domain: "philosophy"
    cluster: "synthesis_processes"

# Pre-computed distances (sample)
distance_matrix:
  TAM_to_SDT: 0.35
  TAM_to_Ecological_Succession: 0.82
  TAM_to_Dialectics: 0.78
  SDT_to_Ecological_Succession: 0.75
  SDT_to_Dialectics: 0.65
```

## Output Format

```markdown
## Semantic Distance Analysis

### Base Concept
**Theory/Concept**: [User's base theory]
**Domain**: [Domain]

### Candidate Combinations (sorted by distance)

| Rank | Candidate | Distance | Risk | Potential |
|------|-----------|----------|------|-----------|
| 1 | [Theory A] | 0.85 | High | ★★★★★ |
| 2 | [Theory B] | 0.78 | Medium-High | ★★★★ |
| 3 | [Theory C] | 0.65 | Medium | ★★★ |
| 4 | [Theory D] | 0.52 | Low-Medium | ★★ |
| 5 | [Theory E] | 0.38 | Low | ★ |

### Recommended Combination
**Selected**: [Base] × [Candidate]
**Distance**: [X.XX]
**Rationale**: [Why this combination is promising]

### Integration Proposal
[How to integrate the two concepts]
```
```

**Step 2: Commit**

```bash
git add .claude/skills/research-coordinator/creativity/semantic-distance.md
git commit -m "feat(creativity): add semantic distance scorer"
```

---

### Task 3.4: Create Temporal Reframing Module

**Files:**
- Create: `.claude/skills/research-coordinator/creativity/temporal-reframing.md`

**Step 1: Write temporal-reframing.md**

```markdown
---
name: temporal-reframing
description: |
  Temporal Reframing mechanism for perspective shifts across time.
  Examines research from past, future, and parallel perspectives.
version: "3.0.0"
---

# Temporal Reframing Mechanism

## Overview

Shifts temporal perspective to reveal hidden assumptions and limitations in current research framing.

## Perspectives

### Past Perspective (1990s)

```yaml
past_perspective:
  timeframe: "1990s"
  question: "If we conducted this research in the 1990s, what would be different?"

  analysis_points:
    - dominant_theories: "What theories were mainstream then?"
    - technology_context: "What technology existed?"
    - methodological_norms: "What methods were standard?"
    - missing_concepts: "What concepts didn't exist yet?"

  insights:
    - historical_constraints: "Why did research evolve this way?"
    - path_dependency: "What alternatives were foreclosed?"
    - theoretical_gaps: "What wasn't explained then that is now?"
```

### Future Perspective (2035)

```yaml
future_perspective:
  timeframe: "2035 (10 years ahead)"
  question: "How will this research be viewed in 10 years?"

  analysis_points:
    - likely_advances: "What will probably change?"
    - current_limitations: "What will seem naive?"
    - emerging_paradigms: "What new frameworks might exist?"
    - technology_evolution: "How will technology change context?"

  insights:
    - temporal_limitations: "What's specific to our current moment?"
    - future_proofing: "How can we make research more durable?"
    - anticipatory_design: "What future developments should we consider?"
```

### Parallel Perspective (Alternate History)

```yaml
parallel_perspective:
  concept: "Alternate developmental trajectory"
  question: "If this field had developed differently, what would we be studying?"

  analysis_points:
    - key_branching_points: "What were pivotal moments?"
    - alternate_outcomes: "What if different choices were made?"
    - suppressed_alternatives: "What approaches were abandoned?"
    - cross_field_imports: "What could we borrow from other fields?"

  insights:
    - hidden_assumptions: "What do we take for granted?"
    - alternative_frameworks: "What other ways of seeing exist?"
    - theoretical_diversity: "What's missing from current discourse?"
```

## Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│                Temporal Reframing Process                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ⬜ CP-TR-001: Select perspective(s)                        │
│     - Past (1990s)                                          │
│     - Future (2035)                                         │
│     - Parallel Universe                                     │
│     - All (recommended)                                     │
│                                                             │
│         │                                                   │
│         ▼                                                   │
│  For each selected perspective:                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 1. Contextualize research in that timeframe         │   │
│  │ 2. Identify what would be different                 │   │
│  │ 3. Extract insights for current research            │   │
│  │ 4. Generate recommendations                         │   │
│  └─────────────────────────────────────────────────────┘   │
│         │                                                   │
│         ▼                                                   │
│  Synthesis:                                                 │
│     - Cross-perspective insights                            │
│     - Recommendations for strengthening research            │
│     - Novel angles revealed                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Output Format

```markdown
## Temporal Reframing Analysis

### Research Topic
[User's research topic]

---

### Past Perspective (1990s)

**Context**: In the 1990s, [describe historical context]

**Key Differences**:
- Dominant theory was [X] instead of [Y]
- Technology context: [description]
- Methodological norms: [description]

**Insights**:
- [Insight 1]: [implication for current research]
- [Insight 2]: [implication for current research]

---

### Future Perspective (2035)

**Projected Context**: By 2035, [anticipated changes]

**Current Limitations Revealed**:
- [Limitation 1]: Will likely seem [X]
- [Limitation 2]: May be superseded by [Y]

**Future-Proofing Recommendations**:
- [Recommendation 1]
- [Recommendation 2]

---

### Parallel Perspective

**Alternate Trajectory**: If [key branching point] had gone differently...

**Suppressed Alternatives**:
- [Alternative 1]: Was abandoned because [reason], but could be revisited
- [Alternative 2]: Never gained traction, but offers [potential]

**Cross-Field Possibilities**:
- From [Field X]: [concept] could inform [aspect of research]

---

### Synthesis

**Cross-Perspective Insights**:
1. [Synthesized insight]
2. [Synthesized insight]

**Recommendations**:
- [Concrete recommendation for strengthening research]
- [Novel angle to consider]
```
```

**Step 2: Commit**

```bash
git add .claude/skills/research-coordinator/creativity/temporal-reframing.md
git commit -m "feat(creativity): add temporal reframing mechanism"
```

---

### Task 3.5: Create Community Simulation Module

**Files:**
- Create: `.claude/skills/research-coordinator/creativity/community-simulation.md`

**Step 1: Write community-simulation.md**

```markdown
---
name: community-simulation
description: |
  Virtual Research Community Simulation for diverse feedback.
  Simulates feedback from 7 researcher personas with different perspectives.
version: "3.0.0"
---

# Community Simulation Mechanism

## Overview

Simulates a virtual academic community with diverse perspectives to provide multi-faceted feedback on research proposals.

## Persona Pool (7 Researchers)

```yaml
personas:
  conservative_methodologist:
    icon: "🔬"
    name: "Dr. Method"
    role: "Conservative Methodologist"
    perspective: "Values rigor, validated methods, established approaches"
    typical_concerns:
      - "Is this methodologically sound?"
      - "Has this approach been validated?"
      - "What are the threats to validity?"
    feedback_style: "Cautious, detail-oriented, risk-averse"

  innovation_seeker:
    icon: "🚀"
    name: "Dr. Nova"
    role: "Innovation Seeker"
    perspective: "Values novelty, paradigm shifts, creative approaches"
    typical_concerns:
      - "What's new here?"
      - "How does this advance the field?"
      - "Is this too incremental?"
    feedback_style: "Enthusiastic about novelty, pushes for more"

  interdisciplinary_researcher:
    icon: "🌐"
    name: "Dr. Bridge"
    role: "Interdisciplinary Researcher"
    perspective: "Values cross-domain connections, synthesis"
    typical_concerns:
      - "How does this connect to other fields?"
      - "What can we learn from [other domain]?"
      - "Are we missing perspectives?"
    feedback_style: "Suggests connections, broadens scope"

  literature_expert:
    icon: "📚"
    name: "Dr. Cite"
    role: "Literature Expert"
    perspective: "Values comprehensive literature grounding"
    typical_concerns:
      - "What does the literature say?"
      - "Have you considered [classic work]?"
      - "How does this fit the existing discourse?"
    feedback_style: "References prior work, situates in context"

  junior_researcher:
    icon: "👨‍🎓"
    name: "Dr. Fresh"
    role: "Junior Researcher"
    perspective: "Values practicality, clarity, accessibility"
    typical_concerns:
      - "How do I actually implement this?"
      - "What are the practical steps?"
      - "Is this feasible with limited resources?"
    feedback_style: "Practical questions, implementation focus"

  emeritus_professor:
    icon: "🏛️"
    name: "Dr. Sage"
    role: "Emeritus Professor"
    perspective: "Values historical context, long-term impact"
    typical_concerns:
      - "How does this fit the field's trajectory?"
      - "What's the lasting contribution?"
      - "Have we seen similar ideas before?"
    feedback_style: "Historical perspective, big picture"

  industry_researcher:
    icon: "🏢"
    name: "Dr. Applied"
    role: "Industry Researcher"
    perspective: "Values practical application, real-world impact"
    typical_concerns:
      - "Can this be applied in practice?"
      - "What's the real-world impact?"
      - "Who will use this?"
    feedback_style: "Application-focused, impact-oriented"
```

## Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│             Community Simulation Process                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ⬜ CP-CS-001: Select personas for feedback                 │
│     - All 7 personas                                        │
│     - Core 3 (Conservative, Innovation, Interdisciplinary) │
│     - Custom selection                                      │
│                                                             │
│         │                                                   │
│         ▼                                                   │
│  For each selected persona:                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 1. Present research proposal to persona             │   │
│  │ 2. Generate persona-specific feedback               │   │
│  │ 3. Identify concerns from their perspective         │   │
│  │ 4. Suggest improvements                             │   │
│  └─────────────────────────────────────────────────────┘   │
│         │                                                   │
│         ▼                                                   │
│  Feedback Compilation:                                      │
│     - Organize by persona                                   │
│     - Identify consensus points                             │
│     - Highlight divergent views                             │
│                                                             │
│  ⬜ CP-CS-002: Select feedback to incorporate               │
│     - Multi-select from feedback items                      │
│                                                             │
│         │                                                   │
│         ▼                                                   │
│  Integration:                                               │
│     - Apply selected feedback                               │
│     - Document rationale for selections                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Output Format

```markdown
## Community Simulation Feedback

### Research Proposal Summary
[Brief description of what was evaluated]

---

### Individual Feedback

#### 🔬 Dr. Method (Conservative Methodologist)
**Overall Assessment**: [Positive/Cautious/Concerned]

**Strengths Noted**:
- [Strength 1]

**Concerns**:
- [Concern 1]: [Explanation]
- [Concern 2]: [Explanation]

**Suggestions**:
- [Suggestion 1]

---

#### 🚀 Dr. Nova (Innovation Seeker)
**Overall Assessment**: [Enthusiastic/Neutral/Disappointed]

**Strengths Noted**:
- [Strength 1]

**Concerns**:
- [Concern 1]: [Explanation]

**Suggestions**:
- [Suggestion 1]

---

[Continue for each selected persona...]

---

### Synthesis

**Consensus Points** (Agreed by 3+ personas):
- [Point 1]
- [Point 2]

**Divergent Views**:
| Topic | Dr. Method | Dr. Nova | Dr. Bridge |
|-------|------------|----------|------------|
| [Topic] | [View] | [View] | [View] |

**Priority Recommendations**:
1. [High priority] - Raised by [X] personas
2. [Medium priority] - Raised by [X] personas

---

### User Selection
[After CP-CS-002, document which feedback was incorporated and why]
```

## Persona Response Templates

Each persona has characteristic phrases and concerns:

```yaml
response_templates:
  conservative_methodologist:
    praise: "The methodological approach is sound because..."
    concern: "I'm concerned about the validity threat from..."
    suggestion: "Consider adding a robustness check for..."

  innovation_seeker:
    praise: "This is a fresh approach that could..."
    concern: "This seems too similar to existing work in..."
    suggestion: "What if we pushed further by..."

  # ... templates for other personas
```
```

**Step 2: Commit**

```bash
git add .claude/skills/research-coordinator/creativity/community-simulation.md
git commit -m "feat(creativity): add community simulation mechanism"
```

---

## Phase 4: Reference Documents & Agent Updates

### Task 4.1: Create New Reference Documents

**Files:**
- Create: `.claude/skills/research-coordinator/references/creativity-mechanisms.md`
- Create: `.claude/skills/research-coordinator/references/user-checkpoint-schema.md`
- Create: `.claude/skills/research-coordinator/references/dynamic-t-score-spec.md`

[Content abbreviated for length - each file documents the specifications for its respective module]

**Commit:**
```bash
git add .claude/skills/research-coordinator/references/
git commit -m "docs(references): add v3.0 specification documents"
```

---

### Task 4.2: Update agent-registry.yaml

**Files:**
- Modify: `.claude/skills/research-coordinator/references/agent-registry.yaml`

**Changes:**
- Add `version: "3.0.0"` to header
- Add `upgrade_level`, `creativity_integration`, `checkpoints`, `dynamic_t_score` fields to each agent
- Update workflow definitions

**Commit:**
```bash
git add .claude/skills/research-coordinator/references/agent-registry.yaml
git commit -m "feat(registry): update agent registry for v3.0"
```

---

### Task 4.3: Update Master SKILL.md

**Files:**
- Modify: `.claude/skills/research-coordinator/SKILL.md`

**Changes:**
- Update version to 3.0.0
- Add module references (core/, creativity/, interaction/)
- Update execution flow with checkpoints
- Add creativity module integration

**Commit:**
```bash
git add .claude/skills/research-coordinator/SKILL.md
git commit -m "feat: upgrade master SKILL.md to v3.0"
```

---

### Task 4.4: Upgrade FULL VS Agents (5 agents)

**Files:**
- Modify: `.claude/skills/research-agents/02-theoretical-framework-architect/SKILL.md`
- Modify: `.claude/skills/research-agents/03-devils-advocate/SKILL.md`
- Modify: `.claude/skills/research-agents/05-systematic-literature-scout/SKILL.md`
- Modify: `.claude/skills/research-agents/10-statistical-analysis-guide/SKILL.md`
- Modify: `.claude/skills/research-agents/16-bias-detector/SKILL.md`

**Changes for each:**
- Add v3.0 frontmatter with `upgrade_level: FULL`
- Add module references
- Add checkpoint integrations
- Add creativity module hooks

**Commit:**
```bash
git add .claude/skills/research-agents/02-*/SKILL.md
git add .claude/skills/research-agents/03-*/SKILL.md
git add .claude/skills/research-agents/05-*/SKILL.md
git add .claude/skills/research-agents/10-*/SKILL.md
git add .claude/skills/research-agents/16-*/SKILL.md
git commit -m "feat(agents): upgrade 5 FULL VS agents to v3.0"
```

---

### Task 4.5: Upgrade ENHANCED VS Agents (6 agents)

**Files:**
- Modify agents 01, 04, 06, 07, 08, 09

**Commit:**
```bash
git commit -m "feat(agents): upgrade 6 ENHANCED VS agents to v3.0"
```

---

### Task 4.6: Upgrade LIGHT VS Agents (9 agents)

**Files:**
- Modify agents 11-15, 17-20

**Commit:**
```bash
git commit -m "feat(agents): upgrade 9 LIGHT VS agents to v3.0"
```

---

## Phase 5: Installation & Documentation

### Task 5.1: Update marketplace.json

**Files:**
- Modify: `.claude-plugin/marketplace.json`

**Commit:**
```bash
git commit -m "feat(install): update marketplace.json for v3.0 modules"
```

---

### Task 5.2: Update install.sh

**Files:**
- Modify: `scripts/install.sh`

**Commit:**
```bash
git commit -m "feat(install): update installer for v3.0 module structure"
```

---

### Task 5.3: Update Documentation

**Files:**
- Modify: `README.md`
- Modify: `CLAUDE.md`
- Modify: `docs/README-ko.md`
- Modify: `docs/AGENT-REFERENCE.md`
- Create: `docs/CREATIVITY-GUIDE.md`
- Create: `docs/MIGRATION-v2-to-v3.md`

**Commit:**
```bash
git commit -m "docs: update all documentation for v3.0"
```

---

### Task 5.4: Final Version Bump & Tag

**Commit:**
```bash
git add .
git commit -m "release: Research Coordinator v3.0.0"
git tag -a v3.0.0 -m "Release v3.0.0 - Creativity Suite"
```

---

## Summary

| Phase | Tasks | Estimated Commits |
|-------|-------|-------------------|
| Phase 1: Core Infrastructure | 3 | 3 |
| Phase 2: Interaction Module | 1 | 1 |
| Phase 3: Creativity Modules | 5 | 5 |
| Phase 4: References & Agents | 6 | 6 |
| Phase 5: Install & Docs | 4 | 4 |
| **Total** | **19** | **19** |
